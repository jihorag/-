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

def extract_via_gpt55(pix_b64):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    prompt = """첨부된 세무사 시험지에서 각 문제의 '선지(①~⑤) 전체 텍스트', '정답', '해설'을 추출하십시오. 
지문 박스(ㄱ,ㄴ,ㄷ...) 내용은 제외하고 하단의 ①~⑤ 선택지만 추출하십시오.
JSON 형식: {results:[{number, options:[①...], answer, explanation}]}"""
    
    payload = {
        "model": "gpt-5.5", 
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{pix_b64}"}}
                ]
            }
        ],
        "max_completion_tokens": 4000, # Updated for GPT-5.5
        "response_format": { "type": "json_object" }
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return None
    return response.json()

def main():
    pdf_path = "2026년도 제63회 세무사 1차시험 1교시 시험지 원본.pdf"
    doc = fitz.open(pdf_path)
    json_path = "viewer/src/data/questions_tax.json"
    output_dir = "viewer/public/images/tax_2026"
    
    all_questions = []

    for page_num in range(13): 
        print(f"\n--- Processing Page {page_num + 1} with GPT-5.5 ---")
        page = doc[page_num]
        
        text_items = []
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        txt = s["text"].strip()
                        if txt: text_items.append({"text": txt, "bbox": s["bbox"]})
        
        text_items.sort(key=lambda x: x["bbox"][1])
        q_headers = [i for i in text_items if re.match(r"^\d+\.?$", i["text"]) and i["bbox"][0] < 150]
        q_headers.sort(key=lambda x: x["bbox"][1])
        
        opts_starts = [i for i in text_items if "①" in i["text"]]
        
        page_crops = []
        for idx, q in enumerate(q_headers):
            try:
                q_num = int(re.sub(r"\D", "", q["text"]))
                if q_num > 40: continue
                y0 = q["bbox"][1] - 12
                my_opt = next((o for o in opts_starts if o["bbox"][1] > y0), None)
                y1 = my_opt["bbox"][1] - 4 if my_opt else (q_headers[idx+1]["bbox"][1]-15 if idx+1 < len(q_headers) else page.rect.height-70)
                
                pix = page.get_pixmap(clip=fitz.Rect(0, y0, page.rect.width, y1), matrix=fitz.Matrix(2.5, 2.5))
                img_path = f"images/tax_2026/q{q_num}_body.png"
                pix.save(os.path.join("viewer/public", img_path))
                page_crops.append({"number": q_num, "img": img_path})
            except: continue

        if not page_crops: continue

        res = extract_via_gpt55(encode_image(page.get_pixmap(matrix=fitz.Matrix(2,2))))
        
        if res and 'choices' in res:
            try:
                data = json.loads(res['choices'][0]['message']['content'])
                gpt_results = data.get('results', [])
                
                for i, crop in enumerate(page_crops):
                    match = None
                    for g in gpt_results:
                        g_num_str = re.sub(r"\D", "", str(g.get('number', '')))
                        if g_num_str and int(g_num_str) == crop['number']:
                            match = g
                            break
                    
                    if not match and len(gpt_results) == len(page_crops):
                        match = gpt_results[i]

                    if match:
                        all_questions.append({
                            "number": crop['number'],
                            "question": f"[IMAGE: {crop['img']}]",
                            "options": match.get('options', []),
                            "answer": match.get('answer', ""),
                            "explanation": match.get('explanation', ""),
                            "is_premium": True
                        })
                        print(f"Added Q{crop['number']} (GPT-5.5)")
            except Exception as e:
                print(f"Error on Page {page_num+1}: {e}")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"results": sorted(all_questions, key=lambda x: x['number'])}, f, ensure_ascii=False, indent=2)
        
        time.sleep(1)

    print("Task Completed with GPT-5.5.")

if __name__ == "__main__":
    main()
