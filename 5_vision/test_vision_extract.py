import base64
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_questions_from_image(image_path):
    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = """
당신은 시험 문제 추출 전문가입니다. 첨부된 시험지 이미지에서 문제들을 추출하여 JSON 객체로 응답하십시오.
반드시 'results'라는 키를 가진 배열 안에 각 문제 정보를 담으십시오.

각 문제 객체는 다음 필드를 포함해야 합니다:
- number: 문제 번호 (정수)
- question: 문제 내용 (텍스트)
- options: 5개의 보기 리스트 (텍스트)
- answer: 정답 (이미지에 표시가 없다면 공백으로 두거나 추론)
- explanation: 간단한 해설

반드시 JSON 형태로만 응답하십시오.
"""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000,
        "response_format": { "type": "json_object" }
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    image_path = "2026년도 제63회 세무사 1차시험 1교시 시험지 원본_p1.png"
    result = extract_questions_from_image(image_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
