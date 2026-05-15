import json

db_path = "questions_db.json"
viewer_db_path = "viewer/src/data/questions_db.json"
extracted_db_path = "tax_2026_s1_extracted.json"

with open(db_path, "r", encoding="utf-8") as f:
    main_db = json.load(f)

with open(extracted_db_path, "r", encoding="utf-8") as f:
    extracted = json.load(f)

seen_ids = {q.get("id") for q in main_db if q.get("id")}
added = 0

for q in extracted:
    # 감평사 시험 범위인 재정학만 필터링 (세법학개론 제외)
    if q.get("subject") != "재정학":
        continue
        
    q_id = f"tax_{q['year']}_{q['subject']}_{q['number']}"
    if q_id in seen_ids:
        continue
        
    q["id"] = q_id
    main_db.append(q)
    added += 1

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(main_db, f, ensure_ascii=False, indent=2)

with open(viewer_db_path, "w", encoding="utf-8") as f:
    json.dump(main_db, f, ensure_ascii=False, indent=2)

print(f"재정학 문제 {added}개가 성공적으로 메인 DB에 병합되었습니다.")
