"""텍스트 기반 문항 배치 추출 (이미지 없이 question+options 텍스트만).
사용법: python3 scratch/pick_text_batch.py <EXAM> <N> [SUBJECT]
- 이미 Gemini/Claude로 분류된(indexing_v4 + processed_by) 문항은 건너뜀
- 본문이 [IMAGE:]뿐인 이미지 의존 문항은 제외
- scratch/text_batch_current.json 에 기록
"""
import json, os, re, sys, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE, "questions_db.json")
IMG_RE = re.compile(r"\[IMAGE:[^\]]*\]")


def safe_load(path, tries=20):
    for _ in range(tries):
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            time.sleep(0.5)
    sys.exit("could not read " + path)


def already_classified(q):
    iv = q.get("indexing_v4")
    if not isinstance(iv, dict):
        return False
    mt = iv.get("mapped_taxonomy")
    return bool(
        mt and mt.get("subject")
        and iv.get("processed_by") in ("gemini-2.5-flash", "claude-sonnet-4-6")
        and iv.get("in_scope") is not False
    )


def is_text(q):
    stem = IMG_RE.sub("", q.get("question", "") or "").strip()
    return len(stem) >= 10


def main():
    exam, n = sys.argv[1], int(sys.argv[2])
    subject = sys.argv[3] if len(sys.argv) > 3 else None
    db = safe_load(DB)
    todo = [
        q for q in db
        if q.get("exam") == exam and not already_classified(q) and is_text(q)
        and (subject is None or (q.get("subject") or q.get("tags", {}).get("subject")) == subject)
    ]
    batch = todo[:n]
    out = []
    for q in batch:
        out.append({
            "id": q["id"],
            "subject": q.get("subject") or q.get("tags", {}).get("subject"),
            "year": q.get("year"),
            "question": IMG_RE.sub("", q.get("question", "") or "").strip(),
            "options": q.get("options") or q.get("choices"),
        })
    json.dump(out, open(os.path.join(BASE, "scratch/text_batch_current.json"), "w"),
              ensure_ascii=False, indent=2)
    from collections import Counter
    print(f"exam={exam} subject={subject} remaining_todo={len(todo)} picked={len(out)}")
    print("subj분포(남은전체):", dict(Counter(
        (q.get('subject') or q.get('tags', {}).get('subject')) for q in todo)))
    print("이번배치 subj:", dict(Counter(o['subject'] for o in out)))


if __name__ == "__main__":
    main()
