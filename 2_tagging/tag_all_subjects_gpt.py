import json
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini" # 비용 절감을 위해 mini 모델로 변경
db_path = "questions_db.json"

with open(db_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

with open("taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy = json.load(f)

def get_flat_taxonomy(subj):
    data = taxonomy.get(subj, [])
    paths = []
    
    def traverse(node, current_path):
        new_path = current_path + [node["name"]]
        if not node.get("children"):
            paths.append(" > ".join(new_path))
        else:
            # If a node has children, we can also tag at this node itself if there's a general question,
            # but usually we want leaf nodes. We will provide all paths.
            paths.append(" > ".join(new_path))
            for child in node["children"]:
                traverse(child, new_path)
                
    for part in data:
        traverse(part, [])
    return paths

prompt_template = """너는 "{subject_name}" 과목의 출제 위원급 전문가야.
아래에 여러 객관식 문제의 텍스트와 보기가 배열(JSON) 형태로 주어질 거야. 각 문제에 대해 태그 데이터를 생성해서, 동일한 순서의 배열(JSON Array) 형태로 반환해줘.

[{subject_name} 공식 허용 분류 경로(Path) 목록]
{taxonomy_paths}

[작업 지시사항]
각 문제 객체에 대해 아래 필드를 가지는 JSON 객체를 만들어, 전체를 하나의 JSON 배열(`[]`)로 출력해.
- id: 입력된 문제의 "id"
- taxonomy_path: 반드시 위 [공식 허용 분류 경로 목록]에 있는 텍스트 중 가장 적절한 하나를 토씨 하나 틀리지 않고 똑같이 복사해서 넣어. 단, 타 시험 문제이거나 감정평가사 {subject_name} 시험 범위와 명백히 무관한 문제라고 판단되면 반드시 "범위 외" 라고 적어. 절대 임의로 경로를 만들지 마.
- concept: 핵심 키워드를 10자 이내로 작성해.
- difficulty: 난이도 (1: 아주 쉬움 ~ 5: 아주 어려움).
- question_type: (예: "조문암기", "판례해석", "계산문제", "이론형", "옳은 것 고르기", "틀린 것 고르기")

반드시 JSON 형식으로만 출력해. 다른 말은 절대 하지 마.
"""

def call_openai_batch(batch_qs, subject_name, paths):
    input_data = []
    for q in batch_qs:
        input_data.append({
            "id": q.get('id'),
            "year": q.get('year', ''),
            "question": q.get('question', ''),
            "options": q.get('options', [])
        })
        
    paths_str = "\n".join(paths)
    prompt = prompt_template.format(subject_name=subject_name, taxonomy_paths=paths_str)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": MODEL_NAME,
        "response_format": { "type": "json_object" },
        "messages": [
            {"role": "system", "content": "You strictly output a JSON object containing an array under the key 'results'."},
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
    paths = get_flat_taxonomy(target_subject)
    if not paths:
        print(f"No taxonomy found for {target_subject}")
        return

    # 식별 로직
    def is_target(q):
        s = q.get('subject', '')
        if target_subject == '회계학' and '회계학' in s: return True
        if target_subject == '경제학원론' and ('경제학' in s or '재정학' in s): return True
        if target_subject in s: return True
        
        ts = q.get('tags', {}).get('subject', '')
        if target_subject == '회계학' and '회계학' in ts: return True
        if target_subject == '경제학원론' and ('경제학' in ts or '재정학' in ts): return True
        if target_subject in ts: return True
        return False

    target_qs = [q for q in questions if is_target(q)]
    print(f"\n[{target_subject}] Total questions matched: {len(target_qs)}")
    
    # 강제로 전부 다시 태깅 (시스템 노트 V2)
    pending_qs = []
    for q in target_qs:
        if q.get('tags', {}).get('system_note') != '완벽경로매핑V2':
            pending_qs.append(q)
            
    print(f"[{target_subject}] Questions to tag: {len(pending_qs)}")
    if len(pending_qs) == 0:
        return
        
    pending_dict = {q['id']: q for q in pending_qs if 'id' in q}
    pending_list = list(pending_dict.values())
    
    batch_size = 50
    count = 0
    for i in range(0, len(pending_list), batch_size):
        batch = pending_list[i:i+batch_size]
        print(f"Tagging {target_subject} batch {i//batch_size + 1} ({i+1} to {min(i+batch_size, len(pending_list))})...")
        
        results = call_openai_batch(batch, target_subject, paths)
        if results and isinstance(results, list):
            for res in results:
                q_id = res.get('id')
                if q_id in pending_dict:
                    tax_path = res.get('taxonomy_path', '')
                    if tax_path == '범위 외':
                        tag_data = {
                            'subject': target_subject,
                            'unit': '범위 외',
                            'sub_unit': '범위 외',
                            'is_out_of_scope': True,
                            'concept': res.get('concept', ''),
                            'difficulty': res.get('difficulty', 3),
                            'question_type': res.get('question_type', ''),
                            'system_note': '완벽경로매핑V2'
                        }
                    else:
                        parts = tax_path.split(' > ')
                        tag_data = {
                            'subject': target_subject,
                            'unit': parts[0] if len(parts) > 0 else '',
                            'sub_unit': parts[1] if len(parts) > 1 else '',
                            'sub_sub_unit': parts[2] if len(parts) > 2 else '',
                            'sub_sub_sub_unit': parts[3] if len(parts) > 3 else '',
                            'is_out_of_scope': False,
                            'concept': res.get('concept', ''),
                            'difficulty': res.get('difficulty', 3),
                            'question_type': res.get('question_type', ''),
                            'system_note': '완벽경로매핑V2'
                        }
                    
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
    subjects_to_tag = ["민법", "감정평가관계법규", "부동산학원론", "경제학원론", "회계학"]
    for subj in subjects_to_tag:
        run_for_subject(subj)
    print("ALL subjects strictly tagged with the new taxonomy! DB updated.")
