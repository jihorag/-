import json
import os
from collections import Counter

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
QDB = os.path.join(ROOT, "questions_db.json")

with open(QDB, "r", encoding="utf-8") as f:
    db = json.load(f)

practice_by_subject = Counter()
for q in db:
    if q.get("tags", {}).get("is_practice", False):
        practice_by_subject[q.get("subject")] += 1

print("Practice questions count by subject:")
for k, v in practice_by_subject.items():
    print(f"  - {k}: {v}")
