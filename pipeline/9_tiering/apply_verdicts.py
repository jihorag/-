#!/usr/bin/env python3
"""에이전트가 직접 읽고 내린 판정을 DB에 반영한다.

외부 LLM API 를 쓰지 않는다. 판정 주체는 대화 중인 에이전트이고,
이 스크립트는 그 결과를 옮겨 적기만 한다.

입력 JSON 형식:
  [{"id": "...", "tier": "A|B|discard", "reason": "..."}, ...]

사용:
  python3 pipeline/9_tiering/apply_verdicts.py verdicts.json [--dry-run]
  python3 pipeline/9_tiering/apply_verdicts.py --self-test
"""
import json
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tier_judge import _atomic_write_json          # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"
DECIDER = "claude-opus-5(직접판정)"
VALID = {"A", "B", "discard"}
REDECIDABLE = "repair"          # 이 등급만 새 판정으로 덮어쓴다


def validate(verdicts):
    """형식을 검사하고 문제를 목록으로 돌려준다."""
    problems = []
    seen = set()
    for i, v in enumerate(verdicts):
        if not isinstance(v, dict):
            problems.append(f"[{i}] dict 아님"); continue
        if not v.get("id"):
            problems.append(f"[{i}] id 없음")
        if v.get("tier") not in VALID:
            problems.append(f"[{i}] tier 값 이상: {v.get('tier')!r}")
        if not str(v.get("reason") or "").strip():
            problems.append(f"[{i}] reason 없음")
        if v.get("id") in seen:
            problems.append(f"[{i}] id 중복: {v['id']}")
        seen.add(v.get("id"))
    return problems


def _self_test():
    assert validate([{"id": "a", "tier": "B", "reason": "근거"}]) == []
    assert validate([{"id": "a", "tier": "C", "reason": "근거"}])      # C 는 허용 안 함
    assert validate([{"id": "a", "tier": "B", "reason": ""}])          # 근거 필수
    assert validate([{"id": "a", "tier": "B", "reason": "x"},
                     {"id": "a", "tier": "A", "reason": "y"}])         # 중복 id
    assert validate([{"tier": "B", "reason": "x"}])                    # id 필수

    # repair 만 덮어쓸 수 있고 확정 등급은 보호된다
    assert REDECIDABLE == "repair"
    assert REDECIDABLE not in VALID       # repair 를 새 판정값으로 줄 수는 없다
    print("apply_verdicts self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("판정 JSON 파일 경로가 필요하다."); sys.exit(2)
    dry = "--dry-run" in sys.argv

    verdicts = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    problems = validate(verdicts)
    if problems:
        print("입력 형식 오류:"); [print("  ", p) for p in problems]; sys.exit(1)

    db = json.loads(DB.read_text(encoding="utf-8"))
    byid = {q["id"]: q for q in db}
    now = datetime.now().strftime("%Y-%m-%d")
    tally = Counter()
    missing = []
    for v in verdicts:
        q = byid.get(v["id"])
        if not q:
            missing.append(v["id"]); continue
        # repair 는 "재판정이 필요하다"는 표시이므로 덮어쓴다.
        # 그 외 확정 등급(A/B/C/discard)은 실수로 뒤집지 않도록 건너뛴다.
        if q.get("tier") and q.get("tier") != REDECIDABLE:
            tally["이미 판정됨(건너뜀)"] += 1; continue
        tally[v["tier"]] += 1
        if dry:
            continue
        tm = q.get("tier_meta") or {}
        if q.get("tier") == REDECIDABLE:      # 되돌릴 수 있게 이전 상태를 남긴다
            tm["prev_tier"] = q.get("tier")
            tm["prev_reason"] = tm.get("reason")
        tm.update({"decided_by": DECIDER, "decided_at": now, "reason": v["reason"]})
        q["tier_meta"] = tm
        q["tier"] = v["tier"]

    for k, n in tally.most_common():
        print(f"  {k}: {n}")
    if missing:
        print(f"  DB 에 없는 id: {len(missing)} — {missing[:3]}")
    if dry:
        print("dry-run — 저장하지 않음"); return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_verdicts_{ts}.json")
    _atomic_write_json(DB, db)
    print(f"저장 완료 (백업 econ.pre_verdicts_{ts}.json)")


if __name__ == "__main__":
    main()
