import base64
import json
import os
import fitz
import time
import unicodedata
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def normalize_nfc(text):
    return unicodedata.normalize('NFC', text)

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def get_physical_q_coords(page, min_q, max_q):
    """PDF 텍스트 엔진을 사용하여 문제 번호의 실제 Y 좌표를 찾음"""
    coords = {}
    for q_num in range(min_q, max_q + 2): # 다음 문제 번호까지 찾아서 범위를 확정
        # "41.", " 41.", "\n41." 등 다양한 패턴 대응
        search_term = f"{q_num}."
        rects = page.search_for(search_term)
        if rects:
            # 가장 왼쪽에 있는 것이 문제 번호일 확률이 높음 (1단 구성이므로)
            target = sorted(rects, key=lambda r: r.x0)[0]
            coords[q_num] = target.y0
    return coords

def extract_content_via_gemini(pix_b64, subject, min_q, max_q):
    """AI는 오직 텍스트 내용과 정답, 해설만 추출 (좌표는 무시)"""
    prompt = f"""
이 이미지는 '{subject}' 시험지입니다. {min_q}~{max_q}번 문제의 텍스트와 정답, 해설을 JSON으로 추출하세요.
좌표(bbox)는 제공할 필요 없습니다.

{{
  "results": [
    {{
      "number": {min_q},
      "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
      "answer": "3",
      "explanation": "...",
      "tags": {{ "unit": "...", "sub_unit": "...", "concept": "..." }}
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
        return json.loads(response.text.replace('\\', '\\\\'))
    except: return None

def process_task_physical(task, taxonomy_data, main_db):
    doc = fitz.open(task['pdf'])
    subject = normalize_nfc(task['subject'])
    
    print(f"\n>> {task['year']}년 {subject} 시작 (물리적 텍스트 좌표 엔진 가동)")
    
    for page_num in range(17, len(doc)):
        page = doc[page_num]
        print(f"  Processing Page {page_num+1}...")
        
        # 1. 물리적 좌표 찾기
        q_coords = get_physical_q_coords(page, task['min_q'], task['max_q'])
        if not q_coords: continue
        
        # 2. AI로 내용 추출
        pix_full = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        ai_res = extract_content_via_gemini(encode_image(pix_full), subject, task['min_q'], task['max_q'])
        ai_data = {int(item['number']): item for item in (ai_res if isinstance(ai_res, list) else ai_res.get('results', [])) if ai_res}

        # 3. 물리적 좌표 기반 크롭 및 저장
        sorted_nums = sorted(q_coords.keys())
        for i, q_num in enumerate(sorted_nums):
            if q_num > task['max_q']: continue
            
            y_top = q_coords[q_num] - 15 # 문제 번호 위로 약간 여유
            
            # 본문의 끝(하단 경계)은 선지 "①"이 시작되기 직전으로 설정
            option_one_rects = page.search_for("①")
            y_bottom = 0
            if option_one_rects:
                # 현재 문제 번호(y_top)보다 아래에 있는 가장 가까운 "①" 찾기
                valid_ones = [r.y0 for r in option_one_rects if r.y0 > y_top + 20]
                if valid_ones:
                    y_bottom = min(valid_ones) - 8 # 선지 기호 8px 위까지만 자름
            
            # 만약 "①"을 못 찾았다면 (매우 긴 문제 등), 다음 문제 번호 직전까지
            if y_bottom <= y_top:
                if i + 1 < len(sorted_nums):
                    y_bottom = q_coords[sorted_nums[i+1]] - 50
                else:
                    y_bottom = min(page.rect.height, y_top + 300)
            
            crop_rect = fitz.Rect(0, y_top, page.rect.width, y_bottom)
            pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
            filename = f"tax_2024_s2_{q_num}_body.png"
            pix_q.save(f"images/{filename}")
            
            # AI 데이터와 결합
            item = ai_data.get(q_num, {})
            q_id = f"tax_{task['year']}_{subject}_{q_num}"
            q_data = {
                "year": task['year'], "subject": subject, "number": str(q_num), "question": f"[IMAGE: {filename}]",
                "options": item.get('options', []), "answer": str(item.get('answer', "")),
                "explanation": item.get('explanation', ""), "tags": item.get('tags', {}),
                "exam": "세무사", "id": q_id
            }
            
            # Upsert
            found = False
            for idx, db_q in enumerate(main_db):
                if normalize_nfc(db_q.get("id", "")) == normalize_nfc(q_id):
                    main_db[idx] = q_data
                    found = True; break
            if not found: main_db.append(q_data)
            print(f"    -> Physical Crop & AI Extraction Success: Q{q_num}")

        # 실시간 저장
        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)

def main():
    task = {"pdf": "sources/기출문제/세무사/2024/2024년도 제61회 세무사 1차시험 2교시 시험지 원본(민법).pdf", "year": "2024", "session": 2, "subject": "민법", "min_q": 41, "max_q": 80}
    with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    process_task_physical(task, {}, main_db)
    print("\n🎉 물리적 좌표 엔진으로 2024년 민법 복구 완료!")

if __name__ == "__main__":
    main()
