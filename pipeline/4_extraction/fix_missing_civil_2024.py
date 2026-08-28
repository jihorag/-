import base64
import json
import os
import fitz
import time
import unicodedata
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def normalize_nfc(text):
    return unicodedata.normalize('NFC', text)

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_spatial_via_gemini(pix_b64, subject_taxonomy, subject, min_q, max_q):
    prompt = f"""
첨부된 이미지는 세무사 1차 시험 '{subject}' 과목의 시험지입니다. 
이미지에 포함된 {min_q}번 ~ {max_q}번 사이의 문제를 JSON으로 추출하세요.
(현재 누락된 {min_q}번부터 {max_q}번까지를 찾는 것이 최우선 목표입니다.)

[필수 요구사항]
1. bbox: 문제 본문 영역 [ymin, xmin, ymax, xmax] (0~1000). 가로폭은 0~1000 전체를 커버하세요.
2. 내용: 정답, 상세 해설, 목차 태깅 필수. 

{{
  "results": [
    {{
      "number": {min_q},
      "bbox": [100, 0, 250, 1000],
      "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
      "answer": "3",
      "explanation": "...",
      "tags": {{ "unit": "...", "sub_unit": "...", "concept": "..." }}
    }}
  ]
}}
"""
    try:
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.1-pro-preview", 
            contents=[prompt, types.Part.from_bytes(data=base64.b64decode(pix_b64), mime_type="image/png")],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        json_text = response.text.replace('\\', '\\\\')
        return json.loads(json_text)
    except Exception as e:
        print(f"[GEMINI API Error] {e}")
        return None

def main():
    task = {"pdf": "sources/기출문제/세무사/2024/2024년도 제61회 세무사 1차시험 2교시 시험지 원본(민법).pdf", "year": "2024", "session": 2, "subject": "민법", "min_q": 59, "max_q": 80}
    with open("taxonomy.json", "r", encoding="utf-8") as f: taxonomy_data = json.load(f)
    with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    
    doc = fitz.open(task['pdf'])
    # 59번이 있을 것으로 예상되는 23페이지(index 22)부터 끝까지 스캔
    for page_num in range(22, len(doc)):
        page = doc[page_num]
        print(f">> Scanning Page {page_num+1} for missing questions (59~80)...")
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        pix_b64 = encode_image(pix)
        
        res = extract_spatial_via_gemini(pix_b64, taxonomy_data.get(task['subject'], {}), task['subject'], task['min_q'], task['max_q'])
        results = res if isinstance(res, list) else res.get('results', []) if res else []
        
        print(f"   Found {len(results)} items.")
        for item in results:
            q_num = int(item.get('number', 0))
            if q_num < task['min_q'] or q_num > task['max_q']: continue
            
            bbox = item.get('bbox')
            if not bbox: continue
            
            # 가로 꽉 찬 크롭 적용
            y_top = max(0, (bbox[0] / 1000.0) * page.rect.height - 12)
            y_bottom = min(page.rect.height, (bbox[2] / 1000.0) * page.rect.height + 12)
            crop_rect = fitz.Rect(0, y_top, page.rect.width, y_bottom)
            
            pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
            filename = f"tax_2024_s2_{q_num}_body.png"
            pix_q.save(f"images/{filename}")
            
            q_id = f"tax_2024_{normalize_nfc(task['subject'])}_{q_num}"
            q_data = {
                "year": "2024", "subject": normalize_nfc(task['subject']), "number": str(q_num), "question": f"[IMAGE: {filename}]",
                "options": item.get('options', []), "answer": str(item.get('answer', "")),
                "explanation": item.get('explanation', ""), "tags": item.get('tags', {}),
                "exam": "세무사", "id": q_id
            }
            
            # Upsert
            found = False
            for i, db_q in enumerate(main_db):
                if normalize_nfc(db_q.get("id", "")) == normalize_nfc(q_id):
                    main_db[i] = q_data
                    found = True; break
            if not found: main_db.append(q_data)
            print(f"   -> Saved Q{q_num}")

        # 실시간 저장
        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
