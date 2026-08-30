#!/usr/bin/env python3
"""게이트 v6 — 여러 문항에 그대로 재사용된 선지로 껍데기를 찾는다.

v1 생성기는 선지 묶음을 만들어 두고 주제어만 바꿔 여러 절에 돌려썼다.
예컨대 "단기와 장기 효과의 구별 부재 / 모형 가정의 비현실성 간과 /
인과관계와 상관관계의 혼동 / 외생변수와 내생변수의 혼동 / 객관적 자료
수집·분석" 다섯 선지가 재산세·빈곤의 측정·공채·리카도 등가정리 문항에
똑같이 쓰였다. 주제어는 문두에만 있어 무엇을 묻는지가 없다.

앞선 게이트들이 문구 목록을 손으로 적었다면 여기서는 코퍼스 자체에서
반복 선지를 세어 채움말 집합을 만든다. 목록을 유지보수할 필요가 없고
새 패턴도 자동으로 잡힌다.

"ㄱ, ㄴ, ㄷ, ㄹ" 같은 보기결합형 선지는 정상적으로 반복되므로 제외한다.

사용:
  python3 pipeline/9_tiering/gate_v6.py [--dry-run] [--self-test]
"""
import json
import re
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
MACHINE = {"tier_gate", "gate_v2", "gate_v3", "gate_v4", "gate_v5", "gate_v6"}

MIN_REUSE = 8       # 이만큼 여러 문항에 그대로 나오면 채움말로 본다
MIN_HITS = 2        # 한 문항에 채움말이 이만큼 있으면 껍데기
MIN_LEN = 10        # 너무 짧은 선지는 우연히 겹칠 수 있다
# 보기결합형·기호형 선지는 반복이 정상이므로 채움말 후보에서 뺀다
BOXLIKE = re.compile(r"^[ㄱ-ㅎA-Ea-e0-9,\s·~×\-]+$")


def _opts(q):
    return [str(o).strip() for o in (q.get("options") or [])]


def build_filler_set(questions):
    """여러 문항에 그대로 재사용된 선지 집합."""
    counts = Counter()
    for q in questions:
        for o in _opts(q):
            if len(o) >= MIN_LEN and not BOXLIKE.match(o):
                counts[o] += 1
    return {o for o, n in counts.items() if n >= MIN_REUSE}


def filler_hits(q, filler):
    return sum(1 for o in _opts(q) if o in filler)


def is_shell(q, filler):
    return filler_hits(q, filler) >= MIN_HITS


def _self_test():
    shared = ["단기와 장기 효과의 구별 부재", "모형 가정의 비현실성 간과",
              "인과관계와 상관관계의 혼동", "외생변수와 내생변수의 혼동",
              "객관적 자료 수집·분석"]
    # 같은 선지 묶음을 여덟 문항이 돌려쓰면 채움말로 잡힌다
    corpus = [{"options": shared} for _ in range(8)]
    filler = build_filler_set(corpus)
    assert set(shared) <= filler
    assert is_shell({"options": shared}, filler)

    # 두 개 미만이면 남긴다
    assert not is_shell({"options": [shared[0], "정상 선지 하나입니다",
                                     "정상 선지 둘입니다", "정상 선지 셋입니다",
                                     "정상 선지 넷입니다"]}, filler)

    # 보기결합형은 아무리 반복돼도 채움말이 아니다
    box = [{"options": ["ㄱ, ㄴ", "ㄱ, ㄴ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ, ㄹ"]}
           for _ in range(20)]
    assert build_filler_set(box) == set()

    # 반복되지 않는 정상 문항은 걸리지 않는다
    normal = [{"options": [f"균형가격 {i}, 균형거래량 {i*2}" for i in range(5)]}]
    assert build_filler_set(normal) == set()
    print("gate_v6 self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return
    dry = "--dry-run" in sys.argv

    db = json.loads(DB.read_text(encoding="utf-8"))
    live = [q for q in db if (q.get("tier_meta") or {}).get("decided_by") not in MACHINE]
    filler = build_filler_set(live)
    print(f"  재사용 선지 {len(filler)}종 (기준 {MIN_REUSE}회 이상)")

    now = datetime.now().strftime("%Y-%m-%d")
    hit, from_tier = 0, Counter()
    for q in live:
        if not is_shell(q, filler):
            continue
        hit += 1
        from_tier[q.get("tier") or "미판정"] += 1
        if dry:
            continue
        tm = q.get("tier_meta") or {}
        tm.update({"prev_tier": q.get("tier"), "prev_decided_by": tm.get("decided_by"),
                   "prev_reason": tm.get("reason"), "decided_by": "gate_v6",
                   "decided_at": now,
                   "reason": f"재사용 선지 껍데기({filler_hits(q, filler)}개)"})
        q["tier_meta"] = tm
        q["tier"] = "discard"

    print(f"  껍데기 검출: {hit}")
    print("  등급별 출처:", dict(from_tier))
    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_gate_v6_{ts}.json")
    _atomic_write_json(DB, db)
    print(f"저장 완료 (백업 econ.pre_gate_v6_{ts}.json)")


if __name__ == "__main__":
    main()
