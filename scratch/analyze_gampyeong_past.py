# -*- coding: utf-8 -*-
import json
import os

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
QDB = os.path.join(ROOT, "questions_db.json")

with open(QDB, "r", encoding="utf-8") as f:
    db = json.load(f)

# Filters:
# Subject is "민법" or contains "민법"
# Exam is "감정평가사" (or similar)
# Not a practice question (not is_practice)
# Mapped taxonomy contains "공동소유", "합유", "총유", "명의신탁" 
# or the question text contains these keywords.

topics = {
    "합유": [],
    "총유": [],
    "준공동소유": [],
    "명의신탁": []
}

print(f"Total questions in database: {len(db)}")

for q in db:
    # Check if it is a past exam question
    is_practice = q.get("tags", {}).get("is_practice", False)
    if is_practice:
        continue
        
    subject = q.get("subject", "")
    if "민법" not in subject:
        continue
        
    exam = q.get("exam", "")
    if "감정평가사" not in exam:
        continue

    # Extract taxonomy details
    tax = {}
    if "indexing_v4" in q and q["indexing_v4"] and "mapped_taxonomy" in q["indexing_v4"]["mapped_taxonomy"]:
        tax = q["indexing_v4"]["mapped_taxonomy"]
    
    chapter = tax.get("chapter", "")
    section = tax.get("section", "")
    item = tax.get("item", "")
    
    path_str = f"{chapter} > {section} > {item}"
    q_text = q.get("question", "")
    
    # Identify topic
    matched = False
    for keyword in topics.keys():
        if keyword in path_str or keyword in q_text:
            topics[keyword].append({
                "id": q.get("id"),
                "year": q.get("year"),
                "number": q.get("number"),
                "question": q_text[:120].replace("\n", " ") + "...",
                "answer": q.get("answer"),
                "options": q.get("options", [])
            })
            matched = True

for topic, qlist in topics.items():
    print(f"\n=========================================\nTOPIC: {topic} ({len(qlist)} questions found)\n=========================================")
    # Sort by year desc
    qlist.sort(key=lambda x: str(x.get("year")), reverse=True)
    for qitem in qlist:
        print(f"\n[{qitem['year']} 감평 Q{qitem['number']}] (ID: {qitem['id']}, Answer: {qitem['answer']})")
        print(f"  Q: {qitem['question']}")
        for idx, opt in enumerate(qitem['options']):
            print(f"    ({idx+1}) {opt}")

