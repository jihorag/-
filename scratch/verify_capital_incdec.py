# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

with open(DB_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

# Section 4 questions are index 2600 to 2650 (1-based Q2601 to Q2650)
sec4_questions = questions[2600:2650]

print(f"Total questions in database: {len(questions)}")
print(f"Loaded {len(sec4_questions)} questions for Section 4 verification.")

errors = []
difficulty_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
table_count = 0

for i, q in enumerate(sec4_questions):
    q_num = 2601 + i
    q_id = q.get("id", "")
    
    # 1. ID Prefix
    expected_id = f"practice-accounting-ch10s04-L{q.get('indexing_v4', {}).get('difficulty', 1)}-{i+1:02d}"
    # Wait, we can just check if it starts with the prefix or matches the expected format
    if not q_id.startswith("practice-accounting-ch10s04-"):
        errors.append(f"Q{q_num}: ID '{q_id}' does not start with 'practice-accounting-ch10s04-'")
        
    # 2. Options check
    options = q.get("options", [])
    if len(options) != 5:
        errors.append(f"Q{q_num}: Must have exactly 5 options, got {len(options)}")
    else:
        prefixes = ["①", "②", "③", "④", "⑤"]
        for opt_idx, opt in enumerate(options):
            if not opt.strip().startswith(prefixes[opt_idx]):
                errors.append(f"Q{q_num}: Option {opt_idx+1} '{opt}' does not start with '{prefixes[opt_idx]}'")
                
    # 3. Answer check
    answer = q.get("answer", "")
    if answer not in ["1", "2", "3", "4", "5"]:
        errors.append(f"Q{q_num}: Invalid answer '{answer}'")
        
    # 4. Option Meta check
    option_meta = q.get("option_meta", [])
    if len(option_meta) != 5:
        errors.append(f"Q{q_num}: option_meta length must be 5, got {len(option_meta)}")
    else:
        try:
            ans_idx = int(answer) - 1
            for idx, meta in enumerate(option_meta):
                is_correct = meta.get("correct")
                if idx == ans_idx:
                    if not is_correct:
                        errors.append(f"Q{q_num}: option_meta does not match answer. Index {idx} should be True.")
                else:
                    if is_correct:
                        errors.append(f"Q{q_num}: option_meta does not match answer. Index {idx} should be False.")
        except ValueError:
            pass
            
    # 5. Explanation check
    explanation = q.get("explanation", "")
    if "[오답 해설]" not in explanation:
        errors.append(f"Q{q_num}: Explanation lacks '[오답 해설]' marker")
        
    # 6. Metadata check
    indexing = q.get("indexing_v4", {})
    if not indexing:
        errors.append(f"Q{q_num}: Missing 'indexing_v4'")
    else:
        difficulty = indexing.get("difficulty")
        if difficulty not in [1, 2, 3, 4, 5]:
            errors.append(f"Q{q_num}: Invalid difficulty {difficulty}")
        else:
            difficulty_counts[difficulty] += 1
            
        taxonomy = indexing.get("mapped_taxonomy", {})
        expected_taxonomy = {
            "subject": "회계학",
            "sub_subject": "재무회계",
            "chapter": "제4장 자본",
            "section": "Chapter 10 자본",
            "item": "4절 증자와 감자"
        }
        for k, v in expected_taxonomy.items():
            if taxonomy.get(k) != v:
                errors.append(f"Q{q_num}: Taxonomy mismatch for {k}: expected '{v}', got '{taxonomy.get(k)}'")
                
        if indexing.get("processed_by") != "claude-sonnet-4-6":
            errors.append(f"Q{q_num}: processed_by should be 'claude-sonnet-4-6', got '{indexing.get('processed_by')}'")
            
        if indexing.get("in_scope") is not True:
            errors.append(f"Q{q_num}: in_scope should be True")
            
    # 7. Table check
    question_text = q.get("question", "")
    if "|" in question_text and "---" in question_text:
        table_count += 1

print("\n--- Summary ---")
print(f"Difficulty distribution: {difficulty_counts}")
print(f"Questions containing tables: {table_count}")

expected_distribution = {1: 10, 2: 15, 3: 15, 4: 8, 5: 2}
for diff, count in expected_distribution.items():
    if difficulty_counts[diff] != count:
        errors.append(f"Difficulty {diff} mismatch: expected {count}, got {difficulty_counts[diff]}")

if table_count < 10:
    errors.append(f"Table count mismatch: expected at least 10, got {table_count}")

if errors:
    print(f"\nFound {len(errors)} errors:")
    for err in errors:
        print(f"- {err}")
    exit(1)
else:
    print("\nAll checks passed successfully!")
    exit(0)
