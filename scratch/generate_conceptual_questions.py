import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

questions = [
    # =========================================================================
    # L1: 기초 개념 (10문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s01-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "재무보고를 위한 개념체계의 위상에 관한 설명으로 옳은 것은?",
        "options": [
          "① 개념체계는 한국채택국제회계기준(K-IFRS)과 동등한 효력을 가진다.",
          "② 개념체계는 특정 기준서에 우선하여 적용된다.",
          "③ 개념체계는 회계기준(기준서)이 아니다.",
          "④ 개념체계는 일반목적재무보고가 아닌 특수목적재무보고만을 규정한다.",
          "⑤ 개념체계는 기업의 세무보고 및 감독보고를 주된 목적으로 한다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계는 회계기준(기준서)이 아니며, 개념체계의 어떠한 내용도 특정 회계기준이나 그 요구사항에 우선하지 않습니다.\n\n[오답 해설]\n①, ② 개념체계는 기준서가 아니므로 기준서의 요구사항에 우선할 수 없습니다.\n④ 개념체계는 일반목적재무보고의 목적과 개념을 서술합니다.\n⑤ 개념체계는 세무보고나 감독보고 등 특수목적 재무보고가 아닌 일반목적재무보고를 규정합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "개념체계는 한국채택국제회계기준(기준서)이 아니며 이에 우선할 수 없습니다.", "articles": [], "principle": "개념체계 위상", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계의 어떠한 내용도 특정 회계기준이나 그 요구사항에 우선하지 않습니다.", "articles": [], "principle": "개념체계 위상", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계는 회계기준이 아닙니다.", "articles": [], "principle": "개념체계 위상", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계는 일반목적재무보고를 규정합니다.", "articles": [], "principle": "개념체계 범위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무보고 및 감독보고 등은 주요 목적이 아닙니다.", "articles": [], "principle": "재무보고 범위", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "개념체계와 한국채택국제회계기준(K-IFRS)의 관계에 관한 설명으로 옳은 것은?",
        "options": [
          "① 개념체계의 규정과 K-IFRS의 규정이 상충될 경우 개념체계가 우선한다.",
          "② 개념체계의 규정과 K-IFRS의 규정이 상충될 경우 K-IFRS가 우선한다.",
          "③ 두 규정이 상충할 경우 재무제표 작성자가 자율적으로 선택하여 적용한다.",
          "④ 두 규정이 상충할 경우 상법의 관련 규정을 우선 적용한다.",
          "⑤ 두 규정이 상충하는 상황은 논리적으로 발생할 수 없다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준이 아니므로, 개념체계와 특정 회계기준(K-IFRS)이 상충할 경우 항상 K-IFRS 기준서의 요구사항이 우선합니다.\n\n[오답 해설]\n① 상충 시 회계기준(K-IFRS)이 우선합니다.\n③ 작성자가 선택할 수 없으며 기준서를 따라야 합니다.\n④ 상법이 아닌 K-IFRS 기준서가 회계처리 상 우선합니다.\n⑤ 일반목적재무보고 목적 달성을 위해 회계기준위원회는 개념체계의 관점에서 일탈한 회계기준을 정할 수 있으므로 상충 상황은 발생할 수 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "상충 시 개념체계가 우선한다는 설명은 틀렸습니다.", "articles": [], "principle": "개념체계 우선순위", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "상충 시 항상 회계기준(K-IFRS)이 우선합니다.", "articles": [], "principle": "개념체계 우선순위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "작성자에게 자율 선택권은 없습니다.", "articles": [], "principle": "회계기준의 강제력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "K-IFRS 기준서의 우선 적용 원칙입니다.", "articles": [], "principle": "K-IFRS 우선", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "상충은 발생 가능하며, 일탈 사례가 존재할 수 있습니다.", "articles": [], "principle": "일탈 발생 가능성", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "개념체계의 개정이 한국채택국제회계기준(K-IFRS)에 미치는 영향으로 옳은 것은?",
        "options": [
          "① 개념체계가 개정되면 상충되는 기존 회계기준은 즉시 자동 개정된다.",
          "② 개념체계가 개정되면 상충되는 기존 회계기준은 효력을 상실한다.",
          "③ 개념체계가 개정되더라도 기존의 회계기준이 자동으로 개정되는 것은 아니다.",
          "④ 개념체계는 수시로 개정될 수 없으며, 국제회계기준(IASB)의 승인을 거쳐 10년에 한 번만 개정된다.",
          "⑤ 개념체계가 개정되면 기업들은 개정된 개념체계에 맞추어 재무제표를 소급 재작성해야 한다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계는 회계기준위원회의 업무 경험을 바탕으로 수시로 개정될 수 있으나, 개념체계가 개정되었다고 해서 자동으로 기존의 회계기준(K-IFRS)이 개정되는 것은 아닙니다.\n\n[오답 해설]\n①, ② 개념체계 개정이 회계기준의 즉각적인 자동 개정이나 효력 소멸을 유발하지 않습니다.\n④ 개념체계는 관련 업무 경험을 토대로 필요 시 수시로 개정될 수 있습니다.\n⑤ 개념체계 개정만으로는 재무제표의 소급 재작성 의무가 발생하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기존 기준서는 자동 개정되지 않습니다.", "articles": [], "principle": "개념체계 개정 영향", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기존 기준서는 효력을 그대로 유지합니다.", "articles": [], "principle": "개념체계 개정 영향", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계의 개정이 기존 회계기준을 자동으로 개정시키지는 않습니다.", "articles": [], "principle": "개념체계 개정 영향", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계는 수시로 개정될 수 있습니다.", "articles": [], "principle": "개념체계 개정 주기", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "소급 재작성 의무는 발생하지 않습니다.", "articles": [], "principle": "소급적용 여부", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "개념체계의 목적에 해당하지 않는 것은?",
        "options": [
          "① 회계기준위원회가 일관된 개념에 기반하여 회계기준을 제·개정하도록 돕는다.",
          "② 적용할 회계기준이 없는 경우 재무제표 작성자가 회계정책을 개발하도록 돕는다.",
          "③ 모든 이해관계자가 회계기준을 이해하고 해석하는 데 도움을 준다.",
          "④ 외부감사인이 재무제표가 회계기준에 따라 작성되었는지 감사의견을 형성하는 데 도움을 준다.",
          "⑤ 과세관청이 세법상 세무조정을 통해 정확한 법인세를 징수하도록 돕는다."
        ],
        "answer": "5",
        "explanation": "⑤ 개념체계는 일반목적재무보고를 위한 개념적 기초를 다지는 문서이며, 세법상의 세무조정이나 세금 징수를 목적으로 하지 않습니다.\n\n[오답 해설]\n①, ②, ③, ④는 모두 개념체계가 공식적으로 규정하고 있는 목적에 해당합니다(외부감사인의 감사 수행 및 작성자의 회계정책 개발 포함).",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "회계기준위원회 지원은 주요 목적 중 하나입니다.", "articles": [], "principle": "개념체계 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "작성자의 회계정책 개발 지원은 목적에 해당합니다.", "articles": [], "principle": "개념체계 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "이해관계자의 회계기준 해석 지원은 목적에 해당합니다.", "articles": [], "principle": "개념체계 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사인의 의견 형성을 돕는 것도 간접적 지원 범위에 속합니다.", "articles": [], "principle": "개념체계 목적", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "세무조정 및 세금 징수 지원은 개념체계의 목적이 아닙니다.", "articles": [], "principle": "개념체계 제외 목적", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "일반목적재무보고의 주요 이용자(Primary Users)에 해당하는 정보이용자로 옳은 것은?",
        "options": [
          "① 기업의 내부 경영진",
          "② 국세청 등 세무당국",
          "③ 현재 및 잠재적 투자자",
          "④ 기업 회계기준 감독기관(금융감독원 등)",
          "⑤ 기업의 영업활동을 감시하는 시민단체"
        ],
        "answer": "3",
        "explanation": "③ 개념체계 상 일반목적재무보고서가 초점을 맞추는 주요 이용자는 '현재 및 잠재적 투자자, 대여자 및 기타 채권자'입니다.\n\n[오답 해설]\n① 경영진은 내부에서 정보를 쉽게 획득하므로 일반목적재무보고서에 전적으로 의존하는 주요 이용자가 아닙니다.\n②, ④, ⑤ 규제기관, 세무당국, 시민단체 등은 주요 이용자 범위에 포함되지 않으며, 일반목적재무보고서 외의 수단으로 정보를 얻을 수 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "경영진은 주요 이용자에서 제외됩니다.", "articles": [], "principle": "주요 이용자 제외", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무당국은 주요 이용자가 아닙니다.", "articles": [], "principle": "주요 이용자 제외", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "현재 및 잠재적 투자자, 대여자, 기타 채권자가 주요 이용자입니다.", "articles": [], "principle": "주요 이용자 범위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감독기관은 주요 이용자가 아닙니다.", "articles": [], "principle": "주요 이용자 제외", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "시민단체는 주요 이용자가 아닙니다.", "articles": [], "principle": "주요 이용자 제외", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "일반목적재무보고서의 성격과 한계에 관한 설명으로 옳은 것은?",
        "options": [
          "① 재무보고서는 보고기업의 시장 가치를 직접 계산하여 정확하게 보여준다.",
          "② 재무보고서는 주요이용자가 필요로 하는 모든 정보를 완벽하게 제공한다.",
          "③ 재무보고서는 보고기업의 가치를 직접 보여주기 위해 고안된 것이 아니다.",
          "④ 재무보고서는 과거 사건의 재무적 영향만을 나타내며, 미래 전망이나 예측을 돕는 정보는 배제한다.",
          "⑤ 재무보고서는 각 정보이용자의 특수한 정보 요구를 개별적으로 반영하여 다르게 작성된다."
        ],
        "answer": "3",
        "explanation": "③ 일반목적재무보고서는 보고기업의 가치를 보여주기 위해 고안된 것이 아닙니다. 다만 주요 이용자가 기업의 가치를 스스로 추정하는 데 유용한 정보를 제공할 뿐입니다.\n\n[오답 해설]\n① 가치를 직접 계산하여 보여주지 않습니다.\n② 주요 이용자가 요구하는 모든 정보를 제공할 수는 없으며 제공하지도 않습니다.\n④ 재무보고서는 미래 예상 등을 포함한 기업 가치 추정에 유용한 미래지향적 정보도 간접적으로 제공합니다.\n⑤ 재무보고서는 공통의 정보 요구를 충족하도록 작성되며 개별적 특수 요구에 맞추어 다르게 작성되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "재무보고서는 기업 가치를 직접 계산해 주지 않습니다.", "articles": [], "principle": "재무보고서의 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "모든 유용한 정보를 완벽하게 제공할 수는 없습니다.", "articles": [], "principle": "재무보고서의 한계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 보고기업의 가치를 보여주기 위해 고안된 것이 아닙니다.", "articles": [], "principle": "재무보고서의 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "미래 전망과 추정에 도움이 되는 정보도 제공합니다.", "articles": [], "principle": "정보의 성격", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "이용자들의 공통 요구사항을 반영해 단일 보고서로 공시됩니다.", "articles": [], "principle": "일반목적재무보고", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "일반목적재무보고서와 보고기업 경영진(Management)의 관계에 관한 설명으로 옳은 것은?",
        "options": [
          "① 경영진은 일반목적재무보고서의 가장 핵심적인 주요이용자에 속한다.",
          "② 경영진은 의사결정을 위해 필요한 정보를 내부에서 입수할 수 있으므로 일반목적재무보고서에 의존할 필요가 없다.",
          "③ 회계기준위원회는 경영진의 특수한 의사결정 요구를 최우선적으로 반영하여 회계기준을 제정한다.",
          "④ 경영진은 재무제표의 신뢰성을 확인하기 위해 회사의 외부보고용 일반목적재무보고서에 전적으로 의존한다.",
          "⑤ 개념체계는 경영진이 내부 의사결정을 할 때 준수해야 하는 강제적인 관리회계 기준을 제시한다."
        ],
        "answer": "2",
        "explanation": "② 보고기업의 경영진도 해당 기업에 대한 재무정보에 관심을 가질 수 있으나, 필요한 정보를 기업 내부에서 입수할 수 있으므로 굳이 일반목적재무보고서에 의존할 필요는 없습니다.\n\n[오답 해설]\n① 경영진은 주요 이용자(외부의 자원 제공자)가 아닙니다.\n③, ⑤ 회계기준은 외부보고용 재무제표 기준이며, 내부 경영진의 내부용 회계(관리회계)나 특정 목적 의사결정을 지배하지 않습니다.\n④ 경영진은 외부보고서를 작성하는 주체이므로 보고서에 의존하여 내부 상태를 파악하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "경영진은 주요 이용자에서 제외됩니다.", "articles": [], "principle": "주요 이용자 범위", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "경영진은 필요한 재무정보를 내부에서 얻으므로 의존할 필요가 없습니다.", "articles": [], "principle": "경영진의 정보 접근성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "경영진의 요구를 최우선 반영하지 않습니다.", "articles": [], "principle": "회계기준 제정 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "경영진은 보고서 작성 및 관리 주체입니다.", "articles": [], "principle": "경영진의 정보 접근성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계는 외부보고 목적입니다.", "articles": [], "principle": "개념체계 적용 범위", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "개념체계의 구성요소 중 다른 모든 개념적 판단의 '기초(Foundation)'를 형성하는 것은?",
        "options": [
          "① 유용한 재무정보의 질적 특성",
          "② 재무제표의 요소 정의",
          "③ 일반목적재무보고의 목적",
          "④ 자본 및 자본유지 개념",
          "⑤ 재무정보에 대한 원가제약"
        ],
        "answer": "3",
        "explanation": "③ 일반목적재무보고의 목적은 개념체계의 기초(Foundation)를 형성합니다. 질적 특성, 재무제표 요소, 측정 및 공시 등 개념체계의 다른 모든 측면들은 이 목적(유용한 재무정보 제공)으로부터 논리적으로 도출됩니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 목적을 달성하기 위해 목적으로부터 전개되는 하위 개념 체계들입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "질적 특성은 목적으로부터 유도됩니다.", "articles": [], "principle": "개념체계 구조", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "재무제표 요소 정의는 목적으로부터 유도됩니다.", "articles": [], "principle": "개념체계 구조", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고의 목적이 개념체계의 가장 밑단에 해당하는 기초를 형성합니다.", "articles": [], "principle": "재무보고의 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자본 및 자본유지는 목적 하위에 위치합니다.", "articles": [], "principle": "개념체계 구조", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "원가제약도 목적을 달성하기 위한 현실적 제약 조건입니다.", "articles": [], "principle": "개념체계 구조", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "개념체계가 정보 격차를 줄이고 자본제공자(Capital Providers)와 자본수탁자(Steward) 간의 관계에서 기여하고자 하는 역할로 옳은 것은?",
        "options": [
          "① 기업의 법적 책임 소송을 중재하는 법률적 중재 기능",
          "② 자본제공자와 수탁자 간의 정보 격차를 줄임으로써 책임을 강화(Accountability)하는 기능",
          "③ 자본수탁자(경영진)가 주가 조작을 하지 못하게 형사 처벌하는 기능",
          "④ 기업의 인수합병 가격을 공정하게 산정하여 강제하는 기능",
          "⑤ 기업의 영업 비밀이 자본시장 참여자에게 절대 유출되지 않도록 정보 차단막을 형성하는 기능"
        ],
        "answer": "2",
        "explanation": "② 개념체계는 정보의 비대칭성(정보 격차)을 줄임으로써 수탁책임(Accountability)을 강화하는 역할을 합니다. 비교가능하고 신뢰성 있는 정보 공시를 통해 경영진의 수탁 의무 이행을 효과적으로 감시하도록 돕습니다.\n\n[오답 해설]\n①, ③, ④ 개념체계는 법적 소송 중재, 형사 처벌, 혹은 인수합병가 강제 등의 법적·행정적 권한이 없습니다.\n⑤ 정보 차단이 아닌, 정보 격차를 '줄이는(줄임으로써 책임을 강화)' 역할을 합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "개념체계는 법률적 중재 기능이 없습니다.", "articles": [], "principle": "개념체계 기능", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "정보 격차를 줄여 수탁책임을 묻는 책임을 강화합니다.", "articles": [], "principle": "책임 강화", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "형사 처벌 기능은 사법당국의 역할입니다.", "articles": [], "principle": "개념체계 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "인수합병 가격을 산정 및 강제하지 않습니다.", "articles": [], "principle": "개념체계 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "정보 차단막이 아닌 공시와 투명성 촉진을 추구합니다.", "articles": [], "principle": "투명성 촉진", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "회계기준위원회(KASB)의 공식 임무로서 개념체계가 바탕을 다지고자 하는 공공이익(Public Interest) 창출의 3대 요소가 아닌 것은?",
        "options": [
          "① 투명성(Transparency)",
          "② 책임성(Accountability)",
          "③ 경제적 효율성(Efficiency)",
          "④ 주주 이익의 극대화(Shareholder Wealth Maximization)",
          "⑤ 장기적 금융안정(Long-term Financial Stability)"
        ],
        "answer": "4",
        "explanation": "④ 회계기준위원회의 공식 임무는 전 세계 금융시장에 투명성, 책임성, 효율성을 제공하여 공공이익에 기여하는 것입니다. 주주 이익의 극대화는 개념체계나 회계기준위원회가 제시하는 공식 임무의 구성요소가 아닙니다.\n\n[오답 해설]\n①, ②, ③은 회계기준위원회가 금융시장에 제공하고자 하는 3대 축입니다.\n⑤ 장기적 금융안정은 신뢰와 성장 유도를 통해 조성하고자 하는 공공이익의 가치입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "투명성은 3대 요소에 포함됩니다.", "articles": [], "principle": "회계기준위원회 임무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "책임성은 3대 요소에 포함됩니다.", "articles": [], "principle": "회계기준위원회 임무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "경제적 효율성은 3대 요소에 포함됩니다.", "articles": [], "principle": "회계기준위원회 임무", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "주주이익 극대화는 공식 임무에 규정되지 않은 별개 경영 목표입니다.", "articles": [], "principle": "회계기준위원회 임무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장기적 금융안정은 공공이익 추구 목적으로 명시되어 있습니다.", "articles": [], "principle": "장기적 금융안정", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },

    # =========================================================================
    # L2: 이해 수준 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s01-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "개념체계의 문항과 한국채택국제회계기준(K-IFRS)의 요구사항이 명백하게 상충할 경우에 대한 K-IFRS 기준서의 지침으로 옳은 것은?",
        "options": [
          "① 기업은 즉시 개념체계의 원칙적인 회계처리를 우선적으로 적용하여 상충을 해소해야 한다.",
          "② 기준서가 우선 적용되며, 회계기준위원회는 관련 기준서의 결론도출근거에 개념체계와의 일탈에 대하여 설명한다.",
          "③ 상충이 발생하는 즉시 당해 기업의 재무제표에 대한 감사보고서는 한정의견으로 작성되어야 한다.",
          "④ 해당 거래에 대하여 금융감독원이 직접 행정지도를 하여 적용 법규를 강제 지정해 줄 때까지 공시를 보류한다.",
          "⑤ 회계기준위원회는 해당 상충을 해결하기 위해 개념체계를 기준서에 부합하도록 즉시 소급 개정한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준이 아니므로 특정 회계기준(K-IFRS)의 요구사항에 우선하지 않습니다. 회계기준위원회가 개념체계와 다른 요구사항을 제정하는 경우가 있을 수 있으며, 이 경우 해당 기준서의 결론도출근거에 그러한 일탈에 대해 설명합니다.\n\n[오답 해설]\n① 상충 시 회계기준(K-IFRS)의 요구사항이 우선합니다.\n③ K-IFRS 기준서 요구사항을 적법하게 준수하였으므로 감사의견 상 한정의견 대상이 아닙니다.\n④ 공시를 보류하는 규정은 없으며 기준서에 따라 처리합니다.\n⑤ 개념체계는 축적된 경험을 토대로 수시로 개정될 수 있으나 기준서에 맞춰 즉시 소급 개정하는 것은 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "상충 시 개념체계를 우선 적용하지 않습니다.", "articles": [], "principle": "개념체계 위상", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서가 우선 적용되며 결론도출근거에 그 일탈이 설명됩니다.", "articles": [], "principle": "개념체계 일탈 설명", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사 의견 거절이나 한정의 사유가 될 수 없습니다.", "articles": [], "principle": "회계기준 우선", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "행정지도를 기다려 공시를 보류하지 않습니다.", "articles": [], "principle": "공시 의무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계가 자동 소급 개정되는 것은 아닙니다.", "articles": [], "principle": "개념체계 개정", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "개념체계의 목적에 대한 서술 중 작성자(Preparer) 관점에서 그 역할로 옳은 것은?",
        "options": [
          "① 세무조정 신고서 작성 시 적용할 세법상의 소득 계산 절차를 통일해 준다.",
          "② 특정 거래에 적용할 회계기준이 없거나 회계기준에서 회계정책을 선택하는 것을 허용하는 경우에 작성자가 일관된 회계정책을 개발하는 데 도움을 준다.",
          "③ 작성자가 특정 자본조달 계약서상의 채무불이행 리스크를 회계 장부에 기재하지 않고 누락할 수 있는 법적 재량을 보장한다.",
          "④ 모든 거래에 관하여 회계기준위원회의 사전 유권해석 없이 자의적인 방법으로 당기순이익을 평준화할 수 있는 기준을 마련해 준다.",
          "⑤ 작성자의 개인적 판단을 완전히 배제하고, 수학적으로 검증된 고정 수치만을 재무상태표에 표시하도록 강제한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계의 공식적인 두 번째 목적은 특정 거래나 다른 사건에 적용할 회계기준이 없거나 회계기준에서 회계정책을 선택하는 것을 허용하는 경우에 재무제표 작성자가 일관된 회계정책을 개발하는 데 도움을 주는 것입니다.\n\n[오답 해설]\n① 개념체계는 세법상 소득 계산과 무관합니다.\n③, ④ 재산 누락이나 자의적인 이익 평준화(분식회계)를 조장하지 않습니다.\n⑤ 재무제표는 정확한 서술보다 추정, 판단, 모형에 상당 부분 근거하므로 개인적 판단을 배제하지 않으며 오히려 지침을 줍니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "세법과는 전혀 무관합니다.", "articles": [], "principle": "개념체계 목적", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "적용할 기준이 없거나 회계정책 선택이 허용된 경우 작성자의 일관된 회계정책 개발을 돕습니다.", "articles": [], "principle": "작성자 지원", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "부채 누락 등 부적절한 목적을 지원하지 않습니다.", "articles": [], "principle": "개념체계 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적인 이익 조정은 허용되지 않습니다.", "articles": [], "principle": "개념체계 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "재무제표는 상당 부분 추정과 판단에 근거합니다.", "articles": [], "principle": "추정과 판단", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "개념체계의 개정(Revision) 절차와 관련한 설명으로 옳지 않은 것은?",
        "options": [
          "① 개념체계는 회계기준위원회가 관련 업무를 통해 축적한 경험을 토대로 수시로 개정될 수 있다.",
          "② 개념체계의 개정이 발생하더라도, 자동으로 기존 회계기준(K-IFRS)이 변경되거나 개정되는 것은 아니다.",
          "③ 개념체계를 개정하려면 회계기준위원회뿐만 아니라 외부 감사법인 연합회의 전원 동의 및 금융위원회의 사전 승인이 필수적이다.",
          "④ 개념체계가 개정되어도 기존 회계기준과의 상충이 발생하는 상황이 즉각 해결되지 않고 과도기적으로 존재할 수 있다.",
          "⑤ 개념체계의 개정 절차는 기준서 제·개정 절차와 독립적으로 운영될 수 있다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계는 한국회계기준원 회계기준위원회가 수시로 심의하여 개정할 수 있으며, 외부 감사법인 연합회의 전원 동의나 금융위원회의 사전 승인을 필수 요건으로 규정하고 있지 않습니다.\n\n[오답 해설]\n① 개념체계는 업무 경험 축적에 따라 수시로 개정 가능합니다.\n② 개념체계가 개정되었다고 하여 기존 기준서의 개정 효력이 자동으로 발생하는 것은 아닙니다.\n④ 개정된 개념체계와 기존 기준서 간 상충이 발생하는 경우에도 기존 기준서의 효력은 유지됩니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "수시 개정 가능 규정은 옳습니다.", "articles": [], "principle": "개념체계 개정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기존 기준서가 자동 개정되지 않는다는 설명은 옳습니다.", "articles": [], "principle": "자동개정 여부", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "금융위원회의 사전 승인이나 감사법인 전원 동의 절차는 개념체계의 공식 개정 절차가 아닙니다.", "articles": [], "principle": "개념체계 개정 주체", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계 개정 직후 상충하는 기존 기준서가 유지되는 과도기가 존재할 수 있습니다.", "articles": [], "principle": "상충의 존속", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기준서 개정과 개념체계 개정은 독립적으로 추진됩니다.", "articles": [], "principle": "개정 절차 독립성", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "개념체계가 회계기준위원회의 공식 임무(Mission)인 투명성(Transparency) 제공에 기여하는 방식으로 옳은 것은?",
        "options": [
          "① 기업의 영업 기밀을 완전히 대중에게 노출하도록 규율한다.",
          "② 재무정보의 국제적 비교가능성과 정보의 질을 향상시킴으로써 기여한다.",
          "③ 전국의 모든 사업체가 매일 발생한 모든 전표를 일일 공시하도록 의무화한다.",
          "④ 재무제표의 모든 작성 오류를 형사상 불법행위로 규정하여 공시 신뢰성을 강제한다.",
          "⑤ 회계처리를 원가모형 하나로 통일하여 평가의 다양성을 원천 차단한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 전 세계 금융시장에 투명성, 책임성, 효율성을 제공하는 회계기준을 개발하도록 기여합니다. 이 중 투명성은 국제적 비교가능성과 정보의 질을 향상시켜 정보이용자가 정보에 입각한 경제적 의사결정을 내릴 수 있도록 지원함으로써 달성됩니다.\n\n[오답 해설]\n① 영업 기밀의 완전 노출을 강제하지 않습니다.\n③ 일일 공시 의무화는 개념체계의 소관이 아닙니다.\n④ 개념체계는 형사처벌 규정을 담고 있지 않습니다.\n⑤ 자산 평가방식을 인위적으로 원가모형으로 강제 통일하여 질적 유용성을 저해하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "투명성은 기밀 노출이 아닌 유용한 정보의 제공입니다.", "articles": [], "principle": "투명성 의의", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "국제적 비교가능성과 정보의 질 향상으로 투명성에 기여합니다.", "articles": [], "principle": "투명성 기여", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "일일 공시 의무화와 무관합니다.", "articles": [], "principle": "공시 주기", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사법적 처벌 권한은 개념체계에 없습니다.", "articles": [], "principle": "처벌 권한 부재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "질적 유용성 향상을 목표로 합니다.", "articles": [], "principle": "평가 모형", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "개념체계가 책임성(Accountability) 강화에 기여하여 공공이익에 기여하는 방식에 관한 설명으로 옳은 것은?",
        "options": [
          "① 주주총회에서 경영진의 연임을 법적으로 자동 금지시키는 역할을 한다.",
          "② 자본제공자와 자본수탁자 간의 정보 격차를 줄이고, 경영진의 책임을 묻는 데 필요한 정보를 제공한다.",
          "③ 기업 경영상의 모든 손실을 이사회가 개인 재산으로 직접 보전하게 규정한다.",
          "④ 외부 회계감사를 수행하는 주기와 수수료 한도를 명시하여 투명성을 감독한다.",
          "⑤ 채권자들에게 보고기업의 채무를 전액 탕감하도록 강제하는 원칙을 부여한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 자본제공자(투자자 등)와 자본수탁자(경영진) 간의 정보 격차(비대칭성)를 줄임으로써 수탁책임을 평가하고 책임을 강화하도록 돕습니다.\n\n[오답 해설]\n① 경영진의 연임 여부는 법률 및 정관의 소관입니다.\n③ 재산적 보전 규정은 상법 등의 소관입니다.\n④ 감사 수수료나 감사 주기 설정은 외감법의 영역입니다.\n⑤ 채무 탕감을 강제하는 등 사적 계약 관계를 강제 조정하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "법적 경영 통제는 개념체계의 역할이 아닙니다.", "articles": [], "principle": "개념체계 적용 범위", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "자본제공자와 수탁자 간 정보 격차를 축소하여 책임을 강화합니다.", "articles": [], "principle": "책임 강화", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "이사회 손실 보전과 무관합니다.", "articles": [], "principle": "상법 상 책임", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "외부감사 수수료 설정 권한이 없습니다.", "articles": [], "principle": "외부감사제도", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "채무 조정 강제와 무관합니다.", "articles": [], "principle": "사적 계약", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "개념체계가 경제적 효율성(Efficiency)에 기여하여 공공이익에 기여하는 효과로 옳은 것은?",
        "options": [
          "① 기업의 대출 이자율을 연 1% 이하로 낮추어 금융비용을 없애 준다.",
          "② 투자자에게 기회와 위험을 파악하도록 도움을 주어 자본 배분을 향상시키며, 신뢰성 있는 단일 회계 언어 사용으로 자본비용을 감소시킨다.",
          "③ 국가 간 환율 변동을 억제하여 고정환율제를 장기적으로 유지시킨다.",
          "④ 기업의 마케팅 광고 선전비 한도를 매출액 대비 5% 이내로 규제하여 비효율을 방지한다.",
          "⑤ 무가치한 부실 자산을 공정가치로 강제 평가하여 시장에서 바로 퇴출되도록 통제한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 투자자가 전 세계의 기회와 위험을 파악하게 도와 효율적인 자본 배분을 유도합니다. 개념체계에 기반한 신뢰성 있는 단일 회계 언어는 전 세계 자본시장에서 자본비용과 국제보고 비용을 경감시킵니다.\n\n[오답 해설]\n① 시장 금리를 개념체계가 통제할 수 없습니다.\n③ 환율 정책은 거시경제 정책의 영역입니다.\n④ 마케팅 예산에 대한 경영상의 한도를 규제하지 않습니다.\n⑤ 자산 강제 처분 등 시장 감독 기구의 직접적 행정명령 성격이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "금리 규제는 개념체계의 소관이 아닙니다.", "articles": [], "principle": "개념체계 범위", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "자본 배분 향상 및 단일 회계 언어로 자본비용을 절감시킵니다.", "articles": [], "principle": "효율성 기여", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "환율 정책과 무관합니다.", "articles": [], "principle": "거시경제", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "광고선전비 규제와 무관합니다.", "articles": [], "principle": "경영 자율권", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "부실자산 강제 매각 권한이 없습니다.", "articles": [], "principle": "감독 기구", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "개념체계의 범위(Scope)와 다른 개념들의 논리적 관계에 관한 설명으로 옳은 것은?",
        "options": [
          "① 유용한 재무정보의 질적 특성이 개념체계의 최상단 기초를 형성하며, 목적은 질적 특성으로부터 파생된다.",
          "② 일반목적재무보고의 목적이 개념체계의 기초(Foundation)를 형성하며, 질적 특성 등 개념체계의 다른 측면들은 이 목적으로부터 논리적으로 전개된다.",
          "③ 자본 및 자본유지 개념이 기초가 되어 보고기업의 목적이 정의되고 인식과 제거 규칙이 정해진다.",
          "④ 원가제약 원칙은 개념체계의 기초이며, 모든 일반목적재무보고서의 목적은 무조건 원가 최소화에 맞춰 설정되어야 한다.",
          "⑤ 개념체계 각 장의 규정은 아무런 논리적 인과관계 없이 회계기준위원회가 무작위로 열거한 것에 불과하다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고의 목적은 개념체계의 기초(Foundation)를 형성합니다. 질적 특성, 보고기업 개념, 재무제표 요소, 인식과 제거, 측정 등은 그 목적으로부터 논리적으로 전개됩니다.\n\n[오답 해설]\n① 질적 특성이 아닌 '일반목적재무보고의 목적'이 최상위 기초입니다.\n③ 자본 유지 개념은 재무제표의 요소와 측정 원리 하위에서 유도되는 개념입니다.\n④ 원가제약은 유용한 정보의 보고에 대한 현실적 제약일 뿐 개념체계의 기초를 이루는 원천 목적이 아닙니다.\n⑤ 개념체계는 목적부터 출발하여 체계적으로 하위 개념을 유도하는 일관된 논리적 완결성을 지니고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "질적 특성이 아닌 재무보고 목적이 기초입니다.", "articles": [], "principle": "개념체계 기초", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고의 목적이 개념체계의 기초를 형성하고 다른 측면이 파생됩니다.", "articles": [], "principle": "개념체계 논리적 연계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자본 개념은 기초가 아닌 논리적 파생물입니다.", "articles": [], "principle": "자본 개념 지위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "원가제약은 기초 목적이 아닙니다.", "articles": [], "principle": "원가제약 지위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계는 정밀한 논리 구조를 가집니다.", "articles": [], "principle": "논리적 인과", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "재무보고서의 정확성(Accuracy)에 관한 개념체계의 현실적 서술로 옳은 것은?",
        "options": [
          "① 재무제표는 수학적 절대 오류가 없어야 하므로 정확한 서술만을 규정한다.",
          "② 재무제표는 상당 부분 정확한 서술보다는 추정, 판단 및 모형에 근거한다.",
          "③ 개념체계는 추정과 판단의 자의성을 늘리기 위해 모호한 정의를 우선적으로 제시한다.",
          "④ 재무제표에 반영되는 모형과 추정은 소수점 단위까지 K-IFRS 기준서에 정확히 매핑된 단일 공식을 사용해야 한다.",
          "⑤ 추정치나 판단이 개입된 재무정보는 신뢰성이 결여되므로 재무상태표의 자산 가액에서 전액 배제해야 한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 재무보고서가 정확한 서술보다는 상당 부분 추정, 판단 및 모형에 근거하고 있음을 명시하고 있습니다. 개념체계는 이러한 추정, 판단 및 모형의 기초가 되는 일관된 개념을 정하는 역할을 합니다.\n\n[오답 해설]\n① 재무제표는 미래 가치 추정 등 주관적인 판단이 불가피하므로 절대적인 정확한 서술로만 구성될 수 없습니다.\n③ 자의성을 늘리는 것이 아니라 일관성을 확보해 주기 위한 기초 개념을 제공합니다.\n④ 기준서가 추정의 단일 공식을 강제하지 않으며 실무적 판단을 존중합니다.\n⑤ 추정치도 신뢰성 있게 측정 가능하다면 자산으로 인식하여 보고해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "절대적 정확한 서술로만 이루어질 수 없습니다.", "articles": [], "principle": "추정의 본질", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 상당 부분 추정, 판단 및 모형에 근거합니다.", "articles": [], "principle": "추정과 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의성을 줄이고 일관성을 높이기 위해 개념을 정립합니다.", "articles": [], "principle": "개념체계 역할", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "단일 공식을 전면 강제하지 않습니다.", "articles": [], "principle": "다양한 추정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "합리적 추정도 자산 인식 요건을 충족하면 인식합니다.", "articles": [], "principle": "인식 요건", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "개념체계가 규정하는 일반목적재무보고의 '주요 이용자(Primary Users)'의 특성과 한계에 관한 설명으로 옳지 않은 것은?",
        "options": [
          "① 주요이용자는 보고기업에 직접 정보를 요구할 권한이 없는 현재 및 잠재적 투자자, 대여자, 기타 채권자를 의미한다.",
          "② 보고기업의 경영진은 기업의 중요 정보를 내부에서 직접 획득할 수 있으므로 주요이용자에 해당하지 않는다.",
          "③ 정부 감독기관이나 일반 대중은 일반목적재무보고서를 유용하게 여길 수 있으나, 이들이 재무보고서가 표방하는 주요이용자는 아니다.",
          "④ 회계기준위원회는 회계기준 제정 시 주요이용자 개별 구성원의 특수한 정보 요구까지 모두 충족할 수 있도록 개별 재무제표 작성을 지시해야 한다.",
          "⑤ 일반목적재무보고서는 주요이용자가 필요로 하는 모든 정보를 완벽하게 제공하지는 못하며 제공할 수도 없다."
        ],
        "answer": "4",
        "explanation": "④ 회계기준위원회는 회계기준을 제정할 때 주요이용자 '최대 다수의 공통적인 수요'를 충족하는 정보를 제공하기 위해 노력합니다. 이용자 개별의 특수한 요구사항을 일일이 만족시키는 개별 재무제표를 지시하지 않습니다.\n\n[오답 해설]\n① 주요이용자의 올바른 정의입니다.\n② 경영진은 주요이용자 범위에서 제외됩니다.\n③ 감독기관이나 일반 대중은 주요 대상이 아닙니다.\n⑤ 재무보고서의 불가피한 내재적 한계에 대한 옳은 기술입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "주요이용자 정의에 대한 옳은 설명입니다.", "articles": [], "principle": "주요이용자 범위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "경영진 제외에 대한 옳은 설명입니다.", "articles": [], "principle": "경영진의 지위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기타 당사자 지위에 대한 옳은 설명입니다.", "articles": [], "principle": "기타 이해관계자", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개별적인 특수 정보 수요를 모두 반영한 보고서를 개별 작성하도록 유도하지는 않습니다.", "articles": [], "principle": "공통 정보수요", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "재무보고서의 한계성에 대한 옳은 설명입니다.", "articles": [], "principle": "재무보고서의 한계", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "개념체계상 일반목적재무보고서가 보고기업의 내재 가치(Value of Reporting Entity)에 대해 가지는 지위로 옳은 것은?",
        "options": [
          "① 보고서 상의 자본 합계액은 기업의 실제 인수합병 가치와 정확히 일치한다.",
          "② 재무보고서는 보고기업의 가치를 보여주기 위해 고안된 것이 아니다.",
          "③ 재무보고서는 보고기업의 실제 기업 가치를 보여주는 것을 최종 목표로 삼는다.",
          "④ 재무보고서는 미래 현금흐름 예측 정보를 완전히 차단하므로 가치 추정에 유용하지 않다.",
          "⑤ 개념체계는 경영진이 인위적으로 기업 가치를 극대화하여 공시하도록 기법을 제시한다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고서는 보고기업의 가치를 직접 보여주기 위해 고안된 것이 아닙니다. 그러나 주요이용자가 보고기업의 가치를 스스로 추정하는 데 도움을 주는 정보(재무상태, 성과 등)를 제공합니다.\n\n[오답 해설]\n① 자본 합계액과 실제 시장 가치(시가총액 등)는 일치하지 않습니다.\n③ 기업 가치의 직접 제시는 재무보고서의 고안 목적이 아닙니다.\n④ 재무보고서의 과거 성과 정보는 미래 현금흐름 추정에 유용한 자료가 됩니다.\n⑤ 가치 평가 극대화 기법을 제공하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "장부금액과 시장 가치는 통상 다릅니다.", "articles": [], "principle": "가치평가 괴리", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 기업의 가치를 직접 제시하기 위해 고안된 문서가 아닙니다.", "articles": [], "principle": "기업가치 추정 지원", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기업 가치 제시가 최종 목표가 아닙니다.", "articles": [], "principle": "보고서 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "미래 현금유입을 추정하는 유용한 정보를 포함합니다.", "articles": [], "principle": "유용한 정보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "인위적 가치 극대화 기법은 포함하지 않습니다.", "articles": [], "principle": "정직한 보고", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "일반목적재무보고서의 공통된 정보 수요(Common Information Needs) 충족 추구와 관련한 설명으로 옳은 것은?",
        "options": [
          "① 공통된 정보 수요에 초점을 맞추므로, 특정 일부 이용자에게 유용할 수 있는 추가 정보를 포함해서는 안 된다.",
          "② 공통된 정보 수요에 초점을 맞춘다고 해서 보고기업이 주요이용자의 특정 일부에게 유용한 추가 정보를 포함하지 못하게 하는 것은 아니다.",
          "③ 공통된 정보 수요란 전 세계 모든 주주의 개인별 요구사항의 평균치를 산출해 이에 부합하게 공시하는 제도이다.",
          "④ 모든 정보이용자는 동일한 직업적 전문성을 가지므로 정보 해독 수준에 맞춤식 변형 공시를 해야 한다.",
          "⑤ 공통 정보만을 제공하므로, 개별 산업(예: 은행, 건설업)의 특성을 반영한 특수 기준 공시는 절대 허용되지 않는다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고서는 다수 이용자의 공통된 정보 수요에 초점을 맞추지만, 이것이 특정 일부에게 매우 유용한 추가 정보를 재무보고서에 포함하는 것을 금지하지는 않습니다.\n\n[오답 해설]\n① 공통 정보 위주로 구성하되 필요한 추가 정보를 주석 등으로 제공하는 것이 허용됩니다.\n③ 개인 요구의 수학적 평균치를 산출하지 않습니다.\n④ 정보이용자들은 재무 정보 해독 능력이 다양하므로 공통 수준에 준하여 보고하되 복합 변형 공시를 자의적으로 남발하지 않습니다.\n⑤ 산업별 특성에 따른 특수 기준서 공시는 K-IFRS 하에서 얼마든지 조화를 이룹니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "추가 정보 기재를 차단하지 않습니다.", "articles": [], "principle": "추가정보 허용", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "공통 정보에 초점을 맞춘다고 해서 추가 정보를 포함하는 것을 금지하지는 않습니다.", "articles": [], "principle": "추가정보 기재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "수학적 평균 산출과 무관합니다.", "articles": [], "principle": "공통 정보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "정보 해독 지침은 정보이용자의 합리적 분석을 가정합니다.", "articles": [], "principle": "이용자의 지식수준", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "산업별 특수 공시를 배척하지 않습니다.", "articles": [], "principle": "산업별 보고", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "개념체계상 일반목적재무보고가 제공하는 기본 정보 유형에 해당하지 않는 것은?",
        "options": [
          "① 보고기업의 경제적자원 및 보고기업에 대한 청구권에 관한 정보",
          "② 보고기업의 경제적자원 및 청구권을 변동시키는 거래와 그 밖의 사건의 영향에 관한 정보",
          "③ 보고기업의 재무성과(발생주의 및 현금흐름 성과)에 관한 정보",
          "④ 재무성과에 기인하지 않은 경제적자원 및 청구권의 변동에 관한 정보",
          "⑤ 미래 시장 환경 변화를 정확하게 가정한 확정적 미래 손익 추정 보고서"
        ],
        "answer": "5",
        "explanation": "⑤ 개념체계는 과거의 사건과 거래가 경제적 자원 및 청구권에 준 영향과 발생주의 및 현금흐름 정보 등을 다루며, 미래 예측에 도움을 주지만 '확정적 미래 손익 추정 보고서'를 공식 정보 유형으로 직접 제공하거나 정확성을 담보하지 않습니다.\n\n[오답 해설]\n①, ②, ③, ④는 모두 개념체계가 공식 규정하고 있는 일반목적재무보고서의 필수적인 정보 제공 영역입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "경제적 자원 및 청구권 정보는 필수 제공 항목입니다.", "articles": [], "principle": "제공 정보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자원과 청구권의 변동 정보는 필수 제공 항목입니다.", "articles": [], "principle": "제공 정보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "재무성과 정보는 필수 제공 항목입니다.", "articles": [], "principle": "제공 정보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "성과 외의 원인에 따른 변동 정보는 필수 제공 항목입니다.", "articles": [], "principle": "제공 정보", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "확정적 미래 추정 보고서는 재무보고서가 제공하는 공식 정보에 포함되지 않습니다.", "articles": [], "principle": "미래 정보의 성격", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "발생주의 회계(Accrual Accounting)가 반영된 재무성과 정보의 유용성에 관한 개념체계의 설명으로 옳은 것은?",
        "options": [
          "① 한 기간 동안의 현금 수취와 지급에 국한된 정보보다 기업의 과거 및 미래 성과를 평가하는 데 더 나은 근거를 제공한다.",
          "② 발생주의 정보는 현금흐름 예측에 방해가 되므로 별도의 현금흐름 정보와 혼합하여 분석해서는 안 된다.",
          "③ 발생주의 정보는 오직 당기순이익의 계산에만 사용될 뿐, 경영진의 수탁책임(Stewardship) 평가에는 아무런 유용성이 없다.",
          "④ 발생주의 회계는 현금 거래가 아직 발생하지 않은 장기 미결제 거래의 인식은 전면 배제하여 안정성을 추구한다.",
          "⑤ 발생주의 회계 정보가 있으면 미래 순현금유입액 전망을 정확하게 확정할 수 있으므로 다른 어떠한 정성적 정보도 필요하지 않다."
        ],
        "answer": "1",
        "explanation": "① 발생기준 회계는 거래와 사건의 영향을 현금의 수령과 지급 시점과 관계없이 발생 기간에 표시하므로, 단순 현금흐름 정보보다 과거 및 미래 성과 평가와 수탁책임 평가에 훨씬 더 나은 근거를 제공합니다.\n\n[오답 해설]\n② 발생주의 정보와 현금흐름 정보는 상호보완적이며 함께 분석해야 효과적입니다.\n③ 경영진의 수탁책임 평가에도 유용한 정보를 제공한다고 명시되어 있습니다.\n④ 현금 결제가 미래에 이루어지더라도 해당 사건이 발생한 기간에 보여주어야 합니다.\n⑤ 미래 전망을 돕지만, 완벽한 확정을 해주거나 정성적 정보의 유용성을 배제하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "발생주의 회계 정보는 단순 현금 수급 정보보다 성과 평가에 우월한 유용성을 가집니다.", "articles": [], "principle": "발생주의의 유용성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "현금흐름 정보와 발생주의 정보는 상호보완적입니다.", "articles": [], "principle": "상호보완성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "수탁책임 평가에도 적극 활용됩니다.", "articles": [], "principle": "수탁책임 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "결제 시점과 무관하게 발생 시 인식합니다.", "articles": [], "principle": "발생주의 정의", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "미래를 완전히 확정 지어주지는 못합니다.", "articles": [], "principle": "발생주의 한계", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "개념체계상 '과거현금흐름(Past Cash Flows)'에 관한 정보가 가지는 고유한 가치로 옳은 것은?",
        "options": [
          "① 기업의 당기순이익이 자의적 추정 없이 100% 현금으로 실현되었음을 영구 보장한다.",
          "② 이용자가 기업의 미래 순현금유입 창출 능력을 평가하고 경영진의 수탁책임이 적절했는지 파악하는 데 도움을 준다.",
          "③ 발생주의 회계를 완전 대체하여 회계의 주류 모형을 현금주의로 원상 복구시키는 근거이다.",
          "④ 기업의 현재 보유 부동산의 시가를 가장 신속하게 포착하여 가치를 평가하도록 돕는다.",
          "⑤ 단기적 세무 체납 리스크의 면제 범위를 세무당국이 결정하도록 하는 유일한 척도이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 한 기간의 현금흐름 정보가 이용자들로 하여금 기업의 미래 순현금유입 창출 능력을 평가하고, 경제적 자원에 대한 경영진의 수탁책임을 평가하는 데 도움을 준다고 규정합니다.\n\n[오답 해설]\n① 당기순이익이 전액 현금 실현됨을 보장할 수 없습니다.\n③ 발생주의 회계를 대체하지 않고 현금흐름표 등에서 보완적으로 제공됩니다.\n④ 현금흐름은 실제 유출입 정보일 뿐 부동산 등 개별 자산의 공정가치 시가를 직접 제시하지 않습니다.\n⑤ 세무 면제 권한을 세무당국에 제공하는 문서가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "이익의 현금화 실현을 영구 보증할 수는 없습니다.", "articles": [], "principle": "현금흐름 한계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "미래 순현금유입 창출 능력 평가 및 수탁책임 평가에 도움을 줍니다.", "articles": [], "principle": "과거 현금흐름 유용성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "발생주의를 대체하지 않습니다.", "articles": [], "principle": "발생주의 유지", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "부동산 시가 평가와 무관합니다.", "articles": [], "principle": "자산 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세법 집행의 유일 척도가 아닙니다.", "articles": [], "principle": "세법 무관", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "개념체계가 외부감사인(External Auditor)에 대하여 제공하는 공식적인 역할로 옳은 것은?",
        "options": [
          "① 감사인이 기업에 수취해야 하는 적정 감사보수를 산정하는 법적 공식을 규율한다.",
          "② 감사인이 특정 회계처리에 대하여 감사보고서의 감사의견을 결정하는 과정에 법적 면책 특권을 부여한다.",
          "③ 모든 이해관계자(감사인 포함)가 한국채택국제회계기준(K-IFRS)을 올바르게 이해하고 해석하는 데 도움을 준다.",
          "④ 감사인이 기업 경영진의 업무를 직접 지시·통제하여 내부 경영을 대행하도록 대리 권한을 부여한다.",
          "⑤ 감사인에게 세무 세무조사 업무를 대행할 수 있는 과세당국의 특별 권한을 부여한다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계는 '모든 이해관계자가 회계기준을 이해하고 해석하는 데 도움을 준다'는 목적을 가집니다. 외부감사인 또한 이해관계자 중 하나이므로 감사 수행 시 기준서의 올바른 해석을 지원하는 데 도움을 받습니다.\n\n[오답 해설]\n① 감사보수 책정 공식을 규정하지 않습니다.\n② 법적 면책 특권을 부여하는 문서가 아닙니다.\n④ 감사인은 독립성을 유지해야 하므로 경영 대행 권한을 가질 수 없으며 개념체계도 이를 허용하지 않습니다.\n⑤ 감사인에게 과세당국의 세무조사 권한을 위임하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "감사보수 규정은 개념체계의 소관이 아닙니다.", "articles": [], "principle": "개념체계 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "법적 면책권과 무관합니다.", "articles": [], "principle": "감사 책임", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "감사인을 포함한 모든 이해관계자가 회계기준을 올바르게 이해하고 해석하는 데 유용합니다.", "articles": [], "principle": "해석 지원", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "경영진 업무 대리는 감사인의 독립성 위반입니다.", "articles": [], "principle": "감사 독립성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 세무조사 위임과 무관합니다.", "articles": [], "principle": "감사인의 권한", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },

    # =========================================================================
    # L3: 적용 및 상황 판단형 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s01-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "(시나리오) A사는 신종 블록체인 기반의 '가상 부동산 소유권' 거래를 개시하였으나, 현재 K-IFRS 기준서 중 해당 거래를 명시적으로 규정한 기준서가 없다. A사의 담당 회계사 김 과장이 회계정책을 수립하기 위해 취해야 할 행동으로 개념체계에 가장 부합하는 것은?",
        "options": [
          "① 관련 기준서가 없으므로 해당 가상 부동산 거래와 관련한 자산 및 부채를 회계장부에서 전액 생략하고 공시하지 않는다.",
          "② 일반목적재무보고의 목적과 질적 특성 등을 담은 개념체계의 내용을 참고하여 기업에 가장 유리하게 당기순이익이 극대화되는 회계정책을 수립한다.",
          "③ 개념체계의 원칙과 요소 정의를 참고하여, 정보이용자에게 유용하고 일관된 회계정책을 자체적으로 개발하여 적용한다.",
          "④ 한국회계기준위원회에 서면 질의를 보내 정식 기준서가 제정되어 공표될 때까지 회계 처리를 3년간 전면 유예한다.",
          "⑤ 타사나 미국회계기준(US-GAAP) 중 A사의 법인세를 가장 적게 발생시키는 규정을 임의 혼용하여 정책을 수립한다."
        ],
        "answer": "3",
        "explanation": "③ 개념체계는 특정 거래나 다른 사건에 적용할 회계기준이 없는 경우에 재무제표 작성자가 일관된 회계정책을 개발하는 데 도움을 주고자 고안되었습니다. 작성자는 개념체계의 목적과 원칙에 부합하는 일관된 정책을 개발하여 적용해야 합니다.\n\n[오답 해설]\n① 기준서가 없다고 공시를 전면 생략하는 것은 타당하지 않습니다.\n②, ⑤ 기업의 순이익 극대화나 법인세 최소화 등 자의적이거나 조세회피 목적의 회계정책 수립은 허용되지 않습니다.\n④ 공식 기준서 공표 시까지 장기간 회계 처리를 보류하는 것은 허용되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "공시 생략은 투명성을 훼손합니다.", "articles": [], "principle": "회계정책 수립", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "이익 임의 극대화 목적의 정책 수립은 불가합니다.", "articles": [], "principle": "회계정책 수립", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서 부재 시 개념체계에 근거한 일관되고 유용한 정책을 작성자가 개발하여 적용해야 합니다.", "articles": [], "principle": "작성자 회계정책 개발", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "회계 처리를 장기간 유예하는 것은 적절하지 않습니다.", "articles": [], "principle": "회계정책 수립", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "법인세 최소화 목적의 자의적 혼용은 불가합니다.", "articles": [], "principle": "회계정책 수립", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "(시나리오) B사는 기계장치의 후속 측정에 있어 K-IFRS 기준서 제1016호에 따라 '원가모형'과 '재평가모형' 중 하나를 선택할 수 있는 대안을 가지고 있다. B사의 이 회계사무관이 기업의 회계 일관성을 지키기 위해 개념체계의 목적에 비추어 행동하는 방식으로 가장 적절한 것은?",
        "options": [
          "① 매년 기말 주가 및 실적에 따라 당기순이익에 유리하도록 모형을 매번 바꾸어 선택 적용한다.",
          "② 회계정책의 선택이 허용되는 경우이므로, 정보이용자의 비교가능성과 목적적합성을 높일 수 있는 일관된 회계정책을 수립하고 준수한다.",
          "③ 감사인이 지목하는 하나의 모형만을 선택하고, 회계정책 수립의 모든 책임을 감사인에게 서면으로 전가한다.",
          "④ 선택 대안이 있는 경우 회계장부의 오류를 차단하기 위해 기계장치 자산 자체를 장부에서 제거하고 비용으로 전액 일시 처리한다.",
          "⑤ 두 모형의 장부 가치 평균값을 산출하여 매년 임의의 잡손실 항목으로 장부에 기록한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계의 두 번째 목적은 회계기준에서 회계정책을 선택하는 것을 허용하는 경우에 재무제표 작성자가 일관된 회계정책을 개발하여 유용한 정보를 제공하도록 돕는 것입니다. 따라서 일관성과 유용성을 갖추어 수립해야 합니다.\n\n[오답 해설]\n① 모형을 매년 자의적으로 번복하면 비교가능성이 심각하게 저해됩니다.\n③ 감사인은 조력자일 뿐 회계정책 수립의 최종 책임은 경영진(작성자)에게 있습니다.\n④, ⑤ 규정에 없는 자의적인 비용 처리나 평균값 잡손실 반영 등은 명백한 분식회계이자 오류입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "매년 임의 변경은 정보의 신뢰성과 일관성을 저해합니다.", "articles": [], "principle": "회계정책 선택", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "정책 선택권 허용 시 개념체계 목적에 비추어 일관되고 유용한 정책을 자체 수립해야 합니다.", "articles": [], "principle": "작성자 회계정책 개발", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "회계정책 수립 책임은 기업 경영진에 있습니다.", "articles": [], "principle": "작성자 책임", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의의 자산 제거는 심각한 오류입니다.", "articles": [], "principle": "자산 인식", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의 평균 잡손실 기록은 부적절합니다.", "articles": [], "principle": "회계 오류", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "(시나리오) C사의 외부감사인인 한 회계사는 '개념체계 상의 자산 정의'가 'K-IFRS 특정 기준서의 부채 평가 규정'보다 논리적으로 훨씬 우월하므로, 기준서 규정을 배제하고 개념체계의 정의에 따라 기말 재무상태표를 수정해야 한다고 C사 재무팀에 강하게 요구하였다. 이에 대한 C사 재무팀의 대응 지침으로 가장 올바른 판단은?",
        "options": [
          "① 감사인의 전문적 권고를 적극 수용하여 K-IFRS 기준서 대신 개념체계를 우선 적용하여 수정한다.",
          "② 감사인의 요구를 거부하고 K-IFRS의 규정을 그대로 고수한다. 개념체계는 회계기준이 아니므로 기준서에 우선할 수 없기 때문이다.",
          "③ 상충이 발견되었으므로 수정 전 재무제표를 공시하지 않고 세무회계 기준에 따라 작성한 재무제표로 대체하여 공시한다.",
          "④ 개념체계와 기준서가 상충할 때에는 두 수치의 산술 평균값을 산출하여 주석에만 공시한다.",
          "⑤ 개념체계와 상충하는 특정 기준서는 효력이 상실된 상태이므로, 감사인과 함께 회계기준위원회에 즉시 징계를 청구한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준(기준서)이 아니며, 개념체계의 어떠한 내용도 특정 회계기준이나 그 요구사항에 우선하지 않습니다. 상충하는 경우 기준서의 규정을 엄격히 따라야 하므로 감사인의 주장은 잘못되었습니다.\n\n[오답 해설]\n① 개념체계는 기준서에 우선할 수 없습니다.\n③ 세무회계 기준으로 재무제표를 대체 공시할 수 없습니다.\n④ 산술 평균값을 취하거나 임의 기재하는 것은 명백한 기준서 위반입니다.\n⑤ 일탈된 기준서도 법적 강제력을 지닌 유효한 기준서이므로 징계 청구의 대상이 될 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "감사인의 오독이며, 개념체계는 기준서에 우선할 수 없습니다.", "articles": [], "principle": "개념체계 위상", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계의 어떠한 규정도 기준서의 규정에 우선하지 않으므로 기준서 규정을 고수해야 합니다.", "articles": [], "principle": "개념체계 위상 및 효력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무회계 대체 공시는 불가합니다.", "articles": [], "principle": "재무제표 공시", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "평균값 계상은 허용되지 않습니다.", "articles": [], "principle": "상충 처리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기준서는 유효한 효력을 가집니다.", "articles": [], "principle": "기준서 효력", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "(시나리오) D사는 다년간 기계장치의 처분과 관련하여 기존 K-IFRS 기준서의 지침에 따라 정상적으로 회계처리를 해왔다. 최근 회계기준위원회가 개념체계 중 자산의 제거 관련 파트를 대대적으로 개정하였다. D사의 박 회계사가 이번 개념체계 개정에 맞추어 회계 처리에 반영해야 할 태도로 옳은 것은?",
        "options": [
          "① 개념체계가 개정되었으므로, 관련 기존 회계기준이 공식 개정되지 않았더라도 즉시 변경된 개념체계에 맞추어 처분 손익을 전액 소급 수정해야 한다.",
          "② 개념체계의 개정은 기존 회계기준을 자동으로 개정시키는 것이 아니므로, 기존 회계기준이 공식 개정되기 전까지는 기존 기준서에 따라 회계처리를 정당하게 유지한다.",
          "③ 개념체계가 개정되는 즉시 기존 처분 거래에 관한 모든 전표를 파기하고 신종 가상 거래로 임의 재분류해야 한다.",
          "④ 개념체계 개정일 이후 발생한 모든 처분 거래에 대하여 회계기준이 개정될 때까지 장부 기록을 전면 유예한다.",
          "⑤ 기존 회계기준서와 개정 개념체계가 상충하므로, 즉시 양 규정을 절반씩 절충한 자의적인 처분 회계 처리를 수행한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계가 수시로 개정될 수 있지만, 개념체계가 개정되었다고 해서 자동으로 기존 회계기준이 개정되는 것은 아닙니다. 따라서 기존 기준서가 적법하게 변경되기 전까지는 해당 기준서에 따라 처분 회계처리를 지속해야 합니다.\n\n[오답 해설]\n① 개념체계 개정만으로 기준서 미개정 상태에서 소급 수정을 해서는 안 됩니다.\n③ 전표 파기 및 임의 재분류는 심각한 분식회계입니다.\n④ 회계 기록 유예는 적시성 및 성실 보고 의무 위반입니다.\n⑤ 자의적인 절충 처리는 허용되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기준서 개정 전 소급 수정은 잘못입니다.", "articles": [], "principle": "개념체계 개정 영향", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계의 개정이 기존 회계기준을 자동으로 변경하지 않으므로 기존 기준서를 따라야 합니다.", "articles": [], "principle": "자동개정 불인정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "전표 파기는 불법행위입니다.", "articles": [], "principle": "장부 관리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기록 유예는 허용되지 않습니다.", "articles": [], "principle": "회계 기록 의무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적 절충 회계는 불가합니다.", "articles": [], "principle": "회계 오류", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "(시나리오) 한국회계기준위원회는 일반목적재무보고의 특수한 목적 달성을 위해 특정 금융상품 기준서를 제정하면서, 부득이하게 개념체계의 자산 정의 범위에서 명백히 벗어난 일탈 규정을 포함시켰다. 이 상황에서 위원회가 개념체계에 따라 취해야 할 후속 공시 행동으로 옳은 것은?",
        "options": [
          "① 해당 일탈 상황이 주주들의 신뢰를 떨어뜨리므로 이를 비공개 보안 안건으로 처리하여 대외 유출을 철저히 차단한다.",
          "② 해당 기준서의 '결론도출근거(Basis for Conclusions)'에 그러한 개념체계로부터의 일탈에 대해 명확히 설명한다.",
          "③ 일탈을 해소하기 위해 해당 기준서의 요구사항을 다음 달에 즉시 무효화하고 폐기 공고를 낸다.",
          "④ 금융감독원장이 직권으로 개념체계의 원칙을 일시 무력화시키는 특별 승인 명령을 내리도록 요청한다.",
          "⑤ 기준서 본문에서 개념체계와 상충이 없다는 취지의 가짜 설명문을 조작하여 삽입한다."
        ],
        "answer": "2",
        "explanation": "② 일반목적 재무보고의 목적을 달성하기 위해 회계기준위원회가 개념체계의 관점에서 벗어난 요구사항을 정하는 경우가 있을 수 있으며, 만약 그러한 사항을 정한다면 해당 기준서의 결론도출근거에 그러한 일탈에 대해 설명해야 합니다.\n\n[오답 해설]\n① 비공개 보안 안건으로 은폐하는 것은 불가능합니다.\n③ 무효화하거나 기준서를 바로 폐기하지 않습니다.\n④ 금융감독원장의 직권 승인 요청은 공식 절차가 아닙니다.\n⑤ 허위 조작 기재는 허용되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "비공개 처리는 투명성 원칙에 반합니다.", "articles": [], "principle": "정보 공개", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서의 결론도출근거에 그러한 개념체계로부터의 일탈 사실과 이유를 설명해야 합니다.", "articles": [], "principle": "결론도출근거 일탈 기재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기준서 폐기는 불필요합니다.", "articles": [], "principle": "기준서 효력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "금감원장의 직권 명령 대상이 아닙니다.", "articles": [], "principle": "기준 제정 권한", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "허위 진술 기재는 불가합니다.", "articles": [], "principle": "정보 정직성", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "(시나리오) 투자자 E는 재무상태표의 자본 합계(Net Assets)가 100억 원인 F사의 주식을 매수하려고 검토 중이다. F사의 실제 시가총액은 약 250억 원에 이른다. 투자자 E가 개념체계상의 일반목적재무보고서 성격을 바르게 이해하고 내린 판단으로 가장 적절한 것은?",
        "options": [
          "① F사의 재무제표 자본 총계가 100억 원이므로 시가총액 250억 원과의 차이인 150억 원은 명백한 분식회계이자 회계 누락의 증거이다.",
          "② 일반목적재무보고서는 보고기업의 가치를 직접 보여주기 위해 고안된 것이 아니므로 장부금액이 기업 가치와 일치할 필요는 없으며, F사의 가치 추정을 위한 유용한 정보를 제공한다.",
          "③ F사의 재무보고서는 150억 원만큼 과소평가된 오류를 범하고 있으므로 회계기준위원회에 즉시 시정 조치 명령을 청구해야 한다.",
          "④ 시가총액과 장부금액의 불일치를 해소하기 위해 F사 재무팀에게 기말 재무제표 상의 자산 가액을 강제로 150억 원만큼 소급 상향 조정하게 권고한다.",
          "⑤ 재무보고서가 가치를 보여주지 못하므로 F사의 이번 기말 재무보고서는 완전히 신뢰할 수 없는 무용지물이다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고서는 보고기업의 가치를 보여주기 위해 고안된 것이 아닙니다. 그러나 투자자 등이 보고기업의 가치를 스스로 추정하는 데 유용한 정보(예: 경제적 자원의 상태, 성과 추이 등)를 충분히 제공합니다.\n\n[오답 해설]\n①, ③, ④ 장부금액(순자산)과 시장 가치(시가총액)의 괴리는 정상적인 회계적 결과이며, 오류나 분식회계가 아닙니다.\n⑤ 가치를 보여주기 위해 고안되지 않았을 뿐, 가치를 '추정'하기 위한 핵심적 기초 자료를 제공하므로 유용합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "가치 괴리는 분식회계의 결과가 아닙니다.", "articles": [], "principle": "가치 괴리", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 가치를 직접 보여주지 않으며, 가치를 추정하는 유용한 재무 정보를 제공할 뿐입니다.", "articles": [], "principle": "기업가치 추정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "위원회 시정조치 대상이 아닙니다.", "articles": [], "principle": "회계적 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장부가액의 강제 시가 매칭 수정은 불가합니다.", "articles": [], "principle": "자산 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "가치를 직접 보여주지 않는다고 해서 무용한 보고서는 아닙니다.", "articles": [], "principle": "보고서의 유용성", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "(시나리오) 다국적 대기업 G사는 과거에 국가별로 상이한 회계 개념에 기초하여 재무제표를 개별 작성하여 공시해왔다. 최근 개념체계에 완전히 기반한 단일의 국제 회계 언어(K-IFRS)를 일괄 도입하기로 결정하였다. G사가 얻게 될 자본시장 효율성(Efficiency)적 이득으로 가장 적절한 것은?",
        "options": [
          "① G사의 모든 사업장의 법인세가 완전 면제되어 세금 지출이 즉시 0원이 된다.",
          "② 투자자에게 기회와 위험을 효과적으로 전달하여 전 세계적인 자본 배분을 향상시키며, 자본비용 및 국제보고 비용을 실질적으로 감소시킨다.",
          "③ 전 세계 주식시장에서 G사의 주가가 매년 무조건 20%씩 강제 상승하는 효과를 낸다.",
          "④ 국가별 세무조사에서 G사의 모든 자회사들이 세무 조정을 회피할 수 있는 완전 면책 효력을 보장받는다.",
          "⑤ 단일 회계 언어 사용으로 내부 재무 직원을 전원 해고하여 인건비를 100% 절감한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 단일의 신뢰성 있는 회계 언어(개념체계에 기반한 회계기준)의 사용이 정보의 국제적 비교가능성을 높이고, 전 세계 자본 배분의 효율성에 기여하며, 궁극적으로 자본비용 감소 및 국제보고 비용 절감을 가능케 한다고 명시합니다.\n\n[오답 해설]\n① 법인세 면제 효력을 갖지 않습니다.\n③ 주가 상승을 보장하는 규정은 시장에 존재하지 않습니다.\n④ 세무조사 회피나 세법 면책과 무관합니다.\n⑤ 재무 직원의 전원 해고 등 고용 정책의 수단이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "조세 경감과 무관합니다.", "articles": [], "principle": "세법 무관", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "단일 회계 언어 사용으로 전 세계 자본 배분을 돕고 자본비용을 경감시킵니다.", "articles": [], "principle": "자본비용 절감", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주가 상승 보장과 무관합니다.", "articles": [], "principle": "주가 영향", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 조사 회피와 무관합니다.", "articles": [], "principle": "세무 조사", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "인건비의 100% 절감과 무관합니다.", "articles": [], "principle": "인적 자원", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "(시나리오) H사의 자산 중 상당 부분은 기말 현재 회수가 불확실한 '소송 채권'으로 구성되어 있어 정확한 회수액을 확정할 수 없다. H사의 회계팀 최 대리는 이 채권의 기말 평가 시 상당한 추정(Estimation)과 모형(Models)을 사용할 수밖에 없다. 최 대리가 개념체계의 지침에 부합하게 내린 결론으로 옳은 것은?",
        "options": [
          "① 추정치와 모형을 사용한 재무보고서는 신뢰성이 상실되므로, 개념체계를 준수하기 위해 재무보고서 작성을 즉시 거부해야 한다.",
          "② 재무보고서는 상당 부분 정확한 서술보다 추정, 판단 및 모형에 근거하므로, 개념체계가 정한 개념적 기초 위에서 합리적으로 추정하여 보고한다.",
          "③ 소송 채권의 회수율을 자의적으로 100%로 가정하여 자산 규모를 최대한 과대 포장하여 보고한다.",
          "④ 모형의 유용성을 배제하기 위해 오직 현금의 수령이 확인된 극히 일부분만 현금주의 방식으로 채권을 자산 인식한다.",
          "⑤ 추정치를 기재하는 대신 소송 가액 전액을 부외자산으로 처리해 숨겨 둔다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 재무보고서가 정확한 서술보다는 상당 부분 추정, 판단 및 모형에 근거하며, 개념체계는 그 추정 등의 기초가 되는 개념을 정함을 기술하고 있습니다. 따라서 합리적 추정을 통한 보고가 개념체계에 부합합니다.\n\n[오답 해설]\n① 추정치 사용을 이유로 보고서 작성을 거부할 수 없습니다.\n③ 자의적인 100% 과대 포장은 분식회계입니다.\n④ 현금주의로 자의적 대체하여 발생주의를 훼손해서는 안 됩니다.\n⑤ 고의적인 부외자산 은폐는 불법입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "추정이 불가피하므로 보고서 작성을 거부해서는 안 됩니다.", "articles": [], "principle": "추정의 불가피성", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 상당 부분 추정과 판단에 근거하며 합리적 기초 위에서 보고되어야 합니다.", "articles": [], "principle": "추정치 공시", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적인 과대평가는 불가합니다.", "articles": [], "principle": "합리적 추정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "현금주의로 임의 전환해서는 안 됩니다.", "articles": [], "principle": "발생주의 적용", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자산 은폐는 허용되지 않습니다.", "articles": [], "principle": "부외자산 금지", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "(시나리오) 주주 J는 K사가 최근 공시한 일반목적재무보고서 외에, K사의 경영진이 보유한 '차세대 핵심 신약의 임상3상 진행 상황 세부 정성 데이터'를 일반목적재무보고서가 왜 포함하고 있지 않은지 재무 부서에 강력히 항의하였다. K사 재무팀의 방어 논리 중 개념체계에 가장 잘 부합하는 것은?",
        "options": [
          "① 해당 데이터가 유출되면 경쟁사에 기술이 이전되므로, 개념체계의 영업기밀보호 강제 원칙에 따라 데이터 기재를 원천 거부한다.",
          "② 일반목적재무보고서는 주요이용자가 필요로 하는 모든 정보를 제공하지는 않으며 제공할 수도 없다. 다만 다수 이용자의 공통 정보 수요를 반영한 한계가 존재한다.",
          "③ 주주 J의 개인적 항의가 있으므로, 주주 J에게만 비밀리에 해당 데이터를 담은 개별 재무제표를 소급 재작성하여 우편 발송한다.",
          "④ 해당 세부 임상 정보는 기업 가치를 직접 보여주는 수치이므로 재무상태표의 무형자산 항목에 임의의 50억 원으로 바로 인식했어야 했다.",
          "⑤ 재무보고서가 아닌 세무보고서에만 해당 내용을 상세히 수록할 수 있게 세법 규정을 준수하였다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고서는 현재 및 잠재적 투자자 등이 필요로 하는 모든 정보를 제공하지 않으며 제공할 수도 없음을 개념체계는 명시하고 있습니다. 주요이용자 최대 다수의 공통 정보 수요에 맞춘 결과물입니다.\n\n[오답 해설]\n① 개념체계에는 영업기밀보호 강제 원칙이라는 세부 원칙은 없습니다.\n③ 특정 주주 1인에게만 특혜적인 개별 보고서를 별도 작성하지 않습니다.\n④ 미확정 임상 정보의 임의 자산화 계상은 불가합니다.\n⑤ 세무보고서의 규정에 대한 개념체계 지침이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "영업기밀 규정은 개념체계의 직접적 규정이 아닙니다.", "articles": [], "principle": "개념체계 내용", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "일반목적재무보고서는 주요이용자가 요구하는 모든 정보를 제공할 수 없는 내재적 한계를 가집니다.", "articles": [], "principle": "재무보고서의 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개별적인 정보 차별 제공은 불가합니다.", "articles": [], "principle": "공평 공시", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의의 무형자산 계상은 분식회계입니다.", "articles": [], "principle": "자산 인식", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무보고서 규정과 무관합니다.", "articles": [], "principle": "세무 보고", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "(시나리오) M사는 최근 공시된 재무제표 상에서 '제조부문 생산설비'를 전년도에 이어 계속하여 K-IFRS 기준서에 부합하게 성실하게 처리하였다. 그러나 국세청 세무조사관 L은 세법상의 세무조정 상각 범위액 계산 방식과 M사의 감가상각 누계액 계산이 상충된다며 재무제표의 감가상각비를 전액 세법 기준대로 수정공시할 것을 지시했다. M사 재무 부장의 대응 중 개념체계에 비추어 올바른 판단은?",
        "options": [
          "① 국세청의 세무조정 지시는 기업 공시에도 우선하므로 재무제표의 감가상각비를 국세청 지시대로 즉시 소급 수정 공시한다.",
          "② 재무제표는 세법이 아닌 K-IFRS 기준서에 부합하게 일관되게 공시하며, 세법과의 차이는 세무조정 계산서 및 법인세회계(이연법인세)를 통해 해소해야 한다.",
          "③ 감사인과 협의하여 기말 감가상각비를 세법과 회계기준의 정중앙 값으로 임의 절충하여 다시 공시한다.",
          "④ 세법과 상충하는 상황이 발생했으므로 당해 재무제표 전체를 파기하고 공시를 즉시 철회한다.",
          "⑤ 회계기준위원회에 서한을 보내 국세청의 법인세법 감가상각 규정을 개념체계에 무조건 강제 통합시킬 것을 공식 요구한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 및 재무보고는 일반목적 재무보고를 목적으로 하며, 세법 상의 세무 조정을 직접 재무제표에 반영하여 기준서를 위반하게 하지 않습니다. 세법과의 일시적 차이는 세무조정 및 법인세회계를 통해 처리하는 것이 올바릅니다.\n\n[오답 해설]\n① 재무제표 작성 기준은 K-IFRS 기준서이며 세법 규정이 재무제표 공시 기준을 임의로 대체할 수 없습니다.\n③ 자의적인 정중앙 값 절충은 금지됩니다.\n④ 공시 철회 사유에 해당하지 않습니다.\n⑤ 세법은 국회가 제정하므로 회계기준위원회가 개념체계에 강제 통합할 권한이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "세법을 이유로 K-IFRS를 위반할 수 없습니다.", "articles": [], "principle": "회계기준의 지위", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무제표는 회계기준에 따라 작성하며 세법과의 차이는 세무조정으로 조율합니다.", "articles": [], "principle": "세무와 회계의 구분", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의의 수치 절충은 회계 오류입니다.", "articles": [], "principle": "회계 처리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "공시 전면 철회는 불가합니다.", "articles": [], "principle": "공시 유지", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세법 통합 요구는 실현 불가능한 조치입니다.", "articles": [], "principle": "법적 독립성", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "(시나리오) 회계학 전공자 N은 감정평가사 1차 회계학 공부를 하던 중, 개념체계가 K-IFRS와 일부 배치되는 문장을 포함하고 있음을 식별했다. N이 개념체계의 위상에 근거하여 내린 학습 결론 중 옳은 것은?",
        "options": [
          "① 시험에 두 규정이 동시에 다른 내용으로 출제된다면, 무조건 개념체계를 정답 기준으로 삼아 문제를 풀어야 한다.",
          "② 개념체계의 어떠한 내용도 특정 기준서나 그 요구사항에 우선하지 않으므로, 세부 회계처리에 있어서는 특정 기준서(K-IFRS)의 요구사항을 최우선 기준으로 공부해야 한다.",
          "③ 개념체계에 맞지 않는 잘못된 기준서는 자동으로 효력이 무효화되었으므로 시험 범위에서 제외된다.",
          "④ 개념체계가 기준서와 상충하는 경우 재무제표 작성자는 자율 선택이 가능하므로 정답이 복수 정답 처리된다.",
          "⑤ 두 규정의 상충 시 개념체계의 역사가 더 오래되었으므로 항상 개념체계를 형법 상 정당방위 원칙에 따라 우선시해야 한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준이 아닙니다. 따라서 개념체계의 어떠한 내용도 특정 회계기준이나 요구사항에 우선하지 않습니다. 실제 회계처리는 기준서가 정한 바를 최우선 따라야 합니다.\n\n[오답 해설]\n① 기준서가 정답의 최우선 기준이 됩니다.\n③ 일탈된 기준서도 유효하므로 시험 범위에 당연히 포함됩니다.\n④ 작성자의 자율 선택권은 없으며 기준서 준수가 의무입니다.\n⑤ 형법 상의 정당방위 원칙 등은 회계 처리 우선순위와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "개념체계가 시험의 회계처리 기준보다 우선하지 않습니다.", "articles": [], "principle": "시험 정답 기준", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계는 회계기준이 아니며 특정 회계기준의 요구사항에 우선하지 않습니다.", "articles": [], "principle": "개념체계와 회계기준 관계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "일탈 기준서도 명백히 유효합니다.", "articles": [], "principle": "기준서 효력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "선택권 부재로 복수정답 사유가 아닙니다.", "articles": [], "principle": "복수정답 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "형법 원칙 적용 주장은 부적절합니다.", "articles": [], "principle": "법규 매핑", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "(시나리오) 대주주 O는 자신이 투자한 P사의 경영진이 올해 기계장치 구매 등의 대형 투자를 감행하여 막대한 '당기순손실'을 기록한 것에 대해 분노했다. O는 재무제표상 손실액이 과다하므로 경영진을 수탁책임 방기로 고소하기 위해 일반목적재무보고서를 분석하고 있다. P사 재무팀이 개념체계에 비추어 O의 오해를 풀어주기 위해 설명할 수 있는 적절한 근거는?",
        "options": [
          "① 당기순손실은 단지 장부상의 가짜 수치일 뿐이며, 경영진은 주주의 간섭 없이 자유롭게 현금을 탕진할 권리가 있다.",
          "② 재무보고서는 경영진의 책임을 묻기 위해 필요한 객관적 정보를 제공할 뿐이며, 손실의 발생 사유(대형 투자에 따른 미래 성장 기반 등)를 다각도로 평가할 수 있는 유용한 성과 및 과거 현금흐름 자료를 함께 제공한다.",
          "③ 대주주의 화를 풀기 위해 올해 발생한 기계장치 구매비를 자산이 아닌 자본 잉여금 증가로 임의 조작해 손실을 지워 주기로 제안한다.",
          "④ 손실이 발생했으므로 개념체계의 즉각 폐기 조항에 따라 올해 회계장부를 전면 백지화한다.",
          "⑤ 손실을 숨기기 위해 해당 보고서를 일반목적재무보고서가 아닌 특수비밀보고서로 명칭을 즉시 변경 공시한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 자본제공자들에게 경영진의 수탁책임을 평가할 수 있는 정보를 제공하는 것을 핵심 목적으로 삼고 있습니다. 당기순손실 등 성과 정보와 현금흐름 정보는 단순히 손실 여부를 넘어 경영진의 의사결정 타당성을 올바르게 평가하는 유기적 근거가 됩니다.\n\n[오답 해설]\n① 경영진에게 독점적 현금 탕진 재량권이 있지 않습니다.\n③, ⑤ 인위적인 자본 조작이나 비밀보고서 변경 등은 범죄행위입니다.\n④ 손실이 발생했다고 장부를 백지화하는 것은 불가합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "경영진의 무제한 탕진 권리는 없습니다.", "articles": [], "principle": "경영 책임", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "보고서는 수탁책임 평가를 위해 필요한 정보(성과 및 자원 변동 등)를 투명하게 제공합니다.", "articles": [], "principle": "수탁책임 정보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의의 자본 변경 조작은 회계 범죄입니다.", "articles": [], "principle": "분식 회계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장부 백지화는 불가능합니다.", "articles": [], "principle": "장부 작성 의무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의의 비밀보고서 변경은 불법입니다.", "articles": [], "principle": "비밀주의 금지", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "(시나리오) 감사위원회 위원 R은 기업의 기말 결산 보고 회의에서, 회사 소속 회계사들이 개념체계를 충분히 검토하지 않은 상태에서 복잡한 금융보증 계약 회계처리를 자의적으로 처리했다고 의심하였다. R이 회사의 재무 정보 신뢰성을 담보하기 위해 취할 수 있는 개념체계에 비추어 올바른 시정 지시로 옳은 것은?",
        "options": [
          "① 관련 금융보증 회계처리를 무조건 자본이 아닌 기말 잡손실로 전액 일괄 계상하여 회계처리를 마감하게 명령한다.",
          "② 관련 보증 거래에 딱 맞는 세부 기준서가 없더라도, 회계사들이 개념체계의 근본 원칙과 자산·부채 정의에 기초하여 일관된 회계정책을 적용해 회계 처리했는지 검토하게 한다.",
          "③ 금융보증에 대한 미국 회계처리를 여과 없이 무단 표절하여 적용하고 주석을 공란으로 처리하라고 지시한다.",
          "④ 결산 보고 마감을 6개월 뒤로 강제 연기하고 회계 부서에 벌금을 부과한다.",
          "⑤ 회사의 장부 기록 일체를 지워 감사위원회가 자체 작성한 비밀 장부로 기말 보고를 대체하게 한다."
        ],
        "answer": "2",
        "explanation": "② 특정 사건에 적용할 구체적인 기준서가 모호하거나 정책 선택이 필요한 경우 작성자(회계사)가 개념체계를 참조하여 일관되고 유용한 정책을 정립하여 처리해야 합니다. 감사위원회는 이러한 부합 여부를 검토하도록 지시하는 것이 타당합니다.\n\n[오답 해설]\n① 자의적인 잡손실 일괄 계상은 회계 기준 위반입니다.\n③ 주석 공란 처리 및 무단 표절은 부적절합니다.\n④ 결산 연기 및 자의적 벌금 부과는 법적 권한 밖의 행동입니다.\n⑤ 비밀 장부로 보고를 대체하는 것은 심각한 위법 행위입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "자의적 일괄 비용 처리는 부적절합니다.", "articles": [], "principle": "회계 정책", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "세부 규정 부재 시 개념체계의 목적과 요소 정의에 따라 일관되게 처리했는지 확인하는 것은 타당합니다.", "articles": [], "principle": "작성자 회계정책 검토", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주석 공란 등은 공시 위반입니다.", "articles": [], "principle": "공시의 충실성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의의 결산 연기 명령 권한은 없습니다.", "articles": [], "principle": "의사 결정 절차", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "비밀장부 대체는 위법입니다.", "articles": [], "principle": "장부 투명성", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "(시나리오) T사는 사업 극심한 부진으로 인해 법원으로부터 회생 불가 판정을 받고 다음 달 청산(Liquidation) 절차를 앞두고 있다. T사의 기말 재무제표 작성자인 강 대리가 이번 결산 시 재무보고 목적에 근거해 내려야 할 회계적 판단으로 가장 올바른 것은?",
        "options": [
          "① 다음 달에 청산할 예정이지만 개념체계상 계속기업가정은 절대 불변의 원칙이므로 평소대로 정상적인 역사적 원가 감가상각 처리를 고수한다.",
          "② 청산 예정인 기업이므로 개념체계상 '계속기업가정(Going Concern)'이 더 이상 유지될 수 없음을 반영하여, 자산과 부채를 청산가치(순실현가능가치 등)로 적절히 평가하여 작성해야 한다.",
          "③ 청산 확정이므로 올해분 결산 재무제표 작성 자체를 전면 거부하고 공시하지 않는다.",
          "④ 자산 금액 전체를 0원으로 수정하여 주주들에게 전액 손실로 마감 보고한다.",
          "⑤ 세무서에 전화하여 청산 관련 법인세를 면제해 주면 계속기업 기준의 장부를 작성하겠다고 협상한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 일반적으로 계속기업가정 하에 재무제표가 작성됨을 전제하지만, 청산이 임박하거나 경영 활동을 중단해야 할 불가피한 상황인 경우 계속기업 전제를 배제하고 청산가치 등 별도의 보고 기준에 따라 유용하게 작성하여야 함을 내포합니다.\n\n[오답 해설]\n① 청산 예정임에도 계속기업가정을 억지로 고수하여 장부를 조작하면 유용성이 훼손됩니다.\n③ 결산 작성을 거부하는 것은 불가능합니다.\n④ 자산을 즉각 0원으로 인위적으로 지우는 것은 타당하지 않습니다.\n⑤ 세무서와의 협상 카드로 회계 원칙을 변경하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "청산 예정인 경우 계속기업을 전제하면 안 됩니다.", "articles": [], "principle": "계속기업 배제", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "계속기업 가정이 성립하지 않으면 대체적인 기준(청산가치 등)에 따라 재무제표를 적절히 작성해야 합니다.", "articles": [], "principle": "계속기업가정의 예외", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "공시 거부는 불가합니다.", "articles": [], "principle": "결산 공시", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "인위적 0원 계상은 오기입니다.", "articles": [], "principle": "자산 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 협상 대상이 아닙니다.", "articles": [], "principle": "협상 부재", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "(시나리오) 회계감사 기법을 연구하는 대학원생 Y는 한국회계기준원(KASB)의 공식 홈페이지에서 개념체계와 K-IFRS 기준서의 히스토리를 분석하고 있다. Y가 연구 리포트에 작성할 개념체계와 기준서 제·개정 프로세스의 특성으로 옳은 것은?",
        "options": [
          "① 회계기준위원회는 전 세계 시장에 투명성, 책임성, 효율성을 제공하기 위한 기반으로 개념체계를 제정하여 운영하며, 개념체계는 기준서 제·개정의 정당한 개념적 기반을 이룬다.",
          "② 개념체계는 회계기준위원회의 공식 임무와 완전히 결별하여 작성되는 독립적인 단순 학술 논문이다.",
          "③ 기준서를 제정할 때 개념체계를 절대 참고하지 못하도록 규율하는 엄격한 보안 프로토콜이 존재한다.",
          "④ 개념체계는 수시 개정이 불가하도록 법적으로 금지되어 있어 최초 제정된 형태가 영구 고정된다.",
          "⑤ 개념체계가 개정될 때마다 상충을 방지하기 위해 전 세계 모든 기준서가 당일 자동으로 통합 삭제된다."
        ],
        "answer": "1",
        "explanation": "① 개념체계는 회계기준위원회의 투명성, 책임성, 효율성을 제공하려는 공식 임무에 기여하며, 일관된 개념에 기반하여 기준서를 제·개정하도록 돕는 기반을 제공합니다.\n\n[오답 해설]\n② 학술 논문이 아닌 회계기준위원회의 제개정 및 작성자 지원 공식 문서입니다.\n③ 기준서 제개정 시 일관된 개념 유지를 위해 개념체계를 강력하게 참고합니다.\n④ 축적된 업무 경험을 기초로 수시로 개정될 수 있습니다.\n⑤ 개념체계 개정 시 기존 기준서가 자동으로 변경되거나 삭제되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "개념체계는 회계기준위원회의 공식 임무를 제공하고 기준서 제개정의 기반이 됩니다.", "articles": [], "principle": "공식 임무 기여", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "학술 논문 지위가 아닙니다.", "articles": [], "principle": "문서 지위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계 기반 제정 원칙입니다.", "articles": [], "principle": "제정 원칙", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "수시 개정 가능이 맞습니다.", "articles": [], "principle": "수시 개정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자동 개정이나 일괄 삭제와 무관합니다.", "articles": [], "principle": "개정 절차", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },

    # =========================================================================
    # L4: 분석 및 박스형 다중 조합 (8문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s01-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "개념체계와 한국채택국제회계기준(K-IFRS)의 관계에 관한 설명 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 개념체계는 회계기준(기준서)이 아니므로 개념체계의 어떠한 내용도 특정 회계기준이나 그 요구사항에 우선하지 않는다.\nㄴ. 일반목적재무보고의 목적을 달성하기 위해 회계기준위원회가 개념체계의 관점에서 명백히 벗어난 요구사항을 기준서로 정할 수 있다.\nㄷ. 회계기준위원회가 개념체계와 벗어난 기준서를 정할 경우, 해당 기준서의 결론도출근거에 그 일탈에 대해 설명한다.\nㄹ. 개념체계가 개정되면 이에 상충하는 기존 한국채택국제회계기준서의 내용은 개정된 개념체계에 맞춰 즉시 자동 개정된다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄱ, ㄹ",
          "③ ㄴ, ㄷ",
          "④ ㄱ, ㄴ, ㄷ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "4",
        "explanation": "④ ㄱ, ㄴ, ㄷ은 모두 개념체계와 K-IFRS의 관계에 관한 옳은 기술입니다. ㄹ의 경우 개념체계가 개정되더라도 자동으로 회계기준(K-IFRS)이 개정되는 것은 아니므로 틀렸습니다.\n\n[보기 검증]\nㄱ. [참] 개념체계 9.1(2)항에서 개념체계는 회계기준이 아니며 기준서에 우선할 수 없음을 규정합니다.\nㄴ. [참] 위원회는 목적 달성을 위해 일탈 규정을 만들 수 있습니다.\nㄷ. [참] 일탈 시 결론도출근거에 그 사실을 기술하여 설명해야 합니다.\nㄹ. [거짓] 개념체계의 개정이 기존 회계기준을 자동으로 개정하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 항목은 틀렸으며, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ은 모두 옳고, ㄹ은 오답입니다.", "articles": [], "principle": "개념체계와 K-IFRS의 관계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 때문에 틀렸습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "개념체계가 명시하는 목적과 범위에 관한 설명 중 옳지 않은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 회계기준위원회가 일관된 개념에 기반하여 기준서를 제·개정하는 데 도움을 준다.\nㄴ. 특정 거래에 적용할 회계기준이 없거나 자율적인 정책 선택이 허용된 경우 재무제표 작성자가 일관된 회계정책을 수립하는 데 도움을 준다.\nㄷ. 모든 이해관계자가 한국채택국제회계기준을 해석하고 이해하는 데 도움을 준다.\nㄹ. 과세관청이 법인세를 정확하게 산정하여 강제 징수할 수 있도록 과세 표준 기준을 설계하는 데 직접적인 도움을 준다.\nㅁ. 외부감사인이 감사의견을 형성할 때 K-IFRS 기준서의 해석에 오류가 없도록 지원한다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄹ",
          "③ ㄹ, ㅁ",
          "④ ㄱ, ㄷ, ㅁ",
          "⑤ ㄴ, ㄹ, ㅁ"
        ],
        "answer": "2",
        "explanation": "② ㄹ만 옳지 않은 기술입니다. 개념체계는 일반목적재무보고를 목적으로 설계된 개념문서이므로 과세관청의 법인세 징수나 세무 과세 표준 설계 목적을 지원하지 않습니다.\n\n[보기 검증]\nㄱ, ㄴ, ㄷ. [참] 개념체계의 공식적인 3대 목적에 해당합니다.\nㄹ. [거짓] 세무 과세 목적은 개념체계 목적이 아닙니다.\nㅁ. [참] 외부감사인은 모든 이해관계자에 포함되므로 감사 중 기준서의 유용한 이해와 해석을 지원받습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄱ, ㄴ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄹ만 유일하게 옳지 않은 오답 지문입니다.", "articles": [], "principle": "개념체계 목적 범위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㅁ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ, ㅁ은 모두 옳은 지문입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ, ㅁ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "회계기준위원회의 공식 임무와 개념체계의 역할에 관한 설명 중 옳은 것의 개수는?\n\n[보기]\n- 위원회의 공식 임무는 전 세계 금융시장에 투명성, 책임성, 효율성을 제공하는 회계기준을 개발하는 것이다.\n- 개념체계에 기반한 회계기준은 자본제공자와 자본수탁자 간의 정보 격차를 완전히 소멸시켜 대리인 비용을 원천 차단(0원)한다.\n- 국제적으로 비교가능한 정보의 원천으로서 개념체계에 기반한 회계기준은 규제기관에게도 매우 중요하다.\n- 기업이 개념체계에 기반한 신뢰성 있는 단일의 회계 언어를 사용하는 것은 자본비용을 증가시킬 우려가 있으므로 조심스럽게 적용되어야 한다.\n- 일반목적재무보고서의 공통된 정보 수요에 초점을 맞춘다고 해서 보고기업이 추가 유용한 정보를 포함하는 것을 금지하지는 않는다.",
        "options": [
          "① 1개",
          "② 2개",
          "③ 3개",
          "④ 4개",
          "⑤ 5개"
        ],
        "answer": "3",
        "explanation": "③ 보기 중 옳은 문장은 첫 번째, 세 번째, 다섯 번째 총 3개입니다.\n\n[보기 검증]\n1. [옳음] 위원회 공식 임무에 대한 올바른 명시입니다.\n2. [틀림] 정보 격차를 '줄이는(줄임으로써 책임을 강화)' 역할을 할 뿐, 격차를 100% 완전히 소멸시키거나 대리인 비용을 0원으로 만들 수는 없습니다.\n3. [옳음] 규제기관에게도 개념체계에 기반한 기준은 매우 유용하고 중요합니다.\n4. [틀림] 단일 회계 언어 사용은 자본비용을 '감소'시키고 국제보고 비용을 '절감'시킵니다.\n5. [옳음] 공통 수요 초점이 추가 유용 정보의 기재를 차단하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "개수가 부족합니다.", "articles": [], "principle": "개수 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개수가 부족합니다.", "articles": [], "principle": "개수 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "1, 3, 5번의 3개 지문이 옳습니다.", "articles": [], "principle": "개념체계 및 위원회 임무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "오답 지문이 2개 섞여 있습니다.", "articles": [], "principle": "개수 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "모두 옳지는 않습니다.", "articles": [], "principle": "개수 판단", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "일반목적재무보고가 제공하는 정보와 한계에 관한 설명 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 재무보고서는 보고기업의 가치를 보여주기 위해 고안된 것이 아니며, 가치 추정을 위한 재무 상태 및 성과 등의 정보를 제공한다.\nㄴ. 일반목적재무보고서는 주요이용자가 필요로 하는 모든 정보를 제공하지는 않으며 제공할 수도 없다.\nㄷ. 발생기준 회계는 한 기간의 현금 수취와 지급만의 정보보다 기업의 과거 및 미래 성과를 평가하는 데 더 나은 근거를 제공한다.\nㄹ. 재무보고서는 상당 부분 정확한 서술보다는 추정, 판단 및 모형에 근거한다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄱ, ㄷ",
          "③ ㄴ, ㄹ",
          "④ ㄱ, ㄴ, ㄷ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "5",
        "explanation": "⑤ 보기의 ㄱ, ㄴ, ㄷ, ㄹ은 모두 개념체계가 공식 규정하고 있는 재무보고 정보의 성격, 한계, 지침에 관한 명백히 옳은 내용입니다.\n\n[보기 검증]\nㄱ. [참] 가치를 보여주지 않으나 가치 추정을 돕습니다.\nㄴ. [참] 모든 정보를 완벽히 제공할 수는 없는 태생적 한계가 존재합니다.\nㄷ. [참] 발생주의 회계는 현금 흐름 단독 수치보다 유용합니다.\nㄹ. [참] 재무제표는 본질적으로 추정과 판단, 모형에 상당 부분 의존합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ, ㄹ 모두 옳습니다.", "articles": [], "principle": "재무보고 유용성과 한계", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "개념체계의 목적과 위상에 관한 설명 중 옳지 않은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 개념체계가 개정되면 상충 상황을 피하기 위해 기존 K-IFRS 기준서의 어떠한 효력도 즉시 상실되어 무효가 된다.\nㄴ. 기준서의 내용과 개념체계가 상충할 경우, 감사인은 개념체계를 적용하라는 의견을 회계 처리에 직접 강제 적용할 수 없다.\nㄷ. 회계기준위원회가 공식 제정한 회계기준은 그것이 개념체계와 상충하는 경우에도 여전히 강력한 유효성을 가진다.\nㄹ. 개념체계의 제1 목적은 외부감사인이 감사의견을 결정할 때 적용해야 할 최우선 단일 판단 기준을 제공하는 것이다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄱ, ㄹ",
          "③ ㄴ, ㄷ",
          "④ ㄴ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ"
        ],
        "answer": "2",
        "explanation": "② 옳지 않은 오답 지문은 ㄱ과 ㄹ입니다.\n\n[보기 검증]\nㄱ. [거짓] 개념체계가 개정되어도 기존 기준서의 효력은 그대로 유지되며 자동 무효화되지 않습니다.\nㄴ. [참] 감사인은 회계 처리를 기업 경영진에게 강제하여 임의 수정시킬 권한이 없으며 기준서가 개념체계에 우선합니다.\nㄷ. [참] 개념체계와 상충하는 요구사항을 담은 기준서도 적법한 제정 절차를 거쳤다면 명백한 유효성을 가집니다.\nㄹ. [거짓] 개념체계의 제1 목적은 회계기준위원회가 일관된 개념에 기반하여 회계기준을 제·개정하도록 돕는 것입니다. 감사인의 단일 기준 제공이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄴ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ과 ㄹ은 틀린 기술이므로 옳지 않은 항목 조합에 해당합니다.", "articles": [], "principle": "개념체계 위상 오류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ, ㄷ은 모두 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ, ㄷ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "개념체계 개정(Revision)이 자본시장에 주는 영향에 관한 복합 지문 중 옳은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 개념체계가 개정되어도 기존 재무제표 작성자는 개정 전의 지침을 그대로 준수하여 작성해야만 형사 처벌을 면한다.\nㄴ. 개념체계가 수시 개정되어도 자동으로 기존 기준서가 변경되지 않으므로 시장의 회계처리 일관성이 단기적으로 보호된다.\nㄷ. 회계기준위원회가 개념체계 개정 이후 기존 기준서의 개정 필요성을 정밀 실무 검토를 거쳐 순차적으로 추진하는 절차가 정당하다.\nㄹ. 개념체계가 개정되면 개정 즉시 해당 기업의 재무제표 자산은 모두 최신 개념체계의 가액 측정 방식으로 소급 평가되어야만 적합하다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄷ",
          "③ ㄴ, ㄹ",
          "④ ㄱ, ㄷ",
          "⑤ ㄱ, ㄴ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 옳은 지문은 ㄴ과 ㄷ입니다.\n\n[보기 검증]\nㄱ. [거짓] 개념체계 미준수를 이유로 감사 대상 법인이나 재무제표 작성자가 즉시 형사 처벌을 받는 규정은 없습니다.\nㄴ. [참] 자동 개정 방지는 시장이 회계처리의 급격한 대혼란에 빠지는 것을 보호해 줍니다.\nㄷ. [참] 위원회가 검토를 거쳐 순차 제개정을 처리하는 것이 타당한 공식 프로세스입니다.\nㄹ. [거짓] 기준서 미개정 상태에서 개념체계 개정만으로 재무제표를 즉각 소급 재작성할 법적 근거가 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄱ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄴ과 ㄷ 지문이 논리적으로 타당하며 옳은 지문입니다.", "articles": [], "principle": "개념체계 개정 영향 분석", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄹ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "개념체계가 기반하는 논리적 연계(Logical Framework)에 관한 설명 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 개념체계는 '자본의 유무'를 식별하는 독립 항목에서 시작하여 거꾸로 재무보고의 목적을 유도하는 역행적 구조이다.\nㄴ. 일반목적재무보고의 목적은 개념체계의 기초(Foundation)를 형성하며, 질적 특성과 보고기업 등 다른 개념은 목적으로부터 논리적으로 파생된다.\nㄷ. 회계정책 수립 지침과 재무제표의 요소 정의는 아무런 논리적 인과관계가 없으므로 각기 다르게 임의 준수되어도 무방하다.\nㄹ. 재무보고의 목적이 변경된다면, 개념체계의 하위 파트인 질적 특성 및 인식 기준도 목적과의 연계성을 위해 논리적으로 전면 재검토되어야 한다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄴ, ㄷ",
          "④ ㄱ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 옳은 지문은 ㄴ과 ㄹ입니다. 개념체계는 목적을 기초로 모든 하위 개념이 파생되고 유도되는 체계적 논리 연계성을 갖고 있습니다.\n\n[보기 검증]\nㄱ. [거짓] 자본이 아닌 '재무보고의 목적'이 맨 아래의 출발점입니다.\nㄴ. [참] 목적이 기초를 형성하고 질적 특성 등이 파생됩니다.\nㄷ. [거짓] 요소 정의와 정책 수립은 긴밀하게 목적 하위에서 연계되어 조화를 이루어야 합니다.\nㄹ. [참] 최상위 목적이 바뀌면 목적으로부터 도출되는 하위 파트도 당연히 일괄 재검토가 불가피합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄱ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄴ과 ㄹ이 개념체계의 논리 구조를 설명하는 옳은 기술입니다.", "articles": [], "principle": "개념체계 논리 연계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "개념체계와 보고기업 가치평가(Valuation)에 관한 설명 중 옳지 않은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 일반목적재무보고서는 보고기업의 가치를 보여주기 위해 고안된 보고서가 아니다.\nㄴ. 보고서의 순자산 가액이 시가와 일치하지 않는 것은 회계장부의 본질적인 기술 오류이다.\nㄷ. 일반목적재무보고서는 현재 및 잠재적 투자자가 F사의 가치를 스스로 추정하는 데 유용한 기초 데이터를 충분히 제공한다.\nㄹ. 재무보고서는 미래를 가정한 추정이 불가피하므로 모든 지표를 정확하게만 기재하려 시도해서는 도저히 발행될 수 없다.",
        "options": [
          "① ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄷ",
          "④ ㄱ, ㄴ",
          "⑤ ㄴ, ㄷ, ㄹ"
        ],
        "answer": "1",
        "explanation": "① 보기 중 명백히 틀린 오답 지문은 ㄴ입니다. 순자산 장부금액과 시가의 불일치는 회계의 오류가 아닌 정상적인 가치 창출의 결과물(무형자산의 자산 인식 한계 등)입니다.\n\n[보기 검증]\nㄱ. [참] 기업 가치를 직접 보여주기 위해 설계된 서류가 아닙니다.\nㄴ. [거짓] 불일치는 장부 오류가 아닌 역사적 원가주의 및 보수주의 등 정당한 회계 원칙 적용 결과입니다.\nㄷ. [참] 스스로 가치를 산정하도록 돕는 간접 유용성을 지닙니다.\nㄹ. [참] 추정과 판단, 모형이 상당 부분 반영되는 한계가 존재함을 기술합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "ㄴ 항목만 유일하게 타당하지 않은 오답 지문입니다.", "articles": [], "principle": "가치평가 불일치 오독", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ은 모두 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ, ㄹ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },

    # =========================================================================
    # L5: 고난도 심화 (2문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s01-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "회계기준위원회가 일반목적재무보고 목적 달성을 위해 개념체계의 관점과 명백히 배치되는 요구사항을 담은 새로운 회계기준(K-IFRS)을 공식 승인 및 공표하였다. 이 결정이 자본시장에 미치는 법적·회계학적 효력과 공시 의무에 대한 분석으로 가장 옳은 것은?",
        "options": [
          "① 해당 기준서는 개념체계와 상충하므로 공표 즉시 무효가 되며 적용할 수 없다.",
          "② 해당 기준서는 개념체계와 상충하더라도 법적 강제력을 지닌 유효한 기준서이며, 위원회는 해당 기준서의 결론도출근거에 그 일탈과 합리적 사유를 명시하여 공시해야 하고 작성자는 기준서를 준수해야 한다.",
          "③ 작성자는 개념체계와 기준서 중 당해 연도 당기순이익에 더 유리한 하나의 수치를 임의 선택하여 재무제표를 소급 재작성할 권리를 가진다.",
          "④ 해당 일탈을 해소하기 위해 회계기준위원회는 기존 개념체계를 즉시 폐기하고 해당 기준서와 100% 동일하게 일괄 자구 수정해야만 한다.",
          "⑤ 외부감사인은 해당 상충을 중대한 감사 제한 사유로 지정하여 해당 기업의 재무제표 전체에 대해 즉각 감사의견 거절을 표명해야 한다."
        ],
        "answer": "2",
        "explanation": "② 일반목적 재무보고의 목적을 달성하기 위해 회계기준위원회가 개념체계의 관점에서 벗어난 요구사항을 기준서로 정할 수 있습니다. 이러한 상충 상황에서도 기준서는 유효한 법적 강제력을 가집니다. 위원회는 해당 기준서의 결론도출근거에 그러한 일탈 사실과 근거를 설명해야 하며, 작성자는 개념체계 대신 해당 기준서를 엄격히 따라 회계처리해야 합니다.\n\n[오답 해설]\n① 상충을 이유로 기준서의 효력이 상실되거나 무효화되지 않습니다.\n③ 작성자가 자의적으로 유리한 대안을 선택하여 임의 적용할 수는 없습니다.\n④ 개념체계를 즉각 의무 폐기하거나 기준서에 완전히 통합시켜야 하는 강제 규정은 없습니다.\n⑤ 적법하게 제정된 기준서를 준수하였으므로 의견거절이나 감사 범위 제한 사유에 해당하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기준서 무효화 주장은 틀렸습니다.", "articles": [], "principle": "기준서 효력 우선", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "일탈 기준서도 유효하며 결론도출근거에 관련 사실을 기재해야 합니다.", "articles": [], "principle": "결론도출근거 일탈 공시", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적 선택은 불가능합니다.", "articles": [], "principle": "일관성 및 기준 준수", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계 즉시 수정 강제는 불필요합니다.", "articles": [], "principle": "개념체계 개정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사의견 거절 사유가 되지 않습니다.", "articles": [], "principle": "감사의견 판단", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s01-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "개념체계가 규정하는 '추정, 판단 및 모형(Estimates, Judgments and Models)'의 지위에 관한 심층적인 분석으로 가장 옳은 것은?",
        "options": [
          "① 추정치와 모형은 재무 정보의 신뢰성을 근본적으로 파괴하므로, 개념체계는 궁극적으로 정확한 수치만을 보고하는 완전한 현금주의 회계를 지향점으로 삼는다.",
          "② 재무보고서는 상당 부분 추정, 판단 및 모형에 근거하며, 개념체계는 이러한 추정 등의 기초가 되는 개념을 정하여 위원회와 작성자가 노력을 기울여 지향해야 하는 '최적의 목표(Goal)'로 서술하고 있다.",
          "③ 개념체계는 추정 모형의 수치적 한계를 최소화하기 위해, 오직 정부가 공인하여 공시하는 감정평가 및 공정시장 지표만을 전적으로 대입할 것을 절대 규정으로 강제한다.",
          "④ 추정과 판단에 오류가 있을 경우 해당 작성자는 형사 소송을 당하므로, 개념체계는 작성자를 보호하기 위해 자산 평가액을 장부에 기재하지 않도록 면제해 준다.",
          "⑤ 추정치와 모형에 반영되는 주관적 요소를 제거하기 위해, 개념체계는 자산 가액의 변동이 있을 때마다 당기 주총의 3분의 2 동의를 거쳐 장부를 수정하게 한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 재무보고서가 상당 부분 추정, 판단 및 모형에 근거함을 정직하게 진술합니다. 또한 이 개념체계가 정하는 여러 원칙들은 추정과 판단의 기초가 되는 개념으로서, 회계기준위원회와 작성자가 지속적인 노력을 통해 달성하고자 지향해야 하는 최적의 공동 목표(Goal)로 자리매김하고 있음을 보여줍니다.\n\n[오답 해설]\n① 추정치는 불가피하며 현금주의 회계로의 복귀를 지향하지 않습니다.\n③ 정부 공인 지표만을 전적으로 강제하지 않으며 합리적 모형의 자율 적용을 허용합니다.\n④ 작성자를 보호하기 위해 자산 기재를 면제하지 않습니다.\n⑤ 주총의 의결을 거쳐 매번 자산 평가액을 변경하는 것은 불가능한 부적절한 절차입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "현금주의 지향은 완전히 틀린 설명입니다.", "articles": [], "principle": "회계의 지향점", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "추정 및 판단은 불가피하며 개념체계는 일관된 기초 개념을 제공해 지향해야 하는 공동의 목표가 됩니다.", "articles": [], "principle": "추정의 지위와 지향 목표", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "특수 지표의 절대 대입을 강제하지 않습니다.", "articles": [], "principle": "추정의 적용", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장부 기재 면제 조항은 없습니다.", "articles": [], "principle": "자산 인식", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주총 의결을 통한 평가액 변경 주장은 터무니없습니다.", "articles": [], "principle": "자산 평가 절차", "case": {"holding": "", "no": None}}
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
            "item": "1절 목적"
          }
        }
    }
]

# Write questions to file
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated total {len(questions)} questions in {DB_PATH.name}")
