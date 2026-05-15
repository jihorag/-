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

def get_text_blocks(page):
    """Extract text blocks with their bounding boxes."""
    blocks = page.get_text("dict")["blocks"]
    text_items = []
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                for s in l["spans"]:
                    text_items.append({
                        "text": s["text"].strip(),
                        "bbox": s["bbox"] # (x0, y0, x1, y1)
                    })
    return text_items

def extract_options_via_gpt(pix_b64, page_num):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    prompt = """
첨부된 이미지에서 각 문제의 '선지(①~⑤)'와 '정답', '해설'을 추출하십시오.
문제 본문은 이미 이미지로 따로 저장하고 있으므로, 오직 선지 텍스트 파싱에 집중하십시오.

결과는 반드시 'results' 키를 가진 JSON 배열로 응답하십시오:
{
  "results": [
    {
      "number": 1,
      "options": ["① 실제내용", "② 실제내용", "③ 실제내용", "④ 실제내용", "⑤ 실제내용"],
      "answer": "정답번호",
      "explanation": "해설"
    }
  ]
}
"""
    payload = {
        "model": "gpt-4o-mini",
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
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def main():
    pdf_path = "2026년도 제63회 세무사 1차시험 1교시 시험지 원본.pdf"
    doc = fitz.open(pdf_path)
    output_dir = "viewer/public/images/tax_2026"
    os.makedirs(output_dir, exist_ok=True)
    
    all_questions = []
    
    for page_num in range(11): 
        page = doc[page_num]
        print(f"Processing page {page_num + 1} with Ultra-Precision Strategy...")
        
        text_items = get_text_blocks(page)
        
        # Identify question headers (e.g., "1.", "2.") and option starters ("①")
        q_starts = []
        opt_starts = []
        
        for item in text_items:
            # Match "1.", "2." at start of block
            if re.match(r"^\d+\.", item["text"]):
                q_starts.append(item)
            # Match "①"
            if "①" in item["text"]:
                opt_starts.append(item)
        
        # Sort by Y coordinate
        q_starts.sort(key=lambda x: x["bbox"][1])
        opt_starts.sort(key=lambda x: x["bbox"][1])
        
        # Create crops
        page_width = page.rect.width
        
        page_results = []
        for q in q_starts:
            q_num = int(re.search(r"^\d+", q["text"]).group())
            if q_num > 40: continue
            
            y_top = q["bbox"][1] - 5 # Margin
            
            # Find the first option ① after this question number
            my_opt = next((o for o in opt_starts if o["bbox"][1] > y_top), None)
            
            if my_opt:
                y_bottom = my_opt["bbox"][1] - 2 # Just before the options
                
                # Determine column (Left or Right)
                # Middle of page is approx page_width / 2
                is_left = q["bbox"][0] < page_width / 2
                x0 = 0 if is_left else page_width / 2
                x1 = page_width / 2 if is_left else page_width
                
                crop_rect = fitz.Rect(x0, y_top, x1, y_bottom)
                pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2,2))
                
                filename = f"q{q_num}_body.png"
                pix_q.save(os.path.join(output_dir, filename))
                
                page_results.append({
                    "number": q_num,
                    "question_image": f"images/tax_2026/{filename}"
                })

        # Get Text from GPT for options/answers
        pix_page = page.get_pixmap(matrix=fitz.Matrix(2,2))
        pix_b64 = encode_image(pix_page)
        gpt_result = extract_options_via_gpt(pix_b64, page_num + 1)
        
        if gpt_result and 'choices' in gpt_result:
            content = gpt_result['choices'][0]['message']['content']
            data = json.loads(content)
            gpt_questions = data.get('results', [])
            
            # Merge 
            for pr in page_results:
                match = next((g for g in gpt_questions if g['number'] == pr['number']), None)
                if match:
                    new_q = {
                        "number": pr['number'],
                        "question": f"[IMAGE: {pr['question_image']}]",
                        "options": match.get('options', []),
                        "answer": match.get('answer', ""),
                        "explanation": match.get('explanation', ""),
                        "is_premium": True
                    }
                    all_questions.append(new_q)
                    print(f"Extracted Ultra-Premium Q{new_q['number']}")
            
            # Save
            with open("viewer/src/data/questions_tax.json", "w", encoding="utf-8") as f:
                json.dump({"results": all_questions}, f, ensure_ascii=False, indent=2)
                
        time.sleep(1)

if __name__ == "__main__":
    main()
