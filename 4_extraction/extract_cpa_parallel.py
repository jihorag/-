import os
import json
import fitz
import re
import unicodedata
from google import genai
from google.genai import types
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def extract_options_text_from_pdf(pdf_path, target_q_num):
    doc = fitz.open(pdf_path)
    found_text = ""
    mid_x = 0
    
    for page in doc:
        if "회계학" not in page.get_text()[:300]: continue
        words = page.get_text("words")
        mid_x = page.rect.width / 2
        q_y = None
        next_q_y = None
        col_rect = None
        
        for w in words:
            if w[4] == f"{target_q_num}.":
                q_y = w[1]
                col_rect = fitz.Rect(0, 0, mid_x, page.rect.height) if w[0] < mid_x else fitz.Rect(mid_x, 0, page.rect.width, page.rect.height)
            elif w[4] == f"{target_q_num + 1}.":
                if q_y is not None:
                    is_same_col = (w[0] < mid_x and col_rect.x1 < mid_x + 10) or (w[0] > mid_x and col_rect.x0 > mid_x - 10)
                    if is_same_col:
                        next_q_y = w[1]
        
        if q_y is not None:
            clip_rect = fitz.Rect(col_rect.x0, q_y, col_rect.x1, next_q_y or page.rect.height)
            found_text = page.get_text("text", clip=clip_rect)
            break
    doc.close()
    return found_text

def refine_options_via_gemini(raw_text, q_num):
    prompt = f"""당신은 전문적인 기출문제 데이터 정제 전문가입니다.
회계사 회계학 {q_num}번 문제의 선지를 정제해 주세요.

[텍스트]
{raw_text}

[규칙]
1. 보기는 ①~⑤로 시작.
2. 금액(￦)은 숫자와 밀착 (예: ￦100,000).
3. 용어 오타 수정.
4. 정답(answer)은 1~5 숫자 추론.

[출력 형식]
JSON:
{{
  "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
  "answer": "정답번호",
  "explanation": "상세 해설",
  "tags": {{ "unit": "재무회계/원가관리회계/정부회계", "sub_unit": "단원명" }}
}}
"""
    try:
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except:
        return None

def process_single_question(q_num, pdf_path):
    print(f"-> Starting Q{q_num}...")
    raw_text = extract_options_text_from_pdf(pdf_path, q_num)
    res = refine_options_via_gemini(raw_text, q_num)
    if res:
        img_name = f"cpa_2026_회계학_{q_num}_body.png"
        tags = res.get("tags") or {}
        unit_raw = tags.get("unit") or ""
        unit_val = "PART 002 원가관리회계" if ("원가" in unit_raw or "관리" in unit_raw) else "PART 001 재무회계"
        if "정부" in unit_raw: unit_val = "PART 003 정부회계"
        
        return {
            "id": f"cpa_2026_회계학_{q_num}",
            "exam": "회계사",
            "year": "2026",
            "subject": "회계학",
            "number": str(q_num),
            "question": f"[IMAGE: {img_name}]",
            "options": res.get("options", []),
            "answer": str(res.get("answer", "")),
            "explanation": res.get("explanation", ""),
            "tags": {
                "subject": "회계학",
                "unit": unit_val,
                "sub_unit": tags.get("sub_unit", ""),
                "concept": tags.get("concept", ""),
                "difficulty": 3
            }
        }
    return None

def main():
    pdf_path = "기출문제/회계사/2026/3교시 회계학(1형)_문제_2026.pdf"
    db_path = "questions_db.json"
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda q: process_single_question(q, pdf_path), range(1, 51)))
    
    final_results = [r for r in results if r is not None]
    
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            main_db = json.load(f)
    except:
        main_db = []
    
    main_db = [q for q in main_db if not (q.get("exam") == "회계사" and q.get("year") == "2026" and q.get("subject") == "회계학")]
    main_db.extend(final_results)
    
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(main_db, f, ensure_ascii=False, indent=2)
    
    import shutil
    shutil.copy(db_path, "viewer/src/data/questions_db.json")
    print(f"\n[+] 병렬 추출 완료! 총 {len(final_results)}개 문항 업데이트됨.")

if __name__ == "__main__":
    main()
