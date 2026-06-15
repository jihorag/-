#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 학습 교재 슬라이스 정밀화 — leaf를 교재 헤딩(절/항) 범위에 정확히 재매핑.

현재 ai_taxonomy_index.json의 section_lines는 거칠어(여러 leaf가 같은 큰 덩어리 공유,
평균 ~700줄/~10K토큰) AI 학습 첫 질문 토큰 낭비. 교재 헤딩 키워드로 각 leaf를 그
절/항에 매핑해 슬라이스를 좁힌다(목표 ~200줄/~3K토큰).

매칭: leaf 제목의 핵심어(번호·'제N관/절' 제거)가 교재 헤딩 핵심어와 포함관계면 매칭.
매칭된 leaf만 section_lines를 그 헤딩 범위로 좁히고, 못 찾으면 기존 유지(안전).

- dry-run(기본): 매칭률·토큰 before/after만 출력
- --apply: ai_taxonomy_index.json 갱신(백업)
사용: python3 scratch/reslice_units.py civil          # 미리보기
      python3 scratch/reslice_units.py civil --apply
"""
import argparse
import json
import re
import sys
from pathlib import Path

import urllib.request
ROOT = Path(__file__).resolve().parent.parent
OLLAMA = 'http://localhost:11434/api/chat'
MODEL = 'qwen3.6:latest'


def llm_match(leaf_title, cands, timeout=90):
    """leaf 제목 → 교재 헤딩 후보 중 가장 맞는 index (없으면 -1)."""
    lst = '\n'.join(f"{i}: {h['text'][:54]}" for i, h in enumerate(cands))
    sys_p = '당신은 감정평가사 교재의 소단원을 해당 교재 헤딩에 매칭하는 사서입니다. 소단원 제목에 가장 정확히 해당하는 헤딩 번호 하나를 고르세요. 적절한 게 없으면 -1.\n[출력 JSON만] {"idx": 정수}'
    user = f"[소단원] {leaf_title}\n\n[교재 헤딩 목록]\n{lst}"
    body = json.dumps({'model': MODEL, 'messages': [{'role':'system','content':sys_p},{'role':'user','content':user}],
        'format':'json','think':False,'stream':False,'options':{'temperature':0.0,'num_predict':60}}).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    c = re.sub(r'<think>[\s\S]*?</think>','',(data.get('message') or {}).get('content','')).strip()
    m = re.search(r'-?\d+', c)
    return int(m.group(0)) if m else -1


def norm(s):
    """제목 핵심어 — 번호·'제N관/절/장/항'·기호·공백 제거."""
    s = re.sub(r'제\s*\d+\s*[관절장항편]', '', s)
    s = re.sub(r'\[[^\]]*\]', '', s)            # [民法] 등 대괄호
    s = re.sub(r'[IVXⅠ-Ⅹ]+\.?', '', s)          # 로마자
    s = re.sub(r'[^가-힣A-Za-z0-9]', '', s)
    return s


def parse_headings(md):
    """(level, normtext, rawtext, start_line) 목록 + 각 헤딩의 end_line."""
    lines = md.split('\n')
    raw = []
    for i, l in enumerate(lines, 1):
        m = re.match(r'^(#{2,4})\s+(.+)', l)
        if m:
            raw.append({'level': len(m.group(1)), 'text': m.group(2).strip(),
                        'norm': norm(m.group(2)), 'start': i})
    # 끝줄: 다음에 나오는 level<=자기 헤딩의 start-1, 없으면 파일 끝
    n = len(lines)
    for idx, h in enumerate(raw):
        end = n
        for h2 in raw[idx + 1:]:
            if h2['level'] <= h['level']:
                end = h2['start'] - 1
                break
        h['end'] = end
    return raw


def best_match(leaf_norm, headings):
    """leaf 핵심어와 포함관계인 헤딩 중 가장 적합(가장 짧은 범위=구체적)."""
    if len(leaf_norm) < 3:
        return None
    cands = []
    for h in headings:
        hn = h['norm']
        if len(hn) < 2:
            continue
        # 양방향 포함 또는 충분한 공통 부분
        if leaf_norm in hn or hn in leaf_norm:
            cands.append(h)
    if not cands:
        return None
    # 범위가 너무 큰 것(>1200줄)은 제외, 가장 구체적(짧은 범위) 우선
    cands = [c for c in cands if (c['end'] - c['start']) <= 1200] or cands
    return min(cands, key=lambda c: c['end'] - c['start'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--llm', action='store_true', help='로컬 LLM 의미 매칭(텍스트 매칭보다 정확)')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    sdir = ROOT / f'viewer/public/data/study/{args.subject}'
    idx_path = sdir / 'ai_taxonomy_index.json'
    d = json.loads(idx_path.read_text(encoding='utf-8'))
    leaves = d.get('leaves', [])

    # 교재별 헤딩 캐시
    head_cache = {}
    def headings_of(unit_file):
        if unit_file not in head_cache:
            p = sdir / unit_file
            head_cache[unit_file] = parse_headings(p.read_text(encoding='utf-8')) if p.exists() else []
        return head_cache[unit_file]

    md_lines = {}
    def linecount(unit_file, a, b):
        return max(0, b - a)

    matched = 0
    before_total = 0
    after_total = 0
    changes = []
    for li, l in enumerate(leaves):
        if args.limit and li >= args.limit:
            break
        uf = l.get('unit_file')
        sl = l.get('section_lines')
        if not uf or not sl or len(sl) != 2:
            continue
        before = sl[1] - sl[0]
        before_total += before
        hs = headings_of(uf)
        if args.llm:
            cands = [x for x in hs if x['level'] in (3, 4) and (x['end'] - x['start']) <= 1200]
            try:
                idx = llm_match(l.get('title', ''), cands) if cands else -1
            except Exception:  # noqa: BLE001
                idx = -1
            h = cands[idx] if 0 <= idx < len(cands) else None
        else:
            h = best_match(norm(l.get('title', '')), hs)
        if h:
            new_sl = [h['start'], h['end']]
            after = h['end'] - h['start']
            # 새 범위가 더 작을 때만 채택(맥락 과소 방지: 최소 40줄)
            if after < before and after >= 40:
                matched += 1
                after_total += after
                changes.append((l, new_sl, before, after))
            else:
                after_total += before
        else:
            after_total += before

    tok = lambda lines: lines * 14  # 한국어 md 줄당 ~14토큰 추정
    print(f'=== {args.subject} 재슬라이싱 {"적용" if args.apply else "미리보기"} ===')
    print(f'leaf {len(leaves)}개 중 정밀매칭 {matched}개 ({matched*100//max(1,len(leaves))}%)')
    print(f'슬라이스 총 줄수: {before_total} → {after_total} ({(before_total-after_total)*100//max(1,before_total)}% 감소)')
    print(f'추정 토큰(매핑 합): ~{tok(before_total)//1000}K → ~{tok(after_total)//1000}K')
    print('\n샘플(좁혀진 leaf 8개):')
    for l, new_sl, b, a in changes[:8]:
        print(f"  {l.get('title','')[:26]:26s} {b}줄 → {a}줄  [{new_sl[0]},{new_sl[1]}]")

    if not args.apply:
        print('\n(미리보기 — 적용은 --apply)')
        return

    for l, new_sl, b, a in changes:
        l['section_lines'] = new_sl
        l['section_key'] = 'heading'
    bak = idx_path.with_suffix('.json.bak-reslice')
    if not bak.exists():
        bak.write_bytes(idx_path.read_bytes())
    idx_path.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'\n✅ 적용 완료({matched}개 leaf 정밀화). 백업: {bak.name}')


if __name__ == '__main__':
    main()
