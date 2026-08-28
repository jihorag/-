import base64
import json
import os
import fitz
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_missing_2025():
    pdf_path = "sources/기출문제/세무사/2025/2025년도 제62회 세무사 1차시험 2교시 시험지 원본(민법).pdf"
    year = "2025"
    session = 2
    subject = "회계학"
    min_q, max_q = 32, 33
    
    doc = fitz.open(pdf_path)
    output_dir = "images"
    
    with open("taxonomy.json", "r", encoding="utf-8") as f:
        taxonomy_data = json.load(f)
    subject_taxonomy = taxonomy_data.get(subject, "목차 없음")
    
    client = genai.Client(api_key=gemini_api_key)
    
    with open("questions_db.json", "r", encoding="utf-8") as f:
        main_db = json.load(f)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if "32." not in text and "33." not in text:
            continue
            
        print(f"Extracting Q32-33 from page {page_num + 1}...")
        pix_page = page.get_pixmap(matrix=fitz.Matrix(3,3))
        pix_b64 = encode_image(pix_page)
        
        prompt = f"IMAGE contains questions 32 and 33 of {subject}. Extract them into JSON format. result: {{ 'results': [ {{ 'number': 32, 'bbox': [ymin, xmin, ymax, xmax], 'options': [...], 'answer': '1' }}, ... ] }}"
        
        response = client.models.generate_content(
            model="gemini-3.1-pro-preview", 
            contents=[prompt, types.Part.from_bytes(data=base64.b64decode(pix_b64), mime_type="image/png")],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        print(f"AI Response for Page {page_num+1}: {response.text}")
        
        json_text = response.text.replace('\\', '\\\\')
        res = json.loads(json_text)
        results = res if isinstance(res, list) else res.get('results', [])
        
        for item in results:
            try:
                q_num = int(item.get('number'))
            except:
                continue
            if q_num not in [32, 33]: continue
            
            ymin, xmin, ymax, xmax = item.get('bbox')
            crop_rect = fitz.Rect(0, (ymin/1000)*page.rect.height - 5, page.rect.width, (ymax/1000)*page.rect.height + 5)
            pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
            filename = f"tax_{year}_s{session}_{q_num}_body.png"
            pix_q.save(os.path.join(output_dir, filename))
            
            q_data = {
                "year": year, "subject": subject, "number": str(q_num),
                "question": f"[IMAGE: {filename}]", "options": item.get('options', []),
                "answer": str(item.get('answer', "")), "explanation": item.get('explanation', ""),
                "tags": item.get('tags', {}), "exam": "세무사", "id": f"tax_{year}_{subject}_{q_num}"
            }
            
            # Upsert
            found = False
            for i, db_q in enumerate(main_db):
                if db_q.get("id") == q_data["id"]:
                    main_db[i] = q_data
                    found = True
                    break
            if not found: main_db.append(q_data)
            print(f"  -> Successfully patched Q{q_num}")

    with open("questions_db.json", "w", encoding="utf-8") as f:
        json.dump(main_db, f, ensure_ascii=False, indent=2)
    with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
        json.dump(main_db, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract_missing_2025()
