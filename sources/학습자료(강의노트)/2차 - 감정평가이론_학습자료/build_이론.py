#!/usr/bin/env python3
"""감정평가이론 단권화 빌드
- 21개 논점을 10단원으로 그룹화
- 단원별 이론 (기본서+필기노트+핵심요약서) + 문제 (기출+GS+모의) 파일 생성
"""
import pypdf, re, os, json, shutil
from pathlib import Path
from collections import defaultdict, Counter

BASE = Path(__file__).parent
OUT = BASE / '_최종산출물_이론'
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

# ============== 기본서 논점 시작 페이지 (자동 검출됨) ==============
BASIC_LOGUM_START = {
    '01': 17, '02': 34, '03': 74, '04': 122, '05': 162, '06': 198, '07': 226,
    '08': 250, '09': 274, '10': 286, '11': 320, '12': 344, '13': 380, '14': 434,
    '15': 452, '16': 476, '17': 498, '18': 566, '19': 580, '20': 592, '21': 604,
}
BASIC_END = 634

# ============== 필기노트 PART 시작 페이지 (첫 페이지 TOC 기준) ==============
NOTE_PART_START = {
    1: 2, 2: 36, 3: 38, 4: 72, 5: 91, 8: 129, 9: 144, 10: 151,
    11: 162, 12: 179, 13: 192, 16: 241, 17: 247, 18: 252, 19: 253, 20: 258,
}
NOTE_END = 303

# 필기노트 PART → 단원 매핑
NOTE_PART_TO_CH = {
    1: 1,    # 감정평가 기초
    2: 2,    # 부동산 기초
    3: 2,    # 부동산 가격론
    4: 3,    # 가격제원칙
    5: 3,    # 부동산시장론
    8: 4,    # 3방식 총론·절차·보고서
    9: 4,    # 비교방식
    10: 5,   # 원가방식
    11: 6,   # 수익방식
    12: 7,   # 기타방식
    13: 7,   # 임대 및 임대차평가
    16: 9,   # 부동산금융론
    17: 9,   # 부동산개발론 및 입지론
    18: 10,  # 마케팅·관리·중개·권리분석
    19: 10,  # 부동산 문제 및 정책론
    20: 10,  # 기타 주요논점
}

# ============== 책 파일 ==============
BOOKS = {
    '기본서':    '감정평가이론_기본서 [업데이트일_250830].pdf',
    '필기노트':  '감정평가이론_필기노트 [업데이트일_230430].pdf',
    '핵심요약서': '감정평가이론_핵심요약서 [업데이트일_250624].pdf',
}

# ============== 문제 PDF ==============
GICHUL_PDF = '감정평가이론_기출문제지 [1-36회] [업데이트일_250728].pdf'
GICHUL_DAPAN_PDF = '감정평가이론 기출예해집(25.10.29).pdf'
GS1_PDF = '스터디파이터_1기_이론_문제 및 예시답안 모음 [총10회분].pdf'
GS3_PDF = '25년대비 이론3기GS 문제 및 예시답안 모음 [총10회분] [업데이트일_25.07.11].pdf'
MOCK1_PDF = '변형 모의고사1 문제지 모음(해설지는 없음).pdf'
MOCK2_PDF = '변형모의고사2 문제지와 답안 모음.pdf'
MOCK2000_PDF = '감정평가이론_실전모의고사 2000점 [업데이트일_210923].pdf'

# ============== 기출 36회 수동 매핑 (Claude 직접 분석) ==============
GICHUL_MANUAL = {
    1:  2,    # 부동산 특성·시장·필요성·기능
    2:  2,    # 지대론·rent론·가격형성원리
    3:  6,    # 수익환원법 (자본환원이론)
    4:  4,    # 3방식·시산가액 조정·금융계수
    5:  2,    # Marshall 가치이론·3방식·약술
    6:  2,    # 가격발생원인·정상가격·적정가격
    7:  7,    # 임료·원가법
    8:  3,    # 가격발생요인·시장동향·가격원칙·TOPEKA
    9:  6,    # 자본환원·저당지분환원법·감가수정
    10: 9,    # 부동산증권화·시장이자율·시장분석
    11: 1,    # 컨설팅·등가교환·지역분석·약술
    12: 9,    # REITs·대체원칙·사정보정·약술
    13: 6,    # 수익방식·환원이율·DCF·재매도가격
    14: 3,    # 시장분석·시장성·생산성·부채금융
    15: 4,    # 3방식 시산가격·구체화·분류
    16: 1,    # 직업윤리·토양오염·표준지 그밖의요인
    17: 2,    # 종별·유형·시장가치/투자가치/계속기업/담보가치
    18: 7,    # 통계평가·지역분석·표준지공시지가/표준주택
    19: 4,    # 일괄평가·부동산가격지수
    20: 8,    # 지상권 토지·공동주택분양가상한제·일단지평가
    21: 8,    # 가격형성요인·비상장주식 평가
    22: 6,    # 송전선로 보상·수익형 부동산 평가
    23: 6,    # 시장가치·수익성 부동산·실물옵션
    24: 3,    # 최유효이용·시장분석·지역분석
    25: 8,    # 리모델링·토양오염·구분점포
    26: 8,    # 토지+건물 평가·전세·저당
    27: 8,    # 기업가치(계속기업)·재무보고
    28: 3,    # 최유효이용 분석
    29: 2,    # 가치발생요인·3면성·3방식
    30: 4,    # 택지조성·후분양·시장가치
    31: 1,    # 감정평가 개념·기준가치·복수감정·보상답변
    32: 3,    # 공간시장·자산시장·절차·윤리
    33: 8,    # 지식재산권·자본환원율
    34: 6,    # 수익환원법 직접환원/DCF·택지비
    35: 5,    # 원가법
    36: 4,    # 토지·담보·건축허가 (종합)
}

# ============== GS1기·GS3기 10회차 수동 매핑 ==============
GS_MANUAL = {
    'GS1기 1회차':  1,   # 부동산 특성·가격특징·기능·직업윤리
    'GS1기 2회차':  1,   # 조건부평가·3방식
    'GS1기 3회차':  2,   # 시장가치·투자가치·계속기업·담보가치
    'GS1기 4회차':  2,   # 시장가치 (가치이론)
    'GS1기 5회차':  2,   # 가치발생요인·3면성·3방식·지역분석
    'GS1기 6회차':  3,   # 최유효이용
    'GS1기 7회차':  3,   # 최유효이용 분석
    'GS1기 8회차':  3,   # 공간시장·자산시장·지역분석
    'GS1기 9회차':  3,   # 시장분석
    'GS1기 10회차': 8,   # 재무보고·기준가치·DCF
    'GS3기 1회차':  6,   # 정적/동적 DCF법
    'GS3기 2회차':  8,   # 영업권평가
    'GS3기 3회차':  8,   # 구분점포 (집합건물)
    'GS3기 4회차':  8,   # 폐기물·토양오염 (가치하락분)
    'GS3기 5회차':  9,   # 실물옵션 (NPV 한계)
    'GS3기 6회차':  9,   # 부동산PF·선분양·후분양
    'GS3기 7회차': 10,   # 용적률 이양제·임료
    'GS3기 8회차':  8,   # 상가권리금·대지권 미등기
    'GS3기 9회차':  8,   # 일단지평가·국공유재산
    'GS3기 10회차':10,   # 재개발 종전자산
}

# ============== 단원별 키워드 (자동 분류용) ==============
CHAPTER_KEYWORDS = {
    1: ['감정평가의 기초','감정평가 절차','기본적 사항','자료 수집','감정평가의 분류','일괄평가','구분평가','감정평가 기능','직업윤리'],
    2: ['부동산 가치','가치이론','가치형성요인','지역요인','개별요인','인근지역','동일수급권','가치발생요인','복잡성','지역분석','개별분석'],
    3: ['가격제원칙','최유효이용','최유효이용의 원칙','부동산시장','경기변동','시장분석','흡수율','경제기반','시장성분석','대체의 원칙','수요공급'],
    4: ['감정평가3방식','3방식 개관','거래사례비교법','사정보정','시점수정','시산가액 조정','시산가액의 조정','비준가액'],
    5: ['원가법','재조달원가','감가수정','내용연수','분해법','정액법','정률법','상환기금법'],
    6: ['수익환원법','직접환원법','DCF법','순수익','환원율','할인율','자본회수','저당지분환원','부동산잔여법'],
    7: ['임대사례비교법','임료','적산법','수익분석법','계속임료','노선가식','회귀분석','조소득승수법','승수법'],
    8: ['기업가치','상장주식','비상장주식','채권','영업권','지식재산권','권리금','무형자산','물건별 평가','특수부동산'],
    9: ['부동산투자','투자분석','레버리지','NPV','IRR','순현재가치','내부수익률','부동산금융','실물옵션','REITs','부동산금융론'],
    10: ['부동산정책론','정책','조세','부동산세','공시지가제도','친환경건축물','건부증감가','상가권리금','국공유지','그 밖의 요인'],
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

def classify_text(text):
    scores = {}
    for ch_no, kws in CHAPTER_KEYWORDS.items():
        scores[ch_no] = sum(text.count(k) for k in kws)
    if not any(scores.values()):
        return None
    return max(scores, key=scores.get)

# ============== Step 1: 단원별 이론 파일 생성 ==============
print('=== Step 1: 단원별 이론 파일 생성 ===')

# 기본서 단원별 페이지 범위 = 단원에 속한 논점들의 page range 통합
def basic_ranges_for_ch(ch_no):
    """단원에 속한 논점들의 기본서 페이지 범위"""
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

# 필기노트 단원별 페이지 범위
def note_ranges_for_ch(ch_no):
    """단원에 속한 필기노트 PART들의 페이지 범위"""
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

    # 논점 인덱스
    content.append('## 📑 이 단원의 논점 인덱스\n')
    for l in ch_info['logum']:
        name = next(n for num,n,_ in LOGUMS if num == l)
        content.append(f'- **[{l}]** {name}')
    content.append('')

    # 본문 목차
    content.append('## 🗺️ 본문 목차\n')
    content.append('- [📖 핵심요약서 (L1 - 압축, 의의정리 발췌)](#핵심요약서)')
    content.append('- [📝 필기노트 (L2 - 키워드·답안 양식)](#필기노트)')
    content.append('- [📚 기본서 (L3 - 본격 서술)](#기본서)\n')
    content.append('---\n')

    # 핵심요약서 (L1) - 전체 통째 포함 (181p로 작음)
    # 더 정밀한 분할은 추후 - 단원 1에만 전체, 나머지엔 인용 안내
    content.append('## <a name="핵심요약서"></a>📖 핵심요약서 — 의의정리 / 핵심정리 (L1)\n')
    content.append('> 핵심요약서는 의의정리 + 핵심정리 합본 181p로 작아 자동 분할 어려움.\n')
    content.append('> 이 단원에 해당하는 부분만 `참조_핵심요약서_전체.md`에서 찾아 학습.\n')
    content.append('> 또는 단원에 속한 논점의 의의(핵심요약서 PART 01)와 핵심(PART 02) 부분 참조.\n')

    # 필기노트 (L2)
    content.append('\n## <a name="필기노트"></a>📝 필기노트 (L2 - 답안 양식·키워드)\n')
    content.append('> 답안 작성 양식, 목차, 핵심 키워드 위주. 시험 직전 복습용.\n')
    note_rng = note_ranges_for_ch(ch_no)
    if note_rng:
        for p, s, e in note_rng:
            content.append(f'\n### 필기노트 PART {p:02d} (p.{s}~{e})\n')
            content.append(extract_pages(note_pdf, s, e))
    else:
        content.append('\n> (이 단원에 매핑된 필기노트 PART가 명시되어 있지 않음. 핵심요약서·기본서로 학습.)\n')

    # 기본서 (L3)
    content.append('\n## <a name="기본서"></a>📚 기본서 (L3 - 본격 서술)\n')
    content.append('> 논점별 본격 서술. 답안 작성 시 깊이있게 가져갈 내용.\n')
    for l, s, e in basic_ranges_for_ch(ch_no):
        name = next(n for num,n,_ in LOGUMS if num == l)
        content.append(f'\n### 기본서 — 논점 {l}: {name} (p.{s}~{e})\n')
        content.append(extract_pages(basic_pdf, s, e))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 2: 문제 분류 ==============
print('\n=== Step 2: 문제 회차별 분류 ===')

# 기출 1-36회 — 이론 기출문제지는 60p로 짧음. 회차별 페이지 추정
# 평균 60/36 = 1.67p/회. 정확히 추정 어려우니 회차 패턴 검색.
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
    # 끝 페이지
    sorted_r = sorted(rounds.keys())
    boundaries = {}
    for i, rn in enumerate(sorted_r):
        s = rounds[rn]
        e = rounds[sorted_r[i+1]] - 1 if i+1 < len(sorted_r) else len(r.pages)
        boundaries[rn] = (s, e)
    return boundaries

GICHUL_ROUNDS = detect_gichul_rounds()
print(f'  기출 회차 감지: {len(GICHUL_ROUNDS)}개')

# 기출 분류 (자동)
problems_by_ch = defaultdict(list)
gichul_pdf_full = BASE / GICHUL_PDF
gichul_dapan_full = BASE / GICHUL_DAPAN_PDF

for rn, (s, e) in GICHUL_ROUNDS.items():
    text = extract_pages(gichul_pdf_full, s, e)
    # 수동 매핑 우선
    ch = GICHUL_MANUAL.get(rn) or classify_text(text) or 4
    problems_by_ch[ch].append({
        'title': f'기출 제{rn}회',
        'text': text,
        'source': '기출문제지'
    })

# GS 분석 - GS1/GS3 회차 페이지 자동 검출
def detect_gs_rounds(pdf_path, label):
    r = pypdf.PdfReader(str(pdf_path))
    rounds = {}
    # "N회차" 또는 "N주차"
    for i in range(len(r.pages)):
        text = r.pages[i].extract_text() or ''
        m = re.search(r'(\d+)\s*(?:회차|주차)', text)
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

GS1_ROUNDS = detect_gs_rounds(BASE / GS1_PDF, 'GS1')
GS3_ROUNDS = detect_gs_rounds(BASE / GS3_PDF, 'GS3')
print(f'  GS1기 회차 감지: {len(GS1_ROUNDS)}개')
print(f'  GS3기 회차 감지: {len(GS3_ROUNDS)}개')

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

# 모의고사 - 종합 문제집이므로 별도 참조파일로만 (단원에 무겁게 들어가지 않음)
# 변형모의1·2·실전모의2000은 '참조_*.md'로 따로 둠 (별도 처리)

for ch_no in sorted(CHAPTERS.keys()):
    titles = [p['title'] for p in problems_by_ch[ch_no]]
    print(f'  단원 {ch_no}: {len(titles)}개 - {titles[:3]}{"..." if len(titles)>3 else ""}')

# ============== Step 3: 문제 파일 생성 ==============
print('\n=== Step 3: 문제 파일 생성 ===')
for ch_no in sorted(CHAPTERS.keys()):
    ch_info = CHAPTERS[ch_no]
    out_path = OUT / f'문제_{ch_no:02d}_{ch_info["name"]}.md'
    content = [f'# 문제 단원 {ch_no:02d} — {ch_info["name"].replace("_"," ")}\n']
    items = problems_by_ch[ch_no]
    if not items:
        content.append('> 이 단원에 자동 매핑된 문제가 없음. 기본서·필기노트로 학습 후 다른 단원의 문제로 보충.\n')
    for p in items:
        content.append(f'\n## {p["title"]} (출처: {p["source"]})\n')
        content.append(p['text'])
        content.append('\n')
    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 4: 부가 파일 ==============
print('\n=== Step 4: 부가 파일 ===')

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
raw_paths = ['_extract/raw_기본서.md', '_extract/raw_필기노트.md', '_extract/raw_핵심요약서.md', '_extract/raw_기출예해집.md']
for p in raw_paths:
    full = BASE / p
    if not full.exists(): continue
    text = full.read_text(encoding='utf-8')
    for pat in 법령_patterns:
        for m in re.finditer(pat, text):
            법령_set.add(m.group(0).strip())
법령_path = OUT / '_법령모음.md'
법령_content = ['# ⚖️ 법령 모음 (감정평가이론 - 자동 추출)\n', f'> 총 {len(법령_set)}개\n```']
for l in sorted(법령_set):
    법령_content.append(l)
법령_content.append('```')
법령_path.write_text('\n'.join(법령_content), encoding='utf-8')
print(f'  ⚖️  _법령모음.md  {법령_path.stat().st_size/1024:.0f}KB ({len(법령_set)}개)')

# 암기카드 시드
카드_set = set()
정의_pattern = r'["“][가-힣\s·()A-Z]{2,30}["”]?\s*(?:이란|란)\s*[^\n。]{20,250}\s*(?:을\s*말한다|를\s*말한다|이다|라\s*한다)'
대안_pattern = r'\d+\s*[가-힣]{2,30}\s*[\n]?[가-힣][^\n]{30,200}을\s*말한다'
for p in ['_extract/raw_기본서.md', '_extract/raw_필기노트.md', '_extract/raw_핵심요약서.md']:
    full = BASE / p
    if not full.exists(): continue
    text = full.read_text(encoding='utf-8')
    for pat in [정의_pattern, 대안_pattern]:
        for m in re.finditer(pat, text):
            d = m.group(0).strip()
            if 30 < len(d) < 350:
                카드_set.add(d)
카드_path = OUT / '_암기카드_시드.md'
카드_content = ['# 🗂️ 암기카드 시드 (이론 정의문 자동 추출)\n', f'> 총 {len(카드_set)}개\n']
for i, c in enumerate(sorted(카드_set), 1):
    카드_content.append(f'### Card {i}\n{c}\n')
카드_path.write_text('\n'.join(카드_content), encoding='utf-8')
print(f'  🗂️  _암기카드_시드.md  {카드_path.stat().st_size/1024:.0f}KB ({len(카드_set)}개)')

# 출제 빈도 통계
통계_path = OUT / '_출제빈도_통계.md'
통계_content = ['# 📊 출제 빈도 통계 (단원별)\n', '## 단원별 분포\n']
통계_content.append('| 단원 | 이름 | 논점 | 기출 | GS | 모의 | 합계 |')
통계_content.append('|---|---|---|---|---|---|---|')
for ch_no in sorted(CHAPTERS.keys()):
    ps = problems_by_ch[ch_no]
    g = sum(1 for p in ps if '기출' in p['title'])
    s = sum(1 for p in ps if 'GS' in p['title'])
    m = sum(1 for p in ps if '모의' in p['title'])
    name = CHAPTERS[ch_no]['name'].replace('_',' ')
    nl = len(CHAPTERS[ch_no]['logum'])
    통계_content.append(f'| {ch_no:02d} | {name} | {nl} | {g} | {s} | {m} | {g+s+m} |')

# 기출 회차별 매핑
통계_content.append('\n## 기출 회차별 매핑\n')
통계_content.append('| 회차 | 단원 | 단원명 |')
통계_content.append('|---|---|---|')
for rn in sorted(GICHUL_ROUNDS.keys()):
    for ch_no, items in problems_by_ch.items():
        for p in items:
            if p['title'] == f'기출 제{rn}회':
                통계_content.append(f'| 제{rn}회 | {ch_no:02d} | {CHAPTERS[ch_no]["name"]} |')
                break

통계_path.write_text('\n'.join(통계_content), encoding='utf-8')
print(f'  📊  _출제빈도_통계.md  {통계_path.stat().st_size/1024:.0f}KB')

# 시험 직전 압축본 = 필기노트 + 핵심요약서 + 법령 모음
print('  🏃 시험 직전 압축본...')
압축본_path = OUT / '🏃_시험직전_압축.md'
압축본_content = ['# 🏃 시험 직전 압축본 (감정평가이론)\n', '> 시험 1~3일 전 1개 파일로 전 과목 복습.\n\n---\n']
압축본_content.append('## ⚖️ 법령 모음\n')
압축본_content.append(법령_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## 📝 필기노트 전체\n')
note_raw = BASE / '_extract/raw_필기노트.md'
if note_raw.exists():
    압축본_content.append(note_raw.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## 📖 핵심요약서 전체\n')
hyak_raw = BASE / '_extract/raw_핵심요약서.md'
if hyak_raw.exists():
    압축본_content.append(hyak_raw.read_text(encoding='utf-8'))
압축본_path.write_text('\n'.join(압축본_content), encoding='utf-8')
print(f'  🏃  🏃_시험직전_압축.md  {압축본_path.stat().st_size/1024:.0f}KB')

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
