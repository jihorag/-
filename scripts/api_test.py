import google.generativeai as genai
import os

# 1. API 키 인증
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "여기에_API_키를_입력하세요"))

# 2. ListModels 호출 및 필터링
print("현재 사용 가능한 텍스트 생성 모델 목록:")
for model in genai.list_models():
    # generateContent(텍스트/콘텐츠 생성)를 지원하는 모델만 출력
    if 'generateContent' in model.supported_generation_methods:
        print(model.name)