#!/usr/bin/env python3
"""부동산학원론 단권화 빌드 (1차 객관식)
- 국승옥 강의노트 MD 기반 (9 PART, 60 Chapter)
- 단원 = PART (9개)
- 기본서·문제집·연도별기출·회차별기출해설 단원별 매핑
"""
import pypdf, re, os, json, shutil
from pathlib import Path
from collections import defaultdict, Counter

BASE = Path(__file__).parent
OUT = BASE / '_최종산출물_부동산학원론'
OUT.mkdir(exist_ok=True)

# ============== 9개 PART (강의노트 기반) ==============
CHAPTERS = {
    'PART01': {'name': '총론',                  'chapters': '01~04', 'desc': '부동산학·개념·분류·특성'},
    'PART02': {'name': '경제론',                'chapters': '05~08', 'desc': '수요·공급·탄력성·계산'},
    'PART03': {'name': '시장론',                'chapters': '09~14', 'desc': '시장·효율성·경기변동·거미집·여과'},
    'PART04': {'name': '정책론',                'chapters': '15~21', 'desc': '정책·외부효과·임대·분양·조세'},
    'PART05': {'name': '투자론',                'chapters': '22~30', 'desc': '수익·위험·결정이론·6계수·현금흐름·분석기법'},
    'PART06': {'name': '금융론',                'chapters': '31~38', 'desc': '대출·상환·MBS·REITs·PF·주택연금'},
    'PART07': {'name': '개발론',                'chapters': '39~46', 'desc': '개발·타당성·관리·마케팅·중개·권리분석'},
    'PART08': {'name': '토지경제와_지리경제',   'chapters': '47~51', 'desc': '지대·도시구조·공업/상업 입지'},
    'PART09': {'name': '감정평가론',            'chapters': '52~60', 'desc': '평가방식·물건별 평가·임대료'},
}
CHAPTER_ORDER = ['PART01','PART02','PART03','PART04','PART05','PART06','PART07','PART08','PART09']

# ============== 단원 키워드 (자동 분류용) ==============
CHAPTER_KEYWORDS = {
    'PART01': ['부동산학', '부동산 활동', '부동산 개념', '복합개념', '복합부동산', '나지', '건부지', '후보지', '이행지', '필지', '획지', '부동성', '부증성', '영속성', '개별성', '용도의 다양성', '병합·분할', '인접성', '저장', '토지의 분류'],
    'PART02': ['수요함수', '공급함수', '시장균형', '균형가격', '균형거래량', '가격탄력성', '소득탄력성', '교차탄력성', '수요의 탄력성', '공급의 탄력성', '대체재', '보완재', '정상재', '열등재', '기펜재', '수요량 변화', '공급량 변화'],
    'PART03': ['부동산 시장', '시장 효율성', '약형 효율적', '준강형', '강형', '경기변동', '경기순환', '에치켈', '거미집 모형', '거미집모형', '주거분리', '주택여과', '하향여과', '상향여과', '필터링'],
    'PART04': ['부동산 정책', '외부효과', '외부불경제', '공공재', '임대주택', '임대료 규제', '분양주택', '분양가 상한제', '청약제도', '부동산 조세', '취득세', '재산세', '종합부동산세', '양도소득세', '조세의 전가', '조세의 귀착', '쿠즈네츠'],
    'PART05': ['투자 수익', '투자 위험', '기대수익률', '요구수익률', '위험회피', '평균-분산', '포트폴리오', '분산투자', '체계적 위험', '비체계적 위험', '6계수', '일시불의 미래가치', '연금의 현재가치', '저당상수', '감채기금계수', '현금흐름', '영업소득세', 'BTCF', 'ATCF', 'NPV', 'IRR', '순현가법', '내부수익률법', '수익성지수', '회수기간법', '회계적 수익률법', '어림셈법'],
    'PART06': ['부동산 금융', '주택금융', '직접금융', '간접금융', '부동산금융의 위험', '대출금액', 'LTV', 'DTI', 'DSR', '대출금리', '저당잔금', '상환방식', '원리금균등', '원금균등', '체증식', 'CAM', 'CPM', 'GPM', 'MBS', '주택저당증권', '주택저당채권', '유동화', 'CMO', '부동산투자회사', 'REITs', '리츠', '프로젝트 대출', 'PF', '주택연금'],
    'PART07': ['부동산 개발', '개발의 위험', '시장성 분석', '타당성 분석', '민감도 분석', '흡수율', '개발방식', '도급', '자체개발', '신탁개발', '컨소시엄', 'BTL', 'BTO', '부동산 관리', '자산관리', '시설관리', '재산관리', '부동산 마케팅', 'STP', '4P', '시장세분화', '표적시장', '포지셔닝', '부동산 중개', '중개수수료', '권리분석', '에스크로'],
    'PART08': ['지대 이론', '차액지대', '절대지대', '독점지대', '준지대', '경제지대', '리카도', '마르크스', '마샬', '튀넨', '입지론', '동심원', '버제스', '선형이론', '호이트', '다핵심', '해리스', '울만', '베버', '최소비용', '최대수요', '레일리', '컨버스', '허프', '넬슨', '소매중력모형'],
    'PART09': ['지역분석', '개별분석', '근린지역', '인근지역', '유사지역', '동일수급권', '균형의 원칙', '적합의 원칙', '예측의 원칙', '변동의 원칙', '대체의 원칙', '기여의 원칙', '거래사례비교법', '원가법', '수익환원법', '재조달원가', '감가수정', '적산법', '임대사례', '수익분석법', '시산가액', '감정평가에 관한 규칙', '감정평가의 3방식', '물건별 주된 평가'],
}

# ============== 책 파일 ==============
BOOKS = {
    '기본서':   '1.5차 부동산학원론_기본서 [업데이트일_251124].pdf',
    '문제집':   '1.5차 부동산학원론 문제집 [업데이트일_26.04.02].pdf',
    '강의노트': '국승옥_강의노트.md',
}

# ============== 문제 PDF ==============
GICHUL_YEONDO = '감정평가사 부동산학원론 연도별 기출문제집 [2018년-2025년] [업데이트일_26.05.10].pdf'
GICHUL_HOECHA = [
    ('감정평가사_2022_33회', '감정평가사 부동산학원론 2022년 33회 기출문제 해설.pdf'),
    ('감정평가사_2023_34회', '감정평가사 부동산학원론 2023년 34회 기출문제 해설.pdf'),
    ('감정평가사_2024',      '2024년 감정평가사 부동산학원론 기출해설.pdf'),
    ('공인중개사_2021_32회', '공인중개사 부동산학개론 2021년 32회 기출문제 해설.pdf'),
    ('공인중개사_2022_33회', '공인중개사 부동산학개론 2022년 33회 기출문제 해설.pdf'),
    ('공인중개사_2023_34회', '공인중개사 부동산학개론 2023년 34회 기출문제 해설.pdf'),
]

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

def extract_all_text(pdf_path):
    """전체 PDF 텍스트 추출 (페이지별)"""
    try:
        r = pypdf.PdfReader(str(pdf_path))
    except Exception:
        return []
    pages = []
    for i in range(len(r.pages)):
        try:
            text = r.pages[i].extract_text() or ''
        except Exception:
            text = ''
        pages.append(text)
    return pages

def classify_text(text):
    # 페이지 헤더(첫 100자)는 보통 시험명·과목명이 들어가서 잘못된 분류 유발 → 본문만 사용
    body = text[100:] if len(text) > 100 else text
    scores = {}
    for ch, kws in CHAPTER_KEYWORDS.items():
        scores[ch] = sum(body.count(k) for k in kws)
    if not any(scores.values()):
        return None
    return max(scores, key=scores.get)

# ============== Step 1: 강의노트 MD 파싱 ==============
print('=== Step 1: 강의노트 MD 파싱 ===')
gangui_path = BASE / BOOKS['강의노트']
gangui_text = gangui_path.read_text(encoding='utf-8')

# PART별 분할
part_pattern = re.compile(r'^## PART (\d+) — (.+)$', re.MULTILINE)
matches = list(part_pattern.finditer(gangui_text))
gangui_parts = {}
for i, m in enumerate(matches):
    part_no = int(m.group(1))
    part_name = m.group(2)
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else len(gangui_text)
    gangui_parts[f'PART0{part_no}'] = gangui_text[start:end]
    print(f'  PART0{part_no} {part_name}: {len(gangui_text[start:end])}바이트')

# ============== Step 2: 기본서 페이지별 PART 키워드 분류 ==============
# 기본서는 PART 구조와 다르게 편/장으로 묶여있음 → 페이지별 키워드 분류 사용
print('\n=== Step 2: 기본서 페이지별 PART 분류 ===')
gibon_pdf = BASE / BOOKS['기본서']
gibon_pages = extract_all_text(gibon_pdf)
print(f'  기본서 총 {len(gibon_pages)}p')

gibon_pages_by_part = defaultdict(list)
for i, text in enumerate(gibon_pages):
    # 목차 페이지 제외 (p.1~6)
    if i < 6: continue
    ch = classify_text(text)
    if ch:
        gibon_pages_by_part[ch].append(i + 1)

for part_id in CHAPTER_ORDER:
    print(f'  기본서 {part_id}: {len(gibon_pages_by_part[part_id])}p')

# ============== Step 3: 단원별 이론 파일 생성 ==============
print('\n=== Step 3: 단원별 이론 파일 생성 ===')

for part_id in CHAPTER_ORDER:
    info = CHAPTERS[part_id]
    out_path = OUT / f'단원_{part_id}_{info["name"]}.md'
    content = [f'# 단원 {part_id} — {info["name"].replace("_"," ")}\n']
    content.append(f'> **포함 Chapter**: {info["chapters"]}')
    content.append(f'> **수업 주제**: {info["desc"]}\n')

    content.append('\n## 🗺️ 본문 목차\n')
    content.append('- [📘 국승옥 강의노트 (L1 - 메인 자료, 단권화)](#강의노트)')
    content.append('- [📚 기본서 (L2 - 본격 학습·세부 보강)](#기본서)')
    content.append('\n---\n')

    # 강의노트 (L1) — 메인 자료
    content.append('## <a name="강의노트"></a>📘 국승옥 강의노트 — L1 (메인·단권화)\n')
    content.append('> 시험 직전 단권화용으로 압축된 자료. 표·명제(①②③) 중심.\n')
    if part_id in gangui_parts:
        content.append(gangui_parts[part_id])
    content.append('\n---\n')

    # 기본서 (L2)
    content.append('## <a name="기본서"></a>📚 기본서 — L2 (본격 학습)\n')
    content.append('> 박문각 1.5차 부동산학원론 기본서 본문 중 본 PART 관련 페이지 (키워드 자동 분류).\n')
    g_pages = gibon_pages_by_part[part_id]
    if g_pages:
        content.append(f'\n### 기본서 발췌 (총 {len(g_pages)}p)\n')
        content.append(extract_specific_pages(gibon_pdf, g_pages[:80]))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 4: 문제 자료 단원별 분류 ==============
print('\n=== Step 4: 문제 자료 단원별 분류 ===')

# 4-1) 연도별 기출문제집
gichul_pdf = BASE / GICHUL_YEONDO
gichul_pages_by_ch = defaultdict(list)
r1 = pypdf.PdfReader(str(gichul_pdf))
for i in range(len(r1.pages)):
    text = r1.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        gichul_pages_by_ch[ch].append(i + 1)
print(f'  연도별기출 ({len(r1.pages)}p)')
for part_id in CHAPTER_ORDER:
    print(f'    {part_id}: {len(gichul_pages_by_ch[part_id])}p')

# 4-2) 문제집
moonjae_pdf = BASE / BOOKS['문제집']
moonjae_pages_by_ch = defaultdict(list)
r2 = pypdf.PdfReader(str(moonjae_pdf))
for i in range(len(r2.pages)):
    text = r2.pages[i].extract_text() or ''
    ch = classify_text(text)
    if ch:
        moonjae_pages_by_ch[ch].append(i + 1)
print(f'\n  문제집 ({len(r2.pages)}p)')
for part_id in CHAPTER_ORDER:
    print(f'    {part_id}: {len(moonjae_pages_by_ch[part_id])}p')

# 4-3) 회차별 기출 해설
hoecha_pages_by_ch = defaultdict(lambda: defaultdict(list))  # {label: {part: [pages]}}
for label, fname in GICHUL_HOECHA:
    fpath = BASE / fname
    if not fpath.exists():
        print(f'  경고: {fname} 없음')
        continue
    try:
        rr = pypdf.PdfReader(str(fpath))
    except Exception as e:
        print(f'  {label} 읽기 실패: {e}')
        continue
    for i in range(len(rr.pages)):
        text = rr.pages[i].extract_text() or ''
        ch = classify_text(text)
        if ch:
            hoecha_pages_by_ch[label][ch].append(i + 1)
print(f'\n  회차별 기출 해설:')
for label, _ in GICHUL_HOECHA:
    total = sum(len(pgs) for pgs in hoecha_pages_by_ch[label].values())
    print(f'    {label}: {total}p 분류완료')

# ============== Step 5: 문제 파일 생성 ==============
print('\n=== Step 5: 문제 파일 생성 ===')

for part_id in CHAPTER_ORDER:
    info = CHAPTERS[part_id]
    out_path = OUT / f'문제_{part_id}_{info["name"]}.md'
    content = [f'# 문제 단원 {part_id} — {info["name"].replace("_"," ")}\n']
    content.append(f'> **포함 Chapter**: {info["chapters"]}\n')
    content.append('---\n')

    # 연도별 기출
    g_pages = gichul_pages_by_ch[part_id]
    if g_pages:
        content.append(f'\n## 🎯 연도별 기출 (감정평가사 2018-2025) — {len(g_pages)}p\n')
        content.append(extract_specific_pages(gichul_pdf, g_pages[:60]))
        content.append('\n')

    # 문제집
    m_pages = moonjae_pages_by_ch[part_id]
    if m_pages:
        content.append(f'\n## ✏️ 문제집 (1.5차 부동산학원론) — {len(m_pages)}p\n')
        content.append(extract_specific_pages(moonjae_pdf, m_pages[:60]))
        content.append('\n')

    # 회차별 기출 해설
    for label, fname in GICHUL_HOECHA:
        fpath = BASE / fname
        h_pages = hoecha_pages_by_ch[label].get(part_id, [])
        if h_pages and fpath.exists():
            content.append(f'\n## 📝 {label.replace("_"," ")} 기출해설 — {len(h_pages)}p\n')
            content.append(extract_specific_pages(fpath, h_pages))
            content.append('\n')

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 6: 부가 파일 ==============
print('\n=== Step 6: 부가 파일 ===')

# 6-1) 단원별 자료량
통계_path = OUT / '_단원별_자료량.md'
통계 = ['# 📊 단원별 자료량\n', '| 단원 | 명칭 | 이론 KB | 문제 KB | 기출 P | 문제집 P |',
        '|---|---|---|---|---|---|']
for part_id in CHAPTER_ORDER:
    info = CHAPTERS[part_id]
    tp = OUT / f'단원_{part_id}_{info["name"]}.md'
    pp = OUT / f'문제_{part_id}_{info["name"]}.md'
    tkb = tp.stat().st_size / 1024 if tp.exists() else 0
    pkb = pp.stat().st_size / 1024 if pp.exists() else 0
    통계.append(f'| {part_id} | {info["name"].replace("_"," ")} | {tkb:.0f} | {pkb:.0f} | {len(gichul_pages_by_ch[part_id])} | {len(moonjae_pages_by_ch[part_id])} |')
통계_path.write_text('\n'.join(통계), encoding='utf-8')
print(f'  OK  _단원별_자료량.md  {통계_path.stat().st_size/1024:.0f}KB')

# 6-2) 출제빈도 분석 (강의노트 자체 기출분석 기반)
빈도_path = OUT / '_출제빈도_분석.md'
빈도_content = """# 📈 부동산학원론 출제빈도 분석

> 강의노트 기출분석표(31회~36회, 6개년) 기반 출제 빈도 정리.
> 매년 약 40문항 출제 기준.

## 🥇 최다 출제 영역 (★★★)

| PART | 영역 | 비고 |
|---|---|---|
| PART07 개발론 | 부동산 개발의 이해 | **6회 연속 출제 — 최다 빈출** |
| PART04 정책론 | 다양한 부동산 정책, 조세 정책 | 매년 다출제, 시사성 높음 |
| PART05 투자론 | 투자분석기법 (NPV·IRR·수익성지수 등) | 거의 매년 |
| PART06 금융론 | 대출 상환 방식, 부동산 간접투자 (REITs) | 빈출 |

## 🥈 꾸준한 출제 영역 (★★)

| PART | 영역 |
|---|---|
| PART03 시장론 | 시장과 정보 효율성, 경기변동 |
| PART09 감정평가론 | 감정평가 방식, 물건별 주된 평가방법 |
| PART02 경제론 | 가격탄력성·시장균형 (계산문제) |
| PART08 토지경제 | 입지 이론 (베버·레일리·허프·튀넨) |

## 🥉 저출제 영역 (★)

- **PART01 총론**: 부동산학 자체, 부동산 활동 → 빠르게 훑고 넘어갈 영역
- 부동산 가치의 본질 같은 추상적 개념 영역

---

## 💡 학습 우선순위 (1차 합격용)

1. **개발론·정책론·투자론·금융론** = 매년 합해서 15~20문항 (전체 1/2)
2. **시장론·감정평가론** = 5~8문항
3. **경제론·토지경제** = 계산문제 중심 5~8문항
4. **총론** = 핵심 명제만 (3~5문항)

---

## 📊 PART별 단원 매핑

| PART | 명칭 | Chapter | 수업 주제 |
|---|---|---|---|
| PART01 | 총론 | 01~04 | 부동산학·개념·분류·특성 |
| PART02 | 경제론 | 05~08 | 수요·공급·탄력성·계산 |
| PART03 | 시장론 | 09~14 | 시장·효율성·경기변동·거미집·여과 |
| PART04 | 정책론 | 15~21 | 정책·외부효과·임대·분양·조세 |
| PART05 | 투자론 | 22~30 | 수익·위험·결정이론·6계수·현금흐름·분석기법 |
| PART06 | 금융론 | 31~38 | 대출·상환·MBS·REITs·PF·주택연금 |
| PART07 | 개발론 | 39~46 | 개발·타당성·관리·마케팅·중개·권리분석 |
| PART08 | 토지경제·지리경제 | 47~51 | 지대·도시구조·공업/상업 입지 |
| PART09 | 감정평가론 | 52~60 | 평가방식·물건별 평가·임대료 |

"""
빈도_path.write_text(빈도_content, encoding='utf-8')
print(f'  OK  _출제빈도_분석.md  {빈도_path.stat().st_size/1024:.0f}KB')

# 6-3) 시험 직전 압축본
print('  🏃 시험 직전 압축본...')
압축_path = OUT / '🏃_시험직전_압축.md'
압축 = ['# 🏃 시험 직전 압축본 (부동산학원론)\n',
       '> 시험 1~3일 전 복습용. 국승옥 강의노트 전체 (시험 직전 단권화 자료).\n\n---\n']
압축.append(gangui_text)
압축_path.write_text('\n'.join(압축), encoding='utf-8')
print(f'  OK  🏃_시험직전_압축.md  {압축_path.stat().st_size/1024:.0f}KB')

# 6-4) 강의노트 원본 복사
print('  📑 강의노트 원본 복사...')
shutil.copy(gangui_path, OUT / '참조_국승옥_강의노트.md')

print('\n=== 완료 ===')
print(f'위치: {OUT}')
