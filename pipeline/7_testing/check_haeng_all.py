import json

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    db_data = json.load(f)

haeng = [q for q in db_data if "행정사" in q.get("exam", "")]

count = 0
for q in haeng:
    opts = q.get("options", [])
    if len(opts) == 6 and opts[0] == opts[1]:
        count += 1

print(f"행정사 문제 {len(haeng)}개 중 옵션이 6개이고 1,2번이 중복인 문제 수: {count}")
