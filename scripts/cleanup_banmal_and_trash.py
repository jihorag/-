#!/usr/bin/env python3
"""반말(~하라) 수정 + 쓰레기([자료]·결과? 패턴) 삭제."""
import json
import re
from pathlib import Path

DATA = Path('viewer/public/data/essay/practice')

# 반말 → 존댓말 치환
BANMAL_FIX = [
    (r'평가하라\.', '평가하시오.'),
    (r'평가하라\b', '평가하시오'),
    (r'약술하라\.', '약술하시오.'),
    (r'약술하라\b', '약술하시오'),
    (r'산정하라\.', '산정하시오.'),
    (r'산정하라\b', '산정하시오'),
    (r'설명하라\.', '설명하시오.'),
    (r'설명하라\b', '설명하시오'),
    (r'논하라\.', '논하시오.'),
    (r'논하라\b', '논하시오'),
    (r'기술하라\.', '기술하시오.'),
    (r'기술하라\b', '기술하시오'),
    (r'분석하라\.', '분석하시오.'),
    (r'분석하라\b', '분석하시오'),
    (r'판단하라\.', '판단하시오.'),
    (r'판단하라\b', '판단하시오'),
    (r'구하라\.', '구하시오.'),
    (r'구하라\b', '구하시오'),
    # 일반화된 "~하라" → "~하시오" (마지막에)
    (r'(하|되|이|아|어|여|시키)라(\.|\?|\s|$)', r'\1라\2'),  # placeholder, will not match
]

# 쓰레기 패턴: "[자료] ... 결과?"
TRASH_PATTERN = re.compile(r'^\s*\[자료\].*결과\s*\??\s*$', re.DOTALL)


def is_trash(body, answer):
    """진짜 쓰레기 판별."""
    body = body.strip()
    answer = answer.strip()
    # [자료] ... 결과? 패턴
    if TRASH_PATTERN.match(body):
        return True
    # 본문 50자 미만 + 답안 100자 미만 + 답이 단순 계산 결과
    if len(body) < 50 and len(answer) < 100:
        # 본문이 단순 계산식 ([자료] 시작 + 수식만)
        if body.startswith('[자료]') or '결과' in body:
            return True
    return False


def fix_banmal(text):
    """반말 → 존댓말."""
    for pattern, repl in BANMAL_FIX:
        text = re.sub(pattern, repl, text)
    return text


def main():
    total_banmal_fixed = 0
    total_trash_deleted = 0

    for ch in ['2a','3','4','5','6a','6b','7','8a','8b']:
        path = DATA / f'{ch}.json'
        data = json.loads(path.read_text(encoding='utf-8'))

        kept = []
        deleted_count = 0
        fixed_count = 0

        for q in data['questions']:
            body = q.get('body', '') or q.get('question', '')
            answer = q.get('modelAnswer', '')

            # 1. 쓰레기 삭제
            if is_trash(body, answer):
                deleted_count += 1
                continue

            # 2. 반말 수정
            new_body = fix_banmal(body)
            new_answer = fix_banmal(answer)

            if new_body != body or new_answer != answer:
                fixed_count += 1
                if q.get('body'):
                    q['body'] = new_body
                if q.get('question'):
                    q['question'] = fix_banmal(q.get('question', ''))
                q['modelAnswer'] = new_answer

            kept.append(q)

        before = len(data['questions'])
        data['questions'] = kept
        data['count'] = len(kept)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

        total_banmal_fixed += fixed_count
        total_trash_deleted += deleted_count
        print(f'단원 {ch}: 삭제 {deleted_count}, 반말 수정 {fixed_count} ({before} → {len(kept)})')

    print(f'\n총: 쓰레기 삭제 {total_trash_deleted}, 반말 수정 {total_banmal_fixed}')


if __name__ == '__main__':
    main()
