# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

with open(DB_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

# 1. Fix Q1318 (index 1317)
# Q1318 ID is practice-accounting-ch05s02-L2-08 (actually index 1317)
q1318 = questions[1317]
print("Fixing Q1318:", q1318["id"])
q1318["option_meta"] = [
    {"correct": True},
    {"correct": False},
    {"correct": False},
    {"correct": False},
    {"correct": False}
]

# 2. Fix Q1342 (index 1341)
# Q1342 ID is practice-accounting-ch05s02-L4-02 (actually index 1341)
q1342 = questions[1341]
print("Fixing Q1342:", q1342["id"])
# Original options had:
# 0: ① 자산 ₩300,000 과소계상, 당기순이익 ₩300,000 과소계상
# 1: **자산 ₩300,000 과소계상, 당기순이익 ₩300,000 과소계상**
# 2: ② 자산 ₩300,000 과대계상, 당기순이익 ₩300,000 과대계상 ...
print("Original options count:", len(q1342["options"]))
q1342["options"] = [
    "① 자산 ₩300,000 과소계상, 당기순이익 ₩300,000 과소계상",
    "② 자산 ₩300,000 과대계상, 당기순이익 ₩300,000 과대계상",
    "③ 자산 ₩100,000 과소계상, 당기순이익 ₩100,000 과소계상",
    "④ 자산 ₩400,000 과소계상, 당기순이익 ₩400,000 과소계상",
    "⑤ 자산 ₩200,000 과대계상, 당기순이익 ₩200,000 과대계상"
]
print("New options count:", len(q1342["options"]))

# Save changes
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Saved changes successfully.")
