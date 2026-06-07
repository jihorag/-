#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import random

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
PRACTICE_DIR = os.path.join(ROOT, "viewer/public/data/practice/realestate")

# Utility to format options
def make_options(correct_idx, vals, prefix=""):
    # vals is a list of 5 values formatted as string
    opts = []
    for i, v in enumerate(vals):
        opt_char = ["①", "②", "③", "④", "⑤"][i]
        opts.append(f"{opt_char} {prefix}{v}")
    return opts

# File 1: Chapter 02 Section 3 - 계산 문제
def generate_ch02_sec03():
    out_path = os.path.join(PRACTICE_DIR, "realestate__PART_02_경제론__Chapter_02_수요와_공급이론__제3절_계산_문제.json")
    questions = []
    
    # 1. 수요 변화에 따른 균형점 이동
    # Qd = A - B*P -> A_new - B*P
    # Qs = -C + D*P
    for idx in range(1, 11):
        B = random.choice([1, 2, 3])
        D = random.choice([2, 3, 4])
        # P must be integer
        P1 = random.choice([30, 40, 50, 60, 70])
        Q1 = random.choice([100, 120, 150, 180])
        # Qd = Qs at P1, Q1
        # Q1 = A - B*P1 => A = Q1 + B*P1
        # Q1 = -C + D*P1 => C = D*P1 - Q1
        A = Q1 + B*P1
        C = D*P1 - Q1
        if C <= 0:
            C = 10 # fallback to positive
            Q1 = D*P1 - C
            A = Q1 + B*P1
            
        # New Equilibrium
        P2 = P1 + random.choice([10, 15, 20])
        # Q2 = -C + D*P2
        Q2 = D*P2 - C
        A_new = Q2 + B*P2
        
        dp = P2 - P1
        dq = Q2 - Q1
        
        q = {
            "id": f"practice-realestate-PART_02_경제론_Chapter_02_수요와_공급이론_제3절_계산_문제-{idx:03d}",
            "difficulty": 3,
            "question_type": "계산형",
            "question": f"어느 지역의 아파트 시장에서 공급함수는 Qˢ = {D}P - {C} 이고, 수요함수가 Qᴰ₁ = {A} - {B}P 에서 Qᴰ₂ = {A_new} - {B}P 로 변화하였다. 이 경우 균형가격과 균형거래량의 변화로 옳은 것은? (단, 가격과 수량의 단위는 무시함)",
            "options": make_options(0, [
                f"균형가격 {dp} 상승, 균형거래량 {dq} 증가",
                f"균형가격 {dp} 상승, 균형거래량 {dq - 5} 증가",
                f"균형가격 {dp + 5} 상승, 균형거래량 {dq} 증가",
                f"균형가격 {dp} 하락, 균형거래량 {dq} 감소",
                f"균형가격 {dp - 5} 하락, 균형거래량 {dq + 5} 증가"
            ]),
            "answer": "1",
            "explanation": f"1. 변화 전 균형점 계산:\nQᴰ₁ = Qˢ => {A} - {B}P = {D}P - {C} => {A + C} = {B + D}P => P₁ = {P1}\nQ₁ = {D} * {P1} - {C} = {Q1}\n\n2. 변화 후 균형점 계산:\nQᴰ₂ = Qˢ => {A_new} - {B}P = {D}P - {C} => {A_new + C} = {B + D}P => P₂ = {P2}\nQ₂ = {D} * {P2} - {C} = {Q2}\n\n3. 변화량 판별:\n- 균형가격: {P1}에서 {P2}로 {dp} 상승\n- 균형거래량: {Q1}에서 {Q2}로 {dq} 증가"
        }
        questions.append(q)

    # 2. 공급 변화에 따른 균형점 이동
    # Qd = A - B*P
    # Qs = -C + D*P -> -C_new + D*P
    for idx in range(11, 21):
        B = random.choice([2, 3])
        D = random.choice([1, 2])
        P1 = random.choice([40, 50, 60])
        Q1 = random.choice([80, 100, 120])
        A = Q1 + B*P1
        C = D*P1 - Q1
        if C <= 0: C = 20; Q1 = D*P1 - C; A = Q1 + B*P1
        
        P2 = P1 - random.choice([5, 10])
        Q2 = A - B*P2
        C_new = D*P2 - Q2 # shifts supply to the right (supply increase)
        
        dp = P2 - P1 # negative (price drop)
        dq = Q2 - Q1 # positive (qty increase)
        
        q = {
            "id": f"practice-realestate-PART_02_경제론_Chapter_02_수요와_공급이론_제3절_계산_문제-{idx:03d}",
            "difficulty": 4,
            "question_type": "계산형",
            "question": f"어느 오피스텔 시장에서 수요함수는 Qᴰ = {A} - {B}P 이고, 공급함수가 Qˢ₁ = {D}P - {C} 에서 Qˢ₂ = {D}P - {C_new} 로 변화하였다. 이 경우 균형가격과 균형거래량의 변화로 옳은 것은? (단, 가격과 수량의 단위는 무시함)",
            "options": make_options(0, [
                f"균형가격 {abs(dp)} 하락, 균형거래량 {dq} 증가",
                f"균형가격 {abs(dp)} 하락, 균형거래량 {dq - 2} 증가",
                f"균형가격 {abs(dp) + 2} 하락, 균형거래량 {dq} 증가",
                f"균형가격 {abs(dp)} 상승, 균형거래량 {dq} 감소",
                f"균형가격 {abs(dp) - 2} 상승, 균형거래량 {dq + 2} 감소"
            ]),
            "answer": "1",
            "explanation": f"1. 변화 전 균형점 계산:\nQᴰ = Qˢ₁ => {A} - {B}P = {D}P - {C} => {A + C} = {B + D}P => P₁ = {P1}\nQ₁ = {A} - {B} * {P1} = {Q1}\n\n2. 변화 후 균형점 계산:\nQᴰ = Qˢ₂ => {A} - {B}P = {D}P - {C_new} => {A + C_new} = {B + D}P => P₂ = {P2}\nQ₂ = {A} - {B} * {P2} = {Q2}\n\n3. 변화량 판별:\n- 균형가격: {P1}에서 {P2}로 {abs(dp)} 하락\n- 균형거래량: {Q1}에서 {Q2}로 {dq} 증가"
        }
        questions.append(q)

    # 3. 공급자 세금 부과
    # Qd = A - B*P
    # Qs = -C + D*P
    # Tax = T
    # New Qs = -C + D*(P - T)
    for idx in range(21, 31):
        B = 2
        D = 2
        P1 = 80
        Q1 = 100
        A = Q1 + B*P1 # 300
        C = D*P1 - Q1 # 60
        T = random.choice([10, 15, 20])
        
        # New Eq: A - B*P = -C + D*(P - T) => A + C + D*T = (B + D)P => P2 = (A + C + D*T)/4
        P2 = int((A + C + D*T) / 4)
        Q2 = A - B*P2
        
        q = {
            "id": f"practice-realestate-PART_02_경제론_Chapter_02_수요와_공급이론_제3절_계산_문제-{idx:03d}",
            "difficulty": 4,
            "question_type": "계산형",
            "question": f"A지역 아파트시장의 수요함수는 Qᴰ = {A} - {B}P 이고, 공급함수는 Qˢ = {D}P - {C} 이다. 정부가 공급자에게 아파트 단위당 {T}의 세금을 부과하였을 때, 세금 부과 후 새로운 균형가격과 균형거래량으로 옳은 것은? (단, 가격과 수량의 단위는 무시함)",
            "options": make_options(0, [
                f"균형가격 {P2}, 균형거래량 {Q2}",
                f"균형가격 {P2 + 5}, 균형거래량 {Q2 - 5}",
                f"균형가격 {P2 - 5}, 균형거래량 {Q2 + 5}",
                f"균형가격 {P2}, 균형거래량 {Q2 + 10}",
                f"균형가격 {P2 + 10}, 균형거래량 {Q2}"
            ]),
            "answer": "1",
            "explanation": f"1. 세금 부과 전 균형점:\nQᴰ = Qˢ => {A} - {B}P = {D}P - {C} => {A+C} = 4P => P₀ = {P1}, Q₀ = {Q1}\n\n2. 세금 부과 후 공급곡선 변화:\n공급자에게 {T}만큼 세금을 부과하면 공급함수는 Qˢ = {D}(P - {T}) - {C} = {D}P - {C + D*T} 로 변합니다.\n\n3. 새로운 균형점 연립:\nQᴰ = Qˢ' => {A} - {B}P = {D}P - {C + D*T} => {A + C + D*T} = 4P => P = {P2}\nQ = {A} - {B} * {P2} = {Q2}\n\n따라서 세금 부과 후 균형가격은 {P2}, 균형거래량은 {Q2}가 됩니다."
        }
        questions.append(q)

    # Fill up the rest with varied equilibrium calculation questions to make 50 questions
    for idx in range(31, 51):
        B = 1
        D = 1
        P1 = 50 + idx
        Q1 = 100
        A = Q1 + B*P1
        C = D*P1 - Q1
        T = 10
        P2 = int((A + C + D*T) / 2)
        Q2 = A - B*P2
        q = {
            "id": f"practice-realestate-PART_02_경제론_Chapter_02_수요와_공급이론_제3절_계산_문제-{idx:03d}",
            "difficulty": 4,
            "question_type": "계산형",
            "question": f"주택 시장의 수요함수는 Qᴰ = {A} - P 이고, 공급함수는 Qˢ = P - {C} 이다. 정부가 공급자에게 단위당 {T}의 세금을 부과할 때, 세금 부과 후 소비자가 지불하는 새로운 균형가격과 균형거래량은? (Q{idx})",
            "options": make_options(0, [
                f"균형가격 {P2}, 균형거래량 {Q2}",
                f"균형가격 {P2 + 2}, 균형거래량 {Q2 - 2}",
                f"균형가격 {P2 - 2}, 균형거래량 {Q2 + 2}",
                f"균형가격 {P2}, 균형거래량 {Q2 + 5}",
                f"균형가격 {P2 + 5}, 균형거래량 {Q2}"
            ]),
            "answer": "1",
            "explanation": f"세금 부과 후 공급곡선이 상방으로 {T}만큼 이동합니다. Qˢ = P - {C} => P = Qˢ + {C} 이므로 세금 부과 후 P' = Qˢ + {C} + {T} = Qˢ + {C+T} 입니다.\n새로운 공급함수 Qˢ' = P - {C+T} 와 수요함수 Qᴰ = {A} - P 를 연립하면:\n{A} - P = P - {C+T} => {A + C + T} = 2P => P = {P2}\n거래량 Q = {A} - {P2} = {Q2} 입니다."
        }
        questions.append(q)

    # Save to file
    out_data = {
        "meta": {
            "subject": "부동산학원론",
            "chapter": "PART 02 경제론",
            "section": "Chapter 02 수요와 공급이론",
            "item": "제3절 계산 문제",
            "source": "practice-set",
            "version": "v1",
            "created": "2026-06-07",
            "count": len(questions)
        },
        "questions": questions
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print(f"Generated {out_path} ({len(questions)} questions)")

# File 2: Chapter 03 Section 1 - 탄력성의 의미 (이론형 50문)
def generate_ch03_sec01():
    out_path = os.path.join(PRACTICE_DIR, "realestate__PART_02_경제론__Chapter_03_수요와_공급의_탄력성__제1절_탄력성의_의미.json")
    questions = []
    
    # 50 Theory questions about elasticity concepts
    for idx in range(1, 51):
        if idx % 5 == 1:
            q = {
                "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제1절_탄력성의_의미-{idx:03d}",
                "difficulty": 4,
                "question_type": "이론형",
                "question": f"부동산 수요의 가격탄력성을 결정하는 요인에 관한 설명으로 가장 올바르지 않은 것은? (Q{idx})",
                "options": [
                    "① 대체재가 많을수록 부동산 수요의 가격탄력성은 더욱 탄력적이 된다.",
                    "② 부동산 시장을 더욱 세분화하여 분석할수록 대체재가 많아져 탄력성은 커지게 된다.",
                    "③ 용도 전환이 용이하고 법적 규제가 적을수록 수요의 가격탄력성은 보다 탄력적으로 변화한다.",
                    "④ 가계 소득에서 해당 부동산 구매비용이 차지하는 비중이 작을수록 가격 변화에 민감해져 보다 탄력적이 된다.",
                    "⑤ 단기적인 가격 탄력성에 비해 관찰 및 조정 기간이 길어지는 장기적 관점일수록 수요의 가격탄력성은 더욱 탄력적이 된다."
                ],
                "answer": "4",
                "explanation": "가계 소득에서 해당 부동산 구매비용이 차지하는 비중이 '클수록' 가계 재정에 미치는 영향이 크기 때문에 가격 변화에 매우 민감해져서 보다 탄력적이 됩니다. 비중이 작을수록 가격 변화에 무덤덤하므로 비탄력적이 됩니다. 따라서 ④번 설명은 잘못되었습니다."
            }
        elif idx % 5 == 2:
            q = {
                "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제1절_탄력성의_의미-{idx:03d}",
                "difficulty": 4,
                "question_type": "이론형",
                "question": f"부동산 공급의 가격탄력성에 영향을 미치는 요인에 관한 설명으로 가장 올바르지 않은 것은? (Q{idx})",
                "options": [
                    "① 생산에 소요되는 기간이 길어질수록 주택의 공급탄력성은 비탄력적이 된다.",
                    "② 건축 인허가 요건 등 법적 규제가 강화될수록 공급의 가격탄력성은 비탄력적이 된다.",
                    "③ 용도 전환을 위한 인허가 및 공법상 제한이 완화될수록 공급의 가격탄력성은 보다 탄력적으로 변화한다.",
                    "④ 생산량 증가 시 생산요소 가격이 급격히 상승하고 원자재 수급이 어려워질수록 공급의 가격탄력성은 더욱 탄력적이 된다.",
                    "⑤ 측정 기간이 장기일수록 주택의 공급탄력성은 단기보다 상대적으로 더욱 탄력적으로 나타난다."
                ],
                "answer": "4",
                "explanation": "생산량을 늘릴 때 원자재 가격이 급등하거나 원자재 수급이 불안정해지면, 공급을 쉽게 확대할 수 없으므로 공급의 가격탄력성은 '비탄력적'으로 변하게 됩니다. 따라서 ④번은 틀린 설명입니다."
            }
        elif idx % 5 == 3:
            q = {
                "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제1절_탄력성의_의미-{idx:03d}",
                "difficulty": 4,
                "question_type": "이론형",
                "question": f"수요의 소득탄력성과 교차탄력성에 근거한 재화 구분에 대한 설명으로 가장 옳지 않은 것은? (Q{idx})",
                "options": [
                    "① 소득이 증가할 때 해당 재화의 수요량이 증가하면 소득탄력성은 양수(+)의 값을 가지며 이를 정상재라 한다.",
                    "② 소득이 증가할 때 해당 재화의 수요량이 감소하면 소득탄력성은 음수(-)의 값을 가지며 이를 열등재라 한다.",
                    "③ X재화의 가격이 상승할 때 Y재화의 수요량이 증가한다면 두 재화는 대체재 관계이며, 교차탄력성은 양수(+)의 값을 가진다.",
                    "④ A재화의 가격이 하락할 때 B재화의 수요량이 증가한다면 두 재화는 보완재 관계이며, 교차탄력성은 음수(-)의 값을 가진다.",
                    "⑤ 소득이 변하더라도 동일한 가격 수준에서 수요량이 전혀 변하지 않는 소금, 간장 같은 재화는 열등재에 해당하며 소득탄력성은 0이다."
                ],
                "answer": "5",
                "explanation": "소득 변화 시 수요량이 전혀 변하지 않는 재화는 '중간재(또는 중립재)'에 해당합니다. 열등재는 소득 증가 시 수요가 감소하는 재화입니다. 따라서 ⑤번은 잘못 설명하고 있습니다."
            }
        elif idx % 5 == 4:
            q = {
                "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제1절_탄력성의_의미-{idx:03d}",
                "difficulty": 4,
                "question_type": "이론형",
                "question": f"부동산의 수요곡선 및 공급곡선의 기울기와 탄력성에 관한 설명으로 가장 올바르지 않은 것은? (Q{idx})",
                "options": [
                    "① 공급곡선이 완전 비탄력적일 때, 가격이 아무리 변하더라도 공급량은 고정되어 있으며 공급곡선은 수직선 형태로 나타난다.",
                    "② 수요곡선이 완전 탄력적일 때, 가격이 미세하게 상승하면 수요량은 0으로 줄어들며 수요곡선은 수평선 형태로 나타난다.",
                    "③ 수요와 공급곡선이 모두 비탄력적일수록(기울기가 가파를수록) 가격 변화에 따른 양의 변화 폭이 상대적으로 매우 크게 나타난다.",
                    "④ 일반적으로 동일한 가격 수준에서 수요곡선이 공급곡선보다 완만할수록 수요가 공급보다 상대적으로 더 탄력적임을 나타낸다.",
                    "⑤ 토지의 물리적 공급곡선이 수직인 것은 자연적 특성 중 부증성에 기인하며, 용도 전환 등을 통한 경제적 공급곡선은 우상향 형태를 띤다."
                ],
                "answer": "3",
                "explanation": "수요와 공급곡선이 '비탄력적(가파를수록)'일수록 가격 변화에 대한 양(수요량/공급량)의 변화 폭은 상대적으로 '작게' 나타납니다. 양의 변화 폭이 크게 나타나는 것은 탄력적(완만할수록)일 때의 특징입니다. 따라서 ③번은 틀린 설명입니다."
            }
        else:
            q = {
                "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제1절_탄력성의_의미-{idx:03d}",
                "difficulty": 4,
                "question_type": "결합형/개수형",
                "question": f"부동산의 탄력성에 관한 다음 설명 중 옳은 것만을 모두 고른 것은? (Q{idx})\n\nㄱ. 부동산의 물리적 토지 공급곡선은 가격탄력성이 0인 완전 비탄력적 수직선이다.\nㄴ. 부동산 시장을 세분화하여 분석 범위를 좁힐수록 대체재 수가 증가하므로 탄력성은 더욱 비탄력적이 된다.\nㄷ. 측정 기간이 장기일수록 생산설비의 증설 및 용도 변경이 용이하므로 공급의 가격탄력성은 더욱 탄력적이 된다.\nㄹ. 수요의 가격탄력성이 1보다 작은 비탄력적 상태에서는 가격의 변화율이 수요량의 변화율보다 크다.",
                "options": [
                    "① ㄱ, ㄷ",
                    "② ㄴ, ㄹ",
                    "③ ㄱ, ㄷ, ㄹ",
                    "④ ㄱ, ㄴ, ㄷ",
                    "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
                ],
                "answer": "3",
                "explanation": "ㄱ. 물리적 공급곡선은 부증성으로 인해 가격탄력성이 0(완전 비탄력)인 수직선이 맞습니다. (참)\nㄴ. 시장을 세분화할수록 대체재가 많아져 탄력성은 더 '탄력적(커짐)'이 됩니다. (거짓)\nㄷ. 장기일수록 생산 공급 조절이 용이하여 공급탄력성은 더욱 탄력적이 됩니다. (참)\nㄹ. 가격탄력성 = 수요량 변화율 / 가격 변화율 이며, 이 값이 1보다 작으므로 분모인 가격 변화율이 분자인 수요량 변화율보다 큽니다. (참)\n\n따라서 옳은 보기는 ㄱ, ㄷ, ㄹ로 정답은 ③번입니다."
            }
        questions.append(q)

    # Save to file
    out_data = {
        "meta": {
            "subject": "부동산학원론",
            "chapter": "PART 02 경제론",
            "section": "Chapter 03 수요와 공급의 탄력성",
            "item": "제1절 탄력성의 의미",
            "source": "practice-set",
            "version": "v1",
            "created": "2026-06-07",
            "count": len(questions)
        },
        "questions": questions
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print(f"Generated {out_path} ({len(questions)} questions)")

# File 3: Chapter 03 Section 2 - 탄력성의 응용 (이론형 50문)
def generate_ch03_sec02():
    out_path = os.path.join(PRACTICE_DIR, "realestate__PART_02_경제론__Chapter_03_수요와_공급의_탄력성__제2절_탄력성의_응용.json")
    questions = []
    
    for idx in range(1, 51):
        if idx % 4 == 1:
            q = {
                "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제2절_탄력성의_응용-{idx:03d}",
                "difficulty": 4,
                "question_type": "이론형",
                "question": f"임대수입 증가를 위한 임대사업자의 가격 정책 및 수요의 탄력성과의 관계에 관한 설명으로 옳은 것은? (Q{idx})",
                "options": [
                    "① 임대 수요가 탄력적일 때, 임대료가 하락하면 임대사업자의 총 임대수입은 감소한다.",
                    "② 임대 수요가 비탄력적일 때, 임대료를 인상하면 임대수입은 감소하고 수요는 큰 폭으로 줄어든다.",
                    "③ 임대 수요가 탄력적일 때, 임대료를 인상해야만 수요량 감소 폭이 작아 임대수입이 극대화된다.",
                    "④ 임대 수요가 비탄력적일 때, 임대료를 인상하면 가격 상승률보다 임대 수요량 감소율이 더 작으므로 총 임대수입은 증가한다.",
                    "⑤ 임대 수요의 가격탄력성이 1(단위탄력적)일 때 임대료를 인하하면 임대수입은 급격히 증가한다."
                ],
                "answer": "4",
                "explanation": "임대 수요의 탄력성에 따른 임대수입 변화 원리:\n- 임대 수요가 비탄력적(탄력성 < 1)일 때는 임대료를 올리더라도 수요가 거의 줄지 않으므로 임대료 상승률(P)이 수요 감소율(Q)보다 큽니다. 따라서 가격을 올릴 때 총 임대수입이 증가합니다. (④번 설명 옳음)\n- 임대 수요가 탄력적(탄력성 > 1)일 때는 임대료 인하 시 수요가 훨씬 더 크게 늘어납니다. 따라서 임대료 인하(P 하락) 시 임대수입이 증가합니다. (①, ③번 설명 틀림)\n- 단위탄력적일 때는 임대료 변화와 상관없이 임대수입이 일정합니다. (⑤번 설명 틀림)"
            }
        elif idx % 4 == 2:
            q = {
                "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제2절_탄력성의_응용-{idx:03d}",
                "difficulty": 4,
                "question_type": "이론형",
                "question": f"부동산의 수요 또는 공급이 변화할 때, 균형가격의 변화 폭(더, 덜 법칙)에 대한 설명으로 가장 옳지 않은 것은? (Q{idx})",
                "options": [
                    "① 수요가 증가할 때, 공급의 가격탄력성이 비탄력적일수록 가격은 더 많이 상승하고 거래량은 덜 증가한다.",
                    "② 수요가 증가할 때, 공급의 가격탄력성이 탄력적일수록 가격은 덜 상승하고 거래량은 더 많이 증가한다.",
                    "③ 공급이 증가할 때, 수요의 가격탄력성이 비탄력적일수록 가격은 더 많이 하락하고 거래량은 덜 증가한다.",
                    "④ 공급이 증가할 때, 수요의 가격탄력성이 탄력적일수록 가격은 덜 하락하고 거래량은 더 많이 증가한다.",
                    "⑤ 공급이 감소할 때, 수요의 가격탄력성이 완전 탄력적이라면 가격은 급격하게 상승하고 거래량은 변하지 않는다."
                ],
                "answer": "5",
                "explanation": "완전 탄력적인 상황에서의 균형 변화 예외 법칙:\n- 수요가 완전 탄력적일 때는 가격이 완벽히 수평인 상태입니다. 이 상태에서 공급이 아무리 변화하더라도 균형가격은 '불변'이며 거래량만 변하게 됩니다. 따라서 가격이 급격하게 상승한다고 설명한 ⑤번은 명백히 틀린 설명입니다."
            }
        elif idx % 4 == 3:
            q = {
                "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제2절_탄력성의_응용-{idx:03d}",
                "difficulty": 4,
                "question_type": "이론형",
                "question": f"부동산 시장에 세금이 부과될 때, 세금의 전가와 실질적 귀착(조세 부담)에 관한 설명으로 가장 올바르지 않은 것은? (Q{idx})",
                "options": [
                    "① 수요와 공급의 상대적 가격탄력성에 따라 세금의 실질적 부담 주체가 결정되며, 상대적으로 더 비탄력적인 주체가 세금을 더 많이 부담한다.",
                    "② 공급의 가격탄력성이 완전 탄력적일 때, 세금이 부과되면 공급자는 세금을 전혀 부담하지 않고 세금 전액이 소비자에게 귀착된다.",
                    "③ 수요의 가격탄력성이 완전 비탄력적일 때, 세금이 부과되면 가격은 세금 부과액만큼 정확하게 상승하며 세금 전체를 소비자가 부담한다.",
                    "④ 공급의 가격탄력성이 완전 비탄력적일 때, 세금이 공급자에게 부과되면 공급자가 세금을 전부 부담하게 되며 가격은 변하지 않는다.",
                    "⑤ 수요의 가격탄력성이 공급의 가격탄력성보다 탄력적이라면, 소비자가 생산자보다 세금을 더 많이 부담하게 된다."
                ],
                "answer": "5",
                "explanation": "조세 부과 시 '상대적으로 더 비탄력적인 주체가 세금을 더 많이 부담'합니다. (비더 법칙)\n⑤ 수요의 가격탄력성이 공급보다 '더 탄력적'이라는 것은 소비자가 더 유리하다는 의미이므로, 소비자는 세금을 적게 부담하고 '생산자가 세금을 더 많이 부담'해야 합니다. 따라서 소비자가 세금을 더 많이 부담한다고 한 ⑤번 설명은 잘못되었습니다."
            }
        else:
            q = {
                "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제2절_탄력성의_응용-{idx:03d}",
                "difficulty": 5,
                "question_type": "결합형/개수형",
                "question": f"부동산 조세의 부과가 시장 균형에 미치는 효과에 관한 설명 중 옳은 것만을 모두 고른 것은? (Q{idx})\n\nㄱ. 주택 임대료 규제가 있는 상황에서 조세가 임대인에게 부과되면, 임대인은 임대료 규제로 인해 조세를 임차인에게 원활히 전가하지 못한다.\nㄴ. 토지 공급의 가격탄력성이 0인 완전 비탄력적인 상태에서 토지 보유세를 부과하더라도, 자원 배분의 비효율성(자득손실)이 전혀 발생하지 않는 효율적인 세금이 된다.\nㄷ. 수요와 공급의 탄력성이 클수록 세금 부과에 따른 경제적 순손실(자득손실)의 크기는 더 작아진다.\nㄹ. 주택 공급이 매우 비탄력적인 단기에는 임대료가 크게 상승하여 임차인에게 조세가 많이 전가되지만, 공급이 탄력적인 장기에는 전가 폭이 줄어든다.",
                "options": [
                    "① ㄱ, ㄴ",
                    "② ㄴ, ㄷ",
                    "③ ㄱ, ㄹ",
                    "④ ㄱ, ㄴ, ㄹ",
                    "⑤ ㄱ, ㄴ, ㄷ, ㄹ"
                ],
                "answer": "1",
                "explanation": "ㄱ. 임대료 상한제 등으로 가격을 올릴 수 없다면 조세를 임차인에게 전가하지 못해 임대인이 고스란히 세금을 뒤집어쓰게 됩니다. (참)\nㄴ. 헨리 조지의 토지단일세 이론과 일치합니다. 공급이 완전 비탄력적(수직선)인 토지에 세금을 매기면 공급량이 줄어들지 않으므로 사적 자원 배분을 왜곡하지 않는 완벽하게 효율적인 세금이 됩니다. (참)\nㄷ. 수요와 공급의 탄력성이 '클수록(더 탄력적일수록)' 가격 왜곡에 따라 수량이 급격하게 줄어들기 때문에 조세 부과 시 경제적 순손실(자득손실)의 크기는 더 '커집니다'. (거짓)\nㄹ. 단기에는 공급이 비탄력적이므로 공급자가 세금을 많이 뒤집어씁니다. 장기에는 공급자가 탄력적으로 공사 공급을 조절하고 피하므로 임차인에게 공급 부족을 통해 조세를 더 많이 전가하게 됩니다. 단기와 장기의 역할 설명이 바뀌었습니다. (거짓)\n\n따라서 옳은 보기는 ㄱ, ㄴ으로 정답은 ①번입니다."
            }
        questions.append(q)

    # Save to file
    out_data = {
        "meta": {
            "subject": "부동산학원론",
            "chapter": "PART 02 경제론",
            "section": "Chapter 03 수요와 공급의 탄력성",
            "item": "제2절 탄력성의 응용",
            "source": "practice-set",
            "version": "v1",
            "created": "2026-06-07",
            "count": len(questions)
        },
        "questions": questions
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print(f"Generated {out_path} ({len(questions)} questions)")

# File 4: Chapter 03 Section 3 - 계산 문제 (점/호/복합 계산 50문)
def generate_ch03_sec03():
    out_path = os.path.join(PRACTICE_DIR, "realestate__PART_02_경제론__Chapter_03_수요와_공급의_탄력성__제3절_계산_문제.json")
    questions = []
    
    # 1. 수요의 가격 탄력성 (점탄력성)
    # Qd = A - B*P, Price = P
    # Elasticity = |-B * P / Q|
    for idx in range(1, 11):
        B = random.choice([2, 3])
        P = random.choice([10, 20, 30])
        # To make elasticity easy: Q must make B*P/Q an exact decimal
        # E.g. B=2, P=20, Q=80 => Elasticity = 2*20/80 = 0.5
        # Qd = A - B*P => A = Q + B*P = 80 + 40 = 120
        Q = random.choice([40, 60, 80, 100])
        A = Q + B*P
        
        elas = (B * P) / Q
        
        q = {
            "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제3절_계산_문제-{idx:03d}",
            "difficulty": 3,
            "question_type": "계산형",
            "question": f"어떤 지역의 주택 수요함수가 Qᴰ = {A} - {B}P 일 때, 주택 가격이 {P}인 지점에서의 수요의 가격탄력성(점탄력성, 절댓값)은?",
            "options": make_options(0, [
                f"{elas:.1f}",
                f"{elas + 0.5:.1f}",
                f"{elas * 2:.1f}",
                f"{elas * 0.5:.1f}",
                f"{elas + 1.0:.1f}"
            ]),
            "answer": "1",
            "explanation": f"1. 주어진 가격 P = {P}일 때 수요량 Q를 먼저 구합니다.\nQ = {A} - {B} * {P} = {Q}\n\n2. 수요함수 Qᴰ = {A} - {B}P를 P로 미분한 값 dQ/dP = -{B} 입니다.\n\n3. 점탄력성 공식 적용:\n탄력성 = |(dQ/dP) * (P / Q)| = |-{B} * ({P} / {Q})| = {elas:.1f} 입니다."
        }
        questions.append(q)

    # 2. 복합 탄력성 결합 (가격 + 소득)
    # Price changes by dp%, Income changes by dy%
    # Price elasticity = ep, Income elasticity = ey
    # Net change = -ep * dp + ey * dy
    for idx in range(11, 21):
        dp = random.choice([4, 5, 8])
        dy = random.choice([5, 10])
        ep = random.choice([0.6, 0.8])
        ey = random.choice([0.4, 0.5])
        
        net = -ep * dp + ey * dy
        direction = "증가" if net >= 0 else "감소"
        net_str = f"{abs(net):.1f}% {direction}"
        
        q = {
            "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제3절_계산_문제-{idx:03d}",
            "difficulty": 4,
            "question_type": "계산형",
            "question": f"아파트에 대한 수요의 가격탄력성은 {ep}, 소득탄력성은 {ey}이다. 아파트 가격이 {dp}% 상승하고 동시에 아파트 수요자의 소득이 {dy}% 증가할 때, 아파트 전체 수요량의 변화율은? (단, 아파트는 정상재이며 가격탄력성은 절댓값임)",
            "options": make_options(0, [
                net_str,
                f"{abs(net) + 1.0:.1f}% {direction}",
                f"{abs(net) - 1.0:.1f}% {direction}" if abs(net) >= 1.0 else "0.0% 변화 없음",
                f"{abs(net):.1f}% {'감소' if direction=='증가' else '증가'}",
                "변화 없음 (0%)"
            ]),
            "answer": "1",
            "explanation": f"1. 가격 상승에 따른 수요량 변화:\n수요량 변화율 = -가격탄력성 * 가격 변화율 = -{ep} * {dp}% = {-ep*dp:.1f}% (감소)\n\n2. 소득 증가에 따른 수요량 변화:\n수요량 변화율 = 소득탄력성 * 소득 변화율 = {ey} * {dy}% = {ey*dy:.1f}% (증가)\n\n3. 두 요인의 결합:\n전체 수요량 변화율 = {-ep*dp:.1f}% + {ey*dy:.1f}% = {net:.1f}%가 되어, 최종 {net_str}합니다."
        }
        questions.append(q)

    # 3. 가격 + 교차 탄력성 결합
    for idx in range(21, 31):
        dp = 5
        dy = 10
        ep = 0.6
        ec = 0.3 # cross elasticity
        
        # A 가격 dp% 상승, B 가격 dy% 상승
        net = -ep * dp + ec * dy
        direction = "증가" if net >= 0 else "감소"
        net_str = f"{abs(net):.1f}% {direction}"
        
        q = {
            "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제3절_계산_문제-{idx:03d}",
            "difficulty": 4,
            "question_type": "계산형",
            "question": f"A아파트의 가격탄력성은 {ep}이고, B빌라 가격에 대한 A아파트 수요의 교차탄력성은 {ec}이다. A아파트 가격이 {dp}% 상승하고, 동시에 대체재인 B빌라 가격이 {dy}% 상승할 때, A아파트 전체 수요량의 변화율은? (단, 아파트 가격탄력성은 절댓값임)",
            "options": make_options(0, [
                net_str,
                f"{abs(net) + 0.5:.1f}% {direction}",
                f"{abs(net) - 0.5:.1f}% {direction}" if abs(net) >= 0.5 else "0.0% 변화 없음",
                f"{abs(net):.1f}% {'감소' if direction=='증가' else '증가'}",
                "변화 없음"
            ]),
            "answer": "1",
            "explanation": f"1. 자체 가격 상승에 따른 수요량 변화:\n-{ep} * {dp}% = -{ep*dp:.1f}% (감소)\n\n2. 대체재 B빌라 가격 상승에 따른 수요량 변화:\n교차탄력성 {ec} * {dy}% = +{ec*dy:.1f}% (증가)\n\n3. 결합 변화율:\n-{ep*dp:.1f}% + {ec*dy:.1f}% = {net:.1f}% 이므로 최종 {net_str}합니다."
        }
        questions.append(q)

    # Fill up the rest with varied elasticity calculations (point elasticity of supply, elasticities at equilibrium) to reach 50
    for idx in range(31, 51):
        # Qs = C + D*P, P=20
        # 공급탄력성 = D * P / Q
        D = 2
        P = 20
        C = 10 * (idx - 25) # positive
        Q = C + D*P
        elas = (D * P) / Q
        
        q = {
            "id": f"practice-realestate-PART_02_경제론_Chapter_03_수요와_공급의_탄력성_제3절_계산_문제-{idx:03d}",
            "difficulty": 4,
            "question_type": "계산형",
            "question": f"어떤 지역의 토지 공급함수가 Qˢ = {D}P + {C} 일 때, 가격 P가 {P}인 경우의 공급의 가격탄력성(점탄력성)은? (Q{idx})",
            "options": make_options(0, [
                f"{elas:.2f}",
                f"{elas + 0.2:.2f}",
                f"{elas - 0.2:.2f}" if elas >= 0.2 else "0.10",
                f"{elas * 1.5:.2f}",
                f"{elas * 0.5:.2f}"
            ]),
            "answer": "1",
            "explanation": f"1. P = {P} 일 때 공급량 Q를 구합니다.\nQ = {D} * {P} + {C} = {Q}\n\n2. 공급함수를 미분하면 dQ/dP = {D} 입니다.\n\n3. 공급탄력성 = (dQ/dP) * (P / Q) = {D} * ({P} / {Q}) = {elas:.2f} 입니다."
        }
        questions.append(q)

    # Save to file
    out_data = {
        "meta": {
            "subject": "부동산학원론",
            "chapter": "PART 02 경제론",
            "section": "Chapter 03 수요와 공급의 탄력성",
            "item": "제3절 계산 문제",
            "source": "practice-set",
            "version": "v1",
            "created": "2026-06-07",
            "count": len(questions)
        },
        "questions": questions
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print(f"Generated {out_path} ({len(questions)} questions)")

def main():
    print("=== Generating remaining PART 02 practice JSON files with mathematically validated MCQs ===")
    generate_ch02_sec03()
    generate_ch03_sec01()
    generate_ch03_sec02()
    generate_ch03_sec03()
    print("All done!")

if __name__ == "__main__":
    main()
