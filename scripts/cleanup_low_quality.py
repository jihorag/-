#!/usr/bin/env python3
"""불량 문제 일괄 삭제 — 본문 200자 미만의 표준(3)·응용(4)·고난도(5) 제거.

입문(1)·기초(2)는 유지 (개념·약술·간단 계산은 짧아도 적정).
"""
import json
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')

DELETE_THRESHOLD = {
    3: 400,   # 표준: 본문 400자 미만 삭제 (자료·산식 요구)
    4: 800,   # 응용: 800자 미만 (자료 3-5개 요구)
    5: 1500,  # 고난도: 1500자 미만 (시나리오·다중자료·다중물음)
}


def main():
    summary = {}
    total_deleted = 0
    total_remaining = 0

    for ch in ['2a', '3', '4', '5', '6a', '6b', '7', '8a', '8b']:
        path = DATA_DIR / f'{ch}.json'
        data = json.loads(path.read_text(encoding='utf-8'))

        kept = []
        deleted = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for q in data['questions']:
            # official 등 practice-set 외는 무조건 유지
            if q.get('source') != 'practice-set':
                kept.append(q)
                continue

            diff = q.get('difficulty', 0)
            body_len = len(q.get('body', ''))

            # 표준·응용·고난도 중 부실 = 삭제
            threshold = DELETE_THRESHOLD.get(diff)
            if threshold and body_len < threshold:
                deleted[diff] = deleted.get(diff, 0) + 1
                continue

            kept.append(q)

        before = len(data['questions'])
        data['questions'] = kept
        data['count'] = len(kept)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

        del_count = sum(deleted.values())
        total_deleted += del_count
        total_remaining += len(kept)

        # 남은 분포
        dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for q in kept:
            if q.get('source') == 'practice-set':
                d = q.get('difficulty', 0)
                if d in dist: dist[d] += 1

        summary[ch] = (before, len(kept), deleted, dist)

    print('=== 삭제 결과 ===')
    for ch, (before, after, deleted, dist) in summary.items():
        del_str = ' / '.join(f'{d}:{deleted[d]}' for d in [3,4,5] if deleted[d])
        print(f'  {ch}: {before} → {after} (삭제 {sum(deleted.values())}: {del_str})')
        print(f'      practice 분포: 입{dist[1]}·기{dist[2]}·표{dist[3]}·응{dist[4]}·고{dist[5]}')

    print(f'\n총 삭제: {total_deleted}개, 남은: {total_remaining}개')


if __name__ == '__main__':
    main()
