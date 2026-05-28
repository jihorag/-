#!/usr/bin/env python3
"""단원 3 Batch 01 — 입문 10개 (1~10)."""
import json
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')

PROBLEMS = [
    {
        'id': 'practice-3-001', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 1, 'points': 10,
        'topic': '건물 평가 — 기초',
        'body': """## 문제 1 — 건물의 정의와 평가 방식 (10점)

부동산 평가에서 건물의 정의와 주된 평가방식을 약술하시오.""",
        'modelAnswer': """## Ⅰ. 서론

건물은 토지에 정착된 인공 구조물. 주된 평가방식은 원가법.


## Ⅱ. 본론

### 1. 건물의 정의
- 토지 정착물
- 지붕·기둥·벽 갖춘 구조물
- 건축법상 건축물

### 2. 주된 평가방식
- 원가법 (감정평가규칙 §15)
- 보조: 거래사례비교법

### 3. 적용 이유
- 건물은 재생산 가능
- 감가 산정 명확


## Ⅲ. 결론

건물 = 원가법 중심. 토지와 별도 산정.


## ★ 핵심 학습 포인트

- 건물 = 정착 구조물
- 주방식 = 원가법
- 보조 = 비교법
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['건물 정의', '원가법', '평가방식']
    },
    {
        'id': 'practice-3-002', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 1, 'points': 10,
        'topic': '재조달원가',
        'body': """## 문제 2 — 재조달원가의 개념 (10점)

원가법에서 재조달원가의 의의를 약술하시오.""",
        'modelAnswer': """## Ⅰ. 서론

재조달원가는 기준시점에 대상과 동일·유사 건물을 새로 건축하는 데 드는 비용.


## Ⅱ. 본론

### 1. 의의
- 신축 시점 비용
- 동일·유사 효용

### 2. 구성
- 직접비: 자재·노무·경비
- 간접비: 일반관리·이윤·금융비

### 3. 산정 방법
- 직접법: 견적
- 간접법: 단위면적당 표준단가


## Ⅲ. 결론

재조달원가는 적산가액의 출발점.


## ★ 핵심 학습 포인트

- 신축 가정 비용
- 직접비 + 간접비
- 단위면적당 표준단가 활용
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['재조달원가', '직접비·간접비', '표준단가']
    },
    {
        'id': 'practice-3-003', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 2, 'points': 15,
        'topic': '감가수정',
        'body': """## 문제 3 — 감가수정의 유형 (15점)

감가수정의 3대 유형을 약술하시오.""",
        'modelAnswer': """## Ⅰ. 서론

감가수정은 재조달원가에서 가치 감소분을 차감하는 절차. 물리·기능·경제 3대 유형.


## Ⅱ. 본론

### 1. 물리적 감가
- 시간 경과·사용으로 인한 마모
- 정액법·정률법·관찰법

### 2. 기능적 감가
- 설비 노후·기능 부족
- 평면 비효율·설비 부족

### 3. 경제적 감가
- 외부 환경 변화
- 입지·도시 변화
- 인근 도로 확장·환경 악화


## Ⅲ. 결론

3가지 모두 검토 후 합산 적용.


## ★ 핵심 학습 포인트

- 물리·기능·경제 3대
- 외부 환경 = 경제적
- 합산 적용
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['감가수정', '3대 유형', '합산 적용']
    },
    {
        'id': 'practice-3-004', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 2, 'points': 15,
        'topic': '정액법 감가',
        'body': """## 문제 4 — 정액법 감가 (15점)

### 자료
- 재조달원가: 1,000,000,000원
- 경과연수: 15년
- 경제적 내용연수: 50년
- 잔존가치율: 10%

### 물음
정액법으로 적산가액을 산정하시오.""",
        'modelAnswer': """## Ⅰ. 서론

정액법은 매년 동일한 감가액을 차감. 건물에 가장 흔히 사용.


## Ⅱ. 본론

### 1. 감가총액
1,000,000,000 × (1 - 0.10) = 900,000,000원

### 2. 연 감가액
900,000,000 / 50 = 18,000,000원/년

### 3. 누적 감가액
18,000,000 × 15 = 270,000,000원

### 4. 적산가액
1,000,000,000 - 270,000,000 = 730,000,000원


## Ⅲ. 결론

적산가액 7.30억원.


## ★ 핵심 학습 포인트

- 정액법 = (RC × 감가율)/n × 경과
- 잔존가치율 고려
- 건물에 표준
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['정액법', '잔존가치율', '경과연수']
    },
    {
        'id': 'practice-3-005', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 2, 'points': 15,
        'topic': '내용연수',
        'body': """## 문제 5 — 내용연수의 유형 (15점)

물리적·경제적·관찰 내용연수의 차이를 약술하시오.""",
        'modelAnswer': """## Ⅰ. 서론

내용연수는 건물의 사용 가능 기간. 3가지 개념 구분 필요.


## Ⅱ. 본론

### 1. 물리적 내용연수
- 물리적 사용가능 한계
- 구조·자재 기준

### 2. 경제적 내용연수
- 경제적 효용 한계
- 통상 평가에 사용

### 3. 관찰 내용연수
- 실제 사용 상태 관찰
- 유지보수 상태 반영

### 4. 관계
- 경제 ≤ 물리
- 관찰 = 실측치


## Ⅲ. 결론

평가는 경제적 내용연수가 표준.


## ★ 핵심 학습 포인트

- 물리·경제·관찰 3유형
- 평가 = 경제적
- 경제 ≤ 물리
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['내용연수', '경제적 내용연수', '관찰']
    },
    {
        'id': 'practice-3-006', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 1, 'points': 10,
        'topic': '복합부동산',
        'body': """## 문제 6 — 복합부동산의 정의 (10점)

복합부동산의 정의와 평가 특징을 약술하시오.""",
        'modelAnswer': """## Ⅰ. 서론

복합부동산은 토지+건물이 일체로 효용을 발휘하는 부동산.


## Ⅱ. 본론

### 1. 정의
- 토지·건물 일체
- 분리 곤란
- 시장에서 일체 거래

### 2. 평가 특징
- 토지·건물 별도 산정 후 합산
- 또는 일체 평가
- 3방식 시산조정

### 3. 적용 사례
- 단독주택
- 상가건물
- 오피스빌딩


## Ⅲ. 결론

복합부동산은 일체 시장가치 = 토지가 + 건물가 + 일체효용가산.


## ★ 핵심 학습 포인트

- 토지+건물 일체
- 별도 또는 일체 평가
- 일체효용 가산 가능
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['복합부동산', '일체 평가', '효용 가산']
    },
    {
        'id': 'practice-3-007', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 2, 'points': 15,
        'topic': '구분소유',
        'body': """## 문제 7 — 구분소유 부동산의 정의 (15점)

집합건물의 구분소유 의의와 평가 특징을 약술하시오.""",
        'modelAnswer': """## Ⅰ. 서론

구분소유는 1동의 건물을 구획하여 각각 독립한 소유권 대상으로 한 것. 집합건물법 적용.


## Ⅱ. 본론

### 1. 정의
- 1동 건물의 구분 소유
- 전용부분 + 공용부분
- 대지권 별도

### 2. 평가 특징
- 거래사례비교법 중심
- 층·향·조망 보정
- 대지권 별도 계산

### 3. 가격 구성
- 전용면적 단가
- 공용·대지권 포함

### 4. 적용
- 아파트·오피스텔
- 구분상가
- 집합건물


## Ⅲ. 결론

집합건물 = 거래사례비교법 중심, 층·향·조망 핵심.


## ★ 핵심 학습 포인트

- 구분소유 = 1동 분할
- 비교법 중심
- 층·향·조망 보정
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['구분소유', '집합건물', '대지권']
    },
    {
        'id': 'practice-3-008', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 2, 'points': 15,
        'topic': '임대료',
        'body': """## 문제 8 — 임대료의 정의 (15점)

임대료의 개념과 평가 방법을 약술하시오.""",
        'modelAnswer': """## Ⅰ. 서론

임대료는 부동산 사용권의 대가. 보증금·월세·관리비로 구성.


## Ⅱ. 본론

### 1. 구성
- 보증금
- 월차임
- 관리비 (실비)

### 2. 평가 방법
- 임대사례비교법 (주된 방법)
- 적산법 (원가 기반)
- 수익분석법 (수익 기반)

### 3. 임대사례비교법
- 사례 임대료 → 시점·지역·개별 보정

### 4. 적산법
- 기초가액 × 기대이율 + 필요제경비
- 신축·자가임대에 적합


## Ⅲ. 결론

임대료 평가 = 임대사례비교법 중심, 보조 적산·수익.


## ★ 핵심 학습 포인트

- 보증금+월세+관리비
- 비교·적산·수익 3방식
- 주방식 = 비교법
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['임대료', '3방식', '임대사례비교']
    },
    {
        'id': 'practice-3-009', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 2, 'points': 15,
        'topic': '적산법',
        'body': """## 문제 9 — 적산법 임대료 (15점)

### 자료
- 기초가액 (대상가액): 2,000,000,000원
- 기대이율: 6%
- 필요제경비: 연 30,000,000원

### 물음
연·월 임대료를 산정하시오.""",
        'modelAnswer': """## Ⅰ. 서론

적산법은 기초가액 × 기대이율 + 필요제경비로 임대료 산정. 신축·자가임대에 활용.


## Ⅱ. 본론

### 1. 기대이익
2,000,000,000 × 0.06 = 120,000,000원/년

### 2. 연 임대료
120,000,000 + 30,000,000 = 150,000,000원/년

### 3. 월 임대료
150,000,000 / 12 = 12,500,000원/월


## Ⅲ. 결론

연 임대료 1.5억, 월 1,250만원.


## ★ 핵심 학습 포인트

- 적산법 = 기초가액 × 기대이율 + 경비
- 기대이율 ≠ 환원이율
- 신축·자가에 적합
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['적산법', '기대이율', '필요제경비']
    },
    {
        'id': 'practice-3-010', 'subject': '감정평가실무', 'chapter': '3',
        'source': 'practice-set', 'difficulty': 1, 'points': 10,
        'topic': '임대 평가',
        'body': """## 문제 10 — 임대료 평가 방식 3가지 (10점)

임대료 평가 3방식을 약술하시오.""",
        'modelAnswer': """## Ⅰ. 서론

임대료 평가는 임대사례비교·적산·수익분석 3방식.


## Ⅱ. 본론

### 1. 임대사례비교법
- 유사 사례 임대료 → 보정
- 주된 방법

### 2. 적산법
- 기초가액 × 기대이율 + 경비
- 신축·자가임대

### 3. 수익분석법
- 임차인 매출 → 부담 가능 임대료
- 영업용에 활용

### 4. 시산조정
- 3방식 비교 후 결정


## Ⅲ. 결론

3방식 시산 후 결정. 비교법 중심.


## ★ 핵심 학습 포인트

- 비교·적산·수익 3방식
- 주방식 = 비교법
- 영업용 = 수익분석법
""",
        'modelAnswerSource': 'ai-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': ['임대료 3방식', '시산조정', '비교법']
    },
]


def main():
    path = DATA_DIR / '3.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    existing_ids = {q['id'] for q in data['questions']}
    new = [p for p in PROBLEMS if p['id'] not in existing_ids]
    data['questions'].extend(new)
    data['count'] = len(data['questions'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"3 Batch 01: +{len(new)}개 → 전체 {data['count']}문제")


if __name__ == '__main__':
    main()
