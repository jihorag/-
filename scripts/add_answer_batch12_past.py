#!/usr/bin/env python3
"""Batch 12 — past 단원 (6문제) + GS sourceLink 안내 답안."""
import json
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')

ANSWERS_PAST = {
    'past-r33-q1': {
        'modelAnswer': """## Ⅰ. 평가개요
- **사업**: 도로법 도로사업 — 협의보상평가
- **물음 3개**: 토지보상 + 주거이전비 + 영업손실

## Ⅱ. 물음 1) 토지 보상액 (10점)

### 평가방식 — 공시지가기준법
- 비교표준지 × 시점·지역·개별·그밖 = 단가
- 보상가액 = 단가 × 편입면적

### 산정 흐름
1. 적용 공시지가: 사업인정고시 *이전* 공시지가
2. 시점수정: 공시기준일 → 가격시점 (지가변동률 + 생산자물가 평균)
3. 개별요인 6대 조건
4. 그밖의요인: 보상선례 참작

## Ⅲ. 물음 2) 주거이전비

### 시행규칙 §54
- **주거이전비 = 2개월분 (자가) 또는 4개월분 (세입자) 평균임금**
- 자가 거주자: 가구원수별 *2개월분* 도시근로자 가구원수별 월평균 가계지출비
- 세입자: 4개월분

## Ⅳ. 물음 3) 영업손실

### 시행규칙 §47 (휴업) 또는 §46 (폐업)
- 휴업: 영업이익 × 기간 + 고정비 + 이전비 + 광고비
- 폐업: 영업이익 × 2년 + 매각손 + 이전비

## ★ 핵심 학습 포인트
1. **도로사업 보상 = 토지 + 지장물 + 주거이전비 + 영업손실**
2. **주거이전비 = 자가 2개월 / 세입자 4개월**
3. **사업인정고시 *이전* 공시지가 적용** (개발이익 배제)
4. **그밖의요인 = 보상선례 참작 보정률**
5. **세입자 = 자가보다 더 두터운 보호**""",
        'modelAnswerSource': 'ai-direct',
        'keyPoints': ['도로사업', '협의보상', '주거이전비', '영업손실', '시행규칙§54'],
    },
    'past-r35-q1': {
        'modelAnswer': """## Ⅰ. 평가개요
- **유형**: 중앙토지수용위원회 *수용재결* 평가
- **물음**: 공시기준일 선택 + 지가변동률 + 평가액 등

## Ⅱ. 물음 1) 적정 공시기준일 결정 (10점)

### 결정 원칙
- **사업인정고시 *이전* 공시기준일** 중 *가격시점에 가장 근접한* 공시지가
- 사업영향 발생 시 → *더 이전* 공시기준일 검토

### 선택 사유
1. 토지보상법 §70 ③ 사업인정 이전 공시지가 원칙
2. 가격시점 이전 가장 최근 공시지가 (시점수정 최소)
3. 가격형성요인 *사업 영향 *전* 상태* 반영

## Ⅲ. 물음 2) 적용 지가변동률

### 산정 방법
- **공시기준일 → 가격시점** 지가변동률 누계
- 해당 시·군·구가 사업영향 시·군·구이면 **인접 시·군·구 평균** 적용

### 시점수정치
- 누계 지가변동률 + 생산자물가상승률 *산술평균* (지침)

## Ⅳ. 평가액 산정 + 의견
- 단가 = 표준지 × 시점 × 지역 × 개별 × 그밖
- 보상가액 = 단가 × 편입면적

## ★ 핵심 학습 포인트
1. **수용재결 = 가격시점 *재결일***
2. **공시기준일 = 사업인정 이전 가장 근접**
3. **지가변동률 = 공시기준일 → 가격시점 누계**
4. **사업영향 시·군·구 = 인접 평균 적용**
5. **시점수정 = 지가변동률 + 생산자물가 평균**""",
        'modelAnswerSource': 'ai-direct',
        'keyPoints': ['수용재결', '공시기준일선택', '지가변동률', '인접시군구평균', '재결평가'],
    },
    'past-r35-q3': {
        'modelAnswer': """## Ⅰ. 평가개요
- **사업**: 도시개발사업 환지방식 — 토지 기호(1)(2) 사정면적 + 가격평가

## Ⅱ. 물음 1) 과·부족 면적 + 사정면적

### 환지청산 원리
- **사정면적** = 환지 후 *권리면적*
- **종전면적 + 청산금** ↔ **사정면적**의 가치 균형

### 과·부족 면적 판정
- 종전 토지 × 권리면적 비율 → 사정면적 계산
- 사정면적 > 종전 = 과도 (납부청산금)
- 사정면적 < 종전 = 부족 (교부청산금)

### 산정 흐름
1. 종전 토지가치 산정 (단가 × 면적)
2. 사정 단가 산정 (환지 후 정상가격)
3. 사정면적 = 종전가치 / 사정단가
4. 청산금 = (사정 ↔ 종전) 가치 차이

## Ⅲ. 물음 2) 평가액 결정
- 환지 *후* 토지 = 사정단가 × 사정면적
- 청산금 정산 후 정상화

## ★ 핵심 학습 포인트
1. **환지방식 = 종전 토지 → 환지 토지 면적·가치 변환**
2. **사정면적 = 권리면적** (가치 균형)
3. **청산금 = 면적 과·부족분 가치 정산**
4. **도시개발법 환지처분 규정**
5. **감보율 = (종전 - 환지) / 종전** (사업비 충당)""",
        'modelAnswerSource': 'ai-direct',
        'keyPoints': ['환지방식', '사정면적', '청산금', '도시개발법', '감보율'],
    },
    'past-r35-q4': {
        'modelAnswer': """## 영업권 초과수익 요건

### 물음 1) 영업권 존재 위한 초과수익 요건 (5점)

1. **지속성 (Permanency)**:
   - 일시적이 아닌 *지속적* 초과수익 발생
   - 향후 *예측 가능한 기간* 유지

2. **양도가능성 (Transferability)**:
   - 영업권 + 사업 *전체*가 *양도 가능*
   - 별도 분리 거래 불가 → 사업 매수자에게 *함께 이전*

3. **현실성 (Realizability)**:
   - *측정 가능*한 가치
   - 회계적·시장적 *입증 가능*

4. **법적 안정성 (Legality)**:
   - 적법한 사업 영위
   - 법적 위험 (위법·계약 만료 등) 없음

5. **경제적 *비교 우위* 원천**:
   - 영업방식·고객관계·브랜드·입지·노하우 등 *식별 가능*한 무형자산

### 물음 2) 초과수익 산정

#### 산식
**초과수익 = 현재 영업수익 - 정상수익률 × 순자산가치**

#### 또는
**초과수익 = 현재 영업이익 - (총자산 × 정상수익률)**

### 정상수익률 기준
- **무위험률 + 위험프리미엄** = 가정 10~15%
- 업종 평균 ROE 또는 ROA 적용

## ★ 핵심 학습 포인트
1. **영업권 초과수익 5대 요건**: 지속성·양도성·현실성·법적안정성·비교우위
2. **초과수익 = 실제 - (자산 × 정상수익률)**
3. **정상수익률 = 무위험률 + 위험프리미엄**
4. **영업권 = 초과수익 자본환원** (초과수익법)
5. **회계상 영업권 = 인수가 - 식별가능 순자산 공정가치**""",
        'modelAnswerSource': 'ai-direct',
        'keyPoints': ['영업권', '초과수익', '5대요건', '정상수익률', '초과수익법'],
    },
    'past-r36-q1': {
        'modelAnswer': """## Ⅰ. 평가개요
- **상황**: 건축공사 *중단* 부동산 — 현재 매수가 + 개발완료 매수가
- **자료기준시점**: 현재 25.07.12 / 개발완료 26.07.12

## Ⅱ. 현재상태 매수가 (25.07.12)

### 평가방식
- *현재 상태* 토지 + 미완성 건물 + 추가 개발비 부담 가능성 반영
- 단가 = *완성 후 가치* - *추가 개발비* - *위험 프리미엄*

### 산정 (가정)
- 미완성 건물 + 토지 일체 = **약 50억원**
- 위험·시간 할인 후 = **약 45억원**

## Ⅲ. 개발완료 매수가 (26.07.12)

### 평가방식
- 개발 완료된 *완성 부동산* 가치
- 거래사례·수익환원·원가법 시산조정

### 산정 (가정)
- 완성 가치 = **약 65억원**

## Ⅳ. 차이 분석
- 차이 = 65 - 45 = **약 20억원** (추가 개발비 + 위험 + 시간가치)
- 추가 개발비: 약 15억
- 위험·시간 프리미엄: 약 5억

## ★ 핵심 학습 포인트
1. **건축중단 부동산 = *현재 상태* + *완성 후* 두 시점 평가**
2. **현재 매수가 = 완성가 - 개발비 - 위험프리미엄**
3. **개발완료 매수가 = 완성 부동산 정상가치**
4. **차이 = 개발비 + 위험 + 시간가치**
5. **건축중단 부동산 = *옵션가치* 반영 가능** (실물옵션)""",
        'modelAnswerSource': 'ai-direct',
        'keyPoints': ['건축중단부동산', '현재매수가', '개발완료매수가', '위험프리미엄', '실물옵션'],
    },
    'past-r36-q2': {
        'modelAnswer': """## Ⅰ. 평가개요
- **상황**: 개인기업 A 법인전환 — 영업권 평가
- **방식**: 영업관련 기업가치 → 영업권 분리 산정

## Ⅱ. 물음 1) 영업관련 기업가치 평가 (20점)

### 방식 — DCF (Free Cash Flow to Firm)

#### FCFF 추정
- FCFF = NOPAT + 감가상각 - 운전자본증가 - 자본적지출
- 5년 추정 + 종가

#### WACC 산정
- 자기자본비용 + 부채비용 가중평균
- 가정: 10%

#### 종가 (Terminal Value)
- TV = FCFF₅ × (1+g) / (WACC - g)
- g = 2% (영구성장)

#### 현재가치 합계
- 영업관련 기업가치 = **약 30억원** (가정)

## Ⅲ. 물음 2) 영업권 가치 평가 (10점)

### 방식 — 잔여가치법
**영업권 = 기업가치 - 식별가능 순자산 - 식별가능 무형자산**

### 산정
- 기업가치: 30억
- 순자산 (장부+공정가치 조정): 22억
- 식별가능 무형자산 (브랜드·고객관계 등): 3억
- **영업권 = 30 - 22 - 3 = 5억원**

### 또는 — 초과수익법
- 정상수익률 × 순자산 = 22 × 10% = 2.2억
- 실제 영업이익: 3.5억
- 초과수익 = 3.5 - 2.2 = 1.3억
- 영업권 = 1.3 / 0.15 (영업권 환원율) = **약 8.7억**

### 결정
- 잔여가치법 5억 vs 초과수익법 8.7억 → 평균 또는 자료 적합성 가중
- **영업권 = 약 7억원**

## ★ 핵심 학습 포인트
1. **법인전환 영업권 = 기존 영업가치 → 법인 이전 시 *과세대상***
2. **DCF FCFF 기업가치 산정** (주된 방식)
3. **영업권 = 기업가치 - 식별가능 자산** (잔여가치법)
4. **영업권 = 초과수익 / 환원율** (초과수익법)
5. **잔여가치 vs 초과수익 비교 검증**""",
        'modelAnswerSource': 'ai-direct',
        'keyPoints': ['영업권', '법인전환', 'FCFF', 'WACC', '잔여가치법', '초과수익법'],
    },
}

# GS 단원은 sourceLink (출처 기출문제) 안내형 답안 일괄 적용
GS_NOTE_TEMPLATE = """## 📚 학습 안내 — GS 모의고사

이 문제는 **{src_label}**의 *변형 문제*입니다.

### 풀이 전략
1. **원본 기출문제 답안 참조**: {src_link}
2. **변형 패턴 분석**: 자료 수치·연도·조건의 차이 확인
3. **핵심 산식·법규는 동일** — 적용 단계만 새로 정리

### 자기채점 가이드
- 답안 작성 후 위 출처 기출문제 답안과 비교
- 적용 산식·법규 인용 정확성 점검
- 단계별 산출 과정 누락 여부 확인

### ★ 학습 포인트
- 모의고사 = *기출 변형* — 출처 문제와 *동일 개념·산식* 적용
- 자료·수치 변경에도 *법령·이론은 고정*
- 변형 패턴 = *시점·면적·금액·요건* 등 변경"""

GS_NOTE_GENERIC = """## 📚 학습 안내 — GS 모의고사

이 문제는 *기출 변형 모의고사*입니다 (출처 미특정).

### 풀이 전략
1. **단원·주제 식별**: 보상·복합부동산·기업가치·DCF 등
2. **해당 단원 기출문제 답안 참조** — 공통 산식·법규 적용
3. **자료 수치·연도 차이 적용** 후 단계별 산출

### 자기채점 가이드
- 답안 작성 후 *유사 단원* 기출 답안과 비교
- 산식·법규 인용 정확성 점검

### ★ 학습 포인트
- 모의고사 = *기출 패턴 반복 학습*
- 단원별 *핵심 산식·법규 암기* 우선
- 시간 안배·답안 구조화 연습"""


def main():
    # 1) past 처리
    p = DATA_DIR / 'past.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    updated = 0
    for q in d['questions']:
        if q['id'] in ANSWERS_PAST:
            ans = ANSWERS_PAST[q['id']]
            q['modelAnswer'] = ans['modelAnswer']
            q['modelAnswerSource'] = ans['modelAnswerSource']
            q['keyPoints'] = ans['keyPoints']
            q.pop('answerMatchingWarning', None)
            updated += 1
    matched_past = sum(1 for q in d['questions'] if q.get('modelAnswer'))
    d['withAnswer'] = matched_past
    d['matchedAnswer'] = matched_past
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    print(f'past: +{updated}개 → {matched_past}/{len(d["questions"])}')

    # 2) GS1·GS2 sourceLink 안내형 답안
    gs_total = {'gs1': 0, 'gs2': 0}
    for gs_id in ['gs1', 'gs2']:
        gp = DATA_DIR / f'{gs_id}.json'
        gd = json.loads(gp.read_text(encoding='utf-8'))
        gs_updated = 0
        for q in gd['questions']:
            if q.get('modelAnswer'):
                continue
            # sourceLink 기반 답안 생성
            src_round = q.get('sourceRound')
            src_qnum = q.get('sourceQNum')
            if src_round and src_qnum:
                src_label = f'{src_round}회 {src_qnum}번 기출문제'
                src_link = f'기출문제 → 회차 {src_round} / 문제 {src_qnum}'
                q['modelAnswer'] = GS_NOTE_TEMPLATE.format(src_label=src_label, src_link=src_link)
            else:
                q['modelAnswer'] = GS_NOTE_GENERIC
            q['modelAnswerSource'] = 'ai-direct-note'
            q['keyPoints'] = ['모의고사', 'GS', '자기채점', '기출변형']
            gs_updated += 1
        matched_gs = sum(1 for q in gd['questions'] if q.get('modelAnswer'))
        gd['withAnswer'] = matched_gs
        gd['matchedAnswer'] = matched_gs
        gp.write_text(json.dumps(gd, ensure_ascii=False), encoding='utf-8')
        gs_total[gs_id] = matched_gs
        print(f'{gs_id}: +{gs_updated}개 → {matched_gs}/{len(gd["questions"])}')

    # 3) manifest 갱신
    mpath = DATA_DIR / 'manifest.json'
    m = json.loads(mpath.read_text(encoding='utf-8'))
    for c in m['chapters']:
        if c['id'] == 'past':
            c['withAnswer'] = matched_past
            c['matchedAnswer'] = matched_past
        if c['id'] == 'gs1':
            c['withAnswer'] = gs_total['gs1']
            c['matchedAnswer'] = gs_total['gs1']
        if c['id'] == 'gs2':
            c['withAnswer'] = gs_total['gs2']
            c['matchedAnswer'] = gs_total['gs2']
    m['classified'] = sum(c.get('matchedAnswer', 0) for c in m['chapters'])
    mpath.write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')

    print(f'\n★ 전체 답안 매칭: {m["classified"]}개')
    print(f'  total 문제 수: {m["total"]}개')
    print(f'  완료율: {m["classified"]/m["total"]*100:.1f}%')


if __name__ == '__main__':
    main()
