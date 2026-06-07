import os
import json

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
PRACTICE_DIR = os.path.join(ROOT, "viewer/public/data/practice/realestate")

files = sorted([f for f in os.listdir(PRACTICE_DIR) if f.endswith(".json")])
print(f"Total files found: {len(files)}")

stats = []
for file in files:
    path = os.path.join(PRACTICE_DIR, file)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        questions = data.get("questions", [])
        if not questions:
            stats.append((file, 0, 0.0, 0, 0))
            continue
        
        diffs = [q.get("difficulty", 0) for q in questions]
        avg_diff = sum(diffs) / len(diffs)
        # Check if the explanation is detailed (e.g. average length of explanation)
        avg_exp_len = sum(len(q.get("explanation", "")) for q in questions) / len(questions)
        stats.append((file, len(questions), avg_diff, avg_exp_len, max(diffs) if diffs else 0))
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Print files with average difficulty and explanation lengths
print(f"{'Filename':<80} | {'Count':<5} | {'Avg Diff':<8} | {'Avg Exp Len':<12}")
print("-" * 115)
for name, cnt, avg_d, avg_e, max_d in stats:
    # Print if average difficulty is high or normal
    status = "HIGH" if avg_d >= 3.8 and avg_e > 1000 else "LOW"
    print(f"{name[:80]:<80} | {cnt:<5} | {avg_d:<8.2f} | {avg_e:<12.1f} | {status}")
