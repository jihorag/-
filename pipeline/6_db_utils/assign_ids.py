import json
import os
import shutil

db_path = 'questions_db.json'
if not os.path.exists(db_path):
    print("DB file not found.")
    exit()

db = json.load(open(db_path, encoding='utf-8'))

assigned_count = 0
for q in db:
    if 'id' not in q:
        period = q.get('period', 'x')
        date = q.get('exam_date', '00000000').replace('-', '')
        num = q.get('number', '0')
        # Ensure ID is unique by including a bit of exam name if needed
        # but period+date+num is usually enough for cbtbank
        q['id'] = f"{period}{date}-{num}"
        assigned_count += 1

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

shutil.copy(db_path, 'viewer/src/data/questions_db.json')
print(f"Successfully assigned IDs to {assigned_count} questions.")
