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


MACHINE_DECIDERS = {"tier_gate", "gate_v2"}


def _is_llm_seen(tm):
    """LLM이 실제로 본 문항인지. gate_v2 가 나중에 덮어써도 prev_decided_by 에
    LLM 판정자가 남아 있으면 LLM이 본 것으로 센다."""
    db = tm.get("decided_by")
    prev = tm.get("prev_decided_by")
    return (bool(db) and db not in MACHINE_DECIDERS) or \
           (bool(prev) and prev not in MACHINE_DECIDERS)


def _calculate_progress(db):
    """진행률 계산 (기계 판정자 tier_gate/gate_v2 는 LLM으로 세지 않는다).
    반환: (llm_판정_count, tier_gate_판정_count, 미판정_count, 전체_count)"""
    llm_count = sum(1 for q in db if _is_llm_seen(q.get("tier_meta") or {}))
    tier_gate_count = sum(1 for q in db if q.get("tier_meta", {}).get("decided_by") == "tier_gate")
    undecided_count = sum(1 for q in db if not q.get("tier"))
    total_count = len(db)
    return llm_count, tier_gate_count, undecided_count, total_count


def _self_test():
    # 프로파일 테스트
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

    # 진행률 계산 테스트 (tier_gate를 LLM 판정과 분리)
    # 실제 데이터: tier_gate는 tier_meta.decided_by="tier_gate"로 기록됨
    test_db = [
        {"tier": "A", "tier_meta": {"decided_by": "gemini"}},             # LLM 판정
        {"tier": "discard", "tier_meta": {"decided_by": "gemini"}},       # LLM discard
        {"tier": "discard", "tier_meta": {"decided_by": "tier_gate"}},    # tier_gate discard
        {"tier": "B"},                                                     # decided_by 없는 B (미기록)
        {},                                                                # 미판정
    ]
    llm, tg, un, tot = _calculate_progress(test_db)
    assert llm == 2, f"LLM 판정 수 틀림: {llm} != 2 (gemini만)"
    assert tg == 1, f"tier_gate 판정 수 틀림: {tg} != 1"
    assert un == 1, f"미판정 수 틀림: {un} != 1"
    assert tot == 5, f"전체 수 틀림: {tot} != 5"

    # gate_v2 는 기계 판정자다 — 통째 덮어써 근거를 잃은 것과 병합돼 prev_decided_by가
    # 남은 것 둘 다 LLM으로 잘못 세면 안 되거나(전자), LLM으로 세야 한다(후자)
    gate_v2_only = [{"tier": "discard", "tier_meta": {"decided_by": "gate_v2"}}]
    assert _calculate_progress(gate_v2_only)[0] == 0, "gate_v2 단독은 LLM이 아니다"
    gate_v2_after_llm = [{"tier": "discard",
                          "tier_meta": {"decided_by": "gate_v2", "prev_decided_by": "gemini:x"}}]
    assert _calculate_progress(gate_v2_after_llm)[0] == 1, \
        "gate_v2가 덮어썼어도 prev_decided_by에 LLM이 남아 있으면 LLM 판정으로 센다"

    # 판정자별 감사표에서 미기록 항목이 보이는지 확인
    # (decided_by가 없는 행이 "미기록"으로 집계되어야 함)
    decider_table = {}
    for q in test_db:
        tier = q.get("tier")
        if not tier:
            continue
        if tier == "discard" and not q.get("tier_meta", {}).get("decided_by"):
            decided_by = "tier_gate"
        else:
            decided_by = (q.get("tier_meta") or {}).get("decided_by") or "미기록"
        decider_table[decided_by] = decider_table.get(decided_by, 0) + 1

    assert "미기록" in decider_table, "미기록 항목이 감사표에서 사라짐"
    assert decider_table["미기록"] == 1, f"미기록 수 틀림: {decider_table.get('미기록')} != 1"

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
    llm_count, tier_gate_count, undecided, total = _calculate_progress(db)
    print("=== 진행률 ===")
    print(f"  LLM 판정 완료: {llm_count}/{total}건 ({100*llm_count//total}%)")
    print(f"  tier_gate 판정: {tier_gate_count}건")
    print(f"  미판정: {undecided}건")

    print("\n=== 등급 분포 ===")
    for k, v in Counter(q.get("tier") or "미판정" for q in db).most_common():
        print(f"  {k}: {v}")

    # 판정자별 분리 집계 (discard 포함, 미기록 감시)
    print("\n=== 판정자별 분포 ===")
    decided_by_counts = Counter()
    decided_by_tiers = {}
    for q in db:
        tier = q.get("tier")
        if not tier:  # 미판정은 집계 안 함
            continue

        # tier_gate 판정: tier가 discard이고 tier_meta/decided_by 없음
        if tier == "discard" and not q.get("tier_meta", {}).get("decided_by"):
            decided_by = "tier_gate"
        else:
            decided_by = (q.get("tier_meta") or {}).get("decided_by") or "미기록"

        decided_by_counts[decided_by] += 1
        if decided_by not in decided_by_tiers:
            decided_by_tiers[decided_by] = Counter()
        decided_by_tiers[decided_by][tier] += 1

    for decider, count in decided_by_counts.most_common():
        tiers = decided_by_tiers.get(decider, {})
        tier_str = " · ".join(f"{tier} {cnt}" for tier, cnt in sorted(tiers.items()))
        print(f"  {decider}: {count}건 | {tier_str}")

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
