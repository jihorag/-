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
    # L1: 기초 개념 (10문항, 551~560번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s02-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 상 재무상태표 본문에 반드시 별도의 항목으로 표시되어야 하는 최소한의 자산 항목으로 가장 올바른 것은?",
        "options": [
            "① 회사 브랜드 명성 가치",
            "② 투자부동산(Investment Property)",
            "③ 사내 게시판 전산 시스템",
            "④ 직원 개인 보유 차량",
            "⑤ 경쟁사의 미공개 특허"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1001호 '재무제표 표시'에 따르면, 투자부동산은 재무상태표 본문에 구분하여 표시하여야 하는 최소한의 항목 목록에 속합니다.\n\n[오답 해설]\n① 명성 가치는 인식 요건을 충족하지 못해 본문 표시 대상이 아닙니다.\n③ 사내 전산 시스템은 일반적으로 유형자산이나 무형자산 등의 대과목에 통합 표시됩니다.\n④ 직원 개인 자산이나 ⑤ 경쟁사 자산은 보고기업의 자산이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "브랜드 명성은 자산 인식 자격이 없습니다.", "articles": [], "principle": "본문 최소 표시 항목", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "투자부동산은 재무상태표 본문에 반드시 별도 구분 표시하여야 하는 최소 표시 항목 중 하나입니다.", "articles": [], "principle": "본문 최소 표시 항목", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "통합 유형/무형자산 항목에 흡수되므로 최소 별도 표시가 강제되는 독립 항목이 아닙니다.", "articles": [], "principle": "본문 최소 표시 항목", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회사의 소유 권리가 없는 자산입니다.", "articles": [], "principle": "본문 최소 표시 항목", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "타사의 자산은 보고 대상이 아닙니다.", "articles": [], "principle": "본문 최소 표시 항목", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "K-IFRS 상 재무상태표에 자산과 부채를 배열하는 가장 기본적이고 원칙적인 구분 표시 방법은 무엇인가?",
        "options": [
            "① 무조건 금액이 큰 순서대로만 정렬하는 방법",
            "② 유동자산과 비유동자산, 유동부채와 비유동부채로 구분하여 표시하는 유동/비유동 구분법",
            "③ 회사의 설립 연도 역순으로 자산을 배열하는 방법",
            "④ 주주들의 거주 국가별로 부채를 배열하는 방법",
            "⑤ 회계사의 성씨 가나다순으로 자산을 나열하는 방법"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 상 자산과 부채는 유동성 순서 배열법이 더 유용한 정보를 제공하는 예외적 상황(금융업 등)을 제외하고는, 유동자산과 비유동자산, 유동부채와 비유동부채로 구분하여 표시하는 것을 원칙으로 합니다.\n\n[오답 해설]\n① 금액 기준 배열은 공식 기준이 아닙니다.\n③, ④, ⑤는 회계 기준과 아무런 관련이 없는 허구의 배열법입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "금액 크기순 정렬은 표준 배열법이 아닙니다.", "articles": [], "principle": "재무상태표 표시 원칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재무상태표는 유동성 구분(유동/비유동 구분법)을 적용하여 자산/부채를 나누어 표시함이 기본 원칙입니다.", "articles": [], "principle": "재무상태표 표시 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "설립 연도 기준 배열은 존재하지 않습니다.", "articles": [], "principle": "재무상태표 표시 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주주 거주지 기준 분류는 불가합니다.", "articles": [], "principle": "재무상태표 표시 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계사 이름순 정렬 등은 전혀 관련 없는 소설입니다.", "articles": [], "principle": "재무상태표 표시 원칙", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "K-IFRS 상 이연법인세자산(Deferred Tax Assets) 및 이연법인세부채(Deferred Tax Liabilities)의 유동성 분류에 관한 철칙으로 가장 올바른 것은?",
        "options": [
            "① 전액 유동자산 또는 유동부채로만 분류하여야 한다.",
            "② 당기에 실현될 부분은 유동으로 분류하고 차기 이후 실현될 부분은 비유동으로 쪼개어 분류한다.",
            "③ 절대로 유동자산이나 유동부채로 분류할 수 없으며, 무조건 비유동자산 또는 비유동부채로 분류하여야 한다.",
            "④ 정부 세무서장의 개별 납세 고지 처리에 따라 수시로 자본 계정에 임의 귀속시킨다.",
            "⑤ 회사의 이익이 적자인 해에는 부채로만 고정 분류한다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1001호에 따르면, 이연법인세자산과 이연법인세부채는 실현 예상 시점(12개월 이내 등)과 무관하게 절대로 유동자산이나 유동부채로 분류할 수 없고, 무조건 '비유동자산' 또는 '비유동부채'로만 분류하도록 강제하고 있습니다.\n\n[오답 해설]\n①, ②는 과거 구 기준이나 잘못된 분류 방식으로 현재는 전면 금지됩니다.\n④, ⑤는 세법 및 이연법인세 성격에 어긋나는 오류입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "이연법인세는 유동 항목으로 갈 수 없습니다.", "articles": [], "principle": "이연법인세의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기간별 쪼개기(유동/비유동 혼합) 분류는 금지되어 있습니다.", "articles": [], "principle": "이연법인세의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이연법인세 자산/부채는 그 회수 기한과 관계없이 비유동자산/비유동부채로만 기재하여야 합니다.", "articles": [], "principle": "이연법인세의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 행정 연동의 자본 임의 전입은 불가능합니다.", "articles": [], "principle": "이연법인세의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회사 손익 실적에 따라 강제 고정하지 않습니다.", "articles": [], "principle": "이연법인세의 유동성 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "K-IFRS 상 기업의 정상영업주기(Normal Operating Cycle)를 명확히 식별하기 곤란한 예외적인 상황에서, 기준서가 가정하도록 규정한 영업주기 기간은 몇 개월인가?",
        "options": [
            "① 3개월",
            "② 6개월",
            "③ 12개월",
            "④ 18개월",
            "⑤ 24개월"
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 상 기업의 정상영업주기가 명확하게 식별되지 않는 경우에는 그 주기가 12개월인 것으로 가정하여 자산과 부채의 유동성 분류를 수행합니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 정상영업주기 불명 시의 기준서 상 가정 수치가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "3개월은 불명 시 가정 기간이 아닙니다.", "articles": [], "principle": "정상영업주기 식별 불능 시 가정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "6개월은 불명 시 가정 기간이 아닙니다.", "articles": [], "principle": "정상영업주기 식별 불능 시 가정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "정상영업주기를 객관적으로 식별할 수 없는 경우, 그 주기는 1년(12개월)으로 가정하여 분류 기준을 삼습니다.", "articles": [], "principle": "정상영업주기 식별 불능 시 가정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "18개월은 오답입니다.", "articles": [], "principle": "정상영업주기 식별 불능 시 가정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "24개월은 오답입니다.", "articles": [], "principle": "정상영업주기 식별 불능 시 가정", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "금융회사(은행, 증권사 등)와 같은 특정 기업이 예외적으로 유동/비유동 구분법을 적용하지 않고, 자산과 부채를 유동성 순서대로 나열하여 표시할 수 있는 정당한 조건은 무엇인가?",
        "options": [
            "① 정부 금융감독원장의 자필 지시서가 분기마다 도달할 때만",
            "② 유동성 순서에 따른 표시방법이 유동/비유동 구분법보다 신뢰성 있고 더욱 목적적합한 정보를 제공할 때",
            "③ 외화 자산의 비중이 90%를 초과할 때",
            "④ 기중에 실제 부도가 발생하여 청산 절차가 시작되었을 때",
            "⑤ 회사의 주주가 10명 미만인 영세 금융실체일 때"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 상 금융회사 등 영업 주기가 명확하지 않거나 현금화 속도가 중요한 업종의 경우, 유동성 순서에 따른 표시가 더 신뢰성 있고 목적적합한 재무정보를 준다면 구분법 대신 유동성 순서 배열법 단독 적용이 인정됩니다.\n\n[오답 해설]\n① 행정 편의적 지시 연동 요건이 아닙니다.\n③ 외화 자산 비율이나 ⑤ 주주 수 등은 배열법 채택 판단의 직접 척도가 아닙니다.\n④ 청산 시에는 청산 회계 기준이 따로 작동합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "금융당국의 강제 행정 명령 사항이 아닙니다.", "articles": [], "principle": "유동성 순서 배열법 조건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "유동성 순서 배열법이 정보 이용자에게 더 신뢰성 있고 유용한 정보를 주는 특수 업종(금융업 등)은 예외적으로 허용됩니다.", "articles": [], "principle": "유동성 순서 배열법 조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "외화 자산의 크기 비율 조건이 아닙니다.", "articles": [], "principle": "유동성 순서 배열법 조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부도 개시 여부와 배열법의 평시 채택은 다릅니다.", "articles": [], "principle": "유동성 순서 배열법 조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소액 주주 구성 여부와 무관합니다.", "articles": [], "principle": "유동성 순서 배열법 조건", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "K-IFRS 상 자산 중 '현금이나 현금성자산'이 유동자산으로 분류되기 위해 충족해야 하는 계약상 사용 제한 기간 한도는?",
        "options": [
            "① 사용에 대한 제한 기간이 보고기간 후 3개월 이상이 아니어야 한다.",
            "② 사용에 대한 제한 기간이 보고기간 후 6개월 이상이 아니어야 한다.",
            "③ 사용에 대한 제한 기간이 보고기간 후 12개월 이상이 아니어야 한다.",
            "④ 사용에 대한 제한 기간이 보고기간 후 24개월 이상이 아니어야 한다.",
            "⑤ 어떠한 사용 제한도 하루조차 걸려 있어서는 안 된다."
        ],
        "answer": "3",
        "explanation": "③ 현금이나 현금성자산이라 하더라도, 교환이나 부채 상환 목적으로의 사용 제한 기간이 보고기간 후 12개월 이상인 경우에는 비유동자산(예: 장기성 예금 등)으로 분류하여야 하며, 12개월 이상이 아닌 경우에만 유동자산으로 분류합니다.\n\n[오답 해설]\n①, ②, ④는 기준서에 규정된 사용제한 한도 기간이 아닙니다.\n⑤ 단기 일시 제한(예: 3개월 정기예금 등)은 유동자산에 들어갈 수 있으므로 제한이 일절 없어야 한다는 주장은 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "3개월은 기준서의 사용제한 기준 기간이 아닙니다.", "articles": [], "principle": "현금의 유동성 분류 조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "6개월은 기준서의 사용제한 기준 기간이 아닙니다.", "articles": [], "principle": "현금의 유동성 분류 조건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기간 종료일 기준 12개월 이상의 장기 사용 제한이 걸려 있지 않은 현금자산만 유동자산으로 기재합니다.", "articles": [], "principle": "현금의 유동성 분류 조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "24개월은 오답입니다.", "articles": [], "principle": "현금의 유동성 분류 조건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단기 거치식 제한 등은 유동자산 분류가 가능하므로 완전 배제 주장은 틀렸습니다.", "articles": [], "principle": "현금의 유동성 분류 조건", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "K-IFRS 상 장기차입 계약 조건을 위반하여 채권자(대여자)가 기말 시점에 즉시 상환을 요구할 수 있게 된 부채의 재무상태표 상 원칙적인 유동성 분류는?",
        "options": [
            "① 자본조정 차감 항목",
            "② 비유동부채(Non-current Liabilities)",
            "③ 유동부채(Current Liabilities)",
            "④ 무형부채",
            "⑤ 평가제외 항목"
        ],
        "answer": "3",
        "explanation": "③ 보고기간 말 이전에 장기차입 계약을 위반하여 채권자가 즉시 상환을 청구할 수 있게 된 부채는, 보고기간 말 현재 결제를 12개월 이상 연기할 수 있는 무조건의 권리가 소멸한 상태이므로 '유동부채'로 분류하는 것이 원칙입니다.\n\n[오답 해설]\n① 자본 거래가 아닙니다.\n② 결제 연기 권리가 없으므로 비유동부채가 될 수 없습니다.\n④, ⑤는 회계 용어가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자본조정 분류 대상이 아닙니다.", "articles": [], "principle": "계약 위반 부채의 기본 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "결제를 연기할 권리가 상실되었으므로 비유동부채 분류는 불가능합니다.", "articles": [], "principle": "계약 위반 부채의 기본 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "채권자가 즉시 상환 청구가 가능해진 채무는 기말 시점에 연기 권리가 박탈된 상태이므로 유동부채로 보고해야 합니다.", "articles": [], "principle": "계약 위반 부채의 기본 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무형부채는 존재하지 않는 과목입니다.", "articles": [], "principle": "계약 위반 부채의 기본 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기말 평가 및 공시 분류가 강제됩니다.", "articles": [], "principle": "계약 위반 부채의 기본 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "K-IFRS 상 부채의 분류방법 중 기존 대출 약정에 따라 보고기간 후 적어도 12개월 이상 부채를 차환할 수 있는 권리(재량권)가 기업에 확실히 부여되어 있을 때의 분류 규칙은?",
        "options": [
            "① 강제로 주식으로 전환 분개하여 자본에 넣는다.",
            "② 만기가 12개월 이내에 도래하더라도 비유동부채로 분류한다.",
            "③ 채권자의 기분을 맞추기 위해 무조건 유동부채로 분류한다.",
            "④ 해당 부채 정보를 재무보고서에서 완전히 누락시킨다.",
            "⑤ 세무서 연동 부채 계정으로 직접 상계 차감한다."
        ],
        "answer": "2",
        "explanation": "② 기업이 기존 계약에 따라 보고기간 종료일로부터 적어도 12개월 이상 부채를 차환하거나 만기를 연장할 수 있는 재량권(재량의 권리)을 가지고 있다면, 비록 형식적 만기가 12개월 내에 오더라도 실질적 상환 연기가 가능하므로 '비유동부채'로 분류합니다.\n\n[오답 해설]\n① 임의 주식 전환은 불가합니다.\n③ 기업의 재량권 권리를 반영해야 하므로 무조건 유동 분류는 틀렸습니다.\n④, ⑤는 부적절한 회계처리 설명입니다.",
        "type": "개념5지",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "출자 전환 약정 등이 없는 한 임의 자본화는 안 됩니다.", "articles": [], "principle": "차환 재량권 보유 부채", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "만기가 단기라도 기업에게 연장 재량권이 확실히 있다면 실질 지위가 유지되므로 비유동부채로 갈 수 있습니다.", "articles": [], "principle": "차환 재량권 보유 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채권자의 태도와 별개로 계약상 권리를 반영해야 합니다.", "articles": [], "principle": "차환 재량권 보유 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 누락은 분식입니다.", "articles": [], "principle": "차환 재량권 보유 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 계정 임의 차감은 불가합니다.", "articles": [], "principle": "차환 재량권 보유 부채", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "K-IFRS 상 기업의 정상영업주기(Normal Operating Cycle)의 공식적인 정의로 가장 올바른 것은?",
        "options": [
            "① 회사가 창립된 날로부터 청산하기로 주주총회 결의를 마친 날까지의 기간",
            "② 영업활동을 위한 자산의 취득시점부터 그 자산이 현금이나 현금성자산으로 실현되는 시점까지 소요되는 기간",
            "③ 매년 1월 1일부터 법인세 신고를 마치는 3월 31일까지의 기간",
            "④ 대표이사가 회사에 출근하여 퇴근할 때까지 소요되는 일일 시간",
            "⑤ 회사가 신규 대출을 신청하여 실제 입금받기까지 걸리는 평균 영업일수"
        ],
        "answer": "2",
        "explanation": "② 정상영업주기란 원재료나 재고자산 등 영업을 위한 자산을 취득하는 시점부터, 제품 가공 및 매출을 거쳐 그 대금이 현금으로 최종 회수되는 시점까지 평균적으로 걸리는 순환 소요 기간을 뜻합니다.\n\n[오답 해설]\n① 은 기업의 수명 기간입니다.\n③ 은 법인세 세무 조정 기한입니다.\n④, ⑤는 영업주기의 정의와 전혀 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기업 존속 기간의 정의입니다.", "articles": [], "principle": "정상영업주기의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산 매입 시점부터 가공/매출을 거쳐 현금화되는 회전 순환 소요 주기가 영업주기의 정확한 정의입니다.", "articles": [], "principle": "정상영업주기의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 조정 기한을 칭하지 않습니다.", "articles": [], "principle": "정상영업주기의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일과 출퇴근 시간과는 무관합니다.", "articles": [], "principle": "정상영업주기의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "여신 심사 소요 기간이 아닙니다.", "articles": [], "principle": "정상영업주기의 정의", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "K-IFRS 상 기업이 서로 성격이 판이한 다양한 사업(예: 소매업과 금융업 병행 등)을 영위하여, 재무상태표의 일부 자산·부채는 유동/비유동으로 적고, 나머지는 유동성 순서대로 섞어 표시하는 재무제표 표시방법의 명칭은?",
        "options": [
            "① 전산 자동 배분 표시방법",
            "② 혼합 표시방법(Mixed basis of presentation)",
            "③ 다차원 분석 표시방법",
            "④ 복식 상계 대조 방법",
            "⑤ 임의 배열 표시방법"
        ],
        "answer": "2",
        "explanation": "② 기업이 다양한 성격의 사업 부문을 동시에 경영하는 경우, 업종 특성에 맞추어 일부는 유동/비유동 구분법으로 기재하고 일부 부문은 유동성 순서 배열법을 적용하여 하나의 재무제표에 혼용 기재하는 '혼합 표시방법'의 채택이 허용됩니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 K-IFRS 기준서에 명시된 재무제표 표시 배열 양식 명칭이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "전산 자동 분류 등은 공식 표시명칭이 아닙니다.", "articles": [], "principle": "혼합 표시방법의 의의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "일부는 구분법, 일부는 순서법을 결합하여 표시하는 방식을 혼합 표시방법이라 부릅니다.", "articles": [], "principle": "혼합 표시방법의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "다차원 분석 등은 관리회계 용어 성격입니다.", "articles": [], "principle": "혼합 표시방법의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "복식 상계 등은 존재하지 않는 표시명입니다.", "articles": [], "principle": "혼합 표시방법의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 기재는 금지되므로 임의 배열 방식은 틀렸습니다.", "articles": [], "principle": "혼합 표시방법의 의의", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },

    # =========================================================================
    # L2: 이해 (15문항, 561~575번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s02-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "다음 중 K-IFRS 상 '이연법인세 자산 및 부채'를 당해 연도 세액 정산 예정 시점의 장단기 유동성 구분과 상관없이 무조건 비유동(Non-current)으로만 보고하게 규정한 주된 이론적 배경은 무엇인가?",
        "options": [
            "① 이연법인세는 실제 세금 환급이 법적으로 무조건 금지되어 있기 때문에",
            "② 세액의 궁극적 정산일 및 실현 조건이 복잡한 법인세법의 과세 소득 발생 여부와 연동되어 있어, 12개월 내에 명확히 청산될 성격의 운전자본이나 단기부채로 보기 곤란하므로 표시의 일관성과 신뢰성을 위해 비유동으로 단일화한 것이다.",
            "③ 이연법인세는 자산이나 부채가 아니라 자본의 자본조정 항목에 불과하므로",
            "④ 정부 기획재정부가 대기업에 세무적 패널티를 가하기 위해 인위적으로 고안한 조항이므로",
            "⑤ 회계사가 기장할 때 계산을 생략하고 비유동에 한 줄만 적게 해 주기 위한 단순 편의 목적이므로"
        ],
        "answer": "2",
        "explanation": "② 이연법인세자산·부채는 일반 상거래 채권·채무와 달리, 향후 회사의 과세소득 세무조정 시점에 따라 실현 시기가 요동칩니다. 매년 세세하게 쪼개어 유동성 분류를 바꾸는 것은 실무적 비용에 비해 정보 신뢰성을 떨어뜨리므로, K-IFRS는 이를 전액 비유동으로 단일 보고하게 함으로써 분류 왜곡을 원천 예방합니다.\n\n[오답 해설]\n① 실제 세무상 세액 정산 및 조정을 통해 자산성이 실현됩니다.\n③ 지분이 아니라 자산/부채 항목입니다.\n④, ⑤는 제도 도입 배경에 관한 전혀 잘못된 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산성이 입증되는 정당한 계정입니다.", "articles": [], "principle": "이연법인세 비유동 분류 사유", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "과세소득 변동에 따른 실현시기 불확실성 때문에, 유동성 분류의 자의적 쪼개기를 방지하고 신뢰성을 올리고자 비유동으로 고정 분류합니다.", "articles": [], "principle": "이연법인세 비유동 분류 사유", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 및 부채의 정의에 부합하는 계정입니다.", "articles": [], "principle": "이연법인세 비유동 분류 사유", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대기업 규제 목적 세무 행정이 아닙니다.", "articles": [], "principle": "이연법인세 비유동 분류 사유", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 기장 편의를 위한 예외 조항 제공 목적이 아닙니다.", "articles": [], "principle": "이연법인세 비유동 분류 사유", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "조선업이나 대규모 건설업처럼 자산의 제조·인도에 상당한 시간이 걸려 기업의 정상영업주기가 12개월을 크게 초과(예: 18개월)하는 경우, 이 영업주기 내에 판매/실현될 것으로 예상되는 재고자산(미완성 선박)과 매출채권의 재무상태표 상 올바른 유동성 분류는?",
        "options": [
            "① 12개월을 초과하여 회수되므로 무조건 비유동자산으로 분류하여야 한다.",
            "② 정상영업주기 내에 실현되거나 판매 소비될 의도가 있다면, 보고기간 후 12개월을 초과하여 실현되더라도 유동자산으로 분류한다.",
            "③ 자산가치 전체를 대손 처리하여 자본 차감으로 지운다.",
            "④ 부채 항목인 유동부채의 예수금 계정으로 이월 보고한다.",
            "⑤ 선박의 공정률만큼 감가상각한 후 남은 잔액만 자본에 직접 더한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 상 재고자산이나 매출채권과 같이 기업의 일상적 영업주기 순환 과정에서 소모·회수되는 영업 운전자본은, 해당 실체의 정상영업주기가 12개월을 초과하는 장기라 하더라도 그 영업주기 내에 정상 실현될 예정이라면 예외적으로 '유동자산' 분류가 허용·의무화됩니다.\n\n[오답 해설]\n① 12개월 초과를 이유로 장기 영업주기 내 운전자본을 비유동으로 보내면 영업 능력이 왜곡 기재됩니다.\n③, ④, ⑤는 비정상적인 회계처리 방식입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "12개월이 초과되더라도 영업주기 기준이 우선하므로 비유동 분류는 틀렸습니다.", "articles": [], "principle": "장기 영업주기 자산의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "영업운전자본(재고자산, 채권)은 정상영업주기 내에만 들어온다면 1년을 넘어가도 유동자산으로 분류함이 규정입니다.", "articles": [], "principle": "장기 영업주기 자산의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정상 자산을 임의 대손(손상) 상각 처리할 수 없습니다.", "articles": [], "principle": "장기 영업주기 자산의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산을 부채로 기장할 수 없습니다.", "articles": [], "principle": "장기 영업주기 자산의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고자산은 감가상각 대상 자산이 아닙니다.", "articles": [], "principle": "장기 영업주기 자산의 유동성 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "정상영업주기가 12개월을 초과(예: 18개월)하는 기업의 부채 중 매입채무(Accounts Payable)와 영업비용에 대한 미지급비용이 보고기간 종료일로부터 14개월 뒤에 결제될 예정일 때, K-IFRS 상의 올바른 분류는?",
        "options": [
            "① 만기가 12개월을 넘어가므로 무조건 비유동부채로 분류해야 한다.",
            "② 정상영업주기 내에 결제될 것으로 예상되는 영업 운전자본 성격의 부채이므로, 12개월이 초과하더라도 유동부채로 분류한다.",
            "③ 대손충당금의 직접 차감 항목으로 기재한다.",
            "④ 자산 항목인 현금성자산의 대변 가산으로 간주한다.",
            "⑤ 법정 세액 감면 혜택을 받기 위해 사외 유출 자본금으로 재기록한다."
        ],
        "answer": "2",
        "explanation": "② 매입채무나 영업상 미지급 비용 등은 영업주기 순환 과정의 결제 의무이므로, 비록 실제 결제 시기가 1년을 초과하더라도 정상영업주기(18개월) 범위 이내라면 '유동부채'로 분류하는 것이 원칙입니다.\n\n[오답 해설]\n① 영업운전자본 부채는 12개월 초과 시에도 유동 분류되므로 오답입니다.\n③ 부채는 대손충당금(자산 차감) 대상이 아닙니다.\n④, ⑤는 분개 논리에 완전히 어긋나는 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상거래 미지급채무는 만기가 1년을 넘어도 영업주기 범위면 유동부채에 듭니다.", "articles": [], "principle": "장기 영업주기 부채의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "조달 및 영업 주기에 수반된 운전자본 부채는 영업주기 내 결제 대상일 때 유동부채로 분류함이 조문 규정입니다.", "articles": [], "principle": "장기 영업주기 부채의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "충당금 가산 처리는 자산 평가 조정에 국한됩니다.", "articles": [], "principle": "장기 영업주기 부채의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미지급 채무를 자산의 직접 조율로 섞어 왜곡할 수 없습니다.", "articles": [], "principle": "장기 영업주기 부채의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 전입 거래와 무관합니다.", "articles": [], "principle": "장기 영업주기 부채의 유동성 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "다음 중 K-IFRS 상 자산의 유동성 분류 요건 4가지에 해당하지 않는 것은?",
        "options": [
            "① 기업의 정상영업주기 내에 실현될 것으로 예상하거나, 정상영업주기 내에 판매하거나 소비할 의도가 있다.",
            "② 주로 단기매매 목적으로 보유하고 있다.",
            "③ 보고기간 후 12개월 이내에 실현될 것으로 예상한다.",
            "④ 현금이나 현금성자산으로서 교환이나 부채 상환 목적으로의 사용 제한 기간이 보고기간 후 12개월 이상이 아니다.",
            "⑤ 회사의 대주주가 본인 자식에게 상속해 줄 목적의 사적 투자 주식에 해당한다."
        ],
        "answer": "5",
        "explanation": "⑤ 자산의 유동자산 분류 요건 4가지는 영업주기 내 실현, 단기매매 보유, 12개월 내 실현, 사용 제한 12개월 미만 현금성자산입니다. 주주의 사적 상속 목적 주식은 기업 회계 상 자산의 분류 기준에 해당하지 않습니다.\n\n[오답 해설]\n①, ②, ③, ④는 K-IFRS 1001호 문단에 규정된 유동자산의 정당한 4가지 요건입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "유동자산 분류 요건 중 첫 번째에 해당합니다.", "articles": [], "principle": "유동자산의 4대 분류 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동자산 분류 요건 중 두 번째(단기매매 보유)에 해당합니다.", "articles": [], "principle": "유동자산의 4대 분류 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동자산 분류 요건 중 세 번째(12개월 내 실현)에 해당합니다.", "articles": [], "principle": "유동자산의 4대 분류 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동자산 분류 요건 중 네 번째(현금 사용 제한 한도)에 해당합니다.", "articles": [], "principle": "유동자산의 4대 분류 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사주 개인의 사생활 상속 주식 지위는 회사의 유동성 판정 조건과 전혀 무관하므로 5가 정답입니다.", "articles": [], "principle": "유동자산의 4대 분류 요건", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "다음 중 K-IFRS 상 부채의 유동성 분류 요건 4가지에 해당하지 않는 것은?",
        "options": [
            "① 정상영업주기 내에 결제될 것으로 예상하고 있다.",
            "② 주로 단기매매 목적으로 보유하고 있다.",
            "③ 보고기간 후 12개월 이내에 결제하기로 되어 있다.",
            "④ 보고기간 후 12개월 이상 부채의 결제를 연기할 수 있는 무조건의 권리를 가지고 있지 않다.",
            "⑤ 회사의 경쟁자가 법적으로 파산 선고를 받은 해의 미결제 수임료에 해당한다."
        ],
        "answer": "5",
        "explanation": "⑤ 유동부채의 분류 요건 4가지는 영업주기 내 결제 예상, 단기매매 목적 보유, 12개월 내 결제 도래, 12개월 이상 연기 권리 결여입니다. 경쟁사의 파산이나 미결제 수임료는 회사의 부채 유동성 판정 기준이 아닙니다.\n\n[오답 해설]\n①, ②, ③, ④는 K-IFRS 1001호 문단에 규정된 유동부채의 정당한 4가지 요건입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "유동부채 분류 요건 중 첫 번째에 해당합니다.", "articles": [], "principle": "유동부채의 4대 분류 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동부채 분류 요건 중 두 번째(단기매매)에 해당합니다.", "articles": [], "principle": "유동부채의 4대 분류 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동부채 분류 요건 중 세 번째(12개월 결제)에 해당합니다.", "articles": [], "principle": "유동부채의 4대 분류 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동부채 분류 요건 중 네 번째(연기 권리 부재)에 해당합니다.", "articles": [], "principle": "유동부채의 4대 분류 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "타인 파산 리스크와 결제 지위는 보고기업 부채 요건 분류에 해당하지 않으므로 5가 답입니다.", "articles": [], "principle": "유동부채의 4대 분류 요건", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "보고기간 종료일 현재 만기가 10개월 뒤에 도래하는 차입금이 있을 때, 기존의 대출 계약서상 만기를 추가로 2년 더 연장할 수 있는 단독 '재량권(Discretion)'이 기업에 보장되어 있고 기업이 연장할 의도가 있다면, K-IFRS 상 이 부채의 올바른 분류는?",
        "options": [
            "① 만기가 1년 미만이므로 무조건 유동부채로 보고하여야 한다.",
            "② 기말에 재량권을 바탕으로 연장할 권리와 기대가 존재하므로 비유동부채로 분류한다.",
            "③ 주식 매입 채무로 재분류하여 영업비용에 직접 가산한다.",
            "④ 기말 결제 금액의 50%를 잡손실 처리하고 차액만 부채로 적는다.",
            "⑤ 회사의 신용등급을 올리기 위해 자본 항목에 직접 적립한다."
        ],
        "answer": "2",
        "explanation": "② 만기가 10개월 뒤로 임박하였더라도 기존 차입 약정상 12개월 이상 부채를 연장(차환)할 재량권(권리)이 기업에게 확실히 있다면, 연장 권리가 확보된 상태이므로 실질적인 장기부채 성격을 나타내어 '비유동부채'로 분류합니다.\n\n[오답 해설]\n① 단순 형식적 만기 기준 적용 오류입니다.\n③, ④, ⑤는 회계 기준에 위배되는 타당하지 않은 처리 방법입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재량권이 계약서에 보장된 경우에는 형식적 만기(10개월)가 1년 미만이라도 유동부채가 되지 않습니다.", "articles": [], "principle": "차환재량권 보유 시 부채 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기간종료일 현재 차환/연장을 선택할 계약상 재량권이 회사에 있고 연장할 의도(기대)가 있으면 비유동부채로 분류하는 것이 타당합니다.", "articles": [], "principle": "차환재량권 보유 시 부채 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주식매입채무 분류 및 비용화는 오류입니다.", "articles": [], "principle": "차환재량권 보유 시 부채 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채의 일부 잡손실 제거 등은 자의적 분식입니다.", "articles": [], "principle": "차환재량권 보유 시 부채 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채무를 자본 계정으로 보낼 수 없습니다.", "articles": [], "principle": "차환재량권 보유 시 부채 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "보고기간 종료일 현재 만기가 8개월 뒤인 차입금에 대해, 회사가 차입 은행과 만기 연장 협상을 우호적으로 진행 중이나 기말 현재 최종 계약은 체결되지 않았고 만기 결정 권한이 오직 은행(대여자)에게 있을 때, K-IFRS 상 이 부채의 유동성 분류 판정은?",
        "options": [
            "① 연장 협상이 진행 중이며 우호적이므로 비유동부채로 분류한다.",
            "② 기말 현재 보고기간 후 12개월 이상 부채 결제를 연기할 수 있는 무조건의 권리(재량권)가 없으므로 유동부채로 분류한다.",
            "③ 대손상각누계액 차감 방식으로 자산에서 마이너스 보고한다.",
            "④ 기말 이자비용을 ₩0원으로 자동 강제 재평가 처리한다.",
            "⑤ 회사의 납입자본금 계정으로 이월 대체한다."
        ],
        "answer": "2",
        "explanation": "② 우호적 협상 중이더라도 보고기간 말(기말) 시점에 계약서상 12개월 이상 만기를 미룰 수 있는 무조건적 권리(재량권)가 기업에게 없다면, 연기 권리가 확보되지 않은 상태이므로 냉정하게 '유동부채'로 분류하여야 합니다.\n\n[오답 해설]\n① 우호적 전망만으로 연기 권리가 있는 것으로 보아 비유동 분류할 수 없습니다.\n③ 자산 감액 계정 차감이 아닙니다.\n④ 이자비용 강제 소멸은 불가합니다.\n⑤ 자본금 대체 대상이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "협상이 진행 중이거나 연장 가능성이 높더라도 기말 현재 권리가 없으므로 비유동부채가 될 수 없습니다.", "articles": [], "principle": "재량권 부재 시 부채 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "연기 권리가 대여자의 승인에 구속되어 있어 회사에 독점 권리가 없는 경우, 만기 임박 부채는 유동부채로 계상하여야 합니다.", "articles": [], "principle": "재량권 부재 시 부채 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채를 자산 대손 충당 차감으로 조작할 수 없습니다.", "articles": [], "principle": "재량권 부재 시 부채 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자비용의 임의 조작은 불허됩니다.", "articles": [], "principle": "재량권 부재 시 부채 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 대체 처리는 불가합니다.", "articles": [], "principle": "재량권 부재 시 부채 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "장기차입 약정을 기중에 위반하여 은행이 언제든 즉시 상환을 청구할 수 있게 되었을 때, '보고기간 말 이전'에 은행이 향후 18개월 동안 약정 위반을 근거로 상환 청구를 하지 않기로 공식 합의(유예기간 부여)해 준 부채의 기말 분류는 무엇인가?",
        "options": [
            "① 유동부채(Current Liabilities)",
            "② 비유동부채(Non-current Liabilities)",
            "③ 주식 자본금 항목",
            "④ 영업비용 차감 항목",
            "⑤ 무형 자산"
        ],
        "answer": "2",
        "explanation": "② 보고기간 종료일(말) 이전에 대여자가 약정 위반에 대한 즉시 상환 청구를 유예(적어도 12개월 이상 상환 요구하지 않음)하기로 공식 합의해 준 경우, 보고기간 말 현재 기업은 12개월 이상 결제를 연기할 수 있는 권리를 회복한 셈이므로 '비유동부채'로 분류합니다.\n\n[오답 해설]\n① 기말 이전에 합의가 끝났으므로 유동부채가 아닌 비유동부채입니다.\n③, ④, ⑤는 분류할 수 없는 잘못된 계정 범주입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기말 전에 상환요구 유예 합의가 이루어졌으므로 유동부채가 되지 않습니다.", "articles": [], "principle": "기말 전 유예 합의 부채", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기간 종료일 이전에 12개월 이상의 상환 유예(결제 연기 권리)가 계약 상 부활되었으므로 비유동부채로 환원 분류합니다.", "articles": [], "principle": "기말 전 유예 합의 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 전입 대상이 아닙니다.", "articles": [], "principle": "기말 전 유예 합의 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업비용과 무관한 차입금 채무입니다.", "articles": [], "principle": "기말 전 유예 합의 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채를 무형자산으로 적을 수 없습니다.", "articles": [], "principle": "기말 전 유예 합의 부채", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "장기차입 약정을 기중에 위반하여 기말 현재 즉시 상환 대상이 된 채무에 대해, 기말 시점에는 아무런 합의가 없었다가 기말 이후인 1월 15일(재무제표 승인일 전)에 은행이 상환 요구를 유예해 주기로 최종 서명 합의한 경우, 이 부채의 '보고기간 말(기말)' 재무상태표 상 분류는?",
        "options": [
            "① 사후 합의가 승인일 전에 성사되었으므로 소급하여 비유동부채로 보고한다.",
            "② 보고기간 말 현재 시점에는 결제를 12개월 이상 연기할 권리가 없었으므로, 사후 합의 여부와 무관하게 보고기간 말 현재는 '유동부채'로 분류하여야 한다.",
            "③ 전액 잡이익으로 처리하여 대변에 기재한다.",
            "④ 기말 부채를 전산 상으로 아예 숨겨 무공시 처리한다.",
            "⑤ 회사의 자본금 계정에서 마이너스 조정한다."
        ],
        "answer": "2",
        "explanation": "② 재무제표 상의 부채 분류는 '보고기간 종료일 현재의 법적 권리 상태'를 기준으로 판정합니다. 기말 시점에는 즉시 상환 요구 대상(연기 권리 없음)이었으나 기말이 지나서 비로소 합의가 된 경우, 기말 자본의 상태를 소급 변경할 수 없고 당해 기말에는 '유동부채'로 보고하고 주석(보고기간 후 사건)으로 보완 설명해야 합니다.\n\n[오답 해설]\n① 기말 이후의 사건을 재무상태표 본문 분류에 소급 적용할 수 없습니다.\n③ 채무의 소멸이 아니므로 잡이익이 아닙니다.\n④ 부채의 무단 은폐는 불법입니다.\n⑤ 자본 차감 거래가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "보고기간 후 승인일 전 합의는 보고기간 후 사건일 뿐, 기말 상태를 소급해 비유동으로 변경할 수 없습니다.", "articles": [], "principle": "기말 후 합의된 계약 위반 부채", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기간 말 현재 시점에는 상환을 연기할 무조건적 권리가 확보되지 않았으므로, 기말에는 유동부채로 보고하여야 합니다.", "articles": [], "principle": "기말 후 합의된 계약 위반 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익 실현 거래가 아니며 채무가 그대로 존속합니다.", "articles": [], "principle": "기말 후 합의된 계약 위반 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공시 누락은 기준 위반입니다.", "articles": [], "principle": "기말 후 합의된 계약 위반 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 차감 조정 계정이 아닙니다.", "articles": [], "principle": "기말 후 합의된 계약 위반 부채", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "다음 중 K-IFRS 제1001호에 따라 유동/비유동 구분법을 적용하여 재무상태표를 공시할 때, 비유동자산(Non-current Assets) 대과목의 고유한 정의로 가장 올바른 것은?",
        "options": [
            "① 기업의 영업주기 밖에서 10년 이상 지나야만 겨우 팔 수 있는 자산 목록",
            "② 유동자산의 정의에 부합하지 않는 모든 자산(투자자산, 유형자산, 무형자산 및 장기 금융자산 등 포함)",
            "③ 대주주가 보유하여 회사에 절대 양도하지 않는 개인 자산",
            "④ 정부 감정평가사들이 매년 역사적 원가로 고정 보존해 둔 무가치한 자산",
            "⑤ 회사의 해산 당일 현금으로 바꿀 수 없는 가상의 장부 계정"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 상 자산은 유동자산 요건을 충족하면 유동자산으로 분류하고, 유동자산의 정의(4대 요건)에 들지 못하는 나머지 모든 자산은 포괄적으로 '비유동자산'으로 정의합니다.\n\n[오답 해설]\n① 10년 등의 인위적 기간 제한 기준은 없습니다.\n③ 개인 자산이나 ④ 역사적 고정 원가 보존액 등은 비유동자산의 정의가 아닙니다.\n⑤ 비유동자산도 정상적으로 실현 및 현금화될 수 있는 실재 자산입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "10년 한도 등의 규정은 기준에 없습니다.", "articles": [], "principle": "비유동자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "유동자산 요건을 충족하지 못하는 모든 자산을 일컫는 여집합 개념의 대과목 정의입니다.", "articles": [], "principle": "비동자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사주 개인 자산은 제외됩니다.", "articles": [], "principle": "비유동자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 평가 방식에 국한된 자산이 아닙니다.", "articles": [], "principle": "비유동자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "청산 시 실현 불가한 가상 계정이 아닙니다.", "articles": [], "principle": "비유동자산의 정의", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "다음 중 K-IFRS 제1001호 상 재무상태표 본문에 중간합계(Subtotals)를 추가하여 표시하고자 할 때, 이를 승인·허용해 주는 표시 기준 조건은 무엇인가?",
        "options": [
            "① 주주총회의 3/4 이상 특별 특별 승인 도장을 받았을 때만",
            "② 기업의 재무상태를 이해하는 데 목적 적합한(Relevant) 경우",
            "③ 중간합계를 내면 회사의 자산 총액이 2배로 증가해 보일 때",
            "④ 정부 세금 영수증 총액과 대차가 정확히 맞을 때",
            "⑤ 회사의 회계 담당자가 임의로 기장을 편하게 유도하고자 할 때"
        ],
        "answer": "2",
        "explanation": "② K-IFRS는 고정된 형식만을 강요하지 않습니다. 정보이용자가 기업의 재무구조를 보다 명료하게 파악하고 목적적합한 이해를 할 수 있다면 본문에 중간합계나 세부 제목 항목을 자유롭게 추가하여 표시할 수 있게 유연성을 보장합니다.\n\n[오답 해설]\n① 주총 3/4 특별결의 등은 관련이 없습니다.\n③ 장부 외형 부풀리기 목적의 조작 합계는 금지됩니다.\n④, ⑤는 합법적인 중간합계의 표시 기준 근거가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "주주총회 승인 사항이 아닙니다.", "articles": [], "principle": "중간합계 추가 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재무구조 파악에 유용하고 목적적합한 추가 합계(예: 순운전자본 합계 등)는 기재가 전면 보장됩니다.", "articles": [], "principle": "중간합계 추가 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수치를 왜곡 팽창시키기 위한 행위는 차단됩니다.", "articles": [], "principle": "중간합계 추가 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세금 납부 내역의 대차 조율 목적이 아닙니다.", "articles": [], "principle": "중간합계 추가 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 실무자 임의 편의에 따르지 않습니다.", "articles": [], "principle": "중간합계 추가 요건", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "다음 중 K-IFRS 상 주로 단기매매(Short-term trading) 목적으로 보유 중인 금융자산 및 금융부채의 재무상태표 유동성 분류에 관한 원칙은?",
        "options": [
            "① 전액 비유동자산 또는 비유동부채로 100% 강제 고정한다.",
            "② 소유주의 개인 자산이므로 회사의 재무상태표에서 완전히 제거한다.",
            "③ 단기매매 목적이므로 회수/결제 시기와 상관없이 '유동자산' 또는 '유동부채'로 분류한다.",
            "④ 주총 승인 시에만 특별히 영업외비용으로 소각 대체한다.",
            "⑤ 차기에 도래할 세금 면제 몫에만 차감 기재한다."
        ],
        "answer": "3",
        "explanation": "③ 단기매매 목적으로 보유하고 있는 주식 등 금융자산이나 단기매매 조건의 금융부채는 유동성 구분 원칙에 의거해 무조건 '유동자산' 및 '유동부채' 범주에 계상되어야 합니다.\n\n[오답 해설]\n① 비유동 분류는 장기투자 성격 자산에 국한됩니다.\n② 기업의 법적 지분자산이므로 제거할 수 없습니다.\n④ 비용 소각 대상이 아닙니다.\n⑤ 과세 제외 한도와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "단기 거래 목적은 비유동으로 갈 수 없습니다.", "articles": [], "principle": "단기매매 자산/부채 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보고 실체의 자산/부채이므로 누락할 수 없습니다.", "articles": [], "principle": "단기매매 자산/부채 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "단기매매(트레이딩) 목적의 금융상품은 유동자산/유동부채로 분류함이 4대 분류 요건의 핵심 중 하나입니다.", "articles": [], "principle": "단기매매 자산/부채 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 비용 처리(소각)는 불가합니다.", "articles": [], "principle": "단기매매 자산/부채 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세금 차감 계정이 아닙니다.", "articles": [], "principle": "단기매매 자산/부채 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "다음 중 K-IFRS 상 비유동자산으로 분류된 유형자산이나 무형자산 중에서, 유동성 분류를 타 유형으로 바꾸지 않고 '매각예정비유동자산(Assets held for sale)'으로 재분류 공시하기 위한 전제 조건은 무엇인가?",
        "options": [
            "① 해당 자산이 파손되어 물리적으로 형체가 완전히 소멸했을 때",
            "② 해당 자산의 장부금액이 주로 계속적인 사용이 아니라 '매각거래'를 통해 회수될 것이며, 매각가능성이 매우 높고 즉시 매각될 수 있는 요건을 충족할 때",
            "③ 대주주가 본인 자택에 보관하기로 가져간 사적 가구인 경우",
            "④ 정부 공인 재활용 가치 평가 보고서가 당기에 도달했을 때",
            "⑤ 회사의 대표이사가 보너스로 챙기기로 사인한 비자금 자산일 때"
        ],
        "answer": "2",
        "explanation": "② 매각예정비유동자산으로 분류되려면, 자산의 회수 방식이 '사용'이 아닌 '매각'을 통해 이루어질 예정이어야 하며, 1년 내 매각완료 가능성이 매우 높은 매각예정(K-IFRS 1105호) 요건을 갖추어야 합니다.\n\n[오답 해설]\n① 폐기 자산은 손상/폐기 손실 대상이지 매각예정이 아닙니다.\n③, ⑤는 사적 재산 횡령/배임적 설명입니다.\n④ 재활용 보고서 도달이 매각예정 분류의 기준서 상 요건이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산 멸실 시에는 매각예정이 아닌 폐기/제거 처리를 거쳐야 합니다.", "articles": [], "principle": "매각예정분류의 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기준서 제1105호에 따라 매각을 통해 장부금액이 실현될 예정이고 매각 조건이 충족될 때 매각예정자산으로 재분류합니다.", "articles": [], "principle": "매각예정분류의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사적 유용은 회계 상 공시 조건이 아닙니다.", "articles": [], "principle": "매각예정분류의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재활용 보고서가 직접 기준은 아닙니다.", "articles": [], "principle": "매각예정분류의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비자금 연동 설명은 무관합니다.", "articles": [], "principle": "매각예정분류의 요건", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "부채의 유동/비유동 분류에 있어 '보고기간 후 12개월 이상 부채의 결제를 연기할 수 있는 무조건의 권리'가 기말 현재 존재하는지를 판단할 때, 계약 상 권리 수준의 올바른 해석은 무엇인가?",
        "options": [
            "① 기말 현재 시점에 법적 계약서 상으로 기업에게 연기할 무조건적 권리가 확보되어 있어야 한다.",
            "② 기말에는 권리가 없었어도 차기 주주총회 날 기분 좋게 은행이 허락해 줄 가능성만 있으면 100% 존재한다고 본다.",
            "③ 대주주가 대여금을 대리 변제해 주기로 구두 구두 약속한 사실만으로 충분하다.",
            "④ 정부 세무서에서 차환을 대리 보증해 줄 미래 기대치에 따른다.",
            "⑤ 법원에 파산 유예 소송을 신청해 둔 대기 상태이면 무조건 권리가 있는 것이다."
        ],
        "answer": "1",
        "explanation": "① K-IFRS는 기말(보고기간 종료일) 현재의 법적 권리 존부를 최우선 척도로 봅니다. 계약서상 은행의 조건 없는 만기 유예 권한 등이 기업에게 '무조건 권리'로 약정 확보되어 있어야 연기 권리가 있다고 인정합니다.\n\n[오답 해설]\n② 사후 허락 가능성이나 ③ 구두 약속, ④ 정부 보증 기대, ⑤ 소송 대기 등 기말 시점에 계약상 보장되지 않은 불확실한 상태는 권리 보유로 인정되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "보고기간 종료일 기말 현재 계약 및 법률 상 무조건 연기 권리가 회사의 지위로 존속하고 있어야 비유동성 권리가 성립합니다.", "articles": [], "principle": "결제연기 권리의 존재 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사후 기대 가능성이나 희망 섞인 관측은 기말 시점의 권리로 보지 않습니다.", "articles": [], "principle": "결제연기 권리의 존재 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "구두 사적 보증은 계약상 권리로 인정되지 않습니다.", "articles": [], "principle": "결제연기 권리의 존재 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 행정 기대는 회계 상 권리가 아닙니다.", "articles": [], "principle": "결제연기 권리의 존재 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소송 대기 사실이 무조건 만기 연장 권리를 창출하지 않습니다.", "articles": [], "principle": "결제연기 권리의 존재 판정", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "장기차입 계약 조건을 기중에 위반하였으나, 보고기간 종료일 현재 은행의 즉시 상환 요구 사유가 실제 발생하지 않았고 위반 사실이 사후 치유 완료되었을 때의 부채 유동성 판정은?",
        "options": [
            "① 기중에 한 번이라도 위반했으므로 기말에는 무조건 유동부채로 적어야 한다.",
            "② 보고기간 종료일 현재 위반 상태가 치유되어 상환 요구 사유가 없고 결제 연기 권리가 보존되어 있으므로 비유동부채 지위를 유지한다.",
            "③ 주식 자본금의 직접 차감 항목으로 기재한다.",
            "④ 기말 차입금 전체를 전액 잡손실로 감액 소각한다.",
            "⑤ 회사의 법정 납입자본금을 임의로 감소시킨다."
        ],
        "answer": "2",
        "explanation": "② 회계 분류는 기말 시점의 현상을 기준으로 판정합니다. 기중에 약정을 위반했었더라도, 기말(보고기간 종료일) 이전에 위반이 해소되어 은행의 즉시 상환요구권이 소멸하고 결제 연기권이 유효한 상태라면 '비유동부채' 분류를 유지하는 것이 적법합니다.\n\n[오답 해설]\n① 기중의 일시적 위반 사실 자체만으로 기말에 무조건 유동화하지 않습니다.\n③, ④, ⑤는 정당한 채무 변동 회계처리가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기말 현재 위반이 실재하지 않고 치유 완료되었다면 유동화할 이유가 없습니다.", "articles": [], "principle": "기중 약정 위반의 치유와 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기간 종료일 기준의 법적 유예 지위가 온전하고 상환 권리가 미도래한 상태이므로 비유동부채 유지가 타당합니다.", "articles": [], "principle": "기중 약정 위반의 치유와 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 차감 항목과 무관합니다.", "articles": [], "principle": "기중 약정 위반의 치유와 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채를 잡손실로 지울 수 없습니다.", "articles": [], "principle": "기중 약정 위반의 치유와 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "납입자본 감액 거래와 무관합니다.", "articles": [], "principle": "기중 약정 위반의 치유와 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },

    # =========================================================================
    # L3: 적용 (15문항, 576~590번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s02-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "(주)평가는 와인 숙성 제조업을 운영하고 있으며, 회사의 정상영업주기는 15개월이다. 회사가 당기말 현재 보유하고 있는 숙성 중인 와인(재고자산) ₩10,000,000은 향후 14개월 뒤에 판매될 예정이며, 관련 매출채권 ₩8,000,000은 보고기간 종료일로부터 13개월 뒤에 회수될 예정이다. K-IFRS 상 와인 재고자산과 매출채권의 유동성 분류 조합으로 가장 올바른 것은?",
        "options": [
            "① 재고자산: 유동자산 / 매출채권: 유동자산",
            "② 재고자산: 유동자산 / 매출채권: 비유동자산",
            "③ 재고자산: 비유동자산 / 매출채권: 유동자산",
            "④ 재고자산: 비유동자산 / 매출채권: 비유동자산",
            "⑤ 두 항목 모두 금액의 50%만 유동자산으로 안분 분류"
        ],
        "answer": "1",
        "explanation": "① 정상영업주기가 15개월인 기업의 경우, 재고자산(14개월 뒤 판매 예정)과 매출채권(13개월 뒤 회수 예정)은 모두 회사의 정상영업주기(15개월) 범위 내에서 실현될 예정입니다. 따라서 12개월을 초과하더라도 두 자산 모두 '유동자산'으로 분류하는 것이 타당합니다.\n\n[오답 해설]\n②, ③, ④는 12개월 초과만을 기준으로 삼아 비유동 분류를 섞거나 전체 적용한 오류입니다.\n⑤ 임의로 반반 안분하는 규정은 없습니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": True, "why": "재고(14개월) 및 채권(13개월) 모두 15개월 영업주기 내에 정상 실현되는 상거래 자산이므로 전액 유동자산으로 분류합니다.", "articles": [], "principle": "영업주기 내 운전자본 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출채권도 영업주기 내 회수되므로 비유동이 아닌 유동자산입니다.", "articles": [], "principle": "영업주기 내 운전자본 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고자산도 유동자산입니다.", "articles": [], "principle": "영업주기 내 운전자본 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "둘 다 유동자산이므로 비유동 자산 묶음은 틀렸습니다.", "articles": [], "principle": "영업주기 내 운전자본 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "안분 기재 법적 근거는 존재하지 않습니다.", "articles": [], "principle": "영업주기 내 운전자본 분류 적용", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "문 L3-01의 동일한 시나리오 하에서, (주)평가가 와인 원자재 구입처에 지급해야 하는 매입채무 ₩6,000,000이 보고기간 종료일로부터 14개월 뒤에 결제될 예정일 때, 이 매입채무의 기말 유동성 분류는 무엇인가?",
        "options": [
            "① 비유동부채(Non-current Liabilities)",
            "② 유동부채(Current Liabilities)",
            "③ 주식 할인발행차금 계정",
            "④ 무형자산 차감 계정",
            "⑤ 충당부채 가산 항목"
        ],
        "answer": "2",
        "explanation": "② 매입채무는 정상영업주기 내에 결제될 예정인 상거래 운전자본 부채입니다. 회사의 정상영업주기가 15개월이므로, 12개월을 초과한 14개월 만기라 하더라도 주기를 벗어나지 않았으므로 '유동부채'로 분류합니다.\n\n[오답 해설]\n① 12개월 초과라고 하여 비유동부채로 분류하면 상거래 부채의 성격을 오도하므로 틀렸습니다.\n③, ④, ⑤는 성격이 전혀 맞지 않는 부적절한 회계 계정들입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "영업주기 범위 내의 상거래 매입채무이므로 비유동부채가 아닙니다.", "articles": [], "principle": "영업주기 내 매입채무 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "14개월은 15개월 정상영업주기 범위 내이므로 이 매입채무는 유동부채로 보고하여야 합니다.", "articles": [], "principle": "영업주기 내 매입채무 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 차감 계정이 아닙니다.", "articles": [], "principle": "영업주기 내 매입채무 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산의 직접 조정 항목이 아닙니다.", "articles": [], "principle": "영업주기 내 매입채무 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "충당부채가 아닌 확정채무입니다.", "articles": [], "principle": "영업주기 내 매입채무 분류 적용", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "(주)평가는 당기말 현재 ₩30,000,000의 장기차입금(만기 10개월 뒤 도래)을 보유하고 있다. 회사는 기존 대출 차입 약정상 만기를 추가로 3년 연장할 수 있는 무조건적 '재량권(Discretion)'이 계약서상 확실히 보장되어 있으며, 연장할 적극적 의도가 있다. 이 장기차입금의 재무상태표 상 분류로 옳은 것은?",
        "options": [
            "① 유동부채 ₩30,000,000",
            "② 비유동부채 ₩30,000,000",
            "③ 유동부채 ₩15,000,000 / 비유동부채 ₩15,000,000",
            "④ 잡이익 ₩30,000,000 대체",
            "⑤ 자본금 ₩30,000,000 가산"
        ],
        "answer": "2",
        "explanation": "② 만기가 10개월로 임박하였더라도 계약에 따른 12개월 이상 부채 차환(연장) 재량권을 기말 현재 독점 보유하고 있고 연장할 예정이므로 '비유동부채'로 분류함이 조문에 부합합니다.\n\n[오답 해설]\n① 재량권이 없을 때의 분류입니다.\n③ 반반 쪼개는 분류 근거는 없습니다.\n④, ⑤는 부채를 소멸시키는 왜곡된 분개입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "재량권 보유로 만기 연장이 통제 하에 있으므로 유동부채가 아닙니다.", "articles": [], "principle": "차환 재량권 보유 시 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "계약상 만기 연장을 강제할 수 있는 일방적 권리(재량권)가 기업에 확실히 존재하므로 비유동부채로 기재합니다.", "articles": [], "principle": "차환 재량권 보유 시 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의 분할 분류는 타당치 않습니다.", "articles": [], "principle": "차환 재량권 보유 시 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입 채무의 잡손익 임의 대체는 불법입니다.", "articles": [], "principle": "차환 재량권 보유 시 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본화(출자전환) 거래가 기말에 실재하지 않았으므로 틀렸습니다.", "articles": [], "principle": "차환 재량권 보유 시 분류 적용", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "(주)평가는 당기말 현재 ₩50,000,000의 장기차입금(만기 8개월 뒤 도래)을 보유하고 있다. 회사는 차환 연장을 위해 대여 은행과 긴밀히 협상하여 연장 가능성이 매우 높지만, 기말 현재 최종 연장 서명은 되지 않았고 만기 결정 재량권은 계약 상 대여 은행이 전적으로 쥐고 있다. 이 차입금의 기말 분류는 무엇인가?",
        "options": [
            "① 비유동부채 ₩50,000,000",
            "② 유동부채 ₩50,000,000",
            "③ 유동부채 ₩25,000,000 / 비유동부채 ₩25,000,000",
            "④ 주식발행초과금 가산",
            "⑤ 대손상각비 인식"
        ],
        "answer": "2",
        "explanation": "② 협상 중이고 성사 가능성이 아무리 높더라도, 기말 현재 12개월 이상 상환을 연기할 수 있는 독점적이고 무조건적인 계약상 권리(재량권)가 기업에게 없으므로 '유동부채'로 분류하는 것이 타당합니다.\n\n[오답 해설]\n① 기말 기준 권리가 확보되지 않았으므로 비유동부채가 될 수 없습니다.\n③ 임의 분류 쪼개기는 불가합니다.\n④, ⑤는 차입금 만기 분류와 상관없는 오과목들입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "기말 현재 연장 권한이 은행에 묶여 있으므로 비유동부채로 보고할 수 없습니다.", "articles": [], "principle": "재량권 부재 시 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "상환 연기 결정권이 전적으로 채권자에게 있어 회사의 무조건적 권리가 결여되었으므로 기말에는 유동부채로 분류합니다.", "articles": [], "principle": "재량권 부재 시 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금액 반반 나누기는 회계 원칙에 위배됩니다.", "articles": [], "principle": "재량권 부재 시 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 잉여금 가산 대상이 아닙니다.", "articles": [], "principle": "재량권 부재 시 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 감액 비용이 아니므로 상각비 인식은 틀렸습니다.", "articles": [], "principle": "재량권 부재 시 분류 적용", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "(주)평가는 20X1년 10월에 체결된 장기차입 계약 조건을 기중에 위반(부채비율 한도 초과)하여 대여 은행이 즉시 상환을 요구할 수 있는 법적 권리를 갖게 되었다. 그러나 (주)평가는 은행을 설득하여 20X1년 12월 26일(보고기간 말 이전)에 '향후 18개월간 약정 위반을 이유로 상환을 청구하지 않겠다'는 공식 상환 청구 유예 합의서 서명을 완료했다. 20X1년말 재무상태표 상 이 차입금의 올바른 분류는?",
        "options": [
            "① 유동부채",
            "② 비유동부채",
            "③ 주식할인발행차금",
            "④ 영업외수익",
            "⑤ 이연법인세자산"
        ],
        "answer": "2",
        "explanation": "② 보고기간 종료일(20X1년말) 이전에 대여 은행이 상환 청구를 하지 않기로 공식 유예 합의(12개월 이상 유예)를 해 주었으므로, 기말 현재 기업은 결제를 12개월 이상 연기할 무조건의 계약상 권리를 회복·보유한 상태입니다. 따라서 '비유동부채'로 분류하는 것이 적법합니다.\n\n[오답 해설]\n① 기말 이전에 합의가 효력을 발휘하였으므로 유동부채가 아닙니다.\n③, ④, ⑤는 부채 성격과 무관한 잘못된 회계과목들입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "기말 전에 유예 합의가 법적으로 유효하게 체결되어 연기 권리가 있으므로 유동부채가 아닙니다.", "articles": [], "principle": "기말 전 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기간 종료일 이전에 12개월(18개월) 상환 유예를 보장받았으므로 기말에는 비유동부채로 분류합니다.", "articles": [], "principle": "기말 전 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 할인 조정 계정이 아닙니다.", "articles": [], "principle": "기말 전 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 면제 등 손익 거래가 발생하지 않았으므로 영업외수익이 아닙니다.", "articles": [], "principle": "기말 전 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이연법인세와 상관없는 장기차입금 채무입니다.", "articles": [], "principle": "기말 전 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "(주)평가는 20X1년 11월에 장기차입 계약 상 재무비율 요건을 위반하여 채권자로부터 즉시 상환 독촉을 받게 되었다. (주)평가는 기말 현재까지 합의를 이끌어내지 못하다가, 기말 이후인 20X2년 1월 12일(재무제표 발행 승인일은 20X2년 2월 25일)에 은행으로부터 '위반에도 불구하고 향후 15개월 동안 상환 청구를 유예하겠다'는 공식 합의서를 수취하였다. 20X1년말 재무상태표 상 이 차입금의 유동성 분류는?",
        "options": [
            "① 발행승인일 전에 사후 합의가 끝났으므로 비유동부채로 소급 보고한다.",
            "② 20X1년 12월 31일(보고기간 말) 현재 시점에는 즉시 상환 요구 대상(연기 권리 없음)이었으므로 사후 합의와 상관없이 '유동부채'로 분류하여야 한다.",
            "③ 자본금 ₩50,000,000 가산",
            "④ 기타포괄이익 인식",
            "⑤ 대손충당금 차감 표시"
        ],
        "answer": "2",
        "explanation": "② 재무제표의 유동성 분류는 보고기간 말(20X1년말) 현재 존재하는 법적 권리에 기초합니다. 기말 시점에는 결제 연기권이 결여되어 즉시 독촉 대상이었으므로 기말에는 반드시 '유동부채'로 분류하고, 사후에 합의된 사실은 보고기간 후 사건으로 공시할 주석 정보에 해당합니다.\n\n[오답 해설]\n① 보고기간 후 사건의 본문 소급 반영은 분류상 금지됩니다.\n③ 자본금 전입 대상이 아닙니다.\n④, ⑤는 채무 분류와 무관한 과목 설명입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "사후적 합의가 승인일 전에 성사되었더라도 기말 현재의 연기 권리를 부활해 주지 못하므로 비유동 분류는 안 됩니다.", "articles": [], "principle": "기말 후 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "20X1년 12월 31일 시점에 즉시 결제 유예할 무조건의 권리가 없었으므로 유동부채 기재가 적법합니다.", "articles": [], "principle": "기말 후 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "출자전환 자본 기입이 아닙니다.", "articles": [], "principle": "기말 후 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기타포괄이익 가산 계정이 아닙니다.", "articles": [], "principle": "기말 후 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채무에 대손충당금 자산 차감 항목을 섞는 것은 불법 기장입니다.", "articles": [], "principle": "기말 후 약정유예 합의 분류 적용", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "(주)평가는 기말 현재 세법 상 유보 발생에 따라 이연법인세자산 ₩10,000,000을 산출하였다. 이 자산 중 ₩4,000,000은 차기(12개월 이내) 법인세 납부 시 정산(실현)될 예정이며, 나머지 ₩6,000,000은 2년 뒤에 실현될 예정이다. 기말 재무상태표에 표시되어야 하는 이연법인세자산의 유동/비유동 분류 조합으로 가장 옳은 것은?",
        "options": [
            "① 유동자산: ₩4,000,000 / 비유동자산: ₩6,000,000",
            "② 유동자산: ₩0 / 비유동자산: ₩10,000,000",
            "③ 유동자산: ₩10,000,000 / 비유동자산: ₩0",
            "④ 전액 자본조정의 차감 항목으로 계상",
            "⑤ 전액 부채 성격의 이연법인세부채로 통합 ₩10,000,000 계상"
        ],
        "answer": "2",
        "explanation": "② 이연법인세자산은 당기 정산(실현) 예정액의 크기와 무관하게 무조건 전액 '비유동자산'으로 보고하도록 규정되어 있습니다. 유동 분류액은 ₩0원이며, 비유동자산으로 ₩10,000,000 전액 계상해야 합니다.\n\n[오답 해설]\n① 은 유동/비유동 쪼개기 분류 오류입니다.\n③ 은 전액 유동자산 분류 오류입니다.\n④ 자본조정 차감 처리가 아닙니다.\n⑤ 자산과 부채를 허가 없이 자의적 상계 통합 보고한 위반입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "일부를 유동 분류하는 회계처리는 금지됩니다.", "articles": [], "principle": "이연법인세의 강제 비유동 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이연법인세자산은 유동 항목 기재가 일절 금지되므로 전액(₩10,000,000) 비유동자산으로 분류하여 기재합니다.", "articles": [], "principle": "이연법인세의 강제 비유동 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동자산으로 분류할 수 없습니다.", "articles": [], "principle": "이연법인세의 강제 비유동 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 차감 조정 성격이 아닌 자산입니다.", "articles": [], "principle": "이연법인세의 강제 비유동 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산과 부채는 자의적으로 상계하여 하나로 지울 수 없습니다.", "articles": [], "principle": "이연법인세의 강제 비유동 분류 적용", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "(주)평가는 기말 현재 현금및현금성자산 ₩100,000,000을 보유하고 있다. 이 중 ₩30,000,000은 대여금에 대한 질권(담보)이 설정되어 기말로부터 향후 18개월 동안 인출 및 상환 목적의 사용이 전면 제한되어 있으며, 나머지 ₩70,000,000은 제한이 없다. 기말 재무상태표에 표시되어야 하는 유동자산 성격의 현금및현금성자산과 비유동자산(장기 금융상품 등)의 올바른 배분액은?",
        "options": [
            "① 유동자산 현금: ₩100,000,000 / 비유동자산: ₩0",
            "② 유동자산 현금: ₩70,000,000 / 비유동자산: ₩30,000,000",
            "③ 유동자산 현금: ₩0 / 비유동자산: ₩100,000,000",
            "④ 유동자산 현금: ₩30,000,000 / 비유동자산: ₩70,000,000",
            "⑤ 전체 ₩100,000,000을 강제 자본금 증자 계정으로 기입"
        ],
        "answer": "2",
        "explanation": "② 현금이라 하더라도 12개월 이상의 장기 사용 제한이 걸려 있다면 이는 유동성 자산의 성격을 상실하므로 비유동자산(장기 금융상품 등)으로 분류합니다. 따라서 유동자산 ₩70,000,000, 비유동자산 ₩30,000,000이 올바릅니다.\n\n[오답 해설]\n① 질권 설정을 무시하고 전액 유동 기재하여 오답입니다.\n③, ④는 대소 분류액이 잘못 매칭되었습니다.\n⑤ 증자 거래가 없었으므로 자본금 증가는 틀렸습니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "사용이 장기 제한된 현금까지 유동자산으로 묶으면 안 됩니다.", "articles": [], "principle": "현금의 질권설정 시 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "1년(12개월) 이상 사용이 묶여 있는 ₩30,000,000은 비유동자산으로 가고, 자유로운 ₩70,000,000만 유동성 현금으로 적습니다.", "articles": [], "principle": "현금의 질권설정 시 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전체 현금을 비유동화할 이유가 없으므로 틀렸습니다.", "articles": [], "principle": "현금의 질권설정 시 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금액 분류 대입이 서로 바뀌어 오답입니다.", "articles": [], "principle": "현금의 질권설정 시 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 납입 대체 분개는 어긋납니다.", "articles": [], "principle": "현금의 질권설정 시 유동성 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "(주)평가는 정상영업주기가 8개월인 도매업체이다. 회사가 보유한 거래처 C사에 대한 매출채권 ₩15,000,000의 최종 만기가 보고기간 종료일로부터 11개월 뒤에 도래할 때, 이 매출채권의 기말 유동성 분류 판단은?",
        "options": [
            "① 영업주기(8개월)를 초과하여 회수되므로 비유동자산으로 분류한다.",
            "② 영업주기(8개월)를 초과하더라도, 보고기간 후 12개월 이내에 회수될 예정이므로 유동자산으로 분류한다.",
            "③ 대손충당금의 직접 취득 가격에 가산한다.",
            "④ 주식 할인발행 계정의 매출로 통합한다.",
            "⑤ 회사의 법정 납입 자본금 증가로 분류한다."
        ],
        "answer": "2",
        "explanation": "② 유동자산 분류 요건에 따르면 정상영업주기 이내이거나, 혹은 보고기간 후 12개월 이내에 실현(회수)될 것으로 예상되는 자산은 유동자산입니다. 11개월 만기 채권은 12개월 이내이므로 당연히 '유동자산'으로 분류합니다.\n\n[오답 해설]\n① 영업주기를 넘더라도 12개월 이내이므로 비유동이 될 수 없습니다.\n③ 충당금 취득가 가산 설명은 오류입니다.\n④, ⑤는 매출채권 분류와 무관한 과목 소설입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "영업주기를 초과하더라도 12개월 이내 만기이므로 비유동자산 분류는 틀렸습니다.", "articles": [], "principle": "영업주기와 12개월의 복합 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "영업주기가 짧더라도 회수 한계선인 12개월 이내(11개월)에 들어오므로 유동자산으로 분류하는 것이 맞습니다.", "articles": [], "principle": "영업주기와 12개월의 복합 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손충당금 관련 처리 설명은 오류입니다.", "articles": [], "principle": "영업주기와 12개월의 복합 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "할인발행 자본조정 통합 기재는 오류입니다.", "articles": [], "principle": "영업주기와 12개월의 복합 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 증가 거래가 아닙니다.", "articles": [], "principle": "영업주기와 12개월의 복합 판정", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "(주)평가는 정상영업주기가 20개월인 선박 건조 업체이다. 당기말 현재 (주)평가가 건조 중인 미완성 선박(재고자산)의 장부가액은 ₩40,000,000이며, 앞으로 17개월 뒤에 건조가 완료되어 발주처에 인도(매출 실현)될 예정이다. 이 건조 중 선박 재고자산의 재무상태표 상 올바른 유동성 분류는?",
        "options": [
            "① 만기가 12개월을 초과하므로 비유동자산으로 보고하여야 한다.",
            "② 만기가 12개월을 초과하더라도, 회사의 정상영업주기(20개월) 범위 내에서 판매·소비될 재고자산이므로 유동자산으로 분류한다.",
            "③ 대손충당금의 평가이익 가산으로 잡는다.",
            "④ 전액 당기 손실 비용으로 소각 처리한다.",
            "⑤ 회사의 자본 내 이익잉여금 증가로 즉시 직접 가산한다."
        ],
        "answer": "2",
        "explanation": "② 정상영업주기가 20개월인 장기 제조 실체의 경우, 12개월을 넘는 17개월 뒤 인도 예정인 미완성 선박 재고자산이라 하더라도, 영업주기 내 순환되는 운전자본이므로 '유동자산'으로 보고합니다.\n\n[오답 해설]\n① 영업주기 원칙의 예외를 무시한 단순 12개월 기준 오류입니다.\n③ 재고에 대손평가 가산은 부적절합니다.\n④ 미인도 자산을 비용 소각하는 것은 분식입니다.\n⑤ 자산 기장을 이익잉여금 직접 가산으로 처리할 수 없습니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "조선업 등 장기 제조의 경우 재고자산은 1년 초과 시에도 유동자산이 되므로 비유동은 틀렸습니다.", "articles": [], "principle": "장기영업주기 재고의 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재고자산은 만기가 17개월로 1년을 초과하나 20개월 영업주기 이내이므로 유동자산으로 분류함이 맞습니다.", "articles": [], "principle": "장기영업주기 재고의 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "충당금 평가이익 가산은 맞지 않습니다.", "articles": [], "principle": "장기영업주기 재고의 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정상 자산의 당기 손실 소각은 위법 기장입니다.", "articles": [], "principle": "장기영업주기 재고의 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손익계산서 등을 거치지 않고 이익잉여금을 바로 늘리는 분개는 불가합니다.", "articles": [], "principle": "장기영업주기 재고의 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "은행으로부터의 차입금 ₩80,000,000의 계약 만기가 11개월 뒤에 도래하지만, 회사는 기존 계약 규정에 의거하여 은행의 추가 동의 없이도 만기를 1년 더 연장할 수 있는 독점적 권리를 보유하고 있고 연장할 의사가 확실하다. 기말 시점 이 차입금의 올바른 분류는?",
        "options": [
            "① 유동부채 ₩80,000,000",
            "② 비유동부채 ₩80,000,000",
            "③ 주식발행초과금 가산",
            "④ 잡이익 ₩80,000,000",
            "⑤ 대손충당금 차감 표시"
        ],
        "answer": "2",
        "explanation": "② 기말 현재 기업이 채권자의 추가적이고 우발적인 동의 없이 만기를 12개월 이상 늦출 수 있는 독점적이고 일방적인 재량 권리를 확보하고 있으므로, 계약상 만기 11개월에 구속되지 않고 '비유동부채'로 분류합니다.\n\n[오답 해설]\n① 일방적 권리를 보유한 경우 유동부채로 분류하지 않습니다.\n③, ④, ⑤는 차입 채무를 소멸시키거나 자본금 잉여금 등으로 잘못 보낸 소설적 오류입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "독점적 차환 권리가 있으므로 단기 유동부채로 보고하지 않습니다.", "articles": [], "principle": "독점적 만기연장권 보유 차입금", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "추가 동의 없는 만기 연장 권리는 차입부채의 실질적인 상환 지연을 보장하므로 비유동부채로 분류합니다.", "articles": [], "principle": "독점적 만기연장권 보유 차입금", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본화(주발초) 대체 계정이 아닙니다.", "articles": [], "principle": "독점적 만기연장권 보유 차입금", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채무 면제 사건이 아니므로 이익 인식이 불가합니다.", "articles": [], "principle": "독점적 만기연장권 보유 차입금", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손충당금 차감은 부채에 적용되지 않습니다.", "articles": [], "principle": "독점적 만기연장권 보유 차입금", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "(주)평가는 단기매매 차익을 얻을 목적으로 보유하고 있는 상장사 주식(공정가치 ₩30,000,000)이 있다. 회사는 이 주식을 향후 2년간은 시장 상황 급변 전까지 매각하지 않고 계속 보유할 계획이다. 기말 재무상태표 상 이 상장사 주식의 올바른 유동성 분류는?",
        "options": [
            "① 향후 2년간 보유할 계획이므로 비유동자산으로 분류한다.",
            "② 보유 기간 계획과 상관없이, 본질적 보유 목적이 단기매매(Trading)이므로 유동자산(단기금융상품 등)으로 분류한다.",
            "③ 전액 잡손실로 감액 대체한다.",
            "④ 기말 이자수익 ₩30,000,000을 인식한다.",
            "⑤ 회사의 법정 자본금 감액 계정으로 가산한다."
        ],
        "answer": "2",
        "explanation": "② 단기매매(트레이딩) 목적으로 보유 중인 금융자산은 유동성 분류 기준 상 실제 매각 시점을 경영진이 향후 1~2년 뒤로 미루어 예상하더라도, 자산의 취득 본질 목적이 단기 회전 매매에 속하므로 '유동자산'으로 고정 보고해야 합니다.\n\n[오답 해설]\n① 2년 보유 계획이라는 경영진의 일시적 의도를 앞세워 비유동자산으로 분류하면 영업 자산 왜곡이 되므로 틀렸습니다.\n③ 미매각 상태의 임의 전액 손실 소각은 불법입니다.\n④ 주식은 배당이나 평가이익 대상이지 이자수익 발생 대상이 아닙니다.\n⑤ 자본금 감액 거래와 무관합니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "취득 성격이 단기매매이므로 2년 보유 예상만으로 비유동 분류할 수 없습니다.", "articles": [], "principle": "단기매매 주식의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "단기매매 목적으로 보유하는 자산은 결제/실현 시기 의도와 무관하게 유동자산으로 기재함이 원칙입니다.", "articles": [], "principle": "단기매매 주식의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 손실 대체 처리는 회계 왜곡입니다.", "articles": [], "principle": "단기매매 주식의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주식 평가에서 생긴 이자수익 인식 주장은 오답입니다.", "articles": [], "principle": "단기매매 주식의 유동성 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감자(자본금 감액) 등기 거래가 아닙니다.", "articles": [], "principle": "단기매매 주식의 유동성 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "(주)평가는 20X1년말 만기가 도래하는 단기차입금 ₩50,000,000이 있다. 회사는 이를 차환하기 위해 20X1년 12월 28일에 신규 장기차입 계약(만기 3년) 체결을 완료하였다. 다만, 구 차입금의 실제 상환 일자는 20X2년 1월 5일로 약정되었다. 20X1년말 재무상태표 상 구 차입금 ₩50,000,000의 올바른 분류는?",
        "options": [
            "① 신규 대출 계약이 완료되었으므로 기말에 비유동부채로 분류한다.",
            "② 구 차입금은 20X1년 12월 31일 현재 상환 의무가 임박(12개월 이내 결제)하고 자체 차환권이 없으므로 '유동부채'로 보고하여야 한다.",
            "③ 전액 자본금 가산으로 주식 발행 분개 처리한다.",
            "④ 기말 이자수익 ₩50,000,000을 인식한다.",
            "⑤ 대손충당금 마이너스 잔액으로 자산에서 상쇄 보고한다."
        ],
        "answer": "2",
        "explanation": "② 구 차입금 자체는 만기가 12개월 내에 도래하고, 기존 계약에 의한 차환권이 아닌 신규 별개 대출 계약을 맺어 갚는 것입니다. 20X1년말 현재 구 차입금은 12개월 내에 상환되어야 하므로 '유동부채'로 분류하는 것이 적법합니다.\n\n[오답 해설]\n① 신규 별도 대출 계약을 맺었다고 하여 구 차입금 자체를 비유동화할 수 없습니다.\n③ 주식 발행이 수반되지 않았습니다.\n④, ⑤는 타당하지 않은 회계과목 대입입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "별개 대출로 차환할 뿐이므로 구 채무 자체는 비유동부채가 될 수 없습니다.", "articles": [], "principle": "신규차입계약과 기존부채분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "20X1년말 현재 구 차입금의 만기가 1년 미만이고, 기존 만기를 회사 뜻대로 연기할 자체 권리가 없으므로 유동부채로 분류합니다.", "articles": [], "principle": "신규차입계약과 기존부채분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "출자전환 자본화 분개 대상이 아닙니다.", "articles": [], "principle": "신규차입계약과 기존부채분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자수익 발생 거래가 아닌 채무 만기 분류입니다.", "articles": [], "principle": "신규차입계약과 기존부채분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손충당금은 부채의 차감 계정이 아닙니다.", "articles": [], "principle": "신규차입계약과 기존부채분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "(주)평가는 은행 차입금의 기중 이자를 기한 내 지급하지 못해 연체 상태에 빠졌다. 대출 계약서에 따르면 연체 발생 시 은행은 즉시 전액 상환 청구가 가능하다고 명시되어 있으며, 기말 현재 연체 및 위반 상태가 지속 중이다. 이 차입금의 기말 재무상태표 상 유동성 분류는?",
        "options": [
            "① 은행이 실제 소송을 제기하기 전까지는 비유동부채로 유지한다.",
            "② 기말 현재 상환 독촉을 미룰 수 있는 법적 권리가 전무하므로 '유동부채'로 분류한다.",
            "③ 전액 자본조정의 감액 항목으로 대체한다.",
            "④ 기말 연체 이자 비용을 수익으로 조작 가산한다.",
            "⑤ 대손충당금의 평가이익 가산으로 잡는다."
        ],
        "answer": "2",
        "explanation": "② 기말 현재 이자 연체 위반으로 대여 은행이 전액 즉시 회수권을 보유하고 있고 회사는 거절 권리가 없습니다. 따라서 기말 기준 연기 권리가 박탈된 상태이므로 '유동부채'로 분류하여 공시해야 합니다.\n\n[오답 해설]\n① 실제 소송 개기 전이라도 법적 약정상 권리가 상실되었으므로 비유동 유지는 불가합니다.\n③ 자본 거래가 아닙니다.\n④, ⑤는 회계 기준 및 일반 원리에 어긋나는 허구의 분개입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": False, "why": "소송 청구 전이라도 계약 상 권리 침해로 상환 요구가 가능하므로 비유동 유지는 틀렸습니다.", "articles": [], "principle": "연체 지속 차입금의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보고기간 종료일 현재 연체 위반 상태가 유지되어 독촉권이 발동되었으므로 유동부채 분류가 적법합니다.", "articles": [], "principle": "연체 지속 차입금의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지분 자본조정 거래가 아닙니다.", "articles": [], "principle": "연체 지속 차입금의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "연체 이자 비용을 수익화하는 조작은 불법입니다.", "articles": [], "principle": "연체 지속 차입금의 분류 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "충당금 평가이익 가산 대상이 아닙니다.", "articles": [], "principle": "연체 지속 차입금의 분류 적용", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "(주)평가는 당기말 세법상 일시적차이의 정산으로 이연법인세부채 ₩5,000,000을 인식하였다. 이 채무 중 ₩2,000,000은 차기(12개월 이내)에 소멸 실현될 것으로 예상되며, ₩3,000,000은 그 이후에 실현될 예정이다. 기말 재무상태표 상 유동부채에 가산되어야 하는 이연법인세부채 금액은 얼마인가?",
        "options": [
            "① ₩0",
            "② ₩2,000,000",
            "③ ₩3,000,000",
            "④ ₩5,000,000",
            "⑤ ₩10,000,000"
        ],
        "answer": "1",
        "explanation": "① 이연법인세부채는 실현 예상일과 관계없이 절대로 유동부채로 표시될 수 없고 전액 비유동부채로 가야 합니다. 따라서 유동부채에 가산될 금액은 ₩0원입니다.\n\n[오답 해설]\n② 일부 유동 분류 금액을 가정한 오류입니다.\n③, ④는 비유동 분류 의무 규정을 위배한 오산출 수치입니다.\n⑤ 임의의 중복 합산액입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": True, "why": "이연법인세부채는 유동부채로 갈 수 있는 금액이 규정 상 0원이므로 1이 정답입니다.", "articles": [], "principle": "이연법인세부채의 유동부채 가산액", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "₩2,000,000은 차기 실현분이더라도 유동부채가 되지 않습니다.", "articles": [], "principle": "이연법인세부채의 유동부채 가산액", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차기 이후 소멸분은 당연히 비유동부채입니다.", "articles": [], "principle": "이연법인세부채의 유동부채 가산액", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전체 금액은 비유동부채로 표시됩니다.", "articles": [], "principle": "이연법인세부채의 유동부채 가산액", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "오계산 수치입니다.", "articles": [], "principle": "이연법인세부채의 유동부채 가산액", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },

    # =========================================================================
    # L4: 분석 (8문항, 591~598번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s02-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "K-IFRS 제1001호 '재무상태표 표시 및 분류'에 관한 설명 중 옳은 것을 모두 고른 것은?\n\n```\nㄱ. 이연법인세자산은 회수가능 시점의 장단기에 따라 유동자산으로 쪼개어 일부 표시할 수 없다.\nㄴ. 신뢰성 있고 더욱 목적적합한 정보 제공 시 일부는 유동/비유동 구분법으로, 나머지는 유동성 순서법으로 섞어 표시하는 혼합표시방법이 허용된다.\nㄷ. 기중 약정 위반으로 즉시 상환 청구가 가능해진 부채라도 기말 이후 발행승인일 전에 은행이 상환 청구를 하지 않기로 유예 합의했다면 기말 재무상태표에 비유동부채로 소급 보고한다.\nㄹ. 영업주기가 12개월을 초과하는 조선업체의 재고자산은 영업주기 내 실현될 예정이라도 무조건 비유동자산으로 분류하여야 한다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄷ, ㄹ",
            "④ ㄱ, ㄴ, ㄹ",
            "⑤ ㄴ, ㄷ, ㄹ"
        ],
        "answer": "1",
        "explanation": "① 보기 분석:\nㄱ. 참: 이연법인세자산은 유동자산으로 쪼개어 표시할 수 없습니다(무조건 비유동).\nㄴ. 참: 혼합 표시방법이 특정 조건(신뢰성/목적적합성 제고) 하에 허용됩니다.\nㄷ. 거짓: 기말 이후에 유예 합의된 것은 기말 시점의 권리 복구가 안 되므로 여전히 유동부채입니다. 소급 보고 설명은 오류입니다.\nㄹ. 거짓: 영업주기 내의 재고자산은 1년 초과 시에도 유동자산으로 분류합니다. 비유동 분류 설명은 오류입니다.\n따라서 옳은 보기는 ㄱ, ㄴ 입니다.\n\n[오답 해설]\n②, ③, ⑤는 거짓 보기(ㄷ, ㄹ)를 포함하여 오답입니다.\n④는 거짓 보기 ㄹ을 포함하여 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "ㄱ과 ㄴ이 모두 타당한 조문 설명이므로 1이 정답입니다.", "articles": [], "principle": "재무상태표 조문 종합 정오판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 기말 후 합의 시 유동부채이므로 거짓 서술을 포함해 오답입니다.", "articles": [], "principle": "재무상태표 조문 종합 정오판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 영업주기 내 재고의 유동자산 분류 원칙에 위배되므로 거짓 조합입니다.", "articles": [], "principle": "재무상태표 조문 종합 정오판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ을 포함하여 오답입니다.", "articles": [], "principle": "재무상태표 조문 종합 정오판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ과 ㄹ을 포함하여 오답입니다.", "articles": [], "principle": "재무상태표 조문 종합 정오판단", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "(주)평가는 당기말 현재 다음과 같은 3개의 부채(차입금) 계약을 가지고 있다. 20X1년말 재무상태표에 기재되어야 하는 '유동부채'의 합계액은 얼마인가?\n\n```\n• 차입금 A (₩20,000,000): 만기가 8개월 뒤 도래하며, 회사가 계약에 따라 1년 이상 연장할 수 있는 독점적 차환 재량권을 보유하고 있고 연장할 의도가 있다.\n• 차입금 B (₩30,000,000): 기중에 약정을 위반하여 은행이 즉시 상환 요구할 수 있게 되었으나, 20X1년 12월 24일(기말 전)에 은행이 상환 요구를 15개월 유예하기로 공식 서면 합의해 주었다.\n• 차입금 C (₩40,000,000): 기중에 약정을 위반하여 은행이 즉시 상환 요구할 수 있게 되었고, 기말 현재까지 아무런 합의가 없다가 기말이 지난 20X2년 1월 10일에 은행이 18개월간 상환 유예를 합의해 주었다.\n```",
        "options": [
            "① ₩0",
            "② ₩20,000,000",
            "③ ₩40,000,000",
            "④ ₩60,000,000",
            "⑤ ₩90,000,000"
        ],
        "answer": "3",
        "explanation": "③ 부채별 유동성 분류 분석:\n- 차입금 A: 연장 재량권이 회사에 있으므로 '비유동부채' 분류 (유동 ₩0).\n- 차입금 B: 기말 전에 15개월 유예 합의가 성사되어 연기 권리가 있으므로 '비유동부채' 분류 (유동 ₩0).\n- 차입금 C: 기말 후(20X2년 1월)에 비로소 합의가 성사되어 20X1년말 종료일 현재 기준으로는 즉시 독촉 대상(연기 권리 없음)이었으므로 '유동부채'로 분류 (유동 ₩40,000,000).\n따라서 유동부채 합계액은 차입금 C의 ₩40,000,000 뿐입니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 각 부채의 분류 판단 실수에 따른 잘못된 합계 수치입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "차입금 C가 유동부채로 분류되어야 하므로 0원은 틀렸습니다.", "articles": [], "principle": "복합 부채 유동부채 총액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입금 A는 비유동부채이므로 합계 오류입니다.", "articles": [], "principle": "복합 부채 유동부채 총액 산정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "차입금 C(₩40,000,000)만 기말 권리 결여로 유동부채가 되어 ₩40,000,000이 정답입니다.", "articles": [], "principle": "복합 부채 유동부채 총액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "A와 C를 합하는 등 오계산치입니다.", "articles": [], "principle": "복합 부채 유동부채 총액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전체 합산액은 분류 오류를 수반한 수치입니다.", "articles": [], "principle": "복합 부채 유동부채 총액 산정", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "(주)평가는 당기말 현재 다음과 같은 4개의 자산 계약 상태를 보유하고 있다. K-IFRS 상 기말 재무상태표에 기재되는 '유동자산'의 총합계액은 얼마인가? (단, 정상영업주기는 14개월로 명확히 입증된다.)\n\n```\n• 매출채권 A (₩10,000,000): 영업 활동 주기와 연계되어 있으며, 보고기간 종료일로부터 13개월 뒤에 회수될 예정이다.\n• 재고자산 B (₩20,000,000): 정상영업주기 내에 정상 제조 완료 및 처분될 예정이나, 실제 인도 예정일은 기말 기준 15개월 뒤이다.\n• 금융기관 예금 C (₩30,000,000): 현금성자산이나, 공장 담보 목적으로 설정되어 기말로부터 향후 18개월 동안 출금 및 상환 목적의 사용이 차단(제한)되어 있다.\n• 단기매매 주식 D (₩40,000,000): 단기 시세차익 목적으로 취득하여 기말 공정가치 평가액을 반영하고 있다.\n```",
        "options": [
            "① ₩50,000,000",
            "② ₩70,000,000",
            "③ ₩80,000,000",
            "④ ₩90,000,000",
            "⑤ ₩100,000,000"
        ],
        "answer": "1",
        "explanation": "① 자산별 유동성 분류 분석:\n- 매출채권 A: 정상영업주기(14개월) 범위 내(13개월)에 실현 예정이므로 '유동자산' 분류 (₩10,000,000).\n- 재고자산 B: 인도 예정이 15개월 뒤로 정상영업주기(14개월)를 초과합니다. 영업주기를 벗어났고 12개월도 넘어가므로 '비유동자산'으로 분류 (유동 ₩0).\n- 예금 C: 사용제한 기간이 18개월(12개월 이상)이므로 '비유동자산' 분류 (유동 ₩0).\n- 단기매매 주식 D: 단기매매 성격의 자산이므로 당연히 '유동자산' 분류 (₩40,000,000).\n따라서 유동자산 합계액 = 매출채권 A ₩10,000,000 + 주식 D ₩40,000,000 = ₩50,000,000 입니다.\n\n[오답 해설]\n②, ③, ④, ⑤는 재고 B나 예금 C의 유동성 분류 기준 적용 실수에 따른 오류 합산 결과들입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": True, "why": "채권 A(₩10,000,000)와 주식 D(₩40,000,000)만 유동자산이 되므로 합계 ₩50,000,000이 정답입니다.", "articles": [], "principle": "복합 자산 유동자산 총액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고 B를 포함하는 등 잘못 계산된 수치입니다.", "articles": [], "principle": "복합 자산 유동자산 총액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "예금 C를 포함하는 등 잘못 계산된 수치입니다.", "articles": [], "principle": "복합 자산 유동자산 총액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고와 다른 분류를 잘못 섞은 결과입니다.", "articles": [], "principle": "복합 자산 유동자산 총액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전체 자산을 합산하여 유동성 분류 오류를 반영한 결과입니다.", "articles": [], "principle": "복합 자산 유동자산 총액 산정", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "K-IFRS 상 재무상태표의 자산/부채 유동성 분류 기준과 이연법인세 세무 조정 영향에 관한 분석으로 가장 올바르지 않은 것은?",
        "options": [
            "① 이연법인세자산과 부채를 무조건 비유동성 대과목으로 분류하게 강제한 것은 매기 발생하는 세제 조정 실현일의 급변성을 감안한 신뢰성 통제 목적이다.",
            "② 재고자산과 매출채권의 유동성 분류 시에는 '12개월 기준'보다 기업 고유의 '정상영업주기 기준'이 우선하여 적용된다.",
            "③ 사외적립자산의 초과적립액이나 확정급여 자산 등의 유동성 분류 역시 개별 기준서가 요구하지 않는 한 원칙적으로 비유동성 성격을 띤다.",
            "④ 이연법인세부채는 차기에 결제(소멸)가 확실히 입증되더라도 재무상태표에는 무조건 유동부채로 우선 보고하는 예외가 인정된다.",
            "⑤ 정상영업주기가 식별 곤란한 기업은 세무 상 법정 기한에 귀속되지 않고 12개월 영업주기 가정을 강제 적용받는다."
        ],
        "answer": "4",
        "explanation": "④ 이연법인세부채는 차기(12개월 이내) 결제가 명백히 입증되더라도 절대로 유동부채로 보고할 수 없으며 무조건 '비유동부채'로 분류하는 것이 K-IFRS의 예외 없는 강제 규칙이므로 유동 보고 예외 주장은 전형적 오류입니다.\n\n[오답 해설]\n① 비유동 고정의 취지를 잘 설명했습니다.\n② 운전자본은 영업주기가 12개월보다 우선합니다.\n③ 퇴직급여 연동 자산의 일반적 비유동 성격을 참으로 설명했습니다.\n⑤ 불명확 시 12개월 가정을 바르게 설명했습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비유동 고정의 신뢰성 향상 목적 지적은 타당합니다.", "articles": [], "principle": "이연법인세와 자산부채 분류 종합분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고/채권의 영업주기 우선 원칙은 참입니다.", "articles": [], "principle": "이연법인세와 자산부채 분류 종합분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "퇴직급여 관련 자산의 비유동 지위 기술은 참입니다.", "articles": [], "principle": "이연법인세와 자산부채 분류 종합분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이연법인세부채는 회수/결제 시점 불문 예외 없이 비유동부채가 되어야 하므로 4의 유동부채 우선 기재 예외 주장은 위반 서술입니다.", "articles": [], "principle": "이연법인세와 자산부채 분류 종합분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "식별 곤란 시 12개월 주기 준용 규칙은 참입니다.", "articles": [], "principle": "이연법인세와 자산부채 분류 종합분석", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "다음 중 K-IFRS 상 부채의 유동성 분류 결정이 기업의 주요 단기 재무 건전성 분석 지표인 '유동비율(Current Ratio = 유동자산 / 유동부채)'에 미치는 왜곡 효과 분석으로 가장 올바르지 않은 것은?",
        "options": [
            "① 만기가 12개월 내에 도래하는 차입금을 재량권 없이 비유동부채로 허위 기재하면 분모가 작아져 유동비율이 과대 평가된다.",
            "② 대출약정 위반 채무에 대해 기말 후 사후 유예 합의가 있었음을 핑계로 비유동부채로 계상하면 유동비율이 비정상적으로 높게 보고되어 건전성 정보가 왜곡된다.",
            "③ 유동성 재분류 오류는 대차평균 원리상 재무상태표의 자산 총계와 부채 총계 자체를 2배로 증가시킨다.",
            "④ 채환 약정의 실제 구속력이나 재량권 유무를 정밀하게 따지지 않고 장기 차입금을 기계적으로 비유동 고정 분류하면 단기 채무 불이행 위험 예측력을 저해한다.",
            "⑤ 영업주기가 18개월인 기업의 상 상거래 매입채무를 유동 분류하는 것은 지극히 타당하므로 유동비율 산정을 왜곡하지 않는다."
        ],
        "answer": "3",
        "explanation": "③ 유동과 비유동의 분류 변경은 자본 내의 계정 분류 변동일 뿐, 대차대조표의 자산 총액이나 부채 총액 자체를 변동시키지 않습니다. 자산/부채 총계를 2배로 증가시킨다는 주장은 기초 복식부기 이론에 어긋나는 오류입니다.\n\n[오답 해설]\n① 유동부채 누락 시 유동비율 과대평가 문제를 올바르게 분석했습니다.\n② 기말 후 합의 부채의 비유동 위장 기장의 위험성을 바르게 설명했습니다.\n④, ⑤는 유동비율 예측 한계 및 정상영업주기 매입채무 분류의 타당성을 잘 짚었습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "허위 비유동 기장 시 단기 유동비율이 왜곡되어 건전성이 과장된다는 분석은 참입니다.", "articles": [], "principle": "분류 오류가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기말 후 합의 사항을 소급 적용 시 건전성 정보의 오도를 유발함은 참입니다.", "articles": [], "principle": "분류 오류가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "유동성 분류 변경(유동 $\\leftrightarrow$ 비유동)은 분류상 재배치이므로 총액 자산이나 부채 크기를 변화시키지 않아 3의 증가 주장은 오류입니다.", "articles": [], "principle": "분류 오류가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재량권 검토 누락 시 유동성 건전성 예측 신뢰도가 떨어진다는 분석은 참입니다.", "articles": [], "principle": "분류 오류가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정상영업주기 상거래 부채의 유동 분류는 지극히 정당하므로 참입니다.", "articles": [], "principle": "분류 오류가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "다음 중 K-IFRS 상 부채의 결제(Settlement) 연기 권리 충족 여부를 판단할 때, '보고기간 말 이전에 부여된 유예기간(Grace period)'의 기간 조건이 유동/비유동 판정에 미치는 영향으로 가장 옳은 것은?",
        "options": [
            "① 은행이 부여한 유예기간이 3개월이든 6개월이든 무조건 비유동부채가 된다.",
            "② 대여자가 부여한 유예기간은 적어도 보고기간 후 '12개월 이상'의 기간이어야만 기말에 비유동부채로 분류할 수 있는 정당한 권리가 된다.",
            "③ 유예기간이 하루라도 부여되면 무조건 주식 자본금으로 분류를 변경한다.",
            "④ 유예기간 정보는 주석에 공시할 수 없으며 무조건 기밀유지 의무를 진다.",
            "⑤ 유예 합의가 있으면 해당 부채의 이자율은 법적으로 자동 0%가 강제된다."
        ],
        "answer": "2",
        "explanation": "② 약정 위반에 따른 유예 합의가 유효하려면, 대여자가 부여해 준 상환 유예 기간(결제 연기 기간)이 보고기간 종료일로부터 적어도 '12개월 이상'이어야만 회사가 결제를 12개월 이상 연기할 무조건적 권리를 쥔 것으로 보아 비유동부채로 분류합니다.\n\n[오답 해설]\n① 12개월 미만의 단기 유예는 기말에 여전히 유동부채입니다.\n③ 자본금 전입 대상이 아닙니다.\n④, ⑤는 법적/회계적 근거가 전혀 없는 소설적 오류입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "12개월 요건에 미달하는 유예기간은 유동화가 불가피합니다.", "articles": [], "principle": "유예기간 부여의 요건 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "연기 권리가 정당성을 인정받으려면 기말 기준 향후 최소 12개월 이상 상환 독촉을 미룰 수 있는 보증 기한이 서면에 반영되어야 합니다.", "articles": [], "principle": "유예기간 부여의 요건 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채를 임의 자본화할 수 없습니다.", "articles": [], "principle": "유예기간 부여의 요건 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "위반 및 유예 조건은 주석의 매우 중요한 공시 항목입니다.", "articles": [], "principle": "유예기간 부여의 요건 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자율 0% 강제 지침 등은 시장 약정과 상관없습니다.", "articles": [], "principle": "유예기간 부여의 요건 분석", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "다음 중 K-IFRS 상 유동자산/유동부채 및 비유동자산/비유동부채의 분류가 올바르게 작동하고 있는지 검증하기 위해, 회사가 보유한 계정과목 조합을 재무상태표 본문에 중간합계(Subtotals) 등으로 기재할 수 있는 정당한 사례에 해당하지 않는 것은?",
        "options": [
            "① 유동자산 총계에서 유동부채 총계를 차감한 '순운전자본(Net Working Capital)' 중간합계를 산출 표시하는 것",
            "② 금융자산 총액에서 충당부채를 직접 상계 소멸시킨 '순투자금융자산'을 임의로 단일 항목 기재하는 것",
            "③ 비유동자산 중 유형자산과 투자부동산을 합산하여 '부동산자산 소계' 중간합계를 내는 것",
            "④ 금융부채 중 차입 성격의 항목만 따로 묶어 '차입부채 합계' 소계를 적는 것",
            "⑤ 무형자산과 개발비를 합산한 '기술성무형자산 소계'를 표시하는 것"
        ],
        "answer": "2",
        "explanation": "② 자산과 부채의 직접적인 무단 상계(금융자산과 충당부채 상쇄)를 통해 순액 보고 항목을 본문 중간합계 등으로 위장하여 표기하는 것은 기준서의 상계 금지 규정을 정면 위반하므로 불허됩니다.\n\n[오답 해설]\n① 순운전자본, ③ 부동산자산 소계, ④ 차입부채 소계, ⑤ 무형자산 소계 등은 총액 정보를 훼손하지 않으면서 정보이용자의 이해를 돕기 위해 추가할 수 있는 합리적인 정당 중간합계 및 항목 추가 사례들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "순운전자본 합계는 건전성 파악에 유용하므로 기재가 허용됩니다.", "articles": [], "principle": "정당한 중간합계 추가 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "상계 금지를 어기는 상쇄 항목을 중간합계로 겉포장해 기재하는 2는 위반 처리 방식입니다.", "articles": [], "principle": "정당한 중간합계 추가 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 범주별 중간 소계 가산은 표시 유연성에 따라 보장됩니다.", "articles": [], "principle": "정당한 중간합계 추가 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 대과목 내의 유의적 중간 소계 적시는 참입니다.", "articles": [], "principle": "정당한 중간합계 추가 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무형자산 계열의 중간 합산 보고는 참입니다.", "articles": [], "principle": "정당한 중간합계 추가 판정", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "다음 중 K-IFRS 상 부채의 유동성 분류에 있어 '보고기간 말 이전에 약정을 위반'하였으나 채권자가 상환 청구를 유예(Grace period)해 주기로 합의했을 때, 이 유예기간이 '12개월 미만'인 경우(예: 6개월 유예 합의)의 분류 결과에 대한 설명으로 옳은 것은?",
        "options": [
            "① 합의가 기말 전에 성사되었으므로 예외 없이 비유동부채가 된다.",
            "② 기말 종료일 현재 12개월 이상 결제를 연기할 무조건의 권리가 확보되지 않은 상태이므로 여전히 '유동부채'로 분류하여야 한다.",
            "③ 전액 자본금으로 직접 전입 등기한다.",
            "④ 기말 차입금 원금을 장부에서 ₩0원으로 자동 제거한다.",
            "⑤ 회사의 대주주 지분율을 강제로 낮춘다."
        ],
        "answer": "2",
        "explanation": "② 약정 위반에 따른 채권자의 유예 약정이 있더라도 그 유예 기간이 기말 기준 12개월에 미달하는 단기(예: 6개월)라면, 보고기간 말 현재 1년 이상의 무조건적 연기권을 회사가 확보하지 못한 상태이므로 계속 유동부채로 보고해야 합니다.\n\n[오답 해설]\n① 12개월 요건 충족이 필수이므로 오답입니다.\n③ 자본금 강제 전입 규정은 없습니다.\n④, ⑤는 회계 원리와 관련이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "합의 시기가 기말 전이라도 연기 기간 요건(12개월)에 미달하면 비유동이 될 수 없습니다.", "articles": [], "principle": "단기 유예기간 합의 부채", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "12개월 이상의 무조건적 결제 연기권 획득 요건을 불충족하므로, 기말에 유동부채로 계상하여야 합니다.", "articles": [], "principle": "단기 유예기간 합의 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적인 자본 전입은 불가합니다.", "articles": [], "principle": "단기 유예기간 합의 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채무 소멸 회계처리는 불법입니다.", "articles": [], "principle": "단기 유예기간 합의 부채", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주주 지분 변동과 관계없습니다.", "articles": [], "principle": "단기 유예기간 합의 부채", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },

    # =========================================================================
    # L5: 심화 (2문항, 599~600번)
    # =========================================================================
    {
        "id": "practice-accounting-ch02s02-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "(주)평가는 20X1년말 현재 다음과 같은 3개의 은행 차입금 계약을 보유하고 있다. K-IFRS 제1001호에 의거해 20X1년말 재무상태표에 기재되는 '비유동부채'의 합계액은 얼마인가?\n\n```\n• 차입금 A (₩30,000,000): 20X1년 10월에 재무 약정을 위반하여 은행이 즉시 전액 상환 청구권을 가졌으나, 20X1년 12월 25일에 은행이 18개월간 상환 독촉을 청구하지 않기로 공식 유예 서면 합의해 주었다.\n• 차입금 B (₩40,000,000): 20X1년 11월에 재무 약정을 위반하여 은행이 즉시 상환 청구권을 가졌으며, 기말 현재까지 아무런 합의서 작성이 없다가 기말이 지난 20X2년 1월 12일(재무제표 승인일은 2월 20일)에 은행이 2년간 상환을 요구하지 않기로 유예 합의해 주었다.\n• 차입금 C (₩50,000,000): 만기가 20X2년 11월 30일(11개월 뒤)에 도래하는 단기 차입금이나, 기존 대출 약정 상 추가적 동의 없이 만기를 3년 더 연장할 수 있는 무조건적 차환 재량권을 기말 현재 독점 보유하고 있으며 연장할 계획이다.\n```",
        "options": [
            "  ① ₩30,000,000",
            "  ② ₩50,000,000",
            "  ③ ₩80,000,000",
            "  ④ ₩90,000,000",
            "  ⑤ ₩120,000,000"
        ],
        "answer": "3",
        "explanation": "③ 부채별 세부 분류 분석:\n- 차입금 A: 20X1년말 이전에 18개월(12개월 이상) 공식 유예 합의가 성사되어 연기 권리가 회복되었으므로 '비유동부채' 분류 (₩30,000,000).\n- 차입금 B: 기말 종료일 현재는 즉시 상환 요구 대상(연기 권리 상실 상태)이었으며 기말 이후에야 합의가 서명되었으므로, 기말에는 '유동부채'로 보고하여야 합니다. (비유동 ₩0).\n- 차입금 C: 만기는 11개월 뒤이지만 만기를 추가 동의 없이 연장할 무조건적 계약 상 재량권을 기말 현재 보유하고 있으므로 '비유동부채' 분류 (₩50,000,000).\n따라서 비유동부채 합계액 = 차입금 A ₩30,000,000 + 차입금 C ₩50,000,000 = ₩80,000,000 입니다.\n\n[오답 해설]\n① 차입금 A만 가산한 오산출액입니다.\n② 차입금 C만 가산한 오산출액입니다.\n④ 차입금 B를 비유동으로 잘못 판단한 합산액입니다.\n⑤ 전체 부채를 비유동으로 잘못 판정한 합산액입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "차입금 C(₩50,000,000)도 비유동부채에 해당하므로 합계가 누락되어 오답입니다.", "articles": [], "principle": "심화 부채분류 및 비유동총량 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입금 A(₩30,000,000)도 비유동부채에 해당하여 누락으로 오답입니다.", "articles": [], "principle": "심화 부채분류 및 비유동총량 산정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "차입금 A(₩30,000,000)와 C(₩50,000,000)가 비유동부채가 되어 합계 ₩80,000,000이 정답입니다.", "articles": [], "principle": "심화 부채분류 및 비유동총량 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입금 B를 비유동으로 섞은 잘못된 계산 결과입니다.", "articles": [], "principle": "심화 부채분류 및 비유동총량 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전체 채무를 비유동화하여 오판정한 수치입니다.", "articles": [], "principle": "심화 부채분류 및 비유동총량 산정", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
            }
        }
    },
    {
        "id": "practice-accounting-ch02s02-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "(주)평가는 기말 재무상태표에 기중의 장기차입약정 위반 사실에 따른 대여 은행의 즉시 상환독촉권 행사가 가능해진 차입금 ₩50,000,000을, 기말 현재 연기할 무조건적 권리가 전혀 없음에도 불구하고 비유동부채로 허위 분류하여 최초 보고하였다. 이 보고서 상의 원래 유동비율(Current Ratio)은 150%(유동자산 ₩150,000,000 / 유동부채 ₩100,000,000)였다. 이후 회계감사 시 감사인에 의해 이 오류가 적발되어 해당 차입금 ₩50,000,000을 즉시 '유동부채'로 강제 올바르게 재분류 수정 분개하여 반영하였다. 이 수정 분개 반영 후의 '수정유동비율'의 변동 크기 및 순운전자본(Net Working Capital = 유동자산 - 유동부채)의 영향 분석 조합으로 가장 올바른 것은?",
        "options": [
            "① 유동비율: 100%로 50%p 하락 / 순운전자본: ₩50,000,000 감소",
            "② 유동비율: 100%로 50%p 하락 / 순운전자본: 변동 없음(₩0)",
            "③ 유동비율: 150%로 변동 없음 / 순운전자본: ₩50,000,000 감소",
            "④ 유동비율: 200%로 50%p 상승 / 순운전자본: ₩50,000,000 증가",
            "⑤ 유동비율: 75%로 75%p 하락 / 순운전자본: 변동 없음(₩0)"
        ],
        "answer": "1",
        "explanation": "① 정밀 재무비율 영향 분석:\n1. 수정 전 상태:\n   - 유동자산 = ₩150,000,000\n   - 유동부채 = ₩100,000,000\n   - 유동비율 = 150%\n   - 순운전자본 = ₩150,000,000 - ₩100,000,000 = ₩50,000,000\n\n2. 오류 수정 분개 반영 후 (비유동부채 ₩50,000,000 $\\rightarrow$ 유동부채로 이동):\n   - 유동자산 = ₩150,000,000 (변동 없음)\n   - 유동부채 = ₩100,000,000 + ₩50,000,000 = ₩150,000,000\n   - 수정 유동비율 = ₩150,000,000 / ₩150,000,000 = 100%\n     (즉, 유동비율은 150%에서 100%로 50%포인트(p) 급락하여 단기 건전성 평가 지표가 대폭 악화됩니다.)\n   - 수정 순운전자본 = ₩150,000,000 - ₩150,000,000 = ₩0\n     (즉, 원래 ₩50,000,000이었던 순운전자본이 ₩0원으로 ₩50,000,000만큼 직접 감소합니다.)\n따라서 올바른 조합은 유동비율 100%로 50%p 하락 / 순운전자본 ₩50,000,000 감소 입니다.\n\n[오답 해설]\n② 순운전자본은 분모/분자 비율이 아니며 절대액 차이이므로 유동부채 증가액만큼 고스란히 ₩50,000,000 감소하므로 변동 없음 서술은 오류입니다.\n③, ④, ⑤는 비율 및 순운전자본 변동을 잘못 연동시킨 오류 해석들입니다.",
        "question_type": "사례5지",
        "option_meta": [
            {"correct": True, "why": "유동부채가 ₩150,000,000으로 늘어나 유동비율은 100%(50%p 하락)가 되고, 순운전자본은 ₩0원(₩50,000,000 감소)이 되므로 1이 정확합니다.", "articles": [], "principle": "유동성 분류가 건전성 지표에 주는 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동부채 증가로 순운전자본 절대액이 ₩50,000,000만큼 차감 감소하므로 변동 없다는 설명은 오답입니다.", "articles": [], "principle": "유동성 분류가 건전성 지표에 주는 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동비율 분모가 늘어났으므로 비율은 변동이 없는 것이 아니라 급락합니다.", "articles": [], "principle": "유동성 분류가 건전성 지표에 주는 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비율이 올라가거나 순운전자본이 늘어나는 계산 방향과 정반대입니다.", "articles": [], "principle": "유동성 분류가 건전성 지표에 주는 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수정 비율이 75%가 아니며 순운전자본도 변동합니다.", "articles": [], "principle": "유동성 분류가 건전성 지표에 주는 영향", "case": {"holding": "", "no": None}}
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
                "item": "2절 재무상태표"
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
