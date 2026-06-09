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
    "chapter": "제2장 자산",
    "section": "Chapter 07 금융자산",
    "item": "4절 기타금융자산"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q1751 ~ Q1760) ---
    {
        "id": "practice-accounting-ch07s04-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "다음 중 K-IFRS 상 현금 등 금융자산을 수취할 계약상 권리가 존재하여 '기타금융자산' 범주에 귀속되는 항목이 아닌 것은?",
        "options": [
            "① 대여 계약서에 의거하여 기중에 대여하고 이자를 받기로 한 장기대여금",
            "② 토지 매각 대금 중 약정에 따라 6개월 뒤에 받기로 한 미수금",
            "③ 차년도 건물의 임차 사용을 위해 임대인에게 사전에 선납한 선급비용(선급금)",
            "④ 정기 예금에 대하여 결산일까지 일수로 발생했으나 아직 약정 수취일이 도래하지 않은 미수수익(미수이자)",
            "⑤ 상가 임차 시 퇴거 시점에 보증금 전액을 반환받기로 약정한 임차보증금"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 선급비용(선급금)은 사전에 대금을 납부하여 장래에 현금이나 금융자산이 아닌 '재화나 용역(서비스)'을 인도받을 계약상 권리이므로 금융자산이 아닌 비금융자산에 해당합니다.\n\n[오답 해설]\n① 대여금, ② 미수금, ④ 미수수익, ⑤ 임차보증금 등은 계약에 의거하여 장래에 확정된 금액의 '현금'을 돌려받거나 수취할 수 있는 명백한 금융자산 항목들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "상거래 이외의 비영업 거래(예: 유형자산이나 유가증권의 매각 등)에서 발생한 채권으로 매출채권과 명백히 분리하여 표시해야 하는 올바른 통합 자산 과목명은?",
        "options": [
            "① 미지급금 (Non-trade Payables)",
            "② 미수금 (Non-trade Receivables)",
            "③ 선급금 (Advance Payments)",
            "④ 선수수익 (Unearned Revenue)",
            "⑤ 외상매출금 (Accounts Receivable)"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 일반적인 상거래 이외의 거래에서 발생한 수취채권은 '미수금' 계정을 사용하여 재무상태표의 매출채권과 엄격히 구별하여 공시합니다.\n\n[오답 해설]\n① 미지급금은 수취 채권이 아니라 지급해야 할 의무인 부채 항목입니다.\n③ 선급금은 재화 등을 받기 위해 선지급한 비금융자산입니다.\n④ 선수수익은 기간 귀속에 따른 비금융 부채입니다.\n⑤ 외상매출금은 영업 상의 거래에서 나타나는 대표적인 매출채권 항목입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "K-IFRS 상 대여금 금융자산을 취득할 때 직접 관련하여 발생한 거래수수료 등 '거래원가(Transaction Cost)'의 회계처리 대원칙으로 올바른 것은? (단, 당해 대여금은 상각후원가(AC) 측정 금융자산으로 분류된다.)",
        "options": [
            "① 대여 자산의 회수 불확실성을 감안하여 취득 즉시 전액 판매비와관리비 비용으로 상각한다.",
            "② 대여금 최초 인식 시의 공정가치(최초 대여금액)에 '직접 가산'하여 장부금액을 구성한다.",
            "③ 자본 거래의 성격이 강하므로 주식발행초과금 자본 계정에서 직접 차감한다.",
            "④ 금융자산은 거래원가를 무조건 영업외수익 대변 항목으로 일시 계상한다.",
            "⑤ 취득 즉시 평가 손실로 반영하여 처분 손실을 미리 인식한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호에 따라 당기손익공정가치측정(FVPL)이 아닌 상각후원가(AC)나 기타포괄손익공정가치측정(FVOCI) 금융자산의 경우에는 최초 인식 시 자산 취득에 직접 관련되는 거래원가를 최초 공정가치에 '가산'하여 취득원가를 구성합니다.\n\n[오답 해설]\n① 취득 즉시 판관비 비용으로 인식하는 것은 당기손익공정가치측정(FVPL) 금융자산의 거래원가 처리 방식입니다.\n③ 주주 거래가 아니므로 자본 조정을 반영하지 않습니다.\n④, ⑤ 수익이나 처분손실 등은 실제 소멸 시점이나 평가 시점의 거래이므로 최초 취득 시점에 잡지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "대여금 금융자산에 대하여 기중에 이자를 수령할 때, 계약서 상 명기된 이자율에 기초하여 실제로 현금을 받아내는 이자의 정당한 명칭은?",
        "options": [
            "① 유효이자 (Effective Interest)",
            "② 시장이자 (Market Interest)",
            "③ 표시이자 또는 액면이자 (Nominal/Stated Interest)",
            "④ 복리이자 (Compound Interest)",
            "⑤ 연체이자 (Penalty Interest)"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 계약서 면에 명기된 표시(액면)이자율에 의해 기중에 현금으로 수취하는 이자 대금을 '표시이자' 또는 '액면이자'라고 칭합니다.\n\n[오답 해설]\n① 유효이자는 최초 장부가격에 유효이자율을 곱하여 실질 손익계산서 상에 기록하는 이자수익의 기준이 됩니다.\n② 시장이자는 시장에서 거래되는 동일 조건의 이자 가치입니다.\n④ 복리이자는 원금에 이자를 더한 금액을 기준으로 다음 기의 이자를 매기는 이자 계산법입니다.\n⑤ 연체이자는 만기 경과로 인해 추가 부과하는 패널티 이자입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "당기 회계연도 중에 은행 예금이나 대여금 등에서 발생한 이자 중, 결산일 현재 기간이 경과하여 이미 받을 권리(수익)는 성립하였으나, 계약 상 이자 지급일이 아직 도래하지 않아 현금을 회수하지 못한 경우에 기말 조정 분개 시 차변에 계상할 올바른 유동자산 과목은?",
        "options": [
            "① 선수수익 (Unearned Revenue)",
            "② 미수금 (Non-trade Receivables)",
            "③ 미수수익 (Accrued Revenues)",
            "④ 선급금 (Advance Payments)",
            "⑤ 미지급비용 (Accrued Expenses)"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 기간 경과에 따라 수익의 발생 요건은 채워졌으나 약정일이 오지 않아 아직 미수취 상태인 수익 채권은 '미수수익' 자산 계정으로 기말에 정비합니다.\n\n[오답 해설]\n① 선수수익은 미리 받은 수익이므로 부채입니다.\n② 미수금은 확정적으로 청구 약정이 완성되었으나 회수하지 못한 비영업 상 채권으로, 기간 경과 미수수익과는 구분됩니다.\n④ 선급금은 사전에 납부한 비금융자산입니다.\n⑤ 미지급비용은 지급하지 못한 비용 의무 부채입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "장기대여금의 액면금액과 시장이자율로 할인한 최초 현재가치의 차이로 인해 발생하는 '현재가치할인차금(Present Value Discount)' 계정이 K-IFRS 재무상태표에 표시되는 정당한 형태로 올바른 것은?",
        "options": [
            "① 재무상태표 유동부채 항목에 이자지급 채무로 별도 공시한다.",
            "② 자본 내 자본잉여금 증가 과목에 직접 상계 가산한다.",
            "③ 해당 장기대여금의 액면가액에서 직접 차감하는 형식의 '평가 차감 계정'으로 공시한다.",
            "④ 기말 유형자산의 감가상각누계액에 합산하여 보고한다.",
            "⑤ 무형자산 영업권 항목으로 이체 기재한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 현재가치할인차금은 본원 자산인 장기대여금 액면가액의 차감 계정(평가차감)으로 재무상태표 상 장기대여금 밑에 마이너스(-) 형식으로 기재하여 순현재가치를 노출시킵니다.\n\n[오답 해설]\n① 부채 항목이 아니라 자산의 평가차감 항목입니다.\n② 자본잉여금 등 자본조정과는 관련이 없습니다.\n④, ⑤ 유형자산 감누나 무형자산 영업권과는 완전히 다른 금융자산 평가 영역에 해당합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "채무자가 결제일에 대금을 지급하지 못하여 채권자에게 손실이 발생할 경우, 보증인이 발행한 보증 계약 조건에 따라 보증인이 대신하여 일정 금액을 채권자에게 상환해 주기로 약정하는 금융 계약의 올바른 명칭은?",
        "options": [
            "① 파생금융부채 (Financial derivative payables)",
            "② 금융보증계약 (Financial Guarantee Contract)",
            "③ 신용평가용역 (Credit rating service)",
            "④ 당좌차월약정 (Overdraft contract)",
            "⑤ 손상환입계약 (Impairment recovery contract)"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 금융보증계약(Financial Guarantee Contract)은 채무자가 결제일에 지급하지 못해 보증 채무 청구가 들어올 시 보증인이 대리 상환 의무를 가지는 보증성 금융상품 계약입니다.\n\n[오답 해설]\n① 파생상품 부채와는 측정 기법과 적용 기준서(K-IFRS 제1109호 일부 단서) 상의 구체적 의무가 구분됩니다.\n③ 신용평가 용역은 단순 신용 등급을 책정하는 서비스 거래입니다.\n④ 당좌차월약정은 은행 한도 대출 약정입니다.\n⑤ 손상환입은 대손 충당 평가와 관계된 회계 용어입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "회사가 해외 거래처에 달러($)화 등 외화 조건으로 자금을 대여한 화폐성 외화자산(외화대여금)을 보유하고 있다. K-IFRS 상 기말 결산 보고 시점에 이 외화자산을 원화로 환산하여 평가할 때 적용해야 하는 올바른 환율 기준은?",
        "options": [
            "① 최초 대여 당시에 약정한 장부 기록 환율(거래일 환율)",
            "② 보고기간종료일(결산일) 현재의 마감환율 (Closing Rate)",
            "③ 해당 외화 채권 취득 연도의 평균 환율",
            "④ 결산일 직후 3개월 이내에 도래할 것으로 예상되는 미래 예측 환율",
            "⑤ 외화 거래 은행이 보증해 준 법적 상한 환율"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1021호 '환율변동효과'에 따라 외화대여금이나 외화미수금 같은 화폐성 외화 자산/부채는 보고기간말(결산일) 현재의 '마감환율(Closing Rate)'을 적용하여 기말 평가 환산합니다.\n\n[오답 해설]\n① 거래일 환율(역사적 환율) 적용 대상은 비화폐성 외화자산(예: 역사적원가로 평가하는 유형자산이나 선급금 등)입니다.\n③ 평균 환율은 손익계산서 상의 수익과 비용 환산 시 보통 허용되는 기준입니다.\n④ 미래 예측 환율이나 ⑤ 보증 환율을 결산 평가에 적용하는 것은 기준서 위반입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "대여금 자산의 채무불이행 가능성(신용 위험)에 대비하여 기말에 적립해 놓은 '대손충당금(손실충당금)'의 정당한 계정 성격 및 재무상태표 표시 방식은?",
        "options": [
            "① 회사가 지급할 이자 의무이므로 유동부채로 보고한다.",
            "② 평가 시점의 평가이익이므로 영업외수익에 적는다.",
            "③ 대여금 액면가액의 차감적 성격인 '평가차감계정'으로 대여금에서 직접 차감 공시한다.",
            "④ 자본의 임의적립금 가산 항목으로 주주총회 결의를 통해 보고한다.",
            "⑤ 별도의 투자자산으로 분리하여 자산 총액을 오히려 가산시킨다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 대여금의 대손(손실)충당금은 본원 자산인 대여금의 차감 평가 계정으로, 매출채권 대손충당금과 마찬가지로 자산의 평가 회수액을 직접 차감 공시하는 형태를 띱니다.\n\n[오답 해설]\n① 부채 항목이 아닙니다.\n② 손실 평가이므로 수익 대변 항목이 아닙니다.\n④, ⑤ 자본잉여금 대체나 별도 자산 계상은 대손 회계의 복식부기 원리에 부합하지 않는 진술입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "장기 대여 시 시장 평균 금리(8%)보다 훨씬 저렴한 무이자로 자금을 대여해 주어 현재가치 할인액(현재가치할인차금)이 발생하였다. 이 할인차금은 기간이 경과함에 따라 어떤 회계적 절차를 거치게 되는가?",
        "options": [
            "① 만기 시까지 변동 없이 고정 기재해 둔다.",
            "② 유효이자율법을 적용해 상각해 나가면서 매년 이자수익(Interest income)으로 증액 반영한다.",
            "③ 유형자산 감가상각비와 합산하여 판매비와관리비로 처분한다.",
            "④ 만기 시점에 일시에 잡이익으로 털어버린다.",
            "⑤ 매입채무의 이자비용과 상계 처리하여 순액 ₩0으로 지운다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 대여금 현재가치할인차금은 유효이자율법을 적용하여 매 회계기간마다 상각해 나가고, 이 상각액만큼 대여금 장부금액을 늘려줌과 동시에 손익계산서 상 '이자수익'으로 정상 반영합니다.\n\n[오답 해설]\n① 현재가치할인차금은 상각 자산이므로 만기까지 고정 기재하는 것은 잘못입니다.\n③ 판관비 감비로 비용화할 성격이 아니며 투자 금융 이자수익 항목입니다.\n④ 만기 일시 정산이 아닌 각 기간별 경과 배분이 회계 발생주의 대원칙입니다.\n⑤ 매입채무 이자비용과 상일상계할 의무가 존재하지 않는 독립적 자산 평가입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    # --- L2 (이해): 15문항 (Q1761 ~ Q1775) ---
    {
        "id": "practice-accounting-ch07s04-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "장기대여금 자산에 대하여 명목상 액면가액이 아닌 미래 현금 수취 스케줄을 시장이자율로 할인한 '현재가치(Present Value)'로 평가하여 보고하는 회계이론적 정당성으로 가장 타당한 것은?",
        "options": [
            "① 미래 수취할 화폐 가치의 시간가치 왜곡을 제거하고 결산일 현재의 실질 자산 가치를 충실하게 표현하기 위함이다.",
            "② 차입금 부채 비율을 임의로 낮추기 위한 편법적인 회계 수단을 제공하기 때문이다.",
            "③ 액면 금액보다 항상 자산 총액을 크게 불려 보고함으로써 투자자에게 과대 정보를 주기 위함이다.",
            "④ 당기순이익의 변동성을 고의로 키워 시장의 투기 위험을 완화하려는 목적이다.",
            "⑤ 세무서에 납부할 세액을 최소화하기 위한 법적인 강제 조항이기 때문이다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 화폐의 시간가치(Time value of money)를 반영하여 결산일 시점의 경제적 장부 잔액을 충실하게 표현(Faithful representation)하기 위해 장기성 채권·채무에 대해서는 현재가치 평가를 필수로 요구합니다.\n\n[오답 해설]\n②, ③, ④ 비율 왜곡, 자산 과대 포장, 이익 고의 변동 유도 등은 투명한 회계 기준서 제정 취지와 완전히 정반대되는 행위입니다.\n⑤ 현재가치 평가는 재무보고 유용성에 근거한 회계 기준서 요건이며 세액 최소화 목적이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "시장 금리보다 낮은 명목 이자 조건으로 발행된 장기대여금에 대하여 '유효이자율법'을 적용하여 상각후원가(AC) 평가를 기재하고 있다. 이 경우 각 회계기간 동안 계상되는 '이자수익(장부액 * 유효이자율)'과 실제로 수취하는 '명목 액면이자(액면가 * 명목이자율)'의 상호 비교 및 장부금액 변동에 대한 기술로 옳은 것은?",
        "options": [
            "① 이자수익은 항상 명목 액면이자 수취액보다 작으며, 이로 인해 대여금의 순장부금액은 만기까지 계속 감소한다.",
            "② 이자수익은 항상 명목 액면이자 수취액보다 크며, 그 차액(상각액)만큼 장기대여금의 순장부금액은 만기 시점 액면가액을 향해 매년 증가한다.",
            "③ 이자수익과 명목 이자액은 언제나 동일하며 장부 잔액 또한 불변 고정된다.",
            "④ 이자수익의 초과분은 기말에 무조건 처분손실로 이체되어 자산을 차감 제거한다.",
            "⑤ 차액이 발생할 때마다 유형자산 감가상각누계액을 줄여주는 회계 정리를 실행한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 시장 이자율(할인율)이 명목 이자율보다 높으므로, 최초 현재가치로 평가된 장부액에 유효이자율을 곱해 산출한 '이자수익'은 현금으로 수취하는 '명목 액면이자'보다 큽니다. 이 차액은 현재가치할인차금의 상각액으로서, 대여금 장부액에 가산되어 만기 시점의 액면가를 향해 매기 점진적으로 증가합니다.\n\n[오답 해설]\n① 이자수익이 명목액보다 크게 산출되어 장부금액은 감소가 아닌 증가 흐름을 탑니다.\n③ 시장과 명목 이자율의 격차가 존재하므로 동일할 수 없습니다.\n④, ⑤ 처분손실 이체나 감가상각누계액 연동 등의 주장은 회계학적 상각 원리와 전혀 무관합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "외화 자산/부채의 기말 환율 평가 시 적용되는 '화폐성 항목(Monetary items)'과 '비화폐성 항목(Non-monetary items)'의 구분 원리에 대한 설명 중 K-IFRS 상 가장 올바른 것은?",
        "options": [
            "① 화폐성 항목의 본질적 특징은 계약 상 확정되었거나 결정가능한 화폐단위의 수취권리 또는 인도 의무를 보유하고 있는 경우이다.",
            "② 선급금과 선수금은 미래에 돌려받거나 지급할 계약 상 화폐(현금) 금액이 확정되어 있으므로 대표적인 화폐성 자산/부채이다.",
            "③ 비화폐성 항목은 언제나 기말 결산 마감환율로만 소급 환산하여 재평가이익을 잡는다.",
            "④ 외화대여금과 외화차입금은 수취/인도할 현금액이 유동적으로 변동하므로 대표적인 비화폐성 항목이다.",
            "⑤ 화폐성 항목은 물가가 급변할 시 외화 가치가 정부 고정환율로 빙의되어 환산 손익 인식이 차단된다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1021호에 정의된 화폐성 항목의 본질은 단위당 수령/지급할 화폐 단위의 수량이 고정되었거나 결정가능한 권리 및 의무 상태입니다.\n\n[오답 해설]\n② 선급금과 선수금은 미래에 현금이 아닌 '재화/용역'의 수급 의무이므로 대표적인 '비화폐성 항목'입니다.\n③ 비화폐성 항목은 원칙적으로 역사적 원가(취득일 환율) 적용이 원칙이며, 공정가치 평가 시에만 해당 평가일 환율을 씁니다.\n④ 외화대여금과 차입금은 확정 화폐(외화) 수취권이므로 명백한 '화폐성 항목'입니다.\n⑤ 물가 급변 등과 상관없이 결산 시 마감환율 환산과 환산손익(당기손익) 인식이 이루어집니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "K-IFRS 제1109호 기대신용손실 모형에 따라 대여금 금융자산의 기말 신용 손실 충당금 설정 시 적용하는 '3단계 신용위험 모형'에서, '1단계'와 '2단계'를 구분 짓는 가장 핵심적인 판정 기준은?",
        "options": [
            "① 채무자의 실제 부도 통지가 은행으로부터 정식 접수되었는지 여부",
            "② 금융자산의 최초 인식 시점 이후 신용 위험이 '유의적으로 증가(Significant increase in credit risk)' 하였는지 여부",
            "③ 대여금이 단기성 대여금인지 혹은 3년 이상의 장기성 대여금인지 여부",
            "④ 대여금의 명목 이자수취액이 기중에 전액 지연 수납되었는지의 형식 연체 일수(10일 기준)",
            "⑤ 채무자 이사회 내부에서 감자 결의를 거쳤는지의 여부"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 기대신용손실 3단계 모형에서 1단계와 2단계를 가르는 기준은 '최초 인식 이후 신용위험의 유의적인 증가 여부'입니다. 유의적 증가가 없다면 1단계로 분류해 12개월 기대신용손실을 인식하고, 유의적 증가가 발생하였다면 2단계로 분류해 전체기간 기대신용손실을 인식합니다.\n\n[오답 해설]\n① 실제 부도 발생이나 신용 손상이 객관적으로 입증되는 단계는 최종 '3단계'의 분류 기준입니다.\n③ 대여금의 만기 장단기 성격 자체는 1~2단계 전환의 직접 지배 요건이 아닙니다.\n④ 단순 10일 수준의 사소한 기술적 연체 일수는 유의적 증가의 절대적 가이드라인이 아닙니다 (보통 30일 초과 연체 시 유의적 증가로 간주하는 반증 가능한 가정이 존재합니다).\n⑤ 채무자 내부 자본 변동 결의는 평가에 직접적 기준이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "회사가 대여금(AC 측정 금융자산)을 실행하면서 거래 수수료를 지급하여 이를 최초 취득원가에 가산하였다. 이 거래원가 가산 처리가 대여 자산의 최초 장부금액 및 최초 시점의 '유효이자율(Effective Interest Rate)'에 미치는 영향 분석으로 옳은 것은?",
        "options": [
            "① 최초 장부금액이 증가하고, 이에 따라 자산의 실질 유효이자율은 최초 계약상의 명목(표시)이자율보다 낮아지게 된다.",
            "② 최초 장부금액이 감소하고, 실질 유효이자율은 명목이자율보다 높아지게 된다.",
            "③ 장부금액과 유효이자율 모두 아무런 변동을 겪지 않는다.",
            "④ 유효이자율이 시장 평균을 초과하여 법정 연체 금리 한도로 자동 조정된다.",
            "⑤ 대여 자산의 이자수익 상각 속도가 매 회계연도마다 기하급수적으로 빨라져 이익 변동이 극대화된다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 대여금 실행 시 거래 수수료를 지급하고 이를 원가 가산 처리하면 최초 장부금액이 대여 액면금액보다 늘어납니다. 대출자 관점에서 더 많은 초기 비용을 투자한 격이 되므로 미래 액면이자 수취액 대비 실질적인 수익률(유효이자율)은 원래 약정된 명목이자율보다 하락(낮아짐)하게 됩니다.\n\n[오답 해설]\n② 장부가는 증가하며 유효이자율은 떨어집니다.\n③ 수수료가 자산원가에 누적되므로 장부가와 이자율에 즉시 변동을 초래합니다.\n④ 법정 연체금 등 사법상의 규제 한도로 자동 연계되는 산식은 회계 장부 측정 요건과 무관합니다.\n⑤ 유효이자율법 적용 시 이자수익은 매기 안정적으로 상각누적되어 배분됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "회사가 상가 사무실을 3년 기한으로 계약하고 임대인에게 임차보증금(무이자 반환 조건)을 예치하였다. K-IFRS 상 이 임차보증금의 최초 인식 및 평가에 대한 회계적 의무 기술로 가장 올바른 것은?",
        "options": [
            "① 보증금은 무이자 자산이므로 회수가 보증되어 자산 취득 가격의 현재가치 평가 대상을 배제한다.",
            "② 무이자 조건은 시장 이자율 대비 실질 혜택 누락 성격이므로, 최초 예치액을 시장이자율로 할인한 현재가치로 평가하여 기타금융자산(임차보증금)으로 잡고, 액면가와의 차액은 임차료 선급금 성격(선급임차료 비금융자산)으로 기재한 후 기한 동안 상각비용화한다.",
            "③ 예치금 전액을 임차비용으로 즉시 당기 비용 처리하고 만기 시점에 잡이익으로 털어 넣는다.",
            "④ 임대인의 동의가 없으면 대차대조표 밖 주석 비망으로만 기재해 둔다.",
            "⑤ 보증금 가치와 재평가 이익을 넷팅 상계하여 공정가치를 언제나 ₩0으로 축소한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 장기 임차보증금은 무이자 또는 저리로 예치하므로 대표적인 시간가치 평가 대상 장기성 금융자산입니다. 예치 액면액을 시장이자율로 할인해 임차보증금 자산을 잡고, 차액(할인분)은 사용기간 동안 미연에 혜택을 지불한 '선급임차료' 비금융자산으로 인식한 뒤 기간 동안 리스/임차 비용으로 안분 정산해야 정당한 K-IFRS 회계처리입니다.\n\n[오답 해설]\n① 1년 초과의 무이자 보증금은 현재가치 평가 적용 대상입니다.\n③ 예치금은 환수될 자산이므로 전액 일시 비용화하는 것은 자산 누락 오류입니다.\n④ 계약 상대의 동의 여부와 무관하게 재무상태표 상 적정 자산 분류 계상이 강제됩니다.\n⑤ 공정가치 ₩0 처리는 자산 왜곡입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "금융보증계약을 발행하여 의무를 부담한 기업(보증인)이 해당 보증 계약을 최초 공정가치로 인식한 이후, 결산일 결산 시점에 후속적으로 측정하여 재무제표 부채 잔액을 평가하는 K-IFRS 상의 지배적인 측정 원칙은?",
        "options": [
            "① 최초에 지급받은 수수료 액면가를 만기까지 절대 변경 없이 유지한다.",
            "② 금융보증부채는 기말 결산시점의 보증대상 자산의 시가 총합과 일치시킨다.",
            "③ K-IFRS 제1109호 손실충당금에 따라 산정한 기대신용손실 충당금 금액과, 최초 인식 금액에서 K-IFRS 제1115호에 따라 인식한 수익누계액을 차감한 잔액 중 '더 큰(맥시멈) 금액'으로 후속 측정한다.",
            "④ 보증 상대의 재무 비율 악화 여부와 무관하게 매년 고정 비율 10%씩 부채를 강제 감액한다.",
            "⑤ 금융보증의 공정가치 평가는 기말에 전액 환입하여 영업이익으로 이체 환원한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1109호에 의거하여 금융보증계약 발행자의 후속 측정은 (1) 신용 손실 평가에 의거한 손실충당금 금액과 (2) 최초 공정가치에서 기간 경과 등으로 상각 인식한 수익 누적액을 뺀 금액 중 '더 큰 금액'으로 계상하도록 명문화되어 리스크를 보수적으로 충실하게 반영합니다.\n\n[오답 해설]\n① 최초 가액을 고수하는 것은 신용 리스크 급변을 누락하여 회계 왜곡을 초래합니다.\n② 보증 대상의 전체 시가 총액을 부채로 올리는 것은 실질 의무를 초과하는 과대평가 오류입니다.\n④, ⑤ 고정 10% 감액 조항이나 강제 전액 환입 기법은 기준서에 존재하지 않는 임의적 거짓 기재법입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "외화 단기대여금 및 외화 미수금 같은 화폐성 외화 자산을 기말에 마감환율로 평가 환산하여 발생하는 '외화환산손익(Gain/Loss on Foreign Currency Translation)'의 포괄손익계산서 상 정당한 분류 위치는?",
        "options": [
            "① 재평가잉여금으로 분류하여 기타포괄손익(OCI) 자본 항목에 누적한다.",
            "② 매출원가의 차감 항목으로 기입하여 영업이익을 늘려준다.",
            "③ 당기손익(PL) 내의 '영업외손익(또는 금융손익)' 항목으로 계상하여 당기순이익에 직접 반영한다.",
            "④ 주식 할인발행차금 자본 감소 항목으로 분류한다.",
            "⑤ 판매비와관리비 내 감가상각비 차감 분으로 대체 기입한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 화폐성 외화 자산/부채의 환율 재평가로 유발되는 외화환산손익은 결산 즉시 당기의 손익(영업외손익 또는 금융손익 항목)으로 손익계산서에 인식 보고하여 당기순이익을 변동시킵니다.\n\n[오답 해설]\n① OCI 누적 자본 처리는 화폐성 외화 항목의 기말 재평가 시에는 적용되지 않고, 해외영업소 재무제표 환산 등의 특수 목적 환산 시 활용됩니다.\n②, ④, ⑤ 매출원가 상계, 자본 감소 과목 대체, 감비 차감 등은 발생주의 계정 분류 체계에 위배됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "㈜A는 모회사나 특수관계자에게 자금을 장기로 대여하면서 시장 이자율(10%)보다 턱없이 낮은 조건인 무이자로 ₩100,000을 3년 기한으로 지원 대여하였다. K-IFRS 상 ㈜A가 이 대여 거래 시점에 이행해야 하는 정당한 회계 처리 원칙에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 무이자이므로 약정이자가 없어 현재가치 평가를 생략하고 액면금액 ₩100,000으로 자산을 고정 계상한다.",
            "② 대여 당시 무이자 조건으로 인해 발생하는 현재가치 할인 차액(현재가치할인차금)을 자산의 차감 항목으로 기입하고, 상대방과의 실질적 경제 관계에 따라 차액을 '기부금(비용)', '주주에 대한 증여(자본차감 등)' 또는 '자회사투자주식(자산가산)' 등으로 대차를 매칭하여 인식한다.",
            "③ 대여 시점에 차액 ₩100,000 전액을 단기차입금 부채로 대변 기입한다.",
            "④ 무이자 거래는 세법 상으로만 가공 이자를 산출하므로 회계 장부에는 기재 자체를 금지한다.",
            "⑤ 대여 자산의 소유권이 영구 상실된 것으로 간주하여 처분손실 ₩100,000을 당기 비용 계상한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 무이자 특수관계자 대여는 거래의 실질이 단순 대여가 아니라 경제적 지원(증여, 자회사 투자 등)을 포함하고 있습니다. 최초 대여 시 현재가치 할인액만큼 장기대여금을 감액(현재가치할인차금 계상)하고, 차변 차액은 지원의 법적·경제적 관계에 맞춰 자회사 지분 가산(자회사주식), 자본 거래 차감, 또는 기부금 비용 등으로 계상해야 타당합니다.\n\n[오답 해설]\n① 1년 초과 무이자 대여는 현재가치 평가 생략 대상이 아닙니다.\n③ 유입 대금이 아니라 대여 유출 거래이므로 단기차입금 부채 기입은 대차 방향 오류입니다.\n④ 세법 외에 회계적으로도 실질 수익 비용 배분을 위해 장부 기록 정정이 수반됩니다.\n⑤ 회수 기한이 약정된 채권 자산 거래이므로 자산 완전 제거 및 ₩100,000 전액 손실 처리는 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "대여금 금융자산에 적용하는 기대신용손실 모형에서, '1단계' 분류 자산은 '12개월 기대신용손실'에 기초해 충당금을 잡는 반면, '2단계' 및 '3단계' 자산은 '전체기간 기대신용손실(Lifetime ECL)'에 기초해 충당금을 설정해야 한다. 다음 중 이 '12개월 기대신용손실'의 정당한 회계학적 정의로 올바른 것은?",
        "options": [
            "① 향후 정확히 12개월 동안에 채무자가 갚아야 할 대여금 원금 전액을 말한다.",
            "② 금융상품의 전체 만기 기간 중에서 '보고기간말 이후 향후 12개월 이내에 발생 가능한 금융상품의 채무불이행 사건(Default event)'으로 인해 유발될 수 있는 금융자산의 기대신용손실분(ECL)을 의미한다.",
            "③ 매년 고정 12%의 기대 이자율을 적용하여 가상으로 정산한 미래 가치 할인액이다.",
            "④ 금융보증 채무액 중 향후 12개월 동안 상각 환입 처리될 예정인 이익 가액이다.",
            "⑤ 최초 대여일로부터 12개월 동안에 회사 장부에 계상된 이자수익 누적액을 뜻한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호 상 '12개월 기대신용손실'이란 보고기간말 이후 12개월 이내에 발생 가능한 대여금 금융상품의 부도(Default) 사건으로 인해 발생할 수 있는 전체기간 신용손실의 일부(확률가중손실액)를 뜻합니다.\n\n[오답 해설]\n① 12개월간 상환할 원금 총액 자체를 뜻하는 대차 원금 개념이 아닙니다.\n③, ⑤ 고정 12% 금리 산정이나 이자수익 장부 누적 가치 등은 기대신용손실의 위험 평가 정의와 무관합니다.\n④ 금융보증 계약의 상각 환입 이익과는 정의가 다릅니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "기중에 이전에 대손 확정 판정으로 장부상 자산 및 충당금에서 완전히 정산 제각(제거) 처리하였던 대여금 ₩8,000을 당기에 예상치 못하게 전액 보통예금으로 회수받았다. 이 회수 거래가 ㈜A의 기말 '대손충당금 잔액' 및 '기말 자산총액'에 미칠 최종 누적 영향으로 옳은 것은? (단, 기말 대손충당금은 보충법에 의해 독립적으로 평가 설정 목표에 수렴한다고 가정한다.)",
        "options": [
            "① 당기에 현금이 ₩8,000 유입되었으나, 기말 보충법 평가로 대손상각비가 추가 환입 상계되어 기말 자산과 충당금에는 아무런 최종 변동도 초래하지 않는다.",
            "② 대손충당금 기말 설정액이 ₩8,000만큼 증가하고, 유동자산총액은 변동이 없다.",
            "③ 대손충당금 기말 잔액은 기말 목표치로 수렴하므로 오류 없이 적정하며, 기중 회입된 현금 ₩8,000의 실제 유입에 힘입어 기말 '자산총액'은 ₩8,000만큼 최종 순증가(당기순이익 증가 연동)한다.",
            "④ 자산총액은 ₩8,000 감소하고, 대손상각비 비용만 ₩8,000 증가한다.",
            "⑤ 대변 자본금 잔액이 ₩8,000 증가하는 자본 조정 결과만 유발된다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 제각 대여금의 기중 회수 거래 분석:\n1. 기중 분개: (차) 보통예금 8,000 / (대) 대손충당금 8,000. 현금이 실제 들어와 보통예금 자산이 ₩8,000 늘어납니다.\n2. 기말 보충법: 기말 대손충당금은 연령분석이나 채권 잔액 조건 등에 기해 산출된 목표액(예: ₩10,000)으로 고정 설정됩니다. 기중에 충당금이 ₩8,000 복원되어 늘어나 있었으므로, 기말에 보충 계상할 대손상각비 비용 적립액은 그만큼 줄어들게(비용 삭감, 이익 증가) 됩니다.\n3. 최종 합산: 충당금 잔액은 정상 목표치로 안착하며, 순이익 및 자본 증가로 인해 기말 자산총액(보통예금 유입분 반영)은 최종 ₩8,000만큼 증가하게 됩니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 현금 유입에 따른 자산의 절대 증가 성격과 기말 보충 계산 후의 피드백 결과를 왜곡 오판한 지문들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "대여자가 채무자의 재무 상태 악화를 이유로 대여 거래 계약의 일부 상환 약정 조건을 완화 조정(Debt restructuring)해 주었다. K-IFRS 상 조건 변경 전후의 미래 현금흐름 현재가치 격차가 기존 대여금 장부금액 대비 최소 몇 % 이상 차이 날 때, 기존 금융자산을 소멸(제거)시키고 신규 금융자산으로 대체 계상해야 하는 '실질적 조건 변경' 조건으로 간주하는가?",
        "options": [
            "① 1% 이상",
            "② 5% 이상",
            "③ 10% 이상",
            "④ 20% 이상",
            "⑤ 50% 이상"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1109호 및 관련 실무 지침에 따라 조건 변경으로 인한 새로운 조건 하의 현금흐름 현재가치와 기존 금융자산 장부금액의 차이가 기존 장부금액의 최소 '10% 이상' 격차가 발생할 때 실질적인 조건 변경(Substantial modification)으로 보아 기존 자산을 제거하고 신규 자산을 공정가치로 새로 인식합니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 기준서 상의 실질 조건 변경의 정량 기준인 10% 요건(10% 테스트)에 위배되는 잘못된 수치 비율들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "㈜A는 X1년말 보유 대여금에 대해 결산일까지 경과된 미수이자 ₩3,000을 장부에 미수수익 자산으로 기입하는 결산 정정 분개를 완전히 누락한 상태로 X1년 보고를 종결하였다. 이 누락 오류가 X1년말 재무제표에 미친 최종 왜곡 영향은?",
        "options": [
            "① 유동자산이 ₩3,000 과대계상되었고, 당기순이익은 적정하다.",
            "② 유동부채가 ₩3,000 과소계상되었고, 당기순이익은 ₩3,000 과대계상되었다.",
            "③ 유동자산이 ₩3,000 과소계상되었고, 당기순이익 또한 ₩3,000 과소계상(수익 누락)되었다.",
            "④ 자본총계만 ₩3,000 과대계상되고 자산과 부채는 적정하다.",
            "⑤ 재무제표 수치 평균화 법칙에 따라 아무런 왜곡도 수반되지 않는다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 미수수익 누락에 따른 왜곡 분석:\n- 정당한 분개: (차) 미수수익 3,000 / (대) 이자수익 3,000\n- 누락 영향: 자산 항목인 미수수익 ₩3,000이 잡히지 않아 유동자산이 ₩3,000 과소계상되었고, 이자수익 ₩3,000이 누락되어 당기 이익이 ₩3,000 과소계상되는 결과를 초래하였습니다.\n따라서 유동자산 및 당기순이익이 각각 ₩3,000 과소계상된 것이 참입니다.\n\n[오답 해설]\n①, ②, ④ 자산과 이익이 과소 계상되었으므로 과대화 주장 등은 오류 분석 실수입니다.\n⑤ 자산과 손익 양 항목에 직접적인 왜곡이 발생했습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "대여금 금융자산에 대하여 과거에 신용 손상 발생 판정으로 인식했던 손실충당금(대손충당금)을, 당기 결산일에 신용 등급 회복에 기해 '손상차손환입(Reversal of impairment loss)'으로 장부에 다시 이익 환원하고자 한다. K-IFRS 상 이 환입액을 계상할 수 있는 한도(Limit) 규정으로 올바른 것은?",
        "options": [
            "① 제한 없이 거래처 신용 등급이 가용한 최댓값 수준으로 무한대로 환입할 수 있다.",
            "② 대여금의 최초 취득 액면금액의 150% 범위까지 환입이 제한된다.",
            "③ 과거에 손상을 인식하지 않았더라면 도달하였을 환입일 현재의 '상각후원가(AC) 장부금액'을 한도로 하여 그 범위 내에서만 환입할 수 있다.",
            "④ 당기 포괄손익계산서 상 매출액 총합의 5% 선으로 제한된다.",
            "⑤ 금융 보증 계약의 유보금 잔액 이하로만 강제 고정된다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 상 대여금이나 수취채권 등 상각후원가(AC) 자산의 손상차손환입 한도는 과거에 자산 손상을 인식하지 않았을 경우의 환입일 현재 시점 도달 가능한 상각후원가 장부금액을 초과할 수 없습니다.\n\n[오답 해설]\n① 한도가 없다면 자산을 부당하게 부풀려 보고하는 분식이 조장되므로 불가능합니다.\n② 액면가 150% 등은 회계 논리에 맞지 않는 자의적 수치입니다.\n④, ⑤ 매출액 대비나 보증 유보금 등의 기준선은 손상차손환입 한도의 결정과 무관합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s04-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "㈜A는 모회사로부터 자금을 장기 대여받아 부채로 가지고 있던 중, 모회사가 대여금에 걸린 명목 이자율 조건을 시장 금리(10%)보다 낮은 5%로 소급 감면 변경해 주어 부채의 공정가치가 일부 하락 정산되었다. 채권자인 모회사 관점에서 이 대출 조건 변경에 따른 가치 하락액의 올바른 처리 장소는?",
        "options": [
            "① 당기 포괄손익계산서 상 '이자수익' 증가로 계상한다.",
            "② 자녀 또는 지분 관계에 따른 모회사 주주로서의 '자본 거래(기부금/자본잉여금 차감 등)' 혹은 실질 관계에 따라 당기 손실 비용으로 인식하여 반영한다.",
            "③ 대변의 주식발행초과금을 즉시 늘려 적는다.",
            "④ 부기 상의 비망 거래일 뿐이므로 어떠한 차대 대차 정정도 이행하지 않는다.",
            "⑤ 감가상각누계액의 환입 이익으로 영업이익에 직접 가산한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 특수관계자(모회사-자회사 등) 간의 비시장적 이자율 감면 조건 변경은 단순 상거래 손익이 아닌 '자본 거래(주주로서의 출자 또는 부의 이전)'의 성격을 내포합니다. 채권자(모회사)는 장부금액 감소 차액을 자회사 투자 주식 원가 가산 또는 자본 조정 등으로 회계처리하여 거래 실질을 정확하게 규명해야 합니다.\n\n[오답 해설]\n① 가치가 깎였는데 이자수익이 늘어난다는 주장은 모순입니다.\n③ 모회사는 발행 주체가 아닌 양도/대여 주체이므로 주발초를 직접 기재하지 못합니다.\n④ 현재가치 및 장부가액의 영구적 차액이 완성되었으므로 비망 기록으로 그쳐서는 안 됩니다.\n⑤ 감비 환입 등 유형자산 평가와는 연동되지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    }
]

questions.extend(new_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully added 25 questions. Total questions in database: {len(questions)}")
