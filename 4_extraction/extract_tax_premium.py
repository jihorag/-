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

def extract_premium_from_page(pix_b64, page_num):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    prompt = """
당신은 시험 문제 추출 전문가입니다. 첨부된 이미지에서 문제들을 추출하십시오.
각 문제에 대해:
1. 문제 번호 식별
2. '문제 본문(선지 제외)' 영역의 y_top, y_bottom 좌표 (0~1000 상대값)
3. 선지 5개 텍스트 추출

JSON 응답 형식:
{
  "results": [
    {
      "number": 1, 
      "y_top": 120, 
      "y_bottom": 450, 
      "options": ["①", "②", "③", "④", "⑤"], 
      "answer": "정답번호(1~5)", 
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
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None

def main():
    pdf_path = "2026년도 제63회 세무사 1차시험 1교시 시험지 원본.pdf"
    doc = fitz.open(pdf_path)
    output_dir = "viewer/public/images/tax_2026"
    os.makedirs(output_dir, exist_ok=True)
    
    all_questions = []
    
    for page_num in range(11): 
        page = doc[page_num]
        print(f"Processing page {page_num + 1}...")
        
        pix_page = page.get_pixmap(matrix=fitz.Matrix(2,2))
        pix_b64 = encode_image(pix_page)
        
        result = extract_premium_from_page(pix_b64, page_num + 1)
        
        if result and 'choices' in result:
            content = result['choices'][0]['message']['content']
            try:
                data = json.loads(content)
            except:
                print("JSON Decode Error")
                continue
                
            questions = data.get('results', [])
            
            page_height = page.rect.height
            page_width = page.rect.width
            
            for q in questions:
                num = q.get('number')
                if not num: continue
                
                y_start = (q.get('y_top', 0) / 1000) * page_height
                y_end = (q.get('y_bottom', 500) / 1000) * page_height
                
                # Crop with a bit of padding
                crop_rect = fitz.Rect(0, max(0, y_start - 5), page_width, min(page_height, y_end + 5))
                pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2,2))
                
                q_img_filename = f"q{num}_body.png"
                pix_q.save(os.path.join(output_dir, q_img_filename))
                
                new_q = {
                    "number": num,
                    "question": f"[IMAGE: images/tax_2026/{q_img_filename}]",
                    "options": q.get('options', []),
                    "answer": q.get('answer', ""),
                    "explanation": q.get('explanation', ""),
                    "is_premium": True
                }
                
                if num <= 40:
                    all_questions.append(new_q)
                    print(f"Extracted Premium Q{num}")
            
            # Save incrementally
            with open("viewer/src/data/questions_tax.json", "w", encoding="utf-8") as f:
                json.dump({"results": all_questions}, f, ensure_ascii=False, indent=2)
        
        time.sleep(1)

if __name__ == "__main__":
    main()
