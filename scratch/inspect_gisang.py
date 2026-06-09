# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path('/Users/hanjiho/Documents/감정평가사 기출문제')
QDB = ROOT / 'questions_db.json'

with open(QDB, encoding='utf-8') as f:
    db = json.load(f)

print(f"Total questions in DB: {len(db)}")

# Filter appraisal questions related to 지상권
gisang_qs = []
for q in db:
    # Check if subject is 민법
    if q.get('subject') != '민법':
        continue
    # Exclude practice questions
    if q.get('period') == 'practice' or q.get('exam') == '[연습문제]':
        continue
    
    # Let's inspect taxonomy v4 mapping
    tax_v4 = q.get('indexing_v4')
    tax = (tax_v4.get('mapped_taxonomy') or {}) if tax_v4 else {}
    chapter = tax.get('chapter', '')
    section = tax.get('section', '')
    item = tax.get('item', '')
    
    # We target 지상권 (제1절 지상권 또는 지상권 키워드 포함)
    is_gisang = False
    if '지상권' in chapter or '지상권' in section or '지상권' in item:
        is_gisang = True
    elif '지상권' in q.get('question', ''):
        is_gisang = True
        
    # Exclude 법정지상권, 관습법상 법정지상권, 구분지상권, 분묘기지권 if we only want general 지상권 (제1관~제4관)
    # However, let's look at all of them first to see the distribution.
    if is_gisang:
        gisang_qs.append(q)

print(f"Total Jisang-related questions found: {len(gisang_qs)}")

# Group by item or section to see the distribution
distribution = {}
for q in gisang_qs:
    tax = q.get('indexing_v4', {}).get('mapped_taxonomy', {})
    item_name = tax.get('item', 'Unclassified')
    if not item_name:
        item_name = tax.get('section', 'Unclassified Section')
    distribution[item_name] = distribution.get(item_name, 0) + 1

print("\n--- Distribution of Jisang Questions ---")
for item_name, count in sorted(distribution.items()):
    print(f"- {item_name}: {count} questions")

# Let's print out the general Jisang questions (Item 01 ~ 04)
# to understand their core concepts, choices and answers.
print("\n--- Details of General Jisang Questions (Item 01 ~ 04) ---")
idx = 1
for q in gisang_qs:
    tax = q.get('indexing_v4', {}).get('mapped_taxonomy', {})
    item_name = tax.get('item', '')
    # Check if it belongs to Item 05 ~ 08
    if any(k in item_name for k in ['구분지상권', '분묘기지권', '법정지상권', '관습법상', '관습상']):
        print(f"\n[{idx}] Exam: {q.get('exam')} | Year: {q.get('year')} | Item: {item_name}")
        print(f"Question: {q.get('question')[:200]}...")
        print("Options:")
        for o_idx, opt in enumerate(q.get('options', [])):
            print(f"  {o_idx+1}. {opt}")
        print(f"Answer: {q.get('answer')}")
        print(f"Explanation (brief): {q.get('explanation')[:300]}...")
        idx += 1
