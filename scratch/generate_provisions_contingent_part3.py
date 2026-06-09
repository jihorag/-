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
    "item": "5절 우발부채와 우발자산"
}

new_questions = [
    # --- L2 (이해): 5문항 (Q2445 ~ Q2449) ---
    {
        "id": "practice-accounting-ch09s02-L2-36",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-36",
        "year": "",
        "question": "K-IFRS 제1037호에 따라 연대보증 등 공동으로 의무를 부담하는 연대채무 상황에서, 제3자가 이행할 것으로 기대되는 의무 부분에 대한 올바른 회계적 분류 및 보고 방법은?",
        "options": [
            "① 관련 공동보증인의 신용등급이 낮다면 무조건 본문 충당부채로 계상하여야 한다.",
            "② 제3자가 의무를 이행할 것으로 기대되는 부분은 '우발부채'로 처리하여 주석으로 공시한다.",
            "③ 계약 상 공동채무이므로 무조건 전체 금액을 당사의 본문 충당부채로 전액 기장하여야 한다.",
            "④ 당사 지분이 아니므로 주석 공시를 포함하여 일체 공시에서 제외한다.",
            "⑤ 기타포괄손익-공정가치측정금융부채로 지정하여 기말 공정가치 평가를 반영한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1037호 문단 29에 따라, 공동으로 의무를 지는 경우에 이행할 것으로 기대되는 의무의 부분 중 제3자가 이행할 부분은 우발부채로 처리하여 주석으로 공시합니다.\n\n[오답 해설]\n① 공동보증인의 신용도와 상관없이 기본 계약에 따른 제3자 이행 기대분은 우발부채로 공시합니다.\n③ 전체 금액을 당사 본문 부채로 잡는 것은 타인 채무의 무단 인식 오류입니다.\n④ 제3자가 이행하지 못할 경우 당사가 추가 책임을 지게 될 잠재적 리스크이므로 우발부채 공시를 해야 합니다.\n⑤ 금융부채 지정 규정은 충당부채/우발부채의 범위에 해당하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-37",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-37",
        "year": "",
        "question": "K-IFRS 제1037호 하에서 경제적 효익이 유출될 가능성에 따른 회계처리와 공시 요건에 대한 설명 중 가장 옳은 것은?",
        "options": [
            "① 가능성이 '희박(Remote)'한 경우에도 이해관계자의 안전을 위해 반드시 주석으로 공시하여야 한다.",
            "② 가능성이 '높음(Probable)'이지만 신뢰성 있는 측정이 불가능한 경우에는 '우발부채'로 분류하여 주석 공시한다.",
            "③ 가능성이 '가능성 있음(Possible)'인 경우에는 재무상태표 본문에 '우발부채' 계정으로 부채로 계상하여야 한다.",
            "④ 가능성이 '높음(Probable)'이고 신뢰성 있게 금액을 측정할 수 있다면 본문에 '우발부채'로 계상한다.",
            "⑤ 우발자산은 경제적 유입 가능성이 '가능성 있음(Possible)'인 수준부터 주석 공시를 허용한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 경제적 유출 가능성이 높음(Probable)이더라도 금액을 신뢰성 있게 측정할 수 없는 경우에는 충당부채 인식요건을 결여한 것이므로, 본문 부채로 잡지 못하고 '우발부채'로 분류하여 주석으로 공시하여야 합니다.\n\n[오답 해설]\n① 가능성이 희박(Remote)한 우발부채는 주석 공시를 생략할 수 있습니다.\n③ 가능성이 있음(Possible) 수준의 우발부채는 본문 계상이 금지되며 주석 공시 대상입니다.\n④ 높음(Probable)과 측정 가능 요건을 모두 충족하면 '충당부채'로 계상하여야 합니다.\n⑤ 우발자산은 유입 가능성이 '높음(Probable)'인 경우에만 주석 공시하며 그 미만은 공시할 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-38",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-38",
        "year": "",
        "question": "K-IFRS 제1037호에 따른 우발자산(Contingent Asset)의 회계처리에 대한 설명 중 옳은 것은?",
        "options": [
            "① 경제적 효익의 유입 가능성이 높음(Probable)인 경우, 미실현 수익을 예방하기 위해 주석 공시조차 전면 금지된다.",
            "② 경제적 효익의 유입이 거의 확실(Virtually Certain)하여 관련 자산과 수익을 정식 인식한 경우, 해당 자산은 더 이상 우발자산이 아니다.",
            "③ 경제적 효익의 유입 가능성이 희박(Remote)하지 않은 모든 우발자산은 반드시 주석으로 공시하여야 한다.",
            "④ 유입 가능성이 높음(Probable)인 우발자산은 재무상태표 본문에 임시 자산 계정으로 계상할 수 있다.",
            "⑤ 우발자산의 가액을 신뢰성 있게 측정할 수 없다면 유입이 거의 확실하더라도 정식 자산으로 계상할 수 없다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 경제적 효익의 유입이 거의 확실(Virtually Certain)해지면 관련 자산은 더 이상 잠재적 성격의 우발자산이 아니므로, 재무제표 본문에 정식 자산 및 관련 수익으로 인식하는 것이 타당합니다.\n\n[오답 해설]\n① 유입 가능성이 높은(Probable) 우발자산은 주석 공시의 대상이 됩니다.\n③ 우발자산은 가능성이 '높음(Probable)'인 경우에만 주석 공시를 하며 그 미만은 공시 생략합니다.\n④ 유입이 거의 확실하기 전까지는 본문 자산 계상이 전면 금지됩니다.\n⑤ 유입이 거의 확실하다면 본문 자산으로 계상하여야 하며, 확실한 권리이므로 측정 신뢰성이 성립된 것으로 봅니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-39",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-39",
        "year": "",
        "question": "충당부채를 결제하기 위해 필요한 지출의 일부나 전부를 제3자가 변제(Reimbursement)할 것이 확실시되는 상황에 대한 K-IFRS 제1037호의 회계규정 중 옳은 것은?",
        "options": [
            "① 기업이 의무를 이행한다면 제3자가 변제할 것이 거의 확실한(Virtually Certain) 때에만 변제금액을 별도의 자산으로 인식한다.",
            "② 재무상태표 표시 시 변제자산은 관련 충당부채와 직접 상계하여 순액으로 표기하여야 한다.",
            "③ 포괄손익계산서에 충당부채와 관련하여 인식한 비용은 제3자 변제액과 상계하여 표시할 수 없다.",
            "④ 인식하는 변제자산의 금액은 관련 충당부채 금액을 초과하여 인식할 수 있다.",
            "⑤ 제3자가 변제할 가능성이 단지 높음(Probable) 수준이더라도 자산으로 인식할 수 있다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1037호 문단 53에 따라, 충당부채를 결제하기 위한 변제 금액은 기업이 의무를 실제로 결제할 때 제3자가 변제할 것이 거의 확실(Virtually Certain)한 때에만 별도의 자산(미수금 등)으로 인식합니다.\n\n[오답 해설]\n② 재무상태표에서는 변제자산과 충당부채를 상계할 수 없으며 각각 총액으로 구분 표시해야 합니다.\n③ 포괄손익계산서에서는 충당부채 관련 비용과 변제 인식 자원(수익)을 상계하여 표시할 수 있습니다.\n④ 변제자산으로 인식하는 금액은 관련 충당부채 금액을 초과할 수 없습니다.\n⑤ 가능성이 높음(Probable) 수준에 그치면 자산으로 계상할 수 없고 우발자산 주석 검토 대상에 해당합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-40",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-40",
        "year": "",
        "question": "K-IFRS 제1037호 문단 92에 규정된 'Prejudice 예외(편견 또는 중대한 피해 우려)' 상황 하에서 우발부채나 충당부채의 공시를 생략할 때, 기업이 주석에 기재하여야 할 대체 정보 요건으로 가장 옳은 것은?",
        "options": [
            "① 관련 소송이나 분쟁이 종결될 때까지 주석 기재를 완전히 생략하고 아무 흔적도 남기지 않는다.",
            "② 분쟁의 일반적 성격과 함께, 구체적 정보가 공시되지 않은 사실 및 그 사유를 주석에 공시한다.",
            "③ 재무상태표 본문에 임의의 가상 부채 금액을 표기하여 대차가 맞음을 입증하여야 한다.",
            "④ 최대 주주의 향후 사적 손실 보전 약정서를 원본 그대로 첨부하여 공시해야 한다.",
            "⑤ 관련 분쟁 대상 금액을 전액 영업외수익으로 가공 기재하여 경쟁사를 오도한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 극히 예외적으로 관련 정보의 공시가 타방과의 분쟁에서 당사의 지위에 심각한 편견이나 중대한 피해(Prejudice)를 줄 것으로 예상되는 경우, 상세 요건 공시를 생략하되 분쟁의 일반적 성격, 정보가 공시되지 않은 사실 및 사유는 주석에 반드시 남겨야 합니다.\n\n[오답 해설]\n① 아무런 흔적도 남기지 않는 완전 누락은 허용되지 않습니다.\n③ 가상 부채 금액의 본체 계상은 명백한 분개 왜곡입니다.\n④ 주주의 사적 보전 약정은 공시 필수 정보가 아닙니다.\n⑤ 가공 수익 기재는 심각한 분식회계에 해당합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },

    # --- L4 (분석): 1문항 (Q2450) ---
    {
        "id": "practice-accounting-ch09s02-L4-29",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "(주)한국은 진행 중인 손해배상 청구 소송(피고)과 관련하여 연도별로 다음과 같은 패소(자원 유출) 가능성 및 배상금 추정 변경서를 법률대리인으로부터 수취하였다. 기말 결산 시 담당 회계사가 처리한 회계처리의 적정성을 진단할 때, K-IFRS 제1037호 및 제1010호 기준 상 발생한 오류 및 분석으로 가장 옳은 것은? (단, 소송가액은 매년 신뢰성 있게 측정 가능하였다)\n\n| 결산 연도 | 기말 패소 확률 판정 | 담당 회계사의 실제 처리 내용 |\n| :--- | :--- | :--- |\n| 20x1년 말 | 유출 가능성 있음 (35%, Possible) | 재무상태표 본문 부채 미계상 및 주석 공시 생략 |\n| 20x2년 말 | 유출 가능성 높음 (80%, Probable) | 재무상태표 본문에 '소송충당부채 ₩200,000' 계상 및 소송손실 인식 |\n| 20x3년 말 | 소송 최종 기각 판결 확정 (유출 0%) | 대변의 '소송충당부채 ₩200,000'을 제거하고 소송충당부채환입(수익) 인식 |",
        "options": [
            "① 20x1년 말에는 유출 확률이 35%(Possible) 수준이므로 우발부채 주석 공시를 의무적으로 수행했어야 하나 이를 생략(누락)한 오류가 존재하며, 20x2년 말과 20x3년 말의 회계처리는 전진적 확률 변동 및 확정을 적절히 반영한 정합한 처리이다.",
            "② 20x1년 말에 부채를 본문에 계상하지 않은 것 자체가 충당부채 과소 계상 오류이다.",
            "③ 20x2년 말에는 1심 판결 전에 충당부채를 미리 인식한 것이 부채 과대 계상 오류이다.",
            "④ 20x3년 말 소송 기각 시 기존 충당부채를 제거하면서 인식한 환입수익은 이익잉여금 처분오류이므로 전기오류수정손실로 소급 수정하여야 한다.",
            "⑤ 모든 연도의 회계처리는 완벽하게 기준서 요건에 부합하며 어떠한 오류도 존재하지 않는다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 연도별 확률 변화에 따른 부채 인식 및 공시 적정성 분석입니다.\n1) 20x1년 말:\n- 유출 패소 확률 35%(Possible)이므로 본체 부채는 인식하지 않는 것이 맞으나, 유출 가능성이 아주 희박(Remote, 보통 <5%)한 경우가 아니므로 '우발부채'로 반드시 주석 공시를 수행했어야 합니다. 따라서 주석 공시를 생략한 것은 공시 누락 오류입니다.\n2) 20x2년 말:\n- 유출 패소 확률이 80%(Probable)로 격상되었으므로 본체에 충당부채 ₩200,000을 정식으로 설정하고 당기 비용으로 반영한 것은 올바른 회계적 전이 조치입니다.\n3) 20x3년 말:\n- 소송 기각 판결 확정으로 의무가 완전 소멸되었으므로 기존 충당부채를 장부에서 제거하고 당기 손익에 환입수익으로 계상한 처리 또한 정당한 회계추정치 변경의 결과물입니다.\n\n[오답 해설]\n② 20x1년 말에는 가능성이 높음(Probable) 미만이므로 부채 본체 계상 의무가 없습니다.\n③ 충당부채는 확정 판결 전이라도 가능성이 높고 측정이 가능하면 반드시 기결산 시점에 인식하여야 합니다.\n④ 충당부채의 기말 환입은 회계추정 변경의 일환으로 당기손익(환입수익)으로 처리하므로 소급 수정 대상이 아닙니다.\n⑤ 20x1년 말 우발부채 주석 공시 누락 오류가 엄연히 존재하므로 완전 정합 주장은 오답입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 4,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    }
]

questions.extend(new_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Saved database with {len(questions)} questions. Added {len(new_questions)} questions.")
