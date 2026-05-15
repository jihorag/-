import json

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    db_data = json.load(f)

for q in db_data[:2]:
    print(list(q.keys()))
