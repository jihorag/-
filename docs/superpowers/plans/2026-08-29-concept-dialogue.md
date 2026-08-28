# 개념 완성 2차 (목차 호응 + 캐릭터 대화) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 개념 완성의 목차를 AI 학습과 완전히 일치시키고, 논점을 "읽는 글"에서 "캐릭터 넷과 주고받는 대화"로 바꾼다.

**Architecture:** 목차는 이미 세 탭이 공유하는 `buildUnitTree` 를 재사용한다(새 축을 만들지 않는다). 목차의 빈칸은 새 전사 없이 **절 안에서 관별로 구간을 다시 나누어** 회수한다. 논점 스키마는 `body` 를 지우지 않고 `turns` 를 더해 점진 이행하며, 화면은 턴을 하나씩 열고 `quiz` 턴에서 선택을 강제한다. 대사·선택지·오답 반박은 배치로 사전 생성하고, 「더 묻기」만 실시간이다.

**Tech Stack:** Python 3.9 (stdlib) · Gemini `gemini-3-flash-preview` · React 19 + Vite 8 · `node --test` (Node 22) · `python3 -m unittest`

**Spec:** `docs/superpowers/specs/2026-08-29-concept-dialogue-design.md`

## Global Constraints

- **과목은 `economics`, phase 는 `basic`.** 다른 과목·회독은 범위 밖이다.
- **재정학은 개념 완성 화면에서만 제외한다.** taxonomy 는 건드리지 않는다. AI 학습·드릴·문제풀이는 지금처럼 재정학을 포함한다.
- **과목명을 코드에 박지 않는다.** 제외 규칙은 `scope.json` 데이터로 둔다.
- **"강사·강의·선생님" 이라는 단어는 여전히 금지.** 캐릭터 「선생」이 말하는 것이지 실제 강사를 인용하는 게 아니다.
- **전사에 없는 결론·수치·예시를 지어내지 않는다.** 전사가 결론 전에 끊기면 채우지 않는다. (1차 구현에서 실제로 발생한 사고다.)
- **디자인은 무채색.** 회색조(`#111827` `#374151` `#6b7280` `#94a3b8` `#a3a3a3` `#d1d5db` `#e5e7eb` `#f3f4f6` `#fafafa` `#fff`)만. 캐릭터를 **색으로 구분하지 않는다.** 아바타 일러스트를 만들지 않는다.
- **새 의존성 금지.** 아이콘은 이미 설치된 `lucide-react`.
- **`viewer/src/trackProgress.js` 를 수정하지 않는다.** 진도 모델은 이미 맞다. `PASSED` 를 찍는 시점만 바뀐다.
- **Python 3.9 호환.** `match` 문, `X | Y` 타입 표기 금지.
- **경로는 `scripts/lectures/_paths.py` 만 쓴다.** 드라이브 이름을 코드에 박지 않는다. 외장 파일명은 NFD 이고 `._*` AppleDouble 파일이 섞여 있다.
- **경로 관련 코드를 만진 뒤에는 `rm -rf scripts/lectures/__pycache__`.**
- **테스트는 `node --test`(JSX import 금지) 와 `python3 -m unittest`.** 로직은 `.js`, 화면은 `.jsx` 로 가른다.
- **`git add` 는 반드시 경로 지정.** `git add -A` / `git add .` 금지.
- 커밋 메시지 관례: `feat(개념완성): …`, `feat(강의): …`, `fix(…): …`

---

## File Structure

| 파일 | 책임 |
|---|---|
| **Create** `viewer/src/conceptTurns.js` | 순수 — 턴 진행 상태 기계(다음 턴, 선택 판정, 2회 오답 시 공개, 통과 판정). DOM·localStorage 없음. |
| **Create** `viewer/src/conceptTurns.test.js` | `node --test`. |
| **Create** `viewer/src/trackScope.js` | 순수 — `scope.json` 을 적용해 목차 범위를 거른다. |
| **Create** `viewer/src/trackScope.test.js` | `node --test`. |
| **Create** `viewer/src/ConceptOutline.jsx` | 목차 화면 — `buildUnitTree` 트리 + 관별 남은 논점 수. |
| **Create** `viewer/src/ConceptScene.jsx` | 논점 하나의 대화 화면 — 말풍선·선택지·viz·예시문제·TTS. |
| **Modify** `viewer/src/ConceptTrack.jsx` | 셸로 축소 — 목차↔장면 전환, 트랙 로드, 진도 저장. |
| **Modify** `viewer/src/ParsedText.jsx:238` | `CALLOUT_TONES` 에 캐릭터 이모지 3종 등록. |
| **Modify** `viewer/src/App.jsx` | 「더 묻기」가 논점 컨텍스트를 넘기도록. |
| **Create** `scripts/lectures/split_spans_by_item.py` | 절 안에서 관별로 spans 재분배 → `align_split.json`. |
| **Modify** `scripts/lectures/build_topic_track.py` | `align_split.json` 소비, `turns` 프롬프트, `_index.json` 생성, `--check` 확장. |
| **Modify** `scripts/lectures/track_core.py` | `check_track` 에 `turns`·`quiz`·오답 `reply` 검사 추가. |
| **Modify** `scripts/lectures/test_track_core.py` | 위 검사의 테스트. |

`ConceptTrack.jsx` 는 지금 318줄이다. 목차 트리와 대화 렌더를 여기 다 넣으면 500줄을 훌쩍 넘긴다. 그래서 목차(`ConceptOutline`)와 장면(`ConceptScene`)을 갈라내고 `ConceptTrack` 은 둘을 잇는 셸로 남긴다.

---

## Task 1: `conceptTurns.js` — 턴 진행 상태 기계

**Files:**
- Create: `viewer/src/conceptTurns.js`
- Test: `viewer/src/conceptTurns.test.js`

**Interfaces:**
- Consumes: 없음 (순수)
- Produces:
  - `WHO = { ask, teach, gotcha, mate, quiz }`
  - `initTurnState() -> {cursor: 0, answers: {}}`
  - `visibleTurns(point, state) -> Array<{turn, index, picked, solved, assisted}>`
  - `canAdvance(point, state) -> boolean`
  - `advance(point, state) -> state`
  - `choose(point, state, turnIndex, choiceIndex) -> state`
  - `isPassed(point, state) -> boolean`
  - `atEnd(point, state) -> boolean`

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`viewer/src/conceptTurns.test.js`:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import {
  WHO, initTurnState, visibleTurns, canAdvance, advance, choose, isPassed, atEnd,
} from './conceptTurns.js';

// 대사 5턴 중 3번째가 quiz — 정답은 0번 선택지.
const POINT = {
  id: 'p1',
  turns: [
    { who: 'ask', text: '이거 왜 배워요?' },
    { who: 'teach', text: '쉽게 말하면…' },
    { who: 'quiz', prompt: '가격이 오르면 공급량은?', choices: [
      { text: '늘어난다', ok: true, reply: '맞아요.' },
      { text: '줄어든다', ok: false, who: 'gotcha', reply: '그건 사는 쪽 얘기예요.' },
      { text: '안 변한다', ok: false, who: 'gotcha', reply: '그건 아주 특수한 경우예요.' },
    ] },
    { who: 'gotcha', text: '공급량 변화와 공급 변화는 다릅니다.' },
    { who: 'mate', text: '이 절은 그 구분 하나만 외우면 됩니다.' },
  ],
};

test('처음에는 첫 턴 하나만 보인다', () => {
  const s = initTurnState();
  assert.equal(visibleTurns(POINT, s).length, 1);
  assert.equal(visibleTurns(POINT, s)[0].turn.who, WHO.ask);
});

test('quiz 가 아닌 턴은 그냥 넘어간다', () => {
  let s = initTurnState();
  assert.equal(canAdvance(POINT, s), true);
  s = advance(POINT, s);
  assert.equal(visibleTurns(POINT, s).length, 2);
});

test('quiz 턴에서는 고르기 전에 못 넘어간다', () => {
  let s = advance(POINT, advance(POINT, initTurnState())); // cursor=2 (quiz)
  assert.equal(canAdvance(POINT, s), false);
});

test('정답을 고르면 넘어갈 수 있다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 0);
  assert.equal(canAdvance(POINT, s), true);
  assert.equal(visibleTurns(POINT, s)[2].solved, true);
  assert.equal(visibleTurns(POINT, s)[2].assisted, false);
});

test('오답 한 번은 기록되지만 여전히 못 넘어간다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 1);
  assert.equal(canAdvance(POINT, s), false);
  assert.deepEqual(visibleTurns(POINT, s)[2].picked, [1]);
  assert.equal(visibleTurns(POINT, s)[2].solved, false);
});

test('두 번 틀리면 정답을 알려주고 넘어가게 한다 — 막히면 학습이 멈춘다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 1);
  s = choose(POINT, s, 2, 2);
  const v = visibleTurns(POINT, s)[2];
  assert.equal(v.solved, true);
  assert.equal(v.assisted, true);       // 도움받아 넘어간 것을 기록한다
  assert.equal(canAdvance(POINT, s), true);
});

test('같은 오답을 다시 골라도 시도 수가 늘지 않는다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 1);
  s = choose(POINT, s, 2, 1);
  assert.deepEqual(visibleTurns(POINT, s)[2].picked, [1]);
  assert.equal(visibleTurns(POINT, s)[2].solved, false);
});

test('정답을 맞힌 뒤에는 선택이 바뀌지 않는다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 0);
  s = choose(POINT, s, 2, 1);
  assert.equal(visibleTurns(POINT, s)[2].solved, true);
  assert.equal(visibleTurns(POINT, s)[2].assisted, false);
});

test('마지막 턴에서 atEnd 가 참이고 더 못 넘어간다', () => {
  let s = initTurnState();
  s = advance(POINT, s); s = advance(POINT, s);
  s = choose(POINT, s, 2, 0);
  s = advance(POINT, s); s = advance(POINT, s);
  assert.equal(atEnd(POINT, s), true);
  assert.equal(canAdvance(POINT, s), false);
});

test('quiz 를 스스로 맞히면 통과', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 0);
  assert.equal(isPassed(POINT, s), true);
});

test('도움받아 넘어간 것은 통과가 아니다', () => {
  let s = advance(POINT, advance(POINT, initTurnState()));
  s = choose(POINT, s, 2, 1);
  s = choose(POINT, s, 2, 2);
  assert.equal(isPassed(POINT, s), false);
});

test('quiz 가 없는 논점은 끝까지 가면 통과 — 옛 데이터 폴백', () => {
  const old = { id: 'p0', turns: [{ who: 'teach', text: 'a' }, { who: 'mate', text: 'b' }] };
  let s = initTurnState();
  assert.equal(isPassed(old, s), false);
  s = advance(old, s);
  assert.equal(atEnd(old, s), true);
  assert.equal(isPassed(old, s), true);
});

test('turns 가 없는 옛 논점은 빈 배열을 돌려주고 터지지 않는다', () => {
  const legacy = { id: 'p9', body: '옛 교재체 서술' };
  const s = initTurnState();
  assert.deepEqual(visibleTurns(legacy, s), []);
  assert.equal(atEnd(legacy, s), true);
  assert.equal(canAdvance(legacy, s), false);
});
```

- [ ] **Step 2: 테스트가 실패하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && node --test src/conceptTurns.test.js
```

Expected: FAIL — `Cannot find module .../src/conceptTurns.js`

- [ ] **Step 3: `conceptTurns.js` 구현**

```js
// 개념 완성 — 한 논점의 대화 진행 상태 기계.
//
// 화면과 분리해 둔 이유: node --test 가 JSX 를 못 읽는다. 진행 규칙(언제 넘어갈 수
// 있는가, 무엇이 통과인가)이 이 화면의 핵심이라 테스트가 없으면 안 된다.
//
// 상태는 { cursor, answers } 뿐이다. cursor 는 지금까지 열린 마지막 턴의 인덱스.
// answers[turnIndex] = { picked: [선택지 인덱스…], solved, assisted }.

export const WHO = {
  ask: 'ask',       // 묻는 이 — 학습자 대신 묻는다
  teach: 'teach',   // 선생 — 설명한다
  gotcha: 'gotcha', // 깐깐이 — 반례·함정
  mate: 'mate',     // 복습 메이트 — 학습 조언만
  quiz: 'quiz',     // 선택지 턴
};

// 두 번 틀리면 정답을 열어 준다. 막히면 학습이 거기서 멈추기 때문이다.
// 대신 assisted 로 남겨 "스스로 맞힌 것"과 구분한다 — 통과 판정에 쓴다.
const MAX_TRIES = 2;

const turnsOf = (point) => (Array.isArray(point?.turns) ? point.turns : []);

export function initTurnState() {
  return { cursor: 0, answers: {} };
}

function answerOf(state, i) {
  return state.answers[i] || { picked: [], solved: false, assisted: false };
}

/** 지금까지 열린 턴들. 각 항목에 그 턴의 응답 상태를 붙여 돌려준다. */
export function visibleTurns(point, state) {
  const turns = turnsOf(point);
  if (!turns.length) return [];
  const last = Math.min(state.cursor, turns.length - 1);
  const out = [];
  for (let i = 0; i <= last; i += 1) {
    const a = answerOf(state, i);
    out.push({ turn: turns[i], index: i, picked: a.picked, solved: a.solved, assisted: a.assisted });
  }
  return out;
}

export function atEnd(point, state) {
  const turns = turnsOf(point);
  if (!turns.length) return true;
  return state.cursor >= turns.length - 1;
}

/** 지금 턴이 quiz 인데 아직 풀리지 않았으면 못 넘어간다. */
export function canAdvance(point, state) {
  const turns = turnsOf(point);
  if (!turns.length) return false;
  if (atEnd(point, state)) return false;
  const cur = turns[state.cursor];
  if (cur && cur.who === WHO.quiz) return answerOf(state, state.cursor).solved;
  return true;
}

export function advance(point, state) {
  if (!canAdvance(point, state)) return state;
  return { ...state, cursor: state.cursor + 1 };
}

/** 선택지를 고른다. 이미 풀린 턴이거나 같은 선택지를 다시 고르면 아무 일도 없다. */
export function choose(point, state, turnIndex, choiceIndex) {
  const turns = turnsOf(point);
  const turn = turns[turnIndex];
  if (!turn || turn.who !== WHO.quiz) return state;
  const prev = answerOf(state, turnIndex);
  if (prev.solved) return state;
  if (prev.picked.includes(choiceIndex)) return state;

  const picked = prev.picked.concat(choiceIndex);
  const ok = !!(turn.choices || [])[choiceIndex]?.ok;
  // 정답을 골랐으면 스스로 푼 것. 시도를 다 썼으면 열어 주되 도움받은 것으로 남긴다.
  const solved = ok || picked.length >= MAX_TRIES;
  const assisted = !ok && solved;

  return {
    ...state,
    answers: { ...state.answers, [turnIndex]: { picked, solved, assisted } },
  };
}

/** 통과 = 모든 quiz 를 스스로 맞혔다. quiz 가 없는 옛 논점은 끝까지 간 것으로 갈음한다. */
export function isPassed(point, state) {
  const turns = turnsOf(point);
  if (!turns.length) return false;
  const quizIdx = turns.map((t, i) => (t.who === WHO.quiz ? i : -1)).filter((i) => i >= 0);
  if (!quizIdx.length) return atEnd(point, state);
  return quizIdx.every((i) => {
    const a = answerOf(state, i);
    return a.solved && !a.assisted;
  });
}
```

- [ ] **Step 4: 테스트가 통과하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && node --test src/conceptTurns.test.js
```

Expected: 13 pass

- [ ] **Step 5: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/conceptTurns.js viewer/src/conceptTurns.test.js
git commit -m "feat(개념완성): 턴 진행 상태 기계 + 테스트

quiz 턴에서 고르기 전에는 못 넘어가고, 두 번 틀리면 열어 주되
assisted 로 남겨 '스스로 맞힌 것'과 구분한다."
```

---

## Task 2: `trackScope.js` — 목차 범위 거르기

**Files:**
- Create: `viewer/src/trackScope.js`
- Test: `viewer/src/trackScope.test.js`
- Create: `viewer/public/data/study/economics/lectures/scope.json`

**Interfaces:**
- Consumes: 없음
- Produces: `applyScope(leaves, scope) -> Array`

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`viewer/src/trackScope.test.js`:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { applyScope } from './trackScope.js';

const LEAVES = [
  { id: 'a', path: ['미시경제학', '제1장', '제1절', '제1관'] },
  { id: 'b', path: ['재정학', '제1장', '제1절', '제1관'] },
  { id: 'c', path: ['거시경제학', '제1장', '제1절', '제1관'] },
];

test('제외 목록의 세부과목이 빠진다', () => {
  const out = applyScope(LEAVES, { exclude_divisions: ['재정학'] });
  assert.deepEqual(out.map((l) => l.id), ['a', 'c']);
});

test('scope 가 없으면 원본 그대로', () => {
  assert.equal(applyScope(LEAVES, null).length, 3);
  assert.equal(applyScope(LEAVES, {}).length, 3);
});

test('원본 배열을 변형하지 않는다 — 순서가 곧 커리큘럼이다', () => {
  const copy = LEAVES.slice();
  applyScope(LEAVES, { exclude_divisions: ['재정학'] });
  assert.deepEqual(LEAVES, copy);
});

test('path 가 없는 leaf 는 버리지 않는다 — 조용한 유실 금지', () => {
  const out = applyScope([{ id: 'x' }], { exclude_divisions: ['재정학'] });
  assert.deepEqual(out.map((l) => l.id), ['x']);
});

test('제외 목록이 빈 배열이면 아무것도 안 뺀다', () => {
  assert.equal(applyScope(LEAVES, { exclude_divisions: [] }).length, 3);
});
```

- [ ] **Step 2: 테스트가 실패하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && node --test src/trackScope.test.js
```

Expected: FAIL — 모듈 없음

- [ ] **Step 3: `trackScope.js` 구현**

```js
// 개념 완성의 목차 범위. 강의가 없는 세부과목을 이 화면에서만 뺀다.
//
// taxonomy 자체는 건드리지 않는다 — AI 학습·드릴·문제풀이는 교재 기반이라
// 강의가 없어도 성립한다. 제외는 개념 완성 화면에서만 이뤄진다.
// 과목명을 코드에 박지 않으려고 규칙을 scope.json 으로 뺐다.

export function applyScope(leaves = [], scope) {
  const ex = scope?.exclude_divisions;
  if (!Array.isArray(ex) || ex.length === 0) return leaves.slice();
  const drop = new Set(ex);
  // path 가 없는 leaf 는 판단할 수 없으므로 남긴다. 조용히 사라지는 쪽이 더 나쁘다.
  return leaves.filter((l) => !(Array.isArray(l?.path) && drop.has(l.path[0])));
}
```

- [ ] **Step 4: 테스트가 통과하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && node --test src/trackScope.test.js
```

Expected: 5 pass

- [ ] **Step 5: `scope.json` 을 만든다**

`viewer/public/data/study/economics/lectures/scope.json`:

```json
{
  "exclude_divisions": ["재정학"],
  "reason": "강의 없음 — 기본이론·심화·문제풀이·모의·특강 어느 회독에도 재정학 단원이 없다. 제목에 재정/조세/공공재/후생이 걸리는 강의는 전부 미시·거시 장 안의 개별 주제다."
}
```

- [ ] **Step 6: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/trackScope.js viewer/src/trackScope.test.js viewer/public/data/study/economics/lectures/scope.json
git commit -m "feat(개념완성): 목차 범위 규칙 — 재정학 제외

taxonomy 는 그대로 두고 개념 완성 화면에서만 뺀다. 과목명을 코드에
박지 않으려고 scope.json 으로 분리했다."
```

---

## Task 3: `ParsedText` 에 캐릭터 콜아웃 등록

**Files:**
- Modify: `viewer/src/ParsedText.jsx:238` (`CALLOUT_TONES`)

**Interfaces:**
- Consumes: 없음
- Produces: `🙋`·`📖`·`🔍` 이모지로 시작하는 인용 블록이 캐릭터 톤으로 렌더된다

`CALLOUT_TONES` 는 이미 `🐶` 를 "복습 메이트(마스코트)" 로 등록해 두었고, 주석에 "다른 콜아웃과 성격이 다르므로 유일하게 푸른 계열을 쓰되 채도는 낮게 둔다" 고 적혀 있다. 나머지 캐릭터 셋을 같은 방식으로 얹는다.

- [ ] **Step 1: 톤 세 줄을 추가한다**

`viewer/src/ParsedText.jsx` 의 `CALLOUT_TONES` 안, `'🐶'` 줄 바로 아래에 넣는다:

```js
  // 개념 완성 캐릭터 — 색으로 구분하지 않는다. 화자 구분은 이름과 말풍선 좌우 위치로 한다.
  // 여기 톤은 대화 밖(교재·강의 필기)에서 같은 이모지가 인용문으로 쓰일 때를 위한 것이다.
  '🙋': { bg: '#f8f9fa', bar: '#94a3b8' },   // 묻는 이
  '📖': { bg: '#f8f8f9', bar: '#6b7280' },   // 선생 — 기존 '도입' 과 같은 톤
  '🔍': { bg: '#f8f9fa', bar: '#a3a3a3' },   // 깐깐이
```

`'📖'` 은 이미 `{ bg: '#f8f8f9', bar: '#6b7280' }` 로 등록돼 있다. **중복 키를 만들지 말고**, 이미 있으면 그대로 두고 주석만 보강한다. 파일을 먼저 읽어 확인하라.

- [ ] **Step 2: 린트로 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run lint 2>&1 | tail -3
```

Expected: 이 파일에서 새 에러 없음. (저장소 전체에 약 142건의 기존 에러가 있다 — 먼저 베이스라인을 재고 대조하라.)

- [ ] **Step 3: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/ParsedText.jsx
git commit -m "feat(개념완성): 캐릭터 콜아웃 톤 등록 (묻는 이·깐깐이)"
```

---

## Task 4: `ConceptScene.jsx` — 대화 화면

**Files:**
- Create: `viewer/src/ConceptScene.jsx`

**Interfaces:**
- Consumes: `conceptTurns.{WHO, initTurnState, visibleTurns, canAdvance, advance, choose, isPassed, atEnd}` (Task 1)
- Produces: `<ConceptScene point={…} onPassed={fn} onAsk={fn} />` default export

- [ ] **Step 1: 컴포넌트를 작성한다**

`viewer/src/ConceptScene.jsx`:

```jsx
// 논점 하나를 대화로 보여준다.
//
// 턴을 한 번에 하나씩 연다. 화면을 채워 놓고 스크롤하게 두면 그건 여전히 읽기다.
// quiz 턴에서는 고르기 전에 다음으로 못 간다 — "다음"만 눌러 통과할 수 있으면
// 이 화면의 존재 이유가 없다.
//
// turns 가 없는 옛 논점(body 만 있는 763개)은 기존 방식으로 폴백한다.
// 관 단위로 점진 갱신할 수 있게 하려는 것이다.
import { useState, useEffect, useCallback } from 'react';
import { ChevronRight, MessageCircle, HelpCircle } from 'lucide-react';
import ParsedText from './ParsedText';
import { SpeakButton } from './Speech';
import {
  WHO, initTurnState, visibleTurns, canAdvance, advance, choose, isPassed, atEnd,
} from './conceptTurns';

// 색으로 구분하지 않는다. 이름·이모지·말풍선 위치로만 화자를 가른다.
const CAST = {
  [WHO.ask]:    { name: '묻는 이', emoji: '🙋', side: 'right' },
  [WHO.teach]:  { name: '선생',    emoji: '📖', side: 'left' },
  [WHO.gotcha]: { name: '깐깐이',  emoji: '🔍', side: 'left' },
  [WHO.mate]:   { name: '복습 메이트', emoji: '🐶', side: 'left' },
};

export default function ConceptScene({ point, onPassed, onAsk }) {
  const [state, setState] = useState(initTurnState);
  const [showSolution, setShowSolution] = useState(false);

  // 논점이 바뀌면 처음부터.
  useEffect(() => { setState(initTurnState()); setShowSolution(false); }, [point?.id]);

  const passed = isPassed(point, state);
  useEffect(() => { if (passed && onPassed) onPassed(); }, [passed, onPassed]);

  const pick = useCallback((turnIndex, choiceIndex) => {
    setState((s) => choose(point, s, turnIndex, choiceIndex));
  }, [point]);

  const turns = visibleTurns(point, state);

  // 옛 논점 폴백 — turns 가 없으면 body 를 그대로 보여준다.
  if (!turns.length) {
    return (
      <article>
        <SceneHead point={point} />
        <ParsedText text={point?.body || ''} />
        {point?.check && (
          <CheckBox check={point.check} onDone={onPassed} />
        )}
        {onAsk && <AskLink onAsk={onAsk} />}
      </article>
    );
  }

  return (
    <article>
      <SceneHead point={point} />

      {turns.map(({ turn, index, picked, solved, assisted }) => (
        turn.who === WHO.quiz
          ? (
            <QuizTurn key={index} turn={turn} picked={picked} solved={solved}
              assisted={assisted} onPick={(ci) => pick(index, ci)} />
          )
          : (
            <Bubble key={index} who={turn.who} text={turn.text} viz={turn.viz} />
          )
      ))}

      {point.example && (
        <section style={exampleBox}>
          <div style={boxLabel}>
            <HelpCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />예시 문제
          </div>
          <ParsedText text={point.example.q} />
          {showSolution
            ? <div style={{ marginTop: 10, paddingTop: 10, borderTop: '1px dashed #d1d5db' }}>
                <ParsedText text={point.example.solution} />
              </div>
            : <button onClick={() => setShowSolution(true)} style={ghostBtn}>풀이 보기</button>}
        </section>
      )}

      <div style={{ display: 'flex', gap: 6, alignItems: 'center', marginTop: 16 }}>
        {canAdvance(point, state) && (
          <button onClick={() => setState((s) => advance(point, s))} style={primaryBtn}>
            다음 <ChevronRight size={14} style={{ verticalAlign: -2 }} />
          </button>
        )}
        {atEnd(point, state) && (
          <span style={{ fontSize: '0.78rem', color: '#6b7280', fontWeight: 700 }}>
            {passed ? '이 논점 완료' : '정답을 확인했습니다'}
          </span>
        )}
        {onAsk && <span style={{ marginLeft: 'auto' }}><AskLink onAsk={onAsk} /></span>}
      </div>
    </article>
  );
}

function SceneHead({ point }) {
  return (
    <header style={{ marginBottom: 14 }}>
      <h3 style={{ fontSize: '1.02rem', margin: '0 0 2px' }}>
        {point?.seq}. {point?.title}
      </h3>
      <p style={{ color: '#6b7280', fontSize: '0.83rem', margin: 0 }}>{point?.gist}</p>
      {point?.source === 'textbook' && (
        <span style={{ fontSize: '0.7rem', color: '#9ca3af', fontWeight: 700 }}>교재 기반</span>
      )}
    </header>
  );
}

function Bubble({ who, text, viz }) {
  const c = CAST[who] || CAST[WHO.teach];
  const right = c.side === 'right';
  return (
    <div style={{ display: 'flex', justifyContent: right ? 'flex-end' : 'flex-start', marginBottom: 12 }}>
      <div style={{ maxWidth: '92%' }}>
        <div style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700, marginBottom: 3,
          textAlign: right ? 'right' : 'left' }}>
          {c.emoji} {c.name}
        </div>
        <div style={{
          background: right ? '#f3f4f6' : '#fafafa',
          border: '1px solid #e5e7eb', borderRadius: 10, padding: '10px 12px',
        }}>
          <ParsedText text={text} />
          {viz && (
            <ParsedText text={'```viz ' + viz.template + '\n'
              + JSON.stringify({ ...viz.params, steps: viz.steps }, null, 1) + '\n```'} />
          )}
          <SpeakButton text={text} />
        </div>
      </div>
    </div>
  );
}

function QuizTurn({ turn, picked, solved, assisted, onPick }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700, marginBottom: 3 }}>
        {CAST[WHO.teach].emoji} {CAST[WHO.teach].name}
      </div>
      <div style={{ background: '#fafafa', border: '1px solid #e5e7eb', borderRadius: 10, padding: '10px 12px' }}>
        <ParsedText text={turn.prompt} />
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 10 }}>
          {(turn.choices || []).map((c, i) => {
            const chosen = picked.includes(i);
            const reveal = solved && c.ok;
            return (
              <button key={i} onClick={() => onPick(i)} disabled={solved || chosen}
                style={{
                  padding: '7px 12px', borderRadius: 7, cursor: solved || chosen ? 'default' : 'pointer',
                  fontSize: '0.82rem', fontWeight: 700,
                  border: reveal ? '1.5px solid #374151' : '1px solid #d1d5db',
                  background: reveal ? '#374151' : chosen ? '#f3f4f6' : '#fff',
                  color: reveal ? '#fff' : chosen ? '#9ca3af' : '#374151',
                }}>{c.text}</button>
            );
          })}
        </div>
      </div>

      {/* 고른 오답마다 그 오답 전용 반박이 붙는다. "틀렸습니다" 가 아니다. */}
      {picked.filter((i) => !(turn.choices || [])[i]?.ok).map((i) => (
        <div key={'w' + i} style={{ marginTop: 8 }}>
          <Bubble who={(turn.choices[i].who) || WHO.gotcha} text={turn.choices[i].reply} />
        </div>
      ))}
      {solved && !assisted && (turn.choices || []).some((c) => c.ok) && (
        <div style={{ marginTop: 8 }}>
          <Bubble who={WHO.teach} text={(turn.choices.find((c) => c.ok) || {}).reply || ''} />
        </div>
      )}
      {assisted && (
        <div style={{ marginTop: 8 }}>
          <Bubble who={WHO.teach}
            text={'정답은 「' + ((turn.choices || []).find((c) => c.ok) || {}).text + '」예요. '
              + (((turn.choices || []).find((c) => c.ok) || {}).reply || '')} />
        </div>
      )}
    </div>
  );
}

function CheckBox({ check, onDone }) {
  const [open, setOpen] = useState(false);
  return (
    <section style={exampleBox}>
      <div style={boxLabel}>
        <HelpCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />확인
      </div>
      <ParsedText text={check.q} />
      {open
        ? (
          <>
            <div style={{ marginTop: 10, paddingTop: 10, borderTop: '1px dashed #d1d5db' }}>
              <ParsedText text={check.a} />
            </div>
            <button onClick={onDone} style={{ ...primaryBtn, marginTop: 12 }}>이해했어요 · 다음</button>
          </>
        )
        : <button onClick={() => setOpen(true)} style={{ ...ghostBtn, marginTop: 10 }}>답 확인</button>}
    </section>
  );
}

function AskLink({ onAsk }) {
  return (
    <button onClick={onAsk} style={linkBtn}>
      <MessageCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />이 논점 더 묻기
    </button>
  );
}

const exampleBox = {
  marginTop: 16, padding: '12px 14px',
  border: '1px solid #e5e7eb', borderRadius: 8, background: '#fafafa',
};
const boxLabel = { fontSize: '0.76rem', color: '#6b7280', fontWeight: 700, marginBottom: 6 };
const primaryBtn = {
  padding: '7px 12px', borderRadius: 7, border: 'none', cursor: 'pointer',
  background: '#374151', color: '#fff', fontSize: '0.82rem', fontWeight: 700,
};
const ghostBtn = {
  padding: '7px 12px', borderRadius: 7, border: '1px solid #d1d5db', cursor: 'pointer',
  background: '#fff', color: '#374151', fontSize: '0.82rem', fontWeight: 700,
};
const linkBtn = {
  background: 'none', border: 'none', padding: 0, cursor: 'pointer',
  color: '#4b5563', fontSize: '0.8rem', fontWeight: 700,
};
```

- [ ] **Step 2: `SpeakButton` 의 실제 export 이름과 props 를 확인한다**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && grep -n "export function SpeakButton\|export default" src/Speech.jsx | head -3
```

`SpeakButton` 이 받는 prop 이 `text` 가 아니면 실제 이름에 맞춰 고치고 보고서에 적어라. 없으면 이 줄을 지워라 — TTS 는 필수 요구사항이 아니다.

- [ ] **Step 3: 린트**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run lint 2>&1 | tail -3
```

Expected: `ConceptScene.jsx` 에서 새 에러 없음.

- [ ] **Step 4: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/ConceptScene.jsx
git commit -m "feat(개념완성): 캐릭터 대화 화면

턴을 하나씩 열고 quiz 에서 선택을 강제한다. 오답마다 그 오답 전용
반박이 붙는다. turns 없는 옛 논점은 body 폴백."
```

---

## Task 5: `ConceptOutline.jsx` — 목차 화면

**Files:**
- Create: `viewer/src/ConceptOutline.jsx`

**Interfaces:**
- Consumes: `unitTree.{buildUnitTree, stripUnitPrefix}`, `trackScope.applyScope` (Task 2)
- Produces: `<ConceptOutline leaves scope index progress onPick />` default export

`buildUnitTree(leaves)` 는 `{ divisions, ordinalById, total, multiDiv }` 를 돌려준다. `divisions[].chapters[].sections[].items[]` 구조이고 각 `item` 은 `{ name, no, hier, leaf }` 다. AI 학습이 쓰는 것과 **같은 함수**이므로 순서와 계층이 자동으로 일치한다.

- [ ] **Step 1: 컴포넌트를 작성한다**

`viewer/src/ConceptOutline.jsx`:

```jsx
// 개념 완성 목차 — AI 학습·드릴·문제풀이와 같은 트리를 쓴다.
//
// buildUnitTree 는 세 탭이 공유하는 '단일 목차' 모델이다(unitTree.js 첫 줄).
// 개념 완성만 이걸 안 쓰고 평면 목록을 그리고 있어서 목차가 어긋나 보였다.
import { useMemo, useState } from 'react';
import { ChevronRight, ChevronDown } from 'lucide-react';
import { buildUnitTree, stripUnitPrefix } from './unitTree';
import { applyScope } from './trackScope';
import { STATE } from './trackProgress';

export default function ConceptOutline({ leaves, scope, index, progress, onPick }) {
  const scoped = useMemo(() => applyScope(leaves || [], scope), [leaves, scope]);
  const { divisions, multiDiv } = useMemo(() => buildUnitTree(scoped), [scoped]);
  const [open, setOpen] = useState({});   // 장 단위 접기/펴기

  const counts = (leafId) => {
    const total = index?.[leafId]?.points || 0;
    const rec = (progress || {})[leafId] || {};
    const passed = Object.values(rec).filter((s) => s >= STATE.PASSED).length;
    return { total, passed };
  };

  return (
    <div>
      {divisions.map((div) => (
        <section key={div.name} style={{ marginBottom: 18 }}>
          {multiDiv && (
            <h3 style={{ fontSize: '0.82rem', color: '#6b7280', fontWeight: 700, margin: '0 0 8px' }}>
              {div.name}
            </h3>
          )}
          {div.chapters.map((ch) => {
            const key = div.name + '/' + ch.name;
            const isOpen = open[key] !== false;   // 기본은 펼침
            const chTotals = ch.sections.flatMap((s) => s.items).reduce((acc, it) => {
              const c = counts(it.leaf.id);
              return { total: acc.total + c.total, passed: acc.passed + c.passed };
            }, { total: 0, passed: 0 });
            return (
              <div key={key} style={{ marginBottom: 10 }}>
                <button onClick={() => setOpen((o) => ({ ...o, [key]: !isOpen }))}
                  style={chapterBtn}>
                  {isOpen ? <ChevronDown size={14} color="#9ca3af" /> : <ChevronRight size={14} color="#9ca3af" />}
                  <span style={{ fontSize: '0.7rem', color: '#9ca3af', fontWeight: 700, minWidth: 26 }}>
                    {ch.hier}
                  </span>
                  <span style={{ flex: 1, fontSize: '0.88rem', color: '#111827', textAlign: 'left' }}>
                    {stripUnitPrefix(ch.name)}
                  </span>
                  {chTotals.total > 0 && (
                    <span style={countPill}>{chTotals.passed} / {chTotals.total}</span>
                  )}
                </button>

                {isOpen && ch.sections.map((sec) => (
                  <div key={sec.name} style={{ marginLeft: 18, marginTop: 4 }}>
                    <div style={{ fontSize: '0.76rem', color: '#6b7280', margin: '6px 0 2px' }}>
                      {stripUnitPrefix(sec.name)}
                    </div>
                    {sec.items.map((it) => {
                      const c = counts(it.leaf.id);
                      const empty = c.total === 0;
                      return (
                        <button key={it.leaf.id} onClick={() => !empty && onPick(it.leaf.id)}
                          disabled={empty} style={{ ...itemBtn, opacity: empty ? 0.45 : 1,
                            cursor: empty ? 'default' : 'pointer' }}>
                          <span style={{ flex: 1, fontSize: '0.84rem', color: '#111827', textAlign: 'left' }}>
                            {stripUnitPrefix(it.name)}
                          </span>
                          <span style={countPill}>
                            {empty ? '준비 중' : `${c.passed} / ${c.total}`}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                ))}
              </div>
            );
          })}
        </section>
      ))}
    </div>
  );
}

const chapterBtn = {
  width: '100%', display: 'flex', alignItems: 'center', gap: 6,
  padding: '8px 10px', border: '1px solid #e5e7eb', borderRadius: 8,
  background: '#fff', cursor: 'pointer',
};
const itemBtn = {
  width: '100%', display: 'flex', alignItems: 'center', gap: 8,
  padding: '7px 10px', border: 'none', borderRadius: 6,
  background: 'transparent',
};
const countPill = {
  fontSize: '0.72rem', color: '#6b7280', fontWeight: 700, whiteSpace: 'nowrap',
};
```

- [ ] **Step 2: 린트**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run lint 2>&1 | tail -3
```

- [ ] **Step 3: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/ConceptOutline.jsx
git commit -m "feat(개념완성): buildUnitTree 기반 목차

AI 학습·드릴·문제풀이가 공유하는 단일 목차 모델을 개념 완성도 쓴다.
관마다 통과/전체 논점 수를 목차에서 바로 보인다."
```

---

## Task 6: `ConceptTrack.jsx` 를 셸로 재배선

**Files:**
- Modify: `viewer/src/ConceptTrack.jsx` (전면 개편)

**Interfaces:**
- Consumes: `ConceptOutline` (Task 5), `ConceptScene` (Task 4), `conceptTurns.isPassed` (Task 1), `trackProgress.*`
- Produces: `<ConceptTrack subjectId leaves onOpenDeep />` — props 불변

지금 `ConceptTrack.jsx` 는 목차·장면·진도를 다 들고 있어 318줄이다. 목차와 장면을 뺐으므로 셸로 줄인다.

- [ ] **Step 1: 기존 파일을 읽고 유지할 것을 확인한다**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제" && cat viewer/src/ConceptTrack.jsx
```

**유지할 것:**
- 트랙 JSON fetch (`lectures/track/{unit}.basic.json`) 와 `dead` 플래그 방어
- `_extra:` 접두 처리(선행·총정리 트랙)
- `syncCoverage` — **`leafId.startsWith('_extra:')` 가드를 반드시 유지**. 과목 레벨 트랙은 taxonomy 의 관이 아니라서 `mastery` 에 쓰면 존재하지 않는 단원 코드로 기록이 생긴다.
- `markActiveToday()` 호출

**바뀔 것:**
- `LeafList` 를 `ConceptOutline` 으로 교체
- 논점 렌더를 `ConceptScene` 으로 교체
- `PASSED` 를 찍는 시점: 「이해했어요」 버튼 → `ConceptScene` 의 `onPassed`
- `_index.json` 과 `scope.json` 을 추가로 로드

- [ ] **Step 2: 셸로 다시 쓴다**

핵심 부분만 보인다. 나머지(트랙 fetch, `_extra:` 처리, `syncCoverage`)는 기존 코드를 그대로 옮긴다.

```jsx
  // 목차가 읽을 색인과 범위 규칙. 트랙 파일 18개를 전부 받지 않고 이 둘만 받는다.
  const [index, setIndex] = useState(null);
  const [scope, setScope] = useState(null);
  useEffect(() => {
    let dead = false;
    Promise.all([
      fetch(`${studyBase(subjectId)}lectures/track/_index.json`).then((r) => (r.ok ? r.json() : null)).catch(() => null),
      fetch(`${studyBase(subjectId)}lectures/scope.json`).then((r) => (r.ok ? r.json() : null)).catch(() => null),
    ]).then(([i, s]) => { if (!dead) { setIndex(i); setScope(s); } });
    return () => { dead = true; };
  }, [subjectId]);
```

목차 화면:

```jsx
  if (!leafId) {
    return (
      <div style={{ padding: 16 }}>
        <h2 style={{ fontSize: '1.05rem', margin: '0 0 4px' }}>개념 완성</h2>
        <p style={{ color: '#6b7280', fontSize: '0.84rem', margin: '0 0 14px' }}>
          강의가 다룬 논점을 순서대로 하나씩 익힙니다. 다 비우면 그 관을 마친 것입니다.
        </p>
        {extra.filter((e) => e.kind === 'prereq').map((e) => (
          <ExtraCard key={e.title} entry={e} onPick={() => setLeafId(`_extra:${e.title}`)} />
        ))}
        <ConceptOutline leaves={leaves} scope={scope} index={index}
          progress={progress} onPick={setLeafId} />
        {extra.filter((e) => e.kind === 'review').map((e) => (
          <ExtraCard key={e.title} entry={e} onPick={() => setLeafId(`_extra:${e.title}`)} />
        ))}
      </div>
    );
  }
```

장면 화면 — 논점 렌더를 통째로 `ConceptScene` 에 넘긴다:

```jsx
      {point && (
        <ConceptScene
          point={point}
          onPassed={() => { mark(STATE.PASSED); goNext(); }}
          onAsk={onOpenDeep ? () => onOpenDeep(leafId, point) : null}
        />
      )}
```

`mark(STATE.SEEN)` 은 지금처럼 논점이 열릴 때 찍는다. `onOpenDeep` 이 이제 **두 번째 인자로 논점을 받는다** — Task 8 이 이걸 쓴다.

- [ ] **Step 3: dev 서버로 확인한다**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run dev
```

확인:
1. 「AI 학습」 → 개념 완성에 **장/절/관 계층 목차**가 뜬다(평면 목록이 아니다)
2. **재정학이 목차에 없다**
3. 관마다 `0 / 8` 같은 논점 수가 보이고, 트랙 없는 관은 흐리게 「준비 중」
4. 관을 열면 기존 논점(`body` 만 있는 것)이 폴백으로 정상 표시된다
5. 새로고침해도 진도가 남는다
6. 콘솔 에러 없음

`_index.json` 은 아직 없으므로 3번의 숫자는 전부 0이거나 「준비 중」이 정상이다. Task 9 에서 생성한다. **그 사실을 보고서에 적어라.**

확인 후 dev 서버를 종료한다.

- [ ] **Step 4: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/ConceptTrack.jsx
git commit -m "feat(개념완성): 목차·장면 분리, 셸로 축소

통과 판정을 '이해했어요' 자기 신고에서 quiz 정답으로 옮긴다."
```

---

## Task 7: `split_spans_by_item.py` — 절 안에서 관별 재분배

**Files:**
- Create: `scripts/lectures/split_spans_by_item.py`

**Interfaces:**
- Consumes: `map_notes_to_leaves.{tfidf_vectors, cosine, monotonic_assign}`, `generate_notes.load_leaf_sections`, `_paths.{STUDY, WORK}`
- Produces: `viewer/public/data/study/{과목}/lectures/align_split.json` — `align.json` 과 같은 스키마

**배경.** 지금 정렬은 절 수준까지는 맞지만 한 절 안에서 관을 못 가른다. 그래서 절의 전 구간이 한 관에 몰리고, 같은 절의 다른 관은 빈다. 실제로 「제2관 소득·교차탄력성」이 3강 40.9분을 통째로 받았고 그 안에 가격탄력성 논점이 6개 들어 있는데, 「제1관 수요의 가격탄력성」은 트랙이 없다.

**핵심 원리.** 강의는 교재 순서대로 진행한다 — 뒤로 돌아가지 않는다. 그래서 spans 를 관에 **단조 배정**하면 된다. `monotonic_assign(score_rows, n_leaves)` 이 이미 그 일을 한다(`score_rows[i][j]` = i번째 조각이 j번째 관에 붙을 점수, 반환은 조각별 관 인덱스).

- [ ] **Step 1: 스크립트를 쓴다**

```python
#!/usr/bin/env python3
"""절(節) 안에서 관(關)별로 전사 구간을 다시 나눈다.

정렬(align)은 절 수준까지는 잘 맞지만 한 절 안에서 관을 가르지 못한다. 그래서 절의 전
구간이 한 관에 몰리고 같은 절의 다른 관은 빈다. 실제로 「제2관 소득·교차탄력성」이
3강 40.9분을 통째로 받았고 그 안에 가격탄력성 논점이 6개 들어 있는데, 같은 절의
「제1관 수요의 가격탄력성」은 트랙이 없었다.

강의는 교재 순서대로 진행하므로 구간을 관에 **단조 배정**하면 된다.

산출: lectures/align_split.json — align.json 과 같은 스키마. 원본을 덮어쓰지 않는다.
      결과가 나쁘면 파일만 지우면 원래대로 돌아간다.

사용:
  python3 scripts/lectures/split_spans_by_item.py economics --phase basic
  python3 scripts/lectures/split_spans_by_item.py economics --phase basic --dry-run
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import STUDY, WORK  # noqa: E402
from generate_notes import load_leaf_sections  # noqa: E402
from map_notes_to_leaves import tfidf_vectors, cosine, monotonic_assign  # noqa: E402

# 한 관이 최소 이만큼은 받아야 논점을 뽑을 수 있다. 너무 잘게 쪼개면 오히려 나빠진다.
MIN_SEC_PER_ITEM = 180


def section_key(path):
    """관의 절 식별자 — 세부과목/장/절."""
    return tuple(path[:3])


def load_transcript_text(tdir, lecture_id, start, end):
    f = tdir / ('%s.json' % lecture_id)
    if not f.exists():
        return ''
    tr = json.loads(f.read_text(encoding='utf-8'))
    return ' '.join(s['text'] for s in tr['segments'] if start <= s['start'] < end)


def item_doc(sec):
    """관을 대표하는 문서 — 제목 + 교재 소제목. 본문 전체는 넣지 않는다(길면 희석된다)."""
    parts = list(sec.get('path') or [])[-1:]
    parts += list(sec.get('heads') or [])[:12]
    return ' '.join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--phase', default='basic')
    ap.add_argument('--dry-run', action='store_true', help='파일을 쓰지 않고 결과만 보고')
    args = ap.parse_args()

    base = STUDY / args.subject / 'lectures'
    align = json.loads((base / 'align.json').read_text(encoding='utf-8'))
    sections = load_leaf_sections(args.subject)
    tdir = WORK / 'transcripts' / args.subject

    by_leaf = align['by_leaf']

    # 절 → 그 절에 속한 관들(교재 순서). sections 의 키 순서가 곧 교재 순서다.
    sec_items = defaultdict(list)
    for lid, sec in sections.items():
        sec_items[section_key(sec.get('path') or [])].append(lid)

    moved = 0
    new_by_leaf = {lid: list(v) for lid, v in by_leaf.items()}

    for skey, items in sec_items.items():
        if len(items) < 2:
            continue
        # 이 절에서 spans 를 가진 관들
        holders = [lid for lid in items if by_leaf.get(lid)]
        if len(holders) != 1:
            continue                      # 이미 여러 관에 나뉘어 있으면 건드리지 않는다
        holder = holders[0]
        spans = sorted(by_leaf[holder], key=lambda s: (s.get('no') or 0, s.get('start', 0.0)))
        if len(spans) < len(items):
            continue                      # 조각이 관 수보다 적으면 나눌 수 없다

        docs = [item_doc(sections[lid]) for lid in items]
        texts = [load_transcript_text(tdir, s['lecture_id'], s['start'], s['end']) for s in spans]
        if not any(t.strip() for t in texts):
            continue

        vecs = tfidf_vectors(docs + texts)
        item_vecs, span_vecs = vecs[:len(docs)], vecs[len(docs):]
        rows = [[cosine(sv, iv) for iv in item_vecs] for sv in span_vecs]
        assign = monotonic_assign(rows, len(items))

        # 배정 결과를 관별로 모은다
        buckets = defaultdict(list)
        for sp, j in zip(spans, assign):
            buckets[items[j]].append(sp)

        # 너무 짧게 떨어진 관은 앞 관에 되돌린다 — 3분 미만이면 논점을 못 뽑는다
        ordered = [lid for lid in items if buckets.get(lid)]
        for k, lid in enumerate(ordered):
            secs = sum(s['end'] - s['start'] for s in buckets[lid])
            if secs < MIN_SEC_PER_ITEM and k > 0:
                buckets[ordered[k - 1]].extend(buckets.pop(lid))

        if len(buckets) < 2:
            continue                      # 나눠지지 않았으면 그대로 둔다

        for lid in items:
            new_by_leaf[lid] = buckets.get(lid, [])
        new_by_leaf = {k: v for k, v in new_by_leaf.items() if v or k not in items}
        moved += 1
        print('  %s → 관 %d개로 분배 (%s)' % (skey[-1][:34], len(buckets),
                                            ' / '.join(str(len(buckets[l])) for l in items if buckets.get(l))))

    before = sum(1 for v in by_leaf.values() if v)
    after = sum(1 for v in new_by_leaf.values() if v)
    tot_before = sum(len(v) for v in by_leaf.values())
    tot_after = sum(len(v) for v in new_by_leaf.values())
    print('\n절 %d개 재분배 · 관 커버리지 %d → %d · 조각 %d → %d' %
          (moved, before, after, tot_before, tot_after))
    if tot_before != tot_after:
        sys.exit('❌ 조각 수가 달라졌습니다 — 유실 발생. 저장하지 않습니다.')

    if args.dry_run:
        print('(dry-run — 저장하지 않음)')
        return

    out = dict(align)
    out['by_leaf'] = new_by_leaf
    out['split_from'] = 'align.json'
    (base / 'align_split.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print('저장: %s' % (base / 'align_split.json'))


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: dry-run 으로 돌려 결과를 본다**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
rm -rf scripts/lectures/__pycache__
python3 scripts/lectures/split_spans_by_item.py economics --phase basic --dry-run
```

Expected: 재분배된 절 목록과 `관 커버리지 97 → N`. **조각 수는 반드시 보존**돼야 한다(유실 0). 안 맞으면 스크립트가 스스로 멈춘다.

- [ ] **Step 3: 표본을 눈으로 확인한다**

재분배된 절 중 하나를 골라, 새로 spans 를 받은 관의 전사 앞부분이 그 관 제목과 맞는지 본다:

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제" && python3 - <<'PY'
import json, sys
sys.path.insert(0, 'scripts/lectures')
from _paths import STUDY, WORK
base = STUDY / 'economics/lectures'
a = json.loads((base / 'align_split.json').read_text(encoding='utf-8'))
for lid, spans in a['by_leaf'].items():
    if '가격탄력성' in lid and spans:
        print(lid.split('__')[-1], len(spans), '조각')
        f = WORK / 'transcripts/economics' / ('%s.json' % spans[0]['lecture_id'])
        tr = json.load(open(f))
        s0 = spans[0]
        txt = ' '.join(x['text'] for x in tr['segments'] if s0['start'] <= x['start'] < s0['end'])
        print('  첫 조각:', txt[:220])
PY
```

**판단 기준:** 관 제목이 「가격탄력성」인데 전사가 소득탄력성 얘기로 시작하면 분배가 틀린 것이다. 그러면 저장하지 말고 보고하라.

- [ ] **Step 4: 실제 저장 후 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 scripts/lectures/split_spans_by_item.py economics --phase basic
git add scripts/lectures/split_spans_by_item.py viewer/public/data/study/economics/lectures/align_split.json
git commit -m "feat(강의): 절 안에서 관별 구간 재분배

절 수준까지만 맞던 정렬을, 강의가 교재 순서대로 간다는 성질을 써서
관 단위로 단조 배정한다. align.json 은 덮어쓰지 않는다."
```

---

## Task 8: `build_topic_track.py` — `align_split` 소비 + `turns` 프롬프트 + `_index.json`

**Files:**
- Modify: `scripts/lectures/build_topic_track.py`

**Interfaces:**
- Consumes: Task 7 의 `align_split.json`, Task 2 의 `scope.json`
- Produces: `turns` 를 담은 트랙 JSON, `track/_index.json`

- [ ] **Step 1: `align_split.json` 을 우선 읽게 한다**

`main()` 과 `do_check()` 의 `align.json` 로드 지점을 바꾼다. 있으면 split 을 쓰고 없으면 원본을 쓴다:

```python
def load_align(base):
    """절 안에서 관별로 다시 나눈 결과가 있으면 그걸 쓴다.

    align_split.json 은 되돌릴 수 있게 따로 둔 파일이다 — 지우면 원래 정렬로 돌아간다.
    """
    sp = base / 'align_split.json'
    src = sp if sp.exists() else (base / 'align.json')
    print('  정렬: %s' % src.name)
    return json.loads(src.read_text(encoding='utf-8'))
```

- [ ] **Step 2: `scope.json` 으로 대상 관을 거른다**

`main()` 의 `targets` 계산 뒤에 넣는다:

```python
    # 강의가 없는 세부과목은 생성 대상에서 뺀다. 화면(개념 완성)의 제외 규칙과 같은 파일을 쓴다.
    scope_f = base / 'scope.json'
    if scope_f.exists():
        ex = set(json.loads(scope_f.read_text(encoding='utf-8')).get('exclude_divisions') or [])
        if ex:
            before = len(targets)
            targets = [t for t in targets
                       if not ((sections[t].get('path') or [''])[0] in ex)]
            print('  범위 제외(%s): %d → %d관' % (', '.join(sorted(ex)), before, len(targets)))
```

- [ ] **Step 3: `STYLE` 프롬프트를 대화체로 바꾼다**

기존 `STYLE` 에서 **"교재처럼 단정 서술하세요"** 계열 지시를 `turns` 에 한해 해제하고, 아래를 요구한다. 기존의 다른 규칙(숫자 지어내기 금지, 전사에 없는 결론 채우기 금지, 대칭 구조, viz/steps, 밀도)은 **그대로 둔다.**

프롬프트에 넣을 문구:

```
[출력 — 각 논점은 대화다]
논점 하나를 캐릭터 넷이 주고받는 대화(turns)로 씁니다. turns 는 6~12개.

캐릭터:
- "ask"    묻는 이 — 학습자 대신 묻는다. 짧고 솔직하게. "이거 왜 배워요?" "아까 그거랑 뭐가 달라요?"
- "teach"  선생 — 설명한다. **일상 언어로 먼저 풀고, 비유를 든 다음, 그제서야 교재 표현**을 말한다.
- "gotcha" 깐깐이 — 찌른다. 반례·경계조건·시험 함정. "그럼 이 경우엔요?"
- "mate"   복습 메이트 — 무엇을 외우고 무엇은 넘길지. **내용 설명은 하지 않는다. 학습 조언만.**

[반드시 지킬 것]
- **turns 에 "quiz" 턴이 최소 하나 있어야 합니다.** 없으면 학습자가 그냥 넘겨 버립니다.
- quiz 는 정답 1개, 오답 2~3개입니다.
- **오답은 그럴듯해야 합니다.** 실제로 헷갈리는 것 — 반대 개념(수요 vs 공급), 조건 하나만
  바꾼 것, 방향만 뒤집은 것. 전사에서 함정이라고 경고한 대목이 있으면 그걸 오답으로 쓰세요.
- **오답마다 그 오답 전용 reply 를 씁니다.** "틀렸습니다" 로 시작하지 마세요.
  왜 그렇게 생각했는지 짚고 바로잡으세요. 예: "그건 사는 쪽 얘기예요. 파는 사람
  입장에서 생각해봐요 — 값이 비싸지면 더 팔고 싶겠죠?"
- 정답 choice 에도 reply 를 씁니다(짧게 확인해 주는 말).
- "강사", "강의", "선생님" 이라는 **단어**는 여전히 쓰지 마세요. 캐릭터 「선생」이 말하는
  것이지 누군가를 인용하는 게 아닙니다.
- 과장된 감탄사나 이모티콘을 남발하지 마세요. 친근하되 유치하지 않게.

[출력 형식 — JSON 배열만]
[
  {"title":"…","gist":"…",
   "turns":[
     {"who":"ask","text":"…"},
     {"who":"teach","text":"…","viz":{"template":"supply-demand","params":{},"steps":[]}},
     {"who":"quiz","prompt":"…","choices":[
        {"text":"…","ok":true,"reply":"…"},
        {"text":"…","ok":false,"who":"gotcha","reply":"…"}
     ]},
     {"who":"gotcha","text":"…"},
     {"who":"mate","text":"…"}
   ],
   "example":{"q":"…","solution":"…"},
   "check":{"q":"…","a":"…"},
   "src":[{"lec":12,"t":1390}]}
]
example 은 계산·판단이 있는 논점에만 넣고, 없으면 생략하세요.
```

기존 `body` 필드는 프롬프트에서 더 이상 요구하지 않는다. 대신 **재생성 시 기존 `body` 를 재료로 넣는다** — 이미 검증된 내용이라 처음부터 다시 읽는 것보다 싸다. `gen_leaf` 의 프롬프트 조립부에 추가:

```python
            + (('[이 관의 이전 정리 — 내용 근거로만 쓰고 문장을 그대로 옮기지 마세요]\n%s\n\n'
                % prev_bodies[:6000]) if prev_bodies else '')
```

`prev_bodies` 는 그 관의 기존 트랙에서 `body` 를 이어 붙인 것이다. 없으면 빈 문자열.

- [ ] **Step 4: 저장할 때 `body` 를 보존한다**

`save_leaf` 에서 새 논점에 `body` 가 없고 같은 `id` 의 옛 논점에 있으면 옮겨 담는다. 화면 폴백과 다음 재생성의 재료로 쓰인다.

- [ ] **Step 5: `_index.json` 을 만든다**

저장이 끝날 때마다(또는 `main()` 마지막에) 트랙 디렉터리를 훑어 색인을 쓴다:

```python
def write_index(base, phase):
    """목차 화면이 읽을 색인. 트랙 파일 18개를 전부 받지 않게 하려는 것이다."""
    out = {}
    for f in sorted((base / 'track').glob('*.%s.json' % phase)):
        d = json.loads(f.read_text(encoding='utf-8'))
        for lf in d.get('leaves') or []:
            if not lf.get('leaf_id'):
                continue
            pts = lf.get('points') or []
            src = (pts[0].get('source') if pts else None) or 'lecture'
            out[lf['leaf_id']] = {'points': len(pts), 'source': src}
    (base / 'track' / '_index.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print('색인 %d관 저장' % len(out))
```

`main()` 끝과 `--check` 시작에서 부른다.

- [ ] **Step 6: `--limit 2` 로 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
rm -rf scripts/lectures/__pycache__
python3 scripts/lectures/build_topic_track.py economics --phase basic --limit 2 --force
```

생성된 논점에 `turns` 가 있는지, `quiz` 가 있는지, 오답에 전용 `reply` 가 있는지 **실제 JSON 을 열어 확인하고 보고서에 붙여라.**

- [ ] **Step 7: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add scripts/lectures/build_topic_track.py
git commit -m "feat(강의): 논점을 캐릭터 대화(turns)로 생성

align_split 우선 사용, scope.json 으로 범위 제외, 목차용 _index.json
생성. 기존 body 는 재료로 넣고 보존한다."
```

---

## Task 9: `check_track` 에 대화 검사 추가

**Files:**
- Modify: `scripts/lectures/track_core.py`
- Modify: `scripts/lectures/test_track_core.py`

**Interfaces:**
- Consumes: 없음
- Produces: `check_track` 이 `turns`·`quiz`·오답 `reply`·`who` 를 검사

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`test_track_core.py` 의 `TestCheckTrack` 에 추가한다. 기존 테스트를 약화·삭제하지 말 것.

```python
    def _dlg(self, turns):
        pt = {'seq': 1, 'id': 'M01-L00-p01', 'title': 't', 'gist': 'g',
              'turns': turns, 'viz': None, 'check': None, 'src': []}
        return {'unit_code': 'M01', 'phase': 'basic',
                'leaves': [{'leaf_id': None, 'title': 'T',
                            'points': [pt, dict(pt), dict(pt)]}],
                'orphans': []}

    GOOD_TURNS = [
        {'who': 'ask', 'text': 'a'},
        {'who': 'quiz', 'prompt': 'q', 'choices': [
            {'text': 'A', 'ok': True, 'reply': '맞아요'},
            {'text': 'B', 'ok': False, 'reply': '그건 반대쪽 얘기예요'},
        ]},
        {'who': 'mate', 'text': 'm'},
    ]

    def test_good_dialogue_has_no_issues(self):
        self.assertEqual(check_track(self._dlg(self.GOOD_TURNS), {}, set()), [])

    def test_missing_quiz_reported(self):
        turns = [{'who': 'teach', 'text': 'a'}, {'who': 'mate', 'text': 'b'}]
        issues = check_track(self._dlg(turns), {}, set())
        self.assertTrue(any('quiz' in i for i in issues))

    def test_no_correct_choice_reported(self):
        turns = [{'who': 'quiz', 'prompt': 'q', 'choices': [
            {'text': 'A', 'ok': False, 'reply': 'x'},
            {'text': 'B', 'ok': False, 'reply': 'y'}]}]
        self.assertTrue(any('정답' in i for i in check_track(self._dlg(turns), {}, set())))

    def test_two_correct_choices_reported(self):
        turns = [{'who': 'quiz', 'prompt': 'q', 'choices': [
            {'text': 'A', 'ok': True, 'reply': 'x'},
            {'text': 'B', 'ok': True, 'reply': 'y'}]}]
        self.assertTrue(any('정답' in i for i in check_track(self._dlg(turns), {}, set())))

    def test_wrong_choice_without_reply_reported(self):
        turns = [{'who': 'quiz', 'prompt': 'q', 'choices': [
            {'text': 'A', 'ok': True, 'reply': 'x'},
            {'text': 'B', 'ok': False, 'reply': ''}]}]
        self.assertTrue(any('반박' in i for i in check_track(self._dlg(turns), {}, set())))

    def test_generic_reply_reported(self):
        """'틀렸습니다' 류는 그 오답 전용 반박이 아니다 — 이걸 허용하면 규칙이 무의미해진다."""
        turns = [{'who': 'quiz', 'prompt': 'q', 'choices': [
            {'text': 'A', 'ok': True, 'reply': 'x'},
            {'text': 'B', 'ok': False, 'reply': '틀렸습니다.'}]}]
        self.assertTrue(any('반박' in i for i in check_track(self._dlg(turns), {}, set())))

    def test_unknown_who_reported(self):
        turns = [{'who': 'narrator', 'text': 'a'}] + self.GOOD_TURNS
        self.assertTrue(any('who' in i for i in check_track(self._dlg(turns), {}, set())))

    def test_turn_count_out_of_range_reported(self):
        turns = [{'who': 'teach', 'text': 'a'}] * 20 + self.GOOD_TURNS
        self.assertTrue(any('턴' in i for i in check_track(self._dlg(turns), {}, set())))

    def test_legacy_body_only_point_reported_as_stale(self):
        """turns 가 없는 옛 논점은 결함이 아니라 '미갱신' 으로 보고한다."""
        pt = {'seq': 1, 'id': 'x', 'title': 't', 'gist': 'g', 'body': 'b', 'src': []}
        t = {'unit_code': 'M01', 'phase': 'basic',
             'leaves': [{'leaf_id': None, 'title': 'T', 'points': [pt, dict(pt), dict(pt)]}],
             'orphans': []}
        self.assertTrue(any('미갱신' in i for i in check_track(t, {}, set())))
```

- [ ] **Step 2: 테스트가 실패하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/scripts/lectures" && python3 -m unittest test_track_core -v 2>&1 | tail -5
```

Expected: 새 테스트 9개 실패

- [ ] **Step 3: `check_track` 에 검사를 더한다**

`track_core.py` 상단에 상수를 추가하고:

```python
WHO_VALUES = ('ask', 'teach', 'gotcha', 'mate', 'quiz')
MIN_TURNS = 3
MAX_TURNS = 14
# 오답 반박이 이 문구로 시작하면 "그 오답 전용" 이 아니다. 규칙을 무의미하게 만드는 형태다.
GENERIC_REPLIES = ('틀렸', '오답', '아닙니다', '아니에요', '다시 생각')
```

`check_track` 의 논점 순회 안에 넣는다(기존 앵커·템플릿·논점 수 검사는 그대로):

```python
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
```

- [ ] **Step 4: 테스트가 통과하는 것을 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/scripts/lectures" && python3 -m unittest test_track_core 2>&1 | tail -3
```

Expected: 기존 29 + 새 9 = 38 OK

- [ ] **Step 5: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add scripts/lectures/track_core.py scripts/lectures/test_track_core.py
git commit -m "feat(강의): --check 에 대화 검사 추가

quiz 유무, 정답 1개, 오답 2개 이상, 오답별 전용 반박, who 값,
턴 수 범위. turns 없는 옛 논점은 '미갱신' 으로 구분해 보고한다."
```

---

## Task 10: 표본 30관 생성 + 사람 검토 관문

**Files:**
- Create: `viewer/public/data/study/economics/lectures/track/*.basic.json` (일부 갱신)

**Interfaces:**
- Consumes: Task 7·8·9
- Produces: 품질 판단 (전량 생성 여부를 가르는 관문)

**이 관문이 필요한 이유.** `--check` 는 오답이 **뻔한지** 를 잡지 못한다. 형식은 다 맞는데 아무도 안 틀리는 선택지만 나오면 이 설계의 목적이 통째로 무너진다. 캐릭터 말투가 유치한지도 기계로는 못 본다.

- [ ] **Step 1: 30관을 생성한다**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 scripts/lectures/build_topic_track.py economics --phase basic --limit 30 --force
```

- [ ] **Step 2: 검사기를 돌린다**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 scripts/lectures/build_topic_track.py economics --phase basic --check 2>&1 | tail -20
```

Expected: 새 대화 관련 문제 0건. 나오면 프롬프트를 고치고 그 관만 `--force --only` 로 재생성한다.

- [ ] **Step 3: 표본 20논점을 실제로 읽는다**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제" && python3 - <<'PY'
import json, glob, itertools
pts = []
for f in sorted(glob.glob('viewer/public/data/study/economics/lectures/track/*.basic.json')):
    d = json.load(open(f))
    for lf in d['leaves']:
        for p in lf['points']:
            if p.get('turns'):
                pts.append((lf['title'], p))
for title, p in pts[:20]:
    print('\n' + '=' * 70)
    print('%s — [%s] %s' % (title[:24], p['seq'], p['title']))
    for t in p['turns']:
        if t['who'] == 'quiz':
            print('  [quiz] %s' % t['prompt'])
            for c in t['choices']:
                print('     %s %s → %s' % ('O' if c.get('ok') else 'X', c['text'], c['reply'][:70]))
        else:
            print('  %-7s %s' % (t['who'], (t.get('text') or '')[:90]))
PY
```

**다음 넷을 판단하고 보고서에 근거와 함께 적어라. 인상평은 쓸모없다 — 구체적인 논점을 짚어라.**

1. **오답이 그럴듯한가.** 학습자가 실제로 헷갈릴 만한가, 아니면 누가 봐도 아닌가? 뻔한 오답이 20논점 중 몇 개인가?
2. **반박이 그 오답 전용인가.** "왜 그렇게 생각했는지" 를 짚는가, 아니면 정답을 다시 말할 뿐인가?
3. **말투가 유치하지 않은가.** 감탄사·이모티콘 남발, 과한 친근함.
4. **「선생」이 일상 언어 → 비유 → 교재 표현 순서를 지키는가.** 아니면 여전히 교과서 문장으로 시작하는가?

문제가 있으면 프롬프트를 고치고 30관을 다시 만든 뒤 **다시 읽어라.** 이 관문을 통과하기 전에 전량 생성으로 넘어가지 마라.

- [ ] **Step 4: 통과하면 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/public/data/study/economics/lectures/track scripts/lectures/build_topic_track.py
git commit -m "feat(강의): 대화형 논점 표본 30관"
```

---

## Task 11: 전량 생성 (160관 범위)

**Files:**
- Modify: `viewer/public/data/study/economics/lectures/track/*.basic.json`

- [ ] **Step 1: 전량 생성**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 scripts/lectures/build_topic_track.py economics --phase basic --force
```

`--force` 를 쓰는 이유: 기존 논점은 `body` 만 있어 건너뛰기 판정에 걸린다. 전부 대화로 갈아야 한다.

3~5시간, 출력 150만~250만 토큰으로 추정한다. 증분 저장이 있으므로 중단·재개가 싸다. **30관쯤 진행됐을 때 실제 토큰을 재서 추정을 갱신하고 보고서에 적어라.**

- [ ] **Step 2: 검사**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
python3 scripts/lectures/build_topic_track.py economics --phase basic --check 2>&1 | tail -20
```

확인: ① 대화 관련 문제 0건 ② "미갱신" 0건 ③ 목차 범위 안에 트랙 없는 관 0건

- [ ] **Step 3: 통계를 낸다**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제" && python3 - <<'PY'
import json, glob, collections
tot = quiz = viz = steps = 0
leaves = 0
who = collections.Counter()
for f in glob.glob('viewer/public/data/study/economics/lectures/track/*.basic.json'):
    d = json.load(open(f))
    for lf in d['leaves']:
        leaves += 1
        for p in lf['points']:
            tot += 1
            for t in p.get('turns') or []:
                who[t.get('who')] += 1
                if t.get('who') == 'quiz':
                    quiz += 1
                if t.get('viz'):
                    viz += 1
                    if t['viz'].get('steps'): steps += 1
print('관 %d · 논점 %d · quiz %d · viz %d · steps %d' % (leaves, tot, quiz, viz, steps))
print('화자 분포:', dict(who))
PY
```

- [ ] **Step 4: 커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/public/data/study/economics/lectures/track
git commit -m "feat(강의): 경제학 대화형 논점 전량 생성"
```

---

## Task 12: 「더 묻기」에 논점 컨텍스트 싣기

**Files:**
- Modify: `viewer/src/App.jsx` (`concept` 뷰 분기의 `onOpenDeep`)
- Modify: `viewer/src/AILearning.jsx` (딥링크 힌트 소비)

**Interfaces:**
- Consumes: Task 6 의 `onOpenDeep(leafId, point)`
- Produces: 「더 묻기」가 그 관·그 논점으로 AI 학습을 연다

스펙 §5-3 의 "「더 묻기」는 그 논점의 `turns` 를 system 블록에 실어 기존 대화 엔진을 부른다" 를 구현한다. 1차 설계에서 콜백만 있고 컨텍스트가 안 실렸던 미구현분이다.

- [ ] **Step 1: 기존 딥링크 통로를 읽는다**

이미 커리큘럼용 딥링크가 있고 **키는 `ailearn-jump`** 다. `App.jsx:2169` 가 저장하고 `AILearning.jsx:1649` 가 mount 시 1회 소비한 뒤 지운다. 지금 형태는 `{ mode, docTab, ts }` 뿐이다.

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제" && sed -n '2169,2176p' viewer/src/App.jsx && sed -n '1649,1672p' viewer/src/AILearning.jsx
```

**같은 통로를 넓혀 쓴다.** 새 키를 만들지 마라 — 두 통로가 생기면 어느 쪽이 이겼는지 알 수 없게 된다.

- [ ] **Step 2: `onOpenDeep` 이 `ailearn-jump` 에 관·논점을 실어 남기게 한다**

`App.jsx` 의 `concept` 뷰 분기:

```jsx
        onOpenDeep={(leafId, point) => {
          // 커리큘럼이 쓰는 것과 같은 통로(ailearn-jump). 기존 필드(mode·docTab·ts)를
          // 유지한 채 leaf_id 와 seed 를 더한다 — 소비 쪽이 없는 필드는 무시한다.
          try {
            localStorage.setItem('ailearn-jump', JSON.stringify({
              mode: 'study', docTab: null, ts: Date.now(),
              subject: subj, leaf_id: leafId,
              seed: point ? {
                title: point.title,
                turns: (point.turns || []).map((t) => t.text || t.prompt).filter(Boolean).join('\n'),
              } : null,
            }));
          } catch { /* 용량 초과 무시 */ }
          setCurrentView('civil');
        }}
```

`Date.now()` 는 기존 코드가 이미 쓰고 있으므로 그대로 둔다.

- [ ] **Step 3: `AILearning` 이 `leaf_id` 로 관을 열고 `seed` 를 싣게 한다**

`AILearning.jsx:1649` 의 딥링크 소비 `useEffect` 를 넓힌다. 지금은 `j.mode` 와 `j.docTab` 만 본다.

```js
    // 개념 완성에서 넘어온 경우 — 그 관을 열고, 방금 본 논점을 기억해 둔다.
    if (j.leaf_id) setCurrent({ subject: j.subject || subjectId, leaf_id: j.leaf_id });
    if (j.seed) setDeepSeed(j.seed);
```

`setCurrent` 는 이 파일이 이미 import 하고 있다(`aiLearningStore` 에서). `deepSeed` 는 새 state 로 만든다.

그리고 system 블록을 조립하는 지점에서 `deepSeed` 가 있으면 **맨 뒤에** 붙인다:

```js
// 학생이 방금 개념 완성에서 본 논점. 이걸 알고 이어서 답해야 같은 설명을 반복하지 않는다.
const seedBlock = deepSeed
  ? `\n\n[학생이 방금 본 논점]\n${deepSeed.title}\n${deepSeed.turns}`
  : '';
```

**프롬프트 캐싱을 깨지 않도록 `cache_control` 이 붙은 블록보다 뒤에 놓아라.** 앞에 끼우면 캐시가 매번 무효화되어 토큰이 그대로 다시 든다(`aiClaudeClient.js` 첫 주석이 이 캐싱을 설명한다). `buildSystemBlocks` 의 반환 배열을 확인하고 캐시 블록 뒤에 새 블록으로 추가하라.

한 번 쓰고 나면 `deepSeed` 를 비운다 — 다음 질문마다 계속 실리면 맥락이 아니라 잡음이 된다.

- [ ] **Step 4: dev 서버로 확인**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run dev
```

확인: 개념 완성에서 논점을 열고 「이 논점 더 묻기」 → AI 학습으로 넘어가며 **그 관이 선택돼 있다.** API 키가 있으면 첫 질문에 그 논점 맥락이 반영되는지 본다. 키가 없으면 관 선택까지만 확인하고 보고서에 그렇게 적어라.

- [ ] **Step 5: 린트·빌드·커밋**

```bash
cd "/Users/hanjiho/Documents/감정평가사 기출문제/viewer" && npm run lint && npm run build
cd "/Users/hanjiho/Documents/감정평가사 기출문제"
git add viewer/src/App.jsx viewer/src/AILearning.jsx
git commit -m "feat(개념완성): 더 묻기에 논점 맥락 전달

커리큘럼이 쓰는 기존 딥링크 통로를 그대로 쓴다."
```

---

## Self-Review

**스펙 커버리지**

| 스펙 절 | 담당 태스크 |
|---|---|
| §4-1 buildUnitTree 재사용 | Task 5 |
| §4-1 `_index.json` | Task 8 Step 5, Task 6 |
| §4-2 재정학 제외 / `scope.json` | Task 2, Task 8 Step 2 |
| §4-3 절 내 2차 분배 | Task 7 |
| §4-4 남는 관 교재 생성 | Task 7 이후 남는 관에 `source: "textbook"` — **Task 11 의 전량 생성이 처리** |
| §5-1 `turns` 스키마 | Task 8 Step 3 |
| §5-1 `body` 폴백·보존 | Task 4 (화면), Task 8 Step 4 (저장) |
| §5-2 캐릭터 넷 | Task 3 (톤), Task 4 (`CAST`), Task 8 (프롬프트) |
| §5-3 턴 하나씩·선택 강제·2회 오답 공개 | Task 1, Task 4 |
| §5-3 통과 판정 = quiz 정답 | Task 1 `isPassed`, Task 6 |
| §5-3 TTS | Task 4 Step 2 |
| §5-3 「더 묻기」 | Task 12 |
| §6-1 문체 전환 | Task 8 Step 3 |
| §6-2 오답 품질 지시 | Task 8 Step 3 |
| §7 진도·coverage 불변 | 어느 태스크도 `trackProgress.js` 를 건드리지 않는다 |
| §8 검증 1~6 | Task 9 (1~5), Task 8 Step 2 + Task 11 Step 2 (6) |
| §8 턴 상태 기계 테스트 | Task 1 |
| §10 오답이 뻔한 위험 | Task 10 (사람 검토 관문) |

**§4-4 보충.** 절 전체가 비어 2차 분배로도 안 채워지는 관은 Task 7 실행 뒤에 확정된다(스펙이 "하드코딩하지 않고 분배 뒤에 계산" 이라고 정했다). Task 11 의 전량 생성에서 그 관들은 전사가 없으므로 `bundle['lectures']` 가 비어 건너뛰어진다. **Task 11 Step 2 의 "목차 범위 안에 트랙 없는 관 0건" 검사가 이걸 잡는다.** 잡히면 그 관 목록으로 교재 기반 생성을 한 번 더 돌린다 — 목록이 실행 전에는 정해지지 않으므로 계획에 고정된 명령을 적을 수 없다. Task 11 Step 2 에서 목록을 확인한 뒤 `--only` 로 처리하고, `source: "textbook"` 이 붙는지 확인하라.

**타입 일관성 확인**

- `WHO` 값 `ask/teach/gotcha/mate/quiz` — Task 1 정의, Task 4 `CAST`, Task 8 프롬프트, Task 9 `WHO_VALUES` 가 모두 같은 문자열.
- `choose(point, state, turnIndex, choiceIndex)` — Task 1 정의, Task 4 `pick` 이 같은 인자 순서.
- `applyScope(leaves, scope)` — Task 2 정의, Task 5 사용.
- `onOpenDeep(leafId, point)` — Task 6 이 두 인자로 부르고, Task 12 가 두 인자로 받는다.
- `_index.json` 형태 `{leafId: {points, source}}` — Task 8 생성, Task 5 `counts()` 소비.
- `STATE.PASSED` — `trackProgress.js` 의 기존 값. Task 5·6 이 읽기만 한다.
