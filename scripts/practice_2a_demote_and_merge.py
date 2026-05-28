#!/usr/bin/env python3
"""단원 2a 정비 — (1) 짧은 표준+를 입문·기초로 강등, (2) AI 신규를 practice-set으로 통합."""
import json
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')


def demote_short(q):
    """본문 길이 기준 난이도·점수 재할당. 긴 문제는 손대지 않음."""
    body_len = len(q.get('body', ''))
    if q.get('source') != 'practice-set':
        return False
    if q.get('difficulty', 0) < 3:
        return False  # 이미 입문·기초는 그대로
    changed = False
    if body_len < 120:
        if q.get('difficulty') != 1:
            q['difficulty'] = 1
            changed = True
        if q.get('points', 0) > 10:
            q['points'] = 5
            changed = True
    elif body_len < 220:
        if q.get('difficulty') != 2:
            q['difficulty'] = 2
            changed = True
        if q.get('points', 0) > 15:
            q['points'] = 10
            changed = True
    elif body_len < 350:
        # 짧은 표준 → 기초 유지
        if q.get('difficulty') != 2:
            q['difficulty'] = 2
            changed = True
        if q.get('points', 0) > 20:
            q['points'] = 15
            changed = True
    # 350자 이상은 그대로 유지 (별도 재생성 대상)
    return changed


def main():
    # === 1. 강등 ===
    path = DATA_DIR / '2a.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    demoted = 0
    for q in data['questions']:
        if demote_short(q):
            demoted += 1
    print(f'[강등] {demoted}개 문제 난이도·점수 재할당')

    # === 2. AI 신규 통합 ===
    gen_path = DATA_DIR / '2a-generated.json'
    if gen_path.exists():
        gen = json.loads(gen_path.read_text(encoding='utf-8'))
        existing_ids = {q['id'] for q in data['questions']}
        ai_practice = []
        # ID는 기존 manual-2a-XXX 유지 (충돌 회피)
        for q in gen.get('questions', []):
            if q['id'] in existing_ids:
                continue
            new_q = dict(q)
            new_q['source'] = 'practice-set'
            # genMode 표시는 제거
            new_q.pop('genMode', None)
            new_q['chapter'] = '2a'
            new_q['subject'] = '감정평가실무'
            # difficulty 미지정 시 4 (AI 신규는 본격 분량)
            if not new_q.get('difficulty'):
                new_q['difficulty'] = 4
            if not new_q.get('points'):
                new_q['points'] = 30
            if not new_q.get('answerFormat'):
                new_q['answerFormat'] = 'essay-narrative'
            if not new_q.get('modelAnswerSource'):
                new_q['modelAnswerSource'] = 'ai-direct-essay'
            ai_practice.append(new_q)
        data['questions'].extend(ai_practice)
        print(f'[통합] AI 신규 {len(ai_practice)}개 → practice-set')

    data['count'] = len(data['questions'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    # 분포 출력
    practice = [q for q in data['questions'] if q.get('source') == 'practice-set']
    dist = {}
    for q in practice:
        d = q.get('difficulty', 0)
        dist[d] = dist.get(d, 0) + 1
    print(f"\n[현재 분포] practice-set 총 {len(practice)}개")
    for k in sorted(dist):
        print(f'  난이도 {k}: {dist[k]}개')


if __name__ == '__main__':
    main()
