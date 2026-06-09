# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

with open(DB_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

q1235 = questions[1234]
print("--- Q1235 Question Text ---")
print(q1235.get("question"))
print("\n--- Q1235 Explanation ---")
print(q1235.get("explanation"))
