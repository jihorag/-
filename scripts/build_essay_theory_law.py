#!/usr/bin/env python3
"""2차 논술 이론·법규 essay 데이터 생성 (골격 MVP).
소스: 'Claude KAPA CHATING copy' 의 _최종산출물 단원/논점 마크다운에서 실제 기출 논점을 추출 →
EssayMode가 읽는 manifest.json + chapter JSON(실무와 동일 스키마) 으로 변환.
모범답안은 비워두고(빈 문자열) AI 채점/자기채점으로 학습. 전수 기출 PDF 추출은 단계적 확장.
"""
import json, re, datetime, unicodedata
from pathlib import Path


def list_units(d):
    """macOS NFD 한글 파일명 대응 — '단원_NN_*.md' 파일을 정규화 매칭으로 수집."""
    out = []
    for f in d.iterdir():
        name = unicodedata.normalize('NFC', f.name)
        m = re.match(r'단원_(\d+)_.*\.md$', name)
        if m:
            out.append((int(m.group(1)), f))
    return sorted(out)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'Claude KAPA CHATING copy'
OUT_BASE = ROOT / 'viewer/public/data/essay'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

THEORY_DIR = SRC / '2차 - 감정평가이론_학습자료/_최종산출물_이론_v2'
LAW_DIR = SRC / '2차 - 감정평가법규_학습자료/_최종산출물_법규'

# 단원 번호 → (title, 영역)
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
STAR_POINTS = {3: 40, 2: 30, 1: 20}


def keypoints_from(title):
    toks = re.split(r'[·,()\s]+', title)
    return [t for t in toks if len(t) >= 2][:6]


def build_theory():
    """_논점별_출제빈도.md 표 → 21 논점 essay 문항."""
    md = (THEORY_DIR / '_논점별_출제빈도.md').read_text(encoding='utf-8')
    # | ★★★ | [17] | 물건별 평가 | 16회 ([...]) | 8 |
    rows = re.findall(r'\|\s*(★+)\s*\|\s*\[(\d+)\]\s*\|\s*([^|]+?)\s*\|\s*(\d+)회[^|]*\|\s*(\d+)\s*\|', md)
    by_ch = {}
    for stars, lnum, name, freq, ch in rows:
        ch = int(ch); star = len(stars)
        q = {
            'logum': int(lnum), 'name': name.strip(), 'star': star,
            'freq': int(freq), 'points': STAR_POINTS.get(star, 25),
        }
        by_ch.setdefault(ch, []).append(q)
    return by_ch


def build_law():
    """각 단원 md의 '논점별 기출모음 발췌' 에서 번호형 논점 라벨 추출 → 단원별 essay 문항."""
    by_ch = {}
    for ch, f in list_units(LAW_DIR):
        text = f.read_text(encoding='utf-8')
        # 핵심요약서 논점 아웃라인의 "01 공용수용" 형태 번호 라벨을 전체에서 추출
        # (이름 클래스에서 개행 제외 → 한 줄 논점만, 줄 넘나드는 잡음 방지)
        labels = re.findall(r'(?m)^[ \t]*(\d{2})[ \t]+([가-힣][가-힣A-Za-z0-9·()· \t]{3,28})[ \t]*$', text)
        GENERIC = {'근거', '특징', '요건', '의의', '내용', '효과', '유형', '절차', '배경', '취지',
                   '개념', '개설', '개요', '문제점', '한계', '비교', '구별', '종류', '성질', '기능',
                   '인정여부', '판단기준', '권리구제', '법적성질', '의의·취지', '서설', '결어'}
        seen, items = set(), []
        for _num, name in labels:
            name = re.sub(r'\s+', ' ', name).strip()
            if name in seen or name in GENERIC:
                continue
            # 한글 글자수 5+ 또는 띄어쓰기 포함(복합 논점)만 채택 → generic 단어 배제
            hangul = len(re.findall(r'[가-힣]', name))
            if hangul < 5 and ' ' not in name:
                continue
            if any(b in name for b in ['스터디파이터', '문제모음', '기출모음', '강의', '제1장', '제2장', 'Part', 'PART', 'p.']):
                continue
            seen.add(name)
            items.append({'name': name, 'points': 25})
        if items:
            by_ch[ch] = items[:16]  # 단원당 최대 16개
    return by_ch


def write_subject(out_dir, subject, ch_titles, by_ch, make_body):
    out_dir.mkdir(parents=True, exist_ok=True)
    chapters_meta = []
    total = 0
    for ch in sorted(ch_titles):
        items = by_ch.get(ch, [])
        questions = []
        for i, it in enumerate(items, 1):
            name = it['name']
            qid = f"tl-{out_dir.name}-c{ch}-q{i}"
            questions.append({
                'id': qid, 'subject': subject, 'chapter': str(ch),
                'source': 'past-topic', 'round': None, 'questionNum': i,
                'points': it.get('points', 25),
                'body': make_body(name, it),
                'modelAnswer': '', 'modelAnswerSource': '',
                'keyPoints': keypoints_from(name),
                'difficulty': 4 if it.get('star', 2) >= 3 else 3,
                'answerFormat': '', 'subchapter': f"{ch}-1",
            })
        total += len(questions)
        # chapter JSON
        (out_dir / f"{ch}.json").write_text(json.dumps({
            'built_at': NOW, 'subject': subject, 'chapter': str(ch),
            'chapterTitle': ch_titles[ch], 'source': 'past-topic',
            'count': len(questions), 'withAnswer': 0, 'matchedAnswer': 0,
            'rounds': [], 'questions': questions,
        }, ensure_ascii=False, indent=1), encoding='utf-8')
        chapters_meta.append({
            'id': str(ch), 'title': ch_titles[ch], 'file': f"{ch}.json",
            'count': len(questions), 'withAnswer': 0, 'matchedAnswer': 0,
            'rounds': [], 'generatedCount': 0,
            'subchapters': [{'id': f"{ch}-1", 'title': ch_titles[ch], 'keywords': keypoints_from(ch_titles[ch])}],
        })
    (out_dir / 'manifest.json').write_text(json.dumps({
        'built_at': NOW, 'subject': subject, 'total': total, 'classified': total,
        'chapters': chapters_meta,
    }, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"  {subject}: {len([c for c in chapters_meta if c['count']>0])}개 단원 채움 / {len(chapters_meta)}, 총 {total}문항 → {out_dir}")
    return total


def main():
    print("이론·법규 2차 논술 데이터 생성")
    t_by_ch = build_theory()
    write_subject(OUT_BASE / 'theory', '감정평가이론', THEORY_CH, t_by_ch,
                  lambda name, it: f"「{name}」에 관하여 논술하시오. (기출 {it['freq']}회 출제 · 약 {it.get('points',25)}점)")
    l_by_ch = build_law()
    write_subject(OUT_BASE / 'law', '감정평가 및 보상법규', LAW_CH, l_by_ch,
                  lambda name, it: f"「{name}」에 관하여 설명하시오.")
    print("완료")


if __name__ == '__main__':
    main()
