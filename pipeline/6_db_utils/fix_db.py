import json
import shutil

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

new_db = []
seen_haengjeongsa = set()

for q in db:
    if q.get('exam') == '행정사':
        key = f"{q.get('year')}_{q.get('number')}"
        if key in seen_haengjeongsa:
            continue
        seen_haengjeongsa.add(key)
    new_db.append(q)

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(new_db, f, ensure_ascii=False, indent=2)

shutil.copy(db_path, 'viewer/src/data/questions_db.json')
print(f"Fixed DB size: {len(new_db)} (removed {len(db) - len(new_db)} duplicates)")
