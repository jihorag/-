#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GS 3기 마무리: (1) 중복 제거(session,questionNum 기준 — 답안 긴 것 유지)
(2) 단원 분류(chapterTag·subchapter) (3) 단원 chapter에서 3기 전부 제거 후 재통합.
병렬 라우팅으로 생긴 중복을 청소하고 단원탭 통합까지 완료.
"""
import json
from pathlib import Path
from collections import Counter

DATA = Path('viewer/public/data/essay/practice')
ORDER = ['2a', '3', '4', '5', '6a', '6b', '7', '8a', '8b']
TITLES = {'2a': '2a 3방식·기초', '3': '3 임대료·집합·복합', '4': '4 특수물건',
          '5': '5 투자·기업가치', '6a': '6a 토지보상', '6b': '6b 특수보상',
          '7': '7 영업·농업보상', '8a': '8a 담보·경매·소송', '8b': '8b 정비·표준지'}

CLASS = {
 '1-1': {1: '5', 2: '5', 3: '3', 4: '4'},
 '2-1': {1: '5', 2: '4', 3: '3', 4: '2a'},
 '3-1': {1: '3', 2: '5', 3: '6b', 4: '3'},
 '4-1': {1: '4', 2: '3', 3: '5', 4: '2a'},
 '5-1': {1: '8a', 2: '5', 3: '5'},
 '6-1': {1: '3', 2: '6a', 3: '2a', 4: '5'},
 '7-1': {1: '2a', 2: '6a', 3: '8a', 4: '8b'},
 '8-1': {1: '4', 2: '8a', 3: '3', 4: '5'},
 '9-1': {1: '6a', 2: '4', 3: '6a', 4: '7'},
 '10-1': {1: '3', 2: '2a', 3: '7', 4: '4'},
}

# (1) dedup
f = DATA / 'gs3.json'
d = json.loads(f.read_text(encoding='utf-8'))
best = {}
for q in d['questions']:
    k = (q['session'], q['questionNum'])
    if k not in best or len(q.get('modelAnswer', '')) > len(best[k].get('modelAnswer', '')):
        best[k] = q
qs = list(best.values())

# (2) classify
miss = []
for q in qs:
    tag = CLASS.get(q['session'], {}).get(q['questionNum'])
    if not tag:
        miss.append((q['session'], q['questionNum'])); continue
    q['chapterTag'] = tag
    q['chapterTagTitle'] = TITLES[tag]
    q['subchapter'] = tag
assert not miss, f'미분류: {miss}'
qs.sort(key=lambda q: (q['round'], q['questionNum']))
d['questions'] = qs
d['count'] = len(qs)
d['withAnswer'] = sum(1 for q in qs if q.get('modelAnswer'))
f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')

# (3) 단원 chapter에서 3기 전부 제거 후 재통합
def chap_entry(q, tag):
    return {'id': q['id'], 'subject': '감정평가실무', 'chapter': tag,
            'source': 'gs', 'gsRound': '3기', 'session': q['session'],
            'visionTranscribed': True, 'bodyFormat': 'markdown',
            'round': q['round'], 'questionNum': q['questionNum'], 'points': q['points'],
            'level': q['level'], 'difficulty': q['level'],
            'subchapter': f"GS3 {q['session']}", 'topic': q['topic'],
            'logicalPoints': q.get('logicalPoints', []), 'lawRefs': q.get('lawRefs', []),
            'body': q['body'], 'modelAnswer': q.get('modelAnswer', ''),
            'modelAnswerSource': q.get('modelAnswerSource', ''),
            'keyPoints': [], 'answerFormat': 'essay-narrative', 'sourcePdf': q.get('sourcePdf', '')}

bytag = {}
for q in qs:
    bytag.setdefault(q['chapterTag'], []).append(q)

affected = {}
for tag in ORDER:
    cf = DATA / f'{tag}.json'
    cd = json.loads(cf.read_text(encoding='utf-8'))
    cleaned = [x for x in cd['questions'] if x.get('gsRound') != '3기']  # 3기 전부 제거
    if tag in bytag:
        cleaned += [chap_entry(q, tag) for q in bytag[tag]]
    cd['questions'] = cleaned
    cd['count'] = len(cleaned)
    cd['withAnswer'] = sum(1 for x in cleaned if x.get('modelAnswer'))
    cf.write_text(json.dumps(cd, ensure_ascii=False, indent=1), encoding='utf-8')
    affected[tag] = len(cleaned)

# manifest
mf = DATA / 'manifest.json'
m = json.loads(mf.read_text(encoding='utf-8'))
cnt = Counter(q['subchapter'] for q in qs)
gch = next((c for c in m['chapters'] if c['id'] == 'gs3'), None)
if gch:
    gch['subchapters'] = [{'id': k, 'title': TITLES[k]} for k in ORDER if cnt.get(k)]
    gch['tagCounts'] = {k: cnt[k] for k in ORDER if cnt.get(k)}
    gch['count'] = d['count']
    gch['withAnswer'] = d['withAnswer']
for ch in m['chapters']:
    if ch['id'] in affected:
        ch['count'] = affected[ch['id']] + ch.get('generatedCount', 0)
m['total'] = sum(ch.get('count', 0) for ch in m['chapters'])
mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

print(f'GS3 정리완료: {d["count"]}문(답안 {d["withAnswer"]}), 중복제거 {len(d["questions"])}←원본')
for k in ORDER:
    if cnt.get(k):
        print(f'  단원 {k:3s}: GS3 {cnt[k]:2d}문 (단원 총 {affected[k]})')
print(f'  manifest total {m["total"]}')
