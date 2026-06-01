#!/usr/bin/env python3
"""감정평가실무 단권화 빌드 v3 (고도화)
- 11단원 분할 + 논점번호 + 출제포인트 + 통합형 + 답안매칭 + 부가파일들
"""
import pypdf, re, os, json, shutil
from pathlib import Path
from collections import defaultdict, Counter
import sys
sys.path.insert(0, str(Path(__file__).parent))
from 논점_데이터 import LOGUMS, CHAPTERS, CHAPTER_ORDER

BASE = Path(__file__).parent
OUT = BASE / '_최종산출물_v3'
OUT.mkdir(exist_ok=True)

# ============== 책 PART 경계 ==============
BOOKS = {
    '핵심요약서': {
        'file': '감정평가실무 핵심요약서 [업데이트일_26.04.02].pdf',
        'parts': {1: (17, 20), 2: (21, 52), 3: (53, 90), 4: (91, 126),
                  5: (127, 136), 6: (137, 164), 7: (165, 226), 8: (227, 266), 9: (267, 299)}
    },
    '기본서_상권': {
        'file': '감정평가실무 기본서 상권 (일반평가편) [업데이트일_26.05.13].pdf',
        'parts': {1: (13, 64), 2: (65, 148), 3: (149, 222), 4: (223, 288), 5: (289, 312), 6: (313, 359)}
    },
    '기본서_하권': {
        'file': '감정평가실무 기본서 하권 (공적평가편) [업데이트일_26.04.30].pdf',
        'parts': {7: (11, 122), 8: (123, 188), 9: (189, 282), 10: (283, 288)}
    },
    '워크북': {
        'file': '감정평가실무 워크북 [제1판] [업데이트일_26.05.14].pdf',
        'parts': {1: (11, 22), 2: (23, 62), 3: (63, 126), 4: (127, 162),
                  5: (163, 172), 6: (173, 216), 7: (217, 274), 8: (275, 302), 9: (303, 381)}
    },
}

# 핵심요약서·기본서_상권의 PART 02를 2a(공시지가·거래·원가)와 2b(수익환원)로 분할
# 핵심요약서: p.21~52 = PART 02
#   공시지가기준법 PART 02 Ch1 (절 1-5, p.5~)
#   수익환원법 PART 02 Ch4 (절 1-7, p.21~36)
# 추정: 핵심요약서 2a=p.21~36, 2b=p.37~52 (대략)
# 기본서 상권: p.65~148 = PART 02
#   2a 공시지가·거래·원가 = p.65~104, 2b 수익환원 = p.105~148 (추정)
# 본 추정값은 핵심요약서 TOC 페이지 수치 기반

SPLIT_PART2 = {
    '핵심요약서': {'2a': (21, 36), '2b': (37, 52)},  # 추정
    '기본서_상권': {'2a': (65, 104), '2b': (105, 148)},  # 추정 (수익환원 시작 = TOC p.105)
    '워크북': {'2a': (23, 34), '2b': (35, 62)},  # 추정 (수익환원 시작 = TOC p.35)
}

# PART 07(토지보상)을 6a(기본·원칙)와 6b(공법·특수)로 분할 추정
# 기본서 하권: p.11~122 = PART 07. 토지보상 절차/원칙은 앞쪽, 공법상제한·특수토지는 뒤쪽
# 핵심요약서: p.165~226. 손실보상·토지보상기준=165~180, 공법·특수=181~226 추정
SPLIT_PART7 = {
    '핵심요약서': {'6a': (165, 180), '6b': (181, 226)},
    '기본서_하권': {'6a': (11, 50), '6b': (51, 122)},
    '워크북': {'6a': (217, 230), '6b': (231, 274)},
}

# PART 09 + 10 (목적별 + 부록)을 8a(목적별)와 8b(표준지·정비·불의타)로 분할
# 핵심요약서: p.267~299 = PART 09 목적별 = 8a 전체
# 기본서 하권: p.189~282=PART 09(목적별)+p.283~288=PART 10(부록=표준지·정비)
# 8a = 핵심요약서 + 기본서 하권 PART 09 일부
# 8b = 기본서 하권 PART 10 + 정비사업 부분
SPLIT_PART9_10 = {
    '핵심요약서': {'8a': (267, 285), '8b': (286, 299)},  # 추정
    '기본서_하권': {'8a': (189, 230), '8b': (231, 288)},  # 정비사업+표준지=8b
    '워크북': {'8a': (303, 340), '8b': (341, 381)},
}

# 단원별 키워드 (개선판 - 11단원)
CHAPTER_KEYWORDS = {
    '1':  ['금융계수','내가계수','현가계수','감채기금','저당상수','화폐의 시간가치','복리연금','상환비율','잔금비율'],
    '2a': ['공시지가기준법','비교표준지','시점수정','거래사례비교법','사정보정','원가법','재조달원가','조성원가법','분해법','적산가액','비준가액','그 밖의 요인'],
    '2b': ['수익환원법','직접환원법','DCF법','부동산잔여법','환원율','할인율','시장추출법','요소구성법','투자결합법','부채감당법','엘우드법','자본회수율','순수익','복귀가액'],
    '3':  ['건물 평가','부대설비','감가수정','내용연수','분해법','일체비준','일체수익','구분건물','집합건물','층별효용','임대사례비교법','적산법','수익분석법','계속임료','노선가식','회귀분석','총수익승수','대쌍비교법','임대료'],
    '4':  ['광천지','골프장용지','공공용지','사도','맹지','택지후보지','지상권','구분지상권','지상정착물','제시외 건물','공유지분 토지','녹색건축물','공사중단','기계기구','공장재단','광산','광업권','어장','어업권','선박의 평가','의제부동산','오염부동산','일조권 침해','토양오염','가치하락분','개발부담금'],
    '5':  ['NPV','IRR','순현재가치','내부수익률','매후환대차','레버리지효과','최유효이용 분석','최유효이용분석','투자의사결정','상장주식','비상장주식','채권의 평가','기업가치 평가','기업가치평가','FCFF','WACC','영업권 평가','영업권의 평가','지식재산권','권리금','무형자산'],
    '6a': ['토지보상법','손실보상','사업인정','사업인정고시일','적용공시지가','공익사업','보상감정평가 기준','비교표준지의 선정','보상평가의 일반기준'],
    '6b': ['공법상 제한','용도지역','도시계획시설','개발제한구역','GB 안','GB지정','잔여지','환매','환매토지','미지급용지','무허가건축물','불법형질변경','송전선로','지하사용료','입체이용저해율','개간비','구분지상권의 보상','사도부지','특수토지'],
    '7':  ['건축물의 보상','잔여건축물','주거용 건축물','공작물의 평가','수목의 평가','과수','묘목','입목','농작물','분묘','영업폐지','영업휴업','휴업보상','일시영업','농업손실','축산업','잠업','휴직보상','실직보상','이주정착금','주거이전비','이사비','동산이전비','이농비','어업권 보상','광업권 보상'],
    '8a': ['담보평가','경매평가','소송평가','국공유','국·공유','국유재산','공유재산','매각평가','공동주택 분양가'],
    '8b': ['종전자산','비례율','정비기반시설','현금청산','표준지공시지가','표준지 공시지가','표준지의 조사','정비사업','도시정비','재개발','재건축','환지','도시개발법','택지비','재무보고','입주권','부가세 절세','Huff'],
}

# ============== 기출 회차 → 단원 수동 매핑 (Claude 직접 분석) ==============
# 각 회차 첫 페이지 문제 stem 직접 확인 후 매핑
GICHUL_MANUAL = {
    1:  '2a',  # [1회]  토지 3방식 종합 (원가/거래/수익/공시) → 토지 3방식 기초
    2:  '6a',  # [2회]  공익사업용지 보상평가 (토지+건물)
    3:  '6a',  # [3회]  택지개발예정지구 토지+지장물 보상
    4:  '3',   # [4회]  건물로 구성된 복합부동산 평가
    5:  '2a',  # [5회]  토지 평가 일반 (지목 대, 200㎡)
    6:  '8a',  # [6회]  아파트 분양가 결정용 택지평가
    7:  '8b',  # [7회]  공유수면 매립지 신규 표준지공시지가 결정
    8:  '6b',  # [8회]  도시계획도로 편입 토지+지장물 보상
    9:  '6a',  # [9회]  택지개발예정지구 토지+지장물 보상
    10: '5',   # [10회] 빌라트 건축 분양 vs 임대 투자우위 판단
    11: '7',   # [11회] 택지개발 토지+영농손실 보상
    12: '5',   # [12회] A빌딩 매입 후 5년 임대 매각 투자타당성
    13: '3',   # [13회] 복합부동산 평가 (비교표준지 선정)
    14: '5',   # [14회] 부동산 매입타당성 + 3방식 + 저당
    15: '3',   # [15회] 복합부동산 DCF 일괄평가
    16: '5',   # [16회] 매도 vs 개발 최유효이용
    17: '5',   # [17회] REIT 부동산 매입가격 + 배당수익률
    18: '2a',  # [18회] 표준지/거래사례/조성사례/임대사례로 토지가격
    19: '6a',  # [19회] 택지개발예정지구 이의재결 토지보상
    20: '8a',  # [20회] 공장 증설 임야 매입 + 담보대출 (개발단계별)
    21: '8a',  # [21회] 한강은행(담보)과 구청(보상) 동시 평가
    22: '3',   # [22회] 생명보험사 부동산 시산가치 조정
    23: '3',   # [23회] 계약임대료/시장임대료 기준 감정평가
    24: '4',   # [24회] 골프장 개발 토지임대료 (골프장용지)
    25: '2a',  # [25회] 표준지·매매사례·평가선례 활용
    26: '7',   # [26회] 보상 이의재결 + 농업손실보상
    27: '7',   # [27회] 영업휴업 보상 + 미지급용지/사실상 사도
    28: '6b',  # [28회] 지하공간 사용 입체이용저해율
    29: '5',   # [29회] 지식재산권/무형자산 (기술강도)
    30: '8a',  # [30회] Z마트 3점포 담보제공 평가
    31: '2a',  # [31회] 토지 개별요인 일반 평가
    32: '3',   # [32회] 단독주택·부속창고 건물 평가
    33: '8b',  # [33회] 표준지공시지가 (일반상업/3종일주)
    34: '6b',  # [34회] 잔여지(맹지) 수용재결평가
    35: '2a',  # [35회] 평가선례·거래사례 (일반거래)
    36: '5',   # [36회] 손익계산서 기업가치 평가 (FCFF)
}

# 기출 36회 페이지 경계
GICHUL_ROUNDS = {
    1: (2, 10), 2: (11, 23), 3: (24, 37), 4: (38, 45), 5: (46, 55),
    6: (56, 67), 7: (68, 89), 8: (90, 102), 9: (103, 117), 10: (118, 129),
    11: (130, 144), 12: (145, 159), 13: (160, 178), 14: (179, 192), 15: (193, 211),
    16: (212, 235), 17: (236, 253), 18: (254, 279), 19: (280, 301), 20: (302, 319),
    21: (320, 334), 22: (335, 354), 23: (355, 371), 24: (372, 390), 25: (391, 410),
    26: (411, 430), 27: (431, 450), 28: (451, 470), 29: (471, 490), 30: (491, 510),
    31: (511, 530), 32: (531, 550), 33: (551, 570), 34: (571, 588), 35: (589, 595),
    36: (596, 604),
}

# 기출답안 회차 페이지 (제11~36회, 평균 ~17p/회로 추정)
# 알려진 데이터: 제11회 p.1, 제12회 p.21, 제28회 p.321 → 회차당 평균 (321-21)/(28-12) = 18.75p
GICHUL_DAPAN_ROUNDS = {}
known = {11: 1, 12: 21, 28: 321}
# 11~12 사이 = 20p, 12~28 사이 = 300p/(28-12) = 18.75p, 28 이후 = (458-321)/(36-28) = 17.1p
for r in range(11, 37):
    if r in known:
        GICHUL_DAPAN_ROUNDS[r] = known[r]
    elif r < 12:
        pass
    elif r < 28:
        # 12 + (r-12)*18.75
        GICHUL_DAPAN_ROUNDS[r] = round(21 + (r-12) * 18.75)
    else:
        GICHUL_DAPAN_ROUNDS[r] = round(321 + (r-28) * 17.1)
# 끝 페이지 = 다음 회차 시작 - 1
GICHUL_DAPAN_END = {}
sorted_r = sorted(GICHUL_DAPAN_ROUNDS.keys())
for i, r in enumerate(sorted_r):
    if i+1 < len(sorted_r):
        GICHUL_DAPAN_END[r] = GICHUL_DAPAN_ROUNDS[sorted_r[i+1]] - 1
    else:
        GICHUL_DAPAN_END[r] = 458

# ============== GS 주차 → 단원 수동 매핑 (Claude 직접 분석) ==============
GS_MANUAL = {
    'GS2기 1주차':  '3',   # 개별/일괄 시산가액 조정 (복합부동산)
    'GS2기 2주차':  '5',   # 권리금 평가 (유형/무형)
    'GS2기 3주차':  '6a',  # 택지개발 이의재결
    'GS2기 4주차':  '4',   # 토양오염 부동산
    'GS2기 5주차':  '8a',  # 경매 + 보상 (구분건물)
    'GS2기 6주차':  '8b',  # 표준지공시지가 결정
    'GS2기 7주차':  '6a',  # LH 택지개발 보상
    'GS2기 8주차':  '5',   # 비상장 기업가치 FCFF
    'GS2기 9주차':  '8b',  # 표준지공시지가
    'GS2기 10주차': '7',   # 도로법 보상 (건축물+영업)
    'GS3기 1주차':  '5',   # 담보+투자의사결정 (요구수익률)
    'GS3기 2주차':  '5',   # NPV 최유효이용
    'GS3기 3주차':  '3',   # 사옥건물 매각목적 (복합)
    'GS3기 4주차':  '4',   # 골프장 평가
    'GS3기 5주차':  '8a',  # 담보+보상+표준지 (담보 핵심)
    'GS3기 6주차':  '3',   # 복합부동산 3방식
    'GS3기 7주차':  '8b',  # 용적률 결합건축 (불의타)
    'GS3기 8주차':  '4',   # 잡종지/임야 (유형별)
    'GS3기 9주차':  '6a',  # 택지개발 보상 (19회 reference)
    'GS3기 10주차': '3',   # 복합부동산 개별/일괄
}

# GS 주차 페이지 경계
GS_WEEKS = {
    'GS2기': {'file': '25년대비 실무2기GS 문제 및 예시답안 모음 [총10회분] [업데이트일_26.01.18].pdf',
              'weeks': [(1,1,20),(2,21,39),(3,40,59),(4,60,78),(5,79,100),
                        (6,101,120),(7,121,138),(8,139,156),(9,157,174),(10,175,341)]},
    'GS3기': {'file': '25년대비 실무3기GS 문제 및 예시답안 모음 [총10회분] [업데이트일_26.01.13].pdf',
              'weeks': [(1,1,17),(2,18,35),(3,36,56),(4,57,73),(5,74,88),
                        (6,89,103),(7,104,125),(8,126,144),(9,145,167),(10,168,304)]},
}

# ============== 헬퍼 함수 ==============
def extract_pages(pdf_path, start, end):
    """PDF의 start~end 페이지 텍스트 추출 (페이지 마커 포함)"""
    r = pypdf.PdfReader(str(pdf_path))
    parts = []
    for i in range(start-1, min(end, len(r.pages))):
        text = r.pages[i].extract_text() or ''
        parts.append(f'\n<!--p.{i+1}-->\n{text}')
    return '\n'.join(parts)

def get_book_range(book_name, ch_id):
    """단원 ID에 해당하는 책의 페이지 범위 가져오기 (분할 단원 처리)"""
    book = BOOKS[book_name]
    ch_info = CHAPTERS[ch_id]

    # 단원 2a/2b 분할
    if ch_id in ('2a', '2b') and book_name in SPLIT_PART2:
        return [SPLIT_PART2[book_name][ch_id]]
    # 단원 6a/6b 분할
    if ch_id in ('6a', '6b') and book_name in SPLIT_PART7:
        return [SPLIT_PART7[book_name][ch_id]]
    # 단원 8a/8b 분할
    if ch_id in ('8a', '8b') and book_name in SPLIT_PART9_10:
        return [SPLIT_PART9_10[book_name][ch_id]]

    # 일반 단원
    parts_list = ch_info['book_parts']
    ranges = []
    for pn in parts_list:
        if pn in book['parts']:
            ranges.append(book['parts'][pn])
    return ranges

def classify_text(text, chapters_kw=CHAPTER_KEYWORDS):
    """텍스트를 단원에 분류 (단원 1 제외)"""
    scores = {}
    for ch_id, kws in chapters_kw.items():
        if ch_id == '1':
            continue
        scores[ch_id] = sum(text.count(k) for k in kws)
    if not any(scores.values()):
        return None
    return max(scores, key=scores.get)

# ============== Step 1: 분석노트 단원별 텍스트 ==============
print('\n=== Step 1: GS0기 분석노트 단원별 분류 ===')
analysis_pdf = BASE / '25년대비 실무0기GS 문제분석노트 [총20회분] [업데이트일_26.05.13].pdf'
analysis_reader = pypdf.PdfReader(str(analysis_pdf))
analysis_by_ch = defaultdict(list)  # ch_id -> [(page, text)]
for i in range(len(analysis_reader.pages)):
    text = analysis_reader.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        analysis_by_ch[ch].append((i+1, text))
for ch_id in CHAPTER_ORDER:
    print(f'  단원 {ch_id}: 분석노트 {len(analysis_by_ch[ch_id])}p')

# ============== Step 2: 기출/GS 문제 단원별 분류 ==============
print('\n=== Step 2: 기출/GS 단원별 분류 ===')
gichul_pdf = BASE / '감정평가실무_기출문제지 [1-36회] [업데이트일_26.03.09].pdf'
problems_by_ch = defaultdict(list)  # ch_id -> [(title, text, dapan_range)]

for rn, (s, e) in GICHUL_ROUNDS.items():
    text = extract_pages(gichul_pdf, s, e)
    # 수동 매핑 우선 (Claude가 직접 분석한 단원)
    ch = GICHUL_MANUAL.get(rn) or classify_text(text) or '2a'
    dapan_range = None
    if rn in GICHUL_DAPAN_ROUNDS:
        dapan_range = (GICHUL_DAPAN_ROUNDS[rn], GICHUL_DAPAN_END[rn])
    problems_by_ch[ch].append({
        'title': f'기출 제{rn}회',
        'text': text,
        'dapan': dapan_range,
        'source': '기출문제지'
    })

# GS2기·GS3기 (수동 매핑 우선)
for gs_name, gs_data in GS_WEEKS.items():
    gs_pdf = BASE / gs_data['file']
    for wk, ws, we in gs_data['weeks']:
        text = extract_pages(gs_pdf, ws, we)
        title = f'{gs_name} {wk}주차'
        ch = GS_MANUAL.get(title) or classify_text(text)
        if ch:
            problems_by_ch[ch].append({
                'title': title,
                'text': text,
                'dapan': None,
                'source': gs_name
            })

for ch_id in CHAPTER_ORDER:
    titles = [p['title'] for p in problems_by_ch[ch_id]]
    print(f'  단원 {ch_id}: {len(titles)}개 - {titles[:3]}{"..." if len(titles)>3 else ""}')

# ============== Step 3: 단원별 이론 파일 생성 ==============
print('\n=== Step 3: 단원별 이론 파일 생성 ===')
gichul_dapan_pdf = BASE / '감정평가실무 기출문제 예시답안 [제11회-제36회] [업데이트일_26.05.13].pdf'

# 분석노트 페이지 → 본문 텍스트 캐시
def get_analysis_text(ch_id, max_chars=50000):
    """단원 분석노트 텍스트 (최대 max_chars)"""
    items = analysis_by_ch[ch_id]
    if not items:
        return ''
    parts = []
    total = 0
    for p, t in items:
        if total >= max_chars:
            break
        parts.append(f'\n<!-- 분석노트 p.{p} -->\n{t}')
        total += len(t)
    return '\n'.join(parts)

for ch_id in CHAPTER_ORDER:
    ch_info = CHAPTERS[ch_id]
    out_path = OUT / f'단원_{ch_id}_{ch_info["name"]}.md'

    # 이 단원에 속하는 논점
    ch_logums = [l for l in LOGUMS if l[3] == ch_id]

    content = []
    # 헤더
    content.append(f'# 단원 {ch_id} — {ch_info["name"].replace("_"," ")}\n')

    # 논점 인덱스
    content.append('## 📑 이 단원의 논점 인덱스\n')
    if ch_logums:
        for num, name, law, _ in ch_logums:
            law_str = f' (`{law}`)' if law else ''
            content.append(f'- **[{num}]** {name}{law_str}')
    else:
        content.append('- (이 단원은 도구·기초 정리만 — 논점 번호 없음)')
    content.append('')

    # TOC
    content.append('## 🗺️ 본문 목차\n')
    content.append('- [📌 출제포인트 분석 (GS0기 분석노트)](#출제포인트-분석)')
    content.append('- [📖 핵심요약서 (1차 학습용)](#핵심요약서)')
    content.append('- [📖 기본서 (2차 상세본)](#기본서)')
    content.append('- [📚 유도은 기본서 (참고)](#유도은)')
    content.append('')
    content.append('---\n')

    # 출제포인트 (분석노트 매핑)
    content.append('## <a name="출제포인트-분석"></a>📌 출제포인트 분석 (GS0기 분석노트)\n')
    if analysis_by_ch[ch_id]:
        content.append(f'> GS0기 분석노트에서 이 단원에 매핑된 페이지 ({len(analysis_by_ch[ch_id])}개)의 출제포인트 분석.\n')
        content.append('> 출제자의 의도·함정·fake 표시·우선순위가 노출된 자료라 시험 전략 수립의 핵심.\n')
        content.append(get_analysis_text(ch_id, 80000))
    else:
        content.append('> 이 단원에 매핑된 분석노트 페이지가 거의 없음. 다른 단원의 분석노트 참조 가능.\n')
    content.append('\n---\n')

    # 핵심요약서 (L1)
    content.append('## <a name="핵심요약서"></a>📖 핵심요약서 — 1차 학습용 (L1 - 압축)\n')
    content.append('> 📌 1차 학습 시 이 부분부터. 시험 직전 복습 시 이 부분만 봐도 됨.\n')
    ranges = get_book_range('핵심요약서', ch_id)
    for s, e in ranges:
        path = BASE / BOOKS['핵심요약서']['file']
        content.append(f'\n### 핵심요약서 p.{s}~{e}\n')
        content.append(extract_pages(path, s, e))
    content.append('\n---\n')

    # 기본서 (L2)
    content.append('## <a name="기본서"></a>📖 기본서 — 2차 상세본 (L2 - 표준)\n')
    content.append('> 📌 핵심요약서 다음 단계. 정의·조문 정확히 확인.\n')

    # 상권 또는 하권 중 매칭되는 것 선택
    for book_name in ['기본서_상권', '기본서_하권']:
        ranges = get_book_range(book_name, ch_id)
        if ranges:
            path = BASE / BOOKS[book_name]['file']
            for s, e in ranges:
                content.append(f'\n### {book_name.replace("_"," ")} p.{s}~{e}\n')
                content.append(extract_pages(path, s, e))
    content.append('\n---\n')

    # 유도은 (L3) - PART 매핑은 직접
    content.append('## <a name="유도은"></a>📚 유도은 기본서 — 심화 참고 (L3 - 심화)\n')
    content.append('> 📌 OCR 일부 깨짐 주의. 예시·사례·시각자료가 풍부.\n')

    # 단원별 유도은 PART 매핑
    yudoen_map = {
        '1':  ['유도은_PART01.md'],
        '2a': ['유도은_PART02.md'],
        '2b': ['유도은_PART02.md'],
        '3':  ['유도은_PART02.md'],
        '4':  ['유도은_PART03.md'],
        '5':  ['유도은_PART03.md'],
        '6a': ['유도은_PART04.md'],
        '6b': ['유도은_PART04.md'],
        '7':  ['유도은_PART04.md'],
        '8a': ['유도은_PART03.md', '유도은_PART04.md'],
        '8b': ['유도은_PART04.md'],
    }
    yudoen_files = yudoen_map.get(ch_id, [])
    content.append(f'\n📁 참고할 파일: {", ".join(yudoen_files) if yudoen_files else "없음"}')
    content.append('\n(원본 폴더의 해당 파일 참고. 전체를 단원에 포함하면 너무 커지므로 링크만.)\n')

    out_path.write_text('\n'.join(content), encoding='utf-8')
    size_kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {size_kb:.0f}KB')

# ============== Step 4: 단원별 문제+답안 파일 생성 ==============
print('\n=== Step 4: 단원별 문제+답안 파일 생성 ===')
workbook_pdf = BASE / BOOKS['워크북']['file']

for ch_id in CHAPTER_ORDER:
    ch_info = CHAPTERS[ch_id]
    out_path = OUT / f'문제_{ch_id}_{ch_info["name"]}.md'

    content = []
    content.append(f'# 문제 단원 {ch_id} — {ch_info["name"].replace("_"," ")}\n')

    # TOC
    content.append('## 🗺️ 목차\n')
    content.append('- [✏️ 워크북 (기초 문제)](#워크북)')
    if problems_by_ch[ch_id]:
        content.append('- [🎯 기출문제 + 답안](#기출)')
        content.append('- [📝 GS 모의고사](#gs)')
    content.append('\n---\n')

    # 워크북
    content.append('## <a name="워크북"></a>✏️ 워크북 (기초 문제)\n')
    ranges = get_book_range('워크북', ch_id)
    for s, e in ranges:
        text = extract_pages(workbook_pdf, s, e)
        content.append(f'\n### 워크북 p.{s}~{e}\n')
        content.append(text)
    content.append('\n---\n')

    # 기출 + 답안
    gichul_problems = [p for p in problems_by_ch[ch_id] if p['source'] == '기출문제지']
    if gichul_problems:
        content.append('## <a name="기출"></a>🎯 기출문제 + 답안\n')
        for p in gichul_problems:
            content.append(f'\n### {p["title"]}\n')
            content.append('\n#### 📝 문제\n')
            content.append(p['text'])
            if p['dapan']:
                ds, de = p['dapan']
                content.append(f'\n#### ✅ 답안 (기출답안집 p.{ds}~{de})\n')
                try:
                    dapan_text = extract_pages(gichul_dapan_pdf, ds, de)
                    content.append(dapan_text)
                except Exception as ex:
                    content.append(f'> 답안 추출 실패: {ex}')
            else:
                content.append(f'\n#### ✅ 답안\n> 11회 이전이라 답안집(11~36회)에 없음. 또는 매칭 불가.\n')
            content.append('\n')

    # GS
    gs_problems = [p for p in problems_by_ch[ch_id] if p['source'] != '기출문제지']
    if gs_problems:
        content.append('\n## <a name="gs"></a>📝 GS 모의고사 (참고)\n')
        for p in gs_problems:
            content.append(f'\n### {p["title"]} (출처: {p["source"]})\n')
            content.append(p['text'])
            content.append('\n')

    out_path.write_text('\n'.join(content), encoding='utf-8')
    size_kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {size_kb:.0f}KB')

print('\n=== Step 5: 부가 파일 ===')

# 공식 모음 - 모든 raw 파일에서 공식 패턴 추출
print('  📐 공식 모음...')
공식_path = OUT / '_공식모음.md'
공식_content = ['# 📐 공식 모음 (자동 추출)\n', '> 책 본문에서 자주 등장하는 공식·산식을 정규식으로 추출했습니다. 정확성은 학습 시 확인 필요.\n']

raw_book_files = ['_extract/raw_핵심요약서.md', '_extract/raw_기본서_상권.md', '_extract/raw_기본서_하권.md']
공식_patterns = [
    r'[가-힣\(\)\d ]{2,40}\s*=\s*[\d×x\(\)+\-÷\/\d\.,\s가-힣²³n]{5,80}',  # 한글 변수명 = 식
    r'\([1-9][\)\.]\s*[가-힣]{3,30}\)\s*[:=]\s*[^\n。]{5,80}',  # (1) 산정 = 식
]

found_set = set()
for raw_path in raw_book_files:
    full = BASE / raw_path
    if not full.exists():
        continue
    text = full.read_text(encoding='utf-8')
    for pat in 공식_patterns:
        for m in re.finditer(pat, text):
            formula = m.group(0).strip()
            if 10 < len(formula) < 100 and formula not in found_set:
                found_set.add(formula)
공식_content.append(f'> 총 {len(found_set)}개 공식 후보 추출')
공식_content.append('\n```')
for f in sorted(found_set):
    공식_content.append(f)
공식_content.append('```')
공식_path.write_text('\n'.join(공식_content), encoding='utf-8')
print(f'    OK  _공식모음.md  {공식_path.stat().st_size/1024:.0f}KB ({len(found_set)}개 후보)')

# 법령 모음
print('  ⚖️ 법령 모음...')
법령_path = OUT / '_법령모음.md'
법령_set = set()
법령_patterns = [
    r'감정평가에 관한 규칙 제\s*\d+조',
    r'감칙\s*제?\s*\d+조',
    r'토지보상법\s*제?\s*\d+조',
    r'토지보상법\s*시행규칙\s*제?\s*\d+조',
    r'토지보상법\s*시행령\s*제?\s*\d+조',
    r'국토계획법\s*제?\s*\d+조',
    r'부동산\s*가격공시.{0,15}\s*제?\s*\d+조',
    r'감정평가\s*및.{0,15}법률.{0,5}\s*제?\s*\d+조',
]
for raw_path in raw_book_files + ['_extract/raw_기출답안.md']:
    full = BASE / raw_path
    if not full.exists(): continue
    text = full.read_text(encoding='utf-8')
    for pat in 법령_patterns:
        for m in re.finditer(pat, text):
            법령_set.add(m.group(0).strip())

법령_content = ['# ⚖️ 법령 모음 (자동 추출)\n',
                '> 책·답안에서 자주 인용되는 조문 목록.\n']
법령_content.append(f'> 총 {len(법령_set)}개')
법령_content.append('\n```')
for l in sorted(법령_set):
    법령_content.append(l)
법령_content.append('```')
법령_path.write_text('\n'.join(법령_content), encoding='utf-8')
print(f'    OK  _법령모음.md  {법령_path.stat().st_size/1024:.0f}KB ({len(법령_set)}개)')

# 암기카드 시드 - "X"란 ~을 말한다 패턴
print('  🗂️ 암기카드 시드...')
카드_path = OUT / '_암기카드_시드.md'
카드_set = set()
정의_pattern = r'["“][가-힣\s·\(\)A-Z]{2,30}["”]?\s*(?:이란|란)\s*[^\n。]{20,200}\s*(?:을\s*말한다|를\s*말한다|이다|입니다|을\s*말한다\.)'
for raw_path in raw_book_files:
    full = BASE / raw_path
    if not full.exists(): continue
    text = full.read_text(encoding='utf-8')
    for m in re.finditer(정의_pattern, text):
        d = m.group(0).strip()
        if 30 < len(d) < 250:
            카드_set.add(d)

카드_content = ['# 🗂️ 암기카드 시드 (정의문 자동 추출)\n',
                '> 책에서 `"X"란 ~을 말한다` 패턴을 자동 추출. 학습 시 시각화·암기팁 추가하여 단권화 카드로 발전.\n']
카드_content.append(f'> 총 {len(카드_set)}개 정의문 추출')
카드_content.append('\n')
for i, c in enumerate(sorted(카드_set), 1):
    카드_content.append(f'### Card {i}\n{c}\n')
카드_path.write_text('\n'.join(카드_content), encoding='utf-8')
print(f'    OK  _암기카드_시드.md  {카드_path.stat().st_size/1024:.0f}KB ({len(카드_set)}개)')

# 출제 빈도 통계
print('  📊 출제 빈도 통계...')
통계_path = OUT / '_출제빈도_통계.md'
통계_content = ['# 📊 출제 빈도 통계 (단원별)\n', '## 단원별 문제 분포\n']
통계_content.append('| 단원 | 이름 | 논점 수 | 기출 회차 | GS 주차 | 합계 |')
통계_content.append('|---|---|---|---|---|---|')
for ch_id in CHAPTER_ORDER:
    ch_info = CHAPTERS[ch_id]
    n_logum = len([l for l in LOGUMS if l[3] == ch_id])
    ps = problems_by_ch[ch_id]
    n_gichul = sum(1 for p in ps if p['source'] == '기출문제지')
    n_gs = sum(1 for p in ps if p['source'] != '기출문제지')
    통계_content.append(f"| {ch_id} | {ch_info['name'].replace('_',' ')} | {n_logum} | {n_gichul} | {n_gs} | {n_gichul+n_gs} |")

# 기출 회차별 분류 표
통계_content.append('\n## 기출 회차별 매핑\n')
통계_content.append('| 회차 | 단원 | 단원명 |')
통계_content.append('|---|---|---|')
for rn in sorted(GICHUL_ROUNDS.keys()):
    for ch_id, items in problems_by_ch.items():
        for p in items:
            if p['title'] == f'기출 제{rn}회':
                통계_content.append(f'| 제{rn}회 | {ch_id} | {CHAPTERS[ch_id]["name"]} |')
                break

통계_path.write_text('\n'.join(통계_content), encoding='utf-8')
print(f'    OK  _출제빈도_통계.md  {통계_path.stat().st_size/1024:.0f}KB')

# 시험 직전 압축본 = 핵심요약서 전체 + 공식 + 법령
print('  🏃 시험 직전 압축본...')
압축본_path = OUT / '🏃_시험직전_압축.md'
압축본_content = ['# 🏃 시험 직전 압축본 (L1 통합)\n',
                  '> 모든 단원의 핵심요약서 + 공식 + 법령을 한 파일로 묶음. 시험 직전 1~3일 복습용.\n\n---\n']
압축본_content.append('## 📐 공식 모음\n')
압축본_content.append((공식_path).read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## ⚖️ 법령 모음\n')
압축본_content.append((법령_path).read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## 📖 핵심요약서 전체\n')
hyak_raw = BASE / '_extract/raw_핵심요약서.md'
if hyak_raw.exists():
    압축본_content.append(hyak_raw.read_text(encoding='utf-8'))
압축본_path.write_text('\n'.join(압축본_content), encoding='utf-8')
print(f'    OK  🏃_시험직전_압축.md  {압축본_path.stat().st_size/1024:.0f}KB')

# 참조 파일 복사
print('  📑 참조 파일 복사...')
ref_files = [
    ('_extract/raw_기출답안.md', '참조_기출답안_11-36회.md'),
    ('_extract/raw_GS0기_문답.md', '참조_GS0기_문답.md'),
    ('_extract/raw_GS0기_분석노트.md', '참조_GS0기_분석노트.md'),
    ('_extract/raw_GS1기.md', '참조_GS1기.md'),
    ('_extract/raw_핵심요약서.md', '참조_핵심요약서_전체.md'),
    ('유도은_PART01.md', '참조_유도은_PART01.md'),
    ('유도은_PART02.md', '참조_유도은_PART02.md'),
    ('유도은_PART03.md', '참조_유도은_PART03.md'),
    ('유도은_PART04.md', '참조_유도은_PART04.md'),
]
for src, dst in ref_files:
    src_path = BASE / src
    dst_path = OUT / dst
    if src_path.exists():
        shutil.copy(src_path, dst_path)

print('\n=== 완료 ===')
print(f'산출물 위치: {OUT}')
