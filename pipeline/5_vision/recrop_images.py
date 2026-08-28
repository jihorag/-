import fitz
import re
import os

pdf_path = "2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf"
doc = fitz.open(pdf_path)

target_nums = {1, 2, 3, 4, 5, 20, 23, 24}
saved_nums = set()

for page_num in range(len(doc)):
    if target_nums == saved_nums:
        break

    page = doc[page_num]

    # Full width crop for all
    clip_x0 = 0
    clip_x1 = page.rect.width

    # Collect text
    text_items = []
    for b in page.get_text("dict")["blocks"]:
        if "lines" in b:
            for l in b["lines"]:
                for s in l["spans"]:
                    txt = s["text"].strip()
                    if txt: text_items.append({"text": txt, "bbox": s["bbox"]})

    text_items.sort(key=lambda x: x["bbox"][1])
    
    q_headers = []
    for i in text_items:
        if re.match(r"^\d+\.?$", i["text"]) and i["bbox"][0] < clip_x0 + 60:
            q_headers.append(i)
            
    q_headers.sort(key=lambda x: x["bbox"][1])
    opts_starts = [i for i in text_items if "①" in i["text"]]
    
    for idx, q in enumerate(q_headers):
        q_num = int(re.sub(r"\D", "", q["text"]))
        if q_num not in target_nums or q_num in saved_nums:
            continue
            
        # For Q1, make sure to include the instructions at the very top of the page
        if q_num == 1:
            y0 = 40  # Start higher up to include common instructions
        else:
            y0 = q["bbox"][1] - 12
            
        my_opt = next((o for o in opts_starts if o["bbox"][1] > y0), None)
        
        if my_opt:
            y1 = my_opt["bbox"][1] - 4
        else:
            if idx + 1 < len(q_headers):
                y1 = q_headers[idx+1]["bbox"][1] - 15
            else:
                y1 = page.rect.height - 70
                
        if y1 <= y0:
            y1 = y0 + 50
            
        rect = fitz.Rect(clip_x0, y0, clip_x1, y1)
        pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(2.5, 2.5))
        
        img_path = f"viewer/public/images/tax_2026/q_s2_{q_num}_body.png"
        pix.save(img_path)
        print(f"Recropped and saved {img_path} (Page {page_num+1})")
        saved_nums.add(q_num)

print("Finished recropping.")
