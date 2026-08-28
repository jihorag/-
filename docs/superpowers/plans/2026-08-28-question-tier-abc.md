# 문항 등급 A/B/C Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 경제학 연습문제 12,120문항에 A(연습)/B(실전) 등급을 붙이고, 기출을 C로 두어 앱에서 세 탭으로 나눠 푼다.

**Architecture:** 파이프라인 스크립트 6개가 순서대로 `questions_db_econ.json`에 `tier` 필드를 채운다. 정량 게이트로 불량을 거르고, 선지 셔플로 정답 편향을 고치고, 감평 기출을 앵커로 붙인 Gemini가 A/B를 판정한다. 앱은 저장된 `tier`를 읽어 탭을 나눈다.

**Tech Stack:** Python 3.12 (stdlib + `google-generativeai`), React 19 / Vite (viewer)

**Spec:** `docs/superpowers/specs/2026-08-28-question-tier-abc-design.md`

## Global Constraints

- **`questions_db.json`은 절대 쓰지 않는다** (CLAUDE.md 원본 보존 규칙). 기출의 C 등급은 저장하지 않고 앱에서 파생한다
- 쓰기 대상은 `questions_db_econ.json` 하나뿐이다
- 모든 JSON 저장은 `json.dump(..., ensure_ascii=False, indent=2)`
- 판례 사건번호는 항상 `null` — 지어내지 않는다
- 폐기는 물리 삭제가 아니라 `tier: "discard"` 라벨이다
- 모든 스크립트는 재실행 안전(멱등)해야 한다. 이미 `tier`가 있는 문항은 건너뛴다
- 모든 스크립트는 DB 쓰기 전 `pipeline/9_tiering/backup/`에 백업한다
- 데이터 변경 후 반영은 `cd viewer && npm run sync-data`
- 새 스크립트는 `pipeline/9_tiering/`에 둔다
- 테스트는 각 스크립트의 `--self-test` 플래그에 `assert` 기반으로 넣는다 (이 저장소에 pytest가 없다)

---

### Task 1: 정량 품질 게이트

**Files:**
- Create: `pipeline/9_tiering/tier_gate.py`
- Modify: 없음

**Interfaces:**
- Consumes: `questions_db_econ.json`
- Produces: 탈락 문항에 `tier="discard"` + `tier_meta.reason`. 생존 문항은 `tier` 미설정(다음 단계 대상). 함수 `gate_reason(q, dup_seen, p90) -> str | None`

- [ ] **Step 1: 자기검증 테스트를 먼저 작성**

`pipeline/9_tiering/tier_gate.py` 안에 넣는다.

```python
def _self_test():
    long_q = {"question": "가" * 300, "explanation": "해" * 100, "options": [1, 2, 3, 4, 5]}
    assert gate_reason(long_q, set(), 252) == "장문"

    short_exp = {"question": "짧은 문제", "explanation": "짧음", "options": [1, 2, 3, 4, 5]}
    assert gate_reason(short_exp, set(), 252) == "해설부실"

    ok = {"question": "정상 문제", "explanation": "해" * 100, "options": [1, 2, 3, 4, 5]}
    assert gate_reason(ok, set(), 252) is None

    # 중복은 대표 1개를 살린다: 첫 등장은 통과, 두 번째부터 탈락
    seen = set()
    assert gate_reason(ok, seen, 252) is None
    seen.add(ok["question"].strip())
    assert gate_reason(ok, seen, 252) == "중복본문"

    four = {"question": "문제", "explanation": "해" * 100, "options": [1, 2, 3, 4]}
    assert gate_reason(four, set(), 252) == "선지수"
    print("tier_gate self-test 통과")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `.venv/bin/python pipeline/9_tiering/tier_gate.py --self-test`
Expected: FAIL — `NameError: name 'gate_reason' is not defined`

- [ ] **Step 3: 구현**

```python
#!/usr/bin/env python3
"""정량 품질 게이트 — 명백한 불량 문항에 tier="discard"를 붙인다.

임계는 기출 경제 문항 분포에서 뽑는다(본문 길이 P90).
중복 본문은 대표 1개를 살리고 나머지를 탈락시킨다.
멱등: 이미 tier가 있는 문항은 건드리지 않는다.

사용:
  python3 pipeline/9_tiering/tier_gate.py [--dry-run] [--self-test]
"""
import json
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
KICHUL = ROOT / "questions_db.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"
MIN_EXPLANATION = 80


def kichul_p90() -> int:
    """기출 경제 문항 본문 길이의 P90. 장문 임계로 쓴다."""
    qs = json.loads(KICHUL.read_text(encoding="utf-8"))
    lens = sorted(len(q.get("question", "")) for q in qs
                  if str(q.get("subject", "")).startswith("경제"))
    return lens[int(len(lens) * 0.90)]


def gate_reason(q, dup_seen, p90):
    """탈락 사유를 돌려준다. 통과면 None.

    dup_seen 은 이미 등장한 본문 집합이다. 호출자가 순회하며 채운다.
    """
    stem = (q.get("question") or "").strip()
    if stem in dup_seen:
        return "중복본문"
    if len(stem) > p90:
        return "장문"
    if len((q.get("explanation") or "").strip()) < MIN_EXPLANATION:
        return "해설부실"
    if len(q.get("options") or []) != 5:
        return "선지수"
    return None


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    dry = "--dry-run" in sys.argv
    p90 = kichul_p90()
    db = json.loads(DB.read_text(encoding="utf-8"))
    now = datetime.now().strftime("%Y-%m-%d")

    dup_seen = set()
    reasons = Counter()
    survived = 0
    for q in db:
        if q.get("tier"):          # 멱등 — 이미 판정된 문항은 건너뛴다
            continue
        r = gate_reason(q, dup_seen, p90)
        dup_seen.add((q.get("question") or "").strip())
        if r:
            reasons[r] += 1
            if not dry:
                q["tier"] = "discard"
                q["tier_meta"] = {"decided_by": "tier_gate", "decided_at": now,
                                  "reason": r, "repaired": False}
        else:
            survived += 1

    print(f"장문 임계(기출 P90): {p90}자")
    for k, v in reasons.most_common():
        print(f"  탈락 {k}: {v}")
    print(f"  생존: {survived} / {len(db)}")

    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_gate_{ts}.json")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장 완료 (백업 econ.pre_gate_{ts}.json)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 테스트 통과 + 실제 실행 확인**

Run: `.venv/bin/python pipeline/9_tiering/tier_gate.py --self-test`
Expected: `tier_gate self-test 통과`

Run: `.venv/bin/python pipeline/9_tiering/tier_gate.py --dry-run`
Expected: 장문 2,817 · 중복본문 1,229 · 해설부실 370 · 생존 7,704

숫자가 다르면 멈추고 보고한다. 스펙의 실측치와 어긋난다는 뜻이다.

- [ ] **Step 5: 실제 적용 후 커밋**

```bash
.venv/bin/python pipeline/9_tiering/tier_gate.py
git add pipeline/9_tiering/tier_gate.py questions_db_econ.json
git commit -m "feat(등급): 정량 품질 게이트 — 불량 4,416문항 discard 표시"
```

---

### Task 2: 선지 셔플 기계 교정

**Files:**
- Create: `pipeline/9_tiering/shuffle_options.py`

**Interfaces:**
- Consumes: Task 1 생존분(`tier` 미설정 문항)
- Produces: 셔플된 `options` / 재계산된 `answer` / 재정렬된 `option_meta`. 함수 `shuffle_q(q, rng) -> bool`

- [ ] **Step 1: 자기검증 테스트를 먼저 작성**

```python
def _self_test():
    import random
    for seed in range(50):
        q = {"id": "t", "options": ["가", "나", "다", "라", "마"], "answer": "2",
             "option_meta": [{"why": f"m{i}"} for i in range(5)]}
        before_correct = q["options"][1]
        before_meta = q["option_meta"][1]["why"]
        shuffle_q(q, random.Random(seed))
        # 정답 텍스트가 보존되고, answer 가 그 위치를 가리킨다
        assert q["options"][int(q["answer"]) - 1] == before_correct
        # option_meta 가 선지를 따라 같이 움직인다
        assert q["option_meta"][int(q["answer"]) - 1]["why"] == before_meta
        assert sorted(q["options"]) == sorted(["가", "나", "다", "라", "마"])

    # option_meta 가 없어도 죽지 않는다
    q2 = {"id": "t2", "options": ["a", "b", "c", "d", "e"], "answer": "5"}
    assert shuffle_q(q2, random.Random(0)) is True
    assert q2["options"][int(q2["answer"]) - 1] == "e"

    # 정답이 비정상이면 건드리지 않는다
    q3 = {"id": "t3", "options": ["a", "b", "c", "d", "e"], "answer": ""}
    assert shuffle_q(q3, random.Random(0)) is False
    print("shuffle_options self-test 통과")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `.venv/bin/python pipeline/9_tiering/shuffle_options.py --self-test`
Expected: FAIL — `NameError: name 'shuffle_q' is not defined`

- [ ] **Step 3: 구현**

```python
#!/usr/bin/env python3
"""선지 셔플 — 정답 순서 편향을 없앤다.

v1 자동생성 문항의 정답이 1번에 몰려 있다. 선지를 섞고 answer 와
option_meta 를 함께 재계산한다. 문항 내용은 바뀌지 않는다.

시드를 문항 id 로 고정해 재실행해도 같은 결과가 나온다(재현 가능).
멱등: tier_meta.shuffled 가 이미 True 면 건너뛴다.

사용:
  python3 pipeline/9_tiering/shuffle_options.py [--dry-run] [--self-test]
"""
import json
import random
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"


def shuffle_q(q, rng) -> bool:
    """선지를 섞고 answer·option_meta 를 맞춘다. 처리했으면 True."""
    opts = q.get("options") or []
    try:
        idx = int(str(q.get("answer")).strip()) - 1
    except (ValueError, TypeError):
        return False
    if not (0 <= idx < len(opts)):
        return False

    meta = q.get("option_meta")
    has_meta = isinstance(meta, list) and len(meta) == len(opts)
    order = list(range(len(opts)))
    rng.shuffle(order)

    q["options"] = [opts[i] for i in order]
    q["answer"] = str(order.index(idx) + 1)
    if has_meta:
        q["option_meta"] = [meta[i] for i in order]
    return True


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    dry = "--dry-run" in sys.argv
    db = json.loads(DB.read_text(encoding="utf-8"))
    done = skipped = 0
    for q in db:
        if q.get("tier"):                       # 이미 폐기된 문항은 대상 아님
            continue
        tm = q.get("tier_meta") or {}
        if tm.get("shuffled"):                  # 멱등
            continue
        rng = random.Random(q.get("id", ""))    # id 기반 고정 시드 — 재현 가능
        if dry:
            done += 1
            continue
        if shuffle_q(q, rng):
            tm["shuffled"] = True
            q["tier_meta"] = tm
            done += 1
        else:
            skipped += 1

    after = Counter(str(q.get("answer")) for q in db if not q.get("tier"))
    print(f"셔플 {done} · 건너뜀(정답 비정상) {skipped}")
    print(f"셔플 후 정답 분포: {sorted(after.items())}")

    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_shuffle_{ts}.json")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장 완료 (백업 econ.pre_shuffle_{ts}.json)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 테스트 통과 + 분포 확인**

Run: `.venv/bin/python pipeline/9_tiering/shuffle_options.py --self-test`
Expected: `shuffle_options self-test 통과`

Run: `.venv/bin/python pipeline/9_tiering/shuffle_options.py`
Expected: 셔플 후 정답 분포가 1~5번 각각 대략 20%씩. 어느 한 번호가 30%를 넘으면 멈추고 보고한다.

- [ ] **Step 5: 커밋**

```bash
git add pipeline/9_tiering/shuffle_options.py questions_db_econ.json
git commit -m "feat(등급): 선지 셔플로 정답 편향 제거"
```

---

### Task 3: 기출 앵커 인덱스

**Files:**
- Create: `pipeline/9_tiering/build_anchors.py`
- Create(산출): `pipeline/9_tiering/anchors_econ.json`

**Interfaces:**
- Consumes: `questions_db.json` (읽기만)
- Produces: `anchors_econ.json` — `{"관 이름": [문항...], "절 이름": [...], "장 이름": [...]}`. 함수 `pick_anchors(index, tax) -> (list, str)`

- [ ] **Step 1: 자기검증 테스트를 먼저 작성**

```python
def _self_test():
    index = {
        "item::제2관 단기 이윤극대화": [{"id": "a1"}, {"id": "a2"}, {"id": "a3"}],
        "section::제13절 완전경쟁시장": [{"id": "b1"}, {"id": "b2"}],
        "chapter::제5장 시장이론": [{"id": "c1"}],
    }
    # 관이 있으면 관을 쓴다
    got, lvl = pick_anchors(index, {"item": "제2관 단기 이윤극대화",
                                    "section": "제13절 완전경쟁시장",
                                    "chapter": "제5장 시장이론"})
    assert [q["id"] for q in got] == ["a1", "a2", "a3"] and lvl == "item"

    # 관이 없으면 절로 내려온다
    got, lvl = pick_anchors(index, {"item": "없는관",
                                    "section": "제13절 완전경쟁시장",
                                    "chapter": "제5장 시장이론"})
    assert [q["id"] for q in got] == ["b1", "b2"] and lvl == "section"

    # 절도 없으면 장
    got, lvl = pick_anchors(index, {"item": "없는관", "section": "없는절",
                                    "chapter": "제5장 시장이론"})
    assert lvl == "chapter"

    # 아무것도 없으면 빈 목록 + none
    got, lvl = pick_anchors(index, {"item": "x", "section": "y", "chapter": "z"})
    assert got == [] and lvl == "none"

    # 최대 3개만
    index["item::많은관"] = [{"id": str(i)} for i in range(10)]
    got, _ = pick_anchors(index, {"item": "많은관", "section": "", "chapter": ""})
    assert len(got) == 3
    print("build_anchors self-test 통과")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `.venv/bin/python pipeline/9_tiering/build_anchors.py --self-test`
Expected: FAIL — `NameError: name 'pick_anchors' is not defined`

- [ ] **Step 3: 구현**

```python
#!/usr/bin/env python3
"""기출 앵커 인덱스 — LLM 판정의 기준선이 될 감평 기출을 단원별로 모은다.

감평 기출이 관 기준 108/222 만 덮으므로 관 → 절 → 장 → 타시험 순으로
폴백한다. 어느 수준의 앵커를 썼는지 기록해 나중에 신뢰도를 구분한다.

questions_db.json 은 읽기만 한다(원본 보존 규칙).

사용:
  python3 pipeline/9_tiering/build_anchors.py [--self-test]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
KICHUL = ROOT / "questions_db.json"
OUT = Path(__file__).resolve().parent / "anchors_econ.json"
MAX_ANCHORS = 3
# 감평이 1순위. 없으면 난이도가 가장 가까운 노무사로 폴백한다.
PREFERRED_EXAMS = ["감정평가사", "공인노무사"]


def build_index(kichul):
    """관/절/장 3수준 인덱스를 만든다. 키는 'item::이름' 형태."""
    index = {}
    for q in kichul:
        if not str(q.get("subject", "")).startswith("경제"):
            continue
        if q.get("exam") not in PREFERRED_EXAMS:
            continue
        mt = (q.get("indexing_v4") or {}).get("mapped_taxonomy") or {}
        slim = {"id": q.get("id"), "exam": q.get("exam"), "year": q.get("year"),
                "question": q.get("question"), "options": q.get("options"),
                "answer": q.get("answer")}
        for level in ("item", "section", "chapter"):
            name = mt.get(level)
            if name:
                index.setdefault(f"{level}::{name}", []).append(slim)
    # 감평을 앞으로 정렬해 폴백 시에도 감평이 먼저 뽑히게 한다
    for v in index.values():
        v.sort(key=lambda q: PREFERRED_EXAMS.index(q["exam"]))
    return index


def pick_anchors(index, tax):
    """관 → 절 → 장 순으로 앵커를 고른다. (앵커목록, 사용수준)."""
    for level in ("item", "section", "chapter"):
        name = (tax or {}).get(level)
        if not name:
            continue
        hit = index.get(f"{level}::{name}")
        if hit:
            return hit[:MAX_ANCHORS], level
    return [], "none"


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return
    kichul = json.loads(KICHUL.read_text(encoding="utf-8"))
    index = build_index(kichul)
    OUT.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    levels = {"item": 0, "section": 0, "chapter": 0}
    for k in index:
        levels[k.split("::")[0]] += 1
    print(f"앵커 인덱스 저장: {OUT.name}")
    print(f"  관 {levels['item']} · 절 {levels['section']} · 장 {levels['chapter']}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 테스트 통과 + 커버리지 확인**

Run: `.venv/bin/python pipeline/9_tiering/build_anchors.py --self-test`
Expected: `build_anchors self-test 통과`

Run: `.venv/bin/python pipeline/9_tiering/build_anchors.py`
Expected: 관 108개 이상, 절 51개 이상이 잡힌다

- [ ] **Step 5: 커밋**

```bash
git add pipeline/9_tiering/build_anchors.py pipeline/9_tiering/anchors_econ.json
git commit -m "feat(등급): 기출 앵커 인덱스 — 관/절/장 폴백"
```

---

### Task 4: LLM 앵커 판정

**Files:**
- Create: `pipeline/9_tiering/tier_judge.py`

**Interfaces:**
- Consumes: Task 1·2 생존분, `anchors_econ.json`, `pick_anchors()` (Task 3에서 import)
- Produces: 각 문항에 `tier` = `"A"` | `"B"` | `"discard"` | `"repair"` + `tier_meta`. 함수 `build_prompt(q, anchors) -> str`, `parse_verdict(text) -> dict | None`

- [ ] **Step 1: 자기검증 테스트를 먼저 작성**

```python
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
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `.venv/bin/python pipeline/9_tiering/tier_judge.py --self-test`
Expected: FAIL — `NameError: name 'parse_verdict' is not defined`

- [ ] **Step 3: 구현**

```python
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
- "B" = 2개 이상 개념 결합 또는 2단계 이상 계산, 오답이 흔한 오개념을 찌름

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
```

- [ ] **Step 4: 자기검증 통과 후 소표본으로 일관성 확인**

Run: `.venv/bin/python pipeline/9_tiering/tier_judge.py --self-test`
Expected: `tier_judge self-test 통과`

Run: `.venv/bin/pip install google-generativeai`
Run: `set -a && . .env && set +a && .venv/bin/python pipeline/9_tiering/tier_judge.py --limit 20`
Expected: 20문항 판정 완료, 오류 2건 이하

판정 결과를 사람이 읽을 수 있게 뽑는다.

```bash
.venv/bin/python -c "
import json
db=json.load(open('questions_db_econ.json',encoding='utf-8'))
for q in [x for x in db if x.get('tier') in ('A','B','discard','repair')][:20]:
    tm=q['tier_meta']
    print(f\"[{q['tier']}] {q['question'][:60]}\")
    print(f\"    근거: {tm['reason']} | 앵커수준: {tm.get('anchor_level')}\")
"
```

**여기서 멈추고 사람에게 이 20건을 보여준다.** 판정이 납득되지 않으면 RUBRIC을 고치고 다시 20건을 돌린다. 전량 실행은 사람 승인 후에 한다.

- [ ] **Step 5: 승인 후 전량 실행 + 커밋**

```bash
set -a && . .env && set +a && .venv/bin/python pipeline/9_tiering/tier_judge.py
git add pipeline/9_tiering/tier_judge.py questions_db_econ.json
git commit -m "feat(등급): 기출 앵커 LLM 판정으로 A/B 등급 부여"
```

---

### Task 5: 선별 교정 + 재심사

**Files:**
- Create: `pipeline/9_tiering/tier_repair.py`

**Interfaces:**
- Consumes: Task 4가 `tier="repair"`로 표시한 문항, `build_prompt`·`parse_verdict` (Task 4에서 import)
- Produces: 교정된 `question`/`explanation` + 재심사 결과 `tier`. 원본은 `tier_meta.orig_question`·`orig_explanation`에 보존. 함수 `parse_repair(text) -> dict | None`

- [ ] **Step 1: 자기검증 테스트를 먼저 작성**

```python
def _self_test():
    v = parse_repair('{"question":"짧게 고친 본문","explanation":"보강한 해설"}')
    assert v["question"] == "짧게 고친 본문" and v["explanation"] == "보강한 해설"

    # 둘 중 하나만 와도 받는다(해설만 보강한 경우)
    v = parse_repair('{"explanation":"보강만"}')
    assert v == {"explanation": "보강만"}

    # 선지·정답을 바꾸려 들면 거부한다 — 교정은 본문/해설만 손댄다
    assert parse_repair('{"question":"x","options":["a"],"answer":"1"}') is None

    # 빈 응답
    assert parse_repair("{}") is None
    assert parse_repair("어쩌고") is None
    print("tier_repair self-test 통과")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `.venv/bin/python pipeline/9_tiering/tier_repair.py --self-test`
Expected: FAIL — `NameError: name 'parse_repair' is not defined`

- [ ] **Step 3: 구현**

```python
#!/usr/bin/env python3
"""선별 교정 — repair 로 분류된 문항만 본문 압축·해설 보강 후 재심사.

교정은 본문과 해설만 손댄다. 선지와 정답은 절대 바꾸지 않는다(바꾸면
문항이 다른 문항이 되고 검증된 계산이 무너진다).

교정본은 Task 4 와 같은 기준으로 재심사해야 A/B 에 편입된다.
통과 못하면 discard 다.

사용:
  python3 pipeline/9_tiering/tier_repair.py [--limit 20] [--self-test]
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
from build_anchors import pick_anchors                  # noqa: E402
from tier_judge import build_prompt, parse_verdict      # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
ANCHORS = Path(__file__).resolve().parent / "anchors_econ.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"
CKPT_EVERY = 25

REPAIR_PROMPT = """너는 한국 감정평가사 1차 경제학원론 출제위원이다.
아래 문항은 내용은 쓸 만한데 형식이 나쁘다. 다음만 고쳐라.

- 본문이 장황하면 군더더기를 덜어 250자 안으로 줄인다. 조건·수치는 하나도 빼지 않는다.
- 해설이 부실하면 왜 정답인지와 왜 오답인지를 모두 담아 보강한다.

절대 금지: 선지 변경, 정답 변경, 조건이나 수치 변경, 없는 내용 추가.

출력은 이 JSON 하나만. 고치지 않은 항목은 넣지 않는다.
{"question": "...", "explanation": "..."}"""


def parse_repair(text):
    """교정 응답을 꺼낸다. 선지·정답을 건드리려 들면 거부한다."""
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        v = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(v, dict):
        return None
    if {"options", "answer", "option_meta"} & set(v):
        return None          # 손대면 안 되는 곳을 건드렸다
    out = {k: v[k] for k in ("question", "explanation")
           if str(v.get(k) or "").strip()}
    return out or None


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("환경변수 GEMINI_API_KEY 미설정.")
        sys.exit(1)
    import google.generativeai as genai
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    db = json.loads(DB.read_text(encoding="utf-8"))
    index = json.loads(ANCHORS.read_text(encoding="utf-8"))
    targets = [q for q in db if q.get("tier") == "repair"]
    if limit:
        targets = targets[:limit]
    print(f"교정 대상 {len(targets)}문항")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_repair_{ts}.json")

    now = datetime.now().strftime("%Y-%m-%d")
    tally = Counter()
    for i, q in enumerate(targets, 1):
        prompt = REPAIR_PROMPT + "\n\n[문항]\n" + json.dumps(
            {"question": q.get("question"), "options": q.get("options"),
             "answer": q.get("answer"), "explanation": q.get("explanation")},
            ensure_ascii=False)
        try:
            r = model.generate_content(prompt, generation_config={"temperature": 0})
            fix = parse_repair(r.text or "")
        except Exception as e:
            print(f"  [오류] {q.get('id')}: {str(e)[:80]}")
            time.sleep(2)
            continue
        if not fix:
            q["tier"] = "discard"
            q["tier_meta"]["reason"] = "교정 실패"
            tally["discard"] += 1
            continue

        tm = q["tier_meta"]
        tm["orig_question"] = q.get("question")
        tm["orig_explanation"] = q.get("explanation")
        q.update(fix)

        # 재심사 — 교정본도 같은 기준을 통과해야 한다
        mt = (q.get("indexing_v4") or {}).get("mapped_taxonomy") or {}
        anchors, level = pick_anchors(index, mt)
        try:
            r2 = model.generate_content(build_prompt(q, anchors),
                                        generation_config={"temperature": 0})
            v = parse_verdict(r2.text or "")
        except Exception as e:
            print(f"  [재심사 오류] {q.get('id')}: {str(e)[:80]}")
            continue
        new_tier = v["tier"] if v and v["tier"] in ("A", "B") else "discard"
        q["tier"] = new_tier
        tm.update({"repaired": True, "rejudged_at": now,
                   "reason": (v or {}).get("reason", "재심사 탈락")})
        tally[new_tier] += 1
        if i % CKPT_EVERY == 0:
            DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  …{i}/{len(targets)} {dict(tally)}")

    DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"완료: {dict(tally)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 테스트 통과 + 소표본 실행**

Run: `.venv/bin/python pipeline/9_tiering/tier_repair.py --self-test`
Expected: `tier_repair self-test 통과`

Run: `set -a && . .env && set +a && .venv/bin/python pipeline/9_tiering/tier_repair.py --limit 20`
Expected: 20문항 처리, 교정 후 본문이 250자 이내인지 눈으로 확인

- [ ] **Step 5: 전량 실행 + 커밋**

```bash
set -a && . .env && set +a && .venv/bin/python pipeline/9_tiering/tier_repair.py
git add pipeline/9_tiering/tier_repair.py questions_db_econ.json
git commit -m "feat(등급): repair 문항 선별 교정 후 재심사"
```

---

### Task 6: 사후 검증 리포트

**Files:**
- Create: `pipeline/9_tiering/tier_report.py`

**Interfaces:**
- Consumes: 등급이 매겨진 `questions_db_econ.json`, `questions_db.json`
- Produces: 콘솔 리포트. 함수 `profile(qs) -> dict`

- [ ] **Step 1: 자기검증 테스트를 먼저 작성**

```python
def _self_test():
    qs = [
        {"question": "Q=100-2P 를 구하시오", "options": ["가나다", "라마바", "사아자", "차카타", "파하가"]},
        {"question": "정의를 고르시오", "options": ["가나다", "라마바", "사아자", "차카타", "파하가"]},
    ]
    p = profile(qs)
    assert p["n"] == 2
    assert p["수식률"] == 50          # 두 문항 중 하나만 수식
    assert p["선지평균"] == 3.0        # 모든 선지가 3자
    assert p["본문중앙"] > 0

    assert profile([]) is None        # 빈 집단은 None
    print("tier_report self-test 통과")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `.venv/bin/python pipeline/9_tiering/tier_report.py --self-test`
Expected: FAIL — `NameError: name 'profile' is not defined`

- [ ] **Step 3: 구현**

```python
#!/usr/bin/env python3
"""사후 검증 — A/B 집단이 기출 프로파일과 닮았는지 확인한다.

B 가 감평 기출(수식 65%, 선지 17.4자)에서 크게 벗어나면 판정 기준이
잘못된 것이므로 RUBRIC 을 고치고 다시 돌려야 한다.

사용:
  python3 pipeline/9_tiering/tier_report.py [--self-test]
"""
import json
import re
import statistics as st
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
KICHUL = ROOT / "questions_db.json"
MATH = re.compile(r"[=+\-*/^]|\$|\\frac|함수|곡선")


def profile(qs):
    """집단의 난이도 프로파일. 빈 집단이면 None."""
    if not qs:
        return None
    lens = [len(q.get("question", "")) for q in qs]
    optlen = [st.mean([len(str(o)) for o in (q.get("options") or [""])]) for q in qs]
    return {
        "n": len(qs),
        "본문중앙": int(st.median(lens)),
        "선지평균": round(st.mean(optlen), 1),
        "수식률": round(100 * sum(bool(MATH.search(q.get("question", ""))) for q in qs) / len(qs)),
    }


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    db = json.loads(DB.read_text(encoding="utf-8"))
    kichul = json.loads(KICHUL.read_text(encoding="utf-8"))
    gam = [q for q in kichul
           if str(q.get("subject", "")).startswith("경제") and q.get("exam") == "감정평가사"]

    print("=== 등급 분포 ===")
    for k, v in Counter(q.get("tier") or "미판정" for q in db).most_common():
        print(f"  {k}: {v}")

    print("\n=== 프로파일 대조 (기준: 감평 기출) ===")
    rows = [("감평 기출", profile(gam))]
    for t in ("A", "B"):
        rows.append((f"{t} 등급", profile([q for q in db if q.get("tier") == t])))
    print(f"{'집단':<10}{'n':>7}{'본문중앙':>9}{'선지평균':>9}{'수식률':>8}")
    for name, p in rows:
        if not p:
            print(f"{name:<10}{'(없음)':>7}")
            continue
        print(f"{name:<10}{p['n']:>7}{p['본문중앙']:>9}{p['선지평균']:>9}{p['수식률']:>8}")

    b = profile([q for q in db if q.get("tier") == "B"])
    if b and abs(b["수식률"] - 65) > 20:
        print("\n⚠️ B 집단 수식률이 감평 기출(65%)에서 20%p 넘게 벗어났다. 판정 기준 재검토 필요.")

    print("\n=== 앵커 신뢰도 ===")
    lv = Counter((q.get("tier_meta") or {}).get("anchor_level")
                 for q in db if q.get("tier") in ("A", "B"))
    for k, v in lv.most_common():
        print(f"  {k or '미기록'}: {v}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 테스트 통과 + 리포트 확인**

Run: `.venv/bin/python pipeline/9_tiering/tier_report.py --self-test`
Expected: `tier_report self-test 통과`

Run: `.venv/bin/python pipeline/9_tiering/tier_report.py`
Expected: 등급 분포와 프로파일 대조표 출력. ⚠️ 경고가 뜨면 멈추고 보고한다.

- [ ] **Step 5: B 등급 20문항을 사람이 검수한다 (스펙 §11 3단계)**

프로파일이 닮았다고 실제 난이도가 맞다는 보장은 없다. B에서 무작위 20문항을
뽑아 사람이 직접 읽는다.

```bash
.venv/bin/python -c "
import json, random
db=json.load(open('questions_db_econ.json',encoding='utf-8'))
b=[q for q in db if q.get('tier')=='B']
for q in random.Random(42).sample(b, min(20,len(b))):
    print(f\"--- {q['id']}\")
    print(q['question'][:200])
    print(f\"정답 {q['answer']} | 근거: {q['tier_meta']['reason']}\")
"
```

**여기서 멈추고 사람 확인을 받는다.** 20건 중 기출 수준에 못 미치는 것이
5건을 넘으면 Task 4의 RUBRIC을 고치고 판정을 다시 돌린다.

- [ ] **Step 6: 커밋**

```bash
git add pipeline/9_tiering/tier_report.py
git commit -m "feat(등급): 사후 프로파일 검증 리포트"
```

---

### Task 7: hq 관 매핑 보정 + 데이터 오류 수정

**Files:**
- Create: `pipeline/9_tiering/fix_hq_taxonomy.py`

**Interfaces:**
- Consumes: `questions_db_econ.json`, `taxonomy_v4.json`
- Produces: hq 문항의 `mapped_taxonomy.item` 채움, 중복 ID 재부여, `difficulty` 이상치 교정. 함수 `pick_item(sections, section_name, question) -> str`

**Why:** hq 수제 문항 2,240개는 `item`이 빈 문자열이라 `App.jsx:3025`의 관 카드 필터(`taxItemName === it.name`)에 걸리지 않는다. 등급을 붙여도 관 단위 학습에서 B 탭이 빈다.

- [ ] **Step 1: 자기검증 테스트를 먼저 작성**

```python
def _self_test():
    sections = {"제13절 완전경쟁시장": ["제1관 완전경쟁의 조건", "제2관 단기 이윤극대화"]}

    # 관 이름의 키워드가 본문에 있으면 그 관으로 간다
    assert pick_item(sections, "제13절 완전경쟁시장",
                     "단기 이윤극대화 생산량은?") == "제2관 단기 이윤극대화"

    # 아무 관에도 안 걸리면 첫 관으로 보낸다(빈 문자열보다 낫다)
    assert pick_item(sections, "제13절 완전경쟁시장",
                     "전혀 관계없는 본문") == "제1관 완전경쟁의 조건"

    # 모르는 절이면 빈 문자열
    assert pick_item(sections, "없는절", "본문") == ""

    # 관이 없는 절이면 빈 문자열
    assert pick_item({"제1절 빈절": []}, "제1절 빈절", "본문") == ""
    print("fix_hq_taxonomy self-test 통과")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `.venv/bin/python pipeline/9_tiering/fix_hq_taxonomy.py --self-test`
Expected: FAIL — `NameError: name 'pick_item' is not defined`

- [ ] **Step 3: 구현**

```python
#!/usr/bin/env python3
"""hq 문항의 관(item) 매핑 보정 + 데이터 오류 수정.

hq 수제 문항 2,240개는 item 이 빈 문자열이라 앱의 관 카드에 안 잡힌다.
관 제목의 키워드를 본문과 맞춰 배정하고, 안 걸리면 그 절의 첫 관으로 보낸다.
빈 문자열로 두면 아예 안 보이므로 첫 관이라도 배정하는 쪽이 낫다.

함께 고치는 것: 중복 ID 5건, difficulty 이상치 1건.

사용:
  python3 pipeline/9_tiering/fix_hq_taxonomy.py [--dry-run] [--self-test]
"""
import json
import re
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
TAX = ROOT / "taxonomy_v4.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"
STOP = re.compile(r"^제\d+관\s*")


def pick_item(sections, section_name, question):
    """절 안의 관 중 본문과 키워드가 겹치는 것을 고른다."""
    items = sections.get(section_name) or []
    if not items:
        return ""
    body = question or ""
    best, best_hit = "", 0
    for it in items:
        title = STOP.sub("", it)
        words = [w for w in re.split(r"[\s·,]+", title) if len(w) >= 2]
        hit = sum(1 for w in words if w in body)
        if hit > best_hit:
            best, best_hit = it, hit
    return best or items[0]


def build_sections(tax):
    """taxonomy_v4 에서 {절 이름: [관 이름...]} 을 만든다.

    과목에 세부과목이 있으면 subjects 아래, 없으면 chapters 아래에 장이 있다.
    경제학은 전자지만 둘 다 받아 둔다.
    """
    out = {}
    econ = tax.get("경제학원론") or {}
    groups = list((econ.get("subjects") or {}).values()) + [econ.get("chapters") or []]
    for chapters in groups:
        for ch in chapters or []:
            for sec in ch.get("sections") or []:
                out[sec["name"]] = [it["name"] for it in (sec.get("items") or [])]
    return out


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    dry = "--dry-run" in sys.argv
    db = json.loads(DB.read_text(encoding="utf-8"))
    sections = build_sections(json.loads(TAX.read_text(encoding="utf-8")))

    filled = 0
    for q in db:
        mt = (q.get("indexing_v4") or {}).get("mapped_taxonomy")
        if not mt or mt.get("item"):
            continue
        item = pick_item(sections, mt.get("section"), q.get("question"))
        if item:
            if not dry:
                mt["item"] = item
            filled += 1

    # 중복 ID 재부여 — 뒤에 나온 것에 접미사를 붙인다
    seen, fixed_ids = set(), 0
    for q in db:
        qid = q.get("id")
        if qid in seen:
            n = 2
            while f"{qid}-dup{n}" in seen:
                n += 1
            if not dry:
                q["id"] = f"{qid}-dup{n}"
            seen.add(f"{qid}-dup{n}")
            fixed_ids += 1
        else:
            seen.add(qid)

    # difficulty 이상치 — 1~5 밖이면 3으로 되돌린다
    fixed_diff = 0
    for q in db:
        iv = q.get("indexing_v4") or {}
        d = iv.get("difficulty")
        if isinstance(d, int) and not (1 <= d <= 5):
            if not dry:
                iv["difficulty"] = 3
                mt = iv.get("mapped_taxonomy")
                if mt:
                    mt["difficulty"] = 3
            fixed_diff += 1

    print(f"item 채움 {filled} · 중복 ID 수정 {fixed_ids} · difficulty 교정 {fixed_diff}")
    left = sum(1 for q in db
               if not (((q.get("indexing_v4") or {}).get("mapped_taxonomy") or {}).get("item")))
    print(f"여전히 item 빈 문항: {left}")

    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_taxfix_{ts}.json")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장 완료 (백업 econ.pre_taxfix_{ts}.json)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 테스트 통과 + 실행 확인**

Run: `.venv/bin/python pipeline/9_tiering/fix_hq_taxonomy.py --self-test`
Expected: `fix_hq_taxonomy self-test 통과`

Run: `.venv/bin/python pipeline/9_tiering/fix_hq_taxonomy.py --dry-run`
Expected: item 채움 2,240 내외 · 중복 ID 수정 5 · difficulty 교정 1

`build_sections`가 빈 dict를 돌려주면 `taxonomy_v4.json`의 구조가 예상과 다른 것이다. 멈추고 실제 구조를 확인한 뒤 `build_sections`를 고친다.

- [ ] **Step 5: 적용 + 커밋**

```bash
.venv/bin/python pipeline/9_tiering/fix_hq_taxonomy.py
git add pipeline/9_tiering/fix_hq_taxonomy.py questions_db_econ.json
git commit -m "fix(경제): hq 문항 관 매핑 보정 + 중복 ID·난이도 이상치 수정"
```

---

### Task 8: 앱 A/B/C 탭 연결

**Files:**
- Modify: `viewer/src/App.jsx:2704-2710` (런타임 lowq 계산)
- Modify: `viewer/src/App.jsx:2728` (반환 객체에 tier 추가)
- Modify: `viewer/src/App.jsx:2763-2780` (baseFilter)
- Modify: `viewer/src/App.jsx:2539` (sourceFilter 초기값)
- Modify: `viewer/src/App.jsx:4941-4950` (토글 UI)

**Interfaces:**
- Consumes: 문항의 `tier` 필드 (Task 4·5가 채움)
- Produces: 없음(최종 소비자)

- [ ] **Step 1: 현재 동작을 기록해 두고 시작**

Run: `cd viewer && npx vite build 2>&1 | tail -3`
Expected: `✓ built in ...` — 변경 전 빌드가 통과함을 확인한다

- [ ] **Step 2: `lowq` 를 저장된 tier 기반으로 바꾼다**

`App.jsx:2704`의 블록을 아래로 교체한다. `tier`가 없는 문항(다른 과목·미판정)은 기존 휴리스틱으로 폴백해, 데이터와 코드를 따로 배포할 수 있게 한다.

```jsx
      // 🏅 등급 — 저장된 tier 가 있으면 그걸 쓰고, 없으면 기존 휴리스틱으로 폴백한다.
      //    (경제학만 tier 가 채워져 있고 나머지 과목은 아직 없다)
      const isAigen = q.exam === '[AI생성]' || (q.id && String(q.id).startsWith('aigen-'));
      const isPracticeQ = !isAigen && (q.source === 'practice' || q.exam === '[연습문제]' || (q.id && String(q.id).startsWith('practice-')));
      let tier = q.tier || null;
      let lowq = false;
      if (tier) {
        lowq = tier === 'discard';
      } else if (isPracticeQ) {
        const stem = (q.question || '').slice(0, 60);
        const first = !seenStem.has(stem); seenStem.add(stem);
        const hasMeta = Array.isArray(q.option_meta) && q.option_meta.length > 0;
        lowq = !(hasMeta && first);
        tier = lowq ? 'discard' : 'A';   // 미판정 연습문제는 일단 A로 둔다
      } else {
        tier = 'C';                       // 기출은 저장하지 않고 여기서 파생한다
      }
```

- [ ] **Step 3: 반환 객체·필터·UI 를 잇는다**

`App.jsx:2728`의 `lowq,` 아래에 한 줄 추가한다.

```jsx
        lowq,
        tier,
```

`App.jsx:2539`의 상태 이름을 바꾼다.

```jsx
  const [tierFilter, setTierFilter] = useState('all');
```

`App.jsx:2763` `baseFilter` 안에서 기존 `sourceFilter` 두 줄을 아래로 교체한다.

```jsx
    // 등급 탭 — A 연습 / B 실전 / C 기출
    if (tierFilter !== 'all' && item.tier !== tierFilter) return false;
```

같은 함수의 의존성 배열을 바꾼다.

```jsx
  }, [taxScope, browseExam, tierFilter]);
```

`App.jsx:4941`의 토글 배열을 바꾼다.

```jsx
            {[['all', '전체'], ['A', 'A 연습'], ['B', 'B 실전'], ['C', 'C 기출']].map(([k, lab]) => (
              <button key={k} onClick={() => setTierFilter(k)}
                style={{ padding: '5px 12px', borderRadius: 7, border: 'none', cursor: 'pointer',
                  background: tierFilter === k ? 'var(--primary)' : 'transparent',
                  color: tierFilter === k ? '#fff' : 'var(--primary-dark)', fontWeight: 700, fontSize: '0.78rem' }}>
                {lab}
              </button>
            ))}
```

- [ ] **Step 4: 남은 `sourceFilter` 참조를 없애고 빌드한다**

Run: `cd viewer && grep -n "sourceFilter" src/App.jsx`
Expected: 결과 없음. 남아 있으면 모두 `tierFilter`로 바꾼다.

Run: `cd viewer && npx vite build 2>&1 | tail -3`
Expected: `✓ built in ...`

Run: `cd viewer && npm run sync-data`
Expected: 동기화 완료. `tier` 필드가 `public/data/exams/*.json`에 실린다

Run: `cd viewer && node -e "const d=require('./public/data/exams/01.json');const q=(d.questions||d);console.log(Object.entries(q.filter(x=>x.subject==='경제학원론').reduce((a,x)=>{a[x.tier||'없음']=(a[x.tier||'없음']||0)+1;return a},{})))"`
Expected: A·B·discard 가 섞여 나온다. 전부 `없음`이면 sync 가 tier 를 안 실은 것이다

- [ ] **Step 5: 커밋**

```bash
git add viewer/src/App.jsx viewer/public/data
git commit -m "feat(앱): 문제풀이 탭을 A 연습/B 실전/C 기출 3등급으로 분리"
```

---

## 실행 순서

Task 1 → 2 → 3 → 4 → 5 → 6 순으로 의존한다. Task 7은 독립이므로 언제 해도 되지만 Task 8 앞에 끝내야 한다. Task 8이 마지막이다.

Task 4 Step 4에서 **반드시 멈추고 사람 확인을 받는다.** 30문항 판정을 눈으로 보지 않고 7,704문항에 돈을 쓰면 안 된다.

## 되돌리기

- 각 스크립트가 `pipeline/9_tiering/backup/`에 실행 전 백업을 남긴다
- 등급만 지우려면: `python3 -c "import json;p='questions_db_econ.json';d=json.load(open(p));[q.pop('tier',None) or q.pop('tier_meta',None) for q in d];json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)"`
- 앱은 `tier`가 없으면 기존 휴리스틱으로 폴백하므로 데이터만 되돌려도 깨지지 않는다
