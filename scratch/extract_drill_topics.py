#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 드릴 주제 추출 — 각 leaf(관) 교재 슬라이스에서 '아주 좁은 개념' 3~6개를 로컬 LLM으로.

드릴 탭은 관(款)을 더 잘게 쪼갠 '주제(topic)' 단위로 짧은 질답을 반복해 개념을 체화한다.
이 스크립트가 그 주제 목록을 미리 추출한다(1회성 배치). 사용자는 앱에서 수동 추가 가능.

각 주제: { id, title(짧은 개념명 8~20자), hint(한 줄 핵심, 질문 방향) }
출력: viewer/public/data/drill/{subjectId}.json = { "<leafId>": [topic, ...] }

- dry-run(기본): 추출 결과 출력만
- --apply: 파일 저장(체크포인트 — 이미 있는 leaf는 건너뜀, --force로 재추출)
사용: python3 scratch/extract_drill_topics.py civil [--limit 3] [--apply] [--force]
"""
import argparse
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLLAMA = 'http://localhost:11434/api/chat'
MODEL = 'qwen3.6:latest'

SYSTEM = """당신은 감정평가사 수험 교재를 '드릴용 최소 개념 단위'로 쪼개는 편집자입니다.
주어진 교재 조각(한 관/절)을 학생이 짧은 질답 2~3개로 확인할 수 있는 '아주 좁은 개념'으로 나눕니다.

[규칙]
- 3~6개. 각 주제는 절·관 수준이 아니라 그보다 더 좁은 단위(정의 하나, 요건 하나, 구별 하나, 판례 논점 하나).
- 교재에 실제로 있는 내용만. 없는 건 만들지 마라.
- title: 8~20자 짧은 개념명. hint: 그 개념에서 학생이 인출해야 할 핵심을 한 줄로(질문 방향).

[출력 — JSON만]
{"topics": [{"title": "개념명", "hint": "인출 핵심 한 줄"}, ...]}"""


def extract(slice_md, leaf_path, timeout=180):
    body_md = slice_md[:6000]
    user = f"[단원] {leaf_path}\n\n[교재 조각]\n{body_md}\n\n위를 드릴용 좁은 개념 3~6개로 나눠라."
    payload = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': user}],
        'format': 'json', 'think': False, 'stream': False,
        'options': {'temperature': 0.2, 'num_predict': 700},
    }).encode('utf-8')
    req = urllib.request.Request(OLLAMA, data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    c = re.sub(r'<think>[\s\S]*?</think>', '', (data.get('message') or {}).get('content', '')).strip()
    m = re.search(r'\{[\s\S]*\}', c)
    parsed = json.loads(m.group(0) if m else c)
    out = []
    for t in parsed.get('topics', []):
        title = str(t.get('title', '')).strip()
        if 2 <= len(title) <= 40:
            out.append({'title': title, 'hint': str(t.get('hint', '')).strip()[:120]})
    return out[:6]


def slice_section(md, lines):
    if not lines or len(lines) != 2:
        return md
    arr = md.split('\n')
    return '\n'.join(arr[max(0, lines[0] - 1): min(len(arr), lines[1])])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--force', action='store_true', help='이미 추출된 leaf도 재추출')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    sdir = ROOT / f'viewer/public/data/study/{args.subject}'
    idx_path = sdir / 'ai_taxonomy_index.json'
    if not idx_path.exists():
        # 2차 과목은 ai_index.json(units/topics) — 이미 정밀, 드릴 주제는 topic 그대로 활용 권장
        raise SystemExit(f'{idx_path} 없음 (2차는 ai_index.json topic을 직접 쓰세요)')
    idx = json.loads(idx_path.read_text(encoding='utf-8'))
    leaves = idx.get('leaves', [])

    out_dir = ROOT / 'viewer/public/data/drill'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f'{args.subject}.json'
    result = json.loads(out_path.read_text(encoding='utf-8')) if out_path.exists() else {}

    md_cache = {}
    def md_of(uf):
        if uf not in md_cache:
            p = sdir / uf
            md_cache[uf] = p.read_text(encoding='utf-8') if p.exists() else ''
        return md_cache[uf]

    todo = [l for l in leaves if l.get('unit_file') and (args.force or l['id'] not in result)]
    if args.limit:
        todo = todo[:args.limit]
    print(f'{args.subject}: leaf {len(leaves)} / 추출 대상 {len(todo)} (이미 {len(result)})')

    t0 = time.time()
    n = 0
    for l in todo:
        md = md_of(l['unit_file'])
        if not md:
            continue
        sliced = slice_section(md, l.get('section_lines')) if l.get('section_key') != 'full' else md
        path = ' / '.join(l.get('path', [])[-2:]) or l.get('title', '')
        try:
            topics = extract(sliced, path)
        except Exception as e:  # noqa: BLE001
            print(f'  추출 실패: {l["id"]} — {str(e)[:50]}')
            continue
        # id 부여 (leaf id + 순번)
        for i, t in enumerate(topics):
            t['id'] = f"{l['id']}__t{i + 1}"
        if topics:
            result[l['id']] = topics
            n += 1
        if n <= 3 or n % 20 == 0:
            print(f'  [{n}] {l.get("title","")[:24]:24s} → {len(topics)}주제: {", ".join(t["title"][:14] for t in topics[:4])}')
        if args.apply and n % 10 == 0:
            out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding='utf-8')

    el = time.time() - t0
    total_t = sum(len(v) for v in result.values())
    print(f'\n완료: {n}개 leaf 추출, 누적 주제 {total_t}개 ({el:.0f}s)')
    if args.apply:
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'✅ 저장: {out_path.relative_to(ROOT)}')
    else:
        print('(미리보기 — 저장은 --apply)')


if __name__ == '__main__':
    main()
