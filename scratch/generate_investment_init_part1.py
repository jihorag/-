# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "questions_db_accounting.json"

if not DB_PATH.exists():
    print(f"Error: {DB_PATH} not found.")
    exit(1)

with open(DB_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded database with {len(questions)} questions.")

taxonomy = {
    "subject": "회계학",
    "sub_subject": "재무회계",
    "chapter": "제2장 자산",
    "section": "Chapter 06 투자부동산",
    "item": "2절 투자부동산의 최초측정"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q1451 ~ Q1460) ---
    {
        "id": "practice-accounting-ch06s02-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1040호 '투자부동산'에 따라 투자부동산을 최초로 인식하는 시점의 측정 기준으로 가장 올바른 것은?",
        "options": [
            "① 역사적 공정가치(Historical Fair Value)로 측정하며 거래원가는 즉시 당기손실 처리한다.",
            "② 취득원가(Cost)로 측정하며, 취득을 위해 발생한 거래원가(Transaction costs)도 취득원가에 포함한다.",
            "③ 순실현가능가치(Net Realizable Value)로 측정하며 부대비용은 전액 비용 처리한다.",
            "④ 기말 현재의 대체원가(Replacement Cost)로 측정한다.",
            "⑤ 회수가능액(Recoverable Amount)과 사용가치 중 작은 금액으로 측정한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1040호 문단 20에 따라, 투자부동산은 최초 인식시점에 취득원가(Cost)로 측정합니다. 또한 취득 거래를 위해 직접적으로 유입 발생한 거래원가(중개 수수료, 취득세 등)는 취득원가에 당연히 포함됩니다.\n\n[오답 해설]\n① 최초 측정은 공정가치가 아닌 취득원가가 대원칙이며, 거래원가는 취득원가에 자본화해야 하므로 틀렸습니다.\n③ 순실현가능가치는 재고자산의 기말평가 기준입니다.\n④ 대체원가는 재조달원가 개념으로 최초 측정법이 아닙니다.\n⑤ 회수가능액과 사용가치는 기말 손상평가 단계에서 적용되는 속성입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "다음 중 K-IFRS 제1040호에 따라 투자부동산의 최초 취득원가에 포함될 수 있는 직접 관련 지출(거래원가)에 해당하지 않는 것은?",
        "options": [
            "① 부동산 취득 시 발생한 법률용역수수료",
            "② 소유권 이전과 직접 관련된 지방세(취득세 등)",
            "③ 부동산 중개인에게 지급한 거래 수수료",
            "④ 부동산 매입 협상을 위해 출장을 다녀온 직원들의 교통비 및 식대",
            "⑤ 기존 건물을 등기 이전하기 위해 대리인에게 지급한 위임 수수료"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 부동산 매입 협상 등 취득 거래 이전에 발생한 일반적인 직원 출장비, 통신비, 내부 행정비 등은 자산의 취득 활동에 직접 관련시켜 추적하기 어려우므로 당기 비용으로 처리해야 하며 취득원가에 가산하지 않습니다.\n\n[오답 해설]\n①, ②, ③, ⑤ 법률용역비, 취득세, 부동산중개수수료, 등기 대리 위임수수료는 모두 부동산 거래를 성사시키기 위해 직접 투입된 거래원가로서 취득원가 가산 대상입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "투자부동산을 취득 및 건설하는 과정에서 발생하는 지출 중, K-IFRS 제1040호에서 명시적으로 '투자부동산의 취득원가에서 제외(당기비용 처리)'하도록 규정하고 있는 항목은?",
        "options": [
            "① 부동산 소유권을 취득하면서 발생한 법적 등록세",
            "② 해당 부동산을 매입하기 위해 중개소에 직접 송금한 복비",
            "③ 영업을 개시하기 전에 발생한 초기 개업비(Start-up costs)",
            "④ 토지 경계선 확정을 위한 법률 대리 지출액",
            "⑤ 노후 건물의 사용 권리를 양도받으면서 대납한 전 소유자의 지방세 체납분"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1040호 문단 23에 따라, 경영진이 의도하는 방식으로 부동산을 운영할 수 있는 상태에 이르게 하는 데 직접 관련이 없는 '초기 개업비(시업비)'는 자산의 취득원가에 포함되지 않고 전액 발생 즉시 비용 처리합니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 부동산 취득과 등기를 완료하기 위해 회피 불가능하게 직접 지출된 비용들이므로 모두 취득원가에 산입해야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "자가건설 투자부동산의 개발 및 신축 과정에서 발생한 지출 중 K-IFRS 제1040호 기준 상 취득원가에 포함할 수 없는 원가는?",
        "options": [
            "① 건물 뼈대 공사에 투입된 정상적인 원재료 비용",
            "② 건설 현장 근로자들에게 지급한 직접 노무비",
            "③ 시방서 및 기본 설계도면 작성을 위한 건축사 수수료",
            "④ 건설 과정에서 발생한 비정상적인 자재 낭비액 및 파손 손실",
            "⑤ 건설과 직접 관련된 적격 자산 성격의 금융 비용(차입원가)"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 자가건설 투자부동산의 최초 취득원가를 집계할 때, 공사 도중 발생한 비정상적인 원자재 낭비액, 인력 비효율로 인한 초과 공임, 또는 파손 사고에 따른 복구 지출 등은 자산의 취득원가에 포함할 수 없으며 전액 즉시 당기손실(비용)로 처리해야 합니다.\n\n[오답 해설]\n①, ②, ③, ⑤ 건물 완공을 위해 정상적인 공정 하에서 불가피하게 소요된 원자재비, 노무비, 설계 용역 수수료 및 차입원가 자본화 금액 등은 모두 취득원가 구성요소입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "투자부동산의 매입 대금 결제를 일반적인 신용조건을 초과하여 장기 이연지급(Deferred payment)하기로 계약한 경우, 최초 취득원가의 산정 기준으로 옳은 것은?",
        "options": [
            "① 계약서 상의 명목상 납부 총액(총 액면가)",
            "② 취득일 시점의 '현금가격상당액(Cash price equivalent)'",
            "③ 계약 상 명목가액에 시중 은행 대출 금리를 단순 곱한 금액",
            "④ 미래에 지급할 할부 대금의 단순 합계액",
            "⑤ 기말 현재 시장에서 재조달할 수 있는 건물의 공정가치"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1040호 문단 24에 따라, 투자부동산 구입대금의 지급이 일반적인 신용기간을 초과하여 이연되는 경우 취득원가는 '현금가격상당액(Cash price equivalent, 즉 미래 결제액의 현재가치)'으로 측정합니다.\n\n[오답 해설]\n①, ④ 이연된 미래 지급액을 단순 합산하여 장부에 올리면 화폐의 시간가치 왜곡으로 자산과 부채가 모두 부풀려지게 되므로 위반입니다.\n③, ⑤ 이자비용 배분을 위한 단순 계산이나 재조달원가는 최초 취득원가 계상법과 무관합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "K-IFRS 제1040호에 따라 비화폐성 자산과의 교환으로 취득한 투자부동산의 최초 원가 측정 기준으로 옳은 것은?",
        "options": [
            "① 교환 계약에 상업적 실질이 존재하는 경우에도 무조건 제공한 자산의 장부금액으로 기재한다.",
            "② 상업적 실질의 존재 여부와 관계없이 취득한 자산의 잔존가치로만 기재한다.",
            "③ 교환거래에 '상업적 실질이 결여'된 경우에는 제공한 자산의 공정가치로 가산 평가한다.",
            "④ 취득한 자산과 제공한 자산 모두의 공정가치를 신뢰성 있게 측정할 수 없는 경우, 제공한 자산의 장부금액으로 최초 원가를 측정한다.",
            "⑤ 교환거래는 자산의 취득으로 간주하지 않으므로 어떠한 장부 가액도 기록하지 않는다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 교환거래에서 상업적 실질이 결여되었거나 취득·제공 자산의 공정가치 모두를 신뢰성 있게 추산할 수 없는 예외적인 경우에 한하여, 취득한 투자부동산의 원가는 '제공한 자산의 장부금액(Carrying amount)'으로 측정합니다.\n\n[오답 해설]\n① 상업적 실질이 존재하는 경우에는 공정가치 측정이 원칙입니다.\n② 잔존가치 기준 적용은 틀린 지문입니다.\n③ 상업적 실질이 결여된 경우에는 공정가치가 아닌 '제공한 자산의 장부금액'으로 인식해야 하므로 문장이 서로 모순됩니다.\n⑤ 교환도 자산의 취득에 해당하므로 장부에 적정 가액으로 등재해야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "자가건설 중인 투자부동산의 자산화 경로 중 '자본화 기간(Capitalization window)'이 언제 종료(즉, 원가 집계를 멈추고 자산의 취득을 확정하는 시점)되는가?",
        "options": [
            "① 임차인을 실제로 모집하여 공실에 최초 입주가 완료된 시점",
            "② 부동산 신축 완공 후 첫 운용리스 임대료가 예금 계좌로 수납된 날",
            "③ 부동산이 경영진이 의도하는 방식으로 운영될 수 있는 상태(의도된 조건에 도달)에 이른 시점",
            "④ 완공된 부동산에 대하여 관할 세무서에 임대업 등록 신청서가 통과된 날",
            "⑤ 건설 비용의 최종 잔금이 대금 결제 은행을 통해 송금 처리된 날"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 자가건설 투자부동산의 취득원가 집계는 부동산이 경영진이 의도하는 방식으로 운영될 수 있는 상태(완공되어 임대가 가능한 물리적 상태)에 이른 날 즉시 종료됩니다. 그 이후에 발생하는 지출(마케팅비, 초기 공실 유지비 등)은 자산원가에 보탤 수 없습니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 실제 영업상의 입주 시점이나 행정 및 대금 지급 등의 사후적 종결 조건들로서, 자산의 물리적 사용가능 상태(자본화 중단) 요건과는 관련이 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "토지와 건물을 일괄 취득한 경우 최초 원가 배분과 관련하여 K-IFRS 제1040호 하에서 자산으로 가산할 수 없는 항목은?",
        "options": [
            "① 일괄 매입 대금 중 감정평가 비율에 맞춰 토지 부분에 배분된 취득가액",
            "② 소유권 이전 대행을 담당한 법무사에게 송금한 정당한 수수료",
            "③ 일괄 매입 협상 과정에서 거래처와 합의하여 즉시 환급받은 현금 리베이트 할인액",
            "④ 등기 접수를 위해 강제로 구입한 정부 공채 채권의 취득원가와 현재가치의 차액(처분손실액)",
            "⑤ 토지 형질 변경을 위해 구청에 추가로 납부한 인허가 취득 면허세"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 매입 과정에서 발생한 할인이나 환급 리베이트는 원가에 포함되는 것이 아니라 오히려 최초 '취득원가에서 직접 차감'해 주어야 하는 요소입니다.\n\n[오답 해설]\n① 개별 감정 평가 비례 배분 취득액은 자본화 대상입니다.\n② 법무사 이전 용역 수수료는 직접 부대원가이므로 가산합니다.\n④ 공채 강제 인수로 인한 손실액은 부동산 취득에 수반되는 불가피한 대가이므로 자산원가에 가산합니다.\n⑤ 형질 변경 등 직접적 인허가 세금도 자산에 가산합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "리스이용자가 취득한 임차 건물 사용권자산이 투자부동산에 해당할 경우, K-IFRS 제1116호 리스 기준에 연계된 사용권투자부동산의 최초 원가 구성 항목으로 적절하지 않은 것은?",
        "options": [
            "① 리스료 지급 청구에 따라 인식한 '리스부채의 최초 측정금액'",
            "② 리스개시일 이전에 리스제공자에게 미리 지급한 선급 리스료",
            "③ 리스이용자가 리스 계약 성사를 위해 직접 지출한 리스개설직접원가",
            "④ 리스이용자가 리스기간 종료 시 자산을 원상태로 되돌려놓기 위해 추정한 복구원가의 현재가치",
            "⑤ 리스 체결 축하금으로 리스제공자로부터 수취하고 아직 정산하지 않은 리스인센티브 수취 총액"
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ 리스제공자로부터 이미 받아낸 리스인센티브 금액은 사용권자산의 최초 취득가액을 구성할 때 '차감(마이너스)'하는 요소이므로, 원가 구성(가산) 항목으로 적절하지 않습니다.\n\n[오답 해설]\n①, ②, ③, ④ 리스부채액, 개시전 리스료, 개설직접원가, 복구충당부채 현재가치는 모두 사용권자산 최초 장부 원가 계산 시 가산(가중)되는 정당한 구성 요소들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "자금 지급을 장기간 이연하는 장기 할부 거래의 최초 취득원가로 잡히는 '현금가격상당액(Cash price equivalent)'의 개념을 가장 바르게 설명한 것은?",
        "options": [
            "① 미래에 매년 나누어 납부할 원금과 명목 이자의 합계 금액",
            "② 거래 시점에 현금을 100% 한 번에 전액 납부한다고 가정할 경우 지불해야 할 거래 합계액(미래 할부액의 현재가치)",
            "③ 기말 결산 보고서 상 자산의 감가상각 누계 잔액에 대출 이자율을 가산한 금액",
            "④ 과거 취득 당시 최초 분양 가격과 현재 공정 시세의 단순 평균가",
            "⑤ 자산 청산 시 강제 경매를 통해 즉각적으로 회수할 수 있는 추정 순유입금"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 현금가격상당액은 취득일 현재 현금을 일시불로 바로 지불한다고 가정할 때의 합의 거래 가격을 뜻합니다. 이는 미래의 장기 이연 지급액을 적절한 할인율로 현재가치로 평가한 금액과 실질적으로 같습니다.\n\n[오답 해설]\n① 화폐 시간가치가 포함된 미래 액면 총액을 가리킵니다.\n③, ④, ⑤ 취득원가 산정 목적의 현금가격상당액의 학술적/실무적 회계 정의와 대치되는 임의의 진술입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    # --- L2 (이해): 15문항 (Q1461 ~ Q1475) ---
    {
        "id": "practice-accounting-ch06s02-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "K-IFRS 제1040호 '투자부동산' 취득원가 산정 시 가산하여야 할 직접 부대원가(Directly attributable costs)와 즉시 비용 처리하여야 할 일반 원가(General costs)를 대비한 해설로 가장 올바른 것은?",
        "options": [
            "① 계약 당사자 서명을 축하하기 위해 개최한 기념 파티 비용은 부동산 소유권을 취득하기 위해 발생한 비용이므로 취득원가에 포함한다.",
            "② 부동산 거래 성사를 위해 지급한 외부 공인중개사의 수수료는 직접 관련 원가이므로 취득원가에 가산한다.",
            "③ 새로운 임대용 오피스를 홍보하기 위해 매체에 집행한 광고 대금은 자산의 용도 변경에 해당하므로 취득원가에 포함한다.",
            "④ 본사 빌딩 매입 계약을 체결하기 전에 임시로 건물을 기획 검토했던 기획실 직원들의 상시 기본 급여는 취득원가에 분할 배분하여 가산한다.",
            "⑤ 취득 이후 임차인을 구하기 전까지 발생한 공실 건물의 난방비 및 경비 용역 수수료는 최초 취득원가에 보탠다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 부동산 거래의 중개인 수수료(복비)는 취득에 직접 귀속되는 거래원가이므로 최초 취득원가에 합산하는 것이 전적으로 정당합니다.\n\n[오답 해설]\n① 계약 파티 비용은 영업 촉진 지출이므로 광고선전비 등의 비용 항목입니다.\n③ 신축 광고 홍보 대금은 마케팅 비용이므로 판매비와관리비로 처리합니다.\n④ 기획 부서 임직원의 기본 급여 등 간접 관리 운영 오버헤드는 취득 원가에 가산할 수 없습니다.\n⑤ 취득 완공 후 임차 개시 전 발생한 공실의 일상 유지비는 자산 사용가능 상태 도달 후의 사건이므로 취득원가가 아닌 당기비용으로 계상합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "투자부동산 매입 시 지출된 부가가치세(VAT) 및 각종 공과금의 취득원가 산입 여부를 결정하는 회계적 판단 기준으로 옳은 것은?",
        "options": [
            "① 매입 시 지출된 부가가치세는 추후 관할 세무서로부터 전액 '환급(Refundable)'받을 수 있는 세액이라도 무조건 취득원가에 가산한다.",
            "② 환급 불가능한 성격의 소유권 취득세 및 법정 공과금 등은 최초 취득원가에 가산하여 처리한다.",
            "③ 세법 상 비과세 대상인 세액 부분까지 경영진의 임의 추정에 따라 자산원가에 보탤 수 있다.",
            "④ 정부 공채를 할인 매입하여 처분할 때 발생하는 매각 차손은 즉시 영업외 비용으로 털어낸다.",
            "⑤ 리스 이용자가 세무상 납부한 취득 관련 보증금은 전액 취득원가에 가산한 후 매각 시 감액한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 소유권을 확보하면서 세법 상 다시 환급 및 돌려받을 수 없는 '환급 불가능한 취득 세금(취득세, 등록면허세 등)'은 취득원가에 의무적으로 가산해야 합니다. 반면, 추후 세무서에 매입세액 공제나 신고를 통해 고스란히 환급받는 환급가능 부가가치세는 리시버블 성격이 되므로 자산 원가에서 전면 제외해야 합니다.\n\n[오답 해설]\n① 환급금은 자산의 취득을 위한 최종 희생 대가가 아니므로 원가에서 제외합니다.\n③ 자의적인 자산 원가 가산은 제한됩니다.\n④ 국공채 강제 매입 손실은 자산 취득 목적의 직접 관련 원가이므로 취득원가에 가산해야지 즉시 비용 처리할 수 없습니다.\n⑤ 리스 보증금은 향후 돌려받을 금융자산(보증금 채권)이므로 투자부동산 사용권자산의 취득원가를 구성하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "구입 대금을 3년간 이연 납부하는 이연지급조건 투자부동산의 최초 측정 원리(K-IFRS 1040 문단 24)와 관련된 이자비용의 후속 배분 처리에 대한 설명으로 옳은 것은?",
        "options": [
            "① 장기 미지급금에 대해 발생하는 이자는 자산의 가치를 높이므로 매년 동일한 금액만큼 투자부동산 원가에 누적 가산한다.",
            "② 현금가격상당액과 총 할부지급액과의 차액은 신용기간 전체에 걸쳐 당기 이자비용(금융원가)으로 유효이자율법 등을 활용하여 매년 인식해야 한다.",
            "③ 계약 상 약정이자율이 시중 이자율과 다른 경우에도 명목 상의 단순 차액 전체를 취득 첫해에 일시 영업외비용으로 전액 털어낸다.",
            "④ 이연 기간 중에 발생한 이자는 K-IFRS 제1023호에 따른 차입원가 자본화 요건을 충족하는지 여부와 관계없이 무조건 전액 비용 처리해야 한다.",
            "⑤ 이연 지급 계약에 따른 현재가치 할인차금은 자본조정 계정인 주식발행초과금과 즉각 상계한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 이연지급 거래에서 발생하는 화폐의 시간가치 차액(총 지급액 - 현재가치 상당 취득원가)은 신용(할부) 기간에 걸쳐 유효이자율법에 기반하여 이자비용으로 상각 인식하는 것이 맞습니다. (단, K-IFRS 1023 차입원가 자본화 기준을 충족하는 적격자산 요건인 건설기간 중이라면 자본화도 가능하나 일반적으로는 당기 금융비용으로 갑니다.)\n\n[오답 해설]\n① 취득 완공 이후 할부 기간에 걸쳐 발생하는 이자는 당기 손익거래(비용)이지 자산 원가 가산 요소가 아닙니다.\n③ 취득 첫해에 일시 상각 처리하는 법은 허용되지 않고 분할 배분해야 합니다.\n④ 차입원가 자본화 기준을 충족하는 적격자산 건설 기간 하에 위치하고 있다면 이자 비용을 원가에 가산할 수 있으므로, '무조건 비용 처리'한다는 말은 틀렸습니다.\n⑤ 할인차금은 자본거래 상계 항목이 아닌 부채(장기미지급금)의 차감계정입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "자가건설 중인 투자부동산과 K-IFRS 제1023호 '차입원가' 자본화 규정의 적용 관계에 대한 K-IFRS의 입장으로 가장 올바른 것은?",
        "options": [
            "① 투자부동산은 유형자산이 아니므로 어떠한 상황에서도 건설 기간의 금융 비용을 원가에 가산할 수 없다.",
            "② 건설 완료 전 공실 임대를 준비하는 단계의 차입 이자는 전대 수익으로 상쇄 처리하여야 자본화가 가능하다.",
            "③ 투자부동산이 경영진의 의도된 조건대로 완공되는 데 상당한 기간이 소요되는 '적격자산(Qualifying Asset)'에 해당한다면 건설 기간 중에 발생한 직접적인 차입원가는 자산원가에 산입해야 한다.",
            "④ 차입 원가 자본화 기간은 건물이 실제 첫 임차를 계약하여 효익이 발생하기 시작하는 날 개시된다.",
            "⑤ 회사가 자산 측정에 공정가치모형을 선택한 경우에도 건설 과정에서 자본화했던 차입원가 잔액을 자산 제거 시까지 감가상각으로 강제 배분 감액해야 한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 자가건설 투자부동산이라 하더라도 완공하여 임대가 시작되기까지 오랜 준비 기간이 소요되는 경우에는 K-IFRS 제1023호에 따라 차입 자금의 금융원가를 건설 과정(적격자산 취득활동 중) 동안 취득원가에 포함(자본화)하여야 합니다.\n\n[오답 해설]\n① 투자부동산 목적 신축 역시 적격자산 범주에 속하므로 금융비용 가산이 가능합니다.\n② 전대 수익으로 차입이자를 물리적으로 상쇄 차감하여 연계하는 기준은 없습니다.\n④ 차입원가 자본화는 적격자산의 취득·건설을 위한 지출과 차입원가가 발생하고 활동이 시작되는 시점에 개시됩니다.\n⑤ 공정가치모형 투자부동산은 감가상각을 적용하지 않으므로 강제 상각 배분 주장은 틀렸습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "자산교환거래에서 투자부동산의 공정가치 측정을 승인하는 핵심 조건인 '상업적 실질(Commercial Substance)'의 존재 여부를 판단하는 K-IFRS 상의 구체적 지표 기준으로 옳은 것은?",
        "options": [
            "① 교환을 통해 거래 당사자 간 취득하게 되는 자산의 물리적 형체(토지 대 건물 등)가 완전히 동일하면 상업적 실질이 존재하는 것으로 본다.",
            "② 교환으로 인수받는 자산과 제공하는 자산의 미래 '현금흐름의 유의적인 차이(구성, 시기, 위험 또는 기업특유가치의 변동)'가 나타나지 않는 때에만 상업적 실질을 인정한다.",
            "③ 취득 자산과 제공 자산의 유입 흐름에 유의적인 차이가 있고, 이로 인해 교환거래를 실행한 보고 실체 내부의 '기업특유가치(Entity-specific value)'가 실질적으로 변동할 때 상업적 실질이 존재하는 것으로 본다.",
            "④ 거래 당사자가 동일한 종속기업 간 거래이거나 이사회 결의가 생략된 경우에는 무조건 상업적 실질이 있는 거래로 인정한다.",
            "⑤ 두 자산의 공정가치 평가 비용의 합계액이 부동산 매매 중개 수수료의 20%를 초과할 경우에 성립한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1040호 문단 27에 따라 상업적 실질은 교환거래로 인하여 기업의 미래현금흐름이 변동될 것으로 기대될 때 성립합니다. 즉, 취득자산과 제공자산의 현금흐름 양상(위험, 시기, 금액)이 달라지거나, 교환으로 인해 기업의 영업부분 가치인 '기업특유가치'가 변동하고 이 차이가 교환된 자산의 공정가치에 비해 유의적일 때 상업적 실질이 있다고 판정합니다.\n\n[오답 해설]\n① 물리적 형태의 동일성 유무는 상업적 실질 판단의 주된 결정 요인이 아닙니다.\n② 현금흐름에 차이가 '있어야' 상업적 실질이 충족되는 것이므로 문장의 수식어가 잘못되었습니다.\n④ 특수관계자 내부거래 등은 상업적 실질 형성을 저해할 우려가 높으므로 무조건적 인정 주장은 거짓입니다.\n⑤ 평가 수수료 비중 등은 상업적 실질을 판정하는 재무적 기준에 속하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "교환을 통해 취득한 투자부동산에 대하여 '상업적 실질이 결여(Lacks commercial substance)'된 것으로 판정된 경우의 취득원가 및 교환손익 회계처리에 대한 설명으로 옳은 것은?",
        "options": [
            "① 취득한 투자부동산의 원가는 무조건 제공한 자산의 취득일 현재 시가로 적고 처분 손익을 전액 영업외수익으로 보고한다.",
            "② 취득한 투자부동산의 원가를 제공한 자산의 장부금액으로 측정하며, 처분(교환)에 따른 어떠한 이익이나 손실도 인식하지 않는다.",
            "③ 제공한 자산의 장부금액보다 취득한 자산의 감정가격이 크다면 그 차액을 기타포괄손익 재평가잉여금으로 적립한다.",
            "④ 상업적 실질이 없으므로 자산 거래 거래액 전액을 대손충당금 설정 차감 계정으로 미루어 둔다.",
            "⑤ 취득자산원가는 ₩0으로 계상하고 제공한 자산 전액을 기중 처분 손실비용으로 처리한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 교환거래에 상업적 실질이 없는 경우에는 자산의 교환을 실질적 거래(처분)로 보지 않으므로, 교환 취득 자산의 최초 원가는 '제공한 자산의 기존 장부금액'으로 승계 인식합니다. 장부액이 그대로 흘러가므로 어떠한 교환손익(처분손익)도 발생하지 않습니다.\n\n[오답 해설]\n① 상업적 실질이 결여되었으므로 시가법 및 처분손익 인식을 배제해야 하므로 규정 위반입니다.\n③ 재평가잉여금을 기타포괄손익으로 강제 인식하는 예외 대안은 제공되지 않습니다.\n④, ⑤ 대손 처리나 0원 취득원가 기재 주장은 자산 교환의 기본 복식부기 원리에 부합하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "K-IFRS 제1040호 문단 28에 따라 교환 취득한 투자부동산을 측정할 때, 제공한 자산과 취득한 자산 모두의 공정가치가 신뢰성 있게 측정되는 경우, 취득한 투자부동산의 원가 결정 기준으로 올바른 것은?",
        "options": [
            "① 제공한 자산의 공정가치를 취득원가 기초로 삼는 것이 원칙이며, 취득한 자산의 공정가치가 더 명백한 경우에만 취득한 자산의 공정가치를 사용한다.",
            "② 언제나 취득한 자산의 감정평가액을 우선 적용하며 제공 자산의 가치는 무시한다.",
            "③ 두 자산의 공정가치를 단순 산술 평균하여 취득가액을 계산한다.",
            "④ 무조건 취득한 자산의 역사적 건설 원가를 추적하여 원가로 대입한다.",
            "⑤ 취득원가를 제공한 자산의 기존 장부액과 기말 시가의 합산 잔액으로 결정한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 교환거래에 상업적 실질이 있어 공정가치로 취득가액을 정할 때, 원칙적으로는 '제공한 자산의 공정가치'에 현금 수수액 조정을 하여 신규 자산의 원가를 도출합니다. 단, '취득한 자산의 공정가치'가 훨씬 더 명백하게 입증되는 경우에만 예외적으로 취득한 자산의 공정가치를 취득원가로 인식하도록 규정하고 있습니다.\n\n[오답 해설]\n② 취득자산의 가치보다 제공한 자산의 공정가치가 최초 기본 경로이므로 우선 적용 설명은 틀렸습니다.\n③, ⑤ 산술평가나 장부액과 시가 합산 등의 계산법은 기준서에 없는 조작적 오답입니다.\n④ 교환거래에서는 역사적 건설 원가를 역산하여 적용하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "투자부동산을 성공적으로 신축 완공하여 사용가능 상태에 도달하였으나, 계획된 임대수율(조업도)에 도달하기 전까지 발생한 공실 관리비 및 초기 영업적자(Initial operating losses)에 대한 회계적 치료 기준으로 옳은 것은?",
        "options": [
            "① 건물의 정상 작동을 준비하는 단계에 해당하므로 취득원가에 전액 합산한다.",
            "② 최초 취득원가에 포함한 후 해당 금액만큼 무형자산인 영업권으로 가산 이체한다.",
            "③ 발생 즉시 전액 당기비용(영업외비용 등)으로 인식하여 손익보고서에 반영하고 자산원가에서 전면 제외한다.",
            "④ 주주들의 지분 투자 유출로 분류하여 자본조정 항목에서 감액 차감한다.",
            "⑤ 감가상각 누계 잔액에 대입하여 상각 비용을 차변에 상쇄하는 방법만 허용한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1040호 문단 23에 따라, 자산이 경영진이 의도하는 방식으로 가동될 수 있는 물리적 준비가 끝난 이후, 실제로 계획된 높은 수준의 임대율(조업도)을 맞추기 전까지 발생한 공실의 난방/경비비 및 초기 임대 적자 영업손실 등은 자산의 취득을 위한 부대 비용이 아니므로 전액 발생 기중의 '당기비용'으로 바로 처리해야 합니다.\n\n[오답 해설]\n① 자산 취득 종료 후의 일상이므로 취득원가에 합산할 수 없습니다.\n②, ④, ⑤ IFRS 자산/자본 회계 원리와 부합하지 않는 임의 처리안입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "신규 투자부동산(임대용 빌딩)을 취득하는 시점에, 당사 직원의 '급여(종업원 급여)'가 취득원가에 가산될 수 있는 정당한 조건은?",
        "options": [
            "① 해당 직원이 본사 빌딩 매입에 직·간접으로 관련되어 있으면 무조건 기본 급여의 50%를 취득원가에 포함한다.",
            "② 해당 직원이 신축 부동산의 '취득 및 건설 활동에 직접 귀속'되어 불가피하게 투입된 직접 노무 원가임이 확실하게 입증되는 경우",
            "③ 회사 관리 부서 임원으로서 부동산 취득 이사회 회의에 배석하여 기안을 확인한 자의 급여 일부",
            "④ 자산 임대 개시 이후 마케팅 활동을 위해 세입자를 찾아다닌 영업직 직원의 성과금 및 연봉",
            "⑤ 취득 이후 경비 부서에서 야간 순찰 임무를 띤 청원 경찰의 월 급료"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 투자부동산의 신축, 건설 또는 직접 취득 업무에만 전념하여 활동한 인력(건설 현장 인부나 매입 수속 전담 실무자)에 대한 종업원 급여는 자산의 취득에 직접 귀속 가능한 원가이므로 취득원가에 가산할 수 있습니다.\n\n[오답 해설]\n① 간접 관련자나 단순 지원 부서의 급여를 임의 안분하는 것은 금지됩니다.\n③ 관리 부서 임직원의 공통 급여는 취득원가 구성요소가 아닙니다.\n④, ⑤ 취득 완료 후의 마케팅 활동 및 방범 활동 급여는 판매비와관리비 등 당기비용으로 계상해야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "정부로부터 특정 토지나 상가를 무상 또는 낮은 대가로 양도받아 투자부동산으로 인식할 때의 K-IFRS 상 최초 측정 기준은?",
        "options": [
            "① 정부가 기록했던 장부상 역사적 대가가 최초 원가가 되며 기업 장부에는 ₩0으로 유지한다.",
            "② 국책 사업 자산이므로 회수가능액을 매년 10배로 가중 계산하여 기재한다.",
            "③ 정부보조금 관련 규정(K-IFRS 제1020호) 및 자산의 정의에 따라 해당 부동산의 '공정가치(Fair value)'를 기준으로 최초 원가를 측정하여 기재하는 것이 원칙이다.",
            "④ 완공될 때까지 매입 대금의 계약서상 액면 대금을 부채 잔액으로 환원 기재한다.",
            "⑤ 정부가 보증한 만기 상환 금액만큼만 금융자산으로 계상하고 임대는 배제한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 정부보조 등 비상업적 국가 지원을 통해 취득한 투자부동산은 K-IFRS 제1020호(정부보조금의 회계처리) 규정을 충족하여 최초 인식 시점에 공정가치로 측정하여 장부에 등재하는 것이 원칙입니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 세부 법적 특수성이나 실질적 시장 시세가 존재하는 토지 건물을 0원 등으로 기재하는 것은 충실한 재무보고 목적에 부합하지 않는 주장입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "임차 건물 사용권자산을 투자부동산으로 분류하여 최초 측정(K-IFRS 1116)할 때, 리스이용자가 부담하는 '복구의무(Dismantling/Restoration obligation)'와 관련된 회계처리의 올바른 기준은?",
        "options": [
            "① 임대 기간 종료 시 지출될 예상 복구 원가 총액을 물가 상승률 고려 없이 단순 합산해 당기말에 한 번에 비용 처리한다.",
            "② 복구의무의 이행으로 미래에 지출될 것으로 예상되는 현금유출액을 적절한 할인율로 할인한 '현재가치(Present value)'를 구하여 최초 취득원가(사용권자산)에 가산하고, 대변에는 '복구충당부채'를 설정한다.",
            "③ 리스 제공자가 원상복구를 면제해 주기로 합의한 특약이 있더라도 무조건 가상으로 계산하여 자산에 보탠다.",
            "④ 복구 충당 부채는 리스부채의 최초 잔액에서 직접 공제하여 장부 가액을 최대한 낮추는 데 쓴다.",
            "⑤ 복구 원가는 유형자산에만 적용되는 원리이므로 투자부동산 성격의 임대 ROU 자산에는 대입을 금지한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 임차 건물을 사용하여 전대하기 위해 복구 의무가 발생하는 경우, 향후 발생할 원상복구 예상원가를 현재가치로 평가하여 사용권투자부동산의 최초 취득가액에 얹고 동시에 대변에 '복구충당부채'를 잡아야 합니다. 이는 K-IFRS 제1116호 및 제1037호(충당부채) 연계 기준에 따릅니다.\n\n[오답 해설]\n① 미래 가액의 단순 액면가 합산 지출이나 일시 비용 처리는 현재가치 측정 규칙에 어긋납니다.\n③ 특약 등으로 복구 의무 자체가 존재하지 않는다면 복구충당부채나 관련 자산화 금액을 설정할 수 없습니다.\n④ 복구충당부채는 리스부채와는 성격과 이행 대상이 다른 독립된 부채 과목입니다.\n⑤ 투자부동산 사용권자산 역시 기초자산이 건물이므로 복구의무가 유효하면 당연히 복구 회계를 동일 적용합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "임차사용권자산(투자부동산 분류)을 확보하는 과정에서 지출되는 '리스개설직접원가(Initial direct costs)'에 대한 기준으로 옳은 것은?",
        "options": [
            "① 리스 계약 성사를 위해 중개인에게 지급한 수수료나 계약서 작성 법률 지출액 등은 취득원가(사용권자산)에 가산하여야 한다.",
            "② 리스개설직접원가는 전액 계약 당해 연도 손익보고서 상의 영업외비용으로 일괄 털어낸다.",
            "③ 리스 실행 여부와 무관하게 기획 중 무산된 계약건에 대한 출장 비용까지 모두 성공한 자산원가에 보태야 한다.",
            "④ 리스이용자가 리스제공자에게 납부할 총 금융리스료 합계액에서 차감하는 형식으로 대체한다.",
            "⑤ 보증인에게 정기적으로 지급하는 신용 수수료도 리스개설직접원가에 속하므로 자산화한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 리스이용자가 리스 계약 체결을 이끌어내기 위해 직접 지출한 증분원가인 리스개설직접원가(법률 계약 조율비, 자산 취득 목적 중개료 등)는 사용권투자부동산의 최초 원가에 가산되어 자본화됩니다.\n\n[오답 해설]\n② 당기 비용 일시 처리는 리스 기준 위반입니다.\n③ 계약이 무산된 건에 대한 지출은 성공한 자산의 원가에 배분할 수 없고 즉시 비용(도중 폐기) 처리합니다.\n④ 리스료 합계액의 변동이 아닌 취득원가의 부대 비용 가산 형태로 기입합니다.\n⑤ 신용 정기 보증료 등은 사용권 획득을 위한 취득원가 증분 비용에 들어가지 않는 기중 수수료 비용입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "투자부동산의 취득원가를 최초 구성할 때, 자산이 물리적으로 확보 및 완공된 시점 이후에 발생하여 자산원가로 볼 수 없는 후속 거래 상태는?",
        "options": [
            "① 최초 사용가능 상태에 도달하였으나 여전히 비어있는 사무실 건물의 관리경비비 및 감시 외주 비용",
            "② 소유권 등기 등록이 법원에 접수되어 처리되는 당일 기납부 완료된 인지세 지출액",
            "③ 건물 건축 도중 기계 수용 하중 테스트를 위해 정상적으로 가동해 본 기중 테스트 공임 비용",
            "④ 토지의 점유 안정성을 확고히 하기 위해 취득일 이전에 소송 합의금으로 전주인에게 대납한 원가",
            "⑤ 토지 위에 방치되어 있던 전 소유주의 노후 잔해물을 완전히 철거하여 분리 수거하는 용역비"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 건물이 완공 및 사용가능 상태가 된 시점 이후에 추가 임차 계약을 위해 발생한 단순 대기 기간의 일상 공실 관리 경비비는 자산의 최초 원가 대상 기간이 아니므로 가산할 수 없고, 당기 운영 비용으로만 인식합니다.\n\n[오답 해설]\n②, ③, ④, ⑤는 모두 취득 완공 전 또는 소유권 이전의 정상적인 상태를 갖추기 위해 직접 수반된 지출들이므로 장부 원가 가산 요소에 부합합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "K-IFRS 제1040호 '투자부동산'과 K-IFRS 제1016호 '유형자산'의 최초 취득 측정 및 부대원가 자본화 기준을 정밀 비교 분석한 내용으로 가장 옳지 않은 설명은?",
        "options": [
            "① 두 기준서 모두 최초 인식 시 취득원가로 측정하는 것을 원칙으로 삼는다.",
            "② 두 기준서 모두 소유권 이전을 위해 직접 납부하는 등기등록 관련 취득세 성격의 제세를 가산하도록 허용한다.",
            "③ 비정상적인 파손 손실이나 원가 낭비 비중은 두 기준서 모두에서 자산화 대상에서 전면 배제하며 즉시 비용 처리한다.",
            "④ 장기 이연결제 시 현재가치(현금가격상당액)로 원가를 기록하고 명목 가치 차액을 이자 비용 배분하는 구조는 두 기준서 간 이론적으로 동일하다.",
            "⑤ 유형자산 기준서에서는 취득 후 가동 이전 단계의 초기 손실을 자산원가에 보태는 예외가 있으나, 투자부동산에서는 이를 철저히 금지한다."
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ K-IFRS 제1016호(유형자산)에서도 자산이 의도하는 방식으로 가동될 수 있는 상태에 도달한 후 실제 조업도 등에 이르기 전 발생하는 초기 가동 손실 등은 자산의 취득원가에 포함할 수 없도록 강제하고 있습니다. 따라서 유형자산 기준서에서는 이를 예외로 가산한다는 설명은 완전한 오류입니다. 두 기준서의 초기 영업손실 배제 원칙은 이론적으로 완벽히 동일합니다.\n\n[오답 해설]\n①, ②, ③, ④ 유형자산과 투자부동산의 최초 측정 원가는 자산의 공통된 취득 경제학적 속성을 반영하므로 원칙과 세부 처리가 서로 대단히 일관됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch06s02-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "투자부동산(건물)의 취득 계약 상 판매자가 매입 대금의 10%를 '매입할인(Trade discount)'해 주었으나, 구매자는 이를 취득세와 퉁치기 위해 장부상 할인 적용 전 명목 가액 전체를 건물 원가로 올리고 할인받은 현금 잔액은 잡이익 처리하였다. 이 회계처리가 미친 영향 및 정정 방향에 대한 설명으로 옳은 것은?",
        "options": [
            "① 자산의 실질 거래 대금이 과다 계상되었으므로, 매입할인을 취득원가에서 즉각 차감하여 자산가액을 줄여야 정당하다.",
            "② 잡이익을 영업이익으로 과목 분류만 변경하면 문제없다.",
            "③ 할인은 마케팅 혜택이므로 즉시 광고선전비용 차감 계정으로 미루어 둔다.",
            "④ 건물의 명목 가치가 훼손되지 않도록 현 장부 금액을 고수하는 것이 IFRS 표현의 충실성에 완벽히 부합한다.",
            "⑤ 할인액은 미래 배당의 원천이 되므로 이익잉여금의 증가 요소로 직접 기입 정정해야 한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 매입할인이나 리베이트는 최초 거래 가격을 실질적으로 깎아주는 요소이므로, 최초 취득원가 계산 시 반드시 총 매입액에서 먼저 차감해야 합니다. 할인 전 명목액을 기재하면 자산이 과대계상되므로, 자산 가액을 삭감하는 정정 분개가 요구됩니다.\n\n[오답 해설]\n② 자산 본체의 과대 계상 오도가 해결되지 않습니다.\n③ 광고선전비 차감 처리는 취득 자산의 회계처리 범주가 아닙니다.\n④, ⑤ 명목 가치 고수나 자의적 자본 잉여 적립은 실질적 가액 측정을 방해하는 오류들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    }
]

questions.extend(new_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully added {len(new_questions)} questions. Total questions in database: {len(questions)}")
