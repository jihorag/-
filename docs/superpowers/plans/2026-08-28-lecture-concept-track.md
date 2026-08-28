# 논점 트랙 (개념 완성) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 강의 전사에서 관(關)마다 "논점 트랙"을 사전 생성하고, 신설 「개념 완성」 화면이 그 트랙을 대화로 소진해 인강을 보지 않고도 강의 내용을 빠짐없이 익히게 한다.

**Architecture:** 배치 파이썬 스크립트(`build_topic_track.py`)가 `align.json`의 `by_leaf` 구간 + 전사 + 교재 슬라이스 + 판서 키프레임을 Gemini에 넣어 관별 논점 JSON을 만들어 저장소에 커밋한다. 앱은 그 JSON을 `/data/study/{과목}/lectures/track/{unit}.{phase}.json`에서 직접 fetch해 논점을 하나씩 보여주고, 진도를 localStorage에 쌓아 `mastery.phases.basic.coverage`를 실측값으로 쓴다. 시각자료는 기존 viz 템플릿 18개를 그대로 두고 `VizRouter` 한 곳에 단계 재생기를 얹는다.

**Tech Stack:** Python 3.9(시스템 `python3`, stdlib만) · Gemini `gemini-3-flash-preview` · React 19 + Vite 8 · `node --test` (Node 22) · `python3 -m unittest`

**Spec:** `docs/superpowers/specs/2026-08-28-lecture-concept-track-design.md`

## Global Constraints

- **파일럿 과목은 `economics`, phase는 `basic`.** 다른 과목·회독은 이 계획 범위 밖이다.
- **`src` 앵커(`{lec, t}`)는 화면에 절대 노출하지 않는다.** 내부 재생성·검증 전용이다.
- **`body`는 강의를 옮겨 적지 않는다.** `generate_notes.py`의 기존 문체 규칙을 상속한다 — "강사·강의·선생님" 단어 금지, 큰따옴표로 말 옮기기 금지, 교재처럼 단정 서술.
- **숫자를 지어내지 않는다.** `generate_notes.py`의 `SUBJECT_RULES`를 그대로 재사용한다.
- **경로는 `scripts/lectures/_paths.py`만 쓴다.** 드라이브 이름을 코드에 박지 않는다.
- **경로 관련 코드를 고친 뒤에는 반드시 `rm -rf scripts/lectures/__pycache__`.** 옛 경로가 컴파일 캐시에 남아 전 관이 조용히 건너뛰어진 사고가 있었다(인수인계서 5-1).
- **외장 파일명은 NFD다.** 한글 이름을 정규식으로 다룰 때 `unicodedata.normalize('NFC', name)`. `._*` AppleDouble 파일은 항상 제외한다.
- **Python은 3.9 호환으로 쓴다** (시스템 `python3`가 3.9). `match` 문, `X | Y` 타입 표기 금지.
- **뷰어 테스트는 순수 `.js`만** — JSX를 import하는 테스트는 만들지 않는다. 그래서 로직은 `.js`로, 화면은 `.jsx`로 가른다.
- **트랙 JSON은 `viewer/public/data/` 아래에 직접 쓴다.** 여기가 곧 서빙 경로라 `sync-data`가 필요 없다.
- 커밋 메시지는 저장소 관례를 따른다: `feat(강의): …`, `fix(강의): …`.

---

## File Structure

| 파일 | 책임 |
|---|---|
| **Create** `scripts/lectures/track_core.py` | 순수 함수만 — 논점 id 생성, 강좌별 span 정렬, 전사 청크 분할, 응답 파싱, 검증. API·파일 I/O 없음. 그래서 테스트가 된다. |
| **Create** `scripts/lectures/test_track_core.py` | 위의 unittest. |
| **Create** `scripts/lectures/build_topic_track.py` | CLI. `_paths`·`build_note_bundle.build`·Gemini 호출·파일 쓰기. 로직은 `track_core`에 위임. |
| **Create** `viewer/src/viz/steps.js` | 순수 — `steps[i]`를 base params에 병합. DOM 없음. |
| **Create** `viewer/src/viz/steps.test.js` | `node --test`. |
| **Create** `viewer/src/viz/StepPlayer.jsx` | 단계 재생 UI(◀ ▶ 재생 · 라벨 · 크로스페이드). |
| **Modify** `viewer/src/viz/VizRouter.jsx` | `params.steps` 있으면 `StepPlayer`로 위임. |
| **Create** `viewer/src/trackProgress.js` | 순수+localStorage — 논점 상태 저장, 관 coverage 계산. |
| **Create** `viewer/src/trackProgress.test.js` | `node --test`. |
| **Create** `viewer/src/ConceptTrack.jsx` | 「개념 완성」 화면. |
| **Modify** `viewer/src/App.jsx` | `concept` 뷰 라우팅 + `SUB_TABS.tutor` 추가 + `TAB_HOME_VIEW.tutor` 변경. |
| **Modify** `viewer/src/AILearning.jsx` | `study` 모드 버튼에 "개념 완성으로" 안내 추가. coverage 쓰기 경로 분기. |

`AILearning.jsx`는 이미 4,080줄이다. 새 화면을 여기 넣지 않고 `ConceptTrack.jsx`로 가른다.

---

## Task 1: `track_core.py` — 순수 로직

**Files:**
- Create: `scripts/lectures/track_core.py`
- Test: `scripts/lectures/test_track_core.py`

**Interfaces:**
- Consumes: 없음 (stdlib만)
- Produces:
  - `make_point_id(unit_code, leaf_idx, seq) -> str`
  - `order_spans(spans, lecture_meta) -> list` — 강좌별로 묶어 (강좌, 강번호, start) 순 정렬
  - `chunk_lectures(lecture_blocks, max_chars=45000) -> list[list]`
  - `parse_points(raw_text) -> list[dict]` — 모델 응답(JSON) 파싱, 코드펜스 제거
  - `check_track(track, align_by_leaf, template_names) -> list[str]` — 문제 문자열 목록

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`scripts/lectures/test_track_core.py`:

```python
import unittest

from track_core import (make_point_id, order_spans, chunk_lectures,
                        parse_points, check_track)


class TestPointId(unittest.TestCase):
    def test_zero_padded_and_stable(self):
        self.assertEqual(make_point_id('M01', 0, 1), 'M01-L00-p01')
        self.assertEqual(make_point_id('M01', 12, 7), 'M01-L12-p07')


class TestOrderSpans(unittest.TestCase):
    """강좌가 여럿이면 강좌별로 묶어 정렬한다.

    회계(재무 63강 + 원가 21강)·법규(도승하 36강 + 김희상 39강)는 둘 다 1강부터
    시작한다. 강번호로만 정렬하면 두 강좌가 지그재그로 섞이고, 트랙은 순서 자체가
    산출물이라 여기서 틀리면 전부 틀린다.
    """
    def test_groups_by_course_then_number(self):
        meta = {
            'a-1': {'no': 1, 'course': 'A'},
            'a-2': {'no': 2, 'course': 'A'},
            'b-1': {'no': 1, 'course': 'B'},
        }
        spans = [
            {'lecture_id': 'b-1', 'start': 10.0},
            {'lecture_id': 'a-2', 'start': 5.0},
            {'lecture_id': 'a-1', 'start': 30.0},
            {'lecture_id': 'a-1', 'start': 10.0},
        ]
        got = [(s['lecture_id'], s['start']) for s in order_spans(spans, meta)]
        self.assertEqual(got, [('a-1', 10.0), ('a-1', 30.0), ('a-2', 5.0), ('b-1', 10.0)])

    def test_unknown_lecture_goes_last_not_dropped(self):
        meta = {'a-1': {'no': 1, 'course': 'A'}}
        spans = [{'lecture_id': 'ghost', 'start': 0.0}, {'lecture_id': 'a-1', 'start': 0.0}]
        got = [s['lecture_id'] for s in order_spans(spans, meta)]
        self.assertEqual(got, ['a-1', 'ghost'])


class TestChunkLectures(unittest.TestCase):
    """긴 관은 잘라내지 않고 나눠 호출한다.

    generate_notes.py 는 MAX_TRANSCRIPT 를 넘으면 앞뒤만 남기고 가운데를 버린다.
    트랙에서 그러면 중간 논점이 통째로 사라지고, 그게 정확히 이 프로젝트가
    없애려는 손실이다.
    """
    def test_splits_without_dropping(self):
        blocks = [{'no': i, 'transcript': 'x' * 20000} for i in range(1, 6)]
        chunks = chunk_lectures(blocks, max_chars=45000)
        self.assertEqual(sum(len(c) for c in chunks), 5)
        self.assertTrue(all(c for c in chunks))

    def test_single_oversize_block_kept_whole(self):
        blocks = [{'no': 1, 'transcript': 'x' * 90000}]
        chunks = chunk_lectures(blocks, max_chars=45000)
        self.assertEqual(chunks, [blocks])


class TestParsePoints(unittest.TestCase):
    def test_strips_code_fence(self):
        raw = '```json\n[{"title":"t","gist":"g","body":"b"}]\n```'
        self.assertEqual(parse_points(raw)[0]['title'], 't')

    def test_object_wrapper_accepted(self):
        raw = '{"points": [{"title":"t","gist":"g","body":"b"}]}'
        self.assertEqual(len(parse_points(raw)), 1)

    def test_garbage_returns_empty(self):
        self.assertEqual(parse_points('설명입니다. JSON 아님'), [])


class TestCheckTrack(unittest.TestCase):
    def _track(self, **over):
        pt = {'seq': 1, 'id': 'M01-L00-p01', 'title': 't', 'gist': 'g', 'body': 'b',
              'viz': None, 'check': {'q': 'q', 'a': 'a'},
              'src': [{'lec': 2, 't': 100}]}
        pt.update(over.pop('point', {}))
        return {'unit_code': 'M01', 'phase': 'basic',
                'leaves': [{'leaf_id': 'L', 'title': 'T', 'points': [pt]}],
                'orphans': []}

    def test_clean_track_has_no_issues(self):
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        self.assertEqual(check_track(self._track(), align, {'supply-demand'}), [])

    def test_anchor_outside_span_reported(self):
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        issues = check_track(self._track(point={'src': [{'lec': 2, 't': 9999}]}),
                             align, {'supply-demand'})
        self.assertTrue(any('앵커' in i for i in issues))

    def test_unknown_template_reported(self):
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        issues = check_track(self._track(point={'viz': {'template': 'nope', 'params': {}}}),
                             align, {'supply-demand'})
        self.assertTrue(any('nope' in i for i in issues))

    def test_point_count_out_of_range_reported(self):
        align = {'L': [{'no': 2, 'start': 60.0, 'end': 180.0}]}
        t = self._track()
        t['leaves'][0]['points'] = t['leaves'][0]['points'] * 41
        self.assertTrue(any('논점 수' in i for i in check_track(t, align, set())))


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: 테스트가 실패하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/scripts/lectures" && python3 -m unittest test_track_core -v
```

Expected: `ModuleNotFoundError: No module named 'track_core'`

- [ ] **Step 3: `track_core.py` 구현**

```python
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
```

- [ ] **Step 4: 테스트가 통과하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/scripts/lectures" && python3 -m unittest test_track_core -v
```

Expected: 11 tests, all OK

- [ ] **Step 5: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add scripts/lectures/track_core.py scripts/lectures/test_track_core.py
git commit -m "feat(강의): 논점 트랙 순수 로직 + 테스트

강좌별 span 정렬(지그재그 방지)·전사 무손실 분할·응답 파싱·트랙 검증.
파일·네트워크에 손대지 않아 API 없이 테스트된다."
```

---

## Task 2: `build_topic_track.py` — 생성 CLI (2관 파일럿)

**Files:**
- Create: `scripts/lectures/build_topic_track.py`
- Read-only 참조: `scripts/lectures/generate_notes.py` (STYLE·SUBJECT_RULES·call_gemini·load_leaf_sections 재사용), `scripts/lectures/build_note_bundle.py` (`build`)

**Interfaces:**
- Consumes: `track_core.{make_point_id, order_spans, chunk_lectures, parse_points}` (Task 1)
- Produces: `viewer/public/data/study/economics/lectures/track/{unit}.basic.json` — §4-2 스키마

- [ ] **Step 1: 스크립트를 쓴다**

`scripts/lectures/build_topic_track.py`:

```python
#!/usr/bin/env python3
"""관(leaf)별 논점 트랙 생성 — 전사 + 교재 + 판서 → 강의 진행 순서의 논점 목록.

`generate_notes.py` 가 "교재에 없는 것만" 뽑는 보충이라면, 이쪽은 **강의가 실제로
다룬 것을 빠짐없이** 순서대로 세운다. 개념 완성 화면이 이 목록을 하나씩 소진하고,
다 비우면 그 관의 강의를 끝까지 들은 것과 같다.

출력: viewer/public/data/study/{과목}/lectures/track/{unit}.{phase}.json

사용:
  python3 scripts/lectures/build_topic_track.py economics --phase basic --limit 2
  python3 scripts/lectures/build_topic_track.py economics --phase basic
  python3 scripts/lectures/build_topic_track.py economics --phase basic --check
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import REPO, STUDY, WORK  # noqa: E402
from build_note_bundle import build, DEFAULT_PDF  # noqa: E402
from map_notes_to_leaves import extract_note_pages  # noqa: E402
from generate_notes import (SUBJECT_RULES, call_gemini, load_leaf_sections,  # noqa: E402
                            MODEL, MAX_FRAMES)
from track_core import (make_point_id, order_spans, chunk_lectures,  # noqa: E402
                        parse_points, check_track, diff_ids)

MAX_CHUNK_CHARS = 45000   # 한 번의 호출에 넣을 전사 글자수 상한

STYLE = """당신은 감정평가사 1차 수험 교재를 쓰는 사람입니다.
강의(음성 전사 + 판서 사진)를 읽고, 그 강의가 **실제로 다룬 논점**을
**강의가 진행된 순서 그대로** 나열합니다.

[가장 중요 — 빠뜨리지 말 것]
- 이 목록을 다 읽은 사람은 강의를 듣지 않아도 됩니다. 강의에서 다룬 내용이
  목록에 없으면 그 사람은 그걸 영영 모릅니다.
- 반대로 강의에 없던 내용을 지어내 채우지 마세요. 교재에서 끌어와 부풀리는 것도 금지입니다.
- 잡담·다음 강의 예고·수강 안내·시스템 공지는 논점이 아닙니다. 버리세요.
- 지금 쓰는 것은 **이 관 하나**입니다. 전사에 다른 관 이야기가 섞여 있어도 걸러내세요.

[문체 — 교재와 구분이 안 되게]
- **"강사", "강의", "선생님" 이라는 단어를 아예 쓰지 마세요.** "강사가 제시한",
  "강의에서 강조한" 같은 표현도 금지입니다. 출처를 밝히지 말고 교재처럼 단정 서술하세요.
- 큰따옴표로 말을 옮기지 마세요. 내용만 일반 서술로 바꾸세요.
- 전사 오류·음성 인식 같은 제작 뒷얘기는 절대 쓰지 마세요.
- 문장은 '~이다/~한다' 체.

[각 논점에 담을 것]
- title: 논점 이름. 명사구가 아니라 **무엇을 알게 되는지**가 드러나게. 25자 이내.
- gist: 한 줄 요약. 목록에서 이것만 보고도 무슨 얘긴지 알게. 60자 이내.
- body: 본문 400~800자. 설명의 순서와 이유, 비유·예시, 무엇을 외우고 무엇은 넘길지,
  판서에만 있는 수식·도식까지. 수식은 KaTeX 인라인 `$...$`.
  둘 이상을 견주는 대목은 마크다운 표로 쓰세요(비교축 3개 이상).
- check: 이 논점을 이해했는지 확인하는 질문 하나와, 정답 + 왜 그런지.
- viz: 그림이 이해를 돕는 논점에만. 아래 [VIZ_CATALOG] 의 템플릿 중에서 고르세요.
  카탈로그에 없으면 viz 를 null 로 두세요. 억지로 붙이지 마세요.
- src: 이 논점의 근거가 된 대목. [12강 23:10] 표기에서 읽어 {"lec":12,"t":1390} 형태로.
  t 는 초 단위 정수입니다.

[출력 형식 — JSON 배열만]
설명·인사말·코드펜스 없이 JSON 배열 하나만 출력하세요.
[
  {"title":"…","gist":"…","body":"…",
   "viz":{"template":"supply-demand","params":{…},"steps":[{"label":"…", …}]},
   "check":{"q":"…","a":"…"},
   "src":[{"lec":12,"t":1390}]}
]
viz 의 steps 는 단계적으로 변하는 그림에만 씁니다(예: 곡선이 이동해 균형이 옮겨가는 과정).
각 step 은 label 과, 그 단계에서 달라지는 파라미터만 담습니다."""


def load_viz_catalog():
    """vizRegistry 가 앱에 주입하는 카탈로그와 같은 내용을 파이썬에서 읽는다.

    레지스트리는 JS 라 여기서 실행할 수 없다. exampleParams 를 그대로 뽑아 쓰는 대신,
    템플릿 이름과 helpText 만 정규식으로 긁어 온다. 파라미터 정확도는 --check 와
    앱의 VizRouter 검증이 잡는다.
    """
    src = (REPO / 'viewer/src/viz/vizRegistry.js').read_text(encoding='utf-8')
    names = re.findall(r"from './templates/(\w+)'", src)
    lines = []
    for n in names:
        f = REPO / 'viewer/src/viz/templates' / (n + '.jsx')
        if not f.exists():
            continue
        t = f.read_text(encoding='utf-8')
        nm = re.search(r"name:\s*'([^']+)'", t)
        ht = re.search(r"helpText:\s*'([^']*)'", t)
        ex = re.search(r'exampleParams:\s*(\{.*?\n  \},)', t, flags=re.S)
        if not nm:
            continue
        lines.append('### %s — %s\n```json\n%s\n```'
                     % (nm.group(1), ht.group(1) if ht else '',
                        (ex.group(1).rstrip(',') if ex else '{}')))
    return ('## [VIZ_CATALOG] 쓸 수 있는 시각자료 템플릿\n\n'
            '아래에 없는 도식은 만들지 말고 viz 를 null 로 두세요.\n\n'
            + '\n\n'.join(lines))


def template_names():
    src = (REPO / 'viewer/src/viz/vizRegistry.js').read_text(encoding='utf-8')
    out = set()
    for n in re.findall(r"from './templates/(\w+)'", src):
        f = REPO / 'viewer/src/viz/templates' / (n + '.jsx')
        if f.exists():
            m = re.search(r"name:\s*'([^']+)'", f.read_text(encoding='utf-8'))
            if m:
                out.add(m.group(1))
    return out


def lecture_meta(align):
    return {lid: {'no': v.get('no'), 'course': v.get('course') or v.get('phase') or ''}
            for lid, v in align.get('by_lecture', {}).items()}


def gen_leaf(key, sec, bundle, catalog, subject):
    """관 하나의 논점 목록을 만든다. 긴 관은 나눠 호출해 이어 붙인다."""
    points = []
    chunks = chunk_lectures(bundle['lectures'], MAX_CHUNK_CHARS)
    for i, blocks in enumerate(chunks, 1):
        transcript = '\n\n'.join('[%s강 %s]\n%s' % (b['no'], b['ts'], b['transcript'])
                                 for b in blocks)
        frames = [f['file'] for b in blocks for f in b['frames']][:MAX_FRAMES]
        cont = ('\n\n[이어서]\n앞 구간에서 이미 세운 논점입니다. 겹치지 말고 이어서 쓰세요.\n'
                + '\n'.join('- ' + p['title'] for p in points)) if points else ''
        prompt = (
            '%s\n%s\n\n%s\n\n'
            '[관] %s\n\n'
            '[교재 본문 — 이 관의 범위를 알기 위한 참고. 여기 있는 내용을 그대로 옮기지 말고,\n'
            ' 강의가 실제로 다룬 것만 쓰세요.]\n%s\n\n'
            '[강의 전사 (%d/%d)]\n%s%s\n\n'
            '첨부한 이미지는 그 구간의 판서 화면입니다. 수식·도식이 텍스트에 없으면 여기서 읽어 반영하세요.'
            % (STYLE, SUBJECT_RULES.get(subject, ''), catalog,
               ' / '.join(sec['path']), sec['body'][:12000],
               i, len(chunks), transcript, cont)
        )
        raw, usage = call_gemini(key_holder['key'], prompt, frames)
        got = parse_points(raw)
        points.extend(got)
        usage_holder['in'] += usage.get('promptTokenCount', 0)
        usage_holder['out'] += usage.get('candidatesTokenCount', 0)
    return points


key_holder = {'key': None}
usage_holder = {'in': 0, 'out': 0}


def track_path(base, unit, phase):
    return base / 'track' / ('%s.%s.json' % (unit, phase))


def do_check(subject, phase):
    base = STUDY / subject / 'lectures'
    align = json.loads((base / 'align.json').read_text(encoding='utf-8'))
    names = template_names()
    tdir = base / 'track'
    if not tdir.exists():
        sys.exit('트랙이 아직 없습니다: %s' % tdir)
    total_issues, total_points, total_leaves = 0, 0, 0
    for f in sorted(tdir.glob('*.%s.json' % phase)):
        track = json.loads(f.read_text(encoding='utf-8'))
        issues = check_track(track, align['by_leaf'], names)
        total_issues += len(issues)
        for lf in track.get('leaves', []):
            total_leaves += 1
            total_points += len(lf.get('points') or [])
        for i in issues:
            print('  ⚠ %s' % i)
    print('\n관 %d개 · 논점 %d개 · 문제 %d건' % (total_leaves, total_points, total_issues))
    orphan_secs = 0
    for f in sorted(tdir.glob('*.%s.json' % phase)):
        track = json.loads(f.read_text(encoding='utf-8'))
        orphan_secs += sum(o.get('sec', 0) for o in track.get('orphans') or [])
    if orphan_secs:
        print('관에 안 붙은 구간 합계 %.1f분' % (orphan_secs / 60))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--phase', default='basic')
    ap.add_argument('--limit', type=int)
    ap.add_argument('--only', help='특정 leaf_id 하나만')
    ap.add_argument('--check', action='store_true', help='생성하지 않고 검증만')
    ap.add_argument('--model', default=MODEL)
    args = ap.parse_args()

    if args.check:
        do_check(args.subject, args.phase)
        return

    import generate_notes
    generate_notes.MODEL = args.model

    env = {}
    for line in (REPO / '.env').read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    key_holder['key'] = env.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    if not key_holder['key']:
        sys.exit('GEMINI_API_KEY 없음')

    base = STUDY / args.subject / 'lectures'
    align = json.loads((base / 'align.json').read_text(encoding='utf-8'))
    nm_path = base / 'note_map.json'
    note_map = (json.loads(nm_path.read_text(encoding='utf-8'))
                if nm_path.exists() else {'pages': [], 'by_leaf': {}})
    pdf = DEFAULT_PDF if args.subject == 'economics' else None
    pages_text = {p['page']: p['text'] for p in extract_note_pages(pdf)} if pdf else {}
    sections = load_leaf_sections(args.subject)
    tdir, kdir = WORK / 'transcripts' / args.subject, WORK / 'keyframes' / args.subject
    catalog = load_viz_catalog()
    meta = lecture_meta(align)

    targets = [lid for lid in align['by_leaf'] if lid in sections]
    if args.only:
        targets = [t for t in targets if t == args.only]
    if args.limit:
        targets = targets[:args.limit]
    print('대상 관 %d개 · 모델 %s\n' % (len(targets), args.model))

    by_unit = {}
    t0 = time.time()
    for n, lid in enumerate(targets, 1):
        sec = sections[lid]
        title = sec['path'][-1] if sec['path'] else lid
        # 정렬 순서를 트랙 기준으로 다시 잡는다 — 순서가 곧 산출물이다.
        align['by_leaf'][lid] = order_spans(align['by_leaf'][lid], meta)
        bundle = build(args.subject, lid, pages_text, note_map, align, tdir, kdir)
        if not bundle['lectures']:
            print('  [%d/%d] 건너뜀(강의 구간 없음) %s' % (n, len(targets), title))
            continue
        try:
            pts = gen_leaf(lid, sec, bundle, catalog, args.subject)
        except Exception as e:
            print('  [%d/%d] ❌ 실패 %s' % (n, len(targets), e))
            continue
        if not pts:
            print('  [%d/%d] ❌ 논점 0개 %s' % (n, len(targets), title))
            continue
        by_unit.setdefault(sec['unit_code'], []).append((lid, title, pts))
        print('  [%d/%d] %-34s 논점 %d개 · %d분' % (n, len(targets), title[:34],
                                                  len(pts), bundle['total_minutes']))

    out_dir = base / 'track'
    out_dir.mkdir(parents=True, exist_ok=True)
    for unit, items in by_unit.items():
        dst = track_path(base, unit, args.phase)
        old = json.loads(dst.read_text(encoding='utf-8')) if dst.exists() else None
        # 기존 관 순서를 지키고 이번에 만든 관만 갈아끼운다.
        # 통째로 다시 쓰면 이번에 안 돌린 관이 사라진다(generate_notes 와 같은 규칙).
        leaves = list((old or {}).get('leaves') or [])
        index = {lf.get('leaf_id'): i for i, lf in enumerate(leaves)}
        for lid, title, pts in items:
            li = index.get(lid, len(leaves))
            for seq, p in enumerate(pts, 1):
                p['seq'] = seq
                p['id'] = make_point_id(unit, li, seq)
                p.setdefault('viz', None)
                p.setdefault('check', None)
                p.setdefault('src', [])
            entry = {'leaf_id': lid, 'title': title, 'points': pts}
            if lid in index:
                leaves[index[lid]] = entry
            else:
                leaves.append(entry)
                index[lid] = len(leaves) - 1
        track = {'subject': args.subject, 'phase': args.phase, 'unit_code': unit,
                 'leaves': leaves, 'orphans': (old or {}).get('orphans') or []}
        if old:
            d = diff_ids(old, track)
            if d['removed']:
                print('  ⚠ %s: 사라진 논점 id %d개 — 진도 확인 필요' % (unit, len(d['removed'])))
        dst.write_text(json.dumps(track, ensure_ascii=False, indent=1), encoding='utf-8')

    print('\n유닛 %d개 저장 · %.1f분' % (len(by_unit), (time.time() - t0) / 60))
    print('토큰 in %s / out %s' % ('{:,}'.format(usage_holder['in']),
                                  '{:,}'.format(usage_holder['out'])))


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: 캐시를 지우고 2관만 생성**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
rm -rf scripts/lectures/__pycache__
python3 scripts/lectures/build_topic_track.py economics --phase basic --limit 2
```

Expected: `대상 관 2개` 후 관마다 `논점 N개 · M분`이 찍히고, `viewer/public/data/study/economics/lectures/track/*.basic.json` 생성.

**실패 시:** "강의 구간 없음"이 뜨면 외장이 안 붙었거나 `__pycache__`에 옛 경로가 남은 것이다(인수인계서 5-1). `ls "/Volumes/T7 Shield/인터넷강의/_ai_pipeline/transcripts/economics" | head` 로 확인한다.

- [ ] **Step 3: 산출물을 눈으로 검토**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 -c "
import json,glob
for f in glob.glob('viewer/public/data/study/economics/lectures/track/*.basic.json'):
    d=json.load(open(f))
    for lf in d['leaves']:
        print('===',lf['title'],len(lf['points']),'논점')
        for p in lf['points'][:3]:
            print(' ',p['seq'],p['title'],'|',p['gist'][:40],'| viz',(p.get('viz') or {}).get('template'))
        print('  body 예시:',lf['points'][0]['body'][:200])
"
```

확인할 것: ① 논점 순서가 강의 진행 순서인가 ② "강사·강의" 단어가 없는가 ③ body가 교재 복붙이 아니라 강의 설명인가 ④ viz가 억지로 붙지 않았는가.

- [ ] **Step 4: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add scripts/lectures/build_topic_track.py
git commit -m "feat(강의): 논점 트랙 생성 CLI

전사를 잘라내지 않고 나눠 호출해 관별 논점을 강의 진행 순서로 세운다.
viz 카탈로그는 vizRegistry 에서 읽어 주입."
```

---

## Task 3: `--check` 검증을 실제 트랙에 돌려 기준을 맞춘다

**Files:**
- Modify: `scripts/lectures/build_topic_track.py` (검증 결과에 따른 프롬프트·상수 조정)

**Interfaces:**
- Consumes: Task 2가 만든 `track/*.basic.json`
- Produces: 없음 (품질 게이트)

- [ ] **Step 1: 검증 실행**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 scripts/lectures/build_topic_track.py economics --phase basic --check
```

Expected: `관 2개 · 논점 N개 · 문제 0건`

- [ ] **Step 2: 문제가 나오면 원인별로 대응**

| 보고 | 원인 | 대응 |
|---|---|---|
| `앵커 …가 이 관의 구간 밖` | 다른 관 내용이 새어 들어옴 | `STYLE`의 "이 관 하나" 지시를 강화하고 해당 관만 `--only`로 재생성 |
| `미등록 템플릿` | 카탈로그 파싱이 이름을 놓침 | `load_viz_catalog()`의 정규식을 확인. 그래도 나면 프롬프트에 "아래 목록의 이름만" 재강조 |
| `논점 수 3개 미만` | 전사가 짧거나 추출 실패 | `bundle['total_minutes']`를 같이 보고 실제로 짧은 관인지 확인. 짧으면 정상 |
| `논점 수 40개 초과` | 잘게 쪼갬 | `STYLE`에 "하나의 논점은 한 번에 설명할 수 있는 크기" 문장 추가 후 재생성 |

- [ ] **Step 3: 문제가 0건이 될 때까지 반복 후 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add scripts/lectures/build_topic_track.py
git commit -m "fix(강의): 논점 트랙 프롬프트·검증 기준 조정"
```

---

## Task 4: 경제학 97관 전량 생성

**Files:**
- Create: `viewer/public/data/study/economics/lectures/track/*.basic.json`

**Interfaces:**
- Consumes: Task 2·3의 CLI
- Produces: 앱이 fetch할 트랙 파일 전량

- [ ] **Step 1: 전량 생성**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 scripts/lectures/build_topic_track.py economics --phase basic
```

Expected: `대상 관 97개`. 60~90분. 끝에 `토큰 in … / out …`.

이미 만든 관도 다시 돈다(`--limit` 없이 돌리면 전량). 중간에 끊기면 그때까지의 유닛은 저장돼 있으므로 다시 돌려도 안전하다.

- [ ] **Step 2: 검증**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 scripts/lectures/build_topic_track.py economics --phase basic --check
```

Expected: `관 97개 · 논점 …개 · 문제 0건`

- [ ] **Step 3: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/public/data/study/economics/lectures/track
git commit -m "feat(강의): 경제학 논점 트랙 97관 생성"
```

---

## Task 5: viz 단계 재생

**Files:**
- Create: `viewer/src/viz/steps.js`
- Create: `viewer/src/viz/steps.test.js`
- Create: `viewer/src/viz/StepPlayer.jsx`
- Modify: `viewer/src/viz/VizRouter.jsx`

**Interfaces:**
- Consumes: `viewer/src/viz/validate.js`의 `validate(schema, value)`, `vizRegistry.getTemplate(name)`
- Produces:
  - `mergeStep(base, step) -> object` — `step`의 `label`을 뺀 나머지를 `base` 위에 얕게 병합
  - `stepParamsList(params) -> array` — `params.steps`가 있으면 각 단계 병합 결과 배열, 없으면 `[params]`
  - `<StepPlayer template={tpl} paramsList={[...]} labels={[...]} />`

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`viewer/src/viz/steps.test.js`:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { mergeStep, stepParamsList } from './steps.js';

test('mergeStep은 label을 빼고 얕게 덮어쓴다', () => {
  const base = { scenario: 'A', shifts: [], axes: { x_label: 'Q' } };
  const out = mergeStep(base, { label: '2단계', shifts: [{ curve: 'D' }] });
  assert.equal(out.label, undefined);
  assert.equal(out.scenario, 'A');
  assert.deepEqual(out.shifts, [{ curve: 'D' }]);
  assert.deepEqual(out.axes, { x_label: 'Q' });
});

test('mergeStep은 base를 변형하지 않는다', () => {
  const base = { shifts: [] };
  mergeStep(base, { shifts: [{ curve: 'S' }] });
  assert.deepEqual(base.shifts, []);
});

test('steps가 없으면 단일 항목', () => {
  const p = { scenario: 'A' };
  assert.deepEqual(stepParamsList(p), [{ scenario: 'A' }]);
});

test('steps는 순서대로 병합된다', () => {
  const p = {
    scenario: 'A',
    steps: [{ label: '1', shifts: [] }, { label: '2', shifts: [{ curve: 'D' }] }],
  };
  const list = stepParamsList(p);
  assert.equal(list.length, 2);
  assert.equal(list[0].scenario, 'A');
  assert.deepEqual(list[1].shifts, [{ curve: 'D' }]);
  assert.equal(list[1].steps, undefined);
});

test('steps가 빈 배열이면 단일 항목으로 폴백', () => {
  assert.deepEqual(stepParamsList({ scenario: 'A', steps: [] }), [{ scenario: 'A' }]);
});
```

- [ ] **Step 2: 테스트가 실패하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && node --test src/viz/steps.test.js
```

Expected: FAIL — `Cannot find module .../src/viz/steps.js`

- [ ] **Step 3: `steps.js` 구현**

```js
// viz 단계 재생 — params.steps 를 base params 위에 병합한다.
// 템플릿 18개는 전부 순수 params → SVG 라서, 여기서 파라미터만 갈아 끼우면
// 템플릿 파일을 하나도 안 건드리고 전부 애니메이션이 된다.

/** step 의 label 을 빼고 나머지를 base 위에 얕게 덮어쓴다. base 는 건드리지 않는다. */
export function mergeStep(base, step) {
  const { label, ...rest } = step || {};
  void label;
  return { ...base, ...rest };
}

/** params → 단계별 params 배열. steps 가 없으면 길이 1. */
export function stepParamsList(params) {
  const { steps, ...base } = params || {};
  if (!Array.isArray(steps) || steps.length === 0) return [base];
  return steps.map((s) => mergeStep(base, s));
}

/** 화면에 띄울 단계 라벨. 없으면 1-based 번호. */
export function stepLabels(params) {
  const steps = params?.steps;
  if (!Array.isArray(steps) || steps.length === 0) return [];
  return steps.map((s, i) => s?.label || `${i + 1}단계`);
}
```

- [ ] **Step 4: 테스트가 통과하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && node --test src/viz/steps.test.js
```

Expected: 5 pass

- [ ] **Step 5: `StepPlayer.jsx` 작성**

```jsx
// 단계 재생기 — 같은 템플릿을 단계별 params 로 갈아 끼운다.
//
// ponytail: 템플릿이 계산된 좌표를 SVG 속성으로 직접 찍기 때문에 단계 전환은 점프다.
// 크로스페이드로 눈에 덜 거슬리게만 했다. 선·점 기반 템플릿(SupplyDemand·CostCurves·
// IsLm·PhillipsCurve)은 CSS 로 지오메트리 전이를 걸면 Chrome·Safari 에서 실제로
// 미끄러진다. 그게 필요해지면 각 단계를 같은 명령 구조의 path 로 뽑아 보간한다.
import { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Play, Pause } from 'lucide-react';

const STEP_MS = 1600;

export default function StepPlayer({ Comp, paramsList, labels }) {
  const [i, setI] = useState(0);
  const [playing, setPlaying] = useState(false);
  const last = paramsList.length - 1;
  const timer = useRef(null);

  useEffect(() => {
    if (!playing) return undefined;
    timer.current = setInterval(() => {
      setI((prev) => {
        if (prev >= last) { setPlaying(false); return prev; }
        return prev + 1;
      });
    }, STEP_MS);
    return () => clearInterval(timer.current);
  }, [playing, last]);

  const go = (n) => { setPlaying(false); setI(Math.max(0, Math.min(last, n))); };

  return (
    <div>
      <div key={i} style={{ animation: 'vizStepIn 0.28s ease-out' }}>
        <Comp params={paramsList[i]} />
      </div>
      <div style={{
        display: 'flex', alignItems: 'center', gap: 8,
        padding: '6px 10px', borderTop: '1px solid #e5e7eb',
      }}>
        <button onClick={() => go(i - 1)} disabled={i === 0}
          aria-label="이전 단계" style={ctrl(i === 0)}><ChevronLeft size={15} /></button>
        <button onClick={() => (i >= last ? go(0) : setPlaying((p) => !p))}
          aria-label={playing ? '일시정지' : '재생'} style={ctrl(false)}>
          {playing ? <Pause size={15} /> : <Play size={15} />}
        </button>
        <button onClick={() => go(i + 1)} disabled={i === last}
          aria-label="다음 단계" style={ctrl(i === last)}><ChevronRight size={15} /></button>
        <span style={{ fontSize: '0.78rem', color: '#374151', fontWeight: 700 }}>
          {labels[i] || `${i + 1}단계`}
        </span>
        <span style={{ marginLeft: 'auto', display: 'flex', gap: 4 }}>
          {paramsList.map((_, n) => (
            <button key={n} onClick={() => go(n)} aria-label={`${n + 1}단계로`}
              style={{
                width: 7, height: 7, padding: 0, borderRadius: '50%', border: 'none',
                cursor: 'pointer', background: n === i ? '#374151' : '#d1d5db',
              }} />
          ))}
        </span>
      </div>
    </div>
  );
}

function ctrl(disabled) {
  return {
    width: 26, height: 26, borderRadius: 6, border: '1px solid #d1d5db',
    background: '#fff', cursor: disabled ? 'default' : 'pointer',
    opacity: disabled ? 0.35 : 1,
    display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#374151',
  };
}
```

`viewer/src/index.css` 끝에 키프레임을 추가한다:

```css
@keyframes vizStepIn { from { opacity: 0.25; } to { opacity: 1; } }
```

- [ ] **Step 6: `VizRouter.jsx`가 steps를 위임하도록 수정**

`viewer/src/viz/VizRouter.jsx`에서 import에 추가:

```js
import { stepParamsList, stepLabels } from './steps';
import StepPlayer from './StepPlayer';
```

`const v = validate(tpl.schema, params);` 줄을 다음으로 교체한다. 각 단계의 병합 결과를 **기존 검증기로 그대로** 검사한다 — 새 검증기를 만들지 않는다.

```js
  const paramsList = stepParamsList(params);
  const labels = stepLabels(params);
  const errs = [];
  paramsList.forEach((p, i) => {
    const r = validate(tpl.schema, p);
    if (!r.ok) errs.push(...r.errors.map((e) => (paramsList.length > 1 ? `[${i + 1}단계] ${e}` : e)));
  });
  const v = { ok: errs.length === 0, errors: errs };
```

그리고 렌더 부분의 `<Comp params={params} />`를 교체:

```jsx
          {paramsList.length > 1
            ? <StepPlayer Comp={Comp} paramsList={paramsList} labels={labels} />
            : <Comp params={paramsList[0]} />}
```

- [ ] **Step 7: 테스트와 린트 통과 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && node --test src/viz/steps.test.js && npm run lint
```

Expected: 5 pass, lint 에러 없음

- [ ] **Step 8: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/viz/steps.js viewer/src/viz/steps.test.js viewer/src/viz/StepPlayer.jsx viewer/src/viz/VizRouter.jsx viewer/src/index.css
git commit -m "feat(시각자료): viz 템플릿 단계 재생

params.steps 를 VizRouter 한 곳에서 병합해 템플릿 18개가 전부 단계 재생을
지원한다. 각 단계는 기존 validate 로 그대로 검증한다."
```

---

## Task 6: `trackProgress.js` — 진도 저장과 coverage 계산

**Files:**
- Create: `viewer/src/trackProgress.js`
- Create: `viewer/src/trackProgress.test.js`

**Interfaces:**
- Consumes: 없음 (localStorage는 주입 가능하게 만들어 테스트한다)
- Produces:
  - `STATE = { NEW: 0, SEEN: 1, PASSED: 2 }`
  - `getTrackProgress() -> object` / `setPointState(leafId, pointId, state)`
  - `leafCoverage(leaf, progress) -> number` — 통과한 논점 ÷ 전체
  - `leafCounts(leaf, progress) -> {total, seen, passed}`
  - `nextPoint(leaf, progress) -> object|null` — 아직 통과 못 한 첫 논점

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`viewer/src/trackProgress.test.js`:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { STATE, leafCoverage, leafCounts, nextPoint } from './trackProgress.js';

const leaf = { leaf_id: 'L1', points: [{ id: 'p1' }, { id: 'p2' }, { id: 'p3' }, { id: 'p4' }] };

test('기록이 없으면 coverage 0', () => {
  assert.equal(leafCoverage(leaf, {}), 0);
});

test('통과한 논점만 센다 — 설명만 본 것은 안 센다', () => {
  const prog = { L1: { p1: STATE.PASSED, p2: STATE.SEEN } };
  assert.equal(leafCoverage(leaf, prog), 0.25);
});

test('전부 통과하면 1', () => {
  const prog = { L1: { p1: 2, p2: 2, p3: 2, p4: 2 } };
  assert.equal(leafCoverage(leaf, prog), 1);
});

test('논점이 없으면 0으로 나누지 않는다', () => {
  assert.equal(leafCoverage({ leaf_id: 'X', points: [] }, {}), 0);
});

test('leafCounts는 seen에 passed를 포함한다', () => {
  const prog = { L1: { p1: STATE.PASSED, p2: STATE.SEEN } };
  assert.deepEqual(leafCounts(leaf, prog), { total: 4, seen: 2, passed: 1 });
});

test('nextPoint는 통과 못 한 첫 논점', () => {
  const prog = { L1: { p1: STATE.PASSED, p2: STATE.SEEN } };
  assert.equal(nextPoint(leaf, prog).id, 'p2');
});

test('전부 통과하면 nextPoint는 null', () => {
  const prog = { L1: { p1: 2, p2: 2, p3: 2, p4: 2 } };
  assert.equal(nextPoint(leaf, prog), null);
});

test('진도에 없는 관은 첫 논점부터', () => {
  assert.equal(nextPoint(leaf, {}).id, 'p1');
});
```

- [ ] **Step 2: 테스트가 실패하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && node --test src/trackProgress.test.js
```

Expected: FAIL — `Cannot find module .../src/trackProgress.js`

- [ ] **Step 3: `trackProgress.js` 구현**

```js
// 논점 트랙 진도 — 관마다 어느 논점을 소진했는지.
//
// 이 값이 mastery.phases.basic.coverage 를 대체한다. 지금까지 coverage 는 AI 가
// 대화 끝에 자기 입으로 추정한 값(coverage_delta)이라 믿을 근거가 없었다.
// 통과한 논점 ÷ 전체 논점은 실측이다.

const KEY = 'ailearn-track-progress';

export const STATE = { NEW: 0, SEEN: 1, PASSED: 2 };

function read() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || '{}');
  } catch {
    return {};
  }
}

export function getTrackProgress() {
  return read();
}

export function setPointState(leafId, pointId, state) {
  if (!leafId || !pointId) return read();
  const all = read();
  const leaf = { ...(all[leafId] || {}) };
  // 되돌리지 않는다 — 통과한 논점을 다시 열어봤다고 진도가 깎이면 안 된다.
  leaf[pointId] = Math.max(leaf[pointId] || 0, state);
  all[leafId] = leaf;
  try { localStorage.setItem(KEY, JSON.stringify(all)); } catch { /* 용량 초과 무시 */ }
  return all;
}

export function resetLeafProgress(leafId) {
  const all = read();
  delete all[leafId];
  try { localStorage.setItem(KEY, JSON.stringify(all)); } catch { /* noop */ }
  return all;
}

export function leafCounts(leaf, progress) {
  const pts = leaf?.points || [];
  const rec = (progress || {})[leaf?.leaf_id] || {};
  let seen = 0; let passed = 0;
  for (const p of pts) {
    const s = rec[p.id] || 0;
    if (s >= STATE.SEEN) seen += 1;
    if (s >= STATE.PASSED) passed += 1;
  }
  return { total: pts.length, seen, passed };
}

export function leafCoverage(leaf, progress) {
  const { total, passed } = leafCounts(leaf, progress);
  return total ? passed / total : 0;
}

export function nextPoint(leaf, progress) {
  const pts = leaf?.points || [];
  const rec = (progress || {})[leaf?.leaf_id] || {};
  return pts.find((p) => (rec[p.id] || 0) < STATE.PASSED) || null;
}
```

- [ ] **Step 4: 테스트가 통과하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && node --test src/trackProgress.test.js
```

Expected: 8 pass

`localStorage`는 순수 함수(`leafCoverage`·`leafCounts`·`nextPoint`) 테스트에서 쓰이지 않으므로 Node에서 그대로 돈다.

- [ ] **Step 5: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/trackProgress.js viewer/src/trackProgress.test.js
git commit -m "feat(개념완성): 논점 진도 저장 + coverage 실측 계산"
```

---

## Task 7: 「개념 완성」 화면

**Files:**
- Create: `viewer/src/ConceptTrack.jsx`

**Interfaces:**
- Consumes:
  - `trackProgress.{STATE, getTrackProgress, setPointState, leafCounts, nextPoint, leafCoverage}` (Task 6)
  - `aiLearningStore.{SUBJECTS, getCurrent, setCurrent, getChapterMastery, updateChapterMastery, markActiveToday}`
  - `ParsedText` (기존 마크다운·KaTeX·viz 렌더러)
  - `aiProviders`의 전송 함수 — 실제 이름은 `viewer/src/aiProviders.js`의 export를 확인해 그대로 쓴다
- Produces: `<ConceptTrack subjectId leaves onOpenDeep />` default export

- [ ] **Step 1: 컴포넌트 작성**

`viewer/src/ConceptTrack.jsx`:

```jsx
// 「개념 완성」 — 관의 논점 트랙을 하나씩 소진한다.
//
// 인강을 보지 않고도 강의 내용을 전부 익히는 것이 목적이다. 그래서 자유 대화가
// 아니라 **선형 트랙**이다. 남은 논점이 몇 개인지 보이는 것이 이 화면의 핵심이고,
// 그 숫자가 곧 mastery coverage 가 된다.
//
// body·viz·check 는 사전 생성분을 그대로 읽는다 — API 키 없이도, 오프라인에서도
// 여기까지는 동작한다. "더 묻기" 를 눌렀을 때만 대화 엔진이 붙는다.
import { useState, useEffect, useMemo, useCallback } from 'react';
import { ChevronRight, CheckCircle2, HelpCircle, MessageCircle } from 'lucide-react';
import ParsedText from './ParsedText';
import {
  STATE, getTrackProgress, setPointState, leafCounts, nextPoint, leafCoverage,
} from './trackProgress';
import { getChapterMastery, updateChapterMastery, markActiveToday } from './aiLearningStore';

const studyBase = (subjectId) => `/data/study/${subjectId}/`;

export default function ConceptTrack({ subjectId, leaves, onOpenDeep }) {
  const [leafId, setLeafId] = useState(null);
  const [track, setTrack] = useState(null);      // 이 관의 { leaf_id, title, points }
  const [progress, setProgress] = useState(() => getTrackProgress());
  const [idx, setIdx] = useState(0);
  const [revealed, setRevealed] = useState(false);   // check 정답 공개
  const [loading, setLoading] = useState(false);

  const leaf = useMemo(() => leaves.find((l) => l.id === leafId) || null, [leaves, leafId]);

  // 트랙 로드 — 아직 만들어지지 않은 관·회독이 대부분이므로 404 는 조용히 빈 값.
  useEffect(() => {
    if (!leaf?.unit_code) { setTrack(null); return undefined; }
    let dead = false;
    setLoading(true);
    fetch(`${studyBase(subjectId)}lectures/track/${leaf.unit_code}.basic.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        if (dead) return;
        const found = d?.leaves?.find((x) => x.leaf_id === leafId) || null;
        setTrack(found);
        setIdx(0);
        setRevealed(false);
      })
      .catch(() => { if (!dead) setTrack(null); })
      .finally(() => { if (!dead) setLoading(false); });
    return () => { dead = true; };
  }, [subjectId, leaf?.unit_code, leafId]);

  // 트랙을 열면 이어서 볼 논점으로 이동
  useEffect(() => {
    if (!track) return;
    const np = nextPoint(track, progress);
    if (np) {
      const i = track.points.findIndex((p) => p.id === np.id);
      if (i >= 0) setIdx(i);
    }
    // 진도 위치만 맞춘다. progress 를 의존성에 넣으면 답할 때마다 튄다.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [track]);

  const counts = track ? leafCounts(track, progress) : { total: 0, seen: 0, passed: 0 };
  const point = track?.points?.[idx] || null;

  // coverage 를 실측값으로 기록. 통과 논점 ÷ 전체.
  const syncCoverage = useCallback((next) => {
    if (!track || !leafId) return;
    const cov = leafCoverage(track, next);
    const prev = getChapterMastery(leafId, 'basic');
    if (Math.abs((prev.coverage || 0) - cov) < 0.001) return;
    updateChapterMastery(leafId, { coverage: cov }, 'basic');
  }, [track, leafId]);

  const mark = (state) => {
    if (!point) return;
    const next = setPointState(leafId, point.id, state);
    setProgress({ ...next });
    syncCoverage(next);
    markActiveToday();
  };

  // 논점을 열면 '설명 봄'
  useEffect(() => {
    if (point) mark(STATE.SEEN);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [point?.id]);

  const goNext = () => {
    setRevealed(false);
    setIdx((i) => Math.min((track?.points?.length || 1) - 1, i + 1));
  };

  if (!leafId) {
    return (
      <div style={{ padding: 16 }}>
        <h2 style={{ fontSize: '1.05rem', margin: '0 0 4px' }}>개념 완성</h2>
        <p style={{ color: '#6b7280', fontSize: '0.84rem', margin: '0 0 14px' }}>
          강의가 다룬 논점을 순서대로 하나씩 익힙니다. 다 비우면 그 관을 마친 것입니다.
        </p>
        <LeafList leaves={leaves} onPick={setLeafId} />
      </div>
    );
  }

  if (loading) return <div style={{ padding: 24, color: '#6b7280' }}>불러오는 중…</div>;

  if (!track) {
    return (
      <div style={{ padding: 16 }}>
        <button onClick={() => setLeafId(null)} style={linkBtn()}>← 단원 목록</button>
        <p style={{ color: '#6b7280', fontSize: '0.86rem', marginTop: 14 }}>
          이 단원은 아직 논점 트랙이 없습니다. 강의가 다루지 않은 범위이거나 아직 생성 전입니다.
        </p>
        {onOpenDeep && (
          <button onClick={() => onOpenDeep(leafId)} style={linkBtn()}>
            AI 학습에서 대화로 배우기 →
          </button>
        )}
      </div>
    );
  }

  const done = counts.passed >= counts.total && counts.total > 0;

  return (
    <div style={{ padding: 16, maxWidth: 760, margin: '0 auto' }}>
      <button onClick={() => setLeafId(null)} style={linkBtn()}>← 단원 목록</button>

      <div style={{ margin: '10px 0 4px', display: 'flex', alignItems: 'center', gap: 8 }}>
        <div style={{ flex: 1, height: 6, background: '#e5e7eb', borderRadius: 3, overflow: 'hidden' }}>
          <div style={{
            width: `${counts.total ? (counts.passed / counts.total) * 100 : 0}%`,
            height: '100%', background: '#374151', transition: 'width 0.3s ease-out',
          }} />
        </div>
        <span style={{ fontSize: '0.76rem', color: '#6b7280', fontWeight: 700, whiteSpace: 'nowrap' }}>
          {counts.passed} / {counts.total}
        </span>
      </div>
      <div style={{ fontSize: '0.78rem', color: '#9ca3af', marginBottom: 14 }}>{track.title}</div>

      {done && (
        <div style={{
          padding: '10px 12px', marginBottom: 14, borderRadius: 8,
          background: '#f3f4f6', fontSize: '0.84rem', color: '#374151', fontWeight: 700,
        }}>
          <CheckCircle2 size={15} style={{ verticalAlign: -2, marginRight: 6 }} />
          이 관의 강의 논점을 모두 마쳤습니다.
        </div>
      )}

      {point && (
        <article>
          <h3 style={{ fontSize: '1.02rem', margin: '0 0 2px' }}>
            {point.seq}. {point.title}
          </h3>
          <p style={{ color: '#6b7280', fontSize: '0.83rem', margin: '0 0 12px' }}>{point.gist}</p>

          {point.viz && (
            <ParsedText text={'```viz ' + point.viz.template + '\n'
              + JSON.stringify({ ...point.viz.params, steps: point.viz.steps }, null, 1)
              + '\n```'} />
          )}

          <ParsedText text={point.body} />

          {point.check && (
            <section style={{
              marginTop: 16, padding: '12px 14px',
              border: '1px solid #e5e7eb', borderRadius: 8, background: '#fafafa',
            }}>
              <div style={{ fontSize: '0.76rem', color: '#6b7280', fontWeight: 700, marginBottom: 6 }}>
                <HelpCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />확인
              </div>
              <ParsedText text={point.check.q} />
              {revealed
                ? (
                  <>
                    <div style={{ marginTop: 10, paddingTop: 10, borderTop: '1px dashed #d1d5db' }}>
                      <ParsedText text={point.check.a} />
                    </div>
                    <div style={{ display: 'flex', gap: 6, marginTop: 12 }}>
                      <button onClick={() => { mark(STATE.PASSED); goNext(); }} style={primaryBtn()}>
                        이해했어요 · 다음 <ChevronRight size={14} style={{ verticalAlign: -2 }} />
                      </button>
                      <button onClick={goNext} style={ghostBtn()}>넘어가기</button>
                    </div>
                  </>
                )
                : (
                  <button onClick={() => setRevealed(true)} style={{ ...ghostBtn(), marginTop: 10 }}>
                    답 확인
                  </button>
                )}
            </section>
          )}

          {onOpenDeep && (
            <button onClick={() => onOpenDeep(leafId)} style={{ ...linkBtn(), marginTop: 16 }}>
              <MessageCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />
              이 논점에 대해 더 묻기
            </button>
          )}
        </article>
      )}

      <nav style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 22 }}>
        {track.points.map((p, i) => {
          const s = (progress[leafId] || {})[p.id] || 0;
          return (
            <button key={p.id} onClick={() => { setIdx(i); setRevealed(false); }}
              title={p.title}
              style={{
                width: 26, height: 26, borderRadius: 6, cursor: 'pointer',
                border: i === idx ? '1.5px solid #374151' : '1px solid #e5e7eb',
                background: s >= STATE.PASSED ? '#374151' : s >= STATE.SEEN ? '#d1d5db' : '#fff',
                color: s >= STATE.PASSED ? '#fff' : '#6b7280',
                fontSize: '0.7rem', fontWeight: 700,
              }}>{p.seq}</button>
          );
        })}
      </nav>
    </div>
  );
}

function LeafList({ leaves, onPick }) {
  const progress = getTrackProgress();
  return (
    <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
      {leaves.map((l) => {
        const rec = progress[l.id] || {};
        const passed = Object.values(rec).filter((s) => s >= STATE.PASSED).length;
        return (
          <li key={l.id}>
            <button onClick={() => onPick(l.id)} style={{
              width: '100%', textAlign: 'left', padding: '10px 12px',
              border: '1px solid #e5e7eb', borderRadius: 8, background: '#fff',
              cursor: 'pointer', marginBottom: 6,
              display: 'flex', alignItems: 'center', gap: 8,
            }}>
              <span style={{ flex: 1, fontSize: '0.87rem', color: '#111827' }}>
                {l.path?.slice(-1)[0] || l.title}
              </span>
              {passed > 0 && (
                <span style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700 }}>
                  {passed}개 완료
                </span>
              )}
              <ChevronRight size={14} color="#9ca3af" />
            </button>
          </li>
        );
      })}
    </ul>
  );
}

const linkBtn = () => ({
  background: 'none', border: 'none', padding: 0, cursor: 'pointer',
  color: '#4b5563', fontSize: '0.8rem', fontWeight: 700,
});
const primaryBtn = () => ({
  padding: '7px 12px', borderRadius: 7, border: 'none', cursor: 'pointer',
  background: '#374151', color: '#fff', fontSize: '0.82rem', fontWeight: 700,
});
const ghostBtn = () => ({
  padding: '7px 12px', borderRadius: 7, border: '1px solid #d1d5db', cursor: 'pointer',
  background: '#fff', color: '#374151', fontSize: '0.82rem', fontWeight: 700,
});
```

- [ ] **Step 2: `viz` 펜스 렌더 경로 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && grep -n "vizMatch" src/ParsedText.jsx | head -3
```

Expected: `ParsedText.jsx:1324`의 ``` /^```(viz)\s+([a-z0-9_-]+)\s*$/i ``` 가 보인다 — `ParsedText`가 `viz` 펜스를 `VizRouter`로 넘긴다(확인됨). 템플릿 이름(`supply-demand` 등)이 이 정규식에 맞으므로 Step 1의 펜스 조립이 그대로 동작한다.

- [ ] **Step 3: 린트 통과 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run lint
```

Expected: 에러 없음

- [ ] **Step 4: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/ConceptTrack.jsx
git commit -m "feat(개념완성): 논점 트랙 주행 화면

사전 생성 트랙을 읽어 논점을 순서대로 보여주고 진도바를 채운다.
API 키 없이도 동작하고, 더 묻기에서만 대화 엔진이 붙는다."
```

---

## Task 8: 앱 배선 — `SUB_TABS`와 라우팅

**Files:**
- Modify: `viewer/src/App.jsx` (import·`TAB_HOME_VIEW`·`SUB_TABS`·뷰 분기)
- Modify: `viewer/src/AILearning.jsx` (`study` 모드에서 개념 완성으로 안내)

**Interfaces:**
- Consumes: `ConceptTrack` (Task 7)
- Produces: `currentView === 'concept'` 라우트, `tutor` 탭의 서브탭 2개

- [ ] **Step 1: `App.jsx`에 import를 추가**

`import AILearning from './AILearning';` 아래에:

```js
import ConceptTrack from './ConceptTrack';
```

- [ ] **Step 2: 탭 홈과 서브탭을 고친다**

`TAB_HOME_VIEW`의 `tutor`를 바꾼다. 1회독이 먼저이므로 AI 학습 탭을 누르면 개념 완성이 열린다.

```js
  const TAB_HOME_VIEW = {
    home: 'home', plan: 'planner', tutor: 'concept',
    drill: 'quizHome', quiz: 'dashboard', report: 'proficiency',
  };
```

`navTab` 계산에서 `concept`도 `tutor` 탭으로 잡히게 한다. 기존:

```js
    : currentView === 'civil' ? 'tutor'
```

를 다음으로:

```js
    : (currentView === 'civil' || currentView === 'concept') ? 'tutor'
```

`SUB_TABS`에 `tutor`를 추가한다:

```js
  const SUB_TABS = {
    plan: [['planner', '플래너'], ['curriculum', '커리큘럼']],
    tutor: [['concept', '개념 완성'], ['civil', '심화']],
    report: [['proficiency', '실력 리포트'], ['stories', '합격수기']],
  };
```

`subNav`의 `aria-label` 삼항을 세 갈래로 넓힌다:

```js
      <div className="sub-nav" role="tablist"
        aria-label={navTab === 'plan' ? '계획' : navTab === 'tutor' ? 'AI 학습' : '실력'}>
```

- [ ] **Step 3: 뷰 분기를 추가**

`if (currentView === 'civil') {` 바로 위에 넣는다. `leavesBySubject`·`shell`은 그 블록에서 쓰는 것과 같은 것을 쓴다 — `civil` 분기(`App.jsx:4394` 부근)를 읽고 실제 이름을 그대로 따른다.

```jsx
  if (currentView === 'concept') {
    const subj = 'economics';   // 파일럿. 과목 전환은 다음 단계에서 붙인다.
    return shell(
      <ConceptTrack
        subjectId={subj}
        leaves={leavesBySubject[subj] || []}
        onOpenDeep={() => setCurrentView('civil')}
      />
    );
  }
```

- [ ] **Step 4: `AILearning`의 `study` 모드에 안내를 붙인다**

`study` 모드를 지우지 않는다. 2차 과목과 트랙이 없는 관은 여전히 이 모드가 필요하고, `recommendMode`가 `{mode:'study'}`를 돌려주는 경로도 살아 있어야 한다. 대신 1차 과목에서 `study`를 고르면 개념 완성으로 가는 길을 보여준다.

`AILearning.jsx`의 모드 버튼 줄 아래(모드 버튼을 그리는 `MODE_ICON` 사용 블록, `App.jsx:3140` 부근에 대응하는 `AILearning.jsx` 위치) 에 다음을 넣는다:

```jsx
{mode === 'study' && subjStage === 1 && (
  <div style={{
    margin: '8px 0', padding: '8px 10px', borderRadius: 7,
    background: '#f3f4f6', fontSize: '0.79rem', color: '#374151',
  }}>
    기본 개념은 <b>개념 완성</b>에서 강의 논점을 순서대로 익히는 편이 빠릅니다.
    여기서는 이미 아는 내용을 깊게 파고들 때 쓰세요.
  </div>
)}
```

- [ ] **Step 5: dev 서버로 실제 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run dev
```

브라우저에서 `http://localhost:5173` → 「AI 학습」 탭 → 서브탭 `[개념 완성 | 심화]`가 보이고 개념 완성이 기본으로 열린다. 경제학 단원을 하나 골라 논점이 뜨고, 「답 확인」→「이해했어요」로 진도바가 오르는지 본다. 새로고침해도 진도가 남는지 본다.

- [ ] **Step 6: 린트와 빌드**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run lint && npm run build
```

Expected: 둘 다 성공

- [ ] **Step 7: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/App.jsx viewer/src/AILearning.jsx
git commit -m "feat(개념완성): AI 학습 탭을 개념 완성/심화로 분리

탭을 7개로 늘리지 않고 기존 SUB_TABS 패턴을 쓴다(모바일 5개 한계).
study 모드는 2차·트랙 없는 관을 위해 남겨 두고 안내만 붙인다."
```

---

## Task 9: coverage 쓰기 경로 교체

**Files:**
- Modify: `viewer/src/AILearning.jsx:2286-2292`

**Interfaces:**
- Consumes: `trackProgress.{getTrackProgress, leafCoverage}` (Task 6)
- Produces: 없음 (동작 변경)

`basic` 회독에 트랙이 있으면 AI의 자기 추정으로 coverage를 올리지 않는다. 트랙이 없는 관·회독에서는 지금 동작을 그대로 둔다.

- [ ] **Step 1: import 추가**

`AILearning.jsx`의 import 목록에:

```js
import { getTrackProgress, leafCoverage } from './trackProgress';
```

- [ ] **Step 2: 트랙 보유 여부 상태를 만든다**

강의 필기를 로드하는 `useEffect`(`AILearning.jsx:1829` 부근) 아래에 같은 모양으로 추가한다:

```js
  // 이 관에 논점 트랙이 있으면 coverage 를 AI 추정으로 올리지 않는다(개념 완성이 실측한다).
  const [trackLeaf, setTrackLeaf] = useState(null);
  useEffect(() => {
    const leaf = leaves.find((l) => l.id === current?.leaf_id);
    if (!leaf?.unit_code || modeToPhase(mode) !== 'basic') { setTrackLeaf(null); return undefined; }
    let dead = false;
    fetch(`${studyBase(subjectId)}lectures/track/${leaf.unit_code}.basic.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        if (dead) return;
        setTrackLeaf(d?.leaves?.find((x) => x.leaf_id === current?.leaf_id) || null);
      })
      .catch(() => { if (!dead) setTrackLeaf(null); });
    return () => { dead = true; };
  }, [mode, current?.leaf_id, leaves, subjectId]);
```

- [ ] **Step 3: coverage 갱신 분기**

`AILearning.jsx:2286-2292`의 블록을 교체한다.

기존:

```js
        if (b && b.session_summary && current) {
          const delta = Number(b.coverage_delta) || 0.05;
          const prev = getChapterMastery(current.leaf_id, curPhase);
          updateChapterMastery(current.leaf_id, {
            coverage: Math.min(1, (prev.coverage || 0) + Math.max(0, Math.min(0.3, delta))),
        }, curPhase);
```

교체 후:

```js
        if (b && b.session_summary && current) {
          // 트랙이 있는 관은 개념 완성이 통과 논점 수로 실측한다. AI 자기 추정으로 덮지 않는다.
          if (trackLeaf) {
            updateChapterMastery(current.leaf_id, {
              coverage: leafCoverage(trackLeaf, getTrackProgress()),
            }, curPhase);
          } else {
            const delta = Number(b.coverage_delta) || 0.05;
            const prev = getChapterMastery(current.leaf_id, curPhase);
            updateChapterMastery(current.leaf_id, {
              coverage: Math.min(1, (prev.coverage || 0) + Math.max(0, Math.min(0.3, delta))),
            }, curPhase);
          }
```

- [ ] **Step 4: 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run lint && npm run build
```

dev 서버에서: 개념 완성으로 논점 2개를 통과시킨 뒤 실력 리포트의 해당 단원 coverage가 `2 / 전체` 비율과 맞는지 본다.

- [ ] **Step 5: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/AILearning.jsx
git commit -m "fix(실력): coverage 를 AI 자기추정에서 논점 소진 실측으로

트랙이 있는 관은 개념 완성이 센 통과 논점 비율을 쓴다. 트랙이 없는
관·회독은 기존 coverage_delta 를 그대로 둔다."
```

---

## Task 10: 관에 안 붙는 강의 — 과목 레벨 트랙

**Files:**
- Modify: `scripts/lectures/build_topic_track.py` (`--extra` 모드 추가)
- Create: `viewer/public/data/study/economics/lectures/track/_subject.basic.json`
- Modify: `viewer/src/ConceptTrack.jsx` (선행·총정리 트랙 노출)

**Interfaces:**
- Consumes: Task 2의 CLI 구조
- Produces: 스펙 §4-4의 `_subject.basic.json`

경제학 `basic` 53강 중 4강이 관에 안 붙는다 — `economics-basic-004`(지수), `-005`(총·평균·한계), `-035`(미시 총정리), `-051`(거시 총정리). 제목에 면수가 없어 관을 찾을 사다리가 없다. 정렬 실패가 아니라 원래 관 축에 안 맞는 강의이고, 버리면 "전부 파악"이 아니게 된다.

- [ ] **Step 1: `--extra` 모드를 추가**

`build_topic_track.py`의 `main()`에 인자를 추가한다:

```python
    ap.add_argument('--extra', action='store_true',
                    help='관에 안 붙은 강의를 과목 레벨 트랙(_subject)으로 생성')
```

그리고 `main()` 안, `targets` 계산 뒤에 분기를 넣는다:

```python
    if args.extra:
        build_extra(args, base, align, tdir, kdir, catalog)
        return
```

`build_extra`를 모듈에 추가한다:

```python
# 관 축에 안 맞는 강의 — 제목에 면수가 없어 붙을 관이 없는 것들.
# 버리면 "전부 파악"이 아니게 되므로 과목 레벨 트랙으로 담는다.
EXTRA_GROUPS = {
    'economics': [
        {'kind': 'prereq', 'title': '경제 기초수학',
         'lectures': ['economics-basic-004', 'economics-basic-005']},
        {'kind': 'review', 'title': '미시경제학 총정리',
         'lectures': ['economics-basic-035']},
        {'kind': 'review', 'title': '거시경제학 총정리',
         'lectures': ['economics-basic-051']},
    ],
}


def build_extra(args, base, align, tdir, kdir, catalog):
    groups = EXTRA_GROUPS.get(args.subject)
    if not groups:
        sys.exit('%s 는 과목 레벨 트랙 정의가 없습니다.' % args.subject)
    out_leaves = []
    for gi, g in enumerate(groups):
        blocks = []
        for lid in g['lectures']:
            f = tdir / ('%s.json' % lid)
            if not f.exists():
                print('  ⚠ 전사 없음: %s' % lid)
                continue
            tr = json.loads(f.read_text(encoding='utf-8'))
            no = align.get('by_lecture', {}).get(lid, {}).get('no')
            if no is None:
                no = int(re.search(r'(\d+)$', lid).group(1))
            blocks.append({'no': no, 'ts': '0:00',
                           'transcript': ' '.join(s['text'] for s in tr['segments']),
                           'frames': []})
        if not blocks:
            continue
        sec = {'path': [g['title']], 'body': '', 'heads': [], 'unit_code': '_subject'}
        pts = gen_leaf(None, sec, {'lectures': blocks}, catalog, args.subject)
        for seq, p in enumerate(pts, 1):
            p['seq'] = seq
            p['id'] = make_point_id('_subject', gi, seq)
            p.setdefault('viz', None)
            p.setdefault('check', None)
            p.setdefault('src', [])
        out_leaves.append({'leaf_id': None, 'kind': g['kind'],
                           'title': g['title'], 'points': pts})
        print('  %-20s 논점 %d개' % (g['title'], len(pts)))

    dst = track_path(base, '_subject', args.phase)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps({'subject': args.subject, 'phase': args.phase,
                               'unit_code': '_subject', 'leaves': out_leaves,
                               'orphans': []}, ensure_ascii=False, indent=1),
                   encoding='utf-8')
    print('저장: %s' % dst)
```

`check_track`은 `leaf_id`가 `None`이면 앵커 검사를 건너뛴다(Task 1의 구현이 이미 `spans = … if lid else []`로 그렇게 돼 있다).

- [ ] **Step 2: 생성**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 scripts/lectures/build_topic_track.py economics --phase basic --extra
```

Expected: 세 그룹의 논점 개수가 찍히고 `_subject.basic.json` 저장.

- [ ] **Step 3: `ConceptTrack.jsx`가 과목 레벨 트랙을 보여주게 한다**

`LeafList`를 감싸는 목록 화면에 선행·총정리를 붙인다. `ConceptTrack` 안에 상태와 로드를 추가한다:

```js
  const [extra, setExtra] = useState([]);
  useEffect(() => {
    let dead = false;
    fetch(`${studyBase(subjectId)}lectures/track/_subject.basic.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => { if (!dead) setExtra(d?.leaves || []); })
      .catch(() => { if (!dead) setExtra([]); });
    return () => { dead = true; };
  }, [subjectId]);
```

목록 화면(`if (!leafId)` 블록)에서 `kind`별로 위아래에 놓는다. 관에 안 붙으므로 mastery coverage에는 반영하지 않는다 — `syncCoverage`가 `leafId`가 없으면 아무것도 하지 않도록 이미 방어돼 있다.

```jsx
        {extra.filter((e) => e.kind === 'prereq').map((e) => (
          <ExtraCard key={e.title} entry={e} onPick={() => setLeafId(`_extra:${e.title}`)} />
        ))}
        <LeafList leaves={leaves} onPick={setLeafId} />
        {extra.filter((e) => e.kind === 'review').map((e) => (
          <ExtraCard key={e.title} entry={e} onPick={() => setLeafId(`_extra:${e.title}`)} />
        ))}
```

`leafId`가 `_extra:`로 시작하면 트랙 로드를 `_subject.basic.json`에서 `title`로 찾도록 로드 `useEffect`에 분기를 넣는다:

```js
    if (leafId?.startsWith('_extra:')) {
      const title = leafId.slice('_extra:'.length);
      const found = extra.find((e) => e.title === title) || null;
      setTrack(found ? { ...found, leaf_id: leafId } : null);
      setIdx(0); setRevealed(false); setLoading(false);
      return undefined;
    }
```

`ExtraCard`를 파일 끝에 추가한다:

```jsx
function ExtraCard({ entry, onPick }) {
  const progress = getTrackProgress();
  const rec = progress[`_extra:${entry.title}`] || {};
  const passed = Object.values(rec).filter((s) => s >= STATE.PASSED).length;
  return (
    <button onClick={onPick} style={{
      width: '100%', textAlign: 'left', padding: '10px 12px', marginBottom: 6,
      border: '1px dashed #d1d5db', borderRadius: 8, background: '#fafafa',
      cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 8,
    }}>
      <span style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700 }}>
        {entry.kind === 'prereq' ? '선행' : '총정리'}
      </span>
      <span style={{ flex: 1, fontSize: '0.87rem', color: '#111827' }}>{entry.title}</span>
      {passed > 0 && (
        <span style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700 }}>{passed}개 완료</span>
      )}
      <ChevronRight size={14} color="#9ca3af" />
    </button>
  );
}
```

- [ ] **Step 4: 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run lint && npm run build
```

dev 서버에서 개념 완성 목록 맨 위에 「선행 · 경제 기초수학」, 맨 아래에 「총정리 · 미시경제학 총정리」·「총정리 · 거시경제학 총정리」가 보이고, 눌러 들어가면 논점이 뜨는지 본다.

- [ ] **Step 5: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add scripts/lectures/build_topic_track.py viewer/src/ConceptTrack.jsx viewer/public/data/study/economics/lectures/track/_subject.basic.json
git commit -m "feat(개념완성): 관에 안 붙는 강의를 과목 레벨 트랙으로

경제 기초수학 특강 2강·총정리 2강은 제목에 면수가 없어 붙을 관이 없다.
버리면 '전부 파악'이 아니므로 선행/총정리로 따로 담는다."
```

---

## Self-Review

**스펙 커버리지**

| 스펙 절 | 담당 태스크 |
|---|---|
| §3 설계 개요 | 전체 |
| §4-2 트랙 스키마 | Task 1·2 |
| §4-4 과목 레벨 트랙 | Task 10 |
| §5 생성 스크립트 | Task 2 |
| §5-1 강좌별 정렬 | Task 1 `order_spans` |
| §5-1 긴 관 무손실 분할 | Task 1 `chunk_lectures` |
| §5-2 논점 개수 규율 | Task 1 `check_track` |
| §5-3 orphans | Task 2 스키마에 자리 확보, Task 3 `--check` 합계 보고 |
| §6-1 화면 분리 | Task 8 |
| §6-2 네비게이션 | Task 8 |
| §6-3 논점 화면 | Task 7 |
| §7-1 논점 상태 | Task 6 |
| §7-2 coverage 교체 | Task 6·9 |
| §8 단계 재생 | Task 5 |
| §9-2 검증 | Task 1·3 |

**미착수로 남기는 것 (스펙 §10에 이미 "하지 않는 것"으로 적힘)**

- `orphans` 자동 채우기 — Task 2가 필드만 만들고 값은 비워 둔다. 경제학은 `align.by_leaf`가 곧 전량이라 orphan이 구조적으로 생기지 않고, 민법·회계로 넓힐 때 채운다.
- 판서 키프레임 화면 노출, 2·3·4회독, 전 과목 확장.

**타입 일관성 확인**

- `make_point_id(unit_code, leaf_idx, seq)` — Task 1 정의, Task 2 Step 1과 Task 10 Step 1에서 같은 인자 순서로 호출.
- `check_track(track, align_by_leaf, template_names)` — Task 1 정의, Task 2의 `do_check`에서 같은 순서로 호출.
- `leafCoverage(leaf, progress)` — Task 6 정의, Task 7 `syncCoverage`와 Task 9 Step 3에서 동일 시그니처.
- `STATE.PASSED = 2` — Task 6 정의, Task 7·10에서 같은 값으로 비교.
- 트랙 파일 경로 `lectures/track/{unit}.{phase}.json` — Task 2 `track_path`, Task 7 fetch, Task 9 fetch가 모두 동일.
