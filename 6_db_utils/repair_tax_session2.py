import base64
import requests
import json
import os
import fitz
from dotenv import load_dotenv
import time
import re
import sys

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Set up logging to both console and file
log_file = open("repair.log", "w", encoding="utf-8")
def log_print(msg):
    print(msg)
    log_file.write(msg + "\n")
    log_file.flush()

def encode_image(pix):
    return base64.b64encode(pix.tobytes("png")).decode('utf-8')

def extract_via_gpt55(pix_b64):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    prompt = """첨부된 시험지 이미지에서 각 문제의 '선지(①~⑤) 전체 텍스트', '정답', '해설'을 추출하십시오. 
지문 박스(ㄱ,ㄴ,ㄷ...) 내용은 제외하고 하단의 ①~⑤ 선택지만 추출하십시오.
반드시 올바른 JSON 형식으로 응답하십시오. (예: {"results":[{"number":1, "options":["①...", ...], "answer":"1", "explanation":""}]})"""
    
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
        ]
    }
    try:
        # Added a 90-second timeout so it doesn't hang forever, but gives the AI enough time
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=90)
        res = response.json()
        if 'error' in res:
            log_print(f"API Error Response: {res['error']}")
        return res
    except Exception as e:
        log_print(f"API Request Failed (Timeout or Error): {e}")
        return None

def main():
    log_print("🚀 실시간 복구 스크립트 가동 시작!")
    pdf_path = "2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf"
    doc = fitz.open(pdf_path)
    db_json_path = "questions_db.json"
    
    with open(db_json_path, "r", encoding="utf-8") as f:
        db_data = json.load(f)
        
    existing_nums = [q['number'] for q in db_data if q.get('year') == '2026' and q.get('exam') == '세무사' and q.get('subject') in ['회계학개론', '민법']]
    missing_nums = [i for i in range(1, 81) if i not in existing_nums]
    
    if not missing_nums:
        log_print("✅ 80문제가 모두 완료되었습니다.")
        return
        
    log_print(f"🚨 총 {len(missing_nums)}문제 복구 필요: {missing_nums}")

    symbol_map = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5', '가': '1', '나': '2', '다': '3', '라': '4', '마': '5'}
    added_count = 0

    for page_num in range(len(doc)): 
        page = doc[page_num]
        
        text_items = []
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        txt = s["text"].strip()
                        if txt: text_items.append({"text": txt, "bbox": s["bbox"]})
        
        text_items.sort(key=lambda x: x["bbox"][1])
        q_headers = [i for i in text_items if re.match(r"^\d+\.?$", i["text"]) and i["bbox"][0] < 150]
        q_headers.sort(key=lambda x: x["bbox"][1])
        
        opts_starts = [i for i in text_items if "①" in i["text"]]
        
        page_crops = []
        for idx, q in enumerate(q_headers):
            try:
                q_num = int(re.sub(r"\D", "", q["text"]))
                if q_num not in missing_nums: continue 
                
                y0 = q["bbox"][1] - 12
                my_opt = next((o for o in opts_starts if o["bbox"][1] > y0), None)
                y1 = my_opt["bbox"][1] - 4 if my_opt else (q_headers[idx+1]["bbox"][1]-15 if idx+1 < len(q_headers) else page.rect.height-70)
                
                pix = page.get_pixmap(clip=fitz.Rect(0, y0, page.rect.width, y1), matrix=fitz.Matrix(2.5, 2.5))
                img_path = f"images/tax_2026/q_s2_{q_num}_body.png"
                pix.save(os.path.join("viewer/public", img_path))
                page_crops.append({"number": q_num, "img": img_path})
            except: continue

        if not page_crops: continue
        log_print(f"\n▶️ [페이지 {page_num + 1}] 복구 중... 대상: {[c['number'] for c in page_crops]}")

        res = extract_via_gpt55(encode_image(page.get_pixmap(matrix=fitz.Matrix(2,2))))
        
        if res and 'choices' in res:
            try:
                raw_content = res['choices'][0]['message']['content']
                if raw_content.startswith('```json'): raw_content = raw_content[7:]
                if raw_content.startswith('```'): raw_content = raw_content[3:]
                if raw_content.endswith('```'): raw_content = raw_content[:-3]
                raw_content = raw_content.strip()
                
                try:
                    data = json.loads(raw_content)
                except json.JSONDecodeError:
                    log_print(f"❌ JSON 파싱 실패! 모델이 이상한 값을 줬습니다: {raw_content[:100]}...")
                    continue

                gpt_results = data.get('results', [])
                
                for i, crop in enumerate(page_crops):
                    match = None
                    for g in gpt_results:
                        g_num_str = re.sub(r"\D", "", str(g.get('number', '')))
                        if g_num_str and int(g_num_str) == crop['number']:
                            match = g
                            break
                    
                    if not match and len(gpt_results) == len(page_crops):
                        match = gpt_results[i]

                    if match:
                        subject = "회계학개론" if crop['number'] <= 40 else "민법"
                        ans = str(match.get('answer', ''))
                        if ans in symbol_map: ans = symbol_map[ans]
                        elif '.' in ans: ans = ans.replace('.', '').strip()

                        db_data.append({
                            "year": "2026",
                            "subject": subject,
                            "number": crop['number'],
                            "question": f"[IMAGE: {crop['img']}]",
                            "options": match.get('options', []),
                            "answer": ans,
                            "explanation": match.get('explanation', ""),
                            "exam": "세무사",
                            "is_premium": True
                        })
                        added_count += 1
                        log_print(f"✅ 완료: {subject} Q{crop['number']}")
            except Exception as e:
                log_print(f"❌ 에러 발생 (페이지 {page_num+1}): {e}")

        # Save incrementally
        with open(db_json_path, "w", encoding="utf-8") as f:
            json.dump(db_data, f, ensure_ascii=False, indent=2)
        os.system('cp questions_db.json viewer/src/data/questions_db.json')
        
        time.sleep(1)

    log_print(f"\n🎉 최종 복구 완료! 총 {added_count}문제가 성공적으로 채워졌습니다.")
    log_file.close()

if __name__ == "__main__":
    main()
