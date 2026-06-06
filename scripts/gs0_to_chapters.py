#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GS 0기 77문제를 chapterTag(단원)에 따라 단원 chapter(2a~8b).json에 추가
→ 기존 단원 탭에서 기출과 함께 보이게 함. id-스코프 멱등(gs0-* 재실행 안전).
gs0.json(회차별 모의고사 뷰)은 그대로 유지 — 동일 id로 양쪽에서 보임.
"""
import json
from pathlib import Path
from collections import defaultdict

DATA = Path('viewer/public/data/essay/practice')


def chap_entry(q, tag):
    return {
        'id': q['id'], 'subject': '감정평가실무', 'chapter': tag,
        'source': 'gs', 'gsRound': '0기', 'session': q['session'],
        'visionTranscribed': True, 'bodyFormat': 'markdown',
        'round': q['round'], 'questionNum': q['questionNum'], 'points': q['points'],
        'level': q['level'], 'difficulty': q['level'],
        'subchapter': f"GS0 {q['session']}", 'topic': q['topic'],
        'logicalPoints': q.get('logicalPoints', []), 'lawRefs': q.get('lawRefs', []),
        'body': q['body'], 'modelAnswer': q.get('modelAnswer', ''),
        'modelAnswerSource': q.get('modelAnswerSource', 'gs-예시답안'),
        'keyPoints': [], 'answerFormat': 'essay-narrative', 'sourcePdf': q.get('sourcePdf', ''),
    }


gs0 = json.loads((DATA / 'gs0.json').read_text(encoding='utf-8'))
by_tag = defaultdict(list)
for q in gs0['questions']:
    by_tag[q['chapterTag']].append(chap_entry(q, q['chapterTag']))

affected = {}
for tag, items in by_tag.items():
    f = DATA / f'{tag}.json'
    d = json.loads(f.read_text(encoding='utf-8'))
    newids = {it['id'] for it in items}
    keep = [x for x in d['questions'] if x.get('id') not in newids]  # gs0-* 제거 후 재삽입(멱등)
    d['questions'] = keep + items
    d['count'] = len(d['questions'])
    d['withAnswer'] = sum(1 for x in d['questions'] if x.get('modelAnswer'))
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    affected[tag] = len(d['questions'])

# manifest: 영향 단원 count = json문항 + generatedCount
m = json.loads((DATA / 'manifest.json').read_text(encoding='utf-8'))
for ch in m['chapters']:
    if ch['id'] in affected:
        ch['count'] = affected[ch['id']] + ch.get('generatedCount', 0)
        ch['gsCount'] = sum(1 for t, items in by_tag.items() if t == ch['id'] for _ in items)
m['total'] = sum(ch.get('count', 0) for ch in m['chapters'])
(DATA / 'manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

print('GS 0기 → 단원 chapter 추가 완료:')
for t in ['2a', '3', '4', '5', '6a', '6b', '7', '8a', '8b']:
    if t in by_tag:
        print(f'  단원 {t:3s}: +{len(by_tag[t]):2d}문 (단원 총 {affected[t]}문)')
print(f'  manifest total {m["total"]}')
