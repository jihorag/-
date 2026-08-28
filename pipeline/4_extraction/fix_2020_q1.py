import os
import json
import fitz
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

def fix_q1_2020_vision():
    pdf_path = "sources/기출문제/세무사/2020/1교시 A형.pdf"
    doc = fitz.open(pdf_path)
    page = doc[0] # Q1 is on page 1
    
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
    img_data = pix.tobytes("png")
    
    client = genai.Client(api_key=gemini_api_key)
    
    prompt = """
이 이미지는 2020년 세무사 1차 재정학 시험지입니다.
'1. 조세의 초과부담에 관한 설명으로 옳은 것은?' 문제의 본문 영역을 찾아주세요.

1. 문제 본문 바운딩 박스 [ymin, xmin, ymax, xmax] (0~1000 scale)
   - ymin: '1.' 번호 바로 위
   - ymax: 첫 번째 선지 ①번 바로 위 (선지는 이미지에 포함되지 않게!)
   - xmin/xmax: 0, 1000 (가로 전체)

반드시 아래 JSON 형식으로만 응답하세요:
{ "bbox": [ymin, 0, ymax, 1000] }
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[types.Part.from_bytes(data=img_data, mime_type="image/png"), prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        res = json.loads(response.text)
        bbox = res['bbox']
        ymin, xmin, ymax, xmax = bbox
        
        page_width = page.rect.width
        page_height = page.rect.height
        crop_rect = fitz.Rect(
            xmin * page_width / 1000,
            ymin * page_height / 1000,
            xmax * page_width / 1000,
            ymax * page_height / 1000
        )
        
        pix_q = page.get_pixmap(clip=crop_rect, matrix=fitz.Matrix(3.0, 3.0))
        img_filename = "tax_2020_s1_1_body.png"
        pix_q.save(f"images/{img_filename}")
        print(f"Fixed image saved: images/{img_filename}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_q1_2020_vision()
