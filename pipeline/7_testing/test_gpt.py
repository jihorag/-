import json, requests, os
from dotenv import load_dotenv
load_dotenv()

with open('questions_db.json', 'r') as f:
    questions = json.load(f)

# Mock is_law
def is_law(q):
    exam = q.get('exam', '감정평가사')
    period = q.get('period', '2')
    num = int(q.get('number', 0))
    if exam == '감정평가사' and period == '2' and 1 <= num <= 40: return True
    if exam == '공인중개사' and period == 'g2' and 41 <= num <= 120: return True
    return False

law_qs = [q for q in questions if is_law(q)]
pending_qs = law_qs[:10]

taxonomy = """
PART 01 국토의 계획 및 이용에 관한 법률
Chapter 01 총칙
Chapter 02 광역도시계획
Chapter 03 도시·군기본계획
Chapter 04 도시·군관리계획
제1절 도시·군관리계획
제2절 용도지역·용도지구·용도구역
제3절 기반시설과 도시·군계획시설 등
제4절 지구단위계획구역과 지구단위계획
Chapter 04의2 공간재구조화계획 및 공간혁신구역
Chapter 05 개발행위의 허가 등
Chapter 06 보칙 및 벌칙
PART 02 건축법...
"""

prompt_template = """너는 감정평가사 "감정평가관계법규" 과목의 출제 위원급 전문가야.
아래에 여러 객관식 문제의 텍스트와 보기가 배열(JSON) 형태로 주어질 거야. 각 문제에 대해 태그 데이터를 생성해서, 동일한 순서의 배열(JSON Array) 형태로 반환해줘.

[감정평가관계법규 목차 분류]
{taxonomy}

[작업 지시사항]
각 문제 객체에 대해 아래 필드를 가지는 JSON 객체를 만들어, 전체를 하나의 JSON 배열(`[]`)로 출력해.
- id: 입력된 문제의 "id"
- subject: "감정평가관계법규"
- unit: 위 목차의 "PART" 이름 (예: "PART 01 국토의 계획 및 이용에 관한 법률") 중 가장 정확하게 일치하는 하나. 만약 위 9개 법률 범위에 해당하지 않는 문제라면 "Out of Scope" 라고 적어.
- sub_unit: 위 목차의 "Chapter" 이름 중 하나. 범위 밖이라면 "Out of Scope"
- concept: 핵심 키워드를 10자 이내로 작성해.
- difficulty: 난이도 (1: 아주 쉬움 ~ 5: 아주 어려움).
- question_type: (예: "조문암기", "박스조합형", "옳은 것 고르기", "틀린 것 고르기"). '옳지 않은 것은?' 등은 "틀린 것 고르기"로 분류.
- in_scope: 출제범위 포함 시 true, 아니면 false (boolean).
- source: "감정평가사 1차" 또는 "공인중개사 2차"
- year: 해당 문제의 연도

반드시 JSON 배열 형태로만 출력해.
"""

input_data = [{"id": q.get('id'), "year": q.get('year'), "question": q.get('question'), "options": q.get('options')} for q in pending_qs]
prompt = prompt_template.format(taxonomy=taxonomy)
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"}
payload = {
    "model": "gpt-4o-mini", # wait user said gpt-5.4-mini-2026-03-17. Let's use gpt-4o-mini here as a proxy if gpt-5.4 isn't real or use the exact name.
    "response_format": { "type": "json_object" },
    "messages": [
        {"role": "system", "content": "You are a legal expert API that strictly outputs a JSON object containing an array under the key 'results'."},
        {"role": "user", "content": prompt + "\n\n[문제 목록]\n" + json.dumps(input_data, ensure_ascii=False)}
    ],
    "temperature": 0.1
}

res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=60).json()
print(res['choices'][0]['message']['content'])
