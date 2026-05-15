import json

raw = """
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

import re
lines = raw.strip().split('\n')
re_taxonomy = []
cur_part = None
cur_chapter = None

for l in lines:
    l = l.strip()
    if not l: continue
    
    if l.startswith("PART"):
        cur_part = {"name": l, "children": []}
        re_taxonomy.append(cur_part)
        cur_chapter = None
    elif l.startswith("Chapter"):
        cur_chapter = {"name": l, "children": []}
        if cur_part:
            cur_part["children"].append(cur_chapter)
    elif l.startswith("제") and "절" in l.split(" ")[0]:
        if cur_chapter:
            cur_chapter["children"].append({"name": l})

with open("taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy = json.load(f)

taxonomy["부동산학원론"] = re_taxonomy

with open("taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(taxonomy, f, ensure_ascii=False, indent=2)

print("Appended 부동산학원론 to taxonomy.json")
