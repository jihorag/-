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

def extract_questions_from_page(pix_b64, page_num):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    prompt = f"""
당신은 시험 문제 추출 전문가입니다. 첨부된 시험지 이미지(재정학)에서 문제들을 추출하여 JSON 객체로 응답하십시오.
반드시 'results'라는 키를 가진 배열 안에 각 문제 정보를 담으십시오.

각 문제 객체는 다음 필드를 포함해야 합니다:
- number: 문제 번호 (정수, 1~40 사이)
- question: 문제 내용 (텍스트)
- options: 5개의 보기 리스트 (텍스트, '① ㄱ, ㄴ' 형태 유지)
- answer: 정답 (가답안이 없다면 문맥과 재정학 지식을 바탕으로 가장 적절한 번호(1~5) 추론)
- explanation: 간단한 해설 (재정학 이론 바탕)
- has_box: 문제 지문 중 'ㄱ, ㄴ, ㄷ, ㄹ' 등의 보기가 들어있는 네모 박스가 있다면 true, 없다면 false

반드시 JSON 형태로만 응답하십시오.
"""
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{pix_b64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4000,
        "response_format": { "type": "json_object" }
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error on page {page_num}:", response.text)
        return None

def find_boxes_on_page(page):
    drawings = page.get_drawings()
    h_lines = [d['rect'] for d in drawings if d['rect'].width > 400 and d['rect'].height < 1]
    h_lines.sort(key=lambda x: x.y0)
    
    boxes = []
    for i in range(0, len(h_lines) - 1, 2):
        y_top = h_lines[i].y0
        y_bottom = h_lines[i+1].y0
        if y_bottom - y_top > 20: 
            bbox = fitz.Rect(h_lines[i].x0, y_top, h_lines[i].x1, y_bottom)
            boxes.append(bbox)
    return boxes

def main():
    pdf_path = "2026년도 제63회 세무사 1차시험 1교시 시험지 원본.pdf"
    doc = fitz.open(pdf_path)
    output_dir = "viewer/public/images/tax_2026"
    os.makedirs(output_dir, exist_ok=True)
    
    all_questions = []
    
    # 1st Period PDF: Pages 1-8 usually cover Q1-40 (Public Finance)
    for page_num in range(9): # Pages 0 to 8
        page = doc[page_num]
        print(f"Processing page {page_num + 1}...")
        
        # 1. Extract and save boxes
        boxes = find_boxes_on_page(page)
        saved_boxes = []
        for i, bbox in enumerate(boxes):
            pix_box = page.get_pixmap(clip=bbox + (-2,-2,2,2), matrix=fitz.Matrix(3,3))
            box_filename = f"tax_2026_p{page_num+1}_box_{i+1}.png"
            pix_box.save(os.path.join(output_dir, box_filename))
            saved_boxes.append(box_filename)
        
        # 2. Extract text via GPT Vision
        pix_page = page.get_pixmap(matrix=fitz.Matrix(2,2))
        pix_b64 = encode_image(pix_page)
        result = extract_questions_from_page(pix_b64, page_num + 1)
        
        if result:
            content = result['choices'][0]['message']['content']
            data = json.loads(content)
            questions = data.get('results', [])
            
            # Map boxes to questions (simple heuristic: order of questions with has_box)
            box_idx = 0
            for q in questions:
                if q.get('has_box') and box_idx < len(saved_boxes):
                    q['box_image'] = f"images/tax_2026/{saved_boxes[box_idx]}"
                    box_idx += 1
                
                # Stop if we hit beyond Q40 (Tax law starts)
                if q.get('number', 0) > 40:
                    break
                
                all_questions.append(q)
                print(f"Extracted Q{q.get('number')}")
            
            # Break early if we've passed Q40
            if any(q.get('number', 0) >= 40 for q in questions):
                break
        
        time.sleep(2) # Rate limiting
        
    # Save to file
    with open("viewer/src/data/questions_tax.json", "w", encoding="utf-8") as f:
        json.dump({"results": all_questions}, f, ensure_ascii=False, indent=2)
    print("Done! Extracted", len(all_questions), "questions.")

if __name__ == "__main__":
    main()
