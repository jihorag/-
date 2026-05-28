#!/usr/bin/env python3
"""단원 5/6a/8a/8b 표준 보강 (각 3개씩, 총 12개)."""
import json
import re
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')


CHAPTER_PROBLEMS = {
    '5': [
        {
            'subchapter': '5-1',
            'difficulty': 3, 'points': 20,
            'topic': '시산조정 — 단순 가중평균',
            'body': """감정평가사 K는 3방식 시산가 단순 가중평균을 의뢰받았다. (20점)

[ 자료 01 ] 시산가
- 원가: 4,200백만
- 비교: 4,500
- 수익: 4,350

[ 자료 02 ] 가중치 (사무용 임대)
- 원가 20% / 비교 50% / 수익 30%

[ 자료 03 ] 가중평균
- 4,200×0.2 + 4,500×0.5 + 4,350×0.3 = 840 + 2,250 + 1,305 = 4,395백만

[ 물음 ]
1. 3방식 시산
2. 가중평균
3. 가중치 근거
4. §12""",
            'modelAnswer': """## Ⅰ. 서론
시산조정은 §12.

## Ⅱ. 본론
### 1. 시산: 원가 4,200 / 비교 4,500 / 수익 4,350
### 2. 가중평균: **4,395백만**
### 3. 가중치: 사무용 임대 통상 2:5:3
### 4. §12: 객관·합리

## Ⅲ. 결론
결정 4,395백만.

## ★ 핵심 학습 포인트
- 가중치 2:5:3
- §12""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['원가 4,200 / 비교 4,500 / 수익 4,350 → 4,395백만', '가중 2:5:3', '§12']
        },
        {
            'subchapter': '5-2',
            'difficulty': 3, 'points': 20,
            'topic': '기업가치 — PER 배수 평가',
            'body': """감정평가사 K는 기업가치 PER 배수 평가를 의뢰받았다. (20점)

[ 자료 01 ] 기업
- 순이익: 1,200백만
- 동종 PER: 12배

[ 자료 02 ] 기업가치
- 1,200 × 12 = 14,400백만

[ 자료 03 ] 비상장 할인 (DLOM 20%)
- 14,400 × 0.8 = 11,520백만

[ 물음 ]
1. 순이익 × PER
2. 비상장 할인
3. 결정 가치
4. PER vs EV/EBITDA""",
            'modelAnswer': """## Ⅰ. 서론
PER = 가격 / 순이익.

## Ⅱ. 본론
### 1. 가치: 14,400백만
### 2. DLOM 20%: 11,520
### 3. 결정: **11,520백만**
### 4. PER vs EV/EBITDA
- PER: 순이익 기준
- EV/EBITDA: 영업이익 + 감가 + 부채 포함

## Ⅲ. 결론
비상장 가치 11,520백만.

## ★ 핵심 학습 포인트
- PER × 순이익
- DLOM 20%
- 비상장 할인""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['순이익 1,200 × PER 12 = 14,400 × DLOM 0.8 = 11,520백만', 'PER vs EV/EBITDA', '비상장 -20%']
        },
        {
            'subchapter': '5-3',
            'difficulty': 3, 'points': 20,
            'topic': '무형자산 — 저작권 평가',
            'body': """감정평가사 K는 저작권 가치 평가를 의뢰받았다. (20점)

[ 자료 01 ] 저작권
- 출판물 인세 연 80백만
- 잔여 보호기간 30년 (저작자 사망 후 70년)
- 환원율 15%

[ 자료 02 ] 영구 환원
- 80 / 0.15 = 533백만

[ 자료 03 ] 30년 한정 (연금현가 6.566)
- 80 × 6.566 = 525백만

[ 자료 04 ] 결정
- 30년 한정 525백만 (보수)

[ 물음 ]
1. 인세 연 수익
2. 영구 vs 한정 환원
3. 결정 가치
4. 저작권법 (보호기간)""",
            'modelAnswer': """## Ⅰ. 서론
저작권은 보호기간 한정.

## Ⅱ. 본론
### 1. 인세 80/년
### 2. 영구 533 / 한정 525
### 3. 결정: **525백만**
### 4. 보호기간: 저작자 사망 + 70년

## Ⅲ. 결론
저작권 525백만.

## ★ 핵심 학습 포인트
- 한정 연금현가
- 저작권 보호기간 70년""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['인세 80/년 × 6.566(30년) = 525백만', '영구 533, 한정 525', '저작권법 70년']
        },
    ],
    '6a': [
        {
            'subchapter': '6a-1',
            'difficulty': 3, 'points': 20,
            'topic': '보상 — 기본 평가 단가 산정',
            'body': """감정평가사 K는 도로 사업 보상 기본 평가를 의뢰받았다. (20점)

[ 자료 01 ] 부동산
- 자연녹지·전 1,000㎡

[ 자료 02 ] 비교표준지
- 공시지가 (2026.1.1): 280,000원/㎡
- 시점 1.0095, 지역 1.000, 개별 0.985
- 그밖의요인 1.22

[ 자료 03 ] 평가
- 280,000 × 1.0095 × 0.985 × 1.22 = 339,758 → 339,000원/㎡
- 총: 339백만

[ 물음 ]
1. 시점·지역·개별 보정
2. 그밖의요인 보정
3. 평가단가·총액""",
            'modelAnswer': """## Ⅰ. 서론
보상 기본 평가는 §70.

## Ⅱ. 본론
### 1. 보정: 280,000 × 1.0095 × 0.985 = 278,490원
### 2. 그밖의요인: × 1.22 = 339,758 → 339,000원/㎡
### 3. 총액: **339백만**

## Ⅲ. 결론
평가 339백만.

## ★ 핵심 학습 포인트
- 시점·지역·개별·그밖의요인
- §70 + §22""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['보정 339,000원/㎡', '총 339백만', '§70 + §22']
        },
        {
            'subchapter': '6a-1',
            'difficulty': 3, 'points': 20,
            'topic': '보상 — 부분 편입 (잔여지 손실 미발생)',
            'body': """감정평가사 K는 부분 편입 (잔여지 정상 사용) 보상을 의뢰받았다. (20점)

[ 자료 01 ] 부동산
- 토지 2,000㎡ (편입 500, 잔여 1,500)

[ 자료 02 ] 단가
- 1,200,000원/㎡

[ 자료 03 ] 편입 평가
- 1,200 × 500 = 600백만

[ 자료 04 ] 잔여
- 정형·접도 양호 → 가치 변동 무
- 잔여 손실 X

[ 물음 ]
1. 편입 평가
2. 잔여 손실 여부
3. 총 보상""",
            'modelAnswer': """## Ⅰ. 서론
잔여 정상 사용 시 손실 미발생.

## Ⅱ. 본론
### 1. 편입: **600백만**
### 2. 잔여: 손실 무 (정형·접도 양호)
### 3. 총: 600백만

## Ⅲ. 결론
편입 보상 600백만.

## ★ 핵심 학습 포인트
- 잔여 사용 가능 시 손실 무
- §73 요건 (가치 하락)""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['편입 500㎡ × 1,200 = 600백만', '잔여 손실 무', '§73 미적용']
        },
        {
            'subchapter': '6a-2',
            'difficulty': 3, 'points': 20,
            'topic': '보상 — 단순 그밖의요인 산정',
            'body': """감정평가사 K는 단순 그밖의요인 산정을 의뢰받았다. (20점)

[ 자료 01 ] 표준지 보정 단가: 250,000원/㎡
[ 자료 02 ] 선례 평균: 320,000원/㎡
[ 자료 03 ] 보정치
- 320,000 / 250,000 = 1.28
[ 자료 04 ] 평가단가: 250,000 × 1.28 = 320,000원/㎡

[ 물음 ]
1. 보정치
2. 평가단가
3. 한도 (1.5)
4. §22""",
            'modelAnswer': """## Ⅰ. 서론
그밖의요인 = 선례 / 표준지.

## Ⅱ. 본론
### 1. 보정치: **1.28**
### 2. 단가: 320,000원/㎡
### 3. 한도 1.5 내
### 4. §22

## Ⅲ. 결론
단가 320,000원/㎡.

## ★ 핵심 학습 포인트
- 보정치 = 선례 / 표준지
- 한도 1.5""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['보정치 1.28', '단가 320,000원/㎡', '§22']
        },
    ],
    '8a': [
        {
            'subchapter': '8a-1',
            'difficulty': 3, 'points': 20,
            'topic': '담보평가 — 토지·건물 일체',
            'body': """감정평가사 K는 토지·건물 일체 담보평가를 의뢰받았다. (20점)

[ 자료 01 ] 부동산
- 시가: 2,500백만

[ 자료 02 ] LTV
- 70% 적용: 1,750백만

[ 자료 03 ] 처분 감액
- 시가 × 0.85 = 2,125
- LTV 70%: 1,488

[ 물음 ]
1. 시가
2. LTV 한도
3. 처분 후 한도""",
            'modelAnswer': """## Ⅰ. 서론
담보 = 시가 × LTV × 처분 감액.

## Ⅱ. 본론
### 1. 시가 2,500
### 2. LTV 1,750
### 3. 처분: **1,488백만**

## Ⅲ. 결론
대출 1,488백만.

## ★ 핵심 학습 포인트
- LTV 70%
- 처분 감액 15%""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['시가 2,500 × 0.7 × 0.85 = 1,488백만', 'LTV 70%', '처분 -15%']
        },
        {
            'subchapter': '8a-2',
            'difficulty': 3, 'points': 20,
            'topic': '경매 — 1차 매각 기대 배당',
            'body': """감정평가사 K는 1차 매각 기대 배당을 의뢰받았다. (20점)

[ 자료 01 ] 부동산
- 시가 1,500백만
- 근저당 800
- 가압류 200

[ 자료 02 ] 매각 (1차)
- 1,500 × 0.85 = 1,275

[ 자료 03 ] 배당
- 우선 50
- 근저당 800
- 가압류 200
- 잔여 225

[ 물음 ]
1. 1차 매각가
2. 배당 분석
3. 잔여 잉여""",
            'modelAnswer': """## Ⅰ. 서론
경매 1차 매각.

## Ⅱ. 본론
### 1. 매각: 1,275백만
### 2. 배당: 우선 50 / 근저당 800 / 가압류 200 / 잔여 **225**
### 3. 잉여 225

## Ⅲ. 결론
잔여 225백만.

## ★ 핵심 학습 포인트
- 1차 매각 = 시가 × 85%
- 배당 순위""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['1차 1,275 - 우선 50 - 근저당 800 - 가압류 200 = 225백만', '배당 순위', '시가 × 85%']
        },
        {
            'subchapter': '8a-3',
            'difficulty': 3, 'points': 20,
            'topic': '국공유 — 매각 시 적정가',
            'body': """감정평가사 K는 국공유 매각 시 적정가를 의뢰받았다. (20점)

[ 자료 01 ] 부동산
- 국유 토지 800㎡, 시가 1,800,000원/㎡
- 시가: 1,440백만

[ 자료 02 ] 매각가
- 일반: 1,440
- 공익: -10% = 1,296

[ 물음 ]
1. 시가
2. 일반·공익 매각가
3. 국유재산법 §43""",
            'modelAnswer': """## Ⅰ. 서론
국유 매각은 §43.

## Ⅱ. 본론
### 1. 시가: 1,440백만
### 2. 일반 1,440 / 공익 **1,296**
### 3. §43 매각

## Ⅲ. 결론
일반 1,440, 공익 1,296백만.

## ★ 핵심 학습 포인트
- §43 매각
- 공익 -10%""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['시가 1,440 / 공익 1,296백만', '국유재산법 §43', '공익 10% 감액']
        },
    ],
    '8b': [
        {
            'subchapter': '8b-1',
            'difficulty': 3, 'points': 20,
            'topic': '표준지 — 단순 거래사례 비교',
            'body': """감정평가사 K는 표준지 거래사례 비교를 의뢰받았다. (20점)

[ 자료 01 ] 표준지
- 일반상업 250㎡

[ 자료 02 ] 거래사례 (보정 후)
- 사례 A: 8,200천원/㎡
- 사례 B: 8,500
- 사례 C: 8,000
- 평균: 8,233

[ 자료 03 ] 결정
- 8,200천원/㎡ (반올림)

[ 물음 ]
1. 사례 평균
2. 결정 단가
3. 부공법 §3""",
            'modelAnswer': """## Ⅰ. 서론
표준지는 적정가격.

## Ⅱ. 본론
### 1. 평균: 8,233천원/㎡
### 2. 결정: **8,200천원/㎡**
### 3. §3 적정가격

## Ⅲ. 결론
표준지 8,200천원/㎡.

## ★ 핵심 학습 포인트
- 거래사례 평균
- 부공법 §3""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['3사례 평균 8,233 → 8,200천원/㎡', '부공법 §3', '단순 비교']
        },
        {
            'subchapter': '8b-2',
            'difficulty': 3, 'points': 20,
            'topic': '정비사업 — 비례율 산정',
            'body': """감정평가사 K는 정비사업 비례율 산정을 의뢰받았다. (20점)

[ 자료 01 ] 사업
- 종전 400,000백만
- 종후 720,000
- 사업비 460,000

[ 자료 02 ] 비례율
- (720,000 - 460,000) / 400,000 = 0.65

[ 물음 ]
1. 비례율 산정
2. 비례율 의미
3. 도시정비법""",
            'modelAnswer': """## Ⅰ. 서론
비례율 = (종후 - 사업비) / 종전.

## Ⅱ. 본론
### 1. 비례율: **0.65**
### 2. 1.0 미만 → 조합원 부담
### 3. 도시정비법 §74

## Ⅲ. 결론
비례율 0.65.

## ★ 핵심 학습 포인트
- 비례율 산식
- 1.0 미만 = 조합원 부담""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['(720 - 460) / 400 = 0.65', '조합원 부담', '도시정비법 §74']
        },
        {
            'subchapter': '8b-3',
            'difficulty': 3, 'points': 20,
            'topic': '불의타 — 화재 단순 손실',
            'body': """감정평가사 K는 화재 단순 손실 평가를 의뢰받았다. (20점)

[ 자료 01 ] 부동산
- 단독건물, 일부 화재

[ 자료 02 ] 손실
- 적산가액 손실: 65백만
- 가구 폐기: 12백만
- 합: 77백만

[ 자료 03 ] 보험
- 보상 60백만
- 자기부담 17

[ 물음 ]
1. 손실
2. 보험 보상
3. 자기부담""",
            'modelAnswer': """## Ⅰ. 서론
화재 손실 = 적산 + 가구 - 보험.

## Ⅱ. 본론
### 1. 손실: 77백만
### 2. 보험: 60백만
### 3. 자기부담: **17백만**

## Ⅲ. 결론
자기부담 17백만.

## ★ 핵심 학습 포인트
- 적산 + 가구
- 보험 차감""",
            'modelAnswerSource': 'ai-direct-essay',
            'answerFormat': 'essay-narrative',
            'keyPoints': ['손실 77 - 보험 60 = 자기부담 17백만', '적산 + 가구재', '보험 차감']
        },
    ],
}


def get_next_id(data, ch):
    next_id = max(
        (int(m.group(1)) for q in data['questions']
         for m in [re.match(rf'practice-{ch}-(\d+)', q['id'])] if m),
        default=0
    ) + 1
    return next_id


def main():
    total = 0
    for ch, problems in CHAPTER_PROBLEMS.items():
        path = DATA_DIR / f'{ch}.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        next_id = get_next_id(data, ch)

        added = []
        for i, p in enumerate(problems):
            qid = f'practice-{ch}-{next_id + i}'
            q = {
                'id': qid,
                'subject': '감정평가실무',
                'chapter': ch,
                'source': 'practice-set',
                'subchapter': p['subchapter'],
                'difficulty': p['difficulty'],
                'points': p['points'],
                'topic': p['topic'],
                'body': p['body'],
                'modelAnswer': p['modelAnswer'],
                'modelAnswerSource': p['modelAnswerSource'],
                'answerFormat': p['answerFormat'],
                'keyPoints': p['keyPoints'],
            }
            data['questions'].append(q)
            added.append(qid)

        data['count'] = len(data['questions'])
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

        total += len(added)
        print(f"단원 {ch} +{len(added)} → 총 {data['count']}")

    print(f'\n전체 추가: {total}개')


if __name__ == '__main__':
    main()
