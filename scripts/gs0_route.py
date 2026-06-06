#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""실무 GS 0기 전사분을 'gs0' 단원(모의고사)으로 라우팅. 기출(단원 분산)과 달리 GS는 단독 단원.
문제 + 예시답안(modelAnswer) 모두 담음. id-스코프 멱등.
"""
import json, datetime
from pathlib import Path

DATA = Path('viewer/public/data/essay/practice')


def session_round(sess):
    """'3-2' → 302 (정렬용)."""
    a, b = sess.split('-')
    return int(a) * 100 + int(b)


def entry(p):
    return {
        'id': p['id'], 'subject': '감정평가실무', 'chapter': 'gs0',
        'source': 'gs', 'gsRound': '0기', 'session': p['session'],
        'visionTranscribed': True, 'bodyFormat': 'markdown',
        'round': session_round(p['session']), 'questionNum': p['questionNum'], 'points': p['points'],
        'level': p['level'], 'difficulty': p['level'],
        'subchapter': p.get('subchapter', p['session']), 'topic': p['topic'],
        'logicalPoints': p.get('logicalPoints', []), 'lawRefs': p.get('lawRefs', []),
        'body': p['body'], 'modelAnswer': p.get('modelAnswer', ''),
        'modelAnswerSource': 'gs-예시답안' if p.get('modelAnswer') else '',
        'keyPoints': [], 'answerFormat': 'essay-narrative',
        'sourcePdf': '25년대비 실무0기GS 문제 및 예시답안 모음 [총20회분]',
    }


def route(problems):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    f = DATA / 'gs0.json'
    d = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {
        'built_at': now, 'chapter': 'gs0', 'chapterTitle': '📘 실무 GS 0기 (20회분·예시답안)', 'questions': []}
    newids = {p['id'] for p in problems}
    keep = [q for q in d.get('questions', []) if q.get('id') not in newids]
    d['questions'] = keep + [entry(p) for p in problems]
    d['questions'].sort(key=lambda q: (q['round'], q['questionNum']))
    d['count'] = len(d['questions'])
    d['withAnswer'] = sum(1 for q in d['questions'] if q.get('modelAnswer'))
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')

    # manifest: gs0 단원 추가/갱신
    mf = DATA / 'manifest.json'
    m = json.loads(mf.read_text(encoding='utf-8'))
    ch = next((c for c in m['chapters'] if c['id'] == 'gs0'), None)
    if not ch:
        ch = {'id': 'gs0', 'title': '📘 실무 GS 0기 (20회분·예시답안)', 'file': 'gs0.json',
              'count': 0, 'withAnswer': 0, 'matchedAnswer': 0, 'rounds': [], 'generatedCount': 0, 'subchapters': []}
        m['chapters'].append(ch)
    ch['count'] = d['count']
    ch['withAnswer'] = d['withAnswer']
    ch['rounds'] = sorted({q['round'] for q in d['questions']})
    m['total'] = sum(c.get('count', 0) for c in m['chapters'])
    mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

    sess = sorted({p['session'] for p in problems})
    print(f"GS0기 라우팅(세션 {sess}): gs0 총 {d['count']}문 (답안보유 {d['withAnswer']}) | manifest total {m['total']}")
    for p in problems:
        print(f"  {p['session']}-{p['questionNum']}번 [{p['points']}점 L{p['level']}] {p['topic'][:34]}{' +답안' if p.get('modelAnswer') else ''}")
