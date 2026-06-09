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
    # L1: 기초 개념 (10문항, 951~960번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s01-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "다음 중 K-IFRS 기준 상 유형자산(Property, Plant, and Equipment)의 정의적 요건에 해당하지 않는 항목은?",
        "options": [
            "① 재화나 용역의 생산이나 제공에 사용할 목적으로 보유한다.",
            "② 타인에 대한 임대 또는 관리활동에 사용할 목적으로 보유한다.",
            "③ 물리적 형태가 있는 비화폐성자산이다.",
            "④ 한 회계기간을 초과하여 사용할 것이 예상되는 자산이다.",
            "⑤ 통상적인 영업과정에서 판매를 목적으로 보유하는 단기 유동자산이다."
        ],
        "answer": "5",
        "explanation": "⑤ 통상적인 영업과정에서 판매를 목적으로 보유하는 자산은 유형자산이 아닌 K-IFRS 제1002호 '재고자산'의 정의에 해당합니다.\n\n[오답 해설]\n①, ②, ③, ④는 K-IFRS 제1016호 문단 6에 명시된 유형자산의 핵심 요건(물리적 형체 존재, 영업/임대/관리용 보유, 장기 사용 예상)에 완벽히 부합합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "생산 및 용역 제공 목적 보유는 유형자산의 정의 요건입니다.", "articles": ["K-IFRS 제1016호 문단 6"], "principle": "유형자산의 정의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "타인 임대 및 관리활동 사용 목적 보유 역시 유형자산 정의에 포함됩니다.", "articles": ["K-IFRS 제1016호 문단 6"], "principle": "유형자산의 정의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "물리적 형태가 존재하여 무형자산과 구분되는 유형자산의 기본 속성입니다.", "articles": ["K-IFRS 제1016호 문단 6"], "principle": "유형자산의 정의 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "한 회계기간을 초과하는 장기 사용 예상이 필요합니다.", "articles": ["K-IFRS 제1016호 문단 6"], "principle": "유형자산의 정의 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "판매 목적으로 보유하는 자산은 유형자산이 아니라 재고자산의 정의이므로 유형자산 요건에서 배제됩니다.", "articles": ["K-IFRS 제1016호 문단 6"], "principle": "유형자산의 정의 요건", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "안전이나 환경상의 이유로 취득하는 유형자산(예: 화학 공장의 유독가스 차단 안전 설비)의 자산 인식 가능 여부에 대한 K-IFRS의 입장으로 가장 올바른 것은?",
        "options": [
            "① 당해 안전 자산 자체에서 직접적인 미래경제적효익을 창출하지 못하므로 자산으로 인식할 수 없고 전액 비용 처리한다.",
            "② 관련 다른 자산으로부터 미래경제적효익을 얻기 위해 필수적이므로 당해 안전 설비도 유형자산으로 인식할 수 있다.",
            "③ 안전 설비는 임시 자산이므로 무조건 부외자산으로 분류하여 공시만 한다.",
            "④ 정부의 강제 규제 충족 여부와 무관하게 전액 영업외비용으로 일괄 처리한다.",
            "⑤ 취득 당시 시장 매각가치가 존재할 때에만 한하여 일시적 재고자산으로 인식한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 11에 의하면, 안전이나 환경상의 이유로 취득하는 유형자산은 그 자체에서 직접 미래경제적효익을 얻을 수는 없지만, 기업이 다른 자산에서 미래경제적효익을 얻기 위하여 필요할 수 있습니다. 이러한 유형자산은 당해 자산을 취득하지 않았을 경우보다 관련 자산으로부터 미래경제적효익을 더 많이 얻을 수 있게 해주기 때문에 자산으로 인식할 수 있습니다.\n\n[오답 해설]\n① 자산인식이 가능하므로 전액 비용설은 오답입니다.\n③, ④, ⑤는 기준서의 자산 인식 근거를 부인하는 잘못된 진술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산인식이 인정되므로 비용화 진술은 틀렸습니다.", "articles": ["K-IFRS 제1016호 문단 11"], "principle": "안전/환경 관련 설비 자산인식", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "타 자산의 경제적 효익을 안전하게 유입하기 위해 필수적인 안전설비는 유형자산으로 인식할 수 있다는 기준서 취지에 정확히 부합합니다.", "articles": ["K-IFRS 제1016호 문단 11"], "principle": "안전/환경 관련 설비 자산인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정식 자산 계상이 허용되므로 부외자산 설명은 오답입니다.", "articles": ["K-IFRS 제1016호 문단 11"], "principle": "안전/환경 관련 설비 자산인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비용 일괄 처리가 아니므로 틀렸습니다.", "articles": [], "principle": "안전/환경 관련 설비 자산인식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고자산이 아닌 영업용 유형자산으로 분류됩니다.", "articles": [], "principle": "안전/환경 관련 설비 자산인식", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "유형자산 취득 시 취득원가에 포함시켜 자본화할 수 없고, 발생 즉시 판매비와관리비 또는 영업외비용으로 비용 처리하여야 하는 지출 항목은?",
        "options": [
            "① 유형자산의 취득이나 건설과 직접적으로 관련되어 발생한 종업원급여",
            "② 기계장치를 가동하기 위해 설치 장소를 준비하는 설치장지 준비 원가",
            "③ 공장 부지를 개설하여 새로운 시설을 가동하기 전에 개최한 홍보 행사 소요 원가",
            "④ 기계장치의 최초 운송비 및 취급 관련 원가",
            "⑤ 설계 관련 전문가에게 지급하는 직접 수수료"
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1016호 문단 19에 명시된 바와 같이, 새로운 시설을 개설하는 데 소요되는 원가, 새로운 상품과 서비스를 소개하는 데 소요되는 원가(광고선전비 등)는 유형자산의 취득원가에 포함할 수 없으며 발생 시 당기비용으로 인식합니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 유형자산이 의도한 방식으로 가동될 수 있도록 필요한 장소와 상태에 이르게 하는 데 직접 기여하는 원가(직접관련원가)로서 모두 자산 취득원가에 산입할 수 있는 항목들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "직접 관련 인건비는 자산원가 구성요소입니다.", "articles": ["K-IFRS 제1016호 문단 17"], "principle": "취득원가 제외 항목 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "설치장소 준비원가는 자산원가에 정상 가산됩니다.", "articles": ["K-IFRS 제1016호 문단 17"], "principle": "취득원가 제외 항목 식별", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "홍보/소개 및 새로운 시설 개설원가는 자산 취득원가에서 제외하고 당기비용 처리함을 바르게 지목했습니다.", "articles": ["K-IFRS 제1016호 문단 19"], "principle": "취득원가 제외 항목 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "운송비 및 취급원가는 직접관련원가로 자산화됩니다.", "articles": ["K-IFRS 제1016호 문단 17"], "principle": "취득원가 제외 항목 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전문가 수수료도 직접관련원가 요건을 충족합니다.", "articles": ["K-IFRS 제1016호 문단 17"], "principle": "취득원가 제외 항목 식별", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "K-IFRS 제1016호 상 유형자산의 취득원가는 인식시점의 어떤 금액을 기준으로 측정하도록 선언되어 있는가?",
        "options": [
            "① 미래 처분 예상 시점의 추정 순매각대금",
            "② 자산 인식시점의 현금가격상당액(Cash price equivalent)",
            "③ 자산의 물리적 해체 시 소요될 복구비 총액",
            "④ 매 보고기간말의 공정가치 총액",
            "⑤ 취득 이후 5년간 예상되는 누적 공헌이익"
        ],
        "answer": "2",
        "explanation": "② 유형자산의 취득원가는 '인식시점의 현금가격상당액'으로 측정함을 원칙으로 합니다.\n\n[오답 해설]\n① 처분 시 가액은 역사적 취득가 측정과 무관합니다.\n③ 복구비는 현재가치로 할인하여 일부 가산할 뿐, 취득원가 전체를 대용하진 못합니다.\n④ 기말 공정가치는 최초 측정이 아닌 후속 측정(재평가모형 등) 관련 개념입니다.\n⑤ 공헌이익은 미래 기대치로 취득원가 기준이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "처분 시 예상액은 최초 측정 기준이 아닙니다.", "articles": ["K-IFRS 제1016호 문단 23"], "principle": "최초 취득원가 측정 기준", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "유형자산 최초 원가는 결제 시점의 현금가격상당액을 기초로 측정함을 바르게 서술했습니다.", "articles": ["K-IFRS 제1016호 문단 23"], "principle": "최초 취득원가 측정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "복구비 총액은 자산의 기준점이 될 수 없습니다.", "articles": ["K-IFRS 제1016호 문단 23"], "principle": "최초 취득원가 측정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매 기말 공정가치는 후속 측정 선택사항 관련 개념입니다.", "articles": [], "principle": "최초 취득원가 측정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기대 공헌이익은 회계 측정 대상액이 아닙니다.", "articles": [], "principle": "최초 취득원가 측정 기준", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "자가건설한 유형자산(Self-constructed assets)의 최초 취득원가를 결정할 때 K-IFRS 기준서에 명시된 제외 요건으로 가장 올바른 것은?",
        "options": [
            "① 외부 구입 자산과 달리 자가건설 자산은 어떠한 직접관련 인건비도 자산화할 수 없다.",
            "② 자가건설에 따른 내부이익과 자가건설 과정에서 원재료, 인력 등의 낭비로 인한 비정상적인 원가는 자산의 원가에 포함하지 않는다.",
            "③ 자가건설 자산은 무조건 완공 후 3년간 감가상각이 보류된다.",
            "④ 건설 중에 지불한 외주 제작사 지급 수수료는 전액 판관비로 비용 처리한다.",
            "⑤ 자가건설한 자산은 완공될 때까지 차입한 자금의 금융원가를 자본화하는 것이 절대 불가능하다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 22에 따르면, 자가건설한 유형자산의 원가는 외부에서 구입한 유형자산과 동일한 기준을 적용하여 결정합니다. 따라서 자가건설에 따른 내부이익이나 자원 낭비로 인한 비정상적인 비효율 원가는 자산의 원가에 포함시키지 않고 즉시 당기손익(비용)으로 털어야 합니다.\n\n[오답 해설]\n① 자가건설 직접 노무비는 당연히 자산화됩니다.\n③ 완공 후 즉시 사용가능한 시점부터 감가상각을 즉각 개시합니다.\n④ 외주 수수료 등은 자산 형성에 기여하므로 자본화 대상입니다.\n⑤ 차입원가(제1023호) 요건 만족 시 금융원가의 자본화가 적법하게 수행됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "직접 인건비는 정상 자산화 대상이므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 22"], "principle": "자가건설 자산 취득원가 규칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "내부이익과 비정상적인 낭비 원가는 취득원가에서 확실히 배제해야 한다는 기준서 조문을 바르게 서술했습니다.", "articles": ["K-IFRS 제1016호 문단 22"], "principle": "자가건설 자산 취득원가 규칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "완공 후 사용가능해지면 즉각 감가상각을 가동합니다.", "articles": [], "principle": "자가건설 자산 취득원가 규칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "외주 용역비는 자본화 대상 취득원가입니다.", "articles": [], "principle": "자가건설 자산 취득원가 규칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입원가 자본화 기준(제1023호)에 따라 금융비용 가산이 가능하므로 오답입니다.", "articles": [], "principle": "자가건설 자산 취득원가 규칙", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "토지와 건물을 일괄 취득(Combined acquisition)한 경우, 취득 목적에 따른 취득원가 분류 배분 원칙으로 가장 옳은 것은?",
        "options": [
            "① 두 자산을 모두 사용할 목적이더라도 별도 계산 없이 전액 건물 취득원가로만 계상한다.",
            "② 토지와 건물을 모두 사용하고자 일괄 매입한 경우, 일괄 구입가격을 각 자산의 취득일 현재 공정가치 비율로 배분하여 각각 토지와 건물의 취득원가로 인식한다.",
            "③ 구건물을 철거하고 새 건물을 지을 목적이라면, 구입대금 전액을 신축 건물의 취득원가에 포함한다.",
            "④ 철거 목적으로 일괄 매입 시 발생한 구건물 철거 비용은 즉시 수선비 비용으로 당기손익에 털어낸다.",
            "⑤ 토지 및 건물은 분리가 불가능하므로 장부에 일괄자산이라는 단일 계정으로 계속 보고한다."
        ],
        "answer": "2",
        "explanation": "② 일괄 취득한 토지와 건물을 모두 사용할 목적이라면 분리 가능한 자산이므로 각각의 공정가치 비율에 따라 구입원가를 배분하여 독립된 자산(토지와 건물)으로 얹어줍니다.\n\n[오답 해설]\n① 모두 사용 시 한쪽 자산에만 얹는 것은 오답입니다.\n③, ④ 구건물 철거 목적으로 일괄 구입한 경우라면 구입비와 구건물 철거 비용 모두를 '토지'의 취득원가에 가산해야 합니다. 신축 건물 원가로 갈 수 없습니다.\n⑤ 토지는 비상각 자산이고 건물은 상각 자산이므로 반드시 구분 보고해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "모두 사용 시 일괄 쏠림 배분은 불가합니다.", "articles": [], "principle": "토지와 건물의 일괄취득 배분 규칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "토지/건물 양자 모두 가동 시 공정가치 비례 안분 적용이 정당함을 바르게 진술했습니다.", "articles": [], "principle": "토지와 건물의 일괄취득 배분 규칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "철거용 매입 시 구입대금은 신축 건물이 아닌 토지원가로 가야 하므로 틀렸습니다.", "articles": [], "principle": "토지와 건물의 일괄취득 배분 규칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "철거비는 당기 비용이 아닌 토지 취득원가에 포함합니다.", "articles": [], "principle": "토지와 건물의 일괄취득 배분 규칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "두 계정은 상각 유무가 달라 무조건 구분 기입해야 합니다.", "articles": [], "principle": "토지와 건물의 일괄취득 배분 규칙", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "토지 매입 후 토지의 사용 가치를 지속하기 위해 도로 개설, 조경 공사, 울타리 설치 등의 부대시설 공사 비용이 추가 지출되었다. 다음 중 이 지출을 '토지의 취득원가'에 가산해야 하는 합리적 판정 기준으로 옳은 것은?",
        "options": [
            "① 해당 시설의 유지보수책임이 기업에 있는 경우",
            "② 해당 시설의 내용연수가 유한하고 유지보수책임도 기업이 영구적으로 부담하는 경우",
            "③ 해당 시설의 내용연수가 영구적이거나, 유지보수책임이 지자체 또는 타인에게 있는 경우",
            "④ 해당 공사의 결제 대금을 이연하여 장기미지급금으로 보유하는 경우",
            "⑤ 공사 계약 규모가 전체 토지 구입대금의 50%를 상회할 때에만 가산한다."
        ],
        "answer": "3",
        "explanation": "③ 도로포장이나 조경공사 등 토지 부대시설의 지출은 내용연수가 영구적이거나(예: 영구 조경), 유지보수책임이 타인(지자체 등)에게 있어 기업에 내용연수 제한에 따른 감가상각 필요가 없을 때에만 '토지 취득원가'에 가산합니다.\n\n[오답 해설]\n①, ② 기업에 유지보수책임이 있고 내용연수가 한정적이라면 별도의 '구축물' 계정으로 얹은 다음 내용연수 동안 감가상각비를 인식해야 합니다.\n④, ⑤는 회계적 자산 분류의 실질적 근거가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기업에 책임이 있다면 구축물 상각 자산화합니다.", "articles": [], "principle": "토지 부대시설 회계 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "내용연수 유한 시 구축물로 갑니다.", "articles": [], "principle": "토지 부대시설 회계 분류", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "감가상각이 불필요한 조건(영구적 혹은 지자체 등 타인 유지보수 책임) 시 토지 원가에 포함함을 정확히 판정했습니다.", "articles": [], "principle": "토지 부대시설 회계 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미지급 잔액 상태는 분류와 관련 없습니다.", "articles": [], "principle": "토지 부대시설 회계 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금액 비중 비율은 구축물 구별 요건이 아니므로 오답입니다.", "articles": [], "principle": "토지 부대시설 회계 분류", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "유형자산 취득 시, 관련 법령에 의하여 지자체 등 발행 국공채를 공정가치보다 높은 가격으로 의무 매입하여 현금이 과다 유출되었다. 이때 K-IFRS 기준 상 차량운반구 등의 최초 취득원가에 반영해야 할 금액은?",
        "options": [
            "① 의무 매입한 국공채의 액면금액 전체",
            "② 의무 매입한 국공채의 매입금액과 매입 당시의 시장이자율로 평가한 공정가치(현재가치)와의 차액",
            "③ 국공채 만기 상환 시 돌려받을 미래의 만기 상환액",
            "④ 국공채의 장부금액에 인위적인 10% 이자 보상 마진을 얹은 가액",
            "⑤ 이 거래로 인한 차액은 유형자산 원가에 가산하지 않고 전액 당기비용화한다."
        ],
        "answer": "2",
        "explanation": "② 국공채를 공정가치보다 높은 가격으로 강제 의무 매입하는 경우, 매입 가격과 현재가치 할인 공정가치의 차액은 자산을 취득하기 위해 강제로 희생한 부대비용에 해당하므로 유형자산(예: 차량운반구)의 최초 취득원가에 가산합니다.\n\n[오답 해설]\n① 액면가 전체를 자산화하지 않고 시장 평가가치와 매입액의 차이만 가산합니다.\n③ 만기 상환액은 만기 회수액일 뿐입니다.\n④, ⑤는 공정가치 평가 대원칙에 저해되는 오답 진술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "액면금액 전체 가산설은 틀렸습니다.", "articles": [], "principle": "국공채 의무매입 차액 반영", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "국공채 매입액과 시장이자율 기반 공정가치와의 차이를 자산 최초 원가에 얹어주는 기준서 취지를 바르게 명시했습니다.", "articles": [], "principle": "국공채 의무매입 차액 반영", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미래 상환액은 차량 원가가 아닙니다.", "articles": [], "principle": "국공채 의무매입 차액 반영", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 가산율 적용설은 오류입니다.", "articles": [], "principle": "국공채 의무매입 차액 반영", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비용화하지 않고 유형자산 취득원가로 자본화하므로 오답입니다.", "articles": [], "principle": "국공채 의무매입 차액 반영", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "유형자산 교환취득 거래에서 '상업적 실질이 존재하는 경우(Commercial substance exists)'에 취득한 자산의 취득원가를 결정하는 원칙적인 기준은?",
        "options": [
            "① 제공한 자산의 장부금액",
            "② 취득한 자산의 공정가치가 더 명백한 경우를 제외하고는, 제공한 자산의 공정가치",
            "③ 취득한 자산의 장부금액과 제공한 자산의 공정가치의 평균치",
            "④ 정부 관서가 매년 고시하는 유형자산 법정 대체 단가",
            "⑤ 취득한 자산의 역사적 취득가"
        ],
        "answer": "2",
        "explanation": "② 교환거래에 상업적 실질이 있고 공정가치 측정이 가능하다면, 취득한 자산의 공정가치가 더 명백한 경우를 제외하고는 '제공한 자산의 공정가치'를 기준으로 취득원가를 측정합니다.\n\n[오답 해설]\n① 제공자산 장부금액은 상업적 실질이 결여되어 있거나 공정가치를 전혀 모를 때 쓰는 보충적 기준입니다.\n③ 평균치 기준은 존재하지 않습니다.\n④, ⑤는 공정가치 교환 회계 기준과 무관한 임의어입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "제공자산 장부가는 실질이 없을 때 씁니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "교환취득 상업적 실질 존재 시 원가", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "취득자산 공정가치가 더 명확한 예외를 빼고는 '제공한 자산의 공정가치'를 원가 기본값으로 둔다는 기준서 조문을 완벽히 제시했습니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "교환취득 상업적 실질 존재 시 원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평가치 평균 산정은 불허됩니다.", "articles": [], "principle": "교환취득 상업적 실질 존재 시 원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정부 법정 대체 단가는 회계상 공정가치가 아닙니다.", "articles": [], "principle": "교환취득 상업적 실질 존재 시 원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적 취득가는 교환 거래의 교환 손익 발생을 설명할 수 없으므로 오답입니다.", "articles": [], "principle": "교환취득 상업적 실질 존재 시 원가", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "유형자산 교환거래에 '상업적 실질이 결여되어 있는 경우(Commercial substance is lacked)' 취득한 유형자산의 취득원가는 제공한 자산의 무엇을 기준으로 측정하여야 하는가?",
        "options": [
            "① 제공한 자산의 취득 시 역사적원가",
            "② 제공한 자산의 교환일 현재 장부금액(Book value)",
            "③ 제공한 자산의 교환일 현재 공정가치(Fair value)",
            "④ 취득한 자산의 교환일 현재 공정가치(Fair value)",
            "⑤ 제공한 자산의 처분예상가격"
        ],
        "answer": "2",
        "explanation": "② 교환거래에 상업적 실질이 결여되어 있는 경우에는 취득한 자산의 원가를 '제공한 자산의 장부금액'으로 측정하며, 처분손익은 일절 인식하지 않습니다.\n\n[오답 해설]\n① 장부금액은 감가상각누계액 등이 차감된 잔액이므로 역사적원가와 다릅니다.\n③, ④ 공정가치 기준은 상업적 실질이 존재할 때 적용하는 원칙입니다.\n⑤ 처분예상가는 공정가치 및 장부가와 별개이므로 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "감누가 차감되지 않은 최초 원가는 장부금액이 아닙니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "교환취득 상업적 실질 결여 시 원가", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "상업적 실질이 없을 때는 교환 손익 인식을 막고 제공자산 장부금액을 새 자산 원가로 이월함을 올바르게 설명했습니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "교환취득 상업적 실질 결여 시 원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "제공자산 공정가치 적용은 실질이 존재할 때의 요건입니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "교환취득 상업적 실질 결여 시 원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득자산 공정가치 역시 실질이 있을 때의 기준입니다.", "articles": [], "principle": "교환취득 상업적 실질 결여 시 원가", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분예상가는 사용 불가한 추정치입니다.", "articles": [], "principle": "교환취득 상업적 실질 결여 시 원가", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },

    # =========================================================================
    # L2: 개념 이해 및 기준 조문 (15문항, 961~975번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s01-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "K-IFRS 제1016호에서 규정하는 유형자산의 취득원가에 포함되는 '직접관련원가(취득부대비용)'의 예시에 해당하지 않는 것은?",
        "options": [
            "① 설치장소 준비 및 공장 기초 다지기 원가",
            "② 최초의 운송 및 취급 관련 원가",
            "③ 설계 및 기계 작동 관련 전문가에게 지급하는 직접 수수료",
            "④ 유형자산이 경영진이 의도하는 방식으로 가동될 수 있으나 실제로 사용되지 않는 대기 기간 동안 발생한 운휴 관리비",
            "⑤ 유형자산이 정상적으로 작동되는지 여부를 시험하는 과정에서 발생하는 조립 및 시험가동비"
        ],
        "answer": "4",
        "explanation": "④ K-IFRS 제1016호 문단 20에 따르면, 유형자산이 경영진이 의도하는 방식으로 가동될 수 있는 장소와 상태에 이른 후에는 더 이상 원가를 인식하지 않습니다. 따라서 의도한 상태에 이르렀으나 아직 실제로 사용되지 않는 대기 기간의 운휴비는 원가에 포함될 수 없으며 즉시 비용 처리해야 합니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 기준서 문단 17에 열거된, 의도한 장소와 상태에 이르게 하기 위한 전형적인 직접관련원가 요건을 완벽히 만족합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "설치장소 준비원가는 정당한 취득부대비용입니다.", "articles": ["K-IFRS 제1016호 문단 17"], "principle": "취득부대비용의 요건 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "운송 및 취급원가 역시 취득원가에 산입됩니다.", "articles": ["K-IFRS 제1016호 문단 17"], "principle": "취득부대비용의 요건 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전문가 수수료도 가동 장소/상태 이전에 기여한 부대비용입니다.", "articles": ["K-IFRS 제1016호 문단 17"], "principle": "취득부대비용의 요건 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "사용 전 대기 기간이나 조업도 미달 가동손실 등은 사후적 지출이므로 자산화에서 전면 배제됨을 올바르게 분석했습니다.", "articles": ["K-IFRS 제1016호 문단 20"], "principle": "취득부대비용의 요건 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조립 및 작동 시험원가는 취득부대비용이 맞습니다.", "articles": ["K-IFRS 제1016호 문단 17"], "principle": "취득부대비용의 요건 판정", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "유형자산의 정상 작동 여부를 시험(Test run)하는 과정에서 생산된 시제품(예: 기계 시험 가동 시 제조된 샘플 제품)의 판매 및 원가 처리에 대한 K-IFRS의 개정된 핵심 규정은?",
        "options": [
            "① 시제품 매각대금을 시험가동비(취득부대원가)에서 전액 차감하여 유형자산 원가를 감액한다.",
            "② 시제품 매각대금과 그 재화의 원가는 취득원가에 반영하지 않고, 각각 적용 가능한 기준서에 따라 당기손익(매출 및 매출원가 등)으로 인식한다.",
            "③ 시제품 매각 금액은 당기순이익에 반영하지 않고 기타포괄손익(OCI) 재평가잉여금에 적립한다.",
            "④ 시제품 원가는 무조건 무형자산 개발비로 계상하여 장기 상각한다.",
            "⑤ 시제품 판매 행위는 부수 영업이므로 전액 이연하여 다음 연도 수익으로 소급 인식한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 20의 개정에 따라, 유형자산이 작동되는지 여부를 시험할 때 생산되는 시제품 등의 매각금액과 그 원가는 자산의 취득원가에서 차감하지 않으며, 각각 당기손익(매출과 당기비용)으로 인식합니다. 이는 과거의 매각대금 차감 관행을 폐지한 매우 중요한 개정 규칙입니다.\n\n[오답 해설]\n① 취득원가에서 차감하는 방식은 개정 전의 구 회계처리 규칙으로 오답입니다.\n③, ④, ⑤는 개정 기준서 조문과 부합하지 않는 잘못된 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "시제품 매각금액을 자산원가에서 차감하는 것은 과거의 규정으로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 20A"], "principle": "시제품 매각 및 원가 처리 개정 조문", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "시제품 판매액과 그 생산원가를 자산 차감 없이 각각 당기 매출과 매출원가 등으로 인식하도록 정하는 개정 규정을 정확히 기술했습니다.", "articles": ["K-IFRS 제1016호 문단 20A"], "principle": "시제품 매각 및 원가 처리 개정 조문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기타포괄손익 분류 대상이 아닌 일반 기간 손익 거래입니다.", "articles": ["K-IFRS 제1016호 문단 20A"], "principle": "시제품 매각 및 원가 처리 개정 조문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "생산원가는 당기 비용 또는 재고자산 원가 규정을 받으므로 무형자산 자본화는 오답입니다.", "articles": [], "principle": "시제품 매각 및 원가 처리 개정 조문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이연 처리를 강제하지 않고 발생 즉시 당기손익화하므로 틀렸습니다.", "articles": [], "principle": "시제품 매각 및 원가 처리 개정 조문", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "유형자산의 취득이나 건설 기간 중에 발생하는 '부수적인 영업(Incidental operations, 예: 공장 신축용 토지 매입 후 임시 주차장으로 운영하여 얻은 수익)'으로 인한 손익의 K-IFRS 상 올바른 회계처리 방법은?",
        "options": [
            "① 부수적인 영업의 수익과 관련 비용은 당기손익으로 각각 인식하고, 수익과 비용 항목으로 구분하여 표시한다.",
            "② 부수적 영업 수익을 토지의 최초 취득원가에서 직접 차감하여 표시한다.",
            "③ 부수적 영업 손익을 건설중인자산의 임시 차감 계정으로 적립한다.",
            "④ 부수적 영업 수익은 자본거래이므로 자본잉여금으로 직접 계상한다.",
            "⑤ 건설이 완료되는 시점에 신축건물의 취득세와 상쇄하여 순액 보고한다."
        ],
        "answer": "1",
        "explanation": "① K-IFRS 제1016호 문단 21에 따르면, 부수적인 영업은 유형자산을 경영진이 의도하는 방식으로 가동하는 데 필수적인 활동이 아니므로, 그러한 수익과 관련 비용은 자산 원가에 묻지 않고 당기손익의 수익과 비용으로 각각 인식하여 분리 보고하여야 합니다.\n\n[오답 해설]\n② 자산 취득원가에서 차감하는 것은 기준서 위배입니다.\n③, ⑤ 임시 차감 또는 건물 취득세와의 상쇄는 허용되지 않는 잘못된 순액 회계처리입니다.\n④ 주주와의 거래가 아니므로 자본 거래가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "부수적 영업은 자산 취득에 필수적이지 않으므로 손익계산서 상 수익/비용으로 별도 인식한다는 기준서의 규정을 올바르게 지목했습니다.", "articles": ["K-IFRS 제1016호 문단 21"], "principle": "부수적 영업손익의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 취득원가(토지나 건설중인자산)에서 차감하지 않으므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 21"], "principle": "부수적 영업손익의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산원가에 영향을 주지 않으므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 21"], "principle": "부수적 영업손익의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일반 당기 영업외수익 등에 속하므로 자본 거래가 아닙니다.", "articles": [], "principle": "부수적 영업손익의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "건물원가 상쇄 처리는 분개상 오류입니다.", "articles": [], "principle": "부수적 영업손익의 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "유형자산의 구입 대금 결제를 일반적인 신용기간을 초과하여 장기로 연기하는 장기할부 조건으로 구매하였다. 이 경우 K-IFRS 기준 상 취득원가와 금융비용 결정 규칙은?",
        "options": [
            "① 미래에 지불할 모든 할부금 총액을 더하여 즉시 취득원가로 계상한다.",
            "② 구입 대금의 최초 현금가격상당액을 취득원가로 하고, 현금가격상당액과 실제 총지급액과의 차액은 이연 신용기간에 걸쳐 이자비용(금융원가)으로 인식한다.",
            "③ 할부이자 상당액은 자산의 감가상각 내용연수 동안 감상비에 얹어 인식한다.",
            "④ 현금가격상당액과 총액의 차액을 전액 취득일 당일에 영업외비용으로 즉각 인식한다.",
            "⑤ 대금 지급 전에는 자산으로 인식하지 못하며, 할부금이 다 완납되는 날 자산으로 등재한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 23에 따라 이연 조건 취득 시 원가는 현금가격상당액이며, 총지급액과의 차액(이자상당액)은 차입원가 자본화 요건에 부합하여 자산화하지 않는 한 신용기간 동안 이자비용으로 기간 배분 배부하여 인식합니다.\n\n[오답 해설]\n① 명목상 할부총액을 자산으로 잡는 것은 현재가치 평가 생략 오류입니다.\n③ 이자비용은 이자 인식 기간에 걸쳐 금융비용으로 가야 하며 감가상각과 무관합니다.\n④ 취득일 당일 일시 비용이 아닌 이자 인식 기간 동안 유효이자율법 등으로 나누어 비용화합니다.\n⑤ 사용가능하고 통제하면 대금 결제 유무와 상관없이 결산일 자산으로 올립니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "할부 원금과 이자를 섞은 총액을 원가로 올리면 현재가치 왜곡이 발생합니다.", "articles": ["K-IFRS 제1016호 문단 23"], "principle": "이연지급조건 하의 원가 결정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "취득원가를 현금상당액으로 끊고 차액은 신용기간 동안 유효이자율법 등으로 이자비용화한다는 원칙을 정밀히 묘사했습니다.", "articles": ["K-IFRS 제1016호 문단 23"], "principle": "이연지급조건 하의 원가 결정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자 비용은 감가상각 계정에 섞일 수 없는 금융비용입니다.", "articles": ["K-IFRS 제1016호 문단 23"], "principle": "이연지급조건 하의 원가 결정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일시 비용이 아닌 기간 귀속 비용입니다.", "articles": ["K-IFRS 제1016호 문단 23"], "principle": "이연지급조건 하의 원가 결정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "완납 전 통제 개시 시점에 이미 유형자산 인식 요건을 충족합니다.", "articles": [], "principle": "이연지급조건 하의 원가 결정", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "유형자산 취득에 필수적으로 수반되는 법정 의무 국공채 의무매입 시, 채권 매입가액과 시장이자율 현재가치(공정가치)의 차액을 자산원가에 가산하는 회계학적 실질과 정당성은?",
        "options": [
            "① 회사가 채권을 싼 가격에 사와 금융이익을 얻었으므로 유형자산 가치를 감액하려는 취지이다.",
            "② 해당 자산을 취득 및 사용 가능한 상태로 만들기 위해 국공채 매입으로 인한 '자금의 기회 손실(초과 지급액)'이 필수적으로 수반되었으므로, 이를 취득부대비용으로 보아 자산화하는 것이 정당하다.",
            "③ 채권은 만기에 상환되므로 투자 수익의 일부를 임의 분할하여 비용을 줄이려는 조치이다.",
            "④ 지자체에 기부한 기부금과 동일하므로 판관비 기부금 항목으로 전액 처리하는 것이 타당하다.",
            "⑤ 국공채 매입 차액은 주주와의 거래로 보아 자본조정 계정으로 이체하려는 배려이다."
        ],
        "answer": "2",
        "explanation": "② 국공채를 공정가치(현재가치)보다 비싼 액면가격으로 의무 매입함에 따라 발생한 초과 지출은 차량 등 유형자산을 취득하기 위해 필수불가결하게 치른 희생이므로, 취득에 직접 관련된 부대비용의 실질을 지닙니다. 따라서 이를 유형자산의 취득원가에 포함하는 것이 자산 측정 이론 상 타당합니다.\n\n[오답 해설]\n① 싼 가격이 아니라 공정가치보다 비싼 가격에 강제 매입하므로 자금의 손실이 발생한 것입니다.\n③ 채권 투자는 금융자산 계정으로 만기까지 관리되며 자산 가치 상환과는 별개입니다.\n④, ⑤ 기부금이나 주주 거래 성격이 아닌 유형자산 취득에 기여한 직접 부대비용입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비싼 가격에 매입하므로 자금 손실 실질을 지닙니다.", "articles": [], "principle": "국공채 의무매입 차액의 회계 실질", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산을 정상 취득하기 위해 피치 못하게 발생한 국공채 과다 지출액을 직접관련 부대비용으로 인정하여 유형자산 원가에 얹는 논리적 근거를 바르게 설명했습니다.", "articles": [], "principle": "국공채 의무매입 차액의 회계 실질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "투자 이익의 기간 배분 조항이 아닙니다.", "articles": [], "principle": "국공채 의무매입 차액의 회계 실질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기부금이 아닌 취득 자산의 자본화 원가 요건에 해당합니다.", "articles": [], "principle": "국공채 의무매입 차액의 회계 실질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주주 지분 거래가 아닙니다.", "articles": [], "principle": "국공채 의무매입 차액의 회계 실질", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "유형자산 최초 인식 시, 자산을 해체, 제거하거나 부지를 복구하는 데 소요될 것으로 최초에 추정되는 원가(복구원가)의 K-IFRS 기준 상 회계처리 규칙으로 가장 옳은 것은?",
        "options": [
            "① 복구 의무는 미래의 불확실한 사건이므로 실제 복구 비용이 지출되는 수십 년 뒤 시점에만 비용 처리한다.",
            "② 복구원가의 미래 예상 지출 총액을 아무런 할인 없이 그대로 취득원가에 전액 합산한다.",
            "③ 복구원가의 현재가치를 합리적으로 추정하여 유형자산 최초 취득원가에 포함하고, 상대 계정으로 '복구충당부채'를 인식한다.",
            "④ 복구 비용 예상액은 전액 당기비용 영업외비용으로 취득 당일 일시 처리하고 충당부채는 생략한다.",
            "⑤ 복구의무는 부채 계상이 불가능하므로 주석으로만 공시하고 기말 평가에서 제외한다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1016호 문단 16 등에 따라, 자산을 해체, 제거하거나 부지를 복구하는 데 소요될 것으로 최초에 추정되는 복구원가는 유형자산의 취득원가를 구성합니다. 이 경우 미래 복구 의무액을 적절한 할인율로 할인한 현재가치만큼 자산원가에 포함하고 동시에 대변에 '복구충당부채'로 인식합니다.\n\n[오답 해설]\n① 지출 시점이 아닌 최초 취득 시점에 충당부채와 자산을 선계상해야 하므로 오답입니다.\n② 시간가치를 고려해야 하므로 명목 총액을 할인 없이 그냥 더하는 것은 오류입니다.\n④, ⑤ 충당부채 계상과 자산 원가 산입이 모두 강제되는 조항이므로 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "실제 지출 시점까지 인식을 지연시키면 자산과 부채의 적시 보고가 누락됩니다.", "articles": ["K-IFRS 제1016호 문단 16"], "principle": "복구원가의 최초 인식 규칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "명목가 누적 합산은 현재가치 측정 원칙 위배입니다.", "articles": ["K-IFRS 제1016호 문단 16"], "principle": "복구원가의 최초 인식 규칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "복구의무의 추정액 현재가치를 유형자산 취득원가와 복구충당부채로 동시에 적시 계상하도록 정하는 원칙을 바르게 설명했습니다.", "articles": ["K-IFRS 제1016호 문단 16"], "principle": "복구원가의 최초 인식 규칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당일 일시 비용화가 아닌 자본화 후 내용연수 상각 구조를 밟으므로 오답입니다.", "articles": [], "principle": "복구원가의 최초 인식 규칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "충당부채 정식 계상 대상이므로 주석 전용설은 틀렸습니다.", "articles": [], "principle": "복구원가의 최초 인식 규칙", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "유형자산이 경영진이 의도하는 방식으로 가동될 수 있는 장소와 상태에 이른 '이후'에 발생한 추가 지출 중, 예외 없이 당기 비용으로 비용 처리해야 하는 성격에 해당하지 않는 것은?",
        "options": [
            "① 자산이 가동될 준비가 되었으나 실제로 영업에 투입되지 않는 대기 기간의 기계 유지관리 원가",
            "② 정상 조업도에 미달하여 완전 가동 수준에 이르기까지 발생하는 가동손실",
            "③ 유형자산 산출물에 대한 수요가 본격적으로 형성되는 과정에서 겪은 초기의 가동 손실액",
            "④ 기업의 영업 전부 또는 일부를 재배치하거나 재편성하는 과정에서 발생한 이사 및 재배치 비용",
            "⑤ 취득 즉시 자산의 미래경제적효익 유입가능성을 유의적으로 높이고 자산의 생산 능력을 획기적으로 개선하기 위해 필수 지출된 엘리베이터 증설 원가"
        ],
        "answer": "5",
        "explanation": "⑤ 5번의 지출은 최초 취득 완료 사후에 발생했으나 자산의 성능 개선, 생산 능력 향상 등을 가져오는 자본적 지출(유형자산 후속 원가 요건)에 해당하므로, 유형자산의 장부금액(자산 원가)에 가산하여 후속 상각할 수 있는 적격 자산화 대상입니다. 즉, 당기비용으로만 털어야 하는 대상이 아닙니다.\n\n[오답 해설]\n①, ②, ③, ④는 K-IFRS 제1016호 문단 20에 따라 의도한 장소/상태 도달 후에 사용 연기, 조업도 미달, 초기가동, 재배치 등으로 발생한 원가들이므로 장부금액에 포함할 수 없고 무조건 당기비용 처리해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "사용 전 대기 기간 원가는 당기 비용 대상입니다.", "articles": ["K-IFRS 제1016호 문단 20"], "principle": "사후 비용화 대상 여부 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조업도 미달 손실은 자산화가 차단되는 비용입니다.", "articles": ["K-IFRS 제1016호 문단 20"], "principle": "사후 비용화 대상 여부 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수요 형성 과정의 초기 손실도 자산화 불가 비용입니다.", "articles": ["K-IFRS 제1016호 문단 20"], "principle": "사후 비용화 대상 여부 판정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업 재배치/재편성 이사 비용은 전액 비용 처리 대상입니다.", "articles": ["K-IFRS 제1016호 문단 20"], "principle": "사후 비용화 대상 여부 판정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "미래경제적효익 유입을 유의적으로 높이는 자본적 사후 지출은 당기비용이 아닌 유형자산 후속 원가로 적격 자산화됨을 명확히 구분해냈습니다.", "articles": ["K-IFRS 제1016호 문단 12, 13"], "principle": "사후 비용화 대상 여부 판정", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "K-IFRS 제1016호 기준서에 부합하는 자가건설 유형자산의 차입원가(Borrowing costs) 자본화 처리에 관한 올바른 규정은?",
        "options": [
            "① 자가건설 기간 중에 발생한 건설자금 차입 이자는 적격성 여부와 무관하게 전액 영업외비용으로만 기입해야 한다.",
            "② 의도된 용도로 사용 가능하게 만드는 데 상당한 기간이 소요되는 '적격자산' 요건을 충족하는 자가건설의 경우, 취득 자금 관련 차입원가를 자산원가에 산입(자본화)한다.",
            "③ 건설이 완전히 완공된 사후 대기 기간 동안 발생한 대출이자까지 건물의 원가에 무제한 누적 가산한다.",
            "④ 금융원가 자본화 금액은 전액 기타포괄손익(OCI)으로 축적하여 차기 주주배당금과 연동 상각한다.",
            "⑤ 자가건설 금융원가는 재고자산 금융원가와 평균 비율을 도출하여 영업비용으로 일괄 털어낸다."
        ],
        "answer": "2",
        "explanation": "② 자가건설 유형자산의 취득, 건설 및 제조와 직접 관련된 차입원가(금융원가)는 해당 자산이 의도된 용도로 사용 또는 판매 가능한 상태에 이르게 하는 데 상당한 기간을 요하는 '적격자산'에 해당할 경우, K-IFRS 제1023호 '차입원가'에 따라 자산원가에 포함(자본화)해야 합니다.\n\n[오답 해설]\n① 적격자산 요건 충족 시 금융비용의 자산화가 의무적이므로 일괄 비용설은 틀렸습니다.\n③ 자산이 의도한 방식으로 가동 가능한 상태에 이른 시점(완공일 등)에 차입원가 자본화를 지체 없이 중단해야 하므로 사후 이자 가산은 위법합니다.\n④, ⑤는 기준서 외의 엉터리 자본/영업 융합 오답 가설입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "적격 자산 요건 하의 금융 비용 자산화를 무시하여 오답입니다.", "articles": ["K-IFRS 제1016호 문단 22", "K-IFRS 제1023호 문단 8"], "principle": "자가건설 시 차입원가 자본화 조문", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "건설 완료 전까지 적격 자산용 대출 이자비용을 자산 취득원가에 포함(자본화)하는 제1023호 연계 규칙을 바르게 서술했습니다.", "articles": ["K-IFRS 제1016호 문단 22", "K-IFRS 제1023호 문단 8"], "principle": "자가건설 시 차입원가 자본화 조문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "완공 후 사용 가능 시점부터 이자 자본화를 전면 중단해야 하므로 오답입니다.", "articles": ["K-IFRS 제1023호 문단 22"], "principle": "자가건설 시 차입원가 자본화 조문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "OCI 배분이나 주주 환원은 불가능한 분개 왜곡입니다.", "articles": [], "principle": "자가건설 시 차입원가 자본화 조문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융비용 평균화 영업비용화 주장은 오답입니다.", "articles": [], "principle": "자가건설 시 차입원가 자본화 조문", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "유형자산 인식기준을 개별 자산단위별로 융통성 있게 적용하는 '인식 요건의 완화 및 예외 실무 지침'에 관한 K-IFRS의 입장으로 가장 올바른 것은?",
        "options": [
            "① 공구나 금형 등 개별적으로 경미하고 금액이 소액인 비품은 절대 개별 유형자산으로 등재할 수 없으며 무조건 판관비 비용으로만 처리해야 한다.",
            "② 공구, 형판, 금형 등 경미한 항목은 개별적으로 인식기준을 적용하지 않고, 이들을 통합하여 하나의 자산(유형자산 등)으로 묶어 인식기준을 적용할 수 있다.",
            "③ 소액의 보수용 예비부품이나 대기성 장비는 사용 여부와 무관하게 무조건 취득일 당일 재고자산으로만 인식해야 한다.",
            "④ 모든 비품은 아무리 소액이라도 공정가치 재평가 대상을 100% 매월 수행하여 보고해야 한다.",
            "⑤ 회사는 자산 분류 단위를 마음대로 조절하여 유형자산을 투자주식 계정으로 통합 보고할 수 있다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 9에 의하면, 기준서는 자산을 인식하는 단위(즉, 무엇이 유형자산의 일 항목을 구성하는지)를 규정하지 않습니다. 따라서 공구, 형판, 금형 등 개별적으로 경미한 항목들에 대하여 통합된 총가치에 기초하여 인식기준을 적용하는 것이 적절할 수 있다고 유연성을 허용합니다.\n\n[오답 해설]\n① 소액 자산도 통합하여 유형자산으로 잡을 수 있는 실무적 예외가 인정되므로 비용 강제설은 오답입니다.\n③ 예비부품이나 대기성 장비가 유형자산 정의를 충족하면 재고가 아닌 유형자산으로 계상합니다.\n④, ⑤는 비교가능성을 침해하는 가공의 재평가/계정 분류 쪼개기 주장입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "소액 비품이라도 통합 적용을 통해 유형자산 계상이 가능하므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 9"], "principle": "유형자산 인식 기준의 유연성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "경미한 소액 품목들을 하나로 묶어 결합 자산으로 유형자산화하는 통합 인식 지침을 정합적으로 설명했습니다.", "articles": ["K-IFRS 제1016호 문단 9"], "principle": "유형자산 인식 기준의 유연성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "예비부품이 1년을 초과하여 장기 사용될 목적이면 재고가 아닌 유형자산입니다.", "articles": ["K-IFRS 제1016호 문단 8"], "principle": "유형자산 인식 기준의 유연성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소액 비품에 대한 매월 강제 공정가치 평가는 규정에 없습니다.", "articles": [], "principle": "유형자산 인식 기준의 유연성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금융 상품이나 투자 자산과의 통합 분류는 기준서 위반입니다.", "articles": [], "principle": "유형자산 인식 기준의 유연성", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "토지 취득 후 건설한 진입 도로, 담장(울타리), 주차장 등의 토지 부대시설 중, 내용연수가 제한되어 있고 유지보수책임이 전적으로 '당사(기업)'에 귀속되는 시설들의 올바른 회계적 자산 분류와 감가상각 처리 방법은?",
        "options": [
            "① 수명이 유한하더라도 토지에 직접 부착되어 분리할 수 없으므로 비상각 자산인 '토지'의 취득원가에 포함한다.",
            "② 해당 지출 총액을 토지원가에서 차감하는 차감적 평가 계정으로 표시한다.",
            "③ 토지와 별개의 상각 대상 유형자산인 '구축물'로 인식하고, 해당 부대시설의 내용연수 동안 체계적으로 감가상각비를 인식한다.",
            "④ 주주에 대한 이익 배분액으로 보아 자본조정 항목으로 직접 적립한다.",
            "⑤ 이 지출은 자산화가 불가능하며 발생 연도에 즉시 판관비 지급수수료로 털어낸다."
        ],
        "answer": "3",
        "explanation": "③ 내용연수가 유한하고 유지보수책임이 기업에 있는 도로포장, 울타리, 하수도 등의 토지 부대시설은 토지와 성격이 다른 별개의 감가상각 대상 유형자산인 '구축물'로 장부에 반영한 다음, 그 시설의 추정 내용연수 동안 감가상각하여 기간 비용화합니다.\n\n[오답 해설]\n① 내용연수가 영구적이거나 유지보수책임이 지자체 등에 있을 때만 비상각 자산인 토지 원가에 가산합니다.\n②, ④, ⑤는 자산의 감가상각 회계 실질 및 계정과목 분류 규칙을 무시한 틀린 보기들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상각 성격을 띤 유한성 자산이므로 비상각 토지원가 합산은 불허됩니다.", "articles": [], "principle": "토지 부대시설의 분류 실질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "토지 차감계정이 아니므로 오답입니다.", "articles": [], "principle": "토지 부대시설의 분류 실질", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수명 제한 및 관리 책임이 기업에 있는 부대설비는 구축물로 분류하여 별도 감가상각한다는 논리를 바르게 설명했습니다.", "articles": [], "principle": "토지 부대시설의 분류 실질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본조정거래가 아니므로 틀렸습니다.", "articles": [], "principle": "토지 부대시설의 분류 실질", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당일 일시 비용화가 아닌 자본화 후 상각 대상이므로 오답입니다.", "articles": [], "principle": "토지 부대시설의 분류 실질", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "기존 건물이 서 있는 토지를 신축(새 건물 건설) 목적으로 일괄 일시 매입한 뒤, 기존 건물을 즉시 철거하는 경우 구건물의 철거 과정에서 회수한 폐자재(고철 등)의 매각 대금은 어떻게 회계처리하여야 하는가?",
        "options": [
            "① 전액 당기 잡이익(영업외수익)으로 영업수익 계상한다.",
            "② 토지의 취득원가(자산 금액)에서 차감하여 반영한다.",
            "③ 새로 짓는 신축건물의 취득세 세액 공제 재원으로 유보한다.",
            "④ 건설중인자산의 평가이익 과목으로 이체하여 기말 환입한다.",
            "⑤ 회사의 자본총계 내 자본조정(자기주식 등)으로 적립한다."
        ],
        "answer": "2",
        "explanation": "② 기존 건물이 있는 토지를 일괄 매입한 후 즉시 철거하는 경우, 일괄 구입비와 철거 비용 모두 토지를 사용가능한 상태로 만들기 위해 유출된 토지 취득원가에 해당합니다. 이때 구건물 철거 시 회수한 폐자재의 처분 매각수익은 토지 취득을 위해 지출된 희생을 일부 보전받은 성격이므로, 토지의 취득원가에서 차감하여 반영합니다.\n\n[오답 해설]\n① 당기손익(잡수익)으로 인식하지 않고 토지원가를 줄여줍니다.\n③, ④, ⑤는 신축건물, 건설중인자산, 혹은 자본 거래로 오도한 잘못된 분개설입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "잡이익으로 영업외수익 처리하지 않고 토지 가액에서 직접 뺍니다.", "articles": [], "principle": "철거 폐자재 수익의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "철거비용이 토지원가에 포함되듯 철거 과정의 부산물 매각대금은 토지의 최초 취득원가에서 차감 조정해야 함을 바르게 서술했습니다.", "articles": [], "principle": "철거 폐자재 수익의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "신축건물 취득세와 무관한 토지 취득 사안입니다.", "articles": [], "principle": "철거 폐자재 수익의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "건설중인자산 계정으로의 이입은 불가합니다.", "articles": [], "principle": "철거 폐자재 수익의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 거래가 아닙니다.", "articles": [], "principle": "철거 폐자재 수익의 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "유형자산 교환거래에 있어 상업적 실질(Commercial substance) 유무 판정에 따라, 교환처분손익(교환에 따른 처분이익 또는 손실)의 손익계산서 인식 여부가 어떻게 결정되는가?",
        "options": [
            "① 상업적 실질의 유무와 상관없이 어떠한 교환거래에서도 교환처분손익은 절대 인식할 수 없다.",
            "② 상업적 실질이 존재하는 교환거래에 한하여 교환처분손익을 인식하며, 상업적 실질이 결여되어 있다면 교환처분손익을 인식하지 않는다(0원).",
            "③ 상업적 실질이 없을 때에만 교환처분이익을 당기수익으로 인식하고, 있을 때는 이연한다.",
            "④ 상업적 실질 유무와 무관하게 모든 교환거래는 무조건 공정가치로 강제 분개하여 동일하게 처분손익을 인식한다.",
            "⑤ 처분손익은 기타포괄손익(OCI)으로만 올려서 재평가잉여금으로 영구 보존한다."
        ],
        "answer": "2",
        "explanation": "② 교환거래에 상업적 실질이 존재하는 경우에는 거래 실질이 실현되었다고 보아 제공자산의 공정가치와 장부금액 대조를 통한 교환처분손익을 인식합니다. 반면, 상업적 실질이 결여되어 있는 경우에는 단지 장부금액의 연속에 불과하므로 취득원가를 제공자산 장부금액으로 삼고 처분손익은 일절 계상하지 않습니다.\n\n[오답 해설]\n① 실질 존재 시 손익 인식이 가능하므로 오답입니다.\n③, ④, ⑤는 실질의 정의 및 발생 손익 귀속에 관한 기준서 논리를 왜곡한 틀린 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상업적 실질 존재 시 처분손익 인식이 허용됩니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "교환취득 상업적 실질별 처분손익 귀속", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "실질 존재 시 처분손익 계상, 실질 결여 시 장부가가 이월되어 손익 인식이 0이 된다는 원칙을 정확하게 설명했습니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "교환취득 상업적 실질별 처분손익 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상업적 실질이 없는 상태에서의 손익 임의 계상은 불인정됩니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "교환취득 상업적 실질별 처분손익 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실질 유무에 따라 대우가 엄격히 구별되므로 오답입니다.", "articles": [], "principle": "교환취득 상업적 실질별 처분손익 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당기순이익(처분손익)으로 귀속되므로 OCI 누적설은 틀렸습니다.", "articles": [], "principle": "교환취득 상업적 실질별 처분손익 귀속", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "상업적 실질이 존재하는 교환거래라 하더라도, 제공한 자산과 취득한 자산 모두의 공정가치를 신뢰성 있게 측정할 수 없는 특수한 경우에 적용해야 하는 취득원가 및 처분손익 기준은?",
        "options": [
            "① 자산의 원가는 제공한 자산의 장부금액으로 측정하고, 처분손익은 인식하지 않는다.",
            "② 어차피 실질이 있으므로 감정평가사의 임의 감정액을 공정가치로 강제 대용하여 처분손익을 억지로 인식한다.",
            "③ 자산의 원가는 취득세 신고 가액으로 측정하고, 기부금 손실을 인식한다.",
            "④ 취득원가는 0원으로 간주하고, 제공한 자산의 장부금액 전체를 처분손실로 인식한다.",
            "⑤ 두 자산의 공정가치 평균값으로 원가를 가상 갱신한다."
        ],
        "answer": "1",
        "explanation": "① K-IFRS 제1016호 문단 24에 따르면, 취득한 자산과 제공한 자산 모두의 공정가치를 신뢰성 있게 측정할 수 없는 경우의 취득원가는 '제공한 자산의 장부금액'으로 측정하며, 교환에 따른 처분손익은 발생하지 않습니다. 즉, 상업적 실질이 결여된 경우와 동일한 측정 경로를 밟게 됩니다.\n\n[오답 해설]\n②, ③, ④, ⑤는 공정가치 측정 신뢰성 상실 시 무리하게 대체치를 작위하여 왜곡을 키우는 불허되는 엉터리 가설입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "공정가치 불능 시 제공자산 장부금액으로 원가를 유도하고 처분손익은 인식하지 않는다는 규정을 정합적으로 진술했습니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "양자 공정가치 측정 불능 시 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "추정이 극히 불가능한 상황에서 억지 시가 평가는 불가하므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 24"], "principle": "양자 공정가치 측정 불능 시 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "취득세 기준은 기업회계기준 상 취득원가 유도 방식이 아닙니다.", "articles": [], "principle": "양자 공정가치 측정 불능 시 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 0원 고정 및 강제 손실 계상 주장은 오류입니다.", "articles": [], "principle": "양자 공정가치 측정 불능 시 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가상 평균값 적용은 기준서와 무관합니다.", "articles": [], "principle": "양자 공정가치 측정 불능 시 처리", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "K-IFRS 제1016호 '유형자산'에 규정된, 교환거래가 '상업적 실질(Commercial substance)'을 갖는지 여부를 판정하기 위한 조건으로 가장 타당하지 않은 것은?",
        "options": [
            "① 취득한 자산과 제공한 자산의 현금흐름의 구성(위험, 타이밍, 금액)에 유의적인 차이가 있다.",
            "② 교환거래의 영향을 받는 영업부분의 기업특유가치(Entity-specific value)가 변동한다.",
            "③ 자산의 물리적 기능이나 제조원가가 완전히 일치하여 교환 전후 기업의 생산 라인이 그대로 동일하게 영위된다.",
            "④ 상업적 실질 판정 조건 중 (1)번이나 (2)번의 차이가 교환된 자산의 공정가치에 비하여 유의적이다.",
            "⑤ 교환 대상 자산 간의 현금흐름의 유의적인 타이밍 및 위험 구조 변동으로 인해 기업의 순자산 가치가 달라진다."
        ],
        "answer": "3",
        "explanation": "③ 교환 후에도 자산의 기능이나 회사의 현금흐름에 아무런 실질적 변화(차이)가 없어 생산 라인이 그대로 똑같이 이어진다면, 이는 경제적 상태가 변하지 않았으므로 상업적 실질이 결여되어 있는 대표적인 정황에 해당합니다. 실질이 존재하기 위한 요건이 결코 아닙니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 K-IFRS 제1016호 문단 25에 규정된, 상업적 실질을 인정하기 위한 세부 기준 조건들의 정당한 서술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "위험, 타이밍, 금액 차이는 상업적 실질의 기본 판정 요건입니다.", "articles": ["K-IFRS 제1016호 문단 25"], "principle": "상업적 실질의 판정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기업특유가치의 변동 또한 조문상 중요 요건입니다.", "articles": ["K-IFRS 제1016호 문단 25"], "principle": "상업적 실질의 판정 기준", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "변화가 전혀 없어 자산의 경제적 실질 상태가 이전과 완전히 동일하다면 상업적 실질이 없음을 명확하게 구분하여 답했습니다.", "articles": ["K-IFRS 제1016호 문단 25"], "principle": "상업적 실질의 판정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차이의 유의성 검토 요건도 규정에 기재되어 있습니다.", "articles": ["K-IFRS 제1016호 문단 25"], "principle": "상업적 실질의 판정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금흐름 구조 변화를 통한 실질성 입증 설명입니다.", "articles": ["K-IFRS 제1016호 문단 25"], "principle": "상업적 실질의 판정 기준", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s01-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "유형자산의 취득원가 중 감가상각 적용단위에 관한 K-IFRS 기준서의 지침으로 가장 옳은 설명은?",
        "options": [
            "① 유형자산은 어떠한 경우에도 전체를 하나의 단일 자산으로만 묶어 평균 내용연수로 감가상각하여야 하며 개별 부속 부품 단위 상각은 불허한다.",
            "② 유형자산을 구성하는 일부의 원가가 당해 유형자산의 전체원가에 비교하여 유의적이라 하더라도, 부품별 분리 감가상각은 실무 상 금지된다.",
            "③ 유형자산을 구성하는 일부의 원가가 당해 유형자산의 전체원가에 비교하여 유의적이라면, 해당 유형자산을 감가상각할 때 그 부분은 별도로 구분하여 감가상각한다.",
            "④ 유의적이지 않은 부분에 대해서는 어떠한 경우에도 분리 상각이 차단된다.",
            "⑤ 항공기의 엔진이나 동체처럼 원가 비중이 높은 경우에도 반드시 단일 항공기 정액법으로 통일 상각한다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1016호 문단 43에 명시된 바와 같이, 유형자산의 유의적인 일부 원가를 가진 부분은 반드시 별도로 분리하여 독립적으로 감가상각하여야 합니다. 예를 들어, 항공기의 동체와 엔진은 원가 비중이 크고 수명이 다르므로 분상 상각해야 합니다.\n\n[오답 해설]\n①, ②, ⑤ 분상 상각(Component depreciation)은 기준서에서 강제하는 사항이므로 단일 일괄 상각 강제설은 모두 오답입니다.\n④ 전체 원가에 비해 유의적이지 않은 부분이라도 기업의 선택에 따라 별도로 분리하여 상각할 수 있는 여지가 열려 있으므로(문단 45) 차단 진술은 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "구성요소별 감가상각이 의무화되어 있으므로 틀렸습니다.", "articles": ["K-IFRS 제1016호 문단 43"], "principle": "구성요소별 감가상각 조문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부품별 분리 상각이 권장 및 강제되는 조항이므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 43"], "principle": "구성요소별 감가상각 조문", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "전체 원가 대비 유의적인 일부 원가 구성요소는 독자적으로 상각단위를 구분해 감가상각비를 매겨야 한다는 기준서 규정을 완벽하게 명시했습니다.", "articles": ["K-IFRS 제1016호 문단 43"], "principle": "구성요소별 감가상각 조문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유의적이지 않은 경미한 부분도 자율적으로 분리 상각할 수 있습니다.", "articles": ["K-IFRS 제1016호 문단 45"], "principle": "구성요소별 감가상각 조문", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "엔진과 동체는 전형적인 성분별 상각 대상 항목입니다.", "articles": ["K-IFRS 제1016호 문단 43"], "principle": "구성요소별 감가상각 조문", "case": {"holding": "", "no": None}}
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
                "item": "1절 유형자산의 인식 및 최초측정"
            }
        }
    }
]

questions.extend(part1_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(part1_questions)} new questions (Part 1). Total questions in questions_db_accounting.json: {len(questions)}")
