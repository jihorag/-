import json

db_path = "questions_db.json"

with open(db_path, "r", encoding="utf-8") as f:
    db_data = json.load(f)

# 행정사 과목 찾기
haeng_questions = [q for q in db_data if "행정사" in q.get("exam", "")]
if not haeng_questions:
    haeng_questions = [q for q in db_data if "행정사" in q.get("subject", "")]

print(f"행정사 문제 수: {len(haeng_questions)}")
if haeng_questions:
    for i, q in enumerate(haeng_questions[:3]):
        print(f"\n[{i+1}] {q.get('year')} {q.get('subject')} {q.get('number')}번")
        print(f"Q: {q.get('question')[:100]}...")
        choices = q.get('choices', [])
        print(f"선지 수: {len(choices)}")
        for j, c in enumerate(choices):
            print(f"  {j+1}: {c[:50]}")
