import json

with open("questions_db.json", encoding="utf-8") as f:
    db = json.load(f)

# Filter for Appraiser Accounting questions related to Inventory (재고자산)
inventory_qs = []
for q in db:
    subj = q.get("subject", "")
    exam = q.get("exam", "")
    question = q.get("question", "")
    
    # Check if the subject is Accounting and exam is Appraiser (감정평가사)
    # And look for inventory keywords
    if "회계" in subj and "감정평가사" in exam:
        # Check if the question is about inventory
        # Keywords: 재고자산, 매입원가, 취득원가, 선적지, 도착지, 시송품, 적송품, 감모, 저가, 평가손실 등
        keywords = ["재고자산", "매입원가", "취득원가", "선적지", "도착지", "시송품", "적송품", "감모", "저가", "평가손실", "평가충당금"]
        if any(kw in question or kw in q.get("explanation", "") for kw in keywords):
            inventory_qs.append(q)

print(f"Total Appraiser inventory questions found: {len(inventory_qs)}")
for idx, q in enumerate(inventory_qs[:10]):
    print(f"[{idx+1}] ID: {q.get('id')}, Year: {q.get('year')}, Number: {q.get('number')}")
    print(f"Question: {q.get('question')[:200]}")
    print(f"Answer: {q.get('answer')}")
    print("-" * 50)
