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
    # 가장 검증된 고성능 제미나이 모델 사용
    prompt = f"""
첨부된 이미지는 세무사 1차 시험 '{subject}' 과목의 시험지입니다. 
이미지에 포함된 {min_q}번 ~ {max_q}번 사이의 모든 문제를 JSON으로 추출하세요.

[필수 요구사항]
1. bbox: 문제 본문의 영역을 [ymin, xmin, ymax, xmax] (0~1000) 좌표로 정확히 반환하십시오. 
   - 문제 번호(예: 41.)부터 문제 끝 문장(예: ~은?)까지만 포함.
   - ①~⑤ 선지는 절대로 bbox에 포함하지 마십시오.
2. 내용: 정답(숫자), 해설(상세히), 분류 태그를 실제 문제 내용에 근거하여 채우십시오. '정답', '해설' 같은 플레이스홀더 사용 금지.
3. 이미지 구성: 이 시험지는 1단(Single Column) 구성입니다. 위에서 아래로 순서대로 문제를 찾으세요.

[목차 참고]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

{{
  "results": [
    {{
      "number": 41,
      "bbox": [100, 50, 250, 900],
      "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
      "answer": "3",
      "explanation": "...",
      "tags": {{ "unit": "...", "sub_unit": "...", "concept": "...", "difficulty": 3 }}
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
        res = json.loads(json_text)
        return res
    except Exception as e:
        print(f"[GEMINI API Error] {e}")
        return None

def process_task(task, taxonomy_data, main_db):
    pdf_path = task['pdf']
    year = task['year']
    session = task['session']
    subject = normalize_nfc(task['subject'])
    min_q, max_q = task['min_q'], task['max_q']
    
    print(f"\n>> {year}년 {session}교시 - {subject} 시작 (Gemini 1.5 Pro 모드)")
    doc = fitz.open(pdf_path)
    output_dir = "images"
    subject_taxonomy = taxonomy_data.get(subject, "목차 없음")
    
    # 민법 시작 페이지(18p)부터 마지막까지
    for page_num in range(17, len(doc)):
        page = doc[page_num]
        print(f"  Processing Page {page_num+1}/{len(doc)}...")
        
        # Matrix(2, 2)로 속도 향상
        pix_page = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        pix_b64 = encode_image(pix_page)
        
        res = extract_spatial_via_gemini(pix_b64, subject_taxonomy, subject, min_q, max_q)
        
        # res가 리스트인 경우 처리
        results = []
        if isinstance(res, list):
            results = res
        elif isinstance(res, dict):
            results = res.get('results', [])
            
        print(f"    [Debug] AI found {len(results)} questions.")
        
        if results:
            for item in results:
                try: q_num = int(item.get('number'))
                except: continue
                if q_num < min_q or q_num > max_q: continue
                
                bbox = item.get('bbox')
                if not bbox: continue
                
                # 좌표 보정 (가로 폭은 잘리지 않게 전체 유지, 세로만 타이트하게)
                y_top = max(0, (bbox[0] / 1000.0) * page.rect.height - 12)
                y_bottom = min(page.rect.height, (bbox[2] / 1000.0) * page.rect.height + 12)
                x_left = 0 # 가로 전체 유지
                x_right = page.rect.width # 가로 전체 유지
                
                crop_rect = fitz.Rect(x_left, y_top, x_right, y_bottom)
                pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
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
                print(f"    -> Extracted Q{q_num} (Saved)")

        # 실시간 저장
        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
            
    return main_db

def main():
    task = {"pdf": "sources/기출문제/세무사/2024/2024년도 제61회 세무사 1차시험 2교시 시험지 원본(민법).pdf", "year": "2024", "session": 2, "subject": "민법", "min_q": 41, "max_q": 80}
    with open("taxonomy.json", "r", encoding="utf-8") as f: taxonomy_data = json.load(f)
    try:
        with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    except: main_db = []
    process_task(task, taxonomy_data, main_db)
    print("\n🎉 2024년도 민법 Gemini 복구 완료!")

if __name__ == "__main__":
    main()
