import os
import json
import fitz
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def restore_q60_2020_vision():
    pdf_path = "sources/기출문제/세무사/2020/2교시 A형(선택과목 민법).pdf"
    doc = fitz.open(pdf_path)
    
    # Q60 is usually on page 10-15. Let's find it.
    target_page = None
    for page in doc:
        if page.search_for("60."):
            target_page = page
            break
    
    if not target_page:
        print("Could not find Q60 in PDF.")
        return

    pix = target_page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
    img_data = pix.tobytes("png")
    
    client = genai.Client(api_key=gemini_api_key)
    
    prompt = """
이 이미지는 2020년 세무사 1차 민법 시험지입니다.
60번 문제의 본문 영역을 찾아주세요.

1. 문제 본문 바운딩 박스 [ymin, xmin, ymax, xmax] (0~1000 scale)
   - ymin: '60.' 번호 바로 위
   - ymax: 첫 번째 선지 ①번 바로 위 (선지는 이미지에 포함되지 않게!)
   - xmin/xmax: 0, 1000 (가로 전체)

2. 선지 ①~⑤의 텍스트와 정답, 해설을 추출해 주세요.

반드시 아래 JSON 형식으로만 응답하세요:
{
  "bbox": [ymin, 0, ymax, 1000],
  "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
  "answer": "숫자",
  "explanation": "상세 해설",
  "tags": { "unit": "...", "concept": "..." }
}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[types.Part.from_bytes(data=img_data, mime_type="image/png"), prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        res = json.loads(response.text)
        
        # Crop and save image
        ymin, xmin, ymax, xmax = res['bbox']
        pw, ph = target_page.rect.width, target_page.rect.height
        crop_rect = fitz.Rect(xmin*pw/1000, ymin*ph/1000, xmax*pw/1000, ymax*ph/1000)
        
        pix_q = target_page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(3.0, 3.0))
        img_filename = "tax_2020_s2_60_body.png"
        pix_q.save(f"images/{img_filename}")
        
        # Add to DB
        db_path = "questions_db.json"
        with open(db_path, "r", encoding="utf-8") as f:
            db = json.load(f)
            
        q_data = {
            "id": "tax_2020_민법_60",
            "exam": "세무사",
            "year": "2020",
            "subject": "민법",
            "number": "60",
            "question": f"[IMAGE: {img_filename}]",
            "options": res['options'],
            "answer": str(res['answer']),
            "explanation": res['explanation'],
            "tags": res.get("tags", {"subject": "민법", "difficulty": 3})
        }
        db.append(q_data)
        
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print("Restored 2020 Civil Law Q60 successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    restore_q60_2020_vision()
