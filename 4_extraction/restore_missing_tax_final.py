import os
import json
import fitz
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def restore_specific_vision(year, subject, q_num, pdf_path, page_hint=None):
    print(f">> Restoring {year} {subject} Q{q_num}...")
    if not os.path.exists(pdf_path): return
        
    doc = fitz.open(pdf_path)
    target_page = doc[page_hint] if page_hint is not None else doc[0]

    pix = target_page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
    img_data = pix.tobytes("png")
    
    client = genai.Client(api_key=gemini_api_key)
    prompt = f"""
이 이미지는 {year}년 세무사 1차 {subject} 시험지입니다.
{q_num}번 문제의 본문 영역을 찾아주세요.

1. 문제 본문 바운딩 박스 [ymin, xmin, ymax, xmax] (0~1000 scale)
   - ymin: '{q_num}.' 번호 바로 위
   - ymax: 첫 번째 선지 ①번 바로 위 (선지는 이미지에 포함되지 않게!)
   - xmin/xmax: 0, 1000 (가로 전체)

2. 선지 ①~⑤의 텍스트와 정답, 해설을 추출해 주세요.

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "bbox": [ymin, 0, ymax, 1000],
  "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
  "answer": "숫자",
  "explanation": "상세 해설",
  "tags": {{ "unit": "...", "concept": "..." }}
}}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[types.Part.from_bytes(data=img_data, mime_type="image/png"), prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        res = json.loads(response.text)
        
        ymin, xmin, ymax, xmax = res['bbox']
        # Safety check
        if ymin >= ymax:
            print(f"   [!] Invalid bbox {res['bbox']}. Using default.")
            ymin, ymax = 100, 300 # Default fallback
            
        pw, ph = target_page.rect.width, target_page.rect.height
        crop_rect = fitz.Rect(xmin*pw/1000, ymin*ph/1000, xmax*pw/1000, ymax*ph/1000)
        
        pix_q = target_page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(3.0, 3.0))
        session = 1 if subject == "재정학" else 2
        img_filename = f"tax_{year}_s{session}_{q_num}_body.png"
        pix_q.save(f"images/{img_filename}")
        
        db_path = "questions_db.json"
        with open(db_path, "r", encoding="utf-8") as f:
            db = json.load(f)
            
        q_data = {
            "id": f"tax_{year}_{subject}_{q_num}",
            "exam": "세무사",
            "year": str(year),
            "subject": subject,
            "number": str(q_num),
            "question": f"[IMAGE: {img_filename}]",
            "options": res['options'],
            "answer": str(res['answer']),
            "explanation": res['explanation'],
            "tags": res.get("tags", {"subject": subject, "difficulty": 3})
        }
        db.append(q_data)
        
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print(f"   [+] Restored Q{q_num} successfully!")
        
    except Exception as e:
        print(f"   [Error] {e}")

if __name__ == "__main__":
    restore_specific_vision("2018", "재정학", 40, "기출문제/세무사/2018/2018 세무사 1차 1교시 A형.pdf", page_hint=10) # Try page 11 (index 10)
    restore_specific_vision("2018", "회계학개론", 22, "기출문제/세무사/2018/2018 세무사 1차 2교시 A형(민🇧ᅥᆸ).pdf", page_hint=6) # Try page 7 (index 6)
