#!/usr/bin/env python3
"""게이트 v7 — 해설 자체가 생성기 정형구인 껍데기를 찾는다.

앞선 게이트들이 선지를 봤다면 여기서는 해설을 본다. 껍데기 문항은
해설도 틀에서 찍혀 나와, 주제어만 갈아 끼운 흔적이 문장에 그대로
남아 있다. 예컨대 "…는 경제학의 모든 분야를 포괄하는 단일 통합
이론은 아니다", "①②④⑤는 모두 자연과학·기타 분야로 경제학과
무관하다"(천체물리학·미생물학을 오답으로 세운 문항의 해설),
"표준 분석틀(이론 모형 + 실증 검증, 합리성·균형 가정)" 같은 문구다.

이 문구들은 정상적인 경제학 해설에는 나올 수 없을 만큼 특이해서
하나만 걸려도 껍데기로 본다. 선지 기반 게이트가 놓친 변종
(선지가 서로 안 닮았고 재사용도 아닌 경우)을 여기서 잡는다.

사용:
  python3 pipeline/9_tiering/gate_v7.py [--dry-run] [--self-test]
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
MACHINE = {"tier_gate", "gate_v2", "gate_v3", "gate_v4", "gate_v5", "gate_v6", "gate_v7"}

# 생성기가 해설에 남긴 정형구. 각각 정상 해설에는 나올 수 없는 표현이라
# 하나만 걸려도 껍데기로 판단한다.
BOILERPLATE = (
    "경제학의 모든 분야를 포괄하는 단일 통합 이론은 아니다",
    "표준 함수관계와 합리성 가정 하에서",
    "표준 분석틀(이론 모형 + 실증 검증",
    "학자의 정치적 견해 채택은 객관성을 해치는",
    "이는 경제학의 핵심 분석 방법이다",
    "관찰자의 개인적 취향은 객관성을 해치므로",
    "모두 자연과학·기타 분야로 경제학과 무관하다",
    "분석자의 주관적 판단에만 의존하는 것은 학문적 분석 원칙에 어긋난다",
    "학파별로 다양한 견해",
    "정의·분류·구성요소가 명확히 체계화됨",
    "비교정태분석에 의해 균형 변수에 예측 가능한 방향",
)


def matched(q):
    exp = q.get("explanation") or ""
    return [p for p in BOILERPLATE if p in exp]


def is_shell(q):
    return bool(matched(q))


def _self_test():
    shell = {"explanation": "재산세는 재정학 > 개별조세이론 영역의 특정 개념으로, "
                            "경제학의 모든 분야를 포괄하는 단일 통합 이론은 아니다."}
    assert is_shell(shell) and len(matched(shell)) == 1

    normal = {"explanation": "수요와 공급을 연립하면 3P=120이므로 균형가격은 40이고 "
                             "균형거래량은 60이다."}
    assert not is_shell(normal)

    empty = {"explanation": ""}
    assert not is_shell(empty)
    assert not is_shell({})

    multi = {"explanation": "표준 함수관계와 합리성 가정 하에서 변화는 "
                            "비교정태분석에 의해 균형 변수에 예측 가능한 방향으로 "
                            "영향을 미친다. 이는 경제학의 핵심 분석 방법이다."}
    assert len(matched(multi)) == 3
    print("gate_v7 self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return
    dry = "--dry-run" in sys.argv

    db = json.loads(DB.read_text(encoding="utf-8"))
    now = datetime.now().strftime("%Y-%m-%d")
    hit, from_tier, by_phrase = 0, Counter(), Counter()
    for q in db:
        tm = q.get("tier_meta") or {}
        if tm.get("decided_by") in MACHINE:
            continue
        hits = matched(q)
        if not hits:
            continue
        hit += 1
        from_tier[q.get("tier") or "미판정"] += 1
        by_phrase[hits[0]] += 1
        if dry:
            continue
        tm = q.get("tier_meta") or {}
        tm.update({"prev_tier": q.get("tier"), "prev_decided_by": tm.get("decided_by"),
                   "prev_reason": tm.get("reason"), "decided_by": "gate_v7",
                   "decided_at": now, "reason": f"해설 정형구 껍데기({hits[0][:24]})"})
        q["tier_meta"] = tm
        q["tier"] = "discard"

    print(f"  껍데기 검출: {hit}")
    print("  등급별 출처:", dict(from_tier))
    for p, n in by_phrase.most_common(5):
        print(f"    {n:4d}  {p[:44]}")
    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_gate_v7_{ts}.json")
    _atomic_write_json(DB, db)
    print(f"저장 완료 (백업 econ.pre_gate_v7_{ts}.json)")


if __name__ == "__main__":
    main()
