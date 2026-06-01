// AI 학습 탭 — 저장소 모듈
// 책임: localStorage 키 정의, 일별 대화 기록, 단원 진척, 일일 사용량 cap.
//
// 위험·검토(#8) 반영:
//  - 일일 메시지 cap (DEFAULT_DAILY_CAP) — 비용 폭주 방지
//  - 7일 이상 지난 대화 자동 압축(요약은 유지, 원문은 따로 보관 후 prune 가능)
//  - 단원 진척 = 학습 깊이(coverage) + 문제 정확도(accuracy) 가중치
//  - Supabase는 user_state.data.ai_learning 서브트리에 누적 (스키마 변경 없이 동기화)
//
// localStorage keys:
//   ailearn-byok                       : string (Claude API key, BYOK)
//   ailearn-prefs                      : { daily_cap, model, hide_handover_hint }
//   ailearn-current                    : { subject, code, section_key }
//   ailearn-mastery                    : { [code]: { coverage, accuracy, status, last_studied } }
//   ailearn-sessions                   : [{ id, date, code, section_key, started_at, ended_at, summary, msg_count }]
//   ailearn-conversations:{YYYY-MM-DD} : [{ role, content, ts, tokens?, refs? }]
//   ailearn-usage                      : { [YYYY-MM-DD]: { messages, input_tokens, output_tokens } }
//   ailearn-assessments                : [{ session_id, code, score, comments, next_topic, ts }]

export const KEY = {
  byok: 'ailearn-byok',
  prefs: 'ailearn-prefs',
  current: 'ailearn-current',
  mastery: 'ailearn-mastery',
  sessions: 'ailearn-sessions',
  usage: 'ailearn-usage',
  assessments: 'ailearn-assessments',
  conv: (date) => `ailearn-conversations:${date}`,
};

export const DEFAULT_PREFS = {
  daily_cap: 50,
  model: 'claude-sonnet-4-6',
  hide_handover_hint: false,
};

const MASTERY_DEFAULT = { coverage: 0, accuracy: 0, status: 'not_started', last_studied: null };

function lsGet(key, def) {
  try {
    const raw = localStorage.getItem(key);
    if (raw == null) return def;
    if (typeof def === 'object' && def !== null) return JSON.parse(raw);
    if (typeof def === 'number') {
      const n = parseFloat(raw);
      return Number.isFinite(n) ? n : def;
    }
    return raw;
  } catch { return def; }
}

function lsSet(key, val) {
  try {
    if (val == null) { localStorage.removeItem(key); return; }
    localStorage.setItem(key, typeof val === 'string' ? val : JSON.stringify(val));
  } catch { /* quota or SSR */ }
}

export function getByok() { return lsGet(KEY.byok, ''); }
export function setByok(k) { lsSet(KEY.byok, k || null); }

export function getPrefs() { return { ...DEFAULT_PREFS, ...lsGet(KEY.prefs, {}) }; }
export function setPrefs(patch) {
  const next = { ...getPrefs(), ...patch };
  lsSet(KEY.prefs, next);
  return next;
}

export function getCurrent() { return lsGet(KEY.current, null); }
export function setCurrent(cur) { lsSet(KEY.current, cur); }

export function getMastery() { return lsGet(KEY.mastery, {}); }
export function getChapterMastery(code) {
  const all = getMastery();
  return { ...MASTERY_DEFAULT, ...(all[code] || {}) };
}
export function updateChapterMastery(code, patch) {
  const all = getMastery();
  const next = { ...MASTERY_DEFAULT, ...(all[code] || {}), ...patch, last_studied: new Date().toISOString() };
  // 학습 상태 자동 분류
  if (next.coverage >= 0.95 && next.accuracy >= 0.8) next.status = 'mastered';
  else if (next.coverage > 0) next.status = 'in_progress';
  all[code] = next;
  lsSet(KEY.mastery, all);
  return next;
}

export function getSessions() { return lsGet(KEY.sessions, []); }
export function addSession(s) {
  const arr = getSessions();
  arr.push(s);
  lsSet(KEY.sessions, arr);
}
export function updateSession(id, patch) {
  const arr = getSessions();
  const i = arr.findIndex((s) => s.id === id);
  if (i >= 0) {
    arr[i] = { ...arr[i], ...patch };
    lsSet(KEY.sessions, arr);
  }
}

export function getConversation(date) { return lsGet(KEY.conv(date), []); }
export function appendMessage(date, msg) {
  const arr = getConversation(date);
  arr.push({ ts: new Date().toISOString(), ...msg });
  lsSet(KEY.conv(date), arr);
}

export function getUsage() { return lsGet(KEY.usage, {}); }
export function todayKey() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}
export function bumpUsage({ messages = 0, input_tokens = 0, output_tokens = 0 } = {}) {
  const all = getUsage();
  const k = todayKey();
  const cur = all[k] || { messages: 0, input_tokens: 0, output_tokens: 0 };
  all[k] = {
    messages: cur.messages + messages,
    input_tokens: cur.input_tokens + input_tokens,
    output_tokens: cur.output_tokens + output_tokens,
  };
  lsSet(KEY.usage, all);
  return all[k];
}
export function canSendMessage() {
  const cap = getPrefs().daily_cap;
  if (!cap || cap <= 0) return { ok: true, remaining: Infinity };
  const today = getUsage()[todayKey()] || { messages: 0 };
  const remaining = cap - today.messages;
  return { ok: remaining > 0, remaining };
}

export function getAssessments() { return lsGet(KEY.assessments, []); }
export function addAssessment(a) {
  const arr = getAssessments();
  arr.push({ ts: new Date().toISOString(), ...a });
  lsSet(KEY.assessments, arr);
}

// ── 오래된 대화 정리 (7일 초과는 요약본만 세션에 보존) ────────────
export function pruneOldConversations(keepDays = 7) {
  const cutoff = Date.now() - keepDays * 86400000;
  const removed = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k || !k.startsWith('ailearn-conversations:')) continue;
      const date = k.split(':')[1];
      const t = new Date(date + 'T00:00:00').getTime();
      if (isFinite(t) && t < cutoff) removed.push(k);
    }
    removed.forEach((k) => localStorage.removeItem(k));
  } catch { /* SSR */ }
  return removed.length;
}

// ── Supabase 동기화 페이로드 빌더 ────────────────────────────────
// App.jsx의 cloud sync(pushState)에 포함시키기 위한 한 덩어리 객체.
export function buildSyncSnapshot() {
  const conv = {};
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k || !k.startsWith('ailearn-conversations:')) continue;
      const date = k.split(':')[1];
      conv[date] = lsGet(k, []);
    }
  } catch { /* SSR */ }
  return {
    prefs: getPrefs(),
    current: getCurrent(),
    mastery: getMastery(),
    sessions: getSessions(),
    usage: getUsage(),
    assessments: getAssessments(),
    conversations: conv,
  };
}

export function applySyncSnapshot(snap) {
  if (!snap || typeof snap !== 'object') return;
  if (snap.prefs) lsSet(KEY.prefs, snap.prefs);
  if (snap.current) lsSet(KEY.current, snap.current);
  if (snap.mastery) lsSet(KEY.mastery, snap.mastery);
  if (Array.isArray(snap.sessions)) lsSet(KEY.sessions, snap.sessions);
  if (snap.usage) lsSet(KEY.usage, snap.usage);
  if (Array.isArray(snap.assessments)) lsSet(KEY.assessments, snap.assessments);
  if (snap.conversations && typeof snap.conversations === 'object') {
    Object.entries(snap.conversations).forEach(([date, msgs]) => {
      if (Array.isArray(msgs)) lsSet(KEY.conv(date), msgs);
    });
  }
}
