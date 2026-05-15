import json

main_db_path = "questions_db.json"
extracted_db_path = "tax_2026_s1_extracted.json"
viewer_db_path = "viewer/src/data/questions_db.json"

with open(main_db_path, "r", encoding="utf-8") as f:
    main_db = json.load(f)

with open(extracted_db_path, "r", encoding="utf-8") as f:
    extracted = json.load(f)

# 고유 ID 생성 후 메인 DB에 추가
for q in extracted:
    # 기존에 같은 번호/연도/과목이 있는지 체크 (덮어쓰기 로직 등)
    # 테스트이므로 단순 추가
    q["id"] = f"tax_{q['year']}_{q['subject']}_{q['number']}"
    # 선지를 choices 대신 options로 유지해도 무방 (App.jsx에서 q.options 지원함)
    main_db.append(q)

with open(main_db_path, "w", encoding="utf-8") as f:
    json.dump(main_db, f, ensure_ascii=False, indent=2)

with open(viewer_db_path, "w", encoding="utf-8") as f:
    json.dump(main_db, f, ensure_ascii=False, indent=2)

print("3개의 테스트 추출 문제가 메인 DB에 성공적으로 병합되었습니다.")
