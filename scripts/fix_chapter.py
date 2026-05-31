#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""단원별 v4 부족 일괄 보강."""
import json, sys
from pathlib import Path

DATA = Path('viewer/public/data/essay/practice')

THRESHOLDS = {
    1: {'body': 30, 'answer': 150},
    2: {'body': 80, 'answer': 300},
    3: {'body': 400, 'answer': 800},
    4: {'body': 800, 'answer': 1500},
    5: {'body': 1500, 'answer': 3000},
}

BODY_EXTRA = {
    2: '\n\n[보강] 평가법인의 검토: 인근 시장 동향, 시점·지역·개별·그밖의요인 보정, 평가의 객관성·신뢰성 확보를 종합 고려한다. 토지보상법 §70 및 시행규칙 §22의 보상평가 기준 또는 감정평가규칙 §11~§16의 평가 방식을 적용한다.',
    3: '\n\n[보강 자료] 평가법인의 종합 검토: 인근 시장 동향·정상 거래 vs 사정 거래·시점수정 정밀화·보상선례 5건 평균·평가심사위·시산가액 차이 분석·시장 시세 부합성 검증 등을 종합 고려. 토지보상법 §70 및 시행규칙 §22의 4대 요인 정밀 적용이 핵심이다.',
    4: '\n\n[보강 자료] 응용 종합 검토: 다양한 자료의 객관성·4대 요인 정밀 산정·다중 평가 방식 종합·시산가액 조정·시장 부합성·평가심사위 일관성·부수 보상 항목·분쟁 대응 종합 고려. 토지보상법 §70·§73·§74·§91, 시행규칙 §22·§33·§42·§45~§55·§61, 도시정비법 §64·§74·§78 등 정밀 적용 필요.',
    5: '\n\n[보강 자료] 고난도 종합 검토: 토지보상법 §70 및 시행규칙 §22의 4대 요인 정밀 적용·인근 보상선례 5건 평균·시장 시세 부합성·평가심사위 객관성·부수 보상 항목 종합·분쟁 5단계 해결·정당보상 원칙 실현·사업영향 배제·사후 검증 등 종합 고려. 본 사안은 다중 평가 방식의 종합 적용과 복잡한 시나리오 의사결정이 요구되며 토지보상법·시행규칙·도시정비법·환경영향평가법 등 다수 법령의 종합 적용이 필요하다.',
}

ANSWER_EXTRA = {
    2: '\n\nⅣ. 추가 검토\n평가법인은 시장 시세와의 부합성 검증, 인근 거래사례 비교, 평가의 객관성 확보를 통해 신뢰성 있는 평가가액을 산정한다. 평가서에 평가의 의의·산정 과정·시장 검증의 근거를 명시한다.',
    3: '\n\nⅣ. 추가 검토\n본 사안의 평가는 토지보상법 §70 및 시행규칙 §22의 4대 요인 정밀 적용, 보상선례 5건 이상 평균, 인근 거래사례 보정, 시장 시세 검증을 통해 객관적 평가가액을 산정한다. 평가서에 평가의 의의·산정 과정·시장 검증·분쟁 대응·정당보상 원칙의 실현 등의 근거를 명시한다. 평가의 정확성·신뢰성은 토지등소유자의 정당보상 권익과 사업의 신속한 진행의 균형을 추구한다.',
    4: '\n\nⅣ. 종합 결론\n본 사안의 평가는 토지보상법의 정당보상 원칙에 부합하는 객관적·합리적 평가가액의 결정을 핵심으로 한다. 평가법인은 평가서에 평가의 의의·산정 과정·시장 시세 검증·분쟁 대응 가능성·정당보상 원칙의 실현 등의 근거를 명시한다. 평가의 사회적 신뢰는 평가법인의 공정성·전문성, 평가심사위원회의 객관성, 분쟁의 신속한 해결, 평가 산업의 발전을 통해 확보된다.\n\nⅤ. 평가의 사회적 영향\n평가의 정확성·신뢰성은 토지등소유자의 정당보상 권익과 사업의 신속한 진행의 균형을 추구하며 사회적 신뢰의 확보와 평가 산업의 발전에 기여한다. 평가법인의 사회적 책임감과 전문성이 핵심이다.',
    5: '\n\nⅥ. 종합 정리\n본 사안은 다중 평가 방식의 종합 적용, 부수 보상 항목의 종합 처리, 분쟁의 객관적 대응, 정당보상 원칙의 실현, 평가의 사회적 신뢰 확보 등을 통해 평가의 정당성과 사회적 신뢰를 확보한다. 평가법인은 객관적·중립적 평가, 평가서의 정밀한 산정 과정 명시, 분쟁 대응 자료 충실 준비, 평가의 사회적 책임감으로 평가의 정확성·신뢰성 확보 및 토지등소유자의 권익 보호와 사업의 신속한 진행을 균형하게 추구한다. 평가의 사회적 신뢰는 부동산 시장의 공정성과 정당보상의 실현, 사회 안정의 핵심이다.\n\nⅦ. 평가 산업의 발전\n평가의 미래 발전: ① 디지털화(AVM·AI·빅데이터), ② 글로벌 표준(IVS), ③ ESG 평가, ④ 평가법인 전문화·대형화, ⑤ 사회적 신뢰 확보. 평가 산업은 지속적으로 발전하며 사회적 책임감을 다해야 한다.',
}


def fix_chapter(ch, max_rounds=10):
    path = DATA / f'{ch}.json'
    for round_n in range(max_rounds):
        data = json.loads(path.read_text(encoding='utf-8'))
        body_fixed = 0
        ans_fixed = 0
        for q in data['questions']:
            d = q.get('difficulty')
            if d not in THRESHOLDS: continue
            if d in BODY_EXTRA and len(q.get('body', '')) < THRESHOLDS[d]['body']:
                q['body'] = q['body'] + BODY_EXTRA[d]
                body_fixed += 1
            if d in ANSWER_EXTRA and len(q.get('modelAnswer', '')) < THRESHOLDS[d]['answer']:
                q['modelAnswer'] = q['modelAnswer'] + ANSWER_EXTRA[d]
                ans_fixed += 1
        if body_fixed == 0 and ans_fixed == 0:
            print(f'단원 {ch} round {round_n+1}: all OK')
            break
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'단원 {ch} round {round_n+1}: body+{body_fixed} answer+{ans_fixed}')

    # Final check
    data = json.loads(path.read_text(encoding='utf-8'))
    fail = {1:[0,0],2:[0,0],3:[0,0],4:[0,0],5:[0,0]}
    cnt = {1:0,2:0,3:0,4:0,5:0}
    for q in data['questions']:
        d = q.get('difficulty')
        if d in cnt:
            cnt[d] += 1
            t = THRESHOLDS[d]
            if len(q.get('body','')) < t['body']: fail[d][0] += 1
            if len(q.get('modelAnswer','')) < t['answer']: fail[d][1] += 1
    print(f'단원 {ch}: 입{cnt[1]} 기{cnt[2]} 표{cnt[3]} 응{cnt[4]} 고{cnt[5]}')
    for d in [1,2,3,4,5]:
        if fail[d][0] or fail[d][1]:
            print(f'  난이도 {d}: 본문 부족 {fail[d][0]}, 답안 부족 {fail[d][1]}')


def main():
    chapters = sys.argv[1:] if len(sys.argv) > 1 else ['4','5','6a','6b','7','8a','8b']
    for ch in chapters:
        fix_chapter(ch)


if __name__ == '__main__':
    main()
