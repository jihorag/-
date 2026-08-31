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
  ox: 'ox',         // OX 지문 — 선지가 둘뿐인 quiz
  recall: 'recall', // 서술 인출 — 백지에 써서 제출하고 스스로 채점한다
};

/**
 * 답을 골라야 넘어갈 수 있는 턴인가.
 * quiz(선지 여럿)와 ox(O/X 둘)를 같은 경로로 처리한다 — 진행 규칙이 같기 때문이다.
 */
export const isChoiceTurn = (t) => t && (t.who === WHO.quiz || t.who === WHO.ox);

/** 답을 내야 넘어갈 수 있는 턴 — 고르기와 쓰기를 함께 본다. */
export const isAnswerTurn = (t) => isChoiceTurn(t) || (t && t.who === WHO.recall);

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

// 두 번 틀리면 정답을 열어 준다. 막히면 학습이 거기서 멈추기 때문이다.
// 대신 assisted 로 남겨 "스스로 맞힌 것"과 구분한다 — 통과 판정에 쓴다.
const MAX_TRIES = 2;

const turnsOf = (point) => (Array.isArray(point?.turns) ? point.turns : []);

export function initTurnState() {
  return { cursor: 0, answers: {} };
}

function answerOf(state, i) {
  return state.answers[i] || { picked: [], solved: false, assisted: false, everAssisted: false, written: '' };
}

/** 지금까지 열린 턴들. 각 항목에 그 턴의 응답 상태를 붙여 돌려준다. */
export function visibleTurns(point, state) {
  const turns = turnsOf(point);
  if (!turns.length) return [];
  const last = Math.min(state.cursor, turns.length - 1);
  const out = [];
  for (let i = 0; i <= last; i += 1) {
    const a = answerOf(state, i);
    out.push({
      turn: turns[i], index: i,
      picked: a.picked, solved: a.solved, assisted: a.assisted,
      written: a.written || '', verdict: a.verdict || null,
      everAssisted: !!a.everAssisted,
    });
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
  if (isAnswerTurn(cur)) return answerOf(state, state.cursor).solved;
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
  if (!turn || !isChoiceTurn(turn)) return state;
  const prev = answerOf(state, turnIndex);
  if (prev.solved) return state;
  if (prev.picked.includes(choiceIndex)) return state;

  const picked = prev.picked.concat(choiceIndex);
  const ok = !!choicesOf(turn)[choiceIndex]?.ok;
  // 정답을 골랐으면 스스로 푼 것. 시도를 다 썼으면 열어 주되 도움받은 것으로 남긴다.
  // OX 는 고를 것이 둘뿐이라 한 번 틀리면 남는 선택이 정답 하나다. 두 번 시도가 의미 없다.
  const maxTries = turn.who === WHO.ox ? 1 : MAX_TRIES;
  const solved = ok || picked.length >= maxTries;
  const assisted = !ok && solved;

  return {
    ...state,
    answers: {
      ...state.answers,
      // everAssisted 는 다시 풀어도 남는다 — retry 주석 참조.
      [turnIndex]: { picked, solved, assisted, everAssisted: prev.everAssisted || assisted },
    },
  };
}

/**
 * 그 quiz 를 다시 푼다 — 시안의 「다시 풀어보기」.
 *
 * 고른 것만 지우고 **도움받았다는 사실은 지우지 않는다**(everAssisted). 지우면
 * 두 번 틀려 답을 본 사람이 곧바로 다시 눌러 「스스로 맞힘」으로 바꿀 수 있고,
 * 그러면 통과율이 실력이 아니라 재시도 횟수를 재게 된다. 다시 보는 것은 자유롭게,
 * 점수는 처음 것으로.
 */
export function retry(point, state, turnIndex) {
  const turns = turnsOf(point);
  const turn = turns[turnIndex];
  if (!turn || !isChoiceTurn(turn)) return state;
  const prev = answerOf(state, turnIndex);
  if (!prev.solved) return state;
  return {
    ...state,
    answers: {
      ...state.answers,
      [turnIndex]: {
        picked: [], solved: false, assisted: false,
        everAssisted: prev.everAssisted || prev.assisted,
      },
    },
  };
}

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

/** 통과 = 모든 quiz 를 스스로 맞혔다. quiz 가 없는 옛 논점은 끝까지 간 것으로 갈음한다. */
export function isPassed(point, state) {
  const turns = turnsOf(point);
  if (!turns.length) return false;
  const quizIdx = turns.map((t, i) => (isAnswerTurn(t) ? i : -1)).filter((i) => i >= 0);
  if (!quizIdx.length) return atEnd(point, state);
  return quizIdx.every((i) => {
    const a = answerOf(state, i);
    return a.solved && !a.assisted && !a.everAssisted;
  });
}

/**
 * 측정 계약에 넘길 상세. isPassed 가 버리는 것을 살린다.
 *
 * isPassed 는 "스스로 다 맞혔는가"만 답하므로, 두 번 틀려 답을 연 경우(assisted)에는
 * false 가 되어 그 시도가 통째로 기록되지 않는다. 여기서는 통과 여부와 별개로
 * "모든 quiz 를 끝냈는가(done)"와 "그중 몇 개를 스스로 맞혔는가(score)"를 돌려준다.
 *
 * quiz 가 없는 옛 논점은 채점 근거가 없다 — score 는 null 이고, 계약에서는 g:'none' 이다.
 */
export function passDetail(point, state) {
  const turns = turnsOf(point);
  const quizIdx = turns.map((t, i) => (isAnswerTurn(t) ? i : -1)).filter((i) => i >= 0);
  const quizCount = quizIdx.length;

  let solvedCount = 0, selfCount = 0, assistedCount = 0, tries = 0;
  for (const i of quizIdx) {
    const a = answerOf(state, i);
    tries += a.picked.length;
    if (a.solved) {
      solvedCount += 1;
      if (a.assisted || a.everAssisted) assistedCount += 1; else selfCount += 1;
    }
  }
  const done = quizCount > 0 && solvedCount === quizCount;
  return {
    quizCount, solvedCount, selfCount, assistedCount, tries,
    done,
    score: quizCount ? selfCount / quizCount : null,
  };
}
