// 학습상태 집계 — 앱이 이미 수집 중인 기록(기출 정오·AI 커버리지·SRS)을 leafStats.getLeafState로
// 단원(leaf) 단위로 계산하고, 과목별로 요약한다. 계획 엔진이 "어디까지 공부했는지"를 알게 하는 층.
//
// 반환(과목별):
//   { total, active, mastered, progressPct, coveredPct, avgAccuracy, lastStudied,
//     due:[state], weak:[state], next:[state] }   // state = getLeafState 결과(leaf 포함)

import { getLeafState } from './leafStats';

export const leafLabel = (leaf) => {
  if (!leaf) return '';
  if (Array.isArray(leaf.path) && leaf.path.length) return leaf.path[leaf.path.length - 1];
  return leaf.title || leaf.id || '';
};

const WEAK_SCORE = 0.7; // 종합 점수 이보다 낮으면 '약점'

/**
 * @param {{leavesBySubject:object, classifiedList:array, progress:object, qidFn:function, mastery:object}} ctx
 */
export function buildSubjectState(ctx) {
  const { leavesBySubject = {}, classifiedList = [], progress = {}, qidFn, mastery = {} } = ctx || {};
  const lctx = { classifiedList, progress, qidFn, mastery };
  const out = {};
  for (const sid of Object.keys(leavesBySubject)) {
    const leaves = leavesBySubject[sid] || [];
    if (!leaves.length) continue;
    let active = 0, mastered = 0, accSum = 0, accN = 0, lastStudied = 0;
    const due = [], weak = [], next = [];
    // 커리큘럼 순서 유지(leaves 배열 순서 = 학습 순서)
    for (const leaf of leaves) {
      const st = getLeafState(leaf, lctx);
      if (!st) continue;
      if (st.is_active) active++;
      if (st.is_mastered) mastered++;
      if (st.quiz.answered > 0) { accSum += st.quiz.accuracy; accN++; }
      const ls = st.ai.last_studied ? new Date(st.ai.last_studied).getTime() : 0;
      if (ls > lastStudied) lastStudied = ls;
      if (st.needs_review) due.push(st);
      else if (st.is_active && !st.is_mastered && st.score < WEAK_SCORE) weak.push(st);
      else if (!st.is_active) next.push(st);
    }
    // 복습: 가장 급한 것 먼저(도래 문항 수 + AI 도래)
    due.sort((a, b) => (b.quiz.due + (b.ai.is_due ? 1 : 0)) - (a.quiz.due + (a.ai.is_due ? 1 : 0)));
    // 약점: 점수 낮은 순
    weak.sort((a, b) => a.score - b.score);
    // next: 커리큘럼 순서 그대로(앞쪽 = 다음에 볼 것)
    const total = leaves.length;
    out[sid] = {
      total, active, mastered,
      progressPct: total ? Math.round((mastered / total) * 100) : 0,
      coveredPct: total ? Math.round((active / total) * 100) : 0,
      avgAccuracy: accN ? Math.round((accSum / accN) * 100) : null,
      lastStudied: lastStudied || null,
      due, weak, next,
    };
  }
  return out;
}

// 전 과목 복습 도래 총량(오늘 복습 큐 크기) — 상시 표시용
export function totalDue(subjectState) {
  return Object.values(subjectState || {}).reduce((n, s) => n + (s.due ? s.due.length : 0), 0);
}
