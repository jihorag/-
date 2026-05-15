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
PART 01 재무회계
Chapter 01 개념체계
1절 목적
2절 개념체계와 기준서
3절 일반목적재무보고
4절 유용한 재무정보의 질적 특성
5절 계속기업가정, 보고기업
6절 재무제표의 요소
7절 인식과 제거
8절 측정
9절 공정가치
10절 자본과 자본유지개념

Chapter 02 재무제표 표시
1절 재무제표
2절 재무상태표
3절 포괄손익계산서

Chapter 03 재고자산
1절 재고자산의 최초측정
2절 기말재고금액
3절 재고자산의 인식시점
4절 기말재고금액의 추정
5절 감모손실과 평가손실
6절 농림어업

Chapter 04 유형자산
1절 유형자산의 인식 및 최초측정
2절 유형자산의 후속지출
3절 유형자산의 후속측정
4절 유형자산의 손상
5절 차입원가 자본화
6절 차입원가 자본화의 순서

Chapter 05 무형자산
1절 무형자산의 정의 및 인식과 측정
2절 무형자산의 상각
3절 무형자산의 제거와 손상
4절 영업권

Chapter 06 투자부동산
1절 투자부동산의 의의
2절 투자부동산의 최초측정
3절 투자부동산의 후속측정
4절 투자부동산의 계정대체

Chapter 07 금융자산
1절 금융상품
2절 현금 및 현금성자산
3절 매출채권과 매입채무
4절 기타금융자산
5절 투자지분상품
6절 투자채무상품
7절 금융자산의 손상과 재분류
8절 받을어음의 할인

Chapter 08 금융부채
1절 금융부채의 인식과 측정
2절 사채
3절 사채의 후속측정
4절 금융부채로 분류하는 상환우선주

Chapter 09 충당부채, 우발부채
1절 충당부채의 인식요건
2절 충당부채의 추정
3절 기타의 충당부채
4절 충당부채의 변제 및 변동
5절 우발부채와 우발자산

Chapter 10 자본
1절 자본의 의의
2절 자본의 분류
3절 주식의 발행
4절 증자와 감자
5절 자기주식
6절 배당금의 배분
7절 이익잉여금 처분

Chapter 11 복합금융상품
1절 전환사채
2절 전환권의 행사
3절 전환사채의 재매입 및 조건변경
4절 신주인수권부사채

Chapter 12 고객과의 계약에서 생기는 수익
1절 수익의 정의
2절 수익 인식의 5단계
3절 기타의 고려사항

Chapter 13 건설계약
1절 건설계약
2절 손실이 예상되는 공사
3절 진행률을 신뢰성 있게 측정하기 어려울 때

Chapter 14 종업원급여
1절 종업원급여
2절 퇴직급여제도
3절 확정급여제도의 재무상태표 표시

Chapter 15 주식기준보상
1절 주식결제형 주식기준보상
2절 현금결제형 주식기준보상

Chapter 16 리스
1절 금융리스로 분류하는 사례
2절 리스이용자 회계처리
3절 리스부채 재측정 및 리스변경
4절 리스제공자 회계처리

Chapter 17 법인세회계
1절 회계이익과 과세소득의 차이
2절 법인세회계
3절 자본에 가감하는 법인세효과

Chapter 18 주당이익
1절 주당이익(EPS)
2절 희석주당이익

Chapter 19 회계변경 및 오류수정
1절 회계변경
2절 오류수정

Chapter 20 현금흐름표
1절 현금흐름표
2절 영업활동 현금흐름 : 직접법 또는 간접법
3절 투자활동 및 재무활동 현금흐름

Chapter 21 재무제표 분석
1절 안전성비율
2절 수익성비율
3절 활동성비율

Chapter 22 관계기업투자주식
1절 관계기업

Chapter 23 보고기간 후 사건, 환율변동효과
1절 보고기간 후 사건의 유형 및 회계처리
2절 수정을 요하는 보고기간 후 사건
3절 보고기간 말 외화자산, 부채의 환산

PART 02 원가관리회계

Chapter 01 제조기업의 원가흐름
1절 원가의 다양한 분류기준
2절 제조기업의 원가흐름

Chapter 02 개별원가계산
1절 실제개별원가계산
2절 정상개별원가계산
3절 배부차이 및 배부차이 조정

Chapter 03 보조부문의 원가배부
1절 보조부문이 하나인 경우
2절 보조부문이 여러 개인 경우

Chapter 04 활동기준원가계산
1절 활동기준원가계산

Chapter 05 종합원가계산
1절 완성품환산량
2절 평균법과 선입선출법
3절 공손

Chapter 06 결합원가계산
1절 결합원가란?
2절 결합원가 배부방법
3절 결합원가 추가고려사항

Chapter 07 전부원가계산, 변동원가계산
1절 전부원가계산, 변동원가계산, 초변동원가계산
2절 각 원가계산방법들의 유용성과 한계점

Chapter 08 원가함수의 추정
1절 원가함수의 추정

Chapter 09 원가-조업도-이익분석(CVP분석)
1절 원가-조업도-이익분석
2절 손익분기점 및 목표이익
3절 안전한계
4절 기타 CVP분석

Chapter 10 표준원가계산
1절 표준원가계산
2절 원가차이 분석

Chapter 11 관련원가와 의사결정
1절 의사결정의 유형
2절 증분접근법(차액접근법)
3절 제약요인하의 의사결정

Chapter 12 대체가격결정
1절 대체가격이란?
2절 대체가격 결정방법

Chapter 13 종합예산
1절 종합예산

Chapter 14 투자중심점 성과평가
1절 투자중심점 성과평가

Chapter 15 최신 원가관리회계
1절 균형성과표
2절 다양한 원가계산
3절 품질원가
"""

prompt_template = """너는 감정평가사 회계학 과목의 출제 위원급 전문가야.
아래에 제공된 객관식 문제의 텍스트, 보기, 해설을 읽고 이 문제에 대한 태그 데이터를 생성해줘. (기존 해설은 무시해도 좋아)

[회계학 목차 분류]
{taxonomy}

[문제 정보]
- 문제: {question}
- 보기: {options}

[작업 지시사항]
이 문제에 대해 분석하여 아래 JSON 형식에 맞게 값을 채워줘.
- subject: "회계학"
- unit: 위 목차의 "PART" 이름 (예: "PART 01 재무회계" 또는 "PART 02 원가관리회계")
- sub_unit: 위 목차의 "Chapter" 이름 (예: "Chapter 03 재고자산") 중 가장 정확하게 일치하는 하나.
- concept: 위 목차의 "절" 이름 (예: "2절 기말재고금액") 중 가장 정확하게 일치하는 하나. (위계에 맞게 선택할 것)
- difficulty: "상", "중", "하" 중 하나.
- question_type: 이 문제의 형태나 필요한 스킬 (예: "계산문제", "재무제표 분석", "말문제(이론)", "옳은 것 고르기")
- source: "감정평가사 1차"
- year: "{year}"

오직 위 8개 필드를 포함하는 유효한 JSON 객체 하나만 출력해. 다른 텍스트는 절대 붙이지 마.
"""

def is_accounting(q):
    # period is '2', number is between 41 and 80
    period = q.get('period', '2')
    num = int(q.get('number', 0))
    if period == '2' and 41 <= num <= 80:
        return True
    return False

def run_tagging():
    acc_qs = [q for q in questions if is_accounting(q)]
    print(f"Total Accounting questions: {len(acc_qs)}")

    pending_qs = [q for q in acc_qs if 'tags' not in q or q['tags'].get('subject') != '회계학']
    print(f"Pending Accounting questions to tag: {len(pending_qs)}")

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
    print("Finished tagging Accounting! DB updated.")

    import shutil
    shutil.copy(db_path, 'viewer/src/data/questions_db.json')
    print("Viewer DB updated.")

if __name__ == '__main__':
    run_tagging()
