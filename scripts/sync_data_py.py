#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sync-data.mjs를 Python으로 재구현 (node 없는 환경용)."""
import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
QDB = ROOT / 'questions_db.json'
TAX = ROOT / 'taxonomy_v4.json'
DEST = ROOT / 'viewer' / 'public' / 'data'
EXAMS = DEST / 'exams'


def is_classified(q):
    iv = q.get('indexing_v4')
    if not iv:
        return False
    if iv.get('in_scope') is False:
        return False
    mt = iv.get('mapped_taxonomy')
    return bool(
        mt and mt.get('subject') and
        iv.get('processed_by') in ('gemini-2.5-flash', 'claude-sonnet-4-6')
    )


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    EXAMS.mkdir(parents=True, exist_ok=True)

    # taxonomy
    if TAX.exists():
        with open(TAX, encoding='utf-8') as f:
            tax = json.load(f)
        with open(DEST / 'taxonomy.json', 'w', encoding='utf-8') as f:
            json.dump(tax, f, ensure_ascii=False)
        kb = (DEST / 'taxonomy.json').stat().st_size / 1024
        print(f'[sync] taxonomy.json ({kb:.1f} KB)')

    # questions
    if not QDB.exists():
        print('No questions_db.json')
        return
    with open(QDB, encoding='utf-8') as f:
        arr = json.load(f)

    groups = {}
    for q in arr:
        ex = q.get('exam') or '기타'
        groups.setdefault(ex, []).append(q)
    exams = sorted(groups.keys())

    want = {f'{i:02d}.json' for i in range(len(exams))}
    for f in os.listdir(EXAMS):
        if f.endswith('.json') and f not in want:
            try:
                os.remove(EXAMS / f)
            except OSError:
                pass

    manifest_exams = []
    for i, name in enumerate(exams):
        lst = groups[name]
        fn = f'{i:02d}.json'
        path = EXAMS / fn
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(lst, f, ensure_ascii=False)
        classified = sum(1 for q in lst if is_classified(q))
        years = sorted({str(q.get('year') or '미상') for q in lst})
        size = path.stat().st_size
        manifest_exams.append({
            'name': name, 'file': fn, 'count': len(lst),
            'classified': classified, 'years': years, 'sizeBytes': size,
        })
        print(f'[sync] {fn} = {name} · {len(lst)}문 ({size/1024:.0f} KB)')

    legacy = DEST / 'questions_db.json'
    if legacy.exists():
        try:
            os.remove(legacy)
            print('[sync] removed legacy questions_db.json')
        except OSError:
            pass

    manifest = {
        'built_at': datetime.now(timezone.utc).isoformat(),
        'total': len(arr),
        'classified': sum(e['classified'] for e in manifest_exams),
        'exams': manifest_exams,
    }
    with open(DEST / 'manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False)
    print(f'[sync] manifest.json -> {len(exams)} exams, {len(arr)} questions, {manifest["classified"]} classified')


if __name__ == '__main__':
    main()
