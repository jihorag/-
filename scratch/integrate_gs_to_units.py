#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""실무 GS 문제(gs0~3)를 핵심 단원(1~8b)에 통합 — 로컬 LLM(Ollama)로 소단원 분류.

GS 문제는 이미 subchapter에 대단원 코드(2a·3·4...)를 갖고 있어 대단원 분류는 완료.
이 스크립트는 각 GS 문제를 그 대단원의 소단원(AI topic) 중 하나로 LLM 분류하여
핵심 단원 파일로 이동한다. GS 출처(gsRound·session·source)는 보존 → 카드에 'GS N기' 표기.

- dry-run(기본): 분류 결과 분포만 출력, 파일 미변경
- --apply: 백업(.bak-gs) 후 핵심 단원 파일에 이동 + gs 파일 비움 → rebuild_manifest 필요

사용:
  python3 scratch/integrate_gs_to_units.py            # 미리보기(분류 분포)
  python3 scratch/integrate_gs_to_units.py --limit 8  # 8문항 샘플 분류 확인
  python3 scratch/integrate_gs_to_units.py --apply     # 실제 통합
"""
import argparse
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'viewer/public/data/essay/practice'
OLLAMA = 'http://localhost:11434/api/chat'
MODEL = 'qwen3.6:latest'
GS_FILES = ['gs0', 'gs1', 'gs2', 'gs3']

SYSTEM = """당신은 감정평가실무 2차 문제를 세부단원으로 분류하는 분류위원입니다.
주어진 문제를 후보 세부단원 중 가장 적합한 하나에 배정하세요.

[출력 — JSON만]
{"subchapter": "후보 id 중 하나", "reason": "근거 한 줄"}

반드시 제시된 후보 id 중에서만 고르세요. 계산·산식 위주이므로 핵심 평가방법으로 판단."""


def classify(q, subs, timeout=120):
    cand = '\n'.join(f"- {s['id']}: {s['title']}" for s in subs)
    body = (q.get('body') or '')[:700]
    kps = q.get('keyPoints') or []
    kp = ('\n[핵심 논점] ' + ', '.join(str(k) for k in kps[:6])) if kps else ''
    user = f"[문제]\n{body}{kp}\n\n[후보 세부단원]\n{cand}\n\n가장 적합한 세부단원 id를 고르세요."
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
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    manifest = json.loads((BASE / 'manifest.json').read_text(encoding='utf-8'))
    core = {c['id']: c for c in manifest['chapters'] if c.get('aiUnit')}
    topics = {cid: c.get('subchapters', []) for cid, c in core.items()}
    valid = {cid: {s['id'] for s in subs} for cid, subs in topics.items()}

    core_data = {cid: json.loads((BASE / f'{cid}.json').read_text(encoding='utf-8')) for cid in core}
    gs_data = {f: json.loads((BASE / f'{f}.json').read_text(encoding='utf-8')) for f in GS_FILES}

    t0 = time.time()
    moved = 0      # 통합된 문항
    skipped = 0    # 대단원이 핵심에 없어 남김
    dist = {}      # 단원별 통합 수
    processed = 0
    for gsf in GS_FILES:
        keep = []
        for q in gs_data[gsf]['questions']:
            if args.limit and processed >= args.limit:
                keep.append(q)
                continue
            unit = q.get('subchapter')  # 대단원 코드 (2a·3·...)
            if unit not in topics or len(topics[unit]) == 0:
                keep.append(q); skipped += 1
                continue
            processed += 1
            try:
                pick = classify(q, topics[unit])
            except Exception as e:  # noqa: BLE001
                print(f'  분류 실패(남김): {q.get("id")} — {str(e)[:60]}', flush=True)
                keep.append(q); skipped += 1
                continue
            sub_id = pick if pick in valid[unit] else topics[unit][0]['id']
            dist[unit] = dist.get(unit, 0) + 1
            moved += 1
            if args.apply:
                nq = {**q, 'chapter': unit, 'subchapter': sub_id}
                core_data[unit]['questions'].append(nq)
            if moved % 20 == 0:
                el = time.time() - t0
                print(f'  {moved}문항 통합 ({moved / el:.2f}/초)', flush=True)
        if args.apply:
            gs_data[gsf]['questions'] = keep
        if args.limit and processed >= args.limit:
            break

    print(f'\n=== GS 통합 {"적용" if args.apply else "미리보기"} ===')
    print(f'통합 {moved} · 남김(대단원 미매칭) {skipped}')
    for cid in sorted(dist, key=lambda c: -dist[c]):
        print(f"  → {cid:4s} {core[cid]['title'][:24]:24s} +{dist[cid]}문항")

    if not args.apply:
        print('\n(미리보기 — 실제 통합은 --apply)')
        return

    stamp = time.strftime('%Y%m%d-%H%M')
    for cid in core:
        bak = BASE / f'{cid}.json.bak-gs-{stamp}'
        if not bak.exists():
            bak.write_bytes((BASE / f'{cid}.json').read_bytes())
        (BASE / f'{cid}.json').write_text(json.dumps(core_data[cid], ensure_ascii=False), encoding='utf-8')
    for gsf in GS_FILES:
        bak = BASE / f'{gsf}.json.bak-gs-{stamp}'
        if not bak.exists():
            bak.write_bytes((BASE / f'{gsf}.json').read_bytes())
        (BASE / f'{gsf}.json').write_text(json.dumps(gs_data[gsf], ensure_ascii=False), encoding='utf-8')
    print(f'\n✅ 통합 완료. 백업: *.bak-gs-{stamp}')
    print('   다음: python3 scratch/rebuild_manifest.py && cd viewer && npm run sync-data')


if __name__ == '__main__':
    main()
