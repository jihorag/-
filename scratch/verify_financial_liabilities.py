# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

if not DB_PATH.exists():
    print(f"Error: {DB_PATH} does not exist.")
    exit(1)

with open(DB_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Total questions in database: {len(questions)}")

# Verify range 2001 to 2050 (index 2000 to 2049)
target_range = range(2000, 2050)
target_questions = []
for i in target_range:
    if i < len(questions):
        target_questions.append(questions[i])

print(f"Loaded {len(target_questions)} questions from target range (2001~2050).")

errors = []
diff_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

for idx, q in enumerate(target_questions):
    q_num = 2001 + idx
    
    # 1. ID check
    q_id = q.get("id", "")
    if not q_id.startswith("practice-accounting-ch08s01-"):
        errors.append(f"Q{q_num}: Invalid ID prefix: '{q_id}'")
        
    # 2. Taxonomy check
    tax = q.get("indexing_v4", {}).get("mapped_taxonomy", {})
    expected_tax = {
        "subject": "회계학",
        "sub_subject": "재무회계",
        "chapter": "제3장 부채",
        "section": "Chapter 08 금융부채",
        "item": "1절 금융부채의 인식과 측정"
    }
    for k, v in expected_tax.items():
        if tax.get(k) != v:
            errors.append(f"Q{q_num}: Taxonomy mismatch for '{k}'. Expected '{v}', got '{tax.get(k)}'")
            
    # 3. Difficulty check
    diff = q.get("indexing_v4", {}).get("difficulty")
    if diff not in diff_counts:
        errors.append(f"Q{q_num}: Invalid difficulty '{diff}'")
    else:
        diff_counts[diff] += 1
        
    # 4. Answer check
    answer = q.get("answer", "")
    if answer not in ["1", "2", "3", "4", "5"]:
        errors.append(f"Q{q_num}: Invalid answer: '{answer}'")
        
    # 5. Options check
    options = q.get("options", [])
    if len(options) != 5:
        errors.append(f"Q{q_num}: Option count is {len(options)}, expected 5")
    else:
        circs = ["①", "②", "③", "④", "⑤"]
        for opt_idx, opt in enumerate(options):
            if not opt.strip().startswith(circs[opt_idx]):
                errors.append(f"Q{q_num}: Option {opt_idx+1} does not start with '{circs[opt_idx]}' (Text: '{opt}')")
                
    # 6. Option meta check
    meta = q.get("option_meta", [])
    if len(meta) != 5:
        errors.append(f"Q{q_num}: option_meta count is {len(meta)}, expected 5")
    else:
        correct_indices = [str(i+1) for i, m in enumerate(meta) if m.get("correct") is True]
        if len(correct_indices) != 1:
            errors.append(f"Q{q_num}: Expected exactly one correct option in option_meta, got {correct_indices}")
        elif correct_indices[0] != answer:
            errors.append(f"Q{q_num}: option_meta correct index '{correct_indices[0]}' does not match answer '{answer}'")
            
        # Verify explanation text has [오답 해설]
        explanation = q.get("explanation", "")
        if "[오답 해설]" not in explanation:
            errors.append(f"Q{q_num}: Explanation lacks '[오답 해설]'")
            
    # 7. Metadata check
    processed_by = q.get("indexing_v4", {}).get("processed_by", "")
    if processed_by != "claude-sonnet-4-6":
        errors.append(f"Q{q_num}: Invalid processed_by: '{processed_by}'")
    in_scope = q.get("indexing_v4", {}).get("in_scope")
    if in_scope is not True:
        errors.append(f"Q{q_num}: Invalid in_scope: '{in_scope}'")
    if q.get("exam") != "[연습문제]":
        errors.append(f"Q{q_num}: Invalid exam field: '{q.get('exam')}'")
    if q.get("subject") != "회계학":
        errors.append(f"Q{q_num}: Invalid subject field: '{q.get('subject')}'")
    if q.get("source") != "practice":
        errors.append(f"Q{q_num}: Invalid source field: '{q.get('source')}'")
    if q.get("question_type") != "개념5지":
        errors.append(f"Q{q_num}: Invalid question_type: '{q.get('question_type')}'")

print("\n--- Difficulty Distribution Check ---")
expected_diffs = {1: 10, 2: 15, 3: 15, 4: 8, 5: 2}
for d in sorted(expected_diffs.keys()):
    print(f"L{d}: Got {diff_counts[d]} (Expected {expected_diffs[d]})")
    if diff_counts[d] != expected_diffs[d]:
        errors.append(f"Difficulty L{d} count mismatch: got {diff_counts[d]}, expected {expected_diffs[d]}")

if len(target_questions) != 50:
    errors.append(f"Total questions count in target range is {len(target_questions)}, expected 50")

if errors:
    print(f"\nVerification FAILED with {len(errors)} errors:")
    for err in errors[:20]:
        print(f"- {err}")
    if len(errors) > 20:
        print(f"... and {len(errors) - 20} more errors")
    exit(1)
else:
    print("\nVerification PASSED successfully!")
