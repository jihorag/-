import os
import json

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
PRACTICE_DIR = os.path.join(ROOT, "viewer/public/data/practice/realestate")

files = sorted([f for f in os.listdir(PRACTICE_DIR) if f.endswith(".json")])

non_mcq_files = []
total_questions = 0
non_mcq_count = 0

for file in files:
    path = os.path.join(PRACTICE_DIR, file)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        questions = data.get("questions", [])
        total_questions += len(questions)
        
        file_non_mcq = 0
        for q in questions:
            opts = q.get("options", [])
            if not opts or not isinstance(opts, list) or len(opts) != 5:
                file_non_mcq += 1
                non_mcq_count += 1
        
        if file_non_mcq > 0:
            non_mcq_files.append((file, file_non_mcq, len(questions)))
    except Exception as e:
        print(f"Error reading {file}: {e}")

print(f"Total Questions Analyzed: {total_questions}")
print(f"Total Non-MCQ Questions (options count != 5): {non_mcq_count}")
print(f"Files containing non-MCQ questions: {len(non_mcq_files)}")
for name, non_cnt, total_cnt in non_mcq_files:
    print(f"- {name}: {non_cnt} / {total_cnt} questions are non-MCQ")
