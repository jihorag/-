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
    # L1: 기초 개념 (10문항, 1051~1060번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s03-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 제1016호 유형자산 기준서에서 최초 인식 이후 적용할 수 있도록 허용하고 있는 두 가지 후속 측정 모형으로 옳은 것은?",
        "options": [
            "① 취득원가모형, 공정가치평가모형",
            "② 원가모형, 재평가모형",
            "③ 손상차손모형, 감가상각모형",
            "④ 역사적원가모형, 현재가치모형",
            "⑤ 순공정가치모형, 사용가치모형"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 29에 따르면, 기업은 유형자산의 회계정책으로 원가모형(Cost model)이나 재평가모형(Revaluation model) 중 하나를 선택하여 유형자산 분류별로 동일하게 적용해야 합니다.\n\n[오답 해설]\n① 공정가치평가모형은 투자부동산 등에서 사용하는 명칭이며 유형자산은 '재평가모형'을 공식 명칭으로 씁니다.\n③, ④, ⑤는 기준서상 공식 후속 측정 모형 분류가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "공정가치평가모형은 투자부동산의 공정가치모형 등과 혼동한 오답입니다.", "articles": ["K-IFRS 제1016호 문단 29"], "principle": "유형자산의 후속 측정 모형", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "K-IFRS는 후속 측정 모형으로 원가모형과 재평가모형 두 가지만을 허용합니다.", "articles": ["K-IFRS 제1016호 문단 29"], "principle": "유형자산의 후속 측정 모형", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손상이나 감가상각은 모형의 하부 회계처리 요소일 뿐 독립된 모형 명칭이 아닙니다.", "articles": [], "principle": "유형자산의 후속 측정 모형", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "역사적원가모형 및 현재가치모형은 공식 명칭이 아닙니다.", "articles": [], "principle": "유형자산의 후속 측정 모형", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순공정가치와 사용가치는 손상차손 회수가능가액 측정 요소입니다.", "articles": [], "principle": "유형자산의 후속 측정 모형", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "유형자산의 재평가모형 적용 시 동일한 분류에 속하는 자산 전체를 동시에 재평가하도록 규정하는 K-IFRS의 주요 목적은?",
        "options": [
            "① 기업의 당기순이익을 극대화하여 재무 상태를 양호하게 보이게 하기 위함이다.",
            "② 자산의 선택적 재평가를 방지하고, 재무제표에 서로 다른 시점의 평가액이 혼재되는 것을 막기 위함이다.",
            "③ 감가상각액의 월할 계산을 간소화하기 위함이다.",
            "④ 세무상 취득세 환급 혜택을 극대화하기 위함이다.",
            "⑤ 회계법인의 외부감사 수수료를 절감하기 위함이다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 36에 따르면, 특정 유형자산을 재평가할 때 그 자산이 속하는 유형자산 분류 전체를 재평가해야 합니다. 이는 자산을 임의로 선택하여 재평가하거나 재무제표에 여러 시점의 원가와 평가액이 혼재되어 신뢰성을 해치는 것을 방지하기 위함입니다.\n\n[오답 해설]\n① 이익 조작 및 이익 극대화는 회계기준의 지향점이 아닙니다.\n③, ④, ⑤는 자산 분류별 일괄 재평가 규정의 도입 목적과 전혀 무관한 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "이익 인위적 극대화는 회계기준의 제정 취지에 부합하지 않습니다.", "articles": [], "principle": "분류별 일괄 재평가의 취지", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "선택적 재평가 방지 및 평가 시점 혼재로 인한 정보 왜곡 차단이 자산 일괄 재평가의 규정 목적임을 정확히 지목했습니다.", "articles": ["K-IFRS 제1016호 문단 36"], "principle": "분류별 일괄 재평가의 취지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각 계산의 편의와는 아무런 관계가 없습니다.", "articles": [], "principle": "분류별 일괄 재평가의 취지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지방세 및 세제 혜택과는 무관합니다.", "articles": [], "principle": "분류별 일괄 재평가의 취지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감사 수수료 절감은 규정의 회계이론적 근거가 아닙니다.", "articles": [], "principle": "분류별 일괄 재평가의 취지", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "유형자산에 대해 재평가모형을 선택한 경우, 재평가의 빈도(수행 주기)에 대한 K-IFRS의 원칙으로 가장 옳은 것은?",
        "options": [
            "① 공정가치의 변동성과 관계없이 매 회계연도 말에 강제적으로 재평가를 수행해야 한다.",
            "② 최초 재평가 이후 10년이 경과할 때마다 정기적으로 재평가한다.",
            "③ 재평가된 자산의 공정가치가 장부금액과 중요하게 차이가 나지 않도록 주기적으로 수행한다.",
            "④ 분기별 결산 시마다 외부 전문 감정기관의 평가를 거쳐 장부를 수정한다.",
            "⑤ 공정가치가 최초 취득원가보다 낮아질 때에만 한하여 임의로 수행한다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1016호 문단 34에 따르면, 재평가는 보고기간 말에 재평가자산의 장부금액이 공정가치와 중요하게 차이가 나지 않도록 주기적으로 수행합니다.\n\n[오답 해설]\n① 공정가치의 변동이 미미하다면 매년 평가할 필요가 없습니다.\n② 10년 주기 강제 규정은 없습니다.\n④ 분기별 강제 외부 평가는 과도한 비용을 유발하므로 규정하지 않습니다.\n⑤ 하락 시에만 수행하는 모형은 재평가모형이 아닌 손상검사 개념에 가깝습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "공정가치 변동성이 크지 않다면 매년 평가가 의무화되지는 않습니다.", "articles": ["K-IFRS 제1016호 문단 34"], "principle": "재평가의 수행 주기", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "10년 경과 의무 조문은 존재하지 않습니다.", "articles": [], "principle": "재평가의 수행 주기", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "공정가치와 장부금액이 중요하게 차이 나지 않도록 하는 적정 주기설이 기준서의 대원칙입니다.", "articles": ["K-IFRS 제1016호 문단 34"], "principle": "재평가의 수행 주기", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "분기별 평가 의무는 기준서의 요구사항이 아닙니다.", "articles": [], "principle": "재평가의 수행 주기", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "하락 시 임의 수행설은 재평가모형의 개념을 호도한 오답입니다.", "articles": [], "principle": "재평가의 수행 주기", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "최초로 유형자산을 재평가하여 자산의 장부금액이 증가(평가이익 발생)한 경우, K-IFRS 상 올바른 회계처리 및 계정 분류는?",
        "options": [
            "① 전액 당기이익으로 영업외수익에 가산한다.",
            "② 기타포괄손익(OCI)으로 인식하고 자본 항목인 '재평가잉여금'에 누적한다.",
            "③ 전액 기말의 매출이익으로 영업이익에 직접 합산한다.",
            "④ 이익잉여금의 전기이월액을 소급하여 증가시킨다.",
            "⑤ 부채 계정인 임의평가부채 과목에 적립한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 39에 따르면, 자산의 재평가로 인하여 장부금액이 증가한 경우 그 증가액은 기타포괄손익으로 인식하고 자본에 '재평가잉여금'으로 누적합니다. (단, 이전에 동일 자산에 대해 당기비용으로 잡은 재평가손실이 있는 경우 그 한도까지는 당기이익 인식)\n\n[오답 해설]\n① 최초 재평가 시의 상승액은 당기손익이 아닌 OCI 대상입니다.\n③ 영업이익 항목이 될 수 없습니다.\n④ 소급 적용하여 이익잉여금을 바로 늘리지 않습니다.\n⑤ 자산 평가 증가액은 부채 계정이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "최초 재평가 증가는 OCI이며 당기이익이 아닙니다.", "articles": ["K-IFRS 제1016호 문단 39"], "principle": "재평가 증가액의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산액 증가를 OCI로 인식하여 자본의 재평가잉여금으로 누적함을 올바르게 지목했습니다.", "articles": ["K-IFRS 제1016호 문단 39"], "principle": "재평가 증가액의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출이익이나 영업이익으로 잡을 수 없습니다.", "articles": [], "principle": "재평가 증가액의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소급법에 따른 이익잉여금 조정 거래가 아닙니다.", "articles": [], "principle": "재평가 증가액의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 평가 상승액은 자본 요소이지 부채가 아닙니다.", "articles": [], "principle": "재평가 증가액의 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "최초로 유형자산을 재평가하여 자산의 장부금액이 감소(평가손실 발생)한 경우, K-IFRS가 요구하는 기본적인 회계처리 분류는?",
        "options": [
            "① 전액 기타포괄손익(OCI)으로 인식하여 자본 차감 항목으로 둔다.",
            "② 전액 당기손익(당기비용, 재평가손실)으로 인식한다.",
            "③ 자본금의 직접 감자 항목으로 상계 처리한다.",
            "④ 무형자산 감액손실로 대체 기재한다.",
            "⑤ 회계오류수정의 소급 누적으로 보아 차기 자본을 직접 감소시킨다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 40에 따르면, 자산의 재평가로 인하여 장부금액이 감소한 경우 그 감소액은 당기손익으로 인식합니다. (단, 기존에 해당 자산과 관련하여 자본에 누적된 재평가잉여금이 있다면 OCI 범위 내에서 먼저 차감)\n\n[오답 해설]\n① 최초 감소는 OCI 잔액이 없으므로 전액 당기비용입니다.\n③, ⑤ 자본금 직접 감자나 오류수정이 아닌 일반 거래적 평가손실입니다.\n④ 무형자산과 유형자산은 구분되므로 대체할 수 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "최초 감소 시에는 차감할 잉여금 잔액이 없으므로 OCI 차감이 불가능합니다.", "articles": ["K-IFRS 제1016호 문단 40"], "principle": "재평가 감소액의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "이전 잉여금 잔액이 없는 최초 감소액은 전액 당기손익(당기비용) 처리함을 바르게 기재했습니다.", "articles": ["K-IFRS 제1016호 문단 40"], "principle": "재평가 감소액의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 직접 감자는 주총 결의 등을 요하는 별도의 법적 자본조정 거래입니다.", "articles": [], "principle": "재평가 감소액의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 분류 오류입니다.", "articles": [], "principle": "재평가 감소액의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과거 회계오류가 아니므로 소급하지 않습니다.", "articles": [], "principle": "재평가 감소액의 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "감가상각 유형자산을 재평가하는 경우, 재평가일의 장부금액이 공정가치와 일치하도록 감가상각누계액을 조정하는 두 가지 K-IFRS 인정 방법의 명칭으로 옳은 것은?",
        "options": [
            "① 정액법, 정률법",
            "② 비례수정법, 누계액제거법",
            "③ 손상차손누계액법, 공정가치법",
            "④ 직접차감법, 이연법",
            "⑤ 회수금액법, 잔존가치법"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 35에 따르면, 유형자산을 재평가할 때 재평가일의 누적감가상각액은 자산 장부금액의 변동에 비례하여 수정(비례수정법)하거나, 자산의 총장부금액에서 제거(누계액제거법)하여 처리합니다.\n\n[오답 해설]\n① 정액법과 정률법은 감가상각 방법입니다.\n③, ④, ⑤는 감가상각누계액의 후속 재평가 조정 방법의 공식 명칭이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "감가상각 방법을 묻는 질문이 아니므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 35"], "principle": "재평가 시 감가상각누계액 조정법", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "K-IFRS에서 규정하는 비례수정법과 누계액제거법 두 명칭을 바르게 제시했습니다.", "articles": ["K-IFRS 제1016호 문단 35"], "principle": "재평가 시 감가상각누계액 조정법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손상 관련 계정 명칭과의 혼동 오류입니다.", "articles": [], "principle": "재평가 시 감가상각누계액 조정법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각누계액 조정법의 정식 규정 명칭이 아닙니다.", "articles": [], "principle": "재평가 시 감가상각누계액 조정법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 오답 단어들의 조합입니다.", "articles": [], "principle": "재평가 시 감가상각누계액 조정법", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "유형자산 재평가 시 '누계액제거법(Elimination method)'을 적용하여 기장하는 기본 원리에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 감가상각누계액은 전혀 건드리지 않고 취득원가만 공정가치로 변경한다.",
            "② 누적된 감가상각누계액을 전액 제거하여 자산의 순장부금액만 남긴 후, 이 순액이 공정가치와 일치하도록 자산 가액을 증감시킨다.",
            "③ 자산의 취득원가와 감가상각누계액을 동일한 백분율로 인상 조정한다.",
            "④ 감가상각누계액을 임의의 부채 계정으로 전출시킨다.",
            "⑤ 감가상각누계액 잔액만큼을 즉시 당기이익으로 잡고 제거한다."
        ],
        "answer": "2",
        "explanation": "② 누계액제거법은 기존의 감가상각누계액 잔액을 전액 자산의 원가계정과 상쇄하여 제거한 뒤, 순액으로 표시된 자산금액을 기말 공정가치로 조정하는 방식입니다. 주로 공정가치 정보가 단일 가액으로 주어졌을 때 분개가 간단한 장점이 있습니다.\n\n[오답 해설]\n① 누계액을 전혀 건드리지 않는 방식은 제거법이 아닙니다.\n③ 취득원가와 누계액을 비례 조정하는 것은 '비례수정법'에 속합니다.\n④, ⑤ 부채 전출이나 즉시 당기이익 환입 등은 적법한 분개가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "누계액 제거 분개가 발생하므로 틀렸습니다.", "articles": ["K-IFRS 제1016호 문단 35"], "principle": "누계액제거법의 기본 원리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "누계액을 최초에 전액 제거해 순액 상태로 만든 후 공정가치와 일치되도록 원가를 조정하는 방식임을 명확히 서술했습니다.", "articles": ["K-IFRS 제1016호 문단 35"], "principle": "누계액제거법의 기본 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비례 수정하는 것은 비례수정법의 성격입니다.", "articles": ["K-IFRS 제1016호 문단 35"], "principle": "누계액제거법의 기본 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채와 자본의 성격을 왜곡한 보도 오류입니다.", "articles": [], "principle": "누계액제거법의 기본 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "누계액 제거 자체가 바로 당기이익으로 가지 않고 자산가액과 퉁쳐집니다.", "articles": [], "principle": "누계액제거법의 기본 원리", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "유형자산 재평가 시 '비례수정법(Proportionate restatement method)'을 적용하여 기장하는 기본 원리에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 감가상각누계액을 무조건 최초 취득원가와 같은 금액으로 강제 인상한다.",
            "② 누계액을 전액 제거하여 자산 취득원가를 공정가치와 같게 일치시킨다.",
            "③ 자산의 순장부금액이 재평가액과 일치하도록, 자산의 총장부금액(원가)과 감가상각누계액을 동일한 비례 비율로 조정한다.",
            "④ 감가상각누계액을 매 기말의 이자율로 할인하여 현재가치로 개정한다.",
            "⑤ 감가상각누계액에 대해서만 OCI를 개별 계상하고 자산원가는 동결한다."
        ],
        "answer": "3",
        "explanation": "③ 비례수정법은 재평가 시점의 순장부금액이 공정가치가 되도록 자산의 총장부금액(취득원가 등)과 감가상각누계액을 비례하여 늘리거나 줄이는 방법입니다.\n\n[오답 해설]\n① 누계액을 원가와 같게 만들면 장부금액이 0이 되므로 모순입니다.\n② 누계액을 전액 제거하는 것은 누계액제거법입니다.\n④, ⑤는 비례수정법의 계산 원리와 무관한 잘못된 설명입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "취득원가와 같게 조정한 비율 수정이 아니므로 오답입니다.", "articles": [], "principle": "비례수정법의 기본 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "누계액제거법의 특징을 잘못 설명한 것입니다.", "articles": ["K-IFRS 제1016호 문단 35"], "principle": "비례수정법의 기본 원리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "순장부가액이 공정가치가 되도록 취득원가와 누계액을 동시에 일정한 비율로 조정함을 정확히 지적했습니다.", "articles": ["K-IFRS 제1016호 문단 35"], "principle": "비례수정법의 기본 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "현재가치 할인법과의 무관한 진술입니다.", "articles": [], "principle": "비례수정법의 기본 원리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "누계액에 대해서만 OCI를 단독 적립하지 않습니다.", "articles": [], "principle": "비례수정법의 기본 원리", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "K-IFRS 상 유형자산 재평가잉여금의 이익잉여금 대체와 관련된 당기손익(처분손익 등) 재분류 조정(Recycling) 가능성에 대한 규정으로 가장 옳은 것은?",
        "options": [
            "① 자산을 처분하는 시점에 재평가잉여금 전액이 처분이익으로 재분류되어 당기순이익을 증가시킨다.",
            "② 재평가잉여금은 기타포괄손익누계액이므로 자산의 사용이나 제거 시 절대로 당기손익으로 재분류 조정될 수 없다.",
            "③ 감가상각 매기마다 대체되는 잉여금액은 당기 판관비 차감 항목으로 기재되어 순이익을 올린다.",
            "④ 재평가잉여금은 법인세 효과 배분 단계에서 전액 당기 법인세 비용으로 자동 재분류된다.",
            "⑤ 회사의 이사회 결의가 있으면 당기순이익으로 자유롭게 이체할 수 있다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 41에 명시된 바와 같이, 유형자산의 재평가잉여금은 자산이 사용되거나 제거(처분)될 때 이익잉여금으로 직접(자본 내부에서) 대체될 수 있을 뿐, 결코 당기손익(처분손익 등)으로 재분류되어 포괄손익계산서상 당기순이익에 영향을 미칠 수 없습니다. 이를 '재분류조정 금지(No Recycling)' 원칙이라고 합니다.\n\n[오답 해설]\n① 처분 시 처분이익(당기손익)으로 가지 않고 이익잉여금(자본)으로 바로 가므로 오답입니다.\n③, ⑤ 당기순이익을 경유하거나 판관비를 차감할 수 없습니다.\n④ 법인세 배분에서도 자본(OCI)에 직접 가감되므로 당기비용으로 재분류되지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "당기 처분손익(당기이익)으로 재분류되지 않으므로 틀렸습니다.", "articles": ["K-IFRS 제1016호 문단 41"], "principle": "재평가잉여금의 재분류조정 금지", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재평가잉여금은 당기손익으로의 재분류조정이 원천 배제되어 있으며 오직 자본 내에서 이익잉여금으로 직접 대체될 수 있을 뿐임을 바르게 묘사했습니다.", "articles": ["K-IFRS 제1016호 문단 41"], "principle": "재평가잉여금의 재분류조정 금지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "판관비 비용을 차감하는 식의 당기손익 간섭은 불가합니다.", "articles": [], "principle": "재평가잉여금의 재분류조정 금지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "법인세 비용 재분류 주장은 회계오류입니다.", "articles": [], "principle": "재평가잉여금의 재분류조정 금지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자의적인 당기순이익 이체는 자본거래와 손익거래의 구분 원칙에 저촉됩니다.", "articles": [], "principle": "재평가잉여금의 재분류조정 금지", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "유형자산에 대해 '원가모형'을 적용하는 경우, 기말 재무상태표에 표시되는 장부금액(Carrying amount)의 올바른 산출 기준은?",
        "options": [
            "① 기말 현재 외부 감정평가법인이 평가하여 통보한 공정가치",
            "② 최초 취득원가에서 감가상각누계액과 손상차손누계액을 차감한 금액",
            "③ 취득원가에 매년의 도매물가상승률을 복리로 곱하여 보정한 가액",
            "④ 기말 현재 자산을 강제 매각할 때 유입될 수 있는 순공정가치",
            "⑤ 취득원가에 그동안 계상한 모든 감가상각비 누적액을 더한 합계금액"
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 30에 따르면, 원가모형을 적용하는 유형자산은 최초 인식 후에 취득원가에서 감가상각누계액과 손상차손누계액을 차감한 금액을 장부금액으로 보고합니다.\n\n[오답 해설]\n①, ④는 재평가모형이나 자산 평가액 측정법에 가깝습니다.\n③ 물가상승률 반영은 역사적 원가주의에 저촉되는 오답입니다.\n⑤ 누계액을 빼야 하므로 더한 합계액이라는 설명은 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "공정가치는 재평가모형에서 기준이 됩니다.", "articles": ["K-IFRS 제1016호 문단 30"], "principle": "원가모형 장부금액 산정 방식", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "취득원가에서 감누와 손상차손누계를 뺀 순액으로 보고함이 원가모형의 정확한 측정 정의입니다.", "articles": ["K-IFRS 제1016호 문단 30"], "principle": "원가모형 장부금액 산정 방식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "인플레이션 물가조정 회계는 일반 K-IFRS 원가모형에 허용되지 않습니다.", "articles": [], "principle": "원가모형 장부금액 산정 방식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순공정가치는 자산 평가액이 아닌 손상검사 지표 중 하나입니다.", "articles": [], "principle": "원가모형 장부금액 산정 방식", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각누계를 가산하면 안 되고 차감해야 하므로 정반대 서술입니다.", "articles": [], "principle": "원가모형 장부금액 산정 방식", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },

    # =========================================================================
    # L2: 이해 및 기준 조문 (15문항, 1061~1075번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s03-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "K-IFRS 상 유형자산의 재평가모형을 적용할 때 동일한 분류 내의 일부 개별 자산에만 선택적 재평가를 적용하는 것이 금지되는 실무적 이유로 가장 올바른 것은?",
        "options": [
            "① 동일 분류 내의 모든 자산은 감가상각 기간이 완전히 같아야 하기 때문이다.",
            "② 기업이 원하는 유리한 자산만 선별 평가하여 자산의 가치를 인위적으로 왜곡하고 장부금액이 혼재되는 것을 차단하기 위함이다.",
            "③ 일괄 재평가를 하지 않으면 세법상 특별법인세가 부과되기 때문이다.",
            "④ 기말 외부 감정평가 보고서 수량을 줄여 회사의 관리 업무를 줄여주기 위함이다.",
            "⑤ 회사의 최대주주 지분가치를 동결하기 위함이다."
        ],
        "answer": "2",
        "explanation": "② 자산의 일괄 재평가 규정이 없을 경우, 기업이 가격이 상승한 자산만 골라 재평가하고 가격이 하락한 자산은 원가모형으로 방치하는 등의 기회주의적 회계선택을 통해 자산가액 및 자기자본을 부풀릴 수 있기 때문에 이를 엄격히 차단하려는 목적이 있습니다.\n\n[오답 해설]\n① 개별 자산마다 상각 기간은 다를 수 있으며, 이는 일괄 재평가 금지 요건과 연관이 없습니다.\n③, ④, ⑤는 임의적으로 지어낸 회계기준 외적이고 타당성 없는 내용들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산마다 수명이나 감가상각 기간은 다를 수 있으므로 무관한 항목입니다.", "articles": [], "principle": "개별 선택적 재평가 금지의 실무적 취지", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기업이 유리한 자산만 취사선택해 가치를 부풀리는 기회주의적 평가 왜곡을 원천 배제하려는 목적을 정확히 기술했습니다.", "articles": ["K-IFRS 제1016호 문단 36"], "principle": "개별 선택적 재평가 금지의 실무적 취지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법상 부과금이나 징벌세 규정과는 관련이 없습니다.", "articles": [], "principle": "개별 선택적 재평가 금지의 실무적 취지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "보고서 수량 감소나 업무 축소는 규정의 본질과 거리가 멉니다.", "articles": [], "principle": "개별 선택적 재평가 금지의 실무적 취지", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "최대주주 지분 변동 관리와는 관계가 없습니다.", "articles": [], "principle": "개별 선택적 재평가 금지의 실무적 취지", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "유형자산 재평가모형 하에서 직전 연도에 장부 감소로 당기비용(재평가손실)을 잡았던 기계장치의 공정가치가 당기 말에 다시 반등 상승하여 평가이익이 발생한 경우, K-IFRS 상 상계 원칙으로 가장 옳은 것은?",
        "options": [
            "① 과거 당기비용으로 털었던 재평가손실을 한도로 당기순이익(재평가이익)으로 인식하고, 이를 초과하는 상승분만 기타포괄손익(OCI)으로 인식한다.",
            "② 이전 기록과 상관없이 당기 상승분 전액을 기타포괄손익(OCI)으로 인식하여 자본에 얹는다.",
            "③ 상승분 전체를 즉시 당기순이익(영업외수익)으로 일괄 보고하여 세금을 정산한다.",
            "④ 직전 연도 감소분을 소급법으로 취소 분개하여 당기 자본에서 직접 가산한다.",
            "⑤ 상승한 공정가치를 장부에 기재할 수 없으며 주석으로만 공시한다."
        ],
        "answer": "1",
        "explanation": "① K-IFRS 제1016호 문단 39에 따르면, 자산의 재평가로 인해 장부금액이 증가한 경우, 그 자산에 대하여 이전에 당기손익으로 인식한 재평가감소액(재평가손실)이 있다면 그 금액을 한도로 증가액을 당기이익(재평가이익)으로 인식하고, 초과분에 대해서만 기타포괄손익(재평가잉여금)으로 인식하도록 정하고 있습니다.\n\n[오답 해설]\n② 이전의 평가손실 당기비용 인식을 무시하고 전액 OCI로 가면 손익 왜곡이 발생하여 부적정합니다.\n③ 전액 당기이익으로 갈 수 없고 과거 비용 범위 내에서만 허용됩니다.\n④ 소급 수정이 아닌 당기 및 차기 전진 적용 방식입니다.\n⑤ 재평가모형이므로 공정가치를 장부 본문에 변경 반영해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "이전에 인식한 당기손실 범위 내에서는 당기이익(재평가이익)으로 환입하고 초과액만 OCI로 누적한다는 상계 원칙을 정확히 지적했습니다.", "articles": ["K-IFRS 제1016호 문단 39"], "principle": "재평가 상승 시 상계 법칙", "case": {"holding": "기계장치", "no": None}},
            {"correct": False, "why": "이전 당기비용 인식분을 복구하는 단계를 누락해 틀렸습니다.", "articles": [], "principle": "재평가 상승 시 상계 법칙", "case": {"holding": "기계장치", "no": None}},
            {"correct": False, "why": "전액 영업외수익은 자본잉여금으로 갈 자본 요소를 당기순이익에 이중 포함시키는 심각한 회계 오류입니다.", "articles": [], "principle": "재평가 상승 시 상계 법칙", "case": {"holding": "기계장치", "no": None}},
            {"correct": False, "why": "소급법은 이 평가 변경 거래에 쓸 수 없습니다.", "articles": [], "principle": "재평가 상승 시 상계 법칙", "case": {"holding": "기계장치", "no": None}},
            {"correct": False, "why": "본문 수정이 이루어져야 하므로 오답입니다.", "articles": [], "principle": "재평가 상승 시 상계 법칙", "case": {"holding": "기계장치", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "유형자산 재평가모형 적용 하에서 이전에 평가 상승으로 계상한 재평가잉여금(자본) 잔액이 존재하는 건물에 대해, 당기 말 재평가로 인해 자산 장부금액이 감소하는 경우의 회계처리 상계 기준으로 옳은 것은?",
        "options": [
            "① 이전 적립금 잔액과 관계없이 감소액 전액을 당기 재평가손실(당기비용)로 턴다.",
            "② 해당 자산의 재평가잉여금 잔액 범위 내에서 감소액을 OCI(재평가잉여금 감소)로 차감하고, 이를 초과하는 감소액 부분만 당기비용(재평가손실)으로 인식한다.",
            "③ 감소액 전액을 이익잉여금 조정을 통해 이월 잉여금에서 직접 깎아낸다.",
            "④ 건물의 취득세 환급 신청 분개로 임의 처리한다.",
            "⑤ 감소액을 감가상각누계액 증가로만 기재하고 OCI는 손대지 않는다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 40에 따라, 재평가로 인해 자산의 장부금액이 감소하는 경우 그 감소액은 당기손익으로 인식합니다. 그러나 해당 자산에 대해 기존에 적립된 기타포괄손익인 '재평가잉여금' 잔액이 있다면 그 잔액 범위 내에서 기타포괄손익(재평가잉여금의 감소)으로 먼저 상쇄 처리하고, 초과분에 대해서만 당기비용으로 인식하여야 합니다.\n\n[오답 해설]\n① 잉여금 상계 과정을 누락하고 전액 당기비용화하면 자본 잔액이 이중 과대 계상되고 순이익은 왜곡되므로 틀렸습니다.\n③, ⑤ 이익잉여금 직접 수정이나 잉여금 묵인은 회계 원리에 어긋납니다.\n④ 세무상 취득세 환급과는 연관이 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "기존 재평가잉여금(자본) 잔액 상계를 빠뜨렸으므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 40"], "principle": "재평가 하락 시 상계 법칙", "case": {"holding": "건물", "no": None}},
            {"correct": True, "why": "기존 잉여금(OCI) 잔액을 먼저 감소시켜 상쇄하고, 이를 초과하는 잔여 감소액만 당기 재평가손실(P&L)로 계상함을 올바르게 지목했습니다.", "articles": ["K-IFRS 제1016호 문단 40"], "principle": "재평가 하락 시 상계 법칙", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "이익잉여금 직접 조정은 손익 계산 단계를 건너뛰는 불법 기장입니다.", "articles": [], "principle": "재평가 하락 시 상계 법칙", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "세제 관련 설명은 엉뚱한 기술입니다.", "articles": [], "principle": "재평가 하락 시 상계 법칙", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "감누의 자의적 수정으로 OCI 잔액을 방치하는 처리는 회계원리에 위배됩니다.", "articles": [], "principle": "재평가 하락 시 상계 법칙", "case": {"holding": "건물", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "재평가모형을 적용하는 유형자산의 기말 평가 시, 당기 감가상각비를 인식하는 순서에 대한 K-IFRS의 올바른 원칙은?",
        "options": [
            "① 당기 감가상각비 인식을 생략하고 기말 공정가치 재평가만 이행한다.",
            "② 기말 공정가치 재평가를 먼저 수행한 후, 그 평가된 금액을 기초로 당기 감가상각비를 거꾸로 산출하여 정산한다.",
            "③ 당기 중에는 감가상각비를 적절히 계상한 후, 기말 시점에 당기 감가상각을 완전히 마친 기말 장부금액을 확정한 다음에 기말 공정가치와 비교하여 재평가손익을 구한다.",
            "④ 감가상각비는 3년에 한 번만 인식하고 평소에는 공정가치로 퉁친다.",
            "⑤ 공정가치 변동액이 당기 감가상각비 예상액보다 클 때에만 감가상각을 이행한다."
        ],
        "answer": "3",
        "explanation": "③ 재평가모형 자산이라 하더라도, 기말에 공정가치 재평가 조정을 수행하기 직전 단계에 당기 1년 동안 발생한 자산의 노후화분인 당기 감가상각비를 먼저 정상적으로 분개 기입하여 기말 현재의 장부금액을 도출해낸 후, 이 최종 장부금액을 바탕으로 공정가치와 비교하여 평가손익을 인식하는 순서를 지켜야 합니다.\n\n[오답 해설]\n① 재평가모형 자산이라 하여 감가상각을 생략할 수는 없습니다.\n② 순서가 역전된 잘못된 설명입니다.\n④, ⑤는 임의의 계산 지침으로 감가상각의 체계적 배분 원칙을 무시한 틀린 진술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "상각 생략은 감가상각 목적을 저버리는 오답입니다.", "articles": ["K-IFRS 제1016호 문단 50"], "principle": "재평가 시 감가상각과 재평가의 처리 순서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순서가 뒤바뀌어 평가 전 상각 완료 원칙을 어겼습니다.", "articles": ["K-IFRS 제1016호 문단 35, 50"], "principle": "재평가 시 감가상각과 재평가의 처리 순서", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "당기분 상각을 먼저 완벽히 수행하여 기말 장부가액을 확정하고, 이를 기말 공정가치와 대조하여 재평가함을 가장 잘 묘사했습니다.", "articles": ["K-IFRS 제1016호 문단 35, 50"], "principle": "재평가 시 감가상각과 재평가의 처리 순서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각의 기간 배분 원칙에 저촉됩니다.", "articles": [], "principle": "재평가 시 감가상각과 재평가의 처리 순서", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "금액 크기 대조에 의한 임의 상각설은 오답입니다.", "articles": [], "principle": "재평가 시 감가상각과 재평가의 처리 순서", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "유형자산 재평가모형 하에서 감가상각 대상 자산의 재평가 이후에 인식할 차기 감가상각비의 계산 공식의 성격에 대한 설명으로 옳은 것은?",
        "options": [
            "① 재평가 이전의 최초 취득가와 잔존가치 기준을 만기까지 강제 고수하여 상각비를 동일하게 유지한다.",
            "② 재평가로 새로 조정된 공정가치 장부금액을 기초로, 변경되거나 기존인 잔여내용연수와 새로운 잔존가치를 전진적으로(Prospective) 대입하여 감가상각비를 다시 계산한다.",
            "③ 이전의 감가상각비 전체를 취소하고 재작성하는 소급법을 쓴다.",
            "④ 재평가 이후에는 자산이 공정가치 상태이므로 감가상각이 영구 중단된다.",
            "⑤ 재평가 후에는 연수합계법만 강제적으로 적용한다."
        ],
        "answer": "2",
        "explanation": "② 재평가가 발생한 경우 이는 회계추정의 변경 효과와 맞물립니다. 따라서 재평가 후에는 조정된 공정가치 장부금액에서 변경된 잔존가치를 빼고, 이를 남은 잔여내용연수로 나눈 새로운 감가상각비를 전진법으로 계산하여 차기 이후 결산에 올립니다.\n\n[오답 해설]\n① 평가를 통해 장부가액이 변했으므로 상각비를 변경 없이 유지하는 것은 불가합니다.\n③ 감가상각비 조정은 정책변경이나 오류수정이 아니므로 소급하지 않습니다.\n④ 상각대상 자산(예: 건물, 기계)은 재평가 여부와 상관없이 소모되므로 감가상각을 멈추면 안 됩니다.\n⑤ 감가상각방법의 변경이 동반되지 않는 한 기존 상각법(예: 정액법 등)을 유지하는 것이 맞습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산액이 바뀐 경우 새로운 조건에 따라 상각비가 재조정되어야 하므로 동일 유지설은 틀렸습니다.", "articles": ["K-IFRS 제1016호 문단 51"], "principle": "재평가 후 감가상각비 재계산", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재평가액을 기준으로 잔여 수명과 잔존가치 변경을 반영하여 전진적으로 상각비를 재산출하는 전진법 원리를 바르게 서술했습니다.", "articles": ["K-IFRS 제1016호 문단 51"], "principle": "재평가 후 감가상각비 재계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "감가상각 추정 조정을 소급하는 것은 회계기준 위반입니다.", "articles": ["K-IFRS 제1008호"], "principle": "재평가 후 감가상각비 재계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각대상 자산의 상각 중단 주장은 중대한 회계 오류입니다.", "articles": [], "principle": "재평가 후 감가상각비 재계산", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기존 상각방법을 계승하는 것이 원칙이므로 특정 방법 강제설은 오답입니다.", "articles": [], "principle": "재평가 후 감가상각비 재계산", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "K-IFRS 제1016호에 의거, 자산을 사용하는 과정에서 발생하는 재평가잉여금의 이익잉여금 대체(Transfer) 회계처리에 대한 설명 중 옳은 것은?",
        "options": [
            "① 재평가잉여금을 매기 이익잉여금으로 이체할 때 당기순이익에 산입하여 영업외수익으로 보고한다.",
            "② 재평가된 금액에 기초한 감가상각비와 역사적원가에 기초한 감가상각비의 차이만큼을 재평가잉여금에서 이익잉여금으로 직접(자본 내부에서) 대체할 수 있다.",
            "③ 대체 분개 수행 시 당기 법인세 비용이 즉시 환입 처리된다.",
            "④ 사용에 따른 대체는 강제 규정이므로 무조건 매달 실행해야 하며 일괄 대체는 불가능하다.",
            "⑤ 이 이체 금액은 회사의 배당가능이익 한도 계산에서 제외된다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 41에 따르면, 기업은 자산을 사용하는 과정에서 일부 재평가잉여금을 이익잉여금으로 대체할 수 있으며, 이 경우 대체할 금액은 재평가된 금액에 기초한 감가상각비와 최초원가에 기초하여 인식하였을 감가상각비의 차이로 계산합니다. 이때 이체 분개는 자본계정 간의 직접 대체이므로 당기순이익에 절대 반영되지 않습니다.\n\n[오답 해설]\n① 손익계산서를 거쳐 수익으로 보고하면 재분류 금지 원칙에 위배되므로 자본 내부의 직접 분개여야 합니다.\n③ 법인세 직접 환입은 불허됩니다.\n④ 사용에 따른 대체는 기업의 '선택' 사항입니다. 대체하지 않고 자산 처분 시 일시 대체하는 것도 허용됩니다.\n⑤ 이익잉여금으로 직접 대체되는 금액은 상법상 주주 배당 가능이익의 원천에 합산될 수 있습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "이익잉여금 대체는 자본 내부 이체 분개일 뿐 당기 손익 수익 인식이 아닙니다.", "articles": ["K-IFRS 제1016호 문단 41"], "principle": "재평가잉여금의 사용에 따른 대체", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재평가 장부가 기준 상각비와 기존 원가 기준 상각비의 차액을 자본계정 간 직접 이체할 수 있다는 K-IFRS 원칙을 완벽히 기술했습니다.", "articles": ["K-IFRS 제1016호 문단 41"], "principle": "재평가잉여금의 사용에 따른 대체", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세무 조정 법인세 계정 환입과는 관계가 없습니다.", "articles": [], "principle": "재평가잉여금의 사용에 따른 대체", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매기 대체 적용 여부는 기업의 선택(임의) 사항이므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 41"], "principle": "재평가잉여금의 사용에 따른 대체", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자유 적립된 이익잉여금으로 변모하므로 배당 재원에 영향이 발생할 수 있습니다.", "articles": [], "principle": "재평가잉여금의 사용에 따른 대체", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "유형자산 재평가모형 하에서 자본에 재평가잉여금이 남아 있는 토지를 제3자에게 매각 처분하였을 때, 재평가잉여금의 최종 처리로 올바른 회계적 규정은?",
        "options": [
            "① 처분 시점에 처분잉여금 전액을 처분 이익(당기손익)에 누적 합산한다.",
            "② 자산의 제거와 관련하여 장부에 남아 있던 재평가잉여금 잔액 전액을 이익잉여금(자본)으로 직접 대체할 수 있다.",
            "③ 남아 있는 재평가잉여금은 자산이 처분되더라도 주주 총회 결의 전까지는 절대 건드릴 수 없다.",
            "④ 재평가잉여금은 국고보조금으로 취소 반환 처리하여 소멸시킨다.",
            "⑤ 토지 매각 대금으로 직접 수령하여 자산화한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 41에 의거하여, 자산이 처분되거나 완전히 장부에서 폐기 제거되는 시점에 해당 자산에 귀속되어 남아 있던 재평가잉여금 잔액 전체는 이익잉여금으로 직접(자본 내의 대체 분개로) 전액 이체할 수 있습니다.\n\n[오답 해설]\n① 처분이익 당기순이익으로 재분류되지 않으므로 틀렸습니다.\n③ 제거되는 시점에 이익잉여금으로 직접 대체하는 것이 정당하므로 처분 후 동결설은 오답입니다.\n④ 국고보조금 상계나 소멸과 아무런 관계가 없습니다.\n⑤ 회계 분개 상 자본 내부 이체 거래이므로 현금 수령과는 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재분류조정으로 당기 처분이익을 늘리는 분개는 회계위반입니다.", "articles": ["K-IFRS 제1016호 문단 41"], "principle": "처분 시 재평가잉여금의 이익잉여금 대체", "case": {"holding": "토지", "no": None}},
            {"correct": True, "why": "자산 제거(처분) 시에 남아 있는 잉여금 전액을 자본 내에서 이익잉여금으로 직접 쏠 수 있도록 규정한 조문을 바르게 진술했습니다.", "articles": ["K-IFRS 제1016호 문단 41"], "principle": "처분 시 재평가잉여금의 이익잉여금 대체", "case": {"holding": "토지", "no": None}},
            {"correct": False, "why": "자산이 사라졌으므로 장부금액이 폐쇄되고 이월 처리되는 것이 정당합니다.", "articles": [], "principle": "처분 시 재평가잉여금의 이익잉여금 대체", "case": {"holding": "토지", "no": None}},
            {"correct": False, "why": "국고보조금과는 전혀 성격이 다른 자본 적립금입니다.", "articles": [], "principle": "처분 시 재평가잉여금의 이익잉여금 대체", "case": {"holding": "토지", "no": None}},
            {"correct": False, "why": "자본 계정 대체일 뿐 자본의 재유입이 아닙니다.", "articles": [], "principle": "처분 시 재평가잉여금의 이익잉여금 대체", "case": {"holding": "토지", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "재평가잉여금(Revaluation surplus)의 성격 및 활용 방안에 관한 진술 중 K-IFRS와 상법의 기준에 저촉되는 오답은?",
        "options": [
            "① 재평가잉여금은 미실현 보유이익에 속하므로 주주에게 현금이나 현물로 배당할 수 없다.",
            "② 재평가잉여금을 무상증자 재원으로 사용하여 회사의 자본금으로 전입시키는 것은 법적으로 불가능하다.",
            "③ 재평가잉여금은 당기손익이 아닌 자본의 기타포괄손익누계액(OCI)에 보고된다.",
            "④ 재평가잉여금을 이익잉여금으로 직접 대체한 이후에는 상법상 배당가능이익 한도 내에 들어와 배당 재원이 될 수 있다.",
            "⑤ 재평가잉여금은 자산별로 개별 관리하며, 동일 유형자산의 손익끼리만 상계 처리한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 상의 재평가잉여금은 상법 및 관련 법규에 따라 무상증자(자본전입)의 재원으로 사용하는 것이 가능합니다. 따라서 자본금 전입이 불가능하다는 진술은 거짓입니다.\n\n[오답 해설]\n① 미실현 보유이익이므로 이사회나 주총에서 현금 배당을 결의하여 외부 유출할 수 없습니다.\n③ 자본의 OCI 누계액 소속이 맞습니다.\n④ 이익잉여금으로 직접 대체된 후에는 실현된 잉여금 성격을 가질 수 있어 상법상 배당 재원으로의 편입이 가능합니다.\n⑤ 자산 개별 단위로 장부를 추적하여 동일 자산의 잉여금 범위 내에서 상계해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "현금배당이 불가능하다는 진술은 상법상 정확한 규칙입니다.", "articles": [], "principle": "재평가잉여금의 법적 성격과 활용", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "재평가잉여금은 무상증자를 통해 자본금에 전입시키는 법적 허용 거래가 가능함에도 불가능하다고 하였으므로 오류입니다.", "articles": [], "principle": "재평가잉여금의 법적 성격과 활용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "OCI 자본 항목이 맞습니다.", "articles": ["K-IFRS 제1016호 문단 39"], "principle": "재평가잉여금의 법적 성격과 활용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익잉여금으로 대체된 후에는 법적으로 현금배당 등의 가능성이 열린다는 진술은 타당합니다.", "articles": [], "principle": "재평가잉여금의 법적 성격과 활용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "개별 자산별 추적 상계 원칙이 맞습니다.", "articles": [], "principle": "재평가잉여금의 법적 성격과 활용", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "유형자산 중 공정가치의 변동이 크지 않고 경미한 자산군(예: 공용 차량운반구, 일반 가구류)의 재평가모형 후속 주기 결정에 대한 K-IFRS 지침으로 타당한 것은?",
        "options": [
            "① 공정가치가 중요하게 요동치지 않더라도 법에 따라 반드시 매 분기 재평가해야 한다.",
            "② 매년 재평가할 필요는 없으며, 보통 3년이나 5년 주기로 재평가하는 것으로 충분하다.",
            "③ 주기적 평가 대상에서 완전 제외하여 원가모형으로 자동 고정시킨다.",
            "④ 20년마다 한 번씩 재평가 보고서를 작성한다.",
            "⑤ 공정가치가 취득원가의 2배를 넘을 때에만 일시 재평가한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 34에 따르면, 재평가자산의 공정가치가 장부금액과 중요하게 차이가 나지 않는다면 매 보고기간 말에 재평가할 필요는 없으며, 3년이나 5년 주기로 재평가하는 것으로 충분합니다. 단, 공정가치가 중요하고 불규칙하게 변동하는 경우에는 매년 재평가가 필요합니다.\n\n[오답 해설]\n① 경미한 변동의 자산까지 매 분기 및 매년 재평가를 강제하면 기업의 비용 부담이 지나쳐 부적절합니다.\n③ 재평가모형을 선택한 이상 장부와 공정가치 차이가 중요해지는 시점에는 평가해야 하므로 완전 제외는 오답입니다.\n④ 20년은 재무 정보의 적시성을 심각히 해치는 지나치게 긴 기간입니다.\n⑤ 취득가의 2배 한도 규칙은 기준서에 없습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "경미한 변동 시 매 보고기간 평가 강제설은 비용 대 편익 관점 및 규정에 부합하지 않습니다.", "articles": ["K-IFRS 제1016호 문단 34"], "principle": "공정가치 변동에 따른 평가 주기 결정", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "변동이 경미한 자산은 3~5년 정도의 주기로 재평가하는 것으로 족함을 명확히 서술했습니다.", "articles": ["K-IFRS 제1016호 문단 34"], "principle": "공정가치 변동에 따른 평가 주기 결정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자동 원가모형 회귀는 선택 정책 위배입니다.", "articles": [], "principle": "공정가치 변동에 따른 평가 주기 결정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "20년 주기설은 정보 유용성을 상실시킵니다.", "articles": [], "principle": "공정가치 변동에 따른 평가 주기 결정", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "원가 대비 2배 비율 규정은 존재하지 않는 오답입니다.", "articles": [], "principle": "공정가치 변동에 따른 평가 주기 결정", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "유형자산 재평가모형 하에서 '누계액제거법'을 적용하여 건물(감가상각대상자산)의 재평가 분개를 끊을 때, 재평가 조정일 직전에 수행하는 대변의 감가상각누계액을 털어내기 위해 사용하는 차변의 대칭 계정으로 옳은 것은?",
        "options": [
            "① (차변) 건물 (원가)",
            "② (차변) 이익잉여금",
            "③ (차변) 재평가이익",
            "④ (차변) 현금",
            "⑤ (차변) 복구충당부채"
        ],
        "answer": "1",
        "explanation": "① 누계액제거법 적용 시, 최초에 건물 취득원가와 상각누계액을 퉁치는 상쇄 분개를 처리합니다. 따라서 차변에 감가상각누계액을 두고 대변에 건물 원가계정을 두어 감누를 전액 털어냅니다. 즉 `(차) 감가상각누계액 XXX / (대) 건물 XXX` 분개가 수반되므로 차변 감누의 상대 대칭 계정은 '건물(자산원가)'입니다.\n\n[오답 해설]\n②, ③, ④, ⑤는 감가상각누계액 제거 시의 상쇄 분개 상대 계정이 아닙니다. 자산 총장부원가에서 제거하여 자산 순액만 남겨야 하기 때문에 본체 자산 계정(건물)이 와야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "차변에 상각누계액을 두고 대변에 자산(건물) 원가를 두어 누적된 상각액을 전액 상쇄 차감하므로 상대 대칭은 건물(원가)이 맞습니다.", "articles": ["K-IFRS 제1016호 문단 35"], "principle": "누계액제거법 분개 원리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "이익잉여금 직접 수정 분개가 아닙니다.", "articles": [], "principle": "누계액제거법 분개 원리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "재평가이익 손익이 상대 계정으로 오지 않습니다.", "articles": [], "principle": "누계액제거법 분개 원리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "비현금 거래이므로 현금이 유입될 수 없습니다.", "articles": [], "principle": "누계액제거법 분개 원리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "충당부채 상쇄는 무관한 분개입니다.", "articles": [], "principle": "누계액제거법 분개 원리", "case": {"holding": "건물", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "유형자산 재평가모형 하에서 감가상각누계액의 '비례수정법'을 사용하여 보고할 때, '누계액제거법'에 비하여 재무상태표의 정보 공시적 가치 측면에서 나타나는 주요 장점은?",
        "options": [
            "① 유형자산의 순장부금액이 훨씬 더 큰 가액으로 과대 계산된다.",
            "② 감가상각누계액의 역사적 누적 금액과 자산 총 원가(총 장부금액) 정보가 재무제표 본문에 상세히 보존되어 나타난다.",
            "③ 당기순이익이 항상 더 높게 창출된다.",
            "④ 법인세 신고 의무를 완전히 면제받게 된다.",
            "⑤ 회사의 자본금이 2배로 자동 무상 증자된다."
        ],
        "answer": "2",
        "explanation": "② 비례수정법을 적용하면 자산의 역사적 취득가(총 장부금액)와 감가상각누계액이 동일한 비율로 불어나기 때문에, 자산의 순가치인 공정가치를 보여주는 동시에 과거 취득 금액과 그동안의 누적 노후화 정보(상각누계액)가 제거되지 않고 그대로 살아있어 투자자에게 총액 정보를 더 유용하게 전달할 수 있습니다. 반면 누계액제거법은 기존 감누를 다 지워버려 순액만 남으므로 정보가 손실됩니다.\n\n[오답 해설]\n① 두 방법 모두 기말 순장부금액은 공정가치와 일치되도록 조정되므로 순장부금액 크기는 똑같습니다.\n③ 감가상각누계액 조정법의 차이가 당기순이익이나 상각비 크기에 영향을 미치진 않습니다.\n④, ⑤ 법인세 면제 및 자본금 무상 증자 등은 전혀 사실이 아닌 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "순장부금액은 공정가치로 두 방법 모두 일치하므로 가치 왜곡이 발생하지 않습니다.", "articles": [], "principle": "비례수정법의 정보 공시적 유용성", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "원가 총액 정보와 상각누계액 누적 가액이 장부상에 살아남아 공시되므로 총액 관점의 풍부한 정보를 보존하는 효과를 잘 지목했습니다.", "articles": ["K-IFRS 제1016호 문단 35"], "principle": "비례수정법의 정보 공시적 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손익 계산상 차이가 발생하지 않는 장부 조정 테크닉입니다.", "articles": [], "principle": "비례수정법의 정보 공시적 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법과 전혀 연계가 없는 보도입니다.", "articles": [], "principle": "비례수정법의 정보 공시적 유용성", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본금 직접 증자 효과는 무관합니다.", "articles": [], "principle": "비례수정법의 정보 공시적 유용성", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "유형자산 재평가모형 적용 시 발생하는 '재평가손실(당기순손익에 기재되는 평가손실)'이 회사의 최종 재무상태 및 당기 실적에 미치는 파급 영향에 대한 설명으로 가장 옳은 것은?",
        "options": [
            "① 자산 장부금액만 감소시킬 뿐, 당기순이익에는 전혀 영향을 주지 않는다.",
            "② 당기 비용으로 영업외비용 등에 합산되어 당기순이익을 직접 감소시키며, 이로 인해 궁극적으로 자본 총계(이익잉여금)를 감소시킨다.",
            "③ 기타포괄손익에 누적되므로 자기자본(OCI)만 깎고 순이익은 변함없다.",
            "④ 재평가손실은 부채로 계상되므로 자본 크기에는 변화가 없다.",
            "⑤ 회사의 매출총이익률을 향상시키는 긍정적 효과가 있다."
        ],
        "answer": "2",
        "explanation": "② 재평가손실은 당기비용으로 포괄손익계산서의 당기순손익에 바로 산입됩니다. 따라서 당기의 당기순이익을 직접적으로 갉아먹으며, 당기순이익은 연말 결산 분개를 거쳐 자본계정인 미처분이익잉여금을 줄이기 때문에 최종 자본 총액을 감소시킵니다.\n\n[오답 해설]\n① 당기순이익을 직접 깎기 때문에 영향이 없는 것이 아닙니다.\n③ OCI 차감으로 끝나는 것은 과거 적립된 재평가잉여금 범위 내일 때에 한합니다. 초과하는 재평가손실은 당기순이익(P&L) 영역입니다.\n④ 부채 계정이 아닙니다.\n⑤ 비용이 늘어나므로 순이익 관련 지표가 악화됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "순이익에 유의적인 영향을 주는 비용 항목이므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 40"], "principle": "재평가손실의 재무제표 파급 효과", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "당기비용(재평가손실)으로 귀속되어 당기순이익을 낮추고 궁극적으로 이익잉여금(자본)을 차감함을 정당하게 명시했습니다.", "articles": ["K-IFRS 제1016호 문단 40"], "principle": "재평가손실의 재무제표 파급 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과거 적립 잉여금 범위를 초과하는 평가 하락은 OCI가 아닌 당기순손익 차감입니다.", "articles": ["K-IFRS 제1016호 문단 40"], "principle": "재평가손실의 재무제표 파급 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채와 전혀 무관한 평가손실입니다.", "articles": [], "principle": "재평가손실의 재무제표 파급 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업실적 및 마진 지표가 나빠집니다.", "articles": [], "principle": "재평가손실의 재무제표 파급 효과", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "유형자산 처분 시 장부에 남아 있던 재평가잉여금을 이익잉여금으로 직접 대체하는 거래가 회사의 '총자본(자기자본 합계액)'에 미치는 영향은?",
        "options": [
            "① 이익잉여금이 추가 적립되므로 총자본이 즉각 증가한다.",
            "② 기타포괄손익누계액이 소멸하므로 총자본이 즉각 감소한다.",
            "③ 자본 계정(재평가잉여금)에서 다른 자본 계정(이익잉여금)으로 직접 이동하는 거래일 뿐이므로 총자본(자기자본) 합계액에는 어떠한 영향도 미치지 않는다.",
            "④ 이 대체로 인해 부채총계가 동일한 금액만큼 늘어난다.",
            "⑤ 대체 즉시 당기순이익이 증가하여 재무구조가 개조된다."
        ],
        "answer": "3",
        "explanation": "③ 재평가잉여금을 이익잉여금으로 대체하는 붕개는 `(차) 재평가잉여금(OCI누계) XXX / (대) 이익잉여금(자본) XXX` 입니다. 이는 자본 구성항목 내부간의 수평 이동에 불과하므로, 자본 내 분류명만 변경될 뿐 대주주 지분 전체인 '총자본(자기자본)' 합계금액은 불변(₩0 변동)입니다.\n\n[오답 해설]\n①, ② 자본 내 이동이므로 자본 총액 증감 주장은 오답입니다.\n④ 부채와 연결되지 않습니다.\n⑤ 당기순이익(처분손익)을 타지 않는 직접 대체 거래입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자본 증가 요인과 차감 요인이 동시에 자본 내에서 일어나므로 총액은 불변입니다.", "articles": [], "principle": "자본 내 대체 시 총자본에 미치는 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 감소를 유발하지 않고 내부 분류만 변경됩니다.", "articles": [], "principle": "자본 내 대체 시 총자본에 미치는 효과", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "기포누(OCI) 감소와 이잉 증가가 자본 내에서 상쇄되어 총자기자본 합계액은 변하지 않음을 바르게 이해했습니다.", "articles": ["K-IFRS 제1016호 문단 41"], "principle": "자본 내 대체 시 총자본에 미치는 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채와 연동되지 않는 순수 자본 분개입니다.", "articles": [], "principle": "자본 내 대체 시 총자본에 미치는 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "당기순이익을 거치지 않으므로 순이익 증가설은 오류입니다.", "articles": [], "principle": "자본 내 대체 시 총자본에 미치는 효과", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "임대수익이나 시세차익 목적으로 보유하는 부동산(투자부동산)의 공정가치모형과, 직접 영업에 사용하는 건물(유형자산)의 재평가모형에서 평가손익을 처리하는 K-IFRS 상의 결정적 차이는?",
        "options": [
            "① 투자부동산 평가손익은 기타포괄손익(OCI)으로 적립하고, 유형자산의 재평가이익은 당기순이익으로 처리한다.",
            "② 투자부동산의 공정가치평가손익은 전액 당기순손익(당기이익 또는 당기비용)으로 처리하는 반면, 유형자산의 재평가이익은 원칙적으로 기타포괄손익(OCI)으로 처리한다.",
            "③ 두 모형 모두 평가손익을 전액 이익잉여금으로 직접 가산하여 차이가 없다.",
            "④ 투자부동산 평가액은 부채로 계상하고 유형자산 평가액은 OCI로 계상한다.",
            "⑤ 투자부동산은 감가상각을 하면서 공정가치로 변경하지만 유형자산은 감가상각이 완전 배제된다."
        ],
        "answer": "2",
        "explanation": "② 투자부동산의 공정가치모형 하에서는 기말 평가에 따른 자산가액 변동손익 전체를 발생 즉시 당기손익(당기순손익)으로 잡으며 감가상각을 하지 않습니다. 반면 일반 유형자산의 재평가모형은 평가상승액을 원칙적으로 기타포괄손익(재평가잉여금)으로 기장하며 매기 감가상각을 반드시 거친 후에 재평가를 수행합니다.\n\n[오답 해설]\n① 처리 대상 손익 분류가 정반대로 기술되어 오답입니다.\n③, ④ 이익잉여금 직접 대체나 부채 계상설은 기준서와 맞지 않습니다.\n⑤ 투자부동산 공정가치모형은 감가상각을 하지 않으며 유형자산 재평가모형은 감가상각을 수행해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "두 자산의 손익 배분 기준을 거꾸로 배치하여 오답입니다.", "articles": [], "principle": "투자부동산 공정가치모형과 유형자산 재평가모형 비교", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "투자부동산 공정가치손익은 당기순손익(P&L)으로 가지만 유형자산 재평가이익은 기타포괄손익(OCI)으로 감을 정당하게 서술했습니다.", "articles": ["K-IFRS 제1040호 문단 35, K-IFRS 제1016호 문단 39"], "principle": "투자부동산 공정가치모형과 유형자산 재평가모형 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익잉여금 직접 기장은 허용되지 않는 처리입니다.", "articles": [], "principle": "투자부동산 공정가치모형과 유형자산 재평가모형 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채와 연동되지 않는 평가 거래입니다.", "articles": [], "principle": "투자부동산 공정가치모형과 유형자산 재평가모형 비교", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "투자부동산 공정가치모형은 감가상각을 중단하며 유형자산은 상각을 매년 해야 합니다.", "articles": [], "principle": "투자부동산 공정가치모형과 유형자산 재평가모형 비교", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s03-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "유형자산의 후속측정모형을 '원가모형'에서 '재평가모형'으로 변경하는 거래가 K-IFRS 상 지니는 회계적 성격 및 허용 요건으로 옳은 것은?",
        "options": [
            "① 단순 회계추정의 변경에 해당하므로 전진법을 쓴다.",
            "② 회계정책의 변경에 해당하며, 변경된 회계정책이 재무제표에 더 신뢰성 있고 목적적합한 정보를 제공할 때에만 허용한다.",
            "③ 단순 회계오류 수정이므로 전기 재무제표를 강제 소급 재작성해야 한다.",
            "④ 재무제표 작성 편의를 돕기 위해 특별한 제한 없이 언제든 매달 변경할 수 있다.",
            "⑤ 이 변경은 기타포괄손익 배분 단계에서 전액 무효화된다."
        ],
        "answer": "2",
        "explanation": "② 유형자산의 측정 모형(원가모형 vs 재평가모형)을 전환하는 것은 회계정책의 선택 변경입니다. K-IFRS 제1008호에 따라 정책의 변경은 변경을 통해 보고하는 정보가 거래등이 재무상태나 재무성과에 미치는 영향에 대하여 더 신뢰성 있고 목적적합한 정보를 제공하는 경우에 한하여 적법하게 인정됩니다. (단, 최초로 재평가모형으로 변경하는 경우에는 소급 적용하지 않고 전진적으로 적용하는 예외 규정이 있음)\n\n[오답 해설]\n① 상각 기간 수명 조절이 아닌 정책 변경이므로 추정변경이 아닙니다.\n③ 과거 오류에 기인한 강제 소급 재작성 대상이 아닙니다.\n④ 신뢰성 및 목적적합성 입증 요건 없이 임의로 전환하는 것은 금지됩니다.\n⑤ 기타포괄손익 배분단계와 관계없이 재평가모형 전환은 타당하게 인식됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "측정 방법론의 변경은 추정의 변경이 아니라 회계정책의 변경입니다.", "articles": ["K-IFRS 제1008호"], "principle": "후속측정 모형 변경의 회계적 성격", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "회계정책의 변경이며 목적적합하고 신뢰성 높은 정보 공시 요건을 요함을 정확히 지적했습니다.", "articles": ["K-IFRS 제1008호"], "principle": "후속측정 모형 변경의 회계적 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "오류수정이 아니므로 틀렸습니다.", "articles": [], "principle": "후속측정 모형 변경의 회계적 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정당한 사유 없는 임의적 변경은 엄격히 차단됩니다.", "articles": [], "principle": "후속측정 모형 변경의 회계적 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "변경 모형 적용 효과는 적법하게 기장되므로 오답입니다.", "articles": [], "principle": "후속측정 모형 변경의 회계적 성격", "case": {"holding": "", "no": None}}
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
                "item": "3절 유형자산의 후속측정"
            }
        }
    }
]

questions.extend(part1_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(part1_questions)} new questions (Part 1). Total questions in questions_db_accounting.json: {len(questions)}")
