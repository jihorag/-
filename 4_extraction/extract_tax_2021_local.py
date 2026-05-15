import os
import json
import fitz
import re
import requests
import unicodedata

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def normalize_nfc(text):
    return unicodedata.normalize('NFC', text)

def extract_options_via_gemini(text, q_num):
    prompt = f"""
다음 텍스트는 세무사 시험 {q_num}번 문제의 보기(선지) 부분입니다.
PDF 추출 과정에서 띄어쓰기가 누락되었을 수 있으므로, **문맥에 맞게 자연스러운 한국어 띄어쓰기를 반드시 적용**하여 ①부터 ⑤까지의 보기를 정제해 주세요.

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
  "explanation": "상세한 해설 (필요시 띄어쓰기 교정 포함)",
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
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"  [Gemini API Error] {e}")
    
    return {
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "",
        "explanation": "",
        "tags": {}
    }

def main():
    db_path = "questions_db.json"
    viewer_db_path = "viewer/src/data/questions_db.json"
    
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            main_db = json.load(f)
    except:
        main_db = []

    existing_ids = {normalize_nfc(q["id"]) for q in main_db if "id" in q}

    tasks = [
        {
            "pdf": "기출문제/세무사/2021/2021년도 제58회 세무사 1차 시험 1교시 A형.pdf",
            "year": "2021", "session": 1, "subjects": [("재정학", 1, 40)]
        },
        {
            "pdf": "기출문제/세무사/2021/2021년도 제58회 세무사 1차 시험 2교시 A형(민법).pdf",
            "year": "2021", "session": 2, "subjects": [("회계학개론", 1, 40), ("민법", 41, 80)]
        }
    ]

    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    for task in tasks:
        pdf_path = task["pdf"]
        year = task["year"]
        session = task["session"]
        
        print(f"\n>> Start Processing {year} Session {session}...")
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            continue
            
        doc = fitz.open(pdf_path)
        
        for subject, min_q, max_q in task["subjects"]:
            print(f"\n  == Subject: {subject} (Q{min_q}~{max_q}) ==")
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Check what questions are on this page
                words = page.get_text("words")
                
                # Find all potential question numbers on this page
                # format: "N."
                q_starts = []
                for w in words:
                    text = w[4]
                    if re.match(r'^\d+\.$', text):
                        q_num_str = text[:-1]
                        q_num = int(q_num_str)
                        if min_q <= q_num <= max_q and w[0] < 120: # Left aligned usually
                            q_starts.append({"q_num": q_num, "y0": w[1], "y1": w[3]})
                
                q_starts.sort(key=lambda x: x["y0"])
                
                for i, q_info in enumerate(q_starts):
                    q_num = q_info["q_num"]
                    q_id = f"tax_{year}_{subject}_{q_num}"
                    if normalize_nfc(q_id) in existing_ids:
                        print(f"    -> Skipping Q{q_num} (Already extracted)")
                        continue
                    
                    print(f"    -> Extracting Q{q_num}...")
                    
                    q_y0 = q_info["y0"]
                    
                    # Find ① after this question
                    options_rects = page.search_for("①")
                    valid_options = [r for r in options_rects if r.y0 > q_y0]
                    
                    if not valid_options:
                        print(f"      [!] Could not find ① for Q{q_num}")
                        continue
                        
                    opt_y0 = valid_options[0].y0
                    
                    # Crop image for question body (from q_y0 to opt_y0)
                    y_top = max(0, q_y0 - 5)
                    y_bottom = min(page.rect.height, opt_y0 - 2)
                    
                    crop_rect = fitz.Rect(0, y_top, page.rect.width, y_bottom)
                    pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(3.0, 3.0))
                    img_filename = f"tax_{year}_s{session}_{q_num}_body.png"
                    pix_q.save(os.path.join(output_dir, img_filename))
                    
                    # Find end of options (either next question or end of page)
                    end_y = page.rect.height
                    if i + 1 < len(q_starts):
                        end_y = q_starts[i+1]["y0"] - 5
                        
                    # Extract text for options
                    opt_crop_rect = fitz.Rect(0, opt_y0 - 5, page.rect.width, end_y)
                    opt_text = page.get_text("text", clip=opt_crop_rect, sort=True)
                    
                    # Send to Gemini
                    llm_res = extract_options_via_gemini(opt_text, q_num)
                    options = llm_res.get("options", ["①", "②", "③", "④", "⑤"])
                    if len(options) != 5:
                        options = [f"① {opt_text[:10]}...", "②", "③", "④", "⑤"]
                        
                    q_data = {
                        "id": q_id,
                        "exam": "세무사",
                        "year": str(year),
                        "subject": subject,
                        "number": str(q_num),
                        "question": f"[IMAGE: {img_filename}]",
                        "options": options,
                        "answer": str(llm_res.get("answer", "")),
                        "explanation": llm_res.get("explanation", ""),
                        "tags": llm_res.get("tags", {
                            "subject": subject,
                            "difficulty": 3
                        })
                    }
                    
                    main_db.append(q_data)
                    existing_ids.add(normalize_nfc(q_id))
                    
                    # Save progressively
                    with open(db_path, "w", encoding="utf-8") as f:
                        json.dump(main_db, f, ensure_ascii=False, indent=2)
                    with open(viewer_db_path, "w", encoding="utf-8") as f:
                        json.dump(main_db, f, ensure_ascii=False, indent=2)
                        
    print("\n[+] 2021년도 전체 (재정학, 회계학개론, 민법) 추출 완료!")

if __name__ == "__main__":
    main()
