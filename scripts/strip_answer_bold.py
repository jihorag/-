#!/usr/bin/env python3
"""모범답안에서 markdown ** bold ** 제거."""
import json
import re
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')
BOLD_RE = re.compile(r'\*\*([^*\n]+?)\*\*')


def strip_bold(text):
    if not text or '**' not in text:
        return text, 0
    return BOLD_RE.subn(r'\1', text)


def main():
    total_q = 0
    total_repl = 0
    for fp in sorted(DATA_DIR.glob('*.json')):
        if fp.name == 'manifest.json':
            continue
        d = json.loads(fp.read_text(encoding='utf-8'))
        if 'questions' not in d:
            continue
        mod = 0
        repl = 0
        for q in d['questions']:
            if q.get('modelAnswer'):
                new, n = strip_bold(q['modelAnswer'])
                if n > 0:
                    q['modelAnswer'] = new
                    mod += 1
                    repl += n
        if mod:
            fp.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
            print(f'{fp.name:18}  답안 {mod:>3}개  ** 제거 {repl:>5}회')
            total_q += mod
            total_repl += repl
    print(f'\n총: 답안 {total_q}개 / ** 제거 {total_repl}회')


if __name__ == '__main__':
    main()
