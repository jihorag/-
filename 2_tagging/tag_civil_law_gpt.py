import json
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

# OpenAI settings
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

taxonomy = """
제1편 민법총칙
제1장 민법 서론
제2장 법률관계와 신의성실의 원칙
제1절 법률관계와 권리·의무
제2절 신의성실의 원칙
제1관 서설
제2관 신의칙의 파생원칙
제3장 권리의 주체
제1절 자연인
제1관 권리능력
제2관 의사능력
제3관 행위능력
제4관 자연인의 주소 · 제5관 부재와 실종
제2절 법인
제4장 권리의 객체
제5장 권리의 변동
제1절 총설
제2절 법률행위
제1관 총설 · 제2관 법률행위의 목적
제3절 의사표시
제1관 흠 있는 의사표시
제2관 의사표시의 효력발생
제4절 법률행위의 대리
제1관 서설
제2관 대리권
제3관 대리행위
제4관 복대리
제5관 무권대리
제5절 법률행위의 무효와 취소
제1관 무효
제2관 취소
제6절 법률행위의 부관
제1관 서설 · 제2관 조건
제3관 기한
제6장 기간
제7장 소멸시효
제1절 총설 · 제2절 소멸시효의 요건
제1관 소멸시효의 대상이 되는 권리
제2관 소멸시효의 기산점
제3관 소멸시효의 기간
제3절 시효의 장애
제1관 소멸시효의 중단
제2관 소멸시효의 정지
제4절 소멸시효 완성의 효과
제5절 제척기간

제2편 물권법
제1장 물권법 총설
제1절 물권법 일반 · 제2절 물권변동
제3절 부동산 물권변동
제1관 법률행위에 의한 부동산 물권의 변동
제2관 법률행위에 의하지 않는 부동산물권의 변동
제3관 부동산
제4관 입목등기 및 명인방법
제4절 동산 물권 변동
제5절 물권의 소멸
제2장 점유권
제1절 서론
제2절 점유권의 취득과 소멸
제3절 점유권의 효력 · 제4절 준점유
제3장 소유권
제1절 총설
제2절 상린관계
제3절 소유권의 취득
제1관 총설
제2관 부동산 점유취득시효
제3관 부동산 등기부 취득시효
제4관 취득시효의 중단과 정지 등
제4절 기타 소유권의 취득
제5절 소유권에 기한 물권적 청구권
제6절 공동소유
제1관 총설
제2관 공유
제3관 합유
제4관 총유
제7절 명의신탁
제1관 총설 · 제2관 부동산 실권리자 명의 등기에 관한 법률
제3관 유효한 명의신탁에 관한 판례의 이론
제4장 용익물권
제1절 지상권
제2절 지역권
제3절 전세권
제5장 담보물권
제1절 총설
제2절 유치권
제3절 질권
제1관 동산질권
제2관 권리질권
제4절 저당권
제1관 총설 · 제2관 저당권의 성립
제3관 저당권의 효력
제4관 저당권의 처분 및 소멸
제5관 특수저당권
제5절 비전형담보
제1관 총설 · 제2관 가등기담보
제3관 양도담보
제4관 소유권유보부 매매
"""

prompt_template = """너는 "민법" 과목의 출제 위원급 전문가야.
아래에 여러 객관식 문제의 텍스트와 보기가 배열(JSON) 형태로 주어질 거야. 각 문제에 대해 태그 데이터를 생성해서, 동일한 순서의 배열(JSON Array) 형태로 반환해줘.

[민법 목차 분류]
{taxonomy}

[작업 지시사항]
각 문제 객체에 대해 아래 필드를 가지는 JSON 객체를 만들어, 전체를 하나의 JSON 배열(`[]`)로 출력해.
- id: 입력된 문제의 "id"
- subject: "민법"
- unit: 위 목차의 "편" 이름 (예: "제1편 민법총칙" 또는 "제2편 물권법") 중 하나.
- sub_unit: 위 목차의 "장" 이름 중 하나.
- sub_sub_unit: 위 목차의 "절" 또는 "관" 이름 중 하나. 가장 구체적인 것을 선택해.
- concept: 핵심 키워드를 10자 이내로 작성해.
- difficulty: 난이도 (1: 아주 쉬움 ~ 5: 아주 어려움).
- question_type: (예: "조문암기", "판례해석", "사례형", "옳은 것 고르기", "틀린 것 고르기")

반드시 JSON 형식으로만 출력해.
"""

def is_civil_law(q):
    subj = q.get('subject', '')
    if '민법' in subj:
        return True
    if q.get('tags') and '민법' in q['tags'].get('subject', ''):
        return True
    return False

def run_tagging():
    civil_qs = [q for q in questions if is_civil_law(q)]
    print(f"Total 민법 questions: {len(civil_qs)}")

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
                    "content": "You are a legal expert API that strictly outputs a JSON object containing an array under the key 'results'."
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
            if isinstance(result_json, list):
                return result_json
            elif "results" in result_json:
                return result_json["results"]
            else:
                return list(result_json.values())[0]
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return None

    count = 0
    batch_size = 30
    
    pending_dict = {q['id']: q for q in civil_qs if 'id' in q}
    pending_list = list(pending_dict.values())
    
    for i in range(0, len(pending_list), batch_size):
        batch = pending_list[i:i+batch_size]
        print(f"Tagging batch {i//batch_size + 1} ({i+1} to {min(i+batch_size, len(pending_list))})...")
        
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
            
            import shutil
            shutil.copy(db_path, 'viewer/src/data/questions_db.json')
            
            print(f"-> Batch saved & Viewer DB updated ({count} tagged so far)")
        else:
            print("Failed to get valid response for this batch, skipping...")

    print("Finished tagging 민법! DB updated.")

if __name__ == '__main__':
    run_tagging()
