# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNK_PATH = ROOT / "viewer" / "public" / "data" / "exams" / "01.json"

if not CHUNK_PATH.exists():
    print(f"Error: {CHUNK_PATH} does not exist.")
    exit(1)

with open(CHUNK_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Total questions in 01.json: {len(questions)}")

# Search for questions with ch06s02
target_questions = [q for q in questions if q.get("id", "").startswith("practice-accounting-ch06s02-")]

print(f"Found {len(target_questions)} questions with prefix 'practice-accounting-ch06s02-' in 01.json.")

if len(target_questions) == 50:
    print("Verification PASSED: Synced chunk 01.json has all 50 questions!")
else:
    print(f"Verification FAILED: Expected 50 questions, found {len(target_questions)}")
    exit(1)
