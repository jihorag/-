#!/usr/bin/env python3
"""
감정평가실무 단권화 빌드 스크립트
- 책들을 PART별로 쪼개서 단원_NN_이론.md 생성
- 워크북/기출/GS를 단원별로 묶어 단원_NN_문제.md 생성
- _최종산출물/ 폴더에 결과물 배치
"""
import pypdf, re, os
from pathlib import Path

BASE = Path('/Users/hanjiho/Documents/Claude KAPA CHATING/2차 - 감정평가실무_학습자료')
OUT = BASE / '_최종산출물'
OUT.mkdir(exist_ok=True)

# ================== 설정 ==================
# 각 책의 PART 시작 페이지 (PDF 페이지 기준, 1-based)
BOOKS = {
    '핵심요약서': {
        'file': '감정평가실무 핵심요약서 [업데이트일_26.04.02].pdf',
        'parts': {
            # PART 번호: (시작p, 끝p)
            1: (17, 20),
            2: (21, 52),
            3: (53, 90),
            4: (91, 126),
            5: (127, 136),
            6: (137, 164),
            7: (165, 226),
            8: (227, 266),
            9: (267, 299),
        }
    },
    '기본서_상권': {
        'file': '감정평가실무 기본서 상권 (일반평가편) [업데이트일_26.05.13].pdf',
        'parts': {
            1: (13, 64),
            2: (65, 148),
            3: (149, 222),
            4: (223, 288),
            5: (289, 312),
            6: (313, 359),
        }
    },
    '기본서_하권': {
        'file': '감정평가실무 기본서 하권 (공적평가편) [업데이트일_26.04.30].pdf',
        'parts': {
            7: (11, 122),
            8: (123, 188),
            9: (189, 282),
            10: (283, 288),
        }
    },
    '워크북': {
        'file': '감정평가실무 워크북 [제1판] [업데이트일_26.05.14].pdf',
        'parts': {
            1: (11, 22),
            2: (23, 62),
            3: (63, 126),
            4: (127, 162),
            5: (163, 172),
            6: (173, 216),
            7: (217, 274),
            8: (275, 302),
            9: (303, 381),
        }
    },
}

# 단원 설계: 8개 단원으로 PART 그룹화
# 키워드는 단원 식별에 강력한 신호만 (일반 단어 X)
CHAPTERS = [
    {'no': 1, 'name': '감정평가실무_기초',           'parts': [1],     'topics': ['감정평가 기초', 'TVM', '금융계수', '면적', '도로'],
     'keywords': ['금융계수','내가계수','현가계수','감채기금','저당상수','화폐의 시간가치','복리연금','상환비율','잔금비율']},
    {'no': 2, 'name': '토지의_감정평가',             'parts': [2],     'topics': ['공시지가법', '거래사례비교법', '원가법', '수익환원법'],
     'keywords': ['공시지가기준법','비교표준지','적용공시지가의 선택','거래사례비교법','사정보정','원가법','재조달원가','조성원가법','수익환원법','직접환원법','DCF법','부동산잔여법','환원율','할인율','시장추출법','요소구성법','투자결합법','부채감당법','엘우드법','자본회수율','시점수정치']},
    {'no': 3, 'name': '건물·복합·임대료',            'parts': [3],     'topics': ['건물 평가', '복합부동산', '구분건물', '임대료', '회귀분석'],
     'keywords': ['건물 평가','부대설비','감가수정','내용연수','분해법','일체비준','일체수익','구분건물','집합건물','층별효용','임대사례비교법','적산법','수익분석법','계속임료','노선가식','회귀분석','총수익승수','대쌍비교법']},
    {'no': 4, 'name': '유형별_평가',                 'parts': [4],     'topics': ['토지/건물 유형별', '기계기구', '광업권', '어업권', '오염'],
     'keywords': ['광천지','골프장용지','공공용지','사도','맹지','택지후보지','지상권','구분지상권','지상정착물','제시외 건물','공유지분 토지','녹색건축물','공사중단','기계기구','공장재단','광산','광업권','어장','어업권','선박의 평가','의제부동산','오염부동산','일조권 침해','토양오염','가치하락분']},
    {'no': 5, 'name': '비가치추계·기업가치·무형자산', 'parts': [5,6],   'topics': ['투자분석', '최유효이용', '기업가치', '주식', '영업권', '권리금'],
     'keywords': ['NPV','IRR','순현재가치','내부수익률','매후환대차','레버리지효과','최유효이용 분석','최유효이용분석','투자의사결정','상장주식','비상장주식','채권의 평가','기업가치 평가','기업가치평가','FCFF','WACC','영업권 평가','영업권의 평가','지식재산권','권리금','무형자산']},
    {'no': 6, 'name': '토지의_보상평가',             'parts': [7],     'topics': ['손실보상', '토지보상', '공법상 제한', '특수토지', '잔여지', '환매'],
     'keywords': ['토지보상법','손실보상','사업인정','사업인정고시일','적용공시지가','공익사업','잔여지','환매','환매토지','미지급용지','무허가건축물','불법형질변경','도시계획시설','개발제한구역','GB 안','GB지정','송전선로','지하사용료','입체이용저해율','개간비','구분지상권의 보상','사도부지']},
    {'no': 7, 'name': '건축물·영업·기타_보상',       'parts': [8],     'topics': ['건축물 보상', '영업손실', '농업손실', '권리 보상', '이주정착금'],
     'keywords': ['건축물의 보상','잔여건축물','주거용 건축물','공작물의 평가','수목','과수','묘목','입목','농작물','분묘','영업폐지','영업휴업','휴업보상','일시영업','농업손실','축산업','잠업','휴직보상','실직보상','이주정착금','주거이전비','이사비','동산이전비','이농비','어업권 보상','광업권 보상']},
    {'no': 8, 'name': '목적별평가·표준지·정비',      'parts': [9,10],  'topics': ['담보', '경매', '국공유', '소송', '표준지공시지가', '정비사업', '재무보고'],
     'keywords': ['담보평가','경매평가','소송평가','국공유','국·공유','국유재산','공유재산','매각평가','종전자산','비례율','정비기반시설','현금청산','표준지공시지가','표준지 공시지가','표준지의 조사','정비사업','도시정비','재개발','재건축','환지','도시개발법','공동주택 분양','택지비','재무보고','입주권']},
]

# 회차/주차 정보
GS_STRUCTURE = {
    'GS0기_문답': {
        'file': '25년대비 실무0기GS 문제 및 예시답안 모음 [총20회분] [업데이트일_26.05.10].pdf',
        'comment': '1주차~5주차×4번 = 20회분 + 답안',
    },
    'GS0기_분석노트': {
        'file': '25년대비 실무0기GS 문제분석노트 [총20회분] [업데이트일_26.05.13].pdf',
        'comment': '문제분석 — 출제포인트 및 풀이전략',
    },
    'GS1기': {
        'file': '25년대비 실무1기GS 문제 및 예시답안 모음 [총20회분] [업데이트일_26.02.13].pdf',
        'comment': '10주차×2회차 = 20회분 + 답안',
    },
    'GS2기': {
        'file': '25년대비 실무2기GS 문제 및 예시답안 모음 [총10회분] [업데이트일_26.01.18].pdf',
        'parts': {1:1, 2:21, 3:40, 4:60, 5:79, 6:101, 7:121, 8:139, 9:157, 10:175, 'END': 341},
        'comment': '10주차',
    },
    'GS3기': {
        'file': '25년대비 실무3기GS 문제 및 예시답안 모음 [총10회분] [업데이트일_26.01.13].pdf',
        'parts': {1:1, 2:18, 3:36, 4:57, 5:74, 6:89, 7:104, 8:126, 9:145, 10:168, 'END': 304},
        'comment': '10주차',
    },
}

# ================== 헬퍼 함수 ==================
def extract_pages(pdf_path, start, end):
    """PDF의 start~end (1-based, inclusive) 페이지 텍스트를 추출"""
    r = pypdf.PdfReader(str(pdf_path))
    parts = []
    for i in range(start-1, min(end, len(r.pages))):
        text = r.pages[i].extract_text() or ''
        parts.append(f'\n\n<!-- p.{i+1} -->\n\n{text}')
    return ''.join(parts)

def classify_text(text, chapters):
    """텍스트에서 각 단원의 키워드 점수를 계산, 최고 점수 단원 반환.
    단원 01(기초)은 자동분류 대상 아님 (워크북 PART 01만 들어감)."""
    scores = {}
    for ch in chapters:
        if ch['no'] == 1:
            continue  # 단원 01은 자동분류 제외
        s = 0
        for kw in ch['keywords']:
            s += text.count(kw)
        scores[ch['no']] = s
    if not any(scores.values()):
        return None
    # 최다득점 단원 반환
    return max(scores, key=scores.get)

# ================== 1단계: 단원_NN_이론.md 생성 ==================
print('\n=== 1단계: 이론 파일 생성 ===')
for ch in CHAPTERS:
    out_path = OUT / f'단원_{ch["no"]:02d}_{ch["name"]}.md'
    parts_list = ch['parts']
    content = [
        f'# 단원 {ch["no"]:02d} — {ch["name"].replace("_"," ")}',
        f'\n> 책 PART: {parts_list}',
        f'> 다루는 주제: {", ".join(ch["topics"])}',
        f'> 키워드: {", ".join(ch["keywords"])}\n',
        '---\n',
    ]
    total_len = 0
    for book_name, book in BOOKS.items():
        # 이론 파일에는 워크북 제외
        if book_name == '워크북':
            continue
        for pn in parts_list:
            if pn in book['parts']:
                start, end = book['parts'][pn]
                pdf_path = BASE / book['file']
                if not pdf_path.exists():
                    print(f'  WARN: 파일 없음 {pdf_path}')
                    continue
                text = extract_pages(pdf_path, start, end)
                content.append(f'\n## 📖 {book_name} — PART {pn:02d} (p.{start}~{end})\n')
                content.append(text)
                content.append('\n')
                total_len += len(text)
    out_path.write_text(''.join(content), encoding='utf-8')
    size_kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {size_kb:.0f}KB')

# ================== 2단계: 기출/GS 회차별 분할 ==================
print('\n=== 2단계: 기출/GS 회차 분할 및 분류 ===')

# 기출문제지 회차 경계 (이전 분석에서 얻은 데이터)
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

gichul_pdf = BASE / '감정평가실무_기출문제지 [1-36회] [업데이트일_26.03.09].pdf'
problems = {ch['no']: [] for ch in CHAPTERS}

# 각 기출 회차 분류
for rn, (s, e) in GICHUL_ROUNDS.items():
    text = extract_pages(gichul_pdf, s, e)
    ch_no = classify_text(text, CHAPTERS)
    if ch_no:
        problems[ch_no].append((f'기출 제{rn}회', text))
    else:
        # 키워드 매칭 안 되면 단원 2 (3방식) 기본값
        problems[2].append((f'기출 제{rn}회', text))

# GS2기 회차 분류
gs2_pdf = BASE / GS_STRUCTURE['GS2기']['file']
gs2_parts = GS_STRUCTURE['GS2기']['parts']
for wk in range(1, 11):
    start = gs2_parts[wk]
    end = gs2_parts.get(wk+1, gs2_parts['END']) - 1 if wk < 10 else gs2_parts['END']
    text = extract_pages(gs2_pdf, start, end)
    ch_no = classify_text(text, CHAPTERS)
    if ch_no:
        problems[ch_no].append((f'GS2기 {wk}주차', text))

# GS3기 회차 분류
gs3_pdf = BASE / GS_STRUCTURE['GS3기']['file']
gs3_parts = GS_STRUCTURE['GS3기']['parts']
for wk in range(1, 11):
    start = gs3_parts[wk]
    end = gs3_parts.get(wk+1, gs3_parts['END']) - 1 if wk < 10 else gs3_parts['END']
    text = extract_pages(gs3_pdf, start, end)
    ch_no = classify_text(text, CHAPTERS)
    if ch_no:
        problems[ch_no].append((f'GS3기 {wk}주차', text))

# 분류 결과 출력
for ch in CHAPTERS:
    cnt = len(problems[ch['no']])
    titles = [t for t,_ in problems[ch['no']]]
    print(f'  단원 {ch["no"]:02d} ({ch["name"]}): {cnt}개 - {titles[:3]}{"..." if len(titles)>3 else ""}')

# ================== 3단계: 단원_NN_문제.md 생성 ==================
print('\n=== 3단계: 문제 파일 생성 ===')
workbook_pdf = BASE / BOOKS['워크북']['file']
workbook_parts = BOOKS['워크북']['parts']

for ch in CHAPTERS:
    out_path = OUT / f'문제_{ch["no"]:02d}_{ch["name"]}.md'
    content = [
        f'# 문제 단원 {ch["no"]:02d} — {ch["name"].replace("_"," ")}',
        f'\n> 다루는 주제: {", ".join(ch["topics"])}\n',
        '---\n',
    ]
    # 워크북 (해당 PART)
    for pn in ch['parts']:
        if pn in workbook_parts:
            start, end = workbook_parts[pn]
            text = extract_pages(workbook_pdf, start, end)
            content.append(f'\n## ✏️ 워크북 PART {pn:02d} (p.{start}~{end})\n')
            content.append(text)
            content.append('\n')
    # 기출/GS
    for title, text in problems[ch['no']]:
        content.append(f'\n## 🎯 {title}\n')
        content.append(text)
        content.append('\n')
    out_path.write_text(''.join(content), encoding='utf-8')
    size_kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {size_kb:.0f}KB')

# ================== 4단계: 참조 파일 복사 ==================
print('\n=== 4단계: 참조 파일 복사 ===')
import shutil
ref_files = [
    ('_extract/raw_기출답안.md', '참조_기출답안_11-36회.md'),
    ('_extract/raw_GS0기_문답.md', '참조_GS0기_문답.md'),
    ('_extract/raw_GS0기_분석노트.md', '참조_GS0기_분석노트.md'),
    ('_extract/raw_GS1기.md', '참조_GS1기.md'),
    ('_extract/raw_핵심요약서.md', '참조_핵심요약서_전체.md'),
]
for src, dst in ref_files:
    src_path = BASE / src
    dst_path = OUT / dst
    if src_path.exists():
        shutil.copy(src_path, dst_path)
        print(f'  OK  {dst}  {dst_path.stat().st_size/1024:.0f}KB')

print('\n=== 완료 ===')
print(f'산출물 위치: {OUT}')
