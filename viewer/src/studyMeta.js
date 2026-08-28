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

// ── 오답 원인 태그 (문항별 다중 태그) ──
// 합격수기: "기출 반복만 하면 '안다는 착각' → 회계 과락". 왜 틀렸는지 유형화해야
// 처방이 나온다("자릿수에서 3번 틀림"). 검산 boolean 카운터로는 부족.
const MISTAKE_KEY = 'q-mistake-v1'; // { [qid]: { s: subject, t: [type…], ts } }
export const MISTAKE_TYPES = [
  { key: 'concept', label: '개념 오해', icon: '🧩' },   // 정의·법리를 잘못 앎
  { key: 'misread', label: '문제 오독', icon: '👓' },   // 지문·조건·함정 놓침 (옳은것↔틀린것 등)
  { key: 'forgot',  label: '인출 실패', icon: '🕳' },    // 알았는데 안 떠오름 (조문·판례·정의)
  { key: 'formula', label: '공식 오적용', icon: '📐' }, // 계산: 식 자체를 틀림
  { key: 'sign',    label: '부호·방향', icon: '±' },    // 계산: 부호·증감·대소
  { key: 'calc',    label: '자릿수·계산', icon: '🔢' }, // 계산: 단순 산수·단위
];
export function getMistake(id) { return lsGet(MISTAKE_KEY, {})[id] || null; }
export function toggleMistake(id, subject, type) {
  const m = lsGet(MISTAKE_KEY, {});
  const e = m[id] || { s: subject || '', t: [] };
  const cur = new Set(e.t);
  if (cur.has(type)) cur.delete(type); else cur.add(type);
  e.t = [...cur]; e.s = subject || e.s || ''; e.ts = Date.now();
  if (e.t.length) m[id] = e; else delete m[id];
  lsSet(MISTAKE_KEY, m); return m[id]?.t || [];
}
export function getMistakeMap() { return lsGet(MISTAKE_KEY, {}); }
export function getMistakeSummary(subject) {
  const m = lsGet(MISTAKE_KEY, {}); const agg = {};
  Object.values(m).forEach((e) => {
    if (subject && e.s !== subject) return;
    (e.t || []).forEach((t) => { agg[t] = (agg[t] || 0) + 1; });
  });
  return agg; // { type: count }
}

// ── 초압축 오답노트 (문항별 1~2문장) ──
// 합격수기(이승재): "오답노트는 한두 문장으로 최대한 간소화, 부피 줄여 자주 회독".
// 저장형: { qid: { t: 본문, s: 과목명, q: 문항라벨, ts } }. (구버전 문자열 값도 호환)
const NOTE_KEY = 'q-note-v1';
const noteText = (v) => (typeof v === 'string' ? v : (v?.t || ''));
export function getNote(id) { return noteText(lsGet(NOTE_KEY, {})[id]); }
export function setNote(id, text, meta) {
  const m = lsGet(NOTE_KEY, {});
  const t = (text || '').trim().slice(0, 200);
  if (t) {
    const prev = m[id];
    m[id] = { t, s: meta?.s || (typeof prev === 'object' ? prev.s : '') || '', q: meta?.q || (typeof prev === 'object' ? prev.q : '') || '', ts: Date.now() };
  } else delete m[id];
  lsSet(NOTE_KEY, m); return t;
}
export function getNoteMap() { // { qid: text } — 기존 호출부(존재여부 판정) 호환
  const m = lsGet(NOTE_KEY, {}); const out = {};
  Object.entries(m).forEach(([k, v]) => { const t = noteText(v); if (t) out[k] = t; });
  return out;
}
// AI 컨텍스트용 — 과목으로 필터(과목 미상 노트는 항상 포함). 최신순.
export function getNoteEntries(subject) {
  const m = lsGet(NOTE_KEY, {});
  return Object.entries(m)
    .map(([qid, v]) => (typeof v === 'string' ? { qid, t: v, s: '', q: '', ts: 0 } : { qid, t: v?.t || '', s: v?.s || '', q: v?.q || '', ts: v?.ts || 0 }))
    .filter((e) => e.t && (!subject || !e.s || e.s === subject))
    .sort((a, b) => (a.ts || 0) - (b.ts || 0));
}

// ── AI 개인화 컨텍스트 — 학생이 직접 남긴 노트·약점을 튜터 프롬프트에 주입 ──
// "AI가 기존에 쓰인 노트를 참고해 학습" — 오답노트·실수유형·자유노트를 학생 본인의 말로 전달한다.
export function buildPersonalNotes(subjectName, leafTitle, freeNotes = []) {
  const lines = [];
  // 0) 이 과목 전략(목표점수·버릴 단원) — 튜터가 목표에 맞춰 과투자/과소투자를 조절하게
  const plan = getStudyPlan();
  const target = plan.targets?.[subjectName];
  const dropped = plan.abandoned?.[subjectName] || [];
  if (target || dropped.length) {
    const bits = [];
    if (target) bits.push(`목표 ${target}점`);
    if (dropped.length) bits.push(`전략적으로 버린 단원: ${dropped.join(', ')}`);
    lines.push(`[이 과목 전략] ${bits.join(' · ')} — 목표에 맞춰 과투자 말고, 버린 단원은 깊이 들어가지 마라.`);
  }
  // 1) 이 과목에서 자주 하는 실수 유형
  const summ = getMistakeSummary(subjectName);
  const mtypes = Object.entries(summ).sort((a, b) => b[1] - a[1]);
  if (mtypes.length) {
    const label = (k) => (MISTAKE_TYPES.find((t) => t.key === k) || {}).label || k;
    lines.push(`[이 학생이 자주 하는 실수] ${mtypes.slice(0, 3).map(([k, n]) => `${label(k)} ${n}회`).join(' · ')} — 이 함정을 특히 조심시켜라.`);
  }
  // 2) 학생이 직접 쓴 초압축 오답노트 (과목 필터)
  const notes = getNoteEntries(subjectName).slice(-10);
  if (notes.length) {
    lines.push(`[학생이 직접 쓴 오답노트 ${notes.length}개 — 학생 본인의 말이다. 그대로 짚어주고 맞는지 확인하라]`);
    notes.forEach((n) => lines.push(`  - ${n.q ? n.q + ' → ' : ''}"${n.t}"`));
  }
  // 3) 저장한 자유 학습 노트 중 이 관/과목과 관련된 것
  const key = (leafTitle || '').trim();
  const rel = (freeNotes || []).filter((n) => {
    const hay = `${n.title || ''} ${(n.tags || []).join(' ')} ${n.leafTitle || ''} ${n.content || ''}`;
    return key && hay.includes(key);
  }).slice(0, 5);
  if (rel.length) {
    lines.push(`[학생이 저장해 둔 학습 노트 ${rel.length}개 (이 관 관련)]`);
    rel.forEach((n) => lines.push(`  - ${(n.title || n.content || '').replace(/\s+/g, ' ').slice(0, 110)}`));
  }
  if (!lines.length) return '';
  return ['', '## 학생이 남긴 노트·약점 (학생 본인이 적은 것 — 이 표현을 활용해 개인화해 가르치고, 노트 내용이 맞는지 확인하라)', ...lines].join('\n');
}

// AI가 참고할 내 노트 요약 — UI 표시용(개인화가 작동 중임을 학생에게 보여준다).
export function personalNoteStats(subjectName) {
  const notes = getNoteEntries(subjectName).length;
  const summ = getMistakeSummary(subjectName);
  const mistakes = Object.values(summ).reduce((a, b) => a + b, 0);
  const top = Object.entries(summ).sort((a, b) => b[1] - a[1])[0];
  const topLabel = top ? ((MISTAKE_TYPES.find((t) => t.key === top[0]) || {}).label || '') : '';
  return { notes, mistakes, topLabel };
}
