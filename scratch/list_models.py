import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=gemini_key)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
