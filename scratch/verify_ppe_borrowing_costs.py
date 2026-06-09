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

# Verify range 1151 to 1200 (index 1150 to 1199)
target_range = range(1150, 1200)
target_questions = [questions[i] for i in target_range if i < len(questions)]

print(f"Loaded {len(target_questions)} questions from target range (1151~1200).")

errors = []
diff_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

for idx, q in enumerate(target_questions):
    q_num = 1151 + idx
    
    # 1. ID check
    q_id = q.get("id", "")
    if not q_id.startswith("practice-accounting-ch04s05-"):
        errors.append(f"Q{q_num}: Invalid ID prefix: '{q_id}'")
        
    # 2. Taxonomy check
    tax = q.get("indexing_v4", {}).get("mapped_taxonomy", {})
    expected_tax = {
        "subject": "회계학",
        "sub_subject": "재무회계",
        "chapter": "제2장 자산",
        "section": "Chapter 04 유형자산",
        "item": "5절 차입원가 자본화"
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

print("\n--- Difficulty Distribution Check ---")
expected_diffs = {1: 10, 2: 15, 3: 15, 4: 8, 5: 2}
for d in sorted(expected_diffs.keys()):
    print(f"L{d}: Got {diff_counts[d]} (Expected {expected_diffs[d]})")
    if diff_counts[d] != expected_diffs[d]:
        errors.append(f"Difficulty L{d} count mismatch: got {diff_counts[d]}, expected {expected_diffs[d]}")

if errors:
    print(f"\nVerification FAILED with {len(errors)} errors:")
    for err in errors[:20]:
        print(f"- {err}")
    if len(errors) > 20:
        print(f"... and {len(errors) - 20} more errors")
    exit(1)
else:
    print("\nVerification PASSED successfully!")
