import json
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

# OpenAI settings
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
MODEL_NAME = "gpt-5.4-mini-2026-03-17"

db_path = "questions_db.json"
with open(db_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

taxonomy = """
PART 01 국토의 계획 및 이용에 관한 법률
Chapter 01 총칙
제1절 용어의 정의
제2절 도시·군계획의 법적 지위
Chapter 02 광역계획권 및 광역도시계획
제1절 광역계획권의 지정
제2절 광역도시계획
Chapter 03 도시·군기본계획
제1절 도시·군기본계획의 수립 및 확정(승인)
제2절 도시·군기본계획의 정비
Chapter 04 도시·군관리계획
제1절 도시·군관리계획의 입안
제2절 도시·군관리계획의 결정
제3절 공간재구조화계획
Chapter 05 용도지역
제1절 용도지역의 종류와 지정절차
제2절 용도지역 지정의 효과
Chapter 06 용도지구 및 용도구역
제1절 용도지구
제2절 용도구역
제3절 둘 이상의 용도지역 등에 걸치는 경우의 행위제한
Chapter 07 기반시설과 도시·군계획시설
제1절 기반시설과 도시·군계획시설
제2절 매수청구 및 실효 등
Chapter 08 지구단위계획구역과 지구단위계획
제1절 지구단위계획구역
제2절 지구단위계획
Chapter 09 개발행위의 허가
제1절 허가대상 개발행위
제2절 개발행위허가기준
Chapter 10 성장관리계획구역 및 성장관리계획
제1절 성장관리계획구역
제2절 성장관리계획
Chapter 11 개발밀도관리구역과 기반시설부담구역
제1절 개발밀도관리구역
제2절 기반시설부담구역
Chapter 12 보칙 및 벌칙
제1절 타인토지에의 출입 등
제2절 청문
제3절 시범도시
제4절 도시계획위원회
제5절 벌칙

PART 02 건축법
Chapter 01 용어의 정의 및 적용대상물
제1절 용어의 정의
제2절 건축법 적용대상물
Chapter 02 건축법 적용대상 행위
제1절 건축 및 대수선
제2절 건축물의 용도변경
Chapter 03 건축허가 및 건축신고
제1절 건축허가
제2절 건축신고
제3절 허가(신고)에 따른 인·허가 등의 의제사항
제4절 가설건축물 및 사용승인
Chapter 04 대지와 도로
제1절 대지
제2절 도로
Chapter 05 건축물의 구조 및 면적산정방법
제1절 건축물의 구조
제2절 대지가 지역·지구 또는 구역에 걸치는 경우
제3절 건폐율·용적률
제4절 건축물의 면적 및 높이 등의 산정방법
Chapter 06 건축물의 높이제한 및 건축협정 등
제1절 건축물의 높이제한
제2절 특별건축구역
제3절 건축협정
제4절 결합건축
제5절 이행강제금
제6절 건축분쟁전문위원회(분쟁위원회)

PART 03 도시 및 주거환경정비법
Chapter 01 총칙
제1절 용어의 정의
Chapter 02 기본계획의 수립 및 정비구역의 지정
제1절 도시 및 주거환경정비 기본방침
제2절 도시·주거환경정비기본계획(기본계획)
제3절 정비계획의 입안 및 정비구역의 지정
제4절 정비구역에서의 행위제한
제5절 정비구역등의 해제
Chapter 03 정비사업의 시행
제1절 정비사업의 시행방법
제2절 정비사업의 시행자
제3절 재개발·재건축사업의 대행자 등
제4절 조합설립추진위원회 및 정비사업조합
제5절 사업시행계획 등
제6절 정비사업시행을 위한 조치
제7절 관리처분계획 등
제8절 공사완료에 따른 조치 등
Chapter 04 비용의 부담 등

PART 04 공간정보의 구축 및 관리 등에 관한 법률
Chapter 01 총칙
Chapter 02 측량
Chapter 03 지적
Chapter 04 지적공부(토지정보등록부)
Chapter 05 토지의 이동
Chapter 06 보칙

PART 05 부동산등기법
Chapter 01 총칙
Chapter 02 등기소와 등기관
Chapter 03 등기부 등
Chapter 04 등기절차
Chapter 05 표시에 관한 등기
Chapter 06 권리에 관한 등기
Chapter 07 이의신청

PART 06 국유재산법
Chapter 01 총칙
Chapter 02 총괄청
Chapter 03 행정재산
Chapter 04 일반재산
Chapter 05 지식재산 관리·처분의 특례
Chapter 06 대장과 보고
Chapter 07 보칙

PART 07 부동산 가격공시에 관한 법률
Chapter 01 용어의 정의
Chapter 02 표준지공시지가
제1절 표준지 선정 및 의뢰
제2절 조사·평가 및 의견청취
제3절 조사·평가보고서 제출 및 공시
제4절 이의신청 및 적용 등
Chapter 03 개별공시지가
Chapter 04 주택가격의 공시
제1절 표준주택가격
제2절 표준주택의 선정 및 의뢰
제3절 조사·산정 보고서 제출 및 공시
제4절 개별주택가격
제5절 공동주택가격
제6절 공동주택의 조사·산정
Chapter 05 비주거용 부동산 가격공시
제1절 비주거용 표준부동산
제2절 비주거용 개별부동산
제3절 비주거용 집합부동산
Chapter 06 부동산가격공시위원회
제1절 중앙부동산가격공시위원회
제2절 시·군·구부동산가격공시위원회

PART 08 감정평가 및 감정평가사에 관한 법률
Chapter 01 총칙
제1절 용어의 정의(제2조)
제2절 감정평가
Chapter 02 감정평가사
제1절 업무와 자격
제2절 시험
제3절 등록 등
제4절 권리와 의무
Chapter 03 감정평가법인
Chapter 04 한국감정평가사협회
Chapter 05 징계
Chapter 06 과징금
Chapter 07 보칙
Chapter 08 벌칙

PART 09 동산·채권 등의 담보에 관한 법률
Chapter 01 총칙
Chapter 02 동산담보권
Chapter 03 채권담보권
Chapter 04 담보등기
Chapter 05 지식재산권의 담보에 관한 특례
Chapter 06 벌칙
"""

prompt_template = """너는 감정평가사 "감정평가관계법규" 과목의 출제 위원급 전문가야.
아래에 여러 객관식 문제의 텍스트와 보기가 배열(JSON) 형태로 주어질 거야. 각 문제에 대해 태그 데이터를 생성해서, 동일한 순서의 배열(JSON Array) 형태로 반환해줘.

[감정평가관계법규 목차 분류]
{taxonomy}

[작업 지시사항]
각 문제 객체에 대해 아래 필드를 가지는 JSON 객체를 만들어, 전체를 하나의 JSON 배열(`[]`)로 출력해.
- id: 입력된 문제의 "id"
- subject: "감정평가관계법규"
- unit: 위 목차의 "PART" 이름 (예: "PART 01 국토의 계획 및 이용에 관한 법률") 중 가장 정확하게 일치하는 하나. 만약 위 9개 법률 범위에 해당하지 않는 문제(예: 세법, 공인중개사법 등)라면 "Out of Scope" 라고 적어.
- sub_unit: 위 목차의 "Chapter" 이름 중 하나. 범위 밖이라면 "Out of Scope"
- concept: 핵심 키워드를 10자 이내로 작성해.
- difficulty: 난이도 (1: 아주 쉬움 ~ 5: 아주 어려움).
- question_type: (예: "조문암기", "박스조합형", "옳은 것 고르기", "틀린 것 고르기"). '옳지 않은 것은?' 등은 "틀린 것 고르기"로 분류.
- in_scope: 출제범위 포함 시 true, 아니면 false (boolean).
- source: "감정평가사 1차" 또는 "공인중개사 2차"
- year: 해당 문제의 연도

반드시 JSON 배열 형태로만 출력해.
"""

def is_law(q):
    exam = q.get('exam', '감정평가사')
    period = q.get('period', '2')
    num = int(q.get('number', 0))
    
    # 1. 감정평가사 관계법규 (2교시 1~40번)
    if exam == '감정평가사' and period == '2' and 1 <= num <= 40:
        return True
    # 2. 공인중개사 2차 (g2 1~120번 - 중개사법, 공법, 공시법, 세법 모두 포함)
    if exam == '공인중개사' and period == 'g2' and 1 <= num <= 120:
        return True
        
    return False

def run_tagging():
    law_qs = [q for q in questions if is_law(q)]
    print(f"Total 감정평가관계법규 questions: {len(law_qs)}")

    pending_qs = [q for q in law_qs if 'tags' not in q or q['tags'].get('subject') != '감정평가관계법규']
    print(f"Pending 감정평가관계법규 questions to tag: {len(pending_qs)}")

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
            # Handle both formats: direct array or wrapped in {"results": [...]}
            if isinstance(result_json, list):
                return result_json
            elif "results" in result_json:
                return result_json["results"]
            else:
                return list(result_json.values())[0]
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            if 'response' in locals():
                print(response.text)
            return None

    count = 0
    batch_size = 10
    
    # Create a lookup dictionary for pending questions
    pending_dict = {q['id']: q for q in pending_qs if 'id' in q}
    
    for i in range(0, len(pending_qs), batch_size):
        batch = pending_qs[i:i+batch_size]
        print(f"Tagging batch {i//batch_size + 1} ({i+1} to {min(i+batch_size, len(pending_qs))})...")
        
        results = call_openai_batch(batch)
        if results and isinstance(results, list):
            for res in results:
                q_id = res.get('id')
                if q_id in pending_dict:
                    # remove 'id' from tag object before saving
                    tag_data = {k: v for k, v in res.items() if k != 'id'}
                    pending_dict[q_id]['tags'] = tag_data
                    count += 1
                    
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            
            # 실시간으로 웹 앱에 반영되도록 뷰어 폴더로 바로 복사
            import shutil
            shutil.copy(db_path, 'viewer/src/data/questions_db.json')
            
            print(f"-> Batch saved & Viewer DB updated ({count} tagged so far)")
        else:
            print("Failed to get valid response for this batch, skipping...")

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print("Finished tagging 감정평가관계법규! DB updated.")

    import shutil
    shutil.copy(db_path, 'viewer/src/data/questions_db.json')
    print("Viewer DB updated.")

if __name__ == '__main__':
    run_tagging()
