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
THEORY_DIR = Path('최종산출물/2과목_2차_감정평가실무')
DEFAULT_MODEL = 'claude-sonnet-4-5'  # 안정·저렴. 더 어려운 신규 문제는 opus 권장
API_URL = 'https://api.anthropic.com/v1/messages'

# ─────────── 프롬프트 템플릿 ───────────

VARY_SYSTEM = """당신은 한국 감정평가사 2차 시험 출제위원입니다.
기존 기출문제와 동일한 논점·계산 패턴을 묻되, 시나리오와 수치만 바꾼 변형 문제를 만들어야 합니다.

원칙:
- 실제 시험 출제 스타일 (조건 제시 → 자료 → 물음) 유지
- 회차·연도 표기 X (예: "○○회", "2024년" 등 사용 금지)
- 모범답안은 동일한 풀이 패턴이 적용되도록 수치 조정
- 변형이 사소하지 않게 의미 있는 차이(다른 부동산 유형, 다른 보상 조건 등)
- 출력은 반드시 JSON 한 덩어리 (앞뒤 설명 텍스트 금지)
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
주어진 단원의 이론·기출 패턴을 참고해 새로운 논점의 시험 문제를 만들어야 합니다.

원칙:
- 실제 시험 출제 스타일 (조건 제시 → 자료 → 물음)
- 기존 기출과 중복되지 않는 새로운 논점
- 회차·연도 표기 X
- 모범답안은 답안 작성 양식(Ⅰ. 평가개요 / Ⅱ. 물음1 등) 따라 충실히
- 적정 배점 25-40점 사이
- 출력은 반드시 JSON 한 덩어리 (앞뒤 설명 텍스트 금지)
"""

NEW_USER = """[단원] {chapter_title}
[기존 기출의 논점 패턴 (참고용, 중복 회피)]
{seed_summaries}

위 단원에서 나올 수 있는 새로운 논점을 다룬 시험 문제를 1개 만드세요.

다음 JSON 형식으로만 출력:
{{
  "body": "문제 본문",
  "modelAnswer": "모범답안",
  "points": <int, 25~40 사이>,
  "topic": "이 문제가 다루는 핵심 논점 한 문장",
  "noveltyVsOriginal": "기존 기출과 어떻게 다른지 한 문장"
}}
"""


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


def new_one(api_key, model, chapter_data, seeds, dry_run=False):
    # 기존 기출 요약 (최대 3개)
    summaries = []
    for i, q in enumerate(seeds[:3]):
        summary = q['body'][:200].replace('\n', ' ')
        summaries.append(f'  {i+1}. {q["round"]}회 {q["questionNum"]}번 ({q["points"]}점): {summary}…')
    seed_text = '\n'.join(summaries) if summaries else '(참고할 기출 없음)'
    user = NEW_USER.format(
        chapter_title=chapter_data['chapterTitle'],
        seed_summaries=seed_text,
    )
    if dry_run:
        return {'_dryrun_prompt_chars': len(user)}
    resp = call_anthropic(api_key, model, NEW_SYSTEM, user)
    text = ''.join(b.get('text', '') for b in resp.get('content', []))
    obj = extract_json(text)
    return obj


def main():
    p = argparse.ArgumentParser(description='2차 essay AI 변형/신규 문제 생성')
    p.add_argument('--chapter', help='단원 ID (예: 2a). --all과 둘 중 하나 필수')
    p.add_argument('--all', action='store_true', help='모든 단원 처리')
    p.add_argument('--mode', choices=['vary', 'new', 'both'], default='vary')
    p.add_argument('--count', type=int, default=2, help='vary: seed당 변형 수 / new: 단원당 신규 수')
    p.add_argument('--model', default=DEFAULT_MODEL)
    p.add_argument('--dry-run', action='store_true', help='API 호출 X, prompt 길이만 출력')
    p.add_argument('--resume', action='store_true', help='기존 generated.json 유지 + 추가')
    p.add_argument('--sleep', type=float, default=1.0, help='API 호출 사이 대기(초)')
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

    total_calls = 0
    total_saved = 0
    for chapter_id in target_ids:
        ch = load_chapter(chapter_id)
        if not ch:
            continue
        print(f'\n=== {chapter_id} · {ch["chapterTitle"]} ({len(ch["questions"])}문항) ===')
        gen = load_generated(chapter_id) if args.resume else {
            'built_at': datetime.now(timezone.utc).isoformat(),
            'chapter': chapter_id,
            'chapterTitle': ch['chapterTitle'],
            'questions': [],
        }
        existing_seeds = {q.get('seedQuestionId') for q in gen['questions'] if q.get('seedQuestionId')}
        existing_topics = {q.get('topic') for q in gen['questions'] if q.get('topic')}

        # vary 모드: 각 seed 문제에 대해 count개 변형
        if args.mode in ('vary', 'both'):
            seeds = [q for q in ch['questions'] if q.get('modelAnswer')]  # 답안 있는 것만
            print(f'  [vary] {len(seeds)}개 seed × {args.count} 변형 = {len(seeds)*args.count} 콜')
            for seed in seeds:
                seed_id = seed['id']
                # resume 시 이미 충분히 생성된 seed는 skip
                made_for_seed = sum(1 for q in gen['questions']
                                    if q.get('seedQuestionId') == seed_id and q.get('genMode') == 'vary')
                need = max(0, args.count - made_for_seed) if args.resume else args.count
                for n in range(need):
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

        # new 모드: 단원당 count개 신규
        if args.mode in ('new', 'both'):
            seeds = ch['questions'][:5]
            already_new = sum(1 for q in gen['questions'] if q.get('genMode') == 'new')
            need = max(0, args.count - already_new) if args.resume else args.count
            print(f'  [new] {need}개 신규 생성')
            for n in range(need):
                try:
                    obj = new_one(api_key, args.model, ch, seeds, dry_run=args.dry_run)
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
