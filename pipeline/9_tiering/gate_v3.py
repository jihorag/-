#!/usr/bin/env python3
"""게이트 v3 — 정답 정합성 결함을 걸러낸다.

gate_v2 가 선지 '형태'를 봤다면 여기서는 정답과 해설·선지·본문 사이의
'정합성'을 본다. 셋 다 학습자가 틀린 것을 외우게 만드는 결함이다.

- 해설-정답 불일치: 해설이 명시한 정답 번호가 answer 와 다르다
- 선지 중복: 같은 선지가 두 번 나온다(정답이 유일하지 않을 수 있다)
- 본문에 정답 노출: 정답 선지 문구가 문제 본문에 그대로 있다

tier_gate·gate_v2 가 이미 버린 문항은 건드리지 않는다.
멱등: decided_by == "gate_v3" 이면 건너뛴다.

사용:
  python3 pipeline/9_tiering/gate_v3.py [--dry-run] [--self-test]
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
MACHINE = {"tier_gate", "gate_v2", "gate_v3"}

CIRCLED = {"①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5"}
ANS_RE = re.compile(r"정답은?\s*([1-5①-⑤])")
LEAK_MIN = 6          # 이보다 짧은 선지는 본문에 우연히 들어갈 수 있다


def _opts(q):
    return [str(o).strip() for o in (q.get("options") or [])]


def _ans_index(q):
    try:
        return int(str(q.get("answer")).strip()) - 1
    except (TypeError, ValueError):
        return -1


def defects(q):
    """정합성 결함 목록. 없으면 빈 리스트."""
    out = []
    opts, i = _opts(q), _ans_index(q)

    m = ANS_RE.search(q.get("explanation") or "")
    if m:
        said = CIRCLED.get(m.group(1), m.group(1))
        if said != str(q.get("answer")).strip():
            out.append("해설정답불일치")

    if opts and len(set(opts)) < len(opts):
        out.append("선지중복")

    if 0 <= i < len(opts) and len(opts[i]) >= LEAK_MIN and opts[i] in (q.get("question") or ""):
        out.append("본문정답노출")
    return out


def _self_test():
    ok = {"question": "문제 본문", "options": ["가나다라", "마바사아", "자차카타", "파하가나", "다라마바"],
          "answer": "2", "explanation": "따라서 정답은 ②입니다."}
    assert defects(ok) == []

    mism = dict(ok, explanation="따라서 정답은 ③입니다.")
    assert defects(mism) == ["해설정답불일치"]

    dup = dict(ok, options=["가나다라", "가나다라", "자차카타", "파하가나", "다라마바"])
    assert defects(dup) == ["선지중복"]

    leak = dict(ok, options=["가나다라", "수요의 가격탄력성", "자차카타", "파하가나", "다라마바"],
                question="수요의 가격탄력성 에 관한 설명으로 옳은 것은?")
    assert defects(leak) == ["본문정답노출"]

    # 짧은 선지는 우연한 포함으로 보고 노출로 치지 않는다
    short = dict(ok, options=["가나다라", "증가", "자차카타", "파하가나", "다라마바"],
                 question="증가 여부를 묻는다")
    assert "본문정답노출" not in defects(short)

    # 해설에 정답 진술이 없으면 불일치를 판단하지 않는다
    noans = dict(ok, explanation="계산 과정만 있다")
    assert defects(noans) == []
    print("gate_v3 self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return
    dry = "--dry-run" in sys.argv

    db = json.loads(DB.read_text(encoding="utf-8"))
    now = datetime.now().strftime("%Y-%m-%d")
    tally = Counter()
    for q in db:
        tm = q.get("tier_meta") or {}
        if tm.get("decided_by") in MACHINE:      # 기계 규칙이 이미 버린 문항
            continue
        d = defects(q)
        if not d:
            continue
        for x in d:
            tally[x] += 1
        tally["_문항"] += 1
        if dry:
            continue
        tm = q.get("tier_meta") or {}
        tm.update({"prev_tier": q.get("tier"), "prev_decided_by": tm.get("decided_by"),
                   "prev_reason": tm.get("reason"), "decided_by": "gate_v3",
                   "decided_at": now, "reason": ",".join(d)})
        q["tier_meta"] = tm
        q["tier"] = "discard"

    for k, v in tally.most_common():
        print(f"  {k}: {v}")
    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_gate_v3_{ts}.json")
    _atomic_write_json(DB, db)
    print(f"저장 완료 (백업 econ.pre_gate_v3_{ts}.json)")


if __name__ == "__main__":
    main()
