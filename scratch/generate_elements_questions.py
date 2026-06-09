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
        "id": "practice-accounting-ch01s06-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "개념체계상 '자산(Asset)'에 관한 정의로 가장 올바른 것은?",
        "options": [
            "① 과거사건의 결과로 기업이 통제하는 현재의 경제적자원",
            "② 미래에 발생할 것으로 예상되는 거래의 결과로 획득할 수 있는 법적 권리",
            "③ 소유주가 사적으로 소유하고 있는 재산 중 가치 평가가 완료된 부동산",
            "④ 기업의 자산에서 부채를 차감한 후의 채권자 소유 지분",
            "⑤ 세무신고서에 기재되어 법적으로 세금을 감면받은 확정 세액 누계"
        ],
        "answer": "1",
        "explanation": "① 개념체계상 자산은 '과거사건의 결과로 기업이 통제하는 현재의 경제적자원'으로 정의됩니다. 경제적자원은 경제적효익을 창출할 잠재력을 지닌 권리를 뜻합니다.\n\n[오답 해설]\n② 미래 예상 사건만으로는 자산이 성립되지 않으며 과거사건의 결과물이어야 합니다.\n③ 소유주 개인의 재산은 기업의 자산이 아닙니다.\n④ 자산에서 부채를 차감한 잔여지분은 자본입니다.\n⑤ 세법상의 감면 세액 누계만을 지칭하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "자산은 과거사건의 결과로 기업이 통제하는 현재의 경제적자원입니다.", "articles": [], "principle": "자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과거사건의 결과여야 하며 미래 거래 예상으로는 자산이 될 수 없습니다.", "articles": [], "principle": "자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기업 실체와 소유주 개인 재산은 별개입니다.", "articles": [], "principle": "자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산에서 부채를 차감한 것은 자본(잔여지분)입니다.", "articles": [], "principle": "자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 신고상 수치에 국한되지 않습니다.", "articles": [], "principle": "자산의 정의", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "개념체계상 '부채(Liability)'에 관한 정의로 가장 올바른 것은?",
        "options": [
            "① 주주들에게 분배해야 할 배당금 중 아직 지급일이 결정되지 않은 금액",
            "② 기업이 법률을 위반하여 법원으로부터 부과받은 형사상 징역형 등의 처벌",
            "③ 과거사건의 결과로 기업이 경제적자원을 이전해야 하는 현재의무",
            "④ 주주들의 초기 자본금 투입액에 법정 이자율을 가산한 잔액",
            "⑤ 회사가 미래에 신규 자산을 구매할 목적으로 수립한 투자 예산"
        ],
        "answer": "3",
        "explanation": "③ 개념체계상 부채는 '과거사건의 결과로 기업이 경제적자원을 이전해야 하는 현재의무'로 정의됩니다. 세 가지 조건(의무, 이전, 과거사건 결과)을 모두 충족해야 합니다.\n\n[오답 해설]\n① 미지급 배당금은 구체적 부채의 일종일 뿐 전체 부채의 정의가 아닙니다.\n② 사법적 형벌은 부채의 회계적 정의가 아닙니다.\n④ 자본 청구권 관련 기술로 부채가 아닙니다.\n⑤ 미래 예산 계획만으로는 현재의 의무가 아니므로 부채가 될 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "미지급 배당금은 부채의 개별 과목 예시일 뿐 정의가 아닙니다.", "articles": [], "principle": "부채의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사법 형사 처벌은 회계상 부채가 아닙니다.", "articles": [], "principle": "부채의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부채는 과거사건의 결과로 기업이 경제적자원을 이전해야 하는 현재의무입니다.", "articles": [], "principle": "부채의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 투입 관련 권리는 자본 항목에 대응됩니다.", "articles": [], "principle": "부채의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 투자 예산 계획은 현재의 의무가 아닙니다.", "articles": [], "principle": "부채의 정의", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "개념체계상 '자본(Equity)'에 관한 설명으로 가장 옳은 것은?",
        "options": [
            "① 기업이 보유한 자산 중 부동산만을 감정평가하여 구한 금액",
            "② 기업의 자산에서 모든 부채를 차감한 후의 잔여지분",
            "③ 대주주들이 기업을 매각할 때 은행에 상환해야 하는 강제 상환금",
            "④ 세무서에 납부 완료한 법인세액의 누계",
            "⑤ 회사의 실제 시장 가격(시가총액)과 소수점까지 일치하는 금액"
        ],
        "answer": "2",
        "explanation": "② 개념체계에 자본은 '기업의 자산에서 모든 부채를 차감한 후의 잔여지분'으로 정의되며, 자본 청구권은 자산에서 부채를 뺀 잔여지분에 대한 청구권입니다.\n\n[오답 해설]\n① 자본은 특정 부동산만의 감정평가액이 아닙니다.\n③ 부채 상환금의 명칭이 아닙니다.\n④ 세무 법인세와 무관한 잔여지분입니다.\n⑤ 자본의 장부금액은 영업권 미인식 등으로 인해 기업의 시가총액과 일반적으로 일치하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "특정 부동산 감정평가액에 제한되지 않습니다.", "articles": [], "principle": "자본의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자본은 기업의 자산에서 모든 부채를 차감한 후의 잔여지분입니다.", "articles": [], "principle": "자본의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채무 상환을 일컫지 않습니다.", "articles": [], "principle": "자본의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "납부 완료 법인세액 누계가 아닙니다.", "articles": [], "principle": "자본의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본의 장부총액은 일반적으로 시가총액과 괴리가 발생합니다.", "articles": [], "principle": "자본의 정의", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "개념체계상 '수익(Income)'에 관한 정의로 가장 올바른 것은?",
        "options": [
            "① 자산의 증가 또는 부채의 감소로서 자본의 증가를 가져오며, 자본청구권 보유자의 출자와 관련된 것을 제외한 것",
            "② 자산의 감소 또는 부채의 증가로서 자본의 감소를 가져오며, 자본청구권 보유자에 대한 분배를 포함한 것",
            "③ 주주들이 신규 투자금을 유입시켜 발생한 법정 자본금의 증가 총액",
            "④ 은행 대출을 실행하여 자금 차입금이 통장에 신규 입금된 금액",
            "⑤ 회사가 보유 중인 유형자산의 면적이 법적으로 확장된 총량"
        ],
        "answer": "1",
        "explanation": "① 개념체계상 수익은 자산의 증가 또는 부채의 감소로서 자본의 증가를 가져오는 거래이며, 주주(자본청구권 보유자)로부터의 출자(증자)는 수익에서 명시적으로 제외됩니다.\n\n[오답 해설]\n② 비용의 성격과 분배를 결합한 설명이며 배당 분배는 제외해야 하므로 오답입니다.\n③ 주주로부터의 출자는 수익의 정의에서 제외됩니다.\n④ 은행 차입금 입금은 부채의 증가이므로 수익이 아닙니다.\n⑤ 자산 면적 확장은 자산/부채/자본의 회계적 변동 수익 정의가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "수익은 자산 증가/부채 감소로 자본 증가를 초래하고 주주의 출자 관련 분은 제외합니다.", "articles": [], "principle": "수익의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비용에 대한 오류 진술입니다.", "articles": [], "principle": "수익의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주주 출자액은 수익에서 제외합니다.", "articles": [], "principle": "수익의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입금 입금은 자산 증가와 동시에 부채가 늘어나므로 자본을 증가시키지 않아 수익이 아닙니다.", "articles": [], "principle": "수익의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 면적 증가는 수익 정의가 아닙니다.", "articles": [], "principle": "수익의 정의", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "개념체계상 '비용(Expenses)'에 관한 정의로 가장 올바른 것은?",
        "options": [
            "① 자산의 증가 또는 부채의 감소로서 자본의 증가를 가져오며, 자본청구권 보유자 배당을 포함하는 거래",
            "② 자산의 감소 또는 부채의 증가로서 자본의 감소를 가져오며, 자본청구권 보유자에 대한 분배와 관련된 것을 제외한 것",
            "③ 회사가 차입한 부채를 갚기 위해 현금이 은행으로 상환 지급된 총액",
            "④ 주주들에게 공식 지급한 배당금 총액",
            "⑤ 회사가 미래의 제품 구매 계약을 맺고 주문서를 작성하여 보관 중인 사실"
        ],
        "answer": "2",
        "explanation": "② 개념체계상 비용은 자산의 감소 또는 부채의 증가로서 자본의 감소를 가져오는 거래이며, 주주(자본청구권 보유자)에 대한 배당 등 분배 행위는 비용에서 명시적으로 제외됩니다.\n\n[오답 해설]\n① 수익 관련 정의와 오답 조건의 결합입니다.\n③ 부채 상환은 자산 감소와 부채 감소가 동시에 일어나 자본의 변동이 없으므로 비용이 아닙니다.\n④ 배당은 비용에서 제외되는 자본 감소 항목입니다.\n⑤ 단순 주문서 보관은 경제적 자원 유출이 없으므로 비용이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수익 개념에 배당을 섞은 오답입니다.", "articles": [], "principle": "비용의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비용은 자산 감소/부채 증가로 자본 감소를 초래하며 주주에 대한 분배 분은 제외합니다.", "articles": [], "principle": "비용의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 상환은 자본 변동을 일으키지 않는 교환 거래로 비용이 아닙니다.", "articles": [], "principle": "비용의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "배당 분배는 비용이 아닙니다.", "articles": [], "principle": "비용의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미이행 계약 주문 사실만으로는 비용이 성립하지 않습니다.", "articles": [], "principle": "비용의 정의", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "개념체계상 '회계단위(Unit of Account)'에 관한 정의로 가장 옳은 것은?",
        "options": [
            "① 거래 금액을 기록하는 원화, 달러 등 법정 통화의 최소 표기 단위",
            "② 인식기준과 측정개념이 적용되는 권리나 권리의 집합, 의무나 의무의 집합 또는 권리와 의무의 집합",
            "③ 대손충당금을 기재하는 계정과목 원장의 최하위 코드 분류 번호",
            "④ 모회사와 자회사의 지분을 교환하는 거래 시장의 법적 명칭",
            "⑤ 회계법인의 회계감사 파트너 1인이 맡을 수 있는 자산 규모 범위"
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계단위를 '인식기준과 측정개념이 적용되는 권리나 권리의 집합, 의무나 의무의 집합 또는 권리와 의무의 집합'으로 정의하고 있습니다.\n\n[오답 해설]\n① 법정 화폐 표기 단위를 뜻하지 않습니다.\n③, ⑤ 원장 계정 코드나 회계사의 수임 한도 등 실무 외적 개념이 아닙니다.\n④ 지분 교환 거래 시장을 회계단위라 부르지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "화폐 단위가 아닙니다.", "articles": [], "principle": "회계단위 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "인식과 측정이 적용되는 권리/의무의 집합 등을 회계단위라 합니다.", "articles": [], "principle": "회계단위 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계정과목 코드 명칭이 아닙니다.", "articles": [], "principle": "회계단위 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래 시장의 명칭이 아닙니다.", "articles": [], "principle": "회계단위 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사인의 감사 수임 한도를 일컫지 않습니다.", "articles": [], "principle": "회계단위 정의", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "개념체계상 '미이행계약(Executory Contract)'에 대한 정의로 가장 올바른 것은?",
        "options": [
            "① 법적으로 효력이 무효화되어 더 이상 이행할 수 없게 된 폐기 계약",
            "② 계약당사자 중 한쪽만 일방적으로 의무를 100% 이행하고 다른 쪽은 대금을 미납한 계약",
            "③ 계약당사자 모두가 자신의 의무를 전혀 수행하지 않았거나 계약당사자 모두가 동일한 정도로 자신의 의무를 부분적으로 수행한 계약",
            "④ 법원의 판결에 의해서 강제로 이행 의무가 정지된 연체 소송 사건",
            "⑤ 회사의 대주주가 개인 자금 대여를 위해 맺은 특수 관계자 금전 대차 계약"
        ],
        "answer": "3",
        "explanation": "③ 개념체계에 따르면 미이행계약은 계약당사자 모두가 의무를 전혀 수행하지 않았거나 모두가 동일한 정도로 부분 수행한 계약을 의미합니다.\n\n[오답 해설]\n① 효력이 무효화된 계약이 아닙니다.\n② 한쪽만 일방 이행한 계약은 미이행계약 상태에서 벗어납니다.\n④, ⑤ 법원 정지 계약이나 주주의 금전 대차 계약 한 분야로 한정하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "무효화된 계약이 아닙니다.", "articles": [], "principle": "미이행계약 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "한쪽만 의무를 다한 경우는 미이행 상태가 유지되지 않습니다.", "articles": [], "principle": "미이행계약 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "양 당사자 모두 의무가 없거나 동등하게 부분 수행한 결합 계약을 뜻합니다.", "articles": [], "principle": "미이행계약 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법원 의무 정지와 무관합니다.", "articles": [], "principle": "미이행계약 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대주주 금전 대차에 한정되지 않습니다.", "articles": [], "principle": "미이행계약 정의", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "개념체계에 따를 때, 기업이 스스로 발행한 후 재매입하여 임시 보관 중인 '자기주식'이 보고기업의 자산(경제적자원)으로 인정받지 못하는 근본적인 이론 논리는?",
        "options": [
            "① 자기주식은 법원 등기소에 등록할 수 없는 불법 증권이기 때문이다.",
            "② 기업은 자기 스스로부터 경제적효익을 획득하는 권리를 가질 수는 없기 때문이다.",
            "③ 자기주식은 은행에 담보로 제공할 수 없도록 회계기준위원회가 차단했기 때문이다.",
            "④ 자기주식은 배당금을 받을 권리가 주주총회 상에서만 영구 면제되기 때문이다.",
            "⑤ 취득할 때 지출된 원가가 0원인 경우가 대부분이기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 자산 요건 중 하나로 권리를 다룰 때, '기업은 기업 스스로부터 경제적효익을 획득하는 권리를 가질 수는 없다'고 규정합니다. 따라서 자기주식이나 재매입 채무상품 등은 자산(경제적자원)이 아닙니다.\n\n[오답 해설]\n① 자기주식 취득은 법적으로 정당한 절차입니다.\n③, ④, ⑤ 은행 담보나 배당 권리 소멸, 취득 원가 수준 자체가 자산 제외의 근본적 개념체계 이론 논리는 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자기주식 취득이 불법 행위는 아닙니다.", "articles": [], "principle": "자기주식 배제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "스스로부터 효익을 얻는 권리를 성립시킬 수 없다는 것이 자산 제외의 이론적 근거입니다.", "articles": [], "principle": "자기주식 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "담보 제공 금지 규정 등은 본질이 아닙니다.", "articles": [], "principle": "자기주식 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "배당권 제한은 부수적 법적 효과일 뿐입니다.", "articles": [], "principle": "자기주식 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득 원가가 0원이라는 것은 틀렸습니다.", "articles": [], "principle": "자기주식 배제", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "계약 조건에 따른 권리와 의무를 재무제표에 충실하게 표현(Faithful Representation)하기 위해 개념체계가 요구하는 핵심 원칙은?",
        "options": [
            "① 법적 계약서의 형식에 구애받지 않고 계약의 '실질(Substance)'을 보고한다.",
            "② 계약 상대방의 세무서 승인 여부를 최우선으로 검증한다.",
            "③ 계약으로 인해 미래에 유입될 최대 예상 낙관 가액만을 기록한다.",
            "④ 법률 전문가들이 작성해 준 문구 문맥의 형식적 법률 자구만을 준용한다.",
            "⑤ 계약 체결 시 지출된 대리인 중개 수수료의 100배를 자산으로 처리한다."
        ],
        "answer": "1",
        "explanation": "① 개념체계는 계약상 권리와 의무의 실질을 표현하기 위해 '실질의 보고(Report the Substance)'를 요구합니다. 실질이 없는 조건은 무시해야 합니다.\n\n[오답 해설]\n② 세무서의 세무 승인은 충실한 표현의 판단 요건이 아닙니다.\n③ 낙관 가액의 기재는 중립성을 해칩니다.\n④ 형식적 법률 형식에만 매달리면 실질적 경제 현상을 오도할 수 있습니다.\n⑤ 수수료의 100배 처리는 중대한 회계 오류입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "법적 형식에 매몰되지 않고 경제적 권리/의무의 실질을 보고해야 표현충실성이 충족됩니다.", "articles": [], "principle": "실질의 보고", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 승인과 충실한 표현은 별개입니다.", "articles": [], "principle": "실질의 보고", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "낙관 가액 기재는 중립성 저해 사유입니다.", "articles": [], "principle": "실질의 보고", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "형식에만 매달리면 경제적 실질이 가려질 수 있습니다.", "articles": [], "principle": "실질의 보고", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중개 수수료 과대 계상은 오류입니다.", "articles": [], "principle": "실질의 보고", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "자산의 경제적효익을 창출할 '잠재력(Potential)' 요건에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 경제적효익을 창출할 것이 백퍼센트 확실하고 보장될 때에만 권리가 자산이 될 수 있다.",
            "② 경제적효익을 창출할 가능성이 아주 낮다면, 해당 권리는 결코 자산이 될 수 없다.",
            "③ 잠재력이 있기 위해 경제적효익을 창출할 것이 확신될 필요는 없으며, 가능성이 낮더라도 권리가 자산의 정의를 충족할 수 있다.",
            "④ 잠재력은 오직 기말 장부가격이 시가총액보다 높을 때에만 임의 인정된다.",
            "⑤ 잠재력 평가는 경영진이 아닌 세무 공무원이 자의적으로 부여하는 세제 혜택 점수이다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계에 따르면, 경제적자원이 되기 위해 경제적효익 창출이 확신될 필요는 없습니다. 권리가 이미 존재하고 적어도 하나의 상황에서 경제적효익을 창출할 잠재력이 있다면 가능성이 낮더라도 자산이 될 수 있습니다.\n\n[오답 해설]\n①, ② 효익 창출이 100% 확실할 필요는 없으며 가능성이 낮아도 자산 정의 충족이 가능합니다.\n④ 시가총액과의 비교는 잠재력 성립 요건이 아닙니다.\n⑤ 경영진의 회계적 평가 및 감사 대상이지 세무관서가 지정하는 등급 점수가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "100% 확실성을 요하지 않습니다.", "articles": [], "principle": "잠재력의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유출입 가능성이 낮아도 자산 요건은 성립할 수 있습니다.", "articles": [], "principle": "잠재력의 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "확신할 필요 없이 하나 이상의 상황에서 효익을 낼 능력이 있으면 가능성이 낮아도 자산이 됩니다.", "articles": [], "principle": "잠재력의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가총액 관계는 무관합니다.", "articles": [], "principle": "잠재력의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 공무원의 점수 부여가 아닙니다.", "articles": [], "principle": "잠재력의 요건", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },

    # =========================================================================
    # L2: 이해 수준 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s06-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "자산의 핵심 구성 요건인 '통제, 권리, 효익창출잠재력'에 대한 설명 중 옳은 것은?",
        "options": [
            "① 지출의 발생은 자산의 취득과 밀접하게 관련되므로 양자는 반드시 완벽하게 일치한다.",
            "② 제공받는 즉시 소비되는 재화나 용역(예: 종업원 용역)은 제공받기 전부터 영구히 자산으로 잡아야 한다.",
            "③ 지출이 발생하였더라도 자산의 요건을 충족하지 못하면 해당 지출은 수익으로 계상된다.",
            "④ 지출의 발생과 자산의 취득은 밀접하게 관련되어 있으나 양자가 반드시 일치하는 것은 아니다.",
            "⑤ 물리적 형태가 없는 특허권 등은 어떠한 경우에도 권리에 해당하지 않아 자산이 될 수 없다."
        ],
        "answer": "4",
        "explanation": "④ 개념체계는 지출의 발생과 자산의 취득이 밀접하나 반드시 일치하지는 않음을 명시합니다. 예를 들어 자산 취득 없이 지출만 발생하여 비용 처리되는 경우(예: 개발비 요건 미달액) 등이 있습니다.\n\n[오답 해설]\n① 일치하지 않는 예외가 존재합니다.\n② 즉시 소비 용역에 대한 통제 권리는 일시적으로 존재할 뿐 영구 자산화될 수 없습니다.\n③ 자산 요건 미충족 지출은 수익이 아닌 비용으로 직행합니다.\n⑤ 특허권 등 무형자산도 통제 가능한 권리에 속하므로 자산이 될 수 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "양자가 일치하지 않는 실무 사례가 많습니다.", "articles": [], "principle": "자산과 지출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "제공받는 즉시 소비되는 권리는 장기 자산이 아닙니다.", "articles": [], "principle": "자산과 지출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지출은 자산이 안 되면 비용이 됩니다.", "articles": [], "principle": "자산과 지출", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "지출 발생과 자산 취득은 밀접하지만 인과관계상 불일치할 수 있습니다.", "articles": [], "principle": "자산과 지출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "물리적 형태 부재가 자산 제외 사유는 아닙니다.", "articles": [], "principle": "자산과 지출", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "자산의 정의 중 '통제(Control)'의 개념에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 기업은 경제적자원의 사용을 지시하고 그로부터 유입될 수 있는 경제적효익을 얻을 수 있는 현재의 능력이 있다면 그 자원을 통제한다.",
            "② 통제에는 다른 당사자가 경제적자원의 사용을 지시하고 이로부터 유입될 수 있는 효익을 얻지 못하게 막는 현재의 능력이 포함된다.",
            "③ 일방의 당사자가 경제적자원을 통제하고 있다면 다른 당사자는 그 자원을 동시에 통제할 수 없다.",
            "④ 법적 소유권(Legal Title)이 없다면 개념체계상 어떠한 자원에 대해서도 통제를 행사할 현재의 능력을 가질 수 없다.",
            "⑤ 통제 능력을 행사하기 위해 법적 집행력(Legal Enforceability)이 반드시 명문화되어 필요한 것은 아니지만 법적 권리가 있으면 통제 입증이 쉬워진다."
        ],
        "answer": "4",
        "explanation": "④ 법적 소유권이 없더라도(예: 금융리스 임차인), 해당 자원의 사용을 지시하고 다른 당사자의 접근을 차단하는 실질적 통제가 가능하면 통제 현재의 능력이 인정되어 자산으로 인식됩니다. 따라서 소유권 부재 시 무조건 통제가 불가하다는 서술은 틀렸습니다.\n\n[오답 해설]\n①, ②, ③, ⑤ 모두 개념체계 상 통제의 요건을 올바르게 서술하였습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "통제의 기본 성질 설명은 맞습니다.", "articles": [], "principle": "통제의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "다른 당사자를 배제하는 능력이 통제에 포함됨은 맞습니다.", "articles": [], "principle": "통제의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일방의 통제는 타방의 통제를 배격합니다.", "articles": [], "principle": "통제의 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "법적 소유권이 없어도 실질적 사용과 배제 능력이 있으면 통제를 행사할 수 있습니다.", "articles": [], "principle": "통제의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법적 권리가 필수 요건이 아님은 옳습니다.", "articles": [], "principle": "통제의 요건", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "부채의 정의 중 '현재의무(Present Obligation)'에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 의무란 기업이 회피할 수 있는 실제 능력이 없는 책무나 책임을 말한다.",
            "② 의무는 항상 다른 당사자(사람, 기업, 사회 전반 등)에게 이행해야 하는 성질을 지닌다.",
            "③ 부채가 존재하기 위해 의무를 이행할 대상인 상대방 당사자들의 구체적 신원(이름, 주소 등)을 명확하게 알아야만 한다.",
            "④ 많은 의무가 계약이나 법률 또는 이에 준하는 수단에 의해 법적 집행력 있게 성립한다.",
            "⑤ 기업의 오랜 실무 관행이나 공개된 방침 등에서 '의제의무(Constructive Obligation)'가 발생할 수도 있다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계에 따르면 의무를 이행할 대상인 상대 당사자(또는 당사자들)의 신원을 구체적으로 파악해 명시할 필요는 없습니다. 사회 전반이나 미래의 특정 집단일 수도 있기 때문입니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 모두 부채의 의무 요건에 부합하는 정당한 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "회피 불가능한 책무가 의무입니다.", "articles": [], "principle": "현재의무의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "다른 당사자에게 이행하는 책무가 맞습니다.", "articles": [], "principle": "현재의무의 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "의무 이행 대상자의 신원을 구체적으로 확정하여 알 필요는 없습니다.", "articles": [], "principle": "현재의무의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계약/법률이 주된 성립 경로입니다.", "articles": [], "principle": "현재의무의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실무 관행에 의한 의제의무도 부채가 될 수 있습니다.", "articles": [], "principle": "현재의무의 요건", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "부채의 성립 조건 중 '의제의무(Constructive Obligation)'에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 법적 소송이 확정되어 판사가 직접 판결문으로 강제 부과한 법적 의무만을 의미한다.",
            "② 기업이 법률을 회피하여 비공식적으로 세금을 덜 내려고 준비해 둔 비밀 자금 마련 책무이다.",
            "③ 기업의 오랜 실무 관행, 공개한 경영방침 또는 성명서와 상충되게 행동할 실제 능력이 없어 상대방에게 정당한 기대를 유발하여 성립하는 의무이다.",
            "④ 의제의무는 주주총회 특별결의를 거쳐서 정관에 등기된 경우에 한해서만 성립한다.",
            "⑤ 회사가 언제든 마음대로 취소하거나 번복할 수 있는 실제 능력을 가진 임의의 구두 선언이다."
        ],
        "answer": "3",
        "explanation": "③ 의제의무는 기업이 실무 관행, 공개 경영방침 또는 성명 등을 통해 특정 책임을 수용할 것임을 나타내고, 그 결과 상대방이 정당한 기대를 가지게 함으로써 기업이 이를 회피할 실제 능력이 없는 경우에 성립하는 의무입니다.\n\n[오답 해설]\n① 법적 판결문 강제 의무는 의제의무가 아니라 법적의무입니다.\n② 불법 비밀 자금 마련은 부채 정의와 상관없습니다.\n④ 정관 등기가 성립의 절대 조건이 아닙니다.\n⑤ 기업이 취소/번복할 실제 능력을 보유하고 있다면 의무가 성립하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "법적 의무만을 일컫지 않습니다.", "articles": [], "principle": "의제의무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비밀 자금 관련 진술은 무관합니다.", "articles": [], "principle": "의제의무", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "실무 관행이나 방침 등으로 인해 기업이 회피할 능력이 없는 신뢰 기대 의무가 의제의무입니다.", "articles": [], "principle": "의제의무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특별결의 정관 등기 필수 규정이 아닙니다.", "articles": [], "principle": "의제의무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회피 실제 능력이 있다면 의무가 될 수 없습니다.", "articles": [], "principle": "의제의무", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "부채의 두 번째 조건인 '경제적자원의 이전(Transfer of Economic Resource)' 의무에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 의무의 이행을 위해 미래에 자원이 이전될 가능성이 극히 낮다면, 해당 의무는 부채가 될 수 없다.",
            "② 자원의 이전 가능성이 낮더라도(예: 보증 의무 등), 이전하도록 요구받게 될 잠재력이 존재한다면 의무는 부채의 정의를 충족할 수 있다.",
            "③ 경제적자원의 이전은 무조건 현금의 직접 유출만을 의미하며, 용역의 제공 등은 포함되지 않는다.",
            "④ 자원 이전이 100% 확실할 때에만 재무상태표 주석에 부채 공시를 개시한다.",
            "⑤ 이전 잠재력의 평가는 오직 국가 규제기관의 승인 문서가 발급될 때 개시된다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 자원 이전 가능성이 낮더라도(예: 보증 수수 대가 등) 의무를 이전해야 할 잠재적 상황이 존재한다면 부채 정의를 충족합니다. 다만 인식 단계에서 측정불확실성이나 목적적합성 등을 별도로 평가할 뿐입니다.\n\n[오답 해설]\n① 가능성이 낮아도 부채 정의 충족은 가능합니다.\n③ 자원 이전은 현금 유출 뿐 아니라 용역 제공, 자산의 양도 등도 포함합니다.\n④ 100% 확실성이 부채 성립과 주석 공시의 최소 조건이 아닙니다.\n⑤ 규제기관 승인 여부에 얽매이지 않고 회계적으로 평가합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "유출 가능성이 낮아도 부채 정의가 충족될 수 있습니다.", "articles": [], "principle": "이전 잠재력", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이전 가능성이 낮아도 요구받게 될 잠재력이 있다면 부채 정의를 충족합니다.", "articles": [], "principle": "이전 잠재력", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금 외의 자산 양도나 서비스 제공도 자원 이전입니다.", "articles": [], "principle": "이전 잠재력", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "확실성을 요건으로 삼지 않습니다.", "articles": [], "principle": "이전 잠재력", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "규제기관 승인은 불필요합니다.", "articles": [], "principle": "이전 잠재력", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "부채 인식과 자산 인식 간의 상호 관계에 관한 개념체계의 설명으로 가장 올바른 것은?",
        "options": [
            "① 거래의 일방 당사자가 부채를 인식하면, 타방 당사자는 무조건 동일 금액의 자산을 동시에 장부에 인식해야만 한다.",
            "② 한 당사자가 부채를 인식하고 이를 특정 금액으로 측정해야 한다는 요구사항이, 다른 당사자가 자산을 인식하거나 동일한 금액으로 측정해야 한다는 것을 의미하지는 않는다.",
            "③ 타방 당사자가 자산 인식을 거절하였다면, 부채 의무가 있는 기업도 부채 인식을 즉시 무단 삭제할 수 있다.",
            "④ 금융기관이 대출 채권을 상각하였다면, 채무자 기업도 부채 상환 의무가 법적으로 자동 면제된다.",
            "⑤ 회계장부의 대칭성은 절대적이므로 양 당사자의 대차대조표 상 자산과 부채 금액은 1원 단위까지 언제나 동일하여야 한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 대칭성이 항상 적용되는 것은 아님을 규정합니다. 즉, 일방의 부채 인식이 상대방의 자산 인식이나 동일 금액 측정을 수반함을 강제하지 않습니다. 상대방의 자산 인식 요건(통제 여부 등)은 별도로 따져야 하기 때문입니다.\n\n[오답 해설]\n①, ⑤ 상대방 자산 인식과 동일 금액 측정이 무조건 강제되는 대칭적 관계가 아닙니다.\n③, ④ 상대방의 상각이나 인식 거부 여부가 내 부채 상환 책임 및 인식 여부를 자의적으로 삭제하지 못합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "동시 인식 및 동일 금액 측정이 강제되지 않습니다.", "articles": [], "principle": "인식 대칭성 배격", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "일방의 부채 인식/측정이 상대방의 자산 인식/동일 금액 측정을 강제하는 대리 조건이 아님이 명시되어 있습니다.", "articles": [], "principle": "인식 대칭성 배격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상대방 태도로 내 부채를 지울 수는 없습니다.", "articles": [], "principle": "인식 대칭성 배격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상대방의 회계 상각이 내 채무 소멸을 뜻하지 않습니다.", "articles": [], "principle": "인식 대칭성 배격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1원 단위 대칭 일치는 의무가 아닙니다.", "articles": [], "principle": "인식 대칭성 배격", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "자본(Equity)의 측정 방식에 관한 개념체계의 설명으로 가장 올바른 것은?",
        "options": [
            "① 자본은 매 영업일 종료 시 주식 시장의 마감 시세를 바탕으로 장부금액을 직접 산출한다.",
            "② 자본의 총장부금액(총자본)은 직접 측정하지 않으며, 인식된 모든 자산의 장부금액에서 인식된 모든 부채의 장부금액을 차감하여 구한다.",
            "③ 자본금과 이익잉여금 등 모든 개별 구성요소도 양(+)의 장부 가치만 가지며 음(-)의 가치는 가질 수 없다.",
            "④ 자본의 측정은 오직 외부 감정평가법인이 평가 보고서를 제출할 때에만 간접 인정된다.",
            "⑤ 수익과 비용을 모두 뺀 영업이익 누계액만을 단독 자본 총액으로 측정 기록한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계상 자본의 총장부금액은 직접 독립 측정하지 않고, 자산 총액에서 부채 총액을 뺀 잔액(잔여지분)으로 일괄 연계 산출합니다.\n\n[오답 해설]\n① 주가 시세로 장부 자본을 매일 갱신하지 않습니다.\n③ 자본잠식 시 총자본이나 개별 항목이 음(-)의 값을 가질 수 있습니다.\n④ 감정평가 보고서 수령이 측정의 필수 조건이 아닙니다.\n⑤ 영업이익 누계 단독 항목만을 자본으로 보지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "주가 마감 시세로 직접 측정하지 않습니다.", "articles": [], "principle": "자본의 측정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자본 총액은 직접 측정하지 않고 자산에서 부채를 차감한 잔여지분액으로 결정합니다.", "articles": [], "principle": "자본의 측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "음(-)의 값을 가질 수 있습니다.", "articles": [], "principle": "자본의 측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감정평가법인의 관여 대상이 아닙니다.", "articles": [], "principle": "자본의 측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업이익에 국한되지 않습니다.", "articles": [], "principle": "자본의 측정", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "자본의 장부총액과 기업의 실제 가치(Value)의 불일치 현상에 관한 개념체계의 설명으로 옳은 것은?",
        "options": [
            "① 자본 장부총액은 반드시 기업의 실제 시가총액과 완벽히 일치하여야 정상 회계이다.",
            "② 일반목적재무제표는 기업의 가치를 직접 보여주기 위해 고안되지 않았기 때문에, 자본의 총장부금액은 기업의 시가총액이나 청산 처분 유입액 등과 일반적으로 일치하지 않는다.",
            "③ 불일치 현상은 회계담당자의 심각한 태만으로 발생한 장부 기재 오류의 증거이다.",
            "④ 기업 가치와의 불일치 금액은 다음 달 영업비용으로 전액 강제 계상되어야 한다.",
            "⑤ 회계기준위원회는 자본 총액과 시가총액을 일치시키기 위해 매월 인위적인 보정 분개를 지시한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 자본의 장부금액이 기업 가치(시가총액, 매각 조달 가치, 청산 조달 가치 등)와 불일치하는 것은 지극히 정상입니다. 재무제표는 가치 추정을 위한 유용한 정보를 제공할 뿐 가치 자체를 직접 보여주도록 설계되지 않았기 때문입니다.\n\n[오답 해설]\n①, ③, ④, ⑤ 불일치는 정상적인 결과이며, 이를 오류나 분식, 인위적 보정 비용 대상 등으로 취급하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "일치할 필요가 없으며 불일치가 정상입니다.", "articles": [], "principle": "자본과 기업가치", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가치를 직접 제시하는 것이 목적이 아니므로 자본총액과 시가총액 등은 괴리되는 것이 당연합니다.", "articles": [], "principle": "자본과 기업가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "장부 오류의 증거가 아닙니다.", "articles": [], "principle": "자본과 기업가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업비용 처리 대상이 아닙니다.", "articles": [], "principle": "자본과 기업가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인위적 시가 보정 분개를 강제하지 않습니다.", "articles": [], "principle": "자본과 기업가치", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "자본의 값의 범위와 음(-)의 자본 발생 타당성에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 자본은 물리적 실체가 존재하는 한 어떠한 경우에도 음(-)의 값을 가질 수 없다.",
            "② 총자본은 일반적으로 양(+)의 값이지만, 인식된 모든 부채가 자산을 초과하는 경우에는 음(-)의 값을 가질 수 있다.",
            "③ 음의 자본 상태가 되면 재무상태표 공시 자체가 즉각 원천 금지된다.",
            "④ 자본의 개별 항목(예: 자기주식 차감 등)은 절대 음(-)으로 적힐 수 없도록 법제화되어 있다.",
            "⑤ 자본이 음(-)이 되는 즉시 회사는 법원으로부터 해산 징역형을 자동 선고받는다."
        ],
        "answer": "2",
        "explanation": "② 인식된 부채가 자산보다 크면 잔여지분인 총자본은 음(-)의 값(자본잠식)을 가질 수 있으며, 이는 개념체계상 자연스러운 측정의 결과입니다.\n\n[오답 해설]\n①, ④ 개별 자본 조정 항목이나 총자본 모두 음(-)의 값을 가질 수 있습니다.\n③ 자본잠식 상태라도 보고서를 공시할 의무는 유효합니다.\n⑤ 자본잠식이 형사 처벌(해산 징역 등) 대상 사유는 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자본잠식 시 음의 자본이 발생할 수 있습니다.", "articles": [], "principle": "음의 자본", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산보다 부채가 많이 인식되는 상황에서는 총자본이 음의 값을 가질 수 있습니다.", "articles": [], "principle": "음의 자본", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공시 금지 대상이 아닙니다.", "articles": [], "principle": "음의 자본", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자기주식 등 개별 음의 자본 항목이 존재합니다.", "articles": [], "principle": "음의 자본", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "해산 징역형 사유가 아닙니다.", "articles": [], "principle": "음의 자본", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "개념체계상 '수익(Income)'의 정의에 대한 정오 판단 중 올바르지 않은 것은?",
        "options": [
            "① 수익은 기업의 재무성과와 관련된 재무제표 요소에 해당한다.",
            "② 수익이 발생하면 결과적으로 기업의 자본이 증가한다.",
            "③ 주주들의 자금 납입으로 인한 출자(유상증자 등)도 자본을 증가시키므로 수익에 해당한다.",
            "④ 수익은 자산의 증가뿐만 아니라 부채의 감소를 통해서도 발생할 수 있다.",
            "⑤ 수익의 정의에 따라 주주의 출자 거래는 수익에서 배제된다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계 수익의 정의상 '자본청구권 보유자(주주)의 출자와 관련된 것'은 명시적으로 제외됩니다. 따라서 출자는 자본을 늘리지만 수익이 아닙니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 모두 수익의 정의와 특징을 올바르게 설명하고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "성과 요건이 맞습니다.", "articles": [], "principle": "수익의 정의 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 증가 효과는 참입니다.", "articles": [], "principle": "수익의 정의 정오", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "주주의 유상증자 출자금 납입은 수익의 정의에서 명시적으로 제외되는 자본 거래입니다.", "articles": [], "principle": "수익의 정의 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 감소로 인한 수익 발생(예: 채무면제이익 등)도 존재합니다.", "articles": [], "principle": "수익의 정의 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "출자 배제가 올바른 정의입니다.", "articles": [], "principle": "수익의 정의 정오", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "개념체계상 '비용(Expenses)'의 정의에 대한 정오 판단 중 올바르지 않은 것은?",
        "options": [
            "① 비용은 기업의 재무성과와 연계되는 재무제표 요소이다.",
            "② 비용이 인식되면 기업의 순자산(자본)이 감소하는 효과를 낸다.",
            "③ 주주들에게 배당금을 분배 지급한 거래는 자본을 감소시키므로 영업비용으로 기재한다.",
            "④ 비용은 자산의 감소뿐만 아니라 부채의 증가(예: 미지급비용 인식)를 통해서도 성립한다.",
            "⑤ 수익과 비용은 재무제표이용자가 기업의 경영 성과를 평가할 때 필수적으로 요구하는 정량적 정보이다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계 비용의 정의상 '자본청구권 보유자(주주)에 대한 분배(현금배당 등)와 관련된 것'은 비용에서 제외됩니다. 배당은 이익잉여금의 감소(자본 거래)로 처리할 뿐 비용이 아닙니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 모두 비용의 정의 및 재무보고상 성격을 충실하게 기술한 참 지문들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "성과 정보 연계는 참입니다.", "articles": [], "principle": "비용의 정의 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 감소 결과는 참입니다.", "articles": [], "principle": "비용의 정의 정오", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "배당 분배는 비용 정의에서 명시적으로 제외되므로 영업비용에 얹을 수 없습니다.", "articles": [], "principle": "비용의 정의 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 감소나 부채 증가가 원인임은 참입니다.", "articles": [], "principle": "비용의 정의 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "성과 평가 필수 요소임은 참입니다.", "articles": [], "principle": "비용의 정의 정오", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "개념체계에 명시된 '회계단위(Unit of Account)'의 선택 및 적용에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 인식기준과 측정개념이 자산/부채 등에 어떻게 적용될 것인지를 고려하여 적절히 선택한다.",
            "② 상황에 따라 인식을 위한 회계단위와 측정을 위한 회계단위를 서로 다르게 선택할 수도 있다.",
            "③ 단일 회계단위 내에서 결합된 권리와 의무를 함께 처리하는 것은, 자산과 부채를 기말에 단순히 서로 퉁쳐서 상계(Offsetting)하는 것과 명확히 구분된다.",
            "④ 회계단위는 무조건 회사 전체의 단일 원장 계정 하나만을 강제적으로 선택 적용하여야 한다.",
            "⑤ 회계단위를 선택할 때에는 정보의 유용성과 적용 원가를 제약 요인으로 함께 검토한다."
        ],
        "answer": "4",
        "explanation": "④ 회계단위는 개별 자산의 성격, 의무의 집합 등에 따라 다르게 선택할 수 있으며, 인식과 측정을 위해 다양한 단위가 유용하게 구분 설정될 수 있습니다. 회사 전체에 하나의 단일 계정만을 강제 적용하지 않습니다.\n\n[오답 해설]\n①, ②, ③, ⑤ 모두 개념체계 회계단위 해설 기준과 완벽하게 일치합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "인식/측정의 유용성을 감안해 설정합니다.", "articles": [], "principle": "회계단위 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인식과 측정 단위를 별도로 잡는 것이 허용됩니다.", "articles": [], "principle": "회계단위 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단일 회계단위 처리는 단순 대차 상계와는 전혀 다른 실질적 회계 회계단위 결정입니다.", "articles": [], "principle": "회계단위 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "원장 하나만을 유일한 회계단위로 쓰라는 강제 규정은 전혀 존재하지 않습니다.", "articles": [], "principle": "회계단위 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유용성과 원가가 제약 조건이 됨은 정당합니다.", "articles": [], "principle": "회계단위 적용", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "개념체계에 따른 '미이행계약(Executory Contract)'이 성립시키는 권리와 의무 및 자산/부채의 지위에 관한 설명으로 옳은 것은?",
        "options": [
            "① 미이행계약의 권리와 의무는 서로 완전히 독립적이므로 별도의 자산과 별도의 부채로 분리하여 각기 장부에 기록한다.",
            "② 미이행계약에 따른 결합된 권리와 의무는 상호의존적이어서 분리할 수 없으므로, 단일 자산 또는 단일 부채를 구성한다.",
            "③ 미이행계약은 계약일 당일에 무조건 자산과 부채를 동시에 같은 금액으로 100% 인식해야 한다.",
            "④ 미이행계약은 계약 당사자 일방이 자신의 의무를 이행하는 즉시 효력이 완전히 소멸하여 폐기된다.",
            "⑤ 미이행계약은 교환 조건의 유리/불리 여부와 무관하게 아무런 정보도 제공하지 않는다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 미이행계약의 권리와 의무는 상호의존적이어서 뗄 수 없습니다. 따라서 이들은 결합하여 '단일의 자산' 또는 '단일의 부채'를 구성하게 됩니다.\n\n[오답 해설]\n① 개별 권리/의무로 강제 분리 기재하지 않습니다.\n③ 계약 조건이 유리하거나 불리해지기 전까지(즉, 등가 상태)는 자산/부채로 인식하지 않는 것이 원칙입니다.\n④ 한쪽이 이행을 개시하면 더 이상 미이행계약이 아니지만 계약 자체가 소멸 폐기되는 것은 아닙니다.\n⑤ 교환조건 변동 시 자산이나 부채가 파생되어 정보를 보고합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상호의존적이라 분리 기재하지 않습니다.", "articles": [], "principle": "미이행계약 지위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "권리와 의무의 상호의존성 때문에 단일 자산이나 단일 부채로 취급됩니다.", "articles": [], "principle": "미이행계약 지위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계약일 당일 무조건 인식을 강제하지 않습니다.", "articles": [], "principle": "미이행계약 지위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일방 이행 시 미이행 딱지는 떼지만 계약이 소멸하진 않습니다.", "articles": [], "principle": "미이행계약 지위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유불리에 따라 자산/부채 정보가 파생됩니다.", "articles": [], "principle": "미이행계약 지위", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "계약 조건상 권리와 의무의 '실질(Substance)'을 반영할 때, 개념체계가 '실질이 없는 조건'에 대해 취하는 조치로 가장 옳은 것은?",
        "options": [
            "① 실질이 없더라도 서류상 존재하면 무조건 가중치를 두어 반영한다.",
            "② 실질이 없는 조건은 무시한다. 조건이 계약의 경제적 측면에서 구별할 수 있는 영향을 미치지 않는다면 그 조건은 실질이 없다.",
            "③ 실질이 없는 조건에 영업권 금액을 배분하여 자산을 증대시킨다.",
            "④ 실질이 없는 조건은 무조건 법원에 형사 고발하여 무효 처분 판결을 받아내야 한다.",
            "⑤ 실질 여부와 상관없이 모든 조항의 글자 수에 비례하여 부채를 나누어 기재한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 계약상 권리와 의무의 실질을 보고하기 위해 실질이 없는 조건은 무시하며, 경제적 영향이 구별되지 않는 조건이 실질이 없는 대표적 예시입니다.\n\n[오답 해설]\n①, ③, ⑤ 실질이 없는 껍데기 조항을 장부에 억지로 반영하거나 자산을 불리는 도구로 쓰면 안 되며 무시하여야 합니다.\n④ 법적 형사 고발 대상이 아닌 회계 상의 무시(정리) 기재 조치입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "형식에 치우친 가중치 부여는 금지됩니다.", "articles": [], "principle": "실질의 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "경제적 영향이 없는 형식뿐인 조항(실질이 없는 조건)은 회계상 무시해야 합니다.", "articles": [], "principle": "실질의 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업권 인위적 배분은 불법입니다.", "articles": [], "principle": "실질의 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사법 형사 고발 대상이 아닙니다.", "articles": [], "principle": "실질의 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "글자 수 비례 측정은 거짓입니다.", "articles": [], "principle": "실질의 판단", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "기업이 보유한 다양한 권리(Rights)와 회계상 '자산'의 관계에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 기업이 법적으로 주장할 수 있는 모든 권리는 100% 자동으로 자산의 정의를 충족한다.",
            "② 권리가 자산이 되기 위해서는 그 권리가 다른 당사자가 누리는 경제적효익을 초과하는 효익을 창출할 잠재력이 있고, 그 기업에 의해 통제되어야 한다.",
            "③ 자산이 되기 위한 권리는 무조건 법원의 사법적 공증 서류가 발급되어야만 한다.",
            "④ 권리의 가치가 0원 이하인 경우에는 자산이 아닌 부채로 분류하여 의무로 기재한다.",
            "⑤ 타인도 공동으로 무제한 자유롭게 쓸 수 있는 공공 도로 이용권도 내 자산에 가산한다."
        ],
        "answer": "2",
        "explanation": "② 기업이 가진 모든 권리가 자산은 아닙니다. 자산이 되기 위해선 나를 위해 초과 효익을 낼 잠재력이 있어야 하고, 내가 통제하고 있어야 합니다. 타인도 똑같이 쓰는 공용 권리 등은 내 통제 밖이므로 자산이 아닙니다.\n\n[오답 해설]\n① 통제되지 않는 법적 권리(예: 공용지 도로 점유 등)는 자산이 아닙니다.\n③ 법원 공증이 필수 요건은 아닙니다.\n④ 가치 0원 이하라고 해서 부채(이전 의무)가 자동 성립하진 않습니다.\n⑤ 공용 도로 사용권 등은 내 독점적 통제가 불가능하므로 자산이 될 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "통제되지 않는 권리는 자산이 될 수 없습니다.", "articles": [], "principle": "권리와 자산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "초과 효익 창출 잠재력과 독점적 통제 능력이 수반되는 권리만이 자산 요건을 충족합니다.", "articles": [], "principle": "권리와 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법원 공증 필수 조항이 아닙니다.", "articles": [], "principle": "권리와 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가치 하락 단독으로 부채 분류를 강제하지 않습니다.", "articles": [], "principle": "권리와 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공용 도로 이용권은 통제 불능이므로 내 자산이 아닙니다.", "articles": [], "principle": "권리와 자산", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },

    # =========================================================================
    # L3: 적용 및 시나리오 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s06-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "A사는 주주가치 제고를 위해 자사 주식(자기주식) 10억 원어치를 장내 매입하여 보유하고 있다. 회계부서의 신입사원 김 대리는 이를 '회사가 보유한 투자주식 자산'으로 보고서 자산 항목에 기재하려 한다. 이에 대한 개념체계상의 판단으로 옳은 것은?",
        "options": [
            "① 타당하다. 자기주식도 시장 거래 가치가 존재하므로 자산이다.",
            "② 타당하지 않다. 기업이 스스로에 대해 경제적효익을 요구할 수 없으므로 자기주식은 자산(경제적자원)이 아니며 자본 차감으로 표시해야 한다.",
            "③ 타당하다. 자기주식을 취득할 때 실제 10억 원의 현금 지출이 발생했기 때문에 자산이다.",
            "④ 타당하지 않다. 자기주식 취득은 법적으로 무효 거래에 해당해 즉각 소거해야 하기 때문이다.",
            "⑤ 타당하다. 이사회 결의를 거쳐 3년 이상 장기 보유할 계획을 수립했다면 자산이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 기업은 스스로에 대해 효익을 얻는 권리를 성립시킬 수 없음을 밝힙니다. 따라서 자기주식은 경제적 자원이 될 수 없으며, 자본의 차감 항목으로 반영하여야 합니다.\n\n[오답 해설]\n①, ③, ⑤ 시장 가치 유무, 현금 지출 발생 여부, 이사회 결의나 장기 보유 계획 등이 자기주식을 자산으로 승격시키지 못합니다.\n④ 법적 무효 거래가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "시장 가치 단독으로 자산성을 부여하지 않습니다.", "articles": [], "principle": "자기주식 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "스스로에 대한 권리는 자산이 될 수 없다는 개념체계 요건에 따라 자본 차감 처리가 맞습니다.", "articles": [], "principle": "자기주식 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지출 발생 단독으로 자산이 성립되진 않습니다.", "articles": [], "principle": "자기주식 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정당한 상법 거래이므로 법적 무효가 아닙니다.", "articles": [], "principle": "자기주식 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보유 계획으로 자산 승격이 불가합니다.", "articles": [], "principle": "자기주식 적용", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "B사는 자회사 C사의 지분 100%를 지배하고 있어 연결재무제표를 작성한다. B사는 당기 중 C사가 발행한 회사채 5억 원을 인수하여 보유 중이다. 연결재무제표(모회사와 자회사를 단일 보고기업으로 보는 재무제표) 작성 시, 이 회사채 5억 원을 보고기업의 자산으로 반영하지 않는 개념체계 상의 올바른 이론적 사유는?",
        "options": [
            "① 자회사 회사채는 이자를 지급하지 않는 특수 불법 사채이기 때문이다.",
            "② 연결 실체라는 단일 보고기업 전체 관점에서 볼 때, 실체 내의 구성원(자회사)이 발행하고 다른 구성원(모회사)이 보유한 채무상품은 실질이 자기 자신에 대한 권리이므로 보고기업 전체의 자산이 될 수 없다.",
            "③ 채무상품은 공정가치 평가 대상에서 영구 제외되어 기재 불가하기 때문이다.",
            "④ 자회사 회사채는 모회사가 임의로 소거 소각 처리할 수 없는 법적 독립물이기 때문이다.",
            "⑤ 회사가 5억 원을 인수할 때 자금 유출이 연결 실체 외부로 전혀 발생하지 않았음을 증명하기 위해서다."
        ],
        "answer": "2",
        "explanation": "② 연결재무제표는 모회사와 자회사를 하나의 '단일 보고기업'으로 취급합니다. 보고기업 전체 관점에서는 실체 내부의 상호 거래나 채권/채무 보유는 자기 자신에 대한 권리/의무에 불과하므로 자산과 부채에서 모두 상계 제거해야 합니다.\n\n[오답 해설]\n① 정상적 회사채 발행 거래입니다.\n③, ④, ⑤ 본질적이고 완결성 있는 자산 배격 사유가 아닌 오답 보기들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "합법적 채권 거래입니다.", "articles": [], "principle": "내부거래 제거", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "단일 보고기업(연결실체) 내부에서 상호 보유한 채권채무는 자기 자신에 대한 요소가 되어 연결자산에서 배제(상계)됩니다.", "articles": [], "principle": "내부거래 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치 평가 배제와 무관합니다.", "articles": [], "principle": "내부거래 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법적 독립성 여부가 연결 제거 논리를 깨지 못합니다.", "articles": [], "principle": "내부거래 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 자금 유출 여부 증명이 목적이 아닙니다.", "articles": [], "principle": "내부거래 제거", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "D화학은 공장 운영 중 주변 하천을 정화해야 하는 법률적 강제 의무는 부과되어 있지 않다. 그러나 D사는 오염 발생 시 자발적으로 강 주변을 환경 정화하여 비용을 모두 지불해 온 20년간의 실무 관행이 언론에 널리 공개되어 정화를 유도하고 있다. 당기 말 공장 가동으로 오염이 유발되었을 때 D사가 정화 비용 3억 원에 대해 기말 부채를 인식해야 하는지의 판단과 회계학적 근거는?",
        "options": [
            "① 인식하지 않는다. 법률에 정화 책임이 명시되어 있지 않으므로 법적 의무가 없어 부채가 아니다.",
            "② 인식한다. D사의 관행과 방침의 공개로 인해 정화를 하지 않고 회피할 실제 능력이 없어 '의제의무'가 발생하였으므로 부채이다.",
            "③ 인식하지 않는다. 3억 원의 현금이 기결산일 당일 유출되지 않았으므로 부채가 아니다.",
            "④ 인식한다. 환경 오염 발생은 무조건 징벌적 비용으로 당기 손익에 벌금 부채로 10배 자동 반영해야 하기 때문이다.",
            "⑤ 인식하지 않는다. 주민들의 정식 민원 고발장이 법원에 접수되기 전까지는 부채가 성립하지 않는다."
        ],
        "answer": "2",
        "explanation": "② 명문화된 법률적 강제 의무가 없더라도, 오랜 실무 관행과 공표 사실로 인해 오염 유발 시 책임을 지지 않고 회피할 실제 능력이 없다면 '의제의무'가 형성됩니다. 과거 사건(당기 공장 가동 오염 유발)의 결과로 발생한 현재의 의무이므로 충실히 부채(충당부채 등)로 인식하여야 합니다.\n\n[오답 해설]\n① 법적 의무가 없어도 의제의무로서 부채 인식이 가능합니다.\n③ 기말 현재 의무가 성립했다면 현금 유출 전이라도 부채입니다.\n④ 10배 징벌적 자동 계상 등은 회계 규칙에 없습니다.\n⑤ 민원 접수가 부채 성립의 조건이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "법적 의무 부재만을 이유로 부채 인식을 부정할 수 없습니다.", "articles": [], "principle": "의제의무 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "오랜 관행으로 유발된 회피 불가능한 기대가 있으므로 의제의무(부채)를 인식하는 것이 타당합니다.", "articles": [], "principle": "의제의무 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금 지급 전이라도 부채 인식은 가능합니다(발생주의).", "articles": [], "principle": "의제의무 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "징벌적 10배 처리 등은 회계에 존재하지 않습니다.", "articles": [], "principle": "의제의무 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "민원 접수가 현재의무의 개시 선결 조건이 아닙니다.", "articles": [], "principle": "의제의무 적용", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "E사는 경쟁사로부터 영업 비밀 유출 혐의로 소송을 당해 기말 현재 계류 중이다. 법률 자문 결과 E사가 최종 패소하여 배상금 10억 원을 지급해야 할 유출 가능성은 약 5%로 극히 낮지만 패소할 잠재력은 엄연히 존재한다. 기말 시점 E사의 배상 의무에 대한 부채 정의 부합 여부 판단으로 가장 옳은 것은?",
        "options": [
            "① 부당하다. 유출 가능성이 50% 미만인 거래는 부채의 정의 자체를 전혀 충족할 수 없다.",
            "② 타당하다. 경제적자원을 이전해야 하는 의무의 유출 가능성이 낮더라도, 이전가능성이 존재하므로 부채의 정의를 충족할 수 있다.",
            "③ 부당하다. 소송 배상금은 패소가 100% 확정되는 재판 판결 당일 전까지는 부채의 정의를 어떠한 경우에도 충족하지 못한다.",
            "④ 타당하다. 소송 제기일 즉시 장부의 현금을 10억 원 감액하는 손실 분개를 강제 처리해야 하기 때문이다.",
            "⑤ 부당하다. 배상 금액이 100억 원을 초과할 때에만 개념체계상 예외적으로 부채 정의를 부여한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 부채의 이전 잠재력 요건에 따르면, 자원 이전 의무의 이행 가능성이 낮더라도 의무가 성립된다면 부채의 정의를 충족할 수 있습니다. 단, 인식 기준 충족 여부(측정 신뢰성 등)를 평가하여 장부 본문에 인식할지, 주석에만 공시할지(우발부채 등) 결정할 뿐입니다.\n\n[오답 해설]\n① 가능성 낮음이 부채 정의 탈락을 보증하지 않습니다.\n③ 재판 판결 전이라도 과거 사건으로 인해 현재의무가 성립하면 부채 정의 충족이 가능합니다.\n④ 정의 충족 즉시 강제 현금 감액은 타당치 않은 분식입니다.\n⑤ 금액 규모 요건은 정의 규정과 별개입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "가능성 수준이 부채 정의 성립 여부를 일방 통제하지 않습니다.", "articles": [], "principle": "이전가능성 낮음", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이전 가능성이 낮더라도 의무가 존재하면 부채의 정의를 충족합니다(우발부채 공시 등 연계).", "articles": [], "principle": "이전가능성 낮음", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재판 판결 전에 의무 정의 성립은 가능합니다.", "articles": [], "principle": "이전가능성 낮음", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금 강제 감액은 틀린 분개입니다.", "articles": [], "principle": "이전가능성 낮음", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특정 금액 제한선은 없습니다.", "articles": [], "principle": "이전가능성 낮음", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "F사는 당기 중 유치한 신규 기관투자자 집단으로부터 50억 원의 유상증자 대금을 납입받아 보통주를 발행하였다. F사의 회계담당자는 이 50억 원으로 인해 자산과 자본총액이 크게 늘어났음을 근거로, 당기 '포괄손익계산서' 상의 '수익(Revenue)' 항목에 50억 원을 전액 합산하여 영업수익을 보고했다. 이 처리에 대한 회계학적 적절성 판단으로 옳은 것은?",
        "options": [
            "① 적절하다. 자산의 증가를 초래하여 결과적으로 자본이 늘어났으므로 수익의 정의를 충족한다.",
            "② 부적절하다. 자본 청구권 보유자(주주)의 출자와 관련된 자본의 증가는 수익의 정의에서 명시적으로 제외하기 때문이다.",
            "③ 적절하다. 이사회 주주총회 승인을 거쳐 공정가액으로 납입받았으므로 수익이다.",
            "④ 부적절하다. 50억 원은 전액 부채에 해당하므로 영업부채 수익으로 기재해야 하기 때문이다.",
            "⑤ 적절하다. 투자자의 지분이 증가하면 기업의 영업권 수익도 자동으로 50억 원 증가하기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계상 수익은 자산 증가/부채 감소로 자본 증가를 가져오는 거래이나, 자본청구권 보유자(주주)의 출자와 관련된 부분은 제외합니다. 증자 대금은 주주의 출자이므로 수익이 아닌 자본 잉여금 거래로 분류되어야 합니다.\n\n[오답 해설]\n① 자본 증가 거래이더라도 주주 출자분은 배제됩니다.\n③ 주총 승인 여부로 수익이 되지 않습니다.\n④ 부채가 아닌 자본 거래입니다.\n⑤ 주주 출자 시 영업권 수익이 자동 생성되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "단순 자본 증가 결과만으로 수익이라 할 수 없습니다.", "articles": [], "principle": "주주출자 배제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수익의 정의상 주주(출자자)의 출자는 자본 거래로 분류되어 수익에서 제외됩니다.", "articles": [], "principle": "주주출자 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주총 결의로 수익 요건을 변경할 수 없습니다.", "articles": [], "principle": "주주출자 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자금 납입은 부채가 아닌 자본 증가 거래입니다.", "articles": [], "principle": "주주출자 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업권 가치 자동 상승은 사실이 아닙니다.", "articles": [], "principle": "주주출자 배제", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "G사는 당기 주주총회 결의에 따라 기말 주주들에게 10억 원의 현금배당을 선언하고 즉시 지급하였다. G사의 회계담당자는 자산(현금)이 10억 원 유출되었고 결과적으로 자본총액이 10억 원 감소했음을 근거로, 이를 당기 '비용(Expenses)'에 가산하여 순이익을 감소시켰다. 이 회계처리의 타당성 판단으로 옳은 것은?",
        "options": [
            "① 타당하다. 현금 유출 및 자본 감소는 비용의 정의를 충족한다.",
            "② 타당하지 않다. 자본청구권 보유자(주주)에 대한 분배(배당)는 비용의 정의에서 명시적으로 제외하기 때문이다.",
            "③ 타당하다. 주주들이 수취한 배당소득은 세법상 과세대상 비용에 해당하므로 영업비용 기재가 맞다.",
            "④ 타당하지 않다. 배당금은 부채의 상환 거래에 속하므로 자본 감소가 아닌 부채 감소로만 적어야 하기 때문이다.",
            "⑤ 타당하다. 회계사의 감사 자문 시 주석 기재 대신 본문 비용 반영을 권고받았다면 타당하다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 비용의 정의상 '자본청구권 보유자(주주)에 대한 분배(배당 등)'는 비용에서 명시적으로 제외됩니다. 배당은 이익잉여금(자본)의 직접 차감으로 반영해야 합니다.\n\n[오답 해설]\n① 자본이 줄었더라도 주주에 대한 분배는 비용이 아닙니다.\n③ 주주 개인 소득세 과세 여부는 기업의 비용 분류 요건이 아닙니다.\n④ 주주는 채권자가 아니므로 부채 상환이 아닙니다.\n⑤ 감사인 등의 자의적 권고로 개념체계 정의를 위배할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자본 감소 결과가 있다고 해서 분배가 비용이 되지는 않습니다.", "articles": [], "principle": "주주분배 배제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비용 정의상 주주(보유자)에 대한 배당 등 분배액은 자본 감소 거래일 뿐 비용이 아닙니다.", "articles": [], "principle": "주주분배 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "개인 과세 기준은 기업의 비용 판정 기준이 아닙니다.", "articles": [], "principle": "주주분배 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "배당은 부채 감소가 아닌 자본 감소입니다.", "articles": [], "principle": "주주분배 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사인 권고가 회계 정의를 우선하지 못합니다.", "articles": [], "principle": "주주분배 배제", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "H사는 I사와 내년 중 고정가격으로 구리를 구매하기로 계약하였다. 당기 말 현재 양사 모두 구리 인도나 대금 지급 등 의무 이행을 전혀 개시하지 않았다. 그러나 기말 현재 구리의 시장 가격이 계약 가격보다 대폭 폭락하여, H사가 계약을 유지할 경우 약 3억 원의 확실한 손실(불리한 교환 조건)이 나는 상태가 되었다. H사의 회계적 조치로 가장 옳은 설명은?",
        "options": [
            "① 미이행계약이며, 양사가 아무 의무도 이행하지 않았으므로 기말 시점 어떠한 자산이나 부채도 인식할 수 없다.",
            "② 미이행계약이지만, 기말 현재 교환조건이 불리하여 계약상 권리 의무의 균형이 깨져 부채(충당부채 등)를 보유하게 된다.",
            "③ 미이행계약이 아니므로 기말 시점 즉시 구리 원자재 자산 3억 원을 선계상한다.",
            "④ 판매자 I사에게 위약금을 지불하고 계약을 취소한 사실이 입증될 때에만 자산으로 계상한다.",
            "⑤ 구리 가격 폭락은 일시적이므로 장부 기재를 무조건 누락 은폐한다."
        ],
        "answer": "2",
        "explanation": "② 양사가 의무를 수행하지 않은 미이행계약이지만, 기말 현재 구리 시장 가격 변동 등으로 인해 교환 조건이 H사에 불리하게 변경되었습니다. 이 경우 권리와 의무의 상호의존적 결합에 따라 단일 부채(손실부담계약에 따른 부채)를 인식하게 됩니다.\n\n[오답 해설]\n① 등가 상태의 미이행계약은 인식하지 않으나, 유불리가 깨진 손실부담 상태가 되면 부채를 인식해야 하므로 오답입니다.\n③ 미이행계약 범주에 포함됩니다.\n④ 취소 사실 여부와 무관하게 평가 부채를 잡아야 합니다.\n⑤ 정보 누락 은폐는 위법입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "교환 유불리가 깨졌다면 부채 인식이 요구됩니다.", "articles": [], "principle": "미이행계약의 변동", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "미이행계약의 교환 조건이 당사에 불리하게 변동된 경우 부채 요건이 충족되어 인식해야 합니다.", "articles": [], "principle": "미이행계약의 변동", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "구리 자산을 선계상하는 것은 잘못입니다.", "articles": [], "principle": "미이행계약의 변동", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취소 전이라도 부채 평가가 행해집니다.", "articles": [], "principle": "미이행계약의 변동", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "누락 은폐 주장은 금지됩니다.", "articles": [], "principle": "미이행계약의 변동", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "J사는 특수 용역을 제공하는 우수 엔지니어 5명을 월 1,000만 원씩의 급여로 채용하여 기중에 활발히 기여를 받았다. 용역은 기말 현재 즉시 제공되고 완전히 소비되었다. J사는 이 유능한 인력들의 미래 가치를 환산해 '인적자원자산 1억 원'을 장부에 기록하려 한다. 개념체계에 비추어 이 자산 기재가 부정되는 이유는?",
        "options": [
            "① 엔지니어들이 소유권 양도 동의서에 날인하지 않았기 때문이다.",
            "② 제공받은 용역은 즉시 소비되어 사라지며, 종업원들의 용역 창출 능력을 기업이 독점적으로 '통제'할 수 없기 때문이다.",
            "③ 엔지니어의 몸무게 등 물리적 실체가 측정 불가능하기 때문이다.",
            "④ 인적자원은 은행 담보 대출 계약서 작성이 불가하기 때문이다.",
            "⑤ 회사가 이들에게 제공하는 급여가 시장 평균 시세보다 낮기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계상 일부 용역(종업원 용역 등)은 제공받는 즉시 소비됩니다. 소비된 용역은 더 이상 미래 통제 가능한 현재의 자산이 될 수 없으며, 인적 자원의 이탈 통제권 등도 기업에 독점 귀속될 수 없으므로 자산 인식이 부정되고 비용 처리됩니다.\n\n[오답 해설]\n① 사람에 대한 소유권 양도는 현대 사법 제도상 성립 불가합니다.\n③, ④, ⑤ 물리적 실체 유무, 대출 담보 가능성, 급여 수준 등은 자산 통제 배격의 원천 논리가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "사람을 소유권 대상으로 삼을 수 없습니다.", "articles": [], "principle": "용역 소비와 자산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "즉시 소비되는 용역의 특성과 인적 결합의 통제 불능성 때문에 자산으로 인식할 수 없습니다.", "articles": [], "principle": "용역 소비와 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "물리적 측정 곤란이 원인이 아닙니다.", "articles": [], "principle": "용역 소비와 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "은행 대출 가능 여부가 자산성 요건은 아닙니다.", "articles": [], "principle": "용역 소비와 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "급여 수준과 무관합니다.", "articles": [], "principle": "용역 소비와 자산", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "K사는 신규 백신 개발을 위해 당기 중 연구원 연구비 등으로 20억 원을 현금 지출하였다. 그러나 백신 개발 성공 여부는 기말 현재 매우 불확실하여 자산 요건을 갖추지 못해 당기 '비용'으로 전액 처리하였다. 이 시나리오가 자산의 경제적 효익 창출 잠재력과 관련하여 보여주는 올바른 교훈은?",
        "options": [
            "① 20억 원 지출로도 자산을 취득하지 못했으므로 회계 오류이다.",
            "② 지출의 발생과 자산의 취득은 밀접하게 관련되어 있으나, 양자가 반드시 완벽하게 일치하는 것은 아니다.",
            "③ 지출은 무조건 자산의 취득 가치와 100% 일치해야 하므로 비용 처리는 잘못이다.",
            "④ 불확실성이 높은 지출은 세무서 법인세 감면 대상에서 제외하여야 함을 뜻한다.",
            "⑤ 지출이 자산으로 연결되지 않는 모든 기업은 즉시 파산 대상이 됨을 뜻한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 지출의 발생과 자산 취득이 밀접하나 일치하진 않음을 명시합니다. 효익 창출 잠재력이 불확실하여 자산으로 승격하지 못하고 비용으로 끝나는 지출이 있음을 증명하는 사례입니다.\n\n[오답 해설]\n①, ③ 지출 후 요건 미달로 비용 처리되는 것은 합리적이고 정상적인 회계 처리입니다.\n④, ⑤ 세무 징수나 즉각 파산 여부와는 아무런 인과관계가 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비용 처리는 정상적인 회계 결과입니다.", "articles": [], "principle": "지출과 자산의 불일치", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "지출이 있었더라도 효익 창출 잠재력 요건을 미충족하면 자산이 아닌 비용이 됨을 입증합니다.", "articles": [], "principle": "지출과 자산의 불일치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지출과 자산 가치 일치 주장은 거짓입니다.", "articles": [], "principle": "지출과 자산의 불일치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법인세 공제 여부와 무관한 회계 원칙입니다.", "articles": [], "principle": "지출과 자산의 불일치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기업의 파산 여부와 관련 없습니다.", "articles": [], "principle": "지출과 자산의 불일치", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "L제약은 신약 특허 사용을 독점할 수 있는 10년 법적 특허권을 획득하여, 라이벌 회사들이 이 특허 공식을 사용하여 의약품을 판매해 효익을 취하지 못하게 즉시 배제할 수 있는 권리를 확보하였다. 개념체계 자산 요건 중 '통제(Control)'에 비추어 L제약의 지위를 바르게 분석한 것은?",
        "options": [
            "① 통제를 증명하기 위해 해당 신약의 전 세계 소비량을 100% 임의 조절해야 하므로 통제 불능이다.",
            "② 자원의 사용을 지시하고 그로부터 유입될 효익을 취할 능력이 존재하며, 타인을 배제할 현재의 능력을 가졌으므로 완벽한 통제 상태가 맞다.",
            "③ 특허권은 물리적 형체가 없으므로 어떠한 배제 능력도 가질 수 없어 통제 밖이다.",
            "④ 특허권의 가치는 매일 주식 시장 종가에 비례해 요동치므로 통제할 수 없다.",
            "⑤ 특허 독점권은 헌법상 독과점 금지 위반이므로 자산으로 통제 기재할 수 없다."
        ],
        "answer": "2",
        "explanation": "② 자원의 사용 지시 및 효익 취득 능력과 더불어, '타인이 사용하고 효익을 취하지 못하게 차단(배제)하는 현재의 능력'이 수반되므로 완벽하게 통제 요건을 충족합니다.\n\n[오답 해설]\n① 소비량 100% 강제 통제가 통제의 정의는 아닙니다.\n③ 물리적 형체 부재와 통제 성립 여부는 별개입니다.\n④ 시장 가치의 변동성이 통제 능력을 무효화하지 않습니다.\n⑤ 독과점 금지법 조항에 따라 회계적 자산 정의가 부정되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "소비량 통제 의무는 없습니다.", "articles": [], "principle": "통제 분석 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "효익 취득 및 타인의 사용 차단 능력을 겸비하였으므로 회계상 자원의 통제가 성립합니다.", "articles": [], "principle": "통제 분석 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무형자산도 통제 가능합니다.", "articles": [], "principle": "통제 분석 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가치 변동성과 통제권 보유 여부는 무관합니다.", "articles": [], "principle": "통제 분석 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "독과점 금지 규정으로 자산 분류가 부정되지 않습니다.", "articles": [], "principle": "통제 분석 적용", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "M사는 당기 중 통과된 친환경 신설 입법 법안으로 인해, 내년 중에 공장 굴뚝에 매연 차단 장치를 설치하지 않으면 공장 가동이 금지된다. 기말 현재 M사는 매연 차단 장치를 아직 구매하지 않은 상태이다. 이 상황에 대해 M사의 회계담당자가 기말 부채를 인식해야 하는지의 여부 판단과 가장 정당한 개념체계 상의 사유는?",
        "options": [
            "① 부채를 인식한다. 내년에 강제로 매연 차단 장치를 구매하여 자금 유출이 발생할 것이 확실하기 때문이다.",
            "② 부채를 인식하지 않는다. 굴뚝 장치 미설치 벌금을 법원이 확정 선고하기 전이므로 아직 의무가 없기 때문이다.",
            "③ 부채를 인식하지 않는다. 내년 중 장치를 취득하여 가동해야 하는 의무는 과거 사건의 결과로 존재하게 되는 미래 활동을 회피할 수 없다는 것을 나타낼 뿐, 기결산일 현재의 과거 사건 결과로 존재하는 현재의무가 아니기 때문이다.",
            "④ 부채를 인식한다. 환경 규제 준수는 무조건 기업의 의제의무로 매년 누적 인식해야 하기 때문이다.",
            "⑤ 부채를 인식하지 않는다. 장치의 예상 가격이 10억 원 이하의 소액이어서 중요성 기준에 미달하기 때문이다."
        ],
        "answer": "3",
        "explanation": "③ 부채가 성립하기 위해선 '과거 사건의 결과로 생긴 현재의무'여야 합니다. 굴뚝 장치 미구입으로 인한 내년도 준수 의무는 미래 가동 조건부이며, 기말 현재 장치 구입 계약 등이 체결되어 이전 의무가 발생한 과거 사건 결과물이 아닙니다. 따라서 현재의무가 없어 부채가 아닙니다.\n\n[오답 해설]\n① 미래 확실한 지출 전망만으로 현재의무가 없으면 부채 인식이 불가합니다.\n② 법원 벌금 판결 여부가 본 부채 미인식의 핵심 개념적 사유는 아닙니다.\n④, ⑤ 규제 준수 강제 적용설이나 자의적 금액 기준은 개념체계와 관련 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "미래 자금 유출 확실성만으로 부채가 성립되진 않습니다.", "articles": [], "principle": "현재의무 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법원 확정 판결 여부가 본질이 아닙니다.", "articles": [], "principle": "현재의무 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "법적 규제 준수 계획 등은 미래 조업 시 발생할 미래 사건이므로 기말 현재 과거 결과로 굳어진 현재의무가 아닙니다.", "articles": [], "principle": "현재의무 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "환경 준수 강제 조항이 아닙니다.", "articles": [], "principle": "현재의무 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "장치 가격 수준이 원인이 아닙니다.", "articles": [], "principle": "현재의무 판단", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "N사는 연속된 적자로 인해 기말 자산이 100억 원이고 부채가 120억 원으로 계산되어 잔여지분(자본)총액이 -20억 원의 자본잠식 상태가 되었다. N사의 경영진은 자본이 마이너스가 되는 것은 회계학 정의상 자산 차감 한계에 모순되므로 부채 20억 원을 은폐하여 자본을 0원으로 표시하라고 담당자에게 지시했다. 회계담당자의 정당한 대처와 개념체계 상의 근거는?",
        "options": [
            "① 경영진의 요구대로 부채를 20억 원 지우는 분개를 수행한다. 마이너스 자본 표시가 더 큰 오류이기 때문이다.",
            "② 자본은 자산에서 부채를 차감한 잔여지분으로서 인식 및 측정 방식에 따라 음(-)의 값을 가질 수도 있음을 설명하고 지시를 거부한다.",
            "③ 회사 자산 20억 원을 임의로 공정가치 상승으로 가공 평가하여 자본을 0원으로 맞춘다.",
            "④ 자본잠식이 되면 개념체계상 기업 청산 등기 절차를 무조건 회사가 셀프로 밟아야 함을 고지한다.",
            "⑤ 회계사가 묵인할 경우에 한해서 부채 20억 원을 단기수익으로 둔갑시킨다."
        ],
        "answer": "2",
        "explanation": "② 잔여지분으로서의 자본은 자산과 부채의 상대적 크기에 따라 당연히 음(-)의 값을 가질 수 있습니다. 경영진 요구대로 부채를 은폐하거나 자산을 부풀리는 조작은 심각한 분식회계이므로 거절해야 합니다.\n\n[오답 해설]\n① 부채 은폐는 불법입니다.\n③ 가공 자산 평가는 분식입니다.\n④ 청산 절차는 주총 및 법률 절차지 담당자 고지 사항이 아닙니다.\n⑤ 수익 둔갑 분식은 위법입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "부채 지우기 지시는 명백한 분식 지시입니다.", "articles": [], "principle": "자본의 음의 값 성립", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자본은 자산에서 부채를 뺀 잔여지분이므로 측정 상 음의 값을 가질 수 있어 경영진의 조작 지시를 거절하여야 합니다.", "articles": [], "principle": "자본의 음의 값 성립", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가공 평가는 불법 분식회계입니다.", "articles": [], "principle": "자본의 음의 값 성립", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "셀프 청산 고지 등은 무관합니다.", "articles": [], "principle": "자본의 음의 값 성립", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단기수익 둔갑은 분식입니다.", "articles": [], "principle": "자본의 음의 값 성립", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "O사는 P사로부터 특수 제조 장비를 임차하여 사용하고 있다. 법적 계약 형식은 '임차(Rent)'이지만, 세부 조항상 장비의 사용권 수명 100%를 O사가 단독 지배하며 경쟁사 배제 능력을 가졌고, 반납 의무 및 파손 손실 위험도 O사가 전액 부담하는 경제적 특성을 띤다. O사가 이 거래를 보고할 때 따라야 할 개념체계 상의 대원칙은?",
        "options": [
            "① 임차라는 형식적 서류 명칭이 최우선이므로 자산에 기록하지 않고 단순 임차료 비용으로만 처리한다.",
            "② 형식적 법률 조건이 어떠하든 간에 경제적 권리와 의무의 '실질(Substance)'을 파악해 자산(사용권자산 등)과 부채로 반영한다.",
            "③ 계약서 기재 금액의 100배를 영업권으로 임의 계상한다.",
            "④ 기말 결산 보고 시 임차 장비의 시가를 경쟁사 시가와 합산하여 상계한다.",
            "⑤ 반납 의무가 존재하므로 기말 자산에서 전액 차감하여 음의 자산으로 적는다."
        ],
        "answer": "2",
        "explanation": "② 계약상 권리와 의무를 충실하게 표현(표현충실성)하기 위해서는 형식적 법적 조건뿐 아니라 거래의 경제적 '실질'을 우선하여 보고해야 합니다(실질의 반영). 따라서 사용권자산과 리스부채 등으로 기재함이 타당합니다.\n\n[오답 해설]\n① 실질을 뭉개고 형식만 쫓으면 표현충실성이 저해됩니다.\n③ 영업권의 100배 가공 계상은 분식입니다.\n④ 경쟁사 시가 합산 및 상계는 위법입니다.\n⑤ 음의 자산 단독 처리는 융통성 없는 오류입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "형식에만 치우치면 유용한 정보 보고가 되지 못합니다.", "articles": [], "principle": "실질의 반영 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "형식보다 실질을 반영하여 경제적 통제 하에 있는 사용권자산 및 부채를 공시하는 것이 개념체계에 부합합니다.", "articles": [], "principle": "실질의 반영 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업권 가공 처리는 위법입니다.", "articles": [], "principle": "실질의 반영 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경쟁사 합산은 무관합니다.", "articles": [], "principle": "실질의 반영 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "음의 자산 단독 처리는 오류입니다.", "articles": [], "principle": "실질의 반영 적용", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "Q사는 원재료를 구매하기 위해 계약 상대방인 R사에 대량 주문서를 작성해 송부하였으나, R사는 아직 주문의 접수 승인 여부를 밝히지 않았고 상호 간의 의무 이행도 개시되지 않은 등가 상태이다. 결산일 현재 교환 조건은 시가와 일치하여 유리하지도 불리하지도 않다. 이 미이행계약에 대한 Q사의 회계적 공시 처리로 옳은 것은?",
        "options": [
            "① 계약 금액 상당액을 자산과 부채에 즉시 동시에 계상하여 기재한다.",
            "② 계약 당일이므로 계약이행보증금 예상액만큼을 임의로 단기수익으로 계상한다.",
            "③ 유리하지도 불리하지도 않은 등가 상태의 미이행계약이므로 기결산일 현재 어떠한 자산이나 부채도 인식하지 않는다.",
            "④ 주문 발송 사실을 즉시 법원에 공증 공고하여 사법적 자산으로 등록한다.",
            "⑤ 계약 상대방이 승인을 유보했으므로 이를 비용으로 100% 선 상각 처리한다."
        ],
        "answer": "3",
        "explanation": "③ 미이행계약은 양 당사자가 의무를 이행하지 않은 상태이며, 현재 교환조건이 유리(자산 보유)하거나 불리(부채 보유)하지 않은 등가 상태라면 회계상 자산이나 부채로 인식하지 않는 것이 원칙입니다.\n\n[오답 해설]\n① 등가 미이행 계약은 자산/부채 인식을 보류합니다.\n② 가공 수익을 계상하면 안 됩니다.\n④ 주문서 발송의 법원 등록 조항은 회계와 상관없습니다.\n⑤ 미승인 주문을 선 상각 비용 처리할 근거가 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "동시 계상 강제 적용은 오답입니다.", "articles": [], "principle": "미이행계약 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가공 수익 계상은 오류입니다.", "articles": [], "principle": "미이행계약 처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "양사가 의무를 개시하지 않은 등가 미이행 계약은 결산 시 자산이나 부채로 인식하지 않습니다.", "articles": [], "principle": "미이행계약 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사법적 등록 대상이 아닙니다.", "articles": [], "principle": "미이행계약 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "선 상각 처리할 비용이 발생하지 않았습니다.", "articles": [], "principle": "미이행계약 처리", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "S사는 보유 중인 기계장치에 대해 정밀 대안 측정을 수행할 경우 유용성을 높일 수 있다고 판단했으나, 그 측정치를 신뢰성 있게 도출하기 위해 필요한 외부 컨설팅 비용이 장비 장부금액보다 훨씬 큰 수치임이 확인되어 정밀 검토를 생략하고 기존 측정치를 쓰기로 결정했다. 이 회계적 결정에 적용된 개념체계 상의 정당한 사유는?",
        "options": [
            "① 외부 감사를 무한 회피할 수 있는 감사 면제권 적용",
            "② 정보 제공의 효익이 정보를 제공하고 사용하는 원가를 정당화할 수 있어야 한다는 '원가제약(Cost Constraint)'의 적용",
            "③ 기계장치의 내용연수가 50년을 초과하여 발생한 감가상각 면제권 적용",
            "④ 측정 불확실성이 높을 경우에는 항상 자산 금액을 0원으로 소거해야 한다는 조항의 준수",
            "⑤ 대주주가 비용 처리를 지시하여 발생한 수탁책임 면제권의 준수"
        ],
        "answer": "2",
        "explanation": "② 원가제약은 인식과 측정 등 모든 재무보고 결정에 적용됩니다. 정밀 측정을 통해 얻을 추가 정보의 효익보다 측정 비용(원가)이 과도하게 크다면, 정밀 측정을 생략하는 것이 합리적인 결정이 됩니다.\n\n[오답 해설]\n① 감사 면제권과 무관합니다.\n③ 감가상각은 면제되지 않습니다.\n④ 불확실성이 높다고 강제 0원 소거를 하지는 않습니다.\n⑤ 대주주 지시가 원가제약의 이론적 사유는 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "감사 면제권은 관련 없습니다.", "articles": [], "principle": "원가제약의 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "정보 제공의 추가 효익보다 수반되는 조대 비용이 더 크다면 측정을 보류하거나 생략하는 것이 원가제약에 부합합니다.", "articles": [], "principle": "원가제약의 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각 면제와 무관합니다.", "articles": [], "principle": "원가제약의 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "0원 소거 강제가 아닙니다.", "articles": [], "principle": "원가제약의 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대주주 지시 단독 수탁책임 면제와 무관합니다.", "articles": [], "principle": "원가제약의 적용", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },

    # =========================================================================
    # L4: 다중 분석 및 조합 (8문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s06-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "다음 중 개념체계 상 '자산의 정의와 세부 기준(권리, 잠재력, 통제)'에 관한 보기 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 자산은 과거사건의 결과로 기업이 통제하는 현재의 경제적자원이다.\nㄴ. 권리가 자산이 되기 위해선 그 권리가 다른 당사자가 이용가능한 효익을 초과하는 효익을 창출할 잠재력이 있고, 그 기업에 의해 통제되어야 한다.\nㄷ. 경제적자원은 효익을 창출할 잠재력을 지닌 권리이며, 이 잠재력이 성립하기 위해 효익 창출 가능성이 높거나 확실하여야만 한다.\nㄹ. 지출의 발생과 자산의 취득은 밀접하게 관련되어 있으며 양자는 언제나 항상 완벽히 일치하여야 자산 요건을 충족한다.",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "1",
        "explanation": "① ㄱ, ㄴ 지문은 옳습니다.\nㄷ. 효익 창출 가능성이 낮더라도 잠재력을 지니면 자산이 될 수 있으므로 틀렸습니다.\nㄹ. 지출 발생과 자산 취득은 반드시 일치하는 것은 아니므로 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "옳은 지문 ㄱ과 ㄴ의 조합으로 구성되었습니다.", "articles": [], "principle": "자산 요건 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 거짓입니다.", "articles": [], "principle": "자산 요건 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 거짓입니다.", "articles": [], "principle": "자산 요건 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ, ㄹ은 거짓입니다.", "articles": [], "principle": "자산 요건 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ, ㄹ이 포함되어 오답입니다.", "articles": [], "principle": "자산 요건 다중 판단", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "개념체계 상 '부채의 정의와 세부 기준(의무, 의제의무, 이전)'에 관한 설명으로 옳지 않은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 부채는 과거사건의 결과로 기업이 경제적자원을 이전해야 하는 현재의무이다.\nㄴ. 의무의 대상인 상대방 당사자의 구체적 신원을 명확하게 알지 못한다면 부채로 분류할 수 없다.\nㄷ. 기업이 실무 관행이나 방침과 상충되게 행동할 실제 능력이 없는 경우 의제의무가 성립할 수 있다.\nㄹ. 의무 이행에 따른 자원 이전의 가능성이 극히 낮더라도 부채의 정의를 충족할 여지가 존재한다.",
        "options": [
            "① ㄱ, ㄷ",
            "② ㄴ 단독",
            "③ ㄴ, ㄹ",
            "④ ㄴ, ㄷ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 옳지 않은 설명은 ㄴ 지문 하나뿐입니다.\nㄴ. 의무 상대방의 신원을 꼭 구체적으로 알아야만 부채가 성립하는 것은 아니므로 틀렸습니다.\nㄱ, ㄷ, ㄹ 지문은 모두 부채의 개념적 정의를 잘 설명하는 참 지문들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ, ㄷ은 옳은 설명입니다.", "articles": [], "principle": "부채 요건 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "틀린 지문인 ㄴ 단독이 올바르게 짝지어졌습니다.", "articles": [], "principle": "부채 요건 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 옳은 설명입니다.", "articles": [], "principle": "부채 요건 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 옳은 설명입니다.", "articles": [], "principle": "부채 요건 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ, ㄷ, ㄹ이 포함되어 오답입니다.", "articles": [], "principle": "부채 요건 다중 판단", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "개념체계 상 '자본의 성격 및 자본과 기업가치의 관계'에 관한 다음 지문 중 옳은 지문의 개수를 고른 것은?\n\n[보기]\n- 자본은 기업의 자산에서 모든 부채를 차감한 후의 잔여지분이다.\n- 자본의 총장부금액(총자본)은 독립적으로 직접 측정하여 산정한다.\n- 일반목적재무제표는 기업 가치를 직접 보여주기 위해 고안되지 않았기 때문에 자본 총액과 시가총액은 일치하지 않는 것이 일반적이다.\n- 총자본 및 자본의 개별 항목은 특정 인식이나 측정 방식에 따라 음(-)의 값을 가질 수도 있다.",
        "options": [
            "① 0개",
            "② 1개",
            "③ 2개",
            "④ 3개",
            "⑤ 4개"
        ],
        "answer": "4",
        "explanation": "④ 세 개의 옳은 지문이 존재합니다.\n- 첫 번째, 세 번째, 네 번째 지문은 옳습니다.\n- 두 번째 지문은 자본 총액이 직접 측정되는 것이 아니라 자산에서 부채를 차감하여 간접 산출되므로 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "옳은 지문이 존재합니다.", "articles": [], "principle": "자본 성격 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1개가 아닙니다.", "articles": [], "principle": "자본 성격 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "2개가 아닙니다.", "articles": [], "principle": "자본 성격 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "첫 번째, 세 번째, 네 번째 지문 총 3개가 정당합니다.", "articles": [], "principle": "자본 성격 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "4개가 전부 맞지는 않습니다(두 번째 지문은 거짓).", "articles": [], "principle": "자본 성격 지문 개수", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "개념체계 상 '수익과 비용의 정의 및 자본 변동 요건'에 관한 설명 중 옳은 지문의 개수를 고른 것은?\n\n[보기]\n- 수익과 비용은 기업의 재무성과와 관련된 재무제표 요소이다.\n- 주주(소유주)로부터의 납입 출자 거래는 자본을 증가시키므로 수익에 당연 포함된다.\n- 주주(소유주)에 대한 현금 배당 분배 거래는 자본을 감소시키므로 비용에서 명시적으로 제외된다.\n- 수익은 자산의 증가뿐만 아니라 부채의 감소로도 발생할 수 있으며 비용은 자산 감소 또는 부채 증가로도 발생할 수 있다.",
        "options": [
            "① 0개",
            "② 1개",
            "③ 2개",
            "④ 3개",
            "⑤ 4개"
        ],
        "answer": "4",
        "explanation": "④ 세 개의 옳은 지문이 존재합니다.\n- 첫 번째, 세 번째, 네 번째 지문은 옳습니다.\n- 두 번째 지문은 주주 출자가 수익의 정의에서 명시적으로 제외되므로 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "옳은 지문이 존재합니다.", "articles": [], "principle": "수익비용 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1개가 아닙니다.", "articles": [], "principle": "수익비용 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "2개가 아닙니다.", "articles": [], "principle": "수익비용 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "첫 번째, 세 번째, 네 번째 지문 총 3개가 정당합니다.", "articles": [], "principle": "수익비용 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "모두 정당하진 않습니다(두 번째 지문은 거짓).", "articles": [], "principle": "수익비용 지문 개수", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "개념체계 상 '회계단위, 미이행계약, 계약의 실질 반영'에 관한 설명 중 옳지 않은 것의 개수를 고른 것은?\n\n[보기]\n- 상황에 따라 인식을 위한 회계단위와 측정을 위한 회계단위를 다르게 선택할 수 없다.\n- 미이행계약은 경제적 자원을 교환할 권리와 의무가 결합되어 있으며 이 권리와 의무는 상호의존적이어서 분리할 수 없다.\n- 미이행계약은 교환조건이 유리하면 자산, 불리하면 부채를 구성하게 된다.\n- 계약의 경제적 측면에서 구별할 수 있는 영향을 미치지 않는 조건(실질이 없는 조건)도 재무제표 작성 시 절대 무시해서는 안 된다.",
        "options": [
            "① 0개",
            "② 1개",
            "③ 2개",
            "④ 3개",
            "⑤ 4개"
        ],
        "answer": "3",
        "explanation": "③ 옳지 않은 지문은 총 2개입니다.\n- 첫 번째 지문은 인식과 측정 단위를 다르게 선택하는 것이 허용되므로 틀렸습니다.\n- 네 번째 지문은 실질이 없는 조건은 무시해야 하므로 틀렸습니다.\n- 두 번째, 세 번째 지문은 옳습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "옳지 않은 지문이 존재합니다.", "articles": [], "principle": "계약실질 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1개가 아닙니다.", "articles": [], "principle": "계약실질 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "첫 번째, 네 번째 지문 총 2개가 거짓입니다.", "articles": [], "principle": "계약실질 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "3개가 아닙니다.", "articles": [], "principle": "계약실질 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "4개가 전부 틀린 것은 아닙니다.", "articles": [], "principle": "계약실질 지문 개수", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "자산의 '통제(Control)'와 '권리(Rights)'에 관한 설명 중 옳은 설명의 조합은?\n\n[보기]\nㄱ. 법적 소유권이 없더라도 자원의 사용을 지시하고 효익을 독점할 현재의 능력이 있다면 통제가 성립한다.\nㄴ. 통제에는 다른 당사자가 자원의 사용을 지시하고 이로부터 유입되는 효익을 얻지 못하게 막는 능력이 필수적으로 수반된다.\nㄷ. 보고기업 전체 관점에서 자회사가 발행하고 모회사가 기말 현재 인수한 채무상품은 보고기업의 자산(경제적자원)으로 남는다.\nㄹ. 기업은 스스로에게서 경제적효익을 얻는 권리를 성립시킬 수 있으므로 자기주식은 자산이다.",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "1",
        "explanation": "① ㄱ, ㄴ 지문은 옳습니다.\nㄷ. 연결 실체 내 자회사 발행/모회사 인수 채권은 내부거래 상계 대상이므로 전체 자산에서 빠져 틀렸습니다.\nㄹ. 스스로에 대한 권리는 자산이 될 수 없어 자기주식은 자산이 아니므로 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "옳은 설명 ㄱ, ㄴ의 조합으로 구성되었습니다.", "articles": [], "principle": "자산통제 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 거짓입니다.", "articles": [], "principle": "자산통제 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 거짓입니다.", "articles": [], "principle": "자산통제 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ, ㄹ은 거짓입니다.", "articles": [], "principle": "자산통제 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ, ㄹ이 포함되어 오답입니다.", "articles": [], "principle": "자산통제 조합", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "부채의 '의제의무(Constructive Obligation)'와 '이전가능성(Transfer Potential)' 요건에 관한 다음 설명 중 옳지 않은 조합을 고른 것은?\n\n[보기]\nㄱ. 의제의무가 성립하기 위해선 실무 관행, 공개 경영방침 등으로 인해 기업이 책임을 회피할 실제 능력이 없어야 한다.\nㄴ. 의무 이행에 따른 자원 유입/유출 가능성이 낮다면, 해당 의무는 어떠한 경우에도 부채의 정의를 충족할 수 없다.\nㄷ. 일방 당사자가 부채를 특정 금액으로 인식/측정하면, 상대방도 반드시 동일 금액의 자산으로 상호 인식하여야 한다.\nㄹ. 법률상 환경정화 강제 법령이 없더라도 과거의 잦은 정화 관행과 정화 선언으로 정화를 하지 않고 회피할 능력이 없으면 부채로 분류할 수 있다.",
        "options": [
            "① ㄱ, ㄹ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 옳지 않은 지문은 ㄴ과 ㄷ입니다.\nㄴ. 자원 이전 가능성이 낮더라도 의무가 성립되면 부채 정의 충족이 가능하므로 틀렸습니다.\nㄷ. 일방의 부채 측정이 상대방의 대칭적 자산 인식을 직접 강제하지 않으므로 틀렸습니다.\nㄱ, ㄹ 지문은 옳은 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ, ㄹ은 옳은 설명입니다.", "articles": [], "principle": "부채오류 조합", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "틀린 지문 ㄴ, ㄷ으로 구성되었습니다.", "articles": [], "principle": "부채오류 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ, ㄹ이 포함되어 오답입니다.", "articles": [], "principle": "부채오류 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ이 포함되어 오답입니다.", "articles": [], "principle": "부채오류 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ, ㄹ이 포함되어 오답입니다.", "articles": [], "principle": "부채오류 조합", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "미이행계약(Executory Contract)과 계약 실질에 관한 설명 중 옳은 지문을 모두 고른 것은?\n\n[보기]\nㄱ. 미이행계약은 경제적자원을 교환할 상호의존적인 권리와 의무가 결합되어 있으므로 단일 자산 또는 단일 부채를 구성한다.\nㄴ. 계약 당사자 양쪽 모두 의무를 부분적으로만 똑같은 정도로 수행한 상태는 미이행계약의 범주에 포함되지 않는다.\nㄷ. 미이행계약의 교환 조건이 당사에 유리하게 변동하면 부채를 보유한 것으로 본다.\nㄹ. 계약 조건에 권리와 의무의 실질이 존재하지 않는 조항은 재무보고 시 무시하여야 한다.",
        "options": [
            "① ㄱ, ㄹ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "1",
        "explanation": "① ㄱ, ㄹ 지문이 옳습니다.\nㄴ. 양 당사자가 동일 정도로 의무를 부분 수행한 경우도 미이행계약이므로 틀렸습니다.\nㄷ. 조건이 유리해지면 부채가 아니라 자산을 보유하므로 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "옳은 지문 ㄱ, ㄹ의 조합이 정확하게 도출되었습니다.", "articles": [], "principle": "계약실질 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ, ㄷ은 거짓입니다.", "articles": [], "principle": "계약실질 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ은 거짓입니다.", "articles": [], "principle": "계약실질 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ, ㄷ은 거짓입니다.", "articles": [], "principle": "계약실질 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ, ㄷ이 포함되어 오답입니다.", "articles": [], "principle": "계약실질 조합", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },

    # =========================================================================
    # L5: 심화 분석 (2문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s06-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "자산의 정의 요건 중 법적 소유권(Legal Ownership)과 개념체계의 통제(Control) 개념이 가지는 이론적 괴리와 실무적 유용성에 관한 분석으로 가장 타당한 것은?",
        "options": [
            "① 법적 소유권이 없는 모든 거래는 장부 왜곡이 불가능하므로, 리스 거래 시 사용권자산을 잡는 행위는 개념체계에 전면 배치되는 오류이다.",
            "② 개념체계는 자산의 실질적 지배력인 '통제'를 법적 소유권보다 우선하여 정의함으로써, 법적 소유권이 없는 임차 자산(리스이용자 자산)이나 양도 후 환매 조건부 자산거래 등에서 형식보다는 경제적 실질(Substance)을 반영한 재무보고가 가능하도록 이론적 정당성을 부여한다.",
            "③ 법적 소유권이 있어야만 미래의 예측 가치가 보장되므로, 개념체계는 사실상 통제 요건을 법적 소유권의 동의어로만 한정 축소 적용하고 있다.",
            "④ 통제 개념은 자산의 물리적 실체 여부만을 판단할 뿐, 법적 소유 여부와는 아무런 논리적 인과관계를 지니지 않는다.",
            "⑤ 법적 소유권 없이 통제 능력을 주장하는 모든 기업은 즉시 사법 당국의 법정 구속 대상이 됨을 입증한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 자산의 핵심 성격으로 '통제'를 설정하고, 법적 소유권이 없더라도 경제적 실질에 의해 자산 사용을 통제하고 있다면 자산으로 잡도록 허용합니다. 이는 금융리스 자산의 사용권자산 인식, 매출채권 양도 시 통제 이전 여부 판단 등 형식보다 실질을 중시하는 현대 회계학의 가장 중요한 이론적 토대를 형성합니다.\n\n[오답 해설]\n① 리스 사용권자산 인식은 개념체계와 기준서에 정확히 부합합니다.\n③ 통제와 소유권은 구별되며 동의어가 아닙니다.\n④ 통제는 물리적 실체 여부를 판단하는 개념이 아니라 자원의 사용 지시 및 배제 능력입니다.\n⑤ 법적 구속 대상 등 사법 규제와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "사용권자산 인식은 개념체계상 지극히 정당한 실무입니다.", "articles": [], "principle": "소유권과 통제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "소유권보다 통제를 중시함으로써 경제적 실질을 충실히 보고할 수 있는 이론적 기반을 제공합니다.", "articles": [], "principle": "소유권과 통제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "통제와 소유권을 동의어로 보지 않습니다.", "articles": [], "principle": "소유권과 통제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "물리적 형태 판단 규정이 아닙니다.", "articles": [], "principle": "소유권과 통제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사법 형벌 위반과 무관합니다.", "articles": [], "principle": "소유권과 통제", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s06-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "개념체계 상 총자본(Total Equity)의 장부금액이 기업의 실제 '시가총액(Market Capitalization)'이나 '기업전체 즉시 매각 처분가치' 등과 필연적이고 상시적으로 불일치할 수밖에 없는 회계 시스템적 요인에 대한 설명으로 가장 옳지 않은 것은?",
        "options": [
            "① 일반목적재무제표는 보고기업의 내재 가치를 직접 계산하여 보여주기 위해 설계된 보고서가 아니기 때문이다.",
            "② 재무상태표의 자산과 부채 중 상당수는 역사적 원가 등 시가 변동을 직접 추적 반영하지 않는 다양한 측정 기준의 혼합으로 계상되어 자본 총액과의 차이를 낳기 때문이다.",
            "③ 내부에서 창출한 우수한 브랜드 가치, 인적 역량, 정교한 마케팅 망 등 기업의 생존 가치를 높여주는 많은 핵심 무형자산들이 회계 장부에 자산으로 인식되지 못하고 누락되기 때문이다.",
            "④ 자본의 장부총액은 자산에서 부채를 차감한 후 계산상 도출되는 수치일 뿐, 시가총액 마감 데이터와 1원 단위까지 완벽하게 강제 보정 일치시키는 분개 로직이 회계 제도로 금지되어 있기 때문이다.",
            "⑤ 회계담당자가 시가총액 정보를 실시간으로 입수하여 장부에 미인식 영업권 가치로 정기 입력하는 법적 의무를 고의로 태만히 불이행했기 때문이다."
        ],
        "answer": "5",
        "explanation": "⑤ 자본의 장부액과 시가총액의 불일치는 회계담당자의 근무 태만이나 의무 불이행이 아닙니다. 재무보고의 고유한 한계 및 개념체계의 목적(기업가치 직접 미제시), 그리고 내부창출 무형자산(영업권 포함)의 인식 제한 규정 등에 따른 회계 시스템의 필연적인 결과입니다.\n\n[오답 해설]\n①, ②, ③, ④ 모두 장부자본과 시장 가치가 괴리될 수밖에 없는 개념체계 상의 정당한 이유를 분석 설명하고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재무보고서의 한계와 고안 목적에 관한 서술은 참입니다.", "articles": [], "principle": "자본과 시가총액 괴리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정 기준의 혼합(역사적 원가 등)이 불일치의 원인임은 참입니다.", "articles": [], "principle": "자본과 시가총액 괴리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "내부창출 영업권의 미인식이 불일치의 주요 원인임은 참입니다.", "articles": [], "principle": "자본과 시가총액 괴리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본은 직접 측정하지 않고 차감 유도되는 수치라는 설명은 참입니다.", "articles": [], "principle": "자본과 시가총액 괴리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "시가총액 차이 반영을 위한 강제 영업권 실시간 입력 의무 조항 등은 회계 제상 전혀 존재하지 않으므로 담당자의 태만 설은 완전한 오류입니다.", "articles": [], "principle": "자본과 시가총액 괴리", "case": {"holding": "", "no": None}}
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
                "item": "6절 재무제표의 요소"
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
