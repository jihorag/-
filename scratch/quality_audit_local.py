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

SYSTEM = """당신은 감정평가사 1차 시험 출제 검수위원입니다. 연습문제 1개를 아래 기준으로 정밀 검수합니다.

[A. 기본 품질]
1. 정답 정확성: 정답 번호가 해설과 일치하는가? 복수정답·무정답 소지는?
2. 선지 품질: 중복·사실상 동일 선지, 형식 불균형, 어색한 한국어
3. 문제 성립성: 단서 부족, 출제 의도 모호, 질문-선지 논리 불일치
4. 해설 품질: 정답 근거 설명 + 오답 이유 포함 여부

[B. 감정평가사 시험 적합성 — exam_fit]
- 이 문제가 실제 감정평가사 1차 시험(민법·경제학원론·부동산학원론·감정평가관계법규·회계학)에
  출제될 법한 주제·수준·어투인가?
- 부적합 사례: 시험 범위 밖 지엽 주제, 학부 시험·공무원 시험 스타일의 동떨어진 출제,
  단순 국어 문제 수준, 실무·법령과 무관한 일반상식, 출제 관행에 없는 형식
- 적합하면 true, 부적합하면 false.

[C. 5단계 출제 원칙 — 난이도 라벨 검증 (difficulty_fit)]
문제에 표기된 난이도 라벨(1~5)이 실제 인지 요구 수준과 맞는지 판정:
- L1 = 단순 정의 암기 (개념 하나, 교과서 정의 그대로)
- L2 = 개념 비교·구별 (A vs B 차이, 유사 개념 중 선택)
- L3 = 복합 비교·파생현상 (3개 이상 개념 동시, 원인-결과 연결)
- L4 = 복합조건 정확 판단 (세부 수치·조건 적용, 정교한 함정)
- L5 = 사례형 종합 판단 (구체 상황에서 분류·성격 판단)
실제 수준을 추정해 estimated_level(1~5)로 답하고, 라벨과 2단계 이상 차이면 결함.

[D. 오답 함정 품질 — 레벨별 기준 (trap_quality)]
- L1~L2 문제: 오답은 완전히 다른 개념이어야 정상 (자명해도 무방)
- L3: 유사 개념 간 미묘한 차이로 함정 구성됐는가
- L4: 조건 일부만 바꾼 정교한 함정인가 ("공법상" vs "사법상" 식)
- L5: 복수 조건 중 일부씩 충족하는 매력적 오답인가
라벨 수준에 비해 오답이 너무 허술하면(찍어도 배제 가능) bad, 적절하면 good.

[출력 — JSON만]
{"score": 1~5, "exam_fit": true|false, "estimated_level": 1~5, "trap_quality": "good"|"weak"|"bad",
 "issues": ["복수정답"|"정답오류"|"선지중복"|"자명한오답"|"모호"|"해설부실"|"수준미달"|"시험부적합"|"난이도불일치"|"함정부실"|"오타" 중 해당],
 "reason": "한 줄 요약"}

score 산정: 5=출제 가능, 4=양호, 3=경미 결함, 2=뚜렷한 결함, 1=사용 불가.
exam_fit=false 또는 (라벨-실제 2단계 이상 차이)면 score는 3 이하여야 함."""


ANSWER_SYSTEM = """당신은 감정평가사 1차 시험 문제를 푸는 검증위원입니다.
주어진 문제를 스스로 풀어 정답 번호를 결정하세요. (기록된 정답은 제공되지 않습니다 — 독립적으로 푸세요)

[출력 — JSON만]
{"my_answer": 1~5 정수, "confidence": "high"|"medium"|"low", "reason": "근거 한두 줄"}

confidence 기준:
- high: 법령·정의·계산상 명확히 단일 정답
- medium: 유력하지만 해석 여지가 있음
- low: 자료 불충분·복수 정답 가능성·문제 자체의 모호함"""


def llm_solve(q, model, think=False, timeout=300):
    """기출 정답 검증 — 기록 정답·해설을 숨기고 독립 풀이."""
    opts = q.get('options') or []
    user = (
        f"[과목] {q.get('subject', '?')} ({q.get('year', '')}년 기출)\n"
        f"[문제] {q.get('question', '')}\n"
        + '\n'.join(f"{i + 1}. {o}" for i, o in enumerate(opts))
    )
    body = json.dumps({
        'model': model,
        'messages': [
            {'role': 'system', 'content': ANSWER_SYSTEM},
            {'role': 'user', 'content': user},
        ],
        'format': 'json',
        'think': think,           # 재검 단계에서만 사고 모드 (정확도↑, 속도↓)
        'stream': False,
        # 사고 모드는 사고 토큰이 num_predict에 포함 — 부족하면 JSON이 비어 나옴
        'options': {'temperature': 0.1, 'num_predict': 6000 if think else 250},
    }).encode('utf-8')
    req = urllib.request.Request(OLLAMA, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    content = (data.get('message') or {}).get('content', '')
    content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
    m = re.search(r'\{[\s\S]*\}', content)
    parsed = json.loads(m.group(0) if m else content)
    return {
        'my_answer': int(parsed.get('my_answer', 0)),
        'confidence': str(parsed.get('confidence', 'low')),
        'reason': str(parsed.get('reason', ''))[:200],
    }


EXPLAIN_SYSTEM = """당신은 시험 문제 해설을 읽고 그 해설이 지지하는 정답 번호를 찾는 검수위원입니다.
문제 지식으로 풀지 말고, 오직 **해설 텍스트가 어느 선지를 정답으로 설명하는지**만 판독하세요.

[출력 — JSON만]
{"explained_answer": 1~5 정수(해설이 지지하는 번호, 판독 불가면 0), "reason": "근거 한 줄"}"""


def llm_explain_check(q, model, timeout=180):
    """해설→정답 번호 독해 (지식 불요 — 전사 오류 판별의 결정타)."""
    opts = q.get('options') or []
    user = (
        f"[문제] {q.get('question', '')}\n"
        + '\n'.join(f"{i + 1}. {o}" for i, o in enumerate(opts))
        + f"\n[해설] {(q.get('explanation') or '')[:800]}"
    )
    body = json.dumps({
        'model': model,
        'messages': [
            {'role': 'system', 'content': EXPLAIN_SYSTEM},
            {'role': 'user', 'content': user},
        ],
        'format': 'json', 'think': False, 'stream': False,
        'options': {'temperature': 0.0, 'num_predict': 200},
    }).encode('utf-8')
    req = urllib.request.Request(OLLAMA, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    content = re.sub(r'<think>[\s\S]*?</think>', '', (data.get('message') or {}).get('content', '')).strip()
    m = re.search(r'\{[\s\S]*\}', content)
    parsed = json.loads(m.group(0) if m else content)
    return int(parsed.get('explained_answer', 0)), str(parsed.get('reason', ''))[:150]


def answer_verdict(recorded, ev):
    if not recorded:
        return 'no_answer'
    if ev['my_answer'] == recorded:
        return 'ok'
    return 'answer_mismatch' if ev['confidence'] == 'high' else 'answer_doubt'


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
    iv = q.get('indexing_v4') or {}
    mt = iv.get('mapped_taxonomy') or {}
    user = (
        f"[과목] {mt.get('subject', q.get('subject', '?'))} / {mt.get('chapter', '')} {mt.get('item') or mt.get('section', '')}\n"
        f"[난이도 라벨] L{iv.get('difficulty', '?')} / [형식 라벨] {q.get('question_type', '?')}\n"
        f"[문제] {q.get('question', '')}\n"
        + '\n'.join(f"{i + 1}. {o}" for i, o in enumerate(opts))
        + f"\n[정답] {q.get('answer')}번"
        + f"\n[해설] {(q.get('explanation') or '')[:600]}"
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
    est = parsed.get('estimated_level')
    return {
        'score': score,
        'exam_fit': bool(parsed.get('exam_fit', True)),
        'estimated_level': int(est) if est in (1, 2, 3, 4, 5, '1', '2', '3', '4', '5') else None,
        'trap_quality': str(parsed.get('trap_quality', '')) or None,
        'issues': [str(x) for x in (parsed.get('issues') or [])][:6],
        'reason': str(parsed.get('reason', ''))[:200],
    }


def verdict_of(ev, rule_flags, label_level):
    hard_rules = [f for f in rule_flags if f not in ('해설미달',)]
    if hard_rules:
        return 'drop'
    if not ev.get('exam_fit', True):
        return 'drop'                      # 감평사 시험에 안 맞으면 점수 무관 탈락
    score = ev['score']
    # 난이도 라벨-실제 괴리 2단계 이상 → 최소 review (L4 라벨인데 L1 수준 등)
    est = ev.get('estimated_level')
    gap = abs(est - label_level) if (est and label_level) else 0
    if score >= 4:
        return 'review' if gap >= 2 else 'keep'
    if score == 3:
        return 'review'
    return 'drop'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('db', help='questions_db_*.json 경로')
    ap.add_argument('--model', default='qwen3.6:latest')
    ap.add_argument('--limit', type=int, default=0, help='샘플 개수 (0=전체)')
    ap.add_argument('--rules-only', action='store_true', help='LLM 없이 규칙 검사만')
    ap.add_argument('--mode', choices=['quality', 'answer'], default='quality',
                    help='quality=연습문제 품질 감사 / answer=기출 정답 키 검증')
    ap.add_argument('--recheck', action='store_true',
                    help='(answer 모드) 1차에서 불일치·의심 문항만 사고 모드로 정밀 재검')
    ap.add_argument('--verify-explanation', action='store_true',
                    help='(answer 모드 3단계) 남은 불일치를 해설 대조로 최종 판별 — '
                         '해설 지지 번호 != 기록 정답이면 key_error_likely(전사 오류 유력)')
    args = ap.parse_args()

    db_path = ROOT / args.db
    db = json.load(open(db_path, encoding='utf-8'))
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = AUDIT_DIR / (db_path.stem + '.jsonl')

    prev = {}  # id → 마지막 레코드 (재검 줄이 이전 판정을 덮음)
    if out_path.exists():
        for line in out_path.read_text(encoding='utf-8').splitlines():
            try:
                r = json.loads(line)
                prev[r['id']] = r
            except (json.JSONDecodeError, KeyError):
                pass
    done = set(prev)

    if args.verify_explanation:
        targets = {i for i, r in prev.items()
                   if r.get('verdict') in ('answer_mismatch', 'answer_doubt') and not r.get('explained')}
        todo = [q for q in db if q.get('id') in targets]
    elif args.recheck:
        # 불일치·의심 문항만 사고 모드로 재검
        targets = {i for i, r in prev.items() if r.get('verdict') in ('answer_mismatch', 'answer_doubt') and not r.get('rechecked')}
        todo = [q for q in db if q.get('id') in targets]
    else:
        todo = [q for q in db if q.get('id') not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f'{db_path.name}: 전체 {len(db)} / 완료 {len(done)} / 이번 대상 {len(todo)}')

    t0 = time.time()
    n_llm = 0
    with open(out_path, 'a', encoding='utf-8') as out:
        for i, q in enumerate(todo):
            if args.mode == 'answer':
                # ── 기출 정답 키 검증 ──
                rec = {'id': q.get('id')}
                blob = (q.get('question') or '') + ' '.join(str(o) for o in (q.get('options') or []))
                if 'IMAGE' in blob or '도면' in (q.get('question') or '')[:30]:
                    # 보기·지문이 이미지에 있으면 텍스트 LLM으로 판정 불가
                    rec.update({'verdict': 'image_skip', 'reason': '이미지 의존 문항 — 텍스트 검증 불가'})
                    out.write(json.dumps(rec, ensure_ascii=False) + '\n')
                    out.flush()
                    continue
                try:
                    recorded = int(str(q.get('answer', '')).strip() or 0)
                except ValueError:
                    recorded = 0
                if args.verify_explanation:
                    # 3단계: 해설 독해 — 해설이 지지하는 번호 vs 기록 정답
                    prev_rec = prev.get(q.get('id'), {})
                    try:
                        if not (q.get('explanation') or '').strip():
                            rec = {**prev_rec, 'explained': True, 'explained_answer': None,
                                   'verdict': 'answer_mismatch'}  # 해설 없음 — 사람 검토 필요
                        else:
                            ea, why = llm_explain_check(q, args.model)
                            rec = {**prev_rec, 'explained': True, 'explained_answer': ea, 'explain_reason': why}
                            if ea == recorded and ea != 0:
                                rec['verdict'] = 'ok'              # 해설=기록 → LLM 풀이가 틀린 것 (위양성)
                            elif ea != 0:
                                rec['verdict'] = 'key_error_likely'  # 해설≠기록 → 정답키 전사 오류 유력
                            # ea==0(판독불가)이면 기존 판정 유지
                    except Exception as e:  # noqa: BLE001
                        print(f'  해설대조 실패(보류): {q.get("id")} — {str(e)[:80]}', flush=True)
                        continue
                    out.write(json.dumps(rec, ensure_ascii=False) + '\n')
                    out.flush()
                    continue
                try:
                    ev = llm_solve(q, args.model, think=args.recheck)
                    rec.update(ev)
                    rec['recorded'] = recorded
                    rec['verdict'] = answer_verdict(recorded, ev)
                    if args.recheck:
                        rec['rechecked'] = True
                except Exception as e:  # noqa: BLE001
                    if args.recheck:
                        print(f'  재검 실패(보류): {q.get("id")} — {str(e)[:80]}', flush=True)
                        continue  # 이전 판정 유지 — 다음 recheck에서 재시도
                    rec.update({'verdict': 'error', 'reason': str(e)[:120]})
                out.write(json.dumps(rec, ensure_ascii=False) + '\n')
                out.flush()
                if (i + 1) % 10 == 0 or i == len(todo) - 1:
                    el = time.time() - t0
                    rate = (i + 1) / el if el else 0
                    eta = (len(todo) - i - 1) / rate / 60 if rate else 0
                    print(f'  {i + 1}/{len(todo)} ({rate:.2f}문항/초, 남은 시간 ~{eta:.0f}분)', flush=True)
                continue

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
                    label_level = (q.get('indexing_v4') or {}).get('difficulty')
                    rec['verdict'] = verdict_of(ev, rule_flags, label_level)
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

    # 요약 — id별 마지막 레코드 기준 (재검이 이전 판정을 덮음)
    last = {}
    for l in out_path.read_text(encoding='utf-8').splitlines():
        try:
            r = json.loads(l)
            last[r['id']] = r
        except (json.JSONDecodeError, KeyError):
            pass
    recs = list(last.values())
    by = {}
    for r in recs:
        by[r['verdict']] = by.get(r['verdict'], 0) + 1
    print(f'\n=== {db_path.name} 감사 현황 (누적 {len(recs)}) ===')
    for k in ('keep', 'review', 'drop', 'ok', 'key_error_likely', 'answer_mismatch', 'answer_doubt', 'image_skip', 'no_answer', 'error', 'rules_pass'):
        if by.get(k):
            print(f'  {k:16s} {by[k]}')
    mis = [r for r in recs if r.get('verdict') in ('key_error_likely', 'answer_mismatch')][:8]
    if mis:
        print('\n  ⚠️ 정답 불일치 의심 (기록 vs LLM):')
        for r in mis:
            print(f"   {r['id']}: 기록 {r.get('recorded')}번 vs LLM {r.get('my_answer')}번 ({r.get('confidence')}) — {r.get('reason', '')[:70]}")
    worst = sorted([r for r in recs if r.get('score')], key=lambda r: r['score'])[:5]
    if worst:
        print('\n  최저점 예시:')
        for r in worst:
            print(f"   [{r['score']}] {r['id']} — {', '.join(r['issues'])} | {r['reason'][:60]}")


if __name__ == '__main__':
    main()
