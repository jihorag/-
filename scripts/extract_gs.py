#!/usr/bin/env python3
"""
GS 모의고사 PDF (1기·2기) → 회차별 문제 추출.
- 페이지 헤더: "스터디파이터 25년 2차 대비 실무 N기 X-Y회차 문제 ..."
- 문제 마커: 【문제 N】 ... (XX점) [- N회 M번]
- 자료: < 자료 N > ...
- 답안 없음 (PDF 자체에 미수록) → 자기채점만 가능

출력: viewer/public/data/essay/practice/gs1.json, gs2.json
manifest 갱신
"""
import re
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

import pdfplumber

DATA_DIR = Path('viewer/public/data/essay/practice')

PDF_SOURCES = [
    {
        'id': 'gs1',
        'title': 'GS 1기 모의고사 (20회분)',
        'path': Path('실무 문제 모음/25년대비 실무1기GS 문제 및 예시답안 모음 [총20회분] [업데이트일_26.02.13].pdf'),
    },
    {
        'id': 'gs2',
        'title': 'GS 2기 모의고사 (10회분)',
        'path': Path('실무 문제 모음/25년대비 실무2기GS 문제 및 예시답안 모음 [총10회분] [업데이트일_26.01.18].pdf'),
    },
]

# 헤더에서 회차 추출
HEADER_RE = re.compile(r'스터디파이터.*?(\d+[-]\d+회차|\d+주차)\s*(문제|답안|예시답안)?')
# 페이지 헤더 라인 (제거용)
HEADER_LINE_RE = re.compile(r'^스터디파이터.*?평가사\s*\d+\s*$', re.M)
# 문제 마커
PROBLEM_RE = re.compile(
    r'【\s*문제\s*(\d+)\s*】'   # 문제 번호
    r'\s*(.*?)'                # 본문 (탐욕 X)
    r'(?=\s*【\s*문제\s*\d+\s*】|\Z)',  # 다음 문제 마커 또는 끝
    re.S
)
# 배점·기출 출처 매칭 (보통 본문 끝부분)
POINTS_RE = re.compile(r'\((\d+)점\)')
SOURCE_RE = re.compile(r'-\s*(\d+)회\s*(\d+)번')


def map_pages_to_rounds(pdf):
    """페이지 → 회차 매핑."""
    page_to_round = {}
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ''
        first_line = text.split('\n')[0] if text else ''
        m = HEADER_RE.search(first_line)
        if m:
            page_to_round[i] = m.group(1)
    return page_to_round


def round_to_pages(page_to_round, total_pages):
    """회차별 페이지 범위 도출."""
    result = {}   # round → [page_indices]
    for i in range(total_pages):
        r = page_to_round.get(i)
        if r:
            result.setdefault(r, []).append(i)
    return result


def extract_round_text(pdf, page_indices):
    """회차 모든 페이지 텍스트 합치기 + 헤더 제거."""
    parts = []
    for idx in page_indices:
        text = pdf.pages[idx].extract_text() or ''
        text = HEADER_LINE_RE.sub('', text).strip()
        parts.append(text)
    return '\n'.join(parts)


def parse_problems(round_text, round_label):
    """회차 본문 → 문제 list."""
    problems = []
    for m in PROBLEM_RE.finditer(round_text):
        q_num = int(m.group(1))
        body = m.group(2).strip()
        # 본문 head 부분에서 배점·출처 추출
        head = body[:200]
        pts_m = POINTS_RE.search(head)
        src_m = SOURCE_RE.search(head)
        problems.append({
            'qNum': q_num,
            'points': int(pts_m.group(1)) if pts_m else None,
            'sourceRound': int(src_m.group(1)) if src_m else None,
            'sourceQNum': int(src_m.group(2)) if src_m else None,
            'body': body,
        })
    return problems


def process_pdf(src):
    """단일 PDF 처리 → 모든 회차 문제 추출."""
    if not src['path'].exists():
        print(f'  ERROR: PDF not found: {src["path"]}', file=sys.stderr)
        return None

    print(f'\n=== {src["id"]} · {src["title"]} ===')
    with pdfplumber.open(src['path']) as pdf:
        print(f'  총 {len(pdf.pages)} 페이지')
        page_to_round = map_pages_to_rounds(pdf)
        print(f'  헤더 인식: {len(page_to_round)}/{len(pdf.pages)}')

        round_pages = round_to_pages(page_to_round, len(pdf.pages))
        print(f'  회차 수: {len(round_pages)}')

        all_problems = []
        for r_label in sorted(round_pages.keys(),
                              key=lambda x: tuple(int(n) for n in re.findall(r'\d+', x))):
            indices = round_pages[r_label]
            round_text = extract_round_text(pdf, indices)
            probs = parse_problems(round_text, r_label)
            for p in probs:
                qid = f'{src["id"]}-{r_label.replace("-", "_")}-q{p["qNum"]}'
                source_link = f'v3-r{p["sourceRound"]}-q{p["sourceQNum"]}' if p['sourceRound'] else None
                all_problems.append({
                    'id': qid,
                    'subject': '감정평가실무',
                    'chapter': src['id'],
                    'source': 'gs',
                    'gsRound': r_label,        # "1-1회차"
                    'questionNum': p['qNum'],
                    'points': p['points'],
                    'body': p['body'],
                    'modelAnswer': None,        # GS에는 답안 없음
                    'modelAnswerSource': None,
                    'sourceRound': p['sourceRound'],   # 기출 출처: N회
                    'sourceQNum': p['sourceQNum'],     # 기출 출처: N번
                    'sourceLink': source_link,
                })
            print(f'  {r_label}: {len(probs)}문제')
        print(f'  ★ 총 {len(all_problems)}개 문제 추출')
        return all_problems


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    chapter_meta = []
    now = datetime.now(timezone.utc).isoformat()

    for src in PDF_SOURCES:
        problems = process_pdf(src)
        if not problems:
            continue
        out = {
            'built_at': now,
            'subject': '감정평가실무',
            'chapter': src['id'],
            'chapterTitle': src['title'],
            'source': 'gs',
            'count': len(problems),
            'withAnswer': 0,
            'matchedAnswer': 0,
            'rounds': sorted(set(p['gsRound'] for p in problems),
                             key=lambda x: tuple(int(n) for n in re.findall(r'\d+', x))),
            'questions': problems,
        }
        out_path = DATA_DIR / f'{src["id"]}.json'
        out_path.write_text(json.dumps(out, ensure_ascii=False), encoding='utf-8')
        size_kb = out_path.stat().st_size // 1024
        print(f'  → wrote {out_path.name} ({size_kb} KB)')
        chapter_meta.append({
            'id': src['id'],
            'title': src['title'],
            'file': f'{src["id"]}.json',
            'count': len(problems),
            'withAnswer': 0,
            'matchedAnswer': 0,
            'rounds': out['rounds'],
            'generatedCount': 0,
        })

    # manifest 갱신 — 기존 chapter에 GS 추가
    mpath = DATA_DIR / 'manifest.json'
    m = json.loads(mpath.read_text(encoding='utf-8'))
    existing_ids = {c['id'] for c in m['chapters']}
    for new_c in chapter_meta:
        if new_c['id'] in existing_ids:
            # 갱신
            for c in m['chapters']:
                if c['id'] == new_c['id']:
                    c.update(new_c)
        else:
            m['chapters'].append(new_c)
    # total 재계산
    m['total'] = sum(c['count'] for c in m['chapters'])
    m['classified'] = sum(c.get('matchedAnswer', 0) for c in m['chapters'])
    mpath.write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')
    print(f'\nmanifest 갱신: 총 {m["total"]}문제, {len(m["chapters"])}개 chapter')


if __name__ == '__main__':
    main()
