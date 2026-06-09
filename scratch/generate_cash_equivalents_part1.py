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
    "item": "2절 현금 및 현금성자산"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q1651 ~ Q1660) ---
    {
        "id": "practice-accounting-ch07s02-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 상 기업의 재무상태표에 공시되는 '현금'의 구성 요소에 속하지 않는 것은?",
        "options": [
            "① 지폐와 주화 등 정부가 공인한 통화",
            "② 통화와 동일한 효력으로 통용되는 수표 및 우편환증서 등의 통화대용증권",
            "③ 은행에 개설되어 수시 입출금이 자유로운 당좌예금 및 보통예금",
            "④ 금융기관 지점이나 현장 부서에서 소액 경비 결제를 위해 보유하는 지점전도금",
            "⑤ 취득일로부터 6개월 뒤에 만기가 도래하는 양도성예금증서(CD)"
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ 취득 당시에 만기가 3개월을 초과하는 양도성예금증서(CD)는 현금이나 현금성자산이 아니며 '단기금융상품' 등으로 분류되어야 합니다.\n\n[오답 해설]\n① 통화(지폐, 주화)는 현금의 핵심 성격입니다.\n② 수표나 우편환 등의 통화대용증권은 즉시 현금화가 가능하므로 현금에 속합니다.\n③ 당좌예금과 보통예금은 인출에 제한이 없는 요구불예금으로 현금에 해당합니다.\n④ 소액 현금 결제를 위한 전도금(소액현금)은 현금에 분류됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "K-IFRS 제1007호 '현금흐름표'에 정의된 '현금성자산(Cash Equivalents)'의 핵심 요건으로 가장 올바른 것은?",
        "options": [
            "① 취득 가격의 하락 위험이 50% 미만으로 비교적 변동성이 적은 상장 지분상품 주식",
            "② 큰 거래비용 없이 확정된 금액의 현금으로 전환이 용이하고 가치변동의 위험이 경미한 단기투자자산",
            "③ 보고기간종료일(결산일)로부터 3개월 이내에 최종 만기가 도래하는 모든 단기채권",
            "④ 거래처에 외상 대금으로 제공하고 1년 뒤에 어음으로 결제받기로 약정한 외상매출금",
            "⑤ 법적으로 인출 및 담보 설정 제약이 걸려 있어도 금리가 높은 모든 정기적금"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 상 현금성자산은 유동성이 매우 높은 단기 투자자산으로서 확정된 금액의 현금으로 전환이 용이하고, 이자율 변동 등에 따른 가치변동의 위험이 경미해야 합니다.\n\n[오답 해설]\n① 지분상품(주식)은 공정가치 변동 위험이 크고 수취 금액이 미확정이므로 원칙적으로 현금성자산이 될 수 없습니다.\n③ 기준서 상 만기 조건은 결산일 기준이 아닌 '취득 당시 만기가 3개월 이내'여야 합니다.\n④ 외상매출금은 수취채권이지 투자자산인 현금성자산이 아닙니다.\n⑤ 인출 제약이나 사용 제한이 있는 자산은 현금성자산에서 제외됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "금융상품이 K-IFRS 상 현금성자산으로 분류되기 위하여 충족해야 하는 만기 조건 기준으로 올바른 것은?",
        "options": [
            "① 보고기간종료일(결산일)로부터 만기일이 1년 이내",
            "② 금융상품의 '최초 취득일로부터 만기일이 3개월(90일) 이내'",
            "③ 금융상품의 발행일로부터 만기일이 1년 이내",
            "④ 결산일로부터 역산하여 최종 상환일까지 잔존 기간이 3개월 이내",
            "⑤ 회사의 평균 영업주기(Operating cycle)의 50% 이내 기간에 도래"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1007호 문단 7에 따라 투자자산이 현금성자산으로 분류되기 위해서는 '취득일로부터 만기일이 3개월 이내'에 도래하는 것이어야 합니다.\n\n[오답 해설]\n① 1년 이내 조건은 일반적인 유동/비유동 구분 및 단기금융상품 구분 요건입니다.\n③ 발행일이 아닌 자사 기준의 '취득일'이 기점입니다.\n④ 결산일 기준 잔존 기간 3개월 조건은 잘못된 오답 유도 조항입니다.\n⑤ 영업주기와 현금성자산 만기 판정은 연계되지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "다음 중 K-IFRS 재무상태표의 '현금및현금성자산'에 합산하여 보고할 수 있는 항목은?",
        "options": [
            "① 세무서에 납부하기 위해 세금고지서 대용으로 사놓은 수입인지",
            "② 거래처에 송금하기 위해 우체국에서 교환하여 보관 중인 우편환증서(Postal money order)",
            "③ 등기 우편 발송을 위해 다량 구매하여 캐비닛에 넣어둔 우표",
            "④ 거래상대방에게 개인 채무 관계의 증빙으로 수취해 둔 차용증서",
            "⑤ 당좌거래 개설 시 당좌계약 보증 용도로 은행에 장기 예치한 당좌개설보증금"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우편환증서는 우체국에서 즉시 통화(현금)와 교환하여 사용이 가능한 대표적인 통화대용증권으로, 현금및현금성자산에 합산 공시합니다.\n\n[오답 해설]\n① 수입인지와 ③ 우표는 소모품비나 선급비용으로 처리하며 현금이 아닙니다.\n④ 차용증서는 단기/장기대여금 채권으로 잡힙니다.\n⑤ 당좌개설보증금은 예치 기간 동안 사용이 법적으로 구속 및 제한되므로 보통 '장기금융상품(비유동자산)'으로 분류합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "㈜감평이 거래처로부터 받아 보관 중인 당좌수표 중, 수표 권면 상의 발행일자가 X2년 2월 15일이나 현재 시점은 X1년 12월 31일인 수표(선일자수표)의 올바른 회계적 처리 방법은?",
        "options": [
            "① 통화대용증권에 해당하므로 X1년말 재무상태표 상 현금으로 기재한다.",
            "② 수표 상 발행일인 X2년 2월 15일 전까지는 '수취채권(받을어음 등)'으로 기재하고, 발행일 이후에 비로소 현금으로 전환 처리한다.",
            "③ 부도수표와 성격이 같으므로 전액 대손충당금과 100% 상계하여 제거한다.",
            "④ 자산 인식을 취소하고 영업외비용으로 X1년에 전액 털어낸다.",
            "⑤ 선일자수표는 법적으로 양도가 불가능하므로 잡손실 비용으로 계상한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 선일자수표(Post-dated cheque)는 수표 상 기재된 발행일 전까지는 은행에 제시하더라도 결제(현금화)를 받을 수 없습니다. 따라서 실질적으로 단기 어음과 성격이 동일하므로 발행일까지는 '수취채권(매출채권 혹은 받을어음 등)'으로 잡고, 발행일 도래 시점에 현금으로 분류 정정해야 합니다.\n\n[오답 해설]\n① 즉시 현금화가 불가능하므로 X1년말 현금 분류는 오답입니다.\n③ 부도가 난 상태가 아니므로 대손 강제 처리는 틀렸습니다.\n④, ⑤ 실질적 채권 권리가 있으므로 비용 삭감 처리는 위법입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "기업이 당좌예금의 잔액을 초과하여 발행한 당좌수표로 인해 발생한 마이너스 예금 잔액인 '당좌차월(Bank Overdrafts)'의 K-IFRS 상 올바른 보고 위치는?",
        "options": [
            "① 당좌예금 자산액에서 직접 마이너스로 차감하여 순액 표시한다.",
            "② 기타포괄손익누계액(자본항목)의 차감 과목으로 자본 계정에 보고한다.",
            "③ 단기 대여채권의 평가충당금 과목으로 기재한다.",
            "④ 재무상태표 상 부채 항목인 '단기차입금'으로 별도 공시하며, 임의로 당좌예금과 상계하지 않는다.",
            "⑤ 무형자산(영업권)의 취득 부대 비용으로 얹어 무형자산으로 이체한다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 당좌차월은 은행으로부터 일시적으로 돈을 빌린 것과 같은 단기 신용 공여이므로 재무상태표 상 '단기차입금(유동부채)'으로 별도 표시해야 합니다. 자산과 부채의 상계 표시 금지 원칙(총액 표시 원칙)에 따라 당좌예금 자산에서 직접 차감 넷팅하여 기재하지 않습니다.\n\n[오답 해설]\n① 상계 표시 금지 위반입니다.\n② 자본 항목이 아닌 유동부채입니다.\n③, ⑤ 대여 평가충당이나 영업권 배분은 회계 논리에 맞지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "보통예금 잔액 중 ₩1,000,000이 금융기관과의 단기 차입 계약에 따른 '담보(Collateral)'로 제공되어 사용 및 인출이 엄격히 차단되어 있다. 이 제한 자산의 K-IFRS 상 올바른 재무상태표 기재 과목은?",
        "options": [
            "① 사용이 금지되어 있어도 요구불예금이므로 현금및현금성자산으로 그대로 보고한다.",
            "② 금융자산의 인식이 상실되었으므로 자산을 전액 장부에서 제거하고 당기처분손실로 떤다.",
            "③ 사용제한 사유 및 기간에 따라 '단기금융상품' 또는 '장기금융상품' 등으로 분류하고, 관련 담보 설정 제한 사항을 주석으로 공시한다.",
            "④ 부채 항목인 '단기보증채무' 부채로 대변에 평행 기입한다.",
            "⑤ 자본 내 임의적립금 항목으로 직접 대체 계상한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 담보 설정 등으로 인출이나 사용이 제한된 예금은 언제든지 찾아서 쓸 수 있는 상태가 아니므로 현금및현금성자산에서 제외하여야 합니다. 제한 기간에 따라 단기/장기금융상품으로 대체 분류하고 주석을 적어야 합니다.\n\n[오답 해설]\n① 사용 및 인출 제약이 걸리면 현금성 분류가 불가합니다.\n② 소유권 통제 자체가 완전히 상실되어 자산이 제거되는 거래가 아니며 단순 담보 보류 상태입니다.\n④, ⑤ 부채 평행 기입이나 자본적립금 대체는 복식부기에 맞지 않는 잘못된 기술입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "회사가 거래처로부터 수취하여 결제를 위해 보유하고 있던 당좌수표를 은행에 제시하였으나, 발행자의 잔고 부족으로 최종 지급이 거절되어 반환받았다(부도수표). 이 부도수표의 정당한 자산 분류 명칭은?",
        "options": [
            "① 통화대용증권이므로 현금및현금성자산으로 유지한다.",
            "② 은행에서 입금을 취소당했으므로 즉시 무형자산(개발비)으로 바꾼다.",
            "③ 지급이 영구 거절되었으므로 대손 상계 처리한 뒤 '매출채권' 혹은 다른 '수취채권' 계정으로 재이전하고 회수 가능성을 재검토한다.",
            "④ 부채 항목인 '미지급부도부채'로 분류한다.",
            "⑤ 부도수표는 법적 효력이 전혀 없으므로 즉시 자산제거(분개 없음)로 털어버린다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 부도수표는 더 이상 언제든지 은행에 가서 돈으로 바꿀 수 있는 통화대용증권이 아니므로 현금 자격을 잃습니다. 따라서 현금 계정에서 제외한 뒤 원인 매출채권 등으로 정정 이전하고 손상 여부를 판단해야 합니다.\n\n[오답 해설]\n① 현금화 권리가 보류·거절되었으므로 현금 유지는 불가합니다.\n② 무형자산이나 ④ 부채 분류는 계정 과목 성격에 전혀 맞지 않는 오답입니다.\n⑤ 권리 추심 의무가 여전히 회사에 상존하므로 장부에서 무단 소멸시킬 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "㈜감평의 결산담당자가 보유 현금 금고를 실사하던 중 발견한 '주식 배당금 지급 통지표(Dividend Warrant)'의 올바른 자산 분류는?",
        "options": [
            "① 배당금은 현금 수령 권리가 확정되어 즉시 지급청구가 가능하므로 통화대용증권(현금)으로 분류한다.",
            "② 피투자회사의 자본 거래이므로 투자지분상품 주식 계정에 직접 더해 기재한다.",
            "③ 미수채권이므로 '미수금' 계정으로 만기 정산 처리한다.",
            "④ 아직 현금이 유입되지 않았으므로 자산으로 기재하지 않고 주석 공시만 한다.",
            "⑤ 피투자사가 배당을 실제 송금해 줄 때까지는 유형자산(기타기계장치)으로 넣어 둔다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 배당금지급통지표는 은행이나 지정 지급처에 들고 가면 즉시 현금(통화)으로 바꾸어 주므로 통화대용증권에 속하며, 기말에 '현금및현금성자산'에 산입합니다.\n\n[오답 해설]\n② 주식 자체의 취득원가나 수량 변동이 아니므로 주식 자산가에 가산하지 않습니다.\n③ 현금과 동등한 환금력이 있으므로 단순 미수채권으로 묶어두지 않고 즉시 현금 처리합니다.\n④, ⑤ 자산 인식의 생략이나 기계장치 오이전은 회계원리 위반입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "다음 중 기말 결산 시점에 은행에서 통보받은 당좌예금 원장 잔액과 기업의 장부 상 당좌예금 잔액의 차이를 파악하고 올바른 예금 잔액을 확정하기 위해 작성하는 서류의 명칭은?",
        "options": [
            "① 시산표(Trial Balance)",
            "② 재무상태표(Statement of Financial Position)",
            "③ 은행계정조정표(Bank Reconciliation Statement)",
            "④ 현금흐름표(Statement of Cash Flows)",
            "⑤ 주주지분변동표(Statement of Changes in Equity)"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 은행계정조정표는 회사 장부 상의 당좌예금 잔액과 거래 은행의 통장 잔액 간 불일치 원인을 분석하고 올바른 예금 잔액을 계산하여 장부를 정정하는 보조 명세서입니다.\n\n[오답 해설]\n① 시산표는 총계정원장 분개의 대차 정합성을 검증하는 표입니다.\n② 재무상태표는 결산이 완전히 끝난 후 종합 재무현황을 공시하는 주재무제표입니다.\n④ 현금흐름표는 기중 현금의 유출입 정보를 활동별로 분류해 나타내는 서류입니다.\n⑤ 주주지분변동표는 자본 변동 내역을 나타냅니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    # --- L2 (이해): 15문항 (Q1661 ~ Q1675) ---
    {
        "id": "practice-accounting-ch07s02-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "K-IFRS 상 현금성자산을 판정할 때 3개월 기준이 '보고기간종료일(결산일)'이 아닌 '금융상품 취득일'을 기준으로 적용되어야 하는 이론적 및 실무적 이유로 가장 올바른 진술은?",
        "options": [
            "① 결산일 기준으로 판정하면, 원래 만기가 3년인 장기 회사채라도 결산일에 임박하여 만기가 2달 남은 시점에 매입했다면 자산의 본질적 변동 위험이 달라지므로 이를 배제하기 위함이다.",
            "② 금융자산의 분류는 취득 시점의 자산 성격과 계약 조건을 기준으로 확정 지어야만 거래 인식의 전관적 일관성이 보장되며, 기중에 시시각각 만기일이 다가옴에 따라 자산 분류를 요구불예금으로 수시로 변경하는 것은 정보 이용자의 혼선을 초래하기 때문이다.",
            "③ 세법에서 결산일 기준 3개월 자산에 대하여 이자소득세를 100% 면제해 주는 우대 조항을 두고 있기 때문이다.",
            "④ 결산일 기준으로 기간을 계산하면 회계 프로그램의 정산 모듈이 오작동하여 부도수표 추적 분개가 실행되지 않기 때문이다.",
            "⑤ 취득일 기준 계산이 결산일 기준 계산보다 회사 보유 자산 총액을 크게 부풀려 주는 영업적 이점이 있기 때문이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS에서 현금성자산을 취득일 기준으로 판정하는 이유는 자산의 분류가 기중 시간 경과에 따라 수시로 변하는 것을 방지하기 위함입니다. 만약 결산일 기준 잔존만기로 판정한다면, 최초 만기가 3년인 회사채도 시간이 흘러 만기가 3달 이내로 남는 시점에 갑자기 '현금성자산'으로 재분류되는 불일치(회계 일관성 상실)가 발생하므로 최초 취득 당시의 본질적 속성을 고수하도록 강제하는 것입니다.\n\n[오답 해설]\n① 만기가 2달 남았을 때 매입했다면 취득 당시 만기가 3개월 이내이므로 오히려 현금성자산 분류 요건을 통과합니다. 따라서 예시는 적절하지 않습니다.\n③ 세법 상의 이자 면제 조항이나 ④ IT 프로그램 오작동, ⑤ 자산 총액 부풀리기 등은 기준서의 이 조항 채택 근거와 상관이 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "은행계정조정표를 작성할 때 발생하는 차이 요인 중 '은행측 조정사항'에 해당하는 거래 항목은?",
        "options": [
            "① 거래처 은행을 통해 매출채권(추심어음)이 추심되어 기업 예금계좌에 입금되었으나, 회사가 은행으로부터 아직 입금 통지를 받지 못한 항목",
            "② 기업이 수표를 발행하여 거래처에 대금으로 지급하였으나, 거래처가 기말까지 은행에 수표의 지급 제시를 하지 않아 은행 장부에 출금되지 않은 기발행미인출수표",
            "③ 당좌예금 계좌에 대하여 당기 중 발생한 당좌차월이자 및 은행 수수료가 예금에서 자동 출금되었으나 회사가 장부에 기록하지 않은 거래",
            "④ 고객이 발행하여 입금된 수표가 부도 처리되어 은행에서 차감되었으나 회사가 장부 정정 분개를 하지 않은 항목",
            "⑤ 회사의 장부담당자가 당좌예금 입금액 ₩12,000을 ₩21,000으로 장부에 오기입한 수표 기장 오류"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 기발행미인출수표는 회사는 수표 발행 시점에 자사 장부에서 예금의 감소를 이미 반영하였으나, 은행은 수표 보유자가 지급 제시를 하러 올 때까지 출금 처리를 유보하고 있습니다. 따라서 은행측 장부 잔액에서 이 금액만큼 차감 조정을 해야 불일치가 해소되므로 '은행측 조정사항'에 해당합니다.\n\n[오답 해설]\n①, ③, ④ 은행은 이미 입출금 처리를 완결했으나 회사가 장부에 반영하지 못한 항목들이므로 '회사측 조정사항'에 해당합니다.\n⑤ 회사의 오기입 오류이므로 회사측 장부 잔액을 정정 조정해야 하는 회사측 조정사항입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "은행계정조정표를 작성할 때 발생하는 차이 요인 중 '회사측 조정사항'에 해당하는 거래 항목으로만 올바르게 짝지어진 것은?",
        "options": [
            "① 미기입예금, 기발행미인출수표",
            "② 미통지입금(어음추심액), 미통지출금(은행 수수료 및 부도수표)",
            "③ 미기입예금, 은행 측의 송금 오류 수정",
            "④ 기발행미인출수표, 회사 장부담당자의 예금 오기입 정정",
            "⑤ 미통지입금, 은행의 이중 입금 오기입 수정"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 회사측 조정사항은 은행은 정상적으로 입출금 처리를 완료했으나, 회사가 아직 통지를 받지 못하거나 장부에 누락 및 오기하여 회사 장부 잔액에 가감 처리가 요구되는 항목들입니다. 미통지입금(추심 등), 미통지출금(수수료, 부도 등)이 이에 해당합니다.\n\n[오답 해설]\n①, ③ 미기입예금과 기발행미인출수표는 회사는 처리했으나 은행이 아직 기입하지 않은 '은행측 조정사항'입니다.\n④ 기발행미인출수표는 은행측 조정사항입니다.\n⑤ 은행의 이중 오기입은 은행 측에서 직접 정정해야 하는 은행측 조정사항입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "은행계정조정표 조정 항목 중 '미기입예금(미통지예금)'에 관한 설명 및 올바른 조정 방법으로 옳은 것은?",
        "options": [
            "① 회사가 기말에 수표를 발행했으나 거래처가 인출하지 않은 것으로, 회사 장부에서 차감 조정한다.",
            "② 회사가 은행에 현금을 마감 직전에 입금하였으나 은행의 영업 시간 종료로 통장에 아직 입금 처리가 안 된 항목으로, 은행 측 잔액에 가산(+) 조정한다.",
            "③ 은행이 회사 통장에 발생한 이자액을 회사 몰래 자동 가산해 준 것으로, 회사 측 잔액에 가산(+) 조정한다.",
            "④ 거래처가 부도를 내어 수표 대금이 정산 취소된 것으로, 은행 측 잔액에서 차감(-) 조정한다.",
            "⑤ 예금 잔액이 마이너스로 넘어가 단기차입금 부채로 자동 이체된 계정이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 미기입예금은 회사는 은행 창구나 야간금고를 통해 예금을 입금 처리하고 장부에 예금 증가를 적었으나, 은행은 마감 시간 도래 등으로 인해 원장에 아직 기입을 완료하지 못한 상태의 금액입니다. 따라서 은행 측 잔액에 가산(+) 조정을 수행해야 불일치가 해소됩니다.\n\n[오답 해설]\n① 이는 기발행미인출수표에 대한 설명입니다.\n③ 이는 미통지입금(회사 측 가산 사항)에 해당합니다.\n④ 부도 처리는 회사 장부에서 자산을 깎아내는 회사 측 차감 조정 사항입니다.\n⑤ 당좌차월에 대한 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "은행계정조정표의 불일치 차이 원인 중 '기발행미인출수표(Outstanding Cheques)'에 관한 설명 및 올바른 조정 방법으로 옳은 것은?",
        "options": [
            "① 회사가 수표를 발행하여 장부 상 예금을 이미 감액시켰으나, 거래처가 은행에 대금 청구를 하지 않은 상태이므로 은행 측 장부 잔액에서 차감(-) 조정한다.",
            "② 은행이 발행사의 자금을 강제로 인출하여 보관하고 있는 예치금으로, 회사 장부에 가산(+) 조정한다.",
            "③ 주식 매각 대금이 회사 통장으로 입금 완료된 항목이므로 회사 장부 잔액에서 차감(-) 조정한다.",
            "④ 회사가 결산일에 수표를 대가로 받아 금고에 넣어 둔 것으로, 은행 측 장부 잔액에 가산(+) 조정한다.",
            "⑤ 선일자수표의 발행일이 만료되어 자동으로 차입금 부채가 소멸한 분개 항목이다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 기발행미인출수표는 회사는 수표를 발행해 주면서 자신의 예금 계정을 깎았으나, 수표를 받은 자가 기말 현재 아직 거래 은행에 수표를 들고 가서 돈을 찾아가지 않아 은행 장부에는 출금이 안 잡혀 있는 상태입니다. 따라서 은행 측 잔액에서 차감(-) 처리해 주어야 양 장부 잔액이 일치하게 됩니다.\n\n[오답 해설]\n②, ③, ④, ⑤ 기발행미인출수표의 실질적 정의 및 회계 조정 원리와 부합하지 않는 오답 설명들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "기말 은행계정조정표 분석 결과 발견된 다음 차이 항목들 중, 조정 결산일 당일 기업이 장부에 '오류 수정 분개(Adjusting Journal Entries)'를 필수로 작성해서 당좌예금 장부 잔액 자체를 고쳐주어야 하는 대상은?",
        "options": [
            "① 회사가 밤 11시에 입금한 야간금고 예입금으로 은행 원장에 기입되지 않은 미기입예금 ₩50,000",
            "② 회사가 거래처에 대금 지급용으로 발행해 주었으나 거래처 사장이 주머니에 넣고 아직 은행에 가지 않은 기발행미인출수표 ₩100,000",
            "③ 은행이 기중 당좌차월 한도 초과 이자비용 ₩3,000을 회사 계좌에서 자동 출금 처리하였으나, 회사 장부에 이자비용 및 당좌예금 차감 분개가 반영되지 않은 항목",
            "④ 다른 회사가 당좌수표를 발행하여 은행 측의 기입 실수로 우리 회사 당좌예금 통장 잔액에서 차감된 은행 측 오기입액 ₩20,000",
            "⑤ 결제 대행사가 당좌거래를 위해 개설해 준 단기 보증 증권의 발행 수수료"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 은행계정조정표 작성 후 회사 장부를 올바른 예금 잔액으로 정정하는 수정 분개는 '회사측 조정사항(회사 장부에 누락되거나 오류가 있는 항목)'에 대해서만 실행합니다. 은행 측 잔액 차이 원인인 미기입예금(①)이나 기발행미인출수표(②), 은행 측 오기입(④)은 은행 측의 내부 정정 사안이거나 시간 경과에 따라 자동 해결되는 사항이므로 회사 장부에 수정 분개를 반영할 필요가 없습니다.\n\n[오답 해설]\n①, ②, ④ 모두 은행 측 장부 원장의 잔액과 연결되는 차이 원인이므로 회사 장부 수정 분개 대상이 아닙니다.\n⑤ 보증서 발행 수수료는 당좌예금 차이 조정표 상의 직접 조정 거래가 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "㈜감평의 회계담당자는 은행계정조정표를 조정하는 과정에서 발견한 다음 오류 및 불일치 거래에 대하여 수정 분개를 반영하고자 한다. 이 중 ㈜감평의 'X1년도 당기순이익(PL)'에 직접적으로 증가 혹은 감소 영향을 미치는 수정 분개가 요구되는 거래는?",
        "options": [
            "① 거래처 ㈜진우로부터 외상출심 대금 ₩50,000이 당좌예금 통장으로 직접 송금 입금되었으나 회사 장부에 누락되었던 미통지입금",
            "② 거래처에 외상매입금 결제를 위해 발행해 주었으나 아직 은행에서 인출되지 않은 수표 ₩100,000",
            "③ 은행이 당좌예금 보관 계좌 관리 용도로 당좌수수료 ₩5,000을 통장에서 자동 인출하였으나 회사가 누락한 거래",
            "④ 회사가 은행 창구에 수표 ₩20,000을 저녁에 예입하였으나 은행 장부에 누락된 미기입예금",
            "⑤ 회사가 보유 중이던 만기 미도래 양도성예금증서(CD)를 정기예금과 맞교환한 거래"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 은행 수수료 ₩5,000의 누락분은 (차) 수수료비용 5,000 / (대) 당좌예금 5,000 으로 회사 장부에 수정 분개를 기입합니다. 이때 차변에 수수료비용(PL 당기비용)이 계상되므로 당기순이익이 ₩5,000만큼 감소하게 됩니다.\n\n[오답 해설]\n① 외상매출금 회수액 입금은 (차) 당좌예금 50,000 / (대) 외상매출금 50,000 의 자산 교환 분개이므로 당기순이익에는 아무런 영향을 주지 않습니다.\n②, ④ 회사 장부에 수정 분개를 하지 않는 은행측 조정사항 항목입니다.\n⑤ 자산 항목 간 교환 거래이므로 손익에 영향이 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "피투자회사가 현금배당금 ₩10,000을 현금 및 현금성자산으로 분류하여 기재해 두었다. 이 배당금이 수취 시점에 현금성자산의 지위를 획득하기 위한 조건으로 가장 올바른 것은?",
        "options": [
            "① 배당금을 주식 계좌로 송금받지 않고 실물 주화 및 지폐로 직접 인출 보관해야만 현금화가 성립한다.",
            "② 현금배당금 지급일이 선언된 결의일로부터 실제로 배당금을 수취 가능한 시점까지의 대기 기간이 3개월 이내여야 한다.",
            "③ 현금배당 지급 통지표를 수령한 즉시 금융기관에서 제한 없이 통화와 현금 상환 교환이 가능해야 한다.",
            "④ 배당금의 30%를 반드시 정부 공채 증권으로 강제 전환 투자해야 현금성자산이 유지된다.",
            "⑤ 피투자회사의 자본잉여금이 이익잉여금 처분 비율의 50%를 초과하는 정상 상태여야 한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 현금배당 통지표를 수령한 경우, 주주는 그 서류를 지급 장소(은행 등)에 제시하여 언제든지 아무런 제약이나 수수료 부담 없이 바로 현금으로 교환하여 찾을 수 있어야 비로소 즉각적인 환금력(통화대용증권)을 인정받아 현금및현금성자산으로 기재될 수 있습니다.\n\n[오답 해설]\n① 통장 예치 상태라도 보통예금 등은 요구불예금이므로 현금에 속합니다.\n② 배당금의 현금성 판정은 대기기간이 아닌 즉시 환금성 유무에 의해 결정됩니다.\n④, ⑤ 강제 전환 의무나 자본 비율 조건 등은 기준서에 존재하지 않는 임의 기술입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "회사가 보유 중인 만기 지급일이 도래한 사채의 이자표(Matured Bond Coupons)의 회계상 분류 및 자산 처리 원칙으로 옳은 것은?",
        "options": [
            "① 아직 대금이 예금 통장에 입입되지 않았으므로 이자수익 미수채권으로 기재한다.",
            "② 금융기관에 제시하여 즉시 현금화할 수 있는 통화대용증권에 속하므로 현금및현금성자산에 포함한다.",
            "③ 사채 발행사의 자산이므로 투자채무상품 장부액에 직접 가산하여 결산한다.",
            "④ 기말 결산일 현재 사채의 시가를 재평가하여 OCI 자본 잔액으로 누적 적립한다.",
            "⑤ 이자표는 인쇄된 종이에 불과하여 결제가 진행될 때까지는 자산성을 원천 부인한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 지급일(만기일)이 도래한 공사채의 이자표는 소지자가 금융기관에 청구하면 즉시 현금으로 현장 교환해 주므로, 현금과 가치가 동일한 통화대용증권에 해당하여 기말에 현금및현금성자산으로 계상합니다.\n\n[오답 해설]\n① 이자 미수 상태라 하더라도 만기가 이미 도래하여 즉시 교환이 가능하므로 단순 미수금 채권으로 놔두지 않고 현금화 기재를 실행합니다.\n③, ④ 채권 장부액 직접 가산이나 OCI 평가는 기준서 위반입니다.\n⑤ 이자표의 정당한 자산 가치 및 환금성을 전면 부정하는 틀린 기술입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "은행계정조정표를 작성하기 위해 양측 예금 원장을 대조하던 중, 은행에서는 회사가 입금한 자기앞수표 ₩50,000을 정상적으로 입금 처리하였으나, 회사 장부에는 이 입금 분개 전체가 기입 누락된 사실을 확인했다. 이 차이 항목의 조정 성격과 올바른 해결 방식으로 옳은 것은?",
        "options": [
            "① 은행 측에서 기입 실수를 한 것이므로 은행 장부 잔액에서 ₩50,000을 차감(-) 조정한다.",
            "② 회사가 장부 기록을 누락한 회사 측 누락 오류이므로, 회사 장부 당좌예금 잔액에 ₩50,000을 가산(+)하고 적절한 수정 분개를 실행한다.",
            "③ 은행 장부에만 잔액이 증액 유지되면 정당하므로 회사는 조정할 필요가 없다.",
            "④ 당좌차월 마이너스 이자를 소멸시키는 오류이므로 유동부채를 늘리는 수정을 수행한다.",
            "⑤ 수표는 회사의 현금성자산 요건을 충족하지 못하므로 양쪽 장부에서 모두 ₩50,000을 제거하는 소멸 분개를 한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 은행은 올바르게 처리했으나 회사의 기장 누락이 원인이므로 '회사측 조정사항'입니다. 회사 장부 당좌예금 잔액에 ₩50,000을 더해 주는(+) 수정을 실행해야 정상 잔액을 도출할 수 있습니다.\n\n[오답 해설]\n① 은행에는 오류가 없으므로 은행 측 잔액을 깎으면 불일치가 왜곡됩니다.\n③ 수정하지 않고 방치하면 기말 시점의 현금 자산 정보가 왜곡 공시되므로 불가합니다.\n④, ⑤ 당좌차월이자 제거 요건이나 수표 무효화 주장은 복식부기 및 현금 기준에 어긋납니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "은행계정조정표의 회사측 조정사항 중 '미통지 출금(Unnotified Withdrawals)'에 해당하는 거래 유형으로 옳지 않은 것은?",
        "options": [
            "① 기중에 은행이 징수한 당좌예금 계좌 이체 수수료 ₩500이 당좌통장에서 출금되었으나 회사가 전표 처리를 하지 않은 항목",
            "② 기업이 은행에 제시하여 예입했던 타인 발행 당좌수표가 발행자의 자금 부족으로 부도 처리되어 예금에서 감액 처리되었으나 회사가 아직 부도 소식을 받지 못한 항목",
            "③ 은행이 회사 당좌차월 한도액 대여에 대하여 계상한 대출이자 ₩2,000이 예금에서 자동 인출되었으나 회사 장부에 기입되지 않은 항목",
            "④ 거래처가 회사에 보낼 물품 대금 ₩50,000을 회사의 예금 통장으로 송금 입금하였으나 회사의 정산 담당자가 이 사실을 통지받지 못한 항목",
            "⑤ 회사가 보유 예금을 자사 지점 은행 간에 이체 조정하며 인출 수수료가 선차감되어 빠져나갔으나 회사가 누락한 금액"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 거래처가 회사 통장으로 대금을 직접 송금한 거래는 회사 당좌예금의 잔액을 '증가'시키는 거래이므로, 미통지 출금이 아니라 '미통지 입금(회사 가산 사항)'에 해당합니다.\n\n[오답 해설]\n①, ⑤ 은행 계좌 수수료 누락 출금은 회사 예금을 차감해야 하는 미통지 출금입니다.\n② 수표 부도 통지 누락은 대금을 취소(차감)해야 하는 미통지 출금입니다.\n③ 차월 대출이자 자동 인출 또한 예금액을 깎아내는 미통지 출금 사항입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "㈜A는 거래처에 외상매입금 ₩1,200을 상환하기 위해 당좌수표를 발행 및 교부하고, 장부에는 ₩2,100을 지급한 것으로 오기입(과대 기록)하였다. 은행은 이 수표 제시 시점에 올바른 금액인 ₩1,200을 정상 출금하였다. 기말 은행계정조정 시 이 거래를 올바른 예금 잔액으로 복원하기 위한 회사 장부의 조정 분개 방향으로 옳은 것은?",
        "options": [
            "① 회사 당좌예금 장부 잔액을 ₩900만큼 감소(-) 조정한다.",
            "② 회사 당좌예금 장부 잔액을 ₩900만큼 가산(+) 조정한다.",
            "③ 은행 장부 잔액을 ₩900만큼 가산(+) 조정한다.",
            "④ 회사 장부에서 자산과 부채를 동시에 ₩1,200씩 감소 소멸시킨다.",
            "⑤ 은행 장부 잔액에서 ₩900만큼 차감(-) 조정한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 회사는 ₩1,200만 줄여야 하는 예금 장부를 ₩2,100만큼 줄여서 오기입했습니다. 즉, 예금을 ₩900만큼 더 과다하게 깎아 장부에 기록한 상태입니다. 따라서 정상 예금 잔액으로 돌려놓기 위해서는 차액인 ₩900만큼 회사 예금 잔액을 다시 가산(+)해 주는 복원 수정을 거쳐야 합니다.\n- 수정 분개: (차) 당좌예금 900 / (대) 외상매입금 900\n\n[오답 해설]\n① ₩900을 추가 감소시키면 장부 상의 예금 과다 차감 오류가 ₩1,800으로 오히려 배가됩니다.\n③, ⑤ 은행 측 장부는 ₩1,200을 적정하게 출금 처리했으므로 은행 잔액을 건드리면 안 됩니다.\n④ 이미 ₩2,100으로 오분개된 전체 거래를 단순 ₩1,200 넷팅으로 소멸시키면 오류가 남습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "은행계정조정표 상의 '회사 기입오류(Company Errors)'와 '은행 기입오류(Bank Errors)'를 정정할 때의 기본 원칙으로 가장 올바른 진술은?",
        "options": [
            "① 모든 기장 오류는 거래 잔액의 크기와 관계없이 무조건 은행 측 원장에서 가산 조정하여 합산 통제한다.",
            "② 기입 오류가 발생한 경우, 오류를 범한 주체(회사 또는 은행)의 장부 잔액에만 해당 오류 금액의 정정분을 가감 조정한다.",
            "③ 회사의 오류는 회사가 기재하되, 은행의 오류도 은행 대신 회사의 자본 항목에서 먼저 차감한 뒤 감사인의 지도를 받는다.",
            "④ 오류 정정 시에는 당좌예금의 최초 개설 시점 금리 조건을 소급 조정하여 이자율 변동 손실을 계상한다.",
            "⑤ 오류 수정 분개는 당기 중 발생한 것이라도 결산 종료 후 다음 연도 첫날에만 분개해야 한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 기입 오류의 정정 원칙은 오류를 발생시킨 주체의 장부 잔액을 정정하는 것입니다. 회사가 실수하여 장부를 오기했다면 회사 장부 잔액을 가감하고, 은행이 실수하여 통장 잔고를 다르게 기입했다면 은행 잔액 측면에 가감 조정을 가합니다.\n\n[오답 해설]\n① 모든 오류를 은행 측 장부에서만 정정하면 회사 장부의 오기가 영구 방치되므로 틀렸습니다.\n③ 은행의 과실을 회사 자본에서 직접 차감 정산하는 회계처리는 존재하지 않습니다.\n④ 이자율 소급 조정과는 아무런 개연성이 없습니다.\n⑤ 당기 결산 보고의 정합성을 위해 연도 말 결산 분개 시점에 오류 수정 분개를 필히 이행해야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "K-IFRS에 따라 '현금및현금성자산'에 대하여 주석(Disclosures) 공시 사항을 작성할 때, 기업이 의무적으로 밝혀야 하는 사항에 해당하는 것은?",
        "options": [
            "① 기업이 보유한 자산 중 사용이나 인출이 법적·계약상 제약으로 제한되어 있는 '사용제한 현금및현금성자산'의 금액 및 내용",
            "② 기중에 발행했던 모든 당좌수표의 수표번호 및 소지자의 개인 인적 사항 리스트",
            "③ 보유 중인 통화대용증권의 지폐 일련번호 및 주화의 발행 연도별 개수 명세",
            "④ 금융자산을 보관하고 있는 시중 은행 지점장들의 신용 등급 및 대출 승인 평정 결과",
            "⑤ 현금성자산의 이자율 변동에 따른 피투자회사의 자본금 유출입 발생 가상 확률표"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1007호 문단 48에 따라, 기업은 종속기업이나 지점 등이 보유하고 있는 유의적인 현금및현금성자산 잔액 중 외환 규제나 법적 제한 등으로 인하여 그룹 전체가 사용할 수 없는 사용제한 금액과 그 내용을 반드시 주석으로 공시하여야 합니다.\n\n[오답 해설]\n② 수표 소지자 인적 정보나 ③ 일련번호 및 주화 연도별 명세 등은 기업 비밀 유출 위험 및 회계 정보 유용성이 전혀 없는 비정상적 주석 사항입니다.\n④ 은행장 신용 등급이나 ⑤ 가상 확률표 등은 공시 의무 조항과 하등 관계가 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s02-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "㈜감평의 회계담당자는 기말에 당좌예금 통장 잔액을 확인하던 중, 은행에서는 타인이 발행한 수표 ₩10,000을 ㈜감평의 계좌에 착오로 '이중 입금(Double Deposit)' 처리하여 통장 잔고를 과대 계상해 준 사실을 인지했다. 이 차이 항목의 올바른 은행계정조정표 상 반영 방법은?",
        "options": [
            "① 은행 측의 오류이므로, 은행 측 장부 잔액에서 ₩10,000을 차감(-) 조정한다.",
            "② 회사 측 장부 당좌예금 계정에 ₩10,000을 가산(+)하는 수정 분개를 실행한다.",
            "③ 은행이 돈을 더 넣어 준 것이므로 회사 측 장부에 '잡이익 ₩10,000'을 대변 분개한다.",
            "④ 양쪽 장부에 아무런 조정을 하지 않고 은행이 정정할 때까지 예금을 차단해 둔다.",
            "⑤ 회사의 당좌차월 한도액에서 ₩10,000을 차감하는 수정 분개를 한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 은행의 기장 실수로 인해 통장 잔고가 실제보다 ₩10,000 과다하게 기록된 상태입니다. 이는 은행 측의 오류이므로 조정표의 '은행 측 장부 잔액'에서 ₩10,000을 차감(-) 조정하여 조정 후 올바른 잔액을 일치시켜야 합니다.\n\n[오답 해설]\n②, ③ 회사는 장부를 정상적으로 기입했으므로 회사 측 장부나 잡이익을 건드려 장부를 인위적으로 왜곡하면 안 됩니다.\n④ 조정표를 통한 검증 과정을 생략하면 기말 자산액 검증에 실패합니다.\n⑤ 당좌차월 부채의 수정 사항이 아닙니다.",
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

print(f"Successfully added {len(new_questions)} questions. Total questions in database: {len(questions)}")
