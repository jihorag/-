import json
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
QDB = ROOT / "questions_db.json"

with open(QDB, "r", encoding="utf-8") as f:
    db = json.load(f)

# count subjects mapped in indexing_v4
subjects_in_tag = Counter()
subjects_in_main = Counter()
subjects_in_mapped = Counter()

for q in db:
    subjects_in_main[q.get("subject")] += 1
    if "tags" in q and q["tags"]:
        subjects_in_tag[q["tags"].get("subject")] += 1
    if "indexing_v4" in q and q["indexing_v4"] and "mapped_taxonomy" in q["indexing_v4"] and q["indexing_v4"]["mapped_taxonomy"]:
        subjects_in_mapped[q["indexing_v4"]["mapped_taxonomy"].get("subject")] += 1

print("Main subjects:")
for k, v in subjects_in_main.most_common():
    print(f"  {k}: {v}")

print("\nTags subjects:")
for k, v in subjects_in_tag.most_common():
    print(f"  {k}: {v}")

print("\nMapped taxonomy subjects:")
for k, v in subjects_in_mapped.most_common():
    print(f"  {k}: {v}")
