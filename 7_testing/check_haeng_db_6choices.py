import json

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    db_data = json.load(f)

# 6지선다인 문제들 찾기
six_choices = [q for q in db_data if len(q.get("choices", [])) == 6]
print(f"전체 DB에서 선지가 6개인 문제 수: {len(six_choices)}")

if six_choices:
    for i, q in enumerate(six_choices[:5]):
        print(f"\n[{i+1}] {q.get('year')} {q.get('subject')} {q.get('number')}번")
        print(f"Q: {q.get('question')[:100]}...")
        choices = q.get('choices', [])
        for j, c in enumerate(choices):
            print(f"  {j+1}: {c[:50]}")
