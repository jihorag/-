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
    "item": "2절 충당부채의 추정"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q2251 ~ Q2260) ---
    {
        "id": "practice-accounting-ch09s02-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1037호에 따른 충당부채 측정 시 '최선의 추정치(Best Estimate)'에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 경영진이 손실 보고를 최소화하기 위해 주관적으로 선택한 최저 지출 금액",
            "② 발생 가능한 모든 지출 금액 중에서 세후 법인세 효과를 가장 크게 적용한 금액",
            "③ 보고기간 말 현재 의무를 이행하거나 제3자에게 이전하기 위해 합리적으로 지불해야 하는 세후 금액",
            "④ 보고기간 말 현재 현재의무를 이행하는 데 소요되는 지출에 대한 합리적인 추정치",
            "⑤ 기업의 영업 비밀 보호를 위해 소송 배상금 최고액의 50%로 일괄 계상한 금액"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ K-IFRS 제1037호에 따르면 충당부채로 인식할 금액은 현재의무를 보고기간 말에 이행하거나 제3자에게 이전하는 데 소요되는 지출에 대한 최선의 추정치여야 합니다.\n\n[오답 해설]\n① 경영진의 주관적이고 자의적인 최소 금액은 최선의 추정치가 아닙니다.\n②, ③ 충당부채는 세후가 아닌 세전 개념을 기준으로 측정합니다.\n⑤ 배상 최고액의 50%로 일괄 계상하는 것은 합리적인 추정 방식이 아닙니다.",
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
        "question": "K-IFRS 제1037호 상 측정 대상 충당부채가 단 하나의 의무(Single Obligation, 예: 대형 단일 소송)로 구성되어 있는 경우, 최선의 추정치를 도출하는 가장 적절한 기준은 무엇인가?",
        "options": [
            "① 발생 가능한 모든 결과의 금액을 단순 산술평균한 금액",
            "② 발생 가능성이 가장 낮은 결과의 예상 지출 금액",
            "③ 개별적으로 가장 발생 가능성이 높은 단일의 결과",
            "④ 기댓값과 최빈값 중 기업에게 유리한 낮은 쪽 금액",
            "⑤ 법원에 기탁할 공탁금 중 이자 상당액"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1037호 문단 40에 따르면, 측정 대상이 단일의 의무인 경우 최선의 추정치는 개별적으로 가장 발생 가능성이 높은 단일의 결과(즉, 최빈값/Most Likely Outcome)가 됩니다.\n\n[오답 해설]\n① 단일 의무 측정 시 단순 산술평균이나 기댓값 가중평균은 최선의 추정치가 되지 않는 경우가 많습니다.\n② 발생 가능성이 가장 낮은 결과는 최선의 추정이 아닙니다.\n④ 낮은 쪽을 유리하게 선택하는 것은 중립성에 위배됩니다.\n⑤ 공탁금 이자당당액은 충당부채 추정 기준이 아닙니다.",
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
        "question": "K-IFRS 제1037호에 따라 충당부채를 측정할 때, 측정 대상이 수많은 제품보증 의무와 같이 다수의 항목으로 구성된 모집단(Large Population of Obligations)인 경우 최선의 추정치를 도출하는 올바른 방식은?",
        "options": [
            "① 개별적으로 가장 발생 가능성이 높은 단일의 결과에 총 항목 수를 곱한 금액",
            "② 발생 가능한 모든 결과의 금액을 각각의 확률로 가중평균한 '기댓값(Expected Value)'",
            "③ 가장 보수적인 관점에서 최대 손실액만을 단순 합산한 금액",
            "④ 최소 지출이 예상되는 최빈값을 모집단 전체에 일괄 배분한 가액",
            "⑤ 회사의 잔여 자산 범위 내에서 주주총회가 매 결산기마다 결의한 한도액"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 다수의 항목으로 구성된 모집단(예: 제품 보증)의 경우, 의무와 관련된 자원의 유출 가능성은 발생 가능한 모든 결과와 그에 대응하는 확률을 고려한 '기댓값(Expected Value)'을 사용하여 추정합니다.\n\n[오답 해설]\n① 단일의 최빈값에 총 항목 수를 곱하는 것은 다수 모집단의 기댓값 모형에 어긋납니다.\n③ 최대 손실액만 단순 합산하는 것은 부채를 과도하게 부풀리는 과대계상에 해당합니다.\n④ 최빈값을 일괄 배분하는 것은 기댓값 방식이 아닙니다.\n⑤ 주주총회의 임의 결의 한도액은 기준서 상의 합리적 추정 방법이 아닙니다.",
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
        "question": "K-IFRS 제1037호에 따른 충당부채의 측정 시, 관련 자산의 예상 처분이익(Expected Disposal of Assets)에 대한 올바른 회계적 처리 원칙은?",
        "options": [
            "① 충당부채를 측정할 때 자산의 예상 처분이익은 고려하지 아니한다.",
            "② 자산의 예상 처분이익이 거의 확실시되면 충당부채에서 즉시 차감하여 순액으로 공시한다.",
            "③ 예상 처분이익의 기댓값만큼 충당부채를 감액하고 차액을 기타포괄손익으로 분류한다.",
            "④ 예상 처분이익은 전액 이연법인세부채의 계상액에 직접 가산하여 부채를 줄인다.",
            "⑤ 자산 처분이익이 예상되더라도 충당부채 총액을 10% 할증하여 본문에 기록한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1037호 문단 51에 따르면, 자산의 예상 처분이익은 충당부채를 측정할 때 고려하지 않습니다. 처분이익을 유발하는 사건은 별개의 거래이므로 충당부채의 지출 의무액을 낮추는 상계 요인으로 삼을 수 없습니다.\n\n[오답 해설]\n②, ③, ④ 예상 처분이익은 충당부채 금액에서 직접 차감, 감액, 상계하거나 이연법인세에 직접 조정하지 않습니다.\n⑤ 10% 강제 할증 역시 규정에 없는 자의적인 처리입니다.",
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
        "question": "K-IFRS 제1037호에 따라 충당부채의 시간가치를 할인할 때 적용하여야 하는 '할인율(Discount Rate)'의 요건에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 기업의 당기 가중평균자본비용(WACC) 중 세후 이자율을 사용해야 한다.",
            "② 화폐의 시간가치에 대한 현 시장의 평가와 부채 특유의 위험을 반영한 세후(Post-tax) 이자율을 사용해야 한다.",
            "③ 향후 납부할 세금 혜택을 차감한 실질 복합 명목이자율을 사용해야 한다.",
            "④ 국세청이 매년 정하는 표준 비과세 이자율을 강제 준용해야 한다.",
            "⑤ 화폐의 시간가치에 대한 현 시장의 평가와 부채 특유의 위험을 반영한 세전(Pre-tax) 이자율을 사용해야 한다."
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ K-IFRS 제1037호 문단 47에 따르면, 할인율은 화폐의 시간가치에 대한 현 시장의 평가와 부채 특유의 위험을 반영한 세전(Pre-tax) 이자율이어야 합니다. 또한 이 할인율은 미래 현금흐름을 추정할 때 고려된 위험을 반영해서는 안 됩니다.\n\n[오답 해설]\n①, ② 충당부채의 할인율은 세후(Post-tax)가 아닌 세전(Pre-tax) 이자율을 사용합니다.\n③, ④ 명목 WACC나 표준 세법 이자율 등은 기준서 상의 올바른 할인율 기준이 아닙니다.",
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
        "question": "매 연말 결산 시 충당부채의 장부금액을 관리할 때 적용하여야 하는 '충당부채의 재검토 및 조정'에 관한 K-IFRS 제1037호의 설명으로 가장 옳은 것은?",
        "options": [
            "① 충당부채는 최초 인식 후 만기 시까지 어떠한 추가 조정이나 remeasurement도 할 수 없다.",
            "② 최초 기장 시점의 할인율을 만기까지 강제 적용하여 평가하여야 한다.",
            "③ 충당부채는 보고기간 말마다 잔액을 검토하고, 보고기간 말 현재 최선의 추정치를 반영하여 조정하여야 한다.",
            "④ 시장 이자율이 변동되더라도 환율 변동 외에는 조정 분개를 기장할 수 없다.",
            "⑤ 회사의 영업 이익이 하락하면 충당부채를 자본조정 항목으로 강제 이체해야 한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1037호 문단 59에 따라 충당부채는 매 보고기간 말마다 잔액을 검토하고, 보고기간 말 현재 최선의 추정치를 반영하여 재조정하여야 합니다.\n\n[오답 해설]\n① 충당부채는 보고기간 말에 의무 발생 변동에 따라 수시로 변동됩니다.\n②, ④ 보고기간 말 현재의 할인율 및 현금흐름 추정치 변경 사항을 반영하여 재조정합니다.\n⑤ 영업이익 하락 시 자본조정으로 부채를 강제 이체하는 회계처리는 인정되지 않습니다.",
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
        "question": "이전에 설정해 둔 충당부채에 대하여, 당기말 검토 시 '의무이행을 위하여 경제적 효익을 갖는 자원이 유출될 가능성이 더 이상 높지 않게 된 경우'에 취해야 하는 올바른 회계처리는?",
        "options": [
            "① 부채를 그대로 둔 채 매기 5%씩 감액 감가상각한다.",
            "② 해당 충당부채를 환입(차감 또는 당기이익) 처리하여 제거한다.",
            "③ 제거 시 대차대조표 상 자산총계를 동일액만큼 부풀려 잔액을 상쇄시킨다.",
            "④ 주주들에게 긴급 배당 재원으로 적립 전환 결의를 한다.",
            "⑤ 금융위원회에 보고한 후 당기 기타포괄손익으로 영구 자본화한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1037호 문단 59에 따라, 의무를 이행하기 위하여 경제적 효익이 내재된 자원이 유출될 가능성이 더 이상 높지 않게(Probable하지 않게) 된 경우에는 관련 충당부채 잔액을 환입하여 감액 제거합니다.\n\n[오답 해설]\n① 부채는 감가상각 대상 자산이 아닙니다.\n③ 자산을 허위로 부풀려 상쇄하는 것은 분식회계에 해당합니다.\n④, ⑤ 자본잉여금 적립이나 기타포괄손익 영구 자본화 처리는 틀린 처리입니다.",
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
        "question": "K-IFRS 제1037호에 따라 의무 이행에 소요될 지출 금액을 추정할 때, 미래에 예상되는 미래사건(예: 기술 진보, 법률 제정 예정 등)의 영향을 반영할 수 있는 필수 조건은?",
        "options": [
            "① 미래사건이 발생할 것이라는 충분하고 객관적인 증거가 있는 경우",
            "② 경영진이 미래사건이 유리하게 발생할 것이라고 주관적으로 굳게 믿는 경우",
            "③ 동종 업계의 타 기업이 그러한 미래사건의 혜택을 이미 공표한 적이 있는 경우",
            "④ 국세청 세법 개정안의 예비 심사가 1단계 통과된 상태인 경우",
            "⑤ 회사의 자본금이 100억 원 이상으로 자본 건전성이 높은 경우"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1037호 문단 48에 따르면, 의무를 이행하기 위하여 소요되는 지출에 영향을 미칠 수 있는 미래사건은 그러한 사건이 발생할 것이라는 '충분하고 객관적인 증거'가 있는 경우에만 충당부채 추정치에 반영합니다.\n\n[오답 해설]\n② 경영진의 주관적이고 막연한 기대나 신념만으로는 미래사건의 영향을 반영할 수 없습니다.\n③ 경쟁사의 공표 사항이 객관적인 증거를 대신할 수는 없습니다.\n④, ⑤ 세법 예비 심사나 자본금 규모 등은 기준서 상의 미래사건 반영 객관적 증거 요건이 아닙니다.",
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
        "question": "K-IFRS 제1037호에 따라 복구충당부채 등의 현재가치 평가를 위해 적용했던 '할인의 효과'를 매 결산기마다 시간 경과에 따라 해제(Unwinding)할 때, 차변에 계상할 올바른 계정 명칭은?",
        "options": [
            "① 이자비용 (금융원가)",
            "② 영업비용 (복구수선비)",
            "③ 기타포괄손익 (FVOOCI 평가손실)",
            "④ 감가상각누계액 차감계정",
            "⑤ 이익잉여금 직접차감액"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 할인의 현재가치 영향이 중요하여 부채를 현재가치로 평가한 경우, 시간 경과에 따라 충당부채의 장부금액이 증가(할인 해제)하는 부분은 기간 비용 성격인 '이자비용(또는 차입원가/금융원가)'으로 인식하여 손익계산서에 반영합니다.\n\n[오답 해설]\n② 복구수선비나 기타 영업비용이 아닌 금융비용(이자비용)으로 인식합니다.\n③ OCI 자본 차감 처리가 아닙니다.\n④ 감가상각누계액 차감 계정이 아닙니다.\n⑤ 자본(이익잉여금) 직접 차감 처리가 불가능합니다.",
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
        "question": "K-IFRS 제1037호 상 충당부채를 청산하기 위해 필요한 지출의 일부나 전부를 제3자가 변제(Reimbursement, 예: 보험 보상금 등)할 것이 예상되는 경우, 이에 대한 올바른 회계처리 및 인식 한도 규정은?",
        "options": [
            "① 변제받을 금액이 '유출 가능성이 높음' 이상이면 충당부채를 즉시 전액 상계 차감한다.",
            "② 변제받을 금액은 부채 총액을 초과하여 최대 2배까지 자산으로 중복 인식할 수 있다.",
            "③ 변제 금액은 기업이 의무를 이행할 때 변제받을 것이 거의 확실한(Virtually Certain) 경우에만 자산으로 인식하며, 그 자산의 인식금액은 관련 충당부채 금액을 초과할 수 없다.",
            "④ 변제 가액은 무조건 자본잉여금에 가산하고 법인세 공제를 전액 면제받는다.",
            "⑤ 변제가 예정되어 있다면 결산서 상 충당부채 자체의 기장을 영구 면제(생략)한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 제3자 변제 자산(보상 미수금 등)은 의무 이행 시 변제받을 것이 '거의 확실(Virtually Certain)'한 경우에 한해 별도의 자산으로 인식합니다. 또한 이 자산의 인식 금액은 관련 충당부채 계상액을 한도로 설정되므로 부채액을 초과하여 잡을 수 없습니다.\n\n[오답 해설]\n① '거의 확실' 상태여야 하며, 충당부채와 직접 상계하여 순액으로 표기하지 않습니다 (총액 보고 원칙).\n② 부채 한도 범위 내로 자산 가액이 묶이므로 초과 인식은 불가능합니다.\n④ 자본 거래가 아니므로 자본잉여금이 될 수 없습니다.\n⑤ 변제 여부와 무관하게 충당부채 요건 충족 시 부채 기장은 필수입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },

    # --- L2 (이해): 15문항 (Q2261 ~ Q2275) ---
    {
        "id": "practice-accounting-ch09s02-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "K-IFRS 제1037호에서 충당부채의 시간가치 할인 시 적용하는 할인율을 '세후(Post-tax) 이자율'이 아닌 '세전(Pre-tax) 이자율'로 강제 규정한 논리적이고 이론적인 주된 이유로 가장 옳은 것은?",
        "options": [
            "① 세후 이자율을 사용하면 충당부채 계상액이 너무 작아져 보수주의에 위배되기 때문이다.",
            "② 충당부채의 할인 시점과 세금 효과 반영 시점을 동일하게 일치시키면 세액공제가 중복 취소되기 때문이다.",
            "③ 충당부채의 세금 효과(법인세 영향)는 K-IFRS 제1012호 '법인세' 기준서에 따라 별도로 평가되어 반영되므로, 이자율 평가 과정에서 세금 효과를 중복으로 차감하는 이중 계산(Double Counting)을 방지하기 위함이다.",
            "④ 세후 이자율을 계산하려면 시장 전체의 가중평균이자율을 매시간 역산해야 하므로 계산이 불가능하기 때문이다.",
            "⑤ 국세청에서 세전 이자율 적용 시에만 이자비용을 전액 손금산입해 주는 규정을 두고 있기 때문이다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 충당부채의 세금 효과(일시적차이 및 이연법인세 등)는 법인세회계 기준서인 K-IFRS 제1012호에 따라 이연법인세자산/부채 등을 별도로 측정하게 됩니다. 따라서 충당부채 할인율에도 세금 효과를 차감한 세후 할인율을 대입하면 세금 영향이 이중으로 왜곡 계상(이중 고려)되므로, 반드시 할인율은 세전(Pre-tax) 상태를 적용하여야 합니다.\n\n[오답 해설]\n① 할인율이 작아지면 현재가치 부채액은 커지므로 원리 설명이 반대입니다.\n② 중복 취소 논리는 세금 효과 이중 계상과 구별됩니다.\n④ 세후 이자율 산출 자체가 불가능하다는 주장은 실무적으로 타당하지 않습니다.\n⑤ 회계 기준은 세법의 손금산입 혜택 요건에 구속되어 논리가 수립되지 않습니다.",
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
        "question": "K-IFRS 제1037호 하에서 충당부채의 최선의 추정치를 반영할 때 요구되는 '위험과 불확실성(Risks and Uncertainties)'에 관한 설명 중 가장 옳지 않은 것은?",
        "options": [
            "① 불확실성이 존재하므로 자산이나 부채를 고의로 과대 또는 과소평가하여 고의적인 비자금 적립을 유도할 수 있도록 조장한다.",
            "② 충당부채의 최선의 추정치를 도출할 때는 많은 사건과 상황을 둘러싸고 있는 위험과 불확실성을 충분히 고려해야 한다.",
            "③ 불확실성 하에서 판단할 때 자산이나 수익이 과대평가되지 않고 부채나 비용이 과소평가되지 않도록 주의(Caution)를 기울여야 한다.",
            "④ 불확실성 하에서의 신중한 판단이 충당부채를 자의적으로 과대계상하거나 고의로 부채를 부풀리는 것까지 정당화해 주지는 않는다.",
            "⑤ 위험을 고려하여 미래 예상 지출액을 상향 조정(Risk Adjustment)하는 조치가 동반될 수 있다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS는 불확실성을 이용하여 고의적으로 재무상태를 왜곡하거나 부채를 허위로 부풀려 비밀적립금(비자금)을 쌓는 행위를 엄격히 금지합니다. 중립성과 신뢰성 있는 재무 정보 공시가 회계 기본 원칙입니다.\n\n[오답 해설]\n②, ③, ⑤ 불확실성을 신중하게 반영하여 비용과 부채 누락을 예방해야 한다는 정론입니다.\n④ 신중성(보수주의)이 자의적인 부채 과대계상(Earnings Management)을 의미하는 것은 아닙니다.",
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
        "question": "충당부채의 최선의 추정치를 산정할 때, 미래 현금흐름의 위험조정(Risk Adjustment)이 발생할 수 있다. 이때 기준서 상 경계해야 하는 '이중 조정(Double Counting) 오류'의 핵심 내용을 가장 올바르게 지적한 것은?",
        "options": [
            "① 미래의 현금흐름 추정치에 위험조정을 가한 경우, 시간가치 할인을 위한 할인율에 대해서는 동일한 위험 요소를 가산(조정)해서는 아니 된다.",
            "② 현금흐름과 이자율 모두에 10%의 고정 가중치를 곱하여 두 번 계산해야 부채가 정확해진다.",
            "③ 물가상승률과 환율 변동 효과를 동시에 감안하여 동일 사건을 자산에 두 번 적립하는 경우를 뜻한다.",
            "④ 할인율을 세전 상태와 세후 상태 두 가지로 별도 산정하여 합산해 기장하는 오류이다.",
            "⑤ 충당부채 계정 대변 잔액을 차변의 자산제거원가와 동일하게 두 번 기장하는 이중 전기를 말한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 충당부채 평가 시 미래의 불확실한 지출 현금유출액 자체에 위험 조정률을 반영하여 지출 추정치를 상향해 두었다면, 할인율(세전 이자율)을 선택할 때는 해당 부채 특유의 위험에 대해 중복하여 할증(조정)해서는 안 됩니다. 즉, 위험 조정은 분자(현금흐름)나 분모(할인율) 중 단 한 번만 반영되어야 이중 고려 오류를 피할 수 있습니다.\n\n[오답 해설]\n② 이중 가산(두 번 계산)은 전형적인 이중 계산 왜곡 오류입니다.\n③, ⑤ 물가상승/환율이나 이중 전기에 관한 설명은 위험의 이중 계상 논점과 다른 설명입니다.\n④ 할인율 세전/세후 이중 기장은 원리상 발생할 수 없는 가공의 서술입니다.",
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
        "question": "K-IFRS 제1037호 하에서 충당부채 측정 시 '예상되는 자산의 처분이익'을 차감 상계하지 않고 별개의 독립적인 사건으로 규정한 보수주의적이고 발생주의적인 회계 논거로 가장 옳은 것은?",
        "options": [
            "① 처분이익은 기업 내부의 주관적인 기대일 뿐이며, 부채 결제 의무라는 '현재의 채무 계약 관계'에 법적인 상계권이 존재하지 않기 때문이다.",
            "② 자산 처분은 법인세를 면제받는 거래이므로 상계를 하면 부채가 이중으로 줄어들기 때문이다.",
            "③ 자산의 가액이 하락하면 처분손실이 되어 부채가 강제로 늘어나기 때문이다.",
            "④ 예상 처분이익은 자본잉여금으로 분류되어 부채의 대변 계정에 섞일 수 없기 때문이다.",
            "⑤ 충당부채는 영업외비용이고 자산 처분은 영업이익이어서 손익 항목이 꼬이기 때문이다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 미래 지출 의무인 충당부채는 과거 거래 결과 피할 수 없는 부채 의무입니다. 반면, 동 거래와 우연히 결합되어 있는 자산의 처분(예: 철거 과정에서 고철 기계 장치 매각 등)은 불확실한 별개의 매각 거래이며 부채 계약 당사자와의 법적 상계 계약이 존재하지 않습니다. 따라서 이를 부채에서 먼저 차감하는 상계는 허용하지 않습니다.\n\n[오답 해설]\n② 처분 거래 법인세 면제설은 틀린 지문입니다.\n③ 자산 하락이 부채 직접 증가로 연결된다는 주장은 맞지 않습니다.\n④ 예상 처분이익은 자본잉여금이 아닙니다.\n⑤ 계정 과목의 영업/영업외 성격 때문에 상계를 금지하는 것이 아니라 거래의 독립성 때문입니다.",
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
        "question": "공장의 폐기물 복구의무와 관련하여, 기말 시점에 신기술 개발(예: 오염 처리 로봇 상용화)에 따라 향후 원상 철거 시점의 복구 비용이 대폭 절감될 것으로 예상되어 이를 복구충당부채 계산에 선반영하고자 한다. K-IFRS 상 이러한 '미래사건'의 영향을 추정치에 적용하기 위해 필요한 '충분하고 객관적인 증거'의 예시로 가장 적절한 것은?",
        "options": [
            "① 회사의 대표이사가 사내 주간 회의에서 해당 기술을 신속 도입하자고 독려한 회의록",
            "② 해당 오염 정화 신기술이 공인 연구 기관에 의해 검증되고 실제 현장 테스트 데이터가 존재하며, 사용 가능한 시점이 객관적으로 도출되는 경우",
            "③ 동종 업계의 경쟁사가 유사한 기술을 도입하기로 홈페이지에 홍보 포스터를 게재한 사실",
            "④ 신기술 개발 시 정부 보조금이 지급될 것이 거의 확실하다는 언론 기사 한 건",
            "⑤ 회사의 자금 상황이 넉넉하여 내년에 기술 연구소를 신축할 예정이라는 이사회 결의문"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 기준 상 미래사건의 영향(예: 기술 진보 등)을 반영하기 위해서는 단순 구두 계획이나 추정이 아니라, 공인된 성능 검증, 실제 가동 테스트 등 충분한 객관적 증거와 그 실현 시기가 타당하게 검증되어 증빙으로 제시되어야 합니다.\n\n[오답 해설]\n① 경영진의 구두 독려나 ③ 경쟁사 포스터는 충분한 객관적 증거가 될 수 없습니다.\n④ 신문 기사나 ⑤ 연구소 신축 예정 이사회 결의 등은 기술의 실질적인 유효성 및 원가 절감에 관한 직접적 객관 증거로 미흡합니다.",
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
        "question": "기업이 보고기간 말마다 충당부채의 잔액을 재검토(Reassessment)할 때, 시장 이자율 등 시장의 위험 평가가 전반적으로 수정되어 적용 할인율이 변동되었다. K-IFRS 제1037호에 따른 올바른 기말 부채 재측정 조치는?",
        "options": [
            "① 할인율 변동은 최초 기장된 부채 가액에 소급 조정해야 하므로 20년 전 최초 결산서를 수정 재작성한다.",
            "② 할인율 변동은 재무보고의 질적 유용성을 저해하므로 차기 만기 상환 전에는 변경 적용을 전면 금지한다.",
            "③ 보고기간 말 현재 변경된 세전 이자율을 적용하여 충당부채 현재가치를 다시 측정하고, 장부금액과의 격차를 반영하여 당기 충당부채 잔액을 업데이트한다.",
            "④ 할인율이 하락하더라도 당기 부채 총량을 임의로 줄이는 환입 조치는 할 수 없다.",
            "⑤ 격차 전액을 기타포괄손익누계액의 자본 잉여 항목에만 기재하고 부채 잔액은 그대로 고정한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 충당부채는 매 보고기간 말마다 잔액을 최선의 추정치로 재조정하므로, 시장 할인율이 변동한 경우 당기말 현재의 업데이트된 세전 이자율을 새 할인율로 삼아 현재가치를 재계산하고 그 조절분을 부채에 반영하여야 합니다.\n\n[오답 해설]\n① 소급하여 과거 20년 전 재무제표를 수정 재작성하는 대상이 아닙니다 (회계추정의 변경으로 전진 적용).\n② 할인율 업데이트는 기말 평가 시 필수 수행 조건입니다.\n④ 이자율 변동이나 추정 가치 변동으로 부채가 감소 시 환입 처리가 정당합니다.\n⑤ OCI 자본 항목이 아닌 부채 본문 계정에 반영합니다.",
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
        "question": "K-IFRS 제1037호 문단 39에 따르면, 추정 대상인 지출의 발생 범위가 연속적인 구간(Continuous Range)으로 분포되어 있고 그 범위 내의 모든 지점의 발생 확률이 동일(Equally Likely)할 때, 최선의 추정치로 도출하기 위해 사용하도록 규정된 대표값은?",
        "options": [
            "① 해당 연속 구간의 최빈 중간값 (Mid-point of the range)",
            "② 해당 연속 구간의 최고 한도 배상액 (Maximum of the range)",
            "③ 해당 연속 구간의 최저 한도 금액 (Minimum of the range)",
            "④ 최고값과 최저값을 2대 8로 내분한 하향 평준화 가액",
            "⑤ 이사회 결정 한도 범위 내의 가치"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 지출의 예상 범위가 연속적인 구간이고 구간 내 모든 점의 발생 확률이 동일하다면, 해당 범위의 기댓값을 대변하는 '중간값(Mid-point)'을 최선의 추정치로 선택하여 충당부채로 계상합니다.\n\n[오답 해설]\n② 최고 한도를 잡는 것은 과도한 부채 계상이며,\n③ 최저 한도를 취하는 것은 부채 과소평가 예방 규정에 저해됩니다.\n④, ⑤ 기준서 상의 합리적이고 객관적인 대안 산식 범주가 아닙니다.",
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
        "question": "K-IFRS 제1037호 하에서 충당부채의 미래 지출액에 대한 현재가치 평가 여부를 판단할 때, '화폐의 시간가치 영향이 중요하지 않은 경우(Not Material)'에 취하여야 하는 올바른 조치는?",
        "options": [
            "① 영향이 미미하더라도 반드시 현재가치로 평가하여 복리 상각 이자비용을 1원 단위까지 기장해야 한다.",
            "② 할인 계산을 전면 거부하고 자본금 계정에서 격차를 상계 소멸시킨다.",
            "③ 화폐의 시간가치 영향이 중요하지 않다면 굳이 미래 예상 지출액을 할인하지 않고 명목가치(Nominal Value)로 충당부채를 측정할 수 있다.",
            "④ 회계 기간을 무조건 1년으로 단축하여 부채를 강제 감액 처리한다.",
            "⑤ 이연법인세 자산을 취소하고 부채의 대변에 10%의 강제 가산 충당금을 얹는다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1037호 문단 47에 의거하여, 화폐의 시간가치 영향이 중요성 기준 하에서 중요하지 않은 경우에는 할인하지 아니하고 명목금액 자체로 충당부채를 기재하는 것이 인정됩니다.\n\n[오답 해설]\n① 비중요한 경우까지 강제 할인을 의무화하지는 않습니다.\n②, ④, ⑤ 중요하지 않은 조건 하에서 자본 상계나 회계기간 단축, 강제 가산금 설정 등은 부적절한 대안입니다.",
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
        "question": "특정 사건과 관련하여 기중에 우발부채로 분류되어 주석에만 공시되던 미결 소송이, 기말 현재 경영 상태의 변동과 유사 판례 축적으로 인해 '자원유출 가능성이 높고 신뢰성 있는 금액 추정이 가능한 상태'로 진입하였다. K-IFRS 제1037호에 따른 올바른 분류 변동 회계처리는?",
        "options": [
            "① 여전히 소송이 최종 종결되지 않았으므로 주석 공시를 그대로 유지하고 본문 기재를 거부한다.",
            "② 소송 사건의 본래 취지에 따라 자산의 평가차감계정인 대손충당금으로 돌려 자산에 상계한다.",
            "③ 재무상태표 본문에 정식 부채인 '충당부채'로 새로이 인식하여 계상하고 당기 비용을 인식하여야 한다.",
            "④ 주식 할인발행 차금으로 대체하여 부채를 소멸시킨다.",
            "⑤ 대표이사 면책 이익으로 분류하여 영업외수익으로 전액 환입한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 우발부채는 매 결산기마다 상황을 재평가합니다. 유출 가능성이 다소 있는 수준(Possible)에서 유출 가능성이 높음(Probable) 및 금액 신뢰성 추정 상태로 요건이 충족 전이되었다면, 이는 더 이상 우발부채가 아니므로 당해 보고기간에 '충당부채'로 재무상태표 본문에 정식 부채로 기록하고 차변에 당기비용으로 계상하여야 합니다.\n\n[오답 해설]\n① 인식 요건을 충족한 경우 본문 기재는 의무화되므로 주석에만 방치하면 오류입니다.\n② 대손충당금은 매출채권 등의 평가 차감 계정이므로 소송 충당부채와 무관합니다.\n④, ⑤ 자본 할인발행 차금 대체나 대표이사 면책 이익 분류 등은 기준에 없는 오류 회계 처리입니다.",
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
        "question": "기업이 다수 모집단 의무인 제품보증충당부채를 기댓값(Expected Value)으로 측정할 때, 과거에 수집한 역사적 데이터 경험률을 적용하고자 한다. 이때 발생할 수 있는 오류를 차단하기 위해 취해야 할 K-IFRS 상의 올바른 조절 방법은?",
        "options": [
            "① 과거 데이터는 무조건 정확하므로 신제품 설계 변동이나 부품 결함률 변동이 있더라도 역사적 수치를 절대로 수정해서는 안 된다.",
            "② 과거의 품질 문제 경험치가 당기 신제품 설계 변경이나 신규 부품 품질 개선 등으로 인해 현재 상태와 불일치한다면, 당기말 최선의 추정치를 도출하기 위해 과거 경험률 데이터를 합리적으로 수정 및 조절 반영하여야 한다.",
            "③ 과거 경험률을 매년 1.5배씩 무조건 할증하여 보수주의를 고수한다.",
            "④ 신제품은 과거 데이터가 없으므로 첫 3년간은 보증 충당부채를 전액 ₩0으로 기록한다.",
            "⑤ 이사회 결정에 따라 매년 고정비 수준의 ₩100,000으로 보증충당부채를 제한 설정한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 기댓값 산정을 위해 과거 경험률 데이터를 인용할 경우, 당기에 도입된 신제품 디자인 수정, 부품 교체 등의 변화가 적용되어 과거 데이터의 통계 성향과 이탈하는 상황이 있다면 경영진은 최선의 추정을 위해 역사적 데이터를 합리적으로 가공, 조정하여 당기 상황에 부합하도록 최신 조치를 취하여야 합니다.\n\n[오답 해설]\n① 과거 데이터의 맹목적인 기계적 대입은 추정치 왜곡을 낳습니다.\n③ 무조건적인 1.5배 할증은 신뢰성과 중립성에 위배됩니다.\n④ 신제품이라 하더라도 유사 제품이나 예비 품질 테스트 데이터를 바탕으로 최선의 추정을 기장해야 하며, 0원 방치는 부채 누락 오류입니다.\n⑤ 이사회 임의 고정금 기장은 기준서의 추정 원칙에 위배됩니다.",
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
        "question": "K-IFRS 제1037호 상 충당부채 청산을 위한 제3자로부터의 보상 수취 판단 요건인 '거의 확실(Virtually Certain)'과 충당부채 유출 판단 요건인 '높음(Probable)'을 옳게 분석 비교한 설명은?",
        "options": [
            "① 거의 확실은 50% 초과 확률을 뜻하며, 높음은 90% 이상 확률을 의미한다.",
            "② 두 조건 모두 동일한 50% 초과 확률을 공유하므로 구분은 무의미하다.",
            "③ 높음(Probable)은 자원유출 가능성이 그렇지 않을 가능성보다 크다(>50%)는 수준이지만, 거의 확실(Virtually Certain)은 사실상 확실하게 유입된다는 훨씬 높은 확신(일반적으로 95% 이상에 준하는 보험사의 지급 확정서 등 구체적 서면 증빙 수반)의 상태를 의미한다.",
            "④ 우발부채는 거의 확실해야 잡고, 우발자산은 유출 가능성이 높으면 잡는다.",
            "⑤ 거의 확실 조건은 전적으로 이사회 결의에 의해서만 확정되는 가공의 확률 기준이다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS는 자산과 부채 인식의 비대칭성을 띱니다. 부채 유출의 '높음(Probable)'은 50% 초과 수준에서 인정되나, 보상 자산 유입의 '거의 확실(Virtually Certain)'은 불확실성이 극도로 희박한 거의 100%에 근접하는 확실한 상태(보험사나 연대 보증인의 공식적인 지급 통지서 등 객관적 권리 성립 완료)를 의미합니다.\n\n[오답 해설]\n① 확률적 정의 범위가 정반대로 기재되어 오답입니다.\n② 두 개념의 문턱값(threshold)은 서로 엄격히 차별화됩니다.\n④ 충당부채는 '높음(Probable)' 이상에서 인식하며, 우발자산은 '거의 확실(Virtually Certain)'해야 자산화됩니다.\n⑤ 이사회 결의만으로 객관적 확실 요건을 생성할 수 없습니다.",
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
        "question": "다음 중 K-IFRS 제1037호에 비추어 볼 때, 미래의 예상 지출 금액이라 하더라도 당기 기말 결산 보고서 상 '충당부채'로 인식할 수 '없는' 결정적 사유는?",
        "options": [
            "① 해당 지출이 미래의 특정 시점에 실행될 것이 확실하지만, 보고기간 말 현재의 시점에서 볼 때 기업이 해당 지출을 피할 수 있는 실질 대안(예: 미래 영업 활동의 수정 또는 중단 등)을 여전히 가지고 있는 경우",
            "② 지출 금액이 수년에 걸쳐 분할 지급되는 장기 의무인 경우",
            "③ 지출 발생 확률이 기댓값 기준 70%로 산정된 경우",
            "④ 복구 비용 계산 시 물가상승률을 감안하여 산정한 경우",
            "⑤ 계약서 상 영문으로 지급 조건이 표시되어 법적 분쟁 소지가 있는 경우"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 미래 지출이 발생하더라도 기업이 미래의 영업 행위(공장 이전, 폐업, 자산 매각 등)를 통해 당해 지출을 충분히 피할 수 있다면, 이는 과거사건의 결과로서 현재 회피할 수 없는 '현재의무'를 구성하지 못합니다. 따라서 충당부채로 올릴 수 없습니다.\n\n[오답 해설]\n② 장기 분할 지급이나 ③ 70%의 높은 발생 확률, ④ 물가상승률 반영 등은 충당부채 인식을 배제하는 사유가 아닙니다.\n⑤ 계약서 작성 언어는 부채의 실질적인 성립 여부에 직접적 차단 원인이 되지 않습니다.",
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
        "question": "이전에 계상해 둔 충당부채(예: 복구충당부채)를 당기말 재평가한 결과, 과거에 예상한 지출의 규모가 감소하여 '부채 중 일부를 환입(Reversal) 처리'하고자 한다. K-IFRS 상 이러한 환입 분개의 손익 표시 방법으로 가장 옳은 것은?",
        "options": [
            "① 당기 재무상태표의 자본금 항목을 직접 증대시켜 처리한다.",
            "② 특별 이익(Extraordinary Profit) 항목으로 구분하여 영업외수익의 최하단에 단독 공시한다.",
            "③ 포괄손익계산서 상 당초 해당 충당부채 설정 시 비용(수선비 등)으로 기장했던 동일 손익 항목의 비용을 차감(상계)하거나, 기타영업수익 등으로 환입 보고하여야 한다.",
            "④ 당기 감가상각비를 취소하여 이익잉여금에 전액 이체 조정한다.",
            "⑤ 환입 분개는 대차가 맞지 않으므로 분개 기장을 영구 금지하고 주석에만 숫자를 적는다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 충당부채의 환입은 최초에 충당부채를 설정하여 손익계산서에 인식했던 비용 항목(예: 수선비, 판매보증비 등)을 직접 차감시켜 주는 방향으로 손익계산서에 반영하거나 영업수익 등으로 공시합니다. (단, 복구충당부채 등 유형자산 취득 원가에 가산된 경우는 유형자산 해석서에 따라 다소 차이가 있지만, 일반 충당부채의 환입 원칙은 손익계산서 상 설정비용의 차감으로 보고됩니다.)\n\n[오답 해설]\n① 자본금 직접 변경은 무상증자나 자본 환원 거래에 한합니다.\n② K-IFRS는 특별손익(Extraordinary items)의 손익계산서 표시를 엄격히 금지하고 있습니다.\n④ 감가상각비의 임의 취소는 허용되지 않습니다.\n⑤ 환입 거래는 장부 상 적절한 조정을 위한 분개 처리가 필수적입니다.",
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
        "question": "K-IFRS 제1037호 하에서 충당부채 할인에 적용되는 '부채 특유의 위험(Risks specific to the liability)'을 할인율에 반영하는 올바른 기법적 전제로 가장 옳은 것은?",
        "options": [
            "① 할인율을 가산 조정할 때, 미래 현금흐름(분자)의 추정치를 도출할 때 이미 충분히 감안하여 반영한 위험 요소들은 할인율(분모) 조정 시 차감 혹은 할증 적용에서 철저히 제외하여야 한다.",
            "② 분자와 분모 양쪽에 다각도로 위험을 누적 적용하여 부채를 최대한 크게 불려야 신뢰성이 올라간다.",
            "③ 부채 특유의 위험은 항상 무위험 이자율보다 낮추어 평가하는 할인을 유도해야 한다.",
            "④ 주주들의 요구 수익률을 가중평균하여 매기 무작위 할증 대입한다.",
            "⑤ 위험 평가는 오직 기재부 장관이 정하는 지표 고시에 의해서만 할증한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 이중 계산(Double Counting) 오류를 예방하는 정합 로직입니다. 미래 현금흐름(분자)에 이미 부채 고유의 채무 불이행 등 위험 요소를 가산하여 현금 유출액을 크게 추정해 두었다면, 할인율(분모)을 선택할 때는 중복으로 해당 위험 프리미엄을 가산하여 할증하지 않고 무위험 이자율 수준을 기준으로 할인하여야 합니다.\n\n[오답 해설]\n② 양쪽에 누적 조정 시 이중 반영 왜곡이 발생합니다.\n③ 부채 위험 반영 시 일반적으로 할인율은 상향 조정(할증)되어 현재가치를 낮추게 되므로 이와 상충됩니다.\n④ 주주의 요구수익률(자본비용)은 부채 고유의 채무 이행 위험과 상이합니다.\n⑤ 기재부 장관 고시 이자율을 강제 준용하는 규정은 회계 상 존재하지 않습니다.",
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
        "question": "복구의무가 있는 30년 만기 장기 복구충당부채의 회계처리에 있어서, 화폐의 시간가치 할인 효과가 미치는 장기적 손익 영향에 관한 분석으로 가장 올바른 것은?",
        "options": [
            "① 장기 부채는 할인하지 않으므로 만기 시점에 1회성 기부금으로 처리한다.",
            "② 만기가 너무 길면 이자비용이 전혀 유발되지 않는 것으로 본다.",
            "③ 최초 인식 시점에는 명목 철거액 전체가 부채로 계상되므로 자본이 즉시 잠식된다.",
            "④ 시간의 경과에 따라 현재가치가 만기 철거예상 명목액으로 점진적 수렴하게 되며, 이에 따라 매년 이자비용(Unwinding Interest Expense)이 복리식으로 기장되어 당기 손익에 중대한 부정적 이자비용 영향을 지속적으로 가하게 된다.",
            "⑤ 시간가치 할인의 해제액은 유형자산의 감가상각비 계정으로 통합 보고된다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 화폐의 시간가치 할인이 중요한 장기 부채(예: 30년 만기 복구의무)는 최초에 극히 낮은 현재가치로 부채(복구충당부채)를 인식합니다. 그러나 매년 유효이자율만큼 부채 가액을 복리로 불려 나가므로(차변: 이자비용, 대변: 복구충당부채) 시간 경과에 따라 매기 이자비용이 계상되며, 만기 시점에는 명목 철거액 총액인 ₩133,100 등 최종 명목액에 완벽하게 도달(수렴)하게 됩니다.\n\n[오답 해설]\n① 30년 만기 등 시간가치 영향이 중요할 경우 현재가치 할인은 필수 의무입니다.\n② 만기가 길어질수록 할인 효과와 매기 상각액(이자비용) 영향은 극도로 증가합니다.\n③ 최초에는 명목액이 아닌 현재가치로 부채를 차감 측정하여 인식합니다.\n⑤ 할인 해제 부분은 유형자산 감가상각비와 성격이 다른 금융 이자비용으로 손익계산서에 단독 표기됩니다.",
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
