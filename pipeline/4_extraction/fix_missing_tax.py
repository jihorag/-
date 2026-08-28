import base64
import json
import os
import fitz
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

def extract_specific_questions(pix_b64, subject_taxonomy, subject, target_nums):
    prompt = f"""
첨부된 이미지는 세무사 1차 시험 시험지입니다. 
이미지에 '{subject}' 과목의 다음 문제들 중 하나라도 포함되어 있다면 JSON으로 추출하세요: {target_nums}
만약 해당 문제 번호가 이 페이지에 없다면 빈 배열 '[]'을 반환하세요.

[필수 요구사항]
1. bbox: 문제 본문의 영역을 [ymin, xmin, ymax, xmax] (0~1000) 좌표로 정확히 반환하십시오. 
   - 문제 번호부터 문제 끝 문장까지만 포함.
   - ①~⑤ 선지는 절대로 bbox에 포함하지 마십시오.
2. 내용: 정답(숫자), 해설(상세히), 분류 태그를 실제 문제 내용에 근거하여 채우십시오.
3. 이 시험지는 1단(Single Column) 구성입니다. 

[목차 참고]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

결과는 반드시 'results' 키를 가진 배열이어야 합니다:
{{
  "results": [
    {{
      "number": 1,
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
        return json.loads(json_text)
    except Exception as e:
        print(f"[GEMINI API Error] {e}")
        return None

def main():
    with open("taxonomy.json", "r", encoding="utf-8") as f: taxonomy_data = json.load(f)
    try:
        with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    except: main_db = []

    fix_tasks = [
        {
            "pdf": "sources/기출문제/세무사/2023/2023년 제60회 세무사 1차시험 2교시 문제지(민법).pdf",
            "year": "2023", "session": 2, "subject": "회계학개론", "missing": [27, 28, 29]
        },
        {
            "pdf": "sources/기출문제/세무사/2022/2022년도 제59회 세무사 1차 시험 2교시 문제지 A형(민법).pdf",
            "year": "2022", "session": 2, "subject": "회계학개론", "missing": [1, 2, 16, 17, 37, 38]
        }
    ]

    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    for task in fix_tasks:
        pdf_path = task["pdf"]
        year = task["year"]
        session = task["session"]
        subject = task["subject"]
        missing_nums = task["missing"]
        
        print(f"\n>> Fixing {year} {subject} - Missing: {missing_nums}")
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            continue
            
        doc = fitz.open(pdf_path)
        subject_taxonomy = taxonomy_data.get(subject, "목차 없음")
        
        # 회계학개론은 보통 앞쪽 페이지(1~15p)에 있음
        for page_num in range(15):
            if not missing_nums: break
            
            page = doc[page_num]
            print(f"    Scanning Page {page_num+1}/15 for {missing_nums}...")
            
            pix_page = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            pix_b64 = encode_image(pix_page)
            
            res = extract_specific_questions(pix_b64, subject_taxonomy, subject, missing_nums)
            
            results = []
            if isinstance(res, list): results = res
            elif isinstance(res, dict): results = res.get('results', [])
            
            if results:
                for item in results:
                    try: q_num = int(item.get('number'))
                    except: continue
                    if q_num not in missing_nums: continue
                    
                    bbox = item.get('bbox')
                    if not bbox: continue
                    
                    y_top = max(0, (bbox[0] / 1000.0) * page.rect.height - 12)
                    y_bottom = min(page.rect.height, (bbox[2] / 1000.0) * page.rect.height + 12)
                    
                    crop_rect = fitz.Rect(0, y_top, page.rect.width, y_bottom)
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
                    
                    # Upsert
                    found = False
                    for i, db_q in enumerate(main_db):
                        if normalize_nfc(db_q.get("id", "")) == normalize_nfc(q_id):
                            main_db[i] = q_data
                            found = True; break
                    if not found: main_db.append(q_data)
                    
                    print(f"        -> [Success] Recovered Q{q_num}")
                    missing_nums.remove(q_num)

            with open("questions_db.json", "w", encoding="utf-8") as f:
                json.dump(main_db, f, ensure_ascii=False, indent=2)
            with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
                json.dump(main_db, f, ensure_ascii=False, indent=2)

    print("\n🎉 Recovery complete!")

if __name__ == "__main__":
    main()
