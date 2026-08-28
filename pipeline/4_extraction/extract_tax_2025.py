import base64
import json
import os
import fitz
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_spatial_via_gemini(pix_b64, subject_taxonomy, subject, min_q, max_q):
    prompt = f"""
첨부된 이미지에는 '{subject}' 과목의 객관식 기출문제가 있습니다. 
각 문제에 대해 아래 JSON 형식으로 모든 데이터를 완벽하게 추출하십시오.
(주의: 추출 대상 문제는 {min_q}번부터 {max_q}번 사이여야 합니다. 이 범위를 벗어나는 문제는 무시하세요.)

특별 지시사항 (Spatial Bounding Box):
- 각 문제의 본문(문제 텍스트, 표, 그래프 등)의 위치를 `bbox` 필드에 [ymin, xmin, ymax, xmax] 형식으로 반환하십시오.
- 좌표는 0에서 1000 사이의 정수로 정규화된 값입니다.
- ⚠️ 매우 중요: 이 `bbox` 영역에는 **절대로 ①~⑤ 선지 부분이 포함되어서는 안 됩니다!** 문제 본문과 자료(표 등)까지만 포함하고, 선지가 시작되기 직전에서 ymax를 끊으십시오.

[과목: {subject} 의 목차 분류 체계 참고]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

반드시 'results' 키를 가진 아래 JSON 배열 형식으로만 응답하십시오:
{{
  "results": [
    {{
      "number": 1,
      "bbox": [150, 50, 400, 950],
      "options": ["① 내용", "② 내용", "③ 내용", "④ 내용", "⑤ 내용"],
      "answer": "정답번호(숫자만)",
      "explanation": "해설",
      "tags": {{
        "unit": "대단원 (참고 목차 기반)",
        "sub_unit": "중단원",
        "concept": "핵심 개념",
        "difficulty": 3,
        "question_type": "유형"
      }}
    }}
  ]
}}
"""
    try:
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents=[
                prompt,
                types.Part.from_bytes(data=base64.b64decode(pix_b64), mime_type="image/png")
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                thinking_config={"thinking_level": "HIGH"}
            )
        )
        json_text = response.text.replace('\\', '\\\\')
        res = json.loads(json_text)
        return res if isinstance(res, list) else res
    except Exception as e:
        print(f"[GEMINI API Error] {e}")
        return None

def process_task(task, taxonomy_data, main_db):
    pdf_path = task['pdf']
    year = task['year']
    session = task['session']
    subject = task['subject']
    min_q = task['min_q']
    max_q = task['max_q']
    
    print(f"\n========================================")
    print(f"Starting Extraction: {year}년 {session}교시 - {subject} ({min_q}~{max_q}번)")
    print(f"========================================")
    
    doc = fitz.open(pdf_path)
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    
    subject_taxonomy = taxonomy_data.get(subject, "목차 없음")
    updated_count = 0
    
    for page_num in range(len(doc)): 
        page = doc[page_num]
        
        # Fast Text Check to skip irrelevant pages
        text = page.get_text()
        found_any = False
        for qn in range(min_q, max_q + 1):
            if f"{qn}." in text or f"{qn} " in text:
                found_any = True
                break
        
        if not found_any:
            print(f"[{year}년 {subject}] Skipping page {page_num + 1}/{len(doc)} (no target questions found)")
            continue
            
        print(f"[{year}년 {subject}] Processing page {page_num + 1}/{len(doc)} via SPATIAL VISION...")
        
        pix_page = page.get_pixmap(matrix=fitz.Matrix(3,3))
        pix_b64 = encode_image(pix_page)
        
        res = extract_spatial_via_gemini(pix_b64, subject_taxonomy, subject, min_q, max_q)
        
        if res and 'results' in res:
            gpt_results = res.get('results', [])
            
            for item in gpt_results:
                q_num = item.get('number')
                
                if not isinstance(q_num, int) or q_num < min_q or q_num > max_q:
                    continue
                    
                bbox = item.get('bbox')
                if not bbox or len(bbox) != 4:
                    print(f"  -> Q{q_num} bbox missing or invalid!")
                    continue
                
                ymin, xmin, ymax, xmax = bbox
                page_height = page.rect.height
                page_width = page.rect.width
                
                y_top = (ymin / 1000.0) * page_height
                y_bottom = (ymax / 1000.0) * page_height
                
                y_top = max(0, y_top - 5)
                y_bottom = min(page_height, y_bottom + 5)
                
                # Full width crop
                crop_rect = fitz.Rect(0, y_top, page_width, y_bottom)
                
                try:
                    pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
                    filename = f"tax_{year}_s{session}_{q_num}_body.png"
                    pix_q.save(os.path.join(output_dir, filename))
                    
                    q_data = {
                        "year": year,
                        "subject": subject,
                        "number": str(q_num),
                        "question": f"[IMAGE: {filename}]",
                        "options": item.get('options', []),
                        "answer": str(item.get('answer', "")),
                        "explanation": item.get('explanation', ""),
                        "tags": item.get('tags', {}),
                        "exam": "세무사",
                        "id": f"tax_{year}_{subject}_{q_num}"
                    }
                    
                    # Update Main DB in memory
                    found = False
                    for i, db_q in enumerate(main_db):
                        if db_q.get("id") == q_data["id"]:
                            main_db[i] = q_data
                            found = True
                            updated_count += 1
                            break
                    if not found:
                        main_db.append(q_data)
                        updated_count += 1
                        
                    print(f"  -> Cropped & Extracted Q{q_num} (y_top:{int(y_top)}, y_bottom:{int(y_bottom)})")
                except Exception as e:
                    print(f"  -> Error cropping Q{q_num}: {e}")

        # Save DB after every page to prevent data loss
        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
            
        time.sleep(1)

    print(f"✅ {subject} 추출 완료! 업데이트 건수: {updated_count}")
    return main_db

def main():
    tasks = [
        {
            "pdf": "sources/기출문제/세무사/2025/2025년도 제62회 세무사 1차시험 1교시 시험지 원본.pdf",
            "year": "2025",
            "session": 1,
            "subject": "재정학",
            "min_q": 1,
            "max_q": 40
        },
        {
            "pdf": "sources/기출문제/세무사/2025/2025년도 제62회 세무사 1차시험 2교시 시험지 원본(민법).pdf",
            "year": "2025",
            "session": 2,
            "subject": "회계학",
            "min_q": 1,
            "max_q": 40
        },
        {
            "pdf": "sources/기출문제/세무사/2025/2025년도 제62회 세무사 1차시험 2교시 시험지 원본(민법).pdf",
            "year": "2025",
            "session": 2,
            "subject": "민법",
            "min_q": 41,
            "max_q": 80
        }
    ]
    
    taxonomy_data = {}
    if os.path.exists("taxonomy.json"):
        with open("taxonomy.json", "r", encoding="utf-8") as f:
            taxonomy_data = json.load(f)
            
    db_path = "questions_db.json"
    with open(db_path, "r", encoding="utf-8") as f:
        main_db = json.load(f)
        
    for task in tasks:
        main_db = process_task(task, taxonomy_data, main_db)
        
    print("\n🎉 모든 2025년도 세무사 기출문제 추출이 완료되었습니다!")

if __name__ == "__main__":
    main()
