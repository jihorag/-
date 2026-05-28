#!/usr/bin/env python3
"""본문에서 markdown ** bold ** 문법만 제거 (헤더 ##, 표, 리스트는 보존)."""
import json
import re
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')

# **text** → text (단순 제거)
BOLD_RE = re.compile(r'\*\*([^*\n]+?)\*\*')


def strip_bold(text):
    if not text or '**' not in text:
        return text, 0
    new_text, n = BOLD_RE.subn(r'\1', text)
    return new_text, n


def main():
    total_files = 0
    total_questions = 0
    total_replacements = 0
    for fp in sorted(DATA_DIR.glob('*.json')):
        if fp.name == 'manifest.json':
            continue
        d = json.loads(fp.read_text(encoding='utf-8'))
        if 'questions' not in d:
            continue
        modified_count = 0
        repl_count = 0
        for q in d['questions']:
            if 'body' in q:
                new_body, n = strip_bold(q['body'])
                if n > 0:
                    q['body'] = new_body
                    modified_count += 1
                    repl_count += n
        if modified_count:
            fp.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
            print(f'{fp.name:18}  문제 {modified_count:>3}개  ** 제거 {repl_count:>5}회')
            total_files += 1
            total_questions += modified_count
            total_replacements += repl_count
    print(f'\n총: 파일 {total_files}개 / 문제 {total_questions}개 / ** 제거 {total_replacements}회')


if __name__ == '__main__':
    main()
