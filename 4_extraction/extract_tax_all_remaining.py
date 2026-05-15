import base64
import json
import os
import fitz
import time
import unicodedata
import glob
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
첨부된 이미지는 세무사 1차 시험 시험지입니다. 
이미지에 '{subject}' 과목의 {min_q}번 ~ {max_q}번 문제가 포함되어 있다면 이를 JSON으로 추출하세요.
해당 과목이나 문제가 페이지에 없다면 빈 배열 '[]'을 반환하세요.

[필수 요구사항]
1. bbox: 문제 본문의 영역을 [ymin, xmin, ymax, xmax] (0~1000) 좌표로 정확히 반환하십시오. 
   - 문제 번호(예: {min_q}.)부터 문제 끝 문장까지만 포함.
   - ①~⑤ 선지는 절대로 bbox에 포함하지 마십시오.
2. 내용: 정답(숫자), 해설(상세히), 분류 태그를 실제 문제 내용에 근거하여 채우십시오.
3. 이 시험지는 1단(Single Column) 구성입니다. 위에서 아래로 찾으세요.

[목차 참고]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

결과는 반드시 'results' 키를 가진 배열이어야 합니다:
{{
  "results": [
    {{
      "number": {min_q},
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
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                thinking_config={"thinking_level": "HIGH"}
            )
        )
        json_text = response.text.replace('\\', '\\\\')
        res = json.loads(json_text)
        return res
    except Exception as e:
        print(f"[GEMINI API Error] {e}")
        return None

def main():
    with open("taxonomy.json", "r", encoding="utf-8") as f: 
        taxonomy_data = json.load(f)
    
    try:
        with open("questions_db.json", "r", encoding="utf-8") as f: 
            main_db = json.load(f)
    except: 
        main_db = []

    pdf_files = sorted(glob.glob("기출문제/세무사/*/*.pdf"))
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        year_str = os.path.basename(os.path.dirname(pdf_path))
        
        try:
            year = int(year_str)
        except:
            continue

        if year < 2024:
            continue

        session = 1 if "1교시" in normalize_nfc(filename) else 2
        
        # 건너뛸 이미 처리된 파일들 조건 (필요시 조정 가능)
        # 2024년 2교시 민법은 별도 스크립트에서 진행 중이므로 패스
        if year == 2024 and session == 2 and "민법" in normalize_nfc(filename):
            print(f">> Skipping {year} Session 2 (handled separately)")
            continue
            
        print(f"\n>> Start Processing {year} Session {session} ({filename})")
        
        if session == 1:
            tasks = [("재정학", 1, 40), ("세법학개론", 41, 80)]
        else:
            tasks = [("회계학개론", 1, 40), ("민법", 41, 80)]
            
        doc = fitz.open(pdf_path)
        
        for subject, min_q, max_q in tasks:
            print(f"\n  == Subject: {subject} (Q{min_q}~{max_q}) ==")
            subject_taxonomy = taxonomy_data.get(subject, "목차 없음")
            
            for page_num in range(len(doc)):
                # 간단한 최적화: 과목별로 대략적인 페이지 범위만 탐색 (여기선 전체 탐색)
                page = doc[page_num]
                pix_page = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                pix_b64 = encode_image(pix_page)
                
                print(f"    Scanning Page {page_num+1}/{len(doc)}...")
                res = extract_spatial_via_gemini(pix_b64, subject_taxonomy, subject, min_q, max_q)
                
                results = []
                if isinstance(res, list): results = res
                elif isinstance(res, dict): results = res.get('results', [])
                
                if results:
                    print(f"      [!] Found {len(results)} questions for {subject}")
                    for item in results:
                        try: q_num = int(item.get('number'))
                        except: continue
                        if q_num < min_q or q_num > max_q: continue
                        
                        bbox = item.get('bbox')
                        if not bbox: continue
                        
                        y_top = max(0, (bbox[0] / 1000.0) * page.rect.height - 12)
                        y_bottom = min(page.rect.height, (bbox[2] / 1000.0) * page.rect.height + 12)
                        x_left = 0
                        x_right = page.rect.width
                        
                        crop_rect = fitz.Rect(x_left, y_top, x_right, y_bottom)
                        pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
                        img_filename = f"tax_{year}_s{session}_{q_num}_body.png"
                        pix_q.save(os.path.join(output_dir, img_filename))
                        
                        q_id = f"tax_{year}_{subject}_{q_num}"
                        q_data = {
                            "year": str(year), "subject": subject, "number": str(q_num), "question": f"[IMAGE: {img_filename}]",
                            "options": item.get('options', []), "answer": str(item.get('answer', "")),
                            "explanation": item.get('explanation', ""), "tags": item.get('tags', {}),
                            "exam": "세무사", "id": q_id
                        }
                        
                        found = False
                        for i, db_q in enumerate(main_db):
                            if normalize_nfc(db_q.get("id", "")) == normalize_nfc(q_id):
                                main_db[i] = q_data
                                found = True; break
                        if not found: main_db.append(q_data)
                        print(f"        -> Extracted Q{q_num} (Saved)")

                # 실시간 저장
                with open("questions_db.json", "w", encoding="utf-8") as f:
                    json.dump(main_db, f, ensure_ascii=False, indent=2)
                with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
                    json.dump(main_db, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
