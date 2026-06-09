import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

if DB_PATH.exists():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)
    print(f"Loaded existing {len(questions)} questions.")
else:
    questions = []
    print("No existing questions file found. Creating new list.")

new_questions = [
    # =========================================================================
    # L1: 기초 개념 (10문항, 501~510번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s01-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 상 재무제표의 근본적인 목적으로 가장 올바르지 않은 것은?",
        "options": [
            "① 광범위한 정보이용자의 경제적 의사결정에 유용한 기업의 재무상태 정보를 제공하는 것",
            "② 광범위한 정보이용자의 경제적 의사결정에 유용한 기업의 재무성과 정보를 제공하는 것",
            "③ 광범위한 정보이용자의 경제적 의사결정에 유용한 기업의 재무상태변동 정보를 제공하는 것",
            "④ 위탁받은 자원에 대한 경영진의 수탁책임 결과를 보여주는 것",
            "⑤ 개별 주주가 개인적으로 거래하는 사적 주식 거래의 최적 매매 타이밍을 결정해 주는 것"
        ],
        "answer": "5",
        "explanation": "⑤ K-IFRS 상 재무제표의 목적은 정보이용자의 의사결정에 유용한 재무상태, 재무성과, 재무상태변동 정보 및 경영진의 수탁책임 결과를 제공하는 것입니다. 사적인 주식 매매 타이밍을 직접 지정·결정해 주는 것은 재무제표의 목적으로 고안된 것이 아닙니다.\n\n[오답 해설]\n①, ②, ③, ④는 기준서에 규정된 재무제표의 정당한 목적에 해당합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재무상태 정보 제공은 재무제표의 정당한 목적입니다.", "articles": [], "principle": "재무제표의 목적", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재무성과 정보 제공은 재무제표의 정당한 목적입니다.", "articles": [], "principle": "재무제표의 목적", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재무상태변동 정보 제공은 재무제표의 정당한 목적입니다.", "articles": [], "principle": "재무제표의 목적", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진의 수탁책임 보고는 재무제표의 정당한 목적입니다.", "articles": [], "principle": "재무제표의 목적", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "개인 투자자의 주관적 매매 시점을 알려주는 기능은 재무제표의 공식 회계적 목적에 해당하지 않습니다.", "articles": [], "principle": "재무제표의 목적", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "K-IFRS 상 전체 재무제표(Complete set of financial statements)를 구성하는 필수 요소로 가장 올바르지 않은 것은?",
        "options": [
            "① 기말 재무상태표",
            "② 기간 포괄손익계산서",
            "③ 기간 자본변동표 및 기간 현금흐름표",
            "④ 주석(유의적인 회계정책 및 그 밖의 설명으로 구성)",
            "⑤ 기업의 핵심 마케팅 전략을 도식화한 브로셔 및 광고 팸플릿"
        ],
        "answer": "5",
        "explanation": "⑤ 전체 재무제표에는 재무상태표, 포괄손익계산서, 자본변동표, 현금흐름표, 주석 및 비교정보 등이 포함됩니다. 기업의 마케팅 광고 팸플릿은 재무제표의 법적 구성 요소가 아닙니다.\n\n[오답 해설]\n①, ②, ③, ④는 K-IFRS 제1001호에서 정의하는 전체 재무제표의 필수 구성 항목입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기말 재무상태표는 전체 재무제표의 필수 요소입니다.", "articles": [], "principle": "전체 재무제표의 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기간 포괄손익계산서는 전체 재무제표의 필수 요소입니다.", "articles": [], "principle": "전체 재무제표의 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본변동표와 현금흐름표는 전체 재무제표의 필수 요소입니다.", "articles": [], "principle": "전체 재무제표의 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석은 전체 재무제표를 구성하는 필수적 요소입니다.", "articles": [], "principle": "전체 재무제표의 범위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "마케팅 광고물이나 브로셔 등은 한국채택국제회계기준의 적용 범위 및 재무제표 구성에 포함되지 않습니다.", "articles": [], "principle": "전체 재무제표의 범위", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "10절 자본과 자본유지개념"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "K-IFRS를 준수하여 재무제표를 작성하는 기업이 준수 사실의 기재(Statement of compliance)를 보고할 때 지켜야 할 기본 규칙은?",
        "options": [
            "① 주석에 그 준수 사실을 명시적이고 제한 없이 기재하여야 한다.",
            "② 세무서장의 특별 승인이 있을 때만 제한적으로 주석에 기록할 수 있다.",
            "③ 재무제표 표지(맨 앞장)에 기재하지 않으면 주석 기재는 아무런 법적 효력이 없다.",
            "④ 기중에 적자가 발생하면 K-IFRS 준수 기재가 법적으로 완전 금지된다.",
            "⑤ 회사의 영어 명칭 뒤에 괄호로만 표시하여야 한다."
        ],
        "answer": "1",
        "explanation": "① 한국채택국제회계기준을 준수하여 재무제표를 작성하는 기업은 그러한 준수 사실을 주석에 명시적이고 제한 없이 기재하여야 합니다.\n\n[오답 해설]\n② 세무서장의 승인 대상이 아닙니다.\n③ 주석에 기재하는 것이 원칙이며, 표지 한정 규정은 없습니다.\n④ 적자 발생 여부와 기준 준수 기재 여부는 무관합니다.\n⑤ 특정한 영어 명칭 연동 제한은 존재하지 않습니다."
        ,
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "한국채택국제회계기준의 준수 사실을 주석에 제한 없이 공표 기재하도록 규정되어 있습니다.", "articles": [], "principle": "K-IFRS 준수 기재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 행정 감독관의 승인이 필요한 요건이 아닙니다.", "articles": [], "principle": "K-IFRS 준수 기재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석 공시 자체로 완벽한 기준 준수 공시 효력을 가집니다.", "articles": [], "principle": "K-IFRS 준수 기재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영 실적(적자 등)과 준수 공시는 무관합니다.", "articles": [], "principle": "K-IFRS 준수 기재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영어 표기 관련 형식 규정은 없습니다.", "articles": [], "principle": "K-IFRS 준수 기재", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "부적절한 회계정책을 채택하여 적용한 기업이, 이에 대하여 주석으로 그 부적절한 사유와 산출 근거를 상세히 설명했을 때의 회계학적 효력은?",
        "options": [
            "① 상세한 고백이 있었으므로 정당한 회계정책으로 법적 인정된다.",
            "② 해당 부적절한 정책은 공시나 주석 또는 보충 자료를 통해 설명하더라도 정당화될 수 없다.",
            "③ 해당 오류에 상응하는 법인세를 환급받을 권리가 생긴다.",
            "④ 회사의 대표이사가 면책 특권을 부여받는다.",
            "⑤ 회계감사 시 무조건 '적정 의견'을 주도록 감리 지침이 규정하고 있다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 상 부적절한 회계정책은 주석이나 보충설명을 제공하더라도 결코 정당화될 수 없으며 여전히 회계 기준 위반에 해당합니다.\n\n[오답 해설]\n① 주석 고백으로 잘못된 회계처리가 적법화되지 않습니다.\n③, ④, ⑤는 회계 원칙 및 관계 법령에 위배되는 잘못된 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "주석 설명으로 회계처리 오류가 정당화되거나 무마될 수 없습니다.", "articles": [], "principle": "부적절한 회계정책의 효과", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기준서 조문에 명시된 바에 따라, 주석 설명이나 보충 공시를 하더라도 부적절한 회계정책은 정당화되지 않습니다.", "articles": [], "principle": "부적절한 회계정책의 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 세액 환급과는 전혀 관련이 없습니다.", "articles": [], "principle": "부적절한 회계정책의 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진의 법적 면책 사유가 되지 않습니다.", "articles": [], "principle": "부적절한 회계정책의 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "오히려 한정이나 의견거절 등의 감사 의견을 받게 됩니다.", "articles": [], "principle": "부적절한 회계정책의 효과", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "경영진이 재무제표를 작성할 때 계속기업으로서의 존속가능성을 평가해야 하는데, 이때 평가에 고려해야 하는 향후 최소 기간 요건은?",
        "options": [
            "① 보고기간 말로부터 향후 적어도 6개월",
            "② 보고기간 말로부터 향후 적어도 12개월",
            "③ 보고기간 말로부터 향후 적어도 3년",
            "④ 보고기간 말로부터 향후 적어도 5년",
            "⑤ 회사의 잔여 설립등기 기간"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 상 계속기업의 가정이 적절한지 평가할 때 경영진은 적어도 보고기간 말로부터 향후 12개월 기간에 대하여 이용가능한 모든 정보를 고려하여야 합니다.\n\n[오답 해설]\n① 6개월은 기준서 요건보다 짧은 기간입니다.\n③, ④, ⑤는 공식적인 기준서 상 최소 평가 요구 기간이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "최소 12개월 이상을 평가해야 하므로 6개월은 오답입니다.", "articles": [], "principle": "계속기업 평가 기간", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "경영진은 보고기간 종료일로부터 적어도 12개월 이상에 대해 계속기업 존속 가능성을 검토해야 합니다.", "articles": [], "principle": "계속기업 평가 기간", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "3년은 최소 준수 기간 조건과 다릅니다.", "articles": [], "principle": "계속기업 평가 기간", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "5년은 최소 준수 기간 조건보다 길게 설정된 오답입니다.", "articles": [], "principle": "계속기업 평가 기간", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법적 등기 잔여 기간과 무관합니다.", "articles": [], "principle": "계속기업 평가 기간", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "경영진이 기업을 청산하거나 경영활동을 중단할 의도를 가지고 있거나, 청산 이외의 대안이 없어 계속기업 가정이 부적절하여 다른 기준(청산기준 등)으로 작성했을 때 반드시 공시해야 하는 사항이 아닌 것은?",
        "options": [
            "① 재무제표가 계속기업의 기준 하에 작성되지 않았다는 사실",
            "② 재무제표가 작성된 세부 기준",
            "③ 그 기업을 계속기업으로 보지 않는 세부 이유",
            "④ 경영진 개개인의 개인 재산 명세서 목록 전체",
            "⑤ 계속기업 가정 평가에 유의적 의문이 제기되는 근거"
        ],
        "answer": "4",
        "explanation": "④ 계속기업 가정이 부적절하여 이를 배제하고 재무제표를 작성했을 때는 그 사실, 작성 기준, 계속기업으로 보지 않는 이유를 공시해야 합니다. 그러나 경영진 개인의 사유재산 명세를 재무제표에 공시해야 할 의무는 없습니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 계속기업 가정 불만족 시 공시가 강제되는 중요 사실들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "계속기업 배제 작성 사실은 필수 공시 사항입니다.", "articles": [], "principle": "계속기업 배제 시 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적용된 대안적 세부 기준(청산원가 등)은 필수 공시 사항입니다.", "articles": [], "principle": "계속기업 배제 시 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계속기업으로 보지 않는 사유와 원인은 필수 공시 사항입니다.", "articles": [], "principle": "계속기업 배제 시 공시", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "임원의 사적 자산 정보 공시는 계속기업 가정 공시 요건이 아니므로 4가 답입니다.", "articles": [], "principle": "계속기업 배제 시 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "불확실성에 대한 증거 제시는 공시 요건에 부합합니다.", "articles": [], "principle": "계속기업 배제 시 공시", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "K-IFRS 상 기업이 재무제표를 작성할 때, 유일하게 발생기준(Accrual Basis) 회계를 적용하지 않고 현금 기준 정보를 수록하는 재무보고서는 무엇인가?",
        "options": [
            "① 재무상태표(Statement of Financial Position)",
            "② 포괄손익계산서(Statement of Comprehensive Income)",
            "③ 자본변동표(Statement of Changes in Equity)",
            "④ 현금흐름표(Statement of Cash Flows)",
            "⑤ 주석(Notes)"
        ],
        "answer": "4",
        "explanation": "④ K-IFRS 상 기업은 현금흐름 정보를 제외하고는 발생기준 회계를 사용하여 재무제표를 작성합니다. 따라서 현금흐름표는 발생기준이 아닌 실제 현금 유출입 기준(현금기준)으로 작성합니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 발생기준에 따라 정보를 포착하고 보고하는 표 및 설명 정보들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재무상태표는 발생기준 회계에 따라 작성됩니다.", "articles": [], "principle": "발생기준 적용 제외", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손익 및 성과표는 발생주의 회계의 핵심 보고서입니다.", "articles": [], "principle": "발생기준 적용 제외", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본변동표도 발생주의 자본 변동액을 기초로 작성됩니다.", "articles": [], "principle": "발생기준 적용 제외", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "현금흐름표는 오직 현금의 직접적 유출입 정보만을 기록하므로 발생주의가 배제되는 유일한 표입니다.", "articles": [], "principle": "발생기준 적용 제외", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석 설명도 발생주의 기반으로 집계된 수치를 해설합니다.", "articles": [], "principle": "발생기준 적용 제외", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "K-IFRS 상 재무제표 표시 원칙 중 '중요성과 통합표시(Materiality and aggregation)'의 기본 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 유사한 항목은 중요성 분류에 따라 재무제표에 구분하여 표시한다.",
            "② 상이한 성격이나 기능을 가진 항목은 구분하여 표시한다.",
            "③ 중요하지 않은 항목은 성격이나 기능이 유사한 항목과 통합하여 표시할 수 있다.",
            "④ 한국채택국제회계기준의 요구에 따라 공시되는 정보라도 중요하지 않다면 그 공시를 제공할 필요는 없다.",
            "⑤ 회사의 기밀에 속하는 중요 항목은 주석에서조차 완전히 누락하여 적지 않는 것이 허용된다."
        ],
        "answer": "5",
        "explanation": "⑤ 중요성에 따른 통합 및 구분 기재는 회계정보의 목적적합성을 높이기 위함입니다. 중요도가 큰 중요 항목을 기밀유지를 핑계로 주석에서 고의 누락하는 회계처리는 허용되지 않는 왜곡 및 정보 은폐 행위입니다.\n\n[오답 해설]\n①, ②, ③, ④는 기준서에 규정된 중요성과 통합표시의 올바른 정형 규칙입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "중요성에 따른 구분 표시는 정당한 원칙입니다.", "articles": [], "principle": "중요성과 통합표시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "서로 다른 성격의 항목 구분 기재는 참입니다.", "articles": [], "principle": "중요성과 통합표시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중요도가 떨어지는 세부항목의 통합 제시는 정당합니다.", "articles": [], "principle": "중요성과 통합표시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "IFRS 요구사항도 중요하지 않으면 공시 생략이 가능하다는 규정은 참입니다.", "articles": [], "principle": "중요성과 통합표시", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "중요한 정보는 정보이용자의 의사결정에 영향을 미치므로 기밀 명목 하의 주석 누락은 절대 불허되어 5가 정답입니다.", "articles": [], "principle": "중요성과 통합표시", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "K-IFRS 상 재무제표의 '상계(Offsetting) 표시'에 관한 기본 원칙으로 가장 올바른 것은?",
        "options": [
            "① 정보의 간결성을 유도하기 위해 매 기말 자산과 부채는 무조건 상상 순액 표시를 원칙으로 한다.",
            "② 한국채택국제회계기준에서 요구하거나 허용하지 않는 한 자산과 부채 그리고 수익과 비용은 상계하지 아니한다.",
            "③ 매출채권과 매입채무는 소송이 진행 중인 경우에만 예외적으로 언제나 상계하여 보고한다.",
            "④ 포괄손익계산서의 비용 항목은 매출액의 10% 범위 하에서 언제나 상계 차감할 수 있다.",
            "⑤ 회사의 대표이사가 개인적으로 승인한 자산/부채는 일괄 상계 표시를 강제 적용한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 상 상계 표시가 거래 실질을 반영하는 특수한 예외 사례를 제외하고는, 자산과 부채 및 수익과 비용의 상계는 이용자의 미래현금흐름 분석을 저해하므로 기준서에서 허용·요구하는 경우 외에는 상계 표시를 전면 금지합니다.\n\n[오답 해설]\n① 상계 금지가 대원칙입니다.\n③, ④, ⑤는 회계 기준 상 전혀 허용되지 않는 가공 설명들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상계 금지가 대원칙이므로 무조건 순액 표시 주장은 틀렸습니다.", "articles": [], "principle": "상계 표시의 원칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기준서 규정 상 명백한 예외 조항이 명시되거나 허용되지 않는 한 상계 표시는 불허됩니다.", "articles": [], "principle": "상계 표시의 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소송 진행 여부와 채권/채무 상계의 당연 허용은 무관합니다.", "articles": [], "principle": "상계 표시의 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출액의 특정 비율 차감 상계 등은 존재하지 않는 규정입니다.", "articles": [], "principle": "상계 표시의 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사적 결재로 회계 기준을 무력화할 수 없습니다.", "articles": [], "principle": "상계 표시의 원칙", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "K-IFRS 상 재무제표의 '표시의 계속성(Consistency of presentation)' 원칙의 기본 의미는 무엇인가?",
        "options": [
            "① 재무제표 항목의 표시와 분류는 매기 동일하여야 한다.",
            "② 매기마다 새로운 회계 표시 방법을 개발하여 즉시 교체 적용해야 한다는 규칙",
            "③ 경쟁 회사들의 표시 방법이 바뀌면 즉시 당사 표시를 무조건 변경해야 함을 의미",
            "④ 재무제표 폰트와 인쇄 규격을 10년마다 한 번씩만 변경해야 한다는 규정",
            "⑤ 회사의 담당 회계사가 바뀌면 표시 방법을 무조건 처음부터 다시 세워 보고하는 규칙"
        ],
        "answer": "1",
        "explanation": "① 표시의 계속성이란 기간 간 비교가능성을 높이기 위해 재무제표 항목의 표시와 분류는 예외 사유(사업 내용의 중대한 변화 등)가 없는 한 매기 동일하게 유지하여야 함을 의미합니다.\n\n[오답 해설]\n②, ③, ⑤는 계속성 원칙과 상반되며,\n④는 폰트 등의 장부 계속성 정의와 관련이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "표시의 계속성이란 재무제표 항목의 표시 및 분류를 기간별로 유지하여 비교가능성을 증진하는 원칙입니다.", "articles": [], "principle": "표시의 계속성 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매기 변경하는 행위는 계속성 원칙을 전면 위배합니다.", "articles": [], "principle": "표시의 계속성 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경쟁사 연동 임의 변경은 불허됩니다.", "articles": [], "principle": "표시의 계속성 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "서식 양식의 인쇄 폰트 고정 규칙이 아닙니다.", "articles": [], "principle": "표시의 계속성 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "담당자 변경에 따른 임의 재구축은 계속성 훼손 행위입니다.", "articles": [], "principle": "표시의 계속성 원칙", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },

    # =========================================================================
    # L2: 이해 (15문항, 511~525번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s01-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "다음 중 K-IFRS의 적용 범위(Scope)와 재무보고서의 성격에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 기업이 주요 재무제표이용자를 위해 발행하는 환경보고서나 부가가치보고서도 K-IFRS의 필수 강제 적용 대상이다.",
            "② 재무제표 이외의 보고서(예: 환경보고서 등)는 한국채택국제회계기준의 적용범위에 해당하지 않는다.",
            "③ 회사의 사내 주간 소식지도 공정한 표시를 위해 K-IFRS 규정에 맞춰 감사받아야 한다.",
            "④ 세무 조정을 위한 법인세 과세 표준 신고서 자체가 K-IFRS 제1001호에 따라 전면 공시되어야 한다.",
            "⑤ 회사가 제공하는 모든 외부 배포 보도자료는 K-IFRS 전체 재무제표 구성에 포함된다."
        ],
        "answer": "2",
        "explanation": "② 많은 기업들이 환경보고서나 부가가치보고서 등 재무제표 이외의 추가 보고서를 제공하지만, 이러한 비재무보고서들은 한국채택국제회계기준의 적용 범위에 해당하지 않습니다.\n\n[오답 해설]\n① 환경/부가가치보고서는 K-IFRS 적용 대상이 아닙니다.\n③ 소식지나 ⑤ 보도자료 등은 적용 대상이 아닙니다.\n④ 세무 신고서는 세법 관할로, 재무제표 표시기준인 K-IFRS 1001호 적용 범위를 벗어납니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "환경보고서 등은 기준서의 적용 제외 대상입니다.", "articles": [], "principle": "기준서의 적용 범위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재무제표를 구성하지 않는 기타 부가 보고서는 IFRS 적용 범주가 아닙니다.", "articles": [], "principle": "기준서의 적용 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사내 소식지 등은 회계 감사 대상이 아닙니다.", "articles": [], "principle": "기준서의 적용 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 세무보고 서식은 회계 표시 기준서 범주가 아닙니다.", "articles": [], "principle": "기준서의 적용 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보도자료는 재무제표 구성 항목이 아닙니다.", "articles": [], "principle": "기준서의 적용 범위", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "K-IFRS 상 재무제표가 기업의 재무상태, 재무성과 및 현금흐름을 '공정하게 표시(Fair presentation)'하기 위해 기본적으로 요구하는 총족 조건으로 가장 적합한 것은?",
        "options": [
            "① 거래의 법적 형식과 소유 관계가 장부상에 100% 일치하도록 기입하여 실질을 완전 배제하는 것",
            "② 개념체계에서 정한 자산, 부채, 수익 및 비용에 대한 정의와 인식요건에 따라 거래, 사건, 상황의 효과를 충실하게 표현하는 것",
            "③ 국세청 법인세 고지 금액에 맞추어 기말 현금 잔액을 강제로 가감 조정하는 것",
            "④ 미래에 발생할 가상의 행운 거래를 임의의 자산 가액으로 가산하여 공시하는 것",
            "⑤ 회사의 부채 비율을 매년 100% 이하로 임의 고정하여 기재하는 것"
        ],
        "answer": "2",
        "explanation": "② 재무제표의 공정한 표시를 달성하기 위해서는 '개념체계'에서 정한 자산, 부채, 수익, 비용에 대한 정의와 인식 요건에 부합하도록 거래, 그 밖의 사건 및 상황의 효과를 충실하게 표현하여야 합니다.\n\n[오답 해설]\n① 법적 형식뿐만 아니라 거래의 경제적 실질을 충실히 표현하여야 합니다.\n③, ④, ⑤는 회계 왜곡 및 부정 기장 사항들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "회계는 법적 형식보다 실질의 충실한 표현을 우선시하므로 틀렸습니다.", "articles": [], "principle": "공정 표시의 의의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "개념체계 상 요소의 정의와 인식요건에 의거해 거래 실질을 충실히 반영할 때 공정한 표시가 달성됩니다.", "articles": [], "principle": "공정 표시의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세액 맞춤식 가감 분개는 부적절합니다.", "articles": [], "principle": "공정 표시의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 가상 거래의 임의 표시는 왜곡입니다.", "articles": [], "principle": "공정 표시의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채비율 강제 고정은 분식 회계입니다.", "articles": [], "principle": "공정 표시의 의의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "K-IFRS를 전면 적용하여 작성된 재무제표(필요에 따라 추가 공시한 경우 포함)의 공정표시 달성 여부에 대한 K-IFRS 기준서의 기본 입장(의제 규정)은 무엇인가?",
        "options": [
            "① K-IFRS를 모두 충족하였더라도 공정하게 표시된 재무제표로 결코 볼 수 없다.",
            "② 한국채택국제회계기준에 따라 작성된 재무제표는 공정하게 표시된 재무제표로 본다(의제한다).",
            "③ 기말에 감사인의 물리적 자필 서명이 첨부된 경우에만 공정표시로 본다.",
            "④ 정부 기획재정부 장관의 공식 인증 도장을 획득해야만 공정표시로 의제한다.",
            "⑤ 적자를 낸 기업은 무조건 공정하지 못한 재무제표로 자동 분류된다."
        ],
        "answer": "2",
        "explanation": "② 한국채택국제회계기준을 준수하여 작성된 재무제표(필요에 따라 추가 공시를 한 경우 포함)는 공정하게 표시된 재무제표로 의제(본다)합니다.\n\n[오답 해설]\n① 준수한 재무제표는 공정표시로 봅니다.\n③, ④는 행정적/절차적 가공 요건입니다.\n⑤ 적자 여부는 공정표시 의제와 관련이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기준 준수 시 공정표시가 달성된 것으로 의제합니다.", "articles": [], "principle": "공정표시의 의제 규정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "K-IFRS를 충실히 준수하여 작성한 재무제표는 공정표시 요건을 갖춘 것으로 본다고 규정되어 있습니다.", "articles": [], "principle": "공정표시의 의제 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사인 자필 서명이 공정표시 판정의 회계 기준 상 직접 규정은 아닙니다.", "articles": [], "principle": "공정표시의 의제 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "장관 인증 절차 등은 기준서에 존재하지 않습니다.", "articles": [], "principle": "공정표시의 의제 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실적 손실 여부는 공정 기장의 판별 척도가 아닙니다.", "articles": [], "principle": "공정표시의 의제 규정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "다음 중 K-IFRS 상 계속기업(Going Concern) 가정 평가 시, 경영진이 의무적으로 고려해야 하는 미래 평가 정보의 범위 및 대상 설명으로 가장 올바른 것은?",
        "options": [
            "① 경영진이 미래 존속 여부를 평가할 때는 보고기간 말로부터 단 하루 뒤의 금융시장 자금 이체 상태만 보면 충분하다.",
            "② 계속기업의 존속능력을 평가할 때, 경영진은 적어도 보고기간 말로부터 향후 12개월 기간에 대하여 이용가능한 모든 정보를 고려하여야 한다.",
            "③ 주주들의 재무상황이나 신용보증 상태는 어떠한 경우에도 계속기업 평가의 고려 대상에 넣어서는 안 된다.",
            "④ 물가상승률이 5% 미만인 국가에서는 계속기업 가정을 무조건 면제하는 특별 예외가 있다.",
            "⑤ 회사의 파산 확률이 99%인 경우에도 계속기업 평가를 아예 생략하고 무조건 정상 기장하는 것이 강제된다."
        ],
        "answer": "2",
        "explanation": "② 계속기업 가정을 평가할 때는 적어도 보고기간 종료일(말)로부터 향후 12개월 기간 동안 이용가능한 모든 정보(영업 현황, 미래 자금 조달 조건 등)를 종합 검토하여야 합니다.\n\n[오답 해설]\n① 12개월 미만 기간의 단기 평가로는 부족합니다.\n③ 주주들의 자금 지원 약정 등 이용 가능한 모든 정보가 고려 대상입니다.\n④, ⑤는 계속기업 가정과 무관한 잘못된 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "단기 하루 단위 평가로는 규정된 존속성 검토에 부합하지 않습니다.", "articles": [], "principle": "계속기업 정보 고려 범위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기간종료일 기준 향후 최소 12개월 이상 기간에 걸친 가용 정보를 총동원하여 계속기업 타당성을 검토해야 합니다.", "articles": [], "principle": "계속기업 정보 고려 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "존속 의문에 영향을 주는 주주 보증 등도 중요한 고려 대상이 됩니다.", "articles": [], "principle": "계속기업 정보 고려 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인플레이션 수치 연동형 가정 면제 조항은 없습니다.", "articles": [], "principle": "계속기업 정보 고려 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "파산 확실 시에는 계속기업 가정을 배제하고 청산기준 등으로 기록해야 합니다.", "articles": [], "principle": "계속기업 정보 고려 범위", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "다음 중 K-IFRS 상 발생기준 회계(Accrual Basis of Accounting) 하에서 자산, 부채, 자본, 수익 및 비용의 인식에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 거래가 발생하여 실제 현금이 금고로 유입되거나 유출된 일자에만 장부에 기록하는 것이다.",
            "② 현금의 수수와 무관하게, 개념체계 상 각 요소의 정의와 인식요건을 충족하는 기간에 사건의 효과를 반영하여 장부에 포착하는 것이다.",
            "③ 정부 세금 납부가 확정되어 통지서가 도달한 해의 1월 1일 자로 일괄 소급 기입하는 방식이다.",
            "④ 모든 회계 요소는 발생일로부터 5년이 경과해야만 자산으로 인식될 자격이 생긴다.",
            "⑤ 회사의 이익이 목표액에 도달한 달의 마지막 날짜로 수익을 전부 이월 기장하는 기술이다."
        ],
        "answer": "2",
        "explanation": "② 발생기준 회계는 실제 현금의 수취·지급 시점과 무관하게, 개념체계가 정한 요소별 정의와 인식 요건을 충족하는 사건이 발생했을 때 해당 기간의 재무제표에 인식하는 회계 방식입니다.\n\n[오답 해설]\n① 은 현금기준(Cash Basis) 회계에 대한 설명입니다.\n③, ④, ⑤는 발생주의 회계 원칙과 전혀 다른 임의적이고 왜곡된 가공 내용입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "현금의 유입출 시점 기장은 현금주의 설명입니다.", "articles": [], "principle": "발생기준 회계의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "현금 흐름의 발생과 상관없이 개념체계 요소 충족 시점에 자산/부채 및 수익/비용을 포착하여 보고합니다.", "articles": [], "principle": "발생기준 회계의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세금 통지 연동 강제 소급 기장은 부적절합니다.", "articles": [], "principle": "발생기준 회계의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "5년 대기 기간 등은 회계 기준에 없습니다.", "articles": [], "principle": "발생기준 회계의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "목표액 달성 연동 인위적 이월은 분식 회계입니다.", "articles": [], "principle": "발생기준 회계의 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "다음 중 K-IFRS 상 재고자산에 대한 재고자산평가충당금이나 매출채권에 대한 대손충당금과 같은 '평가충당금'을 차감하여 관련 자산을 순액으로 측정하는 회계처리에 대한 분석으로 가장 올바른 것은?",
        "options": [
            "① 자산과 부채를 허가 없이 상계한 것이므로 중대한 회계 기준 위반이다.",
            "② 이는 관련 자산의 감액 평가를 자산 내에서 조정한 것일 뿐이며, 기준서 상 상계(Offsetting) 표시에 해당하지 아니한다.",
            "③ 대손충당금 차감은 대주주에 대한 현금 대출 거래와 성격이 완전 동일하다.",
            "④ 정부 세금 공제를 받기 위해 부채 항목을 자산으로 위장한 것이다.",
            "⑤ 평가충당금 차감 시 회사의 영업이익이 복리로 무조건 10%씩 매년 상승한다."
        ],
        "answer": "2",
        "explanation": "② 평가충당금(재고자산평가충당금, 대손충당금 등)을 차감하여 자산의 장부금액을 순액으로 표시하는 것은 자산의 실질 회수가능가치를 측정하기 위한 평가 과정일 뿐이므로, 기준서가 금지하는 상계 표시(자산과 부채를 대등 상쇄하여 생략하는 것)에 해당하지 않습니다.\n\n[오답 해설]\n① 상계가 아니므로 회계 위반이 아닙니다.\n③, ④, ⑤는 충당금 평가 조정의 성격과 무관한 잘못된 내용입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "평가충당금 차감 표시는 정당한 방법이며 회계 위반이 아닙니다.", "articles": [], "principle": "상계와 평가충당금 차감의 구분", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기준서 조문에 명시된 바에 따라, 충당금 차감을 통한 순액 표시는 자산의 속성 조율로 상계에 속하지 않습니다.", "articles": [], "principle": "상계와 평가충당금 차감의 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대주주 자금 대출 등 사외 자본 거래와 상관없습니다.", "articles": [], "principle": "상계와 평가충당금 차감의 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채를 자산으로 유도하는 탈세 분개가 아닙니다.", "articles": [], "principle": "상계와 평가충당금 차감의 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업이익의 복리 상승 효과 설명은 소설입니다.", "articles": [], "principle": "상계와 평가충당금 차감의 구분", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "동일한 종류의 외환거래 집합에서 발생한 외환차익 ₩5,000,000과 외환차손 ₩3,000,000이 있을 때, K-IFRS 상 손익계산서에 이를 외화환산순이익 ₩2,000,000으로 순액 표시하기 위한 중요성 판단 조건은 무엇인가?",
        "options": [
            "① 일반 주주들이 언제나 외화 거래 내역 조회를 거부해야 순액 보고할 수 있다.",
            "② 해당 차익과 차손이 중요(Material)하지 않은 경우에 순액으로 표시하며, 만약 그러한 차익과 차손이 중요한 경우에는 구분하여 표시한다.",
            "③ 외환 거래의 경우 중요도와 무관하게 100% 무조건 총액 구분 표시해야만 한다.",
            "④ 정부 공인 외환 딜러의 자필 보증 도장이 외환 순액 보고의 필수 요건이다.",
            "⑤ 회사의 대표이사가 개인 투자자인 경우에만 순액 처리가 합법화된다."
        ],
        "answer": "2",
        "explanation": "② 외환손익이나 단기매매금융상품 손익과 같이 유사한 거래의 집합에서 발생하는 차익과 차손은 기본적으로 순액으로 표시합니다. 다만, 이러한 차익과 차손이 '중요한 경우'에는 정보를 왜곡하지 않도록 구분하여 총액 방식으로 표시해야 합니다.\n\n[오답 해설]\n① 주주의 거래 조회 거부 조건 등은 회계 규칙에 없습니다.\n③ 무조건 총액 표시만 강제하지 않고, 중요하지 않으면 순액 표시가 허용됩니다.\n④, ⑤는 외환손익 상계 표시에 관한 규정이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "주주의 열람권 배제 연동은 사실무근입니다.", "articles": [], "principle": "유사 거래 차익/차손 상계", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "유사 거래군(외환손익 등)의 차익/차손은 순액 표시가 보편적이나, 금액이 유의적으로 중요하다면 상세 정보 소통을 위해 구분 기재해야 합니다.", "articles": [], "principle": "유사 거래 차익/차손 상계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "외환 거래라고 해서 무조건 총액 기재만 하지는 않습니다.", "articles": [], "principle": "유사 거래 차익/차손 상계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "외부 외환 딜러 도장 증빙은 회계 기준 요건이 아닙니다.", "articles": [], "principle": "유사 거래 차익/차손 상계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대표이사의 주주 신분 연동은 관계가 없습니다.", "articles": [], "principle": "유사 거래 차익/차손 상계", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "다음 중 K-IFRS 상 재무제표의 '보고빈도(Frequency of reporting)'에 관한 규정으로 가장 올바르지 않은 것은?",
        "options": [
            "① 전체 재무제표(비교정보를 포함)는 적어도 1년마다 작성한다.",
            "② 실무적인 이유로 어떤 기업이 52주의 보고기간을 사용하고자 하는 경우, 이 기준서는 이러한 52주 보고관행을 금지하지 않는다.",
            "③ 보고기간종료일을 변경하여 재무제표 보고기간이 1년을 초과하거나 미달하게 되더라도 추가로 이유나 비교가능성 제한 사실을 공시할 필요는 일체 없다.",
            "④ 보고기간이 1년을 초과하거나 미달하게 된 경우 보고기간이 변경된 이유를 공시해야 한다.",
            "⑤ 보고기간이 1년을 초과하거나 미달한 경우 재무제표에 표시된 금액이 완전하게 비교가능하지는 않다는 사실을 공시해야 한다."
        ],
        "answer": "3",
        "explanation": "③ 보고기간종료일을 부득이하게 변경하여 재무제표 보고대상 기간이 1년을 벗어나게 되는 경우, 정보이용자의 혼란을 막기 위해 '그 이유'와 '표시 금액이 완전 비교가능하지는 않다는 사실'을 반드시 추가 공시하도록 기준서는 의무화하고 있습니다.\n\n[오답 해설]\n① 적어도 1년 주기 작성은 강제 원칙입니다.\n② 52주 보고관행(주 단위 결산)은 유연하게 허용됩니다.\n④, ⑤는 보고기간 비정상 변동 시의 정당한 필수 공시 요건들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "1년 주기 재무제표 작성은 의무 조항이 맞습니다.", "articles": [], "principle": "재무제표 보고빈도", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "52주 결산 관행을 불허하지 않고 수용하므로 참입니다.", "articles": [], "principle": "재무제표 보고빈도", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기간 변동 시 오해 방지를 위해 이유와 비교불가성 한계를 명확히 적시 공시해야 하므로 3이 거짓 서술입니다.", "articles": [], "principle": "재무제표 보고빈도", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "변경된 사유 기재 의무는 참입니다.", "articles": [], "principle": "재무제표 보고빈도", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비교 한계 고지 의무는 참입니다.", "articles": [], "principle": "재무제표 보고빈도", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "K-IFRS 상 당기 재무제표에 보고되는 모든 금액에 대한 '전기 비교정보(Comparative information)' 제공 원칙 중 서술형(텍스트) 정보의 비교 처리에 관한 규정으로 옳은 것은?",
        "options": [
            "① 전기 비교정보는 오직 숫자(계정과목 잔액)에만 강제 적용하며, 서술형 정보는 어떠한 경우에도 전기의 내용을 표시해서는 안 된다.",
            "② 당기 재무제표를 이해하는 데 목적적합하다면 서술형 정보의 경우에도 전기 비교정보를 포함한다.",
            "③ 서술형 정보는 전기의 주석을 글자 그대로 복사하여 100% 무조건 동일하게 적어야만 한다.",
            "④ 정부 공청회 승인을 득한 서술형 주석문만 전기 비교 표시가 가능하다.",
            "⑤ 서술형 주석은 매년 무조건 새롭게 작성하여 전기 문장을 완전히 삭제해야 한다."
        ],
        "answer": "2",
        "explanation": "② 비교정보의 원칙은 재무제표 금액뿐만 아니라 서술형 정보(주석 설명 등)에도 미칩니다. 당기 재무제표 정보를 보다 명확히 파악하는 데 유용하다면 전기 서술형 주석 등의 비교 기재가 권장·의무화됩니다.\n\n[오답 해설]\n① 텍스트 정보의 비교 표시 금지 주장은 오답입니다.\n③ 복사기처럼 기계적 복사 작성을 강제하지 않으며, 상황에 맞춰 목적적합하게 기재합니다.\n④, ⑤는 주석 기재 계속성 및 정보 공시 원칙에 위배됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비교정보의 범위는 수치뿐만 아니라 설명문 등 서술 정보도 포괄합니다.", "articles": [], "principle": "서술형 비교정보 제공", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기준서 문단에 입각해, 당기 정보 이해에 도움이 되는 전기 소송 주석이나 정책 설명 등 서술 정보도 비교 표시합니다.", "articles": [], "principle": "서술형 비교정보 제공", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 복사 기입을 강제 규정으로 두지 않습니다.", "articles": [], "principle": "서술형 비교정보 제공", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공청회 승인 절차 등은 기준서에 없습니다.", "articles": [], "principle": "서술형 비교정보 제공", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전기 설명의 완전 지우기 강제 조항은 타당치 않습니다.", "articles": [], "principle": "서술형 비교정보 제공", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "K-IFRS 상 재무제표의 표시나 분류방법을 예외적으로 매기 동일하게 유지하지 않고 '변경'할 수 있는 합법적 사유에 해당하지 않는 것은?",
        "options": [
            "① 사업내용의 유의적인 변화로 다른 표시나 분류방법이 더 적절한 것이 명백한 경우",
            "② 재무제표를 검토한 결과 다른 표시나 분류방법이 더 적절한 것이 명백하여 비교가능성을 해치지 않고 신뢰성 있는 정보 제공이 가능한 경우",
            "③ 한국채택국제회계기준에서 표시방법의 변경을 요구하는 경우",
            "④ 기준서 제1008호 '회계정책, 회계추정치의 변경과 오류'에서 정하는 회계정책의 선택 및 적용 요건에 부합하는 경우",
            "⑤ 회사의 신임 자금담당 과장이 전임자의 기장 양식이 마음에 들지 않아 단순히 개인적 선호도에 맞춰 개편하고자 하는 경우"
        ],
        "answer": "5",
        "explanation": "⑤ 표시의 계속성을 깨고 재무제표 항목의 표시와 분류를 바꿀 수 있는 것은 사업 유의적 변화로 다른 방식의 우월함이 입증(1008호 요건 충족 등)되거나 기준서가 개정 변경을 요구하는 경우로 제한됩니다. 신임 직원 개인의 단순 마음에 들지 않음(사적 선호)을 이유로 한 분류 변경은 불허됩니다.\n\n[오답 해설]\n①, ②, ③, ④는 계속성 예외 적용이 법적으로 인정되는 정당한 사유 조문들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "사업 내용의 유의적 변화 등 명백한 개선 사유 시 변경 가능합니다.", "articles": [], "principle": "표시의 변경 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "신뢰성/목적적합성 제고 시 변경 가능함은 참입니다.", "articles": [], "principle": "표시의 변경 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기준서의 직접적인 개정/변경 요구 시 변경함은 당연합니다.", "articles": [], "principle": "표시의 변경 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계기준서 제1008호의 정책적 선택 요건 충족 시 참입니다.", "articles": [], "principle": "표시의 변경 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "담당 임직원의 자의적 취향이나 기장 변경 선호도는 계속성 예외 사유에 들지 못하므로 5가 정답입니다.", "articles": [], "principle": "표시의 변경 요건", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "회계정책을 적용하는 과정에서 경영진이 내린 다양한 의사결정 중, 재무제표에 인식되는 '금액'에 가장 유의적인 영향을 미쳐 주석에 회계정책과 함께 반드시 공시하도록 요구하는 사항은 무엇인가?",
        "options": [
            "① 경영진이 점심 식사 항목을 복리후생비로 처리했는지 도서인쇄비로 처리했는지에 대한 일일 분류 결정",
            "② 금융자산의 분류 결정(예: 계약상 현금흐름 특성 및 사업모형 평가)이나 특정 임대 부동산을 투자부동산으로 분류할 것인지 여부 등 경영진이 내린 유의적 판단(Judgments)",
            "③ 사무용 복사기 토너 교체 주기를 3개월로 할지 4개월로 할지에 대한 판단",
            "④ 회사 홈페이지 게시판의 답변 등록을 실시간으로 할 것인지 일일 단위로 할 것인지에 대한 결정",
            "⑤ 주주총회 장소 임차 계약금의 송금 은행 지정 판단"
        ],
        "answer": "2",
        "explanation": "② 금액에 유의적 영향을 미친 경영진의 '판단(Judgments)'(예: 리스 계약의 실질 판단, 지분상품의 지배력 행사 여부, 금융자산 사업모형 평가, 투자부동산 분류 등)은 회계정책 주석 설명의 필수 공시 대상입니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 재무제표 금액 인식에 아무런 유의적 영향이 없는 일상적이고 사소한 운영·행정 판단 사항이므로 공시 대상이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "사소한 소액 비용의 임의 분류는 유의적 금액 판단에 해당하지 않습니다.", "articles": [], "principle": "경영진의 유의적 판단 공시", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "금융자산 분류 기준이나 자산의 투자자산 귀속 여부 등 재무제표 구도와 가치 평가에 큰 영향을 주는 핵심 판단은 명확히 주석 기재해야 합니다.", "articles": [], "principle": "경영진의 유의적 판단 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소모품 교환 관리 등 운영 판단은 무관합니다.", "articles": [], "principle": "경영진의 유의적 판단 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인쇄/홍보 활동 관련 판단은 회계정책 판단이 아닙니다.", "articles": [], "principle": "경영진의 유의적 판단 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계좌 이체 수단 결정 등은 회계판단 비대상입니다.", "articles": [], "principle": "경영진의 유의적 판단 공시", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "K-IFRS 상 전체 재무제표가 공시될 때, 각각의 재무제표 항목들이 가지는 표시 상의 중요성(비중)에 관한 규정으로 옳은 것은?",
        "options": [
            "① 재무상태표의 정보가 가장 우월하므로 다른 재무제표보다 2배 이상 크게 표시한다.",
            "② 각각의 재무제표는 전체 재무제표에서 동등한 비중(Equal prominence)으로 표시한다.",
            "③ 주석은 단순 설명문일 뿐이므로 다른 표들에 비해 1/10 크기로 축소 보고해도 무방하다.",
            "④ 현금흐름표는 현금주의이므로 가중치를 가장 낮추어 주석 맨 끝에 별첨으로만 누락 표시한다.",
            "⑤ 자본변동표를 생략하는 대신 포괄손익계산서를 2부 인쇄하여 대체할 수 있다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1001호에 따르면 전체 재무제표를 구성하는 재무상태표, 포괄손익계산서, 자본변동표, 현금흐름표, 주석 등은 모두 재무보고의 동등한 비중을 가지므로 동등한 중요도로 표시 및 공시하여야 합니다.\n\n[오답 해설]\n① 특정 표의 중요도 우위를 전제하지 않습니다.\n③ 주석의 비중 절하 기재는 금지됩니다.\n④ 현금흐름표의 격하 보고나 ⑤ 자본변동표의 임의 대체 생략은 불가능합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재무상태표의 정보 비중 독점 주장은 회계 기준과 다릅니다.", "articles": [], "principle": "재무제표의 표시 비중", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "전체 재무제표의 모든 기본 표와 주석은 정보이용자에게 유기적 정보를 주므로 동등한 비중으로 균형 있게 공시되어야 합니다.", "articles": [], "principle": "재무제표의 표시 비중", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석의 정보 가치를 임의로 깎아내리는 회계처리는 규정 위반입니다.", "articles": [], "principle": "재무제표의 표시 비중", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금흐름표는 독립된 기본 재무제표로 동등 지위를 가집니다.", "articles": [], "principle": "재무제표의 표시 비중", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기본 재무제표 간 대체 표시는 전면 불허됩니다.", "articles": [], "principle": "재무제표의 표시 비중", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "다음 중 K-IFRS 상 재무제표의 항목 간 '상계 표시'가 원칙적으로 금지되는 가장 본질적이고 이론적인 이유는 무엇인가?",
        "options": [
            "① 상계하여 순액으로 표시하면 회사의 차입금 한도가 전산상으로 즉시 소멸하기 때문에",
            "② 자산·부채나 수익·비용을 서로 대등 상쇄하여 숨기면, 거래의 개별 실질 정보가 은폐되어 재무제표이용자가 기업의 실제 미래 현금흐름을 예측하고 상황을 온전히 파악하는 능력을 심각하게 저해하기 때문에",
            "③ 상계 처리를 수행할 경우 세무서에 매번 벌과금 수수료를 현금으로 지급해야 하므로",
            "④ 복식부기 기술상 자산과 부채는 대차가 맞지 않아 상계 자체가 불가능하기 때문에",
            "⑤ 상계하여 보고하면 회사의 주가가 다음 날 무조건 하한가로 내려가기 때문에"
        ],
        "answer": "2",
        "explanation": "② 상계를 하게 되면 자산 규모나 수익 규모가 겉보기에 극도로 축소·왜곡되어, 실제 해당 거래들이 유발할 잠재적 리스크나 회사의 총체적 외형을 정확히 독독할 수 없게 만듭니다. 이는 분석가의 미래현금흐름 추정 유용성을 크게 해칩니다.\n\n[오답 해설]\n① 차입금 한도 연동 전산 차단은 무관합니다.\n③, ⑤는 이론적 본질과 무관한 극단적 설명입니다.\n④ 기술적 상계 조정 분개 자체는 가능하나 기준서가 원칙 금지하는 것입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "차입 한도의 인위적 소멸 규정은 사실이 아닙니다.", "articles": [], "principle": "상계 금지의 이론적 사유", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "상계는 총액 정보(자산 부채의 크기, 수익 비용의 세부 원천)를 지워버려 예측 능력을 상실하게 하므로 금지합니다.", "articles": [], "principle": "상계 금지의 이론적 사유", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 행정 과태료 연동 사항이 아닙니다.", "articles": [], "principle": "상계 금지의 이론적 사유", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대차 평균 상 상계 분개는 기술적으로 가능하므로 오답입니다.", "articles": [], "principle": "상계 금지의 이론적 사유", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주가 연동 설명은 무관한 허구입니다.", "articles": [], "principle": "상계 금지의 이론적 사유", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "다음 중 K-IFRS 제1001호 상 재무제표의 '표시의 계속성' 원칙을 적용할 때, 표시 방법의 변경 타당성을 입증하기 위해 기업이 판단하여 고려해야 하는 요인이 아닌 것은?",
        "options": [
            "① 변경된 표시방법이 재무제표이용자에게 신뢰성 있고 더욱 목적적합한 정보를 제공하는지 여부",
            "② 변경된 구조가 향후 지속적으로 유지될 가능성이 높아 기간 간 비교가능성을 저해하지 않을 것인지 여부",
            "③ 표시방법의 변경이 회계기준 개정 등으로 인한 불가피한 요구사항인지 여부",
            "④ 신임 회계 감사인이 기장의 세부 색상 양식을 본인 선호 양식으로 바꿀 것을 단순 구두 권고했는지 여부",
            "⑤ 변경 과정에서 회계정책의 선택 및 적용 요건(기준서 제1008호)을 정당하게 고려했는지 여부"
        ],
        "answer": "4",
        "explanation": "④ 표시 방법의 변경은 정보의 목적적합성·신뢰성 제고와 구조적 지속성이 담보될 때에만 허용됩니다. 감사인의 세부 서식 디자인에 대한 개인적 구두 선호도는 계속성 원칙을 깰 수 있는 객관적 타당성 근거가 아닙니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 표시 방법 변경 시 계속성 훼손 부작용을 통제하기 위해 의무 검토되는 중요 요건들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "정보의 유용성(신뢰성/목적적합성) 개선 검토는 핵심 요건입니다.", "articles": [], "principle": "계속성 예외 변경 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "변경된 방법의 지속 유지 가능성 검토는 중요합니다.", "articles": [], "principle": "계속성 예외 변경 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "K-IFRS의 변경 요구 사항 여부는 당연 검토 대상입니다.", "articles": [], "principle": "계속성 예외 변경 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "외부 감사인의 사적인 기장 양식 디자인 요구 등은 공식 변경 타당성 조건이 아니므로 4가 답입니다.", "articles": [], "principle": "계속성 예외 변경 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계기준서 제1008호 적용 요건 충족 여부는 검토되어야 합니다.", "articles": [], "principle": "계속성 예외 변경 요건", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "극히 드문 상황으로서 한국채택국제회계기준의 요구사항을 준수하는 것이 오히려 '개념체계'에서 정하고 있는 재무제표의 목적과 상충되어 이용자의 오해를 유발할 때, 관련 감독체계가 이러한 요구사항으로부터의 일탈(Departure)을 허용(의무화하거나 금지하지 않음)하는 경우 기업이 취해야 할 올바른 조치는?",
        "options": [
            "① 기준의 상충 여부와 무관하게 무조건 K-IFRS 요구사항을 100% 맹목적으로 기장하여야 한다.",
            "② 재무제표의 목적과 상충되는 IFRS 요구사항을 달리 적용(일부 미적용)하여 작성하고, 관련 사실과 이탈 적용의 재무적 영향 등을 주석에 상세히 공시한다.",
            "③ 즉시 회사를 해산하고 청산절차를 밟아야 한다.",
            "④ 국세청에 탈세 혐의 자진 신고서를 송부하여야 한다.",
            "⑤ 회계 감사를 받지 않고 재무제표 공시 자체를 무기한 연기한다."
        ],
        "answer": "2",
        "explanation": "② 감독체계가 허용한다면 오해를 방지하기 위해 예외적으로 일탈(이탈) 처리가 허용됩니다. 단, 이 경우 주석에 '경영진이 공정표시를 달성했다고 결론내린 사실', 'K-IFRS의 특정 요구사항을 달리 적용했다는 사실' 및 '각 기간 재무제표에 미치는 재무적 영향' 등을 낱낱이 주석 공시해야 합니다.\n\n[오답 해설]\n① 예외적 일탈 허용 규정이 있으므로 맹목 기장 고수만 답이 아닙니다.\n③, ④, ⑤는 일탈 요건의 정상적 해결책이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "오해를 유발함이 명백하고 감독체계가 허용할 경우 예외적으로 일탈을 인정합니다.", "articles": [], "principle": "IFRS 요구사항 일탈 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "극히 예외적으로 일탈이 정당화될 때 달리 적용하고, 관련 내용과 영향치를 대내외에 공시하도록 되어 있습니다.", "articles": [], "principle": "IFRS 요구사항 일탈 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회사 해산 사유가 아닙니다.", "articles": [], "principle": "IFRS 요구사항 일탈 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "탈세 자진 신고 대상이 아닙니다.", "articles": [], "principle": "IFRS 요구사항 일탈 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공시 연기나 회피 수단이 아닙니다.", "articles": [], "principle": "IFRS 요구사항 일탈 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },

    # =========================================================================
    # L3: 적용 (15문항, 526~540번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s01-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "(주)평가는 당기말 현재 거래처 A에 대해 매출채권 ₩10,000,000을 보유하고 있으며, 동시에 동일한 거래처 A에 대해 매입채무 ₩7,000,000을 부담하고 있다. 두 채권·채무에 대해 법적인 상계 권리가 없고 계약상 상계 합의도 존재하지 않는다. (주)평가가 기말 재무상태표에 매출채권 ₩3,000,000만 순액으로 기재하여 보고하였을 때, 이 회계처리에 대한 평가로 가장 올바른 것은?",
        "options": [
            "① 평가충당금을 반영한 정당한 순액 측정에 해당하므로 K-IFRS에 부합한다.",
            "② 상계금지 원칙을 위반하여 자산과 부채를 무단으로 상계 표시한 회계 기준 위반이다.",
            "③ 소액의 거래이므로 중요성 배제 원칙에 따라 무조건 타당하다.",
            "④ 기말에 현금이 들어온 거래가 아니므로 장부에 기록할 필요가 없다.",
            "⑤ 회사의 부채 비율을 낮추었으므로 재무구조 개선을 달성한 합법적 처리이다."
        ],
        "answer": "2",
        "explanation": "② 동일 거래처라 하더라도 법적 상계 권리나 계약적 순액 결제 합의가 없다면, 매출채권(자산)과 매입채무(부채)를 대등액으로 상쇄하여 재무제표에서 지우는 것은 기준서 상 '상계 금지 원칙'을 정면으로 위반하는 분개 왜곡입니다.\n\n[오답 해설]\n① 평가충당금은 관련 자산의 감액 조정을 뜻하며, 타인 부채를 직접 상쇄하는 것과 다릅니다.\n③ 법적 결합이 없는 채권·채무의 상계는 중요도와 무관하게 원칙 불허됩니다.\n⑤ 부채비율 왜곡 편법일 뿐 정당한 개선이 아닙니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "평가충당금의 성격이 아니라 자산과 부채의 직접적 대등 상쇄이므로 순액 표시가 불허됩니다.", "articles": [], "principle": "사례별 상계 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "법적 권리/합의 없는 매출채권과 매입채무의 순액 기재는 명백한 상계 표시 금지 위반입니다.", "articles": [], "principle": "사례별 상계 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중요성을 핑계로 자산/부채의 인위적 상쇄를 정당화할 수 없습니다.", "articles": [], "principle": "사례별 상계 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "발생주의 하에서 채권/채무 기록은 필수이므로 기장 회피 주장은 틀렸습니다.", "articles": [], "principle": "사례별 상계 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채비율을 낮춘 것은 장부의 외형 왜곡 결과일 뿐입니다.", "articles": [], "principle": "사례별 상계 판정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "(주)평가는 당기 중 기계장치(취득원가 ₩15,000,000, 감가상각누계액 ₩12,000,000)를 중고 시장에 ₩5,000,000의 처분 대금(수수료 없음)을 받고 매각하였다. 포괄손익계산서에 처분금액 ₩5,000,000을 '유형자산처분수익'으로 잡고 장부잔액 ₩3,000,000을 '유형자산처분비용'으로 각각 총액 보고하지 않고, 그 차액인 ₩2,000,000만을 '유형자산처분이익'으로 단일 순액 보고했을 때의 회계 기준 위반 여부 판단은?",
        "options": [
            "① 기계장치의 처분 수익과 비용을 총액 기재하지 않아 상계 금지를 위반한 오류이다.",
            "② 비금융자산의 처분 손익과 같이 동일 거래에서 발생하는 수익과 관련 비용의 차감 표시는 거래 실질을 충실히 반영하므로 K-IFRS 상 상계 위반이 아니며 정당하다.",
            "③ 처분금액의 10배를 추가 공시하지 않았으므로 표시방법 위반이다.",
            "④ 기계장치 처분은 매출에 속하므로 영업수익으로 강제 통합해야 한다.",
            "⑤ 감가상각누계액을 당기 소모품비로 대체 상계하지 않았으므로 위반이다."
        ],
        "answer": "2",
        "explanation": "② 유형자산 등 비유동자산의 처분거래는 기업의 주된 영업활동이 아니므로, 처분대금 전체를 별도 매출(수익)로 잡고 장부가액을 매출원가(비용)로 잡지 않고 차액인 '유형자산처분이익(손실)'만 순액 공시하는 것이 거래 실질을 가장 잘 반영합니다. 이는 기준서가 정당히 허용하는 상계 예외(상계 미해당)입니다.\n\n[오답 해설]\n① 처분 손익의 순액 기재는 정당하므로 위반이 아닙니다.\n③, ④, ⑤는 자산 처분 회계 처리 원칙과 거리가 먼 오답 설명입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "비유동자산 처분 손익의 순액 표시는 상계 금지 위반이 아닙니다.", "articles": [], "principle": "처분손익의 순액 표시 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "동일 자산 처분 거래의 차익/차손은 순액 기재가 실질을 나타내므로 허용됩니다.", "articles": [], "principle": "처분손익의 순액 표시 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "10배 공시 의무 규정은 실재하지 않습니다.", "articles": [], "principle": "처분손익의 순액 표시 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기계 매각액은 경상 매출액으로 분류하지 않는 것이 타당합니다.", "articles": [], "principle": "처분손익의 순액 표시 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각누계액을 소모품비로 보내는 분개는 오류입니다.", "articles": [], "principle": "처분손익의 순액 표시 판정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "(주)평가는 당기 중 보유하고 있는 투자부동산으로부터 임대료 수익 ₩20,000,000을 현금 수취하였고, 동 부동산의 청소비, 엘리베이터 전기료 등 관리비용으로 ₩6,000,000을 현금 지급하였다. 회사가 포괄손익계산서에 임대료 수익 ₩20,000,000과 관리유지비 ₩6,000,000을 각각 구분 기재하지 않고, 순액인 '임대순이익 ₩14,000,000'만 단일 항목으로 보고하였을 때의 평가로 가장 올바른 것은?",
        "options": [
            "① 임대 관리 원가가 차감되었으므로 실무적으로 간편하고 올바른 처리이다.",
            "② 수익과 비용을 기준서 허가 없이 무단 상계한 것으로 K-IFRS 상 상계 금지 원칙 위반이다.",
            "③ 투자부동산 거래는 주주 배당 거래에 해당하므로 자본조정으로 처리해야 한다.",
            "④ 기말 감가상각비를 ₩14,000,000으로 자동 맞춤 계상해야 한다.",
            "⑤ 세무서에 보고할 임대소득세 총액을 ₩0원으로 만들기 위한 적절한 분개이다."
        ],
        "answer": "2",
        "explanation": "② 임대료 수익(수익)과 임대자산 관리유지비(비용)는 각각 독립된 성격의 수익과 비용 거래입니다. 이 둘을 직접 상쇄하여 순액만 적으면, 회사의 실제 임대 규모와 유지비 비중을 확인할 수 없게 되어 정보 예측 가치가 떨어집니다. 이는 명백한 상계 금지 위반입니다.\n\n[오답 해설]\n① 실무적 편의를 이유로 수익·비용 상계가 허용되지 않습니다.\n③ 투자부동산 임대는 영업/투자 성과 거래로 자본 거래가 아닙니다.\n④, ⑤는 회계 이론과 세법에 어긋나는 가공의 오답입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "편의상 상계 기재는 금지됩니다.", "articles": [], "principle": "수익/비용 상계 위반 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "임대 수익과 이에 소요된 경상 비용은 대등 상쇄하지 않고 각각 구분하여 총액 기재하는 것이 원칙이므로 상계 위반입니다.", "articles": [], "principle": "수익/비용 상계 위반 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지분 자본 거래가 아닌 수익/비용 거래입니다.", "articles": [], "principle": "수익/비용 상계 위반 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각비를 인위적 상계 순액에 맞추는 것은 회계 왜곡입니다.", "articles": [], "principle": "수익/비용 상계 위반 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 목적 조작 설명은 타당하지 않습니다.", "articles": [], "principle": "수익/비용 상계 위반 판정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "(주)평가는 정기 주주총회 결의를 통해 기말 보고기간종료일을 매년 12월 31일에서 9월 30일로 변경하였다. 이로 인하여 당기 재무보고 대상 기간이 2026년 1월 1일부터 2026년 9월 30일까지의 9개월이 되었다. (주)평가가 당기 재무제표 공시 시 추가로 공시하여야 하는 필수 주석 사항이 아닌 것은?",
        "options": [
            "① 당기 재무보고 기간이 1년 미만(9개월)이 되게 된 정당한 이유",
            "② 당기 재무제표에 표시된 비교 수치들이 완전하게 비교가능하지는 않다는 사실",
            "③ 전임 대표이사가 사임한 사적 사유의 일기장 공개",
            "④ 당기 재무제표의 대상 주기가 9개월이라는 사실 정보",
            "⑤ 당기 손익계산서 등의 비교 표시된 전기 12개월분 수치와의 차이 안내"
        ],
        "answer": "3",
        "explanation": "③ 보고기간이 1년을 초과하거나 미달하게 되는 경우, 그 이유와 재무제표 수치가 전기와 완전 비교 가능하지 않다는 사실을 추가 공시해야 합니다. 그러나 퇴임한 임원의 사적인 생활 정보(일기장 등)를 재무제표 주석에 기재할 의무나 타당성은 없습니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 보고기간 단축에 따른 정보 왜곡 차단을 위해 기준서가 요구하는 정당한 공시 요건들입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "단축 기간 이유 공시는 기준서가 명문화한 요건입니다.", "articles": [], "principle": "보고기간 변경 시 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "완전 비교 불가능성 사실 고지는 기준서 요구 사항입니다.", "articles": [], "principle": "보고기간 변경 시 공시", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "임직원의 사생활 정보나 일기장 등은 재무제표 주석 공시 대상이 아니므로 3이 오답입니다.", "articles": [], "principle": "보고기간 변경 시 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당기 대상 기간 공시는 기본입니다.", "articles": [], "principle": "보고기간 변경 시 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비교 기간 편차에 대한 서술적 보완 설명은 타당합니다.", "articles": [], "principle": "보고기간 변경 시 공시", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "(주)평가는 당기 중 재무제표 표시 항목의 분류방법을 변경하였다(더 적절한 표시를 위해 유형자산의 일부를 투자부동산으로 재분류함). K-IFRS 상 (주)평가가 전기 비교정보의 표시를 위해 취해야 하는 기본 조치로 가장 올바른 것은?",
        "options": [
            "① 전기의 재무제표 수치는 이미 지나간 과거이므로 절대로 변경하거나 재분류해서는 안 된다.",
            "② 실무적으로 불가능하지 않은 한, 전기 비교정보의 항목도 소급하여 재분류 표시하고 재분류 이유 및 관련 금액을 주석 공시한다.",
            "③ 전기의 비교 자산을 모두 당기에 쓰레기 비용으로 일괄 소각 처리한다.",
            "④ 비교정보를 완전히 삭제하여 당기 단독 재무제표만 공시한다.",
            "⑤ 정부 감정위원회를 소집하여 전기 장부를 다시 인쇄하도록 요청한다."
        ],
        "answer": "2",
        "explanation": "② 재무제표의 표시나 분류를 변경할 때, 기간 간 비교가능성을 유지하기 위해 실무적으로 불가능하지 않은 한 '전기의 비교 수치'도 당기의 새로운 분류 기준에 맞춰 소급 재분류 표시하여야 하며, 관련 재분류 금액과 사유를 공시하여야 합니다.\n\n[오답 해설]\n① 소급 재분류가 대원칙이므로 금지 주장은 오답입니다.\n③ 일괄 비용 소각 등은 회계 오류입니다.\n④ 비교정보 삭제는 K-IFRS 비교표시 의무 위반입니다.\n⑤ 장부 재인쇄 행정 요청 등은 존재하지 않는 실무입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "표시 변경 시 전기 정보의 소급 재분류가 원칙입니다.", "articles": [], "principle": "표시 변경 시 비교정보 재분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비교가능성 조율을 위해 실무적으로 소급 재분류가 불가능한 상황 외에는 전기 비교 수치도 재배치하여 공시합니다.", "articles": [], "principle": "표시 변경 시 비교정보 재분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 임의 소각은 불가합니다.", "articles": [], "principle": "표시 변경 시 비교정보 재분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비교정보 누락은 기준 위반입니다.", "articles": [], "principle": "표시 변경 시 비교정보 재분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재인쇄 요청 행정 업무는 사실무근입니다.", "articles": [], "principle": "표시 변경 시 비교정보 재분류", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "(주)평가의 경영진은 당기 재무제표 작성 시, 회사의 영업 적자가 지속되자 향후 자금 차입 가능 기간을 고려해 기말 시점으로부터 '향후 8개월간'의 정보만을 검토하여 계속기업 가정이 타당하다고 결론 내렸다. 이 계속기업 가정 평가 과정의 적절성 판정은?",
        "options": [
            "① 향후 자금 차입 가능 기간만 보면 충분하므로 매우 적절하다.",
            "② 계속기업 평가 시 검토 기간은 적어도 보고기간 말로부터 '향후 12개월' 이상이어야 하므로, 8개월만 고려한 경영진의 평가는 K-IFRS 위반이며 부적절하다.",
            "③ 적자 기업은 계속기업 평가를 할 수 없으므로 행정 절차상 타당하다.",
            "④ 6개월을 초과하였으므로 법적 분쟁 여지가 없다.",
            "⑤ 회계법인 대표의 개인 승인이 있다면 8개월도 합법화된다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS는 계속기업 타당성 검토를 위한 정보 평가 기간을 적어도 '보고기간종료일로부터 12개월 이상'으로 명시하고 있습니다. 따라서 경영진이 임의로 8개월의 단기 정보만 보고 계속기업 가정이 정당하다고 판단한 것은 회계 기준 위반입니다.\n\n[오답 해설]\n① 12개월 미만 기간은 부적절합니다.\n③ 적자 상태라도 존속가능성 평가를 12개월 기준으로 수행해야 합니다.\n④ 6개월 초과여부는 면책 사유가 아닙니다.\n⑤ 개인 승인으로 회계 기준을 변경할 수 없습니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "12개월 요건에 미달하므로 부적절합니다.", "articles": [], "principle": "계속기업 검토기간의 강제성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기준서 조문에 명시된 향후 12개월 이상 평가 의무를 충족하지 못했으므로 기준 위반입니다.", "articles": [], "principle": "계속기업 검토기간의 강제성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적자 기업이라고 평가를 생략하거나 축소할 수 없습니다.", "articles": [], "principle": "계속기업 검토기간의 강제성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "6개월 단위 한도는 기준서 내용과 상관없습니다.", "articles": [], "principle": "계속기업 검토기간의 강제성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "외부인 사적 승인으로 합법화되지 않습니다.", "articles": [], "principle": "계속기업 검토기간의 강제성", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "다음 중 K-IFRS 상 포괄손익계산서 등에서 자산의 거래나 평가와 관련하여 발생하는 손익 중 '상계 표시'가 거래의 실질을 반영하여 순액 표시하는 것이 정당화되는 올바른 거래 사례는?",
        "options": [
            "① 당기 재고자산 총 매출액에서 생산부 임직원 급여 비용을 직접 차감하여 보고한 거래",
            "② 유형자산처분손실과 유형자산처분이익을 동일 자산의 처분 결과 하에 순액으로 표시한 경우",
            "③ 은행 예금 이자 수익과 차입금 이자 비용을 단일 예대마진 순이익으로 묶어 단기금융손익으로 적은 경우",
            "④ 회사의 마케팅 광고비용을 원재료 매입 대금에서 직접 빼고 순 원재료비만 보고한 거래",
            "⑤ 법인세 비용을 수도광열비에서 차감하여 영업비용을 낮춘 경우"
        ],
        "answer": "2",
        "explanation": "② 유형자산이나 투자유형 자산의 매각 처분 거래 시 발생하는 차익과 차손은 동일 목적의 일회성 처분 거래 실질을 보여주는 척도이므로, 상계 차감한 순액(유형자산처분손익)으로 보고하는 상계 표시가 허용됩니다.\n\n[오답 해설]\n① 매출과 급여의 상계, ③ 예금이자와 차입이자의 상계, ④ 광고비와 원재료비 상계, ⑤ 법인세와 수도광열비 상계는 기업의 경영 위험을 은폐하는 부적절하고 금지된 상계 표시입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "매출과 종업원 급여는 각각 총액 보고해야 합니다.", "articles": [], "principle": "허용되는 상계 거래 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비유동자산 처분에서 생긴 차익/차손의 순액 기재는 기준서가 실질을 반영하는 상계로 인정합니다.", "articles": [], "principle": "허용되는 상계 거래 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자 수익과 비용은 엄연히 성격이 달라 상계 표시할 수 없습니다.", "articles": [], "principle": "허용되는 상계 거래 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "광고비와 원자재비는 서로 다른 기능의 비용으로 상계가 금지됩니다.", "articles": [], "principle": "허용되는 상계 거래 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법인세와 수도비 상계는 불가능한 왜곡 기장입니다.", "articles": [], "principle": "허용되는 상계 거래 판정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "(주)평가는 보유하고 있는 장기 리스자산에 대한 리스이용자의 계약 갱신 가능성을 평가하여, 동 리스를 '금융리스'로 분류하였다. 이로 인해 기말 재무제표에 인식된 자산 및 이자 수익 금액에 지대한 영향이 발생하였다. K-IFRS 상 이 분류 의사결정에 대한 공시 주체는 무엇인가?",
        "options": [
            "① 리스 분류는 단순 추정치 변동이므로 주석 공시를 일체 누락하여 보고한다.",
            "② 회계정책의 적용과정에서 내린 유의적인 영향력의 '경영진의 판단(Judgments)'에 해당하므로, 유의적 회계정책 또는 기타 주석사항과 함께 이를 주석 공시하여야 한다.",
            "③ 정부 국토교통부 리스 등록부의 직권 공시로 대체한다.",
            "④ 리스 이용자가 자기의 인터넷 블로그에 대리 공시해야 한다.",
            "⑤ 회사의 최대 주주가 주주총회 석상에서 개인적으로 구두 발표만 하면 공시가 면제된다."
        ],
        "answer": "2",
        "explanation": "② 리스 계약의 실질이 금융리스인지 운용리스인지 판정하는 분류는 금액에 직접적 영향을 미치는 '경영진의 유의적 판단' 사례입니다. 기준서에 의거해 경영진이 내린 중요 판단 사항은 정책 설명 주석 등에 명시적으로 밝혀 정보이용자에게 소통되어야 합니다.\n\n[오답 해설]\n① 추정치 공시와 구분되는 판단의 공시 대상입니다.\n③, ④, ⑤는 관계 기준이나 법리에 부합하지 않는 오답 설명입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "유의적 판단 공시는 누락 대상이 아닌 필수 대상입니다.", "articles": [], "principle": "판단과 추정의 분류 공시", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산의 분류 성격 판단 등 경영진의 정책적 적용 의사결정은 주석 공시 정보에 반영되어야 합니다.", "articles": [], "principle": "판단과 추정의 분류 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "외부 부서 등록부 대체 처리는 불가능합니다.", "articles": [], "principle": "판단과 추정의 분류 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계약 상대방의 블로그 게시는 적법 공시가 아닙니다.", "articles": [], "principle": "판단과 추정의 분류 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "구두 발표로 주석 공시 의무가 소멸하지 않습니다.", "articles": [], "principle": "판단과 추정의 분류 공시", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "(주)평가는 당기 중 IFRS 기준서가 필수적으로 요구하는 특정 거래처별 리스 약정 만기 목록 세부 공시 규정을 확인하였다. 그러나 조사 결과, 해당 계약 잔액이 회사 총 자산의 0.0001% 미만으로 극히 미미(중요하지 않음)하였다. (주)평가가 해당 세부 주석 기재를 생략하고 공시하지 않았을 때의 적법성 판정은?",
        "options": [
            "① IFRS 요구사항을 단 한 줄이라도 생략하면 무조건 형사 처벌 대상이 되므로 불법이다.",
            "② 한국채택국제회계기준에서 요구하는 공시 정보라도 중요하지 않다면 그 공시를 제공할 필요는 없으므로, (주)평가의 생략 처리는 적법하고 타당하다.",
            "③ 리스 금액은 액수 불문하고 무조건 100% 총액 공시해야 하므로 위반이다.",
            "④ 세무 조정을 통해 즉시 전액 자본금 감액 등기가 수반되어야 적법화된다.",
            "⑤ 회사의 대표이사가 사적으로 리스계약서를 보증한 경우에만 생략이 정당화된다."
        ],
        "answer": "2",
        "explanation": "② 중요성과 통합표시의 세부 규정에 의하면, K-IFRS에서 요구하는 특정 항목의 개별 주석 공시 의무 조항이라 하더라도, 해당 정보가 중요하지 않다면(의사결정에 차이를 유발하지 않는다면) 생략하는 것이 허용되며 정보 유용성을 해치지 않습니다.\n\n[오답 해설]\n① 맹목적인 형사처벌 주장은 사실이 아닙니다.\n③ 리스 역시 중요성 원칙의 통제를 받습니다.\n④ 자본금 감액 등이나 ⑤ 사적 보증 조건 등은 생략 적법 요건이 아닙니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "회계 기장은 중요성 제약을 받아 맹목적 강제 일괄 기재만 고집하지 않습니다.", "articles": [], "principle": "중요성과 공시 생략", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "중요성이 극히 낮은 공시 정보는 재무제표의 불필요한 노이즈를 줄이기 위해 생략이 가능하도록 규정되어 있습니다.", "articles": [], "principle": "중요성과 공시 생략", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "리스 정보도 중요성 원칙의 적용 범위입니다.", "articles": [], "principle": "중요성과 공시 생략", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 조정 및 감자 등기와 연동되는 처리가 아닙니다.", "articles": [], "principle": "중요성과 공시 생략", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사적 보증 여부는 중요성 평가의 직접 척도가 아닙니다.", "articles": [], "principle": "중요성과 공시 생략", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "다음 중 K-IFRS 상 표시의 계속성 원칙에 비추어 볼 때, 사업의 성격이 변하지 않았고 더 명백한 대안이 없음에도 회사가 단순히 '표시 항목 분류'를 당기에 임의로 바꾼 경우, 비교가능성 관점의 평가로 가장 올바른 것은?",
        "options": [
            "① 매년 기장 방법을 바꾸는 것이 창의적인 회계이므로 적극 장하해야 한다.",
            "② 정당한 사유가 없는 표시 분류 변경은 정보이용자의 기간 간 비교가능성을 심각하게 훼손하여 불합리하며 K-IFRS 위반에 해당한다.",
            "③ 대주주 지분율이 50% 이상이면 표시 분류를 매일 바꾸어도 합법이다.",
            "④ 기말 이익이 ₩0원이 되는 결과를 초래하므로 무조건 허용된다.",
            "⑤ 세무서에 수정 신고를 접수만 해두면 계속성 위반 문제가 소멸한다."
        ],
        "answer": "2",
        "explanation": "② 정당한 요건(사업 변화나 기준서 개정)을 충족하지 못한 자의적인 표시 방법의 변경은 전기 재무제표 수치와의 횡적·종적 비교가능성을 차단하여 유용성을 해칩니다. 이는 계속성 원칙 위반입니다.\n\n[오답 해설]\n① 회계에서는 창의적 기장을 빙자한 자의적 분류 변경을 금지합니다.\n③ 지분율 크기와 계속성 준수 의무 면제는 무관합니다.\n④, ⑤는 계속성 위반을 치유할 수 있는 적법한 사유가 아닙니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "자의적인 수시 기장 변경은 비교성을 깨뜨리므로 장려 대상이 아닙니다.", "articles": [], "principle": "계속성 위반 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "표시 방법 변경은 유용성 개선이 입증될 때에만 제한 허용하므로, 단순한 자의적 변경은 회계 기준 위반입니다.", "articles": [], "principle": "계속성 위반 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지주 지분율 연동 면책권은 없습니다.", "articles": [], "principle": "계속성 위반 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익의 크기와 계속성 위반 여부는 별개입니다.", "articles": [], "principle": "계속성 위반 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수정 세무 신고가 재무제표 표시 계속성 기준을 적법화하지 못합니다.", "articles": [], "principle": "계속성 위반 판단", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "(주)평가는 당기 중 매출액을 크게 보이게 유도하고자 거래처 B사와의 거래에서 발생한 원재료 매입비용 ₩30,000,000을 상품 매출액 ₩80,000,000에서 대차대조표(손익계산서) 상 직접 차감하여 '매출액 ₩50,000,000, 원재료비 ₩0'으로 표시하였다. 이 회계처리의 오류 분석으로 가장 올바른 것은?",
        "options": [
            "① 원재료비가 0원으로 표시되어 제조 원가 구조가 건실해 보이므로 타당하다.",
            "② 수익(매출)과 비용(원재료비)은 각각 대등액이 아니며, 상계 시 원천적인 매출 거래 규모 정보가 소멸하므로 상계 금지 원칙 위반이다.",
            "③ 주식 할인발행차금과 성격이 동일하므로 자본조정 차감 처리가 맞다.",
            "④ 기말 감가상각 금액을 자동으로 ₩30,000,000 늘린 것과 같다.",
            "⑤ 회사의 세무 신고 시 법인세가 절감되므로 타당하다."
        ],
        "answer": "2",
        "explanation": "② 매출액(수익)과 매입비용(비용)의 임의 상쇄는 손익계산서의 총액 표시 원칙 및 상계 금지 조항을 정면으로 어기는 오류입니다. 이를 감행하면 회사의 실제 경영 규모인 ₩80,000,000의 매출 외형 정보가 ₩50,000,000으로 왜곡 소실됩니다.\n\n[오답 해설]\n① 원가 구조 왜곡 기장일 뿐 건실함이 아닙니다.\n③ 자본 거래인 주식 할인 발행과 관련이 없습니다.\n④ 감가상각비 가산과 매출-비용 상계는 무관합니다.\n⑤ 조세 절감 수단으로의 위법 기장은 정당화 사유가 아닙니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "장부를 왜곡 조작한 불법 기장이므로 타당치 않습니다.", "articles": [], "principle": "수익/비용의 상계 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수익과 비용은 총액 보고가 의무이므로, 임의 순액 상계는 정보 훼손을 낳아 상계 위반입니다.", "articles": [], "principle": "수익/비용의 상계 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주식 발행차금 성격이 아닌 손익 성과 거래입니다.", "articles": [], "principle": "수익/비용의 상계 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각 계산과 무관합니다.", "articles": [], "principle": "수익/비용의 상계 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "탈세나 법인세 인위적 편법 유도는 타당치 않습니다.", "articles": [], "principle": "수익/비용의 상계 오류 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "K-IFRS 상 전기 비교정보 표시 원칙에 따라, 당기에 특정 자산의 주석 설명을 업데이트하면서 전기의 주석에 서술되었던 '소송 진행 경과' 텍스트 정보를 그대로 전기 비교 몫으로 남겨 두어야 하는 유일한 준거 요건은 무엇인가?",
        "options": [
            "① 전기의 담당 판사의 실명이 노출되어 있어야 한다.",
            "② 전기 비교 서술형 정보가 당기 재무제표를 이해하는 데 목적적합한(Relevant) 경우에 표시한다.",
            "③ 전기의 소송이 당기에 완전히 무죄 판결로 끝났으면 무조건 삭제해야 한다.",
            "④ 일반 투자자들이 소송 관련 주석 기재를 서면 반대하는 경우에만 표시한다.",
            "⑤ 회사의 영어 법률 자문 비용이 ₩0원인 경우에만 남겨 둔다."
        ],
        "answer": "2",
        "explanation": "② 서술형 전기 비교 정보는 '당기 재무제표의 이해에 목적적합한 경우'에 전기 정보를 비교 형식으로 기재합니다. 소송 경과 등은 과거의 배경을 알아야 당기 소송 충당부채 규모를 정확히 이해할 수 있으므로 전기의 소송 진술 내용을 비교 기재하는 것이 타당합니다.\n\n[오답 해설]\n① 판사 실명 노출 조건은 회계 기준과 다릅니다.\n③ 무죄 판결 종결 시에도 당기 기말 상태의 파악 및 비교를 위해 전기 상태 주석 정보가 목적적합할 수 있으므로 무조건 삭제는 아닙니다.\n④, ⑤는 관련이 없는 엉뚱한 내용입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "법원 관계자 실명 여부는 공시 판단 조건이 아닙니다.", "articles": [], "principle": "서술형 비교 정보 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "소송 연혁처럼 당기 재무제표 맥락 파악에 필요한 전기 설명 정보는 비교 목적 하에 남겨 둡니다.", "articles": [], "principle": "서술형 비교 정보 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "종결 여부와 별개로 비교 목적의 타당성에 따라 유보 여부를 정합니다.", "articles": [], "principle": "서술형 비교 정보 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소수 투자자 서면 반대에 좌우되지 않습니다.", "articles": [], "principle": "서술형 비교 정보 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자문비 크기 연동 조건은 회계 기준에 없습니다.", "articles": [], "principle": "서술형 비교 정보 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "다음 중 K-IFRS 상 상계(Offsetting) 표시가 허용되지 않고 '자산과 부채 각각 총액 기재'하여야 하는 거래 유형에 속하는 것은?",
        "options": [
            "① 확정급여채무와 사외적립자산을 K-IFRS 기준서 제1019호에 의거해 서로 상계하여 순액(순확정급여부채)으로 표시한 경우",
            "② 금융자산과 금융부채에 대해 법적으로 상계할 수 있는 권리를 보유하고 있고 동시에 순액결제할 의도가 있어 관련 기준서에 따라 순액 표시한 경우",
            "③ 동일 고객에 대해 발생한 환불부채(부채)와 고객으로부터 반환받을 반환자산(자산)을 임의 상쇄하여 단일 항목으로 기재한 경우",
            "④ 이연법인세자산과 이연법인세부채를 동일한 과세당국과 법적 권리 요건 하에 상계 표시한 경우",
            "⑤ 처분한 비유동자산의 처분 차익과 차손을 순액 표시한 경우"
        ],
        "answer": "3",
        "explanation": "③ 동일 고객 거래라 하더라도 고객에게 줄 '환불부채(부채)'와 돌려받을 '반환자산(자산)'은 성격과 측정 속성이 서로 다른 독립 요소이므로, 관련 기준서가 상계를 명시적으로 허용하지 않는 한 대등 상쇄할 수 없고 각각 총액 표시하여야 합니다.\n\n[오답 해설]\n① 퇴직연금 사외적립자산 상계, ② 금융자산·부채의 요건 충족 상계, ④ 이연법인세 자산·부채 상계는 개별 기준서가 상계를 명확히 허용·요구하는 정당한 상계 처리 사례입니다.\n⑤ 비유동자산 처분 순액 기재는 상계 위반이 아닌 정형 실무입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "퇴직연금 순액 표시는 기준서 제1019호의 정당한 상계 규정입니다.", "articles": [], "principle": "금지되는 상계 거래 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융자산/부채 상계 요건(권리 + 의도 충족) 만족 시의 상계는 합법입니다.", "articles": [], "principle": "금지되는 상계 거래 식별", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "고객에 대한 환불부채와 반환자산은 서로 구별하여 총액 보고해야 하므로 이를 순액 보고한 3은 위반 사례에 해당합니다.", "articles": [], "principle": "금지되는 상계 거래 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이연법인세 자산/부채의 상계 요건 만족 시 상계는 합법입니다.", "articles": [], "principle": "금지되는 상계 거래 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분손익의 차감 표시는 정당한 상계 범위입니다.", "articles": [], "principle": "금지되는 상계 거래 식별", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "다음 중 K-IFRS 상 표시의 계속성 원칙에 의거해, 기업이 재무제표 항목의 표시와 분류를 전기와 다르게 바꾼 경우에 주석에 의무적으로 밝혀 공시해야 하는 사항이 아닌 것은? (단, 소급 재분류는 실무적으로 가능한 상황이다.)",
        "options": [
            "① 재분류를 실시하게 된 명확한 사유 및 배경",
            "② 재분류된 전기 비교정보 항목의 성격",
            "③ 재분류되어 조정된 전기 비교정보 개별 항목의 재분류 금액",
            "④ 재분류 표시 변경을 사적으로 조언해 준 외부 지인의 상세 신상 명세",
            "⑤ 재분류를 소급 적용함에 따른 전기 각 항목의 장부금액 영향치"
        ],
        "answer": "4",
        "explanation": "④ 표시 분류 변경으로 전기를 소급 재분류한 경우 사유, 재분류 항목의 성격, 재분류 금액 등을 상세히 공시해야 합니다. 그러나 조언을 준 개인(외부 지인 등)의 사적 인적 명세를 주석에 기재하는 것은 회계 의무와 상관없습니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 계속성 변경 공시를 투명하게 제공하기 위해 기준서가 강제하는 정형 주석 공시 사항입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "재분류 사유 공시는 필수 조항입니다.", "articles": [], "principle": "재분류 시 주석 공시 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재분류 항목 성격 설명은 필수 조항입니다.", "articles": [], "principle": "재분류 시 주석 공시 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재분류 금액 정보 기재는 필수입니다.", "articles": [], "principle": "재분류 시 주석 공시 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "외부 관계자의 사적 인적 사항은 회계 공시 대상이 아니므로 4가 답입니다.", "articles": [], "principle": "재분류 시 주석 공시 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소급 재분류 영향치 명시는 중요 공시 항목입니다.", "articles": [], "principle": "재분류 시 주석 공시 요건", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "다음 중 K-IFRS 상 계속기업(Going Concern) 가정 평가 시, 기업의 존속능력에 유의적인 의문이 제기될 수 있는 사건이나 상황(예: 연속된 적자, 채무 불이행 위험 등)과 관련된 '중요한 불확실성'을 알게 된 경우 경영진이 취해야 할 올바른 주석 보고 조치는?",
        "options": [
            "① 불확실성이 해소되기 전까지는 회계 기장을 전면 전 정지하고 아무 공시도 하지 않는다.",
            "② 기업의 신용을 보호하기 위해 관련 불확실성 정보는 주석에서 철저히 숨긴다.",
            "③ 그러한 존속 위기 관련 불확실성 사실을 재무제표 주석에 구체적이고 명확하게 공시하여 정보이용자에게 알려야 한다.",
            "④ 정부 공청회에 출석하여 구두 해명하는 것으로 재무제표 주석 공시를 전면 갈음한다.",
            "⑤ 회사의 최대 채권자에게만 이메일로 비밀리 통보하고 기재하지 않는다."
        ],
        "answer": "3",
        "explanation": "③ 계속기업 존속능력에 심각한 의문이 가는 불확실성이 식별된 경우, 재무제표의 신뢰성을 지키고 오도를 막기 위해 해당 불확실성의 성격과 구체적 사실을 반드시 재무제표 주석에 투명하게 밝히도록 의무화하고 있습니다.\n\n[오답 해설]\n① 기장 정지나 ② 정보 은폐 행위는 분식 및 부실 공시입니다.\n④, ⑤는 회계 기준 상 인정되지 않는 부적절한 대안입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "기장 중단은 불가능한 처리입니다.", "articles": [], "principle": "존속 불확실성의 공시 의무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의도적 정보 은폐는 분식 회계에 해당합니다.", "articles": [], "principle": "존속 불확실성의 공시 의무", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "존속 의문 유발 사건 및 불확실성 요소(자금난 등)는 정보이용자의 의사결정을 위해 반드시 주석 공시되어야 합니다.", "articles": [], "principle": "존속 불확실성의 공시 의무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "행정 구두 설명이 공시 의무를 대체할 수 없습니다.", "articles": [], "principle": "존속 불확실성의 공시 의무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특정인 개별 통보로 공시 의무가 충족되지 않습니다.", "articles": [], "principle": "존속 불확실성의 공시 의무", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },

    # =========================================================================
    # L4: 분석 (8문항, 541~548번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s01-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "K-IFRS 제1001호 '재무제표 표시' 기준서 상 재무제표 표시 일반사항(General Features) 조문에 대한 설명 중 옳은 것을 모두 고른 것은?\n\n```\nㄱ. 부적절한 회계정책은 주석이나 보충설명으로 밝히더라도 정당화될 수 없다.\nㄴ. 현금흐름표를 작성할 때에도 발생기준 회계를 필수적으로 적용하여 작성한다.\nㄷ. 한국채택국제회계기준에서 요구하는 공시 요구사항이더라도 중요하지 않다면 제공할 필요는 없다.\nㄹ. 평가충당금을 차감하여 자산을 순액으로 기재하는 것은 상계에 해당하지 않는다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄷ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ 보기 분석:\nㄱ. 참: 부적절한 회계정책은 설명해도 정당화되지 않습니다.\nㄴ. 거짓: 현금흐름표는 발생기준 회계를 적용하지 않는 예외 재무제표입니다.\nㄷ. 참: IFRS 필수 요구 사항이라도 중요하지 않다면 공시 생략 가능합니다.\nㄹ. 참: 대손충당금 등 평가충당금 차감 측정은 상계가 아닙니다.\n따라서 옳은 보기는 ㄱ, ㄷ, ㄹ 입니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 거짓 설명인 ㄴ 을 포함하고 있어 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄴ이 거짓이므로 ㄱ, ㄴ 조합은 오답입니다.", "articles": [], "principle": "일반사항 종합 정오 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ이 거짓이므로 ㄴ, ㄷ 조합은 오답입니다.", "articles": [], "principle": "일반사항 종합 정오 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "참인 조문 ㄱ, ㄷ, ㄹ만 정확히 고른 3이 정답입니다.", "articles": [], "principle": "일반사항 종합 정오 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ을 포함하고 있어 오답입니다.", "articles": [], "principle": "일반사항 종합 정오 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "모든 보기를 고른 것은 거짓 보기를 포함하여 오답입니다.", "articles": [], "principle": "일반사항 종합 정오 판정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "다음 중 K-IFRS 상 계속기업(Going Concern) 가정 및 평가 불만족 시의 회계처리 규칙에 대한 보기의 주장 중 옳지 않은 것을 모두 고른 것은?\n\n```\nㄱ. 계속기업 가정 평가 시 적어도 보고기간 말로부터 향후 12개월 이상을 검토하여야 한다.\nㄴ. 계속기업 가정이 타당한지 여부를 평가할 때, 경영진은 과거 5년간의 이익 추이 정보만 보면 되며 미래에 관한 정보는 일절 배제하여야 한다.\nㄷ. 재무제표가 계속기업 기준 하에 작성되지 않은 사실이 있더라도 주석에 이를 적시 공시하지 않아도 무방하다.\nㄹ. 경영진이 존속능력에 중대한 의문이 드는 불확실성을 발견한 경우 그 불확실성을 반드시 공시해야 한다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄷ, ㄹ",
            "④ ㄱ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ"
        ],
        "answer": "2",
        "explanation": "② 보기 분석:\nㄱ. 참: 계속기업 검토는 종료일로부터 적어도 12개월 이상입니다.\nㄴ. 거짓: 계속기업은 미래 지향적 평가이므로, 과거 실적뿐만 아니라 미래 정보(가용 정보)를 중점 고려해야 하므로 배제 주장은 오류입니다.\nㄷ. 거짓: 계속기업 기준 미적용 사실은 반드시 주석 공시되어야 합니다. 무방하다는 주장은 오류입니다.\nㄹ. 참: 중대한 불확실성 발견 시 공시가 강제됩니다.\n따라서 옳지 않은(거짓) 보기는 ㄴ, ㄷ 입니다.\n\n[오답 해설]\n① 참인 보기를 포함하고 있어 오답입니다.\n③ 참인 보기 ㄹ을 포함하고 있어 오답입니다.\n④, ⑤는 정오 분류가 잘못된 조합입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ이 참이므로 옳지 않은 보기를 묶는 조합에 부적합합니다.", "articles": [], "principle": "계속기업 가정 조문 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "거짓 진술인 ㄴ과 ㄷ만 정확히 골라 묶은 2가 정답입니다.", "articles": [], "principle": "계속기업 가정 조문 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 참인 보존이므로 틀린 몫에 들어갈 수 없습니다.", "articles": [], "principle": "계속기업 가정 조문 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "참인 조문 ㄱ과 ㄹ을 묶어 오답입니다.", "articles": [], "principle": "계속기업 가정 조문 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "참인 조문 ㄱ을 포함하여 오답입니다.", "articles": [], "principle": "계속기업 가정 조문 판단", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "다음 중 K-IFRS 상 자산·부채 및 수익·비용의 '상계(Offsetting) 표시'에 관한 세부 규정 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 거래나 사건의 실질이 순액 표시로 나타나는 경우를 제외하고는, 상계 표시는 정보이용자의 의사결정 능력을 저해하므로 금지한다.",
            "② 대손충당금이나 재고자산평가충당금 등 평가액 차감 표시는 상계에 해당하지 않는다.",
            "③ 동일한 거래에서 발생한 수익과 관련 비용을 상계하는 것이 거래의 실질을 반영하는 정당한 경우(예: 유형자산처분손익)에는 상계하여 보고한다.",
            "④ 주요 영업활동이 아닌 유사 거래 집합에서 발생하는 차익과 차손은 순액으로 표시할 수 있으나, 중요한 경우에는 구분하여 표시한다.",
            "⑤ 기업이 받을 매출채권과 갚을 매입채무를 관련 계약 및 상계권이 없음에도 단순히 재무비율을 예쁘게 보이게 하고자 임의로 순액 기재하는 행위는 기준서가 보장하는 합법적 상계 범위에 든다."
        ],
        "answer": "5",
        "explanation": "⑤ 계약 상 상계 권리나 순액 결제 의도 없이 자의적으로 매출채권과 매입채무를 지워 순액만 기재하는 것은 상계 금지 규정을 심각하게 위배하는 편법 기장으로 절대 허용되지 않습니다.\n\n[오답 해설]\n①, ②, ③, ④는 K-IFRS 제1001호에 제시된 상계 금지 및 상계 미해당(평가충당금), 정당한 상계 허용 범위(처분손익 등)를 완벽히 해설한 문장들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상계 금지의 취지를 바르게 설명한 조문입니다.", "articles": [], "principle": "상계규정의 예외와 원칙 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평가충당금 순액 측정은 상계가 아님은 참입니다.", "articles": [], "principle": "상계규정의 예외와 원칙 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비유동자산 매각처럼 거래 실질이 상계를 요구 시 허용됨은 참입니다.", "articles": [], "principle": "상계규정의 예외와 원칙 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유사군 순액 공시 및 중요 시 구분 기재 원칙은 참입니다.", "articles": [], "principle": "상계규정의 예외와 원칙 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "상계권 합의가 결여된 일반 채권/채무의 자의적 순액 보고는 원칙 위반이므로 5가 오류입니다.", "articles": [], "principle": "상계규정의 예외와 원칙 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "다음 중 K-IFRS 상 중요성과 통합표시(Materiality and aggregation)의 상호작용 규칙에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 유사한 항목은 중요성 분류에 따라 재무제표에 구분하여 표시하며, 상이한 성격/기능을 가진 항목은 구분 표시함이 원칙이다.",
            "② 중요하지 않은 항목이라도 재무제표(기본 재무제표) 상에는 통합 표시되나, 주석에서는 구분 표시해야 할 만큼 충분히 중요할 수 있다.",
            "③ 특정 회계기준서에서 구체적으로 요구하는 공시 사항은 금액적 중요도가 0원에 가까운 완전 무의미한 항목일지라도 생략 없이 무조건 강제 기재하여야만 공정표시로 본다.",
            "④ 한국채택국제회계기준의 요구에 따라 공시되는 정보가 중요하지 않다면 그 공시를 제공할 필요는 없다.",
            "⑤ 중요성 판단은 해당 정보의 성격이나 규모 또는 이들 모두를 종합 고려해 개별 기업 특유의 측면에서 적용된다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS에 따르면 개별 기준서가 구체적인 특정 주석 정보를 기재하라고 규정하고 있더라도, 그 정보가 '중요하지 않은 경우'라면 회사는 해당 공시를 과감히 생략하고 제공하지 않을 수 있습니다. 맹목적 무조건 기재 요구 설명은 오답입니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 중요성과 통합표시의 한계선 및 기재 유연성을 기준서 조문에 따라 옳게 명시한 문장들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "구분 및 통합표시의 기본 규칙 설명은 참입니다.", "articles": [], "principle": "중요성 기준과 공시 생략 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "표에서는 통합되나 주석에서는 구분될 수 있다는 분석은 참입니다.", "articles": [], "principle": "중요성 기준과 공시 생략 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "IFRS 개별 요구사항이라도 중요치 않으면 생략할 수 있으므로, 무조건 기재를 강제한다는 3이 틀렸습니다.", "articles": [], "principle": "중요성 기준과 공시 생략 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중요하지 않은 공시는 생략할 수 있다는 직접 규정은 참입니다.", "articles": [], "principle": "중요성 기준과 공시 생략 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중요성은 성격과 규모를 모두 고려하는 기업 특유의 속성이라는 점은 참입니다.", "articles": [], "principle": "중요성 기준과 공시 생략 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "다음 중 K-IFRS 상 표시의 계속성(Consistency of presentation) 원칙을 적용하여 재무제표 항목의 표시와 분류방법을 부득이하게 변경한 경우, 소급 재분류에 관한 세부 규칙으로 가장 올바른 것은?",
        "options": [
            "① 표시방법 변경 시에는 전기의 비교 수치를 재분류하지 않고 당기부터 전진 적용함이 강제 대원칙이다.",
            "② 실무적으로 불가능하지 않은 한, 전기 비교정보 항목도 소급하여 재분류 표시하고 관련 재분류 금액, 항목 성격 및 변경 사유를 주석에 밝혀야 한다.",
            "③ 전기의 비교정보를 소급 재분류하는 행위는 과거 정보 왜곡 조작 행위에 해당하므로 형사 처벌 대상이다.",
            "④ 전기 정보 소급 재분류 시 당기 수치는 건드리지 않고 전기 수치만 마음대로 임의 조작해 맞춰둔다.",
            "⑤ 실무적인 이유로 소급 재분류가 불가능하다면 표시방법 변경 자체를 법적으로 완전히 원천 금지한다."
        ],
        "answer": "2",
        "explanation": "② 표시 및 분류 변경 시에는 전기의 비교 정보도 소급하여 재분류하여 표시하는 소급 재분류법이 대원칙입니다. 단, 실무적으로 불가능한 극히 제한적 상황에서만 예외가 인정됩니다.\n\n[오답 해설]\n① 소급 재분류가 원칙이므로 전진 적용 강제 주장은 틀렸습니다.\n③ 비교가능성을 위한 정당한 소급 재분류는 적법합니다.\n④ 임의 조작이 아닌 합리적 소급 조정을 거칩니다.\n⑤ 실무적 불가능성 시 변경 자체를 완전 금지하지 않고 대신 불가능한 이유와 재분류하지 못한 내역을 공시하도록 구제 조항을 두고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "표시 변경 시 전진 적용 강제는 기준과 맞지 않는 오답입니다.", "articles": [], "principle": "소급 재분류와 계속성 원칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비교가능성을 해치지 않기 위해 실무적 불가능 외에는 전기 비교정보도 소급 재분류하고 관련 내역을 공시하여야 합니다.", "articles": [], "principle": "소급 재분류와 계속성 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소급 재분류는 형사 처벌 대상이 아닌 합법적 의무 사항입니다.", "articles": [], "principle": "소급 재분류와 계속성 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 기장 조작 설명은 오답입니다.", "articles": [], "principle": "소급 재분류와 계속성 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실무적 적용 한계 시 공시 대체 규정이 있으므로 원천 금지 주장은 틀렸습니다.", "articles": [], "principle": "소급 재분류와 계속성 원칙", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "다음 중 K-IFRS 상 재무제표 공시 시 경영진이 밝혀야 하는 '회계정책 적용 과정에서의 유의적 판단(Judgments)'과 '추정 불확실성의 핵심 원천(Sources of estimation uncertainty)'에 대한 설명 중 가장 옳지 않은 것은?",
        "options": [
            "① 유의적 판단과 추정의 불확실성은 정보이용자가 재무제표 가치 평가 프로세스를 이해하는 데 도움을 주므로 둘 다 주석 공시 대상이다.",
            "② 금융자산의 사업모형 평가나 투자부동산으로의 분류 결정 등은 경영진의 '유의적 판단'의 예시에 속한다.",
            "③ 기말 시점 충당부채나 복구의무 부채 평가 시 미래 인플레이션이나 할인율을 얼마로 설정할 것인지 등은 '추정 불확실성의 원천'에 대응된다.",
            "④ 유의적 판단에 대한 공시와 추정의 불확실성에 대한 공시는 서로 다른 공시 요구사항으로 주석 상에서 명확히 성격을 구분해 공시하는 것이 권장된다.",
            "⑤ 두 사항 모두 기업의 영업 기밀 유출 방지를 위해 어떠한 수치나 사유도 주석에 구체적으로 적지 않고 단순 제목만 한 줄 적어두도록 강제된다."
        ],
        "answer": "5",
        "explanation": "⑤ 유의적 판단과 추정의 불확실성 공시는 정보이용자의 신뢰성을 확보하기 위한 주석 공시입니다. 단순히 기밀 유지를 핑계로 사유나 산정 기초 가정을 가려 제목만 적는 것은 공시 불성실에 해당하므로, 구체적 판단의 배경과 추정의 불확실성 영향 금액을 투명하게 보고하여야 합니다.\n\n[오답 해설]\n①, ②, ③, ④는 경영진의 판단 공시와 추정 불확실성 공시의 정의, 예시, 상호 구별 필요성을 정확히 설명하고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "두 항목 모두 중요한 주석 공시 정보임은 참입니다.", "articles": [], "principle": "판단 공시와 추정 공시 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융자산 사업모형 평가 등은 유의적 회계 판단의 정당한 예시입니다.", "articles": [], "principle": "판단 공시와 추정 공시 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 할인율 추정 등은 추정의 불확실성 원천 예시가 맞습니다.", "articles": [], "principle": "판단 공시와 추정 공시 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "두 정보의 성격이 달라 주석 상 성격 구분이 필요함은 참입니다.", "articles": [], "principle": "판단 공시와 추정 공시 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "제목만 한 줄 적는 것은 부실 공시를 유발하므로, 구체적 산정 가정 및 민감도 분석 등을 공시해야 하므로 5가 오류입니다.", "articles": [], "principle": "판단 공시와 추정 공시 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "극히 드문 상황으로서 K-IFRS의 요구사항을 준수하는 것이 개념체계 목적과 상충되어 오해를 유발함에 따라 요구사항을 달리 적용(일탈)하고 감독체계가 이를 허용하는 경우, 기업이 주석에 구체적으로 밝혀야 하는 사항으로 가장 올바르지 않은 것은?",
        "options": [
            "① 경영진이 재무제표가 기업의 재무상태, 재무성과 및 현금흐름을 공정하게 표시하고 있다고 결론지은 사실",
            "② 한국채택국제회계기준의 유효한 요구사항을 모두 준수하였다는 사실(단, 공정한 표시를 달성하기 위해 특정 요구사항을 달리 적용한 경우 제외)",
            "③ 일탈을 권유하거나 자문해 준 외부 회계 컨설팅 회사의 계좌 번호 및 총 자문비 송금 증빙 내역",
            "④ 달리 적용함으로써 일탈하게 된 해당 한국채택국제회계기준 요구사항의 성격, 기준서가 요구하는 처리방법, 그 요구사항을 준수한다면 오히려 재무제표이용자에게 오해를 유발하여 개념체계 상 목적과 상충되는 세부 사유",
            "⑤ 달리 적용하여 채택한 회계처리방법 및 그로 인해 표시된 재무제표의 각 기간별 개별 재무제표 항목에 미치는 구체적 재무적 영향액"
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 일탈 시 주석에는 경영진의 공정표시 판단 결론, 관련 조문 성격 및 대안 처리방안, 오해 유발 사유 및 재무적 영향치 등이 공시되어야 합니다. 그러나 자문을 준 외부 기관의 계좌번호나 자문 비용 송금 영수증 등 사적 금융 증빙을 주석에 공시할 회계 상 이유는 없습니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 예외적 일탈 처리가 정당화될 때 정보이용자 오해 최소화를 위해 기준서 제1001호가 강제하는 엄격한 공시 리스트 항목들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "경영진의 공정표시 확인 사실 공시는 필수 규정입니다.", "articles": [], "principle": "IFRS 일탈 시 필수 공시 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일탈 조항 외의 기준서 전반적 준수 확인 명시는 필수입니다.", "articles": [], "principle": "IFRS 일탈 시 필수 공시 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "컨설팅사의 사적 금융 계좌 정보나 비용 송금증 기재 의무는 없으므로 3이 오답입니다.", "articles": [], "principle": "IFRS 일탈 시 필수 공시 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일탈한 기준 조문 설명 및 오해 유발 사유 기재는 필수입니다.", "articles": [], "principle": "IFRS 일탈 시 필수 공시 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재무제표 각 계정에 미친 개별 영향 금액 기재는 필수입니다.", "articles": [], "principle": "IFRS 일탈 시 필수 공시 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "다음 중 K-IFRS 상 비교정보(Comparative information) 표시 원칙과 소급 적용에 대한 보기의 설명 중 옳은 것을 모두 고른 것은?\n\n```\nㄱ. 전기의 특정 서술형 정보가 당기 재무제표를 이해하는 데 목적적합하더라도 전기 비교 몫으로 남겨 둘 수 없다.\nㄴ. 당기 재무제표의 표시 분류 변경 시 실무적으로 불가능한 극히 이례적인 예외를 제외하고는 전기 비교 수치도 소급 재분류한다.\nㄷ. 소급 재분류가 불가능하여 전기 수치를 조정하지 못한 경우 그 이유와 조정하지 못한 구체적 사유 및 금액을 별도 공시해야 한다.\nㄹ. 전기의 기본 재무제표 수치 일부가 분식 회계 오류로 판명되어도 소급 수정하지 않고 당기 당기순이익에서 일괄 가감하여 조정한다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄷ, ㄹ",
            "④ ㄱ, ㄴ, ㄹ",
            "⑤ ㄴ, ㄷ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 보기 분석:\nㄱ. 거짓: 당기 이해에 유용하면 서술 정보도 비교 표시합니다.\nㄴ. 참: 표시 분류 변경 시 전기 비교정보 소급 재분류가 원칙입니다.\nㄷ. 참: 소급 재분류 불가능 시 사유와 세부 정보를 주석 공시하여 보완합니다.\nㄹ. 거짓: 분식 오류 등 중대 오류 발견 시에는 기준서 제1008호에 따라 소급하여 전기 재무제표를 재작성(Restatement)해야 하며 당기 손익에 일괄 가감 상계 처리할 수 없습니다.\n따라서 옳은 보기는 ㄴ, ㄷ 입니다.\n\n[오답 해설]\n① 거짓 보기 ㄱ을 포함해 오답입니다.\n③, ④, ⑤는 거짓 보기 ㄹ 등을 포함하고 있어 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ이 거짓이므로 오답입니다.", "articles": [], "principle": "비교정보 및 소급규칙 정오판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "참인 진술 ㄴ과 ㄷ만 명확하게 묶어 선별한 2가 정답입니다.", "articles": [], "principle": "비교정보 및 소급규칙 정오판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 소급 재작성 원칙에 반하는 가공의 처리로 오류입니다.", "articles": [], "principle": "비교정보 및 소급규칙 정오판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ과 ㄹ을 포함해 오답입니다.", "articles": [], "principle": "비교정보 및 소급규칙 정오판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ을 포함해 오답입니다.", "articles": [], "principle": "비교정보 및 소급규칙 정오판단", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },

    # =========================================================================
    # L5: 심화 (2문항, 549~550번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s01-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "(주)평가는 당기 중 대규모 영업양수로 인해 주된 영업 기능이 유통업에서 제조업으로 전격 재편되었다. 이로 인하여 기존의 매출 원가 분류 체계 및 표시 방법을 전면 변경하는 것이 정보의 목적적합성 제고에 명백히 타당하다고 판단하였다. 그러나 전산 시스템 백업 소실 및 과거 물류 데이터 유실로 인해 전기의 비교 수치를 새로운 제조업 분류 체계에 맞춰 소급 재분류하는 것이 실무적으로 완전히 불가능(Impracticable)한 한계 상황에 직면하였다. 이 경우 K-IFRS 계속성 및 비교정보 규칙에 의거한 (주)평가의 가장 타당한 대처 및 공시 방향은?",
        "options": [
            "① 전기 비교 수치 재분류가 불가능하므로 당기의 표시방법 변경 자체를 완전 취소하고 유통업 기장을 고수한다.",
            "② 전기 비교 수치를 임의의 대략적인 수치로 가공하여 임의 기재한 후 정상 소급했다고 보고한다.",
            "③ 소급 재분류를 적용하지 않는 대신, 1) 비교 수치를 재분류하지 않은 구체적 사유, 2) 전기를 새로운 기준으로 재분류했을 경우 조정되었을 금액의 성격 및 영향치를 주석에 투명하게 공시하여 목적적합성 훼손을 보완한다.",
            "④ 기말 감가상각비를 전액 ₩0원으로 하여 소급 불가능 손실액과 직접 상계 제거한다.",
            "⑤ 회계 감사를 포기하고 단식부기 약식 재무보고서로 강등 공시한다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 상 실무적으로 전기 비교정보의 소급 재분류가 불가능한 상황인 경우, 표시방법의 합리적 변경 자체를 강제로 금지하지는 않습니다. 대신 소급 재분류하지 못한 이유와 재분류했을 시 조정되었을 성격 등을 주석에 상세 공시하여 정보이용자의 비교 분석을 대안적으로 보완해야 합니다.\n\n[오답 해설]\n① 명백히 개선된 표시방법 적용을 무조건 포기할 필요는 없습니다.\n② 임의의 가공 수치 기재는 분식 및 부실 감사 대상입니다.\n④ 감가상각과의 직접적 상계는 타당치 않습니다.\n⑤ 감사 포기 등은 상장 또는 회계 감사 대상 기업의 합법적 대처가 아닙니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "표시방법의 명백한 목적적합성 개선 변경까지 포기하게 강제하지 않습니다.", "articles": [], "principle": "소급재분류 불능 시 조치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가짜 데이터를 장부에 적는 것은 분식 회계 범죄입니다.", "articles": [], "principle": "소급재분류 불능 시 조치", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "실무적 불가능 한계 시에는 소급 미적용 사실, 사유 및 조정액 성격을 주석 기재하여 정보 제공의 공정성을 확보해야 하므로 3이 정답입니다.", "articles": [], "principle": "소급재분류 불능 시 조치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각비 강제 차감은 분식입니다.", "articles": [], "principle": "소급재분류 불능 시 조치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단식부기 강등 공시는 불법입니다.", "articles": [], "principle": "소급재분류 불능 시 조치", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 5,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s01-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "(주)평가의 경영진은 당기 중 자산의 인식 요건(미래 경제적 효익의 유입 가능성이 극히 낮음)을 충족하지 못하는 연구개발비용 ₩5,000,000을 재무상태표에 '개발비(무형자산)'로 계상하였다. 이후 재무제표 주석에 '본 개발비는 K-IFRS 기준 상 자산 요건을 충족하지 않으나, 회사의 주가 방어 및 금융권 차입 한도 유지를 위해 부득이하게 자산으로 적었음을 고백합니다'라고 매우 솔직하고 상세히 그 사유를 공시하였다. 이 재무제표의 공정한 표시(Fair presentation)와 K-IFRS 준수 사실 기재(Statement of compliance)의 회계학적 적법성에 대한 최종 논파 판정은?",
        "options": [
            "① 주석에 그 사유를 사실대로 솔직하게 고백했으므로 회계 기준을 완벽하게 준수한 정당한 재무제표이다.",
            "② 부적절한 회계정책은 주석이나 보충자료로 밝히더라도 결코 정당화될 수 없으므로, (주)평가의 재무제표는 명백한 회계 기준 위반 재무제표이며 K-IFRS 준수 사실을 기재해서는 아니 된다.",
            "③ 주가 방어 목적이 입증되면 한시적으로 적법화되는 IFRS 특별 예외 조항에 해당한다.",
            "④ 자산 금액이 ₩5,000,000으로 적은 금액이므로 중요성 제약에 따라 무조건 타당하다.",
            "⑤ 회사의 외부 감사인이 묵인해 준다면 공정표시로 법적 의제된다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS의 대원칙에 따라, 자산 인식 요건에 부합하지 않는 항목을 임의로 자산 처리하는 부적절한 회계정책은 주석에 구체적 의도나 배경을 아무리 투명하게 고백하더라도 정당화되지 않습니다. 따라서 해당 재무제표는 기준 위반 상태이므로 K-IFRS를 준수하여 작성되었다고 공시해서는 아니 됩니다.\n\n[오답 해설]\n① 주석 고백이 위반 분개를 합법화하지 못합니다.\n③ 주가 방어 목적의 예외 조항은 존재하지 않습니다.\n④ 인식 요건 자체를 전면 위배하여 고의 계상한 것은 중요성 배제 사유가 아닙니다.\n⑤ 감사인의 묵인 여부가 기준의 적법 여부를 결정하지 못합니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "주석 설명이나 솔직한 고백으로 부적절한 자산 가공이 정당화될 수 없습니다.", "articles": [], "principle": "부적절한 회계정책과 K-IFRS 준수기재", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기준서 조문에 직시된 바에 따라, 주석 설명 여부와 관계없이 정당화되지 않으므로 K-IFRS 준수 표시를 할 수 없어 2가 정답입니다.", "articles": [], "principle": "부적절한 회계정책과 K-IFRS 준수기재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주가방어 연동 예외 기준은 없습니다.", "articles": [], "principle": "부적절한 회계정책과 K-IFRS 준수기재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인식 조건 미달의 의도적 왜곡 기장은 중요성을 불문하고 위반입니다.", "articles": [], "principle": "부적절한 회계정책과 K-IFRS 준수기재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사인의 단순 묵인이 위반 사실을 정당화하지 못합니다.", "articles": [], "principle": "부적절한 회계정책과 K-IFRS 준수기재", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 5,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제1장 회계의 기초",
                "section": "Chapter 02 재무제표 표시",
                "item": "1절 재무제표"
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
