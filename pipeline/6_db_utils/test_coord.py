import fitz

doc = fitz.open("sources/기출문제/세무사/2021/2021년도 제58회 세무사 1차 시험 1교시 A형.pdf")
page = doc[0] # page 1
for q_num in range(1, 5):
    rects = page.search_for(f"{q_num}.")
    rects_1 = page.search_for("①")
    print(f"Q{q_num}: {rects}")
    print(f"  Option 1: {rects_1}")
