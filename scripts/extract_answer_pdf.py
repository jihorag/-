#!/usr/bin/env python3
"""
스터디파이터 실무 기출 예시답안 PDF에서 회차·문제번호별 답안을 추출.
출력: scripts/_cache/official_answers.json
구조: { "11회": { "1": "...답안...", "2": "..." }, "12회": {...}, ... }
"""
import re
import json
import sys
from pathlib import Path

import pdfplumber

PDF_PATH = Path('실무 문제 모음/감정평가실무 기출문제 예시답안 [제11회-제36회] [업데이트일_26.05.13].pdf')
OUT_PATH = Path('scripts/_cache/official_answers.json')

# 페이지 헤더 제거: "스터디파이터 실무 기출 예시답안(11~36회) 강사 : 윤철신 평가사 N" + 다음 줄
HEADER_LINE_RE = re.compile(r'^스터디파이터.*?평가사\s*\d+\s*$', re.M)
# 회차 시작 표시 — 페이지 단위에서 검색
ROUND_RE = re.compile(r'^\s*제\s*(\d+)\s*회\s*$', re.M)
# 문제 시작 표시
PROBLEM_RE = re.compile(r'\[문제\s*(\d+)\]\s*(?:\((\d+)점\))?')


def extract_pages(pdf_path):
    """페이지별로 텍스트 추출 + 페이지 헤더 제거."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        print(f'총 {len(pdf.pages)} 페이지 추출 중...', file=sys.stderr)
        for i, p in enumerate(pdf.pages):
            text = p.extract_text() or ''
            text = HEADER_LINE_RE.sub('', text).strip()
            pages.append(text)
            if (i + 1) % 50 == 0:
                print(f'  {i+1}/{len(pdf.pages)} 페이지', file=sys.stderr)
    return pages


def find_round_starts(pages):
    """회차 시작 페이지 찾기.
    전략: "제N회" 라벨 명시되어 있으면 그것 우선, 없으면 [문제1] 첫 등장으로 추정.
    회차 번호는 첫 발견 회차에서 시작해 [문제1] 등장마다 +1.
    """
    explicit = []   # [(page_idx, round_num)]
    problem1_pages = []  # 페이지 안에 [문제1]이 등장하는 인덱스
    for i, page_text in enumerate(pages):
        m = ROUND_RE.search(page_text)
        if m:
            explicit.append((i, int(m.group(1))))
        # [문제1] 등장하면서 그 이전 라인에 다른 [문제N] 안 보일 때 = 페이지 첫 머리에 등장
        # 단순화: 페이지 내 첫 PROBLEM_RE 매치가 [문제1]이면 회차 시작 추정
        first_problem = PROBLEM_RE.search(page_text)
        if first_problem and int(first_problem.group(1)) == 1:
            problem1_pages.append(i)

    # explicit 회차들을 anchor로 사용. 그 사이를 [문제1] 페이지로 보간.
    # 가장 명확한 케이스: explicit에 (page=0, round=11), (page=20, round=12) 있으면
    # 13회 시작은 그 다음 [문제1] 등장 페이지 (page > 20).
    starts = []
    if not problem1_pages:
        return explicit

    # 회차 번호 추정: 첫 explicit anchor (보통 11회) 기준으로 [문제1] 페이지 순서대로 +1
    if explicit:
        anchor_page, anchor_round = explicit[0]
    else:
        anchor_page, anchor_round = problem1_pages[0], 11

    # 첫 anchor 이후의 [문제1] 페이지들을 순차적으로 12회, 13회, ... 로 매핑
    # 단, 같은 페이지에 [문제1]이 2번 나오면 중복 제거됨 (set 사용)
    valid_starts = [p for p in problem1_pages if p >= anchor_page]
    # 너무 가까이 있는 [문제1] 은 같은 회차의 사례·문제 번호 재시작일 수 있음 (보통 5-15 페이지 간격)
    filtered = []
    for p in valid_starts:
        if not filtered or p - filtered[-1] >= 3:  # 최소 3페이지 간격
            filtered.append(p)

    # 회차 번호 부여: 첫 회차 = anchor_round, 이후 +1
    for idx, p in enumerate(filtered):
        starts.append((p, anchor_round + idx))
    return starts


def parse_rounds(pages, starts):
    """starts 정보로 페이지 범위를 회차별로 묶고, 각 회차 텍스트를 [문제N]으로 분리."""
    result = {}
    for k, (start_page, round_num) in enumerate(starts):
        end_page = starts[k + 1][0] if k + 1 < len(starts) else len(pages)
        # 회차 페이지들 합치기
        round_text = '\n'.join(pages[start_page:end_page])
        # "제N회" 표시 제거 (이미 처리됨)
        round_text = ROUND_RE.sub('', round_text)
        # [문제N]로 분리
        chunks = PROBLEM_RE.split(round_text)
        # chunks = ['preamble', num1, points1, body1, num2, points2, body2, ...]
        problems = {}
        for j in range(1, len(chunks), 3):
            if j + 2 >= len(chunks):
                break
            try:
                q_num = int(chunks[j])
                q_points = int(chunks[j + 1]) if chunks[j + 1] else None
                q_body = chunks[j + 2].strip()
                problems[q_num] = {'points': q_points, 'body': q_body, 'pages': [start_page+1, end_page]}
            except (ValueError, TypeError):
                continue
        if problems:
            result[round_num] = problems
    return result


def main():
    if not PDF_PATH.exists():
        print(f'ERROR: PDF not found: {PDF_PATH}', file=sys.stderr)
        sys.exit(1)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    pages = extract_pages(PDF_PATH)
    print(f'\n페이지 추출 완료', file=sys.stderr)

    starts = find_round_starts(pages)
    print(f'회차 시작 페이지 {len(starts)}개 발견:', [(p+1, r) for p, r in starts[:30]])

    rounds = parse_rounds(pages, starts)
    total_problems = sum(len(p) for p in rounds.values())
    print(f'\n파싱 결과: {len(rounds)}회차, 총 {total_problems}문제\n')

    for r in sorted(rounds.keys()):
        problems = rounds[r]
        avg_len = sum(len(p['body']) for p in problems.values()) / max(1, len(problems))
        pages_range = next(iter(problems.values())).get('pages')
        print(f'  {r}회: {len(problems)}문제, 평균 답안 {avg_len:.0f}자, 페이지 {pages_range}')

    OUT_PATH.write_text(json.dumps(rounds, ensure_ascii=False), encoding='utf-8')
    print(f'\n저장: {OUT_PATH} ({OUT_PATH.stat().st_size//1024}KB)')


if __name__ == '__main__':
    main()
