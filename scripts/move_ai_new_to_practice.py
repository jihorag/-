#!/usr/bin/env python3
"""AI 신규 문제를 연습문제(practice-set)로 이동 + v4 검증.

처리:
1. *-generated.json에서 ai-new 문제 추출
2. source='practice-set'으로 변경, genMode 제거
3. v4 §9.6 기준 검토 — 통과만 메인 *.json으로 이동, 불통과는 폐기
"""
import json
import re
from pathlib import Path
from datetime import datetime, timezone

DATA = Path('viewer/public/data/essay/practice')

MIN_BODY = {1: 30, 2: 80, 3: 400, 4: 800, 5: 1500}
MIN_ANSWER = {1: 150, 2: 300, 3: 800, 4: 1500, 5: 3000}

TOPIC_LIST = re.compile(r'\[\s*물음\s*\][\s\n]*\d+\.\s*[^\n]{1,30}\n+\d+\.\s*', re.MULTILINE)
SCENARIO = re.compile(r'(감정평가사|평가사|의뢰)')
LAW = re.compile(r'(토지보상법|시행규칙|감정평가규칙|가치\s*§|법\s*§|규칙\s*§|시행령|부공법|도시정비법|국토계획법)')


def check_v4(q):
    diff = q.get('difficulty', 0)
    if diff not in MIN_BODY:
        return False, ['난이도없음']
    body = q.get('body') or ''
    answer = q.get('modelAnswer') or ''
    fails = []
    if len(body) < MIN_BODY[diff]:
        fails.append(f'본문{len(body)}<{MIN_BODY[diff]}')
    if len(answer) < MIN_ANSWER[diff]:
        fails.append(f'답안{len(answer)}<{MIN_ANSWER[diff]}')
    if diff >= 3:
        if TOPIC_LIST.search(body):
            fails.append('주제나열형')
        if not SCENARIO.search(body[:300]):
            fails.append('시나리오없음')
        if not LAW.search(answer):
            fails.append('법령없음')
        if not re.search(r'Ⅰ\.|##\s*Ⅰ', answer):
            fails.append('구조없음')
    return len(fails) == 0, fails


def get_next_id(data, ch):
    next_id = max(
        (int(m.group(1)) for q in data['questions']
         for m in [re.match(rf'practice-{ch}-(\d+)', q['id'])] if m),
        default=0
    ) + 1
    return next_id


def main():
    summary = {'moved': 0, 'deleted': 0, 'by_chapter': {}}

    for ch in ['2a', '6a']:
        gen_path = DATA / f'{ch}-generated.json'
        main_path = DATA / f'{ch}.json'

        if not gen_path.exists():
            continue

        gen_data = json.loads(gen_path.read_text(encoding='utf-8'))
        main_data = json.loads(main_path.read_text(encoding='utf-8'))

        next_id = get_next_id(main_data, ch)

        moved = []
        deleted = []
        remaining_gen = []

        for q in gen_data['questions']:
            # ai-new가 아닌 것은 generated에 그대로 둠
            if not (q.get('source') == 'ai-generated' and q.get('genMode') == 'new'):
                remaining_gen.append(q)
                continue

            # v4 검증
            passes, fails = check_v4(q)

            if not passes:
                deleted.append((q['id'], fails))
                continue

            # practice-set으로 이동
            new_q = dict(q)
            new_q['source'] = 'practice-set'
            new_q.pop('genMode', None)
            old_id = new_q['id']
            new_id = f'practice-{ch}-{next_id}'
            new_q['id'] = new_id
            new_q['chapter'] = ch
            next_id += 1

            main_data['questions'].append(new_q)
            moved.append((old_id, new_id))

        # generated 파일에서 ai-new 제거 후 저장
        gen_data['questions'] = remaining_gen
        gen_data['count'] = len(remaining_gen)
        gen_path.write_text(json.dumps(gen_data, ensure_ascii=False, indent=2), encoding='utf-8')

        # main 파일 업데이트
        main_data['count'] = len(main_data['questions'])
        main_path.write_text(json.dumps(main_data, ensure_ascii=False, indent=2), encoding='utf-8')

        summary['by_chapter'][ch] = (len(moved), len(deleted))
        summary['moved'] += len(moved)
        summary['deleted'] += len(deleted)

        print(f'\n단원 {ch}: 이동 {len(moved)}, 삭제 {len(deleted)}')
        for old, new in moved:
            print(f'  {old} → {new}')
        if deleted:
            print(f'  [v4 미달 폐기]')
            for qid, fails in deleted:
                print(f'    {qid}: {fails}')

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

    print(f'\n=== 결과 ===')
    print(f'연습문제로 이동: {summary["moved"]}')
    print(f'v4 미달 폐기: {summary["deleted"]}')
    print(f'manifest total: {m["total"]}')


if __name__ == '__main__':
    main()
