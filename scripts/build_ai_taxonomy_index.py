#!/usr/bin/env python3
"""
taxonomy.json (민법) leaf 노드 모두에 대해 교재 단원 MD slice를 매핑한 ai_taxonomy_index.json 생성.

매핑 룰 — 교재(M01~M06 / B01~B05) 내 ## 헤더 / 키워드 기반.
"""
import json, re, hashlib, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAX = json.load(open(os.path.join(ROOT, 'viewer/public/data/taxonomy.json')))
UNITS = os.path.join(ROOT, 'viewer/public/data/study/civil/units')

# 1) chapters_index.json에서 sections.lines 정의 재사용 (이미 작성된 큰 단원 slice 좌표)
CIDX = json.load(open(os.path.join(ROOT, 'viewer/public/data/study/civil/chapters_index.json')))
SEC_BY_UNIT = {c['code']: {s['key']: s for s in c.get('sections', [])} for c in CIDX['chapters']}

# 매핑 룰 — Quiz taxonomy leaf 키워드 → (unit_code, section_key, fallback_unit)
# section_key='full'이면 단원 전체. 특정 키이면 chapters_index의 lines 적용.
MAPPING_RULES = [
    # (정규식, unit_code, section_key)
    (r'제1장 민법 서론', 'M01', 'full'),
    (r'제2장.*법률관계와 권리', 'M01', 'full'),
    (r'제2장.*신의성실|신의칙', 'M06', 'ch15'),
    # 자연인
    (r'제1절 자연인.*권리능력', 'M02', 'full'),
    (r'제1절 자연인.*의사능력', 'M02', 'full'),
    (r'제1절 자연인.*행위능력', 'M02', 'full'),
    (r'제1절 자연인.*주소|부재|실종', 'M02', 'full'),
    (r'제1절 자연인$', 'M02', 'full'),
    (r'제2절 법인', 'M03', 'full'),
    (r'제3장 권리의 주체$', 'M02', 'full'),
    # 권리의 객체
    (r'제4장 권리의 객체', 'M04', 'full'),
    # 권리의 변동 — 법률행위
    (r'제5장 권리의 변동.*제1절 총설', 'M05', 'ch05'),
    (r'제2절 법률행위', 'M05', 'ch09'),
    (r'제3절 의사표시.*흠 있는', 'M05', 'ch10'),
    (r'제3절 의사표시.*효력발생', 'M05', 'ch10'),
    (r'제3절 의사표시$', 'M05', 'ch10'),
    (r'제4절 법률행위의 대리.*서설', 'M05', 'ch10'),
    (r'제4절 법률행위의 대리.*대리권', 'M05', 'ch10'),
    (r'제4절 법률행위의 대리.*대리행위', 'M05', 'ch10'),
    (r'제4절 법률행위의 대리.*복대리', 'M05', 'ch10'),
    (r'제4절 법률행위의 대리.*무권대리', 'M05', 'ch10'),
    (r'제4절 법률행위의 대리$', 'M05', 'ch10'),
    (r'제5절.*무효와 취소.*무효', 'M05', 'ch12'),
    (r'제5절.*무효와 취소.*취소', 'M05', 'ch12'),
    (r'제5절.*무효와 취소$', 'M05', 'ch12'),
    (r'제6절 법률행위의 부관', 'M05', 'ch12'),
    # 기간·소멸시효
    (r'제6장 기간', 'M06', 'ch14'),
    (r'제7장 소멸시효', 'M06', 'ch14'),
    # 물권법
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
    (r'물권법.*제3장 소유권.*제6절 공동소유.*총설', 'B03', 'ch16'),
    (r'물권법.*제3장 소유권.*제6절 공동소유.*공유', 'B03', 'ch16'),
    (r'물권법.*제3장 소유권.*제6절 공동소유.*합유', 'B03', 'ch16'),
    (r'물권법.*제3장 소유권.*제6절 공동소유.*총유', 'B03', 'ch16'),
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
]

# 빈도 가중치 — 단원 단위 frequency를 leaf로 상속
FREQUENCY_BY_UNIT = {c['code']: c.get('frequency', 1) for c in CIDX['chapters']}

def slugify(s):
    return re.sub(r'\W+', '_', s).strip('_')

def make_id(path):
    return '__'.join(slugify(p) for p in path)

def find_mapping(path_str):
    for pat, code, sec in MAPPING_RULES:
        if re.search(pat, path_str):
            return code, sec
    return None, None

leaves = []
civ = TAX['민법']
for subj, chapters in civ['subjects'].items():
    for ch in chapters:
        secs = ch.get('sections', [])
        if not secs:
            leaves.append([subj, ch['name']])
            continue
        for sec in secs:
            items = sec.get('items', [])
            if not items:
                leaves.append([subj, ch['name'], sec['name']])
                continue
            for it in items:
                leaves.append([subj, ch['name'], sec['name'], it['name']])

out = []
unmapped = []
for path in leaves:
    path_str = ' / '.join(path)
    code, sec_key = find_mapping(path_str)
    if not code:
        unmapped.append(path_str)
        code, sec_key = 'M01', 'full'  # safe fallback
    unit_meta = next((c for c in CIDX['chapters'] if c['code'] == code), None)
    section = SEC_BY_UNIT.get(code, {}).get(sec_key)
    out.append({
        'id': make_id(path),
        'path': path,
        'leaf_type': ['subject', 'chapter', 'section', 'item'][len(path) - 1],
        'title': path[-1].split('·')[0].strip(),
        'subject_root': subj,
        'frequency': FREQUENCY_BY_UNIT.get(code, 1),
        'unit_code': code,
        'unit_file': f'units/{code}.md',
        'section_key': sec_key,
        'section_lines': section.get('lines') if section else None,
        'section_name': section.get('name') if section else '전체',
        'problems_file': f'problems/{code}.md',
    })

index = {
    'subject': '민법',
    'subject_id': 'civil',
    'exam': '감정평가사 1차',
    'total_questions_per_exam': 40,
    'taxonomy_source': '/data/taxonomy.json',
    'units_dir': '/data/study/civil/units',
    'problems_dir': '/data/study/civil/problems',
    'handover_file': '/data/study/civil/handover.md',
    'leaves': out,
    'tree': civ['subjects'],
    'default_leaf': make_id(['민법총칙', '제3장 권리의 주체', '제1절 자연인', '제3관 행위능력']),
    'version': 'v2.0',
}

with open(os.path.join(ROOT, 'viewer/public/data/study/civil/ai_taxonomy_index.json'), 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f'Total leaves: {len(out)}')
print(f'Unmapped (fell back to M01): {len(unmapped)}')
for u in unmapped: print('  ', u)
