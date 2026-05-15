import json

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    db_data = json.load(f)

fix_count = 0
for q in db_data:
    if "행정사" in q.get("exam", "") or "행정" in q.get("subject", ""):
        opts = q.get("options", [])
        if len(opts) == 6 and opts[0] == opts[1]:
            opts.pop(1)  # 2번째 원소 제거
            fix_count += 1

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db_data, f, ensure_ascii=False, indent=2)

print(f"중복된 행정사 선지 수정 완료. (수정된 문제 수: {fix_count})")
