#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2차 essay 목차를 AI 학습 목차(ai_index.json units/topics)와 정확히 일치시킨다.

대상: 이론(theory)·법규(law). 실무(practice)는 이미 AI topic과 동일(id·title)이라 제외.

Phase A(이 스크립트): manifest 목차 구조만 정렬 — 원본 문제 파일은 건드리지 않음.
  - chapter.title  = AI unit.title (정확히)
  - chapter.subchapters = AI unit.topics (id를 essay 형식 "{chId}-{n}"으로, title 그대로)
  - chapter.aiUnit=True, chapter.aiCode=unit.code (EssayMode 표시·필터용)

문제의 subchapter 재태깅은 Phase B(classify_essay_subchapter.py)에서 로컬 LLM으로.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS = {  # essay 과목 dir → AI study id
    'theory': 'appraisal_theory',
    'law': 'appraisal_law',
}


def essay_sub_id(ch_id, topic_id):
    """AI topic id '01-3' → essay subchapter id '{ch_id}-3'."""
    suffix = topic_id.split('-', 1)[1] if '-' in topic_id else topic_id
    return f'{ch_id}-{suffix}'


def main():
    for essay_key, ai_id in PAIRS.items():
        ai = json.load(open(ROOT / f'viewer/public/data/study/{ai_id}/ai_index.json', encoding='utf-8'))
        units_by_code = {}
        for u in ai.get('units', []):
            try:
                units_by_code[int(u['code'])] = u  # '01' → 1
            except (ValueError, TypeError):
                units_by_code[u['code']] = u

        mf_path = ROOT / f'viewer/public/data/essay/{essay_key}/manifest.json'
        m = json.load(open(mf_path, encoding='utf-8'))

        aligned = 0
        for ch in m['chapters']:
            try:
                key = int(ch['id'])
            except (ValueError, TypeError):
                continue  # 숫자 아닌 특수 단원(gs/past 등) 건너뜀
            u = units_by_code.get(key)
            if not u:
                continue
            ch['title'] = u['title']
            ch['aiUnit'] = True
            ch['aiCode'] = u['code']
            ch['subchapters'] = [
                {'id': essay_sub_id(ch['id'], t['id']), 'title': t['title'],
                 'aiTopicId': t['id'], 'keywords': []}
                for t in u.get('topics', [])
            ]
            aligned += 1

        # chapter 순서를 AI unit 순서대로 (핵심 단원 먼저, 나머지 뒤)
        def sort_key(ch):
            try:
                return (0, int(ch['id']))
            except (ValueError, TypeError):
                return (1, 0)
        m['chapters'].sort(key=sort_key)

        bak = mf_path.with_suffix('.json.bak-align')
        if not bak.exists():
            bak.write_bytes(mf_path.read_bytes())
        json.dump(m, open(mf_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        total_sub = sum(len(c.get('subchapters', [])) for c in m['chapters'] if c.get('aiUnit'))
        print(f'{essay_key}: {aligned}개 단원 정렬, 세부단원 {total_sub}개 (AI topics와 일치)')


if __name__ == '__main__':
    main()
