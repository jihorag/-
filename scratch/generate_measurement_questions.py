import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

# Load existing questions
if DB_PATH.exists():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)
    print(f"Loaded existing {len(questions)} questions.")
else:
    questions = []
    print("No existing questions file found. Creating new list.")

new_questions = [
    # =========================================================================
    # L1: 기초 개념 (10문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s08-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "개념체계 상 재무제표에 인식된 요소를 화폐단위로 수량화하기 위해 측정 대상 항목에 대해 식별된 속성을 무엇이라 칭하는가?",
        "options": [
            "① 거래원가(Transaction Cost)",
            "② 감가상각 누계액(Accumulated Depreciation)",
            "③ 측정기준(Measurement Basis)",
            "④ 복식부기 장부(Double-entry Ledger)",
            "⑤ 회계단위(Unit of Account)"
        ],
        "answer": "3",
        "explanation": "③ 개념체계 상 재무제표에 인식된 요소들을 화폐단위로 수량화하기 위해 선택하는 대상 항목의 식별된 속성(예: 역사적 원가, 공정가치 등)을 '측정기준(Measurement Basis)'이라고 부릅니다.\n\n[오답 해설]\n① 거래원가는 측정에 영향을 주는 비용 요소일 뿐 측정기준 자체가 아닙니다.\n② 감가상각 누계액은 평가 조정 계정입니다.\n④ 복식부기 장부는 장부 기록 기술입니다.\n⑤ 회계단위는 인식기준과 측정개념이 적용되는 단위(자산/부채의 묶음 등)를 의미합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "거래원가는 거래 시 수반되는 비용 요소입니다.", "articles": [], "principle": "측정의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각누계액은 유형자산의 차감 항목입니다.", "articles": [], "principle": "측정의 의의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "측정기준은 자산/부채 등을 수량화하기 위해 식별된 속성을 뜻합니다.", "articles": [], "principle": "측정의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "복식부기 장부는 기입 기술입니다.", "articles": [], "principle": "측정의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계단위는 측정기준 등이 적용되는 자산/부채의 결합 또는 개별 단위를 말합니다.", "articles": [], "principle": "측정의 의의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "개념체계 상 자산을 취득하거나 창출할 때의 '역사적 원가(Historical Cost)'에 포함되는 구성 요소로 가장 올바른 것은?",
        "options": [
            "① 자산의 취득이나 창출을 위해 지급한 대가와 취득 시 발생한 거래원가",
            "② 자산을 1년 뒤에 매각할 때 시장에서 수취할 것으로 기대되는 미래 매각 금액",
            "③ 매 기말마다 발생한 자산의 단순 시가 변동분 전체",
            "④ 자산 취득 후 5년 동안 발생할 것으로 예상되는 미래 화재보험료 누계액",
            "⑤ 회사가 자산을 기부받았을 때 세법상 납부해야 하는 상속세 총액"
        ],
        "answer": "1",
        "explanation": "① 개념체계 상 자산의 역사적 원가는 자산의 취득 또는 창출에 발생한 원가의 가치로서, 자산의 취득을 위하여 지급한 대가와 거래원가를 포함하여 구성됩니다.\n\n[오답 해설]\n② 이는 미래 매각 예상치로 공정가치나 사용가치 성격에 가깝고 역사적원가가 아닙니다.\n③ 역사적원가는 자산의 단순 시가 변동을 추적 갱신하지 않습니다.\n④ 취득 후 발생하는 미래 비용은 취득 역사적 원가에 가산하지 않습니다.\n⑤ 기부 시 법적 세액 자체가 역사적원가의 보편적 구성요소가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "자산의 역사적 원가는 취득을 위해 지급한 대가와 거래원가를 포함합니다.", "articles": [], "principle": "역사적원가의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 매각 기대액은 현행가치 속성입니다.", "articles": [], "principle": "역사적원가의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가 변동 갱신액은 역사적원가에 들어가지 않습니다.", "articles": [], "principle": "역사적원가의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득 후 후속 비용(보험료 등)은 역사적원가 구성요소가 아닙니다.", "articles": [], "principle": "역사적원가의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "개별 상속세 등은 보편적인 역사적원가 구성에 들어가지 않습니다.", "articles": [], "principle": "역사적원가의 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "개념체계 상 부채가 발생하거나 인수할 때의 '역사적 원가(Historical Cost)'에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 부채를 발생시키면서 수취한 대가에 거래원가를 합산한 가치이다.",
            "② 부채를 발생시키거나 인수하면서 수취한 대가에서 거래원가를 차감한 가치이다.",
            "③ 부채가 완전히 만기 상환될 때 채권자에게 추가로 지급해야 할 벌칙 수수료이다.",
            "④ 부채의 공정가치 변동액을 매 기말마다 환율 변동 비율로 나눈 금액이다.",
            "⑤ 부채를 인수한 날로부터 1년 뒤의 기대 할인 이자율이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 부채가 발생하거나 인수할 때의 역사적 원가는 부채를 발생시키거나 인수하면서 수취한 대가에서 거래원가를 차감(차감한 가치)하여 산정합니다.\n\n[오답 해설]\n① 거래원가를 차감해야 하므로 합산한다는 설명은 오류입니다.\n③ 상환 시의 벌칙금 등은 역사적 원가의 정의가 아닙니다.\n④ 공정가치 및 환율 연계액 등은 갱신 정보이므로 역사적원가와 다릅니다.\n⑤ 할인 이자율 자체는 원가 수치가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수취 대가에서 거래원가를 빼야 하므로 합산은 틀렸습니다.", "articles": [], "principle": "부채 역사적원가", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부채의 역사적 원가는 수취 대가에서 거래원가를 차감한 순액 개념입니다.", "articles": [], "principle": "부채 역사적원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "벌칙 수수료 등은 원가의 본질적 정의가 아닙니다.", "articles": [], "principle": "부채 역사적원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치 및 환율 연동 설명은 현행가치 속성으로 역사적원가가 아닙니다.", "articles": [], "principle": "부채 역사적원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 이자율은 부채 역사적 원가의 가치가 아닙니다.", "articles": [], "principle": "부채 역사적원가", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "개념체계 상 현행가치(Current Value)의 대표적 측정기준인 '공정가치(Fair Value)'의 기본 정의로 가장 올바른 것은?",
        "options": [
            "① 측정일에 시장참전자 사이의 정상거래에서 자산을 매도할 때 받거나 부채를 이전할 때 지급하게 될 가격",
            "② 기업이 자산의 사용과 궁극적인 처분으로 얻을 것으로 기대하는 현금흐름의 현재가치",
            "③ 보고기업의 임직원들이 자산의 미래 장부 가액을 임의로 결정해 기록한 금액",
            "④ 정부 공인 감정평가사가 자산의 취득 가격을 매년 역사적 원가로 고정해 둔 수치",
            "⑤ 회사의 대표이사가 자식을 위해 상속할 주식 가치 총액"
        ],
        "answer": "1",
        "explanation": "① 개념체계 상 공정가치는 측정일에 시장참전자 사이의 정상거래에서 자산을 매도할 때 받거나 부채를 이전할 때 지급하게 될 가격(유출가격)으로 정의됩니다.\n\n[오답 해설]\n② 이는 자산의 사용가치(Value in Use)의 정의입니다.\n③ 기업 내부의 임의 가액 결정액이 아닙니다.\n④ 역사적 원가 고정액은 현행가치인 공정가치와 정반대 개념입니다.\n⑤ 개인의 상속 주식 가치는 보고 실체 공정가치의 회계적 정의가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "공정가치는 측정일 시장참전자 간 정상거래 하의 자산 매도/부채 이전 유출가격입니다.", "articles": [], "principle": "공정가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이는 자산의 사용가치에 해당하는 정의입니다.", "articles": [], "principle": "공정가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 결정 수치는 공정가치가 아닙니다.", "articles": [], "principle": "공정가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적 원가 고정액은 역사적원가 기준을 뜻합니다.", "articles": [], "principle": "공정가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사적 자산 상속액 설명은 무관합니다.", "articles": [], "principle": "공정가치 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "개념체계 상 자산의 현행가치 측정기준인 '사용가치(Value in Use)'의 기본 정의로 가장 올바른 것은?",
        "options": [
            "① 기업이 자산의 사용과 궁극적인 처분으로 얻을 것으로 기대하는 현금흐름 또는 그 밖의 경제적효익의 현재가치",
            "② 자산을 현재 시장에서 즉시 처분할 때 발생하는 거래원가를 가산한 역사적 가격",
            "③ 동등한 자산을 측정일에 새로 취득할 때 지급해야 하는 미래 예상 거래원가의 합계",
            "④ 정부 세무관서가 자산에 대해 한도 승인한 당기 감가상각비의 총액",
            "⑤ 회사가 자산을 보증하기 위해 금융회사에 지급한 대출 수수료"
        ],
        "answer": "1",
        "explanation": "① 개념체계 상 자산의 사용가치는 기업이 자산의 사용과 궁극적인 처분으로 얻을 것으로 기대하는 현금흐름 또는 그 밖의 경제적효익의 현재가치로 정의됩니다.\n\n[오답 해설]\n② 처분 거래원가를 더한 역사적 가격은 사용가치와 맞지 않습니다.\n③ 측정일에 새로 취득할 때의 원가는 현행원가(Current Cost) 개념에 대응됩니다.\n④ 세무 감가상각 한도액은 사용가치 정의와 다릅니다.\n⑤ 대출 수수료는 부채 역사적원가 거래원가 등에 해당할 수 있으나 자산 사용가치가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "사용가치는 자산 사용 및 궁극적 처분으로 유입될 미래 효익의 현재가치입니다.", "articles": [], "principle": "사용가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래원가를 더한 역사적 가액은 사용가치의 정의가 아닙니다.", "articles": [], "principle": "사용가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정일 취득 대가와 원가는 현행원가의 속성입니다.", "articles": [], "principle": "사용가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각 한도는 회계적 사용가치 정의가 아닙니다.", "articles": [], "principle": "사용가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융 대출 수수료는 사용가치와 무관합니다.", "articles": [], "principle": "사용가치 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "개념체계 상 부채의 현행가치 측정기준인 '이행가치(Fulfilment Value)'의 기본 정의로 가장 올바른 것은?",
        "options": [
            "① 기업이 부채를 이행할 때 이전해야 하는 현금이나 그 밖의 경제적자원의 현재가치",
            "② 부채를 인수할 당시 채권자에게 납품한 재고자산의 역사적 원가",
            "③ 부채 이자율 상승으로 주주들에게 분배해야 할 현금 배당금의 예상 총액",
            "④ 금융기관이 부채에 대한 만기 보증 조건으로 기업에 빌려준 자산의 감가상각 가치",
            "⑤ 회사가 부채를 이행하지 않기로 서면 합의하고 면제받은 채무면제이익 총량"
        ],
        "answer": "1",
        "explanation": "① 개념체계 상 부채의 이행가치란 기업이 부채를 이행할 때 이전해야 하는 현금이나 그 밖의 경제적자원의 현재가치로 정의됩니다.\n\n[오답 해설]\n② 재고자산의 역사적 원가는 이행가치의 정의와 직접적 상관이 없습니다.\n③ 배당금 예상액은 부채의 이행가치 정의가 아닙니다.\n④ 금융기관 대여 자산 상각액은 부채 이행가치와 무관합니다.\n⑤ 면제받은 이익은 의무의 사후적 소멸 사실일 뿐 이행가치의 개념 정의가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "이행가치는 부채 이행 시 필요한 현금 등 경제적자원의 유출액에 대한 현재가치입니다.", "articles": [], "principle": "이행가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고자산의 취득원가는 이행가치와 다릅니다.", "articles": [], "principle": "이행가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주주 배당금 설명은 부채의 이행가치 정의와 무관합니다.", "articles": [], "principle": "이행가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보증 연계 감가액은 부채 이행가치가 아닙니다.", "articles": [], "principle": "이행가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채무면제이익은 제거 및 처리에 따른 손익으로 정의와 구분됩니다.", "articles": [], "principle": "이행가치 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "개념체계 상 자산의 현행가치 측정기준인 '현행원가(Current Cost)'의 기본 정의로 가장 올바른 것은?",
        "options": [
            "① 측정일에 동등한 자산의 원가로서 측정일에 지급할 대가와 그 날에 발생할 거래원가를 포함한 가치",
            "② 자산을 10년 전에 처음 매입하였을 때 실제로 영수증에 찍힌 취득 대금의 고정 가치",
            "③ 자산의 가치를 영구 보존하기 위해 기말마다 장부에서 감가상각하지 않고 누적해 둔 금액",
            "④ 자산 처분 시 미래에 받을 것으로 예상되는 배당금 기대 현재가치",
            "⑤ 자산 소유주가 개인적으로 자산을 사용할 때 창출되는 주관적인 기쁨을 화폐로 환산한 수치"
        ],
        "answer": "1",
        "explanation": "① 개념체계 상 자산의 현행원가는 측정일에 동등한 자산의 원가로서 측정일에 지급할 대가와 그 날에 발생할 거래원가를 포함하여 평가됩니다.\n\n[오답 해설]\n② 이는 역사적 원가(Historical Cost)에 해당합니다.\n③ 감가상각 보존액 등은 현행원가 정의와 정면 배치됩니다.\n④ 처분 미래 유입 배당금은 사용가치 혹은 배당 평가 모형 관련 기술입니다.\n⑤ 주관적인 효용 가치는 회계학적 현행원가 정의가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "현행원가는 측정일 현재 동등한 자산의 취득에 소요될 대가와 당일 거래원가를 포함합니다.", "articles": [], "principle": "현행원가 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "10년 전 취득 시 실제 지급액은 역사적 원가입니다.", "articles": [], "principle": "현행원가 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각 미실시 누적액은 회계 원리에 어긋납니다.", "articles": [], "principle": "현행원가 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분 배당 현가는 현행원가의 정의가 아닙니다.", "articles": [], "principle": "현행원가 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주관적인 사용 효용은 현행원가가 아닙니다.", "articles": [], "principle": "현행원가 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "개념체계 상 공정가치(Fair Value)를 측정할 때, 자산 취득이나 처분 시 동반되는 '거래원가(Transaction Cost)'의 반영 규칙으로 가장 올바른 것은?",
        "options": [
            "① 자산 취득 거래원가는 공정가치에 무조건 더하고 처분 거래원가는 무조건 뺀다.",
            "② 공정가치는 거래원가로 인해 증가하거나 감소하지 않으며, 자산의 취득이나 처분에서 발생하는 거래원가를 일체 반영하지 않는다.",
            "③ 거래원가의 10배를 계산하여 공정가치에서 강제 차감 처리한다.",
            "④ 거래원가가 발생할 때마다 전액 주주들의 현금 출자금(납입자본)으로 직접 상계한다.",
            "⑤ 거래원가 정보가 입수되지 않는 한 공정가치 평가는 법적으로 무조건 무효가 된다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 공정가치는 특정 자산/부채를 거래시킨 거래나 사건의 가격으로부터 도출되는 투입원가가 아니기 때문에, 취득 시 거래원가로 인해 증가하지 않고 처분 거래원가로 인해 감소하지도 않습니다. 즉, 거래원가를 반영하지 않습니다.\n\n[오답 해설]\n① 거래원가를 가산/차감하는 방식은 역사적원가나 현행원가 및 일부 사용가치 모형의 속성이며 공정가치는 이를 미반영합니다.\n③, ④, ⑤는 회계 이론과 동떨어진 극단적인 가공 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "취득 거래원가를 더하는 방식은 역사적원가 등의 규칙이며 공정가치는 거래원가를 배제합니다.", "articles": [], "principle": "공정가치와 거래원가", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치는 시장참전자 관점의 유출가격이므로 거래 자체의 수반 원가(거래원가)로 증감하지 않습니다.", "articles": [], "principle": "공정가치와 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "10배 강제 차감 등은 터무니없는 기술입니다.", "articles": [], "principle": "공정가치와 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "납입자본과의 강제 상계 처리는 올바르지 않습니다.", "articles": [], "principle": "공정가치와 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래원가가 파악되지 않아도 시장 관측치 등을 통해 공정가치 평가가 가능합니다.", "articles": [], "principle": "공정가치와 거래원가", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "개념체계 상 역사적원가(Historical Cost) 측정기준과 현행가치(Current Value) 측정기준의 가장 본질적이고 이론적인 차이점은?",
        "options": [
            "① 역사적원가는 달러화로만 기록하고 현행가치는 원화로만 기록한다는 점",
            "② 역사적원가는 측정일 현재의 최신 조건으로 가치를 계속 갱신하는 반면, 현행가치는 취득 당시 최초 금액을 절대 바꾸지 않는다는 점",
            "③ 역사적원가는 자산 취득 당시 최초 사건의 가격을 반영하고 시가 변동을 갱신하지 않는 반면, 현행가치는 측정일의 최신 정보를 반영하여 금액을 계속 갱신한다는 점",
            "④ 역사적원가는 세무서에 보고할 때만 쓰고 현행가치는 주주총회 발표 때만 제한적으로 쓴다는 점",
            "⑤ 두 기준의 장부상 표기 폰트와 소수점 자릿수 규정이 완전히 상이하다는 점"
        ],
        "answer": "3",
        "explanation": "③ 역사적원가는 취득/발생 당시의 과거 사건 가격을 유지하고 평가 증액 등의 갱신을 하지 않지만, 현행가치는 측정일 현재의 시장 조건과 기대치를 반영하기 위해 최신 정보로 갱신하는 측정 방식입니다.\n\n[오답 해설]\n① 화폐 단위는 동일하게 적용됩니다.\n② 갱신의 유무 설명이 반대로 서술되어 오답입니다.\n④ 두 기준 모두 보고 목적에 따라 재무제표 전체에 통합 적용될 수 있습니다.\n⑤ 폰트 등은 측정기준의 이론적 본질 차이가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "화폐 단위 기재 규칙과는 무관합니다.", "articles": [], "principle": "역사적원가 vs 현행가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "설명이 반대로 꼬여 있어 틀렸습니다(역사적원가가 고정이고 현행가치가 갱신).", "articles": [], "principle": "역사적원가 vs 현행가치", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "역사적원가는 거래 시점 원가를 고수하며, 현행가치는 측정일 현재 시점으로 정보를 계속 업데이트합니다.", "articles": [], "principle": "역사적원가 vs 현행가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "제출 대상에 따른 제한 규정 설명은 사실이 아닙니다.", "articles": [], "principle": "역사적원가 vs 현행가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인쇄 양식이나 소수점 차이는 기준의 본질이 아닙니다.", "articles": [], "principle": "역사적원가 vs 현행가치", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "개념체계 상 사용가치(Value in Use)나 이행가치(Fulfilment Value)처럼 시장에서 직접 관측되는 가격이 없어 이를 산출하고자 할 때 주로 동원되는 측정 기법은?",
        "options": [
            "① 거래처 주주들의 평판 조사 기법",
            "② 현금흐름기준 측정기법(Cash Flow-based Measurement Technique)",
            "③ 단순 선입선출 자산 재고 실사법",
            "④ 기말 주가 총액의 1/N 배분 비율 산출법",
            "⑤ 회계사의 연차에 비례한 임의 가산 가치 추정법"
        ],
        "answer": "2",
        "explanation": "② 사용가치와 이행가치는 시장에서 직접 관측할 수 없기 때문에, 미래 현금흐름의 유출입액을 합리적으로 추정하여 현재가치화하는 '현금흐름기준 측정기법'을 사용하여 결정합니다.\n\n[오답 해설]\n① 주주 평판은 자산 평가 기법이 아닙니다.\n③ 선입선출은 재고자산 흐름 가정 기법이지 현가 평가 기법이 아닙니다.\n④, ⑤는 회계 이론에 존재하지 않는 인위적이고 잘못된 추정법입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "평판 조사는 사용가치 측정 도구가 아닙니다.", "articles": [], "principle": "현금흐름 기법의 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사용가치와 이행가치는 미래 기대 현금흐름의 현재가치에 기초하므로 현금흐름기준 측정기법이 사용됩니다.", "articles": [], "principle": "현금흐름 기법의 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고 실사법은 물량 흐름 파악을 위함입니다.", "articles": [], "principle": "현금흐름 기법의 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가총액의 1/N 배분 등은 엉터리 기술입니다.", "articles": [], "principle": "현금흐름 기법의 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계사의 직무 연차와 평가 금액은 비례하지 않습니다.", "articles": [], "principle": "현금흐름 기법의 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },

    # =========================================================================
    # L2: 이해 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s08-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "개념체계 상 공정가치(Fair Value)가 반영하는 가치 평가의 주체적 관점은?",
        "options": [
            "① 해당 자산을 실재로 보유하여 사적 유보 시너지를 내고 있는 특정 보고기업 자체의 관점",
            "② 기업이 접근할 수 있는 시장의 시장참전자(Market Participants) 관점",
            "③ 관할 세무서 소속 법인세 조사관의 세무 사법적 관점",
            "④ 보고기업에 자본을 단 1주만 투자한 소액 주주 개인의 주관적 관점",
            "⑤ 자산의 원래 고안자나 발명가가 책정한 감정가 관점"
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 공정가치는 특정 기업의 개별 시너지를 무시하고, 기업이 접근할 수 있는 활성 시장의 '시장참전자 관점'을 반영하여 그들이 가격을 결정할 때 사용할 가정과 동일한 가정을 사용하여 측정합니다.\n\n[오답 해설]\n① 이는 기업 특유의 관점(사용가치)에 대한 기술로 공정가치와 다릅니다.\n③, ④, ⑤는 공정가치 측정 관점이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "보고기업 자체의 시너지나 의도는 공정가치에 들어가지 않으며 이는 사용가치에 들어갑니다.", "articles": [], "principle": "공정가치 관점", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치는 시장참전자 관점을 반영하는 독립적인 시장 기준 평가액입니다.", "articles": [], "principle": "공정가치 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 공무원의 관점은 회계 상 공정가치 측정 대상이 아닙니다.", "articles": [], "principle": "공정가치 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소액주주 개인 관점은 배제됩니다.", "articles": [], "principle": "공정가치 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "발명가 주관적 감정가도 회계 상 공정가치와 다릅니다.", "articles": [], "principle": "공정가치 관점", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "개념체계 상 사용가치(Value in Use)와 이행가치(Fulfilment Value)가 반영하는 가치 평가의 핵심적 관점은?",
        "options": [
            "① 거래처 신용도 변동을 배제하는 정부 관청 관점",
            "② 일반적인 평균 시장참전자(Market Participants)들의 공통 관점",
            "③ 보고기업 특유의 관점(Entity-specific Perspective)",
            "④ 금융업계 애널리스트들의 종합 합산 관점",
            "⑤ 회사의 경쟁 우위 경쟁사들이 평가한 위협 가치 관점"
        ],
        "answer": "3",
        "explanation": "③ 사용가치와 이행가치는 시장 참여자 일반의 평가가 아니라, 해당 자산/부채를 실제로 운용·결제하는 보고기업이 처한 특수한 상황이나 결합 시너지, 의도 등을 반영하는 '보고기업 특유의 관점(Entity-specific Perspective)'을 반영합니다.\n\n[오답 해설]\n① 세무/정부 관점과 관련이 없습니다.\n② 이는 공정가치의 관점입니다.\n④ 애널리스트의 관점도 기업특유관점과 다릅니다.\n⑤ 경쟁사의 관점은 회계 평가 기준이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "정부/관청의 행정적 시각이 반영되는 것이 아닙니다.", "articles": [], "principle": "기업특유관점의 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시장참전자들의 관점은 공정가치의 영역입니다.", "articles": [], "principle": "기업특유관점의 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사용가치와 이행가치는 자산 사용 주체인 보고기업 특유의 현금흐름 기대를 집계하는 기업 특유의 관점입니다.", "articles": [], "principle": "기업특유관점의 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "애널리스트들의 전망치 집합이 아닙니다.", "articles": [], "principle": "기업특유관점의 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경쟁사의 위협 가치 추산은 관련이 없습니다.", "articles": [], "principle": "기업특유관점의 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "개념체계 상 역사적원가(Historical Cost) 측정기준 하에서도 시간이 경과함에 따라 자산이나 부채의 장부 가액이 감액되거나 변경 조정될 수 있는 타당한 사유로 가장 옳지 않은 것은?",
        "options": [
            "① 감가상각이나 아모티제이션(상각)을 통한 자산 소모액 배분",
            "② 자산의 가치가 회수 불가 수준으로 급락하여 인식하는 자산손상(Impairment)",
            "③ 미이행계약이 불리하게 전락하여 인식하는 부채의 손실부담액 가산",
            "④ 기말 시가 변동에 따른 자산의 임의적이고 정기적인 재평가 평가증",
            "⑤ 금융 부채에 적용되는 유효이자율법 하의 이자비용 누적 가산 및 상각"
        ],
        "answer": "4",
        "options": [
            "① 감가상각이나 상각을 통한 자산 소모액 배분",
            "② 자산의 가치가 회수 불가 수준으로 급락하여 인식하는 자산손상(Impairment)",
            "③ 미이행계약이 불리하게 전락하여 인식하는 부채의 손실부담액 가산",
            "④ 기말 시가 상승에 따른 자산의 정기적인 재평가 평가증(Revaluation)",
            "⑤ 금융 부채에 적용되는 유효이자율법 하의 이자 누적 상각"
        ],
        "answer": "4",
        "explanation": "④ 역사적원가 측정기준 하에서는 시장 가격 상승에 따른 자산 재평가 평가증 등의 시가 변동 정보 반영 갱신을 허용하지 않습니다. (재평가모형은 현행가치 요소를 역사적원가에 결합한 예외 모형이거나 별개의 모형입니다.)\n\n[오답 해설]\n①, ②, ③, ⑤는 역사적원가 하에서도 발생주의 및 회수가능성 반영을 위해 예외 없이 인정되는 역사적원가 조정액 범주(상각, 손상, 유효이자 상각, 손실부담)에 속하므로 올바릅니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상각은 역사적원가 배분 절차로 역사적원가주의 내에서 당연 인정됩니다.", "articles": [], "principle": "역사적원가의 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 손상은 역사적원가 하에서도 감액 반영해야 하는 필수 항목입니다.", "articles": [], "principle": "역사적원가의 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손실부담의무 가산은 부채 역사적원가 하의 손실 반영액입니다.", "articles": [], "principle": "역사적원가의 조정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "역사적원가는 자산의 시가 상승 정보를 장부에 가산하여 업데이트하지 않는 것이 고유한 특징이므로 4가 오답입니다.", "articles": [], "principle": "역사적원가의 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각후원가(유효이자율법)는 역사적원가 체계 하의 정당한 부채 조정액입니다.", "articles": [], "principle": "역사적원가의 조정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "개념체계 상 부채의 '공정가치(Fair Value)'를 평가할 때, 부채 가액 결정에 반영되어 고려되어야 하는 신용위험 요소로 가장 올바른 것은?",
        "options": [
            "① 거래 상대방이 부채를 이행하지 못할 위험(신용위험)만 반영하고, 자기 신용위험은 전혀 무시한다.",
            "② 상대방의 신용위험은 물론이고, 보고기업 자체가 자사의 부채를 이행하지 못할 가능성(자기 신용위험)도 모두 반영한다.",
            "③ 국가의 부도 위험인 국가 신용등급 변동만을 100% 반영한다.",
            "④ 금융감독원장이 고시하는 기준 부도율을 곱해 계산하되, 세무 상 가산세만 부채로 계상한다.",
            "⑤ 부채를 계상한 후에는 어떠한 신용등급 변동이나 파산확률 변동도 절대 반영할 수 없다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 공정가치는 상대방이 기업에 대한 의무를 불이행할 신용위험과, 기업 자체가 자신의 부채를 이행하지 못할 가능성인 '자기 신용위험(Own Credit Risk)'을 모두 가격(공정가치) 결정 과정에 반영합니다.\n\n[오답 해설]\n① 자기 신용위험도 포함하여 공정가치를 결정해야 합니다.\n③ 국가 신용만을 단독 100% 반영하는 공식은 없습니다.\n④ 세무 상 가산세 등의 임의 계상 지침은 사실과 무관합니다.\n⑤ 공정가치는 매 측정일마다 신용위험 변동을 실시간 업데이트하므로 반영 불가는 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자기 신용위험도 공정가치 산출 시 반드시 포함되어야 합니다.", "articles": [], "principle": "부채 공정가치와 신용위험", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "개념체계 상 부채 공정가치는 거래상대방 신용위험과 자사의 자기신용위험을 모두 내포하여 측정됩니다.", "articles": [], "principle": "부채 공정가치와 신용위험", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "국가 리스크 단독 결정이 아닙니다.", "articles": [], "principle": "부채 공정가치와 신용위험", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가산세 연동 규정 등은 사실무근입니다.", "articles": [], "principle": "부채 공정가치와 신용위험", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정일의 최신 신용 등급 상태를 계속 반영하여 공정가치를 갱신해야 합니다.", "articles": [], "principle": "부채 공정가치와 신용위험", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "개념체계 상 자산의 사용가치(Value in Use)와 부채의 이행가치(Fulfilment Value)를 결정할 때, '거래원가(Transaction Cost)'의 포함 및 반영 여부에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 자산을 취득하거나 부채를 인수할 때 발생하는 거래원가를 포함하여 계산한다.",
            "② 자산을 취득하거나 부채를 인수할 때 발생하는 거래원가는 포함하지 않으나, 자산을 궁극적으로 처분하거나 부채를 이행할 때 발생할 거래원가의 현재가치는 포함한다.",
            "③ 처분 거래원가는 전액 제외하고 오직 최초 취득 시 발생한 원가만을 고정 반영한다.",
            "④ 거래원가의 모든 요소를 비용이나 자산 가액에 전혀 반영하지 않고 전액 무시한다.",
            "⑤ 취득 거래원가와 처분 거래원가를 모두 합산하여 즉시 주주 지분 배당금에서 강제 차감한다."
        ],
        "answer": "2",
        "explanation": "② 사용가치와 이행가치는 미래에 유입/유출될 기대현금흐름에 기초하므로, 과거 사건인 최초 취득/인수 시 발생한 거래원가는 포함되지 않습니다. 그러나 미래에 발생할 것으로 기대되는 처분/이행 시의 거래원가의 현재가치는 미래 유출 현금흐름의 일부이므로 포함됩니다.\n\n[오답 해설]\n① 취득/인수 거래원가는 포함하지 않습니다.\n③, ④, ⑤는 사용가치/이행가치 내의 거래원가 규칙과 어긋납니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "과거 취득 시 거래원가는 미래 가치 유입 평가인 사용가치에 가산하지 않습니다.", "articles": [], "principle": "사용/이행가치와 거래원가", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사용가치/이행가치는 미래 지향적이므로 취득 시 원가는 미포함하되, 처분/이행 단계 예상 원가의 현재가치는 미래 흐름에 산입합니다.", "articles": [], "principle": "사용/이행가치와 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "설명이 반대로 작성되었습니다.", "articles": [], "principle": "사용/이행가치와 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분 원가 현재가치를 미래 현금흐름으로 포함하므로 완전 무시는 오답입니다.", "articles": [], "principle": "사용/이행가치와 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "배당금 직접 차감 분개는 타당성 없는 왜곡 기재입니다.", "articles": [], "principle": "사용/이행가치와 거래원가", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "개념체계 상 현행원가(Current Cost)와 역사적원가(Historical Cost)의 공통 속성 및 결정적 차이점에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 둘 다 자산 처분 시 유입되는 '유출가치(Exit Value)'이나, 현행원가는 미래 시점을 기준으로 한다는 점이 다르다.",
            "② 둘 다 자산의 조달에 초점을 맞추는 '투입가치(Entry Value)'이나, 역사적원가는 최초 취득 시 가격이고 현행원가는 측정일 현재 기준 가격이라는 점이 다르다.",
            "③ 둘 다 기업 내부의 특유 가치를 나타내는 기업특유가치이나, 역사적원가만 주석에 기재된다는 점이 다르다.",
            "④ 둘 다 활성시장의 관측 불필요 가격이나, 현행원가만 세무서 조세 산정의 단독 잣대로 인정된다는 점이 다르다.",
            "⑤ 둘 다 취득 거래원가를 무조건 배제하지만, 현행원가는 처분 원가를 강제 가산한다는 점이 다르다."
        ],
        "answer": "2",
        "explanation": "② 역사적원가와 현행원가는 자산을 새로이 취득/조달하는 과정에 근거하므로 '투입가치(Entry Value)' 속성을 공유합니다. 단, 역사적원가는 최초 취득 시점에 고정되어 갱신되지 않고, 현행원가는 매 측정일의 시점으로 가격이 갱신(측정일 현재 동등한 자산의 조달 대가)된다는 차이가 있습니다.\n\n[오답 해설]\n① 둘 다 유입가치(투입가치)이므로 유출가치가 아닙니다.\n③ 기업특유관점은 사용가치/이행가치에 적용되며, 역사적원가와 현행원가는 시장 거래 조건에 맞춥니다.\n④ 세무 단독 잣대로만 사용되지 않습니다.\n⑤ 둘 다 취득/인수 거래원가를 각각 가산/차감하므로 배제 진술은 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "두 속성은 취득을 전제하므로 유출가치가 아닌 투입가치입니다.", "articles": [], "principle": "역사적원가 vs 현행원가", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "둘 다 조달 투입가치이나 역사적원가는 취득 시점 고정, 현행원가는 측정일 시점 갱신이라는 점이 다릅니다.", "articles": [], "principle": "역사적원가 vs 현행원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "두 기준은 기업특유 관점을 중점 반영하지 않습니다(시장 기준 조달 가격).", "articles": [], "principle": "역사적원가 vs 현행원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 조사 전용의 조세 산정 수치가 아닙니다.", "articles": [], "principle": "역사적원가 vs 현행원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득 거래원가를 포함하므로 배제한다는 서술은 오류입니다.", "articles": [], "principle": "역사적원가 vs 현행원가", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "개념체계 상 공정가치(Fair Value)와 사용가치(Value in Use)의 '거래원가(Transaction Cost)' 반영 차이에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 공정가치는 취득 거래원가를 가산하는 반면, 사용가치는 취득 거래원가를 완전 배제한다.",
            "② 공정가치와 사용가치 모두 취득 및 처분 거래원가를 동일한 수준으로 100% 장부 가치에 가산한다.",
            "③ 공정가치는 취득 및 처분과 관련된 거래원가를 일체 가액에 반영하지 않지만, 사용가치는 취득 원가는 미포함하되 미래 처분 시의 거래원가 현재가치는 미래 기대유출 현금흐름으로 포함한다.",
            "④ 공정가치는 처분 거래원가의 현재가치를 차감하지만, 사용가치는 이자율의 변동폭만큼 가산한다.",
            "⑤ 사용가치에만 조세 한도 상의 거래 관세를 전액 가산하고 공정가치에는 임의 비율로 뺀다."
        ],
        "answer": "3",
        "explanation": "③ 공정가치는 시장참전자 관점의 유출가격으로 자산 취득/처분 거래원가를 가산/차감하지 않고 완전 배제합니다. 사용가치는 기업특유 미래 현금흐름이므로 취득 거래원가는 배제하되, 미래 발생 기대 처분원가는 유출액에 포함(현재가치화하여 차감 유도)하는 차이가 있습니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 두 기준의 상이한 거래원가 회계 처리 지침을 왜곡되게 설명하였습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "공정가치는 취득 거래원가를 가산하지 않습니다.", "articles": [], "principle": "거래원가 반영 차이", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "동일하게 가산하는 구조가 아닙니다.", "articles": [], "principle": "거래원가 반영 차이", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치는 원가 배제 원칙을 쓰며, 사용가치는 미래 처분 거래원가의 현가만을 미래 유출 흐름에 포함시킵니다.", "articles": [], "principle": "거래원가 반영 차이", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치는 처분원가를 차감하지 않습니다.", "articles": [], "principle": "거래원가 반영 차이", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "관세 관련 설명은 임의의 오답 진술입니다.", "articles": [], "principle": "거래원가 반영 차이", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "개념체계 상 부채의 역사적원가(Historical Cost)를 계산할 때, 부채 인수 시 발생한 '거래원가(Transaction Cost)'를 수취 대가에서 차감하여 산정하는 회계 처리의 이론적 성격은?",
        "options": [
            "① 거래원가만큼 최초 부채의 인식 장부금액을 감소시켜, 실질 부채 가액을 순수 수취액 수준으로 맞추는 것",
            "② 최초 거래처에 지급할 리베이트 가액을 장부에서 숨겨 부식을 유도하는 것",
            "③ 부채의 만기를 단축시켜 대금 회수를 촉진하는 편법을 쓰는 것",
            "④ 거래원가를 전액 무형자산인 영업권으로 위장 인식하여 자산총액을 과다 계상하려는 것",
            "⑤ 이자비용을 당해 연도 세법상 전액 면제받기 위해 자본금을 줄여주는 처리"
        ],
        "answer": "1",
        "explanation": "① 부채 역사적 원가 산정 시 거래원가를 수취 대금에서 차감하는 처리는, 자금을 조달할 때 거래 비용이 빠져나간 실제 순 조달액 수준으로 최초 부채의 평가액을 계상하여 기간 경과에 따라 유효이자 상각을 통해 이자비용으로 가산되도록 설계된 조치입니다.\n\n[오답 해설]\n② 리베이트 은폐나 부식 목적이 아닙니다.\n③ 채무 만기 단축과는 연관성이 없습니다.\n④ 영업권 위장 계상은 분식회계로 엄금됩니다.\n⑤ 세법 면제나 자본금 감소 목적의 기재가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "부채 역사적원가에서 거래원가를 빼 주는 것은 실제 유입된 순 경제적자원의 수준으로 최초 장부액을 설정하기 위함입니다.", "articles": [], "principle": "부채 역사적원가 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부정적 의도나 리베이트 은폐와 무관합니다.", "articles": [], "principle": "부채 역사적원가 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 만기 변동과는 상관이 없습니다.", "articles": [], "principle": "부채 역사적원가 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업권 가공 기재 분식 행위가 아닙니다.", "articles": [], "principle": "부채 역사적원가 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세금 면제 목적의 자본 감자 지침은 사실이 아닙니다.", "articles": [], "principle": "부채 역사적원가 거래원가", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "개념체계 상 재무보고 자산·부채의 측정기준을 선택할 때 고려할 요인에 대한 기술 중 가장 올바른 것은?",
        "options": [
            "① 특정 측정기준이 언제나 최고의 정보만을 산출하도록 지명하는 단일의 결정적인 요인이 존재한다.",
            "② 대부분의 경우, 어떤 측정기준을 선택해야 하는지를 결정하는 단일의 요인은 존재하지 않으며 여러 요인(목적적합성, 표현충실성, 보강적 특성, 원가제약)을 종합 고려해야 한다.",
            "③ 오직 자금 조달에 소요되는 금융 비용만을 단일 결정 요인으로 두어야 한다.",
            "④ 대표이사의 연도별 경영 성과 성과급 책정 기준만이 유일한 측정 선택 기준이 된다.",
            "⑤ 회사의 세무 조사를 회피할 수 있는 세무상 징수액 최소 기준만으로 측정방법을 정한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 어떤 측정기준을 선택해야 하는지를 결정하는 단일의 요인은 없음을 분명히 하고 있으며, 재무제표가 유용한 정보를 제공할 수 있도록 여러 유용성 및 제약 요건을 종합적으로 저울질하여 선택할 것을 요구합니다.\n\n[오답 해설]\n① 단일 결정 요인은 없습니다.\n③, ④, ⑤는 사적인 보상이나 규제 회피 등을 기준으로 측정기준을 선택하려는 잘못된 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "단일의 완벽한 요인이 지명되어 있지는 않습니다.", "articles": [], "principle": "측정기준 선택 요인", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "개념체계 상 측정기준의 선택은 목적적합성과 표현충실성 및 제반 질적 요건과 원가제약을 복합 비교하여 결정합니다.", "articles": [], "principle": "측정기준 선택 요인", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조달 비용 단독 결정론은 오답입니다.", "articles": [], "principle": "측정기준 선택 요인", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대표의 성과급 설계만을 측정 기준으로 삼지 않습니다.", "articles": [], "principle": "측정기준 선택 요인", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 조사 리스크 최소화 방침은 정규 재무보고 측정기준 선택의 결정요인이 아닙니다.", "articles": [], "principle": "측정기준 선택 요인", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "개념체계 상 정보의 보강적 질적 특성 중 '검증가능성(Verifiability)' 관점에서 역사적원가(Historical Cost)와 사용가치(Value in Use)의 비교 설명으로 가장 옳은 것은?",
        "options": [
            "① 사용가치는 계약서에 실제 찍힌 금액을 보존하므로 역사적원가보다 언제나 검증가능성이 월등히 높다.",
            "② 역사적원가는 과거의 실제 거래 사실에 근거하여 영수증 등 객관적 증빙 검증이 용이한 반면, 사용가치는 기업 내부의 주관적이고 독자적인 추정치에 기초하므로 상대적으로 검증가능성이 낮거나 어렵다.",
            "③ 두 기준 모두 검증가능성이 완벽하게 0이므로 회계감사인의 감사의견 서명 대상에서 원천 배제된다.",
            "④ 검증가능성 확보를 위해 사용가치 정보만을 장부에 기재하고 역사적원가는 소각해야 한다.",
            "⑤ 두 기준의 검증가능성은 매 분기 주가 수준 변동의 비율에 비례하여 강제 고정 대칭된다."
        ],
        "answer": "2",
        "explanation": "② 역사적원가는 거래 영수증, 계약서 등 독립적인 외부 증빙을 통해 확인하기 쉬워 검증가능성이 높습니다. 반면, 사용가치는 기업 특유의 가정(미래 매출 예상, 내부 할인율)에 의존하므로 외부 이용자나 감사인이 이를 객관적으로 검증하기가 비교적 까다롭고 검증가능성이 낮습니다.\n\n[오답 해설]\n① 사용가치는 실제 영수증 고정 금액이 아니며 추정치이므로 오답입니다.\n③ 감사의견 부여 대상입니다.\n④ 역사적원가를 임의 소각한다는 설명은 허위입니다.\n⑤ 주가 수준과 검증가능성의 강제 연동 비율은 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "사용가치는 추정 정보이므로 영수증에 기초한 역사적원가보다 검증가능성이 낮습니다.", "articles": [], "principle": "검증가능성과 측정기준", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "역사적원가는 객관적 실증이 쉬워 검증가능성이 높으나, 사용가치는 기업 특유의 미래 추정 요소를 써서 검증이 비교적 어렵습니다.", "articles": [], "principle": "검증가능성과 측정기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "검사 불능 상태가 아니며 정상 의견 표명 대상입니다.", "articles": [], "principle": "검증가능성과 측정기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적원가를 소각할 필요는 없습니다.", "articles": [], "principle": "검증가능성과 측정기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주가 변동과 검증도 간의 강제 수학적 정비례 비례 공식은 회계에 없습니다.", "articles": [], "principle": "검증가능성과 측정기준", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "개념체계 상 정보의 보강적 질적 특성 중 '적시성(Timeliness)'의 극대화 측면에서 역사적원가(Historical Cost) 대비 현행가치(Current Value)가 가질 수 있는 유용한 장점은?",
        "options": [
            "① 최초 거래 가격을 영구 고정하므로 장부 작성 속도를 느리게 지연시킬 수 있는 점",
            "② 측정일 현재의 시장 가격이나 조건 변화를 재무제표에 기민하게 업데이트하여 적시에 이용자에게 시장 정보를 전달할 수 있는 점",
            "③ 감가상각을 원천 생략할 수 있어 회계담당자의 근무시간을 단축시켜 주는 점",
            "④ 세금 고지서의 발급 기일을 연장시키는 조세 혜택을 주는 점",
            "⑤ 주식 시장의 일시 정지를 유도하여 주가 폭락을 미연에 방지할 시간을 주는 점"
        ],
        "answer": "2",
        "explanation": "② 현행가치는 측정일 시점의 경제적 조건과 정보(시장 시가 변동, 이자율 변동)를 실시간 갱신 반영하여 보고하므로, 이용자가 적시에 가장 최근의 재무상태 변화 정보를 획득하도록 보조합니다.\n\n[오답 해설]\n① 역사적원가 고정이 현행가치의 장점이 아닙니다.\n③ 현행가치라 해서 상각을 무조건 생략하는 혜택이 주어지지 않습니다.\n④ 세금 고지서 기일 등 조세 부서 편의와 무관합니다.\n⑤ 거래소의 주식 정지 등은 회계의 적시성과 직접적 관련이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "가격 고정은 역사적원가의 기능이며 적시성과 상충되기도 합니다.", "articles": [], "principle": "적시성과 측정기준", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "현행가치는 측정일의 최신 정보를 반영하여 장부를 업데이트하므로 시장 변동 사건을 적시에 보고하는 이점이 있습니다.", "articles": [], "principle": "적시성과 측정기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각 생략 등을 제공하지 않습니다.", "articles": [], "principle": "적시성과 측정기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세금 납기 연장 등과는 관련이 없습니다.", "articles": [], "principle": "적시성과 측정기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주식 거래 중지 등은 거래소의 고유 기능이며 적시성 정의가 아닙니다.", "articles": [], "principle": "적시성과 측정기준", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "개념체계 상 부채의 이행가치(Fulfilment Value) 측정 시, 미래 부채의 이행 과정에서 기대되는 거래원가(의무 이행 부대 비용 등)의 현재가치를 포함해야 하는 이론적 정당성은?",
        "options": [
            "① 거래원가가 많이 소요될수록 부채의 실제 상환 원금이 저절로 탕감되기 때문이다.",
            "② 기업 특유 관점에서 부채를 실제로 이행하고 해결하는 과정에 반드시 투입되어야 하는 실질적 미래 현금 유출 예정액이기 때문이다.",
            "③ 역사적 원가와 강제 대칭을 맞춰 세법상 공제액을 늘리기 위해서다.",
            "④ 금융기관이 거래원가 전액을 이자로 선공제하여 대신 은행 계좌에 입금하기 때문이다.",
            "⑤ 회사의 당기 매출액을 자의적으로 늘려 순이익을 왜곡하기 위해서다."
        ],
        "answer": "2",
        "explanation": "② 이행가치는 부채를 성실히 이행할 때 최종적으로 빠져나갈 경제적자원의 총 유출액을 추산하는 기업 특유의 현재가치 평가이므로, 미래 이행 시 소요되는 부대 거래원가(이행 비용)는 의무의 이행에 필수적인 현금 유출 흐름이므로 산입하는 것이 정당합니다.\n\n[오답 해설]\n① 부채 원금이 저절로 탕감되지 않습니다.\n③ 세무 공제나 탈세 편법 수단이 아닙니다.\n④ 은행 선공제 등 특수 조건과 무관합니다.\n⑤ 매출액 조작이나 순이익 왜곡 수단이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비용 증가로 부채 원금이 자동 감면되지 않습니다.", "articles": [], "principle": "이행가치와 이행원가", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이행가치는 부채 결제에 필요한 경제적자원의 실질 미래 유출액을 평가하므로 미래 이행 거래원가는 흐름에 넣어야 합니다.", "articles": [], "principle": "이행가치와 이행원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 목적의 상계가 아닙니다.", "articles": [], "principle": "이행가치와 이행원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대출 선이자와 무관한 일반적인 부채 이행 비용에 관한 논리입니다.", "articles": [], "principle": "이행가치와 이행원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익을 왜곡하기 위한 가공 분개가 아닙니다.", "articles": [], "principle": "이행가치와 이행원가", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "개념체계 상 공정가치(Fair Value)를 산정할 때, 활성시장(Active Market)에서 직접적인 관측 가격을 찾을 수 없는 경우에 우회적으로 측정하는 방법은?",
        "options": [
            "① 측정을 포기하고 세법상 상각 완료될 때까지 장부 가격을 무조건 1원으로 고정한다.",
            "② 측정기법(예: 현금흐름기준 측정기법이나 대안적 가치평가모형)을 사용하여 시장 참여자의 가정을 최대한 반영해 간접적으로 결정한다.",
            "③ 회계담당자가 경쟁 회사의 대차대조표를 보고 숫자를 그대로 표절하여 기재한다.",
            "④ 정부 공인 기관에 감정 평가를 의뢰하여 감정액의 100배를 자산가액으로 강제 갱신한다.",
            "⑤ 토론회를 개최하여 사외이사들이 다수결로 합의한 금액으로 매 결산기마다 조정한다."
        ],
        "answer": "2",
        "explanation": "② 활성시장의 직접적인 시장 가격을 관측할 수 없는 불완전한 조건 하에서도, 적절한 평가 기법(예: 현업의 블랙숄즈 모형이나 DCF 현금흐름 기법 등)을 적용해 시장참여자가 결정할 가격 가정을 모사하여 간접적으로 공정가치를 산출할 수 있습니다.\n\n[오답 해설]\n① 직접 관측치가 없다고 곧바로 측정을 포기해 1원으로 둘 필요는 없습니다.\n③ 타사 재무제표의 자의적 표절 기재는 심각한 오류입니다.\n④ 감정액의 100배 과다 가산 등은 위법 사항입니다.\n⑤ 다수결 이사회 토론을 통한 자의적 수치 기재는 회계적 정당성이 결여됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "평가 기법을 통한 간접 측정이 가능하므로 1원 고정 방치론은 틀렸습니다.", "articles": [], "principle": "공정가치의 간접 측정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "직접 시장가격 관측이 불비할 땐 적절한 평가기법(현금흐름 등)을 써서 시장 기준의 공정가치를 간접 추정하여 적용합니다.", "articles": [], "principle": "공정가치의 간접 측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "타사 자료 표절은 엄격히 금지됩니다.", "articles": [], "principle": "공정가치의 간접 측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감정액 100배 기재는 불법 분식입니다.", "articles": [], "principle": "공정가치의 간접 측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "다수결 가격 책정은 합리적 회계가 아닙니다.", "articles": [], "principle": "공정가치의 간접 측정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "개념체계 상 역사적원가(Historical Cost) 측정기준의 특징인 '시가 변동을 추적 갱신하지 않는다'는 속성이 지닌 재무보고 상의 한계점은?",
        "options": [
            "① 장부 작성의 검증가능성과 신뢰성을 완전히 파괴한다는 점",
            "② 기말 자산의 시장 가치가 대폭 올랐더라도 재무상태표의 자산 총액이 저평가 상태로 고정되어 최신 재무 정보를 이용자에게 보고하지 못한다는 점",
            "③ 회계 장부의 줄간격을 맞추기 어렵게 만든다는 점",
            "④ 세법상 납부할 법인세 총액이 매일 자의적으로 변동되는 혼란을 준다는 점",
            "⑤ 회사가 배당금을 줄 때 주주들의 서명을 매번 받아야 하는 의무를 지게 만든다는 점"
        ],
        "answer": "2",
        "explanation": "② 역사적원가는 최초 취득액을 고수하여 최신 시가 변동을 업데이트하지 않으므로, 부동산 등 시가 급등 자산의 실질 경제적 가치 총액을 재무제표가 적절하게 보고하지 못하는 고유한 재무보고 상 한계가 있습니다.\n\n[오답 해설]\n① 역사적원가는 검증성과 신뢰성을 오히려 높여 줍니다.\n③ 장부 줄간격 등 인쇄 서식과는 상관이 없습니다.\n④ 법인세의 실시간 변동을 야기하지 않습니다.\n⑤ 배당 서명 요건 등은 상법 상 지배구조의 문제이지 역사적원가의 이론적 한계가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "역사적원가는 오히려 검증성을 보장하는 핵심 강점이 있습니다.", "articles": [], "principle": "역사적원가의 한계", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "시가 변동을 갱신하지 않으므로 자산 가치가 급변하는 경제 상황에서 최신 가치 정보를 제공하지 못하는 약점이 있습니다.", "articles": [], "principle": "역사적원가의 한계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "문서 인쇄 포맷 한계가 아닙니다.", "articles": [], "principle": "역사적원가의 한계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매일 세액이 요동치는 요인을 제공하지 않습니다.", "articles": [], "principle": "역사적원가의 한계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "배당금 결의 및 주주 서명 절차와 하등의 인과관계가 없습니다.", "articles": [], "principle": "역사적원가의 한계", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "개념체계 상 특정 자산이나 부채의 측정기준(역사적원가 대 현행가치)의 변경 선택이 손익계산서 상 '수익과 비용'의 인식 및 기업 성과 측정에 미치는 영향은?",
        "options": [
            "① 측정기준 선택과 무관하게 모든 연도의 당기순손익 결과는 항상 1원 단위까지 일치하여 출력된다.",
            "② 자산·부채의 재측정에 따른 가치 변동분의 손익 반영 여부와 귀속 시점이 달라져, 당기순손익 및 총포괄손익에 직접적인 차이를 낳는다.",
            "③ 측정기준을 바꾸더라도 손익계산서상의 비용 수치는 매출액과 자동 상계되어 0원으로 강제 초기화된다.",
            "④ 역사적원가를 쓰면 이익이 매월 10배씩 급증하고 현행가치를 쓰면 10배씩 급감한다.",
            "⑤ 회사의 매출 총액 자체가 국세청 감면 혜택으로 완전히 면세 수치로만 표기된다."
        ],
        "answer": "2",
        "explanation": "② 자산과 부채를 기말에 어떻게 측정(역사적원가 고정 vs 현행가치 재평가)하느냐에 따라 평가손익의 발생 여부 및 그 평가손익의 당기손익 또는 기타포괄손익 분류 귀속이 결정되므로, 기업의 당기 성과 측정치에 직접적인 변동 효과를 가져옵니다.\n\n[오답 해설]\n① 측정 기준에 따라 당기순이익 수치는 현격히 다르게 나타납니다.\n③ 비용 수치가 자동으로 상계되어 0원이 되지 않습니다.\n④, ⑤는 아무런 수학적/법적 타당성이 없는 임의의 가상 기술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "측정 선택에 따라 연도별 손익 배분과 누적액이 대폭 달라집니다.", "articles": [], "principle": "측정기준과 성과측정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "평가손익 계상 여부 및 갱신 금액 변동으로 당기순이익과 총포괄이익 수치의 시점별 분배가 다르게 확정됩니다.", "articles": [], "principle": "측정기준과 성과측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비용 계정이 강제로 상계 0원 처리되는 규칙은 없습니다.", "articles": [], "principle": "측정기준과 성과측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특정 배수의 자동 급증/급감 공식 등은 존재하지 않습니다.", "articles": [], "principle": "측정기준과 성과측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 면세 규칙이 회계 성과 계산을 직접 0원으로 변조하지 못합니다.", "articles": [], "principle": "측정기준과 성과측정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },

    # =========================================================================
    # L3: 적용 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s08-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "A사는 공장 설비로 쓸 기계장치를 500만 원에 취득하고, 운송비와 설치비 명목으로 취득 거래원가 10만 원을 지급하였다. 당해 취득일 현재 이 기계장치의 시장 매각 가액(공정가치)은 480만 원이다. 개념체계 상 이 기계장치의 '역사적 원가(Historical Cost)'와 '공정가치(Fair Value)' 자산가액은 각각 얼마로 결정되는가?",
        "options": [
            "① 역사적 원가: 500만 원, 공정가치: 490만 원",
            "② 역사적 원가: 510만 원, 공정가치: 480만 원",
            "③ 역사적 원가: 490만 원, 공정가치: 510만 원",
            "④ 역사적 원가: 510만 원, 공정가치: 490만 원",
            "⑤ 역사적 원가: 500만 원, 공정가치: 480만 원"
        ],
        "answer": "2",
        "explanation": "② 역사적 원가 기준에서는 취득 지급 대가 500만 원에 취득 거래원가 10만 원을 **포함(가산)**하여 **510만 원**이 됩니다. 반면 공정가치 기준은 거래원가를 포함하지 않으므로 순수한 측정일의 매각 가격(유출 가격)인 **480만 원**으로 측정됩니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 역사적원가의 거래원가 가산 원칙 및 공정가치의 거래원가 배제 원칙에 따른 계산을 잘못 수행하여 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "역사적원가 계산 시 거래원가 10만 원 누락 및 공정가치 계산에 거래원가 차감 오유도 오류입니다.", "articles": [], "principle": "거래원가 반영 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산 취득 역사적원가는 취득가+거래원가=510만 원이며, 공정가치는 거래원가 배제로 480만 원이 정확합니다.", "articles": [], "principle": "거래원가 반영 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수치가 완전히 반대로 작성되었습니다.", "articles": [], "principle": "거래원가 반영 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치에 취득원가를 반영하려 한 잘못된 산출입니다.", "articles": [], "principle": "거래원가 반영 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적 원가에 취득 거래원가를 누락하였습니다.", "articles": [], "principle": "거래원가 반영 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "B사는 은행으로부터 단기차입금 3,000만 원을 수취하여 부채를 발생시켰으며, 이 과정에서 차입 수수료 및 계약 거래원가로 50만 원을 차감 지급당했다. 당일 현재 이 부채의 공정가치(유출 가액)가 3,000만 원일 때, 개념체계 상 이 단기차입금의 최초 인식 '역사적 원가(Historical Cost)'와 '공정가치(Fair Value)' 부채가액은 각각 얼마인가?",
        "options": [
            "① 역사적 원가: 3,050만 원, 공정가치: 3,000만 원",
            "② 역사적 원가: 2,950만 원, 공정가치: 3,000만 원",
            "③ 역사적 원가: 3,000만 원, 공정가치: 2,950만 원",
            "④ 역사적 원가: 2,950만 원, 공정가치: 3,050만 원",
            "⑤ 역사적 원가: 3,000만 원, 공정가치: 3,000만 원"
        ],
        "answer": "2",
        "explanation": "② 부채의 역사적 원가는 수취한 대가 3,000만 원에서 거래원가 50만 원을 **차감(차감한 가치)**하므로 **2,950만 원**이 최초 장부액이 됩니다. 반면 부채의 공정가치는 거래원가를 차감하지 않으므로 순수한 유출 가액인 **3,000만 원**이 적용됩니다.\n\n[오답 해설]\n① 부채 역사적 원가 계산 시 거래원가를 차감해야 하나 합산(3,050만 원)하여 잘못되었습니다.\n③, ④, ⑤는 부채 거래원가의 차감 및 배제 로직을 잘못 조합하여 오류가 난 수치들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "부채 역사적원가는 거래원가를 가산하는 것이 아니므로 3,050만 원은 틀립니다.", "articles": [], "principle": "부채 거래원가 산정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부채의 역사적 원가는 최초 수취액에서 거래원가를 뺀 2,950만 원이며, 공정가치는 원가 고려 없는 3,000만 원입니다.", "articles": [], "principle": "부채 거래원가 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수치가 맞지 않습니다.", "articles": [], "principle": "부채 거래원가 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치에 거래원가를 가산하여 오유도한 결과입니다.", "articles": [], "principle": "부채 거래원가 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적원가에서 거래원가 차감을 전혀 반영하지 않은 계산 오류입니다.", "articles": [], "principle": "부채 거래원가 산정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "C사는 반도체 생산용 라인(자산)을 가동하고 있다. 이 설비는 C사의 특허 공정 기술과 결합되어 내부적으로 사용할 때 연간 1억 원의 부가가치(사용가치)를 창출한다. 그러나 이 설비를 해체하여 시장에 그냥 내다 팔 경우 시장 참가자들은 특허 기술을 활용할 수 없어 6,000만 원(공정가치)에만 매입하려 한다. 두 측정 기준 가액 괴리의 원인을 개념체계 상 설명으로 가장 알바르게 지적한 것은?",
        "options": [
            "① 공정가치는 시장참전자 일반의 관점을 반영하므로 기업 특유의 결합 시너지 효과를 배제하는 반면, 사용가치는 보고기업이 해당 자산을 계속 사용함으로써 얻을 수 있는 기업 특유의 시너지를 반영하기 때문이다.",
            "② C사의 기계 회계담당자가 세금을 덜 내기 위해 공정가치 수치를 고의로 누락해 보고하였기 때문이다.",
            "③ 사용가치에만 매년 복식부기 가산 수수료 4,000만 원이 강제로 적용되도록 회계기준서가 지시하기 때문이다.",
            "④ 기계장치의 실제 소유권이 정부 세무관서에 신탁되어 소유 리스크가 발생했기 때문이다.",
            "⑤ 공정가치를 계산할 때 처분 거래원가 4,000만 원을 임의로 더해 주었기 때문이다."
        ],
        "answer": "1",
        "explanation": "① 공정가치는 특정 보고기업 고유의 결합 시너지나 의도를 배제하고 '시장참전자 관점'에서 객관적으로 가격을 책정합니다. 반면 사용가치는 자산을 직접 사용하는 당해 기업의 특수 조건과 시너지를 포괄하는 '기업 특유의 관점'을 반영하므로 두 수치 사이에 차이가 생기는 것은 자연스러운 현상입니다.\n\n[오답 해설]\n② 세금 조작을 위해 공정가치를 조정한 근무 태만 사건이 아닙니다.\n③ 복식부기 가산 수수료 규정은 회계 상 실재하지 않습니다.\n④ 신탁 리스크와 무관한 가치 평가 주체의 관점 차이 문제입니다.\n⑤ 공정가치에는 처분 거래원가를 더하지 않으므로 오진술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "공정가치(시장참전자 관점)는 시너지를 배제하지만, 사용가치(기업특유 관점)는 특유의 시너지와 결합 사용 가치를 모두 포괄하여 산정하므로 차이가 납니다.", "articles": [], "principle": "공정가치와 사용가치 괴리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계담당자의 근무 태만이나 조작 사건이 아닙니다.", "articles": [], "principle": "공정가치와 사용가치 괴리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가공의 가산 수수료 설명은 무효입니다.", "articles": [], "principle": "공정가치와 사용가치 괴리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정부 신탁 등의 지배구조 이슈와 상관없습니다.", "articles": [], "principle": "공정가치와 사용가치 괴리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치 거래원가 가산론은 틀린 내용입니다.", "articles": [], "principle": "공정가치와 사용가치 괴리", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "D사는 활성시장이 없는 비상장 금융 주식을 투자 목적으로 매입하고자 하며, 시장 참여자들의 거래 가정을 모사한 DCF 모형(현금흐름 기법)으로 공정가치를 간접 추정하고 있다. 주식의 취득 가격은 1,000만 원이며 중개인에게 지급한 거래 수수료는 20만 원이다. 당일 공정가치 평가 시, 취득 거래원가인 수수료 20만 원의 적용에 대한 개념체계 상 설명으로 가장 옳은 것은?",
        "options": [
            "① 간접 측정기법을 쓸 경우 수수료 20만 원은 자산의 공정가치에 전액 더해주어야 한다.",
            "② 공정가치는 자산 취득 당시의 원가로 인해 증가하지 않으므로, 수수료 20만 원은 자산의 공정가치에 합산하지 않고 전액 당기비용 등으로 처리해야 한다.",
            "③ 거래 수수료의 100배를 계산하여 자산 가치에서 임의 차감 기재한다.",
            "④ 금융감독원 승인을 얻은 금융 자산에 한하여 20만 원을 감가상각 누계액으로 우선 대체한다.",
            "⑤ 수수료의 절반인 10만 원만 공정가치에 임의 가산하고 나머지는 비밀 자금으로 처리한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 공정가치는 거래원가로 인해 증가하지 않으므로(원가 배제), 주식의 취득 거래원가인 20만 원은 공정가치 평가액에 합산하지 않고 취득 시 별개의 당기비용 등으로 인식해야 합니다.\n\n[오답 해설]\n① 평가기법 사용 여부와 무관하게 공정가치는 거래원가를 합산하지 않습니다.\n③, ④, ⑤는 회계 기준에 반하는 가공의 오처리들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "간접 측정법 사용 시에도 공정가치는 거래원가를 배제해야 합니다.", "articles": [], "principle": "공정가치 거래원가 미적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치는 최초 취득 거래원가로 증가하지 않으므로 수수료는 공정가치 가액에 넣지 않고 별도 처리합니다.", "articles": [], "principle": "공정가치 거래원가 미적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 100배 차감 등은 회계 오류입니다.", "articles": [], "principle": "공정가치 거래원가 미적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융주식에 감가상각누계액 대체 적용은 성립하지 않습니다.", "articles": [], "principle": "공정가치 거래원가 미적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 비율 가산 및 비밀 자금 적립은 심각한 위법 사항입니다.", "articles": [], "principle": "공정가치 거래원가 미적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "E사는 공장 철거 및 환경 복구 의무(복구부채)를 최초 부담하게 되었다. 법적으로 이 의무의 최종 이행(철거 비용 지출)은 5년 뒤에 이루어지며, E사는 이 복구 의무의 '이행가치(Fulfilment Value)'를 최초 계상하려 한다. 이행가치에 포함되는 구성 요소로 개념체계 상 가장 적절한 것은?",
        "options": [
            "① 5년 뒤 이행 시점에 실제로 발생할 것으로 기대되는 복구 거래원가(철거 대행 수수료, 매립 원가 등)의 현재가치",
            "② 복구의무를 맺은 날 당일에 국세청에 납부한 전년도 법인세 누계액의 과거가치",
            "③ 환경 단체에 향후 매년 기부하기로 경영진이 약속한 임의 기부금 예산",
            "④ 5년 동안 가동할 신규 기계장치들의 역사적 취득가액 전체",
            "⑤ 복구의무 면제를 위해 상대방과 매월 협상할 때 사용한 출장 여비 교통비"
        ],
        "answer": "1",
        "explanation": "① 이행가치(Fulfilment Value)는 부채를 이행할 때 최종 유출될 경제적자원의 현재가치이므로, 미래 의무 이행 시점에 필요한 부대 이행비용(철거 수수료, 복구 거래원가)의 현재가치를 포함하여 부채 가액을 구성해야 합니다.\n\n[오답 해설]\n② 과거 법인세액은 복구부채 이행가치와 상관없습니다.\n③ 임의의 기부금 예산은 법적/실질적 이행 의무액에 포함되지 않습니다.\n④ 기계장치 취득원가는 복구부채 이행가치 평가액이 아닙니다.\n⑤ 협상 출장비 등은 의무 이행에 직접 수반되는 복구 원가가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "이행가치에는 미래 결제/이행 단계에 지출될 거래원가의 현재가치가 포함되어야 합니다.", "articles": [], "principle": "이행가치와 거래원가 포함", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과거 법인세는 부채 이행가치와 다른 항목입니다.", "articles": [], "principle": "이행가치와 거래원가 포함", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 기부금은 법적 채무의 이행 비용이 아닙니다.", "articles": [], "principle": "이행가치와 거래원가 포함", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기계장치 가격은 복구부채 이행 비용과 상관없습니다.", "articles": [], "principle": "이행가치와 거래원가 포함", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일반 협상 여비 교통비는 이행가치의 현재가치 포함 항목이 아닙니다.", "articles": [], "principle": "이행가치와 거래원가 포함", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "F사는 보유 중인 운송용 트럭의 '현행원가(Current Cost)'를 결산일에 측정하고자 한다. 측정일 현재 동종 트럭의 신차 조달 시장 가격은 3,000만 원이며, 인도 시 발생하는 거래원가는 100만 원이다. 한편 F사의 트럭은 이미 절반 정도 노후화되어 노후화 비율 50%를 반영해야 한다. 개념체계 상 F사의 노후화된 트럭 현행원가 자산가액은 얼마로 추산하는가?",
        "options": [
            "① 1,450만 원",
            "② 1,500만 원",
            "③ 1,550만 원",
            "④ 1,600만 원",
            "⑤ 3,100만 원"
        ],
        "answer": "3",
        "explanation": "③ 자산의 현행원가는 측정일에 동등한 자산의 조달 원가(대가 + 발생할 거래원가 포함)이므로, 측정일 현재 새 트럭 조달원가는 3,000만 원 + 100만 원 = 3,100만 원이 됩니다. F사의 트럭은 50% 노후화(감가상각 상태)되었으므로 이 조달원가에 50% 비율을 반영하면 **1,550만 원**이 현행원가 기준으로 산출됩니다.\n\n[오답 해설]\n① 거래원가를 빼고 계산(2,900만 원의 50% = 1,450만 원)하여 오답입니다.\n② 거래원가를 누락하고 계산(3,000만 원의 50% = 1,500만 원)하여 오답입니다.\n④ 거래원가를 잘못 가산하여 산정한 오답 수치입니다.\n⑤ 노후화 감액 비율(50%)을 전혀 반영하지 않은 신차 기준 가격입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "현행원가는 조달 거래원가를 가산하므로 뺀 계산은 틀렸습니다.", "articles": [], "principle": "현행원가 계산 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조달 거래원가 100만 원 가산을 누락하였습니다.", "articles": [], "principle": "현행원가 계산 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "(취득대금 3,000만 원 + 거래원가 100만 원) * (1 - 0.5) = 1,550만 원이 정확한 현행원가 자산가액입니다.", "articles": [], "principle": "현행원가 계산 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래원가를 과다 가산하는 등의 산식 오류입니다.", "articles": [], "principle": "현행원가 계산 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "50% 감가 상태를 미반영하여 신차 조달액 전체를 자산으로 올릴 수 없습니다.", "articles": [], "principle": "현행원가 계산 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "G사는 역사적원가 2,000만 원으로 계상되어 있던 건물 자산에 대해 자산손상(Impairment) 징후가 있어 손상평가를 개시하였다. 현재 평가일의 건물 처분부대원가(거래원가) 차감 후 공정가치(순공정가치)는 1,500만 원이며, 건물을 계속 사용함에 따라 기대되는 사용가치는 1,700만 원이다. 자산손상 기준서 및 개념체계의 자산가치 보전 원리에 따를 때, 건물의 회수가능액(Recoverable Amount)은 얼마인가?",
        "options": [
            "① 1,500만 원",
            "② 1,600만 원",
            "③ 1,700만 원",
            "④ 2,000만 원",
            "⑤ 3,200만 원"
        ],
        "answer": "3",
        "explanation": "③ 자산의 손상 평가 시 '회수가능액'은 순공정가치(공정가치에서 처분부대원가 차감액)와 사용가치 중 **더 큰 금액(Max)**으로 결정합니다. 기업이 경제적으로 최선의 선택을 한다면 처분하는 것(1,500만 원 회수)보다 계속 사용하는 것(1,700만 원 회수)을 택할 것이기 때문입니다. 따라서 1,700만 원이 회수가능액이 됩니다.\n\n[오답 해설]\n① 더 작은 금액(Min)을 골라 잘못되었습니다.\n② 두 값의 평균인 1,600만 원을 적용하여 틀렸습니다.\n④ 최초 역사적원가 2,000만 원은 회수가능액 결정 값과 다릅니다.\n⑤ 두 값을 합산한 수치는 적용되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "두 값 중 작은 값인 순공정가치를 고르면 틀립니다.", "articles": [], "principle": "회수가능액의 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "두 수치의 단순 평균 계산은 근거가 없습니다.", "articles": [], "principle": "회수가능액의 산정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "회수가능액은 순공정가치(1,500만 원)와 사용가치(1,700만 원) 중 더 높은 금액인 1,700만 원으로 확정됩니다.", "articles": [], "principle": "회수가능액의 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "최초 장부가액을 회수가능액으로 쓰지 않습니다(손상 차손 인식 대상).", "articles": [], "principle": "회수가능액의 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "두 가액의 단순 합산액은 성립하지 않습니다.", "articles": [], "principle": "회수가능액의 산정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "H사는 당일 신용평가사로부터 신용등급이 기존 'A'에서 'BBB'로 강등당했다. 이로 인해 H사가 발행하여 시장에 유통 중인 자사 회사채(사채부채)의 시장 가격이 폭락하여 사채의 공정가치가 감소하였다. H사가 이 사채를 기말에 '공정가치'로 측정할 경우, 자기신용위험 변동 효과가 부채 장부 가액에 미치는 실무 영향은?",
        "options": [
            "① 자사의 신용등급 강등으로 부채의 공정가치가 감소하므로, 사채부채의 장부금액이 감소하는 결과가 발생한다.",
            "② 신용등급이 하락하면 부채의 원금이 저절로 2배로 증가하여 계상된다.",
            "③ 자기신용위험의 변화는 부채 공정가치에 전혀 영향을 주지 않으므로 장부금액은 고정된다.",
            "④ 신용등급 하락은 주주의 현금 배당 금액을 10배로 늘려 주는 부수 효과를 낳는다.",
            "⑤ 부채를 전액 즉시 제거하고 '자본잉여금'으로 대체 상계한다."
        ],
        "answer": "1",
        "explanation": "① 자기 신용도가 하락(신용위험 증가)하면, 시장참전자들은 당해 사채에 더 높은 할인율(신용스프레드 상승)을 요구하므로 부채의 공정가치(시장 가격)는 하락(감소)합니다. 따라서 부채 장부금액이 감소하게 됩니다.\n\n[오답 해설]\n② 신용 등급 하락으로 부채 원금이 2배가 되지 않으며 공정가치는 오히려 감소합니다.\n③ 자기신용위험은 부채 공정가치 구성의 필수 요인으로 반영됩니다.\n④ 주주 배당금을 자동으로 10배 상승시키지 않습니다.\n⑤ 소멸하지 않은 사채를 자본으로 전액 상계 대체하여 제거하는 것은 불가합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "자사 신용등급 하락 시 회사채 할인율 상승으로 부채의 공정가치가 하락하므로, 부채 장부 가액이 줄어드는 현상이 유도됩니다.", "articles": [], "principle": "자기신용위험과 부채 평가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "신용 하락 시 부채 액면이 배증되지 않습니다.", "articles": [], "principle": "자기신용위험과 부채 평가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치는 자기신용위험 요인을 실시간 반영하므로 고정 설명은 오류입니다.", "articles": [], "principle": "자기신용위험과 부채 평가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주주 배당액 증가 요인을 제공하지 않습니다.", "articles": [], "principle": "자기신용위험과 부채 평가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의무가 남아 있는 한 제거 분개할 수 없습니다.", "articles": [], "principle": "자기신용위험과 부채 평가", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "I사는 거래처에 대해 품질 보증 서비스를 제공하기로 약정했다. 이 보증 채무를 성실히 이행할 때 지출될 것으로 예상되는 현금 유출액의 기댓값은 1년 뒤 1,000만 원이다. 당해 연도 시장의 무위험 이자율은 연 5%이며, 이 보증 채무를 이행하는 것과 관련된 이행 거래원가의 현재가치는 50만 원으로 평가되었다. 개념체계 상 이 보증 채무의 '이행가치(Fulfilment Value)'는 얼마로 결정되는가? (단, 1년 뒤 1,000만 원의 연 5% 현재가치 할인액은 편의상 950만 원으로 계산한다.)",
        "options": [
            "① 900만 원",
            "② 950만 원",
            "③ 1,000만 원",
            "④ 1,050만 원",
            "⑤ 1,100만 원"
        ],
        "answer": "3",
        "explanation": "③ 이행가치(Fulfilment Value)는 부채 이행 시 필요한 기대유출자원의 현재가치(950만 원)에다가, 의무를 최종적으로 이행하고 결제하는 과정에 투입되어 발생할 거래원가의 현재가치(50만 원)를 **포함(합산)**하여 산정합니다. 따라서 950만 원 + 50만 원 = **1,000만 원**이 이행가치가 됩니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 이행가치의 거래원가 합산 계산 규칙을 잘못 구현하여 오답이 나온 수치들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "거래원가를 도리어 차감한 900만 원은 틀린 값입니다.", "articles": [], "principle": "이행가치 산정 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래원가 가산(50만 원)을 누락한 값입니다.", "articles": [], "principle": "이행가치 산정 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부채 결제 현가 950만 원 + 이행 거래원가 현가 50만 원 = 1,000만 원이 올바른 이행가치 총액입니다.", "articles": [], "principle": "이행가치 산정 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래원가 과다 합산 등 산식 오류입니다.", "articles": [], "principle": "이행가치 산정 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "할인 전 기대 원금에 원가를 단순 합산한 잘못된 금액입니다.", "articles": [], "principle": "이행가치 산정 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "J사는 체결 중인 원재료 공급계약이 시장가 폭락으로 인해 원재료 수령액 가치보다 의무 이행 단가가 훨씬 비싸진 불리한 계약(손실부담계약)이 되었다. 계약 파기 시 내야 하는 법적 위약금은 300만 원이고, 계약을 그대로 강제 이행할 때 발생하는 이행가치(손실액 현가)는 400만 원이다. 개념체계 상 이 불리한 미이행계약의 부채 인식액은 얼마인가?",
        "options": [
            "① 100만 원",
            "② 300만 원",
            "③ 400만 원",
            "④ 700만 원",
            "⑤ 1,200만 원"
        ],
        "answer": "2",
        "explanation": "② 불리한 계약(손실부담계약) 하에서 현재의무를 이행하는 것과 관련된 피할 수 없는 원가는 '계약을 이행하기 위해 소요되는 순원가(이행가치 400만 원)'와 '계약을 이행하지 못했을 때 지급해야 하는 보상금이나 위약금(300만 원)' 중 **더 적은 금액(Min)**으로 결정됩니다. 기업은 합리적으로 비용이 적게 드는 계약 파기 및 위약금 300만 원 지급을 택해 손실을 최소화할 것이기 때문입니다. 따라서 300만 원이 부채로 계상됩니다.\n\n[오답 해설]\n① 차액 100만 원을 부채로 잡지 않습니다.\n③ 더 큰 금액인 400만 원을 택해 틀렸습니다.\n④ 두 금액의 합산액인 700만 원은 부채 과대계상 오류입니다.\n⑤ 임의의 곱셈을 한 1,200만 원은 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "차액 100만 원 계산은 규정에 어긋납니다.", "articles": [], "principle": "손실부담계약의 부채", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "회피불가능원가는 계약 이행 순원가(400만 원)와 해지 위약금(300만 원) 중 최소 금액인 300만 원으로 측정합니다.", "articles": [], "principle": "손실부담계약의 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손실이 큰 대안(이행 400만 원)을 부채의 측정값으로 선택하지 않습니다.", "articles": [], "principle": "손실부담계약의 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "합산액 700만 원을 청구당하지는 않습니다.", "articles": [], "principle": "손실부담계약의 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "배배 불필요한 과다 계산액입니다.", "articles": [], "principle": "손실부담계약의 부채", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "K사는 보유하고 있던 토지를 취득원가인 역사적원가 10억 원으로 기재해왔다. 현시점 토지의 시장 가격(공정가치)은 15억 원으로 올랐다. 이 토지를 공정가치(재평가모형)로 측정기준을 갱신 선택할 경우, 늘어나는 차액 5억 원의 회계 처리와 재무적 영향에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 증가한 5억 원은 당기 매출액에 누적 합산하여 이익을 왜곡한다.",
            "② 증가한 5억 원은 일반적으로 기타포괄손익(재평가잉여금)으로 계상되어 자본 총액을 실질적으로 증가시키고, 토지 자산 장부가액은 15억 원으로 업데이트된다.",
            "③ 증가분 5억 원을 즉시 현금 배당금으로 최종 확정하고 사외 유출 단행한다.",
            "④ 토지의 역사적원가와 시가 차액은 전액 법인세 부채로 국세청에 다음 날 납부해야 한다.",
            "⑤ 토지 자산액을 장부에서 지우고 대신 부채인 차입금 계정으로 15억 원을 올린다."
        ],
        "answer": "2",
        "explanation": "② 역사적원가 10억 원에서 공정가치 15억 원으로 측정 갱신 시, 토지의 장부 가액은 15억 원으로 상향 조정되며, 차액 5억 원은 미실현 보유 손익 성격이므로 당기 손익이 아닌 기타포괄손익(재평가잉여금) 자본 항목으로 기재되어 재무구조 개선 효과를 가져옵니다.\n\n[오답 해설]\n① 미실현 손익을 정규 매출로 분류하지 않습니다.\n③ 자본 항목인 재평가잉여금은 즉시 미실현 분배 재원으로 지급할 수 없습니다.\n④ 미실현 평가차익에 대해 다음 날 즉시 실물 과세 세액을 내야 하는 것은 아닙니다.\n⑤ 자산을 부채 차입금으로 분류 변경할 하등의 이유가 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "미실현 토지 상승액을 당기 매출로 분류하는 분개는 허용되지 않습니다.", "articles": [], "principle": "재평가 평가차익 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "토지 평가이익은 기타포괄손익(재평가잉여금) 자본으로 계상되어 총자산과 총자본을 5억 원씩 증가시킵니다.", "articles": [], "principle": "재평가 평가차익 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미실현 평가차익은 당기 배당 재원으로 사외 유출할 수 없습니다.", "articles": [], "principle": "재평가 평가차익 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 상 미실현이익에 대한 즉시 법인세 납부 부채가 강제되지 않습니다.", "articles": [], "principle": "재평가 평가차익 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "토지를 차입 부채로 변조 기재할 수는 없습니다.", "articles": [], "principle": "재평가 평가차익 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "L사는 자산인 금융상품(채권) 1,000만 원을 매각하고 처분 손익을 인식하고자 한다. 거래 계약 시 매각에 따른 처분 거래원가로 15만 원이 발생하였다. 금융상품 처분 시점의 공정가치(매각가)가 1,200만 원일 때, 처분원가 15만 원을 고려한 L사의 최종 '채권처분손익'은 얼마인가?",
        "options": [
            "① 처분이익 215만 원",
            "② 처분이익 200만 원",
            "③ 처분이익 185만 원",
            "④ 처분이익 15만 원",
            "⑤ 처분손실 15만 원"
        ],
        "answer": "3",
        "explanation": "③ 채권의 처분 손익 계산 시에는, 처분 수취금액(공정가치)인 1,200만 원에서 장부가액 1,000만 원을 뺀 순수 차액 200만 원에다가, 처분 과정에 직접 소요된 처분 거래원가(비용) 15만 원을 **차감**하여 최종 **185만 원**의 처분이익을 계상합니다.\n\n[오답 해설]\n① 처분원가를 차감하지 않고 더해 주어(215만 원) 오답입니다.\n② 처분원가를 무시하고 단순 시가 차액(200만 원)만 기재하여 오답입니다.\n④, ⑤는 처분원가 단독만을 계상해 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "처분 비용인 거래원가를 가산하여 처분이익을 크게 유도하면 틀립니다.", "articles": [], "principle": "자산 처분 시 거래원가 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분 과정의 수수료 비용 15만 원의 유출을 미반영한 결과입니다.", "articles": [], "principle": "자산 처분 시 거래원가 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "매각액 1,200만 원 - 장부액 1,000만 원 - 처분원가 15만 원 = 순처분이익 185만 원이 맞습니다.", "articles": [], "principle": "자산 처분 시 거래원가 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수수료 단독액을 이익으로 오인식했습니다.", "articles": [], "principle": "자산 처분 시 거래원가 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수수료 비용 단독만을 전체 처분손실로 볼 수는 없습니다.", "articles": [], "principle": "자산 처분 시 거래원가 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "M사는 보유하고 있던 기계장치 A를 거래처의 기계장치 B와 맞바꾸는 이종 자산 교환 거래를 수립하였다. 기계 A의 장부가액은 300만 원, 공정가치는 400만 원이다. 기계 B의 공정가치는 불분명하다. 상업적 실질이 존재하는 이 교환 거래 하에서 취득한 기계장치 B의 최초 '역사적 원가'는 얼마로 계상하는 것이 타당한가?",
        "options": [
            "① 100만 원",
            "② 300만 원",
            "③ 400만 원",
            "④ 700만 원",
            "⑤ 1,200만 원"
        ],
        "answer": "3",
        "explanation": "③ 상업적 실질이 있는 이종 자산의 교환으로 새로 취득한 자산의 역사적원가는 취득을 위해 지급한 대가인 '제공한 자산(기계 A)의 공정가치'인 **400만 원**으로 책정합니다.\n\n[오답 해설]\n① 400만 원과 300만 원의 차액 100만 원은 처분이익이며, 취득한 기계 B의 원가가 아닙니다.\n② 제공한 기계 A의 장부가액 300만 원을 기준으로 삼는 것은 상업적 실질이 없거나 불분명할 때의 대체 지침입니다.\n④ 두 가액의 합산액인 700만 원은 원가와 상관없습니다.\n⑤ 곱셈을 가한 잘못된 계산입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "차액 100만 원은 처분손익 부분이며 신자산 원가가 아닙니다.", "articles": [], "principle": "교환 거래 자산 취득원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "제공자산의 장부가액을 승계하는 것은 상업적 실질이 결여된 거래 시의 규정입니다.", "articles": [], "principle": "교환 거래 자산 취득원가", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "상업적 실질이 있는 교환 거래의 신취득자산 역사적원가는 제공한 자산의 공정가치(400만 원)에 맞춰 계상합니다.", "articles": [], "principle": "교환 거래 자산 취득원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "장부가와 공정가의 단순 합산액은 원가 기준이 아닙니다.", "articles": [], "principle": "교환 거래 자산 취득원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 계산액입니다.", "articles": [], "principle": "교환 거래 자산 취득원가", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "N사는 제조 공장에서 가동 중인 기계설비(장부 3억 원)를 자사 고유의 우수한 원재료 포뮬러 기술과 통합 연계하여 단독 가동 시보다 5,000만 원의 추가 현금흐름(결합 사용 시너지)을 내고 있다. 이 설비를 외부 시장에 단순 양도할 경우 이 결합 시너지는 타사에 공유되지 않는다. 개념체계 상 이 시너지가 사용가치와 공정가치에 반영되는 형태에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 사용가치에는 시너지 5,000만 원이 가산 반영되는 반면, 시장참전자 관점인 공정가치 측정 시에는 이 결합 시너지가 반영되지 않는다.",
            "② 공정가치와 사용가치 모두 시너지를 100% 무시하고 3억 원의 원가로 동액 고정된다.",
            "③ 공정가치에만 5,000만 원이 가산되고 사용가치에서는 5,000만 원을 강제 삭감한다.",
            "④ 시너지 효과는 무형자산이므로 별도로 자본금란에 강제 증자 인식해야 한다.",
            "⑤ 결합 시너지는 국세청 조세 과세 등급을 상승시키므로 즉시 손실 처리한다."
        ],
        "answer": "1",
        "explanation": "① 사용가치는 자산을 직접 보유 운용하는 기업 고유의 효용 흐름을 집계하는 '기업 특유 관점'이므로 시너지가 온전히 포함됩니다. 그러나 공정가치는 특정 보고기업의 특수한 사용 방식을 배제하고 '시장참전자 관점'에서 보편적인 가격을 측정하므로 개별 결합 시너지가 반영되지 않습니다.\n\n[오답 해설]\n② 시너지를 무시하고 원가로 고정한다는 것은 현행가치 측정 속성과 배치됩니다.\n③ 공정가치와 사용가치의 적용 방향이 반대로 기술되었습니다.\n④ 시너지 자체를 개별 자산 및 증자 거래로 인식하지 않습니다.\n⑤ 세무 과세 등급 상승과 관련한 즉시 손실 처리 지침은 회계 이론상 불합리합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "사용가치는 기업특유관점으로 자산의 결합 시너지를 수용하지만, 공정가치는 시장참전자 관점이므로 이러한 고유 시너지를 가치에 포함하지 않습니다.", "articles": [], "principle": "결합 시너지와 측정 가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현행가치 갱신 정보이므로 둘 다 3억 원 원가 고정은 아닙니다.", "articles": [], "principle": "결합 시너지와 측정 가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적용 관계 설명이 거꾸로 되어 틀렸습니다.", "articles": [], "principle": "결합 시너지와 측정 가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "결합 시너지 자체를 대차대조표 본문에 단독 무형자산 및 증자로 올릴 수는 없습니다.", "articles": [], "principle": "결합 시너지와 측정 가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과세 등급 등 세무 요인을 즉시 회계 손실로 반영할 수 없습니다.", "articles": [], "principle": "결합 시너지와 측정 가치", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "O회사는 자사가 보유한 공장 건물에 화재 방지용 특수 규제 스프링클러를 의무 설치해야 하는 정부의 환경 안전 규제(부채)를 지게 되었다. 이 규제 의무의 결제를 타사에 외주 주어 즉시 양도하는 정상거래 가격(공정가치)은 5,000만 원인 반면, O회사가 자재를 구매해 직접 공사를 벌여 이행할 때 소요되는 현금 흐름의 현재가치(이행가치)는 3,500만 원이다. 개념체계 상 이 부채의 평가 및 의무 이행 판단으로 가장 적절한 것은?",
        "options": [
            "① O회사는 5,000만 원에 외주 주어 이전하는 것이 경제적으로 최선이므로 공정가치를 단독 부채로 계상해야 한다.",
            "② O회사는 외주 양도가 규제상 불가능하고 직접 복구하는 것이 경제적(3,500만 원)이므로, 기업 특유 관점을 반영한 이행가치 3,500만 원을 부채로 계상하여 의사결정에 활용하는 것이 목적적합하다.",
            "③ 스프링클러는 소방 자산이므로 부채 항목이 아닌 '매출액'에 전액 3,500만 원을 더해준다.",
            "④ 두 금액의 차액인 1,500만 원을 주주들에게 사외 보너스 배당금으로 지급하고 부채는 0원 처리한다.",
            "⑤ 회사의 당기순이익을 증가시키기 위하여 스프링클러 의무 가격의 100배인 35억 원을 자산으로 등재한다."
        ],
        "answer": "2",
        "explanation": "② 특정한 법적/행정적 규제 의무는 시장에서 자유롭게 외주 주어 타사에 면제 양도(공정가치 거래)하기가 불가능한 경우가 대다수입니다. 따라서 보고기업의 직접 결제를 전제하는 기업 특유의 '이행가치(3,500만 원)'를 기준으로 부채를 측정 보고하는 것이 실질 재무 상황을 보다 충실히 나타냅니다.\n\n[오답 해설]\n① 외주 양도가 현실적으로 불가하거나 불리하다면 공정가치 중심 보고의 유용성이 저해됩니다.\n③ 의무 규제를 자산 매각 매출로 올리는 것은 분식 행위입니다.\n④ 부채를 마음대로 삭제하고 차액을 배당 지급할 수 없습니다.\n⑤ 100배 과다 가공 자산 등재는 불법 분식회계입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "외주 매각 이전이 통제되지 않는 규제 채무에 공정가치 계상만을 고집하는 것은 부적절할 수 있습니다.", "articles": [], "principle": "이행가치와 공정가치 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "시장 양도가 막혀 있고 기업이 직접 자원을 써서 의무를 해소해야 하는 규제 부채는 기업특유의 이행가치를 보고하는 것이 더 목적적합합니다.", "articles": [], "principle": "이행가치와 공정가치 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소방 설비 의무를 매출액에 합산할 수는 없습니다.", "articles": [], "principle": "이행가치와 공정가치 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 임의 삭제 후 차액 강제 배당은 불가능한 회계입니다.", "articles": [], "principle": "이행가치와 공정가치 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "35억 원의 가공 자산 등재 행위는 불법 분식회계입니다.", "articles": [], "principle": "이행가치와 공정가치 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },

    # =========================================================================
    # L4: 분석 (8문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s08-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "개념체계 상 자산이나 부채 측정 시 발생하는 '거래원가(Transaction Cost)'의 측정기준별 처리 규칙에 관한 진술 중 옳은 것을 모두 고른 것은?\n\n```\nㄱ. 역사적원가와 현행원가는 자산 취득 거래원가를 장부금액에 포함(가산)한다.\nㄴ. 공정가치는 측정일에 시장참전자 관점에서 거래가격을 산출하므로 자산/부채 관련 취득 및 처분 거래원가를 가치 평가 시 일체 반영하지 않는다.\nㄷ. 사용가치와 이행가치는 자산 취득이나 부채 인수 시 발생한 과거 거래원가는 미포함하되, 미래에 발생할 것으로 기대되는 처분/결제 거래원가의 현재가치는 포함한다.\n```",
        "options": [
            "① ㄱ",
            "② ㄴ",
            "③ ㄱ, ㄴ",
            "④ ㄴ, ㄷ",
            "⑤ ㄱ, ㄴ, ㄷ"
        ],
        "answer": "5",
        "explanation": "⑤ ㄱ, ㄴ, ㄷ 모두 개념체계 상 규정된 각 측정기준(역사적원가, 현행원가, 공정가치, 사용/이행가치)의 거래원가 회계 처리 지침을 오류 없이 완벽하게 기술하고 있어 모두 옳습니다.\n\n[오답 해설]\n①, ②, ③, ④는 일부만 참으로 간주하여 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄴ, ㄷ도 정당한 조문 기술이므로 단독 선택은 오답입니다.", "articles": [], "principle": "거래원가 규칙 판별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ, ㄷ도 참입니다.", "articles": [], "principle": "거래원가 규칙 판별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ을 배제하여 오답입니다.", "articles": [], "principle": "거래원가 규칙 판별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ을 배제하여 오답입니다.", "articles": [], "principle": "거래원가 규칙 판별", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ(역사적/현행원가 가산), ㄴ(공정가치 거래원가 배제), ㄷ(사용/이행가치 미래거래원가 포함) 모두 개념체계 상 참인 명제입니다.", "articles": [], "principle": "거래원가 규칙 판별", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "개념체계 상 역사적원가(Historical Cost)와 현행가치(Current Value) 측정기준의 전반적인 특징 비교 설명 중 옳은 보기의 조합만을 고른 것은?\n\n```\nㄱ. 역사적원가는 취득/발생 당시 최초 거래 가격을 기록하고 시가 변동을 추후 갱신하지 않는 반면, 현행가치는 측정일 조건 반영을 위해 갱신한다.\nㄴ. 역사적원가는 조달 당시의 교환가치에 초점을 두므로 기본적으로 '투입가치(Entry Value)' 속성을 가진다.\nㄷ. 공정가치는 유출가격(Exit Value)이고 현행원가는 투입가격(Entry Value)이다.\nㄹ. 공정가치는 특정 보고기업의 시너지를 반영한 기업 특유의 관점(Entity-specific Perspective)을 대변한다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄹ",
            "③ ㄱ, ㄴ, ㄷ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ ㄱ, ㄴ, ㄷ은 개념체계 상 역사적원가(투입가치, 비갱신), 현행원가(투입가치), 공정가치(유출가치, 시장참전자 관점)의 속성을 올바르게 기술하여 참입니다.\n\n[오답 해설]\nㄹ. 공정가치는 특정 기업의 결합 시너지나 주관적 의도를 반영하는 기업 특유의 관점이 아니며, 보편적인 **시장참전자 관점**을 반영합니다. (기업특유관점은 사용가치/이행가치가 반영합니다.)",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄷ도 참이므로 ㄱ, ㄴ만 묶은 보기는 오답입니다.", "articles": [], "principle": "측정기준 특징 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ이 거짓 진술이므로 오답입니다.", "articles": [], "principle": "측정기준 특징 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ(역사적/현행가치 갱신여부), ㄴ(역사적원가의 투입가치성), ㄷ(공정가치의 유출 및 현행원가의 투입가치성) 모두 올바른 회계 이론입니다.", "articles": [], "principle": "측정기준 특징 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ이 오답이므로 틀린 조합입니다.", "articles": [], "principle": "측정기준 특징 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ이 거짓이므로 전결합은 틀렸습니다.", "articles": [], "principle": "측정기준 특징 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "개념체계 상 현행가치(Current Value) 세부 측정기준들의 성격에 관한 진술 중 옳지 않은 서술만을 모두 고른 것은?\n\n```\nㄱ. 공정가치는 활성시장에서 관측되는 가격으로 직접 결정될 수도 있지만, 없는 경우 기법을 써서 간접 결정될 수도 있다.\nㄴ. 사용가치와 이행가치는 직접 관측될 수 없으며 현금흐름기준 측정기법으로 결정해야 한다.\nㄷ. 공정가치는 측정 시 발생할 미래 궁극적인 자산 처분 시의 거래원가 현재가치를 가격에 가산하여 장부총액을 증액시킨다.\nㄹ. 현행원가는 측정일 현재 동등한 자산의 조달에 지급할 대가에서 당일 발생할 거래원가를 차감한 순액으로 자산가치를 계상한다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄷ, ㄹ",
            "④ ㄱ, ㄹ",
            "⑤ ㄴ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ ㄷ과 ㄹ이 옳지 않은 서술(거짓 명제)입니다.\n\n[오답 해설]\nㄷ. 공정가치는 자산 처분 거래원가를 반영하지 않으므로 가산한다는 진술은 거짓입니다.\nㄹ. 자산의 현행원가는 조달 대가에 측정일에 발생할 거래원가를 **포함(가산)**해야 하므로 차감 순액으로 계상한다는 것은 거짓입니다. (부채의 현행원가는 차감합니다.)\n(ㄱ, ㄴ은 개념체계 상 올바른 설명입니다.)",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ, ㄴ은 참이므로 오답 서술 고르기 대상이 아닙니다.", "articles": [], "principle": "현행가치 세부 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ이 참이므로 잘못된 조합입니다.", "articles": [], "principle": "현행가치 세부 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄷ(공정가치의 처분원가 가산설)과 ㄹ(자산 현행원가의 거래원가 차감설)은 모두 개념체계를 정면 왜곡한 오류 진술입니다.", "articles": [], "principle": "현행가치 세부 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ이 참이므로 틀린 묶음입니다.", "articles": [], "principle": "현행가치 세부 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ이 참이므로 오답입니다.", "articles": [], "principle": "현행가치 세부 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "개념체계 상 자산·부채의 측정기준을 최종 선택할 때, 정보의 근본적 질적 특성인 '목적적합성(Relevance)'을 고려하는 세부 판단 기준으로 가장 옳지 않은 것은?",
        "options": [
            "① 자산이나 부채가 기업의 영업활동 등에서 어떻게 경제적효익을 창출하거나 유도하는지에 관한 정보가 목적적합해야 한다.",
            "② 역사적원가를 사용하는 것이 정보이용자의 의사결정에 더 도움(목적적합)된다면 억지로 현행가치로 재평가하지 않는 것이 합당하다.",
            "③ 금융자산처럼 가치 변동이 극심하고 매도 목적 보유인 자산은 공정가치 등 현행가치를 기재하는 것이 역사적원가 고정액보다 목적적합하다.",
            "④ 측정 기준을 선택할 때는 오직 정보 작성을 편하게 할 수 있는 대형 전산망의 설치 원가 한 가지만을 최우선 목적으로 두고 판단해야 한다.",
            "⑤ 특정 자산의 가치를 추정하는 측정불확실성이 높다면, 역사적원가처럼 검증성이 높고 불확실성이 덜한 대안적 측정기준이 더 목적적합할 수 있다."
        ],
        "answer": "4",
        "explanation": "④ 측정기준의 선택은 정보이용자의 의사결정 유용성(목적적합성과 표현충실성 극대화)이 주 목적이며, 전산 설치의 편의성 등 단일 영업 설비 편의 요인만을 최우선하여 회계기준상 측정기준을 선택하지는 않습니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 측정기준 선택 시 목적적합성(의사결정 기여도, 영업 방식의 연계, 변동성 여부, 측정불확실성 상충 등)을 고려하는 올바른 개념체계의 세부 판단 원칙들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산의 경제적 기여 방식(영업 사용 vs 처분)과 측정기준의 결합 유용성 서술은 참입니다.", "articles": [], "principle": "측정과 목적적합성 고려", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적원가의 정보 유용성이 큰 상황에서의 선택 지침은 참입니다.", "articles": [], "principle": "측정과 목적적합성 고려", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융자산 시가 평가의 목적적합성 서술은 올바른 설명입니다.", "articles": [], "principle": "측정과 목적적합성 고려", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "특정 전산 도입 원가나 단순 부서 편의성만을 극대화하려 회계 측정 원칙을 바꾸는 지침은 존재하지 않으므로 오답입니다.", "articles": [], "principle": "측정과 목적적합성 고려", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정불확실성이 극심할 때 역사적원가의 대체적 유용성 지적은 타당한 참입니다.", "articles": [], "principle": "측정과 목적적합성 고려", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "개념체계 상 자산·부채의 측정기준을 최종 선택할 때, 정보의 근본적 질적 특성인 '표현충실성(Faithful Representation)'을 보장하기 위한 고려 사항으로 가장 올바르지 않은 서술은?",
        "options": [
            "① 관련 자산/부채를 측정할 때 측정불확실성이 높다고 해서 유용한 정보 제공이 반드시 불가능한 것은 아니나, 설명 정보(주석) 제공 등 보조 조치가 필요하다.",
            "② 표현충실성을 달성하려면 재무상태표의 자산·부채 총액과 관련 수익·비용 간의 회계 불일치(Accounting Mismatch)를 최소화할 수 있는 일관된 측정기준 조합을 선택해야 한다.",
            "③ 측정불확실성이 극도로 높다면, 해당 항목을 본문에 인식하지 않고 주석으로만 공시하는 것이 오히려 표현충실성을 극대화하는 올바른 대안이 될 수 있다.",
            "④ 표현충실성을 충족하기 위해서는 장부 가치를 매 결산기마다 기업 대표이사가 원하는 가상 이익 수치에 강제로 뜯어 맞추어 임의 기재하는 재량권이 부여된다.",
            "⑤ 재무정보가 충실하게 표현되려면 사용가치나 이행가치 평가 시 적용된 중요 추정치와 산출 모델 가정을 명확히 기술해야 한다."
        ],
        "answer": "4",
        "explanation": "④ 표현충실성의 핵심 요소는 중립성(Neutrality)과 무오류(Free from Error)입니다. 대표가 자의적으로 이익을 맞추기 위해 가액을 임의 조작 기재하는 것은 표현충실성을 정면으로 파괴하는 행위입니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 측정불확실성의 이해, 회계 불일치 최소화 목적, 측정 보류와 주석 대체 규칙, 그리고 가정도 공시 사항 등 표현충실성을 충족하는 정당한 개념체계 적용 세칙들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "측정불확실성이 유용성을 즉각 훼손하지 않는다는 것은 올바른 진술입니다.", "articles": [], "principle": "측정과 표현충실성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계 불일치를 피하기 위한 일관성 지침은 정당한 참입니다.", "articles": [], "principle": "측정과 표현충실성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "고도 불확실성 시 본문 배정 보류 및 주석 공시는 참입니다.", "articles": [], "principle": "측정과 표현충실성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이익 목표 유도를 위한 가액 자의적 기재는 중립성을 위배하여 표현충실성을 훼손하므로 4가 오답입니다.", "articles": [], "principle": "측정과 표현충실성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추정치 및 가정을 투명하게 기술할 요건은 정당합니다.", "articles": [], "principle": "측정과 표현충실성", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "개념체계 상 공정가치(Fair Value)와 사용가치/이행가치(Value in Use/Fulfilment Value)의 평가 주체 및 기업 특유 성격에 대한 분석 중 가장 올바르지 않은 진술은?",
        "options": [
            "① 공정가치는 활성시장의 시장참전자들의 관점을 수용하여 경제적 기대를 평가한다.",
            "② 사용가치와 이행가치는 자산을 실제 운영하고 부채를 직접 감당하는 특정 보고기업 고유의 기대(기업 특유의 관점)에 맞춘다.",
            "③ 보고기업이 내부 시너지 결합을 가지고 있다면 사용가치가 공정가치보다 유의미하게 크게 산출될 수 있다.",
            "④ 공정가치는 거래원가로 인해 가치가 증감하지 않는 반면, 사용가치/이행가치는 최초 취득 거래원가를 반드시 자산의 가치에 직접 가산한다.",
            "⑤ 사용가치는 기업이 자산을 가동 후 궁극적으로 폐기/처분 시 지출할 것으로 예상되는 미래 거래원가의 현가를 차감 산출(현금 유출에 포함)하는 면이 있다."
        ],
        "answer": "4",
        "explanation": "④ 사용가치와 이행가치는 미래 지향적인 현금흐름의 현재가치 기법을 쓰기 때문에, 과거 사건인 '최초 취득 거래원가'를 자산 가치에 직접 가산(포함)하지 않는 공통점이 있습니다. 따라서 가산한다는 진술은 거짓입니다. (취득 거래원가는 역사적원가나 현행원가에 가산됩니다.)\n\n[오답 해설]\n①, ② 두 기준의 관점 차이에 관한 정확한 대조입니다.\n③ 결합 시너지가 반영되는 사용가치의 특징 상 공정가치보다 크게 나올 수 있습니다.\n⑤ 미래 처분 거래원가는 현금 유출 예정액으로 기산하므로 참입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "공정가치가 시장 관점을 쓴다는 명제는 참입니다.", "articles": [], "principle": "측정기준의 세부 대조", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사용/이행가치가 기업 특유 관점을 쓴다는 명제는 참입니다.", "articles": [], "principle": "측정기준의 세부 대조", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "결합 시너지가 사용가치에만 포함되므로 두 가액이 다를 수 있음은 참입니다.", "articles": [], "principle": "측정기준의 세부 대조", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사용가치 역시 최초 취득 거래원가를 가산하지 않는 원칙을 고수하므로 4는 명백히 틀린 진술입니다.", "articles": [], "principle": "측정기준의 세부 대조", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 처분 원가가 사용가치 평가 시 현금유출 항목으로 계상되는 것은 참입니다.", "articles": [], "principle": "측정기준의 세부 대조", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "개념체계 상 부채의 세 가지 측정 속성(역사적원가, 이행가치, 공정가치)과 부채의 이행 주체 및 신용위험 반영 여부에 대한 설명 중 가장 옳지 않은 것은?",
        "options": [
            "① 역사적원가 하에서는 발생/인수 시 수취 대가에서 최초 거래원가를 직접 차감하는 특징이 있다.",
            "② 공정가치 측정 시에는 시장참전자 관점을 도입하며, 거래원가를 배제하는 한편 자기 신용위험의 변동분을 가치에 투영한다.",
            "③ 이행가치는 기업 특유의 관점을 대변하며 미래 복구/이행에 소요될 거래원가의 현재가치를 의무 총액에 포함한다.",
            "④ 부채의 공정가치는 매 결산기마다 측정일의 최신 신용 상태를 갱신하지만, 역사적원가는 최초 발생 거래 시점의 과거 계약 상태를 고수하여 자기신용 변동을 반영하지 않는다.",
            "⑤ 이행가치는 시장참전자의 평균 거래 이자율만을 맹목적으로 도입하므로, 기업 자체가 파산할 수 있는 자기신용위험을 공정가치보다 훨씬 과격하고 빈번하게 기말 장부에 100% 갱신 기재하는 모형이다."
        ],
        "answer": "5",
        "explanation": "⑤ 이행가치는 시장참전자 관점이 아닌 '기업 특유의 관점'에 근거하며, 기업 자체가 자신의 의무를 이행하는 흐름에 집중합니다. 또한 자기신용위험(자사 파산 확률 상승으로 인한 부채 하락)을 기말 장부에 매번 공정가치보다 기민하고 빈번하게 적극 계상하여 부채를 줄이는 특성을 가지지 않습니다. 오히려 이행가치는 이행해야 할 실물 자원액을 기준으로 하므로 이러한 역설적 자기신용 하락 평가를 방지합니다.\n\n[오답 해설]\n①, ②, ③, ④는 부채의 역사적원가, 공정가치, 이행가치가 가진 거래원가 처리 방식과 신용위험 반영 여부에 대한 정확한 설명들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "부채 역사적원가의 조달원가 차감 규정은 참입니다.", "articles": [], "principle": "부채 측정기준 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치 하의 자기신용위험 반영과 거래원가 배제는 참입니다.", "articles": [], "principle": "부채 측정기준 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이행가치의 기업특유관점 및 미래이행비용 포함 규칙은 참입니다.", "articles": [], "principle": "부채 측정기준 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적원가의 비갱신성과 공정가치의 실시간 신용 변동 반영 구분은 올바릅니다.", "articles": [], "principle": "부채 측정기준 비교", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이행가치는 시장참전자 이자율 맹종 모형이 아니며 기업 특유 관점을 쓰며, 자기신용위험 하락에 따른 부채 평가 이익 변조 효과를 배제하므로 5의 서술은 완전 거짓입니다.", "articles": [], "principle": "부채 측정기준 비교", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "개념체계 상 현행원가(Current Cost) 자산 및 부채 측정에 관한 세부 설명 중 가장 올바르지 않은 서술은?",
        "options": [
            "① 자산의 현행원가는 측정일에 동등한 자산의 원가이며, 그 측정일에 지급할 대가와 거래원가를 포함하여 자산가치를 정한다.",
            "② 부채의 현행원가는 측정일에 동등한 부채에 대해 수취할 수 있는 대가에서 그 날에 발생할 거래원가를 차감한 가치이다.",
            "③ 현행원가는 측정일 현재의 조달 단가에 맞춰 금액을 갱신하는 갱신형 가치 속성이다.",
            "④ 현행원가는 자산을 새로 취득하는 경로인 '투입가치(Entry Value)'에 기반하므로, 처분 시 수취할 '유출가치(Exit Value)'인 공정가치와 구별된다.",
            "⑤ 현행원가 측정 시에는 어떠한 노후화나 사용에 따른 자산 손모 상태도 감가상각으로 누계 차감할 수 없고, 오직 당일 출시된 신제품의 완전 무결한 100% 신품 조달가만을 고집하여 장부에 올려야 한다."
        ],
        "answer": "5",
        "explanation": "⑤ 현행원가를 측정할 때 보고기업이 보유 중인 자산이 이미 일부 사용되었거나 노후화(마모)되었다면, 측정일의 신품 가격을 그대로 적는 것이 아니라 보유 자산의 노후화 수준(감가상각 상태)을 동일한 비율로 차감 반영하여 현행원가를 도출합니다. 신품 가격만을 고집하지 않습니다.\n\n[오답 해설]\n①, ②, ③, ④는 현행원가의 투입원가적 정의, 자산/부채별 거래원가 가산 및 차감 규칙, 그리고 공정가치(유출가치)와의 차이점을 정확히 설명한 참 명제들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산 현행원가의 취득 대가 및 원가 가산은 참입니다.", "articles": [], "principle": "현행원가 규칙 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 현행원가의 수취액 거래원가 차감 규칙은 참입니다.", "articles": [], "principle": "현행원가 규칙 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현행원가가 측정일 정보 갱신형 속성임은 참입니다.", "articles": [], "principle": "현행원가 규칙 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "투입가치와 유출가치의 이론적 구분은 올바릅니다.", "articles": [], "principle": "현행원가 규칙 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사용 중인 자산은 측정일 현재 가치로 갱신하되 기존 노후화 상태를 상각 차감 반영하므로, 신품 가격만을 기재한다는 진술은 오류입니다.", "articles": [], "principle": "현행원가 규칙 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },

    # =========================================================================
    # L5: 심화 (2문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s08-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "부채를 공정가치(Fair Value)로 측정할 때, 기업 자체의 신용도 하락(자기신용위험 악화)으로 인한 부채의 평가 감소액을 당기이익(Gain)으로 인식하는 회계처리가 지니는 재무보고 상의 역설적 왜곡과, 현행 기준서가 취하는 보완책에 대한 분석으로 가장 올바르지 않은 설명은?",
        "options": [
            "① 자사의 신용등급 강등(경영 상태 악화)이라는 악재가 발생했음에도, 장부상 부채의 하락으로 인해 대규모 '평가이익'이 계상되어 당기순이익이 증가하는 모순을 낳는다.",
            "② 이는 기업이 당장 회사채 채무를 시장에서 헐값에 매입해 소멸(상환)시킬 것이 아니라면, 실현 불가능한 가상 이익을 보여줌으로써 의사결정에 혼선을 준다.",
            "③ 현행 기준서(IFRS 9 등)는 이러한 왜곡을 막기 위해, 자기신용위험 변동에 따른 금융부채 공정가치 평가 차액을 당기순이익이 아닌 '기타포괄손익(OCI)'으로 구분 적립하여 손익 왜곡을 배제한다.",
            "④ 자기신용도 하락으로 인한 부채 평가이익은 기말에 무조건 대표이사의 사적 계좌로 즉시 현금 인출할 수 있는 실물 배당금의 성격을 가지므로 유용성이 지지된다.",
            "⑤ 자기신용위험 변동 효과의 OCI 분류는 보고기업의 부도 가능성 증대 시 손익계산서가 영업 성과를 긍정적으로 왜곡 묘사하는 한계를 보완하는 충실한 표현 수단이다."
        ],
        "answer": "4",
        "explanation": "④ 자기신용위험 하락에 따른 부채 감소 평가액은 미실현 보유 이익의 성격일 뿐이며, 사외로 유출하거나 대표이사 개인이 사적으로 인출할 수 있는 실물 현금(배당금)이 절대 아닙니다. 이를 기말 현금 인출 대상으로 기술한 4의 서술은 완전한 허구입니다.\n\n[오답 해설]\n① 경영 악화 시 장부 이익이 생기는 회계적 역설을 정확히 상술했습니다.\n② 실현 불가능한 이익 보고에 따른 정보 유용성 훼손 한계 지적은 타당합니다.\n③ 기준서 상 자기신용위험 OCI 분류 강제 규정의 이론적 배경을 정확히 기술했습니다.\n⑤ 기타포괄손익 분류의 재무보고 상 기여(충실한 표현 달성)에 관한 바른 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자기신용 위험 하락에 따른 역설적인 장부 이익 묘사는 참입니다.", "articles": [], "principle": "자기신용위험 역설 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가정이 무너진 상황에서 생기는 미실현 이익의 정보 왜곡 가능성 지적은 참입니다.", "articles": [], "principle": "자기신용위험 역설 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "IFRS 9의 OCI(기타포괄손익) 지정 규정의 이론적 배경은 정확한 사실입니다.", "articles": [], "principle": "자기신용위험 역설 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "미실현 평가 손익을 사적 현금으로 인출할 수 있다는 설명은 자본 침탈이자 있을 수 없는 가공의 기술이므로 4가 정답입니다.", "articles": [], "principle": "자기신용위험 역설 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기타포괄손익 분류가 재무제표 투명성(표현충실성)에 기여한다는 결론은 정당합니다.", "articles": [], "principle": "자기신용위험 역설 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 5,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s08-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "자산의 현행원가(Current Cost)와 역사적원가(Historical Cost)의 투입 원가(Entry Value) 속성 비교 및 자본유지개념(Capital Maintenance Concepts) 하에서의 성과 측정에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 역사적원가와 현행원가는 자산을 매각할 때 받는 유출 가격이 아닌, 자산을 시장에서 조달/취득할 때 지급하는 투입 원가에 기초한다는 점에서 이론적 근원을 공유한다.",
            "② 실물자본유지(Physical Capital Maintenance) 개념 하에서는 기업의 실물 조달 능력을 유지하는 것을 자본 유지로 보므로, 기말 기계나 재고자산의 현행원가 상승에 따른 가치 변동액은 당기순이익이 아닌 '자본유지조정(자본란)'으로 적립하여 배당 유출을 제한한다.",
            "③ 역사적원가 하에서의 당기순이익은 물가 상승 시 미실현 보유 손익과 영업 성과가 혼재되어 나타나지만, 현행원가 회계를 적용하면 순수한 영업 성과(Operating Income)와 보유 손익(Holding Gain/Loss)을 구분하여 보고할 수 있는 정보 효과가 있다.",
            "④ 현행원가 측정 시 기말의 조달 가격 상승액 전체를 당기 매출액에 억지로 합산하여 보고하면 영업 실질이 왜곡되므로, 개념체계는 이를 주석으로 분류 기술하도록 유도한다.",
            "⑤ 현행원가 회계는 측정일에 동등한 자산의 조달 가격을 매번 추정해야 하므로 거래 증빙 중심의 역사적원가 회계에 비해 작성 원가가 높고 측정불확실성이 커서 실무 적용이 제한적이다."
        ],
        "answer": "4",
        "explanation": "④ 현행원가 회계처리 시 자산의 조달 단가 상승(현행원가 변동)에 따른 가치 상승액은 자산의 가치를 높여주고 동액의 자본유지조정(실물자본유지 시) 혹은 보유이익(재무자본유지 시)으로 계상하는 것이지, 이를 물건을 팔아서 생긴 '당기 매출액'에 억지로 가산하여 수익을 조작하는 방식으로 보고하지 않습니다.\n\n[오답 해설]\n① 둘 다 투입원가(Entry Value)를 모태로 함은 참입니다.\n② 실물자본유지 개념 하의 자본유지조정(Capital Maintenance Adjustments) 처리에 관한 바른 회계 이론입니다.\n③ 현행원가가 보유이익과 영업 성과를 분리해 정보 유용성을 높여 주는 강점에 관한 서술입니다.\n⑤ 현행원가 회계의 실무 상 한계(작성 비용 과다, 측정의 임의성)를 적절히 짚었습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "조달 관점의 투입가치 속성을 공유한다는 분석은 참입니다.", "articles": [], "principle": "현행원가와 자본유지이론", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실물자본유지 하에서 자산 가격 상승분을 이익이 아닌 자본조정(자본유지조정)으로 적립하는 규칙은 참입니다.", "articles": [], "principle": "현행원가와 자본유지이론", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "물가상승 시 영업이익과 보유이익의 분리 유용성에 관한 지적은 참입니다.", "articles": [], "principle": "현행원가와 자본유지이론", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "현행원가 상승액을 당기 매출액으로 위장하여 가산 보고하는 방식은 존재하지 않으며 심각한 조작 분개이므로 4가 오답입니다.", "articles": [], "principle": "현행원가와 자본유지이론", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현행원가 추정의 작성 원가 및 신뢰성/불확실성 단점 지적은 정당한 사실입니다.", "articles": [], "principle": "현행원가와 자본유지이론", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 5,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 01 개념체계",
                "item": "8절 측정"
            }
        }
    }
]

# Append new questions
questions.extend(new_questions)

# Save updated questions
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(new_questions)} new questions. Total questions in questions_db_accounting.json: {len(questions)}")
