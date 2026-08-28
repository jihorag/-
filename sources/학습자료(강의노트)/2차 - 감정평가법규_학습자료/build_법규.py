#!/usr/bin/env python3
"""감정평가법규 단권화 빌드 (이론 v2 수준)
- 10단원 (행정법 6 + 개별법 4)
- 기출 36회 + GS 수동 매핑
- 부가파일: 조문/판례/출제빈도/답안골격
"""
import pypdf, re, os, json, shutil
from pathlib import Path
from collections import defaultdict, Counter

BASE = Path(__file__).parent
OUT = BASE / '_최종산출물_법규'
OUT.mkdir(exist_ok=True)

# ============== 10단원 ==============
CHAPTERS = {
    1:  {'name': '행정법_개관·일반원칙·행정법관계',     'area': '행정법'},
    2:  {'name': '행정입법·행정행위',                   'area': '행정법'},
    3:  {'name': '행정계획·인허가의제·공법상계약',     'area': '행정법'},
    4:  {'name': '행정절차·실효성확보수단',             'area': '행정법'},
    5:  {'name': '행정쟁송_(심판·취소소송·기타)',        'area': '행정법'},
    6:  {'name': '행정상_손해전보',                     'area': '행정법'},
    7:  {'name': '공용수용_(사업인정·재결·약식절차)',   'area': '개별법'},
    8:  {'name': '손실보상_(보상기준·환매·생활보상)',   'area': '개별법'},
    9:  {'name': '부동산_가격공시법',                   'area': '개별법'},
    10: {'name': '감정평가법·도정법',                   'area': '개별법'},
}

# ============== 기본서 행정법 v2 PART → 단원 매핑 ==============
# PART 01: 행정법 개관 (p.2~24) → 단원 1
# PART 02: 행정작용법 (p.25~108) → Ch1,2 단원 2, Ch3 단원 3
# PART 03: 행정절차와 실효성 확보수단 (p.109~158) → 단원 4
# PART 04: 행정쟁송 (p.159~230) → 단원 5
# PART 05: 행정상 손해전보 (p.231~247) → 단원 6
# 정밀 페이지는 본문 안 헤더에서 추정. 일단 PART 단위로 통합 후 본문 안에서 분할.

ADMIN_BOOK_PARTS = {  # 행정법 기본서 v2
    'file': '보상법규_기본서_행정법 [업데이트일_26.05.10].pdf',
    'parts': {
        # PART → (start, end)
        1: (2, 24),     # PART 01 행정법 개관
        2: (25, 86),    # PART 02 행정작용법 (Ch1,2)
        3: (87, 108),   # PART 02 Ch3 그 밖의 행위형식
        4: (109, 158),  # PART 03 행정절차·실효성
        5: (159, 230),  # PART 04 행정쟁송
        6: (231, 247),  # PART 05 행정상 손해전보
    }
}

# ============== 기본서 개별법 v2 PART → 단원 매핑 ==============
INDIV_BOOK_PARTS = {  # 개별법 기본서 v2
    'file': '보상법규_기본서_개별법 [업데이트일_26.05.26].pdf',
    'parts': {
        7: (2, 116),    # PART 01 공용수용 (Ch1~11)
        8: (117, 198),  # PART 02 손실보상
        9: (199, 228),  # PART 03 Ch1 부동산 가격공시법
        10: (229, 274), # PART 03 Ch2,3 감정평가법, 도정법
    }
}

# 핵심요약서 개별법 PART → 단원
HYAK_BOOK = {
    'file': '보상법규_핵심요약서_개별법 [업데이트일자_26.05.26].pdf',
    'parts': {
        7: (2, 78),     # PART 01 공용수용
        8: (79, 136),   # PART 02 손실보상
        9: (137, 150),  # PART 03 Ch1 가격공시법
        10: (151, 184), # PART 03 Ch2,3 감평법·도정법
    }
}

# ============== 기출 36회 1번 메인 단원 수동 매핑 ==============
GICHUL_MANUAL = {
    1:  7,   # 사업인정 및 권리구제
    2:  7,   # 피수용자 법적지위
    3:  7,   # 재결에 대한 불복
    4:  8,   # 보상기준과 정당보상
    5:  7,   # 토지수용의 효과
    6:  7,   # 사업인정실효 및 손실보상청구권
    7:  5,   # 무효인 재결과 취소할 수 있는 재결
    8:  8,   # 헌법 23조 3항 해석
    9:  8,   # 정당보상(대토보상)
    10: 7,   # 사업인정 적법여부 + 보상금증감청구소송
    11: 5,   # 원처분주의·재결주의·집행부정지
    12: 8,   # 토지보상법 70조 입법취지·손실보상액
    13: 2,   # 부관의 종류·독립 쟁송가능성
    14: 5,   # 인근토지 소유자의 원고적격
    15: 7,   # 사업인정의 절차상하자
    16: 5,   # 재결의 부작위시 행정쟁송수단
    17: 7,   # 사전결정·사업인정과 재결의 하자승계
    18: 8,   # 보상규정 결여시 23조 3항·대토보상
    19: 8,   # 환매권 소송수단
    20: 8,   # 이주대책 근거·이주정착금
    21: 2,   # 행정규칙 법적성질·잔여지수용청구·이의신청
    22: 5,   # 보상금증감청구소송·법규명령·구체적규범통제
    23: 8,   # 환매권 행사 권리구제·환매대금증액
    24: 1,   # 신뢰보호의 원칙·행정계획변경청구권
    25: 10,  # 조합설립인가 법적성질·원처분주의 (도정법)
    26: 2,   # 법령보충적 행정규칙·보상금증감청구소송
    27: 4,   # 거부처분 사전통지·이유제시·처분사유추가변경
    28: 7,   # 하자승계·수용권남용·계획재량
    29: 8,   # 주거이전비·간접손실보상
    30: 5,   # 대상적격·제소기간·이의신청·하자치유
    31: 8,   # 보상금증감청구소송·공법상 제한받는 토지·공물 수용
    32: 7,   # 재결신청청구권·재결전치주의·잔여지수용청구권
    33: 10,  # 이전고시와 협의소익·사실상 사도·주거이전비 (도정법)
    34: 7,   # 사업인정 법적성질·대상적격·보상금증감청구소송
    35: 8,   # 환매권 법적성질·절차·선결문제
    36: 7,   # 사업인정 전후 협의·요건·영업손실보상
}

# 기출 각 회차의 4문제 → 단원 다중 매핑 (출제빈도 통계용)
GICHUL_LOGUM = {
    1: [7,9,8,8], 2: [7,10,8,8], 3: [7,8,9], 4: [8,9,8],
    5: [7,9,8], 6: [7,9,9], 7: [5,9,8,8], 8: [1,9,7,7],
    9: [8,8,10,9], 10: [7,5,7,7], 11: [5,10,8,8],
    12: [8,8,7,10], 13: [2,8,9,8], 14: [5,8,8,10],
    15: [7,4,8,8], 16: [5,2,4,8], 17: [7,10,8,1],
    18: [8,10,8], 19: [8,9,7], 20: [8,2,4],
    21: [2,7,5,5], 22: [5,2,4,7], 23: [8,8,5,7], 24: [1,6,2,5],
    25: [10,5,6,7], 26: [2,8,8,5], 27: [4,5,5,2], 28: [7,2,7,8],
    29: [8,10,2,9], 30: [5,8,8,7], 31: [8,9,10,5],
    32: [7,5,5,10], 33: [10,2,4,10], 34: [7,5,5,1], 35: [8,9,5,10],
    36: [7,5,5,10],
}

# ============== GS 25년 1·2·3기 페이지 자동 검출용 ==============
GS_FILES = {
    '25년_GS1기': '25년대비 법규1기GS 문제 및 예시답안 모음 [총10회분].pdf',
    '25년_GS2기': '25년대비 법규2기GS 문제 및 예시답안 모음 [총20회분] [업데이트일_25.04.11].pdf',
    '25년_GS3기': '25년대비 법규3기GS 문제 및 예시답안 모음 [총10회분] [업데이트일_25.07.17].pdf',
}

# ============== 단원 키워드 (자동 분류용) ==============
CHAPTER_KEYWORDS = {
    1: ['행정법 개관','행정법의 개념','법치행정','신뢰보호의 원칙','평등의 원칙','부당결부','자기구속','법원 및 일반원칙','법원성','행정법 관계','공권'],
    2: ['행정입법','법규명령','행정규칙','법규성','행정행위','기속행위','재량행위','행정행위의 효력','구성요건적 효력','행정행위의 하자','부관','독립쟁송','독립취소'],
    3: ['행정계획','계획재량','단계적 행정결정','사전결정','인허가의제','공법상 계약','행정상 사실행위','행정지도'],
    4: ['행정절차','이유제시','사전통지','청문','처분사유추가변경','절차상 하자','대집행','행정강제','행정벌','과징금','이행강제금','행정조사'],
    5: ['행정심판','취소소송','대상적격','원고적격','협의의 소익','협의소익','집행정지','집행부정지','가구제','처분사유의 추가','기판력','무효등확인소송','부작위위법확인소송','당사자소송','원처분주의','재결주의','이의신청','제소기간'],
    6: ['국가배상','손해배상','공법상 결과제거','국가배상책임','이중배상금지','자동차손배법','영조물','직무관련성','직무행위'],
    7: ['공용수용','사업인정','협의취득','재결','약식절차','수용재결','이의재결','잔여지수용','확장수용','이전수용','대집행','토지수용위원회','보상협의회','환매','환매권'],
    8: ['손실보상','정당보상','공시지가기준 보상','개발이익배제','잔여지보상','잔여지가격감소','대토보상','채권보상','생활보상','이주대책','이주정착금','주거이전비','간접보상','간접손실보상','영업보상','농업손실보상','지장물 보상'],
    9: ['표준지공시지가','개별공시지가','토지가격비준표','부동산가격공시위원회','산정지가검증','주택가격공시','공동주택가격','중앙부동산가격공시위원회'],
    10: ['감정평가사','감정평가법인','감정평가법인등','자격등록','갱신등록','업무정지','징계위원회','감정평가 실무기준','한국감정평가협회','과징금','정비사업','조합설립인가','관리처분계획','분양신청','이전고시','매도청구','수용재결','도정법'],
}

# ============== 헬퍼 ==============
def extract_pages(pdf_path, start, end):
    if start > end: return ''
    try:
        r = pypdf.PdfReader(str(pdf_path))
    except Exception as e:
        return f'<!-- PDF 읽기 실패: {e} -->'
    parts = []
    for i in range(start-1, min(end, len(r.pages))):
        try:
            text = r.pages[i].extract_text() or ''
        except Exception:
            text = ''
        parts.append(f'\n<!--p.{i+1}-->\n{text}')
    return '\n'.join(parts)

def extract_specific_pages(pdf_path, pages):
    if not pages: return ''
    try:
        r = pypdf.PdfReader(str(pdf_path))
    except Exception as e:
        return f'<!-- PDF 읽기 실패 -->'
    parts = []
    for p in sorted(pages):
        if 1 <= p <= len(r.pages):
            try:
                text = r.pages[p-1].extract_text() or ''
            except Exception:
                text = ''
            parts.append(f'\n<!--p.{p}-->\n{text}')
    return '\n'.join(parts)

def classify_text(text):
    scores = {}
    for ch, kws in CHAPTER_KEYWORDS.items():
        scores[ch] = sum(text.count(k) for k in kws)
    if not any(scores.values()):
        return None
    return max(scores, key=scores.get)

# ============== Step 1: 기출예해집 페이지별 분류 (논점별 기출모음 활용) ==============
print('=== Step 1: 논점별_기출모음 페이지별 분류 ===')
yehae_pdf = BASE / '보상법규 논점별 기출모음 [업데이트일_26.05.19].pdf'
yehae_pages_by_ch = defaultdict(list)
r = pypdf.PdfReader(str(yehae_pdf))
for i in range(len(r.pages)):
    text = r.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        yehae_pages_by_ch[ch].append(i + 1)
for ch in sorted(CHAPTERS.keys()):
    print(f'  단원 {ch}: 논점별 기출 {len(yehae_pages_by_ch[ch])}p')

# 법전 페이지별 분류 (법전이 통째로 1.6MB이므로 단원별 분배)
print('\n=== Step 1-2: 법전 페이지별 분류 ===')
law_pdf = BASE / '스터디파이터 감정평가사 법전 [제2판] [업데이트일_26.04.16].pdf'
law_pages_by_ch = defaultdict(list)
r2 = pypdf.PdfReader(str(law_pdf))
for i in range(len(r2.pages)):
    text = r2.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        law_pages_by_ch[ch].append(i + 1)
for ch in sorted(CHAPTERS.keys()):
    print(f'  단원 {ch}: 법전 {len(law_pages_by_ch[ch])}p')

# ============== Step 2: 단원별 이론 파일 생성 ==============
print('\n=== Step 2: 단원별 이론 파일 생성 ===')

admin_pdf = BASE / ADMIN_BOOK_PARTS['file']
indiv_pdf = BASE / INDIV_BOOK_PARTS['file']
hyak_pdf = BASE / HYAK_BOOK['file']
조문특강_행정 = BASE / '스터디파이터_감정평가보상법규_행정법_조문특강.pdf'
조문특강_개별 = BASE / '스터디파이터_감정평가보상법규_개별법_조문특강.pdf'
판례특강_pdf = BASE / '판례특강 자료.pdf'

for ch_no in sorted(CHAPTERS.keys()):
    ch_info = CHAPTERS[ch_no]
    out_path = OUT / f'단원_{ch_no:02d}_{ch_info["name"]}.md'

    content = [f'# 단원 {ch_no:02d} — {ch_info["name"].replace("_"," ")}\n']
    content.append(f'> **영역**: {ch_info["area"]}\n')

    # 출제 빈도 (★★★/★★/★)
    출제수 = sum(1 for rounds in GICHUL_LOGUM.values() if ch_no in rounds)
    main_수 = sum(1 for v in GICHUL_MANUAL.values() if v == ch_no)
    if 출제수 >= 15:
        stars = '★★★'
    elif 출제수 >= 8:
        stars = '★★'
    else:
        stars = '★'
    content.append(f'> **출제 빈도**: {stars} (4문제 기준 {출제수}회 출제, 1번 메인 {main_수}회)\n')

    # 목차
    content.append('\n## 🗺️ 본문 목차\n')
    content.append('- [📖 핵심요약서 (개별법만)](#핵심요약서)' if ch_info['area'] == '개별법' else '')
    content.append('- [📚 기본서 본문](#기본서)')
    content.append('- [⚖️ 관련 조문 (법전 발췌)](#조문)')
    content.append('- [📕 논점별 기출모음 발췌](#기출논점)')
    content.append('\n---\n')

    # 핵심요약서 (개별법만)
    if ch_info['area'] == '개별법' and ch_no in HYAK_BOOK['parts']:
        s, e = HYAK_BOOK['parts'][ch_no]
        content.append(f'## <a name="핵심요약서"></a>📖 핵심요약서 — 개별법 PART (p.{s}~{e})\n')
        content.append(extract_pages(hyak_pdf, s, e))
        content.append('\n---\n')

    # 기본서 본문
    content.append('## <a name="기본서"></a>📚 기본서 본문\n')
    if ch_info['area'] == '행정법':
        if ch_no in ADMIN_BOOK_PARTS['parts']:
            s, e = ADMIN_BOOK_PARTS['parts'][ch_no]
            content.append(f'\n### 기본서 행정법 (p.{s}~{e})\n')
            content.append(extract_pages(admin_pdf, s, e))
    else:
        if ch_no in INDIV_BOOK_PARTS['parts']:
            s, e = INDIV_BOOK_PARTS['parts'][ch_no]
            content.append(f'\n### 기본서 개별법 (p.{s}~{e})\n')
            content.append(extract_pages(indiv_pdf, s, e))
    content.append('\n---\n')

    # 관련 조문 - 법전 페이지 매칭
    content.append('## <a name="조문"></a>⚖️ 관련 조문 (법전 페이지 매칭)\n')
    law_pages = law_pages_by_ch[ch_no][:30]  # 너무 많으면 30p로 제한
    if law_pages:
        content.append(f'> 법전(594p) 중 이 단원 키워드와 매칭된 페이지 {len(law_pages_by_ch[ch_no])}p 중 처음 30p 발췌\n')
        content.append(extract_specific_pages(law_pdf, law_pages))
    else:
        content.append('> 매칭 없음. 법전 전체는 `참조_법전.md` 참조.\n')
    content.append('\n---\n')

    # 논점별 기출모음 발췌
    content.append('## <a name="기출논점"></a>📕 논점별 기출모음 발췌\n')
    yh_pages = yehae_pages_by_ch[ch_no]
    if yh_pages:
        content.append(f'> 논점별 기출모음 50p 중 이 단원 매칭 {len(yh_pages)}p\n')
        content.append(extract_specific_pages(yehae_pdf, yh_pages))
    else:
        content.append('> 매칭 없음. 전체는 `참조_논점별_기출모음.md` 참조.\n')

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 3: 기출/GS 회차 분할 ==============
print('\n=== Step 3: 기출/GS 회차 분할 ===')

gichul_pdf = BASE / '보상법규_기출문제지[01-36회] [업데이트일_250809].pdf'

def detect_rounds(pdf_path, pattern_options):
    r = pypdf.PdfReader(str(pdf_path))
    rounds = {}
    for i in range(len(r.pages)):
        text = r.pages[i].extract_text() or ''
        head = text[:300]
        for pat in pattern_options:
            m = re.search(pat, head)
            if m:
                rn = int(m.group(1))
                if 1 <= rn <= 40 and rn not in rounds:
                    rounds[rn] = i + 1
                break
    sorted_r = sorted(rounds.keys())
    boundaries = {}
    for i, rn in enumerate(sorted_r):
        s = rounds[rn]
        e = rounds[sorted_r[i+1]] - 1 if i+1 < len(sorted_r) else len(r.pages)
        boundaries[rn] = (s, e)
    return boundaries

GICHUL_ROUNDS = detect_rounds(gichul_pdf, [r'제\s*(\d+)\s*회', r'(\d+)\s*회'])
print(f'  기출 회차 감지: {len(GICHUL_ROUNDS)}개')

# GS 페이지별 분류 (회차 검출이 어려우면 페이지별 분류)
def detect_gs_pages(pdf_path):
    """GS PDF를 페이지별로 단원 분류"""
    pages_by_ch = defaultdict(list)
    try:
        r = pypdf.PdfReader(str(pdf_path))
        for i in range(len(r.pages)):
            text = r.pages[i].extract_text() or ''
            ch = classify_text(text)
            if ch:
                pages_by_ch[ch].append(i + 1)
    except Exception:
        pass
    return pages_by_ch

gs1_pages = detect_gs_pages(BASE / GS_FILES['25년_GS1기'])
gs2_pages = detect_gs_pages(BASE / GS_FILES['25년_GS2기'])
gs3_pages = detect_gs_pages(BASE / GS_FILES['25년_GS3기'])
for ch in sorted(CHAPTERS.keys()):
    print(f'  단원 {ch}: GS1기 {len(gs1_pages[ch])}p / GS2기 {len(gs2_pages[ch])}p / GS3기 {len(gs3_pages[ch])}p')

# ============== Step 4: 문제 파일 생성 ==============
print('\n=== Step 4: 문제 파일 생성 ===')

problems_by_ch = defaultdict(list)
for rn, (s, e) in GICHUL_ROUNDS.items():
    text = extract_pages(gichul_pdf, s, e)
    ch = GICHUL_MANUAL.get(rn) or classify_text(text) or 7
    problems_by_ch[ch].append({
        'title': f'기출 제{rn}회',
        'text': text,
        'round': rn,
    })

for ch_no in sorted(CHAPTERS.keys()):
    ch_info = CHAPTERS[ch_no]
    out_path = OUT / f'문제_{ch_no:02d}_{ch_info["name"]}.md'
    content = [f'# 문제 단원 {ch_no:02d} — {ch_info["name"].replace("_"," ")}\n']

    # 기출
    gichul_items = problems_by_ch[ch_no]
    if gichul_items:
        content.append(f'\n## 🎯 기출 ({len(gichul_items)}개)\n')
        for p in gichul_items:
            content.append(f'\n### {p["title"]}\n')
            content.append(p['text'])
            content.append('\n')

    # GS - 페이지 발췌
    if gs1_pages[ch_no] or gs2_pages[ch_no] or gs3_pages[ch_no]:
        content.append('\n## 📝 GS 모의고사 — 페이지 발췌\n')
        if gs1_pages[ch_no]:
            content.append(f'\n### 25년 GS1기 ({len(gs1_pages[ch_no])}p 발췌)\n')
            content.append(extract_specific_pages(BASE / GS_FILES['25년_GS1기'], gs1_pages[ch_no][:20]))
        if gs2_pages[ch_no]:
            content.append(f'\n### 25년 GS2기 ({len(gs2_pages[ch_no])}p 발췌)\n')
            content.append(extract_specific_pages(BASE / GS_FILES['25년_GS2기'], gs2_pages[ch_no][:20]))
        if gs3_pages[ch_no]:
            content.append(f'\n### 25년 GS3기 ({len(gs3_pages[ch_no])}p 발췌)\n')
            content.append(extract_specific_pages(BASE / GS_FILES['25년_GS3기'], gs3_pages[ch_no][:20]))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 5: 부가 파일 ==============
print('\n=== Step 5: 부가 파일 ===')

# 출제 빈도 통계 (단원별 + 회차별)
logum_counts = Counter()
for rn, chs in GICHUL_LOGUM.items():
    for ch in chs:
        logum_counts[ch] += 1

빈도_path = OUT / '_단원별_출제빈도.md'
빈도_content = ['# 📊 단원별 출제 빈도 (기출 36회 기준)\n', '> 각 회차 4문제를 모두 분석. 단원별 출제 회수.\n']
빈도_content.append('\n| 별점 | 단원 | 이름 | 영역 | 출제 회수 | 1번 메인 |')
빈도_content.append('|---|---|---|---|---|---|')
sorted_chs = sorted(CHAPTERS.keys(), key=lambda c: -logum_counts.get(c, 0))
for ch in sorted_chs:
    count = logum_counts.get(ch, 0)
    main = sum(1 for v in GICHUL_MANUAL.values() if v == ch)
    if count >= 15:
        stars = '★★★'
    elif count >= 8:
        stars = '★★'
    else:
        stars = '★'
    name = CHAPTERS[ch]['name'].replace('_',' ')
    area = CHAPTERS[ch]['area']
    빈도_content.append(f'| {stars} | {ch:02d} | {name} | {area} | {count}회 | {main}회 |')

# 회차별 4문제 매핑
빈도_content.append('\n## 회차별 4문제 단원 매핑\n')
빈도_content.append('| 회차 | 1번 | 2번 | 3번 | 4번 | 메인 단원 |')
빈도_content.append('|---|---|---|---|---|---|')
for rn in sorted(GICHUL_LOGUM.keys()):
    chs = GICHUL_LOGUM[rn]
    main = GICHUL_MANUAL.get(rn, '?')
    cols = [str(c) for c in chs] + ['-'] * (4 - len(chs))
    빈도_content.append(f'| 제{rn}회 | {cols[0]} | {cols[1]} | {cols[2]} | {cols[3]} | **{main}** |')

빈도_path.write_text('\n'.join(빈도_content), encoding='utf-8')
print(f'  OK  _단원별_출제빈도.md  {빈도_path.stat().st_size/1024:.0f}KB')

# 조문특강 통합
조문_path = OUT / '_조문특강_통합.md'
조문_content = ['# ⚖️ 조문특강 통합 (행정법 + 개별법)\n\n']
조문_content.append('## 🏛️ 행정법 조문특강\n')
admin_raw = (BASE / '_extract/raw_조문특강_행정법.md')
if admin_raw.exists():
    조문_content.append(admin_raw.read_text(encoding='utf-8'))
조문_content.append('\n\n---\n## 📕 개별법 조문특강\n')
indiv_raw = (BASE / '_extract/raw_조문특강_개별법.md')
if indiv_raw.exists():
    조문_content.append(indiv_raw.read_text(encoding='utf-8'))
조문_path.write_text('\n'.join(조문_content), encoding='utf-8')
print(f'  OK  _조문특강_통합.md  {조문_path.stat().st_size/1024:.0f}KB')

# 판례특강
판례_path = OUT / '_판례특강.md'
shutil.copy(BASE / '_extract/raw_판례특강.md', 판례_path)
print(f'  OK  _판례특강.md  {판례_path.stat().st_size/1024:.0f}KB')

# 기출연도별 논점정리
논점정리_path = OUT / '_기출연도별_논점정리.md'
shutil.copy(BASE / '_extract/raw_기출연도별_논점정리.md', 논점정리_path)
print(f'  OK  _기출연도별_논점정리.md  {논점정리_path.stat().st_size/1024:.0f}KB')

# 시험 직전 압축본
print('  🏃 시험 직전 압축본...')
압축본_path = OUT / '🏃_시험직전_압축.md'
압축본_content = ['# 🏃 시험 직전 압축본 (감정평가법규)\n', '> 시험 1~3일 전 복습용.\n\n---\n']
압축본_content.append('## 📊 단원별 출제 빈도\n')
압축본_content.append(빈도_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## ⚖️ 조문특강 통합\n')
압축본_content.append(조문_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## ⚖️ 판례특강\n')
압축본_content.append(판례_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## 📖 핵심요약서 개별법 전체\n')
hyak_raw = (BASE / '_extract/raw_핵심요약서_개별법.md')
if hyak_raw.exists():
    압축본_content.append(hyak_raw.read_text(encoding='utf-8'))
압축본_path.write_text('\n'.join(압축본_content), encoding='utf-8')
print(f'  OK  🏃_시험직전_압축.md  {압축본_path.stat().st_size/1024:.0f}KB')

# 참조 파일 복사
print('  📑 참조 파일 복사...')
ref_files = [
    ('_extract/raw_기본서_행정법_v2.md', '참조_기본서_행정법.md'),
    ('_extract/raw_기본서_개별법_v2.md', '참조_기본서_개별법.md'),
    ('_extract/raw_핵심요약서_개별법.md', '참조_핵심요약서_개별법.md'),
    ('_extract/raw_법전.md', '참조_법전.md'),
    ('_extract/raw_논점별_기출모음.md', '참조_논점별_기출모음.md'),
    ('_extract/raw_25_GS1기.md', '참조_GS1기_전체.md'),
    ('_extract/raw_25_GS2기.md', '참조_GS2기_전체.md'),
    ('_extract/raw_25_GS3기.md', '참조_GS3기_전체.md'),
]
for src, dst in ref_files:
    src_path = BASE / src
    if src_path.exists():
        shutil.copy(src_path, OUT / dst)

print('\n=== 완료 ===')
print(f'위치: {OUT}')
