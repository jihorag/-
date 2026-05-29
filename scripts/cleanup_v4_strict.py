#!/usr/bin/env python3
"""v4 §9.6 기준 부적격 문제 일괄 폐기 (강력 cleanup).

폐기 조건:
- 본문 길이 < v4 §9.6 최소
- 답안 길이 < v4 §9.6 최소
- 주제 나열형 물음 (표준 이상)
- 법령 인용 없음 (표준 이상)
- 시나리오 도입 없음 (표준 이상)
- Ⅰ-Ⅱ-Ⅲ 구조 없음 (표준 이상)
"""
import json
import re
from pathlib import Path
from datetime import datetime, timezone

DATA = Path('viewer/public/data/essay/practice')

# v4 §9.6 최소 기준
MIN_BODY = {1: 30, 2: 80, 3: 400, 4: 800, 5: 1500}
MIN_ANSWER = {1: 150, 2: 300, 3: 800, 4: 1500, 5: 3000}

TOPIC_LIST_PATTERN = re.compile(
    r'\[\s*물음\s*\][\s\n]*\d+\.\s*[^\n]{1,30}\n+\d+\.\s*', re.MULTILINE
)
SCENARIO_PATTERN = re.compile(r'(감정평가사|평가사|의뢰)')
LAW_PATTERN = re.compile(
    r'(토지보상법|시행규칙|감정평가규칙|가치\s*§|법\s*§|규칙\s*§|시행령|부공법|도시정비법|국토계획법)'
)


def check_v4(q):
    """v4 기준 통과 여부 + 실패 사유 반환."""
    diff = q.get('difficulty', 0)
    if diff not in MIN_BODY:
        return True, []

    # official 등 practice-set 외는 유지
    if q.get('source') != 'practice-set':
        return True, []

    body = q.get('body') or ''
    answer = q.get('modelAnswer') or ''
    fails = []

    if len(body) < MIN_BODY[diff]:
        fails.append(f'본문{len(body)}<{MIN_BODY[diff]}')
    if len(answer) < MIN_ANSWER[diff]:
        fails.append(f'답안{len(answer)}<{MIN_ANSWER[diff]}')

    if diff >= 3:
        if TOPIC_LIST_PATTERN.search(body):
            fails.append('주제나열형')
        if not SCENARIO_PATTERN.search(body[:300]):
            fails.append('시나리오없음')
        if not LAW_PATTERN.search(answer):
            fails.append('법령없음')
        if not re.search(r'Ⅰ\.|##\s*Ⅰ', answer):
            fails.append('구조없음')

    return len(fails) == 0, fails


def main():
    total_before = 0
    total_after = 0
    total_deleted = 0
    chapter_stats = {}

    for ch in ['2a', '3', '4', '5', '6a', '6b', '7', '8a', '8b']:
        path = DATA / f'{ch}.json'
        data = json.loads(path.read_text(encoding='utf-8'))

        kept = []
        deleted_by_diff = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        before = len(data['questions'])

        for q in data['questions']:
            passes, fails = check_v4(q)
            if passes:
                kept.append(q)
            else:
                diff = q.get('difficulty', 0)
                if diff in deleted_by_diff:
                    deleted_by_diff[diff] += 1

        after = len(kept)
        deleted = before - after

        data['questions'] = kept
        data['count'] = after
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

        chapter_stats[ch] = (before, after, deleted_by_diff)
        total_before += before
        total_after += after
        total_deleted += deleted

    # manifest 업데이트
    m_path = DATA / 'manifest.json'
    m = json.loads(m_path.read_text())
    for c in m['chapters']:
        d = json.loads((DATA / f'{c["id"]}.json').read_text())
        c['count'] = len(d['questions'])
        c['withAnswer'] = sum(1 for q in d['questions'] if q.get('modelAnswer'))
        c['matchedAnswer'] = sum(
            1 for q in d['questions']
            if q.get('modelAnswer') and q.get('modelAnswerSource')
        )
    m['total'] = sum(c['count'] for c in m['chapters'])
    m['built_at'] = datetime.now(timezone.utc).isoformat()
    m_path.write_text(json.dumps(m, ensure_ascii=False, indent=2))

    # 결과 출력
    print('=== v4 강력 cleanup 결과 ===\n')
    print(f'{"단원":<6}{"전":>6}{"후":>6}{"삭제":>6}{"입":>5}{"기":>5}{"표":>5}{"응":>5}{"고":>5}')
    for ch, (before, after, d) in chapter_stats.items():
        deleted = before - after
        print(
            f'{ch:<6}{before:>6}{after:>6}{deleted:>6}'
            f'{d[1]:>5}{d[2]:>5}{d[3]:>5}{d[4]:>5}{d[5]:>5}'
        )

    print(f'\n전체: {total_before} → {total_after} (삭제 {total_deleted})')
    print(f'manifest total: {m["total"]}')


if __name__ == '__main__':
    main()
