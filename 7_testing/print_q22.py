import fitz
import re

doc = fitz.open("2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf")
for page_num in range(len(doc)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]
    has_q22 = False
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                txt = "".join(s["text"] for s in l["spans"]).strip()
                if txt.startswith("22."):
                    has_q22 = True
    if has_q22:
        print(f"Q22 is on Page {page_num+1}")
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    txt = "".join(s["text"] for s in l["spans"]).strip()
                    if txt:
                        print(f"X={l['bbox'][0]:.1f}, Y={l['bbox'][1]:.1f}: {txt}")
