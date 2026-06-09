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
    "item": "5절 투자지분상품"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q1801 ~ Q1810) ---
    {
        "id": "practice-accounting-ch07s05-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 상 금융자산의 분류에서 '투자지분상품(Equity Instruments)'의 본질적인 성격을 가장 올바르게 서술한 것은?",
        "options": [
            "① 발행자에게 계약상 현금을 지급할 의무를 지우는 계약 채무성 상품이다.",
            "② 발행자의 자산에서 모든 부채를 차감한 후의 잔여지분을 나타내는 모든 계약 상 상품이다.",
            "③ 보유자에게 매 회계기간 말 확정된 이자지급을 강제 청구할 법적 권리를 부여한다.",
            "④ 기업이 발행한 자기주식만을 지칭하며 타사 발행 주식은 지분상품 분류에서 배제된다.",
            "⑤ 무조건 만기 상환 금액이 계약 조건으로 사전에 확정 기재되어 있는 상품이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1032호 및 제1109호 상 지분상품은 발행자의 자산에서 모든 부채를 차감한 후의 잔여지분을 나타내는 계약 상 상품(예: 보통주)을 뜻합니다.\n\n[오답 해설]\n①, ③, ⑤는 원금과 이자를 수취/지급할 의무가 연동된 채무상품(Debt instruments)의 성격입니다.\n④ 지분상품은 기업이 타사에 투자할 목적으로 보유하는 타사 발행 주식(투자지분상품)도 핵심 구성요소로 포함합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "K-IFRS 제1109호 기준 상 투자지분상품을 최초 취득하여 자산 분류를 지정할 때, 원칙적으로 적용해야 하는 기본 측정 범주는?",
        "options": [
            "① 상각후원가 측정 금융자산 (Amortized Cost; AC)",
            "② 당기손익-공정가치 측정 금융자산 (Fair Value through Profit or Loss; FVPL)",
            "③ 기타포괄손익-공정가치 측정 금융자산 (Fair Value through OCI; FVOCI)",
            "④ 만기보유 금융자산 (Held-to-maturity; HTM)",
            "⑤ 매도가능 금융자산 (Available-for-sale; AFS)"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호에 따라 지분상품(주식 등)은 계약상 원금과 이자 지급만으로 구성된 현금흐름 요건(SPPI 테스트)을 만족할 수 없으므로, 원칙적으로 '당기손익-공정가치 측정 금융자산(FVPL)'으로 분류합니다.\n\n[오답 해설]\n① 상각후원가(AC)는 채무상품에만 적용되는 분류입니다.\n③ 단기매매 목적이 아닌 경우에 한해 최초 인식 시점에 FVOCI 지정을 선택할 수 있을 뿐이며, 원칙적인 기본 범주는 FVPL입니다.\n④, ⑤는 구 K-IFRS 기준서의 용어로 현행 제1109호에서는 사용하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "투자지분상품의 취득과 직접 관련하여 발생한 증권사 중개수수료 등의 '거래원가(Transaction Cost)' 회계처리 기준으로 가장 올바른 설명은?",
        "options": [
            "① 금융자산의 분류 범주에 관계없이 즉시 영업외비용으로 당기 처리한다.",
            "② FVPL 분류 시에는 당기손익(수수료비용)으로 처리하며, FVOCI 지정 시에는 최초 공정가치(취득금액)에 가산한다.",
            "③ FVPL 분류 시에는 최초 공정가치에 가산하며, FVOCI 지정 시에는 당기 비용으로 상각한다.",
            "④ 금융자산은 거래원가를 자본의 기타포괄손익누계액에 직접 마이너스 기입하여 누적한다.",
            "⑤ 거래원가 전액을 만기 제거 시점까지 취득 대여금 차감 계정으로 비망 기재한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호에 따라 FVPL 금융자산의 취득 관련 거래원가는 발생 즉시 당기손익(비용)으로 인식하지만, FVOCI(및 AC) 금융자산의 경우에는 최초 취득 공정가치에 직접 '가산'하여 취득원가를 구성합니다.\n\n[오답 해설]\n① 범주에 따라 자산원가 가산 여부가 달라집니다.\n③ FVPL과 FVOCI의 거래원가 처리 방식이 정반대로 설명되어 틀렸습니다.\n④, ⑤ 취득 시점에 OCI 누계액을 직접 차감하거나 만기 비망 계정으로 두지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "단기매매항목이 아닌 투자지분상품에 대해 최초 인식 시점에 공정가치 변동액을 기타포괄손익으로 표시하도록 선택하는 'FVOCI 선택 지정'의 정당한 법적 요건 및 취소가능성에 대한 설명으로 옳은 것은?",
        "options": [
            "① 언제든지 이사회 결의를 거쳐 자유롭게 지정 및 취소가 가능하다.",
            "② 최초 인식 시점에만 선택할 수 있으며, 한 번 지정하면 이후 결코 취소할 수 없다(Irrevocable).",
            "③ 기말 결산 보고 완료 후에 감사인의 사전 동의를 받아서 지정 취소를 실행한다.",
            "④ 세무 조정을 용이하게 하기 위해 매 사업연도 개시일마다 갱신하여 취소 선택할 수 있다.",
            "⑤ 지분상품 취득 1년 경과 시점에 자동으로 지정 취소되며 무조건 FVPL로 이체된다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 투자지분상품의 FVOCI 지정은 최초 인식 시점에만 선택할 수 있으며, 이 지정은 '취소불가능한(Irrevocable)' 선택입니다.\n\n[오답 해설]\n①, ③, ④ 자유로운 취소나 감사인 동의에 의한 정정, 매년 개시일 갱신 등은 허용되지 않습니다.\n⑤ 시간 경과에 따라 자동으로 지정이 취소되거나 FVPL로 이체되는 규정은 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "투자지분상품을 FVPL 금융자산과 FVOCI 지정 금융자산으로 보유 중이다. 보고기간 말 기말 평가 시 발생하는 '공정가치 변동 평가손익'의 올바른 기재 장소 조합은?",
        "options": [
            "① FVPL: 당기손익(PL) / FVOCI: 기타포괄손익(OCI)",
            "② FVPL: 기타포괄손익(OCI) / FVOCI: 당기손익(PL)",
            "③ FVPL: 당기손익(PL) / FVOCI: 당기손익(PL)",
            "④ FVPL: 기타포괄손익(OCI) / FVOCI: 기타포괄손익(OCI)",
            "⑤ FVPL: 이익잉여금(RE)에 직접 기입 / FVOCI: 주식발행초과금 가산"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① FVPL 금융자산의 기말 공정가치 변동액은 당기손익(PL)으로 반영하며, FVOCI 금융자산의 기말 평가손익은 기타포괄손익(OCI)으로 재무제표에 인식합니다.\n\n[오답 해설]\n②, ③, ④, ⑤ 각 자산 범주별 기말 공정가치 평가손익의 회계학적 보고 위치에 관한 잘못된 계정 분류 기입 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "K-IFRS 제1109호 상 'FVOCI 지정 투자지분상품'을 기중에 처분하였을 때, 과거에 자본에 인식해 놓았던 기타포괄손익누계액(평가손익)에 대한 회계적 재처리 금지 규정의 올바른 명칭은?",
        "options": [
            "① 손상차손인식 금지 (No Impairment recognition)",
            "② 재분류조정(재순환) 금지 (No Recycling to Profit or Loss)",
            "③ 감가상각안분 금지 (No Amortization allocation)",
            "④ 자본총량 상계 금지 (No Capital offsetting)",
            "⑤ 공정가치 취소 금지 (No Fair value revocation)"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② FVOCI 지정 지분상품은 처분 시 실현된 누적손익을 당기손익으로 보내는 '재분류조정(Recycling; 재순환)'을 절대 금지하고 있습니다.\n\n[오답 해설]\n① 손상(대손) 규정 배제 원리도 존재하나, 자본 누계액을 당기손익으로 대체하는 것을 차단하는 핵심 개념은 '재분류조정 금지'입니다.\n③, ④, ⑤는 지분상품 기말 처분 및 자본 환원과 관련 없는 임의의 단어 조합입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "투자지분상품(주식)에 대하여 K-IFRS 제1109호 상 '대손(손상) 충당금'을 설정하는 기대신용손실(ECL) 평가 규정의 적용 여부와 그 이유로 올바른 설명은?",
        "options": [
            "① 지분상품은 주가 폭락의 위험이 채무 상품보다 훨씬 크므로 3단계 ECL 손상 평가를 배로 엄격히 적용한다.",
            "② 지분상품은 계약상 이자 및 원금의 수취 조건이 존재하지 않아 신용 손실 평가를 진행할 수 없으므로, 손상(대손) 평가를 일체 배제(적용하지 않음)한다.",
            "③ FVOCI 지정 지분상품에 대해서만 매년 말 강제적으로 12개월 기대신용손실을 충당금으로 계상한다.",
            "④ 손상 평가는 하되, 손상차손은 자본조정 항목에만 별도 비망 기록한다.",
            "⑤ 비상장 주식에 대해서만 매 기말 손상 평가를 세무 한도액만큼 적용한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 투자지분상품은 계약 상 이자 및 원금을 돌려받을 명확한 현금흐름 요건이 없으므로 K-IFRS 제1109호 상 손실충당금(기대신용손실) 설정 대상을 원천적으로 배제합니다.\n\n[오답 해설]\n①, ③, ⑤ 지분상품은 주가 폭락 여부나 분류 범주, 상장 여부와 관계없이 기대신용손실(손상) 평가를 적용하지 않습니다.\n④ 손상 평가 자체를 하지 않으므로 자본조정 비망 기록도 실행하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "㈜A가 보유 중인 타사 투자지분상품으로부터 현금 배당을 결의 받아 배당금을 수령하였다. 이 배당 대금의 올바른 손익 보고 방법은? (단, 당해 배당은 투자금의 회수를 나타내지 않는 일반적인 경우이다.)",
        "options": [
            "① FVPL 금융자산은 당기손익(배당금수익)으로 처리하지만, FVOCI 지정 금융자산은 자본(OCI)에 직접 가산한다.",
            "② FVPL 및 FVOCI 지정 금융자산 모두 배당을 받을 권리가 확정되는 시점에 손익계산서 상 '당기손익(배당금수익)'으로 인식한다.",
            "③ 배당수익은 주주 총회 결의 전까지는 이익잉여금 처분 차감액으로 자본에 묶어 둔다.",
            "④ 배당금 수령 즉시 해당 지분상품의 취득원가에서 직접 삭감 제거한다.",
            "⑤ 투자지분상품 배당금은 당기 손익을 배제하고 무조건 기타포괄손익누계액에만 기재한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 투자지분상품(FVPL 및 FVOCI 지정 자산 모두)으로부터 얻는 배당금은 배당을 받을 권리가 확정되는 시점에 포괄손익계산서에 '당기손익(배당금수익)'으로 인식하는 것이 원칙입니다.\n\n[오답 해설]\n①, ⑤ FVOCI 지정 금융자산도 배당금에 대해서는 OCI가 아닌 당기손익으로 처리합니다.\n③ 자본 차감 거래가 아닌 투자수익 획득 자산 거래입니다.\n④ 일반 배당은 자산 취득원가의 차감이 아니라 별도 당기 손익수익으로 보고합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "FVOCI 지정 투자지분상품을 기중에 처분하여 더 이상 장부에 남아있지 않게 되었다. 이 제거 시점에 과거에 쌓아둔 자본 항목인 'FVOCI금융자산평가손익누계액(기타포괄손익누계액)'을 재무제표 내에서 정산할 수 있는 K-IFRS 상의 허용 기준은?",
        "options": [
            "① 반드시 그대로 누계액 자본 상에 영구 영결하여 변경을 배제한다.",
            "② 해당 기타포괄손익누계액 잔액을 기업의 '이익잉여금(Retained Earnings)'으로 대체(Reclassification)하여 환원할 수 있다.",
            "③ 즉시 당기손익계산서 대변에 '금융자산처분이익'으로 이체 환원한다.",
            "④ 주식발행초과금 자본 계정에 이체하여 부채 비율을 줄인다.",
            "⑤ 영업비용 판관비 감가상각누계액 상계액으로 강제 처리한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② FVOCI 지정 지분상품 처분(제거) 시 누적 OCI 평가손익은 당기손익으로 재분류할 수는 없으나, 자본 내부에서 이익잉여금(RE)으로의 대체는 기준서 상 완벽하게 허용(선택)됩니다.\n\n[오답 해설]\n① 이익잉여금 대체가 가능하므로 영구 보존만 강제되는 것은 아닙니다.\n③ 당기손익(처분이익) 대체는 재분류조정 금지 원칙에 정면으로 위배됩니다.\n④ 주식발행초과금이나 ⑤ 감가상각누계액 등과는 성격 상 전혀 관계가 없는 자본 대체 거래입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "투자지분상품(주식)을 취득하면서 목적이 '단기매매항목(Held for trading)'에 명백히 해당하는 경우, 최초 인식 시점에 기타포괄손익(FVOCI) 지정을 선택하여 분류하는 행위에 대한 K-IFRS 상 판정은?",
        "options": [
            "① 단기매매 여부와 관계없이 자유롭게 FVOCI 지정을 적용할 수 있다.",
            "② 단기매매항목인 지분상품은 FVOCI 지정 선택 자체가 원천적으로 허용되지 않으며, 무조건 FVPL로 분류해야 한다.",
            "③ 기말 결산 시 환율이 폭등할 경우에만 예외적으로 FVOCI 적용이 가능하다.",
            "④ 금융감독원의 승인을 득하면 제한적으로 적용할 수 있다.",
            "⑤ 취득 수수료를 즉시 자본 차감하는 분개를 쓰면 지정이 인정된다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호 하에서 투자지분상품을 FVOCI로 지정하기 위해서는 당해 자산이 '단기매매항목이 아니고', 'K-IFRS 제1102호 주식기준보상에 기한 거래가 아니어야 한다'는 단서 조항을 만족해야 합니다. 따라서 단기매매항목은 무조건 FVPL로만 분류해야 합니다.\n\n[오답 해설]\n① 단기매매항목은 지정을 원천 배제합니다.\n③, ④, ⑤ 임의의 예외 조건이나 금융감독원 승인 요건, 분개 방식에 기해 지정이 구제되지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    # --- L2 (이해): 15문항 (Q1811 ~ Q1825) ---
    {
        "id": "practice-accounting-ch07s05-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "㈜A는 거래처 주식 1,000주를 ₩100,000에 매입하고 취득 수수료로 ₩5,000을 추가 지출하였다. 취득 당시 단기매매목적이 아니었다. ㈜A가 이 주식을 (가) FVPL 금융자산으로 회계처리할 때의 최초 인식 장부금액과 (나) FVOCI 금융자산으로 지정하여 회계처리할 때의 최초 인식 장부금액의 올바른 조합은?",
        "options": [
            "① (가) ₩100,000 / (나) ₩100,000",
            "② (가) ₩100,000 / (나) ₩105,000",
            "③ (가) ₩105,000 / (나) ₩100,000",
            "④ (가) ₩105,000 / (나) ₩105,000",
            "⑤ (가) ₩95,000 / (나) ₩105,000"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 지분상품 최초 장부가격 거래원가 조정 원리:\n- FVPL 최초 장부금액 = 공정가치 ₩100,000 (수수료 ₩5,000은 당기 수수료비용 처리)\n- FVOCI 최초 장부금액 = 공정가치 ₩100,000 + 거래원가 ₩5,000 = ₩105,000\n따라서 (가) ₩100,000, (나) ₩105,000이 맞습니다.\n\n[오답 해설]\n① 수수료 처리를 양쪽 다 누락한 경우입니다.\n③ 두 자산 범주 간 최초 거래비용 귀속 원리를 혼동한 오답입니다.\n④ 두 범주 모두 수수료를 자산 가산한 왜곡치입니다.\n⑤ FVPL에서 수수료를 차감(-) 처리하여 얻은 잘못된 계산입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "㈜나진은 비단기매매 목적으로 보유 중인 상장회사 주식에 대해 취득 시점에 FVOCI 지정을 취결하였다. 결산일에 주가가 폭락하여 최초 취득원가 ₩100,000인 주식의 공정가치가 ₩40,000으로 급락하였고, 해당 피투자사의 재무구조가 완전히 악화되어 회복 불가능한 신용 손실 손상 상태인 것으로 입증되었다. K-IFRS 상 ㈜나진이 기말 결산 분개 시 당기 손익에 미쳐야 할 정당한 영향에 관한 설명으로 옳은 것은?",
        "options": [
            "① 영구적인 손상이 입증되었으므로 차액 ₩60,000을 당기손익 상 '손상차손(대손상각비)'으로 즉시 당기 비용 반영한다.",
            "② 지분상품은 기대신용손실 모형을 적용하지 않으므로 손상차손을 계상하지 않으며, 공정가치 폭락액 ₩60,000은 전액 기타포괄손익(OCI) 평가손실 및 자본 차감으로만 보고하고 당기 손익에는 아무런 영향을 주지 않는다.",
            "③ 손상차손 ₩60,000을 자본에서 줄이고 영업이익 가산분으로 대치한다.",
            "④ 주식의 취득 당시 장부금을 영(₩0)으로 즉시 제각 제거한다.",
            "⑤ 피투자사의 손실 비율을 지분법 비율로 환원하여 당기이익을 늘린다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호에 의거, FVOCI 지정 투자지분상품은 가치 하락의 심각성이나 영구성에 관계없이 손상차손을 당기 손익으로 절대 인식하지 않습니다. ₩60,000 전체가 OCI 평가손실로 자본에 남을 뿐입니다.\n\n[오답 해설]\n① 손상차손 ₩60,000을 당기비용으로 처리하는 것은 채무상품의 회계 원리이며, 지분상품에는 허용되지 않습니다.\n③, ④, ⑤ 임의로 영업이익 가산 대체, 장부가 즉시 영(₩0) 제각, 혹은 지분법 변칙 적용 등의 진술은 기준서 위반입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "㈜진우는 FVOCI 지정 투자지분상품을 장부금액 ₩120,000 상태에서 기중에 ₩150,000에 매각 처분하였다. 처분 거래 중 증권사 매각수수료로 ₩3,000을 지출하였다. K-IFRS 상 ㈜진우가 처분 시점의 회계처리 시 이 매각수수료 ₩3,000을 적정하게 처리하는 기준은?",
        "options": [
            "① 처분 시점의 직접적인 거래비용이므로 즉시 판매비와관리비(수수료비용) 당기 비용 처리한다.",
            "② 실질 처분 유입액을 줄여 자본 OCI 누계액(또는 이익잉여금 대체분)으로 정산할 처분대가 순액을 ₩147,000으로 조정 처리한다. (당기 손익 항목에는 절대 수수료비용을 기재하지 않는다.)",
            "③ 처분 자산의 감가상각 가산액으로 대차를 메운다.",
            "④ 금융자산 처분 비용은 무조건 자본금 원장에서 직접 감액한다.",
            "⑤ 수수료를 차입 부채의 증가로 기입한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② FVOCI 지정 지분상품은 취득뿐 아니라 '처분' 시에도 손익계산서 상 당기 처분손익을 기록할 수 없으므로, 매각 시 발생하는 처분비용(수수료 등)은 처분대가에서 직접 차감하여 최종 실질 순수취액(₩147,000)을 기준으로 처분 회계(자본 내부 대체 등)를 마감해야 합니다. 즉, 당기 손익 상 수수료 비용을 잡지 않습니다.\n\n[오답 해설]\n① 당기 판관비 비용으로 인식할 수 없습니다 (손익에 수수료비용이 노출되는 것을 허용하지 않음).\n③, ④, ⑤ 감가상각 연동, 자본금 원장 직접 차감, 차입 부채 계상 등은 발생주의 상각 원칙에 반합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "투자지분상품(보통주)을 보유한 기업이 배당금수익을 당기 손익으로 인식하기 위해 만족해야 하는 K-IFRS 상의 구체적인 요건으로 가장 옳지 않은 것은?",
        "options": [
            "① 배당을 수취할 주주의 권리가 확정(보통 주주총회 배당 결의일)되어야 한다.",
            "② 배당과 관련된 경제적 효익의 유입 가능성이 높아야 한다.",
            "③ 배당금의 금액을 신뢰성 있게 측정할 수 있어야 한다.",
            "④ 당해 배당금이 투자 지분 상품의 취득원가를 유의적으로 회수하는 성격이 아니어야 한다.",
            "⑤ 실제 기업 통장에 현금 대금이 물 물리적으로 완치(입금)되는 날을 기준으로만 배당수익을 계상한다."
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ K-IFRS 상 배당수익은 실제 현금의 영수 시점이 아닌 '배당을 받을 권리가 확정되는 시점'에 발생주의 원칙에 따라 인식합니다.\n\n[오답 해설]\n①, ②, ③ 배당수익 인식의 3대 기본 충족 조건입니다.\n④ 만약 배당금이 피투자기업의 과거 누적 이익이 아닌 자본 환급 성격 등으로 투자원금의 유의적 회수를 구성한다면, 수익이 아닌 자산의 회수로 처리하여 취득원가에서 차감해야 하므로 정당한 단서입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "㈜감평은 투자 목적으로 타사 주식을 취득하고자 한다. 다음 중 지분 결제 성격이 내재되어 있으나, 계약 조건 상 보유자에게 만기 시점에 확정금액의 풋옵션(Put option; 조기상환청구권)이 강제로 부과되어 실질적으로 '계약상 현금흐름(SPPI) 요건'을 유발하여 FVOCI 지정을 적용할 수 없는 특수한 형태의 상품은?",
        "options": [
            "① 보통의 의결권을 지닌 일반 보통주 (Common Stock)",
            "② 비보증형 배당 무의결권 우선주 (Non-cumulative Preferred Stock)",
            "③ 일정 기한 도래 시 발행자에게 액면가 및 누적 연체 이자 상당액의 상환을 요구할 수 있는 '상환우선주(Redeemable Preferred Stock)'",
            "④ 합자회사의 무한책임 지분",
            "⑤ 외국 자회사의 보통 주주권"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 상환청구권(풋옵션)이 장착되어 만기 시 발행자에게 상환을 강제 청구하는 우선주는 실질이 채무상품(Debt instrument)의 현금흐름 속성을 지닙니다. 지분상품이 아닌 채무상품 범주(AC, FVOCI, FVPL)로 사업모형에 따라 테스트해야 하므로, 지분상품에만 전면 허용되는 'FVOCI 선택 지정'의 대상으로 삼을 수 없습니다.\n\n[오답 해설]\n①, ②, ④, ⑤ 발행자에게 잔여 재산 환수 권리만 존재하고 확정 채무를 지우지 않는 순수 지분 성격의 투자 지분 상품 항목들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "비단기매매 투자지분상품에 대해 최초 인식 시점에 FVOCI 지정을 실행할 때, 기말에 주식 평가손익이 발생하여 OCI 자본 누계액에 정산 보고되더라도 이것이 손익계산서 상 당기순이익에 전혀 환원되지 않는 원리를 회계학적 개념으로 설명한 것으로 가장 올바른 것은?",
        "options": [
            "① 미실현 보유 손익을 손익계산서에 누적할 시 실물 자본 유지 개념이 전면 붕괴하기 때문이다.",
            "② 지분 투자에 따른 시세 차익은 경영진의 이익 조정 수단(수익 실현 시점 조작을 통한 순이익 임의 변동)으로 악용될 위험이 크므로, 기준서가 당기순손익 보고(재분류조정) 경로를 원천 차단하여 정보 신뢰성을 제고하기 위함이다.",
            "③ 지분 투자로 발생하는 손익은 국가 경제 규모 변동과는 무관한 단순 분배 거래이기 때문이다.",
            "④ 피투자사 주주는 자산 거래의 상대일 뿐 손익 발생의 주체가 될 수 없기 때문이다.",
            "⑤ 세법 상 이익 산정에 배당 외 보유 손익을 전량 제외하는 관행을 맞춘 법정 조항이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호가 FVOCI 지정 지분상품에 대해 재분류조정(Recycling)을 전면 불허한 핵심 이유는, 경영진이 자사 이익 조정을 위해 보통주를 매각하는 시점을 선택하여 당기 순이익을 임의로 부풀리거나 낮추는 행위(Cherry-picking)를 방지하여 정보의 비교가능성과 중립성을 높이기 위함입니다.\n\n[오답 해설]\n① 실물자본유지 개념을 위해 재분류를 막는 것은 아닙니다.\n③ 국가 경제 변동이나 ④ 상대방 거래 주체성 여부는 회계 기준 논리와 직접적 연관이 없습니다.\n⑤ 세법 관행 추종을 위해 재무보고 기준서를 고안하지 않습니다.\n⑥은 수수료 비용 처리에 관한 완전히 빗나간 복사본 선택지입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "투자지분상품에 대해 최초 취득 시점에 FVOCI 지정을 사용했을 경우, 기업이 재무제표 작성 시 주석(Disclosure)으로 공시해야 하는 법적 필수 사항이 아닌 것은?",
        "options": [
            "① 해당 특정 투자지분상품을 FVOCI로 지정하기로 결정한 합리적 배경과 이유",
            "② 보고기간말 결산일 현재의 각 지분상품별 공정가치 금액",
            "③ 당기 회계기간 중 인식한 배당금수익의 상세 정보 (기제거 자산 배당 vs 보유 자산 배당 구분)",
            "④ 기중에 실행한 지분상품의 처분 정보 (처분 시점 주가, 처분한 주식 수, 처분 이유 및 처분 시점 자본 내부 이체액)",
            "⑤ 피투자사가 기중에 신규로 취득한 유형자산의 감가상각누계액 상세 명세"
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ 피투자사가 자체 취득한 개별 유형자산의 감누 내역은 투자자(보유자)의 재무제표 주석 공시 의무 대상이 아닙니다.\n\n[오답 해설]\n①, ②, ③, ④ K-IFRS 제1107호 '금융상품: 공시'에 따라 FVOCI 지정 지분상품 보유 시 반드시 공시해야 하는 구체적인 주석 요구 요건들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "㈜진우는 비상장 지분상품을 FVOCI 지정 자산으로 보유하던 중, 피투자사의 임시주주총회 결의를 통해 주주환원을 위한 '자본 자본금 차감 환급 배당(청산형 배당)'을 받았다. 이 배당은 투자 자금의 원금 회수를 나타내는 것이 명백하였다. K-IFRS 상 ㈜진우가 수령한 배당금의 정당한 회계처리는?",
        "options": [
            "① 원금 청산형 배당이더라도 일반 배당과 동일하게 전액 손익계산서 상 '배당금수익(당기손익)'으로 계상한다.",
            "② 실질이 투자금의 원금 회수를 나타내므로 배당금수익 당기 손익을 잡지 않으며, 수령액만큼 해당 '투자지분상품(장부금액)'에서 직접 감액(차감)하여 정산한다.",
            "③ 전액 기타포괄손익누계액 가산 자본 거래로만 처리한다.",
            "④ 기말 유형자산 평가이익 증가분으로 이체 정산한다.",
            "⑤ 단기차입금 부채의 환급 조항으로 분류한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 배당금이 명백하게 투자 원금의 회수(청산형 배당 등)를 구성하는 특수한 경우에는, 당기 수익(배당금수익)으로 인식하지 않고 해당 금융자산(투자지분상품)의 장부금액을 직접 감액하는 자산 감소 처리를 적용해야 실질에 부합합니다.\n\n[오답 해설]\n① 원금 회수 성격이 명백할 시 수익 인식이 금지됩니다.\n③ OCI 가산 자본 거래가 아닌 금융자산 장부가 차감 계상 대상입니다.\n④, ⑤ 유형자산 평가나 단기차입금 부채 상환 등과는 관련 없는 투자자산 장부가 변동 거래입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "투자지분상품(FVPL 금융자산)의 기말 공정가치 평가로 인하여 발생한 'FVPL금융자산평가손익'이 법인세 효과를 고려하기 전 단계에서 포괄손익계산서(I/S)의 어느 항목에 통합 분류 기재되어 영업외 손익을 구성하는가?",
        "options": [
            "① 판매비와관리비 (판관비)",
            "② 금융원가 또는 금융수익 (기타영업외손익)",
            "③ 매출원가 (Cost of goods sold)",
            "④ 기타포괄손익 (OCI)",
            "⑤ 재평가잉여금누계액"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② FVPL 지분상품의 공정가치 변동액은 당기손익(금융수익 또는 금융비용 등 영업외손익 성격)으로 분류되어 당기순이익 산출에 반영됩니다.\n\n[오답 해설]\n① 판관비(영업비용)에 계상되지 않습니다.\n③ 재화의 매출에 따른 비용이 아니므로 매출원가가 아닙니다.\n④, ⑤ 기타포괄손익이나 자본 재평가잉여금은 FVPL의 평가 범주가 아닌 FVOCI 또는 유형자산 재평가 범주입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "FVOCI 지정 투자지분상품을 기중에 매각 처분함에 따라, 기존에 적립되었던 자본 내 OCI 평가손익누계액 ₩10,000을 '이익잉여금(Retained Earnings)'으로 대체하기로 내부 결정하였다. 이 자본 간 이체(대체) 처리가 회계 상의 '당기순이익' 및 '총포괄손익(Total Comprehensive Income)'에 미치는 정당한 영향 분석으로 옳은 것은?",
        "options": [
            "① 당기순이익이 ₩10,000만큼 증가하고, 총포괄손익도 ₩10,000만큼 증가한다.",
            "② 당기순이익과 총포괄손익 모두 전혀 변동하지 않는다 (영향 없음).",
            "③ 당기순이익은 변화가 없으나, 총포괄손익만 ₩10,000 증가한다.",
            "④ 당기순이익은 ₩10,000 감소하고, 총포괄손익은 ₩10,000 증가한다.",
            "⑤ 이익잉여금이 과소 정산되어 납부할 법인세 부채가 ₩10,000 즉시 유발된다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 평가손익누계액의 이익잉여금 대체 분개는 (차) OCI누계액 10,000 / (대) 이익잉여금 10,000 과 같은 '자본 계정 간의 내부 이동(Reclassification within equity)'일 뿐입니다. 수익과 비용 거래가 전혀 수반되지 않으므로 당기순이익에 미치는 영향은 ₩0(영향 없음)이며, OCI 감소와 이익잉여금 증가가 서로 상계되므로 총포괄손익 총액 또한 아무런 변동이 발생하지 않습니다.\n\n[오답 해설]\n①, ③, ④ 손익 변동이 없는 순수 자본 간 대체 성격을 이해하지 못하여 발생한 왜곡 설명 지문들입니다.\n⑤ 자본 내부 대체는 법인세 과세소득을 구성하지 않으므로 추가 법인세 유발은 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "㈜A는 투자 목적으로 거래처 B사 주식 30%를 취득하여 사외이사를 파견하고 실질적 경영에 유의적인 영향력(Significant influence)을 행사하고 있다. 이 주식 자산에 대해 ㈜A가 K-IFRS 제1109호 상 'FVPL'이나 'FVOCI 지정 지분상품' 분류를 적용하여 공정가치 평가 손익을 인식하고자 할 때의 타당성 판정은?",
        "options": [
            "① 지분율과 무관하게 언제나 FVPL이나 FVOCI 지정을 임의 적용할 수 있다.",
            "② 유의적 영향력이나 지배력을 행사하는 투자지분은 K-IFRS 제1109호 금융상품 적용 영역에서 제외되며, 원칙적으로 K-IFRS 제1028호 '관계기업과 공동기업 투자'에 따른 '지분법(Equity Method)' 평가를 필수 적용해야 하므로 1109호 범주 지정을 실행할 수 없다.",
            "③ 지분율 30%는 50% 미만이므로 1109호 금융자산 분류가 상시 강제된다.",
            "④ OCI 지정 시에만 지분법 적용을 면제하는 특례가 보장된다.",
            "⑤ 회계담당자 판단에 의거하여 매 분기별로 지분법과 공정가치법을 스위칭할 수 있다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 관계기업(유의적 영향력 행사, 통상 지분율 20%~50%)이나 종속기업(지배력 행사, 지분율 50% 초과) 투자는 K-IFRS 제1109호 금융상품 기준서 적용 대상에서 제외되며, 지분법(제1028호) 또는 연결회계기준이 지배하므로 일반 FVPL/FVOCI 지정 지분상품으로 분류할 수 없습니다.\n\n[오답 해설]\n① 지분 관계에 따른 법적 영향력이 성립하면 자의적 금융상품 분류 지정을 배제합니다.\n③ 지분율 30%는 유의적 영향력의 강력한 반증(20% 이상)이 존재하므로 지분법 적용 요건입니다.\n④, ⑤ 임의의 면제 특례나 매기 스위칭 허용 기법은 회계 기준서 상 존재하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "㈜A는 최초 취득 시점에 FVPL 금융자산으로 자동 분류된 보통주 지분상품을 보유 중이다. 차년도에 사업 모형의 대대적 변경(투자 목적의 영구 전환 등)이 이행되었다는 명목 하에, 이 지분상품을 'FVOCI 지정 금융자산'이나 '상각후원가(AC) 측정 금융자산'으로 재분류(Reclassification)하여 장부 가격을 조율하고자 할 때 K-IFRS 상의 허용 기준은?",
        "options": [
            "① 사업 모형이 바뀌었으므로 다음 분기 개시일부터 즉시 재분류를 이행한다.",
            "② K-IFRS 제1109호에 따라 '투자지분상품'은 어떠한 경우에도 최초 인식 후 다른 측정 범주로 재분류할 수 없다 (지분자산 재분류 전면 금지).",
            "③ AC 측정 자산으로는 재분류 가능하나, FVOCI 지정 변경은 불허한다.",
            "④ 금융자산 재분류는 채무상품과 지분상품 모두 이사회 승인 하에 전면 자유 허용된다.",
            "⑤ 기존 보유 평가액의 50% 한도로만 제한적 이체를 수용한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호 하에서 금융자산의 재분류는 오직 '채무상품(Debt instruments)'에 대해서만 사업모형 변경 시 극히 제한적으로 인정됩니다. 지분상품은 최초 지정 및 분류(FVPL 또는 최초 시점 FVOCI 지정)가 영구적으로 확정되며, 기중 재분류가 원천적으로 불가능합니다.\n\n[오답 해설]\n① 사업 모형이 바뀌더라도 지분상품은 재분류할 수 없습니다.\n③ 지분상품은 AC(상각후원가) 적용 자체가 불가능한 계약 요건을 가집니다.\n④, ⑤ 지분상품 재분류 불허 원칙에 위배되는 왜곡된 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "㈜A는 비상장 벤처기업의 소수 주식을 보유하고 있다. 시장 거래 활성도가 극히 낮아 공정가치를 신뢰성 있게 평가하기 매우 곤란하다. K-IFRS 상 공정가치 측정이 어려운 비상장 투자지분상품의 기말 평가 측정 대원칙으로 올바른 것은?",
        "options": [
            "① 공정가치 측정이 곤란하므로 예외적으로 '역사적 취득 원가(Historical Cost)'로 기말에 평가하여 장부 가격을 고정한다.",
            "② 시장 가격이 존재하지 않더라도 취득원가를 기말 평가액으로 사용할 수 없으며, 모든 가능한 정보(피투자사의 재무지표, 미래현금흐름 할인 기법 등)를 최대한 반영하여 공정가치를 신뢰성 있게 추정하여 평가 기재해야 한다.",
            "③ 평가가 곤란하므로 해당 자산을 자대 대차대조표에서 전액 제거(₩0)한다.",
            "④ 유형자산 감가상각 방식을 적용해 잔존 가치를 10%씩 매년 줄여 적는다.",
            "⑤ 세무상 고시지가법에 의거하여 일방적으로 가격을 하향 고정한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1109호는 금융자산의 원가 측정을 원칙적으로 불허합니다. 시장가치가 없는 비상장주식이라도 평가 시점의 사용 가능한 모든 정보를 동원하여 최선의 기법으로 공정가치를 추정·평가해야 합니다.\n\n[오답 해설]\n① 원가를 기말 평가값으로 무조건 대체 사용하는 과거의 규정은 현행 기준서에서 배제되었습니다.\n③ 자산 제거 요건에 부합하지 않는데 자산 총액을 ₩0으로 임의 제거하는 것은 회계 오류입니다.\n④, ⑤ 지분상품은 감가상각 자산이 아니며, 세법 상의 일방적 하향 고정 등은 재무보고 기준에 맞지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "㈜A는 최초 취득원가 ₩100,000 조건이 동일한 주식 2종을 각각 (가) FVPL 금융자산과 (나) FVOCI 지정 금융자산으로 분류하여 기말까지 보유하였다. 기말 결산 시 두 보통주의 공정가치는 모두 ₩150,000으로 상승 평가되었다. 이 기말 평가가 ㈜A의 결산 보고서 상 '당기순이익'과 '총포괄손익'에 미치는 누적 영향에 대한 비교로 가장 올바른 진술은?",
        "options": [
            "① 두 자산 모두 당기순이익을 ₩50,000만큼 증가시키고, 총포괄손익 또한 동일하게 ₩50,000 증가시킨다.",
            "② (가) FVPL 자산은 당기순이익과 총포괄손익을 각각 ₩50,000 증가시키는 반면, (나) FVOCI 자산은 당기순이익을 전혀 증가시키지 않고 기타포괄손익(총포괄손익)만 ₩50,000 증가시킨다.",
            "③ 두 범주 모두 당기순이익은 변화가 없으며, 총포괄손익만 각각 ₩50,000씩 증가시킨다.",
            "④ (가) FVPL은 당기순이익만 ₩50,000 늘리고 총포괄손익은 적정하며, (나) FVOCI는 영향이 없다.",
            "⑤ 두 자산의 회계처리 명칭 차이일 뿐 총 자산 변동 외에는 손익 영향이 양쪽 모두 ₩0으로 규정된다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 공정가치 평가 손익의 자산 범주별 총포괄 및 당기 손익 영향 비교:\n- FVPL 금융자산: 평가이익 ₩50,000이 당기손익(PL)으로 잡히므로 당기순이익을 ₩50,000 증가시키고, 이는 최종 총포괄손익도 ₩50,000 늘립니다.\n- FVOCI 지정 금융자산: 평가이익 ₩50,000이 OCI(기타포괄손익)로 잡히므로 당기순이익에는 전혀 영향을 주지 않고(₩0), 자본 항목 총합인 총포괄손익만 ₩50,000을 증가시킵니다.\n따라서 ②번 진술이 완벽히 맞습니다.\n\n[오답 해설]\n①, ③, ④, ⑤ FVPL의 당기순이익 귀속과 FVOCI 지정의 자본 OCI 귀속 격차를 정확하게 묘사하지 못한 오류 진술들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s05-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "FVOCI 지정 투자지분상품의 평가와 관련하여 자본에 누적된 '기타포괄손익누계액(평가손익누계액)'에 대한 K-IFRS 상의 사후 처리 규정으로 옳지 않은 것은?",
        "options": [
            "① 해당 지분상품이 영구적으로 제거(처분)되기 전 시점에는, 기중에 자본 내 평가이익누계액을 이익잉여금으로 임의 대체할 수 없다.",
            "② 해당 자산의 제거(처분) 시점에는 누적 기타포괄손익을 이익잉여금으로 자본 내부 이체할 수 있으며, 이 대체 행위는 필수 강제 규정이 아닌 기업의 선택 사항이다.",
            "③ 지분상품의 처분 시 실현된 손익은 결코 포괄손익계산서 상의 당기손익(처분손익)으로 재분류할 수 없다.",
            "④ 평가손익 잔액 중 일부를 처분 시점에 당기 지급수수료 비용과 직접 퉁치는 상계 분개는 기준서 위반이다.",
            "⑤ 지분상품의 공정가치 변동액이 마이너스로 돌아설 시, 자본 OCI 누계액을 거치지 않고 즉시 당기손상차손 비용으로 직행 처리해야 한다."
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ FVOCI 지정 투자지분상품의 가치가 하락하여 평가손실이 발생할 경우, 이는 무조건 기타포괄손익(OCI)으로 먼저 잡혀 자본 차감으로 적립되며, 당기 손상차손 비용으로 직접 처리하는 것은 기준서 위반입니다.\n\n[오답 해설]\n①, ②, ③, ④ FVOCI 지정 지분상품 자본 OCI 잔액의 대체 및 재분류조정 금지, 처분비용 순액 조정 등에 관한 타당한 설명 지문들입니다.",
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

print(f"Successfully added 25 questions. Total questions in database: {len(questions)}")
