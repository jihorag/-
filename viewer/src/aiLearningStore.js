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
  conv: (date) => `ailearn-conversations:${date}`,   // 레거시(날짜 기반)
  room: (leafId) => `ailearn-room:${leafId}`,        // 단원별 채팅방
};

export const DEFAULT_PREFS = {
  daily_cap: 50,
  model: 'claude-sonnet-4-6',
  max_tokens: 1200,
  hide_handover_hint: false,
};

const MASTERY_DEFAULT = {
  coverage: 0, accuracy: 0, status: 'not_started',
  last_studied: null, next_review: null, srs_box: 0,
  attempted: 0, correct: 0,
};

// SRS Leitner 간격 (일) — 다음 복습일 자동 산정에 사용.
export const SRS_LADDER = [1, 3, 7, 16, 35, 70];
const DAY_MS = 86400000;

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
  const prev = { ...MASTERY_DEFAULT, ...(all[code] || {}) };
  const next = { ...prev, ...patch, last_studied: new Date().toISOString() };
  // 학습 상태 자동 분류
  if (next.coverage >= 0.95 && next.accuracy >= 0.8) next.status = 'mastered';
  else if (next.coverage > 0) next.status = 'in_progress';
  // SRS 다음 복습 산정: 마스터 → ladder 따라 박스 진행 / 진행 중이면 box=0(1일 후)
  const now = Date.now();
  if (next.status === 'mastered') {
    const box = Math.min(SRS_LADDER.length - 1, (prev.srs_box || 0) + 1);
    next.srs_box = box;
    next.next_review = new Date(now + SRS_LADDER[box] * DAY_MS).toISOString();
  } else if (next.status === 'in_progress') {
    const box = 0;
    next.srs_box = box;
    next.next_review = new Date(now + SRS_LADDER[box] * DAY_MS).toISOString();
  }
  all[code] = next;
  lsSet(KEY.mastery, all);
  return next;
}

// 채점 결과를 누적해 accuracy 갱신 + SRS lapse 처리
export function recordGrade(code, isCorrect) {
  const all = getMastery();
  const prev = { ...MASTERY_DEFAULT, ...(all[code] || {}) };
  const attempted = (prev.attempted || 0) + 1;
  const correct = (prev.correct || 0) + (isCorrect ? 1 : 0);
  const accuracy = attempted > 0 ? correct / attempted : 0;
  const patch = { attempted, correct, accuracy };
  if (!isCorrect && prev.srs_box > 0) patch.srs_box = Math.max(0, prev.srs_box - 1);
  return updateChapterMastery(code, patch);
}

// 오늘 복습 만기인 단원 코드 목록
export function getDueChapters(now = Date.now()) {
  const all = getMastery();
  const due = [];
  Object.entries(all).forEach(([code, m]) => {
    if (!m || !m.next_review) return;
    const t = new Date(m.next_review).getTime();
    if (isFinite(t) && t <= now) due.push({ code, days_overdue: Math.floor((now - t) / DAY_MS) });
  });
  return due;
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

// 레거시 (날짜별) — 기존 사용자 데이터 호환만 유지
export function getConversation(date) { return lsGet(KEY.conv(date), []); }
export function appendMessage(date, msg) {
  const arr = getConversation(date);
  arr.push({ ts: new Date().toISOString(), ...msg });
  lsSet(KEY.conv(date), arr);
}

// ── 단원별 채팅방 ────────────────────────────────────────────
export function getRoomMessages(leafId) {
  if (!leafId) return [];
  return lsGet(KEY.room(leafId), []);
}
export function appendRoomMessage(leafId, msg) {
  if (!leafId) return;
  const arr = getRoomMessages(leafId);
  arr.push({ ts: new Date().toISOString(), ...msg });
  lsSet(KEY.room(leafId), arr);
}
export function clearRoom(leafId) {
  if (!leafId) return;
  try { localStorage.removeItem(KEY.room(leafId)); } catch { /* noop */ }
}
export function getAllRooms() {
  const out = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k || !k.startsWith('ailearn-room:')) continue;
      const leafId = k.slice('ailearn-room:'.length);
      const arr = JSON.parse(localStorage.getItem(k) || '[]');
      if (!Array.isArray(arr) || !arr.length) continue;
      const last = arr[arr.length - 1];
      out.push({ leafId, msg_count: arr.length, last_ts: last?.ts || null });
    }
  } catch { /* noop */ }
  return out.sort((a, b) => (b.last_ts || '').localeCompare(a.last_ts || ''));
}

export function getUsage() { return lsGet(KEY.usage, {}); }
export function todayKey() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}
export function bumpUsage({ messages = 0, input_tokens = 0, cache_read = 0, cache_write = 0, output_tokens = 0 } = {}) {
  const all = getUsage();
  const k = todayKey();
  const cur = all[k] || { messages: 0, input_tokens: 0, cache_read: 0, cache_write: 0, output_tokens: 0 };
  all[k] = {
    messages: cur.messages + messages,
    input_tokens: (cur.input_tokens || 0) + input_tokens,
    cache_read: (cur.cache_read || 0) + cache_read,
    cache_write: (cur.cache_write || 0) + cache_write,
    output_tokens: (cur.output_tokens || 0) + output_tokens,
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

// ── 1차 5과목 + 2차 3과목 ──────────────────────────────────
export const SUBJECTS = [
  // 1차 (stage:1) — taxonomy 트리 기반
  { id: 'civil',      stage: 1, title: '민법',       short: '민법',     icon: '⚖️', color: '#4f46e5', tax_key: '민법', index_kind: 'taxonomy' },
  { id: 'economics',  stage: 1, title: '경제학원론', short: '경제학',   icon: '📊', color: '#0891b2', tax_key: '경제학원론', index_kind: 'taxonomy' },
  { id: 'realestate', stage: 1, title: '부동산학원론', short: '부동산학', icon: '🏘️', color: '#10b981', tax_key: '부동산학원론', index_kind: 'taxonomy' },
  { id: 'law',        stage: 1, title: '감정평가관계법규', short: '관계법규', icon: '📜', color: '#dc2626', tax_key: '감정평가관계법규', index_kind: 'taxonomy' },
  { id: 'accounting', stage: 1, title: '회계학',     short: '회계학',   icon: '💰', color: '#f59e0b', tax_key: '회계학', index_kind: 'taxonomy' },
  // 2차 (stage:2) — 단원·논점 평탄 구조
  { id: 'appraisal_practice', stage: 2, title: '감정평가실무',         short: '실무',     icon: '🏛️', color: '#7c3aed', index_kind: 'units' },
  { id: 'appraisal_theory',   stage: 2, title: '감정평가이론',         short: '이론',     icon: '📚', color: '#0d9488', index_kind: 'units' },
  { id: 'appraisal_law',      stage: 2, title: '감정평가 및 보상법규', short: '보상법규', icon: '⚖️', color: '#be123c', index_kind: 'units' },
];

export const SUBJECTS_BY_STAGE = {
  1: SUBJECTS.filter((s) => s.stage === 1),
  2: SUBJECTS.filter((s) => s.stage === 2),
};

export const getSubjectMeta = (id) => SUBJECTS.find((s) => s.id === id) || SUBJECTS[0];

// ── 민법 레거시 leaf_id 마이그레이션 ───────────────────────
// 기존 사용자(`민법총칙__...`/`물권법__...`)의 mastery·room·current 키를
// 새 prefix(`civil__...`)로 한 번에 옮긴다. 멱등성 보장.
const CIVIL_LEGACY_PREFIXES = ['민법총칙__', '물권법__'];
function isCivilLegacy(id) { return id && CIVIL_LEGACY_PREFIXES.some((p) => id.startsWith(p)); }

export function migrateLegacyCivilIds() {
  let touched = 0;
  try {
    // mastery
    const m = lsGet(KEY.mastery, {});
    Object.keys(m).forEach((k) => {
      if (isCivilLegacy(k)) {
        const nk = 'civil__' + k;
        if (!m[nk]) m[nk] = m[k];
        delete m[k];
        touched++;
      }
    });
    if (touched) lsSet(KEY.mastery, m);
    // rooms
    const moves = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k || !k.startsWith('ailearn-room:')) continue;
      const leafId = k.slice('ailearn-room:'.length);
      if (isCivilLegacy(leafId)) moves.push([k, KEY.room('civil__' + leafId)]);
    }
    moves.forEach(([oldK, newK]) => {
      const v = localStorage.getItem(oldK);
      if (v != null && !localStorage.getItem(newK)) localStorage.setItem(newK, v);
      localStorage.removeItem(oldK);
      touched++;
    });
    // current
    const cur = lsGet(KEY.current, null);
    if (cur && isCivilLegacy(cur.leaf_id)) {
      cur.leaf_id = 'civil__' + cur.leaf_id;
      cur.subject = cur.subject || 'civil';
      lsSet(KEY.current, cur);
      touched++;
    }
  } catch { /* SSR */ }
  return touched;
}

// ── 전체 학습 진척 초기화 (API 키는 보존) ──────────────────────
// current·mastery·sessions·conversations·usage·assessments 삭제.
// ailearn-byok, ailearn-prefs 는 사용자 설정이므로 유지.
export function resetLearningProgress() {
  const remove = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k || !k.startsWith('ailearn-')) continue;
      if (k === KEY.byok || k === KEY.prefs) continue;
      remove.push(k);
    }
    remove.forEach((k) => localStorage.removeItem(k));
  } catch { /* SSR */ }
  return remove.length;
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
  const rooms = {};
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k) continue;
      if (k.startsWith('ailearn-conversations:')) {
        const date = k.split(':')[1];
        conv[date] = lsGet(k, []);
      } else if (k.startsWith('ailearn-room:')) {
        const leafId = k.slice('ailearn-room:'.length);
        rooms[leafId] = lsGet(k, []);
      }
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
    rooms,
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
  if (snap.rooms && typeof snap.rooms === 'object') {
    Object.entries(snap.rooms).forEach(([leafId, msgs]) => {
      if (Array.isArray(msgs)) lsSet(KEY.room(leafId), msgs);
    });
  }
}
