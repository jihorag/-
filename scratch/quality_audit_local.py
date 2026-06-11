#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""연습문제 품질 감사 — 로컬 LLM(Ollama) 기반.

2단 필터:
  1) 규칙 검사 (즉시): 보기 수·중복 선지·정답 범위·길이 미달 → 자동 drop 플래그
  2) LLM 채점 (qwen3.6 등): 1~5점 + 문제점 태그 + keep/review/drop

원본 DB는 절대 수정하지 않는다 — 결과는 scratch/quality_audit/{db}.jsonl 에
문항당 1줄씩 기록(중단 후 재실행 시 이어서). 적용은 quality_apply_local.py 로 별도.

사용:
  python3 scratch/quality_audit_local.py questions_db_re.json            # 전체
  python3 scratch/quality_audit_local.py questions_db_re.json --limit 20 # 샘플
  python3 scratch/quality_audit_local.py questions_db_civil.json --model qwen3.6:latest
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = ROOT / 'scratch' / 'quality_audit'
OLLAMA = 'http://localhost:11434/api/chat'

SYSTEM = """당신은 감정평가사 1차 시험 출제 검수위원입니다. 연습문제 1개의 품질을 평가합니다.

[평가 기준]
1. 정답 정확성: 정답 번호가 해설과 일치하는가? 복수정답·무정답 소지는 없는가?
2. 선지 품질: 중복·사실상 동일한 선지, 자명하게 어긋나는 오답(찍어도 제외 가능), 선지 간 길이·형식 불균형
3. 문제 성립성: 단서 부족, 출제 의도 모호, 질문과 선지의 논리 불일치
4. 해설 품질: 정답 근거가 실제로 설명되는가, 오답 이유가 있는가
5. 시험 적합성: 실제 시험에 나올 법한 수준인가 (정의 그대로 묻는 수준 미달 trivial 여부)

[출력 — JSON만]
{"score": 1~5 정수, "issues": ["복수정답"|"정답오류"|"선지중복"|"자명한오답"|"모호"|"해설부실"|"수준미달"|"오타" 중 해당하는 것들], "reason": "한 줄 요약"}

score 기준: 5=출제 가능 수준, 4=양호, 3=경미한 결함(검토 필요), 2=뚜렷한 결함, 1=사용 불가."""


def rule_check(q):
    """LLM 없이 잡히는 명백한 결함 → 태그 목록 반환."""
    flags = []
    opts = q.get('options') or []
    if len(opts) != 5:
        flags.append(f'보기{len(opts)}개')
    norm = [re.sub(r'\s+', '', str(o)) for o in opts]
    if len(set(norm)) != len(norm):
        flags.append('선지중복(완전동일)')
    try:
        a = int(str(q.get('answer', '')).strip())
        if not (1 <= a <= max(1, len(opts))):
            flags.append('정답범위밖')
    except (ValueError, TypeError):
        flags.append('정답형식오류')
    if len((q.get('question') or '').strip()) < 15:
        flags.append('문제문장미달')
    if len((q.get('explanation') or '').strip()) < 20:
        flags.append('해설미달')
    if any(len(str(o).strip()) < 2 for o in opts):
        flags.append('빈선지')
    return flags


def llm_eval(q, model, timeout=180):
    opts = q.get('options') or []
    user = (
        f"[문제] {q.get('question', '')}\n"
        + '\n'.join(f"{i + 1}. {o}" for i, o in enumerate(opts))
        + f"\n[정답] {q.get('answer')}번"
        + f"\n[해설] {(q.get('explanation') or '')[:600]}"
        + f"\n[난이도 라벨] {((q.get('indexing_v4') or {}).get('difficulty'))}"
    )
    body = json.dumps({
        'model': model,
        'messages': [
            {'role': 'system', 'content': SYSTEM},
            {'role': 'user', 'content': user},
        ],
        'format': 'json',
        'think': False,          # qwen3 계열 사고 모드 끔 (속도)
        'stream': False,
        'options': {'temperature': 0.1, 'num_predict': 300},
    }).encode('utf-8')
    req = urllib.request.Request(OLLAMA, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    content = (data.get('message') or {}).get('content', '')
    content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
    m = re.search(r'\{[\s\S]*\}', content)
    parsed = json.loads(m.group(0) if m else content)
    score = int(parsed.get('score', 3))
    score = min(5, max(1, score))
    return {
        'score': score,
        'issues': [str(x) for x in (parsed.get('issues') or [])][:6],
        'reason': str(parsed.get('reason', ''))[:200],
    }


def verdict_of(score, rule_flags):
    hard_rules = [f for f in rule_flags if f not in ('해설미달',)]
    if hard_rules:
        return 'drop'
    if score >= 4:
        return 'keep'
    if score == 3:
        return 'review'
    return 'drop'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('db', help='questions_db_*.json 경로')
    ap.add_argument('--model', default='qwen3.6:latest')
    ap.add_argument('--limit', type=int, default=0, help='샘플 개수 (0=전체)')
    ap.add_argument('--rules-only', action='store_true', help='LLM 없이 규칙 검사만')
    args = ap.parse_args()

    db_path = ROOT / args.db
    db = json.load(open(db_path, encoding='utf-8'))
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = AUDIT_DIR / (db_path.stem + '.jsonl')

    done = set()
    if out_path.exists():
        for line in out_path.read_text(encoding='utf-8').splitlines():
            try:
                done.add(json.loads(line)['id'])
            except (json.JSONDecodeError, KeyError):
                pass

    todo = [q for q in db if q.get('id') not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f'{db_path.name}: 전체 {len(db)} / 완료 {len(done)} / 이번 대상 {len(todo)}')

    t0 = time.time()
    n_llm = 0
    with open(out_path, 'a', encoding='utf-8') as out:
        for i, q in enumerate(todo):
            rule_flags = rule_check(q)
            rec = {'id': q.get('id'), 'rule_flags': rule_flags}
            # 명백한 규칙 위반이면 LLM 생략 (비용 절약)
            hard = [f for f in rule_flags if f not in ('해설미달',)]
            if hard or args.rules_only:
                rec.update({'score': 1 if hard else None, 'issues': rule_flags,
                            'reason': '규칙 검사 적발' if hard else '규칙만 검사',
                            'verdict': 'drop' if hard else 'rules_pass'})
            else:
                try:
                    ev = llm_eval(q, args.model)
                    n_llm += 1
                    rec.update(ev)
                    rec['verdict'] = verdict_of(ev['score'], rule_flags)
                except Exception as e:  # noqa: BLE001 — 한 문항 실패가 전체를 멈추지 않게
                    rec.update({'score': None, 'issues': ['평가실패'],
                                'reason': str(e)[:120], 'verdict': 'error'})
            out.write(json.dumps(rec, ensure_ascii=False) + '\n')
            out.flush()
            if (i + 1) % 10 == 0 or i == len(todo) - 1:
                el = time.time() - t0
                rate = (i + 1) / el if el else 0
                eta = (len(todo) - i - 1) / rate / 60 if rate else 0
                print(f'  {i + 1}/{len(todo)} ({rate:.2f}문항/초, 남은 시간 ~{eta:.0f}분)', flush=True)

    # 요약
    recs = [json.loads(l) for l in out_path.read_text(encoding='utf-8').splitlines()]
    by = {}
    for r in recs:
        by[r['verdict']] = by.get(r['verdict'], 0) + 1
    print(f'\n=== {db_path.name} 감사 현황 (누적 {len(recs)}) ===')
    for k in ('keep', 'review', 'drop', 'error', 'rules_pass'):
        if by.get(k):
            print(f'  {k:10s} {by[k]}')
    worst = sorted([r for r in recs if r.get('score')], key=lambda r: r['score'])[:5]
    if worst:
        print('\n  최저점 예시:')
        for r in worst:
            print(f"   [{r['score']}] {r['id']} — {', '.join(r['issues'])} | {r['reason'][:60]}")


if __name__ == '__main__':
    main()
