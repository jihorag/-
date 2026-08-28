import base64
import json
import os
import fitz
import requests
import unicodedata
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def normalize_nfc(text):
    return unicodedata.normalize('NFC', text)

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_via_gpt(pix_b64, subject_taxonomy, subject, target_nums):
    prompt = f"""
This is a Tax Accountant Exam ({subject}). Extract questions {target_nums} from the image.
If a question is not fully present, skip it.

[Rules]
1. bbox: [ymin, xmin, ymax, xmax] (0-1000) for the question body ONLY. Exclude choices ①~⑤.
2. Content: Provide choices, answer, explanation, and taxonomy tags.
3. Use real data, solve the problems.

[Taxonomy]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

Return JSON:
{{
  "results": [
    {{
      "number": {target_nums[0]},
      "bbox": [100, 50, 300, 950],
      "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
      "answer": "3",
      "explanation": "...",
      "tags": {{ "unit": "...", "sub_unit": "...", "concept": "..." }}
    }}
  ]
}}
"""
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{pix_b64}", "detail": "high"}}
                ]
            }
        ],
        "response_format": {"type": "json_object"},
        "max_tokens": 4000
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return json.loads(response.json()['choices'][0]['message']['content'])
    except Exception as e:
        print(f"[GPT Error] {e}")
        return None

def main():
    with open("taxonomy.json", "r", encoding="utf-8") as f: taxonomy_data = json.load(f)
    try:
        with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    except: main_db = []

    tasks = [
        {
            "pdf": "sources/기출문제/세무사/2023/2023년 제60회 세무사 1차시험 2교시 문제지(민법).pdf",
            "year": "2023", "session": 2, "subject": "회계학개론",
            "pages": [13], "missing": [27, 28, 29]
        },
        {
            "pdf": "sources/기출문제/세무사/2022/2022년도 제59회 세무사 1차 시험 2교시 문제지 A형(민법).pdf",
            "year": "2022", "session": 2, "subject": "회계학개론",
            "pages": [1, 8, 17], "missing": [1, 2, 16, 17, 37, 38]
        }
    ]

    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    for task in tasks:
        doc = fitz.open(task["pdf"])
        sub_tax = taxonomy_data.get(task["subject"], "목차 없음")
        
        for p_idx in task["pages"]:
            page = doc[p_idx - 1]
            print(f">> {task['year']} p{p_idx} Scanning for {task['missing']}...")
            
            pix = page.get_pixmap(matrix=fitz.Matrix(3.0, 3.0))
            res = extract_via_gpt(encode_image(pix), sub_tax, task["subject"], task["missing"])
            
            if res and 'results' in res:
                for item in res['results']:
                    q_num = int(item.get('number'))
                    if q_num not in task['missing']: continue
                    
                    bbox = item.get('bbox')
                    y_top = max(0, (bbox[0] / 1000.0) * page.rect.height - 10)
                    y_bottom = min(page.rect.height, (bbox[2] / 1000.0) * page.rect.height + 10)
                    
                    crop_rect = fitz.Rect(0, y_top, page.rect.width, y_bottom)
                    pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
                    img_name = f"tax_{task['year']}_s{task['session']}_{q_num}_body.png"
                    pix_q.save(os.path.join(output_dir, img_name))
                    
                    q_id = f"tax_{task['year']}_{task['subject']}_{q_num}"
                    q_data = {
                        "year": str(task['year']), "subject": task['subject'], "number": str(q_num),
                        "question": f"[IMAGE: {img_name}]", "options": item.get('options', []),
                        "answer": str(item.get('answer', "")), "explanation": item.get('explanation', ""),
                        "tags": item.get('tags', {}), "exam": "세무사", "id": q_id
                    }
                    
                    # Upsert
                    found = False
                    for i, db_q in enumerate(main_db):
                        if normalize_nfc(db_q.get("id", "")) == normalize_nfc(q_id):
                            main_db[i] = q_data
                            found = True; break
                    if not found: main_db.append(q_data)
                    print(f"   -> Recovered Q{q_num}")

        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
