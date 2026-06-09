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
    # L1: 기초 개념 (10문항, 1001~1010번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s02-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "유형자산의 최초 인식 이후 발생하는 '후속원가(Subsequent costs)'의 회계처리에 대한 K-IFRS의 기본적인 판정 요건으로 가장 올바른 것은?",
        "options": [
            "① 지출 금액의 크기가 전체 자산 구입비의 10%를 초과할 때에만 자본화한다.",
            "② 유형자산의 인식기준(미래경제적효익 유입가능성이 높고 원가를 신뢰성 있게 측정 가능)을 충족하면 자본적 지출로 보아 자산의 장부금액에 가산한다.",
            "③ 사후적인 지출은 성격과 관계없이 전액 발생 즉시 당기비용으로 처리한다.",
            "④ 내용연수를 연장하는 지출만 자본화하며, 생산력을 향상시키는 지출은 비용화한다.",
            "⑤ 후속 지출은 자산의 잔존가치를 증가시키므로 전액 자본잉여금으로 계상한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 12에 따르면, 후속원가가 유형자산의 자산인식 요건(미래경제적효익 유입가능성 높고 원가를 신뢰성 있게 측정 가능)을 충족하는 경우에만 유형자산의 장부금액에 포함하고, 그렇지 않으면 당기손익(비용)으로 인식합니다.\n\n[오답 해설]\n① 금액 비중(10% 등)은 기준서상 자산화 여부를 결정하는 절대적 기준이 아닙니다.\n③, ⑤ 지출의 경제적 실질에 따라 자본적 지출과 수익적 지출로 구분하므로 비용 또는 자본잉여금 일괄 인식설은 오답입니다.\n④ 생산력 향상 지출도 인식기준 충족 시 자본화 대상입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "금액 비중은 자산인식기준의 필수요건이 아닙니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "후속원가의 자산인식 기준", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "자산인식기준(효익 유입 및 측정 신뢰성) 충족 시 자산 장부금액에 가산한다는 기준서 원칙에 완벽히 부합합니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "후속원가의 자산인식 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산화가 가능한 자본적 지출이 존재하므로 일괄 비용설은 틀렸습니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "후속원가의 자산인식 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "생산력 향상도 미래경제적효익의 확대를 의미하므로 자본화가 가능합니다.", "articles": [], "principle": "후속원가의 자산인식 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본잉여금 계상은 회계처리에 어긋나는 오답입니다.", "articles": [], "principle": "후속원가의 자산인식 기준", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "유형자산의 작동을 보장하기 위한 일상적인 수선·유지(예: 기계 외관의 주기적인 도색, 엔진오일 교환 등) 지출에 대해 K-IFRS가 규정하는 올바른 회계처리 방법은?",
        "options": [
            "① 당해 유형자산의 장부금액에 포함시켜 자본화한다.",
            "② 해당 지출을 전액 판매비와관리비 또는 제조원가의 당기비용으로 발생 즉시 인식한다.",
            "③ 기타포괄손익(OCI)으로 기재하여 자본 조정을 수행한다.",
            "④ 미지급비용으로 적립하여 5년에 걸쳐 균등 상각비용으로 인식한다.",
            "⑤ 자산의 가액을 차감하는 차감적 대량수선충당부채로 보고한다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 12에 따르면, 유형자산의 일상적인 수선·유지와 관련하여 발생하는 원가는 자산의 장부금액에 포함하여 인식하지 않고 발생시점에 당기손익(비용)으로 인식합니다. 이러한 지출은 주로 '수선유지비' 등의 과목으로 비용 처리됩니다.\n\n[오답 해설]\n① 일상적 수선유지는 성능 개선이 아닌 현상 유지이므로 자산화(자본적 지출)를 금합니다.\n③, ④, ⑤는 임의적인 손익 연기 및 평가 계정 배정으로 기준서에 저촉되는 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "일상 수선은 자산가치 가산 대상이 아닙니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "일상적 수선유지비의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "수선 및 유지 목적 지출은 발생시점에 즉시 비용(당기손익) 처리함을 정당하게 명시했습니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "일상적 수선유지비의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기타포괄손익 분류 대상이 아닙니다.", "articles": [], "principle": "일상적 수선유지비의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지연 상각 처리는 인정되지 않는 자의적 처리입니다.", "articles": [], "principle": "일상적 수선유지비의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "충당부채 계상은 기준서와 무관한 진술입니다.", "articles": [], "principle": "일상적 수선유지비의 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "유형자산 자본적 지출의 결과로 기계장치의 내용연수나 잔존가치가 조정되었을 때, K-IFRS 상 감가상각비를 재계산하는 회계적 처리 방식의 성격은?",
        "options": [
            "① 회계정책의 변경에 해당하므로, 최초 취득 연도로 소급하여 재무제표를 재작성한다.",
            "② 회계오류의 수정에 해당하므로, 이익잉여금 조정을 통해 전기이월 금액을 고친다.",
            "③ 회계추정의 변경에 해당하므로, 지출이 발생한 회계기간부터 전진적으로(Prospective) 감가상각비를 조정한다.",
            "④ 자산 재평가모형의 강제 적용 사유이므로 당해 자산을 즉시 공정가치로 변경 기재한다.",
            "⑤ 이 변경은 회계장부에 기록할 필요가 없으며 단순 주석 공시로 대체한다."
        ],
        "answer": "3",
        "explanation": "③ 내용연수 및 잔존가치의 조정은 대표적인 '회계추정의 변경'에 해당하므로, K-IFRS 제1008호에 따라 소급법을 쓰지 않고 변경이 발생한 연도부터 미래 기간에 걸쳐 전진적으로 반영하여 상각비를 다시 산출합니다.\n\n[오답 해설]\n① 정책의 변경이 아니므로 소급하지 않습니다.\n② 적법한 거래 변경이므로 오류 수정이 아닙니다.\n④ 후속 원가 지출이 재평가모형 강제 전환을 의미하진 않습니다.\n⑤ 자본화 지출액 및 감가상각비의 회계처리는 재무제표 본문에 필수 기록되어야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "회계정책의 변경 및 소급재작성은 오답입니다.", "articles": ["K-IFRS 제1008호"], "principle": "후속 변경의 회계적 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "과거 기록의 오류가 아니므로 이익잉여금 수정 대상이 아닙니다.", "articles": ["K-IFRS 제1008호"], "principle": "후속 변경의 회계적 성격", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "내용연수/상각률의 변경은 추정의 변경이므로 전진법을 통해 변경 연도부터 다시 상각비를 인식함을 올바르게 지목했습니다.", "articles": ["K-IFRS 제1008호", "K-IFRS 제1016호 문단 51"], "principle": "후속 변경의 회계적 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "모형 전환의 의무 요건이 아닙니다.", "articles": [], "principle": "후속 변경의 회계적 성격", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재무제표 기장을 요하는 항목이므로 오답입니다.", "articles": [], "principle": "후속 변경의 회계적 성격", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "항공기의 엔진이나 용광로의 내화벽돌처럼 정기적으로 주요 부품을 대체 교체하는 거래에 대하여 K-IFRS 기준서가 선언하는 제거 규칙으로 가장 옳은 것은?",
        "options": [
            "① 교체된 새 부품의 원가는 비용화하고, 기존 구 부품의 장부금액을 계속 자산으로 둔다.",
            "② 새로운 부품을 취득하여 자산의 장부금액에 가산(자본화)하는 경우, 대체되어 떨어져 나가는 기존 구성요소의 장부금액은 무조건 장부에서 제거하고 당기손익(교체손실)으로 인식한다.",
            "③ 기존 구 부품의 장부금액은 기말에 감가상각으로만 소멸시킬 뿐 교체 시점에 별도로 제거하지 않는다.",
            "④ 교환된 부품은 비화폐성 교환이므로 교체손실 인식이 엄격히 제한된다.",
            "⑤ 감가상각이 완료되지 않은 부품은 물리적으로 교체하더라도 절대 자산에서 털어낼 수 없다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 13 및 문단 70에 따르면, 유형자산의 일부를 대체할 때 발생하는 원가를 자산 장부금액에 가산하여 인식하는 경우, 대체되는 기존 부분의 장부금액은 감가상각 완료 여부와 무관하게 장부에서 제거(Derecognition)하여 처분손실 등으로 처리해야 합니다.\n\n[오답 해설]\n① 신규 부품을 자산화하고 구형 부품을 비용 처리/제거해야 하므로 역방향 기술입니다.\n③, ⑤ 교체 시점에 반드시 제거 분개를 해 주어야 이중 계상을 막을 수 있습니다.\n④ 부품의 폐기 및 대체는 일반 처분거래의 일종이므로 손실 인식이 정당합니다."
    },
    {
        "id": "practice-accounting-ch04s02-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "유형자산 교체 부품의 장부금액을 제거할 때, 기존 구 부품의 취득원가나 감가상각누계액 등의 과거 장부금액 정보를 개별적으로 추적하여 파악하기 곤란한 경우 K-IFRS가 제시하는 대안적 추정 기준은?",
        "options": [
            "① 기존 구 부품의 장부금액을 무조건 '0'으로 간주하여 제거 처리를 생략한다.",
            "② 해당 유형자산 전체의 취득원가를 전액 제거하고 처음부터 다시 계산한다.",
            "③ 대체 시점에 지출한 신형 부품의 취득원가를, 당해 구형 부품이 취득/건설되었을 때의 원가로 갈음하여 기존 부분의 장부금액을 역산 추정한다.",
            "④ 정부 공시 시가표준액의 50%를 강제적으로 감액 처리한다.",
            "⑤ 해당 기계장치의 당기 손상차손 금액으로 일괄 대체 기재한다."
        ],
        "answer": "3",
        "explanation": "③ K-IFRS 제1016호 문단 70에 따르면, 대체되는 부품의 장부금액을 결정하기 어려운 경우, 새로운 대체 부품의 원가를 취득/건설 시점의 원가로 갈음하여(대용치로 써서) 기존 부품의 취득가 및 상각누계액을 합리적으로 역산해 제거할 수 있습니다.\n\n[오답 해설]\n① 제거 생략은 자산의 이중 중복 계상을 유발하므로 금지됩니다.\n② 자산 전체 제거는 실질에 맞지 않는 불필요한 행동입니다.\n④, ⑤는 기준서 조문과 관계없는 임의의 편의적인 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "제거 생략 시 이중계상 오류가 발생하므로 불가합니다.", "articles": ["K-IFRS 제1016호 문단 70"], "principle": "교체 부품 장부금액 추정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 전체를 지울 필요는 없으므로 과장된 오답입니다.", "articles": [], "principle": "교체 부품 장부금액 추정 기준", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "신규 부품 대체원가를 구 부품 취득 시 대용치로 활용해 기존 장부금액을 간접 유도해 지울 수 있도록 허용하는 조문을 바르게 서술했습니다.", "articles": ["K-IFRS 제1016호 문단 70"], "principle": "교체 부품 장부금액 추정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "시가표준액 50% 법은 규정에 없습니다.", "articles": [], "principle": "교체 부품 장부금액 추정 기준", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "손상차손 분류는 계정 과목 오류입니다.", "articles": [], "principle": "교체 부품 장부금액 추정 기준", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "항공기, 선박 등과 같이 계속 가동하기 위해 주기적으로 결함 진단 및 보수를 받아야 하는 '정기적인 종합검사(정밀검사)' 원가에 대한 K-IFRS의 올바른 최초 기장 지침은?",
        "options": [
            "① 종합검사는 물리적 자산의 증가가 없으므로 무조건 당기 판관비 수선비로 털어야 한다.",
            "② 종합검사 비용이 자산인식 기준을 충족하는 경우에는 유형자산의 일부가 대체되는 것으로 보아 관련 자산의 장부금액에 자본화한다.",
            "③ 종합검사비는 무조건 사후 복구충당부채의 환입 항목으로 대체한다.",
            "④ 검사 완료 후 3년간 무형자산 영업권으로 별도 계상하여 상각한다.",
            "⑤ 정기검사는 수익 창출과 무관한 법적 규제 준수 지출이므로 자산 가치가 전혀 인정되지 않는다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 14에 따라, 항공기 등 유형자산의 정기적인 종합검사 과정에서 발생하는 원가가 자산인식기준을 충족하는 경우, 유형자산의 일부가 대체되는 것으로 간주하여 그 원가를 유형자산의 장부금액에 포함시켜 자본화합니다.\n\n[오답 해설]\n① 물리적 증가가 없어도 가동을 위해 필수적인 지출인 종합검사는 자본화가 적법합니다.\n③ 충당부채 환입이 아닌 유형자산 가산 항목입니다.\n④ 무형자산 영업권이 아닌 해당 유형자산(예: 항공기)의 취득부대비용 계열 자본화 지출입니다.\n⑤ 법적 규제 준수를 위한 지출이라도 미래 효익 창출에 기여하므로 자산화됩니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자본화가 가능하므로 무조건 판관비 처리는 오답입니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "정기 종합검사원가의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "인식기준 충족 시 종합검사원가를 자산 일부의 대체로 보아 유형자산 원가에 산입함을 바르게 설명했습니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "정기 종합검사원가의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "복구충당부채 계정과 성격이 다릅니다.", "articles": [], "principle": "정기 종합검사원가의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "영업권 무형자산 분류는 회계기준 위반입니다.", "articles": [], "principle": "정기 종합검사원가의 회계처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 불인정 진술은 오답입니다.", "articles": [], "principle": "정기 종합검사원가의 회계처리", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "정기적인 종합검사 비용을 자본화하여 장부금액에 가산하는 경우, 이전에 수행했던 종합검사와 관련하여 장부에 미상각 잔액으로 남아 있던 과거 장부금액의 처리 원칙은?",
        "options": [
            "① 과거 검사 잔액은 별도로 건드리지 않고 만기까지 이중 상각되도록 나둔다.",
            "② 과거 종합검사의 미상각 잔존 장부금액은 즉시 장부에서 제거하고 당기손익(처분/제거손실)으로 인식하여야 한다.",
            "③ 과거 잔액은 전액 이익잉여금에 직접 가산하여 자본 보정한다.",
            "④ 새로운 종합검사 가격에서 과거 잔액을 차감한 순액만 자산에 얹는다.",
            "⑤ 과거 종합검사 잔액은 기계장치에 흡수되어 제거할 수 없으므로 무시한다."
        ],
        "answer": "2",
        "explanation": "② 정기 종합검사원가를 자산화할 때, 이전 검사에서 발생하여 자산에 얹혀 상각되고 남은 과거 미상각 종합검사 장부금액은 신규 검사원가 가산 시점에 장부에서 완전히 제거하여 제거손실로 당기 비용 처리하여야 합니다. \n\n[오답 해설]\n① 이중 상각 방치는 이중 계산 오류이므로 금지됩니다.\n③ 자본 직접 가산이 아닌 당기손익 항목입니다.\n④ 신규 검사비용 전체를 가산하고 과거 잔액은 분개상 제거하므로 순액 상쇄 자산화는 원칙적인 총액 분개법에 저촉됩니다.\n⑤ 추정해서라도 반드시 장부에서 지워내야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "이중 상각을 방치하는 것은 회계 오류입니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "직전 종합검사원가 잔액의 처리", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "새 검사액 자본화 시 직전 검사 관련 잔존 장부금액을 장부에서 즉각 털어내 손실 반영해야 함을 명확히 설명했습니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "직전 종합검사원가 잔액의 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자본 잉여금이나 이익잉여금 직접 수정 거래가 아닌 당기손익 거래입니다.", "articles": [], "principle": "직전 종합검사원가 잔액의 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순액법 대리 가산이 아닌 과거분 제거와 신규분 가산의 독립된 분개가 원칙입니다.", "articles": [], "principle": "직전 종합검사원가 잔액의 처리", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "제거 불가 무시 진술은 오답입니다.", "articles": [], "principle": "직전 종합검사원가 잔액의 처리", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "다음 중 성격 상 자산화(자본적 지출)를 할 수 없고 발생 즉시 판매비와관리비 또는 제조원가의 비용(수익적 지출)으로 회계처리하여야 하는 지출은?",
        "options": [
            "① 공장 옥상의 방수 누수 차단을 위한 경미한 실리콘 보수 및 도색 지출",
            "② 건물의 엘리베이터가 없어 추가로 신규 장착한 증설 공사 지출",
            "③ 냉난방 효율이 크게 개선되도록 유의적인 내부 보일러 배관 전체 시스템을 교체한 지출",
            "④ 기계장치의 엔진 피스톤을 개조하여 1일 생산 속도를 40% 증가시킨 개선 지출",
            "⑤ 선박의 연비를 15% 향상시키기 위해 특수 선체 코팅 부품을 장착한 지출"
        ],
        "answer": "1",
        "explanation": "① 경미한 실리콘 땜질 및 도색 작업은 자산의 효율을 최초 수준보다 향상시키는 활동이 아니라 현상 유지를 위한 일상 수선비에 가깝기 때문에 자본화할 수 없고 비용 처리(수익적 지출)해야 합니다.\n\n[오답 해설]\n②, ③, ④, ⑤는 모두 자산의 가치를 유의적으로 상승시키거나 성능 향상, 내용연수 증가 등에 해당하는 전형적인 자본적 지출 항목들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "경미한 땜질 및 페인트칠 등은 대표적인 현상유지용 수익적 지출(비용)에 속합니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "자본적지출과 수익적지출의 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "엘리베이터 증설은 자산 가치를 상승시키는 자본적 지출이 맞습니다.", "articles": [], "principle": "자본적지출과 수익적지출의 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "배관 전체 시스템 대체는 가치 증대 및 수명 연장을 가져오므로 자본화합니다.", "articles": [], "principle": "자본적지출과 수익적지출의 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기계 출력 속도 40% 증가 지출은 당연히 자본적 지출입니다.", "articles": [], "principle": "자본적지출과 수익적지출의 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "연비 향상 부품 장착도 미래 경제적 효익을 확대시키므로 자본화 대상입니다.", "articles": [], "principle": "자본적지출과 수익적지출의 식별", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "유형자산의 취득 완료 후에 지출된 자본적 지출(Capital expenditure)이 회사의 재무상태에 미치는 일반적인 영향에 대한 진술로 가장 올바른 것은?",
        "options": [
            "① 당기 자산총액이 즉시 감소한다.",
            "② 당기 비용이 증가하여 당기순이익이 크게 하락한다.",
            "③ 당기 비용으로 일시 처리한 것에 비하여 자산이 보존되어 자기자본(이익잉여금)이 과대하게 유지된다.",
            "④ 기말 유형자산의 취득원가는 변동이 없고 누계액만 감액된다.",
            "⑤ 부채비율이 일시적으로 급증하는 효과를 낳는다."
        ],
        "answer": "3",
        "explanation": "③ 자본적 지출은 비용이 아닌 자산으로 올라가므로, 발생 즉시 전액 비용 처리하는 수익적 지출에 비하여 당기 비용이 덜 잡혀 당기순이익이 크고, 이로 인해 자기자본(이익잉여금)과 자산총액이 더 높게 보고되는 결과를 가져옵니다.\n\n[오답 해설]\n① 자산에 포함되므로 자산총액은 감소하지 않고 유지/증가합니다.\n② 비용 처리가 지연(후속 감가상각으로 상각)되므로 당기 비용은 증가하지 않습니다.\n④ 유형자산의 최초 원가나 장부금액이 직접 늘어나게 됩니다.\n⑤ 자산화 지출 자체는 부채를 직접 늘리는 효과가 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산에 가산하므로 자산총액은 증가 또는 보존됩니다.", "articles": [], "principle": "자본적지출의 재무제표 파급 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비용화 대신 자산화되므로 당기 비용은 작아집니다.", "articles": [], "principle": "자본적지출의 재무제표 파급 영향", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "당기 비용이 즉각 잡히지 않고 자본화되어 자산과 이익 및 이익잉여금이 상대적으로 높게 유지됨을 정확히 묘사했습니다.", "articles": [], "principle": "자본적지출의 재무제표 파급 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 취득원가가 직접 증가하여 반영됩니다.", "articles": [], "principle": "자본적지출의 재무제표 파급 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채와 직결되는 항목이 아니므로 틀렸습니다.", "articles": [], "principle": "자본적지출의 재무제표 파급 영향", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "유형자산에 대한 정기적인 종합검사(정밀검사) 원가를 발생 시 당기 비용으로 털지 않고 자산으로 가산할 수 있게 허용하는 K-IFRS의 이론적 논거로 가장 합당한 것은?",
        "options": [
            "① 종합검사는 유형자산의 내부 구조를 전면적으로 교체하는 거래이기 때문이다.",
            "② 해당 검사를 수행하지 않으면 항공기나 선박을 법적 또는 안전적으로 가동하는 것 자체가 불가능하므로, 자산 가동 상태 유지에 필수불가결한 대체로 보기 때문이다.",
            "③ 종합검사를 통해 회사의 시장 지배적 무형가치가 보장되기 때문이다.",
            "④ 정부가 해당 종합검사비의 100%를 세액공제해 주기 때문이다.",
            "⑤ 정기검사는 일반 수선비와 회계적 성격이 완전히 동일하기 때문이다."
        ],
        "answer": "2",
        "explanation": "② 정기적인 종합검사비용의 자산화 근거는, 당해 검사가 자산을 계속적으로 사용·가동하기 위해 피할 수 없는 필수적 요건이므로 유형자산의 장기적인 효익 유입을 위해 부품 대체와 다름없는 실질을 가지기 때문입니다.\n\n[오답 해설]\n① 종합검사라고 하여 반드시 모든 내부 구조를 전면 교체하는 것은 아닙니다.\n③ 무형가치가 아닌 유형자산 가동 유지와 직결됩니다.\n④ 세법상 지원 여부는 회계상의 자산 요건 충족 논거와 무관합니다.\n⑤ 일반 수선비와 성격이 달라서 자본화가 되므로 동질성 설명은 오류입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "전면 구조 교체를 뜻하진 않으므로 오답입니다.", "articles": [], "principle": "종합검사 자본화의 이론적 근거", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "종합검사를 거치지 않으면 자산의 지속 가동이 차단되므로, 가동을 가능하게 하는 유의적 부품 대체와 실질이 같아 자본화함을 바르게 진술했습니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "종합검사 자본화의 이론적 근거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무형가치 보장 및 영업권과는 무관합니다.", "articles": [], "principle": "종합검사 자본화의 이론적 근거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "세법 규정은 자산 자본화의 회계적 논거가 아닙니다.", "articles": [], "principle": "종합검사 자본화의 이론적 근거", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일반 수선비는 즉시 비용이므로 종합검사비와 회계적 대우가 다릅니다.", "articles": [], "principle": "종합검사 자본화의 이론적 근거", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },

    # =========================================================================
    # L2: 개념 이해 및 기준 조문 (15문항, 1011~1025번)
    # =========================================================================
    {
        "id": "practice-accounting-ch04s02-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "유형자산의 수익적 지출(Revenue expenditure, 예: 공장 유리창 교체, 도색비)에 대한 손익보고서 상 계정 분류 지침으로 가장 옳은 것은?",
        "options": [
            "① 공장 생산 설비와 직접 관련된 수익적 지출은 제조원가(FOH)에 배부하고, 본사 관리용 자산과 관련된 지출은 판매비와관리비(수선비 등)로 당기비용화한다.",
            "② 모든 수익적 지출은 자산의 수리를 뜻하므로 예외 없이 영업외비용으로 기재한다.",
            "③ 수익적 지출은 전액 당기 매출액에서 직접 차감하여 표시하여야 한다.",
            "④ 본사 빌딩에 대한 도색 지출은 제품 매출원가로 직접 산입하여 관리한다.",
            "⑤ 수익적 지출로 발생한 비용은 당기말 기말재고자산 원가에서 전액 공제 차감한다."
        ],
        "answer": "1",
        "explanation": "① 수익적 지출은 자산이 사용되는 부서의 성격에 따라 비용을 귀속시킵니다. 공장 기계 및 생산 설비 수선비는 당기 제조원가로 가고 본사 지원 및 영업 부서의 수선비는 당기 판매비와관리비로 비용 기재됩니다.\n\n[오답 해설]\n② 영업 활동과 직접 관련된 자산 수선은 영업비용(판관비 또는 매출원가)이며 영업외비용이 아닙니다.\n③ 매출 직접 차감은 분개 오류입니다.\n④ 본사 빌딩은 판매비와관리비 항목이지 공장 제조원가 대상이 아닙니다.\n⑤ 재고자산에서 직접 차감하지 않습니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "수익적 지출의 비용화 시 사용처에 따라 제조원가와 판관비로 체계적으로 배분하는 것이 올바름을 명시했습니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "수익적지출의 손익계산서 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "정상적 영업활동 관련 수선은 판관비나 제조원가(영업비용)에 들어갑니다.", "articles": [], "principle": "수익적지출의 손익계산서 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "매출 차감 방식은 틀린 설명입니다.", "articles": [], "principle": "수익적지출의 손익계산서 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "본사 빌딩 관련 수선비는 제조 부문원가에 해당하지 않으므로 오답입니다.", "articles": [], "principle": "수익적지출의 손익계산서 귀속", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기말 재고자산 차감설은 부적정합니다.", "articles": [], "principle": "수익적지출의 손익계산서 귀속", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "부품 대체 시, 기존 부품의 미상각 잔액을 장부에서 제거하여 발생한 '구성요소 대체손실(Derecognition loss)'의 당기 손익계산서 상 계정 과목 및 성격으로 가장 타당한 것은?",
        "options": [
            "① 영업외비용에 속하는 유형자산처분손실(또는 제거손실)로 기재한다.",
            "② 무형자산손상차손 계정을 사용하여 판매비와관리비로 기재한다.",
            "③ 대손상각비 과목으로 영업비용에 직접 가산한다.",
            "④ 기타포괄손익에 누적한 후 자산 매각 시점에 자본이입한다.",
            "⑤ 감가상각비 계정에 전액 포함시켜 매출원가에 합산 보고한다."
        ],
        "answer": "1",
        "explanation": "① 교체에 따라 기존 구형 구성요소를 제거하며 인식하는 차액 손실은 유형자산 처분 및 제거 거래에서 도출되는 손실이므로 영업외비용 계열의 '유형자산처분손실'(또는 유형자산폐기손실, 유형자산제거손실)로 계상합니다.\n\n[오답 해설]\n② 무형자산이 아니며 손상 징후에 의한 손상차손과 성격이 다릅니다.\n③ 대손상각비는 채권 회수 불능 시 쓰는 계정입니다.\n④ 자본 직접 적립(기타포괄손익) 거래가 아닌 당기 당기비용 인식 거래입니다.\n⑤ 일반적인 기간 배분 감가상각비와 분리 기입해야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "대체 제거 시의 차액은 유형자산의 제거로 인한 처분손실 계정(영업외비용)으로 보고하여야 함을 바르게 기술했습니다.", "articles": ["K-IFRS 제1016호 문단 67, 68"], "principle": "부품 대체제거손실의 계정 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무형자산 계정 사용은 틀린 설명입니다.", "articles": [], "principle": "부품 대체제거손실의 계정 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "대손상각비는 수취채권 평가 계정이므로 불가합니다.", "articles": [], "principle": "부품 대체제거손실의 계정 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "기타포괄손익이 아닌 당기손익 항목입니다.", "articles": [], "principle": "부품 대체제거손실의 계정 분류", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일반 감가상각비용에 묻어서 보고하지 않습니다.", "articles": [], "principle": "부품 대체제거손실의 계정 분류", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "K-IFRS 제1016호에 명시된, 유형자산의 정기적인 종합검사 원가의 제거 기준에 대한 설명 중 정오 판단으로 가장 옳은 것은?",
        "options": [
            "① 새로운 종합검사를 진행하더라도 과거의 미상각 종합검사 원가는 다음 감가상각 주기까지는 제거가 전면 보류된다.",
            "② 이전 종합검사 시 발생하여 유형자산 장부금액에 가산되었던 잔액 중 남아 있는 미상각 장부금액은 물리적으로 교체된 부품이 없더라도 전액 제거하여 손실 처리한다.",
            "③ 과거 종합검사 장부금액은 기계 본체에 영구 귀속되므로 법적으로 제거하는 것이 원천 차단되어 있다.",
            "④ 새로운 검사를 자산화하지 못할 때에만 한하여 전기 검사 잔액을 제거한다.",
            "⑤ 과거 종합검사 잔액은 기말 재평가 시점에만 일괄 차감하며 평상 시 제거는 불가하다."
        ],
        "answer": "2",
        "explanation": "② 정기 종합검사는 비물리적이지만 자본화된 독립 상각 요소로 다루어집니다. 따라서 새로운 종합검사를 거쳐 원가를 자산에 새로 올릴 때에는, 과거 검사와 관련해 자산에 가산되어 감가상각되고 남아있던 잔액은 물리적 실체가 없더라도 자산에서 털어내 손실로 반영해야 합니다.\n\n[오답 해설]\n①, ③, ⑤ 제거 보류나 제거 차단 등은 이중 자본화 오류를 방조하므로 오답입니다.\n④ 새로운 검사가 자산화요건을 충족하여 가산되는 시점에 기존 잔액을 털어내야 합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "즉시 제거를 통해 중복 인식을 차단해야 하므로 틀렸습니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "종합검사 잔액 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "비물리적인 종합검사 장부가액도 신형 검사 자본화 시점에는 기존 잔액을 확실히 장부 제거하여 털어야 한다는 기준서 규정에 정확히 부합합니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "종합검사 잔액 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "검사 잔액은 별도 분리 상각이 가능한 단위를 형성하므로 제거 가능합니다.", "articles": [], "principle": "종합검사 잔액 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "새로운 검사가 자산화될 때 기존 분이 지워져야 하므로 전제가 어긋났습니다.", "articles": [], "principle": "종합검사 잔액 제거 요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재평가 시점이 아닌 후속 종합검사 수행 시점에 즉각 털어냅니다.", "articles": [], "principle": "종합검사 잔액 제거 요건", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "유형자산의 자본적 지출이 기중에 수행되어 기계장치의 내용연수 연장 등이 이루어졌을 때, 기중 감가상각비 계산의 적용 시점에 대한 K-IFRS 및 일반적인 실무 지침으로 가장 올바른 설명은?",
        "options": [
            "① 해당 회계연도 전체를 소급하여 최초 취득년도 이자율로 균등 조율한다.",
            "② 지출이 발생한 시점까지는 기존 상각 기준에 의거하여 감가상각비를 일할/월할 상각하고, 지출 시점 이후부터는 새로운 장부금액 및 조정된 잔여내용연수를 기초로 감가상각비를 월할 계산한다.",
            "③ 기중에 지출이 발생하더라도 무조건 지출 연도 1월 1일에 지출한 것으로 의제하여 연초부터 전진 적용한다.",
            "④ 기중 자본적 지출 시 당해 연도는 감가상각을 전면 면제하고 다음 연도 초부터 1년 치를 소급한다.",
            "⑤ 지출 시점과 무관하게 취득 시의 최초 상각 스케줄을 변경하는 것은 절대 불가하다."
        ],
        "answer": "2",
        "explanation": "② 기중에 자본적 지출이 발생한 경우, 지출 전까지는 기존 상각 조건으로 상각비를 인식하고, 지출 시점부터는 [직전 장부가 + 지출액]을 기초로 하여 새로운 내용연수를 전진 적용하여 감가상각비를 월할 안분 계산하는 것이 실무적으로 타당합니다.\n\n[오답 해설]\n① 최초 취득일로의 소급 처리는 회계추정 변경 성격(전진법)에 위배됩니다.\n③, ④, ⑤는 기중 발생 사건의 회계적 성격을 왜곡하거나 임의로 지연시키는 잘못된 진술입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "소급 처리는 회계추정 변경 원칙에 어긋납니다.", "articles": [], "principle": "기중 자본적지출 시 상각 적용 기간", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "지출 시점을 기준으로 전기와 후기를 쪼개어 각각의 상각 공식 및 내용연수 상각률을 적용해 월할 상각하는 적법한 실무를 명시했습니다.", "articles": ["K-IFRS 제1016호 문단 51"], "principle": "기중 자본적지출 시 상각 적용 기간", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "연초 의제 처리는 정확한 월할 배분 원칙에 위배됩니다.", "articles": [], "principle": "기중 자본적지출 시 상각 적용 기간", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각 면제 및 다음 연도 이월은 부당한 비용 인식 이연입니다.", "articles": [], "principle": "기중 자본적지출 시 상각 적용 기간", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각 기준 변경이 가능하므로 고정 불가설은 오답입니다.", "articles": [], "principle": "기중 자본적지출 시 상각 적용 기간", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "자본적 지출에 해당하는 대대적인 부품 교체 지출을 수익적 지출(수선비 비용)로 오인하여 잘못 분개한 오류가 '지출 1차 연도'의 감가상각비와 당기순이익에 미치는 파장으로 옳은 것은?",
        "options": [
            "① 감가상각비는 과대계상되고 당기순이익은 과소계상된다.",
            "② 감가상각비는 과소계상되고 당기순이익은 과대계상된다.",
            "③ 감가상각비는 과소계상되고 당기순이익도 과소계상된다.",
            "④ 감가상각비와 당기순이익 모두 과대계상된다.",
            "⑤ 회사의 재무제표 손익에는 아무런 차이가 발생하지 않는다."
        ],
        "answer": "3",
        "explanation": "③ 자본적 지출을 즉시 비용 처리(수익적 지출화)하면 다음과 같은 결과가 나타납니다.\n1. 당해 지출액이 자산에 더해지지 않았으므로 감가상각비 계산의 모수가 되는 장부금액이 작아져 당기 감가상각비는 과소계상(비용 과소)됩니다.\n2. 한편, 지출액 전액이 즉시 비용(수선비)으로 인식되었으므로, 적정 감가상각비로 서서히 비용화되어야 할 금액보다 과도한 비용이 당기에 일시 보고되었습니다.\n3. 이에 따라 비용 총액(수선비 과대계상액 > 감가상각비 과소계상액)이 커져 당기순이익은 과소계상됩니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 비용 누락 및 일시 비용 인식에 따른 순이익 왜곡 배율을 잘못 설정한 오답입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산화가 누락되어 상각 대상 원가가 작아지므로 감가상각비는 과소계상되어야 합니다.", "articles": [], "principle": "자본적지출을 수익적지출로 오인한 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지출액 전체가 비용으로 먼저 인식되므로 당기순이익은 과소가 맞습니다.", "articles": [], "principle": "자본적지출을 수익적지출로 오인한 효과", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "감가상각 모수 축소로 상각비용은 과소해지고 지출액 즉시 비용화로 전체 비용이 크게 늘어 순이익은 과소해짐을 정확히 판정했습니다.", "articles": [], "principle": "자본적지출을 수익적지출로 오인한 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "양자 과대 진술은 논리 모순입니다.", "articles": [], "principle": "자본적지출을 수익적지출로 오인한 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "비용 인식 시점이 전면 달라지므로 손익 수치가 달라집니다.", "articles": [], "principle": "자본적지출을 수익적지출로 오인한 효과", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "유형자산 구성요소 중 용광로의 내화벽돌 대체와 같이 물리적 교체가 확실한 부품에 대한 K-IFRS 회계처리 기준의 요구사항으로 가장 옳지 않은 것은?",
        "options": [
            "① 해당 기계 전체의 장부금액에 교체 벽돌의 구입원가를 가산한다.",
            "② 대체되는 기존 내화벽돌의 남아 있는 장부금액을 제거하여 제거손익을 잡는다.",
            "③ 벽돌 교체 지출은 단순 수익적 지출이므로 자산화가 원천 금지되며 수선비 처리만 인정된다.",
            "④ 대체되는 부분의 감가상각누계액이 개별 계상되어 있지 않더라도 합리적 배분비율을 추정해 털어낸다.",
            "⑤ 기존 부품의 미상각 잔액이 남아 있다면 이를 비용 처리하여 중복 계상을 방지한다."
        ],
        "answer": "3",
        "explanation": "③ 용광로의 내화벽돌 교체는 자산의 수명을 실질적으로 연장하거나 정상 작동을 위해 필수적인 유의적 부품의 대체 거래이므로, 인식기준 충족 시 자본적 지출로 처리하여 자산화할 수 있습니다. 전면 금지 서술은 명백한 오류입니다.\n\n[오답 해설]\n①, ②, ④, ⑤는 K-IFRS 제1016호 문단 13 및 문단 70에 규정된 구성요소 대체 회계처리의 적법한 요구사항들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "자산 일부의 대체이므로 전체 장부에 가산하는 것이 맞습니다.", "articles": ["K-IFRS 제1016호 문단 13"], "principle": "물리적 구성요소의 대체 처리 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "구 벽돌의 미상각분 제거 및 손실 처리는 필수 의무입니다.", "articles": ["K-IFRS 제1016호 문단 13"], "principle": "물리적 구성요소의 대체 처리 정오", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "식별 가능한 구성요소 부품의 대체 지출은 자본화가 적법하게 인정되므로 전면 금지 및 비용설을 오답으로 잘 식별했습니다.", "articles": ["K-IFRS 제1016호 문단 13"], "principle": "물리적 구성요소의 대체 처리 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "상각누계액의 합리적 추정을 통한 털기가 가능하므로 조문에 맞습니다.", "articles": ["K-IFRS 제1016호 문단 70"], "principle": "물리적 구성요소의 대체 처리 정오", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이중 계상 방지를 위한 비용 털기 원칙에 부합합니다.", "articles": [], "principle": "물리적 구성요소의 대체 처리 정오", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "K-IFRS 제1016호에 근거한 유형자산 후속 원가의 자산 요건 충족 판정을 위한 두 가지 대원칙적 질문으로 가장 적절하게 짝지어진 것은?",
        "options": [
            "① (1) 지출의 외화 환산 가능성 (2) 국가 정책적 보조금 해당 여부",
            "② (1) 지출로 인한 미래경제적효익의 유입가능성이 높은가? (2) 지출원가를 신뢰성 있게 측정할 수 있는가?",
            "③ (1) 지출 상대방의 공신력 (2) 지출 대금 결제 수단의 현금성 유무",
            "④ (1) 기말 재평가 결과 공정가치 상승 여부 (2) 차입원가 자본화 요건 충족 여부",
            "⑤ (1) 감가상각 자산 총액의 변동 유무 (2) 처분손익 누적액의 크기"
        ],
        "answer": "2",
        "explanation": "② 유형자산의 후속원가 자산화(자본적 지출 판정) 기준은 최초 인식요건(미래경제적효익 유입가능성 및 원가 측정 신뢰성)을 그대로 준용합니다.\n\n[오답 해설]\n①, ③, ④, ⑤는 최초 인식 및 자산 판단 대원칙과 거리가 먼 지엽적이고 무관한 설명들입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "국가 보조금이나 외화 환산은 요건이 아닙니다.", "articles": ["K-IFRS 제1016호 문단 7"], "principle": "후속원가 자산화의 2대 판정요건", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "유형자산 일반 인식요건인 미래 효익 유입가능성 및 신뢰성 있는 측정이 그대로 쓰임을 바르게 지목했습니다.", "articles": ["K-IFRS 제1016호 문단 7, 12"], "principle": "후속원가 자산화의 2대 판정요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "지출 상대방 및 수단은 회계 인식 요건이 아닙니다.", "articles": [], "principle": "후속원가 자산화의 2대 판정요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "재평가 유무 및 차입원가는 최초 자본화의 필수 대원칙이 아닙니다.", "articles": [], "principle": "후속원가 자산화의 2대 판정요건", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "처분손익 규모 등은 판단 기준이 아니므로 오답입니다.", "articles": [], "principle": "후속원가 자산화의 2대 판정요건", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "회사가 수익적 지출(예: 건물 청소비, 경미한 누수 보수비) ₩50,000을 장부에 비용으로 기재하지 않고 전액 누락 누설한 회계 오류가 당기말 재무제표 수치에 미치는 손익 파장 분석으로 옳은 것은?",
        "options": [
            "① 당기순이익이 ₩50,000 과대계상된다.",
            "② 당기순이익이 ₩50,000 과소계상된다.",
            "③ 기말 자산총액이 ₩50,000 과소계상된다.",
            "④ 기말 부채비율이 ₩50,000 증가한다.",
            "⑤ 자본잉여금이 ₩50,000 과소계상된다."
        ],
        "answer": "1",
        "explanation": "① 수익적 지출 ₩50,000은 당기에 비용 처리되어야 하는 항목입니다. 이 비용 인식을 누락하였으므로, 당기 비용이 ₩50,000 만큼 덜 잡혀서 당기순이익은 ₩50,000 만큼 과대계상(이익 부풀림) 효과를 보게 됩니다.\n\n[오답 해설]\n② 비용 미인식으로 이익은 늘어나므로 과소계상은 오답입니다.\n③ 수익적 지출은 애초에 자산 기입 계정이 아니므로 자산총액 과소 효과는 무관합니다.\n④, ⑤ 부채 및 자본잉여금 과목과는 직접 연결되지 않는 손익 오류입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "당기 비용으로 빠졌어야 할 지출을 누락했으므로 비용 총계 감소에 따른 당기순이익 ₩50,000 과대계상을 올바르게 유도했습니다.", "articles": [], "principle": "수익적지출 누락 오류의 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익이 과소 계상된다는 진술은 반대이므로 오답입니다.", "articles": [], "principle": "수익적지출 누락 오류의 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "자산 계상 대상이 아니므로 자산총액에 영향을 주지 않습니다.", "articles": [], "principle": "수익적지출 누락 오류의 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "부채 항목의 변동이 아니므로 오답입니다.", "articles": [], "principle": "수익적지출 누락 오류의 영향", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이익잉여금(자본)이 과대해지며 자본잉여금과는 관련이 적습니다.", "articles": [], "principle": "수익적지출 누락 오류의 영향", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "다음 중 K-IFRS 기준 상 정기적인 종합검사(정밀검사) 비용을 자산화하여 유형자산 원가에 산입할 수 있는 업종 및 주요 자산의 대표적 사례가 아닌 것은?",
        "options": [
            "① 항공 운송업을 영위하는 항공사의 대형 여객기 동체 및 결함 검사비",
            "② 해운 수송업을 영위하는 선박 회사의 거대 원유 운반선 도크(dock) 정밀 안전 검사비",
            "③ 정밀 화학 물질을 대량 제조하는 화학 공장의 핵심 반응로 내부 기밀성 종합 안전 검사비",
            "④ 금융업을 영위하는 시중 은행의 금고 자물쇠 기능 수리 및 정기 윤활 도색비",
            "⑤ 정기적인 궤도 진단 및 전면 보수가 요구되는 철도 회사의 열차 선로 종합 검사비"
        ],
        "answer": "4",
        "explanation": "④ 시중 은행 금고의 자물쇠 정기 윤활 및 도색 지출은 자산 가동에 필수적인 종합적인 정밀 안전성 진단 검사라기보다는 일상적인 수선·유지에 속하는 경미한 지출이므로 즉시 비용화(수익적 지출)하여야 합니다. \n\n[오답 해설]\n①, ②, ③, ⑤는 검사를 거치지 않고 가동할 경우 대형 사고를 유발하거나 법적으로 운항이 전면 불허되는 대표적인 거대 자산들로서, 정기 종합검사비의 자산화 요건에 완벽히 부합합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "여객기 종합 검사비는 자산화가 허용되는 대표적 항목입니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "종합검사원가 적용 자산사례", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "운반선 정밀 안전 검사비 역시 자본화 대상 종합검사비입니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "종합검사원가 적용 자산사례", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "핵심 화학 반응로 검사비도 자본화 요건에 부합합니다.", "articles": [], "principle": "종합검사원가 적용 자산사례", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "단순 금고 윤활 및 보색은 가동에 필수적인 종합 결함 검사로 보기 어려운 수익적 지출의 전형임을 바르게 판정했습니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "종합검사원가 적용 자산사례", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "선로 종합 검사비도 철도 가동을 위한 자본화 가능 종합검사 대상입니다.", "articles": [], "principle": "종합검사원가 적용 자산사례", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "본사 빌딩 건물에 엘리베이터(승강기) 장치를 새롭게 설계하여 최초로 증설하는 데 지출된 ₩100,000의 회계처리에 대해 K-IFRS 기준을 적용한 설명으로 가장 올바른 것은?",
        "options": [
            "① 엘리베이터는 건물의 물리적 외벽이 아니므로 즉시 영업외비용으로 일시 상각한다.",
            "② 빌딩 가치의 증대 및 미래 효익을 창출하므로 자본적 지출로 보아 건물의 취득원가에 포함(자본화)한다.",
            "③ 임시 자산이므로 무형자산 영업권으로 계상해 별도 상각한다.",
            "④ 건물의 장부금액과는 별개로 무조건 '기계장치'라는 유동자산 과목으로 독립 보고한다.",
            "⑤ 이 지출로 인한 부채 변경 효과를 자본잉여금 감액 항목에 직접 뺀다."
        ],
        "answer": "2",
        "explanation": "② 기존 건물에 엘리베이터를 새로 설치하는 것은 건물의 내용연수를 연장시키거나 가치를 실질적으로 증가시키는 자본적 지출에 해당하므로 건물의 취득원가에 가산하여 내용연수 동안 함께 감가상각하여야 합니다.\n\n[오답 해설]\n① 자본화가 적법하므로 즉시 영업외비용 처리는 오답입니다.\n③ 무형자산 영업권으로 갈 수 없습니다.\n④ 유형자산(건물 부속 설비)에 합산하여 상각하는 것이 원칙이며 유동자산이 될 수 없습니다.\n⑤ 자본잉여금 감액과는 무관합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "비용화 처리가 아니므로 오답입니다.", "articles": [], "principle": "건물 엘리베이터 증설의 자산화", "case": {"holding": "건물", "no": None}},
            {"correct": True, "why": "효익 유입가능성이 확실한 자본적 지출이므로 건물의 장부금액에 가산하여 자본화함을 정확히 설명했습니다.", "articles": [], "principle": "건물 엘리베이터 증설의 자산화", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "영업권 분류는 부적절합니다.", "articles": [], "principle": "건물 엘리베이터 증설의 자산화", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "유동자산 분류설은 오답입니다.", "articles": [], "principle": "건물 엘리베이터 증설의 자산화", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "자본잉여금 차감 거래가 아닙니다.", "articles": [], "principle": "건물 엘리베이터 증설의 자산화", "case": {"holding": "건물", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "유형자산의 일부 부품을 교체하면서 새 부품 가격은 장부에 가산(자본화)하고서, 기존 구형 부품의 미상각 잔액을 장부에서 지워내는 제거 분개 처리를 누락한 경우, 당기말 재무제표상 유형자산 장부금액에 미치는 직접적 오류 효과는?",
        "options": [
            "① 유형자산의 장부금액이 과소계상된다.",
            "② 유형자산의 장부금액이 이중 중복 계상되어 과대계상된다.",
            "③ 유형자산의 총액에는 아무런 영향이 없다.",
            "④ 감가상각누계액만 인위적으로 과대해진다.",
            "⑤ 해당 기계장치의 취득원가는 감소하고 충당부채만 늘어난다."
        ],
        "answer": "2",
        "explanation": "② 부품 교환 시 구형 부품의 장부금액을 장부에서 제거하지 않으면, 새로운 부품의 가치(자본화액)와 과거 구형 부품의 남아있던 가치가 동시에 자산에 얹혀 있게 되므로, 자산의 가치가 중복 기록되어 유형자산 장부금액이 과대계상되는 직접적인 회계 오류가 발생합니다.\n\n[오답 해설]\n① 지워져야 할 부분이 안 지워졌으므로 과대계상이 맞고 과소계상은 틀립니다.\n③ 중복 쏠림 현상으로 자산 총액이 비정상적으로 팽창합니다.\n④, ⑤는 이 분개 누락에 따른 자산의 올바른 왜곡 진술이 아닙니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "제거 누락으로 자산이 부풀어 오르므로 과소계상은 틀렸습니다.", "articles": ["K-IFRS 제1016호 문단 70"], "principle": "부품교체 시 제거누락의 효과", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "신구 부품 가치가 하나의 장부에 동시에 기입되어 유형자산 장부금액이 과대하게 표기됨을 잘 지적했습니다.", "articles": ["K-IFRS 제1016호 문단 70"], "principle": "부품교체 시 제거누락의 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "이중 계상으로 자산 총액이 왜곡되므로 영향이 없다는 말은 오답입니다.", "articles": [], "principle": "부품교체 시 제거누락의 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "누계액만의 왜곡이 아니므로 틀렸습니다.", "articles": [], "principle": "부품교체 시 제거누락의 효과", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "충당부채 증가 거래와 직결되지 않습니다.", "articles": [], "principle": "부품교체 시 제거누락의 효과", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "유형자산의 후속적인 상황 변동(예: 자산 노후화 가속 등)으로 인하여 기존 내용연수를 단축하기로 결정한 회계추정 변경의 올바른 적용에 대한 설명 중 가장 타당한 것은?",
        "options": [
            "① 단축 결정이 내려진 당해 연도 초부터 변경된 짧은 잔여내용연수를 적용하여 미래 감가상각비를 전진 계산한다.",
            "② 최초 취득 시점까지 소급하여 과거 보고된 모든 상각비를 일괄 증액 수정한다.",
            "③ 내용연수를 단축하더라도 감가상각 누계 잔액은 변경 전 기준대로 강제 완공 상각한다.",
            "④ 이 변경은 손상차손과 동일하므로 무조건 전액 영업외비용으로 당기 일시 제거 분개한다.",
            "⑤ 내용연수 단축은 감가상각방법의 변경이므로 소급법을 의무 적용한다."
        ],
        "answer": "1",
        "explanation": "① 내용연수의 단축은 전형적인 회계추정의 변경 사항입니다. K-IFRS 기준 상 추정 변경이 있는 해의 연초(또는 변경 시점)부터 변경된 잔여내용연수를 분모로 두어 전진법을 통해 감가상각비를 다시 산정합니다.\n\n[오답 해설]\n②, ⑤ 회계추정의 변경은 절대 소급 적용하지 않습니다.\n③ 변경 전 기준 상각 강제설은 추정 변경 회계처리를 전면 부정하는 오답입니다.\n④ 손상차손은 회수가능액 미달 시 잡는 독립된 거래이며 내용연수 단축 추정과 다릅니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": True, "why": "내용연수의 단축(추정 변경) 시 전진법을 사용해 당해 연도부터 단축된 기준을 가동하여 상각비를 재배분함을 정당하게 명시했습니다.", "articles": ["K-IFRS 제1008호", "K-IFRS 제1016호 문단 51"], "principle": "내용연수 변경 추정의 전진적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소급 수정 주장은 회계추정 변경 원칙에 위배됩니다.", "articles": ["K-IFRS 제1008호"], "principle": "내용연수 변경 추정의 전진적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "변경 기준을 적용해 상각하여야 하므로 오답입니다.", "articles": [], "principle": "내용연수 변경 추정의 전진적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일시 상각 처리 대상이 아니므로 틀렸습니다.", "articles": [], "principle": "내용연수 변경 추정의 전진적용", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "방법의 변경이 아닌 추정치 변경이며 양자 모두 전진법을 씁니다.", "articles": [], "principle": "내용연수 변경 추정의 전진적용", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "유형자산의 정기 종합검사 원가를 자산화하면서, 직전에 수행했던 과거 종합검사의 미상각 잔액을 파악할 수 없을 때 기준서가 허용하는 과거 잔액의 제거 대리 분개 방식은?",
        "options": [
            "① 과거 종합검사 잔액은 '0'으로 추정해 지우지 않고 신규 검사액만 더해 둔다.",
            "② 이번에 지출한 신규 종합검사 원가를 기초로 하여, 과거 검사가 수행되었을 때 지출했을 검사원가를 추정 역산한 뒤 감가상각누계액을 뺀 잔액을 구해 장부에서 지워낸다.",
            "③ 관련 기계장치 전체 취득원가의 10%를 강제 제거한다.",
            "④ 직전 검사의 잔액을 이번 검사원가에서 마이너스하여 자본화 금액 자체를 차감한다.",
            "⑤ 무형자산 상각누계액 항목으로 대체 기입해 둔다."
        ],
        "answer": "2",
        "explanation": "② K-IFRS 제1016호 문단 70에 따라, 과거 검사원가의 미상각 잔액을 개별 추적할 수 없는 경우, 신규 종합검사비용의 크기를 당해 자산 취득/건설 시(혹은 직전 검사 시) 원가로 대용 역산하여 과거 검사 관련 취득원가 및 상각누계액을 추정하고 그 미상각 잔액을 확실히 지울 수 있습니다.\n\n[오답 해설]\n① 제거하지 않고 방치하는 것은 이중 계산이 되므로 금지됩니다.\n③ 임의의 10% 강제 차감은 기준서 근거가 없는 오류입니다.\n④ 차감한 순액 자본화는 원칙적인 총액 대체 및 폐기 손익 인식 원칙에 위배됩니다.\n⑤ 무형자산 계정 대체는 불가합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "과거분 제거 의무가 있으므로 방치설은 오답입니다.", "articles": ["K-IFRS 제1016호 문단 14"], "principle": "종합검사원가 추정제거 기법", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "신규 검사비를 대용 가치로 써서 과거 취득가와 상각액을 역산해 털어내는 대안적 추정 경로를 조문대로 바르게 제시했습니다.", "articles": ["K-IFRS 제1016호 문단 70"], "principle": "종합검사원가 추정제거 기법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "임의의 비율 차감은 회계학적 근거가 없습니다.", "articles": [], "principle": "종합검사원가 추정제거 기법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "순액 차감 적용설은 틀렸습니다.", "articles": [], "principle": "종합검사원가 추정제거 기법", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "무형자산 상각누계액 계정 사용은 계정과목 분류 위반입니다.", "articles": [], "principle": "종합검사원가 추정제거 기법", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "다음 중 유형자산 최초 취득 이후 발생한 후속 지출이 자산인식 요건(자본적 지출)을 충족하여 자산 장부금액 가산 처리가 적법하게 인정되는 사유에 해당하는 것은?",
        "options": [
            "① 제품 생산 라인의 재편성에 따른 기계의 물리적 재배치 수송료",
            "② 기계 부품 교체로 생산 속도가 대폭 빨라지고 기계 오작동 비율이 영구적으로 절감되는 개조 지출",
            "③ 기계 외관의 단순 녹 제거 및 일상적 녹 방지 페인트 주입 지출",
            "④ 기계 오동작 수리를 위해 투입된 소모성 예비 나사 및 너트 구입 지출",
            "⑤ 기계 가동을 인위적으로 보류한 정지 기간 동안 들어간 운휴 관리 노동 인건비"
        ],
        "answer": "2",
        "explanation": "② 자본적 지출은 미래경제적효익을 유의적으로 증대시키는 지출이어야 합니다. 기계 오작동 비율이 영구적으로 줄어들고 생산 속도가 빨라진 것은 명백한 미래 효익의 증대이므로 자본적 지출로 자산화할 수 있습니다.\n\n[오답 해설]\n① 재배치 비용은 자산 장부금액에 가산하지 않고 즉시 비용 처리합니다(제1016호 문단 20).\n③, ④는 현상 유지를 위한 일상적인 소모 수선비(수익적 지출)입니다.\n⑤ 운휴 비용은 취득완료 후 유지비로 자산화가 불가능합니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "재배치 원가는 비용화 대상이므로 오답입니다.", "articles": ["K-IFRS 제1016호 문단 20"], "principle": "자본적지출 해당 항목 식별", "case": {"holding": "", "no": None}},
            {"correct": True, "why": "출력 속도 증가 및 오류율 감소는 성능 증대 자본적 지출 요건을 완벽히 만족합니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "자본적지출 해당 항목 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "일상적인 녹 제거 및 페인트 주입은 현상유지비(비용)에 속합니다.", "articles": [], "principle": "자본적지출 해당 항목 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "소모성 잡자재 구입은 당기 수선 소모품비로 털어야 합니다.", "articles": [], "principle": "자본적지출 해당 항목 식별", "case": {"holding": "", "no": None}},
            {"correct": False, "why": "운휴 인건비는 즉시 기간 비용화되므로 오답입니다.", "articles": [], "principle": "자본적지출 해당 항목 식별", "case": {"holding": "", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    },
    {
        "id": "practice-accounting-ch04s02-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "태풍이나 화재 등의 일시적 자연재해로 인하여 건물의 외부 벽돌 일부와 유리창 여러 장이 파손되어, 이를 원상태와 똑같이 복구하기 위해 현금 ₩30,000을 지출한 경우 K-IFRS 상 가장 바람직한 회계처리는?",
        "options": [
            "① 건물의 수명이 새롭게 복원되었으므로 ₩30,000을 건물의 취득원가에 가산한다.",
            "② 재해 파손에 따른 단순 원상복구 및 현상 유지 목적의 수선 활동이므로 ₩30,000 전체를 즉시 당기비용(수선비 또는 재해손실)으로 인식한다.",
            "③ 비용 총액을 10년에 걸쳐 분할 감가상각한다.",
            "④ 건물의 감가상각누계액에서 직접 차감하여 건물의 장부금액을 역으로 늘린다.",
            "⑤ 자본잉여금 과목에서 ₩30,000을 차감하여 손익보고를 회피한다."
        ],
        "answer": "2",
        "explanation": "② 자연재해로 인해 파손된 자산을 원상 복원하여 이전과 동일한 성능 상태로 돌려놓는 지출은 자산가치를 기존의 최고 상태보다 유의적으로 증가시키지 못하는 단순 현상 유지/보수 활동에 속하므로 발생 즉시 당기손익(수선비 혹은 재해손실 등 비용)으로 전액 인식하는 것이 타당합니다.\n\n[오답 해설]\n① 가치의 추가 향상이 없는 단순 복구이므로 자본적 지출이 될 수 없습니다.\n③ 비용 이연 처리는 불허됩니다.\n④ 상각누계액 직접 상계는 원칙적 회계처리가 아닙니다.\n⑤ 자본잉여금 차감은 재무 정보 왜곡을 초래하는 위법한 처리입니다.",
        "question_type": "개념5지",
        "option_meta": [
            {"correct": False, "why": "가치 개선이 없는 단순 보수이므로 자산화 가산은 오답입니다.", "articles": [], "principle": "원상 복구 지출의 회계 처리", "case": {"holding": "건물", "no": None}},
            {"correct": True, "why": "재해 파손 원상 복구 및 단순 유리 교체는 수선비 계열의 수익적 지출(당기비용)로 털어야 함을 바르게 서술했습니다.", "articles": ["K-IFRS 제1016호 문단 12"], "principle": "원상 복구 지출의 회계 처리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "이연 상각 처리는 불가합니다.", "articles": [], "principle": "원상 복구 지출의 회계 처리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "누계액 직접 차감 분개는 타당하지 않습니다.", "articles": [], "principle": "원상 복구 지출의 회계 처리", "case": {"holding": "건물", "no": None}},
            {"correct": False, "why": "자본 직접 차감은 손익 왜곡을 낳으므로 오류입니다.", "articles": [], "principle": "원상 복구 지출의 회계 처리", "case": {"holding": "건물", "no": None}}
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
                "item": "2절 유형자산의 후속지출"
            }
        }
    }
]

questions.extend(part1_questions)

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(part1_questions)} new questions (Part 1). Total questions in questions_db_accounting.json: {len(questions)}")
