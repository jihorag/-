#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""연습문제를 questions_db.json(정본)에 통합 후 sync-data로 chunk 자동 생성.

흐름:
  practice/economics/*.json → 변환 → questions_db.json(append) → sync-data.mjs → chunk
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE_DIR = ROOT / 'viewer/public/data/practice/economics'
QDB = ROOT / 'questions_db.json'
EXAM_NAME = '[연습문제]'


def convert(p, meta):
    return {
        'id': p['id'],
        'number': '',
        'period': 'practice',
        'year': '2026',
        'exam_date': '2026-05-31',
        'question': p['question'],
        'options': p['options'],
        'answer': p['answer'],
        'explanation': p['explanation'],
        'subject': meta['subject'],
        'tags': {
            'subject': meta['subject'],
            'is_practice': True,
            'difficulty': p['difficulty'],
            'question_type': p['question_type'],
            'system_note': 'practice-v1',
        },
        'exam': EXAM_NAME,
        'indexing_v4': {
            'difficulty': p['difficulty'],
            'mapped_taxonomy': {
                'subject': meta['subject'],
                'sub_subject': meta['sub_subject'],
                'chapter': meta['chapter'],
                'section': meta['section'],
                'item': meta['item'],
            },
            'needs_higher_ai': False,
            'reason': f'연습문제 v{meta["version"]} — {meta["item"]} 출제',
            # 'claude-sonnet-4-6'을 사용해야 manifest의 "classified" 통계에 포함되고
            # 앱 분류별 보기에서 정상 노출됨.
            'processed_by': 'claude-sonnet-4-6',
        },
        'indexing_v4_count': 1,
    }


def load_practice():
    qs = []
    if not PRACTICE_DIR.exists():
        return qs
    for fp in sorted(PRACTICE_DIR.glob('*.json')):
        with open(fp, encoding='utf-8') as f:
            data = json.load(f)
        meta = data.get('meta', {})
        for q in data.get('questions', []):
            qs.append(convert(q, meta))
        print(f'  practice loaded: {fp.name} ({len(data.get("questions",[]))}문제)')
    return qs


def merge_to_qdb(new_qs):
    """questions_db.json에서 기존 연습문제 제거 후 새 연습문제 추가."""
    with open(QDB, encoding='utf-8') as f:
        db = json.load(f)

    # 기존 연습문제 제거 (id가 'practice-' 시작하거나 exam이 [연습문제])
    before = len(db)
    db = [q for q in db if not (
        q.get('id', '').startswith('practice-') or q.get('exam') == EXAM_NAME
    )]
    removed = before - len(db)
    print(f'  removed {removed} prior practice questions from db')

    # 새 연습문제 추가
    db.extend(new_qs)
    print(f'  added {len(new_qs)} new practice questions')

    with open(QDB, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False)
    print(f'  questions_db.json: {len(db)} questions total')
    return db


def run_sync():
    """sync 실행 — node가 있으면 sync-data.mjs, 없으면 Python 재구현 사용."""
    # node 시도
    try:
        result = subprocess.run(
            ['node', 'scripts/sync-data.mjs'],
            cwd=ROOT / 'viewer',
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print(result.stdout)
            return True
    except FileNotFoundError:
        pass

    # Python 재구현 사용
    print('  node not found, using Python re-implementation')
    result = subprocess.run(
        ['python3', 'scripts/sync_data_py.py'],
        cwd=ROOT, capture_output=True, text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print('stderr:', result.stderr)
        return False
    return True


def main():
    print('=== 연습문제 → questions_db → app sync ===\n')
    print('[1/3] 연습문제 로드')
    practice_qs = load_practice()
    if not practice_qs:
        print('No practice questions found.')
        return
    print(f'\n[2/3] questions_db.json 통합')
    merge_to_qdb(practice_qs)
    print(f'\n[3/3] sync-data 실행 (chunk 자동 생성)')
    if run_sync():
        print('\n✅ 앱 반영 완료')
        print(f'   dev: http://localhost:5173 (npm run dev)')
        print(f'   build: npm run build')


if __name__ == '__main__':
    main()
