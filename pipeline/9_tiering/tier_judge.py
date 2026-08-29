#!/usr/bin/env python3
"""LLM 앵커 판정 — 감평 기출을 옆에 놓고 A/B/discard/repair 를 정한다.

앵커가 있어야 '어렵다'가 감평 시험 기준에 고정된다. 앵커 없이 물으면
모델의 감각이 시험과 무관하게 표류한다.

멱등·재개 가능: 이미 tier 가 있으면 건너뛴다. CKPT_EVERY 마다 저장한다.
환경: GEMINI_API_KEY 필요.

사용:
  python3 pipeline/9_tiering/tier_judge.py [--limit 50] [--sample 20] [--model gemini-2.5-flash] [--self-test]

--sample N 은 판정 대상을 앵커 수준(item/section/chapter/none) 4무리로 나눠 고르게 N개를 뽑는다
(seed=42 고정, 재현 가능). --limit 은 앞에서부터 자르는 기존 방식 그대로 남겨둔다.
"""
import json
import os
import random
import re
import shutil
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_anchors import pick_anchors            # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
ANCHORS = Path(__file__).resolve().parent / "anchors_econ.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"
CKPT_EVERY = 25
MAX_RETRIES = 3
CONSECUTIVE_FAIL_LIMIT = 20
CALL_INTERVAL = 0.3
VALID_TIERS = {"A", "B", "discard", "repair"}
DEFAULT_MODELS = {"gemini": "gemini-2.5-flash", "openai": "gpt-4o-mini"}
OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def _atomic_write_json(path, data):
    """임시 파일에 쓰고 os.replace 로 원자적 치환한다. 중간에 죽어도 원본은 안전하다."""
    tmp = path.parent / (path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)

RUBRIC = """너는 한국 감정평가사 1차 경제학원론 출제위원이다.
아래 [대상 문항]을 [감평 기출 앵커]와 견주어 등급을 정한다.

먼저 품질을 본다. 하나라도 걸리면 품질 탈락이다.
1. 정답 유일성 — 복수정답·무정답이 없다
2. 개념·계산 정확성 — 해설의 계산이 실제로 맞고 개념 서술에 오류가 없다
3. 해설 완결성 — 왜 정답인지와 왜 오답인지가 모두 있다
4. 출제 범위 적합 — 감정평가사 1차 경제학원론 범위 안이다

품질 탈락일 때:
- 개념·계산이 틀렸거나 범위를 벗어났으면 "discard"
- 내용은 멀쩡한데 본문이 장황하거나 해설만 부실하면 "repair"

품질을 통과하면 난이도를 본다.
- "A" = 단일 개념, 정의 확인 또는 1단계 계산, 함정 없음, 오답이 명백히 다른 개념
- "B" = 2개 이상 개념 결합 또는 2단계 이상 계산, 오답이 흔한 오개념을 찌른다

애매하면 A로 내린다. B의 신뢰도가 이 체계의 핵심이다.

출력은 이 JSON 하나만. 다른 말 금지.
{"tier": "A|B|discard|repair", "reason": "한 문장 근거"}"""


def build_prompt(q, anchors):
    lines = [RUBRIC, "", "[감평 기출 앵커]"]
    if anchors:
        for a in anchors:
            lines.append(f"- ({a.get('exam')} {a.get('year')}) {a.get('question')}")
            lines.append(f"  선지: {a.get('options')}  정답: {a.get('answer')}")
    else:
        lines.append("(이 단원에는 기출 앵커가 없다. 감평 1차 경제학의 일반적 난이도를 기준으로 판단한다.)")
    lines += ["", "[대상 문항]", str(q.get("question")),
              f"선지: {q.get('options')}", f"정답: {q.get('answer')}",
              f"해설: {q.get('explanation')}"]
    return "\n".join(lines)


ANCHOR_LEVELS = ("item", "section", "chapter", "none")


def anchor_taxonomy(q):
    """pick_anchors 에 넘길 mapped_taxonomy 사본을 만든다.

    fix_hq_taxonomy.py 가 키워드 매칭 실패로 "fallback"(그 절의 첫 관에 기계적
    배정) 처리한 문항은 item 이 내용과 무관할 수 있으므로, 앵커 선택에서는
    item 을 지워 절(section) 수준으로 내려가게 한다. 원본 mt 는 건드리지 않는다.
    """
    iv = q.get("indexing_v4") or {}
    mt = dict(iv.get("mapped_taxonomy") or {})
    if iv.get("item_assigned_by") == "fallback":
        mt.pop("item", None)
    return mt


def stratified_sample(targets, index, n, seed=42):
    """판정 대상을 앵커 수준(item/section/chapter/none) 4무리로 나눠 고르게 n개를 뽑는다.

    무리가 n/4보다 적으면 있는 만큼만 쓰고 부족분은 다른 무리에서 채운다.
    """
    groups = {lvl: [] for lvl in ANCHOR_LEVELS}
    for q in targets:
        mt = anchor_taxonomy(q)
        _, level = pick_anchors(index, mt)
        groups[level].append(q)
    rng = random.Random(seed)
    for g in groups.values():
        rng.shuffle(g)
    base, extra = divmod(n, len(ANCHOR_LEVELS))
    picked, leftover = [], []
    for i, lvl in enumerate(ANCHOR_LEVELS):
        want = base + (1 if i < extra else 0)
        picked.extend(groups[lvl][:want])
        leftover.extend(groups[lvl][want:])
    if len(picked) < n:
        picked.extend(leftover[: n - len(picked)])
    return picked[:n]


def parse_verdict(text):
    """모델 응답에서 판정 JSON을 꺼낸다. 형식이 어긋나면 None.

    reason 안에 '}' 가 들어있으면 비탐욕 매칭이 잘라먹으므로 탐욕 매칭을 먼저
    시도하고(전체 텍스트에서 첫 '{' ~ 마지막 '}'), 실패하면 비탐욕으로 폴백한다.
    """
    text = text or ""
    v = None
    for pattern in (r"\{.*\}", r"\{.*?\}"):
        m = re.search(pattern, text, re.S)
        if not m:
            continue
        try:
            v = json.loads(m.group(0))
            break
        except json.JSONDecodeError:
            continue
    if v is None:
        return None
    if v.get("tier") not in VALID_TIERS:
        return None
    if not str(v.get("reason") or "").strip():
        return None      # 근거 없는 판정은 받지 않는다
    return {"tier": v["tier"], "reason": v["reason"]}


def _call_with_retry(call_fn, prompt, max_retries=MAX_RETRIES):
    """최대 max_retries 회, 지수 백오프(2s→4s→8s)로 재시도한다. 다 실패하면 마지막 예외를 던진다.

    call_fn(prompt) -> 응답 텍스트. provider 별 호출부는 call_fn 안에 숨기고
    재시도·백오프·연속실패 판단은 여기 하나로 공유한다.
    """
    delay = 2
    last_exc = None
    for attempt in range(max_retries):
        try:
            return call_fn(prompt)
        except Exception as e:
            last_exc = e
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
    raise last_exc


def _extract_openai_text(resp_json):
    """OpenAI chat/completions 응답 JSON에서 본문 텍스트를 꺼낸다. 네트워크 없이 단위테스트 가능."""
    return resp_json["choices"][0]["message"]["content"]


def _make_openai_call_fn(model_name, api_key):
    def call_fn(prompt):
        r = requests.post(
            OPENAI_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model_name, "temperature": 0,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=60,
        )
        r.raise_for_status()
        return _extract_openai_text(r.json()) or ""
    return call_fn


def _make_gemini_call_fn(model):
    def call_fn(prompt):
        r = model.generate_content(prompt, generation_config={"temperature": 0})
        return r.text or ""
    return call_fn


def run_calibrate(db, index, call_fn, n, seed=42):
    """이미 gemini 로 판정된 문항 n건을 다른 provider(call_fn)로 재판정해 일치율만 잰다.

    DB 는 읽기만 한다 — 여기서 db 딕셔너리를 바꿔도 호출자가 파일에 쓰지 않으면 그만이지만,
    확실히 하기 위해 아예 db 를 수정하지 않는다.
    """
    pool = [q for q in db if str((q.get("tier_meta") or {}).get("decided_by", "")).startswith("gemini:")]
    sample = stratified_sample(pool, index, n, seed=seed)
    results = []
    for q in sample:
        mt = anchor_taxonomy(q)
        anchors, _level = pick_anchors(index, mt)
        text = _call_with_retry(call_fn, build_prompt(q, anchors))
        v = parse_verdict(text)
        results.append({
            "id": q.get("id"),
            "old_tier": q.get("tier"),
            "old_reason": (q.get("tier_meta") or {}).get("reason"),
            "new_tier": v["tier"] if v else None,
            "new_reason": v["reason"] if v else None,
        })
    return results


def print_calibration_report(results):
    n = len(results)
    agree = sum(1 for r in results if r["new_tier"] is not None and r["new_tier"] == r["old_tier"])
    scored = sum(1 for r in results if r["new_tier"] is not None)
    print(f"\n교차검증 {n}건 · 일치 {agree}/{scored} ({(agree / scored * 100 if scored else 0):.1f}%) · 판정실패 {n - scored}")

    confusion = Counter((r["old_tier"], r["new_tier"]) for r in results)
    print("혼동 행렬 (gemini → openai):")
    for (old, new), cnt in sorted(confusion.items(), key=lambda kv: -kv[1]):
        print(f"  {old} → {new}: {cnt}")

    mismatches = [r for r in results if r["new_tier"] is not None and r["new_tier"] != r["old_tier"]]
    print(f"\n불일치 사례 (최대 5건, 전체 {len(mismatches)}건):")
    for r in mismatches[:5]:
        print(f"  [{r['id']}] gemini={r['old_tier']} ({r['old_reason']})")
        print(f"           openai={r['new_tier']} ({r['new_reason']})")


def _self_test():
    # 정상 응답 파싱
    v = parse_verdict('```json\n{"tier":"B","reason":"두 개념 결합"}\n```')
    assert v == {"tier": "B", "reason": "두 개념 결합"}

    # 마커 없는 순수 JSON 도 받는다
    v = parse_verdict('{"tier":"A","reason":"단일 개념"}')
    assert v["tier"] == "A"

    # 허용되지 않은 등급은 거부한다
    assert parse_verdict('{"tier":"C","reason":"x"}') is None
    assert parse_verdict('{"tier":"S","reason":"x"}') is None

    # 사유가 없으면 거부한다 — 근거 없는 판정은 남기지 않는다
    assert parse_verdict('{"tier":"A"}') is None

    # 쓰레기 응답
    assert parse_verdict("모르겠습니다") is None

    # reason 안에 '}' 가 있어도(비탐욕 매칭이면 잘려서 깨졌을 응답) 탐욕 매칭으로 제대로 파싱한다
    v = parse_verdict('{"tier":"A","reason":"보기 } 안에 함정이 있다"}')
    assert v == {"tier": "A", "reason": "보기 } 안에 함정이 있다"}

    # 원자적 저장 — 임시 파일이 남지 않고 내용이 실제로 바뀐다
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "db.json"
        p.write_text("[]", encoding="utf-8")
        _atomic_write_json(p, [{"a": 1}])
        assert json.loads(p.read_text(encoding="utf-8")) == [{"a": 1}]
        assert not (Path(td) / "db.json.tmp").exists()

    # 프롬프트에 앵커 본문과 대상 문항이 모두 들어간다
    q = {"question": "대상문항본문", "options": ["1", "2", "3", "4", "5"],
         "answer": "1", "explanation": "해설본문"}
    p = build_prompt(q, [{"question": "앵커본문", "options": ["a"], "answer": "1",
                          "exam": "감정평가사", "year": "2020"}])
    assert "대상문항본문" in p and "앵커본문" in p and "해설본문" in p

    # fallback 배정된 관은 앵커 선택에서 신뢰하지 않는다 — item 을 지우고 절로 내려간다
    index_fb = {"item::엉뚱한관": [{"id": "wrong"}], "section::제13절 완전경쟁시장": [{"id": "right"}]}
    q_fb = {"indexing_v4": {"item_assigned_by": "fallback",
            "mapped_taxonomy": {"item": "엉뚱한관", "section": "제13절 완전경쟁시장", "chapter": "장"}}}
    mt_fb = anchor_taxonomy(q_fb)
    assert "item" not in mt_fb
    anchors_fb, level_fb = pick_anchors(index_fb, mt_fb)
    assert level_fb == "section" and [a["id"] for a in anchors_fb] == ["right"]
    # 원본 mapped_taxonomy 는 변형하지 않는다
    assert q_fb["indexing_v4"]["mapped_taxonomy"]["item"] == "엉뚱한관"

    # keyword 로 배정된 관은 그대로 신뢰한다
    q_kw = {"indexing_v4": {"item_assigned_by": "keyword",
            "mapped_taxonomy": {"item": "엉뚱한관", "section": "제13절 완전경쟁시장", "chapter": "장"}}}
    assert anchor_taxonomy(q_kw).get("item") == "엉뚱한관"

    # 층화 표본 — 4무리(item/section/chapter/none)가 충분하면 고르게 5개씩
    def _q(id_, item, section, chapter):
        return {"id": id_, "indexing_v4": {"mapped_taxonomy":
                {"item": item, "section": section, "chapter": chapter}}}

    idx = {"item::A": [{"id": "x1"}], "section::B": [{"id": "x2"}],
           "chapter::C": [{"id": "x3"}]}
    targets = ([_q(f"item{i}", "A", "B", "C") for i in range(10)]
               + [_q(f"sec{i}", "Z", "B", "C") for i in range(10)]
               + [_q(f"chap{i}", "Z", "Y", "C") for i in range(10)]
               + [_q(f"none{i}", "Z", "Y", "X") for i in range(10)])

    def _level_counts(sample):
        c = Counter()
        for q in sample:
            mt = q["indexing_v4"]["mapped_taxonomy"]
            _, lvl = pick_anchors(idx, mt)
            c[lvl] += 1
        return c

    sample = stratified_sample(targets, idx, 20, seed=42)
    assert len(sample) == 20
    assert _level_counts(sample) == {"item": 5, "section": 5, "chapter": 5, "none": 5}

    # 재현 가능 — 같은 시드면 같은 결과
    assert [q["id"] for q in sample] == [q["id"] for q in stratified_sample(targets, idx, 20, seed=42)]

    # 무리가 부족하면 있는 만큼만 쓰고 나머지 무리에서 채운다
    short_targets = ([_q(f"item{i}", "A", "B", "C") for i in range(2)]
                      + [_q(f"sec{i}", "Z", "B", "C") for i in range(10)]
                      + [_q(f"chap{i}", "Z", "Y", "C") for i in range(10)]
                      + [_q(f"none{i}", "Z", "Y", "X") for i in range(10)])
    sample2 = stratified_sample(short_targets, idx, 20, seed=42)
    assert len(sample2) == 20
    assert _level_counts(sample2)["item"] == 2

    # OpenAI 응답 형태에서 텍스트를 제대로 꺼낸다
    resp = {"choices": [{"message": {"content": '{"tier":"A","reason":"단일 개념"}'}}]}
    assert _extract_openai_text(resp) == '{"tier":"A","reason":"단일 개념"}'

    # _call_with_retry 는 call_fn 이 성공하면 그대로 반환한다
    assert _call_with_retry(lambda p: "ok:" + p, "prompt") == "ok:prompt"

    # --calibrate 는 DB 를 쓰지 않는다 — 파일 내용·mtime 이 호출 전후로 그대로다
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        db_path = Path(td) / "db.json"
        idx_path = Path(td) / "anchors.json"
        calib_db = [
            {"id": "q1", "tier": "A", "tier_meta": {"decided_by": "gemini:x", "reason": "이유1"},
             "indexing_v4": {"mapped_taxonomy": {"item": "관A", "section": "절A", "chapter": "장A"}}},
            {"id": "q2", "tier": "B", "tier_meta": {"decided_by": "gemini:x", "reason": "이유2"},
             "indexing_v4": {"mapped_taxonomy": {"item": "관B", "section": "절B", "chapter": "장B"}}},
        ]
        db_path.write_text(json.dumps(calib_db, ensure_ascii=False), encoding="utf-8")
        idx_path.write_text("{}", encoding="utf-8")
        before_bytes = db_path.read_bytes()
        before_mtime = db_path.stat().st_mtime_ns

        db_loaded = json.loads(db_path.read_text(encoding="utf-8"))
        index_loaded = json.loads(idx_path.read_text(encoding="utf-8"))
        fake_call_fn = lambda p: '{"tier":"B","reason":"재판정 이유"}'  # noqa: E731
        results = run_calibrate(db_loaded, index_loaded, fake_call_fn, n=2, seed=42)
        assert len(results) == 2
        assert {r["new_tier"] for r in results} == {"B"}

        assert db_path.read_bytes() == before_bytes
        assert db_path.stat().st_mtime_ns == before_mtime

    print("tier_judge self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    provider = "gemini"
    if "--provider" in sys.argv:
        provider = sys.argv[sys.argv.index("--provider") + 1]
    if provider not in DEFAULT_MODELS:
        print(f"알 수 없는 provider: {provider} (gemini|openai)")
        sys.exit(1)

    model_name = DEFAULT_MODELS[provider]
    if "--model" in sys.argv:
        model_name = sys.argv[sys.argv.index("--model") + 1]
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    sample = None
    if "--sample" in sys.argv:
        sample = int(sys.argv[sys.argv.index("--sample") + 1])
    calibrate_n = None
    if "--calibrate" in sys.argv:
        calibrate_n = int(sys.argv[sys.argv.index("--calibrate") + 1])

    if provider == "gemini":
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            print("환경변수 GEMINI_API_KEY 미설정. .env 를 export 하고 재실행.")
            sys.exit(1)
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel(model_name)
        call_fn = _make_gemini_call_fn(model)
    else:
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            print("환경변수 OPENAI_API_KEY 미설정. .env 를 export 하고 재실행.")
            sys.exit(1)
        call_fn = _make_openai_call_fn(model_name, key)

    index = json.loads(ANCHORS.read_text(encoding="utf-8"))

    if calibrate_n:
        db = json.loads(DB.read_text(encoding="utf-8"))
        print(f"교차검증: gemini 판정 문항 중 {calibrate_n}건을 {provider}:{model_name} 로 재판정 (DB 쓰기 없음)")
        results = run_calibrate(db, index, call_fn, calibrate_n)
        print_calibration_report(results)
        return

    db = json.loads(DB.read_text(encoding="utf-8"))
    targets = [q for q in db if not q.get("tier")]
    if sample:
        targets = stratified_sample(targets, index, sample)
    elif limit:
        targets = targets[:limit]
    print(f"판정 대상 {len(targets)}문항 · {provider}:{model_name}")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_judge_{ts}.json")

    now = datetime.now().strftime("%Y-%m-%d")
    tally = Counter()
    api_err = 0
    parse_err = 0
    consecutive_fail = 0
    for i, q in enumerate(targets, 1):
        mt = anchor_taxonomy(q)
        anchors, level = pick_anchors(index, mt)
        try:
            text = _call_with_retry(call_fn, build_prompt(q, anchors))
        except Exception as e:
            api_err += 1
            consecutive_fail += 1
            print(f"  [API 오류] {q.get('id')}: {str(e)[:80]}")
            if consecutive_fail >= CONSECUTIVE_FAIL_LIMIT:
                _atomic_write_json(DB, db)
                print(f"연속 {consecutive_fail}건 실패 — rate limit 또는 인증 문제로 추정, 중단합니다.")
                sys.exit(1)
            continue
        v = parse_verdict(text)
        if not v:
            parse_err += 1
            consecutive_fail += 1
            if consecutive_fail >= CONSECUTIVE_FAIL_LIMIT:
                _atomic_write_json(DB, db)
                print(f"연속 {consecutive_fail}건 실패 — rate limit 또는 인증 문제로 추정, 중단합니다.")
                sys.exit(1)
            continue
        consecutive_fail = 0
        q["tier"] = v["tier"]
        tm = q.get("tier_meta") or {}
        tm.update({"decided_by": f"{provider}:{model_name}", "decided_at": now,
                   "reason": v["reason"],
                   "anchors": [a["id"] for a in anchors],
                   "anchor_level": level,
                   "anchor_fallback": level != "item"})
        q["tier_meta"] = tm
        tally[v["tier"]] += 1
        time.sleep(CALL_INTERVAL)
        if i % CKPT_EVERY == 0:
            _atomic_write_json(DB, db)
            print(f"  …{i}/{len(targets)} {dict(tally)} API오류 {api_err} 파싱오류 {parse_err}")

    _atomic_write_json(DB, db)
    print(f"완료: {dict(tally)} · API오류 {api_err} 파싱오류 {parse_err}")


if __name__ == "__main__":
    main()
