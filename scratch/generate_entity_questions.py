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
        "id": "practice-accounting-ch01s05-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "개념체계상 '보고기업(Reporting Entity)'에 관한 정의로 가장 올바른 것은?",
        "options": [
            "① 재무제표를 작성해야 하거나 작성하기로 선택한 기업으로, 반드시 법적 실체여야만 한다.",
            "② 재무제표를 작성해야 하거나 작성하기로 선택한 기업으로, 반드시 단일의 법적 실체로만 구성된다.",
            "③ 재무제표를 작성해야 하거나 작성하기로 선택한 기업으로, 반드시 둘 이상의 실체로만 구성된다.",
            "④ 재무제표를 작성해야 하거나 작성하기로 선택한 기업으로, 법적 실체일 수도 있고 법적 실체가 아닐 수도 있다.",
            "⑤ 국세청에 소득세 신고 의무를 가지는 영리 법인만을 제한하여 일컫는 용어이다."
        ],
        "answer": "4",
        "explanation": "④ 개념체계상 보고기업은 재무제표를 작성해야 하거나 작성하기로 선택한 기업을 말합니다. 보고기업은 단일 실체일 수도 있고, 실체의 일부일 수도 있으며, 둘 이상의 실체로 구성될 수도 있습니다. 또한 보고기업이 반드시 법적 실체일 필요는 없습니다.\n\n[오답 해설]\n①, ②, ③ 보고기업이 반드시 법적 실체일 필요는 없으며, 단일 실체나 실체의 일부, 둘 이상의 실체 모두 가능합니다.\n⑤ 국세청 소득세 신고 의무 영리법인에만 제한되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "반드시 법적 실체여야 하는 것은 아닙니다.", "articles": [], "principle": "보고기업의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단일의 법적 실체 외에 실체의 일부나 둘 이상의 실체도 가능합니다.", "articles": [], "principle": "보고기업의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단일 실체나 실체의 일부도 보고기업이 될 수 있습니다.", "articles": [], "principle": "보고기업의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기업은 법적 실체일 수도 있고 법적 실체가 아닐 수도 있습니다.", "articles": [], "principle": "보고기업의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법상의 영리법인 개념에 한정되지 않습니다.", "articles": [], "principle": "보고기업의 정의", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "지배기업과 종속기업이 존재하는 상황에서, 지배기업과 종속기업을 단일 보고기업으로 보아 작성하는 재무제표의 명칭은?",
        "options": [
            "① 별도재무제표",
            "② 연결재무제표",
            "③ 결합재무제표",
            "④ 비연결재무제표",
            "⑤ 혼합재무제표"
        ],
        "answer": "2",
        "explanation": "② 보고기업이 지배기업과 그 종속기업들로 구성된다면 그 보고기업의 재무제표를 '연결재무제표'라고 부릅니다.\n\n[오답 해설]\n①, ④ 지배기업 단독의 재무제표는 비연결재무제표(또는 별도재무제표)라고 합니다.\n③ 지배-종속관계로 모두 연결되지 않은 둘 이상 실체로 구성된 경우의 재무제표는 결합재무제표입니다.\n⑤ 혼합재무제표는 개념체계상 공식 명칭이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지배기업 단독의 정보를 제공하는 것은 별도재무제표(비연결재무제표)입니다.", "articles": [], "principle": "재무제표의 종류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "지배기업과 종속기업을 단일 보고기업으로 보는 재무제표는 연결재무제표입니다.", "articles": [], "principle": "연결재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지배-종속관계가 아닌 둘 이상 실체의 재무제표는 결합재무제표입니다.", "articles": [], "principle": "결합재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비연결재무제표는 지배기업만의 자산/부채 등을 보여줍니다.", "articles": [], "principle": "비연결재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "혼합재무제표는 공식 용어가 아닙니다.", "articles": [], "principle": "기타", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "보고기업이 지배-종속관계로 모두 연결되어 있지는 않은 둘 이상의 실체들로 구성된다면, 그 보고기업의 재무제표를 무엇이라 부르는가?",
        "options": [
            "① 연결재무제표",
            "② 결합재무제표",
            "③ 비연결재무제표",
            "④ 통합재무제표",
            "⑤ 다원재무제표"
        ],
        "answer": "2",
        "explanation": "② 보고기업이 지배-종속관계로 모두 연결되어 있지는 않은 둘 이상 실체들로 구성된다면 그 보고기업의 재무제표를 '결합재무제표'라고 부릅니다.\n\n[오답 해설]\n① 연결재무제표는 지배-종속관계로 묶인 실체들의 재무제표입니다.\n③ 비연결재무제표는 지배기업 단독의 재무제표입니다.\n④, ⑤ 통합재무제표와 다원재무제표는 개념체계상 공식 정의 용어가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "연결재무제표는 지배-종속 관계가 있는 경우입니다.", "articles": [], "principle": "연결재무제표", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "지배-종속관계가 아닌 둘 이상 실체로 구성된 보고기업의 재무제표는 결합재무제표입니다.", "articles": [], "principle": "결합재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비연결재무제표는 단독 기업 기준입니다.", "articles": [], "principle": "비연결재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "통합재무제표는 공식 용어가 아닙니다.", "articles": [], "principle": "기타", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "다원재무제표는 공식 용어가 아닙니다.", "articles": [], "principle": "기타", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "개념체계상 재무제표 이용자들이 변화와 추세를 식별하고 평가하는 것을 돕기 위해, 재무제표는 최소한 언제에 대한 비교정보를 제공하여야 하는가?",
        "options": [
            "① 당기 보고기간 말 당일의 정보만 제공하면 되며 비교정보는 필요 없다.",
            "② 최소한 직전 5개년도에 대한 비교정보를 제공해야 한다.",
            "③ 최소한 직전 연도(기간)에 대한 비교정보를 제공해야 한다.",
            "④ 최소한 최근 10개년도의 반기 평균 비교정보를 제공해야 한다.",
            "⑤ 비교정보는 주요이용자의 요구가 있을 때에 한해 당기에만 선택 제공한다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계상 재무제표이용자들이 변화와 추세를 식별하고 평가하는 것을 돕기 위해, 재무제표는 최소한 직전 연도(Preceding Period)에 대한 비교정보를 제공합니다.\n\n[오답 해설]\n① 비교정보는 필수입니다.\n②, ④ 직전 5년이나 10년 평균이 최소 요구 조건은 아닙니다.\n⑤ 이용자의 요구와 무관하게 정기적으로 직전 연도 비교정보를 최소한 제공하여야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비교정보는 기본적으로 요구되는 공시 사항입니다.", "articles": [], "principle": "비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "5개년도는 최소 요구 기준이 아닙니다.", "articles": [], "principle": "비교정보", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "최소한 직전 연도에 대한 비교정보를 제공하여야 합니다.", "articles": [], "principle": "비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "10개년도가 최소 요건이 아닙니다.", "articles": [], "principle": "비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비교정보는 선택 제공 사항이 아닙니다.", "articles": [], "principle": "비교정보", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "재무제표가 채택하는 관점(Perspective)에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 지배기업의 소액주주 집단만을 위한 전용 관점에서 정보를 기술한다.",
            "② 기업의 자원 제공자 중 특정 집단의 관점이 아닌, 보고기업 전체의 관점에서 정보를 제공한다.",
            "③ 보고기업 경영진의 자산 취득 성향에 초점을 맞춘 주관적 관점을 채택한다.",
            "④ 정부 세무당국의 과세 소득 확보 가능성만을 최우선시하는 세제 관점을 채택한다.",
            "⑤ 지배력을 행사하는 지배주주 1인의 개인적 투자 포트폴리오 극대화 관점을 채택한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 따르면, 재무제표는 기업의 현재 및 잠재적 투자자, 대여자와 그 밖의 채권자 중 특정 집단의 관점이 아닌 보고기업 전체의 관점(Perspective of the Reporting Entity as a Whole)에서 거래 및 그 밖의 사건에 대한 정보를 제공합니다.\n\n[오답 해설]\n①, ③, ④, ⑤ 소액주주, 경영진, 세무당국, 지배주주 등 특정 집단의 개별적 관점은 배격됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "특정 소액주주 집단의 관점이 아닙니다.", "articles": [], "principle": "재무제표 관점", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기업 전체의 관점에서 거래 정보를 제공하는 것이 원칙입니다.", "articles": [], "principle": "재무제표 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진의 주관적 관점이 아닙니다.", "articles": [], "principle": "재무제표 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무당국의 관점이 아닙니다.", "articles": [], "principle": "재무제표 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지배주주 개인의 관점이 아닙니다.", "articles": [], "principle": "재무제표 관점", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "개념체계상 '계속기업가정(Going Concern)'의 기본적인 가정으로 가장 옳은 것은?",
        "options": [
            "① 보고기업이 3개월 이내에 자발적으로 영업을 종료할 것이라는 가정",
            "② 보고기업이 계속기업이며 예측가능한 미래에 영업을 계속할 것이라는 가정",
            "③ 국가가 존속하는 한 기업도 강제로 영구히 존속하여야 한다는 사법적 강제 가정",
            "④ 모든 자산을 공정가치로 매일 재평가하여 청산가치로 기재해야 한다는 가정",
            "⑤ 회사가 조만간 영업을 중단하여 자산을 처분할 계획이 확실하다는 가정"
        ],
        "answer": "2",
        "explanation": "② 재무제표는 일반적으로 보고기업이 계속기업이며 예측가능한 미래에 영업을 계속할 것이라는 가정 하에 작성됩니다.\n\n[오답 해설]\n①, ⑤ 청산이나 영업 중단 의도가 없음을 전제합니다.\n③ 영구 존속을 법적으로 강제하는 법률적 의무가 아닙니다.\n④ 계속기업이 유효할 때에는 청산가치 평가를 강제하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "단기 청산을 가정하지 않습니다.", "articles": [], "principle": "계속기업가정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "계속기업이며 예측가능한 미래에 영업을 계속한다는 가정입니다.", "articles": [], "principle": "계속기업가정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사법적 영구 존속 강제 의무가 아닙니다.", "articles": [], "principle": "계속기업가정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매일 청산가치 재평가를 전제하지 않습니다.", "articles": [], "principle": "계속기업가정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업 중단 계획이 없음을 기본 전제로 합니다.", "articles": [], "principle": "계속기업가정", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "K-IFRS 제1001호 '재무제표 표시'에 의할 때, 계속기업가정의 적절성을 평가하기 위해 경영진이 고려해야 하는 미래 기간에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 보고기간말로부터 적어도 3개월 이내의 기간",
            "② 보고기간말로부터 적어도 6개월 이내의 기간",
            "③ 보고기간말로부터 적어도 12개월(1년) 이상의 기간",
            "④ 보고기간말로부터 적어도 5년 이상의 기간",
            "⑤ 평가 시점으로부터 과거 1년 동안의 소급 기간"
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1001호(재무제표 표시)에 따르면 계속기업의 가정이 적절한지의 여부를 평가할 때 경영진은 적어도 보고기간말로부터 향후 12개월(1년) 기간에 대하여 이용가능한 모든 정보를 고려해야 합니다.\n\n[오답 해설]\n①, ② 12개월보다 짧은 기간(3개월, 6개월 등)은 기준서상 요건에 미달합니다.\n④ 5년 이상을 의무적으로 최소 평가 기준으로 요구하지 않습니다.\n⑤ 과거 소급 기간이 아닌 보고기간말로부터 향후(미래) 기간을 평가합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "3개월은 기준서상 최소 고려 기간이 아닙니다.", "articles": [], "principle": "평가 기간", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "6개월은 기준서상 최소 고려 기간이 아닙니다.", "articles": [], "principle": "평가 기간", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "적어도 보고기간말로부터 향후 12개월 기간에 대한 정보를 고려하여야 합니다.", "articles": [], "principle": "평가 기간", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "5년은 최소 요구 기간이 아닙니다.", "articles": [], "principle": "평가 기간", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래의 정보를 고려해야 하므로 과거 소급이 아닙니다.", "articles": [], "principle": "평가 기간", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "보고기업이 청산을 하거나 거래를 중단하려는 의도나 필요가 존재하여 계속기업 가정이 타당하지 않은 경우, 재무제표 작성법에 대한 개념체계의 요구로 가장 올바른 것은?",
        "options": [
            "① 작성 자체를 거부하고 보고서를 미공시해야 한다.",
            "② 계속기업 원칙에 따라 평소와 똑같이 작성하고 주석에도 이를 언급하지 않는다.",
            "③ 계속기업과는 다른 기준에 따라 작성되어야 하며, 재무제표에 사용된 기준을 기술하여야 한다.",
            "④ 정부 공무원에게 위임하여 임의로 작성하도록 방치한다.",
            "⑤ 주주 총회를 생략하고 세무 장부를 대신 공시한다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계에 따르면 기업이 청산을 하거나 거래를 중단하려는 의도나 필요가 있다면, 재무제표는 계속기업과는 다른 기준(청산가치 등)에 따라 작성되어야 하며, 사용된 기준을 재무제표에 기술하여야 합니다.\n\n[오답 해설]\n① 청산 상태라도 재무제표 공시 책임은 유효하므로 보고를 생략해선 안 됩니다.\n② 계속기업 가정이 깨졌으므로 대체 기준으로 전환하고 주석에 밝혀야 합니다.\n④, ⑤ 정당한 회계 처리 의무가 방치되거나 주총 생략 등으로 대체될 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재무보고 자체를 전면 생략할 수 없습니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계속기업 가정이 깨졌을 때는 대체 기준을 사용하여야 합니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "계속기업과 다른 기준에 따라 작성하고, 사용한 기준을 재무제표에 명시하여야 합니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 작성을 방치해선 안 됩니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 장부로 재무보고를 대체할 수 없습니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "개념체계상 '비연결재무제표(Unconsolidated Financial Statements)'에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 지배기업과 종속기업을 모두 합쳐서 단일 실체로 보고하는 재무제표이다.",
            "② 종속기업에 대해서가 아닌 지배기업 단독의 자산, 부채, 자본, 수익 및 비용 정보를 제공하도록 설계된 재무제표이다.",
            "③ 지배-종속 관계가 전혀 없는 독립 기업들이 작성하는 임의의 공익 재무제표이다.",
            "④ 연결재무제표가 요구되는 경우에도 연결재무제표를 완전히 대체하여 단독 제출할 수 있는 충분한 재무제표이다.",
            "⑤ 지배기업 대주주의 개인 가계부 내역만을 보여주기 위해 만들어진 재무보고서이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 따르면 비연결재무제표는 종속기업에 대해서가 아닌 지배기업의 자산, 부채, 자본, 수익 및 비용에 대한 정보를 제공하도록 만들어집니다.\n\n[오답 해설]\n① 지배기업과 종속기업을 합쳐서 단일 보고기업으로 보는 것은 연결재무제표입니다.\n③ 지배-종속 관계 하에서 지배기업 단독의 서술입니다.\n④ 비연결재무제표에 제공되는 정보는 주요이용자의 정보 수요를 충족하기에 불충분하므로 연결재무제표가 요구되는 경우 연결재무제표를 대신할 수 없습니다.\n⑤ 개인 가계부 정보가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지배기업과 종속기업을 합치는 것은 연결재무제표입니다.", "articles": [], "principle": "비연결재무제표", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비연결재무제표는 종속기업이 아닌 지배기업의 정보를 제공하는 것입니다.", "articles": [], "principle": "비연결재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지배-종속 관계가 존재할 때 지배기업의 정보 제공용입니다.", "articles": [], "principle": "비연결재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비연결재무제표는 연결재무제표를 대신할 수 없습니다.", "articles": [], "principle": "비연결재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지배주주 개인의 정보 보고 수단이 아닙니다.", "articles": [], "principle": "비연결재무제표", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "재무제표에 주석 등으로 포함하는 '미래전망 정보(Forward-looking Information)'에 관한 개념체계의 수록 기준으로 가장 올바른 것은?",
        "options": [
            "① 과거에 일어났던 어떠한 자산/부채 거래와도 상관없는 미래의 모든 상상 시나리오 정보",
            "② 보고기간말 현재 또는 보고기간 중 존재했던 실체의 자산, 부채, 자본, 수익, 비용과 관련되며 이용자에게 유용한 경우",
            "③ 회계기준위원회가 당기 결산일에 지정해 준 특정 미래 예측 주가 수치",
            "④ 세무 감면 혜택을 10년 뒤에 얼마나 얻게 될지 경영진이 임의 보증하는 자의적 정보",
            "⑤ 경쟁회사의 미래 제품 개발비 상세 견적서 정보"
        ],
        "answer": "2",
        "explanation": "② 개념체계에 따르면 미래전망 정보가 보고기간말 현재 또는 보고기간 중 존재했던 실체의 자산, 부채(미인식 항목 포함)나 자본, 보고기간의 수익이나 비용과 관련되며 이용자들에게 유용하다면 재무제표에 포함합니다.\n\n[오답 해설]\n①, ④ 과거 재무제표 요소(자산, 부채 등)와 인과관계가 없거나 자의적인 상상 정보는 수록 대상이 아닙니다.\n③ 회계기준위원회가 특정 주가를 지정 공시해 주지 않습니다.\n⑤ 타사 기밀 정보가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "과거 재무요소와 연계되지 않은 상상 시나리오는 포함하지 않습니다.", "articles": [], "principle": "미래전망 정보", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기간말 현재 또는 기간 중 존재한 자산/부채 등과 관련되고 유용하다면 미래전망 정보를 포함합니다.", "articles": [], "principle": "미래전망 정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기준위원회가 주가를 고시하지 않습니다.", "articles": [], "principle": "미래전망 정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진의 자의적 보증 정보를 싣는 수단이 아닙니다.", "articles": [], "principle": "미래전망 정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경쟁사 기밀 정보 공시 조항이 아닙니다.", "articles": [], "principle": "미래전망 정보", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },

    # =========================================================================
    # L2: 이해 수준 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s05-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "보고기업의 법적 경계와 회계적 경계의 불일치 가능성에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 보고기업은 단일 실체일 수도 있고, 실체의 일부일 수도 있다.",
            "② 보고기업이 반드시 법적 실체일 필요는 없으므로, 법인격이 없는 공동 사업 부문도 보고기업이 될 수 있다.",
            "③ 지배기업과 그 종속기업으로 구성된 보고기업은 법적 지위가 없는 하나의 추상적 가상 실체이지만 재무보고상 의미를 가진다.",
            "④ 보고기업이 법적 실체가 아닐 때 그 경계는 주요이용자의 정보 수요에 맞춰 자의적 누락 없이 결정해야 한다.",
            "⑤ 개념체계에 따라 보고기업이 성립하기 위해서는 반드시 법원 등기소에 등록된 독립된 법적 실체여야만 한다."
        ],
        "answer": "5",
        "explanation": "⑤ 개념체계에 명시적으로 보고기업이 반드시 법적 실체일 필요는 없다고 규정되어 있습니다. 따라서 등기소 등록 법인격이 없더라도 보고기업으로 기능할 수 있습니다.\n\n[오답 해설]\n①, ②, ③, ④ 모두 보고기업의 범위 규정에 부합하는 타당한 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "보고기업은 단일 실체나 실체 일부도 가능합니다.", "articles": [], "principle": "보고기업의 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법인격 없는 공동 사업 부문도 보고기업이 될 수 있습니다.", "articles": [], "principle": "보고기업의 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "연결실체는 법적 지위가 없으나 회계적 보고 실체로 인정됩니다.", "articles": [], "principle": "보고기업의 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경계 결정 시 이용자 수요에 맞추며 자의적 누락은 피합니다.", "articles": [], "principle": "보고기업의 범위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기업이 반드시 법적 실체여야 한다는 진술은 명백한 오류입니다.", "articles": [], "principle": "보고기업의 범위", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "연결재무제표와 비연결재무제표의 상호 지위에 대한 설명 중 개념체계에 부합하지 않는 것은?",
        "options": [
            "① 연결재무제표는 특정 종속기업의 자산, 부채 등에 대해 별도 정보를 독립적으로 제공하도록 설계되지 않았다.",
            "② 비연결재무제표는 지배기업 단독의 재무 정보를 보여준다.",
            "③ 비연결재무제표의 정보는 지배기업 주요이용자의 정보 수요를 충족하기에 불충분한 것이 일반적이다.",
            "④ 연결재무제표가 요구되는 경우에도 비연결재무제표를 작성함으로써 연결재무제표의 공시 의무를 완전히 면제받을 수 있다.",
            "⑤ 연결재무제표가 작성되더라도 지배기업은 추가적으로 비연결재무제표를 작성하도록 선택할 수 있다."
        ],
        "answer": "4",
        "explanation": "④ 개념체계에 따르면, 연결재무제표가 요구되는 경우에는 비연결재무제표가 연결재무제표를 대신할 수 없습니다.\n\n[오답 해설]\n① 연결재무제표는 특정 자회사의 단독 공시를 위해 고안된 것이 아닙니다.\n②, ③, ⑤ 모두 비연결재무제표의 한계 및 지위에 대한 올바른 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자회사 단독 정보 제공용이 아님이 올바릅니다.", "articles": [], "principle": "재무제표의 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지배기업 단독 정보 제공이 원래 목적입니다.", "articles": [], "principle": "재무제표의 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정보의 충분성이 떨어집니다.", "articles": [], "principle": "재무제표의 관계", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비연결재무제표는 연결재무제표를 대신할 수 없습니다.", "articles": [], "principle": "재무제표의 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추가 작성 선택권은 존재합니다.", "articles": [], "principle": "재무제표의 관계", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "결합재무제표(Combined Financial Statements)의 적용 조건에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 보고기업을 구성하는 실체들이 모두 지배-종속관계로 묶여 있지 않아야 결합재무제표가 될 수 있다.",
            "② 결합재무제표를 작성하는 보고기업도 법적 실체가 아닐 수 있다.",
            "③ 결합재무제표는 지배기업과 그 종속기업을 단일 보고기업으로 보는 재무제표이다.",
            "④ 지배-종속 관계 없이 공동의 지배를 받는 실체들의 재무 정보를 합산하여 작성할 수 있다.",
            "⑤ 결합재무제표도 개념체계상 하나의 재무제표 유형으로 명시되어 있다."
        ],
        "answer": "3",
        "explanation": "③ 지배기업과 종속기업으로 구성된 보고기업의 재무제표는 '연결재무제표'입니다. 지배-종속관계로 모두 연결되어 있지 않은 둘 이상 실체로 구성되었을 때 결합재무제표라고 부릅니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 모두 결합재무제표의 개념에 부합하는 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지배-종속으로만 묶여 있지 않은 경우에 적용됩니다.", "articles": [], "principle": "결합재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "결합재무제표 보고기업도 법적 실체가 아닐 수 있습니다.", "articles": [], "principle": "결합재무제표", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "지배-종속으로 구성된 재무제표는 결합재무제표가 아닌 연결재무제표입니다.", "articles": [], "principle": "결합재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공동 지배 실체 등 지배-종속 밖의 결합 작성이 가능합니다.", "articles": [], "principle": "결합재무제표", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "개념체계에 정의된 공식 분류명입니다.", "articles": [], "principle": "결합재무제표", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "개념체계상 재무제표의 보고기간 및 비교정보에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 재무제표는 특정 기간(보고기간)에 대하여 작성되는 정보이다.",
            "② 재무제표는 당기 보고기간 중 존재했던 자산과 부채뿐만 아니라 수익과 비용 정보도 당연히 제공한다.",
            "③ 비교정보의 제공은 재무제표이용자가 변화와 추세를 식별하는 것을 방해하므로 극도로 제한되어야 한다.",
            "④ 재무제표는 최소한 직전 연도에 대한 비교정보를 함께 포함하여 제공한다.",
            "⑤ 당기 보고기간 말 현재에는 소멸되었으나 보고기간 중 한때 존재했던 자산에 관한 정보도 보고기간 정보에 포함될 수 있다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계에 따르면 비교정보는 재무제표이용자가 변화와 추세를 식별하고 평가하는 것을 '돕기 위해' 최소한 직전 연도 정보를 필수로 제공하는 것입니다. 따라서 식별을 방해한다는 서술은 정반대입니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 모두 개념체계의 보고기간 및 비교정보 기준에 완벽히 부합합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재무제표는 특정 기간을 단위로 작성됩니다.", "articles": [], "principle": "보고기간 및 비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산/부채/수익/비용 정보를 포함합니다.", "articles": [], "principle": "보고기간 및 비교정보", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비교정보는 변화 추세를 식별하는 데 매우 유용한 필수 정보입니다.", "articles": [], "principle": "보고기간 및 비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "직전 연도 비교정보가 최소 조건입니다.", "articles": [], "principle": "보고기간 및 비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기간 중 존재했다가 소멸한 항목 정보도 당연히 포함됩니다.", "articles": [], "principle": "보고기간 및 비교정보", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "재무제표에 수록될 수 있는 정보 중 주석공시 및 보고기간후사건 정보에 관한 개념체계의 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 미래에 발생할 수 있는 거래/사건에 관한 미래전망 정보도 유용하다면 주석 등에 포함한다.",
            "② 미래전망 정보는 무조건 실제 수치로만 적어야 하며 불확실성을 표시해서는 안 된다.",
            "③ 보고기간 후에 발생한 거래일지라도 재무제표의 목적을 달성하기 위해 필요하다면 재무제표에 포함한다.",
            "④ 미인식 자산이나 미인식 부채에 관련되더라도 유용하다면 주석 공시 정보로 포함할 수 있다.",
            "⑤ 보고기간말 현재 실체에 존재했던 자본 요소와 연계된 정보라면 보고기간후 사건도 제공될 수 있다."
        ],
        "answer": "2",
        "explanation": "② 미래전망 정보는 본질적으로 추정과 불확실성을 내포하므로, 이를 명확히 밝히는 것이 신뢰성에 도움을 줍니다. 무조건 실제 확정 수치로만 적어야 한다는 주장은 틀렸습니다.\n\n[오답 해설]\n①, ③, ④, ⑤ 모두 개념체계 상 주석 및 보고기간후사건, 미래전망정보 수록 기준을 잘 따르고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "유용할 경우 미래전망 정보를 기재할 수 있습니다.", "articles": [], "principle": "주석 및 보고기간후사건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "미래전망 정보의 불확실성은 고지되어야지 확정 수치만을 고집하지 않습니다.", "articles": [], "principle": "주석 및 보고기간후사건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보고기간후사건도 목적상 유용하면 기재합니다.", "articles": [], "principle": "주석 및 보고기간후사건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미인식 항목 정보도 주석에 포함될 수 있습니다.", "articles": [], "principle": "주석 및 보고기간후사건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기존 요소와 연계된 사건 보고 규정은 타당합니다.", "articles": [], "principle": "주석 및 보고기간후사건", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "재무제표가 채택하는 관점(Perspective)에 관하여 개념체계가 취하고 있는 태도로 옳은 것은?",
        "options": [
            "① 지배주주가 투자 의사결정을 독점하므로 지배주주에게 유리하게만 공시해야 한다.",
            "② 금융 채권자가 최우선 주요이용자이므로 청산 가치만을 고정 관점으로 삼아 작성한다.",
            "③ 특정 집단의 관점이 아닌 보고기업 전체의 관점에서 공시하여야 균형 있고 중립적인 정보가 된다.",
            "④ 정부 공공기관의 규제 편의를 돕는 감독기구 관점을 최우선시하여 작성한다.",
            "⑤ 경영진이 성과를 과시할 수 있는 낙관적 관점을 기본적으로 채택한다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계는 재무제표 작성 시 특정 이용자 집단이 아닌 '보고기업 전체의 관점'을 가질 것을 엄격히 요구하고 있습니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 모두 특정 집단에게 유리하게 편향된 관점을 설명하고 있어 틀린 보기입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지배주주 편향 관점은 금지됩니다.", "articles": [], "principle": "채택된 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채권자 맞춤 편향 관점은 금지됩니다.", "articles": [], "principle": "채택된 관점", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "특정 집단이 아닌 보고기업 전체 관점에서 작성해야 중립성이 유지됩니다.", "articles": [], "principle": "채택된 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감독기구 편의를 우선시하지 않습니다.", "articles": [], "principle": "채택된 관점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진 성과 과시 낙관 관점을 금지합니다.", "articles": [], "principle": "채택된 관점", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "개념체계상 계속기업가정(Going Concern Assumption)이 배제되는 상황의 회계 처리에 관한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 기업이 청산을 하거나 거래를 중단하려는 의도나 필요가 있다면 계속기업 전제는 성립하지 않는다.",
            "② 계속기업 전제가 타당하지 않다면 재무제표는 계속기업과는 다른 대체적 기준(청산가치 등)에 따라 작성되어야 한다.",
            "③ 계속기업과 다른 대체적 기준으로 재무제표가 작성될 경우, 어떤 기준이 사용되었는지를 재무제표에 명확히 기술해야 한다.",
            "④ 계속기업 가정이 타당하지 않더라도 관련 주석 공시를 전혀 하지 않고 정상적인 역사적 원가로 기재하는 것이 의무이다.",
            "⑤ 경영을 영구히 유지하기 어려운 예외적 상황은 청산이나 영업 중단 필요성 등을 종합 고려하여 결정한다."
        ],
        "answer": "4",
        "explanation": "④ 계속기업 가정이 성립하지 않을 때는 역사적 원가를 그대로 유지하면 오도할 수 있으므로, 다른 대체 기준에 따라 작성하고 사용된 기준을 기술해야 합니다. 고수하는 것은 의무가 아니라 오류입니다.\n\n[오답 해설]\n①, ②, ③, ⑤ 모두 계속기업 가정 붕괴 시의 대처에 대한 바른 개념 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "청산이나 중단 의도 발생 시 가정은 깨집니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "다른 대체 기준(청산가치 등)을 적용해야 합니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사용된 대체 기준의 기술이 강제됩니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "가정이 무너졌음에도 역사적 원가 분류를 억지로 고집하는 것은 심각한 오류입니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "청산/중단 필요성은 평가 요소입니다.", "articles": [], "principle": "계속기업배제", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "K-IFRS 제1001호 '재무제표 표시' 규정 상, 계속기업가정의 평가 및 공시 요건에 대한 설명으로 가장 올바르지 않은 것은?",
        "options": [
            "① 경영진은 재무제표를 작성할 때 계속기업으로서의 존속가능성을 반드시 평가하여야 한다.",
            "② 경영진이 평가 시점에 존속가능성에 유의적 의문을 제기하는 중대한 불확실성을 알게 되었다면 그러한 불확실성을 공시해야 한다.",
            "③ 계속기업 평가 시 경영진이 고려해야 하는 미래 기간은 보고기간말로부터 적어도 12개월(1년) 이상이어야 한다.",
            "④ 재무제표가 계속기업의 기준 하에 작성되지 않는 경우에는 그 사실만 밝히면 되며, 작성된 기준이나 그 이유까지 공시할 필요는 없다.",
            "⑤ 경영활동의 중단 외에 다른 현실적 대안이 없는 상황이 아니라면 계속기업을 전제로 재무제표를 작성한다."
        ],
        "answer": "4",
        "explanation": "④ K-IFRS 제1001호에 따르면 계속기업의 기준 하에 작성되지 않는 경우, 그 사실과 함께 '재무제표가 작성된 기준' 및 '그 기업을 계속기업으로 보지 않는 이유'까지도 반드시 함께 공시하여야 합니다.\n\n[오답 해설]\n①, ②, ③, ⑤ 모두 기준서 제1001호의 명문 규정을 충실히 설명하고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "경영진의 존속가능성 평가 의무가 존재합니다.", "articles": [], "principle": "기준서 1001호 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중대한 불확실성의 공시 의무가 있습니다.", "articles": [], "principle": "기준서 1001호 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보고기간말로부터 최소 12개월의 정보 고려를 요구합니다.", "articles": [], "principle": "기준서 1001호 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비계속기업 작성 시 사실, 적용 기준, 계속기업 제외 이유의 3가지를 모두 공시해야 합니다.", "articles": [], "principle": "기준서 1001호 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현실적 대안 부재 상황이 아니면 계속기업 전제를 적용합니다.", "articles": [], "principle": "기준서 1001호 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "개념체계상 보고기업의 범위를 설정할 때, '자의적이거나 불완전한 집합을 포함하지 않는 원칙'의 취지로 가장 옳은 것은?",
        "options": [
            "① 가능한 한 법적 실체와 100% 동일하게 맞춰 회계 절차를 단순화하기 위함이다.",
            "② 주요이용자가 필요로 하는 유용한 정보를 누락시키거나 왜곡하여 정보를 오도하지 않도록 하기 위함이다.",
            "③ 지배기업의 이사회 임원들이 내부 경영 기밀을 임의로 유지하기 쉽도록 돕기 위함이다.",
            "④ 외부감사인이 감사를 빠르게 종결하여 감사 보수를 조기 회수하도록 지원하기 위함이다.",
            "⑤ 세무 당국이 기업 자산 중 일부 세목에 대해서만 편리하게 과세하도록 분리하기 위함이다."
        ],
        "answer": "2",
        "explanation": "② 보고기업의 경계(범위)를 정할 때 중요한 정보를 임의로 제외하거나 자의적으로 불완전한 조합으로 경제활동을 묶으면, 주요이용자가 잘못된 판단을 내릴 위험(정보 왜곡 및 오도)이 크므로 이를 방지하고자 하는 취지입니다.\n\n[오답 해설]\n① 법적 실체와 꼭 동일하게 맞출 필요는 없습니다.\n③, ④, ⑤ 경영진, 감사인, 세무서 등 비주요 이용자의 업무 편의를 위한 조항이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "법적 실체와의 일치가 필수 목적이 아닙니다.", "articles": [], "principle": "보고기업 경계 결정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "정보의 왜곡을 방지하고 표현충실성을 갖추기 위해 자의적 조합을 피해야 합니다.", "articles": [], "principle": "보고기업 경계 결정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진 기밀 유지와 관련 없습니다.", "articles": [], "principle": "보고기업 경계 결정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사인 일정 편의와 관련 없습니다.", "articles": [], "principle": "보고기업 경계 결정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 조사 편의와 관련 없습니다.", "articles": [], "principle": "보고기업 경계 결정", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "개념체계에 따른 재무제표 작성 기준 시점 및 보고기간에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 보고기간 중에는 존재했으나 기말 시점에 소멸한 자산은 재무제표에 표시될 여지가 전혀 없다.",
            "② 재무제표에 포함되는 자산, 부채, 자본은 오직 결산 당일(보고기간말) 현재 존재하는 항목에 대한 정보만을 반영하며, 보고기간 중의 정보는 제외된다.",
            "③ 보고기간말 현재 미인식 상태인 자산이나 부채에 관한 유용한 정보도 주석 등을 통해 재무제표에 포함될 수 있다.",
            "④ 재무제표 보고기간은 무조건 3년 단위의 다년 누적으로 공시하여야 하므로 1년 단위 공시는 금지된다.",
            "⑤ 회사는 법률적 실체가 보장되는 영업점 정보만을 의무 기재하여야 한다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계에 따르면 보고기간말 현재 또는 보고기간 중 존재했던 실체의 자산, 부채(미인식 항목 포함)나 자본은 재무제표 정보 범위에 포함되므로 미인식 항목이라도 주석 공시를 통해 포함 가능합니다.\n\n[오답 해설]\n①, ② 기중에 존재했던 자산 등의 변동(수익/비용, 처분 등) 정보도 포함됩니다.\n④ 1년(회기) 단위 보고가 일반적인 실무이며 다년 강제 규정은 없습니다.\n⑤ 법적 경계에 얽매이지 않고 회계 실체 기준으로 작성합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기중 소멸 자산도 손익 등과 연계되어 반영됩니다.", "articles": [], "principle": "보고기간 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기말 현재뿐 아니라 기중의 수익/비용 등 흐름 정보도 제공합니다.", "articles": [], "principle": "보고기간 범위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "미인식 자산이나 부채도 유용하다면 재무제표(주석) 정보에 포함됩니다.", "articles": [], "principle": "보고기간 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1년 단위 작성이 주를 이룹니다.", "articles": [], "principle": "보고기간 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법적 경계 단독 지정 규정이 아닙니다.", "articles": [], "principle": "보고기간 범위", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "연결재무제표가 보고기업 내 특정 자회사(종속기업)에 주는 재무 정보 제공의 범위 한계로 옳은 것은?",
        "options": [
            "① 연결재무제표는 특정 종속기업의 단독 정보를 주요이용자에게 별도 개별 제공하기 위해 고안된 것이 아니다.",
            "② 연결재무제표를 통해 특정 자회사만의 별도 자산 내역을 확인하는 것이 가장 완벽하고 유일한 방법이다.",
            "③ 연결재무제표는 종속기업 자체의 재무보고 의무를 법적으로 완전 면제시켜 준다.",
            "④ 지배기업은 연결재무제표만 공시하면 종속기업의 세무 자료를 제출할 필요가 전혀 없다.",
            "⑤ 연결재무제표는 종속기업 자산의 100%가 지배기업 소유임을 등기상 증명하는 서류이다."
        ],
        "answer": "1",
        "explanation": "① 연결재무제표는 지배기업과 그 종속기업을 단일 보고기업으로 보아 종합 정보를 제공할 뿐, 특정 종속기업만의 개별 별도 정보를 제공하도록 설계되지 않았습니다. 자회사 정보는 자회사 자체 재무제표가 제공합니다.\n\n[오답 해설]\n② 특정 종속기업의 세부 항목 단독 정보는 개별 재무제표를 통해야 합니다.\n③, ④ 연결재무제표 작성이 종속기업의 개별 회계 및 세무 의무를 법적으로 소멸시키지 않습니다.\n⑤ 회계 재무제표는 법적인 소유 등기 증명서가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "연결재무제표는 특정 자회사의 자산/부채 등을 별도 제공하도록 설계된 것이 아님이 맞습니다.", "articles": [], "principle": "연결재무제표의 한계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "개별 정보를 위해서는 자회사 자체 재무제표를 보아야 합니다.", "articles": [], "principle": "연결재무제표의 한계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "종속기업 법적 회계 의무 면제와 무관합니다.", "articles": [], "principle": "연결재무제표의 한계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 자료 제출 면제와 무관합니다.", "articles": [], "principle": "연결재무제표의 한계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계 보고서는 법적 소유권 등기 문서가 아닙니다.", "articles": [], "principle": "연결재무제표의 한계", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "K-IFRS 제1001호 '재무제표 표시'에서 계속기업 가정과 관련된 경영진의 공시 책무로 올바른 것은?",
        "options": [
            "① 향후 12개월간의 예상 매출 실적을 구체적으로 확약하는 보증서 제출",
            "② 계속기업의 존속가능성에 유의적 의문이 제기되는 중대한 불확실성을 알게 된 경우, 해당 불확실성의 공시",
            "③ 주가 폭락을 방지하기 위해 불확실한 재무 위험 요인을 절대 비공개하는 서약",
            "④ 계속기업 가정이 타당하지 않더라도 정상 가정인 것처럼 재무 상태를 위장하는 행위",
            "⑤ 회계법인 감사 파트너에게 경영 책임을 100% 양도하는 위임 계약서 작성"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1001호에 따르면 경영진이 존속가능성에 유의적 의문이 제기되는 중대한 불확실성을 알게 된 경우, 그러한 불확실성을 주석 등으로 명확히 공시하여야 합니다.\n\n[오답 해설]\n① 확약 보증서 제출 의무는 없습니다.\n③ 정보 은폐는 공시 규정 위반입니다.\n④ 계속기업 위장 작성은 회계 위법입니다.\n⑤ 감사인에게 책임을 양도할 수 없으며 작성 책임은 경영진에게 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "예출 보증서 제출과 무관합니다.", "articles": [], "principle": "경영진의 공시 책무", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "유의적 의문이 제기되는 불확실성을 반드시 공시하도록 규정하고 있습니다.", "articles": [], "principle": "경영진의 공시 책무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비공개 은폐 서약은 위법입니다.", "articles": [], "principle": "경영진의 공시 책무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "위장 작성은 회계 부정입니다.", "articles": [], "principle": "경영진의 공시 책무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진의 원천 책임입니다.", "articles": [], "principle": "경영진의 공시 책무", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "K-IFRS 제1001호 상, 재무제표가 계속기업의 기준 하에 작성되지 않는 경우 경영진이 필수적으로 공시하여야 하는 사항이 아닌 것은?",
        "options": [
            "① 재무제표가 계속기업 기준 하에 작성되지 않았다는 명확한 사실",
            "② 해당 재무제표가 작성된 대체 기준(예: 청산가치 기준)",
            "③ 그 기업을 계속기업으로 보지 않는 근본적인 원인이나 이유",
            "④ 기말 현재 보유 중인 모든 유형자산의 차기 양도 소득세 예상 면제액",
            "⑤ 존속 가능성 평가가 이루어진 배경 사유"
        ],
        "answer": "4",
        "explanation": "④ 계속기업 전제 상실 시 공시할 내용은 '비계속기업 사실', '재무제표 작성 기준', '계속기업으로 보지 않는 이유'이며, 유형자산의 차기 양도 소득세 예상 면제액은 필수 기재 사항이 아닙니다.\n\n[오답 해설]\n①, ②, ③, ⑤ 모두 기준서 상 비계속기업 작성 시 요구되는 투명한 공시 구성 요건에 준합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "작성되지 않은 사실 공시는 필수입니다.", "articles": [], "principle": "비계속기업 공시 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "작성된 대체 기준의 공시는 필수입니다.", "articles": [], "principle": "비계속기업 공시 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계속기업으로 보지 않는 이유의 공시는 필수입니다.", "articles": [], "principle": "비계속기업 공시 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "차기 양도 소득세 예상 면제액 등 세부 세무 희망 사항은 필수 공시가 아닙니다.", "articles": [], "principle": "비계속기업 공시 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평가 배경과 사유 기술은 정당합니다.", "articles": [], "principle": "비계속기업 공시 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "개념체계에서 재무제표의 '비교정보'가 유용한 정보 생산 측면에서 수행하는 역할로 가장 적절한 설명은?",
        "options": [
            "① 정보이용자들의 데이터 용량을 초과시켜 재무 보고서 판독 속도를 늦춘다.",
            "② 이용자가 보고기업의 기간별 성과 변화와 장기 추세를 유의미하게 식별하고 평가할 수 있게 한다.",
            "③ 경쟁기업의 과거 단가 단점을 비교 분석하여 비밀 가격 담합을 모의하게 돕는다.",
            "④ 회계장부의 오류를 감출 수 있는 복잡한 노이즈 데이터를 형성한다.",
            "⑤ 회사의 실제 현금 흐름을 축소 보고하도록 회계적 공간을 열어준다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 비교정보는 재무제표이용자가 당기 실적과의 대비를 통해 회사의 변화 및 추세를 올바르게 파악하도록 돕기 위해 최소한 직전 연도를 필수 공시하도록 규정합니다.\n\n[오답 해설]\n① 판독 지연이 목적이 아닙니다.\n③ 담합 등 불법 행위를 유도하지 않습니다.\n④ 오류 은닉 수단이 아닙니다.\n⑤ 흐름 축소 조작을 조장하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "정보 판독을 어렵게 하려는 것이 아닙니다.", "articles": [], "principle": "비교정보의 유용성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "정보이용자가 변화 추이를 합리적으로 평가하도록 기간별 비교정보를 제공합니다.", "articles": [], "principle": "비교정보의 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "담합 등 경쟁 조절과 무관합니다.", "articles": [], "principle": "비교정보의 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "오류 차폐 목적이 아닙니다.", "articles": [], "principle": "비교정보의 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계 부정 공간 확보와 무관합니다.", "articles": [], "principle": "비교정보의 유용성", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "법적 권리 주체가 아닌 사업 부문에 대하여 재무제표를 작성하고자 할 때 경계 설정 방식에 대한 설명으로 옳은 것은?",
        "options": [
            "① 법적 실체가 아니므로 개념체계상 어떠한 경계 설정 시도도 절대 불가능하다.",
            "② 해당 사업 부문 소유주 개인의 사적인 자산 채무도 결합하여 무조건 확대 경계를 설정한다.",
            "③ 경계 설정 시 주요이용자의 정보 수요에 맞춰 자의적인 누락이나 오도 없이 결정한다.",
            "④ 국가 법원 법관의 판결문을 받아서 경계를 결정하는 것만이 허용된다.",
            "⑤ 경쟁 상대 회사가 정해 주는 임의의 기준 경계를 따른다."
        ],
        "answer": "3",
        "explanation": "③ 보고기업이 법적 실체가 아닐 때 보고기업의 경계는 재무제표의 주요이용자들의 정보 수요에 맞춰 결정하며, 이때 불완전한 조합으로 정보를 오도하거나 왜곡해선 안 된다는 개념체계 기준을 준수합니다.\n\n[오답 해설]\n① 법적 실체가 아니어도 보고기업 설정이 가능합니다.\n② 사적 거래를 혼동시켜 기재하면 안 됩니다.\n④, ⑤ 사법 법원 판결이나 타사의 결정 기준을 따르는 조항이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "법적 권리 주체 여부와 관계없이 보고기업 지정이 가능합니다.", "articles": [], "principle": "비법적 실체 경계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사적 거래 결합은 오류를 낳습니다.", "articles": [], "principle": "비법적 실체 경계", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "주요이용자의 수요를 중심으로 오도하지 않도록 범위를 획정합니다.", "articles": [], "principle": "비법적 실체 경계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사법부 판결 절차가 요구되지 않습니다.", "articles": [], "principle": "비법적 실체 경계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "타사 지정을 따르는 것이 아닙니다.", "articles": [], "principle": "비법적 실체 경계", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },

    # =========================================================================
    # L3: 적용 및 시나리오 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s05-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "A사는 B사를 지배하는 모회사이다. A사는 지배-종속관계에 따른 연결재무제표 작성이 번거로워, A사 본사 단독의 재무 상태만을 나타내는 비연결재무제표만을 공식 외부 유일 공시 자료로 배포하고자 한다. 이에 대한 개념체계 상의 타당성 판단으로 가장 올바른 것은?",
        "options": [
            "① 타당하다. 비연결재무제표는 지배기업 정보를 완벽히 담으므로 연결 정보에 대체할 수 있다.",
            "② 타당하다. 회계 정보의 원가 제약을 고려할 때 지배기업의 공시 생략 권한이 보장된다.",
            "③ 타당하지 않다. 연결재무제표가 요구되는 경우 비연결재무제표가 이를 대신할 수 없다.",
            "④ 타당하다. 종속기업 B사가 상장법인이 아닌 경우에는 비연결재무제표가 연결과 똑같은 지위를 가진다.",
            "⑤ 타당하다. A사 주요 대주주 집단이 비연결 정보만을 요구하였다면 개념체계상 전면 허용된다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계에 비연결재무제표는 자원제공자(주요이용자)의 정보 수요를 충족하기에 불충분하므로, 연결재무제표가 요구되는 경우에는 비연결재무제표가 연결재무제표를 대신할 수 없음을 명시하고 있습니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 모두 연결과 비연결의 지위를 잘못 이해한 타당하지 않은 주장들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비연결재무제표는 충분한 정보를 제공하지 못하므로 대체 불가능합니다.", "articles": [], "principle": "연결대체 금지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가제약을 이유로 연결 규정을 무시할 수 없습니다.", "articles": [], "principle": "연결대체 금지", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "연결재무제표가 요구되면 비연결재무제표로 대체할 수 없다는 개념체계 요건에 따릅니다.", "articles": [], "principle": "연결대체 금지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비상장 여부와 상관없이 대체는 금지됩니다.", "articles": [], "principle": "연결대체 금지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대주주 특정 집단만의 요구로 원칙이 변경되지 않습니다.", "articles": [], "principle": "연결대체 금지", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "C사는 당기말 현재 채무 초과 상태이며, 영업 면허가 취소되어 향후 2달 이내에 법적으로 청산이 개시되는 상황이다. C사의 경영진은 자산의 급격한 감액을 피하고자 '계속기업가정'에 기초해 정상적인 역사적 원가 감가상각 방식으로 기말 재무제표를 공시하였다. 이에 대한 개념체계 상의 올바른 비판은?",
        "options": [
            "① 법적 청산 완료일 이전까지는 계속기업이 성립하므로 정상 회계처리가 맞다.",
            "② 청산이나 거래 중단 의도 또는 불가피한 필요성이 있으므로 계속기업가정을 배제하고 청산가치 등 대체 기준으로 작성하고 그 기준을 기술하여야 한다.",
            "③ 공정가치 재평가 대신에 무조건 자산 항목의 잔액을 0원으로 직접 소거하는 조치가 강제된다.",
            "④ 채권단 회의를 소집하여 계속기업가정 적용을 협의 합의하였다면 예외적으로 계속 적용이 허용된다.",
            "⑤ 회계사가 묵인해 준다면 경영진이 어떤 가정을 쓰든 외부 이해관계인은 비판할 자격이 없다."
        ],
        "answer": "2",
        "explanation": "② 기업이 청산을 하거나 영업을 중단할 수밖에 없는 현실적 대안이 없는 상황(불가피한 필요)에 해당하면 계속기업가정을 더 이상 쓸 수 없으며, 대체 기준으로 재무제표를 작성하고 관련 사항을 공시해야 합니다.\n\n[오답 해설]\n① 등기상 소멸일 전이라도 실질적 청산 상태이면 계속기업 가정이 깨집니다.\n③ 자의적으로 자산을 즉시 0원 처리하라는 규정은 없습니다.\n④, ⑤ 채권단 합의나 외부인의 묵인 여부로 회계 기준 원칙이 면제되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "청산 상태에 돌입하면 법적 존속 여부와 무관하게 계속기업은 깨집니다.", "articles": [], "principle": "계속기업 가정 상실", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "청산이 확실하다면 계속기업 전제를 배제하고 청산가치 등 대체 기준을 적용해야 합니다.", "articles": [], "principle": "계속기업 가정 상실", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "0원 소거 의무화는 틀린 조치입니다.", "articles": [], "principle": "계속기업 가정 상실", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이해관계자 합의로 회계 기준을 어길 수 없습니다.", "articles": [], "principle": "계속기업 가정 상실", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이용자의 비판과 검증 대상이 되는 회계 규정입니다.", "articles": [], "principle": "계속기업 가정 상실", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "D사와 E사는 아무런 지배-종속 관계나 법적 모자회사 연결 관계가 없다. 하지만 두 회사는 같은 대주주 그룹의 소유 하에 있어, 회계적으로 두 회사를 단일의 가상의 보고 경계로 묶어 결산 보고서를 발행하고자 한다. 이 보고서의 명칭과 개념체계상 분류로 옳은 것은?",
        "options": [
            "① 지배-종속 관계가 충족되지 않으므로 이러한 결합 보고서는 어떠한 경우에도 공시될 수 없다.",
            "② 연결재무제표이며, 지배관계가 간접 인정되므로 완벽한 정규 연결로 분류한다.",
            "③ 결합재무제표에 해당하며, 지배-종속관계로 모두 연결되어 있지 않은 둘 이상 실체로 구성된 경우의 보고이다.",
            "④ 비연결재무제표이며, 모회사가 단독 작성한 보고서로 갈음한다.",
            "⑤ 분할재무제표이며, 향후 매각을 위한 청산가치 평가 목적 문서이다."
        ],
        "answer": "3",
        "explanation": "③ 지배-종속관계로 모두 연결되어 있지는 않은 둘 이상의 실체들로 보고기업이 구성될 때, 해당 보고기업의 재무제표는 개념체계상 '결합재무제표'로 명확히 정의됩니다.\n\n[오답 해설]\n① 지배-종속이 아니어도 결합재무제표 작성이 규정상 가능합니다.\n② 지배-종속이 있어야 연결재무제표가 됩니다.\n④, ⑤ 비연결이나 분할 등의 정의 분류가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "결합재무제표 형식으로 공시가 가능합니다.", "articles": [], "principle": "결합재무제표 실무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지배종속이 없는 결합은 연결재무제표라 하지 않습니다.", "articles": [], "principle": "결합재무제표 실무", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "지배종속 외의 복수 실체들의 재무제표는 결합재무제표입니다.", "articles": [], "principle": "결합재무제표 실무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비연결재무제표가 아닙니다.", "articles": [], "principle": "결합재무제표 실무", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "분할재무제표는 관련이 없습니다.", "articles": [], "principle": "결합재무제표 실무", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "개념체계와 K-IFRS 제1001호 '재무제표 표시'의 '계속기업가정' 관련 세부 규정을 정밀 비교 분석한 내용으로 가장 옳지 않은 것은?",
        "options": [
            "① 개념체계는 계속기업을 일반적으로 보고기간말로부터 적어도 12개월의 구체적 평가 기간 요건을 명시하고 있는 반면, 제1001호 기준서에는 그러한 구체적 기간 수치 언급이 없다.",
            "② 개념체계는 일반적으로 계속기업 가정 하에 재무제표가 작성됨을 전제하고, 가정이 무너지면 다른 대체 기준의 적용과 사용된 기준의 기술을 요구한다.",
            "③ K-IFRS 제1001호 기준서는 계속기업가정 평가 시 경영진이 '적어도 보고기간말로부터 향후 12개월' 기간에 대한 정보를 고려하도록 명문 규정을 두고 있다.",
            "④ K-IFRS 제1001호 기준서는 존속가능성에 유의적 의문이 제기되는 중대한 불확실성을 알게 된 경우 이를 공시하도록 의무화하고 있다.",
            "⑤ 두 기준 모두 경영진에게 계속기업 여부를 평가할 책임을 원천적으로 부과하거나 전제하고 있다."
        ],
        "answer": "1",
        "explanation": "① 설명이 정반대입니다. 계속기업 평가 시 '적어도 보고기간말로부터 향후 12개월'이라는 구체적 평가 기간 요건을 명시한 규정은 K-IFRS 제1001호(기준서)에 수록되어 있으며, 오히려 개념체계에는 이러한 12개월이라는 명시적 숫자의 제한이 없이 '예측가능한 미래'로 정성적 기술을 하고 있습니다.\n\n[오답 해설]\n②, ③, ④, ⑤ 모두 개념체계와 기준서 제1001호의 차이점 및 일치점을 정확히 짚어낸 진술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "12개월 요건은 개념체계가 아니라 K-IFRS 제1001호 기준서에 있습니다.", "articles": [], "principle": "개념체계와 기준서 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "개념체계는 다른 기준 적용 시 기술 요구가 맞습니다.", "articles": [], "principle": "개념체계와 기준서 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "제1001호 기준서의 적어도 12개월 평가는 사실입니다.", "articles": [], "principle": "개념체계와 기준서 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중대한 불확실성 공시 규정은 사실입니다.", "articles": [], "principle": "개념체계와 기준서 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경영진의 평가 책임 전제는 양자 공통 사항입니다.", "articles": [], "principle": "개념체계와 기준서 비교", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "F사의 대주주는 당기 결산에서 자신들의 주당 가치를 극대화할 수 있도록 재무제표 표시 항목을 특정 자본 항목 위주로 재구성하라고 회계담당자에게 요구하였다. 회계담당자가 이 요구를 거절하며 제시할 수 있는 개념체계 상의 가장 합리적인 근거는?",
        "options": [
            "① 재무제표는 특정 이용자 집단이 아닌 보고기업 전체의 관점에서 거래 정보를 중립적으로 제공해야 하기 때문이다.",
            "② 대주주가 요구하는 정보는 세무조사 면제 대상에서 제외되어 회사가 즉각 처벌받기 때문이다.",
            "③ 자본 총장부액은 언제나 시가총액과 일치하므로 표시를 바꿀 공간이 없기 때문이다.",
            "④ 주석공시는 미래전망 정보를 기재할 수 없도록 강제하고 있기 때문이다.",
            "⑤ 회사는 반드시 3개년 평균 실적만으로 비교정보를 작성해야 하기 때문이다."
        ],
        "answer": "1",
        "explanation": "① 개념체계상 재무제표에 채택된 관점은 특정 주주나 채권자 집단 등의 편향된 관점이 아닌 '보고기업 전체의 관점'에서 중립적으로 정보를 제공하는 것입니다. 따라서 대주주 요구에 맞춘 특정 편향 작성을 거부해야 합니다.\n\n[오답 해설]\n② 세무조사 처벌 사유가 근본적인 개념체계 근거는 아닙니다.\n③ 자본 장부금액과 시가총액은 일반적으로 일치하지 않습니다.\n④ 유용할 경우 미래전망 정보를 주석에 기재할 수 있습니다.\n⑤ 비교정보의 최소 요구 사항은 3개년 평균이 아닌 직전 연도(1년)입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "재무제표는 보고기업 전체의 관점에서 기술되어야 중립성이 유지됩니다.", "articles": [], "principle": "채택된 관점 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 과세 처벌이 개념체계의 거절 근거는 아닙니다.", "articles": [], "principle": "채택된 관점 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 장부액과 시가총액은 개념체계상 일치하지 않는 것이 정상입니다.", "articles": [], "principle": "채택된 관점 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래전망 정보의 주석 기재는 허용됩니다.", "articles": [], "principle": "채택된 관점 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "직전 연도 비교공시가 최소 조건입니다.", "articles": [], "principle": "채택된 관점 적용", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "G사는 2025년 12월 31일을 보고기간말로 설정하였다. 2026년 2월 10일 재무제표 최종 승인 보고 전에 기말 현재 보유하던 핵심 생산 기지가 화재로 소실되는 사고가 발생했다. 이 보고기간후사건에 대해 G사가 개념체계 목적에 맞게 취해야 할 가장 타당한 조치는?",
        "options": [
            "① 2025년 12월 31일 현재에는 화재가 안 났으므로 주석과 본문 모두에 기재하지 않고 은폐한다.",
            "② 재무제표의 목적을 달성하기 위해 보고기간 후 발생한 사고 정보를 재무제표(주석 등)에 유용한 정보로서 포함하여 제공한다.",
            "③ 2025년 12월 31일자의 기말 공장을 즉시 0원으로 소급 장부 삭제 처리한다.",
            "④ 기말 결산 보고서를 작성 거부하고 즉시 법원에 파산 신청서를 단독 공시한다.",
            "⑤ 화재 피해 보상 예상 이익을 당기 손익계산서 상 매출액으로 계상한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 따르면 재무제표의 목적을 달성하기 위해 보고기간 후 발생한 사건에 대한 정보를 제공할 필요가 있다면, 재무제표에 그러한 정보(보고기간후사건 정보)를 포함해야 합니다. 공장 화재 소실은 주석 등으로 공시되어야 할 유의적 사건입니다.\n\n[오답 해설]\n① 중요 사건을 기재하지 않고 은폐하는 것은 표현충실성 위배입니다.\n③ 기말 시점에는 실제 공장이 있었으므로 소급 삭제는 분식입니다.\n④ 작성 거부는 회계 기준 위반입니다.\n⑤ 실현되지 않은 불확실한 피해 보상 이익을 마음대로 매출 계상할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "보고기간후사건이라도 중요한 정보는 은폐해선 안 됩니다.", "articles": [], "principle": "보고기간후사건 처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재무제표 목적 달성을 위해 보고기간 후 발생한 화재 사실 등을 공시 정보에 포함하여야 합니다.", "articles": [], "principle": "보고기간후사건 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기말 당시 존재했던 자산을 소급하여 0원으로 삭제하는 것은 왜곡입니다.", "articles": [], "principle": "보고기간후사건 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보고서 작성 거부는 불가능합니다.", "articles": [], "principle": "보고기간후사건 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 매출 계상은 회계 오류입니다.", "articles": [], "principle": "보고기간후사건 처리", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "H사는 당기 중 진행하던 미완성 신규 바이오 특허 기술개발(아직 무형자산 인식 조건을 충족하지 못해 비용 처리됨)에 대한 미래 상용화 성공 시 예상 유입 현금 정보를 주석에 '미래전망 정보'로 기재하려 한다. 이에 대한 개념체계상의 타당성 검토로 옳은 것은?",
        "options": [
            "① 부당하다. 무형자산으로 장부에 인식되지 않은 항목은 어떠한 정보도 재무제표와 주석에 적을 수 없다.",
            "② 타당하다. 정보가 보고기간말 현재 또는 기중에 존재했던 실체의 자산, 부채 등과 관련되며 이용자에게 유용하다면 미래전망 정보도 주석에 포함할 수 있다.",
            "③ 부당하다. 미래전망 정보는 무조건 당기 포괄손익계산서 본문 손익 항목에 수치 반영해야 한다.",
            "④ 타당하다. 미래전망 정보는 경영진이 자의적으로 임의 낙관 시나리오를 구성할 권한을 전면 보장한다.",
            "⑤ 부당하다. 개념체계는 미래에 발생할 수 있는 거래 정보의 주석 공시를 원천 금지한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 따르면 미래전망 정보는 보고기간말 현재 또는 기중에 존재했던 실체의 자산, 부채(미인식 자산/부채 포함) 등과 관련되며 이용자에게 유용하다면 재무제표에 포함합니다. 연구 비용으로 당기 인식되지 못한 특허 원천 기술이라도 기말 현재 존재하는 미래전망 연관 요소이므로 공시 가능합니다.\n\n[오답 해설]\n① 미인식 자산 항목도 주석 정보에 포함될 수 있습니다.\n③ 손익 본문에 미실현 미래 예상치를 직접 계상할 수는 없습니다.\n④ 자의적이고 오도하는 서술은 금지됩니다.\n⑤ 미래 정보의 주석 공시를 원천 금지하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "미인식 자산 부채 관련 정보도 유용하면 포함 가능합니다.", "articles": [], "principle": "미래전망 정보 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기말 현재 실체 요건(미인식 포함)과 관련되고 유용하다면 미래전망 정보를 재무제표에 포함합니다.", "articles": [], "principle": "미래전망 정보 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "본문 손익 항목에 직접 계상해서는 안 됩니다.", "articles": [], "principle": "미래전망 정보 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적 낙관 왜곡 정보를 허용한다는 뜻은 아닙니다.", "articles": [], "principle": "미래전망 정보 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석 공시 자체를 금지하지 않습니다.", "articles": [], "principle": "미래전망 정보 적용", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "I 공익재단은 등기소에 독립 법인으로 등록되지 않은 부속 복지관 사업 부문을 별도로 분리하여 독립된 재무제표를 발행하려 한다. 법적 실체가 아니며 다른 법적 모자회사 연결 관계도 아닌 상황에서, 보고기업의 경계를 확정하고자 할 때 회계담당자가 따라야 할 가장 올바른 개념체계 기준은?",
        "options": [
            "① 법적 실체가 성립하지 않으므로 경계 설정을 무기한 연기하고 재무제표를 만들지 않는다.",
            "② 주요이용자들의 정보 수요에 맞춰 경계를 결정하되, 중요한 정보의 누락이 없도록 자의적 설정을 피한다.",
            "③ 공익재단 이사장의 사적 부동산 소유 지분을 재무제표 자산에 모두 합산하여 경계를 획정한다.",
            "④ 복지관 이용자 중 무작위 100인을 선발하여 이들이 작성한 기준대로 경계를 설정한다.",
            "⑤ 경쟁 상대 복지재단의 재무제표와 똑같은 금액 수치로 경계를 가공 기재한다."
        ],
        "answer": "2",
        "explanation": "② 보고기업이 법적 실체가 아니고 지배-종속으로만 연결되지 않았을 때 보고기업의 적절한 경계를 결정하는 것은 어렵습니다. 이 경우 주요이용자의 정보 수요에 맞추어, 중요한 정보를 누락하거나 오도하지 않는 객관적 경계를 설정합니다.\n\n[오답 해설]\n① 법인격이 없어도 보고기업을 설정해 재무제표를 만들 수 있습니다.\n③ 이사장 개인 지분을 혼동 결합하면 안 됩니다.\n④, ⑤ 무작위 이용자 설문이나 타사 위조 복제를 규정하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "법적 실체가 아니어도 보고기업 설정이 가능하므로 연기 사유가 아닙니다.", "articles": [], "principle": "경계 결정 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이용자의 정보 수요를 파악하고 자의적 세부 정보를 누락하지 않도록 경계를 결정하여야 합니다.", "articles": [], "principle": "경계 결정 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이사장 개인 자산을 묶는 행위는 오류입니다.", "articles": [], "principle": "경계 결정 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무작위 설문 방식으로 경계를 획정하지 않습니다.", "articles": [], "principle": "경계 결정 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "타사 위조 모방 기재와 무관합니다.", "articles": [], "principle": "경계 결정 적용", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "J사는 자금 사정의 악화로 공장 폐쇄가 결정되었으며, 청산인을 선임하고 청산 절차를 밟기 위한 다른 대체 기준(청산가치 기준)으로 재무제표를 작성하였다. 이때 개념체계와 관련 규정이 요구하는 기재 방법으로 가장 올바른 것은?",
        "options": [
            "① 대체 기준을 썼더라도 표면상에는 계속기업 원칙에 따라 작성된 것처럼 표시를 유지해야 한다.",
            "② 사용된 대체적 측정 기준(예: 청산가치 등)을 재무제표(주석 포함)에 상세히 기술하여 공시하여야 한다.",
            "③ 어떤 대체 기준을 썼는지는 영업 비밀이므로 재무보고서에 절대 명시해서는 안 된다.",
            "④ 정상적인 계속기업가정이 유지되고 있다는 허위의 감사보고서를 동봉해야 한다.",
            "⑤ 주주들의 동의를 받아서 자산을 전부 기부한 것으로 가짜 기재한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계에 따르면 기업이 청산을 하거나 거래를 중단하려는 의도나 필요가 있어 계속기업이 아닌 다른 기준을 사용한 경우, 사용된 기준을 재무제표에 기술하여야 합니다.\n\n[오답 해설]\n①, ③, ④, ⑤ 허위 기재나 영업비밀 은폐 등은 회계 부정이며, 투명하게 사용된 기준을 공시하는 것이 대원칙입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "계속기업인 것처럼 허위 표시해서는 안 됩니다.", "articles": [], "principle": "대체 기준 명시", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사용된 대체 측정 기준을 재무제표에 성실하게 서술하고 기술하여야 합니다.", "articles": [], "principle": "대체 기준 명시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계 기준의 명시는 비밀 사항이 아닙니다.", "articles": [], "principle": "대체 기준 명시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "허위 감사보고서 동봉은 불법입니다.", "articles": [], "principle": "대체 기준 명시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가짜 기재는 분식회계입니다.", "articles": [], "principle": "대체 기준 명시", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "K사는 지난 3년 동안 매년 결산 시 감가상각 방법을 합리적인 이유나 추정의 변경 없이 임의로 정액법, 정률법, 이중체감법으로 번갈아가며 적용하여 비교정보를 제공했다. 이에 대해 개념체계 상의 비교정보 및 일관성 관점에서 내릴 수 있는 비판으로 옳은 것은?",
        "options": [
            "① 훌륭한 회계 실무이다. 매년 다른 방법을 쓰면 다양한 회계 정보를 줄 수 있다.",
            "② 이용자들이 변화와 추세를 일관된 기준으로 식별하고 평가하는 것을 심각하게 방해하여 유용성을 저해하였다.",
            "③ 비교정보는 직전 연도 1회만 제공되므로 3개년 동안 변경 적용한 것은 오류가 될 수 없다.",
            "④ 감가상각 방법 변경은 계속기업가정과 무관하므로 아무런 문제가 없다.",
            "⑤ 주총에서 대주주가 승인한 경우이므로 일관성 위배 비판의 대상이 될 수 없다."
        ],
        "answer": "2",
        "explanation": "② 비교정보를 제공하는 본래의 목적은 이용자들이 기간별 변화와 성과 추세를 올바르게 식별하고 평가하도록 돕는 것입니다. 매년 합리적 이유 없이 측정 방법을 임의 변경하여 기재하는 것은 비교가능성의 근간인 일관성을 훼손하여 보고서 유용성을 저해하는 대표적 위반 사례입니다.\n\n[오답 해설]\n① 임의 변경은 정보의 비교가능성을 떨어뜨립니다.\n③ 매년의 일관성은 비교 정보 제공의 핵심 원리입니다.\n④ 계속기업 하에 감가상각 일관성 유지는 밀접한 연계성을 가집니다.\n⑤ 주총 승인 여부가 개념체계의 비판 회피 요건이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "임의 방식 변경은 유용하지 않습니다.", "articles": [], "principle": "일관성과 비교정보", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "정당한 사유 없는 일관성 상실은 변화와 추세 식별 목적을 저해하여 타당하지 않습니다.", "articles": [], "principle": "일관성과 비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "3개년도에 걸친 다년 일관성도 필수적인 비교가치입니다.", "articles": [], "principle": "일관성과 비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계속기업 전제 하의 감가상각 일관성은 핵심 가정입니다.", "articles": [], "principle": "일관성과 비교정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "개념체계 위배 비판은 주총 승인과 별개입니다.", "articles": [], "principle": "일관성과 비교정보", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "K-IFRS 제1001호에 따라 경영진이 계속기업가정의 적절성을 평가할 때 고려해야 하는 정보의 성격으로 가장 옳지 않은 것은?",
        "options": [
            "① 향후 예측되는 이자율 변동, 차입금의 만기 구조 및 추가 조달 대안 정보",
            "② 보고기간말로부터 적어도 12개월 이상의 미래 영업 지속 가능 정보",
            "③ 오직 직전 연도에 확정된 세무서 신고 완료 소득세 결정세액 수치 단 한 가지만을 고려",
            "④ 유의적인 불확실성이 발견된 경우 주석에 어떻게 투명하게 공시할 것인지에 대한 계획 정보",
            "⑤ 회사의 미래 수익성에 심대한 타격을 줄 수 있는 보고기간 후 소송 제기 사건"
        ],
        "answer": "3",
        "explanation": "③ 계속기업가정 평가 시 경영진은 이용가능한 모든 미래 정보를 종합 고려하여 존속여부를 판단해야 하므로, 단 하나의 세액 수치만을 절대 기준으로 삼는 것은 타당하지 않습니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 모두 경영진이 평가 시 직간접적으로 반드시 검토하고 반영해야 하는 다각적 정보 유형에 해당합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "차입 구조 및 상환 여력은 핵심 고려 사항입니다.", "articles": [], "principle": "평가 시 고려 정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "최소 12개월의 영업 지속성 검토는 필수입니다.", "articles": [], "principle": "평가 시 고려 정보", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "과거 세액 수치 단 하나만을 고집해 미래 생존을 평가하는 것은 절대 불충분합니다.", "articles": [], "principle": "평가 시 고려 정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "불확실성 발견 시 공시 계획 수립은 타당합니다.", "articles": [], "principle": "평가 시 고려 정보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보고기간후 유의적 소송은 존속을 위협하므로 당연히 고려됩니다.", "articles": [], "principle": "평가 시 고려 정보", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "L사는 해외 채권자 은행들로부터 자금 대출 연장 심사를 받고 있다. L사의 최고재무책임자(CFO)는 채권단의 비위를 맞추기 위해 L사의 부채 규모를 임의로 크게 부풀려 안전 마진을 과장하여 표현하는 보수적 방식을 적용하자고 제안했다. 재무제표가 채택해야 하는 관점(Perspective)에 비추어 이 제안의 문제점으로 가장 타당한 설명은?",
        "options": [
            "① 문제가 없다. 채권자 비위를 맞추는 정보가 가장 유용한 정보이다.",
            "② 문제가 있다. 재무제표는 특정 집단(채권자 등)의 편향된 관점이 아닌, 보고기업 전체의 관점에서 중립적으로 작성되어야 하기 때문이다.",
            "③ 문제가 없다. 부채를 과대 계상하는 것은 개념체계상 예측 가치를 극대화한다.",
            "④ 문제가 있다. 채무 상환을 거부할 경우 형사 처벌 조항이 개념체계에 명시되어 있기 때문이다.",
            "⑤ 문제가 없다. 해외 채권자 관점을 수용하면 외화 조달이 용이해지므로 허용된다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 특정 이해관계자(대주주, 채권자 등)만의 편향된 요구 관점이 아닌 '보고기업 전체의 관점'에서 중립적이고 사실적인 정보 보고를 요구하고 있습니다.\n\n[오답 해설]\n①, ⑤ 특정 채권자 편향은 회계의 중립성을 저해합니다.\n③ 부채 과대 계상이 예측 가치를 유의미하게 향상하지 않으며 표현충실성을 위배합니다.\n④ 형사 처벌 등의 조항은 개념체계가 관장하는 분야가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "채권자 편향 정보는 중립성을 훼손합니다.", "articles": [], "principle": "전체 관점 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "특정 채권자 은행의 입맛에 맞춰 왜곡 작성하는 것은 보고기업 전체 관점 원칙과 중립성에 위배됩니다.", "articles": [], "principle": "전체 관점 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 과대 조작은 표현충실성 훼손 행위입니다.", "articles": [], "principle": "전체 관점 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사법적 형벌 규정은 개념체계에 수록되지 않습니다.", "articles": [], "principle": "전체 관점 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "외자 유치 편의 목적으로 원칙을 훼손할 수 없습니다.", "articles": [], "principle": "전체 관점 적용", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "보고기업 경계 결정에서 '자의적이거나 불완전한 경제활동 집합'을 의도적으로 구성하는 것을 배제해야 하는 회계학적 논리로 가장 타당한 설명은?",
        "options": [
            "① 자의적 경계를 허용하면 법인세 징수량이 급감해 국가 재정에 해를 입히기 때문이다.",
            "② 주요이용자가 보고기업에 대한 정확한 판단을 내리기 위해 필수적인 중요 정보를 은폐하거나 누락시켜 재무보고서를 왜곡하는 오도(Misleading) 행위를 막기 위함이다.",
            "③ 대주주가 본인의 소득세를 대리 신고하여 세제 부담을 줄이기 쉽도록 만들기 위함이다.",
            "④ 외부감사인이 회계법인 내부 결재 절차를 건너뛰고 간략한 도장 날인만 수행하게 유도하기 위함이다.",
            "⑤ 회사의 주가 하락 시 감옥에 수감되는 법적 근거가 자의적 경계 조항에서 파생되기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 보고기업 경계를 자의적으로 결정하여 일부 종속 실체나 사업 부문의 불리한 거래를 의도적으로 숨기면(불완전한 집합 구성), 재무제표이용자는 심각하게 왜곡된 의사결정을 내릴 수 있습니다. 이를 막아 표현충실성과 중립성을 지키기 위해 자의적 획정을 배제합니다.\n\n[오답 해설]\n①, ③, ④, ⑤ 모두 개념체계가 도모하는 재무보고의 질적 유용성 확보 목적과 관련 없는 비본질적인 오답 진술들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "세제 세무 징수 목적이 개념체계의 목적은 아닙니다.", "articles": [], "principle": "자의적 경계 배제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자의적 경계 획정은 정보를 의도적으로 누락하여 왜곡하는 행위가 되어 표현충실성을 심각하게 해칩니다.", "articles": [], "principle": "자의적 경계 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대주주 소득세 징수 관련 조항이 아닙니다.", "articles": [], "principle": "자의적 경계 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사인 행정 간소화 조항이 아닙니다.", "articles": [], "principle": "자의적 경계 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사법적 수감 등 형사법 규정이 아닙니다.", "articles": [], "principle": "자의적 경계 배제", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "K-IFRS 제1001호 '재무제표 표시' 규정에 따를 때, 계속기업으로 가동 가능하나 자금 유동성이 일시 부족해 만기 도래 사채 상환 여부에 '중대한 불확실성'이 발생한 경우 경영진의 올바른 대처 방식은?",
        "options": [
            "① 은행권 만기 연장이 백프로 확정될 때까지는 어떠한 불확실성 정보도 재무제표에 공개해서는 안 된다.",
            "② 해당 불확실성이 존재한다는 사실 및 회사의 대응 계획 등을 재무제표(주석)에 상세히 투명하게 공시하여야 한다.",
            "③ 사채 만기가 돌아오는 기일 즉시 재무제표 작성을 거부하고 결산을 중단한다.",
            "④ 부채 항목을 자본 항목으로 강제 대체하여 부채비율을 인위적으로 낮춘다.",
            "⑤ 회사의 모든 자산 계정을 무조건 공정가치 감액 처리하여 조기 청산 상태로 등기 신고한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1001호 상 경영진은 계속기업 가정이 유지되더라도 존속성에 유의적 의문이 제기되는 중대한 불확실성을 알게 된 경우, 해당 불확실성을 명확하게 주석 공시하여 정보이용자가 미래 위험을 인지하도록 해야 합니다.\n\n[오답 해설]\n① 정보의 비공개 은폐는 규정 위반입니다.\n③ 결산 작성을 무단 거부할 수 없습니다.\n④ 자의적이고 허위의 대체 분식은 엄벌 대상입니다.\n⑤ 일시적 유동성 위험만으로 다짜고짜 조기 청산 가치를 강제 적용하지는 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "불확실성의 은폐는 기준 위반입니다.", "articles": [], "principle": "불확실성 공시", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "계속기업 가정 존속에 의문이 생기는 유의적 불확실성은 투명하게 주석 등으로 밝혀야 합니다.", "articles": [], "principle": "불확실성 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "결산 무단 중단은 위법입니다.", "articles": [], "principle": "불확실성 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인위적 자본 대체는 중대 분식입니다.", "articles": [], "principle": "불확실성 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조기 청산가치 의무화 대상이 아닙니다.", "articles": [], "principle": "불확실성 공시", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "계속기업가정이 정상 유효하게 작동할 때, 자산과 부채를 '유동'과 '비유동'으로 합리적으로 분류하는 실무적 의의와 가장 연계성이 깊은 회계 논리는?",
        "options": [
            "① 계속기업가정이 깨지면 모든 자산이 즉시 유동화(처분)되어야 하므로 유동/비유동 구분 분류는 의미를 상실하고 오직 즉시 청산 처분가치만 중요해지기 때문이다.",
            "② 유동과 비유동 분류는 오직 세법의 양도세율 구분 목적을 돕기 위해 만든 편의 규칙이기 때문이다.",
            "③ 계속기업가정은 무조건 모든 자산을 비유동자산으로만 표시할 것을 엄격히 강제하기 때문이다.",
            "④ 비유동부채는 정부 보증 없이는 발행할 수 없으므로 계속기업 원리와 상관없기 때문이다.",
            "⑤ 유동자산만을 많이 보유한 기업은 절대 망하지 않음을 계속기업 원리가 보장해주기 때문이다."
        ],
        "answer": "1",
        "explanation": "① 정상 영업 지속을 전제(계속기업가정)하므로, 자산과 부채를 장기(비유동)와 단기(유동)로 나누어 상환 구조 및 유동성을 정보이용자가 분석하도록 유용하게 분류 제공하는 것입니다. 청산 예정 기업은 이 분류를 할 이유가 없이 청산가치 단일 기준으로 전환합니다.\n\n[오답 해설]\n② 세법 목적 분류가 회계학적 대원칙의 기초는 아닙니다.\n③ 비유동 분류만을 강제하지 않습니다.\n④ 부채 발행 보증과 무관합니다.\n⑤ 망하지 않음을 보증하는 법적 장치가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "계속기업가정이 있으므로 유동/비유동의 구분 표시가 분석상 의미를 갖게 되며, 청산 시에는 이 구분이 불필요해집니다.", "articles": [], "principle": "분류와 가정의 연계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 편의가 근본 기초가 아닙니다.", "articles": [], "principle": "분류와 가정의 연계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비유동 표시만을 강제하지 않습니다.", "articles": [], "principle": "분류와 가정의 연계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정부 보증 관련 설문은 무관합니다.", "articles": [], "principle": "분류와 가정의 연계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회사의 생존을 회계 원칙이 보장하지는 않습니다.", "articles": [], "principle": "분류와 가정의 연계", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },

    # =========================================================================
    # L4: 다중 분석 및 조합 (8문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s05-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "다음 중 개념체계 상 '보고기업 및 재무제표 종류'에 관한 설명으로 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 보고기업은 단일 실체일 수도 있고 실체의 일부일 수도 있으며, 둘 이상의 실체로 구성될 수도 있다.\nㄴ. 보고기업이 반드시 법적 실체여야 하는 것은 아니다.\nㄷ. 연결재무제표가 요구되는 경우에도 비연결재무제표가 연결재무제표를 대신할 수 있다.\nㄹ. 지배-종속관계로 모두 연결되어 있지 않은 둘 이상 실체들로 보고기업이 구성된다면 그 보고기업의 재무제표를 '결합재무제표'라 부른다.",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ ㄱ, ㄴ, ㄹ 지문은 모두 개념체계 규정에 부합하는 옳은 설명입니다. ㄷ 지문은 연결재무제표가 요구될 때 비연결재무제표가 이를 대신할 수 없으므로 틀렸습니다.\n\n[오답 해설]\nㄷ. 비연결재무제표는 연결재무제표를 대체하지 못하므로 ㄷ이 포함된 보기 ①, ②, ④, ⑤는 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄹ 지문이 누락되어 불완전합니다.", "articles": [], "principle": "보고기업 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 거짓이며 ㄹ이 누락되었습니다.", "articles": [], "principle": "보고기업 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ, ㄴ, ㄹ이 모두 옳은 지문으로 구성되었습니다.", "articles": [], "principle": "보고기업 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 거짓이고 ㄱ이 누락되었습니다.", "articles": [], "principle": "보고기업 다중 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ이 포함되어 틀린 보기입니다.", "articles": [], "principle": "보고기업 다중 판단", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "다음 중 개념체계 및 관련 규정 상 '계속기업가정, 보고기간, 미래전망정보'에 관한 설명으로 옳지 않은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 재무제표는 이용자가 변화와 추세를 식별할 수 있도록 최소한 직전 연도에 대한 비교정보를 제공한다.\nㄴ. 미래에 발생할 수 있는 거래/사건에 대한 정보(미래전망 정보)는 어떠한 경우에도 재무제표에 기재할 수 없도록 엄격히 금지된다.\nㄷ. 계속기업 가정이 무너진 청산 상태의 재무제표는 계속기업과는 다른 기준에 따라 작성되어야 하며, 사용된 기준을 밝혀야 한다.\nㄹ. 재무제표는 특정 주주나 채권자 집단 중 특정 다수 자원제공자 집단만의 편향된 관점에서 작성되어야 한다.",
        "options": [
            "① ㄱ, ㄷ",
            "② ㄴ, ㄹ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 옳지 않은 지문은 ㄴ과 ㄹ입니다.\nㄴ. 미래전망 정보도 보고기간말 현재 요소와 연계되고 유용하다면 주석에 포함할 수 있으므로 금지된다는 서술은 틀렸습니다.\nㄹ. 특정 집단의 관점이 아닌 '보고기업 전체의 관점'을 채택해야 하므로 틀렸습니다.\nㄱ, ㄷ 지문은 옳은 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ, ㄷ은 옳은 지문입니다.", "articles": [], "principle": "개념체계 다중 정오", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "틀린 지문인 ㄴ과 ㄹ만으로 올바르게 구성되었습니다.", "articles": [], "principle": "개념체계 다중 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ은 옳은 지문입니다.", "articles": [], "principle": "개념체계 다중 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 옳은 지문입니다.", "articles": [], "principle": "개념체계 다중 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ, ㄷ이 포함되어 오답입니다.", "articles": [], "principle": "개념체계 다중 정오", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "K-IFRS 제1001호 '재무제표 표시'의 계속기업가정 관련 다음 보기 중 옳은 지문의 개수는?\n\n[보기]\n- 경영진은 재무제표를 작성할 때 계속기업으로서의 존속가능성을 평가해야 한다.\n- 존속가능성 평가 시 경영진은 적어도 보고기간말로부터 향후 12개월(1년) 기간에 대하여 이용가능한 모든 정보를 고려하여야 한다.\n- 존속가능성에 유의적 의문이 제기되는 중대한 불확실성을 알게 된 경우, 그러한 불확실성을 재무제표에 공시할 필요 없이 이사회 내부 보고만으로 족하다.\n- 재무제표가 계속기업의 기준 하에 작성되지 않는 경우에는 그 사실과 함께 재무제표가 작성된 기준 및 그 기업을 계속기업으로 보지 않는 이유를 공시하여야 한다.",
        "options": [
            "① 0개",
            "**② 1개** (오타 방지용 가이드)", 
            "③ 2개",
            "④ 3개",
            "⑤ 4개"
        ],
        "answer": "4",
        "explanation": "④ 세 개의 옳은 지문과 한 개의 틀린 지문이 있어 총 3개가 맞습니다. \n- 첫 번째, 두 번째, 네 번째 지문은 옳습니다.\n- 세 번째 지문은 중대한 불확실성을 알게 된 경우 내부 보고에 그치지 않고 외부 재무제표에 반드시 공시하여야 하므로 틀렸습니다.\n\n[오타 정정 및 번호 해설]\n선택지 번호 중 ④번이 정답(3개)입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "옳은 지문이 존재하므로 0개가 아닙니다.", "articles": [], "principle": "지문 개수 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1개가 아닙니다.", "articles": [], "principle": "지문 개수 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "2개가 아닙니다.", "articles": [], "principle": "지문 개수 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "첫 번째, 두 번째, 네 번째 지문 등 총 3개가 옳은 지문입니다.", "articles": [], "principle": "지문 개수 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세 번째 지문은 거짓이므로 4개가 될 수 없습니다.", "articles": [], "articles": [], "principle": "지문 개수 계산", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "개념체계 상 '보고기업의 경계 및 범위 획정'에 관한 설명 중 옳은 지문의 개수는?\n\n[보기]\n- 보고기업이 법적 실체가 아니고 지배-종속관계로만 연결되지 않았을 때 보고기업의 적절한 경계를 결정하는 것이 어려울 수 있다.\n- 보고기업의 적절한 경계를 결정하기 어려운 경우에는 재무제표 주요이용자들의 정보 수요를 무시하고 법률가들의 합의를 우선적으로 따른다.\n- 보고기업의 경계는 주요이용자들의 정보 수요에 맞춰 결정하며, 임의로 중요한 정보를 누락시키거나 왜곡하여 정보를 오도하지 않아야 한다.\n- 보고기업의 경계를 결정할 때에는 항상 동일 업종 경쟁사의 법적 범위와 일치하도록 맞춰야 한다.",
        "options": [
            "① 0개",
            "② 1개",
            "③ 2개",
            "④ 3개",
            "⑤ 4개"
        ],
        "answer": "3",
        "explanation": "③ 두 개의 옳은 지문이 존재합니다.\n- 첫 번째, 세 번째 지문은 옳습니다.\n- 두 번째 지문은 법률가의 합의가 아닌 주요이용자의 정보 수요에 맞추므로 틀렸습니다.\n- 네 번째 지문은 경쟁사의 법적 범위와 일치시킬 하등의 이유가 없으므로 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "옳은 지문이 존재합니다.", "articles": [], "principle": "경계 획정 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1개가 아닙니다.", "articles": [], "principle": "경계 획정 개수", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "첫 번째, 세 번째 지문 총 2개가 정당합니다.", "articles": [], "principle": "경계 획정 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "3개가 아닙니다.", "articles": [], "principle": "경계 획정 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "4개가 아닙니다.", "articles": [], "principle": "경계 획정 개수", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "개념체계 상 '재무제표의 채택 관점 및 보고기간후사건, 주석 미래전망'에 관한 지문 중 옳지 않은 것의 개수는?\n\n[보기]\n- 재무제표는 특정 주주 집단이나 특정 금융 대여자의 개별 관점에서 작성되어야 한다.\n- 보고기간 후에 발생한 거래일지라도 재무제표의 목적을 달성하기 위해 필요하다면 재무제표에 그러한 정보를 포함한다.\n- 기말 현재 존재했던 미인식 자산 부채 항목에 대한 정보는 미래전망 정보를 포함한 주석 기재 대상에서 절대 제외하여야 한다.\n- 비교정보는 정보이용자의 주관적 왜곡을 줄이기 위해 직전 10년간의 변동 평균치만을 공시하도록 한다.",
        "options": [
            "① 0개",
            "② 1개",
            "③ 2개",
            "④ 3개",
            "⑤ 4개"
        ],
        "answer": "4",
        "explanation": "④ 옳지 않은 지문은 총 3개입니다.\n- 첫 번째 지문은 특정 집단이 아닌 '보고기업 전체의 관점'이어야 하므로 틀렸습니다.\n- 세 번째 지문은 미인식 자산 부채 관련 정보도 유용하면 미래전망 정보에 포함할 수 있으므로 틀렸습니다.\n- 네 번째 지문은 비교정보의 최소 요구 기준이 '직전 연도'이므로 틀렸습니다.\n- 두 번째 지문 하나만 옳습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "옳지 않은 지문이 존재합니다.", "articles": [], "principle": "오답 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1개가 아닙니다.", "articles": [], "principle": "오답 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "2개가 아닙니다.", "articles": [], "principle": "오답 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "첫 번째, 세 번째, 네 번째 지문 등 총 3개가 옳지 않은 지문입니다.", "articles": [], "principle": "오답 지문 개수", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "4개가 전부 틀린 것은 아닙니다(두 번째 지문은 참).", "articles": [], "principle": "오답 지문 개수", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "다음 중 계속기업가정에 대한 개념체계와 K-IFRS 제1001호 '재무제표 표시'의 요건 설명으로 옳은 설명의 조합은?\n\n[보기]\nㄱ. 계속기업 전제가 타당하지 않아 대체 기준을 사용하면 사용한 기준을 밝혀야 함은 개념체계와 기준서 공통 요구사항이다.\nㄴ. K-IFRS 제1001호는 계속기업가정 존속성에 중대한 불확실성이 존재하는 경우 그 불확실성의 공시를 요구한다.\nㄷ. 개념체계는 계속기업 평가 대상 기간을 명시적으로 '최소 12개월'로 정하고 있는 반면 K-IFRS 제1001호는 '예측가능한 미래'로 정성 서술한다.\nㄹ. 경영진이 기업을 청산하거나 경영활동을 중단할 불가피한 상황이 아니라면 계속기업을 전제로 재무제표를 작성해야 함은 제1001호 기준서의 규정이다.",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ ㄱ, ㄴ, ㄹ 지문은 모두 옳습니다. ㄷ 지문은 12개월 수치 규정이 K-IFRS 제1001호에 있고 정성적 '예측가능한 미래' 설명이 개념체계에 수록되어 있으므로 설명이 서로 바뀌어 틀렸습니다.\n\n[오답 해설]\nㄷ 지문이 틀렸으므로 ㄷ이 포함된 보기 ②, ④, ⑤는 오답이 되며, ㄹ이 누락된 ①도 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄹ 지문이 누락되었습니다.", "articles": [], "principle": "계속기업 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 거짓이고 ㄹ이 누락되었습니다.", "articles": [], "principle": "계속기업 조합", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "옳은 지문 ㄱ, ㄴ, ㄹ의 조합이 완벽히 식별되었습니다.", "articles": [], "principle": "계속기업 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 거짓이고 ㄱ이 누락되었습니다.", "articles": [], "principle": "계속기업 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ이 거짓이므로 전체 선택은 오답입니다.", "articles": [], "principle": "계속기업 조합", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "다음 중 연결재무제표, 비연결재무제표 및 결합재무제표의 개념에 대한 설명으로 옳지 않은 조합을 고른 것은?\n\n[보기]\nㄱ. 연결재무제표가 작성되어도 지배기업은 추가로 비연결재무제표를 선택 공시할 수 있다.\nㄴ. 비연결재무제표의 정보는 지배기업 주요이용자의 정보 수요를 채우기에 충분한 것이 일반적이므로 연결재무제표 공시 책임을 면제할 수 있다.\nㄷ. 연결재무제표는 특정 종속기업만의 개별 별도 자산 부채 정보를 독립 보고하기 위해 만들어진 재무제표이다.\nㄹ. 보고기업이 지배-종속으로 모두 연결되지 않은 둘 이상 실체로 구성되면 그 보고기업 재무제표를 결합재무제표라고 부른다.",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 옳지 않은 설명은 ㄴ과 ㄷ입니다.\nㄴ. 비연결재무제표는 정보수요 충족에 불충분하여 연결재무제표 공시 의무를 대체 면제할 수 없습니다.\nㄷ. 연결재무제표는 자회사 자체의 단독 정보를 보여주는 목적 설계 문서가 아닙니다(자회사 개별 재무제표가 제공함).\nㄱ, ㄹ 지문은 옳은 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ은 옳은 지문입니다.", "articles": [], "principle": "재무제표 오답 조합", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "틀린 지문인 ㄴ과 ㄷ만으로 올바르게 짝지어졌습니다.", "articles": [], "principle": "재무제표 오답 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ, ㄹ은 옳은 지문입니다.", "articles": [], "principle": "재무제표 오답 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 옳은 지문입니다.", "articles": [], "principle": "재무제표 오답 조합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ, ㄹ이 포함되어 오답입니다.", "articles": [], "principle": "재무제표 오답 조합", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "다음 중 보고기업의 경계 결정이 모호하여 어려울 때 적용하는 기준과 관련 원칙에 대한 설명 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 보고기업의 경계 획정이 어려운 경우, 재무제표의 주요이용자들의 정보 수요를 우선하여 맞춘다.\nㄴ. 경계를 획정할 때 일부 중요 경제 활동을 고의로 빼거나 왜곡하여 이용자의 판단을 오도해서는 안 된다.\nㄷ. 법인격이 존재하지 않는 회계 부문은 독립된 보고기업으로 지정하는 것이 법률상 절대 불가능하다.\nㄹ. 보고기업 범위 내에 포함되는 실체들의 경제 정보는 특정 지배주주 1인의 이익 포트폴리오 최적화 관점을 중심으로 통제 기재하여야 한다.",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄴ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "1",
        "explanation": "① ㄱ, ㄴ 지문은 옳습니다.\nㄷ. 법인격이 없더라도 보고기업으로 지정 가능하므로 불가능하다는 서술은 틀렸습니다.\nㄹ. 특정 주주 1인이 아닌 '보고기업 전체의 관점'이어야 하므로 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "옳은 지문 ㄱ, ㄴ으로만 구성되어 있습니다.", "articles": [], "principle": "경계 결정 다중", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 거짓입니다.", "articles": [], "principle": "경계 결정 다중", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 거짓입니다.", "articles": [], "principle": "경계 결정 다중", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ, ㄹ은 거짓입니다.", "articles": [], "principle": "경계 결정 다중", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ, ㄹ이 포함되어 오답입니다.", "articles": [], "principle": "경계 결정 다중", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },

    # =========================================================================
    # L5: 심화 분석 (2문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s05-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "회계학 이론 상 '계속기업가정(Going Concern Assumption)'이 역사적 원가주의(Historical Cost System) 측정 방식과 장기 자산의 '감가상각(Depreciation)' 제도를 지배하며 정당화하는 논리적 메커니즘을 가장 바르게 분석한 것은?",
        "options": [
            "① 계속기업가정이 깨져 청산 절차에 돌입하더라도 역사적 원가 방식의 감가상각 누계액 계상은 무조건 불변으로 유지되어야 원칙이 보장된다.",
            "② 정상적인 영업이 미래에도 무기한 지속된다고 가정하기 때문에, 자산의 취득 원가를 내용연수에 걸쳐 점진적 분배 상각(감가상각)할 수 있으며, 당장 처분할 청산가액으로 즉시 재평가하지 않고 역사적 원가로 기재하는 논리적 타당성을 제공한다.",
            "③ 계속기업가정은 자산의 감가상각액이 기업의 시가총액과 일대일로 정확히 비례하도록 강제함으로써 시장 가치를 직접 반영하게 돕는다.",
            "④ 감가상각이 완료된 자산은 법원에서 강제로 폐기 처분하므로 계속기업 원리와 아무런 이론적 인과관계가 없다.",
            "⑤ 계속기업가정이 유효할 때에는 부채의 현재가치 할인을 생략하도록 보증한다."
        ],
        "answer": "2",
        "explanation": "② 계속기업가정은 기업이 예측가능한 미래에 영업을 지속하여 보유 자산을 본래 영업 목적(사용)대로 쓸 것을 전제합니다. 따라서 당장 청산하여 시장에 팔아버릴 때의 가치(청산가치)로 평가하지 않고, 취득할 때 지불한 대가(역사적 원가)를 기록한 뒤 내용연수에 걸쳐 수익에 체계적으로 배분(감가상각)하는 실무를 정당화하는 가장 핵심적인 논리적 배경입니다. 만약 계속기업 전제가 무너지면 감가상각은 중단되고 즉시 회수 가능 가치(청산가치 등)로 전환 평가되어야 합니다.\n\n[오답 해설]\n① 청산 시에는 감가상각을 고수하지 않고 즉시 청산가치 평가 기준으로 대체 전환합니다.\n③ 감가상각과 시가총액 비례 규정은 전혀 무관합니다.\n④ 내용연수 만료와 법적 강제 폐기는 무관합니다.\n⑤ 부채의 현재가치 할인 생략과 계속기업 원리는 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "청산 시에는 감가상각 배분을 중단하고 평가 방법을 대체 기준(청산가치)으로 바꾸어야 합니다.", "articles": [], "principle": "계속기업의 정당화 논리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "영업 지속 가정이 있어야 역사적 원가주의 기재 및 기간별 체계적 상각 배분(감가상각)의 이론적 정당성이 성립합니다.", "articles": [], "principle": "계속기업의 정당화 논리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가총액 일대일 비례는 거짓입니다.", "articles": [], "principle": "계속기업의 정당화 논리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각과 계속기업가정은 뗄 수 없는 핵심 연계 관계를 가집니다.", "articles": [], "principle": "계속기업의 정당화 논리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 현재가치 할인 의무 면제와 무관합니다.", "articles": [], "principle": "계속기업의 정당화 논리", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s05-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "법적 실체(Legal Entity)와 회계적 실체(Reporting Entity)의 불일치를 반영하는 '지배-종속 관계' 하에서, 연결재무제표가 비연결재무제표를 대체하여 요구되는 이유 및 한계에 관한 분석으로 가장 옳지 않은 것은?",
        "options": [
            "① 비연결재무제표는 지배기업만의 자산 등을 제공하므로 종속기업을 통합한 실질적 연결 경계의 통제 하에 있는 자원의 상태를 오도하여 충분한 정보를 주지 못한다.",
            "② 연결재무제표는 법률적으로는 별개의 유한책임 실체인 지배기업과 종속기업을 경제적 단일 보고실체로 의제하여 실질을 반영함으로써 정보유용성을 극대화한다.",
            "③ 연결재무제표를 제공함으로써 지배기업 자체는 물론 특정 개별 종속기업이 지닌 자산과 부채의 단독 회수 가능 정보를 완벽히 개별 분석할 수 있도록 주석에 모든 상세 자회사 전용 정보를 대체 기재하여 제공해준다.",
            "④ 지배기업은 연결재무제표를 주된 수단으로 하되, 필요하다면 연결재무제표에 추가하여 비연결재무제표 작성을 병행 선택할 수 있다.",
            "⑤ 연결재무제표가 요구되는 상황에서 모회사의 단독 비연결재무제표만을 제출하여 공시를 갈음하는 것은 개념체계상 절대 불가하다."
        ],
        "answer": "3",
        "explanation": "③ 연결재무제표는 단일 보고실체로서의 정보를 제공하도록 설계된 것일 뿐, 특정 자회사(종속기업)의 자산, 부채 등의 별도 정보를 독립적으로 제공하도록 만들어지지 않았습니다. 해당 상세 개별 정보는 종속기업 자체의 재무제표를 별도로 보아 파악해야 하는 연결재무제표의 내재적 정보 범위 한계가 있습니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 모두 법적 실체와 회계 보고 실체의 관계 및 연결/비연결재무제표의 존재 이유와 상호 보완성을 정확하게 설명하고 있는 옳은 지문들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비연결의 정보 불충분성 진술은 참입니다.", "articles": [], "principle": "연결 및 비연결 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법적 실체와 별도로 경제 실질을 반영한다는 설명은 정당합니다.", "articles": [], "principle": "연결 및 비연결 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "연결재무제표는 특정 종속기업만의 개별적 세부 정보를 별도 제공하도록 설계된 것이 아니라는 한계를 분석해야 하므로 3번 설명이 오답입니다.", "articles": [], "principle": "연결 및 비연결 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "병행 선택권에 관한 진술은 사실입니다.", "articles": [], "principle": "연결 및 비연결 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대체 불가성에 관한 진술은 사실입니다.", "articles": [], "principle": "연결 및 비연결 분석", "case": {"holding": "", "no": None}}
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
                "item": "5절 계속기업가정, 보고기업"
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
