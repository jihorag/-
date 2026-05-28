#!/usr/bin/env python3
"""단원 3 정비 — 짧은 표준+를 입문·기초로 강등."""
import json
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')


def demote_short(q):
    body_len = len(q.get('body', ''))
    if q.get('source') != 'practice-set':
        return False
    if q.get('difficulty', 0) < 3:
        return False
    changed = False
    if body_len < 120:
        if q.get('difficulty') != 1:
            q['difficulty'] = 1; changed = True
        if q.get('points', 0) > 10:
            q['points'] = 5; changed = True
    elif body_len < 220:
        if q.get('difficulty') != 2:
            q['difficulty'] = 2; changed = True
        if q.get('points', 0) > 15:
            q['points'] = 10; changed = True
    elif body_len < 350:
        if q.get('difficulty') != 2:
            q['difficulty'] = 2; changed = True
        if q.get('points', 0) > 20:
            q['points'] = 15; changed = True
    return changed


def main():
    path = DATA_DIR / '3.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    demoted = sum(1 for q in data['questions'] if demote_short(q))
    print(f'[강등] {demoted}개')
    data['count'] = len(data['questions'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    practice = [q for q in data['questions'] if q.get('source') == 'practice-set']
    dist = {}
    for q in practice:
        d = q.get('difficulty', 0)
        dist[d] = dist.get(d, 0) + 1
    print(f"practice-set 분포: {dist}")


if __name__ == '__main__':
    main()
