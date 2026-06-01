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
        # 문서 종류 헤더(목차/마인드/요약/기본서/워크북) 건너뛰기
        if any(k in name for k in ['본문 목차', '마인드 강의', '핵심요약서', '기본서', '워크북', '시험직전']):
            continue
        topics.append({'name': name, 'start': i, 'end': total})
    # end 보정 (다음 ## 헤더 직전)
    for i in range(len(topics) - 1):
        topics[i]['end'] = topics[i + 1]['start'] - 1
    return topics


def build(subject_id, conf):
    print(f'\n[{subject_id}] {conf["title"]}')
    base = os.path.join(DEST, subject_id)
    units = []
    for code, (title, subtitle, freq) in conf['unit_titles'].items():
        unit_file = f'units/{code}.md'
        problems_file = f'problems/{code}.md'
        unit_full = os.path.join(base, unit_file)
        problems_full = os.path.join(base, problems_file)
        exists = os.path.exists(unit_full)
        p_exists = os.path.exists(problems_full)
        topics_raw = extract_topics(unit_full) if exists else []
        # 너무 많으면 상위 8개만
        topics = topics_raw[:12]
        # 추정 학습 시간 — 빈도·content 양 기반
        est = 60 + freq * 15
        units.append({
            'code': code,
            'title': title,
            'subtitle': subtitle,
            'frequency': freq,
            'unit_file': unit_file if exists else None,
            'problems_file': problems_file if p_exists else None,
            'est_minutes': est,
            'topics': [
                {
                    'id': f'{code}-{i+1}',
                    'title': t['name'],
                    'section_lines': [t['start'], t['end']],
                }
                for i, t in enumerate(topics)
            ],
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
