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
이미지에 포함된 {min_q}번 ~ {max_q}번 사이의 모든 문제를 JSON으로 추출하세요.

[필수 요구사항]
1. bbox: 문제 본문 영역 [ymin, xmin, ymax, xmax] (0~1000). 
   - 1단 구성이므로 가로폭은 0~1000 전체를 포함하세요.
   - 문제 번호부터 끝 문장까지만 포함 (선지 제외).
2. 내용: 정답(숫자), 상세 해설, 분류 태그 필수. 

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
        # 3.1 Pro 대신 할당량이 넉넉한 2.5 Pro 사용
        response = client.models.generate_content(
            model="gemini-2.5-pro", 
            contents=[prompt, types.Part.from_bytes(data=base64.b64decode(pix_b64), mime_type="image/png")],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        json_text = response.text.replace('\\', '\\\\')
        res = json.loads(json_text)
        return res if isinstance(res, list) else res.get('results', [])
    except Exception as e:
        print(f"[GEMINI API Error] {e}")
        return None

def process_task(task, taxonomy_data, main_db):
    pdf_path = task['pdf']
    year = task['year']
    session = task['session']
    subject = normalize_nfc(task['subject'])
    min_q, max_q = task['min_q'], task['max_q']
    
    print(f"\n>> {year}년 {session}교시 - {subject} 시작 (Gemini 2.5 Pro 전량 추출 모드)")
    doc = fitz.open(pdf_path)
    output_dir = "images"
    subject_taxonomy = taxonomy_data.get(subject, "목차 없음")
    
    for page_num in range(17, len(doc)):
        page = doc[page_num]
        print(f"  Processing Page {page_num+1}/{len(doc)}...")
        
        pix_page = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        pix_b64 = encode_image(pix_page)
        
        results = extract_spatial_via_gemini(pix_b64, subject_taxonomy, subject, min_q, max_q)
        if results:
            for item in results:
                try: q_num = int(item.get('number'))
                except: continue
                if q_num < min_q or q_num > max_q: continue
                
                bbox = item.get('bbox')
                if not bbox: continue
                
                # 좌표 보정 (번호 잘림 방지를 위해 상단 마진을 35px로 대폭 확대)
                y_top = max(0, (bbox[0] / 1000.0) * page.rect.height - 35)
                y_bottom = min(page.rect.height, (bbox[2] / 1000.0) * page.rect.height + 15)
                x_left = 0
                x_right = page.rect.width
                
                crop_rect = fitz.Rect(x_left, y_top, x_right, y_bottom)
                filename = f"tax_{year}_s{session}_{q_num}_body.png"
                pix_q.save(os.path.join(output_dir, filename))
                
                q_id = f"tax_{year}_{subject}_{q_num}"
                q_data = {
                    "year": year, "subject": subject, "number": str(q_num), "question": f"[IMAGE: {filename}]",
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
                print(f"    -> Gemini Extracted Q{q_num}")

        # 실시간 저장
        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
            
    return main_db

def main():
    task = {"pdf": "기출문제/세무사/2024/2024년도 제61회 세무사 1차시험 2교시 시험지 원본(민법).pdf", "year": "2024", "session": 2, "subject": "민법", "min_q": 41, "max_q": 80}
    with open("taxonomy.json", "r", encoding="utf-8") as f: taxonomy_data = json.load(f)
    try:
        with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    except: main_db = []
    process_task(task, taxonomy_data, main_db)
    print("\n🎉 2024년도 민법 Gemini 전량 복구 완료!")

if __name__ == "__main__":
    main()
