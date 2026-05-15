import json
import requests
import time
import os

# Ollama settings
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:12b"

# Load DB
db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

# The Taxonomy provided by the user
taxonomy = """
PART. 01 미시경제학
1장 경제학의 기초
2장 수요-공급
3장 탄력성
4장 수요-공급이론의 응용
5장 무차별곡선이론
6장 현시선호이론
7장 소비자이론의 응용
8장 불확실성하의 선택이론
9장 생산함수
10장 비용함수
11장 완전경쟁시장
12장 독점시장
13장 독점적 경쟁시장
14장 과점시장
15장 게임이론
16장 요소시장
17장 일반균형이론
18장 후생경제학
19장 시장 실패
20장 정보경제학

PART. 02 거시경제학
1장 국민소득의 측정과 경제구조
2장 고전학파의 국민소득결정이론
3장 케인즈의 국민소득결정이론
4장 소비함수론
5장 투자함수론
6장 금융제도와 화폐공급
7장 화폐수요와 금융정책
8장 IS-LM과 정책효과
9장 총수요-총공급
10장 물가와 인플레이션
11장 노동시장과 실업
12장 필립스곡선과 스태그플레이션
13장 각 학파 모형의 주요 내용
14장 안정화정책과 관련된 논쟁
15장 경제변동론
16장 경제성장론
17장 국제무역이론
18장 무역정책론
19장 환율
20장 국제수지론
"""

prompt_template = """너는 감정평가사 경제학원론 과목의 출제 위원급 전문가야.
아래에 제공된 객관식 문제의 텍스트, 보기, 해설을 읽고 이 문제에 대한 태그 데이터를 생성해줘.

[경제학 목차 분류]
{taxonomy}

[문제 정보]
- 문제: {question}
- 보기: {options}
- 해설: {explanation}

[작업 지시사항]
이 문제에 대해 분석하여 아래 JSON 형식에 맞게 값을 채워줘.
- subject: "경제학원론"
- unit: 반드시 위 목차의 "PART" 이름 (예: "미시경제학" 또는 "거시경제학") 중 하나를 선택해.
- sub_unit: 반드시 위 목차의 "장" 이름 (예: "2장 수요-공급") 중 가장 정확하게 일치하는 하나를 선택해.
- concept: 이 문제가 다루는 구체적인 핵심 개념을 10자 이내의 단어로 요약해줘 (예: "한계효용", "균형가격", "IS-LM 곡선").
- difficulty: "상", "중", "하" 중 하나.
- question_type: 이 문제의 형태나 필요한 스킬 (예: "계산문제", "박스조합형(ㄱ, ㄴ, ㄷ)", "옳은 것 찾기", "틀린 것 찾기").
- source: "감정평가사 1차"
- year: "{year}"

오직 위 필드를 포함하는 유효한 JSON 객체 하나만 출력해. 다른 텍스트는 절대 붙이지 마.

출력 예시:
{{
  "subject": "경제학원론",
  "unit": "미시경제학",
  "sub_unit": "2장 수요-공급",
  "concept": "시장균형이동",
  "difficulty": "중",
  "question_type": "틀린 것 찾기",
  "source": "감정평가사 1차",
  "year": "{year}"
}}
"""

def is_economics(q):
    # period is '1' or '1_old', number is between 41 and 80
    period = q.get('period', '2')
    num = int(q.get('number', 0))
    if period in ['1', '1_old']:
        if 41 <= num <= 80:
            return True
    return False

economics_qs = [q for q in questions if is_economics(q)]
print(f"Total Economics questions: {len(economics_qs)}")

# Filter ones that are not tagged yet
pending_qs = [q for q in economics_qs if 'tags' not in q]
print(f"Pending Economics questions to tag: {len(pending_qs)}")

def call_ollama(q):
    prompt = prompt_template.format(
        taxonomy=taxonomy,
        question=q.get('question', ''),
        options=json.dumps(q.get('options', []), ensure_ascii=False),
        explanation=q.get('explanation', ''),
        year=q.get('year', '')
    )
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return json.loads(data['response'])
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return None

count = 0
for q in pending_qs:
    print(f"Tagging {q['year']} - Q{q['number']}...")
    result = call_ollama(q)
    if result:
        q['tags'] = result
        count += 1
        
        # Save incrementally every 10 questions to avoid losing progress
        if count % 10 == 0:
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            print(f"-> Progress saved ({count} tagged so far)")
    else:
        print("Failed to get a valid response, skipping...")

# Final save
with open(db_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)
print("Finished tagging! DB updated.")

# Copy to viewer
import shutil
shutil.copy(db_path, 'viewer/src/data/questions_db.json')
print("Viewer DB updated.")
