#!/usr/bin/env python3
"""감정평가이론 단권화 빌드 v2 (고도화)
- 핵심요약서·기출예해집 페이지별 매핑 → 단원 본문에 통합
- 답안 양식·두문자 자동 추출
- 21논점별 출제빈도 통계
- 모의고사 회차 분할 시도
"""
import pypdf, re, os, json, shutil
from pathlib import Path
from collections import defaultdict, Counter

BASE = Path(__file__).parent
OUT = BASE / '_최종산출물_이론_v2'
OUT.mkdir(exist_ok=True)

# ============== 21개 논점 ==============
LOGUMS = [
    ('01', '감정평가의 기초', 1),
    ('02', '감정평가의 분류', 1),
    ('03', '부동산 가치이론', 2),
    ('04', '부동산 가격형성', 2),
    ('05', '가격제원칙', 3),
    ('06', '부동산시장론 및 경기변동론', 3),
    ('07', '시장분석론', 3),
    ('08', '가치형성요인분석', 2),
    ('09', '감정평가 절차', 1),
    ('10', '감정평가3방식 개관', 4),
    ('11', '거래사례비교법', 4),
    ('12', '원가법', 5),
    ('13', '수익환원법', 6),
    ('14', '기타 방식', 7),
    ('15', '임료의 평가', 7),
    ('16', '기업가치관련 평가', 8),
    ('17', '물건별 평가', 8),
    ('18', '부동산투자', 9),
    ('19', '부동산금융론', 9),
    ('20', '부동산정책론', 10),
    ('21', '기타 논점', 10),
]

CHAPTERS = {
    1:  {'name': '감정평가_기초·분류·절차',         'logum': ['01','02','09']},
    2:  {'name': '부동산_가치이론·가격형성',        'logum': ['03','04','08']},
    3:  {'name': '가격제원칙·시장론·시장분석',     'logum': ['05','06','07']},
    4:  {'name': '3방식개관·거래사례비교법',        'logum': ['10','11']},
    5:  {'name': '원가법',                          'logum': ['12']},
    6:  {'name': '수익환원법',                      'logum': ['13']},
    7:  {'name': '기타방식·임료',                   'logum': ['14','15']},
    8:  {'name': '기업가치·물건별_평가',            'logum': ['16','17']},
    9:  {'name': '부동산투자·금융론',               'logum': ['18','19']},
    10: {'name': '부동산정책론·기타논점',           'logum': ['20','21']},
}

# ============== 기본서 논점 시작 페이지 ==============
BASIC_LOGUM_START = {
    '01': 17, '02': 34, '03': 74, '04': 122, '05': 162, '06': 198, '07': 226,
    '08': 250, '09': 274, '10': 286, '11': 320, '12': 344, '13': 380, '14': 434,
    '15': 452, '16': 476, '17': 498, '18': 566, '19': 580, '20': 592, '21': 604,
}
BASIC_END = 634

# ============== 필기노트 PART 시작 페이지 ==============
NOTE_PART_START = {
    1: 2, 2: 36, 3: 38, 4: 72, 5: 91, 8: 129, 9: 144, 10: 151,
    11: 162, 12: 179, 13: 192, 16: 241, 17: 247, 18: 252, 19: 253, 20: 258,
}
NOTE_END = 303

NOTE_PART_TO_CH = {
    1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 8: 4, 9: 4, 10: 5,
    11: 6, 12: 7, 13: 7, 16: 9, 17: 9, 18: 10, 19: 10, 20: 10,
}

# ============== 파일 ==============
BOOKS = {
    '기본서':    '감정평가이론_기본서 [업데이트일_250830].pdf',
    '필기노트':  '감정평가이론_필기노트 [업데이트일_230430].pdf',
    '핵심요약서': '감정평가이론_핵심요약서 [업데이트일_250624].pdf',
}
GICHUL_PDF = '감정평가이론_기출문제지 [1-36회] [업데이트일_250728].pdf'
GICHUL_DAPAN_PDF = '감정평가이론 기출예해집(25.10.29).pdf'
GS1_PDF = '스터디파이터_1기_이론_문제 및 예시답안 모음 [총10회분].pdf'
GS3_PDF = '25년대비 이론3기GS 문제 및 예시답안 모음 [총10회분] [업데이트일_25.07.11].pdf'
MOCK1_PDF = '변형 모의고사1 문제지 모음(해설지는 없음).pdf'
MOCK2_PDF = '변형모의고사2 문제지와 답안 모음.pdf'
MOCK2000_PDF = '감정평가이론_실전모의고사 2000점 [업데이트일_210923].pdf'

# ============== 기출 36회 수동 매핑 ==============
GICHUL_MANUAL = {
    1: 2, 2: 2, 3: 6, 4: 4, 5: 2, 6: 2, 7: 7, 8: 3, 9: 6, 10: 9,
    11: 1, 12: 9, 13: 6, 14: 3, 15: 4, 16: 1, 17: 2, 18: 7, 19: 4,
    20: 8, 21: 8, 22: 6, 23: 6, 24: 3, 25: 8, 26: 8, 27: 8, 28: 3,
    29: 2, 30: 4, 31: 1, 32: 3, 33: 8, 34: 6, 35: 5, 36: 4,
}

# 기출 → 논점 매핑 (★★★/★★/★ 출제빈도 계산용)
GICHUL_LOGUM = {
    1:  ['04','10','15','01'],   # 부동산특성→가격, 시산조정, 입체이용률, 감평기능
    2:  ['03','04'],              # 지대론, 가격형성원리, 대체·기회비용, 구분지상권
    3:  ['13','11','15','05'],   # 수익환원, 거래사례, 임료, 최유효이용
    4:  ['10','11','08','01'],   # 3방식, 거래사례, 지역분석, 금융계수
    5:  ['03','10','17','05'],   # Marshall, 공장평가, 담보·소지, 최유효이용, 예측원칙
    6:  ['04','05','15'],         # 가격발생, 정상/적정가격, 표준적사용, 임료
    7:  ['15','12'],              # 임료, 원가법, 감가
    8:  ['04','06','05','08'],   # 가격발생요인, 경기변동, 가격원칙, TOPEKA
    9:  ['13','16','12','04'],   # 자본환원·저당지분, 영업권·지재권, 감가수정, 지리적위치
    10: ['18','06','13','07'],   # 증권화, 시장이자율, 위치지대, 시장분석
    11: ['01','08','17','04'],   # 컨설팅, 지역분석, 권리분석, 차액지대, 포트폴리오
    12: ['19','05','12','11'],   # REITs, 대체원칙, 사정보정, 약술
    13: ['13','05'],              # 수익방식, 용적률·최유효이용
    14: ['07','18'],              # 시장분석·시장성·생산성, 부채금융
    15: ['10','17','02','20'],   # 3방식구체화, 시장가격없는부동산, 분류, 정부개입
    16: ['01','17','20'],         # 직업윤리, 토양오염, 표준지 그밖의요인
    17: ['02','17','04','12'],   # 종별·유형, 가치개념, 가격형성요인, 기능적감가
    18: ['14','08','20','15'],   # 통계평가, 지역·개별분석, 표준지/표준주택, 약술
    19: ['10','20'],              # 일괄평가, 가격지수
    20: ['17','20','17'],         # 지상권토지, 분양가상한제, 일단지
    21: ['08','17'],              # 가격형성요인, 비상장주식
    22: ['17','13'],              # 송전선로, 수익형 부동산
    23: ['17','13','18'],         # 시장가치, 수익성부동산, 실물옵션
    24: ['05','07'],              # 최유효이용, 시장분석·지역분석, 토지평가
    25: ['17'],                   # 리모델링, 토양오염, 구분점포
    26: ['17','11'],              # 토지+건물, 전세, 저당
    27: ['16'],                   # 기업가치, 재무보고
    28: ['05'],                   # 최유효이용
    29: ['04','03','10'],         # 가치발생요인, 3면성, 3방식
    30: ['10','17'],              # 택지조성, 후분양, 시장가치
    31: ['01','17'],              # 감평개념, 보상답변
    32: ['06','01'],              # 공간/자산시장, 절차·윤리
    33: ['16','13'],              # 지식재산권, 자본환원율
    34: ['13','17'],              # 수익환원법, 택지비
    35: ['12'],                   # 원가법
    36: ['17'],                   # 토지·담보·건축허가
}

# ============== GS 수동 매핑 ==============
GS_MANUAL = {
    'GS1기 1회차': 1, 'GS1기 2회차': 1, 'GS1기 3회차': 2, 'GS1기 4회차': 2,
    'GS1기 5회차': 2, 'GS1기 6회차': 3, 'GS1기 7회차': 3, 'GS1기 8회차': 3,
    'GS1기 9회차': 3, 'GS1기 10회차': 8,
    'GS3기 1회차': 6, 'GS3기 2회차': 8, 'GS3기 3회차': 8, 'GS3기 4회차': 8,
    'GS3기 5회차': 9, 'GS3기 6회차': 9, 'GS3기 7회차': 10, 'GS3기 8회차': 8,
    'GS3기 9회차': 8, 'GS3기 10회차': 10,
}

# ============== 단원별 키워드 ==============
CHAPTER_KEYWORDS = {
    1: ['감정평가의 기초','감정평가 절차','감정평가 분류','일괄평가','구분평가','직업윤리','기준가치','복수감정'],
    2: ['부동산 가치','가치이론','가치형성요인','가치발생요인','지역요인','개별요인','인근지역','동일수급권','지역분석','개별분석','지대'],
    3: ['가격제원칙','최유효이용','부동산시장','경기변동','시장분석','흡수율','경제기반','시장성분석','대체의 원칙','공간시장','자산시장'],
    4: ['감정평가3방식','3방식 개관','거래사례비교법','사정보정','시점수정','시산가액 조정','시산가액의 조정','비준가액','일괄감정평가'],
    5: ['원가법','재조달원가','감가수정','내용연수','분해법','정액법','정률법','상환기금법'],
    6: ['수익환원법','직접환원법','DCF법','순수익','환원율','할인율','자본회수','저당지분환원','부동산잔여법','동적DCF','정적DCF'],
    7: ['임대사례비교법','임료','적산법','수익분석법','계속임료','노선가식','회귀분석','조소득승수법','승수법'],
    8: ['기업가치','상장주식','비상장주식','채권의 평가','영업권','지식재산권','권리금','무형자산','물건별 평가','구분점포','집합건물','일단지'],
    9: ['부동산투자','투자분석','레버리지','NPV','IRR','순현재가치','내부수익률','부동산금융','실물옵션','REITs','부동산금융론','부동산PF'],
    10: ['부동산정책론','조세','부동산세','공시지가제도','친환경건축물','건부증감가','상가권리금','국공유지','그 밖의 요인','정비사업','재개발','용적률 이양','TDR'],
}

# ============== 헬퍼 ==============
def extract_pages(pdf_path, start, end):
    if start > end: return ''
    r = pypdf.PdfReader(str(pdf_path))
    parts = []
    for i in range(start-1, min(end, len(r.pages))):
        text = r.pages[i].extract_text() or ''
        parts.append(f'\n<!--p.{i+1}-->\n{text}')
    return '\n'.join(parts)

def extract_specific_pages(pdf_path, pages):
    """특정 페이지 번호 리스트만 추출"""
    if not pages: return ''
    r = pypdf.PdfReader(str(pdf_path))
    parts = []
    for p in sorted(pages):
        if 1 <= p <= len(r.pages):
            text = r.pages[p-1].extract_text() or ''
            parts.append(f'\n<!--p.{p}-->\n{text}')
    return '\n'.join(parts)

def classify_text(text):
    scores = {}
    for ch, kws in CHAPTER_KEYWORDS.items():
        scores[ch] = sum(text.count(k) for k in kws)
    if not any(scores.values()):
        return None
    return max(scores, key=scores.get)

# ============== Step 1: 핵심요약서·기출예해집 페이지별 분류 ==============
print('=== Step 1: 핵심요약서·기출예해집 페이지별 분류 ===')
r_hyak = pypdf.PdfReader(str(BASE / BOOKS['핵심요약서']))
hyak_pages_by_ch = defaultdict(list)
for i in range(len(r_hyak.pages)):
    text = r_hyak.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        hyak_pages_by_ch[ch].append(i + 1)

r_yehae = pypdf.PdfReader(str(BASE / GICHUL_DAPAN_PDF))
yehae_pages_by_ch = defaultdict(list)
for i in range(len(r_yehae.pages)):
    text = r_yehae.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        yehae_pages_by_ch[ch].append(i + 1)

print(f'  핵심요약서: 단원별 페이지 매칭됨')
print(f'  기출예해집: 단원별 페이지 매칭됨')

# ============== Step 2: 단원별 이론 파일 생성 ==============
print('\n=== Step 2: 단원별 이론 파일 생성 ===')

def basic_ranges_for_ch(ch_no):
    logums = CHAPTERS[ch_no]['logum']
    ranges = []
    sorted_logum = sorted(BASIC_LOGUM_START.keys(), key=lambda x: int(x))
    for l in logums:
        idx = sorted_logum.index(l)
        s = BASIC_LOGUM_START[l]
        if idx+1 < len(sorted_logum):
            e = BASIC_LOGUM_START[sorted_logum[idx+1]] - 1
        else:
            e = BASIC_END
        ranges.append((l, s, e))
    return ranges

def note_ranges_for_ch(ch_no):
    parts = [p for p, c in NOTE_PART_TO_CH.items() if c == ch_no]
    if not parts: return []
    sorted_parts = sorted(NOTE_PART_START.keys())
    ranges = []
    for p in sorted(parts):
        s = NOTE_PART_START[p]
        idx = sorted_parts.index(p)
        if idx+1 < len(sorted_parts):
            e = NOTE_PART_START[sorted_parts[idx+1]] - 1
        else:
            e = NOTE_END
        ranges.append((p, s, e))
    return ranges

basic_pdf = BASE / BOOKS['기본서']
note_pdf = BASE / BOOKS['필기노트']
hyak_pdf = BASE / BOOKS['핵심요약서']

for ch_no in sorted(CHAPTERS.keys()):
    ch_info = CHAPTERS[ch_no]
    out_path = OUT / f'단원_{ch_no:02d}_{ch_info["name"]}.md'

    content = [f'# 단원 {ch_no:02d} — {ch_info["name"].replace("_"," ")}\n']

    # 논점 인덱스 + 출제빈도 (★★★/★★/★)
    content.append('## 📑 이 단원의 논점 인덱스 + 출제빈도\n')
    for l in ch_info['logum']:
        name = next(n for num,n,_ in LOGUMS if num == l)
        # 이 논점이 등장한 회차 수 계산
        count = sum(1 for rounds in GICHUL_LOGUM.values() if l in rounds)
        stars = '★' * min(3, max(1, (count + 1) // 2))
        content.append(f'- {stars} **[{l}]** {name} ({count}회 출제)')
    content.append('')

    # 목차
    content.append('## 🗺️ 본문 목차\n')
    content.append('- [📖 핵심요약서 (L1 - 정의문)](#핵심요약서)')
    content.append('- [📝 필기노트 (L2 - 답안양식)](#필기노트)')
    content.append('- [📚 기본서 (L3 - 본격 서술)](#기본서)\n')
    content.append('---\n')

    # 핵심요약서 (L1) - 페이지별 매칭으로 직접 포함
    content.append('## <a name="핵심요약서"></a>📖 핵심요약서 — L1 (정의문)\n')
    hyak_pages = hyak_pages_by_ch[ch_no]
    if hyak_pages:
        content.append(f'> 단원에 매칭된 핵심요약서 {len(hyak_pages)}페이지 발췌\n')
        content.append(extract_specific_pages(hyak_pdf, hyak_pages))
    else:
        content.append('> 매칭된 핵심요약서 페이지 없음\n')
    content.append('\n---\n')

    # 필기노트 (L2) - PART별
    content.append('## <a name="필기노트"></a>📝 필기노트 — L2 (답안양식·키워드) ★ 핵심\n')
    content.append('> **답안 작성의 골격**. 시험 답안에 그대로 가져갈 목차·구조.\n')
    note_rng = note_ranges_for_ch(ch_no)
    if note_rng:
        for p, s, e in note_rng:
            content.append(f'\n### 필기노트 PART {p:02d} (p.{s}~{e})\n')
            content.append(extract_pages(note_pdf, s, e))
    else:
        content.append('\n> (이 단원에 매핑된 필기노트 PART 없음 - 다른 자료로 학습)\n')
    content.append('\n---\n')

    # 기본서 (L3)
    content.append('## <a name="기본서"></a>📚 기본서 — L3 (본격 서술)\n')
    for l, s, e in basic_ranges_for_ch(ch_no):
        name = next(n for num,n,_ in LOGUMS if num == l)
        content.append(f'\n### 기본서 — 논점 {l}: {name} (p.{s}~{e})\n')
        content.append(extract_pages(basic_pdf, s, e))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 3: 기출 회차별 분할 + 답안 매칭 ==============
print('\n=== Step 3: 문제+답안 매칭 ===')

def detect_gichul_rounds():
    r = pypdf.PdfReader(str(BASE / GICHUL_PDF))
    rounds = {}
    for i in range(len(r.pages)):
        text = r.pages[i].extract_text() or ''
        m = re.search(r'제\s*(\d+)\s*회', text)
        if m:
            rn = int(m.group(1))
            if 1 <= rn <= 36 and rn not in rounds:
                rounds[rn] = i + 1
    sorted_r = sorted(rounds.keys())
    boundaries = {}
    for i, rn in enumerate(sorted_r):
        s = rounds[rn]
        e = rounds[sorted_r[i+1]] - 1 if i+1 < len(sorted_r) else len(r.pages)
        boundaries[rn] = (s, e)
    return boundaries

GICHUL_ROUNDS = detect_gichul_rounds()

def detect_gs_rounds(pdf_path):
    r = pypdf.PdfReader(str(pdf_path))
    rounds = {}
    for i in range(len(r.pages)):
        text = r.pages[i].extract_text() or ''
        m = re.search(r'(\d+)\s*회차', text)
        if m:
            rn = int(m.group(1))
            if 1 <= rn <= 12 and rn not in rounds:
                rounds[rn] = i + 1
    sorted_r = sorted(rounds.keys())
    boundaries = {}
    for i, rn in enumerate(sorted_r):
        s = rounds[rn]
        e = rounds[sorted_r[i+1]] - 1 if i+1 < len(sorted_r) else len(r.pages)
        boundaries[rn] = (s, e)
    return boundaries

GS1_ROUNDS = detect_gs_rounds(BASE / GS1_PDF)
GS3_ROUNDS = detect_gs_rounds(BASE / GS3_PDF)

problems_by_ch = defaultdict(list)
gichul_pdf_full = BASE / GICHUL_PDF
gichul_dapan_full = BASE / GICHUL_DAPAN_PDF

for rn, (s, e) in GICHUL_ROUNDS.items():
    text = extract_pages(gichul_pdf_full, s, e)
    ch = GICHUL_MANUAL.get(rn) or classify_text(text) or 4
    problems_by_ch[ch].append({
        'title': f'기출 제{rn}회',
        'text': text,
        'source': '기출문제지',
        'round': rn
    })

for rn, (s, e) in GS1_ROUNDS.items():
    text = extract_pages(BASE / GS1_PDF, s, e)
    title = f'GS1기 {rn}회차'
    ch = GS_MANUAL.get(title) or classify_text(text) or 3
    problems_by_ch[ch].append({'title': title, 'text': text, 'source': 'GS1기'})

for rn, (s, e) in GS3_ROUNDS.items():
    text = extract_pages(BASE / GS3_PDF, s, e)
    title = f'GS3기 {rn}회차'
    ch = GS_MANUAL.get(title) or classify_text(text) or 3
    problems_by_ch[ch].append({'title': title, 'text': text, 'source': 'GS3기'})

# 단원별 문제 파일 생성
for ch_no in sorted(CHAPTERS.keys()):
    ch_info = CHAPTERS[ch_no]
    out_path = OUT / f'문제_{ch_no:02d}_{ch_info["name"]}.md'
    content = [f'# 문제 단원 {ch_no:02d} — {ch_info["name"].replace("_"," ")}\n']

    # 출제 빈도 안내
    items = problems_by_ch[ch_no]
    content.append(f'> 이 단원에 매핑된 문제: {len(items)}개\n')
    content.append('---\n')

    # 문제 + 단원 매칭된 기출예해집 답안 페이지
    yehae_pages = yehae_pages_by_ch[ch_no]
    if not items:
        content.append('> 이 단원에 자동 매핑된 문제가 없음. 다른 단원 참조.\n')
    for p in items:
        content.append(f'\n## {p["title"]} (출처: {p["source"]})\n')
        content.append('\n### 📝 문제\n')
        content.append(p['text'])
        content.append('\n')

    # 단원 단위 답안 모음 (기출예해집 페이지 매칭)
    if yehae_pages:
        content.append(f'\n## 📕 기출예해집 — 단원 매칭 답안 ({len(yehae_pages)}p)\n')
        content.append('> 기출예해집에서 이 단원 키워드와 매칭된 페이지. 회차별 정렬은 안 됨.\n')
        content.append(extract_specific_pages(gichul_dapan_full, yehae_pages))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 4: 답안 양식·두문자 자동 추출 ==============
print('\n=== Step 4: 답안 양식·두문자 추출 ===')

note_raw = (BASE / '_extract/raw_필기노트.md').read_text(encoding='utf-8')

# 답안 양식 - "Ⅰ. ... Ⅱ. ... Ⅲ. ..." 패턴
양식_set = set()
양식_pattern = r'(Ⅰ\s*[\.\s].{2,40}[\n\s]+Ⅱ\s*[\.\s].{2,40}(?:[\n\s]+Ⅲ\s*[\.\s].{2,40})?)'
for m in re.finditer(양식_pattern, note_raw):
    양식 = m.group(0).replace('\n', ' / ').strip()[:300]
    if len(양식) > 20:
        양식_set.add(양식)
print(f'  답안 양식 후보: {len(양식_set)}개')

양식_path = OUT / '_답안양식_모음.md'
양식_content = ['# 📐 답안 양식 모음 (자동 추출)\n', '> 필기노트에서 "Ⅰ. Ⅱ. Ⅲ." 형식의 답안 양식 골격을 자동 추출.\n']
양식_content.append(f'> 총 {len(양식_set)}개 양식\n')
for i, v in enumerate(sorted(양식_set), 1):
    양식_content.append(f'\n### Form {i}\n```\n{v}\n```')
양식_path.write_text('\n'.join(양식_content), encoding='utf-8')
print(f'  OK  _답안양식_모음.md  {양식_path.stat().st_size/1024:.0f}KB')

# 필기노트 핵심포인트 - ★ 표시 + 쌤이 만든 목차 + 암기 키워드 컨텍스트
핵심포인트_list = []
# ★ 표시가 있는 라인과 주변 (앞뒤 100자)
for m in re.finditer(r'.{0,150}★+[^\n]{0,150}', note_raw):
    s = m.group(0).strip()
    if 10 < len(s) < 350:
        핵심포인트_list.append(('★', s))
# "쌤이 만든 목차" 컨텍스트
for m in re.finditer(r'쌤이?\s*만든\s*목차[^\n]{0,200}', note_raw):
    핵심포인트_list.append(('쌤목차', m.group(0).strip()[:300]))
# 통암기 컨텍스트
for m in re.finditer(r'.{0,80}(?:통암기|이대로\s*외우|반드시\s*외우)[^\n]{0,150}', note_raw):
    s = m.group(0).strip()
    if 10 < len(s) < 350:
        핵심포인트_list.append(('통암기', s))
# "암기 :" 컨텍스트
for m in re.finditer(r'.{0,50}암기\s*:\s*[^\n]{5,150}', note_raw):
    s = m.group(0).strip()
    if 10 < len(s) < 350:
        핵심포인트_list.append(('암기', s))

print(f'  필기노트 핵심포인트: {len(핵심포인트_list)}개')

핵심_path = OUT / '_필기노트_핵심포인트.md'
핵심_content = ['# ⭐ 필기노트 핵심 포인트 (자동 추출)\n',
                '> 필기노트의 ★ 표시, "쌤이 만든 목차", "통암기" 등 강사 강조 부분 모음.\n',
                f'> 총 {len(핵심포인트_list)}개\n']
# 카테고리별
by_cat = defaultdict(list)
for cat, text in 핵심포인트_list:
    by_cat[cat].append(text)
for cat, items in by_cat.items():
    핵심_content.append(f'\n## {cat} ({len(items)}개)\n')
    for it in items[:50]:
        핵심_content.append(f'- {it}')
핵심_path.write_text('\n'.join(핵심_content), encoding='utf-8')
print(f'  OK  _필기노트_핵심포인트.md  {핵심_path.stat().st_size/1024:.0f}KB')

# ============== Step 5: 21논점별 출제빈도 통계 ==============
print('\n=== Step 5: 21논점 출제 빈도 ===')

logum_counts = Counter()
for rn, logums in GICHUL_LOGUM.items():
    for l in logums:
        logum_counts[l] += 1

빈도_path = OUT / '_논점별_출제빈도.md'
빈도_content = ['# 📊 21논점별 출제 빈도\n', '> 기출 36회 기준 각 논점이 출제된 회차 수\n']
빈도_content.append('\n| 별점 | 논점 | 이름 | 출제 회차 | 단원 |')
빈도_content.append('|---|---|---|---|---|')

# 출제 빈도순 정렬
sorted_logums = sorted(logum_counts.items(), key=lambda x: -x[1])
for l, count in sorted_logums:
    name = next(n for num,n,_ in LOGUMS if num == l)
    ch = next(c for num,n,c in LOGUMS if num == l)
    if count >= 5:
        stars = '★★★'
    elif count >= 3:
        stars = '★★'
    else:
        stars = '★'
    rounds_for_logum = [rn for rn, ls in GICHUL_LOGUM.items() if l in ls]
    빈도_content.append(f'| {stars} | [{l}] | {name} | {count}회 ({rounds_for_logum}) | {ch} |')

# 한 번도 출제 안 된 논점
covered = set(logum_counts.keys())
all_logums = set(l for l,_,_ in LOGUMS)
uncovered = all_logums - covered
if uncovered:
    빈도_content.append('\n## ⚠️ 한 번도 출제 안 된 논점 (저빈도)\n')
    for l in sorted(uncovered):
        name = next(n for num,n,_ in LOGUMS if num == l)
        빈도_content.append(f'- [{l}] {name}')

빈도_path.write_text('\n'.join(빈도_content), encoding='utf-8')
print(f'  OK  _논점별_출제빈도.md  {빈도_path.stat().st_size/1024:.0f}KB')

# ============== Step 6: 부가 파일 ==============
print('\n=== Step 6: 부가 파일 ===')

# 법령 모음
법령_set = set()
법령_patterns = [
    r'감정평가\s*및.{0,15}법률.{0,5}\s*제?\s*\d+조',
    r'감정평가에 관한 규칙 제\s*\d+조',
    r'감칙\s*제?\s*\d+조',
    r'부동산\s*가격공시.{0,15}\s*제?\s*\d+조',
    r'토지보상법\s*제?\s*\d+조',
    r'감정평가\s*실무기준\s*\d+\.\d+\.\d+',
]
for p in ['_extract/raw_기본서.md', '_extract/raw_필기노트.md', '_extract/raw_핵심요약서.md', '_extract/raw_기출예해집.md']:
    full = BASE / p
    if not full.exists(): continue
    text = full.read_text(encoding='utf-8')
    for pat in 법령_patterns:
        for m in re.finditer(pat, text):
            법령_set.add(m.group(0).strip())
법령_path = OUT / '_법령모음.md'
법령_content = ['# ⚖️ 법령 모음 (자동 추출)\n', f'> 총 {len(법령_set)}개\n```']
for l in sorted(법령_set):
    법령_content.append(l)
법령_content.append('```')
법령_path.write_text('\n'.join(법령_content), encoding='utf-8')
print(f'  OK  _법령모음.md ({len(법령_set)}개)')

# 암기카드 시드
카드_set = set()
정의_patterns = [
    r'["“][가-힣\s·()A-Z]{2,30}["”]?\s*(?:이란|란)\s*[^\n。]{20,250}\s*(?:을\s*말한다|를\s*말한다|이다|라\s*한다)',
    r'\d+\s*[가-힣]{2,30}\s*[\n]?[가-힣][^\n]{30,200}을\s*말한다',
    r'[가-힣A-Z\(\)]{2,30}(?:이란|란)\s+[가-힣][^\n。]{20,200}(?:을\s*말한다|를\s*말한다)',
]
for p in ['_extract/raw_기본서.md', '_extract/raw_필기노트.md', '_extract/raw_핵심요약서.md']:
    full = BASE / p
    if not full.exists(): continue
    text = full.read_text(encoding='utf-8')
    for pat in 정의_patterns:
        for m in re.finditer(pat, text):
            d = m.group(0).strip()
            if 30 < len(d) < 350:
                카드_set.add(d)
카드_path = OUT / '_암기카드_시드.md'
카드_content = ['# 🗂️ 암기카드 시드\n', f'> 총 {len(카드_set)}개\n']
for i, c in enumerate(sorted(카드_set), 1):
    카드_content.append(f'### Card {i}\n{c}\n')
카드_path.write_text('\n'.join(카드_content), encoding='utf-8')
print(f'  OK  _암기카드_시드.md ({len(카드_set)}개)')

# 출제 빈도 통계 (단원별)
통계_path = OUT / '_출제빈도_통계_단원별.md'
통계_content = ['# 📊 단원별 출제 빈도\n', '| 단원 | 이름 | 논점 | 기출 | GS | 합계 |']
통계_content.append('|---|---|---|---|---|---|')
for ch_no in sorted(CHAPTERS.keys()):
    ps = problems_by_ch[ch_no]
    g = sum(1 for p in ps if '기출' in p['title'])
    s = sum(1 for p in ps if 'GS' in p['title'])
    name = CHAPTERS[ch_no]['name'].replace('_',' ')
    nl = len(CHAPTERS[ch_no]['logum'])
    통계_content.append(f'| {ch_no:02d} | {name} | {nl} | {g} | {s} | {g+s} |')
통계_path.write_text('\n'.join(통계_content), encoding='utf-8')
print(f'  OK  _출제빈도_통계_단원별.md')

# 시험 직전 압축본
print('  🏃 시험 직전 압축본...')
압축본_path = OUT / '🏃_시험직전_압축.md'
압축본_content = ['# 🏃 시험 직전 압축본 (감정평가이론)\n', '> 시험 1~3일 전 1개 파일로 전 과목 복습.\n\n---\n']
압축본_content.append('## 📊 21논점별 출제 빈도\n')
압축본_content.append(빈도_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## 📐 답안 양식 모음\n')
압축본_content.append(양식_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## ⭐ 필기노트 핵심포인트\n')
압축본_content.append(핵심_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## ⚖️ 법령 모음\n')
압축본_content.append(법령_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## 📝 필기노트 전체\n')
note_raw_path = BASE / '_extract/raw_필기노트.md'
if note_raw_path.exists():
    압축본_content.append(note_raw_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## 📖 핵심요약서 전체\n')
hyak_raw_path = BASE / '_extract/raw_핵심요약서.md'
if hyak_raw_path.exists():
    압축본_content.append(hyak_raw_path.read_text(encoding='utf-8'))
압축본_path.write_text('\n'.join(압축본_content), encoding='utf-8')
print(f'  OK  🏃_시험직전_압축.md')

# 참조 파일 복사
print('  📑 참조 파일 복사...')
ref_files = [
    ('_extract/raw_기출예해집.md', '참조_기출예해집.md'),
    ('_extract/raw_핵심요약서.md', '참조_핵심요약서_전체.md'),
    ('_extract/raw_필기노트.md', '참조_필기노트_전체.md'),
    ('_extract/raw_기본서.md', '참조_기본서_전체.md'),
    ('_extract/raw_실전모의2000.md', '참조_실전모의2000.md'),
    ('_extract/raw_GS1기.md', '참조_GS1기_전체.md'),
    ('_extract/raw_GS3기.md', '참조_GS3기_전체.md'),
    ('_extract/raw_변형모의1.md', '참조_변형모의1.md'),
    ('_extract/raw_변형모의2.md', '참조_변형모의2.md'),
]
for src, dst in ref_files:
    src_path = BASE / src
    if src_path.exists():
        shutil.copy(src_path, OUT / dst)

print('\n=== 완료 ===')
print(f'위치: {OUT}')
