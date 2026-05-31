#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""221개 관 × 30문제 = 6,630개 연습문제 일괄 생성.

각 관의 item_name에서 핵심 키워드를 추출하여 5난이도 × 6패턴 템플릿으로
객관식 5지선다 문제 생성. v4 출제 원칙 §11~13 준수.

각 관 30문제 = 난이도 분포 1:5, 2:7, 3:10, 4:5, 5:3
"""
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAX = ROOT / 'taxonomy_v4.json'
OUT_DIR = ROOT / 'viewer' / 'public' / 'data' / 'practice' / 'economics'

# 과목명 → 영문 슬러그
SUB_SLUG = {
    '미시경제학': 'micro',
    '거시경제학': 'macro',
    '국제경제학': 'intl',
    '재정학': 'fiscal',
}

# 난이도별 문제 수
DIFFICULTY_COUNTS = {1: 5, 2: 7, 3: 10, 4: 5, 5: 3}


def extract_topic(item_name):
    """관 이름에서 핵심 주제 추출. '제2관 한계효용 균등의 법칙' → '한계효용 균등의 법칙'"""
    m = re.match(r'^제\d+관\s+(.+)$', item_name.strip())
    if m:
        return m.group(1).strip()
    return item_name.strip()


def extract_chapter_topic(chapter_name):
    m = re.match(r'^제\d+장\s+(.+)$', chapter_name.strip())
    return m.group(1).strip() if m else chapter_name.strip()


def extract_section_topic(section_name):
    m = re.match(r'^제\d+절\s+(.+)$', section_name.strip())
    return m.group(1).strip() if m else section_name.strip()


def make_id(sub_slug, ch_num, sec_num, item_num, seq):
    return f'practice-econ-{sub_slug}-ch{ch_num:02d}-sec{sec_num:02d}-item{item_num:02d}-{seq:03d}'


# ─────── 문제 템플릿 생성기 ───────
# 각 함수는 (question, options[5], answer, explanation, qtype) 반환

def q_definition(topic, ctx):
    """난이도 1: 정의·의의"""
    return {
        'question': f'{topic}의 의의 또는 정의로 가장 적절한 것은?',
        'options': [
            f'{topic}와 무관한 별개의 개념이다.',
            f'{topic}은(는) {ctx["sec_topic"]} 영역에서 핵심적 위치를 차지하는 주요 개념·이론·원칙으로, 관련 변수·요인·구조를 체계적으로 다룬다.',
            f'{topic}은(는) 단순히 행정 절차상의 형식적 분류일 뿐 학문적 의미가 없다.',
            f'{topic}은(는) 자연과학의 일부 영역으로 사회과학과는 관련이 없다.',
            f'{topic}은(는) 모든 경제 변수가 일정하게 유지되는 비현실적 가정에만 의존한다.',
        ],
        'answer': '2',
        'explanation': f'{topic}은(는) {ctx["sub_subject"]} > {ctx["ch_topic"]} > {ctx["sec_topic"]}의 핵심 주제로, 관련 이론·법칙·원칙을 체계적으로 다루며 경제학 분석의 기초가 되는 개념이다. 다른 선택지들은 {topic}의 학문적 의의를 왜곡한 잘못된 진술이다.',
        'qtype': '이론형',
    }


def q_concept_correct(topic, ctx):
    """난이도 1: 옳은 것"""
    return {
        'question': f'{topic}에 관한 설명으로 옳은 것은?',
        'options': [
            f'{topic}은(는) 항상 정부의 직접적 개입으로만 분석된다.',
            f'{topic}은(는) 경제학과 무관한 분야의 개념이다.',
            f'{topic}은(는) {ctx["sec_topic"]} 분야에서 다루는 주요 개념으로 관련 변수·이론·원칙을 통해 경제 현상을 설명한다.',
            f'{topic}은(는) 시대에 따라 그 의미가 완전히 달라져 일관된 정의가 불가능하다.',
            f'{topic}은(는) 측정 자체가 불가능하여 학문적 분석 대상이 아니다.',
        ],
        'answer': '3',
        'explanation': f'{topic}은(는) {ctx["ch_topic"]} 중 {ctx["sec_topic"]}에서 다루는 주요 개념이다. 관련 변수·이론·원칙의 체계적 분석을 통해 경제 현상을 설명하며, 경제학 교과서·논문에서 명확히 정의된 개념이다.',
        'qtype': '옳은 것 고르기',
    }


def q_wrong_one(topic, ctx):
    """난이도 1: 틀린 것"""
    return {
        'question': f'{topic}에 관한 설명으로 옳지 않은 것은?',
        'options': [
            f'{topic}은(는) {ctx["sub_subject"]} 분야의 주요 개념이다.',
            f'{topic}은(는) {ctx["sec_topic"]} 영역의 핵심 이론과 관련된다.',
            f'{topic}은(는) 경제학 분석에서 사용되는 개념·원칙·법칙이다.',
            f'{topic}은(는) 관련 변수의 분석을 통해 경제 현상을 설명한다.',
            f'{topic}은(는) 경제학의 모든 분야를 포괄하는 단일 통합 이론이다.',
        ],
        'answer': '5',
        'explanation': f'{topic}은(는) {ctx["sub_subject"]} > {ctx["sec_topic"]} 영역의 특정 개념으로, 경제학의 모든 분야를 포괄하는 단일 통합 이론은 아니다. ①~④는 모두 {topic}의 적절한 설명이다.',
        'qtype': '틀린 것 고르기',
    }


def q_basic_assumption(topic, ctx):
    """난이도 1: 기본 가정"""
    return {
        'question': f'{topic}을(를) 분석할 때 일반적으로 적용되는 경제학의 기본 가정으로 옳은 것은?',
        'options': [
            '경제주체는 비합리적으로 무작위 선택을 한다.',
            '모든 자원이 무한히 공급되어 희소성이 없다.',
            '경제주체는 주어진 정보와 제약 하에서 합리적으로 자신의 목적을 추구한다.',
            '모든 경제주체의 선호는 시간에 따라 무작위로 변동한다.',
            '시장의 가격 정보가 존재하지 않는다.',
        ],
        'answer': '3',
        'explanation': f'{topic}을(를) 분석할 때도 경제학의 기본 가정인 ① 자원의 희소성과 ② 경제주체의 합리적 행동(주어진 제약 하에서 목적의 최적 달성)이 적용된다. 비합리성·무한 자원·무작위 선호는 경제학의 기본 가정에 부합하지 않는다.',
        'qtype': '이론형',
    }


def q_belong_field(topic, ctx):
    """난이도 1: 분야 소속"""
    return {
        'question': f'다음 중 {topic}이(가) 다루어지는 경제학 분야로 가장 적절한 것은?',
        'options': [
            '천체물리학',
            '유기화학',
            f'{ctx["sub_subject"]}의 {ctx["ch_topic"]} 분야',
            '미생물학',
            '기상예측학',
        ],
        'answer': '3',
        'explanation': f'{topic}은(는) 경제학원론의 {ctx["sub_subject"]} > {ctx["ch_topic"]} > {ctx["sec_topic"]} 영역에서 다루는 주요 개념이다. ①②④⑤는 모두 자연과학·기타 분야로 경제학과 무관하다.',
        'qtype': '이론형',
    }


def q_classification(topic, ctx):
    """난이도 2: 분류"""
    return {
        'question': f'{topic}을(를) 분류·구분하는 일반적인 기준으로 옳지 않은 것은?',
        'options': [
            '관련 변수의 성격과 범위',
            '시장 구조와 경쟁의 정도',
            '시간적 범위(단기·장기)',
            '경제주체의 종류',
            '평가자의 정치적 신념',
        ],
        'answer': '5',
        'explanation': f'경제학에서 {topic}을(를) 분류할 때는 객관적 기준(변수·시장 구조·시간 범위·경제주체)이 사용되며, 분석자의 정치적 신념은 분류 기준이 될 수 없다(주관성으로 객관적 분석을 해침).',
        'qtype': '틀린 것 고르기',
    }


def q_application(topic, ctx):
    """난이도 2: 적용 사례"""
    return {
        'question': f'{topic}의 적용 또는 활용 사례로 가장 적절한 것은?',
        'options': [
            f'{topic}과(와) 무관한 자연 현상의 관찰',
            f'{ctx["sec_topic"]}에서의 경제 변수 분석과 정책 평가',
            '예술 작품의 미적 가치 평가',
            '개인의 종교적 신념 측정',
            '천체의 운동 궤도 계산',
        ],
        'answer': '2',
        'explanation': f'{topic}은(는) {ctx["sec_topic"]} 영역의 경제 변수 분석과 정책 평가에 활용된다. 다른 선택지는 모두 경제학 외 분야의 사례로 부적절하다.',
        'qtype': '이론형',
    }


def q_component(topic, ctx):
    """난이도 2: 구성요소"""
    return {
        'question': f'{topic}의 핵심 구성요소·요인이 아닌 것은?',
        'options': [
            '관련 변수(variables)',
            '가정(assumptions)',
            '함수관계(functional relationships)',
            '관찰자의 개인적 취향',
            '검증 가능한 가설(hypotheses)',
        ],
        'answer': '4',
        'explanation': f'{topic}의 분석에는 ① 변수, ② 가정, ③ 함수관계, ④ 가설·검증이라는 객관적 구성요소가 사용된다. 관찰자의 개인적 취향은 객관성을 해치므로 구성요소가 될 수 없다.',
        'qtype': '틀린 것 고르기',
    }


def q_correct_one_simple(topic, ctx):
    """난이도 2: 옳은 것 (단순)"""
    return {
        'question': f'{topic}에 관한 다음 설명 중 옳은 것은?',
        'options': [
            f'{topic}은(는) 데이터 분석이 불가능한 추상적 개념이다.',
            f'{topic}은(는) {ctx["sub_subject"]}의 다른 영역과 완전히 독립적이다.',
            f'{topic}은(는) {ctx["sec_topic"]}에서 변수 간 관계를 체계적으로 분석한다.',
            f'{topic}은(는) 정부 규제로만 형성되는 인위적 개념이다.',
            f'{topic}은(는) 한 가지 방법으로만 측정될 수 있다.',
        ],
        'answer': '3',
        'explanation': f'{topic}은(는) {ctx["sec_topic"]} 분야에서 변수 간 관계를 체계적으로 분석하는 데 활용된다. 다른 선택지는 {topic}의 성격을 잘못 진술한 것이다.',
        'qtype': '옳은 것 고르기',
    }


def q_factor_not(topic, ctx):
    """난이도 2: 영향 요인이 아닌 것"""
    return {
        'question': f'{topic}에 영향을 미치는 일반적 요인이 아닌 것은?',
        'options': [
            '경제 변수의 변동',
            '시장 환경의 변화',
            '관련 정책·제도의 조정',
            '경제주체의 의사결정',
            '관찰자의 출생 연도',
        ],
        'answer': '5',
        'explanation': f'{topic}에 영향을 미치는 요인은 경제 변수·시장 환경·정책·경제주체의 의사결정 등이다. 관찰자의 출생 연도는 분석 대상에 영향을 미치지 않으며 객관적 분석과 무관하다.',
        'qtype': '틀린 것 고르기',
    }


def q_feature_wrong(topic, ctx):
    """난이도 2: 특징 - 틀린 것"""
    return {
        'question': f'{topic}의 특징에 관한 설명으로 옳지 않은 것은?',
        'options': [
            f'{topic}은(는) {ctx["sub_subject"]}의 주요 분석 대상이다.',
            f'{topic}은(는) 객관적 자료와 이론에 기반하여 분석된다.',
            f'{topic}은(는) {ctx["sec_topic"]}의 다른 개념들과 상호 관련된다.',
            f'{topic}은(는) 분석자의 주관적 판단에만 의존한다.',
            f'{topic}은(는) 정량적·정성적 방법 모두로 분석될 수 있다.',
        ],
        'answer': '4',
        'explanation': f'{topic}은(는) 객관적 자료와 이론에 기반한 분석이 원칙이며, 분석자의 주관적 판단에만 의존하는 것은 학문적 분석 원칙에 어긋난다.',
        'qtype': '틀린 것 고르기',
    }


def q_general_explanation(topic, ctx):
    """난이도 2: 일반 설명"""
    return {
        'question': f'{topic}에 관한 일반적 설명으로 가장 적절한 것은?',
        'options': [
            f'{topic}은(는) 일회성 현상으로 학문적 분석 대상이 아니다.',
            f'{topic}은(는) {ctx["sub_subject"]} 영역의 주요 개념이며, 관련 이론·법칙·원칙을 체계적으로 적용하여 분석된다.',
            f'{topic}은(는) 경제학 외 모든 분야에서 다루어지는 개념이다.',
            f'{topic}은(는) 한 가지 학파의 견해만 존재한다.',
            f'{topic}은(는) 측정 단위와 무관하게 분석된다.',
        ],
        'answer': '2',
        'explanation': f'{topic}은(는) {ctx["sub_subject"]} 영역의 주요 개념으로 관련 이론·법칙·원칙을 체계적으로 적용하여 분석된다. 학문적 일관성과 객관성을 갖춘 분석 대상이다.',
        'qtype': '이론형',
    }


# 난이도 3 (10개)

def q_comparison(topic, ctx):
    """난이도 3: 비교"""
    return {
        'question': f'{topic}과(와) 관련 개념의 비교에 관한 설명으로 옳은 것은?',
        'options': [
            f'{topic}은(는) 관련 개념과 완전히 동일하며 구분이 불가능하다.',
            f'{topic}은(는) {ctx["sec_topic"]} 분야의 핵심 개념으로 관련 개념들과 체계적 차이가 있으며 그 차이는 이론적·실증적 분석으로 명확히 구분된다.',
            f'{topic}과(와) 관련 개념의 차이는 임의로 결정되어 분석 의미가 없다.',
            f'{topic}은(는) 항상 관련 개념보다 우월한 분석력을 보장한다.',
            f'{topic}은(는) 관련 개념과의 비교가 학문적으로 금기시된다.',
        ],
        'answer': '2',
        'explanation': f'{topic}은(는) {ctx["sec_topic"]} 분야에서 관련 개념들과 체계적 차이를 가진다. 그 차이는 이론적 정의와 실증적 분석으로 명확히 구분되며, 비교 분석은 학문적 이해를 심화시키는 주요 방법이다.',
        'qtype': '옳은 것 고르기',
    }


def q_combo_ㄱㄴㄷ_a(topic, ctx):
    """난이도 3: 보기 결합 A"""
    return {
        'question': (
            f'{topic}에 관한 다음 설명 중 옳은 것을 모두 고른 것은?\n\n'
            f'ㄱ. {topic}은(는) {ctx["sub_subject"]}의 주요 분석 대상이다.\n'
            f'ㄴ. {topic}의 분석은 관련 변수와 가정의 명시가 필수적이다.\n'
            f'ㄷ. {topic}은(는) 측정·분석이 불가능한 추상적 개념이다.\n'
            f'ㄹ. {topic}의 적용은 분석자의 정치적 신념에 의해 결정된다.'
        ),
        'options': [
            'ㄱ, ㄴ',
            'ㄱ, ㄷ',
            'ㄴ, ㄷ',
            'ㄴ, ㄹ',
            'ㄱ, ㄴ, ㄹ',
        ],
        'answer': '1',
        'explanation': (
            f'ㄱㄴ만 옳다.\n'
            f'ㄱ ✓: {topic}은(는) {ctx["sub_subject"]}의 주요 분석 대상이다.\n'
            f'ㄴ ✓: 모든 경제학 분석은 관련 변수와 가정의 명시가 필수적이다.\n'
            f'ㄷ ✗: {topic}은(는) 다양한 방법으로 측정·분석이 가능하다.\n'
            f'ㄹ ✗: 학문적 분석은 객관적 이론·자료에 기반하며 정치적 신념과 무관해야 한다.'
        ),
        'qtype': '보기 결합형',
    }


def q_combo_ㄱㄴㄷ_b(topic, ctx):
    """난이도 3: 보기 결합 B"""
    return {
        'question': (
            f'{topic}의 분석 방법에 관한 설명 중 옳은 것을 모두 고른 것은?\n\n'
            f'ㄱ. 부분균형분석으로 {topic}의 한 측면을 분리해 살펴볼 수 있다.\n'
            f'ㄴ. 일반균형분석은 {topic}이(가) 다른 시장에 미치는 파급효과까지 분석한다.\n'
            f'ㄷ. {topic}의 분석에는 비교정태분석이 적용될 수 있다.\n'
            f'ㄹ. {topic}은(는) 동태적 분석을 절대 적용할 수 없다.'
        ),
        'options': [
            'ㄱ, ㄴ',
            'ㄴ, ㄷ',
            'ㄱ, ㄴ, ㄷ',
            'ㄱ, ㄷ, ㄹ',
            'ㄱ, ㄴ, ㄷ, ㄹ',
        ],
        'answer': '3',
        'explanation': (
            f'ㄱㄴㄷ 옳다.\n'
            f'ㄱ ✓: 부분균형분석은 다른 조건 일정 가정으로 한 시장만 분리해 분석한다.\n'
            f'ㄴ ✓: 일반균형분석은 모든 시장의 상호작용을 종합 분석한다.\n'
            f'ㄷ ✓: 비교정태분석은 외생변수 변화에 따른 균형 변동을 분석하며 {topic}에 적용 가능하다.\n'
            f'ㄹ ✗: 동태분석은 {topic}을(를) 포함한 모든 경제 변수의 시간 경로 분석에 적용 가능하다.'
        ),
        'qtype': '보기 결합형',
    }


def q_scholar(topic, ctx):
    """난이도 3: 학자 매칭"""
    return {
        'question': f'{topic}의 분석과 관련된 일반적 접근법에 관한 설명으로 옳은 것은?',
        'options': [
            f'고전학파의 시장 자율 조정 원리는 {topic}과 무관하다.',
            f'신고전학파의 한계분석과 일반균형이론은 {topic} 분석에도 적용된다.',
            f'케인즈학파의 단기 가격 경직성 가정은 모든 학파에서 거부된다.',
            f'행동경제학은 합리적 선택 가정만 사용한다.',
            f'마르크스 경제학은 시장 분석을 완전히 거부한다.',
        ],
        'answer': '2',
        'explanation': f'신고전학파(마샬·왈라스 등)의 한계분석과 일반균형이론은 {topic}을(를) 포함한 경제학 다수 영역의 분석에 적용되는 기본 도구이다. 다른 선택지는 각 학파의 입장을 잘못 진술한 것이다.',
        'qtype': '옳은 것 고르기',
    }


def q_impact(topic, ctx):
    """난이도 3: 영향 분석"""
    return {
        'question': f'{topic}의 변동이 경제 변수에 미치는 영향으로 옳은 것은?',
        'options': [
            f'{topic}의 변동은 다른 경제 변수와 무관하게 발생한다.',
            f'{topic}의 변동은 항상 동일한 크기로 모든 변수에 동일 영향을 미친다.',
            f'{topic}의 변동은 {ctx["sec_topic"]} 영역의 관련 변수에 이론적으로 예측 가능한 방향과 크기로 영향을 미친다.',
            f'{topic}의 변동은 측정 불가능하여 분석의 의미가 없다.',
            f'{topic}의 변동은 정부 정책에만 영향을 미치고 시장에는 영향이 없다.',
        ],
        'answer': '3',
        'explanation': f'{topic}의 변동은 {ctx["sec_topic"]} 영역의 관련 변수에 이론적으로 예측 가능한 방향(증가·감소·이동 등)과 크기(탄력성·승수 등)로 영향을 미친다. 비교정태분석으로 그 효과를 정량적으로 분석할 수 있다.',
        'qtype': '옳은 것 고르기',
    }


def q_method(topic, ctx):
    """난이도 3: 분석 방법"""
    return {
        'question': f'{topic}을(를) 분석할 때 사용되는 일반적 방법으로 옳지 않은 것은?',
        'options': [
            '이론 모형을 통한 연역적 추론',
            '실증 자료를 통한 가설 검증',
            '비교정태분석을 통한 균형 변동 분석',
            '관련 학자의 정치적 견해 채택',
            '수학적·통계적 도구의 활용',
        ],
        'answer': '4',
        'explanation': f'{topic} 분석에는 ① 이론 모형, ② 실증 검증, ③ 비교정태분석, ④ 수학·통계적 도구 등 객관적 방법이 사용된다. 학자의 정치적 견해 채택은 객관성을 해치는 분석 방법이 아니다.',
        'qtype': '틀린 것 고르기',
    }


def q_assumption_role(topic, ctx):
    """난이도 3: 가정의 역할"""
    return {
        'question': f'{topic}의 분석에서 가정(assumption)의 역할로 옳지 않은 것은?',
        'options': [
            '복잡한 현실을 단순화하여 분석 가능하게 만든다.',
            '분석의 초점을 명확히 한다.',
            '결론의 적용 범위를 한정한다.',
            '모형의 검증 가능성을 높인다.',
            '분석의 객관성을 완전히 제거한다.',
        ],
        'answer': '5',
        'explanation': f'가정은 분석의 단순화·초점화·범위 한정·검증 가능성 향상의 역할을 한다. 가정 자체가 분석의 객관성을 제거하는 것은 아니며, 오히려 객관적 분석의 출발점이 된다.',
        'qtype': '틀린 것 고르기',
    }


def q_data_interpret(topic, ctx):
    """난이도 3: 자료 해석"""
    return {
        'question': (
            f'다음 자료에 기반할 때 {topic}에 관한 해석으로 옳은 것은?\n\n'
            f'[자료] {ctx["sub_subject"]} > {ctx["ch_topic"]} 영역의 표준 분석틀:\n'
            f'- 핵심 변수: {topic} 및 관련 변수\n'
            f'- 분석 방법: 이론 모형 + 실증 검증\n'
            f'- 적용 가정: 합리적 의사결정, 시장 균형'
        ),
        'options': [
            f'{topic}은(는) 자료 분석과 무관한 추상적 개념이다.',
            f'{topic}은(는) 표준 분석틀에 따라 이론 모형과 실증 검증으로 분석된다.',
            f'{topic}은(는) 가정 없이 분석되어야 한다.',
            f'{topic}은(는) 비합리적 의사결정만 가정한다.',
            f'{topic}은(는) 시장 균형을 부정하는 개념이다.',
        ],
        'answer': '2',
        'explanation': f'자료에 따르면 {topic}은(는) 표준 분석틀(이론 모형 + 실증 검증, 합리성·균형 가정)을 통해 체계적으로 분석되는 {ctx["ch_topic"]} 영역의 핵심 변수이다.',
        'qtype': '옳은 것 고르기',
    }


def q_combo_ㄱㄴㄷ_c(topic, ctx):
    """난이도 3: 보기 결합 C"""
    return {
        'question': (
            f'{topic}의 일반적 적용에 관한 설명 중 옳은 것을 모두 고른 것은?\n\n'
            f'ㄱ. {topic}은(는) 이론 모형의 가정 하에서 분석된다.\n'
            f'ㄴ. {topic}의 실증 분석에는 통계 자료가 활용된다.\n'
            f'ㄷ. {topic}의 결론은 가정의 적정성에 의존한다.\n'
            f'ㄹ. {topic}의 정책적 함의는 규범경제학의 영역에 속한다.'
        ),
        'options': [
            'ㄱ, ㄴ',
            'ㄱ, ㄴ, ㄷ',
            'ㄱ, ㄴ, ㄷ, ㄹ',
            'ㄴ, ㄷ',
            'ㄱ, ㄷ',
        ],
        'answer': '3',
        'explanation': (
            f'ㄱㄴㄷㄹ 모두 옳다.\n'
            f'ㄱ ✓: 모든 경제 이론은 가정 하에서 분석된다.\n'
            f'ㄴ ✓: 실증 분석은 통계 자료를 활용한다.\n'
            f'ㄷ ✓: 결론은 가정의 적정성에 좌우된다.\n'
            f'ㄹ ✓: 정책적 함의(가치 판단)는 규범경제학의 영역이다.'
        ),
        'qtype': '보기 결합형',
    }


def q_period(topic, ctx):
    """난이도 3: 시기적 차이"""
    return {
        'question': f'{topic}의 단기·장기 분석에 관한 설명으로 옳은 것은?',
        'options': [
            f'{topic}은(는) 단기와 장기 구분 없이 동일한 결과를 보인다.',
            f'{topic}은(는) 단기에는 가격 경직성, 장기에는 가격 신축성을 일반적으로 가정한다.',
            f'{topic}은(는) 항상 장기 분석만 가능하다.',
            f'{topic}은(는) 단기 분석만 가능하며 장기는 의미가 없다.',
            f'{topic}의 단기·장기 구분은 모든 학파에서 동일하다.',
        ],
        'answer': '2',
        'explanation': f'경제학에서 단기는 일부 변수가 고정·경직적이고, 장기는 모든 변수가 신축적으로 조정된다. {topic} 분석도 단기에는 가격 경직성을 가정할 수 있고 장기에는 시장이 완전히 조정된다고 분석한다.',
        'qtype': '옳은 것 고르기',
    }


# 난이도 4 (5개)

def q_apply_calc(topic, ctx):
    """난이도 4: 응용 계산"""
    return {
        'question': (
            f'{topic}과(와) 관련된 다음 자료를 활용한 분석으로 가장 적절한 것은?\n\n'
            f'[자료]\n'
            f'- {ctx["sec_topic"]} 영역의 표준 모형 적용\n'
            f'- 핵심 변수의 초기값 X₀\n'
            f'- 외생변수의 변화 Δ\n'
            f'- 모형 계수: 합리적 가정 하의 표준 추정치\n\n'
            f'(단, 모든 분석은 합리성·균형 가정 하에서 이루어진다.)'
        ),
        'options': [
            f'{topic}의 분석은 자료의 의미와 무관하게 임의로 결정된다.',
            f'{topic}의 분석은 자료를 활용해 비교정태분석을 시행하며, 외생변수 변화에 따른 균형 변동의 방향과 크기를 예측한다.',
            f'{topic}의 분석은 모형을 무시하고 직관에만 의존한다.',
            f'{topic}의 분석은 가정의 검토 없이 시행된다.',
            f'{topic}의 분석은 정량적 추정이 불가능하다.',
        ],
        'answer': '2',
        'explanation': f'{topic}의 응용 분석은 표준 모형 + 자료 + 외생변수 변화의 조합으로 비교정태분석을 시행한다. 모형의 가정 하에서 외생변수 변화가 균형 변수에 미치는 방향과 크기를 정량적으로 예측하는 것이 표준 절차이다.',
        'qtype': '옳은 것 고르기',
    }


def q_advanced_combo(topic, ctx):
    """난이도 4: 종합 보기 결합"""
    return {
        'question': (
            f'{topic}의 종합적 분석에 관한 다음 설명 중 옳은 것을 모두 고른 것은?\n\n'
            f'ㄱ. 부분균형분석은 다른 시장의 영향을 무시하므로 정확하지 않을 수 있다.\n'
            f'ㄴ. 일반균형분석은 모든 시장의 동시 균형을 분석하므로 종합적이다.\n'
            f'ㄷ. 비교정태분석은 균형 도달 과정을 분석하므로 동태적이다.\n'
            f'ㄹ. 동태분석은 시간을 명시적으로 도입하여 변수의 변화 경로를 추적한다.\n'
            f'ㅁ. {topic}은(는) 부분균형·일반균형·동태 분석 모두 적용 가능하다.'
        ),
        'options': [
            'ㄱ, ㄴ, ㄷ',
            'ㄱ, ㄴ, ㄹ, ㅁ',
            'ㄴ, ㄷ, ㄹ',
            'ㄱ, ㄷ, ㄹ, ㅁ',
            'ㄱ, ㄴ, ㄷ, ㄹ, ㅁ',
        ],
        'answer': '2',
        'explanation': (
            f'ㄱㄴㄹㅁ 옳다.\n'
            f'ㄱ ✓: 부분균형은 다른 시장의 파급효과를 간과한다.\n'
            f'ㄴ ✓: 일반균형은 모든 시장의 상호작용을 종합 분석한다.\n'
            f'ㄷ ✗: 비교정태분석은 균형 도달 과정을 다루지 않고 균형점 비교만 한다. 도달 과정은 동태분석의 영역이다.\n'
            f'ㄹ ✓: 동태분석은 시간을 명시적으로 도입한다.\n'
            f'ㅁ ✓: {topic}은(는) 모든 분석 방법의 적용 대상이다.'
        ),
        'qtype': '보기 결합형',
    }


def q_advanced_apply(topic, ctx):
    """난이도 4: 응용 시나리오"""
    return {
        'question': (
            f'{topic}이(가) 변동했을 때의 영향을 분석한 다음 사례 중 가장 적절한 것은?\n\n'
            f'[사례] {ctx["sec_topic"]} 영역에서 {topic}의 외생적 변화가 발생하였다. '
            f'관련 변수들 간 표준 함수관계와 합리성 가정 하에서 균형의 변동을 분석하시오.'
        ),
        'options': [
            f'{topic}의 변동은 다른 변수에 영향을 미치지 않는다.',
            f'{topic}의 변동은 임의의 무작위 방향으로 다른 변수에 영향을 미친다.',
            f'{topic}의 변동은 표준 함수관계와 합리성 가정 하에서 이론적으로 예측 가능한 방향과 크기로 균형을 이동시킨다.',
            f'{topic}의 변동은 측정 불가능하며 분석의 의미가 없다.',
            f'{topic}의 변동은 모든 시장에 정확히 동일한 크기로 영향을 미친다.',
        ],
        'answer': '3',
        'explanation': f'표준 함수관계와 합리성 가정 하에서 {topic}의 외생적 변화는 비교정태분석에 의해 균형 변수에 예측 가능한 방향(증가·감소)과 크기(탄력성·승수)로 영향을 미친다. 이는 경제학의 핵심 분석 방법이다.',
        'qtype': '옳은 것 고르기',
    }


def q_wrong_advanced(topic, ctx):
    """난이도 4: 잘못된 응용"""
    return {
        'question': f'{topic}을(를) 응용 분석할 때 발생할 수 있는 오류로 옳지 않은 것은?',
        'options': [
            '모형 가정의 비현실성 간과',
            '외생변수와 내생변수의 혼동',
            '인과관계와 상관관계의 혼동',
            '단기와 장기 효과의 구별 부재',
            '객관적 자료 수집·분석',
        ],
        'answer': '5',
        'explanation': f'{topic}의 응용 분석에서 ①가정의 비현실성, ②변수 혼동, ③인과·상관 혼동, ④시기 구별 부재는 흔한 오류이다. 그러나 객관적 자료 수집·분석은 올바른 분석 절차이며 오류가 아니다.',
        'qtype': '틀린 것 고르기',
    }


def q_school_comparison(topic, ctx):
    """난이도 4: 학파 비교"""
    return {
        'question': f'{topic}에 관한 학파별 견해의 비교로 옳은 것은?',
        'options': [
            f'모든 학파가 {topic}에 대해 완전히 동일한 견해를 가진다.',
            f'학파별로 {topic}의 분석 방법·가정·정책 함의에 차이가 있을 수 있으며, 이는 분석의 다양성을 보장한다.',
            f'{topic}은(는) 특정 학파의 전유물이며 다른 학파는 다룰 수 없다.',
            f'학파별 견해 차이는 학문적 발전을 저해한다.',
            f'학파별 견해는 정치적 신념으로만 결정된다.',
        ],
        'answer': '2',
        'explanation': f'학파별로 {topic}에 대한 분석 방법(부분균형·일반균형 등), 가정(가격 신축성·경직성 등), 정책 함의(자유방임·정부 개입 등)에 차이가 있을 수 있다. 이러한 다양성은 학문적 논의의 풍부함과 분석의 깊이를 보장한다.',
        'qtype': '옳은 것 고르기',
    }


# 난이도 5 (3개)

def q_scenario_synthesis(topic, ctx):
    """난이도 5: 종합 시나리오"""
    return {
        'question': (
            f'{topic}을(를) 활용한 다음 종합적 시나리오 분석으로 가장 적절한 것은?\n\n'
            f'[시나리오]\n'
            f'1. {ctx["sec_topic"]} 영역에서 {topic}이(가) 외생적으로 변화한다.\n'
            f'2. 단기에는 일부 변수의 경직성으로 균형 조정이 부분적이다.\n'
            f'3. 장기에는 모든 변수가 신축적으로 조정되어 새로운 균형에 도달한다.\n'
            f'4. 일반균형분석에서 다른 시장으로의 파급효과도 함께 발생한다.\n\n'
            f'(단, 모든 분석은 합리성·균형 가정 하에서 이루어지며, 비교정태분석과 동태분석을 모두 활용한다.)'
        ),
        'options': [
            f'단기와 장기 모두 {topic}의 변화는 균형에 영향을 미치지 않는다.',
            f'{topic}의 변화는 단기에는 가격 경직성으로 부분적 균형 조정, 장기에는 완전 신축성으로 새로운 균형 도달, 일반균형분석에서 다른 시장에도 파급효과를 미친다. 비교정태분석(균형점 비교) + 동태분석(조정 경로)의 종합 적용이 적절하다.',
            f'{topic}의 변화는 단기에만 영향을 미치고 장기에는 사라진다.',
            f'{topic}의 변화는 일반균형분석을 적용할 수 없다.',
            f'{topic}의 변화는 비교정태분석만 사용 가능하다.',
        ],
        'answer': '2',
        'explanation': (
            f'시나리오의 종합 분석:\n'
            f'① 단기: 가격·임금 경직성으로 인한 부분적 균형 조정 (케인즈학파 관점)\n'
            f'② 장기: 신축성 회복으로 새로운 균형 도달 (고전·신고전학파 관점)\n'
            f'③ 일반균형: 한 시장의 변화가 다른 시장으로 파급 (왈라스 일반균형이론)\n'
            f'④ 분석 방법: 비교정태분석(균형점 비교) + 동태분석(시간 경로) 종합 적용\n'
            f'이는 현대 경제학의 표준 분석틀이며 {topic}에도 적용된다.'
        ),
        'qtype': '옳은 것 고르기',
    }


def q_advanced_synthesis(topic, ctx):
    """난이도 5: 학파 종합 시나리오"""
    return {
        'question': (
            f'{topic}과(와) 관련된 학파별 분석을 종합한 다음 설명 중 옳은 것을 모두 고른 것은?\n\n'
            f'A. 고전학파: 시장 자율 조정으로 {topic}의 균형이 자동 회복된다.\n'
            f'B. 케인즈학파: 단기 가격 경직성으로 {topic}의 균형이 자동 회복되지 않을 수 있다.\n'
            f'C. 신고전학파 종합: 단기는 케인즈, 장기는 고전학파 분석을 결합한다.\n'
            f'D. 새고전학파: 합리적 기대 하에서 예측된 정책은 {topic}에 영향을 미치지 못한다.\n'
            f'E. 새케인즈학파: {topic}의 가격 경직성을 메뉴비용·효율임금 등 미시적 기초로 설명한다.\n'
            f'F. 행동경제학: {topic}의 분석에서 합리성을 완전히 부정한다.'
        ),
        'options': [
            'A, B, C, D',
            'A, B, C, D, E',
            'A, B, C, F',
            'A, B, D, E',
            'A, B, C, D, E, F',
        ],
        'answer': '2',
        'explanation': (
            f'A·B·C·D·E 옳다.\n'
            f'A ✓: 고전학파의 시장 자율 조정.\n'
            f'B ✓: 케인즈학파의 단기 경직성.\n'
            f'C ✓: 신고전학파 종합(neoclassical synthesis)은 단기 케인즈 + 장기 고전을 결합.\n'
            f'D ✓: 새고전학파(루카스)의 정책무력성 정리.\n'
            f'E ✓: 새케인즈학파의 미시적 기초(메뉴비용·효율임금).\n'
            f'F ✗: 행동경제학은 합리성을 완전히 부정하지 않고 제한된 합리성(bounded rationality)과 휴리스틱·편향으로 보완한다.'
        ),
        'qtype': '보기 결합형',
    }


def q_full_synthesis(topic, ctx):
    """난이도 5: 전체 종합"""
    return {
        'question': (
            f'{topic}에 관한 다음 종합 분석 중 가장 적절한 것은?\n\n'
            f'[종합 분석 요구]\n'
            f'1. {topic}의 정의·분류·구성요소\n'
            f'2. 관련 학파별 분석 방법·가정·정책 함의\n'
            f'3. 부분균형·일반균형·동태분석의 적용\n'
            f'4. 실증경제학·규범경제학의 구분과 적용\n'
            f'5. 단기·장기 효과의 비교\n\n'
            f'(단, {topic}을(를) {ctx["sub_subject"]} > {ctx["ch_topic"]} > {ctx["sec_topic"]} 영역의 핵심 개념으로 종합적으로 분석한다.)'
        ),
        'options': [
            f'{topic}은(는) 정의·분류만 다루며 학파별·분석방법별 차이가 없다.',
            f'{topic}은(는) 학파에 따라 분석 방법·가정·정책 함의가 다르며, 부분균형·일반균형·동태분석 모두 적용 가능하고, 실증과 규범의 구분과 단기·장기 차이까지 종합적으로 분석할 수 있는 {ctx["sub_subject"]}의 핵심 개념이다.',
            f'{topic}은(는) 한 학파의 한 가지 분석방법으로만 다룰 수 있다.',
            f'{topic}은(는) 실증경제학에만 속하고 규범경제학과 무관하다.',
            f'{topic}은(는) 단기 분석에만 적용되며 장기는 의미가 없다.',
        ],
        'answer': '2',
        'explanation': (
            f'{topic}은(는) {ctx["sub_subject"]} > {ctx["ch_topic"]} > {ctx["sec_topic"]} 영역의 핵심 개념으로 다음과 같은 종합적 분석이 가능하다:\n'
            f'① 정의·분류·구성요소가 명확히 체계화됨\n'
            f'② 학파별로 다양한 견해 (고전·신고전·케인즈·새고전·새케인즈·행동경제학 등)\n'
            f'③ 분석 방법의 다양성 (부분균형·일반균형·정태·동태·비교정태)\n'
            f'④ 실증경제학(사실 분석)과 규범경제학(정책 평가) 모두 적용\n'
            f'⑤ 단기(부분적 조정)와 장기(완전 조정) 효과의 구분\n'
            f'이러한 다층적·종합적 분석이 현대 경제학의 표준 접근법이다.'
        ),
        'qtype': '옳은 것 고르기',
    }


# 난이도별 템플릿 배열
TEMPLATES = {
    1: [q_definition, q_concept_correct, q_wrong_one, q_basic_assumption, q_belong_field],
    2: [q_classification, q_application, q_component, q_correct_one_simple,
        q_factor_not, q_feature_wrong, q_general_explanation],
    3: [q_comparison, q_combo_ㄱㄴㄷ_a, q_combo_ㄱㄴㄷ_b, q_scholar, q_impact,
        q_method, q_assumption_role, q_data_interpret, q_combo_ㄱㄴㄷ_c, q_period],
    4: [q_apply_calc, q_advanced_combo, q_advanced_apply, q_wrong_advanced, q_school_comparison],
    5: [q_scenario_synthesis, q_advanced_synthesis, q_full_synthesis],
}


def generate_chapter_items(sub_name, chapters):
    """한 과목의 모든 chapter > section > item을 순회하면서 ID 부여."""
    result = []
    for ch_idx, ch in enumerate(chapters, 1):
        sec_idx = 0
        for sec in ch.get('sections', []):
            sec_idx += 1
            for item_idx, item in enumerate(ch.get('sections', [])[sec_idx-1].get('items', []), 1):
                result.append({
                    'sub_subject': sub_name,
                    'chapter': ch['name'],
                    'section': sec['name'],
                    'item': item['name'],
                    'ch_idx': ch_idx,
                    'sec_idx': sec_idx,
                    'item_idx': item_idx,
                })
    return result


def generate_questions_for_item(item_info):
    """한 관에 30문제 생성."""
    topic = extract_topic(item_info['item'])
    ctx = {
        'sub_subject': item_info['sub_subject'],
        'ch_topic': extract_chapter_topic(item_info['chapter']),
        'sec_topic': extract_section_topic(item_info['section']),
    }
    sub_slug = SUB_SLUG[item_info['sub_subject']]
    ch_num = item_info['ch_idx']
    sec_num = item_info['sec_idx']
    item_num = item_info['item_idx']

    questions = []
    seq = 1
    for difficulty in [1, 2, 3, 4, 5]:
        templates = TEMPLATES[difficulty]
        count = DIFFICULTY_COUNTS[difficulty]
        for i in range(count):
            tmpl = templates[i % len(templates)]
            q_data = tmpl(topic, ctx)
            qid = make_id(sub_slug, ch_num, sec_num, item_num, seq)
            questions.append({
                'id': qid,
                'difficulty': difficulty,
                'question_type': q_data['qtype'],
                'question': q_data['question'],
                'options': q_data['options'],
                'answer': q_data['answer'],
                'explanation': q_data['explanation'],
            })
            seq += 1
    return questions


def write_item_file(item_info, questions):
    sub_slug = SUB_SLUG[item_info['sub_subject']]
    ch_num = item_info['ch_idx']
    sec_num = item_info['sec_idx']
    item_num = item_info['item_idx']
    fn = f'{sub_slug}-ch{ch_num:02d}-sec{sec_num:02d}-item{item_num:02d}.json'
    out_path = OUT_DIR / fn
    data = {
        'meta': {
            'subject': '경제학원론',
            'sub_subject': item_info['sub_subject'],
            'chapter': item_info['chapter'],
            'section': item_info['section'],
            'item': item_info['item'],
            'source': 'practice-set',
            'version': 'v1',
            'created': '2026-05-31',
            'count': len(questions),
        },
        'questions': questions,
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out_path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(TAX, encoding='utf-8') as f:
        tax = json.load(f)

    total_items = 0
    total_questions = 0
    for sub_name, chapters in tax['경제학원론']['subjects'].items():
        items = generate_chapter_items(sub_name, chapters)
        for item_info in items:
            qs = generate_questions_for_item(item_info)
            write_item_file(item_info, qs)
            total_items += 1
            total_questions += len(qs)
        print(f'  {sub_name}: {len(items)}관 처리')

    print(f'\n총 {total_items}관 × {total_questions // total_items}문제 = {total_questions}문제 생성')
    print(f'저장: {OUT_DIR}/*.json ({total_items} 파일)')


if __name__ == '__main__':
    main()
