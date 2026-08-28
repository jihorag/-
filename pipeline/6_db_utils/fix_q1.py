import base64
import json
import os
import fitz
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

pdf_path = "sources/기출문제/세무사/2026/2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf"
year = "2026"
session = 2
subject = "회계학"

with open("taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy_data = json.load(f)
subject_taxonomy = taxonomy_data.get(subject, "목차 없음")

doc = fitz.open(pdf_path)
page = doc[0] # Page 1
pix_page = page.get_pixmap(matrix=fitz.Matrix(3,3))
pix_b64 = encode_image(pix_page)

prompt = f"""
첨부된 이미지에는 여러 개의 '{subject}' 객관식 기출문제가 있습니다. 
각 문제에 대해 아래 JSON 형식으로 데이터를 추출하십시오.
특별 지시사항 (Spatial Bounding Box):
- 각 문제의 본문 영역을 bbox 필드에 [ymin, xmin, ymax, xmax] 형식으로 반환. (0~1000)
- bbox 영역에는 절대로 ①~⑤ 선지가 포함되어서는 안 됩니다.
[과목: {subject} 의 목차]
{json.dumps(subject_taxonomy, ensure_ascii=False)}
{{
  "results": [
    {{ "number": 1, "bbox": [150, 50, 400, 950], "options": ["①", "②", "③", "④", "⑤"], "answer": "1", "explanation": "", "tags": {{}} }}
  ]
}}
"""

client = genai.Client(api_key=gemini_api_key)
response = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=[prompt, types.Part.from_bytes(data=base64.b64decode(pix_b64), mime_type="image/png")],
    config=types.GenerateContentConfig(response_mime_type="application/json", thinking_config={"thinking_level": "HIGH"})
)

json_str = response.text.replace('\\', '\\\\')
res = json.loads(json_str)

results = res if isinstance(res, list) else res.get('results', [])

for item in results:
    if item.get('number') == 1:
        ymin, xmin, ymax, xmax = item.get('bbox')
        y_top = (ymin / 1000.0) * page.rect.height
        y_bottom = (ymax / 1000.0) * page.rect.height
        y_top = max(0, y_top - 5)
        y_bottom = min(page.rect.height, y_bottom + 5)
        
        crop_rect = fitz.Rect(0, y_top, page.rect.width, y_bottom)
        pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
        filename = f"tax_{year}_s{session}_1_body.png"
        pix_q.save(os.path.join("images", filename))
        
        q_data = {
            "year": year,
            "subject": subject,
            "number": "1",
            "question": f"[IMAGE: {filename}]",
            "options": item.get('options', []),
            "answer": str(item.get('answer', "")),
            "explanation": item.get('explanation', ""),
            "tags": item.get('tags', {}),
            "exam": "세무사",
            "id": f"tax_{year}_{subject}_1"
        }
        
        with open("questions_db.json", "r", encoding="utf-8") as f:
            main_db = json.load(f)
            
        found = False
        for i, q in enumerate(main_db):
            if q.get("id") == q_data["id"]:
                main_db[i] = q_data
                found = True
                break
        if not found:
            main_db.append(q_data)
            
        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
            
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
            
        print("Q1 fixed and injected into main db!")
