"""1단계 데이터 품질 보정: answer 필드 결정적 정규화 (무위험·가역).

- 원문자 ①②③… → '1','2',…
- 앞뒤 공백 trim
- 유효한 숫자 정답은 그대로, 무효(빈/센티넬)는 손대지 않음(3단계 LLM 대상)
- 기존 유효 정답을 절대 덮어쓰지 않음

사용: python3 pipeline/6_db_utils/normalize_answers.py [--apply]
인자 없으면 dry-run(미리보기), --apply 면 questions_db.json 갱신.
"""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE, "questions_db.json")
CIRCLED = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5',
           '⑥': '6', '⑦': '7', '⑧': '8', '⑨': '9', '⑩': '10'}


def normalized(raw):
    """정규화 결과(str) 또는 None(변경 불필요/불가)."""
    if raw is None:
        return None
    s = str(raw).strip()
    s2 = CIRCLED.get(s, s)
    if s2 == str(raw):
        return None              # 변경 없음
    return s2 if s2.isdigit() else None


def main():
    apply = "--apply" in sys.argv
    db = json.load(open(DB))
    changes = []
    for q in db:
        n = normalized(q.get("answer"))
        if n is not None:
            changes.append((q.get("id"), repr(q.get("answer")), n))
            if apply:
                q["answer"] = n
                q.setdefault("data_quality", {})["answer_normalized"] = True

    print(f"정규화 대상 {len(changes)}건")
    for c in changes[:15]:
        print("  ", c)
    if apply and changes:
        tmp = DB + ".tmp"
        json.dump(db, open(tmp, "w"), ensure_ascii=False, indent=2)
        os.replace(tmp, DB)
        print("적용 완료 → questions_db.json")
    elif not apply:
        print("(dry-run) 적용하려면 --apply")


if __name__ == "__main__":
    main()
