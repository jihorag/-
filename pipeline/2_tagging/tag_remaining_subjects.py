import json
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"
db_path = "questions_db.json"

with open(db_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

with open("taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy = json.load(f)

prompt_template = """너는 "{subject_name}" 과목의 출제 위원급 전문가야.
아래에 여러 객관식 문제의 텍스트와 보기가 배열(JSON) 형태로 주어질 거야. 각 문제에 대해 태그 데이터를 생성해서, 동일한 순서의 배열(JSON Array) 형태로 반환해줘.

[{subject_name} 목차 분류]
{taxonomy_str}

[작업 지시사항]
각 문제 객체에 대해 아래 필드를 가지는 JSON 객체를 만들어, 전체를 하나의 JSON 배열(`[]`)로 출력해.
- id: 입력된 문제의 "id"
- subject: "{subject_name}"
- unit: 위 목차의 가장 큰 단위 (예: PART) 중 하나.
- sub_unit: 위 목차의 중간 단위 (예: Chapter 또는 장) 중 하나.
- sub_sub_unit: 위 목차의 가장 구체적인 하위 단위 (예: 절 또는 관) 중 하나. (만약 없으면 빈 문자열 "")
- concept: 핵심 키워드를 10자 이내로 작성해.
- difficulty: 난이도 (1: 아주 쉬움 ~ 5: 아주 어려움).
- question_type: (예: "조문암기", "판례해석", "계산문제", "이론형", "옳은 것 고르기", "틀린 것 고르기")

반드시 JSON 형식으로만 출력해. 다른 말은 하지 마.
"""

def get_taxonomy_str(subj):
    data = taxonomy.get(subj, [])
    lines = []
    for part in data:
        lines.append(part["name"])
        for ch in part.get("children", []):
            lines.append("  " + ch["name"])
            for sec in ch.get("children", []):
                lines.append("    " + sec["name"])
                for sub in sec.get("children", []):
                    lines.append("      " + sub["name"])
    return "\n".join(lines)

def call_openai_batch(batch_qs, subject_name, taxonomy_str):
    input_data = []
    for q in batch_qs:
        input_data.append({
            "id": q.get('id'),
            "year": q.get('year', ''),
            "question": q.get('question', ''),
            "options": q.get('options', [])
        })
        
    prompt = prompt_template.format(subject_name=subject_name, taxonomy_str=taxonomy_str)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": MODEL_NAME,
        "response_format": { "type": "json_object" },
        "messages": [
            {"role": "system", "content": "You are a legal/economic expert API that strictly outputs a JSON object containing an array under the key 'results'."},
            {"role": "user", "content": prompt + "\n\n[문제 목록]\n" + json.dumps(input_data, ensure_ascii=False)}
        ],
        "temperature": 0.1
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        content = data['choices'][0]['message']['content']
        result_json = json.loads(content)
        if isinstance(result_json, list): return result_json
        elif "results" in result_json: return result_json["results"]
        else: return list(result_json.values())[0]
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return None

def run_for_subject(target_subject):
    tax_str = get_taxonomy_str(target_subject)
    if not tax_str:
        print(f"No taxonomy found for {target_subject}")
        return

    # 식별 로직 (과목명이 포함되거나, 기존 태그가 있는 경우)
    def is_target(q):
        s = q.get('subject', '')
        # 회계학, 회계학개론 모두 매칭
        if target_subject == '회계학' and '회계학' in s: return True
        if target_subject == '경제학원론' and ('경제학' in s or '재정학' in s): return True
        if target_subject in s: return True
        
        ts = q.get('tags', {}).get('subject', '')
        if target_subject == '회계학' and '회계학' in ts: return True
        if target_subject == '경제학원론' and ('경제학' in ts or '재정학' in ts): return True
        if target_subject in ts: return True
        return False

    target_qs = [q for q in questions if is_target(q)]
    print(f"\n[{target_subject}] Total questions: {len(target_qs)}")
    
    pending_dict = {q['id']: q for q in target_qs if 'id' in q}
    pending_list = list(pending_dict.values())
    
    batch_size = 30
    count = 0
    for i in range(0, len(pending_list), batch_size):
        batch = pending_list[i:i+batch_size]
        print(f"Tagging {target_subject} batch {i//batch_size + 1} ({i+1} to {min(i+batch_size, len(pending_list))})...")
        
        results = call_openai_batch(batch, target_subject, tax_str)
        if results and isinstance(results, list):
            for res in results:
                q_id = res.get('id')
                if q_id in pending_dict:
                    tag_data = {k: v for k, v in res.items() if k != 'id'}
                    pending_dict[q_id]['tags'] = tag_data
                    count += 1
                    
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            
            import shutil
            shutil.copy(db_path, 'viewer/src/data/questions_db.json')
            print(f"-> Batch saved ({count} tagged for {target_subject})")
        else:
            print("Failed to get valid response for this batch, skipping...")

if __name__ == '__main__':
    subjects_to_tag = ["감정평가관계법규", "부동산학원론", "경제학원론", "회계학"]
    for subj in subjects_to_tag:
        run_for_subject(subj)
    print("All remaining subjects have been tagged! DB updated.")
