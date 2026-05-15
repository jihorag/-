import os
import json
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def extract_data_from_manual_img(img_path, subject, q_num, year):
    """
    수동 추출된 이미지에서 문제 데이터를 추출합니다.
    """
    with open(img_path, "rb") as f:
        img_data = f.read()
    img_b64 = base64.b64encode(img_data).decode("utf-8")

    prompt = f"""이 이미지는 회계사 시험 {year}년 {subject} 과목 {q_num}번 문제입니다.
이미지에서 보기 ①~⑤를 정확히 읽고, 정답과 해설, 단원 분류를 제공해주세요.
OCR 오류(글자 붙음, 오타 등)는 반드시 문맥에 맞게 교정해주세요.

반드시 아래 JSON 형식만 반환하세요:
{{
  "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
  "answer": "정답번호(숫자만, 모르면 빈 문자열)",
  "explanation": "상세한 해설",
  "tags": {{
    "unit": "재무회계 또는 원가관리회계 또는 정부회계",
    "sub_unit": "세부 단원명",
    "concept": "핵심 개념",
    "difficulty": 3
  }}
}}
"""
    try:
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[
                types.Part.from_bytes(data=base64.b64decode(img_b64), mime_type="image/png"),
                types.Part.from_text(text=prompt)
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"  [Error Q{q_num}] {e}")
        return None

def main():
    db_path = "questions_db.json"
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            main_db = json.load(f)
    except:
        main_db = []

    # 기존 2026 회계학 데이터 제거 (새로고침)
    main_db = [q for q in main_db if not (q.get("exam") == "회계사" and q.get("year") == "2026" and q.get("subject") == "회계학")]

    for q_num in range(1, 51):
        img_name = f"cpa_2026_회계학_{q_num}_body.png"
        img_path = os.path.join("images", img_name)
        
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}")
            continue

        print(f"-> Processing Q{q_num} from manual image...")
        res = extract_data_from_manual_img(img_path, "회계학", q_num, "2026")
        
        if res:
            q_id = f"cpa_2026_회계학_{q_num}"
            
            # Unit Mapping
            unit_raw = res.get("tags", {}).get("unit", "")
            if "원가" in unit_raw or "관리" in unit_raw:
                unit_val = "PART 002 원가관리회계"
            elif "정부" in unit_raw:
                unit_val = "PART 003 정부회계"
            else:
                unit_val = "PART 001 재무회계"

            q_data = {
                "id": q_id,
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
                    "difficulty": res.get("tags", {}).get("difficulty", 3)
                }
            }
            main_db.append(q_data)
            
            # 실시간 저장
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(main_db, f, ensure_ascii=False, indent=2)

    import shutil
    shutil.copy(db_path, "viewer/src/data/questions_db.json")
    print("\n[+] 2026 CPA 회계학 수동 이미지 기반 추출 완료!")

if __name__ == "__main__":
    main()
