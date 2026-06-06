#!/usr/bin/env python3
"""2차 논술 이론·법규 essay 데이터 생성 (실제 기출 전문 추출 + 논점 폴백).
소스: 'Claude KAPA CHATING copy' 의 _최종산출물 단원 마크다운.
 · 이론: "기출문제 N. … (회차.점수)" 블록(본문+물음) 추출 → 실제 기출
 · 법규: "… (N점) [N회, 문N]" 마커가 붙은 실제 기출 문항 추출
 · 마커가 없는 단원(주로 행정법·이론 일부)은 단원 논점명 프롬프트로 폴백
EssayMode가 읽는 manifest.json + chapter JSON(실무와 동일 스키마) 으로 변환.
모범답안은 비워둠(자기채점 키워드 + AI 채점). 전수 예시답안은 단계적 확장.
"""
import json, re, datetime, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'Claude KAPA CHATING copy'
OUT_BASE = ROOT / 'viewer/public/data/essay'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

THEORY_DIR = SRC / '2차 - 감정평가이론_학습자료/_최종산출물_이론_v2'
LAW_DIR = SRC / '2차 - 감정평가법규_학습자료/_최종산출물_법규'

THEORY_CH = {
    1: '감정평가 기초·분류·절차', 2: '부동산 가치이론·가격형성', 3: '가격제원칙·시장론·시장분석',
    4: '3방식 개관·거래사례비교법', 5: '원가법', 6: '수익환원법', 7: '기타방식·임료',
    8: '기업가치·물건별 평가', 9: '부동산투자·금융론', 10: '부동산정책론·기타논점',
}
LAW_CH = {
    1: '행정법 개관·일반원칙·행정법관계', 2: '행정입법·행정행위', 3: '행정계획·인허가의제·공법상계약',
    4: '행정절차·실효성확보수단', 5: '행정쟁송(심판·취소소송)', 6: '행정상 손해전보',
    7: '공용수용(사업인정·재결)', 8: '손실보상(보상기준·환매·생활보상)', 9: '부동산 가격공시법',
    10: '감정평가법·도정법',
}


def list_units(d):
    """macOS NFD 한글 파일명 대응 — '단원_NN_*.md' 수집."""
    out = []
    for f in d.iterdir():
        name = unicodedata.normalize('NFC', f.name)
        m = re.match(r'단원_(\d+)_.*\.md$', name)
        if m:
            out.append((int(m.group(1)), f))
    return sorted(out)


def keypoints_from(title):
    toks = re.split(r'[·,()\s]+', title)
    return [t for t in toks if len(t) >= 2][:6]


def parse_points_round(s):
    """'(3회.40점)' '(13회.40점)' '(20점) [15회, 문3]' 등에서 점수·회차 추출."""
    points = None
    pm = re.findall(r'(\d+)\s*점', s)
    if pm:
        points = max(int(x) for x in pm)
    rm = re.search(r'(\d{1,2})\s*회', s)
    rnd = int(rm.group(1)) if rm else None
    return points, rnd


def extract_theory(text):
    """'기출문제 N. …' 블록(본문 + (n) 물음 라인) 추출."""
    lines = text.splitlines()
    qs, i = [], 0
    while i < len(lines):
        m = re.match(r'^\s*기출문제\s*\d+[.\s]*(.+)$', lines[i])
        if m and ('하' in m.group(1) or '점' in m.group(1) or '?' in m.group(1)):
            stem = m.group(1).strip()
            body = [stem]
            j = i + 1
            # 하위 물음 (1)…(n) 또는 1) 2) 라인만 이어붙임
            while j < len(lines):
                ln = lines[j].strip()
                if re.match(r'^[\(（]?\d+[\)）]\s*\S', ln) and len(ln) < 200:
                    body.append(ln); j += 1
                else:
                    break
            full = '\n'.join(body)
            pts, rnd = parse_points_round(full)
            if len(full) >= 8 and len(full) <= 1400:
                qs.append({'body': full, 'points': pts or 30, 'round': rnd})
            i = j
        else:
            i += 1
    return qs


def extract_law(text):
    """'… (N점) [N회, 문N]' 마커가 붙은 실제 기출 문항 라인 추출."""
    qs, seen = [], set()
    for ln in text.splitlines():
        ln = ln.strip()
        if not re.search(r'\[\s*\d{1,2}\s*회', ln):
            continue
        # 마커 제거한 본문
        body = re.sub(r'\[\s*\d{1,2}\s*회[^\]]*\]', '', ln).strip()
        body = re.sub(r'\s+', ' ', body)
        if len(body) < 8 or len(body) > 600:
            continue
        key = body[:30]
        if key in seen:
            continue
        seen.add(key)
        pts, rnd = parse_points_round(ln)
        qs.append({'body': body, 'points': pts or 25, 'round': rnd})
    return qs


def fallback_logum(text):
    """마커 없는 단원: 핵심요약서 논점 아웃라인의 'NN 논점명' → 프롬프트."""
    labels = re.findall(r'(?m)^[ \t]*(\d{2})[ \t]+([가-힣][가-힣A-Za-z0-9·()· \t]{3,28})[ \t]*$', text)
    GENERIC = {'근거', '특징', '요건', '의의', '내용', '효과', '유형', '절차', '배경', '취지', '개념',
               '개설', '개요', '문제점', '한계', '비교', '구별', '종류', '성질', '기능', '인정여부',
               '판단기준', '권리구제', '법적성질', '서설', '결어'}
    seen, items = set(), []
    for _n, name in labels:
        name = re.sub(r'\s+', ' ', name).strip()
        if name in seen or name in GENERIC:
            continue
        if len(re.findall(r'[가-힣]', name)) < 5 and ' ' not in name:
            continue
        if any(b in name for b in ['스터디파이터', '문제모음', '기출모음', '강의', '제1장', '제2장', 'Part', 'PART', 'p.']):
            continue
        seen.add(name)
        items.append({'body': f"「{name}」에 관하여 설명하시오.", 'points': 25, 'round': None})
    return items[:14]


def build(src_dir, extractor):
    by_ch = {}
    for ch, f in list_units(src_dir):
        text = f.read_text(encoding='utf-8')
        items = extractor(text)
        if len(items) < 3:  # 실제 기출 부족 → 논점 폴백
            fb = fallback_logum(text)
            # 합치되 중복 최소화
            existing = {it['body'][:20] for it in items}
            items = items + [x for x in fb if x['body'][:20] not in existing]
        by_ch[ch] = items
    return by_ch


def write_subject(out_dir, subject, ch_titles, by_ch):
    out_dir.mkdir(parents=True, exist_ok=True)
    chapters_meta, total, real_total = [], 0, 0
    for ch in sorted(ch_titles):
        items = by_ch.get(ch, [])
        questions, rounds = [], set()
        for i, it in enumerate(items, 1):
            is_real = not it['body'].startswith('「')
            if is_real:
                real_total += 1
            if it.get('round'):
                rounds.add(it['round'])
            questions.append({
                'id': f"tl-{out_dir.name}-c{ch}-q{i}", 'subject': subject, 'chapter': str(ch),
                'source': 'official' if is_real else 'past-topic',
                'round': it.get('round'), 'questionNum': i, 'points': it.get('points', 25),
                'body': it['body'], 'modelAnswer': '', 'modelAnswerSource': '',
                'keyPoints': keypoints_from(it['body'][:40]),
                'difficulty': 4 if it.get('points', 25) >= 40 else 3,
                'answerFormat': '', 'subchapter': f"{ch}-1",
            })
        total += len(questions)
        (out_dir / f"{ch}.json").write_text(json.dumps({
            'built_at': NOW, 'subject': subject, 'chapter': str(ch), 'chapterTitle': ch_titles[ch],
            'source': 'mixed', 'count': len(questions), 'withAnswer': 0, 'matchedAnswer': 0,
            'rounds': sorted(rounds), 'questions': questions,
        }, ensure_ascii=False, indent=1), encoding='utf-8')
        chapters_meta.append({
            'id': str(ch), 'title': ch_titles[ch], 'file': f"{ch}.json",
            'count': len(questions), 'withAnswer': 0, 'matchedAnswer': 0,
            'rounds': sorted(rounds), 'generatedCount': 0,
            'subchapters': [{'id': f"{ch}-1", 'title': ch_titles[ch], 'keywords': keypoints_from(ch_titles[ch])}],
        })
    (out_dir / 'manifest.json').write_text(json.dumps({
        'built_at': NOW, 'subject': subject, 'total': total, 'classified': total, 'chapters': chapters_meta,
    }, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"  {subject}: 총 {total}문항 (실제 기출 {real_total} / 논점 {total - real_total}) → {out_dir}")


def main():
    print("이론·법규 2차 논술 데이터 생성 (실제 기출 추출)")
    write_subject(OUT_BASE / 'theory', '감정평가이론', THEORY_CH, build(THEORY_DIR, extract_theory))
    write_subject(OUT_BASE / 'law', '감정평가 및 보상법규', LAW_CH, build(LAW_DIR, extract_law))
    print("완료")


if __name__ == '__main__':
    main()
