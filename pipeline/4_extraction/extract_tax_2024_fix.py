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
    # Pro 002 모델 사용 (3.1 Pro 할당량 우회)
    prompt = f"""
첨부된 이미지는 세무사 1차 시험 '{subject}' 과목의 시험지입니다. 
이미지에 포함된 {min_q}번 ~ {max_q}번 사이의 모든 문제를 하나도 빠짐없이 JSON으로 추출하세요.

[필수 요구사항]
1. bbox: 문제 본문의 영역을 [ymin, xmin, ymax, xmax] (0~1000) 좌표로 정확히 반환하십시오. 
   - 번호(예: 1.)부터 문제 끝 문장(예: ~은?)까지만 포함.
   - ①~⑤ 선지는 절대로 bbox에 포함하지 마십시오.
2. 내용: 정답(숫자), 해설(상세히), 분류 태그를 실제 문제 내용에 근거하여 채우십시오. '정답', '해설' 같은 플레이스홀더 사용 금지.
3. 누락 금지: 페이지에 보이는 번호는 모두 추출해야 합니다.

[목차 참고]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

{{
  "results": [
    {{
      "number": 1,
      "bbox": [100, 50, 250, 480],
      "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
      "answer": "3",
      "explanation": "이 문제는 ~에 관한 것으로, ...이기 때문에 3번이 정답입니다.",
      "tags": {{ "unit": "...", "sub_unit": "...", "concept": "...", "difficulty": 3 }}
    }}
  ]
}}
"""
    try:
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-2.5-pro", 
            contents=[prompt, types.Part.from_bytes(data=base64.b64decode(pix_b64), mime_type="image/png")],
            config=types.GenerateContentConfig(response_mime_type="application/json")
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
    min_q, max_q = task['min_q'], task['max_q']
    
    print(f"\n>> {year}년 {session}교시 - {subject} 시작 (1.5 Pro 고정밀 모드)")
    doc = fitz.open(pdf_path)
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    subject_taxonomy = taxonomy_data.get(subject, "목차 없음")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        # 2024년 2교시는 회계학(1-17p), 민법(18-30p)
        # 해당 과목 범위가 아닌 페이지는 스킵
        if subject == "회계학" and page_num > 17: continue
        if subject == "민법" and page_num < 17: continue
        
        print(f"  Processing Page {page_num+1}/{len(doc)} via 1.5 Pro...")
        pix_page = page.get_pixmap(matrix=fitz.Matrix(3.5, 3.5)) # 해상도 업그레이드
        pix_b64 = encode_image(pix_page)
        
        res = extract_spatial_via_gemini(pix_b64, subject_taxonomy, subject, min_q, max_q)
        if res and 'results' in res:
            # 번호순 정렬
            items = sorted(res.get('results', []), key=lambda x: int(x.get('number', 0)))
            for item in items:
                try: q_num = int(item.get('number'))
                except: continue
                if q_num < min_q or q_num > max_q: continue
                
                bbox = item.get('bbox')
                if not bbox or len(bbox) != 4: continue
                
                # 좌표 보정 및 크롭
                y_top = (bbox[0] / 1000.0) * page.rect.height - 8
                y_bottom = (bbox[2] / 1000.0) * page.rect.height + 8
                # 2단 구성 대응: x좌표가 500 미만이면 왼쪽 단, 500 이상이면 오른쪽 단으로 처리할 수도 있지만, 
                # 여기서는 가로 전체를 잡고 AI가 준 x좌표를 참고하여 크롭 범위를 결정
                x_left = (bbox[1] / 1000.0) * page.rect.width - 10
                x_right = (bbox[3] / 1000.0) * page.rect.width + 10
                
                crop_rect = fitz.Rect(max(0, x_left), max(0, y_top), min(page.rect.width, x_right), min(page.rect.height, y_bottom))
                
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
                print(f"    -> Extracted Q{q_num} (Coord: {bbox})")

        # 실시간 저장
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
    # 기존 DB 로드 (중복 제거를 위해)
    try:
        with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    except: main_db = []
    
    for task in tasks: main_db = process_task(task, taxonomy_data, main_db)
    print("\n🎉 2024년도 2교시(회계학, 민법) 1.5 Pro 복구 완료!")

if __name__ == "__main__":
    main()
