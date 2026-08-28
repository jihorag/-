import json
import re

raw = """
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
Chapter 01 객관식 문제
Chapter 02 재무제표 표시
1절 재무제표
2절 재무상태표
3절 포괄손익계산서
Chapter 02 객관식 문제
Chapter 03 재고자산
1절 재고자산의 최초측정
2절 기말재고금액
3절 재고자산의 인식시점
4절 기말재고금액의 추정
5절 감모손실과 평가손실
6절 농림어업
Chapter 03 객관식 문제
Chapter 04 유형자산
1절 유형자산의 인식 및 최초측정
2절 유형자산의 후속지출
3절 유형자산의 후속측정
4절 유형자산의 손상
5절 차입원가 자본화
6절 차입원가 자본화의 순서
Chapter 04 객관식 문제
Chapter 05 무형자산
1절 무형자산의 정의 및 인식과 측정
2절 무형자산의 상각
3절 무형자산의 제거와 손상
4절 영업권
Chapter 05 객관식 문제
Chapter 06 투자부동산
1절 투자부동산의 의의
2절 투자부동산의 최초측정
3절 투자부동산의 후속측정
4절 투자부동산의 계정대체
Chapter 06 객관식 문제
Chapter 07 금융자산
1절 금융상품
2절 현금 및 현금성자산
3절 매출채권과 매입채무
4절 기타금융자산
5절 투자지분상품
6절 투자채무상품
7절 금융자산의 손상과 재분류
8절 받을어음의 할인
Chapter 07 객관식 문제
Chapter 08 금융부채
1절 금융부채의 인식과 측정
2절 사채
3절 사채의 후속측정
4절 금융부채로 분류하는 상환우선주
Chapter 08 객관식 문제
Chapter 09 충당부채, 우발부채
1절 충당부채의 인식요건
2절 충당부채의 추정
3절 기타의 충당부채
4절 충당부채의 변제 및 변동
5절 우발부채와 우발자산
Chapter 09 객관식 문제
Chapter 10 자본
1절 자본의 의의
2절 자본의 분류
3절 주식의 발행
4절 증자와 감자
5절 자기주식
6절 배당금의 배분
7절 이익잉여금 처분
Chapter 10 객관식 문제
Chapter 11 복합금융상품
1절 전환사채
2절 전환권의 행사
3절 전환사채의 재매입 및 조건변경
4절 신주인수권부사채
Chapter 11 객관식 문제
Chapter 12 고객과의 계약에서 생기는 수익
1절 수익의 정의
2절 수익 인식의 5단계
3절 기타의 고려사항
Chapter 12 객관식 문제
Chapter 13 건설계약
1절 건설계약
2절 손실이 예상되는 공사
3절 진행률을 신뢰성 있게 측정하기 어려울 때
Chapter 13 객관식 문제
Chapter 14 종업원급여
1절 종업원급여
2절 퇴직급여제도
3절 확정급여제도의 재무상태표 표시
Chapter 14 객관식 문제
Chapter 15 주식기준보상
1절 주식결제형 주식기준보상
2절 현금결제형 주식기준보상
Chapter 15 객관식 문제
Chapter 16 리스
1절 금융리스로 분류하는 사례
2절 리스이용자 회계처리
3절 리스부채 재측정 및 리스변경
4절 리스제공자 회계처리
Chapter 16 객관식 문제
Chapter 17 법인세회계
1절 회계이익과 과세소득의 차이
2절 법인세회계
3절 자본에 가감하는 법인세효과
Chapter 17 객관식 문제
Chapter 18 주당이익
1절 주당이익(EPS)
2절 희석주당이익
Chapter 18 객관식 문제
Chapter 19 회계변경 및 오류수정
1절 회계변경
2절 오류수정
Chapter 19 객관식 문제
Chapter 20 현금흐름표
1절 현금흐름표
2절 영업활동 현금흐름 : 직접법 또는 간접법
3절 투자활동 및 재무활동 현금흐름
Chapter 20 객관식 문제
Chapter 21 재무제표 분석
1절 안전성비율
2절 수익성비율
3절 활동성비율
Chapter 21 객관식 문제
Chapter 22 관계기업투자주식
1절 관계기업
Chapter 22 객관식 문제
Chapter 23 보고기간 후 사건, 환율변동효과
1절 보고기간 후 사건의 유형 및 회계처리
2절 수정을 요하는 보고기간 후 사건
3절 보고기간 말 외화자산, 부채의 환산
Chapter 23 객관식 문제

PART 02 원가관리회계
Chapter 01 제조기업의 원가흐름
1절 원가의 다양한 분류기준
2절 제조기업의 원가흐름
Chapter 01 객관식 문제
Chapter 02 개별원가계산
1절 실제개별원가계산
2절 정상개별원가계산
3절 배부차이 및 배부차이 조정
Chapter 02 객관식 문제
Chapter 03 보조부문의 원가배부
1절 보조부문이 하나인 경우
2절 보조부문이 여러 개인 경우
Chapter 03 객관식 문제
Chapter 04 활동기준원가계산
1절 활동기준원가계산
Chapter 04 객관식 문제
Chapter 05 종합원가계산
1절 완성품환산량
2절 평균법과 선입선출법
3절 공손
Chapter 05 객관식 문제
Chapter 06 결합원가계산
1절 결합원가란?
2절 결합원가 배부방법
3절 결합원가 추가고려사항
Chapter 06 객관식 문제
Chapter 07 전부원가계산, 변동원가계산
1절 전부원가계산, 변동원가계산, 초변동원가계산
2절 각 원가계산방법들의 유용성과 한계점
Chapter 07 객관식 문제
Chapter 08 원가함수의 추정
1절 원가함수의 추정
Chapter 08 객관식 문제
Chapter 09 원가-조업도-이익분석(CVP분석)
1절 원가-조업도-이익분석
2절 손익분기점 및 목표이익
3절 안전한계
4절 기타 CVP분석
Chapter 09 객관식 문제
Chapter 10 표준원가계산
1절 표준원가계산
2절 원가차이 분석
Chapter 10 객관식 문제
Chapter 11 관련원가와 의사결정
1절 의사결정의 유형
2절 증분접근법(차액접근법)
3절 제약요인하의 의사결정
Chapter 11 객관식 문제
Chapter 12 대체가격결정
1절 대체가격이란?
2절 대체가격 결정방법
Chapter 12 객관식 문제
Chapter 13 종합예산
1절 종합예산
Chapter 13 객관식 문제
Chapter 14 투자중심점 성과평가
1절 투자중심점 성과평가
Chapter 14 객관식 문제
Chapter 15 최신 원가관리회계
1절 균형성과표
2절 다양한 원가계산
3절 품질원가
Chapter 15 객관식 문제
"""

lines = raw.strip().split('\n')
acc_taxonomy = []
cur_part = None
cur_chapter = None

for l in lines:
    l = l.strip()
    if not l: continue
    
    # Skip problem / answer sections
    if "객관식 문제" in l or "정답 및 해설" in l:
        continue
        
    if l.startswith("PART"):
        cur_part = {"name": l, "children": []}
        acc_taxonomy.append(cur_part)
        cur_chapter = None
    elif l.startswith("Chapter"):
        cur_chapter = {"name": l, "children": []}
        if cur_part:
            cur_part["children"].append(cur_chapter)
    elif "절" in l:
        if cur_chapter:
            cur_chapter["children"].append({"name": l})

with open("taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy = json.load(f)

taxonomy["회계학"] = acc_taxonomy

with open("taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(taxonomy, f, ensure_ascii=False, indent=2)

print("Appended 회계학 to taxonomy.json")
