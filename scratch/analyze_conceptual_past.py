import json

with open("questions_db.json", encoding="utf-8") as f:
    db = json.load(f)

past_qs = []
for q in db:
    subj = q.get("subject", "")
    exam = q.get("exam", "")
    question = q.get("question", "")
    
    if "회계" in subj and "감정평가사" in exam:
        keywords = ["개념체계", "재무보고", "질적 특성", "목적적합성", "표현충실성", "비교가능성", "검증가능성", "적시성", "이해가능성"]
        if any(kw in question or kw in q.get("explanation", "") for kw in keywords):
            past_qs.append(q)

print(f"Total Appraiser conceptual framework questions: {len(past_qs)}")
for idx, q in enumerate(past_qs[:10]):
    print(f"[{idx+1}] ID: {q.get('id')}, Year: {q.get('year')}, Number: {q.get('number')}")
    print(f"Question: {q.get('question')[:200]}")
    print("-" * 50)
