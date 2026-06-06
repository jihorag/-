#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GS 0기 77문제를 단원(2a~8b)으로 분류 → subchapter=단원id 설정 + manifest 단원목록.
앱의 'subchapter 필터' 기계를 재사용해 GS 0기를 단원별로 브라우징 가능하게 함.
담보·경매·보상·정비처럼 '목적'이 단원을 정하는 문제는 topic 기준으로 분류.
"""
import json
from pathlib import Path
from collections import Counter

DATA = Path('viewer/public/data/essay/practice')

ORDER = ['2a', '3', '4', '5', '6a', '6b', '7', '8a', '8b']
TITLES = {
    '2a': '2a 3방식·기초', '3': '3 임대료·집합·복합', '4': '4 특수물건',
    '5': '5 투자·기업가치', '6a': '6a 토지보상', '6b': '6b 특수보상',
    '7': '7 영업·농업보상', '8a': '8a 담보·경매·소송', '8b': '8b 정비·표준지',
}

# session → {questionNum: 단원} (topic 기준 분류)
CLASS = {
    '1-1': {1: '2a', 2: '2a', 3: '2a', 4: '2a', 5: '2a'},
    '1-2': {1: '2a', 2: '2a', 3: '2a', 4: '2a'},
    '2-1': {1: '2a', 2: '5', 3: '3', 4: '2a'},
    '2-2': {1: '2a', 2: '2a', 3: '3', 4: '3', 5: '2a'},
    '3-1': {1: '3', 2: '3', 3: '3'},
    '3-2': {1: '2a', 2: '3', 3: '2a', 4: '3'},
    '4-1': {1: '3', 2: '3', 3: '3'},
    '4-2': {1: '4', 2: '3', 3: '2a', 4: '4', 5: '2a'},
    '5-1': {1: '4', 2: '4', 3: '4', 4: '2a'},
    '5-2': {1: '5', 2: '5', 3: '5', 4: '2a'},
    '6-1': {1: '5', 2: '5', 3: '4', 4: '3'},
    '6-2': {1: '5', 2: '3', 3: '5', 4: '2a'},
    '7-1': {1: '6a', 2: '4', 3: '6a', 4: '2a'},
    '7-2': {1: '3', 2: '4', 3: '6a', 4: '5'},
    '8-1': {1: '6a', 2: '6a', 3: '4', 4: '6a'},
    '8-2': {1: '6a', 2: '7', 3: '3'},
    '9-1': {1: '6b', 2: '6a', 3: '4'},
    '9-2': {1: '6b', 2: '6a', 3: '8a', 4: '6a'},
    '10-1': {1: '8b', 2: '8b', 3: '6b'},
    '10-2': {1: '8a', 2: '8a', 3: '8a'},
}

f = DATA / 'gs0.json'
d = json.loads(f.read_text(encoding='utf-8'))
miss = []
for q in d['questions']:
    tag = CLASS.get(q['session'], {}).get(q['questionNum'])
    if not tag:
        miss.append((q['session'], q['questionNum'])); continue
    q['chapterTag'] = tag                     # 단원 id (별도 보존)
    q['chapterTagTitle'] = TITLES[tag]
    q['subchapter'] = tag                     # 앱 필터가 사용하는 키
assert not miss, f'미분류: {miss}'
d['count'] = len(d['questions'])
f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')

# manifest: gs0 단원 목록(subchapters) 세팅
mf = DATA / 'manifest.json'
m = json.loads(mf.read_text(encoding='utf-8'))
cnt = Counter(q['subchapter'] for q in d['questions'])
ch = next(c for c in m['chapters'] if c['id'] == 'gs0')
ch['subchapters'] = [{'id': k, 'title': TITLES[k]} for k in ORDER if cnt.get(k)]
ch['tagCounts'] = {k: cnt[k] for k in ORDER if cnt.get(k)}
mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

print('GS 0기 단원 분류 완료 (subchapter=단원id):')
for k in ORDER:
    if cnt.get(k):
        print(f'  {TITLES[k]:22s} : {cnt[k]:2d}문')
print(f'  합계 {sum(cnt.values())}문 / 단원 {len([k for k in ORDER if cnt.get(k)])}개')
