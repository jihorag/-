#!/usr/bin/env python3
"""셔플이 깨뜨린 해설-정답 번호 대응을 복구한다.

Task 2(shuffle_options.py)가 선지를 섞고 answer 를 갱신했지만, 해설 본문의
"정답은 N" 서술은 그대로 뒀다. 그 결과 해설이 옛 번호를 가리킨다.

처리 방식은 두 갈래다.
- 해설에 선지 번호 토큰이 "정답은 N" 하나뿐이면 → 그 번호만 현재 answer 로 치환
- 다른 선지를 번호로 지목하는 서술이 함께 있으면 → 치환이 위험하므로
  셔플 이전 선지 순서로 되돌린다(해설이 원래 그대로 맞았던 상태)

사용:
  python3 pipeline/9_tiering/fix_explanation_numbers.py [--dry-run] [--self-test]
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
PRE_SHUFFLE = Path.home() / "Documents" / "감정평가사-셔플복원본-20260829.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"

CIRCLED = {"①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5"}
TO_CIRCLED = {v: k for k, v in CIRCLED.items()}
ANS_RE = re.compile(r"(정답은?\s*)([1-5①-⑤])")
# "⑤는 옳지 않다" / "②가 정답" 처럼 선지를 원문자로 지목하는 서술.
# 이런 해설은 보통 "①~④는 모두 옳다" 처럼 다른 번호도 함께 참조하므로
# 번호 하나만 치환할 수 없다. 셔플 이전 순서로 되돌리는 것이 유일하게 안전하다.
CLAIM_RE = re.compile(r"([①-⑤])\s*(?:은|는|가|이)\s*(?:옳지 않|틀|정답|해당)")
# 선지를 번호로 지목하는 모든 흔적 — 열거용 ①②③ 도 여기 걸리지만 보수적으로 본다
REF_RE = re.compile(r"[①-⑤]|(?<![0-9)])[1-5]\s*번")


def stated_answer(explanation):
    """해설이 명시한 정답 번호. 없으면 None."""
    m = ANS_RE.search(explanation or "")
    if not m:
        return None
    return CIRCLED.get(m.group(2), m.group(2))


def claimed_option(explanation):
    """해설이 원문자로 지목한 선지 번호. 없으면 None."""
    m = CLAIM_RE.search(explanation or "")
    return CIRCLED.get(m.group(1)) if m else None


def is_safe_to_patch(explanation):
    """해설의 선지 번호 토큰이 '정답은 N' 하나뿐이면 치환이 안전하다."""
    m = ANS_RE.search(explanation or "")
    if not m:
        return False
    rest = (explanation[:m.start(2)] + explanation[m.end(2):])
    return not REF_RE.search(rest)


def patch(explanation, new_answer):
    """'정답은 N' 의 N 만 새 정답으로 바꾼다. 원문 표기(원문자/숫자)를 유지."""
    def repl(m):
        old = m.group(2)
        new = TO_CIRCLED[new_answer] if old in CIRCLED else new_answer
        return m.group(1) + new
    return ANS_RE.sub(repl, explanation, count=1)


def _self_test():
    assert stated_answer("따라서 정답은 ③입니다.") == "3"
    assert stated_answer("정답은 2번") == "2"
    assert stated_answer("해설만 있음") is None

    # 번호 토큰이 정답 진술 하나뿐 → 안전
    assert is_safe_to_patch("계산 결과 X 이므로 정답은 ②입니다.")
    # 다른 선지를 지목 → 위험
    assert not is_safe_to_patch("⑤는 틀린 설명입니다. 정답은 ⑤입니다.")
    assert not is_safe_to_patch("정답은 3번이고 1번은 오답이다.")

    # 치환은 표기를 유지한다
    assert patch("정답은 ②입니다.", "5") == "정답은 ⑤입니다."
    assert patch("정답은 2번", "5") == "정답은 5번"
    # 정답 진술만 바뀌고 나머지는 그대로
    assert patch("계산상 정답은 ①. 끝.", "4") == "계산상 정답은 ④. 끝."

    # 원문자로 선지를 지목하는 해설 인식
    assert claimed_option("⑤는 옳지 않다. ①~④는 모두 옳다.") == "5"
    assert claimed_option("②가 정답이다.") == "2"
    assert claimed_option("계산 결과만 있다.") is None
    print("fix_explanation_numbers self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return
    dry = "--dry-run" in sys.argv

    db = json.loads(DB.read_text(encoding="utf-8"))
    pre = {q["id"]: q for q in json.loads(PRE_SHUFFLE.read_text(encoding="utf-8"))}

    tally = Counter()
    for q in db:
        exp = q.get("explanation") or ""
        answer = str(q.get("answer")).strip()

        # 원문자로 선지를 지목하는 해설은 번호 치환이 불가능하므로 무조건 되돌린다
        claim = claimed_option(exp)
        if claim and claim != answer:
            orig = pre.get(q["id"]) or pre.get(re.sub(r"-dup\d+$", "", q["id"]))
            if orig and (orig.get("question") or "").strip() == (q.get("question") or "").strip():
                if not dry:
                    q["options"] = orig["options"]
                    q["answer"] = orig["answer"]
                    if isinstance(orig.get("option_meta"), list):
                        q["option_meta"] = orig["option_meta"]
                    tm = q.setdefault("tier_meta", {})
                    tm["shuffle_reverted"] = True
                    tm.pop("shuffled", None)
                tally["원문자 지목 → 셔플 되돌림"] += 1
            else:
                tally["원문자 지목 → 복원본 없음"] += 1
            continue

        said = stated_answer(exp)
        if not said or said == answer:
            continue
        if is_safe_to_patch(exp):
            if not dry:
                q["explanation"] = patch(exp, str(q.get("answer")).strip())
                q.setdefault("tier_meta", {})["explanation_renumbered"] = True
            tally["번호 치환"] += 1
            continue
        orig = pre.get(q["id"])
        if orig:                      # 셔플 이전 선지 순서로 되돌린다
            if not dry:
                q["options"] = orig["options"]
                q["answer"] = orig["answer"]
                if isinstance(orig.get("option_meta"), list):
                    q["option_meta"] = orig["option_meta"]
                tm = q.setdefault("tier_meta", {})
                tm["shuffle_reverted"] = True
                tm.pop("shuffled", None)
            tally["셔플 되돌림"] += 1
        else:
            tally["복원본에 없음(미처리)"] += 1

    for k, v in tally.most_common():
        print(f"  {k}: {v}")
    print(f"  합계: {sum(tally.values())}")
    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_expfix_{ts}.json")
    _atomic_write_json(DB, db)
    print(f"저장 완료 (백업 econ.pre_expfix_{ts}.json)")


if __name__ == "__main__":
    main()
