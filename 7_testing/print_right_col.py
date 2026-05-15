import fitz
doc = fitz.open("2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf")
page = doc[10] # Page 11
blocks = page.get_text("dict")["blocks"]
for b in blocks:
    if "lines" in b:
        for l in b["lines"]:
            txt = "".join(s["text"] for s in l["spans"]).strip()
            if txt and l['bbox'][0] > 300 and l['bbox'][1] < 320:
                print(f"X={l['bbox'][0]:.1f}, Y={l['bbox'][1]:.1f}: {txt}")
