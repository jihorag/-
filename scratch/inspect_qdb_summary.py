import json
import os
from collections import Counter

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
QDB = os.path.join(ROOT, "questions_db.json")

with open(QDB, "r", encoding="utf-8") as f:
    db = json.load(f)

print(f"Total questions in DB: {len(db)}")

subjects = Counter()
exams = Counter()
is_practice = Counter()

for q in db:
    subjects[q.get("subject")] += 1
    exams[q.get("exam")] += 1
    is_practice[q.get("tags", {}).get("is_practice", False)] += 1

print("\nSubjects:")
for k, v in subjects.items():
    print(f"  - {k}: {v}")

print("\nExams:")
for k, v in exams.items():
    print(f"  - {k}: {v}")

print("\nIs Practice:")
for k, v in is_practice.items():
    print(f"  - {k}: {v}")
