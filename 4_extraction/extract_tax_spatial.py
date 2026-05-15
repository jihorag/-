import base64
import json
import os
import sys
import fitz
from dotenv import load_dotenv
import time
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_spatial_via_gemini(pix_b64, subject_taxonomy, subject):
    prompt = f"""
첨부된 이미지에는 여러 개의 '{subject}' 객관식 기출문제가 있습니다. 
각 문제에 대해 아래 JSON 형식으로 모든 데이터를 완벽하게 추출하십시오.

특별 지시사항 (Spatial Bounding Box):
- 각 문제의 본문(문제 텍스트, 표, 그래프 등)의 위치를 `bbox` 필드에 [ymin, xmin, ymax, xmax] 형식으로 반환하십시오.
- 좌표는 이미지 전체를 기준으로 0에서 1000 사이의 정수로 정규화된 값입니다. (ymin이 상단, ymax가 하단)
- ⚠️ 매우 중요: 이 `bbox` 영역에는 **절대로 ①~⑤ 선지 부분이 포함되어서는 안 됩니다!** 문제 본문과 자료(표 등)까지만 포함하고, 선지가 시작되기 직전에서 ymax를 끊으십시오.

[과목: {subject} 의 목차 분류 체계 참고]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

반드시 'results' 키를 가진 아래 JSON 배열 형식으로만 응답하십시오:
{{
  "results": [
    {{
      "number": 1,
      "bbox": [150, 50, 400, 950],
      "options": ["① 내용", "② 내용", "③ 내용", "④ 내용", "⑤ 내용"],
      "answer": "정답번호(숫자만)",
      "explanation": "해설",
      "tags": {{
        "unit": "대단원 (참고 목차 기반)",
        "sub_unit": "중단원",
        "concept": "핵심 개념",
        "difficulty": 3,
        "question_type": "유형"
      }}
    }}
  ]
}}
"""
    try:
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents=[
                prompt,
                types.Part.from_bytes(data=base64.b64decode(pix_b64), mime_type="image/png")
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                thinking_config={"thinking_level": "HIGH"}
            )
        )
        json_text = response.text.replace('\\', '\\\\')
        res = json.loads(json_text)
        return res if isinstance(res, list) else res
    except Exception as e:
        print(f"[GEMINI API Error] {e}")
        return None

def main():
    pdf_path = "기출문제/세무사/2026/2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf"
    year = "2026"
    session = 2
    
    # taxonomy 로드
    taxonomy_data = {}
    if os.path.exists("taxonomy.json"):
        with open("taxonomy.json", "r", encoding="utf-8") as f:
            taxonomy_data = json.load(f)
            
    doc = fitz.open(pdf_path)
    output_json_path = f"tax_{year}_s{session}_spatial_extracted.json"
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    
    all_questions = []

    for page_num in range(18, len(doc)): 
        page = doc[page_num]
        print(f"[{year}년 {session}교시] Processing page {page_num + 1}/{len(doc)} via SPATIAL VISION...")
        
        # 페이지 전체를 초고해상도(3배수) 이미지로 변환하여 OCR 정확도 향상
        pix_page = page.get_pixmap(matrix=fitz.Matrix(3,3))
        pix_b64 = encode_image(pix_page)
        
        subject = "민법"
        subject_taxonomy = taxonomy_data.get(subject, "목차 없음")
        
        res = extract_spatial_via_gemini(pix_b64, subject_taxonomy, subject)
        
        if res and 'results' in res:
            gpt_results = res.get('results', [])
            
            for item in gpt_results:
                q_num = item.get('number')
                
                # 민법은 41번~80번
                if not isinstance(q_num, int) or q_num < 41 or q_num > 80:
                    continue
                    
                bbox = item.get('bbox')
                if not bbox or len(bbox) != 4:
                    print(f"  -> Q{q_num} bbox missing or invalid!")
                    continue
                
                ymin, xmin, ymax, xmax = bbox
                
                # 정규화된 0~1000 좌표를 실제 PDF 페이지 좌표로 변환
                page_height = page.rect.height
                page_width = page.rect.width
                
                y_top = (ymin / 1000.0) * page_height
                y_bottom = (ymax / 1000.0) * page_height
                
                # 안전장치 및 여백(Padding) 적용
                y_top = max(0, y_top - 5)
                y_bottom = min(page_height, y_bottom + 5)
                
                crop_rect = fitz.Rect(0, y_top, page_width, y_bottom)
                
                try:
                    pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
                    filename = f"tax_{year}_s{session}_{q_num}_body.png"
                    pix_q.save(os.path.join(output_dir, filename))
                    
                    all_questions.append({
                        "year": year,
                        "subject": subject,
                        "number": str(q_num),
                        "question": f"[IMAGE: {filename}]",
                        "options": item.get('options', []),
                        "answer": str(item.get('answer', "")),
                        "explanation": item.get('explanation', ""),
                        "tags": item.get('tags', {}),
                        "exam": "세무사"
                    })
                    print(f"  -> Cropped & Extracted Q{q_num} (y_top:{int(y_top)}, y_bottom:{int(y_bottom)})")
                except Exception as e:
                    print(f"  -> Error cropping Q{q_num}: {e}")

        # 중간 저장
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(all_questions, f, ensure_ascii=False, indent=2)
            
    print(f"\n공간 좌표(Spatial Vision) 기반 {subject} 41~80번 추출 완료! 결과: {output_json_path}")
    
    # 메인 DB에 바로 병합
    db_path = "questions_db.json"
    viewer_db_path = "viewer/src/data/questions_db.json"
    
    with open(db_path, "r", encoding="utf-8") as f:
        main_db = json.load(f)
        
    updated = 0
    for ext_q in all_questions:
        q_id = f"tax_{ext_q['year']}_{ext_q['subject']}_{ext_q['number']}"
        found = False
        for db_q in main_db:
            if db_q.get("id") == q_id:
                db_q["options"] = ext_q.get("options", db_q.get("options"))
                db_q["answer"] = ext_q.get("answer", db_q.get("answer"))
                db_q["explanation"] = ext_q.get("explanation", db_q.get("explanation"))
                db_q["tags"] = ext_q.get("tags", db_q.get("tags"))
                found = True
                updated += 1
                break
        if not found:
            ext_q["id"] = q_id
            main_db.append(ext_q)
            updated += 1
            
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(main_db, f, ensure_ascii=False, indent=2)
    with open(viewer_db_path, "w", encoding="utf-8") as f:
        json.dump(main_db, f, ensure_ascii=False, indent=2)
        
    print(f"메인 DB에 {updated}건 업데이트 완료!")

if __name__ == "__main__":
    main()
