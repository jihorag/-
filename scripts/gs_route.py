#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""실무 GS 1·2·3기 전사분을 gs1/gs2/gs3 단원으로 라우팅 (gs0_route 일반화).
문제 + 예시답안(modelAnswer) 모두. id-스코프 멱등. 각 problem의 'chapter'가 gs1/gs2/gs3.
"""
import json, datetime
from pathlib import Path

DATA = Path('viewer/public/data/essay/practice')
TITLES = {'gs1': '📗 실무 GS 1기 (20회분·예시답안)',
          'gs2': '📙 실무 GS 2기 (10회분·예시답안)',
          'gs3': '📕 실무 GS 3기 (10회분·예시답안)'}


def session_round(sess):
    a, b = sess.split('-')
    return int(a) * 100 + int(b)


def entry(p):
    return {
        'id': p['id'], 'subject': '감정평가실무', 'chapter': p['chapter'],
        'source': 'gs', 'gsRound': p['chapter'].replace('gs', '') + '기', 'session': p['session'],
        'visionTranscribed': True, 'bodyFormat': 'markdown',
        'round': session_round(p['session']), 'questionNum': p['questionNum'], 'points': p['points'],
        'level': p['level'], 'difficulty': p['level'],
        'subchapter': p.get('subchapter', p['session']), 'topic': p['topic'],
        'logicalPoints': p.get('logicalPoints', []), 'lawRefs': p.get('lawRefs', []),
        'body': p['body'], 'modelAnswer': p.get('modelAnswer', ''),
        'modelAnswerSource': 'gs-예시답안' if p.get('modelAnswer') else '',
        'keyPoints': [], 'answerFormat': 'essay-narrative',
        'sourcePdf': f"25년대비 실무{p['chapter'].replace('gs','')}기GS 문제 및 예시답안 모음",
    }


def route(problems):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    chapter = problems[0]['chapter']
    f = DATA / f'{chapter}.json'
    d = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {
        'built_at': now, 'chapter': chapter, 'chapterTitle': TITLES[chapter], 'questions': []}
    if not d.get('questions'):
        d['chapterTitle'] = TITLES[chapter]
    newids = {p['id'] for p in problems}
    keep = [q for q in d.get('questions', []) if q.get('id') not in newids]
    d['questions'] = keep + [entry(p) for p in problems]
    d['questions'].sort(key=lambda q: (q['round'], q['questionNum']))
    d['count'] = len(d['questions'])
    d['withAnswer'] = sum(1 for q in d['questions'] if q.get('modelAnswer'))
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')

    mf = DATA / 'manifest.json'
    m = json.loads(mf.read_text(encoding='utf-8'))
    ch = next((c for c in m['chapters'] if c['id'] == chapter), None)
    if not ch:
        ch = {'id': chapter, 'title': TITLES[chapter], 'file': f'{chapter}.json',
              'count': 0, 'withAnswer': 0, 'matchedAnswer': 0, 'rounds': [], 'generatedCount': 0, 'subchapters': []}
        m['chapters'].append(ch)
    ch['title'] = TITLES[chapter]
    ch['count'] = d['count']
    ch['withAnswer'] = d['withAnswer']
    ch['rounds'] = sorted({q['round'] for q in d['questions']})
    m['total'] = sum(c.get('count', 0) for c in m['chapters'])
    mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

    sess = sorted({p['session'] for p in problems})
    print(f"{chapter} 라우팅(세션 {sess}): {chapter} 총 {d['count']}문 (답안 {d['withAnswer']}) | total {m['total']}")
    for p in problems:
        print(f"  {p['session']}-{p['questionNum']}번 [{p['points']}점 L{p['level']}] {p['topic'][:30]}{' +답안' if p.get('modelAnswer') else ''}")
