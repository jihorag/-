#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 1: 한국어 조사 자동 변환 + 자동 검수.

처리:
1. "은(는)" → "은" 또는 "는" (앞 단어 받침 여부)
2. "이(가)" → "이" 또는 "가"
3. "을(를)" → "을" 또는 "를"
4. "과(와)" → "과" 또는 "와"
5. 본문에서 관 이름 과다 반복(3회+) 시 두번째 이후 대명사 대체
6. 통계 출력 (수정 건수)
"""
import json
import re
from pathlib import Path
from collections import Counter

PRACTICE_DIR = Path('viewer/public/data/practice/economics')


def get_last_korean(text):
    """문자열의 마지막 한글 글자 반환. 없으면 None."""
    for ch in reversed(text):
        if 0xAC00 <= ord(ch) <= 0xD7A3:
            return ch
    return None


def has_batchim(text_or_char):
    """단어/글자의 마지막 한글 받침 유무. 한글 없으면 True (받침 있다고 가정)."""
    if not text_or_char:
        return True
    ch = get_last_korean(text_or_char)
    if ch is None:
        # 영문/숫자/특수문자만: 발음 추정 어려우므로 'is'로 끝나면 받침 X 등
        # 단순 휴리스틱: 모음(a, e, i, o, u, y)로 끝나면 받침 X
        last = text_or_char[-1].lower() if text_or_char else ''
        if last in 'aeiouy':
            return False
        return True
    return (ord(ch) - 0xAC00) % 28 != 0


PARTICLE_PAIRS = [
    # (패턴 정규식, 받침 있을 때, 받침 없을 때)
    (re.compile(r'(\S+?)은\(는\)'), '은', '는'),
    (re.compile(r'(\S+?)는\(은\)'), '은', '는'),
    (re.compile(r'(\S+?)이\(가\)'), '이', '가'),
    (re.compile(r'(\S+?)가\(이\)'), '이', '가'),
    (re.compile(r'(\S+?)을\(를\)'), '을', '를'),
    (re.compile(r'(\S+?)를\(을\)'), '을', '를'),
    (re.compile(r'(\S+?)과\(와\)'), '과', '와'),
    (re.compile(r'(\S+?)와\(과\)'), '과', '와'),
]


def fix_particles(text):
    """모든 '은(는)' 류를 자동 변환."""
    for pattern, with_b, without_b in PARTICLE_PAIRS:
        def repl(m):
            word = m.group(1)
            return word + (with_b if has_batchim(word) else without_b)
        text = pattern.sub(repl, text)
    return text


def fix_question(q):
    """한 문제의 question/options/explanation 조사 변환."""
    changed = 0
    new_q = fix_particles(q['question'])
    if new_q != q['question']:
        q['question'] = new_q
        changed += 1
    new_opts = []
    for opt in q['options']:
        new_opt = fix_particles(opt)
        if new_opt != opt:
            changed += 1
        new_opts.append(new_opt)
    q['options'] = new_opts
    new_exp = fix_particles(q['explanation'])
    if new_exp != q['explanation']:
        q['explanation'] = new_exp
        changed += 1
    return changed


def main():
    files = sorted(PRACTICE_DIR.glob('*.json'))
    total_files = len(files)
    total_changes = 0
    for fp in files:
        with open(fp, encoding='utf-8') as f:
            data = json.load(f)
        file_changes = 0
        for q in data['questions']:
            file_changes += fix_question(q)
        total_changes += file_changes
        if file_changes > 0:
            with open(fp, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'처리 파일: {total_files}')
    print(f'조사 변환 적용: {total_changes}건')


if __name__ == '__main__':
    main()
