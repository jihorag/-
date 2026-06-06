#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""문제풀이(essay) 단원을 AI 학습 11단원/68토픽과 일치시킴 (가 옵션).
- '1 기초'·'2b 수익환원·임대' 단원 신설(빈 파일) → 단원 지도 일치, 딥링크 빈화면 해소.
- 11개 핵심 단원의 title·subchapters를 AI 목차와 동기화.
- 기출/GS는 현 단원 그대로 유지(재분류는 연습문제 완료 후 결정).
"""
import json
from pathlib import Path

ESSAY = Path('viewer/public/data/essay/practice')
ai = json.loads((Path('viewer/public/data/study/appraisal_practice') / 'ai_index.json').read_text(encoding='utf-8'))

# AI 단원 → title, subchapters(토픽)
AIUNIT = {}
for u in ai['units']:
    AIUNIT[u['code']] = {
        'title': u['title'],
        'subchapters': [{'id': t['id'], 'title': t['title']} for t in u.get('topics', [])],
    }
CORE = ['1', '2a', '2b', '3', '4', '5', '6a', '6b', '7', '8a', '8b']

m = json.loads((ESSAY / 'manifest.json').read_text(encoding='utf-8'))
by_id = {c['id']: c for c in m['chapters']}

for code in CORE:
    info = AIUNIT[code]
    if code not in by_id:
        # 신설 단원 (1, 2b) — 빈 파일 + manifest 엔트리
        f = ESSAY / f'{code}.json'
        if not f.exists():
            f.write_text(json.dumps({'subject': '감정평가실무', 'chapter': code,
                                     'chapterTitle': info['title'], 'questions': [], 'count': 0},
                                    ensure_ascii=False, indent=1), encoding='utf-8')
        ch = {'id': code, 'title': info['title'], 'file': f'{code}.json',
              'count': 0, 'withAnswer': 0, 'generatedCount': 0, 'subchapters': info['subchapters'],
              'aiUnit': True}
        m['chapters'].append(ch)
        by_id[code] = ch
        print(f'  + 신설 단원 {code}: {info["title"]}')
    else:
        ch = by_id[code]
        ch['title'] = info['title']               # 제목 AI와 일치
        ch['subchapters'] = info['subchapters']    # 토픽 칩 AI와 일치
        ch['aiUnit'] = True
        print(f'  · 동기화 {code}: {info["title"]} (토픽 {len(info["subchapters"])})')

# 핵심 11단원 순서를 AI 순서로 정렬(나머지 gs/kichul 등은 뒤로)
order = {c: i for i, c in enumerate(CORE)}
m['chapters'].sort(key=lambda c: (order.get(c['id'], 99), c['id']))
m['total'] = sum(c.get('count', 0) for c in m['chapters'])
(ESSAY / 'manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'\n핵심 11단원 정렬 완료. manifest total {m["total"]}. 기출/GS 단원은 그대로 유지.')
