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
PART 01 부동산학 총론

Chapter 01 부동산학과 부동산 활동
제1절 부동산학의 의미
제2절 부동산 활동
Chapter 02 부동산의 개념
제1절 부동산의 복합개념
제2절 정착물과 준부동산
Chapter 03 부동산의 분류
제1절 토지의 분류 및 용어 정의
제2절 주택의 분류
Chapter 04 부동산의 특성
제1절 자연적 특성
제2절 인문적 특성
Chapter 05 기타 유형

PART 02 경제론

Chapter 01 경제론의 기본개념
Chapter 02 수요와 공급이론
제1절 수요와 공급
제2절 균형을 변화시키는 4가지 규칙
제3절 계산 문제
Chapter 03 수요와 공급의 탄력성
제1절 탄력성의 의미
제2절 탄력성의 응용
제3절 계산 문제

PART 03 시장론

Chapter 01 부동산 시장과 주택 시장
제1절 부동산 시장의 특징
제2절 디파스퀠리.위튼의 4사분면 모형
Chapter 02 부동산 시장과 정보의 효율성
제1절 효율적 시장 이론
제2절 할당 효율적 시장
제3절 계산 문제
Chapter 03 부동산 시장의 변화
제1절 부동산 경기변동
제2절 거미집 모형
제3절 주거분리 현상, 주택여과 현상

PART 04 부동산 정책론

Chapter 01 부동산 정책의 이해
제1절 시장실패
제2절 정부의 시장 개입방식
Chapter 02 외부효과와 공공재
제1절 외부효과
제2절 공공재
Chapter 03 임대주택 및 분양주택 정책
제1절 임대주택 정책
제2절 분양주택 정책
Chapter 04 부동산 조세 정책
제1절 조세 전가와 조세 부담
제2절 우리나라 조세 체계
제3절 계산 문제
Chapter 05 다양한 부동산 정책
제1절 부동산 정책
제2절 기타 유형

PART 05 투자론

Chapter 01 부동산 투자의 수익과 위험
제1절 투자의 수익
제2절 지렛대 효과
제3절 투자의 위험
제4절 계산 문제
Chapter 02 투자결정이론
제1절 기대수익률, 요구수익률, 평균.분산 지배원리
제2절 기대수익률, 분산 및 변동계수 계산 문제
Chapter 03 위험의 관리
제1절 위험을 관리하는 방법
제2절 포트폴리오 이론
Chapter 04 투자분석의 기본도구
제1절 화폐의 시간가치
제2절 미래가치와 현재가치 계산 연습
제3절 투자의 현금흐름 분석
제4절 현금흐름 계산 문제
Chapter 05 부동산 투자분석기법
제1절 할인현금흐름분석법
제2절 할인법 계산 문제
제3절 비할인법
제4절 비할인법 계산 문제

PART 06 금융론

Chapter 01 금융의 이해
제1절 금융의 구분
제2절 금융의 위험
Chapter 02 대출금액, 대출금리 및 상환방식
제1절 대출금액 계산 문제
제2절 저당 잔금 계산 문제
제3절 변동금리상품과 고정금리상품
제4절 상환방식의 이해
제5절 상환방식 계산 문제
Chapter 03 주택저당채권 유동화제도
Chapter 04 부동산투자회사
Chapter 05 기타 부동산 관련 금융제도
제1절 프로젝트 대출
제2절 주택담보노후연금, 한국주택금융공사
제3절 부동산신탁
제4절 자산의 유동화

PART 07 부동산 개발론

Chapter 01 부동산 개발론
제1절 개발의 이해
제2절 개발의 위험
제3절 개발을 위한 부동산 분석
제4절 입지계수 계산 문제
제5절 공영개발의 방식
제6절 민간개발의 방식
제7절 민간투자사업방식(민자사업)
Chapter 02 부동산 관리
제1절 부동산 관리의 구분
제2절 비율임대차 계산 문제
제3절 건물의 생애주기
Chapter 03 부동산 마케팅
Chapter 04 부동산 중개론
제1절 중개계약의 종류
제2절 공인중개사에 관한 법률
제3절 에스크로 제도
제4절 권리분석
제5절 권리분석의 구체적 내용

PART 08 토지 경제와 지리 경제

Chapter 01 지대ㆍ지가이론
Chapter 02 도시 내부 구조이론
Chapter 03 공업입지론
Chapter 04 상업입지론
제1절 상업입지 이론
제2절 상업입지 계산 문제

PART 09 감정평가론

Chapter 01 부동산 가치이론
Chapter 02 지역분석과 개별분석
Chapter 03 부동산 가격원칙
Chapter 04 감정평가제도
제1절 감정평가에 관한 규칙
제2절 표준지의 조사 및 평가
Chapter 05 감정평가방식
제1절 감정평가방식의 분류
제2절 시산가액의 조정
제3절 거래사례비교법, 공시지가기준법
제4절 비교방식 계산 문제
제5절 원가법
제6절 원가법 계산 문제
제7절 수익환원법
제8절 수익환원법 계산 문제
제9절 임대료 평가
제10절 물건별 주된 감정평가
Chapter 06 부동산 가격공시제도
"""

prompt_template = """너는 감정평가사 "부동산학원론" 과목의 출제 위원급 전문가야.
아래에 제공된 객관식 문제의 텍스트와 보기를 읽고 이 문제에 대한 태그 데이터를 생성해줘. (기존 해설은 무시해도 좋아)

[부동산학원론 목차 분류]
{taxonomy}

[문제 정보]
- 문제: {question}
- 보기: {options}

[작업 지시사항]
이 문제에 대해 분석하여 아래 JSON 형식에 맞게 값을 채워줘.
- subject: "부동산학원론"
- unit: 위 목차의 "PART" 이름 (예: "PART 01 부동산학 총론") 중 가장 정확하게 일치하는 하나.
- sub_unit: 위 목차의 "Chapter" 이름 (예: "Chapter 02 부동산의 개념") 중 가장 정확하게 일치하는 하나.
- concept: 위 목차에 하위 "절"이 있다면 해당 절 이름, 없다면 Chapter 내의 핵심 키워드를 10자 이내로 작성해.
- difficulty: "상", "중", "하" 중 하나.
- question_type: 이 문제의 형태나 필요한 스킬 (예: "이론", "계산문제", "박스조합형(ㄱ, ㄴ, ㄷ)", "옳은 것 고르기", "틀린 것 고르기")
- source: "감정평가사 1차"
- year: "{year}"

오직 위 8개 필드를 포함하는 유효한 JSON 객체 하나만 출력해. 다른 텍스트는 절대 붙이지 마.
"""

def is_realestate(q):
    # period is '1', number is between 81 and 120
    period = q.get('period', '2')
    num = int(q.get('number', 0))
    if period == '1' and 81 <= num <= 120:
        return True
    return False

def run_tagging():
    re_qs = [q for q in questions if is_realestate(q)]
    print(f"Total 부동산학원론 questions: {len(re_qs)}")

    pending_qs = [q for q in re_qs if 'tags' not in q or q['tags'].get('subject') != '부동산학원론']
    print(f"Pending 부동산학원론 questions to tag: {len(pending_qs)}")

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
    print("Finished tagging 부동산학원론! DB updated.")

    import shutil
    shutil.copy(db_path, 'viewer/src/data/questions_db.json')
    print("Viewer DB updated.")

if __name__ == '__main__':
    run_tagging()
