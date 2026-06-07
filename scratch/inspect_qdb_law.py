import json
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
QDB = ROOT / "questions_db.json"

with open(QDB, "r", encoding="utf-8") as f:
    db = json.load(f)

law_qs = [q for q in db if q.get("subject") == "감정평가관계법규"]
print(f"Total law questions in QDB: {len(law_qs)}")
if law_qs:
    print("Example question:")
    print(json.dumps(law_qs[0], ensure_ascii=False, indent=2))
