#!/usr/bin/env python3
"""
감정평가실무_기출문제지 [1-36회] PDF → 회차별 정확한 본문 추출.
기존 official(11~36회 부분)의 body를 정확한 PDF 본문으로 덮어쓰기.
기존에 없는 회차/문제(1-10회 등)는 'past' chapter로 신규 추가.

TOC 파싱 → 회차별 페이지 범위 → 본문 추출 → 【 문제 N 】으로 split
"""
import re
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

import pdfplumber

PDF_PATH = Path('실무 문제 모음/감정평가실무_기출문제지 [1-36회] [업데이트일_26.03.09] (1).pdf')
DATA_DIR = Path('viewer/public/data/essay/practice')

# 페이지 헤더 제거 (시험지 메타데이터)
HEADER_NOISE = [
    re.compile(r'\d{4}년도\s*제\d+회\s*감정평가사\s*\d+차\s*시험문제지\s*'),
    re.compile(r'교\s*시\s*시험과목\s*시험시간\s*수험번호\s*성\s*명\s*'),
    re.compile(r'\d+교시\s*감정평가실무\s*\d+분\s*'),
    re.compile(r'※\s*공통유의사항\s*'),
    re.compile(r'1\.\s*각\s*문제는\s*해답\s*산정시\s*산식과\s*도출과정을\s*반드시\s*기재할\s*것\.\s*'),
    re.compile(r'2\.\s*단가는.*?소수점\s*셋째자리까지\s*사정함\.\s*', re.S),
    re.compile(r'\d+\s*감정평가실무\s*\d+회\s*기출문제\s*STUDY\s*FIGHTER\s*'),
    re.compile(r'STUDY\s*FIGHTER\s*감정평가실무\s*\d+회\s*기출문제\s*\d*\s*', re.I),
]

# 문제 마커 (공백 포함 가능)
PROBLEM_RE = re.compile(
    r'【\s*문제\s*(\d+)\s*】'
    r'\s*(.*?)'
    r'(?=【\s*문제\s*\d+\s*】|\Z)',
    re.S
)
POINTS_RE = re.compile(r'\((\d+)점\)')


def parse_toc(text):
    """TOC 페이지 텍스트에서 (회차, 시작페이지) 추출."""
    # 패턴: "01회 기출문제 2", "13회 기출문제 160"
    result = []
    for m in re.finditer(r'(\d+)회\s*기출문제\s*(\d+)', text):
        round_num = int(m.group(1))
        page_num = int(m.group(2))
        result.append((round_num, page_num))
    return sorted(result)


def clean_body(text):
    """본문 cleanup — 헤더·푸터·시험지 메타데이터 제거."""
    cleaned = text
    for pat in HEADER_NOISE:
        cleaned = pat.sub('', cleaned)
    # 연속 빈 줄 정리
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
    # 각 라인 끝 공백
    lines = [l.rstrip() for l in cleaned.split('\n')]
    return '\n'.join(lines).strip()


def extract_round_problems(pdf, start_page, end_page):
    """페이지 범위에서 텍스트 추출 + 문제 분리."""
    # PDF는 0-index, TOC는 1-index
    texts = []
    for i in range(start_page - 1, min(end_page - 1, len(pdf.pages))):
        text = pdf.pages[i].extract_text() or ''
        texts.append(text)
    full_text = '\n'.join(texts)
    full_text = clean_body(full_text)

    problems = []
    for m in PROBLEM_RE.finditer(full_text):
        q_num = int(m.group(1))
        body = m.group(2).strip()
        # 본문 head에서 배점 추출
        pts_m = POINTS_RE.search(body[:300])
        problems.append({
            'qNum': q_num,
            'points': int(pts_m.group(1)) if pts_m else None,
            'body': body,
        })
    return problems


def main():
    if not PDF_PATH.exists():
        print(f'ERROR: PDF not found: {PDF_PATH}', file=sys.stderr)
        sys.exit(1)

    with pdfplumber.open(PDF_PATH) as pdf:
        print(f'총 {len(pdf.pages)} 페이지')

        # TOC 페이지에서 회차→시작페이지
        toc_text = pdf.pages[0].extract_text()
        toc = parse_toc(toc_text)
        print(f'TOC 회차 수: {len(toc)}')
        print(f'  처음 5: {toc[:5]}')
        print(f'  마지막 5: {toc[-5:]}')

        # 회차별 페이지 범위
        round_ranges = []
        for k, (rnum, start) in enumerate(toc):
            end = toc[k+1][1] if k+1 < len(toc) else len(pdf.pages) + 1
            round_ranges.append((rnum, start, end))

        # 회차별 문제 추출
        all_extracted = []  # [(round, qNum, body, points)]
        for rnum, start, end in round_ranges:
            problems = extract_round_problems(pdf, start, end)
            for p in problems:
                all_extracted.append({
                    'round': rnum,
                    'qNum': p['qNum'],
                    'body': p['body'],
                    'points': p['points'],
                })
            print(f'  {rnum:>2}회 (p{start}-{end-1}): {len(problems)}문제')

    print(f'\n총 추출: {len(all_extracted)}문제\n')

    # 기존 official 데이터의 (round, qNum) → (chapter_id, q_dict)
    chapter_files = ['2a', '3', '4', '5', '6a', '6b', '7', '8a', '8b']
    location_map = {}   # (round, qNum) → (chapter_id, idx_in_chapter)
    for cid in chapter_files:
        p = DATA_DIR / f'{cid}.json'
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding='utf-8'))
        for i, q in enumerate(d['questions']):
            r = q.get('round')
            n = q.get('questionNum')
            if r and n:
                location_map[(int(r), int(n))] = (cid, i)
    print(f'기존 official 매핑: {len(location_map)}개 (round, qNum)\n')

    # 본문 교체 + 신규 추가
    replaced = 0
    new_past = []
    chapter_data = {}  # cid → data
    for ex in all_extracted:
        key = (ex['round'], ex['qNum'])
        if key in location_map:
            cid, idx = location_map[key]
            if cid not in chapter_data:
                chapter_data[cid] = json.loads((DATA_DIR / f'{cid}.json').read_text(encoding='utf-8'))
            q = chapter_data[cid]['questions'][idx]
            q['body'] = ex['body']        # 본문 교체
            if ex['points'] and not q.get('points'):
                q['points'] = ex['points']
            q['bodySource'] = 'pdf-1-36회'  # 출처 표시
            replaced += 1
        else:
            # 기존에 없음 → 'past' chapter에 추가
            new_past.append({
                'id': f'past-r{ex["round"]}-q{ex["qNum"]}',
                'subject': '감정평가실무',
                'chapter': 'past',
                'source': 'official',
                'round': ex['round'],
                'questionNum': ex['qNum'],
                'points': ex['points'],
                'body': ex['body'],
                'modelAnswer': None,
                'modelAnswerSource': None,
            })

    # 기존 chapter 저장
    for cid, d in chapter_data.items():
        p = DATA_DIR / f'{cid}.json'
        p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    print(f'기존 본문 교체: {replaced}개')

    # 'past' chapter 저장
    if new_past:
        past = {
            'built_at': datetime.now(timezone.utc).isoformat(),
            'subject': '감정평가실무',
            'chapter': 'past',
            'chapterTitle': '기출 전회차 (단원 미분류)',
            'source': 'official',
            'count': len(new_past),
            'withAnswer': 0,
            'matchedAnswer': 0,
            'rounds': sorted(set(q['round'] for q in new_past)),
            'questions': new_past,
        }
        (DATA_DIR / 'past.json').write_text(json.dumps(past, ensure_ascii=False), encoding='utf-8')
        print(f'신규 past chapter: {len(new_past)}문제')

    # manifest 갱신
    mpath = DATA_DIR / 'manifest.json'
    m = json.loads(mpath.read_text(encoding='utf-8'))
    existing_ids = {c['id'] for c in m['chapters']}
    if 'past' not in existing_ids and new_past:
        m['chapters'].append({
            'id': 'past',
            'title': '기출 전회차 (단원 미분류)',
            'file': 'past.json',
            'count': len(new_past),
            'withAnswer': 0,
            'matchedAnswer': 0,
            'rounds': sorted(set(q['round'] for q in new_past)),
            'generatedCount': 0,
        })
    m['total'] = sum(c['count'] for c in m['chapters'])
    mpath.write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')
    print(f'\nmanifest 갱신: 총 {m["total"]}문제, {len(m["chapters"])}개 chapter')


if __name__ == '__main__':
    main()
