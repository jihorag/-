import fitz
doc = fitz.open("2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf")
for page_num in range(2): # Pages 1 and 2
    page = doc[page_num]
    print(f"--- PAGE {page_num+1} ---")
    blocks = page.get_text("dict")["blocks"]
    lines = []
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                txt = "".join(s["text"] for s in l["spans"]).strip()
                if txt:
                    lines.append((l["bbox"][1], txt))
    lines.sort(key=lambda x: x[0])
    for y, txt in lines:
        print(f"Y={y:.1f}: {txt}")
