// 문항 단위 학습 기록 — OX·계산 연습·와꾸의 정오를 남기고 인출 큐를 만든다.
//
// 왜 필요한가: 교재에 OX 8,260지문·계산 연습 1,374문항·와꾸 260개가 있는데
// 지금까지는 "몇 개를 열어봤나"만 알 뿐 맞았는지 틀렸는지는 아무도 몰랐다.
// aiLearningStore 의 SRS 엔진(recordGrade/getDueChapters)은 기출 풀이에만 물려 있었다.
// 여기서 문항 단위로 기록하고, 관(章) 단위 숙련도에도 흘려보낸다.

import { recordGrade } from './aiLearningStore';

const KEY = 'ailearn-items-v1';
const DAY = 86400000;
// 틀리면 처음으로, 맞히면 한 칸씩 — 1일 → 3일 → 7일 → 16일 → 35일 (시험일 미등록 시 폴백)
const LADDER = [1, 3, 7, 16, 35];
// 학습과학 근거(Cepeda 2006/2008): 복습 간격은 고정이 아니라 '시험까지 남은 기간(RI)'에 비례해야 한다.
// 최적 간격 ≈ RI의 10~20%. 숙련도(box)가 오를수록 비율을 키우되 시험 전에 마지막 복습이 들어오게 캡한다.
const GAP_PROP = [0.05, 0.09, 0.14, 0.20, 0.28]; // box별 RI 대비 복습 간격 비율

// 가장 임박한 미래 시험까지 남은 일수(없으면 null) — quiz-exam-dates에서 읽음
function remainingToExam() {
  try {
    const ed = JSON.parse(localStorage.getItem('quiz-exam-dates') || '{}') || {};
    const now = Date.now();
    const days = Object.values(ed)
      .map((s) => { const d = new Date(s + 'T00:00:00').getTime(); return isNaN(d) ? null : Math.ceil((d - now) / DAY); })
      .filter((x) => x != null && x > 0);
    return days.length ? Math.min(...days) : null;
  } catch { return null; }
}
// box(숙련도)에 맞는 다음 복습 간격(일). 시험일이 있으면 RI 비례, 없으면 고정 사다리.
function nextGapDays(box) {
  const R = remainingToExam();
  if (R && R > 1) return Math.max(1, Math.min(Math.round(R * GAP_PROP[box]), R - 1));
  return LADDER[box];
}

// 드릴 체화(회독)용 — box(회독 숙련도)에 맞는 다음 복습 도래 시각. 시험일 비례 간격(RI×10~20%)을 그대로 쓴다.
export function drillReviewDue(box) {
  const b = Math.max(0, Math.min(box || 0, GAP_PROP.length - 1));
  return Date.now() + nextGapDays(b) * DAY;
}

function load() {
  try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch { return {}; }
}
function save(v) {
  try { localStorage.setItem(KEY, JSON.stringify(v)); } catch { /* 용량 초과 등은 조용히 무시 */ }
}

// 렌더러(ParsedText) 안쪽 깊은 곳에서도 "지금 어느 관을 보고 있는지" 알아야 한다.
// props 로 내리려면 ParsedText 전체를 훑어야 해서, 화면당 하나뿐인 값은 모듈 상태로 둔다.
let active = null;
export function setActiveLeaf(info) { active = info || null; }
export function getActiveLeaf() { return active; }

export const itemKey = (leafId, kind, idx) => `${leafId}::${kind}::${idx}`;

/** 한 문항의 정오를 기록한다. 관 단위 숙련도(recordGrade)에도 반영된다. */
export function recordItem({ kind, idx, q, isCorrect, leaf }) {
  const a = leaf || active;
  if (!a?.leafId) return null;
  const all = load();
  const k = itemKey(a.leafId, kind, idx);
  const prev = all[k] || { attempted: 0, correct: 0, box: 0 };
  const box = isCorrect ? Math.min(LADDER.length - 1, (prev.box || 0) + 1) : 0;
  const next = {
    subject: a.subject, leafId: a.leafId, leafTitle: a.leafTitle || '',
    kind, idx, q: (q || prev.q || '').slice(0, 400),
    attempted: (prev.attempted || 0) + 1,
    correct: (prev.correct || 0) + (isCorrect ? 1 : 0),
    lastCorrect: !!isCorrect,
    last: Date.now(),
    box,
    due: Date.now() + nextGapDays(box) * DAY, // 시험일에 비례한 간격(RI×10~20%), 미등록 시 사다리
  };
  all[k] = next;
  save(all);
  try { recordGrade(a.leafId, !!isCorrect); } catch { /* 관 단위 반영 실패는 치명적이지 않다 */ }
  return next;
}

/** 특정 관의 문항 성적 요약 */
export function getLeafItemStats(leafId) {
  const all = load();
  let attempted = 0, correct = 0, wrong = 0;
  Object.values(all).forEach((it) => {
    if (it.leafId !== leafId) return;
    attempted += 1;
    if (it.lastCorrect) correct += 1; else wrong += 1;
  });
  return { attempted, correct, wrong, accuracy: attempted ? correct / attempted : 0 };
}

export function getAllItems() { return Object.values(load()); }

/**
 * 오늘의 인출 큐.
 * ① 마지막에 틀린 문항  ② 복습 만기가 지난 문항  순으로 채운다.
 * 오래 방치된 것부터 나오게 정렬한다.
 */
export function getDrillQueue(limit = 20, now = Date.now()) {
  const items = getAllItems();
  const wrong = items.filter((i) => !i.lastCorrect);
  const due = items.filter((i) => i.lastCorrect && (i.due || 0) <= now);
  const by = (a, b) => (a.due || 0) - (b.due || 0);
  wrong.sort(by); due.sort(by);
  return [...wrong, ...due].slice(0, limit);
}

export function getDrillCounts(now = Date.now()) {
  const items = getAllItems();
  return {
    wrong: items.filter((i) => !i.lastCorrect).length,
    due: items.filter((i) => i.lastCorrect && (i.due || 0) <= now).length,
    total: items.length,
  };
}

/** AI 시스템 프롬프트에 넣을 학습 상태 요약 — 교재만 보던 AI에게 성적을 알려 준다. */
export function buildLearnerStatus(leafId, leafTitle) {
  const items = getAllItems();
  if (!items.length) return '';
  const lines = [];
  const cur = items.filter((i) => i.leafId === leafId);
  if (cur.length) {
    const w = cur.filter((i) => !i.lastCorrect);
    const acc = Math.round((cur.filter((i) => i.lastCorrect).length / cur.length) * 100);
    lines.push(`[이 관 성적] ${leafTitle || leafId} — ${cur.length}문항 풀이, 정답률 ${acc}%`);
    if (w.length) {
      lines.push(`[이 관에서 최근 틀린 문항 ${w.length}개]`);
      w.slice(0, 5).forEach((i) => lines.push(`  - (${i.kind === 'ox' ? 'OX' : i.kind === 'journal' ? '분개' : '계산'}) ${i.q.slice(0, 120)}`));
    }
  }
  const c = getDrillCounts();
  if (c.wrong || c.due) lines.push(`[전체] 오답 ${c.wrong}개 · 복습 만기 ${c.due}개 대기 중`);
  if (!lines.length) return '';
  return ['', '## 학습자 성적 (이 정보를 활용해 약한 곳부터 짚어라)', ...lines].join('\n');
}

export function resetItems() { save({}); }
