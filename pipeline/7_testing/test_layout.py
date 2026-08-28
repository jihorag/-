import fitz
doc = fitz.open("2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf")
for i in range(15):
    page = doc[i]
    blocks = page.get_text("dict")["blocks"]
    has_left = False
    has_right = False
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                x = l['bbox'][0]
                if x < 280: has_left = True
                if x > 310: has_right = True
    print(f"Page {i+1}: left={has_left}, right={has_right}")
