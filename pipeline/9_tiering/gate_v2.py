#!/usr/bin/env python3
"""게이트 v2 — 선지 품질 규칙.

Task 1 정량 게이트는 본문 길이·중복·해설길이·선지개수만 봤고 선지 자체의 품질은
보지 않았다. v1 자동생성 문항에 필러 선지("Pareto"·"관계 없음"·"정부 결정" 등)가
반복 등장해 A/B 등급까지 올라온 것을 여기서 걸러낸다.

세 가지 결함:
  - 필러선지: 필러 집합 중 2개 이상이 선지에 있음 → discard
  - 선지길이불균형: 최단 ≤3자, 최장 ≥20자 동시 성립 → discard
  - 초단문: 본문 30자 미만 → B만 배제(B였으면 A로 강등), 그 외 등급은 그대로

tier_gate.py 가 이미 버린 문항(decided_by == "tier_gate")은 건드리지 않는다.
멱등: decided_by == "gate_v2" 인 문항은 건너뛴다.

사용:
  python3 pipeline/9_tiering/gate_v2.py [--dry-run] [--self-test]
  python3 pipeline/9_tiering/gate_v2.py --repair-meta [--dry-run]   # 1회성 복구
"""
import json
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tier_judge import _atomic_write_json  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"

FILLERS = {"관계 없음", "Pareto", "정부 결정", "단순", "해당 없음", "없음"}
MIN_STEM_LEN = 30


def defects(q) -> list[str]:
    """구조 결함 이름 리스트를 돌려준다. 없으면 빈 리스트."""
    out = []
    options = q.get("options") or []

    filler_count = sum(1 for o in options if str(o).strip() in FILLERS)
    if filler_count >= 2:
        out.append("필러선지")

    if options:
        lens = [len(str(o).strip()) for o in options]
        if min(lens) <= 3 and max(lens) >= 20:
            out.append("선지길이불균형")

    stem = (q.get("question") or "").strip()
    if len(stem) < MIN_STEM_LEN:
        out.append("초단문")

    return out


def _apply_gate_v2(q, new_tier, now, reason, prev_tier):
    """tier_meta 를 병합해 gate_v2 판정을 기록한다.

    tier_judge.py 관행대로 통째 교체가 아니라 tm.update() 로 병합한다 —
    안 그러면 gemini 판정 근거(decided_by/reason)와 앵커·shuffled 마커가 사라진다.
    직전 decided_by/reason 은 prev_decided_by/prev_reason 으로 보존한다.
    """
    q["tier"] = new_tier
    tm = q.get("tier_meta") or {}
    prev_decided_by = tm.get("decided_by")
    prev_reason = tm.get("reason")
    tm.update({"decided_by": "gate_v2", "decided_at": now,
               "reason": reason, "prev_tier": prev_tier})
    if prev_decided_by is not None:
        tm["prev_decided_by"] = prev_decided_by
    if prev_reason is not None:
        tm["prev_reason"] = prev_reason
    q["tier_meta"] = tm


def _self_test():
    ok = {"question": "가"*50, "options": ["선지가나다라마","선지바사아자차","선지카타파하가","선지나다라마바","선지사아자차카"]}
    assert defects(ok) == []

    filler = {"question": "가"*50, "options": ["Pareto","관계 없음","정상선지가나다","정상선지나다라","정상선지다라마"]}
    assert "필러선지" in defects(filler)

    # 필러가 1개뿐이면 걸리지 않는다
    one = {"question": "가"*50, "options": ["Pareto","정상선지가나다","정상선지나다라","정상선지다라마","정상선지라마바"]}
    assert "필러선지" not in defects(one)

    imbal = {"question": "가"*50, "options": ["최대","이것은 아주 긴 선지입니다 정말로 깁니다","보통선지가","보통선지나","보통선지다"]}
    assert "선지길이불균형" in defects(imbal)

    short = {"question": "짧은 문두는?", "options": ["선지가나다라마","선지바사아자차","선지카타파하가","선지나다라마바","선지사아자차카"]}
    assert defects(short) == ["초단문"]

    # 병합: 기존 tier_meta(gemini 판정 근거·앵커·shuffled)를 지우지 않고
    # decided_by/reason 만 prev_* 로 옮긴 뒤 gate_v2 필드를 얹는다
    judged = {"tier": "A", "tier_meta": {"decided_by": "gemini:x", "reason": "원래 근거",
              "anchor_level": "item", "shuffled": True}}
    _apply_gate_v2(judged, "discard", "2026-08-29", "필러선지", "A")
    tm = judged["tier_meta"]
    assert tm["anchor_level"] == "item" and tm["shuffled"] is True
    assert tm["prev_decided_by"] == "gemini:x" and tm["prev_reason"] == "원래 근거"
    assert tm["decided_by"] == "gate_v2" and tm["prev_tier"] == "A"

    print("gate_v2 self-test 통과")


PRE_FIX_COMMIT = "3387677a"  # gate_v2 통째 교체 버그 이전 커밋 — 복구 원본


def _repair_meta(db):
    """gate_v2 초판(통째 교체)이 지운 tier_meta 필드를 커밋 3387677a 원본에서 복구한다.

    id 로 매칭한다(Task 7이 중복 id 5건을 개명했으므로 인덱스 매칭은 위험).
    gate_v2 의 결정(tier/decided_by=gate_v2/reason/prev_tier)은 그대로 두고,
    잃어버린 필드만 채운다. 이미 prev_decided_by 가 있으면(재실행 또는 병합판이
    처리한 것) 건드리지 않는다 — 멱등.
    """
    orig_raw = subprocess.run(
        ["git", "show", f"{PRE_FIX_COMMIT}:questions_db_econ.json"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    orig_by_id = {q["id"]: q for q in json.loads(orig_raw)}

    fixed = 0
    missing = 0
    for q in db:
        tm = q.get("tier_meta") or {}
        if tm.get("decided_by") != "gate_v2":
            continue
        if tm.get("meta_repaired"):
            continue  # 이미 이 스크립트로 처리됨 — 멱등
            # (prev_decided_by 유무로만 판단하면 원본이 애초에 미판정이라
            #  복구할 게 없는 286건이 매번 "처리됨"으로 재집계된다)

        orig = orig_by_id.get(q.get("id"))
        if orig is None:
            missing += 1
            continue
        orig_tm = orig.get("tier_meta") or {}

        if orig_tm.get("decided_by") is not None:
            tm["prev_decided_by"] = orig_tm["decided_by"]
        if orig_tm.get("reason") is not None:
            tm["prev_reason"] = orig_tm["reason"]
        for k in ("anchors", "anchor_level", "anchor_fallback", "shuffled"):
            if k in orig_tm and k not in tm:
                tm[k] = orig_tm[k]
        tm["meta_repaired"] = True
        q["tier_meta"] = tm
        fixed += 1

    return fixed, missing


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    if "--repair-meta" in sys.argv:
        dry = "--dry-run" in sys.argv
        db = json.loads(DB.read_text(encoding="utf-8"))
        fixed, missing = _repair_meta(db)
        print(f"복구 완료: {fixed}건 (원본에 없어 건너뜀 {missing}건)")
        if dry:
            print("dry-run — 저장하지 않음")
            return
        if fixed:
            BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2(DB, BACKUP_DIR / f"econ.pre_repair_meta_{ts}.json")
            _atomic_write_json(DB, db)
            print(f"저장 완료 (백업 econ.pre_repair_meta_{ts}.json)")
        return

    dry = "--dry-run" in sys.argv
    db = json.loads(DB.read_text(encoding="utf-8"))
    now = datetime.now().strftime("%Y-%m-%d")

    defect_counts = Counter()   # 결함 종류별 건수(중복 포함 — 한 문항이 여러 결함 가능)
    hit_any = 0                 # 하나라도 결함 있는 문항 수(중복 제외)
    discarded = 0
    demoted = 0
    a_discarded = 0   # A였다가 discard
    b_discarded = 0   # B였다가 discard
    unjudged_option_defects = 0  # 미판정 중 필러/불균형(판정 재개 시 API 절약분)
    n_checked = 0
    a_before = sum(1 for q in db if q.get("tier") == "A")
    b_before = sum(1 for q in db if q.get("tier") == "B")

    for q in db:
        meta = q.get("tier_meta") or {}
        if meta.get("decided_by") == "tier_gate":
            continue  # Task 1이 이미 버린 문항 — 건드리지 않는다
        if meta.get("decided_by") == "gate_v2":
            continue  # 멱등

        n_checked += 1
        ds = defects(q)
        if not ds:
            continue

        hit_any += 1
        for d in ds:
            defect_counts[d] += 1

        prev_tier = q.get("tier")
        option_defect = "필러선지" in ds or "선지길이불균형" in ds

        if not prev_tier and option_defect:
            unjudged_option_defects += 1

        if option_defect:
            reason = ",".join(ds)
            discarded += 1
            if prev_tier == "A":
                a_discarded += 1
            elif prev_tier == "B":
                b_discarded += 1
            if not dry:
                _apply_gate_v2(q, "discard", now, reason, prev_tier)
        elif "초단문" in ds and prev_tier == "B":
            demoted += 1
            if not dry:
                _apply_gate_v2(q, "A", now, "초단문", prev_tier)
        # 초단문 단독이고 prev_tier가 A·repair·미판정이면 그대로 둔다

    a_after = a_before - a_discarded + demoted
    b_after = b_before - b_discarded - demoted

    print(f"검사 대상(tier_gate 제외): {n_checked} / {len(db)}")
    print(f"결함 있는 문항(하나라도): {hit_any}")
    for k, v in defect_counts.most_common():
        print(f"  결함 {k}: {v} (중복 포함)")
    print(f"  discard 처리: {discarded} (A였던 것 {a_discarded} · B였던 것 {b_discarded})")
    print(f"  B→A 강등: {demoted}")
    print(f"  미판정 중 선지 결함(필러/불균형): {unjudged_option_defects}")
    print(f"  A: {a_before} → {a_after}, B: {b_before} → {b_after}")

    if dry:
        print("dry-run — 저장하지 않음")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_gate_v2_{ts}.json")
    _atomic_write_json(DB, db)
    print(f"저장 완료 (백업 econ.pre_gate_v2_{ts}.json)")


if __name__ == "__main__":
    main()
