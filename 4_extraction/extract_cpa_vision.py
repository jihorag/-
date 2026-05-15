import os
import json
import fitz
import re
import unicodedata
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv
import io
from PIL import Image, ImageFile, ImageChops
Image.MAX_IMAGE_PIXELS = None  # DecompressionBomb 제한 해제

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def normalize_nfc(text):
    return unicodedata.normalize('NFC', text)

def img_to_base64(pix):
    img_bytes = pix.tobytes("png")
    return base64.b64encode(img_bytes).decode("utf-8")

def detect_questions_in_column(col_image_b64, col_width, col_height):
    """
    Vision으로 한 단(column) 이미지 안의 문제 번호와 Y좌표 범위를 감지합니다.
    문제 번호(굵게 표시된 N.)를 직접 읽어냅니다.
    """
    prompt = """이 이미지는 회계사 시험 기출문제지의 한 단(column)입니다.
각 문제는 굵은 글씨로 시작하는 "N." (숫자 + 점) 형태로 시작합니다.
이미지 전체 높이를 1000으로 기준으로, 각 문제의 시작 Y위치를 구해주세요.

반드시 아래 JSON 형식만 반환하세요:
{
  "questions": [
    {"number": 1, "y_start_ratio": 0.05},
    {"number": 2, "y_start_ratio": 0.45}
  ]
}

주의사항:
- number는 실제 시험지에 인쇄된 문제 번호(정수)입니다
- y_start_ratio는 이미지 상단을 0.0, 하단을 1.0으로 보았을 때 해당 문제가 시작하는 상대 위치입니다
- 표 안의 숫자나 보기 번호(①②③)는 문제 번호가 아닙니다
- 문제가 없으면 {"questions": []} 을 반환하세요
"""
    try:
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[
                types.Part.from_bytes(data=base64.b64decode(col_image_b64), mime_type="image/png"),
                types.Part.from_text(text=prompt)
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"  [Vision Error] {e}")
        return {"questions": []}

def extract_question_data(q_image_b64, subject, q_num):
    """
    문제 이미지에서 보기, 정답, 해설, 단원 태그를 추출합니다.
    """
    prompt = f"""이 이미지는 회계사 시험 {subject} 과목 {q_num}번 문제입니다.
이미지에서 보기 ①~⑤를 정확히 읽고, 정답과 해설, 단원 분류를 제공해주세요.
OCR 오류(글자 붙음, 오타 등)는 반드시 교정해주세요.

반드시 아래 JSON 형식만 반환하세요:
{{
  "options": ["① ...", "② ...", "③ ...", "④ ...", "⑤ ..."],
  "answer": "정답번호(숫자만, 모르면 빈 문자열)",
  "explanation": "상세한 해설",
  "tags": {{
    "unit": "미시경제학 또는 거시경제학 또는 재정학 (경제학인 경우) / 재무회계 또는 원가관리회계 (회계학인 경우)",
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
                types.Part.from_bytes(data=base64.b64decode(q_image_b64), mime_type="image/png"),
                types.Part.from_text(text=prompt)
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"  [Data Extract Error] {e}")
        return {"options": ["①", "②", "③", "④", "⑤"], "answer": "", "explanation": "", "tags": {}}

def process_cpa_file_vision(pdf_path, year, target_subjects, main_db, existing_ids):
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n>> [Vision Mode] Processing {year} CPA: {os.path.basename(pdf_path)}...")
    doc = fitz.open(pdf_path)

    current_subject = None
    SCALE = 2.0  # 고해상도 렌더링 (3.0은 PIL 메모리 한계 초과)

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text()

        # 페이지 상단 헤더에서 과목 감지
        header_text = page_text[:200]
        page_subject = None
        for sub in target_subjects:
            if sub in header_text:
                page_subject = sub
                break

        if page_subject:
            current_subject = page_subject

        if not current_subject or current_subject not in target_subjects:
            continue

        db_subject = "경제학" if current_subject == "경제원론" else current_subject

        print(f"  [Page {page_num+1}] Subject: {db_subject}")

        # 전체 페이지를 고해상도 이미지로 렌더링
        mat = fitz.Matrix(SCALE, SCALE)
        full_pix = page.get_pixmap(matrix=mat)
        full_w = full_pix.width
        full_h = full_pix.height

        mid_x = full_w // 2

        # PIL로 변환
        img = Image.frombytes("RGB", [full_w, full_h], full_pix.samples)

        # 좌/우 컬럼으로 분할
        left_col_img = img.crop((0, 0, mid_x, full_h))
        right_col_img = img.crop((mid_x, 0, full_w, full_h))

        for col_img, col_name, col_x_offset in [
            (left_col_img, "left", 0),
            (right_col_img, "right", mid_x)
        ]:
            # PIL 이미지를 base64로 변환
            buf = io.BytesIO()
            col_img.save(buf, format="PNG")
            col_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

            col_w, col_h = col_img.size

            # Vision으로 문제 번호와 Y위치 감지
            detect_result = detect_questions_in_column(col_b64, col_w, col_h)
            questions_info = detect_result.get("questions", [])

            if not questions_info:
                continue

            print(f"    [{col_name} col] Detected questions: {[q['number'] for q in questions_info]}")

            for i, q_info in enumerate(questions_info):
                q_num = q_info["number"]
                y_start_ratio = q_info["y_start_ratio"]

                q_id = f"cpa_{year}_{db_subject}_{q_num}"
                if normalize_nfc(q_id) in existing_ids:
                    print(f"    -> [SKIP] {q_id} already exists")
                    continue

                # Y 좌표 계산 (약간의 여백 추가)
                y_start_px = max(0, int(y_start_ratio * col_h) - 5)

                # 다음 문제 시작 위치 또는 페이지 끝까지
                if i + 1 < len(questions_info):
                    y_end_px = int(questions_info[i+1]["y_start_ratio"] * col_h) - 5
                else:
                    y_end_px = col_h

                # 문제 이미지 크롭
                q_crop = col_img.crop((0, y_start_px, col_w, y_end_px))

                # 너무 작은 이미지는 스킵
                if q_crop.height < 30:
                    print(f"    -> [SKIP] Q{q_num} image too small")
                    continue

                # 이미지 저장 전 여백 제거 (Auto-trim)
                # 배경색(흰색)이 아닌 부분의 경계 상자를 찾음
                bg = Image.new(q_crop.mode, q_crop.size, (255, 255, 255))
                diff = ImageChops.difference(q_crop, bg)
                bbox = diff.getbbox()
                if bbox:
                    # 상하좌우 5px 여백 추가 후 크롭
                    left, upper, right, lower = bbox
                    q_crop = q_crop.crop((
                        max(0, left - 10), 
                        max(0, upper - 10), 
                        min(q_crop.width, right + 10), 
                        min(q_crop.height, lower + 10)
                    ))

                # 이미지 저장
                img_filename = f"cpa_{year}_{db_subject}_{q_num}_body.png"
                img_path = os.path.join(output_dir, img_filename)
                q_crop.save(img_path)

                # 이미지 base64 변환
                buf2 = io.BytesIO()
                q_crop.save(buf2, format="PNG")
                q_b64 = base64.b64encode(buf2.getvalue()).decode("utf-8")

                print(f"    -> Extracting Q{q_num} ({col_name} col, y={y_start_px}~{y_end_px})...")

                # Vision으로 보기, 해설, 태그 추출
                llm_res = extract_question_data(q_b64, db_subject, q_num)

                options = llm_res.get("options", ["①", "②", "③", "④", "⑤"])

                # 단원 매핑
                unit_raw = llm_res.get("tags", {}).get("unit", "")
                if db_subject == "경제학":
                    if "미시" in unit_raw:
                        unit_val = "PART 001 미시경제학"
                    elif "거시" in unit_raw:
                        unit_val = "PART 002 거시경제학"
                    else:
                        unit_val = "PART 003 재정학"
                else:  # 회계학
                    if "원가" in unit_raw or "관리" in unit_raw:
                        unit_val = "PART 002 원가관리회계"
                    else:
                        unit_val = "PART 001 재무회계"

                q_data = {
                    "id": q_id,
                    "exam": "회계사",
                    "year": str(year),
                    "subject": db_subject,
                    "number": str(q_num),
                    "question": f"[IMAGE: {img_filename}]",
                    "options": options,
                    "answer": str(llm_res.get("answer", "")),
                    "explanation": llm_res.get("explanation", ""),
                    "tags": {
                        "subject": db_subject,
                        "unit": unit_val,
                        "sub_unit": llm_res.get("tags", {}).get("sub_unit", ""),
                        "concept": llm_res.get("tags", {}).get("concept", ""),
                        "difficulty": llm_res.get("tags", {}).get("difficulty", 3)
                    }
                }

                main_db.append(q_data)
                existing_ids.add(normalize_nfc(q_id))

                # 실시간 저장
                with open("questions_db.json", "w", encoding="utf-8") as f:
                    json.dump(main_db, f, ensure_ascii=False, indent=2)

def main():
    db_path = "questions_db.json"
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            main_db = json.load(f)
    except:
        main_db = []

    # 기존 CPA 2026 잘못 추출된 것 제거
    before = len(main_db)
    main_db = [q for q in main_db if not (q.get("exam") == "회계사" and q.get("year") == "2026")]
    removed = before - len(main_db)
    print(f"[*] Removed {removed} old 2026 CPA entries for re-extraction.")

    existing_ids = {normalize_nfc(q["id"]) for q in main_db if "id" in q}

    tasks = [
        {
            "pdf": "기출문제/회계사/2026/1교시 경영학 경제원론(1형)_문제_2026.pdf",
            "year": "2026",
            "subjects": ["경제원론"]
        },
        {
            "pdf": "기출문제/회계사/2026/3교시 회계학(1형)_문제_2026.pdf",
            "year": "2026",
            "subjects": ["회계학"]
        }
    ]

    for t in tasks:
        process_cpa_file_vision(t["pdf"], t["year"], t["subjects"], main_db, existing_ids)

    import shutil
    shutil.copy("questions_db.json", "viewer/src/data/questions_db.json")
    shutil.copy("questions_db.json", "viewer/src/data/questions_tax.json")
    print("\n[+] 2026년 회계사 Vision 재추출 완료 및 DB 동기화 성공!")

if __name__ == "__main__":
    main()
