#!/usr/bin/env python3
"""경제학 단권화 빌드 (1차 객관식)
- 마인드 17챕터 (미시 8 + 거시 9) 단원으로 사용
- 기본서·핵심요약서·워크북 + 마인드 통합
- 기출·연습문제·고난도100선 단원별 매핑
"""
import pypdf, re, os, json, shutil
from pathlib import Path
from collections import defaultdict, Counter

BASE = Path(__file__).parent
OUT = BASE / '_최종산출물_경제학'
OUT.mkdir(exist_ok=True)

# ============== 17 챕터 (마인드 + 기본서 매핑) ==============
# 마인드 챕터 → (이름, 영역, 기본서 장 범위, 핵심요약서 장 범위, 워크북 장 범위)
CHAPTERS = {
    'M01': {'name': '수학적_기초·경제학_기초',         'area': '미시', 'book_chapters': [1],     },
    'M02': {'name': '수요와_공급·탄력성·응용',         'area': '미시', 'book_chapters': [2,3,4]  },
    'M03': {'name': '소비자이론',                       'area': '미시', 'book_chapters': [5,6,7,8,9]},
    'M04': {'name': '생산자이론·비용이론',              'area': '미시', 'book_chapters': [10,11]  },
    'M05': {'name': '시장이론_(완전경쟁·독점·과점)',    'area': '미시', 'book_chapters': [12,13,14,15,16]},
    'M06': {'name': '생산요소시장·소득분배',            'area': '미시', 'book_chapters': [17,18]  },
    'M07': {'name': '일반균형·후생경제학',              'area': '미시', 'book_chapters': [19]     },
    'M08': {'name': '시장실패·외부성·공공재·정보경제',  'area': '미시', 'book_chapters': [20,21,22]},
    'G01': {'name': '거시경제학의_기초·국민소득결정',    'area': '거시', 'book_chapters': [1,2,3]   },
    'G02': {'name': '소비함수·투자함수',                'area': '거시', 'book_chapters': [4,5]    },
    'G03': {'name': '화폐금융론',                       'area': '거시', 'book_chapters': [6,7]    },
    'G04': {'name': '총수요·총공급이론',                'area': '거시', 'book_chapters': [8,9,10] },
    'G05': {'name': '실업·인플레이션',                  'area': '거시', 'book_chapters': [11,12]  },
    'G06': {'name': '학파별_비교',                      'area': '거시', 'book_chapters': [13]     },
    'G07': {'name': '경기변동·경제성장',                'area': '거시', 'book_chapters': [14,15]  },
    'G08': {'name': '국제무역이론',                     'area': '거시', 'book_chapters': [16]     },
    'G09': {'name': '국제금융이론',                     'area': '거시', 'book_chapters': [17,18]  },
}
CHAPTER_ORDER = ['M01','M02','M03','M04','M05','M06','M07','M08','G01','G02','G03','G04','G05','G06','G07','G08','G09']

# ============== 단원 키워드 (자동 분류용) ==============
CHAPTER_KEYWORDS = {
    'M01': ['미적분','한계분석','함수','경제학의 기초','경제수학','기회비용','생산가능곡선','PPC','합리적 의사결정'],
    'M02': ['수요함수','공급함수','시장균형','수요량','공급량','탄력성','가격탄력성','소득탄력성','교차탄력성','소비자잉여','생산자잉여','가격통제','최고가격제','최저가격제','조세의 전가','조세귀착'],
    'M03': ['한계효용','효용함수','무차별곡선','한계대체율','MRS','예산제약','소비자균형','대체효과','소득효과','기펜재','정상재','열등재','현시선호','약공리','강공리','기대효용','위험회피','피셔','2기간 모형'],
    'M04': ['생산함수','한계생산','평균생산','등량곡선','한계기술대체율','MRTS','비용함수','한계비용','평균비용','이윤극대화','콥-더글라스','생산자균형'],
    'M05': ['완전경쟁시장','독점시장','독점적경쟁','독점적 경쟁','과점시장','꾸르노','베르트랑','슈타켈베르크','담합','카르텔','게임이론','내쉬균형','우월전략','죄수의 딜레마','독점 가격차별','3급 가격차별'],
    'M06': ['생산요소시장','요소수요','요소공급','한계생산물가치','VMP','한계요소비용','소득분배','로렌츠곡선','지니계수','쿠즈네츠','임금','지대'],
    'M07': ['일반균형','후생경제학','파레토 효율','파레토효율','에지워스 박스','계약곡선','후생경제학의 기본정리','보상원리','애로의 불가능성','사회후생함수'],
    'M08': ['시장실패','외부성','외부불경제','피구세','코즈정리','공공재','무임승차','정보의 비대칭성','역선택','도덕적 해이','신호','선별'],
    'G01': ['거시경제학','GDP','GNI','GNP','국민소득','3면 등가','명목 GDP','실질 GDP','GDP 디플레이터','고전학파','케인즈','세이의 법칙','승수이론','한계소비성향','평균소비성향'],
    'G02': ['절대소득가설','상대소득가설','항상소득가설','생애주기가설','랜덤워크','케인즈 소비함수','프리드만','모딜리아니','홀의 가설','투자함수','현재가치법','내부수익률','신고전학파 투자','가속도이론','토빈의 q'],
    'G03': ['화폐공급','화폐수요','통화량','M1','M2','M3','지급준비율','신용창조','중앙은행','본원통화','통화승수','거래수요','예비적 수요','투기적 수요','유동성 함정','신화폐수량설','현금잔고수량설'],
    'G04': ['IS곡선','LM곡선','IS-LM','AD-AS','총수요','총공급','재정정책','금융정책','구축효과','전달경로','케인즈학파','통화론자','피셔 효과','피구 효과','피셔효과'],
    'G05': ['실업','자연실업률','마찰적 실업','구조적 실업','경기적 실업','오쿤의 법칙','인플레이션','디플레이션','수요견인','비용상승','필립스곡선','기대부가','적응적 기대','스태그플레이션','자연실업률 가설'],
    'G06': ['새고전학파','새케인즈학파','합리적 기대','루카스 비판','메뉴비용','효율임금','경직적 임금','경직적 가격','정책무력성 명제'],
    'G07': ['경기변동','경기순환','RBC','실물경기변동','경제성장','해로드','도마','솔로우 모형','균제상태','내생적 성장','수렴가설','자본축적','황금률'],
    'G08': ['국제무역','비교우위','절대우위','리카도 모형','헥셔-올린','관세','수입쿼터','보호무역','자유무역','무역승수','교역조건','무역수지'],
    'G09': ['환율','구매력평가설','이자율평가설','PPP','국제수지','경상수지','자본수지','J-curve','외환시장','마샬-러너','BP곡선','먼델-플레밍','고정환율','변동환율'],
}

# ============== 책 파일 ==============
BOOKS = {
    '기본서': '가장쉬운경제학 기본서 [업데이트일_26.03.09].pdf',
    '핵심요약서': '경제학 핵심요약서 [업데이트일_26.03.20].pdf',
    '워크북': '경제학_워크북 [업데이트일_190616].pdf',
}

# ============== 문제 PDF ==============
GICHUL_YEONDO = '감정평가사 경제학 연도별 기출문제집 [2018년-2025년] [업데이트일_26.04.02].pdf'
YEONSEUP_PDF = '가장쉬운경제학 연습문제 [업데이트일_26.04.30].pdf'
GONAN_문제 = '경제학 고난도 100선_문제 [업데이트일_26.01.25].pdf'
GONAN_답안 = '경제학 고난도 100선_답안 [업데이트일_26.03.09].pdf'
SEVEN_PDF = '2018년-2019년 국가직 7급, 지방직 7급, 서울시 7급 경제학 문제 및 해설.pdf'

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
    except Exception:
        return ''
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

# ============== Step 1: 기본서·핵심요약서·워크북의 각 장 시작 페이지 자동 검출 ==============
print('=== Step 1: 책별 장 시작 페이지 검출 ===')

def detect_book_chapters(pdf_path, area, max_ch):
    """기본서에서 미시/거시 각 장 시작 페이지 검출"""
    r = pypdf.PdfReader(str(pdf_path))
    result = {}
    seen_area = False
    body_started_p = 0
    for i in range(len(r.pages)):
        text = r.pages[i].extract_text() or ''
        # 미시/거시 영역 시작 확인
        if area == '미시' and not seen_area:
            if '미시경제학' in text[:300] and '제1편' in text[:300] and i > 5:
                seen_area = True
                body_started_p = i
        elif area == '거시' and not seen_area:
            if '거시경제학' in text[:300] and '제1편' in text[:300] and i > 10:
                seen_area = True
                body_started_p = i
        # 영역 진입 후 각 장 헤더 찾기
        if seen_area:
            # 다른 영역 진입 시 중단
            if area == '미시' and '거시경제학' in text[:300] and '제1편' in text[:300] and i > body_started_p + 20:
                break
            if area == '거시' and '미시경제학' in text[:300] and '제1편' in text[:300] and i > body_started_p + 20:
                break
            # 각 장 헤더: "제N장" 또는 "Chapter N"
            for ch in range(1, max_ch + 1):
                # 본문 시작 부분에 큰 글씨로 "제N장 ~"
                pat = rf'^\s*제\s*{ch}\s*장'
                if re.search(pat, text, re.MULTILINE):
                    if ch not in result:
                        result[ch] = i + 1
    return result

# 기본서: 미시 1~22, 거시 1~18
basic_pdf = BASE / BOOKS['기본서']
print('  기본서 미시 1~22장 검출...')
basic_micro = detect_book_chapters(basic_pdf, '미시', 22)
print('  기본서 거시 1~18장 검출...')
basic_macro = detect_book_chapters(basic_pdf, '거시', 18)
print(f'    미시 {len(basic_micro)}장: {sorted(basic_micro.items())}')
print(f'    거시 {len(basic_macro)}장: {sorted(basic_macro.items())}')

# 핵심요약서: 동일 구조
hyak_pdf = BASE / BOOKS['핵심요약서']
print('  핵심요약서 미시 1~22장 검출...')
hyak_micro = detect_book_chapters(hyak_pdf, '미시', 22)
print('  핵심요약서 거시 1~18장 검출...')
hyak_macro = detect_book_chapters(hyak_pdf, '거시', 18)
print(f'    미시 {len(hyak_micro)}장 / 거시 {len(hyak_macro)}장')

# 워크북: 동일 구조
work_pdf = BASE / BOOKS['워크북']
print('  워크북 미시 1~22장 검출...')
work_micro = detect_book_chapters(work_pdf, '미시', 22)
print('  워크북 거시 1~18장 검출...')
work_macro = detect_book_chapters(work_pdf, '거시', 18)
print(f'    미시 {len(work_micro)}장 / 거시 {len(work_macro)}장')

# 각 단원에 해당하는 책 페이지 범위 계산
def get_ranges(book_chapters_dict, ch_no_list, end_page):
    ranges = []
    for ch_no in ch_no_list:
        if ch_no in book_chapters_dict:
            s = book_chapters_dict[ch_no]
            # 끝 페이지: 다음 장 시작 - 1
            next_ch_starts = [book_chapters_dict[c] for c in book_chapters_dict if c > ch_no]
            e = min(next_ch_starts) - 1 if next_ch_starts else end_page
            ranges.append((ch_no, s, e))
    return ranges

# ============== Step 2: 마인드 MD에서 챕터 본문 추출 ==============
print('\n=== Step 2: 마인드 MD 챕터 본문 추출 ===')

mind_micro_path = BASE / '미시경제학_마인드.md'
mind_macro_path = BASE / '거시경제학_마인드.md'

def split_mind_by_chapter(md_path, n_chapters):
    """마인드 MD를 # Chapter NN. 헤더로 분할"""
    text = md_path.read_text(encoding='utf-8')
    chapters = {}
    pattern = re.compile(r'^# Chapter (\d+)\.', re.MULTILINE)
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        ch_no = int(m.group(1))
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        chapters[ch_no] = text[start:end]
    return chapters

mind_micro = split_mind_by_chapter(mind_micro_path, 8)
mind_macro = split_mind_by_chapter(mind_macro_path, 9)
print(f'  미시 마인드: {len(mind_micro)}챕터 ({list(mind_micro.keys())})')
print(f'  거시 마인드: {len(mind_macro)}챕터 ({list(mind_macro.keys())})')

# 마인드 챕터 → 단원 매핑
MIND_TO_CHAPTER = {
    'M01': 1, 'M02': 2, 'M03': 3, 'M04': 4, 'M05': 5, 'M06': 6, 'M07': 7, 'M08': 8,
    'G01': 1, 'G02': 2, 'G03': 3, 'G04': 4, 'G05': 5, 'G06': 6, 'G07': 7, 'G08': 8, 'G09': 9,
}

# ============== Step 3: 단원별 이론 파일 생성 ==============
print('\n=== Step 3: 단원별 이론 파일 생성 ===')

# 기본서 PDF 페이지 끝
basic_total = 501
hyak_total = 166
work_total = 165

for ch_id in CHAPTER_ORDER:
    ch_info = CHAPTERS[ch_id]
    out_path = OUT / f'단원_{ch_id}_{ch_info["name"]}.md'

    content = [f'# 단원 {ch_id} — {ch_info["name"].replace("_"," ")}\n']
    content.append(f'> **영역**: {ch_info["area"]}\n')
    content.append(f'> **기본서 해당 장**: 제{ch_info["book_chapters"]}장\n')

    # 목차
    content.append('\n## 🗺️ 본문 목차\n')
    content.append('- [📘 마인드 강의노트 (L1 - 압축, 시험 직전용)](#마인드)')
    content.append('- [📖 핵심요약서 (L2 - 빠른 복습)](#핵심요약서)')
    content.append('- [📚 기본서 (L3 - 본격 학습)](#기본서)')
    content.append('- [✏️ 워크북 (L4 - 논점별 문제)](#워크북)')
    content.append('\n---\n')

    # 마인드 강의노트 (L1)
    content.append('## <a name="마인드"></a>📘 마인드 강의노트 — L1 (압축·시험직전)\n')
    content.append('> 윤지훈 경제학 마인드. 학파별 흐름·그래프·명제 중심 압축본.\n')
    mind_dict = mind_micro if ch_info['area'] == '미시' else mind_macro
    mind_ch = MIND_TO_CHAPTER[ch_id]
    if mind_ch in mind_dict:
        content.append(mind_dict[mind_ch])
    content.append('\n---\n')

    # 핵심요약서 (L2)
    content.append('## <a name="핵심요약서"></a>📖 핵심요약서 — L2 (빠른 복습)\n')
    hyak_dict = hyak_micro if ch_info['area'] == '미시' else hyak_macro
    hyak_ranges = get_ranges(hyak_dict, ch_info['book_chapters'], hyak_total)
    if hyak_ranges:
        for c, s, e in hyak_ranges:
            content.append(f'\n### 핵심요약서 — 제{c}장 (p.{s}~{e})\n')
            content.append(extract_pages(hyak_pdf, s, e))
    content.append('\n---\n')

    # 기본서 (L3)
    content.append('## <a name="기본서"></a>📚 기본서 — L3 (본격 학습)\n')
    book_dict = basic_micro if ch_info['area'] == '미시' else basic_macro
    book_ranges = get_ranges(book_dict, ch_info['book_chapters'], basic_total)
    if book_ranges:
        for c, s, e in book_ranges:
            content.append(f'\n### 기본서 — 제{c}장 (p.{s}~{e})\n')
            content.append(extract_pages(basic_pdf, s, e))
    content.append('\n---\n')

    # 워크북 (논점별 - 작아서 같이 포함)
    content.append('## <a name="워크북"></a>✏️ 워크북 — 논점별 문제 (이론과 함께)\n')
    work_dict = work_micro if ch_info['area'] == '미시' else work_macro
    work_ranges = get_ranges(work_dict, ch_info['book_chapters'], work_total)
    if work_ranges:
        for c, s, e in work_ranges:
            content.append(f'\n### 워크북 — 제{c}장 (p.{s}~{e})\n')
            content.append(extract_pages(work_pdf, s, e))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 4: 문제 자료 단원별 분류 ==============
print('\n=== Step 4: 문제 자료 단원별 분류 ===')

# 기출 연도별 (감정평가사 2018-2025)
gichul_pdf = BASE / GICHUL_YEONDO
gichul_pages_by_ch = defaultdict(list)
r1 = pypdf.PdfReader(str(gichul_pdf))
for i in range(len(r1.pages)):
    text = r1.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        gichul_pages_by_ch[ch].append(i + 1)
for ch_id in CHAPTER_ORDER:
    print(f'  단원 {ch_id}: 기출연도별 {len(gichul_pages_by_ch[ch_id])}p')

# 연습문제
yeonseup_pdf = BASE / YEONSEUP_PDF
yeonseup_pages_by_ch = defaultdict(list)
r2 = pypdf.PdfReader(str(yeonseup_pdf))
for i in range(len(r2.pages)):
    text = r2.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        yeonseup_pages_by_ch[ch].append(i + 1)
print()
for ch_id in CHAPTER_ORDER:
    print(f'  단원 {ch_id}: 연습문제 {len(yeonseup_pages_by_ch[ch_id])}p')

# 고난도 100선 (문제 + 답안 통합)
gonan_q_pdf = BASE / GONAN_문제
gonan_a_pdf = BASE / GONAN_답안
gonan_pages_by_ch = defaultdict(list)  # 문제만 분류
r3 = pypdf.PdfReader(str(gonan_q_pdf))
for i in range(len(r3.pages)):
    text = r3.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        gonan_pages_by_ch[ch].append(i + 1)
print()
for ch_id in CHAPTER_ORDER:
    print(f'  단원 {ch_id}: 고난도100 {len(gonan_pages_by_ch[ch_id])}p')

# ============== Step 5: 문제 파일 생성 ==============
print('\n=== Step 5: 문제 파일 생성 ===')

for ch_id in CHAPTER_ORDER:
    ch_info = CHAPTERS[ch_id]
    out_path = OUT / f'문제_{ch_id}_{ch_info["name"]}.md'
    content = [f'# 문제 단원 {ch_id} — {ch_info["name"].replace("_"," ")}\n']
    content.append(f'> **영역**: {ch_info["area"]}\n')
    content.append('---\n')

    # 기출 연도별
    gichul_p = gichul_pages_by_ch[ch_id]
    if gichul_p:
        content.append(f'\n## 🎯 기출 연도별 (감정평가사 2018-2025) — {len(gichul_p)}p\n')
        content.append(extract_specific_pages(gichul_pdf, gichul_p[:50]))
        content.append('\n')

    # 연습문제 (가장쉬운경제학)
    yeonseup_p = yeonseup_pages_by_ch[ch_id]
    if yeonseup_p:
        content.append(f'\n## ✏️ 연습문제 (가장쉬운경제학) — {len(yeonseup_p)}p\n')
        content.append(extract_specific_pages(yeonseup_pdf, yeonseup_p[:50]))
        content.append('\n')

    # 고난도 100선
    gonan_p = gonan_pages_by_ch[ch_id]
    if gonan_p:
        content.append(f'\n## 🔥 고난도 100선 — {len(gonan_p)}p\n')
        content.append(extract_specific_pages(gonan_q_pdf, gonan_p))
        content.append('\n')

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 6: 부가 파일 ==============
print('\n=== Step 6: 부가 파일 ===')

# 미시·거시 영역별 학습 통계
통계_path = OUT / '_단원별_자료량.md'
통계_content = ['# 📊 단원별 자료량\n', '| 단원 | 영역 | 이론 KB | 문제 KB | 기출 P | 연습 P | 고난도 P |',
                '|---|---|---|---|---|---|---|']
for ch_id in CHAPTER_ORDER:
    ch_info = CHAPTERS[ch_id]
    theory_path = OUT / f'단원_{ch_id}_{ch_info["name"]}.md'
    problem_path = OUT / f'문제_{ch_id}_{ch_info["name"]}.md'
    tkb = theory_path.stat().st_size / 1024 if theory_path.exists() else 0
    pkb = problem_path.stat().st_size / 1024 if problem_path.exists() else 0
    통계_content.append(f'| {ch_id} | {ch_info["area"]} | {tkb:.0f} | {pkb:.0f} | {len(gichul_pages_by_ch[ch_id])} | {len(yeonseup_pages_by_ch[ch_id])} | {len(gonan_pages_by_ch[ch_id])} |')
통계_path.write_text('\n'.join(통계_content), encoding='utf-8')
print(f'  OK  _단원별_자료량.md  {통계_path.stat().st_size/1024:.0f}KB')

# 학파별 비교 표 (거시 핵심)
print('  📊 거시 학파별 비교 (단원 G06 기반)...')
# G06 단원 본문에서 학파 관련 부분 추출
G06_path = OUT / '단원_G06_학파별_비교.md'
학파_path = OUT / '_거시_학파별_비교표.md'
if G06_path.exists():
    text = G06_path.read_text(encoding='utf-8')
    # 학파별 표 부분 추출 (학파, 케인즈, 고전, 통화론자 등 키워드 모음)
    학파_content = ['# 📊 거시 학파별 비교 (단원 G06 발췌)\n', '> 거시경제학의 핵심: 학파별 흐름·정책 효과·주요 명제 비교\n\n']
    학파_content.append(text[:30000])  # 처음 30K
    학파_path.write_text('\n'.join(학파_content), encoding='utf-8')
    print(f'  OK  _거시_학파별_비교표.md  {학파_path.stat().st_size/1024:.0f}KB')

# 시험 직전 압축본 (마인드 + 핵심요약서)
print('  🏃 시험 직전 압축본...')
압축본_path = OUT / '🏃_시험직전_압축.md'
압축본_content = ['# 🏃 시험 직전 압축본 (경제학)\n', '> 시험 1~3일 전 복습용. 마인드 + 핵심요약서 통합.\n\n---\n']
압축본_content.append('## 📘 미시경제학 마인드 전체\n')
압축본_content.append(mind_micro_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## 📘 거시경제학 마인드 전체\n')
압축본_content.append(mind_macro_path.read_text(encoding='utf-8'))
압축본_content.append('\n\n---\n## 📖 핵심요약서 전체\n')
hyak_raw = (BASE / '_extract/raw_핵심요약서.md')
if hyak_raw.exists():
    압축본_content.append(hyak_raw.read_text(encoding='utf-8'))
압축본_path.write_text('\n'.join(압축본_content), encoding='utf-8')
print(f'  OK  🏃_시험직전_압축.md  {압축본_path.stat().st_size/1024:.0f}KB')

# 참조 파일 복사
print('  📑 참조 파일 복사...')
ref_files = [
    (BASE / '_extract/raw_기본서.md', '참조_기본서_전체.md'),
    (BASE / '_extract/raw_핵심요약서.md', '참조_핵심요약서_전체.md'),
    (BASE / '_extract/raw_워크북.md', '참조_워크북_전체.md'),
    (BASE / '_extract/raw_기출_연도별.md', '참조_기출연도별_2018_2025.md'),
    (BASE / '_extract/raw_연습문제.md', '참조_연습문제_전체.md'),
    (BASE / '_extract/raw_고난도100_문제.md', '참조_고난도100_문제.md'),
    (BASE / '_extract/raw_고난도100_답안.md', '참조_고난도100_답안.md'),
    (BASE / '_extract/raw_7급경제.md', '참조_7급경제_보너스.md'),
    (BASE / '미시경제학_마인드.md', '참조_미시경제학_마인드.md'),
    (BASE / '거시경제학_마인드.md', '참조_거시경제학_마인드.md'),
]
for src, dst in ref_files:
    if src.exists():
        shutil.copy(src, OUT / dst)

print('\n=== 완료 ===')
print(f'위치: {OUT}')
