import os
import json
import fitz
import re
import unicodedata
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def normalize_nfc(text):
    return unicodedata.normalize('NFC', text)

def extract_options_via_gemini(text, subject, q_num):
    prompt = f"""
다음 텍스트는 회계사 시험 {subject} 과목 {q_num}번 문제의 보기(선지) 부분입니다.
OCR 과정에서 띄어쓰기 없이 붙어있는 글자나 오타를 **문맥에 맞게 자연스러운 한국어로 반드시 교정**하여 ①부터 ⑤까지의 보기를 정제해 주세요.

[텍스트]
{text}

[출력 형식]
반드시 아래 JSON 형식으로만 응답하세요.
{{
  "options": [
    "① ...",
    "② ...",
    "③ ...",
    "④ ...",
    "⑤ ..."
  ],
  "answer": "정답번호(숫자만)",
  "explanation": "상세한 해설 (오타 교정 포함)",
  "tags": {{
    "unit": "대단원",
    "sub_unit": "중단원",
    "concept": "핵심 개념",
    "difficulty": 3
  }}
}}
"""
    try:
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"  [Gemini Error] {e}")
    return { "options": ["①", "②", "③", "④", "⑤"], "answer": "", "explanation": "", "tags": {} }

def process_cpa_file(pdf_path, year, target_subjects, main_db, existing_ids):
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n>> Processing {year} CPA: {os.path.basename(pdf_path)}...")
    doc = fitz.open(pdf_path)
    
    current_subject = None
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        words = page.get_text("words")
        text = page.get_text()
        
        # Determine subject on this page
        # Usually written at the top like "경제원론", "회계학"
        page_subject = None
        for sub in target_subjects:
            if sub in text[:300]: # Check header area
                page_subject = sub
                break
                
        if page_subject:
            current_subject = page_subject
            
        if not current_subject or current_subject not in target_subjects:
            continue
            
        # Standardize subject name for DB
        db_subject = "경제학" if current_subject == "경제원론" else current_subject
        
        # 2-column detection logic
        mid_x = page.rect.width / 2
        
        q_starts = []
        for w in words:
            word_text = w[4]
            if re.match(r'^\d+\.$', word_text):
                try:
                    q_num = int(word_text.replace('.', ''))
                    # Valid question number? (1~50)
                    if 1 <= q_num <= 50 and w[0] < page.rect.width:
                        column = "left" if w[0] < mid_x else "right"
                        q_starts.append({"q_num": q_num, "x0": w[0], "y0": w[1], "y1": w[3], "column": column})
                except: continue
                
        # Sort by y-coordinate within each column
        left_qs = sorted([q for q in q_starts if q["column"] == "left"], key=lambda x: x["y0"])
        right_qs = sorted([q for q in q_starts if q["column"] == "right"], key=lambda x: x["y0"])
        
        for col_qs, col_type in [(left_qs, "left"), (right_qs, "right")]:
            for i, q_info in enumerate(col_qs):
                q_num = q_info["q_num"]
                q_id = f"cpa_{year}_{db_subject}_{q_num}"
                
                if normalize_nfc(q_id) in existing_ids: continue
                
                print(f"  -> Extracting [{db_subject}] Q{q_num} ({col_type} col)...")
                q_y0 = q_info["y0"]
                
                # Define column bounding box
                if col_type == "left":
                    col_rect = fitz.Rect(0, 0, mid_x - 5, page.rect.height)
                else:
                    col_rect = fitz.Rect(mid_x + 5, 0, page.rect.width, page.rect.height)
                
                # Search for option marker '①' within this column
                options_rects = page.search_for("①", clip=col_rect)
                valid_options = [r for r in options_rects if r.y0 > q_y0]
                
                if not valid_options:
                    options_rects = page.search_for("(1)", clip=col_rect)
                    valid_options = [r for r in options_rects if r.y0 > q_y0]
                    if not valid_options:
                        print(f"    [!] Missing options for Q{q_num}")
                        continue
                        
                opt_y0 = valid_options[0].y0
                
                # Crop body image
                y_top = max(0, q_y0 - 5)
                y_bottom = min(page.rect.height, opt_y0 - 2)
                
                # We crop only the specific column!
                crop_rect = fitz.Rect(col_rect.x0, y_top, col_rect.x1, y_bottom)
                pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(3.0, 3.0))
                
                img_filename = f"cpa_{year}_{db_subject}_{q_num}_body.png"
                pix_q.save(os.path.join(output_dir, img_filename))
                
                # Extract options text
                end_y = page.rect.height
                if i + 1 < len(col_qs):
                    end_y = col_qs[i+1]["y0"] - 5
                
                opt_crop_rect = fitz.Rect(col_rect.x0, opt_y0 - 5, col_rect.x1, end_y)
                opt_text = page.get_text("text", clip=opt_crop_rect, sort=True)
                
                llm_res = extract_options_via_gemini(opt_text, db_subject, q_num)
                options = llm_res.get("options", ["①", "②", "③", "④", "⑤"])
                
                # Assign unit for Economics
                unit_val = llm_res.get("tags", {}).get("unit", "")
                if db_subject == "경제학":
                    if '미시' in unit_val or '1' in unit_val: unit_val = 'PART 001 미시경제학'
                    elif '거시' in unit_val or '2' in unit_val: unit_val = 'PART 002 거시경제학'
                    else: unit_val = 'PART 003 재정학'
                
                q_data = {
                    "id": q_id,
                    "exam": "회계사",
                    "year": str(year),
                    "subject": db_subject,
                    "number": str(q_num),
                    "question": f"[IMAGE: {img_filename}]",
                    "options": options,
                    "answer": str(llm_res.get("answer", "")),
                    "explanation": llm_res.get("explanation", ""),
                    "tags": {
                        "subject": db_subject,
                        "unit": unit_val,
                        "sub_unit": llm_res.get("tags", {}).get("sub_unit", ""),
                        "concept": llm_res.get("tags", {}).get("concept", ""),
                        "difficulty": llm_res.get("tags", {}).get("difficulty", 3)
                    }
                }
                
                main_db.append(q_data)
                existing_ids.add(normalize_nfc(q_id))
                
                # Save dynamically to avoid losing data
                with open("questions_db.json", "w", encoding="utf-8") as f:
                    json.dump(main_db, f, ensure_ascii=False, indent=2)

def main():
    db_path = "questions_db.json"
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            main_db = json.load(f)
    except:
        main_db = []

    existing_ids = {normalize_nfc(q["id"]) for q in main_db if "id" in q}

    # Focus on recent year 2026 for now
    tasks = [
        {"pdf": "sources/기출문제/회계사/2026/1교시 경영학 경제원론(1형)_문제_2026.pdf", "year": "2026", "subjects": ["경제원론"]},
        {"pdf": "sources/기출문제/회계사/2026/3교시 회계학(1형)_문제_2026.pdf", "year": "2026", "subjects": ["회계학"]}
    ]

    for t in tasks:
        process_cpa_file(t["pdf"], t["year"], t["subjects"], main_db, existing_ids)
        
    import shutil
    shutil.copy("questions_db.json", "viewer/src/data/questions_db.json")
    shutil.copy("questions_db.json", "viewer/src/data/questions_tax.json")
    print("\n[+] 2026년 회계사 추출 완료 및 DB 동기화 성공!")

if __name__ == "__main__":
    main()
