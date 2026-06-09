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
        "id": "practice-accounting-ch01s09-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "IFRS 제1113호상 '공정가치(Fair Value)'의 공식 정의로 가장 옳은 것은?",
        "options": [
            "① 거래처와 구두 합의를 통해 임의로 산정한 미래 기대 매출의 현재가치",
            "② 측정일에 시장참전자 사이의 정상거래에서 자산을 매도할 때 받거나 부채를 이전할 때 지급하게 될 가격",
            "③ 자산의 취득에 소요된 실제 대금과 취득세, 등록세 등 모든 역사적 비용의 합계",
            "④ 기업이 청산할 때 채권자들에게 비례적으로 우선 배분해야 하는 청산 배당 가치",
            "⑤ 회사가 자산을 보증하기 위해 금융회사에 지급한 대출 수수료와 이자율의 가중평균"
        ],
        "answer": "2",
        "explanation": "② IFRS 제1113호상 공정가치는 '측정일에 시장참전자 사이의 정상거래에서 자산을 매도할 때 받거나 부채를 이전할 때 지급하게 될 가격'으로 정의됩니다. 이는 시장에 근거한 측정치이며 유출가격(Exit Price)입니다.\n\n[오답 해설]\n① 미래 기대 매출은 사용가치나 주관적 가치에 가깝고 공정가치의 정의가 아닙니다.\n③ 이는 역사적 원가(Historical Cost)의 정의입니다.\n④ 청산 배당 가치는 공정가치 정의가 아닙니다.\n⑤ 이자율 가중평균은 조달 원가와 관련된 수치입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "미래 기대 매출 현가는 공정가치의 정의가 아닙니다.", "articles": [], "principle": "공정가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치는 측정일에 시장참전자 사이의 정상거래 하의 자산 매도/부채 이전 유출가격입니다.", "articles": [], "principle": "공정가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지급 대금과 거래원가 합계는 역사적 원가입니다.", "articles": [], "principle": "공정가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "청산 분배 가치는 공정가치의 정의와 거리가 멉니다.", "articles": [], "principle": "공정가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대출 수수료 등은 자금 조달 조건입니다.", "articles": [], "principle": "공정가치의 정의", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "공정가치 측정 기준서상 거래가 이루어지는 대상 시장 중 '주된 시장(Principal Market)'의 정의로 가장 올바른 것은?",
        "options": [
            "① 해당 자산이나 부채의 거래 빈도와 거래량이 가장 많은 시장",
            "② 거래원가와 운송원가를 차감한 후의 수취액이 가장 극대화되는 시장",
            "③ 보고기업의 본사 건물이 위치한 행정 구역 내의 유일한 전통 도매시장",
            "④ 대표이사가 개인적으로 가장 선호하여 구두 계약을 자주 체결하는 시장",
            "⑤ 세법상 법인세 감면 세율이 가장 높게 적용되는 조세 피난처 시장"
        ],
        "answer": "1",
        "explanation": "① 주된 시장은 자산이나 부채의 거래 빈도와 거래량이 가장 많은 시장으로 정의됩니다.\n\n[오답 해설]\n② 이는 가장 유리한 시장(Most Advantageous Market)의 정의입니다.\n③ 행정 구역이나 특정 시장 유형으로 정의되지 않습니다.\n④ 대표이사의 개인적 선호는 회계적 시장 결정 요건이 아닙니다.\n⑤ 조세 혜택 수준은 주된 시장 판단 요건이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "주된 시장은 해당 자산이나 부채의 거래 빈도와 거래량이 최대인 시장입니다.", "articles": [], "principle": "주된 시장의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래액 극대화 시장은 가장 유리한 시장에 해당합니다.", "articles": [], "principle": "주된 시장의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특정 지리적 명소 등으로 국한되지 않습니다.", "articles": [], "principle": "주된 시장의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대표의 사적 선호도는 회계적 요건이 아닙니다.", "articles": [], "principle": "주된 시장의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 상 혜택이 주된 시장 거래량 판단 기준이 될 수 없습니다.", "articles": [], "principle": "주된 시장의 정의", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "공정가치 측정 기준서상 주된 시장이 없는 경우 적용하는 '가장 유리한 시장(Most Advantageous Market)'의 정의로 가장 올바른 것은?",
        "options": [
            "① 거래량이 가장 많아 시세 조작의 위험이 원천 배제된 투명한 시장",
            "② 거래원가와 운송원가를 고려하여 자산을 매도할 때 받게 될 금액을 최대화하거나 부채를 이전할 때 지급할 금액을 최소화하는 시장",
            "③ 보고기업이 매달 고정적으로 제품을 독점 납품하여 경쟁 우위를 가지는 시장",
            "④ 금융감독원에 비밀 거래로 신고하여 대외 공시의 제약을 받지 않는 시장",
            "⑤ 회사의 자산 가치를 10배로 증액하여 공표할 수 있도록 허가받은 가상의 시장"
        ],
        "answer": "2",
        "explanation": "② 가장 유리한 시장은 자산이나 부채의 주된 시장이 없는 경우에 적용되며, 거래원가와 운송원가를 고려하여 자산 매도 수취액을 극대화하거나 부채 이전 지급액을 극소화하는 시장을 뜻합니다.\n\n[오답 해설]\n① 이는 거래량 기준 시장(주된 시장 성격)에 가까우며 가장 유리한 시장의 순매득액 기준 정의가 아닙니다.\n③ 독점 납품 등 실무상 유리함과 개념상 정의는 구분됩니다.\n④, ⑤는 회계 기준과 하등의 관련이 없는 오진술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "거래량 위주의 시장은 주된 시장의 설명에 가깝습니다.", "articles": [], "principle": "가장 유리한 시장 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가장 유리한 시장은 원가들을 고려해 매도 시 유입액 최대화, 부채 이행 시 유출액 최소화가 달성되는 시장입니다.", "articles": [], "principle": "가장 유리한 시장 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영 상 독점 구조 시장만을 지칭하지 않습니다.", "articles": [], "principle": "가장 유리한 시장 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비밀 거래 시장 등은 존재하지 않습니다.", "articles": [], "principle": "가장 유리한 시장 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가상의 증액 시장 설명은 불법 오류입니다.", "articles": [], "principle": "가장 유리한 시장 정의", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "공정가치 측정 기준서상 보고기업이 자산을 매각하지 않고 계속 보유하려는 의도나 부채를 조기 결제하지 않으려는 의도가 공정가치 측정에 미치는 영향으로 가장 옳은 것은?",
        "options": [
            "① 보유하려는 의도가 강할수록 공정가치는 매달 10%씩 기계적으로 할증 평가된다.",
            "② 공정가치는 시장에 근거한 측정치이므로 기업이 자산을 계속 보유하거나 결제하려는 의도는 공정가치 측정 시 관련이 없다(배제된다).",
            "③ 보유 의도가 있으면 공정가치 평가 보고 의무 자체가 영구 면제된다.",
            "④ 보유 의도가 확실할 때만 역사적 원가를 취득원가의 100배로 증액 계상한다.",
            "⑤ 결제하지 않으려는 의도가 있으면 부채를 장부에서 즉시 제거하고 영업 외 수익으로 돌린다."
        ],
        "answer": "2",
        "explanation": "② 공정가치는 시장참전자 관점의 객관적인 시장 기준 측정치이므로, 보고기업이 가진 특정 자산의 보유 의도나 결제 의도 등 기업 특유의 계획은 가격(공정가치) 측정에 하등의 영향을 미치지 않고 무시됩니다.\n\n[오답 해설]\n① 자의적인 10% 할증 공식은 없습니다.\n③ 보유 의도가 있어도 공정가치 적용 자산이라면 평가는 수행되어야 합니다.\n④ 원가의 100배 증액 계상은 불가능한 부정 행위입니다.\n⑤ 이행 의사가 없다고 의무 부채를 자의로 제거하고 수익 처리할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "의도에 따른 임의 할증은 허용되지 않습니다.", "articles": [], "principle": "기업의 의도와 공정가치", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치는 기업특유가치가 아니므로 기업의 사적 의도(보유/결제 등)는 가치 평가에 반영되지 않습니다.", "articles": [], "principle": "기업의 의도와 공정가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평가 면제 혜택과는 무관합니다.", "articles": [], "principle": "기업의 의도와 공정가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "100배 증액 등은 분식 조장 서술입니다.", "articles": [], "principle": "기업의 의도와 공정가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의무 미이행 다짐만으로 부채를 제거할 수는 없습니다.", "articles": [], "principle": "기업의 의도와 공정가치", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "공정가치 측정 기준서상 비금융자산(Non-financial Assets)의 공정가치 측정 시 적용하는 가치 평가의 극대화 전제 조건을 지칭하는 용어는?",
        "options": [
            "① 역사적 대체원가(Historical Replacement Cost)",
            "② 보수적 청산가치(Conservative Liquidation Value)",
            "③ 최고 최선 사용(Highest and Best Use)",
            "④ 최소 비용 이행(Minimum Cost Fulfilment)",
            "⑤ 주관적 시너지 사용(Subjective Synergy Use)"
        ],
        "answer": "3",
        "explanation": "③ 비금융자산의 공정가치는 시장참전자가 그 자산을 '최고 최선으로 사용(Highest and Best Use)'하여 경제적 효익을 극대화할 수 있는 능력을 고려하여 측정됩니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 비금융자산 공정가치의 핵심 전제 요건 명칭이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "역사적 원가는 공정가치의 극대화 전제가 아닙니다.", "articles": [], "principle": "최고 최선의 사용 용어", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보수적 청산 가치 개념이 아닙니다.", "articles": [], "principle": "최고 최선의 사용 용어", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비금융자산의 공정가치는 시장참전자 관점에서의 최고 최선 사용(Highest and Best Use)에 기초해 평가됩니다.", "articles": [], "principle": "최고 최선의 사용 용어", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "최소 비용 이행은 부채 관련 성격의 용어입니다.", "articles": [], "principle": "최고 최선의 사용 용어", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주관적 시너지는 공정가치에 배제됩니다.", "articles": [], "principle": "최고 최선의 사용 용어", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "공정가치 측정 기준서상 부채(Liability)의 공정가치를 측정할 때 반드시 함께 반영되어 가치에 영향을 주는 위험 요소를 지칭하는 공식 용어는?",
        "options": [
            "① 환율 변동 위험(Foreign Exchange Risk)",
            "② 화재 재해 위험(Fire Hazard Risk)",
            "③ 불이행위험(Non-performance Risk)",
            "④ 인플레이션 위험(Inflation Risk)",
            "⑤ 담보 권리 상실 위험(Collateral Loss Risk)"
        ],
        "answer": "3",
        "explanation": "③ 부채의 공정가치 측정은 '불이행위험(Non-performance Risk)'의 효과를 직접 반영합니다. 불이행위험은 보고기업 자신의 신용위험(자기신용위험)을 포괄합니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 부채 공정가치가 지칭하는 통합적인 불이행위험의 공식 명칭과 다릅니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "환율 위험은 금융 위험의 일종일 뿐입니다.", "articles": [], "principle": "불이행위험의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "물리적 재해 위험 단독을 뜻하지 않습니다.", "articles": [], "principle": "불이행위험의 의의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부채의 공정가치 측정은 자기신용위험을 포함하는 불이행위험(Non-performance Risk)을 반영합니다.", "articles": [], "principle": "불이행위험의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "물가변동 위험이 공식 위험 지칭이 아닙니다.", "articles": [], "principle": "불이행위험의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "담보권리 상실 위험 명칭은 부채 공정가치 판단 공식용어가 아닙니다.", "articles": [], "principle": "불이행위험의 의의", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "공정가치 측정 및 관련 공시에서 일관성과 비교가능성을 높이기 위해, 투입변수를 3수준으로 분류하여 정해 둔 체계를 지칭하는 용어는?",
        "options": [
            "① 회계오류 서열체계",
            "② 재무상태표 서열체계",
            "③ 공정가치서열체계(Fair Value Hierarchy)",
            "④ 복식부기 서열체계",
            "⑤ 세법공제 서열체계"
        ],
        "answer": "3",
        "explanation": "③ 공정가치 측정치와 그 공시의 품질 및 신뢰성 구분을 유도하기 위해 투입변수의 등급을 3수준으로 분류해 둔 체계를 '공정가치서열체계(Fair Value Hierarchy)'라고 합니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 회계 용어가 아니거나 가공의 명칭들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "가공의 서열체계 명칭입니다.", "articles": [], "principle": "공정가치서열체계 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재무상태표의 공식 서열체계가 아닙니다.", "articles": [], "principle": "공정가치서열체계 의의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "IFRS 기준서 상 투입변수 신뢰성을 3등급으로 나눈 공식 명칭은 공정가치서열체계(Fair Value Hierarchy)입니다.", "articles": [], "principle": "공정가치서열체계 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "복식부기에 우선등급 서열체계는 없습니다.", "articles": [], "principle": "공정가치서열체계 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법과 하등 관련 없는 공시 품질 지표입니다.", "articles": [], "principle": "공정가치서열체계 의의", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "공정가치서열체계에서 가장 높은 순위를 부여하는 '수준 1의 투입변수(Level 1 Inputs)'의 정의로 가장 올바른 것은?",
        "options": [
            "① 기업 내부 직원들의 근무 태도 평가 점수",
            "② 측정일에 동일한 자산이나 부채에 대한 접근할 수 있는 활성시장의 (조정하지 않은) 공시가격",
            "③ 측정기법을 통해 내부적으로 가공하여 추정한 가치의 예상 현재가치",
            "④ 금융자산 양도자가 상대방에게 수령하겠다고 구두 약속한 기대 이자율",
            "⑤ 관행적으로 세무신고 시 제출하는 토지 공시지가의 역사적 최초액"
        ],
        "answer": "2",
        "explanation": "② 수준 1 투입변수는 공정가치서열체계상 최우선 순위가 부여되며, 측정일에 동일한 자산/부채에 대해 접근 가능한 활성시장의 (조정하지 않은) 공시가격으로 정의됩니다.\n\n[오답 해설]\n① 직원 근무 태도는 공정가치 변수가 아닙니다.\n③ 이는 수준 3(관측불가능 투입변수 포함) 등으로 갈 수 있는 추정치입니다.\n④ 구두 약정율은 활성시장 공시가격이 아닙니다.\n⑤ 역사적 공시지가는 수준 1 정의와 어긋납니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "직원 평가는 회계 가치 평가 투입변수가 아닙니다.", "articles": [], "principle": "수준 1 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수준 1 변수는 활성시장에서 관측되는 동일 자산·부채의 조정되지 않은 공시가격입니다.", "articles": [], "principle": "수준 1 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "내부 추정 가공액은 수준 3 등에 분류됩니다.", "articles": [], "principle": "수준 1 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "구두 이자율 약정은 공시가격이 아닙니다.", "articles": [], "principle": "수준 1 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과거 공시지가는 갱신된 활성시장 공시가격의 요건을 충족하지 못합니다.", "articles": [], "principle": "수준 1 투입변수 정의", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "공정가치서열체계에서 가장 낮은 순위를 부여하는 '수준 3의 투입변수(Level 3 Inputs)'의 본질적 특성으로 가장 올바른 것은?",
        "options": [
            "① 시장에서 실시간으로 완벽하게 확인되는 고정된 공시가격",
            "② 자산이나 부채에 대한 관측할 수 없는 투입변수(Unobservable Inputs)",
            "③ 정부 세무서 공무원이 단독으로 정하여 기업에 통보해 주는 강제 가격",
            "④ 금융기관이 이자를 전액 지급한 후 회수 불가능하다고 공인한 대손액",
            "⑤ 회사의 자본금을 즉시 상환할 때 사용되는 임의의 분개 잔액"
        ],
        "answer": "2",
        "explanation": "② 수준 3 투입변수는 자산이나 부채에 대한 관측할 수 없는 투입변수(Unobservable Inputs)를 의미하며, 시장참여자가 가격을 결정할 때 사용할 가정에 대한 보고기업 자신의 자체 가정을 포함하게 되므로 우선순위가 가장 낮습니다.\n\n[오답 해설]\n① 이는 수준 1 투입변수의 설명입니다.\n③, ④, ⑤는 수준 3 투입변수의 정의나 특성이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "관측 가격은 수준 1 또는 수준 2에 해당합니다.", "articles": [], "principle": "수준 3 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수준 3 투입변수는 시장 관측 정보가 불비할 때 사용하는 기업 자체의 관측불가능 투입변수를 말합니다.", "articles": [], "principle": "수준 3 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정부 통보 가격은 수준 3 정의가 아닙니다.", "articles": [], "principle": "수준 3 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손액 수치는 본 정의와 무관합니다.", "articles": [], "principle": "수준 3 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 자본 분개액은 투입변수 개념이 아닙니다.", "articles": [], "principle": "수준 3 투입변수 정의", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "공정가치 측정 시 널리 사용하는 대표적인 세 가지 가치평가기법(Valuation Approaches)에 해당하지 않는 것은?",
        "options": [
            "① 시장접근법(Market Approach)",
            "② 원가접근법(Cost Approach)",
            "③ 이익접근법(Income Approach)",
            "④ 주관적평판접근법(Reputation Approach)",
            "⑤ 이상의 ①, ②, ③ 모두 널리 사용하는 세 가지 가치평가기법에 속한다."
        ],
        "answer": "4",
        "explanation": "④ 공정가치 측정 시 사용하는 세 가지 가치평가기법은 '시장접근법', '원가접근법', '이익접근법'입니다. 주관적평판접근법이라는 기법은 공식 기법 분류에 존재하지 않습니다.\n\n[오답 해설]\n①, ②, ③은 기준서가 예시하여 실무 상 널리 사용되는 공인 가치평가 세 가지 접근법입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "시장접근법은 공식 세 가지 기법 중 하나입니다.", "articles": [], "principle": "평가기법의 종류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가접근법은 공식 세 가지 기법 중 하나입니다.", "articles": [], "principle": "평가기법의 종류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익접근법은 공식 세 가지 기법 중 하나입니다.", "articles": [], "principle": "평가기법의 종류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "주관적 평판을 통한 자의적 평가는 회계 공인 3대 가치평가기법에 들어가지 않습니다.", "articles": [], "principle": "평가기법의 종류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "④가 오답이므로 틀린 보기입니다.", "articles": [], "principle": "평가기법의 종류", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },

    # =========================================================================
    # L2: 이해 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s09-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "공정가치 측정 시, 특정 자산이나 부채가 이전·양도되는 거래 시장의 우선순위 적용 규칙에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 가장 유리한 시장을 항상 최우선 적용하고, 주된 시장은 완전히 무시한다.",
            "② 주된 시장(Principal Market)이 있는 경우에는 그 시장의 가격을 우선 적용하며, 주된 시장이 없는 경우에 한하여 가장 유리한 시장의 가격을 적용한다.",
            "③ 보고기업의 소재국 중앙은행이 매일 아침 지정해 주는 가상 외환 시장만을 강제 적용한다.",
            "④ 두 시장의 평균가격을 산정한 후 무조건 자산의 원가를 차감하는 방식을 쓴다.",
            "⑤ 거래소 폐쇄 결의가 내려진 휴면 시장의 마감가를 10년 동안 승계한다."
        ],
        "answer": "2",
        "explanation": "② 공정가치 측정은 자산 매도/부채 이전 거래가 자산·부채의 '주된 시장'에서 이루어지는 것으로 우선 가정합니다. 단, 주된 시장이 존재하지 않는 예외적 상황에만 차선책으로 '가장 유리한 시장'의 가격을 채택합니다.\n\n[오답 해설]\n① 주된 시장을 제치고 유리한 시장을 우선시하지 않습니다.\n③ 중앙은행 고정 지정 시장이 아닙니다.\n④ 두 시장의 평균 적용은 회계상 근거가 없습니다.\n⑤ 휴면 시장의 가격을 임의 승계할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "가장 유리한 시장보다 주된 시장이 우선적으로 적용되어야 합니다.", "articles": [], "principle": "주된 시장 우선 원칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "거래 빈도/부피가 최대인 주된 시장을 먼저 적용하고, 그것이 없을 때에만 수취액 극대화 목적의 가장 유리한 시장을 씁니다.", "articles": [], "principle": "주된 시장 우선 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중앙은행 고정 시장 기준이 아닙니다.", "articles": [], "principle": "주된 시장 우선 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평균 가격 유도 산식은 성립하지 않습니다.", "articles": [], "principle": "주된 시장 우선 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "폐쇄 시장 가격의 영구 승계는 불가합니다.", "articles": [], "principle": "주된 시장 우선 원칙", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "공정가치 측정 시 자산의 매도 또는 부채 이전 가격에 대한 '거래원가(Transaction Cost)'의 직접적인 조정 여부에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 거래원가는 자산 매도금액을 직접 차감하여 공정가치를 결정하므로 언제나 기말 공정가치에서 삭감 조정된다.",
            "② 주된 시장(또는 가장 유리한 시장)의 거래가격에 거래원가를 직접 조정하지 아니한다.",
            "③ 거래원가는 시장 참여자의 중개 수수료이므로 전액 사외 유보한 채 자산가액에 2배로 가산한다.",
            "④ 거래원가의 변동이 심할 경우에는 금융감독원장의 사전 결재를 맡아 공정가치를 강제 변조한다.",
            "⑤ 거래원가는 부가가치세법 규정에 부합하는 수준으로만 자산 가치에 임의로 포함시킨다."
        ],
        "answer": "2",
        "explanation": "② 공정가치 기준서상 공정가치는 거래원가로 인해 증가하거나 감소하지 않는 고유의 성격을 가집니다. 따라서 공정가치를 측정하기 위해 사용하는 거래가격 자체에 거래원가를 직접 가산하거나 차감 조정하지 않습니다.\n\n[오답 해설]\n① 거래원가는 공정가치에서 차감(조정)하지 않습니다. (다만 순공정가치를 구할 때는 차감합니다.)\n③, ④, ⑤는 거래원가의 회계 처리와 무관한 가공 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "거래원가를 직접 빼서 공정가치 자체를 차감하지 않습니다.", "articles": [], "principle": "공정가치와 거래원가 관계", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치 측정 시에는 해당 주된/유리한 시장 가격에 거래원가를 별도로 차감/조정하지 않는 것이 원칙입니다.", "articles": [], "principle": "공정가치와 거래원가 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "2배 가산 등은 근거가 없습니다.", "articles": [], "principle": "공정가치와 거래원가 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금감원 결재를 통한 임의 변조는 불가합니다.", "articles": [], "principle": "공정가치와 거래원가 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부가세법에 따라 회계 상 공정가치 조정을 임의로 결정하지 않습니다.", "articles": [], "principle": "공정가치와 거래원가 관계", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "공정가치 측정 시, 자산이 존재하는 현재 위치에서 대상 거래 시장까지 자산을 이전하는 데 소요되는 '운송원가(Transportation Cost)'의 회계 처리 및 조정 규칙으로 가장 옳은 것은?",
        "options": [
            "① 운송원가는 가격 결정 요인이 아니므로 어떠한 상황에서도 공정가치에서 공제하지 않는다.",
            "② 위치가 자산의 특성에 해당한다면, 현재의 위치에서 주된(또는 가장 유리한) 시장까지 자산을 운송하는 데에 드는 원가(운송원가)만큼 거래 가격을 조정(차감)하여 공정가치를 산정한다.",
            "③ 운송원가를 자산 가액에 50%를 임의 가산하고 나머지는 감가상각 누계액으로 적립한다.",
            "④ 운송원가가 발생할 때마다 전액 당기순이익 가산 항목(영업수익)으로 대체 처리한다.",
            "⑤ 운송회사의 자본을 보고기업의 자본 총량에 합산 표시하여 운송비 조정을 생략한다."
        ],
        "answer": "2",
        "explanation": "② 운송원가는 자산의 위치가 특성에 귀속되는 경우(예: 특정 창고에 적재된 구리 등 일반원자재 등), 주된 시장으로 가져가기 위해 불가피한 위치 보정 비용이므로 이를 거래가격에서 **차감(조정)**하여 공정가치를 산정하게 됩니다. (즉, 운송원가는 공정가치 자체를 감소시키는 직접 차감 항목입니다.)\n\n[오답 해설]\n① 위치 특성 시 운송원가를 차감 조정하므로 공제 불가는 틀렸습니다.\n③, ④, ⑤는 회계 기준에 어긋나는 설명들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "위치적 특성을 가질 경우 운송원가는 공정가치 자체에서 차감 조정되므로 공제 불가는 오답입니다.", "articles": [], "principle": "운송원가의 공정가치 조정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산의 물리적 위치가 자산 특성에 해당하면, 시장까지의 운송 비용은 거래가격에서 차감하여 공정가치를 결정합니다.", "articles": [], "principle": "운송원가의 공정가치 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각 누계 적립 등은 불가능한 분개 유도입니다.", "articles": [], "principle": "운송원가의 공정가치 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "운송 지출을 자사 영업수익으로 대체할 수는 없습니다.", "articles": [], "principle": "운송원가의 공정가치 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "타사 자본의 합산 표시는 결합 회계 위반입니다.", "articles": [], "principle": "운송원가의 공정가치 조정", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "공정가치 측정 시 주된 시장이 없어 '가장 유리한 시장'을 비교 선택해야 할 때, 각 시장들의 우위를 판단하기 위한 비교 잣대로 사용하는 공식 수치는?",
        "options": [
            "① 거래원가와 운송원가를 모두 가산한 역사적 최초 조달액",
            "② 거래가격에서 운송원가와 거래원가를 모두 차감하여 산출한 순공정가치(Net Proceeds)",
            "③ 단순 거래가격에 이자율 변동분을 곱해 구한 예상 할인 차액",
            "④ 금융기관이 임의 보증해 준 자산의 시가총액 마감 수치",
            "⑤ 토지 거래 시 정부 부처가 과세 목적으로 산정한 토지 기준 시가"
        ],
        "answer": "2",
        "explanation": "② 가장 유리한 시장을 '판단'할 때는 순공정가치(즉, 거래가격 - 운송원가 - 거래원가)가 가장 높은 시장(매도 시) 또는 가장 낮은 시장(부채 이전 시)을 비교 대상으로 삼습니다.\n\n[오답 해설]\n① 원가 가산액을 기준으로 삼지 않습니다.\n③ 이자율 곱한 가치 등을 비교하지 않습니다.\n④ 금융기관의 시가총액 마감 수치를 사용하지 않습니다.\n⑤ 정부의 기준시가는 가장 유리한 시장 판단 기준이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "조달 대금 가산 수치 비교가 아닙니다.", "articles": [], "principle": "가장 유리한 시장 비교 잣대", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가장 유리한 시장을 '결정'하는 단계에서는 순공정가치(거래가격 - 운송원가 - 거래원가)를 기준으로 각 시장의 순유입액을 대조합니다.", "articles": [], "principle": "가장 유리한 시장 비교 잣대", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "할인 차액 계산법은 본 비교 기준이 아닙니다.", "articles": [], "principle": "가장 유리한 시장 비교 잣대", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산의 시가총액 마감 데이터와 무관합니다.", "articles": [], "principle": "가장 유리한 시장 비교 잣대", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과세 기준 시가는 회계 상 시장 비교 잣대가 아닙니다.", "articles": [], "principle": "가장 유리한 시장 비교 잣대", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "공정가치 측정 기준서상 비금융자산의 '최고 최선 사용(Highest and Best Use)'을 평가할 때, 자산 소유 기업 고유의 계획과 시장참전자 기대의 상충에 따른 처리 기준으로 가장 옳은 것은?",
        "options": [
            "① 기업의 내부 사용 계획만을 최고 최선 사용의 유일한 전제로 인정한다.",
            "md. 기업의 사적 사용 의도가 다를지라도, 시장참전자 관점에서 판단한 최고 최선 사용 가정을 기초로 공정가치를 측정한다.",
            "③ 최고 최선 사용 평가 시에는 정부 안전 검사 한도 초과 비용을 자본계정에서 즉시 삭감한다.",
            "④ 기업이 청산할 예정이라면 무조건 최고의 가격으로 자산을 재평가해 처분이익을 의무 기재한다.",
            "⑤ 회사의 경쟁 우위를 위협하는 경쟁사의 사용 방침만을 기준으로 가치화한다."
        ],
        "answer": "2",
        "options": [
            "① 기업의 내부 사용 계획만을 최고 최선 사용의 유일한 전제로 인정한다.",
            "② 기업의 사적 사용 의도가 다를지라도, 시장참전자 관점에서 판단한 최고 최선 사용 가정을 기초로 공정가치를 측정한다.",
            "③ 최고 최선 사용 평가 시에는 정부 안전 검사 한도 초과 비용을 자본계정에서 즉시 삭감한다.",
            "④ 기업이 청산할 예정이라면 무조건 최고의 가격으로 자산을 재평가해 처분이익을 의무 기재한다.",
            "⑤ 회사의 경쟁 우위를 위협하는 경쟁사의 사용 방침만을 기준으로 가치화한다."
        ],
        "answer": "2",
        "explanation": "② 비금융자산의 최고 최선 사용은 보고기업의 실제 결성 의도나 보관 계획에 종속되지 않고, 독립된 시장참전자의 관점에서 자산 가치를 극대화할 수 있는 물리적·법적·재무적 사용 방식을 기준으로 공정가치를 산출해야 합니다.\n\n[오답 해설]\n① 내부 계획만을 반영하는 것은 기업 특유 가치 모형으로 공정가치와 대치됩니다.\n③ 안전검사비 자본 삭감 등의 임의 처리는 사실이 아닙니다.\n④ 청산 예정 시 처분 가치를 적용하나 무조건 가상의 최고가 재평가 처분이익을 강제 계상할 수는 없습니다.\n⑤ 경쟁사의 일방적 방침을 맹종하지는 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기업 고유의 의도에 얽매이지 않고 시장참전자 관점에서 판단합니다.", "articles": [], "principle": "최고최선사용 판단 관점", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비금융자산 공정가치는 소유 기업의 실제 사용 의도보다 시장참전자가 내릴 객관적 최선 사용 가치 기대를 반영합니다.", "articles": [], "principle": "최고최선사용 판단 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "안전검사비 자본 임의 차감은 비회계적입니다.", "articles": [], "principle": "최고최선사용 판단 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가공의 처분이익 의무 기재 조항 등은 없습니다.", "articles": [], "principle": "최고최선사용 판단 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경쟁사의 개별 의도만을 가격 결정 조건으로 채택하지 않습니다.", "articles": [], "principle": "최고최선사용 판단 관점", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "공정가치 측정 기준서상 동일하거나 비슷한 부채 또는 자기지분상품을 이전하기 위한 공시가격이 없고, 다른 상대방도 동일한 항목을 자산으로 보유하고 있지 않은 경우, 공정가치를 측정하는 가치평가 관점은?",
        "options": [
            "① 자산을 매입할 의사가 전혀 없는 비자발적 일반 대중의 주관적 관점",
            "② 부채를 부담하거나 자본에 대한 청구권을 발행한 시장참전자(발행자) 관점",
            "③ 관할 세무서 소속 세무 법인세 담당 조사관의 주관적 징수 관점",
            "④ 금융 자산의 원가를 최초 영수증에 맞게 강제 환급받으려는 매도자 관점",
            "⑤ 회사의 채무를 전액 기부 처리하기로 단독 서명 합의한 자선 단체 관점"
        ],
        "answer": "2",
        "explanation": "② 동일한 부채/지분을 이전할 시장 공시가격이 없고, 타인도 자산으로 보유하지 않은 완전 불비 상황에서는, 해당 부채를 실제 부담하거나 청구권을 발행한 당사자인 '발행자 관점'을 반영한 가치평가기법을 적용해 공정가치를 측정합니다.\n\n[오답 해설]\n① 비자발적 대중의 관점은 가치 기준이 아닙니다.\n③ 법인세 조사관의 관점은 배제됩니다.\n④ 최초 영수증 환급 등의 매도자 관점은 본 상황과 무관합니다.\n⑤ 자선단체의 면제 서명 등은 회계 공식 판단 주체가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비자발적 대중 관점은 성립하지 않습니다.", "articles": [], "principle": "자산 미유보 부채의 측정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "타방이 자산 보유 중이지 않은 부채 공정가치는 의무 부담 발행자 측 시장참전자의 관점에서 추정합니다.", "articles": [], "principle": "자산 미유보 부채의 측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 공무원의 과세 관점은 회계 평가 기준이 아닙니다.", "articles": [], "principle": "자산 미유보 부채의 측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "최초 영수증 소급 처리는 올바르지 않습니다.", "articles": [], "principle": "자산 미유보 부채의 측정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자선단체의 면제 합의 등은 본문 회계 기준과 상관없습니다.", "articles": [], "principle": "자산 미유보 부채의 측정", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "공정가치 측정 기준서상 공정가치 측정을 위해 상황의 변화 등으로 가치평가기법이나 그 적용방법을 변경할 경우의 회계처리 분류로 가장 올바른 것은?",
        "options": [
            "① 회계정책의 변경(Change in Accounting Policy)으로 분류하여 소급법 적용",
            "② 회계추정의 변경(Change in Accounting Estimate)으로 분류하여 전진법 적용",
            "③ 단순 중대한 오류(Significant Prior Period Error)로 보아 전기이월이익잉여금의 소급 수정",
            "④ 감사의견 거절 사유로 보아 재무보고 공시 자체를 무효 선언",
            "⑤ 회사의 대표이사 교체 사유로만 등기소에 기록"
        ],
        "answer": "2",
        "explanation": "② 공정가치 측정을 위해 사용하던 가치평가기법이나 적용방법의 변경은 합리적인 추정의 고도화 과정으로 보아 '회계추정의 변경'으로 회계처리하며 당기와 미래에 전진 적용합니다.\n\n[오답 해설]\n① 정책의 변경이 아니므로 소급 적용하지 않습니다.\n③ 오류수정 사항이 아닙니다.\n④ 정상적인 회계 기법 변경은 감사의견 거절 사유가 아닙니다.\n⑤ 경영진 교체 의무와 하등의 관련이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "회계정책의 변경이 아니므로 소급하지 않습니다.", "articles": [], "principle": "평가기법 변경 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가치평가기법이나 그 적용법 변경에 따른 수정은 회계추정의 변경으로 분류해 전진 처리합니다.", "articles": [], "principle": "평가기법 변경 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전기 오류수정이 아니므로 잉여금 소급 조정을 단행하지 않습니다.", "articles": [], "principle": "평가기법 변경 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의견거절 대상이 아닙니다.", "articles": [], "principle": "평가기법 변경 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대표이사 교체 등의 법인 등기 등과는 인과관계가 없습니다.", "articles": [], "principle": "평가기법 변경 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "공정가치서열체계상 '수준 2의 투입변수(Level 2 Inputs)'의 특성과 구체적인 예시로 가장 올바른 것은?",
        "options": [
            "① 측정일에 동일한 자산에 대한 접근가능한 활성시장의 (조정하지 않은) 공시가격",
            "② 수준 1의 공시가격 이외에 자산이나 부채에 대해 직접적으로나 간접적으로 관측할 수 있는 투입변수 (예: 활성시장에서 유사한 자산의 공시가격 등)",
            "③ 보고기업이 내부 연구를 통해 독점적으로 가정한 미래 현금 유입 추정치 전체",
            "④ 금융기관이 대출 한도 승인 명목으로 자의적으로 부과한 예산 고정 금리",
            "⑤ 세무 당국이 기업의 조세를 부과하기 위해 결정한 개별 과세 표준액"
        ],
        "answer": "2",
        "explanation": "② 수준 2 투입변수는 수준 1의 활성시장 동일자산 공시가격은 아니지만, 직접/간접적으로 관측가능한 시장 정보(예: 활성시장에서 유사한 자산의 공시가격, 비활성시장에서 동일/유사 자산 가격 등)를 의미합니다.\n\n[오답 해설]\n① 이는 수준 1 투입변수의 설명입니다.\n③ 이는 관측불가능한 정보로 수준 3에 해당합니다.\n④, ⑤는 수준 2 투입변수의 예시가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "동일 자산의 활성시장 공시가격은 수준 1 변수입니다.", "articles": [], "principle": "수준 2 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수준 2는 관측가능한 유사의 공시가격이나 금리 곡선 등 간접/직접 관측 가능 시장 자료를 뜻합니다.", "articles": [], "principle": "수준 2 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기업 독자적 관측불가 가정은 수준 3 변수입니다.", "articles": [], "principle": "수준 2 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대출 한도 금리는 본 회계적 분류와 거리가 있습니다.", "articles": [], "principle": "수준 2 투입변수 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과세표준액은 수준 2 투입변수가 아닙니다.", "articles": [], "principle": "수준 2 투입변수 정의", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "공정가치서열체계(Fair Value Hierarchy)와 공정가치 측정을 위해 사용하는 세 가지 '가치평가기법'과의 논리적 관계에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 서열체계는 이익접근법에 가장 높은 수준 1을 부여하고 시장접근법에는 강제로 수준 3을 부여한다.",
            "② 공정가치서열체계는 가치평가기법 자체에 우선순위를 부여하는 것이 아니라, 가치평가기법에 적용하여 투입하는 '투입변수'의 관측가능성 수준에 우선순위를 부여하는 것이다.",
            "③ 서열체계를 높이기 위해 무조건 원가접근법만 사용하여 모든 금융주식을 재평가해야 한다.",
            "④ 가치평가기법이 시장접근법이면 서열체계와 무관하게 무조건 부채로 강제 분류한다.",
            "⑤ 회사의 장부자산 총합을 늘리는 기법일수록 서열체계에서 등급이 자동 하락하도록 고안되어 있다."
        ],
        "answer": "2",
        "explanation": "② 공정가치서열체계는 어떤 가치평가 모델(시장/원가/이익접근법)을 썼느냐 자체에 등급이나 우선순위를 강제하지 않고, 그 모델의 인풋(투입변수)으로 활성시장 공시가(수준 1)를 썼는지 주관적 추정치(수준 3)를 썼는지에 따라 우선순위를 매깁니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 서열체계와 기법 간의 연계 관계를 근거 없이 왜곡되게 설명한 것들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "특정 평가 접근법 자체에 수준을 박제하지는 않습니다.", "articles": [], "principle": "서열체계와 가치평가기법", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치서열체계는 평가 기법의 순위가 아니라, 기법에 입력되는 투입변수의 신뢰성/객관성 등급에 순위를 줍니다.", "articles": [], "principle": "서열체계와 가치평가기법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가접근법 사용 강제 규정은 없습니다.", "articles": [], "principle": "서열체계와 가치평가기법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기법 사용에 따라 부채로 강제 재분류되는 일은 없습니다.", "articles": [], "principle": "서열체계와 가치평가기법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산액 증감과 서열체계 등급 변동은 인과관계가 없습니다.", "articles": [], "principle": "서열체계와 가치평가기법", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "공정가치 측정 시, 가치평가모델에 수준 1(공시가), 수준 2(금리 곡선 등), 수준 3(주관적 성장률 등)의 다양한 투입변수가 혼합되어 적용되었을 때, 이 측정치 전체의 최종 공정가치서열 수준을 결정하는 귀속 원칙은?",
        "options": [
            "① 가장 높은 등급의 투입변수에 맞춰 수준 1로 전체를 강제 통일한다.",
            "② 측정치 전체에 유의적이면서 가장 낮은 수준(Lowest Level)의 투입변수와 같은 수준으로 전체를 분류한다.",
            "③ 각 수준의 투입변수 개수를 세어 다수결 법칙으로 많은 등급에 귀속시킨다.",
            "④ 금융감독원에 지정 신청하여 당해 연도 세법 방침에 따라 등급을 평균 2로 조정한다.",
            "⑤ 회사의 당기순이익을 높여주는 투입변수의 수준에 대칭 배정한다."
        ],
        "answer": "2",
        "explanation": "② 여러 수준의 투입변수가 섞여 있다면, 그 자산/부채의 측정치 전체 등급은 평가 결과에 유의미한 영향력을 주는 변수 중 '가장 낮은 순위(Level의 숫자가 가장 큰 수준)'의 투입변수를 기준으로 결정합니다.\n\n[오답 해설]\n① 가장 높은 수준(수준 1)으로 강제 합치시키면 신뢰성이 과장되므로 금지됩니다.\n③ 다수결 원칙이 아닙니다.\n④, ⑤는 서열체계 최종 등급 판정 규칙이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "높은 수준으로 가치 평가의 신뢰성을 인위적으로 과장할 수 없습니다.", "articles": [], "principle": "여러 수준 변수의 혼합 시 등급", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "혼합 시 전체 공정가치 수준은 유의적이면서 '가장 낮은 수준'의 투입변수 등급으로 최종 분류합니다.", "articles": [], "principle": "여러 수준 변수의 혼합 시 등급", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "다수결 수량 분류법이 아닙니다.", "articles": [], "principle": "여러 수준 변수의 혼합 시 등급", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금감원의 심사 조정이나 세법 연동이 아닙니다.", "articles": [], "principle": "여러 수준 변수의 혼합 시 등급", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순이익 변동량과 수준 분류는 관련이 없습니다.", "articles": [], "principle": "여러 수준 변수의 혼합 시 등급", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "공정가치 측정 시 관측가능한 투입변수(수준 2 등)를 관측할 수 없는 투입변수(수준 3 등)를 사용하여 조정(Adjustment)해야 하고, 그 조정으로 인해 공정가치 측정치에 유의적인 변동이 초래될 때, 이 측정치의 최종 공정가치서열 수준 분류는?",
        "options": [
            "① 수준 1",
            "② 수준 2",
            "③ 수준 3",
            "④ 금융자산이면 수준 2, 금융부채면 수준 3",
            "⑤ 조정 비율을 매달 1/N로 나누어 수준 1, 2, 3 전체에 분할 안분"
        ],
        "answer": "3",
        "explanation": "③ 관측가능한 변수를 관측불가능한 주관적 변수를 사용해 유의적으로 조정(가치 변동액 유발)한다면, 그 측정치의 신뢰성은 관측불가능한 수준에 크게 오염되었다고 볼 수 있어 최종적으로 '수준 3'으로 하향 분류합니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 유의적 조정 변동 발생 시 서열체계 분류 지침과 정면 대치되므로 잘못되었습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수준 1로 분류될 수는 없습니다.", "articles": [], "principle": "조정 시 수준의 변동", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유의적인 관측불가 조정이 개입되었으므로 수준 2에 머무를 수 없습니다.", "articles": [], "principle": "조정 시 수준의 변동", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "관측가능 투입변수를 관측할 수 없는 요소를 써서 유의적으로 수정했다면 최종 수준 3으로 귀속됩니다.", "articles": [], "principle": "조정 시 수준의 변동", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산/부채 구분에 따라 수준 변동이 결정되지 않습니다.", "articles": [], "principle": "조정 시 수준의 변동", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "등급을 3단계에 분할 기재하는 전산 처리는 없습니다.", "articles": [], "principle": "조정 시 수준의 변동", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "공정가치 측정 기준서상 비금융자산의 최고 최선 사용(Highest and Best Use)이 성립하기 위해 동시에 검토되어 충족해야 하는 세 가지 구체적인 판단 기준이 아닌 것은?",
        "options": [
            "① 물리적으로 가능(Physically Possible)해야 한다.",
            "② 법적으로 허용(Legally Permissible)해야 한다.",
            "③ 재무적으로 실현가능(Financially Feasible)해야 한다.",
            "④ 당기 보고기업의 분기 손익을 무조건 전년 대비 증가(Profit Maximizing)시켜야 한다.",
            "⑤ 이상의 ①, ②, ③ 모두 최고 최선 사용 판단 시 필수 검토되어야 하는 기준에 속한다."
        ],
        "answer": "4",
        "explanation": "④ 최고 최선 사용은 해당 자산 자체의 물리적 가능성, 법적 규제 통과 여부(용도 제한), 재무적 자금 유용 가치 창출 여부(재무적 실현가능성)를 따질 뿐이며, 당기 기업의 회계적 이익 증가 여부와는 상관이 없습니다.\n\n[오답 해설]\n①, ②, ③은 최고 최선 사용 판단 시 기준서가 규정한 누적 검증 3단계 허들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "물리적 가능성은 최고 최선의 사용 판단 기준입니다.", "articles": [], "principle": "최고 최선 사용 3대 허들", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법적 허용 가능성은 용도 규제 등을 검토하는 필수 요건입니다.", "articles": [], "principle": "최고 최선 사용 3대 허들", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재무적 실현가능성은 투자 회수 및 타당성을 증명하는 조건입니다.", "articles": [], "principle": "최고 최선 사용 3대 허들", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기업의 단기 손익을 극대화해야만 최고 최선 사용이 성립되는 것은 아니며 회계 이익 조작 목적은 배제됩니다.", "articles": [], "principle": "최고 최선 사용 3대 허들", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "④가 오답이므로 틀린 보기입니다.", "articles": [], "principle": "최고 최선 사용 3대 허들", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "공정가치 측정의 기반이 되는 독립된 '시장참전자(Market Participants)'가 갖추어야 할 요건으로 가장 거리가 먼 것은?",
        "options": [
            "① 거래 당사자 간에 지배-종속 관계나 특수관계가 없는 독립적인 당사자이어야 한다.",
            "② 해당 자산이나 부채에 대하여 합리적인 지식을 가지고 있는 숙련된 당사자이어야 한다.",
            "③ 자산이나 부채의 거래를 기꺼이 수행할 의사(자발적 의사)가 있는 당사자이어야 한다.",
            "④ 보고기업의 자산 가치를 강제로 늘려주기 위해 금융감독원에 비밀 맹세를 한 당사자이어야 한다.",
            "⑤ 거래를 강제당하지 않고 기꺼이 거래할 능력이 있는 거래가능한 당사자이어야 한다."
        ],
        "answer": "4",
        "explanation": "④ 시장참전자는 시장의 정상거래에 참여하는 자발적인 독립 주체일 뿐이며, 보고기업의 편의를 위해 금감원에 비밀 맹세를 한 주체라는 가정은 회계에 존재하지 않는 허구입니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 시장참전자의 핵심 4대 요건(특수관계 없음, 지식 있음, 거래 의사 있음, 거래 능력 있음)을 정확히 설명하고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "독립적 당사자 요건은 참입니다.", "articles": [], "principle": "시장참전자의 조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "합리적인 지식 보유 요건은 참입니다.", "articles": [], "principle": "시장참전자의 조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자발적 거래 의사 보유 요건은 참입니다.", "articles": [], "principle": "시장참전자의 조건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가상의 비밀 맹세 주체 등은 시장참전자 조건에 들어갈 수 없는 명백한 오류입니다.", "articles": [], "principle": "시장참전자의 조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래 수행 능력 보유 요건은 참입니다.", "articles": [], "principle": "시장참전자의 조건", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "공정가치서열체계상 수준 1의 가격 획득의 전제가 되는 '활성시장(Active Market)'의 정의로 가장 올바른 것은?",
        "options": [
            "① 매 10년에 한 번만 임시 개장하는 비밀 폐쇄 시장",
            "② 자산이나 부채의 거래 빈도와 거래량이 지속적으로 가격 정보를 제공하기에 충분할 정도로 충분히 거래가 자주 일어나는 시장",
            "③ 보고기업의 임직원들만이 참여하여 가격을 자유롭게 결정할 수 있는 단독 사내 장터",
            "④ 정부 공무원들이 자산의 세무 가격 결정을 위해 임의 개설한 조세 협의 시장",
            "⑤ 주가가 매일 10배씩 등락을 반복하여 시장이 혼란한 과열 시장"
        ],
        "answer": "2",
        "explanation": "② 활성시장(Active Market)은 지속적으로 가격 정보를 획득할 수 있도록 자산/부채의 거래 빈도와 거래량이 충분히 유지되는 시장으로 정의됩니다.\n\n[오답 해설]\n① 10년 주기 개장 시장은 활성시장이 아닙니다.\n③ 사내 장터 등 특수관계자만의 시장은 활성시장 공시가격 시장으로 부적합합니다.\n④ 세무 협의 시장은 회계 상 활성시장이 아닙니다.\n⑤ 극단적 과열 요동 시장만을 의미하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "폐쇄적 휴면 시장은 활성시장이 아닙니다.", "articles": [], "principle": "활성시장의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "활성시장은 거래량과 거래 빈도가 지속적 가격 관측을 보장할 수 있을 정도로 충분히 높은 시장을 의미합니다.", "articles": [], "principle": "활성시장의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사내 폐쇄시장은 활성시장이 될 수 없습니다.", "articles": [], "principle": "활성시장의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 조세용 시장은 활성시장의 정의가 아닙니다.", "articles": [], "principle": "활성시장의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과열 투기 시장을 활성시장의 기본 회계적 정의라 하진 않습니다.", "articles": [], "principle": "활성시장의 정의", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "재고자산 감액 평가 시 사용되는 '순실현가능가치(Net Realizable Value)'와 일반적인 자산 평가 시의 '공정가치(Fair Value)'의 관계에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 두 수치는 이론과 실무 상 항상 1원 단위까지 강제 일치한다.",
            "② 순실현가능가치는 기업특유가치(Entity-specific Value)인 반면, 공정가치는 시장에 근거한 측정치(시장참전자 관점)이므로 서로 일치하지 않을 수 있다.",
            "③ 순실현가능가치는 세무서 제출용이고 공정가치는 주주총회용으로만 법적으로 용도가 분리된다.",
            "④ 공정가치에 처분원가를 무조건 합산해야만 순실현가능가치가 도출된다.",
            "⑤ 순실현가능가치가 상승하면 무조건 자본금을 10배로 무상 증자해야 한다."
        ],
        "answer": "2",
        "explanation": "② 재고자산 평가에 사용되는 순실현가능가치는 당해 기업의 통상적인 영업과정에서 판매를 통해 직접 실현할 것으로 보는 기업 고유의 가격(기업특유가치)입니다. 이에 반해 공정가치는 특정 보고기업의 특수성과 무관한 객관적 시장참전자 관점의 유출가격이므로 둘은 불일치할 수 있습니다.\n\n[오답 해설]\n① 항상 일치하지 않습니다.\n③ 제출 대상에 따른 법적 용도 고정 설명은 잘못되었습니다.\n④ 공정가치에서 처분부대원가를 빼더라도 순실현가치와 다른 경우가 흔합니다(관점 차이).\n⑤ 무상증자 의무를 지우는 조항은 존재하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "두 수치의 강제 일치 조항은 없습니다.", "articles": [], "principle": "순실현가치와 공정가치 대조", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "순실현가능가치는 특정 기업의 판매기대치를 담는 기업특유가치이며 공정가치는 시장참전자 시각이므로 괴리가 가능합니다.", "articles": [], "principle": "순실현가치와 공정가치 대조", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "용도가 조세/주총으로 이분법 고정되지 않습니다.", "articles": [], "principle": "순실현가치와 공정가치 대조", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분원가를 빼는 것이 순실현가치 유도법이나 그것이 공정가치에 처분원가 합산과 같진 않습니다.", "articles": [], "principle": "순실현가치와 공정가치 대조", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 10배 강제 무상증자 설은 허구입니다.", "articles": [], "principle": "순실현가치와 공정가치 대조", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },

    # =========================================================================
    # L3: 적용 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s09-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "A사는 생산한 농산물 원자재를 해외시장에 처분하고자 한다. 해외시장은 거래량이 가장 많은 주된 시장이다. 해외시장의 원자재 거래가격은 10,000원이며, 해당 해외시장까지 원자재를 운송하는 운송원가는 2,000원, 중개인 수수료 및 거래원가는 1,500원이다. 개념체계 및 IFRS 제1113호상 이 원자재의 공정가치(Fair Value)와 순공정가치(Net Fair Value)는 각각 얼마인가?",
        "options": [
            "① 공정가치: 10,000원, 순공정가치: 8,500원",
            "② 공정가치: 8,000원, 순공정가치: 6,500원",
            "③ 공정가치: 8,000원, 순공정가치: 8,000원",
            "④ 공정가치: 8,500원, 순공정가치: 7,000원",
            "⑤ 공정가치: 10,000원, 순공정가치: 6,500원"
        ],
        "answer": "2",
        "explanation": "② 해외시장이 주된 시장이므로 해외시장 정보를 적용합니다. 공정가치는 거래가격에서 **운송원가만을 차감**하고 거래원가는 직접 조정(차감)하지 않으므로, 공정가치 = 10,000원 - 2,000원 = **8,000원**이 됩니다. 순공정가치는 이 산정된 공정가치에서 다시 거래원가를 차감하여 구하므로, 순공정가치 = 8,000원 - 1,500원 = **6,500원**이 됩니다.\n\n[오답 해설]\n① 공정가치에 운송원가(2,000원) 차감을 누락하여 오답입니다.\n③ 순공정가치 산출 시 거래원가(1,500원) 차감을 생략하여 오답입니다.\n④, ⑤는 운송/거래 원가의 조정 순서를 잘못 계산하여 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "공정가치 결정 시 위치 보정 운송비(2,000원)를 공제하지 않아 오답입니다.", "articles": [], "principle": "주된시장 하의 공정가치 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치(거래가 10,000 - 운송비 2,000 = 8,000원)와 순공정가치(공정가 8,000 - 거래원가 1,500 = 6,500원) 계산이 정확합니다.", "articles": [], "principle": "주된시장 하의 공정가치 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순공정가치 계산 시 거래원가 차감을 전혀 수행하지 않았습니다.", "articles": [], "principle": "주된시장 하의 공정가치 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "운송원가 대신 거래원가를 임의로 먼저 차감한 결과물입니다.", "articles": [], "principle": "주된시장 하의 공정가치 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치에 운송비 공제를 누락한 오류입니다.", "articles": [], "principle": "주된시장 하의 공정가치 계산", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "B사는 보유 자산을 매각할 수 있는 두 개의 시장 A와 B가 있으나, 주된 시장은 존재하지 않는다. 각 시장별 거래 정보는 다음과 같다.\n\n* A시장: 거래가격 5,000원, 운송원가 500원, 거래원가 800원\n* B시장: 거래가격 5,300원, 운송원가 800원, 거래원가 1,200원\n\n이 자산의 공정가치(Fair Value)는 가장 유리한 시장의 기준을 적용하여 산출 시 얼마로 결정되는가?",
        "options": [
            "| A시장 공정가치: 4,500원",
            "| B시장 공정가치: 4,500원",
            "③ 3,700원",
            "④ 3,300원",
            "⑤ 4,200원"
        ],
        "options": [
            "① A시장의 공정가치인 4,500원",
            "② B시장의 공정가치인 4,500원",
            "③ A시장의 순공정가치인 3,700원",
            "④ B시장의 순공정가치인 3,300원",
            "⑤ 두 시장의 공정가치 평균액인 4,500원"
        ],
        "answer": "1",
        "explanation": "① 주된 시장이 없으므로 가장 유리한 시장을 순공정가치(순수익액) 크기로 먼저 판별합니다.\n* A시장 순공정가치 = 5,000원 - 500원(운송원가) - 800원(거래원가) = 3,700원\n* B시장 순공정가치 = 5,300원 - 800원(운송원가) - 1,200원(거래원가) = 3,300원\n따라서 순수익액이 가장 큰 **A시장**이 가장 유리한 시장으로 최종 결정됩니다.\n이때 자산의 공정가치는 거래원가를 조정하지 않고 운송원가만 차감하여 결정하므로, 공정가치 = A시장 가격 5,000원 - 운송원가 500원 = **4,500원**이 됩니다.\n\n[오답 해설]\n② B시장을 가장 유리한 시장으로 오인하여 산출(5,300 - 800 = 4,500원)하여 오답입니다.\n③, ④는 공정가치 수치 자체에 거래원가까지 강제 차감 조정한 순공정가치 수치를 대입하여 오답입니다.\n⑤ 단순 평균은 적용되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "가장 유리한 시장은 순공정가치가 최대인 A시장(3,700원)이며, 이 시장 하의 공정가치는 운송원가만 공제한 4,500원입니다.", "articles": [], "principle": "유리한 시장 판정 및 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "B시장의 순수익액(3,300원)이 A시장보다 적으므로 가장 유리한 시장 선택이 틀렸습니다.", "articles": [], "principle": "유리한 시장 판정 및 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순공정가치 수치 자체를 공정가치 장부액으로 쓰지는 않습니다.", "articles": [], "principle": "유리한 시장 판정 및 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "B시장은 유리한 시장도 아닐 뿐더러 순공정가치 자체를 공정가치라 표기해 오답입니다.", "articles": [], "principle": "유리한 시장 판정 및 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시장 간 평균값 유도는 적용 사유가 없습니다.", "articles": [], "principle": "유리한 시장 판정 및 계산", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "C치킨회사는 생닭 원재료 재고를 다량 보유하고 있다. 다음 자료 하에서 생닭의 '순실현가능가치(NRV)'와 '공정가치(Fair Value)'를 각각 산정하면 얼마인가?\n\n* 후라이드 치킨 완성품 1마리 판매가: 20,000원\n* 생닭을 치킨으로 요리하는 데 추가 발생하는 가공원가: 8,000원\n* 배달수수료: 2,500원, 브랜드 로열티 비용: 3,000원\n* 생닭을 도매 시장에 처분 시 시장 거래금액: 12,000원\n* 도매 시장까지의 생닭 운송원가: 500원, 도매 거래 중개원가: 800원",
        "options": [
            "① 순실현가치: 9,500원, 공정가치: 12,000원",
            "② 순실현가치: 6,500원, 공정가치: 11,500원",
            "③ 순실현가치: 6,500원, 공정가치: 10,700원",
            "④ 순실현가치: 12,000원, 공정가치: 11,500원",
            "⑤ 순실현가치: 9,500원, 공정가치: 10,700원"
        ],
        "answer": "2",
        "explanation": "② 순실현가능가치는 완성품 판매액 20,000원 - 추가 가공비 8,000원 - 직접판매비 2,500원 - 로열티 3,000원 = **6,500원**이 됩니다. 반면 시장참전자 기준의 공정가치는 도매 처분가액 12,000원 - 운송원가 500원 = **11,500원**이 됩니다. (도매 거래원가 800원은 공정가치에서 직접 차감 조정하지 않습니다.)\n\n[오답 해설]\n① 순실현가치 및 공정가치 계산에 운송비/수수료 조정을 누락하였습니다.\n③ 공정가치 수치에 거래원가(800원)까지 차감 조정하여 오답입니다. (10,700원은 순공정가치입니다.)\n④, ⑤는 일부 차감 계산을 누락하거나 혼동하여 도출된 오류 수치들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "가공비 외 배달료와 로열티를 정상 공제하지 않아 순실현가치가 과대산정되었습니다.", "articles": [], "principle": "순실현가치와 공정가치 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "순실현가치는 판매가에서 제반비용을 공제한 6,500원이며, 공정가치는 도매시장가 12,000 - 운송비 500 = 11,500원입니다.", "articles": [], "principle": "순실현가치와 공정가치 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치에서 거래원가 800원까지 무단 차감하여 오답입니다.", "articles": [], "principle": "순실현가치와 공정가치 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조정이 전혀 엉뚱하게 조합된 결과입니다.", "articles": [], "principle": "순실현가치와 공정가치 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순실현가치와 공정가치 계산 시 차감 규칙을 둘 다 위배하였습니다.", "articles": [], "principle": "순실현가치와 공정가치 계산", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "D사는 도심 중심가에 위치한 공장 부지(토지)를 보유 중이다. 현재 공장을 유지할 때의 토지 사용 가치는 50억 원이다. 그러나 시장참전자 관점에서는 해당 토지에 상업용 고층 주상복합 빌딩을 신축하는 개발안이 가장 가치 극대화가 유력하며, 이 개발 시나리오 하에서의 토지 평가 가치는 80억 원에 달한다. 현재 주상복합 개발을 위한 법적 용도변경 규제 완화가 허용되어 있으며 재무적으로도 실현 가능하다. D사의 공정가치 측정 토지 장부 가액은 얼마로 책정하는가?",
        "options": [
            "① 30억 원",
            "② 50억 원",
            "③ 80억 원",
            "④ 130억 원",
            "⑤ 240억 원"
        ],
        "answer": "3",
        "explanation": "③ 비금융자산의 공정가치는 시장참전자 관점에서 본 '최고 최선 사용(Highest and Best Use)'을 전제로 측정합니다. 현재 용도변경이 법적/물리적/재무적으로 성립 가능하므로 최고의 사용인 빌딩 신축 개발 가치인 **80억 원**을 공정가치로 책정하는 것이 기준서에 부합합니다.\n\n[오답 해설]\n① 80억과 50억의 차액은 별도로 기재하지 않습니다.\n② 현재 영업 용도 고수 가격인 50억 원은 최고 최선 사용 요건을 무시한 것이므로 오답입니다.\n④ 두 값을 합산한 수치는 틀렸습니다.\n⑤ 단순 곱셈액은 성립할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "두 시나리오 가액의 차액 산정은 관련이 없습니다.", "articles": [], "principle": "최고 최선의 사용 계산 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현재의 용도 고수 가치는 최고 최선의 경제적 이익을 내지 못하므로 공정가치로 채택될 수 없습니다.", "articles": [], "principle": "최고 최선의 사용 계산 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "물리적, 법적, 재무적으로 가능한 최고 최선의 용도가 주상복합 개발(80억 원)이므로 토지의 공정가치는 80억 원으로 결정됩니다.", "articles": [], "principle": "최고 최선의 사용 계산 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 합산액은 과대 계상 오류입니다.", "articles": [], "principle": "최고 최선의 사용 계산 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 곱셈 산출은 회계 상 근거가 없습니다.", "articles": [], "principle": "최고 최선의 사용 계산 적용", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "E사가 과거에 발행한 회사채 1억 원(부채)에 대한 활성시장 공시가격이 존재하지 않는다. 그러나 F은행이 당해 회사채를 전액 매입하여 '자산(투자채무상품)'으로 보유하고 있으며, F은행의 자산 계정 상 해당 채권의 활성시장 공시 가격은 9,500만 원으로 완벽히 관측 가능하다. E사의 결산 시, 이 회사채 부채의 공정가치 측정에 관한 설명으로 가장 옳은 것은?",
        "options": [
            "① 자사의 부채 공시가격이 없으므로 무조건 1원이나 발행원가로 고정 기재해야 한다.",
            "② 타인이 동일 채무를 자산으로 보유하고 있으므로, 자산 보유 시장참전자 관점의 관측가능 가격인 9,500만 원을 사채부채의 공정가치로 측정하여 인식한다.",
            "③ 부채는 자산과 대칭을 맞추어 무조건 마이너스(-) 9,500만 원으로 표기해야 한다.",
            "④ 주총 결의를 거쳐 F은행 채권을 무단 소멸 처리하고 잉여금 가산으로 끝낸다.",
            "⑤ 상대방이 보유한 자산 가격은 부채 가치 결정에 0.1%의 비례적 영향도 미쳐서는 안 된다."
        ],
        "answer": "2",
        "explanation": "② 동일하거나 비슷한 부채를 이전하기 위한 공시가격을 직접 구할 수 없더라도, 상대방(채권자)이 동일한 항목을 자산으로 보유하고 있는 경우에는 자산 보유자의 관점에서 관측 가능한 시장가격(9,500만 원)을 사채부채의 공정가치 측정치로 사용하는 것이 타당합니다.\n\n[오답 해설]\n① 관측 가능한 상대방 자산 가격이 있음에도 1원 등으로 고정 방치하는 것은 회계 오류입니다.\n③ 부채는 양(+)의 값 9,500만 원으로 기재하되 대변에 계상하므로 음수 표기 명제는 잘못되었습니다.\n④, ⑤는 기준서의 대조 규칙과 다른 잘못된 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상대방 자산의 가격을 원용할 수 있으므로 원가 고정은 오답입니다.", "articles": [], "principle": "상대방 보유 부채의 공정가치", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "상대방이 자산으로 보유하고 있다면 그 시장참전자의 관점에서 공시가격(9,500만 원)을 활용해 자사의 부채 공정가치를 측정합니다.", "articles": [], "principle": "상대방 보유 부채의 공정가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 가액 자체를 마이너스 부호 표기한다는 서술은 틀렸습니다.", "articles": [], "principle": "상대방 보유 부채의 공정가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무단 소멸 및 잉여금 가산은 법 위반입니다.", "articles": [], "principle": "상대방 보유 부채의 공정가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상대방의 자산 가액은 부채 가치에 직접적인 근거가 되므로 영향 배제는 틀렸습니다.", "articles": [], "principle": "상방 보유 부채의 공정가치", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "F사는 기말 비상장 주식옵션의 공정가치를 블랙숄즈 평가모형(이익접근법)으로 측정하였다. 이 평가모형에 들어간 투입변수 중 '기초자산의 최근 관측가격(수준 2)'과 '무위험이자율(수준 2)'은 관측 가능하나, 가장 핵심적인 '미래 기대 변동성 가정(수준 3)'은 관측이 불가능하여 회사가 자체적으로 주관적 산출해 투입했으며 이는 전체 옵션가 가치평가 결과에 극히 유의미하다. 이 자산의 최종 공정가치서열 등급은?",
        "options": [
            "① 수준 1 (Level 1)",
            "② 수준 2 (Level 2)",
            "③ 수준 3 (Level 3)",
            "④ 금융자산이므로 강제로 수준 1 지정",
            "⑤ 평균 등급인 수준 2.33"
        ],
        "answer": "3",
        "explanation": "③ 여러 수준의 투입변수가 혼합된 조건에서, 결과치 전체에 가장 유의적이면서 낮은 등급(순위가 가장 처지는 등급)의 투입변수가 수준 3(변동성 가정)이므로, 측정치 전체는 최종적으로 '수준 3'으로 분류됩니다.\n\n[오답 해설]\n① 수준 1이 섞여 있지도 않을뿐더러 수준 1이 될 수 없습니다.\n② 수준 3의 주관적 변수가 유의적으로 투입되었으므로 수준 2로 올려 분류할 수 없습니다.\n④, ⑤는 서열체계 판정 원칙에 없는 틀린 지문입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수준 1 요건인 활성시장 동일자산 공시가가 없으므로 수준 1이 될 수 없습니다.", "articles": [], "principle": "서열체계 판정 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수준 3의 관측불가 변수가 유의적으로 가치를 좌우하므로 수준 2는 오답입니다.", "articles": [], "principle": "서열체계 판정 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가장 낮은 등급인 수준 3 투입변수가 전체 측정에 유의적이므로 최종 분류 등급은 수준 3이 됩니다.", "articles": [], "principle": "서열체계 판정 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융자산이라 해서 임의로 수준 1로 격상하지 않습니다.", "articles": [], "principle": "서열체계 판정 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소수점 수준 분류법 등은 존재하지 않습니다.", "articles": [], "principle": "서열체계 판정 적용", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "G사는 활성시장에서 실시간 공시되는 금융 채권을 1,000만 원에 매입하고 취득 수수료(거래원가) 20만 원을 지급하였다. 동 금융상품은 '당기손익-공정가치측정 금융자산(FVPL자산)'으로 분류하여 당기 공정가치로 기재된다. 최초 인식일에 FVPL자산으로 기재될 자산가액과 당일 당기손익(비용)에 영향을 미치는 금액은 각각 얼마인가?",
        "options": [
            "① 자산가액: 1,020만 원, 당기비용: 0원",
            "② 자산가액: 1,000만 원, 당기비용: 20만 원",
            "③ 자산가액: 980만 원, 당기비용: 20만 원",
            "④ 자산가액: 1,000만 원, 당기비용: 0원",
            "⑤ 자산가액: 1,020만 원, 당기비용: 20만 원"
        ],
        "answer": "2",
        "explanation": "② 당기손익-공정가치측정 금융자산(FVPL)은 공정가치로 기재되어야 하며, 공정가치는 거래원가를 포함하지 않으므로 취득일에 순수 시장 가격인 **1,000만 원**으로 자산을 인식합니다. 지급한 거래 수수료 20만 원은 자산가액에 얹을 수 없고 당기 손익(수수료비용) **20만 원**으로 즉시 인식합니다.\n\n[오답 해설]\n① 취득수수료를 자산에 합산(1,020만 원)하여 틀렸습니다(이는 상각후원가측정 금융자산 등에서 사용하는 규칙입니다).\n③ 자산가액을 차감 처리하여 오답입니다.\n④ 거래원가를 누락하고 비용도 처리하지 않는 대차 불일치 오류입니다.\n⑤ 자산과 비용을 둘 다 이중으로 늘린 계산 오류입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "취득원가 가산 규칙은 FVPL 금융자산 최초 공정가치 평가 시 적용되지 않습니다.", "articles": [], "principle": "FVPL자산의 거래원가", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "FVPL 금융자산은 거래원가를 자산가에 얹지 않고 전액 당기비용(20만 원) 처리하므로 자산은 1,000만 원이 정확합니다.", "articles": [], "principle": "FVPL자산의 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산액을 980만 원으로 차감할 하등의 이유가 없습니다.", "articles": [], "principle": "FVPL자산의 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수수료 비용 회계처리를 아예 누락하여 대차가 맞지 않습니다.", "articles": [], "principle": "FVPL자산의 거래원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 1,020만 원 계상 설명은 규칙 위반입니다.", "articles": [], "principle": "FVPL자산의 거래원가", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "H사는 기말 금융 자산의 공정가치 측정에 있어, 기존에는 과거 유사 거래 데이터를 토대로 비교 평가하는 '시장접근법'을 적용했으나, 시장 환경 급변으로 인해 올해는 미래 배당 기댓값을 현재가치로 할인하는 '이익접근법'으로 변경하여 측정하였다. 이 기법 변경이 재무제표 공시에 미치는 회계적 영향으로 올바른 설명은?",
        "options": [
            "① 기법 변경일이 속한 당해 분기 재무제표를 포함하여 과거 3년 치 재무제표를 소급해 재작성해야 한다.",
            "② 기법 변경은 회계추정의 변경에 해당하므로 소급 적용을 하지 않고, 변경 당기 및 미래 기간에 전진 적용하며 관련 변경 원인과 재무적 효과를 주석 공시한다.",
            "③ 공정가치 측정기법의 중도 변경은 심각한 회계 원칙 위배로 감사인이 즉시 형사 고발해야 한다.",
            "④ 기법을 바꾸면 자산의 장부총액에서 50%를 강제 삭감해야 한다.",
            "⑤ 변경 시점부터 당해 자산은 즉시 전액 자본금 감소로 강제 상계 처리된다."
        ],
        "answer": "2",
        "explanation": "② 가치평가기법의 변경은 회계추정의 변경에 해당하므로 과거를 소급하지 않고 전진적으로 당기와 미래에 적용합니다. 더 나은 공정가치 묘사를 위해 변경한 사유와 수치 변동 효과를 주석에 성실 공시하면 됩니다.\n\n[오답 해설]\n① 정책의 변경이 아니므로 소급하지 않습니다.\n③ 정당한 평가기법의 변경은 위법도 아니고 감사인의 형사 고발 사유도 아닙니다.\n④, ⑤는 회계 기준과 거리가 있는 가공의 오처리 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "소급법은 평가기법 변경 시 적용되지 않습니다.", "articles": [], "principle": "평가기법 변경의 효과", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기법 변경은 회계추정의 변경으로 당기 전진 처리하며 사유와 효과를 이용자에게 보고합니다.", "articles": [], "principle": "평가기법 변경의 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "형사 고발 등 감사의견 제재 대상이 아닙니다.", "articles": [], "principle": "평가기법 변경의 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "50% 강제 삭감 규정 등은 사실무근입니다.", "articles": [], "principle": "평가기법 변경의 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 감 상계 처리는 틀린 방법입니다.", "articles": [], "principle": "평가기법 변경의 효과", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "I사는 공장용 토지를 취득했다. 기말 공정가치 평가 시, 이 토지를 타사에 매도해 상업용 부지로 최고 최선 개발을 한다고 전제(80억 원 가치)한다면 이는 인근에 위치한 자사의 결합 기계 및 물류창고 자산집단과의 시너지 연계 하에서만 가능한 구조이다. 만약 토지만을 단독 분할 매각할 때의 가치는 60억 원에 그친다. 이 토지 공정가치 산정 시 최고 최선 사용의 '자산 집단화(Asset Grouping)' 적용에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 최고 최선 사용 전제가 타 자산들과의 결합 사용 시너지를 요구하더라도, 다른 자산들은 무시하고 무조건 단독 처분가치 60억 원을 공정가치로 삼아야 한다.",
            "② 최고 최선 사용이 자산 집단과의 결합 사용을 전제한다면, 토지의 공정가치는 해당 집단(60억 원)을 기준으로 삼되 자본금을 소급해 줄여준다.",
            "③ 최고 최선 사용이 다른 자산들과 결합하여 그룹으로 사용될 때 가치 극대화가 일어난다면, 시장참전자도 동일한 자산 집단 하에서 사용을 가정하여 토지를 평가할 것으로 가정하므로 결합 전제 가치(80억 원의 분배액)를 기초로 공정가치를 결정한다.",
            "④ 토지의 단독 가치와 결합 가치 평균액인 70억 원으로 기재한다.",
            "⑤ 결합 자산들에 감가상각을 원천 금지하는 조건으로 80억 원을 자산에 더해준다."
        ],
        "answer": "3",
        "explanation": "③ 비금융자산의 최고 최선 사용이 타 자산들과의 유기적 결합 사용(자산그룹단위 운용) 시 가치가 최대화되고 시장참전자들도 그렇게 행동할 것이라면, 공정가치 평가 또한 자산집단의 일부로 사용될 것을 전제하여 그에 합당한 가치(80억 원 수준의 지분 배분액)를 기초로 토지의 공정가치를 측정합니다.\n\n[오답 해설]\n① 자산 집단 시너지를 고려하므로 단독 처분 60억 원 고집 명제는 잘못되었습니다.\n② 자본금 소급 감소 지침 등은 왜곡입니다.\n④ 단순 평균 가격(70억 원)은 적용되지 않습니다.\n⑤ 감가상각 강제 금지 등의 처리는 회계 위배입니다.",
        "type": "개념5지",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산그룹 시너지가 합당한 최고 최선 사용 조건이라면 단독 처분액 고집은 오답입니다.", "articles": [], "principle": "최고최선사용 자산집단화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 소급 변경 등의 분개는 틀렸습니다.", "articles": [], "principle": "최고최선사용 자산집단화", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "시장참전자가 자산집단 형태로 운용하여 시너지를 극대화할 것이라 기대되면 결합 사용 상태를 가정하여 공정가치를 산출합니다.", "articles": [], "principle": "최고최선사용 자산집단화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평균가 산정은 불비한 근거입니다.", "articles": [], "principle": "최고최선사용 자산집단화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각 금지 등의 위법적 조건을 가산할 수는 없습니다.", "articles": [], "principle": "최고최선사용 자산집단화", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "J사는 기말 금융부채(사채)의 공정가치 측정을 앞두고 있다. 당해 연도 중 J사의 사업 실패 리스크가 고조되어 시장에서 J사 신용등급이 하락하고 자기신용위험이 급격히 증가하였다. 이 등급 하락에 따른 '자기신용위험 변동액'이 기말 부채 공정가치 평가액과 재무구조에 미치는 실무 적용 영향으로 옳은 설명은?",
        "options": [
            "① 등급 강등으로 사채 할인율이 하락하여 부채의 공정가치가 폭증해 당기 손실을 낳는다.",
            "② 자사의 신용위험이 고조(신용등급 하락)되면 사채 시장 할인율이 상승하므로 기말 사채부채의 공정가치는 하락(감소)하여, 장부 상 부채 총액이 감소하는 결과를 낳는다.",
            "③ 신용등급 변동액의 100배를 계산하여 '자본금' 감액 분개로 반영한다.",
            "④ 금융감독원이 부채를 자산으로 강제 등재해 주므로 부채가 완전 소멸한다.",
            "⑤ 회사의 파산 시점까지 부채 가액 1억 원을 무조건 영업비용으로 전액 상계한다."
        ],
        "answer": "2",
        "explanation": "② 자기신용등급 강등은 해당 기업이 발행한 채무의 시장 가치(공정가치)를 하락시키는 결과를 가져옵니다(시장 참여자의 요구 이자율 스프레드가 증가하기 때문). 따라서 부채 공정가치 장부액이 줄어들어 역설적으로 부채 총액이 감소하게 됩니다.\n\n[오답 해설]\n① 등급 강등 시 할인율이 상승하여 공정가치는 폭락(감소)하므로 오답입니다.\n③ 자본금 강제 감액 100배 기재는 오류입니다.\n④ 금감원의 자산 강제 등재는 실무 상 없습니다.\n⑤ 파산 전 무단 비용 상계는 불허됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "신용 강등 시 스프레드 상승으로 할인율이 올라가 공정가치는 감소하므로 폭증 설명은 거짓입니다.", "articles": [], "principle": "자기신용위험 적용 영향", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자기신용 하락 시 요구수익률이 올라가 회사채 시장 가치가 하락하므로 사채부채 공정가치가 감소하여 부채 장부 가액이 줄어듭니다.", "articles": [], "principle": "자기신용위험 적용 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 강제 상환 100배는 회계 오류입니다.", "articles": [], "principle": "자기신용위험 적용 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채의 자산 강제 대체 규정 등은 실재하지 않습니다.", "articles": [], "principle": "자기신용위험 적용 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 비용 상계는 불허됩니다.", "articles": [], "principle": "자기신용위험 적용 영향", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "K사는 보유 중인 금융주식의 공정가치 측정을 위해 거래소 마감일 공시가격(수준 1)을 기본 가격으로 입수하였다. 그러나 거래소 폐장 직후 발생한 대형 화재 사고 악재 소식이 사후 입수되어, 결산 기재 시 수준 1 가격을 시장 정보 할인율 등 관측가능 변수를 써서 인위 조정(Adjust)하게 되었다. 이 인위 조정을 거친 공정가치 측정치의 최종 공정가치서열 분류 변동으로 가장 옳은 것은?",
        "options": [
            "① 수준 1에 그대로 머무른다.",
            "② 조정을 거쳤고 더 이상 조정하지 않은 활성시장 가격이 아니므로, 수준 1에서 수준 2(또는 조정 수준 유의 시 수준 3)로 변경 분류해야 한다.",
            "③ 금융감독원장의 직권으로 수준 100등급으로 강제 강등 당한다.",
            "④ 가격 조정을 거친 즉시 당해 금융주식은 장부에서 전액 비용으로 삭제 제거된다.",
            "⑤ 주가가 0원으로 고정되므로 수준 분류 자체가 무의미하다."
        ],
        "answer": "2",
        "explanation": "② 수준 1의 핵심 조건은 '조정하지 않은 활성시장의 공시가격'이어야 합니다. 시장 폐장 후 악재 발생 등으로 가격에 인위적 수정이나 조정을 가한 순간, 이는 더 이상 수준 1 변수가 될 수 없고 수준 2(또는 조정액이 매우 크고 관측불가 조건 개입 시 수준 3)로 변경 분류되어 공시되어야 합니다.\n\n[오답 해설]\n① 조정을 가했으므로 수준 1 고정은 틀렸습니다.\n③ 수준 100 등급 등 가상의 등급은 존재하지 않습니다.\n④ 자산의 강제 비용 삭제 제거 처리는 오류입니다.\n⑤ 주가가 자동 0원 고정되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "조정이 유입되는 순간 수준 1 가격 정의를 탈실하므로 수준 1 유지는 불가능합니다.", "articles": [], "principle": "수준 가격의 조정과 등급변동", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공시가격에 조정을 가하면 수준 1 요건(조정하지 않은 가격)을 충족하지 못해 수준 2 또는 수준 3으로 귀속 등급이 변경됩니다.", "articles": [], "principle": "수준 가격의 조정과 등급변동", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가상의 수준 100 등급은 불가능합니다.", "articles": [], "principle": "수준 가격의 조정과 등급변동", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 강제 비용화 제거 지침은 회계 위배입니다.", "articles": [], "principle": "수준 가격의 조정과 등급변동", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가격이 0원 고정된다는 것은 사실이 아닙니다.", "articles": [], "principle": "수준 가격의 조정과 등급변동", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "L사는 해외 수출용 구리 일반상품(Commodity)을 다량 보유하고 있으며 결산일 공정가치 측정을 수행한다. 거래소 정상거래 가격은 1톤당 100만 원이나, L사의 구리 적재 창고는 지방 외곽에 있어 거래소 지정 창고까지 운송하는 데 운송원가 5만 원이 소요된다. 중개 수수료인 거래원가는 3만 원이다. 위치 특성을 반영한 이 구리의 1톤당 공정가치는 얼마인가?",
        "options": [
            "① 92만 원",
            "② 95만 원",
            "③ 97만 원",
            "④ 100만 원",
            "⑤ 102만 원"
        ],
        "answer": "2",
        "explanation": "② 위치가 구리(일반상품)의 고유 특성에 결합되어 있으므로 현재 적재 장소에서 주된 시장까지의 운송 비용은 공정가치에서 직접 차감 조정합니다. (단 중개 거래원가 3만 원은 공정가치 계산 시 차감하지 않습니다.)\n따라서 공정가치 = 100만 원 - 5만 원 = **95만 원**이 됩니다.\n\n[오답 해설]\n① 거래원가 3만 원까지 중복 차감하여 오답입니다. (92만 원은 순공정가치에 해당합니다.)\n③ 운송비 대신 수수료만 차감하여 오답입니다.\n④ 운송원가 차감 조정을 누락해 오답입니다.\n⑤ 운송원가를 오히려 가산하여 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "거래원가인 수수료 3만 원까지 차감 조정하여 공정가치를 계산하면 틀립니다.", "articles": [], "principle": "위치보정 공정가치 산출", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "위치 특성 운송원가 5만 원은 차감 조정하되 수수료 3만 원은 배제하므로 공정가치는 95만 원이 정확합니다.", "articles": [], "principle": "위치보정 공정가치 산출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수수료만 공제한 계산식은 틀렸습니다.", "articles": [], "principle": "위치보정 공정가치 산출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "운송원가 5만 원 공제를 누락한 오류입니다.", "articles": [], "principle": "위치보정 공정가치 산출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "운송비를 합산 가산하여 가액을 부풀린 것은 오류입니다.", "articles": [], "principle": "위치보정 공정가치 산출", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "M사는 보유 중인 기계장치에 대해 시장참전자의 사용/매도 제약 요건이 공정가치 측정에 미치는 영향을 분석하고 있다. 이 제약 조건이 '자산 자체의 특성(예: 환경오염 유발 설비로 정부의 양도 시 정화 의무 박제)'인 경우와 '보유자 개인의 일시적인 특성(예: M사가 채무 불이행으로 채권자 압류 조치를 당해 자산 매각이 임시 금지됨)'일 때의 공정가치 반영 여부에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 두 제약 조건 모두 공정가치 측정 시 무조건 100% 반영하여 장부가액을 0원으로 감액해야 한다.",
            "② 두 제약 조건 모두 공정가치 측정에 아무런 영향도 미치지 못하므로 전면 배제한다.",
            "③ 자산 자체의 특성에 해당하는 제약 조건은 시장참전자도 가격 결정 시 반영하므로 공정가치 측정에 반영하지만, 보유자 개인의 일시적 압류 등 제약은 자산 고유 특성이 아니므로 공정가치 측정 시 반영하지 않는다.",
            "④ 보유자 개인의 제약만 반영하고 자산 특성 제약은 주석 기재도 누락하는 편법을 쓴다.",
            "⑤ 두 제약이 발생하면 기계장치를 즉시 전액 자본금 감액 상계 처리한다."
        ],
        "answer": "3",
        "explanation": "③ 공정가치는 특정 보고기업 고유의 특성이 아닌 시장 참여자 일반의 관점을 반영합니다. 따라서 자산 자체에 영구 결합된 제약은 자산의 특성이므로 공정가치 측정 시 당연 반영(가격 감소 요인)되나, 보고기업 개인의 임시적인 재무적 매각 제약(압류 등)은 자산 자체의 특성이 아니므로 공정가치에서 제외하는 것이 올바른 적용입니다.\n\n[오답 해설]\n① 0원으로 전액 감액할 사유가 아닙니다.\n② 자산 자체 특성 제약마저 배제하는 것은 가치 왜곡입니다.\n④ 반영 여부가 반대로 작성되었습니다.\n⑤ 자본 상계 감자 분개는 불법 회계입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "두 제약을 동액 0원 감액할 이유는 없습니다.", "articles": [], "principle": "제약 특성과 공정가치 반영", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 고유 특성 제약까지 배제하는 명제는 틀렸습니다.", "articles": [], "principle": "제약 특성과 공정가치 반영", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산 자체의 특성에 기인한 용도 제약 등은 공정가치에 반영하나, 기업 특유의 개별 사적 제약은 가치 평가에서 제외합니다.", "articles": [], "principle": "제약 특성과 공정가치 반영", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "반영 대상 설명이 거꾸로 되어 틀렸습니다.", "articles": [], "principle": "제약 특성과 공정가치 반영", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 감 상계 처리는 틀린 처리입니다.", "articles": [], "principle": "제약 특성과 공정가치 반영", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "N사는 미래 현금흐름 할인모형(이익접근법)을 사용하여 장기 투자 채무의 공정가치를 추정하고 있다. 현금흐름 할인 시 사용되는 시장 할인율(시장 금리)에 반영되어 조정되어야 하는 요건에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 무위험 이자율에다가 시장 참여자들이 요구하는 신용 스프레드 및 위험 프리미엄을 모두 적절히 가산 반영하여 할인율을 구성한다.",
            "② 금융기관의 우대금리 단 한 가지만을 어떠한 조정도 없이 무조건 5%로 고정해 쓴다.",
            "③ 기업의 내부 목표 자본비용률을 대표이사 서명만 받아 자의적으로 가산 반영한다.",
            "④ 이자율이 높을수록 자산 가치가 급증하도록 할인율을 음(-)의 값으로 변조한다.",
            "⑤ 세무상 이자 비용 면제 혜택 한도를 비례하여 매달 일일 할인율로 쓴다."
        ],
        "answer": "1",
        "explanation": "① 미래 기대 현금흐름의 현재가치(공정가치)를 구하기 위한 할인율은, 기본 시간가치인 무위험 이자율에 해당 채무의 위험 수준(신용 스프레드 등 시장참전자 요구 프리미엄)을 적절히 반영하여 복합적으로 도출해야 합니다.\n\n[오답 해설]\n② 우대금리 단독 5% 고정은 임의의 수치 기재입니다.\n③ 대표의 자의적 내부 목표 비율을 공정가치 할인율로 강제할 수는 없습니다(시장 기준 우선).\n④ 할인율을 음수로 기재하는 변조 처리는 불법입니다.\n⑤ 세법 이자 면제 혜택 한도는 할인율 산정의 보편적 기준이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "이익접근법 적용 할인율은 시간가치(무위험률)와 대상 자산·부채의 특수한 신용/시장 위험 프리미엄을 종합 내포해 결정됩니다.", "articles": [], "principle": "할인율의 구성 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "5% 임의 고정 처리는 오답입니다.", "articles": [], "principle": "할인율의 구성 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "내부 주관적 목표율을 시장참전자용 공정가치 할인율에 맹목적으로 쓸 수는 없습니다.", "articles": [], "principle": "할인율의 구성 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "할인율의 음수 변조 기재는 비상식적인 왜곡입니다.", "articles": [], "principle": "할인율의 구성 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 한도 연계 매일 할인율 설명은 거짓입니다.", "articles": [], "principle": "할인율의 구성 요건", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "O사는 결산보고일을 맞아 비금융자산인 상업용 빌딩의 공정가치 측정 내역을 공시하려 한다. 현재 이 빌딩의 최고 최선 사용은 '상업용 오피스 임대'로 평가되었으나, O사는 이를 현재 사내 직원 보육시설 및 연구동 용도로 특수 사용(내부 사용)하고 있다. 이 비금융자산의 기말 공시 및 가치 측정 보고 지침으로 가장 올바른 것은?",
        "options": [
            "① O사가 사내 보육용으로 쓰고 있으므로 최고 최선 임대 가치는 무시하고 보육시설 가치로만 낮추어 장부에 적고 공시는 일체 생략한다.",
            "② 자산의 측정가액 자체는 시장참전자 관점인 최고 최선 사용(임대 가치) 금액을 기초로 공정가치를 산정하여 재무상태표 본문에 반영하되, 현재의 사용 목적(보육시설)이 최고 최선 사용과 다르다는 그 사실과 이유 등을 재무제표 주석에 상세 공시하여 이용자에게 정보 보고를 수행한다.",
            "③ 빌딩의 가치가 상승한 차액 전체를 '기부금' 비용으로 당기 손익에 마이너스 반영한다.",
            "④ 건물의 감가상각을 원천 소급 취소하고 자본잉여금을 10배 늘려 보고한다.",
            "⑤ O사의 건물 소유권을 즉시 국세청으로 등기 이전해 주어 공시 부담을 회피한다."
        ],
        "answer": "2",
        "explanation": "② 비금융자산의 공정가치는 최고 최선 사용(임대 가치)을 기초로 본문에 기재하되, 현재 실제 용도(보육시설)가 최고 최선 사용(임대)과 다른 예외적 상태에 있다면 이 사실과 구체적 배경 사유를 이용자 소통을 위해 주석으로 상세 설명 공시해야 합니다.\n\n[오답 해설]\n① 임의로 낮추어 적고 공시를 생략하는 처리는 성실성 위배입니다.\n③ 증가 차액을 기부금 비용으로 처리하는 분개는 이론 상 어긋납니다.\n④ 감가상각의 소급 취소 및 자본잉여금 10배 갱신은 분식회계입니다.\n⑤ 소유권 무단 이전 설명은 비상식적 회계 회피책입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "실제 용도에 얽매여 공정가치 본문 평가를 임의 감액 방치하는 것은 기준 위반입니다.", "articles": [], "principle": "최고 최선 사용과 실제 사용 불일치", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가치는 최고 최선 사용 기준으로 평가하되, 실제 용도와의 불일치 사실과 구체적인 배경 사유는 주석으로 투명하게 주석 공시합니다.", "articles": [], "principle": "최고 최선 사용과 실제 사용 불일치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상승액을 당기 기부금 비용 차감으로 잡지 못합니다.", "articles": [], "principle": "최고 최선 사용과 실제 사용 불일치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각 소급 취소 및 자본잉여금 과장은 분식회계에 귀속됩니다.", "articles": [], "principle": "최고 최선 사용과 실제 사용 불일치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "국세청 소유 명의 이전을 통한 공시 회피설은 불가능합니다.", "articles": [], "principle": "최고 최선 사용과 실제 사용 불일치", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },

    # =========================================================================
    # L4: 분석 (8문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s09-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "공정가치 측정 기준서(IFRS 제1113호)상 공정가치 가액 결정 및 거래원가와 운송원가의 처리 규칙에 관한 설명 중 옳은 보기만을 모두 고른 것은?\n\n```\nㄱ. 공정가치는 특정 보고기업의 시너지를 대변하는 기업특유가치가 아니라 시장참전자들의 관점을 대변하는 시장 기준 가격이다.\nㄴ. 자산이나 부채의 공정가치 가격 자체에서 최초 취득이나 양도 거래와 관련된 거래원가를 직접 가산하거나 차감 조정하지 아니한다.\nㄷ. 자산의 위치가 자산 고유 특성에 해당하는 경우, 시장까지 도달하기 위한 운송원가는 공정가치에서 직접 차감 조정한다.\nㄹ. 순공정가치는 산정된 공정가치에서 거래원가를 차감하여 도출한다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄴ, ㄷ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "5",
        "explanation": "⑤ ㄱ, ㄴ, ㄷ, ㄹ 모두 공정가치의 본질(시장 기준 가격, 유출가격), 그리고 거래원가(미공제)와 운송원가(위치 특성 시 공제) 및 순공정가치 산출 정의를 정확하게 기술하고 있어 모두 참입니다.\n\n[오답 해설]\n①, ②, ③, ④는 참인 보기들의 일부를 누락하여 틀린 조합입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄷ, ㄹ도 참이므로 누락 조합인 1은 틀렸습니다.", "articles": [], "principle": "공정가치 원가규칙 종합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ, ㄹ도 올바른 기준서 서술입니다.", "articles": [], "principle": "공정가치 원가규칙 종합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ도 참입니다.", "articles": [], "principle": "공정가치 원가규칙 종합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ도 참입니다.", "articles": [], "principle": "공정가치 원가규칙 종합", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ(공정가치의 성격), ㄴ(거래원가 미조정), ㄷ(운송원가 차감), ㄹ(순공정가치 산출원리) 모두 기준서 내용과 합치하는 참입니다.", "articles": [], "principle": "공정가치 원가규칙 종합", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "공정가치 측정 시 적용하는 주된 시장(Principal Market)과 가장 유리한 시장(Most Advantageous Market)에 관한 설명 중 가장 올바르지 않은 서술은?",
        "options": [
            "① 공정가치 측정은 자산을 매도하거나 부채를 이전하는 거래가 주된 시장에서 이루어진다고 우선 가정한다.",
            "② 주된 시장이 존재하지 않는 경우에 한하여 가장 유리한 시장의 가격을 공정가치 평가 기준으로 적용한다.",
            "③ 주된 시장은 보고기업이 측정일에 해당 시장에 접근 가능해야 하지만, 가장 유리한 시장은 접근 요건이 면제되므로 접근할 수 없는 가상의 우량 해외 시장을 임의 지정하여 가격을 원용해도 합법이다.",
            "④ 주된 시장은 해당 자산이나 부채의 거래 빈도와 거래량이 최대인 시장을 기준으로 판별하며, 보고기업 개별 거래량이 최대인 시장을 뜻하진 않는다.",
            "⑤ 가장 유리한 시장을 '결정(판단)'할 때는 거래원가와 운송원가를 모두 순수익액 대조 시 차감 고려하여 결정한다."
        ],
        "answer": "3",
        "explanation": "③ 주된 시장뿐 아니라 주된 시장이 없어 선택하게 되는 '가장 유리한 시장' 역시, 보고기업이 측정일에 반드시 '접근할 수 있어야(접근 가능성 요건)' 합니다. 접근조차 불가능한 해외 차단 시장의 가격을 공정가치 측정을 위해 끌어다 쓸 수는 없습니다.\n\n[오답 해설]\n①, ② 주된 시장 우선 및 가장 유리한 시장 보완 적용은 공정가치의 핵심 시장 대입 기본 원칙입니다.\n④ 주된 시장은 개별 기업의 1회사 단독 거래량이 아닌 전체 시장의 빈도/부피를 잣대로 판단합니다.\n⑤ 가장 유리한 시장 판단비교 시에는 순매득액(순공정가치) 크기를 비교하므로 운송/거래 원가를 모두 차감합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "주된 시장 최선 가정 원칙은 올바른 참입니다.", "articles": [], "principle": "시장 판단 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가장 유리한 시장의 차선책 보완 사용 설명은 참입니다.", "articles": [], "principle": "시장 판단 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가장 유리한 시장 역시 보고기업의 접근 요건 충족이 필수적이므로 접근 없이 임의 원용해도 된다는 3의 진술은 명백한 오류입니다.", "articles": [], "principle": "시장 판단 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전체 시장의 거래량과 빈도가 판단 잣대라는 설명은 참입니다.", "articles": [], "principle": "시장 판단 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유리한 시장 판단(비교) 시 거래원가와 운송원가를 모두 순액 차감하는 것은 참입니다.", "articles": [], "principle": "시장 판단 정오 분석", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "question_type": "개념5지",
        "question": "공정가치 측정 시 적용하는 세 가지 가치평가기법과 기법 변경 회계처리에 관한 진술 중 옳지 않은 것만을 고른 것은?\n\n```\nㄱ. 시장접근법은 동일하거나 비교할 수 있는 자산·부채의 시장 거래 생성 가격 정보를 사용한다.\nㄴ. 이익접근법은 미래 예상 금액을 현재의 할인된 단일 금액으로 전환하여 평가한다.\nㄷ. 원가접근법은 자산의 사용 능력을 대체할 때 현재 필요한 금액(통상 현행대체원가)을 반영한다.\nㄹ. 공정가치 측정을 위해 사용하던 가치평가기법을 변경하는 수정은 회계정책의 변경에 해당하므로 관련 과거 재무제표를 소급 재작성한다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄹ",
            "④ ㄱ, ㄹ",
            "⑤ ㄴ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ ㄹ 단 하나만이 옳지 않은 서술(거짓 진술)입니다.\n\n[오답 해설]\nㄹ. 가치평가기법이나 적용방법의 변경 수정은 회계정책의 변경이 아니라 '회계추정의 변경'에 해당하므로 소급하지 않고 전진적으로 당기와 미래에 적용합니다.\n(ㄱ, ㄴ, ㄷ은 기준서가 명시한 3대 평가기법의 충실한 정의 설명으로 참입니다.)",
        "option_meta": [
            {"correct": False, "why": "ㄱ, ㄴ은 참이므로 옳지 않은 것 고르기 대상이 아닙니다.", "articles": [], "principle": "평가기법 및 변경 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ, ㄷ이 참입니다.", "articles": [], "principle": "평가기법 및 변경 정오", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄹ은 정책의 변경 소급법이라 명시해 기준서(추정의 변경 전진법)와 배치되는 오류입니다.", "articles": [], "principle": "평가기법 및 변경 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ이 참이므로 대상이 아닙니다.", "articles": [], "principle": "평가기법 및 변경 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ이 참이므로 잘못 묶인 조합입니다.", "articles": [], "principle": "평가기법 및 변경 정오", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "공정가치서열체계(Fair Value Hierarchy)의 수준 1~3 투입변수 적용 및 공시 기준에 관한 설명 중 가장 옳지 않은 것은?",
        "options": [
            "① 공정가치서열체계는 동일 자산·부채 활성시장 공시가격에 가장 높은 수준 1 순위를 주며, 관측불가능 투입변수에 가장 낮은 수준 3을 부여한다.",
            "② 공정가치서열체계는 가치평가기법에의 투입변수에 우선순위를 부여하는 것이지, 공정가치를 측정하기 위해 사용하는 가치평가기법 자체에 우선순위를 부여하는 것은 아니다.",
            "③ 하나의 자산의 공정가치를 측정할 때 2개 이상의 수준의 투입변수가 혼합 적용된다면, 전체 측정치 수준은 유의적이면서 '가장 낮은 수준'으로 분류한다.",
            "④ 관측가능한 투입변수(수준 2)를 관측할 수 없는 투입변수(수준 3)를 써서 유의적으로 조정한 결과물은 서열체계 상 최우선 등급인 '수준 1'로 강제 격상 분류된다.",
            "⑤ 수준 1의 공시가격에 다른 요소를 임의 가산하여 인위 조정한 가격은 수준 1에서 배제되며 수준 2나 수준 3으로 귀속된다."
        ],
        "answer": "4",
        "explanation": "④ 관측가능한 변수를 관측할 수 없는 변수를 사용해 유의적으로 조정한 경우, 그 조정으로 인해 측정치 결과가 크게 변하므로 신뢰성이 관측불가 조건에 오염된 것으로 보아 서열체계 상 최하위 순위인 **수준 3**으로 하향 분류해야지 수준 1로 격상시킬 수 없습니다.\n\n[오답 해설]\n① 서열체계의 기본 정의입니다.\n② 기법 자체에 우선순위를 부여하지 않는다는 것은 올바른 설명입니다.\n③ 혼합 시 최저 수준 분류 규칙은 참입니다.\n⑤ 수준 1 공시가는 '조정하지 않아야' 성립하므로, 조정한 즉시 수준 1에서 배제됨은 참입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "서열체계 등급의 기본 설명으로 참입니다.", "articles": [], "principle": "서열체계 조문 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가치평가기법 자체에 우선순위를 주지 않는다는 설명은 참입니다.", "articles": [], "principle": "서열체계 조문 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "혼입 시 최저 수준 귀속 규정은 올바른 참 서술입니다.", "articles": [], "principle": "서열체계 조문 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "관측불가 요소를 결합해 유의적 수정을 했다면 신뢰 등급이 가장 낮은 수준 3으로 떨어지므로 수준 1 격상설은 완전 오류입니다.", "articles": [], "principle": "서열체계 조문 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조정이 들어간 가격의 수준 1 배제 규정은 참입니다.", "articles": [], "principle": "서열체계 조문 분석", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "공정가치 측정 기준서상 비금융자산의 최고 최선 사용(Highest and Best Use)에 관한 설명 중 가장 옳지 않은 진술은?",
        "options": [
            "① 최고 최선 사용은 비금융자산에 대해서만 고려하며, 금융자산의 공정가치 측정 시에는 최고 최선 사용의 개념을 적용하지 않는다.",
            "② 최고 최선 사용을 판단할 때는 시장참전자의 관점에서 판단하며, 기업이 다르게 사용할 의도가 있더라도 시장참전자 기대를 배제할 수 없다.",
            "③ 시장참전자가 비금융자산을 다르게 사용하여 가치를 극대화할 것이라는 점이 다른 요소에 의해 제시되지 않는 한, 기업이 비금융자산을 현재 사용하는 것을 최고 최선 사용으로 본다.",
            "④ 최고 최선 사용은 물리적으로 가능하고, 법적으로 허용되며, 재무적으로 실현가능해야 한다.",
            "⑤ 최고 최선 사용이 자산집단과의 결합 사용을 전제하더라도, 개별 토지 등은 집단과의 시너지를 차단하고 무조건 단독 매각 형태의 가격으로만 본문에 기재해야 한다."
        ],
        "answer": "5",
        "explanation": "⑤ 최고 최선 사용이 타 자산들과 결합하여 그룹으로 사용될 때 가치 극대화가 일어난다면(예: 공장 부지와 공장 건물 설비의 결합 운용), 시장참전자도 동일한 자산 집단 하에서 사용을 가정하여 토지를 평가할 것으로 가정하므로 단독 강제 매각 처분가로 장부에 올리지 않습니다. 자산집단 하의 가치를 기준으로 배분합니다.\n\n[오답 해설]\n① 최고 최선 사용은 실물이 있는 비금융자산에 국한하여 적용합니다.\n② 소유 기업 의도와 별개로 시장참전자 시각을 따릅니다.\n③ 별도 증거가 없으면 현 사용 목적을 최고 최선 사용으로 봅니다.\n④ 물리적/법적/재무적 3대 성립 조건은 바릅니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비금융자산에만 적용한다는 규정은 정당한 사실입니다.", "articles": [], "principle": "최고 최선 사용 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시장참전자 관점 판단과 소유자 의사 무관성은 참입니다.", "articles": [], "principle": "최고 최선 사용 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현재의 용도를 우선적 최고 최선으로 간주하는 규칙은 참입니다.", "articles": [], "principle": "최고 최선 사용 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "3대 조건(물리적, 법적, 재무적) 설명은 정확합니다.", "articles": [], "principle": "최고 최선 사용 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "결합 사용 하에서 가치 극대화 시에는 집단화 가정을 적용하므로 무조건 단독가 기재를 강제한다는 지문은 오답입니다.", "articles": [], "principle": "최고 최선 사용 분석", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "공정가치 측정 기준서상 부채와 자기지분상품의 공정가치 측정 시 적용하는 세부 지침 설명으로 가장 옳지 않은 것은?",
        "options": [
            "① 동일하거나 비슷한 부채/지분상품 이전 가격 공시가 없더라도, 상대방이 자산으로 보유 중이면 자산 보유자 시장참전자 관점에서 측정한다.",
            "② 부채의 공정가치는 기업 자신의 신용위험(자기신용위험)을 포괄하는 불이행위험의 효과를 포함해야 한다.",
            "③ 상대방이 부채를 자산으로 보유하고 있는 금융자산 가격이 관측 가능하다면, 자사의 부채 공정가치 측정 시 그 금액을 직접 사용할 수 있다.",
            "④ 부채와 지분상품을 상대방이 자산으로 보유하지 않은 완전 불비 상황에서는, 채권자(수령자)의 임의 요구 이자율을 기말 자산 합계에 100배로 곱해 결정한다.",
            "⑤ 부채의 불이행위험은 부채의 이전 전후로 동일하게 유지되는 것으로 가정한다."
        ],
        "answer": "4",
        "explanation": "④ 부채/지분을 상대방이 자산으로 보관하지 않는 특수 상황에서는, 채권자 수령가액에 임의의 100배 곱셈을 하여 결정하는 무근본 연산이 아니라, 부채 부담자/발행 시장참전자 관점에서 적절한 가치평가기법을 설계(발행자 관점의 할인법 등)하여 측정합니다.\n\n[오답 해설]\n① 상대방 자산 유보 시 관점 규칙은 정당합니다.\n② 불이행위험 및 자기신용위험 반영은 필수 요건입니다.\n③ 관측 금융자산 가격 원용 가능 조항은 참입니다.\n⑤ 이전 전후에 불이행위험이 승계되어 같다는 가정이 적용됨은 참입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상대방 자산 보유 시 관용 조항은 참입니다.", "articles": [], "principle": "부채 공정가치 조문 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "불이행위험(자기신용포함) 반영은 부채 공정가치의 의무 규정입니다.", "articles": [], "principle": "부채 공정가치 조문 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융자산 공시가격의 직접 수용 가능 서술은 참입니다.", "articles": [], "principle": "부채 공정가치 조문 정오", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "채권자 요구율의 100배 곱셈을 통한 자산총액 기재 등의 편법 처리는 불법이므로 4가 오답입니다.", "articles": [], "principle": "부채 공정가치 조문 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "불이행위험이 이전 전후로 일정하다는 전제는 참입니다.", "articles": [], "principle": "부채 공정가치 조문 정오", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "공정가치 측정에 영향을 미치는 운송원가(Transportation Cost)와 거래원가(Transaction Cost) 및 시장의 접근 가능성(Accessibility)에 대한 설명 중 가장 옳지 않은 것은?",
        "options": [
            "① 가장 유리한 시장을 '판단'하기 위해 두 시장의 순매득액을 계산할 때는 거래원가와 운송원가를 모두 차감하여 대조한다.",
            "② 가장 유리한 시장이 결정되고 그 시장 정보를 활용해 '공정가치' 수치 자체를 도출해 낼 때는 거래원가는 차감하지 않고 운송원가만 차감해야 한다.",
            "③ 보고기업은 측정일에 주된 시장 또는 가장 유리한 시장에 직접 거래를 체결하여 접근할 수 있는 물리적·제도적 역량을 충족하고 있어야 한다.",
            "④ 거래원가는 자산을 매도하거나 부채를 이전하는 정상거래를 위해 필수 불가결한 직접 부대 원가이므로, 공정가치 계산에 당연히 차감되어야만 자산 총액을 현실성 있게 낮춰준다.",
            "⑤ 공정가치 측정일에 특정 자산을 매도할 수 있거나 특정 부채를 이전할 수 있어야만 하는 것은 아니며, 보고기업이 해당 시장에 접근할 수만 있으면 가격 정보 원용이 성립한다."
        ],
        "answer": "4",
        "explanation": "④ 공정가치는 거래원가로 인해 증가하거나 감소하지 않습니다(IFRS 제1113호). 따라서 거래원가는 공정가치 계산 시 차감하지 않고 배제해야 하며, 당연히 차감하여 자산 총액을 낮춘다는 서술은 거짓입니다.\n\n[오답 해설]\n① 시장의 우열 '비교 단계'에 순공정가치를 쓰므로 원가 둘 다 빼는 것은 참입니다.\n② 실제 공정가치 수치 확정 시 거래원가를 배제하고 운송비만 차감함은 매우 까다롭고 빈출되는 참 명제입니다.\n③, ⑤ 해당 시장에 접근할 수 있어야 하지만 당일 즉시 매각을 강제하지 않는다는 조항은 참입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "가장 유리한 시장 비교 시에 순공정가치를 적용하므로 두 원가를 빼서 판단한다는 것은 참입니다.", "articles": [], "principle": "원가 조정과 접근성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치 확정액에는 운송원가만 조정하고 거래원가는 배제하는 조항은 참입니다.", "articles": [], "principle": "원가 조정과 접근성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시장의 접근가능성(Accessibility) 확보 요건은 올바른 설명입니다.", "articles": [], "principle": "원가 조정과 접근성 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "거래원가를 공정가치에서 직접 차감 조정하지 않는 것이 명백한 기준이므로, 당연 차감해야 자산을 현실성 있게 낮춘다는 지문은 오답입니다.", "articles": [], "principle": "원가 조정과 접근성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "접근 권한이 있으면 족하지 당일 즉시 거래 강제가 요건이 아님은 참입니다.", "articles": [], "principle": "원가 조정과 접근성 분석", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "공정가치 측정에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 공정가치는 특정 보고기업의 고유한 경영 의도를 무시한 시장에 근거한 측정치이다.",
            "② 공정가치 측정은 정상거래의 유출가격을 반영하므로 역사적원가처럼 취득할 때의 투입가격과는 엄격히 구분된다.",
            "③ 관측가능한 투입변수의 활용도를 극대화하고 관측불가능한 투입변수의 사용을 최소화하도록 가치평가 모델을 가동해야 한다.",
            "④ 공정가치서열체계는 시장 공시가격인 수준 1 투입변수의 순위가 가장 높다.",
            "⑤ 활성시장에서 관측되는 동일 자산의 공가격에 일부 신용스프레드 조정을 가산 반영하더라도, 여전히 등급은 가장 신뢰성이 높은 '수준 1'로 분류 유지된다."
        ],
        "answer": "5",
        "explanation": "⑤ 수준 1의 핵심 조건은 '조정하지 않은 활성시장의 공시가격'이어야 합니다. 시장 가격에 추가적인 조정(신용 스프레드 가산 등)을 가한 순간, 이는 더 이상 수준 1의 정의를 만족하지 못하므로 수준 2나 수준 3으로 귀속 변경해야 하며 수준 1 유지는 불가능합니다.\n\n[오답 해설]\n①, ②, ③, ④는 공정가치의 기본 정의(유출가, 비기업특유), 투입변수 사용 우선순위, 서열체계 요건을 바르게 진술한 참 명제들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "시장에 근거한 측정치 설명은 정당한 사실입니다.", "articles": [], "principle": "공정가치 종합 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유출가격 속성을 가지므로 최초 투입원가와 대조됨은 참입니다.", "articles": [], "principle": "공정가치 종합 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "관측 변수 극대화 및 관측불가 최소화 지침은 올바릅니다.", "articles": [], "principle": "공정가치 종합 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수준 1 공시가격의 최우선 순위 규정은 참입니다.", "articles": [], "principle": "공정가치 종합 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "조정이 들어간 가격은 수준 1에 유지될 수 없고 하위 수준으로 변경 공시되어야 하므로 5의 유지 서술은 명백한 오류입니다.", "articles": [], "principle": "공정가치 종합 분석", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },

    # =========================================================================
    # L5: 심화 (2문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s09-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "비금융자산의 '최고 최선 사용(Highest and Best Use)' 가정을 수립할 때, 자산 자체의 법적 규제(용도 제한)와 재무적 실현가능성의 상충 조건 하에서 시장참전자의 기대를 반영하여 공정가치를 결정하는 회계학적 메커니즘에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 물리적 사용이 가능하더라도 법적 규제로 용도 변경이 원천 금지되어 있다면, 변경 후 시나리오의 가치는 최고 최선 사용으로 채택될 수 없다.",
            "② 용도 변경 완화가 미래에 실현 가능하다고 시장 참여자들이 기대하고 이를 가격 결정에 반영하고 있다면, 비록 현재 시점에는 법적 규제가 풀리지 않았더라도 규제 완화 확률과 비용을 반영하여 용도 변경 후의 가정을 최고 최선 사용으로 채택해 공정가치를 측정할 수 있다.",
            "③ 최고 최선 사용은 보고기업 고유의 특수한 사용 방안이 아니라, 시장 참여자 일반이 내릴 객관적 의사결정 기대를 기준으로 자산 가치를 최대화하는 방식을 대변한다.",
            "④ 기업이 재무적 청산 절차(Liquidation)에 들어가 자산의 조속한 강제 처분이 불가피한 상황이라도, 기말 재무상태표의 토지 공정가치는 무조건 '공장 영구 존속 사용'의 계속기업 전제 가액인 최고가로만 고정 기재하고 처분부대원가 차감 정보를 은폐해야 한다.",
            "⑤ 최고 최선 사용이 현재의 사용 목적(예: 사택 등)과 다르며 다른 대안적 용도(예: 상업 빌딩 등)의 가치가 훨씬 큼에도 기업이 현재 사용을 고수하고 있다면, 공정가치는 대안적 용도 기준으로 본문에 평가 적되, 용도 불일치 사실과 배경 사유는 주석으로 투명하게 주석 공시해야 한다."
        ],
        "answer": "4",
        "explanation": "④ 기업이 계속기업가정을 위배하여 실질적인 청산 절차에 돌입하고 조기 매각 처분이 강제된다면, 시장 참여자들의 가정 역시 조기 유출 가격(처분부대원가 공제 및 급매 처분가 등)에 맞춰 갱신될 것입니다. 무조건 계속기업 상태의 고액 가격으로 고정 기재하고 처분원가를 은폐하라는 서술은 중립성과 충실한 표현 원칙을 파괴하는 불법 오류입니다.\n\n[오답 해설]\n① 법적 불가능 시 최고 최선 사용 불성립 서술은 참입니다.\n② 규제 완화 기대를 반영한 공정가치 측정 가능성은 KAPA/CPA 심화 단골 참 조문입니다.\n③ 시장참전자 관점의 정의를 바르게 설명했습니다.\n⑤ 최고 최선 사용과 실제 용도 불일치 시 본문 평가 및 주석 기술 원칙의 심도 있는 바른 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "법적 규제 완화 불능 시 최고최선 사용 채택 불가는 참입니다.", "articles": [], "principle": "최고 최선 사용 심화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시장 참여자들의 용도 변경 기대 및 관련 비용/확률을 반영한 최고 최선 사용 평가 가능성은 참입니다.", "articles": [], "principle": "최고 최선 사용 심화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "객관적 시장 관점의 가치 극대화 판단 원칙은 참입니다.", "articles": [], "principle": "최고 최선 사용 심화", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "청산이 확실하여 급매 처분이 강제되는 상황에서도 계속기업의 고액 가치를 고집하고 원가를 은폐하라는 진술은 완전한 분식 조장이므로 오답입니다.", "articles": [], "principle": "최고 최선 사용 심화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실제 사용 불일치 시의 본문 평가 및 주석 병행 공시 규칙은 참입니다.", "articles": [], "principle": "최고 최선 사용 심화", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s09-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "공정가치서열체계상 수준 2(Level 2)의 투입변수를 사용한 가치평가에 있어, 시장의 일시적 비활성화로 인해 발생한 유동성 할인(Liquidity Discount) 등의 관측할 수 없는 조정액(Unobservable Adjustment)을 결합시킬 때, 이 조정의 유의성(Significance) 여부에 따른 서열 수준 전이(Level Transition) 및 공시 부담에 관한 심층 분석 중 가장 올바르지 않은 설명은?",
        "options": [
            "① 관측불가능한 조정액이 가치평가 결과 전체에 비해 지극히 미미하여 무시해도 될 수준(유의적이지 않음)이라면, 최종 공정가치 등급은 기존 '수준 2'에 그대로 머무를 수 있다.",
            "② 관측불가능한 조정액이 가치평가 결과에 상당한 왜곡이나 금액 변동을 낳을 정도로 크다면(유의적임), 수준 2에서 '수준 3'으로 귀속 등급이 전이(Transition)되어 공시되어야 한다.",
            "③ 수준 3으로 공정가치 측정 등급이 분류되면, 보고기업은 기말 재무보고 시 자산 가액뿐만 아니라 관측할 수 없는 주요 투입변수의 가정도 주석에 명시하고 민감도 분석(Sensitivity Analysis) 결과까지 상세히 기술해야 하는 등 공시 부담이 크게 가중된다.",
            "④ 금융자산이 수준 3으로 떨어지면 회사는 당기순이익 조작을 목적으로 주관적 조정 비율을 매달 10배씩 임의 변경하고 주석에는 '영업비밀'로 처리해 은폐해도 회계법상 전적으로 면죄부가 부여된다.",
            "⑤ 관측가능 투입변수를 관측불가능 조정변수로 대폭 수정한 결과가 수준 3 분류로 귀속되는 것은, 정보 이용자에게 재무보고 공시 정보의 주관성과 추정 위험을 투명하게 경고하기 위함이다."
        ],
        "answer": "4",
        "explanation": "④ 수준 3 분류는 주관적 추정이 많이 개입된 등급이므로 회계 기준서 및 공시법에 따라 가장 가혹하고 까다로운 설명 의무(민감도 분석, 자체 변수 값 명시, 변동 대사 등)가 강제됩니다. 임의 조작 후 영업비밀 핑계로 이를 누락하거나 은폐하는 기재는 즉각적인 회계 부정 및 처벌 대상이 되며 면죄부는 결코 주어지지 않습니다.\n\n[오답 해설]\n① 유의적이지 않은 조회의 경우 수준 2 유지 가능성에 대한 참 서술입니다.\n② 유의적인 관측불가 변수 개입 시 수준 3 전이 원칙의 바른 설명입니다.\n③ 수준 3 분류 시 수반되는 무거운 공시 부담(민감도 분석 등)의 실무적 영향력 서술로 참입니다.\n⑤ 수준 3 분류 제도가 지닌 궁극적인 정보 유용성 보전(추정 리스크 경고) 목적에 관한 타당한 분석입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "미미한 관측불가 조정 개입 시 수준 2 유지는 참입니다.", "articles": [], "principle": "서열체계 등급의 전이", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유의적인 관측불가 요인 개입 시 수준 3 하락 분류는 참입니다.", "articles": [], "principle": "서열체계 등급의 전이", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수준 3 귀속 시 수반되는 주석의 민감도 분석 및 공시 부담 상술은 사실입니다.", "articles": [], "principle": "서열체계 등급의 전이", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수준 3 분류 시에는 은폐 면제 혜택이 없으며 되려 가장 엄격한 상세 주석 공시 책임(할인율 등 변수 값 상세 보고)이 뒤따르므로 4가 오답입니다.", "articles": [], "principle": "서열체계 등급의 전이", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "서열체계 분류 제도가 갖는 투자자 보호 및 투명성 보완 취지 설명은 참입니다.", "articles": [], "principle": "서열체계 등급의 전이", "case": {"holding": "", "no": None}}
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
                "item": "9절 공정가치"
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
