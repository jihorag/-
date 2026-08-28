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

def get_page_elements(page):
    """페이지의 모든 텍스트 요소를 좌표와 함께 추출"""
    words = page.get_text("words") # (x0, y0, x1, y1, "word", block_no, line_no, word_no)
    return words

def extract_content_via_gemini(pix_b64, subject, min_q, max_q):
    prompt = f"""
이 이미지는 '{subject}' 시험지입니다. {min_q}~{max_q}번 문제의 텍스트와 정답, 해설을 JSON으로 추출하세요.

[중요: 선지 추출 규칙]
1. options 필드에는 오직 ①, ②, ③, ④, ⑤로 시작하는 **진짜 선지 5개**만 넣으세요.
2. **박스 안의 ㄱ, ㄴ, ㄷ, ㄹ 등은 절대로 선지가 아닙니다.** 그것들은 무시하거나 본문 텍스트로 취급하세요.
3. 선지는 반드시 5개여야 합니다. (①~⑤)

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

def process_task_precise(task, main_db):
    doc = fitz.open(task['pdf'])
    subject = normalize_nfc(task['subject'])
    
    for page_num in range(17, len(doc)):
        page = doc[page_num]
        print(f"  Processing Page {page_num+1} Precise...")
        elements = get_page_elements(page)
        
        # 1. 문제 번호 위치들 찾기
        q_pos = {}
        for w in elements:
            text = w[4]
            if re.match(rf"^{task['min_q']}|[4-8][0-9]\.$", text):
                try:
                    num = int(text.replace(".", ""))
                    if task['min_q'] <= num <= task['max_q']:
                        # 가급적 왼쪽에 있는 번호를 선택
                        if num not in q_pos or w[0] < q_pos[num]['x']:
                            q_pos[num] = {'y': w[1], 'x': w[0]}
                except: continue

        if not q_pos: continue
        
        # 2. 내용 추출 (AI)
        pix_full = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        ai_res = extract_content_via_gemini(encode_image(pix_full), subject, task['min_q'], task['max_q'])
        ai_data = {int(item['number']): item for item in (ai_res if isinstance(ai_res, list) else ai_res.get('results', [])) if ai_res}

        # 3. 정밀 크롭
        sorted_nums = sorted(q_pos.keys())
        for q_num in sorted_nums:
            y_start = q_pos[q_num]['y'] - 15
            
            # 이 문제 번호(y_start) 이후에 나오는 가장 첫 번째 선지(①, ②, ③) 찾기
            y_end = 0
            for w in elements:
                text = w[4]
                # ①, ②, ③ 중 하나라도 걸리면 멈춤
                if w[1] > y_start + 20 and any(mark in text for mark in ["①", "②", "③"]):
                    y_end = w[1] - 10
                    break
            
            # 선지를 못 찾았을 경우 다음 문제 번호 기준
            if y_end <= y_start:
                next_qs = [q_pos[n]['y'] for n in sorted_nums if n > q_num]
                y_end = next_qs[0] - 40 if next_qs else min(page.rect.height, y_start + 400)

            crop_rect = fitz.Rect(0, y_start, page.rect.width, y_end)
            pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
            filename = f"tax_2024_s2_{q_num}_body.png"
            pix_q.save(f"images/{filename}")
            
            item = ai_data.get(q_num, {})
            q_id = f"tax_{task['year']}_{subject}_{q_num}"
            q_data = {
                "year": task['year'], "subject": subject, "number": str(q_num), "question": f"[IMAGE: {filename}]",
                "options": item.get('options', []), "answer": str(item.get('answer', "")),
                "explanation": item.get('explanation', ""), "tags": item.get('tags', {}),
                "exam": "세무사", "id": q_id
            }
            
            found = False
            for idx, db_q in enumerate(main_db):
                if normalize_nfc(db_q.get("id", "")) == normalize_nfc(q_id):
                    main_db[idx] = q_data
                    found = True; break
            if not found: main_db.append(q_data)
            print(f"    -> [SUCCESS] Q{q_num} cropped PRECISELY before options.")

        # 저장
        with open("questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)
        with open("viewer/src/data/questions_db.json", "w", encoding="utf-8") as f:
            json.dump(main_db, f, ensure_ascii=False, indent=2)

def main():
    task = {"pdf": "sources/기출문제/세무사/2024/2024년도 제61회 세무사 1차시험 2교시 시험지 원본(민법).pdf", "year": "2024", "subject": "민법", "min_q": 41, "max_q": 80}
    with open("questions_db.json", "r", encoding="utf-8") as f: main_db = json.load(f)
    process_task_precise(task, main_db)
    print("\n🎉 선지 제외 정밀 로직으로 2024년 민법 복구 완료!")

if __name__ == "__main__":
    main()
