#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GS N기(gs1/gs2/gs3) 문제를 단원(2a~8b)으로 분류 → (1) GS 단원 내 subchapter=단원id로
세팅(자체 단원 필터) + (2) 단원 chapter(2a~8b)에 추가(기존 단원 탭 통합).
사용: python3 scripts/gs_classify.py gs1
담보·경매·보상·정비는 '목적' 기준 분류(공시지가 등 method 논점이 아닌).
"""
import sys, json
from pathlib import Path
from collections import defaultdict, Counter

DATA = Path('viewer/public/data/essay/practice')
ORDER = ['2a', '3', '4', '5', '6a', '6b', '7', '8a', '8b']
TITLES = {'2a': '2a 3방식·기초', '3': '3 임대료·집합·복합', '4': '4 특수물건',
          '5': '5 투자·기업가치', '6a': '6a 토지보상', '6b': '6b 특수보상',
          '7': '7 영업·농업보상', '8a': '8a 담보·경매·소송', '8b': '8b 정비·표준지'}

CLASS = {
 'gs1': {
  '1-1': {1: '3', 2: '3', 3: '8a'},
  '1-2': {1: '2a', 2: '8a', 3: '2a', 4: '2a'},
  '2-1': {1: '3', 2: '3', 3: '3', 4: '3', 5: '3'},
  '2-2': {1: '3', 2: '3', 3: '3'},
  '3-1': {1: '5', 2: '4', 3: '4'},
  '3-2': {1: '3', 2: '3', 3: '4', 4: '3', 5: '3'},
  '4-1': {1: '3', 2: '8a', 3: '8a', 4: '8a'},
  '4-2': {1: '8a', 2: '2a', 3: '5', 4: '5', 5: '4'},
  '5-1': {1: '5', 2: '8a', 3: '5', 4: '2a'},
  '5-2': {1: '3', 2: '5', 3: '5', 4: '5'},
  '6-1': {1: '3', 2: '8a', 3: '5', 4: '3'},
  '6-2': {1: '3', 2: '4', 3: '3', 4: '2a'},
  '7-1': {1: '3', 2: '2a', 3: '6a', 4: '7'},
  '7-2': {1: '6a', 2: '6a', 3: '6b', 4: '6a'},
  '8-1': {1: '3', 2: '4', 3: '6b'},
  '8-2': {1: '6b', 2: '6b', 3: '6b', 4: '6b'},
  '9-1': {1: '6a', 2: '6a', 3: '6b', 4: '7'},
  '9-2': {1: '6a', 2: '6a', 3: '7', 4: '7', 5: '7'},
  '10-1': {1: '8b', 2: '8b', 3: '8b', 4: '8b'},
  '10-2': {1: '8a', 2: '2a', 3: '8a', 4: '4', 5: '5'},
 },
 'gs2': {
  '1-1': {1: '3', 2: '3', 3: '3'},
  '2-1': {1: '5', 2: '8b', 3: '3'},
  '3-1': {1: '6a', 2: '8a', 3: '4', 4: '8b'},
  '4-1': {1: '4', 2: '3', 3: '5', 4: '4'},
  '5-1': {1: '8a', 2: '8a', 3: '2a', 4: '5'},
  '6-1': {1: '8b', 2: '8b', 3: '8b', 4: '7'},
  '7-1': {1: '6a', 2: '4', 3: '6a', 4: '4'},
  '8-1': {1: '5', 2: '5', 3: '2a', 4: '8a'},
  '9-1': {1: '8b', 2: '8b', 3: '6a'},
  '10-1': {1: '7', 2: '6a', 3: '3'},
 },
}

chapter = sys.argv[1] if len(sys.argv) > 1 else 'gs1'
gsnum = chapter.replace('gs', '')
cmap = CLASS[chapter]

# ── (1) GS 단원 자체에 단원 태그 부여 ──
f = DATA / f'{chapter}.json'
d = json.loads(f.read_text(encoding='utf-8'))
miss = []
for q in d['questions']:
    tag = cmap.get(q['session'], {}).get(q['questionNum'])
    if not tag:
        miss.append((q['session'], q['questionNum'])); continue
    q['chapterTag'] = tag
    q['chapterTagTitle'] = TITLES[tag]
    q['subchapter'] = tag
assert not miss, f'미분류: {miss}'
f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')

# ── (2) 단원 chapter(2a~8b)에 추가 ──
def chap_entry(q, tag):
    return {
        'id': q['id'], 'subject': '감정평가실무', 'chapter': tag,
        'source': 'gs', 'gsRound': f'{gsnum}기', 'session': q['session'],
        'visionTranscribed': True, 'bodyFormat': 'markdown',
        'round': q['round'], 'questionNum': q['questionNum'], 'points': q['points'],
        'level': q['level'], 'difficulty': q['level'],
        'subchapter': f"GS{gsnum} {q['session']}", 'topic': q['topic'],
        'logicalPoints': q.get('logicalPoints', []), 'lawRefs': q.get('lawRefs', []),
        'body': q['body'], 'modelAnswer': q.get('modelAnswer', ''),
        'modelAnswerSource': q.get('modelAnswerSource', ''),
        'keyPoints': [], 'answerFormat': 'essay-narrative', 'sourcePdf': q.get('sourcePdf', ''),
    }

by_tag = defaultdict(list)
for q in d['questions']:
    by_tag[q['chapterTag']].append(chap_entry(q, q['chapterTag']))

affected = {}
for tag, items in by_tag.items():
    cf = DATA / f'{tag}.json'
    cd = json.loads(cf.read_text(encoding='utf-8'))
    newids = {it['id'] for it in items}
    keep = [x for x in cd['questions'] if x.get('id') not in newids]
    cd['questions'] = keep + items
    cd['count'] = len(cd['questions'])
    cd['withAnswer'] = sum(1 for x in cd['questions'] if x.get('modelAnswer'))
    cf.write_text(json.dumps(cd, ensure_ascii=False, indent=1), encoding='utf-8')
    affected[tag] = len(cd['questions'])

# ── manifest: GS 단원 subchapters + 단원 chapter count 갱신 ──
mf = DATA / 'manifest.json'
m = json.loads(mf.read_text(encoding='utf-8'))
cnt = Counter(q['subchapter'] for q in d['questions'])
gch = next(c for c in m['chapters'] if c['id'] == chapter)
gch['subchapters'] = [{'id': k, 'title': TITLES[k]} for k in ORDER if cnt.get(k)]
gch['tagCounts'] = {k: cnt[k] for k in ORDER if cnt.get(k)}
for ch in m['chapters']:
    if ch['id'] in affected:
        ch['count'] = affected[ch['id']] + ch.get('generatedCount', 0)
        ch['gsCount'] = ch.get('gsCount', 0)  # keep
m['total'] = sum(ch.get('count', 0) for ch in m['chapters'])
mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

print(f'{chapter} 단원 분류 + 단원탭 통합 완료:')
for k in ORDER:
    if cnt.get(k):
        print(f'  단원 {k:3s} {TITLES[k][3:]:16s}: +{cnt[k]:2d}문 (단원 총 {affected[k]})')
print(f'  합계 {sum(cnt.values())}문 / manifest total {m["total"]}')
