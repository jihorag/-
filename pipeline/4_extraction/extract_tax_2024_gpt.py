import base64
import json
import os
import fitz
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_spatial_via_gpt(pix_b64, subject_taxonomy, subject, min_q, max_q):
    prompt = f"""
첨부된 이미지에는 '{subject}' 과목의 객관식 기출문제가 있습니다. 
각 문제에 대해 아래 JSON 형식으로 모든 데이터를 완벽하게 추출하십시오.
(추출 대상: {min_q}번 ~ {max_q}번)

특별 지시사항 (Spatial Bounding Box):
- 각 문제의 본문 영역을 `bbox` 필드에 [ymin, xmin, ymax, xmax] 형식으로 반환. (0~1000)
- ⚠️ 중요: `bbox` 영역에는 **절대로 ①~⑤ 선지 부분이 포함되어서는 안 됩니다!** 문제 본문까지만 포함하세요.

[목차 참고]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

반드시 아래 JSON 구조로 응답하십시오:
{{
  "results": [
    {{
      "number": {min_q},
      "bbox": [150, 50, 400, 950],
      "options": ["① 내용", "② 내용", "③ 내용", "④ 내용", "⑤ 내용"],
      "answer": "정답번호(숫자)",
      "explanation": "해설",
      "tags": {{ "unit": "...", "sub_unit": "...", "concept": "...", "difficulty": 3 }}
    }}
  ]
}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{pix_b64}"}
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=4096,
        )
        print(f"DEBUG Response: {response}")
        content = response.choices[0].message.content
        if content is None:
            print(f"DEBUG Refusal: {response.choices[0].message.refusal}")
            return None
        res = json.loads(content)
        return res
    except Exception as e:
        print(f"[GPT API Error] {e}")
        return None

def process_task(task, taxonomy_data, main_db):
    pdf_path = task['pdf']
    year = task['year']
    session = task['session']
    subject = task['subject']
    min_q, max_q = task['min_q'], task['max_q']
    
    print(f"\n>> {year}년 {session}교시 - {subject} 시작 (GPT-4o 정밀 모드)")
    doc = fitz.open(pdf_path)
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    subject_taxonomy = taxonomy_data.get(subject, "목차 없음")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        print(f"  Processing Page {page_num+1}/{len(doc)} via GPT-4o...")
        
        pix_page = page.get_pixmap(matrix=fitz.Matrix(3,3))
        pix_b64 = encode_image(pix_page)
        
        res = extract_spatial_via_gpt(pix_b64, subject_taxonomy, subject, min_q, max_q)
        if res and 'results' in res:
            for item in res.get('results', []):
                try: q_num = int(item.get('number'))
                except: continue
                if q_num < min_q or q_num > max_q: continue
                
                bbox = item.get('bbox')
                if not bbox or len(bbox) != 4: continue
                
                y_top = (bbox[0] / 1000.0) * page.rect.height - 5
                y_bottom = (bbox[2] / 1000.0) * page.rect.height + 5
                crop_rect = fitz.Rect(0, max(0, y_top), page.rect.width, min(page.rect.height, y_bottom))
                
                pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
                filename = f"tax_{year}_s{session}_{q_num}_body.png"
                pix_q.save(os.path.join(output_dir, filename))
                
                q_data = {
                    "year": year, "subject": subject, "number": str(q_num), "question": f"[IMAGE: {filename}]",
                    "options": item.get('options', []), "answer": str(item.get('answer', "")),
                    "explanation": item.get('explanation', ""), "tags": item.get('tags', {}),
                    "exam": "세무사", "id": f"tax_{year}_{subject}_{q_num}"
                }
                
                # Upsert
                found = False
                for i, db_q in enumerate(main_db):
                    if db_q.get("id") == q_data["id"]:
                        main_db[i] = q_data
                        found = True; break
                if not found: main_db.append(q_data)
                print(f"    -> Extracted Q{q_num}")

        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
    return main_db

def main():
    tasks = [
        {"pdf": "sources/기출문제/세무사/2024/2024년도 제61회 세무사 1차시험 2교시 시험지 원본(민법).pdf", "year": "2024", "session": 2, "subject": "회계학", "min_q": 1, "max_q": 40},
        {"pdf": "sources/기출문제/세무사/2024/2024년도 제61회 세무사 1차시험 2교시 시험지 원본(민법).pdf", "year": "2024", "session": 2, "subject": "민법", "min_q": 41, "max_q": 80}
    ]
    with open("taxonomy.json", "r", encoding="utf-8") as f: taxonomy_data = json.load(f)
    with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    for task in tasks: main_db = process_task(task, taxonomy_data, main_db)
    print("\n🎉 2024년도 누락분(회계학, 민법) GPT-4o 복구 추출 완료!")

if __name__ == "__main__":
    main()
