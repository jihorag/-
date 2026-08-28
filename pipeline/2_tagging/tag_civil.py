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
PART 01 민법총칙

Chapter 01. 법원
- 민법의 법원(法源)
- 물권법의 법원(法源)
Chapter 02. 법률관계와 권리의무
- 법률관계
- 권리와 의무
Chapter 03. 법률관계의 변동
Chapter 04. 법률행위
- 법률행위의 종류
- 법률행위의 해석
Chapter 05. 자연인
- 권리능력
- 의사능력
- 행위능력
- 부재와 실종
Chapter 06. 법인
- 법인의 권리능력
- 법인의 기관
- 법인의 불법행위능력
- 정관변경·보충과 법인의 감독
- 권리능력 없는 사단·재단
Chapter 07. 권리의 객체
- 물건
- 부동산과 동산
- 주물과 종물
- 원물과 과실(果實)
Chapter 08. 법률행위의 목적
- 확실성, 실현가능성, 적법성
- 반사회질서의 법률행위
- 불공정한 법률행위
Chapter 09. 의사표시
- 진의 아닌 의사표시
- 통정허위표시
- 착오
- 사기·강박에 의한 의사표시
- 의사표시의 효력발생
Chapter 10. 법률행위의 대리
- 대리권
- 대리행위와 대리효과
- 복대리
- 표현대리
- 무권대리
Chapter 11. 무효와 취소
- 취소와 추인
- 무효
- 유동적 무효
Chapter 12. 조건과 기한, 기간
- 조건
- 기한
- 기간
Chapter 13. 소멸시효
- 소멸시효 일반
- 소멸시효의 요건
- 소멸시효의 중단·정지
- 소멸시효완성의 효과

PART 02 물권법

Chapter 01. 물권법 총설
Chapter 02. 점유와 점유권
Chapter 03. 법률행위 부동산 물권변동
- 등기부
- 등기의 절차
- 등기의 효력
- 명인방법
Chapter 04. 법률행위 아닌 부동산 물권변동
Chapter 05. 선의취득
Chapter 06. 물권적 청구권
Chapter 07. 본권에 기한 물권적 청구권
Chapter 08. 점유권에 기한 물권적 청구권
Chapter 09. 본권과 점유권과의 관계
Chapter 10. 물권의 소멸
Chapter 11. 법률규정상의 소유권 제한
- 소유권 일반
- 주위토지통행권
- 그 외 상린관계
Chapter 12. 집합건물법
Chapter 13. 취득시효
- 점유취득시효
- 등기부취득시효
- 취득시효의 중단
Chapter 14. 선점·습득·발견
Chapter 15. 첨부 (부합·혼화·가공)
Chapter 16. 공동소유
- 공유
- 합유
- 총유
Chapter 17. 명의신탁
- 명의신탁 일반
- 부동산실권자 명의등기에 관한 법률
Chapter 18. 지상권
- 지상권
- 분묘기지권
Chapter 19. 법정지상권·관습법상 법정지상권
- 법정지상권, 관습법상 법정지상권
- 일괄경매청구권
Chapter 20. 지역권
Chapter 21. 전세권
Chapter 22. 유치권
Chapter 23. 질권
- 동산질권
- 권리질권
Chapter 24. 저당권
Chapter 25. 근저당권
Chapter 26. 공동저당
Chapter 27. 가등기담보 등에 관한 법률
Chapter 28. 신의성실의 원칙
"""

prompt_template = """너는 감정평가사 "민법" 과목의 출제 위원급 전문가야.
아래에 제공된 객관식 문제의 텍스트와 보기를 읽고 이 문제에 대한 태그 데이터를 생성해줘. (기존 해설은 무시해도 좋아)

[민법 목차 분류]
{taxonomy}

[문제 정보]
- 문제: {question}
- 보기: {options}

[작업 지시사항]
이 문제에 대해 분석하여 아래 JSON 형식에 맞게 값을 채워줘.
- subject: "민법"
- unit: 위 목차의 "PART" 이름 (예: "PART 01 민법총칙") 중 가장 정확하게 일치하는 하나.
- sub_unit: 위 목차의 "Chapter" 이름 (예: "Chapter 10. 법률행위의 대리") 중 가장 정확하게 일치하는 하나.
- concept: 위 목차에 하위 세부 내용('-' 로 표시된 항목)이 있다면 해당 내용, 없다면 Chapter 내의 핵심 키워드를 15자 이내로 작성해.
- difficulty: "상", "중", "하" 중 하나.
- question_type: 이 문제의 형태나 필요한 스킬 (예: "판례문제", "이론", "박스조합형(ㄱ, ㄴ, ㄷ)", "옳은 것 고르기", "틀린 것 고르기")
- source: "감정평가사 1차"
- year: "{year}"

오직 위 8개 필드를 포함하는 유효한 JSON 객체 하나만 출력해. 다른 텍스트는 절대 붙이지 마.
"""

def is_civil(q):
    # period is '1' or '1_old', number is between 1 and 40
    period = q.get('period', '2')
    num = int(q.get('number', 0))
    if period in ['1', '1_old'] and 1 <= num <= 40:
        return True
    return False

def run_tagging():
    civil_qs = [q for q in questions if is_civil(q)]
    print(f"Total 민법 questions: {len(civil_qs)}")

    pending_qs = [q for q in civil_qs if 'tags' not in q or q['tags'].get('subject') != '민법']
    print(f"Pending 민법 questions to tag: {len(pending_qs)}")

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
    print("Finished tagging 민법! DB updated.")

    import shutil
    shutil.copy(db_path, 'viewer/src/data/questions_db.json')
    print("Viewer DB updated.")

if __name__ == '__main__':
    run_tagging()
