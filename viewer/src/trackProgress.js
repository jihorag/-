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
