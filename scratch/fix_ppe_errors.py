# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

with open(DB_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

# 1. Fix Q1215 (index 1214)
q1215 = questions[1214]
q1215["indexing_v4"]["mapped_taxonomy"]["item"] = "6절 차입원가 자본화의 순서"
print("Fixed Q1215 taxonomy item.")

# 2. Fix Q1235 (index 1234)
q1235 = questions[1234]
q1235["answer"] = "2"

# Update explanation to start with ② and update [오답 해설]
old_exp = q1235["explanation"]
new_exp = old_exp.replace("③ 완공된 특정차입금이", "② 완공된 특정차입금이")

# Add explanation for ③ in [오답 해설]
if "[오답 해설]" in new_exp:
    parts = new_exp.split("[오답 해설]")
    incorrect_exps = parts[1].strip()
    
    # We want to insert explanation for ③.
    # Let's place it between ① and ④.
    # The original incorrect_exps contains:
    # ① 7~12월 기간 적수 비율을 다르게 곱한 오류입니다.
    # ④ 실제 일반이자 한도 검토를 누락하고 단순 계산액 전체(₩240,000)를 취해 규정을 어긴 오답입니다.
    # ⑤ 일반차입 전환을 무시하고 자본화액을 ₩0으로 처리한 오류 선지입니다.
    
    ins_text = "③ 특정차입금의 일반차입금 귀속 변경이나 이자율 자본화 한도를 잘못 적용한 오류 선지입니다.\n"
    updated_incorrect = incorrect_exps.replace("① 7~12월 기간 적수 비율을 다르게 곱한 오류입니다.\n", "① 7~12월 기간 적수 비율을 다르게 곱한 오류입니다.\n" + ins_text)
    
    # If the replace didn't match exactly because of newlines, let's try a simpler replace
    if ins_text not in updated_incorrect:
        updated_incorrect = incorrect_exps.replace("① 7~12월 기간 적수 비율을 다르게 곱한 오류입니다.", "① 7~12월 기간 적수 비율을 다르게 곱한 오류입니다.\n" + ins_text)
        
    new_exp = parts[0] + "[오답 해설]\n" + updated_incorrect

q1235["explanation"] = new_exp
print("Fixed Q1235 answer and explanation.")

# Save back to database
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Saved changes to database.")
