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
        "id": "practice-accounting-ch01s03-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "일반목적재무보고의 근본적인 목적에 관한 설명으로 가장 올바른 것은?",
        "options": [
          "① 기업의 내부 경영진이 일일 경영 전략을 수립하는 데 필요한 기밀 정보를 제공한다.",
          "② 현재 및 잠재적 투자자, 대여자 및 기타 채권자가 기업에 자원을 제공하는 의사결정을 할 때 유용한 정보를 제공한다.",
          "③ 국세청이 정확한 세무조사를 수행하여 즉시 세금을 부과하도록 돕는다.",
          "④ 기업의 인수합병 시장가치를 소수점 단위까지 정확하게 계산해 명시한다.",
          "⑤ 기업의 주가 조작 시도를 사전에 감시하여 강제 구속하는 사법적 효력을 낸다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고의 근본적 목적은 현재 및 잠재적 투자자, 대여자 및 기타 채권자가 기업에 자원을 제공하는 것과 관련된 의사결정을 할 때 유용한 보고기업 재무정보를 제공하는 것입니다.\n\n[오답 해설]\n① 경영진은 내부에서 직접 정보를 획득하므로 일반목적보고의 최우선 대상이 아닙니다.\n③ 세제 징수 목적이 아닙니다.\n④ 기업 가치를 직접 보여주기 위해 고안되지 않았습니다.\n⑤ 사법적 권한이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "경영진의 내부 의사결정이 근본 목적이 아닙니다.", "articles": [], "principle": "재무보고 목적", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "현재 및 잠재적 투자자, 대여자, 기타 채권자에게 유용한 정보를 제공하는 것이 목적입니다.", "articles": [], "principle": "재무보고 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세법 과세 목적이 아닙니다.", "articles": [], "principle": "세법", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "시장가치를 계산해 제공하지 않습니다.", "articles": [], "principle": "가치 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사법권이 존재하지 않습니다.", "articles": [], "principle": "사법부", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "일반목적재무보고서의 혜택을 받는 '주요 이용자(Primary Users)'에 해당하는 당사자는?",
        "options": [
          "① 기업의 현직 CEO 및 이사회 임원",
          "② 해당 기업을 감사하는 외부감사인",
          "③ 현재 및 잠재적 투자자, 대여자 및 기타 채권자",
          "④ 기획재정부 법인세제과 담당 공무원",
          "⑤ 기업의 영업활동을 정기 모니터링하는 일반 시민단체"
        ],
        "answer": "3",
        "explanation": "③ 개념체계 상 일반목적재무보고서의 대상이 되는 주요 이용자는 기업에 직접 정보를 요구할 권한이 없는 '현재 및 잠재적 투자자, 대여자 및 기타 채권자'입니다.\n\n[오답 해설]\n① 경영진은 내부 정보를 얻으므로 제외됩니다.\n②, ④, ⑤ 감사인, 세무당국, 시민단체 등은 주요이용자 범위에 속하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "경영진은 주요이용자에서 제외됩니다.", "articles": [], "principle": "주요이용자 제외", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "외부감사인은 주요이용자가 아닙니다.", "articles": [], "principle": "주요이용자 제외", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "현재 및 잠재적 투자자, 대여자, 기타 채권자가 주요이용자입니다.", "articles": [], "principle": "주요이용자 정의", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무당국은 주요이용자가 아닙니다.", "articles": [], "principle": "주요이용자 제외", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "시민단체는 주요이용자가 아닙니다.", "articles": [], "principle": "주요이용자 제외", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "일반목적재무보고서와 보고기업 경영진(Management)의 정보 획득 지위에 관한 설명으로 옳은 것은?",
        "options": [
          "① 경영진은 일반목적재무보고서의 최우선 주요이용자이다.",
          "② 경영진은 회사 내부에서 정보를 직접 입수하므로 일반목적재무보고서에 전적으로 의존할 필요가 없다.",
          "③ 경영진이 요구하는 정성 데이터를 제공하기 위해 재무보고서는 분기별로 소급 재작성되어야 한다.",
          "④ 경영진은 재무제표의 오류 신뢰성을 파악하기 위해 외부 보고서가 공표될 때까지 의사결정을 보류한다.",
          "⑤ 경영진이 재무제표의 오류를 유발하더라도 감사인은 이에 대해 수정 지시할 수 없다."
        ],
        "answer": "2",
        "explanation": "② 보고기업 경영진도 재무 정보에 관심이 있으나, 경영진은 필요로 하는 정보를 내부에서 구할 수 있으므로 일반목적재무보고서에 의존할 필요가 없습니다. 따라서 주요 이용자에서 제외됩니다.\n\n[오답 해설]\n① 주요이용자 범위에서 경영진은 제외됩니다.\n③ 경영진 전용 정성 데이터 반영 소급 작성을 하지 않습니다.\n④ 경영진은 내부 상태를 실시간 파악하므로 공표를 기다리지 않습니다.\n⑤ 감사인은 오류 지적 권한을 가집니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "경영진은 주요이용자가 아닙니다.", "articles": [], "principle": "주요이용자", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "경영진은 내부 정보 입수가 가능하므로 재무보고서에 의존하지 않습니다.", "articles": [], "principle": "경영진 정보성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "경영진용 보고서로 별도 소급하지 않습니다.", "articles": [], "principle": "보고서 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "경영진은 실시간 파악이 가능합니다.", "articles": [], "principle": "내부 통제", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사인의 오류 지적 권한은 있습니다.", "articles": [], "principle": "감사 권한", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "일반목적재무보고서의 태생적 한계에 대한 설명 중 옳은 것은?",
        "options": [
          "① 주요이용자가 필요로 하는 모든 정보를 완벽하게 제공하지는 못하며 제공할 수도 없다.",
          "② 재무보고서는 시장 참여자의 주관적 리스크를 완전히 소멸시켜 100% 안전한 투자를 가능케 한다.",
          "③ 주총 3분의 2 동의가 없으면 대외 공시가 법적으로 영구 금지되는 한계가 있다.",
          "④ 보고서의 정보는 오직 과거의 역사적 사건만을 기재해야 하므로 미래 예측 가치를 전혀 갖지 못한다.",
          "⑤ 단기적인 세무 과세 표준을 탕감해 주는 사법 조항을 담지 못하는 법률적 한계가 있다."
        ],
        "answer": "1",
        "explanation": "① 일반목적재무보고서는 주요이용자가 필요로 하는 모든 정보를 제공하지 않으며 제공할 수도 없음을 개념체계는 정직하게 밝히고 있습니다.\n\n[오답 해설]\n② 리스크를 100% 소멸시킬 수는 없습니다.\n③ 주총 의결과 관련 없이 상장 법인은 정기적으로 투명하게 공시할 의무가 있습니다.\n④ 과거 사건에 대한 정보는 정보이용자의 미래 예측(예측가치)에 훌륭한 입력치가 됩니다.\n⑤ 세법 조세 탕감을 결정하는 법률 문서가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "재무보고서는 이용자가 요구하는 모든 유용한 정보를 제공하지 못하는 태생적 한계가 존재합니다.", "articles": [], "principle": "재무보고서의 한계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "투자의 안전성을 전면 보장하지 못합니다.", "articles": [], "principle": "투자 리스크", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주총 의결과 무관하게 공시 의무가 있습니다.", "articles": [], "principle": "공시 요건", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "미래 예측을 돕는 유용한 예측가치를 지닙니다.", "articles": [], "principle": "예측 가치", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세법 적용 대상 법률서가 아닙니다.", "articles": [], "principle": "법적 한계", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "일반목적재무보고서와 보고기업의 가치평가(Valuation)에 관한 개념체계의 설명으로 옳은 것은?",
        "options": [
          "① 재무보고서는 기업의 기말 시장 가치를 직접 계산하여 정확하게 보여준다.",
          "② 재무보고서는 보고기업의 가치를 보여주기 위해 고안된 것이 아니다.",
          "③ 재무보고서는 기업 가치 평가를 최종 목표로 삼으며 그 외의 정보는 생략한다.",
          "④ 장부상 자본 총계와 시가총액의 불일치는 회계담당자의 명백한 분식회계 죄가 성립한다.",
          "⑤ 개념체계는 주식 시장의 모든 가치 평가액을 위원회가 통제하도록 규정한다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고서는 보고기업의 가치를 보여주기 위해 고안된 것이 아닙니다. 그러나 주요이용자가 가치를 스스로 추정하는 데 도움이 되는 핵심 정보를 풍부하게 제공합니다.\n\n[오답 해설]\n① 직접 가치를 계산해 제공하지 않습니다.\n③ 기업 가치 평가가 최종 목표가 아닙니다.\n④ 순자산 장부액과 시가의 불일치는 회계의 오류나 죄가 아닌 역사적 원가주의 및 보수주의 적용에 따른 정상적 차이입니다.\n⑤ 시장의 평가액을 위원회가 통제하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "가치를 직접 계산하여 명시하지 않습니다.", "articles": [], "principle": "가치평가 한계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 기업 가치를 직접 보여주기 위해 고안된 것이 아닙니다.", "articles": [], "principle": "가치평가 목적의 부재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "가치 평가가 단독 목적이 아닙니다.", "articles": [], "principle": "재무보고 목적", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "시가와의 차이는 회계 오류나 죄가 아닙니다.", "articles": [], "principle": "회계 가치 괴리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "시장의 평가액을 위원회가 통제하지 못합니다.", "articles": [], "principle": "시장 통제 불가", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "재무보고서의 정확성(Accuracy)과 작성 기법의 본질에 대한 개념체계의 올바른 진술은?",
        "options": [
          "① 재무보고서는 100% 오류 없는 절대적인 수리적 정확한 서술만을 수록해야 한다.",
          "② 재무보고서는 정확한 서술보다는 상당 부분 추정, 판단 및 모형에 근거한다.",
          "③ 개념체계는 추정과 판단의 사용을 불법으로 엄격히 규율하여 배척한다.",
          "④ 모형과 추정을 사용한 재무제표는 감사 보고서 상 의견거절 대상이다.",
          "⑤ 추정치 기재를 면제받기 위해 자산 거래는 오직 현금 결제 분만 기재한다."
        ],
        "answer": "2",
        "explanation": "② 재무보고서는 주관적이고 객관적인 미래 가치 평가나 충당 설정 등이 동반되므로 정확한 서술보다는 상당 부분 추정, 판단 및 모형에 근거하여 작성됩니다.\n\n[오답 해설]\n① 절대 오류 없는 정확한 서술로만 구성되는 것은 불가능합니다.\n③ 추정치 사용은 재무제표 작성에 필수적인 정상적 과정입니다.\n④ 추정을 합리적으로 반영한 장부는 당연히 적정 의견 대상입니다.\n⑤ 발생주의 준수를 위해 미결제 거래도 의무적으로 자산 부채로 기재합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "절대적 정확한 서술로만 채울 수는 없습니다.", "articles": [], "principle": "정확성의 성격", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 상당 부분 추정, 판단 및 모형에 근거하여 작성됩니다.", "articles": [], "principle": "추정 판단의 적극 개입", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "추정 사용은 지극히 정당한 합법적 기법입니다.", "articles": [], "principle": "추정의 정당성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "의견거절 사유가 될 수 없습니다.", "articles": [], "principle": "감사 의견", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "현금주의로 대체할 수 없습니다.", "articles": [], "principle": "발생주의 준수", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "일반목적재무보고서가 보고기업의 재무상태(Financial Position)에 관하여 기본 제공하는 정보 영역은?",
        "options": [
          "① 기업 경영진의 연도별 사적 소득 지출 명세",
          "② 기업의 경제적자원 및 보고기업에 대한 청구권에 관한 정보",
          "③ 경쟁사 임직원들의 개인 신용 정보 및 연봉 데이터",
          "④ 당해 지역의 부동산 시가총액 평균 등 거시 통계 데이터",
          "⑤ 세무 세무조사에서 감면받은 세액의 누계액 수치"
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고서는 보고기업의 재무상태에 관한 정보, 즉 기업의 경제적 자원 및 보고기업에 대한 청구권(부채와 자본)에 관한 정보(재무상태표 항목)를 공시합니다.\n\n[오답 해설]\n① 경영진 개인의 사적 소득 지출을 기재하지 않습니다.\n③ 경쟁사 임직원의 개인 신용 데이터는 공시 대상이 아닙니다.\n④ 당해 지역 거시 부동산 시가 자료를 담지 않습니다.\n⑤ 세무 감면 세액의 누계 등을 단독 재무상태 정보로 수록하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "경영진 사적 정보는 제외됩니다.", "articles": [], "principle": "사적 정보 배제", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기업의 경제적 자원(자산) 및 청구권(부채, 자본) 정보가 재무상태 정보의 본질입니다.", "articles": [], "principle": "재무상태 제공 정보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "경쟁사 정보는 수록하지 않습니다.", "articles": [], "principle": "경쟁 정보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "거시 통계 지표와 무관합니다.", "articles": [], "principle": "거시 통계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 감면 누계는 본질 정보가 아닙니다.", "articles": [], "principle": "세무 정보", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "보고기업의 경제적자원 및 청구권을 변동시키는 두 가지 근본 사유를 올바르게 연결한 것은?",
        "options": [
          "① 기업의 당기순이익에 따른 재무성과, 그리고 지분/채무 발행 등 재무성과 외의 거래",
          "② 국세청의 세금 징수, 그리고 감사위원회의 소송 제기",
          "③ 주식시장의 종합주가지수 변동, 그리고 거시 환율 인하 정책",
          "④ 기업 회계사의 개인적 급여 인상, 그리고 기계장치 폐기 처분",
          "⑤ 외부 감사인의 감사 수수료 인상, 그리고 경쟁사 부도 사건"
        ],
        "answer": "1",
        "explanation": "① 보고기업의 자원 및 청구권의 변동은 '그 기업의 재무성과', 그리고 '채무상품이나 지분상품의 발행(재무성과 외의 거래)' 등 두 가지 원천 경로를 통해 발생합니다.\n\n[오답 해설]\n② 세금 징수나 소송 제기 단독을 변동 원천의 2대 경로로 기술하지 않습니다.\n③ 거시 주가지수나 환율 등은 기업 외부의 시장 변수입니다.\n④, ⑤ 회계사 연봉 인상이나 감사 수수료 인상 등은 부분적 비용일 뿐 원천 분류에 해당하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "재무성과에 따른 변동과 재무성과 외의 사건(자본 거래 등)에 따른 변동이 2대 사유입니다.", "articles": [], "principle": "자원 변동의 구분", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "소송 단독이 변동 2대 사유가 아닙니다.", "articles": [], "principle": "변동 사유", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "거시 지표는 외부 환경 요인입니다.", "articles": [], "principle": "거시 환경", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "개별 직원의 급여 인상 등은 작은 미시 요인입니다.", "articles": [], "principle": "미시 비용", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사 수수료 변경 등은 작은 요인입니다.", "articles": [], "principle": "감사 비용", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "개념체계가 명시하는 발생주의 회계(Accrual Accounting)의 가장 근본적인 지침 서술은?",
        "options": [
          "① 현금의 실제 수취와 지급이 완료된 바로 그날에만 장부에 기재한다.",
          "② 거래와 사건의 영향이 발생한 기간에 보여주며, 현금 수취와 지급 시점이 다른 기간에 이루어지더라도 해당 사건 발생 기간에 반영한다.",
          "③ 발생주의 회계는 자의성이 높으므로 감사 보고서 한정 의견 대상이다.",
          "④ 현금거래가 발생하기 전에는 어떠한 장기 미결제 거래도 장부 기록을 법적으로 차단한다.",
          "⑤ 발생주의는 오직 세법 상의 법인세를 줄이기 위한 목적으로만 가변적으로 허용된다."
        ],
        "answer": "2",
        "explanation": "② 발생기준 회계는 거래와 사건의 영향을 현금 수수와 상관없이 그 영향이 발생한 기간에 장부에 표시하여 성과 평가의 타당성을 높이는 회계 방식입니다.\n\n[오답 해설]\n① 현금주의에 대한 설명이므로 틀렸습니다.\n③ 발생주의는 국제 회계의 기본 의무 기준입니다.\n④ 현금 거래 전에도 외상 매출/매입 등을 적법하게 인식합니다.\n⑤ 조세 회피 전용 지침이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "현금주의에 대한 오독 지문입니다.", "articles": [], "principle": "현금주의", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "발생주의는 현금 수수와 무관하게 사건의 영향이 발생한 기간에 회계 처리합니다.", "articles": [], "principle": "발생주의 정의", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기본 의무 기준이므로 한정 사유가 아닙니다.", "articles": [], "principle": "회계 적정성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "외상 거래 인식도 당연히 허용됩니다.", "articles": [], "principle": "미결제 거래", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "조세 피 목적의 가변적 규칙이 아닙니다.", "articles": [], "principle": "세금", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "일반목적재무보고서 상의 '과거현금흐름(Past Cash Flows)' 정보가 정보이용자에게 기여하는 공식적인 유용성은?",
        "options": [
          "① 기업의 기말 당기순이익이 100% 현금으로 금고에 보관되어 있음을 영구 입증한다.",
          "② 이용자가 기업의 미래 순현금유입 창출 능력을 평가하고 경영진의 수탁책임이 적정했는지 분석하는 데 도움을 준다.",
          "③ 발생주의 회계를 완전 배제하고 현금주의로 장부를 강제 단일화하는 근거를 이룬다.",
          "④ 기업 소유 부동산의 시장 평가 가격을 즉각 감정평가하여 보여준다.",
          "⑤ 단기적인 세금 면제 액수를 국세청이 지정하도록 유도한다."
        ],
        "answer": "2",
        "explanation": "② 한 기간의 현금흐름 정보는 정보이용자가 기업의 미래 순현금유입 창출 능력을 평가하고, 경제적 자원에 대한 경영진의 수탁책임을 평가하는 데 도움을 줍니다.\n\n[오답 해설]\n① 당기순이익이 전액 현금 보유됨을 보장하지 않습니다.\n③ 발생주의를 폐기 배제하지 않고 상호보완적으로 운영됩니다.\n④ 부동산 감정평가액을 직접 도출하지 못합니다.\n⑤ 세금 면제 조항 지정과 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "이익의 현금 보관을 입증하지 못합니다.", "articles": [], "principle": "현금화 리스크", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "미래 현금유입 창출력 평가 및 경영진 수탁책임 감시에 기여합니다.", "articles": [], "principle": "과거 현금흐름의 의의", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "발생주의를 배제하지 않습니다.", "articles": [], "principle": "상호보완성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "부동산 시가 평가액 도출과 무관합니다.", "articles": [], "principle": "감정 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세금 면제 지정과 무관합니다.", "articles": [], "principle": "세금", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },

    # =========================================================================
    # L2: 이해 수준 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s03-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "일반목적재무보고의 '주요 이용자'가 보고기업에 직접 정보를 요구할 수 없다는 사실이 일반목적재무보고의 존재 의의에 미치는 영향으로 가장 타당한 설명은?",
        "options": [
          "① 주요이용자는 직접 조사를 진행할 수 있으므로 보고서의 존재 의의가 단기 상실된다.",
          "② 주요이용자가 필요로 하는 정보의 많은 부분을 일반목적재무보고서에 의존해야만 하므로, 보고서의 작성 및 투명한 공시가 필수적이고 타당하다.",
          "③ 작성자는 주요이용자에게 기말 보고서 대신 사적 메시지로 정보를 개별 발송하고 비용을 절감한다.",
          "④ 해당 의존성으로 인해 재무보고서는 상법 상 불법 정보 독점 혐의의 강제 조사 대상이 된다.",
          "⑤ 주요이용자의 직접 질의가 금지되므로, 작성자는 보고서의 내용을 임의 축소 은폐하여 마감한다."
        ],
        "answer": "2",
        "explanation": "② 현재 및 잠재적 투자자 등 주요 이용자들은 보고기업에 정보를 직접 요구할 권한이 거의 없으므로, 공시되는 일반목적재무보고서에 크게 의존합니다. 이것이 보고서의 강력한 존재 의의를 이룹니다.\n\n[오답 해설]\n① 주요이용자에게 기업 내부 직접 조사 권한이 존재하지 않습니다.\n③ 사적 메시지를 통한 차별적 정보 발송은 공평 공시 위반입니다.\n④ 불법 독점 혐의 조사 대상 사유가 아닙니다.\n⑤ 정보 의존성이 높으므로 은폐 기재를 해서는 절대 안 됩니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "직접 조사 권한이 주요이용자에게 없습니다.", "articles": [], "principle": "이용자 권한", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "이용자들이 정보를 자발적으로 구할 수 없으므로 일반목적보고서에 의존한다는 지문은 완전히 옳습니다.", "articles": [], "principle": "정보 의존성과 재무보고", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사적 발송은 공평 공시 위반입니다.", "articles": [], "principle": "공평 공시", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "불법 혐의 대상이 되지 않습니다.", "articles": [], "principle": "법적 유효성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "의존성이 높으므로 은폐 기재는 위법입니다.", "articles": [], "principle": "공시 의무", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "일반 대중(General Public)이나 정부 규제기관 등이 일반목적재무보고서를 유용하게 여길 수 있음에도 불구하고, 개념체계가 이들을 '주요 이용자' 범위로 지정하지 않은 올바른 논리적 배경은?",
        "options": [
          "① 일반 대중은 주식을 거래할 금융 자산이 전혀 없다고 가정하기 때문이다.",
          "② 규제당국은 법적 권한에 근거하여 기업에게 필요한 개별 세무/행정 정보를 직접 강제 요구하여 획득할 수 있으므로, 외부보고용 재무보고서에만 전적으로 의존하는 당사자가 아니기 때문이다.",
          "③ 대중이나 규제기관이 재무보고서를 읽으면 정보의 왜곡 유출 리스크가 무조건 발생하기 때문이다.",
          "④ 위원회가 일반 대중을 시장 참여자로 아예 배척하려는 장기 비밀 정책을 수립했기 때문이다.",
          "⑤ 이들이 주요이용자가 되면 기업 법인세가 영구 상향 조정되는 불이익이 있기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 규제당국이나 정부 과세관청 등은 세법이나 관련 법령에 의거하여 기업에 필요한 특수 정보를 직접 요구할 강제적 권한이 있습니다. 반면 일반 투자자들은 그러한 권한이 없어 보고서에만 의존하므로 투자자들만을 주요이용자로 지정해 공통 수요를 맞춥니다.\n\n[오답 해설]\n① 대중 중에도 많은 투자자가 금융 자산을 보유하므로 가정이 틀렸습니다.\n③ 정보 유출 리스크를 이유로 범위에서 배제하지 않습니다.\n④ 일반 대중을 악의적으로 배척하려 설계하지 않았습니다.\n⑤ 법인세 상향 여부와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "대중도 주식 거래 자산이 있습니다.", "articles": [], "principle": "대중의 지위", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "규제당국은 강제적 정보 요구권이 있어 보고서 전적 의존자가 아니므로 주요이용자 범위에서 제외됩니다.", "articles": [], "principle": "주요이용자 제외 논리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "왜곡 유출을 이유로 배제하지 않습니다.", "articles": [], "principle": "정보 유출", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "악의적 대중 배척과 관계없습니다.", "articles": [], "principle": "위원회 성격", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "법인세율 조정과 무관합니다.", "articles": [], "principle": "세율", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "회계기준위원회가 회계기준(K-IFRS)을 제정할 때 주요 이용자들의 개 개별 구성원의 특수한 정보 수요 대신 '공통된 정보 수요(Common Information Needs)'에 초점을 맞추는 실무적 의의로 옳은 것은?",
        "options": [
          "① 기업들의 재무제표 작성 부담과 비용을 현실적으로 경감시켜 주고, 가장 핵심적인 공통 정보의 비교가능성을 보장하기 위함이다.",
          "② 세법상 세무 과세 표준을 100% 동일하게 묶어 관리하기 위함이다.",
          "③ 전 세계 주주들이 당기순이익에 전혀 관심을 갖지 않도록 유도하기 위함이다.",
          "④ 모든 기업들이 자산 규모를 동일하게 맞추어 공시하도록 통제하기 위함이다.",
          "⑤ 주석 기재의 의무 자체를 장기적으로 생략 마감하도록 돕기 위함이다."
        ],
        "answer": "1",
        "explanation": "① 정보이용자 개인의 요구를 모두 만족시키는 재무제표를 기업이 건건이 발행하는 것은 불가능하며, 엄청난 비용을 초래합니다. 따라서 다수 이용자의 공통 수요에 집중하여 경제적 효율성과 비교성을 높입니다.\n\n[오답 해설]\n② 세무 표준 묶음 관리와 무관합니다.\n③ 주주들의 당기순이익 관심을 차단하지 않습니다.\n④ 기업 자산 규모 획일화 통제 목적이 아닙니다.\n⑤ 주석 기재 생략을 유도하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "공통 정보 수요에 집중함으로써 작성 비용 절감 및 유용한 비교가능성을 도모합니다.", "articles": [], "principle": "공통 정보수요의 의의", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 표준 관리 목적이 아닙니다.", "articles": [], "principle": "세무 조정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "이익 관심 차단과 무관합니다.", "articles": [], "principle": "이익 관심", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자산 규모 획일화와 관계없습니다.", "articles": [], "principle": "자산 규모", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주석 생략 유도가 아닙니다.", "articles": [], "principle": "주석 공시", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "일반목적재무보고가 '공통된 정보 수요'에 초점을 맞춘다는 사실이 특정 일부 이용자의 '추가 유용한 정보'의 공시 여부에 미치는 영향으로 옳은 설명은?",
        "options": [
          "① 공통 정보에 초점을 맞추므로, 주주 일부가 요구하는 추가 정보는 절대 재무보고서에 포함될 수 없으며 위반 시 감리 제재를 받는다.",
          "② 공통된 정보 수요에 초점을 맞춘다고 해서 보고기업이 주요이용자의 특정 일부에게 유용한 추가 정보를 재무제표(주석 등)에 포함하지 못하게 하는 것은 아니다.",
          "③ 추가 정보를 계상하려면 국세청의 사전 대외비 승인 절차가 강제 필수적이다.",
          "④ 추가 정보 기재 시 전년도 당기순이익에 해당하는 벌금이 이사회에 직접 부과된다.",
          "⑤ 추가 정보는 반드시 부외 거래의 특별 비밀 장부에만 기록될 수 있고 외부 공시 보고서에서는 자동 탈락한다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고서의 기준서 초점은 다수의 공통수요이지만, 그렇다고 해서 기업이 특정 소수 주주나 투자자에게 필요한 유용한 추가 정보를 주석 등에 기재해 공시하는 것을 금지하지는 않습니다.\n\n[오답 해설]\n① 추가 정보 기재를 제재하지 않습니다.\n③ 국세청 사전 승인과 무관합니다.\n④ 벌금 부과 대상이 아닙니다.\n⑤ 비밀 장부 기재 규정이 아닌, 투명한 보고서 공시 사항입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "추가 기재를 위반 제재하지 않습니다.", "articles": [], "principle": "추가 기재 허용", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "공통 정보에 초점을 맞추더라도 유용한 추가 정보를 보고서에 포함시키는 것은 금지되지 않습니다.", "articles": [], "principle": "추가 유용정보의 지위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "국세청 사전 승인과 무관합니다.", "articles": [], "principle": "행정 승인", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "벌금 부과가 성립하지 않습니다.", "articles": [], "principle": "제재 부재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "비밀장부 기록이 아닌 적법 공시 대상입니다.", "articles": [], "principle": "장부 투명성", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "일반목적재무보고서가 미래지향적(Future-oriented) 가치 추정 분석에 도움을 제공하는 구체적 메커니즘으로 옳은 것은?",
        "options": [
          "① 기업의 미래 확정 이익 수치를 위원회가 계산하여 재무제표 전면 상단에 명시한다.",
          "② 과거 거래와 현재 자원 구조의 영향을 투명하게 보고하여, 이용자가 과거 사건의 흐름을 토대로 기업의 미래 순현금유입 및 가치를 합리적으로 추정할 수 있게 돕는다.",
          "③ 미래 예측에 유용하도록 주가 예측을 매월 산출하는 공식을 주석 1번에 기재한다.",
          "④ 미래의 리스크를 피하기 위해 경영진의 미래 예상 투자 지출을 장부에서 전액 비용 지워 은폐한다.",
          "⑤ 세법 상의 미래 과세액을 전세 세무서 기준으로 미리 확정 계산해 보여준다."
        ],
        "answer": "2",
        "explanation": "② 재무제표는 본질적으로 과거에 유발된 사건과 자원의 상태를 보여주지만, 이용자가 이 과거 성과 정보와 자무 상태 추이를 분석함으로써 미래의 전망을 타당하게 추정할 수 있도록 피드백 정보(예측가치)를 제공합니다.\n\n[오답 해설]\n① 미래의 확정 이익을 미리 계산해 주지 못합니다.\n③ 주가 예측 공식 기재 의무가 없습니다.\n④ 예상 투자 지출을 인위적으로 은폐 기록하지 않습니다.\n⑤ 미래 세액 확정 수치를 기재하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "미래 이익 확정치를 기재하지 않습니다.", "articles": [], "principle": "미래 이익", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "과거 및 현재의 투명한 재무 정보 제공을 통해 이용자가 미래 가치를 스스로 추정하도록 유도합니다.", "articles": [], "principle": "미래 예측 지원 방식", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주가 예측과 관계없습니다.", "articles": [], "principle": "주가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "지출 은폐 기재는 위법입니다.", "articles": [], "principle": "지출 공시", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "미래 세액 확정과 관계없습니다.", "articles": [], "principle": "세금", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "발생주의 회계(Accrual Accounting)가 반영된 재무성과 정보가 현금 수급 단독 정보보다 우월한 평가 근거를 제공하는 이유로 옳은 것은?",
        "options": [
          "① 발생주의는 현금의 흐름을 완전히 위장하여 기업의 도산 리스크를 영구 은폐하기 때문이다.",
          "② 비록 현금 수취와 지급이 다른 기간에 이루어지더라도, 거래와 사건 및 상황이 경제적자원 및 청구권에 미친 실제 영향을 발생 기간에 투명하게 보여주기 때문이다.",
          "③ 발생주의 수치와 현금흐름 수치는 언제나 수학적으로 100% 일치하기 때문이다.",
          "④ 현금 수급 정보만을 기재할 시 발생하는 감사 수수료 할인을 막기 위함이다.",
          "⑤ 세무 당국이 기업의 현금 결제 장부를 직접 무단 파기하도록 유도하기 위함이다."
        ],
        "answer": "2",
        "explanation": "② 발생기준 회계는 거래의 영향과 시점을 현금의 유출입 기간이 아닌 거래가 실제로 귀속되는 발생 기간에 보여주므로, 한 기간 동안의 현금 수지 단독 정보보다 과거/미래 성과와 수탁책임을 평가하는 데 있어 훨씬 논리적으로 뛰어난 근거를 제공합니다.\n\n[오답 해설]\n① 도산 리스크 은폐 목적이 아닙니다.\n③ 발생주의 수치와 현금흐름 수치는 기간적 차이로 대개 일치하지 않습니다.\n④ 감사 수수료 할인 방지 목적과 관계없습니다.\n⑤ 장부 파기 유도 목적이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "도산 리스크 은폐 목적이 아닙니다.", "articles": [], "principle": "리스크 은폐 배제", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "결제 시점과 상관없이 거래의 영향이 발생한 기간에 기재함으로써 성과 평가의 우월성을 가집니다.", "articles": [], "principle": "발생주의 우월성 근거", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "두 수치는 일치하지 않습니다.", "articles": [], "principle": "현금과 발생 일치", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사 수수료와 무관합니다.", "articles": [], "principle": "감사 수수료", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 장부 파기와 관계없습니다.", "articles": [], "principle": "장부 관리", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "개념체계가 강조하는 '재무성과에 기인하지 않은 경제적자원 및 청구권의 변동'(예: 지분상품 발행 등)에 대한 정보가 정보이용자에게 가지는 의의로 옳은 것은?",
        "options": [
          "① 기업이 무상으로 주식을 나누어 주어 모든 투자자가 즉시 부자가 됨을 보증하는 의의",
          "② 자원과 청구권이 변동된 실제 원인과 그 변동이 기업의 미래 재무성과에 주는 의미를 정보이용자가 완전히 이해하도록 돕는 의의",
          "③ 당해 지분 발행 거래가 국세청 세무조사에서 감세 대상임을 입증하는 의의",
          "④ 기업의 인수합병 가격을 임의로 두 배 상향시키는 조항의 의의",
          "⑤ 지분 발행 시 수반되는 감사 비용을 사외적립금으로 즉시 대체시키는 의의"
        ],
        "answer": "2",
        "explanation": "② 보고기업의 자원 및 청구권은 자본 거래(지분 발행 등)와 같이 성과 외의 사유로도 변동합니다. 이에 관한 정보는 이용자가 변동의 근본 원인을 구분해 미래 성과 의미를 해석하도록 돕는 역할을 합니다.\n\n[오답 해설]\n① 주주가 즉시 부자가 됨을 보증하지 않습니다.\n③ 세무조사 감세 입증용 정보가 아닙니다.\n④ 인수합병 가격을 인위적으로 조정하지 않습니다.\n⑤ 감사 비용의 사외적립금 대체 등과 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "주주의 재산 실현 보증과 관계없습니다.", "articles": [], "principle": "주주 이익", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "자본 거래 등 재무성과 외 원인을 밝혀 미래 재무성과 파급 효과를 이용자가 완전히 이해하게 돕습니다.", "articles": [], "principle": "재무성과 외 변동의 의의", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 감세 입증과 무관합니다.", "articles": [], "principle": "세무", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "인수합병가 2배 조정과 관계없습니다.", "articles": [], "principle": "인수합병", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사 비용 대체와 무관합니다.", "articles": [], "principle": "감사 비용", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "일반목적재무보고서 상의 재무성과(Financial Performance) 정보가 주주들이 경영진의 수탁책임(Stewardship)을 평가하는 데 도움을 주는 구체적 방식은?",
        "options": [
          "① 주주들이 매년 주총에서 이사진의 재선임 결정을 강제 무효화시키는 방식으로 돕는다.",
          "② 한 기간 동안 경제적 자원을 사용해 성과를 창출한 실적과 자원 보존 상태를 보고하여, 경영진이 수탁 책무를 효과적으로 이행했는지 감독할 수 있게 돕는다.",
          "③ 경영진이 실수한 모든 거래 손실액을 이사진의 개인 급여에서 공제하도록 명시해 돕는다.",
          "④ 해당 재무성과가 적정이면 경영진이 어떠한 불법 횡령을 하더라도 형사 면책을 받도록 보장하여 돕는다.",
          "⑤ 당기 재무성과를 임의의 잡손실 계정으로 합산하여 이사회가 숨기도록 유도해 돕는다."
        ],
        "answer": "2",
        "explanation": "② 재무성과에 관한 정보는 주주들이 보고기업의 자원에 대한 경영진의 수탁책임(자원을 효율적이고 효과적으로 유지·증대시켰는지 여부)을 올바르게 감시하고 평가하는 데 기여합니다.\n\n[오답 해설]\n① 주총 재선임 무효를 강제하는 직접 사법 장치가 아닙니다.\n③ 이사진 개인 급여 공제 규칙을 규율하지 않습니다.\n④ 횡령 면책 등 형사상 면책 혜택을 부여하지 않습니다.\n⑤ 성과를 임의로 은폐하여 마감하도록 지원하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "주총 직접 강제 권한이 없습니다.", "articles": [], "principle": "사법 권한", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "자원 대비 성과 효율성을 보고하여 경영진의 책임 이행 적정성 평가를 효과적으로 지원합니다.", "articles": [], "principle": "수탁책임 평가 방식", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "이사진 급여 공제 규칙이 아닙니다.", "articles": [], "principle": "급여 공제", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "형사 횡령 면책 특권을 주지 않습니다.", "articles": [], "principle": "형사 면책 부재", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장부 은폐를 허용하지 않습니다.", "articles": [], "principle": "정직한 보고", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "개념체계가 명시한 과거현금흐름 정보의 독자적인 쓰임새 중, 미래 순현금유입 창출 능력 평가 외의 추가적인 공식 유용성으로 옳은 것은?",
        "options": [
          "① 기업의 당기 법인세를 0원으로 감면하는 용도",
          "② 기업의 경제적자원에 대한 경영진의 수탁책임(Stewardship)을 올바르게 평가하는 용도",
          "③ 주식 거래량을 인위적으로 5배 증가시키는 용도",
          "④ 기업의 인수합병 가격을 임의로 두 배 높이는 용도",
          "⑤ 당기 현금흐름으로 감사 수수료를 사외적립 대체시키는 용도"
        ],
        "answer": "2",
        "explanation": "② 과거 현금흐름에 대한 정보는 미래 순현금유입액 창출 능력 평가뿐만 아니라, 자원에 대한 경영진의 수탁책임이 얼마나 성실히 수행되었는지 함께 평가하는 용도로 활용됩니다.\n\n[오답 해설]\n① 법인세 감면과 무관합니다.\n③ 주식 거래량을 인위적으로 조절하지 못합니다.\n④ 인수합병 가격 결정에 임의 개입하지 않습니다.\n⑤ 감사 수수료 적립 용도와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "법인세 감면 용도가 아닙니다.", "articles": [], "principle": "세제 감면", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "경영진의 수탁책임 평가도 과거 현금흐름 정보가 기여하는 중요한 공식 유용성입니다.", "articles": [], "principle": "과거 현금흐름의 수탁책임 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주식 거래량 조정과 무관합니다.", "articles": [], "principle": "주식 시장", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "인수합병 가격 개입과 관계없습니다.", "articles": [], "principle": "인수합병", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사 수수료 대체와 무관합니다.", "articles": [], "principle": "감사 비용", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "개념체계가 정한 여러 개념적 원칙들이 한국회계기준위원회와 작성자가 지속적으로 노력하여 지향해야 하는 '최적의 목표(Goal)' 지위를 가지는 근본 이유로 옳은 것은?",
        "options": [
          "① 목표를 달성하지 못하면 즉시 감사 대상 지정 벌금이 이사회에 부과되기 때문이다.",
          "② 재무제표는 상당 부분 오류 없는 서술보다는 추정, 판단 및 모형에 근거하므로, 완벽한 이상적 상태에 즉각 도달하긴 어려우나 유용성 극대화를 위해 계속 부합하도록 노력을 기울여야 하는 지향점이기 때문이다.",
          "③ 주총의 3분의 2 찬성을 유도하기 위한 마케팅 수단으로 목표를 설정했기 때문이다.",
          "④ 목표를 달성하면 국세청의 모든 세무조사를 영구 면제해 주는 지침이기 때문이다.",
          "⑤ 입법 소송을 제기하여 상충 기준서를 말소하기 위한 사법적 목표이기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 재무제표는 주관적 추정과 모형이 다수 내재되어 있어 완벽한 100% 오류 없는 물리적 정확한 표시는 어렵습니다. 따라서 개념체계의 조항은 이상적인 질적 유용성을 향해 계속 수렴하도록 노력을 유도하는 최적의 지향 목표를 의미합니다.\n\n[오답 해설]\n① 미달성으로 인한 벌금 부과 조항과 무관합니다.\n③ 주총 마케팅 수단이 아닙니다.\n④ 세무조사 면제 특권을 주지 못합니다.\n⑤ 사법 입법 소송을 위한 법적 목표서가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "벌금 강제 규정이 아닙니다.", "articles": [], "principle": "제재 부재", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "추정의 불가피성 속에서 유용성을 끊임없이 다듬어 수렴하게 하는 최적의 지향 목표가 됩니다.", "articles": [], "principle": "지향 목표의 지위 원인", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주총 의결 수단이 아닙니다.", "articles": [], "principle": "주총 수단 배제", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무조사 면제와 무관합니다.", "articles": [], "principle": "세무조정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사법 소송 목적이 아닙니다.", "articles": [], "principle": "사법 소송", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "일반목적재무보고서 상의 '경제적 자원 및 청구권' 정보가 정보이용자의 의사결정에 차이를 낳도록 돕는 구체적 기여 방식으로 옳은 것은?",
        "options": [
          "① 이용자들에게 무상 대출 승인 보증서를 자동으로 지급해 돕는다.",
          "② 보고기업의 재무적 강점과 약점을 식별하게 돕고, 유동성/지급능력을 평가하며 재무구조 분석 및 미래 현금흐름의 시기와 불확실성을 예측하도록 돕는다.",
          "③ 주식시장 투자 리스크를 완전히 0원으로 만들어 돕는다.",
          "④ 해당 기업의 감가상각 금액을 전액 세법과 일치시키도록 강제해 돕는다.",
          "⑤ 기업의 영업 비밀이 자본시장에 영구 유출되지 않도록 차단막을 형성해 돕는다."
        ],
        "answer": "2",
        "explanation": "② 경제적 자원(자산) 및 청구권(부채/자본)에 대한 정보는 정보이용자가 기업의 재무적 강약점을 포착하고 유동성 및 재무구조, 장기 지급능력 등을 과학적으로 평가하도록 기여합니다.\n\n[오답 해설]\n① 무상 대출 승인 보증서를 제공하지 않습니다.\n③ 투자 리스크를 완전히 지워 0원으로 만들 수 없습니다.\n④ 세법 감가상각과의 강제 일치 의무가 없습니다.\n⑤ 영업 비밀 차단 장치가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "무상 대출 보증서와 무관합니다.", "articles": [], "principle": "대출 보증", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무 상태 및 강약점 식별, 유동성, 지급능력 등을 다각도로 평가할 핵심 자료를 제공합니다.", "articles": [], "principle": "자원과 청구권 정보의 유용성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "리스크를 0원으로 소멸하지 못합니다.", "articles": [], "principle": "투자 안전성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세법 상각비의 강제 일치 의무가 없습니다.", "articles": [], "principle": "세무 조정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "영업 비밀 차단막이 아닙니다.", "articles": [], "principle": "비밀주의 배제", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "일반목적재무보고 상 '보고기업에 대한 청구권' 정보가 기업의 유동성(Liquidity) 및 지급능력(Solvency) 평가에 기여하는 직접적 방식으로 옳은 것은?",
        "options": [
          "① 청구권을 전액 면제 탕감해 주는 법률 효력을 기재해 기여한다.",
          "② 청구권의 성격과 금액 정보(예: 단기 채무 대 장기 부채 비율 등)를 기재하여, 장단기 채무 만기 충당 능력을 예측하게 기여한다.",
          "③ 대주주가 채무를 연대 보증하도록 상법 상 강제 조치하여 기여한다.",
          "④ 해당 청구권 금액의 10%를 감사인에게 의무 수수료로 지급하도록 명시해 기여한다.",
          "⑤ 채권자들의 회사 영업 비밀에 대한 정보 차단권을 설정해 기여한다."
        ],
        "answer": "2",
        "explanation": "② 보고기업의 청구권(부채의 구조) 정보는 만기나 상환 조건 등을 나타내므로, 이용자가 장단기 채무 충당에 필요한 추가 자금 조달 능력을 올바르게 식별(유동성과 지급능력 판단)할 수 있게 합니다.\n\n[오답 해설]\n① 청구권 면제 탕감 효력을 발동시키지 못합니다.\n③ 대주주의 상법 상 강제 보증 의무를 설정하지 않습니다.\n④ 감사 수수료 지급 강제 지침이 아닙니다.\n⑤ 영업 비밀 정보 차단권 설정 등과 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "청구권 면제와 관련 없습니다.", "articles": [], "principle": "채무 탕감 부재", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "단기 및 장기 부채의 만기 구조 정보를 통해 기업의 상환 만기 대응 능력을 평가하도록 돕습니다.", "articles": [], "principle": "유동성 지급능력 평가 기여", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "대주주 강제 보증 조치가 아닙니다.", "articles": [], "principle": "대주주 보증", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사 수수료 명시 조항이 아닙니다.", "articles": [], "principle": "감사 수수료", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "비밀 차단권 설정과 관계없습니다.", "articles": [], "principle": "정보 차단", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "발생기준 회계가 반영된 재무성과 정보와 과거 현금흐름 정보의 상호 관계에 관한 개념체계의 인식으로 옳은 것은?",
        "options": [
          "① 발생주의 정보와 현금흐름 정보는 서로 상충하므로 둘 중 하나는 반드시 폐기해야 한다.",
          "② 양 정보는 상호보완적이며, 성과 평가와 미래 현금유입 창출 능력의 시기 및 불확실성을 완전히 평가하려면 두 정보를 유기적으로 함께 분석해야 한다.",
          "③ 발생주의가 현금흐름 정보보다 언제나 100% 우월하므로 현금흐름표는 재무제표 구성 항목에서 제외해야 한다.",
          "④ 현금 수급 정보만이 사실이고 발생주의는 가짜 정보이므로 발생주의를 보조 수단으로만 한계 적용한다.",
          "⑤ 두 정보의 충돌을 해소하기 위해 기업은 매 기말 수치적 평균값을 주석에만 공시한다."
        ],
        "answer": "2",
        "explanation": "② 발생기준 정보와 현금주의 정보는 재무성과 분석에 있어 상호 보완적인 유용성을 가집니다. 따라서 정보이용자는 두 정보를 유기적으로 조화시켜 분석해야 의사결정 차이를 낳을 수 있습니다.\n\n[오답 해설]\n① 두 규정이 충돌하여 폐기 대상이 되지 않으며 둘 다 필수 제출 보고서에 반영됩니다.\n③ 현금흐름표 또한 K-IFRS 상의 핵심 재무제표 중 하나이므로 제외할 수 없습니다.\n④ 발생주의를 가짜 정보로 격하하지 않습니다. 발생주의 정보가 더 나은 근거를 제공함을 밝힙니다.\n⑤ 산술 수치적 평균값 강제 공시 제도는 존재하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "두 정보 모두 필수 공시 항목입니다.", "articles": [], "principle": "공시 요건", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "두 정보는 상호보완적이며 기업 성과와 자금 대응력을 평가하는 데 모두 유기적으로 유용합니다.", "articles": [], "principle": "상호보완적 유용성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "현금흐름표 제외 주장은 틀렸습니다.", "articles": [], "principle": "재무제표 구성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "발생주의를 보조 수치로 격하하지 않습니다.", "articles": [], "principle": "발생주의 지위", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "평균값 계상 공시는 불가합니다.", "articles": [], "principle": "평균값", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "일반목적재무보고가 제공하는 '재무성과에 기인하지 않은 경제적자원 및 청구권의 변동'을 설명하는 구체적인 예시로 가장 타당한 것은?",
        "options": [
          "① 당기 중 공장의 기계장치가 불타서 발생한 '재해손실' 기록",
          "② 기업이 자금 조달을 위해 주주들을 대상으로 실시한 '유상증자(지분상품 발행)' 거래",
          "③ 거래처에 기계부품을 외상으로 판매하고 기록한 '매출액' 성과",
          "④ 기말 현재 보유 부동산의 단순 시가 상승에 따른 '평가이익' 계상",
          "⑤ 기말 결산 감가를 위해 설정한 '감가상각비' 설정"
        ],
        "answer": "2",
        "explanation": "② '재무성과에 기인하지 않은 변동'은 당기 영업 성과나 평가 손익 등이 아닌, 주주와의 자본 거래(유상증자, 감자, 배당 등 지분 발행)나 채무상품 발행 등을 의미합니다.\n\n[오답 해설]\n① 재해손실은 당기 비용 성과 항목입니다.\n③ 외상 매출은 매출액 성과 항목입니다.\n④ 부동산 시가 상승 평가이익은 당기 손익 성과에 기인한 변동입니다.\n⑤ 감가상각비는 성과 비용 항목입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "재해손실은 당기성과 비용입니다.", "articles": [], "principle": "성과 분류", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "유상증자와 같은 지분상품 발행은 재무성과 외 원인에 따른 자원 변동 사례가 맞습니다.", "articles": [], "principle": "재무성과 외 변동 사례", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "매출액은 성과 수익입니다.", "articles": [], "principle": "성과 분류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "평가이익은 성과 수익입니다.", "articles": [], "principle": "성과 분류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감가상각비는 성과 비용입니다.", "articles": [], "principle": "성과 분류", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "일반목적재무보고서 상의 자원 변동 원인 중 '재무성과(Financial Performance)'에 해당하는 거래를 올바르게 지적한 것은?",
        "options": [
          "① 주주들에게 지급한 '당기 배당금 분배' 거래",
          "② 채권자들에게 이자를 지급하기 위해 신규 사채를 발행한 거래",
          "③ 당기 중 고객에게 재화를 인도하고 대금을 수취해 발생한 '영업 수익' 거래",
          "④ 자사주 매입을 위해 기말에 현금을 사외 유출한 거래",
          "⑤ 회사가 자본을 감소시키기 위해 주식을 소각(감자)한 거래"
        ],
        "answer": "3",
        "explanation": "③ 재무성과는 자본거래를 제외한 기업의 영업 활동 결과(수익과 비용)를 나타냅니다. 따라서 재화를 인도하고 발생한 영업 수익 거래가 재무성과를 이룹니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 모두 주주나 채권자와의 자본 거래 또는 자금 조달 거래이므로 '재무성과 외의 변동 원인'에 귀속됩니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "배당금은 자본거래 변동입니다.", "articles": [], "principle": "성과 외 변동", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사채 발행은 자본거래 변동입니다.", "articles": [], "principle": "성과 외 변동", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재화 인도에 따른 영업 수익은 재무성과 변동에 속합니다.", "articles": [], "principle": "재무성과 변동 사례", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자사주 매입은 자본거래 변동입니다.", "articles": [], "principle": "성과 외 변동", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주식 소각 감자는 자본거래 변동입니다.", "articles": [], "principle": "성과 외 변동", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },

    # =========================================================================
    # L3: 적용 및 상황 판단형 (15문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s03-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "(시나리오) 소액 주주 A는 K사의 기말 재무제표 상 자본 합계액이 50억 원인 것에 반해, K사의 주식시장에서의 시가총액이 120억 원에 이른다는 기사를 읽고 회사 재무팀장에게 \"70억 원 규모의 중대한 장부 기재 누락 및 분식 혐의가 있다\"고 거세게 해명을 요구했다. K사 재무팀장이 개념체계에 비추어 내릴 올바른 해명은?",
        "options": [
          "① 누락을 즉시 인정하고 주총 동의 하에 자산 금액을 70억 원 인위적으로 늘려 소급 재작성하겠다고 한다.",
          "② 일반목적재무보고서는 보고기업의 가치를 직접 보여주기 위해 고안된 것이 아니므로 불일치는 당연하며, 재무보고서는 주주가 가치(120억 원)를 추정하는 데 유용한 자료를 제공한 것임을 설명한다.",
          "③ 시가총액 차액 70억 원을 세제 감면 환급용 잡손실 계정으로 즉시 장부 소급 기재해 주겠다고 제안한다.",
          "④ 해당 거래소 주가를 강제로 50억 원으로 낮춰 불일치를 강제 해소하겠다고 통보한다.",
          "⑤ 재무보고서가 무가치함을 시인하고 올해분 결산 공시 전체를 전면 철회 취소한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 일반목적 재무보고서가 기업 가치를 직접 계산해 보여주기 위해 고안된 서류가 아님을 서술합니다. 장부가와 시장가의 차이는 자연스러운 회계적 결과이며, 보고서는 가치를 추정할 유용한 근거를 주는 역할을 함을 주주에게 차분히 설득하는 것이 타당합니다.\n\n[오답 해설]\n① 70억 원의 자의적 소급 평가는 분식회계입니다.\n③ 세무 환급 잡손실 계상은 허용되지 않는 오류입니다.\n④ 위원회나 기업이 주식 시가를 강제로 하향 조절할 권한이 없습니다.\n⑤ 공시 철회는 불가능합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "자의적 소급 평가는 불허됩니다.", "articles": [], "principle": "분식회계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 기업 가치를 직접 보여주지 않으며 추정 판단 자료만 제공함을 명시한 올바른 해명 지문입니다.", "articles": [], "principle": "가치평가 불일치 대처", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적 손실 처리는 오류입니다.", "articles": [], "principle": "회계 오류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주가 조정 통제 권한이 없습니다.", "articles": [], "principle": "주가 통제", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "공시 철회는 불가합니다.", "articles": [], "principle": "공시 유지", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "(시나리오) M사의 경영진은 회사 내부의 극비 핵심 신약 임상 세부 데이터를 재무보고서에 상세히 추가하여 공시하라고 재무 부서에 지시했다. 이에 대해 M사 재무팀장이 개념체계 상의 '일반목적재무보고의 한계'에 비추어 지시를 철회하게 유도할 수 있는 올바른 거부 사유는?",
        "options": [
          "① 해당 데이터 기재 시 금융감독원에 1억 원의 특별 과태료를 직접 납부해야만 하는 법규가 있기 때문이다.",
          "② 일반목적재무보고서는 주요이용자 다수의 공통 정보 수요에 맞추며 이용자가 필요로 하는 모든 정보를 제공할 수도 없으므로, 영업 기밀이자 기업 가치에 직결된 극비 내부 상세 데이터를 외부 일반보고서에 노출해 손실을 볼 필요가 없음을 피력한다.",
          "③ 해당 데이터를 주석에 담으면 올해 회사 법인세가 2배 자동 가산 인상되는 불이익이 발생하기 때문이다.",
          "④ 경영진의 지시는 감사인과의 합의 없이는 어떠한 내용도 보고서에 적법 반영될 수 없기 때문이다.",
          "⑤ 극비 데이터를 적으면 재무제표가 자동으로 특수비밀보고서로 변경 고시되어 효력을 잃기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고서는 주요이용자 최대 다수의 공통 수요를 맞출 뿐, 모든 세부 정보를 제공할 수도 제공하도록 강제하지도 않습니다. 극비 신약 데이터 등 핵심 경쟁력은 외부보고서에서 적절히 제외해 기밀을 유지하는 것이 합리적입니다.\n\n[오답 해설]\n① 1억 원 과태료 규정은 존재하지 않는 허구입니다.\n③ 법인세 가산 인상 리스크와 무관합니다.\n④ 작성 정책 수립의 최종 결정 주체는 경영진(회사)이며 감사인의 사전 동의를 법적 필수 요건으로 하진 않습니다.\n⑤ 특수비밀보고서 변경 취소 등은 허구 지문입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "과태료 규정이 존재하지 않습니다.", "articles": [], "principle": "행정 제재", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 모든 이용자의 세부 수요를 완벽히 만족하지 못하는 한계가 있어 기밀의 은밀한 누출을 차단하는 결정을 내릴 수 있습니다.", "articles": [], "principle": "재무보고 범위와 기밀 관리", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "법인세 인상과 무관합니다.", "articles": [], "principle": "세율 영향", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "작성 최종 권한은 회사에 있습니다.", "articles": [], "principle": "작성 권한", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "비밀보고서 자동 변경 규정은 허구입니다.", "articles": [], "principle": "보고서 명칭", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "(시나리오) 주주 D는 적정의견을 받은 D사의 재무제표 상 당기순이익이 10억 원임에도 불구하고, 실제 회사의 기말 현금 잔액은 오히려 감소한 것에 대해 분노하며 이사회를 사기죄로 고소하겠다고 주장하고 있다. D사 재무팀장이 주주 D를 발생주의 회계 원리로 타당하게 설득할 수 있는 근거는?",
        "options": [
          "① 당기순이익 수치는 주주총회를 속이기 위해 임의로 가공해 놓은 가짜 번호임을 시인하고 빌어 고소를 취하하게 한다.",
          "② 발생기준 회계는 거래의 영향이 발생한 기간에 보여주므로, 결제 수령이 아직 안 된 외상 매출 등도 당기 이익에 정당하게 포함되며, 이는 현금의 단순 유출입 정보보다 장기 성과와 경영진 책임을 평가하는 데 더 나은 정보를 제공함을 해명한다.",
          "③ 주주의 화를 풀기 위해 미실현 이익 10억 원을 사외 적립금으로 조작 이전해 주겠다고 거래를 제안한다.",
          "④ 현금 잔액 일치를 위해 기말 장부의 현금 보유액을 강제로 10억 원 인위적으로 늘려 소급 공시하겠다고 한다.",
          "⑤ 세무서에 고발하여 회사 법인세를 면제해 주겠다고 설득한다."
        ],
        "answer": "2",
        "explanation": "② 발생주의 회계는 거래의 영향이 발생 기간에 반영되므로, 현금의 단순 유출입 시점 차이로 인해 당기순이익과 기말 현금 잔액의 불일치가 발생하는 것은 지극히 정상적인 현상입니다. 발생주의 정보가 현금주의 정보보다 우월한 의사결정 차이를 줌을 주주에게 납득시켜야 합니다.\n\n[오답 해설]\n① 이익 수치는 기준서에 따라 적법하게 계산된 정당한 수치입니다.\n③, ④ 임의의 사외 적립금 조작이나 현금 보유액 허위 소급 기재는 중대한 위법 회계 사기입니다.\n⑤ 법인세 면제와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "수치는 적법 수치이므로 가짜가 아닙니다.", "articles": [], "principle": "수치의 적법성", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "발생주의 원리 상 현금 수지와 성과 순이익은 불일치할 수 있으며 이것이 합리적 정보를 줌을 설명해야 합니다.", "articles": [], "principle": "발생주의와 현금주의 차이 해명", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의 사외 이전 제안은 불법입니다.", "articles": [], "principle": "사외 적립", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "현금 잔액 허위 기재는 위법입니다.", "articles": [], "principle": "현금 조작", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세제 면제와 무관합니다.", "articles": [], "principle": "세금 면제", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "(시나리오) 정부 감독기관의 회계 과장 E는 기업 공시된 일반목적재무보고서가 \"감독기관의 규제 적법성 심사를 위한 특수 지표들을 정확히 분류하여 제공하지 않고 있어 행정 행위에 부적합하다\"고 규제 경고 처분을 내리려 한다. 이에 대한 관련 법규 및 개념체계 상의 방어 논리로 타당한 것은?",
        "options": [
          "① 일반목적재무보고서가 감독기관의 요구를 최우선적으로 만족해야 하므로 즉시 특수 지표에 맞춰 전면 개정 공시해야 한다.",
          "② 일반목적재무보고서는 규제당국 등의 특수 목적 정보 제공을 일차적 표방 대상으로 한 것이 아니므로 규제 적합성에 완전히 맞출 필요는 없으며, 규제기관은 기업에 관련 특수 지표를 강제 직접 요구할 권한을 지니고 있음을 해명한다.",
          "③ 감독기관의 화를 누그러뜨리기 위해 즉시 회계기준위원회 위원 전원의 감사를 직권 보류 요청한다.",
          "④ 해당 거래 금액을 타 지표로 임의 섞어서 재분류 공시하겠다고 타협한다.",
          "⑤ 즉시 재무제표 전체를 파기 취소하여 공시 대상에서 전면 철수한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 일반목적 재무보고서가 감독당국이나 기타 비주요이용자 집단을 주요 대상으로 한 것이 아님을 밝히고 있습니다. 규제기관은 자체 법적 권한으로 필요한 정보를 기업에 직접 따로 요구해 얻을 수 있습니다.\n\n[오답 해설]\n① 감독당국의 특수 목적 요구에 보고서를 강제 매칭해 전면 개정할 의무가 없습니다.\n③ 위원회 감사 보류 요청은 법적 공식 절차가 아닙니다.\n④ 임의 섞기 분류 타협은 오류를 범하는 것입니다.\n⑤ 공시 전면 철수는 불가합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "지표 강제 매칭 의무가 없습니다.", "articles": [], "principle": "행정 대처", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "규제기관은 주요이용자가 아니며 직접 요구권을 쓰면 됨을 해명하는 것은 개념체계에 완벽히 부합합니다.", "articles": [], "principle": "규제당국과 일반목적재무보고", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "위원회 감사 보류 권한이 없습니다.", "articles": [], "principle": "감사 보류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의 분류 조작 타협은 불가합니다.", "articles": [], "principle": "계정 분류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "공시 전면 파기는 불허됩니다.", "articles": [], "principle": "공시 의무", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "(시나리오) F사의 이 상무는 매년 기말 평가 시 자사 이익에 유리하게 대손충당금 설정 비율을 자의적으로 변경 적용하여 이익을 인위적으로 관리하려 시도했다. 이에 대한 F사 회계담당자 정 대리의 개념체계 상의 올바른 조언은?",
        "options": [
          "① 이사진의 이익 관리는 정당한 경영 판단 재량이므로 모형을 매번 자의적으로 바꾸는 것이 정당하다.",
          "② 재무보고서는 추정과 판단, 모형에 상당 부분 근거하므로, 일관성과 정보 질의 신뢰성을 유지하고 정보이용자의 오도를 피하기 위해 일관된 합리적 모형과 판단을 적용해야 한다.",
          "③ 대손충당금 계정을 장부에서 지워 없애고 손익계산서의 감가상각 누계액으로 은밀히 이전한다.",
          "④ 매년 번복 조정을 해도 가산세를 부과당하지 않도록 세무서장에게 은밀히 요청한다.",
          "⑤ 충당금을 기재하는 대신 전 소송금액을 비밀 차명 계좌에 예치하여 부외자산으로 숨겨 준다."
        ],
        "answer": "2",
        "explanation": "② 재무제표는 추정과 모형에 크게 의존하지만, 이것이 경영진의 자의적인 이익 조정이나 모형 변경 권한을 부여하지는 않습니다. 개념체계는 추정 판단 지침의 일관성을 강력히 유도합니다.\n\n[오답 해설]\n① 자의적인 매년 변경은 위법한 회계 조작입니다.\n③ 감가상각 누계액으로의 은밀한 계정 이전은 분식회계입니다.\n④ 세무서장에게 비밀 가산세 면제 요청 등은 불가능합니다.\n⑤ 부외자산 은닉 및 차명 계좌 사용은 중대한 범죄입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "자의적 실적 조작은 위법입니다.", "articles": [], "principle": "이익 관리 금지", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "추정치와 모형이 정보의 유용성을 저해하지 않으려면 합리적이고 일관된 지침 아래 작동해야 합니다.", "articles": [], "principle": "추정치의 신뢰성 확보", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "계정 분류 오류 조작은 위법입니다.", "articles": [], "principle": "계정 분류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "가산세 면제 협상은 불가합니다.", "articles": [], "principle": "세무 세법", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "비밀 차명 계좌 은닉은 범죄입니다.", "articles": [], "principle": "부외 자산", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "(시나리오) 투자자 G는 H사의 당기 영업 현금흐름 정보와 발생주의 당기순이익 수치를 동시에 분석하고 있다. G가 이 두 정보를 유기적으로 결합하여 내린 분석 결론 중 개념체계에 비추어 올바른 투자 판단은?",
        "options": [
          "① 영업 현금흐름과 당기순이익이 불일치하므로 H사의 장부는 100% 분식회계 상태이다.",
          "② 발생기준 성과는 미래 유입 창출 능력을 예측하는 우월한 근거를 제공하며, 현금흐름 정보는 단기 지급 능력과 현금 창출 원천을 보완해 보여주므로 두 정보를 보완하여 H사의 가치를 스스로 합리적으로 추정한다.",
          "③ 두 수치의 격차 금액을 H사 재무팀에게 즉각 자본금 증가 전표로 강제 기재하도록 명령한다.",
          "④ 현금 수지가 발생이익보다 적으므로 즉시 H사를 임시 청산 대상 기업으로 가정하여 주식을 긴급 매도한다.",
          "⑤ 거래소에 두 정보의 불일치를 사유로 H사의 주식 거래를 즉시 정지시킬 것을 청구한다."
        ],
        "answer": "2",
        "explanation": "② 발생기준 정보와 과거 현금흐름 정보는 재무성과와 미래 자금 대응 예측에 있어 완벽한 상호보완적 정보 가치를 제공합니다. 따라서 두 수치를 유기적으로 함께 비교 분석하는 것이 올바릅니다.\n\n[오답 해설]\n① 불일치는 발생주의 회계 상 정상적 차이입니다.\n③ 투자자가 기업 자본금을 강제 수정 전표 기재하게 할 수 없습니다.\n④ 단기 수지 불일치만으로 임시 청산 기업 가정을 내리는 것은 무리가 있습니다.\n⑤ 거래 정지 제소 사유가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "수치 불일치는 분식회계 증거가 아닙니다.", "articles": [], "principle": "회계 차이", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "발생주의와 현금흐름 정보는 상호보완적이며 두 정보를 비교 분석하는 것이 합리적 판단을 돕습니다.", "articles": [], "principle": "양 정보의 상호보완적 분석", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자본금 강제 수정 권한이 없습니다.", "articles": [], "principle": "장부 전표", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "청산 가정의 사유가 아닙니다.", "articles": [], "principle": "계속기업가정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "거래 정지 청구 사유가 아닙니다.", "articles": [], "principle": "주식 거래", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "(시나리오) 주주 J는 경영진 K가 올해 신규 사채(Debentures)를 대량 발행하여 부채 비율을 높였지만, 당기 영업순이익(재무성과) 자체는 흑자 상태를 유지한 것을 식별했다. J가 이 두 종류의 변동 정보에 근거해 내린 경영진 수탁책임(Stewardship) 분석 결론으로 옳은 것은?",
        "options": [
          "① 사채 발행은 재무성과가 아니므로 주주들에게 아무런 재무적 영향을 주지 않는 완전 무가치한 거래이다.",
          "② 사채 발행은 재무성과 외의 사유로 자원과 청구권을 변동시킨 지표이고 영업이익은 성과이므로, 이 두 원천을 구별하여 사채 자금 조달의 효율성과 영업 실적 보존 능력을 다각도로 성실히 평가한다.",
          "③ 즉시 경영진 K를 사채 대량 발행죄로 사법 기소하여 연임을 법적으로 자동 박탈한다.",
          "④ 사채 수치를 장부에서 은밀히 지워 지분 자본 계정으로 100% 임의 대체 계상시킨다.",
          "⑤ 두 정보가 충돌하므로 당기순이익 전체를 국세청에서 특별 압류할 것을 건의한다."
        ],
        "answer": "2",
        "explanation": "② 보고기업의 미래 순현금유입액 전망과 경영진 수탁책임을 올바르게 평가하기 위해, 이용자는 재무성과에 따른 변동과 재무성과 외의 거래(사채 발행 등)에 따른 변동을 명확하게 구별할 수 있어야 합니다.\n\n[오답 해설]\n① 사채 발행은 부채 증가 등 심대한 영향을 주므로 무가치하지 않습니다.\n③ 사채 발행은 합법적인 자금 조달 행위이므로 처벌 대상이 아닙니다.\n④ 사채 수치를 자본으로 조작 대체하는 것은 중대한 분식회계입니다.\n⑤ 국가가 당기순이익을 압류하지 못합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "사채 발행은 매우 유효한 정보입니다.", "articles": [], "principle": "사채 발행 정보", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "변동 원천인 성과와 성과 외의 자본거래를 구별하여 경영진의 책임 이행 능력을 다각도로 평가해야 합니다.", "articles": [], "principle": "변동 원천 구별과 수탁책임 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사채 대량 발행이 법적 처벌 죄가 아닙니다.", "articles": [], "principle": "사법", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "부채를 자본으로 조작하는 것은 분식회계입니다.", "articles": [], "principle": "부채 자본 조작", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "이익 특별 압류는 불가합니다.", "articles": [], "principle": "사유 재산", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "(시나리오) 신종 가상계약 거래를 두고 L사의 회계담당자는 자산으로 기재해야 할지 고민하고 있다. 이 신종 거래는 현행 K-IFRS 기준서의 지침이 다소 공백인 상태이다. 회계사가 개념체계의 '경제적 자원' 정의에 비추어 올바르게 내린 판단은?",
        "options": [
          "① 명시된 기준서가 없으므로 해당 자산 거래 전체를 비용 처리해 공시하지 않는다.",
          "② 경제적 자원의 기본 요건(과거 사건 결과, 기업 통제, 미래 유입 가능성)을 충족하는지 개념체계를 성실히 해석하여 타당한 자산 계정으로 합리적으로 수립 공시한다.",
          "③ 감사 회계법인의 수습 직원 지시에 전적으로 따라 자의적으로 장부를 계상한다.",
          "④ 해당 거래 금액을 타 지표와 섞어서 비밀 주석에만 공란 표시한다.",
          "⑤ 기준서 개정안이 공표될 때까지 회계 기록을 3년간 거부한다."
        ],
        "answer": "2",
        "explanation": "② 특정 K-IFRS 기준서의 지침이 공백인 경우, 작성자는 개념체계가 정한 경제적 자원 및 청구권의 본질적 정의를 참조하여 합리적이고 유용한 회계정책을 자체 수립해 보고하는 것이 적법합니다.\n\n[오답 해설]\n① 무조건 생략하거나 자의적 비용 처리하지 않습니다.\n③ 감사인에 대한 수동적 위임은 불가합니다.\n④ 비밀 차명 계상이나 주석 공란은 위법입니다.\n⑤ 기재 거부는 적시성 위반입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "생략 비용 처리는 불허됩니다.", "articles": [], "principle": "회계정책", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "기준서 부재 시 개념체계의 자산 정의를 해석 준수하여 정책을 개발해야 합니다.", "articles": [], "principle": "자산 정의 적용", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감사인에게 장부 작성 책임을 미룰 수 없습니다.", "articles": [], "principle": "책임 전가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "비밀 주석 공란은 위법입니다.", "articles": [], "principle": "공시 위반", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기록 거부는 불가합니다.", "articles": [], "principle": "적시 기록", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "(시나리오) 다국적 대기업 M사는 전 세계 자회사의 미래 실적을 예측하고 투자를 분배하려고 한다. M사의 기획조정실은 국가별 지사들의 장부를 어떻게 분석해야 하는가? 개념체계의 발생주의 회계 정보 유용성에 비추어 옳은 행동은?",
        "options": [
          "① 발생주의는 국가별로 조작 가능성이 있으므로 전 해외 지사의 장부를 무시하고 오직 기말 현금 금고 잔액 수치로만 투자를 분배한다.",
          "② 각 지사의 발생주의 회계 정보를 통일적으로 취합하여, 현금 수급 차이 등의 왜곡 없이 기간 중 지사들의 실제 성과 창출 능력을 투명하게 비교하여 투자 여부를 결정한다.",
          "③ 각 지사의 감가상각 금액을 현지 세무 법률과 강제 통합시켜 자의적으로 지출을 숨기게 유도한다.",
          "④ 현지 주총의 3분의 2 동의가 없어도 모든 지사의 수익을 인위적으로 모회사 순자산에 합산 공시한다.",
          "⑤ 지사들의 결산 자료 제출 일정을 무기한 연기시키고 세법을 고쳐 달라고 소송한다."
        ],
        "answer": "2",
        "explanation": "② 발생주의 회계 정보는 단순 현금 수급 정보보다 기간 중의 실제 영업 활동 성과를 훨씬 더 합리적이고 객관적으로 보여줍니다. 따라서 다국적 기업은 발생주의 지표를 기준으로 자회사의 성과를 공정 비교하는 것이 효율적입니다.\n\n[오답 해설]\n① 단순 현금 금고 잔액만으로 장기 성과 투자를 분배하면 왜곡된 결정을 내리게 됩니다.\n③ 세무 세법과의 강제 불법 통합은 금지됩니다.\n④ 주총 동의 없이 임의의 회계처리를 하는 것은 상법 위반 우려가 있으나, 회계 결산 자체는 연결 회계 기준서에 따라 진행해야 하며 자의적 합산 조작은 금지됩니다.\n⑤ 결산 연기나 세법 소송은 합리적이지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "현금 수지만으로 분석하면 성과가 오도됩니다.", "articles": [], "principle": "현금주의 한계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "지사들의 발생주의 성과 정보를 비교 분석해 투자 결정을 내리는 것이 개념체계 상의 유용성 원리에 부합합니다.", "articles": [], "principle": "발생주의 비교 분석 적용", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 세법과의 불법 통합은 금지됩니다.", "articles": [], "principle": "세법", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "자의적 합산 조작은 금지됩니다.", "articles": [], "principle": "연결 회계", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "행정 소송 등은 오류입니다.", "articles": [], "principle": "소송", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "(시나리오) 거래소 감리반은 O사가 '신규 주식 발행액'(재무성과 외의 변동)을 마치 당기 '매출액'(재무성과)인 것처럼 왜곡 기재하여 당기순이익을 부풀린 혐의를 적발했다. 거래소 감리반의 지적 및 행정 조치의 정당성에 대한 분석으로 옳은 것은?",
        "options": [
          "① 주식 발행도 회사의 현금 유입을 유발했으므로 매출액으로 분류하는 것은 정당한 창조적 회계이다.",
          "② 자원 및 청구권의 변동은 재무성과에 따른 변동과 지분 발행 등 성과 외의 변동으로 엄격히 구별되어야 하므로, O사의 왜곡 기재는 명백한 분식회계이며 감리 조치는 백퍼센트 정당하다.",
          "③ O사가 세금을 회피하지 않았다면 감리 조치는 즉시 기각되어야 한다.",
          "④ 적발된 주식 전액을 정부 예산으로 몰수 처리하는 지시를 즉시 집행한다.",
          "⑤ O사에게 주식 시장 감독 규정을 영구 면제해 주는 타협으로 종결한다."
        ],
        "answer": "2",
        "explanation": "② 개념체계는 미래 순현금유입액 전망과 경영진 수탁책임을 평가하기 위해 이용자가 재무성과에 따른 변동과 재무성과 외의 거래에 따른 변동을 명확히 구분할 수 있어야 함을 기술합니다. 두 원천을 뒤섞어 매출액으로 위장한 것은 중대한 분식회계입니다.\n\n[오답 해설]\n① 현금 유입이 된다고 자본거래를 매출로 위장하는 창조적 회계(분식회계)는 금지됩니다.\n③ 감세 여부와 상관없이 회계 투명성을 훼손했으므로 처벌 대상입니다.\n④ 정부가 임의로 사유 주식을 몰수할 수 없습니다.\n⑤ 감리 면제 타협은 허용되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "자본거래의 매출 위장은 중대한 분식회계입니다.", "articles": [], "principle": "분식회계", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "변동의 두 원천을 왜곡하여 매출로 위장한 것은 명백한 위반이므로 거래소 조치는 타당합니다.", "articles": [], "principle": "변동 원천 오독 및 적발", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세금 납부 여부와 무관하게 분식입니다.", "articles": [], "principle": "세금 무관", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "정부의 사유재산 몰수는 불가합니다.", "articles": [], "principle": "재산 몰수", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "행정 감독 면제는 위법입니다.", "articles": [], "principle": "감독 면제 부재", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "(시나리오) 대학생 P는 감정평가사 1차 회계학을 공부하던 중 \"재무보고서는 정확한 서술보다 모형에 근거한다\"는 구절에 의문을 가졌다. P가 개념체계의 목적에 비추어 내린 올바른 학습 결론으로 옳은 것은?",
        "options": [
          "① 모형에 근거하므로, 재무제표의 모든 숫자는 회계사가 마음대로 적는 임의의 낙서에 불과하다.",
          "② 재무제표는 미래의 대손이나 퇴직급여 추정 등이 포함되므로 수학적 절대 정확성은 불가능하며, 다만 합리적인 개념(모형)을 통해 유용성을 달성하고자 노력하는 최적의 목표임을 이해한다.",
          "③ 정확하지 않으므로 재무제표를 바탕으로 한 어떠한 기업 분석도 시간 낭비이다.",
          "④ 작성자가 처벌받지 않도록 하기 위해 모형의 사용을 즉각 전면 금지시켜야 한다.",
          "⑤ 세무서장이 지정해 주는 단일 공식을 대입하여 작성함으로써 정확성 한계를 완전히 해결할 수 있다."
        ],
        "answer": "2",
        "explanation": "② 재무제표는 본질적으로 추정과 판단, 모형에 크게 의존합니다. 이는 한계가 아닌 회계의 내재적 성격이며, 개념체계는 이 추정과 판단이 합리적이고 일관된 궤도 위에서 이뤄지도록 안내하는 유용한 목표 역할을 합니다.\n\n[오답 해설]\n① 자의적인 낙서가 아닌, 합리적이고 객관적인 공식을 준수합니다.\n③ 정확성의 한계가 있을 뿐, 여전히 가장 유용한 미래 추정의 피드백을 제공합니다.\n④ 모형 사용 금지는 회계 작성 자체를 마비시킵니다.\n⑤ 세무서장 지정 공식이 재무회계의 지향점이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "임의의 낙서가 아닙니다.", "articles": [], "principle": "회계의 객관성", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서의 한계와 지향 목표로서의 성격을 올바르게 이해한 기술입니다.", "articles": [], "principle": "추정 판단의 올바른 해석", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "기업 분석에 핵심적으로 유용합니다.", "articles": [], "principle": "정보 유용성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "모형 사용은 필수적입니다.", "articles": [], "principle": "모형 사용", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세무 공식 대입은 해결책이 아닙니다.", "articles": [], "principle": "세법", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "(시나리오) 대여 주체인 Q 은행은 R사에 대하여 대형 신규 대출을 승인할지 심사하고 있다. Q 은행이 R사의 일반목적재무보고서 상 '청구권(부채와 자본)' 정보를 통해 R사의 지급능력(Solvency)을 적절하게 평가하여 의사결정을 내린 과정으로 옳은 것은?",
        "options": [
          "① R사의 장부상 청구권 총액이 0원이므로 리스크가 전혀 없다고 판단하고 무담보로 대출을 자동 승인한다.",
          "② R사의 청구권 만기 구조와 단장기 부채 비율을 정밀 분석하여, R사가 미래에 추가 자금을 조달하거나 만기 부채를 상환할 수 있는 지급 능력을 합리적으로 평가하여 대출 한도를 설정한다.",
          "③ R사의 대주주에게 사법 징역형 연대 서약서를 작성해 제출하도록 강제하여 승인한다.",
          "④ R사의 자산 가액을 임의로 두 배 늘린 가짜 재무제표를 주석에 첨부하도록 타협하여 승인한다.",
          "⑤ R사의 영업 비밀 차단권을 은행이 직접 인수하여 장부 외 거래로 마감한다."
        ],
        "answer": "2",
        "explanation": "② 보고기업에 대한 청구권(부채 구조) 정보는 기업의 채무 만기 구조와 상환 조건을 나타내므로, 자금을 대여하려는 은행이 기업의 단장기 지급능력 및 자금 유동성을 감시하는 유용한 근거가 됩니다.\n\n[오답 해설]\n① 청구권 0원 상태가 대출 무담보 자동 승인의 정당한 사유가 아닙니다.\n③ 사법 징역형 서약서 강제 조치 등은 불법입니다.\n④ 가짜 재무제표 작성 타협은 명백한 불법 및 분식 공모입니다.\n⑤ 비밀 차단권 인수 등은 존재하지 않는 지문입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "무담보 자동 승인은 리스크 분석 오류입니다.", "articles": [], "principle": "대출 심사", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "청구권 정보의 유용한 흐름을 활용하여 기업의 장단기 채무 대응력과 추가 자금 조달 능력을 합리적으로 평가했습니다.", "articles": [], "principle": "청구권 정보와 지급능력 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사법 서약 강제는 불법입니다.", "articles": [], "principle": "사법 강제", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "분식 공모는 불법입니다.", "articles": [], "principle": "분식 공모", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "차단권 인수는 관계없습니다.", "articles": [], "principle": "정보 차단", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "(시나리오) T사는 다음 주 법원의 강제 파산 경매 절차를 앞두고 있다. T사의 기말 재무제표 작성자 정 대리가 개념체계 상의 일반목적재무보고 목적에 근거해 수행해야 할 타당한 측정 의사결정은?",
        "options": [
          "① 계속기업가정은 영구 불변이므로 평소와 똑같이 역사적 원가로 기계장치 감가상각을 유지한다.",
          "② 계속기업 전제가 타당하지 않은 예외적 청산 상황이므로, 역사적 원가 대신 청산 가치 등 대체적 측정 기준으로 자산을 평가해 적절히 보고하고 이를 주석에 밝힌다.",
          "③ 파산이므로 재무보고서 제출 및 공시를 거부하고 장부를 무단 은닉한다.",
          "④ 기말 자산 전체를 임의로 0원으로 깎아서 전 주주에게 통보한다.",
          "⑤ 국세청에 법인세를 면제해 주면 감가상각 장부를 계속기업 기준으로 기재하겠다고 제안한다."
        ],
        "answer": "2",
        "explanation": "② 계속기업 전제가 무너진 청산 상태의 기업은 개념체계 목적에 비추어 역사적 원가 고수를 배제하고 대체적인 측정 기준(청산가치 등)으로 적절히 자산과 부채를 평가해 밝혀야 유용한 정보가 됩니다.\n\n[오답 해설]\n① 청산 예정 기업에 계속기업을 고수하는 것은 오류입니다.\n③ 장부 은닉 및 보고서 거부는 형사 위법입니다.\n④ 자의적인 0원 평가는 금지됩니다.\n⑤ 로비 시도는 불법입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "청산 시 역사적 원가 고수는 타당하지 않습니다.", "articles": [], "principle": "역사적 원가", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "계속기업 가정이 성립하지 않을 때에는 대안적 기준(청산가치 등)에 따라 작성하고 관련 사실을 밝혀야 합니다.", "articles": [], "principle": "계속기업 가정의 예외", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "장부 은닉 거부는 위법입니다.", "articles": [], "principle": "장부 은닉", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "임의 0원 소거는 위법입니다.", "articles": [], "principle": "자산 소거", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "로비는 불법입니다.", "articles": [], "principle": "로비", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "(시나리오) 자산 500억 원인 U사는 정부로부터 친환경 설비 구축을 조건으로 '무상 보조금 50억 원'을 지급받았다. U사의 회계팀 최 과장은 이 보조금 거래가 개념체계상 '재무성과'에 속하는지 '재무성과 외의 변동'인지 판단하려 한다. 최 과장의 분석 결과로 옳은 것은?",
        "options": [
          "① 주주와의 거래가 아니며 친환경 설비 운영에 따른 정부 보조금 수익 요건을 충족하므로, 이는 재무성과(수익) 범주에 속해 감가상각과 연동해 보고해야 한다.",
          "② 보조금은 회사의 주식을 발행해 얻은 자본금이므로 재무성과 외의 변동으로만 분류해야 한다.",
          "③ 보조금은 공짜 돈이므로 장부에 기재하지 않고 전액 사외 비밀 적립금으로 숨겨 둔다.",
          "④ 해당 거래 금액을 감사위원회의 사적 복지 비용 계정으로 즉시 대체 기록한다.",
          "⑤ 보조금 50억 원을 세법 상 면세 처리해 주지 않으면 결산서 작성을 전면 중단한다."
        ],
        "answer": "1",
        "explanation": "① 정부보조금은 주주(자본제공자)와의 자본 거래가 아닙니다. 친환경 기준을 만족하여 얻는 지원 혜택이므로 기준서(제1020호 등)에 따라 관련 감가상각 비용과 조화를 이루어 영업 수익(재무성과) 또는 자산차감으로 인식하는 것이 맞습니다.\n\n[오답 해설]\n② 지분상품이나 사채 발행이 아니므로 주주 자본금 성격이 아닙니다.\n③ 비밀 적립금 은닉은 불법입니다.\n④ 사적 복지비 대체는 횡령입니다.\n⑤ 법인세 비과세 협상을 이유로 결산을 거부할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": True, "why": "정부보조금은 주주 거래가 아니며 영업 성과와 대응되므로 재무성과에 연동해야 합니다.", "articles": [], "principle": "정부보조금의 재무성과 귀속", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "지분상품이나 채무발행이 아닙니다.", "articles": [], "principle": "지분상품", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "비밀 은닉은 위법입니다.", "articles": [], "principle": "장부 투명성", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "사적 유용은 횡령입니다.", "articles": [], "principle": "횡령 배임", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "결산 중단은 위법입니다.", "articles": [], "principle": "결산 의무", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "(시나리오) 투자자 K는 L사의 미래 현금유입 전망을 평가하기 위해 과거 현금흐름 정보와 발생주의 성과 정보를 함께 연동 분석하여 성과 추이를 도출했다. K가 개념체계에 비추어 올바른 판단을 내린 리포트 내용으로 옳은 것은?",
        "options": [
          "① \"과거현금흐름 정보가 발생주의 정보보다 100% 신뢰성이 높으므로 발생주의 장부는 리포트에서 전면 폐기한다.\"",
          "② \"발생기준 성과는 거래 시점의 실제 영업 성과를 보여주어 미래 현금유입 창출력을 평가하는 핵심을 이루고, 현금흐름 정보는 실제 자금의 유입 시점을 보완해 주므로 두 정보를 함께 분석하는 것이 미래 예측 시 오도를 예방한다.\"",
          "③ \"두 정보가 일치하지 않는 3억 원은 L사의 경영진이 고의로 횡령한 가짜 손실액이다.\"",
          "④ \"일치하지 않는 차액만큼 회사의 주가를 강제로 소급 하향 조정하도록 법률 건의를 한다.\"",
          "⑤ \"P사의 감가상각 장부를 현금주의로 통일하도록 금감원에 직접 행정 제소한다.\""
        ],
        "answer": "2",
        "explanation": "② 재무성과 정보(발생기준)와 현금흐름 정보(과거현금흐름)는 상호보완적으로 운영되며, 미래 예측 시 발생주의의 장기 예측력과 현금흐름의 실제 수지 분석을 함께 고려해야 의사결정의 오도를 피할 수 있습니다.\n\n[오답 해설]\n① 발생주의 장부 폐기 주장은 회계학적으로 부당합니다.\n③ 불일치 차액이 횡령 손실액이 아닙니다.\n④ 주가 임의 소급 하향 조정 건의는 사법 상 성립하지 않습니다.\n⑤ 현금주의로 감가상각 통일 제소는 불가능합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "발생주의 폐기는 완전한 오독입니다.", "articles": [], "principle": "발생주의 위상", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "두 정보의 상호보완적 특성을 잘 연동하여 미래 현금유입을 합리적으로 평가한 타당한 리포트 서술입니다.", "articles": [], "principle": "양 정보 연동 분석 적용", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "횡령액 판단은 오류입니다.", "articles": [], "principle": "횡령 판단 오류", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "주가 소급 조정은 사법 상 성립하지 않습니다.", "articles": [], "principle": "주가 조정", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "감가상각 현금주의 통일은 불가합니다.", "articles": [], "principle": "감가상각 회계", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },

    # =========================================================================
    # L4: 분석 및 박스형 다중 조합 (8문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s03-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "일반목적재무보고의 목적과 주요이용자의 지위에 관한 설명 중 옳은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 일반목적재무보고의 대상이 되는 주요이용자는 현재 및 잠재적 투자자, 대여자 및 기타 채권자이다.\nㄴ. 보고기업의 경영진도 재무 정보에 관심이 있으나, 내부에서 필요한 정보를 입수하므로 주요이용자에 해당하지 않는다.\nㄷ. 일반 대중이나 정부 규제기관도 보고서를 유용하게 여길 수 있으나, 재무보고서가 표방하는 주요이용자는 아니다.\nㄹ. 일반목적재무보고서는 주요이용자가 요구하는 모든 유용한 정보를 완벽하게 제공하지는 못하며 제공할 수도 없다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "5",
        "explanation": "⑤ 보기의 ㄱ, ㄴ, ㄷ, ㄹ은 모두 개념체계가 공식 규정하고 있는 일반목적재무보고의 대상자 범위와 내재적 한계에 대한 명백히 참인 지문들입니다.\n\n[보기 검증]\nㄱ. [참] 자원 제공 의사결정을 하는 자원제공자가 주요 이용자입니다.\nㄴ. [참] 경영진은 내부 획득자이므로 주요이용자에서 제외됩니다.\nㄷ. [참] 규제기관이나 대중은 주요 대상이 아닙니다.\nㄹ. [참] 보고서의 태생적 범위 한계에 관한 옳은 기술입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ, ㄹ 모두 참인 옳은 기술입니다.", "articles": [], "principle": "재무보고 대상자 및 한계", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "일반목적재무보고서가 제공하는 기본 정보 유형과 의의에 관한 분석 중 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 보고기업의 경제적 자원 및 보고기업에 대한 청구권 정보(재무상태)를 제공한다.\nㄴ. 자원과 청구권의 변동 정보는 기업의 재무성과, 그리고 지분/채무 발행 등 성과 외 거래의 영향 정보를 포함한다.\nㄷ. 발생기준 재무성과 정보는 과거 및 미래 성과, 그리고 경영진 수탁책임을 평가하는 데 현금 수지 단독 정보보다 우월하다.\nㄹ. 과거 현금흐름 정보는 기업의 미래 순현금유입 창출 능력과 경영진 수탁책임 적정성을 함께 분석하는 데 도움을 준다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "5",
        "explanation": "⑤ 보기의 ㄱ, ㄴ, ㄷ, ㄹ은 모두 재무제표가 공시해야 하는 제공 정보들의 정의와 고유한 의의에 대한 완전히 참인 조문 설명입니다.\n\n[보기 검증]\nㄱ. [참] 재무상태 정보 제공 의무 조항입니다.\nㄴ. [참] 자원 변동 2대 원천 분류 조항입니다.\nㄷ. [참] 발생기준 정보의 평가 우월성 조항입니다.\nㄹ. [참] 현금흐름 정보의 수탁책임 연동 지침입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ, ㄹ 모두 옳은 참 지문입니다.", "articles": [], "principle": "재무보고 제공 정보 분석", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "발생주의 회계(Accrual Accounting)가 반영된 재무성과 정보의 유용성 분석 중 옳은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 거래와 사건 및 상황이 경제적자원 및 청구권에 미친 실제 영향을 비록 현금의 수지 시점이 다르더라도 그 영향 발생 기간에 보여준다.\nㄴ. 발생주의는 자의성이 높아 현금 흐름 정보 예측을 방해하므로 주석에서만 예외적 사용이 권장된다.\nㄷ. 발생기준 성과 정보는 기간 중의 현금 수지와 성과를 유기적으로 구별하게 하여 경영진의 수탁책임 이행을 감독하는 데 더 나은 근거를 제공한다.",
        "options": [
          "① ㄱ",
          "② ㄱ, ㄴ",
          "③ ㄱ, ㄷ",
          "④ ㄴ, ㄷ",
          "⑤ ㄱ, ㄴ, ㄷ"
        ],
        "answer": "3",
        "explanation": "③ 보기 중 옳은 지문은 ㄱ과 ㄷ입니다. ㄴ의 경우 발생주의가 예측을 방해해 주석에서만 제한적으로 사용 권장된다는 설명은 발생주의의 기본적 위상을 심각하게 부정하는 잘못된 오답 지문입니다.\n\n[보기 검증]\nㄱ. [참] 발생주의의 본질적 회계 기간 귀속 원칙입니다.\nㄴ. [거짓] 발생주의는 필수 본문 재무제표의 기본 뼈대이며 주석 제한 대상이 아닙니다.\nㄷ. [참] 수탁책임 감독의 우수성을 입증하는 참 지문입니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ은 틀린 설명입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ과 ㄷ이 발생주의 회계의 유용성을 입증하는 옳은 설명입니다.", "articles": [], "principle": "발생주의 유용성 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ은 틀린 설명입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ 때문에 틀렸습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "일반목적재무보고서 상의 가치평가 및 정확성의 한계에 대한 복합 지문 중 옳은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 재무보고서는 보고기업의 시장 가치를 직접 계산하여 정확하게 전달하기 위해 고안된 것이 아니다.\nㄴ. 보고서의 순자산 가액이 주식 시가총액과 일치하지 않는 것은 회계장부의 본질적 기술 오류에 속한다.\nㄷ. 재무보고서는 상당 부분 정확한 서술보다는 합리적 추정, 판단 및 모형에 근거하여 작성된다.\nㄹ. 추정치 사용이 재무제표 작성에 개입되더라도 그것이 명확히 주석 기재되는 한 정보 유용성을 해치지 않는다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄷ, ㄹ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ 보기 중 옳은 지문은 ㄱ, ㄷ, ㄹ입니다. ㄴ의 경우 시가와의 불일치를 회계 기술 오류로 단정 지은 것은 자본 괴리의 본질적 이유를 오해한 오답 지문이므로 틀렸습니다.\n\n[보기 검증]\nㄱ. [참] 가치 직접 제시는 설계 목적이 아닙니다.\nㄴ. [거짓] 불일치는 원가주의 및 보수주의 적용의 정상적 결과입니다.\nㄷ. [참] 추정, 판단, 모형 의존성을 정직하게 설명합니다.\nㄹ. [참] 투명성이 동반된 추정은 유용성을 훼손하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ은 틀린 설명이며, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄷ, ㄹ 지문은 개념체계 상의 가치평가 및 정확성 한계를 바르게 설명합니다.", "articles": [], "principle": "가치평가 및 정확성 지침", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ은 틀린 설명입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄴ 때문에 틀렸습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "일반목적재무보고가 제공하는 '변동 원천 구분'에 관한 복합 설명 중 옳지 않은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 기말 유형자산의 재평가 평가이익 계상은 재무성과에 따른 변동에 해당한다.\nㄴ. 당기 중 주주 대상 유상증자를 통해 10억 원 자본금을 조달한 것은 재무성과에 따른 변동이다.\nㄷ. 미래 순현금유입액 전망을 올바르게 평가하려면 성과에 따른 변동과 성과 외 변동을 구별해 파악해야 한다.\nㄹ. 지분상품 발행 거래 정보는 단지 자본금의 내역 변동일 뿐, 미래 성과 예측에 아무런 유용한 정보를 주지 않는다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄷ, ㄹ",
          "④ ㄱ, ㄷ",
          "⑤ ㄴ, ㄷ, ㄹ"
        ],
        "answer": "2",
        "explanation": "② 옳지 않은 오답 지문은 ㄴ과 ㄹ입니다. 유상증자는 주주와의 자본 거래이므로 '재무성과 외의 변동 원인'에 속해야 하며, 지분상품 발행 정보 또한 미래 성과 의미를 해석하는 데 매우 유용하므로 배제되어선 안 됩니다.\n\n[보기 검증]\nㄱ. [참] 평가이익은 성과 수익입니다.\nㄴ. [거짓] 유상증자는 자본거래이므로 성과 외 변동입니다.\nㄷ. [참] 두 변동의 명확한 구별은 경영진 평가에 필수입니다.\nㄹ. [거짓] 미래 성과에 주는 의미를 정보이용자가 완전히 이해하게 돕습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄱ은 옳은 설명입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄴ과 ㄹ은 틀린 오답 진술이므로 옳지 않은 항목 조합에 해당합니다.", "articles": [], "principle": "변동 원천 오독 진단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ은 옳은 설명입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ은 모두 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ은 옳은 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "일반목적재무보고와 세법(Tax Law)의 구별 관계에 대한 복합 지문 중 옳은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 재무제표는 세법이 아닌 K-IFRS 기준서에 따라 작성하여 공시해야 투명성이 인정된다.\nㄴ. 세법 기준과의 충돌을 이유로 감가상각비를 기준서와 다르게 세법대로 수정공시하는 것은 위반이다.\nㄷ. 세무조정 명세서 작성을 통한 법인세 납부액 계산은 외부 재무보고서 공시와 독립적으로 처리된다.\nㄹ. 개념체계가 명시하는 발생주의 회계는 조세 감세를 위한 자의적 목적에 휘둘려서는 안 된다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "5",
        "explanation": "⑤ 보기의 ㄱ, ㄴ, ㄷ, ㄹ은 모두 일반목적재무보고와 세무회계(세법)의 법적·개념적 독립성과 상호처리 원칙에 대한 참인 지문들입니다.\n\n[보기 검증]\nㄱ. [참] K-IFRS 준수가 외부공시의 적법 요건입니다.\nㄴ. [참] 세법에 맞춰 장부를 강제 훼손하는 것은 회계 오류입니다.\nㄷ. [참] 세무조정은 독립적인 과세 소득 계산 절차입니다.\nㄹ. [참] 조세 회피 전용으로 발생주의 기간 귀속을 임의 조작하지 못합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ, ㄹ 모두 참인 옳은 기술입니다.", "articles": [], "principle": "세법과 재무보고의 독립성", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "개념체계상 '청구권(Claims)' 정보가 제공하는 재무적 유용성 지문 중 옳은 것만을 모두 고른 것은?\n\n[보기]\nㄱ. 청구권 정보(부채와 자본 구조)는 기업의 유동성 및 장단기 지급능력 평가에 필수적이다.\nㄴ. 만기나 상환 조건 같은 청구권 정보는 기업의 채무 만기 충당 능력을 예측하게 해 준다.\nㄷ. 청구권 정보는 사적 계약상 발생한 채무를 법적으로 무상 변제 탕감해 주는 척도이다.\nㄹ. 청구권 정보를 통해 정보이용자는 자원을 추가 조달하거나 배분할 수 있는 능력을 식별할 수 있다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄹ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "3",
        "explanation": "③ 보기 중 옳은 설명은 ㄱ, ㄴ, ㄹ입니다. ㄷ의 경우 청구권 정보가 사적 계약 채무를 법적으로 무상 탕감하는 척도라는 설명은 개념체계의 회계학적 기능을 완전히 오도한 오답 지문이므로 틀렸습니다.\n\n[보기 검증]\nㄱ. [참] 유동성 및 장단기 지급력 평가의 토대입니다.\nㄴ. [참] 부채의 만기 조건이 유동성 판단 지표가 됩니다.\nㄷ. [거짓] 채무 탕감 법률서가 아닙니다.\nㄹ. [참] 추가 자금조달(부채/자본 조달) 여력 판단을 돕습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄴ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄹ 지문은 청구권 정보의 재무 분석적 유용성을 바르게 서술합니다.", "articles": [], "principle": "청구권 정보의 유용성 식별", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ은 틀린 기술입니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄷ 때문에 틀렸습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "일반목적재무보고의 성격과 관련해 '추정과 판단 및 모형'이 지향해야 하는 가치로 옳은 것을 모두 고른 것은?\n\n[보기]\nㄱ. 측정불확실성이 아무리 높더라도 그것이 유용한 재무정보의 제공을 무조건 방해하는 것은 아니다.\nㄴ. 추정이 일관되고 주석을 통해 한계와 산출 절차가 투명하게 기술되면 정보의 질이 충실하다고 평가한다.\nㄷ. 경영진은 이익 관리를 위해 모형을 임의 변경하지 않고 정당한 개념에 근거하여 목표에 다다르도록 노력해야 한다.\nㄹ. 완벽한 정확성은 달성하기 어려우나 개념체계 원칙을 최적의 지향 목표(Goal)로 삼아 준수해야 한다.",
        "options": [
          "① ㄱ, ㄴ",
          "② ㄴ, ㄹ",
          "③ ㄱ, ㄴ, ㄷ",
          "④ ㄴ, ㄷ, ㄹ",
          "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
        ],
        "answer": "5",
        "explanation": "⑤ 보기의 ㄱ, ㄴ, ㄷ, ㄹ은 모두 재무보고서가 추정과 모형을 반영할 때 추구해야 하는 합리성, 일관성 및 지향 지위의 당위성에 관한 완전히 참인 설명들입니다.\n\n[보기 검증]\nㄱ. [참] 측정불확실성과 유용성은 별개로 존재 가능합니다.\nㄴ. [참] 투명한 기재는 표현충실성을 극대화합니다.\nㄷ. [참] 실적 조작 목적의 임의 모형 변경은 금지됩니다.\nㄹ. [참] 개념적 원칙이 최적의 공동 목표(지향점)가 됨을 기술합니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "ㄷ, ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ, ㄷ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄹ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "ㄱ 항목이 누락되었습니다.", "articles": [], "principle": "조합 판단", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "ㄱ, ㄴ, ㄷ, ㄹ 조항 모두 참인 옳은 기술입니다.", "articles": [], "principle": "추정 판단의 논리적 가치", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },

    # =========================================================================
    # L5: 고난도 심화 (2문항)
    # =========================================================================
    {
        "id": "practice-accounting-ch01s03-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "발생주의 회계(Accrual Accounting)가 반영된 재무성과 정보가 과거 현금 수지 단독 정보보다 기업의 과거 및 미래 성과를 평가하고 경영진의 수탁책임(Stewardship)을 감독하는 데 논리적으로 우월한 정보를 제공하는 이유에 대한 가장 타당한 학술적 분석은?",
        "options": [
          "① 발생주의는 현금의 흐름을 인위적으로 통제하여 적자 기업을 흑자 기업으로 영구 조작하여 주가를 방어할 기회를 주기 때문이다.",
          "② 결제 시점(현금 수급 시점)에 얽매이지 않고, 한 기간 동안 실제로 자원을 획득하고 투입하여 경제적 청구권을 변동시킨 사건의 실질적 영향(수익의 실현과 비용의 발생 대응)을 정확한 발생 기간에 매핑하여 제공함으로써, 기업 성과 창출력과 수탁 적정성의 실질 분석을 가능케 하기 때문이다.",
          "③ 발생주의를 적용하면 당기순이익이 100% 현금으로 즉시 실현되어 부도 가능성을 완전 차단해 주기 때문이다.",
          "④ 현금 수지만을 계상할 때 수반되는 세법 상의 모든 법인세 신고 의무를 완전히 면제 처리해 주기 때문이다.",
          "⑤ 발생주의가 현금 흐름 정보의 소급 입법 제소를 통해 현금주의를 완전히 무효화시키는 효력이 있기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 발생기준 회계는 거래와 상황이 보고기업의 경제적 자원 및 청구권에 미친 영향을 발생 시점에 보여주므로, 단순 현금 수지의 기간 시차 왜곡(예: 외상 거래나 선급 거래로 인한 현금 유출입 시점 차이)을 제거하여 장기 실적 성과와 경영 책임 이행 정도를 훨씬 공정하고 일관되게 감시하도록 돕습니다.\n\n[오답 해설]\n① 흑자 기업 조작 주장은 회계 부정을 옹호하는 잘못된 서술입니다.\n③ 순이익이 100% 현금 실현되거나 부도를 차단하지는 못합니다.\n④ 세법 신고 면제 특권은 없습니다.\n⑤ 현금주의를 법적으로 취소 무효화시키는 소송 효력을 갖지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "흑자 조작을 옹호하는 설명은 완전한 회계 부정입니다.", "articles": [], "principle": "분식회계 배제", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "결제 시점 차이로 발생하는 왜곡을 제거하고 발생 시점에 매핑하여 성과와 책임 평가의 합리성을 높입니다.", "articles": [], "principle": "발생주의의 논리적 우월성 입증", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "부도 가능성을 100% 차단해 주지는 못합니다.", "articles": [], "principle": "부도 리스크", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "세제 신고 면제 특권이 없습니다.", "articles": [], "principle": "세금", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "현금주의를 소송 무효화하지 못합니다.", "articles": [], "principle": "회계법규", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
          }
        }
    },
    {
        "id": "practice-accounting-ch01s03-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "일반목적재무보고서가 보고기업의 가치(Value of Reporting Entity)를 직접 계산하여 보여주지 못하는 한계 상황 속에서도, 정보이용자의 경제적 의사결정에 여전히 유의미한 가치(의사결정 차이)를 제공하는 개념적 경로에 관한 비판적 분석으로 가장 옳은 것은?",
        "options": [
          "① 가치를 보여주지 않는 보고서는 완전히 무용한 문서이므로, 이용자는 오직 당일의 시장 거래 주가에만 근거해 임의 투자를 단행하는 경로를 밟는다.",
          "② 재무보고서는 가치평가서가 아니므로 가치를 직접 제시하지 않으나, 가치의 원천이 되는 미래 순현금유입 창출의 기반(경제적 자원의 종류와 성격, 청구권 구조, 기간 중 발생 성과 및 현금흐름 추이)을 정직하게 공시함으로써 이용자 스스로 가치를 정확히 '추정'하도록 돕는 유기적 가교 역할을 수행한다.",
          "③ 보고서 상의 순자산 가액이 주총의 3분의 2 동의를 얻어 강제로 시장 시가와 병합 고정 공시되는 정당한 사법적 경로이다.",
          "④ 해당 보고서를 국세청이 강제 개입하여 법인세를 100% 탕감하는 핑계 자료로 활용하는 세무 상의 우회 경로이다.",
          "⑤ 기존 기준서가 상충할 때마다 작성자가 임의로 가공 손익을 기재하여 시장 참여자를 속여 이익을 주는 경로이다."
        ],
        "answer": "2",
        "explanation": "② 일반목적재무보고는 직접적인 가치평가서의 지위를 갖지는 않으나, 가치를 구성하는 핵심 경제적 입력 요인들(자원 및 청구권, 이들의 변동, 재무 성과 및 현금흐름)을 합리적으로 제공해 줌으로써 이용자가 자기 책임 하에 가치를 분석하고 추정하는 논리적 연결 통로가 되어 줍니다.\n\n[오답 해설]\n① 무용한 문서 격하 설명은 개념체계의 목적에 전면 위배됩니다.\n③ 주총 의결을 통해 순자산을 시가와 강제 병합 소급하는 법은 없습니다.\n④ 세무 감면 우회 도구로 악용되지 않습니다.\n⑤ 가공 손익 기재를 옹호하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
          {"correct": False, "why": "재무보고서를 무용지물로 판단한 서술은 오류입니다.", "articles": [], "principle": "재무보고 가치", "case": {"holding": "", "no": None}},
          {"correct": True, "why": "재무보고서는 가치를 직접 제시하지 않으나, 가치 추정을 위한 핵심적인 자원과 성과 정보를 객관적으로 풍부히 제공합니다.", "articles": [], "principle": "기업가치 추정과 재무보고 역할", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "시가와 강제 병합 고정은 불가합니다.", "articles": [], "principle": "자산 평가", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "법인세 감면 핑계 활용은 불가합니다.", "articles": [], "principle": "세제", "case": {"holding": "", "no": None}},
          {"correct": False, "why": "가공 손익 기재 옹호는 분식회계입니다.", "articles": [], "principle": "분식회계", "case": {"holding": "", "no": None}}
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
            "item": "3절 일반목적재무보고"
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
