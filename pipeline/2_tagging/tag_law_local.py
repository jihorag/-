import json
import requests
import time
import os

# Ollama settings
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:12b"

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

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
Chapter 05 개발행위의 허가 등
Chapter 06 보칙 및 벌칙

PART 02 건축법
Chapter 01 총칙
Chapter 02 건축물의 건축 등
Chapter 03 건축물의 대지와 도로
Chapter 04 건축물의 구조 및 재료
Chapter 05 지역 및 지구 안의 건축물
Chapter 06 특별건축구역, 건축협정, 결합건축, 벌칙

PART 03 도시 및 주거환경정비법
Chapter 01 총칙
Chapter 02 기본계획의 수립 및 정비구역의 지정
Chapter 03 정비사업의 시행
제1절 시행자 및 사업시행계획
제2절 관리처분계획 및 소유권이전

PART 04 공간정보의 구축 및 관리 등에 관한 법률
Chapter 01 총칙
Chapter 02 측량
Chapter 03 지적(地籍)
제1절 토지의 조사 및 등록
제2절 지번
제3절 지목
제4절 경계
제5절 면적
Chapter 04 지적공부
Chapter 05 토지의 이동 등
제1절 토지의 이동
제2절 등록사항의 정정 등

PART 05 부동산등기법
Chapter 01 총칙
Chapter 02 등기부 등
Chapter 03 등기절차
Chapter 04 표시에 관한 등기
Chapter 05 권리에 관한 등기
Chapter 06 이의신청

PART 06 국유재산법
Chapter 01 총칙
Chapter 02 총괄청
Chapter 03 행정재산
Chapter 04 일반재산
Chapter 05 지식재산 관리·처분의 특례
Chapter 06 대장과 보고 및 보칙

PART 07 부동산 가격공시에 관한 법률
Chapter 01 용어의 정의
Chapter 02 표준지공시지가
Chapter 03 개별공시지가
Chapter 04 주택가격의 공시
Chapter 05 비주거용 부동산가격의 공시
Chapter 06 부동산가격공시위원회

PART 08 감정평가 및 감정평가사에 관한 법률
Chapter 01 총칙
Chapter 02 감정평가사
Chapter 03 감정평가법인
Chapter 04 징계
Chapter 05 과징금
Chapter 06 보칙 및 벌칙

PART 09 동산.채권 등의 담보에 관한 법률
Chapter 01 동산담보권
Chapter 02 채권담보권
Chapter 03 담보등기
"""

prompt_template = """너는 감정평가사 "감정평가관계법규" 과목의 출제 위원급 전문가야.
아래에 제공된 객관식 문제의 텍스트와 보기를 읽고 이 문제에 대한 태그 데이터를 생성해줘. (기존 해설은 무시해도 좋아)

[감정평가관계법규 목차 분류]
{taxonomy}

[문제 정보]
- 문제: {question}
- 보기: {options}

[작업 지시사항]
이 문제에 대해 분석하여 아래 JSON 형식에 맞게 값을 채워줘.
- subject: "감정평가관계법규"
- unit: 위 목차의 "PART" 이름 (예: "PART 01 국토의 계획 및 이용에 관한 법률") 중 가장 정확하게 일치하는 하나. 만약 위 9개 법률 범위에 해당하지 않는 문제(예: 세법, 공인중개사법 등)라면 "Out of Scope" 라고 적어.
- sub_unit: 위 목차의 "Chapter" 이름 중 하나. 범위 밖이라면 "Out of Scope"
- concept: 핵심 키워드를 10자 이내로 작성해.
- difficulty: 문제의 난이도를 1부터 5까지의 정수로 평가해 (1: 아주 쉬움 ~ 5: 아주 어려움).
- question_type: 이 문제의 형태나 필요한 스킬 (예: "조문암기", "박스조합형(ㄱ, ㄴ, ㄷ)", "옳은 것 고르기")
- in_scope: 위 9개 법률(감정평가사 출제범위)에 포함되는 문제라면 true, 포함되지 않는다면 false (불리언 값으로 작성해).
- source: "감정평가사 1차" 또는 "공인중개사 2차" (가장 적절한 것)
- year: "{year}"

오직 위 9개 필드를 포함하는 유효한 JSON 객체 하나만 출력해. 다른 텍스트는 절대 붙이지 마.
"""

def is_law(q):
    exam = q.get('exam', '감정평가사')
    period = q.get('period', '2')
    num = int(q.get('number', 0))
    
    # 1. 감정평가사 관계법규 (2교시 1~40번)
    if exam == '감정평가사' and period == '2' and 1 <= num <= 40:
        return True
    # 2. 공인중개사 2차 (g2 41~120번 - 공법, 공시법, 세법 포함. 세법 등은 LLM이 in_scope=false로 필터링)
    if exam == '공인중개사' and period == 'g2' and 41 <= num <= 120:
        return True
        
    return False

def run_tagging():
    law_qs = [q for q in questions if is_law(q)]
    print(f"Total 감정평가관계법규 questions: {len(law_qs)}")

    pending_qs = [q for q in law_qs if 'tags' not in q or q['tags'].get('subject') != '감정평가관계법규']
    print(f"Pending 감정평가관계법규 questions to tag: {len(pending_qs)}")

    def call_ollama(q):
        prompt = prompt_template.format(
            taxonomy=taxonomy,
            question=q.get('question', ''),
            options=json.dumps(q.get('options', []), ensure_ascii=False),
            year=q.get('year', '')
        )
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.1}
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
            if count % 10 == 0:
                with open(db_path, "w", encoding="utf-8") as f:
                    json.dump(questions, f, ensure_ascii=False, indent=2)
                print(f"-> Progress saved ({count} tagged so far)")
        else:
            print("Failed to get a valid response, skipping...")

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print("Finished tagging 감정평가관계법규! DB updated.")

    import shutil
    shutil.copy(db_path, 'viewer/src/data/questions_db.json')
    print("Viewer DB updated.")

if __name__ == '__main__':
    run_tagging()
