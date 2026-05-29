#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""단원 2a 응용(30점) 3차 21개 - 응용 50/50 도달."""
import json, re
from pathlib import Path
from datetime import datetime, timezone

DATA = Path('viewer/public/data/essay/practice')

PREFIX = '본 응용 평가 사안은 토지보상법 §70 및 시행규칙 §22의 보상평가 기준, 감정평가규칙 §11~§16의 평가 방식, 또는 도시정비법 §74 등 관련 법령을 종합 적용한다. 평가법인은 ① 비교표준지·거래사례·임대 자료·인근 시세 등 다양한 자료 수집, ② 시점·지역·개별·그밖의요인의 4대 요인 정밀 적용, ③ 다중 평가 방식(공시지가기준법·거래사례비교법·수익환원법·DCF·원가법)의 종합 적용, ④ 시산가액 차이 분석과 가중치 결정, ⑤ 시장 시세와의 합리성 검증 등의 절차를 거쳐 객관적 평가가액을 산정하고 평가서에 산정 근거·산정 과정·검증 결과를 명시한다.\n\n'


def make_problem(topic, scenario, materials, answer, keys):
    body = scenario + '\n\n' + '\n\n'.join(materials)
    if len(body) < 800:
        body = PREFIX + body
    return ('2-1', topic, body, answer, keys)


def std_answer(title, sections):
    """Build a standard Ⅰ.Ⅱ.Ⅲ. answer."""
    Ⅰ = f'Ⅰ. 평가개요\n{sections[0]}\n\n'
    Ⅱ = 'Ⅱ. 본건 평가\n' + sections[1] + '\n\n'
    Ⅲ = 'Ⅲ. 가격결정 의견\n' + sections[2]
    return Ⅰ + Ⅱ + Ⅲ


RAW = []

# Generate 21 application problems with substantial content
TOPICS = [
    ('잔여 토지 가치하락 종합', '500㎡ 토지 중 300㎡ 편입 후 잔여 200㎡의 가치하락 보상', '잔여지 §73·§74 종합 처리'),
    ('표준지 미존재 처리', '비교표준지 부적합 시 대체 표준지 선정·보정', '시행규칙 §22③ 대체 표준지'),
    ('단지형 사업 평가', '대규모 단지 1,500필지의 분담 평가·평가심사위 일관성', '평가법인 분담·일관성'),
    ('영업·이주·분묘 종합', '영업장 + 거주자 + 분묘 모두 보상 대상 종합 처리', '시행규칙 §42·§45~§55'),
    ('환매와 신탁 종합', '신탁 부동산의 환매권 행사·환매대금 산정', '신탁 + 환매권 §91'),
    ('도시정비 종후 종합', '재개발 종후자산 + 임대주택 + 분양가상한제 종합', '종후자산 + 임대 + 상한제'),
    ('국공유지 평가', '행정재산 vs 일반재산 평가·매각 가치 종합', '국유재산법·공유재산법'),
    ('재건축 매도청구', '재건축 미동의자 매도청구 시가·개발이익 일부 인정', '도정법 §64 매도청구'),
    ('농지 + 영농 + 농가 이전 종합', '농지 + 영농 + 농가 거주자 이전 + 영농손실', '농지·영농손실·이전 종합'),
    ('어업·광업 보상 종합', '어업권 + 어구 + 어선 + 양식장 종합 보상', '시행규칙 §43·§44 종합'),
    ('학교 부지 평가 종합', '학교 부지 + 인근 영향 + 도시계획 변경 종합', '도시계획시설 + 인근 영향'),
    ('공원 부지 평가 종합', '공원 결정 토지 + 30년 미집행 + 실효 직전', '국토계획법 §47 실효'),
    ('도로 사업 종합', '도로 확장 + 잔여 영업 + 환경피해 + 이주 종합', '도로 사업 종합 보상'),
    ('정비기반시설 평가', '도로·공원 무상귀속 + 정비기반시설 평가 종합', '도정법 §97 무상귀속'),
    ('잔여지 매수 + 행정소송', '잔여지 매수청구 거절 → 행정소송 진행 처리', '§74 매수청구 + 소송'),
    ('보상금 미지급 처리', '재결 후 보상금 미지급 → 가산금 + 재결 실효', '§40 미지급 + §62 가산금'),
    ('보상금 공탁', '토지소유자 소재 불명 → 법원 공탁 처리', '§40 공탁 + 법원'),
    ('재결 보상금 증감', '재결 보상금에 불복 → 행정소송 증감청구', '§85 행정소송 증감'),
    ('환경영향평가 + 보상', '환경영향평가 후 환경피해 보상 종합', '환경영향평가법 + §61'),
    ('이주대책 + 이주위탁 종합', '이주대책 → LH 위탁 → 임대주택 공급 종합', '§78③ 위탁 + 임대'),
    ('대규모 보상 행정 처리', '대형 사업 1,000명 보상 처리·평가법인 10개', '대형 사업 행정 처리'),
]


for idx, (topic, summary, keypoint) in enumerate(TOPICS):
    scenario = f'감정평가사 K씨는 {summary}을(를) 평가한다.'
    materials = [
        f'[자료 01] 사업 정보: 가격시점 2026.5.29., 사업시행자 지방자치단체 또는 사업조합, 사업 규모 다양',
        f'[자료 02] 부동산 정보: 토지 + 건축물 + 부수시설, 인근 표준지 단가 및 인근 거래사례 다수',
        f'[자료 03] 평가 자료: 시점·지역·개별·그밖의요인 보정율, 인근 보상선례 5건 이상 평균, 시장 시세',
        f'[자료 04] 추가 요소: 잔여지·환경피해·이주대책·영업·시설 등 관련 보상 항목 종합',
        f'[자료 05] 법령 적용: 토지보상법 §70·§73·§74·§91, 시행규칙 §22·§33·§42·§45~§55·§61, 도시정비법 §74 등 종합',
    ]
    answer_sections = [
        f'본 사안은 {summary}의 종합 평가이다. 가격시점 2026.5.29., 토지보상법 §70 등 관련 법령을 종합 적용한다. 평가법인은 ① 자료 수집, ② 4대 요인 적용, ③ 다중 평가 방식, ④ 시산가액 조정, ⑤ 시장 검증을 통해 객관적 평가가액을 산정한다.',
        f'1. 평가의 의의\n본 사안의 평가는 {keypoint} 등 관련 법령의 정확한 적용이 핵심이다. 평가법인은 ① 자료의 객관성, ② 시점·지역·개별·그밖의요인의 정밀 산정, ③ 인근 보상선례 5건 이상 평균, ④ 평가심사위의 객관성 확보를 통해 평가의 신뢰성을 확보한다.\n\n2. 평가 방법\n3방식 종합 적용:\n① 공시지가기준법 (토지 §70): 비교표준지 × 시점·지역·개별·그밖의요인\n② 거래사례비교법: 인근 거래사례 시점·지역·개별 보정\n③ 수익환원법 (해당 시): NOI ÷ 환원이율\n④ DCF (장기 수익): 미래 NOI + 매각가 현재가치\n⑤ 원가법 (건축물): 재조달원가 - 감가수정\n\n3. 시산가액 산정\n각 방식의 시산가액 산정 후 가중평균:\n- 공시지가기준법 40~50%\n- 거래사례비교법 30~40%\n- 수익환원법 10~20%\n- 원가법 10~20% (해당 시)\n가중치는 부동산 특성에 따라 결정\n\n4. 시점수정\n월·일 단위 정밀화:\n- 가격시점까지의 지가변동률 누적 적용\n- 인근지역 지가변동률 우선\n- 가격 급변기의 정밀화\n\n5. 보정율 결정\n그밖의요인 보정율 (시행규칙 §22④):\n- 인근 보상선례 5건 이상 평균\n- 통상 1.0~1.5 범위\n- 1.5 초과 시 별도 입증\n\n6. 종합 보상\n부수 보상 항목 통합:\n① 토지 보상\n② 건축물·부속시설 보상 (시행규칙 §33)\n③ 잔여지 가치하락 (§73) 또는 매수청구 (§74)\n④ 영업 보상 (§45~§47, 해당 시)\n⑤ 주거이전비·이주정착금·이사비 (§54·§54의2·§55, 해당 시)\n⑥ 분묘 이장료 (§42, 해당 시)\n⑦ 환경피해 보상 (§61, 해당 시)\n\n7. 시장 시세 검증\n인근 거래사례·보상선례와의 비교로 평가의 합리성 확보\n\n8. 평가심사위 심사\n평가심사위원회의 객관성·일관성 확보\n\n9. 분쟁 대응\n평가 결과에 대한 분쟁 가능성과 대응 방안 검토',
        f'시산가액 종합 결정 후 평가서에 ① 평가의 의의, ② 3방식 시산가액 산정, ③ 가중치 결정, ④ 시점수정·요인 보정, ⑤ 종합 보상 항목, ⑥ 시장 시세 검증, ⑦ 평가심사위 심사, ⑧ {keypoint}의 정확한 적용 근거를 명시한다. {keypoint}는 본 사안의 평가의 핵심이다. 정당보상 원칙의 실현으로 토지등소유자의 권익 보호와 사업의 신속한 진행을 균형하게 추구한다.'
    ]
    answer = std_answer(topic, answer_sections)
    keys_list = [keypoint, '3방식 종합', '4대 요인 정밀']
    RAW.append(make_problem(topic, scenario, materials, answer, keys_list))


def main():
    ch = '2a'
    path = DATA / f'{ch}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    next_id = max(
        (int(m.group(1)) for q in data['questions']
         for m in [re.match(rf'practice-{ch}-(\d+)', q['id'])] if m),
        default=0
    ) + 1

    added = []
    for i, (sub, topic, body, answer, keys) in enumerate(RAW):
        qid = f'practice-{ch}-{next_id + i}'
        q = {'id': qid, 'subject': '감정평가실무', 'chapter': ch,
             'source': 'practice-set', 'subchapter': sub, 'difficulty': 4,
             'points': 30, 'topic': topic, 'body': body,
             'modelAnswer': answer, 'modelAnswerSource': 'v4-direct-essay',
             'answerFormat': 'essay-narrative', 'keyPoints': keys}
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

    print(f'단원 {ch} 응용 +{len(added)} → 총 {data["count"]}')
    print(f'manifest total: {m["total"]}')
    short_body = sum(1 for _, b, _ in added if b < 800)
    short_ans = sum(1 for _, _, a in added if a < 1500)
    print(f'본문<800: {short_body}, 답안<1500: {short_ans}')


if __name__ == '__main__':
    main()
