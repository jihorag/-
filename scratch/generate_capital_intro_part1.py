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
    "item": "1절 자본의 의의"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q2451 ~ Q2460) ---
    {
        "id": "practice-accounting-ch10s01-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 재무보고를 위한 개념체계에 따른 '자본(Equity)'의 정의로 가장 올바른 것은?",
        "options": [
            "① 기업이 보유하고 있는 현금 및 현금성자산의 단순 합계액",
            "② 기업의 자산총액에서 부채총액을 차감한 잔여지분(residual interest)",
            "③ 주주총회에서 결의된 배당가능이익의 최대 법적 한도액",
            "④ 기업이 영업활동을 통해 획득한 당기순이익의 누적액",
            "⑤ 발행주식의 액면금액에 총 발행주식수를 곱한 법정자본금"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 개념체계에 따라 자본은 기업의 모든 부채를 차감한 후에 남는 기업 자산에 대한 잔여지분(residual interest)으로 정의됩니다.\n\n[오답 해설]\n① 자본은 현금자산의 합계가 아니라 자산에서 부채를 뺀 순자산의 총액입니다.\n③ 배당가능이익은 자본의 일부(이익잉여금)를 구성할 뿐 자본 전체의 정의가 아닙니다.\n④ 당기순이익 누적액은 이익잉여금을 의미하며, 자본에는 주주가 납입한 자본금이나 자본잉여금 등도 포함되므로 자본 전체의 정의로 불충분합니다.\n⑤ 법정자본금은 자본의 한 구성요소(자본금)에 불과합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "K-IFRS 재무제표 표시 기준 상 자본의 성격과 측정(Measurement)에 관한 설명 중 가장 올바르지 않은 것은?",
        "options": [
            "① 자본은 재무상태표에서 자산과 부채와 달리 독립적으로 측정하는 단위나 기준을 갖지 않는다.",
            "② 자본은 자산과 부채가 측정됨에 따라 부수적으로 측정되는 종속적 성격을 가진다.",
            "③ 자본의 총계는 기업의 시장가치(시가총액)나 공정가치와 원칙적으로 일치하여야 한다.",
            "④ 자본은 소유주의 투자, 이익의 유보, 기타포괄손익 등의 누적으로 구성된다.",
            "⑤ 자본의 세부 분류(자본금, 자본잉여금 등)는 재무제표 이용자에게 유용한 정보(의사결정 리스크 등)를 제공하기 위해 구분하여 표시된다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 재무제표 상 자본의 장부금액은 자산과 부채의 측정 기준에 따라 유도되는 잔액일 뿐이며, 주식시장에서 거래되는 기업의 시가총액이나 공정가치와 일치하지 않는 것이 일반적입니다.\n\n[오답 해설]\n①, ② 자본은 부채를 차감한 잔액으로 평가되므로 독립적인 측정 단위가 없고 종속적으로 산출됩니다.\n④ 자본의 증가 및 변동은 출자, 손익의 유보 및 평가손익(OCI)의 발생으로 누적됩니다.\n⑤ 상법 등 법적 규정이나 투자자 유용성에 부합하도록 자본 내역을 세부 계정으로 구획 보고합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "회계에서 주주(소유주)와 관련된 '자본거래(Capital Transactions)'와 경영성과와 관련된 '손익거래(Income Transactions)'를 엄격히 분리하여 인식하는 핵심 회계학적 배경으로 옳은 것은?",
        "options": [
            "① 주주에게 배당금을 무조건 지급하여 영업이익을 0으로 강제 환원하기 위함이다.",
            "② 소유주로서의 자격을 행사하는 주주와의 자본거래는 당기 포괄손익(당기손익 및 기타포괄손익) 계상에서 전면 배제하여 자본에 직접 반영하기 위함이다.",
            "③ 기업의 총부채 비율을 항상 100% 이하로 통제하기 위한 세무상의 조치이다.",
            "④ 이익잉여금을 세무 세액 공제를 위해 자본금과 상계 처리하여 제거하기 위함이다.",
            "⑤ 모든 자본 잉여금의 현금 환원을 주식 시장에서 차단하기 위함이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 자본거래와 손익거래의 구분 실질입니다. 주주가 소유주 자격으로 참여하는 자본거래(유상증자, 감자, 배당 등)는 당기의 이익이나 손실을 구성하는 포괄손익계산서 항목이 될 수 없으며, 재무상태표 상의 자본 계정에 직접 가감 조치해야 합니다.\n\n[오답 해설]\n① 배당금은 당기 비용이 아닌 이익잉여금 처분이므로 영업이익 차감과 무관합니다.\n③ 부채 비율 통제는 재무 관리 목적일 뿐 자본/손익 분리의 근거가 아닙니다.\n④, ⑤ 상계 제거 조항 및 현금 환원 차단은 회계적 분리 논리와 상관없는 왜곡 서술입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "다음 중 한국의 일반적인 회계 관행과 상법에 따라 구분 표시하는 자본의 5대 구성 분류 중, 성격이 손익거래의 누적 결과에 해당하는 자본 계정은?",
        "options": [
            "① 자본금 (Capital Stock)",
            "② 자본잉여금 (Capital Surplus)",
            "③ 자본조정 (Capital Adjustment)",
            "④ 이익잉여금 (Retained Earnings)",
            "⑤ 기타자본조정"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 이익잉여금(Retained Earnings)은 영업활동 등 손익거래에서 발생한 이익 중 배당 등으로 유출되지 않고 사내에 유보되어 자본화된 당기순손익의 누적 성격입니다.\n\n[오답 해설]\n① 자본금은 발행주식의 액면가 총액으로 자본거래의 성격입니다.\n② 자본잉여금은 증자, 감자 등 주주와의 자본거래에서 발생한 액면 초과 금액 등 자본 성격의 이입분입니다.\n③ 자본조정은 자본거래 중 자본금이나 자본잉여금으로 분류하기 어려운 가감 계정입니다.\n⑤ 기타자본조정 또한 자본조정의 한 분류로 자본거래에 속합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "K-IFRS 제1032호에 의거하여 유상증자 등 주식을 발행하는 과정에서 주간사 수수료, 인수 법률 비용 등 발행과 직접적으로 관련되어 발생한 '자본거래 원가(Transaction Costs)'의 올바른 회계처리 방법은?",
        "options": [
            "① 당기 포괄손익계산서 상의 당기비용(지급수수료 등)으로 전액 즉시 인식한다.",
            "② 자본거래의 일부이므로 주식발행액에서 차감하여 자본(주식발행초과금 등)에서 직접 차감 반영한다.",
            "③ 무형자산인 개업비로 처리하여 5년간 정액 감가상각한다.",
            "④ 유형자산 건설중인자산 취득원가에 전액 자본화 가산한다.",
            "⑤ 기타포괄손익(OCI) 평가손실로 분류하여 자본 대변에 기입한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 자본거래원가의 회계처리 원칙입니다. 신주 발행 등 자본거래와 직접 관련하여 발생한 증자 수수료나 법률 비용은 관련 세무효과를 반영한 후, 주식발행가액에서 차감하여 자본(주식발행초과금에서 차감, 부족 시 주식할인발행차금으로 자본조정 가산)에 직접 조치해야 합니다.\n\n[오답 해설]\n① 비용으로 손익에 던지는 처리는 기준 위배입니다.\n③ 개업비 무형자산 상각은 과거의 폐지된 회계 기준입니다.\n④ 유형자산화하는 것은 자산 왜곡입니다.\n⑤ OCI 평가 변동에 속하지 않으므로 오답입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "K-IFRS 기준 상 자본거래(예: 자기주식 처분손익, 주식발행 수수료 등)와 직접 연동되어 법인세 감면 등의 효과(Tax Effects)가 유발된 경우, 이 세액 감면액은 어디에 보고하여야 하는가?",
        "options": [
            "① 당기순이익에 가산할 법인세 비용 절감 수익으로 법인세비용에서 차감한다.",
            "② 손익계산서를 거치지 않고, 당해 세무 효과 금액을 연관된 자본 계정에 직접 가감(자본 직접 반영)하여야 한다.",
            "③ 전액 납입자본금 계정에 가산하여 자본금 총액을 불린다.",
            "④ 이월결손금 전액과 즉시 대체하여 장부에서 소멸시킨다.",
            "⑤ 이사회 특별 결의를 거치기 전에는 세무 조정 유보로 전액 부채란에 둔다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1012호 및 제1032호에 따라, 자본에 직접 기입되는 항목(자본거래 원가 등)과 관련된 당기법인세 및 이연법인세 효과는 관련된 자본 계정에 직접 반영해야 합니다 (손익계산서 본문의 법인세 비용에 반영해서는 안 됩니다).\n\n[오답 해설]\n① 당기순이익의 법인세비용 차감 계정으로 보내는 조치는 당기 손익을 왜곡하는 회계 오류입니다.\n③ 자본금(액면가)을 변동시키는 분개는 불가능합니다.\n④, ⑤ 결손금 자동 소멸 및 부채 강제 보유 지침은 기준 외 자의적인 거짓 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "K-IFRS 제1032호 금융상품 표시 기준에 따라, 특정 상품이 '금융부채'가 아닌 '지분상품(자본)'으로 분류되기 위해 필수적으로 결여되어야 하는 성격은?",
        "options": [
            "① 거래처에 제품을 인도할 일반적 상거래 계약",
            "② 계약 상대방에게 현금 등 금융자산을 인도하거나 잠재적으로 불리한 조건으로 금융자산/부채를 교환해야 하는 계약상 의무(Contractual Obligation)",
            "③ 주식 매입 시 배당금을 소급 수취할 채권적 권리",
            "④ 만기 시 원금을 유형자산으로 대체 상환받을 내재 조건",
            "⑤ 회사의 의결권을 획득하여 주주총회에 참석할 권능"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 금융부채와 지분상품(자본)의 가장 핵심적인 구분 잣대입니다. 발행자가 계약 상대방에게 현금 등 금융자산을 인도하거나 불리한 조건으로 금융자산을 교환해야 하는 '계약상 의무(Contractual Obligation)'를 부담하지 않고, 이를 무조건 회피할 권리를 가질 때에만 '지분상품(자본)'으로 적합하게 인식할 수 있습니다.\n\n[오답 해설]\n① 상거래 제품 인도 의무는 금융부채 분류와 직결된 금융자산 인도 계약이 아닙니다.\n③ 배당 수취 권리는 투자자의 자산 측면 설명입니다.\n④ 원금을 유형자산으로 대체하는 조항이나 ⑤ 의결권 보유 등은 지분상품으로 귀결되기 위한 계약상 인도 의무 배제 원리와 무관합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "K-IFRS 제1032호 기준 하의 지분상품(Equity Instrument)에 대한 설명 중 가장 옳은 것은?",
        "options": [
            "① 발행 시점에 이자가 확정적으로 지급되며 만기일에 원금 상환이 법적으로 보장되는 증서",
            "② 기업의 자산에서 모든 부채를 차감한 후의 잔여지분을 나타내는 계약",
            "③ 기업이 만기 시 자기주식을 제3자에게 시장 가격보다 비싸게 매각하기로 맺은 파생부채 계약",
            "④ 법정 기일 내에 환불이 청구될 경우 무조건 현금을 돌려주기로 서약한 예금 성격의 상품",
            "⑤ 신용 손실이 발생할 경우 예금자 보험공사로부터 보상받는 금융자산 보호 권리"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1032호 문단 11에 의거, 지분상품(자본)이란 기업의 모든 부채를 차감한 후의 잔여지분을 나타내는 모든 계약을 통칭합니다.\n\n[오답 해설]\n① 이자 확정 및 원금 상환 보장은 정형적인 금융부채(사채 등)의 설명입니다.\n③ 파생부채나 ④ 무조건적 현금 환불 의무는 부채로 분류되어야 하는 계약들입니다.\n⑤ 예금 보호 조항은 지분상품의 본질적 정의와 무관합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "K-IFRS 개념체계 상 '자본유지개념(Capital Maintenance Concepts)'에 관한 설명 중 가장 올바르지 않은 것은?",
        "options": [
            "① 자본유지개념은 기업이 유지하고자 하는 자본을 어떻게 정의하느냐에 따라 재무적 자본유지와 실물적 자본유지로 구분된다.",
            "② 재무적 자본유지개념 하에서는 명목화폐단위 또는 불변구매력단위로 측정된 순자산의 증가액을 이익으로 본다.",
            "③ 실물적 자본유지개념 하에서는 기초의 실물생산능력을 초과하여 기말에 보유한 실물생산능력의 증가분을 이익으로 본다.",
            "④ 실물적 자본유지개념을 적용할 때 기말 자산·부채의 가격 변동에 따른 모든 평가손익은 즉시 당기순이익으로 인식한다.",
            "⑤ 자본유지개념은 이익이 측정되는 기저를 제공하며, 자본의 정의와 직접적으로 연계된다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 실물적 자본유지개념 하에서는 자산과 부채의 가격 변동(보유손익)을 이익으로 보지 않고, 기업의 실물생산능력을 유지하기 위한 자본의 일부(자본유지조정 항목)로 취급하여 직접 자본에 계상합니다 (당기순이익에 포함하지 않습니다).\n\n[오답 해설]\n①, ⑤ 자본유지의 두 축인 재무적/실물적 구분 및 이익 산정의 가이드라인에 대한 정합한 기술입니다.\n② 재무적 자본유지에서는 순자산(가치)의 화폐적 증가를 이익으로 인식합니다.\n③ 실물적 자본유지에서는 일일 생산량이나 공장 설비 등 실물적 공급 능력의 물리적 증강분을 기준으로 삼습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "회계의 손익보고체계에서 자본 항목의 변동을 반영하는 '기타포괄손익(Other Comprehensive Income; OCI)'과 '당기순이익(Net Income)'의 관계 및 성격에 대한 설명 중 옳은 것은?",
        "options": [
            "① 기타포괄손익은 당기순이익의 하부 구성요소이므로 매년 당기순이익에 전액 합산된다.",
            "② 당기순이익과 기타포괄손익의 합계액은 포괄손익(Total Comprehensive Income)을 구성하며, 주주와의 자본거래를 제외한 순자산의 모든 기중 변동을 나타낸다.",
            "③ 기타포괄손익은 주주에게 지불한 배당금을 명칭 변경한 것뿐이다.",
            "④ 당기순이익은 재무상태표 본문에 직접 계상되고, 기타포괄손익은 자본금 액면가를 직접 조정한다.",
            "⑤ 기타포괄손익누계액은 매기말 결산 시 무조건 이익잉여금 계정으로 전액 자동 합산되어 소멸한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 포괄손익의 개념입니다. 당기순이익과 기타포괄손익(OCI)을 더한 총포괄손익은 주주와의 거래(증자, 배당 등)를 제외하고 거래나 기타 사건으로 인해 발생한 순자산의 총 변동액을 의미합니다.\n\n[오답 해설]\n① OCI는 당기순이익과 별도로 포괄손익계산서에 구성되며 당기순이익에 누적 가산되지 않습니다.\n③ 배당금은 이익잉여금의 유출 거래로 OCI와 완전 무관합니다.\n④ OCI는 자본금 액면가를 조정하지 않고 별도의 자본항목인 기타포괄손익누계액으로 쌓입니다.\n⑤ 재분류되지 않는 OCI 누계액(예: FVOCI 지분상품 평가손익) 등은 자동으로 이익잉여금으로 이체 소멸되지 않으며 자본 항목 내에 잔존합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },

    # --- L2 (이해): 15문항 (Q2461 ~ Q2475) ---
    {
        "id": "practice-accounting-ch10s01-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "K-IFRS 제1032호 기준에 따라 우선주(Preference Shares)의 계약 조건에 따른 회계적 분류(부채 vs 자본) 판정 중 가장 옳은 것은?",
        "options": [
            "① 우선주라는 명칭이 붙어있다면 계약상 실질과 무관하게 상법 규정에 따라 무조건 지분상품(자본)으로 분류하여야 한다.",
            "② 발행자가 특정 시점에 주주에게 무조건 원금을 상환하여야 하거나 주주가 상환을 청구할 권리를 보유하는 상환우선주(Redeemable Preference Shares)는 '금융부채'로 분류한다.",
            "③ 발행자가 상환권(콜옵션)을 보유하고 주주에게는 상환 청구권이 없는 상환우선주도 발행 즉시 금융부채로 분류하는 것이 대칭적이다.",
            "④ 배당 결의를 연기할 수 있는 재량권이 없는 우선주는 전액 기타포괄손익 자본조정 계정으로 이월한다.",
            "⑤ 발행주식수 조절 옵션이 내재되어 있다면 액면금액의 50%를 부채로, 50%를 자본으로 일괄 가분한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우선주의 계약상 실질에 따른 부채/자본 분류 판단입니다. 만일 상환우선주의 계약 조건상 보유자(주주)가 상환 청구권을 가지거나, 발행자가 의무적으로 상환해야 하는 조항이 있다면 이는 발행자가 현금 등 금융자산을 인도해야 하는 계약상 의무를 피할 수 없으므로 실질이 사채와 같아 '금융부채'로 분류됩니다.\n\n[오답 해설]\n① 명칭이 우선주(지분 성격)라 하더라도 계약 조건에 상환 의무가 강제되어 있다면 부채로 분류하는 실질우선의 원칙이 적용됩니다.\n③ 발행자만 상환권(선택권)을 가진 상환우선주는 주주에게 현금을 갚아야 하는 무조건적인 의무가 없으므로 원칙적으로 '지분상품(자본)'에 해당합니다.\n④, ⑤ 배당 재량권 결여 시의 자본조정 이체나 50%씩 일괄 안분한다는 주장은 K-IFRS 기준을 위배한 거짓 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "다음 중 K-IFRS 제1032호 금융상품 표시 원칙 상, 발행 회사 입장에서 '지분상품(자본)'으로 적합하게 분류할 수 있는 우선주는?",
        "options": [
            "① 보유자(주주)에게 계약상 의무적인 만기일에 자금을 상환받을 청구권이 부여된 상환우선주",
            "② 주주가 기업의 자산에서 모든 부채를 차감한 후의 잔여지분에 분배를 요구할 권리만 있고, 발행자에게 상환(현금화) 의무나 배당 지급에 대한 누적적 의무 강제가 부과되지 않은 순수 비상환우선주",
            "③ 주채무자의 자금 부도 발생 시 발행자가 무조건 액면 금액으로 바이백(Buy-back)할 것을 약정한 우선주",
            "④ 매년 당기순이익의 존재 여부와 주주총회 결의 여부와 무관하게 연 10%의 확정 배당금을 누적 지급할 의무가 계약상 강제된 누적적 우선주",
            "⑤ 상환 가격이 사전에 고정되지 않고 미래의 금리 변동에 비례하여 변동 조절되어 결제되는 조건부 상환우선주"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 지분상품(자본)의 요건 충족 사례입니다. 발행자에게 현금 등 금융자산을 인도해야 하는 무조건적인 계약상 의무가 결여되어 있고, 배당선언에 대한 전적인 재량권(의무 결여)을 보유하며 잔여지분을 나타내는 순수 비상환우선주는 지분상품(자본)으로 온전히 분류됩니다.\n\n[오답 해설]\n① 만기 상환청구권 우선주, ③ 부도 시 의무 바이백 우선주, ④ 배당 의무가 강제된 우선주, ⑤ 변동 조건부 상환우선주 등은 발행자에게 자산 인도 의무가 회피 불가능하게 연동되어 있으므로 전액 혹은 일부가 '금융부채'로 분류되어야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "계약 조건상 '금융부채'로 성격 규정된 상환우선주에 대해, 발행 회사가 주주에게 지급한 배당금(Dividends)의 포괄손익계산서 상의 적격한 표시 및 처리 방법은?",
        "options": [
            "① 지분상품의 배당이므로 자본 변동표 상에서 이익잉여금의 차감(처분)으로 직접 처리한다.",
            "② 금융부채에서 발생한 금융비용이므로, 당기 포괄손익계산서 상의 '이자비용(영업외비용)'으로 인식하여 당기순손익에 반영한다.",
            "③ 기타포괄손익(OCI) 평가손실의 자본 항목으로 직접 대변 대체한다.",
            "④ 유형자산의 차입원가로 보아 장부 금액에 소급 가산하여 자산화한다.",
            "⑤ 법인세 비용의 선납 세금 자산으로 인식하여 차기 결산으로 넘긴다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1032호 문단 35 및 36에 따라, 금융부채로 분류된 금융상품(예: 부채성 상환우선주)의 보유자에게 지급한 배당금이나 분배금은 사채의 표시이자와 마찬가지로 당기 포괄손익계산서의 '이자비용(비용)'으로 인식하여 당기순손익을 계산해야 합니다.\n\n[오답 해설]\n① 부채로 판정된 우선주의 배당은 이익잉여금 직접 처분이 불가능하며 비용 계상이 필수입니다.\n③ OCI 차감이나 ④ 자산화 처리, ⑤ 선납세금 대체 등은 금융부채 배당금의 이자비용 분류 원칙에 정면으로 위배되는 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "다음 중 K-IFRS 제1032호 및 제1109호 상 '금융부채'와 '지분상품(자본)'의 구분에 대한 설명 중 가장 옳지 않은 것은?",
        "options": [
            "① 발행자가 자금을 무조건 상환해야 하는 의무를 지는 상품은 실질에 따라 금융부채로 분류된다.",
            "② 지분상품은 자산에서 부채를 차감한 후 잔여지분을 나타내므로, 기업의 자산 및 부채가 재측정될 때 자본 항목의 평가 잔액도 함께 유도적으로 조정된다.",
            "③ 계약 상 보유자가 원할 때 언제든지 주식을 기업에 반환하고 현금을 수취할 수 있는 풋옵션부 주식(Puttable Instrument)은 원칙적으로 발행자 입장에서 금융부채에 해당한다.",
            "④ 복합금융상품(예: 전환사채) 발행 시 부채요소와 자본요소로 분리하여 인식하는 조치는 거래의 계약상 결제 실질을 충실히 표현하기 위한 것이다.",
            "⑤ 발행주식의 액면금액은 주식시장에서 거래되는 시가총액 변동에 맞추어 기말 평가 시마다 매번 공정가치로 재측정하여 장부 자본금 총액을 갱신하여야 한다."
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ 주식의 액면금액은 상법 상 고정된 법정자본금을 구성하므로, 주식의 시가 변동이나 기말 평가와 전혀 무관하며 공정가치로 장부 자본금을 재측정하는 회계처리는 허용되지 않습니다.\n\n[오답 해설]\n① 상환의무성 부채 판정, ② 자본의 잔여지분 성격에 따른 재측정 유도, ③ 풋옵션부 주식의 원칙적 부채 분류(의무 존재), ④ 전환사채의 부채/자본 복합 분리 요건은 K-IFRS 상 부채와 자본의 대칭 분류 원칙을 올바르게 설명하고 있습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "기업이 소유주(주주)의 자격을 행사하는 기존 주주들에게 주식 기준 배당(주식배당)을 실시하거나, 주주가 아닌 근로자 등에게 주식기준보상(스톡옵션)을 제공하는 경우에 대한 K-IFRS 기준 상 자본 분류에 관한 설명으로 옳은 것은?",
        "options": [
            "① 주식배당은 기업 외부로 자산의 유출이 없으므로 자본총계에 아무런 영향이 없으며 자본 항목 간의 대체만 발생한다.",
            "② 주식배당은 당기순이익에 직접 차감하는 비용 분개를 수반하여 기말 순이익을 감소시킨다.",
            "③ 종업원에게 부여한 주식선택권(스톡옵션)은 부여 시점에 즉시 법정자본금으로 대변 인식한다.",
            "④ 주식배당 시 발행되는 신주의 액면총액만큼 자본잉여금을 대변에 일치 기장하여야 한다.",
            "⑤ 주식배당을 선언한 시점에는 아직 주식이 발행되지 않았으므로 임시로 금융부채 대변에 이체 계상해야 한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 주식배당의 자본 영향입니다. 주식배당은 현금 배당과 달리 회사 외부로 자원(현금 등)이 유출되지 않고, 이익잉여금이 법정자본금으로 전입되는 형태이므로 자본 내의 항목 간 이동(자본금 증가, 이익잉여금 감소)에 불과하며 자본총계에는 변동이 없습니다.\n\n[오답 해설]\n② 주식배당은 손익계산서 비용이 아니므로 순이익 감소와 무관합니다.\n③ 스톡옵션은 권리 행사 전까지 자본조정(주식선택권) 등으로 관리하며 최초 부여 시 즉시 자본금(액면가)으로 설정하지 못합니다.\n④ 주식배당 시 전입액만큼 '자본금'이 늘어나므로 자본잉여금 증가 설명은 거짓입니다.\n⑤ 주식배당 선언 시에는 자본조정(미교부주식배당금)으로 대기할 뿐 자산 유출 의무가 없으므로 부채가 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "자기주식(Treasury Shares)의 취득, 보유 및 처분에 대한 K-IFRS 기준 상 회계처리와 자본 표시에 관한 설명 중 옳은 것은?",
        "options": [
            "① 자기주식을 취득할 때 지출한 대금은 당기 포괄손익계산서 상의 영업외비용으로 계상한다.",
            "② 자기주식은 주주와의 거래를 통해 회수한 것이므로 취득 가액만큼 자본에서 직접 차감(자본조정의 차감 항목)하여 표시한다.",
            "③ 자기주식을 보유하는 동안에는 공정가치 변동을 매 결산기마다 측정하여 자기주식 평가이익(당기손익)을 설정한다.",
            "④ 자기주식을 매입가보다 높은 가격에 처분할 때 발생하는 자기주식처분이익은 당기순이익(영업외수익)에 계상한다.",
            "⑤ 자기주식의 보유 잔액은 재무상태표 차변의 정식 유동자산(투자자산) 항목으로 분류하여 보고한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 자기주식의 자본 성격과 회계처리입니다. 자기주식의 취득과 처분은 소유주(주주)와의 자본거래에 해당합니다. 따라서 취득 가액은 자산으로 계상할 수 없고 자본에서 차감하는 자본조정 항목으로 대차대조표에 표기하여야 합니다.\n\n[오답 해설]\n① 취득 대금은 비용이 아닌 자본 차감입니다.\n③ 자기주식은 자산이 아니므로 공정가치 평가 대상이 아닙니다.\n④ 자기주식처분이익은 자본거래의 결과물이므로 당기 손익(수익)이 아니라 자본잉여금으로 직접 자본 대변에 쌓아야 합니다.\n⑤ 자산 분류는 K-IFRS 하에서 전면 금지되는 왜곡 보고입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "자기 지분상품(자기주식)으로 결제되거나 결제될 수 있는 계약(파생상품 계약 등)에 대해 K-IFRS 제1032호가 규정하는 부채와 자본의 판정 요건 중, 이른바 'Fixed-for-Fixed(고정 수량 대 고정 금액)' 원칙에 대한 설명으로 옳은 것은?",
        "options": [
            "① 인도할 자기지분상품의 수량이 기말 주가 변동에 따라 계속 변동되더라도 수령할 현금액이 고정되어 있다면 무조건 자본으로 인식한다.",
            "② 계약 상대방에게 확정 수량의 자기지분상품을 인도하고 확정 금액의 현금 등 금융자산을 수취하는 계약에 한하여 '지분상품(자본)'으로 분류할 수 있다.",
            "③ 인도할 지분 수량과 금액이 모두 유동적으로 변동되어야 비로소 자본거래 요건이 승인된다.",
            "④ 자기주식 10주를 인도하고 기말 환율에 연동된 변동 외화를 수취하는 계약은 자본 분류 요건에 전적으로 부합한다.",
            "⑤ 수량과 금액 중 하나라도 확정되어 있다면 자본조정 평가액의 50%를 부채로 이월한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1032호 상 자기지분상품 결제 계약의 자본 분류 요건(Fixed-for-Fixed)입니다. 변동 수량이나 변동 금액 조건의 결제 계약은 실질적으로 자기주식을 결제 수단(현금 대용)으로 활용하는 파생부채/자산 계약에 불과하므로, '확정 수량의 자기주식'과 '확정 금액의 현금'이 교환되는 순수 선도/옵션 거래인 경우에만 예외적으로 '지분상품(자본)'으로 분류를 인정합니다.\n\n[오답 해설]\n① 수량이 변동된다면 고정 금액을 받더라도 파생부채로 분류해야 합니다.\n③ 변동 조건은 부채 분류 사유입니다.\n④ 변동 외화 수취 조건은 원화 가치로 환산 시 변동 수취에 해당하므로 부채 분류 건에 해당합니다.\n⑤ 50% 이월 기준 등은 K-IFRS에 근거가 없는 오답 지문입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "K-IFRS 제1032호 문단 25에 의거하여, 의무의 유효성이나 결제 여부가 기업과 보유자 모두 통제할 수 없는 불확실한 미래사건의 발생 여부에 따라 결정되는 '조건부 결제규정(Contingent Settlement Provisions)'이 내재된 금융상품의 올바른 회계적 분류 원칙은?",
        "options": [
            "① 아직 미래 사건이 발생하지 않았으므로 사건 발생 전까지는 무조건 자본으로 선 분류한다.",
            "② 발행자가 현금 등 금융자산의 인도를 회피할 수 있는 무조건적인 권리가 없으므로 원칙적으로 '금융부채'로 분류한다.",
            "③ 계약 상 조건부 조항이 있다면 주주총회 특별의결 전까지는 장부 기재를 완전 보류한다.",
            "④ 금융감독원 승인을 거쳐 무조건 자본조정 누적금으로 이월 관리하여야 한다.",
            "⑤ 조건부 결제 사건의 성격이 아주 희박하더라도 무조건 자본 항목의 감액 분개를 수행한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 조건부 결제 규정이 있는 경우의 부채 분류 대원칙입니다. 발행자가 통제할 수 없는 사건에 연동되어 상환이나 현금 결제가 강제될 위험이 있는 계약은, 발행자 입장에서 금융자산 인도를 회피할 무조건적인 권리가 결여된 현재의무 상태로 해석하므로 원칙적으로 '금융부채'로 분류합니다. (단, 결제 규정의 실현 가능성이 극히 희박하거나 청산 시에만 발동되는 경우 등 극히 제한적인 예외 하에서만 자본 분류가 유지될 수 있습니다.)\n\n[오답 해설]\n① 사건 발생 전이라도 의무 회피 불능 조건 하에서는 부채 분류가 선행되어야 하므로 오답입니다.\n③ 장부 기재 보류나 ④ 자본조정 이체, ⑤ 자본 감액 분개 강제 규정 등은 정합성이 없는 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "다음 중 K-IFRS 기준 상 '자본잉여금(Capital Surplus)'과 '자본조정(Capital Adjustment)'의 계정 분류 대조에 대한 설명으로 가장 옳지 않은 것은?",
        "options": [
            "① 자본잉여금은 주식발행초과금, 감자차익, 자기주식처분이익 등을 포함하는 주주 거래의 초과 이입액 범위이다.",
            "② 자본조정은 자본거래에 해당하지만 자본금이나 자본잉여금으로 임의 구획하기 어려운 주식할인발행차금, 감자차손, 자기주식 등을 가감 성격으로 보고하는 계정 분류이다.",
            "③ 자기주식처분손실은 기중에 자본잉여금에 잔액이 있다면 우선 상계하고, 남은 차액을 자본조정(자기주식처분손실)으로 대변 기장하여 관리한다.",
            "④ 주식할인발행차금은 주식발행초과금과 즉시 우선 상계 처리한 후 잔액을 자본조정에 얹어야 한다.",
            "⑤ 자본조정 항목에 속하는 미교부주식배당금은 만기 도래 시 포괄손익계산서 상의 당기 매출액으로 강제 계상하여야 한다."
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ 미교부주식배당금은 자본조정(자본 항목)에 속하며, 실제 주식이 발행되는 주주총회 결의 집행 시점에 대변의 '자본금'으로 대체될 뿐 매출액이나 수익 손익 계정으로 계상되는 경로를 거치지 않습니다.\n\n[오답 해설]\n① 자본잉여금의 정의, ② 자본조정의 가감 임시 계정 분류 성격, ③ 자기주식처분손실의 자본잉여금 우선 상계 및 자본조정 이월 원칙, ④ 주식할인발행차금과 주식발행초과금의 대칭 상계 반영 원리는 상법 및 일반 회계 원칙에 완벽하게 부합합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "K-IFRS 개념체계 상 '실물적 자본유지개념'을 채택하여 당기 이익을 산출하고자 할 때 발생하는 회계적 특징으로 옳은 것은?",
        "options": [
            "① 물가 변동에 따른 자산의 가격 상승액(평가이익)은 기업의 실물생산능력을 유지하는 자본의 일부로 보아 직접 자본(자본유지조정)으로 반영하며, 당기 이익으로 보지 않는다.",
            "② 모든 자산의 장부금액을 역사적 원가(취득 원가)로 고정 평가하여 감가상각비를 0으로 유지한다.",
            "③ 명목 화폐 금액의 순자산 증가를 즉시 포괄손익계산서 상의 영업외이익으로 기장한다.",
            "④ 주주들에게 현금으로 배당금을 지급한 시점에 당기순이익이 2배로 증가하게 유도된다.",
            "⑤ 부채 비율을 임의로 축소하기 위해 부채 총량을 자본으로 일괄 이체 처리한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 실물적 자본유지개념의 핵심적인 기장적 특징입니다. 기업이 기존의 물리적인 조업/생산능력을 기말까지 지속 유지하기 위해서는 자산의 가격 상승(예: 기계장치나 원재료 가격 상승)분을 이익으로 나누어 소비해 버리면 생산능력이 위축되므로, 이를 자본의 보전 유보액(자본유지조정 자본계정)으로 보고하여 당기손익수익 계산에서 차단합니다.\n\n[오답 해설]\n② 현행 원가(Current Cost)로 자산가치를 재평가하여 상각하므로 역사적 원가 고정 주장은 틀렸습니다.\n③ 명목 화폐 증가를 그대로 이익으로 잡는 것은 '재무적 자본유지개념'의 성격입니다.\n④, ⑤ 배당 시의 순이익 급증설이나 부채 임의 자본 이체설은 회계 원리에 어긋나는 거짓 문장입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "기업이 사채(Bonds Payable)를 발행하면서 사채 보유자에게 미래 시점에 발행 회사의 주식(보통주)으로 전환할 수 있는 전환권(Conversion Option)을 제공하는 복합금융상품(전환사채)의 최초 분류와 관련하여, K-IFRS 제1032호가 규정하는 올바른 표시 원칙은?",
        "options": [
            "① 전환권은 주식으로 상환되는 것이 보장되므로 전환사채 총 액면금액을 전액 최초 자본(자본금)으로만 계상하여야 한다.",
            "② 계약상 의무에 해당하는 부채요소(사채 부분)와 현금 유출 의무가 없는 자본요소(전환권 대가)를 분리하여 재무제표 본문에 각각 부채와 자본으로 계상한다.",
            "③ 사채 부분과 전환권의 분리가 불가능하므로 최초 시점에는 전액 금융자산 유동자산으로만 대칭 기입한다.",
            "④ 전환권 대가는 주주총회 청산 시에만 분리가 가능하므로 최초 시점에는 주석 공시도 생략한다.",
            "⑤ 전환사채 총액의 80%를 기타포괄손익누계액 자본으로 강제 구획 배분한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 복합금융상품의 부채·자본 분리인식 의무입니다. 전환사채와 같이 하나의 금융상품 안에 부채의 실질(원리금 현금 상환 의무)과 자본의 실질(주식 청구 권리)이 복합된 경우에는, 최초 발행 시점에 부채요소의 공정가치를 먼저 측정하여 금융부채로 잡고, 잔액을 전환권 대가로서 자본요소로 계상하도록 강제하고 있습니다.\n\n[오답 해설]\n① 전액 자본금 기재는 부채를 탈루하는 분개 왜곡입니다.\n③ 자산 계상설이나 ④ 주석 배제 및 분리 지연설, ⑤ 80% OCI 안분설은 K-IFRS 복합상품 분리 원리와 동떨어진 오류 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "K-IFRS 개념체계 상 '재무적 자본유지개념'을 채택하여 기업의 당기 손익을 평가할 때, 명목화폐단위(Nominal Monetary Unit) 측정과 불변구매력단위(Constant Purchasing Power Unit) 측정 간의 회계적 차이에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 명목화폐단위를 채택할 때 가격 변동에 따른 자산 보유손익은 자본 조정을 거쳐 자본금 대변에 고정 잔액으로 묶여 당기손익에서 완전 배제된다.",
            "② 명목화폐단위 하에서는 보고기간 동안의 일반물가 수준 상승을 반영하기 위해 기초 순자산 가액에 무조건 물가상승율 10%를 곱한 가상 평가손실을 당기비용으로 가산하여야 한다.",
            "③ 불변구매력단위를 채택하여 자본을 유지하는 경우, 보고기간 동안 일반 물가 수준의 변동(인플레이션 등)에 따른 기초순자산의 구매력 변동 효과(자본유지조정)를 차감한 잔여 증가분만을 당기 이익으로 인식한다.",
            "④ 불변구매력단위 하에서는 모든 자산 재평가를 금지하며 역사적 화폐 취득 단가로 장부 가치를 강제 동결 보고한다.",
            "⑤ 두 단위 측정 방식 모두 동일한 당기순이익 수치를 도출하므로 공시 분류 명칭만 차이 난다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 재무적 자본유지 개념 하 불변구매력단위 적용 논리입니다. 일반 물가 상승율(구매력 저하)을 반영하는 경우, 물가상승분만큼 기초 자본의 가치가 보전되어야 실물적 의미의 실질 구매력이 유지됩니다. 따라서 자산의 명목 증가액 중 일반 물가 상승에 연동된 부분은 이익이 아닌 '자본유지조정(자본)'으로 분류하고, 이를 초과하여 상승한 잔여 실질 증가액만을 순손익(이익)으로 인식함으로써 인플레이션에 따른 왜곡을 정제합니다.\n\n[오답 해설]\n① 명목화폐단위 하에서는 기중의 자산 가격 상승분을 당기 이익(보유손익)으로 잡는 것이 정규 회계입니다.\n② 명목단위에서는 인플레이션 수정을 가하지 않고 단순 대조하므로 가상 평가손실 가산은 거짓입니다.\n④ 구매력 환산을 위해 현행 가치 평가 및 물가 지수 보정이 병행되므로 동결설은 오답입니다.\n⑤ 이익의 귀속 가액 결과물 자체가 크게 차이 나므로 동일 순이익 주장은 틀렸습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "다음 중 K-IFRS 제1032호 기준 상, 계약조건에 의거하여 발행 회사인 당사가 발행할 '자기지분상품(자기주식 보통주)'의 인도 조건에 따른 금융부채와 지분상품 분류 매칭 중 가장 옳지 않은 것은?",
        "options": [
            "① 확정 금액의 현금을 대가로 확정 수량의 보통주를 양도하기로 한 선도 계약 -> 지분상품 (자본)",
            "② 기중 변동되는 시장 이자율이나 주가 변동에 연동되어, 정산 시점의 공정가치에 부합하는 금액만큼 자기지분상품의 인도 주식수가 계속 가변 조절되는 계약 -> 금융부채 (파생부채)",
            "③ 보유자의 의결 청구에 따라 고정 비율(1:1)로 보통주 전환을 약정한 신주인수권부 대가 -> 지분상품 (자본)",
            "④ 결제 시 당사가 보통주 주식을 넘기거나 주주가 원할 경우 동등 가치의 현금으로 직접 결제(결제 선택권이 발행자에게 없음)할 수 있게 부여된 조건부 의무 계약 -> 금융부채",
            "⑤ 발행주식의 양도 가격을 대주주 사적 환율로 고정하여 보통주를 임의 배분하기로 약정한 정액 주식매각 보증 -> 지분상품 (자본)"
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ 주식 인도 계약이 대주주의 사적 환율이나 변동 지표에 의해 정산 금액 및 수량이 조절된다면 이는 '확정 수량 대 확정 가액(Fixed-for-Fixed)' 규칙을 위배하므로 지분상품(자본)이 아니라 금융부채(파생금융부채)로 분류되어야 합니다.\n\n[오답 해설]\n① 확정 대 확정 교환의 자본 분류, ② 변동 수량 주식 인도의 부채 분류, ③ 고정 비율 전환권의 자본요소 분류, ④ 현금 결제 회피권 결여에 따른 부채 분류는 K-IFRS 제1032호의 자기주식 연동 결제 요건들에 전적으로 부합합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "K-IFRS 제1001호 '재무제표 표시' 기준서 상, 자본의 총계와 세부 구성(자본금, 적립금 등)의 기중 변동 내역을 정보이용자에게 충실히 공시하기 위해 기업이 필수적으로 작성 및 보고하여야 하는 정식 재무제표의 명칭은?",
        "options": [
            "① 이익잉여금처분계산서 (Statement of Retained Earnings Appropriation)",
            "② 자본변동표 (Statement of Changes in Equity)",
            "③ 현금흐름표 (Statement of Cash Flows)",
            "④ 주기적 자본조정 보고서",
            "⑤ 재무상태표 주석 요약집"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 하에서 자본의 각 구성요소(납입자본, 이익잉여금, 기타포괄손익누계액 등)별 기초 잔액, 당기 변동 내역(당기순손익, 기타포괄손익, 주주거래 등) 및 기말 잔액의 변동 흐름을 명확히 대조 보고하는 공식 기본 재무제표는 '자본변동표'입니다.\n\n[오답 해설]\n① 이익잉여금처분계산서는 K-IFRS 상 기본 재무제표가 아니며 주석 등으로 공시됩니다.\n③ 현금흐름표는 현금 기준 유출입 정보이며 자본 구성의 총괄 변동서가 아닙니다.\n④, ⑤ 공식적인 독립 기본 재무제표 명칭이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch10s01-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "다음 중 K-IFRS 기준 상 회계처리가 포괄손익계산서 상의 '비용' 또는 '수익'으로 흘러가지 않고, 자본 계정 내에 직접 가감(손익계산서 배제)되어야 하는 거래에 속하는 항목은?",
        "options": [
            "① 유형자산 기계장치를 처분하면서 장부가액보다 높은 대금을 받아 발생한 유형자산처분이익",
            "② 유상증자를 위하여 신주를 할인 발행하면서 액면금액 미달액으로 유발된 주식할인발행차금",
            "③ 화폐성 외화예금을 기말 마감환율로 평가하면서 발생한 외화환산손실",
            "④ 매출채권에 대해 연령분석법을 적용하여 설정한 기말 대손상각비",
            "⑤ 사채를 만기 이전에 조기 상환하면서 발생한 사채상환손실"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 소유주 거래와 비소유주 거래의 분류입니다. 신주 발행 시 액면가 이하로 발행된 할인발행차액은 주주와의 거래(자본거래)의 일부이므로 자본조정(자본차감) 항목에 직접 기재하고 사후 주식발행초과금과 상계 조치할 뿐, 손익계산서 상 당기 비용으로 갈 수 없습니다.\n\n[오답 해설]\n① 유형자산처분이익(영업외수익), ③ 외화환산손실(영업외비용), ④ 대손상각비(판매비와관리비), ⑤ 사채상환손실(영업외비용)은 모두 비소유주와의 거래 및 자산·부채 재측정 결과물이므로 포괄손익계산서 당기 손익에 귀속되어야 합니다.",
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
