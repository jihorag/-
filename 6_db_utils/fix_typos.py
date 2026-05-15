import json

db_path = "questions_db.json"
viewer_db_path = "viewer/src/data/questions_db.json"

def fix_options(q):
    if q.get("number") == "4":
        q["options"] = [
            "① 조세 부과시 초과부담은 후생(소비자잉여+생산자잉여) 감소분에서 조세 수입을 차감한 것이다.",
            "② 조세 부과시 상대가격 체계의 변화에 의해 민간부문의 의사결정이 왜곡되어 발생한다.",
            "③ 초과부담을 정확히 측정하려면 보상수요곡선을 사용해야 한다.",
            "④ 세율이 높을수록, 수요의 가격탄력성이 클수록 초과부담은 커진다.",
            "⑤ 대체재의 수가 적은 재화일수록 조세 부과의 초과부담은 커진다."
        ]
    elif q.get("number") == "11":
        q["options"] = [
            "① ㄱ, ㄴ, ㄷ",
            "② ㄱ, ㄴ, ㄹ",
            "③ ㄱ, ㄷ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄷ, ㄹ, ㅁ"
        ]

with open(db_path, "r", encoding="utf-8") as f:
    main_db = json.load(f)

for q in main_db:
    if q.get("exam") == "세무사" and q.get("subject") == "재정학":
        fix_options(q)

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(main_db, f, ensure_ascii=False, indent=2)

with open(viewer_db_path, "w", encoding="utf-8") as f:
    json.dump(main_db, f, ensure_ascii=False, indent=2)

print("Typos fixed!")
