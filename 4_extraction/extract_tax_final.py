import base64
import requests
import json
import os
import fitz
from dotenv import load_dotenv
import time
import re

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_via_gpt4o(pix_b64):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    prompt = """
첨부된 세무사 시험지에서 각 문제의 '선지(①~⑤)', '정답', '해설'을 추출하십시오.
반드시 'results' 배열에 담아 JSON으로 응답하십시오.
각 선지 앞에는 반드시 ①, ②, ③, ④, ⑤ 기호를 포함하십시오. 
예: ["① 직접세는...", "② 간접세는...", ...]
"""
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{pix_b64}"}}
                ]
            }
        ],
        "max_tokens": 4000,
        "response_format": { "type": "json_object" }
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()
    except:
        return None

def main():
    pdf_path = "2026년도 제63회 세무사 1차시험 1교시 시험지 원본.pdf"
    doc = fitz.open(pdf_path)
    output_dir = "viewer/public/images/tax_2026"
    os.makedirs(output_dir, exist_ok=True)
    
    final_results = []
    
    # Process only up to Q40 (Subject 1: Public Finance)
    # Usually around page 1-12
    for page_num in range(13): 
        page = doc[page_num]
        print(f"\n--- Scanning Page {page_num + 1} ---")
        
        text_items = []
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        txt = s["text"].strip()
                        if txt: text_items.append({"text": txt, "bbox": s["bbox"]})
        
        text_items.sort(key=lambda x: x["bbox"][1])
        q_headers = [i for i in text_items if re.match(r"^\d+\.?$", i["text"]) and i["bbox"][0] < 100]
        opts_starts = [i for i in text_items if "①" in i["text"]]
        
        # 1. Crop Images First
        page_crops = {}
        for idx, q in enumerate(q_headers):
            try:
                q_num = int(re.sub(r"\D", "", q["text"]))
                if q_num > 40: continue # STOP AT 40
            except: continue
            
            y0 = q["bbox"][1] - 12
            my_opt = next((o for o in opts_starts if o["bbox"][1] > y0), None)
            y1 = my_opt["bbox"][1] - 4 if my_opt else (q_headers[idx+1]["bbox"][1]-15 if idx+1 < len(q_headers) else page.rect.height-70)
            
            if y1 - y0 < 15: continue
            
            pix = page.get_pixmap(clip=fitz.Rect(0, y0, page.rect.width, y1), matrix=fitz.Matrix(2.5, 2.5))
            img_path = f"images/tax_2026/q{q_num}_body.png"
            pix.save(os.path.join("viewer/public", img_path))
            page_crops[q_num] = img_path
            print(f"Cropped Q{q_num}")

        # 2. Get Text via GPT
        if not page_crops: continue
        
        pix_page = page.get_pixmap(matrix=fitz.Matrix(2,2))
        res = extract_via_gpt4o(encode_image(pix_page))
        
        if res and 'choices' in res:
            try:
                data = json.loads(res['choices'][0]['message']['content'])
                for g in data.get('results', []):
                    try:
                        g_num = int(re.sub(r"\D", "", str(g.get('number', ''))))
                        if g_num in page_crops:
                            q_data = {
                                "number": g_num,
                                "question": f"[IMAGE: {page_crops[g_num]}]",
                                "options": g.get('options', []),
                                "answer": g.get('answer', ""),
                                "explanation": g.get('explanation', ""),
                                "is_premium": True
                            }
                            # Check if already added
                            if not any(x['number'] == g_num for x in final_results):
                                final_results.append(q_data)
                                print(f"Successfully integrated Q{g_num}")
                    except: continue
            except: pass

        # Save incrementally
        with open("viewer/src/data/questions_tax.json", "w", encoding="utf-8") as f:
            json.dump({"results": sorted(final_results, key=lambda x: x['number'])}, f, ensure_ascii=False, indent=2)
            
    print(f"\nDone! Total {len(final_results)} questions integrated.")

if __name__ == "__main__":
    main()
