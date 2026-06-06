#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""5단계 연습문제(practice-set)를 논점별로 단원 chapter에 삽입.
한 문제씩 공들여 제작 → 이 라우터로 1건씩 추가(id-스코프 멱등).
객관식(ox/cloze/mcq/short)은 options·answer, 주관식(essay)은 modelAnswer.
해설은 lesson 레이어(정의·암기법·비교표·목차·채점키워드).
"""
import json
from pathlib import Path

DATA = Path('viewer/public/data/essay/practice')


def entry(p):
    return {
        'id': p['id'], 'subject': '감정평가실무', 'chapter': p['unit'],
        'source': 'practice-set', 'bodyFormat': 'markdown',
        'conceptNo': p.get('conceptNo', ''), 'conceptName': p.get('conceptName', ''),
        'topicId': p.get('topicId'), 'unitCode': p['unit'],
        'level': p['level'], 'difficulty': p['level'], 'format': p['format'],
        'points': p.get('points', 0),
        'subchapter': p.get('topicId') or f"연습 {p.get('conceptNo', '')} {p.get('conceptName', '')}".strip(),
        'topic': p.get('topic', p['conceptName']),
        'logicalPoints': p.get('logicalPoints', [p['conceptName']]),
        'lawRefs': p.get('lawRefs', []),
        'body': p['body'],
        'options': p.get('options', []),
        'answer': p.get('answer'),
        'modelAnswer': p.get('modelAnswer', ''),
        'lesson': p.get('lesson', {}),
        'refAnchors': p.get('refAnchors', []),   # 제작 시 참고한 기존 문제 id
        'keyPoints': [], 'answerFormat': 'practice',
        'sourcePdf': '자체제작(기출 역설계)',
    }


def route(problems):
    by_unit = {}
    for p in problems:
        by_unit.setdefault(p['unit'], []).append(p)
    for unit, items in by_unit.items():
        f = DATA / f'{unit}.json'
        d = json.loads(f.read_text(encoding='utf-8'))
        newids = {it['id'] for it in items}
        keep = [q for q in d['questions'] if q.get('id') not in newids]
        d['questions'] = keep + [entry(p) for p in items]
        d['count'] = len(d['questions'])
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')

    # manifest count = json + generatedCount
    mf = DATA / 'manifest.json'
    m = json.loads(mf.read_text(encoding='utf-8'))
    for ch in m['chapters']:
        if ch['id'] in by_unit:
            n = len(json.loads((DATA / f"{ch['id']}.json").read_text(encoding='utf-8'))['questions'])
            ch['count'] = n + ch.get('generatedCount', 0)
            ch['practiceCount'] = sum(1 for q in json.loads((DATA / f"{ch['id']}.json").read_text(encoding='utf-8'))['questions'] if q.get('source') == 'practice-set')
    m['total'] = sum(ch.get('count', 0) for ch in m['chapters'])
    mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

    for p in problems:
        tag = p.get('topicId') or p.get('conceptNo', '')
        print(f"  [{p['id']}] L{p['level']} {p['format']:5s} [{tag}] {p.get('conceptName', '')} ({p['unit']})")
    print(f"manifest total {m['total']}")
