import json

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    db_data = json.load(f)

haeng = [q for q in db_data if "행정사" in q.get("exam", "")]
if not haeng:
    haeng = [q for q in db_data if "행정사" in q.get("subject", "") or "행정" in q.get("exam", "")]

if not haeng:
    # try searching exam="행정"
    for q in db_data:
        if q.get("exam") == "행정사":
            haeng.append(q)

for i, q in enumerate(haeng[:2]):
    print(json.dumps(q, ensure_ascii=False, indent=2))
