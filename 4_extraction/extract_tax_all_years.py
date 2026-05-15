import base64
import requests
import json
import os
import sys
import fitz
from dotenv import load_dotenv
import time
import re
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

gpt_fallback_until = 0

def get_active_api():
    if time.time() < gpt_fallback_until:
        return "gpt"
    return "gemini" if gemini_api_key else "gpt"

def handle_api_error(api_name, e):
    global gpt_fallback_until
    print(f"[{api_name.upper()} API Error] {e}")
    if api_name == "gemini":
        print("=> Switching to GPT-4o for 5 minutes due to Gemini error.")
        gpt_fallback_until = time.time() + 300

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_via_ai(pix_b64, prompt):
    active_api = get_active_api()
    
    if active_api == "gemini":
        try:
            client = genai.Client(api_key=gemini_api_key)
            # Thinking 모드를 활성화한 최신 SDK 호출
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
            return json.loads(response.text)
        except Exception as e:
            handle_api_error("gemini", e)
            active_api = "gpt"
            
    if active_api == "gpt":
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{pix_b64}"}}
                    ]
                }
            ],
            "max_tokens": 4000,
            "response_format": { "type": "json_object" }
        }
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            res = response.json()
            return json.loads(res['choices'][0]['message']['content'])
        except Exception as e:
            handle_api_error("gpt", e)
            return None

def main():
    if len(sys.argv) < 4:
        print("사용법: python3 extract_tax_all_years.py <PDF경로> <연도> <교시: 1 또는 2>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    year = sys.argv[2]
    session = int(sys.argv[3])

    if not os.path.exists(pdf_path):
        print(f"파일을 찾을 수 없습니다: {pdf_path}")
        sys.exit(1)

    # 분류체계(Taxonomy) 로드
    taxonomy_data = {}
    if os.path.exists("taxonomy.json"):
        with open("taxonomy.json", "r", encoding="utf-8") as f:
            taxonomy_data = json.load(f)

    doc = fitz.open(pdf_path)
    output_json_path = f"tax_{year}_s{session}_extracted.json"
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    
    last_q_num = 0
    all_questions = []

    for page_num in range(len(doc)): 
        page = doc[page_num]
        print(f"[{year}년 {session}교시] Processing page {page_num + 1}/{len(doc)}...")
        
        text_items = []
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text_items.append({"text": s["text"].strip(), "bbox": s["bbox"]})
        
        q_starts = []
        opt_starts = []
        for item in text_items:
            if re.match(r"^\d+\.", item["text"]) and item["bbox"][0] < page.rect.width / 2 + 50:
                q_starts.append(item)
            if "①" in item["text"]:
                opt_starts.append(item)
        
        q_starts.sort(key=lambda x: x["bbox"][1])
        opt_starts.sort(key=lambda x: x["bbox"][1])
        
        page_width = page.rect.width
        page_crops = []
        
        for idx, q in enumerate(q_starts):
            try:
                q_num = int(re.search(r"^\d+", q["text"]).group())
                if q_num > 80: continue
                
                # 가짜 문제 번호(표 내부의 1., 2. 등)가 이전 문제 번호보다 작거나 같으면 무시
                if q_num <= last_q_num:
                    continue
                last_q_num = q_num
                
                y_top = q["bbox"][1] - 8
                my_opt = next((o for o in opt_starts if o["bbox"][1] > y_top), None)
                
                x0 = 0
                x1 = page_width
                
                if my_opt:
                    y_bottom = my_opt["bbox"][1] - 2
                else:
                    y_bottom = q_starts[idx+1]["bbox"][1] - 10 if idx+1 < len(q_starts) else page.rect.height - 50
                
                crop_rect = fitz.Rect(x0, y_top, x1, y_bottom)
                pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(2.5, 2.5))
                
                filename = f"tax_{year}_s{session}_{q_num}_body.png"
                pix_q.save(os.path.join(output_dir, filename))
                
                page_crops.append({"number": q_num, "img": filename, "rect": crop_rect})
            except Exception as e:
                continue

        if not page_crops: continue

        # 현재 페이지의 주 과목 파악 (페이지 첫 문제 번호 기준)
        first_q_num = page_crops[0]['number']
        if session == 1:
            subject = "재정학" if first_q_num <= 40 else "세법학개론"
        else:
            subject = "회계학" if first_q_num <= 40 else "민법"

        # 타겟 과목 필터링 (세법학개론 등 불필요한 과목은 스킵하여 API 비용 절감)
        target_subjects = ["재정학", "회계학", "민법"]
        if subject not in target_subjects:
            # 페이지 내 모든 문제가 타겟 과목이 아니라면 통째로 스킵
            all_non_target = True
            for crop in page_crops:
                q_num = crop['number']
                if session == 1:
                    sub = "재정학" if q_num <= 40 else "세법학개론"
                else:
                    sub = "회계학" if q_num <= 40 else "민법"
                if sub in target_subjects:
                    all_non_target = False
                    break
            
            if all_non_target:
                print(f"  -> Skipping page (Contains only {subject})")
                continue

        subject_taxonomy = taxonomy_data.get(subject, "등록된 목차가 없습니다. 내용을 기반으로 적절히 생성하세요.")

        prompt = f"""
첨부된 이미지에서 각 문제의 '선지(①~⑤)'와 '정답', '해설'을 추출하고, 
해당 과목({subject})의 내용에 맞게 분류 태깅(목차)을 동시에 수행하십시오.

[과목: {subject} 의 목차 분류 체계 참고]
{json.dumps(subject_taxonomy, ensure_ascii=False)}

결과는 반드시 'results' 키를 가진 아래 JSON 배열 형식으로 응답하십시오:
{{
  "results": [
    {{
      "number": 1,
      "options": ["① 실제내용", "② 실제내용", "③ 실제내용", "④ 실제내용", "⑤ 실제내용"],
      "answer": "정답번호(숫자만)",
      "explanation": "해설",
      "tags": {{
        "unit": "대단원 (참고 목차 기반)",
        "sub_unit": "중단원 (참고 목차 기반)",
        "concept": "핵심 개념",
        "difficulty": 3,
        "question_type": "유형 (계산형, 이론형 등)"
      }}
    }}
  ]
}}
"""

        pix_page = page.get_pixmap(matrix=fitz.Matrix(2,2))
        pix_b64 = encode_image(pix_page)
        
        res = extract_via_ai(pix_b64, prompt)
        
        if res and 'results' in res:
            try:
                gpt_results = res.get('results', [])
                
                for crop in page_crops:
                    match = next((g for g in gpt_results if str(g.get('number', '')) == str(crop['number'])), None)
                    
                    if match:
                        q_num = crop['number']
                        if session == 1:
                            sub = "재정학" if q_num <= 40 else "세법학개론"
                        else:
                            sub = "회계학" if q_num <= 40 else "민법"
                            
                        if sub not in target_subjects:
                            continue
                        
                        all_questions.append({
                            "year": year,
                            "subject": sub,
                            "number": str(q_num),
                            "question": f"[IMAGE: {crop['img']}]",
                            "options": match.get('options', []),
                            "answer": match.get('answer', ""),
                            "explanation": match.get('explanation', ""),
                            "tags": match.get('tags', {}),
                            "exam": "세무사"
                        })
                        print(f"  -> Extracted & Tagged Q{q_num} ({sub}) using {get_active_api().upper()}")
            except Exception as e:
                print(f"  -> Failed to parse AI output: {e}")

        # 중간 저장
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(all_questions, f, ensure_ascii=False, indent=2)
            
        time.sleep(1)

    print(f"\n{year}년 {session}교시 추출 및 태깅 완료! 결과: {output_json_path}")

if __name__ == "__main__":
    main()
