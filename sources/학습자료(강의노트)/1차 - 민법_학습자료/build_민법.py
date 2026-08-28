#!/usr/bin/env python3
"""민법 단권화 빌드 (1차 객관식)
- 위패스 마이 정리(MD) 메인 + 기본서/핵심요약서/문제집 PDF 보강
- 11개 단원 (민법총칙 6 + 물권법 5)
"""
import pypdf, re, os, json, shutil
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent
OUT = BASE / '_최종산출물_민법'
OUT.mkdir(exist_ok=True)

# ============== 11개 단원 (기본서 구조 기반) ==============
CHAPTERS = {
    'M01': {'name': '서론',                    'area': '민법총칙', 'desc': '법원·법률관계·법률행위 변동'},
    'M02': {'name': '자연인',                  'area': '민법총칙', 'desc': '권리능력·의사능력·행위능력·부재실종·주소'},
    'M03': {'name': '법인',                    'area': '민법총칙', 'desc': '법인 설립·기관·권리능력·소멸'},
    'M04': {'name': '물건',                    'area': '민법총칙', 'desc': '권리의 객체 — 동산·부동산·주물·종물·과실'},
    'M05': {'name': '법률행위',                'area': '민법총칙', 'desc': '법률행위·의사표시·대리·무효취소·부관'},
    'M06': {'name': '기간과_소멸시효',         'area': '민법총칙', 'desc': '기간·소멸시효·신의칙'},
    'B01': {'name': '물권변동',                'area': '물권법',   'desc': '물권의 종류·효력·부동산/동산 물권변동·등기'},
    'B02': {'name': '점유권',                  'area': '물권법',   'desc': '점유·자주/타주·점유권의 취득과 효력'},
    'B03': {'name': '소유권',                  'area': '물권법',   'desc': '소유권·취득시효·공동소유·명의신탁'},
    'B04': {'name': '용익물권',                'area': '물권법',   'desc': '지상권·지역권·전세권'},
    'B05': {'name': '담보물권',                'area': '물권법',   'desc': '유치권·질권·저당권·가등기담보'},
}
CHAPTER_ORDER = ['M01','M02','M03','M04','M05','M06','B01','B02','B03','B04','B05']

# ============== 단원 키워드 (자동 분류용) ==============
CHAPTER_KEYWORDS = {
    'M01': ['법원(法源)', '법원의 의의', '관습법', '판례법', '조리', '신의성실', '법률관계와 권리', '법률관계의 변동', '권리의 종류', '권리의 경합', '권리의 충돌', '호의관계', '신뢰관계', '사실관계'],
    'M02': ['권리능력', '의사능력', '행위능력', '미성년자', '피성년후견', '피한정후견', '피특정후견', '제한능력자', '법정대리인', '태아', '부재', '실종선고', '실종', '주소', '거소', '가족관계', '인지', '대습상속'],
    'M03': ['법인', '사단법인', '재단법인', '비법인사단', '법인 아닌 사단', '권리능력 없는 사단', '법인의 설립', '법인의 기관', '이사', '감사', '사원총회', '법인의 정관', '법인의 소멸', '청산'],
    'M04': ['물건', '부동산', '동산', '주물', '종물', '원물', '과실', '천연과실', '법정과실', '권리의 객체', '특정물', '불특정물', '대체물', '소비물'],
    'M05': ['법률행위', '의사표시', '진의 아닌', '비진의', '통정허위표시', '착오', '사기', '강박', '하자있는 의사표시', '대리', '복대리', '무권대리', '표현대리', '쌍방대리', '자기계약', '무효', '취소', '추인', '법률행위의 부관', '조건', '기한', '정지조건', '해제조건', '시기', '종기', '불공정한 법률행위', '제103조', '제104조', '반사회적'],
    'M06': ['기간', '초일불산입', '말일', '시효', '소멸시효', '시효의 기산점', '시효의 중단', '시효의 정지', '시효이익의 포기', '제척기간', '신의성실의 원칙', '권리남용', '실효의 원칙', '사정변경'],
    'B01': ['물권', '물권법정주의', '물권의 종류', '물권의 효력', '물권적 청구권', '물권변동', '부동산물권변동', '동산물권변동', '등기', '가등기', '본등기', '명인방법', '선의취득', '제186조', '제187조', '인도', '점유개정', '간이인도', '목적물반환청구권'],
    'B02': ['점유', '점유권', '자주점유', '타주점유', '간접점유', '직접점유', '점유보호청구', '점유의 추정', '점유의 승계', '점유개정', '평온', '공연', '점유물반환', '점유자와 회복자', '선의의 점유자'],
    'B03': ['소유권', '취득시효', '점유취득시효', '등기부 취득시효', '공동소유', '공유', '합유', '총유', '명의신탁', '구분소유', '집합건물', '상린관계', '인지사용청구권', '주위토지통행권', '경계', '소유권에 기한 물권적 청구권', '물상청구권', '첨부', '부합', '혼화', '가공'],
    'B04': ['용익물권', '지상권', '지역권', '전세권', '관습법상 법정지상권', '분묘기지권', '구분지상권', '요역지', '승역지', '지료', '존속기간', '전세금'],
    'B05': ['담보물권', '유치권', '질권', '동산질권', '권리질권', '저당권', '근저당', '공동저당', '가등기담보', '양도담보', '담보권 실행', '경매', '채권담보', '담보제공', '피담보채권', '우선변제권'],
}

# ============== 파일 ==============
BOOKS = {
    '기본서':     '민법_기본서 [업데이트일_231025].pdf',
    '문제집':     '민법 문제집 [업데이트일_26.03.09].pdf',
    '핵심요약서': '민법 핵심요약서 [업데이트일_26.03.09].pdf',
}
GICHUL_YEONDO = '감정평가사 민법 연도별 기출문제집 [2018년-2025년] [업데이트일_26.04.02].pdf'
JUNG_MD = {
    '민법총칙': '민법총칙_정리.md',
    '물권법':   '물권법_정리.md',
}

# ============== 기본서/문제집/핵심요약서 PART·장 페이지 매핑 (수동 검출 결과) ==============
# 검출 결과: (단원ID → (PDF, start_page, end_page))
# 기본서
GIBON_RANGES = {
    'M01': (5, 26),
    'M02': (27, 54),
    'M03': (55, 78),
    'M04': (79, 88),
    'M05': (89, 186),
    'M06': (187, 208),
    'B01': (211, 244),
    'B02': (245, 264),
    'B03': (265, 316),
    'B04': (317, 356),
    'B05': (357, 407),
}

# 핵심요약서 (CHAPTER 헤더 수동 매핑)
# 핵심요약서 162p — TOC에서 CHAPTER 시작 페이지
# 11 → CH01 서론 (M01), 51 → CH04 물건(M04) 등, 101 → CH06 기간소멸시효(M06), 151 → 물권법 CH05 담보물권(B05)
# 정확한 매핑은 자동검출 + 수동 보강

# 문제집 (CHAPTER 헤더 수동 매핑)
# 문제집 515p — 1장 서론 부터 시작 (p.5 본문 시작)

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
    body = text[100:] if len(text) > 100 else text
    scores = {}
    for ch, kws in CHAPTER_KEYWORDS.items():
        scores[ch] = sum(body.count(k) for k in kws)
    if not any(scores.values()):
        return None
    return max(scores, key=scores.get)

# ============== Step 1: 정리.md 키워드 기반 발췌 ==============
print('=== Step 1: 위패스 마이 정리.md 단원별 매핑 ===')
# 정리.md는 김묘엽 교재(15+31장) 구조. 단원(11개)과 직접 1:1 매핑 안됨 → 키워드 기반으로 분류
jung_text = {}
for area, fname in JUNG_MD.items():
    p = BASE / fname
    if p.exists():
        jung_text[area] = p.read_text(encoding='utf-8')
        print(f'  {area}: {len(jung_text[area])}자 로드')

def split_md_by_chapter(text):
    """## 제N장 헤더 기준 분할"""
    pattern = re.compile(r'^## (제\d+장.*)$', re.MULTILINE)
    matches = list(pattern.finditer(text))
    chunks = []
    if not matches:
        return [('전체', text)]
    # 헤더 이전 텍스트(서문) 포함
    if matches[0].start() > 0:
        chunks.append(('서문', text[:matches[0].start()]))
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        chunks.append((m.group(1).strip(), text[start:end]))
    return chunks

jung_chunks = {}  # {area: [(title, content), ...]}
for area, txt in jung_text.items():
    jung_chunks[area] = split_md_by_chapter(txt)
    print(f'  {area} 분할: {len(jung_chunks[area])}청크')

def assign_chunk_to_chapter(chunk_text):
    """청크 내용을 키워드로 단원 분류"""
    return classify_text(chunk_text)

# 단원별 정리.md 청크 모음
jung_by_chapter = defaultdict(list)
for area, chunks in jung_chunks.items():
    for title, content in chunks:
        ch = assign_chunk_to_chapter(content)
        if ch:
            jung_by_chapter[ch].append((area, title, content))
            print(f'    {area} > {title} → {ch}')

# ============== Step 2: 핵심요약서 PART/CHAPTER 페이지 검출 ==============
print('\n=== Step 2: 핵심요약서 CHAPTER 페이지 검출 ===')
haek_pdf = BASE / BOOKS['핵심요약서']
haek_pages = extract_all_text(haek_pdf)
# CHAPTER 0N 헤더 검출
haek_starts = {}
current_part = None
for i, t in enumerate(haek_pages):
    head = t[:300]
    if 'PART' in head and '민법' in head and '총칙' in head:
        current_part = 'M'
    elif 'PART' in head and '물권법' in head:
        current_part = 'B'
    m = re.search(r'CHAPTER\s*0?(\d+)', head)
    if m and current_part:
        ch_no = int(m.group(1))
        key = f'{current_part}0{ch_no}' if ch_no < 10 else f'{current_part}{ch_no}'
        if key in CHAPTERS and key not in haek_starts:
            haek_starts[key] = i + 1

# Sort and compute ranges
haek_ranges = {}
sorted_haek = sorted(haek_starts.items(), key=lambda x: x[1])
for i, (ch, start) in enumerate(sorted_haek):
    end = sorted_haek[i+1][1] - 1 if i+1 < len(sorted_haek) else len(haek_pages)
    haek_ranges[ch] = (start, end)
for ch in CHAPTER_ORDER:
    if ch in haek_ranges:
        s, e = haek_ranges[ch]
        print(f'  {ch}: p.{s}~{e} ({e-s+1}p)')
    else:
        print(f'  {ch}: 검출 실패')

# ============== Step 3: 문제집 PART/장 페이지 검출 ==============
print('\n=== Step 3: 문제집 장 페이지 검출 ===')
moonjae_pdf = BASE / BOOKS['문제집']
moonjae_pages = extract_all_text(moonjae_pdf)
moonjae_starts = {}
current_part = None
for i, t in enumerate(moonjae_pages):
    if i < 3: continue
    head = t[:300]
    # PART 검출
    if 'PART 01' in head and '민법' in head:
        current_part = 'M'
    elif 'PART 02' in head and '물권법' in head:
        current_part = 'B'
    elif '제1편 민법총칙' in head or '민법총칙' in head[:80]:
        if current_part is None:
            current_part = 'M'
    elif '제2편 물권법' in head or '물권법' in head[:80]:
        # 물권법 첫 발견 시 전환
        if current_part != 'B' and '서론' in head and '서설' in head[:300]:
            current_part = 'B'
    # 제N장 검출
    m = re.search(r'제\s*([1-9])\s*장\s+[가-힣]', head)
    if m and current_part:
        ch_no = int(m.group(1))
        key = f'{current_part}0{ch_no}'
        if key in CHAPTERS and key not in moonjae_starts:
            moonjae_starts[key] = i + 1

# 위 검출이 부정확할 수 있으므로 키워드 기반 분류로 페이지별 분류
moonjae_pages_by_ch = defaultdict(list)
for i, t in enumerate(moonjae_pages):
    if i < 3: continue
    ch = classify_text(t)
    if ch:
        moonjae_pages_by_ch[ch].append(i + 1)
for ch in CHAPTER_ORDER:
    print(f'  문제집 {ch}: {len(moonjae_pages_by_ch[ch])}p')

# ============== Step 4: 연도별 기출 페이지 분류 ==============
print('\n=== Step 4: 연도별 기출 단원별 분류 ===')
gichul_pdf = BASE / GICHUL_YEONDO
gichul_pages = extract_all_text(gichul_pdf)
gichul_pages_by_ch = defaultdict(list)
for i, t in enumerate(gichul_pages):
    ch = classify_text(t)
    if ch:
        gichul_pages_by_ch[ch].append(i + 1)
print(f'  연도별 기출 총 {len(gichul_pages)}p')
for ch in CHAPTER_ORDER:
    print(f'  {ch}: {len(gichul_pages_by_ch[ch])}p')

# ============== Step 5: 이론 파일 생성 ==============
print('\n=== Step 5: 단원별 이론 파일 생성 ===')

gibon_pdf = BASE / BOOKS['기본서']

for ch_id in CHAPTER_ORDER:
    info = CHAPTERS[ch_id]
    out_path = OUT / f'단원_{ch_id}_{info["name"]}.md'
    content = [f'# 단원 {ch_id} — {info["name"].replace("_"," ")}\n']
    content.append(f'> **영역**: {info["area"]}')
    content.append(f'> **수업 주제**: {info["desc"]}\n')

    content.append('\n## 🗺️ 본문 목차\n')
    content.append('- [📘 위패스 마이 정리 (L1 - 메인 단권화)](#정리)')
    content.append('- [📖 핵심요약서 (L2 - 빠른 복습)](#핵심요약서)')
    content.append('- [📚 기본서 (L3 - 본격 학습)](#기본서)')
    content.append('\n---\n')

    # L1: 위패스 마이 정리
    content.append('## <a name="정리"></a>📘 위패스 마이 정리 — L1 (메인·단권화)\n')
    content.append('> 김묘엽 교수 「위패스 마이 민법총칙/물권법」 교재 정리본 (키워드 자동 분류).\n')
    if ch_id in jung_by_chapter:
        for area, title, jt in jung_by_chapter[ch_id]:
            content.append(f'\n### [{area}] {title}\n')
            content.append(jt)
    content.append('\n---\n')

    # L2: 핵심요약서
    content.append('## <a name="핵심요약서"></a>📖 핵심요약서 — L2 (빠른 복습)\n')
    content.append('> 스터디파이터 민법 핵심요약서.\n')
    if ch_id in haek_ranges:
        s, e = haek_ranges[ch_id]
        content.append(f'\n### 핵심요약서 (p.{s}~{e})\n')
        content.append(extract_pages(haek_pdf, s, e))
    content.append('\n---\n')

    # L3: 기본서
    content.append('## <a name="기본서"></a>📚 기본서 — L3 (본격 학습)\n')
    content.append('> 감정평가사 민법 기본서 (407p) 해당 장.\n')
    if ch_id in GIBON_RANGES:
        s, e = GIBON_RANGES[ch_id]
        content.append(f'\n### 기본서 (p.{s}~{e})\n')
        content.append(extract_pages(gibon_pdf, s, e))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 6: 문제 파일 생성 ==============
print('\n=== Step 6: 단원별 문제 파일 생성 ===')

for ch_id in CHAPTER_ORDER:
    info = CHAPTERS[ch_id]
    out_path = OUT / f'문제_{ch_id}_{info["name"]}.md'
    content = [f'# 문제 단원 {ch_id} — {info["name"].replace("_"," ")}\n']
    content.append(f'> **영역**: {info["area"]}\n')
    content.append('---\n')

    # 연도별 기출
    g_pages = gichul_pages_by_ch[ch_id]
    if g_pages:
        content.append(f'\n## 🎯 연도별 기출 (감정평가사 2018-2025) — {len(g_pages)}p\n')
        content.append(extract_specific_pages(gichul_pdf, g_pages[:80]))
        content.append('\n')

    # 문제집
    m_pages = moonjae_pages_by_ch[ch_id]
    if m_pages:
        content.append(f'\n## ✏️ 문제집 (스터디파이터 민법) — {len(m_pages)}p\n')
        content.append(extract_specific_pages(moonjae_pdf, m_pages[:80]))
        content.append('\n')

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 7: 부가 파일 ==============
print('\n=== Step 7: 부가 파일 ===')

# 7-1) 단원별 자료량
통계_path = OUT / '_단원별_자료량.md'
통계 = ['# 📊 단원별 자료량\n', '| 단원 | 영역 | 이론 KB | 문제 KB | 기출 P | 문제집 P |',
        '|---|---|---|---|---|---|']
for ch_id in CHAPTER_ORDER:
    info = CHAPTERS[ch_id]
    tp = OUT / f'단원_{ch_id}_{info["name"]}.md'
    pp = OUT / f'문제_{ch_id}_{info["name"]}.md'
    tkb = tp.stat().st_size / 1024 if tp.exists() else 0
    pkb = pp.stat().st_size / 1024 if pp.exists() else 0
    통계.append(f'| {ch_id} | {info["area"]} | {tkb:.0f} | {pkb:.0f} | {len(gichul_pages_by_ch[ch_id])} | {len(moonjae_pages_by_ch[ch_id])} |')
통계_path.write_text('\n'.join(통계), encoding='utf-8')
print(f'  OK  _단원별_자료량.md')

# 7-2) 출제빈도 분석
빈도_path = OUT / '_출제빈도_분석.md'
빈도_content = """# 📈 민법 출제빈도 분석

> 감정평가사 1차 민법 2018-2025년 기출 기반.
> 매년 약 40문항 출제 (민법총칙 ~25문항 + 물권법 ~15문항).

## 🥇 최다 출제 (★★★)

| 단원 | 영역 | 핵심 빈출 |
|---|---|---|
| **M05 법률행위** | 민법총칙 | 의사표시·대리·무효취소·법률행위 부관 — **단연 최다 출제** |
| **M02 자연인** | 민법총칙 | 권리능력·행위능력·실종선고·태아 |
| **M06 소멸시효·신의칙** | 민법총칙 | 시효 기산점·중단·정지 |
| **B03 소유권** | 물권법 | 취득시효·공동소유·명의신탁·상린관계 |

## 🥈 꾸준한 출제 (★★)

| 단원 | 영역 |
|---|---|
| M03 법인 | 민법총칙 (비법인사단 빈출) |
| B01 물권변동 | 물권법 (등기·선의취득) |
| B05 담보물권 | 물권법 (저당권·유치권) |

## 🥉 비교적 적은 출제 (★)

- M01 서론, M04 물건
- B02 점유권, B04 용익물권 (지상권 등 다소 출제)

---

## 💡 학습 우선순위 (1차 합격용)

1. **M05 법률행위** = 매년 5~8문항 (단원 1개로 시험의 1/4 차지)
2. **M02 자연인 / M06 소멸시효 / B03 소유권** = 매년 3~5문항씩
3. **B05 담보물권 / M03 법인 / B01 물권변동** = 매년 2~4문항
4. 나머지(M01·M04·B02·B04) = 매년 1~2문항

## 📊 단원 매핑

| 단원 | 영역 | 명칭 |
|---|---|---|
| M01 | 민법총칙 | 서론 (법원·법률관계) |
| M02 | 민법총칙 | 자연인 (권리능력·행위능력) |
| M03 | 민법총칙 | 법인 |
| M04 | 민법총칙 | 물건 (권리의 객체) |
| M05 ★★★ | 민법총칙 | 법률행위 (의사표시·대리·무효취소·부관) |
| M06 | 민법총칙 | 기간과 소멸시효 (신의칙 포함) |
| B01 | 물권법 | 물권변동 |
| B02 | 물권법 | 점유권 |
| B03 ★★★ | 물권법 | 소유권 (취득시효·공동소유·명의신탁) |
| B04 | 물권법 | 용익물권 (지상권·지역권·전세권) |
| B05 | 물권법 | 담보물권 (유치권·질권·저당권) |
"""
빈도_path.write_text(빈도_content, encoding='utf-8')
print(f'  OK  _출제빈도_분석.md')

# 7-3) 시험 직전 압축본
print('  🏃 시험 직전 압축본...')
압축_path = OUT / '🏃_시험직전_압축.md'
압축 = ['# 🏃 시험 직전 압축본 (민법)\n',
       '> 시험 1~3일 전 복습용. 위패스 마이 정리(민법총칙+물권법) + 핵심요약서.\n\n---\n']
압축.append('## 📘 위패스 마이 — 민법총칙\n')
if '민법총칙' in jung_text:
    압축.append(jung_text['민법총칙'])
압축.append('\n\n---\n## 📘 위패스 마이 — 물권법\n')
if '물권법' in jung_text:
    압축.append(jung_text['물권법'])
압축_path.write_text('\n'.join(압축), encoding='utf-8')
print(f'  OK  🏃_시험직전_압축.md  {압축_path.stat().st_size/1024:.0f}KB')

# 7-4) 원본 정리 파일 복사
print('  📑 원본 정리 파일 복사...')
for area, fname in JUNG_MD.items():
    src = BASE / fname
    if src.exists():
        shutil.copy(src, OUT / f'참조_{fname}')
# 목차도 복사
for fname in ['민법총칙_목차.md', '물권법_목차.md']:
    src = BASE / fname
    if src.exists():
        shutil.copy(src, OUT / f'참조_{fname}')

print('\n=== 완료 ===')
print(f'위치: {OUT}')
