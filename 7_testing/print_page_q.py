import fitz
doc = fitz.open("2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf")
for page_num in [9, 11]: # Page 10, Page 12
    page = doc[page_num]
    print(f"--- PAGE {page_num+1} ---")
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                txt = "".join(s["text"] for s in l["spans"]).strip()
                if txt:
                    print(f"X={l['bbox'][0]:.1f}, Y={l['bbox'][1]:.1f}: {txt}")
