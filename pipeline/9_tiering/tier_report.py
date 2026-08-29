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


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    db = json.loads(DB.read_text(encoding="utf-8"))
    kichul = json.loads(KICHUL.read_text(encoding="utf-8"))
    gam = [q for q in kichul
           if str(q.get("subject", "")).startswith("경제") and q.get("exam") == "감정평가사"]

    # 진행률 표시
    judged = sum(1 for q in db if q.get("tier") and q.get("tier") != "discard")
    total_judged = len([q for q in db if q.get("tier")])
    undecided = sum(1 for q in db if not q.get("tier"))
    print(f"=== 진행률 ===")
    print(f"  LLM 판정 완료: {total_judged}/{len(db)}건 ({100*total_judged//len(db)}%)")
    print(f"  미판정: {undecided}건")

    print("\n=== 등급 분포 ===")
    for k, v in Counter(q.get("tier") or "미판정" for q in db).most_common():
        print(f"  {k}: {v}")

    # 판정자별 분리 집계
    print("\n=== 판정자별 분포 ===")
    decided_by_counts = Counter()
    decided_by_tiers = {}
    for q in db:
        if q.get("tier") and q.get("tier") not in ("discard",):
            decided_by = (q.get("tier_meta") or {}).get("decided_by")
            decided_by_counts[decided_by] += 1
            if decided_by not in decided_by_tiers:
                decided_by_tiers[decided_by] = Counter()
            decided_by_tiers[decided_by][q.get("tier")] += 1

    for decider, count in decided_by_counts.most_common():
        tiers = decided_by_tiers.get(decider, {})
        tier_str = " · ".join(f"{tier} {cnt}" for tier, cnt in sorted(tiers.items()))
        print(f"  {decider or '미기록'}: {count}건 | {tier_str}")

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
