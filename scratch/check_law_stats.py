import json
import os
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
PRACTICE_DIR = ROOT / "viewer" / "public" / "data" / "practice" / "law"

def check_files():
    if not PRACTICE_DIR.exists():
        print(f"Error: practice directory {PRACTICE_DIR} does not exist.")
        return
        
    json_files = list(PRACTICE_DIR.glob("*.json"))
    print(f"Found {len(json_files)} practice files.")
    
    total_questions = 0
    total_difficulty = 0.0
    total_exp_len = 0.0
    errors = []
    
    for fp in sorted(json_files):
        with open(fp, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                errors.append(f"JSON load error in {fp.name}: {e}")
                continue
                
            questions = data.get("questions", [])
            if len(questions) != 50:
                errors.append(f"Question count mismatch in {fp.name}: expected 50, got {len(questions)}")
                
            file_diff = 0.0
            file_exp_len = 0.0
            
            for idx, q in enumerate(questions):
                qid = q.get("id")
                diff = q.get("difficulty")
                opts = q.get("options")
                ans = q.get("answer")
                exp = q.get("explanation", "")
                
                # Check options
                if not opts or not isinstance(opts, list) or len(opts) != 5:
                    errors.append(f"{fp.name} (Q{idx+1}): invalid options count: {opts}")
                else:
                    # check symbols
                    for o in opts:
                        if not any(o.startswith(sym) for sym in ["①", "②", "③", "④", "⑤"]):
                            errors.append(f"{fp.name} (Q{idx+1}): option missing standard symbol: {o}")
                            
                # Check answer
                if not ans or str(ans) not in ["1", "2", "3", "4", "5"]:
                    errors.append(f"{fp.name} (Q{idx+1}): invalid answer index: {ans}")
                    
                # Check difficulty
                if not diff or not (1 <= diff <= 5):
                    errors.append(f"{fp.name} (Q{idx+1}): invalid difficulty: {diff}")
                else:
                    file_diff += diff
                    total_difficulty += diff
                    
                # Check explanation
                exp_len = len(exp)
                file_exp_len += exp_len
                total_exp_len += exp_len
                if exp_len < 1000:
                    errors.append(f"{fp.name} (Q{idx+1}): explanation length too short: {exp_len} chars")
                    
            total_questions += len(questions)
            avg_diff = file_diff / len(questions) if questions else 0.0
            avg_exp = file_exp_len / len(questions) if questions else 0.0
            
            # Print warning if a file average is low
            if avg_diff < 4.0:
                print(f"Warning: {fp.name} has low average difficulty ({avg_diff:.2f})")
            if avg_exp < 1000:
                print(f"Warning: {fp.name} has low average explanation length ({avg_exp:.2f})")
                
    if total_questions > 0:
        overall_avg_diff = total_difficulty / total_questions
        overall_avg_exp = total_exp_len / total_questions
        print("\n--- Summary ---")
        print(f"Total Questions Verified: {total_questions}")
        print(f"Overall Average Difficulty: {overall_avg_diff:.4f} (Target >= 4.0)")
        print(f"Overall Average Explanation Length: {overall_avg_exp:.2f} chars (Target > 1000)")
    else:
        print("No questions found to verify.")
        
    if errors:
        print(f"\n❌ Validation failed with {len(errors)} errors:")
        for err in errors[:20]:
            print(f"  - {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors.")
    else:
        print("\n✅ All validation checks passed successfully!")

if __name__ == "__main__":
    check_files()
