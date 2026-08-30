#!/usr/bin/env python3
"""게이트 v4 — 지식 없이 풀리는 자동생성 껍데기 문항을 걸러낸다.

gate_v2 가 선지의 '형태', gate_v3 가 정답 '정합성'을 봤다면 여기서는
문항이 실제로 무엇인가를 묻고 있는지를 본다. 두 패턴 모두 v1 자동생성기가
선지를 채우지 못해 남긴 흔적이다.

- 플레이스홀더: 선지에 "(오답 방지 선지 N)" 이나
  "해당 개념에 부합하지 않는 …" 같은 생성기 안내문이 그대로 노출된다.
- 동어반복 템플릿: 선지 넷 이상이 문제의 주제어로 시작하고, 정답은
  "…영역의 주요 개념으로 관련 이론·원칙을 체계적으로 적용한다" 식의
  순환 정의다. 나머지는 "경제학과 무관한 개념이다" 같은 억지라
  주제를 몰라도 정답을 고를 수 있다.

숫자형 계산문항은 선지가 "소비자 부담액 = " 처럼 구조를 공유하는 것이
정상이므로, 접두사가 문제 본문에도 등장할 때만 동어반복으로 본다.

tier_gate·gate_v2·gate_v3 가 이미 버린 문항은 건드리지 않는다.
멱등: decided_by == "gate_v4" 이면 건너뛴다.

사용:
  python3 pipeline/9_tiering/gate_v4.py [--dry-run] [--self-test]
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
MACHINE = {"tier_gate", "gate_v2", "gate_v3", "gate_v4"}

PLACEHOLDER = re.compile(r"오답\s*방지\s*선지|해당 개념에 부합하지 않는")
# 정답 선지가 주제어를 되풀이하는 순환 정의인지 가르는 상투구.
# 이 조건이 없으면 "경제활동참가율 = 70%, 실업률 = 14.3%" 같은
# 정상 계산 선지까지 접두사 공유만으로 걸려 오탐이 난다.
BOILERPLATE = re.compile(
    r"주요 개념|체계적으로|이론·법칙·원칙|이론·원칙|분야에서 다루는|영역에서 다루|핵심적 위치|학문적 분석")
PREFIX_LENGTHS = (8, 10, 12)
MIN_SHARED = 4          # 5지 중 넷 이상이 같은 주제어로 시작해야 한다
STEM_ECHO = 6           # 접두사 앞 6자가 문제 본문에 있으면 주제어 반복으로 본다


def _opts(q):
    return [str(o).strip() for o in (q.get("options") or [])]


def has_placeholder(q):
    return any(PLACEHOLDER.search(o) for o in _opts(q))


def _answer_index(q):
    try:
        return int(str(q.get("answer")).strip()) - 1
    except (TypeError, ValueError):
        return -1


def is_tautology(q):
    """선지 다수가 주제어를 되풀이하고 정답이 순환 정의인 껍데기 문항인가."""
    opts, stem = _opts(q), q.get("question") or ""
    i = _answer_index(q)
    if len(opts) < 5 or not (0 <= i < len(opts)):
        return False
    if not BOILERPLATE.search(opts[i]):     # 정답이 순환 정의가 아니면 정상 문항
        return False
    for length in PREFIX_LENGTHS:
        counts = Counter(o[:length] for o in opts if len(o) >= length)
        if not counts:
            continue
        prefix, n = counts.most_common(1)[0]
        if n >= MIN_SHARED and prefix[:STEM_ECHO] in stem:
            return True
    return False


def defects(q):
    out = []
    if has_placeholder(q):
        out.append("플레이스홀더선지")
    if is_tautology(q):
        out.append("동어반복템플릿")
    return out


def _self_test():
    ok = {"question": "수요의 가격탄력성에 관한 설명으로 옳은 것은?",
          "options": ["탄력성은 1보다 크다", "기울기와 같다", "항상 0이다",
                      "소득과 무관하다", "대체재가 많을수록 커진다"]}
    assert defects(ok) == []

    ph = dict(ok, options=["정상 선지 하나", "해당 개념에 부합하지 않는 거시경제적 설명 (오답 방지 선지 1)",
                           "가", "나", "다"])
    assert defects(ph) == ["플레이스홀더선지"]

    taut = {"question": "조세전가의 개념에 관한 설명으로 옳은 것은?", "answer": "5",
            "options": ["조세전가의 개념은 측정이 불가능하다",
                        "조세전가의 개념은 일관된 정의가 없다",
                        "조세전가의 개념은 경제학과 무관하다",
                        "조세전가의 개념은 정부 개입으로만 분석된다",
                        "조세전가의 개념은 조세 귀착 분야에서 다루는 주요 개념이다"]}
    assert defects(taut) == ["동어반복템플릿"]

    # 정답이 순환 정의가 아니면 접두사를 공유해도 정상 문항이다
    numeric = {"question": "경제활동참가율과 실업률의 조합으로 옳은 것은?", "answer": "5",
               "options": ["경제활동참가율 = 60%, 실업률 = 16.7%",
                           "경제활동참가율 = 60%, 실업률 = 14.3%",
                           "경제활동참가율 = 70%, 실업률 = 10.0%",
                           "경제활동참가율 = 50%, 실업률 = 20.0%",
                           "경제활동참가율 = 70%, 실업률 = 14.3%"]}
    assert defects(numeric) == []

    # 계산문항은 선지가 구조를 공유해도 걸리지 않는다 — 접두사가 본문에 없다
    calc = {"question": "수요가 Qd=100-P, 공급이 Qs=-20+2P일 때 조세 부담은?", "answer": "3",
            "options": ["소비자 부담액 = 5, 정부 세입 = 750",
                        "소비자 부담액 = 10, 정부 세입 = 600",
                        "소비자 부담액 = 10, 정부 세입 = 750",
                        "소비자 부담액 = 5, 정부 세입 = 600",
                        "소비자 부담액 = 15, 정부 세입 = 900"]}
    assert defects(calc) == []

    # 선지가 5개 미만이면 판정하지 않는다
    assert defects({"question": "x", "answer": "1", "options": ["a", "b"]}) == []
    print("gate_v4 self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return
    dry = "--dry-run" in sys.argv

    db = json.loads(DB.read_text(encoding="utf-8"))
    now = datetime.now().strftime("%Y-%m-%d")
    tally, from_tier = Counter(), Counter()
    for q in db:
        tm = q.get("tier_meta") or {}
        if tm.get("decided_by") in MACHINE:
            continue
        d = defects(q)
        if not d:
            continue
        for x in d:
            tally[x] += 1
        tally["_문항"] += 1
        from_tier[q.get("tier") or "미판정"] += 1
        if dry:
            continue
        tm = q.get("tier_meta") or {}
        tm.update({"prev_tier": q.get("tier"), "prev_decided_by": tm.get("decided_by"),
                   "prev_reason": tm.get("reason"), "decided_by": "gate_v4",
                   "decided_at": now, "reason": ",".join(d)})
        q["tier_meta"] = tm
        q["tier"] = "discard"

    for k, v in tally.most_common():
        print(f"  {k}: {v}")
    print("  등급별 출처:", dict(from_tier))
    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_gate_v4_{ts}.json")
    _atomic_write_json(DB, db)
    print(f"저장 완료 (백업 econ.pre_gate_v4_{ts}.json)")


if __name__ == "__main__":
    main()
