import base64
import json
import os
import fitz
import time
import unicodedata
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def normalize_nfc(text):
    return unicodedata.normalize('NFC', text)

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_via_gpt(pix_b64, subject_taxonomy, subject, min_q, max_q):
    prompt = f"""
You are an expert archivist digitizing PUBLIC domain exam papers. 
Extract questions for '{subject}' between {min_q} and {max_q} from the image.

[Rules]
1. bbox: [ymin, xmin, ymax, xmax] (0~1000) for question body only.
2. Output JSON with fields: number, bbox, options, answer, explanation, tags.
3. NO PLACEHOLDERS. Solve the problems.

{{
  "results": [
    {{
      "number": {min_q},
      "bbox": [100, 0, 300, 1000],
      "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
      "answer": "3",
      "explanation": "...",
      "tags": {{ "unit": "...", "sub_unit": "...", "concept": "..." }}
    }}
  ]
}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{pix_b64}", "detail": "high"}}
                ]}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"[GPT Error] {e}")
        return None

def main():
    task = {"pdf": "sources/기출문제/세무사/2024/2024년도 제61회 세무사 1차시험 2교시 시험지 원본(민법).pdf", "year": "2024", "subject": "민법", "min_q": 59, "max_q": 80}
    with open("taxonomy.json", "r", encoding="utf-8") as f: taxonomy_data = json.load(f)
    with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    
    doc = fitz.open(task['pdf'])
    # 59번이 시작될 23페이지부터 끝까지
    for page_num in range(22, len(doc)):
        page = doc[page_num]
        print(f">> [GPT-4o] Scanning Page {page_num+1} for Q59~80...")
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        pix_b64 = encode_image(pix)
        
        res = extract_via_gpt(pix_b64, taxonomy_data.get(task['subject'], {}), task['subject'], task['min_q'], task['max_q'])
        results = res.get('results', []) if res else []
        
        print(f"   Found {len(results)} items.")
        for item in results:
            q_num = int(item.get('number', 0))
            if q_num < task['min_q'] or q_num > task['max_q']: continue
            
            bbox = item.get('bbox')
            if not bbox: continue
            
            # 가로 꽉 찬 크롭 (Full-width)
            y_top = max(0, (bbox[0] / 1000.0) * page.rect.height - 15)
            y_bottom = min(page.rect.height, (bbox[2] / 1000.0) * page.rect.height + 15)
            crop_rect = fitz.Rect(0, y_top, page.rect.width, y_bottom)
            
            pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
            filename = f"tax_2024_s2_{q_num}_body.png"
            pix_q.save(f"images/{filename}")
            
            q_id = f"tax_2024_{normalize_nfc(task['subject'])}_{q_num}"
            q_data = {
                "year": "2024", "subject": normalize_nfc(task['subject']), "number": str(q_num), "question": f"[IMAGE: {filename}]",
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
            print(f"   -> GPT Saved Q{q_num}")

        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
