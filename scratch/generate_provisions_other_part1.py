# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

if not DB_PATH.exists():
    print(f"Error: {DB_PATH} not found.")
    exit(1)

with open(DB_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded database with {len(questions)} questions.")

taxonomy = {
    "subject": "회계학",
    "sub_subject": "재무회계",
    "chapter": "제3장 부채",
    "section": "Chapter 09 충당부채, 우발부채",
    "item": "3절 기타의 충당부채"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q2301 ~ Q2310) ---
    {
        "id": "practice-accounting-ch09s02-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1037호에 따른 충당부채 대상 거래 중 '구조조정(Restructuring)'의 정의로 가장 옳은 것은?",
        "options": [
            "① 제품 품질 결함을 수선하기 위해 매년 일정 비율로 계상하는 사후 관리 정책",
            "② 새로운 지분을 발행하여 자본을 확충하고 타 법인 주식을 취득하는 경영 활동",
            "③ 경영진이 계획하고 통제하며, 기업이 수행하는 사업의 범위나 사업 수행 방식에 유의적인 변화를 가져오는 프로그램",
            "④ 기업의 외화 대여금이 환율 변동으로 인해 환산 손익이 유발되는 외환 거래",
            "⑤ 회사의 최대주주가 변동됨에 따라 이사회 구성원 전원을 임의 교체하는 절차"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1037호 문단 70에 따르면, 구조조정이란 경영진이 계획하고 통제하며, 기업이 수행하는 사업의 범위나 사업 수행 방식에 유의적인 변화를 가져오는 프로그램으로 정의됩니다.\n\n[오답 해설]\n① 제품 품질보증 충당부채에 관한 정의입니다.\n② 자본 확충 및 주식 취득은 금융자산/자본 거래에 해당합니다.\n④ 외화 환산 및 외환 거래는 외화기준서 적용 사항입니다.\n⑤ 주주 변동에 따른 이사회 교체는 회계 상 구조조정 충당부채 설정 대상 구조조정이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "K-IFRS 제1037호 상 기업이 구조조정에 대한 '의제의무(Constructive Obligation)'를 부담하여 당기말 충당부채를 인식할 수 있기 위해 '동시에 충족'해야 하는 요건이 아닌 것은?",
        "options": [
            "① 구조조정 계획에 관한 구체적이고 공식적인 계획이 존재해야 한다.",
            "② 계획의 이행에 착수하였거나 계획의 주요 내용을 공표하여 구조조정 대상자가 정당한 기대를 가지게 해야 한다.",
            "③ 이사회 내부 회의에서 경영진들끼리 구조조정이 필요하다는 공감대를 형성하고 구두 서약을 마쳐야 한다.",
            "④ 공식 계획에는 관련 사업이나 사업장, 대상 종업원의 기능과 대략적인 인원수, 지출될 금액 및 이행 시기가 포함되어야 한다.",
            "⑤ 구조조정 계획은 차기 중에 신속히 실행될 수 있는 타당한 기한 정보가 구체화되어야 한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 경영진의 내부적 결의나 사내 구두 논의만으로는 외부 대상자(임직원, 거래처 등)에게 정당한 기대를 형성시키지 못하므로 의제의무가 수립되지 않습니다. 반드시 이행 착수 또는 공식 공표 조치가 수반되어야 합니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 구조조정 의제의무 수립을 위해 동시에 충족해야 하는 세부적이고 구체적인 공식 계획 및 전달 요건들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "K-IFRS 제1037호에 따른 '손실부담계약(Onerous Contracts)'의 핵심 정의로 가장 옳은 것은?",
        "options": [
            "① 기업의 당기순손실이 자본금의 50%를 초과하는 심각한 재무 위기 계약",
            "② 계약상 의무 이행에 따르는 회피불가능한 원가가 당해 계약에 의해 기대되는 경제적 효익을 초과하는 계약",
            "③ 계약의 효력이 무효화되어 거래처로부터 계약금 전체를 몰수당하는 계약",
            "④ 이자율이 시장 실세금리보다 지나치게 높게 묶여 있어 조기 상환할 수밖에 없는 사채 계약",
            "⑤ 판매 가격이 원가보다 10% 이상 하락하여 기말 재고평가손실을 유발하는 재고자산 거래"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 손실부담계약이란 계약상의 의무 이행에 따르는 회피 불가능한 원가가 당해 계약에 의해 기대되는 경제적 효익을 초과하여 계약 유지 자체로 순손실이 확정되는 계약을 뜻합니다.\n\n[오답 해설]\n① 재무 위기 자체는 특정 계약의 손실부담 여부를 정의하지 못합니다.\n③ 계약 무효나 몰수 조항과는 무관한 정상 계약 하에서의 손실 상태입니다.\n④ 사채 계약의 조기상환은 손실부담계약의 적용 영역이 아닙니다.\n⑤ 재고자산의 평가손실은 재고자산 기준서(제1002호)의 적용 대상입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "K-IFRS 제1115호 '고객과의 계약에서 생기는 수익' 기준서와 K-IFRS 제1037호의 관계 속에서, 기업이 제공하는 제품 보증 유형 중 '확신 유형의 보증(Assurance Warranty)'과 '용역 유형의 보증(Service Warranty)'의 기본 구별 원칙으로 가장 옳은 것은?",
        "options": [
            "① 확신 유형의 보증은 수행의무로 식별하여 거래가격을 배분하고, 용역 유형의 보증은 즉시 전액 당기 비용으로만 떤다.",
            "② 확신 유형의 보증은 K-IFRS 제1037호에 따른 충당부채를 설정하고, 용역 유형의 보증은 고객에게 별도의 용역을 제공하는 수행의무로 보아 수익을 이연하여 이행 시점에 인식한다.",
            "③ 두 보증 모두 충당부채 설정 대상이므로 용역보증도 선수수익을 잡을 수 없다.",
            "④ 용역보증은 무형자산 취득원가에 직접 가산하여 자산화시킨다.",
            "⑤ 두 보증 모두 법률에 강제되는 거래이므로 자본조정의 이익준비금으로만 적립한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 상 제품보증의 성격적 구별 원칙입니다.\n- 확신보증(Assurance-type): 제품이 합의된 규격에 부합한다는 확신을 제공하므로 K-IFRS 제1037호 '충당부채'를 설정하여 비용 및 부채로 매칭합니다.\n- 용역보증(Service-type): 제품 규격 확신 외에 추가적인 서비스 용역을 약정하는 것으로, 독립된 수행의무에 해당하여 관련 거래가격을 선수금(계약부채)으로 이연한 후 사용 기간 동안 수익화합니다.\n\n[오답 해설]\n① 설명이 거꾸로 명시되었습니다.\n③ 용역보증은 수행의무에 해당하여 수익이연(계약부채/선수수익) 적용 대상입니다.\n④, ⑤ 무형자산 취득원가 가산이나 이익준비금 적립 등은 틀린 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "정부로부터 무상할당(Free Allocation)받은 온실가스 배출권 범위 내에서 기업이 실제로 온실가스를 배출한 경우, K-IFRS 일반기업회계기준 및 배출권 회계 원칙에 따른 '온실가스 배출부채'의 기본 인식 가액은?",
        "options": [
            "① 배출 즉시 시장 가격으로 전액 평가하여 부채로 잡는다.",
            "② 배출권 액면 금액의 50%를 부채로 계상한다.",
            "③ 무상할당받은 범위 내의 배출에 대해서는 배출부채의 장부금액을 ₩0(영)으로 측정하여 부채를 인식하지 아니한다.",
            "④ 배출권의 역사적 취득원가에 물가상승률을 곱한 금액으로 계상한다.",
            "⑤ 무상배출권은 자산이 아니므로 배출 즉시 전액 기타포괄손익 손실로 분류한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 정부가 기무상 할당한 배출권 쿼터 범위 내에서 실현된 가스 배출 행위에 대해서는, 기업이 향후 추가로 지출할 경제적 의무가 없으므로 해당 의무 지출에 대한 배출부채 가액은 ₩0으로 평가되어 별도의 부채 기장을 실행하지 않습니다.\n\n[오답 해설]\n① 무상할당 한도를 초과하여 배출한 부족분에 대해서만 기말 시장가격 등으로 배출부채를 인식합니다.\n② 50% 일괄 평가는 규정이 없습니다.\n④, ⑤ 역사적 원가 물가 반영이나 OCI 자본 차감 처리는 인정되지 않는 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "K-IFRS 제1037호 문단 80에 따라, 구조조정 계획 확정 시 대변에 기상할 '구조조정 충당부채'의 측정 한도 범위에서 법적으로 엄격하게 제외되어야 하는 지출은?",
        "options": [
            "① 해고수당 및 퇴직위로금",
            "② 폐쇄될 사업장의 잔여 임차 리스 계약 위약금",
            "③ 계속 근무할 잔류 종업원들의 다른 영업소 전근 여비 및 직무 재교육 교육훈련비",
            "④ 폐쇄 대상 영업 계약의 중도 해지 합의금",
            "⑤ 해고 임직원들의 정리를 위한 법률 대문 소요 비용"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 상 구조조정 충당부채는 '구조조정으로 인하여 직접 유발되는 지출'만 포함합니다. 잔류 임직원의 직무 재교육비, 전근 전출 여비, 기계 이설 및 신규 마케팅 등은 모두 구조조정이 완료된 이후 기업의 '계속적인 영업 활동'과 연계된 미래 지출이므로 부채 범위에서 철저히 배제합니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 구조조정 합의 폐쇄 등으로 인해 불가피하게 직접 발생하여 유출이 종용되는 적격한 충당부채 포함 비용 항목들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "K-IFRS 제1037호 문단 69에 따라, 손실부담계약의 요건을 충족하여 대변에 '손실부담계약 충당부채'를 인식하기에 앞서 '필수적으로 선행 완료'하여 장부에 기장해야 하는 회계 조치로 명시된 것은?",
        "options": [
            "① 전용 기계장치의 취득원가를 최초 자본금으로 전액 리셋한다.",
            "② 당해 계약을 이행하기 위하여 전용으로 지정된 자산이 있는 경우, 그 자산에 대하여 발생한 손상차손(K-IFRS 제1036호 '자산손상' 적용)을 우선 인식하여야 한다.",
            "③ 계약 상대방에게 계약금 반환을 청구하는 우발자산을 먼저 기장한다.",
            "④ 유형자산의 감가상각을 즉시 중단하고 이월 결손금으로 대체한다.",
            "⑤ 이사회를 열어 자본금 10% 한도의 보전 적립금을 적립 이체한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 손실부담계약으로 인한 현금 유출 채무를 부채로 설정하기 전에, 해당 계약을 위해 사용되는 개별 자산의 가액이 과대평가되는 것을 방지하기 위해, 기준서는 해당 전용 자산의 손상 검사를 먼저 거쳐 '자산손상차손'을 적립(자산 가치 삭감)하는 분개를 실행하도록 규정하고 있습니다.\n\n[오답 해설]\n① 자본금 리셋이나 ③ 우발자산 가식 기장 등은 기준서에 부합하지 않습니다.\n④ 감가상각 중단 조치는 손실부담계약의 선행 조건이 아닙니다.\n⑤ 보전 적립금 등의 자본 항목 조절은 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "기업이 판매 촉진을 위해 고객에게 매출액 기준 일정 마일리지나 포인트(Points)를 부여하고 향후 물품 결제 시 할인 혜택을 주는 '고객충성제도(Customer Loyalty Programs)'의 일반적인 기말 회계처리에 대한 설명 중 옳은 것은?",
        "options": [
            "① K-IFRS 제1037호에 따라 전액 '충당부채'로 계상하고 대변에 복구충당금 명칭을 쓴다.",
            "② 포인트는 부채가 아니므로 기말 결산 보고서에서 완전히 기장 누락 처리한다.",
            "③ 포인트 지급액은 전액 임직원의 급여(판관비)로 보아 원천징수한다.",
            "④ K-IFRS 제1115호에 따라 포인트 부여분을 독립된 수행의무로 식별하여 거래가격을 배분하고, 포인트가 이행되거나 소멸하기 전까지는 '계약부채(Deferred Revenue/선수수익)'로 이연 보고하여야 한다.",
            "⑤ 포인트를 자산조정의 미수금으로 기재하고 매출채권에서 직접 상계 차감한다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 과거에는 포인트를 충당부채(비용보충법)로 처리하기도 하였으나, 현행 K-IFRS 제1115호 '수익' 기준서 하에서는 포인트 부여 거래를 다중 수행의무로 보아 거래가격을 상대적 개별판매가격 비율로 안분 배분하고, 포인트에 배분된 대금은 선수금(계약부채)으로 이연한 후 실제 포인트 사용 시 수익화하도록 정밀 규정하고 있습니다.\n\n[오답 해설]\n① 충당부채나 복구충당금 등의 IAS 37 부채 계정은 포인트 거래의 정석 회계처리가 아닙니다.\n② 포인트 부채 누락은 부채 과소계상 오류입니다.\n③ 임직원 급여나 ⑤ 미수금 자산 상계 조항 등은 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "K-IFRS 제1037호에 의거하여, 구조조정 충당부채 설정 조건 중 '공식적이고 구체적인 구조조정 계획'에 반드시 포함(명시)되어 있어야 하는 사항에 해당하지 않는 것은?",
        "options": [
            "① 관련 사업 혹은 사업의 일부 및 영향을 받는 주요 사업장 위치",
            "② 퇴직을 유도하거나 보상을 제공할 대상 종업원의 기능, 위치 및 대략적인 인원수",
            "③ 구조조정을 실행함으로써 차기에 획득할 것으로 추정되는 예상 신규 영업이익 총액",
            "④ 구조조정으로 인하여 발생할 구체적인 예상 지출 금액",
            "⑤ 구조조정 계획을 실행에 옮길 시기(타당한 기한 명시)"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 구조조정 공식 계획에는 사업 폐쇄, 인원 감축, 지출 규모, 실행 일정 등의 의무적 구체 사항이 기술되어야 하지만, 구조조정 완료 후 차기 영업이익 예상치 등은 충당부채의 인식(의무 수립) 요건인 공식 계획의 필수 기재 항목에 해당하지 않습니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 구조조정 의제의무를 형성하는 공식 계획서의 필수 5대 기재 요건들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "온실가스 배출권 거래제 하에서 기업이 온실가스 배출부채를 인식하게 만드는 최초의 실제적인 '의무발생사건(Obligating Event)'은 무엇인가?",
        "options": [
            "① 정부가 당해 연도 배출권 무상 할당 계획을 관보에 최초 고시한 시점",
            "② 배출권을 시장에서 거래하기 위해 증권 거래소 계좌를 신설 개설한 날",
            "③ 기업이 조업 가동 중 실제로 온실가스를 대기 중에 배출한 사건 및 배출량 누적 행위",
            "④ 이사회에서 차기 배출 저감 시설 설치를 결의하고 기각한 시점",
            "⑤ 외화 환율이 급등하여 배출권 선물 가치가 하락한 당일"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 온실가스 배출부채를 유발하는 과거 사건의 결과는 배출 저감 계획이나 고시가 아니라, 실제 조업 중에 온실가스를 '대기 중에 물리적으로 배출한 행위' 그 자체입니다. 배출을 하였으므로 향후 정산일에 배출권으로 정산 납부해야 하는 현재의무가 형성됩니다.\n\n[오답 해설]\n① 고시 시점이나 ② 계좌 개설, ④ 저감 결의, ⑤ 선물 가치 변동 등은 배출부채를 성립시키는 본질적인 의무발생사건이 될 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },

    # --- L2 (이해): 15문항 (Q2311 ~ Q2325) ---
    {
        "id": "practice-accounting-ch09s02-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "K-IFRS 제1037호 하에서 구조조정 계획 수립 시 '임직원 재교육훈련비'나 '신제품 마케팅비', '신규 전산 시스템 구축비' 등을 구조조정 충당부채 측정 범위에서 엄격하게 배제하고 발생 시점에 즉시 당기 비용화하도록 정한 이론적 배경은?",
        "options": [
            "① 해당 비용들은 법인세 공제 대상에서 원천 배제되기 때문이다.",
            "② 재교육비 등은 자본금 직접 차감 항목이기 때문이다.",
            "③ 해당 지출들은 구조조정의 성립 여부와 상관없이 향후 기업의 '미래 영업 및 계속적인 경영 활동' 과정에서 유발되는 성격이므로, 결산일 현재의 과거 사건에 따른 피할 수 없는 부채 의무가 아니기 때문이다.",
            "④ 주주총회의 의결을 거치면 언제든지 부채로 소급하여 합산할 수 있기 때문이다.",
            "⑤ 해당 지출들은 항상 현금으로만 즉시 지급되므로 충당부채 설정 대상에서 제외된다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 구조조정 충당부채는 '구조조정으로 직접 발생하는 지출'에 한합니다. 즉, 미래 영업 행위와 연동되어 향후 피할 수 있는 지출(교육, 홍보, 이전비 등)은 현재의무를 구성하지 않으므로 부채 기장에서 제외하고 후속 발생 시 발생주의에 의해 영업 비용 처리합니다.\n\n[오답 해설]\n① 법인세 공제 여부는 회계 기준의 자산/부채 성립 정의 요건을 좌우하지 않습니다.\n② 자본금 직접 차감 항목이 아닙니다.\n④ 주주총회 의결만으로 부채의 성격이 없는 항목을 부채로 소급 가산할 수 없습니다.\n⑤ 현금 지급 여부와 충당부채/확정부채 분류는 연관성이 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "K-IFRS 제1037호에 의거하여, 기업이 공식적인 구조조정 계획을 공표(Announcement)하는 행위가 제3자에게 '정당한 기대(Valid Expectation)'를 유발하여 의제의무를 형성하기 위한 전달 방식 조건으로 가장 옳은 것은?",
        "options": [
            "① 이사회에서 임의로 구두 논의하고 사내 인트라넷에 비공개 보관한 경우",
            "② 대상 종업원이나 대리인, 계약 상대방 등 영향을 받는 당사자들에게 구조조정의 범위, 시기, 대상 등을 구체적이고 구속력 있는 형태로 전달하여 당해 계획이 실행될 것임을 확신시키는 경우",
            "③ 최대주주 한 명에게만 개인 메일로 해고 리스트를 전달한 경우",
            "④ 공표일로부터 20년 후에 진행할 수도 있다는 유예 기간 조항을 덧붙인 경우",
            "⑤ 경쟁사에 공장을 매각할 수도 있다는 미확정 소문을 유포한 경우"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 구조조정 공표가 의제의무를 유발하여 기말 충당부채 성립 요건이 되려면, 영향을 받는 상대방에게 구체적이고 철회 불가능할 정도의 실행 신뢰를 심어 정당한 기대를 야기해야 합니다.\n\n[오답 해설]\n① 사내 비공개 보관이나 ③ 개인적 이메일 송부 등은 공표 요건에 맞지 않습니다.\n④ 20년 장기 유예 조항은 신속한 이행 일정 조건에 어긋나며,\n⑤ 매각 소문 유포는 공식적인 실행 계획 공표가 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "K-IFRS 제1037호 하에서 손실부담계약의 '회피불가능한 원가(Unavoidable Costs)'를 계산할 때, 계약을 이행하기 위해 소요되는 순원가와 계약 불이행(취소) 시 발생하는 위약금/보상금 중 '더 작은 금액(Min)'을 취하도록 규정한 합리적 배경으로 가장 옳은 것은?",
        "options": [
            "① 기업이 항상 최소 세금만 납부할 수 있도록 세무 혜택을 제공하기 위함이다.",
            "② 기업은 경제적으로 합리적인 의사결정(즉, 손실을 최소화하는 방향으로 계약 취소 또는 이행 선택)을 할 것이라고 가정하기 때문에, 강제되는 회피 불가능한 최소 손실 한도를 최선의 추정액으로 삼는 것이 타당하기 때문이다.",
            "③ 계약을 파기하면 자산가치가 무조건 두 배로 증가하는 우발 효과를 반영하기 위함이다.",
            "④ 큰 금액을 부채로 잡으면 자본조정이 잠식되어 이자율이 변동하기 때문이다.",
            "⑤ 회계사가 임의로 부채를 지울 수 있는 주관적 면책권을 주기 위함이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 손실부담계약 시 합리적 기업이라면 ₩80,000의 이행 손실과 ₩60,000의 계약 해지 벌과금 중 당연히 더 적은 ₩60,000의 벌과금을 내고 계약을 파기하여 손실을 최소화할 것입니다. 따라서 피할 수 없는 '회피불가능한 원가'는 두 대안 중 낮은 쪽으로 귀결됩니다.\n\n[오답 해설]\n① 세무 혜택 유도설은 오답입니다.\n③ 계약 파기가 자산가치를 증대시킨다는 서술은 거짓입니다.\n④ 자본조정 잠식 및 이자율 변동설은 인과관계가 없습니다.\n⑤ 회계사의 주관적 면책권은 회계 기준 수립의 근거가 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "K-IFRS 제1115호 및 제1037호에 비추어 볼 때, 제조업자가 판매 시 무상으로 첨부하는 '확신 유형의 보증(Assurance-type)'의 회계 처리 및 당기 손익에 미치는 영향으로 가장 옳은 것은?",
        "options": [
            "① 보증 기간 동안 실제로 수리 요청이 접수될 때까지 어떠한 비용도 잡지 않고 현금주의로 처리한다.",
            "② 판매 시점에 수익 인식액의 일부를 강제로 취소하여 자본금으로 적립한다.",
            "③ 제품 판매(인도) 완료 시점에 예상 보증수리비의 최선의 추정액을 당기 비용(제품보증비)으로 즉시 인식하고 동시에 대변에 '제품보증충당부채'를 인식하여 수익-비용 대응을 달성한다.",
            "④ 고객 소송이 터져 법원 판결을 받기 전에는 부채 기장을 전면 보류한다.",
            "⑤ 확신보증비는 무형자산 영업권에 합산하여 매년 상각하여야 한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 확신보증은 제품의 고유 품질 규격을 보장하는 부수 계약이므로 제품 인도 시점에 보증비용 기댓값을 당기 비용으로 계상하고 대변에 제품보증충당부채(부채)를 인식하는 발생주의 회계 처리를 수행합니다.\n\n[오답 해설]\n① 실제 접수 시점에만 비용을 잡는 것(현금주의 성격)은 발생주의 및 수익비용대응 원칙에 어긋납니다.\n② 수익을 취소하여 자본금으로 바로 돌리는 분개는 인정되지 않습니다.\n④ 법적 소송 전이라도 의무 성립 시 충당부채를 기장해야 합니다.\n⑤ 보증비는 무형자산 영업권의 취득 원가 가산 대상이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "K-IFRS 제1115호 '수익' 기준서 상 고객이 제품과 별도로 추가 구매할 수 있는 '용역 유형의 보증(Service-type)'의 수익 인식 프로세스로 가장 옳은 것은?",
        "options": [
            "① 보증 상품 판매 당일 전액 당기 매출 수익으로 일시 인식한다.",
            "② 판매 대금을 전액 이익잉여금 자본으로 직접 기장한다.",
            "③ 해당 보증금액을 이연하지 않고 대변에 유형자산 평가 차손으로 상쇄 처리한다.",
            "④ 판매 대금 중 보증 용역에 배분된 거래가격을 최초에 '계약부채(선수수익)'로 인식(이연)하고, 보증 서비스 기간이 경과함에 따라 정액법 등으로 수행의무를 이행하는 시점에 맞추어 점진적으로 수익으로 인식한다.",
            "⑤ 용역보증 수익은 기말 무형자산 개발비 계정에 무조건 가산 상각한다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 용역보증은 별도의 서비스 상품이므로 거래가격을 배분하여 최초에는 선수금(계약부채)으로 이연한 후, 보증 제공 기간 동안 계약 성과 이행 경과에 따라 매출 수익으로 점진적 실현시킵니다.\n\n[오답 해설]\n① 판매 당일에 전액 일시 수익화하는 것은 기간 경과 수행의무 이행 원칙에 위배됩니다.\n② 자본으로 직접 기장할 수 없습니다.\n③ 자산 평가 차손 상쇄 조치는 오류입니다.\n⑤ 무형자산 개발비 가산 처리설은 오답입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "손실부담계약에 대하여 K-IFRS가 '계약 전용 자산에 대한 손상차손'을 충당부채 기장보다 선행하여 적용 완료하도록 강제하는 주된 회계적 이유로 가장 옳은 것은?",
        "options": [
            "① 자산 감액 평가를 먼저 실행해야 부채의 이자율 할증이 자동으로 계산되기 때문이다.",
            "② 계약 전용 자산의 가액이 부풀려진 채 방치된 상태에서 부채만 추가로 늘려 적으면, 재무제표 상 자산과 부채가 동시에 이중 과대계상(Gross up 왜곡)되어 정보 이용자에게 왜곡된 정보를 제공하기 때문이다.",
            "③ 전용 자산의 상각을 면제받기 위한 주관적 회계 수단이다.",
            "④ 자산손상을 잡으면 기말 법인세액이 무조건 2배 면제되는 세법 규정과 연동되기 때문이다.",
            "⑤ 부채를 전액 기타포괄손익 자본 항목으로 대체하기 위한 선행 요건이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 전용 기계장치의 가치 하락(손상)을 정리하지 않고, 대변에 손실부담충당부채만 가산하면 총자산과 총부채가 동시에 과대 계상됩니다. 따라서 자산 손상을 먼저 차감하여 자산 가액을 줄인 후, 남은 순의무 격차분만 부채로 적는 것이 대차대조표 총량 신뢰성에 정합합니다.\n\n[오답 해설]\n① 선행 손상이 할인율 할증을 자동 계산하게 만들지 않습니다.\n③ 자산 감가상각 면제 목적이 아닙니다.\n④ 세법의 강제 면제 조항 연동설은 사실이 아닙니다.\n⑤ 기타포괄손익 자본 대체 절차와 무관합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "온실가스 배출권 거래제 하에서 무상할당 범위를 초과하여 가스를 배출한 경우, 보유하고 있는 '매입 온실가스 배출권(자산)'의 한도 내에서 배출부채를 측정하는 올바른 기준 장부금액은?",
        "options": [
            "① 배출 시점의 기중 달러 평균 환율",
            "② 해당 매입 온실가스 배출권 자산의 최초 취득 장부금액(취득원가)",
            "③ 기말 결산일 현재의 시장 공정가치(종가 시세)",
            "④ 무상할당 배출권의 가상 액면가",
            "⑤ 이사회에서 임의 승인한 표준 기준 단가"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 무상할당을 초과하여 배출한 배출부채 중, 회사가 부족 조달을 위해 이미 외부에서 사들여 장부에 얹어둔 매입 배출권 자산의 수량 한도 내에 대해서는, 당해 매입 배출권 자산의 '최초 취득 장부금액(원가)'을 기준으로 배출부채(충당부채) 금액을 계산하여 적립합니다.\n\n[오답 해설]\n① 배출 시점 평균 환율이나 ③ 기말 시장 공정가치는 보유 중인 매입배출권 범위 내 측정에 대입하지 않습니다. (기말 공정가치는 배출권이 없어 외부에서 추가 사와야 하는 '순 부족분' 지출액을 평가할 때 사용합니다.)\n④ 무상배출권은 장부가가 ₩0이어서 대입 대상이 아닙니다.\n⑤ 이사회 표준 단가 기장은 기준 외 임의 왜곡 처리입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "온실가스 배출권 거래제 적용 기업이 기중에 가스를 대량 배출하여 무상할당량 및 기매입배출권을 모두 초과하는 '순 부족 배출량(Shortfall)'이 유발되었다. 이 부족분에 대해 기말 현재 인식할 온실가스 배출부채의 올바른 측정 기준금액은?",
        "options": [
            "① 과거 최초 가동 시점의 역사적 평균 유가",
            "② 무상할당 배출권의 당초 가상 장부가액(₩0)",
            "③ 보고기간 말(기말 결산일) 현재 시장에서 거래되는 배출권의 시장가격(공정가치)",
            "④ 발행 주식의 주당 장부금액",
            "⑤ 부족 수량에 관계없이 ₩1,000,000의 정액 충당금"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 보유 중인 배출권 한도를 초과하여 기말 현재 순부족분(Shortfall)으로 남은 가스 배출량은 향후 정산 납부를 위해 외부 시장에서 새로 사와 채워야 하는 피할 수 없는 지출입니다. 따라서 기말 결산일 현재 시점의 '시장 가격(Market Price/공정가치)'을 기준으로 하여 지출 예상액을 추정하여 배출부채로 계상합니다.\n\n[오답 해설]\n① 역사적 평균 유가나 ④ 주당 장부가는 배출부채 추정 기준이 될 수 없습니다.\n② 부족분에 대해 ₩0을 대입하면 장부 상 부채 누락 오류가 발생합니다.\n⑤ ₩1M 정액 계상은 합리적 추정 방법이 아닌 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "K-IFRS 제1037호 하에서 기업의 구조조정 계획에 '사업부의 매각(Sale of an Operation)' 건이 직접 연계 포함되어 있는 경우, 이 매각 부문에 대한 매각손실 또는 관련 보상 충당부채의 인식 의무(의제의무)가 발생되는 실제 성립 시점으로 가장 옳은 것은?",
        "options": [
            "① 이사회에서 해당 사업부를 내년 중 매각하자고 구두 결의한 시점",
            "② 투자 자문사에 매각 자문 수수료 계약을 맺고 송금한 거래 당일",
            "③ 해당 사업부 매각과 관련하여 매수자와 '구속력 있는 매매계약(Binding Sale Agreement)'을 정식 체결한 시점",
            "④ 신문에 매각 대상을 공고하고 인수 후보자들의 입찰 인수를 마감한 날",
            "⑤ 해당 사업부 자산의 장부금액 평가 감액을 이익잉여금에 직접 기장 완료한 날"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1037호 문단 78에 따라 구조조정에 사업부 매각이 연계된 경우, 매수자와의 구속력 있는 정식 매매계약(Binding Sale Agreement)이 성립되기 전에는 기업이 매각 결정을 자의적으로 철회하거나 영업을 지속할 여지가 있으므로 의무가 성립되지 않습니다. 반드시 구속력 있는 매매계약 체결 시점에 의무가 확정되어 부채 인식 조건이 수립됩니다.\n\n[오답 해설]\n① 이사회 매각 결의나 ② 자문 계약, ④ 입찰 마감 등은 매각 철회 대안이 남아 있는 회피 가능 상태이므로 의무 발생 시점이 될 수 없습니다.\n⑤ 임의 자본 조정 기장일은 기준 외 오류 시점입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "K-IFRS 제1037호 문단 82에 의거하여, 구조조정 이행 완료일까지 폐쇄될 사업부에서 불가피하게 지속 누적되어 발생할 '구조조정 개시 시점 이후의 예상 영업손실(Expected Operating Losses up to the date of a restructuring)'을 당기말 구조조정 충당부채 범위에서 제외해야 하는 주된 이론적 사유는?",
        "options": [
            "① 영업손실은 세금 납부 후 차감되는 자본 잠식액이기 때문이다.",
            "② 해당 미래 손실은 과거사건의 결과가 아니며, 결산일 현재 기업이 짊어지고 있는 '피할 수 없는 현재의무'의 정의 요건(과거 사건 성격)을 원천 결여하고 있기 때문이다.",
            "③ 손실이 나면 국세청이 전액 비과세 지원을 해주기 때문이다.",
            "④ 영업손실은 충당부채가 아닌 대손충당금으로만 감액 기재하도록 법제화되어 있기 때문이다.",
            "⑤ 이사회 승인 시 이익잉여금 잔액 범위 내에서 전액 소급 충당할 수 있기 때문이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 미래의 예상 영업손실은 발생 확률이 아무리 높거나 구조조정 계획과 우연히 연관되어 있더라도 결산일 현재의 과거 사건 결과에 따른 회피 불가능한 채무(현재의무) 요건을 미달합니다. 따라서 부채 범위에 넣을 수 없고, 향후 실제 영업손실 발생기에 당기 영업손실 비용으로 인식하여야 합니다.\n\n[오답 해설]\n① 영업손실은 자본잠식액이 아닌 손익 항목입니다.\n③ 비과세 지원 연동설은 터무니없는 서술입니다.\n④ 대손충당금은 수취채권의 평가 차감 계정이어서 영업손실 부채와 성격이 다릅니다.\n⑤ 이익잉여금의 임의 자본 적립으로 부채 인식을 우회할 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "K-IFRS 제1115호에 따라 제품 판매 시 고객에게 무상 적립해 주는 포인트 마일리지의 개별 판매가격(Stand-alone Selling Price)을 산정하여 거래가격을 배분할 때 적용하여야 하는 올바른 조정 고려 사항은 무엇인가?",
        "options": [
            "① 포인트의 미래 실물 교환 단가를 주주 요구수익률로 나눈 할인율을 사용한다.",
            "② 고객이 향후 해당 포인트를 사용하지 않고 소멸시킬 확률(낙수율/Forfeiture rate)과 제공받을 할인 혜택의 가치 비중을 반영하여 합리적으로 조정한 개별 판매가격을 산출 배분하여야 한다.",
            "③ 포인트는 자산이 아니므로 무조건 ₩0의 단가로 거래가격 배분을 전면 제외한다.",
            "④ 국세청 표준 부가세 10%를 차감한 명목 액면 단가를 사용한다.",
            "⑤ 회사의 최대주주가 임의 지정한 단가를 일괄 대입한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 포인트의 개별 판매가격을 측정할 때에는 포인트당 획득 가능한 할인 가치에 더불어, 일부 고객이 포인트를 사용하지 않고 유효기간 만료 등으로 소멸시킬 가능성(낙수율/회수율 추정)을 통계 반영하여 조정한 상대적 가격 비중을 적용하여 매출액 배분을 실행합니다.\n\n[오답 해설]\n① 요구수익률 적용은 포인트 가격 산정과 무관합니다.\n③ 포인트의 가치를 0원으로 취급하여 거래가격 배분에서 제외하는 것은 기준서 위배입니다.\n④ 부가세 10%의 기계적 대입이나 ⑤ 최대주주 지정 단가 대입은 오답입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "K-IFRS 제1037호 개정 조항에 따라, 손실부담계약의 회피불가능원가를 판정하기 위해 '계약을 이행하는 데 소요되는 원가(Cost of Fulfilling a Contract)'를 도출할 때 포함해야 하는 비용 범주로 가장 옳은 것은?",
        "options": [
            "① 오직 계약을 위해서만 추가 발생되는 직접노무비 및 직접재료비와 같은 증분원가(Incremental Costs)만 인정된다.",
            "② 기업 전체 가중평균 이자비용 배분액만 포함된다.",
            "③ 계약에 직접 관련된 원가로서, 계약을 이행하기 위한 추가 증분원가(직접 재료, 직접 노무비 등)뿐만 아니라 계약 이행 활동에 직접 관련되는 기타 원가의 배분액(예: 계약 이행에 사용된 유형자산의 감가상각비 배분액 등)을 모두 합산하여 포함하여야 한다.",
            "④ 향후 발생할 것이 예상되는 미래의 추정 대손상각비 전액을 합산한다.",
            "⑤ 계약 파기 시 소송 배상금을 최대 2배 할증한 위약금만 포함된다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1037호 개정 기준에 따르면, 손실부담계약의 이행원가는 단순히 '증분원가(Incremental Cost)'에만 국한되지 않고, 계약과 직접 관련되는 모든 원가를 포함합니다. 여기에는 증분원가(직접 재료/노무비 등)와 더불어 계약 이행에 직접 배분되는 기타 원가(전용 설비의 감가상각비, 공동 관리비 안분액 등)가 누적 합산됩니다.\n\n[오답 해설]\n① 개정 이전이나 일부 제한적인 해석으로 증분원가만 가리켰던 설명은 오답입니다.\n② 기업 전체 가중평균이자 비용은 계약과 직접 관련된 원가가 아닙니다.\n④ 미래 추정 대손비나 ⑤ 위약금 할증액 등은 계약 이행 원가에 산입되는 기본 정의와 무관합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "기업이 당기말(12월 31일) 이전에는 구조조정에 대한 공표나 실행 행위가 없었으나, 기말 경과 후 재무제표 승인일(차기 2월) 전에 구조조정 세부 계획을 공식적으로 확정 및 외부 공표하였다. K-IFRS 기준 상 취해야 하는 당기말 결산 회계조치로 가장 옳은 것은?",
        "options": [
            "① 보고기간 후 사건이므로 당기 결산서 재무상태표 본문에 소급하여 구조조정 충당부채를 기장한다.",
            "② 당기 손익계산서의 비용을 차감시키고 대변에 이익잉여금 처분액으로만 기재한다.",
            "③ 보고기간 말 현재에는 의무발생사건(공표 등)에 따른 현재의무가 존재하지 않았으므로 당기 본문 부채 인식은 불가하며, 재무제표 이용자 정보 제공을 위해 당기 재무제표 '주석(Notes) 공시'로 해당 사실과 금액을 기재하여야 한다.",
            "④ 차기 결산 분개로 소급 기장하여 당기 재고 자산을 강제 감액 처리한다.",
            "⑤ 회계 추정치 변경이므로 어떠한 기장이나 주석 공시도 법적으로 면제된다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 결산일(12월 31일) 현재 시점에서 구조조정 의제의무가 성립 완료되어 있어야 당기말 본문 부채(충당부채) 계상이 가능합니다. 기말 시점에는 공표 사실이 없어 현재의무가 미달하였으므로 당기 부채 기장은 불가하며, 이는 보고기간 후 '수정을 요하지 않는 사건(Non-adjusting Event)'에 해당하여 차기 주석에 주요 공시 조치만 실행하게 됩니다.\n\n[오답 해설]\n① 수정을 요하는 사건이 아니므로 본문 부채 소급 기장은 허용되지 않습니다.\n② 이익잉여금 임의 조정은 부부적절합니다.\n④ 재고자산의 강제 차감 조치는 관련성이 없습니다.\n⑤ 중대한 의사결정의 보고기간 후 발생은 주석 공시 대상이므로 면제는 틀렸습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "기업이 판매한 제품에 대해 확신 유형의 보증충당부채 ₩100,000을 기말에 계상해 둔 상태이다. 이후 차기 중에 실제 고객들로부터 접수된 보증 수리 청구 비용이 ₩130,000으로 최종 판명되어 현금 정산 지급하였다. 이때 유발되는 회계적 처리 및 당기 손익 영향에 관한 분석으로 가장 옳은 것은?",
        "options": [
            "① 기존에 설정해 둔 충당부채 ₩100,000을 먼저 제거하고, 초과 발생액 ₩30,000은 당기 포괄손익계산서 상 '당기 비용(제품보증손실 등)'으로 인식한다.",
            "② 초과 발생액 ₩30,000은 전액 전년도 결산서의 영업비용을 소급 취소 수정한다.",
            "③ 차변에 제품보증충당부채를 한도 초과인 ₩130,000으로 적어 부채를 마이너스로 만든다.",
            "④ 초과액을 자본잉여금 증가 거래로 기장하여 자본을 확대한다.",
            "⑤ 수리 비용 초과 발생은 벌과금이므로 전액 이익잉여금 처분 차감으로 돌린다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 실제 보증 유출 발생 시, 장부에 잡혀 있던 제품보증충당부채 ₩100,000을 먼저 상쇄 제거합니다. 이후 한도를 초과하여 실제 유출된 ₩30,000 부분은 과거 재무제표 소급법이 아닌 당해 연도의 추가 발생 '당기 비용'으로 계상하여 정산 처리하는 것이 타당합니다.\n- 분개: (차) 제품보증충당부채 100,000, 제품보증비(당기비용) 30,000 / (대) 현금 130,000\n\n[오답 해설]\n② 충당부채 추정 격차는 회계추정의 변경 범주로 취급하여 당기 이후 전진 적용하므로 전년도 재무제표를 소급 수정하지 않습니다.\n③ 부채 계정을 마이너스로 표기하는 분개는 부적절합니다.\n④, ⑤ 자본잉여금 증가나 이익잉여금 직접 처분 차감은 기준 외 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "온실가스 배출권 거래제를 적용받는 기업이 정부로부터 무상할당받은 배출권을 보유 중인 경우, K-IFRS 상의 회계적 계정 분류 범주로 가장 올바른 결합은?",
        "options": [
            "① 배출권: 금융자산(FVPL), 배출부채: 금융부채(AC)",
            "② 배출권: 자본조정(OCI), 배출부채: 기타자본조정",
            "③ 배출권: 무형자산(또는 재고자산), 배출부채: 충당부채",
            "④ 배출권: 유형자산(기계장치), 배출부채: 미지급금",
            "⑤ 배출권: 투자부동산, 배출부채: 예수금"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 정부가 부여했거나 매입한 온실가스 배출권 자산은 물리적 실체가 없으나 식별 가능한 통제 자원이므로 원칙적으로 '무형자산'으로 분류하며, 배출 의무에 따라 결산일 현재의 과거 배출량 초과 부족분에 대해 계상하는 배출부채는 시기와 금액이 불확실한 '충당부채'로 분류합니다.\n\n[오답 해설]\n① 배출권은 현금 지급 등의 계약상 금융자산 정의를 직접 만족하지 않으므로 금융자산이 아닙니다.\n② 자본조정 항목이 아닙니다.\n④, ⑤ 유형자산, 투자부동산, 예수금 등은 성격에 맞지 않는 분류 오기입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    }
]

# Write back
questions.extend(new_questions)
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Saved database with {len(questions)} questions. Added {len(new_questions)} questions.")
