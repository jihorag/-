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
    "chapter": "제3장 부채",
    "section": "Chapter 09 충당부채, 우발부채",
    "item": "5절 우발부채와 우발자산"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q2401 ~ Q2410) ---
    {
        "id": "practice-accounting-ch09s02-L1-21",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-21",
        "year": "",
        "question": "K-IFRS 제1037호에 따른 '우발부채(Contingent Liability)'의 정의로 가장 올바르지 않은 것은?",
        "options": [
            "① 과거사건에 의하여 발생하였으나, 기업이 전적으로 통제할 수 없는 불확실한 미래사건의 발생 여부에 의해서만 존재가 확인되는 잠재적 의무",
            "② 과거사건에 의하여 발생하였으나, 자원의 유출 가능성이 높지(probable) 않아서 충당부채로 인식하지 않는 현재의무",
            "③ 과거사건에 의하여 발생하였으나, 지출 금액을 신뢰성 있게 측정할 수 없어서 충당부채로 인식하지 않는 현재의무",
            "④ 재무상태표 본문에 부채로 계상하여야 하나 상환 시기가 확정되지 않은 확정채무",
            "⑤ 유출 가능성이 아주 희박하지(remote) 않는 한 재무제표 주석으로 공시하여야 하는 의무"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 우발부채는 충당부채의 인식 요건(의무의 유효성, 유출 가능성, 신뢰성 측정) 중 일부를 결여하여 재무상태표 본문에 부채로 인식할 수 없습니다. 상환 시기가 미정이더라도 요건 충족 시 인식하는 충당부채 및 확정채무와는 구분됩니다.\n\n[오답 해설]\n①, ②, ③ K-IFRS 제1037호 문단 10에 정의된 우발부채의 3가지 핵심 정의 및 분류 경로입니다.\n⑤ 우발부채는 유출 가능성이 극히 희박(Remote)하지 않는 한 주석 공시 대상입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-22",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-22",
        "year": "",
        "question": "K-IFRS 제1037호에 따른 '우발자산(Contingent Asset)'의 핵심 정의와 특징으로 옳은 것은?",
        "options": [
            "① 경제적 효익의 유입 가능성이 높지 않더라도 무조건 재무상태표 차변에 임의 자산으로 계상하여야 한다.",
            "② 과거사건에 의하여 발생하였으나, 기업이 전적으로 통제할 수 없는 하나 이상의 불확실한 미래사건의 발생 여부에 의해서만 그 존재가 확인되는 잠재적 자산",
            "③ 미래에 발생할 것이 예상되므로 최초 시점에 감가상각을 시작하여 영업비용을 배분해야 한다.",
            "④ 주주총회 승인을 거치면 유입 가능성에 상관없이 항상 이익잉여금 자본으로 직접 대체 기장할 수 있다.",
            "⑤ 자원의 유입 가능성이 희박(remote)한 경우에도 주석에 반드시 기재하여야 한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우발자산이란 과거사건의 결과로 발생하였으나, 기업이 전적으로 통제할 수 없는 불확실한 미래사건의 발생 여부에 의해서만 존재가 확인되는 잠재적 성격의 자산입니다.\n\n[오답 해설]\n① 경제적 효익 유입 가능성이 높음(Probable) 수준인 우발자산은 주석 공시만 가능하며 본문 차변 자산 계상은 금지됩니다.\n③ 미실현 자산이므로 감가상각 대상이 아닙니다.\n④ 주주총회 결의만으로 미인식 자산을 자본화하는 분개는 허용되지 않습니다.\n⑤ 우발자산은 유입 가능성이 높은(Probable) 경우에만 공시하며, 그 미만(Possible, Remote)은 공시하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-23",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-23",
        "year": "",
        "question": "K-IFRS 제1037호 기준 상 '우발부채'의 공시 원칙에 관한 설명 중 가장 올바르지 않은 것은?",
        "options": [
            "① 우발부채는 재무상태표 본문에 부채로 인식하지 않는다.",
            "② 자원의 유출 가능성이 아주 희박한(Remote) 경우가 아니라면 재무제표 주석에 우발부채를 반드시 공시하여야 한다.",
            "③ 공동으로 의무를 지는 연대채무의 경우, 제3자가 이행할 것으로 기대되는 의무의 부분은 우발부채로 처리하여 주석에 공시한다.",
            "④ 유출 가능성이 높음(Probable) 수준에 도달하고 신뢰성 있게 금액을 측정할 수 있게 변동되었다면 더 이상 우발부채가 아니므로 충당부채로 계상하여야 한다.",
            "⑤ 우발부채의 주석 공시는 항상 기업의 영업이익에 직접 차감하는 감액 분개를 동반한다."
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ 주석 공시(Disclosure)는 재무제표 본문(재무상태표, 포괄손익계산서)에 기장(분개)을 반영하지 않고 주석 란에 정보만을 기술하므로, 당기순손익이나 영업이익 등에 미치는 직접적인 차감 분개 조치는 동반되지 않습니다.\n\n[오답 해설]\n①, ②, ③, ④ K-IFRS 상 우발부채의 본문 배제 원칙, 희박(Remote) 시 공시 제외, 연대보증 분할 처리, 충당부채로의 전환 요건에 관한 정합한 조문 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-24",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-24",
        "year": "",
        "question": "K-IFRS 제1037호에 의거하여, 손해배상 제소 소송 등 기업에 발생한 '우발자산'을 재무제표 주석으로 의무 공시하기 위해 요구되는 경제적 효익의 유입 가능성 수준은?",
        "options": [
            "① 가능성이 희박(Remote, <5%)한 경우",
            "② 어느 정도 가능성이 있음(Possible, 5~50%) 수준에 그치는 경우",
            "③ 경제적 효익의 유입 가능성이 높음(Probable, >50%) 수준인 경우",
            "④ 유입 가능성이 거의 확실(Virtually Certain)하여 자산으로 인식한 경우",
            "⑤ 자산의 가액이 ₩0인 가상의 기대 상태인 경우"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1037호 문단 30 및 89에 따라, 우발자산은 경제적 효익의 유입 가능성이 높은(Probable, 보통 50% 초과) 경우에만 주석으로 공시합니다. 유입 가능성이 높지 않은 경우에는 주석 공시를 할 수 없습니다.\n\n[오답 해설]\n①, ② 유입 가능성이 희박하거나 단순 가능성이 있는 수준은 우발자산 공시 대상에서 제외됩니다.\n④ 유입이 거의 확실(Virtually Certain)해지면 본문에 정식 자산으로 기입해야 하므로, 더 이상 우발자산 주석 공시 대상이 아닌 본문 자산 인식 건입니다.\n⑤ 가상 가치는 회계적 공시 요건이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-25",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-25",
        "year": "",
        "question": "K-IFRS 제1037호 하에서 경제적 효익이 유출될 가능성이 '아주 희박(Remote)'하여 재무제표 본문 기재는 물론 주석 공시까지도 면제(생략)되는 부채 항목은?",
        "options": [
            "① 충당부채",
            "② 확정채무",
            "③ 미지급비용",
            "④ 유출 가능성이 아주 희박한 우발부채",
            "⑤ 연대채무 중 당사가 전액 부담하기로 서약한 현재의무"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 우발부채는 기본적으로 주석 공시 의무가 있으나, 경제적 유출 가능성이 '아주 희박한(Remote)' 경우에 한해서는 정보 제공의 유용성이 없으므로 주석 공시 생략을 전면 허용합니다.\n\n[오답 해설]\n① 충당부채는 가능성 높음 요건이므로 공시 생략이 불가능합니다.\n②, ③ 확정채무와 미지급비용은 확정부채로서 재무상태표 본문에 반드시 계상되어야 합니다.\n⑤ 당사 책임 지분 현재의무는 충당부채 또는 확정부채 대상이므로 공시 생략이 불가합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-26",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-26",
        "year": "",
        "question": "우발자산의 가능성을 기말에 매기 재평가하던 중, 경제적 효익의 유입 가능성이 드디어 '거의 확실(Virtually Certain)'한 상태에 도달하였음을 확인하였다. 이 경우 K-IFRS 기준 상 올바른 후속 회계처리는?",
        "options": [
            "① 자산 유입이 실현되었으므로 주석 공시를 누락하고 전액 기타포괄손익 자본으로만 관리한다.",
            "② 유입이 거의 확실하므로 관련 자산과 그에 상응하는 당기 이익(수익 등)을 당기 재무제표 본문에 공식 인식(기장)한다.",
            "③ 여전히 현금이 들어오지 않았으므로 계속 우발자산 주석 공시 상태를 유지하며 본문 기재를 금지한다.",
            "④ 자산 금액의 50%만을 영업비용 차감 계정으로 부가 등재한다.",
            "⑤ 즉시 해당 자산을 부채 계정의 대손충당금 자본조정으로 전액 상쇄하여 삭제한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1037호 문단 33에 따라, 자원의 유입이 거의 확실(Virtually Certain)해지면 관련 자산은 더 이상 우발자산이 아니므로 재무상태표 본문에 정식 자산으로 기장하고, 그에 따른 수익이나 원가 차감 등을 당기 손익에 적격하게 반영합니다.\n\n[오답 해설]\n① OCI 자본으로만 이월하여 숨기는 처리는 부적절합니다.\n③ 거의 확실한 시점에는 주석 공시 유지가 아니라 본문 계상으로 전이되어야 하므로 오답입니다.\n④ 50% 간편 평가 조항이나 ⑤ 대손충당금 상쇄 조항 등은 회계 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-27",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-27",
        "year": "",
        "question": "K-IFRS 하에서 '충당부채'와 '우발부채'의 회계처리 상의 본질적인 차이점에 대한 설명 중 옳은 것은?",
        "options": [
            "① 충당부채는 재무상태표 본문에 부채로 계상하여 공시하지만, 우발부채는 본문에 기재하지 않고 주석으로만 공시한다.",
            "② 우발부채는 당기순손실을 발생시키지만 충당부채는 당기순이익에 영향을 준다.",
            "③ 두 부채 항목 모두 재무상태표 본문에 동일한 부채 금액으로 계상되므로 차이가 없다.",
            "④ 충당부채는 주석 공시를 전혀 하지 않으며 본문에만 일괄 기록한다.",
            "⑤ 우발부채는 자본조정금의 차감 항목으로 본문에 적는다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 충당부채와 우발부채의 대차대조표 상 본질적 차이입니다. 충당부채는 인식요건을 충족하여 재무상태표 본체 부채란에 기재되지만, 우발부채는 요건 미달로 인해 본문에 기재되지 못하고 주석 보고 정보로 공시 처리됩니다.\n\n[오답 해설]\n② 우발부채는 분개되지 않으므로 당기순손실을 유발하지 않고, 충당부채는 비용 설정을 통해 당기순손실(비용 증가)을 유발합니다.\n③ 본문 계상 여부에서 극명하게 갈리므로 차이가 없다는 것은 오답입니다.\n④ 충당부채도 본문 기장과 동시에 중요 지출 내역을 주석 공시하여야 합니다.\n⑤ 우발부채는 자본조정 차감 항목이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-28",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-28",
        "year": "",
        "question": "회계에서 우발부채는 경제적 자원의 유출 가능성이 '높음(Probable)' 미만이거나 금액 추정이 어려울 때 주석 공시하며, 우발자산은 경제적 유입 가능성이 '높음(Probable)'인 경우에만 주석 공시하도록 강제하여 두 항목 간 비대칭적인 규칙을 설정한 핵심 이론적 배경은 무엇인가?",
        "options": [
            "① 기업의 영업 매출액을 2배로 강제 팽창시키기 위한 세무 목적이다.",
            "② 자산을 과대평가하거나 부채를 과소평가하여 정보이용자가 받게 될 재무적 오도와 왜곡을 미연에 방지하고자 하는 회계의 보수주의(Prudence) 및 신중성 원칙 때문이다.",
            "③ 외국 기업의 유입 투자를 규제하기 위한 법적 수단이다.",
            "④ 자산과 부채를 항상 상계하여 순액으로 표기하기 위해 유도된 분개 편의성이다.",
            "⑤ 회계사가 기장료를 더 많이 징수할 수 있도록 복잡성을 유도한 결과이다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우발자산과 우발부채의 인식 요건 비대칭성 배경입니다. 불확실성 상황에서 기업이 실현되지 않은 잠재적 이익(우발자산)을 섣불리 재무제표에 인식/공시하여 정보이용자를 오도하는 것은 막고, 잠재적 리스크(우발부채)는 잉여적으로 주석 기재하게 함으로써 재무적 건전성 및 신중성(보수주의)을 달성하고자 하는 회계학의 기본적 프레임워크가 작용하고 있습니다.\n\n[오답 해설]\n① 매출액 강제 팽창, ③ 외국 투자 규제, ④ 순액 상계 편의, ⑤ 회계사 수수료 연동 등은 회계 이론적 배경과 전혀 연관성이 없는 오답 설명입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-29",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-29",
        "year": "",
        "question": "K-IFRS 제1037호에 따른 우발부채 주석 공시 시, 정보이용자의 유용한 재무 분석을 위해 주석 본문에 필수적으로 기술(명시)되어야 하는 세부 사항에 해당하지 않는 것은?",
        "options": [
            "① 우발부채를 형성하는 과거 사건의 개요 및 성격 설명",
            "② 재무적 영향의 추정치 (가능한 경우)",
            "③ 자원의 유출 시기 및 금액과 관련된 불확실성의 정도와 징후",
            "④ 당해 우발채무를 변제(보상)받을 가능성 및 청구 권리의 명세",
            "⑤ 최대 주주의 향후 10개년 동안의 개인적인 자산 매각 계획 및 사적 지출 예상 예산서"
        ],
        "answer": "5",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True}
        ],
        "explanation": "⑤ 주주의 사적 자산 매각 계획 등은 기업 자체의 우발부채 주석 공시 필수 정보(IFRS 기준서 제1037호 문단 86)에 속하지 않으며, 공시할 권한 및 의무도 없습니다.\n\n[오답 해설]\n①, ②, ③, ④ 우발부채 주석 공시 시 기준서가 명시하고 있는 기업 의무 기재 4대 핵심 내역입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L1-30",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-30",
        "year": "",
        "question": "다음 중 기말 재검토 시 '우발부채' 상태의 채무가 K-IFRS 기준 상 재무상태표 본문에 계상할 '충당부채'로 상태가 공식 전이(인식)되기 위해 반드시 발생해야 하는 상황 변화로 가장 옳은 것은?",
        "options": [
            "① 관련 과거사건의 유출 가능성이 당초 '미미함' 수준에서 기말 현재 '가능성 높음(Probable, >50%)' 수준으로 격상되고, 지출액을 신뢰성 있게 측정할 수 있는 최선의 추정치가 확보된 경우",
            "② 이사회에서 감사를 전면 거부하기로 합의한 날",
            "③ 회사의 발행주식수가 갑자기 2배로 감자되어 자본 구조가 위축된 사건",
            "④ 거래처가 부도나서 당사의 매출채권을 전액 제거 처리한 날",
            "⑤ 관련 소송이 기각되어 법원 판결금이 ₩0으로 확정 소멸된 날"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 우발부채는 유출 가능성이 높지 않거나 측정이 어려워 부채 미계상된 상태입니다. 기중에 사건 정황이 진척되어 자원 유출 가능성이 50%를 초과(Probable)하게 되었고 신뢰성 있는 측정치가 수립되었다면, 인식요건 충족에 의해 기말 재무상태표 본문에 '충당부채'로 전이시켜 장부 계상하여야 합니다.\n\n[오답 해설]\n② 감사 거부나 ③ 감자 처리, ④ 매출채권 부도는 충당부채 인식 전환 요건과 상관이 없습니다.\n⑤ 소송 기각 및 판결금 ₩0 확정 시에는 부채 의무가 소멸하므로 충당부채 설정 대상이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },

    # --- L2 (이해): 15문항 (Q2411 ~ Q2425) ---
    {
        "id": "practice-accounting-ch09s02-L2-26",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-26",
        "year": "",
        "question": "K-IFRS 제1037호 하에서 경제적 효익을 갖는 자원의 유출 가능성이 '높음(Probable)' 수준을 충족하지만, 당해 의무의 이행에 소요될 지출 가액을 '신뢰성 있게 측정할 수 없는(Cannot be measured reliably)' 예외적인 현재의무가 발생하였다. 이 의무의 기말 올바른 회계적 분류 및 보고 방법은?",
        "options": [
            "① 측정할 수 없으므로 부채 총액을 ₩1,000,000의 가상 정액 충당부채로 기재한다.",
            "② 본문 부채(충당부채)로 계상하지 아니하고, '우발부채'로 분류하여 재무제표 주석에 공시한다.",
            "③ 부채가 아니므로 주석 공시를 포함하여 모든 공시 의무에서 영구 누락 처리한다.",
            "④ 유형자산의 취득원가에 직접 가산하여 자산화시킨다.",
            "⑤ OCI 평가 이익 자본으로 일단 잡고 차기 세무 조정에서 수정한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 기준 상 충당부채의 3대 인식요건(현재의무, 유출확률, 신뢰성 측정) 중 '신뢰성 있는 금액 측정 가능성'이 결여된 경우에는 본문 충당부채 인식을 할 수 없습니다. 이 경우 해당 의무는 '우발부채' 경로로 분류되어 주석 공시 대상이 됩니다.\n\n[오답 해설]\n① 임의 금액 기장은 회계 신뢰성 훼손으로 불인정됩니다.\n③ 주석 공시마저 누락하는 것은 우발부채 공시 의무 위반입니다.\n④ 자산 취득원가 가산 대상이 아닙니다.\n⑤ OCI 자본 대체 경로는 오답입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-27",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-27",
        "year": "",
        "question": "K-IFRS 제1037호 우발자산의 사후 회계처리와 관련하여, 기말에 공시되어 있던 '우발자산'이 실제 경제적 자원의 유입으로 실현되었거나 거의 확실(Virtually Certain)하게 되어 본문에 정식 자산으로 기장하는 경우, 이 자산 취득 및 당기 이익 인식 처리가 재무제표에 적용되는 시점 판단으로 옳은 것은?",
        "options": [
            "① 최초에 우발자산 주석을 공시하였던 과거 연도로 소급(Retroactive)하여 관련 연도 손익 재무제표를 재작성 반영한다.",
            "② 자산 유입 불확실성이 해소되어 자산이 실현되거나 거의 확실하게 된 '당해 당기 기간(전진 적용)'의 자산 및 당기순손익(수익 등)으로 인식한다.",
            "③ 영원히 자산으로 잡을 수 없고 주석에 평생 우발상태로 두어야 한다.",
            "④ 관련 자산 총액을 주식발행초과금 자본에 소급 가산하여 이월한다.",
            "⑤ 회사의 기중 법인세 차감액에만 직접 상계 기장 처리한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우발자산이 거의 확실(Virtually Certain)해져 자산으로 격상되는 조정은, 불확실성이 해소된 현시점의 새로운 회계적 경제적 사건입니다. 따라서 과거 재무제표 소급 수정 없이, 해당 확실성이 획득된 '당해 당기 기간(전진법)'의 재무제표 본문에 자산 및 당기 이익(수익)으로 적합하게 인식합니다.\n\n[오답 해설]\n① 소급 처리는 회계 추정의 본질과 어긋나며 인정되지 않습니다.\n③ 거의 확실해진 경우 우발자산 경로를 이탈하므로 주석 보류는 틀렸습니다.\n④ 자본잉여금(주발초) 직접 가산은 오류 분개입니다.\n⑤ 법인세 차감 상계는 기준 외 무관한 처리입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-28",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-28",
        "year": "",
        "question": "K-IFRS 제1037호에 의거하여, 기업이 우발자산의 주석 공시를 구성할 때 정보이용자 오도 방지를 위해 준수하여야 할 공시 문장 작성 지침(문단 89)으로 가장 옳은 것은?",
        "options": [
            "① 미래에 획득할 것으로 확실시되는 배상금액을 자산 확정액처럼 표기하고 당사의 무결성을 장담하여 기술해야 한다.",
            "② 수익이 발생하는 듯한 잘못된 인상을 주지 않도록, 자원의 유입 가능성 수준과 재무적 기대 영향의 미확정적 성격을 객관적이고 신중하게 기술하여야 한다.",
            "③ 가능성을 은폐하기 위해 구체적 수치는 모두 삭제하고 임의의 암호문 형태로 기재하여야 한다.",
            "④ 주석 본문에는 무조건 ₩100의 명목 가치로만 공정하게 표기하여야 한다.",
            "⑤ 경쟁사에 공포감을 주기 위해 예상 소송 가액을 10배로 과장 기술하여 공시해야 한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우발자산은 아직 미실현된 잠재적 경제적 유입 정보입니다. 따라서 주석 기재 시 정보이용자가 이 우발자산을 이미 확정된 실현 수익인 것처럼 오해하지 않도록, 불확실한 진행 상태와 유입 기대의 신중한 추정 논조를 정합하게 기재해야 합니다.\n\n[오답 해설]\n① 확정 자산처럼 과장 기술하거나, ③ 정보 은폐용 암호문 표기, ④ 명목 ₩100 일괄 기재, ⑤ 10배 과장 기술 등은 재무 정보의 신뢰성 및 충실한 표현(표현의 충실성) 요건을 위반한 심각한 왜곡입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-29",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-29",
        "year": "",
        "question": "K-IFRS 제1037호 문단 92에 따른 우발부채 주석 공시 제외의 '특별한 예외 상황(Prejudice 예외)'에 대한 설명으로 옳은 것은?",
        "options": [
            "① 기업의 당기순이익이 적자 상태일 때는 모든 우발부채 공시를 영구 생략할 수 있다.",
            "② 타사와의 소송 등 특정 분쟁 사건에서 K-IFRS가 요구하는 관련 우발부채 주석 공시 정보의 전체 혹은 일부를 상세 기재하는 것이, 분쟁 상대방에게 유리한 무기가 되어 당사에 '심각한 편견이나 피해(Seriously prejudice)'를 줄 것으로 예상되는 극히 예외적인 상황인 경우, 구체적 정보 공시를 생략하고 사건의 성격 및 공시 생략 사실과 그 사유만을 주석에 공시할 수 있다.",
            "③ 최대주주가 개인 비리로 기소되었을 때는 회사 재무상태표 전체 공시를 중단한다.",
            "④ 국세청의 세무조사가 착수된 당일에는 모든 장부 기재를 주석에서 완전 누락 처리해야 한다.",
            "⑤ 회사의 경쟁력이 낮아 실적 공시가 부끄러울 때는 모든 충당부채 환입 공시를 거부할 수 있다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 제1037호 문단 92의 예외 규정입니다. 소송 등 민감한 분쟁에서 구체적 금액이나 법적 조율 명세를 공시하는 것이 기업에 중대한 타격을 줄 정도로 심각한 피해를 유발하는 극히 예외적 경우에 한해, 세부 정보를 생략하고 분쟁의 일반적 성격과 공시 생략 이유만을 적는 예외 조항을 규정하고 있습니다.\n\n[오답 해설]\n① 당기순손실 적자 상황, ③ 주주 개인 비리, ④ 세무조사 착수, ⑤ 경쟁력 저하 등은 기준서 상 공시 의무 생략의 정당한 예외 조건이 될 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-30",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-30",
        "year": "",
        "question": "다음 중 K-IFRS 기준 상 보고기간 말(기말 결산일) 현재 시점의 경제적 유출/유입 가능성 확률 정보와 재무제표 표시 요건 간의 매칭이 가장 옳지 않은 것은?",
        "options": [
            "① 유출 가능성 80% (Probable, 신뢰성 측정 가능) -> 재무상태표 본문에 '충당부채'로 계상",
            "I② 유입 가능성 80% (Probable) -> 재무상태표 본문에 '우발자산' 계정으로 차변에 계상",
            "③ 유출 가능성 30% (Possible) -> 재무상태표 본문 부채 인식 배제 및 주석에 '우발부채'로 공시",
            "④ 유입 가능성 98% (Virtually Certain) -> 재무상태표 본문에 정식 '자산'으로 계상",
            "⑤ 유출 가능성 3% (Remote) -> 본문 부채 계상 제외 및 주석 공시도 생략 가능"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 자산(유입)의 경우 가능성이 높음(Probable, 80%) 수준에서는 아직 불확실성이 있어 정식 자산 계상을 할 수 없습니다. 이 경우 '우발자산'으로 보고하여 주석으로만 공시하여야 합니다. 본문 차변에 기재하는 것은 명백한 자산 과대계상 오류입니다.\n\n[오답 해설]\n①, ③, ④, ⑤ K-IFRS 제1037호 하의 유출/유입 가능성 단계별(Remote, Possible, Probable, Virtually Certain) 충당부채, 우발부채, 우발자산 및 자산의 올바른 대칭 기재 요건들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-31",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-31",
        "year": "",
        "question": "기업이 제3자를 위하여 채무보증(보증계약)을 서서 우발채무를 부담하고 있다. 당초에는 주채무자의 자금 사정이 양호하여 유출 가능성이 희박(Remote)했으나, 기중에 주채무자가 부도 위기에 처해 기말 현재 당사가 연대하여 대위상환할 가능성이 매우 높아진(Probable) 상태로 급변하였다. K-IFRS 기준 상 당기말에 취해야 하는 올바른 회계적 조치는?",
        "options": [
            "① 보증 책임은 자본 거래이므로 이익잉여금 처분계산서에만 이체하고 본문은 수정하지 않는다.",
            "② 유출 가능성이 아주 높아졌고 상환 의무액을 신뢰성 있게 추정할 수 있으므로, 기존 우발부채(주석) 분류에서 이탈하여 기말 재무상태표 대변에 '충당부채(보증충당부채)'를 인식하고 당기 비용으로 반영하여야 한다.",
            "③ 대위상환은 주주가 책임질 일이며 법적으로 부채 기장이 금지된다.",
            "④ 주채무자가 실제로 법적 파산 선고를 받기 전에는 무조건 주석으로만 방치해야 한다.",
            "⑤ 보증 채무액을 유형자산 토지 취득원가에 직접 합산 가산한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 채무보증 등의 우발부채 건도 기말 재검토 결과 자원 유출 가능성이 높음(Probable) 수준에 이르고 신뢰성 측정이 가능하다면 즉시 본문에 충당부채(보증충당부채)로 분개하여 인식하고 당기 손실비용으로 반영하여야 합니다.\n\n[오답 해설]\n① 자본 이체나 ⑤ 유형자산 가산 처리는 정합성이 없는 분개 오류입니다.\n③, ④ 실제 파산 선고 전이라도 보고기간 말 현재 의무 가능성이 유효하다면 충당부채 기장이 필수입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-32",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-32",
        "year": "",
        "question": "K-IFRS 제1037호에 따른 우발자산의 사후 기말 재검토에 대한 설명 중 가장 옳은 것은?",
        "options": [
            "① 우발자산은 보고기간 말마다 재검토하여, 경제적 효익의 유입 가능성이 높아진(Probable) 경우에 재무제표 주석에 우발자산으로 공시하고, 거의 확실(Virtually Certain)해진 경우 자산으로 계상한다. 반면, 유입 가능성이 더 이상 높지 않게 변동된 경우에는 주석 공시를 철회(생략)한다.",
            "② 우발자산은 한 번 기재하면 유입 가능성 변동에 상관없이 10년 동안 주석 공시를 강제 유지해야 한다.",
            "③ 가능성이 낮아지면 OCI 자본 항목에 강제 누적 차감한다.",
            "④ 최초 공시 시점에 자산으로 전액 소급 가산하여 자산총계를 복원한다.",
            "⑤ 우발자산의 재검토는 법원 최종 승인 시까지 잠정 중단하는 것이 원칙이다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 우발자산도 매 기말에 변경된 현행 가능성을 재검토합니다. 유입 가능성이 높지 않게(50% 이하로 하락) 재평가되었다면 더 이상 주석에 공시할 자격(요건 미달)을 잃으므로 공시에서 제외합니다. 반대로 거의 확실해지면 자산으로 본문 기장합니다.\n\n[오답 해설]\n② 가능성 하락 시 공시 제외가 규정이므로 10년 강제 유지는 거짓입니다.\n③ OCI 누적 자본 차감 등은 우발자산의 회계 경로에 맞지 않는 오류입니다.\n④ 우발자산은 본문 자산 소급 가산을 할 수 없습니다.\n⑤ 기말 시점의 현행 상황을 발생주의에 의해 기말마다 계속 업데이트 반영해야 합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-33",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-33",
        "year": "",
        "question": "K-IFRS 상 우발채무와 '약정사항(Commitments)'의 근본적인 차이에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 두 항목은 동일한 단어이므로 재무상태표 부채총계에 전액 가산한다.",
            "② 우발채무는 과거 사건의 결과로 유출 확률이 불확실한 잠재적 리스크인 반면, 약정사항은 계약 상대방과 미래 특정 거래(대출, 매입 등)를 실행하기로 맺은 구속력 있는 미이행 계약 성격의 미래 약속에 가깝다.",
            "③ 약정사항은 주주총회의 특별의결을 거치면 자본조정금으로 즉시 전환된다.",
            "④ 우발채무는 이자비용을 매달 발생시키지만 약정사항은 감가상각비를 발생시킨다.",
            "⑤ 두 항목 모두 재무상태표 본문에 자산 차감 계정으로 공시하는 공통점이 있다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 우발채무와 약정사항은 둘 다 주석 공시 대상이라는 유사점은 있으나, 성격이 다릅니다. 우발채무는 이미 발생한 과거 사건(소송, 부도 등)으로 유출 리스크가 불확실한 채무이고, 약정사항(Commitments)은 미래에 계약에 의거하여 특정 자금 대여, 설비 매입 등을 실행하기로 합의한 미이행 약속 거래 명세입니다.\n\n[오답 해설]\n① 두 항목은 본문 부채 기장이 불가합니다.\n③ 자본조정금 임의 전환이나, ④ 이자/상각비 발생설, ⑤ 자산 차감 계정 공시 등은 기준에 부합하지 않는 잘못된 오답 지문들입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-34",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-34",
        "year": "",
        "question": "K-IFRS 기준 상 동질한 과거 특허 소송 사건에 대하여 원고인 A사와 피고인 B사의 기말 회계처리에 대한 설명 중 옳은 것은?",
        "options": [
            "① A사와 B사 모두 유출입 가능성을 80%로 동등하게 판단할 때, A사는 재무상태표 본문에 정식 자산으로 기장하고 B사도 본문에 충당부채로 계상하여 대칭성을 이룬다.",
            "② A사와 B사 모두 가능성을 80%(Probable)로 판단하더라도 비대칭성 원칙에 의해, 피고인 B사는 현재의무 및 높은 유출 확률 요건 충족으로 본문에 '소송충당부채(부채)'를 인식하지만, 원고인 A사는 유입이 거의 확실(Virtually Certain)하지 않고 단지 높음(Probable) 수준이므로 본문에 자산을 잡을 수 없고 '우발자산' 주석 공시만 실행한다.",
            "③ 법원 최종 판결 전에는 A사, B사 모두 어떠한 주석 공시나 재무제표 기재도 완전히 금지된다.",
            "④ B사는 충당부채를 잡고 A사도 전액을 기타포괄손익 자본으로 직접 대변 기장한다.",
            "⑤ 두 회사 모두 영업외손실 ₩500,000을 일괄 분개하여 대차를 일치시킨다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 회계의 보수주의 및 신중성으로 인한 자산/부채의 비대칭적 인식 조건 예시입니다. 피고(B사)는 유출 가능성이 높으므로 본문 충당부채를 기장해야 하지만, 동일 사건의 대칭점인 원고(A사)는 자원의 유입 가능성이 거의 확실(Virtually Certain)한 단계에 이르지 못했으므로 본문 자산 기장을 할 수 없고 '우발자산' 주석 공시에 머물러 비대칭적 재무 상태를 나타내게 됩니다.\n\n[오답 해설]\n① A사는 Probable 수준에서는 본문 자산 계상을 할 수 없습니다.\n③ 최종 판결 전이라도 의무 성립 및 가능성 수준에 맞추어 주석 또는 충당부채 기장이 강제됩니다.\n④ A사의 OCI 자본 직접 기장이나 ⑤ 두 회사의 동일한 영업외손실 분개 등은 회계 논리에 어긋납니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch09s02-L2-35",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-35",
        "year": "",
        "question": "다음 중 K-IFRS 제1037호 하에서 우발부채(Contingent Liability)의 기말 주석 공시를 완벽하게 기술하기 위해 제공할 수 없는 항목은?",
        "options": [
            "① 관련 소송 및 분쟁 건의 개별 법적 사건번호 및 담당 판사/변호사의 사적인 신상 정보와 이메일 주소 명세",
            "② 의무를 이행할 경우 예상되는 재무적 영향의 최선 추정치",
            "③ 자원 유출의 시기와 금액 결정과 연동된 불확실성 요인 및 정황 설명",
            "④ 제3자 보상자산 변제 계약의 존재 및 회수 가능 금액에 대한 추정 정보",
            "⑤ 보고기간 말 현재 상황을 기준으로 합리적으로 도출된 추정 범위"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 법적 사건의 성격은 주석에 요약 기술하지만, 담당 판사나 변호사 개인의 신상 정보, 이메일 주소 등 사적인 영역은 기업의 재무 보고 주석 공시 사항에 해당하지 않으며 개인정보 보호법 위반 소지가 있습니다.\n\n[오답 해설]\n②, ③, ④, ⑤ K-IFRS 제1037호 문단 86 및 87에 따라 기업이 우발부채와 관련하여 주석에 공시 가능한 정합한 정보들입니다.",
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

print(f"Saved database with {len(questions)} questions. Added {len(new_questions)} questions.")
