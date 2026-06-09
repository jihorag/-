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
        "id": "practice-accounting-ch01s07-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "개념체계 상 '인식(Recognition)'의 정의에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 거래처와 체결한 미이행계약의 세부 조항을 정기적으로 감사인에게 이메일로 전송하는 보고 절차이다.",
            "② 자산, 부채, 자본, 수익, 비용 등 재무제표 요소 중 하나의 정의를 충족하는 항목을 재무상태표나 재무성과표에 포함하기 위하여 포착하는 과정이다.",
            "③ 기업의 내부 영업권 가치를 임의로 추정하여 매월 재무제표 본문에 가산하는 기재 방식을 뜻한다.",
            "④ 재무상태표에 표시된 자산의 시장 가격 변동액을 실시간으로 추적하여 전산망에 기록하는 내부통제 프로세스이다.",
            "⑤ 회계장부에 잘못 기재된 과거 오류를 소급하여 수정하는 회계처리를 지칭한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계상 인식은 재무제표 요소 중 하나의 정의를 충족하는 항목을 재무상태표나 재무성과표에 포함하기 위하여 포착(capturing)하는 과정으로 정의됩니다.\n\n[오답 해설]\n① 미이행계약의 보고 절차에 대한 설명이 아닙니다.\n③ 내부적으로 창출된 영업권은 자산 정의를 충족하지 못해 인식 대상이 아닙니다.\n④ 시가 변동의 단순 기록을 뜻하지 않고, 재무제표 본문(합계)에 포착·포함시키는 과정입니다.\n⑤ 이는 오류 수정에 해당하며 인식의 정의가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "감사인에게 이메일 전송하는 절차는 인식이 아닙니다.", "articles": [], "principle": "인식의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "인식은 재무제표 요소 정의를 충족하는 항목을 재무제표에 포함하기 위해 포착하는 과정입니다.", "articles": [], "principle": "인식의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "내부 영업권은 인식이 허용되지 않으며 자의적 가산과도 무관합니다.", "articles": [], "principle": "인식의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가 변동 실시간 추적 프로세스는 인식의 정의가 아닙니다.", "articles": [], "principle": "인식의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소급 수정 회계처리는 오류수정입니다.", "articles": [], "principle": "인식의 정의", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "개념체계 상 '제거(Derecognition)'의 정의로 가장 올바른 것은?",
        "options": [
            "① 거래처의 파산으로 매출채권을 대손 처리하였으나 추후 전액 회수한 회계 분개이다.",
            "② 기업의 재무상태표에서 인식된 자산이나 부채의 전부 또는 일부를 삭제하는 것이다.",
            "③ 보고기간 말에 영업 외 비용을 매출원가 계정으로 대체하여 당기순손익을 인위적으로 조정하는 거래이다.",
            "④ 주주총회 결의를 통해 이익잉여금의 일부를 배당금으로 최종 확정하고 재무상태표에서 차감하는 절차이다.",
            "⑤ 세법 개정으로 법인세 납부 의무가 면제되었을 때 세금을 환급받는 과정이다."
        ],
        "answer": "2",
        "explanation": "② 개념체계상 제거(Derecognition)란 기업의 재무상태표에서 인식된 자산이나 부채의 전부 또는 일부를 삭제하는 것을 말합니다.\n\n[오답 해설]\n① 대손처리된 채권의 추후 회수 분개는 단순 채권 회수 분개로 제거 자체가 아닙니다.\n③ 손익계산서 계정 대체는 제거의 회계적 정의가 아닙니다.\n④ 배당금 배정 처리는 주주 자본 거래 분개일 뿐 제거의 정의가 아닙니다.\n⑤ 세금 환급은 자산 유입의 예시로 제거의 정의와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "채권 추후 회수 거래는 제거의 정의가 아닙니다.", "articles": [], "principle": "제거의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "제거는 인식된 자산이나 부채의 전부 또는 일부를 재무상태표에서 삭제하는 것입니다.", "articles": [], "principle": "제거의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계정 대체 거래는 제거의 정의가 아닙니다.", "articles": [], "principle": "제거의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "배당금 자본 거래는 제거의 개념 정의와 다릅니다.", "articles": [], "principle": "제거의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세금 환급은 자산 취득/유입이며 제거의 정의가 아닙니다.", "articles": [], "principle": "제거의 정의", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "개념체계 상 재무제표 요소(자산, 부채 등)의 정의를 충족하는 항목의 인식 여부에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 요소의 정의를 충족하는 항목은 재무제표 본문에 무조건 인식되어야 하며 예외는 없다.",
            "② 요소의 정의를 충족하더라도 항상 인식되는 것은 아니며, 특정 조건(목적적합성, 표현충실성, 원가제약)을 고려하여 인식 여부를 결정한다.",
            "③ 정의를 충족하는 항목은 기업의 자의적 판단에 따라 인식을 배제할 수 있는 권한이 법적으로 부여된다.",
            "④ 요소의 정의를 충족하지 못하는 항목이라도 정보이용자의 요청이 있다면 얼마든지 재무상태표에 인식할 수 있다.",
            "⑤ 정의를 충족하는 모든 부채는 당해 연도 세법 규정에 부합할 때만 인식의 대상이 된다."
        ],
        "answer": "2",
        "explanation": "② 개념체계상 자산, 부채 또는 자본의 정의를 충족하는 항목만이 재무상태표에 인식됩니다. 그러나 정의를 충족하는 항목이라고 할지라도 항상 인식되는 것은 아닙니다. 목적적합한 정보와 충실한 표현을 제공하고 원가제약을 충족할 때 인식합니다.\n\n[오답 해설]\n① 무조건 인식하는 것은 아닙니다. 질적 특성과 제약 요인을 고려해야 합니다.\n③ 기업의 자의적 권한이 아니라 개념체계가 정한 인식기준에 따릅니다.\n④ 개념체계는 정의를 충족하지 않는 항목의 인식을 명시적으로 금지(허용하지 않음)합니다.\n⑤ 회계기준은 세법 규정에 종속되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "정의를 충족해도 목적적합성이나 표현충실성, 원가제약에 따라 인식하지 않을 수 있습니다.", "articles": [], "principle": "인식기준", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "요소 정의를 충족하는 항목이라도 목적적합성과 표현충실성을 고려하여 유용한 경우에만 인식합니다.", "articles": [], "principle": "인식기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적 판단이 아니라 회계 이론적 기준에 의해 결정됩니다.", "articles": [], "principle": "인식기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정의를 충족하지 않는 항목은 어떠한 경우에도 인식할 수 없습니다.", "articles": [], "principle": "인식기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인식기준은 세법 적용 여부와 직접적인 인과관계가 없습니다.", "articles": [], "principle": "인식기준", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "개념체계 상 자산의 제거(Derecognition)가 일어나는 일반적인 요건으로 가장 올바른 것은?",
        "options": [
            "① 자산의 시장 가격이 취득원가보다 낮아져서 역사적 원가가 훼손되었을 때",
            "② 기업이 인식한 자산의 전부 또는 일부에 대한 통제를 상실하였을 때",
            "③ 자산을 취득한 날로부터 1년 이상의 시간이 경과하여 비유동자산으로 변동되었을 때",
            "④ 정부 세무관서가 해당 자산에 대한 감가상각 한도액을 공식적으로 제한하였을 때",
            "⑤ 회사의 대표이사가 자산을 매각하기로 이사회에서 구두로 다짐하였을 때"
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 기업은 일반적으로 자신이 인식한 자산의 전부 또는 일부에 대한 '통제를 상실'하였을 때 해당 자산을 제거합니다.\n\n[오답 해설]\n① 평가손실 발생이나 시장가치 하락 시에는 감액이나 평가 손실을 인식할 뿐 자산을 완전히 장부에서 삭제(제거)하지는 않습니다.\n③ 시간 경과는 제거 요건이 아닙니다.\n④ 세무 감가상각 한도는 회계 제거와 무관합니다.\n⑤ 단순 이사회의 구두 다짐이나 매각 계획만으로는 통제 상실이 일어나지 않으므로 제거할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "시가 변동에 의한 감액 등은 제거가 아니라 자산의 평가/측정 변동입니다.", "articles": [], "principle": "자산 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산은 기업이 그 자산에 대한 통제를 상실하였을 때 재무상태표에서 제거합니다.", "articles": [], "principle": "자산 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유동구분의 변경은 제거가 아닙니다.", "articles": [], "principle": "자산 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 규정이나 상각 한도는 재무제표 제거의 기준이 아닙니다.", "articles": [], "principle": "자산 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실제 거래가 이루어져 통제가 이전되기 전의 내부 계획만으로는 자산을 제거할 수 없습니다.", "articles": [], "principle": "자산 제거 요건", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "개념체계 상 부채의 제거(Derecognition)가 일어나는 일반적인 상황으로 가장 올바른 것은?",
        "options": [
            "① 부채의 시장 이자율이 급격히 상승하여 미래 상환액의 현재가치가 대폭 감소하였을 때",
            "② 기업이 인식한 부채의 전부 또는 일부에 대한 현재의무를 더 이상 부담하지 않을 때",
            "③ 채권자가 채무를 독촉하는 우편물을 3회 이상 연속하여 발송하지 않았을 때",
            "④ 기업이 상환 여력이 충분하다는 사실을 신용평가사를 통해 공식 공표하였을 때",
            "⑤ 회사의 재무부서장이 단기차입금의 만기를 임의로 연장해달라는 내용의 메일을 거래은행에 송신하였을 때"
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 기업은 일반적으로 자신이 인식한 부채의 전부 또는 일부에 대한 '현재의무를 더 이상 부담하지 않을 때'에 부채를 제거합니다.\n\n[오답 해설]\n① 이자율 상승에 의한 현재가치 변동은 제거 사유가 아니라 공정가치 평가 변동(인식되는 경우)에 불과합니다.\n③ 단순 독촉이 없다는 사실은 법적/실질적 의무 소멸이 아니므로 부채를 제거할 수 없습니다.\n④ 기업의 신용도나 상환 여력 공표는 의무의 존재 여부와 무관합니다.\n⑤ 만기 연장 요청 메일 송신만으로는 의무가 소멸하지 않으며 실제 만기 연장 합의가 서면 등으로 확정되더라도 의무 자체는 제거되지 않고 유지됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "이자율 변동으로 인한 현가 변화는 부채의 제거가 아닙니다.", "articles": [], "principle": "부채 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부채는 현재의무가 이행, 취소, 만료 등의 사유로 더 이상 부담되지 않을 때 제거합니다.", "articles": [], "principle": "부채 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "독촉 우편물 미송신은 현재의무를 소멸시키지 못합니다.", "articles": [], "principle": "부채 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자체 상환 여력 공표는 부채의 제거와 무관합니다.", "articles": [], "principle": "부채 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "만기 연장 요청 메일만으로는 현재 의무가 없어지지 않습니다.", "articles": [], "principle": "부채 제거 요건", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "개념체계 상 재무보고 제약요인 중 '인식(Recognition)' 결정에도 직접적인 제약을 미치는 공통 제약요인은?",
        "options": [
            "① 역사적 원가주의(Historical Cost Constraint)",
            "② 보수주의(Prudence)",
            "③ 원가제약(Cost Constraint)",
            "④ 복식부기(Double-entry bookkeeping)",
            "⑤ 세법적합성(Tax alignment)"
        ],
        "answer": "3",
        "explanation": "③ 개념체계 상 원가(Cost)는 다른 재무보고 결정들과 마찬가지로 인식에 대한 결정도 제약합니다. 자산이나 부채를 인식할 때 정보 작성자와 이용자가 부담하는 원가보다 이로 인한 정보의 효익이 정당화될 때에만 인식합니다.\n\n[오답 해설]\n① 역사적 원가주의는 측정 기준 중 하나일 뿐 질적 특성에 대한 제약 요인이 아닙니다.\n② 보수주의(Prudence)는 충실한 표현의 일부로서 신중성을 가리킬 뿐 인식 결정의 공통 제약요인이 아닙니다.\n④ 복식부기는 장부기록 기술이며 인식의 결정 제약 원칙이 아닙니다.\n⑤ 세법적합성은 회계 개념체계의 재무보고 제약요인이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "역사적 원가는 측정 기준의 한 예일 뿐입니다.", "articles": [], "principle": "인식 제약요인", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "신중성(보수주의)은 질적 특성의 신중한 판단 지침이지 인식을 전반적으로 제약하는 요인이 아닙니다.", "articles": [], "principle": "인식 제약요인", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "원가는 인식 결정도 제약하며, 제공되는 정보의 효익이 원가를 정당화할 때 인식해야 합니다.", "articles": [], "principle": "인식 제약요인", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "복식부기는 기록 기법입니다.", "articles": [], "principle": "인식 제약요인", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법적합성은 재무보고 개념체계 상 제약요인이 아닙니다.", "articles": [], "principle": "인식 제약요인", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "개념체계 상 '인식'이라는 구체적인 포착 과정에 결합되어 수반되는 절차로 가장 거리가 먼 것은?",
        "options": [
            "① 대상 항목의 성격에 맞는 명칭을 서술적으로 표기하기",
            "② 해당 항목의 화폐금액 결정(측정)하기",
            "③ 결정된 화폐금액을 재무상태표나 재무성과표의 합계에 포함하기",
            "④ 주석에 그 항목의 배경과 세부 내역을 설명하는 정보 공시하기",
            "⑤ 회사의 경쟁 우위 확보를 위한 마케팅 홍보 시안 승인하기"
        ],
        "answer": "5",
        "explanation": "⑤ 마케팅 홍보 시안 승인은 회사 경영진의 일반적인 영업 관리 활동일 뿐, 재무보고 목적의 회계 인식 포착 절차와 무관합니다.\n\n[오답 해설]\n①, ②, ③, ④는 모두 재무보고서 내에 자산이나 부채를 정식으로 인식하고 포착할 때 동반되는 정상적 회계 절차 및 후속 설명 공시 과정에 속합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "명칭 서술은 인식의 일환입니다.", "articles": [], "principle": "인식의 포착 과정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정(금액화)은 인식을 위해 반드시 수반됩니다.", "articles": [], "principle": "인식의 포착 과정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금액을 총계에 포함하는 것은 인식의 본질적 과정입니다.", "articles": [], "principle": "인식의 포착 과정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석 설명 정보 제공도 인식 및 그와 연동된 후속 절차에 포함됩니다.", "articles": [], "principle": "인식의 포착 과정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "마케팅 시안 승인은 경영 의사결정으로 회계 상 포착 과정에 들어가지 않습니다.", "articles": [], "principle": "인식의 포착 과정", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "개념체계 상 재무제표 요소(자산, 부채, 자본, 수익, 비용)의 정의를 충족하지 못하는 항목의 처리에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 정의를 충족하지 못하더라도 원가제약을 충족한다면 재무제표 본문에 자산이나 부채로 인식할 수 있다.",
            "② 정의를 충족하지 못하면 목적적합한 정보 제공에 도움이 되더라도 재무상태표나 재무성과표에 인식할 수 없다.",
            "③ 정의를 충족하지 못하는 항목은 주석으로도 공시해서는 안 되며, 외부 보고 시 완전히 은폐해야 한다.",
            "④ 정의를 충족하지 못하는 항목을 재무제표 본문에 기재한 후, 감사인에게 확인 도장만 받으면 합법적 인식이 된다.",
            "⑤ 정의를 충족하지 못하면 무조건 자본계정에 직접 가산하여 '미분류자본잉여금'으로 표시한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 자산, 부채, 자본, 수익, 비용 등의 요소 정의를 충족하지 못하는 항목의 재무상태표나 재무성과표 상 인식을 전혀 허용하지 않습니다.\n\n[오답 해설]\n① 정의를 충족하지 못하면 원가제약과 관계없이 본문에 인식할 수 없습니다.\n③ 정의를 충족하지 않아 본문에 인식할 수 없더라도, 유용한 정보라면 주석(설명 정보)을 통해 기재하거나 공시할 수 있으며 은폐해서는 안 됩니다.\n④ 외부 감사의 확인이 있더라도 요소 정의를 만족하지 않으면 인식이 허용되지 않습니다.\n⑤ 자본은 자산에서 부채를 차감한 잔여지분이므로 마음대로 기타 항목을 직접 인식하여 자본에 넣을 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "정의 미충족 항목은 원가제약 충족 여부와 상관없이 본문에 인식될 수 없습니다.", "articles": [], "principle": "정의 미충족 항목의 처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "개념체계는 정의를 충족하지 않는 항목의 인식을 허용하지 않습니다.", "articles": [], "principle": "정의 미충족 항목의 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "본문 인식은 불가능하지만, 정보 이용에 필요한 사항은 주석으로 공시 가능하며 오히려 권장됩니다.", "articles": [], "principle": "정의 미충족 항목의 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사인의 승인이 있더라도 개념체계 상 인식이 될 수 없습니다.", "articles": [], "principle": "정의 미충족 항목의 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의로 자본계정에 직접 배정하여 기재하는 처리는 불가합니다.", "articles": [], "principle": "정의 미충족 항목의 처리", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "개념체계 상 재무상태표에서 인식된 자산이나 부채가 제거(Derecognition)되는 일반적인 계기(Trigger)로 가장 옳은 것은?",
        "options": [
            "① 해당 항목이 더 이상 자산 또는 부채의 정의를 충족하지 못하게 되었을 때",
            "② 결산기가 도래하여 새로운 연도의 장부를 이월 개설할 때",
            "③ 주주들이 회사의 상호를 변경하고 사업 목적을 등기부등본에 추가 기재하였일 때",
            "④ 정부 공무원들이 해당 기업의 공장 설비에 대한 안전 검사를 실시하였을 때",
            "⑤ 회사의 주가가 주식시장에서 비정상적인 등락을 보이며 거래가 일시 정지되었을 때"
        ],
        "answer": "1",
        "explanation": "① 제거는 일반적으로 인식된 자산이나 부채가 더 이상 자산 또는 부채의 정의를 충족하지 못할 때 발생합니다. (예: 자산의 경우 통제 상실, 부채의 경우 의무 소멸)\n\n[오답 해설]\n② 장부 이월 시에는 잔액이 계속 이월되며 제거되지 않습니다.\n③ 상호 변경 및 등기 등록은 부채나 자산의 제거 계기가 아닙니다.\n④ 공장 안전 검사는 자산/부채 정의 충족 여부와 무관합니다.\n⑤ 주가 등락 및 거래 정지는 제거와 상관없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "제거는 인식된 항목이 더 이상 자산/부채 정의를 충족하지 못할 때 수반됩니다.", "articles": [], "principle": "제거 시점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "새해 장부 이월 시 자산/부채 잔액은 그대로 승계되며 제거가 아닙니다.", "articles": [], "principle": "제거 시점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회사 상호 변경은 제거 계기가 아닙니다.", "articles": [], "principle": "제거 시점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공장 검사는 제거 계기가 될 수 없습니다.", "articles": [], "principle": "제거 시점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주가 흐름은 자산/부채 제거와 직접적인 상관이 없습니다.", "articles": [], "principle": "제거 시점", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "개념체계 상 재무제표의 인식(Recognition)과 측정(Measurement)의 논리적 상관관계에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 인식을 위해 항목을 포착하는 과정에서는 반드시 화폐 금액을 결정하는 측정이 요구된다.",
            "② 측정을 완벽하게 끝낸 자산만이 인식을 시도할 수 있으며, 추정치를 이용한 측정은 인식에 절대 활용될 수 없다.",
            "③ 인식과 측정은 서로 완전히 분리되어 있어, 재무제표 본문에 금액이 표시되지 않아도 서술만 기재되면 인식이 완료된 것으로 본다.",
            "④ 측정 기준이 역사적 원가인 자산만 인식이 가능하며, 현행원가나 공정가치로 측정되는 자산은 인식이 원천 금지된다.",
            "⑤ 측정이 불가능하여 장부에 0원으로 인식한 경우라도 자산의 인식은 원칙적으로 불가능하다."
        ],
        "answer": "1",
        "explanation": "① 개념체계상 자산이나 부채를 인식하기 위해서는 이를 화폐단위로 수량화해야 하므로, 측정기준을 선택하여 화폐금액을 결정하는 측정이 필수적으로 수반됩니다.\n\n[오답 해설]\n② 추정치를 사용하는 합리적인 측정도 회계의 필수 부분이며 인식을 가능하게 만듭니다.\n③ 화폐금액으로 재무제표의 합계에 포함하는 것이 인식이므로, 금액 없이 단순 기술만 하는 주석 공시를 인식이라 칭하지 않습니다.\n④ 역사적 원가 외에 공정가치, 현행원가, 사용가치 등 다양한 측정기준이 인식에 사용될 수 있습니다.\n⑤ 측정이 전혀 불가능하다면 본문에 인식할 수 없습니다. (다만 추정이 가능한 불확실성 범위 내에서 측정이 수행됩니다.)",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "자산이나 부채를 인식하기 위해서는 측정기준에 맞춰 화폐금액을 결정하는 측정이 수반됩니다.", "articles": [], "principle": "인식과 측정의 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추정을 통한 측정도 인식을 가능하게 하는 핵심 도구입니다.", "articles": [], "principle": "인식과 측정의 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재무제표 본문 금액 표시 및 합계 산입이 인식의 필수 요소입니다.", "articles": [], "principle": "인식과 측정의 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치나 사용가치 등도 인식 시 사용되는 유효한 측정 기준입니다.", "articles": [], "principle": "인식과 측정의 관계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정이 전혀 불가능한 경우 인식이 불가한 것은 맞으나 지문 5의 논리는 0원으로 강제 인식한다는 전제가 모순됩니다.", "articles": [], "principle": "인식과 측정의 관계", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },

    # =========================================================================
    # L2: 이해 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s07-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "개념체계 상 특정 자산이나 부채의 정의를 충족하더라도 이를 본문에 인식하는 것이 목적적합하지 않은 정보 제공으로 이어질 수 있는 구체적인 원인에 해당하는 것은?",
        "options": [
            "① 해당 자산이 물리적 형태가 없는 무형자산인 경우",
            "② 해당 부채에 적용할 이자율이 시장에서 매일 변동하는 경우",
            "③ 자산이나 부채가 존재하는지 여부가 불확실하거나, 경제적효익의 유입·유출 가능성이 낮은 경우",
            "④ 자산의 법적 소유권이 확실하여 분쟁의 여지가 전혀 없는 경우",
            "⑤ 회사가 자산의 취득 가액을 세무서에 완벽히 보고하여 조세 마찰의 위험이 없는 경우"
        ],
        "answer": "3",
        "explanation": "③ 개념체계 상 특정 자산이나 부채의 정의를 충족하더라도, (1) 존재의 불확실성이 있거나 (2) 경제적효익의 유입·유출 가능성이 매우 낮은 경우에는 인식을 함으로써 오히려 정보이용자에게 목적적합하지 않은 정보가 전달될 우려가 있습니다.\n\n[오답 해설]\n① 물리적 형태 여부는 무형자산의 인식기준(식별가능성 등) 충족 시 인식에 방해가 되지 않습니다.\n② 이자율 매일 변동은 인식 가능 여부와 상관없습니다.\n④ 소유권 분쟁이 없다면 오히려 인식을 보조하는 긍정적 요인입니다.\n⑤ 조세 마찰 유무는 회계 인식의 목적적합성 판단 요건이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "형태 유무 자체는 인식이 부적절해지는 직접적 원인이 아닙니다.", "articles": [], "principle": "목적적합성과 인식의 상충", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자율 변동성은 인식을 불가능하게 하는 조건이 아닙니다.", "articles": [], "principle": "목적적합성과 인식의 상충", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "존재 불확실성이나 낮은 유입/유출가능성이 있다면 인식을 안 하는 것이 더 목적적합한 정보 제공일 수 있습니다.", "articles": [], "principle": "목적적합성과 인식의 상충", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소유권 확정은 인식을 지지하는 안전한 요인입니다.", "articles": [], "principle": "목적적합성과 인식의 상충", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 조세 행정 요인은 회계학적 인식 목적적합성과 무관합니다.", "articles": [], "principle": "목적적합성과 인식의 상충", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "개념체계 상 '존재의 불확실성(Existence Uncertainty)'에 대한 회계적 처리 및 설명으로 가장 올바른 것은?",
        "options": [
            "① 자산이나 부채가 존재하는지 불확실하더라도, 정의만 충족하면 무조건 현금수지표 본문에 금액을 반영하여 표기해야 한다.",
            "② 존재의 불확실성이 있고 경제적효익의 낮은 유입·유출가능성 등과 결합되어 있다면, 단일 금액으로만 측정하여 본문에 인식하는 것이 목적적합한 정보를 제공하지 못할 수 있다.",
            "③ 소송 등 존재의 불확실성이 발생하면 기업은 해당 연도의 모든 재무제표 작성을 판결이 확정될 때까지 중단해야 한다.",
            "④ 존재의 불확실성이 있는 항목은 어떠한 경우에도 주석 공시의 대상에서 영구 제외되어야 한다.",
            "⑤ 존재의 불확실성이 해소되는 즉시 과거의 모든 재무상태표를 매 보고기간마다 소급하여 당초부터 자산이 있었던 것처럼 재작성한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 자산·부채의 존재 여부가 불확실한 경우, 발생가능한 결과의 범위가 넓고 낮은 효익 유입/유출가능성과 결합되면 이를 단일 금액으로 억지 측정하여 재무상태표 본문에 인식하는 것이 불합리(목적적합하지 않음)할 수 있습니다.\n\n[오답 해설]\n① 무조건 본문에 인식해야 하는 것은 아닙니다.\n③ 불확실성이 있다고 재무제표 작성 자체를 중단해서는 안 됩니다.\n④ 본문에 인식하지 않더라도 주석으로 해당 상황에 관한 설명정보(우발 상황 등)를 공시해야 합니다.\n⑤ 불확실성 해소 시 당기나 미래에 전진적으로 인식하며, 과거 재무상태표를 소급 재작성하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "정의를 충족해도 존재 불확실성으로 인해 본문 인식이 배제될 수 있습니다.", "articles": [], "principle": "존재의 불확실성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "존재 불확실성이 극심하면 단일 측정치로 본문에 인식하기보다 미인식하고 주석 공시를 하는 것이 유용합니다.", "articles": [], "principle": "존재의 불확실성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계 기간 보고는 정해진 시점에 계속 작성되어야 합니다.", "articles": [], "principle": "존재의 불확실성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "본문 미인식 시에도 주석을 통한 설명은 매우 중요하므로 제외 대상이 아닙니다.", "articles": [], "principle": "존재의 불확실성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산의 신규 발생이나 상태 변화에 따른 회계처리는 소급 오류수정 대상이 아닙니다.", "articles": [], "principle": "존재의 불확실성", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "개념체계 상 '경제적효익의 유입가능성이나 유출가능성이 매우 낮은 자원이나 의무'에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 유입 또는 유출가능성이 매우 낮다면 개념체계상 자산이나 부채의 정의 자체가 성립되지 않는다.",
            "② 유입 또는 유출가능성이 매우 낮더라도 자산이나 부채의 정의를 충족하고 존재할 수 있다.",
            "③ 가능성이 극히 낮은 거래는 어떠한 계약적 권리나 법률적 효과도 전혀 창출하지 못한다.",
            "④ 가능성이 낮은 권리는 금융자산으로만 한정하여 매월 법정 시장 가격으로 무조건 인식한다.",
            "⑤ 유출가능성이 매우 낮은 의무는 항상 전액 부채로 본문에 먼저 기재한 후, 기말에 영업 외 수익으로 대체한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 경제적효익의 유입가능성이나 유출가능성이 낮더라도 자산이나 부채가 존재할 수 있음을 명시하고 있습니다. (즉, 유입/유출가능성의 고저는 자산·부채 정의 충족의 절대적 허들이 아닙니다.)\n\n[오답 해설]\n① 자산의 잠재력 요건이나 부채의 이전잠재력은 확신이나 높은 가능성을 요구하지 않으므로 정의 충족이 가능합니다.\n③ 계약을 통해 권리가 이미 성립했으므로 가능성이 낮아도 법적 권리 등은 존재합니다.\n④ 금융자산으로 자동 한정하여 시가로 본문 인식해야 한다는 규칙은 없습니다.\n⑤ 유출가능성이 낮으면 부채로 인식하지 않는 것이 일반적이며, 먼저 인식했다가 대체한다는 회계 처리는 근거가 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "유입가능성이 낮아도 자산의 정의(효익을 창출할 잠재력을 지닌 권리)를 충족할 수 있습니다.", "articles": [], "principle": "유입/유출가능성과 정의의 성립", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "경제적효익의 유입/유출가능성이 낮더라도 자산이나 부채는 존재(정의 충족)할 수 있습니다.", "articles": [], "principle": "유입/유출가능성과 정의의 성립", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계약으로 보증된 권리 등이 엄연히 창출되므로 왜곡된 기술입니다.", "articles": [], "principle": "유입/유출가능성과 정의의 성립", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자동으로 시가 인식된다는 설명은 개념체계에 맞지 않습니다.", "articles": [], "principle": "유입/유출가능성과 정의의 성립", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유출가능성이 낮은 의무를 본문에 부채로 강제 선계상하는 규정은 전혀 없습니다.", "articles": [], "principle": "유입/유출가능성과 정의의 성립", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "개념체계 상 경제적효익의 유입가능성이나 유출가능성이 낮은 자산이나 부채에 대하여, 재무제표 이용자에게 가장 목적적합한 정보를 전달하기 위한 주된 공시 방식은?",
        "options": [
            "① 재무상태표 본문에 정식 자산/부채 금액으로 계상하되 비고란에 '낮은 확률'이라고 표기한다.",
            "② 발생가능한 유입이나 유출의 크기, 발생가능한 시기 및 발생가능성에 영향을 미치는 요인에 관한 설명 정보를 주석(Notes)에 기재한다.",
            "③ 해당 연도 자산총액에서 그 자산의 역사적 원가를 차감하여 차액을 당기비용으로 직접 털어낸다.",
            "④ 금융감독원에 비밀 문서로 제출하여 대외 공시를 차단하고 보안을 유지한다.",
            "⑤ 회사의 공식 웹사이트 팝업창을 통해서만 정보를 공시한다."
        ],
        "answer": "2",
        "explanation": "② 경제적효익의 유입가능성이나 유출가능성이 낮은 경우, 그 자산이나 부채에 대해 가장 목적적합한 정보는 보통 발생가능한 유입·유출 크기, 시기 및 발생가능성 영향 요인에 대한 정보이며, 이러한 정보는 일반적으로 주석에 기재합니다.\n\n[오답 해설]\n① 유입/유출가능성이 낮은 것은 일반적으로 본문 계상보다 주석 공시를 합니다.\n③ 자산 총액에서 원가를 빼서 강제 비용 처리하는 논리는 왜곡된 회계처리입니다.\n④, ⑤는 공식적 재무보고 공시 경로와 거리가 멉니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "본문 금액 계상보다 일반적으로 주석 기재를 선호합니다.", "articles": [], "principle": "유입/유출가능성 저하 시 주석 공시", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "경제적효익 유입/유출가능성이 낮은 경우 시기, 규모, 확률 요인 등을 주석에 설명하는 것이 가장 목적적합한 정보 제공 방법입니다.", "articles": [], "principle": "유입/유출가능성 저하 시 주석 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가를 자산총액에서 차감하여 임의 비용 처리하는 처리는 회계 위배입니다.", "articles": [], "principle": "유입/유출가능성 저하 시 주석 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비밀 문서 처리 등은 재무공시의 투명성과 상충됩니다.", "articles": [], "principle": "유입/유출가능성 저하 시 주석 공시", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "웹사이트 팝업창은 정규 재무제표 공시 수단이 아닙니다.", "articles": [], "principle": "유입/유출가능성 저하 시 주석 공시", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "개념체계 상 경제적효익의 유입가능성이나 유출가능성이 매우 낮음에도 불구하고, 자산이나 부채를 본문에 인식하는 것이 재무제표 이용자에게 오히려 목적적합한 정보를 제공할 수 있는 대표적인 경우는?",
        "options": [
            "① 거래처와의 구두상으로 맺은 일반적인 납품 계약",
            "② 공정가치 등 목적적합한 측정방법이 존재하며 정보 제공의 유용성이 검증된 파생상품이나 보증 계약",
            "③ 단순 시외 지역 토지의 향후 개발 예정에 따른 시세 상승 예상 정보",
            "④ 대표이사 소유의 개인 주택에 설정된 소송 리스크",
            "⑤ 회사의 브랜드 가치를 높이기 위한 대규모 TV 광고 계약 예산"
        ],
        "answer": "2",
        "explanation": "② 파생상품이나 보증 계약 등은 경제적효익의 유입·유출 가능성이 매우 낮아도, 공정가치로 측정하여 관련 거래의 실질을 재무상태표 본문에 반영해 주는 것이 목적적합한 정보를 제공할 수 있습니다.\n\n[오답 해설]\n① 구두 납품 계약은 미이행계약의 초기 형태로 본문 인식 요건을 충족하지 못합니다.\n③ 단순 상승 예상 등은 자산의 정의 및 인식기준을 만족하지 못합니다.\n④ 주주의 개인 재산 리스크는 보고기업의 부채로 인식될 수 없습니다.\n⑤ 광고비 예산은 실제 지출 시 비용 처리될 뿐 인식 대상 자산이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "미이행 계약의 일반적 상태는 본문 인식 대상이 아닙니다.", "articles": [], "principle": "유입/유출가능성이 낮을 때의 본문 인식", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "유입/유출가능성이 낮더라도 파생상품이나 보증계약처럼 공정가치를 통해 가치를 목적적합하게 측정할 수 있으면 인식하는 것이 유용합니다.", "articles": [], "principle": "유입/유출가능성이 낮을 때의 본문 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시세 상승 등의 미래 가치 예상은 인식 대상이 아닙니다.", "articles": [], "principle": "유입/유출가능성이 낮을 때의 본문 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "개인 자산이나 개인 소송은 법인의 회계 보고 실체에 들어오지 못합니다.", "articles": [], "principle": "유입/유출가능성이 낮을 때의 본문 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 광고 예산 계획 등은 인식 대상 요소가 아닙니다.", "articles": [], "principle": "유입/유출가능성이 낮을 때의 본문 인식", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "개념체계 상 측정이 추정에 의존할 수밖에 없음으로 인해 발생하는 '측정불확실성(Measurement Uncertainty)'에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 재무제표의 모든 측정치에 추정이 도입되면 정보의 표현충실성은 자동적으로 완전히 상실된다.",
            "② 합리적인 추정의 사용은 재무정보 작성의 필수적인 부분이며, 추정치를 명확하고 정확하게 설명한다면 정보의 유용성을 훼손하지 않는다.",
            "③ 추정이 들어간 자산은 시장 거래 가치의 검증이 불가하므로 세무 보고 시 무조건 0원으로 평가해야 한다.",
            "④ 개념체계는 추정에 의한 측정을 원천적으로 금지하며 오직 확실한 현금 수납 영수증에 기초한 거래만 인식하도록 제한한다.",
            "⑤ 측정불확실성이 조금이라도 존재하면 당해 자산은 즉시 전액 대손충당금으로 적립해야 한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 많은 측정치에 추정이 요구되며, 합리적인 추정치를 사용하는 것은 재무보고 작성의 필수적 부분입니다. 추정의 한계와 가정을 이용자에게 투명하게 설명한다면 추정 정보는 유용합니다.\n\n[오답 해설]\n① 추정 도입이 표현충실성의 즉각적이고 완전한 상실을 뜻하지 않습니다.\n③, ④, ⑤는 회계 상 추정치 활용을 전면 부정하거나 왜곡된 실무 처리를 기술하고 있어 잘못되었습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "추정의 사용이 표현충실성을 반드시 저해하거나 파괴하는 것은 아닙니다.", "articles": [], "principle": "측정불확실성 개요", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "합리적인 추정은 필수적이며, 추정치를 명확히 공시하고 가정을 기술하면 정보의 유용성이 보존됩니다.", "articles": [], "principle": "측정불확실성 개요", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추정이 들어간 자산을 무조건 0원 세무 평가한다는 기준은 없습니다.", "articles": [], "principle": "측정불확실성 개요", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금주의 영수증 기반 정보만 인식한다는 규정은 없습니다(발생주의 회계 원칙).", "articles": [], "principle": "측정불확실성 개요", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "불확실성이 있다고 무조건 대손충당금을 기계적으로 적립하지는 않습니다.", "articles": [], "principle": "측정불확실성 개요", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "개념체계 상 자산·부채 측정에 수반되는 '높은 수준의 측정불확실성'과 '인식(Recognition)'의 상관관계에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 높은 수준의 측정불확실성이 있다면 그러한 추정치는 유용한 정보를 절대 제공할 수 없으므로 무조건 인식을 금지한다.",
            "② 높은 수준의 측정불확실성이 있더라도, 그러한 추정치가 유용한 정보를 반드시 제공하지 못하는 것은 아니다.",
            "③ 측정불확실성의 수준이 높으면 무조건 기업이 유리한 방향으로 자의적 평가액을 기재하여 인식한다.",
            "④ 측정불확실성이 높을 경우에는 취득원가가 아닌 시가총액을 반비례 비율로 나눈 금액으로 인식해야 한다.",
            "⑤ 높은 불확실성이 내포된 부채는 항상 자산으로 강제 재분류하여 인식하도록 규정되어 있다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 높은 수준의 측정불확실성이 있더라도, 그러한 추정치가 반드시 유용한 정보를 제공하지 못하는 것은 아님을 명확히 하고 있습니다. (즉, 불확실성이 높다는 이유만으로 인식을 자동 배제하지 않습니다.)\n\n[오답 해설]\n① 높은 불확실성이 있어도 정보가 유용하고 목적적합하다면 인식될 수 있습니다.\n③ 자의적 평가액을 기재하는 것은 충실한 표현(중립성)과 어긋납니다.\n④ 시가총액을 반비례로 배분하여 계상한다는 공식은 회계 원리에 없습니다.\n⑤ 부채를 자산으로 자의적으로 재분류하는 규정은 존재하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "높은 측정불확실성이 유용한 정보 제공 가능성을 완전히 차단하여 인식을 무조건 금지하지는 않습니다.", "articles": [], "principle": "측정불확실성과 인식의 유용성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "측정불확실성의 수준이 높다 하더라도, 추정치가 합리적으로 도출되었다면 여전히 유용한 정보를 제공할 수 있습니다.", "articles": [], "principle": "측정불확실성과 인식의 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적 평가 기재는 허용되지 않습니다.", "articles": [], "principle": "측정불확실성과 인식의 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "반비례 계산 배분법 등은 성립하지 않습니다.", "articles": [], "principle": "측정불확실성과 인식의 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채와 자산은 서로의 정의에 맞게 분류해야 합니다.", "articles": [], "principle": "측정불확실성과 인식의 유용성", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "개념체계 상 측정불확실성이 극도로 높고 설명 정보만으로는 충분히 명확히 규명할 수 없는 상황에서, 표현충실성을 달성하기 위한 가장 적절한 회계적 대안은?",
        "options": [
            "① 해당 자산이나 부채를 재무상태표 본문에 인식하지 않고, 주석으로 공시한다.",
            "② 임의의 최소 금액인 1원으로 본문에 우선 기재하고 주석 기재를 완전히 생략한다.",
            "③ 대손 가능성이 가장 높은 채권을 골라 자산 가치를 10배로 증액하여 표시한다.",
            "④ 측정불확실성을 0으로 강제 선언하고 과거의 평균 역사적 원가로 고정 기재한다.",
            "⑤ 회사의 당기순이익이 매년 균등하게 유지되도록 매 기말마다 금액을 슬라이딩 방식으로 조정 계상한다."
        ],
        "answer": "1",
        "explanation": "① 측정불확실성이 극도로 높고 설명 정보만으로 충실한 표현을 담을 수 없는 특별한 상황에서는, 자산이나 부채를 본문에 인식하지 않는 대신 주석(설명 정보)으로 공시하는 것이 유일하거나 최선의 대안일 수 있습니다.\n\n[오답 해설]\n② 최소 가액 기재 및 주석 생략은 충실한 표현에 위배됩니다.\n③ 자산 가치를 10배 증액하는 등은 허위 재무정보 기재로 금지됩니다.\n④ 측정불확실성을 자의적으로 0이라 간주하는 것은 왜곡 보고에 해당합니다.\n⑤ 인위적인 이익 평활화(Income Smoothing) 조작은 중립성을 정면으로 위배하는 행위입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "극도로 높은 측정불확실성이 해소되지 않으면, 본문 미인식 후 주석으로 상황을 충실히 기술하는 것이 최선책입니다.", "articles": [], "principle": "극단적 측정불확실성 대처", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적으로 1원 표기 후 주석을 생략하는 행위는 유용성과 정직성을 해칩니다.", "articles": [], "principle": "극단적 측정불확실성 대처", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 가치 왜곡 기재는 부정 회계에 해당합니다.", "articles": [], "principle": "극단적 측정불확실성 대처", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "불확실성을 고의로 은폐하고 원가 고정하는 행위는 왜곡입니다.", "articles": [], "principle": "극단적 측정불확실성 대처", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익을 평활하게 임의 가액 조정하는 조작 행위는 불가합니다.", "articles": [], "principle": "극단적 측정불확실성 대처", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "개념체계 상 제거(Derecognition)를 규율하는 회계처리가 궁극적으로 달성하고자 하는 재무보고 목표는?",
        "options": [
            "① 당해 기업이 보유한 총 현금잔고를 다른 경쟁 실체와 정확히 일치시키는 것",
            "② 해당 제거 거래가 발생한 후, 보고기업의 재무상태 변화를 가장 충실하게 표현하는 것",
            "③ 주식시장의 투자자들이 당기 손익 예측 시 아무런 오차도 내지 않도록 모든 불확실성을 완전히 박멸하는 것",
            "④ 세무 당국에 세금을 납부할 때 장부상 부채의 원가를 부풀려 감세 혜택을 극대화하는 것",
            "⑤ 회사의 회계 장부를 간소화하기 위하여 매년 말에 자산 잔액의 절반을 강제로 삭제하는 것"
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 제거 회계처리가 지향하는 목표는 제거 거래 이후에 보고기업이 보유하게 되는 자산/부채 및 재무상태의 변화를 재무상태표에 가장 충실하게 표현하여 이용자에게 전달하는 것입니다.\n\n[오답 해설]\n① 다른 기업과 보유 현금을 일치시킬 이유가 없습니다.\n③ 예측 오차의 발생 방지가 목표이더라도 미래 불확실성을 회계가 완전히 소멸시킬 수는 없습니다.\n④ 절세 편법이나 탈세를 위해 제거 회계를 적용하지 않습니다.\n⑤ 장부 간소화를 위해 자산 잔액의 절반을 강제 삭제하는 것은 심각한 회계 오류이자 부정 행위입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "다른 기업과의 잔고 일치와는 무관합니다.", "articles": [], "principle": "제거의 목적", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "제거 회계처리는 이전 거래 전후의 자산·부채 변동과 기업의 실질 재무상태 변화를 충실히 나타내기 위해 설계됩니다.", "articles": [], "principle": "제거의 목적", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계정보가 시장의 오차나 불확실성 자체를 소멸시켜 주지는 못합니다.", "articles": [], "principle": "제거의 목적", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조세 포탈 목적은 제거 회계의 이론적 목적이 아닙니다.", "articles": [], "principle": "제거의 목적", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "장부 청소를 위한 강제 자산 삭제는 허위 기재입니다.", "articles": [], "principle": "제거의 목적", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "개념체계 상 자산의 정의와 연동되어 자산의 '제거(Derecognition)' 여부를 결정짓는 가장 핵심적인 기준 개념은?",
        "options": [
            "① 법적 소유권(Legal Title)",
            "② 통제(Control)",
            "③ 시가(Market Value)",
            "④ 현금 수취(Cash Collection)",
            "⑤ 취득원가(Historical Cost)"
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 자산은 기업이 '통제'하는 현재의 경제적자원으로 정의되므로, 자산의 제거는 기업이 해당 자산에 대한 통제를 상실하였을 때 발생하게 됩니다.\n\n[오답 해설]\n① 법적 소유권이 이전되더라도 실질적인 경제적 통제를 유지하고 있다면 자산을 제거하지 않는 것이 충실한 표현일 수 있습니다. (통제가 우선함)\n③, ⑤는 측정 기준의 개념이지 제거 여부 판단의 핵심 질적 허들이 아닙니다.\n④ 대금을 회수하기 전이라도 통제가 이전되면 자산이 제거될 수 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "법적 소유권 유무보다 경제적 실질인 통제 여부가 우선합니다.", "articles": [], "principle": "자산 제거와 통제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산의 제거는 그 자산에 대한 통제권을 상실했을 때 비로소 일어납니다.", "articles": [], "principle": "자산 제거와 통제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가 변동 여부는 제거를 결정하지 않습니다.", "articles": [], "principle": "자산 제거와 통제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금 수취 시점이 제거 시점과 일치할 필요는 없습니다(통제 이전이 기준).", "articles": [], "principle": "자산 제거와 통제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적 원가는 제거 결정 기준이 아닙니다.", "articles": [], "principle": "자산 제거와 통제", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "개념체계 상 부채의 정의와 연동되어 부채의 '제거(Derecognition)'를 결정하는 본질적 요건은?",
        "options": [
            "① 채권자와의 구두상 말다툼으로 거래 관계가 단절되는 것",
            "② 기업이 인식한 부채에 대해 더 이상 '현재의무'를 부담하지 않는 것",
            "③ 부채의 장부 가액이 전년도 대비 10% 이상 하락하여 기재되는 것",
            "④ 채무자가 신규 투자를 위한 새로운 이사회 승인 보고서를 채택하는 것",
            "⑤ 세무 당국이 기업의 세금 환급액 수준을 확정 발표하는 것"
        ],
        "answer": "2",
        "explanation": "② 부채는 경제적 자원을 이전해야 하는 '현재의무'이므로, 기업이 해당 부채에 대해 현재의무를 더 이상 부담하지 않을 때(채무의 상환, 면제, 만료 등) 비로소 부채를 제거합니다.\n\n[오답 해설]\n① 거래 관계의 감정적 단절 등은 부채의 제거 요건이 아닙니다.\n③ 장부 가액의 수치 변화 자체로 제거 여부가 결정되지 않습니다.\n④ 내부 승인은 의무 소멸과 무관합니다.\n⑤ 세무 사항은 기업의 회계학 상 부채 제거의 본질적이고 보편적인 사유가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "말다툼이나 관계 소원 등은 회계적 의무 소멸이 아닙니다.", "articles": [], "principle": "부채 제거의 본질", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부채는 이행, 법적 소멸, 면제 등으로 현재의무를 부담하지 않게 될 때 제거됩니다.", "articles": [], "principle": "부채 제거의 본질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "장부 가액 하락은 제거가 아닌 측정의 문제입니다.", "articles": [], "principle": "부채 제거의 본질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "내부 보고서 채택은 의무를 소멸시키지 못합니다.", "articles": [], "principle": "부채 제거의 본질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "국세청의 환급액 발표 등은 일반 부채 제거 요건이 아닙니다.", "articles": [], "principle": "부채 제거의 본질", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "개념체계 상 인식기준(Recognition Criteria)을 충족시키기 위해 동시에 달성되어야 하는 근본적 질적 특성들의 조합으로 가장 올바른 것은?",
        "options": [
            "① 적시성(Timeliness)과 이해가능성(Understandability)",
            "② 목적적합성(Relevance)과 표현충실성(Faithful Representation)",
            "③ 비교가능성(Comparability)과 검증가능성(Verifiability)",
            "④ 보수주의(Prudence)와 역사적 원가주의(Historical Costing)",
            "⑤ 중요성(Materiality)과 발생주의(Accrual Basis)"
        ],
        "answer": "2",
        "explanation": "② 개념체계 상 재무제표 요소 정의를 충족하는 항목이라도 항상 인식되는 것은 아닙니다. 정보이용자에게 '목적적합한 정보'를 제공하고 '충실한 표현'을 제공할 수 있을 때에만 인식합니다. 이 둘은 근본적 질적 특성입니다.\n\n[오답 해설]\n①, ③은 보강적 질적 특성들의 모음이거나 조합으로, 근본적 질적 특성이 아닙니다.\n④, ⑤는 질적 특성과 측정 지침/회계 가정이 혼합된 것으로 인식기준의 판단 질적 요소가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "적시성과 이해가능성은 보강적 질적 특성에 속합니다.", "articles": [], "principle": "인식기준과 질적특성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "개념체계 상 정의를 충족하는 항목은 목적적합한 정보와 충실한 표현을 모두 제공할 때 인식됩니다.", "articles": [], "principle": "인식기준과 질적특성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비교가능성과 검증가능성은 보강적 질적 특성입니다.", "articles": [], "principle": "인식기준과 질적특성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보수주의와 원가주의는 근본적 질적 특성이 아닙니다.", "articles": [], "principle": "인식기준과 질적특성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "발생주의는 가정/지침이며 중요성은 목적적합성의 기업 특유 측면입니다.", "articles": [], "principle": "인식기준과 질적특성", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "개념체계 상 '존재의 불확실성(Existence Uncertainty)'과 '측정불확실성(Measurement Uncertainty)'의 구별에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 두 불확실성은 용어만 다를 뿐 완벽하게 동일한 개념이다.",
            "② 존재의 불확실성은 자산이나 부채가 실재하는가의 문제이고, 측정불확실성은 그 가치를 화폐 금액으로 합리적 추정할 수 있는지의 문제이다.",
            "③ 존재의 불확실성은 기업이 파산할 위기인지 판단하는 것이며, 측정불확실성은 금고에 현금이 몇 원 있는지 세어보는 것이다.",
            "④ 존재의 불확실성이 해소되어야만 측정불확실성의 파악을 비로소 개시할 수 있으며, 두 가정이 동시에 공존할 수는 없다.",
            "⑤ 측정불확실성이 높은 항목은 자동적으로 존재의 불확실성도 최고 수준인 것으로 간주된다."
        ],
        "answer": "2",
        "explanation": "② 존재의 불확실성은 권리(자산)나 의무(부채)가 보고기업에 실제로 존재하는가의 문제(예: 법적 분쟁 판결 전 상태 등)이고, 측정불확실성은 그 자산/부채의 가치를 합리적 추정하여 금액으로 측정할 수 있는지에 관한 평가 상의 문제입니다.\n\n[오답 해설]\n① 두 개념은 엄격히 구별됩니다.\n③ 파산 여부나 단순 현금 실사와는 무관한 왜곡된 예시입니다.\n④ 소송 중인 사건처럼 두 불확실성은 동시에 공존할 수 있습니다.\n⑤ 자산이 실재하더라도 측정불확실성이 높을 수 있으므로(예: 특별한 무형자산), 둘이 강제로 정비례 연계되는 것은 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "두 불확실성은 개념체계에서 별개의 카테고리로 다뤄집니다.", "articles": [], "principle": "불확실성 종류의 구분", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "존재 불확실성은 존재 여부의 규명 문제이며, 측정 불확실성은 추정의 정교함/정밀성 문제입니다.", "articles": [], "principle": "불확실성 종류의 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "파산 위기나 현금 실사 등에 관한 설명은 본 개념과 어긋납니다.", "articles": [], "principle": "불확실성 종류의 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "두 조건은 동시 존재 및 관여가 가능합니다.", "articles": [], "principle": "불확실성 종류의 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유형자산처럼 존재는 확실하지만 노후화에 의한 측정 가치 추정의 불확실성이 높을 수 있습니다.", "articles": [], "principle": "불확실성 종류의 구분", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "개념체계 상 자산이나 부채가 정의를 충족하나 목적적합성이나 표현충실성 한계로 본문에 인식되지 못할 때, '주석(Notes)'을 통한 설명 정보 제공의 의의로 가장 옳은 것은?",
        "options": [
            "① 본문 미인식으로 인한 유용한 정보 누락을 주석 공시를 통해 보완하며, 이용자의 의사결정을 지원한다.",
            "② 주석으로 공시만 해두면 감사인이나 감독기관이 본문 계상 오류를 절대 적발하여 처벌할 수 없다.",
            "③ 주석에 금액을 명시하면 재무상태표의 자산 합계액에 자동 가산되어 전산 연동된다.",
            "④ 주석 공시는 형식적 요건일 뿐, 실제로 정보를 읽는 투자자는 없으므로 중요성이 없다.",
            "⑤ 주석에 기재된 정보는 법적 효력이 없어 소송 등 분쟁 발생 시 증거로 활용되지 않는다."
        ],
        "answer": "1",
        "explanation": "① 자산이나 부채가 본문에 인식되지 않더라도, 발생 가능한 유출입 크기, 시기, 불확실성 조건 등에 관한 설명 정보를 주석으로 제공함으로써 재무제표의 유용성을 크게 보완해 줍니다.\n\n[오답 해설]\n② 본문에 올려야 할 항목을 누락하고 주석으로 떼우는 편법 기재는 오류 적발 및 수정 대상입니다.\n③ 주석 금액은 본문 합계에 자동으로 합산되지 않습니다.\n④ 주석은 재무제표의 핵심 유기적 구성요소로 투자자에게 매우 중요합니다.\n⑤ 주석 정보도 공식 재무보고 공시 내용이므로 법적/사회적 책임 대상이 됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "본문 인식 요건을 충족하지 못해도 유용한 불확실성 정보는 주석으로 알리는 것이 중요합니다.", "articles": [], "principle": "미인식 시 주석의 역할", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "본문에 올려야 할 항목을 미인식하고 주석 처리하는 것은 분식회계나 오류에 해당합니다.", "articles": [], "principle": "미인식 시 주석의 역할", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석 기재 수치가 본문 합계로 유입되지 않습니다.", "articles": [], "principle": "미인식 시 주석의 역할", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석은 재무보고에서 부수적이지 않은 필수불가결한 정보입니다.", "articles": [], "principle": "미인식 시 주석의 역할", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석 공시도 법적 증명력과 책임이 뒤따릅니다.", "articles": [], "principle": "미인식 시 주석의 역할", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "개념체계 상 미이행계약(Executory Contract)의 체결 시점과 결합된 권리·의무의 인식 문제에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 미이행계약은 계약을 체결한 즉시 자산과 부채를 각각 거액의 별개 계정으로 총액 인식한다.",
            "② 계약 당사자 모두가 자신의 의무를 이행하지 않은 초기 상태에서는, 결합된 권리와 의무가 상호의존적이어서 일반적으로 자산이나 부채로 본문에 인식하지 않는다.",
            "③ 계약 중 한쪽 당사자가 의무를 이행하는 순간에도 계약은 미이행으로 분류되어 자산의 인식이 영구 지연된다.",
            "④ 미이행계약은 무조건 이익잉여금의 임의적 적립금 계정으로 본문 자본란에 우선 인식된다.",
            "⑤ 계약이 해지되는 시점에도 제거 분개를 하지 않고 장부에 계속 자산으로 놔두어야 한다."
        ],
        "answer": "2",
        "explanation": "② 미이행계약은 양 당사자 모두 의무를 미수행했거나 동등하게 부분 수행한 계약입니다. 이 결합된 권리와 의무는 상호의존적이어서 단일 자산/부채를 구성하나, 이행 전에는 상계된 단일 권리/의무 상태로 보아 통상 정식 인식하지 않고 대기합니다.\n\n[오답 해설]\n① 체결 즉시 총액 인식하지 않습니다.\n③ 한쪽이 이행하는 순간 더 이상 동등하게 미이행된 계약이 아니며, 이행 수준에 맞춰 자산이나 부채가 정상적으로 인식되기 시작합니다.\n④ 자본에 직접 임의적립금 계정으로 타당성 없이 인식하지 않습니다.\n⑤ 계약 해지 시 권리/의무가 소멸하므로 제거 회계처리를 즉시 수반해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "미이행 계약 초기에는 자산/부채 총액 인식을 수행하지 않습니다.", "articles": [], "principle": "미이행계약의 인식", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "미이행계약은 결합된 권리·의무가 상호의존적이므로, 어느 쪽도 이행하지 않은 상태에선 일반적으로 본문 자산·부채로 인식하지 않습니다.", "articles": [], "principle": "미이행계약의 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일방의 이행 개시 시점부터는 미이행계약의 범주를 벗어나 자산/부채 인식이 촉발됩니다.", "articles": [], "principle": "미이행계약의 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본의 이익잉여금 임의적립 항목과 하등의 관련이 없습니다.", "articles": [], "principle": "미이행계약의 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계약 해지 시에는 잔존 권리의 소멸로 당연 제거해야 합니다.", "articles": [], "principle": "미이행계약의 인식", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },

    # =========================================================================
    # L3: 적용 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s07-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "A회사는 특허권 침해 혐의로 소송을 제기당해 피고 신분이 되었으며, 재판 결과에 따라 배상금을 지급할 현재의무가 존재하는지가 극히 불확실한 상태이다. 개념체계 상 이 소송 사건의 본문 부채 인식 여부 판단 기준으로 가장 적절한 것은?",
        "options": [
            "① 소송 피소액이 자산 총액의 1% 미만인 경우라면 재무제표 작성을 하지 않고 넘어가면 된다.",
            "② 의무의 존재 여부가 불확실하고 이에 다른 유출가능성도 낮으며, 발생 가능한 배상금의 결과 범위가 예외적으로 넓어 단일 금액 측정이 목적적합하지 않다면, 본문에 부채로 인식하지 않고 관련 상세 내역을 주석에 공시해야 한다.",
            "③ 특허권 관련 소송은 세무상 손금 산입 대상이 아니므로 회계상으로도 무조건 부채로 인식해야 한다.",
            "④ 판결 전이라도 원고가 제시한 최대 청구액을 재무상태표의 '단기차입금' 항목에 가산하여 보고한다.",
            "⑤ 의무가 존재할 확률이 10%에 불과하더라도 일단 사외에 현금을 전액 신탁하고 전액 자산으로 계상한다."
        ],
        "answer": "2",
        "explanation": "② 존재 불확실성과 낮은 이전 가능성, 그리고 넓은 결과 범위로 인한 측정불확실성이 결합된 경우에는, 단일 금액 부채 계상보다 미인식 후 주석 공시를 진행하는 것이 개념체계 상의 올바른 적용 지침입니다.\n\n[오답 해설]\n① 중요성이나 소송 규모에 관계없이 보고 기간 중 발생한 핵심 우발상황은 주석에 공시해야 합니다.\n③ 세무 손금 여부와 개념체계의 부채 인식기준은 별개입니다.\n④ 확정되지 않은 소송 청구액을 단기차입금(확정 채무)으로 올리는 것은 충실한 표현(정직성)을 심각하게 왜곡합니다.\n⑤ 임의의 신탁 자산화나 자산 계상은 규정에 없는 회계 처리입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재무제표 작성 자체를 누락하고 넘어가는 것은 오류입니다.", "articles": [], "principle": "존재 불확실성 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "존재 및 측정불확실성이 고도로 결합된 피소 사건은 부채 본문 인식을 보류하되 주석 공시로 이용자에게 사실관계를 알립니다.", "articles": [], "principle": "존재 불확실성 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 규정에 종속되지 않으며, 무조건 부채 인식하는 사유가 될 수 없습니다.", "articles": [], "principle": "존재 불확실성 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미확정 청구액을 확정부채인 단기차입금에 가산하는 것은 불법 왜곡입니다.", "articles": [], "principle": "존재 불확실성 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사외 현금 신탁 및 강제 자산화는 회계처리의 왜곡입니다.", "articles": [], "principle": "존재 불확실성 적용", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "B은행은 수출기업인 C사를 위하여 대출 상환 보증을 섰다. 현재 C사의 파산 확률은 극히 낮으므로 B은행이 보증 의무를 이행할(현금 유출) 가능성은 매우 낮다. B은행의 재무제표 작성 시, 이 보증 의무의 부채 인식 기준에 대한 설명으로 가장 적절한 것은?",
        "options": [
            "① 유출가능성이 매우 낮으므로 보증 계약을 체결한 사실조차 재무제표 어디에도 기재하지 않는다.",
            "② 이전가능성이 매우 낮더라도 공정가치 등 목적적합한 방식으로 측정할 수 있고 정보 유용성이 있다면 보증 채무를 부채로 인식할 수 있으며, 관련 우발 사항을 주석에 함께 기재한다.",
            "③ 보증 채무는 항상 C사가 차입한 대출원금 전액을 B은행의 '차입금' 본문 계정에 계상하여 보고해야 한다.",
            "④ C사가 파산하여 현금 유출이 현실화될 때까지 보증 관련 장부처리를 완전히 누락하는 것이 중립성 확보에 기여한다.",
            "⑤ 파산 가능성이 조금이라도 있으므로 즉시 당기 손실로 전액 처리하고 동액의 현금을 소각한다."
        ],
        "answer": "2",
        "explanation": "② 금융 보증이나 파생상품 계약은 경제적효익의 유출가능성이 매우 낮더라도, 공정가치를 통해 가치를 목적적합하게 측정할 수 있고 정보 유용성이 있다면 재무제표 본문에 부채로 인식하는 것이 합당할 수 있으며, 이와 관련된 내역은 주석으로 함께 상세 설명 공시합니다.\n\n[오답 해설]\n① 보증 사실 자체를 은폐하는 것은 중요한 유용성 정보의 누락입니다.\n③ 피보증인의 채무액 전체를 보증인의 확정 차입금으로 본문에 기재하면 채무 관계가 심각하게 왜곡됩니다.\n④ 아무 처리를 안 하고 있다가 터졌을 때만 분개하는 것은 발생주의 및 보증가치 미인식 왜곡입니다.\n⑤ 현금 소각 등은 정상적인 기업 회계 실무와 전혀 관련이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "중요한 보증 사실의 영구 누락은 재무보고의 성실성 위배입니다.", "articles": [], "principle": "낮은 가능성 부채 인식 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보증 채무처럼 이행 확률이 낮더라도 금융 요소 가치를 목적적합하게 공정가치 측정할 수 있다면 본문 인식 및 주석 병행이 가능합니다.", "articles": [], "principle": "낮은 가능성 부채 인식 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "C사의 대출액을 자사의 차입금으로 이중 계상할 수는 없습니다.", "articles": [], "principle": "낮은 가능성 부채 인식 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실제 파산 전까지 아예 처리를 누락하는 행위는 부적절합니다.", "articles": [], "principle": "낮은 가능성 부채 인식 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금 소각 및 이유 없는 손실 계상은 무근본 실무입니다.", "articles": [], "principle": "낮은 가능성 부채 인식 적용", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "D제조회사는 자사가 보유하고 있던 기계장치(장부가액 1,000만 원)를 외부 금융회사에 1,200만 원에 매각하였다. 그러나 계약상 D사는 동일 기계장치를 1년 뒤 1,300만 원에 무조건 도로 사 와야 하는 강제 환매조건(Repurchase Agreement)을 맺고 있다. 개념체계 상 이 거래의 자산 제거 여부 판단으로 가장 적절한 것은?",
        "options": [
            "① 매각 대금 1,200만 원이 계좌로 유입되었고 법적 소유권 계약서가 체결되었으므로, D사는 즉시 기계장치를 장부에서 제거하고 매각자산처분이익 200만 원을 수익 인식한다.",
            "② D사는 1년 뒤 기계를 강제로 도로 매입해야 하므로 실질적으로 기계장치의 통제를 상실하지 않았다. 따라서 기계장치를 제거해서는 안 되며, 받은 대금 1,200만 원은 '차입금(금융부채)'으로 처리해야 한다.",
            "③ 환매가격과 매각가격의 차이인 100만 원을 당기 매출액으로 계상한 후, 기계장치의 절반 금액만 일시 제거한다.",
            "④ 기계장치의 시장가격 변동을 알아본 후, 가격이 하락했다면 자산을 제거하고 상승했다면 제거하지 않는 자의적 방법을 쓴다.",
            "⑤ 환매조건부 판매는 세무상 부가가치세 면세 거래이므로 즉시 자산을 전액 자본계정으로 대체한다."
        ],
        "answer": "2",
        "explanation": "② 형식적(법적)으로는 매각 형식을 띠고 있으나 강제 환매 조건이 붙어 있어 매도자가 자산의 사용 지시 및 효익 취득을 계속 통제합니다. 따라서 실질적인 통제 상실이 없으므로 자산을 제거할 수 없고, 거래 실질은 담보 차입 거래(받은 대금은 부채 처리)로 분류됩니다.\n\n[오답 해설]\n① 법적 거래 양식만 보고 통제가 여전히 남아 있는 자산을 제거하고 가공의 처분이익을 잡는 것은 표현충실성(실질 우선)에 위배됩니다.\n③ 차액 100만 원은 차입 이자에 대응하므로 매출액이 아니라 기간 경과에 따라 이자비용으로 인식합니다.\n④ 시가 변동 여부에 따라 제거 여부를 기계적으로 바꾸는 논리는 비회계적입니다.\n⑤ 세법상의 면세 여부 등은 회계 자산 제거 기준의 실질 판단 요건이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "법적 외관만을 보고 처분 처리하면 거래 실질(차입)이 훼손되므로 제거할 수 없습니다.", "articles": [], "principle": "자산 제거 실질 우선", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "환매의무로 인해 통제가 상실되지 않았으므로 자산을 제거하지 않고 담보 차입으로 처리하는 것이 충실한 표현입니다.", "articles": [], "principle": "자산 제거 실질 우선", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차액은 매출이 아니라 이자비용의 성격입니다.", "articles": [], "principle": "자산 제거 실질 우선", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적인 시가 변동 연계 제거 처리는 잘못되었습니다.", "articles": [], "principle": "자산 제거 실질 우선", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법과 회계 개념체계 상 제거 판단 요건은 개별적입니다.", "articles": [], "principle": "자산 제거 실질 우선", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "E사는 거래은행인 F은행에 대한 단기차입금 5,000만 원을 상환해야 하는 현재의무가 있다. E사는 G사에게 대가를 지불하고 해당 채무를 G사가 인수(제3자 채무인수)하도록 계약을 체결했다. E사의 재무상태표에서 이 5,000만 원의 부채를 제거할 수 있는 조건으로 가장 올바른 것은?",
        "options": [
            "① E사와 G사가 채무 인수 계약서를 작성하고 서명 날인한 당일 즉시 부채를 제거한다.",
            "② 채권자인 F은행이 G사로의 채무 인수를 공식 동의하고 법적으로 E사의 상환 의무를 면제하여, E사가 더 이상 F은행에 대해 현재의무를 부담하지 않게 되었을 때 제거한다.",
            "③ 채무 인수가 세법상 손금 불산입으로 처리되지 않는 연도 말에 한하여 분기별로 제거한다.",
            "④ 부채 제거 시 동액의 가공 매출액을 인식하는 조건이 내부 기안서에 포함되어 있을 때 제거한다.",
            "⑤ G사의 주가가 E사의 주가보다 높아 부채 상환 여력이 충분해 보이는 순간 즉시 소급 제거한다."
        ],
        "answer": "2",
        "explanation": "② 부채는 채무자 입장에서 현재의무를 더 이상 부담하지 않을 때에만 제거됩니다. 제3자가 인수를 약정했더라도 채권자의 면제나 법적 권리 양도가 완성되어 본사의 의무가 확실히 소멸하지 않았다면 부채를 제거할 수 없습니다.\n\n[오답 해설]\n① 채무자와 인수자 간의 합의만으로는 채권자에 대한 채무자 본인의 의무가 소멸하지 않으므로 부채 제거가 안 됩니다.\n③ 세무 손금 여부와 부채 제거 시점은 관련이 없습니다.\n④ 가공 매출액 가설은 비상식적 회계 분개 유도입니다.\n⑤ 주가 고저나 주식 시장 상황은 부채의 법적/실질적 소멸을 판가름하는 잣대가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "채권자의 면제가 없는 채무자와 제3자 간 계약서만으로는 의무가 소멸하지 않습니다.", "articles": [], "principle": "부채 제거 요건 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "채권자가 채무자의 의무를 최종 면제하여 채무자가 더 이상 현재의무를 지지 않게 될 때 부채를 제거합니다.", "articles": [], "principle": "부채 제거 요건 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 규정에 따라 제거가 좌우되지 않습니다.", "articles": [], "principle": "부채 제거 요건 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가공 매출 인식 등의 조건은 위법 사항입니다.", "articles": [], "principle": "부채 제거 요건 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주가 수준 비교 등은 부채 소멸 판단과 완전 무관합니다.", "articles": [], "principle": "부채 제거 요건 적용", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "H제약회사는 백신 개발을 위해 10억 원의 연구비(Research Phase)를 지출했다. 현시점에서 상업화 성공 여부나 미래 경제적 효익의 유입 시기·크기는 극도로 불확실하다. 개념체계 상 이 연구비 지출의 인식 처리에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 연구비 지출은 측정불확실성이 높더라도 일단 '백신개발투자권'이라는 자산으로 무조건 기재하여 보고해야 한다.",
            "② 미래 경제적 효익을 창출할 현재의 권리가 불확실하거나 측정불확실성이 너무 높아 충실한 표현이 어렵다면, 자산으로 인식하지 않고 즉시 비용 처리한다.",
            "③ 백신 개발 사업이 완료될 때까지 관련 10억 원의 분개를 누락하여 대차대조표를 불일치 상태로 보관한다.",
            "④ 지출 즉시 주주총회 결의를 거쳐 전액을 '자본금' 감액 분개로 반영해야 한다.",
            "⑤ 정부의 백신 개발 보조금 수령 여부에 상관없이 전액 법인세 납부 부채로 인식한다."
        ],
        "answer": "2",
        "explanation": "② 연구 단계의 지출은 미래 경제적 효익을 창출할 현재의 경제적 자원(권리)의 존재 자체가 불확실하거나, 가치 측정을 위한 신뢰성이 현저히 결여(극심한 측정불확실성)되므로 자산 인식기준을 미충족합니다. 따라서 발생 즉시 전액 당기 비용으로 처리합니다.\n\n[오답 해설]\n① 미래 가치 창출 여부가 불확실하고 통제가 불비한 상태에서 자산 강제 계상은 불허됩니다.\n③ 대차 불일치 장부 방치는 회계의 기본 기록 원리에 위배되는 불법 행위입니다.\n④ 일반 연구비 지출을 감자(자본금 감액) 처리할 근거는 전혀 없습니다.\n⑤ 이를 납부 부채로 인식해야 할 회계 이론적 정당성은 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산 정의 및 충실한 표현 요건을 미충족하므로 자산 강제 계상은 잘못되었습니다.", "articles": [], "principle": "측정불확실성과 자산인식 유보", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "효익 유입 권리의 존재가 불확실하고 측정불확실성이 높은 연구 단계 지출은 자산 인식하지 않고 발생 시 비용 처리합니다.", "articles": [], "principle": "측정불확실성과 자산인식 유보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대차가 맞지 않는 분개 방치는 심각한 회계 오류입니다.", "articles": [], "principle": "측정불확실성과 자산인식 유보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "연구비 지출은 감자 거래가 아닙니다.", "articles": [], "principle": "측정불확실성과 자산인식 유보", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "연구비 지출을 법인세 부채로 계상할 수 없습니다.", "articles": [], "principle": "측정불확실성과 자산인식 유보", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "I사는 거래처에 대한 매출채권 1억 원을 금융회사에 조기 매각(팩토링)하였다. 그러나 계약 상 해당 매출채권이 부도가 날 경우 I사가 금융회사에 전액 대신 대위변제해 주어야 하는 무조건적 '소구의무(Recourse Obligation)'를 보유하고 있다. 개념체계 상 이 거래의 채권 제거 여부 판단으로 가장 적절한 것은?",
        "options": [
            "① 대금이 회수되었으므로 즉시 매출채권 1억 원을 제거하고 매출채권처분손실을 계상한다.",
            "② 매출채권 부도 리스크와 권리의 실질적 통제가 I사에 완전히 남아 있으므로 채권을 장부에서 제거하지 않고, 받은 자금은 '단기차입금(담보부차입)' 부채로 인식한다.",
            "③ 채권액의 절반은 제거하고 나머지 절반은 자본금 증가로 대체한다.",
            "④ 금융감독원이나 관할 세무서에 문의하여 당해 연도 세법 방침에 따라 제거 여부를 무작위로 선택한다.",
            "⑤ 금융회사가 I사의 대주주이므로 제거 회계처리와 상관없이 전액 수익으로 임의 기재한다."
        ],
        "answer": "2",
        "explanation": "② 자산 이전 거래에서 이전자가 신용 위험 및 부도 손실 위험(소구의무)을 전적으로 부담한다면 자산의 실질적 통제가 이전되지 않은 것으로 봅니다. 따라서 매출채권을 제거할 수 없으며 담보 차입 거래로 처리합니다.\n\n[오답 해설]\n① 소구의무 등 실질적 통제가 유지되고 있음에도 제거 후 매각 처리하는 것은 회계 오류입니다.\n③ 자본금 대체나 임의 절반 제거는 규정이 없습니다.\n④ 개념체계 판단 요건은 세법과 개별 독립적으로 규율됩니다.\n⑤ 특수관계자 거래라 하더라도 실질 통제 양도 여부 기준에 맞춰 올바르게 분개해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "소구의무 부담은 통제 이전 실패를 의미하므로 처분 제거할 수 없습니다.", "articles": [], "principle": "소구의무와 자산 제거", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산 양도자가 부도 리스크(소구의무)를 완전히 통제 보유한다면 자산을 제거하지 않고 차입부채로 계상합니다.", "articles": [], "principle": "소구의무와 자산 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 대체나 절반 분할 제거는 근거가 없습니다.", "articles": [], "principle": "소구의무와 자산 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법과 회계 개념체계의 제거 기준은 별개입니다.", "articles": [], "principle": "소구의무와 자산 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특수관계 여부와 무관하게 통제 기준으로 회계처리해야 합니다.", "articles": [], "principle": "소구의무와 자산 제거", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "J사는 보유 중인 상가 건물을 타사에 매각하면서, 6개월 이내에 매수인이 지급한 금액에 이자율을 가산한 금액으로 해당 건물을 도로 사 올 수 있는 '콜옵션(Call Option, 매수선택권)'을 계약 조건에 명시했다. 이 콜옵션은 현재 내가가격(In-the-money) 상태로 행사 확률이 매우 유력하다. 건물의 제거 판단에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 건물의 법적 등기가 이미 양도되었으므로 무조건 즉시 제거하고 거액의 처분이익을 잡아야 한다.",
            "② J사가 건물에 대한 통제를 콜옵션을 통해 실질적으로 계속 쥐고 있으므로 상가 건물을 제거해서는 안 되며 금융 거래로 회계처리해야 한다.",
            "③ 콜옵션 행사 전에 미리 건물을 제거하고 행사 당일에 소급하여 취득하는 전산 분개를 수립한다.",
            "④ 건물의 감가상각 누계액을 자본잉여금으로 이전 상계하고 건물 자산 계정은 영구 보존한다.",
            "⑤ 옵션 거래는 장외 거래이므로 재무제표에 일체 공시하지 않고 비밀에 부친다."
        ],
        "answer": "2",
        "explanation": "② 콜옵션 권리를 통해 이전 자산을 언제든 도로 찾아올 수 있고 그 권리 행사가 유력하다면, 건물에 대한 경제적 통제가 이전되지 않은 것과 다름없습니다. 따라서 건물을 제거할 수 없고 금융 거래(차입 등)로 회계처리해야 합니다.\n\n[오답 해설]\n① 법적 등기 이전만으로 제거 처리하는 것은 회계상 표현충실성(실질의 반영)에 부합하지 않습니다.\n③ 미리 제거했다가 소급 재조정하는 비정상적 기재는 허용되지 않습니다.\n④ 상각 누계액을 자본잉여금과 상계시키는 분개 논리는 회계 위배입니다.\n⑤ 장외 옵션 거래라 하더라도 재무적 영향이 발생하므로 본문/주석에 공시해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "콜옵션을 통한 실질적 통제 유지가 확인되므로 등기 이전만으로 제거할 수 없습니다.", "articles": [], "principle": "콜옵션 보유와 자산제거", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산 양도자가 가치 있는 콜옵션을 유보하여 실질 통제를 유지한다면, 자산을 제거하지 않고 차입부채 등으로 처리합니다.", "articles": [], "principle": "콜옵션 보유와 자산제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "행사 전에 선제거 후 재취득 소급 처리는 분개 왜곡입니다.", "articles": [], "principle": "콜옵션 보유와 자산제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각누계액과 자본잉여금을 상계하는 회계 처리는 잘못되었습니다.", "articles": [], "principle": "콜옵션 보유와 자산제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비밀주의적 비공시는 재무제표 공시 원칙에 위배됩니다.", "articles": [], "principle": "콜옵션 보유와 자산제거", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "개념체계 상 미인식 자산이나 부채와 결합된 제거 거래의 표현충실성에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 미인식 자산이 결합된 거래는 본문에 아무런 기록도 남기지 않는 것이 표현충실성이다.",
            "② 자산이나 부채의 이전 후에도 보고기업의 재무상태 변화를 가장 적절히 묘사할 수 있는 방식으로 회계처리를 설계해야 하며, 필요시 새로운 자산/부채를 추가 인식하거나 종전 자산을 계속 인식한다.",
            "③ 미인식 자산이 이전되었다면 즉시 해당 금액만큼 자본금을 강제 상환 감자해야 한다.",
            "④ 금융 자산을 이전하고 수수료를 지급한 거래는 수수료를 전부 광고비로 오분류하는 것이 허용된다.",
            "⑤ 회사의 미인식 특허권이 소멸하였다면 과거의 특허 취득 예상액을 가공 계상하여 비용 처리한다."
        ],
        "answer": "2",
        "explanation": "② 자산이나 부채의 이전 거래 결과로 종전 자산이 소멸하는 한편 새로운 권리/의무(미인식 자산/부채 등)가 생기거나, 일부만 통제권을 상실한 경우 재무상태 변화를 가장 충실하게 묘사하는 제거 회계처리를 선택하여 적용합니다.\n\n[오답 해설]\n① 기록을 아예 생략하는 것은 왜곡입니다.\n③ 자본금 강제 상환은 제거의 본질적 회계 처리가 아닙니다.\n④ 수수료를 다른 광고비 등으로 일부러 왜곡 보고하는 것은 허용되지 않습니다.\n⑤ 미인식 자산의 소멸에 가공의 자산과 비용을 인위로 창출해 분개하는 행위는 심각한 분식회계입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "아무런 기록도 남기지 않는 방식은 표현충실성을 해칩니다.", "articles": [], "principle": "이전 거래의 표현충실성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이전 후 보고기업의 자산·부채 변동 양상을 가장 충실하게 묘사하도록 회계처리를 설계 적용해야 합니다.", "articles": [], "principle": "이전 거래의 표현충실성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 감자 처리 지침은 사실과 무관합니다.", "articles": [], "principle": "이전 거래의 표현충실성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의도적인 오분류 계상은 충실한 표현(중립성)에 어긋납니다.", "articles": [], "principle": "이전 거래의 표현충실성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가공 자산/비용 기재는 심각한 부정 오류입니다.", "articles": [], "principle": "이전 거래의 표현충실성", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "K사는 만기가 도래한 차입금 1억 원의 변제를 위해, 은행과 협의하여 이자율과 만기를 대폭 변경한 새로운 대출 계약으로 재체결하고 기존 대출 계약을 법적으로 소멸시켰다. 이 거래의 제거 및 신규 인식 판단으로 가장 옳은 것은?",
        "options": [
            "① 기존 채무와 계약 형태가 완전히 변경되고 종전 채무에 대한 의무가 소멸하였으므로, 기존 부채 1억 원을 제거하고 신규 부채를 공정가치로 새로 인식한다.",
            "② 금액이 1억 원으로 동일하므로 장부상 아무런 변화나 분개 없이 기존 채무 명칭을 그대로 방치한다.",
            "③ 차입 부채의 조건 변동은 세법상 과세 대상이 아니므로 장부 제거를 세법상 원천 금지한다.",
            "④ 기존 부채액을 전액 매출액으로 대체하여 기재한 후, 신규 차입금은 광고선전비로 비용 처리한다.",
            "⑤ 은행이 이자를 감면해주었더라도 장부상에는 기존 이자율을 고정하여 가공 부채를 추가로 쌓는다."
        ],
        "answer": "1",
        "explanation": "① 부채의 조건이 실질적으로 크게 변경되었거나 종전 계약이 법적으로 소멸하여 새로운 의무로 대체된 경우, 기존 부채는 더 이상 현재의무가 아니므로 제거하고, 새로 계약된 부채를 공정가치로 신규 인식하는 것이 충실한 표현에 부합합니다.\n\n[오답 해설]\n② 계약 조건의 중요 변동이나 법적 소멸 사실을 무시하고 아무 분개도 하지 않는 것은 거래의 오인식입니다.\n③ 세법 방침에 따라 제거 여부가 결정되지 않습니다.\n④ 부채를 매출로 잡거나 차입금을 광고선전비로 분개하는 논리는 극심한 회계오류입니다.\n⑤ 이자 감면 시 이자비용 경감이나 부채 감소를 반영해야 하며 가공 부채 계상은 허용되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "기존 의무가 법적으로 소멸하고 다른 실질의 채무로 교환되었다면 기존 부채를 제거하고 새 부채를 인식합니다.", "articles": [], "principle": "부채 조건 변경의 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "중요한 계약 변경 사실을 무시하고 기존 장부를 방치해서는 안 됩니다.", "articles": [], "principle": "부채 조건 변경의 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 과세 조건에 관계없이 회계 실질에 맞춰 부채를 조정합니다.", "articles": [], "principle": "부채 조건 변경의 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 이전액을 가공 매출로 인식하는 것은 분식회계입니다.", "articles": [], "principle": "부채 조건 변경의 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실제 이자 소멸액을 장부에 반영하지 않고 가공 부채를 유지할 수 없습니다.", "articles": [], "principle": "부채 조건 변경의 제거", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "L사는 과거 경제적 효익의 유입가능성이 매우 낮아 자산으로 인식하지 않고 주석으로만 기재했던 특허 소송의 권리자(원고)였다. 당해 연도 법원 최종심에서 승소 판결이 내려져 상대방으로부터 5,000만 원을 수취할 법적 권리가 최종 확정되었다. 이 시점의 회계처리로 가장 옳은 것은?",
        "options": [
            "① 과거에 자산으로 본문 인식하지 않았으므로, 확정된 판결 이후에도 영원히 자산으로 잡을 수 없다.",
            "② 유입가능성이 확실해지고 권리가 완전 확정되었으므로, 해당 5,000만 원의 매출채권(미수금) 자산을 본문에 인식하고 동액의 소송수익(이익)을 당기손익에 계상한다.",
            "③ 과거 연도의 모든 재무제표를 소급하여 과거 1년 차 대차대조표에 자산으로 강제 소급 기재한다.",
            "④ 5,000만 원을 자산으로 잡되, 상대방의 부도 위험을 고려하여 동액의 자본금을 소급 감자 처리한다.",
            "⑤ 회사의 비밀 기금으로 적립하여 경영진의 격려금으로 즉시 지급하고 장부에는 일체 남기지 않는다."
        ],
        "answer": "2",
        "explanation": "② 상황 변화로 인해 과거 유입가능성이 낮던 자원의 권리 유입이 확실해지고 금액이 최종 확정되면, 이는 자산의 인식요건(목적적합성, 표현충실성)을 충족하므로 본문에 자산으로 정식 인식하고 관련 손익을 당기 손익에 귀속시킵니다.\n\n[오답 해설]\n① 새로운 사실의 발생에 따라 인식이 이루어져야 합니다.\n③ 상황 변화에 따른 신규 인식은 소급 수정 오류 사항이 아니며 당기 전진 처리합니다.\n④ 수취 권리가 생긴 자산 인식 거래에 자본금 감자를 단행할 이유가 없습니다.\n⑤ 회계장부 누락 및 비밀 기금 조성을 통한 격려금 무분개 지급은 횡령이자 회계 위반입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상황의 실질적 변화로 권리가 확정되었는데도 자산 인식을 거부하는 것은 틀렸습니다.", "articles": [], "principle": "상황 변화와 자산 신규 인식", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "판결 확정으로 현금 유입이 사실상 보장되고 권리가 생긴 시점에 자산과 관련 수익을 당기 인식합니다.", "articles": [], "principle": "상황 변화와 자산 신규 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소급 재작성 사항이 아니며 확정 시점에 당기 전진 인식합니다.", "articles": [], "principle": "상황 변화와 자산 신규 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채권 인식 거래에서 엉뚱하게 소급 감자 분개를 넣는 것은 무효입니다.", "articles": [], "principle": "상황 변화와 자산 신규 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "횡령이나 임의 누락은 용인되지 않는 불법 사항입니다.", "articles": [], "principle": "상황 변화와 자산 신규 인식", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "M사는 보유하고 있던 본사 사옥을 부동산 신탁회사에 법적으로 이전 등기하였다. 그러나 신탁 계약 조건 상 부동산의 모든 임대 수익과 시세 차익은 100% M사에 귀속되며 신탁회사는 단순 명의 관리만 수행한다. 개념체계 상 사옥의 제거 판단으로 가장 적절한 것은?",
        "options": [
            "① 등기부등본 상 법적 소유주가 변경되었으므로 즉시 건물을 제거하고 양도손익을 인식해야 한다.",
            "② 사옥에서 생기는 모든 경제적 효익을 M사가 지시하고 획득하는 통제권을 실질적으로 유지하고 있으므로 건물을 제거해서는 안 된다.",
            "③ 건물의 절반만 임시로 제거한 후, 10년 뒤에 나머지 절반을 서서히 제거한다.",
            "④ 건물의 명의가 이전되었으므로 동액의 '부채'를 장부에 가산하고 자본금은 전액 상각한다.",
            "⑤ 회계담당자가 임의로 건물의 잔액을 매년 자본조정 계정으로 숨겨 두는 기재를 쓴다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 자산의 판단에 있어 법적 소유권보다 실질적인 통제 여부(경제적 실질)를 중시합니다. 모든 효익의 향유와 통제권이 매도자(위탁자)에게 잔존하므로 자산을 제거해서는 안 됩니다.\n\n[오답 해설]\n① 법적 명의 이전만을 기준으로 제거 처리를 하는 것은 실질의 충실한 표현에 위배됩니다.\n③, ④, ⑤는 아무런 근거가 없는 부적절한 분개 유도 및 자의적 숨기기 기재 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "법적 양도 외관만으로 경제적 통제가 남아 있는 자산을 제거할 수 없습니다.", "articles": [], "principle": "신탁 부동산의 통제와 제거", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "실질적인 사용 통제권과 경제적 효익 수취권이 여전히 기업에 귀속되므로 사옥 자산을 제거하지 않는 것이 올바릅니다.", "articles": [], "principle": "신탁 부동산의 통제와 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적인 일부 기간 분할 제거 등은 허용되지 않습니다.", "articles": [], "principle": "신탁 부동산의 통제와 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "명의 이전을 부채의 증가나 자본 상각으로 대체하는 회계 처리는 잘못되었습니다.", "articles": [], "principle": "신탁 부동산의 통제와 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "장부금액을 편법으로 자본조정란 등에 숨겨 두는 꼼수 기재는 허용되지 않습니다.", "articles": [], "principle": "신탁 부동산의 통제와 제거", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "N가전회사는 판매한 제품에 대해 1년간 무상 품질 보증(Warranty) 서비스를 제공한다. 개별 제품당 하자가 발생하여 AS 비용이 발생할 가능성은 낮지만, 과거 대량의 판매 통계 데이터를 바탕으로 볼 때 전체적인 AS 비용 청구 총액은 매우 신뢰성 있게 추정(추정치 산출)할 수 있다. 개념체계 상 이 품질보증 의무의 부채 인식에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 개별 제품의 무상 수리 의무 가능성이 낮으므로 본사 품질보증 부채 계상은 전면 금지된다.",
            "② 비록 개별 건별로는 불확실성이 크더라도 포트폴리오(전체 판매분) 관점에서 합리적 추정이 가능하고 부채의 정의를 충족하므로, 품질보증충당부채를 인식하고 당기 품질보증비용을 처리하는 것이 타당하다.",
            "③ 보증 비용 지급 시점까지 아무 장부 처리를 하지 않다가, 돈이 나간 연도 말에 한꺼번에 '기부금'으로 회계 처리한다.",
            "④ 품질 보증은 마케팅 비용이므로 전액 당기순이익에 가산하는 분개를 시행한다.",
            "⑤ 회사의 판매 수익을 낮추기 위한 목적으로 추정 총액의 100배를 과다 계상하여 부채로 기재한다."
        ],
        "answer": "2",
        "explanation": "② 품질보증 의무처럼 대량의 포트폴리오 거래에서는 통계적 기댓값을 통해 측정불확실성을 유용하게 통제하고 합리적으로 추정할 수 있습니다. 따라서 부채 정의를 충족하는 충당부채를 인식하는 것이 발생주의 및 충실한 표현에 잘 부합합니다.\n\n[오답 해설]\n① 개별 건의 가능성이 낮다는 이유로 포트폴리오 전체의 확실한 추정치 인식을 배제하지 않습니다.\n③ 현금 지급 시에만 기부금 등 잘못된 계정으로 처리하는 것은 발생주의 위배입니다.\n④ 보증의 실질은 부채와 비용의 인식이며 순이익에 가산하는 자본 유입이 아닙니다.\n⑤ 자의적인 과다 계상은 중립성(표현충실성) 위반입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "개별 확률이 낮더라도 대량 통계로 추정이 가능하다면 인식을 배제할 필요가 없습니다.", "articles": [], "principle": "품질보증부채 인식 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "과거 경험률에 기초해 신뢰성 있게 추정한 품질보증 의무액은 충당부채와 비용으로 본문에 정상 인식하는 것이 목적적합합니다.", "articles": [], "principle": "품질보증부채 인식 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보증수리비를 기부금으로 대체 처리하는 것은 잘못입니다.", "articles": [], "principle": "품질보증부채 인식 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "품질 보증 관련 지출은 수익 가산 항목이 아닌 부채/비용 항목입니다.", "articles": [], "principle": "품질보증부채 인식 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "의도적인 100배 과다 계상은 중립성과 정직성을 파괴하는 분식 행위입니다.", "articles": [], "principle": "품질보증부채 인식 적용", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "O회사는 거래처와 공장 건설용 특수 강재를 1년 뒤 납품받기로 하는 미이행계약(Executory Contract)을 맺었다. 그러나 계약 체결 후 철강 가격이 폭락하여, 계약 조건에 따라 시장 가격보다 훨씬 비싼 값으로 의무를 이행해야 하는 '불리한(Onerous) 교환 조건'으로 전락하였다. 개념체계 상 이 불리한 미이행계약의 인식에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 교환 조건이 불리해지더라도 계약이 완전 미이행 상태라면 본문 부채 인식이 원천 불가능하다.",
            "② 미이행계약의 결합된 권리와 의무 중 교환조건이 현재 불리하게 되어 회피할 수 없는 손실 의무가 성립했다면, 관련 부채(충당부채)를 인식하는 것이 재무상태를 충실히 표현하는 것이다.",
            "③ 불리한 계약은 무조건 자산 항목의 '선급금' 계정으로 대체하여 본문 자산 총액을 인위로 늘린다.",
            "④ 거래처에 연락하여 구두로 계약을 파기하겠다고 일방 선언하고 장부에서 지출 예상액을 완전 누락한다.",
            "⑤ 회사의 세무 조사를 방해하기 위한 목적에 한해 부채를 매일 10배씩 증액 기재한다."
        ],
        "answer": "2",
        "explanation": "② 미이행계약이 유리하면 자산, 불리하면 부채의 성격을 띱니다. 특히 계약 상 회피할 수 없는 원가가 예상 효익을 초과하는 '불리한 계약(손실부담계약)'의 경우, 현재 의무가 성립되므로 부채를 부채인식기준에 맞게 인식해야 합니다.\n\n[오답 해설]\n① 불리한 계약으로 인해 현재의무가 도출되면 인식해야 합니다.\n③ 불리한 부채를 자산인 선급금으로 왜곡 표시하는 것은 오류입니다.\n④ 일방 구두 선언만으로 법적 손해배상 의무가 소멸하지 않으므로 임의 누락하면 안 됩니다.\n⑤ 세무조사 방해 등 위법 목적의 임의 증액은 회계기준에 위배됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "계약의 성격이 불리하게 변하여 현재의무가 생기면 미이행 상태라도 충당부채 인식을 검토해야 합니다.", "articles": [], "principle": "불리한 미이행계약 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "교환조건이 불리한 미이행계약(손실부담계약)은 부채 정의를 충족하여 충당부채 등으로 인식될 수 있습니다.", "articles": [], "principle": "불리한 미이행계약 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 성격 항목을 자산으로 분류 기재하는 것은 잘못입니다.", "articles": [], "principle": "불리한 미이행계약 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 의무 은폐 누락은 불허됩니다.", "articles": [], "principle": "불리한 미이행계약 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과세 관청의 눈속임을 위한 부채 증액 분개는 탈법 행위입니다.", "articles": [], "principle": "불리한 미이행계약 적용", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "P사는 보유 중인 금융자산인 채권 5,000만 원을 타사에 양도하는 계약을 체결했다. 그러나 계약 상 P사는 양수자가 원할 경우 언제든지 동일 채권을 도로 환매해 주어야 하는 무조건적 환매요구권(Put Option)을 상대방에게 부여했다. 이 조건은 상대방에게 매우 유리하여 행사 확률이 확실시된다. 채권의 제거 여부에 대한 판단으로 가장 올바른 것은?",
        "options": [
            "① 채권 양도일에 매각 대금이 유입되었으므로 즉시 채권을 장부에서 제거하고 처분손실을 인식한다.",
            "② 상대방이 풋옵션을 행사해 채권을 도로 가져올 가능성이 매우 높고 통제와 위험이 P사에 실질적 잔존하므로, 채권을 장부에서 제거할 수 없으며 받은 대금은 부채 처리한다.",
            "③ 채권의 이자수익은 상대방이 가져가므로 채권 원금의 10%만 강제 제거하고 매달 이자비용을 가산한다.",
            "④ 회사의 장부자본을 늘리기 위해 채권을 제거하고 동액만큼 무형자산인 영업권으로 가산 분개한다.",
            "⑤ 풋옵션 행사 시점까지 채권 가액을 매 보고기간 말마다 10배씩 평가 증액하는 편법을 쓴다.",
        ],
        "answer": "2",
        "explanation": "② 양수인이 무조건적 환매요구권(풋옵션)을 보유하고 행사가 유력하다면, 자산의 통제 및 관련 위험이 양도자(P사)에게 실질적으로 유보되어 있습니다. 따라서 채권을 제거해서는 안 되며 담보부 차입부채로 처리해야 합니다.\n\n[오답 해설]\n① 풋옵션 보유로 인한 통제 미이전 상태인데 매각 처리로 지우는 것은 오류입니다.\n③, ④, ⑤는 회계 이론적 타당성이 전혀 없는 임의의 가상 회계 처리 기술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상대방의 풋옵션 권리로 실질적 통제가 잔존하므로 양도 시점에 제거할 수 없습니다.", "articles": [], "principle": "풋옵션 유보와 자산 제거", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "양수인이 확실히 행사할 풋옵션을 보유하여 통제권이 이전되지 않았다면 자산을 제거할 수 없고 담보 차입부채로 처리합니다.", "articles": [], "principle": "풋옵션 유보와 자산 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원금의 일부 임의 제거 및 이자 처리는 근거가 없습니다.", "articles": [], "principle": "풋옵션 유보와 자산 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 제거 후 영업권으로 대체하여 자본을 부풀리는 행위는 분식회계입니다.", "articles": [], "principle": "풋옵션 유보와 자산 제거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "10배 임의 평가 증액 기재는 잘못된 처리입니다.", "articles": [], "principle": "풋옵션 유보와 자산 제거", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "Q사는 심각한 경영 악화로 법원으로부터 파산 선고를 받았으며, 더 이상 계속기업가정(Going Concern)을 적용하기 불가하여 청산 기준(Liquidation Basis)으로 재무제표를 작성하게 되었다. 개념체계 상 이 청산 가정 하에서의 자산 인식 및 제거 기준의 실무 변화로 가장 옳은 것은?",
        "options": [
            "① 청산 기준 하에서도 일반 계속기업의 통제 기반 인식 및 제거 규정이 한 치의 차이도 없이 유지된다.",
            "② 청산 기준에서는 미래 경제적 효익의 회수가 불가하므로, 기존의 정상적 영업 목적 자산들은 대폭 제거(감액)되거나 즉시 순실현가능가치로 전면 재측정되어 장부에 반영되어야 한다.",
            "③ 청산 가정 하에서는 모든 부채를 자산총액에 가산하여 순자산을 극대화하여 공표한다.",
            "④ 법인 해산 당일까지 재무상태표의 모든 숫자 기재를 백지로 가공 비워두고 주석만 공시한다.",
            "⑤ 회사의 잔여 재산을 대표이사가 독점적으로 가져가도록 전액 자본금 감자 처리만 매일 단행한다."
        ],
        "answer": "2",
        "explanation": "② 계속기업가정이 훼손되면 역사적 원가나 통제 목적의 계속 상각 등은 더 이상 목적적합하지 않습니다. 따라서 자산은 즉시 회수/청산 가치인 순실현가능가치 등으로 재측정되며, 효익 상실분은 대폭 감액/제거됩니다.\n\n[오답 해설]\n① 청산 시에는 인식/측정의 이론적 대전제가 달라집니다.\n③ 부채를 자산에 합산하여 순자산을 조작하는 행위는 불가합니다.\n④ 재무제표 수치를 빈칸으로 두는 것은 성실성 위배입니다.\n⑤ 대표이사 사적 취득 목적의 감자 처리는 합법적인 청산 분배 절차가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "계속기업 가정이 붕괴되면 회계 인식 및 측정의 대전제가 청산 가치 기준으로 바뀝니다.", "articles": [], "principle": "청산가정과 인식/제거 변화", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "청산 시에는 미래 영업 가치가 소멸하므로 자산들의 처분 가능 금액(순실현가치 등)으로의 조정 및 대폭 감액/제거가 동반됩니다.", "articles": [], "principle": "청산가정과 인식/제거 변화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채를 자산에 합산 표시하는 조작은 성립할 수 없습니다.", "articles": [], "principle": "청산가정과 인식/제거 변화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재무상태표 자체를 공란으로 방치할 수는 없습니다.", "articles": [], "principle": "청산가정과 인식/제거 변화", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대표이사의 사적 편취를 위한 자본 조작은 불가합니다.", "articles": [], "principle": "청산가정과 인식/제거 변화", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },

    # =========================================================================
    # L4: 분석 (8문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s07-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "개념체계 상 재무제표 요소의 '인식(Recognition)'과 '제거(Derecognition)'에 관한 설명 중 옳은 보기만을 모두 고른 것은?\n\n```\nㄱ. 인식은 요소의 정의를 충족하는 항목을 재무상태표나 재무성과표에 포착하여 포함하는 과정이다.\nㄴ. 요소의 정의를 충족하지 않는 항목이라도 정보이용자의 편의를 위해 중요성이 높다면 재무상태표 본문에 임의로 인식할 수 있다.\nㄷ. 자산은 일반적으로 보고기업이 인식한 자산의 전부 또는 일부에 대한 통제를 상실하였을 때 제거한다.\nㄹ. 부채는 기업이 해당 부채의 전부 또는 일부에 대한 현재의무를 더 이상 부담하지 않을 때 제거한다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄱ, ㄷ, ㄹ",
            "④ ㄴ, ㄷ, ㄹ",
            "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ ㄱ, ㄷ, ㄹ은 개념체계의 인식과 제거의 정의 및 자산/부채 제거 요건을 충실히 설명한 참인 서술입니다.\n\n[오답 해설]\nㄴ. 개념체계는 정의를 충족하지 않는 항목의 인식을 허용하지 않습니다. 중요성이나 이용자 편의 유무를 막론하고 재무제표 본문에 자산·부채로 기재할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ, ㄷ, ㄹ만 참입니다.", "articles": [], "principle": "인식과 제거 종합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ은 정의 미충족 항목의 인식 금지 원칙에 위배되므로 거짓입니다.", "articles": [], "principle": "인식과 제거 종합", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ(인식의 정의), ㄷ(자산 제거 요건), ㄹ(부채 제거 요건)은 모두 개념체계 상 올바른 설명입니다.", "articles": [], "principle": "인식과 제거 종합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ이 오답이므로 틀린 조합입니다.", "articles": [], "principle": "인식과 제거 종합", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ이 틀렸으므로 모두 포함될 수 없습니다.", "articles": [], "principle": "인식과 제거 종합", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "개념체계 상 인식기준 중 '목적적합성(Relevance)'에 관한 설명 중 옳지 않은 서술만을 고른 것은?\n\n```\nㄱ. 정의를 충족하는 항목이라도 그것을 인식하는 것이 항상 목적적합한 정보를 제공하는 것은 아닐 수 있다.\nㄴ. 자산이나 부채가 존재하는지 여부가 불확실한 경우(존재 불확실성), 그 존재 여부와 상관없이 무조건 단일 금액으로만 측정하여 본문에 계상하는 것이 항상 유용하다.\nㄷ. 경제적효익의 유입가능성이나 유출가능성이 매우 낮다면, 해당 항목은 어떠한 경우에도 자산이나 부채로 정의조차 성립될 수 없다.\nㄹ. 유입가능성이 낮은 경우, 발생가능한 결과의 유입/유출 크기, 시기 등을 주석에 설명하는 것이 가장 목적적합한 정보 제공일 수 있다.\n```",
        "options": [
            "① ㄱ, ㄴ",
            "② ㄴ, ㄷ",
            "③ ㄷ, ㄹ",
            "④ ㄱ, ㄷ",
            "⑤ ㄴ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② ㄴ과 ㄷ이 잘못된 서술(옳지 않은 서술)입니다.\n\n[오답 해설]\nㄴ. 존재 불확실성과 극단적 변동성이 결합되면 단일 금액 측정이 목적적합한 정보를 제공하지 못할 수 있어 본문 인식을 보류하는 것이 유용합니다.\nㄷ. 효익 유입/유출 가능성의 고저는 자산·부채 정의 성립의 필수 허들이 아닙니다. 유입가능성이 낮아도 자산의 정의를 충족하고 존재할 수 있습니다.\n(ㄱ, ㄹ은 개념체계 상 올바른 설명입니다.)",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ은 참이므로 옳지 않은 서술 고르기 대상이 아닙니다.", "articles": [], "principle": "목적적합성 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄴ(단일금액 억지 계상은 목적적합성을 해침)과 ㄷ(가능성이 낮아도 정의 충족 가능)은 둘 다 개념체계를 왜곡한 거짓 진술입니다.", "articles": [], "principle": "목적적합성 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ은 참이므로 틀린 조합입니다.", "articles": [], "principle": "목적적합성 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄱ이 참이므로 대상이 아닙니다.", "articles": [], "principle": "목적적합성 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄹ이 참이므로 잘못된 매칭입니다.", "articles": [], "principle": "목적적합성 정오 분석", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "개념체계 상 '측정불확실성(Measurement Uncertainty)'과 '표현충실성(Faithful Representation)'의 상호관계에 관한 설명 중 옳은 진술만을 모두 고른 것은?\n\n```\nㄱ. 측정을 위해 추정치를 사용하는 것은 재무정보 작성의 필수 부분이며, 정보의 유용성을 반드시 훼손하는 것은 아니다.\nㄴ. 측정불확실성의 수준이 높더라도, 그러한 추정치가 유용한 정보를 제공하지 못하는 것은 아니다.\nㄷ. 측정불확실성이 극도로 높고 설명 정보만으로는 충분히 표현충실성을 갖추기 불가능한 경우라도, 개념체계는 주석 공시 대신 무조건 장부에 인식하는 것만을 최고의 회계처리로 규정하고 있다.\n```",
        "options": [
            "① ㄱ",
            "② ㄴ",
            "③ ㄱ, ㄴ",
            "④ ㄴ, ㄷ",
            "⑤ ㄱ, ㄴ, ㄷ"
        ],
        "answer": "3",
        "explanation": "③ ㄱ과 ㄴ은 측정불확실성과 정보의 유용성에 관한 개념체계의 핵심 진술을 정확히 반영하고 있어 참입니다.\n\n[오답 해설]\nㄷ. 측정불확실성이 극도로 높고 설명 정보만으로 충실하게 나타낼 수 없는 경우에는, 본문에 인식하지 않고 주석으로만 공시하는 것이 유일하거나 최선의 대안이 될 수 있습니다. 무조건 본문 계상을 강제하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "ㄱ 외에 ㄴ도 참이므로 단독 선택은 오답입니다.", "articles": [], "principle": "측정불확실성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄴ 외에 ㄱ도 참입니다.", "articles": [], "principle": "측정불확실성 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "ㄱ(추정의 유용성)과 ㄴ(높은 불확실성과 정보 가치)은 모두 올바른 회계학적 참입니다.", "articles": [], "principle": "측정불확실성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ은 잘못된 명제입니다.", "articles": [], "principle": "측정불확실성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ㄷ이 틀린 진술이므로 전체 포함은 오답입니다.", "articles": [], "principle": "측정불확실성 분석", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "개념체계 상 자산 및 부채의 '제거(Derecognition)' 요건과 거래의 실질 반영 회계처리에 대한 설명 중 가장 올바르지 않은 서술은?",
        "options": [
            "① 제거는 기업의 재무상태표에서 인식된 자산이나 부채의 전부 또는 일부를 삭제하는 것이며, 통상 그 요소 정의를 충족하지 못하게 되었을 때 발생한다.",
            "② 법적 소유권이 타인에게 등기 이전되었다 하더라도, 자산의 모든 사용을 통제하고 경제적 효익을 향유할 실질적 권리를 보고기업이 계속 보유한다면 해당 자산을 제거해서는 안 된다.",
            "③ 부채의 제3자 인수가 약정되었더라도, 채권자의 의무 면제가 없어 현재의무를 계속 보유하고 있다면 그 부채를 재무상태표에서 제거할 수 없다.",
            "④ 금융자산을 이전하고 무조건적 환매 콜옵션을 보유하여 통제를 상실하지 않은 거래는 처분 거래로 매각 제거 처리하되, 콜옵션 평가액만 장외 파생자산으로 별도 인식하는 것이 개념체계 상 실질 묘사 원칙에 가장 잘 어울린다.",
            "⑤ 제거 회계처리는 자산 또는 부채의 이전 후에도 보고기업이 유보하고 있는 권리와 의무를 가장 충실하게 표현하는 방식으로 기재되어야 한다."
        ],
        "answer": "4",
        "explanation": "④ 콜옵션 보유로 인해 자산의 경제적 통제가 이전되지 않았다면 자산을 제거할 수 없고, 거래 전체를 금융부채(차입거래)로 처리해야 합니다. 자산을 마음대로 처분 제거한 후 옵션 가액만 잡는 것은 실질 반영을 현저히 저해하는 오처리입니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 제거 및 통제 상실 요건, 부채의 의무 소멸 여부, 그리고 실질 반영 회계의 대전제들을 정확하게 기술하고 있어 올바른 설명들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "제거의 정의와 일반적 시점 설명은 올바릅니다.", "articles": [], "principle": "제거 요건 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산의 경제적 통제 유지 시 제거 불가는 충실한 표현(실질 우선)에 부합하는 참입니다.", "articles": [], "principle": "제거 요건 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채권자 승인이 없는 부채의 제거 불가는 참입니다.", "articles": [], "principle": "제거 요건 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "환매 콜옵션 등으로 통제가 유지되면 자산을 매각 제거할 수 없으며 차입 거래로 계상하는 것이 실질 묘사에 해당하므로 4의 서술은 완전 오류입니다.", "articles": [], "principle": "제거 요건 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유보된 권리/의무의 충실한 표현 목적은 제거 회계의 정당한 지향점입니다.", "articles": [], "principle": "제거 요건 분석", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "개념체계 상 존재의 불확실성(Existence Uncertainty)과 경제적효익의 낮은 유입·유출가능성(Low Probability)에 대한 분석으로 가장 올바르지 않은 서술은?",
        "options": [
            "① 경제적효익의 유입가능성이나 유출가능성이 낮더라도 자산이나 부채가 존재할 수 있다.",
            "② 존재의 불확실성이 매우 높고 발생 가능한 배상금의 결과 범위가 예외적으로 넓은 상황이 낮은 확률과 겹쳐 있다면, 자산·부채를 단일 금액으로만 억지 측정하여 본문에 기재하는 것은 유용하지 않을 수 있다.",
            "③ 가능성이 극도로 낮은 보증의무나 파생상품 계약의 경우에도, 공정가치 등으로 정교하게 가치화할 수 있고 관련 세부 정보를 제공하는 것이 합당하다면 본문에 인식하는 것이 목적적합한 재무정보를 제공할 수 있다.",
            "④ 경제적효익의 낮은 유입/유출가능성 상태에서 가장 목적적합한 정보는 보통 유입/유출의 크기, 발생시기, 영향요인 등에 대한 정보이며, 이러한 정보는 일반적으로 주석에 기재한다.",
            "⑤ 가능성이 5% 미만인 소송 사건의 경우, 소송이 아직 종결되지 않았더라도 원고와 피고 모두 각자의 재무상태표 본문에 '미수확정소송권'이라는 임의 자산을 동액으로 강제 대칭 인식해야만 복식부기 원칙에 부합한다."
        ],
        "answer": "5",
        "explanation": "⑤ 소송 미확정 상태이고 가능성이 매우 낮은 경우에는 원고와 피고 모두 임의 자산을 대칭 계상하지 않으며, 판결 확정이나 의무 성립 요건이 구체화될 때까지 본문 인식을 차단(보류)하는 것이 개념체계에 맞습니다. 강제 대칭 인식은 회계 기준에 어긋납니다.\n\n[오답 해설]\n①, ②, ③, ④는 모두 가능성의 저하 및 존재 불확실성 하에서의 회계 처리(인식 대 주석의 배분)에 대한 개념체계 지침을 완벽하게 기술하고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "낮은 유입/유출가능성도 정의 성립을 방해하지 않는다는 기술은 참입니다.", "articles": [], "principle": "확률과 불확실성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "억지 단일금액 표기의 부적합성 지적은 정당한 참입니다.", "articles": [], "principle": "확률과 불확실성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "파생상품의 낮은 확률 공정가치 인식 타당성은 참입니다.", "articles": [], "principle": "확률과 불확실성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석 기재 사항(규모, 시기, 변수) 설명은 올바릅니다.", "articles": [], "principle": "확률과 불확실성 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "미확정 소송권을 본문에 자의적 대칭 계상하는 규정은 없으며, 개념체계의 인식기준을 정면으로 어기는 오류 명제입니다.", "articles": [], "principle": "확률과 불확실성 분석", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "개념체계 상 재무제표 인식(Recognition)의 정의와 인식기준 충족 요건에 관한 설명 중 가장 옳지 않은 것은?",
        "options": [
            "개념체계는 재무상태표에서 자산, 부채, 자본의 정의를 충족하지 않는 항목의 인식을 허용하지 않는다.",
            "수익이나 비용의 정의를 충족하는 항목만이 재무성과표에 인식될 수 있다.",
            "인식기준을 결정하는 정보의 효익 평가도 여타 의사결정과 마찬가지로 원가제약의 적용을 받는다.",
            "재무제표 요소 정의를 충족하는 임의의 항목은, 정보이용자의 요청만 결합되면 별도의 질적 검증을 생략하고 재무성과표 본문에 우선 기재하는 것이 원칙이다.",
            "어떤 경우에는 인식하기 위한 회계단위와 측정을 적용하기 위한 회계단위를 서로 다르게 선택하여 회계처리를 진행할 수도 있다."
        ],
        "answer": "4",
        "explanation": "④ 재무제표 요소 정의를 충족하는 항목이라도 항상 인식되는 것은 아닙니다. 정보이용자에게 '목적적합한 정보'와 '충실한 표현'을 모두 제공할 수 있고 원가제약을 통과할 때 비로소 인식합니다. 단순 정보이용자 요청이 있다고 질적 검증을 생략할 수는 없습니다.\n\n[오답 해설]\n①, ② 정의 미충족 시 인식 불가 원칙은 절대적입니다.\n③ 원가제약은 인식 결정의 제약요소입니다.\n⑤ 인식 회계단위와 측정 회계단위를 상이하게 선정하는 선택도 허용됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "정의 미충족 항목의 인식 불허 규정은 올바른 설명입니다.", "articles": [], "principle": "인식 요건 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정의 충족 수익/비용만 인식 가능하다는 서술은 참입니다.", "articles": [], "principle": "인식 요건 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인식에도 원가제약이 적용됨은 올바른 참 서술입니다.", "articles": [], "principle": "인식 요건 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "정의 충족 요소라도 목적적합성, 표현충실성, 원가제약을 충족할 때 비로소 인식하므로 지문의 기재 원칙 서술은 허구입니다.", "articles": [], "principle": "인식 요건 정오 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인식과 측정의 회계단위를 다르게 설정할 수 있음은 개념체계 상 가능하도록 명시되어 있습니다.", "articles": [], "principle": "인식 요건 정오 분석", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "개념체계 상 자산의 제거 시 통제 상실 여부와 관련 거래의 계약상 권리·의무의 실질 반영에 대한 설명 중 가장 옳지 않은 것은?",
        "options": [
            "① 자산의 실질적 통제가 타인에게 완전히 양도되지 않았음에도, 법적 서류 양식을 이유로 자산을 조기 제거하는 기재는 표현충실성을 왜곡한 것이다.",
            "② 조건부 매각이나 옵션 보유 거래처럼 자산의 통제가 부분적으로만 상실된 경우, 이전된 부문만 제거하고 유보된 부문은 계속 자산으로 유지하는 회계설계가 필요할 수 있다.",
            "③ 계약의 조건이 보고기업의 권리와 의무에 미치는 영향이 미미하고 실질적인 영향력이 없는 무의미한 조항이라면, 해당 조항은 실질이 없으므로 회계 제거 판단 시 무시해야 한다.",
            "④ 금융자산을 팩토링 거래를 통해 양수자에게 명의 이전하고, 동시에 양수인이 자산의 반환을 요구할 경우 이에 응해야 하는 강제 의무가 매도인에게 유보되어 있다면 매각 제거 분개가 타당하다.",
            "⑤ 제거 회계처리는 자산 이전 전후로 보고기업에 귀속되는 총자산과 총부채의 상태 변화를 정확하게 나타내는 것을 기본 원칙으로 한다."
        ],
        "answer": "4",
        "explanation": "④ 양수인이 반환 요구 권리를 가지고 있고 매도인에게 무조건적 환매(반환) 의무가 유보되어 있다면, 자산에 대한 통제권과 경제적 위험이 사실상 매도자에게 잔류합니다. 따라서 매각 제거 처리를 할 수 없고 금융부채 담보차입 거래로 회계처리해야 합니다.\n\n[오답 해설]\n① 법적 형식보다 경제적 실질이 우선합니다.\n② 부분 통제 상실 시 일부 제거 및 잔여분 유지 모델이 활용될 수 있습니다.\n③ 영향력이 결여된 실질 없는 조건은 판단 시 무시하는 것이 충실한 표현입니다.\n⑤ 이전 전후의 실질적 재무 상태 변화를 나타내야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "실질 통제가 귀속되는데 자산을 강제 조기 제거하는 행위는 왜곡입니다.", "articles": [], "principle": "제거와 계약의 실질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부분 통제 상실에 대한 점진적 또는 부분적 제거/유보 설계는 유용합니다.", "articles": [], "principle": "제거와 계약의 실질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실질이 결여된 가공의 계약 조항 무시는 개념체계에 합치됩니다.", "articles": [], "principle": "제거와 계약의 실질", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "양수자의 반환권과 매도자의 반환의무(환매의무)가 결합되어 있다면 통제가 상실되지 않았으므로 매각 처리가 불가능합니다.", "articles": [], "principle": "제거와 계약의 실질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이전 거래 전후의 자산부채 변화 묘사는 제거 회계의 타당한 목적입니다.", "articles": [], "principle": "제거와 계약의 실질", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "개념체계 상 재무보고에 가해지는 '원가제약(Cost Constraint)'과 특정 항목의 본문 인식 및 주석 공시의 배분 원칙에 대한 설명 중 가장 올바르지 않은 것은?",
        "options": [
            "① 특정 자산이나 부채의 목적적합한 측정을 위해 보고서 작성자가 부담해야 하는 정보 산출 원가는 인식 여부를 가르는 실질적 허들이 된다.",
            "② 재무제표이용자도 기업이 보고한 복잡한 추정 수치나 불확실성 정보를 분석하고 해석하기 위해 분석 전문가 고용 원가 등의 원가를 직간접적으로 부담한다.",
            "③ 제공되는 재무정보의 효익이 그 정보를 작성하고 분석하는 데 소요되는 사회적 원가를 정당화할 때에만 비로소 해당 요소를 본문에 인식해야 한다.",
            "④ 원가제약이 과도하다면, 비록 본문 인식 대상 항목이라도 인식을 보류하고 원가가 현저히 낮게 소요되는 간략화된 주석 공시 등으로 대체하는 것이 최선의 정보 유용성 보전 방책일 수 있다.",
            "⑤ 회사의 장부 관리 편의를 위하여 원가제약이 없는 대형 현금 거래는 장부에 일체 분개하지 않고 주석 기재도 생략하는 방침이 투명성 제고를 위해 인정된다."
        ],
        "answer": "5",
        "explanation": "⑤ 대형 현금 거래와 같이 기업의 정상적인 영업 거래는 측정불확실성이 없고 자산의 통제 및 유출입이 명확하므로, 원가제약을 이유로 장부 분개와 주석 기재를 임의로 누락할 수 없습니다. 이는 분식회계이자 회계부정입니다.\n\n[오답 해설]\n①, ②, ③, ④는 인식 단계에 미치는 원가제약의 개념적 지위, 작성자와 정보 이용자 쌍방이 부담하는 비용, 그리고 이로 인해 본문 인식 대신 간소화된 보고(주석)로 대체될 수 있는 정당한 예외 조항들을 개념체계의 목적에 맞춰 성실하게 상술하고 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "정보작성자의 비용 부담이 인식을 제한한다는 설명은 정당한 사실입니다.", "articles": [], "principle": "원가제약과 공시배분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이용자의 분석 원가 부담 지적도 개념체계 상의 원가제약 기술 내용입니다.", "articles": [], "principle": "원가제약과 공시배분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "효익이 비용을 초과할 때의 인식 원칙은 참입니다.", "articles": [], "principle": "원가제약과 공시배분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과도한 측정 원가 상황에서 미인식 및 주석 대체 방안은 유효한 회계적 대안입니다.", "articles": [], "principle": "원가제약과 공시배분", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "명확한 대형 실물 현금 거래의 임의 누락 방침은 회계기준 및 세법을 전면 어기는 횡령/오류 조장 서술이므로 오류입니다.", "articles": [], "principle": "원가제약과 공시배분", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },

    # =========================================================================
    # L5: 심화 (2문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s07-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "금융자산 등 다양한 자산의 제거(Derecognition) 회계처리 모델 설계 시, 개념체계가 '통제접근법(Control Approach)'을 기초로 하면서 발생할 수 있는 거래의 실질 묘사 및 '위험-보상접근법(Risk-and-Reward Approach)'과의 비교 분석에 대한 설명으로 가장 옳지 않은 것은?",
        "options": [
            "① 통제접근법은 기업이 자산의 사용을 지시하고 그로부터 생기는 효익을 얻는 능력을 상실했는지를 기준 삼아 제거 여부를 결정한다.",
            "② 위험-보상접근법은 자산과 관련된 소유에 따른 위험(예: 신용위험)과 보상의 대부분이 타인에게 이전되었는가를 제거 기준으로 설정한다.",
            "③ 현행 개념체계 상 자산의 본질이 '통제'에 있으므로, 자산의 제거 결정 역시 통제 상실 여부를 추적하는 통제접근법이 논리적으로 일관된다.",
            "④ 통제접근법 하에서는 이전 후 잔존하는 일부 위험(소구의무 등)이 부채의 정의를 만족할 경우 자산을 제거하는 동시에 새로운 보증부채를 별도로 잡을 수 있는 반면, 위험-보상접근법 하에서는 위험이 남았다면 자산 전체를 제거하지 않는 처리가 흔히 유도된다.",
            "⑤ 통제접근법은 법률적 명의 이전만을 절대적 기준선으로 채택하고 경제적 사용 권한의 변화를 무시하기 때문에, 소유와 경영이 분리된 현대 주식회사 제도의 거래 실질을 전혀 표현하지 못한다는 태생적 비판이 있으며 이로 인해 현행 기준서에서 완전 배제되었다."
        ],
        "answer": "5",
        "explanation": "⑤ 현행 개념체계 및 많은 IFRS 기준서들은 '통제(Control)'를 자산의 핵심 정의이자 제거 기준으로 두고 있습니다. 통제는 단순 법적 등기 이전뿐 아니라 자산의 사용을 지시하고 효익을 얻는 능력을 포괄하는 실질주의 접근법입니다. 따라서 법적 명의만을 맹종하여 기준서에서 완전 배제되었다는 설명은 사실과 전혀 다릅니다.\n\n[오답 해설]\n① 통제접근법의 올바른 의의입니다.\n② 위험-보상접근법의 전형적인 판단 기준입니다.\n③ 개념체계 상 자산 정의(통제하는 경제적 자원)와 제거 논리의 일관성에 대한 타당한 서술입니다.\n④ 통제접근법은 권리/의무의 다차원적 분할 인식(일부 제거 + 부채 신설)에 기여하는 반면, 위험-보상접근법은 올-오어-낫싱(All-or-Nothing) 형태의 전체 제거 유무 판단으로 귀결되기 쉬운 차이가 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "통제접근법의 일반적인 정의로 참입니다.", "articles": [], "principle": "통제접근법 vs 위험보상접근법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "위험-보상접근법의 기본 요건에 관한 참입니다.", "articles": [], "principle": "통제접근법 vs 위험보상접근법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산의 본질적 정의인 '통제'와 제거 요건의 일관성 연결은 타당한 회계학적 지적입니다.", "articles": [], "principle": "통제접근법 vs 위험보상접근법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "두 모형 간의 실무적 분개 방식(부분 제거/보증 계상 대 총액 제거 유보) 차이에 관한 심도 있는 정당한 설명입니다.", "articles": [], "principle": "통제접근법 vs 위험보상접근법", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "개념체계 및 회계기준서는 통제접근법을 핵심 축으로 사용하고 있으며 법적 명의만을 맹종하지도 배제하지도 않았으므로 5는 완벽히 잘못된 명제입니다.", "articles": [], "principle": "통제접근법 vs 위험보상접근법", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
            }
        }
    },
    {
        "id": "practice-accounting-ch01s07-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "개념체계 상 재무제표 요소 인식 시 발생하는 '측정불확실성(Measurement Uncertainty)'의 성격과 정보의 두 근본적 질적 특성인 '목적적합성(Relevance)' 및 '표현충실성(Faithful Representation)' 간의 조화(Trade-off 및 절충적 관점)에 대한 설명으로 가장 올바르지 않은 서술은?",
        "options": [
            "① 추정치 사용에 따른 측정불확실성은 목적적합한 측정 기준을 적용하기 위한 불가피한 대가인 경우가 많으며, 추정 가정이 합리적이라면 정보 유용성이 유지된다.",
            "② 표현충실성을 달성하기 위해 선택된 측정치가 고도의 측정불확실성을 내포하고 있다면, 비록 그 정보가 의사결정에 매우 목적적합하더라도 경우에 따라서는 해당 자산·부채의 본문 인식을 차단(미인식)하는 것이 유일하거나 최선의 대안이 될 수 있다.",
            "③ 본문에 자산을 인식하지 않고 주석으로만 공시하기로 결정했다면, 이는 자산의 정의를 미충족하기 때문일 수도 있지만, 측정불확실성이 너무 높아 주석 공시를 결합하더라도 자산 상태의 충실한 표현을 본문 기재를 통해서는 제공할 수 없다는 판단에 기인할 수도 있다.",
            "④ 측정불확실성이 매우 높은 자산(예: 개발 중인 특허 가치 등)을 장부에 고액으로 인식하는 것은 목적적합성을 극대화하지만 표현충실성을 훼손하므로, 이러한 상충 시에는 무조건 '역사적 원가'를 0원으로 고정하고 주석마저 완전 누락하는 것이 개념체계의 절충안이다.",
            "⑤ 높은 수준의 측정불확실성이 재무정보의 유용성을 반드시 손상시키는 것은 아니며, 높은 불확실성을 가진 추정치라도 다른 대안적 측정치보다 더 유용한 의사결정 정보를 제공한다면 해당 요소는 인식될 수 있다."
        ],
        "answer": "4",
        "explanation": "④ 측정불확실성이 고도로 높을 때, 본문 인식은 보류하되 주석(설명 정보)을 기재하여 이용자의 이해를 도와야 합니다. 무조건 원가를 0원으로 고정한 후 주석마저 은폐하라는 것은 투명한 공시 및 개념체계 상의 절충 방식과 정면 배치됩니다.\n\n[오답 해설]\n① 추정과 유용성의 상호 보완성 설명은 참입니다.\n② 측정불확실성이 너무 크면 본문 미인식이 최선일 수 있다는 명제는 참입니다.\n③ 미인식 결정이 단순히 정의 미충족뿐 아니라 표현충실성(측정의 난해함 및 불명확성) 실패에 기인할 수 있다는 서술은 매우 정교하고 정당한 개념체계 분석입니다.\n⑤ 불확실성이 높은 추정치라도 다른 대안보다 의사결정에 기여(목적적합)한다면 인식 대상이 될 수 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "추정치의 타당성과 유용성 논리는 개념체계에 합치되는 참입니다.", "articles": [], "principle": "측정불확실성과 질적특성 상충", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "극심한 불확실성 하에서의 본문 인식 배제가 유효한 대안이라는 지적은 올바른 설명입니다.", "articles": [], "principle": "측정불확실성과 질적특성 상충", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주석 기재와 본문 배정의 의사결정 동기 분석(정의 미충족 vs 표현충실성 한계)은 참입니다.", "articles": [], "principle": "측정불확실성과 질적특성 상충", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "불확실성 상충 시 주석마저 강제로 누락하고 0원 기재하라는 설명은 개념체계의 투명한 정보 공시 절차와 일탈되는 명백한 가공 거짓 진술입니다.", "articles": [], "principle": "측정불확실성과 질적특성 상충", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대안 측정치 중 유용한 의사결정 정보를 준다면 높은 불확실성을 감수하고 인식할 수 있다는 이론적 설명은 참입니다.", "articles": [], "principle": "측정불확실성과 질적특성 상충", "case": {"holding": "", "no": None}}
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
                "item": "7절 인식과 제거"
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
