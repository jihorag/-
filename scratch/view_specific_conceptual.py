import json

with open("questions_db.json", encoding="utf-8") as f:
    db = json.load(f)

target_ids = ["cem20190302-59", "cem20160312-64"]
for q in db:
    if q.get("id") in target_ids:
        print(f"ID: {q.get('id')}")
        print(f"Question:\n{q.get('question')}")
        print("Options:")
        for opt in q.get("options", []):
            print(opt)
        print(f"Answer: {q.get('answer')}")
        print(f"Explanation:\n{q.get('explanation')}")
        print("=" * 60)
