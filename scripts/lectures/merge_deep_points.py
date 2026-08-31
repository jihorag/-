#!/usr/bin/env python3
"""심화(deep) 회독 논점을 1회독 트랙의 같은 관에 이어 붙인다.

사용자가 고른 방식: 회독별 트랙을 따로 만들지 않고 **같은 관의 논점 목록 뒤에**
심화 논점을 덧붙인다. 대신 각 논점에 `phase: "deep"` 을 남겨, 나중에 회독별로
걸러 보고 싶어지면 그 한 줄로 갈라낼 수 있게 한다.

id 는 진도 저장의 키다. 기존 논점의 id 는 절대 건드리지 않고, 새 논점만
그 관에서 아직 쓰지 않은 seq 를 이어 받는다.

사용:
  python3 scripts/lectures/merge_deep_points.py economics --only <leaf_id>
  python3 scripts/lectures/merge_deep_points.py economics          # _work 에 있는 것 전부
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import STUDY  # noqa: E402
from track_core import make_point_id  # noqa: E402

WORK_DIR = Path(__file__).resolve().parent / '_work'


def leaf_slot(track, leaf_id):
    for lf in track['leaves']:
        if lf.get('leaf_id') == leaf_id:
            return lf
    return None


def next_seq(leaf):
    """이 관에서 아직 쓰지 않은 seq. 기존 id 를 침범하지 않는다."""
    used = []
    for p in leaf['points']:
        m = re.search(r'-p(\d+)$', p.get('id') or '')
        if m:
            used.append(int(m.group(1)))
    return (max(used) + 1) if used else 1


def leaf_index(track, leaf_id):
    for i, lf in enumerate(track['leaves']):
        if lf.get('leaf_id') == leaf_id:
            return i
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--phase', default='deep')
    ap.add_argument('--only', help='leaf_id 하나만')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    src_dir = WORK_DIR / args.subject / args.phase
    track_dir = STUDY / args.subject / 'lectures/track'
    files = ([src_dir / ('%s.json' % args.only)] if args.only
             else sorted(p for p in src_dir.glob('*.json') if not p.name.startswith('_')))

    # 관 → 어느 트랙 파일에 있는지 미리 훑는다.
    tracks = {}
    where = {}
    for tp in sorted(track_dir.glob('*.basic.json')):
        t = json.loads(tp.read_text(encoding='utf-8'))
        tracks[tp] = t
        for lf in t['leaves']:
            if lf.get('leaf_id'):
                where[lf['leaf_id']] = tp

    merged = skipped = added = 0
    for f in files:
        if not f.exists():
            print('  ⚠ 없음: %s' % f.name)
            continue
        leaf_id = f.stem
        tp = where.get(leaf_id)
        if tp is None:
            print('  ⚠ 트랙에 없는 관: %s' % leaf_id)
            skipped += 1
            continue
        pts = json.loads(f.read_text(encoding='utf-8'))
        if not isinstance(pts, list) or not pts:
            print('  · 비어 있음(강의가 다루지 않음): %s' % leaf_id)
            skipped += 1
            continue

        track = tracks[tp]
        leaf = leaf_slot(track, leaf_id)
        unit = track.get('unit_code') or tp.name.split('.')[0]
        li = leaf_index(track, leaf_id)
        seq = next_seq(leaf)

        # 같은 제목이 이미 있으면 다시 붙이지 않는다(재실행 안전).
        have = {p.get('title') for p in leaf['points']}
        fresh = [p for p in pts if p.get('title') not in have]
        for p in fresh:
            p['phase'] = args.phase
            p['id'] = make_point_id(unit, li, seq)
            seq += 1
        leaf['points'].extend(fresh)
        print('  [%s] %s — 심화 %d개 추가 (총 %d)'
              % (unit, leaf['title'], len(fresh), len(leaf['points'])))
        merged += 1
        added += len(fresh)

    if not args.dry_run:
        for tp, t in tracks.items():
            tp.write_text(json.dumps(t, ensure_ascii=False), encoding='utf-8')

    print('\n관 %d개 병합 · 논점 %d개 추가 · 건너뜀 %d개%s'
          % (merged, added, skipped, ' (dry-run)' if args.dry_run else ''))


if __name__ == '__main__':
    main()
