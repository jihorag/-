#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""교재 관(款) 단위 재구조화 — 같은 범위를 공유하는 leaf 그룹을 로컬 LLM으로 분할.

문제: ai_taxonomy_index.json의 여러 leaf(관)가 같은 거친 범위(예: 740줄)를 공유해
AI 학습 첫 질문 토큰 낭비. 교재 헤딩 체계(장-절-항)와 목차 체계(장-절-관)가 달라
텍스트 매칭이 안 됨.

해법: 같은 (unit_file, section_lines) 그룹의 leaf 제목들을 LLM에 주고, 그 범위
교재 텍스트(줄번호 부여) 안에서 각 관이 시작하는 줄번호를 받아 관 경계를 재설정.
교재 파일은 불변 — section_lines만 정밀화.

- dry-run(기본): 그룹별 분할 결과 미리보기 + 토큰 절감 추정
- --apply: ai_taxonomy_index.json 갱신(백업)
사용: python3 scratch/restructure_units.py civil [--group N] [--apply]
"""
import argparse
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLLAMA = 'http://localhost:11434/api/chat'
MODEL = 'qwen3.6:latest'


def split_group(md_lines, start, end, leaf_titles, timeout=240):
    """범위[start,end] 교재를 leaf_titles 순서대로 분할 → {title: 시작줄}."""
    # 줄번호 부여 텍스트 (범위 내)
    numbered = '\n'.join(f'{i}|{md_lines[i - 1]}' for i in range(start, min(end, len(md_lines)) + 1))
    if len(numbered) > 24000:
        numbered = numbered[:24000]  # 과대 입력 컷
    titles = '\n'.join(f'- {t}' for t in leaf_titles)
    sys_p = (
        '당신은 감정평가사 교재를 소단원(관) 경계로 나누는 편집자입니다. '
        '주어진 교재 텍스트(각 줄 앞 "줄번호|")를 아래 소단원들이 순서대로 차지한다고 보고, '
        '각 소단원이 시작하는 줄번호를 찾으세요. 소단원은 제시된 순서대로 본문에 등장합니다.\n'
        '[출력 — JSON만] {"분할": [{"title": "소단원제목", "start_line": 줄번호}, ...]}'
    )
    user = f'[교재 텍스트 — 줄 {start}~{end}]\n{numbered}\n\n[순서대로 등장하는 소단원]\n{titles}'
    body = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'system', 'content': sys_p}, {'role': 'user', 'content': user}],
        'format': 'json', 'think': False, 'stream': False,
        'options': {'temperature': 0.0, 'num_predict': 800},
    }).encode('utf-8')
    req = urllib.request.Request(OLLAMA, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    c = re.sub(r'<think>[\s\S]*?</think>', '', (data.get('message') or {}).get('content', '')).strip()
    m = re.search(r'\{[\s\S]*\}', c)
    parsed = json.loads(m.group(0) if m else c)
    out = {}
    for item in parsed.get('분할', []):
        ln = item.get('start_line')
        if isinstance(ln, int) and start <= ln <= end:
            out[item.get('title', '')] = ln
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--group', type=int, default=-1, help='특정 그룹만(테스트용, 크기순 index)')
    args = ap.parse_args()

    sdir = ROOT / f'viewer/public/data/study/{args.subject}'
    idx_path = sdir / 'ai_taxonomy_index.json'
    d = json.loads(idx_path.read_text(encoding='utf-8'))
    leaves = d.get('leaves', [])

    # 같은 (unit_file, section_lines) 그룹화 — 2개 이상 공유 + 범위 큰 것
    groups = defaultdict(list)
    for l in leaves:
        uf, sl = l.get('unit_file'), l.get('section_lines')
        if uf and sl and len(sl) == 2 and l.get('section_key') != 'heading':
            groups[(uf, tuple(sl))].append(l)
    # 분할 대상: 2개 이상 leaf가 공유 + 범위 >= 200줄
    targets = [(k, v) for k, v in groups.items() if len(v) >= 2 and (k[1][1] - k[1][0]) >= 200]
    targets.sort(key=lambda x: -(x[0][1][1] - x[0][1][0]) * len(x[1]))  # 절감 큰 순

    md_cache = {}
    def lines_of(uf):
        if uf not in md_cache:
            md_cache[uf] = (sdir / uf).read_text(encoding='utf-8').split('\n')
        return md_cache[uf]

    print(f'분할 대상 그룹: {len(targets)}개 (2+ leaf 공유, 200줄+)')
    before_t = after_t = 0
    sel = enumerate(targets)
    if args.group >= 0:
        sel = [(args.group, targets[args.group])] if args.group < len(targets) else []
    for gi, ((uf, sl), grp) in sel:
        a, b = sl
        span = b - a
        before_t += span * len(grp)
        titles = [l.get('title', '') for l in grp]
        try:
            starts = split_group(lines_of(uf), a, b, titles)
        except Exception as e:  # noqa: BLE001
            print(f'  [{gi}] {uf} [{a},{b}] {len(grp)}개 — 분할 실패: {str(e)[:50]}')
            after_t += span * len(grp)
            continue
        # 제목→시작줄 정렬, 경계 계산
        pts = sorted([(starts.get(t), t) for t in titles if starts.get(t)], key=lambda x: x[0])
        if len(pts) < 2:
            print(f'  [{gi}] {uf} [{a},{b}] {len(grp)}개 — 분할점 부족({len(pts)}), 유지')
            after_t += span * len(grp)
            continue
        bounds = {}
        for i, (ln, t) in enumerate(pts):
            end = (pts[i + 1][0] - 1) if i + 1 < len(pts) else b
            bounds[t] = [ln, end]
        print(f'  [{gi}] {uf} [{a},{b}] {len(grp)}개 leaf → {len(bounds)}개 분할:')
        MIN_LINES = 40  # 헤딩만 잡힌 과소 조각은 버리고 기존 범위 유지(맥락 보존)
        for t in titles:
            bs = bounds.get(t)
            if bs and (bs[1] - bs[0]) >= MIN_LINES:
                after_t += bs[1] - bs[0]
                print(f'        {t[:30]:30s} [{bs[0]},{bs[1]}] ({bs[1]-bs[0]}줄)')
            else:
                after_t += span  # 유지
                if bs:
                    print(f'        {t[:30]:30s} (분할 {bs[1]-bs[0]}줄 과소 → 유지)')
        if args.apply:
            for l in grp:
                t = l.get('title', '')
                bs = bounds.get(t)
                if bs and (bs[1] - bs[0]) >= MIN_LINES:
                    l['section_lines'] = bs
                    l['section_key'] = 'heading'

    print(f'\n토큰 절감 추정(대상 그룹): ~{before_t*14//1000}K → ~{after_t*14//1000}K '
          f'({(before_t-after_t)*100//max(1,before_t)}% 감소)')
    if args.apply:
        bak = idx_path.with_suffix('.json.bak-restruct')
        if not bak.exists():
            bak.write_bytes(idx_path.read_bytes())
        idx_path.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'✅ 적용 완료. 백업: {bak.name}')
    else:
        print('(미리보기 — 적용은 --apply)')


if __name__ == '__main__':
    main()
