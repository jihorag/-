#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2차 essay 문제를 AI 목차(subchapter=AI topic)에 로컬 LLM으로 재분류.

align_essay_to_ai.py(Phase A)로 manifest 세부단원이 AI topics와 일치된 뒤 실행.
각 chapter 파일의 문제를 그 chapter의 subchapter 후보 중 하나로 분류 → q.subchapter 갱신.

원본 백업(.bak-classify) 후 in-place 수정. 체크포인트 없이 chapter 단위로 저장.
사용: python3 scratch/classify_essay_subchapter.py theory law
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLLAMA = 'http://localhost:11434/api/chat'
MODEL = 'qwen3.6:latest'

SYSTEM = """당신은 감정평가사 2차 시험 문제를 세부단원으로 분류하는 분류위원입니다.
주어진 문제를 후보 세부단원 중 가장 적합한 하나에 배정하세요.

[출력 — JSON만]
{"subchapter": "후보 id 중 하나", "reason": "근거 한 줄"}

반드시 제시된 후보 id 중에서만 고르세요. 애매하면 가장 핵심 논점에 해당하는 것을 선택."""


def classify(q, subs, timeout=120):
    cand = '\n'.join(f"- {s['id']}: {s['title']}" for s in subs)
    body_q = (q.get('body') or q.get('question') or q.get('title') or '')[:700]
    kps = q.get('keyPoints') or []
    kp_txt = ('\n[핵심 논점] ' + ', '.join(str(k) for k in kps[:6])) if kps else ''
    user = f"[문제]\n{body_q}{kp_txt}\n\n[후보 세부단원]\n{cand}\n\n가장 적합한 세부단원 id를 고르세요."
    payload = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': user}],
        'format': 'json', 'think': False, 'stream': False,
        'options': {'temperature': 0.1, 'num_predict': 200},
    }).encode('utf-8')
    req = urllib.request.Request(OLLAMA, data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    content = re.sub(r'<think>[\s\S]*?</think>', '', (data.get('message') or {}).get('content', '')).strip()
    m = re.search(r'\{[\s\S]*\}', content)
    parsed = json.loads(m.group(0) if m else content)
    return str(parsed.get('subchapter', '')).strip()


def main():
    subjects = sys.argv[1:] or ['theory', 'law']
    for subj in subjects:
        base = ROOT / f'viewer/public/data/essay/{subj}'
        m = json.load(open(base / 'manifest.json', encoding='utf-8'))
        sub_by_ch = {c['id']: c.get('subchapters', []) for c in m['chapters'] if c.get('aiUnit')}
        valid_ids = {c['id']: {s['id'] for s in c.get('subchapters', [])} for c in m['chapters']}

        t0 = time.time()
        n_total = n_done = n_keep = 0
        for ch_id, subs in sub_by_ch.items():
            if len(subs) <= 1:
                continue  # 후보 1개 이하 — 분류 불필요
            f = base / f'{ch_id}.json'
            if not f.exists():
                continue
            d = json.load(open(f, encoding='utf-8'))
            bak = f.with_suffix('.json.bak-classify')
            if not bak.exists():
                bak.write_bytes(f.read_bytes())
            changed = False
            for q in d.get('questions', []):
                n_total += 1
                cur = q.get('subchapter')
                # 이미 유효한 세부(끝자리>1)면 유지 — 첫 분류 대상은 X-1/무태그
                if cur and cur in valid_ids.get(ch_id, set()) and not cur.endswith('-1'):
                    n_keep += 1
                    continue
                try:
                    pick = classify(q, subs)
                    if pick in valid_ids.get(ch_id, set()):
                        if q.get('subchapter') != pick:
                            q['subchapter'] = pick
                            changed = True
                        n_done += 1
                    else:
                        n_keep += 1
                except Exception as e:  # noqa: BLE001
                    print(f'  분류 실패(유지): {q.get("id")} — {str(e)[:60]}', flush=True)
                    n_keep += 1
            if changed:
                json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False)
            el = time.time() - t0
            print(f'  [{subj}/{ch_id}] 누적 {n_done}분류 / {n_keep}유지 ({n_total}건, {el:.0f}s)', flush=True)
        print(f'{subj} 완료: 재분류 {n_done}, 유지 {n_keep}, 전체 {n_total}\n')


if __name__ == '__main__':
    main()
