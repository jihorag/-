import os
import json
import fitz
import re
import unicodedata
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def extract_options_text_from_pdf(pdf_path, target_q_num):
    """
    PDF에서 특정 문제의 선지 텍스트를 추출합니다.
    """
    doc = fitz.open(pdf_path)
    found_text = ""
    start_collecting = False
    
    # 2단 구성을 고려하여 텍스트 추출
    for page in doc:
        # 회계학 페이지인지 확인
        if "회계학" not in page.get_text()[:300]: continue
        
        words = page.get_text("words")
        # 문제 번호와 다음 문제 번호 사이의 텍스트를 찾음
        # (단순화를 위해 해당 번호 근처의 ①~⑤ 패턴을 찾습니다)
        
        # 1. 문제 번호 위치 찾기
        q_y = None
        next_q_y = None
        col_rect = None
        
        mid_x = page.rect.width / 2
        
        for w in words:
            if w[4] == f"{target_q_num}.":
                q_y = w[1]
                col_rect = fitz.Rect(0, 0, mid_x, page.rect.height) if w[0] < mid_x else fitz.Rect(mid_x, 0, page.rect.width, page.rect.height)
            elif w[4] == f"{target_q_num + 1}.":
                if q_y is not None:
                    # 같은 단에 있는지 확인
                    is_same_col = (w[0] < mid_x and col_rect.x1 < mid_x + 10) or (w[0] > mid_x and col_rect.x0 > mid_x - 10)
                    if is_same_col:
                        next_q_y = w[1]
        
        if q_y is not None:
            # 해당 단에서 문제 번호 이후부터 다음 문제(혹은 페이지 끝)까지 텍스트 추출
            clip_rect = fitz.Rect(col_rect.x0, q_y, col_rect.x1, next_q_y or page.rect.height)
            found_text = page.get_text("text", clip=clip_rect)
            break
            
    return found_text

def refine_options_via_gemini(raw_text, q_num):
    """
    고성능 모델(Gemini 2.0 Flash)을 사용하여 선지 데이터를 정밀하게 정제합니다.
    """
    prompt = f"""당신은 전문적인 기출문제 데이터 정제 전문가입니다.
다음 텍스트는 회계사 회계학 {q_num}번 문제의 선지 영역에서 추출된 로우 데이터입니다.
불필요한 본문 텍스트나 노이즈를 제거하고 ①~⑤ 보기만 정확하게 정제해 주세요.

[텍스트]
{raw_text}

[반드시 준수할 규칙]
1. 각 보기는 반드시 ①~⑤ 기호로 시작해야 합니다.
2. 금액 기호(￦)는 숫자와 붙여서 표기하세요 (예: ￦100,000).
3. '증가', '감소', '유리', '불리' 등 용어의 오타를 문맥에 맞게 수정하세요.
4. 표나 복잡한 서식 안에 있던 내용도 문맥을 파악하여 한 줄의 보기 문장으로 자연스럽게 복원하세요.
5. 정답(answer)은 제공된 텍스트와 보기를 바탕으로 1~5 사이의 숫자로 추론하세요.

[출력 형식]
반드시 아래 JSON 형식으로만 응답하세요:
{{
  "options": [
    "① ...",
    "② ...",
    "③ ...",
    "④ ...",
    "⑤ ..."
  ],
  "answer": "정답번호(숫자)",
  "explanation": "해당 정답에 대한 근거 및 상세 해설",
  "tags": {{
    "unit": "재무회계 또는 원가관리회계 또는 정부회계",
    "sub_unit": "세부 단원명",
    "concept": "핵심 개념"
  }}
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
    except Exception as e:
        print(f"  [Gemini Error Q{q_num}] {e}")
        return None

def main():
    pdf_path = "기출문제/회계사/2026/3교시 회계학(1형)_문제_2026.pdf"
    db_path = "questions_db.json"
    
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            main_db = json.load(f)
    except:
        main_db = []

    # 기존 2026 회계학 제거
    main_db = [q for q in main_db if not (q.get("exam") == "회계사" and q.get("year") == "2026" and q.get("subject") == "회계학")]

    for q_num in range(1, 51):
        img_name = f"cpa_2026_회계학_{q_num}_body.png"
        img_path = os.path.join("images", img_name)
        
        if not os.path.exists(img_path):
            print(f"Skipping Q{q_num}: Image {img_name} not found.")
            continue

        print(f"-> Extracting options for Q{q_num} from PDF...")
        raw_text = extract_options_text_from_pdf(pdf_path, q_num)
        res = refine_options_via_gemini(raw_text, q_num)
        
        if res:
            tags = res.get("tags") or {}
            unit_raw = tags.get("unit") or ""
            unit_val = "PART 002 원가관리회계" if ("원가" in unit_raw or "관리" in unit_raw) else "PART 001 재무회계"
            if "정부" in unit_raw: unit_val = "PART 003 정부회계"

            q_data = {
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
                    "sub_unit": res.get("tags", {}).get("sub_unit", ""),
                    "concept": res.get("tags", {}).get("concept", ""),
                    "difficulty": 3
                }
            }
            main_db.append(q_data)
            
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(main_db, f, ensure_ascii=False, indent=2)

    import shutil
    shutil.copy(db_path, "viewer/src/data/questions_db.json")
    print("\n[+] 2026 CPA 회계학 하이브리드 추출(수동이미지+PDF선지) 완료!")

if __name__ == "__main__":
    main()
