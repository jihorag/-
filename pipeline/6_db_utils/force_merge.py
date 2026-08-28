import json

db_path = "questions_db.json"
viewer_db_path = "viewer/src/data/questions_db.json"
extracted_db_path = "tax_2026_s1_extracted.json"

with open(db_path, "r", encoding="utf-8") as f:
    main_db = json.load(f)

with open(extracted_db_path, "r", encoding="utf-8") as f:
    extracted = json.load(f)

updated = 0
for ext_q in extracted:
    q_id = f"tax_{ext_q['year']}_{ext_q['subject']}_{ext_q['number']}"
    for db_q in main_db:
        if db_q.get("id") == q_id:
            db_q["options"] = ext_q.get("options", db_q.get("options"))
            db_q["answer"] = ext_q.get("answer", db_q.get("answer"))
            db_q["explanation"] = ext_q.get("explanation", db_q.get("explanation"))
            db_q["tags"] = ext_q.get("tags", db_q.get("tags"))
            updated += 1
            break

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(main_db, f, ensure_ascii=False, indent=2)

with open(viewer_db_path, "w", encoding="utf-8") as f:
    json.dump(main_db, f, ensure_ascii=False, indent=2)

print(f"Force updated {updated} questions!")
