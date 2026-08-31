# AI 학습 3탭 구현 계획 ① — 시스템

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 관 하나에 개념 완성·기출 분석·심화 세 탭을 세우고, 세 탭이 같은 렌더러를 쓰며, 학습 중 아무 때나 끼어들어 묻고 그 자리로 돌아올 수 있게 한다.

**Architecture:** `ConceptScene` 이 `turns` 스키마를 그리는 유일한 렌더러가 된다. 탭은 어떤 트랙 파일을 물리느냐만 다르다(`{unit}.basic.json` / `{unit}.exam.json` / 없음). 순수 로직(샛길 상태·검색·프롬프트 조립·약점 산출)은 `.js` 로 빼서 `node --test` 로 검증하고, JSX 는 브라우저에서 눈으로 확인한다.

**Tech Stack:** React 19 · Vite 8 · 순수 CSS(토큰) · `node --test` · Python 3.9(시스템 파이썬 — `match` 문과 `X | Y` 타입 표기 금지)

**Spec:** [`docs/superpowers/specs/2026-09-01-ai-learning-three-tracks-design.md`](../specs/2026-09-01-ai-learning-three-tracks-design.md)

**범위:** 스펙 §11 의 1~7단계. **8단계(기출 720문항 저작)는 이 계획에 없다** — 이 계획이 끝나 `{unit}.exam.json` 을 실제로 읽는 화면이 선 뒤에 계획 ②로 따로 쓴다. 그래야 저작 형식을 화면에 대고 확정할 수 있다.

## Global Constraints

- **학습 활동은 전부 `viewer/src/measure/record.js` 의 `record()` 를 거친다.** 자기만의 localStorage 키를 새로 만들지 않는다. `f`(recog/recall/produce/write) · `g`(machine/ai/human/self/none) · `axis`(knowledge/performance) 셋은 필수다. 빠뜨리면 개발 빌드에서 throw 한다. (CLAUDE.md §0)
- **무게·상한·반감기 같은 튜닝 값은 `viewer/src/measure/tables.js` 에만 둔다.**
- **색은 정해진 뜻만 쓴다.** 파랑 `--accent` = 선택·현재 위치·기본 동작·**샛길**. 노랑 `--hl-formula` = 외울 공식·정의. 보라 `--hl-flip` = 시험이 뒤집는 자리. 빨강 `--wrong` = 오답·약점. **초록은 쓰지 않는다.**
- **강조는 한 화면에 세 곳까지.** 한 말풍선에 형광펜 하나, 강조는 통틀어 둘까지(`emphasis.js`).
- **열 정렬:** 말풍선·그림 카드·선택지·버튼·입력창이 모두 `min(100%, 560px)` 로 같은 세로선에 선다.
- **빈 값은 자리를 비운다.** `—` 로 채우지 않는다.
- **아이콘은 선화, 배경 없음, `--ink-2`, 20px.** lucide 만 쓰고 이모지는 쓰지 않는다.
- **진행 바는 트랙 하나에 채움 하나.** 구간으로 나누지 않는다.
- **API 제공자 셋(anthropic·openai·google)을 그대로 지원한다.** 하나로 좁히지 않는다.
- **키 없이도 개념 완성과 기출 분석은 끝까지 진행된다.** 키는 심화와 끼어들기만 막는다.
- **Figma 시안이 정본이다**(DECISIONS.md 2026-08-31). 시안과 코드가 어긋나면 시안을 따른다.

---

## 파일 구조

**새로 만드는 것**

| 파일 | 책임 |
|---|---|
| `viewer/src/sideThread.js` | 샛길(끼어들기) 상태·저장. 순수 함수 |
| `viewer/src/sideThread.test.js` | 위 테스트 |
| `viewer/src/rag/search.js` | 청크 키워드 검색. 순수 함수 |
| `viewer/src/rag/search.test.js` | 위 테스트 |
| `viewer/src/rag/context.js` | 프롬프트 블록 조립 + 예산 상한. 순수 함수 |
| `viewer/src/rag/context.test.js` | 위 테스트 |
| `viewer/src/weakSpots.js` | 심화 탭 약점 카드 산출. 순수 함수 |
| `viewer/src/weakSpots.test.js` | 위 테스트 |
| `viewer/src/ConceptTabs.jsx` | 관 안의 상단 3탭 |
| `viewer/src/DeepChat.jsx` | 심화 탭 — 약점 카드 + 자유 대화 + 키 없을 때 |
| `viewer/src/TextbookPanel.jsx` | 4단째 교재 패널 |
| `scripts/lectures/build_rag_chunks.py` | 교재 md → 청크 JSON |
| `scripts/lectures/test_build_rag_chunks.py` | 위 테스트 |
| `scripts/lectures/merge_mnemonics.py` | 암기법 → 복습 메이트 턴 |

**고치는 것**

| 파일 | 무엇을 |
|---|---|
| `viewer/src/ConceptTrack.jsx` | 탭 상태, 트랙 파일 분기, 교재 패널 토글 |
| `viewer/src/ConceptScene.jsx` | OX 도크, 서술 인출 도크, 샛길 렌더, 기출 딥링크 카드 |
| `viewer/src/conceptTurns.js` | `ox`·`recall` 턴 종류 |
| `viewer/src/App.jsx` | `ConceptTrack` 에 prop 추가 |
| `viewer/src/index.css` | 새 클래스 |
| `viewer/scripts/sync-data.mjs` | `rag/` 디렉터리 복사 |

---

## Task 1: 상단 3탭과 트랙 분기

**Files:**
- Create: `viewer/src/ConceptTabs.jsx`
- Modify: `viewer/src/ConceptTrack.jsx`
- Modify: `viewer/src/index.css`

**Interfaces:**
- Consumes: 없음 (첫 태스크)
- Produces: `ConceptTrack` 이 내부 state `tab` 을 갖는다 — 값은 `'concept' | 'exam' | 'deep'`. 트랙 fetch 경로가 `tab` 에 따라 갈린다.

- [ ] **Step 1: `ConceptTabs.jsx` 를 만든다**

```jsx
// 관 안의 상단 3탭 — 시안 316:3 의 tabs.
// 탭 전환은 관을 벗어나지 않는다. 같은 관의 다른 트랙으로 갈아 끼울 뿐이다.
export const TABS = [
  { key: 'concept', label: '개념 완성' },
  { key: 'exam', label: '기출 분석' },
  { key: 'deep', label: '심화' },
];

export default function ConceptTabs({ tab, onPick, right }) {
  return (
    <div className="ctabs" role="tablist" aria-label="학습 방식">
      {TABS.map((t) => (
        <button type="button" key={t.key} role="tab"
          aria-selected={tab === t.key}
          className={`ctab${tab === t.key ? ' is-on' : ''}`}
          onClick={() => onPick(t.key)}>
          {t.label}
        </button>
      ))}
      {right && <span className="ctabs-right">{right}</span>}
    </div>
  );
}
```

- [ ] **Step 2: CSS 를 넣는다**

`viewer/src/index.css` 끝에 붙인다.

```css
/* ── 관 안의 상단 3탭 — 시안 316:3 ────────────────────────── */
.ctabs {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  flex: 0 0 auto;
  padding: 0 var(--space-4);
  background: var(--sheet);
  border-bottom: 1px solid var(--line);
}
.ctab {
  padding: 14px 2px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  font: inherit;
  font-size: var(--text-sm);
  color: var(--ink-meta);
  cursor: pointer;
}
.ctab:hover { color: var(--ink-2); }
.ctab.is-on {
  color: var(--ink);
  font-weight: var(--weight-bold);
  border-bottom-color: var(--accent);
}
.ctabs-right {
  margin-left: auto;
  font-size: var(--text-xs);
  color: var(--ink-meta);
  font-variant-numeric: tabular-nums;
}
```

- [ ] **Step 3: `ConceptTrack.jsx` 에 탭 상태를 넣는다**

`import ConceptTree from './ConceptTree';` 아래에 추가:

```jsx
import ConceptTabs from './ConceptTabs';
```

`const [summary, setSummary] = useState(false);` 아래에 추가:

```jsx
  // 'concept' 개념 완성 · 'exam' 기출 분석 · 'deep' 심화.
  // 관을 옮겨도 탭은 유지한다 — 기출을 보던 사람은 다음 관에서도 기출부터 본다.
  const [tab, setTab] = useState('concept');
```

- [ ] **Step 4: 트랙 fetch 를 탭별로 가른다**

`ConceptTrack.jsx` 의 트랙 로드 `useEffect` 안에서 이 줄을 찾는다.

```jsx
    fetch(`${studyBase(subjectId)}lectures/track/${leaf.unit_code}.basic.json`)
```

이렇게 바꾼다.

```jsx
    // 개념은 basic, 기출은 exam. 심화는 트랙이 없다(DeepChat 이 맡는다).
    const suffix = tab === 'exam' ? 'exam' : 'basic';
    fetch(`${studyBase(subjectId)}lectures/track/${leaf.unit_code}.${suffix}.json`)
```

같은 `useEffect` 의 의존성 배열에 `tab` 을 더한다.

```jsx
  }, [subjectId, leaf?.unit_code, leafId, extra, tab]);
```

- [ ] **Step 5: 헤더 위에 탭을 그린다**

`ConceptTrack.jsx` 의 `workspace` 헬퍼 안, `{inner}` 앞에 넣지 말고 **`inner` 를 감싸는 쪽**에 넣는다. `return workspace(` 로 시작하는 마지막 렌더의 `<div className="concept-runner">` 바로 다음 줄에 추가:

```jsx
      <ConceptTabs tab={tab} onPick={setTab}
        right={tab === 'exam' && counts.total ? `기출 ${counts.passed} / ${counts.total}` : null} />
```

- [ ] **Step 6: 브라우저에서 확인**

```bash
cd viewer && npm run dev
```

`http://localhost:5173/#/subject/concept/-/-/-/-/-` 에서 아무 관이나 연다.
확인할 것: 탭 셋이 보인다 · 「개념 완성」이 파란 밑줄로 선택돼 있다 · 「기출 분석」을 누르면 트랙이 없어 「이 단원은 아직 논점 트랙이 없습니다」가 뜬다 · 다시 「개념 완성」을 누르면 원래 대화로 돌아온다.

- [ ] **Step 7: 커밋**

```bash
git add viewer/src/ConceptTabs.jsx viewer/src/ConceptTrack.jsx viewer/src/index.css
git commit -m "feat(AI 학습): 관 안에 상단 3탭 — 개념 완성·기출 분석·심화"
```

---

## Task 2: 기출 트랙이 없을 때의 안내

**Files:**
- Modify: `viewer/src/ConceptTrack.jsx`

**Interfaces:**
- Consumes: Task 1 의 `tab` state
- Produces: 없음

Task 1 을 끝내면 기출 탭에서 「논점 트랙이 없습니다」라는 개념 완성용 문구가 뜬다. 기출 탭에는 맞지 않는 말이다.

- [ ] **Step 1: 트랙 없음 화면을 탭별로 가른다**

`ConceptTrack.jsx` 에서 `if (!track) {` 블록의 `<p className="concept-index-lede" ...>` 를 찾아 이렇게 바꾼다.

```jsx
        <p className="concept-index-lede" style={{ marginTop: 14 }}>
          {tab === 'exam'
            ? '이 관의 기출 분석은 아직 준비되지 않았습니다. 개념 완성부터 익혀 두세요.'
            : '이 단원은 아직 논점 트랙이 없습니다. 강의가 다루지 않은 범위이거나 아직 생성 전입니다.'}
        </p>
```

- [ ] **Step 2: 개념으로 돌아가는 버튼을 준다**

같은 블록의 `{onOpenDeep && (` 조건 앞에 추가한다.

```jsx
        {tab === 'exam' && (
          <button type="button" className="concept-op" onClick={() => setTab('concept')}>
            개념 완성으로 →
          </button>
        )}
```

- [ ] **Step 3: 브라우저에서 확인**

기출 탭에서 안내 문구가 바뀌고 「개념 완성으로 →」가 동작하는지 본다.

- [ ] **Step 4: 커밋**

```bash
git add viewer/src/ConceptTrack.jsx
git commit -m "feat(기출 분석): 트랙이 없을 때의 안내를 탭에 맞게"
```

---

## Task 3: 샛길 상태 기계

**Files:**
- Create: `viewer/src/sideThread.js`
- Create: `viewer/src/sideThread.test.js`

**Interfaces:**
- Consumes: 없음
- Produces:
  - `sideKey(leafId, pointId) -> string`
  - `loadSide(leafId, pointId) -> Array<{who:'me'|'ai', text:string, ts:number}>`
  - `appendSide(leafId, pointId, msg) -> Array` (저장 후 새 배열을 돌려준다)
  - `clearSide(leafId, pointId) -> void`
  - `sideCount(leafId, pointId) -> number`
  - `SIDE_MAX = 40`

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`viewer/src/sideThread.test.js`:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { sideKey, loadSide, appendSide, clearSide, sideCount, SIDE_MAX } from './sideThread.js';

// node 에는 localStorage 가 없다. 최소 구현을 심는다.
function fakeStorage() {
  const m = new Map();
  return {
    getItem: (k) => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => m.set(k, String(v)),
    removeItem: (k) => m.delete(k),
  };
}
test.beforeEach(() => { globalThis.localStorage = fakeStorage(); });

test('키는 관과 논점을 함께 담는다 — 심화 탭의 관 단위 키와 겹치지 않는다', () => {
  assert.equal(sideKey('leaf-1', 'p-3'), 'ailearn-side:leaf-1:p-3');
});

test('아무것도 없으면 빈 배열', () => {
  assert.deepEqual(loadSide('leaf-1', 'p-3'), []);
  assert.equal(sideCount('leaf-1', 'p-3'), 0);
});

test('붙이면 쌓이고 다시 읽힌다', () => {
  appendSide('leaf-1', 'p-3', { who: 'me', text: '왜요?', ts: 1 });
  const after = appendSide('leaf-1', 'p-3', { who: 'ai', text: '이래서요', ts: 2 });
  assert.equal(after.length, 2);
  assert.deepEqual(loadSide('leaf-1', 'p-3').map((m) => m.who), ['me', 'ai']);
  assert.equal(sideCount('leaf-1', 'p-3'), 2);
});

test('논점이 다르면 따로 쌓인다', () => {
  appendSide('leaf-1', 'p-3', { who: 'me', text: 'A', ts: 1 });
  appendSide('leaf-1', 'p-4', { who: 'me', text: 'B', ts: 2 });
  assert.equal(sideCount('leaf-1', 'p-3'), 1);
  assert.equal(sideCount('leaf-1', 'p-4'), 1);
});

test('상한을 넘으면 오래된 것부터 버린다', () => {
  for (let i = 0; i < SIDE_MAX + 5; i += 1) {
    appendSide('leaf-1', 'p-3', { who: 'me', text: `m${i}`, ts: i });
  }
  const all = loadSide('leaf-1', 'p-3');
  assert.equal(all.length, SIDE_MAX);
  assert.equal(all[0].text, 'm5', '오래된 다섯이 밀려나야 한다');
});

test('지우면 비워진다', () => {
  appendSide('leaf-1', 'p-3', { who: 'me', text: 'A', ts: 1 });
  clearSide('leaf-1', 'p-3');
  assert.deepEqual(loadSide('leaf-1', 'p-3'), []);
});

test('저장소가 깨져 있어도 던지지 않는다', () => {
  localStorage.setItem(sideKey('leaf-1', 'p-3'), '{망가진 json');
  assert.deepEqual(loadSide('leaf-1', 'p-3'), []);
});
```

- [ ] **Step 2: 테스트가 실패하는지 본다**

```bash
cd viewer && node --test src/sideThread.test.js
```

Expected: FAIL — `Cannot find module './sideThread.js'`

- [ ] **Step 3: 구현한다**

`viewer/src/sideThread.js`:

```js
// 샛길 — 학습 중 끼어들어 물은 대화. 논점 하나에 하나씩 붙는다.
//
// 심화 탭의 관 단위 대화(`ailearn-room:{leafId}`)와 **다른 키를 쓴다**.
// 논점에 붙은 즉문즉답과 관 전체를 놓고 하는 대화는 다시 열었을 때 보여야 할 것이
// 다르다. 같은 키에 담으면 논점 A 에서 물은 것이 논점 B 에도 뜬다.
//
// 트랙 상태(conceptTurns 의 cursor)는 여기서 건드리지 않는다 — 그래야 돌아갈 자리가
// 정확하다. 이 파일은 대화만 들고 있다.

/** 한 논점에 남길 최대 메시지 수. 넘으면 오래된 것부터 버린다. */
export const SIDE_MAX = 40;

export const sideKey = (leafId, pointId) => `ailearn-side:${leafId}:${pointId}`;

export function loadSide(leafId, pointId) {
  try {
    const raw = localStorage.getItem(sideKey(leafId, pointId));
    const arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch {
    // 저장소가 깨졌다고 학습을 멈출 이유는 없다.
    return [];
  }
}

export function appendSide(leafId, pointId, msg) {
  const next = loadSide(leafId, pointId).concat(msg).slice(-SIDE_MAX);
  try {
    localStorage.setItem(sideKey(leafId, pointId), JSON.stringify(next));
  } catch { /* 용량 초과 — 화면의 대화는 그대로 두고 저장만 포기한다 */ }
  return next;
}

export function clearSide(leafId, pointId) {
  try { localStorage.removeItem(sideKey(leafId, pointId)); } catch { /* noop */ }
}

export const sideCount = (leafId, pointId) => loadSide(leafId, pointId).length;
```

- [ ] **Step 4: 테스트가 통과하는지 본다**

```bash
cd viewer && node --test src/sideThread.test.js
```

Expected: PASS — 7 tests

- [ ] **Step 5: 커밋**

```bash
git add viewer/src/sideThread.js viewer/src/sideThread.test.js
git commit -m "feat(샛길): 논점에 붙는 끼어들기 대화 저장 — 관 단위 대화와 다른 키"
```

---

## Task 4: 샛길 렌더와 색 구분

**Files:**
- Modify: `viewer/src/ConceptScene.jsx`
- Modify: `viewer/src/index.css`

**Interfaces:**
- Consumes: Task 3 의 `loadSide` · `appendSide` · `clearSide`
- Produces: `ConceptScene` 이 새 prop 둘을 받는다 — `leafId: string` · `onAskSide: (text, ctx) => Promise<string>`. `onAskSide` 가 없으면 입력줄이 키 안내를 띄운다.

- [ ] **Step 1: CSS 를 넣는다**

`viewer/src/index.css` 끝에 붙인다.

```css
/* ── 샛길 — 학습 중 끼어들어 물은 대화 ─────────────────────
   구분선이나 머리글을 두지 않는다. 색이 그 일을 한다.
   파랑을 쓰는 이유는 남아서가 아니라 뜻이 맞아서다 — 파랑은 이미 「시스템이
   개입한 자리」다(선택된 관·이어서 카드·현재 위치). 노랑·보라는 본문 강조
   전용이라 말풍선 배경으로 쓰면 형광펜과 충돌하고, 빨강은 오답 전용이다. */
.cs-side {
  border-left: 3px solid var(--accent);
  background: var(--accent-bg);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding: var(--space-3) var(--space-3) var(--space-2);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.cs-side .cs-bubble { background: var(--sheet); }
.cs-side .cs-line.is-right .cs-bubble { background: var(--sheet-3); }
/* 색만으로는 부족하다 — 색각 이상이면 파란 면과 흰 면이 구분되지 않는데,
   이 구분은 「어디까지가 검증된 내용인가」를 가르는 것이라 놓치면 안 된다. */
.cs-side-tag {
  display: inline-flex;
  align-items: center;
  padding: 1px 5px;
  margin-left: 4px;
  border-radius: var(--radius-sm);
  background: var(--accent);
  color: var(--ink-invert);
  font-size: 10px;
  font-weight: var(--weight-bold);
  letter-spacing: .04em;
}
.cs-side-back {
  align-self: flex-end;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  background: none;
  border: none;
  border-radius: var(--radius-md);
  color: var(--accent-ink);
  font: inherit;
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  cursor: pointer;
}
.cs-side-back:hover { background: var(--sheet); }
.cs-side-note { font-size: var(--text-xs); color: var(--ink-3); }
```

- [ ] **Step 2: `ConceptScene.jsx` 에 샛길 상태를 넣는다**

import 줄에 추가한다.

```jsx
import { loadSide, appendSide, clearSide } from './sideThread';
import { CornerDownLeft } from 'lucide-react';
```

`export default function ConceptScene({` 의 인자에 `leafId, onAskSide,` 를 더한다.

`const [draft, setDraft] = useState('');` 아래에 추가한다.

```jsx
  // 샛길 — 트랙의 cursor 를 건드리지 않는다. 그래야 돌아갈 자리가 정확하다.
  const [side, setSide] = useState([]);
  const [asking, setAsking] = useState(false);
  useEffect(() => {
    setSide(leafId && point?.id ? loadSide(leafId, point.id) : []);
  }, [leafId, point?.id]);
```

- [ ] **Step 3: 샛길 전송 함수를 만든다**

`const again = () => {` 위에 추가한다.

```jsx
  // 끼어들어 묻기. 답이 오든 안 오든 트랙은 그대로다.
  const askSide = async (text) => {
    if (!leafId || !point?.id) return;
    const mine = { who: 'me', text, ts: Date.now() };
    setSide(appendSide(leafId, point.id, mine));
    if (!onAskSide) {
      setSide(appendSide(leafId, point.id, {
        who: 'ai', ts: Date.now(),
        text: '물어보려면 API 키가 필요합니다. 설정에서 키를 넣어 주세요. 키 없이도 논점 대화와 기출 풀이는 끝까지 진행됩니다.',
      }));
      return;
    }
    setAsking(true);
    try {
      const answer = await onAskSide(text, { point, turns });
      setSide(appendSide(leafId, point.id, { who: 'ai', text: answer, ts: Date.now() }));
    } catch (e) {
      setSide(appendSide(leafId, point.id, {
        who: 'ai', ts: Date.now(),
        text: `답을 가져오지 못했습니다. ${e?.message || ''}`.trim(),
      }));
    } finally {
      setAsking(false);
    }
  };
```

- [ ] **Step 4: 샛길을 스트림 끝에 그린다**

`<Stream turns={turns} />` 다음 줄에 추가한다.

```jsx
        {side.length > 0 && (
          <div className="cs-side">
            {side.map((m, i) => (
              <Bubble key={i} who={m.who === 'me' ? WHO.ask : WHO.teach}
                text={m.text} sideTag={m.who === 'ai'} />
            ))}
            {asking && <p className="cs-side-note">답을 가져오는 중…</p>}
            <button type="button" className="cs-side-back"
              onClick={() => { clearSide(leafId, point.id); setSide([]); }}>
              <CornerDownLeft size={14} strokeWidth={1.75} />돌아가기
            </button>
          </div>
        )}
```

- [ ] **Step 5: `Bubble` 에 「AI」 표식을 받는다**

`function Bubble({ who, text, mood = 'idle', cont = false }) {` 를 이렇게 바꾼다.

```jsx
function Bubble({ who, text, mood = 'idle', cont = false, sideTag = false }) {
```

그 안의 `{!cont && <span className="cs-who">{c.name}</span>}` 를 이렇게 바꾼다.

```jsx
        {!cont && (
          <span className="cs-who">
            {c.name}
            {sideTag && <span className="cs-side-tag">AI</span>}
          </span>
        )}
```

- [ ] **Step 6: 입력줄이 샛길로 가게 한다**

`onSend={(text) => { setDraft(''); onAsk?.(text); }}` 를 이렇게 바꾼다.

```jsx
      onSend={(text) => { setDraft(''); askSide(text); }}
```

그리고 `canAsk={!!onAsk}` 를 이렇게 바꾼다.

```jsx
      canAsk
```

- [ ] **Step 7: `ConceptTrack` 이 `leafId` 를 넘기게 한다**

`ConceptTrack.jsx` 의 `<ConceptScene` 에 추가한다.

```jsx
            leafId={leafId}
```

- [ ] **Step 8: 브라우저에서 확인**

관을 열고 하단 입력줄에 「이거 왜요?」를 쓰고 Enter.
확인할 것: 왼쪽에 파란 띠가 있는 블록이 스트림 끝에 붙는다 · 「선생」 옆에 작은 파란 **AI** 표식이 있다 · 키가 없으면 키 안내가 뜬다 · 「돌아가기」를 누르면 샛길이 사라지고 **트랙의 현재 논점·현재 턴이 그대로**다.

- [ ] **Step 9: 커밋**

```bash
git add viewer/src/ConceptScene.jsx viewer/src/ConceptTrack.jsx viewer/src/index.css
git commit -m "feat(샛길): 학습 중 끼어들어 묻고 그 자리로 돌아오기 — 색으로 구분"
```

---

## Task 5: 교재 청크 빌드 스크립트

**Files:**
- Create: `scripts/lectures/build_rag_chunks.py`
- Create: `scripts/lectures/test_build_rag_chunks.py`

**Interfaces:**
- Consumes: 없음
- Produces: `viewer/public/data/study/{과목}/rag/{unit}.chunks.json` — `{"unit": str, "chunks": [{"id": str, "path": [str], "text": str, "terms": [str]}]}`

시스템 파이썬은 3.9 다. `match` 문과 `X | Y` 타입 표기를 쓰면 안 된다.

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`scripts/lectures/test_build_rag_chunks.py`:

```python
import unittest
from build_rag_chunks import split_chunks, terms_of

MD = """# G01 경제학의 기초

### 1. 경제학의 정의

경제학은 희소한 자원의 배분을 다루는 학문이다.

#### 가. 미시경제학

개별 경제주체의 선택을 본다.

#### 나. 거시경제학

경제 전체의 총량을 본다.
"""


class SplitTest(unittest.TestCase):
    def test_소제목마다_청크가_하나씩(self):
        cs = split_chunks(MD)
        self.assertEqual(len(cs), 3)

    def test_제목_경로를_보존한다(self):
        cs = split_chunks(MD)
        self.assertEqual(cs[1]['path'], ['1. 경제학의 정의', '가. 미시경제학'])

    def test_본문이_들어간다(self):
        cs = split_chunks(MD)
        self.assertIn('개별 경제주체', cs[1]['text'])

    def test_너무_짧은_토막은_버린다(self):
        cs = split_chunks("### 빈 절\n\n### 다음\n\n내용이 충분히 긴 문단입니다. 검색에 쓸 만합니다.\n")
        self.assertEqual(len(cs), 1)


class TermsTest(unittest.TestCase):
    def test_어절과_2gram_을_함께_뽑는다(self):
        t = terms_of('한계대체율은 무차별곡선의 기울기다')
        self.assertIn('한계대체율은', t)
        self.assertIn('한계', t)

    def test_한_글자_어절은_버린다(self):
        self.assertNotIn('의', terms_of('의 것'))


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: 테스트가 실패하는지 본다**

```bash
cd scripts/lectures && python3 -m unittest test_build_rag_chunks -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'build_rag_chunks'`

- [ ] **Step 3: 구현한다**

`scripts/lectures/build_rag_chunks.py`:

```python
# 교재 md → 검색용 청크. 심화 탭의 RAG 가 이걸 읽는다.
#
# 왜 필요한가: 지금 심화 튜터는 단원 md 를 통째로 프롬프트에 넣는다(평균 10만 자).
# 질문이 무엇이든 같은 덩어리가 가고, 관련 없는 부분까지 매번 들어간다.
# 소제목 단위로 쪼개 두면 질문에 관련된 것만 골라 넣을 수 있다.
#
# 임베딩을 쓰지 않는다 — 제공자마다 달라서 제공자를 바꾸면 인덱스를 다시 만들어야
# 한다. 어절과 2-gram 만으로도 시험 용어(「한계대체율」·「구축효과」)는 그대로 잡힌다.
import json
import os
import re
import sys

# 이보다 짧은 토막은 검색에 쓸 수 없다. 제목만 있고 본문이 없는 자리다.
MIN_CHARS = 80
HEAD = re.compile(r'^(#{3,4})\s+(.+?)\s*$', re.M)


def split_chunks(md):
    """소제목(### / ####) 단위로 쪼갠다. 제목 경로를 보존한다."""
    heads = list(HEAD.finditer(md))
    out = []
    for i, m in enumerate(heads):
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(md)
        body = md[start:end].strip()
        if len(body) < MIN_CHARS:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        # 제목 경로 — 이 청크 위쪽에서 더 얕은 제목을 거슬러 올라간다.
        path = [title]
        lv = level
        for prev in reversed(heads[:i]):
            plv = len(prev.group(1))
            if plv < lv:
                path.insert(0, prev.group(2).strip())
                lv = plv
        out.append({'path': path, 'text': body})
    return out


def terms_of(text):
    """어절 + 2-gram. 형태소 분석기 없이 한국어 용어를 잡는 최소 장치."""
    words = [w for w in re.split(r'[^0-9A-Za-z가-힣]+', text) if len(w) >= 2]
    grams = set(words)
    for w in words:
        for k in range(len(w) - 1):
            grams.add(w[k:k + 2])
    return sorted(grams)


def build(unit_path, out_path):
    md = open(unit_path, encoding='utf-8').read()
    unit = os.path.splitext(os.path.basename(unit_path))[0]
    chunks = []
    for n, c in enumerate(split_chunks(md)):
        chunks.append({
            'id': '%s#%d' % (unit, n),
            'path': c['path'],
            'text': c['text'],
            'terms': terms_of(c['path'][-1] + ' ' + c['text']),
        })
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump({'unit': unit, 'chunks': chunks},
              open(out_path, 'w', encoding='utf-8'), ensure_ascii=False)
    return len(chunks)


def main(subject):
    src_dir = 'viewer/public/data/study/%s/units' % subject
    out_dir = 'viewer/public/data/study/%s/rag' % subject
    total = 0
    for name in sorted(os.listdir(src_dir)):
        if not name.endswith('.md') or name.endswith('.orig'):
            continue
        n = build(os.path.join(src_dir, name),
                  os.path.join(out_dir, name[:-3] + '.chunks.json'))
        print('%s → %d청크' % (name, n))
        total += n
    print('합계 %d청크' % total)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'economics')
```

- [ ] **Step 4: 테스트가 통과하는지 본다**

```bash
cd scripts/lectures && python3 -m unittest test_build_rag_chunks -v
```

Expected: PASS — 6 tests

- [ ] **Step 5: 실제로 돌려 본다**

```bash
cd /Users/hanjiho/Documents/감정평가사\ 기출문제 && python3 scripts/lectures/build_rag_chunks.py economics
ls -la viewer/public/data/study/economics/rag/ | head
du -sh viewer/public/data/study/economics/rag/
```

Expected: 청크 파일이 단원 수만큼 생기고 합계가 1,000~1,500 사이. 전체 크기 1MB 미만.

- [ ] **Step 6: 커밋**

```bash
git add scripts/lectures/build_rag_chunks.py scripts/lectures/test_build_rag_chunks.py viewer/public/data/study/economics/rag
git commit -m "feat(RAG): 교재 md 를 소제목 청크로 — 10만 자 통째 대신 검색 가능한 단위로"
```

---

## Task 6: 키워드 검색

**Files:**
- Create: `viewer/src/rag/search.js`
- Create: `viewer/src/rag/search.test.js`

**Interfaces:**
- Consumes: Task 5 가 만든 청크 JSON 모양
- Produces:
  - `queryTerms(q) -> string[]`
  - `scoreChunk(chunk, terms) -> number`
  - `searchChunks(chunks, q, limit = 6) -> Array<chunk & {score:number}>`

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`viewer/src/rag/search.test.js`:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { queryTerms, scoreChunk, searchChunks } from './search.js';

const mk = (id, title, text) => ({
  id, path: [title], text,
  terms: [...new Set(
    text.split(/[^0-9A-Za-z가-힣]+/).filter((w) => w.length >= 2)
      .flatMap((w) => [w, ...Array.from({ length: w.length - 1 }, (_, i) => w.slice(i, i + 2))]),
  )],
});

const CHUNKS = [
  mk('a', '한계대체율', '한계대체율은 무차별곡선의 기울기이며 체감한다'),
  mk('b', '구축효과', '구축효과는 정부지출이 민간투자를 밀어내는 현상이다'),
  mk('c', '탄력성', '수요의 가격탄력성은 대체재가 많을수록 커진다'),
];

test('질문에서 두 글자 이상 어절을 뽑는다', () => {
  const t = queryTerms('구축효과가 뭐예요?');
  assert.ok(t.includes('구축효과가'));
  assert.ok(!t.includes('가'));
});

test('겹치는 말이 많을수록 점수가 높다', () => {
  const t = queryTerms('구축효과');
  assert.ok(scoreChunk(CHUNKS[1], t) > scoreChunk(CHUNKS[0], t));
});

test('가장 관련 있는 청크가 맨 앞', () => {
  const hits = searchChunks(CHUNKS, '구축효과가 뭐예요?');
  assert.equal(hits[0].id, 'b');
});

test('limit 을 넘지 않는다', () => {
  assert.equal(searchChunks(CHUNKS, '한계 구축 탄력', 2).length, 2);
});

test('겹치는 말이 없으면 빈손으로 돌려준다 — 지어내지 않게', () => {
  assert.deepEqual(searchChunks(CHUNKS, '점심 메뉴 추천'), []);
});

test('빈 질문은 빈 결과', () => {
  assert.deepEqual(searchChunks(CHUNKS, ''), []);
  assert.deepEqual(searchChunks(null, '구축효과'), []);
});
```

- [ ] **Step 2: 테스트가 실패하는지 본다**

```bash
cd viewer && node --test src/rag/search.test.js
```

Expected: FAIL — `Cannot find module './search.js'`

- [ ] **Step 3: 구현한다**

`viewer/src/rag/search.js`:

```js
// 교재 청크 검색 — 키 없이 동작한다.
//
// 임베딩을 쓰지 않는 이유: 임베딩은 제공자마다 다르고 Anthropic 에는 엔드포인트가
// 없다. 제공자를 바꾸면 인덱스를 다시 만들어야 한다. 어느 제공자든 최소한은
// 동작해야 하므로 어절과 2-gram 으로 점수를 낸다.
//
// 정직하게: 키워드 검색은 임베딩보다 약하다. 「물가가 오르면 실질임금은?」처럼
// 용어가 안 겹치는 질문은 잘 못 찾는다. 못 찾으면 **빈손으로 돌려준다** —
// 엉뚱한 청크를 주느니 튜터가 「교재에서 못 찾았습니다」라고 말하는 편이 낫다.

/** 검색에 쓸 최소 점수. 이보다 낮으면 우연히 두 글자가 겹친 것이다. */
const MIN_SCORE = 2;

export function queryTerms(q) {
  const words = String(q || '').split(/[^0-9A-Za-z가-힣]+/).filter((w) => w.length >= 2);
  const set = new Set(words);
  for (const w of words) {
    for (let i = 0; i < w.length - 1; i += 1) set.add(w.slice(i, i + 2));
  }
  return [...set];
}

export function scoreChunk(chunk, terms) {
  if (!chunk?.terms?.length || !terms.length) return 0;
  const have = new Set(chunk.terms);
  let score = 0;
  for (const t of terms) {
    if (!have.has(t)) continue;
    // 긴 말이 겹치는 쪽이 값지다. 두 글자 조각 하나는 우연일 수 있다.
    score += t.length >= 3 ? 3 : 1;
  }
  return score;
}

export function searchChunks(chunks, q, limit = 6) {
  if (!Array.isArray(chunks) || !chunks.length) return [];
  const terms = queryTerms(q);
  if (!terms.length) return [];
  return chunks
    .map((c) => ({ ...c, score: scoreChunk(c, terms) }))
    .filter((c) => c.score >= MIN_SCORE)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}
```

- [ ] **Step 4: 테스트가 통과하는지 본다**

```bash
cd viewer && node --test src/rag/search.test.js
```

Expected: PASS — 6 tests

- [ ] **Step 5: 커밋**

```bash
git add viewer/src/rag/search.js viewer/src/rag/search.test.js
git commit -m "feat(RAG): 키워드 청크 검색 — 못 찾으면 빈손으로 돌려준다"
```

---

## Task 7: 프롬프트 조립과 예산 상한

**Files:**
- Create: `viewer/src/rag/context.js`
- Create: `viewer/src/rag/context.test.js`

**Interfaces:**
- Consumes: Task 6 의 `searchChunks`
- Produces:
  - `BUDGET = { chunks: 3000, points: 600, record: 800, lecture: 800 }`
  - `buildContext({ question, chunks, points, record, lecture }) -> { text: string, cited: Array<{id,path}> }`

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`viewer/src/rag/context.test.js`:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { buildContext, BUDGET } from './context.js';

const chunk = (id, text) => ({ id, path: ['제3절', '취득원가'], text, terms: ['취득원가', '취득'] });

test('예산 상한이 스펙 값과 같다', () => {
  assert.deepEqual(BUDGET, { chunks: 3000, points: 600, record: 800, lecture: 800 });
});

test('찾은 청크를 본문에 넣고 출처를 돌려준다', () => {
  const r = buildContext({
    question: '취득원가가 뭐죠?',
    chunks: [chunk('G01#1', '취득원가는 매입원가와 전환원가의 합이다')],
  });
  assert.ok(r.text.includes('매입원가와 전환원가'));
  assert.equal(r.cited.length, 1);
  assert.equal(r.cited[0].id, 'G01#1');
});

test('청크 예산을 넘기지 않는다', () => {
  const big = Array.from({ length: 20 }, (_, i) => chunk(`G01#${i}`, '취득원가 '.repeat(200)));
  const r = buildContext({ question: '취득원가', chunks: big });
  const body = r.text.split('[교재]')[1] || '';
  assert.ok(body.length <= BUDGET.chunks + 400, `교재 블록이 예산을 넘었다: ${body.length}`);
});

test('찾은 것이 없으면 그렇게 적는다 — 지어내지 않게', () => {
  const r = buildContext({ question: '점심 메뉴', chunks: [chunk('G01#1', '취득원가는…')] });
  assert.ok(r.text.includes('교재에서 찾지 못했다'));
  assert.deepEqual(r.cited, []);
});

test('논점·학습 기록·강의 필기도 각자 상한을 지킨다', () => {
  const r = buildContext({
    question: '취득원가',
    chunks: [],
    points: 'ㄱ'.repeat(5000),
    record: 'ㄴ'.repeat(5000),
    lecture: 'ㄷ'.repeat(5000),
  });
  assert.ok((r.text.match(/ㄱ/g) || []).length <= BUDGET.points);
  assert.ok((r.text.match(/ㄴ/g) || []).length <= BUDGET.record);
  assert.ok((r.text.match(/ㄷ/g) || []).length <= BUDGET.lecture);
});

test('빈 블록은 아예 넣지 않는다', () => {
  const r = buildContext({ question: '취득원가', chunks: [] });
  assert.ok(!r.text.includes('[학습 기록]'));
});
```

- [ ] **Step 2: 테스트가 실패하는지 본다**

```bash
cd viewer && node --test src/rag/context.test.js
```

Expected: FAIL — `Cannot find module './context.js'`

- [ ] **Step 3: 구현한다**

`viewer/src/rag/context.js`:

```js
// 심화 튜터에게 줄 자료를 조립한다 — 블록마다 상한을 못 박는다.
//
// 지금은 단원 md 를 통째로 넣는다(평균 10만 자). 관련 없는 부분까지 매번 들어가고
// 캐시 자리를 잡아먹는다. 여기서는 블록마다 글자 수를 자른다.
//
// 상한은 스펙 §6-4 의 값이다. 튜닝하려면 스펙을 먼저 고친다.

export const BUDGET = { chunks: 3000, points: 600, record: 800, lecture: 800 };

const clip = (s, n) => (s && s.length > n ? s.slice(0, n) : (s || ''));

/**
 * @returns {{ text: string, cited: Array<{id:string, path:string[]}> }}
 *   text  — 시스템 블록에 얹을 자료
 *   cited — 넣은 청크. 답변의 출처 칩을 만들 때 화면이 쓴다.
 */
export function buildContext({ question, chunks, points, record, lecture }) {
  const parts = [];
  const cited = [];

  const hits = Array.isArray(chunks) ? chunks : [];
  if (hits.length) {
    let used = 0;
    const lines = [];
    for (const c of hits) {
      const body = clip(c.text, BUDGET.chunks - used);
      if (!body) break;
      lines.push(`— ${(c.path || []).join(' › ')}\n${body}`);
      cited.push({ id: c.id, path: c.path || [] });
      used += body.length;
      if (used >= BUDGET.chunks) break;
    }
    parts.push(`[교재]\n${lines.join('\n\n')}`);
  } else {
    // 빈손일 때 그렇다고 적는 것이 중요하다. 안 적으면 모델이 기억으로 지어낸다.
    parts.push(`[교재]\n이 질문에 걸리는 대목을 교재에서 찾지 못했다. 교재를 인용하지 말고, 모르면 모른다고 답하라.`);
  }

  if (points) parts.push(`[이 관의 논점]\n${clip(points, BUDGET.points)}`);
  if (record) parts.push(`[학습 기록]\n${clip(record, BUDGET.record)}`);
  if (lecture) parts.push(`[강의 필기]\n${clip(lecture, BUDGET.lecture)}`);

  return { text: parts.join('\n\n'), cited };
}
```

- [ ] **Step 4: 테스트가 통과하는지 본다**

```bash
cd viewer && node --test src/rag/context.test.js
```

Expected: PASS — 6 tests

- [ ] **Step 5: 커밋**

```bash
git add viewer/src/rag/context.js viewer/src/rag/context.test.js
git commit -m "feat(RAG): 프롬프트 블록 조립 — 블록마다 상한, 빈손이면 빈손이라 적는다"
```

---

## Task 8: 약점 산출

**Files:**
- Create: `viewer/src/weakSpots.js`
- Create: `viewer/src/weakSpots.test.js`

**Interfaces:**
- Consumes: 없음 (입력은 호출자가 모아 준다)
- Produces: `weakSpots({ leafId, track, progress, items, quizStats }) -> Array<{ title, why, pointId, seq }>` — 최대 5개, 아픈 순.

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`viewer/src/weakSpots.test.js`:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { weakSpots, WEAK_MIN_MISS } from './weakSpots.js';

const TRACK = {
  points: [
    { id: 'p1', seq: 1, title: '취득원가의 범위' },
    { id: 'p2', seq: 2, title: '매입할인의 처리' },
    { id: 'p3', seq: 3, title: '저가법 적용 단위' },
  ],
};

test('두 번 넘게 틀린 논점만 뽑는다', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [
      { leafId: 'L', pointId: 'p2', attempted: 3, correct: 0, kind: 'ox' },
      { leafId: 'L', pointId: 'p1', attempted: 3, correct: 3, kind: 'ox' },
    ],
  });
  assert.equal(out.length, 1);
  assert.equal(out[0].pointId, 'p2');
});

test('why 가 숫자로 근거를 댄다', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [{ leafId: 'L', pointId: 'p2', attempted: 3, correct: 0, kind: 'ox' }],
  });
  assert.equal(out[0].why, '확인 문제 3회 중 3개 오답 · 논점 2');
});

test('기출 오답은 「기출」로 적는다', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [{ leafId: 'L', pointId: 'p3', attempted: 2, correct: 0, kind: 'exam' }],
  });
  assert.ok(out[0].why.startsWith('기출 2문제 중 2개 오답'));
});

test('더 많이 틀린 것이 앞', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [
      { leafId: 'L', pointId: 'p1', attempted: 3, correct: 1, kind: 'ox' },
      { leafId: 'L', pointId: 'p2', attempted: 4, correct: 0, kind: 'ox' },
    ],
  });
  assert.deepEqual(out.map((w) => w.pointId), ['p2', 'p1']);
});

test('다섯 개를 넘지 않는다', () => {
  const many = Array.from({ length: 9 }, (_, i) => ({
    leafId: 'L', pointId: `p${i}`, attempted: 3, correct: 0, kind: 'ox',
  }));
  const track = { points: many.map((m, i) => ({ id: m.pointId, seq: i + 1, title: `T${i}` })) };
  assert.equal(weakSpots({ leafId: 'L', track, items: many }).length, 5);
});

test('다른 관의 기록은 섞지 않는다', () => {
  const out = weakSpots({
    leafId: 'L', track: TRACK,
    items: [{ leafId: '다른관', pointId: 'p2', attempted: 3, correct: 0, kind: 'ox' }],
  });
  assert.deepEqual(out, []);
});

test('상수는 2다 — 「두 번 이상 틀린 곳」', () => {
  assert.equal(WEAK_MIN_MISS, 2);
});

test('입력이 비어도 던지지 않는다', () => {
  assert.deepEqual(weakSpots({}), []);
});
```

- [ ] **Step 2: 테스트가 실패하는지 본다**

```bash
cd viewer && node --test src/weakSpots.test.js
```

Expected: FAIL — `Cannot find module './weakSpots.js'`

- [ ] **Step 3: 구현한다**

`viewer/src/weakSpots.js`:

```js
// 심화 탭의 약점 카드 — 「이 관에서 두 번 이상 틀린 곳입니다」.
//
// 자유 대화는 「무엇을 물어야 할지 모르겠다」에서 막힌다. 약점 카드가 첫 발을
// 대신 뗀다. 화면과 프롬프트가 **같은 것**을 보게 하려고 여기 한 곳에서만 뽑는다.
//
// 부제(why)가 근거다 — 「기출 3문제 중 3개 오답」처럼 왜 약점으로 뽑혔는지 숫자로
// 말한다. 근거 없이 「약점」이라고만 하면 믿을 이유가 없다.

/** 이만큼 틀려야 약점이다. 한 번 틀린 것은 실수일 수 있다. */
export const WEAK_MIN_MISS = 2;

const MAX = 5;
const KIND_LABEL = { exam: '기출', ox: '확인 문제', recall: '서술 인출', quiz: '확인 문제' };
const KIND_UNIT = { exam: '문제', ox: '회', recall: '회', quiz: '회' };

export function weakSpots({ leafId, track, items }) {
  const points = track?.points || [];
  if (!leafId || !points.length || !Array.isArray(items)) return [];
  const byId = new Map(points.map((p) => [p.id, p]));

  const rows = [];
  for (const it of items) {
    if (it?.leafId !== leafId) continue;             // 다른 관의 기록을 섞지 않는다
    const p = byId.get(it.pointId);
    if (!p) continue;
    const miss = (it.attempted || 0) - (it.correct || 0);
    if (miss < WEAK_MIN_MISS) continue;
    const label = KIND_LABEL[it.kind] || '확인 문제';
    const unit = KIND_UNIT[it.kind] || '회';
    rows.push({
      pointId: p.id,
      seq: p.seq,
      title: p.title,
      miss,
      why: `${label} ${it.attempted}${unit} 중 ${miss}개 오답 · 논점 ${p.seq}`,
    });
  }
  return rows.sort((a, b) => b.miss - a.miss).slice(0, MAX);
}
```

- [ ] **Step 4: 테스트가 통과하는지 본다**

```bash
cd viewer && node --test src/weakSpots.test.js
```

Expected: PASS — 8 tests

- [ ] **Step 5: 커밋**

```bash
git add viewer/src/weakSpots.js viewer/src/weakSpots.test.js
git commit -m "feat(심화): 약점 산출 — 부제가 숫자로 근거를 댄다"
```

---

## Task 9: 심화 탭 화면

**Files:**
- Create: `viewer/src/DeepChat.jsx`
- Modify: `viewer/src/ConceptTrack.jsx`
- Modify: `viewer/src/index.css`

**Interfaces:**
- Consumes: Task 8 의 `weakSpots`, Task 6 의 `searchChunks`, Task 7 의 `buildContext`, `aiLearningStore` 의 `getApiKey`
- Produces: `DeepChat({ leafId, leafTitle, track, chunks, items, onAsk, onGoPoint })`. `onAsk` 가 없으면 키 입력 안내를 띄운다.

- [ ] **Step 1: CSS 를 넣는다**

`viewer/src/index.css` 끝에 붙인다.

```css
/* ── 심화 탭 — 시안 316:506 ───────────────────────────────── */
.deep-cards { display: flex; flex-direction: column; gap: var(--space-2); }
.deep-card {
  display: flex;
  flex-direction: column;
  gap: 3px;
  width: 100%;
  padding: 13px var(--space-4);
  background: var(--sheet);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  font: inherit;
  text-align: left;
  cursor: pointer;
}
.deep-card:hover { border-color: var(--line-strong); background: var(--sheet-2); }
.deep-card-title { font-size: var(--text-base); color: var(--ink); }
.deep-card-why { font-size: var(--text-xs); color: var(--ink-meta); }
.deep-note { font-size: var(--text-sm); color: var(--ink-meta); text-align: center; padding: var(--space-3) 0; }

/* 출처 칩 — 답변이 어느 논점에서 왔는지. 교재 문단 번호가 아니라 논점이다. */
.deep-cite {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: var(--space-2);
  padding: 3px 8px;
  background: var(--sunken);
  border: none;
  border-radius: var(--radius-sm);
  color: var(--ink-2);
  font: inherit;
  font-size: var(--text-2xs);
  cursor: pointer;
}
.deep-cite:hover { background: var(--accent-bg); color: var(--accent-ink); }

/* 키 입력 — 시안 284:2 */
.byok { max-width: 640px; margin: var(--space-7) auto 0; padding: 0 var(--space-4); }
.byok h2 { margin: 0 0 var(--space-4); font-size: var(--text-xl); color: var(--ink); }
.byok ul { margin: 0 0 var(--space-5); padding-left: 18px; color: var(--ink-2); font-size: var(--text-sm); line-height: var(--leading-read); }
.byok-box {
  background: var(--sheet);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
}
.byok-box h3 { margin: 0 0 var(--space-2); font-size: var(--text-md); color: var(--ink); }
.byok-box p { margin: 0 0 var(--space-4); font-size: var(--text-sm); color: var(--ink-2); line-height: var(--leading-read); }
.byok-row { display: flex; gap: var(--space-2); }
.byok-row select, .byok-row input {
  min-height: 44px;
  padding: 0 var(--space-3);
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-md);
  background: var(--sheet);
  font: inherit;
  font-size: var(--text-sm);
  color: var(--ink);
}
.byok-row input { flex: 1 1 auto; min-width: 0; }
.byok-hint { margin-top: var(--space-3); font-size: var(--text-xs); color: var(--ink-meta); }
```

- [ ] **Step 2: `DeepChat.jsx` 를 만든다**

```jsx
// 심화 탭 — 약점에서 출발하는 자유 대화.
//
// 빈손으로 시작하지 않는다(시안 316:506). 탭을 열면 「이 관에서 두 번 이상 틀린
// 곳입니다」와 약점 카드가 먼저 뜬다. 자유 대화는 「무엇을 물어야 할지 모르겠다」에서
// 막히기 때문이다.
//
// 말풍선은 개념 완성과 같은 렌더러(ConceptScene 의 Bubble)를 쓰지 않고 여기서 다시
// 그린다 — Bubble 은 ConceptScene 안의 지역 컴포넌트라 지금 내보내지 않는다.
// 클래스 이름은 같은 것을 쓰므로 생김새는 같다.
import { useMemo, useState } from 'react';
import ParsedText from './ParsedText';
import Avatar from './ConceptCast';
import { markEmphasis } from './emphasis';
import { weakSpots } from './weakSpots';
import { WHO } from './conceptTurns';

export default function DeepChat({
  leafTitle, track, items, onAsk, onGoPoint, onOpenSettings,
}) {
  const [msgs, setMsgs] = useState([]);
  const [draft, setDraft] = useState('');
  const [busy, setBusy] = useState(false);
  const weak = useMemo(
    () => weakSpots({ leafId: track?.leaf_id, track, items }),
    [track, items],
  );

  if (!onAsk) {
    return (
      <div className="cs-room">
        <div className="cs-stream">
          <div className="byok">
            <h2>AI 튜터와 단원별 1:1 학습</h2>
            <ul>
              <li>교재 전 단원을 대화하며 개념 학습 → 이해 확인 퀴즈</li>
              <li>문제풀이 중 막히면 「AI 튜터로 이 단원 배우기」로 바로 연결</li>
              <li>학습 기록 기반 약점 분석·복습 추천</li>
            </ul>
            <div className="byok-box">
              <h3>API 키 입력</h3>
              <p>
                본 앱은 사용자의 API 키로 직접 요청합니다. 키는 이 기기에만 저장되고
                서버로 전송되지 않습니다. 키 없이도 개념 완성과 기출 분석은 끝까지 진행됩니다.
              </p>
              <button type="button" className="cs-primary" onClick={onOpenSettings}>
                설정에서 키 넣기
              </button>
              <p className="byok-hint">Claude · OpenAI · Gemini 를 모두 지원합니다.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const send = async (text) => {
    if (!text.trim() || busy) return;
    setDraft('');
    setMsgs((m) => m.concat({ who: 'me', text }));
    setBusy(true);
    try {
      const { answer, cited } = await onAsk(text);
      setMsgs((m) => m.concat({ who: 'ai', text: answer, cited }));
    } catch (e) {
      setMsgs((m) => m.concat({ who: 'ai', text: `답을 가져오지 못했습니다. ${e?.message || ''}`.trim() }));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="cs-room">
      <div className="cs-stream">
        {msgs.length === 0 && (
          <>
            <Line who={WHO.teach} text={weak.length
              ? '이 관에서 두 번 이상 틀린 곳입니다.\n눌러서 바로 이야기해요.'
              : `${leafTitle || '이 관'}에 대해 무엇이든 물어보세요.`} />
            {weak.length > 0 && (
              <div className="deep-cards">
                {weak.map((w) => (
                  <button type="button" key={w.pointId} className="deep-card"
                    onClick={() => send(`${w.title}에 대해 다시 설명해 주세요. 제가 자꾸 틀립니다.`)}>
                    <span className="deep-card-title">{w.title}</span>
                    <span className="deep-card-why">{w.why}</span>
                  </button>
                ))}
              </div>
            )}
            <p className="deep-note">목록에 없는 것도 아래에 바로 물어보세요.</p>
          </>
        )}
        {msgs.map((m, i) => (
          <Line key={i} who={m.who === 'me' ? WHO.ask : WHO.teach} text={m.text}
            cited={m.cited} onGoPoint={onGoPoint} />
        ))}
        {busy && <p className="deep-note">답을 가져오는 중…</p>}
      </div>
      <div className="cs-dock">
        <div className="cs-inputwrap">
          <div className="cs-input">
            <input value={draft} onChange={(e) => setDraft(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); send(draft); } }}
              placeholder="무엇이든 물어보세요" aria-label="질문" />
            <button type="button" className="cs-send" onClick={() => send(draft)}
              disabled={!draft.trim() || busy} aria-label="보내기">→</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function Line({ who, text, cited, onGoPoint }) {
  const right = who === WHO.ask;
  return (
    <div className={`cs-line${right ? ' is-right' : ''}`}>
      {!right && <div className="cs-avatar"><Avatar who={who} size={28} /></div>}
      <div className="cs-linebody">
        <span className="cs-who">{right ? '나' : '선생'}</span>
        <div className={`cs-bubble cs-bubble--${who}`}>
          <ParsedText text={markEmphasis(text)} />
          {/* 출처는 교재 문단 번호가 아니라 논점이다 — 학습자가 아는 단위가 그것이다. */}
          {(cited || []).slice(0, 2).map((c) => (
            <button type="button" key={c.id} className="deep-cite"
              onClick={() => onGoPoint?.(c)}>
              {(c.path || []).slice(-1)[0] || '교재'}
            </button>
          ))}
        </div>
      </div>
      {right && <div className="cs-avatar"><Avatar who={who} size={28} /></div>}
    </div>
  );
}
```

- [ ] **Step 3: `ConceptTrack` 이 심화 탭에서 `DeepChat` 을 그리게 한다**

`ConceptTrack.jsx` import 에 추가한다.

```jsx
import DeepChat from './DeepChat';
import { getAllItems } from './studyDrill';
```

`if (loading) return workspace(` 바로 앞에 추가한다.

```jsx
  // 심화는 트랙이 없다. 로딩·트랙 없음 분기보다 먼저 가로챈다.
  if (leafId && tab === 'deep') {
    return workspace(
      <div className="concept-runner">
        <ConceptTabs tab={tab} onPick={setTab} />
        <DeepChat
          leafTitle={leaf?.title || ''}
          track={track ? { ...track, leaf_id: leafId } : null}
          items={getAllItems()}
          onAsk={null}
          onOpenSettings={() => onOpenDeep?.(leafId, null, null, { openSettings: true })}
          onGoPoint={null}
        />
      </div>,
    );
  }
```

`onAsk={null}` 은 Task 10 에서 실제 호출로 바꾼다. 지금은 키 입력 화면이 보이는 것까지가 목표다.

- [ ] **Step 4: 브라우저에서 확인**

관을 열고 「심화」 탭을 누른다.
확인할 것: 「AI 튜터와 단원별 1:1 학습」 안내와 키 입력 상자가 보인다 · 개념 완성으로 돌아가면 대화가 그대로다.

- [ ] **Step 5: 커밋**

```bash
git add viewer/src/DeepChat.jsx viewer/src/ConceptTrack.jsx viewer/src/index.css
git commit -m "feat(심화): 약점 카드로 시작하는 탭 — 키가 없으면 안내"
```

---

## Task 10: 심화·샛길을 실제 모델에 연결

**Files:**
- Modify: `viewer/src/ConceptTrack.jsx`
- Modify: `viewer/src/App.jsx`

**Interfaces:**
- Consumes: Task 6·7 의 `searchChunks`·`buildContext`, `aiProviders` 의 `sendMessagesUnified`, `aiLearningStore` 의 `getApiKey`·`getPrefs`
- Produces: `ConceptTrack` 이 `askTutor(question) -> Promise<{answer, cited}>` 를 갖고, 이를 `DeepChat.onAsk` 와 `ConceptScene.onAskSide` 에 넘긴다.

- [ ] **Step 1: 청크를 읽는다**

`ConceptTrack.jsx` 의 `const [index, setIndex] = useState(null);` 아래에 추가한다.

```jsx
  // 교재 청크 — 심화·샛길의 검색 재료. 관이 아니라 단원 단위 파일이다.
  const [chunks, setChunks] = useState([]);
  useEffect(() => {
    if (!leaf?.unit_code) { setChunks([]); return undefined; }
    let dead = false;
    fetch(`${studyBase(subjectId)}rag/${leaf.unit_code}.chunks.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => { if (!dead) setChunks(d?.chunks || []); })
      .catch(() => { if (!dead) setChunks([]); });
    return () => { dead = true; };
  }, [subjectId, leaf?.unit_code]);
```

- [ ] **Step 2: 튜터 호출을 만든다**

`const runCommand = useCallback((cmd) => {` 위에 추가한다.

```jsx
  // 심화·샛길이 함께 쓰는 튜터 호출. 키가 없으면 null 을 넘겨 화면이 안내를 띄우게 한다.
  const hasKey = !!getApiKey(getPrefs().provider || 'anthropic');
  const askTutor = useCallback(async (question) => {
    const hits = searchChunks(chunks, question);
    const ctx = buildContext({
      question,
      chunks: hits,
      points: (track?.points || []).map((p) => `- ${p.title}: ${p.gist || ''}`).join('\n'),
      record: buildLearnerStatus(leafId, leaf?.title || ''),
    });
    const prefs = getPrefs();
    const res = await sendMessagesUnified({
      model: prefs.model,
      apiKey: getApiKey(getProviderForModel(prefs.model)),
      max_tokens: prefs.max_tokens || 1200,
      system: [
        { type: 'text', text: '당신은 감정평가사 1차 시험 과외 선생님입니다. 학생이 지금 보고 있는 관에 대해 답합니다.' },
        { type: 'text', text: '답한 내용이 어느 대목에서 온 것인지 밝히고, 준 자료에 없는 내용은 「교재에 없습니다」라고 말하고 지어내지 마라.' },
        { type: 'text', text: ctx.text },
      ],
      messages: [{ role: 'user', content: question }],
    });
    return { answer: res?.text || '', cited: ctx.cited };
  }, [chunks, track, leafId, leaf?.title]);
```

import 를 더한다.

```jsx
import { searchChunks } from './rag/search';
import { buildContext } from './rag/context';
import { sendMessagesUnified, getProviderForModel } from './aiProviders';
import { getApiKey, getPrefs } from './aiLearningStore';
import { buildLearnerStatus, getAllItems } from './studyDrill';
```

- [ ] **Step 3: `DeepChat` 과 `ConceptScene` 에 연결한다**

Task 9 에서 넣은 `onAsk={null}` 을 바꾼다.

```jsx
          onAsk={hasKey ? async (q) => askTutor(q) : null}
```

`<ConceptScene` 에 추가한다.

```jsx
            onAskSide={hasKey ? async (q) => (await askTutor(q)).answer : null}
```

- [ ] **Step 4: 브라우저에서 확인 — 키 없이**

설정에서 키를 비운 상태로 심화 탭을 연다.
확인할 것: 키 입력 안내가 보인다 · 개념 완성에서 입력줄에 질문을 쓰면 샛길 블록에 키 안내가 뜬다 · **트랙은 그대로**다.

- [ ] **Step 5: 브라우저에서 확인 — 키를 넣고**

설정에서 키를 넣는다. 심화 탭에서 「구축효과가 뭐죠?」를 묻는다.
확인할 것: 답이 오고 아래에 출처 칩이 붙는다 · 개념 완성에서 샛길로 물어도 답이 온다 · 「돌아가기」로 원래 턴에 정확히 돌아온다.

- [ ] **Step 6: 커밋**

```bash
git add viewer/src/ConceptTrack.jsx viewer/src/App.jsx
git commit -m "feat(심화·샛길): 검색·예산 조립을 실제 모델 호출에 연결"
```

---

## Task 11: OX 턴

**Files:**
- Modify: `viewer/src/conceptTurns.js`
- Modify: `viewer/src/conceptTurns.test.js`
- Modify: `viewer/src/ConceptScene.jsx`
- Modify: `viewer/src/index.css`

**Interfaces:**
- Consumes: 기존 `choose`·`visibleTurns`
- Produces: 턴 `{ who: 'ox', prompt, answer: true|false, reply }` 를 quiz 와 같은 경로로 처리한다.

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`viewer/src/conceptTurns.test.js` 끝에 붙인다.

```js
// ── OX 턴 — 지문 하나를 O/X 로 묻는다 ──────────────────────────────
const OX_POINT = {
  id: 'ox1',
  turns: [
    { who: 'teach', text: '취득원가는 셋의 합입니다.' },
    { who: 'ox', prompt: '「매입할인은 수익으로 잡는다」', answer: false, reply: '차감합니다.' },
    { who: 'mate', text: '이 자리는 자주 뒤집힙니다.' },
  ],
};

test('OX 도 quiz 처럼 풀어야 넘어간다', () => {
  let s = advance(OX_POINT, initTurnState());     // ox 턴으로
  assert.equal(canAdvance(OX_POINT, s), false);
  s = choose(OX_POINT, s, 1, 1);                  // 1 = X (오답 아님: answer=false 니 X 가 정답)
  assert.equal(canAdvance(OX_POINT, s), true);
});

test('OX 를 맞히면 통과다', () => {
  let s = advance(OX_POINT, initTurnState());
  s = choose(OX_POINT, s, 1, 1);
  s = advance(OX_POINT, s);
  assert.equal(isPassed(OX_POINT, s), true);
});

test('OX 를 틀리면 한 번에 답이 열리고 도움받은 것으로 남는다', () => {
  let s = advance(OX_POINT, initTurnState());
  s = choose(OX_POINT, s, 1, 0);                  // 0 = O (틀림)
  const a = visibleTurns(OX_POINT, s)[1];
  assert.equal(a.solved, true, 'OX 는 두 번 고를 것이 없다 — 한 번에 열린다');
  assert.equal(a.assisted, true);
  assert.equal(isPassed(OX_POINT, advance(OX_POINT, s)), false);
});
```

- [ ] **Step 2: 테스트가 실패하는지 본다**

```bash
cd viewer && node --test src/conceptTurns.test.js
```

Expected: FAIL — OX 턴을 quiz 로 보지 않아 `canAdvance` 가 true 다.

- [ ] **Step 3: 구현한다**

`conceptTurns.js` 의 `WHO` 에 추가한다.

```js
  ox: 'ox',         // OX 지문 — 선지가 둘뿐인 quiz
```

`WHO` 아래에 추가한다.

```js
/**
 * 답을 골라야 넘어갈 수 있는 턴인가.
 * quiz(선지 여럿)와 ox(O/X 둘)를 같은 경로로 처리한다 — 진행 규칙이 같기 때문이다.
 */
export const isChoiceTurn = (t) => t && (t.who === WHO.quiz || t.who === WHO.ox);

/** OX 를 quiz 모양으로 펴서 돌려준다. 화면과 상태 기계가 같은 모양을 본다. */
export function choicesOf(turn) {
  if (!turn) return [];
  if (turn.who === WHO.quiz) return turn.choices || [];
  if (turn.who === WHO.ox) {
    return [
      { text: 'O', ok: turn.answer === true, reply: turn.reply || '' },
      { text: 'X', ok: turn.answer === false, reply: turn.reply || '' },
    ];
  }
  return [];
}
```

`canAdvance` 안의 조건을 바꾼다.

```js
  if (isChoiceTurn(cur)) return answerOf(state, state.cursor).solved;
```

`choose` 안을 바꾼다.

```js
  if (!turn || !isChoiceTurn(turn)) return state;
```

같은 함수의 `const ok = ...` 와 `const solved = ...` 를 바꾼다.

```js
  const ok = !!choicesOf(turn)[choiceIndex]?.ok;
  // OX 는 고를 것이 둘뿐이라 한 번 틀리면 남는 선택이 정답 하나다. 두 번 시도가 의미 없다.
  const maxTries = turn.who === WHO.ox ? 1 : MAX_TRIES;
  const solved = ok || picked.length >= maxTries;
```

`retry` 안을 바꾼다.

```js
  if (!turn || !isChoiceTurn(turn)) return state;
```

`isPassed` 와 `passDetail` 의 `t.who === WHO.quiz` 를 `isChoiceTurn(t)` 로 바꾼다(두 곳).

- [ ] **Step 4: 테스트가 통과하는지 본다**

```bash
cd viewer && node --test src/conceptTurns.test.js
```

Expected: PASS — 기존 21 + 신규 3

- [ ] **Step 5: 화면이 OX 를 그리게 한다**

`ConceptScene.jsx` 의 import 에 `choicesOf, isChoiceTurn` 을 더한다.

`streamItems` 안의 `const isQuiz = turn.who === WHO.quiz;` 를 바꾼다.

```js
    const isQuiz = isChoiceTurn(turn);
```

`openQuiz` 계산을 바꾼다.

```jsx
  const openQuiz = last && isChoiceTurn(last.turn) ? last : null;
```

`quizSay` 안의 `const choices = turn.choices || [];` 를 바꾼다.

```js
  const choices = choicesOf(turn);
```

`ChoiceDock` 안의 `const choices = item.turn.choices || [];` 를 바꾼다.

```jsx
  const choices = choicesOf(item.turn);
  const isOx = item.turn.who === WHO.ox;
```

같은 컴포넌트의 `<div className="cs-choices" ...>` 를 바꾼다.

```jsx
    <div className={`cs-choices${isOx ? ' is-ox' : ''}`} role="group" aria-label="선택지">
```

그리고 번호 칸을 OX 에서는 감춘다.

```jsx
            {!isOx && <span className="cs-choice-no">{'①②③④⑤⑥'[i] || i + 1}</span>}
```

- [ ] **Step 6: OX 도크 CSS 를 넣는다**

```css
/* OX 는 선지가 둘뿐이라 가로로 크게 — 시안 330:126 */
.cs-choices.is-ox { flex-direction: row; gap: var(--space-2); }
.cs-choices.is-ox .cs-choice {
  flex: 1 1 0;
  justify-content: center;
  min-height: 56px;
  font-size: var(--text-lg);
  font-weight: var(--weight-medium);
}
.cs-choices.is-ox .cs-choice-text { flex: 0 0 auto; }
.cs-choices.is-ox + .cs-choice-hint { margin-top: 6px; }
```

`.cs-choices.is-ox` 아래 자식인 힌트·조작 줄이 가로로 눕지 않도록, `ChoiceDock` 의 힌트와 `cs-choice-ops` 는 `cs-choices` 밖으로 빼지 말고 그대로 두되 CSS 로 폭을 준다.

```css
.cs-choices.is-ox .cs-choice-hint,
.cs-choices.is-ox .cs-choice-ops { flex: 1 0 100%; }
```

- [ ] **Step 7: 손으로 만든 트랙으로 확인한다**

임시로 아무 관의 `*.basic.json` 한 논점에 OX 턴을 끼워 넣고(작업 뒤 되돌린다) 브라우저에서 본다.

```bash
cd /Users/hanjiho/Documents/감정평가사\ 기출문제
python3 - <<'PY'
import json, glob
p = sorted(glob.glob('viewer/public/data/study/economics/lectures/track/*.basic.json'))[0]
d = json.load(open(p, encoding='utf-8'))
pt = d['leaves'][0]['points'][0]
pt['turns'].insert(1, {'who': 'ox', 'prompt': '「경제학은 희소성을 다루지 않는다」',
                       'answer': False, 'reply': '희소성이 경제학의 출발점입니다.'})
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print('임시 OX 삽입:', p)
PY
```

확인할 것: 하단에 **O / X 큰 버튼 둘**이 가로로 선다 · 틀리면 한 번에 정답이 열린다 · 맞히면 다음으로 넘어간다.

확인 뒤 되돌린다.

```bash
git checkout viewer/public/data/study/economics/lectures/track/
```

- [ ] **Step 8: 커밋**

```bash
git add viewer/src/conceptTurns.js viewer/src/conceptTurns.test.js viewer/src/ConceptScene.jsx viewer/src/index.css
git commit -m "feat(개념 완성): OX 턴 — 선지 둘짜리 quiz 로 같은 경로에 태운다"
```

---

## Task 12: 서술 인출 턴

**Files:**
- Modify: `viewer/src/conceptTurns.js`
- Modify: `viewer/src/conceptTurns.test.js`
- Modify: `viewer/src/ConceptScene.jsx`
- Modify: `viewer/src/index.css`

**Interfaces:**
- Consumes: 기존 상태 기계
- Produces: 턴 `{ who: 'recall', prompt, answer, hint }` 와 상태 기계 함수 `submitRecall(point, state, turnIndex, text)` · `gradeRecall(point, state, turnIndex, verdict)`. `verdict` 는 `'right' | 'partial' | 'wrong'`.

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`conceptTurns.test.js` 끝에 붙인다.

```js
// ── 서술 인출 — 백지에서 꺼내 쓰기 ────────────────────────────────
// 고르기는 알아보기(recog)고 쓰기는 꺼내기(recall)다. 시험장에서 필요한 것은 뒤쪽이다.
const RC_POINT = {
  id: 'rc1',
  turns: [
    { who: 'teach', text: '취득원가는 셋의 합입니다.' },
    { who: 'recall', prompt: '취득원가에 들어가는 세 가지를 써보세요.', answer: '매입원가·전환원가·기타 원가' },
    { who: 'mate', text: '백지에 써 봐야 압니다.' },
  ],
};

test('쓰기 전에는 넘어갈 수 없다', () => {
  const s = advance(RC_POINT, initTurnState());
  assert.equal(canAdvance(RC_POINT, s), false);
});

test('제출하면 답이 열리지만 아직 채점 전이다', () => {
  let s = advance(RC_POINT, initTurnState());
  s = submitRecall(RC_POINT, s, 1, '매입원가, 전환원가');
  const a = visibleTurns(RC_POINT, s)[1];
  assert.equal(a.written, '매입원가, 전환원가');
  assert.equal(a.solved, false, '자기 채점을 해야 끝난다');
  assert.equal(canAdvance(RC_POINT, s), false);
});

test('스스로 맞았다고 하면 통과', () => {
  let s = advance(RC_POINT, initTurnState());
  s = submitRecall(RC_POINT, s, 1, '매입원가, 전환원가, 기타 원가');
  s = gradeRecall(RC_POINT, s, 1, 'right');
  assert.equal(canAdvance(RC_POINT, s), true);
  assert.equal(isPassed(RC_POINT, advance(RC_POINT, s)), true);
});

test('부분·틀림은 도움받은 것으로 남아 통과가 아니다', () => {
  let s = advance(RC_POINT, initTurnState());
  s = submitRecall(RC_POINT, s, 1, '매입원가');
  s = gradeRecall(RC_POINT, s, 1, 'partial');
  assert.equal(canAdvance(RC_POINT, s), true, '넘어갈 수는 있어야 한다');
  assert.equal(isPassed(RC_POINT, advance(RC_POINT, s)), false);
});

test('빈 답은 제출되지 않는다', () => {
  let s = advance(RC_POINT, initTurnState());
  const before = s;
  s = submitRecall(RC_POINT, s, 1, '   ');
  assert.equal(s, before);
});
```

`import` 줄에 `submitRecall, gradeRecall` 을 더한다.

- [ ] **Step 2: 테스트가 실패하는지 본다**

```bash
cd viewer && node --test src/conceptTurns.test.js
```

Expected: FAIL — `submitRecall is not a function`

- [ ] **Step 3: 구현한다**

`conceptTurns.js` 의 `WHO` 에 추가한다.

```js
  recall: 'recall', // 서술 인출 — 백지에 써서 제출하고 스스로 채점한다
```

`isChoiceTurn` 아래에 추가한다.

```js
/** 답을 내야 넘어갈 수 있는 턴 — 고르기와 쓰기를 함께 본다. */
export const isAnswerTurn = (t) => isChoiceTurn(t) || (t && t.who === WHO.recall);

/** 백지에 쓴 답을 제출한다. 채점은 아직이다 — 정답을 펴 보인 뒤 스스로 매긴다. */
export function submitRecall(point, state, turnIndex, text) {
  const turn = turnsOf(point)[turnIndex];
  if (!turn || turn.who !== WHO.recall) return state;
  const body = String(text || '').trim();
  if (!body) return state;
  const prev = answerOf(state, turnIndex);
  if (prev.written) return state;
  return {
    ...state,
    answers: { ...state.answers, [turnIndex]: { ...prev, picked: [], written: body, solved: false } },
  };
}

/** 자기 채점. right 만 통과로 친다 — partial·wrong 은 넘어가되 도움받은 것으로 남는다. */
export function gradeRecall(point, state, turnIndex, verdict) {
  const turn = turnsOf(point)[turnIndex];
  if (!turn || turn.who !== WHO.recall) return state;
  const prev = answerOf(state, turnIndex);
  if (!prev.written || prev.solved) return state;
  const assisted = verdict !== 'right';
  return {
    ...state,
    answers: {
      ...state.answers,
      [turnIndex]: {
        ...prev, solved: true, assisted, verdict,
        everAssisted: prev.everAssisted || assisted,
      },
    },
  };
}
```

`answerOf` 의 기본값에 `written: ''` 을 더한다.

`visibleTurns` 가 `written` 과 `verdict` 를 함께 돌려주게 한다.

```js
      picked: a.picked, solved: a.solved, assisted: a.assisted,
      written: a.written || '', verdict: a.verdict || null,
      everAssisted: !!a.everAssisted,
```

`canAdvance` · `isPassed` · `passDetail` 의 `isChoiceTurn` 을 `isAnswerTurn` 으로 바꾼다(세 곳).

- [ ] **Step 4: 테스트가 통과하는지 본다**

```bash
cd viewer && node --test src/conceptTurns.test.js
```

Expected: PASS — 기존 24 + 신규 5

- [ ] **Step 5: 화면을 만든다**

`ConceptScene.jsx` 의 `ChoiceDock` 아래에 추가한다.

```jsx
// ── 서술 인출 도크 — 시안 330:309 ────────────────────────────────
// 쓰기 전에는 정답을 보여 주지 않는다. 보고 쓰면 인출이 아니다.
function RecallDock({ item, onSubmit, onGrade, onNext, nextLabel }) {
  const [text, setText] = useState('');
  const written = item.written;
  if (!written) {
    return (
      <div className="cs-recall">
        <textarea className="cs-recall-input" rows={3} value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="여기에 써보세요" aria-label="인출 답안" />
        <button type="button" className="cs-primary"
          onClick={() => onSubmit(text)} disabled={!text.trim()}>답 제출</button>
      </div>
    );
  }
  if (!item.solved) {
    return (
      <div className="cs-recall">
        <div className="cs-recall-answer">
          <span className="cs-recall-label">정답</span>
          <ParsedText text={markEmphasis(item.turn.answer || '')} />
        </div>
        <div className="cs-recall-grade">
          <button type="button" className="cs-secondary" onClick={() => onGrade('wrong')}>못 썼음</button>
          <button type="button" className="cs-secondary" onClick={() => onGrade('partial')}>일부만</button>
          <button type="button" className="cs-primary" onClick={() => onGrade('right')}>다 썼음</button>
        </div>
      </div>
    );
  }
  return (
    <button type="button" className="cs-primary" onClick={onNext}>
      {nextLabel} <ChevronRight size={16} strokeWidth={1.75} />
    </button>
  );
}
```

`openQuiz` 옆에 인출 턴을 잡는다.

```jsx
  const openRecall = last && last.turn.who === WHO.recall ? last : null;
```

도크의 분기를 셋으로 늘린다 — `{openQuiz ? (...) : (...)}` 를 이렇게 바꾼다.

```jsx
        {openQuiz
          ? (
            <ChoiceDock item={openQuiz} onPick={pick} onAgain={again}
              onNext={goForward} nextLabel={nextLabel} />
          )
          : openRecall
            ? (
              <RecallDock item={openRecall}
                onSubmit={(t) => setState((s) => submitRecall(point, s, openRecall.index, t))}
                onGrade={(v) => setState((s) => gradeRecall(point, s, openRecall.index, v))}
                onNext={goForward} nextLabel={nextLabel} />
            )
            : (
              <button type="button"
                className={finished ? 'cs-primary' : 'cs-secondary'}
                onClick={goForward}
                disabled={stuck} aria-keyshortcuts="Space ArrowRight">
                {nextLabel} <ChevronRight size={16} strokeWidth={1.75} />
              </button>
            )}
```

`streamItems` 가 인출 턴의 물음도 말풍선으로 올리게 한다 — `const text = isQuiz ? turn.prompt : turn.text;` 를 바꾼다.

```js
    const text = (isQuiz || turn.who === WHO.recall) ? turn.prompt : turn.text;
```

`import` 에 `submitRecall, gradeRecall` 을 더한다.

- [ ] **Step 6: CSS 를 넣는다**

```css
/* ── 서술 인출 — 시안 330:309 ─────────────────────────────── */
.cs-recall { display: flex; flex-direction: column; gap: var(--space-2); }
.cs-recall-input {
  width: 100%;
  padding: 12px var(--space-4);
  background: var(--sheet);
  border: 1.5px solid var(--accent);
  border-radius: 10px;
  font: inherit;
  font-size: var(--text-base);
  line-height: var(--leading-read);
  color: var(--ink);
  resize: vertical;
}
.cs-recall-input:focus { outline: none; }
.cs-recall-answer {
  padding: 12px var(--space-4);
  background: var(--sunken);
  border-radius: 10px;
  font-size: var(--text-sm);
  color: var(--ink);
}
.cs-recall-label {
  display: block;
  margin-bottom: 4px;
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  color: var(--ink-3);
}
.cs-recall-grade { display: flex; gap: var(--space-2); }
.cs-recall-grade > * { flex: 1 1 0; }
```

- [ ] **Step 7: 손으로 만든 트랙으로 확인한다**

```bash
cd /Users/hanjiho/Documents/감정평가사\ 기출문제
python3 - <<'PY'
import json, glob
p = sorted(glob.glob('viewer/public/data/study/economics/lectures/track/*.basic.json'))[0]
d = json.load(open(p, encoding='utf-8'))
pt = d['leaves'][0]['points'][0]
pt['turns'].insert(1, {'who': 'recall', 'prompt': '경제학이 다루는 근본 문제를 한 줄로 써보세요.',
                       'answer': '희소한 자원을 어떻게 배분할 것인가'})
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print('임시 인출 삽입:', p)
PY
```

확인할 것: 여러 줄 입력창과 「답 제출」이 뜬다 · 제출 전에는 정답이 안 보인다 · 제출하면 정답과 「못 썼음 / 일부만 / 다 썼음」이 뜬다 · 「다 썼음」만 통과로 잡힌다(헤더의 통과 수가 오른다).

확인 뒤 되돌린다.

```bash
git checkout viewer/public/data/study/economics/lectures/track/
```

- [ ] **Step 8: 커밋**

```bash
git add viewer/src/conceptTurns.js viewer/src/conceptTurns.test.js viewer/src/ConceptScene.jsx viewer/src/index.css
git commit -m "feat(개념 완성): 서술 인출 턴 — 백지에 쓰고 스스로 채점"
```

---

## Task 13: 인출 큐 연결과 측정 기록

**Files:**
- Modify: `viewer/src/ConceptTrack.jsx`
- Modify: `viewer/src/ConceptScene.jsx`

**Interfaces:**
- Consumes: `studyDrill` 의 `recordItem`, `measure/record.js` 의 `record`
- Produces: 없음 (부작용만)

- [ ] **Step 1: 인출·OX 결과를 큐에 올린다**

`ConceptScene.jsx` 의 `detail.done` effect 아래에 추가한다.

```jsx
  // 논점을 통과하는 순간 그 논점의 문항을 SRS 사다리에 올린다.
  // 관을 마칠 때까지 기다리면 20논점짜리 관에서 첫 논점의 복습 시점이 그만큼 밀린다.
  const queuedRef = useRef(null);
  useEffect(() => {
    if (!detail.done || !leafId || !point?.id) return;
    if (queuedRef.current === point.id) return;
    queuedRef.current = point.id;
    (point.turns || []).forEach((t, i) => {
      if (!isAnswerTurn(t)) return;
      const a = state.answers[i];
      if (!a?.solved) return;
      onQueueItem?.({
        kind: t.who === WHO.recall ? 'recall' : t.who === WHO.ox ? 'ox' : 'quiz',
        idx: `${point.id}:${i}`,
        pointId: point.id,
        q: t.prompt || '',
        isCorrect: !a.assisted && !a.everAssisted,
      });
    });
  }, [detail.done, point?.id, leafId, state.answers, onQueueItem, point?.turns]);
```

`ConceptScene` 인자에 `onQueueItem,` 을 더하고, import 에 `isAnswerTurn` 을 더한다.

- [ ] **Step 2: `ConceptTrack` 이 큐에 넣게 한다**

`ConceptTrack.jsx` 의 `<ConceptScene` 에 추가한다.

```jsx
            onQueueItem={(it) => {
              recordItem({
                kind: it.kind, idx: it.idx, q: it.q, isCorrect: it.isCorrect,
                leaf: { leafId, subject: subjectId, leafTitle: track?.title || '' },
                gradedBy: it.kind === 'recall' ? 'self' : 'machine',
                f: it.kind === 'recall' ? 'recall' : it.kind === 'ox' ? 'recall' : 'recog',
                nopt: it.kind === 'ox' ? 2 : undefined,
              });
            }}
```

import 에 `recordItem` 을 더한다.

```jsx
import { buildLearnerStatus, getAllItems, recordItem } from './studyDrill';
```

- [ ] **Step 3: 브라우저에서 확인**

Task 11·12 에서 쓴 임시 트랙을 다시 넣고 한 논점을 끝까지 푼다. 그 뒤 콘솔에서 확인한다.

```js
JSON.parse(localStorage.getItem('ailearn-items-v1'))
```

확인할 것: `kind: 'ox'` 와 `kind: 'recall'` 항목이 생겼다 · `due` 가 오늘보다 뒤다 · `leafId` 가 지금 관이다.

- [ ] **Step 4: 커밋**

```bash
git add viewer/src/ConceptScene.jsx viewer/src/ConceptTrack.jsx
git commit -m "feat(인출): 논점 통과 시점에 SRS 큐 등록 — 관 완료를 기다리지 않는다"
```

---

## Task 14: 교재 패널

**Files:**
- Create: `viewer/src/TextbookPanel.jsx`
- Modify: `viewer/src/ConceptTrack.jsx`
- Modify: `viewer/src/index.css`

**Interfaces:**
- Consumes: Task 10 의 `chunks`, Task 10 의 `askTutor`
- Produces: `TextbookPanel({ chunks, focusId, onClose, onAskAbout })`

- [ ] **Step 1: `TextbookPanel.jsx` 를 만든다**

```jsx
// 4단째 교재 패널 — 시안 334:229.
//
// 대화가 근거를 못 대면 확인할 데가 있어야 한다. 대화 열이 560 에서 약 470 으로
// 좁아지는 것을 감수하는 대신 교재와 대화를 나란히 본다.
//
// 교재 본문에도 대화와 **같은 형광펜 규칙**을 적용한다 — 노랑=공식, 보라=뒤집힘.
// 같은 색이 같은 뜻이어야 한다.
import { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import ParsedText from './ParsedText';
import { markEmphasis } from './emphasis';

export default function TextbookPanel({ chunks, focusId, onClose, onAskAbout }) {
  const ref = useRef(null);
  useEffect(() => {
    if (focusId) ref.current?.querySelector(`[data-chunk="${focusId}"]`)?.scrollIntoView({ block: 'center' });
  }, [focusId]);

  return (
    <aside className="tbook" aria-label="교재">
      <div className="tbook-head">
        <span className="tbook-label">교재</span>
        <button type="button" className="cs-tool" onClick={onClose} aria-label="닫기">
          <X size={15} strokeWidth={1.75} />
        </button>
      </div>
      <div className="tbook-body" ref={ref}>
        {chunks.length === 0 && <p className="tbook-empty">이 단원의 교재가 아직 없습니다.</p>}
        {chunks.map((c) => (
          <section key={c.id} data-chunk={c.id} className="tbook-chunk">
            <h4 className="tbook-h">{(c.path || []).join(' › ')}</h4>
            <ParsedText text={markEmphasis(c.text)} />
            {onAskAbout && (
              <button type="button" className="tbook-ask"
                onClick={() => onAskAbout(c)}>이 부분 물어보기</button>
            )}
          </section>
        ))}
      </div>
    </aside>
  );
}
```

- [ ] **Step 2: CSS 를 넣는다**

```css
/* ── 교재 패널 — 시안 334:229 ─────────────────────────────── */
.tbook {
  display: none;
  flex: 0 0 380px;
  width: 380px;
  flex-direction: column;
  min-height: 0;
  background: var(--sheet);
  border-left: 1px solid var(--line);
}
@media (min-width: 1280px) { .tbook { display: flex; } }
.tbook-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 0 0 auto;
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--line);
}
.tbook-label {
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  letter-spacing: .06em;
  color: var(--ink-3);
}
.tbook-body { flex: 1 1 auto; min-height: 0; overflow-y: auto; padding: var(--space-4); }
.tbook-chunk { padding-bottom: var(--space-5); }
.tbook-h { margin: 0 0 var(--space-2); font-size: var(--text-sm); font-weight: var(--weight-bold); color: var(--ink); }
.tbook-empty { font-size: var(--text-sm); color: var(--ink-meta); }
.tbook-ask {
  display: block;
  width: 100%;
  margin-top: var(--space-3);
  padding: 10px;
  background: var(--accent-bg);
  border: none;
  border-radius: var(--radius-md);
  color: var(--accent-ink);
  font: inherit;
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  cursor: pointer;
}
.tbook-ask:hover { filter: brightness(.97); }
```

- [ ] **Step 3: `/교재` 명령에 연결한다**

`ConceptTrack.jsx` 의 `runCommand` 안 `case '/교재':` 를 바꾼다.

```jsx
      case '/교재':
        setBook((v) => !v);
        break;
```

state 를 더한다.

```jsx
  const [book, setBook] = useState(false);
```

`workspace` 헬퍼의 `{inner}` 다음에 패널을 붙인다.

```jsx
      {inner}
      {book && (
        <TextbookPanel chunks={chunks} focusId={null}
          onClose={() => setBook(false)}
          onAskAbout={hasKey ? (c) => {
            // 교재를 읽다 막히면 그 문단을 물고 대화로 돌아간다 — 샛길의 또 다른 입구.
            const q = `교재의 「${(c.path || []).slice(-1)[0]}」 부분을 쉽게 풀어 설명해 주세요.`;
            setBook(false);
            askTutor(q).then((r) => alert(r.answer)).catch(() => {});
          } : null} />
      )}
```

import 를 더한다.

```jsx
import TextbookPanel from './TextbookPanel';
```

- [ ] **Step 4: 브라우저에서 확인**

1280 이상 폭에서 관을 열고 입력줄에 `/교재` 를 친 뒤 Enter.
확인할 것: 우측에 교재 패널이 뜬다 · 본문에 노랑·보라 형광펜이 보인다 · 대화 열이 좁아지지만 말풍선·도크가 여전히 같은 세로선에 선다 · 닫기가 동작한다.

- [ ] **Step 5: 커밋**

```bash
git add viewer/src/TextbookPanel.jsx viewer/src/ConceptTrack.jsx viewer/src/index.css
git commit -m "feat(교재): 4단째 패널 — 본문에도 같은 형광펜 규칙"
```

---

## Task 15: 암기법을 복습 메이트 대사로

**Files:**
- Create: `scripts/lectures/merge_mnemonics.py`
- Create: `scripts/lectures/test_merge_mnemonics.py`

**Interfaces:**
- Consumes: 교재 md 의 `#### 🧠 암기법` 섹션
- Produces: `{unit}.basic.json` 의 각 관 마지막 논점에 `{ who: 'mate', text }` 턴을 더한다. 이미 있으면 건너뛴다(재실행 안전).

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`scripts/lectures/test_merge_mnemonics.py`:

```python
import unittest
from merge_mnemonics import extract_mnemonics, already_has

MD = """### 1. 취득원가

본문입니다.

#### 🧠 암기법

- 취득원가 세 가지: 「매·전·기」 — 매입·전환·기타
- 매입할인은 빼는 것: 「깎으면 줄어든다」

### 2. 다음 절

본문입니다.
"""


class ExtractTest(unittest.TestCase):
    def test_암기법_항목을_뽑는다(self):
        got = extract_mnemonics(MD)
        self.assertEqual(len(got), 2)
        self.assertIn('매·전·기', got[0])

    def test_암기법_섹션이_없으면_빈_리스트(self):
        self.assertEqual(extract_mnemonics('### 절\n\n본문\n'), [])


class IdempotentTest(unittest.TestCase):
    def test_이미_있으면_다시_넣지_않는다(self):
        point = {'turns': [{'who': 'mate', 'text': '외우는 법: 「매·전·기」'}]}
        self.assertTrue(already_has(point, '외우는 법: 「매·전·기」'))
        self.assertFalse(already_has(point, '다른 말'))


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: 테스트가 실패하는지 본다**

```bash
cd scripts/lectures && python3 -m unittest test_merge_mnemonics -v
```

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: 구현한다**

`scripts/lectures/merge_mnemonics.py`:

```python
# 교재의 「🧠 암기법」을 관 마지막 복습 메이트 대사로 옮긴다.
#
# 지금은 우측 교재 패널의 별도 탭에 있어서, 논점을 다 익힌 사람이 그 탭을 따로
# 눌러야 본다. 대화 끝에 두면 익힌 직후에 만난다.
#
# 재실행 안전 — 같은 문장이 이미 있으면 건너뛴다.
import json
import os
import re
import sys

MEM_HEAD = re.compile(r'^#{3,4}\s*🧠\s*암기법\s*$', re.M)
NEXT_HEAD = re.compile(r'^#{1,4}\s', re.M)
BULLET = re.compile(r'^\s*[-*]\s+(.+?)\s*$', re.M)


def extract_mnemonics(md):
    """「🧠 암기법」 섹션의 불릿을 순서대로 돌려준다."""
    m = MEM_HEAD.search(md)
    if not m:
        return []
    rest = md[m.end():]
    nxt = NEXT_HEAD.search(rest)
    body = rest[:nxt.start()] if nxt else rest
    return [b.strip() for b in BULLET.findall(body)]


def already_has(point, text):
    for t in point.get('turns', []):
        if t.get('who') == 'mate' and t.get('text', '').strip() == text.strip():
            return True
    return False


def merge(track_path, unit_md_path):
    md = open(unit_md_path, encoding='utf-8').read()
    tips = extract_mnemonics(md)
    if not tips:
        return 0
    d = json.load(open(track_path, encoding='utf-8'))
    added = 0
    for leaf in d.get('leaves', []):
        pts = leaf.get('points') or []
        if not pts:
            continue
        last = pts[-1]
        # 관 하나에 한 줄만. 여러 줄을 몰아넣으면 마지막 말풍선이 벽이 된다.
        text = '외우는 법 — ' + tips[0]
        if already_has(last, text):
            continue
        last.setdefault('turns', []).append({'who': 'mate', 'text': text})
        added += 1
    if added:
        json.dump(d, open(track_path, 'w', encoding='utf-8'), ensure_ascii=False)
    return added


def main(subject):
    base = 'viewer/public/data/study/%s' % subject
    tdir = os.path.join(base, 'lectures', 'track')
    total = 0
    for name in sorted(os.listdir(tdir)):
        if not name.endswith('.basic.json'):
            continue
        unit = name[:-len('.basic.json')]
        md = os.path.join(base, 'units', unit + '.md')
        if not os.path.exists(md):
            print('건너뜀(교재 없음): %s' % unit)
            continue
        n = merge(os.path.join(tdir, name), md)
        print('%s → %d관에 추가' % (unit, n))
        total += n
    print('합계 %d관' % total)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'economics')
```

- [ ] **Step 4: 테스트가 통과하는지 본다**

```bash
cd scripts/lectures && python3 -m unittest test_merge_mnemonics -v
```

Expected: PASS — 3 tests

- [ ] **Step 5: 실제로 돌리고 두 번째 실행이 무해한지 본다**

```bash
cd /Users/hanjiho/Documents/감정평가사\ 기출문제
python3 scripts/lectures/merge_mnemonics.py economics
python3 scripts/lectures/merge_mnemonics.py economics   # 두 번째 — 「0관에 추가」여야 한다
cd viewer && npm run sync-data
```

Expected: 첫 실행은 관 수만큼 추가, 두 번째는 전부 0.

- [ ] **Step 6: 브라우저에서 확인**

관을 끝까지 진행해 마지막 논점의 마지막 대사가 「외우는 법 — …」인지 본다.

- [ ] **Step 7: 커밋**

```bash
git add scripts/lectures/merge_mnemonics.py scripts/lectures/test_merge_mnemonics.py viewer/public/data/study/economics/lectures/track
git commit -m "feat(개념 완성): 암기법을 관 마지막 복습 메이트 대사로"
```

---

## Task 16: sync-data 가 청크를 옮기게 한다

**Files:**
- Modify: `viewer/scripts/sync-data.mjs`

**Interfaces:**
- Consumes: Task 5 가 만드는 `rag/` 디렉터리
- Produces: 없음

- [ ] **Step 1: 지금 무엇을 옮기는지 본다**

```bash
cd viewer && grep -n "study\|copy" scripts/sync-data.mjs | head -20
```

- [ ] **Step 2: `rag` 를 목록에 더한다**

`sync-data.mjs` 에서 `study/{subject}` 하위를 옮기는 목록(예: `['units', 'problems', 'lectures']`)을 찾아 `'rag'` 를 더한다. 목록이 없고 디렉터리 전체를 옮기는 구조라면 이 태스크는 **아무 것도 고치지 않고** Step 3 로 간다.

- [ ] **Step 3: 확인한다**

```bash
cd viewer && npm run sync-data && ls public/data/study/economics/rag/ | head -3
```

Expected: 청크 파일이 있다.

- [ ] **Step 4: 커밋**

변경이 있었을 때만.

```bash
git add viewer/scripts/sync-data.mjs
git commit -m "chore(sync-data): RAG 청크 디렉터리 동기화 대상에 포함"
```

---

## Task 17: 1차는 새 3탭으로, 2차는 그대로 — 그리고 `/쉽게`

**Files:**
- Modify: `viewer/src/App.jsx`
- Modify: `viewer/src/ConceptTrack.jsx`

**Interfaces:**
- Consumes: Task 10 의 `askTutor`
- Produces: 없음

스펙 §6-1 이 요구하는 갈라짐이다. 1차 과목은 새 3탭만 쓰고, 2차 과목(답안·양식·논점·실전이 필요한 곳)은 `AILearning.jsx` 를 그대로 쓴다. **`AILearning.jsx` 를 깎지 않는다** — 깎으면 2차 기능이 함께 사라진다.

- [ ] **Step 1: 1차에서 심화로 나가던 길을 끊는다**

`ConceptTrack.jsx` 의 `runCommand` 안 `case '/쉽게':` 를 바꾼다. 지금은 `onOpenDeep` 으로 `AILearning` 화면에 넘기는데, 이제 샛길이 그 일을 한다.

```jsx
      case '/쉽게':
        // 「더 쉽게」는 지금 논점을 벗어날 이유가 없다. 샛길로 그 자리에서 묻는다.
        askSideFromTrack('방금 설명을 더 쉬운 말로 다시 해 주세요.');
        break;
```

- [ ] **Step 2: `ConceptTrack` 이 샛길 전송을 부를 수 있게 한다**

`ConceptScene` 안에만 있던 `askSide` 를 밖에서도 부르려면 ref 가 필요하다. `ConceptTrack.jsx` 에 추가한다.

```jsx
  // 「/쉽게」가 ConceptScene 안의 샛길 전송을 부른다.
  const sceneRef = useRef(null);
  const askSideFromTrack = (q) => sceneRef.current?.askSide?.(q);
```

`<ConceptScene` 에 `ref={sceneRef}` 를 더한다.

- [ ] **Step 3: `ConceptScene` 이 `askSide` 를 밖에 연다**

`ConceptScene.jsx` 의 import 에 `useImperativeHandle, forwardRef` 를 더하고, 선언을 바꾼다.

```jsx
const ConceptScene = forwardRef(function ConceptScene({
  point, seq, total, leafId, onPassed, onDone, onNext, onAsk, onAskSide, onCommand, onQueueItem,
}, ref) {
```

`askSide` 정의 아래에 추가한다.

```jsx
  // 「/쉽게」 같은 슬래시 명령이 밖에서 샛길을 열 수 있게 한다.
  useImperativeHandle(ref, () => ({ askSide }), [askSide]);
```

파일 끝의 `}` 뒤에 추가한다.

```jsx
export default ConceptScene;
```

그리고 기존 `export default function ConceptScene(` 의 `export default` 를 지운다.

- [ ] **Step 4: 1차 과목이 AILearning 으로 새지 않게 한다**

`App.jsx` 의 `if (currentView === 'civil') {` 블록 맨 앞에 추가한다.

```jsx
    // 1차 과목은 새 3탭(개념 완성·기출 분석·심화)만 쓴다. AILearning 은 2차 전용이다.
    // 깎지 않고 남겨 둔다 — 답안·양식·논점·실전은 2차에 아직 필요하다(스펙 §6-1·§12).
    const cur = getAiCurrent?.() || {};
    const meta = AI_SUBJECTS.find((x) => x.id === cur.subject);
    if (meta && meta.stage === 1) {
      setCurrentView('concept');
      return null;
    }
```

`getAiCurrent` 가 import 돼 있지 않으면 `aiLearningStore` 에서 가져온다. 이름이 다르면 그 파일의 실제 export 를 쓴다.

```bash
grep -n "^export function getCurrent" viewer/src/aiLearningStore.js
```

- [ ] **Step 5: 브라우저에서 확인**

1. 경제학(1차) 관에서 `/쉽게` 를 친다 → **샛길이 열리고** AILearning 화면으로 나가지 않는다
2. 감정평가실무(2차)를 고르면 **기존 AILearning 화면**이 그대로 뜬다
3. 1차 과목에서 예전 경로로 `civil` 뷰에 들어가려 해도 3탭 화면으로 돌아온다

- [ ] **Step 6: 커밋**

```bash
git add viewer/src/App.jsx viewer/src/ConceptScene.jsx viewer/src/ConceptTrack.jsx
git commit -m "feat(AI 학습): 1차는 3탭으로, 2차는 AILearning 그대로 — /쉽게는 샛길로"
```

---

## 마무리 검증

- [ ] **전체 테스트**

```bash
cd viewer && node --test src/*.test.js src/rag/*.test.js
cd ../scripts/lectures && python3 -m unittest discover -p 'test_*.py' -v
```

Expected: 전부 통과.

- [ ] **빌드**

```bash
cd viewer && npx --no-install vite build
```

Expected: 에러 없음.

- [ ] **두 폭에서 눈으로**

1280 과 390 에서 다음을 확인한다.

1. 탭 셋이 보이고 전환된다
2. 개념 완성 대화가 예전처럼 진행된다
3. 샛길이 파란 면 + 「AI」 표식으로 구분되고 「돌아가기」가 자리를 지킨다
4. 심화 탭에서 키가 없으면 안내, 있으면 약점 카드와 대화
5. 말풍선·그림·선택지·버튼·입력창이 같은 세로선(560px)에 선다
6. 진행 바가 한 덩이다
7. 정답률이 없는 절의 칸이 비어 있다(`—` 없음)

---

## 이 계획이 다루지 않는 것

- **기출 720문항 저작**(스펙 §11 의 8단계). 이 계획이 끝나 `{unit}.exam.json` 을 읽는 화면이 선 뒤 계획 ②로 쓴다.
- **OX 507지문을 논점에 붙이는 작업.** Task 11 은 OX 턴을 **그릴 수 있게** 만들 뿐이고, 어느 논점 뒤에 붙일지 정하는 것은 저작이라 계획 ②에 넣는다.
- **기출 딥링크 카드**(스펙 §5-2). `point_ref` 가 있는 exam 트랙이 있어야 만들 수 있어 계획 ②로 미룬다.
- **`/기출` 명령**(스펙 §6-6) — 심화 대화에서 그 문항을 기출 분석 탭으로 가져오는 것.
  역시 exam 트랙이 있어야 하므로 계획 ②로 미룬다.
- **「같은 자리를 물은 기출」 카드**(스펙 §6-6). 위와 같은 이유.
- **2차 시험 과목.** `AILearning.jsx` 는 그대로 둔다(스펙 §12).
