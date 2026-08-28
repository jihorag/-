#!/usr/bin/env python3
"""논점 트랙의 순수 로직. 파일·네트워크에 손대지 않아 테스트가 된다.

build_topic_track.py 는 여기에 판단을 위임하고 I/O 와 Gemini 호출만 한다.
"""
import json
import re

# 관 하나의 논점 개수 상식 범위. 강제하지 않고 --check 가 보고만 한다.
MIN_POINTS = 3
MAX_POINTS = 40

# 앵커의 초는 프롬프트에 들어간 [36강 6:06] 표기에서 읽히므로 구간 시작보다
# 최대 1초 이르게 찍힌다. 경계 오차로 거짓 경고가 관마다 뜨면 진짜 누출 신호가 묻힌다.
ANCHOR_TOL_SEC = 5


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


def _try_json_loads(s):
    """json.loads 를 시도하고 실패하면 None. 예외를 상위로 흘리지 않기 위한 얇은 래퍼."""
    try:
        return json.loads(s)
    except ValueError:
        return None


def _fix_bad_escapes(s):
    """JSON 문자열 안의 잘못된 백슬래시 이스케이프를 복구한다.

    Gemini 가 수식을 JSON으로 감싸면서 LaTeX 명령을 백슬래시 하나로 그대로 써
    버린다 (`$\\sum MB = MC$`, `$\\frac{1}{1-c}$`, `$\\times$`). JSON 명세상
    `\\s`·`\\u`(4자리 hex 아님)·`\\x` 등은 유효한 이스케이프가 아니라 그 지점에서
    전체 파싱이 깨진다. 원본 json.loads 가 이미 실패했을 때만 이 함수를 거친다
    — 정상 응답은 절대 이 경로를 타지 않는다.

    규칙: 백슬래시를 만나면
      - 다음 문자가 JSON 표준 이스케이프(`"` `\\` `/` `b` `f` `n` `r` `t`) 인데
        그 뒤가 영문자가 아니면 → 진짜 이스케이프로 보고 그대로 둔다.
        (`\\n\\n`, `\\"` 는 유지. `\\frac`/`\\times`/`\\beta` 처럼 `f`/`t`/`b`/`n`/`r`
        다음에 알파벳이 이어지면 LaTeX 명령으로 보고 두 개로 늘린다 — 그렇지
        않으면 `\\frac` 이 폼피드 문자 + `rac` 으로 깨져 파싱은 성공해도 내용이
        망가진다.)
      - 다음 문자가 `u` 이고 그 뒤 4자가 16진수면 → 유니코드 이스케이프이므로
        그대로 둔다.
      - 그 외 → LaTeX 명령으로 보고 백슬래시를 두 개로 늘린다.

    한계: 순수 문자열 스캔이라 실제 문자열 리터럴 경계(따옴표 안팎)를 구분하지
    않는다. JSON 구조 문자 자체에는 백슬래시가 나오지 않으므로 실무상 문제는
    없지만, 100% 정확한 파서는 아니다. 판정이 틀려도 이 함수는 원본 파싱이
    이미 실패했을 때만 쓰이고, 복구본도 실패하면 그대로 빈 리스트로 떨어진다.
    """
    out = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c != '\\' or i + 1 >= n:
            out.append(c)
            i += 1
            continue
        nxt = s[i + 1]
        if nxt == 'u' and re.match(r'^[0-9a-fA-F]{4}$', s[i + 2:i + 6]):
            out.append(s[i:i + 6])
            i += 6
        elif nxt in '"\\/':
            out.append(s[i:i + 2])
            i += 2
        elif nxt in 'bfnrt':
            after = s[i + 2] if i + 2 < n else ''
            # LaTeX 명령은 항상 ASCII 알파벳이다. 한글은 str.isalpha() 가 True를
            # 돌려주므로 ASCII로 한정하지 않으면 "...\n둘째 줄" 같은 정상적인
            # 줄바꿈 뒤 한글 문장까지 LaTeX로 오판해 이스케이프를 깨뜨린다.
            if after.isalpha() and after.isascii():
                out.append('\\\\' + nxt)
            else:
                out.append(s[i:i + 2])
            i += 2
        else:
            out.append('\\\\' + nxt)
            i += 2
    return ''.join(out)


def parse_points(raw):
    """모델 응답에서 논점 배열을 꺼낸다. 실패하면 빈 리스트(호출부가 건너뛴다)."""
    if not raw:
        return []
    txt = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip())
    d = _try_json_loads(txt)
    if d is None:
        m = re.search(r'[\[{].*[\]}]', txt, flags=re.S)
        if not m:
            return []
        candidate = m.group(0)
        d = _try_json_loads(candidate)
        if d is None:
            # 코드펜스 제거·괄호 추출까지 다 실패한 경우에만 LaTeX 이스케이프
            # 복구를 시도한다 (정상 응답의 동작은 절대 바꾸지 않는다).
            d = _try_json_loads(_fix_bad_escapes(candidate))
        if d is None:
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
                ok = any(no == a.get('lec')
                         and st - ANCHOR_TOL_SEC <= a.get('t', -1) < en + ANCHOR_TOL_SEC
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
