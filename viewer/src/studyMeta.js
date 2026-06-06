// 합격 수기 기반 학습 메타 기능 저장소 (localStorage)
//  · 과목별 목표점수·버리기 단원 (전략 보드)
//  · 회독/암기 소요시간 로그 (메타인지 타이머)
//  · 검산으로 잡은 실수 카운터 (검산 트레이너)

const lsGet = (key, fallback) => {
  try { const v = localStorage.getItem(key); return v == null ? fallback : JSON.parse(v); }
  catch { return fallback; }
};
const lsSet = (key, val) => { try { localStorage.setItem(key, JSON.stringify(val)); } catch { /* noop */ } };

// ── 전략 보드: 과목별 목표점수 + 버리기 단원 ──
const PLAN_KEY = 'study-plan-v1';
export function getStudyPlan() {
  const p = lsGet(PLAN_KEY, {});
  return { targets: p.targets || {}, abandoned: p.abandoned || {} }; // targets:{[subj]:점수}, abandoned:{[subj]:[라벨]}
}
export function setSubjectTarget(subject, score) {
  const p = getStudyPlan();
  p.targets = { ...p.targets, [subject]: score };
  lsSet(PLAN_KEY, p); return p;
}
export function addAbandoned(subject, label) {
  const p = getStudyPlan();
  const cur = p.abandoned[subject] || [];
  if (label && !cur.includes(label)) p.abandoned = { ...p.abandoned, [subject]: [...cur, label] };
  lsSet(PLAN_KEY, p); return p;
}
export function removeAbandoned(subject, label) {
  const p = getStudyPlan();
  p.abandoned = { ...p.abandoned, [subject]: (p.abandoned[subject] || []).filter((x) => x !== label) };
  lsSet(PLAN_KEY, p); return p;
}

// ── 메타인지 타이머: 회독/암기 소요시간 로그 ──
const TIMER_KEY = 'round-timer-logs-v1';
export function getTimerLogs() { return lsGet(TIMER_KEY, []); }
export function addTimerLog({ label, ms, items }) {
  const logs = getTimerLogs();
  logs.push({ label: label || '회독', ms, items: items || 0, ts: Date.now() });
  lsSet(TIMER_KEY, logs.slice(-40)); // 최근 40개
  return logs;
}
export function clearTimerLogs() { lsSet(TIMER_KEY, []); }

// ── 셀프진단 신뢰도 라벨 (문항별 '안다/애매/모른다') ──
const CONF_KEY = 'q-confidence-v1';
export function getConfidence(id) { return lsGet(CONF_KEY, {})[id] || null; }
export function setConfidence(id, val) {
  const m = lsGet(CONF_KEY, {});
  if (val) m[id] = val; else delete m[id];
  lsSet(CONF_KEY, m); return val;
}
export function getConfidenceMap() { return lsGet(CONF_KEY, {}); }

// ── 검산 트레이너: 검산 시도/실수 적발 카운터 ──
const GYEOMSAN_KEY = 'gyeomsan-stats-v1';
export function getGyeomsanStats() { return lsGet(GYEOMSAN_KEY, { checks: 0, caught: 0 }); }
export function bumpGyeomsan(caught) {
  const s = getGyeomsanStats();
  const next = { checks: s.checks + 1, caught: s.caught + (caught ? 1 : 0) };
  lsSet(GYEOMSAN_KEY, next); return next;
}
