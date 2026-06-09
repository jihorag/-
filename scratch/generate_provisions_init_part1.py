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
    "item": "1절 충당부채의 인식요건"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q2201 ~ Q2210) ---
    {
        "id": "practice-accounting-ch09s01-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1037호에 따른 '충당부채(Provision)'의 가장 핵심적이고 본질적인 정의로 가장 옳은 것은?",
        "options": [
            "① 지출의 시기나 금액이 확정되어 있어 즉시 결제할 수 있는 금융채무",
            "② 주주총회의 결의를 통해 이익 배당이 완전히 확정된 미지급배당금",
            "③ 지출의 시기나 금액이 불확실한 부채",
            "④ 미래에 발생할 가능성이 전혀 없어 장부에 기재할 수 없는 가상 부채",
            "⑤ 회사의 자산 가치가 하락함에 따라 인식하는 평가 차감 계정"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1037호에 따르면 충당부채는 일반 부채(매입채무 등)와 달리 '지출의 시기나 금액이 불확실한 부채'로 정의됩니다. 비록 불확실성이 존재하나 부채의 정의를 충족하므로 재무상태표 본문에 부채로 계상합니다.\n\n[오답 해설]\n① 지출의 시기와 금액이 확정된 것은 매입채무나 미지급금 등 일반 부채입니다.\n② 미지급배당금은 금액과 시기가 확정된 확정부채입니다.\n④ 충당부채는 발생 가능성이 높아 장부에 기록하는 실재 부채입니다.\n⑤ 자산 평가 차감 계정(대손충당금 등)은 부채가 아닌 자산의 차감 항목입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "K-IFRS 제1037호 상 충당부채를 재무상태표에 부채로 인식하기 위해 '동시에 충족'해야 하는 3대 요건에 해당하지 않는 것은?",
        "options": [
            "① 과거사건의 결과로 현재의무(법제의무 또는 의제의무)가 존재한다.",
            "② 당해 의무를 이행하기 위하여 경제적효익을 갖는 자원이 유출될 가능성이 높다.",
            "③ 당해 의무의 이행에 소요되는 금액을 신뢰성 있게 추정할 수 있다.",
            "④ 의무를 이행해야 하는 최종 만기일이 최초 발행일로부터 1년 이내여야 한다.",
            "⑤ 의무를 회피할 수 있는 무조건적인 권리가 발행자에게 없어야 한다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ K-IFRS 상 충당부채는 장기(비유동부채)와 단기(유동부채) 모두 설정 가능하므로 만기일이 1년 이내여야 한다는 요건은 충당부채 인식 조건에 해당하지 않습니다.\n\n[오답 해설]\n①, ②, ③ 충당부채 인식을 위한 3가지 누적(동시) 충족 요건입니다.\n⑤ 의무를 피할 수 없어야 현재의무에 해당하므로 요건에 부합합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "충당부채의 인식 요건인 '현재의무(Present Obligation)'에 관한 설명 중 가장 옳지 않은 것은?",
        "options": [
            "① 현재의무는 법률이나 계약에 의한 법제의무와, 기업의 과거 행동에 기인한 의제의무를 모두 포함한다.",
            "② 미래에 발생할 것으로 예상되는 영업손실은 과거사건의 결과가 아니므로 현재의무에 해당하지 않는다.",
            "③ 법제화가 아직 완료되지 않은 법률안의 경우에는 어떠한 경우에도 현재의무를 형성할 수 없다.",
            "④ 현재의무가 존재하기 위해서는 기업이 해당 의무의 이행을 회피할 수 있는 실질적인 대안이 없어야 한다.",
            "⑤ 과거사건의 결과로 존재하는 의무만이 현재의무가 되며, 미래의 영업행위와 무관하게 발생한 의무여야 한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 아직 입법안 단계인 법률안이라 하더라도, 법제화가 거의 확실시되어 제정안대로 의무를 이행할 수밖에 없는 수준에 이르렀다면 실질적으로 현재의무가 존재하는 것으로 봅니다.\n\n[오답 해설]\n① K-IFRS 상 현재의무는 법제의무뿐만 아니라 의제의무도 포함합니다.\n② 미래의 영업손실은 현재의무 요건인 과거 사건 성격이 결여되어 충당부채를 잡을 수 없습니다.\n④, ⑤ 현재의무는 회피 대안이 없고 과거사건과 연결되어야 한다는 정석적인 서술입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "기업이 과거의 실무관행, 방침 또는 선언을 통해 제3자에게 해당 의무를 이행하겠다는 의사를 스스로 표명하고, 그 결과 제3자가 기업이 의무를 이행할 것이라는 정당한 기대를 가지게 됨으로써 성립하는 의무를 지칭하는 회계학적 용어는?",
        "options": [
            "① 법제의무 (Legal Obligation)",
            "② 의제의무 (Constructive Obligation)",
            "③ 계약상 의무 (Contractual Obligation)",
            "④ 금융의무 (Financial Obligation)",
            "⑤ 우발의무 (Contingent Obligation)"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 기업의 공표된 정책이나 과거 행동 양식을 통해 채권자나 제3자에게 신뢰 및 기대를 유발하여 형성되는 의무를 '의제의무(Constructive Obligation)'라고 합니다. K-IFRS는 의제의무에 의해서도 충당부채를 잡도록 규정합니다.\n\n[오답 해설]\n① 법제의무는 계약이나 명시적 법률 조항에 근거해야 합니다.\n③ 계약상 의무는 법제의무의 일종입니다.\n④, ⑤ 기준서 상 정식 정의되지 않은 가공의 계정 분류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "다음 중 K-IFRS 기준 상 법률 조문, 명시적 계약 조건, 혹은 법규의 적용에 근거하여 기업에게 법적으로 구속력을 부여하는 의무를 지칭하는 올바른 용어는?",
        "options": [
            "① 법제의무 (Legal Obligation)",
            "② 의제의무 (Constructive Obligation)",
            "③ 도덕적 의무 (Moral Obligation)",
            "④ 자율적 의무 (Voluntary Obligation)",
            "⑤ 관행적 의무 (Customary Obligation)"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 계약서 상 합의 사항이나 소송의 법원 판결, 법령상의 의무화 규정 등 법적 집행력에 기인하는 의무를 '법제의무(Legal Obligation)'라고 부릅니다.\n\n[오답 해설]\n② 의제의무는 법적 구속력은 없으나 사회적/행동적 정당한 기대에 기반합니다.\n③, ④, ⑤ 회계 기준에서 인정하는 정식 구별 범주가 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "과거사건에 의하여 발생하였으나 기업이 전적으로 통제할 수 없는 미래사건의 발생 여부에 의해서만 그 존재가 확인되는 잠재적 의무로, 재무상태표에 부채로 인식할 수 없는 의무를 지칭하는 올바른 명칭은?",
        "options": [
            "① 확정부채",
            "② 충당부채",
            "③ 우발부채 (Contingent Liability)",
            "④ 이연부채",
            "⑤ 선수부채"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 발생 여부가 통제 불가한 우발적인 조건에 묶여 있고, 충당부채의 3대 인식 요건을 충족하지 못하는 잠재적 성격의 의무를 '우발부채(Contingent Liability)'라고 하며, 재무상태표 본문에는 부채로 계상하지 않습니다.\n\n[오답 해설]\n① 확정부채는 부채액과 시기가 고정된 일반 채무입니다.\n② 충당부채는 재무상태표에 부채로 계상하여야 하는 항목입니다.\n④, ⑤ 충당부채 및 우발부채와 구별되는 일반 선급/이연 관련 항목입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "과거사건에 의하여 발생하였으나 기업이 전적으로 통제할 수 없는 불확실한 미래사건의 발생 여부에 의해서만 그 존재가 확인되는 잠재적 자산을 지칭하는 K-IFRS 상의 용어는?",
        "options": [
            "① 이연자산",
            "② 미수자산",
            "③ 우발자산 (Contingent Asset)",
            "④ 무형자산",
            "⑤ 선급자산"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 기업이 온전히 지배하지 못하는 외부 우발사건의 해결로 인하여 경제적 효익의 유입 여부가 확정되는 잠재적 자산 상태를 '우발자산(Contingent Asset)'이라고 합니다.\n\n[오답 해설]\n①, ②, ⑤ 발생이 고정되거나 발생주의로 기인하는 자산 계정입니다.\n④ 특허권이나 개발비 등 실체가 규명된 장기 자산 항목입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "K-IFRS 제1037호에 따라 재무제표의 '주석(Notes) 공시' 대상으로 명시된 우발부채의 범위에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 의무 이행을 위한 자원의 유출 가능성이 극히 희박(Remote)한 경우에만 주석 공시한다.",
            "② 자원의 유출 가능성이 극히 희박(Remote)하지 않은 모든 우발부채는 주석으로 공시하여야 한다.",
            "③ 발생 가능성이 10% 이하인 경우에는 무조건 재무상태표 본문에 직접 기재 공시하여야 한다.",
            "④ 우발부채는 기업 회계에 혼란을 주므로 어떠한 상황에서도 주석 기재를 엄격히 금지한다.",
            "⑤ 회사의 최대주주가 변동될 가능성이 있을 때만 선별하여 공시한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우발부채는 재무상태표 본문에는 부채로 올리지 않지만, 자원의 유출 가능성이 '극히 희박(Remote)'하지 않은 한 재무제표 이용자 정보 공시를 위해 반드시 '주석으로 공시'하도록 규정하고 있습니다.\n\n[오답 해설]\n① 극히 희박한 경우에는 주석 공시를 '생략(면제)'합니다.\n③ 우발부채는 본문 기재를 하지 않습니다.\n④ 주석 공시는 필수적인 공시 수단입니다.\n⑤ 주주 변동과 우발부채 공시는 무관합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "K-IFRS 제1037호 상 우발자산에 대한 재무보고 기준 원칙으로 가장 옳은 것은?",
        "options": [
            "① 경제적 효익의 유입 가능성이 '높지 않아도' 무조건 주석으로 공시하여야 한다.",
            "② 잠재적 이익의 조기 인식을 방지하기 위해 우발자산은 주석 기재를 완전히 배제한다.",
            "③ 경제적 효익의 유입 가능성이 높을(Probable) 때에만 주석으로 공시할 수 있다.",
            "④ 유입 가능성이 극히 희박(Remote)한 경우에 한해 재무상태표에 자산으로 올린다.",
            "⑤ 유입 가능성에 상관없이 최초 취득원가로 평가하여 자본조정의 자산항목으로 올린다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 보수주의 회계 처리 원칙에 따라 우발자산은 인식하지 않으며, 경제적 효익의 유입 가능성이 '높은(Probable)' 경우에 한해서만 주석 공시를 허용합니다. 가능성이 낮거나 보통 수준이면 주석으로도 공시하지 않습니다.\n\n[오답 해설]\n① 가능성이 높을 때만 공시하며 높지 않으면 생략합니다.\n② 가능성이 높을 때는 정보 제공을 위해 주석 공시를 허용하므로 완전 배제는 틀렸습니다.\n④, ⑤ 우발자산은 재무상태표 본문에 올릴 수 없으므로 오답입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "K-IFRS 제1037호 하에서 충당부채 인식 조건인 '자원유출 가능성이 높다(Probable)'는 기준서 상의 수학적 및 정량적 확률 판정 범위로 가장 올바른 것은?",
        "options": [
            "① 발생 확률이 정확히 100%여야 한다.",
            "② 발생 확률이 90% 이상을 초과하는 거의 확실한 상태여야 한다.",
            "③ 발생 가능성이 발생하지 않을 가능성보다 높은 상태, 즉 실질적으로 50%를 초과하는 수준이어야 한다.",
            "④ 발생 가능성이 최소 10% 이상 수준만 충족되면 된다.",
            "⑤ 발생 가능성이 0%보다 큰 임의의 희박하지 않은 수준을 의미한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 기준서 제1037호 문단 23에 따르면, 충당부채의 자원유출 가능성이 높다는 것은 '의무 이행을 위해 자원이 유출될 가능성이 유출되지 않을 가능성보다 높은 경우(More likely than not)'를 뜻하며, 이는 정량적으로 '50% 초과' 수준의 확률 범위를 의미합니다.\n\n[오답 해설]\n①, ② 이는 거의 확실(Virtually Certain) 상태에 가까운 과도한 조건입니다.\n④, ⑤ 발생 가능성이 높다는 수준의 기준에 부합하지 못하는 너무 낮은 임계치입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },

    # --- L2 (이해): 15문항 (Q2211 ~ Q2225) ---
    {
        "id": "practice-accounting-ch09s01-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "다음 중 K-IFRS 상 충당부채(Provision)를 미지급금(Payables)이나 미지급비용(Accrued Expenses)과 같은 일반 채무 부채와 논리적으로 '구분' 짓는 가장 뚜렷한 특징은?",
        "options": [
            "① 미지급금은 지출 시기가 완전 불확실하지만, 충당부채는 지출 시기가 계약 상 정해져 있다.",
            "② 충당부채는 지출의 시기나 금액의 불확실성이 내포되어 있어 상당한 추정이 개입되지만, 미지급금이나 미지급비용은 확정되었거나 추정의 필요성이 거의 없다.",
            "③ 미지급비용은 당기 손익에 영향을 주지 않지만, 충당부채는 당기 손익에만 비용으로 반영된다.",
            "④ 충당부채는 오직 자본조정 항목에서만 차감 기장되는 소액 자본이다.",
            "⑤ 일반 채무는 재무상태표의 자산 섹터에 공시하는 반면, 충당부채는 부채 섹터에만 공시한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 충당부채는 지출의 시기나 금액이 불확실하여 부채 가치 산정 시 합리적이고 주관적인 추정 절차가 깊이 관여합니다. 반면, 매입채무나 미지급금은 청구서 등에 의해 금액과 시기가 확정되어 있고, 미지급비용은 지출 시기가 확정적이고 추정 비율이 극히 낮아 명확한 구분을 보입니다.\n\n[오답 해설]\n① 수식 설명이 정반대로 기재되어 틀렸습니다.\n③, ⑤ 미지급비용도 손익계산서 상 비용과 연동되며, 일반 채무도 부채 영역에 공시되므로 적절치 못합니다.\n④ 충당부채는 자본조정 차감 항목이 아닌 부채입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "충당부채의 성립 요건 중 하나인 '의무발생사건(Obligating Event)'에 대한 설명으로 K-IFRS 기준 상 가장 옳은 것은?",
        "options": [
            "① 기업이 의무를 이행하는 것 외에는 실질적인 대안이 없도록 만드는 과거사건이어야 한다.",
            "② 미래에 발생할 것으로 확정된 이사회의 투자 계획 결의일이다.",
            "③ 주식 배당을 위한 주주 명부의 폐쇄 공고 거래일이다.",
            "④ 기업이 의무를 거부할 경우 정부가 보조금을 지급하는 면제 사건을 뜻한다.",
            "⑤ 발행주식의 시장 주가가 발행일보다 50% 이상 오르는 호재 사건을 말한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 의무발생사건이 되기 위해서는 과거에 일어난 사건의 결과로서, 기업 입장에서 당해 의무를 이행하는 것 외에는 법적 혹은 의무 이행적 실질 대안을 찾을 수 없는 통제 밖의 구속력이 유발되어야 합니다.\n\n[오답 해설]\n②, ③, ⑤ 이사회 결의, 주주명부 폐쇄, 주가 상승 등은 의무발생사건의 정의에 부합하지 않습니다.\n④ 의무 면제 사건은 부채의 소멸 거래를 유발하므로 발생 사건이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "K-IFRS 제1037호 하에서 기업의 '미래 영업손실(Future Operating Losses)'에 대하여 매 연말 결산 시 충당부채를 인식할 수 없는 이론적이고 원리적인 배경으로 가장 옳은 것은?",
        "options": [
            "① 영업손실은 금액이 확정되어 추정이 필요 없기 때문이다.",
            "② 미래 영업손실은 과거사건의 결과로 존재하는 의무가 아니며, 충당부채 인식 조건인 '과거 사건의 결과로서의 현재의무' 성격을 충족하지 못하기 때문이다.",
            "③ 손실이 발생하면 세무서에서 이연법인세자산을 전액 공제 처리해 주기 때문이다.",
            "④ 영업손실은 자본잉여금을 직접 차감시키는 자본 항목이기 때문이다.",
            "⑤ 회사가 미래 영업 방식을 수정하면 손실 자체를 전액 회피할 수 있는 실질적인 대안이 여전히 회사에 남아있기 때문이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 미래의 예상 영업손실은 발생 가능성이 아무리 높더라도 결산일 현재의 '과거사건의 결과물'이 아니며, 현재 시점에서 지출을 종용받는 피할 수 없는 '현재의무'의 정의를 충족하지 못합니다. 따라서 충당부채로 계상할 수 없고, 해당 손실이 예상되는 영업 부문의 자산 손상 평가(자산 감액) 조치로 대응해야 합니다.\n\n[오답 해설]\n① 영업손실은 확정금액이 아닙니다.\n③, ④ 이연법인세 자동 공제설이나 자본잉여금 차감설은 틀린 회계 설명입니다.\n⑤ 미래 영업수정으로 손실을 회피할 가능성은 영업행위의 회피 가능 논리에 부합하나, 본질적인 부채 요건 결여(과거 사건 미성립)가 부채 미인식의 핵심 논거입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "기업이 보유 중인 화학공장의 운영 중 발생한 환경오염 사고에 대해, 기말 결산일 현재 오염 정화를 요구하는 '법률안이 제정되어 통과될 것이 거의 확실하다'고 판단되어 정화충당부채를 인식하고자 한다. 이때 충당부채를 형성하는 실제적인 '의무발생사건'은 무엇인가?",
        "options": [
            "① 공장의 오염 사고 발생 및 그로 인한 오염 행위 자체",
            "② 해당 환경정화 의무화 법률안의 의회 정식 발의 시점",
            "③ 회사가 차기에 정화 장치를 설치하겠다는 투자 계획을 발표한 날",
            "④ 오염 사실을 언론 보도를 통해 최초 보도한 결산일 당일 환율 변동일",
            "⑤ 해당 화학공장의 최초 가동 개시일"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 입법 제정이 거의 확실하여 환경 정화 의무를 피할 수 없게 된 상황에서, 이 의무를 물리적으로 묶는 과거의 실제 의무발생사건은 정화 장치 투자 결의나 법안 발의가 아니라 과거에 실제로 저지른 '공장의 오염 배출 및 사고 행위' 그 자체입니다. 이 배출 행위가 존재하므로 법률 발동 시 피할 수 없는 정화 현금유출 채무가 발생하게 됩니다.\n\n[오답 해설]\n② 법률안 발의 시점은 법제화 진행 단계일 뿐이며,\n③ 정화장치 설치 계획은 미래 행위에 해당하여 회피 가능하므로 의무발생사건이 되지 못합니다.\n④, ⑤ 언론 보도일이나 최초 가동일은 오염 복구 의무의 직접적 발생 시점으로 삼을 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "기업이 특허권 침해 소송의 피고가 되어 연말 결산 시점에 소송이 진행 중인 경우, 법적 분쟁 사건이 현재의무(Present Obligation)를 형성하는지의 여부를 평가할 때 K-IFRS 기준 상 취해야 하는 가장 올바른 판단 프로세스는?",
        "options": [
            "① 소송이 법원에서 최종 판결 종결되어 원화 배상액이 지급 완료될 때까지 평가를 영구 유보한다.",
            "② 기말 현재 이용 가능한 모든 증거(변호사 자문 및 법률 판례 등)를 종합적으로 고려하여, 결산일 현재 기업이 패소하여 의무를 부담할 가능성이 그렇지 않을 가능성보다 높은지(50% 초과 여부)를 평가하여야 한다.",
            "③ 원고(상대방)가 요구한 총 소송 배상 요구액을 전액 금융부채로 즉시 강제 기장한다.",
            "④ 특허권 소송은 무형자산 거래이므로 소송 비용을 무형자산의 취득원가에 가산하고 부채 평가는 면제한다.",
            "⑤ 회사의 대표이사가 면책 선언을 하는 즉시 부채 검토 대상에서 영구 제외한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 미결 소송 등 불확실한 채무 조건 하에서 결산일 현재의 현재의무 존재 여부를 판단할 때에는 법률 전문가의 소송 의견서, 유사 판례 등 입수 가능한 모든 증거를 종합 분석하여, 결산일 현재 의무가 존재할 가능성(패소율)이 50%를 초과하는지를 판단하여 현재의무 유무를 수립합니다.\n\n[오답 해설]\n① 최종 종결 시까지 부채 검토를 방치(유보)하는 것은 기준서 위배입니다.\n③ 상대방의 일방적 청구액을 검토 없이 부채로 기장할 수 없습니다.\n④ 소송에 따른 배상 청구는 자산이 아닌 자원 유출 부채 항목입니다.\n⑤ 경영진의 주관적 기각 의견만으로 회계상 부채 검토를 임의 배제할 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "다음 중 K-IFRS 제1037호 하에서 기업이 보유한 제품보증(Warranty) 정책에 대해 당기 기말 결산 시점에 '충당부채'를 인식해야 하는 타당성 및 논리적 배경으로 가장 옳은 것은?",
        "options": [
            "① 제품보증은 미래에 무상 수리라는 자산 가액의 순증을 주주에게 보상하기 때문이다.",
            "② 제품보증 조건이 명시된 제품을 고객에게 실제 인도 및 판매 완료한 '과거사건(의무발생사건)'이 이미 존재하며, 이에 따라 보증 수리라는 경제적 효익의 유출 가능성이 높고 신뢰성 있는 추정이 가능하기 때문이다.",
            "③ 제품 수리를 실제로 접수하여 수리 작업을 개시하는 당일 전액 당기 비용으로만 종결하도록 유도하기 위함이다.",
            "④ 고객이 소송을 통해 법적 청구 판결을 획득하기 전에는 보증액을 자본조정 예수금으로 묶어야 하기 때문이다.",
            "⑤ 국세청에서 보증 한도 비과세 혜택을 주는 강제 회계 기준이기 때문이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 제품보증 충당부채는 보증 조건부 제품의 인도/판매 완료라는 과거사건의 발생으로 인해 구매 고객들에 대한 정당한 의무가 성립합니다. 따라서 해당 과거사건에 연동되어 향후 발생할 품질 보증비의 유출 가능성이 높고 역사적 경험률로 추정 가능하므로 결산일에 보증충당부채를 기장하는 것이 타당합니다.\n\n[오답 해설]\n① 주주 보상 거래가 아닌 외부 고객과의 채무 정산 거래입니다.\n③ 실제 수리 시점에 비용으로 인식하는 방식(현금주의에 가까움)은 발생주의를 위배한 처리입니다.\n④ 법적 판결 전이라도 의무가 성립하면 충당부채를 계상해야 하며 자본조정 예수금이 될 수 없습니다.\n⑤ 회계 기준은 세법의 비과세 혜택을 시발점으로 설계되지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "임차 중인 매장 건물에 대하여 임차 계약서 상 '임차 기간 종료 시 매장을 원상 복구하여 반환해야 한다'는 강제 원상복구 조건이 포함되어 있는 경우, 복구 의무에 대한 K-IFRS 상의 복합적 인식 분석으로 가장 올바른 것은?",
        "options": [
            "① 임차 기간이 만료되어 실제로 인테리어를 뜯어내는 퇴거일 전에는 부채 계산을 면제받는다.",
            "② 인테리어 시설물을 매장 내부에 실제로 설치하고 훼손하는 '과거사건'의 발생 시점에, 원상 복구해야 하는 법제의무가 현재의무로 성립하므로 충당부채를 인식하고 당해 복구비 현재가치를 자산(유형자산) 원가에 합산하여야 한다.",
            "③ 계약 상 복구 비용은 매달 지급하는 임차료에 포함된 비용이므로 이중 기장을 방지하기 위해 부채에서 전액 제외한다.",
            "④ 복구 비용은 자산 처분 손익의 일부이므로 기타포괄손익누계액의 감액 계정으로 단독 표시한다.",
            "⑤ 복구 의무는 임차인의 전적인 권리이므로 부채가 아닌 무형자산 사용권으로 대변 기재한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 임차 건물 원상복구 의무는 인테리어를 실제 설치하거나 건물을 변형시키는 순간 피할 수 없는 미래 복구 유출액이 성립하게 됩니다. 따라서 설치일 현재 복구 의무(현재의무)를 인식하여 충당부채(복구충당부채)를 적고, 해당 지출의 상대 계정은 자산의 제거 원가로 취급하여 인테리어(유형자산) 취득 원가에 가산한 후 사용 기간 감가상각하여 비용화시킵니다.\n\n[오답 해설]\n① 퇴거일에 일시 비용 처리하는 것은 의무 발생 시점의 부채 계상 원칙에 위배됩니다.\n③ 임차료와 인테리어 복구 의무는 엄연히 별개 계약이므로 자산/부채 이중 기장이 아닙니다.\n④, ⑤ OCI 평가계정이나 사용권 대변 기재 조항 등은 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "피고 소송에서 유리한 국면이 펼쳐져, 원고에게 소송 배상금을 돌려받거나 보상금을 받아낼 가능성이 '거의 확실(Virtually Certain)'한 수준에 도달하였을 때 K-IFRS 상 취해야 하는 올바른 회계적 조치는?",
        "options": [
            "① 여전히 우발자산에 머물러 있으므로 주석으로만 공시한다.",
            "② 잠재적 가치가 실현된 실질적 자산이므로 재무상태표 본문에 '자산(기타수취채권 등)'으로 인식하고, 이에 따른 당기수익을 손익계산서에 반영한다.",
            "③ 자본잉여금 증가 거래로 보아 자본금 계정을 직접 증가시킨다.",
            "④ 보수주의 원칙에 따라 실제 현금이 통장에 유입될 때까지 어떠한 회계 공시나 주석 기재도 전면 유보한다.",
            "⑤ 회사의 무형자산인 영업권에 직접 가산하여 자산 규모를 늘린다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우발자산은 보수주의 관점에서 원칙적으로 자산으로 인식할 수 없으나, 관련 보상의 경제적 효익 유입 가능성이 '거의 확실(Virtually Certain)'한 수준에 도달하여 사실상 불확실성이 소멸되었다면, 이는 더 이상 우발자산이 아닌 확정 자산에 해당하므로 당해 보고기간에 자산과 수익으로 정상 인식하여야 합니다.\n\n[오답 해설]\n① 거의 확실 상태가 되었으므로 주석 공시를 초과하여 본문에 기재해야 합니다.\n③ 자본 거래가 아니므로 자본금 직접 증가 처리를 할 수 없습니다.\n④ 실제 현금 수취일 전이라도 거의 확실 요건 충족 시 발생주의에 의해 자산/수익을 잡아야 합니다.\n⑤ 자산은 영업권이 아닌 미수금 등 금융자산 또는 수취채권으로 분류됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "회사가 이전에 인식한 미결 소송 관련 우발부채에 대하여, 매 결산 시마다 환류를 검토할 때 과거에 '자원유출 가능성이 극히 희박(Remote)'하여 주석 공시도 생략하고 있었으나, 당기에 판세가 뒤집혀 '유출 가능성이 다소 존재(Possible)'하는 상태로 전이되었다. K-IFRS 제1037호에 따른 올바른 후속 회계 조치는?",
        "options": [
            "① 판세가 뒤집혔더라도 과거의 최초 분류를 고수하여 기말 주석 기재를 계속 누락(생략)한다.",
            "② 지출 불확실성이 증가하였으므로 즉시 재무상태표 본문에 충당부채로 즉시 계상한다.",
            "③ 더 이상 가능성이 극히 희박(Remote)하지 않으므로 당기 결산 보고서 주석에 해당 소송 사건과 예상 손실액을 새로이 공시하여야 한다.",
            "④ 소송 관련 상대방 자산의 취득원가에서 이 격차 금액만큼을 차감한다.",
            "⑤ 이사회 결의를 거쳐 자본금의 10%를 긴급 충당금으로 이익 처분 적립한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 우발부채는 상황 변화를 반영하기 위해 기말마다 재검토합니다. 이전에는 자원 유출 가능성이 극히 희박(Remote)하여 공시하지 않았으나, 당기말 시점 검토 시 가능성이 가능성 있음(Possible) 수준 등으로 상승하여 더 이상 Remote하지 않게 되었다면, K-IFRS 공시 규정에 따라 당해 연도 주석에 해당 사실을 새로 기재하여 밝혀야 합니다.\n\n[오답 해설]\n① 상황 변동 시점에는 후속 재평가 후 공시 유형을 리셋해야 하므로 생략을 지속하면 공시 누락 오류가 됩니다.\n② 충당부채는 가능성이 '높아야(Probable; >50%)' 하므로 Possible 수준에서는 본문 인식이 불가합니다.\n④, ⑤ 자산 차감이나 자본 적립 등의 회계처리는 기준 외 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "쌍무계약으로서 계약 당사자 양측이 서로의 의무를 전혀 이행하지 않았거나 의무의 일부만 동일한 정도로 이행한 상태의 계약으로, 일반적인 경우 K-IFRS 제1037호 상 충당부채 설정 대상에서 제외되는 계약을 지칭하는 용어는?",
        "options": [
            "① 미이행계약 (Executory Contracts)",
            "② 금융보증계약",
            "③ 손실부담계약 (Onerous Contracts)",
            "④ 리스변경계약",
            "⑤ 퇴직연금확약"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 쌍무적 의무 거래이나 양측 모두 미이행 상태인 일상적인 계약 상태를 '미이행계약(Executory Contracts)'이라고 합니다. 미이행계약은 계약 체결 자체만으로는 결산일 현재의 과거사건 결과에 따른 현재의무를 형성하지 않는 것으로 보아 원칙적으로 충당부채를 인식하지 않습니다. 단, 당해 계약이 손실부담계약(Onerous Contracts)으로 전환된 예외적인 경우에는 충당부채를 인식합니다.\n\n[오답 해설]\n② 금융보증이나 ④ 리스변경 등은 별도의 고유 기준서 적용 대상 부채입니다.\n③ 손실부담계약은 미이행계약 중 부채를 강제 인식해야 하는 특수 예외 상품입니다.\n⑤ 종업원 퇴직급여 기준서 적용 대상입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "K-IFRS 제1037호에 따라 기업이 사업 일부의 폐쇄, 사업장 이전, 혹은 조직 구조 개편 등 구조조정(Restructuring)을 계획할 때, 결산일에 '구조조정 충당부채'를 장부에 인식하기 위해 갖추어야 하는 구체적인 의제의무 요건으로 가장 옳은 것은?",
        "options": [
            "① 이사회에서 임의로 구조조정을 진행하자는 구두 논의를 마친 날 전액 인식한다.",
            "② 구조조정에 대한 '구체적인 공식 계획'이 수립되어 있어야 하며, 동시에 당해 계획의 이행을 시작하였거나 영향을 받을 당사자들에게 구조조정의 핵심 내용을 공표하여 그들이 정당한 기대를 가지게 한 경우에만 인식한다.",
            "③ 세법에 따른 특별 고용 재난 지원금을 청구하는 당일 전액 환산 반영한다.",
            "④ 실제 구조조정이 완료되어 종업원 퇴직금을 지급 결제 정산 완료한 익년도 말에 인식한다.",
            "⑤ 구조조정 후 회사의 기대이익이 기존 사업 대비 2배 이상 상승할 것이 입증되어야만 한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 구조조정 계획은 경영진 내부 결의만으로는 현재의무를 갖지 못합니다. K-IFRS 기준서에 의거, 대상 사업과 규모, 폐쇄 예정일 등이 확정된 '구체적인 공식 계획(Detailed Formal Plan)'이 수립되어 있고, 결산일 전에 이 계획의 실제 실행에 착수했거나 영향받을 당사자들(해고 종업원, 거래처 등)에게 주요 공표 조치를 완료하여 그들에게 이행에 관한 정당한 기대를 생성시킨 시점에만 '의제의무'가 성립하여 구조조정 충당부채를 인식할 수 있습니다.\n\n[오답 해설]\n① 구두 논의 수준이나 이사회의 단순 내부 승인만으로는 의제의무가 성립하지 않습니다.\n③ 세법상 청구일이나 ⑤ 기대이익 수치 등은 회계상 인식 요건이 아닙니다.\n④ 의무가 발생하는 시점(결산일 전 요건 충족 시)에 인식해야 하므로 퇴거 사후 인식은 이연 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "20x1년 12월 15일, (주)한국의 이사회는 사업 부문의 폐쇄를 결의하고 세부 구조조정 계획을 확정하였다. 그러나 20x1년 12월 31일(기말 결산일) 현재까지 이 계획은 외부 이해관계자나 임직원에게 공표되지 않았고, 실행에도 전혀 착수하지 않았다. 20x1년 말 (주)한국의 구조조정 충당부채 인식 여부에 대한 판단으로 가장 옳은 것은?",
        "options": [
            "① 이사회 승인이 완료되었으므로 전액 충당부채로 계상하여야 한다.",
            "② 결산일 현재 외부 당사자들에게 공표 및 실행 착수가 없었으므로 회사는 구조조정을 철회하거나 임의 변경할 여지가 남아있어 현재의무가 없다. 따라서 충당부채로 계상할 수 없다.",
            "③ 주석으로만 공시하고 본문에는 부채의 50%만을 자본조정 차감으로 적는다.",
            "④ 이사회 결의일은 법제의무의 발생일이므로 금융부채에 단기차입금으로 기재한다.",
            "⑤ 회사의 자산 가치가 하락한 것으로 보아 유형자산 감가상각비를 2배로 계산한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 이사회의 의결 및 계획 확정 조치가 결산일 전에 있었더라도, 당해 사실이 외부에 알려지기 전이라면 기업은 언제든지 이 계획을 취소, 수정할 수 있는 회피 능력을 여전히 가지고 있습니다. 따라서 제3자에게 정당한 기대를 야기하지 못한 상태이므로 의제의무(현재의무)가 성립하지 않아 구조조정 충당부채를 인식할 수 없습니다.\n\n[오답 해설]\n① 내부 승인만으로는 회피 불가능성이 성립하지 않아 부채 분류가 안 됩니다.\n③, ④, ⑤ 임시 자본 기재, 단기차입금 계상, 감가상각비 2배 계상 등은 회계 원칙을 위배한 잘못된 처리입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "충당부채를 청산하기 위해 소요되는 지출의 일부 또는 전부를 제3자(보험회사 등)로부터 보상받을 것이 확실한 경우, 해당 '제3자 보상금(Reimbursement)'에 대한 K-IFRS 상의 정석적인 재무상태표 및 포괄손익계산서 상 기재 방식으로 가장 옳은 것은?",
        "options": [
            "① 보상금은 충당부채 계정에서 직접 상계(차감)하여 순액으로 부채를 재무상태표에 표시하며, 손익계산서 이자도 상계한다.",
            "② 보상금 수취가 거의 확실(Virtually Certain)한 경우에만 보상금 가액을 '별도의 자산(미수금 등)'으로 인식하여 재무상태표에 표시하며, 이때 인식할 자산 가액은 관련 충당부채 장부금액을 초과할 수 없다.",
            "③ 보상받을 것이 확실하면 충당부채 설정을 전액 면제받고 자본조정의 가산 항목으로만 남긴다.",
            "④ 보상금은 우발자산에 준하여 어떠한 경우에도 자산으로 올릴 수 없고 무조건 주석으로만 공시한다.",
            "⑤ 회사의 자본금 계정에 주식발행초과금으로 대변에 직접 가산한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1037호 문단 53에 따라 충당부채 지출 보상금은 수취가 거의 확실(Virtually Certain)해진 시점에만 별도의 자산으로 인식합니다. 이때 자금의 유입 성격은 채권 거래이므로 부채에서 직접 깎아 순액 표시하는 것을 금지하며, 인식하는 보상 자산의 크기는 대응하는 충당부채 부채액을 초과할 수 없습니다. (단, 포괄손익계산서 상에서 비용과 관련 수익을 상계하여 순액 보고하는 것은 허용됩니다.)\n\n[오답 해설]\n① 재무상태표 상의 부채액 직접 차감(상계)은 부채의 축소 왜곡을 방지하기 위해 엄격히 금지됩니다.\n③ 부채 설정의 강제 면제 조항은 없습니다.\n④ 유입이 거의 확실하면 우발자산 단계를 넘어서 자산으로 계상하여야 합니다.\n⑤ 자본잉여금 증가 거래가 아닌 영업외 자산/수익 거래입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "정부의 새로운 소방 법안의 도입으로, (주)한국은 영업 중인 물류 창고에 법률적 의무 기준에 부합하는 소방 스프링클러 장치를 차기 연도 내에 반드시 설치하여야 한다. 설치하지 않을 경우 거액의 과태료 및 영업정지 처분을 받게 된다. 20x1년 말 현재 (주)한국의 스프링클러 설치 비용에 대한 충당부채 계상 여부 판단으로 가장 옳은 것은?",
        "options": [
            "① 법률 조문에 강제된 법제의무에 속하므로 설치예상액을 기말 충당부채로 반드시 계상한다.",
            "② 스프링클러 설치는 회사가 물류 창고 영업을 중단하거나 처분함으로써 최종적으로 회피할 수 있는 미래 행위이다. 따라서 결산일 현재 피할 수 없는 현재의무가 아니므로 충당부채를 계상할 수 없다.",
            "③ 설치비의 50%만을 영업외비용으로 계상하고 나머지는 무형자산에 가산한다.",
            "④ 물류창고는 비유동자산이므로 해당 예상액을 전액 감가상각누계액으로 직접 대변 가산한다.",
            "⑤ 회사의 자본금 계정에서 주식발행초과금을 감액하는 차변 분개로 종결한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 기준서에 의하면, 법령 등의 강제로 인해 향후 지출이 예상되더라도, 당해 지출을 유발하는 활동(예: 물류창고 영업의 지속) 자체를 기업이 중단하거나 영업 방식을 수정하여 피해갈 수 있다면, 이는 과거사건에 기인한 피할 수 없는 '현재의무'에 해당하지 않습니다. 따라서 스프링클러 설치 예정비는 기말에 부채로 계상하지 않고, 향후 설치가 실제 완료되는 시점에 유형자산 등으로 원가 인식하여 상각합니다.\n\n[오답 해설]\n① 법률 강제가 예정되어 있더라도 회사의 미래 의사에 따라 회피 가능하므로 부채 요건 결여입니다.\n③, ④, ⑤ 임시 비용화, 감가상각누계액 가산, 자본잉여금 감액 등은 기준에 위배되는 자의적 처리입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s01-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "K-IFRS 제1037호에 따라 구조조정 충당부채를 기말에 인식하기에 앞서, 구조조정에 포함되는 개별 사업부 자산(기계장치 등)에 대하여 기업이 선행하여 이행하여야 하는 올바른 회계적 평가 절차는?",
        "options": [
            "① 개별 자산의 장부금액을 최초 취득원가로 소급 환원하여 감가상각을 원점 취소한다.",
            "② 해당 구조조정 대상 사업부의 자산에 대하여 K-IFRS 제1036호 '자산손상' 기준서를 적용하여, 손상평가를 수행하고 손상차손을 먼저 장부에 인식하여야 한다.",
            "③ 개별 자산의 잔존가치를 전액 ₩0으로 감액하여 기말 자본을 직접 깎아낸다.",
            "④ 자산 임의 매각이 완료될 때까지 평가 보고서의 작성을 전면 중단한다.",
            "⑤ 개별 유형자산의 대변 잔액을 이익잉여금 처분계산서의 임의적립금 환입에 대응 기재한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1037호 문단 71에 의하면, 기업이 구조조정 관련 충당부채를 최종적으로 결정 및 인식하기 전에, 구조조정 계획에 포함되어 있는 사업부의 자산(유형/무형자산 등)에 대하여 반드시 '자산손상평가'를 먼저 선행하여 수행하고, 자산 손상이 확인되면 손상차손을 우선적으로 회계 기장하여 자산 장부를 정리하여야 합니다.\n\n[오답 해설]\n① 상각 원점 취소는 상각후원가 평가 원칙에 위배됩니다.\n③ 잔존가치를 자의적으로 ₩0으로 밀어 감액하는 것은 손상 평가 기준 외 편법입니다.\n④ 자산 매각 전이라도 기말 보고기간 기준 손상 징후 검토는 즉각 시행되어야 합니다.\n⑤ 유형자산의 손익을 자본 이익잉여금 환입에 연동시킬 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    }
]

# Add to database
for q in new_questions:
    questions.append(q)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Saved database with {len(questions)} questions. Added {len(new_questions)} questions.")
