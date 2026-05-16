import json
import os
import base64
import re
import time
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
import google.generativeai as genai

# .env 파일에서 환경변수 불러오기
load_dotenv()

# ==========================================
# ⚙️ 설정 (실제 존재하는 모델명으로 고정)
# 1. 가성비 모델 (1차 처리용)
GEMINI_MODEL_NAME = "gemini-2.5-flash" # 모든 사용자에게 안정적으로 지원되는 플래시 모델

# 2. 프리미엄 모델 (2차 정밀 분석용)
PREMIUM_MODEL_NAME = "gpt-4o" 

# 파일 경로 설정 (원본 DB를 직접 업데이트)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.normpath(os.path.join(BASE_DIR, "../questions_db.json"))
TAXONOMY_FILE = os.path.normpath(os.path.join(BASE_DIR, "../taxonomy_v4.json"))
IMAGE_DIR_BASE = os.path.normpath(os.path.join(BASE_DIR, "../"))
TARGET_EXAM = "감정평가사"
# ==========================================

# 클라이언트 초기화 (.env의 GEMINI_API_KEY 또는 GOOGLE_API_KEY 모두 지원)
gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not gemini_key:
    print("❌ API 키 오류: .env 파일에 GEMINI_API_KEY 또는 GOOGLE_API_KEY가 없습니다.")
if not os.environ.get("OPENAI_API_KEY"):
    print("❌ API 키 오류: .env 파일에 OPENAI_API_KEY가 없습니다.")

genai.configure(api_key=gemini_key)
gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
openai_client = OpenAI()

def get_image_for_gemini(image_path):
    clean_path = image_path.replace("./", "")
    full_path = os.path.join(IMAGE_DIR_BASE, clean_path)
    if not os.path.exists(full_path):
        return None
    with open(full_path, "rb") as f:
        content = f.read()
    ext = image_path.split('.')[-1].lower()
    mime_type = "image/gif" if ext == "gif" else f"image/{ext}"
    return {"mime_type": mime_type, "data": content}

def get_base64_image_for_openai(image_path):
    clean_path = image_path.replace("./", "")
    full_path = os.path.join(IMAGE_DIR_BASE, clean_path)
    if not os.path.exists(full_path):
        return None
    with open(full_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def build_system_prompt(taxonomy_data):
    taxonomy_str = json.dumps(taxonomy_data, ensure_ascii=False, indent=2)
    return f"""당신은 최고 수준의 감정평가사 1차 시험 출제위원 및 수험 전문가입니다.
주어진 기출문제를 분석하여 아래 제공된 V4 분류체계(장, 절, 항목/관) 중 가장 적합한 단원을 찾고, 1~5단계 난이도를 산정하세요.

[V4 분류체계 (Taxonomy Hierarchy)]
{taxonomy_str}

[분류 지침]
1. 과목 -> 세부과목 -> 장 -> 절 -> 항목/관 순서로 가장 구체적인 단원을 찾으세요.
2. 반드시 JSON 형식으로만 응답하세요. 다른 텍스트는 금지합니다.

{{
  "difficulty": 3,
  "mapped_taxonomy": {{
    "subject": "과목명",
    "sub_subject": "세부과목명(없으면 빈문자열)",
    "chapter": "장 이름",
    "section": "절 이름",
    "item": "세부 항목 또는 관 이름"
  }},
  "needs_higher_ai": false,
  "reason": "분류 근거"
}}"""

def main():
    with open(TAXONOMY_FILE, 'r', encoding='utf-8') as f:
        taxonomy_data = json.load(f)
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
        
    # 타겟 기출문제만 필터링 (그러나 저장은 전체 DB에 해야함)
    target_questions = [q for q in all_questions if q.get('exam', '') == TARGET_EXAM]
    print(f"🎯 총 {len(target_questions)}개의 {TARGET_EXAM} 기출문제를 처리합니다.")
    
    system_prompt = build_system_prompt(taxonomy_data)
    
    for q in tqdm(target_questions, desc="인덱싱 진행중"):
        # 기존에 정밀 분류를 1회 이상 통과한 문제는 패스 (이어서 진행 기능)
        if q.get('indexing_v4_count', 0) >= 1:
            continue
            
        text_content = f"[문제]: {q.get('question', '')}\n[선지]: {json.dumps(q.get('options', []), ensure_ascii=False)}\n[해설]: {q.get('explanation', '')}"
        img_tags = re.findall(r'\[IMAGE:\s*(.*?)\]', q.get('question', '') + q.get('explanation', ''))
        
        try:
            # 1단계: Gemini Flash
            gemini_parts = [system_prompt, text_content]
            for img_path in img_tags:
                img_data = get_image_for_gemini(img_path)
                if img_data: gemini_parts.append(img_data)
            
            response = gemini_model.generate_content(gemini_parts)
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if not json_match: raise ValueError("JSON parsing error")
            result_json = json.loads(json_match.group())
            
            # 2단계: Fallback
            if result_json.get('needs_higher_ai', False):
                tqdm.write(f"🧠 [ID {q.get('id')}] GPT-4o 투입")
                openai_content = [{"type": "text", "text": text_content}]
                for img_path in img_tags:
                    b64 = get_base64_image_for_openai(img_path)
                    if b64:
                        openai_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
                
                premium_resp = openai_client.chat.completions.create(
                    model=PREMIUM_MODEL_NAME,
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": openai_content}],
                    response_format={"type": "json_object"}
                )
                result_json = json.loads(premium_resp.choices[0].message.content)
                result_json['processed_by'] = PREMIUM_MODEL_NAME
            else:
                result_json['processed_by'] = GEMINI_MODEL_NAME
            
            # 분류 결과 및 재분류 카운트(count) DB 원본 데이터에 바로 기록
            q['indexing_v4'] = result_json
            q['indexing_v4_count'] = q.get('indexing_v4_count', 0) + 1
            
            # 진행상황 출력
            tax = result_json.get('mapped_taxonomy', {})
            hierarchy = f"{tax.get('subject', '')} > {tax.get('chapter', '')} > {tax.get('section', '')} > {tax.get('item', '')}"
            icon = "⚡" if result_json['processed_by'] == GEMINI_MODEL_NAME else "🧠"
            tqdm.write(f"{icon} [ID:{q.get('id')}] {result_json['processed_by']} | Lv.{result_json.get('difficulty')} | 카운트:{q['indexing_v4_count']} | {hierarchy}")
            
            # 원본 DB 파일 덮어쓰기 (전체 데이터를 다시 저장하여 안정성 보장)
            with open(INPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_questions, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            tqdm.write(f"❌ Error {q.get('id')}: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
