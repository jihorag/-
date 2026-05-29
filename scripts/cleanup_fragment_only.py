#!/usr/bin/env python3
"""문장 미완결(fragment) 문제만 정밀 삭제 + 반말 수정.

기준 (둘 다 만족 시 삭제):
- 본문 2줄 이하
- 종결 인정 패턴(마침표·물음표·~시오·~하라·약술/설명/구하시 등) 없음
"""
import json
import re
from pathlib import Path

DATA = Path('viewer/public/data/essay/practice')

SENTENCE_END = re.compile(
    r'[.。!?！？]'
    r'|시오'
    r'|하라'
    r'|약술'
    r'|설명'
    r'|구하시'
    r'|산정하시'
    r'|판단하시'
    r'|기술하시'
    r'|논하시'
    r'|쓰시'
    r'|작성하'
)

BANMAL_FIX = [
    (r'평가하라\b', '평가하시오'),
    (r'약술하라\b', '약술하시오'),
    (r'산정하라\b', '산정하시오'),
    (r'설명하라\b', '설명하시오'),
    (r'논하라\b', '논하시오'),
    (r'기술하라\b', '기술하시오'),
    (r'분석하라\b', '분석하시오'),
    (r'판단하라\b', '판단하시오'),
    (r'구하라\b', '구하시오'),
]


def is_fragment(body):
    body = body.strip()
    if not body:
        return True
    lines = [l for l in body.split('\n') if l.strip()]
    if len(lines) > 2:
        return False
    return not SENTENCE_END.search(body)


def fix_banmal(text):
    for p, r in BANMAL_FIX:
        text = re.sub(p, r, text)
    return text


def main():
    total_deleted = 0
    total_fixed = 0
    for ch in ['2a','3','4','5','6a','6b','7','8a','8b']:
        path = DATA / f'{ch}.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        kept = []
        deleted = 0
        fixed = 0
        for q in data['questions']:
            body = q.get('body') or q.get('question') or ''
            if is_fragment(body):
                deleted += 1
                continue
            # 반말 수정
            new_body = fix_banmal(body)
            new_answer = fix_banmal(q.get('modelAnswer', ''))
            if new_body != body:
                if q.get('body'):
                    q['body'] = new_body
                if q.get('question'):
                    q['question'] = fix_banmal(q.get('question', ''))
                fixed += 1
            if new_answer != q.get('modelAnswer', ''):
                q['modelAnswer'] = new_answer
            kept.append(q)
        before = len(data['questions'])
        data['questions'] = kept
        data['count'] = len(kept)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        total_deleted += deleted
        total_fixed += fixed
        print(f'단원 {ch}: -{deleted} fragment, 반말 수정 {fixed} ({before} → {len(kept)})')
    print(f'\n총: fragment 삭제 {total_deleted}, 반말 수정 {total_fixed}')


if __name__ == '__main__':
    main()
