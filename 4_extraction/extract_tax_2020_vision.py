import os
import json
import fitz
import re
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def extract_page_questions_vision(page, year, session):
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
    img_data = pix.tobytes("png")
    
    client = genai.Client(api_key=gemini_api_key)
    
    prompt = f"""
이 이미지는 {year}년 세무사 1차 시험지입니다.
이 페이지에 포함된 모든 문제들을 추출해 주세요.

[지시사항]
1. 각 문제의 바운딩 박스(bbox)를 [ymin, xmin, ymax, xmax] 형식으로 제공하세요. (0~1000 scale)
   - ymin: 문제 번호 바로 위
   - ymax: 첫 번째 선지 기호 ①이 시작되기 직전 (매우 중요: 이미지 하단에 ① 기호가 조금이라도 포함되면 안 됩니다)
   - xmin/xmax: 0과 1000을 사용하여 가로 여백을 전체적으로 포함하세요.
2. 각 문제의 번호, 선지(①~⑤), 정답, 상세 해설, 태그를 JSON 형식으로 반환하세요.
   - 선지 텍스트는 이미지에서 제외되지만, JSON 데이터에는 반드시 포함되어야 합니다.

반드시 아래 JSON 리스트 형식으로만 응답하세요:
[
  {{
    "number": "번호",
    "bbox": [ymin, 0, ymax, 1000],
    "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
    "answer": "정답번호",
    "explanation": "상세 해설 (띄어쓰기 교정 포함)",
    "tags": {{ "unit": "...", "sub_unit": "...", "concept": "...", "difficulty": 3 }}
  }},
  ...
]
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[
                types.Part.from_bytes(data=img_data, mime_type="image/png"),
                prompt
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"  [Gemini Vision Error] {e}")
        return []

def main():
    db_path = "questions_db.json"
    viewer_db_path = "viewer/src/data/questions_db.json"
    
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            main_db = json.load(f)
    except:
        main_db = []

    existing_ids = {q["id"] for q in main_db if "id" in q}

    tasks = [
        {"pdf": "기출문제/세무사/2020/1교시 A형.pdf", "year": "2020", "session": 1, "subjects": ["재정학", "세법학개론"]},
        {"pdf": "기출문제/세무사/2020/2교시 A형(선택과목 민법).pdf", "year": "2020", "session": 2, "subjects": ["회계학개론", "민법"]}
    ]

    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    for task in tasks:
        pdf_path = task["pdf"]
        year = task["year"]
        session = task["session"]
        
        print(f"\n>> Processing {year} Session {session} (Vision)...")
        if not os.path.exists(pdf_path):
            continue
            
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            print(f"  - Page {page_num+1}/{len(doc)}")
            page = doc[page_num]
            
            questions = extract_page_questions_vision(page, year, session)
            
            for q in questions:
                try:
                    q_num = str(q["number"])
                    # Determine subject based on question number
                    # 2020 Session 1: 1-40 재정학, 41-80 세법학개론
                    # 2020 Session 2: 1-40 회계학개론, 41-80 민법
                    n = int(re.sub(r'\D', '', q_num))
                    if session == 1:
                        subject = "재정학" if n <= 40 else "세법학개론"
                    else:
                        subject = "회계학개론" if n <= 40 else "민법"
                    
                    if subject == "세법학개론": continue # Skip as requested before
                    
                    q_id = f"tax_{year}_{subject}_{n}"
                    if q_id in existing_ids: continue
                    
                    print(f"    -> Saving Q{n} ({subject})...")
                    
                    # Crop image
                    ymin, xmin, ymax, xmax = q["bbox"]
                    page_width = page.rect.width
                    page_height = page.rect.height
                    crop_rect = fitz.Rect(
                        xmin * page_width / 1000,
                        ymin * page_height / 1000,
                        xmax * page_width / 1000,
                        ymax * page_height / 1000
                    )
                    
                    pix = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(3.0, 3.0))
                    img_filename = f"tax_{year}_s{session}_{n}_body.png"
                    pix.save(os.path.join(output_dir, img_filename))
                    
                    q_data = {
                        "id": q_id,
                        "exam": "세무사",
                        "year": str(year),
                        "subject": subject,
                        "number": str(n),
                        "question": f"[IMAGE: {img_filename}]",
                        "options": q["options"],
                        "answer": str(q["answer"]),
                        "explanation": q["explanation"],
                        "tags": q.get("tags", {"subject": subject, "difficulty": 3})
                    }
                    
                    main_db.append(q_data)
                    existing_ids.add(q_id)
                    
                    # Save progressively
                    with open(db_path, "w", encoding="utf-8") as f:
                        json.dump(main_db, f, ensure_ascii=False, indent=2)
                    with open(viewer_db_path, "w", encoding="utf-8") as f:
                        json.dump(main_db, f, ensure_ascii=False, indent=2)
                        
                except Exception as e:
                    print(f"    [Error] {e}")
                    
    print("\n[+] 2020 Vision extraction complete!")

if __name__ == "__main__":
    main()
