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
