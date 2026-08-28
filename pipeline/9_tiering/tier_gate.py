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
