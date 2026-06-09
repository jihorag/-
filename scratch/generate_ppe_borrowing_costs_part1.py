# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

if DB_PATH.exists():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)
    print(f"Loaded existing {len(questions)} questions.")
    if len(questions) > 1150:
        print(f"Truncating database from {len(questions)} back to 1150 to remove any extraneous data.")
        questions = questions[:1150]
else:
    questions = []
    print("No existing questions file found. Creating new list.")

part1_questions = [
    # =========================================================================
    # L1: 기초 개념 및 조문 식별 (10문항, 1151~1160번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s05-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1023호 '차입원가' 기준서에 의거하여, 자본화 대상이 될 수 있는 '적격자산(Qualifying asset)'의 정의로 가장 올바른 것은?",
        "options": [
            "① 취득 후 즉시 판매하거나 즉시 사용할 수 있는 모든 금융자산 및 유형자산",
            "② 의도된 용도로 사용하거나 판매가능한 상태에 이르게 하는 데 상당한 기간(보통 1년 이상)을 필요로 하는 자산",
            "③ 구입 의사결정 시점부터 실제 대금 지급 완료 시점까지 3개월 미만이 소요되는 자산",
            "④ 기중에 감가상각이 완료되어 더 이상 감가상각비가 계상되지 않는 유휴 기계장치",
            "⑤ 취득원가가 ₩10,000,000 이하인 단기 소모성 비품 및 공구비품"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 5에 따르면, 적격자산(자격 있는 자산)이란 의도된 용도로 사용하거나 판매가능한 상태에 이르게 하는 데 상당한 기간(상당한 기간은 기업의 상황에 따라 판단하나 보통 1년 이상)을 필요로 하는 자산을 의미합니다.\n\n[오답 해설]\n① 취득 즉시 사용/판매가능한 자산은 준비 기간이 필요 없으므로 적격자산에서 제외됩니다.\n③ 3개월 미만의 단기 자산은 상당한 기간을 필요로 하지 않으므로 제외됩니다.\n④ 이미 상각이 끝난 유휴 자산은 자본화 적격 대상이 아닙니다.\n⑤ 금액적 소액 비품 역시 자본화 대상 적격자산으로 분류되기 어렵습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "취득 즉시 사용가능한 상태의 자산은 적격자산이 될 수 없으므로 오답입니다.", "articles": ["K-IFRS 제1023호 문단 7"], "principle": "적격자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "준비에 상당한 기간(의도된 용도로 쓰거나 팔 수 있는 상태로 만드는 데 보통 1년 이상)을 요구하는 자산이라는 기준서 상의 적격자산 핵심 정의에 부합합니다.", "articles": ["K-IFRS 제1023호 문단 5"], "principle": "적격자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대금 결제 기간 요건은 적격자산의 판단 기준과 무관합니다.", "articles": [], "principle": "적격자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각 완료 자산 및 유휴 자산은 신규 취득/건설 적격자산이 아닙니다.", "articles": [], "principle": "적격자산의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특정 금액 이하나 소모성 자산은 자본화 적격 요건을 갖추지 못합니다.", "articles": [], "principle": "적격자산의 정의", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "다음 중 K-IFRS 제1023호에 규정된 '차입원가(Borrowing costs)'의 범위에 포함될 수 없는 항목은?",
        "options": [
            "① 유효이자율법을 적용하여 계산한 이자비용",
            "② 금융리스부채에 대한 금융원가",
            "③ 외화차입금과 관련하여 이자비용의 조정으로 간주되는 외환차이",
            "④ 주주들에게 지급하기 위해 선언한 보통주식 배당금",
            "⑤ 차입금 조달 시 발생한 사채발행비 등 유효이자율 계산에 반영되는 금융원가"
        ],
        "answer": "4",
        "explanation": "④ 주식배당금(보통주 배당금)은 자본 거래의 배분이며, 부채 차입에 따른 이자비용 조정 항목이 아니므로 차입원가의 정의에 포함되지 않습니다.\n\n[오답 해설]\n① 유효이자율법 이자비용, ② 금융리스 금융원가, ③ 이자비용 조정으로 인정되는 외환차이, ⑤ 유효이자율에 반영되는 사채발행비 등 발행 부대원가는 모두 K-IFRS 상 차입원가의 범위에 속합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "유효이자율법 상 이자비용은 차입원가의 대표 항목입니다.", "articles": ["K-IFRS 제1023호 문단 6"], "principle": "차입원가의 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융리스부채 이자 역시 기준서상 명시된 차입원가입니다.", "articles": ["K-IFRS 제1023호 문단 6"], "principle": "차입원가의 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "외화차입금 외환차이 중 이자비용 조정분은 차입원가 범위에 인정됩니다.", "articles": ["K-IFRS 제1023호 문단 6"], "principle": "차입원가의 범위", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "보통주 배당금은 자본거래에 따른 이익의 배분으로서 부채 관련 이자원가가 아니므로 차입원가 범위에서 완벽하게 배제됩니다.", "articles": ["K-IFRS 제1023호 문단 6"], "principle": "차입원가의 범위", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입 관련 유효이자율 계산에 직접 반영되는 거래원가는 차입원가의 일부를 구성합니다.", "articles": ["K-IFRS 제1023호 문단 6"], "principle": "차입원가의 범위", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "기업이 적격자산의 취득에 소요된 차입원가를 자산화(자본화)하기 시작하는 '자본화 개시시점(Commencement date)'의 3가지 충족 조건이 아닌 것은?",
        "options": [
            "① 해당 적격자산에 대한 지출이 발생하고 있을 것",
            "② 차입원가가 실제로 발생하고 있을 것",
            "③ 적격자산을 의도된 용도로 사용하거나 판매가능한 상태에 이르게 하는 데 필요한 활동을 수행 중일 것",
            "④ 당해 차입금에 대해 국세청 세무서장의 자본화 사전 승인 공문을 수령하였을 것",
            "⑤ 위 ①, ②, ③의 세 가지 조건이 모두 동시에 만족되는 첫 날일 것"
        ],
        "answer": "4",
        "explanation": "④ K-IFRS 상 차입원가 자본화 개시를 위해 세무서장이나 정부 기관의 사전 승인을 얻어야 한다는 법적 조항은 존재하지 않습니다. 자산 지출, 차입원가 발생, 건설 활동 진행이라는 세 실질 요건이 모두 충족되는 시점에 자동 개시합니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 K-IFRS 제1023호 문단 22에 규정된 개시일 판단의 핵심 3대 실질 충족 조건 및 결합 규칙입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지출 발생은 개시 요건 중 하나이므로 오답지입니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "자본화 개시시점의 충족 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입원가 발생 역시 개시 요건 중 하나입니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "자본화 개시시점의 충족 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "물리적/관리상 준비 활동의 진행 역시 개시의 필수 조건입니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "자본화 개시시점의 충족 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "세무 세법상의 관청 승인 요건 등은 K-IFRS 상의 회계적 자본화 개시 실질 요건과 하등 무관하므로 부적절한 설명입니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "자본화 개시시점의 충족 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세 조건이 동시 충족되는 날을 개시일로 잡으므로 맞는 설명입니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "자본화 개시시점의 충족 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "건설 중인 적격자산의 적극적인 개발 활동이 장기간 중단되는 기간에 대하여 K-IFRS 제1023호가 선언하는 이자비용 자본화의 '중단(Suspension)' 규정으로 가장 올바른 것은?",
        "options": [
            "① 중단 기간에도 원래의 이자 계산 방식에 따라 중단 없이 계속 자본화한다.",
            "② 적극적인 개발 활동을 중단한 장기 기간 동안에는 차입원가의 자본화를 중단(비용 처리)하여야 한다.",
            "③ 중단 기간에는 정부가 대신 이자를 변제하므로 기장을 생략한다.",
            "④ 중단 기간의 이자는 자본조정 계정으로 계상해 둔다.",
            "⑤ 중단 기간에는 감가상각을 즉시 개시하여 이자를 상쇄한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 24에 따르면, 적격자산의 취득, 건설 또는 제조 관련 적극적인 개발 활동이 중단된 장기 기간 동안에는 차입원가의 자본화를 중단하고 당기 비용으로 보고하도록 규정하고 있습니다.\n\n[오답 해설]\n① 개발이 실제로 장기 중단되면 자본화를 일시 중단해야 하므로 계속 자본화설은 규정 위배입니다.\n③, ④, ⑤ 기장 생략이나 자본조정 이월, 즉시 감가상각 등은 기준서의 이자 비용 중단 처리 지침과 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지속 자본화를 고집하면 자산이 과대계상되므로 규정에 저촉됩니다.", "articles": ["K-IFRS 제1023호 문단 24"], "principle": "자본화 중단 기간의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "건설이나 개발의 적극적 가동이 장기 휴지 상태에 들어가면 해당 기간 중 발생한 이자비용은 자산원가에 보태지 못하고 즉시 비용(이자비용) 처리한다는 기준을 정확히 명시했습니다.", "articles": ["K-IFRS 제1023호 문단 24"], "principle": "자본화 중단 기간의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자는 이행 의무이므로 기장 생략은 불가능합니다.", "articles": [], "principle": "자본화 중단 기간의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본조정 적립은 인정되는 회계 처리가 아닙니다.", "articles": [], "principle": "자본화 중단 기간의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "사용 개시 전 건설중인자산 상태에서는 감가상각을 진행할 수 없습니다.", "articles": [], "principle": "자본화 중단 기간의 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "유형자산 건설 프로젝트가 종료되어 자본화를 완전히 끝내야 하는 '자본화 종료시점(Cessation)'에 관해 K-IFRS가 규정하는 올바른 기준은?",
        "options": [
            "① 적격자산을 의도된 용도로 사용하거나 판매가능한 상태에 이르게 하는 데 필요한 거의 모든 활동이 완료된 시점",
            "② 해당 건설 자산에 대한 감가상각이 50% 실행 완료된 날",
            "③ 관련 차입금 원금 전체를 은행에 중도 상환 완료한 날",
            "④ 건설 회사가 공사 잔금을 추가 청구하기 시작한 월말",
            "⑤ 기업의 당기순이익이 흑자로 돌아선 사업연도 종료일"
        ],
        "answer": "1",
        "explanation": "① K-IFRS 제1023호 문단 25에 의거, 적격자산을 의도된 용도로 사용하거나 판매가능한 상태에 이르게 하는 데 필요한 '거의 모든 활동이 완료된 때'에 차입원가 자본화를 종료합니다.\n\n[오답 해설]\n② 감가상각 진척도나 ③ 차입금 변제 완료 여부, ④ 잔금 청구일, ⑤ 흑자 귀속일 등은 물리적·회계적 준비 활동의 완료 여부와 관련이 없는 자의적 지표들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "자산 준비에 수반되는 실질적이고 필수적인 물리적·행정적 활동이 사실상 마무리된 시점(거의 모든 활동이 완료된 때)을 자본화의 종착지로 삼는 기준서 조항에 정밀하게 일치합니다.", "articles": ["K-IFRS 제1023호 문단 25"], "principle": "자본화 종료시점의 판단 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본화 종료 이후 상각이 개시되므로 상각 완료일 기준설은 시점이 왜곡되었습니다.", "articles": [], "principle": "자본화 종료시점의 판단 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입금 채무 소멸은 자산의 완성 실질과 관련이 없습니다.", "articles": [], "principle": "자본화 종료시점의 판단 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대금 청구일 등 거래 조건은 완성 지표가 아닙니다.", "articles": [], "principle": "자본화 종료시점의 판단 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "흑자 전환 시점 등은 경영 성과상의 수치이므로 오답입니다.", "articles": [], "principle": "자본화 종료시점의 판단 기준", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "K-IFRS 제1023호에 따르면, 적격자산 취득만을 목적으로 직접 차입한 '특정차입금(Specific borrowings)'의 경우 자본화 가능 차입원가를 산정할 때 해당 기간 발생 이자비용에서 차감하여야 하는 핵심 자본 요율 요소는?",
        "options": [
            "① 차입금 관련 주선 금융수수료 누적액",
            "② 특정차입자금의 일시적 투자 및 예치로부터 얻은 모든 투자수익(이자수익 등)",
            "③ 본사 사옥 감가상각비 가산분",
            "④ 경쟁사가 동일 목적 차입 시 얻은 이자 이득분",
            "⑤ 회사가 지급한 법인세 중 특정차입금 비률 세액"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 12에 의하면, 적격자산을 취득하기 위해 직접 차입한 특정차입금의 경우, 자본화할 수 있는 차입원가는 회계기간 동안 그 차입자금에서 실제 발생한 차입원가에서 '그 차입자금의 일시적 운용(예치 등)으로 얻은 투자수익'을 차감한 순금액으로 결정됩니다.\n\n[오답 해설]\n① 금융수수료는 오히려 가산되는 발행 비용 성격입니다.\n③ 본사 상각비나 ④ 경쟁사 정보, ⑤ 세금 비율 배분 등은 일시투자수익 차감 계산 조항과 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수수료는 차감 요소가 아니므로 오답입니다.", "articles": [], "principle": "특정차입금 일시투자수익 차감 원칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자금이 실제로 적격자산 지출로 투입되기 전 일시적으로 은행 등에 예치되어 얻은 투자 수익은 당해 특정자금 유치에 따른 금융비용을 차감 경감시키는 실제 실질을 가지므로 손익 상계하도록 한 규칙에 합치합니다.", "articles": ["K-IFRS 제1023호 문단 12"], "principle": "특정차입금 일시투자수익 차감 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "본사 건물 상각비는 특정 이자 상계와 아무 상관이 없습니다.", "articles": [], "principle": "특정차입금 일시투자수익 차감 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경쟁사 지표 대입은 불가능합니다.", "articles": [], "principle": "특정차입금 일시투자수익 차감 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법인세 공제 배분은 차감 조항이 아닙니다.", "articles": [], "principle": "특정차입금 일시투자수익 차감 원칙", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "K-IFRS 상 일반적인 운영 및 다양한 목적을 위해 공통 조달한 차입금 중 적격자산 건설에 지출된 '일반차입금(General borrowings)'에 대해 자본화 차입원가를 산정할 때 적용되는 일시투자수익(이자수익)의 차감 여부에 대한 설명으로 옳은 것은?",
        "options": [
            "① 일반차입금의 일시투자수익도 특정차입금처럼 전액 의무적으로 차감 차감한다.",
            "② 일반차입금의 경우, 차입금과 특정 자산 지출 간의 직접적인 인과관계를 맺을 수 없으므로 관련 자금의 일시 예치 투자수익을 자본화액에서 차감하지 않는다.",
            "③ 세무서가 이자수익 발생분의 50%만 임의로 차감해 준다.",
            "④ 일반차입금은 투자수익 차감은 하되 자본화 스케줄을 3년 소급 적용한다.",
            "⑤ 차차기 결산기까지 투자수익 차감을 미뤄 보류한다."
        ],
        "answer": "2",
        "explanation": "② 일반차입금은 기업이 일반적인 목적으로 조달한 공동 자금 풀에서 일부를 꺼내어 적격자산에 투입한 것이므로, 특정 차입자금의 물리적 통제나 일시 예치 인과관계를 특정할 수 없습니다. 따라서 일반차입금의 경우 일시 예치 이자수익을 계산 과정에서 차감하지 않는 것이 기준서 상의 원칙입니다.\n\n[오답 해설]\n① 특정차입금에만 일시투자수익 차감 의무가 적용되므로 오답입니다.\n③, ④, ⑤ 임의율 차감이나 소급 적용, 보류 등은 회계 규칙과 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "일반차입금은 이자수익 차감 규정이 직접 적용되지 않으므로 틀린 설명입니다.", "articles": ["K-IFRS 제1023호 문단 14"], "principle": "일반차입금의 이자수익 차감 배제 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "일반차입금은 조달 목적이 자산 건설에만 국한되지 않는 자금 풀이므로, 해당 차입금 관련 발생 투자수익을 개별 적격자산의 자본화가능액에서 쳐내지 않는다는 규정 실질을 정확히 묘사했습니다.", "articles": ["K-IFRS 제1023호 문단 14"], "principle": "일반차입금의 이자수익 차감 배제 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과세당국의 임의 결정율 적용은 틀린 내용입니다.", "articles": [], "principle": "일반차입금의 이자수익 차감 배제 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본화의 소급 규정 등은 존재하지 않으므로 오답입니다.", "articles": [], "principle": "일반차입금의 이자수익 차감 배제 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 보류 기간 적용은 타당하지 않습니다.", "articles": [], "principle": "일반차입금의 이자수익 차감 배제 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "유형자산 외에 '재고자산(Inventories)'의 경우에도 K-IFRS 상 차입원가 자본화가 가능한 적격자산으로 분류될 수 있는 필수적인 요건은 무엇인가?",
        "options": [
            "① 단기간 내에 대량으로 반복 생산되어 즉시 출고되는 재고자산이어야 한다.",
            "② 취득원가가 시가보다 2배 이상 폭등한 재고자산이어야 한다.",
            "③ 의도된 용도로 사용하거나 판매가능한 상태에 이르게 하는 데 상당한 기간(보통 1년 이상)을 필요로 하는 재고자산이어야 한다.",
            "④ 제조 활동 없이 외부에서 완제품 형태로 즉시 구매해 들여온 상품이어야 한다.",
            "⑤ 법인세 공제 혜택을 받는 수입 원자재 재고자산이어야 한다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1023호 문단 5 및 7에 따르면, 단기간 내에 제조되거나 반복적으로 대량 생산되는 재고자산은 적격자산에서 명백히 배제됩니다. 그러나 숙성 기간이 필요한 주류(와인, 위스키)나 오랜 제작 기간이 필요한 특수 선박, 대형 건설형 재고자산처럼 의도된 판매 상태에 이르기까지 상당한 기간(장기)이 소요되는 재고자산은 적격자산에 포함될 수 있습니다.\n\n[오답 해설]\n① 단기 대량 생산 재고는 적격자산에서 제외됩니다.\n② 가격 급등이나 ④ 외부 즉시 구매 완성품, ⑤ 세제 혜택 유무 등은 적격자산 판정 기준에 속하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "단기 대량 반복 생산 재고는 적격자산에서 명시적으로 제외하므로 정반대입니다.", "articles": ["K-IFRS 제1023호 문단 7"], "principle": "재고자산의 적격자산 포함 요건", "case": {"holding": "재고자산", "no": None}},
            {"correct": False, "why": "가격의 변동폭은 자본화 적격 요건과 무관합니다.", "articles": [], "principle": "재고자산의 적격자산 포함 요건", "case": {"holding": "재고자산", "no": None}},
            {"correct": True, "why": "위스키 숙성이나 대형 특수설비 제작 등과 같이 판매가능한 품질·물리적 상태가 되기까지 오랜 기간(보통 1년 이상) 동안 조업 및 가동 기간을 요구하는 재고라면 차입원가 자본화 적격을 충족한다는 사실을 정확히 지목했습니다.", "articles": ["K-IFRS 제1023호 문단 5, 7"], "principle": "재고자산의 적격자산 포함 요건", "case": {"holding": "재고자산", "no": None}},
            {"correct": False, "why": "외부 완제품 즉시 취득 상품은 조업 기간이 없으므로 자본화 대상이 불가능합니다.", "articles": ["K-IFRS 제1023호 문단 7"], "principle": "재고자산의 적격자산 포함 요건", "case": {"holding": "재고자산", "no": None}},
            {"correct": False, "why": "수입 원자재나 세무 혜택 기준 등은 회계 요건이 아닙니다.", "articles": [], "principle": "재고자산의 적격자산 포함 요건", "case": {"holding": "재고자산", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "K-IFRS 제1023호에 규정된 차입원가 자본화 '중단(Suspension)'의 예외 조항 중, 개발 활동이 일시적으로 지체되더라도 예외적으로 차입원가 자본화를 멈추지 않고 '계속 유지'할 수 있는 합당한 사유에 해당하는 것은?",
        "options": [
            "① 경영진의 재정 악화로 인해 공사를 기약 없이 무기한 중단하는 기간",
            "② 해당 자산을 완성하는 과정에서 일시적인 지연이 필수적인 부분인 경우 (예: 교량 건설을 위해 수위 상승이 불가피하여 잠시 공사를 멈춘 기간)",
            "③ 노조와의 임금 협상 실패로 공장 부지 출입이 장기간 완전 봉쇄된 기간",
            "④ 관할 구청의 인허가 취소로 건설 공사 허가가 영구 취소된 기간",
            "⑤ 건설 설계 도면을 분실하여 6개월간 신규 재작성을 위해 대기한 기간"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 24에 명시된 바와 같이, 일시적인 지연이 자산을 의도된 용도로 사용하거나 판매가능한 상태에 이르게 하는 과정에서 '필수적인 부분'인 경우(예: 교량 건설 시 수위가 상승하여 작업을 일시 멈춘 기간이나 특정 조업 과정상 필수 건조 기간)에는 차입원가의 자본화를 중단하지 않고 계속 자본화합니다.\n\n[오답 해설]\n① 자금 부족 무기한 중단, ③ 장기 임금 분쟁 봉쇄, ④ 인허가 영구 취소, ⑤ 도면 분실 등의 사유는 필수적이고 통제 불가능한 자연적/기술적 필수 지연 과정이 아니므로 자본화를 중단하여 비용 처리하여야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재정 파탄으로 인한 단순 휴업은 자본화 중단 대상이므로 오답입니다.", "articles": ["K-IFRS 제1023호 문단 24"], "principle": "자본화 중단의 예외 조건(자본화 계속 요건)", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산을 완성하는 공정상 기후적, 지질적 조건 등에 따라 '필수적으로 수반되는 임시적 작업 정지 기간'에는 자본화를 중단치 않고 정상 반영한다는 규정에 완벽히 부합합니다.", "articles": ["K-IFRS 제1023호 문단 24"], "principle": "자본화 중단의 예외 조건(자본화 계속 요건)", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "파업이나 봉쇄 등 인위적 정지는 자본화를 멈추어야 하는 중단 사유입니다.", "articles": ["K-IFRS 제1023호 문단 24"], "principle": "자본화 중단의 예외 조건(자본화 계속 요건)", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영구 취소는 자산가치 손실 및 중단 사유에 해당합니다.", "articles": [], "principle": "자본화 중단의 예외 조건(자본화 계속 요건)", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "설계 도면 분실 등의 부주의나 관리 실패로 인한 정지는 자본화 중단 대상입니다.", "articles": [], "principle": "자본화 중단의 예외 조건(자본화 계속 요건)", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "K-IFRS 제1023호 '일반차입금(General borrowings)' 자본화 계산 시, 산정된 자본화 가능 차입원가가 당해 회계기간에 실제로 발생한 일반차입금의 실제 차입원가(한도액)를 초과하게 되는 경우 적용하여야 할 기장 한도 조절 규칙은?",
        "options": [
            "① 실제 발생액을 한도로 설정하여 실제 발생한 이자비용 총액까지만 자본화하고 초과액은 자본화할 수 없다.",
            "② 초과된 차액만큼을 기계장치 취득가액에 얹고 대변에 잡이익으로 계상한다.",
            "③ 한도를 무시하고 계산 공식이 도출한 초과 계산액 전체를 여과 없이 자본화한다.",
            "④ 금융감독원 특별 신고를 거치면 전액 환입 처리 후 자본잉여금으로 보낸다.",
            "⑤ 차액 전체를 매년 균등 배분하여 10년간 선급비용으로 이월 기장한다."
        ],
        "answer": "1",
        "explanation": "① 일반차입금의 경우, 자본화이자율을 곱해 산출된 자본화 금액이 당기 중 발생한 일반차입금의 실제 차입원가 총액을 초과할 수 없습니다. 따라서 실제 발생액을 초과하는 산출분은 자본화가 차단되며 실제 발생액만을 한도로 계상합니다.\n\n[오답 해설]\n② 잡이익 계상, ③ 한도 무시 전액 자본화, ④ 특별 신고 자본잉여금 분류, ⑤ 선급비용 10년 이월 등은 모두 K-IFRS 기준서 위반 또는 존재하지 않는 임의의 기장입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "일반차입금의 계산상 자본화가 실제 지출된 금융비용 금액을 넘어설 수 없다는 이자 비용 한도 제약 규정(Min(산출액, 실제 발생액))에 정밀히 일치합니다.", "articles": ["K-IFRS 제1023호 문단 14"], "principle": "일반차입금 자본화의 실제 이자 발생액 한도 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가상의 이익을 얹는 왜곡된 회계처리이므로 오답입니다.", "articles": [], "principle": "일반차입금 자본화의 실제 이자 발생액 한도 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "한도 규정을 묵살하여 자산을 과대 표장하므로 회계기준 위반입니다.", "articles": ["K-IFRS 제1023호 문단 14"], "principle": "일반차입금 자본화의 실제 이자 발생액 한도 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금감원 신고나 자본잉여금 배분 등은 규정에 없는 거짓 내용입니다.", "articles": [], "principle": "일반차입금 자본화의 실제 이자 발생액 한도 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "선급비용 계상 및 10년 상각 등은 임의의 오답지입니다.", "articles": [], "principle": "일반차입금 자본화의 실제 이자 발생액 한도 규정", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },

    # =========================================================================
    # L2: 이해 및 기준 조문 (15문항, 1161~1175번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s05-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "일반차입금에 대한 자본화이자율(Capitalization rate)을 산출할 때, 연도 중에 조건이나 이자율이 서로 다른 여러 개의 일반차입금이 존재하는 경우 K-IFRS가 요구하는 자본화이자율 결정의 이론적 원칙은?",
        "options": [
            "① 가장 이자율이 높은 고리 차입금의 단일 이자율을 적용한다.",
            "② 가장 이자율이 낮은 저리 차입금의 단일 이자율을 적용한다.",
            "③ 회계기간 동안 미상환된 일반차입금 전체의 가중평균이자율을 산출하여 적용한다.",
            "④ 금융기관들이 제시한 기준금리의 산술평균 이자율을 적용한다.",
            "⑤ 회사의 주주 지분 배당률과 차입 이자율의 가중평균치(WACC)를 적용한다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1023호 문단 14에 의거하여, 회계기간 동안 미상환된 일반차입금 전체에 대해 가중평균이자율(차입금 이자율을 차입 잔액 가중치로 가중평균한 비율)을 적용하여 자본화이자율을 산출하는 것이 원칙입니다.\n\n[오답 해설]\n① 최고 이율이나 ② 최저 이율을 자의적으로 쓰면 이자 배분의 형평성이 왜곡됩니다.\n④ 시중 금리의 단순 평균이나 ⑤ 가중평균자본비용(WACC)은 기업의 전체 자본 원가 지표이지 일반차입금의 전용 자본화이자율 지표가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "극단적인 최고 이율 적용은 자본화 금융원가를 과다 계상하게 되므로 오답입니다.", "articles": [], "principle": "일반차입금 자본화이자율 계산 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "최저 이율 단독 적용 역시 부적절합니다.", "articles": [], "principle": "일반차입금 자본화이자율 계산 원칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "연중 조달된 다양한 일반차입금의 실제 잔액 가중치를 반영한 '가중평균이자율'을 이자율로 사용하여 자금 흐름의 실질 평균치를 구하는 기준 요건을 정확히 명시했습니다.", "articles": ["K-IFRS 제1023호 문단 14"], "principle": "일반차입금 자본화이자율 계산 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 평균 금리는 이자액 가중치를 미반영하여 부정확하므로 오답입니다.", "articles": [], "principle": "일반차입금 자본화이자율 계산 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "WACC는 자본비용 평가 지표이며 일반차입금 이자율 산정 대상이 아닙니다.", "articles": [], "principle": "일반차입금 자본화이자율 계산 원칙", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "자본화가능 차입원가 계산의 모태가 되는 적격자산의 '평균누적지출액(Average accumulated expenditures)'을 계산할 때, 건설기간 도중에 '정부보조금(Government grants)' 또는 '공사기성금'을 유입하여 수령한 경우 K-IFRS 상의 처리 요건은?",
        "options": [
            "① 보조금 수령과 상관없이 최초 계약 지출액 총합을 그대로 고수하여 평균액을 매긴다.",
            "② 정부보조금이나 기성금 수령액만큼을 적격자산에 대한 실제 지출액에서 차감(공제)하여 평균지출액을 산정하여야 한다.",
            "③ 보조금 수령액의 2배를 오히려 지출액에 가산하여 평균을 늘린다.",
            "④ 보조금 거래는 별도의 금융부채 계정으로 적립하고 자산 평가에는 합산하지 않는다.",
            "⑤ 보조금 전액을 잡수익으로 즉시 영업외수익 보고한 뒤 자본화와는 연계하지 않는다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 18에 따르면, 자본화기간 중 적격자산에 대한 평균누적지출액을 산정할 때에는 해당 자산과 관련하여 수령한 정부보조금이나 공사대금 기성금 수령액을 지출액에서 직접 차감하여 순 지출 실질 기준으로 계산하도록 규정하고 있습니다.\n\n[오답 해설]\n① 보조금 효과를 묵살하면 지출액이 과대 평가되어 차입원가가 과도하게 자본화됩니다.\n③ 지출액에 가산하는 것은 정반대의 회계 왜곡입니다.\n④ 부채 이월이나 ⑤ 잡수익 즉시 인식은 자산 순누적지출액 차감 규정과 어긋납니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "보조금 수령액을 공제하지 않으면 이자가 과다 자본화되므로 오답입니다.", "articles": ["K-IFRS 제1023호 문단 18"], "principle": "정부보조금 수령 시 누적지출액 계산의 차감 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "지출을 메워준 정부보조금이나 기성회수액을 공제하여, 회사가 순수하게 자기 자금(또는 차입 자금)으로 감당하여 적립된 실제 누적 적수 지출액만을 자본화 대상으로 유도하도록 한 기준에 일치합니다.", "articles": ["K-IFRS 제1023호 문단 18"], "principle": "정부보조금 수령 시 누적지출액 계산의 차감 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보조금 가산설은 규정과 정반대의 오답입니다.", "articles": [], "principle": "정부보조금 수령 시 누적지출액 계산의 차감 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 적립 분류는 순 지출액 산출 원리에 위배됩니다.", "articles": [], "principle": "정부보조금 수령 시 누적지출액 계산의 차감 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "즉시 잡수익 인식으로 자본화 차감을 생략하는 처리는 기준서 조항과 저촉됩니다.", "articles": [], "principle": "정부보조금 수령 시 누적지출액 계산의 차감 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "다음 중 자본화 개시를 위한 필수적인 3대 실질 요건이 모두 만족되는 첫 날을 찾아 개시일을 결정할 때, 개시일 결정의 시차 불일치에 따른 K-IFRS 상의 의사결정 원리로 옳은 것은?",
        "options": [
            "① 지출 발생일, 차입원가 발생일, 준비 활동 개시일 중 가장 먼저 도래한 날을 기준으로 자본화를 강제 개시한다.",
            "② 세 가지 사건(지출, 차입이자, 준비 활동)이 모두 동시에 만족되는 날(즉, 세 날짜 중 가장 늦게 도래하는 날)을 개시일로 설정한다.",
            "③ 은행에서 차입금 계약서에 서명한 날을 무조건 개시일로 의제한다.",
            "④ 토지 취득 지출이 발생한 지 1년이 지나서 이자가 발생하더라도 1년 전으로 소급해 개시한다.",
            "⑤ 건설 설계 용역을 체결한 날과 차입금 입금일의 단순 중간 날짜를 쓴다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 22에 명시된 자본화 개시일은 지출이 발생하고(Expenditures incurred), 차입원가가 발생하며(Borrowing costs incurred), 자산의 의도된 용도를 위해 활동을 수행 중(Activities in progress)이라는 세 가지 조건이 '모두 충족되는 날'이어야 하므로, 개별 날짜 중 가장 늦게 만족되는 시점에 개시일이 도래합니다.\n\n[오답 해설]\n① 가장 먼저 도래하는 날에 시작하면 요건이 충족되지 않은 상태(예: 차입을 안 했거나 준비가 안 됨)에서 자본화가 일어나므로 부적절합니다.\n③ 계약 서명일이나 ⑤ 임의 평균일 등은 개시일 요건이 아닙니다.\n④ 미발생 금융 비용을 소급하여 자본화할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "가장 이른 날 개시 시 자산 과대계상 및 미충족 상태 자본화 리스크가 있어 규정 위반입니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "자본화 개시일의 시차 결정 원리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "세 가지 조건(적격 지출, 이자 발생, 준비 행동) 중 가장 늦은 날짜에 도달해서야 삼자 요건이 최종 결합 만족되므로 이를 첫 날로 본다는 실질 원리를 완벽히 이해했습니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "자본화 개시일의 시차 결정 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계약서 명목 서명일은 실질 건설 투입일과 다를 수 있습니다.", "articles": [], "principle": "자본화 개시일의 시차 결정 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융비용 소급 적용은 인정되지 않습니다.", "articles": [], "principle": "자본화 개시일의 시차 결정 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 중간일 대입 주장은 오답입니다.", "articles": [], "principle": "자본화 개시일의 시차 결정 원리", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "회계이론적 및 수익·비용 대응의 관점에서, K-IFRS 기준서가 적격자산 건설에 소요된 차입원가를 당기 비용이 아닌 자산의 취득원가로 자본화하도록 규정하는 근본적인 당위성(회계학적 취지)에 관한 설명으로 가장 적절한 것은?",
        "options": [
            "① 당기에 이자비용을 많이 털어내면 주주배당을 더 많이 할 수 있기 때문이다.",
            "② 건설 기간 중에 발생한 이자는 미래 당해 자산의 가동을 통해 창출할 수익과 미래에 대응되어야 하므로, 자산원가에 포함해 두었다가 후속적인 감가상각 과정을 거쳐 매출원가 및 비용으로 유기적으로 기간배분(Matching)하기 위함이다.",
            "③ 자본 조달 비용을 자산으로 표시함으로써 회사의 부채비율을 인위적으로 급락시켜 신용등급을 교란하기 위함이다.",
            "④ 이자비용은 세법상 전액 손금불산입되는 자본거래 성격이기 때문이다.",
            "⑤ 건설업의 단기 세제 혜택을 극대화하기 위해 설계된 정치적 임시 조항이다."
        ],
        "answer": "2",
        "explanation": "② 차입원가 자본화의 이론적 핵심은 역사적 취득원가의 관점과 수익·비용 대응 원칙입니다. 자산을 의도된 용도로 사용할 상태로 만들기까지의 모든 불가피한 희생(금융 비용 포함)은 자산 취득원가의 구성 항목이어야 하며, 해당 자산의 내용연수 동안 감가상각비를 통해 미래 매출 및 수익과 올바르게 조화 대응됩니다.\n\n[오답 해설]\n① 이자비용의 자산화는 당기순이익을 늘려 배당 가능 이익을 늘리지만, 이는 자본화의 본질적인 매칭 취지가 아닌 부가적 결과일 뿐입니다.\n③ 신용등급 교란이나 ⑤ 정치적 세제 목적 등은 회계학적 자본화의 진실한 이론적 의도가 아닙니다.\n④ 세무상 손금불산입 여부와 IFRS 자본화 규정의 회계이론적 취지는 결이 다릅니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "주주 배당 가용 이익 확보가 이자 자본화 규정의 본원적 학술 배경이 될 수 없습니다.", "articles": [], "principle": "차입원가 자본화의 회계이론적 배경", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산이 완성된 후 수년에 걸쳐 용역을 제공하고 매출을 실현할 것이므로, 해당 자산의 완성까지 투입된 금융비용도 유형자산 역사적 원가로 유보했다가 감가상각으로 수익에 대응시킨다는 매칭 사상에 완벽히 정합합니다.", "articles": ["K-IFRS 제1023호"], "principle": "차입원가 자본화의 회계이론적 배경", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채비율 인위 왜곡 지표 개선은 회계 기준이 지향하는 가치와 반대입니다.", "articles": [], "principle": "차입원가 자본화의 회계이론적 배경", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 세제와 연계된 소득 계산 목적 설명은 부적당합니다.", "articles": [], "principle": "차입원가 자본화의 회계이론적 배경", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정치적/세제 혜택 논리는 회계적 당위성을 설명하지 못합니다.", "articles": [], "principle": "차입원가 자본화의 회계이론적 배경", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "K-IFRS 제1023호에 규정된 차입원가 범위 중 외화차입금과 관련하여 발생하는 '외환차이(Exchange differences)'의 자본화 허용 여부 및 조건에 대한 설명으로 옳은 것은?",
        "options": [
            "① 외환차이는 기중에 환율이 등락하면 징수 유무를 불문하고 이자 비용과 상관없이 무조건 100% 자본화에 투입한다.",
            "② 외화차입금 관련 외환차이는 '이자비용의 조정(Adjustment to interest costs)'으로 간주되는 범위 내에서만 차입원가로 분류되어 자본화가 가능하다.",
            "③ 외환차이는 기업의 영업 활동과 직접 관련이 없으므로 회계기준상 원천적으로 자본화의 범위에 들어올 수 없다.",
            "④ 세무대리인의 확인을 필한 경우에만 영업외손익으로 보낸 후 자산액에 합산한다.",
            "⑤ 환율 상승 시 발생한 이익분만 골라서 자산에 가산한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 6에 따르면, 외화차입금과 관련하여 발생하는 외환차이는 '이자비용의 조정으로 간주되는 한도 내에서만' 차입원가의 범위에 포함시켜 자본화 처리를 허용합니다.\n\n[오답 해설]\n① 환율 등락에 따른 모든 외환차이를 아무 한도 없이 자산화하는 것은 허용되지 않습니다.\n③ 외환차이가 이자 조정 요건을 충족하면 자본화 가능하므로 전면 불허 주장은 오답입니다.\n④ 세무대리인 확인 절차나 ⑤ 환차익 편식 자산화 등은 자의적인 왜곡 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "무조건 100% 자본화한다는 진술은 기준서 한도 조건에 저촉됩니다.", "articles": ["K-IFRS 제1023호 문단 6"], "principle": "외화차입금 외환차이의 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "외환차이 중 이자 조정 범위(예: 해외에서 낮은 금리로 차입하는 대신 부담하게 되는 환율 차이 등)로 인정되는 부분만을 차입원가로 규정하여 자본화를 통제하는 조항에 완벽하게 일치합니다.", "articles": ["K-IFRS 제1023호 문단 6"], "principle": "외화차입금 외환차이의 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "범위 편입이 가능하므로 원천 차단 주장은 오답입니다.", "articles": ["K-IFRS 제1023호 문단 6"], "principle": "외화차입금 외환차이의 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 처리 요건으로 회계 원리를 왜곡하여 오답입니다.", "articles": [], "principle": "외화차입금 외환차이의 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익분만을 가산하는 변칙 회계는 인정되지 않습니다.", "articles": [], "principle": "외화차입금 외환차이의 자본화 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "여러 부분으로 구성되어 부분별로 순차 건설되는 대형 복합 적격자산의 경우, 특정 부분의 건설이 완료되었을 때 그 완료된 부분에 대한 차입원가 자본화의 '종료(Cessation)' 처리에 관해 K-IFRS 제1023호가 선언하는 올바른 실질 원칙은?",
        "options": [
            "① 복합 프로젝트 전체의 최후 한 부분이 마저 끝날 때까지는 개별 완료 부분도 이자를 계속 자본화하여 자산을 늘린다.",
            "② 적격자산의 각 부분이 다른 부분의 건설이 계속되는 동안에도 독립적으로 사용가능하다면, 그 일부분을 의도된 용도로 사용하거나 판매가능한 상태에 이르게 하는 데 필요한 거의 모든 활동이 완료되었을 때 당해 완료 부분의 차입원가 자본화를 종료한다.",
            "③ 공장 전체 가동률이 100%에 도달할 때까지는 모든 부분의 자본화 종료를 금지한다.",
            "④ 건설사 부도 시에만 완료된 부품의 이자를 일괄 종료한다.",
            "⑤ 각 부분의 완공 순서와 상관없이 무조건 5년간 연간 균등 강제 자본화한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 27에 의하면, 적격자산의 각 부분이 다른 부분의 건설이 계속되는 동안에 독립적으로 사용 가능하다면(예: 여러 동으로 구성된 업무용 단지에서 완공된 일부 동의 선사용 등), 그 일부분의 준비 활동이 사실상 완료된 시점에 당해 완료 부분에 대한 차입원가 자본화를 개별적으로 종료해야 합니다.\n\n[오답 해설]\n① 독립 사용가능함에도 전체 완공일까지 이자를 계속 자본화하는 것은 허용되지 않습니다.\n③ 공장 전체 가동률 100% 지표나 ④ 건설사 부도 여부, ⑤ 5년 강제 배분 등은 독립적 사용 가능에 따른 부분별 완료 규정과 부합하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "개별 독립 사용 가능한 부분이 완공되었음에도 프로젝트 전체 종결 시까지 지연 종료하는 것은 과도한 이자 자본화를 유발해 금지됩니다.", "articles": ["K-IFRS 제1023호 문단 27"], "principle": "적격자산의 부분별 자본화 종료 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "여러 동의 아파트 단지 등 개별 동이 먼저 준공되어 독립 사용이 가능해진 경우, 해당 동에 배분되는 차입금 이자는 완공 시점에 즉시 자본화를 마치도록 한 분할 종료 규정을 충실히 설명했습니다.", "articles": ["K-IFRS 제1023호 문단 27"], "principle": "적격자산의 부분별 자본화 종료 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가동률 지표는 자본화 완료 시점의 판단 실질이 아닙니다.", "articles": [], "principle": "적격자산의 부분별 자본화 종료 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부도 여부는 자본화 종료 실질과 무관합니다.", "articles": [], "principle": "적격자산의 부분별 자본화 종료 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 5년 균등 배분 설명은 오답입니다.", "articles": [], "principle": "적격자산의 부분별 자본화 종료 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "기업이 지배기업(모회사)이나 관계기업으로부터 시장 이자율 수준으로 유인하여 자금을 조달하고, 이를 적격자산 건설에 직접 사용하여 이자비용을 지급한 경우, 이 특수관계자 간 차입금 이자의 K-IFRS 상 자본화 허용 규정에 관한 설명으로 옳은 것은?",
        "options": [
            "① 특수관계인 차입금은 내부 거래에 해당하므로 개별 재무제표 상에서도 전면 자본화가 불허된다.",
            "② 개별 재무제표 상에서 해당 차입금과 이자 지출이 실질적인 적격자산 요건을 충족하고 실제 차입 금융비용을 형성한다면 차입원가 자본화의 요건에 따라 정상적으로 자본화할 수 있다.",
            "③ 세법에 따라 특수관계자 이자는 무조건 20% 페널티 차감 후 자본화한다.",
            "④ 특수관계자 차입 이자는 영업외비용으로만 잡고 자산에는 전혀 가산할 수 없다.",
            "⑤ 지배주주의 승인 서명이 있으면 회수가능액의 300%까지 이자를 임의로 부풀려 자본화한다."
        ],
        "answer": "2",
        "explanation": "② 특수관계자 차입금이라 하더라도 개별 기업의 법적 실체 관점에서 실제 이자 비용이 발생하고 적격자산 건설에 정상 투입되었다면 K-IFRS 제1023호의 자본화 기준을 엄격하게 적용하여 자본화할 수 있습니다 (연결재무제표 상 소거 거래와 개별 재무제표 상 실질의 구분).\n\n[오답 해설]\n① 개별재무제표 상에서는 실질 부채거래이므로 전면 불허 주장은 오답입니다.\n③ 20% 페널티나 ⑤ 300% 부풀림 등은 임의의 왜곡 보기에 해당합니다.\n④ 개별 재무제표 상 자본화 편입이 가능하므로 가산 불가설은 틀렸습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "개별 보고 실체 관점에서 발생하는 이자비용을 무조건 불허하지는 않으므로 오답입니다.", "articles": ["K-IFRS 제1023호"], "principle": "특수관계자 차입 이자의 개별재무제표 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "개별 회사의 장부상 실제 이자가 흐르고 적격자산에 연동되었다면 개별 재무제표 관점에서는 자본화 대상 차입원가에 속함을 정확하게 분석했습니다.", "articles": ["K-IFRS 제1023호"], "principle": "특수관계자 차입 이자의 개별재무제표 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 세법상 차감 비율 제시는 오답입니다.", "articles": [], "principle": "특수관계자 차입 이자의 개별재무제표 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비용 단독 귀속설은 틀린 회계 지침입니다.", "articles": [], "principle": "특수관계자 차입 이자의 개별재무제표 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가치 부풀리기 등의 설명은 회계 부정 진술이므로 오답입니다.", "articles": [], "principle": "특수관계자 차입 이자의 개별재무제표 자본화 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "일반차입금의 연도 중 잔액이 등락하고, 각 차입금별로 차입 시점과 만기 시점이 서로 달라 연중 존재한 기간이 상이할 때 일반차입금의 '연평균 잔액'을 산출하는 기간 가중평균 가중치 계산에 관한 K-IFRS 상의 원칙은?",
        "options": [
            "① 각 차입금의 연중 존재 기간의 적수(일수 또는 개월 수)를 가중치로 한 가중평균 잔액을 산출한다.",
            "② 실제 조달 일수와 무관하게 연말 현재 남아있는 잔액의 단순 기말 명목 액수를 쓴다.",
            "③ 연중 발생한 최고 잔액과 최저 잔액을 더해 2로 나눈 값을 쓴다.",
            "④ 주주총회 결의로 지정한 특정 월의 1일 잔액을 고정 대입한다.",
            "⑤ 모든 차입금의 만기 상환 예정 총액의 산술합계를 쓴다."
        ],
        "answer": "1",
        "explanation": "① 일반차입금의 기중 가중평균이자율 계산을 위한 분모인 일반차입금 연평균 잔액은 각 일반차입금이 연중 존재했던 개월 수 또는 일수(적수)를 12개월 또는 365일 기준으로 안분 계산한 가중평균 연잔액을 뜻합니다.\n\n[오답 해설]\n② 기말 단독 잔액을 쓰면 기중 조기 상환된 차입금 정보가 누락되어 연평균 잔액이 왜곡됩니다.\n③ 최고/최저의 평균이나 ④ 특정일 잔액 고정, ⑤ 만기 상환 총액 단순합 등은 금융 시간가치 및 잔존 실질에 저촉되는 오답 계산입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "각 부채 차입금별 연중 유효하게 존재했던 개월 수 또는 일수를 곱해 연가중 평균 잔액을 유도하는 적수 가중 원리를 적합하게 지목하였습니다.", "articles": ["K-IFRS 제1023호 문단 14"], "principle": "일반차입금 연평균 잔액의 적수 가중평균 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "연말 단순 기말액 사용 주장은 기중 소멸 차입 잔액을 고려하지 못해 왜곡을 낳습니다.", "articles": [], "principle": "일반차입금 연평균 잔액의 적수 가중평균 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "최고/최저 단순 연산 평균은 회계적 적수 계산과 무관합니다.", "articles": [], "principle": "일반차입금 연평균 잔액 of 적수 가중평균 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주총 결의에 따른 특정일 잔액 차용 주장은 오답입니다.", "articles": [], "principle": "일반차입금 연평균 잔액의 적수 가중평균 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 만기 총액 가산설은 잔액 실질을 반영하지 못합니다.", "articles": [], "principle": "일반차입금 연평균 잔액의 적수 가중평균 원리", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "기업이 건물을 지을 목적으로 나대지(토지)를 구입한 경우, 토지 매입 자금과 관련하여 지급한 이자비용을 K-IFRS 상 차입원가로 자본화하여 '토지 자산원가'에 산입하기 위한 지출 및 조업 상의 필수 조건은 무엇인가?",
        "options": [
            "① 토지는 감가상각이 안 되므로 토지 관련 이자는 어떠한 상황에서도 절대 자본화할 수 없다.",
            "② 토지 구입 후 단순히 보유(방치)만 하더라도 토지 관련 차입원가는 자동으로 매년 토지원가에 자본화된다.",
            "③ 토지 취득 지출이 발생하고, 그 토지를 건물의 건설 등 의도된 목적을 위한 적격 자산으로 만들기 위해 실질적인 굴착, 개발, 정지 등 적극적인 준비 활동(Active development)이 수행되고 있는 기간 동안에만 토지 관련 이자를 토지(또는 건물) 원가에 자본화할 수 있다.",
            "④ 토지를 국가에 기부채납하는 조건 하에서만 임시 자본화가 허용된다.",
            "⑤ 토지 주변 주택 가격이 상승하는 기간에만 시가 상승률만큼 이자를 자본화한다."
        ],
        "answer": "3",
        "explanation": "③ 토지 지출에 대한 이자비용은 토지를 매입한 후 단순히 방치하는 기간에는 자본화할 수 없습니다. 토지를 취득하고 이를 목적 상태로 만들기 위한 실질적인 준비 및 정지, 개발 활동(적극적인 조업)이 일어나는 기간 동안에만 차입원가를 자본화할 수 있습니다.\n\n[오답 해설]\n① 준비/개발 활동 수행 시에는 자본화가 가능하므로 절대 불가 주장은 틀렸습니다.\n② 보유 방치 기간에는 자본화가 전면 금지되어 당기 비용 처리해야 하므로 오답입니다.\n④ 기부채납 요건이나 ⑤ 주택 가격 연계 요인 등은 자본화 기준과 연계되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "토지 개발 조업 기간에는 자본화가 성립되므로 전면 불허 주장은 오답입니다.", "articles": [], "principle": "토지 지출 관련 차입원가 자본화 요건", "case": {"holding": "토지", "no": None}},
            {"correct": False, "why": "보보유·방치 기간에는 자본화를 중지하고 전액 당기 비용 처리해야 하므로 규정 위반입니다.", "articles": ["K-IFRS 제1023호"], "principle": "토지 지출 관련 차입원가 자본화 요건", "case": {"holding": "토지", "no": None}},
            {"correct": True, "why": "나대지 매입 후 단순 보유 상태가 아니라 흙을 깎고 건물을 올리기 위한 물리적 조업 활동(적극적인 활동)이 실제 개시되고 지속되는 시기 동안에만 금융비용 가산이 가능함을 적합하게 발라냈습니다.", "articles": ["K-IFRS 제1023호"], "principle": "토지 지출 관련 차입원가 자본화 요건", "case": {"holding": "토지", "no": None}},
            {"correct": False, "why": "기부채납은 토지 자본화 개시 요건이 아닙니다.", "articles": [], "principle": "토지 지출 관련 차입원가 자본화 요건", "case": {"holding": "토지", "no": None}},
            {"correct": False, "why": "지가 변동과 이자 자본화는 하등 무관합니다.", "articles": [], "principle": "토지 지출 관련 차입원가 자본화 요건", "case": {"holding": "토지", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "유형자산을 장기연불조건(대금 분할 납부) 또는 할부 계약으로 취득하는 경우, 명목 매입 대금에 가산되어 지급되는 '이자 상당액'에 관한 K-IFRS 상의 회계적 성격 분류 및 차입원가 자본화 연동에 관한 설명으로 옳은 것은?",
        "options": [
            "① 장기연불이자는 자산의 역사적 구입원가에 무조건 전액 산입되고, 이자비용으로는 어떤 경우에도 인식하지 않는다.",
            "② 연불 구입에 따른 이자액은 원칙적으로 신용공여기간(할부기간)에 걸쳐 이자비용(당기손익)으로 인식하되, 당해 자산 취득 거래가 K-IFRS 제1023호 상의 '적격자산' 요건을 충족한다면 차입원가 자본화 규정에 의해 자산 원가에 산입할 수 있다.",
            "③ 장기연불이자는 자본을 직접 감소시키는 자본차감 항목이다.",
            "④ 할부 구입 이자는 차입원가의 정의에서 법적으로 배제되므로 자본화가 원천 차단된다.",
            "⑤ 대금 결제 비율만큼 유형자산 감가상각비를 직접 차감하여 조정한다."
        ],
        "answer": "2",
        "explanation": "② 장기연불 조건으로 취득 시, 현재가치와 명목 할부금의 차액(할부 이자 부분)은 신용제공기간 동안 이자비용으로 상각 인식합니다. 다만 이 기계나 자산 취득 거래 자체가 대규모 장기 적격자산 취득에 부합하여 차입원가 자본화 요건을 통과한다면, 당해 이자 부분도 차입원가의 일종으로 보아 자산원가에 보태는 자본화 기장이 가능합니다.\n\n[오답 해설]\n① 무조건 이자비용을 부인하고 자산 원가에 다 밀어 넣을 수는 없습니다.\n③ 자본 차감 계정이 아니며 부채 상각 및 손익 계정입니다.\n④ 신용 공여 관련 이자 부분도 차입원가의 범위에 부합할 수 있으므로 원천 차단설은 오답입니다.\n⑤ 상각비 직접 조정 주장은 허무맹랑한 거짓입니다.",
        "type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "취득시점에 명목가로 무조건 자산 가산하는 처리는 현재가치 평가 원칙에 위배됩니다.", "articles": ["K-IFRS 제1016호 문단 23"], "principle": "장기연불 취득 자산의 이자상당액 처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "현재가치 할인에 따른 이자 부분은 기중 이자비용으로 분배 상각하되, 당해 취득 자산이 1년 이상 제작을 요하는 적격자산이라면 기준서 제1023호에 따라 차입원가 자본화에 편입시켜 취득원가화할 수 있음을 정확히 설명하였습니다.", "articles": ["K-IFRS ... 문단 23, 제1023호 문단 6"], "principle": "장기연불 취득 자산의 이자상당액 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 직접 거래가 아니므로 자본차감 주장은 틀렸습니다.", "articles": [], "principle": "장기연불 취득 자산의 이자상당액 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "신용공여 이자 상당도 차입원가 범위에 속할 수 있어 자본화 차단설은 오답입니다.", "articles": [], "principle": "장기연불 취득 자산의 이자상당액 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각비 차감 조정설은 회계 이론상 저촉됩니다.", "articles": [], "principle": "장기연불 취득 자산의 이자상당액 처리", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "유형자산 공장 건설을 개시하기 전에 설계 도면 작성, 지질조사, 인허가 획득 등을 위한 '행정적·기술적 준비 활동(Planning & design stage)'을 이행하는 단계에서 발생한 관련 차입금의 이자비용에 대한 K-IFRS 상 자본화 허용 여부 판정은?",
        "options": [
            "① 물리적 착공(삽을 뜨는 행위)이 일어나지 않은 준비 단계의 이자는 무조건 당기 비용이다.",
            "② 물리적 착공 전이라도 적격자산을 의도된 용도로 사용가능한 상태로 만들기 위해 필수적으로 요구되는 기술적·행정적 준비 활동이 수행되고 있다면 자본화 개시 요건을 갖추어 이자를 자본화할 수 있다.",
            "③ 준비 단계의 이자는 자본잉여금으로 임의 이월한다.",
            "④ 기중 발생한 차입이자 총액의 10%만 일괄 비용 처리한다.",
            "⑤ 건설회사 동의를 얻을 때에만 감가상각누계액 가산 항목으로 분류한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 22에 따르면, 개시 요건 중 '준비 활동'은 단순히 물리적 건설뿐만 아니라 자산 완성에 필수적인 행정적·기술적 준비 활동(설계, 인허가 절차 등)을 이행하는 기간도 포함됩니다. 따라서 이 기간에 지출과 차입이자가 동시 발생하고 있다면 착공 전이라도 자본화가 가능합니다.\n\n[오답 해설]\n① 물리적 착공만을 기준 삼는 것은 기준서의 준비 활동 범위를 협소하게 오해한 오답입니다.\n③ 자본잉여금 이월, ④ 10% 일괄 처리, ⑤ 상각누계액 가산 등은 모두 자본화 조항과 무관한 자의적 기장입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "착공 전이라도 자본화 요건을 달성할 수 있으므로 강제 당기비용화 진술은 오답입니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "착공 전 준비 단계 차입이자의 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "물리적 삽을 뜨기 전 단계인 지질 검사 및 기술 설계, 행정 인허가 이행 등의 준비 기간 역시 자산 준비를 위한 필수 활동이므로, 개시의 타당성을 인정한 조항에 부합합니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "착공 전 준비 단계 차입이자의 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 항목으로의 임의 이월은 불가능하므로 오답입니다.", "articles": [], "principle": "착공 전 준비 단계 차입이자의 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "고정 비율 10% 감액 및 일괄 비용 등은 가설적 수치에 불과합니다.", "articles": [], "principle": "착공 전 준비 단계 차입이자의 자본화 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "협력사 합의 등 거래 관행은 회계 기준 판정에 영향을 주지 못합니다.", "articles": [], "principle": "착공 전 준비 단계 차입이자의 자본화 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "일반차입금의 자본화가능액을 구하기 위하여 적격자산의 평균누적지출액에서 특정차입금의 평균사용액을 차감하였더니 차감액이 마이너스(-) 또는 ₩0 이하로 도출된 경우, 일반차입금으로부터 자본화할 이자비용의 결정은?",
        "options": [
            "① 일반차입금의 연간 발생 이자 전액을 그대로 강제 자본화한다.",
            "② 일반차입금으로 충당한 건설 지출이 전혀 존재하지 않음을 뜻하므로, 일반차입금에 귀속될 자본화가능 차입원가는 ₩0으로 결정된다.",
            "③ 마이너스액 만큼을 무조건 잡손실로 당기 비용 처리한다.",
            "④ 특정차입금의 남는 한도만큼 일반차입금 이자비용에 가산한다.",
            "⑤ 일반차입금 이자비용을 대변에 기장하여 수익으로 환원한다."
        ],
        "answer": "2",
        "explanation": "② 평균누적지출액(건설에 쏟은 자금 적수)이 특정차입금 평균액(자산 전용 차입금)보다 작다는 것은 적격자산 건설에 들어간 돈 전체를 특정차입금만으로 다 덮고도 남았음을 의미합니다. 이 경우 공통 풀인 일반차입금 자본이 건설에 투입된 비율은 전혀 없으므로 일반차입금에서 추출하여 자본화할 이자는 ₩0(없음)이 올바른 실질입니다.\n\n[오답 해설]\n① 투입되지도 않은 일반 차입 이자를 강제 자본화하면 자산 과대계상 및 부정 기장입니다.\n③ 잡손실로의 별도 인식이나 ④ 특정차입금 이율 가산, ⑤ 수익 환원 등은 회계 논리에 위배되는 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "투입 비율이 없는데도 일반차입금 전체를 자본화하면 왜곡 기장이 되므로 오답입니다.", "articles": [], "principle": "일반차입금 배분액 ₩0 판정 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "건설비 지출 평균보다 특정 용도 차입금이 더 크거나 같아 일반차입금 배분액(평균지출 - 특정차입평균)이 ₩0 이하가 되면, 일반차입 자금의 투입분이 없어 자본화 금융비용이 ₩0이 된다는 원리에 완벽히 맞습니다.", "articles": ["K-IFRS 제1023호 문단 14"], "principle": "일반차입금 배분액 ₩0 판정 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 손실 계상 설명은 거짓입니다.", "articles": [], "principle": "일반차입금 배분액 ₩0 판정 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "특정차입금과의 한도 강제 결합 및 가산은 오답입니다.", "articles": [], "principle": "일반차입금 배분액 ₩0 판정 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자비용 대변 기장 수익화 주장은 회계 순환 논리에 어긋납니다.", "articles": [], "principle": "일반차입금 배분액 ₩0 판정 요건", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "주식회사 미래가 보유한 토지(나대지)에 신규 사옥 건물을 신축하기로 결의하고 공사를 시작하였다. 이 과정에서 지급된 토지 취득 지출액과 건물 공사 지출액에 대하여, 건물 건설 기간 동안의 자본화대상 '평균누적지출액' 계산 시 토지 매입 지출의 포함 여부에 대한 K-IFRS 상의 판정은?",
        "options": [
            "① 토지는 토지이고 건물은 건물이므로, 건물 건설을 위해 빌린 돈의 이자 계산 시 토지 지출액은 무조건 전액 제외한다.",
            "② 건물 신축 활동(토지 정지, 굴착 등)이 개시되었다면, 토지의 준비가 건물 자산 완성을 위한 필수적인 지출의 일부를 형성하므로, 건물 건설의 자본화 이자 계산 시 토지 관련 지출액도 평균누적지출액의 구성 요소에 합산 반영하여야 한다.",
            "③ 토지 매입비의 50%만 매년 강제로 깎아 가산한다.",
            "④ 토지 이자는 건물 감가상각 완료 후에만 소급 합산한다.",
            "⑤ 토지 관련 매입비 지출은 이자 자본화 계산 시 오직 특정차입금 잔액에서만 강제로 뺀다."
        ],
        "answer": "2",
        "explanation": "② 건물을 올리기 위한 목적으로 취득한 토지의 경우, 토지 매입 지출은 건물 완성에 이바지하는 필수 기초 지출을 형성합니다. 따라서 건물의 건설 기간 동안 발생하는 차입원가 자본화 계산(평균누적지출액 산정) 시 토지 취득 관련 지출액도 분모/평균지출액 계산에 당연히 포함하여 차입원가를 가산하여야 합니다.\n\n[오답 해설]\n① 토지 관련 지출을 기계적으로 전액 차단하는 것은 자산 지출 실질의 범위를 오류 판단한 것입니다.\n③ 50% 강제 할인, ④ 감가상각 완료 후 소급, ⑤ 특정차입금에서 강제 공제 등은 기준에 없는 거짓 진술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "토지 지출의 가산을 전면 부인하면 자본화할 이자가 과소 평가되므로 규정에 저촉됩니다.", "articles": ["K-IFRS 제1023호"], "principle": "사옥 신축 시 토지 지출의 평균누적지출액 포함 여부", "case": {"holding": "토지", "no": None}},
            {"correct": True, "why": "건물이 올라가는 부지가 되는 토지 취득비는 건물 건설에 필수 결합되는 누적 선지출액이므로, 건물 관련 평균누적지출액 계산에 토지 투입 원장을 합산하여 평균치를 유도한다는 규정에 완벽하게 부합합니다.", "articles": ["K-IFRS 제1023호"], "principle": "사옥 신축 시 토지 지출의 평균누적지출액 포함 여부", "case": {"holding": "토지", "no": None}},
            {"correct": False, "why": "특정 비율 50% 대입 주장은 근거 없는 거짓 보기입니다.", "articles": [], "principle": "사옥 신축 시 토지 지출의 평균누적지출액 포함 여부", "case": {"holding": "토지", "no": None}},
            {"correct": False, "why": "소급 합산설 등은 회계 규칙과 무관합니다.", "articles": [], "principle": "사옥 신축 시 토지 지출의 평균누적지출액 포함 여부", "case": {"holding": "토지", "no": None}},
            {"correct": False, "why": "특정차입금 잔액에서만 뺀다는 설명도 자본화 산수 공식에 어긋나는 왜곡입니다.", "articles": [], "principle": "사옥 신축 시 토지 지출의 평균누적지출액 포함 여부", "case": {"holding": "토지", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "유형자산 공장 설비의 물리적 외장 조립이 모두 끝났으나, 의도된 상태로의 실제 가동이 가능한지 여부를 확인하기 위해 '시험생산(Test run) 및 시운전'을 이행하는 기간이 존재할 때, 이 시운전 기간 동안 발생하는 차입금 이자비용의 자본화 여부에 관한 K-IFRS 상의 지침으로 옳은 것은?",
        "options": [
            "① 물리적 조립 완료일(외장 완성일)에 자본화가 무조건 종료되므로 시운전 기간의 이자는 자본화할 수 없다.",
            "② 시운전 및 테스트 역시 자산을 의도된 용도로 사용가능한 상태에 이르게 하는 데 필요한 필수적인 활동이 수행 중인 기간에 해당하므로, 이 시운전 기간 동안의 차입원가도 계속 자본화하여 자산에 얹는다.",
            "③ 시운전 기간의 이자는 즉시 이익잉여금 전기이월액에서 직접 차감한다.",
            "④ 시운전 이자는 전액 잡손실로 계상하되 부가가치세를 환급받는다.",
            "⑤ 건설회사와 공동 부담하여 50%만 비용 처리한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1023호 문단 25에 의하면, 자산이 의도된 용도로 작동할 수 있는지를 확인하기 위한 시험(테스트 및 시운전)을 수행하는 기간은 자산 준비에 필수적으로 요구되는 활동 기간에 해당하므로 차입원가 자본화를 멈추지 않고 완료 시까지 계속 가산합니다.\n\n[오답 해설]\n① 단순 물리적 조립이 끝났더라도 시험가동이 완료되지 않았다면 준비 활동이 끝난 것이 아니므로 자본화를 멈추는 것은 규정 위배입니다.\n③ 이익잉여금 직접 수정이나 ④ 부가세 환급 잡손실 계상, ⑤ 건설사 공동 분담 등은 자본화 기준과 연계되지 않는 임의의 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "외장 완성으로 바로 이자를 끊어버리면 시운전 필수비용 누락을 낳아 오답입니다.", "articles": ["K-IFRS 제1023호 문단 25"], "principle": "시운전 테스트 기간 이자비용의 자본화 여부 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "정상 작동 여부를 시험하는 테스트(시운전) 공정도 자산을 목적 상태로 끌어올리는 필수 연장선이므로, 자본화 개시 연장(종료 지연)을 인정해 계속 가산함이 타당함을 설명했습니다.", "articles": ["K-IFRS 제1023호 문단 25"], "principle": "시운전 테스트 기간 이자비용의 자본화 여부 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익잉여금 직접 조정 거래가 아니므로 오답입니다.", "articles": [], "principle": "시운전 테스트 기간 이자비용의 자본화 여부 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잡손실 및 세제 조항 대입설은 회계 이론에 저촉됩니다.", "articles": [], "principle": "시운전 테스트 기간 이자비용의 자본화 여부 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "건설사 분담 배분 비율 등의 설명은 회계 기준과 무관합니다.", "articles": [], "principle": "시운전 테스트 기간 이자비용의 자본화 여부 판정", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s05-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "일반차입금의 실제 차입원가 한도 검토 규정(Min[일반차입금 자본화액 산출치, 실제 이자 발생액])이 기업회계 상 실재하는 핵심적인 회계학적 의미로 가장 올바른 설명은?",
        "options": [
            "① 발생하지도 않은 가상의 일반이자비용을 자산에 과도하게 부풀려 얹어 자산의 실질가치와 재무상태표를 과대 왜곡 표시하는 것을 전면 차단하기 위함이다.",
            "② 금융기관에 이자를 깎아달라고 정식 요청하기 위한 근거 조항이다.",
            "③ 주주들의 지분 평가율을 인위적으로 통제하기 위한 자본 규제 장치이다.",
            "④ 일반차입금의 실제 이자가 많을수록 자산액을 일부러 쪼그라뜨려 세금을 덜 내게 만들기 위함이다.",
            "⑤ 회계담당자의 수작업 계산 부담을 영구히 줄여주기 위한 편의 조항이다."
        ],
        "answer": "1",
        "explanation": "① 일반차입금 자본화 계산 시, 지출액에 자본화이자율을 곱해 기장할 금액이 만약 실제 회사가 낸 일반 차입 이자비용의 파이 자체를 초과해 버린다면, 회사는 '실제 조달하지 않은 가상의 금융비용'을 자산에 얹는 셈이 됩니다. 이는 역사적 취득가 원칙을 중대하게 위반하며 자산을 가공 부풀리는 사태를 유발하므로, 실제 지출된 일반 차입 금융비용 총액을 넘지 못하게 상한 장치를 둔 것입니다.\n\n[오답 해설]\n② 금융사 협상용 이자 삭감 근거나 ③ 주주 평가율 규제, ④ 인위적 자산 감축을 통한 탈세, ⑤ 담당자 편의 등은 회계학적인 한도 제약 규정의 본질적 의미가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "지출액 대비 차입금 평균이 작을 때 연산 상 실제 발생 금액보다 큰 가상의 이자가 계상되어 자산이 부풀려지는 것을 막기 위해, 실제 회사가 부담한 돈(실제 일반차입금 이자비용)을 상한으로 한정한다는 원리를 정확하게 파악했습니다.", "articles": ["K-IFRS 제1023호 문단 14"], "principle": "일반차입금 실제 이자 한도 규정의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대외 은행 금리 협상 등 영업 활동 용도로 규정된 룰이 아닙니다.", "articles": [], "principle": "일반차입금 실제 이자 한도 규정의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주주 지분 통제나 자본 규제와는 전혀 무관한 자산 원가 통제 장치입니다.", "articles": [], "principle": "일반차입금 실제 이자 한도 규정의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인위적 자산 왜곡이나 세금 탈루 목적 조항이 아니므로 오답입니다.", "articles": [], "principle": "일반차입금 실제 이자 한도 규정의 의의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "담당자 편의 제약은 규정의 학술적 의도가 아닙니다.", "articles": [], "principle": "일반차입금 실제 이자 한도 규정의 의의", "case": {"holding": "", "no": None}}
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
                "item": "5절 차입원가 자본화"
            }
        }
    }
]

questions.extend(part1_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(part1_questions)} new questions (Part 1). Total questions in questions_db_accounting.json: {len(questions)}")
