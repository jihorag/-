import os
import json
import fitz
import unicodedata
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def nfd(text):
    return unicodedata.normalize('NFD', text)

def restore_final_one():
    year, subject, q_num = "2018", "회계학개론", 22
    print(f">> Final Restoration: {year} {subject} Q{q_num}...")
    
    # Use normalized paths
    base_dir = nfd("기출문제/세무사/2018")
    target_file = None
    if os.path.exists(base_dir):
        for f in os.listdir(base_dir):
            if nfd("2교시") in nfd(f) and f.endswith(".pdf"):
                target_file = os.path.join(base_dir, f)
                break
            
    if not target_file:
        print("   [!] File not found even with normalization.")
        return
    
    print(f"   [+] Opening: {target_file}")
    doc = fitz.open(target_file)
    target_page = doc[8] # Page 9

    pix = target_page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
    img_data = pix.tobytes("png")
    
    client = genai.Client(api_key=gemini_api_key)
    prompt = f"""
이 이미지는 2018년 세무사 1차 회계학개론 시험지입니다.
22번 문제의 본문 영역을 찾아주세요.

1. 문제 본문 바운딩 박스 [ymin, xmin, ymax, xmax] (0~1000 scale)
   - ymin: '22.' 번호 바로 위
   - ymax: 첫 번째 선지 ①번 바로 위
   - xmin/xmax: 0, 1000

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
        pw, ph = target_page.rect.width, target_page.rect.height
        crop_rect = fitz.Rect(xmin*pw/1000, ymin*ph/1000, xmax*pw/1000, ymax*ph/1000)
        
        pix_q = target_page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(3.0, 3.0))
        img_filename = f"tax_2018_s2_22_body.png"
        pix_q.save(f"images/{img_filename}")
        
        db_path = "questions_db.json"
        with open(db_path, "r", encoding="utf-8") as f:
            db = json.load(f)
            
        q_data = {
            "id": f"tax_2018_회계학개론_22",
            "exam": "세무사",
            "year": "2018",
            "subject": "회계학개론",
            "number": "22",
            "question": f"[IMAGE: {img_filename}]",
            "options": res['options'],
            "answer": str(res['answer']),
            "explanation": res['explanation'],
            "tags": res.get("tags", {"subject": "회계학개론", "difficulty": 3})
        }
        db.append(q_data)
        
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print("   [+] All restoration 100% complete!")
        
    except Exception as e:
        print(f"   [Error] {e}")

if __name__ == "__main__":
    restore_final_one()
