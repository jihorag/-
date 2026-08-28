#!/usr/bin/env python3
"""논점 트랙의 순수 로직. 파일·네트워크에 손대지 않아 테스트가 된다.

build_topic_track.py 는 여기에 판단을 위임하고 I/O 와 Gemini 호출만 한다.
"""
import json
import re

# 관 하나의 논점 개수 상식 범위. 강제하지 않고 --check 가 보고만 한다.
MIN_POINTS = 3
MAX_POINTS = 40


def make_point_id(unit_code, leaf_idx, seq):
    """진도 저장의 키. 재생성해도 바뀌면 안 되므로 자리수를 고정한다."""
    return '%s-L%02d-p%02d' % (unit_code, leaf_idx, seq)


def order_spans(spans, lecture_meta):
    """강좌별로 묶어 (강좌, 강번호, start) 순으로 정렬한다.

    lecture_meta: {lecture_id: {'no': int, 'course': str}}
    메타에 없는 강의는 버리지 않고 맨 뒤로 보낸다 — 조용한 유실이 가장 나쁘다.
    """
    def key(s):
        m = lecture_meta.get(s['lecture_id'])
        if m is None:
            return (1, '', 0, s.get('start', 0.0))
        return (0, m.get('course') or '', m.get('no') or 0, s.get('start', 0.0))
    return sorted(spans, key=key)


def chunk_lectures(blocks, max_chars=45000):
    """전사 블록을 글자수 상한에 맞춰 나눈다. 버리지 않는다.

    블록 하나가 이미 상한을 넘으면 그대로 한 덩어리로 둔다 — 문장 중간을 자르면
    논점이 반토막 난다.
    """
    chunks, cur, size = [], [], 0
    for b in blocks:
        n = len(b.get('transcript', ''))
        if cur and size + n > max_chars:
            chunks.append(cur)
            cur, size = [], 0
        cur.append(b)
        size += n
    if cur:
        chunks.append(cur)
    return chunks


def parse_points(raw):
    """모델 응답에서 논점 배열을 꺼낸다. 실패하면 빈 리스트(호출부가 건너뛴다)."""
    if not raw:
        return []
    txt = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip())
    try:
        d = json.loads(txt)
    except ValueError:
        m = re.search(r'[\[{].*[\]}]', txt, flags=re.S)
        if not m:
            return []
        try:
            d = json.loads(m.group(0))
        except ValueError:
            return []
    if isinstance(d, dict):
        d = d.get('points') or []
    return [p for p in d if isinstance(p, dict) and p.get('title')]


def check_track(track, align_by_leaf, template_names):
    """트랙 하나를 검사해 사람이 읽는 문제 목록을 돌려준다."""
    issues = []
    unit = track.get('unit_code', '?')
    for leaf in track.get('leaves', []):
        lid = leaf.get('leaf_id')
        title = leaf.get('title') or lid or '?'
        pts = leaf.get('points') or []

        if len(pts) < MIN_POINTS:
            issues.append('%s / %s: 논점 수 %d개 (%d개 미만 — 추출 실패 의심)'
                          % (unit, title, len(pts), MIN_POINTS))
        elif len(pts) > MAX_POINTS:
            issues.append('%s / %s: 논점 수 %d개 (%d개 초과 — 잘게 쪼갠 것 의심)'
                          % (unit, title, len(pts), MAX_POINTS))

        # 앵커가 이 관의 실제 강의 구간 안에 있는가.
        # 밖이면 다른 관의 이야기가 새어 들어온 것이다.
        spans = align_by_leaf.get(lid) or [] if lid else []
        ranges = [(s.get('no'), s.get('start', 0.0), s.get('end', 0.0)) for s in spans]
        for p in pts:
            for a in p.get('src') or []:
                if not ranges:
                    continue
                ok = any(no == a.get('lec') and st <= a.get('t', -1) < en
                         for no, st, en in ranges)
                if not ok:
                    issues.append('%s / %s / %s: 앵커 %s강 %ss 가 이 관의 구간 밖'
                                  % (unit, title, p.get('id'), a.get('lec'), a.get('t')))

            viz = p.get('viz')
            if viz and viz.get('template') not in template_names:
                issues.append('%s / %s / %s: 미등록 템플릿 "%s"'
                              % (unit, title, p.get('id'), viz.get('template')))
    return issues


def diff_ids(old_track, new_track):
    """재생성 전후 논점 id 대조. 진도 마이그레이션이 필요한지 판단하는 근거."""
    def ids(t):
        return {p['id'] for lf in (t or {}).get('leaves', []) for p in lf.get('points', [])}
    o, n = ids(old_track), ids(new_track)
    return {'removed': sorted(o - n), 'added': sorted(n - o)}
