import requests
import json
import os
import re
import shutil
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-5.4-mini-2026-03-17"

db_path = "questions_db.json"
questions = json.load(open(db_path, encoding='utf-8'))

taxonomy = """
PART 01 부동산학 총론
Chapter 01 부동산의 개념과 분류
Chapter 02 토지의 특성

PART 02 부동산 경제론
Chapter 01 부동산의 수요와 공급
Chapter 02 부동산의 경기변동

PART 03 부동산 시장론
Chapter 01 부동산시장
Chapter 02 입지 및 공간구조론

PART 04 부동산 정책론
Chapter 01 부동산정책의 의의와 표준
Chapter 02 토지정책
Chapter 03 주택정책
Chapter 04 부동산 조세정책

PART 05 부동산 투자론
Chapter 01 부동산투자이론
Chapter 02 부동산투자분석 및 기법

PART 06 부동산 금융론
Chapter 01 부동산금융론
Chapter 02 부동산증권론

PART 07 부동산 개발 및 관리론
Chapter 01 부동산이용론
Chapter 02 부동산개발론
Chapter 03 부동산관리론
Chapter 04 부동산마케팅론

PART 08 부동산 감정평가론
Chapter 01 감정평가의 기초이론
Chapter 02 감정평가방식(3방식 6방법)
Chapter 03 부동산가격공시제도
"""

prompt_template = """
당신은 부동산학개론 전문가입니다. 주어진 문제들을 아래의 목차(Taxonomy)에 따라 분류하고 분석하십시오.

[목차]
{taxonomy}

[출력 형식]
반드시 JSON 배열 형태로 응답하십시오. 각 객체는 다음 필드를 포함해야 합니다:
- id: 입력된 문제의 "id"
- subject: "부동산학개론"
- unit: 위 목차의 "PART" 이름 (예: "PART 02 부동산 경제론")
- sub_unit: 위 목차의 "Chapter" 이름 (예: "Chapter 01 부동산의 수요와 공급")
- concept: 핵심 키워드 (10자 이내)
- difficulty: 난이도 (1: 아주 쉬움 ~ 5: 아주 어려움)
- question_type: (예: "계산문제", "개념정의", "특성분석", "옳은 것 고르기", "틀린 것 고르기")
- in_scope: 출제범위 포함 여부 (boolean)
- source: "감정평가사 1차" 또는 "공인중개사 1차"
- year: 해당 문제의 연도

반드시 JSON 배열 형태로만 출력해.
"""

def is_real_estate(q):
    exam = q.get('exam', '감정평가사')
    period = q.get('period', '1')
    num_str = str(q.get('number', '0'))
    try: num = int(num_str)
    except: num = 0
    
    # 1. 감정평가사 부동산학원론 (1교시 81~120번)
    if (exam == '감정평가사' or exam is None) and period == '1' and 81 <= num <= 120:
        return True
    # 2. 공인중개사 1차 부동산학개론 (g1 1~40번)
    if exam == '공인중개사' and period == 'g1' and 1 <= num <= 40:
        return True
        
    return False

def run_tagging():
    re_qs = [q for q in questions if is_real_estate(q)]
    print(f"Total 부동산학개론 questions: {len(re_qs)}")

    pending_qs = [q for q in re_qs if 'tags' not in q or q['tags'].get('subject') != '부동산학개론']
    print(f"Pending 부동산학개론 questions to tag: {len(pending_qs)}")

    def call_openai_batch(batch_qs):
        input_data = []
        for q in batch_qs:
            input_data.append({
                "id": q.get('id'),
                "year": q.get('year', ''),
                "question": q.get('question', ''),
                "options": q.get('options', [])
            })
            
        prompt = prompt_template.format(taxonomy=taxonomy)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        payload = {
            "model": MODEL_NAME,
            "response_format": { "type": "json_object" },
            "messages": [
                {
                    "role": "system",
                    "content": "You are a real estate expert API that strictly outputs a JSON object containing an array under the key 'results'."
                },
                {
                    "role": "user",
                    "content": prompt + "\n\n[문제 목록]\n" + json.dumps(input_data, ensure_ascii=False)
                }
            ],
            "temperature": 0.1
        }
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            result_json = json.loads(content)
            if "results" in result_json:
                return result_json["results"]
            elif isinstance(result_json, list):
                return result_json
            else:
                return list(result_json.values())[0]
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return None

    count = 0
    batch_size = 10
    pending_dict = {q['id']: q for q in pending_qs if 'id' in q}
    
    for i in range(0, len(pending_qs), batch_size):
        batch = pending_qs[i:i+batch_size]
        print(f"Tagging batch {i//batch_size + 1} ({i+1} to {min(i+batch_size, len(pending_qs))})...")
        
        results = call_openai_batch(batch)
        if results and isinstance(results, list):
            for res in results:
                q_id = res.get('id')
                if q_id in pending_dict:
                    tag_data = {k: v for k, v in res.items() if k != 'id'}
                    pending_dict[q_id]['tags'] = tag_data
                    count += 1
                    
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            
            shutil.copy(db_path, 'viewer/src/data/questions_db.json')
            print(f"-> Batch saved & Viewer DB updated ({count} tagged so far)")
        else:
            print("Failed to get valid response for this batch, skipping...")

    print("Finished tagging 부동산학개론! DB updated.")

if __name__ == '__main__':
    run_tagging()
