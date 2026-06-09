import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db.json"

with open(DB_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

matching = []
for q in data:
    if q.get("subject") == "회계학":
        mapped = q.get("indexing_v4", {}).get("mapped_taxonomy", {})
        if mapped and mapped.get("section") == "Chapter 01 개념체계":
            q_text = q.get("question", "")
            if any(k in q_text for k in ["목적", "위상", "이용자", "기준서"]):
                matching.append(q)

print(f"Found {len(matching)} questions with keywords:")
for q in matching:
    idx = q.get("indexing_v4", {}).get("mapped_taxonomy", {})
    print(f"- ID: {q['id']}, Number: {q.get('number')}, Mapped item: {idx.get('item')}")
    print(f"  Question: {q['question']}")
    print(f"  Options: {q.get('options')}")
    print(f"  Answer: {q.get('answer')}")
    print()
