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
  byok: 'ailearn-byok',                              // Anthropic (legacy 호환)
  byokOpenai: 'ailearn-byok-openai',                 // OpenAI API key
  byokGoogle: 'ailearn-byok-google',                 // Google AI API key
  baseUrls: 'ailearn-base-urls',                     // 프록시 URL { openai, google }
  prefs: 'ailearn-prefs',
  current: 'ailearn-current',
  mastery: 'ailearn-mastery',
  sessions: 'ailearn-sessions',
  usage: 'ailearn-usage',
  assessments: 'ailearn-assessments',
  mocks: 'ailearn-mocks',                            // 2차 모의 history
  conv: (date) => `ailearn-conversations:${date}`,   // 레거시(날짜 기반)
  room: (leafId) => `ailearn-room:${leafId}`,        // 단원별 채팅방
  // Phase α — 답안 히스토리 (2차 답안 작성 추이)
  answers: (leafId) => `ailearn-answers:${leafId}`,
  // Phase γ — 학습 노트
  notes: 'ailearn-notes',
  // Phase δ — 관측 데이터
  vizUsage: 'ailearn-viz-usage',
  msgRatings: 'ailearn-msg-ratings',
  // Phase β — D-day 시험 플래너
  examPlan: 'ailearn-exam-plan',
  // Phase ε — 학습 streak
  streak: 'ailearn-streak',
};

export const DEFAULT_PREFS = {
  daily_cap: 500,
  model: 'gemini-3.5-flash',
  max_tokens: 1200,
  reasoning_effort: 'minimal', // GPT-5: minimal | low | medium | high  (학습에는 minimal 권장)
  verbosity: 'high',           // GPT-5: low | medium | high
  hide_handover_hint: false,
};

const MASTERY_DEFAULT = {
  coverage: 0, accuracy: 0, status: 'not_started',
  last_studied: null, next_review: null, srs_box: 0,
  attempted: 0, correct: 0,
  // 2차 전용 필드 (사용 안 하면 0으로 무시)
  answer_count: 0,       // 답안 작성 횟수
  avg_score_pct: 0,      // 평균 점수 %
  avg_time_ratio: 1.0,   // 사용시간/목표시간
};

// 2차 답안 채점 결과 반영
export function recordAnswerScore(leafId, scoreResult) {
  if (!leafId || !scoreResult) return null;
  const all = getMastery();
  const prev = { ...MASTERY_DEFAULT, ...(all[leafId] || {}) };
  const count = (prev.answer_count || 0) + 1;
  // max<=0·NaN이면 pct→NaN이 되어 평균이 영구 오염되므로 방어 (호출처가 b.max||30로 막지만 공개 함수 자체도 가드)
  const safeMax = Number(scoreResult.max) > 0 ? Number(scoreResult.max) : 30;
  const safeScore = Number.isFinite(Number(scoreResult.score)) ? Number(scoreResult.score) : 0;
  const pct = Math.max(0, Math.min(100, (safeScore / safeMax) * 100));
  const newAvg = (prev.avg_score_pct * (count - 1) + pct) / count;
  const timeRatio = scoreResult.time_target_min > 0
    ? scoreResult.time_used_min / scoreResult.time_target_min
    : 1.0;
  const newTimeAvg = (prev.avg_time_ratio * (count - 1) + timeRatio) / count;
  const next = {
    ...prev,
    answer_count: count,
    avg_score_pct: newAvg,
    avg_time_ratio: newTimeAvg,
    coverage: Math.min(1, count / 5),  // 5번 작성하면 100%
    accuracy: newAvg / 100,
    last_studied: new Date().toISOString(),
  };
  if (newAvg >= 80 && count >= 3) next.status = 'mastered';
  else if (newAvg >= 60 && count >= 2) next.status = 'passing';
  else if (count > 0) next.status = 'drafting';
  // SRS 적용
  const now = Date.now();
  if (next.status === 'mastered') {
    const box = Math.min(SRS_LADDER.length - 1, (prev.srs_box || 0) + 1);
    next.srs_box = box;
    next.next_review = new Date(now + SRS_LADDER[box] * DAY_MS).toISOString();
  } else {
    next.srs_box = 0;
    next.next_review = new Date(now + SRS_LADDER[0] * DAY_MS).toISOString();
  }
  all[leafId] = next;
  lsSet(KEY.mastery, all);
  return next;
}

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

// 멀티-프로바이더 키 (provider: 'anthropic' | 'openai' | 'google')
export function getApiKey(provider) {
  if (provider === 'openai') return lsGet(KEY.byokOpenai, '');
  if (provider === 'google') return lsGet(KEY.byokGoogle, '');
  return lsGet(KEY.byok, ''); // anthropic 기본
}
export function setApiKey(provider, k) {
  if (provider === 'openai') return lsSet(KEY.byokOpenai, k || null);
  if (provider === 'google') return lsSet(KEY.byokGoogle, k || null);
  return lsSet(KEY.byok, k || null);
}

// 프록시 baseUrl (CORS 우회용) — { openai?: 'https://my-proxy.workers.dev', google?: '...' }
export function getBaseUrls() { return lsGet(KEY.baseUrls, {}); }
export function setBaseUrl(provider, url) {
  const cur = getBaseUrls();
  cur[provider] = url || undefined;
  lsSet(KEY.baseUrls, cur);
}

// 구 모델 ID → 신 ID 매핑 (Gemini 3.1 의 정확한 generateContent 모델명으로 마이그레이션)
const MODEL_ID_MIGRATE = {
  'gemini-3.1-pro': 'gemini-3.1-pro-preview',
  'gemini-3.1-flash': 'gemini-3.1-flash-lite',
};
export function getPrefs() {
  const merged = { ...DEFAULT_PREFS, ...lsGet(KEY.prefs, {}) };
  if (merged.model && MODEL_ID_MIGRATE[merged.model]) {
    merged.model = MODEL_ID_MIGRATE[merged.model];
    lsSet(KEY.prefs, merged);
  }
  return merged;
}
export function setPrefs(patch) {
  const next = { ...getPrefs(), ...patch };
  lsSet(KEY.prefs, next);
  return next;
}

// 구 civil default_leaf(행위능력) 자동 리셋 — 1회성. 사용자가 명시적으로 선택한 게 아니면 첫 단원으로.
const LEGACY_CIVIL_DEFAULT = 'civil__민법총칙__제3장_권리의_주체__제1절_자연인__제3관_행위능력';
const CIVIL_RESET_FLAG = 'ailearn-civil-default-reset-v1';
export function getCurrent() {
  const cur = lsGet(KEY.current, null);
  try {
    if (cur?.subject === 'civil' && cur?.leaf_id === LEGACY_CIVIL_DEFAULT
        && !localStorage.getItem(CIVIL_RESET_FLAG)) {
      localStorage.setItem(CIVIL_RESET_FLAG, '1');
      return null; // 초기화 → 인덱스 로드 시 default_leaf(첫 단원)로 자동 세팅됨
    }
  } catch { /* noop */ }
  return cur;
}
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
// 마지막 메시지 1개 제거 (전송 실패 롤백용). 제거된 메시지를 반환.
export function popRoomMessage(leafId) {
  if (!leafId) return null;
  const arr = getRoomMessages(leafId);
  if (!arr.length) return null;
  const removed = arr.pop();
  lsSet(KEY.room(leafId), arr);
  return removed;
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

// ── 단원 채팅 세이브파일 (현재 단원 1개 내보내기/불러오기) ──────
export const ROOM_SAVE_TYPE = 'ailearn-room-save';
// 다운로드용 직렬화 객체. messages 원문 + 어느 단원인지 식별 메타 포함.
export function buildRoomExport(leafId, meta = {}) {
  return {
    type: ROOM_SAVE_TYPE,
    version: 1,
    leafId,
    subject: meta.subject || null,
    leafPath: meta.path || null,           // 사람이 알아볼 단원 경로 (검증·표시용)
    exported_at: new Date().toISOString(),
    msg_count: getRoomMessages(leafId).length,
    messages: getRoomMessages(leafId),
  };
}
// 세이브파일에서 messages 배열만 안전하게 추출. 형식이 어긋나면 null.
export function parseRoomImport(raw) {
  let data = raw;
  if (typeof raw === 'string') {
    try { data = JSON.parse(raw); } catch { return null; }
  }
  if (!data) return null;
  // 두 형태 허용: { messages:[...] } 세이브파일 또는 순수 메시지 배열
  const msgs = Array.isArray(data) ? data : data.messages;
  if (!Array.isArray(msgs)) return null;
  const clean = msgs.filter((m) => m && typeof m === 'object' && typeof m.role === 'string');
  return { messages: clean, meta: Array.isArray(data) ? {} : data };
}
// mode: 'replace'(교체) | 'append'(뒤에 이어붙이기)
export function importRoomMessages(leafId, messages, mode = 'replace') {
  if (!leafId || !Array.isArray(messages)) return null;
  const next = mode === 'append'
    ? [...getRoomMessages(leafId), ...messages]
    : messages.slice();
  lsSet(KEY.room(leafId), next);
  return next;
}

// ── Phase α: 답안 히스토리 (2차 답안 작성 추이) ──────────
// 같은 leaf 에서 답안 N건 시간순 비교 + 점수 추이 + AI 인사이트 누적
export function getAnswerHistory(leafId) {
  if (!leafId) return [];
  return lsGet(KEY.answers(leafId), []);
}
export function appendAnswer(leafId, record) {
  if (!leafId) return;
  const arr = getAnswerHistory(leafId);
  arr.push({ ts: new Date().toISOString(), ...record });
  // 최근 30건만 유지
  while (arr.length > 30) arr.shift();
  lsSet(KEY.answers(leafId), arr);
  return arr;
}
export function getAllAnswerHistories() {
  const out = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k || !k.startsWith('ailearn-answers:')) continue;
      const leafId = k.slice('ailearn-answers:'.length);
      const arr = JSON.parse(localStorage.getItem(k) || '[]');
      if (!Array.isArray(arr) || !arr.length) continue;
      out.push({ leafId, history: arr });
    }
  } catch { /* noop */ }
  return out;
}

// ── Phase β: D-day 시험 플래너 ──────────
export function getExamPlan() {
  return lsGet(KEY.examPlan, { exam_date: null, target_subjects: [] });
}
export function setExamPlan(plan) {
  lsSet(KEY.examPlan, { ...getExamPlan(), ...plan });
}
export function daysUntilExam() {
  const plan = getExamPlan();
  if (!plan.exam_date) return null;
  const target = new Date(plan.exam_date + 'T00:00:00');
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return Math.ceil((target - today) / (1000 * 60 * 60 * 24));
}

// ── Phase γ: 학습 노트 ──────────
// kind: 'viz'(차트) | 'message'(AI 답변) | 'manual'(자유)
export function getNotes() { return lsGet(KEY.notes, []); }
export function addNote(note) {
  const arr = getNotes();
  const id = 'note_' + Date.now() + '_' + Math.floor(Math.random() * 9999);
  arr.unshift({ id, ts: new Date().toISOString(), ...note });
  while (arr.length > 500) arr.pop();
  lsSet(KEY.notes, arr);
  return id;
}
export function removeNote(id) {
  const arr = getNotes().filter((n) => n.id !== id);
  lsSet(KEY.notes, arr);
}

// ── Phase δ: 관측 — viz 사용 통계 + 메시지 평가 ──────────
export function getVizUsage() { return lsGet(KEY.vizUsage, {}); }
export function incrementVizUsage(name, ok = true) {
  const all = getVizUsage();
  const cur = all[name] || { ok: 0, err: 0, last_ts: null };
  if (ok) cur.ok++; else cur.err++;
  cur.last_ts = new Date().toISOString();
  all[name] = cur;
  lsSet(KEY.vizUsage, all);
}
export function getMsgRatings() { return lsGet(KEY.msgRatings, {}); }
export function rateMsg(msgKey, rating) {
  const all = getMsgRatings();
  if (rating === 0 || rating == null) delete all[msgKey];
  else all[msgKey] = { rating, ts: new Date().toISOString() };
  lsSet(KEY.msgRatings, all);
}

// ── Phase ε: 학습 streak (연속 학습일) ──────────
// 매 메시지 송신 시 markActiveToday() 호출. 자동으로 streak 누적/초기화.
export function getStreak() {
  return lsGet(KEY.streak, { current: 0, longest: 0, last_active: null, active_dates: [] });
}
export function markActiveToday() {
  const today = todayKey();
  const s = getStreak();
  if (s.last_active === today) return s;
  // active_dates 누적 (최근 60일만)
  const dates = new Set(s.active_dates || []);
  dates.add(today);
  const sortedDates = Array.from(dates).sort();
  const recent = sortedDates.slice(-60);
  // current streak 계산
  const yesterday = (() => {
    const d = new Date(); d.setDate(d.getDate() - 1);
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  })();
  let cur = 1;
  if (s.last_active === yesterday) cur = (s.current || 0) + 1;
  // 어제도 아니고 오늘도 아니면 1로 reset
  const longest = Math.max(s.longest || 0, cur);
  const next = { current: cur, longest, last_active: today, active_dates: recent };
  lsSet(KEY.streak, next);
  return next;
}
export function isActiveOnDate(dateStr) {
  const s = getStreak();
  return (s.active_dates || []).includes(dateStr);
}

// ── Phase β: 약점 탐지 — mastery + 답안 점수 가중 ──────────
// 반환: TOP N 약점 leafId 배열 + score
export function detectWeaknesses(masteryDict, allAnswerHistories, topN = 5) {
  const candidates = [];
  // 1차: mastery accuracy < 70% & 시도 횟수 ≥ 3
  Object.entries(masteryDict || {}).forEach(([leafId, m]) => {
    if ((m.attempted || 0) >= 3 && (m.accuracy || 0) < 0.7) {
      candidates.push({
        leafId,
        weakness: (0.7 - (m.accuracy || 0)) * (m.attempted || 0),
        reason: `정답률 ${Math.round((m.accuracy || 0) * 100)}% (${m.attempted}회 풀이)`,
        kind: 'quiz',
      });
    }
  });
  // 2차: 답안 평균 점수 < 70% & 시도 ≥ 2
  (allAnswerHistories || []).forEach(({ leafId, history }) => {
    if (history.length < 2) return;
    const scores = history.map((h) => h.score / (h.max || 30)).filter((v) => !isNaN(v));
    if (!scores.length) return;
    const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
    if (avg < 0.7) {
      candidates.push({
        leafId,
        weakness: (0.7 - avg) * Math.min(scores.length, 5),
        reason: `답안 평균 ${Math.round(avg * 100)}% (${scores.length}회 작성)`,
        kind: 'answer',
      });
    }
  });
  candidates.sort((a, b) => b.weakness - a.weakness);
  return candidates.slice(0, topN);
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

// ── 2차 모의 시험 history ────────────────────────────────
export function getMocks() { return lsGet(KEY.mocks, []); }
export function addMock(record) {
  const arr = getMocks();
  arr.push({ ts: new Date().toISOString(), ...record });
  // 최근 50개만 유지
  while (arr.length > 50) arr.shift();
  lsSet(KEY.mocks, arr);
  return arr;
}
export function getMocksBySubject(subjectId) {
  return getMocks().filter((m) => m.subject_id === subjectId);
}

// ── 1차 5과목 + 2차 3과목 ──────────────────────────────────
export const SUBJECTS = [
  // 1차 (stage:1) — taxonomy 트리 기반
  { id: 'economics',  stage: 1, title: '경제학원론', short: '경제학',   icon: '📊', color: '#0891b2', tax_key: '경제학원론', index_kind: 'taxonomy' },
  { id: 'accounting', stage: 1, title: '회계학',     short: '회계학',   icon: '💰', color: '#f59e0b', tax_key: '회계학', index_kind: 'taxonomy' },
  { id: 'civil',      stage: 1, title: '민법',       short: '민법',     icon: '⚖️', color: '#4f46e5', tax_key: '민법', index_kind: 'taxonomy' },
  { id: 'realestate', stage: 1, title: '부동산학원론', short: '부동산학', icon: '🏘️', color: '#10b981', tax_key: '부동산학원론', index_kind: 'taxonomy' },
  { id: 'law',        stage: 1, title: '감정평가관계법규', short: '관계법규', icon: '📜', color: '#dc2626', tax_key: '감정평가관계법규', index_kind: 'taxonomy' },
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
