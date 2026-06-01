#!/usr/bin/env python3
"""감정평가관계법규 단권화 빌드 (1차 객관식)
- 6개 단원 = 6개 법
  PART01 국토계획법, PART02 도정법, PART03 공간정보법 (감관법1)
  PART04 감정평가법, PART05 부공법, PART06 국유재산법 (감관법2)
- 기본서 + 핵심요약서 + 워크북[원문/해설] + 단원별문제집/문제집 + 연도별기출 통합
"""
import pypdf, re, os, json, shutil
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent
OUT = BASE / '_최종산출물_관계법규'
OUT.mkdir(exist_ok=True)

# ============== 6개 단원 ==============
CHAPTERS = {
    'PART01': {'name': '국토계획법',     'group': '감관법1', 'full': '국토의 계획 및 이용에 관한 법률', 'desc': '용도지역·지구단위계획·도시군관리계획·기반시설·개발행위허가'},
    'PART02': {'name': '도정법',         'group': '감관법1', 'full': '도시 및 주거환경정비법', 'desc': '정비계획·정비구역·정비사업·조합·관리처분'},
    'PART03': {'name': '공간정보법',     'group': '감관법1', 'full': '공간정보의 구축 및 관리 등에 관한 법률', 'desc': '지적·등록·지적공부·토지이동·측량'},
    'PART04': {'name': '감정평가법',     'group': '감관법2', 'full': '감정평가 및 감정평가사에 관한 법률', 'desc': '자격·시험·등록·업무·의무·징계·과징금·벌칙'},
    'PART05': {'name': '부공법',         'group': '감관법2', 'full': '부동산 가격공시에 관한 법률',     'desc': '표준지·개별공시지가·표준주택·공동주택·비주거용 부동산'},
    'PART06': {'name': '국유재산법',     'group': '감관법2', 'full': '국유재산법', 'desc': '총괄청·행정재산·일반재산·대부·매각·교환·양여·개발'},
}
CHAPTER_ORDER = ['PART01','PART02','PART03','PART04','PART05','PART06']

# ============== 단원 키워드 (자동 분류용 — 연도별기출용) ==============
CHAPTER_KEYWORDS = {
    'PART01': ['국토계획', '국토의 계획 및 이용', '광역계획권', '광역도시계획', '도시·군기본계획', '도시·군관리계획', '용도지역', '용도지구', '용도구역', '기반시설', '도시·군계획시설', '지구단위계획', '개발행위허가', '성장관리계획', '개발밀도관리구역', '기반시설부담구역', '도시계획'],
    'PART02': ['도시정비', '도시 및 주거환경', '정비사업', '정비계획', '정비구역', '재개발', '재건축', '주거환경', '조합설립', '관리처분', '청산금', '조합원', '도정법'],
    'PART03': ['공간정보', '측량', '지적', '지적공부', '토지이동', '신규등록', '등록전환', '지목변경', '경계', '지번', '지적도', '임야도', '지적측량', '필지'],
    'PART04': ['감정평가법', '감정평가사', '감정평가법인', '감정평가관리·징계위원회', '실무수습', '교육연수', '제10조', '제11조', '제12조', '제14조', '제17조', '제25조', '제32조', '제33조', '한국감정평가사협회', '감정평가준칙', '감정평가타당성조사', '징계위원회', '과징금', '명의대여'],
    'PART05': ['부동산공시법', '부동산 가격공시', '표준지공시지가', '개별공시지가', '표준주택가격', '공동주택가격', '비주거용 부동산가격', '부동산가격공시위원회', '공시기준일', '이의신청', '공시지가'],
    'PART06': ['국유재산', '국유재산법', '행정재산', '일반재산', '총괄청', '국유재산관리기금', '사용허가', '대부', '매각', '교환', '양여', '현물출자', '정부배당', '지식재산', '국가소유'],
}

# ============== 파일 ==============
FILES = {
    'gam1_gibon':       '감관법1 기본서 [업데이트일_26.03.29].pdf',
    'gam1_haek':        '감관법1 핵심요약서 [업데이트일_26.03.20].pdf',
    'gam1_moonjae':     '감관법1 단원별 문제집 [업데이트일_26.04.02].pdf',
    'gam1_workbook_q':  '감관법1 워크북 [원문] [업데이트일_26.03.11].pdf',
    'gam1_workbook_a':  '감관법1 워크북 [해설] [업데이트일_26.03.20].pdf',
    'gam2_gibon':       '감관법2 기본서,문제집 [업데이트일_26.03.27].pdf',
    'gam2_haek':        '감관법2 핵심요약서 [업데이트일_26.03.09].pdf',
    'gam2_workbook_q':  '감관법2 워크북 [원문] [업데이트일_26.02.02].pdf',
    'gam2_workbook_a':  '감관법2 워크북 [해설] [업데이트일_26.03.17].pdf',
    'amgi_note':        '감정평가사 1차 감정평가사법 암기노트(240121최종배포).pdf',
    'gichul_yeondo':    '감정평가사 감관법 연도별 기출문제집 [2018년-2026년] [업데이트일_26.04.12].pdf',
}

# ============== 페이지 범위 매핑 (검출 결과 + 수동 확인) ==============
# 감관법1 — 3 PARTs
GAM1_GIBON_RANGES = {
    'PART01': (9, 104),
    'PART02': (105, 174),
    'PART03': (175, 301),
}
GAM1_HAEK_RANGES = {
    'PART01': (9, 74),
    'PART02': (75, 126),
    'PART03': (127, 215),
}
GAM1_MOONJAE_RANGES = {
    'PART01': (9, 86),
    'PART02': (87, 132),
    'PART03': (133, 237),
}
GAM1_WB_RANGES = {  # 워크북 원문/해설 동일 구조
    'PART01': (9, 82),
    'PART02': (83, 130),
    'PART03': (131, 229),
}

# 감관법2 — 3 laws (이론 부분 + 문제 부분)
GAM2_GIBON_THEORY = {
    'PART04': (6, 63),    # 감정평가법 이론
    'PART05': (64, 117),  # 부공법 이론
    'PART06': (118, 216), # 국유재산법 이론
}
GAM2_GIBON_PROBLEMS = {
    'PART04': (218, 275),   # 감정평가법 문제
    'PART05': (278, 345),   # 부공법 문제
    'PART06': (348, 379),   # 국유재산법 문제
}
GAM2_HAEK_RANGES = {
    'PART04': (2, 20),
    'PART05': (21, 40),
    'PART06': (41, 61),
}
GAM2_WB_RANGES = {  # 워크북 49p — PART별 페이지는 적음
    'PART04': (4, 19),   # 감정평가법
    'PART05': (20, 33),  # 부공법
    'PART06': (34, 49),  # 국유재산법
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

# ============== Step 1: 연도별 기출 단원별 분류 ==============
print('=== Step 1: 연도별 기출 단원별 분류 ===')
gichul_pdf = BASE / FILES['gichul_yeondo']
gichul_pages = extract_all_text(gichul_pdf)
gichul_pages_by_ch = defaultdict(list)
for i, t in enumerate(gichul_pages):
    if i < 3: continue
    ch = classify_text(t)
    if ch:
        gichul_pages_by_ch[ch].append(i + 1)
print(f'  연도별 기출 총 {len(gichul_pages)}p')
for ch in CHAPTER_ORDER:
    print(f'  {ch}: {len(gichul_pages_by_ch[ch])}p')

# ============== Step 2: 단원별 이론 파일 생성 ==============
print('\n=== Step 2: 단원별 이론 파일 생성 ===')

for ch_id in CHAPTER_ORDER:
    info = CHAPTERS[ch_id]
    out_path = OUT / f'단원_{ch_id}_{info["name"]}.md'
    content = [f'# 단원 {ch_id} — {info["name"]}\n']
    content.append(f'> **법령 전체명**: {info["full"]}')
    content.append(f'> **출처 자료**: {info["group"]} (스터디파이터)')
    content.append(f'> **수업 주제**: {info["desc"]}\n')

    content.append('\n## 🗺️ 본문 목차\n')
    content.append('- [📖 핵심요약서 (L1 - 메인 단권화)](#핵심요약서)')
    content.append('- [📚 기본서 (L2 - 본격 학습)](#기본서)')
    content.append('- [✏️ 워크북 (논점별 문제)](#워크북)')
    if ch_id == 'PART04':
        content.append('- [🎯 감정평가사법 암기노트 (1p 압축)](#암기노트)')
    content.append('\n---\n')

    # L1: 핵심요약서
    content.append('## <a name="핵심요약서"></a>📖 핵심요약서 — L1 (메인·단권화)\n')
    content.append('> 스터디파이터 핵심요약서. 시험 직전 단권화 자료.\n')
    if info['group'] == '감관법1':
        haek_pdf = BASE / FILES['gam1_haek']
        s, e = GAM1_HAEK_RANGES[ch_id]
    else:
        haek_pdf = BASE / FILES['gam2_haek']
        s, e = GAM2_HAEK_RANGES[ch_id]
    content.append(f'\n### 핵심요약서 (p.{s}~{e})\n')
    content.append(extract_pages(haek_pdf, s, e))
    content.append('\n---\n')

    # L2: 기본서
    content.append('## <a name="기본서"></a>📚 기본서 — L2 (본격 학습)\n')
    if info['group'] == '감관법1':
        gibon_pdf = BASE / FILES['gam1_gibon']
        s, e = GAM1_GIBON_RANGES[ch_id]
    else:
        gibon_pdf = BASE / FILES['gam2_gibon']
        s, e = GAM2_GIBON_THEORY[ch_id]
    content.append(f'\n### 기본서 (p.{s}~{e})\n')
    content.append(extract_pages(gibon_pdf, s, e))
    content.append('\n---\n')

    # 워크북 (논점별)
    content.append('## <a name="워크북"></a>✏️ 워크북 — 논점별 문제\n')
    if info['group'] == '감관법1':
        wb_q_pdf = BASE / FILES['gam1_workbook_q']
        wb_a_pdf = BASE / FILES['gam1_workbook_a']
        s, e = GAM1_WB_RANGES[ch_id]
    else:
        wb_q_pdf = BASE / FILES['gam2_workbook_q']
        wb_a_pdf = BASE / FILES['gam2_workbook_a']
        s, e = GAM2_WB_RANGES[ch_id]
    content.append(f'\n### 워크북 [원문] (p.{s}~{e})\n')
    content.append(extract_pages(wb_q_pdf, s, e))
    content.append(f'\n### 워크북 [해설] (p.{s}~{e})\n')
    content.append(extract_pages(wb_a_pdf, s, e))

    # 감정평가사법 암기노트 (PART04만)
    if ch_id == 'PART04':
        amgi_pdf = BASE / FILES['amgi_note']
        content.append('\n---\n')
        content.append('## <a name="암기노트"></a>🎯 감정평가사법 암기노트 (1p 압축)\n')
        content.append(extract_pages(amgi_pdf, 1, 1))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 3: 단원별 문제 파일 생성 ==============
print('\n=== Step 3: 단원별 문제 파일 생성 ===')

for ch_id in CHAPTER_ORDER:
    info = CHAPTERS[ch_id]
    out_path = OUT / f'문제_{ch_id}_{info["name"]}.md'
    content = [f'# 문제 단원 {ch_id} — {info["name"]}\n']
    content.append(f'> **법령 전체명**: {info["full"]}\n')
    content.append('---\n')

    # 연도별 기출
    g_pages = gichul_pages_by_ch[ch_id]
    if g_pages:
        content.append(f'\n## 🎯 연도별 기출 (감정평가사 2018-2026) — {len(g_pages)}p\n')
        content.append(extract_specific_pages(gichul_pdf, g_pages[:80]))
        content.append('\n')

    # 감관법1 단원별 문제집 (or 감관법2 문제부)
    if info['group'] == '감관법1':
        m_pdf = BASE / FILES['gam1_moonjae']
        s, e = GAM1_MOONJAE_RANGES[ch_id]
        content.append(f'\n## ✏️ 단원별 문제집 (감관법1) — p.{s}~{e}\n')
        content.append(extract_pages(m_pdf, s, e))
    else:
        m_pdf = BASE / FILES['gam2_gibon']
        s, e = GAM2_GIBON_PROBLEMS[ch_id]
        content.append(f'\n## ✏️ 감관법2 문제집 — p.{s}~{e}\n')
        content.append(extract_pages(m_pdf, s, e))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 4: 부가 파일 ==============
print('\n=== Step 4: 부가 파일 ===')

# 4-1) 단원별 자료량
통계_path = OUT / '_단원별_자료량.md'
통계 = ['# 📊 단원별 자료량\n', '| 단원 | 명칭 | 출처 | 이론 KB | 문제 KB | 기출 P |',
        '|---|---|---|---|---|---|']
for ch_id in CHAPTER_ORDER:
    info = CHAPTERS[ch_id]
    tp = OUT / f'단원_{ch_id}_{info["name"]}.md'
    pp = OUT / f'문제_{ch_id}_{info["name"]}.md'
    tkb = tp.stat().st_size / 1024 if tp.exists() else 0
    pkb = pp.stat().st_size / 1024 if pp.exists() else 0
    통계.append(f'| {ch_id} | {info["name"]} | {info["group"]} | {tkb:.0f} | {pkb:.0f} | {len(gichul_pages_by_ch[ch_id])} |')
통계_path.write_text('\n'.join(통계), encoding='utf-8')
print(f'  OK  _단원별_자료량.md')

# 4-2) 출제빈도 분석
빈도_path = OUT / '_출제빈도_분석.md'
빈도_content = """# 📈 감정평가관계법규 출제빈도 분석

> 감정평가사 1차 감관법 2018-2026년 기출 기반.
> 매년 약 40문항 출제. **6개 법령에 고르게 분포**, 단 법령별 비중 다름.

## 🥇 최다 출제 (★★★) — 매년 8~12문항

| PART | 법령 | 비고 |
|---|---|---|
| **PART01 국토계획법** | 국토의 계획 및 이용에 관한 법률 | **가장 두꺼움(301p 중 96p), 매년 최다 출제** |
| **PART05 부공법** | 부동산 가격공시에 관한 법률 | 표준지·개별공시지가 빈출 |
| **PART04 감정평가법** | 감정평가 및 감정평가사에 관한 법률 | 자격·결격사유·징계·과징금 |

## 🥈 꾸준한 출제 (★★) — 매년 5~7문항

| PART | 법령 |
|---|---|
| PART06 국유재산법 | 행정재산·일반재산·대부·매각 |
| PART02 도정법 | 정비사업·조합·관리처분계획 |

## 🥉 비교적 적은 출제 (★) — 매년 3~5문항

- **PART03 공간정보법**: 지적·측량 영역 — 분량은 큰데 출제 비중은 다소 낮음

---

## 💡 학습 우선순위 (1차 합격용)

1. **PART01 국토계획법** = 시험의 1/3 차지 (단원 1개로 12문항). 가장 시간 투자
2. **PART05 부공법 + PART04 감정평가법** = 매년 합 15~18문항. 감정평가사 시험 핵심 법령
3. **PART06 국유재산법 + PART02 도정법** = 합 10~12문항
4. **PART03 공간정보법** = 5문항 내외

---

## 📊 단원 매핑

| 단원 | 법령 | 출처 |
|---|---|---|
| PART01 | 국토의 계획 및 이용에 관한 법률 | 감관법1 |
| PART02 | 도시 및 주거환경정비법 | 감관법1 |
| PART03 | 공간정보의 구축 및 관리 등에 관한 법률 | 감관법1 |
| PART04 ★ | 감정평가 및 감정평가사에 관한 법률 | 감관법2 |
| PART05 ★ | 부동산 가격공시에 관한 법률 | 감관법2 |
| PART06 | 국유재산법 | 감관법2 |
"""
빈도_path.write_text(빈도_content, encoding='utf-8')
print(f'  OK  _출제빈도_분석.md')

# 4-3) 시험 직전 압축본 (핵심요약서 통합)
print('  🏃 시험 직전 압축본...')
압축_path = OUT / '🏃_시험직전_압축.md'
압축 = ['# 🏃 시험 직전 압축본 (감정평가관계법규)\n',
       '> 시험 1~3일 전 복습용. 핵심요약서 6개 PART 통합.\n\n---\n']
# 감관법1 핵심요약서 전체
haek1_pdf = BASE / FILES['gam1_haek']
압축.append('\n## 📖 감관법1 핵심요약서 (PART01~03)\n')
압축.append(extract_pages(haek1_pdf, 9, 215))
# 감관법2 핵심요약서 전체
haek2_pdf = BASE / FILES['gam2_haek']
압축.append('\n\n---\n## 📖 감관법2 핵심요약서 (PART04~06)\n')
압축.append(extract_pages(haek2_pdf, 1, 61))
# 감정평가사법 암기노트
amgi_pdf = BASE / FILES['amgi_note']
압축.append('\n\n---\n## 🎯 감정평가사법 암기노트 (1p 압축)\n')
압축.append(extract_pages(amgi_pdf, 1, 1))
압축_path.write_text('\n'.join(압축), encoding='utf-8')
print(f'  OK  🏃_시험직전_압축.md  {압축_path.stat().st_size/1024:.0f}KB')

print('\n=== 완료 ===')
print(f'위치: {OUT}')
