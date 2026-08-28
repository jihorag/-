#!/usr/bin/env python3
"""
generate_essay_variations.py — 2차 essay 문제 AI 변형/신규 생성

사용:
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 scripts/generate_essay_variations.py --chapter 2a --mode vary --count 2
  python3 scripts/generate_essay_variations.py --chapter 2a --mode new --count 3
  python3 scripts/generate_essay_variations.py --all --mode vary --count 1 --dry-run

옵션:
  --chapter ID      특정 단원만 (예: 2a, 6b). --all로 전체
  --all             모든 단원
  --mode {vary,new,both}
                    vary = 기존 문제 시나리오 변형 (안정적)
                    new  = 단원 이론 기반 신규 문제 (도전적, 모범답안도 AI 생성)
                    both = 둘 다
  --count N         vary 모드: 문제당 변형 N개 / new 모드: 단원당 신규 N개. 기본 2
  --model NAME      Anthropic 모델. 기본 claude-sonnet-4-5
  --dry-run         API 호출 없이 prompt만 출력 (비용 확인용)
  --resume          기존 generated.json 보존하고 추가만

출력:
  viewer/public/data/essay/practice/<chapter>-generated.json
  + manifest.json 업데이트 (generatedCount 추가)

비용 (대략):
  Claude Sonnet 4.5 기준 vary 1개 ≈ $0.01~0.03
  157문제 × 2 변형 = 약 $3~10
"""

import os, sys, json, time, argparse, hashlib, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone

DATA_DIR = Path('viewer/public/data/essay/practice')
THEORY_DIR = Path('outputs/2과목_2차_감정평가실무')
DEFAULT_MODEL = 'claude-sonnet-4-5'  # 안정·저렴. 더 어려운 신규 문제는 opus 권장
API_URL = 'https://api.anthropic.com/v1/messages'

# ─────────── 프롬프트 템플릿 ───────────

VARY_SYSTEM = """당신은 한국 감정평가사 2차 시험 출제위원입니다.
기존 기출문제와 동일한 논점·계산 패턴을 묻되, 시나리오와 수치만 바꾼 변형 문제를 만들어야 합니다.

원칙:
- 실제 시험 출제 스타일 유지: 평가의뢰 개요 → 평가자료(공시지가/거래사례/임대사례/조성사례 등) → 물음 1) 2) 3)
- 회차·연도 표기 X (예: "○○회", "2024년" 같은 직접 표기 금지). 가격시점은 가공된 일자 사용 가능.
- 자료는 표 형태로 제시 — `|` 또는 줄바꿈으로 정렬
- 모범답안은 동일한 풀이 패턴 (감칙 조문 인용 → 공식 적용 → 수치 계산 → 결정 의견)
- 시나리오는 의미 있게 다르게 (다른 부동산 유형/도시/보상 상황/특수 조건)
- 답안 구조: Ⅰ. 평가개요 → Ⅱ. 물음별 풀이 → Ⅲ. 결정 (필요시)
- 출력은 반드시 JSON 한 덩어리, 앞뒤 설명 텍스트 금지
"""

VARY_USER = """[원본 단원] {chapter_title}
[원본 회차·번호] {round}회 {questionNum}번 ({points}점)

[원본 문제]
{body}

[원본 모범답안]
{model_answer}

위 문제와 같은 논점·풀이 패턴을 묻되 시나리오·수치를 바꾼 변형 문제를 1개 만드세요.

다음 JSON 형식으로만 출력:
{{
  "body": "변형 문제 본문 (실제 시험지처럼 자세하게, 자료 표 포함)",
  "modelAnswer": "변형된 모범답안 (계산 과정 포함)",
  "points": {points},
  "changedFromOriginal": "원본과 무엇이 달라졌는지 한 문장"
}}
"""

NEW_SYSTEM = """당신은 한국 감정평가사 2차 시험 출제위원입니다.
주어진 단원의 기출 패턴을 참고해 새로운 시나리오·논점의 실전형 시험 문제를 만들어야 합니다.

품질 체크리스트 (모든 항목 충족):
[1] 평가의뢰 부동산 개요 — 소재지/면적/지목/용도지역/건물 구조 등 명시
[2] 자료 3~5개 — 공시지가 표준지 / 거래사례 / 임대사례 / 조성사례 / 비교표 등 (표 형태)
[3] 물음 1)~5) — 각 물음마다 명확한 풀이 방향 (~80~140자/물음)
[4] 가격시점 명시 + 단위(원/㎡, 천원 등) 정확히
[5] 모범답안: Ⅰ. 평가개요 → Ⅱ. 물음별 풀이 (감칙 조문 인용 → 공식 → 수치) → Ⅲ. 결정
[6] 실제 부동산 평가에서 가능한 시나리오 (비현실적 수치 X)
[7] 회차·연도 표기 X. 시나리오에서 가공된 일자 사용 (예: "2024.05.30")

스타일 (실제 기출 톤):
- "감정평가사 ○○씨는 ... 평가의뢰를 받고 ..." 도입
- 자료마다 [ 자료 01 ], [ 자료 02 ] 번호 부여
- 물음은 1) 2) 3) 형식 (배점 명시)

출력: JSON 한 덩어리만 (앞뒤 설명 텍스트 X, ```json fence도 X)
"""

NEW_USER = """[단원] {chapter_title}

[이 단원의 기존 기출 — few-shot 예시]
{seed_examples}

위 단원에서 나올 수 있는 **새로운 시나리오·논점**을 다룬 실전형 시험 문제를 1개 만드세요.
- 위 예시와 유사한 출제 형식·구조·길이를 따르되, 시나리오·자료·물음은 달라야 함
- 단원 주제({chapter_topic_hint})의 핵심 논점 중 하나를 깊게 묻기

다음 JSON 형식으로만 출력:
{{
  "body": "문제 본문 — 평가의뢰 개요 + 자료 3~5개 + 물음 1)~3)~5) (실제 시험지 길이, 1500자 이상)",
  "modelAnswer": "모범답안 — Ⅰ. 평가개요 + Ⅱ. 물음별 풀이 + Ⅲ. 결정 (수치 계산 포함, 1000자 이상)",
  "points": <int, 25~40 사이>,
  "topic": "이 문제가 다루는 핵심 논점 한 문장",
  "noveltyVsOriginal": "기존 기출과 어떻게 다른지 한 문장"
}}
"""

# 단원 주제 힌트 (new 모드의 prompt 다양성용 — 매 호출마다 random pick으로 분산)
CHAPTER_TOPIC_HINTS = {
    '1': ['금융계수·할인율 활용', '면적·환산·체감률', '실무 기초 수학 응용'],
    '2a': ['공시지가기준법 + 거래사례비교', '원가법 토지·건물 평가', '비교표 활용 + 그 밖의 요인',
           '공법상 제한 토지 평가', '담보·일반거래 목적 평가'],
    '2b': ['수익환원법 (직접환원·DCF)', '임대료 평가 + 임대 사례', '복합부동산 임대료'],
    '3':  ['구분소유 부동산', '복합부동산 일괄·구분 평가', '임대료 다양한 산정법'],
    '4':  ['유형별 평가 — 기계기구·광업권', '비특수 부동산 vs 특수 부동산', '농지·임야 평가'],
    '5':  ['비가치추계 (재구축비·재조달원가)', '기업가치 평가 + 비상장주식', '무형자산 (영업권·특허)'],
    '6a': ['토지보상 기본원칙·기준', '비교표준지 선정 + 그 밖의 요인', '시점수정 + 개별요인 비교'],
    '6b': ['공법상 제한 토지 보상', '미지급용지·환매', '도시계획시설 토지 보상 + 잔여지'],
    '7':  ['건축물 보상 (이전비·물건가격)', '영업보상 + 휴업·폐업', '농업·축산·이주대책·생활보상'],
    '8a': ['담보평가 (대출 가능금액)', '경매·국공유재산 처분', '소송감정·법원 평가'],
    '8b': ['표준지 공시지가 평가', '정비사업 (재개발·재건축)', '불의의 타격 보상'],
}


def call_anthropic(api_key: str, model: str, system: str, user: str, max_tokens: int = 4096):
    body = json.dumps({
        'model': model,
        'max_tokens': max_tokens,
        'system': system,
        'messages': [{'role': 'user', 'content': user}],
    }).encode('utf-8')
    req = urllib.request.Request(
        API_URL,
        data=body,
        method='POST',
        headers={
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'HTTP {e.code}: {err[:300]}')
    return data


def extract_json(text: str):
    """LLM 출력에서 JSON 객체 추출. ```json fence나 ``` 제거."""
    s = text.strip()
    if s.startswith('```'):
        # remove first fence line + last fence
        lines = s.split('\n')
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith('```'):
            lines = lines[:-1]
        s = '\n'.join(lines).strip()
    # Try direct parse
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    # Find {...} block heuristically
    start = s.find('{')
    end = s.rfind('}')
    if start >= 0 and end > start:
        try:
            return json.loads(s[start:end+1])
        except json.JSONDecodeError as e:
            raise RuntimeError(f'JSON parse fail: {e} — content head: {s[:200]}')
    raise RuntimeError(f'No JSON in response: {s[:200]}')


def short_id(s: str) -> str:
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:8]


def load_chapter(chapter_id: str):
    path = DATA_DIR / f'{chapter_id}.json'
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8'))


def load_generated(chapter_id: str):
    path = DATA_DIR / f'{chapter_id}-generated.json'
    if not path.exists():
        return {'built_at': None, 'chapter': chapter_id, 'questions': []}
    return json.loads(path.read_text(encoding='utf-8'))


def save_generated(chapter_id: str, payload: dict):
    path = DATA_DIR / f'{chapter_id}-generated.json'
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')


def update_manifest():
    mpath = DATA_DIR / 'manifest.json'
    m = json.loads(mpath.read_text(encoding='utf-8'))
    for c in m['chapters']:
        gpath = DATA_DIR / f'{c["id"]}-generated.json'
        if gpath.exists():
            g = json.loads(gpath.read_text(encoding='utf-8'))
            c['generatedCount'] = len(g.get('questions', []))
        else:
            c['generatedCount'] = 0
    mpath.write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')


def vary_one(api_key, model, chapter_data, seed_q, dry_run=False):
    user = VARY_USER.format(
        chapter_title=chapter_data['chapterTitle'],
        round=seed_q['round'],
        questionNum=seed_q['questionNum'],
        points=seed_q['points'] or 30,
        body=seed_q['body'][:2500],   # 너무 길면 잘라서 토큰 절약
        model_answer=(seed_q.get('modelAnswer') or '(원본 답안 없음)')[:3000],
    )
    if dry_run:
        return {'_dryrun_prompt_chars': len(user)}
    resp = call_anthropic(api_key, model, VARY_SYSTEM, user)
    text = ''.join(b.get('text', '') for b in resp.get('content', []))
    obj = extract_json(text)
    return obj


def new_one(api_key, model, chapter_data, seeds, dry_run=False, topic_idx=0):
    """new 문제 1개 생성. seeds 중 2개를 few-shot 예시로 전체 body·answer 제시."""
    import random
    # few-shot: 답안 있는 seeds 중 2개를 골라 전체 본문+답안 노출
    full_seeds = [s for s in seeds if s.get('modelAnswer')]
    picks = full_seeds[:2] if len(full_seeds) >= 2 else seeds[:2]
    examples = []
    for i, q in enumerate(picks):
        ex = (
            f"--- 예시 {i+1} ({q['points'] or '미명시'}점) ---\n"
            f"[문제 본문]\n{q['body'][:1800]}\n"
        )
        if q.get('modelAnswer'):
            ex += f"\n[모범답안 발췌]\n{q['modelAnswer'][:1500]}\n"
        examples.append(ex)
    seed_text = '\n'.join(examples) if examples else '(이 단원에 참고 가능한 기출이 없음 — 일반 감정평가실무 패턴으로 출제)'

    # topic hint — 다양성을 위해 호출마다 다른 hint 사용
    hints = CHAPTER_TOPIC_HINTS.get(chapter_data['chapter'], ['일반 감정평가실무'])
    topic_hint = hints[topic_idx % len(hints)]

    user = NEW_USER.format(
        chapter_title=chapter_data['chapterTitle'],
        seed_examples=seed_text,
        chapter_topic_hint=topic_hint,
    )
    if dry_run:
        return {'_dryrun_prompt_chars': len(user), 'topic_hint': topic_hint}
    resp = call_anthropic(api_key, model, NEW_SYSTEM, user, max_tokens=6000)
    text = ''.join(b.get('text', '') for b in resp.get('content', []))
    obj = extract_json(text)
    obj['_topicHint'] = topic_hint
    return obj


def estimate_cost(model, vary_calls, new_calls):
    """대략적 비용 추정 (Sonnet 4.5 기준)."""
    if 'opus' in model.lower():
        per_vary, per_new = 0.06, 0.10  # opus
    elif 'haiku' in model.lower():
        per_vary, per_new = 0.005, 0.01
    else:
        per_vary, per_new = 0.02, 0.04  # sonnet
    cost = vary_calls * per_vary + new_calls * per_new
    return cost


def main():
    p = argparse.ArgumentParser(description='2차 essay AI 변형/신규 문제 생성')
    p.add_argument('--chapter', help='단원 ID (예: 2a). --all과 둘 중 하나 필수')
    p.add_argument('--all', action='store_true', help='모든 단원 처리')
    p.add_argument('--mode', choices=['vary', 'new', 'both'], default='vary')
    p.add_argument('--count', type=int, default=2, help='vary: seed당 변형 수 / new: 단원당 신규 수')
    p.add_argument('--target', type=int,
                   help='단원당 목표 총 문제수. set이면 mode/count 무시, vary 40%% + new 60%%로 자동 분배')
    p.add_argument('--model', default=DEFAULT_MODEL)
    p.add_argument('--dry-run', action='store_true', help='API 호출 X, prompt 길이만 출력')
    p.add_argument('--resume', action='store_true', help='기존 generated.json 유지 + 추가')
    p.add_argument('--sleep', type=float, default=1.0, help='API 호출 사이 대기(초)')
    p.add_argument('--yes', action='store_true', help='비용 확인 프롬프트 건너뛰기')
    args = p.parse_args()

    if not args.chapter and not args.all:
        p.error('--chapter 또는 --all 중 하나 필수')

    api_key = os.environ.get('ANTHROPIC_API_KEY', '').strip()
    if not args.dry_run and not api_key:
        print('ERROR: ANTHROPIC_API_KEY 환경변수 필요', file=sys.stderr)
        print('  export ANTHROPIC_API_KEY=sk-ant-...', file=sys.stderr)
        sys.exit(1)

    if not DATA_DIR.exists():
        print(f'ERROR: {DATA_DIR} 없음. 먼저 build_essay.py 실행', file=sys.stderr)
        sys.exit(1)

    manifest = json.loads((DATA_DIR / 'manifest.json').read_text(encoding='utf-8'))
    chapter_ids = [c['id'] for c in manifest['chapters']]
    if args.chapter:
        if args.chapter not in chapter_ids:
            print(f'ERROR: 단원 {args.chapter} 없음. 가능: {chapter_ids}', file=sys.stderr)
            sys.exit(1)
        target_ids = [args.chapter]
    else:
        target_ids = chapter_ids

    # ─────────── --target 모드: vary+new 자동 분배 ───────────
    plan = {}  # chapter_id → (vary_seed_count, vary_per_seed, new_count)
    if args.target:
        for cid in target_ids:
            ch = load_chapter(cid)
            if not ch: continue
            gen_existing = load_generated(cid) if args.resume else {'questions': []}
            already = len(gen_existing.get('questions', []))
            need = max(0, args.target - already)
            seeds_with_ans = [q for q in ch['questions'] if q.get('modelAnswer')]
            # 40% vary (안전, 답안 있는 seed당 1개씩 우선) + 60% new (다양성)
            vary_target = min(int(need * 0.4), len(seeds_with_ans) * 3)
            vary_per_seed = max(1, (vary_target // max(1, len(seeds_with_ans)))) if seeds_with_ans else 0
            actual_vary = vary_per_seed * len(seeds_with_ans) if seeds_with_ans else 0
            new_count = max(0, need - actual_vary)
            plan[cid] = (len(seeds_with_ans), vary_per_seed, new_count)
        total_vary = sum(s * v for s, v, _ in plan.values())
        total_new = sum(n for _, _, n in plan.values())
    else:
        # 기존 mode/count 기반
        for cid in target_ids:
            ch = load_chapter(cid)
            if not ch: continue
            seeds = [q for q in ch['questions'] if q.get('modelAnswer')]
            v = len(seeds) * args.count if args.mode in ('vary', 'both') else 0
            n = args.count if args.mode in ('new', 'both') else 0
            plan[cid] = (len(seeds), args.count if args.mode in ('vary', 'both') else 0, n)
        total_vary = sum(s * v for s, v, _ in plan.values())
        total_new = sum(n for _, _, n in plan.values())

    est_cost = estimate_cost(args.model, total_vary, total_new)
    print(f'\n══════ 작업 계획 ══════')
    print(f'모델: {args.model}')
    print(f'단원: {len(target_ids)}개')
    for cid, (seeds, per_seed, n) in plan.items():
        print(f'  [{cid}] vary {seeds} seed × {per_seed} = {seeds*per_seed} + new {n} = 총 {seeds*per_seed + n}개')
    print(f'\n총 호출: vary {total_vary} + new {total_new} = {total_vary + total_new}회')
    print(f'예상 비용: 약 ${est_cost:.2f} USD (실제는 ±50%)')

    if args.dry_run:
        print('\n[dry-run 종료]')
        sys.exit(0)
    if not args.yes:
        ans = input('\n진행하시겠습니까? (y/N): ').strip().lower()
        if ans != 'y':
            print('취소됨')
            sys.exit(0)

    total_calls = 0
    total_saved = 0
    for chapter_id in target_ids:
        ch = load_chapter(chapter_id)
        if not ch:
            continue
        seeds_count, vary_per_seed, new_count = plan.get(chapter_id, (0, 0, 0))
        print(f'\n=== {chapter_id} · {ch["chapterTitle"]} (vary {seeds_count}×{vary_per_seed} + new {new_count}) ===')
        gen = load_generated(chapter_id) if args.resume else {
            'built_at': datetime.now(timezone.utc).isoformat(),
            'chapter': chapter_id,
            'chapterTitle': ch['chapterTitle'],
            'questions': [],
        }
        existing_seeds = {q.get('seedQuestionId') for q in gen['questions'] if q.get('seedQuestionId')}
        existing_topics = {q.get('topic') for q in gen['questions'] if q.get('topic')}

        # vary 모드
        if vary_per_seed > 0:
            seeds = [q for q in ch['questions'] if q.get('modelAnswer')]
            for seed in seeds:
                seed_id = seed['id']
                # resume 시 이미 충분히 생성된 seed는 skip
                made_for_seed = sum(1 for q in gen['questions']
                                    if q.get('seedQuestionId') == seed_id and q.get('genMode') == 'vary')
                need = max(0, vary_per_seed - made_for_seed) if args.resume else vary_per_seed
                for _n in range(need):
                    try:
                        obj = vary_one(api_key, args.model, ch, seed, dry_run=args.dry_run)
                        if args.dry_run:
                            print(f'    [dry] seed={seed_id} prompt={obj["_dryrun_prompt_chars"]}자')
                            total_calls += 1
                            continue
                        new_q = {
                            'id': f'ai-vary-{seed_id}-{short_id(json.dumps(obj, ensure_ascii=False))}',
                            'subject': ch.get('subject', '감정평가실무'),
                            'chapter': chapter_id,
                            'source': 'ai-generated',
                            'genMode': 'vary',
                            'aiModel': args.model,
                            'aiTimestamp': datetime.now(timezone.utc).isoformat(),
                            'seedQuestionId': seed_id,
                            'round': None,
                            'questionNum': None,
                            'points': obj.get('points', seed.get('points')),
                            'body': obj['body'],
                            'modelAnswer': obj.get('modelAnswer'),
                            'modelAnswerSource': 'ai-generated',
                            'changedFromOriginal': obj.get('changedFromOriginal'),
                        }
                        gen['questions'].append(new_q)
                        total_calls += 1
                        total_saved += 1
                        print(f'    ✓ vary {seed_id} → {new_q["id"][:30]}…')
                        save_generated(chapter_id, gen)  # 매번 저장 (중간 실패 안전)
                        time.sleep(args.sleep)
                    except Exception as e:
                        print(f'    ✗ vary {seed_id} 실패: {e}', file=sys.stderr)
                        time.sleep(args.sleep * 2)

        # new 모드: 단원당 N개 신규
        if new_count > 0:
            seeds = ch['questions'][:5]
            already_new = sum(1 for q in gen['questions'] if q.get('genMode') == 'new')
            need = max(0, new_count - already_new) if args.resume else new_count
            print(f'  [new] {need}개 신규 생성 (topic hint rotation)')
            for n in range(need):
                try:
                    obj = new_one(api_key, args.model, ch, seeds, dry_run=args.dry_run, topic_idx=n + already_new)
                    if args.dry_run:
                        print(f'    [dry] new prompt={obj["_dryrun_prompt_chars"]}자')
                        total_calls += 1
                        continue
                    topic = obj.get('topic', '')
                    if topic in existing_topics:
                        print(f'    ⚠ topic 중복, skip: {topic}')
                        continue
                    new_q = {
                        'id': f'ai-new-{chapter_id}-{short_id(json.dumps(obj, ensure_ascii=False))}',
                        'subject': ch.get('subject', '감정평가실무'),
                        'chapter': chapter_id,
                        'source': 'ai-generated',
                        'genMode': 'new',
                        'aiModel': args.model,
                        'aiTimestamp': datetime.now(timezone.utc).isoformat(),
                        'seedQuestionId': None,
                        'round': None,
                        'questionNum': None,
                        'points': obj.get('points', 30),
                        'body': obj['body'],
                        'modelAnswer': obj.get('modelAnswer'),
                        'modelAnswerSource': 'ai-generated',
                        'topic': topic,
                        'noveltyVsOriginal': obj.get('noveltyVsOriginal'),
                    }
                    gen['questions'].append(new_q)
                    existing_topics.add(topic)
                    total_calls += 1
                    total_saved += 1
                    print(f'    ✓ new → {topic[:50]}')
                    save_generated(chapter_id, gen)
                    time.sleep(args.sleep)
                except Exception as e:
                    print(f'    ✗ new 실패: {e}', file=sys.stderr)
                    time.sleep(args.sleep * 2)

    if not args.dry_run:
        update_manifest()
        print(f'\n총 API 호출: {total_calls}, 저장: {total_saved}')
        print(f'manifest.json 갱신 완료')
    else:
        print(f'\n[dry-run] 총 {total_calls}회 호출 예정. 실제 실행 시 --dry-run 제거')


if __name__ == '__main__':
    main()
