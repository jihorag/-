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
