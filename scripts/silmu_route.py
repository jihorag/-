#!/usr/bin/env python3
"""실무 기출 전사분을 단원별로 분류·라우팅하는 공유 모듈.
id-스코프 멱등: 같은 id만 교체하고 다른 회차/문제는 보존(여러 회차가 같은 단원을 써도 안전).
"""
import json, datetime
from pathlib import Path
from collections import defaultdict

DATA = Path('viewer/public/data/essay/practice')


def entry(p):
    return {
        'id': p['id'], 'subject': '감정평가실무', 'chapter': p['chapter'],
        'source': 'official', 'visionTranscribed': True, 'bodyFormat': 'markdown',
        'round': p['round'], 'questionNum': p['questionNum'], 'points': p['points'],
        'level': p['level'], 'difficulty': p['level'],
        'subchapter': p['subchapter'], 'topic': p['topic'],
        'logicalPoints': p.get('logicalPoints', []), 'lawRefs': p.get('lawRefs', []),
        'body': p['body'], 'modelAnswer': '', 'modelAnswerSource': '',
        'keyPoints': [], 'answerFormat': 'essay-narrative',
        'sourcePdf': '감정평가실무_기출문제지 [1-36회]',
    }


def route(problems):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    by_ch = defaultdict(list)
    for p in problems:
        by_ch[p['chapter']].append(entry(p))

    affected = {}
    for ch, items in by_ch.items():
        f = DATA / f'{ch}.json'
        d = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {
            'subject': '감정평가실무', 'chapter': ch, 'questions': []}
        newids = {it['id'] for it in items}
        keep = [q for q in d.get('questions', []) if q.get('id') not in newids]  # id-스코프(타 회차 보존)
        d['questions'] = keep + items
        d['count'] = len(d['questions'])
        d['withAnswer'] = sum(1 for q in d['questions'] if q.get('modelAnswer'))
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
        affected[ch] = len(d['questions'])

    # manifest: 영향 단원 count(기출+generated) 재계산
    m = json.loads((DATA / 'manifest.json').read_text(encoding='utf-8'))
    for ch in m['chapters']:
        cid = ch['id']
        if cid in affected:
            ch['count'] = affected[cid] + ch.get('generatedCount', 0)
    m['total'] = sum(ch.get('count', 0) for ch in m['chapters'])
    (DATA / 'manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

    rounds = sorted({p['round'] for p in problems})
    print(f"전사+분류 라우팅(회차 {rounds}): {dict(affected)} | manifest total {m['total']}")
    for p in problems:
        print(f"  {p['round']}회-{p['questionNum']} → 단원 {p['chapter']}({p['subchapter']}) L{p['level']} · {p['topic'][:28]}")
