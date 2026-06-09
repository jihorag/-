# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

if not DB_PATH.exists():
    print(f"Error: {DB_PATH} not found.")
    exit(1)

with open(DB_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded database with {len(questions)} questions.")

# We want to fix questions from index 1250 to 1399 (Q1251 ~ Q1400)
# These belong to:
# - Q1251~1300: 1절 무형자산의 정의 및 인식과 측정
# - Q1301~1350: 2절 무형자산의 상각
# - Q1351~1400: 3절 무형자산의 제거와 손상

# We will group questions by item (section/item) to calculate their difficulty sequence number.
# Difficulty sequence counters: we can count difficulty occurrences per section.
# Let's map each index to a section number (1, 2, or 3)
# Q1251 (index 1250) to Q1300 (index 1299): Section 1
# Q1301 (index 1300) to Q1350 (index 1349): Section 2
# Q1351 (index 1350) to Q1400 (index 1399): Section 3

counters = {
    1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    2: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
}

for i in range(1250, 1400):
    if i >= len(questions):
        print(f"Warning: Index {i} is out of bounds (length={len(questions)}).")
        continue
        
    q = questions[i]
    
    # Determine section
    if 1250 <= i < 1300:
        sec = 1
    elif 1300 <= i < 1350:
        sec = 2
    else:
        sec = 3
        
    # Get difficulty
    difficulty = q.get("indexing_v4", {}).get("difficulty", 1)
    counters[sec][difficulty] += 1
    seq = counters[sec][difficulty]
    
    # Update metadata
    q["exam"] = "[연습문제]"
    q["subject"] = "회계학"
    q["source"] = "practice"
    q["number"] = f"L{difficulty}-{seq:02d}"
    q["year"] = ""
    q["question_type"] = "개념5지"
    
    # Update indexing_v4
    if "indexing_v4" not in q:
        q["indexing_v4"] = {}
    q["indexing_v4"]["processed_by"] = "claude-sonnet-4-6"
    q["indexing_v4"]["in_scope"] = True

# Write back to DB
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Metadata fix completed successfully for Q1251~1400!")
