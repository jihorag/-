import os
import json

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
PRACTICE_DIR = os.path.join(ROOT, "viewer/public/data/practice/realestate")

files = sorted([f for f in os.listdir(PRACTICE_DIR) if f.endswith(".json")])

ox_questions = []
for file in files:
    path = os.path.join(PRACTICE_DIR, file)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        questions = data.get("questions", [])
        for q in questions:
            opts = q.get("options", [])
            # Check if any options are purely "O" or "X" or contain O/X pattern
            is_ox = False
            for opt in opts:
                cleaned = opt.replace("①", "").replace("②", "").replace("③", "").replace("④", "").replace("⑤", "").strip()
                if cleaned in ["O", "X", "정답", "오답"]:
                    is_ox = True
            # Also check if options have placeholders like "-", "", "N/A"
            placeholder_count = sum(1 for opt in opts if opt.strip() in ["①", "②", "③", "④", "⑤", "① -", "② -", "③ -", "④ -", "⑤ -"])
            if is_ox or placeholder_count > 0:
                ox_questions.append((file, q.get("id"), opts))
    except Exception as e:
        print(f"Error reading {file}: {e}")

print(f"Total potential OX or placeholder questions: {len(ox_questions)}")
for fn, qid, opts in ox_questions[:20]:
    print(f"- File: {fn}\n  QID: {qid}\n  Opts: {opts}")
if len(ox_questions) > 20:
    print("... (truncated)")
