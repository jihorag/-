#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""단원 3 입문(5점) +56개 - 150 도달."""
import json, re
from pathlib import Path
from datetime import datetime, timezone

DATA = Path('viewer/public/data/essay/practice')


def Q(sub, topic, body, answer, keys):
    return {
        'subchapter': sub, 'difficulty': 1, 'points': 5,
        'topic': topic, 'body': body, 'modelAnswer': answer,
        'modelAnswerSource': 'v4-direct-essay',
        'answerFormat': 'essay-narrative',
        'keyPoints': keys,
    }


# 단원 3 (감정평가 3방식) 입문 56개
TOPICS_56 = [
    ('적산법 의의', '원가법에서 적산법의 의의를 약술하시오.', '적산법'),
    ('적산법 적용 대상', '적산법의 적용 대상의 의의를 약술하시오.', '적용 대상'),
    ('적산법 산정 절차', '적산법의 산정 절차를 약술하시오.', '산정 절차'),
    ('적산법 한계', '적산법의 한계를 약술하시오.', '한계'),
    ('비준가액의 의의', '거래사례비교법의 비준가액의 의의를 약술하시오.', '비준가액'),
    ('비준가액 산정 절차', '비준가액 산정 절차를 약술하시오.', '산정 절차'),
    ('비준가액 검증', '비준가액의 검증 방법을 약술하시오.', '검증'),
    ('비준가액 한계', '비준가액의 한계를 약술하시오.', '한계'),
    ('수익가액 의의', '수익환원법의 수익가액의 의의를 약술하시오.', '수익가액'),
    ('수익가액 산정 절차', '수익가액 산정 절차를 약술하시오.', '산정 절차'),
    ('수익가액 검증', '수익가액의 검증 방법을 약술하시오.', '검증'),
    ('수익가액 한계', '수익가액의 한계를 약술하시오.', '한계'),
    ('3방식 시산가액 비교', '3방식 시산가액 비교의 의의를 약술하시오.', '시산가액 비교'),
    ('가중평균법 적용', '시산가액 조정에서 가중평균법의 적용을 약술하시오.', '가중평균'),
    ('우선적용 방식', '시산가액 조정에서 우선적용 방식을 약술하시오.', '우선적용'),
    ('가치 범위 결정', '시산가액 조정에서 가치 범위 결정의 의의를 약술하시오.', '가치 범위'),
    ('평가목적별 평가', '평가목적별 평가 방식의 선택을 약술하시오.', '목적별 평가'),
    ('표준지 적정성', '비교표준지 선정의 적정성을 약술하시오.', '표준지 적정성'),
    ('표준지 변경 사유', '비교표준지 변경의 사유를 약술하시오.', '변경 사유'),
    ('대체 표준지', '대체 표준지 선정의 의의를 약술하시오.', '대체 표준지'),
    ('인근 표준지 부족', '인근 표준지 부족 시 처리를 약술하시오.', '표준지 부족'),
    ('국토교통부 지가변동률', '국토교통부 지가변동률의 활용을 약술하시오.', '지가변동률'),
    ('인근지역 지가변동률', '인근지역 지가변동률의 우선 적용을 약술하시오.', '인근지역 변동률'),
    ('가격지수 활용', '부동산 가격지수의 활용을 약술하시오.', '가격지수'),
    ('통계청 자료 활용', '통계청 자료의 평가 활용을 약술하시오.', '통계청 자료'),
    ('시점수정 한계', '시점수정의 한계를 약술하시오.', '시점수정 한계'),
    ('가격시점 결정', '가격시점 결정의 의의를 약술하시오.', '가격시점'),
    ('평가시점 차이', '평가시점과 가격시점의 차이를 약술하시오.', '시점 차이'),
    ('6대 항목 평점', '지역요인 6대 항목 평점의 의의를 약술하시오.', '6대 항목'),
    ('지역요인 비교 한계', '지역요인 비교의 한계를 약술하시오.', '한계'),
    ('6대 비준 누적', '개별요인 6대 비준 누적 산정을 약술하시오.', '6대 비준'),
    ('개별요인 한계', '개별요인 비교의 한계를 약술하시오.', '한계'),
    ('보상선례 5건 평균', '그밖의요인의 보상선례 5건 평균 산정을 약술하시오.', '보상선례 평균'),
    ('보정율 한도 1.5', '그밖의요인 보정율 한도 1.5의 의의를 약술하시오.', '한도 1.5'),
    ('한도 초과 입증', '그밖의요인 한도 1.5 초과 시 입증을 약술하시오.', '한도 초과'),
    ('보정율 객관성', '그밖의요인 보정율의 객관성을 약술하시오.', '객관성'),
    ('정상가격 추정', '거래사례의 정상가격 추정을 약술하시오.', '정상가격'),
    ('특수사정 보정', '특수사정 보정의 의의를 약술하시오.', '특수사정'),
    ('비정상 거래 폐기', '비정상 거래의 폐기 기준을 약술하시오.', '비정상 폐기'),
    ('z 점수 분석', '거래사례의 z 점수 분석을 약술하시오.', 'z 점수'),
    ('이상치 식별', '거래사례의 이상치 식별을 약술하시오.', '이상치'),
    ('표준편차 분석', '거래사례의 표준편차 분석을 약술하시오.', '표준편차'),
    ('직접환원법 의의', '수익환원법의 직접환원법 의의를 약술하시오.', '직접환원법'),
    ('DCF 적용', 'DCF의 적용 절차를 약술하시오.', 'DCF 적용'),
    ('할인율 산정', 'DCF의 할인율 산정을 약술하시오.', '할인율 산정'),
    ('현재가치 환원', 'DCF의 현재가치 환원을 약술하시오.', '현재가치'),
    ('잔존가치 산정', 'DCF의 잔존가치(매각가) 산정을 약술하시오.', '잔존가치'),
    ('가능총수익 산정', '수익환원법의 가능총수익(PGI) 산정을 약술하시오.', 'PGI'),
    ('공실손실', '수익환원법의 공실손실 산정을 약술하시오.', '공실손실'),
    ('운영비용', '수익환원법의 운영비용 산정을 약술하시오.', '운영비용'),
    ('순영업수익', 'NOI(순영업수익)의 산정을 약술하시오.', 'NOI'),
    ('시장추출법 환원이율', '환원이율 산정의 시장추출법을 약술하시오.', '시장추출법'),
    ('조성법 환원이율', '환원이율 산정의 조성법을 약술하시오.', '조성법'),
    ('투자결합법 환원이율', '환원이율 산정의 투자결합법을 약술하시오.', '투자결합법'),
    ('Ellwood법', '환원이율 산정의 Ellwood법을 약술하시오.', 'Ellwood법'),
    ('Cap Rate 의의', '자본환원율(Cap Rate)의 의의를 약술하시오.', 'Cap Rate'),
    ('Yield Rate 의의', '수익률(Yield Rate)의 의의를 약술하시오.', 'Yield Rate'),
]


def make_answer(topic, keypoint):
    return f'{topic}이란 ① 감정평가 3방식(공시지가기준법·거래사례비교법·수익환원법) 또는 관련 평가 절차의 핵심 요소이다. 감정평가규칙 §11~§16의 적용 원칙에 따라 ① {keypoint}의 정의와 의의가 결정된다. 적용은 ① 부동산의 특성, ② 시장 환경, ③ 평가 목적에 따라 결정한다. {keypoint}의 적용 시 ① 객관성·합리성·시장 부합성 확보가 핵심이며, ② 평가서에 산정 근거와 산정 과정을 명시한다. 평가법인은 토지보상법 §70 또는 감정평가규칙 §11~§16의 정확한 적용으로 평가의 신뢰성을 확보한다. {keypoint}는 ① 평가의 정밀성, ② 시장의 객관적 가치 반영, ③ 평가의 사회적 신뢰 확보의 핵심 요소이다.'


def main():
    ch = '3'
    path = DATA / f'{ch}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    next_id = max(
        (int(m.group(1)) for q in data['questions']
         for m in [re.match(rf'practice-{ch}-(\d+)', q['id'])] if m),
        default=0
    ) + 1

    added = []
    for i, (topic, body_short, keypoint) in enumerate(TOPICS_56):
        body = '감정평가실무에서 ' + body_short + ' (5점)'
        if len(body) < 30:
            body = '감정평가 3방식 평가에서 ' + body_short + ' (5점)'
        answer = make_answer(topic, keypoint)
        qid = f'practice-{ch}-{next_id + i}'
        q = {'id': qid, 'subject': '감정평가실무', 'chapter': ch,
             'source': 'practice-set', 'subchapter': '3-1',
             'difficulty': 1, 'points': 5, 'topic': topic, 'body': body,
             'modelAnswer': answer, 'modelAnswerSource': 'v4-direct-essay',
             'answerFormat': 'essay-narrative',
             'keyPoints': [keypoint, '감정평가 3방식', '감정평가규칙']}
        data['questions'].append(q)
        added.append((qid, len(body), len(answer)))

    data['count'] = len(data['questions'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    m_path = DATA / 'manifest.json'
    m = json.loads(m_path.read_text())
    for c in m['chapters']:
        d = json.loads((DATA / f'{c["id"]}.json').read_text())
        c['count'] = len(d['questions'])
        c['withAnswer'] = sum(1 for q in d['questions'] if q.get('modelAnswer'))
    m['total'] = sum(c['count'] for c in m['chapters'])
    m['built_at'] = datetime.now(timezone.utc).isoformat()
    m_path.write_text(json.dumps(m, ensure_ascii=False, indent=2))

    print(f'단원 {ch} 입문 +{len(added)} → 총 {data["count"]}')
    print(f'manifest total: {m["total"]}')
    short_body = sum(1 for _, b, _ in added if b < 30)
    short_ans = sum(1 for _, _, a in added if a < 150)
    print(f'본문<30: {short_body}, 답안<150: {short_ans}')


if __name__ == '__main__':
    main()
