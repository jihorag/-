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
        "id": "practice-accounting-ch01s04-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "개념체계 상 재무보고의 '근본적 질적 특성(Fundamental Qualitative Characteristics)'에 해당하는 것으로만 짝지어진 것은?",
        "options": [
            "① 목적적합성, 비교가능성",
            "② 표현충실성, 검증가능성",
            "③ 목적적합성, 표현충실성",
            "④ 비교가능성, 이해가능성",
            "⑤ 적시성, 이해가능성"
        ],
        "answer": "3",
        "explanation": "③ 개념체계 상 근본적 질적 특성은 '목적적합성'과 '표현충실성' 두 가지입니다. 나머지는 모두 보강적 질적 특성에 해당합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비교가능성은 보강적 질적 특성입니다.", "articles": [], "principle": "질적 특성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "검증가능성은 보강적 질적 특성입니다.", "articles": [], "principle": "질적 특성 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "목적적합성과 표현충실성이 근본적 질적 특성입니다.", "articles": [], "principle": "근본적 질적 특성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비교가능성과 이해가능성은 모두 보강적 질적 특성입니다.", "articles": [], "principle": "질적 특성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적시성과 이해가능성은 모두 보강적 질적 특성입니다.", "articles": [], "principle": "질적 특성 분류", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "개념체계 상 재무보고의 '보강적 질적 특성(Enhancing Qualitative Characteristics)'에 해당하지 않는 것은?",
        "options": [
            "① 중요성(Materiality)",
            "② 비교가능성(Comparability)",
            "③ 검증가능성(Verifiability)",
            "④ 적시성(Timeliness)",
            "⑤ 이해가능성(Understandability)"
        ],
        "answer": "1",
        "explanation": "① 중요성(Materiality)은 목적적합성의 개별 기업 측면의 속성으로, 근본적 질적 특성인 목적적합성에 포함되는 하위 개념입니다. 보강적 질적 특성 4가지는 비교가능성, 검증가능성, 적시성, 이해가능성입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "중요성은 근본적 질적 특성인 목적적합성의 하위 요소입니다.", "articles": [], "principle": "보강적 질적 특성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비교가능성은 보강적 질적 특성입니다.", "articles": [], "principle": "보강적 질적 특성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "검증가능성은 보강적 질적 특성입니다.", "articles": [], "principle": "보강적 질적 특성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적시성은 보강적 질적 특성입니다.", "articles": [], "principle": "보강적 질적 특성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이해가능성은 보강적 질적 특성입니다.", "articles": [], "principle": "보강적 질적 특성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "다음 중 근본적 질적 특성인 '목적적합성(Relevance)'과 직접적인 관련이 없는 개념은?",
        "options": [
            "① 예측가치(Predictive Value)",
            "② 확인가치(Confirmatory Value)",
            "③ 중요성(Materiality)",
            "④ 의사결정에의 영향력",
            "⑤ 중립성(Neutrality)"
        ],
        "answer": "5",
        "explanation": "⑤ 중립성(Neutrality)은 '표현충실성'의 세 가지 구성 요소(완전성, 중립성, 오류 없음) 중 하나입니다. 예측가치, 확인가치, 중요성은 모두 목적적합성과 관련이 있는 하위 속성입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "예측가치는 목적적합성의 하위 요소입니다.", "articles": [], "principle": "목적적합성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "확인가치는 목적적합성의 하위 요소입니다.", "articles": [], "principle": "목적적합성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중요성은 목적적합성의 하위 요소입니다.", "articles": [], "principle": "목적적합성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의사결정에 차이를 나도록 하는 성질이 목적적합성의 본질입니다.", "articles": [], "principle": "목적적합성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "중립성은 표현충실성의 하위 요소입니다.", "articles": [], "principle": "표현충실성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "다음 중 근본적 질적 특성인 '표현충실성(Faithful Representation)'을 이루는 세 가지 서술적 요건에 해당하는 것으로만 묶인 것은?",
        "options": [
            "① 예측가치, 확인가치, 중요성",
            "② 완전한 서술, 중립적 서술, 오류 없는 서술",
            "③ 비교가능성, 검증가능성, 적시성",
            "④ 중립적 서술, 신중성, 일관성",
            "⑤ 적시성, 오류 없는 서술, 중립적 서술"
        ],
        "answer": "2",
        "explanation": "② 개념체계는 표현충실성이 완벽하기 위해 서술에 완전함(Completeness), 중립성(Neutrality), 오류 없음(Free from error)의 세 가지 특성이 있어야 한다고 명시합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "목적적합성의 세부 속성들입니다.", "articles": [], "principle": "목적적합성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "완전, 중립, 오류 없음이 표현충실성의 3대 서술 요건입니다.", "articles": [], "principle": "표현충실성 3대 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보강적 질적 특성들입니다.", "articles": [], "principle": "보강적 질적 특성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "신중성은 중립성을 뒷받침하며, 일관성은 비교가능성의 수단입니다.", "articles": [], "principle": "질적 특성 세부개념", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적시성은 보강적 질적 특성입니다.", "articles": [], "principle": "질적 특성 분류", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "재무보고로 제공되는 정보의 포괄적 제약요인(Pervasive Constraint)에 해당하는 것은?",
        "options": [
            "① 중요성(Materiality)",
            "② 신중성(Prudence)",
            "③ 측정불확실성(Measurement Uncertainty)",
            "④ 원가(Cost)",
            "⑤ 일관성(Consistency)"
        ],
        "answer": "4",
        "explanation": "④ 개념체계 상 재무보고에 대한 포괄적 제약요인은 '원가(Cost)'입니다. 재무정보의 효익은 정보 제공을 위해 지출되는 원가를 정당화해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "중요성은 목적적합성의 개별 기업적 측면의 제한입니다.", "articles": [], "principle": "중요성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "신중성은 판단 상의 주의로 제약요인이 아닙니다.", "articles": [], "principle": "신중성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정불확실성은 추정에서 발생하지만 포괄적 제약요인은 아닙니다.", "articles": [], "principle": "측정불확실성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "원가는 재무정보 보고에 대한 포괄적 제약요인입니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일관성은 비교가능성의 방법론적 수단입니다.", "articles": [], "principle": "일관성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "개념체계가 규정하는 '유용한 재무정보의 질적 특성'의 적용 범위에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 오직 법적으로 의무 공시되는 재무제표 본문에만 적용된다.",
            "② 재무제표에 제공되는 재무정보뿐만 아니라, 그 밖의 방법으로 제공되는 재무정보에도 적용된다.",
            "③ 주석을 제외한 자산, 부채, 자본의 계량적 수치에만 제한 적용된다.",
            "④ 재무보고 이외에 기업이 발표하는 모든 마케팅 및 IR 홍보자료에도 법적 강제력으로 적용된다.",
            "⑤ 상장기업의 내부 의사결정용 관리회계 보고서에만 전적으로 적용된다."
        ],
        "answer": "2",
        "explanation": "② 개념체계의 마지막 문단(질적 특성의 적용범위)에 따라, 유용한 재무정보의 질적 특성은 재무제표에서 제공되는 재무정보뿐만 아니라 그 밖의 방법으로 제공되는 재무정보(예: 중간보고서, 추가 공시 등)에도 적용됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재무제표 본문 외의 재무정보에도 적용됩니다.", "articles": [], "principle": "질적 특성 적용범위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재무제표 정보 및 그 외 재무보고서의 정보 전체에도 적용된다는 지문은 올바릅니다.", "articles": [], "principle": "질적 특성 적용범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석도 질적 특성이 당연히 적용되는 재무제표의 일부입니다.", "articles": [], "principle": "질적 특성 적용범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "마케팅이나 IR 홍보자료 전반에 개념체계가 법적 강제력으로 적용되지는 않습니다.", "articles": [], "principle": "질적 특성 적용범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "관리회계 보고서는 개념체계의 대상이 아닙니다.", "articles": [], "principle": "질적 특성 적용범위", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "개념체계 상 근본적 질적 특성 중 하나인 '목적적합성(Relevance)'의 가장 기초적인 정의에 부합하는 서술은?",
        "options": [
            "① 거래와 사건의 세법적 적법성을 회계담당자가 완전히 보장하는 성질",
            "② 정보이용자가 기업의 청산 가치를 100% 동일하게 추적할 수 있도록 획일화하는 성질",
            "③ 재무 정보가 정보이용자의 의사결정에 차이가 나도록 할 수 있는 성질",
            "④ 재무제표의 모든 기재 금액이 소수점 이하까지 정확하게 수렴하는 성질",
            "⑤ 경영진이 수탁 책임을 지지 않도록 재량적으로 보고서를 조작할 수 있는 권한"
        ],
        "answer": "3",
        "explanation": "③ 목적적합한 재무정보는 정보이용자의 의사결정에 차이가 나도록 할 수 있습니다. 의사결정에 차이를 유발하지 못하는 정보는 목적적합하지 않은 정보입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "세법의 적법성 보장과는 무관한 개념입니다.", "articles": [], "principle": "목적적합성 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "청산가치 획일화와 무관합니다.", "articles": [], "principle": "목적적합성 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이용자의 의사결정에 차이가 나도록 할 수 있는 정보가 목적적합하다는 설명은 정확합니다.", "articles": [], "principle": "목적적합성 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소수점 수리적 정확성은 표현충실성(오류 없음)에 가깝습니다.", "articles": [], "principle": "오류 없음", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진의 조작 권한과는 관련이 없습니다.", "articles": [], "principle": "목적적합성 정의", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "개념체계 상 근본적 질적 특성 중 하나인 '표현충실성(Faithful Representation)'의 가장 본질적인 지향점은?",
        "options": [
            "① 경제적 현상의 실질을 글과 숫자로 충실하게 표현하는 것",
            "② 기업의 법적 형식을 있는 그대로 모사하여 실질에 관계없이 기재하는 것",
            "③ 주식시장의 일일 주가 변동 차트를 기재하는 것",
            "④ 외부 감사인이 작성한 감사보고서의 의견 문구를 100% 카피하는 것",
            "⑤ 회계담당자의 임의적인 판단을 전면 배제하고 오직 현금 출납만을 기록하는 것"
        ],
        "answer": "1",
        "explanation": "① 표현충실성은 나타내고자 하는 현상의 실질을 글과 숫자로 충실하게 표현하는 것을 의미합니다. 많은 경우 경제적 현상의 실질과 법적 형식은 같지만, 만약 다르다면 법적 형식이 아닌 실질을 반영해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "경제적 실질을 글과 숫자로 나타내는 것이 표현충실성의 본질입니다.", "articles": [], "principle": "표현충실성 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실질과 법적 형식이 다를 때는 실질을 우선 공시해야 충실한 표현이 됩니다.", "articles": [], "principle": "실질의 우선", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주가 변동 차트 기재를 지향하지 않습니다.", "articles": [], "principle": "표현충실성 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사의견 카피가 목적이 아닙니다.", "articles": [], "principle": "표현충실성 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추정과 판단은 필수적이며 현금주의만을 강제하지 않습니다.", "articles": [], "principle": "발생주의와 추정", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "보강적 질적 특성 중 하나인 '비교가능성(Comparability)'의 고유한 성격에 관한 설명으로 옳은 것은?",
        "options": [
            "① 단 하나의 단독 재무 항목만을 놓고 관찰할 때 최대로 발휘된다.",
            "② 최소한 두 항목 이상이 있어야만 비교가 성립된다.",
            "③ 일관성(Consistency)과 명칭 및 정의가 완벽히 동일하다.",
            "④ 모든 기업의 자산 규모를 강제로 통일(Uniformity)시키는 것을 목표로 한다.",
            "⑤ 발생주의 회계를 폐기해야만 비로소 발현될 수 있다."
        ],
        "answer": "2",
        "explanation": "② 다른 질적 특성과 달리 비교가능성은 단 하나의 항목에만 관련된 것이 아니며, 비교를 하려면 최소한 두 항목이 필요합니다. 또한 일관성과 비교가능성은 다른 개념이며(일관성은 수단, 비교가능성은 목표), 비교가능성은 통일성이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "단 하나의 항목으로는 비교가 불가능합니다.", "articles": [], "principle": "비교가능성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비교를 위해서는 최소한 두 항목이 존재해야 한다는 설명은 옳습니다.", "articles": [], "principle": "비교가능성 속성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일관성은 수단이며 비교가능성은 도달 목표이므로 다릅니다.", "articles": [], "principle": "비교가능성 vs 일관성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "통일성과 다릅니다. 비슷한 것은 비슷하게, 다른 것은 다르게 보여야 합니다.", "articles": [], "principle": "비교가능성 vs 통일성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "발생주의 하에서 당연히 비교가능성이 추구됩니다.", "articles": [], "principle": "발생주의", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "보강적 질적 특성 중 하나인 '적시성(Timeliness)'의 기본 목적은?",
        "options": [
            "① 의사결정자가 의사결정에 영향을 미칠 수 있도록 제때에 정보가 이용 가능하게 하는 것",
            "② 매일 아침 주식 장 개시 전에 무조건 일일 자산 총계보고를 공시하는 것",
            "③ 보고기간 말이 지나면 전년도 재무제표의 모든 역사적 수치를 자동으로 소각하는 것",
            "④ 작성 원가가 효익을 아무리 초과하더라도 실시간 속도로만 데이터를 전송하는 것",
            "⑤ 회계담당자가 정보를 작성하는 즉시 수정 불가능하도록 영구 락(Lock)을 거는 것"
        ],
        "answer": "1",
        "explanation": "① 적시성은 의사결정에 영향을 미칠 수 있도록 의사결정자가 정보를 제때에 이용할 수 있게 하는 것을 의미합니다. 오래된 정보일수록 유용성이 떨어지기 때문입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "적시성은 제때에 의사결정자에게 정보를 제공하여 의사결정에 기여함을 목적으로 합니다.", "articles": [], "principle": "적시성 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매일 아침 강제 보고 규정은 개념체계에 없습니다.", "articles": [], "principle": "적시성 오독", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과거 재무제표를 소각하지 않고 비교정보로 활용합니다.", "articles": [], "principle": "비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "포괄적 제약인 원가 제약은 적시성 추구 시에도 적용됩니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영구 락과 관련이 없습니다.", "articles": [], "principle": "적시성 오독", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },

    # =========================================================================
    # L2: 이해 수준 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s04-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "개념체계 상 재무정보가 '예측가치(Predictive Value)'를 갖기 위한 요건에 관한 설명으로 옳은 것은?",
        "options": [
            "① 재무정보 자체가 미래의 확실한 예측치 또는 예상치이어야만 한다.",
            "② 정보이용자가 미래 결과를 예측하기 위해 사용하는 절차의 입력요소(Input)로 사용될 수 있으면 족하다.",
            "③ 과거 평가에 대해 어떠한 확인이나 변경을 가져오지 않는 순수 독립적 미래 보고서이어야 한다.",
            "④ 주총에서 주주 전원이 만장일치로 미래 가치를 인정한 보고서이어야 한다.",
            "⑤ 회계담당자가 임의로 조작한 미래 현금유입의 가상 시나리오이어야 한다."
        ],
        "answer": "2",
        "explanation": "② 재무정보가 예측가치를 갖기 위해서 그 자체가 예측치 또는 예상치일 필요는 없습니다. 이용자들이 미래 결과를 예측하기 위해 사용하는 절차의 투입요소(입력치)로 사용될 수 있다면 그 정보는 예측가치를 갖습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "예측가치를 갖기 위해 자체가 예측치/예상치일 필요는 없습니다.", "articles": [], "principle": "예측가치 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "예측 절차의 입력요소로 사용될 수 있다면 예측가치를 가진다는 설명은 완전히 옳습니다.", "articles": [], "principle": "예측가치 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "확인가치와 상호 연관되어 있어 피드백을 수반하는 경우가 많습니다.", "articles": [], "principle": "예측가치와 확인가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주주 만장일치 요건은 전혀 없습니다.", "articles": [], "principle": "예측가치 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 조작이나 가상 시나리오는 표현충실성 위배입니다.", "articles": [], "principle": "표현충실성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "재무보고 개념체계 상 '예측가치'와 '확인가치(Confirmatory Value)'의 상호관계에 대한 설명 중 옳은 것은?",
        "options": [
            "① 예측가치를 갖는 정보는 본질적으로 확인가치를 가질 수 없도록 차단된다.",
            "② 예측가치와 확인가치는 서로 독립적이어서 두 속성은 상호 연관될 수 없다.",
            "③ 예측가치를 갖는 정보는 과거 평가를 변경하거나 확인하는 피드백 정보, 즉 확인가치도 갖는 경우가 많다.",
            "④ 확인가치는 오직 역사적 원가 정보에만 속하며, 예측가치는 오직 공정가치 정보에만 귀속된다.",
            "⑤ 하나의 보고서가 예측가치와 확인가치를 동시에 제공하면 감리 지적 대상이 된다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계 상 재무정보의 예측가치와 확인가치는 서로 밀밀히 연관되어 있습니다. 예측가치를 갖는 정보는 과거 평가를 확인하거나 변경시키는 확인가치도 동시에 가지는 경우가 많습니다(예: 당기 매출액 정보는 내년 매출 예측의 입력요소가 되는 동시에, 작년에 예측했던 금년 매출에 대한 피드백 역할을 함).",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "두 가치는 배타적이지 않으며 상호 보완적입니다.", "articles": [], "principle": "예측가치와 확인가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "독립적이지 않고 상호 유기적으로 결합되어 있습니다.", "articles": [], "principle": "예측가치와 확인가치", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "예측가치를 지닌 정보가 확인가치도 겸하는 경우가 흔하다는 설명은 정확합니다.", "articles": [], "principle": "예측가치와 확인가치 연관성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정 기준에 따라 한 가치만 갖도록 분할되지 않습니다.", "articles": [], "principle": "측정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "동시 제공은 권장되는 사항으로 감리 제재 대상이 아닙니다.", "articles": [], "principle": "유용한 정보", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "개념체계 상 재무보고의 '중요성(Materiality)'에 관한 성격을 올바르게 이해한 기술은?",
        "options": [
            "① 중요성은 모든 보고기업에 일률적으로 적용되는 회계기준위원회(IASB)의 통일 기준이다.",
            "② 정보가 누락되더라도 의사결정에 영향을 주지 않는다면 무조건 중요성이 인정된다.",
            "③ 중요성은 보고기업 특유의 관점에서 정보의 성격이나 규모, 또는 이 둘 모두에 근거한 특유한 측면의 목적적합성이다.",
            "④ 중요성은 보강적 질적 특성 중 이해가능성을 높이기 위해 임의로 자산을 생략하는 권한이다.",
            "⑤ 중요성이 성격에 기초해 평가될 때는 기업의 자산 총액 비율만 반영해야 한다."
        ],
        "answer": "3",
        "explanation": "③ 중요성은 개별 기업 재무보고서 관점에서 해당 정보와 관련된 항목의 성격이나 규모, 또는 이 둘 모두에 근거하여 해당 기업에 특유한 측면의 목적적합성을 의미합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "일률적인 통일 기준이 아닌 개별 기업 특유의 기준입니다.", "articles": [], "principle": "중요성의 개별성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의사결정에 영향을 주는 정보라야 중요한 정보입니다.", "articles": [], "principle": "중요성 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "성격이나 규모에 근거한 기업 특유의 목적적합성이라는 정의는 전적으로 부합합니다.", "articles": [], "principle": "중요성 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의로 정보를 은폐/생략하는 권리가 아닙니다.", "articles": [], "principle": "중요성 오독", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "성격에 기초할 때는 비율 수치가 아닌 항목 자체의 고유 성질(예: 특수관계자 거래 등)이 중요할 수 있습니다.", "articles": [], "principle": "성격적 중요성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "회계기준위원회(K-KASB 또는 IASB)가 중요성에 대하여 내린 업무 방식에 관한 개념체계 상의 올바른 서술은?",
        "options": [
            "① 회계기준위원회는 모든 산업에 일괄 적용할 자산 대비 5% 등의 획일적인 계량 임계치를 정하여 공표해야 한다.",
            "② 회계기준위원회는 중요성에 대한 획일적인 계량 임계치를 정하거나 특정한 상황에서 무엇이 중요한 것인지를 미리 결정할 수 없다.",
            "③ 위원회는 매년 분기별로 기업의 시가총액을 고려해 개별 기업용 임계치를 법률로 고시해야 한다.",
            "④ 중요성은 회계감사인만의 전유물이므로 기준위원회는 중요성 규정 자체를 개념체계에 수록하지 않는다.",
            "⑤ 중요성이 판단되면 모든 유형자산은 강제로 공정가치로만 계상하도록 지시해야 한다."
        ],
        "answer": "2",
        "explanation": "② 중요성은 개별 보고기업의 특유한 상황에 의존하므로, 회계기준위원회는 중요성에 대한 획일적인 계량 임계치를 사전에 일방적으로 정하거나 특정한 상황에서 무엇이 중요한 것인지를 미리 결정할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "획일적 임계치를 정해두지 않았습니다.", "articles": [], "principle": "중요성 기준", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "계량 임계치를 미리 정하거나 무엇이 중요한지 결정할 수 없다는 지문은 개념체계의 명확한 서술입니다.", "articles": [], "principle": "임계치 결정 불가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "분기별로 고시하지 않습니다.", "articles": [], "principle": "중요성 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "개념체계 목적적합성 항목 하에 공식적으로 수록되어 있습니다.", "articles": [], "principle": "개념체계 체계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정 기준 지정과는 관련성이 없습니다.", "articles": [], "principle": "측정 기준", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "재무제표 작성에 수반되는 '측정불확실성(Measurement Uncertainty)'과 재무정보의 유용성에 관한 개념체계의 설명으로 올바른 것은?",
        "options": [
            "① 측정불확실성이 높다면 해당 추정 정보는 의사결정에 전혀 기여할 수 없어 무조건 재무제표에서 배제되어야 한다.",
            "② 합리적인 추정치의 사용은 재무정보의 작성에 필수적인 부분이며, 추정이 명확하고 정확하게 기술되고 설명되는 한 정보의 유용성을 저해하지 않는다.",
            "③ 개념체계는 어떠한 형태의 추정이나 판단도 완벽한 표현충실성 달성을 위해 전면 차단한다.",
            "④ 높은 측정불확실성이 있는 충당부채는 재무상태표 부채 항목에 수록될 법적 권리가 전면 박탈된다.",
            "⑤ 추정을 완화하기 위해 모든 자산의 기말 평가는 오직 정부가 지정한 고정 고시가로 대체한다."
        ],
        "answer": "2",
        "explanation": "② 측정불확실성은 화폐액을 직접 관측할 수 없어 추정할 때 생깁니다. 개념체계에 따르면, 합리적 추정치는 필수적인 요소이며 이것이 유용성을 훼손하지 않습니다. 심지어 측정불확실성의 수준이 높더라도 그러한 추정이 유용한 재무정보를 제공할 수도 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "불확실성이 높더라도 정보가 유용할 수 있어 무조건 배제하지 않습니다.", "articles": [], "principle": "측정불확실성과 유용성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "추정의 합리적 사용은 필수적이며 명확히 설명되는 한 유용성을 저해하지 않는다는 기술은 옳습니다.", "articles": [], "principle": "측정불확실성 인정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추정과 모형의 사용은 지극히 정상적인 회계 기법입니다.", "articles": [], "principle": "추정 판단 개입", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 요건을 충족하면 높은 불확실성 하에서도 부채로 인식할 수 있습니다.", "articles": [], "principle": "인식 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정부 고시가 대체 강제는 회계기준에 부합하지 않습니다.", "articles": [], "principle": "가치평가", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "표현충실성의 서술적 요소 중 '완전한 서술(Complete depiction)'이 제공해야 하는 정보 범위로 가장 올바른 설명은?",
        "options": [
            "① 기업의 영업 비밀과 미공개 기밀 특허 설계도까지 상세히 기술해야 한다.",
            "② 정보이용자가 서술되는 경제적 현상을 이해하는 데 필요한 모든 기술과 설명을 포함하여야 한다.",
            "③ 대차대조표의 자산 과목 수치만을 표기하고, 주석은 전면 생략하여 간결성을 극대화해야 한다.",
            "④ 미래 발생할 가능성이 1% 미만인 모든 무작위 사건을 무제한 나열해야 한다.",
            "⑤ 외부 감사인의 감사 조서 세부 사본 전체를 파일로 첨부해야 한다."
        ],
        "answer": "2",
        "explanation": "② 완전한 서술은 필요한 기술과 설명을 포함하여 이용자가 서술되는 현상을 이해하는 데 필요한 '모든 정보'를 포함하는 것을 말합니다. 영업 비밀 노출이나 무제한 감사조서 첨부 등은 해당하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기업의 경영상 영업 비밀 유출까지 요구하지 않습니다.", "articles": [], "principle": "완전한 서술 한계", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "경제 현상 이해를 돕기 위한 서술, 기술, 설명을 모두 포함한다는 지문은 올바릅니다.", "articles": [], "principle": "완전한 서술 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석을 전면 생략하는 것은 완전성 위배입니다.", "articles": [], "principle": "완전한 서술", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무작위 사건의 무제한 나열은 오히려 이해가능성을 훼손합니다.", "articles": [], "principle": "이해가능성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사조서 사본 첨부 의무는 없습니다.", "articles": [], "principle": "완전한 서술", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "표현충실성의 서술적 요소 중 '중립적 서술(Neutral depiction)'에 대한 설명으로 올바른 것은?",
        "options": [
            "① 중립적 정보는 재무성과가 나쁘게 보이도록 의도적으로 왜곡 감액하는 지침이다.",
            "② 중립적 서술은 재무정보의 선택이나 표시에 편의(bias)가 없는 것이다.",
            "③ 중립적 정보는 정의상 목적이 없거나 이용자들의 행동에 영향력을 미칠 수 없는 죽은 정적 정보이다.",
            "④ 중립성을 지키기 위해 이사회는 보고서에 어떠한 정성적 코멘트도 달 수 없다.",
            "⑤ 중립성은 세무당국이 요구하는 세수 과표를 그대로 차용하는 것을 강제한다."
        ],
        "answer": "2",
        "explanation": "② 중립적 서술은 재무정보의 선택이나 표시에 편의가 없는 것입니다. 중립적 서술은 편중되거나 왜곡, 조작되지 않습니다. 또한 중립적 정보는 '목적이 없거나 행동에 영향이 없는 것'을 의미하지 않습니다. 목적적합한 정보는 중립적이라도 의사결정에 차이를 내게 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "의도적 왜곡 감액은 중립성 위배이며 편의가 개입된 상태입니다.", "articles": [], "principle": "중립성 위배", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "선택과 표시에 편의가 배제된 상태가 중립성이라는 진술은 전적으로 정당합니다.", "articles": [], "principle": "중립적 서술 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중립적 정보라도 목적적합하게 행동에 영향을 줍니다.", "articles": [], "principle": "중립성의 오독", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정성적 코멘트도 중립적으로 기재할 수 있습니다.", "articles": [], "principle": "완전성과 중립성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 과표 차용과 관련이 없습니다.", "articles": [], "principle": "중립적 서술", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "표현충실성의 속성인 '오류 없는 서술(Free from error)'에 대한 개념체계의 설명으로 올바른 것은?",
        "options": [
            "① 오류가 없다는 것은 재무보고서의 모든 숫자 서술이 단 1원도 틀리지 않고 완벽하게 정확해야 함을 의미한다.",
            "② 오류가 없다는 것은 현상의 기술에 오류나 누락이 없고, 보고 정보를 생산하는 데 사용되는 절차의 선택과 적용 시 절차상 오류가 없음을 의미한다.",
            "③ 대손설정 등 추정액이 실제 기말 시점과 차이가 발생했다면, 이는 '오류 없는 서술' 지침을 명백히 위배한 불법 회계이다.",
            "④ 기말 재고실사에서 발생한 모든 감모손실은 즉각 분식회계 죄목으로 법적 기소 대상이 된다.",
            "⑤ 회계담당자가 계산기를 잘못 눌러 발생한 단순 오타도 표현충실성이 있는 것으로 간주한다."
        ],
        "answer": "2",
        "explanation": "② 이 맥락에서 오류가 없다는 것은 모든 면에서 완벽하게 정확하다는 것을 의미하지는 않습니다. 현상의 기술에 오류나 누락이 없고, 보고 정보를 생산하는 데 사용되는 절차의 선택과 적용 시 절차상 오류가 없음을 의미하는 것입니다. (추정의 경우 절차 선택에 오류가 없다면 충실하게 표현되었다고 봅니다.)",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "완벽하게 정확해야 함을 의미하는 것은 불가능에 가깝고 기준서 지침도 아닙니다.", "articles": [], "principle": "오류 없음의 의의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기술 상의 오류 누락이 없고 절차 선택/적용에 오류가 없음을 뜻한다는 지문은 정확합니다.", "articles": [], "principle": "오류 없는 서술 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "합리적인 추정치의 차이는 단순 오류 위법이 아닙니다.", "articles": [], "principle": "추정치의 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감모손실은 일반적인 회계 영업 사건일 뿐 범죄가 아닙니다.", "articles": [], "principle": "재고 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 오타 등은 절차상 오류에 속하므로 표현충실성을 저해합니다.", "articles": [], "principle": "절차상 오류", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "보강적 질적 특성인 '검증가능성(Verifiability)'의 요건에 관한 개념체계 상의 진술로 올바른 것은?",
        "options": [
            "① 검증가능성이 확보되려면, 기재 정보가 오직 단일 점추정치(Single point estimate)로만 기재되어야 하며 범위 표시는 불가능하다.",
            "② 합리적인 판단력이 있고 독립적인 서로 다른 관찰자가 어떤 서술이 충실한 표현이라는 데 의견이 일치할 수 있음을 의미한다.",
            "③ 관찰자들이 소수점 셋째 자리까지 100% 오차 없이 완벽히 일치해야 검증되었다고 본다.",
            "④ 모든 회계 증빙 서류는 오직 국세청 전산망을 거쳐서만 직접 증명되어야 한다.",
            "⑤ 검증가능성을 확보하기 위해 경영진의 주관적 대손 판단은 모두 배제하고 대손충당금은 영(0)으로 계상한다."
        ],
        "answer": "2",
        "explanation": "② 검증가능성은 합리적인 판단력이 있고 독립적인 서로 다른 관찰자가 어떤 서술이 충실한 표현이라는 데, 비록 반드시 완전히 일치하지는 못하더라도, 의견이 일치할 수 있다는 것을 의미합니다. (또한 단일 점추정치일 필요는 없고 가능한 범위 및 관련된 확률도 검증 가능합니다.)",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "단일 점추정치일 필요가 없고 금액 범위나 확률도 검증 가능합니다.", "articles": [], "principle": "검증가능성 범위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "독립적 관찰자들이 완벽 일치는 아니더라도 의견 일치할 수 있는 성질이라는 설명은 옳습니다.", "articles": [], "principle": "검증가능성 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "완전히 일치하지는 못하더라도 의견이 도달할 수 있으면 족합니다.", "articles": [], "principle": "검증가능성 수준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "국세청 전산망 검증만을 강제하지 않습니다.", "articles": [], "principle": "검증 방법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손충당금 자의적 영 계상은 표현충실성(중립성) 위배입니다.", "articles": [], "principle": "충실한 표현", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "개념체계 상 검증가능성을 달성하는 방법인 '직접검증'과 '간접검증'의 비교로 올바른 것은?",
        "options": [
            "① 직접검증은 모형의 계산식을 검산하는 것이고, 간접검증은 실제 현금을 세어보는 것이다.",
            "② 직접검증은 현금과 같은 금액을 직접 관측하여 검증하는 것을 의미하며, 간접검증은 입력치와 모형을 재조정해 결과값을 확인하는 것이다.",
            "③ 직접검증과 간접검증은 계량할 수 없는 주관적 정보에만 제한 적용된다.",
            "④ 직접검증은 오직 자산 항목에만 쓰이고, 간접검증은 오직 자본 항목에만 유효하다.",
            "⑤ 간접검증은 감사인이 회사 내부에 투입되어 직접 장부를 눈으로 관측하는 것이다."
        ],
        "answer": "2",
        "explanation": "② 직접검증은 현금을 실제 세어보는 것처럼 금액이나 다른 서술을 직접 관측하여 검증하는 것입니다. 간접검증은 모형, 공식 또는 다른 기법의 입력치(수량, 원가 등)를 확인하고 그 결과를 동일한 모형을 적용해 재계산하여 출력을 재검증하는 것을 말합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "설명이 반대로 뒤바뀌어 틀렸습니다.", "articles": [], "principle": "검증 방식", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "직접검증은 직접 관측, 간접검증은 모형과 입력치 재계산 및 검정이라는 구분은 전적으로 옳습니다.", "articles": [], "principle": "직접 vs 간접검증", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주로 계량적 금액 정보 등에 보편 적용됩니다.", "articles": [], "principle": "검증가능성 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과목별로 배타 분할 적용되지 않습니다.", "articles": [], "principle": "검증가능성 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "간접검증은 실사 직접 관측이 아닌 산출 재계산 방식입니다.", "articles": [], "principle": "간접검증 정의", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "보강적 질적 특성 중 '이해가능성(Understandability)'을 위해 복잡한 거래 정보를 다룰 때 개념체계 상 취하는 올바른 입장은?",
        "options": [
            "① 재무제표를 더 이해하기 쉽게 만들기 위해 본질적으로 복잡한 재무정보는 전면 배제하여 누락시키는 것이 타당하다.",
            "② 복잡한 경제적 현상에 대한 정보를 재무보고서에서 제외하면 더 이해하기 쉬워질 수 있으나, 보고서 자체가 불완전하여 정보이용자를 오도할 수 있으므로 제외해서는 안 된다.",
            "③ 복잡한 정보는 오직 주석의 맨 마지막 장에 아주 작은 폰트(부록)로만 수록할 의무가 있다.",
            "④ 이용자들은 무조건 자문가 없이 단독으로 재무보고서를 100% 독해해야 할 신의성실 의무가 있다.",
            "⑤ 복잡한 외화 파생상품 거래 정보는 감사인만 확인하고 일반 주주에게는 전면 비공개로 봉인 마감한다."
        ],
        "answer": "2",
        "explanation": "② 일부 경제 현상은 본질적으로 복잡하여 이해하기 어렵습니다. 그러나 이해가능성 제고를 명분으로 재무보고서에서 복잡한 정보를 제외한다면, 그 보고서는 '불완전'해져 이용자를 오도할 우려가 큽니다. 따라서 아무리 복잡하더라도 재무보고서에 반드시 포함해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "복잡하다는 이유로 배제하면 완전성 위배입니다.", "articles": [], "principle": "완전성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "배제 시 보고서의 불완전성을 초래하고 이용자를 오도하므로 반드시 기재해야 한다는 기술은 옳습니다.", "articles": [], "principle": "이해가능성 기재 의무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "폰트 크기 강제 규정은 개념체계에 없습니다.", "articles": [], "principle": "이해가능성 오독", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "때로는 박식하고 부지런한 이용자라도 자문가의 도움을 받는 것이 타당하며 이를 권장합니다.", "articles": [], "principle": "이용자 수준과 자문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비공개 봉인은 자본 시장 공시 제도의 취지와 전면 배치됩니다.", "articles": [], "principle": "공시 원칙", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "보강적 질적 특성들이 갖는 근본적 한계에 대한 개념체계 상의 핵심 논지는?",
        "options": [
            "① 보강적 질적 특성이 극대화되면 근본적 질적 특성이 불만족스럽더라도 유용한 재무 정보가 된다.",
            "② 보강적 질적 특성은 정보가 목적적합하지 않거나 충실하게 표현되지 않는다면, 개별적으로든 집단적으로든 그 정보를 유용하게 만들 수 없다.",
            "③ 보강적 질적 특성이 단 하나라도 결여된다면 근본적 질적 특성이 만족되더라도 그 재무제표는 상법 상 전면 무효화된다.",
            "④ 보강적 질적 특성은 포괄적 제약인 원가 제약의 지배를 받지 않고 무제한 자본을 투입해 확보해야 한다.",
            "⑤ 보강적 질적 특성의 극대화 과정은 항상 엄격하게 규정된 단계별 순서(적시성 -> 이해성 등)를 강제 준수해야 한다."
        ],
        "answer": "2",
        "explanation": "② 보강적 질적 특성은 정보 유용성을 더 보강하는 역할을 할 뿐입니다. 정보가 근본적 질적 특성(목적적합성, 표현충실성)을 충족하지 못하면 보강적 특성을 아무리 많이 갖추어도 그 정보는 쓸모없습니다. 또한 보강적 질적 특성의 적용은 규정된 순서를 따르지 않는 반복적 과정입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "근본적 특성 결여 시 보강적 특성만으로는 정보 유용성을 창출하지 못합니다.", "articles": [], "principle": "보강적 질적 특성 한계", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "근본적 특성(목적적합성, 충실한 표현)이 없는 무익한 정보를 보강적 특성이 유용하게 만들 수 없다는 지문은 올바릅니다.", "articles": [], "principle": "보강적 질적 특성 한계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보강적 특성이 다소 부족하다고 해서 재무제표 전체가 상법 상 법적 무효 처리되지는 않습니다.", "articles": [], "principle": "법적 유효성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "포괄적 제약인 원가 제약의 한계 안에서 보강적 특성이 추구됩니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "어떤 규정된 순서를 따르지 않는 반복적 과정입니다.", "articles": [], "principle": "보강적 특성 적용 순서", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "개념체계 상 재무보고에 대한 '원가 제약(Cost Constraint)'의 성격을 올바르게 이해한 것은?",
        "options": [
            "① 재무제표 작성에 드는 비용은 기업 자산총액의 1% 이하로 매월 사전 통제되어야 한다.",
            "② 해당 정보 보고의 효익이 그 정보를 생산/공시하는 데 소요되는 원가를 정당화해야 한다는 원칙이다.",
            "③ 원가 제약은 오직 소규모 중소기업에만 면제 적용되고 상장 대기업에는 적용을 제외한다.",
            "④ 작성 원가가 유용성 효익보다 아무리 크더라도 주요이용자의 명령이 있다면 즉각 무제한 작성 보고해야 한다.",
            "⑤ 원가 제약으로 인해 모든 기업은 분기 재무제표 주석 기재의 90%를 의무 삭제해야 한다."
        ],
        "answer": "2",
        "explanation": "② 원가는 재무보고 정보에 대한 포괄적 제약요인입니다. 재무정보의 보고에는 필연적으로 원가가 소요되므로, 해당 정보를 보고함으로써 정보이용자들이 얻는 경제적 효익이 그 작성 및 공시 원가보다 커서 원가가 정당화되는 것이 중요합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산 1% 등 계량적 규제 조항은 개념체계에 없습니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고의 경제적 효익이 소요 원가를 정당화(효익 > 원가)해야 한다는 진술은 정확합니다.", "articles": [], "principle": "원가 제약의 본질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 제약은 규모에 관계없이 재무보고 전체에 적용되는 포괄적 제약요인입니다.", "articles": [], "principle": "원가 제약 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "효익이 원가를 하회하면 정보 제공이 제한될 수 있습니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의무 삭제 조항이 아닙니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "개념체계 상 재무 정보가 목적적합하지 않을 때 일어나는 현상으로 옳은 설명은?",
        "options": [
            "① 보강적 질적 특성인 검증가능성과 적시성이 우수하다면 그 정보는 여전히 매우 유용하다.",
            "② 표현충실성이 아무리 극대화되어 완벽하게 기재되어 있더라도, 이용자의 의사결정에 도움을 주지 못한다.",
            "③ 회계감사인으로부터 '적정의견'을 받으면 목적적합하지 않은 현상도 목적적합한 현상으로 강제 치환된다.",
            "④ 목적적합성이 없더라도 원가 제약을 만족하면 공시 의무가 법적으로 강제 개시된다.",
            "⑤ 이용자는 목적적합성 결여를 보완하기 위해 임의로 재무성과 수치를 상향 조정해야 한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 따르면, 목적적합하지 않은 현상에 대한 충실한 표현(예: 완전하고 오류 없지만 의사결정에 무용한 정보)과 목적적합한 현상에 대한 충실하지 못한 표현은 모두 정보이용자가 좋은 결정을 내리는 데 도움이 되지 않습니다. 따라서 목적적합성이 결여된 정보는 아무리 충실히 표현되어도 가치가 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "근본적 특성 결여 시 보강적 특성이 유용하게 만들 수 없습니다.", "articles": [], "principle": "질적 특성 한계", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "목적적합성이 없으면 아무리 완벽하게 표현충실해도 정보이용자에게 기여하지 못한다는 지문은 정확합니다.", "articles": [], "principle": "근본적 특성의 필요조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사의견 적정은 회계처리의 충실성을 나타낼 뿐 목적적합성 자체를 강제 창출하지 않습니다.", "articles": [], "principle": "감사의견", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유용하지 않은 정보는 원가에 무관하게 공시를 권장하지 않습니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적 수치 조향은 금지됩니다.", "articles": [], "principle": "표현충실성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "발생기준 회계(Accrual Accounting)와 현금흐름 정보가 유용한 재무정보의 질적 특성을 보강 및 충족하는 논리에 관한 설명 중 옳은 것은?",
        "options": [
            "① 발생기준 성과 정보는 단기 적시성만 제공할 뿐 예측가치는 전혀 지니지 못한다.",
            "② 발생주의 회계는 거래의 영향이 발생한 기간에 기재되므로, 현금수취 시점만을 기재하는 현금주의보다 기간 간 비교가능성과 예측가치를 일반적으로 더 우월하게 확보한다.",
            "③ 현금흐름 정보는 발생기준 정보보다 수탁책임 평가에 무조건 열등하므로 재무보고에서 완전 제외된다.",
            "④ 발생주의를 준수하기 위해 대손 등을 추정하는 행위는 표현충실성의 오류 없음 요건을 100% 영구 훼손한다.",
            "⑤ 발생주의 회계처리는 원가 제약을 적용받지 않고 어떤 비용이 들더라도 절대 준수해야 한다."
        ],
        "answer": "2",
        "explanation": "② 발생기준 회계는 거래와 사건의 영향을 발생 기간에 보여주므로, 단순히 현금 수취와 지급 시점만 보여주는 현금주의보다 정보이용자가 과거 및 미래 성과를 평가하고 예측가치를 가지며, 일관된 기준 적용에 의한 기간 간 비교가능성을 확보하기에 훨씬 유용합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "발생주의 정보는 장기적 예측가치를 풍부하게 가집니다.", "articles": [], "principle": "발생주의 예측성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사건의 발생 기간 매칭을 통해 기간 비교와 미래 예측을 더 타당하게 해 준다는 진술은 올바릅니다.", "articles": [], "principle": "발생주의 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금흐름표는 재무제표의 한 축으로서 유용하게 공시됩니다.", "articles": [], "principle": "현금흐름 정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "합리적인 절차에 기초한 추정은 오류 없음 요건을 충족할 수 있습니다.", "articles": [], "principle": "오류 없음과 추정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "발생주의 작성도 원가 제약하에 이루어집니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },

    # =========================================================================
    # L3: 적용 수준 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s04-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "재무보고 개념체계 상 '신중성(Prudence)'과 '비대칭성(Asymmetry)'의 지위에 관한 설명으로 가장 올바른 기술은?",
        "options": [
            "① 신중성을 기한다는 것은 자산과 수익의 의도적인 과소평가나 부채와 비용의 의도적인 과대평가(비대칭성 유발)를 허용하거나 내포하는 개념이다.",
            "② 신중성을 기하는 것이 비대칭(Asymmetry)의 필요성을 내포하는 것은 아니며, 그러한 비대칭은 유용한 재무정보의 질적 특성이 아니다.",
            "③ 비대칭성은 목적적합성을 높이는 핵심 보강적 질적 특성으로 개념체계에 정식 등록되어 있다.",
            "④ 신중성은 표현충실성의 오류 없는 서술 요건을 뒷받침하는 핵심 보강적 질적 특성이다.",
            "⑤ 개념체계는 특정 회계기준서에서 비대칭적인 요구사항이 도입되는 것을 절대 금지하고 이를 적발 즉시 차단한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 따르면, 신중성을 기하는 것이 비대칭의 필요성을 내포하는 것은 아니며, 비대칭은 유용한 재무정보의 질적 특성이 아닙니다. 다만, 나타내고자 하는 바를 충실하게 표현하는 가장 목적적합한 정보를 선택하려는 결정의 결과가 비대칭이라면 특정 기준서에서 비대칭적 요구를 포함할 수도 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산 과소평가나 부채 과대평가는 신중성이 허용하지 않는 왜곡입니다.", "articles": [], "principle": "신중성의 한계", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "신중성이 비대칭을 강제 내포하지 않으며, 비대칭 자체는 질적 특성이 아니라는 설명은 정확합니다.", "articles": [], "principle": "신중성과 비대칭성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비대칭성은 질적 특성이 아닙니다.", "articles": [], "principle": "비대칭성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "신중성은 중립성을 뒷받침하는 질적 속성으로 표현충실성에 기여합니다.", "articles": [], "principle": "신중성과 중립성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특정 기준서에서 목적적합성을 위해 비대칭 요구사항을 포함시킬 수 있습니다.", "articles": [], "principle": "비대칭 요구 가능", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "개념체계 상 '신중성(Prudence)'의 의미를 정확하게 해석한 기술로 옳지 않은 것은?",
        "options": [
            "① 신중성은 불확실한 상황에서 판단할 때 주의를 기울이는 것이다.",
            "② 신중성을 기한다는 것은 자산과 수익이 과대평가되지 않고 부채와 비용이 과소평가되지 않는 것을 의미한다.",
            "③ 신중성을 기한다는 것은 자산이나 수익의 과소평가나 부채나 비용의 과대평가를 전적으로 허용하지 않는다.",
            "④ 신중성에 의해 유발된 자산의 그릇된 과소평가는 미래 기간의 수익이나 비용의 과대평가나 과소평가(왜곡)로 이어질 수 있다.",
            "⑤ 불확실한 소송 비용이 있다면 신중성을 지키기 위해 실제 예상 부채의 5배를 부채로 과대계상해야 한다."
        ],
        "answer": "5",
        "explanation": "⑤ 신중성을 기한다는 것은 주의를 기울이는 것이지 부채를 의도적으로 과대계상(예: 예상의 5배 계상)하는 그릇된 평가를 정당화하는 것이 아닙니다. 자산/수익의 과소평가나 부채/비용의 과대평가 모두 허용되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "주의를 기울이는 것이 신중성의 기본 정의입니다.", "articles": [], "principle": "신중성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 과대 및 부채 과소 방지는 신중성의 올바른 의도입니다.", "articles": [], "principle": "신중성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의도적 과소평가나 과대평가도 질적 왜곡이므로 불허한다는 진술은 맞습니다.", "articles": [], "principle": "신중성 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 과소평가는 후속 연도 처분이익의 비정상적 과대계상 등으로 이어지므로 왜곡을 초래합니다.", "articles": [], "principle": "신중성과 왜곡", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "소송 부채를 5배로 고의 과대계상하는 것은 신중성의 적용 범위를 위배한 회계 오류입니다.", "articles": [], "principle": "의도적 왜곡 금지", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "보강적 질적 특성인 '비교가능성'과 '일관성(Consistency)'의 명확한 차이에 관한 기술로 옳은 것은?",
        "options": [
            "① 비교가능성과 일관성은 명칭만 다를 뿐 정의와 논리 구조가 완벽히 동일한 동의어이다.",
            "② 비교가능성은 하나의 목표이고, 일관성은 그 목표를 달성하는 데 도움을 주는 수단이다.",
            "③ 일관성이 최종 도달해야 할 장기적 목표이며, 비교가능성은 일관성을 위해 매달 수행하는 부분 수단이다.",
            "④ 일관성을 유지하기 위해 기업은 기말에 무조건 모든 자산을 전년도와 다른 기법으로 재계산해야 한다.",
            "⑤ 비교가능성을 달성하기 위해서는 일관성을 배제하고 매년 다른 회계 기법을 무작위 적용해야 한다."
        ],
        "answer": "2",
        "explanation": "② 일관성은 한 보고기업 내에서 기간 간 또는 같은 기간 동안에 기업 간, 동일한 항목에 대해 동일한 방법을 적용하는 것을 의미하며, 비교가능성(이용자가 항목 간의 유사점과 차이점을 식별하고 이해할 수 있게 하는 특성)은 이를 통해 달성하고자 하는 목표이고, 일관성은 이를 달성하기 위한 수단입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "동일한 명칭이나 동의어가 아닌 상보적 관계입니다.", "articles": [], "principle": "비교가능성과 일관성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비교가능성은 최종 목표이고, 일관성은 그 목표를 위한 방법론적 수단이라는 지문은 정확합니다.", "articles": [], "principle": "비교가능성과 일관성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "목표와 수단이 거꾸로 기술되어 틀렸습니다.", "articles": [], "principle": "비교가능성과 일관성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일관성은 동일한 방법을 계속 적용하는 것입니다.", "articles": [], "principle": "일관성 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무작위 적용 시 일관성 훼손으로 비교가능성이 하락합니다.", "articles": [], "principle": "비교가능성 저해", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "개념체계 상 '비교가능성(Comparability)'과 '통일성(Uniformity)'의 관계에 대한 설명 중 옳은 것은?",
        "options": [
            "① 비교가능성은 모든 기업의 회계처리를 100% 기계적으로 박아 넣는 통일성과 일치한다.",
            "② 비교가능성은 통일성이 아니다. 정보가 비교가능하기 위해서는 비슷한 것은 비슷하게 보여야 하고 다른 것은 다르게 보여야 한다.",
            "③ 비슷한 것을 달리 보이게 하거나, 비슷하지 않은 것을 비슷하게 보이게 함으로써 비교가능성이 보강된다.",
            "④ 통일성을 높이기 위해 기준서 위원회는 모든 자산의 측정 기준을 원가주의로 단일 통합 규제해야 한다.",
            "⑤ 다른 거래 현상을 동일한 기법으로 일관되게 표시하여 유사하게 보이게 만드는 것이 비교가능성의 본질이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 비교가능성이 '통일성'이 아니라고 명확히 밝힙니다. 정보가 비교가능하기 위해서는 비슷한 사건은 비슷하게 보이고, 다른 성격의 사건은 다르게 표현되어야 합니다. 비슷하지 않은 것을 비슷하게 처리하면 비교가능성이 오히려 훼손됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "통일성과 일치하지 않습니다.", "articles": [], "principle": "비교가능성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비교가능성은 통일성이 아니며, 비슷한 것은 비슷하게 다른 것은 다르게 해야 한다는 설명은 완전무결합니다.", "articles": [], "principle": "비교가능성 vs 통일성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비슷하지 않은 것을 비슷하게 보이면 비교가능성이 감축/훼손됩니다.", "articles": [], "principle": "비교가능성 저해", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정의 단일 통합 규제는 타당하지 않습니다.", "articles": [], "principle": "측정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "다른 거래를 동일 기법으로 위장하는 것은 비교가능성 파괴입니다.", "articles": [], "principle": "비교가능성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "재무제표 작성 시 '대체적인 회계처리방법의 허용(Alternative Accounting Treatments)'이 비교가능성에 미치는 영향으로 가장 타당한 설명은?",
        "options": [
            "① 다양한 대체적 방법을 적용하므로 기간 간 비교가능성이 영구 상향 조정된다.",
            "② 동일한 경제적 현상에 대해 대체적인 회계처리방법을 허용하면 비교가능성이 감소한다.",
            "③ 대체적 방법의 존재 유무는 비교가능성 증감에 아무런 영향을 미치지 않는다.",
            "④ 대체법을 허용해야만 비로소 일관성(Consistency)이 극대화된다.",
            "⑤ 회계기준위원회는 비교가능성을 최고치로 높이기 위해 대체적 회계처리방법을 무제한 허용하는 방침을 쓴다."
        ],
        "answer": "2",
        "explanation": "② 동일한 경제적 현상에 대해 여러 가지 대체적인 회계처리방법을 허용하면, 기업마다 다른 방법을 선택할 수 있어 기업 간 또는 기간 간의 비교가능성이 유의적으로 감소합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "대체적 방법 허용 시 기업별 선택이 달라져 비교가능성이 파괴/하락합니다.", "articles": [], "principle": "비교가능성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "대체적인 회계처리를 허용하면 정보 비교가능성이 감축한다는 설명은 옳습니다.", "articles": [], "principle": "대체방법과 비교가능성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매우 직접적인 악영향을 미칩니다.", "articles": [], "principle": "비교가능성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "방법이 수시로 바뀌면 일관성이 도리어 저해됩니다.", "articles": [], "principle": "일관성 저해", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "위원회는 비교가능성 제고를 위해 불필요한 대체적 기법을 배제하려 노력합니다.", "articles": [], "principle": "기준제정 목적", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "회계감사 상황에서 '직접검증'과 '간접검증'의 실제 사례가 올바르게 짝지어진 것은?",
        "options": [
            "① 직접검증 - 재고수량을 실사하여 물리적 존재 확인 / 간접검증 - 원가 가정을 검토하여 동일 모형으로 장부상 재고금액 재산출",
            "② 직접검증 - 미래 예상 매출을 모형에 대입 / 간접검증 - 금고 내 보유 달러 화폐 액수를 손으로 직접 카운팅",
            "③ 직접검증 - 법인세 비용을 역추적 모형으로 계산 / 간접검증 - 은행 예금 잔액 증명서를 직접 눈으로 확인",
            "④ 직접검증 - 경쟁사의 분기 자산 총액 분석 / 간접검증 - 기업 빌딩의 대지 면적 측정 자료를 감사조서에 수록",
            "⑤ 직접검증 - 기말 대손율을 공식으로 재계산 / 간접검증 - 당기 발생한 외상 거래 총액의 실사"
        ],
        "answer": "1",
        "explanation": "① 직접검증은 금액이나 다른 서술을 직접 확인하는 것입니다(예: 재고실사로 수량 세기, 금고의 실제 현금 잔액 확인). 간접검증은 모형의 입력치를 확인하고 그 결과값을 동일한 방법(예: 선입선출법 재계산 등)을 적용해 도출 과정을 역검증하는 것입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "재고실사(직접관측)와 재고단가 결정 모형 재계산(간접)으로 짝지은 지문은 완벽하게 합당합니다.", "articles": [], "principle": "직접 vs 간접검증 사례", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "직접과 간접 사례의 성격이 거꾸로 되어 틀렸습니다.", "articles": [], "principle": "검증 방식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잔액증명서 확인은 직접검증에 가까우며 모형 역추적은 간접에 해당하므로 뒤섞여 틀렸습니다.", "articles": [], "principle": "검증 방식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경쟁사 총액 분석이나 대지면적 자체는 검증 기법 매칭이 아닙니다.", "articles": [], "principle": "검증 방식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공식 재계산은 간접검증에 속하므로 매칭 오류입니다.", "articles": [], "principle": "검증 방식", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "개념체계 상 재무보고서가 상정하고 있는 '정보이용자의 기본적 역량 및 태도'에 대한 공식 지침은?",
        "options": [
            "① 회계학적 지식이 전무하여 복잡한 재무제표를 읽을 수 없는 미성년 대중",
            "② 사업활동과 경제활동에 대해 합리적인 지식이 있고, 부지런히 정보를 검토하고 분석하는 이용자",
            "③ 재무제표의 모든 기재 숫자를 오직 인공지능(AI) 프로그램을 활용하여 기계적으로 자동 필터링하는 전산 프로그램",
            "④ 보고서에 자문가의 조력을 받는 것을 전면 금지하는 초전문가 주주",
            "⑤ 회사의 장부 기재 오류가 발생하면 즉각 고소 고발하는 사법 사정관"
        ],
        "answer": "2",
        "explanation": "② 개념체계는 재무보고서가 '사업활동과 경제활동에 대해 합리적인 지식이 있고, 부지런히 정보를 검토하고 분석하는 이용자'를 위해 작성된다고 명시하고 있습니다. 또한 때로는 복잡한 사항에 대해 자문가의 조력을 받을 수 있다고 봅니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지식이 완전히 결여된 이용자를 기준으로 설계되지 않았습니다.", "articles": [], "principle": "이용자 상정 지위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "합리적인 지식과 정보를 부지런히 분석하는 독자를 전제한다는 기술은 정확한 문장입니다.", "articles": [], "principle": "이용자 상정 지위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "AI 자동 프로그램 전용으로 디자인된 것이 아닙니다.", "articles": [], "principle": "이용자 상정 지위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이용자들이 자문가의 조력을 구하는 것을 당연히 허용하며, 필요성을 밝히고 있습니다.", "articles": [], "principle": "자문가 조력권", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사법 사정관 전용 문서가 아닙니다.", "articles": [], "principle": "이용자 상정 지위", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "개념체계 상 근본적 질적 특성인 목적적합성과 표현충실성을 효율적이고 효과적으로 '적용하는 일련의 순서 및 단계'로 올바른 설명은?",
        "options": [
            "① 첫째로 재무제표의 모든 숫자를 검증하고, 둘째로 의사결정에 차이를 내게 만든 뒤, 셋째로 중요성을 획일화한다.",
            "② 첫째로 유용할 수 있는 정보의 대상이 되는 경제적 현상을 식별하고, 둘째로 가장 목적적합한 정보 유형을 식별하며, 셋째로 그 정보가 이용가능하고 충실하게 표현할 수 있는지 결정한다.",
            "③ 첫째로 원가를 차감하고, 둘째로 감사 의견을 구하며, 셋째로 보고서를 임의 축소 공시한다.",
            "④ 첫째로 보강적 질적 특성(적시성)을 우선 확보하고, 둘째로 근본적 특성을 단계적으로 조율한다.",
            "⑤ 순서에 관계없이 일단 보고서를 공시한 뒤, 문제가 발생하면 그 경제적 현상을 역추적하여 락을 건다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 근본적 질적 특성의 효율적 적용 절차로 다음의 3단계를 제시합니다. 1) 경제적 현상 식별 -> 2) 가장 목적적합한 정보 유형 식별 -> 3) 충실히 표현할 수 있는지 결정. 이 절차가 만족되면 그 시점에 끝나며, 불만족 시 차선의 목적적합한 정보에 대해 이 절차를 반복합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "검증이나 중요성 획일화는 적용 순서 3단계가 아닙니다.", "articles": [], "principle": "적용 절차", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "경제현상 식별 -> 목적적합 정보 식별 -> 표현 가능 여부 결정이라는 3단계 설명은 완벽합니다.", "articles": [], "principle": "근본적 특성 적용 순서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 제약이나 감사 의견은 적용 절차의 본질 순서가 아닙니다.", "articles": [], "principle": "적용 절차", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "근본적 질적 특성을 만족하기 전에는 보강적 특성이 정보를 유용하게 할 수 없으므로 근본적 특성부터 적용해야 합니다.", "articles": [], "principle": "보강적 질적 특성 한계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역추적 락킹 절차가 아닙니다.", "articles": [], "principle": "적용 절차", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "보강적 질적 특성의 적용 프로세스에 대한 설명 중 개념체계에 가장 부합하는 지문은?",
        "options": [
            "① 보강적 질적 특성은 무조건 비교가능성을 1위로 고정하고 적시성을 4위로 고정하는 하향식 고정 순서로 적용된다.",
            "② 보강적 질적 특성을 적용하는 것은 어떤 규정된 순서를 따르지 않는 반복적인 과정이며, 때로는 다른 특성의 극대화를 위해 하나의 보강적 질적 특성이 감소되어야 할 수도 있다.",
            "③ 하나의 보강적 질적 특성이 감소하는 것은 회계기준 위반에 따른 임원 해임 사유가 성립한다.",
            "④ 보강적 특성은 항상 근본적 질적 특성 적용 전에 완료하여, 근본적 특성을 배제하는 방향으로 쓰인다.",
            "⑤ 이해가능성 확보를 위해 적시성을 영구 0으로 수렴시켜 공시를 중단할 수도 있다."
        ],
        "answer": "2",
        "explanation": "② 보강적 질적 특성의 적용은 정해진 기계적 순서를 따르지 않는 반복적인 과정입니다. 또한 때에 따라서는 하나의 보강적 질적 특성을 극대화하기 위해(예: 검증성 극대화) 다른 특성(예: 적시성)을 다소 희생해야 하는 상충(Trade-off) 절충이 수반됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "고정된 순서가 존재하지 않습니다.", "articles": [], "principle": "보강적 특성 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "규정 순서 없는 반복 과정이며, 특정 보강특성 극대화를 위해 타 특성이 감소할 수 있다는 설명은 정확합니다.", "articles": [], "principle": "보강적 특성 간 상충", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상충에 따른 자연스러운 절충 결과이므로 위법 제재 대상이 아닙니다.", "articles": [], "principle": "보강적 특성 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "근본적 특성 적용이 보강적 특성보다 우선합니다.", "articles": [], "principle": "근본적 특성 우선", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적시성 영구 0 수렴으로 인한 공시 중단은 중대한 오류입니다.", "articles": [], "principle": "적시성 저해", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "재무제표 작성 시 '측정불확실성(Measurement Uncertainty)'이 중대하게 작용하는 항목에 대하여 표현충실성을 충족시키기 위해 기업이 수행해야 할 올바른 공시 지침은?",
        "options": [
            "① 불확실한 금액은 무조건 기재하지 않고 전액 누락 처리한다.",
            "② 해당 금액이 추정치임을 명확하고 정확하게 기술하고, 그 추정 절차의 성격과 한계를 상세히 설명하며, 적절한 절차를 선택하여 선택 및 적용하는 데 오류가 없어야 한다.",
            "③ 회계담당자는 주가가 폭락하는 리스크를 막기 위해 임의로 고정 낙관치를 기재한다.",
            "④ 불확실성이 큰 부채는 '자산' 계정으로 허위 위장하여 계상한다.",
            "⑤ 감사를 피하기 위해 추정치에 관련된 모든 보조 계산서 파일을 전면 파기 마감한다."
        ],
        "answer": "2",
        "explanation": "② 측정불확실성이 높은 경우에도 그 추정이 합리적으로 수행되었다면 유용한 정보가 될 수 있습니다. 단, 표현충실성을 만족시키려면 추정치로서의 금액을 명확하고 정확하게 설명하고, 추정 절차의 성격 및 한계를 공시하고, 도출 절차에 오류가 없었음을 입증해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "누락 처리는 완전성 위배입니다.", "articles": [], "principle": "완전성 위배", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "추정치 명시, 한계 및 절차 설명, 오류 없는 적용이 표현충실성 확보 요건이라는 설명은 정확합니다.", "articles": [], "principle": "측정불확실성 대처", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 낙관치는 중립성(편의 없음)에 전면 위배됩니다.", "articles": [], "principle": "중립성 위배", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "허위 위장은 중대한 분식회계 죄가 됩니다.", "articles": [], "principle": "분식회계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "증빙 파기는 형사 처벌 대상입니다.", "articles": [], "principle": "증빙 파기", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "개념체계 상 '중요성(Materiality)'을 평가할 때 기준이 되는 요소를 가장 타당하게 지적한 기술은?",
        "options": [
            "① 오직 해당 항목의 절대적인 금액 크기(규모)에 의해서만 수학적으로 판단된다.",
            "② 오직 해당 거래의 사법적 불법성 여부(성격)에 의해서만 법률적으로 판단된다.",
            "③ 항목의 성격이나 규모 또는 이 둘 모두에 근거하여 개별 보고기업 특유의 측면에서 판단된다.",
            "④ 국세청 세무조사관의 사적 의견 크기에 따라 가변적으로 결정된다.",
            "⑤ 회사의 장부 자산총액의 50%를 초과하는 항목에 한해 무조건 기계적으로 적용된다."
        ],
        "answer": "3",
        "explanation": "③ 중요성은 통일된 획일적인 규칙이 아니라 개별 기업 재무보고서 관점에서 해당 정보와 관련된 '항목의 성격이나 규모, 또는 이 둘 모두'에 근거하여 판단하는 기업 특유의 속성입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "금액이 작아도 성격 상 중요한 경우(예: 경영진 횡령이나 특수관계자 거래 등)가 있으므로 규모 단독이 아닙니다.", "articles": [], "principle": "중요성의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법적 불법성 성격 단독으로만 제한되지 않습니다.", "articles": [], "principle": "중요성의 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "성격, 규모, 혹은 이 둘 모두에 근거해 개별적으로 판단된다는 진술은 완벽한 개념체계 문장입니다.", "articles": [], "principle": "중요성 평가 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무조사관 개인 의견에 좌우되지 않습니다.", "articles": [], "principle": "중요성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 50% 초과 한계는 비합리적으로 크며 계량 규칙도 부재합니다.", "articles": [], "principle": "중요성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "재무보고서가 과거에 가졌던 '확인가치(Confirmatory Value)'가 실제로 정보이용자에게 피드백(Feedback)을 작동시키는 실무적 사례는?",
        "options": [
            "① 당기순이익이 흑자로 나자 회계담당자가 보너스를 수령하고 감사를 생략하는 상황",
            "② 투자자 B가 과거에 예상했던 금년도 P사의 영업이익 추정치와, 실제 공시된 P사의 금년도 영업이익 실제치를 상호 비교하여 기존 자신의 평가/예측 모형을 수정 및 변경하는 상황",
            "③ 주가가 하락하자 투자자가 주총 이사진을 전원 구속 고소하는 상황",
            "④ 회사가 장부를 폐기하고 사적 대화로만 기말 성과를 전달하는 상황",
            "⑤ 회계사가 기말 자산을 전년도와 다른 기법으로 무단 소급 변경하여 감추는 상황"
        ],
        "answer": "2",
        "explanation": "② 확인가치는 과거 평가에 대한 피드백을 제공(과거 평가를 확인하거나 변경)함으로써 발휘됩니다. 투자자가 기존 추정치와 실제 공시치를 비교 분석해 피드백을 얻어 기존 평가 모형을 변경하는 것이 가장 전형적인 확인가치 적용 사례입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "보너스 수령 및 감사 생략은 적법한 피드백이 아닌 규정 위반 행위입니다.", "articles": [], "principle": "내부 통제 위배", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "예측과 실제를 비교해 과거 평가를 확인/수정하는 것은 확인가치 및 피드백의 실무 사례로 정확합니다.", "articles": [], "principle": "확인가치 적용 사례", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이사진 구속 소송은 확인가치 기능과 무관합니다.", "articles": [], "principle": "사법 소송", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "장부 폐기는 불법 범죄 행위입니다.", "articles": [], "principle": "장부 보존 의무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무단 변경 및 은폐는 중립성 및 일관성 위배입니다.", "articles": [], "principle": "질적 특성 위배", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "유용한 재무보고에 대한 '원가 제약'을 평가할 때, 개념체계가 인정하는 정보 제공의 효익(Benefits)에 관한 올바른 설명은?",
        "options": [
            "① 효익은 오직 재무제표를 제공하는 개별 보고기업이 취득하는 직접적 사적 현금 유입만을 뜻한다.",
            "② 정보 제공에 따른 효익은 보통 다수의 정보이용자(자본 시장 전체)에게 광범위하게 배분되므로, 효익을 원가와 기계적으로 일대일로 비교 계량하는 것은 어렵고 한계가 있다.",
            "③ 정보의 효익은 감사인이 수취하는 연간 감사 보수 수수료 총액으로만 강제 계산해야 한다.",
            "④ 효익은 항상 작성 원가보다 무조건 적을 수밖에 없으므로 원가 제약 조항은 영구 폐지되어야 한다.",
            "⑤ 효익을 높이기 위해 기업은 주주들에게 재무제표의 모든 라인을 건당 유료로 과금 발송해야 한다."
        ],
        "answer": "2",
        "explanation": "② 재무정보 제공의 효익은 정보를 생산하는 기업이 직접 사적으로 모두 회수하기보다, 투자자의 합리적 의사결정에 따른 시장의 자원 배분 효율성 증대 등 공공재적 성격으로 다수 참여자에게 분산 배분됩니다. 따라서 효익을 개별 원가와 단순 일대일 계량적 비교하는 데는 어려움이 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "효익은 사적 유입에만 그치지 않고 시장 전체의 자원 배분 효율화 등 공익을 포괄합니다.", "articles": [], "principle": "원가 제약의 효익", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "효익이 다수에게 광범위 분산되어 단순 원가 대비 계량 비교가 어렵다는 진술은 정확합니다.", "articles": [], "principle": "원가 제약과 효익 평가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사 수수료가 정보의 사회적 효익이 될 수 없습니다.", "articles": [], "principle": "감사 보수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "효익이 원가를 능가하는 정보가 많으므로 제약 조항은 유효합니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재무제표의 유료 유료 과금 발송은 공시 제도의 기본 원칙에 어긋납니다.", "articles": [], "principle": "공시 공평성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "법적 형식(Legal Form)과 경제적 실질(Economic Substance)이 불일치할 때, '표현충실성'에 따라 처리되는 실무적 사건의 예시로 가장 적절한 것은?",
        "options": [
            "① 리스이용자가 리스자산의 법적 소유권이 없다는 이유로 임차료 지불 시 비용으로만 전액 처리하고 리스자산과 부채를 인식하지 않는 경우",
            "② 금융리스 거래에서 리스이용자가 형식상 법적 소유권은 없으나, 자산 사용에 따른 위험과 효익의 실질이 이전되었으므로 장부상 사용권자산과 리스부채로 계상하여 처리하는 경우",
            "③ 주주와의 자본 거래를 당기 영업 수익으로 임의 가장하여 당기순이익에 반영하는 경우",
            "④ 특수관계자에게 무상으로 토지를 이전하고 장부 상에는 일반 정상 매각으로 위장 기록하는 경우",
            "⑤ 회사의 장기 대여금을 단순 비용 누락 처리하고 현금 입금 시점에만 잡수익으로 잡는 경우"
        ],
        "answer": "2",
        "explanation": "② 형식과 실질이 다른 경우, 형식(법적 소유권 없음)에만 의존해 기재하면 실질을 충실히 표현하지 못합니다. 금융리스 계약처럼 형식상 소유권은 없으나 사용 통제 실질이 이전되었으므로 장부에 자산과 부채(사용권자산, 리스부채)로 인식하는 것이 표현충실성(실질의 반영)을 준수한 대표적 사례입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "법적 형식에만 매몰되어 실질을 왜곡하는 잘못된 회계처리입니다.", "articles": [], "principle": "표현충실성 위배", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "소유권은 없으나 실질 통제권을 반영해 자산/부채를 잡는 금융리스 회계는 표현충실성의 타당한 사례입니다.", "articles": [], "principle": "실질의 우선 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본거래를 영업수익으로 위장하는 것은 고의적 왜곡(중립성/완전성 위배)입니다.", "articles": [], "principle": "분식 회계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무상 이전을 매각 위장 기재하는 것은 명백한 거짓 기록입니다.", "articles": [], "principle": "거짓 표현", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "발생주의 및 완전성에 위배되는 누락 회계입니다.", "articles": [], "principle": "누락 회계", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "개념체계 상 재무 정보의 '이해가능성'을 적용할 때, 이용자가 자문가(Adviser)의 도움을 받는 것에 관한 올바른 가이드라인은?",
        "options": [
            "① 개념체계는 자문가 등 대리인의 개입을 불법 대리 공시 행위로 보아 규율한다.",
            "② 이용자들은 모든 수치를 스스로 독파해야 하므로 자문비를 지불하는 것은 원가 제약에 따라 이사회에서 금지된다.",
            "③ 때로는 박식하고 부지런한 이용자들도 복잡한 경제적 현상에 대한 정보를 이해하기 위해 자문가의 도움을 받는 것이 필요할 수 있다.",
            "④ 자문가를 사용하는 즉시 해당 재무제표는 제3자 정보 유출 혐의로 소송 기소된다.",
            "⑤ 자문가는 반드시 회계기준위원회 위원장만의 허가를 득한 국책 회계사로만 한정된다."
        ],
        "answer": "3",
        "explanation": "③ 이해가능성은 부지런한 독자를 상정하지만, 복잡한 거래의 경우 이들도 자문가의 도움을 받아 정보를 해석하는 것이 필요함을 개념체계는 명문으로 허용 및 명시하고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "불법 행위로 규율하지 않습니다.", "articles": [], "principle": "이해가능성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 제약은 보고서 작성 기업의 통제이지 이용자 사적 자문비 제한이 아닙니다.", "articles": [], "principle": "원가 제약", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부지런한 이용자도 필요시 자문가의 조력을 구하는 것이 적법하고 유용하다는 기술은 정확합니다.", "articles": [], "principle": "자문가 활용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기소나 유출 혐의 사유가 성립하지 않습니다.", "articles": [], "principle": "이해가능성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자문가 승인 한정 절차는 없습니다.", "articles": [], "principle": "이해가능성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },

    # =========================================================================
    # L4: 분석 수준 (8문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s04-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "다음 유용한 재무정보의 '근본적 질적 특성'에 관한 설명 중 옳은 지문의 개수는?\n\n```\nㄱ. 목적적합한 재무정보는 정보이용자의 의사결정에 차이가 나도록 할 수 있다.\nㄴ. 중요성은 개별 기업 재무보고서 관점에서 항목의 성격이나 규모 또는 이 둘 모두에 근거하여 판단하는 개별 기업 특유의 목적적합성이다.\nㄷ. 중립적 서술은 재무정보의 선택이나 표시에 편의가 없는 것이며, 목적이 없거나 행동에 영향을 미치지 않는 정보를 의미한다.\nㄹ. 오류가 없다는 것은 현상의 기술에 누락이나 오류가 없고 절차 상의 오류가 없음을 뜻하며, 모든 면에서 완벽하게 정확하다는 것을 포함한다.\n```",
        "options": [
            "① 1개",
            "② 2개",
            "③ 3개",
            "④ 4개",
            "⑤ 없음"
        ],
        "answer": "2",
        "explanation": "② 옳은 지문은 ㄱ, ㄴ 2개입니다.\n\n[오답 판단]\nㄷ. 중립적 정보는 목적이 없거나 행동에 영향력이 없는 정보를 의미하는 것이 아닙니다. (의사결정에 영향을 줍니다.)\nㄹ. 오류가 없다는 것은 모든 면에서 완벽하게 정확하다는 것을 의미하는 것은 아닙니다. (추정치 절차의 정당성을 포함합니다.)",
        "question_type": "박스형",
        "option_meta": [
            {"correct": False, "why": "1개가 아닙니다. 옳은 것은 ㄱ, ㄴ입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ, ㄴ 지문은 정확하고 ㄷ, ㄹ은 오독 문장이므로 총 2개가 정답입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "3개가 아닙니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "4개가 아닙니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "0개가 아닙니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "다음 보강적 질적 특성에 관한 기술 중 옳지 않은 것만을 모두 고른 것은?\n\n```\nㄱ. 보강적 질적 특성은 정보가 목적적합하지 않거나 충실하게 표현되지 않으면 그 정보를 개별적으로든 집단적으로든 유용하게 만들 수 없다.\nㄴ. 일관성은 비교가능성과 직접 관련된 목표이고, 비교가능성은 그 목표를 달성하는 데 도움을 주는 수단이다.\nㄷ. 계량화된 정보가 검증가능하기 위해서 단일 점추정치이어야 할 필요는 없으며 가능한 범위 및 확률도 검증될 수 있다.\nㄹ. 보강적 질적 특성을 적용하는 것은 정해진 순서를 따르는 순차적 반복이다.\n```",
        "options": [
            "① ㄱ, ㄷ",
            "② ㄴ, ㄹ",
            "③ ㄱ, ㄹ",
            "④ ㄴ, ㄷ",
            "⑤ ㄷ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 옳지 않은 것은 ㄴ, ㄹ입니다.\n\n[오답 판단]\nㄴ. 비교가능성이 목표이고, 일관성은 수단입니다. (목표와 수단이 반대로 기술됨)\nㄹ. 보강적 질적 특성을 적용하는 것은 '어떤 규정된 순서를 따르지 않는' 반복적인 과정입니다. (순차적 적용이 아님)\n\n[정답 분석]\nㄱ, ㄷ은 모두 개념체계에 부합하는 올바른 기술입니다.",
        "question_type": "박스형",
        "option_meta": [
            {"correct": False, "why": "ㄱ, ㄷ은 올바른 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄴ, ㄹ 지문은 오류 지문이므로 옳지 않은 조합으로 정답입니다.", "articles": [], "principle": "오류 조합 선택", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ은 옳은 지문입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 옳은 지문입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 옳은 지문입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "다음 신중성과 중립성에 관한 네 가지 지문 중 각각의 참(T)/거짓(F) 여부를 올바르게 표시한 것은?\n\n```\n(1) 중립성은 신중성을 기함으로써 뒷받침된다.\n(2) 신중성은 불확실한 상황에서 판단할 때 자산과 수익의 과소평가를 장려한다.\n(3) 신중성을 기한다는 것은 자산과 수익이 과대평가되지 않고 부채와 비용이 과소평가되지 않는 주의를 의미한다.\n(4) 특정 기준서에서 비대칭적인 요구사항을 절대 포함할 수 없다.\n```",
        "options": [
            "① (1): T, (2): T, (3): F, (4): F",
            "^^② (1): T, (2): F, (3): T, (4): F^^",
            "③ (1): F, (2): T, (3): T, (4): T",
            "④ (1): F, (2): F, (3): T, (4): F",
            "⑤ (1): T, (2): T, (3): T, (4): T"
        ],
        "answer": "2",
        "explanation": "② 각 지문의 참/거짓 판단은 다음과 같습니다.\n(1) T: 중립성은 신중성에 의해 지지/뒷받침됩니다.\n(2) F: 신중성은 자산/수익의 과소평가를 허용/장려하지 않습니다.\n(3) T: 자산 과대 및 부채 과소 방지 주의가 신중성의 정확한 지침입니다.\n(4) F: 특정 기준서에서 비대칭 요구사항을 포함할 수도 있습니다.",
        "question_type": "박스형",
        "option_meta": [
            {"correct": False, "why": "(2)와 (3)의 정오 판단이 잘못되었습니다.", "articles": [], "principle": "정오 조합", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "(1) 참, (2) 거짓, (3) 참, (4) 거짓 조합은 개념체계 조항에 완벽히 상응합니다.", "articles": [], "principle": "정오 조합 정답", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "(1), (4) 등의 판단이 틀렸습니다.", "articles": [], "principle": "정오 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "(1)번 판단이 틀렸습니다.", "articles": [], "principle": "정오 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "모두 참이 아닙니다.", "articles": [], "principle": "정오 조합", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "다음 중요성(Materiality)에 관한 기술 중 옳은 것의 조합을 고른 것은?\n\n```\nㄱ. 중요성은 개별 기업 특유의 측면이므로 회계기준위원회는 획일적인 계량 임계치를 정해둘 수 없다.\nㄴ. 정보가 누락되었더라도 이용자의 의사결정에 차이를 유발하지 않았다면 그 정보는 중요한 것이다.\nㄷ. 중요성 판단은 정보이용자의 특수한 개별 수요가 아닌 다수 이용자의 공통된 정보 수요의 중요성에 집중한다.\nㄹ. 항목의 성격이나 규모 또는 이 둘 모두에 근거하여 중요성을 판단한다.\n```",
        "options": [
            "① ㄱ, ㄴ, ㄷ",
            "② ㄱ, ㄷ, ㄹ",
            "③ ㄴ, ㄷ, ㄹ",
            "④ ㄱ, ㄴ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 옳은 설명은 ㄱ, ㄷ, ㄹ입니다.\n\n[오답 분석]\nㄴ. 정보가 누락/왜곡되었을 때 의사결정에 영향을 주어야만 중요성이 인정됩니다. 영향을 주지 않았다면 중요하지 않은 정보입니다.",
        "question_type": "박스형",
        "option_meta": [
            {"correct": False, "why": "ㄴ은 틀린 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ, ㄷ, ㄹ 지문은 모두 올바른 설명의 조합입니다.", "articles": [], "principle": "올바른 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ은 틀린 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ은 틀린 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ이 포함되어 오답입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "다음 중 '예측가치'와 '확인가치'의 실제 작동에 대한 문장 중 옳은 것만을 모두 연결한 것은?\n\n```\nㄱ. 재무정보가 예측가치를 갖기 위해 그 자체가 예측치나 예상치일 필요는 없다.\nㄴ. 과거 평가에 대한 피드백을 제공(확인하거나 변경)한다면 확인가치를 갖는다.\nㄷ. 예측가치를 갖는 정보는 확인가치도 갖는 경우가 많다.\nㄹ. 예측가치와 확인가치는 배타적이어서 하나의 재무제표 안에서 공존하는 것이 감점 요인이다.\n```",
        "options": [
            "① ㄱ, ㄴ, ㄷ",
            "② ㄴ, ㄷ, ㄹ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄱ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "1",
        "explanation": "① 옳은 설명은 ㄱ, ㄴ, ㄷ입니다.\n\n[오답 분석]\nㄹ. 두 가치는 상호 긴밀히 연관되어 있으며 공존하고 보완하는 상태가 유익합니다. 배타적이지 않습니다.",
        "question_type": "박스형",
        "option_meta": [
            {"correct": True, "why": "ㄱ, ㄴ, ㄷ 지문은 모두 개념체계에 합치하는 올바른 설명입니다.", "articles": [], "principle": "올바른 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 틀린 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 틀린 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 틀린 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ이 포함되어 오답입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "보강적 질적 특성(검증가능성, 적시성, 이해가능성)에 관한 다음 서술 중 옳지 않은 지문의 개수는?\n\n```\nㄱ. 검증가능성은 독립적인 서로 다른 관찰자가 어떤 서술이 충실한 표현이라는 데 반드시 완전히 일치해야 함을 의미한다.\nㄴ. 적시성이란 의사결정에 영향을 미칠 수 있도록 제때에 이용가능하게 함을 뜻하며, 정보는 오래될수록 유용성이 무조건 100% 즉시 영(0)이 된다.\nㄷ. 이해가능성을 보장하기 위해 본질적으로 복잡한 재무 정보는 정보이용자를 오도할 수 있으므로 절대 제외해서는 안 된다.\nㄹ. 보강적 질적 특성은 정보가 목적적합하지 않다면 그 자체만으로 정보를 유용하게 할 수 없다.\n```",
        "options": [
            "① 1개",
            "② 2개",
            "③ 3개",
            "④ 4개",
            "⑤ 없음"
        ],
        "answer": "2",
        "explanation": "② 옳지 않은 것은 ㄱ, ㄴ 2개입니다.\n\n[오답 분석]\nㄱ. 반드시 완전히 일치하지는 못하더라도 의견이 일치할 수 있음을 의미합니다.\nㄴ. 일반적으로 오래될수록 유용성이 낮아지지만, 일부 정보는 보고기간 후에도 오랫동안 적시성이 있을 수 있으며 즉각 0이 되지는 않습니다.\n\n[정답 분석]\nㄷ, ㄹ은 올바른 지문입니다.",
        "question_type": "박스형",
        "option_meta": [
            {"correct": False, "why": "1개가 아닙니다. 옳지 않은 지문은 ㄱ, ㄴ 2개입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ, ㄴ 지문은 명백한 왜곡 서술이므로 옳지 않은 것의 개수는 2개가 정답입니다.", "articles": [], "principle": "오류 개수 선택", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "3개가 아닙니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "4개가 아닙니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "0개가 아닙니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "다음 '충실한 표현(Faithful Representation)'과 '측정불확실성'에 관한 기술 중 옳은 것의 조합을 고른 것은?\n\n```\nㄱ. 경제 현상의 실질과 법적 형식이 같지 않다면, 법적 형식에 따른 정보만 제공하여서는 경제적 현상을 충실히 표현할 수 없다.\nㄴ. 화폐금액을 직접 관측할 수 없어 추정하는 것은 재무 정보 유용성을 언제나 심각하게 저해한다.\nㄷ. 측정불확실성이 높더라도 합리적으로 추정하고 성격과 한계를 설명하면 충실한 표현이 될 수 있다.\nㄹ. 완벽한 표현충실성을 만족시키기는 어려우며, 위원회 목적은 완전성, 중립성, 오류 없음을 극대화하는 것이다.\n```",
        "options": [
            "① ㄱ, ㄴ, ㄷ",
            "② ㄴ, ㄷ, ㄹ",
            "③ ㄱ, ㄷ, ㄹ",
            "④ ㄱ, ㄴ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ 옳은 설명은 ㄱ, ㄷ, ㄹ입니다.\n\n[오답 분석]\nㄴ. 합리적인 추정치의 사용은 필수적이며, 추정이 명확하고 정확하게 기술되고 설명되는 한 측정불확실성이 높더라도 정보 유용성을 저해하지 않습니다.",
        "question_type": "박스형",
        "option_meta": [
            {"correct": False, "why": "ㄴ은 틀린 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ은 틀린 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ, ㄷ, ㄹ 지문은 모두 충실한 표현에 관한 타당한 설명입니다.", "articles": [], "principle": "올바른 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ은 틀린 설명입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ이 포함되어 오답입니다.", "articles": [], "principle": "박스형 판단", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "다음 '원가 제약' 및 '질적 특성 적용범위'에 관한 네 가지 지문 중 각각의 T/F 여부를 올바르게 표시한 것은?\n\n```\n(1) 원가 제약은 재무보고 제공 정보에 대한 포괄적 제약요인이다.\n(2) 질적 특성은 재무제표 정보 외의 다른 경로의 재무보고 정보에는 절대 적용되지 않는다.\n(3) 원가는 정보 효익이 비용을 정당화하는 수준 하에서 작동해야 한다.\n(4) 원가 수준 평가는 오직 특정 일부 이용자의 요구 정보 수에만 기계적으로 비례한다.\n```",
        "options": [
            "① (1): T, (2): T, (3): T, (4): F",
            "② (1): T, (2): F, (3): T, (4): F",
            "③ (1): F, (2): T, (3): T, (4): T",
            "④ (1): F, (2): F, (3): T, (4): F",
            "⑤ (1): T, (2): T, (3): T, (4): T"
        ],
        "answer": "2",
        "explanation": "② 각 질문의 참/거짓 판단은 다음과 같습니다.\n(1) T: 원가는 포괄적 제약요인입니다.\n(2) F: 질적 특성은 재무제표뿐만 아니라 다른 방법으로 제공되는 재무정보에도 적용됩니다.\n(3) T: 효익이 원가를 정당화해야 합니다.\n(4) F: 원가 평가는 일방 주주의 요구 수에만 비례하지 않고 시장 전체의 사회적 효익과 결합 평가됩니다.",
        "question_type": "박스형",
        "option_meta": [
            {"correct": False, "why": "(2)번의 정오 판단이 잘못되었습니다.", "articles": [], "principle": "정오 조합", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "(1) 참, (2) 거짓, (3) 참, (4) 거짓 조합은 개념체계 논리에 완전히 부합합니다.", "articles": [], "principle": "정오 조합 정답", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "(1)번 등의 판단이 틀렸습니다.", "articles": [], "principle": "정오 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "(1)번 판단이 틀렸습니다.", "articles": [], "principle": "정오 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "모두 참이 아닙니다.", "articles": [], "principle": "정오 조합", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },

    # =========================================================================
    # L5: 심화 수준 (2문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s04-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "개념체계 상 '비대칭성(Asymmetry)'은 유용한 재무정보의 질적 특성이 아니라고 밝히고 있음에도 불구하고, 구체적인 기준서(예: 유형자산 손상차손 인식 등)에서 비대칭적 요구사항을 포함할 수 있는 근거와 의의를 가장 잘 설명한 기술은?",
        "options": [
            "① 특정 기준서의 개별적 세부 조항은 개념체계의 목적보다 항상 우선적 사법 효력을 갖기 때문이다.",
            "② 나타내고자 하는 바를 충실하게 표현하는 가장 목적적합한 정보를 선택하려는 결정의 결과(예: 자산의 과대평가를 주의 깊게 차단하는 등)가 비대칭적이라면, 특정 기준서에서 비대칭적인 요구사항을 요구할 수도 있기 때문이다.",
            "③ 비대칭성이 높을수록 세무 감면 혜택을 극대화하려는 위원회의 숨겨진 탈세 의도가 반영된 결과이다.",
            "④ 비대칭적인 요구는 회계감사를 무력화하고 기업 경영진의 재량권을 극대화하려는 역사적 합의의 결과이다.",
            "⑤ 비대칭성은 보강적 질적 특성인 적시성을 전면 말살하여 자본시장의 리스크를 인위적으로 소멸시키기 위한 요건이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 비대칭성 자체를 공식 질적 특성으로 규정하지는 않습니다. 그러나 나타내고자 하는 바를 충실하게 표현하는 가장 목적적합한 정보를 선택하려는 판단의 논리적 귀결이 비대칭(예: 회수가능액이 장부가액에 미달하면 손실은 바로 인식하지만, 초과 상승분은 인식하지 않는 등)이라면, 개별 기준서에서 이러한 비대칭적 회계를 타당하게 포함시킬 수 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "개별 기준서가 개념체계에 우선한다는 지위는 별개이며, 비대칭 포함의 타당한 논리가 아닙니다.", "articles": [], "principle": "개념체계와 기준서 우선", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가장 목적적합하고 충실한 표현을 선택하려는 결정의 결과가 비대칭을 띤다면 기준서가 이를 수용할 수 있다는 진술은 정확한 논리입니다.", "articles": [], "principle": "비대칭 요구사항의 배경", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "탈세 의도 등은 비합리적인 지문입니다.", "articles": [], "principle": "기준제정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진의 독단적 재량권 보장 수단이 아닙니다.", "articles": [], "principle": "중립성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적시성 말살이나 리스크 소멸 조치는 사실이 아닙니다.", "articles": [], "principle": "적시성", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s04-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "재무보고서 작성 시 근본적 질적 특성인 '목적적합성(Relevance)'과 '표현충실성(Faithful Representation)' 간의 상충 및 절충(Trade-off) 관계가 실제로 발생하는 상황에 관한 비판적 분석으로 가장 적절한 것은?",
        "options": [
            "① 역사적 원가 정보는 목적적합성은 매우 높지만 표현충실성(측정검증의 정확성)은 극도로 결여된 절충의 예시이다.",
            "② 보고기업의 장기적인 영업권(Goodwill)을 평가할 때, 이를 기말 공정가치 추정치로 기재하는 행위는 이용자의 자원의사결정 판단(목적적합성)에 큰 피드백을 줄 수 있으나, 관측할 수 없는 주관적 투입변수에 근거하므로 측정불확실성(표현충실성의 저해 요인)이 중대하게 수반되는 절충 상황을 보여준다.",
            "③ 목적적합성과 표현충실성이 충돌할 경우, 개념체계는 항상 표현충실성을 100% 우선 만족하고 목적적합성은 영(0)으로 수렴하도록 규정한다.",
            "④ 상충이 발생하면 회계감사인은 의견거절 외에는 어떠한 회계처리도 승인할 수 없다.",
            "⑤ 상충 관계를 해소하기 위해 기업은 기말 재무보고서 공시 시점 자체를 무기한 연기할 권한을 부여받는다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 근본적 질적 특성 간에는 절충(Trade-off)이 수반되는 경우가 많습니다. 예컨대 자산의 유용한 미래 가치 변동이나 내부영업권 추정치를 재무제표에 반영하면 목적적합성은 높아질 수 있으나, 화폐액을 직접 관측할 수 없어 상당한 측정불확실성(표현충실성의 불리한 제한)을 감수해야 하는 전형적인 상충/절충 상황을 형성합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "역사적 원가는 오히려 검증성과 표현충실성(오류 없음)은 비교적 우수하지만, 시가를 반영하지 못해 목적적합성이 떨어지는 상충의 사례입니다.", "articles": [], "principle": "역사적 원가 상충", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "주관적 추정 자산(영업권 등) 반영이 정보의 유용성(목적적합)과 불확실성(충실성 저해) 간 상충을 유발한다는 지문은 합리적이고 정확합니다.", "articles": [], "principle": "질적 특성 간의 상충", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "한쪽을 강제로 영 수렴시키는 획일적 우선순위는 존재하지 않으며 유용성을 저울질해 절충합니다.", "articles": [], "principle": "질적 특성 간 조화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "절충적인 상태도 주석 등으로 투명하게 설명된다면 정상적인 적정 감사 대상이 됩니다.", "articles": [], "principle": "감사 적합성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공시 무기한 연기는 원가 제약이나 적시성 기준에 전면 위배되어 불허됩니다.", "articles": [], "principle": "적시성 위배", "case": {"holding": "", "no": None}}
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
                "item": "4절 유용한 재무정보의 질적 특성"
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
