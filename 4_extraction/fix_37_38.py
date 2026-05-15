import base64
import json
import os
import fitz
import unicodedata
import glob
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_37_38(pix_b64, taxonomy_data):
    prompt = f"""
이미지에서 37번과 38번 문제를 추출하세요.
복잡한 표가 포함되어 있으니 정확하게 분석하십시오.

[필수 요구사항]
1. bbox: [ymin, xmin, ymax, xmax] (0~1000). 선지 ①~⑤는 제외하고 본문+표까지만.
2. 내용: 정답(숫자), 상세 해설, 분류 태그(단원: 원가관리회계 등)
3. 37번과 38번 각각 별도의 객체로 반환.

결과 JSON:
{{
  "results": [
    {{
      "number": 37,
      "bbox": [50, 50, 450, 950],
      "options": ["① ₩66.25", "② ₩75.50", "③ ₩77.50", "④ ₩80.25", "⑤ ₩85.50"],
      "answer": "...",
      "explanation": "...",
      "tags": {{ "unit": "원가관리회계", "sub_unit": "...", "concept": "..." }}
    }}
  ]
}}
"""
    client = genai.Client(api_key=gemini_api_key)
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview", 
        contents=[prompt, types.Part.from_bytes(data=base64.b64decode(pix_b64), mime_type="image/png")],
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    return json.loads(response.text)

def main():
    try:
        with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    except: main_db = []

    path = glob.glob("기출문제/세무사/2022/2022*민법*.pdf")[0]
    doc = fitz.open(path)
    page = doc[16] # p17
    
    print(">> Extracting 2022 Q37, Q38...")
    pix = page.get_pixmap(matrix=fitz.Matrix(3.0, 3.0))
    res = extract_37_38(encode_image(pix), {})
    
    if res and 'results' in res:
        for item in res['results']:
            q_num = item.get('number')
            if q_num not in [37, 38]: continue
            
            bbox = item.get('bbox')
            y_top = (bbox[0] / 1000.0) * page.rect.height
            y_bottom = (bbox[2] / 1000.0) * page.rect.height
            
            crop_rect = fitz.Rect(0, y_top - 10, page.rect.width, y_bottom + 10)
            pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
            img_name = f"tax_2022_s2_{q_num}_body.png"
            pix_q.save(os.path.join("images", img_name))
            
            q_id = f"tax_2022_회계학개론_{q_num}"
            q_data = {
                "year": "2022", "subject": "회계학개론", "number": str(q_num),
                "question": f"[IMAGE: {img_name}]", "options": item.get('options', []),
                "answer": str(item.get('answer', "")), "explanation": item.get('explanation', ""),
                "tags": item.get('tags', {}), "exam": "세무사", "id": q_id
            }
            
            # Upsert
            found = False
            for i, db_q in enumerate(main_db):
                if db_q.get("id") == q_id:
                    main_db[i] = q_data
                    found = True; break
            if not found: main_db.append(q_data)
            print(f"   -> Recovered Q{q_num}")

    with open("questions_db.json", "w", encoding="utf-8") as f:
        json.dump(main_db, f, ensure_ascii=False, indent=2)
    with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
        json.dump(main_db, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
