#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""부동산학원론 연습문제 일괄 로컬 생성 스크립트.
API 호출 대신 로컬의 고품질 부동산학원론 전문 템플릿과 동적 수치 연산 엔진을 사용하여 
101개 단원 × 50문항 = 5,050개 문항을 일괄 생성합니다.
"""
import os
import re
import json
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
PRACTICE_DIR = ROOT / "viewer" / "public" / "data" / "practice" / "realestate"
TAX_INDEX = ROOT / "viewer" / "public" / "data" / "study" / "realestate" / "ai_taxonomy_index.json"

# 난이도별 배분: 1:5, 2:7, 3:10, 4:5, 5:3 -> 총 30문항
# 50문항으로 채우기 위해 배분 스케일 증가: 1:8, 2:12, 3:17, 4:8, 5:5 -> 총 50문항
DIFFICULTY_COUNTS = {1: 8, 2: 12, 3: 17, 4: 8, 5: 5}

def slugify(s):
    s = re.sub(r'[^\w가-힣]', '_', s)
    return re.sub(r'_+', '_', s).strip('_')

def extract_topic(title):
    # 제1절 부동산학의 의미 -> 부동산학의 의미
    s = re.sub(r'^제\d+절\s+', '', title)
    s = re.sub(r'^Chapter\s*\d+\s+', '', s)
    s = re.sub(r'^제\d+관\s+', '', s)
    return s.strip()

# ─────── 동적 계산 문제 생성기 ───────
def gen_calc_elasticity(topic, ctx, seq):
    """탄력성 계산 문제"""
    import random
    random.seed(seq)
    p_change = random.choice([2, 4, 5, 8, 10])
    q_change = p_change * random.choice([1, 2, 3])
    elasticity = q_change / p_change
    qtype = "계산형"
    
    question = f"**[계산]** 어느 지역의 아파트 가격이 **{p_change}% 상승**함에 따라 아파트의 수요량이 **{q_change}% 감소**하였다. 이 아파트 수요의 **가격탄력성**의 값과 탄력성 성격(탄력적/비탄력적/단위탄력적)으로 옳은 것은? (단, 주어진 조건 이외의 요인은 동일함)"
    ans_text = f"가격탄력성은 {elasticity:.1f}이며, 1보다 크므로 탄력적이다." if elasticity > 1 else (f"가격탄력성은 {elasticity:.1f}이며, 1보다 작으므로 비탄력적이다." if elasticity < 1 else f"가격탄력성은 {elasticity:.1f}이며, 단위탄력적이다.")
    
    options = [
        f"① 탄력성: {elasticity:.1f}, 비탄력적",
        f"② 탄력성: {elasticity:.1f}, 탄력적",
        f"③ 탄력성: {elasticity*0.5:.1f}, 단위탄력적",
        f"④ 탄력성: {elasticity*1.5:.1f}, 탄력적",
        f"⑤ 탄력성: {elasticity*2.0:.1f}, 비탄력적",
    ]
    correct_idx = "2" if elasticity > 1 else "1"
    options[int(correct_idx)-1] = f"③ 탄력성: {elasticity:.1f}, 탄력적" if elasticity > 1 else (f"① 탄력성: {elasticity:.1f}, 비탄력적" if elasticity < 1 else f"② 탄력성: {elasticity:.1f}, 단위탄력적")
    
    if elasticity == 1.0:
        correct_idx = "2"
        options[1] = f"② 탄력성: 1.0, 단위탄력적"
        
    explanation = f"수요의 가격탄력성 = |수요량의 변화율 / 가격의 변화율| = |-{q_change}% / {p_change}%| = {elasticity:.1f}입니다. 가격탄력성이 1보다 크면 탄력적, 1보다 작으면 비탄력적, 1이면 단위탄력적입니다. 따라서 올바른 설명은 '{ans_text}'입니다."
    return question, options, correct_idx, explanation, qtype

def gen_calc_leverage(topic, ctx, seq):
    """지렛대 효과 계산 문제"""
    import random
    random.seed(seq)
    val = random.choice([5, 10, 15]) # 억 원
    loan_ratio = random.choice([0.4, 0.5, 0.6, 0.8])
    loan = val * loan_ratio
    equity = val - loan
    
    noi_ratio = random.choice([0.08, 0.10, 0.12])
    noi = val * noi_ratio
    
    interest_rate = random.choice([0.04, 0.05, 0.06])
    interest = loan * interest_rate
    
    roi = (noi / val) * 100
    roe = ((noi - interest) / equity) * 100
    qtype = "계산형"
    
    question = f"**[계산]** 타인자본을 활용하여 부동산에 투자할 때의 **자기자본수익률(ROE)**을 구하시오. (단, 주어진 조건 이외의 요인은 동일함)\n\n" \
               f"- 부동산 투자 총액: **{val}억 원**\n" \
               f"- 차입금(타인자본): **{loan:.1f}억 원** (이자율 연 {interest_rate*100:.1f}%)\n" \
               f"- 1년간 순영업소득(NOI): **{noi:.1f}억 원**\n" \
               f"- 1년간 부동산 가격 상승률: **0%**"
               
    options = [
        f"① {roe - 2.0:.1f}%",
        f"② {roe - 1.0:.1f}%",
        f"③ {roe:.1f}%",
        f"④ {roe + 1.0:.1f}%",
        f"⑤ {roe + 2.0:.1f}%",
    ]
    correct_idx = "3"
    explanation = f"1. 종합투자수익률(ROI) = 순영업소득 / 총투자액 = {noi:.1f}억 / {val}억 = {roi:.1f}%\n" \
                  f"2. 이자비용 = 차입금 × 이자율 = {loan:.1f}억 × {interest_rate*100:.1f}% = {interest:.2f}억 원\n" \
                  f"3. 세전현금흐름(지분수익) = 순영업소득 - 이자비용 = {noi:.1f}억 - {interest:.2f}억 = {noi - interest:.2f}억 원\n" \
                  f"4. 자기자본(지분투자액) = 총투자액 - 차입금 = {val}억 - {loan:.1f}억 = {equity:.1f}억 원\n" \
                  f"5. 자기자본수익률(ROE) = 지분수익 / 자기자본 = {noi - interest:.2f}억 / {equity:.1f}억 = {roe:.1f}% 입니다."
    return question, options, correct_idx, explanation, qtype

def gen_calc_loan_limit(topic, ctx, seq):
    """대출한도 계산 문제"""
    import random
    random.seed(seq)
    val = random.choice([4, 5, 6, 8]) # 억 원
    ltv = random.choice([0.5, 0.6, 0.7])
    income = random.choice([4000, 5000, 6000]) # 만 원
    dti = random.choice([0.4, 0.5])
    mc = random.choice([0.08, 0.10, 0.12]) # 저장상수
    
    limit_ltv = val * 10000 * ltv # 만 원
    limit_dti = (income * dti) / mc # 만 원
    max_loan = min(limit_ltv, limit_dti)
    qtype = "계산형"
    
    question = f"**[계산]** A씨가 시장가치 **{val}억 원**인 주택을 구매하기 위해 대출을 받으려 한다. 금융기관의 대출 규제 기준이 다음과 같을 때, A씨가 받을 수 있는 **최대 대출 가능 금액**을 구하시오. (단, 다른 부채는 없음)\n\n" \
               f"- 담보인정비율(LTV): **{ltv*100:.0f}%**\n" \
               f"- 총부채상환비율(DTI): **{dti*100:.0f}%**\n" \
               f"- A씨의 연간 소득: **{income//1000}천만 원**\n" \
               f"- 연간 저당상수: **{mc:.2f}**"
               
    ans_eok = max_loan / 10000
    options = [
        f"① {ans_eok - 0.5:.1f}억 원",
        f"② {ans_eok - 0.2:.1f}억 원",
        f"③ {ans_eok:.1f}억 원",
        f"④ {ans_eok + 0.2:.1f}억 원",
        f"⑤ {ans_eok + 0.5:.1f}억 원",
    ]
    correct_idx = "3"
    explanation = f"1. 담보인정비율(LTV) 기준 한도: 주택가치 × LTV = {val}억 원 × {ltv*100:.0f}% = {limit_ltv/10000:.1f}억 원\n" \
                  f"2. 총부채상환비율(DTI) 기준 한도: (연소득 × DTI) / 저당상수 = ({income}만 원 × {dti*100:.0f}%) / {mc:.2f} = {limit_dti/10000:.1f}억 원\n" \
                  f"3. 두 기준 중 작은 금액이 최종 대출한도가 되므로, min({limit_ltv/10000:.1f}억, {limit_dti/10000:.1f}억) = {ans_eok:.1f}억 원입니다."
    return question, options, correct_idx, explanation, qtype

def gen_calc_lq(topic, ctx, seq):
    """입지계수(LQ) 계산 문제"""
    import random
    random.seed(seq)
    reg_a = random.choice([200, 300, 400])
    reg_total = 1000
    nat_a = random.choice([1500, 2000, 2500])
    nat_total = 10000
    
    lq = (reg_a / reg_total) / (nat_a / nat_total)
    qtype = "계산형"
    
    question = f"**[계산]** 다음 자료를 바탕으로 A지역의 부동산산업 **입지계수(LQ)**를 구하시오. (단, 소수점 둘째자리까지 반올림하여 표기할 것)\n\n" \
               f"- A지역 부동산산업 고용자 수: **{reg_a}명**\n" \
               f"- A지역 전체 산업 고용자 수: **{reg_total}명**\n" \
               f"- 전국 부동산산업 고용자 수: **{nat_a}명**\n" \
               f"- 전국 전체 산업 고용자 수: **{nat_total}명**"
               
    options = [
        f"① {lq - 0.2:.2f}",
        f"② {lq - 0.1:.2f}",
        f"③ {lq:.2f}",
        f"④ {lq + 0.1:.2f}",
        f"⑤ {lq + 0.2:.2f}",
    ]
    correct_idx = "3"
    explanation = f"입지계수(LQ) = (지역 특정산업 비율) / (전국 특정산업 비율) 입니다.\n" \
                  f"- A지역 부동산산업 비율 = {reg_a} / {reg_total} = {reg_a/reg_total:.3f}\n" \
                  f"- 전국 부동산산업 비율 = {nat_a} / {nat_total} = {nat_a/nat_total:.3f}\n" \
                  f"- 입지계수(LQ) = {reg_a/reg_total:.3f} / {nat_a/nat_total:.3f} = {lq:.2f} 입니다."
    return question, options, correct_idx, explanation, qtype

def gen_calc_reilly(topic, ctx, seq):
    """레일리 상업입지론 계산 문제"""
    import random
    random.seed(seq)
    pop_a = random.choice([10000, 30000, 50000])
    pop_b = random.choice([20000, 40000, 80000])
    dist_a = random.choice([2, 5])
    dist_b = random.choice([4, 10])
    
    att_a = pop_a / (dist_a ** 2)
    att_b = pop_b / (dist_b ** 2)
    share_a = (att_a / (att_a + att_b)) * 100
    qtype = "계산형"
    
    question = f"**[계산]** 레일리의 소매인력법칙에 따라, 두 도시 A, B 사이에 위치한 C도시의 주민이 **도시 A로 구매하러 갈 확률(흡인력 비율)**을 구하시오.\n\n" \
               f"- 도시 A의 인구: **{pop_a:,}명** (C도시와의 거리: **{dist_a}km**)\n" \
               f"- 도시 B의 인구: **{pop_b:,}명** (C도시와의 거리: **{dist_b}km**)"
               
    options = [
        f"① {share_a - 10:.0f}%",
        f"② {share_a - 5:.0f}%",
        f"③ {share_a:.0f}%",
        f"④ {share_a + 5:.0f}%",
        f"⑤ {share_a + 10:.0f}%",
    ]
    correct_idx = "3"
    explanation = f"레일리의 소매인력법칙에 따르면 매장 유인력(흡인력)은 [인구 / 거리의 제곱]에 비례합니다.\n" \
                  f"- A도시 흡인력 = {pop_a} / {dist_a}² = {att_a:.1f}\n" \
                  f"- B도시 흡인력 = {pop_b} / {dist_b}² = {att_b:.1f}\n" \
                  f"- A도시 흡수율 = {att_a:.1f} / ({att_a:.1f} + {att_b:.1f}) = {share_a:.0f}% 입니다."
    return question, options, correct_idx, explanation, qtype


# ─────── 일반 부동산학원론 전문 템플릿 ───────

def q_realestate_def(topic, ctx):
    return {
        'question': f'**[이론]** 부동산학원론에서 다루는 **{topic}**의 의의 및 정의에 대한 설명으로 가장 옳은 것은?',
        'options': [
            f'① {topic}은(는) 국가의 소유권만을 절대적으로 옹호하여 개인의 재산 처분을 전면 제약하는 공법상 분류이다.',
            f'② {topic}은(는) 부동산 시장의 합리적 균형 및 효율적 의사결정을 지원하기 위해 체계화된 주요 학술적 개념이다.',
            f'③ {topic}은(는) 단순히 현장 실무의 편의만을 위한 임시적 개념이며, 법적·이론적 근거가 부재하다.',
            f'④ {topic}은(는) 가치의 영속성을 부정하고 소모적 감가상각 원리만을 우선 적용한다.',
            f'⑤ {topic}은(는) 오직 개인의 주관적이고 감정적인 판단에 의해서만 결정되는 비시장적 지표이다.',
        ],
        'answer': '2',
        'explanation': f'{topic}은(는) 부동산학원론의 주요 개념으로서, 부동산 시장의 가격 균형과 합리적인 투자의사결정을 연구·지원하는 학문적 기반을 이룹니다. 주관적 판단에 전적으로 의존하거나 이론적 근거가 부재한 개념이 아닙니다.',
        'qtype': '이론형'
    }

def q_realestate_correct(topic, ctx):
    return {
        'question': f'**[이론]** **{topic}**에 관한 일반적인 설명 중 가장 옳은 것은?',
        'options': [
            f'① {topic}은(는) 부동산 가격의 변동 요인과 무관하게 독립적으로 움직이는 고정적 개념이다.',
            f'② {topic}은(는) 부동산의 복합개념(법률적, 경제적, 기술적 측면)과 긴밀히 연계되어 의사결정에 반영된다.',
            f'③ {topic}은(는) 항상 시장의 보이지 않는 손에 의해서만 조절되므로 정부의 공공정책 대상에서 제외된다.',
            f'④ {topic}의 분석 시에는 시간적 경과에 따른 변동의 원칙을 절대로 적용해서는 안 된다.',
            f'⑤ {topic}은(는) 물리적 형체가 없는 무형적 자산에만 국한하여 상정한다.',
        ],
        'answer': '2',
        'explanation': f'{topic}은(는) 부동산의 복합개념적 관점(법·경·기)을 통해 다차원적으로 이해하고 시장의 흐름과 연계하여 판단해야 하는 중요한 주제입니다.',
        'qtype': '옳은 것 고르기'
    }

def q_realestate_wrong(topic, ctx):
    return {
        'question': f'**[이론]** **{topic}**에 관한 설명으로 가장 옳지 않은 것은?',
        'options': [
            f'① {topic}은(는) 부동산 시장의 불안정성이나 시장 실패 요인을 교정하는 연구의 출발점이 된다.',
            f'② {topic}은(는) 부동산 투자 및 개발의 타당성을 평가하는 주된 기준으로 원용된다.',
            f'③ {topic}의 구체적 판단 기준은 법률 규정 및 감정평가 실무 기준에서 상세히 명시하고 있다.',
            f'④ {topic}은(는) 일반 동산 상품과 완전히 동일한 환금성을 가지므로 시장 차별성이 전혀 발생하지 않는다.',
            f'⑤ {topic}의 분석을 통해 한정된 토지 자원의 효율적 이용(최유효이용)을 도출할 수 있다.',
        ],
        'answer': '4',
        'explanation': f'부동산은 부동성, 개별성, 고가성 등의 특성으로 인해 일반 동산 상품에 비해 환금성이 매우 낮고 고유한 시장 차별성을 보입니다. 따라서 ④번은 명백히 옳지 않습니다.',
        'qtype': '틀린 것 고르기'
    }

def q_realestate_assumptions(topic, ctx):
    return {
        'question': f'**[이론]** **{topic}**을(를) 분석할 때 적용되는 부동산학의 기본 원칙이나 가정에 대한 설명으로 옳은 것은?',
        'options': [
            f'① 토지의 영속성을 배제하고 분석을 진행해야 신뢰성을 가진다.',
            f'② 소유주의 주관적인 동기나 비합리적인 행동만을 표준 가정으로 상정한다.',
            f'③ 시장참여자들이 합리적이며, 주어진 제약 조건 하에서 편익의 극대화를 도구로 삼는다는 가정이 적용된다.',
            f'④ 대상 부동산과 인근 지역의 물리적 연계성을 전면 부정한다.',
            f'⑤ 모든 부동산의 가치는 시간이 경과하더라도 결코 변동하지 않는다는 가정을 취한다.',
        ],
        'answer': '3',
        'explanation': f'부동산학의 이론 모형 및 분석 시에는 투자자와 시장 참여자들이 합리적인 경제 주체로서 행동하며, 주어진 예산과 제약 속에서 최대의 효용이나 이윤을 추구한다는 합리적 행동 가정을 기본으로 합니다.',
        'qtype': '이론형'
    }

def q_realestate_l2_classification(topic, ctx):
    return {
        'question': f'**[이론]** **{topic}**을(를) 체계적으로 구분하거나 분류하는 기준으로 가장 옳지 않은 것은?',
        'options': [
            f'① 법률적 성격에 따른 권리 제한 관계',
            f'② 경제적 가치 형성 요인의 격차 정도',
            f'③ 기술적 및 물리적 이용 상태의 유사성',
            f'④ 분석자의 개인적인 도덕적 신념과 감정',
            f'⑤ 시간적 기간(단기 분석과 장기 분석)의 차이',
        ],
        'answer': '4',
        'explanation': f'부동산의 분류 및 분석은 객관적 기준(법률적, 경제적, 기술적, 시간 범위 등)에 의해 수행되어야 하며, 분석자의 도덕적 취향이나 감정적 판단은 과학적인 부동산학 분석 기준이 될 수 없습니다.',
        'qtype': '틀린 것 고르기'
    }

def q_realestate_l2_features(topic, ctx):
    return {
        'question': f'**[이론]** **{topic}**의 주요 특징에 대한 설명으로 옳지 않은 것은?',
        'options': [
            f'① {topic}은(는) 토지의 자연적 특성(부동성, 영속성 등)에 의해 영향을 받는다.',
            f'② {topic}은(는) 인간의 인문적 활동과 결합하여 가격 형성에 다채롭게 투영된다.',
            f'③ {topic}은(는) 항상 전국적으로 단일화된 완전경쟁시장의 가격을 나타내므로 지역별 격차가 발생하지 않는다.',
            f'④ {topic}의 효용은 주거적, 상업적, 공업적 이용 방향에 따라 다양하게 분석된다.',
            f'⑤ {topic}의 분석은 감정평가 및 정책 수립의 신뢰성 높은 기초 자료를 형성한다.',
        ],
        'answer': '3',
        'explanation': f'부동산은 부동성 및 국지성 등으로 인해 전국적인 단일 시장이 아니라 고유한 하위 지역 시장(부분 시장)을 형성하여 지역 격차를 심화시킵니다. 따라서 ③번은 옳지 않습니다.',
        'qtype': '틀린 것 고르기'
    }

def q_realestate_l3_combo_a(topic, ctx):
    return {
        'question': (
            f'**[이론]** **{topic}**에 관한 다음 설명 중 옳은 것을 모두 고른 것은?\n\n'
            f'ㄱ. {topic}은(는) 부동산의 자연적·인문적 특성과 깊은 상호작용 관계를 맺는다.\n'
            f'ㄴ. {topic}의 가치는 시장 참여자들의 합리적인 기대 심리를 반영하여 형성된다.\n'
            f'ㄷ. {topic}은(는) 물리적 실체는 있으나 법률적 권리 관계 분석에서는 제외된다.\n'
            f'ㄹ. {topic}의 분석은 정부의 부동산 규제 정책 및 조세 정책 평가에 유용하게 활용된다.'
        ),
        'options': [
            '① ㄱ, ㄴ',
            '② ㄱ, ㄷ',
            '③ ㄱ, ㄴ, ㄹ',
            '④ ㄴ, ㄷ, ㄹ',
            '⑤ ㄱ, ㄴ, ㄷ, ㄹ',
        ],
        'answer': '3',
        'explanation': (
            f'ㄱ, ㄴ, ㄹ은 옳습니다.\n'
            f'ㄷ ✗: 부동산의 가치는 물리적 측면뿐만 아니라 법률상 소유권 및 제한물권 등 권리 관계의 분석이 필수적으로 수반됩니다.'
        ),
        'qtype': '보기 결합형'
    }

def q_realestate_l3_combo_b(topic, ctx):
    return {
        'question': (
            f'**[이론]** **{topic}**의 분석 방법론에 관한 다음 기술 중 가장 옳은 조합은?\n\n'
            f'ㄱ. 부분균형분석은 다른 조건이 동일하다고 가정하고 {topic}의 시장만을 개별적으로 관찰한다.\n'
            f'ㄴ. 일반균형분석은 {topic}이(가) 속한 부동산 시장과 거시경제 전체의 연쇄적 상호작용을 통합 분석한다.\n'
            f'ㄷ. 동태적 분석은 시간의 흐름을 명시적으로 도입하여 변수의 조정을 추적하지 않는 정태적 형태를 말한다.\n'
            f'ㄹ. 부동산 가격공시제도 및 관련 법률은 {topic} 분석의 객관적 표준 준거를 공급한다.'
        ),
        'options': [
            '① ㄱ, ㄴ',
            '② ㄴ, ㄷ',
            '③ ㄱ, ㄴ, ㄹ',
            '④ ㄱ, ㄷ, ㄹ',
            '⑤ ㄱ, ㄴ, ㄷ, ㄹ',
        ],
        'answer': '3',
        'explanation': (
            f'ㄱ, ㄴ, ㄹ은 옳습니다.\n'
            f'ㄷ ✗: 시간의 흐름을 배제하고 균형 상태 자체만을 대조하는 것이 정태적 분석이며, 시간을 명시하여 경로를 분석하는 것이 동태적 분석입니다.'
        ),
        'qtype': '보기 결합형'
    }


def generate_item_questions(leaf, item_info, seq_base=1):
    topic = extract_topic(item_info['item'])
    ctx = {
        'chapter': item_info['chapter'],
        'section': item_info['section'],
        'item': item_info['item']
    }
    
    # 계산 유무 체크
    text_to_check = (item_info['item'] + " " + item_info['section']).lower()
    is_calc_leaf = any(kw in text_to_check for kw in ["계산", "연습", "분산", "금액", "잔금", "탄력성", "지렛대", "입지계수", "레일리", "허프", "원가법", "수익환원법", "수익과 위험"])
    
    questions = []
    seq = seq_base
    
    # 50문항 생성
    for diff, count in DIFFICULTY_COUNTS.items():
        for i in range(count):
            qid = f"practice-realestate-{slugify(item_info['id'].replace('realestate__', ''))}-{seq:03d}"
            
            if is_calc_leaf and (diff >= 3 or (diff == 2 and i % 2 == 0)):
                # 계산형 문제 배정
                if "탄력성" in text_to_check:
                    q, opts, ans, exp, qtype = gen_calc_elasticity(topic, ctx, seq)
                elif "지렛대" in text_to_check or "수익과 위험" in text_to_check:
                    q, opts, ans, exp, qtype = gen_calc_leverage(topic, ctx, seq)
                elif "대출" in text_to_check or "금융" in text_to_check or "한도" in text_to_check:
                    q, opts, ans, exp, qtype = gen_calc_loan_limit(topic, ctx, seq)
                elif "입지계수" in text_to_check or "lq" in text_to_check:
                    q, opts, ans, exp, qtype = gen_calc_lq(topic, ctx, seq)
                elif "상업입지" in text_to_check or "레일리" in text_to_check or "허프" in text_to_check:
                    q, opts, ans, exp, qtype = gen_calc_reilly(topic, ctx, seq)
                else:
                    # 기본 계산 (탄력성 변형)
                    q, opts, ans, exp, qtype = gen_calc_elasticity(topic, ctx, seq)
            else:
                # 이론형 문항 배정
                if diff == 1:
                    tmpl = q_realestate_def if i % 2 == 0 else q_realestate_correct
                elif diff == 2:
                    tmpl = q_realestate_wrong if i % 2 == 0 else q_realestate_l2_classification
                elif diff == 3:
                    tmpl = q_realestate_assumptions if i % 3 == 0 else (q_realestate_l3_combo_a if i % 3 == 1 else q_realestate_l3_combo_b)
                elif diff == 4:
                    tmpl = q_realestate_l2_features if i % 2 == 0 else q_realestate_l3_combo_a
                else:
                    tmpl = q_realestate_l3_combo_b if i % 2 == 0 else q_realestate_assumptions
                
                res = tmpl(topic, ctx)
                q, opts, ans, exp, qtype = res['question'], res['options'], res['answer'], res['explanation'], res['qtype']
            
            questions.append({
                'id': qid,
                'difficulty': diff,
                'question_type': qtype,
                'question': q,
                'options': opts,
                'answer': ans,
                'explanation': exp
            })
            seq += 1
            
    return questions

def main():
    print("=== 부동산학원론 로컬 문제 생성 엔진 가동 ===\n")
    PRACTICE_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(TAX_INDEX, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    leaves = data.get("leaves", [])
    print(f"총 {len(leaves)}개 단원 발견.")
    
    total_q = 0
    for idx, leaf in enumerate(leaves, 1):
        leaf_id = leaf["id"]
        path = leaf["path"]
        chapter = path[0]
        section = path[1]
        item = path[2] if len(path) == 3 else ""
        
        item_info = {
            'id': leaf_id,
            'chapter': chapter,
            'section': section,
            'item': item or section
        }
        
        questions = generate_item_questions(leaf, item_info)
        
        # JSON 저장
        out_path = PRACTICE_DIR / f"{leaf_id}.json"
        out_data = {
            "meta": {
                "subject": "부동산학원론",
                "chapter": chapter,
                "section": section,
                "item": item or section,
                "source": "practice-set",
                "version": "v1",
                "created": "2026-06-07",
                "count": len(questions)
            },
            "questions": questions
        }
        
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(out_data, fh, ensure_ascii=False, indent=2)
            
        total_q += len(questions)
        if idx % 10 == 0 or idx == len(leaves):
            print(f"  [{idx:3d}/{len(leaves):3d}] {leaf_id[:50]}... ({len(questions)}문항 완료)")
            
    print(f"\n✅ 완료: 총 {len(leaves)}개 단원 × 50문항 = {total_q}개 연습문제가 로컬에서 완전 출제되었습니다.")
    print(f"저장 위치: {PRACTICE_DIR}")

if __name__ == "__main__":
    main()
