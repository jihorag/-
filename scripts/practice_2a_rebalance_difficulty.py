#!/usr/bin/env python3
"""단원 2a 신규 연습문제 100개의 난이도 재조정.
기준 명확화:
  1 (입문): 단답형, 개념 정의, 5점
  2 (기초): 단순 계산, 1단계 산식, 5점
  3 (표준): 2-3단계 계산, 자료 분석, 5-10점
  4 (응용): 다단계 계산, 시산조정, 10-15점
  5 (고난도): 종합 평가, 다방식·복잡 사례, 15점+
"""
import json
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')

# id → 재조정된 difficulty
DIFFICULTY_ADJUSTMENTS = {
    # 1 (입문) — 단답형, 개념
    'practice-2a-001': 1, 'practice-2a-005': 1, 'practice-2a-007': 1,
    'practice-2a-008': 1, 'practice-2a-011': 1, 'practice-2a-012': 1,
    'practice-2a-013': 1, 'practice-2a-051': 1, 'practice-2a-052': 1,
    'practice-2a-053': 1, 'practice-2a-054': 1, 'practice-2a-056': 1,
    'practice-2a-075': 1, 'practice-2a-078': 1, 'practice-2a-081': 1,
    'practice-2a-082': 1, 'practice-2a-097': 1,

    # 2 (기초) — 단순 계산
    'practice-2a-002': 2, 'practice-2a-014': 2, 'practice-2a-020': 2,
    'practice-2a-021': 2, 'practice-2a-023': 2, 'practice-2a-035': 2,
    'practice-2a-045': 2, 'practice-2a-066': 2, 'practice-2a-067': 2,
    'practice-2a-068': 2, 'practice-2a-069': 2, 'practice-2a-085': 2,
    'practice-2a-087': 2, 'practice-2a-090': 2, 'practice-2a-091': 2,
    'practice-2a-099': 2,

    # 3 (표준) — 2-3단계 계산
    'practice-2a-003': 3, 'practice-2a-015': 3, 'practice-2a-016': 3,
    'practice-2a-022': 3, 'practice-2a-024': 3, 'practice-2a-025': 3,
    'practice-2a-026': 3, 'practice-2a-031': 3, 'practice-2a-032': 3,
    'practice-2a-033': 3, 'practice-2a-034': 3, 'practice-2a-036': 3,
    'practice-2a-039': 3, 'practice-2a-041': 3, 'practice-2a-042': 3,
    'practice-2a-043': 3, 'practice-2a-044': 3, 'practice-2a-046': 3,
    'practice-2a-047': 3, 'practice-2a-048': 3, 'practice-2a-055': 3,
    'practice-2a-057': 3, 'practice-2a-059': 3, 'practice-2a-071': 3,
    'practice-2a-073': 3, 'practice-2a-077': 3, 'practice-2a-079': 3,
    'practice-2a-080': 3, 'practice-2a-083': 3, 'practice-2a-084': 3,
    'practice-2a-088': 3, 'practice-2a-092': 3, 'practice-2a-093': 3,
    'practice-2a-094': 3, 'practice-2a-098': 3,

    # 4 (응용) — 다단계 계산·종합
    'practice-2a-004': 4, 'practice-2a-009': 4, 'practice-2a-017': 4,
    'practice-2a-018': 4, 'practice-2a-019': 4, 'practice-2a-028': 4,
    'practice-2a-029': 4, 'practice-2a-037': 4, 'practice-2a-038': 4,
    'practice-2a-040': 4, 'practice-2a-058': 4, 'practice-2a-061': 4,
    'practice-2a-062': 4, 'practice-2a-064': 4, 'practice-2a-065': 4,
    'practice-2a-072': 4, 'practice-2a-074': 4, 'practice-2a-076': 4,
    'practice-2a-086': 4, 'practice-2a-089': 4, 'practice-2a-095': 4,

    # 5 (고난도) — 종합 평가·다방식·실무 사례
    'practice-2a-006': 5, 'practice-2a-010': 5, 'practice-2a-027': 5,
    'practice-2a-030': 5, 'practice-2a-049': 5, 'practice-2a-050': 5,
    'practice-2a-060': 5, 'practice-2a-063': 5, 'practice-2a-070': 5,
    'practice-2a-096': 5, 'practice-2a-100': 5,
}


def main():
    p = DATA_DIR / '2a.json'
    d = json.loads(p.read_text(encoding='utf-8'))

    updated = 0
    for q in d['questions']:
        if q['id'] in DIFFICULTY_ADJUSTMENTS:
            new_diff = DIFFICULTY_ADJUSTMENTS[q['id']]
            old_diff = q.get('difficulty')
            if old_diff != new_diff:
                q['difficulty'] = new_diff
                updated += 1

    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')

    # 분포 확인
    from collections import Counter
    src_diff = {'official': Counter(), 'practice-set': Counter()}
    for q in d['questions']:
        src = q.get('source')
        diff = q.get('difficulty')
        if src in src_diff:
            src_diff[src][diff] += 1
    print(f'단원 2a 난이도 재조정: {updated}개')
    print(f'\n재조정 후 분포:')
    for src in ['official', 'practice-set']:
        print(f'  {src}:')
        for d_val in [1, 2, 3, 4, 5, None]:
            cnt = src_diff[src][d_val]
            if cnt > 0:
                star = '★' * d_val if d_val else '-'
                print(f'    난이도 {d_val} ({star}): {cnt}개')


if __name__ == '__main__':
    main()
