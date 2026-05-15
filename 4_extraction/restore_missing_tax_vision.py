import os
import json
import fitz
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def extract_via_vision(page, q_num, subject, year):
    # Capture the whole page as image
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
    img_data = pix.tobytes("png")
    
    client = genai.Client(api_key=gemini_api_key)
    
    prompt = f"""
이 이미지는 {year}년 세무사 {subject} 시험지입니다.
{q_num}번 문제의 [문제 본문 영역]과 [선지 ①~⑤]를 찾아주세요.

1. 문제 본문 이미지를 크롭하기 위한 바운딩 박스 [ymin, xmin, ymax, xmax] (0~1000 scale)를 제공해 주세요.
2. 선지 ①~⑤의 텍스트를 추출해 주세요.
3. 정답과 해설을 제공해 주세요.

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "bbox": [ymin, xmin, ymax, xmax],
  "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
  "answer": "숫자",
  "explanation": "해설",
  "tags": {{ "unit": "...", "concept": "..." }}
}}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[
                types.Part.from_bytes(data=img_data, mime_type="image/png"),
                prompt
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error in Vision API: {e}")
        return None

def main():
    db_path = "questions_db.json"
    with open(db_path, "r", encoding="utf-8") as f:
        main_db = json.load(f)
        
    missing = [
        {"pdf": "기출문제/세무사/2014/2014년 재정학A형.pdf", "year": "2014", "q": 20, "sub": "재정학"},
        {"pdf": "기출문제/세무사/2014/2014년 재정학A형.pdf", "year": "2014", "q": 37, "sub": "재정학"},
        {"pdf": "기출문제/세무사/2014/2014년 회계학 A형.pdf", "year": "2014", "q": 27, "sub": "회계학개론"},
        {"pdf": "기출문제/세무사/2014/2014년 회계학 A형.pdf", "year": "2014", "q": 29, "sub": "회계학개론"},
        {"pdf": "기출문제/세무사/2015/2015년 세무사 1차 재정학 A형.pdf", "year": "2015", "q": 5, "sub": "재정학"},
        {"pdf": "기출문제/세무사/2015/2015년 세무사 1차 민법 A형.pdf", "year": "2015", "q": 44, "sub": "민법"},
    ]

    for item in missing:
        print(f"Restoring {item['year']} {item['sub']} Q{item['q']}...")
        doc = fitz.open(item['pdf'])
        # Find page with q_num
        target_page = None
        for page in doc:
            if page.search_for(f"{item['q']}."):
                target_page = page
                break
        
        if not target_page: target_page = doc[0] # Fallback
        
        res = extract_via_vision(target_page, item['q'], item['sub'], item['year'])
        if res and "bbox" in res:
            try:
                bbox = res['bbox']
                if isinstance(bbox[0], list): bbox = bbox[0]
                ymin, xmin, ymax, xmax = bbox
                
                page_width = target_page.rect.width
                page_height = target_page.rect.height
                
                crop_rect = fitz.Rect(
                    xmin * page_width / 1000,
                    ymin * page_height / 1000,
                    xmax * page_width / 1000,
                    ymax * page_height / 1000
                )
                
                pix = target_page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(3.0, 3.0))
                img_name = f"tax_{item['year']}_missing_{item['q']}.png"
                pix.save(f"images/{img_name}")
                
                q_data = {
                    "id": f"tax_{item['year']}_{item['sub']}_{item['q']}",
                    "exam": "세무사",
                    "year": str(item['year']),
                    "subject": item['sub'],
                    "number": str(item['q']),
                    "question": f"[IMAGE: {img_name}]",
                    "options": res['options'],
                    "answer": str(res['answer']),
                    "explanation": res['explanation'],
                    "tags": res.get("tags", {"subject": item['sub']})
                }
                main_db.append(q_data)
                
                with open(db_path, "w", encoding="utf-8") as f:
                    json.dump(main_db, f, ensure_ascii=False, indent=2)
                with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
                    json.dump(main_db, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Error parsing result for Q{item['q']}: {e}")
                
    print("Restore complete!")

if __name__ == "__main__":
    main()
