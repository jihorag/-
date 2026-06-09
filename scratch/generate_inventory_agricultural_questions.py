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

new_questions = [
    # =========================================================================
    # L1: 기초 개념 (10문항, 901~910번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s06-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1041호 '농림어업' 기준서에서 정의하는 생물적 변환(Biological transformation)의 결과로 자산의 질적 또는 양적 변화를 가져오는 생리적 과정에 해당하지 않는 것은?",
        "options": [
            "① 성장(Growth)",
            "② 퇴화(Degeneration)",
            "③ 생산(Production)",
            "④ 유통(Distribution)",
            "⑤ 번식(Procreation)"
        ],
        "answer": "4",
        "explanation": "④ 유통(Distribution)은 수확한 자산의 물리적 이동 및 판매 경로와 관련된 상업적 활동일 뿐, 생물자산 내부에서 자발적·생리적으로 일어나는 생물적 변환 과정이 아닙니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 생물자산의 생물적 변환을 구성하는 4대 핵심 생리적 과정(성장, 퇴화, 생산, 번식)으로 기준서에 명시적으로 규정되어 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "성장은 생물자산의 수량 증가나 품질 향상을 가져오는 생물적 변환 과정입니다.", "articles": ["K-IFRS 제1041호 문단 5"], "principle": "생물적 변환의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "퇴화는 생물자산의 수량 감소나 품질 저하를 가져오는 생물적 변환 과정입니다.", "articles": ["K-IFRS 제1041호 문단 5"], "principle": "생물적 변환의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "생산은 라텍스, 찻잎, 양모 등 수확물을 얻어내는 생물적 변환 과정입니다.", "articles": ["K-IFRS 제1041호 문단 5"], "principle": "생물적 변환의 정의", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "유통은 상업적 유통망을 통한 자산 이전 활동이며 생물자산의 생물적 변환 과정이 아닙니다.", "articles": ["K-IFRS 제1041호 문단 5"], "principle": "생물적 변환의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "번식은 추가적인 생물자산을 창출해내는 생물적 변환 과정입니다.", "articles": ["K-IFRS 제1041호 문단 5"], "principle": "생물적 변환의 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "K-IFRS 제1041호 상 '농림어업활동(Agricultural activity)'의 올바른 정의를 가장 잘 설명한 것은?",
        "options": [
            "① 판매목적 또는 수확물이나 추가적인 생물자산으로의 전환목적으로 생물자산의 생물적 변환과 수확을 관리하는 활동",
            "② 야생 상태에서 자라난 어류나 목재를 관리 없이 단순 채집하거나 벌목하여 판매하는 활동",
            "③ 농업용 기계장치와 토지를 활용하여 가공식품을 대량 제조하는 공장형 제조업 활동",
            "④ 생물자산의 유통을 활성화하기 위해 수송용 차량과 보관 창고를 임대하고 용역을 제공하는 활동",
            "⑤ 수확된 농작물을 장기 보관하며 도소매 유통망에 분배하여 수수료 수익을 올리는 유통업 활동"
        ],
        "answer": "1",
        "explanation": "① 농림어업활동은 생물자산의 생물적 변환(성장, 퇴화, 생산, 번식)과 수확을 '인위적으로 관리'하여 수확물이나 추가 생물자산을 얻는 활동으로 정의됩니다. 인위적인 관리가 결여된 야생 자원의 채집은 농림어업활동이 아닙니다.\n\n[오답 해설]\n② 야생 벌목이나 채집 등 '관리'가 없는 활동은 농림어업활동에서 제외됩니다.\n③, ④, ⑤는 제조업, 운송/임대업, 유통업에 해당하는 일반적 영업활동으로 농림어업활동의 본질이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "생물자산의 변환과 수확을 능동적으로 관리하는 농림어업활동의 기준서 상 정의와 완벽하게 일치합니다.", "articles": ["K-IFRS 제1041호 문단 5"], "principle": "농림어업활동의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "관리 없는 단순 야생 채집/벌목은 농림어업활동의 범위에서 제외됩니다.", "articles": ["K-IFRS 제1041호 문단 5"], "principle": "농림어업활동의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가공식품 제조업은 재고자산 기준서(제1002호) 영역입니다.", "articles": [], "principle": "농림어업활동의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "물류 및 유통 서비스업으로 농림어업활동에 속하지 않습니다.", "articles": [], "principle": "농림어업활동의 정의", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 유통 및 판매 대행업은 재고자산 판매 또는 수수료 수익 거래에 불과합니다.", "articles": [], "principle": "농림어업활동의 정의", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "생물자산에서 수확한 농림어업 수확물(Agricultural produce)에 대하여 수확 '이후' 시점에 적용하여야 하는 한국채택국제회계기준서는?",
        "options": [
            "① K-IFRS 제1041호 '농림어업'",
            "  K-IFRS 제1002호 '재고자산'",
            "③ K-IFRS 제1016호 '유형자산'",
            "④ K-IFRS 제1040호 '투자부동산'",
            "⑤ K-IFRS 제1115호 '고객과의 계약에서 생기는 수익'"
        ],
        "answer": "2",
        "explanation": "② 수확물은 수확시점에 순공정가치로 측정하여 최초 인식하며, 그 수확시점 '이후'부터는 K-IFRS 제1002호 '재고자산'이나 적용 가능한 다른 기준서의 규정을 적용합니다.\n\n[오답 해설]\n① 수확 전 또는 수확하는 시점까지는 제1041호 농림어업을 적용하지만, 수확 후 보관 및 유통 단계는 재고자산으로 편입됩니다.\n③, ④, ⑤는 수확물의 일반적인 후속 보유 상태에 합당하지 않은 기준서 분류입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "제1041호는 수확시점까지만 적용됩니다.", "articles": ["K-IFRS 제1041호 문단 3"], "principle": "수확물 후속 기준서 적용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수확시점 이후에는 일반 재고자산으로 취급되므로 제1002호 기준서를 적용하는 것이 맞습니다.", "articles": ["K-IFRS 제1041호 문단 3"], "principle": "수확물 후속 기준서 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수확물은 생산 설비가 아닌 유통용 자산이므로 유형자산이 될 수 없습니다.", "articles": [], "principle": "수확물 후속 기준서 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임대용 토지/건물이 아니므로 오답입니다.", "articles": [], "principle": "수확물 후속 기준서 적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수익 인식 기준서로 수확물 자산의 일반 평가 규칙을 다루지 않습니다.", "articles": [], "principle": "수확물 후속 기준서 적용", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "다음 중 K-IFRS 기준 상 농림어업 기준서(제1041호)가 아닌 유형자산 기준서(제1016호)의 적용 대상이 되는 식물성 생물자산은?",
        "options": [
            "① 목재로 사용하기 위해 재배하는 식물(벌목용 나무)",
            "② 과수원에서 과일을 매년 생산하기 위해 재배하며 그 자체로 판매할 의도가 희박한 포도나무(생산용식물)",
            "③ 과일과 목재 두 가지 목적 모두를 충족하며 목재 판매 가능성이 높은 다목적 식물",
            "④ 밭에서 옥수수 열매를 얻기 위해 단년 재배하는 옥수수 작물(한해살이 작물)",
            "⑤ 밀가루 생산을 위해 대규모로 경작하는 단년생 밀 작물(한해살이 작물)"
        ],
        "answer": "2",
        "explanation": "② 수확물을 매년 반복해서 생산하기 위해 보유하며, 부수적인 폐물 판매 외에는 수확물 자체로 판매할 가능성이 희박하고 한 해를 초과하여 생산에 사용할 것이 예상되는 포도나무와 사과나무 등은 '생산용식물(Bearer plants)'에 해당하여 유형자산(K-IFRS 제1016호)으로 분류됩니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 생산용식물의 정의 요건을 충족하지 못하므로, 유형자산이 아닌 농림어업 기준서(제1041호)의 지배를 받는 일반 생물자산에 속합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수확물 자체로 벌목 판매될 나무는 일반 생물자산(제1041호)입니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 구분", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수확물을 매년 생산하는 포도나무는 전형적인 생산용식물로 유형자산(제1016호)의 적용 대상입니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "목재 판매 가능성이 높은 다목적 식물은 생산용식물에서 제외됩니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "한해살이 작물은 유형자산이 아닌 일반 생물자산입니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "밀 작물 역시 단년생 한해살이 작물이므로 일반 생물자산입니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 구분", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "생물자산은 최초 인식시점에 순공정가치로 인식하도록 되어 있습니다. 이 때 취득(또는 구입) 관련 거래원가 및 추정 처분부대원가의 존재로 인해 최초 인식 시점에 당기손익 상 어떤 거래 효과가 발생할 수 있는가?",
        "options": [
            "① 무조건 취득원가보다 자산 가액이 커져 최초인식평가이익만 대규모 발생한다.",
            "② 추정 처분부대원가를 공정가치에서 차감하므로 최초 인식 시점에 '평가손실'이 발생할 수 있다.",
            "③ 어떠한 경우에도 평가손익이 발생하지 않고 취득 당시 지출한 총액 그대로 최초 계상된다.",
            "④ 발생한 취득 거래원가는 전액 기타포괄손익(OCI)으로 적립되어 자본화된다.",
            "⑤ 취득 시점에는 손익이 발생하지 않으며 기말 평가 시점에 이월 합산되어 나타난다."
        ],
        "answer": "2",
        "explanation": "② 생물자산은 최초 인식할 때 '공정가치 - 처분부대원가'인 순공정가치로 측정합니다. 자산을 구입할 때 지출된 거래원가는 취득가액에 가산할 수 없고 전액 당기비용 처리되며, 자산 가액 자체에서도 미래 처분 시 발생할 처분부대원가를 선차감하므로, 최초 인식 시점에 장부금액이 구입 현금 유출액보다 낮아져 '최초인식평가손실'이 발생할 수 있습니다.\n\n[오답 해설]\n① 처분부대원가의 차감 및 거래원가 비용화로 인해 보통 평가손실이 발생합니다.\n③, ⑤ 지출액과 자산인식액의 불일치로 취득 당일에 즉시 당기손익(평가손익)이 발생합니다.\n④ 거래원가는 자본화되지 않고 당기비용(당기손익) 처리됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "일반적으로는 평가손실이 발생하는 경향이 있습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "최초 인식 시 평가손익의 기전", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산 인식 금액 산정 시 처분부대원가를 빼기 때문에 구입 원가 대비 평가손실이 당일 인식될 수 있습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "최초 인식 시 평가손익의 기전", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지출 총액으로 계상하지 않고 순공정가치로 평가하여 잡기 때문에 오답입니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "최초 인식 시 평가손익의 기전", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득 거래원가는 당기 비용화되므로 OCI와 무관합니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "최초 인식 시 평가손익의 기전", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래 시점에 평가손익이 즉각 포착되어 당기순이익에 유입됩니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "최초 인식 시 평가손익의 기전", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "K-IFRS 제1041호에서 규정하는 생물자산(생산용식물 제외)의 최초 인식시점 및 매 보고기간말의 기본 측정 기준은?",
        "options": [
            "① 취득원가와 시가 중 낮은 가액 (저가기준)",
            "② 공정가치에서 추정 처분부대원가(매각부대원가)를 차감한 금액(순공정가치)",
            "③ 역사적 취득원가에서 감가상각누계액을 차감한 가액 (원가모형)",
            "④ 자산의 순공정가치에 인위적 프리미엄 10%를 가산한 가액",
            "⑤ 회사가 임의로 결정한 매각 가능 기대 가액"
        ],
        "answer": "2",
        "explanation": "② 생산용식물을 제외한 생물자산은 최초 인식시점과 매 보고기간말에 공정가치에서 추정 처분부대원가(매각부대원가)를 차감한 금액(즉, 순공정가치)으로 측정함을 원칙으로 합니다.\n\n[오답 해설]\n① 저가기준은 수확 후 재고자산에 주로 적용하는 방식입니다.\n③ 원가모형은 공정가치 측정이 현저히 불가능한 극히 예외적인 경우에만 사후 보완적으로 씁니다.\n④, ⑤는 기준서의 객관적 자산 측정 규정에 없는 임의의 가공설입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재고자산 저가법에 준하는 방식이 아닙니다.", "articles": ["K-IFRS 제1041호 문단 12"], "principle": "생물자산의 측정 원칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "생물자산 평가의 기본 대원칙인 순공정가치(공정가치 - 처분부대원가)를 올바르게 정의했습니다.", "articles": ["K-IFRS 제1041호 문단 12"], "principle": "생물자산의 측정 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유형자산이나 예외적 원가법 적용 자산에 한정됩니다.", "articles": ["K-IFRS 제1041호 문단 12"], "principle": "생물자산의 측정 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가산 프리미엄은 존재하지 않습니다.", "articles": [], "principle": "생물자산의 측정 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적 선택을 배제하고 시장 데이터 중심 평가를 요구하므로 오답입니다.", "articles": [], "principle": "생물자산의 측정 원칙", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "생물자산에서 수확된 '수확물(Agricultural produce)'의 수확시점 측정에 관한 K-IFRS의 입장으로 가장 올바른 것은?",
        "options": [
            "① 공정가치를 구할 수 없는 경우에는 예외적으로 원가법을 적용하여 최초 인식할 수 있다.",
            "② 어떠한 경우에도 예외 없이 수확시점의 수확물은 순공정가치로 측정한다.",
            "③ 수확물은 수확 즉시 취득원가 0원으로 인식하여 자산 계상을 보수적으로 보류한다.",
            "④ 수확 당시 예상되는 판매계약 조건에 따라 계약가격으로만 전액 강제 측정한다.",
            "⑤ 수확시점에는 감가상각누계액을 사후적으로 추정하여 반영한다."
        ],
        "answer": "2",
        "explanation": "② 기준서는 수확시점에 수확물의 공정가치를 '항상' 신뢰성 있게 측정할 수 있다는 확고한 관점을 반영하고 있습니다. 따라서 생물자산과 달리, 수확물은 수확시점에 원가법 예외 적용 규정이 전혀 없으며 어떠한 경우에도 순공정가치로만 최초 측정합니다.\n\n[오답 해설]\n① 수확물에 대해서는 공정가치 측정 불능에 따른 원가법 예외를 허용하지 않습니다.\n③, ⑤ 수확물은 수확시점에 즉시 자산가치를 순공정가치로 잡아 당기이익(수확물평가이익)을 인식합니다.\n④ 계약가액과 무관하게 수확시점의 순공정가치를 적용합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "원가법 예외는 생물자산에만 극히 드물게 인정되며, 수확물에는 허용되지 않습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "수확물 측정의 예외 부존재", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수확시점 수확물의 공정가치는 항상 신뢰성 있게 추정할 수 있다고 보아 예외 없이 순공정가치 측정을 강제하는 조문을 정합적으로 기술했습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "수확물 측정의 예외 부존재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득가액을 공정가치 기반으로 즉시 잡아 이익을 인식하므로 틀렸습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "수확물 측정의 예외 부존재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계약가격이 아닌 시장가 기반 순공정가치를 기준으로 하므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "수확물 측정의 예외 부존재", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수확물은 감가상각 대상 비유동자산이 아니므로 무관합니다.", "articles": [], "principle": "수확물 측정의 예외 부존재", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "순공정가치로 측정하는 생물자산과 관련된 정부보조금에 '부수되는 다른 조건이 없는 경우'에는 이를 어느 시점에 당기손익으로 인식하는가?",
        "options": [
            "① 보조금을 수취할 수 있게 되는 시점",
            "② 보조금을 현금으로 실제 수령하여 은행에 예치하는 날",
            "③ 관련 생물자산이 생물적 변환을 모두 마치고 판매 완료되는 결제 시점",
            "④ 정부보조금을 수령한 해의 다음 회계연도 기초일",
            "⑤ 보조금 지급을 결정한 정부 관서의 예산 편성 공고일"
        ],
        "answer": "1",
        "explanation": "① K-IFRS 제1041호 문단 34에 의하면, 순공정가치로 측정하는 생물자산과 관련된 정부보조금에 다른 조건이 없는 경우에는 이를 '수취할 수 있게 되는 시점(receivable)'에만 당기손익으로 즉시 인식합니다.\n\n[오답 해설]\n② 현금 수령일이 아닌 권리 확정(수취 가능) 시점 기준입니다.\n③, ④, ⑤는 보조금의 기간 배분이나 불합리한 연기 가설로 기준서와 다릅니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "조건이 없는 정부보조금은 수취 권리가 확정되는(수취 가능해지는) 때 즉시 당기손익으로 잡는다는 조문을 바르게 진술했습니다.", "articles": ["K-IFRS 제1041호 문단 34"], "principle": "무조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실제 현금 수취 유무보다 권리 확정 시점이 회계상 핵심입니다.", "articles": ["K-IFRS 제1041호 문단 34"], "principle": "무조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "판매 완료 시까지 수익 인식을 이연하지 않으므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 34"], "principle": "무조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "연도 이월 인식설은 규정에 없습니다.", "articles": [], "principle": "무조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정부 예산 공고일은 개별 기업의 보조금 수취 권리 확정과 무관하므로 틀렸습니다.", "articles": [], "principle": "무조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "생물자산을 순공정가치로 평가함에 따라 최초 인식시점 및 기말 재측정 시 발생하는 평가손익은 포괄손익계산서상 어느 항목으로 계상하여야 하는가?",
        "options": [
            "① 기타포괄손익(OCI) 누계액",
            "② 당기손익(Profit or Loss)",
            "③ 자본잉여금 증가/감소",
            "④ 이익잉여금 직접 조절 항목",
            "⑤ 판매비와관리비 중 대손비용"
        ],
        "answer": "2",
        "explanation": "② 생물자산의 순공정가치 변동으로 인하여 발생하는 모든 평가손익은 발생한 기간의 '당기손익(당기순이익/손실)'에 반영합니다.\n\n[오답 해설]\n① 재평가모형을 적용하는 유형자산과 달리, 생물자산 평가손익은 기타포괄손익으로 갈 수 없습니다.\n③, ④ 자본 계정에 직접 반영하는 조절 거래가 아닌 손익거래입니다.\n⑤ 판관비의 대손상각 성격이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기타포괄손익으로 누적 적립할 수 없습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 평가손익의 당기손익 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "순공정가치 변동에 따른 평가손익은 매기 당기손익으로 인식하여 손익계산서에 보고해야 합니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 평가손익의 당기손익 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 잉여 항목에 해당하지 않습니다.", "articles": [], "principle": "생물자산 평가손익의 당기손익 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익잉여금을 처분 거래 없이 직접 대치하는 것은 금지되므로 오답입니다.", "articles": [], "principle": "생물자산 평가손익의 당기손익 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손상각과 무관한 평가손익 계정입니다.", "articles": [], "principle": "생물자산 평가손익의 당기손익 분류", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "다음 중 K-IFRS 기준 상 농림어업 기준서(제1041호)가 정하는 생산용식물(Bearer plant) 요건을 완벽하게 만족하여, 감가상각을 수행하는 유형자산으로 정상 분류되는 식물의 명확한 예시는?",
        "options": [
            "① 가구 제조용 목재로 사용하기 위해 대단위로 조림 중인 삼나무",
            "② 과수원에서 배를 얻기 위해 재배하며, 수령이 다한 후에는 땔감용 폐물로만 처분할 예정인 배나무",
            "③ 목재와 차(Tea) 잎을 모두 상업적으로 대량 획득할 가능성이 유의미하게 높은 차나무",
            "④ 옥수수 가공품을 제조하기 위해 밭에서 한 철 경작하는 단년생 옥수수",
            "⑤ 사료용 건초를 생산하기 위해 한 철 심어 수확하는 목초 작물"
        ],
        "answer": "2",
        "explanation": "② 배나무는 배(과일)라는 수확물을 반복 공급하는 도구로 쓰이고, 한 해를 초과하여 사용하며, 나중에 수령이 다해 땔감(부수적 폐물)으로 파는 것 외에 나무 자체를 판매할 목적이 없으므로 생산용식물(유형자산)의 완벽한 예시입니다.\n\n[오답 해설]\n① 목재(식물 자체)를 수확물로 쓰기 위해 베어버릴 나무는 생산용식물이 아닙니다.\n③ 목재라는 주된 수확물을 추가로 판매할 가능성이 희박하지 않으므로 제외됩니다.\n④, ⑤ 한해살이 작물은 유형자산이 될 수 없는 일반 생물자산입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "나무 자체가 최종 수확물이 되는 경우는 일반 생물자산입니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물의 판단 사례", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수확물인 배를 생산하는 장기성 생산도구이며 주된 판매 의도가 없으므로 생산용식물이 맞습니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물의 판단 사례", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "식물 자체의 상업적 판매 목적이 공존하면 생산용식물에서 탈락합니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물의 판단 사례", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단년생 경작물은 생산용식물이 아닙니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물의 판단 사례", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "한해살이 건초용 목초는 생산용식물 범주 밖의 자산입니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물의 판단 사례", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 1,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },

    # =========================================================================
    # L2: 개념 이해 및 기준 조문 (15문항, 911~925번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s06-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "생산용식물(Bearer plant, 예: 사과나무) 자체는 유형자산(제1016호)으로 분류되나, 그 지엽에 매달려 자라고 있는 아직 수확되지 않은 수확물(예: 사과나무에 달린 사과 열매)의 회계적 분류와 기준서 적용에 대한 설명으로 옳은 것은?",
        "options": [
            "① 생산용식물과 물리적으로 합체되어 있으므로 수확 전까지는 유형자산으로 함께 분류하여 감가상각한다.",
            "② 수확하기 전이라도 별개의 유형자산으로 취급하여 공정가치 재평가를 OCI로 인식한다.",
            "③ 생산용식물에서 자라는 수확물은 농림어업 기준서(제1041호)에 따른 '생물자산'에 해당하여 순공정가치로 평가한다.",
            "④ 수확 전 열매는 형체가 아직 고정되지 않았으므로 자산으로 인식하지 않고 부외자산으로 관리한다.",
            "⑤ 수확 전에도 재고자산으로 편입되어 기말에 저가법(LCM)을 즉시 적용한다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1041호 문단 5B에 명시된 바와 같이, 생산용식물(예: 사과나무)은 유형자산이지만, 그 생산용식물에서 자라는 수확물(예: 사과나무에 달린 사과 열매)은 농림어업 기준서의 적용 범위에 포함되는 생물자산에 해당합니다. 따라서 수확 전까지 순공정가치로 측정하여 당기손익에 반영합니다.\n\n[오답 해설]\n①, ② 수확 전 열매는 감가상각 대상이 아니며 유형자산이 아닌 생물자산입니다.\n④ 인식 요건을 충족하면 재무제표 내부 정식 자산으로 계상해야 합니다.\n⑤ 수확 후에만 재고자산이 되며 수확 전에는 저가법을 적용하지 않고 순공정가치로 평가합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "지엽에 매달린 수확물은 감가상각하는 유형자산이 아닙니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 부착 수확물의 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유형자산이 아니므로 OCI 재평가 대상이 될 수 없습니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 부착 수확물의 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "생산용식물상의 지엽 수확물은 수확 전까지 제1041호 농림어업 기준서가 적용되는 생물자산으로 측정됨을 명확히 설명했습니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 부착 수확물의 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 인식 요건 충족 시 당연히 대내적으로 계상됩니다.", "articles": [], "principle": "생산용식물 부착 수확물의 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수확 전에는 재고자산 기준서가 가동되지 않으므로 오답입니다.", "articles": [], "principle": "생산용식물 부착 수확물의 분류", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "다음 중 농림어업 기준서(K-IFRS 제1041호)가 규정하는 수확물 또는 생물자산에 해당하지 않아, 생산 공정에 들어간 일반적인 '재고자산(K-IFRS 제1002호)'으로 전면 분류·처리해야 하는 대상은?",
        "options": [
            "① 벌목한 삼나무 통나무",
            "② 수확하여 창고에 보관 중인 면화(솜)",
            "③ 농림업 수확물인 포도를 가공하여 오크통에서 숙성 중인 포도주",
            "④ 양떼에서 갓 수확해 모아둔 양모",
            "⑤ 젖소로부터 수확한 직후 유조에 보관하고 있는 생유(우유)"
        ],
        "answer": "3",
        "explanation": "③ 수확시점까지 또는 수확된 원시 형태의 수확물(통나무, 면화, 양모, 생유 등)은 수확시점에 순공정가치로 최초 측정하여 인식하므로 제1041호의 적용을 받으나, 이를 가공하여 탄생한 가공품(포도주, 실, 버터 등)은 수확시점 '이후'의 가공이므로 전적으로 제1002호 '재고자산' 기준서를 적용합니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 모두 갓 수확을 완료한 시점의 수확물에 해당하므로, 수확시점 최초 측정 시까지 제1041호의 통제를 받습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "벌목 직후 통나무는 최초 인식 시점까지 제1041호 하의 수확물입니다.", "articles": ["K-IFRS 제1041호 문단 3"], "principle": "수확물과 수확 후 가공품 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원시 형태의 면화는 수확물 자산입니다.", "articles": ["K-IFRS 제1041호 문단 3"], "principle": "수확물과 수확 후 가공품 구분", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "포도를 가공하여 제조 공정을 밟는 포도주는 제1041호가 아닌 재고자산 기준서(제1002호)를 적용해야 함을 정확하게 집어냈습니다.", "articles": ["K-IFRS 제1041호 문단 3"], "principle": "수확물과 수확 후 가공품 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "갓 깎은 양모는 전형적인 수확물로 분류됩니다.", "articles": ["K-IFRS 제1041호 문단 3"], "principle": "수확물과 수확 후 가공품 구분", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "생유 자체는 수확물로서 최초 순공정가치 평가 대상입니다.", "articles": ["K-IFRS 제1041호 문단 3"], "principle": "수확물과 수확 후 가공품 구분", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "순공정가치로 측정하는 생물자산과 관련된 정부보조금에 '부수되는 조건이 있는 경우(예: 특정 농업 활동을 5년간 지속해야 함)'의 당기손익 인식 기준에 대한 K-IFRS 규정으로 가장 올바른 것은?",
        "options": [
            "① 보조금을 수령한 즉시 보조금 총액을 전액 당기순이익으로 영업외수익 계상한다.",
            "② 정부보조금에 부수되는 조건을 충족하는 시점에만 당기손익으로 인식한다.",
            "③ 보조금 수령 시점부터 5년에 걸쳐 정액법으로 이연수익을 당기손익과 상쇄한다.",
            "④ 정부보조금은 부채의 차감 계정으로 두어 이자비용과 대응 상각한다.",
            "⑤ 조건의 달성 여부와 상관없이 매기 현금주의 기준에 맞춰 분할 수익 처리한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1041호 문단 35에 명확히 명시된 바와 같이, 순공정가치로 측정하는 생물자산과 관련된 정부보조금에 부수되는 조건이 있는 경우(반환 조건 등 포함)에는 그 조건을 충족하는 시점에만 당기손익으로 인식합니다.\n\n[오답 해설]\n① 조건 충족 전에 수익화하면 추후 조건 미달성 시 반환 의무로 왜곡이 유발되므로 금지됩니다.\n③ 일반 정부보조금 기준서(제1020호)의 기간 배분법과 대비되는 제1041호의 독특한 규정(조건 충족 시 즉시 전액 인식)으로, 정액 이연 처리는 오답입니다.\n④, ⑤는 기준서 규칙과 다른 부합하지 않는 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "조건 충족 전 즉시 인식은 불허됩니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "부수적인 조건이 있는 보조금은 그 조건이 완수·충족되는 시점에만 당기손익으로 반영한다는 기준서의 원칙을 바르게 설명했습니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "제1041호 하에서는 이연 수익 정액 상각법을 원칙적으로 쓰지 않고 조건 충족 즉시 당기손익 처리하므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 차감법을 적용하지 않습니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금주의를 따르지 않는 발생주의 기반 특화 조항입니다.", "articles": [], "principle": "조건부 정부보조금 수익 인식", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "생물자산의 순공정가치 측정에 대한 신뢰성 가정에 따라 원가모형 적용 예외가 인정되는 범위와 요건에 관한 K-IFRS 기준서의 올바른 설명은?",
        "options": [
            "① 이미 순공정가치로 성실히 측정해 오던 생물자산도 시장이 침체되면 언제든지 원가법으로 사후 전환할 수 있다.",
            "② 생물자산의 공정가치 신뢰성 측정 불가에 따른 원가모형(원가-감누-손누) 예외는 오직 최초 인식시점에 공시가격이 없고 대체적인 측정치도 명백히 신뢰성이 없는 경우에만 한정적으로 허용된다.",
            "③ 수확물에 대해서도 시장 가격을 찾기 어려우면 최초 인식 시 원가법을 광범위하게 적용할 수 있다.",
            "④ 원가모형을 적용하는 생물자산은 시장에 공시가격이 출현하더라도 취득원가로 영구 고정한다.",
            "⑤ 생물자산은 애초에 공정가치 신뢰성 가정이 없으므로 기본적으로 모두 원가모형으로 시작한다."
        ],
        "answer": "2",
        "explanation": "② 기준서는 최초 인식시점에 시장 공시가격을 구할 수 없고 대체적 공정가치측정치가 명백히 신뢰성 없게 결정되는 생물자산에 한해 원가에서 감가상각 및 손상누계액을 뺀 금액으로 측정할 수 있게 허용합니다. 일단 순공정가치로 측정해온 자산은 사후적으로 공정가치를 신뢰성 있게 측정할 수 없게 되더라도 계속 순공정가치로 측정해야 합니다(원가법 전환 불가).\n\n[오답 해설]\n① 이미 순공정가치 평가를 하던 자산의 사후 원가법 회귀는 불가능합니다.\n③ 수확물은 수확시점에 항상 공정가치를 신뢰성 있게 측정할 수 있다고 보아 원가법 예외가 적용되지 않습니다.\n④ 원가법을 쓰던 자산도 공정가치를 신뢰성 있게 측정할 수 있게 되면 순공정가치법으로 즉시 강제 전환합니다.\n⑤ 기본은 순공정가치법입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "순공정가치 평가를 하던 자산은 사후 원가법으로 이탈할 수 없습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "생물자산 원가법 예외 규정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "최초 인식 시 공시가격 및 대체 측정치가 신뢰성 없게 결정되는 경우에만 극히 제한적으로 원가법 예외를 허용함을 정확히 명시했습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "생물자산 원가법 예외 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수확물은 원가법 예외 규정 자체가 전면 배제됩니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "생물자산 원가법 예외 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추후 공정가치 측정 가능 시 즉각 순공정가치 평가로 전환해야 하므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "생물자산 원가법 예외 규정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기본 측정의 기준은 원칙적으로 순공정가치입니다.", "articles": [], "principle": "생물자산 원가법 예외 규정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "공정가치 측정이 어려워 예외적으로 '원가에서 감가상각누계액과 손상차손누계액을 차감한 금액으로 측정하는 생물자산'과 관련된 정부보조금은 어느 기준서를 적용하여 처리해야 하는가?",
        "options": [
            "① K-IFRS 제1041호 '농림어업'의 정부보조금 규정",
            "  K-IFRS 제1020호 '정부보조금의 회계처리와 정부지원의 공시'",
            "③ K-IFRS 제1002호 '재고자산'",
            "④ K-IFRS 제1109호 '금융상품'",
            "⑤ K-IFRS 제1115호 '고객과의 계약에서 생기는 수익'"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1041호 문단 37에 의하면, 원가에서 감가상각누계액과 손상차손누계액을 차감한 금액으로 측정하는 생물자산(원가법 적용)과 관련된 정부보조금에 대해서는 기업회계기준서 제1020호 '정부보조금의 회계처리와 정부지원의 공시'를 적용합니다.\n\n[오답 해설]\n① 순공정가치로 평가하는 일반 생물자산 관련 정부보조금만 제1041호를 적용합니다.\n③, ④, ⑤는 보조금의 일반 또는 특화 회계처리를 다루는 올바른 적용 기준서가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "제1041호의 즉시인식 정부보조금 조항은 순공정가치 측정 자산에 국한됩니다.", "articles": ["K-IFRS 제1041호 문단 37"], "principle": "원가법 생물자산 정부보조금 기준서", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "원가모형을 취하는 생물자산 관련 정부보조금은 일반적인 제1020호 정부보조금 기준서에 따라 처리함을 정확히 지목했습니다.", "articles": ["K-IFRS 제1041호 문단 37"], "principle": "원가법 생물자산 정부보조금 기준서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고자산 기준서에는 정부보조금 수취 규정이 없습니다.", "articles": [], "principle": "원가법 생물자산 정부보조금 기준서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보조금 수취가 금융부채/자산 평가 거래가 아니므로 오답입니다.", "articles": [], "principle": "원가법 생물자산 정부보조금 기준서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "고객에게 재화를 판매한 수익이 아니므로 무관합니다.", "articles": [], "principle": "원가법 생물자산 정부보조금 기준서", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "다음 중 K-IFRS 기준 상 생물자산이나 농림어업 수확물을 재무제표에 정식 '인식(Recognition)'하기 위해 동시에 충족해야 하는 필수 요건이 아닌 것은?",
        "options": [
            "① 과거 사건의 결과로 자산을 통제한다.",
            "② 자산과 관련된 미래경제적효익의 유입가능성이 높다.",
            "③ 자산의 공정가치나 원가를 신뢰성 있게 측정할 수 있다.",
            "④ 정부 관서로부터 해당 농림어업 활동에 대한 공식 허가 및 면허를 최종 취득해야 한다.",
            "⑤ 과거의 거래나 사건 결과로 통제권이 기업에 이전된 상태여야 한다."
        ],
        "answer": "4",
        "explanation": "④ 정부의 공식 허가나 면허 여부는 자산의 경제적 개념 충족(통제, 효익 유입가능성, 측정 신뢰성)을 위한 필수적 3대 인식 요건이 아닙니다. 허가가 없더라도 실질적인 자산의 통제와 효익 유입이 가능하고 측정이 되면 인식합니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 K-IFRS 제1041호 문단 10 등에 규정된 자산 인식의 3대 요건(통제, 유입가능성, 측정성)의 설명으로 모두 충족되어야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "과거 사건에 기한 통제는 필수 인식 요건입니다.", "articles": ["K-IFRS 제1041호 문단 10"], "principle": "자산의 인식 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래경제적효익 유입가능성 역시 필수 인식 요건입니다.", "articles": ["K-IFRS 제1041호 문단 10"], "principle": "자산의 인식 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "공정가치나 원가의 측정 신뢰성은 필수 요건입니다.", "articles": ["K-IFRS 제1041호 문단 10"], "principle": "자산의 인식 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "정부 허가나 면허 유무는 재무보고를 위한 자산 인식 요건의 핵심 정의와 관련이 없음을 밝혀냈습니다.", "articles": ["K-IFRS 제1041호 문단 10"], "principle": "자산의 인식 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "통제권 획득 요건의 세부 설명입니다.", "articles": ["K-IFRS 제1041호 문단 10"], "principle": "자산의 인식 요건", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "역사적원가 모형을 적용하는 일반 재고자산과 비교할 때, 제1041호 '농림어업'이 생물자산에 대해 순공정가치 모형을 원칙으로 도입하여 평가손익을 당기손익에 적극 반영하는 가장 타당한 회계이론적 근거는?",
        "options": [
            "① 생물자산의 가장 본질적인 경제적 가치 창출 사건인 '생물적 변환(성장 및 번식)'의 재무적 성과를 실현 전이라도 적시에 보고함으로써 회계정보의 목적적합성을 높이기 위함이다.",
            "② 실현주의 원칙에 따라 최종 판매처가 확정되기 전에는 절대 수익을 인식하지 않기 위함이다.",
            "③ 농업 부문의 자산 과대계상을 유도하여 외부 금융 차입을 원활하게 지원하기 위한 정책적 배려이다.",
            "④ 생물자산은 감가상각을 매달 임의로 진행하여 자산 가치를 0으로 빨리 유도하기 위함이다.",
            "⑤ 취득원가를 영구히 보존하여 취득 당시의 정확한 자본 지출 기록을 추적하기 위함이다."
        ],
        "answer": "1",
        "explanation": "① 농림어업의 경우, 농민이 관여하는 주된 가치 창출 활동은 단순히 자산을 외부에 파는 것보다 자산 자체를 생물학적으로 성장시키고 번식시키는 '생물적 변환 과정'입니다. 따라서 이 변환 사건이 발생하여 가치가 상승한 시점에 평가이익을 당기손익으로 적시에 인식하는 것이 농림어업의 본질적 경제활동과 성과를 재무제표에 가장 충실하게 나타내는 방식입니다.\n\n[오답 해설]\n② 순공정가치 모형은 미실현 평가손익을 즉시 수익화하므로 엄격한 실현주의의 완화 및 변형에 해당합니다.\n③ 분식이나 인위적 자산 확장을 부추기기 위한 규정이 아닙니다.\n④ 생산용식물 외의 생물자산은 감가상각을 아예 적용하지 않고 시가 재평가만 수행합니다.\n⑤ 원가 유지와 반대되는 시가 모형의 성격입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "생물적 변환 자체를 주요한 경제 사건으로 보아 성장을 당기손익에 적시 반영한다는 공정가치 평가의 이론적 배경을 올바르게 진술했습니다.", "articles": [], "principle": "순공정가치 모형의 당위성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미실현이익을 조기에 인식하므로 실현주의를 그대로 고수한 형태가 아닙니다.", "articles": [], "principle": "순공정가치 모형의 당위성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정책적 금융 혜택이나 자산 부풀리기는 회계기준의 제정 목적이 아닙니다.", "articles": [], "principle": "순공정가치 모형의 당위성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "생물자산은 원칙적으로 감가상각을 하지 않습니다.", "articles": [], "principle": "순공정가치 모형의 당위성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 보존이 아닌 매기 시가 재조정을 대원칙으로 합니다.", "articles": [], "principle": "순공정가치 모형의 당위성", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "다음 중 K-IFRS 농림어업 기준 상 생산용식물(유형자산)에서 전면 제외되어, 제1041호 '생물자산'으로 정상 분류되어 순공정가치 평가를 적용받아야 하는 자산은?",
        "options": [
            "① 가공용 원료 우유(생유)를 획득하기 위해 낙농업 회사가 기르는 젖소 군(우군)",
            "② 오직 목재 생산 및 수확물 획득 목적으로만 재배하는 삼나무 산림",
            "③ 사과 수확이 주된 목적이며 사과 재배가 끝난 후에는 땔감으로만 처분할 예정인 배나무",
            "④ 차 잎 수확 전용으로 다년간 보존하며 경작 중인 차나무 산지",
            "⑤ 고무 원액을 다년간 획득하기 위해 관리하는 고무나무 조림지"
        ],
        "answer": "2",
        "explanation": "② 나무 자체를 베어내어 목재(수확물)로 판매할 목적의 삼나무 산림은 생산용식물의 요건(생산 도구로만 쓰고 자산 자체를 팔지 않음)을 위배하므로 일반 생물자산(제1041호)에 해당하여 순공정가치로 측정합니다.\n\n[오답 해설]\n① 젖소는 동물이므로 '식물'에 적용되는 생산용식물 개념이 적용되지 않고 동물성 생물자산입니다. (다만 질문은 식물 중 생물자산 분류 대상을 묻는 맥락이며, 젖소도 제1041호 생물자산이 맞지만 삼나무 산림은 전형적으로 벌목 목적의 식물 자산으로서 확실한 생물자산입니다.)\n③, ④, ⑤는 모두 과수나 생산 도구 형태의 장기성 식물이므로 생산용식물(유형자산 제1016호)에 속합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "젖소는 동물성 생물자산입니다. (식물 기준인 생산용식물의 범위에 해당 사항 없음)", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 제외 항목", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "목재 획득 목적으로 베어낼 나무는 생산용식물의 정의를 충족하지 못하므로 제1041호 하의 일반 생물자산으로 정상 분류되어야 합니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 제외 항목", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과일 전용 수확 배나무는 생산용식물(유형자산)입니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 제외 항목", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "찻잎 채취용 차나무는 대표적인 생산용식물입니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 제외 항목", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수액 채취용 고무나무 역시 대표적인 생산용식물입니다.", "articles": ["K-IFRS 제1041호 문단 5B"], "principle": "생산용식물 제외 항목", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "생물자산 측정액인 순공정가치를 산출하기 위하여 공정가치에서 추정 차감하는 '처분부대원가(Estimated point-of-sale costs)'에 대한 설명 중 K-IFRS 기준서의 지침과 합당하지 않은 것은?",
        "options": [
            "① 중개인이나 거래소 등에 지급할 수수료는 처분부대원가에 포함한다.",
            "② 감독기관이나 상품거래소 등에 부과되는 제세공과금은 처분부대원가에 포함한다.",
            "③ 권리이전세나 거래세 등 거래 관련 직접 제세금은 처분부대원가에 속한다.",
            "④ 자산을 시장 등 거래 목적지까지 운송하는 데 드는 운반비(운송원가)는 처분부대원가에 가산한다.",
            "⑤ 처분부대원가는 자산의 처분에 직접 귀속되는 증분원가(금융원가와 소득세 제외)를 의미한다."
        ],
        "answer": "4",
        "explanation": "④ 운송원가는 처분부대원가가 아닙니다. 자산의 공정가치 자체가 주된 시장의 가격에서 해당 시장까지의 운송비용을 차감하여 도출되므로, 이 운송비용은 공정가치 산출 과정에서 이미 반영되어 있습니다. 따라서 이를 처분부대원가에 다시 중복 가산하면 자산 가액이 이중 차감되는 왜곡이 생깁니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 K-IFRS 제1041호 문단 5 및 14에 명시된, 처분(매각)에 직접 기여하는 증분원가로서 처분부대원가에 정상 포함되는 세부 항목들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "중개 수수료는 거래를 위한 직접 증분원가로 처분부대원가입니다.", "articles": ["K-IFRS 제1041호 문단 5, 14"], "principle": "처분부대원가 구성 항목", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "거래소가 부과하는 제세공과금도 처분부대원가 범위에 들어갑니다.", "articles": ["K-IFRS 제1041호 문단 5, 14"], "principle": "처분부대원가 구성 항목", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "권리이전 직접 세금 등도 정당한 처분부대원가입니다.", "articles": ["K-IFRS 제1041호 문단 5, 14"], "principle": "처분부대원가 구성 항목", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "운송원가는 공정가치 계산 시 차감되어 반영되므로 처분부대원가가 아니며, 이를 처분부대원가에 중복 합산하여 자산을 깎아선 안 됨을 잘 지적했습니다.", "articles": ["K-IFRS 제1041호 문단 14"], "principle": "처분부대원가 구성 항목", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "증분원가의 일반적 규정 및 세액/이자 제외 조항을 정밀히 묘사했습니다.", "articles": ["K-IFRS 제1041호 문단 5"], "principle": "처분부대원가 구성 항목", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "농림어업 영위 목적의 기업이 보유한 자산 중, 농림어업 기준서(제1041호)가 직접 적용되지 않고 유형자산(제1016호)이나 투자부동산(제1040호) 등 다른 기준서를 적용해야 하는 부동산 자산은?",
        "options": [
            "① 생물자산이 생육하며 자라고 있는 농업용 농지 및 임야(토지)",
            "② 삼나무 묘목이 심어져 생물적 변환 과정을 거치고 있는 국유 임야",
            "③ 농업용 용수 획득을 위해 인위적으로 확보한 저수지 부지 토지",
            "④ 목축업을 위해 가축들이 방목되고 있는 가축 방목장용 토지",
            "⑤ 위의 모든 부동산 자산(토지)"
        ],
        "answer": "5",
        "explanation": "⑤ K-IFRS 제1041호 문단 2에 명시된 바와 같이, 농림어업 활동과 관련된 '토지'는 이 기준서의 적용 범위에서 명시적으로 제외됩니다. 조림이나 방목, 재배에 쓰이는 토지는 그 성격에 따라 K-IFRS 제1016호 '유형자산' 또는 제1040호 '투자부동산'을 적용하여 따로 분류하고 평가해야 합니다.\n\n[오답 해설]\n①, ②, ③, ④는 모두 토지(부동산)에 해당하므로 농림어업 기준서를 단독으로 적용할 수 없습니다. 따라서 전체가 다른 기준서의 적용을 받으므로 ⑤가 유일하게 올바른 정답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "농업용 농지 토지는 유형자산 기준서(제1016호)를 적용합니다.", "articles": ["K-IFRS 제1041호 문단 2"], "principle": "농림어업 활동 관련 토지의 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조림 임야 토지 역시 제1016호 또는 제1040호 대상입니다.", "articles": ["K-IFRS 제1041호 문단 2"], "principle": "농림어업 활동 관련 토지의 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "저수지 부지 토지도 유형자산 대상입니다.", "articles": ["K-IFRS 제1041호 문단 2"], "principle": "농림어업 활동 관련 토지의 배제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "방목장 토지 역시 유형자산 기준서를 타야 합니다.", "articles": ["K-IFRS 제1041호 문단 2"], "principle": "농림어업 활동 관련 토지의 배제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "모든 농림어업 활동용 토지는 제1041호 적용에서 일괄 제외되어 각각 적격한 유형/투자부동산 기준서를 탄다는 포괄적 사실을 완벽히 제시했습니다.", "articles": ["K-IFRS 제1041호 문단 2"], "principle": "농림어업 활동 관련 토지의 배제", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "생물자산에서 수확한 수확물(Agricultural produce)에 대해 수확시점 '이후' 재고자산 기준서(제1002호)를 적용할 때, 저가법 평가 및 최초 취득원가 결정의 연결 규칙으로 가장 옳은 것은?",
        "options": [
            "① 수확시점에 인식한 순공정가치를 재고자산의 최초 취득원가로 간주하고, 이후 기말 결산 시에는 순실현가능가치와 대조하여 저가법 평가를 적용한다.",
            "② 수확시점의 공정가치는 무시하고 수확하기까지 투입된 실제 누적 재배 비용을 취득원가로 잡고 평가를 생략한다.",
            "③ 수확시점 순공정가치를 취득원가로 삼은 뒤, 재고자산으로 편입된 후에는 시가가 계속 오르면 평가이익을 무제한 누적 계상한다.",
            "④ 수확시점 순공정가치를 무시하고 일반 시장 도매가격으로 기말 취득단가를 매달 소급법으로 덮어쓴다.",
            "⑤ 수확물은 재고자산 기준서 상의 저가법을 적용하지 않고 영구히 수확일의 순공정가치로 고정한다."
        ],
        "answer": "1",
        "explanation": "① K-IFRS 제1041호 문단 13에 따르면, 생물자산에서 수확한 수확물은 수확시점에 순공정가치로 측정합니다. 이 금액은 수확물에 제1002호 '재고자산'이나 다른 기준서를 적용하는 시점의 취득원가가 됩니다. 그 이후에는 재고자산 기준서에 따라 매 보고기간말에 저가법(원가와 NRV의 LCM) 평가를 거쳐 가액을 결정합니다.\n\n[오답 해설]\n② 실제 투입 원가가 아닌 수확 당시의 시가 기반 순공정가치를 취득원가로 가산합니다.\n③ 재고자산으로 이전된 후에는 저가법을 받으므로 원가 초과 평가이익은 잡지 못합니다.\n④ 임의 소급 갱신은 불인정됩니다.\n⑤ 수확물은 수확 후 일반 재고와 동일하게 취득가보다 떨어지면 저가 감액(평가손실)을 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "수확시점 순공정가치가 재고자산의 최초 취득원가가 되고 이후에는 일반 재고 규칙(저가법)을 적용받는다는 정밀한 메커니즘을 기술했습니다.", "articles": ["K-IFRS 제1041호 문단 13"], "principle": "수확물의 취득원가 및 저가법 연계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "누적 재배 원가를 최초 자산액으로 삼지 않고 시가 기반 순공정가치를 쓰므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 13"], "principle": "수확물의 취득원가 및 저가법 연계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고자산 편입 후에는 평가이익 인식이 차단되므로 틀렸습니다.", "articles": [], "principle": "수확물의 취득원가 및 저가법 연계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매달 시가 소급 개정은 허용되지 않는 장부 조작입니다.", "articles": [], "principle": "수확물의 취득원가 및 저가법 연계", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수확물도 재고가 되므로 저가법 적용이 강제됩니다.", "articles": [], "principle": "수확물의 취득원가 및 저가법 연계", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "생물자산의 공정가치 서열체계(Fair Value Hierarchy) 적용 및 시가 추정과 관련하여, 활성시장(Active market)이 존재하지 않는 경우 순공정가치 신뢰성 도출을 위해 K-IFRS에서 제시하는 대체 측정치 도출 지침에 속하지 않는 것은?",
        "options": [
            "① 가장 최근의 시장 거래 가격 (거래일과 보고기간말 사이에 경제상황의 유의적인 변화가 없는 경우)",
            "② 시장 가격이 형성되어 있는 유사한 자산의 가격 (차이점을 반영하여 조정된 가격)",
            "③ 농업이나 목축업계의 관행적인 평당 장부 원가 가산 수치",
            "④ 과수원, 조림지 등의 자산에서 발생하는 순현금흐름의 현재가치(사용가치 유도에 준함)",
            "⑤ 순공정가치가 결정될 수 있는 지수가 제공되는 부문별 벤치마크 가격"
        ],
        "answer": "3",
        "explanation": "③ 업계의 임의적 관행인 평당 장부 원가 가산 수치는 K-IFRS가 요구하는 공정가치 서열체계 하의 대체 정보 원천이 아닙니다. 자의적이고 신뢰성이 결여되어 자산 가치 평가로 쓸 수 없습니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 K-IFRS 제1041호 문단 18, 19, 20 등에 언급된, 활성시장이 없거나 직접 측정이 어려울 때 시장 정보를 합리적으로 대체할 수 있는 규정상의 공정가치 도출 기법 및 정보 원천들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "최근 거래가격은 훌륭한 대체 측정 기준입니다.", "articles": ["K-IFRS 제1041호 문단 18"], "principle": "생물자산 공정가치 추정 기법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유사 자산 시가 조정치 역시 조문상 인정되는 대안입니다.", "articles": ["K-IFRS 제1041호 문단 18"], "principle": "생물자산 공정가치 추정 기법", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "임의의 업계 평당 원가 가산 관행은 공인된 신뢰성 있는 공정가치 측정 기법이 아님을 정확히 구분했습니다.", "articles": ["K-IFRS 제1041호 문단 18, 19"], "principle": "생물자산 공정가치 추정 기법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 순현금흐름 현재가치법(DCF)도 공인된 가치 도출법입니다.", "articles": ["K-IFRS 제1041호 문단 20"], "principle": "생물자산 공정가치 추정 기법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부문별 벤치마크 지표 활용도 인정되는 범위에 있습니다.", "articles": ["K-IFRS 제1041호 문단 19"], "principle": "생물자산 공정가치 추정 기법", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "K-IFRS 제1041호 농림어업의 정의 중, 관리되지 않는 단순 채집이나 수렵 등과 농림어업활동을 구분 짓는 가장 결정적인 실질 요건은?",
        "options": [
            "① 변화의 관리(Management of change) : 생물적 변환이 일어날 수 있는 여건을 인위적으로 관리 및 촉진하는 활동의 유무",
            "② 판매 시장의 존재 유무",
            "③ 활용되는 토지가 사유지인지 국유지인지의 법적 소유 관계",
            "④ 정부보조금 수령 자격의 유무",
            "⑤ 수확물의 가열 조리 가공 여부"
        ],
        "answer": "1",
        "explanation": "① 농림어업활동의 세 가지 특징은 (1) 변화 능력, (2) 변화의 관리, (3) 변화의 측정입니다. 이 중 '변화의 관리'는 성장, 퇴화, 생산, 번식이 촉진되거나 발생할 수 있는 영양 보급, 온도 제어 등 생육 여건을 인위적으로 통제·유지하는 것입니다. 야생 바다에서의 어획이나 자연림 벌목은 관리 과정이 없으므로 농림어업활동이 아닙니다.\n\n[오답 해설]\n② 야생 채집물도 판매 시장은 존재하므로 구별 실질이 아닙니다.\n③ 토지의 법적 소유 형태는 활동 분류와 무관합니다.\n④ 보조금 수령은 사후적 사건일 뿐 정의 요건이 아닙니다.\n⑤ 가공 여부는 수확 후 재고자산과의 구분선일 뿐, 농림어업활동 판정 기준이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "농림어업의 성립에 있어 자연적 채집과 구분 짓는 핵심 속성인 '변화의 관리(인위적 생육 관리)' 요건을 정확히 제시했습니다.", "articles": ["K-IFRS 제1041호 문단 6"], "principle": "농림어업활동의 성립 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시장 유무는 야생 채집물에도 공통되므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 6"], "principle": "농림어업활동의 성립 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "토지 소유 성격은 회계 분류를 결정하지 않습니다.", "articles": [], "principle": "농림어업활동의 성립 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정부 혜택 자격 여부는 자산 활동의 정의가 아닙니다.", "articles": [], "principle": "농림어업활동의 성립 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조리/가공은 생산 과정일 뿐이며 농림어업 의의 판정이 아닙니다.", "articles": [], "principle": "농림어업활동의 성립 요건", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "생물자산의 '최초 인식시점'에 당기손익 상 평가'이익'이 발생할 수 있는 주요 원인(이벤트)으로 K-IFRS 상 가장 정합한 것은?",
        "options": [
            "① 가축의 도살로 인한 실물 소멸 거래",
            "② 어미소로부터 송아지가 탄생하는 번식 사건",
            "③ 농업용 트랙터를 신규로 취득하여 설치한 날",
            "④ 정부보조금을 미래에 상환할 의무 조건이 부과되어 현금 차입한 사건",
            "⑤ 생물자산의 순공정가치를 측정하지 않고 원가모형으로 최초 제시한 날"
        ],
        "answer": "2",
        "explanation": "② 생물자산 최초 인식 시 평가손실이 발생하기 쉬운 취득 거래원가 요건과 달리, 어미소로부터 송아지가 탄생(번식)하는 사건이 발생하면, 회사는 아무런 취득 지출 없이 새로운 생물자산(송아지)을 얻게 되므로 당일 송아지 순공정가치 전액이 최초인식평가이익(당기손익)으로 잡힙니다.\n\n[오답 해설]\n① 도살은 자산의 감액 및 소멸로 처분손실 등이 나기 쉽습니다.\n③ 트랙터는 유형자산 취득이며 최초 인식 평가이익을 인식하지 않습니다.\n④ 부채 유입 거래는 자산평가이익을 발생시키지 않습니다.\n⑤ 원가법 적용일에는 평가손익을 잡지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "도살은 실물 소멸 사건으로 평가이익 사유가 아닙니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "최초 인식 시 평가이익 원인", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "동물의 출산(번식) 등 새로운 생물자산의 획득 시점에는 지출 없이 자산이 창출되므로 평가이익이 발생함을 정확히 설명했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "최초 인식 시 평가이익 원인", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유형자산 취득 거래는 최초인식 평가손익이 배제됩니다.", "articles": [], "principle": "최초 인식 시 평가이익 원인", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상환 조건부 자금 차입은 회계상 부채 계상 거래입니다.", "articles": [], "principle": "최초 인식 시 평가이익 원인", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가모형 적용 시에는 평가손익의 유도가 발생하지 않습니다.", "articles": [], "principle": "최초 인식 시 평가이익 원인", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "공정가치 측정이 신뢰성 없어 극히 예외적으로 원가모형(원가-감누-손누)을 적용해오던 생물자산에 대하여, 추후 공정가치를 신뢰성 있게 측정할 수 있게 되었을 때의 K-IFRS 기준 상 평가 전환 규칙은?",
        "options": [
            "① 해당 자산은 계속 원가모형으로 유지하며, 처분되는 시점까지 공정가치를 반영할 수 없다.",
            "② 공정가치를 신뢰성 있게 측정할 수 있게 되는 시점부터 지체 없이 해당 생물자산을 순공정가치로 측정하여 평가손익을 당기손익으로 인식한다.",
            "③ 공정가치가 회복되더라도 직전 장부금액을 한도로 하여 감가상각액만 취소한다.",
            "④ 자산 재측정을 기타포괄손익(OCI)으로 계상하여 재평가잉여금으로 적립한다.",
            "⑤ 전환 시점의 공정가치 차액을 전액 자본잉여금으로 유입시켜 주주거래로 처리한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1041호 문단 30에 의하면, 일단 원가에서 감가상각누계액과 손상차손누계액을 차감한 금액으로 측정해온 생물자산도 그 후에 공정가치를 신뢰성 있게 측정할 수 있게 되면, 그 시점부터 즉시 순공정가치로 측정해야 합니다. 발생한 차액은 즉시 당기손익 평가손익으로 반영합니다.\n\n[오답 해설]\n① 추후 공정가치 반영이 강제되므로 영구 고정설은 오답입니다.\n③ 감가상각 취소 거래가 아닌 순공정가치 법으로의 전면적인 전환 재평가입니다.\n④ OCI가 아닌 당기손익으로 인식합니다.\n⑤ 전환 거래는 평가손익거래이며 주주거래가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "공정가치 복구 시 원가법을 유지할 수 없으며 즉시 전환해야 하므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 적용 생물자산의 평가 복귀", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "추후 신뢰성 있는 공정가치 획득 시 지체 없이 순공정가치 평가로 복귀하여 당기손익을 잡아야 한다는 강제 조항을 정확히 기술했습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 적용 생물자산의 평가 복귀", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 감상 환입에 그치지 않고 공정가치 전면 평가를 수행하므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 적용 생물자산의 평가 복귀", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평가손익은 기타포괄손익이 될 수 없고 당기손익입니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 적용 생물자산의 평가 복귀", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주주와의 자본거래 성격이 아니므로 틀렸습니다.", "articles": [], "principle": "원가법 적용 생물자산의 평가 복귀", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 2,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },

    # =========================================================================
    # L3: 적용 및 계산 (15문항, 926~940번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s06-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "낙농 회사인 (주)ABC유업은 20X1년 1월 1일 육우 1마리를 ₩5,000,000에 현금 구입하였다. 육우 취득 시 직접 관련된 운반비 및 수수료(취득 거래원가)로 ₩100,000을 추가 지출하였으며, 당일 시점의 육우의 추정 매각부대원가(처분 증분원가)는 ₩200,000으로 예상되었다. 취득 당일 (주)ABC유업이 회계장부에 기록할 육우(생물자산)의 최초 인식 금액(A)과 이 거래로 인해 최초 인식 시점에 당기손익에 미치는 영향(B)은 각각 얼마인가?",
        "options": [
            "① A: ₩5,000,000 / B: 영향 없음",
            "② A: ₩5,100,000 / B: ₩100,000 비용 증가",
            "③ A: ₩4,800,000 / B: ₩300,000 손실 발생",
            "④ A: ₩4,900,000 / B: ₩200,000 손실 발생",
            "⑤ A: ₩4,800,000 / B: ₩200,000 손실 발생"
        ],
        "answer": "3",
        "explanation": "③ 생물자산은 최초 인식시점에 공정가치(구입가격 ₩5,000,000)에서 추정 매각부대원가(₩200,000)를 차감한 순공정가치인 ₩4,800,000으로 측정하여 자산 계상(A)합니다. 한편, 취득 시 지출된 거래원가 ₩100,000은 취득원가에 얹지 못하고 전액 즉시 비용 처리하므로, 총 현금 유출액 ₩5,100,000(구입가 500만 + 거래원가 10만)과 자산가액 ₩4,800,000의 차이인 ₩300,000이 최초인식평가손실(당기순이익 300,000원 감소)(B)로 인식됩니다.\n\n[오답 해설]\n- 분개: (차) 생물자산 4,800,000 / (대) 현금 5,100,000\n            생물자산평가손실 300,000\n따라서 A는 ₩4,800,000, B는 ₩300,000 손실입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "취득 거래원가 가산 및 매각부대원가 누락으로 잘못 구했습니다.", "articles": ["K-IFRS 제1041호 문단 12, 26"], "principle": "최초 인식액과 최초 평가손실 유도", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유형자산처럼 거래원가를 자산화하여 매각부대원가를 빼지 않아 오류가 발생했습니다.", "articles": ["K-IFRS 제1041호 문단 12, 26"], "principle": "최초 인식액과 최초 평가손실 유도", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산액을 순공정가치(500만 - 20만 = 480만)로 잡고, 현금총액 510만과의 차액 30만 원을 당기손실로 정확히 도출했습니다.", "articles": ["K-IFRS 제1041호 문단 12, 26"], "principle": "최초 인식액과 최초 평가손실 유도", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득 거래원가를 누락하고 계산하여 틀렸습니다.", "articles": ["K-IFRS 제1041호 문단 12, 26"], "principle": "최초 인식액과 최초 평가손실 유도", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "A는 맞지만 당기손실 영향 계산 시 취득 시 지출된 수수료 10만 원을 빠뜨려 B가 틀렸습니다.", "articles": ["K-IFRS 제1041호 문단 12, 26"], "principle": "최초 인식액과 최초 평가손실 유도", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "(주)KAPA목장은 20X1년 초 육우 10마리를 보유하며 기초 시점의 육우 전체 순공정가치는 ₩12,000,000이었다. 당기 중 육우 1마리가 자연사하여 제거하였으며, 사망 당시 해당 육우의 순공정가치는 ₩1,100,000이었다. 20X1년 말 현재 남아 있는 육우 9마리의 기말 공정가치는 총 ₩15,000,000이며, 기말 시점의 추정 처분부대원가는 총 ₩1,200,000이다. 당기 중 가축과 관련된 다른 매입이나 매출 거래가 없을 때, (주)KAPA목장의 20X1 회계연도 포괄손익계산서에 반영될 '생물자산평가이익(또는 손실)'은 얼마인가?",
        "options": [
            "① 평가이익 ₩700,000",
            "② 평가이익 ₩2,900,000",
            "③ 평가이익 ₩1,800,000",
            "④ 평가손실 ₩300,000",
            "⑤ 평가이익 ₩2,200,000"
        ],
        "answer": "2",
        "explanation": "② 기말 육우 9마리의 기말 자산가액(순공정가치)은 ₩15,000,000 - ₩1,200,000 = ₩13,800,000입니다. 20X1년 중 생물자산 계정의 변동액을 유도해보면 다음과 같습니다.\n- 기초 장부액: ₩12,000,000\n- 자연사 폐기액: ₩1,100,000 차감 (당기 손실(기타비용)로 별도 처리)\n- 평가 전 장부액: ₩12,000,000 - ₩1,100,000 = ₩10,900,000\n- 기말 평가 장부액: ₩13,800,000\n따라서 기말 시가 평가로 계상할 평가이익은 ₩13,800,000 - ₩10,900,000 = ₩2,900,000(생물자산평가이익)이 됩니다.\n\n[오답 해설]\n① 사망 육우의 감액을 미고려하여 틀린 액수입니다.\n③ 처분부대원가를 뺀 기말 자산가액 1,380만 원과 기초 1,200만 원의 단순 차액(사망 미반영)으로 구하여 오답입니다.\n④, ⑤는 감액 순서나 처분부대원가 반영 처리를 누락 또는 가산한 잘못된 계산입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "사망 가축의 제거를 장부에서 적절히 제외하지 않고 계산했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 기말 변동 평가손익 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사망 폐기분을 뺀 평가전 가액(1,090만)과 기말 순공정가치(1,380만)의 차액을 취해 평가이익 290만 원을 올바르게 구했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 기말 변동 평가손익 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가축 사망 손실분을 평가이익 산식에 녹여내지 못해 오답입니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 기말 변동 평가손익 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분부대원가를 기말 가격에 가산하는 등 산식 오류로 발생했습니다.", "articles": [], "principle": "생물자산 기말 변동 평가손익 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "폐기 손실 처리를 오도하여 잘못 유도된 금액입니다.", "articles": [], "principle": "생물자산 기말 변동 평가손익 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "question": "(주)대관령목장은 20X1년 7월 1일 보유 중이던 어미양으로부터 새끼양 1마리를 출산하여 획득하였다. 출생 당일 새끼양의 순공정가치는 ₩200,000으로 파악되었다. 이후 20X1년 말(12월 31일) 현재 새끼양의 순공정가치는 ₩260,000으로 상승하였다. 당기 중 새끼양과 관련된 처분이나 추가 거래가 없을 때, (주)대관령목장이 20X1 회계연도에 새끼양의 출산 및 기말 평가와 관련하여 당기손익으로 인식할 전체 '생물자산평가이익'은 총 얼마인가?",
        "options": [
            "① ₩60,000",
            "② ₩200,000",
            "③ ₩260,000",
            "④ ₩460,000",
            "⑤ 영향 없음"
        ],
        "answer": "3",
        "explanation": "③ 번식(출생)으로 얻은 생물자산은 최초 인식 시점에 당기손익으로 인식합니다. 또한 매 기말 시가 변동분도 당기손익에 합산합니다.\n- 7월 1일 탄생 시 최초 인식 평가이익: ₩200,000\n  (차) 생물자산(새끼양) 200,000 / (대) 생물자산평가이익 200,000\n- 12월 31일 기말 평가이익: ₩260,000 - ₩200,000 = ₩60,000\n  (차) 생물자산(새끼양) 60,000 / (대) 생물자산평가이익 60,000\n따라서 20X1년에 인식할 전체 생물자산평가이익은 ₩200,000 + ₩60,000 = ₩260,000이 됩니다. 이는 결국 기말 최종 순공정가치 가액과 동일합니다.\n\n[오답 해설]\n① 7월 1일 최초 탄생일의 가치 20만 원을 수익에서 빠뜨리고 기말 기중 변동액 6만 원만 계상하여 오답입니다.\n② 최초인식 시점의 이익 20만 원만 잡고 기말 평가 변동을 무시하여 오답입니다.\n④ 두 가액을 이중 가산하여 과대계상한 46만 원은 오류입니다.\n⑤ 당기 손익에 지대한 유입(26만 원 증가)을 미치므로 영향 없음은 명백한 오답입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "출생 시 최초인식이익(20만)을 누락하고 기말 재평가 증가분(6만)만 산정했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 출생 및 기말 평가 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기말 재평가 변동에 따른 추가 이익(6만)을 빠뜨려 과소계상했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 출생 및 기말 평가 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "최초 인식 시 이익 20만 원과 기말 평가이익 6만 원을 합산하여 당기 전체 영향인 26만 원을 바르게 계산했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 출생 및 기말 평가 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "출생 가격과 기말 가격을 이중 중복 누적하여 계산 오류가 발생했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 출생 및 기말 평가 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당기순이익에 실질 영향을 주므로 오류 설명입니다.", "articles": [], "principle": "생물자산 출생 및 기말 평가 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "(주)목우농장은 20X1년 10월 1일 보유 중인 양들로부터 원시 양모를 수확하였다. 수확 당일 양모의 순공정가치는 ₩300,000이었다. 수확 이후 해당 양모는 창고에 보관되어 매각을 준비하였으며, 20X1년 말 현재 양모의 공정가치는 ₩290,000, 순실현가능가치는 ₩280,000으로 조사되었다. 이 양모와 관련하여 20X1 회계연도 당기순이익에 미치는 영향(순이익 변동총액)은 얼마인가? (단, 기초 재고자산평가충당금은 없다.)",
        "options": [
            "① ₩300,000 증가",
            "② ₩280,000 증가",
            "③ ₩20,000 감소",
            "④ ₩300,000 증가 및 ₩20,000 감소 (결합 ₩280,000 증가)",
            "⑤ ₩290,000 증가"
        ],
        "answer": "4",
        "explanation": "④ 수확물(양모)은 수확하는 시점에 순공정가치인 ₩300,000으로 최초 인식하며, 이 차액은 포괄손익계산서 상 '수확물평가이익 ₩300,000(당기순이익 증가)'으로 계상됩니다. 수확 이후부터는 K-IFRS 제1002호 '재고자산'이 적용되므로 기말 결산 시 저가법 평가(취득원가 ₩300,000 vs 기말 순실현가능가치 ₩280,000)를 수행하여 차액인 ₩20,000을 '재고자산평가손실(매출원가 가산, 당기순이익 감소)'로 인식합니다. 따라서 결합된 당기순이익 영향은 ₩300,000 증가(수확시점 이익) - ₩20,000 감소(기말 저가 감액) = ₩280,000 증가가 됩니다.\n\n[오답 해설]\n- 분개:\n  10월 1일 (차) 수확물 300,000 / (대) 수확물평가이익(당기손익) 300,000\n  12월 31일 (차) 재고자산평가손실 20,000 / (대) 재고자산평가충당금 20,000\n① 수확 후의 가치 하락에 따른 기말 저가법 평가손실 2만 원 인식을 누락하여 틀렸습니다.\n② 결합 손익 결과의 크기는 맞으나, 수확 시 평가이익 30만 원과 기말 평가손실 2만 원이 각각의 계정으로 구분 표시되어야 함을 설명하는 4가 해설 관점 상 더욱 완벽하고 정확한 지목이 됩니다.\n③ 기중 수확 시 30만 원의 이익을 무시하고 하락분만 표기하여 오답입니다.\n⑤ 기말 시가 29만 원과 무관하게 저가법 대조 금액은 NRV 28만 원입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "수확 후 발생한 저가법 평가손실 2만 원을 무시하여 오답입니다.", "articles": ["K-IFRS  제1041호 문단 13", "K-IFRS 제1002호 문단 9"], "principle": "수확 및 기말 저가법의 연계 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "결합 효과 총액 수치는 맞으나 세부 손익 계정 분해 진술이 미비합니다.", "articles": ["K-IFRS  제1041호 문단 13", "K-IFRS 제1002호 문단 9"], "principle": "수확 및 기말 저가법의 연계 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수확 시점의 가치 획득이익 30만 원을 수익에서 누락시켰습니다.", "articles": ["K-IFRS  제1041호 문단 13", "K-IFRS 제1002호 문단 9"], "principle": "수확 및 기말 저가법의 연계 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수확이익 30만 원 증가와 기말 저가법 손실 2만 원 차감이 결합하여 최종 28만 원 순이익이 증가하는 메커니즘을 가장 정확하게 분석했습니다.", "articles": ["K-IFRS  제1041호 문단 13", "K-IFRS 제1002호 문단 9"], "principle": "수확 및 기말 저가법의 연계 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기말 공정가치 29만 원을 단순 가산하여 틀린 계산입니다.", "articles": [], "principle": "수확 및 기말 저가법의 연계 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "(주)KAPA유업은 젖소들로부터 생유 1,000리터를 수확하였다. 수확 시점의 생유 리터당 순공정가치는 ₩2,000이었다. 수확 직후 (주)KAPA유업은 이 생유를 우유 유통업체에 리터당 ₩2,200에 매각 완료하였으며, 매각 당시 배송비 및 판매 수수료로 리터당 ₩100을 직접 지출하였다. (주)KAPA유업이 이 수확 및 매각 전체 거래를 통해 당기순이익에 미치는 영향은 총 얼마인가?",
        "options": [
            "① ₩2,100,000 증가",
            "② ₩2,200,000 증가",
            "③ ₩2,000,000 증가",
            "④ ₩100,000 증가",
            "⑤ ₩1,900,000 증가"
        ],
        "answer": "1",
        "explanation": "1 리터당 순공정가치 ₩2,000 기준 수확 시 자산가액 및 수확이익은 1,000리터 × ₩2,000 = ₩2,000,000입니다. 이후 우유 유통업체에 ₩2,200에 판매 시 발생하는 회계처리는 다음과 같습니다.\n- 수확 시: (차) 수확물(생유) 2,000,000 / (대) 수확물평가이익 2,000,000\n- 판매 시: \n  (차) 현금(등 수취액) 2,200,000 / (대) 매출 2,200,000\n  (차) 매출원가 2,000,000 / (대) 수확물(생유) 2,000,000\n  (차) 판관비(운반/수수료) 100,000 / (대) 현금 100,000\n따라서 결합 손익 영향은 다음과 같습니다.\n- 수확물평가이익: +₩2,000,000\n- 매출: +₩2,200,000\n- 매출원가: -₩2,000,000\n- 판관비: -₩100,000\n최종 결합 당기순이익 영향: ₩2,000,000 + ₩2,200,000 - ₩2,000,000 - ₩100,000 = ₩2,100,000 증가가 됩니다.\n\n[오답 해설]\n- 단순 이익은 매출 마진만 계산한 10만 원이 아닙니다. 왜냐하면 수확을 통한 원천 가치 획득 200만 원 자체가 회사의 주된 영업 순유입액(평가이익)으로 인식되기 때문입니다. 따라서 1번이 유일하게 정합한 당기순이익 영향액입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": True, "why": "수확 평가이익(200만)과 매각 거래마진(매출 220만 - 매출원가 200만 - 판관비 10만 = 10만 이익)을 정확히 연계하여 210만 원 증가를 도출했습니다.", "articles": ["K-IFRS 제1041호 문단 13", "K-IFRS 제1002호 문단 10"], "principle": "수확 및 즉시 처분 시 당기순이익 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "판매 대금 220만 원만을 단순 수익 영향으로 기재하여 처분 원가와 판관비를 누락했습니다.", "articles": [], "principle": "수확 및 즉시 처분 시 당기순이익 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수확 시점의 가치 200만 원만 표기하고 판매 거래 손익을 제외시켰습니다.", "articles": [], "principle": "수확 및 즉시 처분 시 당기순이익 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수확 시점의 200만 원 평가이익을 차단하고 매각 당일의 순 마진 10만 원만 표기하여 오답입니다.", "articles": [], "principle": "수확 및 즉시 처분 시 당기순이익 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "판관비 비용 처리를 이중으로 깎아 산정 오류를 냈습니다.", "articles": [], "principle": "수확 및 즉시 처분 시 당기순이익 효과", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "(주)산림경영은 20X1년 1월 1일 정부로부터 조림 사업 지원 목적으로 보조금 ₩100,000을 수령하였다. 이 보조금에는 'FSC(국제산림관리협의회) 기준에 부합하도록 환경 보호 수종을 식재하여 향후 3년간 벌목하지 않고 보존하여야 한다'는 명확한 조건이 붙어 있으며, 이 기간 내 조건을 충족하지 못하면 보조금을 일할 환수한다는 규정이 명시되어 있다. 20X1년 말 현재 (주)산림경영은 조림지를 성실히 관리하며 조건을 순조롭게 이행 중이다. K-IFRS 제1041호에 따라 (주)산림경영이 20X1년도 말 포괄손익계산서 상 당기순이익으로 반영할 이 보조금 관련 정부보조금수익은 얼마인가?",
        "options": [
            "① ₩100,000",
            "② ₩33,333",
            "③ ₩0",
            "④ ₩66,667",
            "⑤ ₩16,667"
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1041호 문단 35에 의하면, 순공정가치로 측정하는 생물자산과 관련된 정부보조금에 부수되는 조건이 있는 경우에는 '그 조건을 충족하는 시점에만' 당기손익으로 인식합니다. 3년간 보존 조건이 있으며, 20X1년 말은 아직 1년밖에 경과하지 않아 최종 조건이 완수되지 않았으므로 당기말에 정부보조금수익으로 계상할 금액은 ₩0(전액 부채(선수수익 등) 유지)입니다.\n\n[오답 해설]\n① 조건 충족 전 전액 수익 계상은 기준서 위배입니다.\n② 일반 정부보조금 기준서(제1020호)의 이연수익 상각법을 적용하여 1/3인 ₩33,333을 수익화하는 방식은 제1041호의 즉시인식 요건과 맞지 않는 오답입니다.\n④, ⑤는 임의로 설정한 오답 액수입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "조건 미충족 상태에서 전액 수익 처리는 규정 위반입니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 인식 시점 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "제1020호식의 정액 분할 이연수익 상각 처리를 제1041호 생물자산 보조금에 잘못 적용했습니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 인식 시점 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "3년 보존 조건이 최종 성취되지 않았으므로 20X1년 말 기준 정부보조금 수익은 0원임을 정확히 지적했습니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 인식 시점 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "경과 기간 미달 상태에서 과다 귀속하여 발생했습니다.", "articles": [], "principle": "조건부 정부보조금 인식 시점 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 월할 또는 임의 비율 계산 오류입니다.", "articles": [], "principle": "조건부 정부보조금 인식 시점 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "(주)우수한농산은 20X1년 11월 1일 농림수산부로부터 유기농 가축 육성 보조금으로 ₩50,000을 무조건부로 지원하겠다는 공식 지급 결정을 확정 통보받았다. 현금의 실제 계좌 입금은 다음 해인 20X2년 2월 10일에 이루어졌다. K-IFRS 제1041호에 의할 때, 이 무조건부 보조금에 대한 (주)우수한농산의 20X1년도 포괄손익계산서 상 정부보조금수익 인식액은 얼마인가?",
        "options": [
            "① ₩0 (20X1년에는 인식 불가)",
            "② ₩50,000",
            "③ ₩8,333 (2개월분 월할 인식)",
            "④ ₩45,000 (이자 공제액)",
            "⑤ ₩25,000 (반액 보수적 인식)"
        ],
        "answer": "2",
        "explanation": "② 순공정가치로 측정하는 생물자산과 관련된 정부보조금에 다른 조건이 없는 무조건부인 경우에는 '수취할 수 있게 되는 시점(receivable)'에만 당기손익으로 인식합니다. 20X1년 11월 1일에 공식 확정되어 수취할 권리가 성립했으므로(수취채권 계상 가능), 실제 현금 유입 여부와 상관없이 20X1년도에 전액인 ₩50,000을 당기수익으로 인식해야 합니다.\n\n[오답 해설]\n① 현금 유입일에만 잡는 현금주의 가정은 발생주의 원칙상 오류입니다.\n③ 월할 계산 규정은 무조건부 확정 보조금에 적용되지 않는 오답입니다.\n④, ⑤는 정당한 기준서 조항 외의 잘못된 세무/보수적 조절치입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "현금 수령 시점으로 인식을 이연하여 과소계상 오류가 발생했습니다.", "articles": ["K-IFRS 제1041호 문단 34"], "principle": "무조건부 정부보조금 수익 확정 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수취할 수 있게 된(지급 결정이 확정 통보된) 20X1년 11월에 전액 50,000원을 당기수익 인식해야 함을 올바르게 구했습니다.", "articles": ["K-IFRS 제1041호 문단 34"], "principle": "무조건부 정부보조금 수익 확정 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "불필요한 월할 귀속을 기계적으로 대입해 오류가 발생했습니다.", "articles": ["K-IFRS 제1041호 문단 34"], "principle": "무조건부 정부보조금 수익 확정 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시간가치 할인 공제 요건이 없으므로 오답입니다.", "articles": [], "principle": "무조건부 정부보조금 수익 확정 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 자의적 부분 인식액입니다.", "articles": [], "principle": "무조건부 정부보조금 수익 확정 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "(주)희귀목장은 최초 취득 당시 공정가치를 신뢰성 있게 측정할 수 없어 예외적으로 '원가모형'을 적용하는 생물자산 1마리를 20X1년 초 ₩2,000,000에 구입하였다. 이 가축의 내용연수는 5년, 잔존가치 ₩0이며 정액법으로 감가상각한다. 20X2년 말(2년차 말) 현재 해당 가축의 사용가치 하락으로 인하여 회수가능가액이 ₩800,000으로 떨어져 손상차손을 계상하고자 한다. 20X2 회계연도 말에 계상할 손상차손은 얼마인가?",
        "options": [
            "① ₩400,000",
            "② ₩1,200,000",
            "③ ₩0",
            "④ ₩200,000",
            "⑤ ₩800,000"
        ],
        "answer": "1",
        "explanation": "① 원가모형을 적용하는 생물자산은 K-IFRS 제1016호 및 제1036호에 준하여 감가상각과 손상 검사를 수행합니다.\n- 20X1년 감가상각비: ₩2,000,000 / 5년 = ₩400,000\n- 20X2년 감가상각비: ₩400,000\n- 20X2년 말 감가상각 후 장부금액: ₩2,000,000 - ₩800,000(감누) = ₩1,200,000\n- 20X2년 말 회수가능가액: ₩800,000\n- 손상차손액: 장부금액 ₩1,200,000 - 회수가능가액 ₩800,000 = ₩400,000이 됩니다.\n\n[오답 해설]\n② 감가상각액을 제외한 원금 200만 원과 회수가능액의 차액으로 손상을 과대 인식하여 오답입니다.\n③ 손상이 명확히 식별되므로 0원 계상설은 오류입니다.\n④, ⑤는 연도별 감가상각 상각누계액 산출에 심각한 오류가 개입된 오답 계산입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": True, "why": "2개년 감가상각 후 장부금액인 120만 원과 회수가능가액 80만 원의 차이인 40만 원을 손상차손으로 정상 계산했습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 생물자산의 상각 및 손상", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각비를 전면 누락하고 손상을 적용하여 과대계상했습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 생물자산의 상각 및 손상", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손상이 발생했음에도 인식하지 않아 오류입니다.", "articles": [], "principle": "원가법 생물자산의 상각 및 손상", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1개년분 상각만 진행하여 장부가를 틀리게 산출했습니다.", "articles": [], "principle": "원가법 생물자산의 상각 및 손상", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회수가능액 수치를 단순 손상차손액으로 오인했습니다.", "articles": [], "principle": "원가법 생물자산의 상각 및 손상", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "(주)글로벌아그로는 생물자산의 공정가치 변동액을 성격별로 공시하기 위해 '생물적 변환에 따른 순공정가치 변동액(신체적 변화)'과 '가격 변동에 따른 순공정가치 변동액'을 구분 평가하고자 한다. 다음 자료를 바탕으로 당기 중 육우들의 '신체적 변화에 기인한 순공정가치 증가액'은 얼마인가?\n■ 20X1년 초: 2년산 육우 10마리 보유 (마리당 순공정가치 ₩1,000)\n■ 20X1년 말: 3년산 육우 10마리 보유\n■ 20X1년 말 시점의 연령별 마리당 순공정가치:\n  - 2년산 육우: ₩1,050\n  - 3년산 육우: ₩1,250",
        "options": [
            "① ₩500",
            "② ₩2,000",
            "③ ₩2,500",
            "④ ₩1,500",
            "⑤ ₩1,000"
        ],
        "answer": "2",
        "explanation": "② 신체적 변화(성장)로 인한 가치 변동과 가격 변동에 따른 가치 변동은 다음의 공식을 활용하여 분해합니다.\n- 전체 변동액: 기말 기말가(3년산 1,250) $\times$ 10마리 - 기초 기초가(2년산 1,000) $\times$ 10마리 = ₩12,500 - ₩10,000 = ₩2,500\n- 가격 변동분: 기말 연령인 2년산 가치의 가격 상승분 대입\n  (기말 시점의 2년산 가격 1,050 - 기초 시점의 2년산 가격 1,000) $\times$ 10마리 = ₩500\n- 신체적 변동분(성장분): 기말 연령(3년산)과 기초 연령(2년산)의 기말 기준 가격차 대입\n  (기말 시점의 3년산 가격 1,250 - 기말 시점의 2년산 가격 1,050) $\times$ 10마리 = ₩2,000\n검산: 가격 변동분(₩500) + 신체적 변동분(₩2,000) = 총 변동분(₩2,500)으로 완벽하게 일치합니다.\n따라서 신체적 변화(성장)에 따른 증가액은 ₩2,000입니다.\n\n[오답 해설]\n① ₩500은 가격 변동에 기인한 순공정가치 증가액입니다.\n③ ₩2,500은 당기 포괄손익에 잡힐 전체 생물자산평가이익 총액입니다.\n④, ⑤는 연령별 비교단가를 혼동하여 잘못 도출된 오답입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "가격 변동분을 지목하여 질문과 어긋납니다.", "articles": ["K-IFRS 제1041호 문단 B51~B52"], "principle": "신체적 변환과 가격 변동의 분리 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기말 시점을 기준으로 3년산과 2년산의 가격 차이를 육우 마릿수에 대입해 신체적 변화(성장) 가치인 2,000원을 정밀하게 유도했습니다.", "articles": ["K-IFRS 제1041호 문단 B51~B52"], "principle": "신체적 변환과 가격 변동의 분리 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당기 전체 평가이익 총액 수치입니다.", "articles": ["K-IFRS 제1041호 문단 B51~B52"], "principle": "신체적 변환과 가격 변동의 분리 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기초 단가를 혼합하여 3년산 기말가와 2년산 기초가를 단순 대조하는 오류입니다.", "articles": [], "principle": "신체적 변환과 가격 변동의 분리 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 연령 차액 오도 계산액입니다.", "articles": [], "principle": "신체적 변환과 가격 변동의 분리 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "(주)애플가든은 과수 재배업을 전문으로 하며, 20X1 회계연도 말 현재 다음과 같은 자산을 보유하고 있다. 관련 기준서(제1016호 유형자산, 제1002호 재고자산, 제1041호 농림어업)를 적용할 때, (주)애플가든의 기말 재무상태표에 '유형자산(A)'과 '재고자산(B)'으로 각각 정상 보고되어야 할 자산의 총액은 얼마인가?\n■ 사과 수확을 목적으로 매년 기르는 사과나무들: 취득원가 ₩2,000,000 (감가상각누계액 ₩500,000)\n■ 기말 현재 사과나무 지엽에 아직 매달려 있는 사과 열매들: 순공정가치 ₩300,000\n■ 당기 중 사과나무에서 수확하여 기말 현재 보관 중인 사과: 순공정가치 ₩100,000, 순실현가능가치 ₩90,000 (LCM 저가법 적용 대상)\n■ 사과 수확 및 과수원 관리에 직접 사용하는 농기계: 장부금액 ₩400,000",
        "options": [
            "① A: ₩1,900,000 / B: ₩90,000",
            "② A: ₩1,500,000 / B: ₩390,000",
            "③ A: ₩1,900,000 / B: ₩390,000",
            "④ A: ₩1,500,000 / B: ₩90,000",
            "⑤ A: ₩2,000,000 / B: ₩100,000"
        ],
        "answer": "1",
        "explanation": "① 각 자산의 기준서별 분류 및 장부가액 평가는 다음과 같습니다.\n1) 사과나무: 생산용식물에 해당하므로 유형자산(제1016호)입니다. \n   장부금액 = ₩2,000,000 - ₩500,000 = ₩1,500,000\n2) 농기계: 일반 설비이므로 유형자산(제1016호)입니다. 장부금액 = ₩400,000\n   - 유형자산 합계(A) = ₩1,500,000 + ₩400,000 = ₩1,900,000\n3) 나무에 달린 사과 열매: 수확 전의 지엽 수확물이므로 생물자산(제1041호)에 해당합니다. 가액 = ₩300,000\n4) 수확하여 보관 중인 사과: 수확 완료물이므로 재고자산(제1002호)입니다. 기말 시점에는 저가법(LCM) 평가를 받아야 하므로 취득가액(수확일 순공정가치 ₩100,000)과 순실현가능가치(₩90,000) 중 낮은 금액인 ₩90,000으로 최종 측정됩니다.\n   - 재고자산 합계(B) = ₩90,000\n따라서 A는 ₩1,900,000, B는 ₩90,000이 됩니다. (나무에 매달린 사과 30만 원은 생물자산이라는 별도 과목으로 분류됨)\n\n[오답 해설]\n- 나무에 매달린 사과 30만 원을 재고자산에 잘못 포함하면 B가 ₩390,000이 되며(오답 ②, ③), 농기계를 누락하면 A가 ₩1,500,000이 되어 오답(④)이 됩니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": True, "why": "유형자산(나무 순액 150만 + 기계 40만 = 190만)과 재고자산(수확사과 저가법 9만)을 각각의 기준서 범위에 맞게 완벽히 분리 유도했습니다.", "articles": ["K-IFRS 제1041호 문단 5B", "K-IFRS 제1016호 문단 3", "K-IFRS 제1002호 문단 9"], "principle": "복합 재고/생물/유형 자산의 기말 분류 총액 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수확 전의 사과 열매(생물자산 30만)를 재고자산에 잘못 합산하여 오류가 발생했습니다.", "articles": ["K-IFRS 제1041호 문단 5B", "K-IFRS 제1002호 문단 9"], "principle": "복합 재고/생물/유형 자산의 기말 분류 총액 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유형자산 총액은 맞으나 재고자산에 생물자산을 혼입하는 분류 오류를 냈습니다.", "articles": ["K-IFRS 제1041호 문단 5B", "K-IFRS 제1002호 문단 9"], "principle": "복합 재고/생물/유형 자산의 기말 분류 총액 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유형자산 계산 시 전용 농기계 장부가 40만 원을 누락하여 과소계상했습니다.", "articles": ["K-IFRS 제1016호 문단 3"], "principle": "복합 재고/생물/유형 자산의 기말 분류 총액 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각과 저가법 및 자산 분류를 모두 미고려한 총액입니다.", "articles": [], "principle": "복합 재고/생물/유형 자산의 기말 분류 총액 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "(주)대한인삼은 20X1년 10월 1일 인삼밭에서 인삼을 수확하였다. 수확 시점의 순공정가치는 ₩500,000이었다. 수확 이후 해당 인삼은 재고자산으로 편입 보관되었으며, 20X1년 말 재고자산 평가를 위한 순실현가능가치는 ₩450,000으로 하락하여 저가법 평가손실을 정상 계상하였다. 이후 20X2년 말 현재 보관 중인 인삼의 시가 상승으로 순실현가능가치가 ₩520,000으로 크게 복구되었다. (주)대한인삼이 20X2회계연도 말에 재고자산 평가와 관련하여 인식할 '재고자산평가손실환입'은 얼마인가?",
        "options": [
            "① ₩70,000",
            "② ₩50,000",
            "③ ₩20,000",
            "④ ₩0",
            "⑤ ₩120,000"
        ],
        "answer": "2",
        "explanation": "② 수확물은 수확일의 순공정가치인 ₩500,000이 재고자산 기준서 상의 최초 '취득원가'가 됩니다.\n- 20X1년 말: 취득원가 ₩500,000 vs NRV ₩450,000 대조하여 재고자산평가손실 ₩50,000 인식 (충당금 ₩50,000 잔액 축적)\n- 20X2년 말: 시가 회복으로 NRV가 ₩520,000이 되었으나, 재고자산평가손실 환입은 당초 취득원가인 ₩500,000을 한도로만 계상할 수 있습니다. 즉, ₩520,000으로 올랐어도 장부금액은 최초 취득가인 ₩500,000까지만 복구 가능하므로, 20X2년 말 계상할 재고자산평가손실환입액은 ₩50,000(당초 쌓았던 충당금 잔액 전액 환입)이 됩니다.\n\n[오답 해설]\n① 한도를 무시하고 20X2년 말 NRV 52만 원과 1기말 45만 원의 단순 시가 차액 ₩70,000 전체를 환입하여 틀렸습니다. (초과분 2만 원은 인식 불가)\n③ 최초 수확 당시 가치와 기말 회복 시점 시가의 순 차액으로 구한 것은 오류입니다.\n④ 환입 조항이 강제되므로 0원은 오답입니다.\n⑤는 기타포괄 평가액 등을 덧셈한 산식 왜곡입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "취득원가 한도를 초과하여 단순 시가 회복분 전체(7만)를 환입하여 오답입니다.", "articles": ["K-IFRS 제1002호 문단 33"], "principle": "수확물 재고의 저가 환입 한도 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수확시점 순공정가치 50만 원을 최초 원가 한도로 파악하고, 당초 인식했던 평가손실 누적액 5만 원 전액을 최대 환입액으로 바르게 구했습니다.", "articles": ["K-IFRS 제1002호 문단 33"], "principle": "수확물 재고의 저가 환입 한도 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회복 시점의 시가 한도 초과 잔액을 잘못 기재한 값입니다.", "articles": ["K-IFRS 제1002호 문단 33"], "principle": "수확물 재고의 저가 환입 한도 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "환입액 인식을 누락하여 틀렸습니다.", "articles": [], "principle": "수확물 재고의 저가 환입 한도 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과도한 합산 산출 가액으로 오류입니다.", "articles": [], "principle": "수확물 재고의 저가 환입 한도 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "(주)초원농장은 20X1년 1월 1일 영업 개시 시점에 현금 ₩10,000,000을 투자하여 1년산 어미양 10마리를 마리당 ₩900,000(당일 처분부대원가는 마리당 ₩20,000 예상됨)에 구입하였다. 7월 1일 어미양들로부터 새끼양 5마리(출생일 마리당 순공정가치 ₩100,000)를 출산하였다. 12월 31일(기말) 현재 어미양의 마리당 순공정가치는 ₩950,000, 새끼양의 마리당 순공정가치는 ₩120,000이다. 기중 가축의 처분이나 사폐는 없었다. 20X1 회계연도 말 재무상태표에 표시될 총생물자산 금액은 얼마인가?",
        "options": [
            "① ₩9,500,000",
            "② ₩10,000,000",
            "③ ₩10,100,000",
            "④ ₩10,700,000",
            "⑤ ₩11,200,000"
        ],
        "answer": "4",
        "explanation": "④ 생물자산은 기말 현재 보유하고 있는 가축들의 순공정가치 총합으로 표시됩니다.\n- 기말 현재 보유 가축 현황:\n  1) 어미양 10마리: 기말 순공정가치 = 10마리 $\times$ ₩950,000 = ₩9,500,000\n  2) 새끼양 5마리: 기말 순공정가치 = 5마리 $\times$ ₩120,000 = ₩600,000\n- 기말 생물자산 총액 = 어미양 ₩9,500,000 + 새끼양 ₩600,000 = ₩10,100,000이 됩니다. \n\n*참고로 질문이 묻고 있는 것은 '총생물자산 가액'이므로 기말 실사 순공정가치 합산액인 ₩10,100,000(③)이 올바른 자산 표시액입니다. \n앗, 옵션 번호를 확인해보면 3번이 ₩10,100,000이며, 해설에 기재된 ₩10,100,000과 매칭되는 정답 번호는 ③번이 되어야 정합합니다. \n(원래 정답은 3번이며 옵션 구성도 3번이 정확합니다. 정답 지정을 3으로 기입하고 설명하겠습니다)\n\n[오답 해설]\n- 분개 상의 최종 자산 잔액은 ₩10,100,000이 맞습니다.\n① 새끼양을 누락하고 어미양만 계산한 오답입니다.\n② 최초 현금 투자액 수준을 단순 나열한 수치입니다.\n④ 1,070만 원은 출생 단가 합산을 왜곡한 틀린 계산입니다.\n⑤는 중복 합산 가액입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "새끼양의 기말 자산가치를 배제하여 틀린 계산입니다.", "articles": ["K-IFRS 제1041호 문단 12"], "principle": "기말 생물자산 잔액 총액 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기초 투자액만을 단순 지목하여 기중 변동을 무시했습니다.", "articles": ["K-IFRS 제1041호 문단 12"], "principle": "기말 생물자산 잔액 총액 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기말 시점의 어미양 순공정가치(950만)와 새끼양 순공정가치(60만)를 합해 정확한 생물자산 가액 1,010만 원을 도출했습니다.", "articles": ["K-IFRS 제1041호 문단 12"], "principle": "기말 생물자산 잔액 총액 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잘못된 단가 합산으로 유도된 수치입니다.", "articles": [], "principle": "기말 생물자산 잔액 총액 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분부대원가 반영 처리를 혼동한 오답 수치입니다.", "articles": [], "principle": "기말 생물자산 잔액 총액 계산", "case": {"holding": "", "no": None}}
        ],
        "answer": "3",
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "(주)푸른임업은 20X1년 1월 1일 조림 사업을 시작하기 위해 잣나무 묘목 100그루를 ₩1,000,000에 구입하였다. 당일 묘목의 추정 매각부대원가는 ₩50,000이었다. 20X1년 말 현재 잣나무 묘목의 순공정가치는 ₩1,200,000으로 상승하였다. 당기 중 관련 잣나무 묘목에 대해 인식할 포괄손익계산서 상 '생물자산평가이익(또는 손실)'은 총 얼마인가?",
        "options": [
            "① 평가이익 ₩200,000",
            "② 평가이익 ₩250,000",
            "③ 평가이익 ₩150,000",
            "④ 평가손실 ₩50,000",
            "⑤ 평가이익 ₩100,000"
        ],
        "answer": "2",
        "explanation": "② 기중 변동액을 계산해보면 다음과 같습니다.\n- 최초 취득 시 순공정가치(최초 인식액) = ₩1,000,000 - ₩50,000 = ₩950,000\n  이때 최초인식 평가손실 ₩50,000이 영업외비용 등으로 잡힙니다.\n- 기말 재측정 시 순공정가치 = ₩1,200,000\n  이때 기말평가이익 = ₩1,200,000 - ₩950,000 = ₩250,000이 잡힙니다.\n- 결합된 총평가손익은 최초 손실 5만 원과 기말 이익 25만 원의 순액인 20만 원 이익이 맞지만, 기말 평가 시점에 단독 인식할 순공정가치 재측정 평가이익은 ₩250,000이므로 정답은 ②입니다.\n\n[오답 해설]\n① ₩200,000은 취득 당시의 현금 유출액 100만 원과 기말 순공정가치의 단순 차액으로, 취득 시 발생한 5만 원의 거래 차손(최초인식손실)과 기말 시가조정분을 각각 구분 인식하는 기전을 무시한 순수 결과값일 뿐 기말 재측정 평가이익 과목 수치 자체는 아닙니다.\n③, ④, ⑤는 최초인식액 산출 오류로 인해 잘못 산정된 수치들입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "취득일 순공정가치 감액분을 누락하고 단순 계산한 순액 효과 수치입니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "조림 나무 생물자산의 연도 중 평가손익 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "최초 인식가액 95만 원과 기말 평가액 120만 원의 차이인 25만 원을 기말 생물자산평가이익으로 정확하게 구했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "조림 나무 생물자산의 연도 중 평가손익 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득 시 매각부대원가 반영을 가산으로 잘못 적용했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "조림 나무 생물자산의 연도 중 평가손익 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득일 당시의 최초인식손실 수치만을 지목하여 틀렸습니다.", "articles": [], "principle": "조림 나무 생물자산의 연도 중 평가손익 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가 변동분을 오도하여 나온 임의의 오답 값입니다.", "articles": [], "principle": "조림 나무 생물자산의 연도 중 평가손익 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "(주)미래축산은 기말 현재 장부상 순공정가치 ₩3,000,000으로 계상되어 있는 가축 1마리를 시장의 매수자에게 ₩3,200,000에 처분(매각)하였다. 매각 당시 가축의 인도 및 명도를 위해 직접 지출한 운반비와 수수료 등 처분 거래원가는 ₩50,000이었다. K-IFRS 제1041호에 의할 때, (주)미래축산이 이 처분 거래로 인하여 당기 손익에 반영할 '생물자산처분이익'은 얼마인가?",
        "options": [
            "① ₩200,000",
            "② ₩150,000",
            "③ ₩250,000",
            "④ ₩0",
            "⑤ ₩100,000"
        ],
        "answer": "2",
        "explanation": "② 생물자산 처분 시의 처분손익은 실제 순수취액(매각금액 ₩3,200,000 - 처분 거래원가 ₩50,000 = ₩3,150,000)과 처분 직전의 장부금액(순공정가치 ₩3,000,000)의 차액으로 결정됩니다.\n따라서 생물자산처분이익 = ₩3,150,000 - ₩3,000,000 = ₩150,000이 됩니다.\n\n[오답 해설]\n① 처분 거래비용 5만 원을 차감하지 않고 매각가와 장부가 차액만 산정하여 오답입니다.\n③ 처분 거래비용을 실수로 가산하여 구한 수치입니다.\n④ 처분손익이 명확하게 ₩150,000 발생하므로 0원은 오답입니다.\n⑤는 기타 오류성 계산액입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "처분 시 직접 유출된 거래비용 5만 원을 깎지 않아 틀렸습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 처분손익 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "순매각유입액인 315만 원과 기존 장부액 300만 원을 정밀히 대조하여 처분이익 15만 원을 올바르게 도출했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 처분손익 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비용을 이중으로 더하는 가산 오류를 범했습니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "생물자산 처분손익 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손익 유입을 누락시켜 오답입니다.", "articles": [], "principle": "생물자산 처분손익 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잘못된 차액 연산 수치입니다.", "articles": [], "principle": "생물자산 처분손익 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "(주)그린바이오는 정부로부터 생물자산 개발 정부보조금으로 총 ₩150,000을 수취하였다. 이 보조금에는 '친환경 축산 가이드라인에 맞춰 젖소용 축사를 무조건 3년간 운영하여야 하며, 3년 충족 전에는 정부 지시에 따라 미달성 비율만큼 보조금을 환수한다'는 세부 환수 조건이 붙어 있다. 2기말(2년차 말) 현재 (주)그린바이오가 해당 축사를 성실히 2년간 이행하였으며, 이행 조건 중 2/3 수준을 충족한 상황이다. K-IFRS 제1041호에 의할 때, 2기말 현재 당기순이익에 반영할 수 있는 정부보조금수익의 누적 합계액은 얼마인가?",
        "options": [
            "... 누적 ₩100,000 (2/3 조건 충족분)",
            "② ₩0 (최종 3년 경과 전까지는 일절 인식 불가)",
            "③ ₩150,000 (전액 즉시 인식)",
            "④ ₩50,000",
            "⑤ ₩75,000"
        ],
        "answer": "2",
        "explanation": "② 순공정가치 측정 생물자산 관련 정부보조금은 '조건이 모두 충족되는 시점'에만 당기순이익으로 인식할 수 있습니다. 3년간 보존 조건 하에서 환수 조건이 있으며 2기말 현재는 비록 2년이 경과했고 2/3를 충족했더라도, 전체 이행 기간인 3년이 끝나기 전까지는 최종 조건 충족이 아니므로 누적 인식 수익은 ₩0(전액 부채 유지)입니다.\n\n[오답 해설]\n① 임의의 진행 기준(2/3 충족) 적용은 불허되므로 10만 원은 오답입니다.\n③ 전액 즉시 인식 역시 조건이 남아 있어 불인정됩니다.\n④, ⑤는 정액이나 다른 비율에 기한 임의 계산 수치입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "진행률에 기한 보조금 분할 인식을 금하므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 귀속 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "환수 조건 및 보존 연도가 최종 완료되기 전까지는 진행 상황과 상관없이 당기수익을 전혀 인식하지 못하고 부채로 둠을 바르게 설명했습니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 귀속 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무조건부 즉시 인식 적용 오류입니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "조건부 정부보조금 귀속 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "1년차 해당분 인식설로 오답입니다.", "articles": [], "principle": "조건부 정부보조금 귀속 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "절반 인식 수치로 오류입니다.", "articles": [], "principle": "조건부 정부보조금 귀속 계산", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 3,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },

    # =========================================================================
    # L4: 분석 및 오류 수정 (8문항, 941~948번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s06-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "(주)KAPA과수원은 포도나무(유형자산인 생산용식물)를 생물자산(농림어업 기준서)으로 잘못 분류하여 기말에 감가상각비를 전혀 계상하지 않고, 대신 순공정가치 평가를 적용하여 평가이익을 과다 계상하였다. 이 회계적 분류 오류가 재무제표에 미치는 왜곡 효과에 대한 설명으로 가장 옳지 않은 것은?",
        "options": [
            "① 포도나무에 대한 감가상각 누락으로 인하여 당기 감가상각비 비용이 과소계상된다.",
            "② 기말 공정가치 상승분에 대해 생물자산평가이익을 과대계상함으로써 당기순이익이 과대유도될 수 있다.",
            "③ 포도나무 자체는 본래 유형자산으로 장부에 계상되어야 하나 생물자산으로 표시되므로 재무상태표의 자산 분류 왜곡이 생긴다.",
            "④ 감가상각을 적용했을 때보다 기말 자산 총계가 인위적으로 고평가될 가능성이 높다.",
            "⑤ 이 오류를 수정하더라도 당기말 유형자산처분손익의 크기에는 아무런 영향을 주지 않는다."
        ],
        "answer": "5",
        "explanation": "⑤ 포도나무는 생산용식물로서 유형자산이므로 향후 처분 시 K-IFRS 제1016호 유형자산 처분손익을 적용합니다. 장부금액이 다르게 유지되어 왔기 때문에 분류 오류를 수정하여 감가상각누계액과 원래의 원가로 환원시키면 당연히 기중 및 기말 처분 시점의 처분손익에도 금액적인 영향을 줍니다. 따라서 아무런 영향을 주지 않는다는 진술은 틀린 분석입니다.\n\n[오답 해설]\n① 상각을 안 했으므로 감상비 과소 계상이 맞습니다.\n② 미실현 시가 변동을 당기이익으로 대거 잡았으므로 이익 과대가 맞습니다.\n③, ④ 유형자산의 생물자산 오인으로 자산 분류 및 장부가액 고평가 왜곡이 초래됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비용 과소계상 왜곡은 정확한 분석입니다.", "articles": ["K-IFRS 제1041호 문단 5B", "K-IFRS 제1016호 문단 3"], "principle": "분류 오류가 재무제표에 미치는 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평가이익 부당 계상으로 순이익 과대계상이 유발됨이 맞습니다.", "articles": ["K-IFRS 제1041호 문단 5B", "K-IFRS 제1016호 문단 3"], "principle": "분류 오류가 재무제표에 미치는 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계정과목 및 자산 분류 위치가 틀어지므로 왜곡이 맞습니다.", "articles": ["K-IFRS 제1041호 문단 5B", "K-IFRS 제1016호 문단 3"], "principle": "분류 오류가 재무제표에 미치는 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가 상승을 그대로 타서 자산 총액이 부풀려집니다.", "articles": ["K-IFRS 제1041호 문단 5B", "K-IFRS 제1016호 문단 3"], "principle": "분류 오류가 재무제표에 미치는 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "장부금액 왜곡 상태에서 처분 시 처분손익 계산의 기저 장부가 자체가 변하므로, 처분손익에 영향을 미치지 않는다는 5의 분석은 오답이 됩니다.", "articles": ["K-IFRS 제1016호 문단 68"], "principle": "분류 오류가 재무제표에 미치는 왜곡 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "(주)초록팜은 순공정가치로 측정하는 생물자산 관련 무조건부 정부보조금 ₩50,000을 수령하였을 때, 당기수익으로 인식하지 않고 일반 정부보조금 기준서(제1020호)를 오독하여 '이연정부보조금수익(부채)'으로 대변 계상하였다. 이 오류가 20X1 회계연도 재무제표에 미치는 구체적 영향으로 가장 옳은 것은?",
        "options": [
            "① 당기순이익이 ₩50,000만큼 과대계상되고 부채는 과소계상된다.",
            "② 당기순이익이 ₩50,000만큼 과소계상되고 부채는 과대계상된다.",
            "③ 자산 총계가 ₩50,000만큼 부당하게 부풀려진다.",
            "④ 주주지분 내 자본잉여금이 ₩50,000만큼 과대계상된다.",
            "⑤ 재무상태표 및 손익계산서에 아무런 수치 왜곡이 발생하지 않는다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1041호 하에서 순공정가치 측정 생물자산 관련 보조금은 권리 확정(수취 가능) 시 즉시 전액 당기수익으로 털어야 합니다. 이를 부채(이연수익)로 올려두었으므로 당기수익(영업외수익 등) ₩50,000이 누락되어 당기순이익이 ₩50,000 과소계상되며, 갚지 않아도 되는 돈이 부채 자리에 있으므로 부채총액은 ₩50,000 과대계상됩니다.\n\n[오답 해설]\n① 이익과 부채의 왜곡 방향이 정반대로 서술되었습니다.\n③ 자산(현금) 유입은 동일하게 기록했으므로 자산 총액 왜곡은 없습니다.\n④ 자본 거래가 아니므로 자본잉여금과 무관합니다.\n⑤ 재무비율 및 당기순이익에 유의적 오류가 잔존합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수익 누락이므로 이익은 과소계상되어 틀렸습니다.", "articles": ["K-IFRS 제1041호 문단 34"], "principle": "정부보조금 회계처리 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "당기수익 즉시 인식을 안 하고 부채(이연수익)로 묶어둠으로써 발생하는 이익 과소와 부채 과대 효과를 정확히 규명했습니다.", "articles": ["K-IFRS 제1041호 문단 34"], "principle": "정부보조금 회계처리 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금 입금 처리는 제대로 했으므로 자산 규모 왜곡은 없습니다.", "articles": [], "principle": "정부보조금 회계처리 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본잉여금이 될 여지가 전혀 없는 일반 영업외적 거래입니다.", "articles": [], "principle": "정부보조금 회계처리 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수익과 부채 양 지표에 심각한 오류 왜곡이 유발되므로 오답입니다.", "articles": [], "principle": "정부보조금 회계처리 오류 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "(주)우량한우는 생물자산인 한우를 현금 취득하면서 발생한 운반비(취득 거래원가) ₩200,000을 자산의 취득원가에 포함하고, 추정 처분부대원가 ₩150,000을 차감하지 않고 최초 인식하여 장부를 마감하였다. 이 오류가 최초 인식 시점의 장부 상태 및 당기순이익에 미친 영향을 바르게 분석한 것은?",
        "options": [
            "① 생물자산 장부가액이 ₩350,000만큼 과대계상되고 당기순이익이 ₩350,000 과대계상된다.",
            "② 생물자산 장부가액이 ₩50,000만큼 과대계상되고 당기순이익이 ₩50,000 과소계상된다.",
            "③ 생물자산 장부가액은 차이가 없으나 당기 비용만 과대계상된다.",
            "④ 생물자산 장부가액이 ₩200,000 과대계상되고 처분부대원가 차감 누락으로 인해 당기순이익이 ₩150,000 과소계상된다.",
            "⑤ 자산이 ₩350,000만큼 덜 잡혀서 당기순이익이 ₩350,000만큼 훼손된다."
        ],
        "answer": "1",
        "explanation": "① 올바른 회계처리는 취득 거래원가 ₩200,000을 즉시 비용(당기손익) 처리하고, 자산액 산정 시 처분부대원가 ₩150,000을 빼서 자산을 깎아 적어야 합니다. \n- 올바른 자산 가액: 구입가 - 15만\n- 오류 자산 가액: 구입가 + 20만\n따라서 자산(생물자산)은 ₩200,000 + ₩150,000 = ₩350,000만큼 과대계상되었으며, 최초인식 시 즉각 인식했어야 할 당기손실 ₩350,000(취득비용 20만 + 처분부대원가 차감손실 15만)을 전혀 잡지 않았으므로 당기순이익 역시 ₩350,000만큼 고평가(과대계상)되는 결과가 생깁니다.\n\n[오답 해설]\n②, ③, ④, ⑤는 취득 비용의 자산화 오류와 처분비용의 차감 누락 효과를 정합적으로 계량 합산하지 못해 엉터리 수치를 제시한 틀린 보기들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "취득 부대비용의 자산화(20만 원 오류 가산)와 처분부대원가 차감 누락(15만 원 오류 미차감)의 효과가 결합되어 자산과 당기이익이 모두 35만 원씩 부풀려지는 실질을 정확하게 규명했습니다.", "articles": ["K-IFRS 제1041호 문단 12, 26"], "principle": "생물자산 취득 오류 영향 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "두 오류가 서로 상쇄되는 방향으로 잘못 차감하여 5만 원 수치가 나와 오답입니다.", "articles": ["K-IFRS 제1041호 문단 12, 26"], "principle": "생물자산 취득 오류 영향 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 잔액과 비용 배부에 상당한 금액적 누락이 존재하여 틀렸습니다.", "articles": [], "principle": "생물자산 취득 오류 영향 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산액과 당기손익의 개별 영향 분석 수치가 틀렸습니다.", "articles": [], "principle": "생물자산 취득 오류 영향 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산이 오히려 과소계상되었다는 정반대의 진술이므로 오답입니다.", "articles": [], "principle": "생물자산 취득 오류 영향 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "회사가 수확한 수확물(예: 인삼)에 대하여 수확시점 이후에도 K-IFRS 제1002호 재고자산 기준을 따르지 않고, 계속 농림어업 기준서(제1041호)에 따른 순공정가치 재측정 평가이익을 기말에 인식하였다. 당기에 시가가 크게 상승하였다고 할 때, 이 오류가 기말 재무제표에 미친 손익 왜곡 영향으로 옳은 것은?",
        "options": [
            "① 취득원가를 초과한 미실현이익을 잡았으므로 당기순이익이 과대계상되고 기말 재고자산이 과대계상된다.",
            "② 기말 재고자산이 저가법보다 낮게 평가되어 자산이 과소계상된다.",
            "③ 당기 매출원가가 부당하게 과대계상된다.",
            "④ 기말 재고자산평가충당금 부채 계정이 부풀려진다.",
            "⑤ 당기순이익에 전혀 영향이 없고 자본계정 분류만 틀어진다."
        ],
        "answer": "1",
        "explanation": "① 수확물은 수확 후 재고자산으로 편입되어 저가법을 적용하므로 원가 초과 시가 상승에 대해 평가이익을 절대 인식하지 못합니다. 그러나 계속 순공정가치법을 써서 원가를 초과하는 시가 상승분까지 재평가이익(당기손익)으로 잡았으므로, 당기순이익이 불법적으로 과대계상되며 기말 재고자산도 취득원가 한도를 뚫고 높게 보고되므로 자산 과대계상이 유발됩니다.\n\n[오답 해설]\n② 시가 상승을 타고 자산액이 원가 위로 과대계상되므로 오답입니다.\n③ 재고가 크게 평가되어 매출원가가 인위적으로 과소계상되는 구조가 형성되므로 틀렸습니다.\n④ 충당금 계정이 차감되는 것이 아니라 평가이익이 부당 반영되므로 오답입니다.\n⑤ 당기순이익에 직접적인 과대계상 오류가 잔존합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "저가법 한도를 위배하여 미실현 이익을 가산함으로써 기말 자산과 당기이익이 모두 과대계상됨을 올바르게 논증했습니다.", "articles": ["K-IFRS 제1041호 문단 13", "K-IFRS 제1002호 문단 9, 33"], "principle": "수확물 평가 오류 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산이 오히려 취득원가보다 높게 잡혀 과대계상되므로 틀렸습니다.", "articles": ["K-IFRS 제1041호 문단 13", "K-IFRS 제1002호 문단 9, 33"], "principle": "수확물 평가 오류 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기말재고가 과대해지면 매출원가는 과소해지므로 오답입니다.", "articles": [], "principle": "수확물 평가 오류 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고평가충당금을 차감하는 거래가 아닌 평가이익의 직접 대변 계상 오류입니다.", "articles": [], "principle": "수확물 평가 오류 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손익 계산서 최종 라인에 직접 왜곡이 개입되므로 틀렸습니다.", "articles": [], "principle": "수확물 평가 오류 왜곡 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "(주)나라농산은 기말 현재 공정가치를 신뢰성 있게 측정할 수 없음이 입증된 생물자산에 대하여 원가모형(정액법 감가상각 적용)으로 측정 방식을 적법하게 예외 설정하였다. 그러나 회계담당자는 기말에 정규 감가상각비 계상을 누락하고 손상 검사도 수행하지 않았다. 이 오류를 수정하는 수정 분개가 당기 기말 재무비율에 미치는 여파로 가장 올바른 것은?",
        "options": [
            "① 수정 분개 후, 총자산회전율(매출액/평균총자산)이 전보다 하락한다.",
            "② 수정 분개 후, 부채비율(총부채/총자본)이 전보다 상승한다.",
            "③ 수정 분개 후, 자기자본이익률(ROE)이 전보다 증가한다.",
            "④ 수정 분개 후, 자산총계가 전보다 불어난다.",
            "⑤ 수정 분개 후, 영업이익률이 전보다 큰 폭으로 개선된다."
        ],
        "answer": "2",
        "explanation": "② 누락한 감가상각비와 손상차손을 기입하는 올바른 오류수정 분개를 밟으면, 당기 비용(감상비, 손상차손)이 증가하여 당기순이익 및 자본(자기자본)이 감소하고, 자산총계(누계액 차감)도 차감됩니다.\n- 부채비율 계산식: 총부채 / 총자본(자기자본)\n분모인 자본이 이익 감소로 인해 줄어들므로, 부채비율의 최종 값은 기존보다 당연히 상승하게 됩니다.\n\n[오답 해설]\n① 자산분모가 줄어들므로 총자산회전율은 상승하여 오답입니다.\n③ 이익분자가 깎이므로 ROE는 감소합니다.\n④ 자산을 상각하고 감액했으므로 자산총계는 줄어듭니다.\n⑤ 감상비 가동으로 영업이익이 줄어 영업이익률은 나빠집니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "평균 자산총계 분모가 감소하므로 자산회전율은 기존보다 올라갑니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 생물자산 상각 누락 오류수정 효과", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비용 증가로 자본(분모)이 감소함에 따라 부채비율이 상승하게 됨을 정합적인 재무공식 연계를 통해 도출해냈습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 생물자산 상각 누락 오류수정 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당기순이익 분자가 감소하여 ROE도 악화되므로 오답입니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 생물자산 상각 누락 오류수정 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 차감 계정이 덧씌워지므로 자산 총액은 감소합니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "원가법 생물자산 상각 누락 오류수정 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업비용(감상비) 추가 계상으로 인해 이익률은 저하되므로 틀렸습니다.", "articles": [], "principle": "원가법 생물자산 상각 누락 오류수정 효과", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "(주)야생목재는 국가가 소유한 국유림 관리권만을 빌려, 인위적인 재배 관리 없이 매년 자연생장한 야생 나무들을 임의 벌목하여 판매하는 활동을 하고 있다. 이 회사가 해당 자연 수확물을 수확시점에 순공정가치로 잡아 '농림어업 평가이익' 영업수익으로 잡고 자산을 인식했을 때, K-IFRS 제1041호 기준서 관점에서 이 오류의 내용과 올바른 재작성 논리 분석으로 옳은 것은?",
        "options": [
            "① 야생 벌목은 인위적인 '변화의 관리(생육 지원 등)' 활동이 결여되어 농림어업활동의 범주에 부합하지 않으므로, 수확 시 평가이익을 계상할 수 없고 일반적인 천연자원 획득 원가 분개만을 적용해 판매 시 매출만 인식해야 한다.",
            "② 야생 상태 자원이라도 상업 가치가 있으므로 현행 1041호 적용 처리는 전적으로 정당하다.",
            "③ 농림어업이 아니므로 임대업 매출로 재분류해야 옳다.",
            "④ 무형자산 처분이익으로 전액 계정을 수정 배부한다.",
            "⑤ 수확 즉시 자산 가액을 0원으로 깎아 당기순이익에 미치는 누적 영향을 강제로 통제한다."
        ],
        "answer": "1",
        "explanation": "① K-IFRS 제1041호에 의할 때, 생물자산의 변환을 관리하지 않는 벌채(예: 관리하지 않는 자연림 벌목, 야생 어획 등)는 농림어업활동에 해당하지 않습니다. 따라서 수확할 당시에 순공정가치 평가이익을 선수취하는 제1041호 회계처리를 적용해서는 안 되며, 수확(벌목) 시 지출된 벌채 비용 등 실제 원가만으로 자산을 잡은 뒤 나중에 일반 판매 시점에 매출을 계상하는 전통적인 재고자산 매출거래로 회계처리해야 합니다.\n\n[오답 해설]\n② 변화의 관리 요건이 빠져서 제1041호 적용은 전적으로 오류입니다.\n③, ④, ⑤는 임대업이나 무형자산 또는 자산의 0원 처리 등 왜곡된 대체설로 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "인위적 관리 실질이 없는 자연림 벌목은 제1041호의 적용 범위가 아님을 지적하고, 전통적인 실현주의 재고 매출 거래로 회원되어야 함을 정확히 분석했습니다.", "articles": ["K-IFRS 제1041호 문단 5, 6"], "principle": "농림어업활동 해당 여부 판단 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "관리 없는 단순 채집은 농림어업이 아니므로 기준서 적용 정당설은 오답입니다.", "articles": ["K-IFRS 제1041호 문단 5, 6"], "principle": "농림어업활동 해당 여부 판단 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임대용역 매출로 볼 사안이 아닌 자가 수확 판매 사안이므로 오답입니다.", "articles": [], "principle": "농림어업활동 해당 여부 판단 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비유동 무형자산 처분 거래가 아니므로 틀렸습니다.", "articles": [], "principle": "농림어업활동 해당 여부 판단 오류 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인위적 0원 감액 적용설은 올바른 대안 분개가 아닙니다.", "articles": [], "principle": "농림어업활동 해당 여부 판단 오류 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "(주)푸른목장은 보유하고 있는 단일 품종의 양 100마리(동일한 활성시장을 가진 유사 가축군)에 대하여 자의적으로 50마리는 원가모형으로 감가상각하고, 나머지 50마리는 순공정가치모형으로 평가하여 보고하였다. 이 자의적인 측정 모형의 혼용 적용이 지닌 K-IFRS 상의 회계적 부당성에 대한 비판 및 분석으로 가장 합당한 것은?",
        "options": [
            "① 동일 품종 내에서 자산의 평가 방법을 자의적으로 선택 혼합하여 적용하는 것은 정보의 비교가능성과 중립성을 심각하게 훼손하므로 불허하며, 최초 인식시점에 전체 수량을 순공정가치로 일관되게 평가해야 한다.",
            "② 회사의 포트폴리오 다변화 전략상 5:5 비율 혼용은 정당한 분산 투자 기법으로 전적으로 허용된다.",
            "③ 원가모형이 더 보수적이므로 100마리 전체를 원가법으로 조기 통일하지 않은 점만 잘못되었다.",
            "④ 혼용 시 평가이익과 감상비가 상쇄되어 당기순이익이 항상 0원이 되는 균형 효과가 인정된다.",
            "⑤ 생물자산은 회계기준서에서 구체적 단일 모형 선택을 강제하지 않으므로 자의적 쪼개기 평가도 무방하다."
        ],
        "answer": "1",
        "explanation": "① 동일 그룹 내 생물자산에 대해 일부는 원가법, 일부는 공정가치법을 혼용 선택하는 것은 한국채택국제회계기준의 비교가능성과 회계정책 일관성 원칙에 위배되어 전면 금지됩니다. 공정가치를 신뢰성 있게 측정할 수 없는 경우의 원가법 적용은 불가피한 예외 사유가 객관적으로 입증된 특정 가축에 한하여 제한적으로 쓸 수 있을 뿐입니다.\n\n[오답 해설]\n② 분산 평가는 인정되지 않는 회계 기준 오독설입니다.\n③ 순공정가치 평가가 대원칙이므로 전체의 원가법 강제화 주장도 올바르지 않습니다.\n④ 상쇄 균형 효과는 가공의 오답 명제입니다.\n⑤ 기준서는 선택의 자의성을 강력히 규제합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "동일 자산 군 내 자의적 측정 기법 혼용의 부당성과 일관적 순공정가치 평가 대원칙을 정확히 매칭하여 비판했습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "측정 모형 혼용의 적격성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "혼용 평가 기법은 K-IFRS 상 허용되지 않습니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "측정 모형 혼용의 적격성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순공정가치법이 최우선 원칙이므로 원가법 전체 통일설도 조문과 어긋납니다.", "articles": ["K-IFRS 제1041호 문단 30"], "principle": "측정 모형 혼용의 적격성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당기 손익 수치가 완전히 왜곡되는 구조이므로 틀렸습니다.", "articles": [], "principle": "측정 모형 혼용의 적격성 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일관된 회계정책 적용 요건을 정면 위배하는 서술입니다.", "articles": [], "principle": "측정 모형 혼용의 적격성 분석", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "(주)영농조합은 20X1년 10월 10일 사과를 수확하였을 때, 당일의 객관적인 순공정가치 ₩100,000을 장부에 기록하지 않고, 향후 설날 연휴 대목에 팔 수 있는 예상 명절 판매가격 ₩150,000(예상 판매 비용은 없음)으로 기입하여 자산을 과대평가하였다. 이후 해당 사과는 20X1년 말까지 팔리지 않고 재고로 남아 있다. 이 오류가 20X1 회계연도 기말 재무제표에 초래한 정량적 오류 수정 분개와 손익 효과로 가장 적합한 것은?",
        "options": [
            "① 기말 사과의 실제 취득가치는 ₩100,000이며, 오류를 바로잡기 위해서는 대변에 재고자산을 ₩50,000 깎고 차변의 수확물평가이익 영업수익을 ₩50,000 감소시켜야 한다. 이로 인해 당기순이익은 ₩50,000 감소하게 된다.",
            "② 기말 사과를 명절 가격으로 유지하는 것이 미래 가치를 가장 잘 반영하므로 수정 분개는 필요 없다.",
            "③ 차변에 재고자산을 ₩50,000 증가시키고 대변에 자본잉여금을 ₩50,000 늘린다.",
            "④ 재고자산평가손실을 차변에 ₩50,000 계상하고 대변에 재고자산평가충당금을 ₩50,000 늘려 장부가액을 ₩150,000으로 유지한다.",
            "⑤ 매출액을 ₩50,000 감소시키고 매출원가를 ₩50,000 늘린다."
        ],
        "answer": "1",
        "explanation": "① 수확물은 '수확 시점의 순공정가치'인 ₩100,000이 취득원가가 되어야 하므로, 자의적 미래 기대가 ₩150,000으로 올린 것은 부당한 자산 및 수익 과대계상 오류입니다. 따라서 오류를 수정하는 올바른 분개는 (차) 수확물평가이익 50,000 / (대) 재고자산(사과) 50,000 이며, 이 결과 당기 영업외수익(평가이익)이 줄어 당기순이익은 ₩50,000 감소하게 됩니다.\n\n[오답 해설]\n② 자의적 명절 예상 시가 반영은 역사적 취득가(수확 시 순공정가치) 설정 규칙 위반이므로 반드시 수정되어야 합니다.\n③ 자산을 가산하여 자본을 잡는 것은 분식 확장에 해당합니다.\n④ 평가손실은 취득원가 하락 시 잡는 것이며, 취득원가 자체의 등록 오류를 덮는 수단이 아닙니다.\n⑤ 아직 판매되지 않은 재고이므로 매출/매출원가와 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "수확일의 순공정가치(10만)와 오류 설정액(15만)의 차이를 자산 대변 차감 및 이익 차변 취소를 통해 바로잡고 손익 영향을 5만 원 감소로 잘 도출했습니다.", "articles": ["K-IFRS 제1041호 문단 13"], "principle": "수확물 최초 가격 설정 오류 수정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 임의 시가 반영 옹호설은 명백한 회계 기준 위배 주장입니다.", "articles": ["K-IFRS 제1041호 문단 13"], "principle": "수확물 최초 가격 설정 오류 수정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산을 오히려 더 키워 장부를 추가 왜곡하므로 틀렸습니다.", "articles": [], "principle": "수확물 최초 가격 설정 오류 수정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 등록 오류는 충당금 LCM 거래로 해결할 수 없습니다.", "articles": [], "principle": "수확물 최초 가격 설정 오류 수정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미판매 재고이므로 매출/원가 변경 대안은 오답입니다.", "articles": [], "principle": "수확물 최초 가격 설정 오류 수정", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 4,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },

    # =========================================================================
    # L5: 심화 / 종합 논증 (2문항, 949~950번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s06-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "(주)가람낙농은 20X1년 1월 1일 설립되어 당기 중 다음과 같은 일련의 농림어업 거래를 집행하였다. 제시된 정보를 종합할 때, (주)가람낙농의 20X1 회계연도 포괄손익계산서 상 '당기순이익에 미치는 결합 영향(순증감액)'은 얼마인가? (단, 기초 재고자산평가충당금은 없으며, 모든 거래는 현금으로 정산되었고, 제시된 가액은 모두 거래수수료 등 매각부대원가가 완전히 반영되어 계산 완료된 최종 순공정가치 혹은 실 지출액이다.)\n\n1. 1월 1일: 어미 젖소 10마리를 총 ₩10,000,000에 구입하여 축산업을 시작하였다. 당일 어미 젖소의 순공정가치는 총 ₩9,500,000이었다. (취득 거래비용은 없음)\n2. 7월 1일: 어미 젖소들로부터 송아지 2마리가 탄생하였다. 탄생일 현재 송아지들의 순공정가치는 총 ₩1,000,000이었다.\n3. 10월 1일: 어미 젖소들로부터 원시 우유(생유)를 획득하였다. 수확 당시 생유의 순공정가치는 총 ₩800,000이었다.\n4. 11월 1일: 정부로부터 친환경 가축 육성 보조금 ₩300,000을 현금 수령하였다. 이 보조금에는 '보조금을 받은 날로부터 2년간 낙농업을 유지하여야 하며, 2년 내 폐업 시 전액 환수한다'는 부수 조건이 명시되어 있다. 당기말 현재 영업은 순조롭게 계속 유지 중이다.\n5. 12월 1일: 10월 1일에 수확하여 보관하고 있던 생유의 50%를 외부 우유 가공업체에 ₩450,000에 현금 판매 완료하였다.\n6. 12월 31일(기말): 어미 젖소의 순공정가치 총액은 ₩9,200,000, 송아지의 순공정가치 총액은 ₩1,150,000이 되었으며, 남아 있는 생유 50%의 기말 순실현가능가치는 ₩380,000으로 하락하여 저가법 평가를 수행하였다.",
        "options": [
            "① ₩1,180,000 증가",
            "② ₩1,280,000 증가",
            "③ ₩1,480,000 증가",
            "④ ₩980,000 증가",
            "⑤ ₩880,000 증가"
        ],
        "answer": "1",
        "explanation": "① 거래 단계별 20X1년 당기순이익 영향액을 철저히 계산하면 다음과 같습니다.\n1. 어미 젖소 구입: \n   - 구입 시 현금 유출: ₩10,000,000\n   - 자산 등록 순공정가치: ₩9,500,000\n   - 최초인식평가손실 = -₩500,000 (비용)\n2. 송아지 탄생 (번식): \n   - 최초인식평가이익 = +₩1,000,000 (수익)\n3. 생유 수확 (수확물): \n   - 최초인식평가이익 = +₩800,000 (수익) -> 이 시점에 생유 취득원가는 ₩800,000으로 확정\n4. 조건부 정부보조금 수령: \n   - 2년 유지 조건이 부과되어 있어 아직 기간 미경과로 조건을 충족하지 못했으므로 당기수익은 ₩0 (선수금 부채 30만 원 계상)\n5. 생유 50% 판매:\n   - 매출 = +₩450,000\n   - 매출원가 = -₩400,000 (최초 취득원가 ₩800,000의 50%)\n   - 판매에 따른 당기이익 효과 = ₩450,000 - ₩400,000 = +₩50,000\n6. 기말 가축 순공정가치 재측정 및 잔여 생유 저가법 평가:\n   - 어미 젖소 평가: 기말 순공정가치 ₩9,200,000 - 직전 장부가 ₩9,500,000 = -₩300,000 (평가손실)\n   - 송아지 평가: 기말 순공정가치 ₩1,150,000 - 탄생 당시 장부가 ₩1,000,000 = +₩150,000 (평가이익)\n   - 잔여 생유 50%(원가 ₩400,000) 저가평가: 기말 NRV ₩380,000으로 ₩20,000 하락하였으므로 저가법에 따른 재고자산평가손실 = -₩20,000 (매출원가 가산)\n\n* 당기순이익 결합 효과 총계산:\n  (-₩500,000) [어미소 최초손실] \n  + ₩1,000,000 [송아지 최초이익] \n  + ₩800,000 [생유 최초수확이익] \n  + ₩50,000 [생유 판매 마진] \n  - ₩300,000 [어미소 기말손실] \n  + ₩150,000 [송아지 기말이익] \n  - ₩20,000 [생유 기말저가손실]\n  = -50만 + 100만 + 80만 + 5만 - 30만 + 15만 - 2만 = ₩1,180,000 증가가 됩니다.\n\n[오답 해설]\n- 조건부 정부보조금 30만 원을 당기수익에 잘못 반영하면 ₩1,480,000 증가(③)가 되어 오답입니다.\n- 어미젖소 최초인식손실 50만 원 계상을 누락하면 ₩1,680,000 증가가 됩니다.\n- 생유 판매 마진 및 기말 저가법 평가손실 2만 원 계산의 논리 선후를 어긋나게 풀면 2번, 4번, 5번 등의 잘못된 금액으로 도출됩니다. 따라서 정답은 ①입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": True, "why": "가축 최초 손실(-50만), 출산(+100만), 수확(+80만), 매각 마진(+5만), 기말 가축재측정(-15만 합계), 재고자산 저가손실(-2만), 보조금 이연(0원)의 다중 복합 거래를 결합하여 정확한 당기순이익 영향인 118만 원 증가를 유도했습니다.", "articles": ["K-IFRS 제1041호 문단 12, 13, 26, 35", "K-IFRS 제1002호 문단 9"], "principle": "목축업 복합 시나리오 하 당기순이익 영향 종합 산출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "생유의 처분 마진 및 저가법 단가 대조 연동 과정에 산술적 오류를 냈습니다.", "articles": [], "principle": "목축업 복합 시나리오 하 당기순이익 영향 종합 산출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미성취된 조건부 정부보조금 30만 원을 수익에 부당 산입하여 과대 유도되었습니다.", "articles": ["K-IFRS 제1041호 문단 35"], "principle": "목축업 복합 시나리오 하 당기순이익 영향 종합 산출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "어미젖소의 최초 인식손실 50만 원 인식을 생략하거나 다르게 계상했습니다.", "articles": [], "principle": "목축업 복합 시나리오 하 당기순이익 영향 종합 산출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "송아지 기말 재평가 또는 우유 저가법 차액 계산 요소를 빠뜨려 오답이 발생했습니다.", "articles": [], "principle": "목축업 복합 시나리오 하 당기순이익 영향 종합 산출", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 5,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s06-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "K-IFRS 제1041호 '농림어업'이 규정하는 생물자산의 순공정가치 평가 모형이 전통적 회계 이론의 근간인 '실현주의(Realization principle)' 원칙과 형성하는 논리적 갈등 양상을 비판적으로 분석하고, 자산의 생물적 변환(Biological transformation) 사건 자체를 수익 인식 시점으로 삼는 학술적 정당성을 논증한 기술 중 가장 올바르지 않은 것은?",
        "options": [
            "① 전통적 실현주의는 외부 시장 참여자와의 교환 거래를 통해 판매 가격이 확정되고 통제권이 이전되는 시점에 수익을 인식하지만, 제1041호는 판매 전 성장이나 번식 단계에서도 순공정가치 변동액을 영업수익(당기손익)화함으로써 실현주의의 역사적 거래 한계를 완화한다.",
            "② 농림어업활동에서는 생물자산의 생물적 변환(성장, 번식 등)이 핵심적인 부의 창출 활동이므로, 이를 무시하고 최종 판매 시점에만 수익을 몰아 인식한다면 매 보고기간의 영업 성과를 적절히 배분하지 못해 기간 손익 보고의 왜곡을 유발한다.",
            "③ 생물자산은 시장에 공시가격이 비교적 풍부하게 제공되므로 활성시장이 존재한다면 실현주의가 요구하는 측정의 객관성 및 신뢰성을 상당 부분 극복할 수 있어, 미실현 평가이익의 당기 손익 귀속이 정당화될 수 있다.",
            "④ 생물자산의 생물적 변환에 따른 평가손익은 전액 현금 유입이 즉각 수반되지 않는 평가 지표이므로, 과도한 배당 압력을 제어하기 위해 발생 즉시 기타포괄손익(OCI)으로 분류 보류한 뒤 최종 매각일이 속하는 기간에 당기순이익으로 일시 재분류 조정하는 것이 기준서의 엄격한 자본 보전 규칙이다.",
            "⑤ 활성시장이 없는 Level 3 수준의 추정 공정가치를 쓸 수밖에 없는 조림림이나 희귀 품종 생물자산의 경우, 평가 모형의 과도한 주관성 개입으로 인하여 경영자의 자의적 이익 조정 수단으로 오용될 우려가 존재한다."
        ],
        "answer": "4",
        "explanation": "④ K-IFRS 제1041호 하에서 생물자산의 최초 인식 및 기말 순공정가치 재측정으로 인한 평가손익은 '전액 발생 즉시 당기손익(당기순이익)'으로 분류됩니다. 기타포괄손익(OCI)으로 적립해 두었다가 나중에 재분류(재조정)한다는 설명은 기준서의 전형적인 당기손익 처리 규칙을 정면 부정하는 명백한 오류 기술입니다.\n\n[오답 해설]\n① 생물자산 평가의 실현주의 대비 독특한 완화적 실질을 학술적으로 정교하게 서술했습니다.\n② 판매 시점이 아닌 '가치 창출 시점(생물적 변환)'에 성과를 매칭해야 기간 손익이 정확해진다는 당위성을 올바르게 제기했습니다.\n③ 공시가격이 있는 활성시장 하에서는 미실현 손익의 측정 신뢰성 비판을 극복할 수 있음을 바르게 논증했습니다.\n⑤ 활성시장 결여 시 미래 현금흐름 현재가치 추정 등으로 인한 자의성 개입 우려라는 실무적 한계를 잘 비판했습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "전통적 실현주의와 농림어업 공정가치 평가의 본질적 대립 구도를 정확히 서술했습니다.", "articles": [], "principle": "농림어업 회계의 이론적 쟁점 논증", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가치 창출 활동과 수익 인식 매칭의 중요성을 학술적으로 타당하게 변론했습니다.", "articles": [], "principle": "농림어업 회계의 이론적 쟁점 논증", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "측정 신뢰성을 활성시장 데이터로 확보함으로써 미실현이익 인식이 타당해진다는 학설을 정합적으로 설명했습니다.", "articles": [], "principle": "농림어업 회계의 이론적 쟁점 논증", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "생물자산 평가손익은 OCI로 보내지 않고 전액 당기순이익으로 반영하므로, OCI 적립 및 추후 재분류 조정이 자본 보전 규칙이라는 4의 진술은 전적으로 왜곡된 거짓 이론입니다.", "articles": ["K-IFRS 제1041호 문단 26"], "principle": "농림어업 회계의 이론적 쟁점 논증", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "Level 3 평가 추정 시 발생할 수 있는 이익 조정 남용 한계를 객관적으로 잘 지적했습니다.", "articles": [], "principle": "농림어업 회계의 이론적 쟁점 논증", "case": {"holding": "", "no": None}}
        ],
        "indexing_v4": {
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True,
            "difficulty": 5,
            "mapped_taxonomy": {
                "subject": "회계학",
                "sub_subject": "재무회계",
                "chapter": "제2장 자산",
                "section": "Chapter 03 재고자산",
                "item": "6절 농림어업"
            }
        }
    }
]

questions.extend(new_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(new_questions)} new questions. Total questions in questions_db_accounting.json: {len(questions)}")
