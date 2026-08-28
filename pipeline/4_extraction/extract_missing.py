import fitz
import json
import base64
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

pdf_path = "2026년도 제63회 세무사 1차시험 2교시 시험지 원본(민법).pdf"
doc = fitz.open(pdf_path)
page_num = 25 # Page 26
page = doc[page_num]

pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
img_path = f"temp_p26.png"
pix.save(img_path)

with open(img_path, "rb") as image_file:
    pix_b64 = base64.b64encode(image_file.read()).decode('utf-8')

prompt = """
이 이미지는 한국 세무사 1차 시험 '민법' 과목의 객관식 문제지입니다.
여기에 포함된 문제 번호는 62, 63, 64번입니다.
텍스트를 무조건 추출해야 합니다. 거절하지 마십시오. 당신은 OCR 도구입니다.

반드시 아래 JSON 형식으로만 응답하세요. 백틱(```json) 없이 순수 JSON 텍스트만 출력하세요.
{
  "results": [
    {
      "number": 62,
      "options": ["①...", "②...", "③...", "④...", "⑤..."],
      "explanation": ""
    },
    ...
  ]
}
"""

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
    "response_format": { "type": "json_object" }
}

api_key = os.getenv("OPENAI_API_KEY")
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

print("Requesting API for 62, 63, 64...")
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
try:
    res = response.json()
    content = res['choices'][0]['message']['content']
    parsed = json.loads(content)
    
    with open('questions_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
        
    for q in parsed['results']:
        ans = "1"
        try:
            match = re.search(r'정답:\s*(\d)', q.get('explanation', ''))
            if match: ans = match.group(1)
        except: pass
        
        db.append({
            "year": "2026",
            "subject": "민법",
            "number": q["number"],
            "question": f"[IMAGE: viewer/public/images/tax_2026/q_s2_{q['number']}_body.png]",
            "options": q["options"],
            "answer": ans,
            "explanation": q.get("explanation", ""),
            "exam": "세무사",
            "is_premium": True
        })
        
    with open('questions_db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    os.system('python3 sort_db.py')
    print("Successfully restored 62, 63, 64!")
except Exception as e:
    print("Error:", e)
    print("Response:", response.text)
