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

import pypdf

PDF_PATH = Path('실무 문제 모음/감정평가실무 기출문제 예시답안 [제11회-제36회] [업데이트일_26.05.13].pdf')
OUT_PATH = Path('scripts/_cache/official_answers.json')

# 페이지 헤더 제거 패턴
HEADER_RE = re.compile(
    r'스터디파이터\s*실무\s*기출\s*예시답안.*?평가사\s*\d+', re.S
)
# 회차 시작 표시
ROUND_RE = re.compile(r'제(\d+)회')
# 문제 시작 표시
PROBLEM_RE = re.compile(r'\[문제(\d+)\]\s*(?:\((\d+)점\))?')


def extract_all_pages(pdf_path):
    """모든 페이지의 텍스트를 한 덩어리로. 페이지 헤더는 제거."""
    reader = pypdf.PdfReader(pdf_path)
    print(f'총 {len(reader.pages)} 페이지 추출 중...', file=sys.stderr)
    chunks = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        # 페이지 헤더 제거 — "스터디파이터 ... 평가사<N>" 패턴 (페이지 시작부)
        text = HEADER_RE.sub('', text)
        chunks.append(text)
        if (i + 1) % 50 == 0:
            print(f'  {i+1}/{len(reader.pages)} 페이지', file=sys.stderr)
    return '\n'.join(chunks)


def parse_rounds(full_text):
    """전체 텍스트를 회차·문제로 분리.
    구조: 제N회 → [문제M] → ... → [문제M+1] → ... → 제(N+1)회 → ...
    """
    # 회차로 split. 각 split의 첫 문자는 회차 번호.
    round_chunks = re.split(r'(제\d+회)', full_text)
    # round_chunks = ['preamble', '제11회', 'body of 11회', '제12회', 'body of 12회', ...]

    result = {}
    for i in range(1, len(round_chunks), 2):
        round_label = round_chunks[i]  # '제11회'
        body = round_chunks[i + 1] if i + 1 < len(round_chunks) else ''
        round_num_match = re.match(r'제(\d+)회', round_label)
        if not round_num_match:
            continue
        round_num = int(round_num_match.group(1))

        # 문제로 split
        problem_chunks = re.split(r'\[문제(\d+)\]\s*(?:\((\d+)점\))?', body)
        # problem_chunks = ['preamble', num1, points1, body1, num2, points2, body2, ...]

        if round_num not in result:
            result[round_num] = {}
        for j in range(1, len(problem_chunks), 3):
            if j + 2 >= len(problem_chunks):
                break
            q_num = int(problem_chunks[j])
            q_points = int(problem_chunks[j + 1]) if problem_chunks[j + 1] else None
            q_body = problem_chunks[j + 2].strip()
            # 답안 본문 cleanup (페이지 헤더 잔여물 등)
            q_body = HEADER_RE.sub('', q_body).strip()
            # 회차 끝부분에 다른 회차 답안 시작이 섞여있을 수 있음 — 이미 round split했으므로 안전
            # 단, 답안 내에 "제N회" 텍스트가 답안 본문에 등장할 수도 (조항 인용 등) - 무시
            result[round_num][q_num] = {
                'points': q_points,
                'body': q_body,
            }

    return result


def main():
    if not PDF_PATH.exists():
        print(f'ERROR: PDF not found: {PDF_PATH}', file=sys.stderr)
        sys.exit(1)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    full_text = extract_all_pages(PDF_PATH)
    print(f'\n총 텍스트 길이: {len(full_text)}자', file=sys.stderr)

    rounds = parse_rounds(full_text)
    total_problems = sum(len(p) for p in rounds.values())
    print(f'\n파싱 결과: {len(rounds)}회차, 총 {total_problems}문제', file=sys.stderr)

    # 회차별 문제 수
    for r in sorted(rounds.keys()):
        problems = rounds[r]
        avg_len = sum(len(p['body']) for p in problems.values()) / max(1, len(problems))
        print(f'  {r}회: {len(problems)}문제, 평균 답안 {avg_len:.0f}자')

    OUT_PATH.write_text(json.dumps(rounds, ensure_ascii=False), encoding='utf-8')
    print(f'\n저장: {OUT_PATH}')


if __name__ == '__main__':
    main()
