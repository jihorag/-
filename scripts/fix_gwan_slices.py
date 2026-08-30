#!/usr/bin/env python3
"""
ai_taxonomy_index.json(economics) 의 "제N관" leaf 27개가 조각 슬라이스만 받는 문제 수정.

원인: narrow_subslice.py 가 (또는 그 이전 auto/anchored 계산이) 키워드를 교재의
'마인드 강의노트'(L1) 층 소제목에서 먼저 찾아 멈춰, '기본서'(L3) 층의 진짜
"### 제N관 …" 헤딩 구간을 놓쳤다. 예: 제3관 국민소득 3면 등가 → 마인드 층 144자
조각을 받았지만, 진짜 본문은 기본서 층 1380~1623줄에 있다.

고치는 법: generate_notes.load_leaf_sections() 은 수정 금지 대상이라,
인덱스(section_lines) 쪽을 다시 계산한다.

핵심 관찰(검증됨, 0 mismatch across 17 unit files):
  각 unit_file 안에서 "### 제N관 …" 레벨-3 헤딩들을 문서 순서대로 나열한 리스트와,
  ai_taxonomy_index.json 의 leaves 배열에서 같은 unit_file 을 가리키는,
  제목이 "제N관 …" 형태인 leaf 들을 배열 순서대로 나열한 리스트가 1:1 로 정확히
  대응한다 (개수도 같고, 각 쌍의 N 도 같다). 즉 index 는 원래 문서 순서로 만들어졌고,
  문제는 각 leaf 의 section_lines 값만 틀어진 것이다.

그래서: 각 unit_file 별로 두 리스트를 zip 해서, 각 leaf 의 section_lines 를
[해당 헤딩 줄, 다음 헤딩(레벨 2 또는 3) 줄 - 1] (또는 파일 끝) 로 재계산한다.
이미 맞는 leaf 는 값이 그대로 나오므로 실질적으로 안 바뀐다(증명: dry-run에서 diff 확인).
"""
import json, re, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, 'viewer/public/data/study/economics')
IDX_PATH = os.path.join(BASE, 'ai_taxonomy_index.json')

HEAD_RE = re.compile(r'^(#{2,3})\s+(.*)$')
GWAN_RE = re.compile(r'^제(\d+)관\b')


def compute():
    idx = json.load(open(IDX_PATH, encoding='utf-8'))
    leaves = idx['leaves'] if isinstance(idx, dict) else idx

    by_unit = {}
    for l in leaves:
        uf = l.get('unit_file')
        if uf:
            by_unit.setdefault(uf, []).append(l)

    changes = []  # (leaf, old_lines, new_lines)
    mismatches = []

    for uf, unit_leaves in by_unit.items():
        path = os.path.join(BASE, uf)
        if not os.path.exists(path):
            continue
        lines = open(path, encoding='utf-8').read().split('\n')
        all_heads = []
        for i, line in enumerate(lines, start=1):
            m = HEAD_RE.match(line)
            if m:
                all_heads.append((i, len(m.group(1)), m.group(2).strip()))

        gwan_heads = [(ln, txt) for ln, lvl, txt in all_heads if lvl == 3 and GWAN_RE.match(txt)]
        gwan_leaves = [l for l in unit_leaves if GWAN_RE.match(l.get('title', ''))]

        if len(gwan_heads) != len(gwan_leaves):
            mismatches.append((uf, len(gwan_heads), len(gwan_leaves)))
            continue

        ok = True
        for (ln, txt), lf in zip(gwan_heads, gwan_leaves):
            if GWAN_RE.match(txt).group(1) != GWAN_RE.match(lf['title']).group(1):
                ok = False
        if not ok:
            mismatches.append((uf, 'NUM_MISMATCH'))
            continue

        for idx_i, ((ln, txt), lf) in enumerate(zip(gwan_heads, gwan_leaves)):
            start = ln
            end = gwan_heads[idx_i + 1][0] - 1 if idx_i + 1 < len(gwan_heads) else None
            if end is None:
                # 다음 관 헤딩이 없으면: 파일의 다음 아무 헤딩(레벨2/3) 혹은 파일 끝
                nxt = [h for h in all_heads if h[0] > ln]
                end = (nxt[0][0] - 1) if nxt else len(lines)
            new_lines = [start, end]
            old_lines = lf.get('section_lines')
            if old_lines != new_lines:
                changes.append((lf, old_lines, new_lines))

    return idx, leaves, changes, mismatches


def main():
    apply = '--apply' in sys.argv
    idx, leaves, changes, mismatches = compute()

    print(f'unit 파일 {len(set(l.get("unit_file") for l in leaves if l.get("unit_file")))}개 검사')
    print(f'번호 불일치(수정 안 함): {len(mismatches)}')
    for m in mismatches:
        print('  ', m)
    print(f'section_lines 변경 대상: {len(changes)}개')
    for lf, old, new in changes:
        print(f'  {lf["title"][:40]:42} {old} -> {new}  ({lf.get("unit_file")})')

    if not apply:
        print('\n(dry-run) 실제로 적용하려면 --apply 를 붙이세요.')
        return

    bak = IDX_PATH + '.bak'
    if not os.path.exists(bak):
        shutil.copy(IDX_PATH, bak)
    else:
        # 기존 .bak 은 더 이전 상태(narrow 이전) 보존용 — 덮어쓰지 않고
        # 이번 수정 직전 상태를 별도로 남긴다.
        shutil.copy(IDX_PATH, IDX_PATH + '.pre_gwan_fix.bak')

    for lf, old, new in changes:
        lf['section_lines'] = new

    with open(IDX_PATH, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    print(f'\n적용 완료: {len(changes)}개 section_lines 갱신, 백업 → {IDX_PATH}.pre_gwan_fix.bak')


if __name__ == '__main__':
    main()
