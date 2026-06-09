# -*- coding: utf-8 -*-
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

part1_questions = [
    # =========================================================================
    # L1: 기초 개념 (10문항, 1101~1110번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s04-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1036호 '자산손상' 기준서에 의거하여, 자산에 대한 손상차손(Impairment loss)을 장부에 인식하여야 하는 기본적인 회계적 발생 요건은?",
        "options": [
            "① 자산의 취득원가가 기말 공정가치보다 낮아졌을 때",
            "② 자산의 장부금액이 회수가능액을 초과할 때",
            "③ 자산의 감가상각누계액이 취득원가의 50%를 넘어섰을 때",
            "④ 자산의 순공정가치가 사용가치보다 낮아졌을 때",
            "⑤ 자산의 시장 이자율이 전년 대비 소폭 하락했을 때"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 59에 따르면, 자산의 장부금액이 회수가능액을 초과하는 경우에만 장부금액을 회수가능액으로 감액하고 그 차액을 손상차손으로 인식합니다.\n\n[오답 해설]\n① 취득원가가 공정가치보다 낮아지면 평가이익 상황이므로 손상과 무관합니다.\n③ 감가상각비의 누적 수준은 손상차손 인식의 절대적 기준이 아닙니다.\n④ 순공정가치가 사용가치보다 낮더라도 장부금액이 회수가능액 이하라면 손상을 인식하지 않습니다.\n⑤ 시장 이자율 하락은 오히려 사용가치(현재가치)를 높여 회수가능액을 상승시키는 요인입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "평가이익 상황을 묘사하여 오답입니다.", "articles": [], "principle": "손상차손의 인식 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산의 장부상 가치(장부금액)가 실제 건져 올릴 수 있는 가치(회수가능액)를 초과할 때 그 차액을 자산의 직접 감액 혹은 평가차감 계정으로 털어내 손상차손 처리한다는 기본 요건에 정밀 부합합니다.", "articles": ["K-IFRS 제1036호 문단 59"], "principle": "손상차손의 인식 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감누의 비율은 손상차손 인식 요건과 무관합니다.", "articles": [], "principle": "손상차손의 인식 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회수가능액은 두 가치 중 큰 금액을 쓰므로 상호 대조는 손상 발생의 직접 요인이 아닙니다.", "articles": [], "principle": "손상차손의 인식 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자율 하락은 회수가능가치를 올리는 긍정적 지표이므로 오답입니다.", "articles": [], "principle": "손상차손의 인식 요건", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "K-IFRS 상 유형자산의 손상차손 계산의 기준이 되는 '회수가능액(Recoverable amount)'의 정의로 가장 올바른 것은?",
        "options": [
            "① 순공정가치와 사용가치 중 더 큰 금액",
            "② 순공정가치와 사용가치 중 더 작은 금액",
            "③ 순공정가치와 사용가치의 단순 산술평균액",
            "④ 기말 현재 자산의 보험가입 금액",
            "⑤ 자산의 최초 역사적 취득원가에 법인세 효과를 제한 금액"
        ],
        "answer": "1",
        "explanation": "① K-IFRS 제1036호 문단 6에 따르면, 자산 또는 현금창출단위의 회수가능액은 그 자산의 '순공정가치'와 '사용가치' 중 더 큰 금액(Max)으로 규정되어 있습니다.\n\n[오답 해설]\n② 더 작은 금액(Min)이 아닌 더 큰 금액입니다.\n③ 산술평균을 적용하지 않습니다.\n④ 보험가액은 회계상의 회수가능액 지표가 아닙니다.\n⑤ 역사적 취득원가는 손상 검사의 비교 가액이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "회수가능액은 순공정가치와 사용가치 중 더 큰 금액(Max)으로 선택하여 자산의 효익을 가장 충실히 묘사하도록 한 규정에 부합합니다.", "articles": ["K-IFRS 제1036호 문단 6"], "principle": "회수가능액의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "더 작은 금액(Min)으로 명시하여 규정에 위배됩니다.", "articles": ["K-IFRS 제1036호 문단 6"], "principle": "회수가능액의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평균 계산은 기준서에 존재하지 않습니다.", "articles": [], "principle": "회수가능액의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보험 관련 금액은 회계 측정 기준과 무관합니다.", "articles": [], "principle": "회수가능액의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득가 및 법인세 효과 결합설은 임의의 오답입니다.", "articles": [], "principle": "회수가능액의 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "회수가능액 구성요소 중 '순공정가치(Fair value less costs of disposal)'가 의미하는 기장 상의 정확한 정의는?",
        "options": [
            "① 공정가치에서 그 자산의 폐기 시 수거 비용을 더한 금액",
            "② 공정가치에서 자산의 처분(매각)과 직접 관련하여 발생하는 부대원가를 차감한 금액",
            "③ 기말 현재 기계장치의 미상각 잔존 역사적 원가",
            "④ 외부 감정평가금액의 70% 고정 할인 가액",
            "⑤ 취득원가에 매년의 세무조정 비용을 가산한 금액"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 6에 의거, 순공정가치는 합리적인 판단력과 거래 의사가 있는 독립된 당사자 사이의 거래에서 자산의 매각으로부터 얻을 수 있는 금액(공정가치)에서 처분부대원가(매각과 직접 관련된 거래원가)를 차감한 금액을 뜻합니다.\n\n[오답 해설]\n① 폐기 시 비용을 더하지 않고 처분 비용을 뺍니다.\n③ 역사적 원가 잔액은 장부금액이지 순공정가치가 아닙니다.\n④ 고정 할인 가액 70% 조항은 없습니다.\n⑤ 세무조정 비용 가산설은 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수거비를 더하는 것이 아니라 처분 비용을 제해야 하므로 정반대 진술입니다.", "articles": [], "principle": "순공정가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치에서 처분부대원가(직접적인 매각 원가)를 제하여 순수한 유입 예상액을 유도하는 정의에 정확히 일치합니다.", "articles": ["K-IFRS 제1036호 문단 6"], "principle": "순공정가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적 원가 잔액은 장부금액이므로 틀렸습니다.", "articles": [], "principle": "순공정가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특정 비율 70% 깎는 조항은 기준서에 없습니다.", "articles": [], "principle": "순공정가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득세 및 세무조정 비용 가산과는 무관합니다.", "articles": [], "principle": "순공정가치의 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "회수가능액 구성요소 중 '사용가치(Value in use)'의 올바른 산출 기준은?",
        "options": [
            "① 기중에 발생한 실제 현금 매출액의 총합",
            "② 자산에서 얻을 것으로 예상되는 미래현금흐름의 현재가치",
            "③ 자산의 강제 청산 시 유입될 청산가치 명목액",
            "④ 경쟁사가 동일한 자산을 매입할 때 지불할 것으로 추정되는 원가",
            "⑤ 기말 현재 자산을 새로 다시 짓는 데 소요될 재조달원가"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 6에 따르면, 사용가치는 자산이나 현금창출단위에서 얻을 것으로 예상되는 미래현금흐름의 현재가치(할인된 금액)로 측정됩니다.\n\n[오답 해설]\n① 역사적 매출 총액이 아닌 미래 예상 현금흐름 기준입니다.\n③ 청산가치나 ④ 경쟁사 취득원가, ⑤ 재조달원가는 사용가치의 정의와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지나간 역사적 현금 매출액 합산은 오답입니다.", "articles": [], "principle": "사용가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산을 계속 사용함에 따라 발생할 미래의 현금흐름을 시간가치 할인율로 땡겨 현재가치화한 금액이라는 정의에 완벽히 부합합니다.", "articles": ["K-IFRS 제1036호 문단 6"], "principle": "사용가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "청산가치는 자산 사용을 계속하는 전제인 사용가치와 실질이 다릅니다.", "articles": [], "principle": "사용가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대체 취득가 성격은 사용가치 정의에 어긋납니다.", "articles": [], "principle": "사용가치의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재조달원가는 원가법 평가 시 쓰는 개념입니다.", "articles": [], "principle": "사용가치의 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "유형자산에 대해 손상차손을 기장하여야 하는 징후(Indicator)가 존재하는지 여부를 검토하는 주기에 관한 K-IFRS 상의 원칙은?",
        "options": [
            "① 10년에 한 번 감사인 지적이 있을 때에만 이행한다.",
            "② 매 보고기간 말마다 자산손상을 시사하는 징후가 있는지를 검토하여야 한다.",
            "③ 매달 임의로 날짜를 지정하여 상시 검토한다.",
            "④ 공정가치가 최초 취득가의 3배를 넘어설 때에만 평가한다.",
            "⑤ 감가상각이 전액 완료된 시점에만 일괄 검토한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 9에 따라, 기업은 매 보고기간 말마다 자산손상을 시사하는 징후가 있는지를 검토하여야 하며, 그러한 징후가 있는 경우에만 당해 자산의 회수가능액을 정밀하게 추정하여 손상을 인식합니다.\n\n[오답 해설]\n① 10년 주기는 너무 길어 재무적 정보 신뢰성을 해칩니다.\n③ 매달 정밀 검증은 과도한 운영 비용을 유발합니다.\n④ 공정가치 급등(3배 등) 시에는 손상 징후가 아닌 재평가 징후에 가깝습니다.\n⑤ 감가상각 도중에도 손상 징후가 있으면 당연히 검사해야 하므로 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지나치게 긴 임의 주기는 재무보고 목적에 어긋납니다.", "articles": [], "principle": "손상 징후 검토의 주기", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "매 보고기간 말(매 회계연도 결산일)마다 징후 존재 유무를 확인하는 것이 규정에 완벽히 일치합니다.", "articles": ["K-IFRS 제1036호 문단 9"], "principle": "손상 징후 검토의 주기", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "월간 상시 검토 의무는 실무적 편익 대비 비용 측면에서 규정되어 있지 않습니다.", "articles": [], "principle": "손상 징후 검토의 주기", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가치 상승 시에는 손상 징후가 발생하지 않습니다.", "articles": [], "principle": "손상 징후 검토의 주기", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각 완료 전 노후 기간 도중에도 징후는 나타날 수 있으므로 오답입니다.", "articles": [], "principle": "손상 징후 검토의 주기", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "다음 중 K-IFRS 제1036호가 규정하는 손상 징후 판단의 정보원 중 기업의 '내부 보고' 또는 내부적 정보(Internal sources of information)에 해당하는 것은?",
        "options": [
            "① 당기 중 자산의 시장가치가 시간 경과나 정상적인 사용에 따라 기대되는 수준보다 유의적으로 더 하락한 경우",
            "② 기술, 시장, 경제 또는 법률 환경에 중대한 불리한 변화가 일어난 경우",
            "③ 자산의 시장 이자율이 상승하여 자산의 사용가치를 계산하는 데 쓰일 할인율이 올라간 경우",
            "④ 자산의 진부화나 물리적 손상이 명백히 드러나는 증거가 있는 경우",
            "⑤ 회사의 순자산 장부금액이 기말 주식 시가총액을 초과하는 경우"
        ],
        "answer": "4",
        "explanation": "④ 진부화나 물리적 손상의 발생은 자산 자체의 물리적 실태를 내부적으로 확인하여 입증되는 정보이므로 내부 정보원에 해당합니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 모두 기업 외부의 거시경제, 시장 지표, 주식시장 시가총액 비교 등에서 포착되는 전형적인 외부 정보원(External sources of information)들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "시장가치 하락은 외부 관찰 가능 지표이므로 외부 정보원입니다.", "articles": ["K-IFRS 제1036호 문단 12"], "principle": "손상 징후 정보원의 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법률 및 환경 변화는 외부 시장 요인이므로 외부 정보원입니다.", "articles": ["K-IFRS 제1036호 문단 12"], "principle": "손상 징후 정보원의 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시장 이자율 변동은 거시 금융 요인이므로 외부 정보원입니다.", "articles": ["K-IFRS 제1036호 문단 12"], "principle": "손상 징후 정보원의 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부품의 물리적 파손 및 작동 불능(진부화) 등은 회사 내부 생산 관리나 공장에서 보고되는 핵심 내부 정보원임을 올바르게 발라냈습니다.", "articles": ["K-IFRS 제1036호 문단 12"], "principle": "손상 징후 정보원의 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가총액 비교는 주식시장(외부) 평가 정보이므로 외부 정보원입니다.", "articles": ["K-IFRS 제1036호 문단 12"], "principle": "손상 징후 정보원의 분류", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "유형자산에 대해 '원가모형'을 적용하는 경우, 기말에 인식하는 손상차손에 대해 자산의 역사적 취득원가 계정을 직접 깎지 않고 대변에 표시하는 차감적 평가 계정의 명칭으로 옳은 것은?",
        "options": [
            "① 감가상각누계액",
            "② 재평가손실누계액",
            "③ 손상차손누계액",
            "④ 대손충당금",
            "⑤ 복구충당부채"
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 하에서 손상차손을 직접법(자산 원가 차감)이 아닌 간접법으로 기장하는 경우, 대변에 '손상차손누계액' 계정을 사용하여 재무상태표 상 취득원가 밑에서 감액 평가 계정으로 표시합니다.\n\n[오답 해설]\n① 감가상각누계액은 노후화 배분 누적액입니다.\n② 재평가손실누계액이라는 자본 차감 누계 계정은 공식 명칭이 아닙니다.\n④ 대손충당금은 수취채권 평가 계정입니다.\n⑤ 복구충당부채는 미래 해체 의무 관련 부채 계정입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "정상 감가상각비 누적액 표시 계정이므로 오답입니다.", "articles": [], "principle": "손상차손 인식 시 차감 계정의 명칭", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "존재하지 않는 가상의 계정 과목입니다.", "articles": [], "principle": "손상차손 인식 시 차감 계정의 명칭", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "원가모형 유형자산 손상차손 계상 시 대변의 차감 평가 계정은 '손상차손누계액'임을 명확히 서술했습니다.", "articles": ["K-IFRS 제1036호"], "principle": "손상차손 인식 시 차감 계정의 명칭", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "채권용 충당금 계정이므로 틀렸습니다.", "articles": [], "principle": "손상차손 인식 시 차감 계정의 명칭", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "충당부채는 부채 항목이므로 자산 차감 평가 계정이 아닙니다.", "articles": [], "principle": "손상차손 인식 시 차감 계정의 명칭", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "유형자산에 대해 '재평가모형'을 적용하는 건물에 대해 최초로 자산 손상 징후에 따라 장부액을 깎아 손상차손을 기장할 때, 기존에 건물과 관련해 자본에 적립되어 남아 있던 재평가잉여금 잔액이 전혀 없다면, 이 최초 손상차손은 어떤 손익으로 분류되는가?",
        "options": [
            "① 전액 당기순이익에 반영되는 영업외비용(당기손손실)으로 인식한다.",
            "② 전액 기타포괄손익(OCI)으로 분류하여 자본을 차감한다.",
            "③ 전액 이익잉여금 전기이월 잔액을 차감하는 수정 거래로 처리한다.",
            "④ 손상이 발생하더라도 상계할 잉여금이 없으면 기장을 생략한다.",
            "⑤ 전액 단기사채 부채 계정으로 이월한다."
        ],
        "answer": "1",
        "explanation": "① K-IFRS 상 재평가모형을 적용하는 자산에 손상이 발생한 경우, 우선 기존에 해당 자산과 관련하여 자본에 적립된 '재평가잉여금' 잔액 범위 내에서 기타포괄손익(OCI)으로 먼저 잉여금을 차감 상쇄하고, 이를 초과하거나 기존 잔액이 없는 최초 손상 상황이라면 전액 당기순손익(당기비용, 즉 재평가손실 또는 손상차손)으로 당기 성과에 직접 반영합니다.\n\n[오답 해설]\n② 기존 잉여금 잔액이 없으므로 OCI로 차감할 수 없어 전액 당기 비용입니다.\n③ 전기이월 이익잉여금을 바로 깎아내지 않습니다.\n④ 기장을 생략하는 것은 이중 장부 왜곡입니다.\n⑤ 부채 이월설은 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "기존에 차감할 잉여금 잔액이 존재하지 않는 최초 손상 상황이므로 하락액 전체가 즉시 당기손익(당기비용, 영업외비용 성격)에 직접 반영됨이 맞습니다.", "articles": ["K-IFRS 제1036호 문단 60, K-IFRS 제1016호 문단 40"], "principle": "재평가 자산 최초 손상 시 손익 귀속", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "자본 잉여금 상계액이 없으므로 OCI 직접 계상은 불가능합니다.", "articles": ["K-IFRS 제1016호 문단 40"], "principle": "재평가 자산 최초 손상 시 손익 귀속", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "소급 조정 항목이 아니므로 틀렸습니다.", "articles": [], "principle": "재평가 자산 최초 손상 시 손익 귀속", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "자산액이 깎였으므로 의무 기장해야 하며 기장 생략은 불가합니다.", "articles": [], "principle": "재평가 자산 최초 손상 시 손익 귀속", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "부채 계정 대체설은 회계 이론에 저촉됩니다.", "articles": [], "principle": "재평가 자산 최초 손상 시 손익 귀속", "case": {"holding": "건물", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "K-IFRS 제1036호에 명시된, 기업이 취득한 '영업권(Goodwill)'에 대하여 과거 연도에 인식하였던 손상차손의 차후 결산 시 환입(Reversal) 가능 여부에 대한 원칙은?",
        "options": [
            "① 외부 시가가 급등하는 경우에는 다른 자산보다 우선하여 환입을 허용한다.",
            "② 과거에 인식한 영업권의 손상차손은 후속 기간에 회수가능액이 회복되더라도 절대 환입할 수 없다.",
            "③ 매년 상각비 범위 내에서 10%씩 소액 균등 환입은 허용한다.",
            "④ 세무서 승인을 얻을 때에만 OCI로 우회 환입한다.",
            "⑤ 회사의 미처분이익잉여금이 플러스일 때에만 일시 환입한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 124에 명시된 바와 같이, 영업권에 대해 인식한 손상차손은 후속 기간에 환입할 수 없습니다. 이는 영업권의 환입을 허용할 경우 내부적으로 창출된 영업권을 자산으로 인식하는 결과를 낳아 신뢰성을 크게 훼손하기 때문입니다.\n\n[오답 해설]\n①, ③, ④, ⑤ 어떠한 예외적 조건 하에서도 영업권 손상차손의 환입은 절대적으로 금지되어 있으므로 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "시가 변동 여부와 무관하게 영업권 환입은 원천 금지되므로 오답입니다.", "articles": ["K-IFRS 제1036호 문단 124"], "principle": "영업권 손상차손의 환입 불허 원칙", "case": {"holding": "영업권", "no": None}},
            {"correct": True, "why": "과거 인식된 영업권 손상차손은 이후 사정이 복구되더라도 결코 환입할 수 없음을 규정에 맞게 지목했습니다.", "articles": ["K-IFRS 제1036호 문단 124"], "principle": "영업권 손상차손의 환입 불허 원칙", "case": {"holding": "영업권", "no": None}},
            {"correct": False, "why": "일부 균등 환입 허용설도 규정 위반입니다.", "articles": [], "principle": "영업권 손상차손의 환입 불허 원칙", "case": {"holding": "영업권", "no": None}},
            {"correct": False, "why": "과세 당국 승인 유무와 관련 없이 회계기준상 전면 불허됩니다.", "articles": [], "principle": "영업권 손상차손의 환입 불허 원칙", "case": {"holding": "영업권", "no": None}},
            {"correct": False, "why": "미처분이익잉여금 상태와 연계되지 않는 엄격한 조항입니다.", "articles": [], "principle": "영업권 손상차손의 환입 불허 원칙", "case": {"holding": "영업권", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "유형자산에 대해 손상차손을 장부에 인식한 이후, 차기(다음 연도) 결산 시 인식할 감가상각비의 산정 기준으로 올바른 것은?",
        "options": [
            "① 손상차손 인식 전의 기존 감가상각 계획표와 상각비를 그대로 고수하여 적용한다.",
            "② 손상차손 반영 후의 조정된 장부금액을 기준으로, 잔여내용연수와 새로운 잔존가치를 전진적으로(Prospective) 적용하여 상각비를 재배분한다.",
            "③ 손상으로 자산 가액이 깎였으므로 상각을 즉시 영구 중단한다.",
            "④ 과거에 덜 잡았던 상각비를 한꺼번에 소급하여 재작성한다.",
            "⑤ 손상차손 금액의 20%를 매년 감가상각비에 강제 가산한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 63에 따르면, 자산의 손상차손을 인식한 후에는 새로운 장부금액에서 잔존가치를 차감한 조정된 금액을 자산의 남은 잔여내용연수 동안 전진적으로 감가상각비를 배분하여 재산출합니다.\n\n[오답 해설]\n① 장부가가 하락했으므로 상각비를 고수하면 만기 시 장부가가 0 이하가 되므로 모순입니다.\n③ 자산이 계속 사용되므로 감가상각을 멈출 수 없습니다.\n④ 소급 적용하여 고치지 않습니다.\n⑤ 손상차손의 특정 비율을 가산하는 강제 법률 조항은 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산액이 쪼그라들었으므로 감가상각 스케줄을 재조정해야 해 동일 고수설은 오답입니다.", "articles": ["K-IFRS 제1036호 문단 63"], "principle": "손상 후 차기 감가상각비 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "손상 후 하락 장부가를 기점으로 남은 수명과 개정된 가치를 적용해 전진법 상각비를 다시 매기는 회계추정변경의 처리법에 완벽히 부합합니다.", "articles": ["K-IFRS 제1036호 문단 63"], "principle": "손상 후 차기 감가상각비 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지속 가동 자산이므로 상각을 영구 멈추면 안 됩니다.", "articles": [], "principle": "손상 후 차기 감가상각비 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추정 변경의 전진법 취지에 위배되므로 소급법 적용은 불가능합니다.", "articles": [], "principle": "손상 후 차기 감가상각비 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 가산 수치 공식은 회계 규칙과 무관합니다.", "articles": [], "principle": "손상 후 차기 감가상각비 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },

    # =========================================================================
    # L2: 이해 및 기준 조문 (15문항, 1111~1125번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s04-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "자산손상의 외부 징후 정보원 중 '시장 이자율의 변동'이 기업이 보유한 기계장치의 자산손상 판정에 실질적인 영향(할인율 및 가치 하락)을 미치게 되는 구체적인 이론 경로에 대한 설명으로 옳은 것은?",
        "options": [
            "① 시장 이자율이 하락하면 자산의 청산가치가 직접 상승하기 때문이다.",
            "② 시장 이자율이 상승하면 자산의 사용가치를 계산할 때 미래현금흐름에 적용하는 할인율이 동반 상승하여 사용가치가 크게 하락하므로, 이로 인해 자산의 회수가능액이 감소하기 때문이다.",
            "③ 이자율 변동은 세법상 강제 취득가 상각을 유발하기 때문이다.",
            "④ 이자율이 변동하면 기계장치의 물리적 마모 속도가 빨라지기 때문이다.",
            "⑤ 이자율 상승은 기업 시가총액을 직접 불려 순자산 배분율을 늘리기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 사용가치는 미래현금흐름의 현재가치(PV)입니다. 시장 이자율이 상승하면 현가 계산에 사용되는 세전 할인율도 상승하게 되며, 분모인 할인율이 커지면 사용가치 결과값은 대폭 감소합니다. 이로 인해 회수가능액($\text{Max}(\text{순공정가}, \text{사용가})$)이 떨어져 손상차손을 인식할 리스크가 커집니다.\n\n[오답 해설]\n① 이자율 하락은 오히려 현가(사용가치)를 높이므로 손상 가능성을 낮춥니다.\n③ 세제 감액 정책이나 ④ 물리적 마모와 이자율은 무관합니다.\n⑤ 시가총액이 불어나는 것과 개별 기계의 이자율 연계 경로와는 성격이 다릅니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "이자율 하락은 사용가치를 증가시키는 방향이므로 오답입니다.", "articles": [], "principle": "시장 이자율 상승이 자산손상에 미치는 영향", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "시장 이자율 상승이 사용가치 할인율(세전)을 증가시켜 분모를 키우고 사용가치(현가)를 갉아먹음으로써 회수가능액 감소로 연결되는 과정을 완벽히 이해했습니다.", "articles": ["K-IFRS 제1036호 문단 12"], "principle": "시장 이자율 상승이 자산손상에 미치는 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세제상 규정과는 인과관계가 없습니다.", "articles": [], "principle": "시장 이자율 상승이 자산손상에 미치는 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자율 상승이 물리적인 기계의 마모를 직접 야기하진 않습니다.", "articles": [], "principle": "시장 이자율 상승이 자산손상에 미치는 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가총액 증가 주장은 왜곡입니다.", "articles": [], "principle": "시장 이자율 상승이 자산손상에 미치는 영향", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "유형자산 사용가치(Value in use) 산출 시 대입할 '미래 현금유출입 흐름의 추정'과 관련하여, K-IFRS 기준서가 포함시키는 것을 엄격히 차단(배제)하도록 선언하는 예산 추정 요건으로 옳은 것은?",
        "options": [
            "① 현재의 상태에서 자산을 계속 사용함에 따라 유입될 예상 현금 영업수익",
            "② 자산을 계속 사용가능하게 유지하는 데 필연적으로 발생하는 일상 수선 유지 비용",
            "③ 아직 확약되지 않은 미래의 구조조정이나 자산의 성능 향상 및 개조를 위한 미래 지출로부터 유입될 현금흐름",
            "④ 자산 사용 시 공장에서 배출되는 폐수 처리와 관련된 법적 의무 이행 현금 유출액",
            "⑤ 자산 처분 시 유입될 순현금 잔액"
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1036호 문단 44에 따르면, 사용가치 계산에 반영할 미래현금흐름은 '현재 상태의 자산'을 기준으로 추정해야 합니다. 따라서 아직 확약되지 않은 구조조정이나 자산의 성능 개선, 성능 향상을 통하여 도출될 것으로 예상되는 미래의 현금유출입은 현금흐름 추정 시 배제하여야 합니다.\n\n[오답 해설]\n① 계속 사용에 따른 영업수익이나 ② 현상유지비, ④ 필수 유출 의무액, ⑤ 처분 유입액 등은 모두 사용가치 공식에 정상 포함되는 실질적 현금흐름 구성항목들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "사용에 따른 유입액은 당연히 포함 항목입니다.", "articles": ["K-IFRS 제1036호 문단 39"], "principle": "사용가치 현금흐름 추정 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유지를 위한 필수 비용은 차감 반영되어야 하므로 배제하지 않습니다.", "articles": ["K-IFRS 제1036호 문단 39"], "principle": "사용가치 현금흐름 추정 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "아직 의무화되지 않은 미래 구조조정이나 자산 성능 가치 인상을 위한 미래의 자본지출 효과는 자산을 과대 포장할 위험이 있어 차단 배제함을 바르게 짚어냈습니다.", "articles": ["K-IFRS 제1036호 문단 44"], "principle": "사용가치 현금흐름 추정 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법적 유출 의무비는 비용에 포함하여 차감해야 하므로 배제 대상이 아닙니다.", "articles": [], "principle": "사용가치 현금흐름 추정 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분 시 현금 유입은 정상 가산 항목입니다.", "articles": [], "principle": "사용가치 현금흐름 추정 요건", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "유형자산의 사용가치를 계산할 때 미래현금흐름에 대입할 '할인율(Discount rate)'의 세무적 및 재무적 성격으로 K-IFRS가 규정하는 올바른 조건은?",
        "options": [
            "① 주주들이 요구하는 배당률에 세후 효과를 가감한 이율",
            "② 자산의 특유한 위험과 화폐의 시간가치에 대한 현 시장 평가를 반영한 세전 할인율",
            "③ 시중 은행의 대출 금리 평균의 세후 명목 이율",
            "④ 정부 공인 기준 이자율의 세후 복합이율",
            "⑤ 회사의 자기자본비용(Ke) 세후 지표"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 55에 명시된 바와 같이, 사용가치 계산에 사용하는 할인율은 화폐의 시간가치에 대한 현 시장 평가와 자산의 특유한 위험에 대한 현 시장 평가를 반영한 세전 할인율(Pre-tax rate)이어야 합니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 세후(Post-tax) 이율을 적용하거나 자산 특유의 위험이 반영되지 않은 단순 시중 금리 등을 나열한 것으로 모두 기준서와 부합하지 않는 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "세후 지표 및 배당률은 사용가치 세전 할인율 요건에 부적합합니다.", "articles": ["K-IFRS 제1036호 문단 55"], "principle": "사용가치 할인율의 성격", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산의 위험 요소와 현 시간가치를 결합한 세전(Pre-tax) 할인율이어야 함을 정확하게 제시했습니다.", "articles": ["K-IFRS 제1036호 문단 55"], "principle": "사용가치 할인율의 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세후 명목 이율이 아니므로 오답입니다.", "articles": [], "principle": "사용가치 할인율의 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기준금리 단독 대입이나 세후 이율 적용은 틀린 진술입니다.", "articles": [], "principle": "사용가치 할인율의 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자기자본비용 세후 지표는 기준서 조항에 맞지 않는 수치입니다.", "articles": [], "principle": "사용가치 할인율의 성격", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "K-IFRS 제1036호에서 정의하는 '현금창출단위(Cash-generating unit, CGU)'의 본질적인 성격으로 가장 알맞은 표현은?",
        "options": [
            "① 기업 전체의 영업이익을 10% 단위로 나누어 배분하는 임의의 행정 조직",
            "② 다른 자산이나 자산집단으로부터의 현금유입과는 거의 독립적인 현금유입을 창출하는 식별 가능한 가장 작은 자산집단",
            "③ 외부 세무서에 매년 신고하는 지점별 과세 보고 단위",
            "④ 기계장치의 본체와 모터 부품을 분리 기재한 개별 분개 과목",
            "⑤ 회사의 연구개발(R&D) 부서만을 지칭하는 자본 계정"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 6에 명시된 바와 같이, 현금창출단위(CGU)는 다른 자산이나 자산집단으로부터의 현금유입과는 거의 독립적인 현금유입을 창출하는 식별 가능한 가장 작은 자산집단으로 규정되어 있습니다. 개별 자산의 회수가능액을 독립적으로 구하기 어려울 때 이 CGU 단위로 묶어 손상검사를 수행합니다.\n\n[오답 해설]\n① 임의의 이익 배분 조직이 아닙니다.\n③ 세법상 지점 보고 단위나 ④, ⑤의 연구개발 부서 등과는 회계 이론상 완전히 분리된 독립된 자산 집단 개념입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "임의의 영업이익 배분 조직이 아니므로 틀렸습니다.", "articles": [], "principle": "현금창출단위의 개념", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "다른 자산과 무관하게 독립적인 캐시플로우를 발생시키는 식별 가능한 최소한의 자산 묶음군(집단)이라는 CGU 정의에 충실합니다.", "articles": ["K-IFRS 제1036호 문단 6"], "principle": "현금창출단위의 개념", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 지점 보고 단위설은 회계원리 외적 서술입니다.", "articles": [], "principle": "현금창출단위의 개념", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부품 개별 구분 분개와는 스케일이 다릅니다.", "articles": [], "principle": "현금창출단위의 개념", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 계정이나 부서명이 아니므로 오답입니다.", "articles": [], "principle": "현금창출단위의 개념", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "현금창출단위(CGU)에 대한 손상차손을 기장할 때, CGU 내에 존재하는 개별 자산(영업권 포함)들에 손상액을 깎아 배분하는 올바른 기장 순서는?",
        "options": [
            "① 다른 기계나 건물에 손상을 먼저 비례 배분하여 0으로 깎은 후, 남은 금액을 영업권에 배분한다.",
            "② 우선 현금창출단위에 배분된 영업권(Goodwill)의 장부금액을 우선적으로 전액 감액하고, 그 다음 남은 손상차손을 단위를 구성하는 다른 자산들의 장부금액 비례로 안분 배분한다.",
            "③ 영업권은 절대 건드리지 않고 다른 자산들의 장부금액 비율로만 영구 상계한다.",
            "④ 영업권과 토지에 절반씩 일괄 배분하고 종료한다.",
            "⑤ 회사의 대표자 지분가치에 우선 차감 기재한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 104에 따르면, 현금창출단위의 손상차손은 다음의 순서로 배분합니다. 첫째, CGU에 배분된 영업권의 장부금액을 우선 감소(0이 한도)시킵니다. 둘째, 그 다음 남은 손상차손은 CGU 내의 다른 개별 자산들의 장부금액 비율에 비례하여 안분 배분합니다.\n\n[오답 해설]\n① 영업권보다 기계나 건물을 먼저 지우지 않으므로 순서가 왜곡되었습니다.\n③ 영업권의 가치가 가장 먼저 지워져야 하므로 잉여 보존설은 거짓입니다.\n④, ⑤ 토지 절반 배분이나 대표자 지분 상계 등은 소설적인 보도입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "일반 개별자산을 먼저 상각하고 영업권을 나중에 깎는 것은 순서가 뒤집힌 오류입니다.", "articles": ["K-IFRS 제1036호 문단 104"], "principle": "CGU 손상차손 배분 순서", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "CGU 손상 발생 시 가장 거품적 성격이 짙은 영업권(Goodwill)의 장부가를 먼저 ₩0으로 전액 차감한 후, 남은 손상차손을 타 개별 자산에 비례 안분한다는 기준서 배분 규정을 바르게 서술했습니다.", "articles": ["K-IFRS 제1036호 문단 104"], "principle": "CGU 손상차손 배분 순서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업권을 우선 감액해야 하므로 보존설은 틀렸습니다.", "articles": [], "principle": "CGU 손상차손 배분 순서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "토지와 영업권 반반 배분은 규정에 없는 임의 비율입니다.", "articles": [], "principle": "CGU 손상차손 배분 순서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 주주 지분에 직접 기입할 수 없습니다.", "articles": [], "principle": "CGU 손상차손 배분 순서", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "현금창출단위(CGU)의 손상차손을 개별 구성 자산들에 안분 배분할 때, 개별 자산의 장부금액을 깎아 내릴 수 없는 물리적/회계적 '감액의 하한선(Floor)'에 대한 규정으로 옳은 것은?",
        "options": [
            "① 무조건 최초 역사적 원가의 10% 이하로는 깎을 수 없다.",
            "② 당해 개별 자산의 순공정가치, 사용가치, 0 중 가장 큰(Max) 금액 이하로는 장부금액을 줄일 수 없다.",
            "③ 당해 자산의 장부금액을 마이너스(-) 1억 원까지 자유롭게 깎을 수 있다.",
            "④ 외부 감정평가액의 50% 선에서 강제 합의 차단된다.",
            "⑤ 회사의 발행 자본금 총량 이하로는 자산을 줄이지 못한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 105에 따르면, 현금창출단위의 손상차손을 배분할 때 개별 자산의 장부금액은 '순공정가치', '사용가치', '0' 중 가장 큰 금액(Max) 이하로 감액할 수 없습니다. 즉 개별적으로 측정된 가치 하한선이 보장된다면, 그 이하로 깎인 배분 손상액은 다른 하한선에 안 걸린 자산들에 재배분하게 됩니다.\n\n[오답 해설]\n① 10% 원가 하한 규정은 없습니다.\n③ 마이너스(-) 자산 장부 기재는 부적정합니다.\n④ 감평액 50%나 ⑤ 발행자본금 연동 등은 전혀 사실이 아닌 임의의 보기들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "취득원가 10% 하한 룰은 기준서에 없습니다.", "articles": [], "principle": "개별 자산의 손상 감액 하한 규정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "개별 자산의 회수가능액 제약 조건인 순공정가, 사용가치, 0 중 맥스(Max) 가액 이하로는 장부금액을 추가 감액하여 깎을 수 없다는 안전 장치 규정을 정확히 지목했습니다.", "articles": ["K-IFRS 제1036호 문단 105"], "principle": "개별 자산의 손상 감액 하한 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산은 차변 요소이므로 마이너스 계상은 대단히 비정상적입니다.", "articles": [], "principle": "개별 자산의 손상 감액 하한 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감평가 50% 룰은 오답입니다.", "articles": [], "principle": "개별 자산의 손상 감액 하한 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 총액과는 연계되지 않는 자산별 개별 지표입니다.", "articles": [], "principle": "개별 자산의 손상 감액 하한 규정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "K-IFRS 상 현금창출단위(CGU)에 포함된 영업권(Goodwill)에 대해 과거 인식한 손상차손을 후속 기간의 공정가치 회복 시에도 절대로 환입하지 못하도록 전면 통제하는 회계이론적 지향점은?",
        "options": [
            "① 영업권은 무형자산이므로 감가상각으로만 소멸해야 타당하기 때문이다.",
            "② 영업권 손상차손의 환입을 적법하게 허용해 버리면, 장부상에 자의적으로 가치를 부풀려 '내부적으로 창출된 영업권(Self-generated goodwill)'을 자산으로 새로 기재하여 적립하는 왜곡을 낳기 때문이다.",
            "③ 영업권은 물리적 형체가 없는 단순 전표상의 가짜 자산이기 때문이다.",
            "④ 세법상 무상 증여로 의심받을 여지가 있기 때문이다.",
            "⑤ 이사회 승인 없이는 자본 대체를 금지하기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 영업권은 사업결합(M&A) 시 대가 지불 과정에서 입증된 '취득한 영업권'만 자산화가 허용됩니다. 손상된 영업권이 나중에 회사의 실적 개선으로 다시 반등했을 때 이를 장부에 다시 얹어 환입해버리면, M&A와 관계없이 회사가 내부적으로 창출해 가치를 올린 영업권(K-IFRS 상 자산인식 절대 금지 대상)을 자산으로 변칙 인식하는 것과 다름없어지므로 이를 철저히 금지하는 것입니다.\n\n[오답 해설]\n① 영업권은 비한정 내용연수이므로 감가상각 자체를 수행하지 않습니다.\n③ 무형자산은 적법한 권리 자산이며 가짜 자산이 아닙니다.\n④, ⑤는 세법 및 이사회 절차와 무관한 순수 회계기준 상의 이론적 정당성 확보 차원의 제한 조치입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "영업권은 상각 대상 무형자산이 아니므로(비한정 수명) 전제가 틀렸습니다.", "articles": [], "principle": "영업권 손상환입 금지의 이론적 당위성", "case": {"holding": "영업권", "no": None}},
            {"correct": True, "why": "과거 손상된 영업권의 환입 허용 시 자산인식이 엄격히 배제된 내부창출 영업권을 장부에 새로 계상하는 것과 같은 결과를 초래하여 신뢰성을 훼손함을 명밀히 설명했습니다.", "articles": ["K-IFRS 제1036호 문단 124"], "principle": "영업권 손상환입 금지의 이론적 당위성", "case": {"holding": "영업권", "no": None}},
            {"correct": False, "why": "법적 가치를 지닌 식별 가능한 자산이므로 가짜 자산설은 오답입니다.", "articles": [], "principle": "영업권 손상환입 금지의 이론적 당위성", "case": {"holding": "영업권", "no": None}},
            {"correct": False, "why": "세제 증여 쟁점과는 인과가 없습니다.", "articles": [], "principle": "영업권 손상환입 금지의 이론적 당위성", "case": {"holding": "영업권", "no": None}},
            {"correct": False, "why": "자본 대체의 이사회 권한과는 무관한 회계 조항입니다.", "articles": [], "principle": "영업권 손상환입 금지의 이론적 당위성", "case": {"holding": "영업권", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "유형자산의 회수가능액 반등에 따라 과거 인식하였던 손상차손을 장부에 다시 복구하는 '손상차손환입이익'의 당기 포괄손익계산서 상 분류로 타당한 것은?",
        "options": [
            "① 기타포괄이익(OCI)으로 적립하여 자본을 바로 늘린다.",
            "② 판매비와관리비의 직접 차감액으로 넣는다.",
            "③ 당기순손익에 포함되는 영업외수익(또는 기타수익)으로 당기순이익에 직접 반영한다.",
            "④ 이익잉여금의 전기이월 수정이익으로 계상한다.",
            "⑤ 매출액 가산 항목으로 합산 보고한다."
        ],
        "answer": "3",
        "explanation": "③ 원가모형 하에서 유형자산 손상차손 환입은 당기순손익(당기이익, 즉 '유형자산손상차손환입' 등 기타영업외수익 계열)으로 분류되어 당기순이익을 올리는 요소가 됩니다.\n\n[오답 해설]\n① 원가모형의 환입은 자본(OCI)이 아닌 당기손익(P&L) 영역입니다.\n② 판관비 마이너스로 잡지 않고 별도의 기타영업외수익으로 처리합니다.\n④ 소급 이월이익 수정은 오류가 아니므로 불가합니다.\n⑤ 매출로 잡을 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "원가모형 적용 시의 손상환입은 당기손익이며 OCI 적치가 아니므로 오답입니다.", "articles": [], "principle": "손상차손환입액의 손익보고 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "판관비 비용 차감은 계정 성격상 맞지 않습니다.", "articles": [], "principle": "손상차손환입액의 손익보고 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "포괄손익계산서 상의 당기손익(영업외수익/기타수익 과목)에 직접 얹어 당기 성과를 개선시킴이 규정에 부합합니다.", "articles": ["K-IFRS 제1036호 문단 119"], "principle": "손상차손환입액의 손익보고 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 직접 소급 수정이 불가능합니다.", "articles": [], "principle": "손상차손환입액의 손익보고 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출과 자산 환입은 엄격히 분리되는 다른 계정입니다.", "articles": [], "principle": "손상차손환입액의 손익보고 분류", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "K-IFRS 자산손상 기준서가 규정하는, 손상차손 환입액 인식 시 산출될 자산의 '새 장부금액'이 도달할 수 없는 상한선(한도액)의 성격으로 옳은 것은?",
        "options": [
            "① 자산의 최초 취득 당시의 취득원가 무상액",
            "② 과거에 손상차손을 인식하지 않았을 경우에 도달했을 가상의 감가상각 반영 후 장부금액(원가모형 한도)",
            "③ 직전 연말에 감평사가 보고해 둔 재평가 공정가치",
            "④ 기말 손상환입 징후 검증 당일의 경쟁사 유사 자산 장부가",
            "⑤ 자산의 최초 취득원가에 그동안의 물가상승 보정액을 더한 액수"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 117에 따르면, 손상차손 환입으로 증가하는 자산의 장부금액은 과거에 손상차손을 인식하기 전 장부금액의 감가상각 반영 후 장부금액(즉, 손상이 없었을 경우 도달했을 가상의 원가모형 장부금액)을 초과할 수 없습니다. 이는 손상 환입을 이용해 자산의 장부금액을 역사적 상각 스케줄 이상으로 과대포장하는 회계 왜곡을 막기 위함입니다.\n\n[오답 해설]\n① 상각되지 않은 명목 원가로 잡으면 감가상각을 무력화하므로 오답입니다.\n③, ④, ⑤는 한도 제한 요건의 공식 기준과 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수명 소모를 무시한 역사적 원가 명목액은 환입 한도가 될 수 없습니다.", "articles": [], "principle": "손상차손 환입 한도의 성격", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "손상이 발생하지 않았을 경우 기계장치가 도달했을 가상의 정규 상각 후 장부가액(원가모형 한도)을 상한으로 삼는 규정에 정밀하게 일치합니다.", "articles": ["K-IFRS 제1036호 문단 117"], "principle": "손상차손 환입 한도의 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과거 임의 공정가치 등은 한도의 직접 지표가 아닙니다.", "articles": [], "principle": "손상차손 환입 한도의 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경쟁사 지표 인용은 회계 원리에 저촉됩니다.", "articles": [], "principle": "손상차손 환입 한도의 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인플레 보정 물가 회계는 허용되지 않습니다.", "articles": [], "principle": "손상차손 환입 한도의 성격", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "유형자산에 대해 '재평가모형'을 적용하는 건물에 대해 과거에 잡았던 손상차손을 후속 기간 공정가치 급등에 따라 환입할 때, 가상의 감가상각 반영 후 장부금액(원가모형 한도)을 초과하는 상승액의 올바른 회계적 계정 처리 분류는?",
        "options": [
            "① 초과액도 동일하게 당기순이익(손상차손환입)으로 잡는다.",
            "② 초과액은 기타포괄손익(OCI)으로 분류하고 자본 항목인 '재평가잉여금'에 누적한다.",
            "③ 초과액은 무조건 단기 부채 선수금으로 기재한다.",
            "④ 초과액은 전액 연구개발비용 차감액으로 돌린다.",
            "⑤ 초과액은 주주 배당 재원으로 직접 유출 전출한다."
        ],
        "answer": "2",
        "explanation": "② 재평가모형 자산의 경우, 손상차손 환입 시 가상의 감가상각 후 장부금액 한도까지는 '손상차손환입(당기이익)'으로 잡고, 그 한도액을 초과하여 공정가치까지 추가로 상승한 부분은 재평가모형 본연의 재평가증가액 규정에 따라 기타포괄손익(재평가잉여금)으로 계상합니다.\n\n[오답 해설]\n① 한도를 넘어선 금액을 당기이익으로 넣으면 원가법의 대전제를 어기므로 오답입니다.\n③, ④, ⑤는 자본잉여 항목(OCI)으로 적립되어야 할 평가상승분을 왜곡 기장한 명백한 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "한도 초과분까지 당기이익(환입이익)으로 털 수 없으므로 오답입니다.", "articles": ["K-IFRS 제1036호 문단 117, 119"], "principle": "재평가 자산의 한도 초과 환입분 처리", "case": {"holding": "건물", "no": None}},
            {"correct": True, "why": "가상의 원가 장부가 한도까지는 당기이익으로 환입하되, 초과한 순수 가치 상승액은 OCI로 인식하여 자본의 재평가잉여금에 꽂아 넣는 규정에 정당하게 부합합니다.", "articles": ["K-IFRS 제1036호 문단 117, 119"], "principle": "재평가 자산의 한도 초과 환입분 처리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "부채 계상설은 대차 평균 왜곡 오류입니다.", "articles": [], "principle": "재평가 자산의 한도 초과 환입분 처리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "연구개발비 차감과는 아무런 관련이 없습니다.", "articles": [], "principle": "재평가 자산의 한도 초과 환입분 처리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "자본 내 미실현 이익이므로 현금배당으로 바로 나갈 수 없습니다.", "articles": [], "principle": "재평가 자산의 한도 초과 환입분 처리", "case": {"holding": "건물", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "K-IFRS 상 유형자산의 '감가상각(Depreciation)'과 '손상차손(Impairment loss)'의 회계이론 상의 가장 본질적인 차이를 서술한 것으로 옳은 것은?",
        "options": [
            "① 감가상각은 자산의 수명 동안 원가를 체계적이고 합리적으로 배분하는 내부적 자본배식 절차이고, 손상차손은 외부 환경 변화 등으로 가치가 급격히 소실된 예기치 못한 하락 사건을 반영하는 거래이다.",
            "② 감가상각은 현금 지출 거래이고 손상차손은 비현금 거래이다.",
            "③ 감가상각은 부채를 늘리는 거래이고 손상차손은 자산을 늘리는 거래이다.",
            "④ 감가상각은 강제 사항이나 손상차손은 기업의 선택에 따르는 임의 거래이다.",
            "⑤ 두 제도는 계산 공식이 동일하여 이론상 구분할 수 없다."
        ],
        "answer": "1",
        "explanation": "① 감가상각은 자산의 미래 사용에 따라 원가를 체계적으로 수익과 비용에 대응 배분하는 기간 안분 테크닉인 반면, 손상차손은 자산의 회수가능액이 중요하게 급감하여 예상치 못한 가치 파손 사건이 일어난 현실을 장부에 기록하는 사건적 성격을 가집니다.\n\n[오답 해설]\n② 두 제도 모두 현금의 실제 지출이 따르지 않는 비현금 회계평가 거래입니다.\n③ 둘 다 자산의 감소를 의미합니다.\n④ 둘 다 요건 충족 시 의무 기장해야 하는 강제 사항입니다.\n⑤ 이론적 배경과 계산 방식이 완전히 다른 별개의 규정입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "감가상각의 본질인 원가 배분과 손상차손의 본질인 예상치 못한 가치 급감 반영이라는 이론적 대칭을 정확히 지적했습니다.", "articles": ["K-IFRS 제1016호 문단 50, K-IFRS 제1036호 문단 59"], "principle": "감가상각과 손상차손의 본질적 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "둘 다 현금이 나가지 않는 비현금 항목이므로 오류입니다.", "articles": [], "principle": "감가상각과 손상차손의 본질적 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "둘 다 자산의 직접/간접 차감 차변 비용이므로 오답입니다.", "articles": [], "principle": "감가상각과 손상차손의 본질적 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손상도 징후 포착 및 요건 충족 시 의무적 강제 기장이 원칙입니다.", "articles": ["K-IFRS 제1036호 문단 9"], "principle": "감가상각과 손상차손의 본질적 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "산출 방식과 성격이 완전히 달라 구분 명확설이 타당합니다.", "articles": [], "principle": "감가상각과 손상차손의 본질적 비교", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "원가모형을 적용하던 유형자산에 대해 손상차손을 장부에 기장하고 1년이 경과한 기말 시점에, 다시 손상차손의 환입이 발생했을 때의 감가상각비 적용 방법에 대한 K-IFRS의 지침은?",
        "options": [
            "① 환입이 일어나고 조정된 새 장부금액에 대해 기존 잔여 수명을 적용해 전진법으로 상각비를 조정한다.",
            "② 환입으로 자산액이 불어났으므로 즉시 상각을 완전 중단한다.",
            "③ 과거의 모든 연도 상각비를 취소하고 소급 재산출한다.",
            "④ 환입이 일어난 연도에는 감가상각비를 ₩0으로 처리한다.",
            "⑤ 환입액 크기만큼을 차기 감가상각비에서 다이렉트로 차감한다."
        ],
        "answer": "1",
        "explanation": "① 손상차손 환입이 이루어지면 자산의 장부가가 다시 상향 조정됩니다. 이는 새로운 추정 조건의 생성이므로 회계추정변경 전진법 규정에 부합하게, 기말 환입 후 조정된 기말 장부가를 기초로 잔여내용연수를 적용하여 다음 기간 이후의 감가상각비를 전진적으로 다시 계산해 인식합니다.\n\n[오답 해설]\n② 상각 대상 유형자산은 가동 중이므로 상각 중단은 불가합니다.\n③ 감가상각 스케줄 개정은 오류수정이 아니므로 소급하지 않습니다.\n④ 환입과 상각비는 독립된 별개의 거래이므로 ₩0 처리 주장은 틀렸습니다.\n⑤ 상각비에서 다이렉트 상계 차감하지 않고 상각비용 계정으로 독립 기입해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "환입 조정 반영 후 개정된 장부가를 기산점으로 잔여 수명을 대입하여 차기 상각비를 전진적으로 개편 적용함을 올바르게 제시했습니다.", "articles": ["K-IFRS 제1036호 문단 121"], "principle": "손상차손 환입 후 차기 감가상각 방법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 노후화는 계속되므로 상각을 멈추는 것은 오답입니다.", "articles": [], "principle": "손상차손 환입 후 차기 감가상각 방법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추정 조정을 소급법으로 소급 재작성하는 것은 기준 위반입니다.", "articles": [], "principle": "손상차손 환입 후 차기 감가상각 방법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당기에도 가동 기간 상각은 필요하므로 ₩0 처리는 모순입니다.", "articles": [], "principle": "손상차손 환입 후 차기 감가상각 방법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각비 계정 직접 상쇄 주장은 오답입니다.", "articles": [], "principle": "손상차손 환입 후 차기 감가상각 방법", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "다음 K-IFRS 상의 자산 중, 손상 징후(Indicator of impairment)의 존재 여부와 관계없이 매년 의무적으로 회수가능액을 추정하여 손상검사를 주기적으로 수행하여야 하는 자산으로 묶인 것은?",
        "options": [
            "① 건물, 기계장치, 토지",
            "② 내용연수가 비한정인 무형자산, 아직 사용할 수 없는 무형자산, 사업결합으로 취득한 영업권",
            "③ 매출채권, 대여금, 미수금",
            "④ 재고자산, 선급비용, 선급금",
            "⑤ 차량운반구, 비품, 가구류"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1036호 문단 10에 따르면, (1) 내용연수가 비한정인 무형자산, (2) 아직 사용할 수 없는 무형자산, (3) 사업결합으로 취득한 영업권에 대해서는 손상을 시사하는 징후가 있는지와 관계없이 매년 회수가능액을 추정하여 손상검사를 의무적으로 수행해야 합니다.\n\n[오답 해설]\n①, ⑤ 건물, 기계, 비품 등 일반 유형자산은 손상 징후가 있을 때에만 손상검사를 수행합니다.\n③ 금융자산이나 ④ 재고자산은 제1036호 손상 검사 대상 자산군이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "일반 유형자산은 징후가 있을 때에만 검사하므로 오답입니다.", "articles": ["K-IFRS 제1036호 문단 9"], "principle": "매년 의무적 손상검사 대상 자산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비한정 수명 무형자산, 사용 불가 무형자산, 사업결합 영업권은 징후 유무를 불문하고 매년 강제 손상검사를 받아야 하는 대상 자산임을 정확히 모았습니다.", "articles": ["K-IFRS 제1036호 문단 10"], "principle": "매년 의무적 손상검사 대상 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수취채권은 금융자산 대손상각 기준(제1109호)의 관할입니다.", "articles": [], "principle": "매년 의무적 손상검사 대상 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고자산은 저가법 평가(제1002호) 대상입니다.", "articles": [], "principle": "매년 의무적 손상검사 대상 자산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일반 상각 대상 유형자산은 매년 의무 검사 대상이 아닙니다.", "articles": [], "principle": "매년 의무적 손상검사 대상 자산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "유형자산에 대해 손상 징후(예: 경쟁사 신제품 출시 등)가 포착되었으나, 당기 결산 시점에 추정한 자산의 회수가능액이 기말 현재 자산의 장부금액보다 더 높게 계산된 경우 K-IFRS 상 올바른 기장 처리는?",
        "options": [
            "① 회수가능액과 장부금액 차액만큼을 강제로 손상차손환입이익으로 인식한다.",
            "② 징후가 있었으므로 무조건 ₩10,000의 상징적 손상차손을 계상한다.",
            "③ 장부금액이 회수가능액 이하이므로 어떠한 손상차손도 인식하지 않으며 기존 장부 상태를 그대로 유지한다.",
            "④ 자산 원가를 공정가치와 같게 임의로 보정하여 늘린다.",
            "⑤ 회사가 이미 적립한 재평가잉여금 잔액을 전액 강제 처분 취소한다."
        ],
        "answer": "3",
        "explanation": "③ 자산 손상은 장부금액이 회수가능액을 초과할 때 그 초과액을 털어 자산을 낮추는 회계처리입니다. 비록 손상 징후가 포착되어 손상검사(회수가능액 추정)를 이행하였더라도, 실제 회수가능가액이 장부상 가액 이상으로 양호함이 확인되었다면 장부에 기록할 손상차손 금액은 ₩0(인식 없음)이 타당합니다.\n\n[오답 해설]\n① 기존에 인식한 손상차손이 없다면 환입이익을 임의로 적립할 수 없습니다.\n② 상징적 임의 손상 기장 주장은 오답입니다.\n④ 원가모형의 자산을 임의로 증액할 수 없습니다.\n⑤ 잉여금 강제 취소 의무가 발생하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "과거 손상 잔액이 없는 상태에서 장부가액을 임의 초과 증액하는 환입이익 계상은 불가합니다.", "articles": [], "principle": "회수가능액이 장부금액 이상일 때의 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상징적 임의 감액은 회계 정보 신뢰성을 해치므로 오답입니다.", "articles": [], "principle": "회수가능액이 장부금액 이상일 때의 처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "장부금액이 회수가능가 이하이므로 손상 리스크가 없어 아무런 평가 분개를 하지 않고 자산을 고수해야 함을 올바르게 설명했습니다.", "articles": ["K-IFRS 제1036호 문단 59"], "principle": "회수가능액이 장부금액 이상일 때의 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가모형 하에서 자산 임의 증액은 금지됩니다.", "articles": [], "principle": "회수가능액이 장부금액 이상일 때의 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잉여금 소멸 의무가 없습니다.", "articles": [], "principle": "회수가능액이 장부금액 이상일 때의 처리", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s04-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "기업이 공장 기계장치에 대해 거액의 '손상차손(Impairment loss)'을 인식한 사건이, 당해 및 후속 회계기간의 주요 재무분석 지표(당기순이익, 자기자본이익률(ROE))에 초래할 수 있는 인위적 왜곡 효과에 대한 분석으로 가장 옳은 것은?",
        "options": [
            "① 당기순이익은 당기에 하락하지만, 차기 이후에는 감가상각 대상 자산액이 크게 줄어 매년 인식할 감가상각비용이 격감하므로 차기 당기순이익이 인위적으로 크게 상승하며, 이로 인해 분모인 자기자본 축소 효과와 맞물려 ROE가 비정상적으로 높게 급증하는 착시 효과를 낳는다.",
            "② 당기 및 차기 모든 연도의 ROE를 동일한 ₩0으로 고정시킨다.",
            "③ 손상 인식은 총자산 회전율을 영구히 하락시킨다.",
            "④ 차기 이후 감가상각비가 대폭 증가하는 모순을 낳는다.",
            "⑤ 손상차손은 자본 총계에 아무런 영향을 주지 못한다."
        ],
        "answer": "1",
        "explanation": "① 손상차손은 당기순이익과 자기자본(이잉)을 당기에 급락시킵니다. 그러나 일단 자산 장부가가 깎이고 나면 다음 연도부터 매년 청구될 감가상각비(비용)가 대폭 줄어듭니다. 비용이 줄면 차기 당기순이익(분자)은 크게 증가하는 반면, 분모인 자기자본(자산 감액으로 축소됨)은 쪼그라든 상태이므로, 차기 이후의 자기자본이익률(ROE = 순이익/자기자본) 지표가 장부상 비정상적으로 치솟는 일종의 '빅배스(Big bath)' 착시 왜곡을 초래하게 됩니다.\n\n[오답 해설]\n② ROE를 ₩0으로 고정시키지 않습니다.\n③ 총자산(분모)이 줄어들므로 총자산회전율은 반대로 장부상 상승(개선)하게 됩니다.\n④ 장부가가 줄었으므로 감가상각비는 감소합니다.\n⑤ 순이익 차감을 통해 이익잉여금(자본)을 직접 깎아내므로 영향이 큽니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "자산 감액이 당기 실적은 악화시키지만, 차기 이후 상각비 축소로 이익을 반등시키고 분모(자본) 축소와 겹쳐 ROE를 급격히 상승시키는 재무비율 착시(Big Bath) 현상을 정확히 파악했습니다.", "articles": [], "principle": "자산손상이 후속 재무비율에 미치는 왜곡 효과 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "ROE 고정설은 회계 원리에 반합니다.", "articles": [], "principle": "자산손상이 후속 재무비율에 미치는 왜곡 효과 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "분모인 자산총액이 깎이므로 자산회전율 지표는 인위적으로 개선되는 방향입니다.", "articles": [], "principle": "자산손상이 후속 재무비율에 미치는 왜곡 효과 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각비는 비례하여 크게 줄어드므로 증가설은 거짓입니다.", "articles": [], "principle": "자산손상이 후속 재무비율에 미치는 왜곡 효과 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순이익 감소로 자본총계를 크게 깎아내리므로 영향 무설은 틀렸습니다.", "articles": [], "principle": "자산손상이 후속 재무비율에 미치는 왜곡 효과 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 04 유형자산",
                "item": "4절 유형자산의 손상"
            }
        }
    }
]

questions.extend(part1_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(part1_questions)} new questions (Part 1). Total questions in questions_db_accounting.json: {len(questions)}")
