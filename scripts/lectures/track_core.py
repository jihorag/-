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

WHO_VALUES = ('ask', 'teach', 'gotcha', 'mate', 'quiz')
MIN_TURNS = 3
MAX_TURNS = 14
# 오답 반박이 이 문구로 시작하면 "그 오답 전용" 이 아니다. 규칙을 무의미하게 만드는 형태다.
GENERIC_REPLIES = ('틀렸', '오답', '아닙니다', '아니에요', '다시 생각')


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


# \frac→\x0c+rac, \bar→\x08+ar, \times→\t+imes 처럼 JSON 유효 이스케이프와 겹치는
# LaTeX 명령은 1차 파싱이 성공해 버려 복구 경로를 안 탄다. 결과를 다시 훑어 잡는다.
# \t·\r 은 본문에 정상적으로 쓰일 수 있으므로 "뒤에 영문자가 붙은 경우"만 깨짐으로 본다.
_LATEX_BREAK = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]|[\t\r](?=[a-zA-Z])')


def _extract_points(d):
    if isinstance(d, dict):
        d = d.get('points') or []
    return [p for p in d if isinstance(p, dict) and p.get('title')]


def _latex_broken(points):
    """points 의 title/gist/body/check.q/check.a 문자열에 LaTeX 깨짐 흔적이 있는가.

    json.dumps 로 재직렬화해서 검사하면 제어문자가 다시 \\t·\\f 로 이스케이프되어
    보이지 않는다 — 반드시 파싱된 문자열 값을 직접 훑는다.
    """
    for p in points:
        for key in ('title', 'gist', 'body'):
            v = p.get(key)
            if isinstance(v, str) and _LATEX_BREAK.search(v):
                return True
        chk = p.get('check')
        if isinstance(chk, dict):
            for key in ('q', 'a'):
                v = chk.get(key)
                if isinstance(v, str) and _LATEX_BREAK.search(v):
                    return True
    return False


def parses_as_json(raw):
    """raw 가 (배열이든 {"covered":false,"points":[]} 래퍼든) 문법적으로 유효한
    JSON인지만 본다. 강의가 이 관을 다루지 않아 모델이 정당하게 빈 배열을 낸
    경우도 유효한 JSON이므로, parse_points 가 돌려주는 빈 리스트만으로는
    "파싱 실패"와 "정당한 빈 응답"을 구분할 수 없다 — 이 구분에 쓴다."""
    if not raw:
        return False
    txt = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip())
    if _try_json_loads(txt) is not None:
        return True
    m = re.search(r'[\[{].*[\]}]', txt, flags=re.S)
    return bool(m and _try_json_loads(m.group(0)) is not None)


def parse_meta(raw):
    """모델 응답이 {"covered": bool, "reason": "...", "points": [...]} 래퍼면
    covered/reason 을 읽는다. 배열만 온 옛 형식이면 (None, '') — 판정 근거가
    없다는 뜻이지 커버 안 됐다는 뜻이 아니므로 호출부가 None 을 "판정 없음"으로
    다뤄야 한다."""
    if not raw:
        return None, ''
    txt = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip())
    d = _try_json_loads(txt)
    if d is None:
        m = re.search(r'[\[{].*[\]}]', txt, flags=re.S)
        d = _try_json_loads(m.group(0)) if m else None
    if isinstance(d, dict):
        return d.get('covered'), d.get('reason') or ''
    return None, ''


def parse_points(raw):
    """모델 응답에서 논점 배열을 꺼낸다. 실패하면 빈 리스트(호출부가 건너뛴다)."""
    if not raw:
        return []
    txt = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip())
    d = _try_json_loads(txt)
    candidate = txt
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
    points = _extract_points(d)
    # \frac/\bar/\times 같은 명령은 JSON 표준 이스케이프와 겹쳐 1차 파싱이
    # 예외 없이 성공해버린다. 성공한 결과라도 제어문자 흔적이 있으면 복구를
    # 재시도한다 — 복구본이 더 나쁘면(파싱 실패·논점 소실·여전히 깨짐) 원본을
    # 그대로 유지한다.
    if _latex_broken(points):
        recovered = _try_json_loads(_fix_bad_escapes(candidate))
        if recovered is not None:
            recovered_points = _extract_points(recovered)
            if recovered_points and not _latex_broken(recovered_points):
                return recovered_points
    return points


LOW_SEVERITY_PREFIX = '[시각추정]'


def check_track(track, align_by_leaf, template_names):
    """트랙 하나를 검사해 사람이 읽는 문제 목록을 돌려준다.

    반환값은 지금처럼 문자열 리스트다 (호출부인 build_topic_track.py 의
    do_check 가 이 형태를 그대로 출력·카운트한다).

    앵커(`src`) 검사는 성격이 다른 두 가지를 구분해서 담는다:
      - 강 번호 자체가 그 관의 spans 에 없음 → 진짜 신호. 접두사 없이,
        "이 관에 없는 강의를 가리킴" 문구로 보고한다. 다른 강의 내용이
        섞였거나 모델이 강 번호를 지어낸 경우다.
      - 강 번호는 맞고 시각만 그 강의 구간 밖(허용치 ANCHOR_TOL_SEC 초과)
        → 낮은 심각도. 메시지 앞에 LOW_SEVERITY_PREFIX(`[시각추정]`) 를 붙여
        구분한다. 전사는 그 관의 구간만 프롬프트에 넣으므로 내용 자체는
        맞고, 모델이 긴 블록 뒷부분의 시각을 눈대중으로 외삽했을 뿐이다.
    두 종류 모두 문자열 리스트에 섞여 담기지만 접두사로 구분되므로,
    호출부에서 `[시각추정]` 유무로 걸러 세면 된다.
    """
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

        # 청크 일부가 실패한 채 저장된 관 — build_topic_track.py 의 gen_leaf 가
        # 몇 청크를 성공했는지 chunks_ok/chunks_total 에 남긴다. 필드가 없는
        # 관(이 검사 이전에 저장된 기존 관)은 대조할 게 없으니 통과시킨다.
        c_ok, c_total = leaf.get('chunks_ok'), leaf.get('chunks_total')
        if c_ok is not None and c_total is not None and c_ok < c_total:
            issues.append('%s / %s: 청크 %d/%d 성공 — 강의 일부가 유실됐을 수 있음'
                          % (unit, title, c_ok, c_total))

        # 앵커가 이 관의 실제 강의 구간 안에 있는가.
        # 밖이면 다른 관의 이야기가 새어 들어온 것이다.
        spans = align_by_leaf.get(lid) or [] if lid else []
        ranges = [(s.get('no'), s.get('start', 0.0), s.get('end', 0.0)) for s in spans]
        for p in pts:
            for a in p.get('src') or []:
                if not ranges:
                    continue
                lec_known = any(no == a.get('lec') for no, st, en in ranges)
                if not lec_known:
                    issues.append('%s / %s / %s: 앵커 %s강 %ss — 이 관에 없는 강의를 가리킴'
                                  % (unit, title, p.get('id'), a.get('lec'), a.get('t')))
                    continue
                ok = any(no == a.get('lec')
                         and st - ANCHOR_TOL_SEC <= a.get('t', -1) < en + ANCHOR_TOL_SEC
                         for no, st, en in ranges)
                if not ok:
                    issues.append('%s %s / %s / %s: 앵커 %s강 %ss 가 이 관의 구간 밖(같은 강의, 시각 추정 오차 의심)'
                                  % (LOW_SEVERITY_PREFIX, unit, title, p.get('id'), a.get('lec'), a.get('t')))

            viz = p.get('viz')
            if viz and viz.get('template') not in template_names:
                issues.append('%s / %s / %s: 미등록 템플릿 "%s"'
                              % (unit, title, p.get('id'), viz.get('template')))

        # 대화(turns) 검사 — quiz 유무, 정답/오답 구성, 오답별 전용 반박, who 값, 턴 수.
        # turns 가 없는 논점은 turns 프롬프트 이전에 저장된 옛 논점이다 — 결함이
        # 아니라 "미갱신"으로 구분해 보고하고 나머지 turns 검사는 건너뛴다.
        for p in pts:
            turns = p.get('turns')
            if not turns:
                issues.append('%s / %s / %s: 미갱신 (turns 없음 — body 폴백)'
                              % (unit, title, p.get('id')))
                continue

            if not (MIN_TURNS <= len(turns) <= MAX_TURNS):
                issues.append('%s / %s / %s: 턴 %d개 (%d~%d 범위 밖)'
                              % (unit, title, p.get('id'), len(turns), MIN_TURNS, MAX_TURNS))

            quizzes = [t for t in turns if t.get('who') == 'quiz']
            if not quizzes:
                issues.append('%s / %s / %s: quiz 턴 없음 — 그냥 넘겨 통과할 수 있다'
                              % (unit, title, p.get('id')))

            for t in turns:
                if t.get('who') not in WHO_VALUES:
                    issues.append('%s / %s / %s: 알 수 없는 who "%s"'
                                  % (unit, title, p.get('id'), t.get('who')))

            for qz in quizzes:
                ch = qz.get('choices') or []
                oks = [c for c in ch if c.get('ok')]
                if len(oks) != 1:
                    issues.append('%s / %s / %s: 정답 선택지가 %d개 (1개여야 함)'
                                  % (unit, title, p.get('id'), len(oks)))
                if len(ch) - len(oks) < 2:
                    issues.append('%s / %s / %s: 오답 선택지가 %d개 (2개 이상이어야 함)'
                                  % (unit, title, p.get('id'), len(ch) - len(oks)))
                for c in ch:
                    if c.get('ok'):
                        continue
                    r = (c.get('reply') or '').strip()
                    if not r or r.startswith(GENERIC_REPLIES):
                        issues.append('%s / %s / %s: 오답 "%s" 에 전용 반박이 없다'
                                      % (unit, title, p.get('id'), (c.get('text') or '')[:14]))
    return issues


def diff_ids(old_track, new_track):
    """재생성 전후 논점 id 대조. 진도 마이그레이션이 필요한지 판단하는 근거."""
    def ids(t):
        return {p['id'] for lf in (t or {}).get('leaves', []) for p in lf.get('points', [])}
    o, n = ids(old_track), ids(new_track)
    return {'removed': sorted(o - n), 'added': sorted(n - o)}
