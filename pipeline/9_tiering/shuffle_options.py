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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tier_judge import _atomic_write_json  # noqa: E402

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
    _atomic_write_json(DB, db)
    print(f"저장 완료 (백업 econ.pre_shuffle_{ts}.json)")


if __name__ == "__main__":
    main()
