import json
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
QDB = ROOT / "questions_db.json"

with open(QDB, "r", encoding="utf-8") as f:
    db = json.load(f)

print(f"Total questions in database: {len(db)}")

# Filter Appraisal (감정평가사) Civil Law (민법) Jisang (지상권) questions
jisang_questions = []
for q in db:
    # Check if exam is appraisal and subject is civil law
    exam = q.get("exam", "")
    if "감정평가사" not in exam:
        continue
    
    # Check taxonomy mapping in indexing_v4
    idx = q.get("indexing_v4", {})
    if not idx:
        continue
    tax = idx.get("mapped_taxonomy", {})
    if not tax:
        continue
    
    subj = tax.get("subject", "")
    if subj != "민법":
        continue
        
    chap = tax.get("chapter", "")
    sec = tax.get("section", "")
    item = tax.get("item", "")
    
    # Check if it falls under 용익물권 -> 지상권
    # We should also handle case-insensitive or mapping details
    is_jisang = False
    if "용익물권" in chap and "지상권" in sec:
        is_jisang = True
    elif "지상권" in chap or "지상권" in sec:
        is_jisang = True
        
    if is_jisang:
        jisang_questions.append({
            "id": q.get("id"),
            "year": q.get("year"),
            "number": q.get("number"),
            "question": q.get("question"),
            "options": q.get("options"),
            "answer": q.get("answer"),
            "explanation": q.get("explanation"),
            "item": item
        })

print(f"Total Jisang (지상권) questions found for Appraisal Exam: {len(jisang_questions)}")

# Let's count by year
years = Counter([q["year"] for q in jisang_questions])
print("\nYearly Distribution:")
for yr, cnt in sorted(years.items()):
    print(f"  {yr}년: {cnt}문제")

# Let's print unique items mapped
items = Counter([q["item"] for q in jisang_questions])
print("\nItem Mapped Distribution:")
for it, cnt in sorted(items.items()):
    print(f"  {it or 'None'}: {cnt}문제")

# Let's list some representative questions (e.g. up to 5)
print("\nRepresentative Questions:")
for i, q in enumerate(jisang_questions[:5]):
    print(f"\n[{i+1}] {q['year']}년 {q['number']}번 (ID: {q['id']}, Item: {q['item']})")
    print(f"Q: {q['question']}")
    print("Options:")
    for opt_idx, opt in enumerate(q["options"]):
        print(f"  ({opt_idx+1}) {opt}")
    print(f"A: {q['answer']}")
    print(f"Explanation snippet: {q['explanation'][:150]}...")
