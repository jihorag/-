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
        "id": "practice-accounting-ch01s02-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "개념체계와 한국채택국제회계기준(K-IFRS)의 관계에 관한 설명 중 가장 올바른 정의는?",
        "options": [
          "① 개념체계는 회계기준에 속하므로 기준서에 우선하여 효력이 발생한다.",
          "② 개념체계는 회계기준(기준서)이 아니다.",
          "③ 개념체계는 기업의 조세 부담을 줄이기 위한 세법의 연장선상에 있는 문서이다.",
          "④ 개념체계와 기준서가 다를 경우 작성자가 두 수치의 중앙값으로 재무상태표를 수정해야 한다.",
          "⑤ 개념체계는 외부감사인의 독립성을 철저하게 통제하여 감사의견을 결정해 주는 법률이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준(기준서)이 아니며, 개념체계의 어떠한 내용도 특정 회계기준이나 요구사항에 우선하지 않습니다.\n\n[오답 해설]\n① 개념체계는 기준서가 아니며 우선하지 않습니다.\n③ 세법과 전혀 무관합니다.\n④ 중앙값 임의 절충은 불가합니다.\n⑤ 감사인의 독립성 통제 법률이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "개념체계는 회계기준이 아닙니다.", "articles": [], "principle": "개념체계 성격", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계는 회계기준이 아닙니다.", "articles": [], "principle": "개념체계 정의", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세법과 전혀 관련이 없습니다.", "articles": [], "principle": "세법 관계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적인 중간값 계산은 불가합니다.", "articles": [], "principle": "상충 처리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사인 통제 법률이 아닙니다.", "articles": [], "principle": "감사법규", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "개념체계와 한국채택국제회계기준(K-IFRS)의 요구사항이 상충하는 경우에 대한 지침으로 옳은 것은?",
        "options": [
          "① 개념체계의 어떠한 내용도 회계기준이나 그 요구사항에 우선하지 않는다.",
          "② 상충 시에는 상법 상의 법원이 정해 주는 임시 판례를 우선 적용한다.",
          "③ 작성자는 임의로 두 수치를 합산하여 평균값으로 수정 보고한다.",
          "④ 해당 거래를 공시 대상에서 전면 누락하여 불확실성을 피한다.",
          "⑤ 회계기준위원회는 상충이 발생할 때마다 기존 개념체계를 수시로 자동 폐기한다."
        ],
        "answer": "1",
        "explanation": "① 개념체계는 특정 기준서(K-IFRS)의 명시적 요구사항보다 결코 우선할 수 없습니다. 따라서 기준서의 요구사항을 엄격하게 적용하여 처리해야 합니다.\n\n[오답 해설]\n② 법원의 상법 판례를 우선 적용해 기준서를 위반할 수 없습니다.\n③ 임의의 가액 합산 평균 보고는 불허됩니다.\n④ 상충을 피하고자 공시를 누락하는 것은 공시의 의무를 위배하는 것입니다.\n⑤ 개념체계를 자동으로 폐기하거나 무효화하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "개념체계는 기준서의 요구사항에 결코 우선하지 않습니다.", "articles": [], "principle": "상충 시 우선순위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "상법 판례가 기준서에 우선하여 임의 대체하지 않습니다.", "articles": [], "principle": "법원 관계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의의 가치 평가는 금지됩니다.", "articles": [], "principle": "가치 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "공시 누락은 심각한 회계 위반입니다.", "articles": [], "principle": "공시의 성실성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계의 자동 폐기 규정은 없습니다.", "articles": [], "principle": "개념체계 효력", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "회계기준위원회(KASB)가 개념체계의 기본 관점에서 벗어난 일탈 요구사항을 담은 기준서를 제정할 때, 이 일탈 사실을 명시해야 하는 공식 문서의 명칭은?",
        "options": [
          "① 당해 기업 재무상태표의 주석 첫 페이지",
          "② 국세청 과세표준 세무조정 명세서",
          "③ 해당 기준서의 결론도출근거(Basis for Conclusions)",
          "④ 해당 기업 이사회의 의사록",
          "⑤ 한국거래소 시장 감리 보고서"
        ],
        "answer": "3",
        "explanation": "③ 회계기준위원회가 일반목적재무보고 목적 달성을 위해 개념체계에서 벗어난 요구사항을 기준서로 정할 경우, 해당 기준서의 '결론도출근거(Basis for Conclusions)'에 그러한 일탈을 명확히 설명해야 합니다.\n\n[오답 해설]\n① 기업의 재무제표 주석이 아닌 위원회의 기준서 문서에 기재합니다.\n② 세무 보고서와 무관합니다.\n④, ⑤ 개별 기업 이사회 의사록이나 거래소 감리 보고서의 소관이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기업의 주석에 위원회의 결론 의무를 담지 않습니다.", "articles": [], "principle": "공시 위치", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "국세청 문서와 관련 없습니다.", "articles": [], "principle": "세법 관계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "해당 기준서의 결론도출근거(Basis for Conclusions)에 기록합니다.", "articles": [], "principle": "결론도출근거 일탈 설명", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "이사회 의사록의 소관이 아닙니다.", "articles": [], "principle": "이사회", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "거래소 문서의 소관이 아닙니다.", "articles": [], "principle": "거래소", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "개념체계의 수시 개정이 발생하였을 경우, 자동으로 기존의 회계기준(K-IFRS)들이 개정되는지에 대한 설명으로 옳은 것은?",
        "options": [
          "① 개념체계가 개정되면 상충되는 기존 회계기준은 별도의 절차 없이 자동 개정된다.",
          "② 개념체계가 개정되더라도 기존의 회계기준이 자동으로 개정되는 것은 아니다.",
          "③ 개념체계 개정일로부터 3개월 내에 모든 기준서가 전면 소급 개정되어 폐기된다.",
          "④ 개념체계 개정은 기존 회계기준의 법적 강제력을 상실시키는 유일한 원인이다.",
          "⑤ 개념체계의 개정 효력은 기존 기준서의 개정이 완료될 때까지 전면 유예된다."
        ],
        "answer": "2",
        "explanation": "② 개념체계가 개정되더라도 기존의 회계기준(K-IFRS)이 자동으로 개정되는 것은 아닙니다. 기존 기준서를 수정하려면 독립적인 기준서 제·개정 심의 절차를 밟아야 합니다.\n\n[오답 해설]\n① 자동 개정되지 않습니다.\n③ 3개월 내 소급 폐기 의무가 없습니다.\n④ 개념체계 개정은 기존 기준서의 법적 유효성에 영향을 주지 않습니다.\n⑤ 개념체계 개정 효력 자체가 유예되지 않으며, 개념체계는 개정된 시점부터 그 자체로 유효합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "자동으로 기준서가 변경되지는 않습니다.", "articles": [], "principle": "개정 영향", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계가 개정되더라도 기존 기준서가 자동으로 개정되는 것은 아닙니다.", "articles": [], "principle": "개념체계 개정의 독립성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "3개월 폐기 의무는 없습니다.", "articles": [], "principle": "개정 시차", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기존 기준서의 법적 강제력은 그대로 유효합니다.", "articles": [], "principle": "기준서의 효력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계 효력 유예와 무관합니다.", "articles": [], "principle": "개념체계 적용", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "회계기준에서 특정 거래에 대해 자율적인 회계정책 선택 대안(원가모형 또는 재평가모형 등)을 허용하는 경우, 재무제표 작성자가 개념체계로부터 받을 수 있는 공식 지원은?",
        "options": [
          "① 작성자가 어떤 대안을 선택하든 매년 임의 세금을 탕감받을 수 있는 법적 보증",
          "② 일관된 회계정책을 수립하여 작성하고 정보의 신뢰성을 높이도록 돕는 개념적 안내",
          "③ 감사인의 모든 감사 지적 사항에 대하여 즉시 소송을 제기할 수 있는 면책 특권",
          "④ 매년 번복하여 선택하더라도 가산세를 면제받을 수 있는 세무상 혜택",
          "⑤ 회계장부에서 해당 거래 자산 자체를 지워 없애도 처벌받지 않도록 하는 유예"
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준에서 특정 회계정책을 선택하는 것을 허용하는 상황에서 작성자가 일관되고 합리적인 회계정책을 개발하도록 도움을 줍니다.\n\n[오답 해설]\n①, ④ 세무 탕감이나 가산세 면제 등 세무 혜택과 관계없습니다.\n③ 감사 분쟁 관련 사법적 면책권을 주지 않습니다.\n⑤ 자산 누락 처벌 유예 권한이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "세무 세금과 무관합니다.", "articles": [], "principle": "세법 관계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "정책 선택 대안 존재 시 작성자의 일관된 회계정책 수립을 지원합니다.", "articles": [], "principle": "작성자 정책 수립 지원", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사 면책 특권을 주지 않습니다.", "articles": [], "principle": "감사 관계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "가산세 면제와 무관합니다.", "articles": [], "principle": "세금", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자산 임의 제거를 보장하지 않습니다.", "articles": [], "principle": "장부 오류", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "기업이 직면한 특정 거래에 관하여 명시적으로 정한 K-IFRS 기준서 규정이 존재하지 않는 경우, 재무제표 작성자가 취해야 하는 원칙적인 태도로 옳은 것은?",
        "options": [
          "① 해당 거래의 회계처리를 일체 거부하고 주석 공시에서도 전액 누락한다.",
          "② 관련 개념체계의 목적과 자산·부채 정의에 기초하여 일관된 회계정책을 자체적으로 개발하여 적용해야 한다.",
          "③ 감사법인이 추천해 주는 임의의 무장부 처리를 수행하고 수수료를 지급한다.",
          "④ 해당 신규 사업 전체를 임시로 폐업 처리한 것으로 위장 보고한다.",
          "⑤ 기준서가 제정되어 공표될 때까지 당기 결산 마감 일정을 3년 연기한다."
        ],
        "answer": "2",
        "explanation": "② 적용할 회계기준이 없는 특수한 거래나 상황이 발생하는 경우, 작성자는 개념체계를 바탕으로 정보이용자에게 유용하고 일관된 회계정책을 자체 수립하여 적용해야 합니다.\n\n[오답 해설]\n① 공시 거부는 허용되지 않습니다.\n③, ④ 감사인의 자의적 회계처리나 폐업 위장은 명백한 회계 부정입니다.\n⑤ 기준서 제정을 기다려 결산 마감을 미루는 것은 불가능합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "공시 누락 처리는 불가합니다.", "articles": [], "principle": "공시 의무", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서 부재 시 개념체계의 원리를 사용해 작성자가 합리적 회계정책을 수립해야 합니다.", "articles": [], "principle": "회계정책 개발 의무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "무장부 처리 등은 위법입니다.", "articles": [], "principle": "장부 작성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "폐업 위장은 위법입니다.", "articles": [], "principle": "위장 보고", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "결산 마감 임의 연기는 불가합니다.", "articles": [], "principle": "결산 보고", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "개념체계와 K-IFRS 기준서의 지위와 관련하여, 외부감사인이 가질 수 없는 권한으로 옳은 것은?",
        "options": [
          "① 기업이 명백한 특정 기준서의 조항을 따라 작성한 장부에 대해, 개념체계 조항에 부합하지 않는다는 독단적 이유로 기재 수정을 강제하는 권한",
          "② 기업이 적용한 기준서 해석의 타당성을 객관적으로 검토하는 감사 권한",
          "③ 재무제표가 전반적으로 K-IFRS에 적정하게 도출되었는지 독립적 감사 의견을 표명하는 권한",
          "④ 기업의 회계처리가 특정 기준서의 지침에 맞지 않음을 지적하는 권한",
          "⑤ 기말 재무제표의 주석 기재 사항이 충분한지 확인하는 권한"
        ],
        "answer": "1",
        "explanation": "① 개념체계는 회계기준에 우선하지 않으므로, 기업이 유효한 기준서를 따라 적절히 장부를 작성했다면 감사인은 개념체계 위배를 이유로 기재 수정을 강제할 수 없습니다.\n\n[오답 해설]\n②, ③, ④, ⑤는 모두 외부감사인이 적법하게 보유한 외부 감사 업무 상의 권한이자 의무에 해당합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "감사인은 적법한 기준서 적용 재무제표에 대해 개념체계를 빌미로 수정을 강제할 권한이 없습니다.", "articles": [], "principle": "감사인 권한의 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "타당성 검토는 감사인의 기본 권한입니다.", "articles": [], "principle": "감사 권한", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "의견 표명은 감사인의 기본 임무입니다.", "articles": [], "principle": "감사 임무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기준서 위반 지적은 감사인의 권한입니다.", "articles": [], "principle": "감사 지적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주석 기재 충실성 검토는 감사인의 권한입니다.", "articles": [], "principle": "주석 검토", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "개념체계와 상충하는 특정 K-IFRS 기준서의 예외적 일탈(Deviation)을 공식적으로 심의하고 정할 수 있는 유일한 의사결정 기구는?",
        "options": [
          "① 기획재정부 세제실",
          "② 한국회계기준원 회계기준위원회(KASB)",
          "③ 한국공인회계사회 윤리위원회",
          "④ 한국감정평가사협회 이사회",
          "⑤ 서울남부지방법원 금융 합의부"
        ],
        "answer": "2",
        "explanation": "② 한국채택국제회계기준(K-IFRS)의 제·개정과 개념체계의 관점 일탈 여부를 공식 결정하고 설명할 수 있는 유일한 권한 기구는 회계기준위원회(KASB)입니다.\n\n[오답 해설]\n① 기재부 세제실은 세법 개정 소관입니다.\n③ 회계사회는 감사인 단체로 기준 제정 권한이 없습니다.\n④ 감평협회는 회계학 기준서 제정과 관련 없습니다.\n⑤ 사법 법원은 회계기준 제정 기구가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기재부는 세법 소관입니다.", "articles": [], "principle": "기획재정부", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "회계기준위원회(KASB)가 공식 회계기준서의 일탈 여부를 정하는 주체입니다.", "articles": [], "principle": "기준 제정 기구", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "공인회계사회는 기준 제정 기구가 아닙니다.", "articles": [], "principle": "회계사회", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감평협회는 기준 제정 기구가 아닙니다.", "articles": [], "principle": "감평협회", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "법원은 기준 제정 기구가 아닙니다.", "articles": [], "principle": "사법부", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "개념체계 본문과 개별 K-IFRS 기준서(회계기준) 본문의 물리적·구조적 통합 여부에 관한 설명으로 옳은 것은?",
        "options": [
          "① 개념체계는 매년 개정되어 모든 개별 기준서의 제1장으로 의무 병합된다.",
          "② 개념체계는 회계기준(기준서)에 포함되지 않으므로 개별 기준서 본문의 일부가 아니다.",
          "③ 개념체계는 개별 기준서의 주석 부분에 요약본으로 반드시 인쇄 첨부되어야 한다.",
          "④ 개념체계는 기준서에 속하므로 기준서 본문 뒤의 별지 부록 형식으로만 존재한다.",
          "⑤ 개념체계와 기준서는 하나의 파일로 묶여 국가 법령 법전으로 통합 공표된다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준이 아닙니다. 따라서 개념체계의 어떠한 규정도 특정 회계기준에 병합되거나 개별 기준서 본문의 일부를 이루지 않으며, 독립적인 개념적 지침서로 존재합니다.\n\n[오답 해설]\n① 기준서 본문에 의무 병합되지 않습니다.\n③ 기준서 주석에 첨부 의무가 없습니다.\n④ 기준서의 별지 부록 형태에 국한되지 않고 별개 문서로 관리됩니다.\n⑤ 국가 법령 법전으로 법률 통합 공표되는 성격이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기준서에 강제 병합되지 않습니다.", "articles": [], "principle": "개념체계 독립성", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계는 회계기준이 아니며 기준서 본문의 일부가 아닙니다.", "articles": [], "principle": "개념체계의 독립적 지위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주석에 의무 인쇄되지 않습니다.", "articles": [], "principle": "개념체계 공시", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기준서 부록에 국한되지 않습니다.", "articles": [], "principle": "개념체계 관리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "국가 법령 통합이 아닙니다.", "articles": [], "principle": "법령 체계", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "개념체계와 한국채택국제회계기준(K-IFRS)의 논리적 충돌 가능성을 개념체계가 스스로 인정하는 지침 내용으로 옳은 것은?",
        "options": [
          "① 회계기준위원회는 목적 달성을 위해 일체 개념체계에서 일탈한 요구사항을 정할 수 없다고 단언한다.",
          "② 일반목적재무보고 목적 달성을 위해 위원회가 개념체계의 관점에서 벗어난 요구사항을 정하는 경우가 있을 수 있음을 인정한다.",
          "③ 상충이 생기면 개념체계는 즉시 효력을 잃고 영구 폐기됨을 선언한다.",
          "④ 위원회가 개념체계에서 벗어난 요구사항을 지정할 때는 금융감독원의 징계 처분을 받게 된다고 경고한다.",
          "⑤ 상충하는 모든 기준서는 헌법재판소에 위헌법률 심판을 청구하여 효력을 정지시켜야 한다고 지적한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 일반목적 재무보고의 목적을 달성하기 위해 회계기준위원회가 개념체계의 관점에서 벗어난 요구사항을 정하는 경우(일탈)가 있을 수 있음을 공식 인정하고 있습니다.\n\n[오답 해설]\n① 일탈 규정을 정하는 것을 허용하므로 단언적으로 정할 수 없다고 하지 않습니다.\n③, ④, ⑤ 징계, 자동 폐기, 위헌법률 심판 청구 등 행정·사법적 조치를 규정하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "일탈 제정 권한을 명시적으로 인정합니다.", "articles": [], "principle": "위원회 제정 권한", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "목적 달성을 위해 개념체계 관점 일탈 기준서 제정 가능성을 공식 수용합니다.", "articles": [], "principle": "상충 가능성 인정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "효력 소멸 선언과 무관합니다.", "articles": [], "principle": "개념체계 효력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "징계 경고 규정이 아닙니다.", "articles": [], "principle": "제재 조항 부재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "위헌 제청 등 사법 절차 지침이 아닙니다.", "articles": [], "principle": "사법 절차", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },

    # =========================================================================
    # L2: 이해 수준 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s02-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "개념체계와 K-IFRS 특정 기준서가 불일치할 때 재무제표 작성자가 자의적인 절충안을 취할 수 없는 회계적 지침의 본질적 이유로 옳은 것은?",
        "options": [
          "① 자의적 절충안은 세금 환급액을 자동으로 감소시키는 불이익을 초래하기 때문이다.",
          "② 기준서 요구사항은 법적 의무 사항이므로 개념체계와 충돌하더라도 기준서의 지침을 100% 온전히 따라야만 적법한 재무보고가 되기 때문이다.",
          "③ 감사인이 절충안을 직접 작성하여 이사회에 인가해 주는 전결권이 없기 때문이다.",
          "④ 절충안을 허용하면 형법 상 주주들에 대한 사기죄 공모 혐의가 자동 성립하기 때문이다.",
          "⑤ 두 수치를 절충하면 소급 감가상각이 법적으로 무효화되기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준에 우선하지 못하므로, 두 규정이 상충할 시 작성자는 자의적으로 절충해서는 안 되며 반드시 기준서의 명시적 요구사항을 엄격하게 준수하여 장부를 기재해야 합니다.\n\n[오답 해설]\n① 세금 환급액 손실을 본질적 이유로 들지 않습니다.\n③ 감사인의 전결권 부재를 원인으로 설명하지 않습니다.\n④ 사기죄의 자동 형사 기소를 회계 조항에서 선언하지 않습니다.\n⑤ 감가상각 무효 조항과 관계없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "세무 환급과 무관합니다.", "articles": [], "principle": "세법 관계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서의 법적 구속력으로 인해 상충 시 기준서 지침을 예외 없이 완전히 따라야 합니다.", "articles": [], "principle": "기준서의 우선 구속력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사인 전결권과 무관합니다.", "articles": [], "principle": "감사인 권한", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "형사 공모 혐의 선언은 회계 개념 범위가 아닙니다.", "articles": [], "principle": "사법 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감가상각 무효와 관계없습니다.", "articles": [], "principle": "회계 오류", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "회계기준위원회가 특정 기준서에 개념체계의 관점과 벗어난 일탈 조항을 제정 및 기재할 때, 해당 기준서의 '결론도출근거'에 포함해야 하는 정보 설명 수준으로 옳은 것은?",
        "options": [
          "① 단순히 일탈이 발생했다는 사실만 1줄로 단조롭게 기재하고 세부 근거는 숨긴다.",
          "② 그러한 개념체계와의 일탈(상충)이 발생한 구체적인 사실과 그렇게 벗어난 요구사항을 제정하게 된 합리적 결론도출 사유를 명시하여 설명해야 한다.",
          "③ 일탈을 주도한 위원회 위원들의 이름과 인적 사항을 대외에 강제 기재하여 처벌을 유도한다.",
          "④ 해당 일탈이 유발하는 예상 주가 하락률을 정확하게 공식 시뮬레이션하여 산출 수치로 표기한다.",
          "⑤ 일탈 조항이 유발하는 법인세 증감액을 전 국세청 신고 기준에 맞춰 산출 표기한다."
        ],
        "answer": "2",
        "explanation": "② 위원회가 개념체계 일탈 요구사항을 기준서로 지정하는 경우, 해당 결론도출근거에 그 일탈의 성격과 그러한 설계를 정하게 된 이유 및 결론 도출 과정을 자세히 명시하고 설명해야 정보이용자가 해석할 수 있습니다.\n\n[오답 해설]\n① 1줄의 단조로운 축약 기재나 은폐는 투명성 원칙에 반합니다.\n③ 위원 개인의 처벌을 유도하는 기재를 하지 않습니다.\n④ 주가 영향 예측 시뮬레이션 기재 의무가 없습니다.\n⑤ 법인세 증감 세액을 기준서 결론도출근거에 담지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "단순 누락이나 축약은 투명성 원칙 위배입니다.", "articles": [], "principle": "공시 충실성", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "해당 결론도출근거에 일탈 사실 및 합리적 이유를 명시적으로 설명해야 합니다.", "articles": [], "principle": "결론도출근거 설명 수준", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "인적 사항 강제 노출과 무관합니다.", "articles": [], "principle": "개인정보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주가 산출 시뮬레이션 의무가 없습니다.", "articles": [], "principle": "주가 예측", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세액 산출 기재 의무와 무관합니다.", "articles": [], "principle": "세금", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "K-IFRS 특정 기준서 규정이 명백하게 존재하여 회사가 이에 따라 회계 처리를 충실하게 완료하였다. 외부감사인이 개념체계의 자산 정의를 주장하며 재무제표 감사의견을 적정이 아닌 의견거절로 내리겠다고 위협할 때, 회사가 반박할 수 있는 정당한 근거로 옳은 것은?",
        "options": [
          "① 감사인을 위계에 의한 업무방해죄로 사법 처벌하겠다고 법적으로 통보한다.",
          "② 개념체계는 회계기준이 아니므로 특정 기준서의 지침에 우선할 수 없음을 밝히고, 기준서 준수가 감사보고서 상 적정 의견의 올바른 요건임을 지적한다.",
          "③ 감사인의 주장을 들어주는 척하며 뒷돈 거래(뇌물)를 제안하여 상황을 덮는다.",
          "④ 즉시 당해 자산을 전액 비용으로 삭제하고 감사인의 의견대로 장부를 고친다.",
          "⑤ 세무서에 감사인을 세무조사 누락 혐의로 직접 고발하여 위협한다."
        ],
        "answer": "2",
        "explanation": "② 감사인은 기업이 유효한 기준서를 따라 장부를 기재했음에도 개념체계와 다르다는 자의적 이유를 대며 수정 요구를 하거나 의견 거절 등의 부적절한 감사의견을 남발할 수 없습니다. 개념체계는 기준서에 결코 우선하지 않기 때문입니다.\n\n[오답 해설]\n① 형사 처벌 사법 통보를 회계학적 직접 반박 근거로 보지 않습니다.\n③, ⑤ 뇌물 제안이나 세무당국 무고 등은 심각한 불법 행위입니다.\n④ 기준서를 위반하여 자의적으로 자산을 지우는 것은 분식회계에 해당합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "업무방해 고소 위협은 회계학적 근거가 아닙니다.", "articles": [], "principle": "사법 조치", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계는 기준서에 우선하지 않으므로 기준서에 따라 처리한 재무제표가 적정합니다.", "articles": [], "principle": "기준서의 우선 효력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "뇌물은 불법입니다.", "articles": [], "principle": "윤리 규정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기준서 이탈 수정은 회계 오류입니다.", "articles": [], "principle": "회계 처리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "고발 조치는 올바른 반박이 아닙니다.", "articles": [], "principle": "행정 사법", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "개념체계가 개정된 시점과 개별 K-IFRS 기준서들이 실제로 이에 맞춰 개정되는 시점 사이의 시간적 간격(Time lag)이 초래하는 자본시장의 영향에 대한 해석으로 옳은 것은?",
        "options": [
          "① 개념체계 개정일 즉시 모든 상충 기준서가 소멸되므로 일체 회계 처리가 불가능한 공백 상태가 된다.",
          "② 개념체계의 개정이 기존 기준서를 자동으로 개정시키지 않으므로, 기준서가 공식 수정될 때까지 과도기적으로 상충이 존재할 수 있으며 그 기간에는 기존 기준서를 그대로 준수하여 처리한다.",
          "③ 상충 기간 동안 작성자는 본인의 선호에 따라 아무런 회계 처리도 하지 않는 것이 강제 권장된다.",
          "④ 금융감독원장이 직권으로 개정 개념체계를 기준서에 우선 적용하게 하는 임시 규칙을 공포한다.",
          "⑤ 두 규정이 불일치하는 즉시 주식거래소는 해당 기업들의 거래를 무기한 정지시켜야 한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계가 개정되더라도 기존의 회계기준(K-IFRS)이 자동으로 개정되는 것은 아닙니다. 따라서 양 규정 간의 불일치가 발생하는 과도기적 기간이 존재할 수 있으며, 이 시기에는 여전히 유효한 기존 기준서에 따라 처리해야 합니다.\n\n[오답 해설]\n① 기준서가 소멸하여 공백 상태가 되지 않습니다.\n③ 회계 처리를 보류하거나 방치해서는 안 됩니다.\n④ 금감원장에게 임시 대체 규칙 공포 권한이 있지 않습니다.\n⑤ 불일치 발생이 주식 거래 정지 사유에 해당하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기준서 소멸 공백은 발생하지 않습니다.", "articles": [], "principle": "기준서 유효성", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개 개념체계 개정 직후 기준서 미개정 과도기에는 여전히 유효한 기존 기준서에 따라 처리합니다.", "articles": [], "principle": "개정 시차와 회계 처리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "회계 처리 보류 방치는 금지됩니다.", "articles": [], "principle": "보고 의무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "금감원장 권한 밖의 행동입니다.", "articles": [], "principle": "감독 권한", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "거래 정지 사유가 아닙니다.", "articles": [], "principle": "거래소", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "회계기준위원회(KASB)가 기준서를 제정 및 개정할 때 개념체계를 핵심 기반으로 삼는 실무적 의의로 가장 적절한 것은?",
        "options": [
          "① 새로운 기준서를 개발할 때 일관된 개념적 프레임워크를 제공하여 자의적이거나 조각보 형태의 기준 제정을 방지하고 기준의 품질과 신뢰를 향상시킨다.",
          "② 세법상의 세금 징수를 위한 산식을 자동으로 정형화하여 제정 비용을 없앤다.",
          "③ 전 세계 기업들의 주가를 동일하게 묶어 관리하도록 유도한다.",
          "④ 기업들이 어떠한 장부도 기재하지 않는 순수한 비밀회계 제도를 장려한다.",
          "⑤ 기준서의 모든 영문 번역 의무를 면제하여 제정 절차를 10배 신속하게 처리하도록 돕는다."
        ],
        "answer": "1",
        "explanation": "① 개념체계는 회계기준위원회가 일관된 개념에 기반하여 한국채택국제회계기준을 제·개정하도록 도움을 줍니다. 이를 통해 자의적 판단을 예방하고 질적 일관성을 확보할 수 있습니다.\n\n[오답 해설]\n② 세제 산식 정형화와 관계없습니다.\n③ 주가 강제 묶음 통제와 무관합니다.\n④ 비밀회계는 투명성 원칙에 반합니다.\n⑤ 기준서의 영문 번역 의무 면제 등 번역 업무 절차와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "일관된 프레임워크를 제공하여 일관성 있고 품질 높은 기준서 개발을 가능케 합니다.", "articles": [], "principle": "기준 제정 지원 의의", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 산식 개발 목적이 아닙니다.", "articles": [], "principle": "세법", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주가 통제와 무관합니다.", "articles": [], "principle": "주식 시장", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "비밀회계 조장은 투명성 저해입니다.", "articles": [], "principle": "투명성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "번역 절차 속도 단축 등과 관계없습니다.", "articles": [], "principle": "행정 업무", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "재무제표 작성자가 명시된 K-IFRS 기준서의 지침을 무시하고, 개념체계상의 자산 요소를 근거로 기말 재무상태표를 수정하여 보고하였다. 이 자의적 판단이 초래한 오류의 성격으로 옳은 것은?",
        "options": [
          "① 개념체계를 성실히 준수하였으므로 K-IFRS를 완벽하게 만족시킨 수범 사례이다.",
          "② 개념체계는 회계기준서에 우선할 수 없으므로 명시된 기준서 조항을 배제한 회계 처리는 중대한 회계기준 위반이자 오류이다.",
          "③ 작성자가 세법상 감세를 위해 정당하게 수행할 수 있는 합법적 조세회피이다.",
          "④ 감사인의 동의만 있다면 어떠한 기준서 위반도 회계적 오류로 인정되지 않는다.",
          "⑤ 두 규정이 상충 시 작성자의 재량권이 가장 돋보인 창조적 회계(Creative Accounting)이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준서가 아니며 우선할 수 없습니다. 따라서 기준서가 엄연히 존재함에도 개념체계를 우선 적용하여 기준서를 배제하는 것은 명백한 기준서 위반이며 중대한 회계 오류입니다.\n\n[오답 해설]\n① 기준서 위반이므로 수범 사례가 될 수 없습니다.\n③ 합법적 조세회피 기법이 아닌 명백한 위법입니다.\n④ 감사인의 동의 유무와 상관없이 회계기준 위반 오류입니다.\n⑤ 자의적인 창조적 회계(분식회계)는 금지됩니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기준서 위반이므로 수범 사례가 아닙니다.", "articles": [], "principle": "회계 위반", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서가 존재함에도 개념체계를 핑계로 이를 배제하는 행동은 중대한 회계 오류입니다.", "articles": [], "principle": "기준서 배제 위반", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "조세회피나 감세 목적의 정당행위가 아닙니다.", "articles": [], "principle": "조세 포탈", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사인 동의로 오류가 정당화될 수 없습니다.", "articles": [], "principle": "감사의 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적인 분식회계는 허용되지 않습니다.", "articles": [], "principle": "창조적 회계 금지", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "개념체계와 K-IFRS 기준서가 모두 정보의 '일관성(Consistency)'을 강조하는 핵심적 이유로 옳은 것은?",
        "options": [
          "① 기업의 영업 비밀이 경쟁사로 유출되는 비율을 매년 일정한 비율로 제한하기 위함이다.",
          "② 정보이용자가 보고기업의 기간별 추세를 비교하고 타 기업 간의 유사점과 차이점을 파악하는 '비교가능성(Comparability)'을 달성하기 위함이다.",
          "③ 기업의 감사 수수료 인상률을 전년도 물가상승률과 정확하게 일치시켜 강제하기 위함이다.",
          "④ 매년 법인세 납부액을 고정 수치로 일정하게 납부할 수 있는 핑계를 제공하기 위함이다.",
          "⑤ 회계장부 전표의 종이 크기와 줄 간격을 전 공공기관에 걸쳐 동일하게 규격화하기 위함이다."
        ],
        "answer": "2",
        "explanation": "② 일관성은 비교가능성(Goal)을 달성하기 위한 수단(Method)입니다. 기업이 동일한 항목에 동일한 방법을 지속적으로 적용(일관성)함으로써 정보이용자의 항목 간 유사점/차이점 이해(비교가능성)가 보강됩니다.\n\n[오답 해설]\n① 영업 비밀 유출 비율 통제와 무관합니다.\n③ 감사 수수료 인상률 강제와 관련 없습니다.\n④ 법인세 고정 납부와 관계없습니다.\n⑤ 전표의 종이 규격 등 물리적 서식 인쇄 통일화와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "비밀 보호 조항이 아닙니다.", "articles": [], "principle": "영업 비밀", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "일관성은 비교가능성이라는 중요한 목표를 달성하는 핵심 도구입니다.", "articles": [], "principle": "일관성과 비교가능성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사 수수료 한도 책정과 무관합니다.", "articles": [], "principle": "감사 비용", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "법인세 일정액 납부와 무관합니다.", "articles": [], "principle": "세금 납부", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "서식 규격화와 관계없습니다.", "articles": [], "principle": "인쇄 규격", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "회계기준위원회(KASB)가 기준서를 제정할 때 불가피하게 개념체계의 자산 정의를 일탈하는 결정을 내릴 수 있는 논리적 배경으로 옳은 것은?",
        "options": [
          "① 개념체계의 목적에 비추어 특정 시점의 자본시장 투명성을 훼손하는 것이 이익 창출에 더 유리하다고 보았기 때문이다.",
          "② 특정 금융거래에 있어 형식보다 '경제적 실질'을 표현하는 특수한 회계 정보가 이용자에게 훨씬 목적적합하고 충실한 표현(유용성)을 제공하기 때문이다.",
          "③ 해당 일탈을 통해 회계기준위원회 소속 위원들의 성과급을 대폭 인상시키는 인센티브 제도가 작동했기 때문이다.",
          "④ 해당 거래가 세무서 감사 대상에서 즉각 제외될 수 있도록 하는 정치적 합의가 도출되었기 때문이다.",
          "⑤ 개념체계 자체를 아예 폐지하려는 장기 음모가 위원회 내부에서 의결되었기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 일반목적 재무보고의 목적을 최적으로 달성하기 위해, 때로는 구체적 현상의 실질적 유용성을 극대화하는 과정에서 개념체계의 일부 관점에서 벗어난 요구사항을 기준서에 담는 예외가 타당하게 발생할 수 있습니다.\n\n[오답 해설]\n① 투명성을 고의로 훼손하려 일탈을 정하지 않습니다.\n③, ⑤ 위원의 성과급이나 개념체계 폐지 음모 등은 전혀 사실이 아닙니다.\n④ 세무당국의 조사 제외 합의와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "투명성을 고의 저해하지 않습니다.", "articles": [], "principle": "투명성", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "실질적 유용성 향상이 개념체계의 문자 그대로의 정의보다 중요할 때 일탈 제정이 정당화됩니다.", "articles": [], "principle": "일탈의 논리적 배경", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "위원 성과급과 무관합니다.", "articles": [], "principle": "위원회", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 조사 면제 합의와 무관합니다.", "articles": [], "principle": "정치적 영향", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계 음모론 주장은 부적절합니다.", "articles": [], "principle": "음모론 배제", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "개념체계가 개정(Revision)되었으나 아직 관련 K-IFRS 기준서가 개정되지 않은 과도기 상황에 대한 작성자 의사결정의 법적 근거로 옳은 것은?",
        "options": [
          "① 신구 규정의 충돌이므로 즉시 올해분 장부 기재를 일체 중단한다.",
          "② 개념체계의 개정이 기존의 회계기준을 자동으로 개정시키는 것은 아니므로 여전히 유효한 기존 기준서를 준수하여 회계처리한다.",
          "③ 개정된 개념체계를 우선 소급 적용하여 기존 재무제표를 소급 재작성하고 공시한다.",
          "④ 금융위원회에 서한을 보내 상충이 해결될 때까지 기존 기준서 효력을 강제 정지해 달라고 명령한다.",
          "⑤ 임의의 중앙값 회계처리를 발굴하여 독자적으로 공시한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계가 개정되어도 기존 기준서가 자동으로 개정되지 않으므로, 기준서가 공식 수정 고시되기 전까지는 기존 기준서가 적법한 회계처리의 최우선 유효 기준이 됩니다.\n\n[오답 해설]\n① 장부 기재 중단은 적시성 위반입니다.\n③ 기준서 개정 없는 자의적 소급 평가는 회계 위반입니다.\n④ 금융위원회가 기준서 효력을 임의로 즉시 강제 정지시키지 않습니다.\n⑤ 자의적 절충 회계처리는 허용되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기재 중단은 허용되지 않습니다.", "articles": [], "principle": "장부 기재", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계 개정이 기존 기준서를 자동으로 개정하는 것이 아니므로 기존 기준서에 따라 처리합니다.", "articles": [], "principle": "기준서의 지속적 유효성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의의 소급 평가는 회계 오류입니다.", "articles": [], "principle": "소급 적용 오류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "금융위 강제 명령과 관련 없습니다.", "articles": [], "principle": "행정 승인", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적 임의 공시는 금지됩니다.", "articles": [], "principle": "자의성 배제", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "개념체계와 K-IFRS 기준서의 지위를 오독하여, 개념체계 조항을 핑계로 명시된 K-IFRS 기준서의 자산 손상 평가 규정을 고의 누락한 기업에 대해 시장 규제기관이 취해야 하는 올바른 조치로 옳은 것은?",
        "options": [
          "① 개념체계를 준수하기 위한 부득이한 지연이므로 규제 대상에서 전면 면제해 준다.",
          "② 명백한 기준서 위반 및 회계 부정으로 판단하고 감리 대상 지정 및 시정 명령 등의 행정 제재 조치를 취해야 한다.",
          "③ 회계기준위원회 위원 전원을 법적으로 징계 면직하여 책임을 전가한다.",
          "④ 해당 기업의 감가상각 누계액을 국유화 조치하여 압류한다.",
          "⑤ 규제할 법적 근거가 없으므로 이를 모르는 척 은폐해 준다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준에 결코 우선하지 않으므로, 개념체계를 핑계로 명시된 기준서 조항 적용을 누락하는 것은 중대한 회계기준 위반이자 감리 지적 사유에 해당합니다.\n\n[오답 해설]\n① 규제 대상에서 면제되지 않습니다.\n③ 위원회의 징계 면직 사유가 아닙니다. 책임은 기업 경영진에 있습니다.\n④ 사유 자산을 압류하거나 감가상각비를 국유화하는 법은 존재하지 않습니다.\n⑤ 은폐 조치는 위법입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "규제 면제 사유가 아닙니다.", "articles": [], "principle": "규제 면제 부재", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계를 이유로 한 기준서 적용 누락은 명백한 회계 위반이므로 적절한 제재 대상입니다.", "articles": [], "principle": "규제 기관 조치", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "위원회 위원 징계 사유가 아닙니다.", "articles": [], "principle": "위원회 책임 범위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "압류 국유화 조치와 무관합니다.", "articles": [], "principle": "재산권 보호", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "은폐는 불가합니다.", "articles": [], "principle": "공정 규제", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "개념체계와 K-IFRS 기준서의 지위와 관련해, 세법(Tax Law)과의 관계에 미치는 영향에 대한 설명으로 옳은 것은?",
        "options": [
          "① 세법이 명시적으로 개념체계를 전면 수정 지시할 수 있는 권한을 가진다.",
          "② 세법상의 세무 조정은 기업 외부보고용 재무제표의 기준서 준수 적정성과 논리적으로 독립되어 처리된다.",
          "③ 개념체계와 상충하는 세법 규정은 자동 위헌 결정이 나므로 세무 세금을 납부할 의무가 소멸한다.",
          "④ 국세청장은 회계기준위원회의 사전 허가를 받아야만 법인세율을 인상할 수 있다.",
          "⑤ 세무 회계는 개념체계를 기초로 파생되어 개발되므로 재무회계와 절대 불일치가 발생할 수 없다."
        ],
        "answer": "2",
        "explanation": "② 일반목적 재무보고서 작성 기준(K-IFRS)과 세법상의 과세 소득 산정(세무회계)은 서로 목적과 법적 기반이 다르므로 논리적으로 독립적입니다. 상충은 이연법인세 등을 통해 회계적으로 조율할 뿐입니다.\n\n[오답 해설]\n① 세법은 개념체계 제개정에 영향을 주지 않습니다.\n③ 세무 세금 납부 의무 소멸과 무관합니다.\n④ 법인세율 인상 권한은 국회에 있습니다.\n⑤ 세무회계는 개념체계의 목적 하위 파생물이 아니므로 목적 불일치가 상시 발생합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "세법이 개념체계를 수정하지 못합니다.", "articles": [], "principle": "법규 위상", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "세무 조정은 재무보고 기준서 준수와 독립적으로 작동하며 세법에 따라 처리됩니다.", "articles": [], "principle": "세법과 회계의 관계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 의무 소멸 주장은 거짓입니다.", "articles": [], "principle": "위헌 판단 부재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "위원회는 세율 결정 권한이 없습니다.", "articles": [], "principle": "세율 권한", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "두 회계는 목적 차이로 불일치가 발생합니다.", "articles": [], "principle": "재무와 세무 회계", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "개념체계와 K-IFRS 기준서의 지위 상 '일탈(Deviation)'에 대한 주석 공시를 생략한 채, 기준서만 임의 준수한 상태로 마감 공시한 회계기준위원회의 행정적 책임에 관한 설명으로 옳은 것은?",
        "options": [
          "① 주석 공시와 관계없이 기준서 조항만 통과되었으므로 어떠한 절차 위반도 없다.",
          "② 결론도출근거 상에 일탈에 대한 구체적 이유를 문서화하고 밝히지 않은 것은 회계기준위원회의 행정적 적법 절차(Due Process) 위반에 해당한다.",
          "③ 국세청이 직권으로 회계기준위원회를 기소하여 벌금을 징수할 수 있다.",
          "④ 해당 일탈 기준서 자체가 즉시 자동 파기 처리되는 소급 무효화가 발생한다.",
          "⑤ 위원회가 책임을 지기 위해 전 자산을 금융감독원에 몰수당하게 된다."
        ],
        "answer": "2",
        "explanation": "② 회계기준위원회가 개념체계와 상충하는 요구사항을 기준서로 지정하는 경우 반드시 그 이유를 결론도출근거에 밝혀야 합니다. 이의 누락은 기준 제정 기구로서 준수해야 할 공식적 적법 절차(Due Process) 위반입니다.\n\n[오답 해설]\n① 절차상 누락이므로 절차 위반이 맞습니다.\n③ 국세청의 직접 기소 및 벌금 징수 대상이 아닙니다.\n④ 일탈 설명 누락으로 기준서가 자동 소급 무효화되지는 않으며 보완 조치가 이뤄집니다.\n⑤ 자산 몰수 등의 사법 처분 대상이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "설명 누락은 명백한 절차적 오류입니다.", "articles": [], "principle": "제정 절차", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "일탈에 대한 결론도출근거 상의 설명 누락은 위원회의 적법 절차 위반입니다.", "articles": [], "principle": "제정 적법 절차 준수", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "국세청 기소 대상이 아닙니다.", "articles": [], "principle": "기소 권한 부재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기준서 자동 무효화와는 무관합니다.", "articles": [], "principle": "기준서 유효성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "금감원 자산 몰수 대상이 아닙니다.", "articles": [], "principle": "자산 몰수", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "개념체계와 K-IFRS 기준서의 지위 하에서 회계정책의 변경(Accounting Policy Change)이 발생할 때, 개념체계가 미치는 한계적 영향으로 옳은 것은?",
        "options": [
          "① 개념체계의 개정 소식만으로 기업은 기존의 모든 합리적 회계정책을 의무적으로 변경해야 한다.",
          "② 개념체계는 회계정책 변경의 직접적 법적 강제 사유가 될 수 없으며, 변경은 특정 기준서의 개정이나 기업의 자발적 유용성 향상 입증이 있을 때만 가능하다.",
          "③ 변경 시 발생하는 감가상각 금액의 차액은 전액 국세청에서 특별 소급 환급해 준다.",
          "④ 회계정책을 변경하려면 전 세계 모든 주주의 100% 서면 합의서가 제출되어야만 유효하다.",
          "⑤ 개념체계의 위상 상 변경된 회계정책은 오직 가치평가 모형에만 적용될 수 있고 원가 계산에는 배제된다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준서가 아니므로 개념체계 단독 개정만을 원인으로 회계정책 변경 의무가 발생하지 않습니다. 변경은 기준서의 개정 요건이나 기업의 자발적 유용성 증가 입증 요건(기준서 제1008호 등)에 부합해야 합니다.\n\n[오답 해설]\n① 개념체계 개정만으로 변경 의무가 강제되지 않습니다.\n③ 세무 환급과 무관합니다.\n④ 주주 100% 서면 합의 요건은 상법 상 존재하지 않는 잘못된 요건입니다.\n⑤ 원가 계산 등 재무제표 전반에 회계정책 변경이 적용될 수 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "개정 소식만으로 변경이 강제되지 않습니다.", "articles": [], "principle": "개정 한계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계는 기준서가 아니므로 회계정책 변경의 법적 강제 근거가 되지 못합니다.", "articles": [], "principle": "회계정책 변경 요건", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 환급과 관련 없습니다.", "articles": [], "principle": "세무 환급", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주주 100% 동의 요건이 아닙니다.", "articles": [], "principle": "주총 요건", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "원가 계산에도 적용 가능합니다.", "articles": [], "principle": "적용 범위", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "개념체계와 한국채택국제회계기준(K-IFRS)의 관계에 대하여 전 세계 규제기관(Regulatory Bodies)들이 인식하는 공식 지위로 옳은 것은?",
        "options": [
          "① 규제기관들은 개념체계 조항을 위반한 기업에게 형사 사법권을 직접 발동하여 처벌한다.",
          "② 개념체계에 기반한 일관된 회계기준은 자본시장 참여자 간의 정보 격차를 줄이고 투명성을 높여 규제기관의 시장 감독에 매우 유용하고 중요하게 취급된다.",
          "③ 규제기관들은 개념체계의 내용을 완전히 무시하고 오직 세법 단독 수치로만 감독을 진행한다.",
          "④ 규제기관은 기업들에게 분기별로 개념체계 필기시험을 치르게 하여 점수를 공시하도록 강제한다.",
          "⑤ 규제기관의 권고에 따라 개념체계는 매년 무기한 무효화가 선포될 수 있는 가변적 규칙이다."
        ],
        "answer": "2",
        "explanation": "② 전 세계 자본시장 규제기관들은 투명성과 효율성을 촉진하는 개념체계 기반 기준서(K-IFRS 등)를 정보의 신뢰성과 비교가능성을 제공하는 매우 중요한 근거로 인정하고 이를 공공이익을 위해 활용합니다.\n\n[오답 해설]\n① 개념체계는 형사 사법권 적용 법률이 아닙니다.\n③ 규제기관들은 세법과 별도로 자본시장 공시 감독 시 회계기준을 엄격히 적용합니다.\n④ 회계 필기시험 공시 강제 제도는 존재하지 않습니다.\n⑤ 규제기관이 개념체계를 임의로 전면 무효화 선포하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "사법권 발동 대상이 아닙니다.", "articles": [], "principle": "사법 처벌", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "규제기관들은 개념체계에 기반한 회계기준이 자본시장 투명성에 기여하므로 중요하게 여깁니다.", "articles": [], "principle": "규제기관의 인식", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세법 수치로만 공시 감독하지 않습니다.", "articles": [], "principle": "공시 감독", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "필기시험 공시 제도는 허구입니다.", "articles": [], "principle": "공시 요건", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "무효화 선포 권한과 관계없습니다.", "articles": [], "principle": "개념체계 위상", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "개념체계와 K-IFRS 기준서의 지위 상, 개념체계가 제시하는 재무제표의 '계속기업가정(Going Concern Assumption)'과 기준서 규정의 관계에 관한 설명으로 옳은 것은?",
        "options": [
          "① 계속기업가정은 개념체계의 전제조건일 뿐이며, 특정 기준서가 이를 명시적으로 거부하더라도 무조건 역사적 원가 평가를 강제한다.",
          "② 일반적으로 계속기업을 전제로 재무제표를 작성하지만, 청산이 임박하는 등 타당한 사유가 발생한 경우 기준서에 따라 대체 기준(청산가치 등)으로 기재하며 그 사실을 주석 공시해야 한다.",
          "③ 기업이 청산되더라도 개념체계 준수를 위해 평생 동안 동일한 방법으로 감가상각 장부를 유지 공시해야 한다.",
          "④ 계속기업 가정이 깨어지는 즉시 회사는 법원으로부터 파산 징역형을 자동 선고받는다.",
          "⑤ 회계기준위원회는 계속기업가정을 위반한 모든 기업의 이름을 일간지에 강제 공고하여 시장에서 영구 추방한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 계속기업가정을 기본 전제로 삼지만, 기업이 경영 활동을 중단해야 하거나 청산 절차를 밟아야 하는 경우 계속기업 전제를 배제하고 다른 적절한 측정 기준(청산가치 등)에 따라 재무제표를 작성해야 함을 인정하며, 이 사실을 투명하게 주석 보고해야 합니다.\n\n[오답 해설]\n① 청산 임박 시 역사적 원가 감가상각을 억지로 강제하지 않습니다.\n③ 청산 시에는 기존 상각 장부 유지가 불합리하므로 적절한 가액으로 대체 평가합니다.\n④ 계속기업 가정 탈락이 형사 파산 징역형 사유가 아닙니다.\n⑤ 일간지 강제 추방 공고 등의 사법 조치 권한이 위원회에 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "청산 시 역사적 원가 고수는 타당하지 않습니다.", "articles": [], "principle": "역사적 원가 한계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "계속기업 가정이 성립하지 않을 때에는 대안적 기준에 따라 작성하고 관련 사실을 밝혀야 합니다.", "articles": [], "principle": "계속기업가정 예외 처리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "청산 기업에 상각 장부 강제는 위반입니다.", "articles": [], "principle": "자산 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "형사 징역형 자동 선고는 허구입니다.", "articles": [], "principle": "사법 형법", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "일간지 영구 추방 등의 강제는 위원회 권한 밖입니다.", "articles": [], "principle": "행정 제재", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },

    # =========================================================================
    # L3: 적용 및 상황 판단형 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s02-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "(시나리오) A사의 신임 회계사 강 대리는 '제조 설비에 부착하는 특수 촉매제'의 회계 처리를 검토하고 있다. 이에 대해 명시적으로 정한 K-IFRS 기준서 규정이 없다. 강 대리가 취한 의사결정 중 개념체계에 비추어 가장 적법한 행동은?",
        "options": [
          "① 관련 세법상의 상각 방식 중 올해 회사 법인세를 가장 많이 환급해 주는 임의 산식을 선택하여 일시 비용 처리한다.",
          "② 촉매제의 물리적 실질과 경제적 실질이 자산의 정의(과거 사건 결과, 기업 통제, 미래 유입)를 충족하는지 개념체계를 분석하여 합리적 자체 회계정책을 수립한다.",
          "③ 감사 회계법인에게 전화를 걸어 \"기준서가 없으므로 회계법인이 장부를 직접 작성해 달라\"고 요청한다.",
          "④ 해당 거래 금액이 장부에 기록되면 결산이 늦어지므로 장부 누락을 결정한다.",
          "⑤ 기준서가 없으므로 해당 촉매제를 타사에 허위 매각한 것으로 위장 장부를 조작한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 기준서가 명시적으로 존재하지 않는 특수한 거래는 재무제표 작성자가 개념체계(자산·부채 정의, 인식 기준 등)를 지침으로 삼아 일관되고 목적적합한 회계정책을 자체 수립해 적용해야 합니다.\n\n[오답 해설]\n① 법인세 환급만을 위해 자의적인 산식을 남용해 비용 처리해서는 안 됩니다.\n③ 감사인에게 장부의 대리 작성을 위임하는 것은 감사 독립성 원칙에 위배됩니다.\n④, ⑤ 장부 누락이나 위장 매각 거래 기재 등은 위법입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "세금 환급 목적의 자의적 처리는 불허됩니다.", "articles": [], "principle": "회계정책", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서 부재 시 개념체계의 목적과 요소 정의에 따라 유용한 정책을 작성자가 개발해야 합니다.", "articles": [], "principle": "기준서 부재 시 회계정책 개발", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사인의 장부 대리 작성은 감사 윤리 위반입니다.", "articles": [], "principle": "감사 독립성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장부 누락은 분식회계입니다.", "articles": [], "principle": "장부 기재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "허위 위장 거래 기재는 불법입니다.", "articles": [], "principle": "위법 행위", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "(시나리오) B사의 감사인 박 회계사는 B사의 '자산 재평가 회계처리'에 대하여, K-IFRS 기준서의 지침이 존재함에도 불구하고 \"개념체계의 표현충실성 정의를 우선적으로 고려해야 하므로 기준서의 역사적 원가 조항을 즉시 배제하고 재평가모형으로 수정 기재해야 한다\"고 강요했다. 이에 대한 B사 재무팀의 올바른 대응 논리로 옳은 것은?",
        "options": [
          "① 감사인이 의견거절을 주겠다고 압박하므로 K-IFRS를 무시하고 재평가 모형으로 수정한다.",
          "② 개념체계는 특정 기준서의 지침에 우선하지 않으므로, 명시된 기준서 조항을 배제하고 개념체계만을 우선 적용하라는 감사인의 주장은 부당함을 지적한다.",
          "③ 상충 문제를 해결하기 위해 거래 가격 전체를 부외자산으로 숨겨 장부에서 지운다.",
          "④ 두 규정이 상충하므로 양자가 지시하는 수치들의 평균을 내어 주석 기재한다.",
          "⑤ 감사인에게 거래 가격의 10%에 달하는 고액 감사 성과급을 약속하고 설득한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준서에 우선하지 못하므로, 명시적인 K-IFRS 기준서가 유효하게 존재하고 있다면 기업은 감사인의 부적절한 주장을 거부하고 기준서 조항에 맞게 적법하게 기재해야 합니다.\n\n[오답 해설]\n① 감사인의 부당 압박에 굴하여 기준서를 위배해서는 안 됩니다.\n③ 자산 은폐(부외자산)는 명백한 불법 행위입니다.\n④ 임의적인 수치 절충 및 주석 계상은 불허됩니다.\n⑤ 성과급(뇌물) 약속은 범죄 행위입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기준서 위반 지시는 따를 수 없습니다.", "articles": [], "principle": "감사 압박 대처", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계는 기준서에 우선할 수 없으므로 기존 기준서 규정을 따르는 것이 정당합니다.", "articles": [], "principle": "개념체계 위상 적용", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자산 은폐는 불법입니다.", "articles": [], "principle": "자산 누락", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "산술 평균 계상은 불가합니다.", "articles": [], "principle": "회계 오류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "뇌물 약속은 불법입니다.", "articles": [], "principle": "뇌물", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "(시나리오) 주주 C는 C사가 공시한 기말 재무제표의 유형자산 감가상각 누계액 수치가 최근 개정된 개념체계의 자산 제거 정의 방향과 배치된다며 해명을 요구했다. C사 재무팀이 주주 C의 오해를 풀어주기 위해 설명할 수 있는 가장 적합한 회계학적 해명은?",
        "options": [
          "① 주주 C의 권리를 인정하여, 즉시 이번 장부를 파기하고 신 개념체계에 맞춰 소급 재작성해 주겠다고 약속한다.",
          "② 개념체계의 개정이 기존 K-IFRS 기준서를 자동으로 수정하는 것은 아니므로, 관련 기준서가 정식 개정되기 전까지는 기존 기준서를 적법하게 준수하여 보고했음을 설명한다.",
          "③ 개념체계 개정일 이후에 발생한 모든 감가상각비를 주주 C의 개인 계좌로 전액 현금 환급해 주겠다고 제안한다.",
          "④ 해당 상각 누계액 수치를 장부에서 은밀히 지우고 타 손실 계정으로 합산 보고한다.",
          "⑤ 위 상충 상황을 금융감독원에 제소하여 해당 개념체계 개정안 전체를 취소시켜 주겠다고 설명한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계가 개정되어도 기존 회계기준서가 자동으로 변경되는 것은 아닙니다. 따라서 기존에 적법하게 수립되어 유효한 기준서 조항을 따라 재무제표를 공시한 것은 완전히 올바르며, 소급 수정하지 않는 것이 타당합니다.\n\n[오답 해설]\n① 기준서 미개정 상태에서 개념체계 개정을 원인으로 임의 소급 수정하는 것은 기준서 위반입니다.\n③ 주주 개인 환급 약속은 터무니없는 배임 행위입니다.\n④ 임의의 손실 합산은 분식회계에 해당합니다.\n⑤ 개념체계 취소 제소는 불가능한 조치입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "임의의 소급 수정은 회계 오류입니다.", "articles": [], "principle": "장부 수정", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계 개정이 기준서를 자동 변경하지 않으므로 기존 기준서에 따라 처리한 것을 주주에게 해명해야 합니다.", "articles": [], "principle": "개념체계 개정 영향 해명", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주주 개인 배임은 불법입니다.", "articles": [], "principle": "배임 행위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "손실 임의 합산은 분식회계입니다.", "articles": [], "principle": "계정 분류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "금감원에 개념체계 취소 소송은 불가합니다.", "articles": [], "principle": "행정 사법", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "(시나리오) 한국회계기준위원회는 목적적합한 금융 거래 정보 제공을 위해 새로운 리스 기준서를 제정하면서, 불가피하게 개념체계의 자산 정의를 일탈(Deviation)시켰다. 그러나 위원회는 해당 기준서의 결론도출근거에 그 일탈에 대한 구체적 설명을 누락했다. 이 상황에 대한 정당한 분석으로 옳은 것은?",
        "options": [
          "① 일탈에 대한 결론도출근거 설명이 누락된 것은 회계기준원 제정 절차(Due Process) 상의 오류이자 결함에 해당한다.",
          "② 설명 누락과 무관하게 기준서 본문만 통과되었으므로 어떠한 행정적 절차 하자도 존재하지 않는다.",
          "③ 즉시 해당 리스 기준서의 효력은 소급 무효화가 되어 사용할 수 없다.",
          "④ 금융감독원장이 직권으로 금융사들의 리스 회계 처리를 3년간 강제 유예 명령을 내려야 한다.",
          "⑤ 위원회 소속 연구원들을 국세청에서 특별 감금 처벌할 법적 근거가 된다."
        ],
        "answer": "1",
        "explanation": "① 회계기준위원회가 개념체계와 다른 요구사항을 정한다면 해당 기준서의 결론도출근거에 그러한 일탈에 대해 설명할 것이 요구됩니다. 이의 누락은 적법 절차(Due Process) 상의 오류 및 결함입니다.\n\n[오답 해설]\n② 결론도출근거에 관련 기술을 명시해야 하므로 절차 하자가 존재합니다.\n③ 절차 하자가 즉각적인 기준서 효력 상실(소급 무효)을 뜻하지는 않으며, 보완 및 재공고 절차가 요구됩니다.\n④, ⑤ 금감원장의 유예 명령이나 국세청의 특별 감금 처벌은 법적 근거가 없는 잘못된 지문입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "일탈 발생 시 결론도출근거 기재 누락은 제정 기구의 명백한 절차적 흠결입니다.", "articles": [], "principle": "제정 적법 절차 위반", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "설명 누락은 절차상 하자가 맞습니다.", "articles": [], "principle": "절차 하자", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기준서의 즉각적 자동 무효화와는 다릅니다.", "articles": [], "principle": "기준서 효력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "금감원장의 유예 명령 대상이 아닙니다.", "articles": [], "principle": "행정 명령", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사법적 형벌(특별 감금) 대상이 아닙니다.", "articles": [], "principle": "사법권 적용", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "(시나리오) E사는 기계장치의 처분과 관련한 K-IFRS 기준서상의 '선택 가능한 두 가지 회계 대안'을 가지고 매년 자사 실적에 따라 유리하게 번복 적용하여 보고해왔다. 이에 대해 투자자 F가 이의를 제기했을 때, 개념체계에 비추어 E사가 지켜야 할 일관성(Consistency)과 비교가능성(Comparability)의 올바른 해석은?",
        "options": [
          "① 번복 적용은 주주가치의 극대화를 위해 기업에 정당하게 부여된 회계정책 자율권에 속한다.",
          "② 일관성은 비교가능성이라는 목표를 달성하는 수단이므로, 선택지가 허용되더라도 정당한 이유 없이 번복하지 않고 일관되게 정책을 유지해야 비교가능성이 저해되지 않는다.",
          "③ 투자자 F의 이의가 있으므로 두 모형의 정중앙 가격 수치로 전년도 장부를 영구 소급 고정 적용한다.",
          "④ 감세 목적에 맞다면 어떠한 번복 적용도 회계기준 위반 오류가 될 수 없다.",
          "⑤ 일관성은 단순히 개념체계의 하위 낙서에 불과하므로 번복 적용을 자유롭게 해도 무방하다."
        ],
        "answer": "2",
        "explanation": "② 일관성은 비교가능성을 유도하기 위한 구체적 방법입니다. 타당한 사유(예: 기업 상황의 중대한 변화, 기준서 변경 등) 없이 단순히 이익 조정을 목적으로 선택적 정책을 매년 번복하면 비교가능성이 심각하게 저해되므로 금지됩니다.\n\n[오답 해설]\n① 자의적인 매년 정책 번복은 정당한 회계정책 자율권이 아닙니다.\n③, ④ 임의 중앙값 소급 기재나 감세 목적의 임의 정책 변경은 회계 오류입니다.\n⑤ 일관성은 정보의 유용성 보강을 위한 핵심 개념적 지침입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "자의적 매년 변경은 허용되지 않습니다.", "articles": [], "principle": "회계 변경", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "일관성은 비교가능성을 확보하기 위한 수단이므로 합리적 사유 없이 정책을 번복하면 안 됩니다.", "articles": [], "principle": "일관성 유지 의무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "산술 평균 소급 고정은 오류입니다.", "articles": [], "principle": "회계 오류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세금 목적 변경은 불허됩니다.", "articles": [], "principle": "회계 변경 제한", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "일관성은 중요 개념입니다.", "articles": [], "principle": "일관성 위상", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "(시나리오) 다국적 펀드 투자자 H는 동종 업계의 I사와 J사의 '재무적 강점과 약점'을 비교 분석하려 한다. I사는 K-IFRS 기준서 규정을 엄격히 준수했고, J사는 \"개념체계의 원리가 더 마음에 든다\"는 이유로 기준서 규정을 배제한 채 개념체계만을 앞세워 장부를 작성했다. H가 두 회사의 장부를 분석한 후 내린 결론 중 개념체계에 비추어 올바른 판단은?",
        "options": [
          "① J사가 개념체계를 사용하였으므로 J사의 장부 신뢰성과 국제 비교가능성이 I사보다 훨씬 높다.",
          "② J사의 장부는 명백히 유효한 K-IFRS 기준서를 배제하고 개념체계만을 우선 적용한 오류 장부이므로, H는 I사와 J사의 장부를 상호 비교 분석할 수 없으며 J사 재무제표는 신뢰할 수 없다.",
          "③ 두 회사 장부의 감가상각 누계액을 합산 평균한 수치를 신규 기준으로 삼아 직접 재조정한다.",
          "④ 규정이 상충하므로 J사의 결산 장부 전체를 임시 파산 기업 장부로 처리한다.",
          "⑤ H는 금융감독원에 두 회사의 주식 거래를 즉시 정지시킬 것을 법적으로 강제 지시한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준에 우선하지 못합니다. 따라서 기준서가 유효함에도 이를 배제한 채 작성한 J사의 재무제표는 기준서 위반 오류에 해당하며, 두 기업 간의 신뢰성 있는 비교분석을 불가능하게 만듭니다.\n\n[오답 해설]\n① 기준서 위반 장부이므로 비교가능성이 저해되며 오류 상태입니다.\n③ 투자자가 임의로 기업 장부의 감가상각비를 합산 재조정 공시하지 않습니다.\n④ 파산 전제 장부로 임의 처리할 수 없습니다.\n⑤ 투자자에게 주식 거래 정지 강제 지시 권한이 있지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "기준서 위반 장부가 우월할 수 없습니다.", "articles": [], "principle": "비교 우위 오류", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서를 이탈하여 개념체계만으로 작성된 장부는 위반 오류 상태이므로 상호 비교 분석이 불가능합니다.", "articles": [], "principle": "기준서 위반과 비교가능성 저해", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의 재조정은 투자자 소관이 아닙니다.", "articles": [], "principle": "재조정 불가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "파산 장부 분류는 불가합니다.", "articles": [], "principle": "파산 기준", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "거래 정지 지시 권한이 없습니다.", "articles": [], "principle": "거래소 권한", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "(시나리오) 소송 대리인 K 변호사는 자신이 자문하는 기업 L사의 회계 소송(기말 자산 누락 혐의) 변론을 준비하고 있다. 기말 자산 누락은 관련 특정 K-IFRS 기준서의 세부 요건을 엄격히 해석한 적법한 처리였으나, 개념체계의 자산 정의 범위보다는 좁았다. K 변호사가 개념체계의 위상에 기초하여 변론서에 작성할 법적 방어 논리로 옳은 것은?",
        "options": [
          "① \"개념체계의 자산 정의 범위가 기준서보다 넓으므로, 자산을 무조건 인식하지 않은 L사는 형법 상 사기 혐의가 자동 유죄 선고되어야 마땅하다.\"",
          "② \"개념체계는 회계기준서가 아니며 어떠한 요구사항도 기준서에 우선하지 못하므로, 명시적인 K-IFRS 기준서의 지침에 완벽하게 부합하게 자산을 미인식한 처리(누락)는 명백히 합법적이고 적법한 회계 처리이다.\"",
          "③ \"L사는 상충 상황을 해결하기 위해 이사진 전원의 급여를 세금 면제 처리하여 국가에 기부하겠다.\"",
          "④ \"두 조항의 충돌로 인해 L사의 이번 기말 재무제표는 자동 무효화되었음을 자백한다.\"",
          "⑤ \"사법부는 개념체계를 세법과 즉각 통합시켜 새로운 형사 처벌 법안을 발의해야 한다.\""
        ],
        "answer": "2",
        "explanation": "② 특정 K-IFRS 기준서의 요구사항은 개념체계에 항상 우선하므로, 기준서 요건에 완벽히 부합하게 자산을 인식하지 않은 것은 위반이 아닌 완전히 적법한 회계적 처리입니다.\n\n[오답 해설]\n① 기준서 미충족으로 미인식한 것을 사기죄 유죄로 볼 수 없습니다.\n③ 급여 세금 면제 기부 주장은 변론 논리가 될 수 없습니다.\n④ 상충으로 재무제표가 소급 자동 무효화되지 않습니다.\n⑤ 사법부의 형사 법안 직접 발의 등은 사법 체계 상 존재하지 않는 지문입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "사기 유죄 논리는 타당하지 않습니다.", "articles": [], "principle": "사법 형사", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서 요건에 부합하게 미인식 처리한 것은 개념체계에 우선하는 기준서의 법적 효력 상 완전히 적법합니다.", "articles": [], "principle": "기준서의 절대적 유효성 변론", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기부 주장은 무관합니다.", "articles": [], "principle": "기부", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자동 무효화 자백은 부적절합니다.", "articles": [], "principle": "재무제표 효력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "법안 발의 주장은 오류입니다.", "articles": [], "principle": "입법부 권한", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "(시나리오) M사는 '보고기간후사건'과 관련하여 법인세법 기준(세제 징수)과 K-IFRS 기준서 규정의 명백한 회계적 불일치를 겪고 있다. 기말 결산 시 M사의 정 대리가 내린 회계적 판단 중 개념체계에 비추어 올바른 판단은?",
        "options": [
          "① 법인세법이 언제나 공시에도 우선하므로 세법 방식대로 재무제표의 자산 가액을 직접 수정 기재한다.",
          "② 세법과 무관하게 외부보고용 재무제표는 명시된 K-IFRS 기준서에 전적으로 부합하게 공시하고, 세법과의 불일치는 별도의 세무조정 명세서 및 이연법인세를 활용해 회계 처리한다.",
          "③ 세법 충돌을 우려해 기말 자산을 전액 현금으로 환전하여 비밀 금고에 넣어 숨긴다.",
          "④ 두 규정을 정반반씩 섞어 자의적으로 가공한 신종 자산 계정을 생성한다.",
          "⑤ 국세청에 직접 전화를 하여 세법 기준 감가상각 규정을 개념체계와 똑같이 고쳐 달라고 요구하며 공시를 무기한 유예한다."
        ],
        "answer": "2",
        "explanation": "② 과세 소득 계산을 위한 법인세법 기준과 일반목적 재무보고서 기준은 서로 독립적이므로 재무제표는 기준서(K-IFRS)에 맞춰 온전히 작성하고 차액은 세무조정으로 조율하는 것이 맞습니다.\n\n[오답 해설]\n① 세법 방식을 재무제표에 강제 적용하여 기준서를 위배해서는 안 됩니다.\n③ 자산 현금 환전 후 은닉은 횡령 및 분식회계입니다.\n④ 임의 가공 계정 생성은 불허됩니다.\n⑤ 국세청에 상각 규정 수정 요구를 빌미로 결산 공시를 유예할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "세법이 재무보고 공시 기준을 대체할 수 없습니다.", "articles": [], "principle": "세법 관계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무제표는 기준서에 따라 적법하게 작성하고 세법 차이는 세무조정 명세서로 대체 조율합니다.", "articles": [], "principle": "세법과 회계의 분리 준수", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자산 은닉은 횡령 배임입니다.", "articles": [], "principle": "자산 은닉", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "가공 계정은 분식회계입니다.", "articles": [], "principle": "분식회계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "공시 유예는 불가합니다.", "articles": [], "principle": "적시 공시", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "(시나리오) 글로벌 투자사 O는 한국 기업 P사의 회사채를 매수할지 고민하고 있다. P사는 국제적 합의가 완료된 개념체계에 충실하게 기반한 회계기준(K-IFRS)을 사용해 재무제표를 공시해왔다. O가 이 정보에 기초해 내린 재무적 판단으로 옳은 것은?",
        "options": [
          "① P사가 국제 공인 회계기준을 쓰더라도 정보 격차가 언제나 100% 차단되지는 않으므로 투자 의사결정 시 추가적인 모니터링이 필요하다. 그러나 단일 회계 언어로 신뢰성과 비교가능성이 제고되어 정보 획득 자본비용이 감소한 이득이 있다.",
          "② K-IFRS 사용으로 P사의 투자 원금 상환 리스크가 자동으로 0원이 되므로 무조건 전 자산을 채권 매수에 투입한다.",
          "③ P사의 장부 순자산 가액이 실제 시가와 100% 정확히 일치함을 확인하고 가치 평가 단계를 건너뛴다.",
          "④ 개념체계 사용 기업의 채무는 상법 상 무조건 국가가 지급 보증하므로 보증서 발급을 요구하지 않는다.",
          "⑤ P사의 회계처리가 개념체계를 썼으므로 어떠한 감사 한계도 존재하지 않는 완벽한 정확성을 보장한다고 굳게 믿는다."
        ],
        "answer": "1",
        "explanation": "① 개념체계에 기반한 회계기준의 준수는 투자자의 자본비용을 경감하고 비교가능성을 높여 유용하지만, 재무보고의 근본적인 한계(정보의 격차 존재, 추정과 판단의 한계)로 인해 여전히 적절한 모니터링 분석이 수반되어야 합니다.\n\n[오답 해설]\n② 투자 리스크가 자동으로 0원이 될 수 없습니다.\n③ 장부 순자산과 실제 시가는 일치하지 않습니다.\n④ 국가가 채권 지급 보증을 하지 않습니다.\n⑤ 재무보고서는 추정, 판단, 모형에 근거하므로 완벽한 정확성을 절대적으로 보장하지 못합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "단일 회계기준 준수로 자본비용이 감소하나 재무보고의 근본적 한계를 파악하고 추가 분석을 병행해야 합니다.", "articles": [], "principle": "자본비용 경감 및 재무보고 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "리스크가 0원이 될 수 없습니다.", "articles": [], "principle": "리스크", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장부금액과 시가는 일치하지 않습니다.", "articles": [], "principle": "가치평가 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "국가 지급 보증과 관계없습니다.", "articles": [], "principle": "지급 보증", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "완벽한 절대적 정확성은 제공 불가합니다.", "articles": [], "principle": "추정의 한계", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "(시나리오) R사는 기말 결산 평가 시 상당한 '추정과 판단(Estimates and Judgments)'이 들어가는 대손충당금 설정 모형을 사용하고 있다. R사의 재무부장 이 상무는 개념체계의 추정 지침을 준수하기 위해 대손 설정을 관리하려 한다. 이 상무가 취해야 할 개념체계에 비추어 올바른 의사결정은?",
        "options": [
          "① 추정은 재무 정보의 정확성을 해치므로, 대손 설정을 전면 취소하고 오직 돈이 떼이는 날에만 현금주의 방식으로 즉시 비용 처리한다.",
          "② 추정이 명확하고 정확하게 기술되고 추정의 한계와 성격이 주석으로 잘 설명되는 한 정보의 유용성을 저해하지 않으므로, 합리적이고 일관된 모형을 사용해 충당금을 적절히 계상한다.",
          "③ 대손율을 매년 경영진 임의대로 0%에서 80% 사이에서 조작하여 당기 실적을 인위적으로 통제한다.",
          "④ 감사인이 권고하는 특정 대손율 공식 10%를 검토 없이 받아들이고, 책임 면제 계약서를 별도로 감사인과 작성한다.",
          "⑤ 추정치 기재를 숨기기 위해 대손충당금 항목을 장부에서 숨겨 부외자산으로 차감 기록한다."
        ],
        "answer": "2",
        "explanation": "② 추정과 판단은 재무제표 작성에 필수적인 부분이며, 추정의 기초와 한계가 명확하게 기재 및 설명되는 한 재무보고의 질적 유용성을 저해하지 않습니다. 따라서 합리적 모형을 통한 대손 충당 계상이 타당합니다.\n\n[오답 해설]\n① 현금주의로 자의적 대체 처리해서는 안 됩니다.\n③ 자의적인 충당금 비율 조정 조작은 분식회계입니다.\n④ 감사인의 책임 면제 계약 등은 법적 효력이 없습니다.\n⑤ 충당금을 은폐 기록하는 것은 분식회계입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "현금주의 강제는 불가합니다.", "articles": [], "principle": "발생기준 적용", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "추정이 합리적 절차에 기초하고 투명하게 설명된다면 정보 유용성에 부합합니다.", "articles": [], "principle": "추정치의 유용성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적 실적 조작은 분식회계입니다.", "articles": [], "principle": "이익 조정 금지", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사인 책임 면제는 성립하지 않습니다.", "articles": [], "principle": "감사 책임", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "부외 자산 은폐는 불법입니다.", "articles": [], "principle": "자산 은폐", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "(시나리오) 자회사 S는 기말 결산 시 모회사 T의 '수주 계약 회계정책'을 아무런 검토 없이 그대로 무단 적용하여 당기 수익을 인식했다. 그러나 모회사 T사가 적용한 방식은 해당 거래의 특수 기준서 요구사항을 일부 위배한 단순 개념체계 지문 짜깁기 정책에 불과했다. 자회사 S사가 유발한 오류의 교정 방향으로 옳은 것은?",
        "options": [
          "① 모회사의 결정을 무단 적용한 것은 자회사로서의 정당한 지배 구조 의무 준수이므로 오류가 아니다.",
          "② 모회사의 짜깁기 정책은 명백한 기준서 위배이므로, 자회사 S사는 모회사의 기준서 위반 정책을 즉시 폐기하고 올바른 K-IFRS 기준서 규정을 준수하여 수익 인식을 소급 수정하여 공시해야 한다.",
          "③ 감사인의 서면 동의를 얻어 당기 수익을 전액 사외 적립금으로 조작 이전한다.",
          "④ 해당 거래 장부 전체를 임시 파산 장부로 강제 분류하여 보관한다.",
          "⑤ 금감원에 모회사와 자회사의 모든 주식 거래 정지 해제 명령서 발급을 요청한다."
        ],
        "answer": "2",
        "explanation": "② 지배기업(모회사)의 잘못된 회계정책 적용을 종속기업(자회사)이 그대로 따랐다 하더라도 이는 동일한 기준서 위반 오류에 해당합니다. 자회사는 독립된 작성 주체로서 오류를 적법한 기준서 조항에 맞게 즉시 소급 수정 공시하여 교정해야 합니다.\n\n[오답 해설]\n① 지배 구조 복종을 이유로 회계 위반이 정당화될 수 없습니다.\n③ 수익 조작 이전은 불법입니다.\n④ 임의 파산 장부 분류는 허용되지 않습니다.\n⑤ 거래 정지 등은 금감원 질의 사유와 직접 매핑되지 않는 무관한 지문입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "지배구조 복종이 회계 기준 위반을 면제하지 않습니다.", "articles": [], "principle": "종속기업 책임", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "지배기업의 오류 정책을 그대로 수용한 것도 위반이므로 올바른 기준서 규정에 맞춰 자회사가 직접 소급 수정해야 합니다.", "articles": [], "principle": "연결 및 개별 회계오류 교정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사외 적립금 임의 조작은 위법입니다.", "articles": [], "principle": "계정 조작", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의 파산 분류는 불가합니다.", "articles": [], "principle": "회계 분류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "거래 정지 요청은 부적합합니다.", "articles": [], "principle": "감독 기구", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "(시나리오) 금융감독원 회계감리반 U는 V사가 개념체계의 질적 특성을 주장하며 명백히 명시된 기준서 조항의 '평가 손실 인식'을 누락한 사실을 확인하고 감리 적발 처분을 진행했다. 감리반 U의 V사에 대한 시정 조치 명령 및 벌금 부과 타당성 분석으로 가장 옳은 것은?",
        "options": [
          "① V사가 개념체계를 사용하였으므로 감리반 U의 적발 처분은 전적으로 위법하며 즉시 취소되어야 한다.",
          "② 개념체계는 회계기준서에 우선하지 못하므로, V사의 평가손실 누락은 명백한 회계기준 위반이 맞고 감리반 U의 적시 시정 명령 및 행정 제재 조치는 법적으로 매우 타당하다.",
          "③ 회계기준위원회 위원 전원을 동반 소환하여 법적 벌금을 임의 부과하는 것이 합당하다.",
          "④ 해당 거래 금액을 즉시 정부가 몰수하여 국가 예산에 귀속하는 명령을 내린다.",
          "⑤ V사에게 세무 세무조사 면제 특권을 영구 부여하여 사건을 종결한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 회계기준이 아닙니다. 기준서가 명백히 평가손실 인식을 강제하고 있다면 기업은 개념체계를 핑계로 이를 배제할 수 없습니다. 따라서 금감원 U의 감리 지적 및 시정 명령은 완전히 정당합니다.\n\n[오답 해설]\n① 감리반 U의 처분은 합법적입니다.\n③ 위원회 위원을 동반 벌금 기소하지 않습니다.\n④ 국가가 기업 재산을 압류하거나 예산 귀속 몰수를 할 수 없습니다.\n⑤ 세무조사 면제 권한을 금감원이 영구 부여할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "U의 처분은 적법합니다.", "articles": [], "principle": "감리 적법성", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "개념체계를 핑계로 기준서를 위배한 V사의 회계처리는 감리 적발 지적의 타당한 대상입니다.", "articles": [], "principle": "회계감리 및 제재 타당성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "위원회 위원 소환 벌금 부과는 불가합니다.", "articles": [], "principle": "위원회", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "정부의 자산 몰수는 위법입니다.", "articles": [], "principle": "사유재산 몰수", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무조사 면제 영구 부여는 불가능합니다.", "articles": [], "principle": "세무조사 면제", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "(시나리오) 청산 절차가 임박하여 계속기업 전제가 무너진 W사는 감가상각 관련 기존 K-IFRS 기준서의 역사적 원가 규칙 적용 여부를 검토하고 있다. W사의 강 대리가 내린 올바른 측정 의사결정으로 옳은 것은?",
        "options": [
          "① 개념체계의 역사적 원가 원칙은 청산 여부와 무관하게 무조건 강제 적용되어야 하므로 기존 장부 기록 방식을 억지로 고수한다.",
          "② 계속기업가정이 유지되지 않는 청산 상태이므로, 기준서 지침에 따라 역사적 원가 대신 청산 가치 등 대체적 측정 기준에 맞게 자산을 재평가하여 공시해야 한다.",
          "③ 청산 확정이므로 당해 결산 마감 및 재무보고서 제출을 전면 거부하고 방치한다.",
          "④ 기말 자산 전체를 장부에서 0원으로 지워 흔적을 말소한다.",
          "⑤ 세무서에 로비를 하여 청산 소득세를 탕감해 주면 계속기업 기준 장부를 작성하겠다고 제안한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 일반적으로 계속기업가정 하에서 장부를 작성함을 기본 전제로 하지만, 청산이나 활동 중단이 불가피한 경우 계속기업가정은 성립하지 않으므로 역사적 원가 대신 대체적인 적절한 측정 기준(청산가치 등)으로 전환해야 합니다.\n\n[오답 해설]\n① 청산 상황에서 역사적 원가를 억지로 고수하는 것은 오도하는 재무 정보를 만듭니다.\n③ 보고서 제출 거부 및 방치는 금지됩니다.\n④ 자산을 인위적으로 즉시 0원으로 소거하는 것은 위반입니다.\n⑤ 세무 세금 탕감 로비 등은 불법이며 타당한 의사결정이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "청산 상태에서 역사적 원가 고수는 부적합합니다.", "articles": [], "principle": "역사적 원가 한계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "계속기업 전제 상실 시 대체 기준인 청산가치 등으로 평가해 보고해야 유용합니다.", "articles": [], "principle": "계속기업 전제 상실의 처리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "제출 거부 방치는 위법입니다.", "articles": [], "principle": "제출 의무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장부 소거는 분식회계입니다.", "articles": [], "principle": "장부 관리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "로비 주장은 불법입니다.", "articles": [], "principle": "뇌물 및 로비", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "(시나리오) Y사는 정부로부터 '이산화탄소 저감 장치 무상 대여 혜택'을 제공받았으나, 현행 K-IFRS 기준서 상에 정부 대여 혜택의 자산·부채 인식과 관련한 구체적 요건 규정이 다소 모호하다. Y사의 회계팀 최 대리가 이 거래의 적법한 회계정책을 자체적으로 수립하려 할 때, 개념체계의 지침 적용 순서로 가장 타당한 것은?",
        "options": [
          "① 자의적으로 처리할 수 있으므로, 올해 회사 법인세 납부액을 최소화하는 산식을 임의 적용하여 주석 공시 없이 끝낸다.",
          "② 개념체계가 규정하는 일반목적재무보고의 목적과 자산·부채 정의, 그리고 인식 및 측정의 일반원칙에 모호한 거래가 부합하는지 정밀하게 부합 여부를 검토하여 일관된 회계정책을 설계 적용한다.",
          "③ 감사 회계법인의 실무 수습사원에게 전결권을 전면 위임하여 지시를 따른다.",
          "④ 해당 거래 금액을 타인의 사외 비밀 차명 계좌로 분산 송금하여 숨긴다.",
          "⑤ 기준서 개정안이 공표되어 공표될 때까지 당기 장부 기재를 전면 거부한다."
        ],
        "answer": "2",
        "explanation": "② 기준서의 세부 지침이 모호하거나 공백이 존재할 경우, 재무제표 작성자는 개념체계가 제시하는 목적, 정의, 인식 및 측정의 근본 원칙을 지침 삼아 회계정책을 자체 수립해 유용한 정보를 보고해야 합니다.\n\n[오답 해설]\n① 법인세 최소화를 목적으로 자의적 조작을 가해서는 안 됩니다.\n③ 감사인(실무 수습사원 포함)에게 회계정책 수립 책임을 전가하는 것은 부적절합니다.\n④ 사외 차명 비밀 계좌 사용 등은 횡령 및 범죄입니다.\n⑤ 기준서 개정 때까지 장부 기재를 거부할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "조세 포탈 성격의 정책 수립은 불가합니다.", "articles": [], "principle": "회계정책 수립", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서 모호 시 개념체계의 자산 정의 및 목적에 부합하게 자체 회계정책을 수립하는 것은 타당합니다.", "articles": [], "principle": "모호한 규정 하 정책 수립", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사인에게 권한 위임은 불가합니다.", "articles": [], "principle": "감사 위임", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "차명 계좌 사용은 불법입니다.", "articles": [], "principle": "차명 계좌", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장부 기재 거부는 불법입니다.", "articles": [], "principle": "장부 기재 의무", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "(시나리오) 회계학 교수 A와 석사 과정생 B는 세미나에서 '개념체계와 K-IFRS 기준서의 상충과 조화'를 토론하고 있다. B가 쓴 연구 계획서 중 개념체계에 비추어 볼 때 학술적 반박을 받을 수 있는 오류 지문은?",
        "options": [
          "① \"K-IFRS 기준서의 특정 조항이 개념체계와 불일치하는 것은 회계기준위원회가 실질 유용성을 도모하는 과정에서 정당하게 발생할 수 있는 정상적 현상이다.\"",
          "② \"개념체계와 상충하는 특정 기준서 규정은 자동 무효가 되며, 대리인 비용을 원천 차단하기 위해 주주들이 즉시 민사 소송을 제기할 수 있는 위법 조항이다.\"",
          "③ \"개념체계가 개정되더라도 자동으로 기존의 개별 회계기준이 개정되는 것은 아님을 명확히 분석해야 한다.\"",
          "④ \"회계기준위원회는 일탈 요구사항을 기준서로 지정할 때 결론도출근거에 관련 사실을 기재할 행정적 의무가 있다.\"",
          "⑤ \"재무제표 작성자는 명시적인 기준서가 있다면 개념체계와 다르더라도 기준서를 반드시 최우선 준수해야 한다.\""
        ],
        "answer": "2",
        "explanation": "② 개념체계와 상충하는 기준서가 존재하더라도 그 기준서의 법적 효력은 온전히 유지되며, 주주가 위법을 이유로 무효 민사 소송을 제기할 법적 하자가 되지 못합니다. 따라서 ②는 오류입니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 모두 개념체계와 기준서의 공식적 관계와 위상을 바르게 명시하고 있는 타당한 학술 지문들입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "위원회 일탈 타당성은 학술적으로 입증되어 있습니다.", "articles": [], "principle": "일탈의 의의", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "상충 기준서가 자동 무효가 되거나 민사 소송 대상 위법 규정이 되는 것은 완전한 오류 설명입니다.", "articles": [], "principle": "상충 기준서의 유효성과 학술 분석", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자동 개정 불인정은 옳은 지문입니다.", "articles": [], "principle": "개정 독립성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "결론도출근거 기재 의무는 옳은 지문입니다.", "articles": [], "principle": "결론도출근거", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기준서 최우선 준수 의무는 옳은 지문입니다.", "articles": [], "principle": "기준서 우선", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },

    # =========================================================================
    # L4: 분석 및 박스형 다중 조합 (8문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s02-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "개념체계와 한국채택국제회계기준(K-IFRS)의 관계에 관한 설명 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 개념체계는 회계기준이 아니므로 특정 회계기준이나 요구사항에 우선하지 않는다.\nㄴ. 회계기준위원회가 개념체계와 벗어난 요구사항을 기준서로 지정하는 경우에도 해당 기준서의 효력은 법적으로 유효하다.\nㄷ. 회계기준위원회가 일탈 기준서를 정하는 경우, 결론도출근거에 관련 사실을 기재해야 하며 그렇지 않을 시 제정 절차적 하자가 발생한다.\nㄹ. 작성자는 명시적 기준서 조항이 있는 경우, 그것이 개념체계와 다르더라도 예외 없이 기준서 조항을 따라 회계처리해야 한다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "5",
        "explanation": "⑤ 보기의 ㄱ, ㄴ, ㄷ, ㄹ은 모두 개념체계와 K-IFRS 기준서의 지위 및 우선순위, 위원회 의무에 관한 명백히 옳은 조문 서술입니다.\n\n[보기 검증]\nㄱ. [참] 개념체계는 기준서가 아니며 우선하지 않습니다.\nㄴ. [참] 일탈 기준서도 명백한 법적 효력을 가집니다.\nㄷ. [참] 결론도출근거에 설명할 의무가 존재합니다.\nㄹ. [참] 기준서 규정이 최우선이므로 무조건 준수해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ, ㄹ 모두 참인 옳은 기술입니다.", "articles": [], "principle": "개념체계와 K-IFRS의 종합적 지위", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "개념체계의 수시 개정 및 기존 기준서에 미치는 영향에 대한 설명 중 옳지 않은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 개념체계가 개정되면 개정 즉시 상충되는 기존 K-IFRS 기준서는 자동으로 개정 처리된다.\nㄴ. 개념체계 개정일 직후 기존 기준서가 공식 수정되기 전까지는 개정된 개념체계를 우선 소급 적용하여 장부를 재평가해야 한다.\nㄷ. 회계기준위원회가 개념체계 개정 이후에 관련 기준서 개정의 필요성을 심의하여 독립적으로 제개정을 처리하는 절차는 정당하다.\nㄹ. 개념체계 개정으로 기존 자본시장의 적법한 회계처리를 강제 번복 수정하지 않는 것은 회계 시장의 일관성 및 신뢰성 보호를 위함이다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄷ",
          "③ ㄷ, ㄹ",
          "④ ㄱ, ㄴ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ"
        ],
        "answer": "1",
        "explanation": "① 옳지 않은 오답 지문은 ㄱ과 ㄴ입니다. 개념체계 개정이 기존 기준서를 자동으로 바꾸지 않으며, 소급 적용하여 장부를 강제 소급 재작성할 수도 없습니다. ㄷ, ㄹ은 정당한 지문입니다.\n\n[보기 검증]\nㄱ. [거짓] 자동으로 기준서가 개정되지 않습니다.\nㄴ. [거짓] 기준서 미개정 시에는 소급 적용해 장부를 수정해서는 안 됩니다.\nㄷ. [참] 독립적인 위원회의 심의 제개정 추진이 맞습니다.\nㄹ. [참] 자동 번복 차단으로 거래 신뢰를 보호합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "ㄱ과 ㄴ은 완전히 잘못된 설명이므로 옳지 않은 조합에 매핑됩니다.", "articles": [], "principle": "개념체계 개정 한계의 오류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ은 옳은 설명입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ, ㄹ은 모두 옳은 설명입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ은 옳은 설명입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ은 옳은 설명입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "회계기준위원회(KASB)의 공식 제정 절차와 관련해 결론도출근거(Basis for Conclusions)의 성격에 관한 분석 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 결론도출근거는 특정 기준서 본문의 예외적 일탈과 제정 이유를 밝히는 필수 공시 문서이다.\nㄴ. 결론도출근거에 기재된 일탈 사실은 개별 기업 작성자에게 특정 기준서를 무시하고 개념체계로 우회 적용할 수 있는 임의 대안을 부여하는 문서가 아니다.\nㄷ. 결론도출근거의 작성이 누락된 상태에서 일탈 조항만 기준서 본문으로 통과되면, 해당 기준서는 적법한 제정 절차(Due Process) 위반 하자가 성립한다.\nㄹ. 결론도출근거는 외부 감사인에게 감사 수수료를 한정 면제하게 규율하는 감사 계약 법률서의 효력을 가진다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "3 보기 중 옳은 지문은 ㄱ, ㄴ, ㄷ입니다. ㄹ의 경우 결론도출근거가 외부감사인의 감사 수수료나 감사인 계약을 법적으로 면제하는 효력을 가진다는 소관 외의 터무니없는 서술이므로 틀렸습니다.\n\n[보기 검증]\nㄱ. [참] 일탈 사실과 사유를 밝히는 중요한 공식 설명 문서입니다.\nㄴ. [참] 작성자에게 자의적 기준서 배제 대안을 허용하지 않습니다.\nㄷ. [참] 설명 누락은 공식 제정의 적법 절차적 결함입니다.\nㄹ. [거짓] 감사 수수료 및 계약은 사적 민사 계약이며 결론도출근거와 관련이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ은 틀린 지문입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ은 모두 결론도출근거의 성격과 역할을 바르게 설명합니다.", "articles": [], "principle": "결론도출근거 지위 분석", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ은 틀린 지문입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "개념체계와 한국채택국제회계기준(K-IFRS)의 관계에 대하여 작성자(Preparer) 및 외부감사인(External Auditor)의 법적 행동 원칙에 대한 설명 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 작성자는 유효한 개별 기준서 조항이 있는 한, 개념체계 조항과 상충하더라도 반드시 기준서를 준수하여 기재해야 한다.\nㄴ. 감사인은 작성자가 적법한 기준서를 따라 기재한 재무제표에 대해 개념체계와 일치하지 않는다는 개별 사유만으로 수정이나 거절 의견을 줄 권한이 없다.\nㄷ. 작성자는 특정 거래에 대해 명시적 기준서 지침이 없는 결손 공백이 발생하면, 개념체계를 준수하여 합리적인 회계정책을 자체 수립해 보고해야 한다.\nㄹ. 감사인은 작성자가 기준서가 부재한 거래에 대해 개념체계를 성실히 해석 적용해 수립한 회계정책이 타당한지 객관적으로 성실 검토할 의무가 있다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "5",
        "explanation": "⑤ 보기의 ㄱ, ㄴ, ㄷ, ㄹ은 모두 개념체계 위상 하에서 기업의 작성 담당자와 외부 회계감사인이 준수해야 하는 올바른 실무적 행동 원칙을 설명하고 있습니다.\n\n[보기 검증]\nㄱ. [참] 기준서 준수가 최우선 의무입니다.\nㄴ. [참] 기준서 적용 적정성에 대해 감사인이 자의적 요구를 강제할 수 없습니다.\nㄷ. [참] 기준서 부재 시 작성자의 수립 의무를 명시합니다.\nㄹ. [참] 자체 수립 정책의 합리성 준수 여부는 감사인의 적법한 감사 사항입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ, ㄹ 지문 모두 명백히 참입니다.", "articles": [], "principle": "작성자 및 감사인 행동준칙", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "개념체계 기반 회계기준 사용에 따라 투자자 및 규제기관이 얻게 되는 경제적 효율성(Efficiency)에 대한 설명 중 옳은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 단일의 개념체계 기반 회계 언어(K-IFRS)의 사용은 글로벌 투자자들이 각국 기업의 기회와 위험을 비교가능하게 파악하도록 돕는다.\nㄴ. 국제적 비교가능성 향상으로 해외 투자유치가 한결 용이해지며, 자본조달에 수반되는 자본비용을 감소시킨다.\nㄷ. 여러 국가별로 다르게 재무 보고서를 작성하여 이중 제출해야 하는 국제보고 비용을 실질적으로 절감시켜 준다.\nㄹ. 단일 회계 언어를 준수하면 자본 조달 시 발생하는 부채 리스크에 대해 국가가 100% 무상 예산 지급 보증을 직접 강제한다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "3 보기 중 옳은 지문은 ㄱ, ㄴ, ㄷ입니다. ㄹ의 경우 단일 회계기준 준수가 국가의 무상 부채 상환 지급 보증 효력을 유발한다는 잘못된 서술이 포함되어 있으므로 오답입니다.\n\n[보기 검증]\nㄱ. [참] 자본시장의 비교가능한 가치 파악을 도울 수 있습니다.\nㄴ. [참] 전 세계 비교가능성 향상으로 자본비용이 감소합니다.\nㄷ. [참] 단일 공시 언어 구축으로 행정 보고 비용이 절감됩니다.\nㄹ. [거짓] 국가의 무상 채무 변제 보증 혜택을 제공하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ은 개념체계 기반 기준서 적용의 효율성 이득을 바르게 진술합니다.", "articles": [], "principle": "효율성 이득 분석", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "K-IFRS 기준서에 명시적 지침이 존재하지 않는 신규 거래가 발생했을 때, 재무제표 작성자의 회계정책 수립 과정에 관한 분석 중 옳은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 작성자는 개념체계가 설정한 일반목적재무보고의 목적, 자산·부채의 요소 정의를 준수하여 정책을 수립해야 한다.\nㄴ. 관련 기준서 조항이 없다는 명분을 들며 해당 거래로 취득한 기말 자산을 장부에서 아예 누락하여 공시하는 판단은 금지된다.\nㄷ. 작성자가 회계정책을 자체 수립하더라도, 세법상의 법인세를 고의 최소화하기 위해 자의적인 평가 방식을 남용할 수 없다.\nㄹ. 회계기준위원회가 당해 거래에 관한 새로운 기준서를 나중에 공표하게 된다면, 자체 수립한 정책보다 신종 기준서 규정이 무조건 우선 적용되어야 한다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "5",
        "explanation": "⑤ 보기의 ㄱ, ㄴ, ㄷ, ㄹ은 모두 기준서 부재 시 작성자가 지켜야 하는 의사결정 원리와 신종 기준서 제정 상황에 대한 조치 방향에 관한 완전히 옳은 내용입니다.\n\n[보기 검증]\nㄱ. [참] 개념체계 원칙 준수 수립 의무가 있습니다.\nㄴ. [참] 자의적 누락은 중대한 공시 위반입니다.\nㄷ. [참] 자의적 세무 조작은 금지됩니다.\nㄹ. [참] 신종 기준서가 공표되면 기준서 우선 원칙 상 기준서를 새로 따라야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ, ㄹ 모두 참인 옳은 기술입니다.", "articles": [], "principle": "기준서 공백 하 작성자 준칙", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "개념체계와 K-IFRS 기준서의 지위와 관련하여, 외부감사인의 부당한 행위에 속하는 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 기업이 적법한 특정 기준서를 준수했음에도 개념체계 지문과 다르다는 이유를 대며 장부 수정을 강제 지시하는 행위\nㄴ. 기업의 적법한 기준서 적용 재무제표에 대해 개념체계 미일치를 근거로 기말 감사보고서 상에 의견거절을 표명하겠다고 압박하는 행위\nㄷ. 기업이 수립한 기준서 부재 거래의 자체 회계정책이 개념체계 원칙에 맞게 일관되게 수립되었는지 면밀히 객관적으로 검토하는 행위",
        "options": [
          "① ㄱ",
          "② ㄱ, ㄴ",
          "③ ㄴ, ㄷ",
          "④ ㄱ, ㄷ",
          "⑤ ㄱ, ㄴ, ㄷ"
        ],
        "answer": "2",
        "explanation": "② 감사인의 부당한 행위(월권 및 오류)에 속하는 것은 ㄱ과 ㄴ입니다. ㄷ의 경우 감사인의 당연한 감사 의무이자 합법적이고 정당한 검토 행위에 해당하므로 부당한 행위가 아닙니다.\n\n[보기 검증]\nㄱ. [참: 부당함] 기준서 적용 기업에 개념체계 잣대로 수정을 강제하는 것은 감사 권한 밖의 오류입니다.\nㄴ. [참: 부당함] 적법 장부에 개념체계 미일치를 이유로 감사의견 한정이나 거절 압박을 가하는 것은 월권 위법입니다.\nㄷ. [거짓: 정당함] 자체 수립한 정책의 타당성 검토는 감사인의 적법하고 의무적인 기본 감사 사항입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄴ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ은 감사인의 명백한 월권 및 부당한 행위 조합에 해당합니다.", "articles": [], "principle": "감사인 월권 범위 판별", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ은 감사인의 정당한 의무이므로 부당한 행위가 아닙니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ은 감사인의 정당한 의무입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ이 섞여 있어 틀렸습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "개념체계상 '추정, 판단 및 모형'에 관한 설명 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 재무보고서는 본질적으로 상당 부분 추정, 판단 및 모형에 근거한다.\nㄴ. 추정치가 사용되더라도 그것이 명확하게 설명되고 그 절차 상 오류가 없다면 정보의 유용성이 저해되지 않는다.\nㄷ. 측정불확실성이 아무리 높더라도 그것이 유용한 재무정보의 제공을 무조건 불가능하게 하는 것은 아니다.\nㄹ. 개념체계는 추정 모형의 수치적 한계를 없애기 위해 단일 점추정치 공식을 기준서로 모든 자산에 획일적으로 강제한다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "3 보기 중 옳은 설명은 ㄱ, ㄴ, ㄷ입니다. ㄹ의 경우 개념체계가 추정치의 자율성을 억제하기 위해 단일 점추정치를 획일적으로 모든 자산에 강제한다는 서술이 포함되어 있으므로 오답입니다.\n\n[보기 검증]\nㄱ. [참] 주관적 추정과 모형이 반영되는 것은 재무제표의 자연스러운 성격입니다.\nㄴ. [참] 절차의 투명성과 합리성이 담보되는 한 추정치는 유용합니다.\nㄷ. [참] 측정불확실성이 높더라도 목적적합한 정보로서 자산 보고의 효용이 인정됩니다.\nㄹ. [거짓] 자산의 특성에 따라 범위 확률 등 다양한 모형 사용이 허용되며 획일화하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ은 틀린 지문입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ은 개념체계 상 추정치 유용성 한계를 서술하는 참인 설명입니다.", "articles": [], "principle": "추정 및 측정불확실성 지침", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ은 틀린 지문입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },

    # =========================================================================
    # L5: 고난도 심화 (2문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s02-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "회계기준위원회(KASB)의 적법 절차(Due Process) 상 기준서 제정 시 개념체계 일탈(Deviation)을 허용하는 조치에 대한 심층 분석으로 가장 타당한 설명은?",
        "options": [
          "① 일탈은 위원회의 단순 행정 착오에 기인하므로 결론도출근거에 관련 기록을 지워 숨기는 것이 법률 분쟁을 차단하는 최선책이다.",
          "② 일반목적 재무보고의 목적을 달성하는 데 있어, 개념체계의 자산 정의의 경직성을 탈피해 경제적 현상의 실질적 유용성을 향상시키는 특수 설계가 필요한 예외적 경우에 한해 일탈 제정이 조화롭게 정당화되며, 위원회는 결론도출근거에 그 사유를 명확히 입증해 설명할 의무를 진다.",
          "③ 일탈이 성립하면 기존 개념체계는 즉시 소급 무효화가 선포되므로 전 세계 규제기관들에게 개념체계 미사용 권고안을 보내야 한다.",
          "④ 일탈 조항을 포함한 기준서가 통과되면 감사인은 이에 부합하게 처리한 기업에 대해 적정이 아닌 의견거절이나 한정을 강제 표명해야 정당하다.",
          "⑤ 일탈은 세무조정 시 세금을 100% 감면하기 위해 정부와 위원회가 기밀 결탁하여 제정하는 특혜 지침이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계의 목적에 비추어 볼 때, 때로는 문자 그대로의 개념체계 준수보다 경제적 현상의 실제적 유용성 촉진이 더 목적적합할 때 위원회는 일탈 기준을 제정할 수 있으며, 결론도출근거를 통해 이의 당위성을 투명하게 공시해 시장의 이해와 해석을 구해야 합니다.\n\n[오답 해설]\n① 일탈의 은폐는 위법 행위이며 허용되지 않습니다.\n③ 개념체계가 자동 소급 무효화되지 않습니다.\n④ 감사인은 기준서를 준수한 기업에 의견 거절을 내릴 권한이 없습니다.\n⑤ 세금 전액 감면 목적의 정부 기밀 결탁은 완전한 허구 소설 지문입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "일탈의 은폐 주장은 완전히 위법입니다.", "articles": [], "principle": "투명성 의무", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "실질적 유용성 확보 목적으로 결론도출근거 상의 명시를 수반한 일탈 기준 제정은 적법하게 인정됩니다.", "articles": [], "principle": "일탈의 철학적 당위성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개념체계 무효화와 관련 없습니다.", "articles": [], "principle": "개념체계 효력", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "의견거절 강제는 부적절합니다.", "articles": [], "principle": "의견거절 사유 부재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세금 감면 결탁 설은 허구입니다.", "articles": [], "principle": "기밀 결탁 부재", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s02-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "개념체계의 문항들이 회계기준위원회(KASB)와 재무보고서의 작성자(Preparer)가 지속적으로 '노력을 기울이는 목표(Goal)'의 성격을 가진다고 개념체계가 서술하는 취지에 대한 올바른 해석으로 옳은 것은?",
        "options": [
          "① 개념체계의 지침들은 단순히 장식용 선언에 불과하므로 실제 실무에서 굳이 노력을 들여 준수하려 애쓸 가치가 없음을 내포한다.",
          "② 재무제표는 상당 부분 정확한 서술보다 추정, 판단 및 모형에 근거하므로, 완벽한 정확성은 달성하기 어려우나 개념체계가 제시하는 일관된 질적 유용성 원칙들을 지향점 삼아 끊임없이 부합하도록 작성 노력을 기울여야 하는 최적의 목표(지향점)를 형성함을 뜻한다.",
          "③ 주총 3분의 2 동의가 없으면 어떠한 작성자도 자산 평가 추정치를 기재할 권리가 없으므로, 주총 합의를 얻어내기 위해 경영진이 투쟁해야 하는 정치적 목적을 가리킨다.",
          "④ 세법상의 세금 면제를 100% 달성하기 위해 국세청과 납세자가 공동으로 합의해야 하는 과세 탕감의 목표를 의미한다.",
          "⑤ 기존 기준서가 개념체계와 상충하는 경우 무조건 소송을 통해 기준서를 즉각 폐기 처분하는 입법 투쟁의 목표를 가리킨다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 재무보고서가 완벽하게 정확한 서술만으로 이뤄지기 힘든 현실(추정, 판단, 모형의 적극 개입)을 안고 있으므로, 개념체계가 정하는 여러 원칙은 회계기준 제정 기구와 작성자가 끊임없이 정보의 질을 지향하고 다듬기 위해 도달하고자 노력하는 최적의 이상적인 공동 지향 목표(Goal)가 됨을 바르게 서술하고 있습니다.\n\n[오답 해설]\n① 준수할 가치가 없다는 주장은 개념체계 지위를 부정하는 오류입니다.\n③ 주총 의결을 통한 평가 추정치 통제 주장은 회계학 상 존재하지 않습니다.\n④ 세법상의 과세 탕감과 무관합니다.\n⑤ 입법 소송 투쟁 지침이 전혀 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "가치가 없다는 설명은 완전한 오독입니다.", "articles": [], "principle": "개념체계 가치", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무제표의 한계를 극복하고 유용성을 지향하기 위해 개념체계는 도달하려 노력해야 하는 최적의 지향 목표를 의미합니다.", "articles": [], "principle": "지향 목표로서의 지위 분석", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주총 의결을 통한 추정치 기재 통제 주장은 오류입니다.", "articles": [], "principle": "장부 작성 권한", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "과세 탕감 목표와 무관합니다.", "articles": [], "principle": "과세 소득", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "입법 폐기 소송 주장은 허위입니다.", "articles": [], "principle": "소송 투쟁", "case": {"holding": "", "no": None}}
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
            "item": "2절 개념체계와 기준서"
          }
        }
    }
]

# Append new questions to existing ones
questions.extend(new_questions)

# Save combined questions back to file
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated 50 new questions. Total questions in {DB_PATH.name}: {len(questions)}")
