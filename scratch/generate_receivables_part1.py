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
    "item": "3절 매출채권과 매입채무"
}

new_questions = [
    # --- L1 (기초): 10문항 (Q1701 ~ Q1710) ---
    {
        "id": "practice-accounting-ch07s03-L1-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-01",
        "year": "",
        "question": "K-IFRS 상 일반적인 상거래에서 발생한 매출채권(Trade Receivables)을 최초로 인식할 때, 유의적인 금융요소가 포함되어 있지 않은 경우의 최초 측정 기준으로 가장 올바른 것은?",
        "options": [
            "① 거래상대방의 신용등급을 반영하여 할인한 세후 현재가치",
            "② 해당 자산의 미래 현금흐름에 대한 역사적 평균 회수액",
            "③ K-IFRS 제1115호(고객과의 계약에서 생기는 수익)에 따라 정의되는 '거래가격(Transaction Price)'",
            "④ 기말 결산시점의 공정가치에서 추정 처분부대비용을 차감한 순공정가치",
            "⑤ 유사한 신용 등급을 가진 채무상품의 시장 평균 이자율로 할인한 현재가치"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1109호에 따라 최초 인식시점에 유의적인 금융요소가 포함되어 있지 않은 매출채권은 K-IFRS 제1115호에 따른 '거래가격'으로 측정합니다.\n\n[오답 해설]\n①, ⑤ 유의적인 금융요소가 없다면 최초 인식 시 이자율 등을 통한 현재가치 평가를 이행하지 않고 거래가격 그대로 인식합니다.\n② 역사적 평균 회수액은 대손 설정 시의 참고 수치이지 최초 인식 측정치가 아닙니다.\n④ 순공정가치는 손상이나 재평가 시 고려되는 개념이며 최초 측정 기준이 아닙니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L1-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-02",
        "year": "",
        "question": "다음 중 K-IFRS 재무상태표 상 일반적인 상거래 관련 '매출채권'과 '매입채무'에 통합 공시될 수 있는 과목들의 결합으로 가장 옳은 것은?",
        "options": [
            "① 매출채권: 미수금과 대여금 / 매입채무: 미지급금과 선수금",
            "② 매출채권: 외상매출금과 받을어음 / 매입채무: 외상매입금과 지급어음",
            "③ 매출채권: 선급금과 매출채권 / 매입채무: 선수금과 매입채무",
            "④ 매출채권: 미수수익과 당좌예금 / 매입채무: 미지급비용과 당좌차월",
            "⑤ 매출채권: 외상매출금과 선급비용 / 매입채무: 외상매입금과 선수수익"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 일반적인 상거래(주된 영업활동인 재화나 용역의 매매)에서 발생한 채권인 '외상매출금'과 '받을어음'은 '매출채권'으로 통합 표시하며, 채무인 '외상매입금'과 '지급어음'은 '매입채무'로 통합 공시합니다.\n\n[오답 해설]\n① 미수금, 대여금, 미지급금은 일반적인 영업거래 이외에서 발생하는 비영업용 채권·채무이므로 별도 표시합니다. 선수금은 비금융부채입니다.\n③ 선급금과 선수금은 재화나 용역을 수취할 권리/의무로서 비금융 항목에 해당하므로 매출채권/매입채무와 성격이 다릅니다.\n④, ⑤ 미수수익, 미지급비용, 선급비용, 선수수익 등은 기간 귀속에 따른 결산정리 항목(비금융 또는 기타채권)으로 구분됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L1-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-03",
        "year": "",
        "question": "조기 대금 회수를 촉진하기 위해 판매 대금을 약정 기일보다 일찍 상환받는 대가로 판매자가 대금의 일정 비율을 깎아주는 혜택을 뜻하는 올바른 용어는?",
        "options": [
            "① 거래할인 (Trade Discount)",
            "② 매출에누리 (Sales Allowance)",
            "③ 매출환입 (Sales Return)",
            "④ 매출할인 (Sales Discount)",
            "⑤ 매출제각 (Sales Write-off)"
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 매출할인(Sales Discount)은 신용 판매 대금을 조기에 현금으로 납부(결산)할 때 일정액을 감면해 주는 현금할인을 의미합니다.\n\n[오답 해설]\n① 거래할인은 구매 수량이나 거래 규모에 따라 단가를 직접 인하해 주는 상업적 혜택입니다.\n② 매출에누리는 품질 불량이나 파손 등의 사유로 값을 깎아주는 것입니다.\n③ 매출환입은 판매된 상품이 반품되어 들어오는 거래입니다.\n⑤ 매출제각은 대손이 확정되어 채권을 장부에서 지우는 거래입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L1-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-04",
        "year": "",
        "question": "K-IFRS 기대신용손실 모형에 따라 매출채권의 신용손상 위험을 평가하여 결산 시점에 손실충당금(대손충당금)을 추가로 계상하고자 할 때, 정당한 결산 정정 분개 유형은?",
        "options": [
            "① (차) 매출채권 XXX / (대) 손실충당금 XXX",
            "② (차) 손실충당금 XXX / (대) 매출채권처분손실 XXX",
            "③ (차) 대손상각비(손상차손) XXX / (대) 손실충당금 XXX",
            "④ (차) 손실충당금환입 XXX / (대) 대손상각비 XXX",
            "⑤ (차) 대손상각비(손상차손) XXX / (대) 매출액 XXX"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 결산 시 추가로 손실을 반영할 때는 차변에 비용 계정인 '대손상각비(손상차손)'를 적고, 대변에 매출채권의 평가차감 계정인 '손실충당금(대손충당금)'을 기입합니다.\n\n[오답 해설]\n① 매출채권을 대변이 아닌 차변에 늘리는 것은 자산의 이중 인식을 야기합니다.\n②, ④ 충당금을 차변에 적는 것은 기존 적립한 충당금을 상계 또는 환입할 때의 분개입니다.\n⑤ 매출액을 차변에 직접 상계하지 않고 별도의 비용 과목을 사용하여 평가합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L1-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-05",
        "year": "",
        "question": "기중에 특정 매출채권의 회수가 불가능한 것으로 최종 확정되어 해당 채권 ₩5,000을 대손충당금(잔액 충분함)과 상계하여 장부에서 제거(제각)하였다. 이 제각 거래가 발생한 직후 회사의 재무 상태에 미치는 영향으로 가장 옳은 것은?",
        "options": [
            "① 자산총액이 ₩5,000만큼 감소하고 당기순이익도 ₩5,000 감소한다.",
            "② 부채총액이 ₩5,000만큼 증가하고 자산총액은 변동이 없다.",
            "③ 매출채권 순장부금액(Net carrying amount)은 변동이 없으며, 자산총액과 당기 손익에 영향을 주지 않는다.",
            "④ 대손충당금 자본 조정을 환원시켜 자본총계가 ₩5,000만큼 증가한다.",
            "⑤ 대변의 자산이 감소하고 차변에 부채가 유발되어 대차 균형이 무너진다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 대손이 확정되어 제각할 때는 차변에 대손충당금을 차감하고 대변에 매출채권을 제거합니다. 이는 매출채권 총액과 차감 계정인 대손충당금이 같은 금액만큼 동시에 줄어드는 거래이므로, 매출채권의 '순장부금액(매출채권 - 대손충당금)' 및 자산총액에는 아무런 변동이 없으며 손익도 발생하지 않습니다.\n\n[오답 해설]\n① 이미 기말 결산 시 충당금으로 비용처리를 완료해 두었으므로 기중 제각 시점에는 추가 비용(이익 감소)이 발생하지 않습니다.\n②, ④, ⑤ 부채 유발이나 자본총계 증가, 대차 무너짐 등의 주장은 복식부기 논리에 어긋나는 거짓 진술입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L1-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-06",
        "year": "",
        "question": "과거 회계연도에 대손 확정 판정을 내려 장부상에서 이미 제각(제거) 처리하였던 매출채권 중 일부인 ₩3,000을 당기에 뜻밖에 회수하여 현금으로 지급받았다. 이 회수 거래에 대한 올바른 회계처리 분개는?",
        "options": [
            "① (차) 현금 3,000 / (대) 매출액 3,000",
            "② (차) 현금 3,000 / (대) 대손충당금(손실충당금) 3,000",
            "③ (차) 현금 3,000 / (대) 매출채권처분이익 3,000",
            "④ (차) 현금 3,000 / (대) 잡이익 3,000",
            "⑤ (차) 대손상각비 3,000 / (대) 현금 3,000"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 이미 제각했던 매출채권을 회수하는 경우, 해당 채권의 부활 및 회수를 기록해야 합니다. 최종 분개 넷팅 시 (차) 현금 3,000 / (대) 대손충당금 3,000 이 됩니다.\n\n[오답 해설]\n① 이미 지난 기의 매출이므로 매출액을 대변에 기재하는 것은 매출의 이중 계상 오류를 범하게 됩니다.\n③, ④ 채권 부활은 충당금을 복원해 주어야 하므로 처분이익이나 잡이익으로 직접 털지 않습니다.\n⑤ 현금 지급이 아니라 현금 유입(회수) 거래이므로 차대변이 맞지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L1-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-07",
        "year": "",
        "question": "회사가 자사가 보유한 매출채권을 금융기관에 양도(Transfer)하여 현금화하고자 한다. 이 자산 양도 거래가 K-IFRS 상 '매각거래(Sale transaction)'가 아닌 '차입거래(Collateralized borrowing)'로 판정될 때 나타나는 회계적 효과는?",
        "options": [
            "① 매출채권을 장부에서 지우고 처분손실을 인식한다.",
            "② 자산 이전 거래이므로 차변에 현금을 기록하고 대변에는 매출액 자본금 증가를 기재한다.",
            "③ 양도한 매출채권 자산을 그대로 장부에 유지하고, 유입된 현금에 대해 '단기차입금(금융부채)'을 대변에 인식한다.",
            "④ 차입금은 부채이므로 재무제표 밖 부외거래로 처리하고 주석 공시만 진행한다.",
            "⑤ 양도 거래가 자동 소멸하므로 대차대조표 상 자산과 부채 변동이 전혀 유발되지 않는다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 양도한 자산의 소유에 따른 위험과 보상의 대부분을 기업이 여전히 통제 및 부담하여 제거 요건을 충족하지 못하면 '차입거래'에 해당합니다. 이 경우 양도 자산은 제거하지 않고 그대로 유지하며 대가로 받은 현금은 차입금 부채로 보고합니다.\n\n[오답 해설]\n① 자산을 제거하고 처분손실을 잡는 분개는 매각거래(제거 요건 충족) 시의 처리입니다.\n② 매출액이나 자본금을 대변에 적는 것은 복식부기 원리에 부합하지 않습니다.\n④ 차입거래는 엄연히 재무상태표 상 단기차입금으로 계상해야 하는 실질 거래이며 부외거래 대상이 아닙니다.\n⑤ 현금 유입과 부채 계상이 발생하므로 자산과 부채 변동이 유발됩니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L1-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-08",
        "year": "",
        "question": "매입채무(Trade Payables)의 최초 인식 시점은 재고자산 등의 자산 통제권(소유권)이 이전되는 시점이어야 한다. 다음 중 '선적지 인도조건(F.O.B. shipping point)'으로 상품을 수입하는 경우, 매입자가 매입채무와 해당 재고를 장부에 기입해야 하는 시점은?",
        "options": [
            "① 상품이 선적국가 항구에서 선박에 '선적(Shipment)'되는 시점",
            "② 상품이 수입국 통관을 최종 통과하는 수입 통관 완결일",
            "③ 상품이 당사 창고에 실물로 입고되어 검수가 종료된 시점",
            "④ 구매 대금 송금을 위해 거래 은행에 대금을 납부 완료한 날짜",
            "⑤ 수출자로부터 계약금을 송금받은 최초 계약일"
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 선적지 인도조건은 수출지에서 운송인에게 상품을 인도(선적)하는 시점에 통제권과 소유권이 매입자에게 넘어가므로, 매입자는 선적된 시점에 재고자산과 매입채무를 인식해야 합니다.\n\n[오답 해설]\n②, ③ 도착지 인도조건(F.O.B. destination) 등에서는 수입 통관이나 실물 입고 시점을 판단할 수 있으나 선적지 조건에서는 부적절합니다.\n④ 대금 납부 시점은 매입채무의 소멸 시점 결정 요인이며 최초 인식 기준이 아닙니다.\n⑤ 단순 계약체결일에는 아직 이행되지 않은 계약이므로 매입채무를 인식할 수 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L1-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-09",
        "year": "",
        "question": "주로 매출채권의 신용 위험과 수금 관리를 금융기관에 이전하고 조기 자금 조달을 위하여 자사가 보유한 외상매출금 등 매출채권을 팩토링회사(Factor)에 할인·양도하여 회수하는 일련의 금융 거래 방식의 명칭은?",
        "options": [
            "① 매도선택권 (Put Option)",
            "② 차입금 차환 (Refinancing)",
            "③ 팩토링 (Factoring)",
            "④ 리스운용 (Operating lease)",
            "⑤ 채권 환매 약정 (Repo)"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 팩토링(Factoring)은 기업이 영업활동으로 획득한 매출채권을 팩토링 회사에 양도하여 자금을 융통하는 자산 유동화 거래 형태 중 하나입니다.\n\n[오답 해설]\n① 풋옵션은 자산 권리를 행사하여 일정 가액에 매도하는 파생 금융 상품 계약입니다.\n② 차환은 만기가 도래한 부채를 갚기 위해 새로운 부채를 조달하는 행위입니다.\n④ 리스는 임대차 운용에 관한 사항입니다.\n⑤ 환매조건부채권매매(Repo)는 일정 기간 후 환매할 것을 조건으로 양도하는 단기 금융 거래입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L1-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L1-10",
        "year": "",
        "question": "매출 및 매입 거래 시 조기 결제 혜택인 현금할인을 장부에 기입할 때, 최초 거래 시점에는 할인이 적용되지 않은 총액으로 매출과 자산을 전액 기록하고, 실제 결제 시점에 할인을 차감하는 회계처리 방식을 뜻하는 용어는?",
        "options": [
            "① 순액법 (Net Method)",
            "② 총액법 (Gross Method)",
            "③ 공정가치법 (Fair value Method)",
            "④ 현재가치법 (Present value Method)",
            "⑤ 상계법 (Offsetting Method)"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 총액법(Gross Method)은 최초 판매나 매입 시점에 약정된 할인혜택이 적용되지 않은 총 청구액을 기준으로 장부를 계상한 뒤, 기한 내에 할인을 받아 지급하는 시점에 할인을 차감 정산하는 회계 방식입니다.\n\n[오답 해설]\n① 순액법은 최초 거래 발생 시점에 조기 상환 할인이 확실히 적용될 것을 가정하고, 할인액을 뺀 순액으로 매출채권/매입채무를 기록하는 방식입니다.\n③, ④ 자산의 현재 가치 평가나 결산 평가와 관련된 일반 용어로서 현금할인 기록법의 분류명이 아닙니다.\n⑤ 자산 부채의 일방적 삭감 기재인 상계법과는 성격이 다릅니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 1,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    # --- L2 (이해): 15문항 (Q1711 ~ Q1725) ---
    {
        "id": "practice-accounting-ch07s03-L2-01",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-01",
        "year": "",
        "question": "K-IFRS 제1109호 금융자산 기준서가 채택하고 있는 기대신용손실(ECL) 모형이 과거 구 발생손실(Incurred loss) 모형에 비해 가지는 실무적 및 이론적 차이점에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 기대신용손실 모형은 대손이 실제로 발생한 손상 사건(Trigger event)이 사전에 입증된 경우에만 대손충당금을 인식할 수 있게 한다.",
            "② 발생손실 모형은 장래의 경기 전망 등 미래 전망 정보(Forward-looking information)를 매 결산일마다 강제 반영하여 선제적으로 충당금을 쌓게 한다.",
            "③ 기대신용손실 모형 하에서는 매출채권의 최초 인식 시점부터 장래에 발생할 것으로 예상되는 기대신용손실을 신용위험 수준에 따라 즉각적으로 충당금에 적립하여 보고하도록 요구한다.",
            "④ 발생손실 모형이 기대신용손실 모형에 비해 당기 이익의 변동성을 완화하여 비교 가능성을 더 극대화한다.",
            "⑤ 기대신용손실 모형은 금융자산 제거 요건을 완전히 무력화하여 회수가 지연된 모든 채권을 매입채무와 상계한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 기대신용손실(ECL) 모형은 실제 손상사건이 발생하기 전이라도 최초 인식 시점부터 금융자산의 신용 상태를 고려해 기대신용손실을 인식하도록 요구합니다.\n\n[오답 해설]\n① 실제 손상 사건(Trigger) 입증을 요건으로 하던 방식은 과거 발생손실 모형입니다.\n② 미래 전망 정보(Forward-looking)를 필수 반영하도록 혁신한 것은 기대신용손실 모형입니다.\n④ 발생손실 모형은 금융위기 등 대손 폭발 시점에 일시에 손실을 계상하여 이익 변동성을 과도하게 키우는 단점이 지적되어 폐기되었습니다.\n⑤ 손실 모형은 충당금 설정의 신용 위험 측정법일 뿐, 자산 제거 요건을 무력화하거나 채무와 상계 처리를 연동하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-02",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-02",
        "year": "",
        "question": "기업이 상품을 매출한 이후 거래처의 정당한 크레임(품질 불량 등)을 수용하여 대금을 일부 감면해 준 '매출에누리'와 반품 처리된 '매출환입'이 발생하였다. 총액주의 매출 기록 하에서 이 거래들이 기말 재무제표에 미치는 회계적 결과 분석으로 올바른 것은?",
        "options": [
            "① 당기순이익에 미치는 영향은 없으며 오로지 재무상태표의 유동자산 총합만 증가시킨다.",
            "② 총매출액에서 매출에누리와 매출환입을 직접 차감하여 '순매출액'을 산출하고, 동시에 장부상 매출채권을 제거하여 순자산을 감소시킨다.",
            "③ 에누리와 환입액은 영업외비용으로 계상하고 매출채권 잔액은 결제 시점까지 원금 그대로 보존한다.",
            "④ K-IFRS 상 매출에누리는 대손상각비 판정 요건에 준하므로 즉시 손실충당금을 복원하는 수정 분개를 한다.",
            "⑤ 회사가 상계 처리를 배제하므로 총매출액과 총자산이 동시에 과대계상된 결과로 공시된다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 매출에누리와 매출환입은 매출액의 실질적 차감 항목이므로, 총매출액에서 이 금액들을 차감하여 포괄손익계산서 상 '순매출액'을 보고합니다. 동시에 회수 권리가 소멸하였으므로 자산인 매출채권을 장부에서 직접 감소 처리합니다.\n\n[오답 해설]\n① 순매출액 감소에 따라 매출총이익 및 당기순이익이 감소하고 자산도 감소합니다.\n③ 에누리와 환입은 영업외비용이나 판관비 성격의 비용이 아니라 매출액의 차감 항목입니다.\n④ 대손 회계는 채무자의 신용 위험에 기인한 미회수 가능성을 잡는 개념이며, 거래 조건에 따른 에누리/환입과는 구별됩니다.\n⑤ 포괄손익계산서 상 순매출액으로 순액 보고하는 것이 원칙이므로 과대계상되지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-03",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-03",
        "year": "",
        "question": "㈜A는 상품을 외상 판매하면서 대금 청구서에 현금할인 거래 조건으로 '2/10, n/30'을 명시하였다. 이 할인 조건의 상거래적 및 회계적 해석으로 가장 올바른 것은?",
        "options": [
            "① 거래일로부터 2일 이내에 지급하면 10%의 현금 할인을 부여하며, 30일 이내에 전액 납부해야 한다.",
            "② 거래일로부터 10일 이내에 대금을 조기 지급하면 2%의 매출 할인을 적용받고, 할인 기간이 지나더라도 매출일로부터 30일 이내에는 총액 잔액을 전액 결제해야 한다.",
            "③ 대금 결제의 20%는 10일 이내에 완료해야 하며, 나머지 80% 채무는 30일 이내에 상환해야 무이자가 적용된다.",
            "④ 거래 연도 내에 2회 분할 납부가 가능하며, 이율은 연 10%이고 연체이자 기준일은 30일이다.",
            "⑤ 연체 이자율은 10%이며 결제 완료 기한이 최종 2~30일 이내임을 뜻한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② '2/10, n/30'에서 앞의 '2/10'은 판매일로부터 10일 이내에 대금을 입금하면 2%를 깎아주는 혜택을 말하며, 뒤의 'n/30'은 할인 혜택을 포기하더라도 판매일로부터 30일 이내에는 약정된 외상액 전액(Net)을 결제해야 함을 뜻합니다.\n\n[오답 해설]\n① 할인율은 2%이며, 할인 기한은 10일입니다.\n③, ④, ⑤ 분할 납부 규정이나 연체 이자율 10% 등의 기술은 기호 표시의 표준적 약속과 무관한 자의적 오해입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-04",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-04",
        "year": "",
        "question": "매출채권의 평가 방법 중 기말 매출채권 잔액을 경과 기간(연령대)별로 분류하여 각 범주마다 과거 경험 및 미래 신용 상태에 기초한 대손 설정률을 곱해 충당금을 추정하는 '연령분석법(Aging Method)'의 논리적 기초로 가장 타당한 것은?",
        "options": [
            "① 거래처의 규모가 클수록 대손 위험이 비례하여 증가하므로 채권 금액별로 설정율을 차등하는 방법이다.",
            "② 기중 매출이 일어난 월별 총액에 무조건 고정 비율을 부과하는 것이 합리적이기 때문이다.",
            "③ 채권의 회수 지체 기간이 길어질수록 거래처의 재무 상태 악화 및 부도 개연성이 높아져 미회수 위험이 체증한다는 회계적 합리성을 반영한다.",
            "④ 연령분석법은 충당금을 최소화하여 보고기간말 자산 가치를 가장 크게 왜곡 없이 부풀릴 수 있기 때문이다.",
            "⑤ 개별 채권의 법적 만기일 도래 순서와 실제 부도 통지 일자의 시차를 정밀 조율하여 이익을 수시 조절하기 위한 목적이다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 연령분석법은 기말 현재 회수되지 않고 장부에 남아 있는 채권의 연령(경과일수)이 오래될수록 대손 발생 확률(기대손실률)이 기하급수적으로 증가한다는 논리적 추정에 기반하여 충당금 설정률을 연령구간별로 상향 대입하는 합리적인 평가법입니다.\n\n[오답 해설]\n① 채권 규모(금액 크기)가 아닌 연령(연체 기간)에 따라 차등을 둡니다.\n② 기중 월별 매출액 기준이 아닌 기말 시점의 잔액을 연령별로 쪼갭니다.\n④ 충당금 계상을 합리적으로 판단하는 것이 목적이며 의도적 자산 부풀리기는 분식입니다.\n⑤ 이익 조절(이익 유연화) 등은 투명한 회계 보고의 목적에 부합하지 않습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-05",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-05",
        "year": "",
        "question": "K-IFRS 제1109호 상 금융자산(매출채권 등)의 양도 시 제거(Derecognition) 판단을 내릴 때, 1단계 검토 사항인 '소유에 따른 위험과 보상의 대부분 이전' 여부에 관한 설명으로 가장 올바른 것은?",
        "options": [
            "① 양도한 채권의 채무불이행 시 양수자로부터 환매를 요구받는 조건(소구조건)이 포함되어 있다면 위험과 보상이 대부분 이전된 것이다.",
            "② 위험과 보상의 대부분을 이전했는지 여부는 양도 전후로 해당 자산의 순현금흐름의 금액과 시기 변동성에 대한 노출 정도의 변화를 평가하여 판단한다.",
            "③ 위험과 보상의 대부분을 기업이 보유하고 있는 경우에도 통제권을 물리적으로 양수자에게 인계했다면 무조건 즉시 자산을 장부에서 제거한다.",
            "④ 금융자산의 제거 판단은 오직 양도대금 수령 계약서의 법적 형식(Form)에 의해서만 결정되며 거래의 경제적 실질은 고려하지 않는다.",
            "⑤ 소유에 따른 위험은 언제나 정부 보증에 의해 상쇄되므로 대손충당금만 처분손실로 이체하면 완결된다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② K-IFRS 기준서에 따라 양도 전후로 자산의 순현금흐름 금액 및 시기 변동성 노출 정도를 비교 평가하여 위험과 보상의 대부분 이전 여부를 판정합니다.\n\n[오답 해설]\n① 소구조건(With Recourse)이 있다면 채무불이행 위험을 회사가 고스란히 안고 있으므로 위험과 보상이 대부분 '보유'된 것입니다.\n③ 위험과 보상의 대부분을 회사가 보유하고 있다면 통제권의 제3자 인도 여부와 상관없이 장부에서 제거할 수 없습니다. (차입거래 처리)\n④ 회계 처리는 법적 형식이 아닌 거래의 '경제적 실질(Substance over form)'을 지배적 기준으로 삼습니다.\n⑤ 정부 보증 여부는 일반 사기업 상거래 채권 거래의 기본 제거 판단 요건과 직접적 상관이 없습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-06",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-06",
        "year": "",
        "question": "회사가 은행과 매출채권 팩토링 계약을 체결하였다. 만약 채무자가 결제일에 대금을 최종 지급하지 못할 경우, 은행이 회사에 대해 해당 대금 상환을 청구할 수 있는 법적 권리인 '소구권(Recourse right)'을 보유하고 있는 조건(소구조건부 양도)일 때의 정당한 회계적 판단은?",
        "options": [
            "① 양도 시점에 매출채권을 전액 장부에서 차감 제거하고 매출채권처분손실을 기재한다.",
            "② 채무자의 부도 발생 위험을 은행이 전량 독점하므로 매각거래에 해당한다.",
            "③ 대손충당금을 전액 환입하여 당기 영업이익을 증가시키고 부채를 감소시킨다.",
            "④ 채무불이행 위험(신용위험)의 대부분을 양도자인 회사가 계속 부담하고 있으므로, 매출채권 제거 요건에 위배되어 매각거래가 아닌 '차입거래'로 회계처리하여 유입 현금을 부채(단기차입금)로 보고한다.",
            "⑤ 이자비용 대신 자본금 차감 항목인 주식할인발행차금으로 직접 분개한다."
        ],
        "answer": "4",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False}
        ],
        "explanation": "④ 소구조건부 매출채권 양도(With Recourse)는 양수 은행이 부도 위험을 회피하여 판매자에게 고스란히 전가한 형태입니다. 즉, 매출채권의 신용위험을 양도인이 여전히 지고 있어 위험과 보상의 대부분을 보유한 것이 되므로 매출채권을 제거할 수 없으며 '차입거래'로 회계처리하여 단기차입금(부채)을 계상해야 합니다.\n\n[오답 해설]\n①, ② 소구조건이 있으면 신용위험이 매입자에게 가지 않으므로 매각거래로 자산을 장부에서 지우는 것은 규정 위반입니다.\n③ 신용 불확실성이 그대로 남아 있으므로 충당금을 환입할 수 없습니다.\n⑤ 차입에 따른 수수료성 이자는 이자비용으로 인식하며 자본 직접 차감은 불가능합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-07",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-07",
        "year": "",
        "question": "매입 대금의 현금할인 거래에 대하여 '총액법'을 선택하여 외상매입금 부채를 최초 기록한 회사가, 약정된 조기 할인 기간(예: 10일 이내)을 경과하여 할인을 받지 못하고 최종 만기 시점에 외상 원금 전액을 결제하였다. 이 경우 만기 결제 시점에 회사가 처리해야 할 적정 회계처리는?",
        "options": [
            "① (차) 외상매입금 (총액) / (대) 현금 (총액) 으로 분개하여 부채를 정상 상환하고 추가적인 할인 상실 이자비용 등은 따로 기재하지 않는다.",
            "② 할인 혜택을 상실했으므로 차변에 이자비용을 별도로 인식하고 대변에는 외상매입금을 늘려 적는다.",
            "③ 순액 결제액과의 차액을 매입할인누락 영업외수익으로 처리하여 대변에 가산한다.",
            "④ 재고자산의 평가 가치를 강제로 삭감하고 평가손실 비용을 당기 비용으로 계상한다.",
            "⑤ 회계처리를 원천 무효화하고 외상 거래 자체를 장부에서 소급 삭감한다."
        ],
        "answer": "1",
        "option_notes": "총액법은 최초에 할인되지 않은 총액으로 매입채무를 기록하므로, 결제 시점에 할인기간 경과로 전액을 지급하게 되더라도 이미 부채가 총액으로 적혀 있으므로 단순히 부채 상환 분개만 진행하고 별도 처리는 필요 없습니다.",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① 총액법에서는 최초 취득 시점에 할인하지 않은 전체 총액을 외상매입금(부채)으로 잡아두었습니다. 따라서 할인기간 경과 후 만기 상환 시에는 장부상 적혀 있던 최초 부채액 그대로 현금 유출 상환을 실행하므로 추가 정정이나 별도 비용 계정이 불필요합니다.\n\n[오답 해설]\n②, ③ 할인 상실을 이자비용으로 분리 정산하는 법은 '순액법' 하에서 발생하는 결산 및 결제 정정 분개입니다.\n④ 재고자산의 최초 가액은 확정되었으므로 매입채무 결제 타이밍에 따라 재고 취득 가치를 매번 사후 재조정하지 않습니다.\n⑤ 상환은 정상 결제 거래이므로 소급 삭감은 부적절합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-08",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-08",
        "year": "",
        "question": "매입 거래에 대대하여 '순액법'을 취급하여 최초 매입 시점에 약정 조기 할인을 이미 차감한 순가액으로 매입채무를 인식하였다. 그러나 이후 할인 기한을 놓치는 바람에 최종 만기 결제 시점에 외상 총액 원금을 어쩔 수 없이 전액 상환하게 되었다. 이 만기 결제 거래에 적용되는 올바른 회계적 회계처리는?",
        "options": [
            "① 순액으로 기재되어 있는 장부의 부채와 대등하게 현금도 순액만 지급하고 차액 정산 요구를 무시한다.",
            "② 만기에 총액으로 유출된 현금과 순액법 부채 잔액과의 차액을 '매입할인상실(또는 이자비용)' 영업외비용 등으로 차변에 반영한다.",
            "③ 차액을 대변에 기재하여 매입채무처분이익으로 처리해 당기순이익에 가산한다.",
            "④ 재고자산의 원가에 차액을 가산하여 유동자산 가치를 늘리고 부채 정산 처리는 누락한다.",
            "⑤ 차액을 대변의 자본잉여금으로 영구 계상하여 이익 귀속을 단절한다."
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 순액법 하에서는 부채가 이미 '순액(총액 - 현금할인액)'으로 적혀 있습니다. 그러나 기한 초과로 인해 만기에 지급한 현금은 '총액'이 되므로, 부채 순액과 현금 지급액(총액) 사이의 차액인 할인 상실분은 금융 비용 성격의 '매입할인상실(이자비용)'로 정비하여 차변에 비용 처리해야 대차 평균의 원리가 성립합니다.\n\n[오답 해설]\n① 실제 상환액은 총액이므로 현금을 순액만 내는 것은 채무불이행입니다.\n③ 비용이 발생한 차액이므로 수익 대변 기입은 거꾸로 된 분개입니다.\n④ 재고자산 취득 취지는 최초에 확정되므로 결제 시점의 이자 비용 성격은 자산 원가에 올리지 않고 당기 비용 정산합니다.\n⑤ 자본 거래가 아니므로 자본잉여금 계상은 불가능합니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-09",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-09",
        "year": "",
        "question": "회사가 회계연도 중에 거래처의 실제 파산 사실을 통보받고 보유 중이던 해당 외상매출금 ₩10,000을 장부 상에서 완전히 상계 제거(제각)하고자 한다. 당시 장부에 기상 적립되어 있던 대손충당금(손실충당금) 잔액이 ₩8,000 존재하였을 경우, 이 제각 분개가 '당기순이익(PL)'에 미치는 최종 금액적 영향은 얼마인가?",
        "options": [
            "① 매출채권 제거에 따른 처분손실 ₩10,000 전액만큼 당기순이익이 감소한다.",
            "② 충당금 ₩8,000이 감소하여 순손실은 발생하지 않고 이익은 적정 유지된다.",
            "③ 충당금 잔액을 초과하여 제각 처리해야 하는 부족분인 ₩2,000(대손상각비 인식액)만큼 당기순이익이 최종 감소한다.",
            "④ 기중 대손 제각 거래는 언제나 전액 이익에 환입되므로 ₩8,000만큼 당기순이익이 오히려 가산 증가한다.",
            "⑤ 대차 차액 ₩2,000을 자본 잉여금에서 차감하므로 순이익 영향은 없다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 외상매출금 ₩10,000을 제각할 때 기존 적립해 둔 충당금 ₩8,000을 먼저 상계하고, 부족분 ₩2,000은 당기 비용인 '대손상각비(손상차손)'로 직접 반영해야 합니다. 이에 따라 비용이 추가로 계상되므로 당기순이익이 ₩2,000 감소하게 됩니다.\n- 분개: (차) 대손충당금 8,000, 대손상각비 2,000 / (대) 외상매출금 10,000\n\n[오답 해설]\n① ₩8,000은 이미 이전 결산 시에 비용 처리하여 적립된 충당금이므로 기중에 다시 비용화하지 않습니다.\n② 충당금 잔액을 넘어선 채권 제거는 당기 비용 처리를 수반하므로 영향이 발생합니다.\n④, ⑤ 제각 거래는 자산의 차감이며 비용 계상이 뒤따르므로 이익 증가나 자본 직접 대입 주장은 오류입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-10",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-10",
        "year": "",
        "question": "K-IFRS 제1109호 금융자산 평가 기준 상, 결산일에 매출채권 등에 대해 기대신용손실(ECL)을 합리적이고 객관적인 사실에 근거하여 측정하고자 할 때 기업이 반드시 동시에 결합하여 평가해야 하는 세 가지 핵심 정보에 부합하지 않는 것은?",
        "options": [
            "① 과거 사건의 이력 및 대손 경험율에 관한 역사적 내부 정보",
            "② 기말 결산시점 현재의 채무자 신용 상태 및 거래 실태 정보",
            "③ 대차대조표 상 매출채권을 기말에 FVOCI 자산으로 재지정하여 얻는 가상의 자본 평가이익 예측 정보",
            "④ 미래의 거시 경제 여건, 이자율 변동 전망 및 국가 신용 리스크 등 미래전망정보(Forward-looking info)",
            "⑤ 합리적이고 뒷받침될 수 있는 과거, 현재 및 미래 경제 전망과 관련된 가용한 모든 정보"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 기대신용손실 측정 시에는 과거의 역사적 경험 정보(①), 현재의 신용 상태 정보(②), 그리고 미래의 거시 경제 지표 등의 전망 정보(④)를 종합 고려해야 합니다. 자산 제거 회피 목적의 지정 변경 자본 평가액 분석 등은 신용손실 측정과 성격이 다른 자의적 예측이므로 배제됩니다.\n\n[오답 해설]\n① 과거 경험 정보는 기본 뼈대가 됩니다.\n② 결산 시점의 현재 상황 정보 역시 필수적입니다.\n④ 미래 전망 정보(Forward-looking info)의 강제 결합은 기대신용손실 모형의 대표적인 요건입니다.\n⑤ 가용한 합리적 정보를 모두 활용하는 것이 기본 대원칙입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-11",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-11",
        "year": "",
        "question": "기업이 매출채권의 양도 계약을 평가한 결과, 소유에 따른 위험과 보상의 대부분을 이전하지도 않았고 그렇다고 대부분을 보유하고 있지도 않은 중간 단계 상태에 처해 있다. 이 경우 자산 제거 여부를 결정하는 최종 요건인 '자산의 통제(Control) 상실' 판단 기준으로 가장 올바른 것은?",
        "options": [
            "① 양수자(인계받은 금융기관 등)가 자신의 일방적 결정에 따라 그 자산을 제3자에게 매도할 수 있는 실제적인 능력이 있는지 여부를 확인하여 결정한다.",
            "② 회사의 이사회 결의가 완전히 승인되었는지 여부만을 기초로 결정한다.",
            "③ 국가 금융위원회의 사전 승인 장부가 발급되었는지 확인하여 결정한다.",
            "④ 채무자가 양도 거래 사실에 대해 공증을 발송하였는지 확인하여 결정한다.",
            "⑤ 회사가 자산의 이자 수취 권리를 대리 수금하는 대행계약을 해제했는지의 형식 조건으로 결정한다."
        ],
        "answer": "1",
        "option_meta": [
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "① K-IFRS 제1109호에 따라 위험과 보상의 대부분을 이전하지도 보유하지도 않은 경우, 통제권 보유 여부를 따집니다. 양수자가 추가적인 제한 없이 자산을 제3자에게 매도할 수 있는 실제적 능력이 있다면 기업은 통제권을 상실한 것으로 판단하여 해당 자산을 제거합니다.\n\n[오답 해설]\n②, ③ 이사회 결의나 금융위 승인 여부는 기준서 상의 경제적 제거 판단 기준이 아닙니다.\n④ 채무자의 법적 공증 유무는 통제권 상실을 판가름하는 기준선이 아닙니다.\n⑤ 회사가 이송된 대리 수금을 단순 실행하는 용역(Service) 계약을 했어도 양수자의 양도 매각 능력이 증빙되면 제거 대상이 될 수 있습니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-12",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-12",
        "year": "",
        "question": "㈜A는 상품 외상 매출액 ₩20,000에 대해 결제일에 거래처로부터 반품 크레임 조로 매출에누리 ₩2,000을 확정하여 차감 승인해 준 뒤, 나머지 잔액 ₩18,000은 전액 보통예금으로 즉시 수납하여 예입하였다. 이 거래(에누리 확정 및 예입 완결)가 ㈜A의 유동비율(유동자산/유동부채) 및 부채비율(부채/자본)에 미친 결과적 영향으로 옳은 것은? (단, 당초 ㈜A의 유동비율은 100%보다 크다고 가정한다.)",
        "options": [
            "① 유동자산이 증가하여 유동비율이 상승한다.",
            "② 보통예금이 늘어났으므로 자본총계가 상승하여 부채비율이 하락한다.",
            "③ 에누리 차감으로 인해 유동자산이 ₩2,000 순감소하므로 유동비율이 하락하고, 당기순이익 감소로 자본이 줄어 부채비율은 상승한다.",
            "④ 부채 항목인 매입채무가 변동하여 부채비율만 소폭 하락한다.",
            "⑤ 재무비율에는 아무런 왜곡이나 변동도 발생하지 않는다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 1. 자산 변동: 외상매출금 ₩20,000이 전액 사라지고 보통예금은 ₩18,000만 들어왔으므로 유동자산(자산총액)은 ₩2,000만큼 순감소합니다. 유동부채는 변동이 없으므로 유동비율은 하락합니다.\n2. 자본 및 부채비율 변동: 매출에누리 ₩2,000은 매출액의 차감 항목이므로 당기순이익이 ₩2,000 감소하여 기말 자본총계가 줄어듭니다. 부채는 변동이 없으므로 '부채/자본'인 부채비율은 상승합니다.\n\n[오답 해설]\n① 유동자산이 ₩2,000 순감소하므로 비율은 오히려 내려갑니다.\n② 현금 ₩18,000은 이미 외상 자산에 기 반영된 가액의 정산 유입일 뿐이고, 에누리비용으로 이익(자본)은 도리어 줄어듭니다.\n④ 매출에누리는 매출채권과 관계된 거래이므로 부채(매입채무)의 변동이 아닙니다.\n⑤ 자산 감소와 자본 감소가 명백히 수반되므로 재무비율이 변동합니다.",
        "type": "개념5지",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-13",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-13",
        "year": "",
        "question": "매입자가 상품을 외상으로 취득하여 매입채무를 장부에 올린 뒤, 결제일에 은행 수수료 절감 및 조기 지급 약정에 따라 '매입할인(Purchase Discount)'을 받았다. K-IFRS 상 매입자가 취득한 매입할인액의 가장 적합한 회계 기재 장소는?",
        "options": [
            "① 당기 포괄손익계산서 상 영업외수익으로 인식한다.",
            "② 자본 변동표 상의 자본잉여금 증가로 직접 계상한다.",
            "③ 당기 취득한 '재고자산의 매입 원가'에서 직접 차감 정산한다.",
            "④ 판매비와관리비 내 대손충당금환입 계정에 합산하여 감액 공시한다.",
            "⑤ 포괄손익계산서 상 이자수익으로 계상한다."
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ K-IFRS 제1002호 '재고자산'에 따라 재고자산의 매입원가를 결정할 때 발생한 매입할인, 매입에누리, 매입환출 등은 매입 원가에서 직접 차감하여 재고자산의 취득 원가를 올바르게 낮추어 주어야 합니다.\n\n[오답 해설]\n① 영업외수익으로 처리하면 자산 취득원가가 왜곡되어 매출원가 왜곡을 초래합니다.\n② 자본 잉여금은 주주 거래의 결과물이므로 상일상 거래인 매입할인은 귀속될 수 없습니다.\n④, ⑤ 대손충당금 환입이나 이자수익은 상거래 매입 차감액과 본질적 성격이 다릅니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-14",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-14",
        "year": "",
        "question": "회사가 보유한 매출채권을 매각거래 요건에 부합하도록 금융기관에 양도 처분하였다. 이 제거 거래에 대하여 장부에 기재할 '매출채권처분손실'을 측정하는 적정한 공식 구성으로 올바른 것은?",
        "options": [
            "① 처분손실 = 양도 시점에 수령한 현금 대가 - 해당 매출채권의 순장부금액 (단, 양수자에게 지급한 팩토링수수료 등 거래 비용은 별도 영업외비용 비용 처리)",
            "② 처분손실 = 해당 매출채권의 순장부금액 - (양도 수령 대가 - 환매 위험 보증채무의 공정가치 등 새로 인식할 자산/부채 의 순액 영향)",
            "③ 처분손실 = 해당 매출채권의 액면가 - 기 발행된 당좌수표 금액",
            "④ 처분손실 = 양도 수령 대가 - 매출원가",
            "⑤ 처분손실 = 매출채권의 최초 장부 잔액 + 결산 이자수익 누적액"
        ],
        "answer": "2",
        "option_meta": [
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "② 매출채권 매각거래 시 처분손실은 제거된 매출채권의 순장부금액에서 회사가 이전 대가로 수령한 현금(양수자에게 지급한 수수료 및 보증 의무 부채 등의 공정가치 변동액 반영 후 순수령액)을 차감하여 측정합니다. 즉, [제거된 자산의 순장부금액 - (수령 대가 - 새로 부과된 의무 부채 가치)]의 논리로 처분손실이 발생합니다.\n\n[오답 해설]\n① 팩토링 수수료 및 보증 비용은 처분손실에 직접 산입하여 통일하여 보고해야 하므로 별도 일반 영업비용 분류 처리는 오류입니다.\n③ 액면가와 수표의 단순 차액 계산은 제거 손익의 기속 원리와 무관합니다.\n④, ⑤ 매출원가 대입이나 자산잔액에 이자 가산하는 주장은 잘못된 수식 구성입니다.",
        "question_type": "개념5지",
        "indexing_v4": {
            "mapped_taxonomy": taxonomy,
            "difficulty": 2,
            "processed_by": "claude-sonnet-4-6",
            "in_scope": True
        }
    },
    {
        "id": "practice-accounting-ch07s03-L2-15",
        "exam": "[연습문제]",
        "subject": "회계학",
        "source": "practice",
        "number": "L2-15",
        "year": "",
        "question": "다음 중 K-IFRS 상 계약 체결에 의해 현금 등 금융자산을 수취할 '계약상 권리'가 존재하지 않아 금융자산(매출채권 등)으로 분류되지 못하는 '비금융자산' 항목으로만 짝지어진 것은?",
        "options": [
            "① 외상매출금, 받을어음",
            "② 대여금, 보통예금",
            "③ 선급금(Prepayments), 미수세금(Current tax assets)",
            "④ 미수금, 미수수익",
            "⑤ 요구불예금, 주택청약저합통장"
        ],
        "answer": "3",
        "option_meta": [
            {"correct": False},
            {"correct": False},
            {"correct": True},
            {"correct": False},
            {"correct": False}
        ],
        "explanation": "③ 선급금은 사전에 대금을 납부하여 미래에 '현금'이 아닌 '재화나 용역(서비스)'을 인도받을 권리이므로 금융자산이 아닙니다. 미수세금(법인세환급액)은 계약에 의한 계약상 권리가 아닌 세법이라는 법률적 규정에 의해 발생하는 세무적 권리이므로 금융자산 분류에서 배제되는 비금융자산입니다.\n\n[오답 해설]\n①, ②, ④ 외상매출금, 받을어음, 대여금, 미수금, 미수수익 등은 거래 상대방과 체결한 계약에 따라 미래에 확정된 금액의 '현금'을 요구할 수 있는 명백한 금융자산 항목들입니다.\n⑤ 예금 및 청약 예금은 은행과의 약정에 따라 가용한 현금 권리가 보장되므로 금융자산입니다.",
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
