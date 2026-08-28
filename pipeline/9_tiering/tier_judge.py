#!/usr/bin/env python3
"""LLM 앵커 판정 — 감평 기출을 옆에 놓고 A/B/discard/repair 를 정한다.

앵커가 있어야 '어렵다'가 감평 시험 기준에 고정된다. 앵커 없이 물으면
모델의 감각이 시험과 무관하게 표류한다.

멱등·재개 가능: 이미 tier 가 있으면 건너뛴다. CKPT_EVERY 마다 저장한다.
환경: GEMINI_API_KEY 필요.

사용:
  python3 pipeline/9_tiering/tier_judge.py [--limit 50] [--model gemini-2.0-flash] [--self-test]
"""
import json
import os
import re
import shutil
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_anchors import pick_anchors            # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
ANCHORS = Path(__file__).resolve().parent / "anchors_econ.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"
CKPT_EVERY = 25
VALID_TIERS = {"A", "B", "discard", "repair"}

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


def parse_verdict(text):
    """모델 응답에서 판정 JSON을 꺼낸다. 형식이 어긋나면 None."""
    m = re.search(r"\{.*?\}", text or "", re.S)
    if not m:
        return None
    try:
        v = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if v.get("tier") not in VALID_TIERS:
        return None
    if not str(v.get("reason") or "").strip():
        return None      # 근거 없는 판정은 받지 않는다
    return {"tier": v["tier"], "reason": v["reason"]}


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

    # 프롬프트에 앵커 본문과 대상 문항이 모두 들어간다
    q = {"question": "대상문항본문", "options": ["1", "2", "3", "4", "5"],
         "answer": "1", "explanation": "해설본문"}
    p = build_prompt(q, [{"question": "앵커본문", "options": ["a"], "answer": "1",
                          "exam": "감정평가사", "year": "2020"}])
    assert "대상문항본문" in p and "앵커본문" in p and "해설본문" in p
    print("tier_judge self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    model_name = "gemini-2.0-flash"
    if "--model" in sys.argv:
        model_name = sys.argv[sys.argv.index("--model") + 1]
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("환경변수 GEMINI_API_KEY 미설정. .env 를 export 하고 재실행.")
        sys.exit(1)
    import google.generativeai as genai
    genai.configure(api_key=key)
    model = genai.GenerativeModel(model_name)

    db = json.loads(DB.read_text(encoding="utf-8"))
    index = json.loads(ANCHORS.read_text(encoding="utf-8"))
    targets = [q for q in db if not q.get("tier")]
    if limit:
        targets = targets[:limit]
    print(f"판정 대상 {len(targets)}문항 · 모델 {model_name}")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_judge_{ts}.json")

    now = datetime.now().strftime("%Y-%m-%d")
    tally = Counter()
    err = 0
    for i, q in enumerate(targets, 1):
        mt = (q.get("indexing_v4") or {}).get("mapped_taxonomy") or {}
        anchors, level = pick_anchors(index, mt)
        try:
            r = model.generate_content(build_prompt(q, anchors),
                                       generation_config={"temperature": 0})
            v = parse_verdict(r.text or "")
        except Exception as e:
            err += 1
            print(f"  [오류] {q.get('id')}: {str(e)[:80]}")
            time.sleep(2)
            continue
        if not v:
            err += 1
            continue
        q["tier"] = v["tier"]
        tm = q.get("tier_meta") or {}
        tm.update({"decided_by": f"gemini:{model_name}", "decided_at": now,
                   "reason": v["reason"],
                   "anchors": [a["id"] for a in anchors],
                   "anchor_level": level,
                   "anchor_fallback": level != "item"})
        q["tier_meta"] = tm
        tally[v["tier"]] += 1
        if i % CKPT_EVERY == 0:
            DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  …{i}/{len(targets)} {dict(tally)} 오류 {err}")

    DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"완료: {dict(tally)} · 오류 {err}")


if __name__ == "__main__":
    main()
