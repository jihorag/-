#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""연습문제 ↔ AI 학습 토픽 연결 (호응).
1) 연습문제에 topicId(2a-1 등)·unitCode 부여 + subchapter=topicId (EssayMode 필터 일치).
2) essay manifest의 단원 subchapters를 AI 학습 목차 토픽으로 동기화(칩 제목 일치).
3) practice_index.json 생성: AI 학습이 '이 토픽 연습문제'를 바로 찾도록 topicId→문항 인덱스.
"""
import json
from pathlib import Path
from collections import defaultdict

ESSAY = Path('viewer/public/data/essay/practice')
STUDY = Path('viewer/public/data/study/appraisal_practice')

ai = json.loads((STUDY / 'ai_index.json').read_text(encoding='utf-8'))
# 토픽 마스터: topicId -> (title, unitCode)
TOPIC = {}
UNIT_TOPICS = defaultdict(list)
for u in ai['units']:
    for t in u.get('topics', []):
        TOPIC[t['id']] = (t['title'], u['code'])
        UNIT_TOPICS[u['code']].append({'id': t['id'], 'title': t['title']})


def topic_of(q):
    """연습문제 → topicId (키워드 규칙). 현재 단원 2a(공시지가기준법)만 채워짐."""
    t = q.get('topic', '') + ' ' + ' '.join(q.get('logicalPoints', []))
    u = q.get('chapter', '')
    if u == '2a':
        if any(k in t for k in ['시점수정', '지가변동률']): return '2a-3'
        if '지역요인' in t: return '2a-4'
        if any(k in t for k in ['개별요인', '평점', '상승식', '총화식']): return '2a-5'
        if any(k in t for k in ['그 밖의 요인', '그밖요인', '격차율']): return '2a-6'
        if any(k in t for k in ['선정', '배제', '인근지역', '유사지역', '동일수급권']): return '2a-2'
        if '거래사례' in t: return '2a-7'
        return '2a-1'
    return f'{u}-1'  # 타 단원은 추후 세분


# ── 1) 연습문제 태깅 + 2) manifest subchapters 동기화 ──
mani = json.loads((ESSAY / 'manifest.json').read_text(encoding='utf-8'))
index = defaultdict(lambda: defaultdict(list))  # topicId -> level -> [ids]
touched_units = set()

for ch in mani['chapters']:
    cid = ch['id']
    f = ESSAY / f'{cid}.json'
    if not f.exists():
        continue
    if cid == 'cleanup':
        continue  # 옛 폐기 자체제작은 제외
    d = json.loads(f.read_text(encoding='utf-8'))
    changed = False
    for q in d['questions']:
        if q.get('source') != 'practice-set':
            continue
        if not q.get('conceptNo'):
            continue  # 정성 제작(conceptNo 보유)만 토픽 연결
        tid = topic_of(q)
        q['topicId'] = tid
        q['unitCode'] = cid
        q['subchapter'] = tid          # EssayMode subchapter 필터가 토픽과 일치
        index[tid][q['level']].append(q['id'])
        touched_units.add(cid)
        changed = True
    if changed:
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    # manifest subchapters = AI 학습 토픽 (해당 단원)
    if cid in UNIT_TOPICS:
        ch['subchapters'] = UNIT_TOPICS[cid]

(ESSAY / 'manifest.json').write_text(json.dumps(mani, ensure_ascii=False, indent=1), encoding='utf-8')

# ── 3) practice_index.json (AI 학습용 토픽→연습문제 인덱스) ──
out = {'subject': 'appraisal_practice', 'source': 'essay/practice (practice-set)',
       'note': 'AI 학습 토픽별 연습문제 인덱스. EssayMode 데이터(2a.json 등)에 source=practice-set로 존재.',
       'topics': {}}
for tid in sorted(index):
    levels = {str(lv): sorted(index[tid][lv]) for lv in sorted(index[tid])}
    counts = {str(lv): len(index[tid][lv]) for lv in sorted(index[tid])}
    out['topics'][tid] = {
        'title': TOPIC.get(tid, (tid, ''))[0], 'unitCode': TOPIC.get(tid, ('', ''))[1],
        'total': sum(counts.values()), 'countsByLevel': counts, 'idsByLevel': levels,
        'essayChapter': TOPIC.get(tid, ('', tid.split('-')[0]))[1] or tid.split('-')[0],
    }
(STUDY / 'practice_index.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')

print('연습문제↔토픽 연결 완료:')
for tid in sorted(out['topics']):
    ti = out['topics'][tid]
    print(f"  {tid:6s} {ti['title'][:22]:24s} 총 {ti['total']:3d}  {ti['countsByLevel']}")
print(f"touched units: {sorted(touched_units)}  → practice_index.json 생성")
