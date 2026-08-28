#!/usr/bin/env python3
"""회계학 단권화 빌드 (1차 객관식)
- 황윤하 MD 메인 (재무 25장 + 원가 17장 = 42장)
- 12개 단원으로 그룹핑 (재무 8 + 원가 4)
- 기본서/문제집/기출 페이지별 키워드 분류
"""
import pypdf, re, os, shutil
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent
OUT = BASE / '_최종산출물_회계학'
OUT.mkdir(exist_ok=True)

# ============== 12개 단원 ==============
# 재무회계 F01~F08, 원가회계 C01~C04
CHAPTERS = {
    'F01': {'name': '재고자산',
            'area': '재무회계',
            'hwang_chapters': [1],
            'desc': '재고자산 인식·측정·평가·매출원가'},
    'F02': {'name': '유형자산·투자부동산·무형자산·차입원가',
            'area': '재무회계',
            'hwang_chapters': [2,3,4,5],
            'desc': '유형자산 취득·감가상각·재평가, 투자부동산, 무형자산, 차입원가자본화'},
    'F03': {'name': '금융부채·자본·충당부채',
            'area': '재무회계',
            'hwang_chapters': [6,7,8],
            'desc': '사채·금융부채·자본·충당부채·보고기간후사건'},
    'F04': {'name': '개념체계·재무제표·공정가치',
            'area': '재무회계',
            'hwang_chapters': [9,10,11],
            'desc': '재무보고 개념체계·재무제표 표시·공정가치 측정'},
    'F05': {'name': '금융자산·복합금융상품·주식기준보상',
            'area': '재무회계',
            'hwang_chapters': [12,13,14],
            'desc': '금융자산 분류·평가·복합금융상품(전환사채)·주식기준보상'},
    'F06': {'name': '종업원급여·리스·법인세',
            'area': '재무회계',
            'hwang_chapters': [15,16,17],
            'desc': '종업원급여·리스(IFRS 16)·법인세회계'},
    'F07': {'name': '회계변경·주당이익·현금흐름표·기타',
            'area': '재무회계',
            'hwang_chapters': [18,19,20,21],
            'desc': '회계변경·오류수정·주당이익·현금흐름표·재무회계 기타'},
    'F08': {'name': '수익·사업결합·지분법·환율변동',
            'area': '재무회계',
            'hwang_chapters': [22,23,24,25],
            'desc': '고객과의 계약에서 생기는 수익·사업결합·지분법·환율변동(외화환산)'},
    'C01': {'name': '원가의_흐름·보조부문·개별·종합·공손',
            'area': '원가회계',
            'hwang_chapters': [1,2,3,4,5],
            'desc': '원가의 흐름·보조부문 배분·개별원가·종합원가·공손'},
    'C02': {'name': '결합원가·변동원가·활동기준',
            'area': '원가회계',
            'hwang_chapters': [6,7,8],
            'desc': '결합원가·변동원가/초변동원가·활동기준원가계산(ABC)'},
    'C03': {'name': '원가추정·CVP·관련원가·불확실성·종합예산',
            'area': '원가회계',
            'hwang_chapters': [9,10,11,12,13],
            'desc': '원가추정·CVP분석·관련원가분석·불확실성하 의사결정·종합예산'},
    'C04': {'name': '표준원가·투자중심점·대체가격·생산관리',
            'area': '원가회계',
            'hwang_chapters': [14,15,16,17],
            'desc': '표준원가계산·투자중심점·대체가격결정·생산관리이론'},
}
CHAPTER_ORDER = ['F01','F02','F03','F04','F05','F06','F07','F08','C01','C02','C03','C04']

# ============== 단원 키워드 (자동 분류용) ==============
CHAPTER_KEYWORDS = {
    'F01': ['재고자산', '매출원가', '기말재고', '기초재고', '당기매입', '실지재고조사법', '계속기록법', '저가법', '소매재고법', '매출총이익률법', '선입선출', '평균법', '이동평균', '순실현가능가치', 'NRV', '운송중상품', '시송품', '미착상품'],
    'F02': ['유형자산', '감가상각', '정액법', '정률법', '연수합계법', '생산량비례법', '취득원가', '재평가모형', '원가모형', '손상차손', '유형자산 처분', '투자부동산', '무형자산', '연구비', '개발비', '내용연수', '잔존가치', '차입원가', '자본화', '적격자산'],
    'F03': ['금융부채', '사채', '사채할인발행차금', '사채할증발행차금', '유효이자율', '액면이자율', '시장이자율', '자본', '주식발행', '자기주식', '이익잉여금', '자본잉여금', '주식분할', '주식배당', '자본금', '충당부채', '우발부채', '보고기간후사건'],
    'F04': ['개념체계', '재무보고', '재무제표의 목적', '재무제표 표시', '재무상태표', '포괄손익계산서', '자본변동표', '주석', '계속기업', '발생주의', '공정가치', '공정가치 측정', '시장 접근법', '원가 접근법', '소득 접근법', 'IFRS 13'],
    'F05': ['금융자산', 'FVPL', 'FVOCI', '상각후원가', '대손충당금', '신용손실', '기대신용손실', '유가증권', '복합금융상품', '전환사채', '신주인수권부사채', '주식기준보상', '주식결제형', '현금결제형', '가득기간', '부여일'],
    'F06': ['종업원급여', '확정급여제도', '확정기여제도', '퇴직급여', '리스', 'IFRS 16', '사용권자산', '리스부채', '운용리스', '금융리스', '법인세', '이연법인세', '일시적차이', '영구적차이', '법인세회계'],
    'F07': ['회계변경', '회계정책 변경', '회계추정 변경', '오류수정', '주당이익', '기본주당이익', '희석주당이익', 'EPS', '현금흐름표', '영업활동현금흐름', '투자활동현금흐름', '재무활동현금흐름', '간접법', '직접법'],
    'F08': ['고객과의 계약', '수익', '수익인식', '거래가격', '5단계 모형', '수행의무', '진행기준', '한 시점', '기간 인식', '사업결합', '취득법', '영업권', 'goodwill', '지분법', '관계기업', '공동기업', '환율변동', '외화환산', '해외사업장', '기능통화', '표시통화'],
    'C01': ['원가의 분류', '제조원가', '직접재료비', '직접노무비', '제조간접비', '재공품', '제품', '원가의 흐름', '보조부문원가', '직접배분법', '단계배분법', '상호배분법', '개별원가계산', '작업원가표', '예정배부율', '종합원가계산', '평균법', '선입선출법', '완성품환산량', '공손', '정상공손', '비정상공손', '재작업'],
    'C02': ['결합원가', '결합제품', '부산물', '분리점', '판매가치법', '순실현가치법', '균등이익률법', '변동원가계산', '초변동원가계산', '전부원가계산', '활동기준원가계산', 'ABC', '활동중심', '원가동인', '자원동인'],
    'C03': ['원가추정', '고저점법', '회귀분석', 'CVP', '공헌이익', '손익분기점', 'BEP', '안전한계', '영업레버리지', '관련원가', '비관련원가', '매몰원가', '특별주문', '부품을 자가제조', '외부구입', '의사결정', '불확실성', '기대가치', '완전정보', '종합예산', '판매예산', '제조예산', '현금예산'],
    'C04': ['표준원가', '차이분석', '재료차이', '가격차이', '능률차이', '수량차이', '제조간접원가차이', '예산차이', '조업도차이', '능률차이', '투자중심점', 'ROI', '잔여이익', 'RI', 'EVA', '대체가격', '대체가격결정', '생산관리이론', 'JIT', 'TOC', '제약이론'],
}

# ============== 파일 ==============
FILES = {
    'gibon_jaemu':      '재무회계 기본서 [공통] [업데이트일_26.03.20].pdf',
    'gibon_wonga':      '원가회계 기본서 [업데이트일_26.03.09].pdf',
    'gibon_hoegye':     '회계원리_기본서 [업데이트일_250825].pdf',
    'moonjae_jaemu1':   '재무회계1 기본문제집 [업데이트일_26.03.17].pdf',
    'moonjae_jaemu2':   '재무회계2 기본문제집 [업데이트일_26.03.14].pdf',
    'simhwa_jaemu1':    '재무회계1 심화문제집 [업데이트일_26.04.02].pdf',
    'simhwa_wonga':     '원가회계 심화문제집 [업데이트일_26.04.03].pdf',
    'jabon_haek':       '재무회계1 제15장 자본파트 핵심요약자료 [업데이트일_240926].pdf',
    'gyejung_jung':     '회계학_중요계정과목정리 [업데이트일_250412].pdf',
    'gichul_yeondo':    '감정평가사 회계학 연도별 기출문제집 [2018년-2025년] [업데이트일_26.05.06].pdf',
}
HWANG_MD = {
    '재무회계': '황윤하_재무회계.md',
    '원가회계': '황윤하_원가회계.md',
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

def classify_text(text, restrict_area=None):
    """단원 분류. restrict_area='재무회계'면 F만, '원가회계'면 C만 고려"""
    body = text[100:] if len(text) > 100 else text
    scores = {}
    for ch, kws in CHAPTER_KEYWORDS.items():
        if restrict_area == '재무회계' and not ch.startswith('F'):
            continue
        if restrict_area == '원가회계' and not ch.startswith('C'):
            continue
        scores[ch] = sum(body.count(k) for k in kws)
    if not scores or not any(scores.values()):
        return None
    return max(scores, key=scores.get)

# ============== Step 1: 황윤하 MD 챕터 분할 ==============
print('=== Step 1: 황윤하 MD 챕터 분할 ===')
hwang_chapters = {'재무회계': {}, '원가회계': {}}
for area, fname in HWANG_MD.items():
    txt = (BASE / fname).read_text(encoding='utf-8')
    pattern = re.compile(r'^## Chapter (\d+)\.', re.MULTILINE)
    matches = list(pattern.finditer(txt))
    for i, m in enumerate(matches):
        ch_no = int(m.group(1))
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(txt)
        hwang_chapters[area][ch_no] = txt[start:end]
    print(f'  {area}: {len(hwang_chapters[area])}챕터')

# ============== Step 2: 기본서/문제집/기출 페이지 키워드 분류 ==============
print('\n=== Step 2: PDF 페이지 단원별 분류 ===')

# 2-1) 재무회계 기본서
gibon_jaemu = BASE / FILES['gibon_jaemu']
gibon_jaemu_pages = extract_all_text(gibon_jaemu)
gibon_jaemu_by_ch = defaultdict(list)
for i, t in enumerate(gibon_jaemu_pages):
    if i < 6: continue
    ch = classify_text(t, restrict_area='재무회계')
    if ch:
        gibon_jaemu_by_ch[ch].append(i + 1)
print(f'  재무회계 기본서 {len(gibon_jaemu_pages)}p')
for ch in CHAPTER_ORDER:
    if ch.startswith('F'):
        print(f'    {ch}: {len(gibon_jaemu_by_ch[ch])}p')

# 2-2) 원가회계 기본서
gibon_wonga = BASE / FILES['gibon_wonga']
gibon_wonga_pages = extract_all_text(gibon_wonga)
gibon_wonga_by_ch = defaultdict(list)
for i, t in enumerate(gibon_wonga_pages):
    if i < 6: continue
    ch = classify_text(t, restrict_area='원가회계')
    if ch:
        gibon_wonga_by_ch[ch].append(i + 1)
print(f'  원가회계 기본서 {len(gibon_wonga_pages)}p')
for ch in CHAPTER_ORDER:
    if ch.startswith('C'):
        print(f'    {ch}: {len(gibon_wonga_by_ch[ch])}p')

# 2-3) 재무회계1·2 기본문제집 + 재무회계1 심화
moonjae_jaemu1 = BASE / FILES['moonjae_jaemu1']
moonjae_jaemu2 = BASE / FILES['moonjae_jaemu2']
simhwa_jaemu1 = BASE / FILES['simhwa_jaemu1']
def classify_pdf(p, area=None):
    pages = extract_all_text(p)
    result = defaultdict(list)
    for i, t in enumerate(pages):
        if i < 3: continue
        ch = classify_text(t, restrict_area=area)
        if ch:
            result[ch].append(i + 1)
    return result, len(pages)

moonjae_jaemu1_by_ch, m1_total = classify_pdf(moonjae_jaemu1, '재무회계')
moonjae_jaemu2_by_ch, m2_total = classify_pdf(moonjae_jaemu2, '재무회계')
simhwa_jaemu1_by_ch, sj1_total = classify_pdf(simhwa_jaemu1, '재무회계')
print(f'  재무1 기본문제집 {m1_total}p, 재무2 기본문제집 {m2_total}p, 재무1 심화 {sj1_total}p')

# 2-4) 원가회계 심화
simhwa_wonga = BASE / FILES['simhwa_wonga']
simhwa_wonga_by_ch, sw_total = classify_pdf(simhwa_wonga, '원가회계')
print(f'  원가 심화 {sw_total}p')

# 2-5) 연도별 기출
gichul_pdf = BASE / FILES['gichul_yeondo']
gichul_by_ch, gichul_total = classify_pdf(gichul_pdf)
print(f'  연도별 기출 {gichul_total}p')
for ch in CHAPTER_ORDER:
    print(f'    {ch}: {len(gichul_by_ch[ch])}p')

# ============== Step 3: 단원별 이론 파일 생성 ==============
print('\n=== Step 3: 단원별 이론 파일 생성 ===')

for ch_id in CHAPTER_ORDER:
    info = CHAPTERS[ch_id]
    out_path = OUT / f'단원_{ch_id}_{info["name"]}.md'
    content = [f'# 단원 {ch_id} — {info["name"].replace("_"," ")}\n']
    content.append(f'> **영역**: {info["area"]}')
    content.append(f'> **황윤하 교재 챕터**: Ch.{info["hwang_chapters"]}')
    content.append(f'> **수업 주제**: {info["desc"]}\n')

    content.append('\n## 🗺️ 본문 목차\n')
    content.append('- [📕 황윤하 교재 (L1 - 메인)](#황윤하)')
    content.append('- [📚 기본서 (L2 - 본격 학습·보강)](#기본서)')
    content.append('\n---\n')

    # L1: 황윤하 MD
    content.append('## <a name="황윤하"></a>📕 황윤하 교재 — L1 (메인)\n')
    content.append('> 황윤하 회계학 교재(재무회계 25장 + 원가회계 17장) 마크다운 본문. 본 단원에 해당하는 챕터 모두 포함.\n')
    hwang_dict = hwang_chapters[info['area']]
    for ch_no in info['hwang_chapters']:
        if ch_no in hwang_dict:
            content.append(f'\n### 황윤하 — Chapter {ch_no:02d}\n')
            content.append(hwang_dict[ch_no])
    content.append('\n---\n')

    # L2: 기본서 발췌 (키워드 분류)
    content.append('## <a name="기본서"></a>📚 기본서 — L2 (본격 학습·보강)\n')
    if info['area'] == '재무회계':
        content.append('> 재무회계 기본서[공통] 발췌 (키워드 자동 분류).\n')
        g_pages = gibon_jaemu_by_ch[ch_id]
        if g_pages:
            content.append(f'\n### 기본서 발췌 (총 {len(g_pages)}p)\n')
            content.append(extract_specific_pages(gibon_jaemu, g_pages[:80]))
    else:
        content.append('> 원가회계 기본서 발췌 (키워드 자동 분류).\n')
        g_pages = gibon_wonga_by_ch[ch_id]
        if g_pages:
            content.append(f'\n### 기본서 발췌 (총 {len(g_pages)}p)\n')
            content.append(extract_specific_pages(gibon_wonga, g_pages[:80]))

    # 자본파트 핵심요약 (F03만 — Ch.7 자본 포함)
    if ch_id == 'F03':
        jabon_pdf = BASE / FILES['jabon_haek']
        content.append('\n---\n')
        content.append('## 🎯 자본파트 핵심요약자료 (재무회계1 제15장)\n')
        content.append(extract_pages(jabon_pdf, 1, 999))

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 4: 단원별 문제 파일 생성 ==============
print('\n=== Step 4: 단원별 문제 파일 생성 ===')

for ch_id in CHAPTER_ORDER:
    info = CHAPTERS[ch_id]
    out_path = OUT / f'문제_{ch_id}_{info["name"]}.md'
    content = [f'# 문제 단원 {ch_id} — {info["name"].replace("_"," ")}\n']
    content.append(f'> **영역**: {info["area"]}\n')
    content.append('---\n')

    # 연도별 기출
    g_pages = gichul_by_ch[ch_id]
    if g_pages:
        content.append(f'\n## 🎯 연도별 기출 (감정평가사 2018-2025) — {len(g_pages)}p\n')
        content.append(extract_specific_pages(gichul_pdf, g_pages[:80]))
        content.append('\n')

    if info['area'] == '재무회계':
        # 재무1 기본 + 재무2 기본 + 재무1 심화
        for pdf_path, label, src_by_ch in [
            (moonjae_jaemu1, '재무회계1 기본문제집', moonjae_jaemu1_by_ch),
            (moonjae_jaemu2, '재무회계2 기본문제집', moonjae_jaemu2_by_ch),
            (simhwa_jaemu1, '재무회계1 심화문제집', simhwa_jaemu1_by_ch),
        ]:
            pgs = src_by_ch[ch_id]
            if pgs:
                content.append(f'\n## ✏️ {label} — {len(pgs)}p\n')
                content.append(extract_specific_pages(pdf_path, pgs[:60]))
                content.append('\n')
    else:
        # 원가 심화문제집
        pgs = simhwa_wonga_by_ch[ch_id]
        if pgs:
            content.append(f'\n## ✏️ 원가회계 심화문제집 — {len(pgs)}p\n')
            content.append(extract_specific_pages(simhwa_wonga, pgs[:60]))
            content.append('\n')

    out_path.write_text('\n'.join(content), encoding='utf-8')
    kb = out_path.stat().st_size / 1024
    print(f'  OK  {out_path.name}  {kb:.0f}KB')

# ============== Step 5: 부가 파일 ==============
print('\n=== Step 5: 부가 파일 ===')

# 5-1) 단원별 자료량
통계_path = OUT / '_단원별_자료량.md'
통계 = ['# 📊 단원별 자료량\n', '| 단원 | 영역 | 이론 KB | 문제 KB | 기출 P |',
        '|---|---|---|---|---|']
for ch_id in CHAPTER_ORDER:
    info = CHAPTERS[ch_id]
    tp = OUT / f'단원_{ch_id}_{info["name"]}.md'
    pp = OUT / f'문제_{ch_id}_{info["name"]}.md'
    tkb = tp.stat().st_size / 1024 if tp.exists() else 0
    pkb = pp.stat().st_size / 1024 if pp.exists() else 0
    통계.append(f'| {ch_id} | {info["area"]} | {tkb:.0f} | {pkb:.0f} | {len(gichul_by_ch[ch_id])} |')
통계_path.write_text('\n'.join(통계), encoding='utf-8')
print(f'  OK  _단원별_자료량.md')

# 5-2) 출제빈도 분석
빈도_path = OUT / '_출제빈도_분석.md'
빈도_content = """# 📈 회계학 출제빈도 분석

> 감정평가사 1차 회계학 2018-2025년 기출 기반.
> 매년 약 40문항 출제 — **재무회계 + 원가회계 통합**.
> 황윤하 교재 절별 "필수/권장/선택" 라벨 기준 정리.

## 🥇 최다 출제 (★★★)

| 단원 | 영역 | 핵심 빈출 |
|---|---|---|
| **F01 재고자산** | 재무회계 | 매출원가·저가법·소매재고법 |
| **F02 유형자산·투자부동산** | 재무회계 | 감가상각·재평가·손상 |
| **F05 금융자산·복합금융상품** | 재무회계 | FVPL/FVOCI·전환사채 |
| **F08 수익·사업결합·지분법** | 재무회계 | 5단계 모형·영업권·지분법 |
| **C01 원가의 흐름·종합원가** | 원가회계 | 완성품환산량·평균법/선입선출 |
| **C03 CVP·관련원가·종합예산** | 원가회계 | BEP·공헌이익·특별주문 |

## 🥈 꾸준한 출제 (★★)

| 단원 | 영역 |
|---|---|
| F03 금융부채·자본 | 재무회계 (사채·자기주식) |
| F06 리스·법인세 | 재무회계 (IFRS 16·이연법인세) |
| F07 현금흐름표 | 재무회계 (간접법 빈출) |
| C04 표준원가·투자중심점 | 원가회계 (차이분석·ROI) |

## 🥉 비교적 적은 출제 (★)

- F04 개념체계·재무제표·공정가치 (이론형)
- C02 결합원가·변동원가·ABC (계산 일부)

---

## 💡 학습 우선순위 (1차 합격용)

### 황윤하 교재 라벨 활용

황윤하 교재는 절별로 **필수/권장/선택** 라벨이 있습니다:
- **필수**: 면과락(40점) 목표 — 반드시 학습
- **권장**: 60점 안정적 득점
- **선택**: 고득점(70+) 목표

### 절대 우선순위 (재무 우선 / 원가 후순위)
1. **F01 재고자산 / F02 유형자산** — 매년 5~8문항 (재무 핵심)
2. **C01 원가의 흐름·종합원가** — 매년 4~6문항 (원가 기초)
3. **F05 금융자산 / F08 수익** — 매년 3~5문항씩
4. **C03 CVP·관련원가** — 매년 3~5문항
5. 나머지 단원 — 시간 남으면 권장 절까지

### 회계학 면과락 전략 (재무1 + 원가1만)
> "재무1 원가1만 가져가기로 결정"한 합격자 수기 참조
- **재무1**: F01, F02, F03, F04 (~Ch.10) 위주
- **원가1**: C01, C02 (~Ch.7) 위주
- 두 영역 필수 절만 완벽 학습 → 면과락 가능

---

## 📊 단원 매핑

| 단원 | 영역 | 황윤하 챕터 |
|---|---|---|
| F01 ★★★ | 재무회계 | Ch.01 재고자산 |
| F02 ★★★ | 재무회계 | Ch.02-05 유형자산·투자부동산·무형자산·차입원가 |
| F03 ★★ | 재무회계 | Ch.06-08 금융부채·자본·충당부채 |
| F04 ★ | 재무회계 | Ch.09-11 개념체계·재무제표·공정가치 |
| F05 ★★★ | 재무회계 | Ch.12-14 금융자산·복합금융·주식기준보상 |
| F06 ★★ | 재무회계 | Ch.15-17 종업원급여·리스·법인세 |
| F07 ★★ | 재무회계 | Ch.18-21 회계변경·EPS·CF표·기타 |
| F08 ★★★ | 재무회계 | Ch.22-25 수익·사업결합·지분법·환율변동 |
| C01 ★★★ | 원가회계 | Ch.01-05 원가의 흐름·보조부문·개별·종합·공손 |
| C02 ★ | 원가회계 | Ch.06-08 결합원가·변동원가·ABC |
| C03 ★★★ | 원가회계 | Ch.09-13 원가추정·CVP·관련원가·불확실성·종합예산 |
| C04 ★★ | 원가회계 | Ch.14-17 표준원가·투자중심점·대체가격·생산관리 |
"""
빈도_path.write_text(빈도_content, encoding='utf-8')
print(f'  OK  _출제빈도_분석.md')

# 5-3) 시험 직전 압축본 (황윤하 MD 전체 + 자본파트 핵심요약 + 중요계정과목정리)
print('  🏃 시험 직전 압축본...')
압축_path = OUT / '🏃_시험직전_압축.md'
압축 = ['# 🏃 시험 직전 압축본 (회계학)\n',
       '> 시험 1~3일 전 복습용. 황윤하 MD(재무+원가) + 자본파트 핵심요약 + 중요계정과목정리.\n\n---\n']
압축.append('## 📕 황윤하 재무회계 전체\n')
압축.append((BASE / HWANG_MD['재무회계']).read_text(encoding='utf-8'))
압축.append('\n\n---\n## 📗 황윤하 원가회계 전체\n')
압축.append((BASE / HWANG_MD['원가회계']).read_text(encoding='utf-8'))
압축.append('\n\n---\n## 🎯 자본파트 핵심요약 (재무회계1 제15장)\n')
압축.append(extract_pages(BASE / FILES['jabon_haek'], 1, 999))
압축.append('\n\n---\n## 📑 중요계정과목정리\n')
압축.append(extract_pages(BASE / FILES['gyejung_jung'], 1, 999))
압축_path.write_text('\n'.join(압축), encoding='utf-8')
print(f'  OK  🏃_시험직전_압축.md  {압축_path.stat().st_size/1024:.0f}KB')

# 5-4) 원본 MD 복사
print('  📑 원본 마크다운 복사...')
for area, fname in HWANG_MD.items():
    src = BASE / fname
    if src.exists():
        shutil.copy(src, OUT / f'참조_{fname}')

print('\n=== 완료 ===')
print(f'위치: {OUT}')
