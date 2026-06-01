#!/usr/bin/env python3
"""
1차 5과목 전체에 대해 ai_taxonomy_index.json 생성.

각 과목별로 taxonomy.json leaf 노드를 펼치고, 매핑 룰을 통해
교재 단원(또는 PART) MD 파일과 연결한다.
leaf_id는 '{subject_id}__{slugified_path}' 형태로 prefix 분리해 충돌 방지.
"""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAX = json.load(open(os.path.join(ROOT, 'viewer/public/data/taxonomy.json')))

# ── 과목 정의 ───────────────────────────────────────────────
# subject_id: app/data 경로
# tax_key: taxonomy.json 상의 top-level 키
# default_leaf_keyword: 첫 진입 시 default 후보 키워드(없으면 leaves[0])
# mapping: (regex, unit_code, section_key='full') tuples
SUBJECTS = {
    'civil': {
        'tax_key': '민법',
        'title': '민법',
        'mapping': [
            (r'제1장 민법 서론', 'M01', 'full'),
            (r'제2장.*법률관계와 권리', 'M01', 'full'),
            (r'제2장.*신의성실|신의칙', 'M06', 'ch15'),
            (r'제1절 자연인.*권리능력', 'M02', 'full'),
            (r'제1절 자연인.*의사능력', 'M02', 'full'),
            (r'제1절 자연인.*행위능력', 'M02', 'full'),
            (r'제1절 자연인.*주소|부재|실종', 'M02', 'full'),
            (r'제1절 자연인$', 'M02', 'full'),
            (r'제2절 법인', 'M03', 'full'),
            (r'제3장 권리의 주체$', 'M02', 'full'),
            (r'제4장 권리의 객체', 'M04', 'full'),
            (r'제5장 권리의 변동.*제1절 총설', 'M05', 'ch05'),
            (r'제2절 법률행위', 'M05', 'ch09'),
            (r'제3절 의사표시.*흠 있는', 'M05', 'ch10'),
            (r'제3절 의사표시.*효력발생', 'M05', 'ch10'),
            (r'제3절 의사표시$', 'M05', 'ch10'),
            (r'제4절 법률행위의 대리', 'M05', 'ch10'),
            (r'제5절.*무효와 취소', 'M05', 'ch12'),
            (r'제6절 법률행위의 부관', 'M05', 'ch12'),
            (r'제6장 기간', 'M06', 'ch14'),
            (r'제7장 소멸시효', 'M06', 'ch14'),
            (r'물권법.*제1장.*제1절 물권법 일반|물권변동.*제1절|제2절 물권변동', 'B01', 'L1a'),
            (r'물권법.*제1장.*부동산 물권변동', 'B01', 'ch03'),
            (r'물권법.*제1장.*동산 물권', 'B01', 'ch05'),
            (r'물권법.*제1장.*물권의 소멸', 'B01', 'ch07'),
            (r'물권법.*제1장', 'B01', 'L1a'),
            (r'물권법.*제2장 점유권', 'B02', 'full'),
            (r'물권법.*제3장 소유권.*제1절 총설', 'B03', 'ch12'),
            (r'물권법.*제3장 소유권.*제2절 상린관계', 'B03', 'ch12'),
            (r'물권법.*제3장 소유권.*제3절 소유권의 취득.*총설', 'B03', 'ch14'),
            (r'물권법.*제3장 소유권.*제3절 소유권의 취득.*점유취득시효', 'B03', 'ch14'),
            (r'물권법.*제3장 소유권.*제3절 소유권의 취득.*등기부 취득시효', 'B03', 'ch14'),
            (r'물권법.*제3장 소유권.*제3절 소유권의 취득.*중단', 'B03', 'ch14'),
            (r'물권법.*제3장 소유권.*제4절 기타 소유권', 'B03', 'ch14'),
            (r'물권법.*제3장 소유권.*제5절 소유권에 기한 물권적 청구권', 'B02', 'ch08'),
            (r'물권법.*제3장 소유권.*제6절 공동소유', 'B03', 'ch16'),
            (r'물권법.*제3장 소유권.*제7절 명의신탁', 'B03', 'ch17'),
            (r'물권법.*제3장 소유권', 'B03', 'ch12'),
            (r'물권법.*제4장 용익물권.*지상권', 'B04', 'ch18'),
            (r'물권법.*제4장 용익물권.*지역권', 'B04', 'ch20'),
            (r'물권법.*제4장 용익물권.*전세권', 'B04', 'ch21'),
            (r'물권법.*제4장 용익물권', 'B04', 'ch18'),
            (r'물권법.*제5장 담보물권.*제1절 총설', 'B05', 'ch22'),
            (r'물권법.*제5장 담보물권.*제2절 유치권', 'B05', 'ch23'),
            (r'물권법.*제5장 담보물권.*제3절 질권.*동산질권', 'B05', 'ch24'),
            (r'물권법.*제5장 담보물권.*제3절 질권.*권리질권', 'B05', 'ch25'),
            (r'물권법.*제5장 담보물권.*제4절 저당권', 'B05', 'ch26'),
            (r'물권법.*제5장 담보물권.*제5절 비전형담보', 'B05', 'ch31'),
            (r'물권법.*제5장 담보물권', 'B05', 'ch22'),
        ],
    },
    'economics': {
        'tax_key': '경제학원론',
        'title': '경제학원론',
        'mapping': [
            # 미시 — M01~M08
            (r'미시.*제1장', 'M01', 'full'),
            (r'미시.*제2장', 'M02', 'full'),
            (r'미시.*제3장', 'M03', 'full'),
            (r'미시.*제4장', 'M04', 'full'),
            (r'미시.*제5장', 'M05', 'full'),
            (r'미시.*제6장', 'M06', 'full'),
            (r'미시.*제7장', 'M07', 'full'),
            (r'미시.*제8장', 'M08', 'full'),
            # 거시 — G01~G07
            (r'거시.*제1장', 'G01', 'full'),
            (r'거시.*제2장', 'G02', 'full'),
            (r'거시.*제3장', 'G03', 'full'),
            (r'거시.*제4장', 'G04', 'full'),
            (r'거시.*제5장', 'G05', 'full'),
            (r'거시.*제6장', 'G06', 'full'),
            (r'거시.*제7장', 'G07', 'full'),
            # 국제 — G08·G09
            (r'국제.*제1장', 'G08', 'full'),
            (r'국제.*제2장', 'G09', 'full'),
            # 재정 — 별도 자료 없음. 미시 일부로 fallback
            (r'재정.*제1장', 'M01', 'full'),
            (r'재정.*제2장', 'M08', 'full'),
            (r'재정.*제3장', 'M08', 'full'),
            (r'재정.*제4장', 'M02', 'full'),
            (r'재정.*제5장', 'M02', 'full'),
            (r'재정.*제6장', 'M07', 'full'),
            (r'재정.*제7장', 'M07', 'full'),
        ],
    },
    'realestate': {
        'tax_key': '부동산학원론',
        'title': '부동산학원론',
        'mapping': [
            (r'PART 01', 'PART01', 'full'),
            (r'PART 02', 'PART02', 'full'),
            (r'PART 03', 'PART03', 'full'),
            (r'PART 04', 'PART04', 'full'),
            (r'PART 05', 'PART05', 'full'),
            (r'PART 06', 'PART06', 'full'),
            (r'PART 07', 'PART07', 'full'),
            (r'PART 08', 'PART08', 'full'),
            (r'PART 09', 'PART09', 'full'),
        ],
    },
    'law': {
        'tax_key': '감정평가관계법규',
        'title': '감정평가관계법규',
        # taxonomy 9 PART → 단원 자료 6 PART(국토계획·도정·공간정보·감정평가·부공·국유재산)
        # 매핑: 국토계획법 PART 01→PART01, 건축법 PART 02→PART01(국토계획법에 통합), 도정법 PART 03→PART02,
        #       공간정보 PART 04→PART03, 부동산등기 PART 05→PART05(부공법), 국유재산 PART 06→PART06,
        #       부공법 PART 07→PART05, 감정평가법 PART 08→PART04, 동산담보 PART 09→PART05 fallback
        'mapping': [
            (r'PART 01', 'PART01', 'full'),
            (r'PART 02', 'PART01', 'full'),
            (r'PART 03', 'PART02', 'full'),
            (r'PART 04', 'PART03', 'full'),
            (r'PART 05', 'PART05', 'full'),
            (r'PART 06', 'PART06', 'full'),
            (r'PART 07', 'PART05', 'full'),
            (r'PART 08', 'PART04', 'full'),
            (r'PART 09', 'PART05', 'full'),
        ],
    },
    'accounting': {
        'tax_key': '회계학',
        'title': '회계학',
        # 재무회계 7장(taxonomy) ↔ F01~F08(단원), 원가 6장 ↔ C01~C04.
        # 더 정확한 매핑 위해 leaf 후미 키워드 기반 룰 사용.
        'mapping': [
            # 재무회계 제1장: 개념체계·재무제표 표시
            (r'재무.*개념체계|재무.*재무제표 표시|재무.*제1장', 'F04', 'full'),
            # 재무회계 제2장: 재고·유형·무형 자산
            (r'재무.*재고자산', 'F01', 'full'),
            (r'재무.*유형자산|재무.*투자부동산|재무.*차입원가', 'F02', 'full'),
            (r'재무.*무형자산', 'F02', 'full'),
            (r'재무.*제2장', 'F01', 'full'),
            # 재무회계 제3장: 금융부채·충당
            (r'재무.*금융부채|재무.*충당부채|재무.*제3장', 'F03', 'full'),
            # 재무회계 제4장: 자본·복합금융
            (r'재무.*복합금융', 'F05', 'full'),
            (r'재무.*자본|재무.*제4장', 'F03', 'full'),
            # 재무회계 제5장: 수익·건설계약·종업원
            (r'재무.*고객과의 계약|재무.*건설계약|재무.*수익|재무.*제5장', 'F08', 'full'),
            (r'재무.*종업원급여', 'F06', 'full'),
            # 재무회계 제6장: 주당이익·회계변경·현금흐름
            (r'재무.*주당이익|재무.*회계변경|재무.*오류수정|재무.*현금흐름|재무.*제6장', 'F07', 'full'),
            # 재무회계 제7장: 관계기업·환율·보고기간 후
            (r'재무.*관계기업|재무.*지분법|재무.*환율|재무.*보고기간 후|재무.*제7장', 'F08', 'full'),
            # 추가: 금융자산·리스·법인세 (단원 파일에 들어있음)
            (r'재무.*금융자산', 'F05', 'full'),
            (r'재무.*리스|재무.*법인세', 'F06', 'full'),
            (r'재무.*주식기준보상', 'F05', 'full'),
            (r'재무.*사업결합', 'F08', 'full'),
            # 원가관리 제1장: 원가흐름·제조기업
            (r'원가.*원가흐름|원가.*제조기업|원가.*제1장', 'C01', 'full'),
            # 원가관리 제2장: 개별·보조부문·활동기준
            (r'원가.*개별원가|원가.*보조부문', 'C01', 'full'),
            (r'원가.*활동기준', 'C02', 'full'),
            (r'원가.*제2장', 'C01', 'full'),
            # 원가관리 제3장: 변동원가·CVP·원가추정
            (r'원가.*전부원가|원가.*변동원가', 'C02', 'full'),
            (r'원가.*원가함수|원가.*추정', 'C03', 'full'),
            (r'원가.*CVP|원가.*조업도|원가.*제3장', 'C03', 'full'),
            # 원가관리 제4장: 표준원가
            (r'원가.*표준원가|원가.*제4장', 'C04', 'full'),
            # 원가관리 제5장: 관련원가·대체가격
            (r'원가.*관련원가|원가.*불확실성|원가.*의사결정', 'C03', 'full'),
            (r'원가.*대체가격', 'C04', 'full'),
            (r'원가.*제5장', 'C03', 'full'),
            # 원가관리 제6장: 종합예산·투자중심점
            (r'원가.*종합예산|원가.*예산', 'C03', 'full'),
            (r'원가.*투자중심점|원가.*성과평가|원가.*최신|원가.*제6장', 'C04', 'full'),
            # 결합원가 (C02)
            (r'원가.*결합원가', 'C02', 'full'),
            # 종합·공손 (C01)
            (r'원가.*종합원가|원가.*공손', 'C01', 'full'),
        ],
    },
}


def slugify(s):
    return re.sub(r'\W+', '_', s).strip('_')


def make_id(subject_id, path):
    return f"{subject_id}__" + '__'.join(slugify(p) for p in path)


_MD_SECTION_CACHE = {}

def extract_md_sections(unit_path):
    """단원 MD의 ## 헤더(제외: ###) line range 추출. 캐시."""
    if unit_path in _MD_SECTION_CACHE:
        return _MD_SECTION_CACHE[unit_path]
    if not os.path.exists(unit_path):
        _MD_SECTION_CACHE[unit_path] = []
        return []
    txt = open(unit_path, encoding='utf-8').read()
    lines = txt.split('\n')
    out = []
    cur = None
    for i, line in enumerate(lines, 1):
        if line.startswith('### '): continue
        m = re.match(r'^##\s+(.+?)\s*$', line)
        if m:
            if cur:
                cur['end'] = i - 1
                out.append(cur)
            cur = {'name': m.group(1).strip(), 'start': i, 'end': len(lines)}
    if cur:
        out.append(cur)
    _MD_SECTION_CACHE[unit_path] = out
    return out


def _norm_title(s):
    """비교용 정규화 — 제N장/절/관/Chapter/PART 접두 제거."""
    s = re.sub(r'<a\s+name="[^"]+"\s*>\s*</a>', '', s)
    s = re.sub(r'^[\W_]+|[\W_]+$', '', s)
    s = re.sub(r'^(제\d+(장|절|관|편)|Chapter\s*\d+|PART\s*\d+)\s+', '', s)
    return s.strip()


def match_leaf_section(leaf_path, md_sections):
    """leaf의 path 후미를 단원 MD의 ## 헤더와 매칭. 가장 좋은 match return (없으면 None)."""
    if not md_sections: return None
    for tok in reversed(leaf_path):
        t = _norm_title(tok)
        if not t: continue
        for s in md_sections:
            n = _norm_title(s['name'])
            if not n: continue
            if t == n: return s
        for s in md_sections:
            n = _norm_title(s['name'])
            if not n: continue
            if (t in n) or (n in t): return s
    return None


_MD_TEXT_CACHE = {}

def fuzzy_window_in_md(unit_path, leaf_path, before=40, after=700):
    """## 헤더 매칭 실패 시: 본문에서 leaf 키워드 첫 등장 위치 ± 윈도우.
    단원 MD가 200~600KB로 클 때 700줄 윈도우는 ~50KB로 토큰 효율."""
    if not unit_path or not os.path.exists(unit_path): return None
    if unit_path not in _MD_TEXT_CACHE:
        _MD_TEXT_CACHE[unit_path] = open(unit_path, encoding='utf-8').read()
    txt = _MD_TEXT_CACHE[unit_path]
    total = txt.count('\n') + 1
    for tok in reversed(leaf_path):
        kw = _norm_title(tok)
        if not kw or len(kw) < 2: continue
        idx = txt.find(kw)
        if idx < 0: continue
        line_no = txt.count('\n', 0, idx) + 1
        return {
            'name': kw,
            'start': max(1, line_no - before),
            'end': min(total, line_no + after),
        }
    return None


def best_section_for_leaf(unit_path, leaf_path):
    """## 헤더 매칭 우선, 실패 시 본문 키워드 검색 윈도우."""
    md_secs = extract_md_sections(unit_path)
    matched = match_leaf_section(leaf_path, md_secs)
    if matched and matched.get('end', 0) - matched.get('start', 0) < 2000:
        return matched
    return fuzzy_window_in_md(unit_path, leaf_path) or matched


def flatten_leaves(subject_id, conf):
    tax_key = conf['tax_key']
    if tax_key not in TAX:
        print(f'  ⚠ taxonomy에 {tax_key} 없음, skip')
        return []
    s = TAX[tax_key]
    leaves = []
    has_subs = s.get('has_subjects')
    if has_subs:
        for sub, chapters in s['subjects'].items():
            for ch in chapters:
                _flatten_chapter([sub, ch['name']], ch, leaves)
    else:
        for ch in s.get('chapters', []):
            _flatten_chapter([ch['name']], ch, leaves)
    return leaves


def _flatten_chapter(prefix, ch, out):
    secs = ch.get('sections', [])
    if not secs:
        out.append(prefix)
        return
    for sec in secs:
        items = sec.get('items', [])
        if not items:
            out.append(prefix + [sec['name']])
            continue
        for it in items:
            out.append(prefix + [sec['name'], it['name']])


def find_mapping(path_str, mapping):
    for pat, code, sec in mapping:
        if re.search(pat, path_str):
            return code, sec
    return None, None


def build_for_subject(subject_id, conf):
    print(f'\n[{subject_id}] {conf["title"]}')
    base = os.path.join(ROOT, f'viewer/public/data/study/{subject_id}')
    units_dir = os.path.join(base, 'units')
    leaves = flatten_leaves(subject_id, conf)
    out = []
    unmapped = []
    for path in leaves:
        path_str = ' / '.join(path)
        code, sec_key = find_mapping(path_str, conf['mapping'])
        if not code:
            unmapped.append(path_str)
            # 첫 단원으로 fallback
            unit_files = sorted([f for f in os.listdir(units_dir) if f.endswith('.md')]) if os.path.isdir(units_dir) else []
            code = (unit_files[0].replace('.md', '') if unit_files else 'PART01')
            sec_key = 'full'
        unit_file_rel = f'units/{code}.md'
        unit_file_full = os.path.join(base, unit_file_rel)
        exists = os.path.exists(unit_file_full)
        problems_file_rel = f'problems/{code}.md'
        problems_exists = os.path.exists(os.path.join(base, problems_file_rel))
        # section_lines 자동 매칭: ## 헤더 → fuzzy 키워드 검색 → fallback full
        section_lines = [1, 99999]
        section_name = '전체'
        actual_sec_key = sec_key
        if exists:
            matched = best_section_for_leaf(unit_file_full, path)
            if matched:
                section_lines = [matched['start'], matched['end']]
                section_name = matched['name']
                actual_sec_key = 'auto'
        out.append({
            'id': make_id(subject_id, path),
            'path': path,
            'leaf_type': ['subject', 'chapter', 'section', 'item'][min(len(path) - 1, 3)],
            'title': path[-1].split('·')[0].strip(),
            'subject_root': path[0],
            'frequency': 2,
            'unit_code': code,
            'unit_file': unit_file_rel if exists else None,
            'section_key': actual_sec_key,
            'section_lines': section_lines,
            'section_name': section_name,
            'problems_file': problems_file_rel if problems_exists else None,
        })
    index = {
        'subject': conf['title'],
        'subject_id': subject_id,
        'exam': '감정평가사 1차',
        'total_questions_per_exam': 40,
        'taxonomy_source': '/data/taxonomy.json',
        'units_dir': f'/data/study/{subject_id}/units',
        'problems_dir': f'/data/study/{subject_id}/problems',
        'handover_file': f'/data/study/{subject_id}/handover.md',
        'leaves': out,
        'tree': TAX[conf['tax_key']].get('subjects') or {'_root': TAX[conf['tax_key']].get('chapters', [])},
        'default_leaf': out[0]['id'] if out else None,
        'version': 'v2.1',
    }
    target = os.path.join(base, 'ai_taxonomy_index.json')
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f'  leaves={len(out)}, unmapped={len(unmapped)}')
    if unmapped:
        for u in unmapped[:5]: print(f'    · {u}')
    print(f'  → {target}')


if __name__ == '__main__':
    # civil은 기존 chapters_index의 정교한 section_lines를 보존하기 위해
    # 명시 인자가 있을 때만 재생성. 기본은 4과목만.
    targets = sys.argv[1:] if len(sys.argv) > 1 else ['economics', 'realestate', 'law', 'accounting']
    for sid in targets:
        if sid in SUBJECTS:
            build_for_subject(sid, SUBJECTS[sid])
        else:
            print(f'unknown subject: {sid}')
