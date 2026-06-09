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
    "chapter": "제4장 자본",
    "section": "Chapter 10 자본",
    "item": "3절 주식의 발행"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q2551 ~ Q2560) ---
    {
        "id": "practice-accounting-ch10s03-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "주식의 발행과 관련된 다음 설명 중 가장 기초적인 개념으로 올바르지 않은 것은?",
        "options": [
            "① 주식을 액면금액보다 높은 가격으로 발행하는 거래를 할증발행이라고 한다.",
            "② 주식을 액면금액보다 낮은 가격으로 발행하는 거래를 할인발행이라고 한다.",
            "③ 주식을 액면금액과 동일한 가격으로 발행하는 거래를 액면발행이라고 한다.",
            "④ 주식을 발행할 때 액면금액을 초과하여 입금된 금액은 당기 영업수익으로 즉시 인식한다.",
            "⑤ 주식의 할인발행 시 액면금액과 발행금액의 차액은 주식할인발행차금으로 계상한다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 주식 발행 시 액면금액을 초과하여 입금된 금액은 주주와의 자본거래에서 발생한 잉여금인 '주식발행초과금(자본잉여금)'으로 처리하며, 당기순이익에 영향을 미치는 영업수익으로 인식할 수 없습니다.\n\n[오답 해설]\n① 할증발행의 기초 정의입니다.\n② 할인발행의 기초 정의입니다.\n③ 액면발행의 기초 정의입니다.\n⑤ 할인발행 시 발생하는 대차 차액은 자본조정 차감 항목인 주식할인발행차금으로 기록됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "다음 중 주식을 발행하는 과정에서 직접적으로 발생하는 '신주발행비'의 일반적인 범위에 포함되지 않는 것은?",
        "options": [
            "① 주권 인쇄비와 등록세",
            "② 금융기관의 주식 청약 수수료 및 인수 수수료",
            "③ 신주 발행을 위한 법률 자문 비용 및 광고비",
            "④ 신주 발행일 이후에 발생한 주주총회 개최 비용 및 통상적인 IR 광고비",
            "⑤ 증자 등기를 위한 등록면허세 및 법무사 대행 수수료"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 신주발행비는 신주 발행 거래에 '직접 관련하여 직접 유발된 비용'만을 의미합니다. 신주 발행 완료 시점(발행일) 이후에 발생하는 일상적인 주주총회 비용, IR 비용, 광고 선전비 등은 당기 판매비와관리비 또는 영업외비용으로 처리하며 신주발행비에 포함하지 않습니다.\n\n[오답 해설]\n① 주권 인쇄와 등록세는 전형적인 신주발행비에 해당합니다.\n② 주식 청약 및 인수와 직접 연동된 수수료는 신주발행비에 가산됩니다.\n③ 발행 결정을 위해 유발된 전문직 자문료 및 광고비 역시 자본 직접 차감 요소입니다.\n⑤ 자본금 증자 법적 등기를 위한 세무 비용과 법무 대행 수수료도 직접 거래 원가에 포함됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "다음 중 주식 발행 시 대변에 기록되는 '자본금'에 대한 K-IFRS 상의 측정 기준으로 옳은 것은?",
        "options": [
            "① 발행 주식 수에 발행 시점의 주당 시가(공정가치)를 곱한 가액",
            "② 발행 주식 수에 주당 액면가액을 곱한 액면총액",
            "③ 주식 발행으로 인입된 순현금 수입액",
            "④ 발행 주식 수에 주당 장부가액을 곱한 장부총액",
            "⑤ 발행주식의 액면가에서 신주발행비를 직접 차감한 잔액"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 상 법정자본금 제도를 따르는 주식발행 회사는 주식 발행 시 무조건 발행주식 수에 액면금액(액면가액)을 곱한 금액을 '자본금'으로 대변에 계상하여야 합니다. 발행가액이나 발행 수수료 등은 자본금 가액에 직접 가감하지 않고 주발초나 주할차 등 별도 자본 항목을 통해 조정합니다.\n\n[오답 해설]\n① 시가를 곱한 금액은 총 유입 가치이며, 이를 초과하는 금액은 주식발행초과금이 됩니다.\n③ 순현금 수입액은 자본총계 증가액에 가깝습니다.\n④ 자본금은 액면가 기준이므로 장부가 기준 측정 설명은 잘못되었습니다.\n⑤ 신주발행비는 자본금이 아닌 주발초/주할차 등에서 차감합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "현물출자(Non-cash Contribution)에 대한 다음 설명 중 가장 기초적인 개념으로 옳은 것은?",
        "options": [
            "① 현금을 출자받아 주식을 발행하는 일반적인 유상증자 거래를 말한다.",
            "② 토지나 건물, 특허권 등 현금 이외의 비화폐성 자산을 제공받고 그 대가로 주식을 발행하는 자본 거래이다.",
            "③ 주식 발행 시 취득하는 자산의 장부금액만을 전액 자본금으로 기재하는 자본 거래이다.",
            "④ 현물출자는 자산 취득 거래이므로 자본 변동이 전혀 수반되지 않는다.",
            "⑤ 현물출자 거래의 차변은 항상 영업비용 계정으로 처리한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 현물출자는 회사가 현금 대신 유형/무형자산 등 비화폐성 자산을 출자받으면서 그 보상 대가로 신주를 발행해 주는 자본 조달 거래의 전형적인 기초 개념입니다.\n\n[오답 해설]\n① 현금을 수취하는 증자는 일반 유상증자입니다.\n③ 장부금액이 아닌 취득 자산의 공정가치 기준으로 자산원가를 계상하는 것이 원칙입니다.\n④ 자산 유입과 동시에 주식이 발행되므로 회사의 자본총계가 직접 증가합니다.\n⑤ 차변에는 유입되는 유형자산, 무형자산 등 자산 계정이 기록됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "출자전환(Debt-for-Equity Swap)의 기초적인 개념에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 회사가 주식을 매입하여 소각하는 감자 거래를 말한다.",
            "② 금융기관이나 거래처 등 채권자에게 진 부채(채무)를 상환하는 대신, 채권자에게 회사 신주를 발행하여 교부함으로써 채무를 자본으로 대체하는 거래이다.",
            "③ 기존 보통주 주식을 우선주로 일방 대체하여 재배부하는 소유주간 계약이다.",
            "④ 부채가 줄어들고 동일한 금액만큼 자산이 늘어나는 재무 거래이다.",
            "⑤ 회사의 자본금이 일시적으로 감소하는 감자 유발 요인이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 출자전환이란 기업이 차입금이나 사채 등의 금융부채를 상환할 현금이 부족할 때, 부채 채권자에게 채권 상환 액수만큼 회사의 주식을 새로 발행하여 인도함으로써 부채를 상멸시키고 자본(자본금 및 주발초)으로 대체하는 구조조정 거래를 뜻합니다.\n\n[오답 해설]\n① 감자는 자본금을 줄여 주주에게 돈을 돌려주는 거래로 출자전환이 아닙니다.\n③ 보통주와 우선주의 단순 대체는 출자전환이 아니라 주식의 전환입니다.\n④ 부채가 감소하고 대변에 자본(자본금 등)이 가산되어 증가하므로 자산이 증가하는 거래가 아닙니다.\n⑤ 주식 발행을 수반하므로 자본금이 물리적으로 증가합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "보통주와 우선주를 동시에 하나의 일괄 대가로 발행하는 '일괄발행' 거래에 관한 다음 설명 중 가장 기초적인 것으로 옳은 것은?",
        "options": [
            "① 두 종류의 주식을 공정가치와 관계없이 액면금액 비율로만 반드시 배분해야 한다.",
            "② 한 번의 거래 계약을 통해 2종 이상의 서로 다른 주식을 일괄적으로 청약받아 발행하는 거래이다.",
            "③ 보통주와 우선주는 자본금이 동일하므로 금액을 구분 기재할 필요가 없다.",
            "④ 일괄 대금을 수령하면 자본금 대신 '일괄발행잉여금' 계정으로 통합 보고한다.",
            "⑤ 주주 총액 비례로 이익잉여금 처분 결의를 병행하여야 한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 일괄발행은 보통주와 우선주, 혹은 보통주와 사채처럼 성격이 다른 2가지 이상의 금융상품을 묶어서 단일 대금(Lump-sum)을 받고 발행하는 거래의 정의입니다.\n\n[오답 해설]\n① 원칙적으로 상대적 공정가치법에 의한 비례 배분을 우선 적용합니다.\n③ 자본금은 발행 주식별 액면가로 명확히 분리하여 장부에 기재하여야 합니다.\n④ 일괄발행잉여금이라는 통합 임시 계정은 K-IFRS 상 인정되지 않으며 최종 배분액을 개별 자본 항목으로 보고해야 합니다.\n⑤ 이 거래는 이익잉여금 처분 거래가 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "청약에 의한 주식발행 절차에서, 청약 시점에 청약자로부터 수령하는 '신주청약증거금'에 대한 회계상 성격 분류로 가장 올바른 것은?",
        "options": [
            "① 유동부채",
            "② 자본잉여금",
            "③ 자본조정 (가산 항목)",
            "④ 기타포괄손익누계액",
            "⑤ 영업수익"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 신주청약증거금은 청약자가 청약 시점에 납입한 금액으로, 납입 기일에 정식 자본금으로 전입되기 전까지 임시로 계상하는 성격을 가집니다. 이는 주주가 될 자들로부터 수취한 소유주 자본 성격이므로 부채가 아니며, 아직 주식이 발행되지 않았으므로 자본조정의 가산(+) 항목으로 분류합니다.\n\n[오답 해설]\n① 법적 청약 대금 환불 의무가 일반적인 상황이 아니므로 금융부채(유동부채)가 아닙니다.\n②, ④, ⑤ 정식 주식 배부 완료 및 대체 전까지는 자본잉여금, AOCI, 당기수익 등으로 인식할 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "일반적으로 종류주식 중 '보통주'와 대비하여 발행되는 '우선주(Preferred Shares)'의 가장 기본적인 특징에 대한 설명으로 옳은 것은?",
        "options": [
            "① 보통주에 비해 항상 의결권이 강하게 부여되어 회사 지배력이 높은 주식이다.",
            "② 회사가 이익배당이나 청산 시 잔여재산 분배에 있어 보통주 주주보다 우선적으로 배분받을 권리를 가질 수 있는 주식이다.",
            "③ 액면금액이 보통주에 비해 항상 무조건 2배 이상 높게 설정되어 보고되는 법정 주식이다.",
            "④ 우선주는 무조건 자본이 아닌 부채로만 재무제표에 최초 인식되는 것이 원칙이다.",
            "⑤ 발행주식의 만기가 1년 이내로 고정되어 영구적 보유가 차단된 주식이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우선주는 보통주에 대비되는 대표 종류주식으로서, 주주총회 의결권이 제한되거나 없는 대신 이익배당 배분율이나 회사 해산 청산 시 잔여재산의 회수 분배에 보통주 주주보다 선행하여 우선적인 분배 권리를 가지는 특징을 가집니다.\n\n[오답 해설]\n① 의결권이 배제되는 경우가 대다수이므로 지배력은 보통주보다 낮습니다.\n③ 액면가는 회사 정관으로 결정하므로 우선주라고 액면가가 더 크거나 규제 한도가 정해진 것은 아닙니다.\n④ 상환우선주 중 일부 조건에 한해서만 금융부채로 분류되며 기본 우선주는 자본 분류가 원칙입니다.\n⑤ 만기가 없는 영구 우선주도 다수 존재합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "회사가 신주를 유상 발행하여 증자를 완료했을 때, 당해 거래가 회사 재무제표에 미치는 기본적인 효과로 가장 옳은 것은?",
        "options": [
            "① 자산총계와 자본총계가 동시에 증가한다.",
            "② 부채총계와 자본총계가 동시에 증가한다.",
            "③ 자본금은 증가하지만 자본총계는 전혀 변하지 않는다.",
            "④ 자산은 늘어나지만 부채도 동액만큼 늘어나 순자산은 불변이다.",
            "⑤ 이익잉여금이 즉각적으로 대폭 증가하게 된다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 유상증자를 통해 현금 등 자산이 회사로 유입(차변: 현금)되고, 대가로 주식이 발행되어 대변에 자본금 및 주발초(자본)가 증가하므로 자산총계와 자본총계가 완벽히 비례적으로 동시에 증가합니다.\n\n[오답 해설]\n② 유상증자는 부채를 증가시키지 않습니다.\n③ 무상증자나 주식배당은 자본총계가 불변이지만 유상증자는 외부 자금이 신규 유입되므로 자본총계가 증가합니다.\n④ 부채 증가는 유발되지 않습니다.\n⑤ 자본 유입액은 자본잉여금 등으로 가므로 이익잉여금에 직접적인 증가 효과는 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "우리나라 상법 상 허용되는 '무액면주식(No-par value stock)'을 신규 발행하여 자본을 확충할 때, 회사 대변에 계상할 법정 '자본금' 가액의 일반적인 결정 기준은?",
        "options": [
            "① 무액면주식이므로 자본금 계정은 사용하지 않고 전액 주식발행초과금으로 계상한다.",
            "② 주식 발행가액의 최소 50% 이상을 자본금으로 계상하고, 남은 차액을 주식발행초과금으로 적는다.",
            "③ 발행 당일의 주당 시가 전액을 자본금으로 보고한다.",
            "④ 이사회가 자본금으로 적지 않기로 결의한 금액만 자본금으로 적는다.",
            "⑤ 회사의 누적 당기순이익에 비례하여 정부가 직접 지정해 준다."
        ],
        "answer": "2",
        "options": [
            "① 무액면주식의 발행 시 자본금 계정은 일절 기재할 수 없으며 전액 주식발행초과금으로 처리한다.",
            "② 상법 상 주식 발행가액의 2분의 1(50%) 이상의 금액으로서 이사회(또는 주주총회)에서 자본금으로 계상하기로 정한 금액을 자본금으로 계상한다.",
            "③ 발행 당일의 자산 평가 가액 전액을 무조건 법정자본금으로 기재한다.",
            "④ 액면주식의 규정을 준용하므로 임의적 액면가 ₩5,000을 자본금으로 강제 고정한다.",
            "⑤ 자본금 없이 오직 이익잉여금에 직접 누적 적립하여 보고한다."
        ],
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 액면가가 없는 무액면주식을 발행할 때 대변 자본금에 적을 가액은 상법 상 발행가액의 2분의 1(50%) 이상의 금액 범위 내에서 회사가 자본금으로 계상하기로 지정 결의한 가액이 되며, 자본금으로 계상하지 않은 남은 2분의 1 이하의 발행가액 부분은 주식발행초과금으로 계상합니다.\n\n[오답 해설]\n① 자본금은 상법상 의무적으로 설정해야 하므로 ₩0 처리는 불가능합니다.\n③, ④, ⑤는 상법 및 자본 회계 기준에 맞지 않는 임의 서술입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },

    # --- L2 (이해): 15문항 (Q2561 ~ Q2575) ---
    {
        "id": "practice-accounting-ch10s03-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "K-IFRS 상 신주 발행 시 지출된 '신주발행비'의 회계처리 원칙으로 가장 옳은 것은?",
        "options": [
            "① 전액 당기비용인 '수수료비용(판관비)' 또는 '영업외비용'으로 즉시 인식한다.",
            "② 무형자산의 '창업비' 또는 '개발비' 과목으로 계상한 후 5년간 정액 상각비용화한다.",
            "③ 주식의 발행가액에서 직접 차감하므로, 할증발행 시에는 주식발행초과금을 차감하고 할인발행 시에는 주식할인발행차금에 가산한다.",
            "④ 자산 항목의 '이연자산'으로 보고한 후 미래 유효이자율법으로 상각한다.",
            "⑤ 보통주 발행비는 자본조정에서 빼고, 우선주 발행비는 부채의 누적 금융비용에 가산한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 기준 상 주식 발행과 직접 연관되어 발생한 원가(신주발행비)는 손익계산서 상의 비용으로 인식하는 것이 엄격히 차단되며, 주식발행 대금(유입가액)에서 직접 공제하는 형식의 자본조정 처리를 수행합니다. 이에 따라 할증발행으로 주식발행초과금이 생성되었을 때 이를 차감하며, 할인발행으로 주식할인발행차금이 생성되었을 때 이를 누적 가산합니다.\n\n[오답 해설]\n① 당기 비용 처리는 K-IFRS 상 금지됩니다.\n②, ④ 창업비나 무형자산과 같은 이연 자산화 계상은 불가능합니다.\n⑤ 우선주가 부채 성격인 경우를 제외한 자본인 경우에는 모두 동일하게 발행가액에서 차산합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "주식의 할인발행 및 신주발행비 거래 연동과 관련된 다음 설명 중 가장 옳은 이해는?",
        "options": [
            "① 할인발행 시 발생하는 신주발행비는 당기 비용으로 계상하여 할인발행차금을 감소시킨다.",
            "② 신주발행비의 발생은 할인발행 시 최종 기말 '자본조정' 차감 잔액을 증가시키는 결과를 낳는다.",
            "③ 신주발행비는 발행가액의 공제 요소이므로 자본금 계정에서 직접 액면금액을 줄여 마이너스 기재한다.",
            "④ 주식할인발행차금은 자본잉여금으로 직접 우회 상계되어 소멸하므로 신주발행비와 연동되지 않는다.",
            "⑤ 발행 수수료가 아무리 크게 발생하더라도 주식할인발행차금 원장에 추가 합산되는 것은 불가능하다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 할인발행 시 신주발행비는 발행가액을 깎아내려 주주로부터 납입받은 순가치를 줄입니다. 이는 대차 차액인 주식할인발행차금(자본조정 차감 과목) 잔액을 추가로 증가시켜 기말 자본 차감폭(자본조정 차감 총액)을 늘리는 역할을 수행하게 됩니다.\n\n[오답 해설]\n① 당기 비용 계상이 아니며 할인발행차금을 늘립니다(차감폭 확대).\n③ 자본금 액면가는 변경될 수 없습니다.\n④ 주식할인발행차금 원장에 가산되므로 신주발행비와 밀접하게 연동됩니다.\n⑤ 발행비는 전액 차금에 합산되도록 규정되어 있습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "신주를 할증발행하면서 대량의 신주발행비가 납입 대금에서 공제 수납되었을 때, 이 거래가 기말 재무상태표의 '자본잉여금'에 미치는 누적 효과에 대한 올바른 서술은?",
        "options": [
            "① 자본잉여금 중 주식발행초과금의 최종 보고 잔액을 감소시키는 효과를 가진다.",
            "② 자본잉여금을 감소시키는 대신 자본조정의 가산 과목을 생성한다.",
            "③ 신주발행비는 영업외비용으로 계상되므로 자본잉여금 총량에는 어떠한 변화도 없다.",
            "④ 법인세 절감 효과가 발생하므로 주식발행초과금은 오히려 증가하게 된다.",
            "⑤ 주식발행초과금 잔액을 음수(-)로 변환하여 자본조정으로 분류를 강제 이전시킨다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 할증발행 시 신주발행비는 [차변: 주식발행초과금 XXX / 대변: 현금(지출액) XXX] 의 형식으로 분개되어 주식발행초과금(자본잉여금) 잔액을 직접 줄이는 누적 결과를 미치게 됩니다.\n\n[오답 해설]\n② 자본조정 가산이 아닌 자본잉여금(주발초)의 직접 차감 처리를 행합니다.\n③ 당기 손익 비용이 아닌 자본에서 직접 공제되므로 자본잉여금이 명백히 줄어듭니다.\n④ 법인세 배분이 연동되더라도 세후 효과가 차감되므로 주발초가 순증가하는 것은 불가능합니다.\n⑤ 주발초가 초과하여 차감되어 음수가 되더라도 이는 주식할인발행차금(자본조정) 잔액으로 잡힐 뿐 주발초 원장이 음수가 되지는 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "K-IFRS 상 유형자산 등을 출자받고 신주를 발행하는 '현물출자' 거래에서, 취득 자산의 최초 취득원가(장부금액)를 책정하는 일반적인 원칙적 측정 기준은?",
        "options": [
            "① 출자하는 거래처 장부에 기재되어 있던 종전 역사적 원가",
            "② 제공받은 현물자산의 취득일 공정가치(Fair Value)",
            "③ 발행해 준 주식의 총 액면가액",
            "④ 취득 자산의 미래 현금흐름을 최초 세후 할인율로 할인한 기대 장부가",
            "⑤ 자산의 지방세 시가표준액 등 공인 정부 고시 가격"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 기준 상 현물출자로 취득하는 유형자산이나 무형자산 등의 비화폐성 자산은 '제공받은 자산의 공정가치(Fair Value)'를 원칙적인 최초 취득 원가로 보아 장부에 등재합니다.\n\n[오답 해설]\n① 상대방 거래처의 장부가액은 유용한 장부정보가 될 수 없습니다.\n③ 주식의 액면가액은 법정 자본금의 표기 단위일 뿐 자산의 취득 가치와는 연동되지 않습니다.\n④ 미래 현금흐름 할인은 측정 신뢰성 수준이 상대적으로 떨어져 1순위 적용 대상이 아닙니다.\n⑤ 정부 고시 가격은 원칙적 시가(공정가치) 정의와 다릅니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "K-IFRS 상 현물출자 거래 시, 제공받은 자산(건물, 토지 등)의 공정가치를 전혀 신뢰성 있게 측정할 수 없는 특수한 예외적인 상황에서 적용하는 차순위 취득 자산 측정액의 결정 방식은?",
        "options": [
            "① 그 대신 회사가 대가로 발행하여 인도한 '지분상품(주식)의 공정가치'를 기준으로 자산원가를 측정한다.",
            "② 신뢰성 측정이 불가능하므로 자산 취득원가는 무조건 액면가 ₩0으로 기록한다.",
            "③ 발행한 주식의 액면가 총액을 그대로 자산 취득금액으로 계상한다.",
            "④ 세무 상 기준시가를 강제 원가로 변환하여 적는다.",
            "⑤ 자산 기재를 포기하고 자본잉여금으로만 수취액을 인식한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 현물출자 거래의 우선측정 순위 설명입니다. 제공받은 자산의 공정가치를 신뢰성 있게 측정하기 어려운 예외적인 시나리오 하에서는, 대가로 교부한 지분상품(회사 주식)의 공정가치(시가)를 측정하여 이 금액을 취득 자산의 최초 취득원가로 계상합니다.\n\n[오답 해설]\n② 자산유입이 분명하므로 ₩0 처리는 불가합니다.\n③ 액면가 기준 측정은 최후순위로도 사용하지 않습니다.\n④ 세무상 기준시가는 예외 기준에 속하지 않습니다.\n⑤ 차변에 취득 자산의 기재는 회계 의무입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "K-IFRS 해석서 제2119호 '지분상품의 발행을 통한 금융부채의 소멸(출자전환)'에 따른 회계상 소멸 부채 상환 측정의 대원칙(1순위 기준)으로 옳은 것은?",
        "options": [
            "① 소멸될 금융부채의 최종 역사적 취득가액",
            "② 금융부채 소멸 대가로 발행하여 제공하는 '지분상품의 공정가치'",
            "③ 소멸되는 금융부채의 장부금액 전액",
            "④ 발행되는 신주의 액면금액 총액",
            "⑤ 회사의 잔여 자본총계의 분배 지분액"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 출자전환 해석서(제2119호)에 따르면, 금융부채를 변제 또는 소멸시키기 위해 발행된 지분상품의 공정가치를 신뢰성 있게 측정할 수 있다면, 그 '발행 지분상품의 공정가치'를 소멸 부채의 상환 및 지분 대가 대변 계상 원가로 측정하는 것을 제1순위 원칙으로 규정하고 있습니다.\n\n[오답 해설]\n① 역사적 취득가액은 상환 시점의 측정치가 될 수 없습니다.\n③ 장부금액은 채무조정손익을 도출하기 위한 대조 기준일 뿐 소멸 상환액의 최초 측정치가 아닙니다.\n④ 액면가액은 측정 기준에서 제외됩니다.\n⑤ 소유주의 분배 지분액과는 무관합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "K-IFRS 해석서 제2119호에 의거하여 출자전환 거래를 분개 처리할 때, 소멸되는 금융부채의 장부금액과 최초 계상될 발행 지분상품의 공정가치(또는 소멸 부채의 공정가치) 간에 발생한 대차 차액의 후속 결산 마감 처리로 가장 올바른 것은?",
        "options": [
            "① 자본조정의 '주식할인발행차금' 계정에 상계 없이 가산한다.",
            "② 자본잉여금에 직접 '출자전환잉여금' 과목으로 계상하여 유보한다.",
            "③ 당기 손익계산서 상의 '채무조정이익' 또는 '채무조정손실'로 하여 당기순이익에 즉시 반영한다.",
            "④ 기타포괄손익누계액(AOCI)에 분류한 후 사후 재분류 조정을 준비한다.",
            "⑤ 차액은 없는 것으로 간주하고 발행 지분상품 금액을 금융부채 장부금액과 강제로 일치시켜 기재한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 출자전환 시 소멸 부채의 장부가와 지분상품 공정가치(상환 측정액)의 차이는 회사 채무가 탕감되거나 조정되면서 실현된 손익 성격이므로, 자본잉여금이 아니라 당기순이익 상의 '채무조정이익(또는 손실)'으로 분류하여 당기 손익에 즉시 반영하여야 합니다.\n\n[오답 해설]\n① 주할차 자본 항목으로 우회할 수 없습니다.\n② 자본잉여금 귀속 항목이 아닌 당기 영업외손익 항목입니다.\n④ 미실현 OCI가 아닌 실현 당기 손익입니다.\n⑤ 차액을 인식하지 않고 임의 조정을 가하는 분개는 기준서 위반입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "출자전환(Debt-for-Equity Swap) 거래 시, 신규로 발행하여 인도한 회사 지분상품의 공정가치를 전혀 신뢰성 있게 측정할 수 없는 경우에 채무 상환 가치 측정을 위해 예외적으로 사용하는 차선책(2순위 기준)은?",
        "options": [
            "① 소멸되는 해당 '금융부채의 공정가치'를 기준으로 지분상품의 가치를 대리 측정한다.",
            "② 차선책이 없으므로 채무조정이익을 무조건 ₩0으로 가정 처리한다.",
            "③ 주식의 액면금액을 상환 측정액으로 강제 고정한다.",
            "④ 국세청 상속세및증여세법 상 주식 평가액을 우선한다.",
            "⑤ 거래처가 주장하는 채권 회수 희망 금액을 적는다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 해석서 제2119호 상의 예외적 2순위 측정 지침입니다. 발행 지분상품의 공정가치를 신뢰성 있게 추정하기 곤란할 경우에는 소멸 제거 대상이 되는 '금융부채 자체의 공정가치(재평가 시가)'를 기준으로 소멸액을 책정해 기록합니다.\n\n[오답 해설]\n② 채무조정이익 산정을 보류하거나 무시할 수 없습니다.\n③ 액면가액은 금융부채의 상환 가치나 시가를 대리할 수 없습니다.\n④, ⑤는 회계 기준 상 인정되지 않는 임의 평가 기준입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "보통주와 우선주를 동일 대가로 '일괄발행'할 때, 개별 주식의 공정가치가 명확히 확인되어 이를 비례하여 일괄발행금액을 나누어 배분하는 회계 기법의 정식 명칭은?",
        "options": [
            "① 잔여가치법 (Residual Value Method)",
            "② 상대적 공정가치비율 배분법 (Relative Fair Value Method)",
            "③ 액면가 비율 배분법 (Par Value Allocation Method)",
            "④ 장부가 비율 배분법 (Book Value Allocation Method)",
            "⑤ 역사적원가 비례 배분법 (Historical Cost Allocation Method)"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 복수의 금융상품을 일괄 발행하고 그 총대가를 나눌 때, 각 상품의 개별 공정가치를 합한 총공정가치 중에서 각 상품이 차지하는 '상대적인 공정가치 비율'대로 안분 배분하는 기법을 '상대적 공정가치비율 배분법'이라고 칭하며, K-IFRS 하의 대원칙입니다.\n\n[오답 해설]\n① 잔여가치법은 일부 공정가치만 신뢰성 있게 알 때 시가 확인 가능 부분 먼저 차감 후 남은 잔액을 배분하는 차선책입니다.\n③, ④ 액면가나 장부가는 공정가치를 대변하지 못하므로 배분 기준이 될 수 없습니다.\n⑤ 역사적원가는 주식 신규 발행 시점의 평가 속성과 부합하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "보통주와 우선주의 일괄발행 거래에서, 우선주의 개별 공정가치(시가)는 신뢰성 있게 추정 가능하나 보통주의 시가는 전혀 파악할 수 없는 예외적 상태에서 일괄발행금액을 각 주식에 배분하는 방법인 '잔여가치법(Residual Value Method)'의 처리 규칙은?",
        "options": [
            "① 보통주에 먼저 액면가를 배분하고, 우선주에 잔액을 다 배분한다.",
            "② 일괄 수령 총액에서 개별 시가를 아는 우선주의 공정가치를 우선 차감 배정하고, 남은 잔여 금액 전액을 시가를 모르는 보통주에 배분한다.",
            "③ 우선주와 보통주의 발행 수를 기준으로 반씩 균등 안분한다.",
            "④ 양자의 액면가 차액만큼을 무조건 할인차금으로 계상한다.",
            "⑤ 잔여가치가 발생하므로 보통주 발행을 취소하고 우선주만 기재한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 일괄발행 시 사용되는 잔여가치법의 구체적인 작동 규칙을 묻는 문제입니다. 공정가치를 신뢰성 있게 알 수 있는 금융상품(우선주)에 해당 공정가치 금액을 우선 배정하고, 일괄수취액에서 이를 차감한 '나머지 잔여액' 전체를 공정가치를 모르는 금융상품(보통주)의 발행 대가로 책정합니다.\n\n[오답 해설]\n① 액면가를 먼저 배분하는 기준은 잘못되었습니다.\n③ 주식 수 균등 안분은 자산/자본 실질에 전혀 부합하지 않는 임의 처리입니다.\n④ 할인차금 계상은 분개 차액 정산 결과일 뿐 배분 논리가 아닙니다.\n⑤ 자본 거래 자체를 취소시킬 수는 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "청약에 의한 주식발행 결산 시, 청약일 결산기말 시점에 차변에 수취된 현금 대가와 매칭하여 대변에 임시 기재한 '신주청약증거금'의 K-IFRS 상 기말 재무상태표의 올바른 분류 위치는?",
        "options": [
            "① 자본 > 2. 자본잉여금",
            "② 자본 > 3. 자본조정",
            "③ 부채 > 1. 유동부채",
            "④ 자본 > 4. 기타포괄손익누계액",
            "⑤ 자본 > 5. 이익잉여금"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 신주청약증거금은 정식 주식배부일(납입일 완료 후 증자일) 직전까지 주주 예정자들로부터 수취한 돈을 모아 두는 임시 항목이므로, K-IFRS 상 자본 범주 하의 '자본조정'으로 분류하여 재무상태표에 기재하여야 합니다.\n\n[오답 해설]\n① 주발초와 같은 실질 잉여금 확정 상태가 아니므로 자본잉여금이 아닙니다.\n③ 채무 반환 부채가 아닙니다.\n④, ⑤ 포괄 평가손익이나 당기 영업 결과 누적액이 아니므로 AOCI 및 이익잉여금 분류는 오답입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "신주청약증거금 수취 후 주식이 정식으로 배부되어 신주 발행이 확정 완료되는 '발행일' 시점에 수행할 올바른 분개 대체 방식은?",
        "options": [
            "① 대변의 신주청약증거금을 차변으로 보내어 소멸시키고, 대변에 액면총액 상당의 '자본금'과 초과금액 상당의 '주식발행초과금'을 계상한다.",
            "② 신주청약증거금은 그대로 두고, 추가로 현금을 차변에 똑같이 한 번 더 기재한다.",
            "③ 차변에 신주청약증거금을 소멸시키며 대변에는 '이익잉여금'만 늘려 기입한다.",
            "④ 대변에 자본조정을 차감하고 차변에 영업외수익을 가산하여 당기이익을 늘린다.",
            "⑤ 자본전입 결의를 통해 신주청약증거금을 전액 이익준비금으로만 보낸다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 청약주식의 최종 배부 완료(발행일) 분개 대체 흐름에 대한 이해입니다. 기 수취하여 대변에 기재되어 있던 자본조정 항목인 '신주청약증거금'을 차변으로 보내 소멸 제거하고, 대변에 정식 액면금액 기준 법정 '자본금'과 액면초과 대가 기준 '주식발행초과금(자본잉여금)'을 기입하여 대체 정산합니다.\n\n[오답 해설]\n② 현금이 이중 유입되지 않으므로 추가 현금 기입은 오류입니다.\n③ 보통주자본금의 대변 증가가 필수적이므로 자본금 계상이 누락된 이익잉여금 단독 가산은 틀립니다.\n④, ⑤ 당기순이익이나 이익준비금 대체와는 무관한 정식 신주 교부 자본 대체 거래입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "회사가 발행한 종류주식인 우선주 중, 특정 만기에 주주가 회사에 상환을 청구하거나 회사가 반드시 의무적으로 현금을 지급하고 매입 소각하여야 하는 계약 조건이 명시된 '의무상환식 우선주'의 K-IFRS 상의 재무제표 표시 분류는?",
        "options": [
            "① 자본 > 1. 자본금",
            "② 자본 > 2. 자본잉여금",
            "③ 부채 > 금융부채 (상각후원가 측정 부채 등)",
            "④ 자본 > 3. 자본조정",
            "⑤ 부채 > 충당부채"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1032호 '금융상품 표시'에 따라, 회사가 주식을 상환하기 위해 미래에 현금 등 금융자산을 인도해야 할 계약상 회피 불가능한 의무를 부담하는 경우(의무상환식 우선주 등), 명칭이 주식(우선주)일지라도 실질에 맞추어 자본이 아닌 '금융부채'로 분류하여 재무제표 부채 영역에 기재하도록 요구합니다.\n\n[오답 해설]\n①, ②, ④ 계약상 의무가 지배적이어서 회피가 불가능하므로 자본 분류(자본금, 자본잉여금, 자본조정 등)는 적용이 원칙적으로 배제됩니다.\n⑤ 금액과 지출 시점이 확정되어 계약상 의무를 가지므로 추정 부채인 충당부채가 아닌 확정 금융부채로 갑니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "우선주를 신규 발행할 때, 해당 우선주 주주에게 언제든지 보통주 주식으로 1:1로 전환을 청구할 수 있는 권리가 내재된 '전환우선주(Convertible Preferred Shares)'가 K-IFRS 상 완벽한 '자본'으로 분류되기 위한 가장 핵심적인 계약 조건은?",
        "options": [
            "① 보통주 전환 시 수량 비율이 확정수량 대 확정금액 조건('Fixed-for-Fixed')을 충족하여야 한다.",
            "② 우선주의 만기가 무조건 3년 이내로 보장되어 조기 소멸해야 한다.",
            "③ 우선주 배당률이 변동금리에 완전 연동되어 이자비용처럼 흘러가야 한다.",
            "④ 전환 시 추가 현금을 납입하지 않는 현물 교환이어야 한다.",
            "⑤ 회사가 보통주 대신 채무 증서로도 지급해 줄 수 있는 선택권이 보유되어야 한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 전환우선주나 전환사채 등의 복합금융상품 성격 지분 대안이 부채 요소 없이 순수 자본(지분상품)으로 안전하게 분류되기 위해서는 전환 시 인도할 보통주식의 수량과 수취할 대가가 확정 대 확정('Fixed-for-Fixed') 조건을 충족해야 합니다. 주가 변동에 따라 인도할 주식 수가 사후 변동(Refixing 등)되는 조건이 붙는다면 자본이 아닌 금융부채(파생부채 요소 등)로 분류되어 평가받게 됩니다.\n\n[오답 해설]\n② 만기가 정해진 상환권이 개입되면 부채 성격이 강해집니다.\n③ 변동금리 배당조건은 부채적 성격을 나타낼 수 있지만 자본분류의 절대적 고유판단 조건은 아닙니다.\n④, ⑤는 전환 시 자본성 확립 조건과 무관한 추가 계약 사항들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s03-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "우리나라 상법 상 보통주의 액면가 미달 유상증자(주식할인발행)를 실시할 때, 회사가 반드시 사전에 이행하여야 하는 적법 법적 요건에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 이사회의 출석 이사 전원 찬성 결의만 있으면 법적 요건이 충족된다.",
            "② 주주총회의 특별결의를 거쳐 법원의 인가(승인)를 얻어야 하고, 회사 설립일로부터 2년이 경과한 후에만 할인발행이 가능하다.",
            "③ 상법상 어떠한 경우에도 주식의 액면 미달 발행은 원천 차단된다.",
            "④ 금융감독원장이 지정해 준 감정평가사의 할인액 감정을 선행하여야 한다.",
            "⑤ 채권자 전체의 서면 서명이 담긴 채권자 이의신청 절차 통과가 우선 필수적이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 자본 충실의 원칙에 따라 우리나라 상법은 액면 이하의 주식 할인발행을 제한하고 있으며, 예외적으로 이를 실행하기 위해서는 회사 설립일로부터 2년이 경과하여야 하고, 주주총회의 특별결의를 통과한 후 법원의 최종 승인(인가)을 얻었을 때 비로소 할인발행이 가능합니다.\n\n[오답 해설]\n① 이사회 단독 결의로는 자본 충실 의무 조항을 우회할 수 없습니다.\n③ 상법상 조건부로 허용하므로 원천 차단 주장은 틀렸습니다.\n④, ⑤ 금융감독원장 및 채권자 서면 동의 절차는 법정 할인발행 승인 요건이 아닙니다.",
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

print(f"Saved database with {len(questions)} questions. Added {len(new_questions)} questions.")
