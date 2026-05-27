#!/usr/bin/env python3
# build_essay.py — 2차 essay 문제 파서 (Python 버전, node 없는 환경용)
#
# 입력: 최종산출물/2과목_2차_감정평가실무/문제_*.md
# 출력: viewer/public/data/essay/practice/<chapter>.json + manifest.json
#
# 파싱 대상: `## 🎯 기출문제 + 답안` 섹션만 (워크북·GS는 v1에서 제외)
# 문제 단위: `【 문제 N 】` · 답안 단위: `[문제#N]`
# 라운드 단위: `### 기출 제N회`
#
# Vercel 빌드용 build_essay.mjs와 동일한 출력을 만들어야 함.

import re, json, sys, os, hashlib
from pathlib import Path
from datetime import datetime, timezone

SRC = Path('최종산출물/2과목_2차_감정평가실무')
DEST = Path('viewer/public/data/essay/practice')
SUBJECT = '감정평가실무'

# 파일명: 문제_2a_3방식기초_공시지가·거래사례·원가.md
CHAPTER_RE = re.compile(r'^문제_([0-9]+[a-z]?)_(.+)\.md$')
KICHUL_SEC_RE = re.compile(r'^##\s.*🎯\s*기출.*$', re.M)
NEXT_SECTION_RE = re.compile(r'^##\s', re.M)
ROUND_SPLIT_RE = re.compile(r'^###\s*기출\s*제(\d+)회[^\n]*\n', re.M)
PROBLEM_HEADER_RE = re.compile(r'^####\s*📝\s*문제\s*$', re.M)
ANSWER_HEADER_RE = re.compile(r'^####\s*✅\s*답안[^\n]*$', re.M)
PROBLEM_MARK_RE = re.compile(r'【\s*문제\s*(\d+)\s*】')
# 답안 마커: 앞에 회차 번호가 있을 수 있음 (예: "19회 [문제#1]" — 다음 회차가 같은 섹션에 섞여 있음)
# group(1) = 다음 회차 번호 (있으면), group(2) = 문제 번호, group(3) = 배점
ANSWER_MARK_RE = re.compile(r'(?:(\d+)회\s*)?\[문제\s*#(\d+)\]\s*(?:\((\d+)점\))?')
POINTS_RE = re.compile(r'\((\d+)\s*점\)')

# 본문 오염 패턴 (PDF 변환 시 끼어든 페이지 헤더/푸터/카피라이트)
NOISE_PATTERNS = [
    re.compile(r'^STUDY\s*FIGHTER\b.*$', re.M | re.I),
    re.compile(r'^스터디파이터\b.*$', re.M),
    re.compile(r'^\s*\d+\s*$', re.M),  # 페이지 번호 단독 라인
    re.compile(r'<!--p\.\d+-->'),
    re.compile(r'^감정평가실무\s+\d+회?\s*기출문제\s*$', re.M),
    re.compile(r'^.{0,3}교\s*시\s+시험과목\s+시험시간.*$', re.M),
    re.compile(r'^감정평가실무\s+\d+분\s*$', re.M),
    re.compile(r'^\d{4}년도\s+제\d+회\s+감정평가사\s+\d+차\s+시험문제지\s*$', re.M),
]

# 답안 휴리스틱 줄바꿈: PDF 변환에서 줄바꿈 소실된 답안에 가독성용 break 삽입
ANSWER_BREAK_BEFORE = re.compile(r'(?<![\n])(?=(?:Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ)\.)')
ANSWER_BREAK_NUM = re.compile(r'(?<=[^\n])(?=(?:\d+\.\s|\(\d+\)|①|②|③|④|⑤|⑥))')

def short_id(s: str) -> str:
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:8]

def clean_body(text: str) -> str:
    # 알려진 oise 패턴 제거 (페이지 헤더/푸터, 카피라이트, 시험지 헤더 등)
    for pat in NOISE_PATTERNS:
        text = pat.sub('', text)
    # 줄 시작 공백 보존하되 끝 공백 정리
    lines = [l.rstrip() for l in text.split('\n')]
    # 연속 빈 줄 1개로 축소
    out = []
    blank = False
    for l in lines:
        if not l.strip():
            if blank: continue
            blank = True
        else:
            blank = False
        out.append(l)
    return '\n'.join(out).strip()


def enhance_answer(text: str) -> str:
    """PDF에서 줄바꿈이 소실된 답안에 휴리스틱 줄바꿈을 추가해 가독성 ↑."""
    if not text:
        return text
    cleaned = clean_body(text)
    # Roman 숫자 절 앞에 줄바꿈
    cleaned = ANSWER_BREAK_BEFORE.sub('\n', cleaned)
    # 숫자/괄호 절 앞에 줄바꿈 (이미 줄 시작인 건 제외 — 룩비하인드 처리)
    cleaned = ANSWER_BREAK_NUM.sub('\n', cleaned)
    # 연속 줄바꿈 1개로
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()

def parse_chapter(md_text: str, chapter_id: str, source_file: str):
    """기출 섹션 내 모든 문제를 추출. 각 문제는 dict 1개."""
    m = KICHUL_SEC_RE.search(md_text)
    if not m:
        return []
    section_start = m.end()
    next_sec = NEXT_SECTION_RE.search(md_text, section_start)
    section_end = next_sec.start() if next_sec else len(md_text)
    section = md_text[section_start:section_end]

    # 회차로 split: parts = [preamble, round1, body1, round2, body2, ...]
    parts = ROUND_SPLIT_RE.split(section)
    results = []
    rounds_seen = set()
    for i in range(1, len(parts), 2):
        round_num = int(parts[i])
        if round_num in rounds_seen:
            # 같은 회차 중복 (예: 두 번 등장) — 합치지 말고 첫 번째만 사용
            continue
        rounds_seen.add(round_num)
        round_body = parts[i+1] if i+1 < len(parts) else ''

        # 다음 ### 또는 EOF 까지 (위에서 이미 회차 split했으므로 round_body는 한 회차 분량)
        # 그 안에 #### 📝 문제 → #### ✅ 답안 → (그 다음 #### 또는 EOF)
        prob_m = PROBLEM_HEADER_RE.search(round_body)
        ans_m = ANSWER_HEADER_RE.search(round_body)
        if not prob_m:
            continue
        prob_start = prob_m.end()
        if ans_m:
            prob_end = ans_m.start()
            ans_start = ans_m.end()
            # 답안은 끝까지 (회차 내 더 없음)
            ans_end = len(round_body)
        else:
            prob_end = len(round_body)
            ans_start = ans_end = None

        problem_text = round_body[prob_start:prob_end]
        answer_text = round_body[ans_start:ans_end] if ans_start is not None else ''

        # 문제 split
        prob_iter = list(PROBLEM_MARK_RE.finditer(problem_text))
        problems = {}
        for j, pm in enumerate(prob_iter):
            n = int(pm.group(1))
            body_start = pm.end()
            body_end = prob_iter[j+1].start() if j+1 < len(prob_iter) else len(problem_text)
            body = clean_body(problem_text[body_start:body_end])
            pts_m = POINTS_RE.search(body[:300])
            points = int(pts_m.group(1)) if pts_m else None
            problems[n] = {'body': body, 'points': points}

        # 답안 split — 같은 답안 섹션에 다음 회차 답안이 섞여 있을 수 있어 round-aware하게 처리
        # 패턴: (?:(\d+)회)?\[문제#(\d+)\] — 회차 번호가 있으면 그 회차의 답안 시작
        answers = {}
        ans_iter = list(ANSWER_MARK_RE.finditer(answer_text))
        current_round = round_num  # 시작 회차
        for j, am in enumerate(ans_iter):
            mark_round = int(am.group(1)) if am.group(1) else None
            if mark_round is not None:
                current_round = mark_round
            n = int(am.group(2))
            ans_pts = int(am.group(3)) if am.group(3) else None
            # 다른 회차의 답안은 무시 (이 round_num의 답안만 수집)
            if current_round != round_num:
                continue
            body_start = am.end()
            body_end = ans_iter[j+1].start() if j+1 < len(ans_iter) else len(answer_text)
            body = enhance_answer(answer_text[body_start:body_end])
            answers[n] = {'body': body, 'points': ans_pts}

        # 답안이 매칭 안 되면 전체 답안 텍스트가 한 덩어리일 수도 있음
        # (예: 답안에 [문제#N] 마커 없이 평문) — 이 경우 전체를 round-level로 보존
        # 단, 답안 텍스트에 다른 회차 마커가 있으면 거기까지만 자른다
        round_level_answer = None
        if not answers and answer_text.strip():
            # 다른 회차 마커가 있으면 그 앞까지만
            other_round = re.search(r'(\d+)회\s*\[문제\s*#\d+\]', answer_text)
            cut = answer_text[:other_round.start()] if other_round else answer_text
            cleaned = enhance_answer(cut)
            if cleaned and not cleaned.startswith('> 11회 이전') and '답안집(11~36회)에 없음' not in cleaned:
                round_level_answer = cleaned

        for n in sorted(problems):
            qid = f'v3-{chapter_id}-r{round_num}-q{n}'
            entry = {
                'id': qid,
                'subject': SUBJECT,
                'chapter': chapter_id,
                'source': 'official',
                'round': round_num,
                'questionNum': n,
                'points': problems[n]['points'],
                'body': problems[n]['body'],
                'modelAnswer': answers[n]['body'] if n in answers else round_level_answer,
                'modelAnswerSource': 'matched' if n in answers else ('round' if round_level_answer else None),
                'sourceFile': source_file,
            }
            results.append(entry)
    return results


def main():
    if not SRC.exists():
        print(f'ERROR: source not found: {SRC}', file=sys.stderr)
        sys.exit(1)
    DEST.mkdir(parents=True, exist_ok=True)

    chapters_meta = []
    total_q = 0
    for fname in sorted(os.listdir(SRC)):
        m = CHAPTER_RE.match(fname)
        if not m: continue
        chapter_id = m.group(1)
        chapter_title = m.group(2).replace('_', ' ')
        path = SRC / fname
        md = path.read_text(encoding='utf-8')
        questions = parse_chapter(md, chapter_id, fname)
        if not questions:
            print(f'  [{chapter_id}] {chapter_title}: 기출 없음 — skip')
            continue
        with_answer = sum(1 for q in questions if q['modelAnswer'])
        matched = sum(1 for q in questions if q['modelAnswerSource'] == 'matched')
        rounds = sorted({q['round'] for q in questions})
        out = {
            'built_at': datetime.now(timezone.utc).isoformat(),
            'subject': SUBJECT,
            'chapter': chapter_id,
            'chapterTitle': chapter_title,
            'source': 'official',
            'count': len(questions),
            'withAnswer': with_answer,
            'matchedAnswer': matched,
            'rounds': rounds,
            'questions': questions,
        }
        out_path = DEST / f'{chapter_id}.json'
        out_path.write_text(json.dumps(out, ensure_ascii=False), encoding='utf-8')
        chapters_meta.append({
            'id': chapter_id,
            'title': chapter_title,
            'file': f'{chapter_id}.json',
            'count': len(questions),
            'withAnswer': with_answer,
            'matchedAnswer': matched,
            'rounds': rounds,
        })
        total_q += len(questions)
        print(f'  [{chapter_id}] {chapter_title}: {len(questions)}문항 (답안 매칭 {matched}/{len(questions)})')

    manifest = {
        'built_at': datetime.now(timezone.utc).isoformat(),
        'subject': SUBJECT,
        'total': total_q,
        'chapters': chapters_meta,
    }
    (DEST / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')
    print(f'\nmanifest: {len(chapters_meta)} chapters, {total_q} questions')
    print(f'output: {DEST}')


if __name__ == '__main__':
    main()
