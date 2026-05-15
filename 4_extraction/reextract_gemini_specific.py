import base64
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

target_questions = [1, 2, 3, 4, 5, 9, 11, 12]
subject = "재정학"
year = "2026"
session = 1

def encode_image(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def extract_single_q_via_gemini(pix_b64, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key={gemini_api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/png", "data": pix_b64}}
            ]
        }],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        res = response.json()
        text_result = res['candidates'][0]['content']['parts'][0]['text']
        return json.loads(text_result)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

def main():
    db_path = "questions_db.json"
    viewer_db_path = "viewer/src/data/questions_db.json"
    pdf_path = "기출문제/세무사/2026/2026년도 제63회 세무사 1차시험 1교시 시험지 원본.pdf"
    
    with open(db_path, "r", encoding="utf-8") as f:
        main_db = json.load(f)
        
    taxonomy_data = {}
    if os.path.exists("taxonomy.json"):
        with open("taxonomy.json", "r", encoding="utf-8") as f:
            taxonomy_data = json.load(f)
            
    subject_taxonomy = taxonomy_data.get(subject, "등록된 목차가 없습니다.")

    import fitz
    import re
    doc = fitz.open(pdf_path)
    
    last_q_num = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        text_items = []
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text_items.append({"text": s["text"].strip(), "bbox": s["bbox"]})
        
        q_starts = []
        opt_starts = []
        for item in text_items:
            if re.match(r"^\d+\.", item["text"]) and item["bbox"][0] < page.rect.width / 2 + 50:
                q_starts.append(item)
            if "①" in item["text"]:
                opt_starts.append(item)
                
        q_starts.sort(key=lambda x: x["bbox"][1])
        opt_starts.sort(key=lambda x: x["bbox"][1])
        
        for idx, q in enumerate(q_starts):
            try:
                q_num = int(re.search(r"^\d+", q["text"]).group())
                if q_num > 80: continue
                if q_num <= last_q_num: continue
                last_q_num = q_num
                
                if q_num not in target_questions:
                    continue
                    
                print(f"Correctly Cropping and Re-extracting Q{q_num} from PDF...")
                
                y_top = q["bbox"][1] - 8
                my_opt = next((o for o in opt_starts if o["bbox"][1] > y_top), None)
                
                x0 = 0
                x1 = page.rect.width
                
                if my_opt:
                    y_bottom = my_opt["bbox"][1] - 2
                else:
                    y_bottom = q_starts[idx+1]["bbox"][1] - 10 if idx+1 < len(q_starts) else page.rect.height - 50
                    
                crop_rect = fitz.Rect(x0, y_top, x1, y_bottom)
                pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
                
                img_path = f"images/tax_{year}_s{session}_{q_num}_body.png"
                pix_q.save(img_path)
                
                pix_b64 = encode_image(img_path)
                
                prompt = f"""
첨부된 이미지에서 {q_num}번 문제의 '선지(①~⑤)'와 '정답', '해설'을 추출하고, 
해당 과목({subject})의 내용에 맞게 분류 태깅(목차)을 동시에 수행하십시오.
이미지 내의 {q_num}번 문제 하나에 대해서만 응답하세요.

[과목: {subject} 의 목차 분류 체계 참고]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

결과는 반드시 'results' 키를 가진 아래 JSON 배열 형식으로 응답하십시오:
{{
  "results": [
    {{
      "number": {q_num},
      "options": ["① 실제내용", "② 실제내용", "③ 실제내용", "④ 실제내용", "⑤ 실제내용"],
      "answer": "정답번호(숫자만)",
      "explanation": "해설",
      "tags": {{
        "unit": "대단원 (참고 목차 기반)",
        "sub_unit": "중단원 (참고 목차 기반)",
        "concept": "핵심 개념",
        "difficulty": 3,
        "question_type": "유형 (계산형, 이론형 등)"
      }}
    }}
  ]
}}
"""
                res = extract_single_q_via_gemini(pix_b64, prompt)
                
                if res and 'results' in res and len(res['results']) > 0:
                    new_data = res['results'][0]
                    q_id = f"tax_{year}_{subject}_{q_num}"
                    for db_q in main_db:
                        if db_q.get("id") == q_id:
                            db_q["options"] = new_data.get("options", db_q.get("options"))
                            db_q["answer"] = new_data.get("answer", db_q.get("answer"))
                            db_q["explanation"] = new_data.get("explanation", db_q.get("explanation"))
                            db_q["tags"] = new_data.get("tags", db_q.get("tags"))
                            print(f"  -> DB Updated successfully for Q{q_num}")
                            break
            except Exception as e:
                print(f"Error processing Q{q_num}: {e}")

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(main_db, f, ensure_ascii=False, indent=2)
    with open(viewer_db_path, "w", encoding="utf-8") as f:
        json.dump(main_db, f, ensure_ascii=False, indent=2)
        
    print("All targeted questions re-extracted and DB updated!")

if __name__ == "__main__":
    main()
