#!/usr/bin/env python3
"""
2차 3과목(실무·이론·법규)의 ai_index.json 생성.
1차의 taxonomy 트리와 달리, 단원·논점 평탄 구조.
각 단원 안에서 ## 헤더를 topic으로 자동 추출.
"""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, 'viewer/public/data/study')

# ── 과목 정의 ────────────────────────────────────────────
SUBJECTS = {
    'appraisal_practice': {
        'subject': '감정평가실무',
        'title': '감정평가실무',
        'short': '실무',
        'essence': '주어진 자료에서 출제자가 숨겨놓은 논점을 읽어내고, 산식 흐름을 누락 없이 보여주는 시험',
        'exam_meta': {
            'minutes': 100,
            'problems_per_session': 4,
            'score_distribution': [40, 30, 20, 10],
            'min_score_per_question': 40,
            'pass_threshold': 60,
        },
        'unit_titles': {
            '1':  ('감정평가실무 기초', 'TVM·금융계수·면적·도로', 1),
            '2a': ('3방식 기초 — 공시지가·거래사례·원가', '공시지가기준법 ★', 3),
            '2b': ('3방식 — 수익환원·임대', 'DCF·임대료', 2),
            '3':  ('건물·복합·구분·임대료', '★ 19회 빈출', 3),
            '4':  ('유형별 평가', '토지·건물·기계기구', 2),
            '5':  ('비가치추계·기업가치·무형자산', 'DCF·기업가치', 2),
            '6a': ('토지보상 기본·원칙', '★ 보상 핵심', 3),
            '6b': ('토지보상 — 공법상제한·특수', '공법상제한·잔여지', 2),
            '7':  ('건축물·영업·기타 보상', '영업손실보상', 2),
            '8a': ('목적별 평가', '목적별 4종', 1),
            '8b': ('표준지·정비·불의타', '표준지·정비사업', 1),
        },
        'high_priority': ['2a', '3', '6a', '5'],
        'study_progression': ['1', '2a', '2b', '3', '5', '6a', '6b', '4', '7', '8a', '8b'],
        'has_calc': True,
    },
    'appraisal_theory': {
        'subject': '감정평가이론',
        'title': '감정평가이론',
        'short': '이론',
        'essence': '지식 깊이가 아닌 정형 답안 목차(Ⅰ·Ⅱ·Ⅲ)와 키워드로 100분 4문항 풀어내는 답안 작성 기술 시험',
        'exam_meta': {
            'minutes': 100,
            'problems_per_session': 4,
            'score_distribution': [40, 30, 20, 10],
            'pass_threshold': 60,
        },
        'unit_titles': {
            '01': ('감정평가 기초·분류·절차', '기초 개념', 2),
            '02': ('부동산 가치이론·가격형성', '가치이론', 2),
            '03': ('가격제원칙·시장론·시장분석', '가격제원칙 ★', 3),
            '04': ('3방식 개관·거래사례비교법', '비교법', 2),
            '05': ('원가법', '원가법', 2),
            '06': ('수익환원법', '★ 8회 빈출', 3),
            '07': ('기타방식·임료', '임료·기타', 1),
            '08': ('기업가치·물건별 평가', '★★★ 16회 1순위', 3),
            '09': ('부동산 투자·금융론', '투자·금융', 2),
            '10': ('부동산 정책론·기타논점', '정책론', 2),
        },
        'high_priority': ['08', '03', '06', '02'],
        'study_progression': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'],
        'has_templates': True,
    },
    'appraisal_law': {
        'subject': '감정평가 및 보상법규',
        'title': '감정평가 및 보상법규',
        'short': '보상법규',
        'essence': '사례 속에서 행정법+토지보상법 논점을 추출해 조문→학설→판례→결론으로 풀어내는 시험',
        'exam_meta': {
            'minutes': 120,
            'problems_per_session': 4,
            'score_distribution': [40, 30, 20, 10],
            'pass_threshold': 60,
        },
        'unit_titles': {
            '01': ('행정법 개관·일반원칙·행정법관계', '행정법 기초', 2),
            '02': ('행정입법·행정행위', '행정행위', 2),
            '03': ('행정계획·인허가의제·공법상계약', '행정계획', 1),
            '04': ('행정절차·실효성확보수단', '절차·확보수단', 2),
            '05': ('행정쟁송 (심판·취소소송·기타)', '★ 23회', 3),
            '06': ('행정상 손해전보', '국가배상', 2),
            '07': ('공용수용 (사업인정·재결·약식)', '★★ 24회', 3),
            '08': ('손실보상 (보상기준·환매·생활보상)', '★★★ 38회 1순위', 3),
            '09': ('부동산 가격공시법', '가격공시', 2),
            '10': ('감정평가법·도정법', '감정평가법·도정법', 2),
        },
        'high_priority': ['08', '07', '05'],
        'study_progression': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'],
        'has_cases': True,
    },
}


def extract_topics(unit_path):
    """단원 MD의 ## 헤더(또는 ### 부속)에서 topic 자동 추출."""
    if not os.path.exists(unit_path):
        return []
    txt = open(unit_path, encoding='utf-8').read()
    lines = txt.split('\n')
    topics = []
    total = len(lines)
    for i, line in enumerate(lines, 1):
        m = re.match(r'^##\s+(.+?)\s*$', line)
        if not m or line.startswith('###'):
            continue
        name = re.sub(r'<a\s+name="[^"]+"\s*>\s*</a>', '', m.group(1)).strip()
        name = re.sub(r'^[📘📖📚🎯🗺️🏃✏️🔧📝]\s*', '', name).strip()
        if len(name) < 2 or len(name) > 60:
            continue
        if any(k in name for k in ['본문 목차', '마인드 강의', '핵심요약서', '기본서', '워크북', '시험직전']):
            continue
        topics.append({'name': name, 'start': i, 'end': total})
    for i in range(len(topics) - 1):
        topics[i]['end'] = topics[i + 1]['start'] - 1
    return topics


# ── 명시적 소단원(논점) 정의 — 시험 빈출 기반 세분화 ─────────
EXPLICIT_TOPICS = {
    'appraisal_practice': {
        '1': [
            '화폐의 시간가치(TVM) — 6공식',
            '면적·도로 — 사각형·도로조건',
            '단가 환산 — 원/㎡·소수점',
            '단위면적·환산 기초',
            '용도지역·이용상황 분류',
        ],
        '2a': [
            '공시지가기준법 — 의의·산식',
            '비교표준지 선정 — 우선순위',
            '시점수정 — 지가변동률·생산자물가',
            '지역요인 비교',
            '개별요인 비교 — 격자형 정리',
            '그밖의 요인 보정 — 산정·검증',
            '거래사례비교법 — 사례 선택·배제',
            '사정보정 — 정상화·계량화',
            '원가법 — 재조달원가·감가수정',
            '감가수정 — 내용연수·정액·정율',
        ],
        '2b': [
            '수익환원법 — 직접환원법',
            'DCF — 할인현금흐름분석',
            '환원이율 결정 — 시장추출·요소구성',
            '자본환원율·재매도가격',
            '임대료 평가 — 적산법·임대사례',
            '실질임료·계약임료',
        ],
        '3': [
            '건물 평가 — 원가법 적용',
            '복합부동산 — 일체비준',
            '복합부동산 — 토지·건물 구분',
            '구분소유 건물 — 전유부분·공용부분',
            '구분소유 — 대지권',
            '임대료 평가 — 건물·복합',
        ],
        '4': [
            '토지 평가 — 일반·특수',
            '건물 평가 — 일반·특수',
            '기계기구 평가',
            '선박·항공기 평가',
            '자동차·건설기계',
        ],
        '5': [
            '비가치추계 — 의의·방법',
            '기업가치 평가 — DCF·시장가치',
            '기업가치 — 자본환원',
            '무형자산 평가 — 영업권',
            '무형자산 — 특허·상표',
            '주식·채권 평가',
        ],
        '6a': [
            '토지보상 — 평가원칙·보상기준',
            '공시지가기준 보상',
            '비교표준지 선정 — 보상평가',
            '시점수정 — 보상',
            '그밖의 요인 — 보상사례 활용',
            '잔여지 — 의의·평가',
        ],
        '6b': [
            '공법상 제한 — 일반·개별',
            '용도지역 변경 — 영향평가',
            '도시계획시설 부지',
            '미보상 토지 — 손실보상',
            '특수 토지 — 분묘·도로·하천',
            '환매권 — 의의·요건',
        ],
        '7': [
            '건축물 보상 — 잔여건축물·이전료',
            '영업손실 보상 — 휴업·폐업',
            '영업손실 — 잔여시설 보수',
            '농업 손실 — 농작물·과수',
            '광업·어업 손실',
            '기타 손실 — 휴직·실직',
        ],
        '8a': [
            '담보 평가 — 의의·방법',
            '경매·공매 평가',
            '국·공유재산 평가',
            '소송 평가 — 일반',
            '조세 부과 평가',
            '회계·재무보고 평가',
        ],
        '8b': [
            '표준지 공시지가 — 평가',
            '표준주택 가격 — 평가',
            '정비사업 — 재개발·재건축',
            '정비사업 — 분양가·종전자산',
            '관리처분 평가',
            '불의타 — 손실 평가',
        ],
    },
    'appraisal_theory': {
        '01': [
            '감정평가 의의·목적',
            '감정평가 분류 — 평가목적별',
            '감정평가 절차 — 의뢰부터 보고서',
            '평가서·평가의견서 작성',
            '평가사 의무·책임',
        ],
        '02': [
            '부동산 가치이론 — 사용가치·교환가치',
            '가치형성요인 — 자연·사회·경제',
            '가격형성과정',
            '시장가격 vs 정상가격',
            '특수가격 — 한정·특정',
        ],
        '03': [
            '가격제원칙 — 최유효이용 ★',
            '가격제원칙 — 균형·적합·기여',
            '가격제원칙 — 변동·경쟁·예측',
            '시장론 — 부동산시장의 특성',
            '시장분석 — 수급·가격',
            '지역분석 — 인근지역·유사지역',
        ],
        '04': [
            '3방식 개관 — 원가·비교·수익',
            '거래사례비교법 — 의의·절차',
            '사례 선택·사정보정·시점수정',
            '지역요인·개별요인 비교',
        ],
        '05': [
            '원가법 — 의의·산식',
            '재조달원가 — 추계방법',
            '감가수정 — 물리적·기능적·경제적',
            '감가수정 — 정액·정율·상환기금',
        ],
        '06': [
            '수익환원법 — 의의·체계',
            '직접환원법 — 환원이율',
            'DCF — 할인율·미래현금흐름',
            '환원이율 산정 — 시장추출·요소구성',
            '자본환원율',
            '운영순수익 산정',
        ],
        '07': [
            '기타 평가방식',
            '적산법·임대사례비교법',
            '임료의 종류·산정',
            '실질임료·지불임료',
        ],
        '08': [
            '기업가치 평가 — 방식',
            '기업가치 — DCF·자본환원',
            '무형자산 — 영업권·특허',
            '물건별 평가 — 총론 ★★★',
            '물건별 평가 — 5분류',
            '주식·채권·동산 평가',
        ],
        '09': [
            '부동산 투자분석 — NPV·IRR',
            '부동산 금융 — 모기지·MBS',
            '부동산 자금조달',
            '리츠·부동산 펀드',
        ],
        '10': [
            '부동산 정책 — 토지·주택',
            '정책 효과 분석',
            '부동산 조세',
            '기타 — ESG·디지털 부동산',
        ],
    },
    'appraisal_law': {
        '01': [
            '행정법 의의·법원',
            '행정법 일반원칙 — 비례·신뢰보호',
            '행정법관계 — 공권·공의무',
            '특별권력관계',
            '행정법관계의 변동',
        ],
        '02': [
            '행정입법 — 법규명령·행정규칙',
            '행정행위 — 의의·성립요건',
            '행정행위 — 분류·재량·기속',
            '행정행위 — 부관(조건·기한·부담)',
            '행정행위 — 하자·취소·철회',
            '확약·공법상 사실행위',
        ],
        '03': [
            '행정계획 — 의의·법적 성질',
            '계획재량·형량명령',
            '인허가의제 — 의의·요건',
            '공법상 계약',
        ],
        '04': [
            '행정절차 — 의견청취·이유제시',
            '청문·공청회·의견제출',
            '실효성확보수단 — 강제집행',
            '직접강제·이행강제금·과징금',
            '행정조사',
        ],
        '05': [
            '행정심판 — 의의·종류',
            '취소소송 — 원고적격·대상적격 ★',
            '취소소송 — 협의의 소익',
            '취소소송 — 제소기간·관할',
            '취소소송 — 본안판단',
            '무효등확인소송·부작위위법확인',
            '당사자소송·기관소송',
        ],
        '06': [
            '국가배상 — 공무원·공공시설',
            '국가배상 — 요건·법리',
            '손해배상 vs 손실보상',
            '결과제거청구',
        ],
        '07': [
            '공용수용 — 의의·요건 ★★',
            '사업인정 — 의의·효과 (2011두1051)',
            '사업인정 — 절차·고시·실효',
            '재결 — 의의·신청·절차',
            '재결신청청구 (2011두2309)',
            '협의성립확인 (2018두57865)',
            '약식절차 — 천재지변·시급',
        ],
        '08': [
            '손실보상 — 의의·법적 근거 ★★★',
            '보상기준 — 정당보상·공시지가',
            '잔여지 수용 (2008두822, 2014두46669)',
            '환매권 — 요건·행사',
            '이주대책 (92다35783 전합)',
            '주거이전비 (2011두3685)',
            '생활보상 — 의의·범위',
            '영업손실보상',
        ],
        '09': [
            '부동산 가격공시 — 의의·체계',
            '표준지 공시지가 — 결정·이의',
            '개별공시지가 — 산정·정정',
            '표준주택·개별주택 공시',
            '비주거용 부동산공시',
        ],
        '10': [
            '감정평가법 — 평가사 의무·책임',
            '평가사 — 자격·등록·징계',
            '감정평가법인',
            '도시정비법 — 정비사업 개관',
            '재개발·재건축 — 분양·관리처분',
        ],
    },
}


def build(subject_id, conf):
    print(f'\n[{subject_id}] {conf["title"]}')
    base = os.path.join(DEST, subject_id)
    units = []
    explicit_map = EXPLICIT_TOPICS.get(subject_id, {})
    for code, (title, subtitle, freq) in conf['unit_titles'].items():
        unit_file = f'units/{code}.md'
        problems_file = f'problems/{code}.md'
        unit_full = os.path.join(base, unit_file)
        problems_full = os.path.join(base, problems_file)
        exists = os.path.exists(unit_full)
        p_exists = os.path.exists(problems_full)
        # 명시적 topic 우선, 없으면 자동 추출 fallback
        explicit = explicit_map.get(code)
        if explicit:
            topics_arr = [
                {
                    'id': f'{code}-{i+1}',
                    'title': t,
                    'section_lines': [1, 999999],   # 단원 전체에서 검색
                }
                for i, t in enumerate(explicit)
            ]
        else:
            topics_raw = extract_topics(unit_full) if exists else []
            topics_arr = [
                {
                    'id': f'{code}-{i+1}',
                    'title': t['name'],
                    'section_lines': [t['start'], t['end']],
                }
                for i, t in enumerate(topics_raw[:12])
            ]
        est = 60 + freq * 15
        units.append({
            'code': code,
            'title': title,
            'subtitle': subtitle,
            'frequency': freq,
            'unit_file': unit_file if exists else None,
            'problems_file': problems_file if p_exists else None,
            'est_minutes': est,
            'topics': topics_arr,
        })
    index = {
        'subject': conf['subject'],
        'subject_id': subject_id,
        'subject_short': conf['short'],
        'stage': 2,
        'exam': '감정평가사 2차',
        'essence': conf['essence'],
        'exam_meta': conf['exam_meta'],
        'units_dir': f'/data/study/{subject_id}/units',
        'problems_dir': f'/data/study/{subject_id}/problems',
        'handover_file': f'/data/study/{subject_id}/handover.md',
        'high_priority': conf['high_priority'],
        'study_progression': conf['study_progression'],
        'units': units,
        'default_unit': conf['study_progression'][0],
        'has_calc': conf.get('has_calc', False),
        'has_templates': conf.get('has_templates', False),
        'has_cases': conf.get('has_cases', False),
        'version': 'v1.0',
    }
    target = os.path.join(base, 'ai_index.json')
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    total_topics = sum(len(u['topics']) for u in units)
    print(f'  units={len(units)}, total topics={total_topics}')
    print(f'  → {target}')


if __name__ == '__main__':
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(SUBJECTS.keys())
    for sid in targets:
        if sid in SUBJECTS:
            build(sid, SUBJECTS[sid])
