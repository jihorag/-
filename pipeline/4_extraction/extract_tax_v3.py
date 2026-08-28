import base64
import requests
import json
import os
import fitz
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def find_boxes_on_page(page):
    drawings = page.get_drawings()
    # Find horizontal lines. Columns are approx from x=74 to x=542
    h_lines = []
    for d in drawings:
        r = d['rect']
        if r.width > 300 and r.height < 2:
            h_lines.append(r)
    
    h_lines.sort(key=lambda x: x.y0)
    
    boxes = []
    i = 0
    while i < len(h_lines) - 1:
        y_top = h_lines[i].y0
        found = False
        # Look for the CLOSEST line below within a reasonable height (e.g., 250px)
        for j in range(i + 1, len(h_lines)):
            height = h_lines[j].y0 - y_top
            if 20 < height < 250: # Standard box height range
                bbox = fitz.Rect(h_lines[i].x0, y_top, h_lines[i].x1, h_lines[j].y0)
                boxes.append(bbox)
                i = j 
                found = True
                break
            elif height >= 250: # Too far, not a box
                break
        if not found:
            i += 1
    return boxes

def extract_questions_from_page(pix_b64, page_num):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    prompt = """
당신은 시험 문제 추출 전문가입니다. 첨부된 이미지에서 문제들을 추출하여 JSON 객체로 응답하십시오.
반드시 'results'라는 키를 가진 배열 안에 각 문제 정보를 담으십시오.
각 문제 객체는 number, question, options (5개), answer, explanation, has_box (지문 박스 유무) 필드를 포함해야 합니다.
박스 유무는 지문에 'ㄱ, ㄴ, ㄷ...' 보기가 들어있는 경우 true로 하십시오.
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
    
    for page_num in range(11): # Up to page 11 for Q40
        page = doc[page_num]
        print(f"Processing page {page_num + 1}...")
        
        # Crop boxes
        boxes = find_boxes_on_page(page)
        saved_boxes = []
        for i, bbox in enumerate(boxes):
            pix_box = page.get_pixmap(clip=bbox + (-2,-2,2,2), matrix=fitz.Matrix(3,3))
            box_filename = f"box_p{page_num+1}_{i+1}.png"
            pix_box.save(os.path.join(output_dir, box_filename))
            saved_boxes.append(box_filename)
        
        # Get text
        pix_page = page.get_pixmap(matrix=fitz.Matrix(2,2))
        pix_b64 = encode_image(pix_page)
        result = extract_questions_from_page(pix_b64, page_num + 1)
        
        if result and 'choices' in result:
            data = json.loads(result['choices'][0]['message']['content'])
            questions = data.get('results', [])
            
            box_idx = 0
            for q in questions:
                if q.get('has_box') and box_idx < len(saved_boxes):
                    q['box_image'] = f"images/tax_2026/{saved_boxes[box_idx]}"
                    box_idx += 1
                
                if q.get('number') <= 40:
                    all_questions.append(q)
                    print(f"Added Q{q.get('number')}")
            
            # Save incrementally after each page so USER can see live progress
            with open("viewer/src/data/questions_tax.json", "w", encoding="utf-8") as f:
                json.dump({"results": all_questions}, f, ensure_ascii=False, indent=2)
        
        time.sleep(1)
        
    with open("viewer/src/data/questions_tax.json", "w", encoding="utf-8") as f:
        json.dump({"results": all_questions}, f, ensure_ascii=False, indent=2)
    print(f"Finished! Total {len(all_questions)} questions.")

if __name__ == "__main__":
    main()
