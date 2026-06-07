import json
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
QDB = ROOT / "questions_db.json"

with open(QDB, "r", encoding="utf-8") as f:
    db = json.load(f)

law_qs = []
for q in db:
    if "indexing_v4" in q and q["indexing_v4"] and "mapped_taxonomy" in q["indexing_v4"] and q["indexing_v4"]["mapped_taxonomy"]:
        if q["indexing_v4"]["mapped_taxonomy"].get("subject") == "감정평가관계법규":
            law_qs.append(q)

print(f"Found {len(law_qs)} questions mapped to 감정평가관계법규 in taxonomy.")
for i in range(min(5, len(law_qs))):
    q = law_qs[i]
    print(f"\n[{i+1}] ID: {q['id']}, Exam: {q.get('exam')}, Year: {q.get('year')}")
    print(f"Question: {q['question']}")
    print(f"Options: {q['options']}")
    print(f"Answer: {q['answer']}")
    print(f"Explanation: {q['explanation'][:200]}...")
    print(f"Mapped chapter: {q['indexing_v4']['mapped_taxonomy'].get('chapter')}")
    print(f"Mapped section: {q['indexing_v4']['mapped_taxonomy'].get('section')}")
