#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""연습문제 JSON을 앱의 exam chunk 형식으로 변환·통합."""
import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
PRACTICE_DIR = ROOT / 'viewer/public/data/practice/economics'
EXAMS_DIR = ROOT / 'viewer/public/data/exams'
MANIFEST_PATH = ROOT / 'viewer/public/data/manifest.json'

# 연습문제 → 13.json
TARGET_FILE = '13.json'
EXAM_NAME = '[연습문제]'


def convert_practice_question(p, meta, seq):
    """연습문제 한 문제를 questions_db 호환 형식으로 변환."""
    return {
        'id': p['id'],
        'number': str(seq),
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
            'processed_by': 'practice-v1',
        },
        'indexing_v4_count': 1,
    }


def load_practice_files():
    """practice/economics/ 하위 모든 JSON 로드."""
    qs = []
    if not PRACTICE_DIR.exists():
        print(f'No practice dir: {PRACTICE_DIR}')
        return qs

    seq = 1
    for fp in sorted(PRACTICE_DIR.glob('*.json')):
        with open(fp, encoding='utf-8') as f:
            data = json.load(f)
        meta = data.get('meta', {})
        for q in data.get('questions', []):
            converted = convert_practice_question(q, meta, seq)
            qs.append(converted)
            seq += 1
        print(f'  loaded {fp.name}: {len(data.get("questions", []))} questions')

    return qs


def write_chunk(qs):
    """13.json에 기록."""
    EXAMS_DIR.mkdir(parents=True, exist_ok=True)
    target = EXAMS_DIR / TARGET_FILE
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)
    size = target.stat().st_size
    print(f'\nWrote {target.name}: {len(qs)} qs, {size} bytes')
    return size


def update_manifest(count, size):
    """manifest.json에 [연습문제] exam 등록."""
    with open(MANIFEST_PATH, encoding='utf-8') as f:
        m = json.load(f)

    # 기존 [연습문제] 엔트리 제거 (있으면 갱신)
    m['exams'] = [e for e in m['exams'] if e['name'] != EXAM_NAME]

    # 새 엔트리 추가
    m['exams'].append({
        'name': EXAM_NAME,
        'file': TARGET_FILE,
        'count': count,
        'classified': count,
        'years': ['2026'],
        'sizeBytes': size,
    })

    # 정렬: 파일명 순서대로
    m['exams'].sort(key=lambda e: e['file'])

    # total/classified 재산정
    m['total'] = sum(e['count'] for e in m['exams'])
    m['classified'] = sum(e['classified'] for e in m['exams'])
    m['built_at'] = datetime.now(timezone.utc).isoformat()

    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    print(f'\nUpdated manifest.json:')
    print(f'  [연습문제] {count}문제 등록 ({TARGET_FILE})')
    print(f'  Total: {m["total"]}, Classified: {m["classified"]}')


def main():
    print('=== 연습문제 → 앱 통합 ===\n')
    qs = load_practice_files()
    if not qs:
        print('No practice questions found.')
        return
    size = write_chunk(qs)
    update_manifest(len(qs), size)
    print('\n✅ 앱 반영 완료')


if __name__ == '__main__':
    main()
