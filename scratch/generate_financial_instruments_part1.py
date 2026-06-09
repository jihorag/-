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
    "section": "Chapter 07 금융자산",
    "item": "1절 금융상품"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q1601 ~ Q1610) ---
    {
        "id": "practice-accounting-ch07s01-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1032호 '금융상품: 표시'에 따를 때 '금융상품(Financial Instrument)'의 정의로 가장 올바른 것은?",
        "options": [
            "① 거래당사자 일방에게 금융자산을 발생시키는 동시에 다른 거래상대방에게 금융부채나 지분상품을 발생시키는 모든 계약",
            "② 기업의 자산에서 모든 부채를 차감한 후에 남는 잔여지분을 나타내는 계약",
            "③ 계약에 의하지 않더라도 법적 강제력에 의해 현금을 징수하거나 지급하게 하는 국가와의 의무 관계",
            "④ 미래에 실물자산(토지, 건물 등)을 인도받거나 서비스 제공을 청구할 수 있는 모든 거래",
            "⑤ 회사의 영업주기 내에 현금으로 회수될 것이 거의 확실한 단기 유동자산의 합계"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1032호에 따르면 금융상품은 거래당사자 일방에게 금융자산을 발생시키는 동시에 다른 거래상대방에게 금융부채나 지분상품을 발생시키는 모든 계약을 말합니다. 금융상품의 가장 핵심적인 특징은 '계약(Contract)'에 기초한다는 점입니다.\n\n[오답 해설]\n② 이는 지분상품(Equity instrument) 또는 자본에 대한 정의입니다.\n③ 세금이나 법적 의무 등 계약에 의하지 않은 항목은 금융상품의 정의를 충족하지 못합니다.\n④, ⑤ 실물자산의 인도청구권이나 단순 유동자산의 합계는 금융상품의 일반 정의가 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "다음 중 K-IFRS 상 '금융자산'에 해당하지 않는 항목은?",
        "options": [
            "① 기업이 보유하고 있는 현금 및 예금",
            "② 거래처에 원재료를 매입하기 위해 선지급한 선급금",
            "③ 매출 거래에서 발생하여 받을 권리가 있는 매출채권",
            "④ 다른 기업이 발행한 보통주 주식(투자지분상품)",
            "⑤ 거래상대방에게서 현금을 수취할 계약상 권리가 있는 대여금"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 선급금은 미래에 현금 등 금융자산을 수취할 계약상 권리가 아니라, 재화나 서비스를 인도받을 권리이므로 금융자산이 아닌 '비금융자산'으로 분류됩니다.\n\n[오답 해설]\n① 현금은 금융자산의 가장 대표적인 항목입니다.\n③ 매출채권은 현금을 수취할 계약상 권리이므로 금융자산입니다.\n④ 다른 기업의 지분상품(주식)은 금융자산에 포함됩니다.\n⑤ 대여금은 계약에 따라 현금을 수취할 권리이므로 금융자산입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "다음 중 K-IFRS 상 재무상태표의 '금융부채'로 분류되는 항목은?",
        "options": [
            "① 고객으로부터 미리 현금으로 받고 나중에 제품을 인도해야 하는 선수금",
            "② 미래에 발생할 자산 해체 및 복구 의무를 추정하여 적립한 복구충당부채",
            "③ 세법에 따라 세무서에 납부해야 하는 미지급법인세",
            "④ 금융기관으로부터 현금을 차입하고 미래에 이자와 원금을 상환하기로 한 차입금",
            "⑤ 차기 이후의 기간에 귀속될 임대료 수익을 미리 받아 이연시킨 선수수익"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 차입금은 계약에 따라 미래에 현금 등 금융자산을 인도해야 할 계약상 의무가 있으므로 금융부채에 해당합니다.\n\n[오답 해설]\n① 선수금과 ⑤ 선수수익은 현금이 아닌 재화나 서비스를 제공할 의무이므로 비금융부채입니다.\n② 복구충당부채는 계약상의 부채가 아닌 의제·법적 의무에 기초한 추정치 부채이므로 금융부채가 아닙니다.\n③ 미지급법인세는 법률적 납세 의무일 뿐 계약상 합의에 따른 채무가 아니므로 금융부채가 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "K-IFRS 제1109호 '금융상품'에 따라 금융자산을 최초로 인식하는 시점에 적용해야 할 측정 기준으로 가장 올바른 것은?",
        "options": [
            "① 최초 인식 시점에는 원칙적으로 공정가치(Fair Value)로 측정한다.",
            "② 금융자산의 미래 명목현금흐름을 시장금리로 할인하지 않은 총액으로 측정한다.",
            "③ 계약 만기 시에 수취하게 될 약정 원금 금액으로 측정한다.",
            "④ 자산의 취득에 사용된 역사적 장부금액과 순실현가능가치 중 낮은 금액으로 측정한다.",
            "⑤ 최초 인식 시에는 취득 목적과 관계없이 액면금액으로 일관되게 기재한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1109호에 따라 금융자산은 최초 인식 시점에 공정가치로 측정하는 것이 원칙입니다. 일반적으로 제공하거나 수취한 대가(즉, 거래가격)가 공정가치가 됩니다.\n\n[오답 해설]\n② 화폐의 시간가치를 고려해야 하므로 명목흐름 총액 적용은 틀렸습니다.\n③, ⑤ 만기 약정액이나 액면금액은 최초인식 시점의 공정가치와 일치하지 않는 한 최초 측정치가 될 수 없습니다.\n④ 저가법(장부금액과 순실현가능가치 중 적은 것)은 재고자산 평가 등에서 활용되는 기준으로 최초인식 측정 기준이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "당기손익-공정가치 측정 금융자산(FVPL 금융자산)을 취득하는 과정에서 발생한 거래원가(Transaction costs)의 K-IFRS 상 올바른 회계처리 방법은?",
        "options": [
            "① 취득 시점에 금융자산의 장부금액(최초 공정가치)에 전액 가산한다.",
            "② 취득 즉시 전액 당기비용(수수료비용 등)으로 인식한다.",
            "③ 자본 내 기타포괄손익누계액으로 반영한 뒤 자산 제거 시점에 손실 처리한다.",
            "④ 취득 후 예상 보유기간 동안 정액법으로 안분하여 감가상각비로 상각한다.",
            "⑤ 부채 계정인 '차입원가조정' 차감 항목으로 대변에 적립한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 당기손익-공정가치 측정 금융자산(FVPL)의 취득과 직접 관련하여 발생하는 거래원가는 최초 인식하는 공정가치에 가산하지 않고 발생 즉시 당기손익(비용)으로 인식합니다.\n\n[오답 해설]\n① 거래원가를 취득가액에 가산하는 것은 상각후원가(AC) 측정 자산 및 기타포괄손익-공정가치(FVOCI) 측정 자산에 적용되는 규정입니다.\n③, ④, ⑤ 거래원가를 자본 누적, 정액 상각, 부채 차감으로 계상하는 방식은 기준서에 부합하지 않는 오답입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "상각후원가 측정 금융자산(AC 금융자산) 또는 기타포괄손익-공정가치 측정 금융자산(FVOCI 금융자산)을 최초로 취득 및 인식할 때 발생한 직접적인 거래원가의 올바른 처리 방식은?",
        "options": [
            "① 취득 즉시 영업외비용으로 당기 처리한다.",
            "② 최초 인식하는 금융자산의 공정가치에 직접 가산하여 측정한다.",
            "③ 거래원가는 자산 분류와 무관하게 항상 별도의 무형자산(개발비)으로 등재한다.",
            "④ 매매거래가 완료된 기말 결산일에 자본금에서 직접 차감 처리한다.",
            "⑤ 거래원가는 전액 부채 항목인 '미지급거래원가'로 계상한 뒤 만기에 상환한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호에 따라, 당기손익-공정가치 측정 금융자산(FVPL)이 아닌 금융자산(AC, FVOCI)의 경우에는 취득과 직접 관련되는 거래원가를 최초 인식 시점의 공정가치에 가산하여 측정합니다.\n\n[오답 해설]\n① 당기 비용 처리는 FVPL 금융자산에만 국한되는 특수 규정입니다.\n③ 무형자산 분류나 ④ 자본금 직접 차감, ⑤ 부채 대기 계상은 모두 오류 회계처리입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "투자채무상품(채권 등)을 계약상 현금흐름을 수취하기 위한 목적으로만 보유하고, 그 계약 조건에 따라 특정일에 원금과 원금잔액에 대한 이자만으로 구성된 현금흐름(SPPI)이 발생하는 경우 이 자산의 K-IFRS 상 분류는?",
        "options": [
            "① 당기손익-공정가치 측정 금융자산(FVPL)",
            "② 상각후원가 측정 금융자산(AC)",
            "③ 기타포괄손익-공정가치 측정 지분자산",
            "④ 지분법적용 투자주식",
            "⑤ 위험회피지정 파생자산"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 계약상 현금흐름의 수취만을 목적으로 하는 사업모형을 가지고, 계약상 현금흐름이 원리금 지급(SPPI)만으로 구성된 채무상품은 '상각후원가 측정 금융자산(AC 금융자산)'으로 분류합니다.\n\n[오답 해설]\n① 계약 조건이나 보유 목적이 단기 매도용이 아니므로 FVPL이 아닙니다.\n③ 기타포괄손익-공정가치(FVOCI)는 계약상 현금흐름 수취와 '매도' 둘 다를 목적으로 할 때 적용되는 분류입니다.\n④, ⑤ 지분법이나 파생자산 분류는 채무상품의 현금흐름 수취 모형에 대응되지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "투자채무상품을 보유할 때, 사업모형이 '계약상 현금흐름의 수취'와 '금융자산의 매도' 둘 다를 통해 목적을 달성하는 것이고, 계약상 원리금 수취 요건(SPPI)을 충족하는 경우 이 채무상품의 K-IFRS 상 분류는?",
        "options": [
            "① 상각후원가 측정 금융자산(AC)",
            "② 기타포괄손익-공정가치 측정 금융자산(FVOCI)",
            "③ 당기손익-공정가치 측정 금융자산(FVPL)",
            "④ 자본 조정 항목 내 투자자산",
            "⑤ 연결대상 종속기업투자주식"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 계약상 현금흐름의 수취와 매도 둘 다를 사업모형의 목적으로 삼고, 계약상 원리금 지급 요건(SPPI)을 충족하는 채무상품은 '기타포괄손익-공정가치 측정 금융자산(FVOCI 금융자산)'으로 분류합니다.\n\n[오답 해설]\n① 현금흐름 수취'만'을 목적으로 하지 않으므로 AC 자산이 될 수 없습니다.\n③ 매도 및 그 외의 목적에 한정될 때 FVPL 자산으로 분류하는 것이 일반적입니다.\n④, ⑤ 자본 차감 유보 자산이나 종속기업투자 등의 개념은 이 분류 체계에 들어맞지 않는 별개 규정입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "K-IFRS 제1109호에 따를 때, 사업모형 및 계약 조건에 관계없이 투자지분상품(타사 주식 등)의 기본적인 분류 범주로 원칙적으로 적용해야 하는 자산 그룹은?",
        "options": [
            "① 상각후원가 측정 금융자산(AC)",
            "② 당기손익-공정가치 측정 금융자산(FVPL)",
            "③ 기타포괄손익-공정가치 측정 금융자산(FVOCI)",
            "④ 만기보유 금융자산",
            "⑤ 매도가능 지분법주식"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 투자지분상품(주식)은 계약상 원리금 수취 요건(SPPI)을 본질적으로 충족할 수 없으므로(이자와 원금의 개념이 없음), 원칙적으로 '당기손익-공정가치 측정 금융자산(FVPL 금융자산)'으로 분류해야 합니다.\n\n[오답 해설]\n① 주식은 원리금 특성이 결여되므로 절대 AC 금융자산으로 갈 수 없습니다.\n③ 단기매매목적이 아닌 주식은 최초 인식 시점에 FVOCI 지정을 '선택'할 수 있는 예외가 있을 뿐, 원칙적인 기본 분류는 FVPL입니다.\n④, ⑤ 만기보유나 매도가능 등은 과거 구 기준서(K-IFRS 1039호)의 레거시 명칭 및 잘못된 분류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "다음 중 K-IFRS 상 금융부채에 해당하는 미지급금과 비금융부채에 해당하는 미지급법인세를 구분하는 가장 근본적인 회계학적 기준은?",
        "options": [
            "① 계약(Contract)의 성립 여부",
            "② 거래상대방이 개인인지 법인인지 여부",
            "③ 지급 기일이 1년 이내에 도래하는지 여부",
            "④ 대금의 지급 수단이 통화인지 어음인지 여부",
            "⑤ 회사의 업종이 제조업인지 서비스업인지 여부"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 금융상품(자산/부채)은 '계약'에 근거하여 당사자 간에 권리와 의무가 법적으로 확정되는 거래를 뜻합니다. 미지급금은 거래 계약에 기초하므로 금융부채인 반면, 미지급법인세는 법률에 따른 납세 의무(비계약성)이므로 비금융부채에 해당합니다.\n\n[오답 해설]\n② 상대방의 법적 지위(개인/법인)는 금융자산/부채 구분의 잣대가 아닙니다.\n③ 1년 기일 여부는 유동/비유동 구분 기준입니다.\n④ 결제 도구(현금/어음)나 ⑤ 회사의 업종은 계약성 자산/부채 판단에 직접 영향을 주지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    # --- L2 (이해): 15문항 (Q1611 ~ Q1625) ---
    {
        "id": "practice-accounting-ch07s01-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "단기매매목적이 아닌 투자지분상품에 대하여 최초 인식시점에 기타포괄손익-공정가치 측정 금융자산(FVOCI 금융자산)으로 지정하는 선택과 관련하여 K-IFRS의 규정으로 가장 올바른 것은?",
        "options": [
            "① 언제든지 취소할 수 있으며, 기중에 원하면 FVPL 자산으로 바꿀 수 있다.",
            "② 최초 인식 시점에만 지정할 수 있으며, 한 번 지정하면 이를 취소할 수 없다.",
            "③ 처분할 때 발생하는 누적 평가손익은 즉시 당기순이익(처분손익)으로 재분류 조정해야 한다.",
            "④ 금융감독원에 분기마다 승인을 얻어 연장 기재해야 효력이 생긴다.",
            "⑤ 지분상품의 공정가치 변동액 중 이익 부분만 OCI로 보내고, 손실 부분은 당기 비용 처리한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호에 따르면 단기매매목적이 아닌 지분상품에 대한 FVOCI 지정 선택은 최초 인식 시점에만 가능하며, 한 번 지정하면 이후에 결코 취소할 수 없습니다.\n\n[오답 해설]\n① 취소불가능한 선택이므로 기중 임의 변경은 허용되지 않습니다.\n③ FVOCI로 지정된 지분상품의 처분 시점에 자본에 누적된 누적 평가손익(기타포괄손익누계액)은 절대 당기순이익으로 재분류조정(Recycling)할 수 없으며 이익잉여금으로 직접 대체해야만 합니다.\n④ 금융감독원 승인은 회계 분류 지정 조건과 무관합니다.\n⑤ 평가이익과 평가손실 모두 기타포괄손익(OCI)으로 일관되게 처리합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "K-IFRS 제1109호에 규정된 채무상품 분류의 2가지 핵심 조건인 '사업모형 평가'와 '계약상 현금흐름 특성(SPPI)'에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 사업모형 평가는 개별 금융자산 단위로 수행하며 경영진의 개별 매도 의도에 따라 수시로 결정된다.",
            "② 계약상 현금흐름 특성은 해당 자산이 특정일에 원금과 원금잔액에 대한 이자만으로 구성된 현금흐름(SPPI)을 발생시키는지 여부를 뜻한다.",
            "③ 채무상품이 계약상 원리금 회수 조건(SPPI)을 충족하지 못하더라도 사업모형이 수취 목적이면 AC 금융자산으로 분류할 수 있다.",
            "④ 금융자산의 보유 목적이 '매도'에만 국한되더라도 원리금 조건(SPPI)만 충족하면 무조건 AC 금융자산으로 지정된다.",
            "⑤ 회계불일치를 해소하기 위한 목적이라도 금융자산을 최초 인식 시점에 당기손익-공정가치 측정 자산(FVPL)으로 지정할 수는 없다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 계약상 현금흐름 특성 요건은 채무상품의 원리금 지급 조건(SPPI) 충족 여부를 판단하는 것이며, 이를 만족해야만 AC 또는 FVOCI로 분류가 가능합니다.\n\n[오답 해설]\n① 사업모형 평가는 개별 자산 단위가 아닌, 금융자산을 공동으로 관리하고 영업 목적을 함께 달성하는 '포트폴리오(현업 부서) 수준'에서 평가됩니다.\n③ 원리금 요건(SPPI)을 충족하지 못하면 사업모형과 관계없이 무조건 당기손익-공정가치 측정 금융자산(FVPL)으로 분류해야 합니다.\n④ 보유 목적이 매도 중심이면 원리금 조건 충족 여부와 무관하게 FVPL 금융자산으로 가야 합니다.\n⑤ 회계불일치를 제거하거나 유의적으로 줄이는 경우, 최초 인식 시점에 금융자산을 취소 불가능하게 FVPL로 지정할 수 있습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "K-IFRS 상 금융자산의 취득 및 이전과 관련된 '거래원가(Transaction Costs)'의 정의와 자산 가산 여부에 대한 진술 중 옳지 않은 것은?",
        "options": [
            "① 거래원가는 금융자산의 취득, 발행, 처분에 직접 귀속되는 증분원가를 의미한다.",
            "② 금융자산을 취득하지 않았거나 발행하지 않았다면 발생하지 않았을 지출액이 거래원가에 해당한다.",
            "③ 거래원가에는 중개인이나 대리인에게 지급하는 수수료, 주식이나 채권 거래 세금 등이 포함된다.",
            "④ 금융자산을 발행할 때 드는 자금조달 원가(Financing cost)나 내부 관리 비용도 거래원가에 가산하여 처리하는 것이 적당하다.",
            "⑤ 상각후원가로 측정하는 대여금의 취득과 직접 관련된 증분 거래비용은 최초 인식 장부금액에 가산된다."
        ],
        "answer": "4",
        "options": [
            "① 거래원가는 금융자산의 취득, 발행, 처분에 직접 귀속되는 증분원가를 의미한다.",
            "② 금융자산을 취득하지 않았거나 발행하지 않았다면 발생하지 않았을 지출액이 거래원가에 해당한다.",
            "③ 거래원가에는 중개인이나 대리인에게 지급하는 수수료, 주식이나 채권 거래 세금 등이 포함된다.",
            "④ 금융자산을 취득할 때 발생하는 자금조달 원가(Financing cost)나 내부 관리 비용도 증분거래원가로 분류하여 자산에 가산한다.",
            "⑤ 상각후원가로 측정하는 채권의 취득과 직접 관련된 증분 거래원가는 최초 인식 시 장부금액에 가산하여 측정한다."
        ],
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 자금조달 비용(채무 이자 비용 등), 보유 비용, 혹은 회사의 내부 관리 비용 및 관리 부서 운영비 등은 금융자산의 취득에 직접 귀속되는 '증분원가(Incremental costs)'가 아니므로 거래원가에 포함되지 않습니다.\n\n[오답 해설]\n①, ② 거래원가는 거래를 실행하지 않았더라면 피할 수 있었을 증분원가로 정의됩니다.\n③ 중개료, 거래세 등은 대표적인 증분거래비용에 속합니다.\n⑤ AC나 FVOCI 금융자산의 최초 측정 시 증분 거래원가는 자산 가액에 더해져 기재됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "금융자산의 '재분류(Reclassifications)'에 관한 K-IFRS 제1109호의 규정 중 가장 올바른 설명은?",
        "options": [
            "① 회사가 금융자산을 관리하는 '사업모형을 변경'한 경우에만 관련 금융자산을 재분류하며, 이러한 변경은 극히 드물어야 한다.",
            "② 경영진이 자산의 투자 전략이나 매각 의도를 바꾸면 그 변경일 당일에 즉시 재분류 분개를 처리한다.",
            "③ 투자지분상품을 FVPL에서 FVOCI로 지정한 선택이 마음에 들지 않으면 언제든지 재분류하여 소급 수정할 수 있다.",
            "④ 재분류는 사업모형 변경이 발생한 보고기간의 첫날로 소급하여 관련 자산의 이자수익을 재계산한다.",
            "⑤ 회계불일치를 해소하기 위해 최초 인식 시점에 당기손익-공정가치 측정 항목으로 지정한 채권은 후속적으로 언제든지 지정을 취소하여 재분류할 수 있다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False
        }
        ],
        "explanation": "① K-IFRS 제1109호에 따르면 금융자산의 재분류는 기업이 금융자산을 관리하는 '사업모형을 변경'한 경우에만 허용됩니다. 이러한 모형의 변경은 기업의 외부 또는 내부 변화에 따른 중대 사건이 있어야 하므로 극히 드물게 일어납니다.\n\n[오답 해설]\n② 단순 개별 자산의 매각 의도나 투자 전략 변화는 사업모형의 변경이 아니므로 재분류 대상이 아닙니다.\n③ 지분상품의 FVOCI 지정은 최초 인식 시점에만 가능하며 취소 불가능하므로 재분류가 불가능합니다.\n④ 재분류일은 사업모형의 변경 후 첫 번째 보고기간의 첫 번째 날(재분류일)부터 전진적으로 적용합니다.\n⑤ 회계불일치 해소를 위해 FVPL로 지정한 금융자산은 취소할 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "금융자산을 당기손익-공정가치 측정 금융자산(FVPL 금융자산)으로 취소불가능하게 지정할 수 있는 요건(FVPL 지정 권한)에 대한 설명으로 옳은 것은?",
        "options": [
            "① 최초 취득가액보다 기말 시가가 30% 이상 상승할 것으로 합리적으로 추정되는 모든 경우",
            "② 금융자산을 FVPL로 지정함으로써 서로 다른 기준에 따라 자산이나 부채를 측정하여 발생하는 '회계불일치(측정·인식 불일치)'를 제거하거나 유의적으로 줄일 수 있는 경우",
            "③ 세법 상 과세 표준 금액을 줄여 법인세 비용을 절감하는 전략을 수립한 경우",
            "④ 금융자산의 사업모형이 '수취 목적'이며 계약상 원리금 지급 조건을 충족하는 모든 단순 거래",
            "⑤ 회사의 외부 회계감사인이 기중 감사 보고서 상에 금융자산의 변동성을 OCI로 보고할 것을 권고한 경우"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호에 따라 최초 인식시점에 다른 측정 기준으로 인한 측정이나 인식의 불일치(회계불일치)를 제거하거나 유의적으로 줄이는 경우에는 금융자산을 FVPL로 취소 불가능하게 지정할 수 있습니다.\n\n[오답 해설]\n① 시가 상승 추정이나 ③ 법인세 비용 절감 목적 등은 지정 요건이 아닙니다.\n④ 원리금 조건과 수취 모형을 만족하면 AC 자산 분류가 원칙이며, 회계불일치가 존재하지 않는 한 강제로 FVPL 지정을 수행할 수 없습니다.\n⑤ 감사인 권고도 기준서 상의 합법적 회계불일치 요건을 대체하지 못합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "K-IFRS 제1109호에 따를 때 활성시장이 없어서 지분상품의 공정가치를 신뢰성 있게 측정하기 어려운 매우 제한적인 상황에서, 지분상품의 '원가(Cost)'가 공정가치의 적절한 추정치가 될 수 있는 객관적 상태에 대한 설명으로 옳은 것은?",
        "options": [
            "① 투자 대상 기업이 설립된 지 얼마 되지 않았고, 최근에 입수할 수 있는 재무 정보가 불충분하거나 공정가치 측정을 위한 유의적인 변동 증거가 관측되지 않는 경우",
            "② 투자 대상 기업이 코스닥 시장에 신규 상장되어 활성시장이 막 개설된 직후",
            "③ 피투자회사의 최근 영업이익이 전년 대비 100% 이상 급격히 급증하여 고속 성장 중인 경우",
            "④ 외부 독립 평가기관이 복수의 현금흐름 할인모형을 활용하여 적정 시가를 정밀 도출해 준 경우",
            "⑤ 회사가 자산의 평가 비용을 아끼기 위해 경영진 서면 결의로 원가법 적용을 채택한 모든 경우"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 지분상품은 최초 취득 후 공정가치 평가가 원칙이지만, 최근 정보가 불충분하거나 공정가치의 유의적인 지표 변동이 없는 극히 예외적인 경우에 한하여 취득 원가가 공정가치의 적절한 대용치(추정치)로 허용될 수 있습니다.\n\n[오답 해설]\n② 활성시장이 개설되었다면 공시가격을 사용해야 하므로 원가 추정은 배제됩니다.\n③ 피투자회사가 고속 성장 중인 것은 가치 변동이 있다는 유의적인 증거이므로 원가를 사용할 수 없습니다.\n④ 독립 시가가 산출되었다면 공정가치 적용을 수행해야 합니다.\n⑤ 기업의 자의적 평가비용 절감 의도는 원가 추정치 적용 사유가 될 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "투자채무상품이 계약상 원리금 지급 조건(SPPI 테스트)을 충족하지 못하여 무조건 당기손익-공정가치 측정 금융자산(FVPL)으로 분류되는 계약 조건의 예시로 가장 올바른 것은?",
        "options": [
            "① 채권의 이자율이 변동금리(예: CD 금리 등 시장지표금리)에 연동되어 연 주기마다 재설정되는 계약",
            "② 만기 원금 상환금액이 물가상승률(CPI)에 비례하여 조정되는 인플레이션 연동 조건의 국공채",
            "③ 채무상품의 원리금 지급액이 발행자의 당기순이익이나 특정 원자재(예: 금, 구리) 시세 변동률에 추가 연동되어 배분되는 계약",
            "④ 발행일로부터 5년 뒤에 액면원금을 일시 상환하고, 매년 말 고정된 5%의 표면이자를 후급하는 일반 회사채",
            "⑤ 발행자가 부도 등의 신용 악화 사건을 겪었을 때, 투자자가 채권 만기일 전에 원금을 조기 상환 청구할 수 있는 풋옵션이 내재된 회사채"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 채무상품의 원리금이 발행자의 이익이나 원자재 시세와 같은 외부 변수에 연동되면, 계약상 현금흐름이 단순 대여 계약의 이자와 원금(시간가치 및 신용위험에 대한 대가) 범위를 넘어서는 투자적 요소(위험노출)를 가집니다. 따라서 이는 SPPI 테스트를 통과하지 못하며 무조건 FVPL로 분류됩니다.\n\n[오답 해설]\n① 시장 지표 기준 금리 연동은 화폐 시간 가치의 변동 요인이므로 SPPI를 충족합니다.\n② 인플레이션 연동은 원금 실질가치 유지 장치이므로 이자 조건으로 용인됩니다.\n④ 전형적인 고정금리 채권은 당연히 SPPI 요건을 완벽하게 통과합니다.\n⑤ 신용 악화에 기초한 조기상환권은 대여 계약의 합리적 신용위험 보완 조항으로 취급되어 SPPI 통과가 가능합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "K-IFRS 제1115호 '고객과의 계약에서 생기는 수익'에 따른 '계약자산(Contract Assets)'과 K-IFRS 제1109호 '금융상품'의 금융자산 범위 적용에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 계약자산은 시간의 경과에 따라서만 대가를 청구할 수 있는 권리이므로 본질적으로 수취채권과 완벽히 동일하다.",
            "② 계약자산은 권리 청구를 위해 고객에게 추가적인 의무 수행을 완료해야 하는 등 이행 조건이 있으나, K-IFRS 제1109호의 손상(대손) 규정은 동일하게 적용된다.",
            "③ 계약자산은 재고자산과 유사하여 금융상품 기준서의 어떠한 규정도 적용받지 않는다.",
            "④ 계약자산은 금융부채인 '선수금부채'와 상계하여 기말에 소멸되므로 자산으로 유지될 수 없다.",
            "⑤ 계약자산의 공정가치는 매 결산일마다 외부 감정평가를 의뢰하여 자산 재평가이익을 대변에 인식해야 한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 계약자산은 수취채권(매출채권)과 달리 추가 조건 이행이 필요한 자산이지만, 신용위험 노출 측면에서 K-IFRS 제1109호에 따른 기대신용손실(ECL) 모형 기반 손상(감액) 규정을 동일하게 적용받습니다.\n\n[오답 해설]\n① 시간의 경과에 따라서만 대가를 청구할 수 있는 권리는 '수취채권(매출채권)'의 정의이며, 계약자산은 이와 구별됩니다.\n③ 금융자산의 특수 형태이므로 손상 검토 등 특정 금융상품 기준서 규정이 적용됩니다.\n④ 선수금과 기중에 자동 상계되어 소멸하는 일시적 대체 계정이 아니며 엄격히 자산으로 공시됩니다.\n⑤ 계약자산은 재평가모형 적용 자산이 아니므로 공정가치 재평가이익 환입 대상이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "K-IFRS 제1116호 '리스'에 따른 리스제공자의 '리스채권(Lease Receivables)'에 대한 금융상품 기준서(K-IFRS 1109호)의 규정 적용 범위로 옳은 것은?",
        "options": [
            "① 리스채권은 리스 기준서에만 의거하여 제거 여부를 판단하므로 금융상품 기준서의 제거 규정은 적용되지 않는다.",
            "② 리스채권은 금융상품 기준서의 기대신용손실 손상(대손) 규정과 제거(Derecognition) 규정이 모두 적용된다.",
            "③ 리스채권은 비금융자산이므로 제거 및 손상 규정 둘 다 적용에서 명백히 제외된다.",
            "④ 리스채권은 공정가치 평가 대상이므로 기말에 무조건 FVOCI 평가손익을 OCI로 분류 계상한다.",
            "⑤ 리스채권의 회수 불가액은 리스제공자의 매출원가에 직접 더해 자산을 상계할 뿐 기대손실 반영 대상이 아니다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 리스채권은 리스 거래에서 파생된 금융자산으로, K-IFRS 제1109호의 금융자산 제거(Derecognition) 규정과 손상(기대신용손실 평가 및 대손충당금 설정) 규정이 모두 적용됩니다.\n\n[오답 해설]\n① 리스채권의 장부 상 통제 상실 및 제거 요건은 K-IFRS 1109호 제거 조항을 준용합니다.\n③ 리스채권은 현금을 수취할 계약상 권리이므로 금융자산입니다.\n④ 리스채권은 공정가치 변동액을 OCI로 평가하는 대상 자산군이 아닙니다.\n⑤ 회수 불확실액은 기대신용손실 모형에 따라 대손충당금 비용으로 인식해야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "어떤 계약상 발행된 지분(예: 우선주 등)을 발행자의 재무제표 상 '자본(지분상품)'과 '부채(금융부채)' 중 어느 쪽으로 분류할 것인가를 결정할 때 적용되는 K-IFRS 제1032호의 가장 핵심적인 판단 기준은?",
        "options": [
            "① 상품의 공식 명칭이 '우선주 주식'으로 발행되어 등기부등본 상 주식 수로 등재되었는지 여부",
            "② 발행자에게 거래상상대방에게 현금 등 금융자산을 인도해야 할 '계약상 의무(Contractual obligation)'가 존재하는지 여부",
            "③ 매 기말 결산일에 법정 배당률만큼 배당금을 지급하기로 주주총회에서 의결 완료했는지 여부",
            "④ 상품의 만기가 발행일로부터 50년 이상 장기로 설정되어 있어 만기 미상환 가능성이 높은지 여부",
            "⑤ 투자자가 회사에 의결권을 행사하여 경영 전반에 실질 관여할 수 있는 법적 권리 부여 비율"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 상 금융부채와 지분상품을 구분할 때는 형식적인 명칭이나 등기 형태가 아닌, 발행자가 보유자에게 현금 등 금융자산을 인도해야 할 '피할 수 없는 계약상 의무(Contractual obligation)'를 부담하고 있는지라는 실질적인 요건을 기준으로 판단합니다. 상환 우선주와 같이 의무가 존재하면 금융부채입니다.\n\n[오답 해설]\n① 주식 명칭이나 등기 여부는 형식적인 외관에 불과하여 자본 분류의 보증이 되지 못합니다.\n③ 배당 의결은 사후 자본 처분 절차일 뿐, 최초 분류의 기준이 아닙니다.\n④ 만기 조항이 존재하고 상환 의무가 계약상 지워져 있다면 만기 연수와 무관하게 금융부채입니다.\n⑤ 의결권 행사 비율은 자본과 부채의 실질 구분 요소가 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "자기지분상품(자사의 주식)으로 결제되거나 결제될 수 있는 계약이 K-IFRS 상 '지분상품(자본)'으로 분류되기 위한 이른바 'fixed-for-fixed(확정 수량 대 확정 금액)' 원칙에 대한 설명으로 옳은 것은?",
        "options": [
            "① 확정되지 않은 가변적 금액의 부채를 결제하기 위해 발행 시점의 주가에 비례하는 변동 수량의 자기주식을 제공하기로 약정한 계약",
            "② 확정 수량의 자기지분상품을 확정 금액의 현금 등 금융자산과 교환하여 결제하는 방법으로만 결제될 계약(단, 파생상품의 경우)",
            "③ 현금 결제와 주식 결제 중 어느 쪽으로든 발행자가 결제 방식을 매년 임의로 선택할 수 있는 다중 옵션 계약",
            "④ 계약 체결일 현재 발행자가 보유한 자기주식 전부를 시장 평균가액으로 처분하여 부채 상환 재원으로 쓰는 거래",
            "⑤ 자기지분상품의 공정가치가 시장 상황에 맞춰 변동하는 동안 결제해야 할 주식 수를 무상주 지급 비율로 자동 배분하는 조건"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1032호에 따라 자기지분상품으로 결제되는 파생상품이 지분상품(자본)이 되기 위해서는 '확정 수량의 자기주식'을 '확정 금액의 현금 등 금융자산'과 교환하여 결제하는 방법(Fixed-for-fixed)으로만 인도되어야 합니다. 그렇지 않으면(예: 인도할 주식 수가 변동하는 경우) 금융자산이나 금융부채로 분류됩니다.\n\n[오답 해설]\n① 수취할 자기주식의 수량이 변동 가능한 비파생상품은 자본이 아닌 금융자산/금융부채로 분류됩니다.\n③, ⑤ 결제 방식이나 주식 수의 가변성, 임의 선택권이 있는 계약은 fixed-for-fixed 요건을 위배하므로 지분상품이 아닙니다.\n④ 단순 시장가 처분 및 대금 지급 거래는 자기지분 파생 결제 자본화 조항에 해당하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "K-IFRS 제1109호에 따라 최초 인식 시점에 기타포괄손익-공정가치 측정 항목(FVOCI)으로 선택 지정한 '투자지분상품(비단기매매 보통주)'에 대한 후속 손익 회계처리 원칙으로 옳은 것은?",
        "options": [
            "① 해당 지분상품에서 수령한 배당금(Dividends)은 원칙적으로 당기손익(PL)으로 인식한다.",
            "② 기말 공정가치 하락으로 발생한 모든 평가손실은 재무제표 상 당기손익(평가손실)으로 우선 차감한다.",
            "③ 지분상품의 신용 사건이나 부도로 손상이 발생하면, 누계 OCI 손실액을 즉시 당기손상차손 비용으로 재분류한다.",
            "④ 취득 거래에서 발생하여 최초 자산에 가산했던 거래원가는 매 연말 감액하여 수수료 비용으로 소급 처리한다.",
            "⑤ 지분상품의 주식분할로 인해 추가 무상주 주식을 수령하면 이를 평가이익 수익으로 잡는다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① FVOCI로 지정된 투자지분상품에서 받는 배당금은 투자주식의 취득원가를 회수하는 성격이 명백하지 않는 한, 원칙적으로 당기손익(배당요건 충족일, 보통 주주총회 결의일에 PL)으로 인식합니다.\n\n[오답 해설]\n② 기말 평가손익은 전액 기타포괄손익(OCI)으로 누적되며 당기순이익에 영향을 미치지 않습니다.\n③ FVOCI 지정 지분상품은 원칙적으로 손상(Impairment) 규정이 적용되지 않아, 누적된 OCI 평가손실을 당기 손상차손으로 전환(재분류)하지 않습니다.\n④ 거래원가는 자산 취득가에 반영되어 자본(OCI)에 흡수 유보되며 소급 환원하지 않습니다.\n⑤ 무상주 수령은 회계처리를 하지 않고 주식 수와 단가만 재조정합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "최초 인식 시점에 기타포괄손익-공정가치 측정 항목(FVOCI)으로 지정한 '투자지분상품(보통주 주식)'을 당기 중 제3자에게 전량 처분하였다. 처분 당일의 회계처리와 자본 항목 처리에 대한 K-IFRS 상의 설명으로 옳은 것은?",
        "options": [
            "① 처분 시 수취한 처분 대가와 취득가액의 총 차액을 당기손익 상 '처분손익'으로 전액 환입 보고한다.",
            "② 자본 내 기타포괄손익누계액에 쌓여 있던 관련 평가손익 누계액은 처분일에 당기손익(재분류조정)으로 재구성할 수 없다.",
            "③ 처분 후 자본(AOCI)에 남아 있는 잉여금은 전액 취소되며 회계장부에서 소멸하여 재무제표 밖으로 소급 삭제된다.",
            "④ 처분 시 처분 수수료 및 거래 수수료 비용은 전액 최초 취득시점의 자산가액에 반영되어 소급 조정된다.",
            "⑤ 처분 당일에 법적으로 주식 소유가 유지되고 있으므로 주주총회 전까지는 처분 분개를 연기해야 한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② FVOCI 지정 지분상품은 처분(제거)할 때 기존 자본에 유보되어 누적된 기타포괄손익누계액을 당기순이익으로 절대 재분류(Recycling)할 수 없도록 기준서가 엄격하게 차단하고 있습니다.\n\n[오답 해설]\n① 처분 시에도 당기처분손익은 장부에 계상되지 않습니다(₩0).\n③ 자본 내에 남아 있는 기타포괄손익누계액 잔액은 처분일에 '이익잉여금'으로 직접 대체(자본 내 과목 간 이체)하여 장부를 정리할 뿐, 소급 삭제하거나 환입하지 않습니다.\n④, ⑤ 처분 비용 소급 조정이나 처분 분개 연기 등은 회계 처리 원칙에 위배됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "금융자산의 통상적인 매입 또는 매도(Regular Way Purchase or Sale) 계약의 거래 인식 방법과 관련하여, K-IFRS 상 명시된 두 가지 회계처리 원칙(매매일 회계 및 결제일 회계)에 관한 설명으로 옳은 것은?",
        "options": [
            "① 매매일(Trade Date)과 결제일(Settlement Date) 중 어떤 방법을 쓸 것인지는 회사가 자산 범주(예: AC, FVOCI, FVPL)별로 동일한 방법을 일관되게 선택하여 적용해야 한다.",
            "② 결제일 회계는 계약을 체결한 날인 매매일에 자산의 취득과 대금 결제 채무를 즉시 재무상태표에 등재하는 방식이다.",
            "③ 매매일 회계를 채택하는 경우, 자산을 실제로 인도받는 날까지 발생하는 공정가치 변동액은 장부에 전혀 기록할 수 없다.",
            "④ 금융자산을 매도할 때 결제일 회계를 사용하면, 매매일부터 결제일 사이에 발생한 매도 자산의 시가 변동분은 손익계산서 반영 대상에서 제외된다.",
            "⑤ 회사는 보유한 자산 전체에 대하여 단일의 인식 방식만 선택하여 강제 사용해야 하며 범주별 차등 선택은 위법이다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1109호 하에서 통상적인 매매 거래는 매매일 회계(Trade date accounting)와 결제일 회계(Settlement date accounting) 중 하나를 선택할 수 있으며, 동일한 범주의 금융자산 내에서는 선택한 방식을 일관되게 적용하여야 합니다.\n\n[오답 해설]\n② 매매일에 자산을 즉시 등재하는 방식은 '매매일 회계'에 해당하며, 결제일 회계는 실제 인도·결제일에 장부를 기재합니다.\n③ 매매일 회계는 계약일 당일부터 자산 가액을 올리므로 시가 변동이 장부에 반영됩니다.\n④ 결제일 회계를 쓰더라도 매도 계약이 체결되면 매매일부터 결제일 사이의 공정가치 변동분은 자산 분류 성격(예: FVPL이면 PL, FVOCI이면 OCI)에 맞춰 평가 반영해야 합니다.\n⑤ 전체 금융자산에 단일 적용하지 않고, 자산의 범주별로 구분하여 매매일/결제일 회계를 각각 지정할 수 있습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s01-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "투자채무상품(회사채 등)이 원리금 지급 조건(SPPI 요건)을 만족하는지 여부를 검토할 때, 이자의 구성 요소로서 금융상품 기준서(K-IFRS 1109호)가 허용하는 정상적인 대여 이자 구성요소가 아닌 것은?",
        "options": [
            "① 화폐의 시간 가치(Time value of money)에 대한 대가",
            "② 특정 기간 동안의 신용위험(Credit risk) 노출에 대한 보상",
            "③ 자산의 유동성위험(Liquidity risk) 및 일반적인 대여 행정 비용에 대한 대가",
            "④ 금융자산을 보유하는 동안 발생한 채무발행자의 주가 상승률에 연동되는 초과 성과급 보상",
            "⑤ 대여 거래에서 적정한 이윤(Normal profit margin)을 획득하기 위한 가산 마진"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 채무의 이자율이 발행자의 주가 상승률 등 자산 지분가치나 실적에 추가 연동되는 조건은 단순 대여 계약의 신용위험 및 시간가치 보상 범위를 벗어납니다. 따라서 이는 SPPI 요건을 위배하는 비정상 이자 구성 요소입니다.\n\n[오답 해설]\n①, ②, ③, ⑤ 화폐의 시간가치, 신용위험, 유동성위험 보상, 대여 관련 행정비용, 정상적인 가산 마진 등은 모두 이자의 정상적인 구성요소(Basic lending arrangement)로 취급되어 SPPI 통과가 가능합니다.",
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
