#!/usr/bin/env python3
"""난이도 자동 재분류 — 본질 기준 (방식 수·자료 수·물음 수·시산조정·시나리오)."""
import json
import re
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')

# 평가 방식 키워드
METHOD_KEYWORDS = [
    '공시지가기준법', '거래사례비교법', '원가법', '수익환원법',
    '임대사례비교법', '적산법', '수익분석법',
]

# 시산조정·종합 키워드
INTEGRATION_KEYWORDS = [
    '시산조정', '시산가액', '가중치', '결정가액',
    '시나리오', 'vs', '비교', '선택', '권장', '의사결정',
    '판단', '결정', '의견',
]

# 그밖의요인·종합 보정
COMPREHENSIVE_KEYWORDS = [
    '그밖의요인', '6대 요인', '6대 조건', '시점수정', '사정보정',
    '비교표준지', '보상선례',
]


def count_methods(text):
    """방식 수 (중복 제거)"""
    found = set()
    for kw in METHOD_KEYWORDS:
        if kw in text:
            found.add(kw)
    return len(found)


def count_data_sections(body):
    """자료 [자료 01], [자료 02] 등 갯수"""
    matches = re.findall(r'\[\s*자료\s*\d+\s*\]', body)
    return len(matches)


def count_questions(body):
    """[물음] 또는 [물음] 후 번호 갯수"""
    # [물음] 섹션 찾기
    if '[ 물음 ]' in body or '[물음]' in body:
        # [물음] 이후 텍스트
        idx = body.find('물음')
        if idx < 0:
            return 1
        after = body[idx:]
        # 번호 매김 (1. 2. 3...)
        nums = re.findall(r'^\s*(\d+)\.\s', after, re.MULTILINE)
        if nums:
            return len(set(nums))
    # 물음 섹션 없으면 body 전체에서 번호 찾기
    nums = re.findall(r'^\s*(\d+)\.\s', body, re.MULTILINE)
    return len(set(nums)) if nums else 1


def has_integration(text):
    """시산조정·시나리오 키워드 있나"""
    return any(kw in text for kw in INTEGRATION_KEYWORDS)


def is_comprehensive(text):
    """종합 보정 (그밖의요인 등) 키워드"""
    return any(kw in text for kw in COMPREHENSIVE_KEYWORDS)


def classify_difficulty(q):
    """본질 기준 난이도 판별

    1 입문: 개념·약술 (방식 0~1, 자료 0, 물음 1~2)
    2 기초: 단순 계산 (방식 1, 자료 1~2, 물음 1~3, 단순 산식)
    3 표준: 종합 계산 (방식 1, 자료 3+, 물음 3+, 종합 보정)
    4 응용: 다중 적용 (방식 2~3, 시산조정 ◯)
    5 고난도: 복합 종합 (방식 3+, 자료 5+, 물음 4+, 시산조정+판단)
    """
    body = q.get('body', '')
    body_len = len(body)
    points = q.get('points') or 10

    methods = count_methods(body)
    data_n = count_data_sections(body)
    question_n = count_questions(body)
    integration = has_integration(body)
    comprehensive = is_comprehensive(body)

    # 입문 — 개념·약술
    if body_len < 200 and methods <= 1 and data_n == 0 and points <= 15:
        return 1

    # 기초 — 단순 계산
    if data_n <= 2 and question_n <= 3 and methods <= 1 and not integration:
        if body_len < 600:
            return 2
        return 3  # 길이 길면 표준으로

    # 고난도 — 복합 종합 (최우선 체크)
    if methods >= 3 and data_n >= 5 and question_n >= 4 and integration:
        return 5
    if data_n >= 6 and question_n >= 5 and integration:
        return 5
    if body_len >= 1500 and methods >= 2 and data_n >= 4 and integration:
        return 5

    # 응용 — 다중 적용
    if methods >= 2 and integration:
        return 4
    if data_n >= 4 and question_n >= 3 and (integration or comprehensive):
        return 4
    if methods >= 2 and data_n >= 3:
        return 4

    # 표준 — 종합 계산
    if data_n >= 2 and question_n >= 2:
        return 3
    if comprehensive and data_n >= 2:
        return 3

    # 기본 = 기초
    return 2


def assign_points(diff):
    """난이도별 표준 점수 (기존 점수 유지가 원칙, 명백 불일치 시만 조정)"""
    return {1: 10, 2: 15, 3: 25, 4: 35, 5: 45}[diff]


def main():
    summary = {}
    changes = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    total_changed = 0

    for ch in ['2a', '3', '4', '5', '6a', '6b', '7', '8a', '8b']:
        path = DATA_DIR / f'{ch}.json'
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding='utf-8'))

        dist = {1:0, 2:0, 3:0, 4:0, 5:0}
        for q in data['questions']:
            if q.get('source') != 'practice-set':
                continue
            old_diff = q.get('difficulty', 0)
            new_diff = classify_difficulty(q)
            dist[new_diff] = dist.get(new_diff, 0) + 1
            if old_diff != new_diff:
                q['difficulty'] = new_diff
                # 점수는 기존 유지 (큰 변화 없는 한)
                if abs((q.get('points') or 10) - assign_points(new_diff)) > 20:
                    q['points'] = assign_points(new_diff)
                total_changed += 1

        summary[ch] = dist
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    # 전체 요약
    print(f'=== 총 {total_changed}개 재분류 ===\n')
    print('단원별 새 분포:')
    total_dist = {1:0, 2:0, 3:0, 4:0, 5:0}
    for ch, dist in summary.items():
        total_dist = {k: total_dist[k] + dist.get(k, 0) for k in total_dist}
        print(f"  {ch:4s}: {dist}")
    print(f"\n  전체: {total_dist}")


if __name__ == '__main__':
    main()
