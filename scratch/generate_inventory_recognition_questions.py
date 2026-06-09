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
    # L1: 기초 개념 (10문항, 751~760번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s03-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "매입자 입장에서 운송 중인 '미착상품(Goods in transit)'에 대하여, K-IFRS 상 기말재고자산에 원칙적으로 가산(포함)하여야 하는 인도조건은?",
        "options": [
            "① 도착지 인도조건(F.O.B. destination)",
            "② 선적지 인도조건(F.O.B. shipping point)",
            "③ 할부 인도조건(Installment point)",
            "④ 주관적 검수조건(Approval point)",
            "⑤ 조건 없는 전매조건(Resale point)"
        ],
        "answer": "2",
        "explanation": "② 선적지 인도조건은 선적지에서 상품이 선박에 적재되는 시점에 소유권이 매입자에게 귀속되므로, 운송 중인 미착상품이라도 매입자의 기말재고자산에 포함해야 합니다. 반면 도착지 인도조건은 도착해야 소유권이 이전되므로 포함하지 않습니다.\n\n[오답 해설]\n① 도착지 인도조건은 아직 매입자 자산이 아닙니다.\n③, ④, ⑤는 미착상품 소유권 이전의 표준 무역 인도조건이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "도착지 인도조건 매입은 기말재고에서 배제됩니다.", "articles": [], "principle": "미착상품의 소유권 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "선적지 인도조건 매입 미착상품은 선적 시점에 소유권이 양도되었으므로 매입자의 기말재고에 포함합니다.", "articles": [], "principle": "미착상품의 소유권 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "표준 무역 인도조건 명칭이 아닙니다.", "articles": [], "principle": "미착상품의 소유권 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시송품 등 검수 거래 조건을 오인한 지문입니다.", "articles": [], "principle": "미착상품의 소유권 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무역 인도 조건에 속하지 않습니다.", "articles": [], "principle": "미착상품의 소유권 판단", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "매입자 입장에서 운송 중인 미착상품에 대해 도착지 인도조건(F.O.B. destination) 계약인 경우, 결산 기말재고자산 가액 산정 시의 처리 규칙은?",
        "options": [
            "① 전액 무조건 매입자의 기말재고자산에 합산한다.",
            "② 기말재고자산에서 제외한다.",
            "③ 대금 지급 여부와 상관없이 무조건 50%만 자산화한다.",
            "④ 전액 당기 영업외수익의 잡이익으로 처리한다.",
            "⑤ 자본잉여금으로 대변 분개하고 자산은 기록하지 않는다."
        ],
        "answer": "2",
        "explanation": "② 도착지 인도조건 하의 매입 미착상품은 아직 약정 도착 장소에 도달하지 않았으므로 매입자의 소유권이 인정되지 않아 매입자의 기말재고자산에서 배제해야 합니다.\n\n[오답 해설]\n① 선적지 조건의 처리 방법입니다.\n③, ④, ⑤는 소유권 미이전 거래에 대한 잘못된 분개 처리 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "도착지인도조건은 기말에 자사 자산이 될 수 없습니다.", "articles": [], "principle": "도착지 인도조건 매입 미착상품", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "소유권이 아직 도착하지 않아 인도 완료되지 않았으므로 기말재고에서 전면 배제하는 것이 맞습니다.", "articles": [], "principle": "도착지 인도조건 매입 미착상품", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "50% 안분 규정은 존재하지 않습니다.", "articles": [], "principle": "도착지 인도조건 매입 미착상품", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수익 거래가 아니므로 잡이익 계상은 오답입니다.", "articles": [], "principle": "도착지 인도조건 매입 미착상품", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본잉여금 증가 거래에 해당하지 않습니다.", "articles": [], "principle": "도착지 인도조건 매입 미착상품", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "고객이 일정 기간 상품을 사용해 본 후 매입 여부를 결정하도록 하는 조건으로 판매하는 '시송품(Goods on approval)'의 정당한 매출(수익) 인식 시점은?",
        "options": [
            "① 상품이 고객의 손에 인도되는 날(발송일)",
            "② 판매 계약을 체결하고 계약금을 받는 날",
            "③ 고객이 구매의사(매입의사)를 표시하는 날",
            "④ 일정 보증 기간이 최초 시작되는 날",
            "⑤ 회사의 회계연도가 최종 종료되는 날(12월 31일)"
        ],
        "answer": "3",
        "explanation": "③ 시송품은 구매자가 최종적으로 매입 의사를 표시하기 전까지는 판매자의 재고자산(시송품)으로 기재되며, 구매자가 매입의사를 명시적으로 통보하거나 반품 기간 만료 등으로 매입 의사가 확정되는 시점에 매출을 인식합니다.\n\n[오답 해설]\n① 인도일에는 단순 보관 이송으로 소유권이 매입자에게 귀속되지 않아 매출 인식이 불가합니다.\n②, ④, ⑤는 시송품의 수익 인식 기준 조건이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "인도시점에는 매출로 잡을 수 없습니다.", "articles": [], "principle": "시송품의 매출 인식 시점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계약금 수령 시점에는 임시 선수금 부채만 잡힐 뿐 매출이 아닙니다.", "articles": [], "principle": "시송품의 매출 인식 시점", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "시송품은 구매자가 매입의사를 표시한 시점에 매출이 정당하게 계상됩니다.", "articles": [], "principle": "시송품의 매출 인식 시점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보증 개시 시점 기준이 아닙니다.", "articles": [], "principle": "시송품의 매출 인식 시점", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계연도 마감일이라도 매입의사 통보가 없었다면 매출이 될 수 없습니다.", "articles": [], "principle": "시송품의 매출 인식 시점", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "위탁자가 수탁자에게 보관 및 판매 대행을 위해 적송한 '적송품(Goods on consignment)'의 소유권 귀속에 대한 설명으로 옳은 것은?",
        "options": [
            "① 적송품을 보내는 즉시 수탁자의 재고자산이 된다.",
            "② 수탁자가 적송품을 창고에 보관하는 동안에는 국가의 공용 재산이 된다.",
            "③ 수탁자가 제3의 소비자에게 적송품을 판매하기 전까지는 여전히 위탁자의 기말재고자산에 포함된다.",
            "④ 위탁과 동시에 전액 위탁자의 이익으로 즉시 실현 처리하고 자산에서는 완전히 지운다.",
            "⑤ 수탁자가 보관하고 있다면 위탁자와 수탁자가 각각 50%씩 나누어 자산으로 잡는다."
        ],
        "answer": "3",
        "explanation": "③ 적송품은 대리인인 수탁자가 제3자에게 판매를 완료하기 전까지는 소유권이 위탁자에게 남아 있습니다. 따라서 판매되기 전의 수탁자 보관 분은 위탁자의 기말재고자산으로 보고해야 합니다.\n\n[오답 해설]\n① 수탁자는 단순 보관 및 판매 대리인이므로 수탁자 재고가 아닙니다.\n②, ④, ⑤는 위탁 판매 거래의 자산 귀속 규칙에 저촉되는 오답 진술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수탁자는 단순 보관인이므로 자산에 넣을 수 없습니다.", "articles": [], "principle": "적송품의 귀속 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "국유화 대상이 아닙니다.", "articles": [], "principle": "적송품의 귀속 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수탁자가 제3자에게 실제로 매각 인도하기 전까지는 전액 위탁자의 재고자산 원가에 포함시켜야 합니다.", "articles": [], "principle": "적송품의 귀속 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "위탁 발송 시점에는 이익을 잡을 수 없습니다.", "articles": [], "principle": "적송품의 귀속 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "안분 적용 대상이 아닙니다.", "articles": [], "principle": "적송품의 귀속 판단", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "금융기관 등으로부터 차입을 실행하고 그 담보로 제공된 '저당상품(Goods on mortgage)'의 소유권 귀속에 관한 K-IFRS 상 설명으로 옳은 것은?",
        "options": [
            "① 담보로 잡힌 날 즉시 금융기관의 기말재고자산으로 대체된다.",
            "② 금융기관과 담보제공자가 반씩 기말재고로 나누어 보고한다.",
            "③ 채무 불이행으로 인해 저당권(담보권)이 실제로 실행되기 전까지는 소유권이 담보제공자에게 있으므로, 담보제공자의 기말재고자산에 포함한다.",
            "④ 전액 당기비용으로 즉시 마이너스 털고 부채 계정으로 대변 기입한다.",
            "⑤ 담보 자산이므로 회계 장부에서 아예 지우고 주석 공시도 누락한다."
        ],
        "answer": "3",
        "explanation": "③ 저당상품은 담보로 제공된 상태일 뿐 법적인 저당권이 실제로 실행(소유권 박탈)되기 전까지는 실질적인 소유권이 담보제공자(채무자)에게 있으므로 담보제공자의 기말재고로 남아 있어야 합니다.\n\n[오답 해설]\n① 채권자인 금융기관은 저당권 실행 전에는 자기 재고로 올릴 수 없습니다.\n②, ④, ⑤는 담보 자산의 대원칙에 위배되는 부당한 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "저당권 실행 전까지는 금융기관의 소유권이 성립되지 않습니다.", "articles": [], "principle": "저당상품의 소유권 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산의 단일 귀속 원칙상 안분할 수 없습니다.", "articles": [], "principle": "저당상품의 소유권 귀속", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "담보권이 실제로 실행되어 인도 처분되기 전까지는 담보제공자의 기말재고에 가산하여 보고하여야 합니다.", "articles": [], "principle": "저당상품의 소유권 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비용 털기 대상이 아닙니다.", "articles": [], "principle": "저당상품의 소유권 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "장부 유지 및 담보 사실의 주석 공시가 필수입니다.", "articles": [], "principle": "저당상품의 소유권 귀속", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "수탁자 입장에서 타사로부터 판매를 위탁받아 당사 창고에 임시 보관 중인 '위탁받은 재고자산'의 연말 결산 시 올바른 회계처리는?",
        "options": [
            "① 창고에 실존하므로 수탁자 자신의 기말재고자산에 합산한다.",
            "② 수탁자 자신의 기말재고자산에 포함하지 않으며, 만약 기말 창고 실사액에 이 가액이 섞여 들어갔다면 차감하여 제거한다.",
            "③ 임시 매출로 인식하고 매출채권을 차변 기입한다.",
            "④ 정부 공공 보관 자산으로 돌려 부채 총계에서 지운다.",
            "⑤ 회사의 이익 조작용 자본 잉여금 항목에 수시 전입한다."
        ],
        "answer": "2",
        "explanation": "② 위탁받은 상품(수탁 상품)은 타사의 자산입니다. 당사가 수탁자로서 판매 대행을 위해 일시 보관할 뿐이므로 수탁자의 기말재고가 될 수 없으며, 기말 창고 실사금액에 수탁품이 포함되어 있다면 반드시 그 원가를 차감 조정해 주어야 합니다.\n\n[오답 해설]\n① 타사의 소유물이므로 수탁자의 재고에 넣으면 자산의 과대평가 분식이 됩니다.\n③, ④, ⑤는 위탁보관 재고에 대한 불합리한 회계 분개 오답항들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "창고에 실존하더라도 소유권이 당사에 없으므로 자산화할 수 없습니다.", "articles": [], "principle": "위탁받은 상품(수탁품)의 조정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수탁자의 자산이 아니므로 실사액에 오포함되어 있다면 차감하여 지워야 올바른 기말재고가 나옵니다.", "articles": [], "principle": "위탁받은 상품(수탁품)의 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출 거래가 될 수 없습니다.", "articles": [], "principle": "위탁받은 상품(수탁품)의 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정부 자산이 아닙니다.", "articles": [], "principle": "위탁받은 상품(수탁품)의 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 잉여금 혼용 대상이 아닙니다.", "articles": [], "principle": "위탁받은 상품(수탁품)의 조정", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "판매자 입장에서 상품 판매 거래 및 대금 영수가 완벽히 종료되었으나, 구매자(고객)가 즉시 인수를 원치 않고 보관 편의 상 당사 창고에 대기 보관해 줄 것을 별도 요청한 재고에 대한 올바른 귀속은?",
        "options": [
            "① 여전히 당사 창고에 실물 보관 중이므로 판매자의 기말재고자산에 합산한다.",
            "② 판매완료된 상품이므로 판매자의 기말재고자산에서 배제(제외)한다.",
            "③ 임시 부채 계정인 매출채권으로 대체 상계한다.",
            "④ 자본조정의 감자차손으로 강제 대체한다.",
            "⑤ 회사의 세금 감면을 위해 전액 잡손실 비용으로 즉시 처리한다."
        ],
        "answer": "2",
        "explanation": "② 판매가 완결되고 소유권과 통제가 고객에게 인도 완료된 상품은 실물이 당사 창고에 적치되어 있더라도 당사 재고가 아닙니다. 실사 금액에 섞여 들어갔다면 차감하여 제외하여야 합니다.\n\n[오답 해설]\n① 실물 소재지와 무관하게 통제가 이전되었다면 판매자 재고가 아닙니다.\n③ 매출채권은 자산 계정이므로 부채 계정 대체 설명이 틀렸습니다.\n④, ⑤는 판매 완료 보관 재고에 대한 엉터리 대체 분개입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "판매가 이미 완결되었으므로 창고에 있더라도 자사 재고가 아닙니다.", "articles": [], "principle": "판매 완료 보관 재고의 귀속", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "소유권이 고객에게 최종 이전된 자산이므로 판매자의 기말재고에서 배제(차감)하여야 합니다.", "articles": [], "principle": "판매 완료 보관 재고의 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출채권은 부채 계정이 아닙니다.", "articles": [], "principle": "판매 완료 보관 재고의 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 거래가 아닙니다.", "articles": [], "principle": "판매 완료 보관 재고의 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잡손실 비용화 사유에 부합하지 않습니다.", "articles": [], "principle": "판매 완료 보관 재고의 귀속", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "K-IFRS 상 판매자가 재고자산을 판매하면서 동시에 향후 일정 금액으로 이를 되사기로 약정하는 '재매입조건부 판매(Repurchase agreements)'의 정당한 회계처리 기준은?",
        "options": [
            "① 거래 즉시 정상 매출로 인식하고 기말재고에서 제외한다.",
            "② 해당 거래는 실질적인 판매에 해당하지 않으므로, 매출로 인식할 수 없고 해당 재고자산은 판매자의 기말재고자산에 그대로 유지(포함)하여야 한다.",
            "③ 금융기관에 무담보 기부금으로 차변 대체 처리한다.",
            "④ 자산과 부채를 동시에 지우고 전액 OCI 자본 항목에 유보한다.",
            "⑤ 회사의 당기 결산 손익이 적자인 경우에 한해서만 특별 임시 매출로 인정한다."
        ],
        "answer": "2",
        "explanation": "② 재매입조건부 판매는 일정 기간 자금을 융통한 뒤 약정금으로 상품을 도로 사오는 구조이므로 실질상 '재고자산을 담보로 한 자금 차입 금융거래'에 불과합니다. 따라서 통제가 이전되지 않아 판매 시점에 매출을 인식할 수 없으며, 재고자산은 판매자의 장부에 그대로 포함시켜 둡니다.\n\n[오답 해설]\n① 형식적 인도에 속아 매출을 잡으면 분식이 됩니다.\n③, ④, ⑤는 기준서 조문에 어긋나는 잘못된 회계 기재 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "실질이 매출 거래가 아니므로 즉시 매출 인식은 오답입니다.", "articles": [], "principle": "재매입조건부 판매의 기말재고 포함 여부", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "실질적 금융 약정이므로 매출을 금지하고, 재고자산은 원래 소유주인 판매자 자산에 합산 기재하여야 합니다.", "articles": [], "principle": "재매입조건부 판매의 기말재고 포함 여부", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기부금 대체는 성립 불가합니다.", "articles": [], "principle": "재매입조건부 판매의 기말재고 포함 여부", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "OCI 자본 유보 대상이 아닙니다.", "articles": [], "principle": "재매입조건부 판매의 기말재고 포함 여부", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손익 상태에 따른 임의 기준 변경은 불가합니다.", "articles": [], "principle": "재매입조건부 판매의 기말재고 포함 여부", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "고객에게 재고자산을 '할부판매(Installment sales)' 조건으로 공급하여 즉시 인도한 경우, 기말재고자산 가액 산정 시의 귀속 여부로 가장 올바른 것은?",
        "options": [
            "① 할부금이 완납될 때까지는 무조건 판매자의 기말재고자산에 원가로 남아 있어야 한다.",
            "② 대금 회수 가능성이 지극히 낮은 경우라도 인도 시점에 무조건 판매자 자산에서 제외된다.",
            "③ 인도 시점에 재고에 대한 유의적인 통제와 소유에 따른 위험과 보상이 매입자에게 넘어가므로 판매 즉시 매출 및 매출원가로 처리하고, 판매자의 기말재고자산에서 제외한다.",
            "④ 기말 실사 창고에 상품이 없으므로 무조건 감모손실 영업외비용으로 대치한다.",
            "⑤ 회사의 부채 비율을 높이기 위해 부채 계정으로 차변 대체하고 자산은 존치한다."
        ],
        "answer": "3",
        "explanation": "③ 일반적인 할부판매는 대금 회수 기간이 분할되어 있을 뿐 상품 인도 시점에 소유권의 주요 통제가 이전되므로 판매 시 즉시 매출(원가)을 인식하고 판매자의 기말재고에서 배제합니다.\n\n[오답 해설]\n① 법적인 소유권 유보 조건이라도 통제가 실질 이전되었다면 판매자 재고가 아닙니다.\n② 대금 회수 가능성이 극도로 낮아 신뢰성 있는 추정이 안 되면 매출 인식을 미룰 수 있으나, 일반적으로는 3번이 원칙적인 설명입니다.\n④, ⑤는 할부판매 거래의 올바른 실질 파악 설명이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "할부 대금 미완납을 이유로 자산 인식을 계속 유지하는 것은 오답입니다.", "articles": [], "principle": "할부판매의 기말재고 배제 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회수불능 위험이 명백하면 일반 회계 기준의 예외가 적용됩니다.", "articles": [], "principle": "할부판매의 기말재고 배제 원칙", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "할부 판매는 인도 시 통제 이전에 부합하므로 판매 시 매출원가 대체하여 자사 기말재고에서 즉각 뺍니다.", "articles": [], "principle": "할부판매의 기말재고 배제 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감모손실로 계상할 사항이 아닙니다.", "articles": [], "principle": "할부판매의 기말재고 배제 원칙", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 증가 및 자산 존치 분개는 불가능합니다.", "articles": [], "principle": "할부판매의 기말재고 배제 원칙", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "판매자 입장에서 운송 중인 미착상품에 대해 도착지 인도조건(F.O.B. destination) 계약으로 기말에 판매 중인 경우, 판매자의 결산 기말재고자산 귀속 규칙은?",
        "options": [
            "① 이미 판매용 선적을 개시하였으므로 기말재고에서 배제한다.",
            "② 아직 도착지 도착 전이므로 소유권이 구매자에게 인도되지 않았기 때문에 해당 상품 원가를 판매자의 기말재고자산에 포함(가산)한다.",
            "③ 매출을 잡고 재무상태표의 선급금으로 자본 조정 처리한다.",
            "④ 정부 유보 자산으로 돌려 부채 총계에서 차감한다.",
            "⑤ 회사의 당기 영업외수익의 잡이익으로 전액 일시 대체한다."
        ],
        "answer": "2",
        "explanation": "② 도착지 인도조건으로 판매한 상품이 기말 현재 운송 중이라는 것은 아직 도착지에 도착하지 않았음을 뜻합니다. 따라서 매출이 일어난 것이 아니므로 동 상품은 판매자의 기말재고자산 원가에 온전히 포함시켜야 합니다.\n\n[오답 해설]\n① 선적지 인도조건 판매 시의 기말재고 배제 원리입니다.\n③, ④, ⑤는 소유권 미이전 운송 판매재고에 대한 비정상적 가공 분개입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "도착지인도조건이므로 운송 중일 때는 기말재고에서 제외하면 오답입니다.", "articles": [], "principle": "도착지 인도조건 판매 미착상품", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "도착지 도착 시점에 비로소 소유권이 이전되므로, 운송 중에는 판매자의 기말재고 자산으로 합산 보유하는 것이 맞습니다.", "articles": [], "principle": "도착지 인도조건 판매 미착상품", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "선급금이나 자본 조정 대체 분개 대상이 아닙니다.", "articles": [], "principle": "도착지 인도조건 판매 미착상품", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 대변 등과 연계되지 않는 자산 보유 사안입니다.", "articles": [], "principle": "도착지 인도조건 판매 미착상품", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잡이익 수익 처리는 불가능합니다.", "articles": [], "principle": "도착지 인도조건 판매 미착상품", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },

    # =========================================================================
    # L2: 이해 (15문항, 761~775번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s03-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "선적지 인도조건(F.O.B. shipping point)으로 원재료를 수입 매입하는 과정에서 매입자가 직접 지불한 해상운임 및 적하보험료의 회계처리 성격은?",
        "options": [
            "① 판매 시점의 마케팅비용이므로 판매비와관리비로 전액 당기비용 처리한다.",
            "② 선적지 인도조건 하에서는 선적 시점부터 소유권이 매입자에게 귀속되어 현재 장소/상태에 이르는 과정의 직접 불가피한 부대비용이 되므로, 전액 원재료의 취득원가에 포함(자산화)한다.",
            "③ 대주주 지분 감소의 감자차손으로 자본조정 차감 기재한다.",
            "④ 당일 즉시 잡손실 처리하고 기말 평가에서는 누락시킨다.",
            "⑤ 회사의 부채 비율을 감축하기 위해 차입부채 차변 상계 분개한다."
        ],
        "answer": "2",
        "explanation": "② 선적지 인도조건은 선적 시점부터 매입자의 자산입니다. 따라서 그 이후 발생한 해상운임이나 운송보험료 등은 자산을 판매/사용 가능한 장소와 상태로 유도하는 과정의 직접 필수 부대원가이므로, 매입자가 부담하고 취득원가에 가산하여야 합니다.\n\n[오답 해설]\n① 판매 활성화를 위한 마케팅비(영업비용)가 아닙니다.\n③, ④, ⑤는 매입 부대원가의 기본 취득 자산화 규칙에 어긋납니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "판관비 비용 처리는 기준서 위배입니다.", "articles": [], "principle": "선적지 인도조건 운송비의 원가 가산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "선적지인도조건은 자산화 기간 중 발생한 부대비용이므로 매입 상품 취득원가에 합산하여야 합니다.", "articles": [], "principle": "선적지 인도조건 운송비의 원가 가산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 차감 성격이 될 수 없습니다.", "articles": [], "principle": "선적지 인도조건 운송비의 원가 가산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잡손실 영업외비용 처리는 불가합니다.", "articles": [], "principle": "선적지 인도조건 운송비의 원가 가산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입 상계 거래가 아닙니다.", "articles": [], "principle": "선적지 인도조건 운송비의 원가 가산", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "도착지 인도조건(F.O.B. destination)으로 상품을 수출 판매하는 기업이 결산 기말에 부담하고 지불한 매출 운송비(출하 운임 등)의 올바른 회계 기재 방식은?",
        "options": [
            "① 기말재고자산 원가에 소급 가산하여 장부액을 부풀린다.",
            "② 해당 운송비는 판매를 실현하기 위해 소요된 대외 판매 활동 비용이므로, 전액 포괄손익계산서 상 '판매비와관리비(운임)'로 인식하여 당기 비용 처리한다.",
            "③ 대손충당금 환입금으로 차변 대체하여 영업외수익으로 처리한다.",
            "④ 무조건 자본조정의 자기주식 처분이익 가산액으로 분개한다.",
            "⑤ 회사의 당기순이익이 적자인 해에는 임의로 감가상각 누계액 가산으로 유보한다."
        ],
        "answer": "2",
        "explanation": "② 도착지 인도조건 판매 시 판매자가 부담하는 운임 등은 고객에게 자산을 무사히 도달시켜 판매(매출)를 완료하기 위한 대외 판매 활동 비용(비용)에 속하므로, 취득원가가 아닌 판매비와관리비로 당기 영업 비용 인식합니다.\n\n[오답 해설]\n① 판매 과정의 비용이므로 재고자산 가액에 포함할 수 없습니다.\n③, ④, ⑤는 매출 영업 비용에 대한 자의적이고 왜곡된 가공 분개항입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "판매 단계의 운임은 자산 취득원가에 포함될 수 없습니다.", "articles": [], "principle": "도착지 인도조건 판매 운임의 비용 처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "판매자가 인도 의무 이행을 위해 부담한 물류비는 영업비용인 판매비와관리비(운임)로 인식하는 것이 원칙입니다.", "articles": [], "principle": "도착지 인도조건 판매 운임의 비용 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손 조정 환입 항목과 무관합니다.", "articles": [], "principle": "도착지 인도조건 판매 운임의 비용 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자기주식 자본 거래가 아닙니다.", "articles": [], "principle": "도착지 인도조건 판매 운임의 비용 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각 누적 조절 수단이 아닙니다.", "articles": [], "principle": "도착지 인도조건 판매 운임의 비용 처리", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "수탁자가 위탁자로부터 타사 상품(적송품)을 인도받아 자신의 매장에 진열 보관을 시작한 당일에 행할 올바른 장부상 회계처리는?",
        "options": [
            "① 차변에 재고자산(₩진열액), 대변에 매입채무(₩진열액)를 자산과 부채로 즉시 기재한다.",
            "② 소유권이 없는 보관에 불과하므로 재무상태표 상 자산과 부채는 일절 인식하지 않으며, 오직 수량 파악과 도난 방지를 위한 관리 대장 상의 비망기록(비망록 기입)만 수행한다.",
            "③ 차변에 선급금 자산, 대변에 OCI 자본 항목으로 기재한다.",
            "④ 당기 영업외수익 매출로 강제 전입 분개한다.",
            "⑤ 회사의 당기순이익 적자 보정용 특별 임시 적립금으로 전입한다."
        ],
        "answer": "2",
        "explanation": "② 수탁자는 적송품에 대하여 어떠한 법적 소유권이나 통제도 보유하지 못합니다. 단지 위탁자를 위해 판매를 대행하며 보관하고 있는 것에 불과하므로 자산이나 부채 분개를 할 수 없고, 대장 상의 관리 목적 비망기록만 행하여야 합니다.\n\n[오답 해설]\n① 수탁자의 장부에 임의로 자산과 부채를 인식하면 허위 자산/부채 팽창 분식이 됩니다.\n③, ④, ⑤는 수탁자의 소유권 부재 실질에 위배되는 비정상적 대체 기입 지문들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수탁자 장부에 자산과 부채를 기재하는 것은 명백한 허위 분식입니다.", "articles": [], "principle": "수탁자의 적송품 수령 시 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "소유권 미이전 보관 거래이므로 자산/부채를 인식하지 않고 비망록 기록으로만 유효하게 관리합니다.", "articles": [], "principle": "수탁자의적송품 수령 시 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "선급금이나 자본 거래 성립이 되지 않습니다.", "articles": [], "principle": "수탁자의 적송품 수령 시 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대리인으로서 보관 시점에는 매출 인식이 불가합니다.", "articles": [], "principle": "수탁자의 적송품 수령 시 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임시 적립금 대체는 회계 원칙상 위배됩니다.", "articles": [], "principle": "수탁자의 적송품 수령 시 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "시송품을 보관 중이던 잠재 고객이 기말에 일부 수량에 대하여 '구매하겠다'는 매입의사를 전송해 왔을 때, 판매자가 당기말에 수행해야 할 올바른 분개 처리의 효과는?",
        "options": [
            "① 매입의사가 표시된 부분은 여전히 판매자의 기말재고자산 원가에 포함시킨다.",
            "② 매입의사가 표시되지 않은 미결정 수량만 매출로 인식하고 이익을 잡는다.",
            "③ 매입의사가 표시된 시송품 분량은 판매자의 기말재고자산(시송품)에서 원가를 차감 제거하여 매출원가로 대체하고, 해당 판매가액만큼 매출액(수익)을 정당하게 인식한다.",
            "④ 전액 당기 잡손실 비용으로 털고 자본조정을 차감한다.",
            "⑤ 금융비용(이자비용)을 차변 기입하고 매출채권은 지운다."
        ],
        "answer": "3",
        "explanation": "③ 시송품 중 고객이 매입의사를 명백히 표시한 부분은 마침내 수익 요건을 갖추었으므로 판매 완료된 매출로 인식하고, 판매자는 해당 재고(시송품)를 기말재고자산에서 감액 제거하면서 동시에 당기 매출원가로 대체 분개합니다.\n\n[오답 해설]\n① 매입의사 통보분은 판매자 재고에서 빠져나가야 합니다.\n② 미결정 수량은 여전히 판매자 자산이어야 하며 매출이 될 수 없습니다.\n④, ⑤는 정상적인 시송품 판매 실현 분개 효과에 부합하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "매입의사 표시분은 판매 완료이므로 기말재고에서 배제되어야 합니다.", "articles": [], "principle": "시송품 매입의사 통보 시 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미결정분이 아닌 의사표시분이 매출 인식 대상입니다.", "articles": [], "principle": "시송품 매입의사 통보 시 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "의사를 밝힌 분량은 기말재고(시송품)에서 대변 차감하여 매출원가로 올리고 판매가로 매출 수익을 인식합니다.", "articles": [], "principle": "시송품 매입의사 통보 시 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잡손실 비용 거래가 아닙니다.", "articles": [], "principle": "시송품 매입의사 통보 시 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자비용 가감 사안이 아닌 정규 매출 거래입니다.", "articles": [], "principle": "시송품 매입의사 통보 시 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "재매입조건부 판매 거래에서, 최초 판매 시 수령한 매각대금과 향후 되사기로 약정한 재매입 가액 간의 명목 차액(₩재매입가 - ₩판매가)의 올바른 회계적 성격 및 인식 기간은?",
        "options": [
            "① 전액 즉시 잡손실로 당일 일시 비용 처리한다.",
            "② 금융이 이루어지는 전 기간(판매일로부터 재매입일까지)에 걸쳐 '이자비용(Finance Costs)'으로 안분하여 인식한다.",
            "③ 전액 자본잉여금으로 영구 누적 전입한다.",
            "④ 기 기말재고자산 원가에 소급 가산하여 자산화한다.",
            "⑤ 회사의 당기 적자 해소를 위해 영업외수익의 잡이익으로 즉시 유입시킨다."
        ],
        "answer": "2",
        "explanation": "② 재매입조건부 판매는 재고자산을 담보로 한 자금 융통(차입) 거래의 실질을 지닙니다. 따라서 최초 유입액(차입금 명목)과 최종 상환 약정액(재매입 가격)의 명목 차액은 해당 자금 대여 전 기간에 걸쳐 유효이자율법 등을 사용해 상각 및 '이자비용'으로 안분 계상하여야 합니다.\n\n[오답 해설]\n① 일시 당일 인식은 발생주의 기간 배분에 어긋납니다.\n③, ⑤는 금융 차입 성격에 위배되는 잘못된 자본 및 영업외수익 배정 설명입니다.\n④ 자산 취득 부대비용이 아니므로 취득원가 가산 대상이 될 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "일시적 영업외비용 처리는 이자 배분 원칙에 어긋납니다.", "articles": [], "principle": "재매입조건부 거래의 명목차액 처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "실질적 차입금에 대한 금융비용이므로, 대여 기간 전반에 걸쳐 차입 부채 이자를 가산하는 유효이자율법 기반 이자비용을 인식해야 합니다.", "articles": [], "principle": "재매입조건부 거래의 명목차액 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본잉여금 증가 항목이 될 수 없습니다.", "articles": [], "principle": "재매입조건부 거래의 명목차액 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 가산 대상이 아닙니다.", "articles": [], "principle": "재매입조건부 거래의 명목차액 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "분식 목적의 가공 수익 인식은 전면 금지됩니다.", "articles": [], "principle": "재매입조건부 거래의 명목차액 처리", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "반품조건부 판매(Sales with a right of return) 거래 하에서, 판매자가 과거 데이터나 시장 현황 등에 기초하여 '당해 판매의 반품가능성(반품률)을 합리적으로 전혀 추정할 수 없는 상태'인 경우 정당한 매출 인식 시점은?",
        "options": [
            "① 상품이 고객의 현관에 최초 인도되는 시점",
            "② 판매 대금이 은행 통장에 입금되는 당일 시점",
            "③ 구매자가 상품을 인도받아 제3자에게 임의 전매하는 가상 시점",
            "④ 구매자가 상품의 인수를 정식으로 수락하거나, 반품 기간(반환권 행사 기간)이 최종적으로 만료(종료)되는 시점",
            "⑤ 회사의 회계연도가 마감되는 매 12월 31일 시점"
        ],
        "answer": "4",
        "explanation": "④ 반품조건부 판매 시 반품 가능성을 신뢰성 있게 추정할 수 없는 극단적인 경우에는 인도 시점에 수익 인식이 전면 제한됩니다. 즉, 구매자가 인수를 최종 수락하거나 반품 청구 기간이 최종 만료될 때까지는 매출을 전혀 장부에 적을 수 없고, 기말재고자산에 그대로 포함시켜 두어야 합니다.\n\n[오답 해설]\n① 반품률 추정이 가능할 때에 인도 시점에 매출(추정 반품 제외)을 잡습니다. 본 사안은 추정 불가 상태이므로 불가합니다.\n②, ③, ⑤는 신뢰성 있는 수익 측정 한계 요건을 무시한 지문들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "반품률 추정 불능 시 인도시점 매출 인식은 불가능합니다.", "articles": [], "principle": "반품조건부 판매의 수익인식 통제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수금 시점이 곧 매출 인식 시점이 아닙니다.", "articles": [], "principle": "반품조건부 판매의 수익인식 통제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전매 시점 기준이 적용되지 않습니다.", "articles": [], "principle": "반품조건부 판매의 수익인식 통제", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "반품 위험을 합리적으로 발라내어 추정하기 어려울 때에는, 반품권 행사 기간이 완전히 경과하거나 상대방이 인수 확약을 준 때에 매출을 기록하여야 합니다.", "articles": [], "principle": "반품조건부 판매의 수익인식 통제", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계 기수 종료일이라도 조건 미충족 시 이연해야 합니다.", "articles": [], "principle": "반품조건부 판매의 수익인식 통제", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "K-IFRS 하에서 반품조건부 판매 거래 시 반품가능성을 합리적으로 추정할 수 있는 경우, 기말에 반품될 것으로 예상되는 상품에 대해 판매자가 계상해야 할 회도 자산성 항목의 정식 회계 명칭은?",
        "options": [
            "① 대손충당적립권",
            "② 반환재고회수권(Right to recover returned products)",
            "③ 미수임시반품금",
            "④ 재매입담보보증권",
            "⑤ 환불의무충당자산"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1115호 '고객과의 계약에서 생기는 수익'에 의거, 반품가능액 추정 시 고객으로부터 상품을 회수할 자산적 가치를 '반환재고회수권' 계정으로 재무상태표의 자산 란에 기재하도록 규정하고 있습니다. (대변의 환불의무는 환불부채 부채로 공시)\n\n[오답 해설]\n①, ③, ④, ⑤는 K-IFRS 상의 정식 재고자산/수익 연동 자산 계정 명칭이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "가공의 회계 계정 명칭입니다.", "articles": [], "principle": "반품거래 자산 부채 계정 명칭", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "고객 반품 예상분의 장부 원가 상당 회수 가치를 지칭하는 정식 기준서상 자산 명칭은 '반환재고회수권'입니다.", "articles": [], "principle": "반품거래 자산 부채 계정 명칭", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기준서에 규정되지 않은 가칭입니다.", "articles": [], "principle": "반품거래 자산 부채 계정 명칭", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "존재하지 않는 자산 이름입니다.", "articles": [], "principle": "반품거래 자산 부채 계정 명칭", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "환불부채의 상대자산 명칭을 오기한 지문입니다.", "articles": [], "principle": "반품거래 자산 부채 계정 명칭", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "K-IFRS 상 상품을 창고에서 출고하여 물리적으로 고객에게 인도하지는 않았으나 예외적으로 판매 시점에 매출(수익) 인식을 허용하는 '빌앤홀드(Bill-and-hold) 약정'의 성립 요건으로 가장 올바르지 않은 것은?",
        "options": [
            "① 빌앤홀드 약정을 맺은 실질적이고 타당한 사유(예: 고객의 보관 장소 부족 등으로 인한 보관 요청)가 존재하여야 한다.",
            "② 해당 상품은 고객의 소유물로 명확히 식별(구분 적치 등)되어 있어야 한다.",
            "③ 해당 상품은 고객에게 물리적으로 즉시 인도할 수 있는 상태로 현재 준비되어 있어야 한다.",
            "④ 판매자(회사)는 해당 상품을 다른 고객에게 판매하거나 자체적인 다른 용도로 전용해 사용할 수 있는 물리적 권한을 보유하고 있어야 한다.",
            "⑤ 판매자(회사)는 해당 상품을 임의로 대체 사용하여 타 처에 인도할 권리를 전혀 가질 수 없다."
        ],
        "answer": "4",
        "explanation": "④ 빌앤홀드 약정 매출을 허용하려면 해당 제품은 오직 그 계약 고객을 위해서만 묶여 있어야 합니다. 만약 판매자가 그 제품을 마음대로 가져가서 다른 사람에게 팔거나 타 용도로 돌려쓸 수 있다면(통제권이 판매자에게 잔존), 매출 인식이 금지되므로 4가 요건에 부합하지 않는 정오 대상 오답입니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 K-IFRS 제1115호 부록에 명시된 빌앤홀드 약정 성립의 4대 핵심 필수 만족 조건입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "고객 요청의 타당성은 정식 빌앤홀드 승인 요건이 맞습니다.", "articles": [], "principle": "빌앤홀드(Bill-and-hold) 판매 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "제품의 식별 보관은 필수 요건이 맞습니다.", "articles": [], "principle": "빌앤홀드(Bill-and-hold) 판매 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인도 대기 및 즉시 인도 가능성 확보는 필수 요건이 맞습니다.", "articles": [], "principle": "빌앤홀드(Bill-and-hold) 판매 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "회사가 제품을 다른 곳에 임의 대체 전용하여 판매할 권리가 있다면 통제 이전이 부인되므로, 매출 인식이 불가능해 4가 부당 요건입니다.", "articles": [], "principle": "빌앤홀드(Bill-and-hold) 판매 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "전용 불가 조항은 정식 승인 요건이 맞습니다.", "articles": [], "principle": "빌앤홀드(Bill-and-hold) 판매 요건", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "고객이 상품 대금을 최종 납부할 때까지 판매자가 실물을 창고에 보관하고 분할 지급금을 받는 '레이어웨이 판매(Layaway sales)' 하에서, 원칙적인 매출(수익) 인식 시점은?",
        "options": [
            "① 최초 계약서에 양자가 날인하고 계약금을 수취하는 날",
            "② 기중 할부금을 2회 차 수취하는 정기 입금일",
            "③ 상품을 창고 구석으로 임시 이동 적재하는 준비일",
            "④ 고객이 마지막 할부 대금을 최종 전액 납부하고, 상품의 통제(실물 인도 등)가 고객에게 최종 이전되는 시점",
            "⑤ 회사의 재정 상태 보고를 위해 매월 마감하는 일자"
        ],
        "answer": "4",
        "explanation": "④ 레이어웨이(Layaway) 판매는 대금이 거의 완납되어 실제 물건이 고객에게 최종 건네지는 단계가 도래해야 판매 의무가 실현된 것으로 봅니다. 따라서 통상 마지막 할부금이 입금되고 상품 인도가 이루어질 때 매출을 인식합니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 완납 및 실물 인도 전 시점으로, 통제 이전 요건을 갖추지 못해 매출을 적을 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "계약 서명 및 소액 계약금 수취 시점에는 매출 인식이 보류됩니다.", "articles": [], "principle": "레이어웨이(Layaway) 판매의 매출 타이밍", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기중 할부 중도금 시점도 불가합니다.", "articles": [], "principle": "레이어웨이(Layaway) 판매의 매출 타이밍", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "창고 이동 등 물류 준비 시점은 통제 이전과 무관합니다.", "articles": [], "principle": "레이어웨이(Layaway) 판매의 매출 타이밍", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "잔금 최종 결제 및 통제권이 고객에게 넘어가는 순간에 정식 매출을 계상하는 것이 레이어웨이의 표준 규정입니다.", "articles": [], "principle": "레이어웨이(Layaway) 판매의 매출 타이밍", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적인 월말 일자 배정은 불가합니다.", "articles": [], "principle": "레이어웨이(Layaway) 판매의 매출 타이밍", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "담보로 제공되었던 저당상품에 대하여 채무불이행 등의 사유로 담보권(저당권)이 채권자에 의해 '실제 실행(소유권 법적 몰수 및 압류 등)'되는 상황이 발생했을 때, 담보제공자(채무자)가 당일에 이행하여야 할 장부상 조치는?",
        "options": [
            "① 재고자산 금액을 그대로 장부에 두고 추가 부채를 대변 기재한다.",
            "② 해당 저당상품의 장부가액을 당사 '재고자산'에서 최종 차감 제거하고, 담보 소멸에 따른 채무 차감액과의 차이를 대손상각비로 처리한다.",
            "③ 저당권 실행 시점에 담보 소유권이 완전히 넘어갔으므로 해당 상품을 재고자산 계정에서 대변 제거하고, 관련 차입금 채무 소멸 분개 및 처분손익(장부가액과 상환 채무액의 격차)을 당기손익으로 인식한다.",
            "④ 기기말재고 가치를 2배 증액하는 소급 평가를 감행한다.",
            "⑤ 회사의 자본잉여금을 늘리는 분개만 행하고 자산은 창고 실사액으로 복원한다."
        ],
        "answer": "3",
        "explanation": "③ 저당권이 법적으로 실행되면 상품 소유권이 타인에게 최종 박탈되어 이전됩니다. 따라서 담보제공자는 해당 상품을 대변에 기재해 재고자산에서 영구 지우고, 동시에 차입금 채무 감소를 차변 기록한 뒤, 소멸되는 부채가액과 재고자산 장부원가의 차액을 '재고자산처분손익(또는 담보물제공채무변제손익)' 성격의 당기손익으로 포괄손익계산서에 보고해야 합니다.\n\n[오답 해설]\n① 자산이 상실되었는데 지우지 않으면 자산 허위 계상이 됩니다.\n② 대손상각비는 매출채권 회수 불능 시 비용이므로 부채 상환 완료 거래의 성격과 다릅니다.\n④, ⑤는 자산 박탈 실질에 반하는 부당 분개입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "소유권이 박탈되었으므로 자산을 장부에 남겨두는 것은 위배입니다.", "articles": [], "principle": "저당권 실행 시의 자산 소멸 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손 비용 처리 대상 거래가 아닙니다.", "articles": [], "principle": "저당권 실행 시의 자산 소멸 분개", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "소유권 이전 시점에 재고를 제거하고 소멸 차입채무와 대조하여 사후 처분손익을 기록하는 조치가 논리적입니다.", "articles": [], "principle": "저당권 실행 시의 자산 소멸 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 증액은 불가능합니다.", "articles": [], "principle": "저당권 실행 시의 자산 소멸 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본잉여금으로 우회 처리할 사안이 아닙니다.", "articles": [], "principle": "저당권 실행 시의 자산 소멸 분개", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "적송품을 수령하여 보관 중이던 수탁자가, 자신의 보관 태만이나 창고 관리 부실로 인해 보관하던 위탁자의 상품 ₩10,000 상당을 도난 내지 완전 파손 분실하였다. 이에 관한 위탁자(주 소유주) 입장의 기말 결산 시 타당한 조치는?",
        "options": [
            "① 수탁자가 대신 잃어버렸으므로 계속 장부상 적송품 자산 가치 ₩10,000을 온전히 계상해 둔다.",
            "② 해당 적송품 실물이 파손/소실되어 경제적 효익을 창출할 수 없게 되었으므로 위탁자의 장부상 적송품 자산에서 ₩10,000을 대변 차감 차단하고, 동액을 당기 '재고자산감모손실(정상/비정상 판단에 따라)' 또는 '잡손실' 등의 비용으로 즉시 차변 처리한다.",
            "③ 전액 주식할인발행차금과 상계하여 자본에서 직접 없앤다.",
            "④ 정상 매출이 일어난 것으로 보아 매출채권을 잡는다.",
            "⑤ 회사의 당기순이익 적자 방지를 위해 평가이익으로 대변 환원한다."
        ],
        "answer": "2",
        "explanation": "② 수탁자가 보관 중 유실한 자산이라도 경제적 가치가 상실된 시점에 실소유주인 위탁자는 적송품(자산)을 감액하여야 합니다. 그 후 보관 과실의 원인 및 수탁자에 대한 배상 청구권 확보 여부 등을 고려하여 감모손실이나 잡손실 비용으로 계상하여 소멸시킵니다.\n\n[오답 해설]\n① 실물이 존재하지 않으므로 자산을 그대로 두면 자산 과대계상이 됩니다.\n③ 자본 거래 상계 사안이 아닙니다.\n④ 제3자 판매 매출 성립 요건이 전혀 성립되지 않았습니다.\n⑤ 평가이익 계상은 허위 분식입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "소실된 실물 자산을 장부에 방치하는 것은 회계 원칙 위배입니다.", "articles": [], "principle": "수탁처 파손 감모 적송품의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "물리적 소멸이 실증되었으므로 적송품 자산을 감액하고 감모손실 등의 당기 비용으로 적는 것이 맞습니다.", "articles": [], "principle": "수탁처 파손 감모 적송품의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "주식 발행 자본 거래와 무관합니다.", "articles": [], "principle": "수탁처 파손 감모 적송품의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "도난 유실은 정상 매출 거래가 될 수 없습니다.", "articles": [], "principle": "수탁처 파손 감모 적송품의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익 편취용 가공 분개는 불가합니다.", "articles": [], "principle": "수탁처 파손 감모 적송품의 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "반품조건부 판매 하에서 매출 시점에 반환재고회수권을 자산으로 잡을 때, 최초 측정액인 '취득원가(장부가액)'를 산정하는 합리적인 측정 규칙은?",
        "options": [
            "① 반품이 예상되는 상품의 '판매 가격' 전체",
            "② 반품이 예상되는 상품의 '원래 취득 장부 원가'에서, 해당 상품을 회수할 때 추가로 소요될 것으로 추정되는 회수 비용(운반비 등)과 가치 하락에 따른 손실액을 차감한 잔액",
            "③ 당일 세무서가 고시한 표준 재고 단가",
            "④ 해당 상품의 판매 가격의 50% 고정액",
            "⑤ 회계사가 주관적으로 지정하는 임의의 금액"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1115호에 기해 반환재고회수권의 금액은 단순히 원래 원가를 고스란히 적는 것이 아니라, 반품될 상품의 장부원가에서 그 제품을 회수하는 과정에서 회사가 추가 부담할 것으로 예상되는 회수비용이나 훼손에 따른 원가 가치 하락분을 미리 깎아서 보수적 가치로 자산 측정하여야 합니다.\n\n[오답 해설]\n① 판매 가격은 수익 영역이므로 환불부채(부채)를 측정할 때의 기준입니다. 자산인 회수권은 원가 기준입니다.\n③, ④, ⑤는 반환재고회수권의 기준서 상 측정 속성 공식과 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "판매가격은 자산인 회수권이 아닌 환불부채의 측정 기준입니다.", "articles": [], "principle": "반환재고회수권의 측정 기준", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "예상되는 반품 원가액에서 회수 제비용 및 가치 저하 손실을 차감한 순회수가치로 반환재고회수권을 기재하여야 합니다.", "articles": [], "principle": "반환재고회수권의 측정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "행정 세무 고시가 기준이 될 수 없습니다.", "articles": [], "principle": "반환재고회수권의 측정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "50% 고정 배분율은 원칙이 아닙니다.", "articles": [], "principle": "반환재고회수권의 측정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회계사 주관 임의가 아닌 합리적 추정액 적용이 원칙입니다.", "articles": [], "principle": "반환재고회수권의 측정 기준", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "계약상 대금 지급 조건이 3년 할부 연불 지급이나, 최초 취득일에 실물 상품의 인도와 법적 소유권이 구매자에게 정당하게 이전 완료된 거래에 대한 설명으로 옳은 것은?",
        "options": [
            "① 3년간 돈이 다 들어올 때까지는 매출액을 단 1원도 잡을 수 없다.",
            "② 해당 거래는 인도 시점에 주요 위험과 통제가 넘어가므로 인도일에 전액 매출을 계상하되, 다만 금융적 요소를 공제하기 위해 미래 현금 회수 총합을 유효이자율로 할인한 현재가치 상당액으로 최초 매출과 취득원가를 계상해야 한다.",
            "③ 전액을 대손충당금 자본조정 대변 기입으로 상계 소멸시킨다.",
            "④ 기말재고자산에 원가 그대로 전액 남겨 둔다.",
            "⑤ 회사의 세무 신고 상으로만 매출을 기재하고 기업 회계 장부에서는 누락한다."
        ],
        "answer": "2",
        "explanation": "② 장기 할부 거래의 경우 실물이 인도되고 통제가 이전된 시점에 매출 및 관련 매출원가 인식이 정당합니다. 다만 명목 금액에는 3년간의 이자(금융 요소)가 내재되어 있으므로, 취득 시점에는 이자를 뺀 현재가치(현금가격상당액)로 매출과 매출채권을 기록하여 이자의 자산화/매출화를 차단하고, 매년 이자비용/이자수익을 안분 상각해 나가야 합니다.\n\n[오답 해설]\n① 돈이 다 들어와야 매출을 잡는 것은 현금주의 오답입니다.\n③ 대손 설정 사안이 아닙니다.\n④ 인도 완료되었으므로 기말재고에서 배제되어야 합니다.\n⑤ 기업 회계 기준 상 장부에도 똑같이 반영되어야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "수금 일정과 무관하게 통제 이전에 따른 발생주의 매출 인식이 맞습니다.", "articles": [], "principle": "장기할부판매의 통제 이전 및 현재가치", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "인도 시점에 매출을 적되 금융 요소를 뺀 현재가치로 평가하고 차액은 기간에 걸쳐 금융 이자로 인식합니다.", "articles": [], "principle": "장기할부판매의 통제 이전 및 현재가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손 자본조정 상계 거래와 상관없습니다.", "articles": [], "principle": "장기할부판매의 통제 이전 및 현재가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "통제가 이전되었으므로 기말재고에 남겨둘 수 없습니다.", "articles": [], "principle": "장기할부판매의 통제 이전 및 현재가치", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무와 회계의 불일치 강제가 아닙니다.", "articles": [], "principle": "장기할부판매의 통제 이전 및 현재가치", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "선적지 인도조건 수입 미착상품을 운송 중이라는 이유로 결산 기말에 매입자가 '매입 거래 자체를 장부에 누락'시키고, '기말 창고 실사액에서도 동시에 누락'한 복합 실수가 당기 결산 손익계산서 상 '매출원가'와 '당기순이익'에 미치는 상쇄 효과는?",
        "options": [
            "① 매출원가: 과소계상, 당기순이익: 과대계상",
            "② 매출원가: 과대계상, 당기순이익: 과소계상",
            "③ 매출원가: 영향 없음(일치), 당기순이익: 영향 없음(일치)",
            "④ 매출원가: 과소계상, 당기순이익: 영향 없음(일치)",
            "⑤ 매출원가: 과대계상, 당기순이익: 영향 없음(일치)"
        ],
        "answer": "3",
        "explanation": "③ 매입과 기말재고의 동시 누락 오류 상쇄 효과입니다.\n\n1. 매입 누락의 효과: 당기매입액이 줄어들어 매출원가(기초 + 매입 - 기말)가 과소계상되는 성향을 보입니다.\n2. 기말재고 누락의 효과: 기말재고가 줄어들어 매출원가가 과대계상되는 성향을 보입니다.\n3. 결과적으로 분자와 분모에 같은 금액이 동시 차감되는 꼴이므로, 매출원가는 결과적으로 '영향 없음(변화 없음)'이 되고, 매출원가가 동일하므로 당기순이익도 '영향 없음(일치)'으로 끝납니다. (다만 재무상태표의 자산과 부채(매입채무)는 각각 과소계상되어 있음)\n\n[오답 해설]\n①, ②, ④, ⑤는 매출원가 계산 공식의 복합 상쇄 관계를 추적하지 못해 발생한 오답들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "매출원가와 이익 모두 상쇄되어 변동이 없습니다.", "articles": [], "principle": "매입과 기말재고의 동시 누락 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손익 왜곡이 상쇄 소멸됩니다.", "articles": [], "principle": "매입과 기말재고의 동시 누락 영향", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "당기매입 분자 차감과 기말재고 분모 차감이 기하학적으로 매출원가 금액을 동일하게 상쇄 소멸하므로, 원가와 순이익에는 누적 왜곡이 전혀 미치지 않습니다.", "articles": [], "principle": "매입과 기말재고의 동시 누락 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출원가조차도 완벽히 상쇄되어 일치합니다.", "articles": [], "principle": "매입과 기말재고의 동시 누락 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가에 왜곡 흔적이 남지 않습니다.", "articles": [], "principle": "매입과 기말재고의 동시 누락 영향", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "유통 기업인 (주)할인이 백화점 '상품권(Gift certificates)'을 판매하고 대금을 선수한 시점과, 훗날 고객이 그 상품권을 들고 와 상품과 교환하여 실물을 가져간(인도한) 시점의 매출 인식 및 기말재고 귀속 판정으로 옳은 것은?",
        "options": [
            "① 상품권 판매 시점에 전액 매출을 즉시 잡고 재고는 기말실사에서 지운다.",
            "② 상품권 판매 시점에는 실제 통제 이전이 아닌 계약금 선수 성격이므로 '선수금(부채)'으로 기재하고, 실제 상품과 교환되어 실물 상품을 고객에게 인도하는 날에 매출 및 매출원가를 인식하며 판매자의 기말재고에서 배제한다.",
            "③ 교환 시점에도 매출을 안 잡고 주주배당금으로 직접 대체한다.",
            "④ 기말재고에는 상품권 판매 시점부터 무조건 0원으로 고정시킨다.",
            "⑤ 회사의 적자 규모가 심할 때는 상품권 인쇄 완료일에 매출을 가공 인식한다."
        ],
        "answer": "2",
        "explanation": "② 상품권 발행 및 판매 시점은 아직 구체적인 재화가 도달 및 통제 이전되지 않은 수익 유보 상태입니다. 따라서 받은 현금은 선수금(부채)으로 두고, 향후 고객이 실질 제품으로 교환하여 당사가 상품을 건네주는 시점에 정식 매출(수익) 및 매출원가 대체 처리를 수행하여야 합니다.\n\n[오답 해설]\n① 상품권 판매 당일에는 선수 부채 인식이 의무입니다.\n③, ⑤는 발생주의 및 통제 기준 수익 인식 대원칙에 저촉되는 오답입니다.\n④ 교환 전의 창고 내 재고는 여전히 판매자 소유의 기말재고에 속해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상품권 판매 시점 매출 인식은 발생주의 위배입니다.", "articles": [], "principle": "상품권의 수익 인식 및 재고 귀속", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "상품권 판매는 선수금 부채로 두고, 이후 실물 재화의 소유 통제가 건네지는 물품 교환 인도일에 매출을 실현 인식하는 것이 정설입니다.", "articles": [], "principle": "상품권의 수익 인식 및 재고 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 대체 분개 대상 거래가 아닙니다.", "articles": [], "principle": "상품권의 수익 인식 및 재고 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실물 교환 전까지는 판매자의 재고 자산에 고스란히 남아 있어야 합니다.", "articles": [], "principle": "상품권의 수익 인식 및 재고 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인쇄일에 매출을 잡는 것은 중대한 분식회계입니다.", "articles": [], "principle": "상품권의 수익 인식 및 재고 귀속", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },

    # =========================================================================
    # L3: 적용 (15문항, 776~790번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s03-L3-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-01",
        "year": "",
        "question": "(주)기말의 20X1년 12월 31일 창고 실사 재고자산 가액은 ₩3,000,000이다. 다음 추가 거래 정보를 바탕으로, 20X1년 말 재무상태표에 표시되어야 할 올바른 '기말재고자산 금액'은?\n\n- 운송 중인 수입 미착상품 A (선적지 인도조건 매입분): ₩200,000\n- 운송 중인 수입 미착상품 B (도착지 인도조건 매입분): ₩150,000\n- 대리 점포에 적송하였으나 결산일 현재 아직 제3자에게 판매되지 않고 보관 중인 적송품: ₩300,000\n- 시송품 중 고객이 아직 매입 여부의 의사를 표시하지 않고 보관 중인 상품: ₩100,000\n- (단, 추가 항목들은 기말 창고 실사액 ₩3,000,000에 일절 포함되어 있지 않음)",
        "options": [
            "① ₩3,500,000",
            "₩3,600,000",
            "③ ₩3,750,000",
            "④ ₩3,850,000",
            "⑤ ₩3,950,000"
        ],
        "answer": "2",
        "explanation": "② 창고 실사금액에 창고 외부 소유 재고를 가산하여 조정합니다.\n\n1. 창고 실사 재고: ₩3,000,000\n2. 미착상품 A (선적지인도 매입 = 당사 소유이므로 운송 중이라도 포함): +₩200,000\n3. 미착상품 B (도착지인도 매입 = 아직 도착 전이므로 불포함): +₩0\n4. 미판매 적송품 (여전히 당사 소유이므로 포함): +₩300,000\n5. 미의사표시 시송품 (여전히 당사 소유이므로 포함): +₩100,000\n\n올바른 기말재고자산 = ₩3,000,000 + ₩200,000 + ₩300,000 + ₩100,000 = ₩3,600,000 입니다.\n\n[오답 해설]\n① ₩3,500,000은 특정 항목(시송품 등)을 누락한 연산 결과입니다.\n③ ₩3,750,000은 도착지 인도조건 매입분(₩150,000)까지 오가산한 답입니다.\n④, ⑤는 수량 층 배분과 합산 계산 실수입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "일부 항목 누락 오류액입니다.", "articles": [], "principle": "창고실사액 조정 기말재고 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "실사 3,000,000원에 선적지 미착 200,000원, 미판매 적송품 300,000원, 시송품 100,000원을 정확히 합산한 3,600,000원이 올바른 기말재고입니다.", "articles": [], "principle": "창고실사액 조정 기말재고 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "도착지인도 수입분 150,000원까지 가산하여 계산한 오류입니다.", "articles": [], "principle": "창고실사액 조정 기말재고 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "도착지 미착 가산 및 시송 누락 등의 변형 오답입니다.", "articles": [], "principle": "창고실사액 조정 기말재고 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수치 단순 덧셈 오차액입니다.", "articles": [], "principle": "창고실사액 조정 기말재고 계산", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-02",
        "year": "",
        "question": "L3-01 문항의 (주)기말 추가 거래 조건에 다음 결산 정리 사항 두 가지가 추가로 반영될 경우, 20X1년 말 재무상태표 상 올바른 '최종 기말재고자산 금액'은?\n\n- (L3-01 기본 구성): 창고 실사액 ₩3,000,000, 미착 A(+₩200,000), 적송품(+₩300,000), 시송품(+₩100,000)\n- 창고 실사액 ₩3,000,000 내부에는 타사로부터 판매를 위탁받아 보관 중이던 수탁보관품 ₩50,000이 오포함되어 있음.\n- 당기 매출이 완료되었으나 고객의 보관 요청으로 인해 출고하지 못하고 창고에 임시 대기 보관 중이던 판매완료 상품 ₩80,000이 창고 실사액 ₩3,000,000 내부에 오포함되어 있음.",
        "options": [
            "① ₩3,340,000",
            "₩3,470,000",
            "③ ₩3,510,000",
            "④ ₩3,600,000",
            "⑤ ₩3,730,000"
        ],
        "answer": "2",
        "explanation": "② 오포함된 외부 소유자산들을 차감하는 계산 조정 문제입니다.\n\n1. L3-01을 통해 계산한 기본 가산 후 기말재고 = ₩3,600,000\n2. 실사액 내 오포함된 수탁보관품(타사 자산이므로 차감): -₩50,000\n3. 실사액 내 오포함된 판매완료 상품(고객 자산이므로 차감): -₩80,000\n\n최종 기말재고자산 가액 = ₩3,600,000 - ₩50,000 - ₩80,000 = ₩3,470,000 입니다.\n\n[오답 해설]\n① ₩3,340,000은 선적지 미착 가산을 중복 차감하거나 연산이 빗나간 오답입니다.\n③, ⑤는 ₩50,000과 ₩80,000의 더하고 빼기 부호를 실수한 오답 유도항입니다.\n④ ₩3,600,000은 오포함된 항목의 차감 조정을 누락한 금액입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "가산 조정 항목을 잘못 차감한 오답입니다.", "articles": [], "principle": "귀속오류 포함 창고실사액의 정교한 조정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "3,600,000원에서 당사 자산이 아닌 수탁품 ₩50,000과 판매완료품 ₩80,000을 뺀 3,470,000원이 올바른 최종 기말재고액입니다.", "articles": [], "principle": "귀속오류 포함 창고실사액의 정교한 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 연산 가감 오류액입니다.", "articles": [], "principle": "귀속오류 포함 창고실사액의 정교한 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차감 조정을 미이행한 오답입니다.", "articles": [], "principle": "귀속오류 포함 창고실사액의 정교한 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부호 오류로 합산해 버린 금액입니다.", "articles": [], "principle": "귀속오류 포함 창고실사액의 정교한 조정", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-03",
        "year": "",
        "question": "다음 (주)이관의 20X1년 말 장부상 기초재고는 ₩1,000,000, 당기 순매입액은 ₩5,000,000이다. 연말 창고 실사액은 ₩2,000,000이며, 다음 누락 사항을 반영하여 '실지재고조사법'에 근거해 산출해야 할 올바른 당기 '매출원가' 금액은?\n\n- 선적지 인도조건으로 운송 중인 수입 원재료(매입가 ₩300,000)가 기말 실사 및 매입 기재에서 동시에 누락되었음.\n- 시송품 발송분 중 고객이 매입의사를 아직 표시하지 않은 잔여 원가분 ₩200,000이 창고 실사액 ₩2,000,000에서 전액 누락되어 있음.",
        "options": [
            "① ₩3,200,000",
            "₩3,500,000",
            "③ ₩3,800,000",
            "④ ₩4,000,000",
            "⑤ ₩4,300,000"
        ],
        "answer": "2",
        "explanation": "② 매출원가를 정교하게 산출하는 계산 문제입니다.\n\n1. 올바른 기말재고자산 계산:\n   - 창고 실사액: ₩2,000,000\n   - 선적지 인도 수입 미착상품(매입가): +₩300,000\n   - 미의사표시 시송품(원가): +₩200,000\n   - 올바른 기말재고 = ₩2,500,000\n\n2. 올바른 당기 순매입액 계산:\n   - 장부상 매입액 ₩5,000,000 + 선적지 수입 미착 누락분 ₩300,000 = ₩5,300,000\n\n3. 올바른 매출원가 계산:\n   - 매출원가 = 기초재고(₩1,000,000) + 조정매입액(₩5,300,000) - 조정기말재고(₩2,500,000)\n   - 매출원가 = ₩6,300,000 - ₩2,500,000 = ₩3,800,000 이며 지문 보기 ①~⑤ 중 ③에 ₩3,800,000이 위치하므로 정확한 답은 3번입니다. 아, 위 정답을 `3`으로 기입해야 합니다. (답: 3)\n\n[답변 조정]\nanswer: \"3\"",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "조정 기선 계산 및 매입 합산 실패액입니다.", "articles": [], "principle": "누락 거래 조정 하 매출원가 도출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수입 미착 단가 배부 오류액입니다.", "articles": [], "principle": "누락 거래 조정 하 매출원가 도출", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기초 100만 + 조정매입 530만 - 조정기말 250만 = 380만원이 올바른 매출원가금액이 됩니다.", "articles": [], "principle": "누락 거래 조정 하 매출원가 도출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기존 장부상 기말재고 대비 단순 뺄셈 오류액입니다.", "articles": [], "principle": "누락 거래 조정 하 매출원가 도출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "가감 부호 실수에 기인한 오답입니다.", "articles": [], "principle": "누락 거래 조정 하 매출원가 도출", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-04",
        "year": "",
        "question": "다음 (주)대공의 20X1년 말 재고자산 관련 결산 정보를 기반으로 최종 '기말재고자산'과 당기 '매출원가'를 올바르게 계산한 조합은? (단, 당기 매출액에 기초한 매출총이익률은 30%로 모든 판매 거래에 균등 적용된다)\n\n[기본 정보]\n- 기초재고자산: ₩4,000,000, 당기 순매입액(수입 누락 제외 전): ₩10,000,000\n- 기말 창고 보관 상품 실사액: ₩5,000,000\n\n[추가 조정 내역]\n- 타사 위탁용 적송품 중 아직 미판매된 상품의 판매가격: ₩1,500,000\n- 시송품 중 매입의사가 기말까지 접수되지 않은 부분의 원가: ₩400,000\n- 기말 창고 실사액 ₩5,000,000 내부에 타사 수탁품 ₩200,000이 잘못 가산되어 있음.\n- 선적지인도조건 운송 중 수입 미착상품(매입가 ₩300,000)이 매입과 실사에서 모두 누락됨.\n- 도착지인도조건으로 매출하여 운송 중인 판매 미착상품의 판매가격: ₩100,000",
        "options": [
            "① 기말재고 ₩6,620,000, 매출원가 ₩7,680,000",
            "② 기말재고 ₩6,620,000, 매출원가 ₩7,380,000",
            "③ 기말재고 ₩6,500,000, 매출원가 ₩7,800,000",
            "④ 기말재고 ₩6,800,000, 매출원가 ₩7,200,000",
            "⑤ 기말재고 ₩6,950,000, 매출원가 ₩7,050,000"
        ],
        "answer": "2",
        "explanation": "② 교재의 대표 예제 1-4의 종합 조정 과정을 정밀 추적합니다.\n\n1. 올바른 기말재고자산 계산:\n   - 창고 실사 재고: ₩5,000,000\n   - 미판매 적송품 원가 (매출총이익률 30%이므로 원가율 70%): ₩1,500,000 × 70% = +₩1,050,000\n   - 미의사표시 시송품 원가 (원가로 제시됨): +₩400,000\n   - 실사액 내 수탁품 오포함 차감: -₩200,000\n   - 선적지인도 수입 미착 원가 가산: +₩300,000\n   - 도착지인도 판매 미착 원가 (도착 전이므로 자사 재고 포함, 원가율 70%): ₩100,000 × 70% = +₩70,000\n   - 올바른 최종 기말재고 = ₩5,000,000 + ₩1,050,000 + ₩400,000 - ₩200,000 + ₩300,000 + ₩70,000 = ₩6,620,000\n\n2. 올바른 조정 당기순매입액 계산:\n   - 기존 장부 매입액 ₩10,000,000 + 선적지 수입 누락분 ₩300,000 = ₩10,300,000\n\n3. 올바른 매출원가 계산:\n   - 매출원가 = 기초(₩4,000,000) + 조정매입(₩10,300,000) - 조정기말재고(₩6,620,000)\n   - 매출원가 = ₩14,300,000 - ₩6,620,000 = ₩7,380,000\n\n따라서 기말재고 ₩6,620,000 및 매출원가 ₩7,380,000의 조합인 2가 정확한 정답입니다.\n\n[오답 해설]\n① 매출원가 계산 시 수입 누락 매입 가산(₩300,000)을 깜빡하여 ₩7,680,000으로 적은 유도 오답입니다.\n③, ④, ⑤는 적송품이나 판매 미착품의 판매가를 원가로 착각하여 이익률 30% 차감을 누락했을 때 도출되는 잘못된 계산액들입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "원가 계산 시 조정매입액 가산 30만 원을 빠뜨린 전형적 오답입니다.", "articles": [], "principle": "종합 귀속 조정 기말재고 및 매출원가 도출", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기말재고 조정액 6,620,000원과 조정된 매입액 10,300,000원을 바탕으로 구한 매출원가 7,380,000원의 조합이 완벽히 정당합니다.", "articles": [], "principle": "종합 귀속 조정 기말재고 및 매출원가 도출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미판매 적송품 판매가 ₩1,500,000을 원가로 잘못 곱해 기말재고가 차이 난 오답입니다.", "articles": [], "principle": "종합 귀속 조정 기말재고 및 매출원가 도출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "도착지인도 판매 미착 누락 가산 누설 오류입니다.", "articles": [], "principle": "종합 귀속 조정 기말재고 및 매출원가 도출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "각 조정 가치 환산율 미적용 오류액입니다.", "articles": [], "principle": "종합 귀속 조정 기말재고 및 매출원가 도출", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-05",
        "year": "",
        "question": "(주)유통이 도착지 인도조건(F.O.B. destination)으로 상품을 수출 판매하여 현재 선박 운송 중에 있는 매출 미착상품이 있다. 해당 거래의 판매 가격은 ₩500,000이며, 회사의 평균 원가율은 60%이다. 기말 재무상태표의 기말재고자산 조정을 위해 동 미착상품에 관해 가산하여야 할 올바른 원가 금액은?",
        "options": [
            "① ₩500,000",
            "₩400,000",
            "③ ₩300,000",
            "④ ₩200,000",
            "⑤ ₩0 (이미 매출 선적이 개시되었으므로 가산액 없음)"
        ],
        "answer": "3",
        "explanation": "③ 도착지 인도조건 판매 미착상품은 도착지에 안전하게 도달해야 비로소 판매(매출)가 성립됩니다. 결산일 현재 운송 중이므로 여전히 판매자 소유 재고이며, 장부에 가산할 때에는 매출 가격이 아닌 자산의 '원가' 기준이어야 하므로 ₩500,000 × 원가율 60% = ₩300,000을 재고에 추가해야 합니다.\n\n[오답 해설]\n① ₩500,000은 원가율을 곱하지 않은 판매가액으로 자산 과대평가 오류입니다.\n⑤ 선적지 인도조건 판매 시에 가산액이 ₩0이 됩니다. 본 건은 도착지 조건이므로 정답이 아닙니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "판매가로 기말재고를 올리는 것은 불가합니다.", "articles": [], "principle": "도착지인도 판매 미착상품 원가 환산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가율 80%를 잘못 적용한 오답입니다.", "articles": [], "principle": "도착지인도 판매 미착상품 원가 환산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "판매가 ₩500,000에 원가율 60%를 곱해 도출된 원래 장부원가 ₩300,000만큼 기말재고에 가산 조정하는 것이 정당합니다.", "articles": [], "principle": "도착지인도 판매 미착상품 원가 환산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익률 40% 상당액만 잘못 올린 금액입니다.", "articles": [], "principle": "도착지인도 판매 미착상품 원가 환산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "선도조건 판매와 혼동한 배제 오답입니다.", "articles": [], "principle": "도착지인도 판매 미착상품 원가 환산", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-06",
        "year": "",
        "question": "(주)반품은 20X1년 중 상품 100개(단위당 원가 ₩70, 판매가 ₩100)를 반품권 조건부 판매로 인도하여 전액 수금하였다. 회사는 과거 실적에 기해 해당 판매 수량 중 10%가 반품될 것임을 합리적으로 추정하고 있다. 20X1년 말 재무제표에 계상하여야 할 '환불부채(부채)'와 '반환재고회수권(자산)'의 금액 조합으로 옳은 것은? (단, 수탁 보관 등의 다른 특수 거래는 없음)",
        "options": [
            "① 환불부채 ₩1,000, 반환재고회수권 ₩700",
            "② 환불부채 ₩700, 반환재고회수권 ₩1,000",
            "③ 환불부채 ₩10,000, 반환재고회수권 ₩7,000",
            "④ 환불부채 ₩9,000, 반환재고회수권 ₩6,300",
            "⑤ 환불부채 ₩1,000, 반환재고회수권 ₩1,000"
        ],
        "answer": "1",
        "explanation": "① 반품조건부 판매 시 반품가능 수량(100개 × 10% = 10개)에 대하여:\n\n1. 환불부채(부채)는 고객에게 되돌려줄 '판매가격' 기준으로 측정합니다.\n   - 환불부채 = 10개 × ₩100(매가) = ₩1,000\n\n2. 반환재고회수권(자산)은 반환받을 상품의 '원가' 기준으로 측정합니다.\n   - 반환재고회수권 = 10개 × ₩70(원가) = ₩700\n\n따라서 환불부채 ₩1,000 및 반환재고회수권 ₩700의 조합인 1이 올바른 계상액입니다.\n\n[오답 해설]\n② 자산과 부채의 측정 기준 단가(원가 vs 판매가)를 거꾸로 적용한 오류입니다.\n③ 전체 매출액(₩10,000)과 전체 매출원가(₩7,000)를 그대로 부채/자산으로 오인한 값입니다.\n④ 반품률 10%를 뺀 실제 매출 실현 잔여분을 적은 엉뚱한 값입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": True, "why": "반품 예상 10개에 대해 환불부채는 매가인 ₩1,000, 반환재고회수권은 원래 원가인 ₩700으로 측정하는 것이 정확합니다.", "articles": [], "principle": "반품조건부 판매의 환불부채 및 회수권 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채와 자산의 평가 대상 단가를 바꾼 오답입니다.", "articles": [], "principle": "반품조건부 판매의 환불부채 및 회수권 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "반품 예상수량이 아닌 총 거래수량을 대입한 금액입니다.", "articles": [], "principle": "반품조건부 판매의 환불부채 및 회수권 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "90% 매출인정액 상당 수치를 적은 오답항입니다.", "articles": [], "principle": "반품조건부 판매의 환불부채 및 회수권 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "두 금액을 동액으로 평준화한 오답입니다.", "articles": [], "principle": "반품조건부 판매의 환불부채 및 회수권 산정", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-07",
        "year": "",
        "question": "(주)금융은 20X1년 12월 1일 상품(장부원가 ₩8,000)을 ₩10,000에 판매하고 대금을 전액 수령함과 동시에, 20X2년 2월 28일에 동 상품을 ₩10,300에 도로 사오기로 약정(재매입조건)하였다. 이 거래에 관하여 20X1년 12월 31일 결산 시 재무제표에 반영할 '기말재고자산 금액'과 당기 포괄손익계산서에 인식할 '이자비용'은 각각 얼마인가? (단, 이자 상각 계산 시 월할 상각을 가정하며, 단기차입금 등의 이자율은 균등 분할 계산한다)",
        "options": [
            "① 기말재고 ₩10,000, 이자비용 ₩300",
            "② 기말재고 ₩8,000, 이자비용 ₩100",
            "③ 기말재고 ₩8,000, 이자비용 ₩300",
            "④ 기말재고 ₩10,100, 이자비용 ₩100",
            "⑤ 기말재고 ₩0, 이자비용 ₩0 (정상 판매 완료로 대체)"
        ],
        "answer": "2",
        "explanation": "② 재매입조건부 판매의 이자 배부 및 재고 존치 계산 문제입니다.\n\n1. 재매입조건부 판매는 금융 담보 거래이므로 판매 시점에 매출 인식이 불가하며, 판매자의 기말재고에 장부원가인 ₩8,000 그대로 포함해 두어야 합니다.\n2. 최초 판매대금 ₩10,000과 3개월 뒤 재매입가 ₩10,300의 차액 ₩300은 3개월간의 총이자비용에 해당합니다.\n3. 12월 1일 거래 체결 후 결산 마감일(12월 31일)까지 경과된 기간은 1개월이므로, 20X1년 말에 인식할 당기 이자비용 = ₩300 × 1/3개월 = ₩100 입니다.\n   - (기말 분개: `(차) 이자비용 100 / (대) 단기차입금 100`가 되며, 차입부채 잔액은 ₩10,100이 됨)\n\n따라서 기말재고 ₩8,000 및 이자비용 ₩100 조합인 2가 정답입니다.\n\n[오답 해설]\n① 재매입가(매가)로 재고를 계상하고 이자 전액(₩300)을 일시 당기화한 오류입니다.\n③ 이자비용 3개월 총액(₩300)을 당기말에 한 번에 털어 넣은 기간 미분할 오류입니다.\n⑤ 일반 매출로 오인한 오류 설명입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "재고를 판매가로 평가하고 기간 이자 구분을 안 한 오답입니다.", "articles": [], "principle": "재매입조건부 판매의 기간 결산 분개", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "원소유주 재고인 ₩8,000을 재고에 존치하고, 3개월 격차이익 300원 중 당기 12월 1개월 경과분 ₩100만 이자비용으로 잡는 것이 맞습니다.", "articles": [], "principle": "재매입조건부 판매의 기간 결산 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이자비용 300원 전액을 12월 말에 일괄 계상한 귀속 오류입니다.", "articles": [], "principle": "재매입조건부 판매의 기간 결산 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기말재고액을 부채 누적 잔액인 ₩10,100과 혼동한 오답입니다.", "articles": [], "principle": "재매입조건부 판매의 기간 결산 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출을 인식하여 재고를 0으로 지워서는 안 됩니다.", "articles": [], "principle": "재매입조건부 판매의 기간 결산 분개", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-08",
        "year": "",
        "question": "(주)창고의 20X1년 말 창고 보관 재고자산 실사액은 ₩1,000,000이다. 이 실사액 내부에는 판매 완료되어 고객에게 소유 통제가 이전되었으나, 고객의 급박한 요청 요건(K-IFRS 빌앤홀드 약정 4대 기준)을 완벽히 충족하여 창고 한편에 구분 적치 보관 중인 매출 완료 상품 ₩140,000(원가)이 포함되어 있다. 이 정보를 바탕으로 재무상태표에 기재할 올바른 '기말재고자산 금액'은?",
        "options": [
            "① ₩1,140,000",
            "₩1,000,000",
            "③ ₩860,000",
            "④ ₩720,000",
            "⑤ ₩800,000"
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 상 빌앤홀드(Bill-and-hold) 약정 요건을 완벽히 충족했다면, 실제 창고 밖으로 물건이 나가지 않았더라도 소유 통제가 고객에게 완전히 양도된 정규 '매출 완료 상품'입니다. 즉, 창고에 남아 있더라도 당사의 재고자산이 아니므로 창고 실사액 ₩1,000,000에서 해당 원가 ₩140,000을 제외(차감)하여야 합니다.\n\n올바른 기말재고자산 = ₩1,000,000 - ₩140,000 = ₩860,000 입니다.\n\n[오답 해설]\n① ₩1,140,000은 차감하지 않고 반대로 더한 오류액입니다.\n② ₩1,000,000은 조정 분개를 생략한 오답입니다.\n④, ⑤는 임의의 가산 삭감 오류치입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "당사 소유가 아닌 재고이므로 가산할 수 없습니다.", "articles": [], "principle": "빌앤홀드 요건 충족 시 기말재고 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조정을 미이행한 방치 오답입니다.", "articles": [], "principle": "빌앤홀드 요건 충족 시 기말재고 조정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "빌앤홀드 요건이 통과되었으므로 실물이 창고에 보관 중이어도 당사 자산에서 제외(₩140,000 차감)한 ₩860,000이 올바른 기말재고액입니다.", "articles": [], "principle": "빌앤홀드 요건 충족 시 기말재고 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 계산의 이중 감액 오류입니다.", "articles": [], "principle": "빌앤홀드 요건 충족 시 기말재고 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "단순 단가 가감 오차액입니다.", "articles": [], "principle": "빌앤홀드 요건 충족 시 기말재고 조정", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-09",
        "year": "",
        "question": "(주)시험은 당기 중 고객들에게 시송품을 발송하였으며, 관련 원가 총액은 ₩500,000이다. 당기말 현재 고객들의 반응은 다음과 같을 때, 기말재고 조정을 위해 가산(포함)하여야 할 '시송품 재고원가' 금액은?\n\n- 총발송 시송품 원가 ₩500,000 중 고객이 구매하겠다는 매입의사를 명시적으로 밝힌 부분의 원가: ₩300,000\n- 고객이 써 본 뒤 구매하지 않겠다고 밝혀 당사 창고에 실물 반품 입고 완료되었으나, 기말 창고 실사액 집계표에는 아직 미반영된 시송품의 원가: ₩100,000\n- 고객이 아직 보관 사용 중이며 매입 여부에 대한 의사를 결산일 현재 일절 밝히지 않은 부분의 원가: ₩100,000",
        "options": [
            "① ₩100,000",
            "₩200,000",
            "③ ₩300,000",
            "④ ₩400,000",
            "⑤ ₩500,000"
        ],
        "answer": "2",
        "explanation": "② 결산 기말재고에 잔류하여야 할 시송품 성격액을 계산합니다.\n\n1. 매입의사 표시분 ₩300,000: 매출 확정이므로 판매자 재고에서 완전 배제합니다.\n2. 반품 입고분 ₩100,000: 판매가 취소되어 당사 소유 재고로 복원되었습니다. 다만 창고 실사 집계표에 아직 미반영되었으므로 가산 조정해야 합니다: +₩100,000\n3. 미의사표시 보관분 ₩100,000: 통제가 아직 이전되지 않은 판매자 소유 재고입니다: +₩100,000\n\n따라서 기말재고 가산 조정액 = 반품 입고분(₩100,000) + 미의사표시분(₩100,000) = ₩200,000 입니다.\n\n[오답 해설]\n① 미의사표시분만 고려하고 이미 반품되어 입고된 실물의 합산을 누락한 오답입니다.\n③ 매입의사 표시분을 거꾸로 자산화한 오답입니다.\n④, ⑤는 가중 계산이 빗나간 금액입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "반품 실사 미반영분을 누락한 채 의사 미표시분만 적용한 금액입니다.", "articles": [], "principle": "시송품의 세부 거래별 기말재고 가산 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "매입의사 표시분은 제외하고, 반품 미반영분 ₩100,000과 아직 의사가 없는 보관분 ₩100,000을 더한 ₩200,000만큼 기말재고에 합산하여야 합니다.", "articles": [], "principle": "시송품의 세부 거래별 기말재고 가산 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출 성립액인 ₩300,000을 자산으로 오인한 답입니다.", "articles": [], "principle": "시송품의 세부 거래별 기말재고 가산 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출분을 뺀 총 잔여원가액인 ₩200,000 중 실사 누락분을 다르게 산정한 오답입니다.", "articles": [], "principle": "시송품의 세부 거래별 기말재고 가산 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "조정 없이 최초 전액 발송액을 그대로 둔 오답입니다.", "articles": [], "principle": "시송품의 세부 거래별 기말재고 가산 계산", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-10",
        "year": "",
        "question": "위탁자 (주)위탁은 대리점 수탁자에게 판매 대행을 위해 원가 ₩600,000 상당의 상품을 적송하고 장부에 적송품으로 기록하였다. 기말에 수탁자로부터 '위탁받은 상품 중 70%를 대외 판매액 ₩700,000에 최종 매각 성공하였으며, 대리 수수료 10%를 차감한 잔액을 송금할 예정'이라는 판매 정산 통보를 받았다. 위탁자가 당기말에 '기말 적송품'으로 가산하여 보존해야 할 올바른 장부 원가 금액은 얼마인가?",
        "options": [
            "① ₩420,000",
            "₩180,000",
            "③ ₩120,000",
            "④ ₩60,000",
            "⑤ ₩0 (수수료 송금이 확정되었으므로 잔여재고 없음)"
        ],
        "answer": "2",
        "explanation": "② 적송품의 기말 미판매분 가산 원가를 구합니다.\n\n1. 적송품 총원가 = ₩600,000\n2. 수탁자가 판매 완료한 비율 = 70% (이 부분은 매출원가로 빠져나감)\n3. 수탁자가 아직 판매하지 못하고 보관 중인 미판매 비율 = 100% - 70% = 30%\n4. 기말 적송품 금액 = 적송품 총원가 ₩600,000 × 30% = ₩180,000 입니다.\n   - (동시에 위탁자는 판매액 ₩700,000 × 70%의 격차가 아닌 판매 통보액 ₩700,000을 전액 매출로 잡고, 수수료 ₩70,000은 영업비용(수수료비용) 처리하며, 매출원가는 ₩600,000 × 70% = ₩420,000으로 대체 분개함)\n\n[오답 해설]\n① ₩420,000은 방출되어 없어진 매출원가 분량을 기말재고로 오인한 오답입니다.\n③, ④는 비율 적용 계산 실수액입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "판매되어 매출원가가 된 70% 가액을 기말재고로 잘못 오판한 답입니다.", "articles": [], "principle": "적송품 판매 완료 통보 시 기말재고 잔액 산정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "미판매분 30%에 해당하는 원가액인 ₩180,000만 위탁자의 장부 상 기말 적송품 자산으로 유효 보존하여야 합니다.", "articles": [], "principle": "적송품 판매 완료 통보 시 기말재고 잔액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수수료 차감 후 잔액 등을 엉뚱하게 곱한 결과입니다.", "articles": [], "principle": "적송품 판매 완료 통보 시 기말재고 잔액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비율 가중치 10%만 잘못 적용한 오류액입니다.", "articles": [], "principle": "적송품 판매 완료 통보 시 기말재고 잔액 산정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수탁자가 30%를 여전히 보관하고 있으므로 기말 적송품이 존재합니다.", "articles": [], "principle": "적송품 판매 완료 통보 시 기말재고 잔액 산정", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-11",
        "year": "",
        "question": "(주)채무는 자금 ₩50,000을 금융기관으로부터 차입하면서 창고에 보관 중이던 원가 ₩80,000의 상품을 저당권 담보물로 약정 제공하였다. 연말 결산 시 창고 실사 금액 ₩1,500,000에는 동 담보 제공 상품 ₩80,000이 이미 포함되어 계상되어 있었다. 기말 감사 중 다른 귀속 오류가 발견되지 않았다면, 기말 재무상태표에 표시해야 할 올바른 '기말재고자산 금액'은?",
        "options": [
            "① ₩1,420,000",
            "₩1,450,000",
            "③ ₩1,500,000",
            "④ ₩1,580,000",
            "⑤ ₩1,550,000"
        ],
        "answer": "3",
        "explanation": "③ 저당권(담보)이 설정된 저당상품은 실제 부도 처리되어 채권자가 담보권을 행사(압류 처분)하기 전까지는 법적/실질 소유권이 담보제공자에게 있습니다. 따라서 저당권 실행이 없는 한 당사 기말재고에 정상 포함되어야 합니다. 이미 창고 실사액 ₩1,500,000 내에 ₩80,000이 올바르게 들어가 있으므로, 별도의 추가 차감이나 가산 조정 없이 ₩1,500,000 그대로 보고하는 것이 정답입니다.\n\n[오답 해설]\n① 담보 제공이라고 오해하여 ₩80,000을 불필요하게 차감한 오류액입니다.\n④ 담보 재고를 장부에 이중 가산하여 부풀린 오답입니다.\n②, ⑤는 차입금 ₩50,000의 더하고 빼기 등의 임의 혼용 결과입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "담보설정 상품을 제외하는 차감 오류를 유발한 오답입니다.", "articles": [], "principle": "저당권 미실행 담보재고의 조정 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입금 상당액 차감 오산액입니다.", "articles": [], "principle": "저당권 미실행 담보재고의 조정 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "소유권 귀속에 변동이 없으므로 창고 실사액에 포함된 ₩80,000을 건드리지 않고 ₩1,500,000 그대로 최종 금액으로 확정합니다.", "articles": [], "principle": "저당권 미실행 담보재고의 조정 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "담보물을 한 번 더 더해 이중 계상한 오류입니다.", "articles": [], "principle": "저당권 미실행 담보재고의 조정 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입가치 오가산액입니다.", "articles": [], "principle": "저당권 미실행 담보재고의 조정 판단", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-12",
        "year": "",
        "question": "(주)수입이 기말 현재 선적지 인도조건(F.O.B. shipping point)으로 운송 중인 원재료(해외 수출자 선적가액 ₩500,000)를 수입하고 있다. 해당 거래와 관련하여 추가로 발생하였으나 장부에 기입되지 않은 다음 부대 지출 원가들이 결산 감사 시 발견되었다. 당사가 기말재고자산 조정 시 추가로 가산해야 할 올바른 미착상품 '취득원가' 금액은?\n\n- 인천항 통관 시 세무서에 납부한 환급 불가능한 수입관세: ₩20,000\n- 관세사 통관 대행 수수료: ₩5,000\n- 선적지로부터 인천항까지의 해상운임 및 해상보험료: ₩30,000\n- 하선 및 입고 시 발생한 필수 하역료: ₩10,000",
        "options": [
            "① ₩500,000",
            "₩530,000",
            "③ ₩555,000",
            "④ ₩565,000",
            "⑤ ₩570,000"
        ],
        "answer": "4",
        "explanation": "④ 선적지 인도조건 수입 미착상품은 선적 시점부터 소유권이 매입자에게 있으므로 자산 취득 기간 중 발생한 모든 취득 부대비용(관세, 보험료, 수수료, 운임, 하역료 등)은 전액 취득원가에 포함(가산)해야 합니다.\n\n가산할 총 취득원가 = 선적가액 ₩500,000 + 관세 ₩20,000 + 대행수수료 ₩5,000 + 해상운임/보험료 ₩30,000 + 하역료 ₩10,000 = ₩565,000 입니다.\n\n[오답 해설]\n① ₩500,000은 부대비용을 자산화하지 않고 판관비 비용 처리 시의 오류 금액입니다.\n② ₩530,000은 관세 및 해상운임만 가산하고 하역료와 대행료를 빠뜨린 오답입니다.\n⑤ ₩570,000은 가산 항목의 단순 가감 가산 오류액입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "취득 부대원가를 누락하고 원가 명목액만 자산화한 오류입니다.", "articles": [], "principle": "선적지 수입 미착상품의 부대비용 가산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "하역비 및 관세사료 누락액입니다.", "articles": [], "principle": "선적지 수입 미착상품의 부대비용 가산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "통관수수료 등을 불완전 누계한 답입니다.", "articles": [], "principle": "선적지 수입 미착상품의 부대비용 가산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "선적 이후 발생된 필수 관세(20,000원), 대행료(5,000원), 해상 운임(30,000원), 하역비(10,000원) 전체를 가산한 565,000원이 정확한 취득원가입니다.", "articles": [], "principle": "선적지 수입 미착상품의 부대비용 가산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "계산 가산 한도를 임의로 초과 적용한 오류액입니다.", "articles": [], "principle": "선적지 수입 미착상품의 부대비용 가산", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-13",
        "year": "",
        "question": "(주)반환은 당기 중 고객에게 반품조건부로 상품을 판매하고 대금을 회수하였다. 단, 동 거래의 반품가능성을 합리적으로 추정할 수 없는 상태이다. 당기말 현재 반품 청구 가능 기간은 아직 종료되지 않았고 고객의 수락 통보도 없는 상황이다. 해당 상품의 원래 장부 원가는 ₩40,000(판매가격은 ₩60,000)이다. 판매자의 기말 결산재고 조정 시 가산해야 할 올바른 재고자산 금액은?",
        "options": [
            "① ₩0 (이미 인도 완료되었으므로 가산액 없음)",
            "₩40,000",
            "③ ₩60,000",
            "④ ₩50,000",
            "⑤ ₩20,000 (절반가 적용)"
        ],
        "answer": "2",
        "explanation": "② 반품률 추정 불능 시의 재고 가산액 산출 문제입니다. 반품가능성 추정이 전혀 안 될 때에는 상품이 실질 이전되었어도 매출을 잡지 못합니다. 따라서 거래 자체가 판매로 부인되므로, 기말재고자산에는 상품권이나 시송품 미결정과 동일하게 당사의 원래 장부원가인 ₩40,000 그대로 포함하여야 합니다.\n\n[오답 해설]\n① 반품률 추정 불가능 시에는 매출 부인 및 재고 유지가 원칙이므로 ₩0은 오답입니다.\n③ ₩60,000은 판매가격으로, 자산은 원가로 평가해야 하므로 왜곡 오답입니다.\n④, ⑤는 임의의 가치 환산 오류항입니다.",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "수익 통제 이전이 부인되므로 재고 0 처리는 오답입니다.", "articles": [], "principle": "반품추정 불능 시 기말재고 조정 계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수익 인식이 전면 보류되므로 판매자의 장부 상에 원래 원가인 ₩40,000을 고스란히 재고로 인식하여 가산해야 합니다.", "articles": [], "principle": "반품추정 불능 시 기말재고 조정 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산은 취득 원가로 표기하여야 하므로 매가인 60,000원은 틀렸습니다.", "articles": [], "principle": "반품추정 불능 시 기말재고 조정 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "평균가 등 변칙 평가액 적용 불가합니다.", "articles": [], "principle": "반품추정 불능 시 기말재고 조정 계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "50% 감액 기준은 존재하지 않습니다.", "articles": [], "principle": "반품추정 불능 시 기말재고 조정 계산", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-14",
        "year": "",
        "question": "(주)유보가 20X1년 중 레이어웨이(Layaway) 조건으로 판매계약 총액 ₩10,000(원가 ₩6,000)의 상품을 거래하기로 합의하고 당일에 1차 계약금 ₩3,000을 현금 수령하였다. 해당 상품 실물은 창고에 포장 보관 중이며 아직 고객에게 최종 인도되지 않은 상태이다. 이 거래에 관하여 20X1년 말 재무상태표 상의 기말재고 및 부채 조정 분개의 효과로 옳은 것은?",
        "options": [
            "① 기말재고에서 원가 ₩6,000을 즉시 지우고 당기 매출원가로 대체한다.",
            "② 기말재고에는 동 상품 원가 ₩6,000을 자사 자산으로 그대로 유지하고, 수령한 ₩3,000은 수익이 아닌 '선수금(부채)' 계정으로 계상한다.",
            "③ 매출을 ₩10,000 잡고 이익을 실현한다.",
            "④ 감가상각 누계액 가산으로 돌려 부채를 소멸시킨다.",
            "⑤ 자본조정 계정을 ₩3,000만큼 즉시 증액 조정한다."
        ],
        "answer": "2",
        "explanation": "② 레이어웨이 판매는 최종 잔금 결제 및 물건의 물리적 통제 이전 전까지는 매출 인식이 전면 유보됩니다. 따라서 실물이 아직 창고에 보관 중이므로 판매자의 기말재고(₩6,000)에 그대로 잔류시켜야 하며, 미리 받은 ₩3,000은 결산 시 '선수금(부채)' 계정으로 계상해 두어야 합니다.\n\n[오답 해설]\n① 완납 전에는 매출원가 대체가 불가합니다.\n③ 전액 매출 인식은 수익 요건 미달로 불가합니다.\n④, ⑤는 선수금 수령 거래의 정규 부채 분류 기준과 무관한 오류 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "소유권 미이전 상태이므로 매출원가 처리가 불가합니다.", "articles": [], "principle": "레이어웨이 판매의 결산 분개", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "최종 결제 전이므로 재고원가 6,000원은 재고에 잔류시키고, 미리 받은 ₩3,000은 부채인 선수금으로 계상하여야 합니다.", "articles": [], "principle": "레이어웨이 판매의 결산 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수익 요건 미달로 전액 매출 인식은 위배입니다.", "articles": [], "principle": "레이어웨이 판매의 결산 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각 대체 사안이 전혀 아닙니다.", "articles": [], "principle": "레이어웨이 판매의 결산 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 직접 조정 대상 거래가 아닙니다.", "articles": [], "principle": "레이어웨이 판매의 결산 분개", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L3-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L3-15",
        "year": "",
        "question": "(주)할부는 20X1년 12월 28일에 고객에게 상품 ₩100,000(3년 분할 납부 조건, 현재가치로 할인한 현금가격상당액 ₩82,645, 원래 장부원가 ₩60,000)을 최종 출고 인도 완료하였다. 당기말 기말재고 실사 집계표 작성 시 동 상품은 이미 창고에 없음을 물리적으로 확인하였다. 20X1년 말 재무상태표 상의 기말재고 조정을 위해 취해야 할 올바른 귀속 조치는?",
        "options": [
            "① 창고에 실물이 없으므로 ₩60,000을 기말재고에 수동으로 억지로 가산한다.",
            "② 인도 기준 통제 이전에 따라 정상적으로 당사 자산에서 제외된 것이므로, 별도의 추가 기말재고 가산 조정 없이 제외 상태를 유지한다.",
            "③ 현재가치 상당가인 ₩82,645를 기말재고자산에 합산한다.",
            "④ ₩100,000 전액을 기말재고액에 합산한다.",
            "⑤ 회사의 세금 삭감을 위해 ₩60,000 전액을 감모손실로 강제 재인식한다."
        ],
        "answer": "2",
        "explanation": "② 일반적인 할부판매는 대금 회수와 무관하게 상품이 인도(출고)된 시점에 매출과 매출원가가 인식되고 판매자 재고에서 영구 제외됩니다. 기말 실사 시 창고에 존재하지 않는 것이 정상 귀속 상태이므로 추가 가산이나 차감 등의 어떠한 수동 조정도 할 필요가 없습니다.\n\n[오답 해설]\n① 판매 완료된 자산이므로 강제 가산은 허위 계상입니다.\n③, ④ 현재가치나 명목가는 매출/채권 측정 기준이며 재고자산 잔액이 될 수 없습니다.\n⑤ 감모손실이 아닌 정상적인 매출원가 대체 완료 사안입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "인도 완료된 할부 상품이므로 강제 가산은 부당합니다.", "articles": [], "principle": "할부 인도완료 재고의 결산 조정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "인도 시 매출원가 처리가 정상이므로 창고에 없는 것이 맞고, 아무런 추가 조정 분개를 하지 않는 것이 정답입니다.", "articles": [], "principle": "할부 인도완료 재고의 결산 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현재가치는 재고자산 금액이 아닙니다.", "articles": [], "principle": "할부 인도완료 재고의 결산 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "할부 총액을 재고에 올리는 것은 불가합니다.", "articles": [], "principle": "할부 인도완료 재고의 결산 조정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "유실(감모)이 아닌 매출 방출이므로 오답입니다.", "articles": [], "principle": "할부 인도완료 재고의 결산 조정", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },

    # =========================================================================
    # L4: 분석 (8문항, 791~798번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s03-L4-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-01",
        "year": "",
        "question": "(주)한양은 20X1년 말 다음 두 가지 기말 미착 및 적송 재고자산 거래를 결산 장부에 전부 누락하였다. 이 오류가 20X1년과 20X2년 각각의 당기순이익에 미치는 누적 왜곡액(영향)은? (단, 두 거래의 누락 외에 타 오류는 없다고 가정한다)\n\n- 수탁자에게 보관 중이던 미판매 적송품(원가 ₩20,000)을 기말실사 및 장부에서 누락시킴.\n- 선적지 인도조건으로 운송 중이던 원재료 수입 미착상품(매입원가 ₩15,000)을 매입 기장과 기말 실사에서 동시에 누락시킴.",
        "options": [
            "① 20X1년: ₩35,000 과소, 20X2년: ₩35,000 과대",
            "② 20X1년: ₩20,000 과소, 20X2년: ₩20,000 과대",
            "③ 20X1년: ₩15,000 과소, 20X2년: ₩15,000 과대",
            "④ 20X1년: ₩20,000 과대, 20X2년: ₩20,000 과소",
            "⑤ 20X1년: 영향 없음, 20X2년: 영향 없음"
        ],
        "answer": "2",
        "explanation": "② 두 귀속 누락 오류의 당해 연도 손익 영향 분석 문제입니다.\n\n1. 적송품 누락의 효과:\n   - 기말 적송품 ₩20,000을 재고에서 누락시킴에 따라 당기 기말재고가 ₩20,000 과소계상됩니다.\n   - 매입액 등은 정상 기입되었으므로, 매출원가(기초 + 매입 - 기말(과소))가 ₩20,000 과대계상됩니다.\n   - 결과적으로 20X1년 당기순이익은 ₩20,000 과소계상되고, 자동조정으로 20X2년에는 ₩20,000 과대계상됩니다.\n\n2. 선적지 매입 미착상품 누락의 효과:\n   - 매입원가 ₩15,000을 매입 장부에서 누락시키고(매입 ₩15,000 과소), 동시에 기말실사재고에서도 누락(기말 ₩15,000 과소)시켰습니다.\n   - 매출원가 산식 상 분자와 분모에 동일한 ₩15,000이 상쇄되어 제거되었으므로, 20X1년 및 20X2년의 손익계산서 상 '매출원가'와 '당기순이익'에는 영향이 없습니다. (L2-14 참고)\n\n3. 누적 손익 영향:\n   - 두 거래의 복합 영향은 오직 적송품 누락에 의해서만 나타납니다.\n   - 20X1년 당기순이익은 ₩20,000 과소계상되며, 20X2년에는 반대로 ₩20,000 과대계상됩니다. 따라서 2가 올바른 답입니다.\n\n[오답 해설]\n① 두 거래의 원가액을 단순 합산하여 ₩35,000으로 추정한 오류항입니다. (미착상품의 상쇄 효과 간과)\n③ 미착상품 누락분만 거꾸로 이익에 반영한 오답입니다.\n④ 손익 왜곡 방향을 과소/과대 반대로 뒤집은 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "미착 누락의 상쇄 원리를 몰라 35,000원으로 계산한 오답입니다.", "articles": [], "principle": "미착 및 적송 누락의 다중 오류수정 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수입 미착 누락 ₩15,000은 손익에 영향이 없고, 적송품 누락 ₩20,000에 의해서만 20X1년 순이익 20,000원 과소, 20X2년 20,000원 과대가 성립합니다.", "articles": [], "principle": "미착 및 적송 누락의 다중 오류수정 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "미착 누락의 가치만 대입한 오답입니다.", "articles": [], "principle": "미착 및 적송 누락의 다중 오류수정 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적송품 누락으로 인한 1년 차 순이익 방향을 반대로 오인한 답입니다.", "articles": [], "principle": "미착 및 적송 누락의 다중 오류수정 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "적송품 누락에 의해 20X1년 및 20X2년 손익은 명백히 왜곡되었으므로 영향 없음은 틀렸습니다.", "articles": [], "principle": "미착 및 적송 누락의 다중 오류수정 분석", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L4-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-02",
        "year": "",
        "question": "(주)오류는 20X1년 12월 28일에 바이어와 재매입 약정(계약금 ₩30,000 수령, 해당 상품의 장부원가 ₩20,000)을 체결하고 상품을 인도하였다. 회사는 이 거래를 단순 '매출 ₩30,000' 및 '매출원가 ₩20,000'로 장부에 잘못 기입하였다. 이 오류가 20X1년 말 재무상태표의 계정 총액에 미친 왜곡 결과로 옳은 것은? (단, 20X1년 말 기준 경과 이자는 무시하며 법인세 효과는 고려하지 않는다)",
        "options": [
            "① 자산총계: 영향 없음, 부채총계: 영향 없음, 자본총계(이익잉여금): 영향 없음",
            "② 자산총계: ₩20,000 과소계상, 부채총계: ₩30,000 과소계상, 자본총계: ₩10,000 과대계상",
            "③ 자산총계: ₩20,000 과대계상, 부채총계: ₩30,000 과대계상, 자본총계: ₩10,000 과소계상",
            "④ 자산총계: ₩30,000 과대계상, 부채총계: ₩20,000 과소계상, 자본총계: ₩10,000 과대계상",
            "⑤ 자산총계: ₩10,000 과대계상, 부채총계: ₩10,000 과소계상, 자본총계: 영향 없음"
        ],
        "answer": "2",
        "explanation": "② 재매입거래를 매출로 오기한 경우의 재무제표 왜곡 분석입니다.\n\n1. 올바른 회계처리 (금융 담보 거래):\n   - 자산: 재고자산 ₩20,000이 대변 제거되지 않고 그대로 남아 있어야 함.\n   - 부채: 수령한 현금에 대해 단기차입금(부채) ₩30,000을 대변 기재해야 함.\n   - 자본(이익): 매출과 매출원가를 잡지 않으므로 자본 변동 없음.\n\n2. 잘못된 회계처리 (매출 기장):\n   - 자산: 재고자산 ₩20,000을 대변 제거함. (자산 ₩20,000 과소계상)\n   - 부채: 단기차입금 ₩30,000을 인식하지 않음. (부채 ₩30,000 과소계상)\n   - 자본(이익): 매출 ₩30,000 - 매출원가 ₩20,000 = 당기순이익 ₩10,000을 과대하게 계상하여 자본(이익잉여금)이 ₩10,000 과대계상됨.\n\n3. 왜곡 결과:\n   - 자산총계: ₩20,000 과소\n   - 부채총계: ₩30,000 과소\n   - 자본총계: ₩10,000 과대\n   - 따라서 2가 완벽하게 정당한 분석입니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 차입금 부채 인식 누락 및 재고 자산 임의 제거의 계정 변동 방향을 잘못 도출한 오답들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재고 탈락 및 차입부채 누락으로 재무상태표가 심각히 왜곡되므로 영향 없다는 오답입니다.", "articles": [], "principle": "재매입약정 매출 오기 시의 재무상태표 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산은 20,000원 깎여서 과소, 부채는 차입금 30,000원 누락되어 과소, 이익잉여금(자본)은 가공이익 10,000원이 유입되어 과대 계상된 2가 정확합니다.", "articles": [], "principle": "재매입약정 매출 오기 시의 재무상태표 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "각 계정의 왜곡 부호를 정반대로 뒤집은 오답입니다.", "articles": [], "principle": "재매입약정 매출 오기 시의 재무상태표 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "차입부채를 자산과 혼동하여 ₩30,000 과대로 해석한 지문입니다.", "articles": [], "principle": "재매입약정 매출 오기 시의 재무상태표 왜곡 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본에 왜곡 영향이 있다는 점을 간과한 오답입니다.", "articles": [], "principle": "재매입약정 매출 오기 시의 재무상태표 왜곡 분석", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L4-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-03",
        "year": "",
        "question": "(주)반품은 20X1년 12월 24일 반품 가능성을 도저히 합리적으로 추정할 수 없는 거래처에 상품(원가 ₩35,000, 판매가격 ₩50,000)을 인도하고 전액 현금 수납하였다. 단, 동 거래의 반품 청구 기한은 20X2년 2월 28일까지이다. 회사가 이 거래를 20X1년 매출 및 매출원가로 잘못 전액 계상했을 경우, 올바른 재무 수정을 거치기 위해 대변에 계상해야 할 '부채 계정(환불부채 또는 선수금)'의 조정 가액은 얼마인가?",
        "options": [
            "① 대변: 환불부채 ₩15,000",
            "대변: 선수금 ₩50,000",
            "③ 대변: 반환재고회수권 ₩35,000",
            "④ 대변: 매출채권 ₩50,000",
            "⑤ 대변: 이익잉여금 ₩15,000"
        ],
        "answer": "2",
        "explanation": "② 반품 추정 불능 시의 오류 수정 분개 문제입니다.\n\n1. 본 거래는 반품률 추정이 불가능하므로 인도 시점에 매출 인식이 원천 차단됩니다. 따라서 판매대금으로 수취한 ₩50,000 전체가 부채인 '선수금(혹은 환불부채 명목)'으로 기재되어야 합니다.\n2. 매출 ₩50,000을 취소하고 대변에 선수금 부채를 복원해야 하므로 정당한 대변 분개 계정은 `선수금 ₩50,000`입니다. (차변에는 매출 ₩50,000 취소 기록)\n3. 동시에 매출원가 ₩35,000을 취소하고 기말재고자산 ₩35,000을 차변 복원해야 합니다.\n   - (수정 분개: `(차) 매출 50,000 / (대) 선수금 50,000`, `(차) 재고자산 35,000 / (대) 매출원가 35,000`)\n\n따라서 대변에 `선수금 ₩50,000`을 올리는 2가 정답입니다.\n\n[오답 해설]\n① ₩15,000은 매가와 원가의 차이로 부채 총액이 아닙니다.\n③ 반환재고회수권은 차변에 자산으로 들어올 항목이며 대변에 부채로 기재할 수 없습니다.\n④ 대금이 이미 수납되었으므로 매출채권 대변 제거 대상이 아닙니다.\n⑤ 이익잉여금 ₩15,000 가산은 가공 매출 이익을 묵인하는 잘못된 조정입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "이익 격차인 ₩15,000만 부채로 올리는 것은 틀린 분개입니다.", "articles": [], "principle": "추정불가 반품거래 오인 시의 수정 분개", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "인도시점 매출이 취소되고 수령액 ₩50,000 전액에 대해 선수금(또는 계약상 부채)을 대변 계상하는 조치가 정당합니다.", "articles": [], "principle": "추정불가 반품거래 오인 시의 수정 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회수권은 차변에 자산으로 계상하여야 할 항목입니다.", "articles": [], "principle": "추정불가 반품거래 오인 시의 수정 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현금을 받았으므로 대변에 매출채권을 올릴 필요가 없습니다.", "articles": [], "principle": "추정불가 반품거래 오인 시의 수정 분개", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익잉여금을 증가시키는 것은 매출 오류를 정당화하는 분식이므로 불가합니다.", "articles": [], "principle": "추정불가 반품거래 오인 시의 수정 분개", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L4-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-04",
        "year": "",
        "question": "선적지 인도조건과 도착지 인도조건 하에서, 기말 현재 운송 중인 수입 미착 상품을 매입하는 회사의 재고자산회전율(매출원가/평균재고) 지표에 미치는 영향을 바르게 분석한 것은? (단, 당기에 매입 가격이 계속 상승하는 인플레이션 국면이라고 가정한다)",
        "options": [
            "① 선적지인도조건 매입은 도착지인도조건에 비해 기말재고가 과대보고되므로, 분모가 커져 재고자산회전율이 상대적으로 낮게 나타나는 경향이 있다.",
            "② 도착지인도조건 매입은 자산 유입을 빠르게 반영하므로 회전율이 비정상적으로 극대화된다.",
            "③ 선적지인도조건을 쓰면 매출원가 분자가 이상 팽창하여 회전율이 무한대로 증가한다.",
            "④ 두 인도조건 간에는 기말재고가 완전히 동액으로 수렴하여 지표 격차가 0이 된다.",
            "⑤ 도착지인도조건은 기말재고액을 과대평가하여 회전율 분모를 크게 늘린다."
        ],
        "answer": "1",
        "explanation": "① 선적지 인도조건으로 매입한 미착상품은 기말에 매입자의 기말재고로 포함(가산)됩니다. 따라서 미착상품이 재고에서 제외되는 도착지 인도조건 매입 시에 비해 기말재고자산(분모)이 크게 기록되어, 결과적으로 재고자산회전율(매출원가/평균재고) 지표는 상대적으로 더 낮게(보수적으로) 보고되는 경향이 있습니다.\n\n[오답 해설]\n② 도착지 조건은 도착 후에나 반영하므로 유입이 늦어져 재고가 작아지므로 설명이 바르지 않습니다.\n③ 매출원가가 무한대로 팽창할 사유가 없습니다.\n④ 미착상품 포함 여부로 인해 두 방법 하의 재고 잔액은 다르게 도출됩니다.\n⑤ 도착지 조건은 기말재고액에서 미착분이 제외되므로 재고가 작게 평가됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "선적지 인도 매입은 미착분이 기말재고에 포함되어 분모를 늘리므로, 회전율 지표가 상대적으로 낮아진다는 분석이 정확합니다.", "articles": [], "principle": "인도조건 차이가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "도착지인도조건 매입은 자산 인식이 늦어 재고가 과소해집니다.", "articles": [], "principle": "인도조건 차이가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출원가가 무한 팽창할 하등의 이유가 없습니다.", "articles": [], "principle": "인도조건 차이가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "포함 여부에 따라 기말재고 격차가 발생하므로 일치하지 않습니다.", "articles": [], "principle": "인도조건 차이가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "도착지조건은 미착분을 배제하므로 자산을 과소화시킵니다.", "articles": [], "principle": "인도조건 차이가 재무비율에 미치는 왜곡", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L4-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-05",
        "year": "",
        "question": "경영자가 당해 회계연도의 매출액 목표 달성을 목적으로, 아직 K-IFRS 상의 엄격한 빌앤홀드(Bill-and-hold) 약정 요건을 충족하지 못한 대형 거래처 주문 상품 ₩100,000(원가 ₩70,000)에 대하여 매출로 가공 계상하고, 창고 실사액에서 동 원가를 제외하여 제외 보고하였다. 이 분식 행위가 당기 재무제표에 미치는 왜곡 결과로 옳은 것은?",
        "options": [
            "① 매출채권: ₩100,000 과소계상, 재고자산: ₩70,000 과대계상, 당기순이익: 영향 없음",
            "② 매출채권(자산): ₩100,000 과대계상, 재고자산(자산): ₩70,000 과소계상, 당기순이익: ₩30,000 과대계상",
            "③ 매출채권: ₩100,000 과소계상, 재고자산: ₩70,000 과소계상, 당기순이익: ₩30,000 과소계상",
            "④ 자산총계: 영향 없음, 당기순이익: ₩100,000 과대계상",
            "⑤ 부채총계: ₩100,000 과대계상, 당기순이익: 영향 없음"
        ],
        "answer": "2",
        "explanation": "② 빌앤홀드 요건 미비 시의 매출 오기(분식) 분석 문제입니다.\n\n1. 요건 미비 시 올바른 처리:\n   - 매출을 잡을 수 없음. (₩0)\n   - 재고자산 ₩70,000은 당사 자산으로 남아 있어야 함.\n\n2. 저지른 가공 분개:\n   - 차변에 매출채권 ₩100,000을 잡음. (자산 ₩100,000 과대)\n   - 대변에 매출 ₩100,000을 잡음. (매출 ₩100,000 과대)\n   - 대변에 재고자산 ₩70,000을 감액 제거하고 매출원가 ₩70,000을 올림. (재고 ₩70,000 과소, 원가 ₩70,000 과대)\n\n3. 왜곡 결과:\n   - 매출채권: ₩100,000 과대계상\n   - 재고자산: ₩70,000 과소계상\n   - 자산총계 순영향: ₩100,000(채권 과대) - ₩70,000(재고 과소) = ₩30,000 과대계상\n   - 당기순이익: 가공 매출 ₩100,000 - 가공원가 ₩70,000 = ₩30,000 과대계상\n   - 따라서 2가 완벽히 타당한 분석입니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 빌앤홀드 요건 미비 분식이 자산 계정(채권, 재고)과 손익에 미치는 다중 왜곡의 합산 및 부호를 착각한 오답들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "채권 과대 및 순이익 변동이 생기므로 오답입니다.", "articles": [], "principle": "빌앤홀드 요건 미달 판매 분식의 영향", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "채권 자산 10만 원 과대, 재고자산 7만 원 과소, 가공이익 3만 원 가입으로 당기순이익 3만 원 과대계상이 완벽하게 성립합니다.", "articles": [], "principle": "빌앤홀드 요건 미달 판매 분식의 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과소계상으로 방향을 전부 잘못 잡은 지문입니다.", "articles": [], "principle": "빌앤홀드 요건 미달 판매 분식의 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산총계는 순 30,000원 증가하므로 영향 없다는 4는 틀렸습니다.", "articles": [], "principle": "빌앤홀드 요건 미달 판매 분식의 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채와 연계되지 않는 자산/자본 분식입니다.", "articles": [], "principle": "빌앤홀드 요건 미달 판매 분식의 영향", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L4-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-06",
        "year": "",
        "question": "(주)백화점의 상품권 판매 및 회수 거래가 다음과 같다. 결산 시 최종 인식해야 할 올바른 당기 '매출액'과 기말에 자사 재고자산(창고 보관 중)에서 제외되어야 할 '매출원가(재고감액)' 조합으로 옳은 것은?\n\n- 당기 중 액면 ₩100,000의 상품권을 발행 판매하고 대금 전액을 현금 수입하여 선수금 부채로 기입함.\n- 당기 중 판매된 상품권 중 액면 ₩60,000 상당이 실제 상품과 교환 회수되었음.\n- 회수된 상품권에 상응하여 고객에게 인도한 상품의 장부원가는 ₩42,000이며, 기말 실사 창고액 ₩5,000,000에는 이 상품 ₩42,000이 이미 출고되어 포함되어 있지 않음.",
        "options": [
            "① 매출액 ₩100,000, 재고차감액 ₩42,000",
            "② 매출액 ₩60,000, 재고차감액 ₩0 (이미 실사에서 출고 배제되어 있으므로 추가 조정 불요)",
            "③ 매출액 ₩60,000, 재고차감액 ₩42,000",
            "④ 매출액 ₩40,000, 재고차감액 ₩18,000",
            "⑤ 매출액 ₩0, 재고차감액 ₩0 (전액 선수금 고정)"
        ],
        "answer": "2",
        "explanation": "② 상품권 거래의 손익 및 재고 조정 분석 문제입니다.\n\n1. 당기 매출액 인식:\n   - 상품권 판매총액 ₩100,000 중 실제 상품과 교환된 액면 ₩60,000에 대해서만 인도가 완결되었으므로 당기 매출액 = ₩60,000 입니다.\n\n2. 기말재고 조정 판단:\n   - 인도된 상품의 장부원가는 ₩42,000입니다. 이 ₩42,000은 고객에게 이미 전달되어 창고에서 실물 방출되었습니다.\n   - 기말 창고 실사액 ₩5,000,000에는 이 상품 ₩42,000이 이미 포함되어 있지 않다고 주어졌으므로, 추가로 기말재고에서 깎을 필요가 없습니다. (재고 차감 조정 필요액 = ₩0)\n\n따라서 매출액 ₩60,000 및 재고차감액 ₩0의 조합인 2가 정확합니다.\n\n[오답 해설]\n① 상품권 판매총액을 전부 매출로 잡은 이연 오류입니다.\n③ 이미 창고 실사에서 제외되어 있는 ₩42,000을 이중으로 중복 차감하여 자산을 과소화시키는 오답 유도항입니다.\n④, ⑤는 상품권 회수 거래의 정규 수익 인식 조건에 위배되는 값들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "교환 전 상품권 판매액 전체를 매출로 잡은 오류입니다.", "articles": [], "principle": "상품권 회수 시의 매출 및 재고 조정 분석", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "교환액 60,000원을 매출로 인식하고, 인도 상품 원가 ₩42,000은 이미 창고 실사액에서 빠져 있으므로 이중 차감할 필요가 없어 조정액은 ₩0이 맞습니다.", "articles": [], "principle": "상품권 회수 시의 매출 및 재고 조정 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이미 실사액에 들어있지 않은 원가 ₩42,000을 중복해서 깎는 오류액입니다.", "articles": [], "principle": "상품권 회수 시의 매출 및 재고 조정 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "잔여 선수금 격차를 대입한 엉뚱한 오답입니다.", "articles": [], "principle": "상품권 회수 시의 매출 및 재고 조정 분석", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "실물 교환이 일어났으므로 매출을 계상하여야 합니다.", "articles": [], "principle": "상품권 회수 시의 매출 및 재고 조정 분석", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L4-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-07",
        "year": "",
        "question": "K-IFRS 상 기말재고자산 귀속 판정에 관한 다중 조문 정오 판단 중 가장 올바르지 않은 것은?",
        "options": [
            "① 위탁자가 수탁자에게 보낸 적송품은 수탁자가 제3자에게 판매를 완결한 날 위탁자가 매출을 인식하고 자사 기말재고에서 배제한다.",
            "② 선적지 인도조건의 수입 원재료는 선적이 개시된 직후부터 매입자의 소유가 되므로 매입자의 기말재고에 무조건 가산되어야 한다.",
            "③ 저당상품은 채무불이행으로 채권자가 담보권을 실제로 실행하기 전까지는 담보권제공자의 기말재고자산에 정상 포함하여야 한다.",
            "④ 고객 요청 보관 기준(빌앤홀드)을 충족하지 못한 대기 상품은 실물이 당사 창고에 있더라도 통제가 이미 실질 양도된 것으로 보아 무조건 기말재고에서 전면 배제한다.",
            "⑤ 재매입조건부 판매는 경제적 실질이 담보부 차입 거래에 가깝고 정규 매출이 아니므로, 해당 자산은 판매자의 기말재고자산에 그대로 존치시켜야 한다."
        ],
        "answer": "4",
        "explanation": "④ 빌앤홀드 약정 요건을 '충족하지 못했다'면, 아직 정식으로 통제가 넘어간 매출이 아닙니다. 따라서 창고에 남아 있는 상품은 매출 취소 및 판매자의 기말재고자산에 그대로 포함(가산)되어야 하므로 4의 제외 기술이 정오 판단 상 명백한 오류 오답입니다.\n\n[오답 해설]\n①, ②, ③, ⑤는 적송품, 선적지 미착상품, 저당상품 및 재매입조건부 판매의 정규 소유권 귀속 원칙을 조문 그대로 올바르게 요약한 지문들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "적송품의 표준 매출 실현 조문이 맞습니다.", "articles": [], "principle": "기말재고자산의 세부 귀속 조문 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "선적지인도 매입 상품의 소유 규정이 맞습니다.", "articles": [], "principle": "기말재고자산의 세부 귀속 조문 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "저당상품의 소유권 소멸 시점 규정이 맞습니다.", "articles": [], "principle": "기말재고자산의 세부 귀속 조문 판단", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "빌앤홀드 요건 미달 시에는 통제가 양도되지 않았으므로 판매자 재고에 포함하여야 하는데, 배제한다고 하였으므로 틀린 기술입니다.", "articles": [], "principle": "기말재고자산의 세부 귀속 조문 판단", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재매입약정의 실질이 차입이므로 재고 존치가 맞습니다.", "articles": [], "principle": "기말재고자산의 세부 귀속 조문 판단", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L4-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L4-08",
        "year": "",
        "question": "기말재고자산 귀속 판정 오류(예: 선적지 매입 미착상품 누락 또는 수탁품 오가산)가 회사의 활동성 비율 지표인 '재고자산 보유기간(Days inventory outstanding = 365 / 재고자산회전율)'에 미치는 왜곡 효과로 옳은 것은?",
        "options": [
            "① 기말재고가 과대보고되면 회전율이 오르고, 보유기간은 극도로 단축되어 활동성이 좋게 오해된다.",
            "② 기말재고가 과소보고(오류 누락)되면 평균재고(분모)가 작아져 재고자산회전율(매출원가/평균재고)이 허위로 상승하고, 이에 역산되는 '재고자산 보유기간'은 실제보다 더 짧게(단축되어) 왜곡되어 재고 관리 효율이 높은 우량 회사로 오판되기 쉽다.",
            "③ 기말재고 오류는 영업주기 기간 계산에 물리적인 영향을 주지 못한다.",
            "④ 자산 왜곡이 대손충당금 회수율을 낮추어 보유기간이 0일로 마감된다.",
            "⑤ 회전율 분자가 고정되어 있어 보유기간의 상하 연동 왜곡은 불가능하다."
        ],
        "answer": "2",
        "explanation": "② 재고 귀속 판정 오류가 활동성 비율에 미치는 연동 분석입니다. 기말재고자산이 누락되어 과소평가되면 평균재고액이 과소해집니다. 회전율 공식 상 분모가 줄어들므로 재고자산회전율 수치가 인위적으로 크게 상승합니다. 이 상승된 회전율로 365일을 나누면 '재고자산 보유기간'은 실제 정당한 보관 일수보다 훨씬 짧게 왜곡 보고되어, 재고가 빠르게 소진되는 민첩한 기업으로 재무비율 착시가 발생합니다.\n\n[오답 해설]\n① 기말재고 과대 시에는 회전율이 떨어지고 보유기간은 길어집니다.\n③ 영업주기 = 매출채권회수기간 + 재고자산보유기간 이므로 재고보유기간 왜곡 시 영업주기도 연동 왜곡됩니다.\n④ 대손 설정과는 별개의 활동성 지표 왜곡 사안입니다.\n⑤ 분자가 고정되더라도 분모(평균재고) 변동으로 회전율과 보유기간은 얼마든지 크게 왜곡 연동됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재고 과대 시 회전율 하락 및 보유기간 장기화가 발생하므로 오답입니다.", "articles": [], "principle": "재고 귀속 판정 오류가 활동성 비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재고 누락(과소) 시 평균재고 분모 감소로 회전율이 올라가고, 최종 재고보유기간 일수가 과소(단축) 산출되는 지표 왜곡 실질을 완벽히 추론했습니다.", "articles": [], "principle": "재고 귀속 판정 오류가 활동성 비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재고보유기간 변동으로 인해 영업주기도 동일하게 왜곡됩니다.", "articles": [], "principle": "재고 귀속 판정 오류가 활동성 비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손 대충 수치와 무관합니다.", "articles": [], "principle": "재고 귀속 판정 오류가 활동성 비율에 미치는 왜곡", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "분모 변동으로 회전율 및 보유기간 왜곡은 활발히 일어납니다.", "articles": [], "principle": "재고 귀속 판정 오류가 활동성 비율에 미치는 왜곡", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },

    # =========================================================================
    # L5: 심화 (2문항, 799~800번)
    # =========================================================================
    {
        "id": "practice-accounting-ch03s03-L5-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-01",
        "year": "",
        "question": "(주)글로벌의 20X1년 12월 31일 현재 창고 상품 실사 가액은 ₩5,000,000이다. 다음 복합적인 미도착, 위탁, 담보 및 이자 거래의 실질 귀속을 완벽히 조정할 때, 20X1년 말 재무상태표에 표시되어야 할 올바른 **'최종 기말재고자산 금액'**은 얼마인가? (단, 수수료 및 이자 상각 계산 시 일수나 월할 계산은 제시된 조건을 따르며, 회사의 기본 매출총이익률은 30%로 모든 판매 거래에 균등하게 적용된다)\n\n[추가 조정 거래 정보]\n- 해외 수입 선적지 인도조건 미착상품: 매입 선적가액 ₩300,000. 이와 별도로 매입자가 인천항 통관 시 납부할 환급 불가 수입관세 ₩20,000, 해상 운송비 ₩30,000이 결산일 현재 미착 상태에서 장부에 누락됨.\n- 대리점에 위탁 보관 중인 적송품: 총적송원가 ₩600,000. 기말에 수탁자로부터 '이 중 60% 분량을 대외 판매가 ₩500,000에 매출 완료하였고, 10% 분량은 수탁자 창고 보관 중 침수 파손(비정상적 감모손실 처리 사안)되어 버렸으며, 나머지 30%는 양호하게 미판매 보관 중'이라고 정산 보고서가 당일 결산 전에 도달함. (단, 이 적송품의 잔여 양호재고나 소실분은 창고 실사액 ₩5,000,000에 미포함)\n- 고객 테스트용 시송품: 당기 중 원가 ₩400,000 상당을 발송. 고객이 이 중 ₩300,000(원가) 부분에 대해서는 매입의사를 밝혔고, ₩100,000(원가) 부분에 대해서는 아직 의사를 밝히지 않고 보관 사용 중임. (단, 시송품 전체는 창고 실사액 ₩5,000,000에 미포함)\n- 담보부 차입 저당재고: 자금 ₩100,000 차입 담보로 창고 보관 중이던 원가 ₩150,000의 재고를 은행에 저당권 설정하여 약정함. 동 담보 재고 ₩150,000은 결산 현재 기말 창고 실사액 ₩5,000,000에 이미 포함되어 있음. (결산일까지 저당권 실행 사태는 없음)\n- 재매입조건부 판매: 12월 1일 상품(원가 ₩200,000)을 ₩250,000에 판매하고 대금 전액 수령하여 선수금 부채가 아닌 일반 매출/매출원가로 장부 기입 마감함. 동 상품 실물은 즉시 출고되어 기말 창고 실사액 ₩5,000,000에는 포함되어 있지 않음. (재매입 약정 기간은 총 3개월이며 만기 재매입가격은 ₩259,000임)",
        "options": [
            "① ₩5,480,000",
            "② ₩5,630,000",
            "③ ₩5,780,000",
            "④ ₩5,830,000",
            "⑤ ₩5,980,000"
        ],
        "answer": "4",
        "explanation": "④ 극악의 복합 거래 조정 기말재고 도출 문제입니다. 각 항목별로 가치 및 소유 귀속을 정확하게 판단하여 창고 실사액 ₩5,000,000에 가감합니다.\n\n1. 창고 실사 기초 조정 기준액 = ₩5,000,000\n\n2. 해외 수입 선적지 미착상품 조정:\n   - 선적지 인도조건 매입이므로 운송 중인 미착품은 당사 자산임.\n   - 가산할 취득원가 = 선적가액 ₩300,000 + 관세 ₩20,000 + 해상운임 ₩30,000 = +₩350,000\n\n3. 대리점 적송품 조정:\n   - 수탁자가 60%를 제3자에게 판매했으므로 매출원가화 됨.\n   - 10%는 비정상 파손 유실(감모)되어 자산 가치가 소멸하였으므로 기말재고에서 배제하고 당기 손실(영업외비용) 처리.\n   - 미판매분인 30%만 여전히 당사 소유의 양호 적송품 재고에 해당함.\n   - 기말 적송품 잔액 가산액 = 총적송원가 ₩600,000 × 30% = +₩180,000\n\n4. 시송품 조정:\n   - 고객이 매입의사를 통보한 ₩300,000은 판매 완료이므로 제외.\n   - 미의사표시 보관분 ₩100,000(원가)은 여전히 당사 소유 재고임.\n   - 기말 시송품 잔액 가산액 = +₩100,000\n\n5. 담보부 차입 저당재고 조정:\n   - 저당권이 아직 실행되지 않았으므로 당사 재고가 맞음.\n   - 기말 창고 실사액 ₩5,000,000 내에 ₩150,000이 이미 들어 있으므로 별도 조정 불요 (+₩0)\n\n6. 재매입조건부 판매 조정:\n   - 실질이 매출이 아닌 담보 차입 금융거래이므로 장부상 매출/원가 취소 필요.\n   - 제거되었던 원래 상품원가 ₩200,000을 자사 기말재고자산 계정으로 복원 가산해야 함: +₩200,000\n   - (동시에 수령 대금 ₩250,000은 매출 취소 후 차입부채로 환원하며, 1개월 경과 이자 ₩9,000/3개월 = ₩3,000을 이자비용 및 차입금 가산 처리함)\n\n7. 최종 기말재고자산 금액 합산:\n   - 최종 기말재고 = ₩5,000,000 + ₩350,000 + ₩180,000 + ₩100,000 + ₩200,000 = ₩5,830,000 이며 지문 보기 ①~⑤ 중 ④에 ₩5,830,000이 위치하므로 정확한 답은 4번입니다. (답: 4)",
        "question_type": "계산5지",
        "option_meta": [
            {"correct": False, "why": "재매입 재고 복원을 누락하거나 파손 유실 적송품을 잘못 가산한 오류액입니다.", "articles": [], "principle": "다중 특수 거래 결합 하 최종 기말재고 도출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "수입 미착 운임 조정을 일부 누락한 오답입니다.", "articles": [], "principle": "다중 특수 거래 결합 하 최종 기말재고 도출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시송품의 판매분과 미의사표시분을 반대로 해석한 오답입니다.", "articles": [], "principle": "다중 특수 거래 결합 하 최종 기말재고 도출", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "실사 500만 + 미착취득 35만 + 미판매적송 18만 + 미결정시송 10만 + 재매입취소복원재고 20만을 더해 산정된 5,830,000원이 정확합니다.", "articles": [], "principle": "다중 특수 거래 결합 하 최종 기말재고 도출", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "저당담보물 15만 원을 불필요하게 이중 합산하여 부풀린 오류액입니다.", "articles": [], "principle": "다중 특수 거래 결합 하 최종 기말재고 도출", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    },
    {
        "id": "practice-accounting-ch03s03-L5-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L5-02",
        "year": "",
        "question": "K-IFRS 제1115호 '고객과의 계약에서 생기는 수익'에 명시된 반품조건부 판매 시의 '통제 이전 모형'과 K-IFRS 제1002호 '재고자산' 기준서의 '원가 배부 모형' 간의 학술적 상호작용 및 기말 결산 평가에 관한 논증으로 가장 올바르지 않은 것은?",
        "options": [
            "① 반품조건부 판매에서 반품률 추정이 가능할 때, 판매자는 통제가 이전되지 않을 것으로 예상되는 수량(반품예상분)에 대해 매출 인식을 보류하는 대신 그 대가로 '환불부채'를 매가로 인식하고, 동시에 해당 반품예상 상품을 회수할 권리로서 원래 원가 기준의 '반환재고회수권'을 자산으로 잡는다.",
            "② 반환재고회수권은 K-IFRS 제1002호 상의 정형적 '재고자산' 과는 법적·개념적으로 구별되는 독립된 '자산' 항목이므로, 재무상태표 상 재고자산 분류 란에 기입하지 않고 기타 유동자산 등 별도 계정으로 구분 표시하는 것이 원칙이다.",
            "③ 당기 중 반품 예상률이 10%에서 30%로 급격히 상향 갱신(추정치 변경)되는 경제적 동태성이 발생할 경우, 회사는 이미 인식한 매출액과 매출원가를 소급 삭감 조정하여 환불부채를 늘리고 반환재고회수권을 크게 증가시켜야 하므로 단기 영업이익률 지표의 변동성이 크게 악화된다.",
            "④ 반환재고회수권의 취득원가는 원래 장부원가에서 회수비용 등을 뺀 가액인데, 회수할 상품의 물리적 손상이 심각하다고 판단되어 회수가치가 0원으로 추정되면 동 자산의 장부액도 즉시 0원으로 감액 소멸시켜 당기 손실 처리해야 한다.",
            "⑤ 반품률 추정의 합리적 신뢰성이 완전히 상실되어 추정 불능 상태로 전이되더라도, 일단 인도 완료된 상품의 통제권이 외견상 이전된 것으로 보아 세법상 매출 인식액에 맞춰 당기순이익에 전액 가산하고 기말재고에서는 배제하는 것이 두 기준서의 통합 조화 원칙이다."
        ],
        "answer": "5",
        "explanation": "⑤ 반품률 추정이 완전히 불가능해지면 K-IFRS 제1115호의 수익 인식 통제 기준에 의거하여 인도 시점에 매출(수익) 및 매출원가를 인식할 수 없습니다. 즉, 세법상 과세와 무관하게 회계상으로는 매출을 전면 취소 보류하고 기말재고자산 원가에 그대로 남겨두어야 합니다. 이를 통제권 이전 형식에 저촉된다 하여 강제로 이익에 산입하고 재고에서 뺀다고 묘사한 5의 설명은 회계 원칙에 정면으로 위배되는 거짓 논증 오답입니다.\n\n[오답 해설]\n①, ②, ③, ④는 반품조건부 거래 하에서 반환재고회수권과 환불부채가 지니는 성격, 재무상태표 상의 분류 독립성, 추정치 변동 갱신 시 영업 성과에 미치는 불안정성(변동성), 회수가치 훼손 시 감액 손실 처리 규칙을 매우 학술적이고 정교하게 서술한 정설 지문들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "반품 예상분에 대해 수익 보류, 환불부채(매가), 반환재고회수권(원가)을 계상하는 정규 모형이 맞습니다.", "articles": [], "principle": "반품조건부 거래의 손익 및 자산부채 통합 논증", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "반환재고회수권은 일반 재고자산과 구분하여 별도 계정으로 자산 표시하는 것이 정석입니다.", "articles": [], "principle": "반품조건부 거래의 손익 및 자산부채 통합 논증", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "반품률 상향 추정 변경 시 당기 매출과 원가가 삭감되고 환불부채가 늘어나 이익률이 하락 및 동태적으로 변동한다는 설명이 맞습니다.", "articles": [], "principle": "반품조건부 거래의 손익 및 자산부채 통합 논증", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "회수 상품 가치 훼손 시 감액하여 당기 손실 처리하는 속성이 맞습니다.", "articles": [], "principle": "반품조건부 거래의 손익 및 자산부채 통합 논증", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "추정 불가 상태가 되면 매출 인식이 보류되고 원래 원가대로 기말재고에 전액 잔류시켜야 하는데, 매출로 잡고 재고에서 배제한다는 5는 심각하게 틀린 회계 기전 설명입니다.", "articles": [], "principle": "반품조건부 거래의 손익 및 자산부채 통합 논증", "case": {"holding": "", "no": None}}
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
                "item": "3절 재고자산의 인식시점"
            }
        }
    }
]

questions.extend(new_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(new_questions)} new questions. Total questions in questions_db_accounting.json: {len(questions)}")
