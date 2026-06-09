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

if len(questions) > 2700:
    questions = questions[:2700]
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"Truncated database to {len(questions)} questions.")
else:
    print("No truncation needed, database is already 2700 or fewer questions.")
