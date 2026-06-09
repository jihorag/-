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
    "section": "Chapter 06 투자부동산",
    "item": "1절 투자부동산의 의의"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q1401 ~ Q1410) ---
    {
        "id": "practice-accounting-ch06s01-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1040호 '투자부동산'에 규정된 투자부동산의 핵심 정의로 가장 올바른 것은?",
        "options": [
            "① 임대수익이나 시세차익 또는 둘 다를 얻기 위하여 소유자나 리스이용자가 보유하는 부동산",
            "② 통상적인 영업과정에서 판매하기 위하여 보유하는 부동산",
            "③ 재화의 생산이나 용역의 제공 및 타인에 대한 임대를 위해 보유하는 유형의 자산",
            "④ 기업의 일상적인 관리 목적 및 종업원의 주거 편의를 위해 소유하고 있는 부동산",
            "⑤ 제3자와의 장기 공급계약에 따라 당사자 간 공동으로 개발 및 지배하는 부동산"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1040호에 따르면, 투자부동산은 임대수익(Rentals)이나 시세차익(Capital appreciation) 또는 둘 다를 얻기 위하여 소유자나 리스이용자(사용권자산)가 보유하는 부동산(토지, 건물, 또는 토지와 건물의 일부나 전부)을 의미합니다.\n\n[오답 해설]\n② 통상적인 영업과정에서의 판매 목적 부동산은 K-IFRS 제1002호 '재고자산'에 해당합니다.\n③ 이는 K-IFRS 제1016호 '유형자산'(자가사용부동산)의 정의에 해당합니다. 유형자산의 정의에도 '타인에 대한 임대'가 포함되어 있으나, 투자부동산 기준서에서 말하는 임대수익만을 목적으로 하는 임대(운용리스 제공)와는 구분됩니다.\n④ 관리 목적 부동산 및 종업원 사용 사택은 자가사용부동산(유형자산)으로 분류됩니다.\n⑤ 공동약정이나 공동지배 관련 자산은 K-IFRS 제1111호 등의 지배구조 기준서에 따릅니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "토지의 분류 중 K-IFRS 제1040호에 따라 '투자부동산'으로 분류하여야 하는 가장 대표적인 항목은?",
        "options": [
            "① 단기적인 영업과정에서 분양하기 위해 보유하고 있는 토지",
            "② 장기적인 시세차익을 얻기 위하여 보유하고 있는 토지",
            "③ 공장을 건설하여 제품을 생산하기 위해 현재 사용 중인 토지",
            "④ 본사 빌딩 신축을 예정하고 임시 주차장으로 직접 사용 중인 토지",
            "⑤ 금융리스 계약을 맺고 타인에게 장기 대여한 토지"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 장기적인 시세차익을 얻기 위하여 보유하는 토지는 대표적인 투자부동산 예시입니다. 단기 매각 목적이 아니므로 재고자산이 아니며, 자가사용 목적이 아니므로 유형자산도 아닙니다.\n\n[오답 해설]\n① 통상적인 영업과정에서 분양 목적으로 보유하면 재고자산에 해당합니다.\n③, ④ 제품 생산이나 본사 부지 등으로 직접 또는 간접적으로 사용하는 토지는 자가사용부동산(유형자산)입니다.\n⑤ 금융리스로 대여한 토지는 리스 채권의 성격이 되어 대차대조표에서 제거되므로 투자부동산이 될 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "기업이 보유 중인 토지의 '미래 용도를 현재 시점에서 결정하지 못한 경우' K-IFRS 제1040호에 따른 분류 방법으로 옳은 것은?",
        "options": [
            "① 자산 분류를 보류하고 임시계정인 건설중인자산으로 처리한다.",
            "② 재고자산으로 분류하여 저가법을 적용한다.",
            "③ 자가사용부동산으로 보아 유형자산(토지)으로 분류한다.",
            "④ 시세차익 목적으로 보유하는 것으로 보아 투자부동산으로 분류한다.",
            "⑤ 기타비유동자산의 투자자산 계정으로 임의 계상한다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ K-IFRS 제1040호 문단 8(1)에 따르면, 미래에 자가사용할지 또는 통상적인 영업과정에서 단기 판매할지를 결정하지 못한 토지는 시세차익을 얻기 위하여 보유하는 것으로 보아 '투자부동산'으로 분류합니다.\n\n[오답 해설]\n① 건설중인자산은 자가사용 목적으로 건설 중인 경우에 사용하는 유형자산 항목이므로 미래 용도 미확정 토지에는 적용되지 않습니다.\n②, ③ 용도가 불분명한 토지를 재고자산이나 유형자산으로 계상하는 것은 기준서 위반입니다.\n⑤ IFRS 상 공식적인 과목 명칭은 '투자부동산'이어야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "다음 중 K-IFRS 제1040호의 적용 범위 상 투자부동산에 해당할 수 있는 건물 보유 상태는?",
        "options": [
            "① 타인에게 금융리스로 제공 중인 건물",
            "② 종업원의 사택 목적으로 무상 공급하여 사용 중인 건물",
            "③ 타인에게 하나 이상의 운용리스로 제공 중인 건물",
            "④ 정상적인 영업활동 과정에서 고객에게 분양하기 위하여 건축 중인 상가건물",
            "⑤ 공장 부지 내에 위치하여 제품 적재용 창고로 직접 사용 중인 건물"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 임차인에게 운용리스 조건으로 제공되는 건물은 대표적인 투자부동산입니다.\n\n[오답 해설]\n① 금융리스로 대여한 자산은 리스이용자에게 실질적 소유 위험과 혜택이 넘어가므로 임대인의 투자부동산에서 배제됩니다.\n② 종업원에게 제공하는 사택은 복리후생 및 관리 목적으로 분류되어 자가사용부동산(유형자산)에 속합니다.\n④ 분양 목적 건축물은 재고자산(미완성주택 등)에 해당합니다.\n⑤ 공장 창고 등 제조·관리 활동에 직접 쓰는 건물은 유형자산으로 분류됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "현재 비어 있는 상태(Vacant)이나, 제3자에게 운용리스로 제공하기 위하여 보유하고 있는 건물의 분류 기준은?",
        "options": [
            "① 운용리스 개시 시점까지는 임시로 유형자산으로 분류한다.",
            "② 공실 상태이므로 자산으로 인식할 수 없으며 기중 비용으로 처리한다.",
            "③ 영업 활동에 직접 기여하지 않으므로 무형자산으로 분류한다.",
            "④ 리스 개시 전이라도 운용리스 제공 목적이 명확하다면 투자부동산으로 분류한다.",
            "⑤ 영업외자산 계정인 비가동유휴자산으로 별도 분류한다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ K-IFRS 제1040호 문단 8(3)에 따라, 현재 비어있으나 하나 이상의 운용리스로 제공하기 위하여 보유하고 있는 건물은 리스 계약이 개시되지 않았더라도 투자부동산으로 분류합니다.\n\n[오답 해설]\n① 리스 개시 전이라는 이유로 유형자산에 분류할 수 없습니다.\n② 비어있더라도 경제적 효익 창출 목적(운용리스 제공)이 뚜렷하므로 비동작 기간에도 자산으로 유지되어야 합니다.\n③, ⑤ IFRS 기준 상 건물 자산은 유형자산 또는 투자부동산으로 분류되어야 하며 비가동유휴자산 등은 공식적인 분류 항목이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "미래에 투자부동산으로 사용할 목적으로 현재 건설 중이거나 개발 중인 부동산(Property under construction or development)의 회계학상 분류로 올바른 것은?",
        "options": [
            "① 건설 과정에서는 유형자산(건설중인자산)으로 분류하고 완공 시점에 투자부동산으로 대체한다.",
            "② 개발 및 건설 과정에서도 처음부터 투자부동산으로 분류한다.",
            "③ 개발비에 준하여 무형자산으로 분류하고 감가상각을 즉시 개시한다.",
            "④ 완공되어 실제 임대수익이 실현될 때까지는 자산성이 없으므로 전액 당기비용으로 계상한다.",
            "⑤ 토지 부분은 투자부동산으로, 건물 신축 비용 부분은 유형자산으로 이원화하여 분류한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1040호 문단 8(5)에 따라, 미래에 투자부동산으로 사용하기 위하여 건설하거나 개발 중인 부동산은 건설 중인 기간에도 투자부동산으로 분류합니다.\n\n[오답 해설]\n① 과거 기준에서는 완공 전까지 유형자산(건설중인자산)으로 다룬 적이 있으나, 개정된 현행 기준에서는 건설 중인 기간에도 투자부동산으로 분류하도록 규정하고 있습니다.\n③ 무형자산이 아닌 부동산(유형자산성격)이므로 부적절합니다.\n④ 개발 및 건설 중인 자산도 미래의 경제적 효익을 기대할 수 있으므로 자산으로 자본화합니다.\n⑤ 토지와 건물은 투자부동산이라는 동일한 하나의 목적으로 결합하여 개발되고 있으므로 전체를 투자부동산으로 처리하는 것이 원칙입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "다음 중 K-IFRS 제1040호에 따라 투자부동산에서 명확히 배제되는 자가사용부동산(Owner-occupied property)에 해당하는 것은?",
        "options": [
            "① 미래에 투자부동산으로 사용하기 위해 개발 중인 유휴 토지",
            "② 종업원이 사용하고 있는 주택(종업원이 시장이자율 수준의 임차료를 지급하는지 여부와 무관)",
            "③ 임대수익과 장기 시세차익을 동시에 얻기 위해 보유하는 상가 건물",
            "④ 제3자에게 운용리스 조건으로 임대하기 위해 취득하여 수리 중인 오피스텔",
            "⑤ 미래 용도가 결정되지 않아 일단 보유 중인 임야"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1040호 문단 9(3)에 명시된 바와 같이, 종업원이 사용 중인 사택은 종업원이 시장이자율이나 시장가격 수준의 임대료를 지불하는지 여부와 관계없이 자가사용부동산에 속하며, K-IFRS 제1016호 '유형자산'을 적용합니다.\n\n[오답 해설]\n①, ④ 미래 투자부동산 예정인 개발 자산 및 수리 자산은 투자부동산에 해당합니다.\n③ 임대 및 시세차익 목적은 가장 대표적인 투자부동산 사유입니다.\n⑤ 미래 미결정 토지는 시세차익 목적으로 보유하는 투자부동산으로 가정합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "부동산 매매를 주업으로 하는 기업이 통상적인 영업과정에서 판매하기 위하여 취득 및 보유하고 있는 아파트나 미분양 건물은 재무제표 상 어느 계정으로 분류해야 하는가?",
        "options": [
            "① 투자부동산",
            "② 유형자산",
            "③ 재고자산",
            "④ 무형자산",
            "⑤ 기타비동작자산"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1040호 문단 9(1)에 따르면, 통상적인 영업과정에서 판매하기 위하여 보유하는 부동산이나 판매를 위하여 건설 또는 개발 중인 부동산은 K-IFRS 제1002호 '재고자산'에 해당합니다.\n\n[오답 해설]\n① 시세차익이나 임대 목적이 아닌 통상적 판매 목적이므로 투자부동산이 될 수 없습니다.\n② 기업 자체의 생산/공급이나 자가사용 용도가 아니므로 유형자산도 아닙니다.\n④, ⑤ 건물 등 형체가 있는 물리적 자산이므로 무형자산이 될 수 없으며, 영업상의 주된 상품이므로 재고자산으로 명확히 계상합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "리스 계약 유형에 따른 소유 부동산의 계상 방법 중 투자부동산으로 대차대조표(재무상태표)에 인식할 수 없는 경우는?",
        "options": [
            "① 토지 보유자가 제3자에게 5년 기간의 운용리스로 임대해 준 토지",
            "② 건물 소유주가 임차인과 운용리스 계약을 맺고 매월 리스료를 수취하는 건물",
            "③ 리스이용자 측면에서 기초자산을 전대할 목적으로 인식한 운용사용권(사용권자산)",
            "④ 금융리스 계약에 따라 실질적 권리와 위험이 리스이용자에게 이전된 임대 빌딩",
            "⑤ 공실 상태로 방치되어 있으나 향후 운용리스 제공을 위해 리스 파트너를 모집 중인 건물"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 금융리스로 대여한 자산은 리스이용자가 자산의 실질적 통제와 위험을 부담하므로, 임대인(소유자)은 이를 재무상태표에서 제거(매각에 준함)하고 '금융리스채권'을 인식하여야 합니다. 따라서 투자부동산으로 인식할 수 없습니다.\n\n[오답 해설]\n①, ② 운용리스 임대 부동산은 소유주가 투자부동산으로 처리합니다.\n③ 사용권자산이 투자부동산의 정의를 충족하여 사용권을 전대(임대)하는 경우 사용권자산 자체를 투자부동산으로 분류할 수 있습니다.\n⑤ 미임대 상태라도 향후 운용리스 제공 목적이 뚜렷하면 투자부동산으로 분류합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "지배기업이 종속기업에 건물을 운용리스로 제공한 거래에 대하여, 지배기업의 '개별재무제표'와 연결실체의 '연결재무제표'상 해당 부동산의 올바른 분류는?",
        "options": [
            "① 개별재무제표: 투자부동산, 연결재무제표: 투자부동산",
            "② 개별재무제표: 유형자산(자가사용), 연결재무제표: 유형자산(자가사용)",
            "③ 개별재무제표: 투자부동산, 연결재무제표: 유형자산(자가사용)",
            "④ 개별재무제표: 유형자산(자가사용), 연결재무제표: 투자부동산",
            "⑤ 개별재무제표: 재고자산, 연결재무제표: 유형자산(자가사용)"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1040호 문단 15에 따르면, 지배기업이 종속기업에 부동산을 리스해 준 경우 개별(별도)재무제표 관점에서는 법적으로 독립된 타인에게 리스해 준 것이므로 '투자부동산' 분류 요건을 충족합니다. 그러나 연결실체 전체 관점에서는 연결실체 내부 구성원(종속기업)이 자가사용하고 있는 부동산이므로 '투자부동산'이 아닌 '유형자산(자가사용부동산)'으로 분류하여야 합니다.\n\n[오답 해설]\n① 연결실체 관점의 사용 목적을 간과하여 연결재무제표에서도 투자부동산으로 처리하면 오류입니다.\n② 개별재무제표는 개별 법인 관점이므로 운용리스 임대 대상 자산인 투자부동산으로 인식하여야 합니다.\n④, ⑤ 개별과 연결재무제표의 올바른 분류 대조 방향이 완전히 반대로 뒤바뀌어 있거나 재고자산으로 잘못 분류하였습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    # --- L2 (이해): 15문항 (Q1411 ~ Q1425) ---
    {
        "id": "practice-accounting-ch06s01-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "일부 영역은 임차인에게 임대하여 수익을 얻고(운용리스), 다른 영역은 자기가 직접 사용하는(생산·관리 목적) '복합용도 부동산'에 대한 K-IFRS 제1040호의 회계처리 규칙으로 가장 올바른 것은?",
        "options": [
            "① 부분별로 분할 매각할 수 있는지 여부와 관계없이, 전체 부동산의 공정가치 비중에 따라 무조건 개별 자산으로 분배 등기하여 처리한다.",
            "② 부분별로 분할하여 매각(또는 금융리스 제공)할 수 있다면, 각 부분을 구분하여 각각 투자부동산과 유형자산으로 계상한다.",
            "③ 분할 매각이 불가능하더라도, 자가사용 부분이 전체 면적의 50%를 초과하는 경우에는 무조건 전체를 유형자산으로 단일 분류한다.",
            "④ 분할 매각이 불가능한 경우에는 자가사용 목적으로 보유하는 부분이 매우 '경미한(Insignificant)' 수준이라도 절대 투자부동산으로 통합할 수 없다.",
            "⑤ 분할 매각의 가능 여부와 상관없이 지배력을 행사하는 대표 용도 하나를 경영진이 임의 선택하여 단일 과목으로 공시한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 복합용도 부동산의 경우, 부분별로 분할하여 매각할 수 있는 경우에는 각각 투자부동산 부분과 유형자산 부분으로 나누어 회계처리합니다. 분할 매각이 불가능한 경우에는 자가사용 부분이 매우 '경미한' 수준인 경우에만 전체 부동산을 투자부동산으로 분류합니다.\n\n[오답 해설]\n① 분할 매각 가능 여부가 회계분류의 가장 최초 의사결정 경로이므로 관계없다고 한 설명은 거짓입니다.\n③ 분할 매각이 불가능할 경우 자가사용 부분이 경미할 때만 전체를 투자부동산으로 분류하며, 면적 50% 등의 단순 고정 수치 기준은 기준서에 존재하지 않습니다.\n④ 분할 매각이 불가할 때 자가사용 부분이 경미하다면 전체를 투자부동산으로 계상할 수 있는 예외 조항이 명시되어 있습니다.\n⑤ 자의적 분류가 아닌 기준서가 제공하는 분할 가능성 및 경미성 요건에 따라 강제 처리해야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "부동산 소유자가 점유자에게 '부수적 용역(Ancillary services)'을 제공하는 경우의 분류 기준으로 옳은 것은?",
        "options": [
            "① 용역의 제공 비중이 유의적인지 여부와 상관없이 용역 수입이 발생하면 즉시 유형자산으로 강제 재분류된다.",
            "② 제공하는 용역이 전체 계약에서 '경미한 수준(Insignificant)'인 경우에만 전체 부동산을 투자부동산으로 분류할 수 있다.",
            "③ 제공하는 용역이 유의적이라 하더라도 토지와 건물의 소유권이 이전되지 않았다면 항상 투자부동산으로 남는다.",
            "④ 부수적 용역 제공 계약이 있는 부동산은 기준서 적용 범위에서 영구 배제되어 무조건 투자자산 내의 잡자산으로 공시된다.",
            "⑤ 용역비용의 합계가 부동산 감가상각비보다 큰 경우에만 투자부동산으로 분류가 유지된다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1040호 문단 11에 따라, 부동산 보유자가 사용자에게 제공하는 부수적 용역이 전체 계약에서 경미한 수준(예: 오피스 빌딩 임차인들에게 제공하는 경비, 청소, 시설 관리 서비스)인 경우, 임대인은 해당 부동산 전체를 '투자부동산'으로 인식할 수 있습니다.\n\n[오답 해설]\n① 용역의 경미성 판단에 따라 투자부동산 유지가 가능하므로 틀린 지문입니다.\n③ 용역 비중이 유의적인 수준(예: 직접 호텔을 관리·운영하는 경우)에 이르게 되면 투자부동산이 아니라 자가사용부동산(유형자산)으로 처리해야 합니다.\n④, ⑤ IFRS 분류 체계에 없는 임의 기준이나 부적합한 자산 계정 명칭입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "소유주가 호텔을 직접 관리하고 고객에게 숙박 및 식음료 등 광범위한 서비스를 직접 제공하는 경우(Owner-managed hotel), 해당 호텔 부동산의 K-IFRS 상 올바른 자산 분류 기준은?",
        "options": [
            "① 임대업의 일종으로 보아 투자부동산으로 분류한다.",
            "② 제공하는 부수 용역이 매우 유의적이므로 자가사용부동산(유형자산)으로 분류한다.",
            "③ 부동산 부분과 서비스 부분을 강제 안분하여 별도의 유형자산과 무형자산으로 각각 보고한다.",
            "④ 고객과의 계약에서 수행의무가 이행된 것이므로 매출채권으로 대체 계상한다.",
            "⑤ 숙박 계약 형태가 단기 리스에 해당하므로 리스 채권으로 회계처리한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 소유주가 직접 경영하는 호텔의 경우, 투숙객에게 제공하는 용역(보안, 청소 수준을 넘어 식음료, 객실 관리, 헬스장, 연회장 등 종합 서비스 제공)이 매우 유의적(Significant)이므로, 이는 단순 자산 임대라기보다 기업의 적극적인 영업활동에 직접 사용하는 자가사용부동산에 해당합니다. 따라서 K-IFRS 제1016호 '유형자산'을 적용해야 합니다.\n\n[오답 해설]\n① 호텔 경영은 용역 유의성이 매우 크기 때문에 투자부동산으로 분류할 수 없습니다.\n③ 토지 및 건물의 물리적 형체를 임의로 유형자산과 서비스 무형자산으로 갈라쳐 보고하는 기준은 없습니다.\n④, ⑤ 계약 자산이나 리스 거래의 결제 채권에 불과한 형태로 건물 자체를 지울 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "K-IFRS 제1040호 문단 15에서 지배·종속기업 간 임대부동산을 '연결재무제표' 상에서 투자부동산으로 유지할 수 없다고 규정하는 이론적 배경으로 가장 적절한 것은?",
        "options": [
            "① 연결재무제표는 연결실체를 '단일의 경제적 보고기업(Single Reporting Entity)'으로 보아 작성되기 때문이다.",
            "② 지배기업과 종속기업은 별개의 법적 실체이므로 회계과목도 독립적으로 표시하여야 하기 때문이다.",
            "③ 내부거래에서 발생하는 리스료 수익은 자본거래의 성격을 가지므로 자산성이 완전 소멸하기 때문이다.",
            "④ 연결실체 내부의 임대인은 실질적인 통제권을 종속기업 경영진에 완전히 양도하여 회수가 불가능하기 때문이다.",
            "⑤ 개별재무제표 상의 자산 표시가 연결재무제표 상의 표시보다 항상 우선하는 법률적 성격을 지니기 때문이다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 연결재무제표는 지배·종속관계를 형성하는 여러 법적 실체를 하나의 '단일 경제적 실체(Reporting Entity)'로 취급합니다. 따라서 내부적으로 자산을 대여하고 사용하는 거래는 실체 관점에서는 자가사용에 해당하여 투자부동산 지위를 상실하고 유형자산으로 회생되어야 합니다.\n\n[오답 해설]\n② 법적으로 독립된 실체라는 논리는 '개별재무제표' 상에서 투자부동산으로 분류하는 근거이지 연결재무제표의 기준이 아닙니다.\n③ 리스료의 상계 제거는 부차적인 연결 조정이며 자산 자체의 물리적 실재성이 소멸하는 것은 아닙니다.\n④ 통제권 양도 여부보다는 하나의 경제적 단일체라는 관점이 본질적인 회계처리 기준입니다.\n⑤ 연결재무제표가 연결실체의 실질을 우선 공시하므로 개별 표시가 연결보다 법적으로 우선한다는 것은 오답입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "K-IFRS 제1040호 개정(과거 대비 변동 사항)에 따라 '투자부동산으로 사용하기 위해 건설 중인 부동산'에 대한 현행 회계처리와 과거 회계처리의 변화를 바르게 설명한 것은?",
        "options": [
            "① 과거에는 투자부동산으로 전액 분류하였으나, 현재는 유형자산으로 상시 통합 분류한다.",
            "② 과거에는 완공 시까지 유형자산(건설중인자산)으로 분류하였으나, 현재는 건설 과정에서도 투자부동산으로 분류한다.",
            "③ 과거에는 기중 비용으로 처리했으나, 현재는 무형자산인 개발비로 분류하여 자본화한다.",
            "④ 과거와 현재 모두 어떠한 자산성도 인정하지 않고 현금 유출 시 전액 즉시 처분손실로 잡는다.",
            "⑤ 토지 취득 비용만 투자부동산으로 처리하고 건물 신축 공사비는 영업 비용으로 강제 처리하도록 규제가 강화되었다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1040호 개정 전에는 미래 투자부동산 목적 건설 자산을 완공 전까지 유형자산(건설중인자산)으로 처리하도록 하였으나, 현행 기준서에서는 건설 및 개발 중인 기간에도 투자부동산으로 직접 분류하도록 개정되어 규정 간 일관성을 확보하였습니다.\n\n[오답 해설]\n① 현행 기준은 건설 단계부터 투자부동산 분류를 강제하므로 서술 방향이 잘못되었습니다.\n③, ⑤ 건물 신축 공사비나 토지비는 부동산의 취득원가를 구성하는 자산 자본화 대상이지 비용이나 무형자산 분류 대상이 아닙니다.\n④ 자산성을 인정하지 않는다는 표현은 대차대조표의 기본 구조와 대치됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "리스이용자가 리스 계약에 따라 인식한 '사용권자산(Right-of-use asset)'을 투자부동산으로 분류하기 위한 요건에 대한 설명으로 옳은 것은?",
        "options": [
            "① 리스이용자의 사용권자산은 어떠한 경우에도 투자부동산으로 분류할 수 없다.",
            "② 리스이용자가 해당 사용권자산을 전대(Sublease)할 목적 없이 직접 관리 부서 사무실로 사용하는 경우 분류 가능하다.",
            "③ 사용권자산의 기초자산이 토지나 건물이고, 이를 임대수익이나 시세차익을 얻기 위해 운용리스 등으로 보유하는 경우 투자부동산으로 분류한다.",
            "④ 사용권자산의 공정가치 변동액을 전액 기타포괄손익으로만 평가 인식하는 조건 하에서만 가능하다.",
            "⑤ 금융리스 조건의 리스이용자로서 해당 부동산을 본사 창고로 활용하는 때에만 가능하다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 리스이용자가 리스 계약을 통해 보유 중인 사용권자산이라도 기초자산이 부동산(토지, 건물 또는 둘 다)이고, 투자부동산의 정의(임대수익 또는 시세차익 목적 보유)를 충족한다면 사용권자산 자체를 '투자부동산'으로 분류하여야 합니다.\n\n[오답 해설]\n① 사용권자산도 투자부동산의 정의 충족 시 분류가 가능합니다.\n② 직접 관리 부서 사무실로 쓰는 경우에는 자가사용부동산(유형자산의 사용권자산)으로 분류됩니다.\n④ 공정가치 변동은 투자부동산의 측정 모형에 따르며, 공정가치 모형 적용 시 변동분은 당기손익으로 갑니다.\n⑤ 본사 창고 활용 시에는 유형자산으로 계상하여야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "K-IFRS 제1040호 '투자부동산'의 공정가치모형(Fair Value Model)과 K-IFRS 제1016호 '유형자산'의 재평가모형(Revaluation Model)의 평가손익 인식에 대한 차이점을 바르게 설명한 것은?",
        "options": [
            "① 투자부동산 공정가치모형의 평가손익은 당기손익으로 인식하고, 유형자산 재평가모형의 재평가증가액은 기타포괄손익으로 인식한다.",
            "② 투자부동산 공정가치모형의 평가손익은 기타포괄손익으로 인식하고, 유형자산 재평가모형의 재평가증가액은 당기손익으로 인식한다.",
            "③ 두 모형 모두 평가 증가액은 자본잉여금으로 적립하고 평가 감소액만 당기손실로 처리한다.",
            "④ 두 모형 모두 평가 시 발생하는 모든 손익을 당기손익으로 즉시 환원한다.",
            "⑤ 두 모형 모두 재무상태표 상 자산 가액을 역사적 원가로 고정 표시하며 손익 거래는 전혀 발생하지 않는다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 투자부동산의 공정가치모형을 적용하면 공정가치 변동으로 발생하는 손익은 발생한 기간에 전액 당기손익(당기순이익에 직접 가감)으로 인식합니다. 반면, 유형자산의 재평가모형에서는 재평가 시 발생하는 자산 증가액은 원칙적으로 기타포괄손익(OCI, 재평가잉여금)으로 인식하여 자본에 가산합니다.\n\n[오답 해설]\n② 두 자산군별 평가액의 손익구조가 정반대로 뒤바뀐 진술입니다.\n③, ④ 유형자산의 재평가는 기본적으로 기타포괄손익 중심이고, 투자부동산 공정가치 평가는 전액 당기손익 계상이므로 일률적인 통폐합 서술은 오답입니다.\n⑤ 두 모형 모두 재무상태표 상의 기말 금액을 평가일 현재의 공정가치(재평가액)로 갱신하여 공시하는 변동 회계 모형입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "K-IFRS 제1040호 하에서 투자부동산의 후속 측정 모형 선택에 따른 '감가상각(Depreciation)' 수행 여부 규칙으로 옳은 것은?",
        "options": [
            "① 공정가치모형을 선택한 경우에도 매년 건물 부분에 대해 경제적 상각을 적용해 장부금액을 줄여야 한다.",
            "② 공정가치모형을 선택한 투자부동산은 감가상각을 수행하지 않는다.",
            "③ 원가모형을 선택한 경우 감가상각을 생략하고 매년 공정가치 변동액만 기재한다.",
            "④ 어떠한 측정 모형을 선택하더라도 원가모형과 마찬가지로 동일하게 정액법 감가상각을 의무 적용한다.",
            "⑤ 토지 부분은 공정가치모형을 적용하고 건물 부분은 원가모형으로 감가상각하는 혼합 적용만 허용한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 투자부동산에 대하여 공정가치모형을 선택한 경우에는 기말에 공정가치로 측정하고 평가손익을 인식하므로, 추가적인 감가상각을 수행하지 않습니다. (원가모형을 선택한 투자부동산은 유형자산과 동일하게 내용연수에 따라 감가상각을 수행해야 합니다.)\n\n[오답 해설]\n① 공정가치모형에서는 공정가치 평가 자체에 시간의 흐름에 따른 건물 노후화 요인이 모두 흡수 반영되므로 별도의 감가상각을 돌리지 않습니다.\n③ 원가모형 투자부동산은 감가상각을 필히 수행하며 공정가치 변동액을 장부에 기록하지 않습니다.\n④, ⑤ 측정 모형에 따른 감가상각 유무는 상이하며, 동일한 용도의 부동산 포트폴리오 전반에 일관된 모형을 사용해야지 자의적 개별 혼합은 금지됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "유형자산이나 재고자산을 투자부동산으로 대체하거나, 반대로 투자부동산을 다른 자산 계정으로 재분류하는 '계정 대체(Transfer)'의 필수 선결 요건은?",
        "options": [
            "① 이사회 결의를 통한 장부 재평가 의사의 공식 문서화",
            "② 세법 상 세액 공제 요건을 충족하기 위한 소유권 변동 접수",
            "③ 해당 부동산의 '실질적인 사용 목적의 변경(Change in Use)' 발생",
            "④ 부동산 시장의 연간 평균 거래 대금의 10% 이상 하락",
            "⑤ 외부 독립 감정평가사의 계정 변경 권고 진단서 확보"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1040호 문단 57에 따라, 부동산의 계정 대체는 부동산의 실질적인 '사용 목적의 변경(Change in Use)'이 있고, 그 변경을 입증하는 객관적인 사건이 발생한 경우에만 수행할 수 있습니다. 단순한 경영진의 의도 변경만으로는 대체할 수 없습니다.\n\n[오답 해설]\n①, ⑤ 경영진의 자의적 판단이나 형식적인 의결서 및 권고서만으로는 객관적 사용 변경 사실 없이 자산을 임의 재분류할 수 없습니다.\n②, ④ 세무적 사유나 단순 거시 지표 변화는 계정 대체 요건에 부합하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "다음 중 K-IFRS 제1040호 투자부동산 기준서에서 명시하는 '자가사용부동산(Owner-occupied property)'에 해당하지 않는 자산 상태는?",
        "options": [
            "① 미래에 자가사용부동산으로 사용할 목적으로 보유하는 부동산",
            "② 미래에 개발하여 자가사용할 목적으로 현재 개발 중인 부동산",
            "③ 종업원이 사용하고 있는 사택(임차료 납부 유무 무관)",
            "④ 처분예정인 자가사용부동산",
            "⑤ 타인에게 운용리스 조건으로 임차 계약을 완료하고 공실 상태인 오피스텔"
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ 타인에게 운용리스 조건으로 대여하기 위해 임차 계약을 완료하고 공실인 건물은 자가사용 목적이 전혀 없으므로 투자부동산에 해당합니다.\n\n[오답 해설]\n①, ② 자가사용할 목적을 가지고 보관 및 개발 중인 자산은 자가사용부동산(유형자산)입니다.\n③ 종업원 사택은 유형자산으로 다룹니다.\n④ 자가사용하다 처분을 앞둔 자산도 처분 완료나 K-IFRS 1105호의 매각예정자산으로의 재분류 전까지는 자가사용부동산(유형자산) 범주로 분류됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "부동산의 소유주가 호텔 경영 전문가 집단인 제3의 운영사에게 호텔의 일상적 관리를 전액 위탁하였으나, 호텔 운영 실적에 따른 모든 경제적 손익 위험과 운영 위험을 최종적으로 소유주가 전적으로 부담하는 계약을 맺은 경우, 해당 호텔 부동산의 K-IFRS 상 분류로 올바른 것은?",
        "options": [
            "① 위탁 대행을 통한 간접 임대 성격이므로 투자부동산으로 분류한다.",
            "② 실질적으로 자산 보유자가 사업상 현금흐름 변동 위험을 부담하고 통제하므로 자가사용부동산(유형자산)으로 분류한다.",
            "③ 계약 상 대행 비용이 발생하므로 금융리스 채권으로 이전 인식한다.",
            "④ 호텔 영업이 종속 법인화된 것이므로 투자주식 계정으로 재분류한다.",
            "⑤ 토지는 투자부동산, 건물은 무형자산으로 각각 전환 인식한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1040호 문단 13에 따르면, 소유자가 경영을 위탁(외주) 주더라도 계약 구조 상 호텔의 운영 성과에 따른 현금흐름의 유의적인 변동 위험(수익성 악화 시 손실을 모두 소유주가 떠안는 구조)을 소유주가 여전히 직접 노출 및 통제하고 있다면, 이는 사실상 소유주가 직접 사업을 영위하는 자가사용부동산(유형자산)에 가깝습니다.\n\n[오답 해설]\n① 외형상 위탁 용역 구조를 띄더라도 본질적 영업 위험을 전면 지고 있으므로 투자부동산이 될 수 없습니다.\n③ 리스이용자 측으로 자산 이전 거래가 일어난 금융리스 구조가 아닙니다.\n④, ⑤ 법인 주식의 지분이나 물리적 분할 인식을 유도하는 잘못된 회계논리입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "기업이 장기간 시세차익 목적으로 보유하던 투자부동산(토지)을 '개발 단계(신축 등)를 전혀 거치지 않고' 즉시 제3자에게 매각하기로 결정한 경우, 해당 자산의 회계처리 규칙으로 올바른 것은?",
        "options": [
            "① 매각 결정 즉시 재고자산으로 대체 재분류한다.",
            "② 매각 결정 즉시 자가사용부동산(유형자산)으로 임시 이체한다.",
            "③ 제거될 때까지 계속 투자부동산으로 보유하며, 매각(제거) 시점에 한 번에 처리한다.",
            "④ 토지의 미래 사용 가치가 소멸한 것으로 보아 전액 즉시 손상차손 비용으로 감액한다.",
            "⑤ 매각을 위한 처분비용을 자산의 역사적 원가에 가산하여 장부액을 높인다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1040호 문단 58에 따르면, 기업이 기존의 투자부동산을 개발(재개발이나 상가 신축 분양 등)하지 않고 처분하기로 결정한 경우, 해당 자산이 최종적으로 제거(매각 완료)될 때까지는 계속 투자부동산으로 분류하여야 하며 재고자산 등으로 임의 대체할 수 없습니다. (단, K-IFRS 제1105호의 매각예정자산 기준을 충족하는 경우에는 매각예정비유동자산으로 분류할 수 있습니다.)\n\n[오답 해설]\n① 판매 목적으로 용도를 바꿨으나, 개발 시작 없이 즉시 매각하는 경우이므로 재고자산으로 갈 수 없습니다.\n② 자가사용 목적으로의 복원이 없으므로 유형자산으로 대체할 이유가 없습니다.\n④ 정상 매각 예정이므로 손상 사유에 해당하지 않습니다.\n⑤ 처분비용은 처분대가에서 차감되는 요소이므로 취득자산원가에 얹을 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "투자부동산을 재무상태표 상 자산으로 최초 인식하기 위해 동시에 충족해야 하는 인식 기준(Recognition criteria)으로 가장 올바른 것은?",
        "options": [
            "① 부동산의 소유권 등기가 법원에 공식 접수되고, 지방세 납부 영수증을 수령함",
            "② 부동산과 관련된 미래경제적효익의 유입 가능성이 높고, 부동산의 원가를 신뢰성 있게 측정할 수 있음",
            "③ 부동산의 시가가 취득원가보다 항상 높게 유지되고, 임차 보증금을 회수한 상태임",
            "④ 부동산을 제3자에게 최소 10년 이상 의무 리스해주기로 서면 서약하고 공정가치를 결정함",
            "⑤ 부동산 매입에 따른 금융 대출 만기가 도래하고 채권자의 채무 면제 승인이 완료됨"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1040호 문단 16에 따라 투자부동산은 다음 요건을 모두 충족할 때 자산으로 인식합니다.\n1. 부동산에 관련된 미래경제적효익이 기업에 유입될 가능성이 높다.\n2. 부동산의 원가를 신뢰성 있게 측정할 수 있다.\n\n[오답 해설]\n① 법률상 등기 접수나 세금 영수증은 인식 요건을 직접 강제하는 IFRS의 기준이 아닙니다.\n③ 시가가 취득원가보다 높아야 한다는 등 시세 관련 조건은 자산 인식의 통제 기준이 아닙니다.\n④, ⑤ 계약 기간의 장단점이나 자금 조달 조건 등은 자산 인식의 기본 요건에 속하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "K-IFRS 제1116호 '리스'에 따라 사용권자산을 인식한 임차인(리스이용자)이 해당 임차 건물을 다시 제3자에게 운용리스 조건으로 sublease(전대)하는 경우, 이 사용권자산의 올바른 분류 기준서는?",
        "options": [
            "① K-IFRS 제1016호 유형자산",
            "② K-IFRS 제1002호 재고자산",
            "③ K-IFRS 제1038호 무형자산",
            "④ K-IFRS 제1040호 투자부동산",
            "⑤ K-IFRS 제1115호 고객과의 계약에서 생기는 수익"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 임차인이라 하더라도 리스계약을 통해 통제권을 얻은 '사용권자산'을 다시 제3자에게 임대수익이나 차익 목적으로 운용리스 임대해 준 경우, 리스이용자의 재무상태표 상 해당 사용권자산은 K-IFRS 제1040호 '투자부동산'을 적용하여 계상 및 공시해야 합니다.\n\n[오답 해설]\n① 직접 사용 목적이 아닌 재임대 목적이므로 일반 유형자산 기준서가 아닙니다.\n②, ③ 일반 재고자산이나 무형자산 범주에 해당할 수 없는 물리적 부동산의 점유 사용권리입니다.\n⑤ 자산 분류 과목의 인식 및 측정을 규정하는 기준서가 아닌 수익 인식 모형 기준서입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s01-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "K-IFRS 제1016호에 규정된 '자가사용부동산'의 정의로 옳은 것은?",
        "options": [
            "① 임대수익이나 시세차익을 얻기 위하여 소유자가 보유하는 부동산",
            "② 재화나 용역의 생산 또는 제공, 타인에 대한 임대(운용리스 제외), 또는 관리활동에 사용하기 위하여 보유하는 부동산",
            "③ 통상적인 영업활동 과정에서 단기 매각을 목적으로 보유하는 부동산",
            "④ 리스이용자가 타인에게 금융리스로 양도하기 위해 일시적으로 보유하는 점유권",
            "⑤ 장래 신축 개발을 기획하여 매각 여부를 저울질하는 단계의 보유 부동산"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 자가사용부동산은 재화나 용역의 생산 또는 제공, 타인에 대한 임대(투자부동산 기준에 부합하는 운용리스 성격의 임대는 제외), 또는 관리활동에 사용하기 위하여 소유자나 리스이용자가 보유하는 부동산(토지, 건물 또는 둘 다)으로 정의되며, 유형자산 회계처리를 따릅니다.\n\n[오답 해설]\n① 투자부동산의 본질적 정의입니다.\n③ 재고자산의 성격에 해당합니다.\n④ 금융리스 임대인의 자산 양도 거래는 리스 자산 제거 사유입니다.\n⑤ 미결정 상태의 부동산 보유는 투자부동산 분류에 부합합니다.",
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
