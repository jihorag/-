#!/usr/bin/env python3
"""2차 논술 이론·법규 기출문제 전수 추출 (제1~36회 기출문제지 PDF → essay JSON).
 · 회차 헤더 "제N회 감정평가사 2차 시험문제지" 로 회차 분할
 · "【 문제 N 】 {전문} (N점)" 블록 추출 (사례형 다물음 포함)
 · 법규: _단원별_출제빈도.md 의 '회차별 4문제→단원' 표로 정확 배정
 · 이론: 21논점 키워드 매칭으로 단원 배정 (미스매치는 best-effort)
모범답안은 비워둠(자기채점 키워드 + AI 채점). EssayMode 스키마와 동일.
"""
import json, re, datetime, unicodedata, glob
from pathlib import Path
import pypdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'Claude KAPA CHATING copy'
OUT_BASE = ROOT / 'viewer/public/data/essay'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

THEORY_CH = {
    1: '감정평가 기초·분류·절차', 2: '부동산 가치이론·가격형성', 3: '가격제원칙·시장론·시장분석',
    4: '3방식 개관·거래사례비교법', 5: '원가법', 6: '수익환원법', 7: '기타방식·임료',
    8: '기업가치·물건별 평가', 9: '부동산투자·금융론', 10: '부동산정책론·기타논점',
}
LAW_CH = {
    1: '행정법 개관·일반원칙·행정법관계', 2: '행정입법·행정행위', 3: '행정계획·인허가의제·공법상계약',
    4: '행정절차·실효성확보수단', 5: '행정쟁송(심판·취소소송)', 6: '행정상 손해전보',
    7: '공용수용(사업인정·재결)', 8: '손실보상(보상기준·환매·생활보상)', 9: '부동산 가격공시법',
    10: '감정평가법·도정법',
}

# 이론 단원별 키워드 (21논점 + 단원명 기반) — 회차 문제→단원 배정용
THEORY_KW = {
    1: ['감정평가의 기초', '감정평가의 분류', '감정평가의 절차', '평가절차', '직업윤리', '감정평가제도', '평가제도', '감정평가의 의의', '감정평가의 기능', '감정평가사', '기본적 사항', '기준시점', '기준가치', '대상물건 확정'],
    2: ['가치이론', '가격형성', '가치형성요인', '가격형성요인', '지역분석', '개별분석', '가치발생', '가치형성', '효용', '희소성', '위치지대', '지대', '입지', '가치와 가격', '가치의 종류', '교환가치', '투자가치', '인근지역', '유사지역', '동일수급권', '정상가격', '적정가격', '최빈매매', '균형가격', 'Age-cycle', '지역요인'],
    3: ['가격제원칙', '최유효이용', '시장론', '시장분석', '경기변동', '부동산시장', '시장성', '대체의 원칙', '균형의 원칙', '기여의 원칙', '예측의 원칙', '변동의 원칙', '적합', '시장흡수율', '흡수율', '하위시장', '시장의 효율성', 'TOPEKA', '토페카', '허프', 'Huff', '소매인력', 'Reilly', '라일리', '상권', '주택여과', '여과', '도시공간', '입지론', '컨버스'],
    4: ['3방식', '삼방식', '거래사례비교법', '비교방식', '시산가액', '시산가격', '사정보정', '시점수정', '지역요인', '개별요인', '방식의 병용', '시산조정', '산식'],
    5: ['원가법', '재조달원가', '감가수정', '적산가액', '내용연수', '잔가율', '복성', '관찰감가', '정액법', '정률법'],
    6: ['수익환원법', '환원이율', '환원율', '수익방식', 'DCF', 'NOI', '순수익', '할인현금', '자본환원', '직접환원', '소득접근', '자본회수'],
    7: ['임료', '임대료', '적산법', '수익분석법', '임대사례비교법', '기타방식', '회귀분석', '노선가', '입체이용', '입체이용률', '공중권', '구분지상권', '지상권', '한계심도', '구분지상'],
    8: ['기업가치', '물건별', '무형자산', '권리금', '영업권', '특허', '지식재산', '동산', '의제부동산', '광업', '어업', '소음', '오염', '공장', '공장재단', '산림', '입목', '과수', '구분소유', '집합건물', '비가치추계', '타당성', '특수토지', '구분건물', '환경', '일단지', '비상장주식', '사모', '주식펀드', '건부감가', '광천지', '골프장'],
    9: ['투자분석', '부동산금융', '포트폴리오', 'LTV', 'DTI', '레버리지', '투자위험', '수익률', '리츠', 'REITs', '증권화', '부동산투자', '금융론', '위험과 수익', 'Project Financing', 'PF', 'Sensitivity'],
    10: ['부동산정책', '조세', '개발이익', '공시제도', '담보평가', '경매', '소송감정', 'ESG', '탄소', '빅데이터', '도시정비', '정책론', '감정평가와 정책', '공시지가', '표준지', '분양가상한제', '분양가', '재건축', '매도청구'],
}

# 강제 배정(키워드 점수보다 우선) — 명백한 단일 논점
THEORY_OVERRIDES = [
    ('TOPEKA', 3), ('토페카', 3), ('허프', 3), ('Huff', 3), ('소매인력', 3), ('Reilly', 3),
    ('주택여과', 3), ('여과현상', 3), ('분양가상한제', 10), ('매도청구', 10),
    ('일단지', 8), ('비상장주식', 8), ('사모', 8), ('한계심도', 7), ('건부감가', 8),
    ('정상가격과', 2), ('적정가격', 2), ('인근지역', 2), ('최빈매매', 2),
    ('정비사업', 8), ('관리처분', 8), ('종후자산', 8), ('종전자산', 8),
    ('보증부월세', 7), ('보증금', 7), ('기능적 감가', 5), ('치유불가능', 5), ('치유가능', 5),
    ('지상권이 설정', 7), ('실거래가', 10),
]


def level_from_points(points):
    """배점 기반 학습 단계(1~5). 기출 자체가 약술~종합으로 단계가 갈림."""
    p = points or 0
    if p >= 40: return 5
    if p >= 25: return 4
    if p >= 15: return 3
    if p >= 8:  return 2
    return 1


def wrap_bare_term(body):
    """부모 '약술하라' 헤더가 분리된 단답 stub(예: '수몰민 보상 (20점)')을 독립 프롬프트로 복원."""
    b = body.strip()
    # 물음 동사가 전혀 없고 짧으면 약술 프롬프트로 감쌈
    if len(b) <= 40 and not re.search(r'(시오|하라|하시오|인가|는가|\?|구하|설명|논하|약술|서술|기술|검토|비교)', b):
        term = re.sub(r'\s*\(\s*\d+\s*점\s*\)\s*$', '', b).strip(' .·')
        pts = re.search(r'\(\s*(\d+)\s*점\s*\)', b)
        if term:
            return f"「{term}」에 관하여 약술하시오." + (f" ({pts.group(1)}점)" if pts else '')
    return body


def norm(s):
    return unicodedata.normalize('NFC', s)


def find_pdf(subdir, keyword):
    for f in glob.glob(str(SRC / subdir / '*.pdf')):
        if keyword in norm(Path(f).name):
            return f
    return None


def pdf_text(path):
    r = pypdf.PdfReader(path)
    return '\n'.join((p.extract_text() or '') for p in r.pages)


def clean_body(b):
    # 헤더/페이지 노이즈 제거
    b = re.sub(r'STUDY\s*FIGHTER[^\n]*', ' ', b)
    b = re.sub(r'\d{4}년도\s*제\s*\d+\s*회[^\n]*', ' ', b)
    b = re.sub(r'교\s*시\s*시험과목[^\n]*', ' ', b)
    b = re.sub(r'\d교시\s*감정평가[^\n]*분', ' ', b)
    b = re.sub(r'감정평가(이론|법규)\s*\d+\s*회\s*기출문제', ' ', b)
    # 다음 회차 페이지 머리(예: "3 1991년도", "10 1997년도")가 꼬리에 남는 것 제거
    b = re.sub(r'\s*\d{1,3}\s*(19|20)\d{2}년도\s*$', '', b)
    b = re.sub(r'\s*\d{1,3}\s*$', '', b)  # 꼬리 페이지번호
    b = re.sub(r'[ \t]+', ' ', b)
    b = re.sub(r'\n{2,}', '\n', b).strip()
    b = trim_law_bleed(b)
    return b


# 물음 종결 어미(한국어 시험 문항의 다양한 끝맺음)
ASK_END = re.compile(r'(시오|하라|하시오|답하라|약술하라|논하라|논급하라|구하라|쓰시오'
                     r'|인가|는가|은가|가\?|\?|보시오|밝히시오|기술하시오|서술하시오)\s*[\.)）]?\s*(\(\s*\d+\s*점\s*\))?\s*$')


def trim_law_bleed(b):
    """물음이 끝난 뒤 다음 문제의 법령/시행령 발췌가 꼬리에 붙은 경우 잘라냄.
    물음 종결 직후 '「…법…」' 또는 '제N조(' 로 시작하는 100자+ 법조문 블록만 제거(보수적)."""
    m = re.search(r'(\(\s*\d+\s*점\s*\)\s*)\n?\s*(「[^」]*법[^」]*」|제\s*\d+\s*조\s*\()', b)
    if m:
        head = b[:m.start(2)].rstrip()
        tail = b[m.start(2):]
        # 잘라낼 꼬리가 충분히 길고(다음문제 자료로 추정), head가 물음으로 끝나면 trim
        if len(tail) > 80 and ASK_END.search(head[-25:]):
            return head
    return b


def extract_rounds(text):
    """회차 헤더로 분할 → {round: segment_text}."""
    # "제N회 감정평가사 2차" 위치
    marks = [(int(m.group(1)), m.start()) for m in re.finditer(r'제\s*0*(\d+)\s*회\s*감정평가사', text)]
    if not marks:
        return {}
    out = {}
    for idx, (rnd, start) in enumerate(marks):
        end = marks[idx + 1][1] if idx + 1 < len(marks) else len(text)
        # 같은 회차가 여러 번 잡히면 가장 긴 세그먼트 유지
        seg = text[start:end]
        if rnd not in out or len(seg) > len(out[rnd]):
            out[rnd] = seg
    return out


def extract_questions(seg):
    """세그먼트에서 '【 문제 N 】' 블록 추출 → [(qnum, body, points)]."""
    parts = list(re.finditer(r'【\s*문제\s*(\d+)\s*】', seg))
    qs = []
    for idx, m in enumerate(parts):
        qnum = int(m.group(1))
        b_start = m.end()
        b_end = parts[idx + 1].start() if idx + 1 < len(parts) else len(seg)
        body = clean_body(seg[b_start:b_end])
        pts = [int(x) for x in re.findall(r'\(?\s*(\d+)\s*점\s*\)?', body)]
        points = max(pts) if pts else 25
        if 5 <= len(body) <= 2000:
            qs.append((qnum, body, points))
    return qs


def law_round_chapter_map():
    """_단원별_출제빈도.md → {round: [ch1,ch2,ch3,ch4]}."""
    md = (SRC / '2차 - 감정평가법규_학습자료/_최종산출물_법규/_단원별_출제빈도.md').read_text(encoding='utf-8')
    mp = {}
    for m in re.finditer(r'\|\s*제(\d+)회\s*\|([^\n]+)\|', md):
        rnd = int(m.group(1))
        cells = [c.strip() for c in m.group(2).split('|')]
        chs = []
        for c in cells[:4]:
            chs.append(int(c) if c.isdigit() else None)
        mp[rnd] = chs
    return mp


def theory_chapter_for(body):
    """이론 본문 → (단원, 매칭 논점 키워드 리스트). override 우선."""
    for sub, ch in THEORY_OVERRIDES:
        if sub in body:
            return ch, [sub]
    scores = {ch: 0 for ch in THEORY_CH}
    hits = {ch: [] for ch in THEORY_CH}
    for ch, kws in THEORY_KW.items():
        for kw in kws:
            if kw in body:
                scores[ch] += (3 if len(kw) >= 4 else 1)
                hits[ch].append(kw)
    best = max(scores, key=scores.get)
    if scores[best] <= 0:
        return None, []
    return best, hits[best][:3]


def law_points_for(body, ch_title):
    """법규 본문에서 간단 논점 태그(앞부분 핵심어) + 단원명."""
    pts = [ch_title]
    return pts


def build_subject(out_dir, subject, ch_titles, pdf_path, chapter_fn):
    text = pdf_text(pdf_path)
    rounds = extract_rounds(text)
    by_ch = {ch: [] for ch in ch_titles}
    n_total, n_unmapped = 0, 0
    for rnd in sorted(rounds):
        for (qnum, body, points) in extract_questions(rounds[rnd]):
            ch, lpoints = chapter_fn(rnd, qnum, body)
            if ch is None:
                n_unmapped += 1
                ch = 1  # 미배정은 1단원로 폴백
            body = wrap_bare_term(body)
            by_ch.setdefault(ch, []).append({'round': rnd, 'qnum': qnum, 'body': body,
                                             'points': points, 'logicalPoints': lpoints or []})
            n_total += 1

    out_dir.mkdir(parents=True, exist_ok=True)
    chapters_meta, total = [], 0
    for ch in sorted(ch_titles):
        items = by_ch.get(ch, [])
        items.sort(key=lambda x: (x['round'], x['qnum']))
        questions, rset = [], set()
        for i, it in enumerate(items, 1):
            rset.add(it['round'])
            lvl = level_from_points(it['points'])
            questions.append({
                'id': f"ki-{out_dir.name}-c{ch}-r{it['round']}-q{it['qnum']}",
                'subject': subject, 'chapter': str(ch), 'source': 'official',
                'round': it['round'], 'questionNum': it['qnum'], 'points': it['points'],
                'body': it['body'], 'modelAnswer': '', 'modelAnswerSource': '',
                'keyPoints': [], 'logicalPoints': it.get('logicalPoints', []),
                'level': lvl, 'difficulty': lvl,
                'answerFormat': '', 'subchapter': f"{ch}-1",
            })
        total += len(questions)
        (out_dir / f"{ch}.json").write_text(json.dumps({
            'built_at': NOW, 'subject': subject, 'chapter': str(ch), 'chapterTitle': ch_titles[ch],
            'source': 'official', 'count': len(questions), 'withAnswer': 0, 'matchedAnswer': 0,
            'rounds': sorted(rset), 'questions': questions,
        }, ensure_ascii=False, indent=1), encoding='utf-8')
        chapters_meta.append({
            'id': str(ch), 'title': ch_titles[ch], 'file': f"{ch}.json", 'count': len(questions),
            'withAnswer': 0, 'matchedAnswer': 0, 'rounds': sorted(rset), 'generatedCount': 0,
            'subchapters': [{'id': f"{ch}-1", 'title': ch_titles[ch], 'keywords': []}],
        })
    (out_dir / 'manifest.json').write_text(json.dumps({
        'built_at': NOW, 'subject': subject, 'total': total, 'classified': total, 'chapters': chapters_meta,
    }, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"  {subject}: {len(rounds)}회차, 총 {total}문항 (미배정 폴백 {n_unmapped}) → {out_dir}")


def main():
    print("2차 기출문제 전수 추출 (기출문제지 PDF)")
    # 이론
    t_pdf = find_pdf('2차 - 감정평가이론_학습자료', '기출문제지')
    build_subject(OUT_BASE / 'theory', '감정평가이론', THEORY_CH, t_pdf,
                  lambda rnd, qn, body: theory_chapter_for(body))
    # 법규 — 회차 매핑 표
    lmap = law_round_chapter_map()
    l_pdf = find_pdf('2차 - 감정평가법규_학습자료', '기출문제지')

    def law_ch(rnd, qn, body):
        chs = lmap.get(rnd)
        if chs and 1 <= qn <= len(chs) and chs[qn - 1]:
            c = chs[qn - 1]
            return c, [LAW_CH[c]]
        return None, []
    build_subject(OUT_BASE / 'law', '감정평가 및 보상법규', LAW_CH, l_pdf, law_ch)
    print("완료")


if __name__ == '__main__':
    main()
