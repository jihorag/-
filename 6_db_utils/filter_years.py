import json
import shutil

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

print(f"Original DB size: {len(db)}")

filtered_db = []
for q in db:
    year = int(q.get('year', 0))
    exam = q.get('exam', '감정평가사')
    
    if exam == '감정평가사' or year >= 2014:
        filtered_db.append(q)

print(f"Filtered DB size: {len(filtered_db)}")
removed = len(db) - len(filtered_db)
print(f"Removed {removed} questions (older than 2014, non-감정평가사).")

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(filtered_db, f, ensure_ascii=False, indent=2)

shutil.copy(db_path, 'viewer/src/data/questions_db.json')
print("Viewer DB updated.")
