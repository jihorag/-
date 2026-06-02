import { useState, useMemo, useEffect, useCallback, useRef } from 'react';
import { ArrowLeft, House, Compass, RotateCcw, ChartColumn, BookOpen, Sparkles } from 'lucide-react';
import { cloudEnabled, supabase, pullState, pushState } from './cloud';
import AILearning from './AILearning';
import ToastContainer, { toast } from './Toast';
import CmdK from './CmdK';
import { findLeafByPath, questionsInLeaf, leafQuizStats, QUIZ_SUBJECT_TO_AI, AI_SUBJECT_TO_QUIZ } from './leafStats';
import { setCurrent as setAiCurrent, getMastery as getAiMastery, getDueChapters as getAiDue, SUBJECTS as AI_SUBJECTS, getPrefs as getAiPrefs, setPrefs as setAiPrefs, getApiKey as getProviderKey, setApiKey as setProviderKey, getBaseUrls, setBaseUrl } from './aiLearningStore';
import { MODELS as AI_MODELS } from './aiClaudeClient';
import { getProviderForModel } from './aiProviders';
import MockExam from './MockExam';
import EssayMode from './EssayMode';
import { ParsedText } from './ParsedText';

// ===== 사용자 데이터 관리 (백업/복원/초기화) =====
// 모든 학습 상태는 localStorage 의 quiz-* 키에 저장됨. 계정 동기화의 단일 레이어.
const collectUserData = () => {
  const data = {};
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    // quiz-* (기출 진척), mem-* (구 통암기 호환), ailearn-* (AI 학습 탭) 모두 동기화 대상.
    // API 키(ailearn-byok)는 단일 기기에 머물러야 하므로 동기화에서 제외.
    if (!k) continue;
    if (k === 'ailearn-byok') continue;
    if (k.startsWith('quiz-') || k.startsWith('mem-') || k.startsWith('ailearn-')) {
      data[k] = localStorage.getItem(k);
    }
  }
  return { version: 1, exportedAt: new Date().toISOString(), data };
};
const loadProfile = () => {
  try { return JSON.parse(localStorage.getItem('quiz-profile') || '{}') || {}; }
  catch { return {}; }
};
const saveProfile = (p) => {
  try { localStorage.setItem('quiz-profile', JSON.stringify(p)); } catch { /* SSR */ }
};
const exportUserData = () => {
  // 백업 시각 기록(백업 후 수집되도록 먼저 저장)
  saveProfile({ ...loadProfile(), lastBackup: new Date().toISOString() });
  const blob = new Blob([JSON.stringify(collectUserData(), null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `gampyeong-backup-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
};
const SYNC_PREFIXES = ['quiz-', 'mem-', 'ailearn-'];
const isSyncKey = (k) => k && k !== 'ailearn-byok' && SYNC_PREFIXES.some((p) => k.startsWith(p));
const importUserData = (text) => {
  const parsed = JSON.parse(text);
  const data = parsed && parsed.data;
  if (!data || typeof data !== 'object') throw new Error('형식이 올바르지 않은 백업 파일입니다.');
  for (let i = localStorage.length - 1; i >= 0; i--) {
    const k = localStorage.key(i);
    if (isSyncKey(k)) localStorage.removeItem(k);
  }
  for (const k in data) {
    if (isSyncKey(k) && typeof data[k] === 'string') localStorage.setItem(k, data[k]);
  }
};
const resetUserData = () => {
  for (let i = localStorage.length - 1; i >= 0; i--) {
    const k = localStorage.key(i);
    if (isSyncKey(k)) localStorage.removeItem(k);
  }
};

// v4 난이도(1~5) 배지 메타: 색/라벨
const DIFFICULTY_META = {
  1: { label: '난이도 1 · 매우쉬움', bg: '#ecfdf5', fg: '#047857' },
  2: { label: '난이도 2 · 쉬움', bg: '#f0fdf4', fg: '#15803d' },
  3: { label: '난이도 3 · 보통', bg: '#fefce8', fg: '#a16207' },
  4: { label: '난이도 4 · 어려움', bg: '#fff7ed', fg: '#c2410c' },
  5: { label: '난이도 5 · 매우어려움', bg: '#fef2f2', fg: '#b91c1c' },
};

// 멀티-프로바이더 API 키 + 프록시 baseUrl 위젯 (GlobalSettingsDrawer 'ai' 컨텍스트용)
function ApiKeysWidget({ activeProvider, onChange }) {
  const [anthropicKey, setAnthropicKey] = useState(localStorage.getItem('ailearn-byok') || '');
  const [openaiKey, setOpenaiKey] = useState(getProviderKey('openai') || '');
  const [googleKey, setGoogleKey] = useState(getProviderKey('google') || '');
  const [openaiBase, setOpenaiBase] = useState(getBaseUrls().openai || '');
  const [googleBase, setGoogleBase] = useState(getBaseUrls().google || '');
  const save = (provider, key, baseUrl) => {
    if (provider === 'anthropic') { localStorage.setItem('ailearn-byok', key || ''); }
    else { setProviderKey(provider, key); }
    if (baseUrl !== undefined) setBaseUrl(provider, baseUrl);
    if (onChange) onChange();
  };
  const row = (active, bg, fgBorder, label, key, setKey, base, setBase, placeholder, baseHint, provider, link) => (
    <div style={{ padding: 10, background: active ? bg : '#fff', border: `1px solid ${active ? fgBorder : '#e5e7eb'}`, borderRadius: 8, marginTop: 6 }}>
      <div style={{ fontSize: '0.78rem', fontWeight: 700, color: active ? fgBorder : '#374151', marginBottom: 4 }}>
        {label}{active && ' · 현재 활성'}{key ? ' · ✅ 키 입력됨' : ''}
      </div>
      <input type="password" value={key}
        onChange={(e) => { setKey(e.target.value); save(provider, e.target.value); }}
        placeholder={placeholder}
        style={{ width: '100%', padding: '6px 10px', border: '1px solid #d1d5db', borderRadius: 6, fontSize: '0.85rem', marginBottom: 4, boxSizing: 'border-box' }} />
      {provider !== 'anthropic' && (
        <input type="text" value={base}
          onChange={(e) => { setBase(e.target.value); save(provider, key, e.target.value); }}
          placeholder="프록시 baseUrl (https://your-worker.workers.dev)"
          style={{ width: '100%', padding: '6px 10px', border: '1px solid #d1d5db', borderRadius: 6, fontSize: '0.85rem', marginBottom: 4, boxSizing: 'border-box' }} />
      )}
      <div style={{ fontSize: '0.7rem', color: '#6b7280' }}>
        <a href={link} target="_blank" rel="noreferrer" style={{ color: fgBorder }}>키 발급</a>
        {baseHint && <span> · {baseHint}</span>}
      </div>
    </div>
  );
  return (
    <div>
      {row(activeProvider === 'anthropic', '#fef3c7', '#92400e', 'Anthropic Claude', anthropicKey, setAnthropicKey, '', null, 'sk-ant-...', '브라우저 직호출 OK', 'anthropic', 'https://console.anthropic.com/settings/keys')}
      {row(activeProvider === 'openai', '#dbeafe', '#1e40af', 'OpenAI GPT', openaiKey, setOpenaiKey, openaiBase, setOpenaiBase, 'sk-proj-...', '⚠️ CORS 차단 → 프록시 필수', 'openai', 'https://platform.openai.com/api-keys')}
      {row(activeProvider === 'google', '#dcfce7', '#166534', 'Google Gemini', googleKey, setGoogleKey, googleBase, setGoogleBase, 'AIza...', '⚠️ CORS 차단 → 프록시 필수', 'google', 'https://aistudio.google.com/apikey')}
    </div>
  );
}

// 정답 정규화: 원문자/공백 처리 후 1..optCount 범위의 숫자 문자열만 유효, 아니면 null
const CIRCLED = { '①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5', '⑥': '6', '⑦': '7', '⑧': '8', '⑨': '9', '⑩': '10' };
const normAnswer = (raw, optCount) => {
  if (raw == null) return null;
  let s = String(raw).trim();
  if (CIRCLED[s]) s = CIRCLED[s];
  if (!/^\d+$/.test(s)) return null;            // 빈값·'정답없음'·서술형 센티넬 등
  const n = parseInt(s, 10);
  if (n < 1) return null;                        // '0' 등
  if (optCount && n > optCount) return null;     // 범위 초과
  return String(n);
};

// ===== 감정평가사 전용 메타 =====
// 단일 시험(감정평가사)에만 집중. 다른 시험 데이터는 둘러보기에서 노출하되,
// 홈/현황/추천/D-DAY/합격코치는 모두 감정평가사 기준.
const PRIMARY_EXAM = '감정평가사';
const TARGET_EXAMS = [PRIMARY_EXAM]; // 호환을 위해 배열로 유지 (renderModePicker는 비활성)
// 1차 표준 시간(분) — MockExam 시간 권장값. 1교시 110분 (2과목) + 2교시 110분 (3과목) = 220분.
// 단순화하여 1차 1세트 기준 120분 유지.
const EXAM_DEFAULT_MIN = { '감정평가사': 120 };

// 감정평가사 1차 5과목 (taxonomy.json 의 subject 명과 정확히 일치해야 함)
const APPRAISER_1ST_SUBJECTS = ['민법', '경제학원론', '부동산학원론', '감정평가관계법규', '회계학'];

// 감정평가사 2차 4과목 (essay 시험 — manifest 의 subject 명과 일치)
const APPRAISER_2ND_SUBJECTS = ['감정평가실무', '감정평가이론', '감정평가관계법규', '감정평가 및 보상법규'];
const daysUntil = (yyyymmdd) => {
  if (!yyyymmdd) return null;
  const d = new Date(yyyymmdd + 'T00:00:00');
  if (isNaN(d.getTime())) return null;
  const today = new Date(); today.setHours(0, 0, 0, 0);
  return Math.ceil((d - today) / 86400000);
};
const fmtDday = (n) => n == null ? '' : n === 0 ? 'D-DAY' : n > 0 ? `D-${n}` : `+${-n}일`;
const EXAM_DATES_KEY = 'quiz-exam-dates';
const loadExamDates = () => {
  try { return JSON.parse(localStorage.getItem(EXAM_DATES_KEY) || '{}') || {}; }
  catch { return {}; }
};

// ===== 학습 진행률 (localStorage) =====
const PROGRESS_KEY = 'quiz-progress-v1';
const qid = (q) => q.id || `${q.exam}_${q.year}_${q.number}`;

const loadProgress = () => {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}') || {};
  } catch {
    return {};
  }
};

// 검색·필터 영속화 (새로고침/딥링크 시 유지)
const FILTERS_KEY = 'quiz-filters-v1';

// 가이드 학습 세션 이어풀기: 개념별 마지막 위치(localStorage)
const POS_KEY = 'quiz-pos-v1';
const loadPos = () => {
  try { return JSON.parse(localStorage.getItem(POS_KEY) || '{}') || {}; }
  catch { return {}; }
};
const savePos = (map) => {
  try { localStorage.setItem(POS_KEY, JSON.stringify(map)); } catch { /* quota/SSR */ }
};
const EMPTY_FILTERS = { exams: [], subjects: [], years: [], diffs: [], kw: '', cleanOnly: false };
const loadFilters = () => {
  try {
    const f = JSON.parse(localStorage.getItem(FILTERS_KEY) || 'null');
    return f && typeof f === 'object' ? { ...EMPTY_FILTERS, ...f } : { ...EMPTY_FILTERS };
  } catch {
    return { ...EMPTY_FILTERS };
  }
};

// ===== 기억 곡선(간격 반복) =====
// Leitner 간격(일): 맞히면 다음 칸으로, 틀리면 1칸으로. 끝까지 가면 graduated.
const SRS_LADDER = [1, 3, 7, 16, 35, 70];
const DAY = 86400000;
const dayStart = (t) => { const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); };
// 복습 강도: 간격 배율 + 하루 복습 상한
// 배열에서 무작위 n개(Fisher-Yates 부분 셔플). 모듈 레벨이라 렌더 순수성 규칙 밖.
const sampleN = (arr, n) => {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a.slice(0, n);
};

// B4: 스와이프 추적(렌더와 무관한 전역 트랜션트 상태)
const swipe = { x: 0, y: 0 };
// C2: 문항 목록 스크롤 위치 기억(목록↔학습 왕복 시 복원)
const scrollMem = { qlist: 0 };

// A4: 컨페티 조각(모듈 로드 시 1회 생성 — 렌더 순수성 규칙 밖)
const CONFETTI_COLORS = ['#2563eb', '#16a34a', '#ea580c', '#eab308', '#ec4899', '#06b6d4'];
const CONFETTI_PIECES = Array.from({ length: 90 }, () => ({
  left: Math.random() * 100,
  delay: Math.random() * 0.5,
  dur: 2 + Math.random() * 1.6,
  color: CONFETTI_COLORS[Math.floor(Math.random() * CONFETTI_COLORS.length)],
  rot: Math.random() * 360,
}));
const Confetti = () => (
  <div className="confetti-layer" aria-hidden="true">
    {CONFETTI_PIECES.map((p, i) => (
      <span key={i} className="confetti-pc" style={{
        left: `${p.left}%`, background: p.color,
        animationDelay: `${p.delay}s`, animationDuration: `${p.dur}s`,
        transform: `rotate(${p.rot}deg)`,
      }} />
    ))}
  </div>
);

const SRS_MODES = {
  hard:   { label: '빡세게', factor: 0.6, cap: Infinity },
  normal: { label: '보통',   factor: 1,   cap: 40 },
  easy:   { label: '여유',   factor: 1.7, cap: 20 },
};
const SRS_MODE_KEY = 'quiz-srs-mode';
const ladderFor = (mode) => {
  const f = (SRS_MODES[mode] || SRS_MODES.normal).factor;
  return SRS_LADDER.map(d => Math.max(1, Math.round(d * f)));
};
// prevSrs + 정오답 → 다음 srs. due는 해당 날짜 0시(ms). graduated면 due=null.
const nextSrs = (prevSrs, correct, mode = 'normal') => {
  const ladder = ladderFor(mode);
  const lapses = (prevSrs && prevSrs.lapses) || 0;
  const reps = (prevSrs && prevSrs.reps) || 0;
  if (!correct) {
    return { box: 0, reps: reps + 1, lapses: lapses + 1,
             due: dayStart(Date.now()) + ladder[0] * DAY };
  }
  const box = ((prevSrs && typeof prevSrs.box === 'number') ? prevSrs.box : -1) + 1;
  if (box >= ladder.length) {
    return { box, reps: reps + 1, lapses, due: null, graduated: true };
  }
  return { box, reps: reps + 1, lapses, due: dayStart(Date.now()) + ladder[box] * DAY };
};

// 진행률 상태 + 영속화 훅. record(q,sel,correct) 최초기록, update() 복습 재채점.
const saveProgress = (next) => {
  try { localStorage.setItem(PROGRESS_KEY, JSON.stringify(next)); } catch { /* quota/SSR */ }
  return next;
};

const useProgress = () => {
  const [progress, setProgress] = useState(loadProgress);
  const [srsMode, setSrsModeState] = useState(() => {
    try { return SRS_MODES[localStorage.getItem(SRS_MODE_KEY)] ? localStorage.getItem(SRS_MODE_KEY) : 'normal'; }
    catch { return 'normal'; }
  });
  const setSrsMode = (m) => {
    setSrsModeState(m);
    try { localStorage.setItem(SRS_MODE_KEY, m); } catch { /* SSR */ }
  };
  // 함수형 업데이트로 직전 상태 기준 병합 → 빠른 연속 응답에도 기록 유실 없음.
  // 최초 응답이 오답(채점됨)이면 즉시 복습 스케줄(srs) 부여.
  const record = (q, sel, correct) => {
    const id = qid(q);
    setProgress(prev => {
      if (prev[id]) return prev;
      const entry = { sel, correct, ts: Date.now() };
      if (correct === false) entry.srs = nextSrs(null, false, srsMode);
      return saveProgress({ ...prev, [id]: entry });
    });
  };
  // 복습 재채점: 기존 기록 덮어씀 + 기억곡선 재스케줄. reviewed 누적.
  const update = (q, sel, correct) => {
    const id = qid(q);
    setProgress(prev => {
      const p = prev[id] || {};
      const srs = (correct === null || correct === undefined)
        ? p.srs                                   // 채점불가는 스케줄 변경 안 함
        : nextSrs(p.srs, correct === true, srsMode);
      return saveProgress({
        ...prev,
        [id]: { sel, correct, ts: Date.now(), reviewed: (p.reviewed || 0) + 1, srs },
      });
    });
  };
  const reset = () => setProgress(saveProgress({}));
  const clearMany = (ids) => {
    const set = new Set(ids);
    setProgress(prev => {
      const next = {};
      for (const k in prev) if (!set.has(k)) next[k] = prev[k];
      return saveProgress(next);
    });
  };
  return { progress, record, update, reset, clearMany, srsMode, setSrsMode };
};

// 문항 북마크 — 사유 태그(중요/헷갈림/실수). 정오답과 무관, 별도 영속
const BM_KEY = 'quiz-bookmarks-v1';
// 탭 시 사유 순환: 없음→중요→헷갈림→실수→없음
const BM_REASONS = ['important', 'confusing', 'mistake'];
const BM_META = {
  important: { label: '중요', icon: '★', color: '#f59e0b' },
  confusing: { label: '헷갈림', icon: '★', color: '#8b5cf6' },
  mistake:   { label: '실수', icon: '★', color: '#ef4444' },
};
const bmReasonOf = (v) => (typeof v === 'string' && BM_META[v]) ? v : (v ? 'important' : null); // 레거시(1)→중요
const loadBookmarks = () => {
  try { return JSON.parse(localStorage.getItem(BM_KEY) || '{}') || {}; }
  catch { return {}; }
};
const useBookmarks = () => {
  const [bm, setBm] = useState(loadBookmarks);
  const cycleBookmark = (q) => {
    const id = qid(q);
    setBm(prev => {
      const cur = bmReasonOf(prev[id]);
      const i = cur ? BM_REASONS.indexOf(cur) : -1;
      const nextReason = BM_REASONS[i + 1]; // 마지막 다음은 undefined → 해제
      const next = { ...prev };
      if (nextReason) next[id] = nextReason; else delete next[id];
      try { localStorage.setItem(BM_KEY, JSON.stringify(next)); } catch { /* quota/SSR */ }
      return next;
    });
  };
  return { bm, cycleBookmark };
};

// ===== 분석/코치/커버리지 빌더 (모드별 재사용을 위해 모듈 레벨 순수 함수) =====
const COACH_TARGET = 70; // 목표 정답률(%)

// classifiedList → 과목·난이도·일별 집계 + 약점·연속학습 등
function buildAnalytics(list, progress, trendDays, dailyGoal) {
  const subj = {};
  const diff = {};
  const days = new Set();
  const dayAgg = {};
  let todayCount = 0;
  const todayStr = new Date().toDateString();
  for (const q of list) {
    const sName = q.taxSubjectName || '기타';
    const s = subj[sName] || (subj[sName] = { total: 0, scored: 0, correct: 0, sec: {} });
    s.total++;
    const p = progress[qid(q)];
    if (!p) continue;
    if (p.ts) {
      const ds = new Date(p.ts).toDateString();
      days.add(ds);
      if (ds === todayStr) todayCount++;
      const da = dayAgg[ds] || (dayAgg[ds] = { count: 0, scored: 0, correct: 0 });
      da.count++;
      if (p.correct === true || p.correct === false) { da.scored++; if (p.correct === true) da.correct++; }
    }
    if (p.correct === true || p.correct === false) {
      s.scored++; if (p.correct === true) s.correct++;
      const secName = q.taxSectionName || q.taxChapterName || '기타';
      const sc = s.sec[secName] || (s.sec[secName] = { scored: 0, correct: 0, ids: [] });
      sc.scored++; if (p.correct === true) sc.correct++; sc.ids.push(qid(q));
      if (typeof q.difficulty === 'number') {
        const d = diff[q.difficulty] || (diff[q.difficulty] = { scored: 0, correct: 0 });
        d.scored++; if (p.correct === true) d.correct++;
      }
    }
  }
  let streak = 0;
  const cur = new Date(); cur.setHours(0, 0, 0, 0);
  if (!days.has(cur.toDateString())) cur.setDate(cur.getDate() - 1);
  while (days.has(cur.toDateString())) { streak++; cur.setDate(cur.getDate() - 1); }

  const metDay = (d) => ((dayAgg[d.toDateString()] || {}).count || 0) >= dailyGoal;
  let goalStreak = 0;
  const gc = new Date(); gc.setHours(0, 0, 0, 0);
  if (!metDay(gc)) gc.setDate(gc.getDate() - 1);
  while (metDay(gc)) { goalStreak++; gc.setDate(gc.getDate() - 1); }
  const weekMet = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - i);
    weekMet.push({ label: ['일', '월', '화', '수', '목', '금', '토'][d.getDay()], met: metDay(d), isToday: i === 0 });
  }

  const subjects = Object.entries(subj).map(([name, v]) => ({
    name, total: v.total, scored: v.scored, correct: v.correct,
    acc: v.scored ? Math.round((v.correct / v.scored) * 100) : null,
    weakSection: Object.entries(v.sec)
      .filter(([, c]) => c.scored >= 3)
      .map(([nm, c]) => ({ nm, acc: c.correct / c.scored, ids: c.ids }))
      .sort((a, b) => a.acc - b.acc)[0] || null,
    allWrongUnseenIds: [],
  }));
  const weak = subjects.filter(s => s.scored >= 5 && s.acc != null)
    .sort((a, b) => a.acc - b.acc).slice(0, 3);
  const diffAcc = [1, 2, 3, 4, 5].map(d => {
    const v = diff[d];
    return { d, scored: v ? v.scored : 0, acc: v && v.scored ? Math.round((v.correct / v.scored) * 100) : null };
  });
  const trend = [];
  for (let i = trendDays - 1; i >= 0; i--) {
    const dt = new Date(); dt.setHours(0, 0, 0, 0); dt.setDate(dt.getDate() - i);
    const a = dayAgg[dt.toDateString()] || { count: 0, scored: 0, correct: 0 };
    trend.push({
      label: trendDays <= 7 ? ['일', '월', '화', '수', '목', '금', '토'][dt.getDay()] : '',
      isToday: i === 0,
      count: a.count,
      acc: a.scored ? Math.round((a.correct / a.scored) * 100) : null,
    });
  }
  const trendMax = Math.max(1, ...trend.map(t => t.count));
  const trendSum = trend.reduce((n, t) => n + t.count, 0);
  return { subjects, weak, diffAcc, streak, goalStreak, weekMet, todayCount, studiedDays: days.size, trend, trendMax, trendSum };
}

// analytics.subjects → 합격 준비도·약점 우선순위·verdict
function buildCoach(analyticsSubjects) {
  let sumCorrect = 0, sumScored = 0, sumTotal = 0;
  const rows = analyticsSubjects
    .filter(s => s.total >= 8)
    .map(s => {
      sumCorrect += s.correct; sumScored += s.scored; sumTotal += s.total;
      const acc = s.scored >= 5 ? Math.round((s.correct / s.scored) * 100) : null;
      const cov = Math.round((s.scored / s.total) * 100);
      let tier;
      if (acc == null) tier = 'unknown';
      else if (acc >= COACH_TARGET) tier = 'safe';
      else if (acc >= 50) tier = 'warn';
      else tier = 'risk';
      const gap = acc == null ? COACH_TARGET : Math.max(0, COACH_TARGET - acc);
      const impact = acc == null ? s.total * 0.5 : (s.total * gap) / 100;
      return { name: s.name, total: s.total, scored: s.scored, acc, cov, tier, impact,
        weakSection: s.weakSection };
    })
    .sort((a, b) => b.impact - a.impact);
  const skillAcc = sumScored ? Math.round((sumCorrect / sumScored) * 100) : null;
  const coverage = sumTotal ? Math.round((sumScored / sumTotal) * 100) : 0;
  const readiness = skillAcc == null ? null
    : Math.round(skillAcc * (0.4 + 0.6 * Math.min(1, coverage / 60)));
  const riskCount = rows.filter(r => r.tier === 'risk').length;
  const warnCount = rows.filter(r => r.tier === 'warn').length;
  const topFix = rows.find(r => r.tier === 'risk' || r.tier === 'warn') || rows[0] || null;
  let verdict;
  if (readiness == null) verdict = '데이터를 조금만 더 쌓으면 진단할 수 있어요';
  else if (readiness >= COACH_TARGET) verdict = '합격선 안정권 — 페이스 유지';
  else if (readiness >= 55) verdict = '합격선 근접 — 약한 단원만 잡으면 됩니다';
  else if (readiness >= 40) verdict = '기초 보강 구간 — 약점부터 좁히세요';
  else verdict = '지금부터 약점 위주로 차근차근';
  return { rows, skillAcc, coverage, readiness, riskCount, warnCount, topFix, verdict };
}

// classifiedList → 커버리지(미응답·학습·복습필요·마스터) + 시험별 진척
function buildCoverage(list, progress) {
  let unseen = 0, learned = 0, review = 0, mastered = 0;
  const byExam = {};
  for (const q of list) {
    const ex = q.exam || '기타';
    const e = byExam[ex] || (byExam[ex] = { total: 0, answered: 0, scored: 0, correct: 0, mastered: 0 });
    e.total++;
    const p = progress[qid(q)];
    if (!p) { unseen++; continue; }
    e.answered++;
    const grad = p.srs && p.srs.graduated;
    if (grad) { mastered++; e.mastered++; }
    else if (p.correct === false) review++;
    else learned++;
    if (p.correct === true || p.correct === false) { e.scored++; if (p.correct === true) e.correct++; }
  }
  const total = list.length || 1;
  const exams = Object.entries(byExam)
    .map(([name, v]) => ({
      name, ...v,
      coverPct: Math.round((v.answered / (v.total || 1)) * 100),
      acc: v.scored ? Math.round((v.correct / v.scored) * 100) : null,
    }))
    .sort((a, b) => b.total - a.total);
  return {
    total: list.length, unseen, learned, review, mastered,
    pct: (n) => Math.round((n / total) * 100),
    exams,
  };
}

// 문항 배열에 대한 진행 통계
const progressStats = (questions, progress) => {
  let answered = 0, correct = 0, scored = 0, dSum = 0, dCnt = 0;
  for (const q of questions) {
    if (typeof q.difficulty === 'number') { dSum += q.difficulty; dCnt++; }
    const p = progress[qid(q)];
    if (p) {
      answered++;
      if (p.correct === true) correct++;
      if (p.correct !== null && p.correct !== undefined) scored++; // 정답 정보 있는 채점 대상
    }
  }
  const avgDiff = dCnt ? dSum / dCnt : null;
  // accuracy: 채점 가능한(scored) 문항 기준 정답률
  return {
    answered, correct, scored, total: questions.length,
    accuracy: scored ? Math.round((correct / scored) * 100) : null,
    avgDiff, level: avgDiff ? Math.round(avgDiff) : null,
  };
};

// ===== URL 라우팅 (해시 동기화) =====
// 네비게이션 계층을 #/seg/seg.. 로 직렬화. 빈 값은 '-'.
const NAV_KEYS = ['viewMode', 'currentView', 'scope', 'taxSubject', 'taxSubSubject', 'taxChapter', 'taxSection'];
const enc = (v) => (v == null || v === '' ? '-' : encodeURIComponent(v));
const dec = (v) => (v == null || v === '-' ? null : decodeURIComponent(v));

const serializeNav = (s) => {
  const scope = s.taxScope ? `${s.taxScope.kind}~${s.taxScope.value}` : null;
  const parts = [s.viewMode, s.currentView, scope, s.taxSubject, s.taxSubSubject, s.taxChapter, s.taxSection];
  return '#/' + parts.map(enc).join('/');
};

const parseNav = (hash) => {
  if (!hash || !hash.startsWith('#/')) return null;
  const segs = hash.slice(2).split('/');
  if (segs.length < 2) return null;
  const obj = {};
  NAV_KEYS.forEach((k, i) => { obj[k] = dec(segs[i]); });
  let taxScope = null;
  if (obj.scope) {
    const [kind, ...rest] = obj.scope.split('~');
    const value = rest.join('~');
    if (kind === 'exam' || kind === 'year') {
      taxScope = { kind, value, label: kind === 'year' ? `${value}년` : value };
    }
  }
  return {
    viewMode: obj.viewMode || 'exam',
    currentView: obj.currentView || 'home',
    taxScope,
    taxSubject: obj.taxSubject,
    taxSubSubject: obj.taxSubSubject,
    taxChapter: obj.taxChapter,
    taxSection: obj.taxSection,
  };
};

// SafeImage / ParsedText — './ParsedText' 모듈에서 import (모의고사도 동일 렌더 공유)

// Interactive Question Component
const QuestionItem = ({ q, prior, onAnswer, bmReason, onToggleBookmark, keyboard }) => {
  const [selectedOpt, setSelectedOpt] = useState(prior ? (prior.sel ?? null) : null);
  const isRevealed = selectedOpt !== null;
  const hasAnswer = !!q.answerNorm;          // 정답 정보가 유효한 문항인가
  const noOptions = !q.options || q.options.length === 0;

  const handleOptionClick = (optIdx) => {
    if (isRevealed) return; // 응답 후 변경 방지
    const sel = String(optIdx + 1);
    setSelectedOpt(sel);
    const correct = hasAnswer ? sel === q.answerNorm : null;
    // 햅틱: 정답 짧게, 오답 패턴 진동 (지원 기기에서만)
    try {
      if (correct === true && navigator.vibrate) navigator.vibrate(18);
      else if (correct === false && navigator.vibrate) navigator.vibrate([35, 30, 35]);
    } catch { /* 미지원 */ }
    // correct: 정답 있으면 boolean, 없으면 null(채점 제외)
    if (onAnswer) onAnswer(q, sel, correct);
  };

  // 가이드 학습: 숫자키 1~9로 보기 선택(단일 문항 표시 화면에서만)
  useEffect(() => {
    if (!keyboard || isRevealed) return;
    const optCount = noOptions ? 4 : q.options.length;
    const onKey = (e) => {
      const tag = e.target && e.target.tagName;
      if (tag && /^(INPUT|TEXTAREA|SELECT)$/.test(tag)) return;
      const n = parseInt(e.key, 10);
      if (n >= 1 && n <= optCount) handleOptionClick(n - 1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [keyboard, isRevealed, noOptions, q]);

  return (
    <div style={{ background: '#fff', borderRadius: '12px', padding: '24px', marginBottom: '24px', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', gap: '8px' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontWeight: '700', fontSize: '1.125rem', color: '#2563eb' }}>Q. {q.number}</span>
          {typeof q.difficulty === 'number' && (() => {
            const m = DIFFICULTY_META[q.difficulty] || DIFFICULTY_META[3];
            return (
              <span style={{
                fontSize: '0.75rem', fontWeight: 700, padding: '2px 8px', borderRadius: '999px',
                background: m.bg, color: m.fg
              }}>
                {m.label}
              </span>
            );
          })()}
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '0.875rem', color: '#9ca3af' }}>
            {q.exam} {q.year}년 {q.number}번
          </span>
          {onToggleBookmark && (() => {
            const m = bmReason ? BM_META[bmReason] : null;
            return (
              <button
                onClick={() => onToggleBookmark(q)}
                aria-label="북마크"
                title={m ? `북마크: ${m.label} (탭하여 변경)` : '북마크 (중요→헷갈림→실수)'}
                style={{ border: 'none', background: 'none', cursor: 'pointer', display: 'flex',
                  alignItems: 'center', gap: '3px', padding: 0, lineHeight: 1,
                  color: m ? m.color : '#d1d5db' }}
              >
                <span style={{ fontSize: '1.2rem' }}>{m ? m.icon : '☆'}</span>
                {m && <span style={{ fontSize: '0.7rem', fontWeight: 700 }}>{m.label}</span>}
              </button>
            );
          })()}
        </span>
      </div>
      
      <h3 className="q-text" style={{ lineHeight: '1.6', marginBottom: '20px', fontWeight: '600' }}>
        <ParsedText text={q.question} />
      </h3>
      
      {noOptions && (
        <div style={{ fontSize: '0.82rem', color: '#9ca3af', marginBottom: '12px' }}>
          보기 텍스트는 미공개 — 번호로 정답만 선택해 채점해요.
        </div>
      )}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
        {(noOptions ? ['', '', '', ''] : q.options).map((opt, optIdx) => {
          const optNumber = String(optIdx + 1);
          const isCorrectAnswer = hasAnswer && q.answerNorm === optNumber;
          const isSelected = selectedOpt === optNumber;

          const showCorrect = isRevealed && isCorrectAnswer;
          const showWrong = isRevealed && isSelected && !isCorrectAnswer;

          let bgColor, borderColor, badgeBg = '#fff', badgeColor = '#4b5563', badgeBorder = '1.5px solid #d1d5db';
          let anim = '';
          if (showCorrect) {
            bgColor = '#eff6ff'; borderColor = '#93c5fd'; badgeBg = '#2563eb'; badgeColor = '#fff'; badgeBorder = 'none';
            anim = 'opt-correct';
          } else if (showWrong) {
            bgColor = '#fef2f2'; borderColor = '#fca5a5'; badgeBg = '#dc2626'; badgeColor = '#fff'; badgeBorder = 'none';
            anim = 'opt-wrong';
          } else {
            bgColor = '#f9fafb'; borderColor = '#e5e7eb';
            if (isRevealed) { bgColor = '#fff'; }
          }

          return (
            <button
              key={optIdx}
              type="button"
              className={`opt-btn ${anim}`.trim()}
              onClick={() => handleOptionClick(optIdx)}
              disabled={isRevealed}
              aria-pressed={isSelected}
              aria-label={`${optIdx + 1}번 보기${showCorrect ? ' (정답)' : showWrong ? ' (오답·내 선택)' : ''}`}
              style={{ background: bgColor, borderColor }}
            >
              <span style={{
                display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                width: '26px', height: '26px', borderRadius: '50%',
                background: badgeBg, color: badgeColor, border: badgeBorder,
                fontSize: '0.875rem', fontWeight: '700', flexShrink: 0
              }}>
                {showCorrect ? '✓' : showWrong ? '✕' : optIdx + 1}
              </span>
              {opt
                ? <span className="q-opt" style={{ lineHeight: '1.5', color: '#1f2937' }}><ParsedText text={opt} /></span>
                : <span className="q-opt" style={{ color: '#6b7280' }}>{optIdx + 1}번</span>}
            </button>
          );
        })}
      </div>
      
      {isRevealed && (() => {
        // 채점 결과: 정답 정보 없으면 중립 안내, 있으면 정/오답
        const correct = hasAnswer && selectedOpt === q.answerNorm;
        const accent = !hasAnswer ? '#6b7280' : (correct ? '#16a34a' : '#ef4444');
        return (
          <div className="result-box" style={{ padding: '16px', background: '#f3f4f6', borderRadius: '8px', borderLeft: `4px solid ${accent}` }}>
            <div style={{ fontWeight: '700', marginBottom: q.explanation ? '8px' : '0', fontSize: '0.95rem', display: 'flex', justifyContent: 'space-between' }}>
              <span>{q.explanation ? '해설' : '결과'}</span>
              <span style={{ color: accent }}>
                {!hasAnswer ? 'ℹ 공식 정답 미공개 · 해설로 학습' : (correct ? '✓ 정답입니다!' : '✕ 오답입니다.')}
              </span>
            </div>
            {q.explanation
              ? <div className="q-exp" style={{ lineHeight: '1.6', color: '#4b5563' }}><ParsedText text={q.explanation} /></div>
              : (hasAnswer && <div style={{ fontSize: '0.9rem', color: '#6b7280' }}>정답: {q.answerNorm}번</div>)}
          </div>
        );
      })()}
    </div>
  );
};

const App = () => {
  const [questionsData, setQuestionsData] = useState([]);
  const [taxonomyData, setTaxonomyData] = useState(null);
  // 플로팅 설정 드로어 — 탭별 컨텍스트로 다른 항목 표시
  const [showGlobalSettings, setShowGlobalSettings] = useState(false);
  const [settingsContext, setSettingsContext] = useState('home'); // home | ai | practice | review | status
  // Cmd+K 글로벌 검색 모달
  const [showCmdK, setShowCmdK] = useState(false);
  const [aiPrefs, setAiPrefsState] = useState(() => getAiPrefs());
  const openSettings = (ctx) => { setSettingsContext(ctx); setShowGlobalSettings(true); };
  const openContextSettings = () => {
    let ctx = 'home';
    if (currentView === 'civil') ctx = 'ai';
    else if (currentView === 'reviewHome' || currentView === 'today' || currentView === 'review') ctx = 'review';
    else if (currentView === 'status') ctx = 'status';
    else if (currentView === 'home') ctx = 'home';
    else ctx = 'practice';
    openSettings(ctx);
  };
  // 5과목 AI 학습 leaves — 4탭 공통 참조용. 백그라운드 로드.
  const [leavesBySubject, setLeavesBySubject] = useState({});
  useEffect(() => {
    // 1차 5과목 (taxonomy 트리)
    ['civil', 'economics', 'realestate', 'law', 'accounting'].forEach((sid) => {
      fetch(`/data/study/${sid}/ai_taxonomy_index.json`)
        .then((r) => r.ok ? r.json() : null)
        .then((idx) => {
          if (idx && idx.leaves) {
            setLeavesBySubject((prev) => ({ ...prev, [sid]: idx.leaves }));
          }
        })
        .catch(() => {});
    });
    // 2차 3과목 (units 평탄) — leaves 형식으로 정규화
    ['appraisal_practice', 'appraisal_theory', 'appraisal_law'].forEach((sid) => {
      fetch(`/data/study/${sid}/ai_index.json`)
        .then((r) => r.ok ? r.json() : null)
        .then((raw) => {
          if (!raw) return;
          const leaves = [];
          (raw.units || []).forEach((u) => {
            const baseId = `${raw.subject_id}__${u.code}`;
            leaves.push({
              id: baseId, path: [raw.subject, u.title], leaf_type: 'unit',
              title: u.title, subject_root: raw.subject, frequency: u.frequency || 1,
              unit_code: u.code, unit_file: u.unit_file, problems_file: u.problems_file,
              stage: 2,
            });
            (u.topics || []).forEach((t) => {
              leaves.push({
                id: `${baseId}__${t.id}`, path: [raw.subject, u.title, t.title], leaf_type: 'topic',
                title: t.title, subject_root: raw.subject, frequency: u.frequency || 1,
                unit_code: u.code, unit_file: u.unit_file, problems_file: u.problems_file,
                section_key: t.section_key || 'narrow', section_lines: t.section_lines,
                stage: 2,
              });
            });
          });
          setLeavesBySubject((prev) => ({ ...prev, [sid]: leaves }));
        })
        .catch(() => {});
    });
  }, []);
  // tax 위치 → 해당 AI leaf 찾기 (현재 taxSubject/Chapter/... 상태 기반)
  const findAiLeafForTax = useCallback((tax) => {
    const subjName = tax?.subject;
    const subjId = QUIZ_SUBJECT_TO_AI[subjName];
    if (!subjId || !leavesBySubject[subjId]) return null;
    const path = [tax.sub_subject, tax.chapter, tax.section, tax.item].filter(Boolean);
    return findLeafByPath(leavesBySubject[subjId], path);
  }, [leavesBySubject]);
  // AI 학습 탭으로 점프 (특정 leaf 지정 가능)
  const jumpToAILearn = useCallback((leaf) => {
    if (leaf) {
      const sid = (leaf.id || '').split('__')[0];
      try { setAiCurrent({ subject: sid, leaf_id: leaf.id }); } catch { /* SSR */ }
    }
    setCurrentView('civil');
    window.scrollTo(0, 0);
  }, []);
  const [essayManifest, setEssayManifest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadPct, setLoadPct] = useState(0);
  const [loadError, setLoadError] = useState(false);
  // 새로고침/딥링크 복원: 최초 렌더에서 URL 해시를 1회 파싱해 초기 상태로 사용
  const [bootNav] = useState(() => {
    const parsed = parseNav(typeof window !== 'undefined' ? window.location.hash : '');
    // 'settings' 라우트는 폐기 — 플로팅 드로어로 통합. 홈으로 리디렉트.
    if (parsed && parsed.currentView === 'settings') parsed.currentView = 'home';
    return parsed;
  });
  const bootView = (() => {
    if (!bootNav) return 'home';
    let cv = bootNav.currentView;
    if (cv === 'question_list' || cv === 'study') {
      if (bootNav.taxSection) cv = 'tax_items';
      else if (bootNav.taxChapter) cv = 'tax_sections';
      else if (bootNav.taxSubSubject) cv = 'tax_chapters';
      else if (bootNav.taxSubject) cv = 'tax_sub_subjects';
      else if (bootNav.taxScope) cv = 'tax_subjects';
      else cv = 'dashboard';
    }
    return cv;
  })();

  const [viewMode, setViewMode] = useState(bootNav?.viewMode || 'exam'); // 'exam' | 'subject' | 'year' | 'chapter'
  const [currentView, setCurrentView] = useState(bootView);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [studyIdx, setStudyIdx] = useState(0); // 가이드 학습 모드 현재 문항 인덱스
  const [studyNonce, setStudyNonce] = useState(0); // 재학습 시 문항 카드 강제 리마운트
  const [autoNext, setAutoNextState] = useState(() => {
    try { return localStorage.getItem('quiz-autonext') === '1'; } catch { return false; }
  });
  const setAutoNext = (v) => {
    setAutoNextState(v);
    try { localStorage.setItem('quiz-autonext', v ? '1' : '0'); } catch { /* SSR */ }
  };
  const [autoSec, setAutoSecState] = useState(() => {
    try { const n = parseInt(localStorage.getItem('quiz-autosec'), 10); return [3, 5, 8].includes(n) ? n : 5; }
    catch { return 5; }
  });
  const setAutoSec = (n) => {
    setAutoSecState(n);
    try { localStorage.setItem('quiz-autosec', String(n)); } catch { /* SSR */ }
  };
  const autoTimerRef = useRef(null);
  const fileRef = useRef(null);
  const onImportFile = (e) => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    const r = new FileReader();
    r.onload = () => {
      try { importUserData(String(r.result)); toast.success('가져오기 완료 · 새로고침합니다'); setTimeout(() => window.location.reload(), 600); }
      catch (err) { toast.error('가져오기 실패: ' + err.message); }
    };
    r.readAsText(f);
  };
  const clearAutoTimer = () => { if (autoTimerRef.current) { clearTimeout(autoTimerRef.current); autoTimerRef.current = null; } };
  const [autoPending, setAutoPending] = useState(false); // 자동 다음 대기 표시
  const [studyOrder, setStudyOrderState] = useState(() => {
    try { return localStorage.getItem('quiz-study-order') === 'random' ? 'random' : 'difficulty'; }
    catch { return 'difficulty'; }
  });
  const setStudyOrder = (o) => {
    setStudyOrderState(o);
    try { localStorage.setItem('quiz-study-order', o); } catch { /* SSR */ }
  };
  // 둘러보기 시험 모드 — 감정평가사 전용 변환 후 기본값은 '감정평가사'.
  // 빈 문자열('')은 '전체' 둘러보기 (다른 자격시험 DB까지 포함). 사용자가 명시 선택 시에만.
  // 홈/현황/D-DAY/합격코치는 모두 '감정평가사' 기준으로 동작.
  const [browseExam, setBrowseExamState] = useState(() => {
    try {
      const v = localStorage.getItem('quiz-browse-exam');
      // null = 첫 진입 → 감정평가사 기본. 명시적 '' = 전체 둘러보기 선택.
      return v == null ? PRIMARY_EXAM : v;
    } catch { return PRIMARY_EXAM; }
  });
  // 2차 essay 모드 — 단원/문항 선택 상태 (URL에는 미반영, 세션 내 navigation 용)
  const [essayChapter, setEssayChapter] = useState(null);
  const [essayQuestionId, setEssayQuestionId] = useState(null);

  // 시험 일정 — 3시험 동시 준비 시 D-DAY 표시·일일 권장량 계산용
  const [examDates, setExamDatesState] = useState(loadExamDates);
  const setExamDate = (exam, date) => {
    const next = { ...examDates };
    if (date) next[exam] = date;
    else delete next[exam];
    setExamDatesState(next);
    try { localStorage.setItem(EXAM_DATES_KEY, JSON.stringify(next)); } catch { /* SSR */ }
  };
  const [reviewSubject, setReviewSubject] = useState(null); // 오답 복습 2단계 드릴(과목 선택)
  const [nowTs] = useState(() => Date.now()); // 세션 기준 현재시각(렌더 순수성)
  const [trendDays, setTrendDays] = useState(7); // 학습 추이 기간(7|30)
  const [dailyGoal, setDailyGoalState] = useState(() => {
    try { const n = parseInt(localStorage.getItem('quiz-daily-goal'), 10); return [10, 20, 30, 50].includes(n) ? n : 20; }
    catch { return 20; }
  });
  const setDailyGoal = (n) => {
    setDailyGoalState(n);
    try { localStorage.setItem('quiz-daily-goal', String(n)); } catch { /* SSR */ }
  };
  const [nickname, setNicknameState] = useState(() => loadProfile().nickname || '');
  const setNickname = (v) => {
    setNicknameState(v);
    saveProfile({ ...loadProfile(), nickname: v });
  };

  // 클라우드 동기화(선택)
  const [authUser, setAuthUser] = useState(null);
  const [cloudMsg, setCloudMsg] = useState('');
  const [cloudEmail, setCloudEmail] = useState('');
  const [cloudPw, setCloudPw] = useState('');
  const cloudAuth = async (mode) => {
    setCloudMsg('처리 중…');
    try {
      const creds = { email: cloudEmail.trim(), password: cloudPw };
      const { error } = mode === 'signup'
        ? await supabase.auth.signUp(creds)
        : await supabase.auth.signInWithPassword(creds);
      if (error) throw error;
      setCloudPw('');
      setCloudMsg(mode === 'signup' ? '가입 완료. 로그인되었어요.' : '로그인되었어요.');
    } catch (e) { setCloudMsg((e.message || String(e))); }
  };
  useEffect(() => {
    if (!supabase) return;
    supabase.auth.getSession().then(({ data }) => setAuthUser(data?.session?.user || null));
    const { data: sub } = supabase.auth.onAuthStateChange((_e, session) => setAuthUser(session?.user || null));
    return () => sub?.subscription?.unsubscribe();
  }, []);
  const cloudPush = useCallback(async (silent) => {
    try {
      const at = await pushState(collectUserData());
      saveProfile({ ...loadProfile(), lastCloud: at });
      if (!silent) setCloudMsg('클라우드에 백업했어요.');
    } catch (e) { if (!silent) setCloudMsg('백업 실패: ' + (e.message || e)); }
  }, []);
  const cloudPull = useCallback(async () => {
    try {
      const row = await pullState();
      if (!row || !row.data) { setCloudMsg('클라우드에 저장된 기록이 없어요.'); return; }
      if (!window.confirm('클라우드 기록으로 이 기기를 덮어쓸까요? 현재 진행은 사라집니다.')) return;
      importUserData(JSON.stringify(row.data));
      window.location.reload();
    } catch (e) { setCloudMsg('불러오기 실패: ' + (e.message || e)); }
  }, []);
  // 로그인 중이면 앱이 백그라운드로 갈 때 자동 백업
  useEffect(() => {
    if (!supabase || !authUser) return;
    const onHide = () => { if (document.visibilityState === 'hidden') cloudPush(true); };
    document.addEventListener('visibilitychange', onHide);
    return () => document.removeEventListener('visibilitychange', onHide);
  }, [authUser, cloudPush]);
  const [notifPref, setNotifPref] = useState(() => {
    try { return localStorage.getItem('quiz-notif') === '1' && typeof Notification !== 'undefined' && Notification.permission === 'granted'; }
    catch { return false; }
  });
  useEffect(() => {
    try { localStorage.setItem('quiz-notif', notifPref ? '1' : '0'); } catch { /* SSR */ }
  }, [notifPref]);
  // B1: 본문 글자 크기(작게 0.9 / 보통 1 / 크게 1.18). --q-fs CSS 변수로 반영.
  const [fontScale, setFontScaleState] = useState(() => {
    try { const n = parseFloat(localStorage.getItem('quiz-fontscale')); return [0.9, 1, 1.18].includes(n) ? n : 1; }
    catch { return 1; }
  });
  const setFontScale = (n) => {
    setFontScaleState(n);
    try { localStorage.setItem('quiz-fontscale', String(n)); } catch { /* SSR */ }
  };
  useEffect(() => {
    try { document.documentElement.style.setProperty('--q-fs', String(fontScale)); } catch { /* SSR */ }
  }, [fontScale]);
  // C2: 문항 목록으로 돌아오면 직전 스크롤 위치 복원
  useEffect(() => {
    if (currentView !== 'question_list') return;
    const y = scrollMem.qlist;
    if (y > 0) requestAnimationFrame(() => window.scrollTo(0, y));
  }, [currentView]);
  // A4: 목표 달성 컨페티(하루 1회)
  const [confetti, setConfetti] = useState(false);

  const { progress, record: recordAnswer, update: updateAnswer, reset: resetProgress, clearMany, srsMode, setSrsMode } = useProgress();
  const { bm, cycleBookmark } = useBookmarks();
  // 복합 검색·필터 상태
  const [filters, setFilters] = useState(loadFilters);

  // taxonomy states
  const [taxSubject, setTaxSubject] = useState(bootNav?.taxSubject || null);
  const [taxSubSubject, setTaxSubSubject] = useState(bootNav?.taxSubSubject || null);
  const [taxChapter, setTaxChapter] = useState(bootNav?.taxChapter || null);
  const [taxSection, setTaxSection] = useState(bootNav?.taxSection || null);
  // 시험별/연도별 진입 시 적용되는 분류 스코프: null | {kind:'exam'|'year', value, label}
  const [taxScope, setTaxScope] = useState(bootNav?.taxScope || null);

  // 데이터 불러오기 — manifest → 시험별 chunk 병렬 fetch (E2 chunk loading)
  // 단일 24MB 파일 대신 13개 chunk를 HTTP/2 병렬로 받아 첫 로드 체감 속도와
  // 캐시 granularity 개선. 진행률은 chunk 완료 누적 가중치.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [manifestRes, tData, essayMan] = await Promise.all([
          fetch('/data/manifest.json').then(r => {
            if (!r.ok) throw new Error('manifest ' + r.status);
            return r.json();
          }),
          fetch('/data/taxonomy.json').then(r => r.json()),
          fetch('/data/essay/practice/manifest.json').then(r => r.ok ? r.json() : null).catch(() => null),
        ]);
        if (cancelled) return;
        const exams = manifestRes.exams || [];
        const totalBytes = exams.reduce((s, e) => s + (e.sizeBytes || 1), 0);
        let receivedBytes = 0;
        const chunkPromises = exams.map(async (e) => {
          const r = await fetch(`/data/exams/${e.file}`);
          if (!r.ok) throw new Error(`chunk ${e.file} ${r.status}`);
          const arr = await r.json();
          receivedBytes += (e.sizeBytes || 0);
          if (!cancelled) setLoadPct(Math.min(99, Math.round((receivedBytes / totalBytes) * 100)));
          return arr;
        });
        const chunks = await Promise.all(chunkPromises);
        if (cancelled) return;
        const qData = chunks.flat();
        setLoadPct(100);
        setQuestionsData(qData);
        setTaxonomyData(tData);
        setEssayManifest(essayMan);
        setLoading(false);
      } catch (err) {
        console.error('데이터 로딩 실패:', err);
        if (cancelled) return;
        setLoadError(true);
        setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, []);

  // ----- URL 라우팅: 해시 ↔ 네비게이션 상태 동기 -----
  const hydratedRef = useRef(false);

  const applyNav = useCallback((n) => {
    if (!n) return;
    setViewMode(n.viewMode);
    setTaxScope(n.taxScope);
    setTaxSubject(n.taxSubject);
    setTaxSubSubject(n.taxSubSubject);
    setTaxChapter(n.taxChapter);
    setTaxSection(n.taxSection);
    setSelectedGroup(null);
    // 문제목록은 filterFn 직렬화가 불가 → 가장 가까운 상위 목록으로 복원
    let cv = n.currentView;
    if (cv === 'question_list' || cv === 'study') {
      if (n.taxSection) cv = 'tax_items';
      else if (n.taxChapter) cv = 'tax_sections';
      else if (n.taxSubSubject) cv = 'tax_chapters';
      else if (n.taxSubject) cv = 'tax_sub_subjects';
      else if (n.taxScope) cv = 'tax_subjects';
      else cv = 'dashboard';
    }
    setCurrentView(cv);
  }, []);

  // ===== 글로벌 키보드 단축키 =====
  // Cmd/Ctrl+K — 검색 모달
  // Cmd/Ctrl+1~5 — 탭 전환 (홈/AI학습/문제풀이/복습/현황)
  // Esc — 모달/드로어 닫기 (각 컴포넌트에서 처리)
  useEffect(() => {
    const onKey = (e) => {
      const mod = e.metaKey || e.ctrlKey;
      // 입력 중인 필드에선 일부 단축키 무시 (그러나 Cmd+K는 우선)
      const inField = ['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName);
      if (mod && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        setShowCmdK(true);
        return;
      }
      if (inField) return;
      if (mod && e.key >= '1' && e.key <= '5') {
        e.preventDefault();
        const map = { '1': 'home', '2': 'civil', '3': 'dashboard', '4': 'reviewHome', '5': 'status' };
        const v = map[e.key];
        if (v) { setCurrentView(v); window.scrollTo(0, 0); }
        return;
      }
      if (e.key === 'Escape') {
        if (showCmdK) { setShowCmdK(false); return; }
        if (showGlobalSettings) { setShowGlobalSettings(false); return; }
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [showCmdK, showGlobalSettings]);

  // popstate(브라우저 뒤로/앞으로) 구독. 초기 상태는 이미 해시에서 복원됨.
  useEffect(() => {
    hydratedRef.current = true;
    const onPop = () => applyNav(parseNav(window.location.hash));
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, [applyNav]);

  // 네비게이션 상태 변경 → 해시 push (딥링크/뒤로가기 지원)
  useEffect(() => {
    if (!hydratedRef.current) return;
    const hash = serializeNav({ viewMode, currentView, taxScope, taxSubject, taxSubSubject, taxChapter, taxSection });
    if (hash !== window.location.hash) {
      window.history.pushState(null, '', hash);
    }
  }, [viewMode, currentView, taxScope, taxSubject, taxSubSubject, taxChapter, taxSection]);

  // 검색·필터 영속화: 변경 시 localStorage 저장 (새로고침 후 복원)
  useEffect(() => {
    try { localStorage.setItem(FILTERS_KEY, JSON.stringify(filters)); } catch { /* quota/SSR */ }
  }, [filters]);

  // 모드 set + 시험별 viewMode 불일치 정규화 (구버전 hash로 진입한 경우 등)
  useEffect(() => {
    if (browseExam && viewMode === 'exam') setViewMode('subject');
  }, [browseExam, viewMode]);

  // Process data
  const processedData = useMemo(() => {
    if (loading || !questionsData) return [];
    return questionsData.map(q => {
      // V4 분류 정보: Gemini 또는 Claude로 분류되어 mapped_taxonomy가 있고
      // in_scope!==false 인 문제만 전 탭(시험/과목/단원/연도)에 노출.
      const iv = q.indexing_v4;
      const mt = iv && iv.mapped_taxonomy;
      const isClassified = !!(
        iv && mt && mt.subject &&
        (iv.processed_by === 'gemini-2.5-flash' || iv.processed_by === 'claude-sonnet-4-6') &&
        iv.in_scope !== false
      );

      const opts = q.options || q.choices || [];
      return {
        ...q,
        year: q.year || '2025',
        exam: q.exam || '감정평가사',
        options: opts, // options / choices 통일
        // 정답 정규화: 원문자(①②③..)→숫자, 1..보기수 범위만 유효, 그 외(빈/센티넬)는 null
        answerNorm: normAnswer(q.answer, opts.length),
        // 실제 v4 난이도(1~5). 분류 전이면 null. 4 이상을 '취약'으로 간주.
        difficulty: (iv && typeof iv.difficulty === 'number') ? iv.difficulty : null,
        isWeak: !!(iv && typeof iv.difficulty === 'number' && iv.difficulty >= 4),
        // v4 mapped_taxonomy 기반 분류 필드 (모든 탭이 공유하는 단일 분류축)
        isClassified,
        taxSubjectName: isClassified ? mt.subject : null,
        taxSubSubjectName: isClassified ? (mt.sub_subject || null) : null,
        taxChapterName: isClassified ? (mt.chapter || null) : null,
        taxSectionName: isClassified ? (mt.section || null) : null,
        taxItemName: isClassified ? (mt.item || null) : null,
      };
    });
  }, [loading, questionsData]);

  // 가이드 학습: 키보드 ← 이전 / → · Enter 다음
  useEffect(() => {
    if (currentView !== 'study' || !selectedGroup) return;
    const onKey = (e) => {
      const tag = e.target && e.target.tagName;
      if (tag && /^(INPUT|TEXTAREA|SELECT)$/.test(tag)) return;
      if (e.key === 'ArrowLeft') {
        setStudyIdx(i => Math.max(0, i - 1)); window.scrollTo(0, 0);
      } else if (e.key === 'ArrowRight' || e.key === 'Enter') {
        const n = processedData.filter(selectedGroup.filterFn).length;
        setStudyIdx(i => Math.min(Math.max(0, n - 1), i + 1)); window.scrollTo(0, 0);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [currentView, selectedGroup, processedData]);

  // 가이드 학습 위치 영속화(비복습 세션만) → 이어풀기
  useEffect(() => {
    if (currentView !== 'study' || !selectedGroup || selectedGroup.review || !selectedGroup.posKey) return;
    const map = loadPos();
    if (studyIdx > 0) map[selectedGroup.posKey] = studyIdx;
    else delete map[selectedGroup.posKey];
    savePos(map);
  }, [currentView, selectedGroup, studyIdx]);

  // ===== 단일 v4 분류축 엔진 =====
  // 모든 탭(시험별/과목별/단원별/연도별)이 동일한 mapped_taxonomy 분류축을 공유한다.
  // taxScope: null(과목별/단원별) | {kind:'exam'|'year', value, label} (시험별/연도별 진입 시)
  // browseExam: 둘러보기 상단 모드 픽커 — taxScope 없을 때만 작동(taxScope가 더 구체적)
  const baseFilter = useCallback((item) => {
    if (!item.isClassified) return false;
    if (taxScope) {
      if (taxScope.kind === 'exam') return item.exam === taxScope.value;
      if (taxScope.kind === 'year') return String(item.year) === String(taxScope.value);
      return true;
    }
    if (browseExam && item.exam !== browseExam) return false;
    return true;
  }, [taxScope, browseExam]);

  const scopedClassified = useMemo(
    () => processedData.filter(baseFilter),
    [processedData, baseFilter]
  );

  // Level 0: 연도 목록 (연도별 탭) — 분류 완료 문항만 집계 + browseExam 적용
  const yearGroups = useMemo(() => {
    const groups = {};
    processedData.forEach(q => {
      if (!q.isClassified) return;
      if (browseExam && q.exam !== browseExam) return;
      const key = q.year;
      if (!groups[key]) {
        groups[key] = {
          type: 'year_group',
          title: `${q.year}년`,
          subtitle: '기출연도',
          total: 0,
          weak: false,
          tag: '기출',
          rawValue: q.year
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    return Object.values(groups).sort((a, b) => parseInt(b.rawValue) - parseInt(a.rawValue));
  }, [processedData, browseExam]);

  // Level 0: 시험 목록 (시험별 탭) — 분류 완료 문항만 집계
  // browseExam이 set이면 의미 없음(1개 시험뿐) → UI에서 viewMode='exam' 자체를 숨김
  const examGroups = useMemo(() => {
    const groups = {};
    processedData.forEach(q => {
      if (!q.isClassified) return;
      if (browseExam && q.exam !== browseExam) return;
      const key = q.exam;
      if (!groups[key]) {
        groups[key] = {
          type: 'exam',
          title: q.exam,
          subtitle: '자격시험',
          total: 0,
          weak: false,
          tag: '기출문제'
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    return Object.values(groups).sort((a, b) => b.total - a.total);
  }, [processedData, browseExam]);

  // 과목(taxonomy subject) 목록 — 시험별/과목별/단원별/연도별 공용 (scope 반영)
  const taxSubjectGroups = useMemo(() => {
    if (!taxonomyData) return [];
    const groups = Object.keys(taxonomyData).map(subj => {
      const filtered = scopedClassified.filter(q => q.taxSubjectName === subj);
      return {
        type: 'tax_subject',
        title: subj,
        subtitle: taxScope ? taxScope.label : '단원별 학습',
        total: filtered.length,
        weak: filtered.some(q => q.isWeak),
        tag: '과목'
      };
    }).filter(g => g.total > 0);
    // 2차 essay — '감정평가실무' 과목으로 통합 노출
    // 조건: ① essayManifest 로딩됨, ② 시험 필터(browseExam)가 비었거나 '감정평가사',
    //       ③ scope가 없거나(전체) 감정평가사 시험 scope, 또는 연도 scope
    const examMatch = !browseExam || browseExam === '감정평가사';
    const scopeMatch = !taxScope
      || (taxScope.kind === 'exam' && taxScope.value === '감정평가사')
      || taxScope.kind === 'year';
    if (essayManifest && examMatch && scopeMatch) {
      groups.push({
        type: 'essay_entry',
        title: '감정평가실무',
        subtitle: '2차 논술 기출',
        total: essayManifest.total || 0,
        weak: false,
        tag: '2차'
      });
    }
    return groups;
  }, [taxonomyData, scopedClassified, taxScope, essayManifest, browseExam]);

  // 세부과목 또는 장(Chapter) 목록 (scope 반영)
  const taxSubSubjectGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject) return [];
    const subjData = taxonomyData[taxSubject];
    const filtered = scopedClassified.filter(q => q.taxSubjectName === taxSubject);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSubject} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject
    });

    if (subjData.has_subjects) {
      Object.keys(subjData.subjects).forEach(subSubj => {
        const sub = filtered.filter(q => q.taxSubSubjectName === subSubj);
        if (sub.length === 0) return;
        groups.push({
          type: 'tax_sub_subject',
          title: subSubj,
          subtitle: taxSubject,
          total: sub.length,
          weak: sub.some(q => q.isWeak),
          tag: '세부과목'
        });
      });
    } else {
      subjData.chapters.forEach(ch => {
        const chFiltered = filtered.filter(q => q.taxChapterName === ch.name);
        if (chFiltered.length === 0) return;
        groups.push({
          type: 'tax_chapter',
          title: ch.name,
          subtitle: taxSubject,
          total: chFiltered.length,
          weak: chFiltered.some(q => q.isWeak),
          tag: 'PART/장',
          filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxChapterName === ch.name
        });
      });
    }
    return groups;
  }, [taxonomyData, taxSubject, scopedClassified, baseFilter]);

  // 장(Chapter) 목록 (세부과목이 있는 경우, scope 반영)
  const taxChapterGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxSubSubject) return [];
    const subjData = taxonomyData[taxSubject];
    const chapters = subjData.subjects[taxSubSubject] || [];
    const filtered = scopedClassified.filter(q =>
      q.taxSubjectName === taxSubject && q.taxSubSubjectName === taxSubSubject);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSubSubject} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSubSubjectName === taxSubSubject
    });
    chapters.forEach(ch => {
      const chFiltered = filtered.filter(q => q.taxChapterName === ch.name);
      if (chFiltered.length === 0) return;
      groups.push({
        type: 'tax_chapter',
        title: ch.name,
        subtitle: taxSubSubject,
        total: chFiltered.length,
        weak: chFiltered.some(q => q.isWeak),
        tag: 'PART/장',
        filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxChapterName === ch.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, scopedClassified, baseFilter]);

  // 절(Section) 목록 — 절은 클릭 시 관(item) 목록으로 진입 (scope 반영)
  const taxSectionGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxChapter) return [];
    const subjData = taxonomyData[taxSubject];
    let chapters = [];
    if (subjData.has_subjects && taxSubSubject) {
      chapters = subjData.subjects[taxSubSubject];
    } else if (!subjData.has_subjects) {
      chapters = subjData.chapters;
    }
    const chapterData = chapters.find(c => c.name === taxChapter);
    if (!chapterData || !chapterData.sections) return [];

    const filtered = scopedClassified.filter(q =>
      q.taxSubjectName === taxSubject && q.taxChapterName === taxChapter);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxChapter} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxChapterName === taxChapter
    });

    chapterData.sections.forEach(sec => {
      const secQs = filtered.filter(q => q.taxSectionName === sec.name);
      if (secQs.length === 0) return;
      const hasItems = (sec.items || []).some(it =>
        secQs.some(q => q.taxItemName === it.name));
      groups.push({
        // 관(item) 단위 분류가 있으면 진입형(tax_section), 없으면 바로 풀기(play_all_tax)
        type: hasItems ? 'tax_section' : 'play_all_tax',
        title: sec.name,
        subtitle: taxChapter,
        total: secQs.length,
        weak: secQs.some(q => q.isWeak),
        tag: '절',
        filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSectionName === sec.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, taxChapter, scopedClassified, baseFilter]);

  // 관(item) 목록 — 최저 분류 단위 (scope 반영)
  const taxItemGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxChapter || !taxSection) return [];
    const subjData = taxonomyData[taxSubject];
    let chapters = [];
    if (subjData.has_subjects && taxSubSubject) {
      chapters = subjData.subjects[taxSubSubject];
    } else if (!subjData.has_subjects) {
      chapters = subjData.chapters;
    }
    const chapterData = chapters.find(c => c.name === taxChapter);
    const sectionData = chapterData && (chapterData.sections || []).find(s => s.name === taxSection);
    if (!sectionData) return [];

    const filtered = scopedClassified.filter(q =>
      q.taxSubjectName === taxSubject && q.taxSectionName === taxSection);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSection} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSectionName === taxSection
    });

    (sectionData.items || []).forEach(it => {
      const itQs = filtered.filter(q => q.taxItemName === it.name);
      if (itQs.length === 0) return;
      groups.push({
        type: 'play_all_tax',
        title: it.name,
        subtitle: taxSection,
        total: itQs.length,
        weak: itQs.some(q => q.isWeak),
        tag: '관',
        filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSectionName === taxSection && item.taxItemName === it.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, taxChapter, taxSection, scopedClassified, baseFilter]);

  // 4개 탭 모두 동일 v4 분류축 사용. 시험별/연도별은 picker → 스코프 설정 후 동일 엔진.
  let activeGroups = [];
  if (viewMode === 'subject' || viewMode === 'chapter') activeGroups = taxSubjectGroups;
  else if (viewMode === 'year') activeGroups = yearGroups;
  else if (viewMode === 'exam') activeGroups = examGroups;

  const classifiedList = useMemo(
    () => processedData.filter(q => q.isClassified),
    [processedData]
  );

  const bookmarkedList = useMemo(
    () => classifiedList.filter(q => bm[qid(q)]),
    [classifiedList, bm]
  );

  // 오답(채점 결과 false) 집합 + 과목별 그룹
  const wrongList = useMemo(
    () => classifiedList.filter(q => { const p = progress[qid(q)]; return p && p.correct === false; }),
    [classifiedList, progress]
  );
  const reviewGroups = useMemo(() => {
    const by = {};
    for (const q of wrongList) {
      const k = q.taxSubjectName || '기타';
      (by[k] || (by[k] = [])).push(q);
    }
    return Object.entries(by)
      .map(([subj, qs]) => ({ subj, ids: qs.map(qid), count: qs.length }))
      .sort((a, b) => b.count - a.count);
  }, [wrongList]);

  // 기억곡선 스케줄: 오늘(이전 포함) 복습 도래분 + 다음 예정일
  const srs = useMemo(() => {
    const now = nowTs;
    const dueAllPairs = [];   // [{q, dueAt}]
    let next = null;          // 가장 이른 미래 복습일(ms)
    for (const q of classifiedList) {
      const p = progress[qid(q)];
      if (!p) continue;
      // 레거시: 오답인데 srs 없으면 즉시 복습 대상으로 간주
      const s = p.srs || (p.correct === false ? { due: 0 } : null);
      if (!s || s.graduated) continue;
      if (s.due == null) continue;
      if (s.due <= now) dueAllPairs.push({ q, dueAt: s.due });
      else if (next == null || s.due < next) next = s.due;
    }
    // 하루 상한: 가장 오래 밀린 것부터 cap개, 초과분은 다음 기회로 이월
    dueAllPairs.sort((a, b) => a.dueAt - b.dueAt);
    const cap = (SRS_MODES[srsMode] || SRS_MODES.normal).cap;
    const dueTotal = dueAllPairs.length;
    const due = dueAllPairs.slice(0, cap === Infinity ? dueTotal : cap).map(x => x.q);
    const bysubj = {};
    for (const q of due) {
      const k = q.taxSubjectName || '기타';
      (bysubj[k] || (bysubj[k] = [])).push(q);
    }
    return {
      due, dueTotal, capped: dueTotal > due.length,
      groups: Object.entries(bysubj)
        .map(([subj, qs]) => ({ subj, ids: qs.map(qid), count: qs.length }))
        .sort((a, b) => b.count - a.count),
      nextDue: next,
    };
  }, [classifiedList, progress, nowTs, srsMode]);

  // 앱 열 때 알림: 권한 허용 + 옵트인 + 오늘 도래분 있음 + 당일 1회만.
  // (앱이 닫힌 상태의 백그라운드 푸시는 별도 서버/푸시 인프라 필요 → 범위 밖)
  useEffect(() => {
    if (!notifPref || loading || srs.due.length === 0) return;
    if (typeof Notification === 'undefined' || Notification.permission !== 'granted') return;
    const today = new Date().toDateString();
    try {
      if (localStorage.getItem('quiz-notif-last') === today) return;
      localStorage.setItem('quiz-notif-last', today);
    } catch { /* SSR */ }
    try {
      new Notification('오늘의 복습', { body: `기억 곡선에 따라 복습할 ${srs.due.length}문제가 있어요.` });
    } catch { /* 일부 브라우저는 SW 필요 */ }
  }, [notifPref, loading, srs.due.length]);

  // 복합 필터 선택지
  // 모드 set 시 chip 옵션도 그 시험에 맞춰 좁힘 — 다른 시험 chip이 안 보임
  const filterOptions = useMemo(() => {
    const exams = new Set(), subjects = new Set(), years = new Set();
    for (const q of classifiedList) {
      if (browseExam && q.exam !== browseExam) continue;
      exams.add(q.exam);
      if (q.taxSubjectName) subjects.add(q.taxSubjectName);
      years.add(String(q.year));
    }
    return {
      exams: [...exams].sort(),
      subjects: [...subjects].sort(),
      years: [...years].sort((a, b) => Number(b) - Number(a)),
      diffs: [1, 2, 3, 4, 5],
    };
  }, [classifiedList, browseExam]);

  // 복합 필터 결과 (AND 결합, 키워드는 문제/보기/해설 OR 매칭)
  // 모드 set이면 자동으로 그 시험 필터링 (chip 미선택이어도 적용)
  const filteredResults = useMemo(() => {
    const { exams, subjects, years, diffs, kw, cleanOnly } = filters;
    const active = exams.length || subjects.length || years.length || diffs.length || kw.trim() || cleanOnly;
    if (!active) return [];
    const k = kw.trim().toLowerCase();
    return classifiedList.filter(q => {
      if (browseExam && q.exam !== browseExam) return false;
      if (exams.length && !exams.includes(q.exam)) return false;
      if (subjects.length && !subjects.includes(q.taxSubjectName)) return false;
      if (years.length && !years.includes(String(q.year))) return false;
      if (diffs.length && !diffs.includes(q.difficulty)) return false;
      if (cleanOnly) {
        const dq = q.data_quality || {};
        if (dq.no_answer || dq.no_options) return false;   // 채점 가능 문항만
      }
      if (k) {
        const hay = `${q.question || ''} ${(q.options || []).join(' ')} ${q.explanation || ''}`.toLowerCase();
        if (!hay.includes(k)) return false;
      }
      return true;
    });
  }, [classifiedList, filters, browseExam]);

  const toggleFilter = (key, val) => setFilters(f => {
    const arr = f[key];
    return { ...f, [key]: arr.includes(val) ? arr.filter(x => x !== val) : [...arr, val] };
  });
  const clearFilters = () => setFilters({ ...EMPTY_FILTERS });
  const totalQuestions = classifiedList.length;
  const overall = useMemo(
    () => progressStats(classifiedList, progress),
    [classifiedList, progress]
  );

  // 학습 분석: 모듈-레벨 buildAnalytics에 위임 (전체 + 모드별 재사용)
  const analytics = useMemo(
    () => buildAnalytics(classifiedList, progress, trendDays, dailyGoal),
    [classifiedList, progress, trendDays, dailyGoal]
  );
  // 합격 코치: 전체 데이터 기반 (현황 탭 default + startRecommended 입력)
  const coach = useMemo(() => buildCoach(analytics.subjects), [analytics.subjects]);

  // 모드(browseExam) 컨텍스트 — set일 때 analytics/coach/coverage를 그 시험만으로 재계산
  // status 탭에서 모드 인지 표시, home의 todo-hero 약점 추천이 그 시험 중심이 되도록.
  const modeClassifiedList = useMemo(
    () => browseExam ? classifiedList.filter(q => q.exam === browseExam) : classifiedList,
    [classifiedList, browseExam]
  );
  const modeAnalytics = useMemo(
    () => browseExam ? buildAnalytics(modeClassifiedList, progress, trendDays, dailyGoal) : null,
    [browseExam, modeClassifiedList, progress, trendDays, dailyGoal]
  );
  const modeCoach = useMemo(
    () => browseExam && modeAnalytics ? buildCoach(modeAnalytics.subjects) : null,
    [browseExam, modeAnalytics]
  );

  // 시험별 합격 준비도 — 홈 multi-gauge용. classifiedList를 시험별로 필터해 같은 공식 적용.
  // analytics를 재사용하지 않는 이유: analytics는 전체 데이터 기반(과목별 합산).
  // 시험별로는 같은 과목(예: 민법)이 시험마다 별도 통계를 가져야 함.
  const coachByExam = useMemo(() => {
    const out = {};
    for (const targetExam of TARGET_EXAMS) {
      const subj = {};
      for (const q of classifiedList) {
        if (q.exam !== targetExam) continue;
        const sName = q.taxSubjectName || '기타';
        const s = subj[sName] || (subj[sName] = { total: 0, scored: 0, correct: 0 });
        s.total++;
        const p = progress[qid(q)];
        if (!p) continue;
        if (p.correct === true || p.correct === false) {
          s.scored++; if (p.correct === true) s.correct++;
        }
      }
      let sumCorrect = 0, sumScored = 0, sumTotal = 0;
      let riskCount = 0, warnCount = 0;
      for (const name in subj) {
        const v = subj[name];
        if (v.total < 8) continue;
        sumCorrect += v.correct; sumScored += v.scored; sumTotal += v.total;
        const acc = v.scored >= 5 ? (v.correct / v.scored) * 100 : null;
        if (acc != null) {
          if (acc < 50) riskCount++;
          else if (acc < COACH_TARGET) warnCount++;
        }
      }
      const skillAcc = sumScored ? Math.round((sumCorrect / sumScored) * 100) : null;
      const coverage = sumTotal ? Math.round((sumScored / sumTotal) * 100) : 0;
      const readiness = skillAcc == null ? null
        : Math.round(skillAcc * (0.4 + 0.6 * Math.min(1, coverage / 60)));
      out[targetExam] = { readiness, skillAcc, coverage, riskCount, warnCount,
        totalQ: sumTotal, scoredQ: sumScored };
    }
    return out;
  }, [classifiedList, progress]);

  // A4: 오늘 목표 도달 시 컨페티 1회(하루 1번만)
  useEffect(() => {
    if (analytics.todayCount < dailyGoal) return;
    const today = new Date().toDateString();
    let last = null;
    try { last = localStorage.getItem('quiz-confetti-date'); } catch { /* SSR */ }
    if (last === today) return;
    try { localStorage.setItem('quiz-confetti-date', today); } catch { /* SSR */ }
    const t1 = setTimeout(() => setConfetti(true), 60);
    const t2 = setTimeout(() => setConfetti(false), 2700);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [analytics.todayCount, dailyGoal]);

  // 커버리지: 전체 대비 미응답/정답/복습필요/마스터 + 시험별 진척
  const coverage = useMemo(() => buildCoverage(classifiedList, progress), [classifiedList, progress]);

  // 모든 leaf의 quiz 진척 dict — { leaf_id: {total, answered, correct, wrong, due, accuracy, coverage} }
  // 4탭 공통 참조: AI 학습(LeafPicker 인라인), 둘러보기(카드), 현황(통합 view), 복습(due 카운트)
  const quizStatsByLeaf = useMemo(() => {
    const out = {};
    if (!classifiedList?.length) return out;
    Object.values(leavesBySubject).forEach((arr) => {
      (arr || []).forEach((leaf) => {
        const s = leafQuizStats(leaf, classifiedList, progress, qid);
        if (s.total > 0) out[leaf.id] = s;
      });
    });
    return out;
  }, [leavesBySubject, classifiedList, progress]);

  // AI 학습 탭 — 5과목 quiz 오답률 기반 취약 단원 path 집계.
  // 결과: { civil: [...], economics: [...], realestate: [...], law: [...], accounting: [...] }
  const aiWeakPathsBySubject = useMemo(() => {
    const SUBJ_MAP = {
      '민법': 'civil',
      '경제학원론': 'economics',
      '부동산학원론': 'realestate',
      '감정평가관계법규': 'law',
      '회계학': 'accounting',
    };
    const buckets = { civil: new Map(), economics: new Map(), realestate: new Map(), law: new Map(), accounting: new Map() };
    if (!classifiedList || !classifiedList.length) {
      return Object.fromEntries(Object.keys(buckets).map((k) => [k, []]));
    }
    for (const q of classifiedList) {
      const sid = SUBJ_MAP[q.taxSubjectName];
      if (!sid || !q.taxChapterName) continue;
      const acc = buckets[sid];
      // 과목별 path 구성: 민법·경제·회계는 sub_subject 포함, 부동산·관계법규는 직접 chapter
      const path = [q.taxSubSubjectName, q.taxChapterName, q.taxSectionName, q.taxItemName].filter(Boolean);
      const p = progress[qid(q)];
      if (!p) continue;
      const key = path.join('|');
      const cur = acc.get(key) || { path, attempts: 0, correct: 0 };
      cur.attempts += 1;
      if (p.correct === true) cur.correct += 1;
      acc.set(key, cur);
    }
    const out = {};
    Object.entries(buckets).forEach(([sid, m]) => {
      out[sid] = Array.from(m.values())
        .filter((a) => a.attempts >= 3 && a.correct / a.attempts < 0.6)
        .map((a) => ({ ...a, wrong_rate: 1 - a.correct / a.attempts }))
        .sort((a, b) => b.wrong_rate - a.wrong_rate)
        .slice(0, 8);
    });
    return out;
  }, [classifiedList, progress]);
  // 모드별 커버리지 (status 탭의 스택바)
  const modeCoverage = useMemo(
    () => browseExam ? buildCoverage(modeClassifiedList, progress) : null,
    [browseExam, modeClassifiedList, progress]
  );

  // 한 과목을 집중 연습: 오답·미응답 우선(없으면 전체) 가이드 학습
  // examFilter set이면 그 시험의 그 과목만 (모드 인지 학습)
  const startConcept = (subjectName, title, examFilter = null) => {
    const ids = [];
    for (const q of classifiedList) {
      if ((q.taxSubjectName || '기타') !== subjectName) continue;
      if (examFilter && q.exam !== examFilter) continue;
      const p = progress[qid(q)];
      if (!p || p.correct === false) ids.push(qid(q));   // 미응답 또는 오답 우선
    }
    const finalIds = ids.length ? ids
      : classifiedList.filter(q => (q.taxSubjectName || '기타') === subjectName
        && (!examFilter || q.exam === examFilter)).map(qid);
    startReview(finalIds, title, 'home');
  };

  // 오늘의 추천(적응형): 합격 임팩트 큰 약점 절 → 약점 과목 오답 → 그 외 오답 → 약점 미학습 → 그 외 미학습
  // examFilter set이면 그 시험 안에서만 추천 (modeCoach 기준)
  const startRecommended = (examFilter = null) => {
    const usedCoach = examFilter && modeCoach ? modeCoach : coach;
    const weakNames = new Set(usedCoach.rows.filter(r => r.tier === 'risk' || r.tier === 'warn').map(r => r.name));
    const prioritySec = new Set(); // 정답률 최저 절(임팩트순)의 문항 id
    for (const r of usedCoach.rows) {
      if ((r.tier === 'risk' || r.tier === 'warn') && r.weakSection) {
        for (const id of r.weakSection.ids) prioritySec.add(id);
      }
    }
    const isWeakSubj = (q) => weakNames.has(q.taxSubjectName || '기타');
    const rank = (q) => {
      const id = qid(q);
      const p = progress[id];
      const wrong = p && p.correct === false;
      const unseen = !p;
      if (!wrong && !unseen) return 99;          // 이미 맞힘 → 제외 대상
      if (prioritySec.has(id)) return 0;          // 약점 절 최우선
      if (wrong && isWeakSubj(q)) return 1;
      if (wrong) return 2;
      if (unseen && isWeakSubj(q)) return 3;
      return 4;                                   // 그 외 미학습
    };
    const sourceList = examFilter ? classifiedList.filter(q => q.exam === examFilter) : classifiedList;
    const pool = sourceList
      .map(q => ({ q, r: rank(q) }))
      .filter(x => x.r < 99)
      .sort((a, b) => a.r - b.r);
    const ids = pool.slice(0, dailyGoal).map(x => qid(x.q));
    if (ids.length) startReview(ids, examFilter ? `${examFilter} 추천 학습` : '오늘의 추천 학습', 'home');
  };

  // 무작위 N문제 (셔플은 모듈 레벨 sampleN — 렌더 순수성 규칙 회피)
  const startRandom = (n = 20) => {
    const ids = sampleN(classifiedList, n).map(qid);
    if (ids.length) startReview(ids, `랜덤 ${ids.length}문제`, 'home');
  };

  // 카드 한 장이 대표하는 문항 집합 (filterFn 없으면 타입별 추론)
  const cardQuestions = (group) => {
    if (group.filterFn) return processedData.filter(group.filterFn);
    if (group.type === 'exam') return classifiedList.filter(q => q.exam === group.title);
    if (group.type === 'year_group') return classifiedList.filter(q => String(q.year) === String(group.rawValue));
    if (group.type === 'tax_subject') return scopedClassified.filter(q => q.taxSubjectName === group.title);
    if (group.type === 'tax_sub_subject') return scopedClassified.filter(q => q.taxSubjectName === taxSubject && q.taxSubSubjectName === group.title);
    return [];
  };

  const enterTaxScope = (scope) => {
    setTaxScope(scope);
    setTaxSubject(null);
    setTaxSubSubject(null);
    setTaxChapter(null);
    setTaxSection(null);
    setCurrentView('tax_subjects');
    window.scrollTo(0, 0);
  };

  // 오답 복습 시작: 진입 시점의 오답 id를 스냅샷 → 세션 중 목록 안정, 가이드 학습 재사용
  const startReview = (ids, title, backView = 'review') => {
    const set = new Set(ids);
    setSelectedGroup({
      type: 'play_all_review',
      review: true,
      backView,                       // 학습 종료 후 복귀할 화면(review | today)
      title,
      subtitle: backView === 'today' ? '오늘 복습' : backView === 'search' ? '검색 학습' : backView === 'status' ? '북마크 복습' : '오답 복습',
      filterFn: (q) => set.has(qid(q)),
    });
    setStudyIdx(0);
    setStudyNonce(n => n + 1);
    setCurrentView('study');
    window.scrollTo(0, 0);
  };

  const handleGroupClick = (group) => {
    if (group.type === 'exam') {
      enterTaxScope({ kind: 'exam', value: group.title, label: group.title });
    } else if (group.type === 'year_group') {
      enterTaxScope({ kind: 'year', value: group.rawValue, label: `${group.rawValue}년` });
    } else if (group.type === 'tax_subject') {
      setTaxSubject(group.title);
      setCurrentView('tax_sub_subjects');
      window.scrollTo(0, 0);
    } else if (group.type === 'essay_entry') {
      setEssayChapter(null);
      setEssayQuestionId(null);
      setCurrentView('essay_subjects');
      window.scrollTo(0, 0);
    } else if (group.type === 'tax_sub_subject') {
      setTaxSubSubject(group.title);
      setCurrentView('tax_chapters');
      window.scrollTo(0, 0);
    } else if (group.type === 'tax_chapter') {
      setTaxChapter(group.title);
      setCurrentView('tax_sections');
      window.scrollTo(0, 0);
    } else if (group.type === 'tax_section') {
      setTaxSection(group.title);
      setCurrentView('tax_items');
      window.scrollTo(0, 0);
    } else {
      // 개념 단위 안정 키 → 이어풀기 위치 복원
      const posKey = [taxScope && taxScope.kind, taxScope && taxScope.value,
        taxSubject, taxSubSubject, taxChapter, taxSection, group.type, group.title]
        .map(x => x || '').join('|');
      const saved = loadPos()[posKey];
      const resumeIdx = Number.isInteger(saved) && saved > 0 ? saved : 0;
      setSelectedGroup({ ...group, posKey, resumeIdx });
      setStudyIdx(resumeIdx);
      setStudyNonce(n => n + 1);
      setCurrentView('study');
      window.scrollTo(0, 0);
    }
  };

  const handleBack = () => {
    clearAutoTimer();
    if (currentView === 'question_list' || currentView === 'study') {
      // 오답 복습에서 진입한 경우 복습 화면으로 복귀
      if (selectedGroup && selectedGroup.review) {
        setCurrentView(selectedGroup.backView || 'review');
        setSelectedGroup(null);
        return;
      }
      // play_all_tax: 진입했던 가장 깊은 tax 레벨로 복귀
      if (taxSection) setCurrentView('tax_items');
      else if (taxChapter) setCurrentView('tax_sections');
      else if (taxSubSubject) setCurrentView('tax_chapters');
      else if (taxSubject) setCurrentView('tax_sub_subjects');
      else if (taxScope) setCurrentView('tax_subjects');
      else setCurrentView('dashboard');
      setSelectedGroup(null);
    } else if (currentView === 'tax_items') {
      setCurrentView('tax_sections');
      setTaxSection(null);
    } else if (currentView === 'tax_sections') {
      setCurrentView('tax_chapters');
      setTaxChapter(null);
    } else if (currentView === 'tax_chapters') {
      setCurrentView('tax_sub_subjects');
      setTaxSubSubject(null);
    } else if (currentView === 'tax_sub_subjects') {
      setCurrentView(taxScope ? 'tax_subjects' : 'dashboard');
      setTaxSubject(null);
    } else if (currentView === 'tax_subjects') {
      setCurrentView('dashboard');
      setTaxScope(null);
    } else {
      setCurrentView('dashboard');
    }
  };

  // 둘러보기 모드 변경 — 드릴다운 리셋 + 시험별 viewMode면 자동 전환
  const setBrowseExam = (v) => {
    const next = v || '';
    setBrowseExamState(next);
    try { localStorage.setItem('quiz-browse-exam', next); } catch { /* SSR */ }
    setTaxScope(null);
    setTaxSubject(null);
    setTaxSubSubject(null);
    setTaxChapter(null);
    setTaxSection(null);
    setSelectedGroup(null);
    // 모드 set 시 시험별은 의미 없음(1개 시험뿐) → 과목별로 자연 전환
    if (next && viewMode === 'exam') setViewMode('subject');
    window.scrollTo(0, 0);
  };

  // 탭 전환: 모든 드릴다운 상태를 초기화하고 대시보드로
  const switchTab = (mode) => {
    setViewMode(mode);
    setCurrentView('dashboard');
    setTaxScope(null);
    setTaxSubject(null);
    setTaxSubSubject(null);
    setTaxChapter(null);
    setTaxSection(null);
    setSelectedGroup(null);
    window.scrollTo(0, 0);
  };

  // 하단 탭바: 루트 화면에서만 노출(드릴/풀이는 전체화면)
  const navTab =
    (currentView === 'home' || currentView === 'profile'
      || currentView === 'mock' || currentView === 'mockResult'
      || currentView === 'essay_subjects' || currentView === 'essay_chapters'
      || currentView === 'essay_questions' || currentView === 'essay_result') ? 'home'
    : (currentView === 'reviewHome' || currentView === 'review' || currentView === 'today') ? 'review'
    : currentView === 'status' ? 'status'
    : currentView === 'civil' ? 'ai'
    : 'browse'; // dashboard + tax_* + search(둘러보기 흡수)
  const goTab = (t) => {
    clearAutoTimer();
    if (t === 'home') setCurrentView('home');
    else if (t === 'browse') setCurrentView('dashboard');
    else if (t === 'review') { setReviewSubject(null); setCurrentView('reviewHome'); }
    else if (t === 'ai') setCurrentView('civil');
    else if (t === 'status') setCurrentView('status');
    window.scrollTo(0, 0);
  };
  const NAV_ITEMS = [
    ['home', House, '홈'],
    ['ai', Sparkles, 'AI 학습'],
    ['browse', Compass, '문제풀이'],
    ['review', RotateCcw, '복습'],
    ['status', ChartColumn, '현황'],
  ];
  const bottomNav = (
    <nav className="bottom-nav">
      {NAV_ITEMS.map(([t, Ico, label]) => {
        const active = navTab === t;
        return (
          <button key={t} className={active ? 'active' : ''} onClick={() => goTab(t)}>
            <span className="nav-ico" style={{ position: 'relative' }}>
              <Ico size={22} strokeWidth={active ? 2.4 : 1.9} />
              {t === 'review' && srs.due.length > 0 && (
                <span className="nav-badge">{srs.due.length > 99 ? '99+' : srs.due.length}</span>
              )}
            </span>
            {label}
          </button>
        );
      })}
    </nav>
  );
  // 전역 오버레이(컨페티) — 루트/드릴 양쪽에 삽입
  const overlays = <>{confetti && <Confetti />}</>;
  // 글로벌 설정 플로팅 드로어 — 우측에서 슬라이드
  const globalSettingsDrawer = showGlobalSettings ? (
    <>
      <div onClick={() => setShowGlobalSettings(false)}
        style={{
          position: 'fixed', inset: 0, background: 'rgba(15, 23, 42, 0.45)',
          zIndex: 100, animation: 'fadeIn 0.18s ease-out',
        }} />
      <div style={{
        position: 'fixed', top: 0, right: 0, bottom: 0,
        width: 'clamp(320px, 38vw, 480px)', background: '#fff',
        boxShadow: '-12px 0 28px rgba(0,0,0,0.18)', zIndex: 101,
        display: 'flex', flexDirection: 'column',
        animation: 'slideInRight 0.24s cubic-bezier(0.22, 0.61, 0.36, 1)',
      }}>
        <header style={{
          padding: '14px 16px', borderBottom: '1px solid #e5e7eb',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          background: 'linear-gradient(180deg, #eef2ff 0%, #fff 100%)',
        }}>
          <h2 style={{ margin: 0, fontSize: '1.05rem', fontWeight: 800, color: '#1e3a8a' }}>⚙️ 설정</h2>
          <button onClick={() => setShowGlobalSettings(false)}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#6b7280', fontSize: '1.2rem', padding: 4 }}>
            ✕
          </button>
        </header>
        <div style={{ flex: 1, overflowY: 'auto', padding: 16, display: 'flex', flexDirection: 'column', gap: 14 }}>
          {(() => {
            const Pill = ({ on, label, onClick }) => (
              <button onClick={onClick}
                style={{
                  flex: 1, padding: '7px', borderRadius: 8, fontSize: '0.82rem', fontWeight: 700, cursor: 'pointer',
                  border: on ? '1.5px solid #4f46e5' : '1px solid #d1d5db',
                  background: on ? '#eef2ff' : '#fff',
                  color: on ? '#1d4ed8' : '#6b7280',
                }}>{label}</button>
            );
            const Section = ({ title, desc, children }) => (
              <div>
                <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#374151' }}>{title}</div>
                {desc && <div style={{ fontSize: '0.74rem', color: '#9ca3af', marginTop: 2, marginBottom: 6 }}>{desc}</div>}
                {!desc && <div style={{ marginBottom: 6 }} />}
                {children}
              </div>
            );

            // ── 컨텍스트 라벨 ──
            const ctxMeta = {
              home: { icon: '🏠', label: '홈 설정' },
              ai: { icon: '🎓', label: 'AI 학습 설정' },
              practice: { icon: '📚', label: '문제풀이 설정' },
              review: { icon: '🔁', label: '복습 설정' },
              status: { icon: '📊', label: '현황 설정' },
            };
            const meta = ctxMeta[settingsContext] || ctxMeta.home;

            return (
              <>
                <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: 700,
                  background: '#eef2ff', padding: '6px 10px', borderRadius: 8, alignSelf: 'flex-start' }}>
                  {meta.icon} {meta.label}
                </div>

                {/* 🏠 홈 컨텍스트 */}
                {settingsContext === 'home' && (
                  <>
                    <Section title="📅 시험일 (D-DAY)" desc="홈에 1차/2차 D-DAY와 일일 권장량이 표시돼요.">
                      <div style={{ display: 'flex', gap: 6 }}>
                        {[['1차', '4월경'], ['2차', '8월경']].map(([label, hint]) => {
                          const key = `${PRIMARY_EXAM}_${label}`;
                          return (
                            <label key={label} style={{ flex: 1, fontSize: '0.74rem', color: '#9ca3af' }}>
                              {label} <span style={{ fontSize: '0.66rem' }}>({hint})</span>
                              <input type="date" value={examDates[key] || ''}
                                onChange={(e) => setExamDates(key, e.target.value)}
                                style={{ width: '100%', padding: '6px 8px', marginTop: 2,
                                  border: '1px solid #d1d5db', borderRadius: 6, fontSize: '0.85rem' }} />
                            </label>
                          );
                        })}
                      </div>
                    </Section>
                    <Section title="🎯 일일 학습 목표" desc="하루에 풀 문제 수 목표.">
                      <div style={{ display: 'flex', gap: 4 }}>
                        {[10, 20, 30, 50].map((g) => <Pill key={g} on={dailyGoal === g} label={`${g}문제`} onClick={() => setDailyGoal(g)} />)}
                      </div>
                    </Section>
                  </>
                )}

                {/* 🎓 AI 학습 컨텍스트 */}
                {settingsContext === 'ai' && (
                  <>
                    <Section title="🤖 모델" desc="제공자별 가격·CORS 정책이 다름.">
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                        {[
                          { group: 'Anthropic — 브라우저 직호출', items: [
                            ['claude-sonnet-4-6', '🎯 Sonnet 4.6 (균형·권장)'],
                            ['claude-haiku-4-5-20251001', '⚡ Haiku 4.5 (빠름·저렴)'],
                            ['claude-opus-4-7', '🧠 Opus 4.7 (최고품질·비쌈)'],
                          ]},
                          { group: 'OpenAI — 프록시 필요', items: [
                            ['gpt-5.4', '🔵 GPT-5.4 (-30% vs Sonnet)'],
                            ['gpt-5.4-mini', '🔵 GPT-5.4 mini (-80%)'],
                          ]},
                          { group: 'Google — 일부 환경 직호출 가능', items: [
                            ['gemini-3.1-pro-preview', '🟢 Gemini 3.1 Pro (-43%)'],
                            ['gemini-3.1-flash-lite', '🟢 Gemini 3.1 Flash Lite (-85%)'],
                          ]},
                        ].map((grp) => (
                          <div key={grp.group}>
                            <div style={{ fontSize: '0.7rem', color: '#9ca3af', fontWeight: 700, marginBottom: 4 }}>{grp.group}</div>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                              {grp.items.map(([v, l]) => (
                                <button key={v} onClick={() => { const next = setAiPrefs({ model: v }); setAiPrefsState(next); }}
                                  style={{ padding: '8px 10px', textAlign: 'left', borderRadius: 8, cursor: 'pointer', fontSize: '0.85rem', fontWeight: 700,
                                    border: aiPrefs.model === v ? '1.5px solid #4f46e5' : '1px solid #d1d5db',
                                    background: aiPrefs.model === v ? '#eef2ff' : '#fff',
                                    color: aiPrefs.model === v ? '#1d4ed8' : '#374151' }}>
                                  {l}
                                </button>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </Section>
                    <Section title="📏 응답 길이 상한" desc="짧을수록 빠른 응답.">
                      <div style={{ display: 'flex', gap: 4 }}>
                        {[[600, '짧음'], [1200, '권장'], [2000, '길게'], [3000, '종합']].map(([v, l]) =>
                          <Pill key={v} on={(aiPrefs.max_tokens || 1200) === v} label={l}
                            onClick={() => { const next = setAiPrefs({ max_tokens: v }); setAiPrefsState(next); }} />
                        )}
                      </div>
                    </Section>
                    <Section title="🌊 응답 스트리밍" desc="토큰별 흐름 vs 완성 후 한 번에 (권장: 끔).">
                      <div style={{ display: 'flex', gap: 4 }}>
                        <Pill on={!aiPrefs.streaming} label="끄기 (권장)" onClick={() => { const next = setAiPrefs({ streaming: false }); setAiPrefsState(next); }} />
                        <Pill on={!!aiPrefs.streaming} label="켜기" onClick={() => { const next = setAiPrefs({ streaming: true }); setAiPrefsState(next); }} />
                      </div>
                    </Section>
                    <Section title="📨 일일 메시지 cap" desc="하루 최대 AI 호출 수 (비용 통제).">
                      <input type="number" min={0} max={2000} value={aiPrefs.daily_cap || 500}
                        onChange={(e) => { const next = setAiPrefs({ daily_cap: parseInt(e.target.value, 10) || 0 }); setAiPrefsState(next); }}
                        style={{ width: '100%', padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: 8, fontSize: '0.9rem' }} />
                    </Section>
                    {/^gpt-5/i.test(aiPrefs.model) && (
                      <>
                        <Section title="🧠 추론 강도 (GPT-5 전용)" desc="높을수록 내부 추론 다지지만, 응답 표시 토큰을 소모. 학습엔 minimal 권장.">
                          <div style={{ display: 'flex', gap: 4 }}>
                            {['minimal', 'low', 'medium', 'high'].map((v) =>
                              <Pill key={v} on={(aiPrefs.reasoning_effort || 'minimal') === v} label={v}
                                onClick={() => { const next = setAiPrefs({ reasoning_effort: v }); setAiPrefsState(next); }} />
                            )}
                          </div>
                        </Section>
                        <Section title="📝 응답 상세도 (GPT-5 전용)" desc="visible 응답 길이 가이드.">
                          <div style={{ display: 'flex', gap: 4 }}>
                            {['low', 'medium', 'high'].map((v) =>
                              <Pill key={v} on={(aiPrefs.verbosity || 'high') === v} label={v}
                                onClick={() => { const next = setAiPrefs({ verbosity: v }); setAiPrefsState(next); }} />
                            )}
                          </div>
                        </Section>
                      </>
                    )}
                    <Section title="🔑 API 키 — 프로바이더 3개" desc="키 입력해두면 모델 전환 자유. 현재 활성 표시됨.">
                      <ApiKeysWidget activeProvider={getProviderForModel(aiPrefs.model)} onChange={() => setAiPrefsState({ ...aiPrefs })} />
                    </Section>
                    <Section title="🗑️ 현재 단원 채팅 초기화" desc="지금 열려 있는 단원의 대화만 삭제. 진척도·다른 단원 채팅은 유지.">
                      {(() => {
                        let cur = null;
                        try { cur = JSON.parse(localStorage.getItem('ailearn-current') || 'null'); } catch { /* noop */ }
                        const leafId = cur?.leaf_id;
                        if (!leafId) {
                          return <div style={{ fontSize: '0.78rem', color: '#9ca3af' }}>활성 단원이 없습니다.</div>;
                        }
                        let msgCount = 0;
                        try { msgCount = (JSON.parse(localStorage.getItem(`ailearn-room:${leafId}`) || '[]')).length; } catch { /* noop */ }
                        return (
                          <button
                            onClick={() => {
                              if (!window.confirm(`현재 단원 채팅(${msgCount}개 메시지)을 삭제하시겠습니까?\n진척도는 유지됩니다.`)) return;
                              try { localStorage.removeItem(`ailearn-room:${leafId}`); } catch { /* noop */ }
                              toast.success('단원 채팅 초기화 완료 · 새로고침합니다');
                              setTimeout(() => window.location.reload(), 600);
                            }}
                            disabled={msgCount === 0}
                            style={{ width: '100%', padding: '8px', background: msgCount === 0 ? '#f3f4f6' : '#fef2f2', color: msgCount === 0 ? '#9ca3af' : '#991b1b',
                              border: `1px solid ${msgCount === 0 ? '#e5e7eb' : '#fecaca'}`, borderRadius: 8, fontSize: '0.82rem', fontWeight: 700,
                              cursor: msgCount === 0 ? 'not-allowed' : 'pointer' }}>
                            {msgCount === 0 ? '이 단원에 메시지 없음' : `🗑️ ${msgCount}개 메시지 삭제`}
                          </button>
                        );
                      })()}
                    </Section>
                    <Section title="🎓 AI 학습 진척 초기화" desc="대화·세션·진척도 전부 삭제 (API 키·설정은 유지).">
                      <button
                        onClick={() => {
                          if (!window.confirm('AI 학습 대화·세션·진척도를 모두 삭제하시겠습니까?\n되돌릴 수 없습니다.')) return;
                          try {
                            for (let i = localStorage.length - 1; i >= 0; i--) {
                              const k = localStorage.key(i);
                              if (k && k.startsWith('ailearn-') && k !== 'ailearn-byok' && k !== 'ailearn-prefs') {
                                localStorage.removeItem(k);
                              }
                            }
                          } catch { /* noop */ }
                          toast.success('AI 학습 진척 초기화 완료 · 새로고침합니다');
                          setTimeout(() => window.location.reload(), 600); return;
                          window.location.reload();
                        }}
                        style={{ width: '100%', padding: '10px', background: '#fef2f2', color: '#991b1b',
                          border: '1px solid #fecaca', borderRadius: 8, fontSize: '0.82rem', fontWeight: 700, cursor: 'pointer' }}>
                        🗑️ AI 학습 진척 초기화
                      </button>
                    </Section>
                  </>
                )}

                {/* 📚 문제풀이 컨텍스트 */}
                {settingsContext === 'practice' && (
                  <>
                    <Section title="🔀 학습 순서" desc="가이드 학습에서 문제가 나오는 순서.">
                      <div style={{ display: 'flex', gap: 4 }}>
                        <Pill on={studyOrder === 'difficulty'} label="난이도순" onClick={() => setStudyOrder('difficulty')} />
                        <Pill on={studyOrder === 'random'} label="무작위" onClick={() => setStudyOrder('random')} />
                      </div>
                    </Section>
                    <Section title="⏭️ 자동 다음" desc="정답 확인 후 다음 문제로 자동 이동.">
                      <div style={{ display: 'flex', gap: 4, marginBottom: 8 }}>
                        <Pill on={autoNext} label="켜기" onClick={() => setAutoNext(true)} />
                        <Pill on={!autoNext} label="끄기" onClick={() => setAutoNext(false)} />
                      </div>
                      {autoNext && (
                        <div style={{ display: 'flex', gap: 4 }}>
                          {[3, 5, 8].map((s) => <Pill key={s} on={autoSec === s} label={`${s}초`} onClick={() => setAutoSec(s)} />)}
                        </div>
                      )}
                    </Section>
                    <Section title="🔤 글자 크기" desc="문제·보기·해설 본문 크기.">
                      <div style={{ display: 'flex', gap: 4 }}>
                        {[[0.9, '작게'], [1, '보통'], [1.18, '크게']].map(([v, l]) =>
                          <Pill key={v} on={fontScale === v} label={l} onClick={() => setFontScale(v)} />
                        )}
                      </div>
                    </Section>
                  </>
                )}

                {/* 🔁 복습 컨텍스트 */}
                {settingsContext === 'review' && (
                  <>
                    <Section title="💪 복습 강도" desc="간격 반복 일정의 빡셈 정도.">
                      <div style={{ display: 'flex', gap: 4 }}>
                        {Object.entries(SRS_MODES).map(([k, v]) =>
                          <Pill key={k} on={srsMode === k} label={v.label} onClick={() => setSrsMode(k)} />
                        )}
                      </div>
                    </Section>
                    <Section title="🔔 복습 알림" desc="복습할 문제가 있으면 앱 진입 시 하루 한 번 알림.">
                      <button
                        onClick={() => {
                          if (typeof Notification === 'undefined') return;
                          if (Notification.permission === 'granted') setNotifPref((p) => !p);
                          else Notification.requestPermission().then((r) => setNotifPref(r === 'granted'));
                        }}
                        style={{ width: '100%', padding: '10px', cursor: 'pointer',
                          border: notifPref ? '1.5px solid #4f46e5' : '1px solid #d1d5db',
                          background: notifPref ? '#eef2ff' : '#fff',
                          borderRadius: 8, fontWeight: 700, fontSize: '0.85rem',
                          color: notifPref ? '#1d4ed8' : '#6b7280' }}>
                        {notifPref ? '🔔 켜짐' : '🔕 꺼짐'}
                      </button>
                    </Section>
                  </>
                )}

                {/* 📊 현황 컨텍스트 */}
                {settingsContext === 'status' && (
                  <>
                    <Section title="📈 추세 기간" desc="추세 그래프 기간.">
                      <div style={{ display: 'flex', gap: 4 }}>
                        {[7, 30].map((d) => <Pill key={d} on={trendDays === d} label={`${d}일`} onClick={() => setTrendDays(d)} />)}
                      </div>
                    </Section>
                  </>
                )}

                <div style={{ borderTop: '1px dashed #e5e7eb', margin: '4px 0' }} />

                {/* 공통 — 데이터 관리 */}
                <Section title="💾 데이터 관리" desc="모든 학습 기록 백업/복원.">
                  <button onClick={exportUserData}
                    style={{ width: '100%', padding: '10px', marginBottom: 6, background: '#fff', color: '#1e40af',
                      border: '1px solid #c7d2fe', borderRadius: 8, fontSize: '0.85rem', fontWeight: 700, cursor: 'pointer' }}>
                    📥 백업 다운로드
                  </button>
                  <label style={{ display: 'block', width: '100%', padding: '10px', background: '#fff', color: '#1e40af',
                    border: '1px solid #c7d2fe', borderRadius: 8, fontSize: '0.85rem', fontWeight: 700, cursor: 'pointer', textAlign: 'center' }}>
                    📤 백업 복원
                    <input type="file" accept="application/json" style={{ display: 'none' }}
                      onChange={(e) => {
                        const f = e.target.files?.[0]; if (!f) return;
                        const r = new FileReader();
                        r.onload = () => {
                          try { importUserData(String(r.result)); toast.success('가져오기 완료 · 새로고침합니다'); setTimeout(() => window.location.reload(), 600); }
                          catch (err) { toast.error('형식 오류: ' + err.message); }
                        };
                        r.readAsText(f);
                      }} />
                  </label>
                </Section>

                {/* 프로필 진입 */}
                <button onClick={() => { setShowGlobalSettings(false); setCurrentView('profile'); }}
                  style={{ width: '100%', padding: '11px', background: '#f9fafb', color: '#374151',
                    border: '1px solid #e5e7eb', borderRadius: 8, fontSize: '0.85rem', fontWeight: 700, cursor: 'pointer' }}>
                  👤 프로필·계정 →
                </button>
              </>
            );
          })()}
        </div>
      </div>
    </>
  ) : null;

  // 모든 탭 헤더 우상단 공통 ⚙️ 버튼 — fixed로 떠 있음
  const globalSettingsFab = (
    <button
      onClick={openContextSettings}
      title="이 탭 설정"
      style={{
        position: 'fixed',
        top: 'calc(env(safe-area-inset-top, 0px) + 14px)',
        right: 14, zIndex: 50,
        width: 38, height: 38, borderRadius: '50%',
        background: 'rgba(255,255,255,0.85)',
        border: '1px solid #d1d5db',
        backdropFilter: 'blur(8px)',
        boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
        cursor: 'pointer', fontSize: '1.1rem',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}
    >
      ⚙️
    </button>
  );

  const shell = (content, extraClass = '') => (
    <div className={`app-shell with-nav${extraClass ? ' ' + extraClass : ''}`}>
      {content}
      {/* 홈은 banner에 자체 ⚙️ 버튼이 있어 FAB 중복 노출 회피 */}
      {currentView !== 'home' && globalSettingsFab}
      {globalSettingsDrawer}
      {bottomNav}
      {overlays}
      <ToastContainer />
      <CmdK
        open={showCmdK}
        onClose={() => setShowCmdK(false)}
        subjects={AI_SUBJECTS}
        leaves={Object.values(leavesBySubject).flat()}
        rooms={(() => {
          try {
            const arr = [];
            for (let i = 0; i < localStorage.length; i++) {
              const k = localStorage.key(i);
              if (!k || !k.startsWith('ailearn-room:')) continue;
              const leafId = k.slice('ailearn-room:'.length);
              const items = JSON.parse(localStorage.getItem(k) || '[]');
              if (Array.isArray(items) && items.length) {
                const last = items[items.length - 1];
                arr.push({ leafId, msg_count: items.length, last_ts: last?.ts });
              }
            }
            return arr.sort((a, b) => (b.last_ts || '').localeCompare(a.last_ts || '')).slice(0, 10);
          } catch { return []; }
        })()}
        leafById={new Map(Object.values(leavesBySubject).flat().map((l) => [l.id, l]))}
        onNavigate={(action) => {
          if (action.type === 'tab') {
            setCurrentView(action.view);
            window.scrollTo(0, 0);
          } else if (action.type === 'subject') {
            try { setAiCurrent({ subject: action.id, leaf_id: null }); } catch { /* noop */ }
            setCurrentView('civil');
            window.scrollTo(0, 0);
          } else if (action.type === 'leaf') {
            if (!action.leaf) return;
            const sid = (action.leaf.id || '').split('__')[0];
            try { setAiCurrent({ subject: sid, leaf_id: action.leaf.id }); } catch { /* noop */ }
            setCurrentView('civil');
            window.scrollTo(0, 0);
          } else if (action.type === 'settings') {
            openSettings(action.ctx);
          }
        }}
      />
    </div>
  );

  // 드릴 화면 공통 상단바: 좌측 뒤로가기 + 우측 액션(옵션)
  const drillHeader = (rightAction = null) => (
    <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', display: 'flex', justifyContent: 'space-between' }}>
      <button className="back-btn" onClick={handleBack}>
        <ArrowLeft size={24} style={{ marginRight: '8px' }} />
        <span style={{ fontSize: '1rem', fontWeight: '600' }}>뒤로가기</span>
      </button>
      {rightAction}
    </header>
  );

  // 시험 모드 픽커 — 홈/둘러보기/현황에서 일관된 디자인으로 사용
  // 감정평가사 전용 변환 후 — 시험 picker는 둘러보기 탭에서만 "감정평가사 ↔ 전체 DB" 토글로 단순화.
  // withDday 인자는 하위 호환만 위해 유지 (홈에서는 더 이상 사용 안 함).
  const renderModePicker = () => {
    const pillStyle = (on) => ({
      flex: '1 0 auto',
      padding: '8px 12px',
      whiteSpace: 'nowrap',
      border: on ? '1.5px solid #2563eb' : '1px solid #d1d5db',
      background: on ? '#eff6ff' : '#fff',
      color: on ? '#1d4ed8' : '#374151',
      borderRadius: 10,
      fontWeight: on ? 800 : 600,
      fontSize: '0.85rem',
      cursor: 'pointer',
      textAlign: 'center',
    });
    return (
      <div style={{ display: 'flex', gap: 6 }}>
        <button onClick={() => setBrowseExam(PRIMARY_EXAM)} style={pillStyle(browseExam === PRIMARY_EXAM)}>
          🎯 {PRIMARY_EXAM} 기출
        </button>
        <button onClick={() => setBrowseExam('')} style={{
          ...pillStyle(!browseExam),
          color: !browseExam ? '#1d4ed8' : '#6b7280',
        }}>
          🌐 전체 DB ({TARGET_EXAMS.length === 1 ? '14자격' : ''})
        </button>
      </div>
    );
  };

  // AI 학습 탭 — 하단 탭바 노출되는 루트 화면. (구 통암기 탭 대체)
  // PC 에서 사이드바+채팅 2컬럼이 전체 화면을 활용하도록 fullwidth 클래스.
  if (currentView === 'civil') {
    return shell(
      <AILearning
        isTabRoot
        browseExam={browseExam}
        weakPathsBySubject={aiWeakPathsBySubject}
        leavesBySubject={leavesBySubject}
        onJumpToBrowse={(leaf) => {
          // leaf.path → tax 드릴 위치로 점프 (가장 구체적인 단계)
          const subjId = (leaf.id || '').split('__')[0];
          const subjName = AI_SUBJECT_TO_QUIZ[subjId];
          if (!subjName || !taxonomyData) return;
          const hasSubs = !!taxonomyData[subjName]?.has_subjects;
          const p = leaf.path || [];
          setTaxScope({ key: PRIMARY_EXAM, label: PRIMARY_EXAM });
          setTaxSubject(subjName);
          setTaxSubSubject(hasSubs ? p[0] : null);
          setTaxChapter(hasSubs ? p[1] : p[0]);
          setTaxSection(hasSubs ? (p[2] || null) : (p[1] || null));
          // 가장 구체적인 단계로 currentView 결정
          const sectionVal = hasSubs ? p[2] : p[1];
          const chapterVal = hasSubs ? p[1] : p[0];
          if (sectionVal) setCurrentView('tax_items');
          else if (chapterVal) setCurrentView('tax_sections');
          else setCurrentView('tax_chapters');
          window.scrollTo(0, 0);
        }}
        getQuizCountForLeaf={(leaf) => {
          if (!leaf || !classifiedList?.length) return 0;
          return questionsInLeaf(classifiedList, leaf).length;
        }}
        quizStatsByLeaf={quizStatsByLeaf}
      />,
      'fullwidth'
    );
  }

  // 모의고사: picker/result는 하단 탭 유지, session은 집중 모드(no shell).
  if (currentView === 'mock' || currentView === 'mockResult') {
    return shell(
      <MockExam
        mode={currentView}
        classifiedList={classifiedList}
        progress={progress}
        recordAnswer={recordAnswer}
        qidFn={qid}
        onNavigate={(v) => { setCurrentView(v); window.scrollTo(0, 0); }}
        onStartReview={startReview}
        fontScale={fontScale}
        browseExam={browseExam}
        examDates={examDates}
      />
    );
  }
  if (currentView === 'mockSession') {
    return (
      <div className="app-shell">
        <MockExam
          mode={currentView}
          classifiedList={classifiedList}
          progress={progress}
          recordAnswer={recordAnswer}
          qidFn={qid}
          onNavigate={(v) => { setCurrentView(v); window.scrollTo(0, 0); }}
          onStartReview={startReview}
          fontScale={fontScale}
          browseExam={browseExam}
          examDates={examDates}
        />
        {overlays}
      </div>
    );
  }

  // 2차 essay 모드 — 5 sub-view (subjects/chapters/questions/write/result)
  // write는 집중 모드(no shell), 나머지는 하단 nav 유지
  if (currentView === 'essay_subjects' || currentView === 'essay_chapters'
      || currentView === 'essay_questions' || currentView === 'essay_result') {
    return shell(
      <EssayMode
        mode={currentView}
        chapter={essayChapter}
        questionId={essayQuestionId}
        setChapter={setEssayChapter}
        setQuestionId={setEssayQuestionId}
        onNavigate={(v) => { setCurrentView(v); window.scrollTo(0, 0); }}
        fontScale={fontScale}
      />
    );
  }
  if (currentView === 'essay_write') {
    return (
      <div className="app-shell">
        <EssayMode
          mode={currentView}
          chapter={essayChapter}
          questionId={essayQuestionId}
          setChapter={setEssayChapter}
          setQuestionId={setEssayQuestionId}
          onNavigate={(v) => { setCurrentView(v); window.scrollTo(0, 0); }}
          fontScale={fontScale}
        />
        {overlays}
      </div>
    );
  }

  // 가이드 학습 모드: 한 개념의 문제를 난이도↑ 순으로 한 문제씩, 해설로 누적 학습
  if (currentView === 'study' && selectedGroup) {
    const shuffleMode = !selectedGroup.review && studyOrder === 'random';
    // 세션 내 안정 셔플: qid+studyNonce 해시 → 같은 세션에선 순서 고정
    const seededRank = (q) => {
      let h = studyNonce * 2654435761 >>> 0;
      const id = qid(q);
      for (let i = 0; i < id.length; i++) h = (h * 31 + id.charCodeAt(i)) >>> 0;
      return h;
    };
    const ordered = processedData
      .filter(selectedGroup.filterFn)
      .sort((a, b) => {
        if (shuffleMode) return seededRank(a) - seededRank(b);
        if (selectedGroup.review) {
          // 복습: 여러 번 틀린 것 먼저, 그다음 어려운 것 먼저
          const ra = (progress[qid(a)] && progress[qid(a)].reviewed) || 0;
          const rb = (progress[qid(b)] && progress[qid(b)].reviewed) || 0;
          if (ra !== rb) return rb - ra;
          const dda = a.difficulty ?? 0, ddb = b.difficulty ?? 0;
          if (dda !== ddb) return ddb - dda;
        } else {
          const da = a.difficulty ?? 99, db = b.difficulty ?? 99;
          if (da !== db) return da - db;               // 학습: 쉬운 문제부터
        }
        const ya = parseInt(a.year, 10), yb = parseInt(b.year, 10);
        if (ya !== yb) return yb - ya;                  // 최신 연도
        return parseInt(a.number, 10) - parseInt(b.number, 10);
      });
    const total = ordered.length;
    const idx = Math.min(studyIdx, Math.max(0, total - 1));
    const q = ordered[idx];
    const s = progressStats(ordered, progress);
    const pathParts = q ? [q.taxSubjectName, q.taxSubSubjectName, q.taxChapterName, q.taxSectionName, q.taxItemName].filter(Boolean) : [];
    const done = total > 0 && s.answered >= total;
    const goPrev = () => { clearAutoTimer(); setAutoPending(false); setStudyIdx(Math.max(0, idx - 1)); window.scrollTo(0, 0); };
    const goNext = () => { clearAutoTimer(); setAutoPending(false); setStudyIdx(Math.min(total - 1, idx + 1)); window.scrollTo(0, 0); };
    const baseAnswer = selectedGroup.review ? updateAnswer : recordAnswer;
    const handleAnswer = (qq, sel, correct) => {
      baseAnswer(qq, sel, correct);
      if (autoNext && idx < total - 1) {
        clearAutoTimer();
        setAutoPending(true);
        autoTimerRef.current = setTimeout(() => {
          autoTimerRef.current = null;
          setAutoPending(false);
          setStudyIdx(i => Math.min(total - 1, i + 1));
          window.scrollTo(0, 0);
        }, autoSec * 1000);
      }
    };
    return (
      <div className="app-container">
        {drillHeader(
          <button className="drill-action" onClick={() => setCurrentView('question_list')}>
            ▦ 목록
          </button>
        )}

        <div className="drill-head sticky">
          <div style={{ fontSize: '0.8rem', color: '#6b7280' }}>{selectedGroup.title}</div>
          {pathParts.length > 0 && (
            <div style={{ fontSize: '0.85rem', color: '#374151', margin: '6px 0', fontWeight: 600 }}>
              {pathParts.join(' ▸ ')}
            </div>
          )}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '8px' }}>
            <div style={{ flex: 1, height: '8px', background: '#e5e7eb', borderRadius: '999px', overflow: 'hidden' }}>
              <div style={{ width: `${total ? Math.round((s.answered / total) * 100) : 0}%`, height: '100%', background: 'var(--primary)', transition: 'width .3s' }} />
            </div>
            <span style={{ fontSize: '0.8rem', color: '#6b7280', whiteSpace: 'nowrap' }}>
              {idx + 1} / {total} · 정답 <b style={{ color: '#16a34a' }}>{s.correct}</b>
            </span>
          </div>
          <div style={{ display: 'flex', gap: '8px', marginTop: '10px', flexWrap: 'wrap' }}>
            {!selectedGroup.review && (
              <button
                onClick={() => { setStudyOrder(studyOrder === 'random' ? 'difficulty' : 'random'); setStudyIdx(0); setStudyNonce(n => n + 1); window.scrollTo(0, 0); }}
                style={{ border: '1px solid #d1d5db', background: '#fff', color: '#374151',
                  borderRadius: '999px', padding: '6px 12px', fontSize: '0.78rem', fontWeight: 700, cursor: 'pointer' }}
              >
                {studyOrder === 'random' ? '🔀 무작위 순서' : '↕ 난이도순'}
              </button>
            )}
            <button
              onClick={() => { const v = !autoNext; setAutoNext(v); if (!v) { clearAutoTimer(); setAutoPending(false); } }}
              style={{ border: `1px solid ${autoNext ? 'var(--primary)' : '#d1d5db'}`,
                background: autoNext ? 'var(--primary)' : '#fff', color: autoNext ? '#fff' : '#374151',
                borderRadius: '999px', padding: '6px 12px', fontSize: '0.78rem', fontWeight: 700, cursor: 'pointer' }}
            >
              ⏩ 자동 다음 {autoNext ? 'ON' : 'OFF'}
            </button>
            {autoNext && [3, 5, 8].map(sec => (
              <button key={sec} onClick={() => setAutoSec(sec)}
                style={{ border: `1px solid ${autoSec === sec ? 'var(--primary)' : '#d1d5db'}`,
                  background: autoSec === sec ? '#eff6ff' : '#fff', color: autoSec === sec ? 'var(--primary)' : '#6b7280',
                  borderRadius: '999px', padding: '6px 10px', fontSize: '0.74rem', fontWeight: 700, cursor: 'pointer' }}>
                {sec}초
              </button>
            ))}
          </div>
          {/* 키보드 단축키 안내 — desktop pointer:fine 환경에서만 (모바일엔 숨김) */}
          <div className="study-kbd-hint" style={{ marginTop: 8, fontSize: '0.7rem',
            color: '#9ca3af', display: 'none' }}>
            ⌨ 단축키: <b>1-9</b> 보기 선택 · <b>← →</b> 이전/다음 · <b>Enter</b> 다음
          </div>
        </div>

        <main
          style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}
          onTouchStart={(e) => { const t = e.changedTouches[0]; swipe.x = t.clientX; swipe.y = t.clientY; }}
          onTouchEnd={(e) => {
            const t = e.changedTouches[0];
            const dx = t.clientX - swipe.x, dy = t.clientY - swipe.y;
            if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return; // 가로 스와이프만
            if (dx < 0 && idx < total - 1) goNext();
            else if (dx > 0 && idx > 0) goPrev();
          }}
        >
          {q ? (
            <>
              {selectedGroup.resumeIdx > 0 && studyIdx === selectedGroup.resumeIdx && (
                <div style={{ background: '#eff6ff', border: '1px solid #bfdbfe', color: '#1d4ed8',
                  borderRadius: '10px', padding: '10px 14px', marginBottom: '12px', fontSize: '0.85rem', fontWeight: 600 }}>
                  ⏯️ 이어서 풀기 — {studyIdx + 1}번째 문제부터
                </div>
              )}
              <QuestionItem
                key={`${qid(q)}-${studyNonce}`}
                q={q}
                prior={selectedGroup.review ? undefined : progress[qid(q)]}
                onAnswer={handleAnswer}
                bmReason={bmReasonOf(bm[qid(q)])}
                onToggleBookmark={cycleBookmark}
                keyboard
              />
              {autoPending && (
                <div onClick={() => { clearAutoTimer(); setAutoPending(false); }}
                  style={{ marginTop: '10px', padding: '10px 14px', borderRadius: '10px', cursor: 'pointer',
                    background: '#eff6ff', border: '1px solid #bfdbfe', color: '#1d4ed8', fontSize: '0.85rem', fontWeight: 600, textAlign: 'center' }}>
                  ⏩ 잠시 후 다음 문제로… (탭하여 멈춤)
                </div>
              )}
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', marginTop: '8px' }}>
                <button
                  onClick={goPrev}
                  disabled={idx === 0}
                  style={{ flex: 1, padding: '14px', minHeight: '48px', borderRadius: '10px', border: '1px solid #d1d5db', background: '#fff', cursor: idx === 0 ? 'default' : 'pointer', color: idx === 0 ? '#d1d5db' : '#374151', fontWeight: 600 }}
                >← 이전</button>
                <button
                  onClick={goNext}
                  disabled={idx >= total - 1}
                  style={{ flex: 2, padding: '14px', minHeight: '48px', borderRadius: '10px', border: 'none', background: idx >= total - 1 ? '#e5e7eb' : 'var(--primary)', color: idx >= total - 1 ? '#9ca3af' : '#fff', cursor: idx >= total - 1 ? 'default' : 'pointer', fontWeight: 700 }}
                >다음 문제 →</button>
              </div>
              <div className="kbd-hint" style={{ textAlign: 'center', fontSize: '0.75rem', color: '#9ca3af', marginTop: '8px' }}>
                키보드 <b>1~5</b> 보기 · <b>←</b> 이전 · <b>→</b>·<b>Enter</b> 다음
              </div>
              <div className="swipe-hint" style={{ textAlign: 'center', fontSize: '0.75rem', color: '#9ca3af', marginTop: '8px' }}>
                ← 좌우로 밀어 이전·다음 →
              </div>
              {done && selectedGroup.review && (() => {
                const stillWrong = ordered.filter(x => { const p = progress[qid(x)]; return p && p.correct === false; });
                const cleared = total - stillWrong.length;
                return (
                  <div style={{ marginTop: '20px', padding: '20px', background: stillWrong.length ? '#fef2f2' : '#ecfdf5', border: `1px solid ${stillWrong.length ? '#fecaca' : '#a7f3d0'}`, borderRadius: '12px', textAlign: 'center' }}>
                    <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: '6px' }}>
                      {stillWrong.length ? '복습 1회전 완료' : '오답 전부 해결 🎉'}
                    </div>
                    <div style={{ color: '#374151', marginBottom: '14px' }}>
                      복습 {total}개 · 해결 <b style={{ color: '#16a34a' }}>{cleared}</b> · 여전히 오답 <b style={{ color: '#dc2626' }}>{stillWrong.length}</b>
                    </div>
                    {stillWrong.length > 0 ? (
                      <button onClick={() => startReview(stillWrong.map(qid), selectedGroup.title, selectedGroup.backView)}
                        style={{ padding: '12px 20px', borderRadius: '10px', border: 'none', background: '#ef4444', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>
                        여전히 틀린 {stillWrong.length}개 다시 풀기
                      </button>
                    ) : (
                      <button onClick={() => { const bv = selectedGroup.backView || 'review'; setSelectedGroup(null); setReviewSubject(null); setCurrentView(bv); window.scrollTo(0, 0); }}
                        style={{ padding: '12px 20px', borderRadius: '10px', border: 'none', background: '#16a34a', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>
                        {/* today면 오늘 복습으로 */}목록으로
                      </button>
                    )}
                  </div>
                );
              })()}
              {done && !selectedGroup.review && (
                <div style={{ marginTop: '20px', padding: '20px', background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '12px', textAlign: 'center' }}>
                  <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: '6px' }}>이 개념 학습 완료 🎉</div>
                  <div style={{ color: '#374151', marginBottom: '14px' }}>
                    {total}문제 중 정답 <b style={{ color: '#16a34a' }}>{s.correct}</b> · 오답 <b style={{ color: '#dc2626' }}>{s.scored - s.correct}</b>
                    {s.answered > s.scored && <> · 채점제외 <b style={{ color: '#6b7280' }}>{s.answered - s.scored}</b></>}
                    {s.accuracy !== null && <> · 정답률 <b>{s.accuracy}%</b></>}
                  </div>
                  {(() => {
                    const wrongNow = ordered.filter(x => { const p = progress[qid(x)]; return p && p.correct === false; });
                    return (
                      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', flexWrap: 'wrap' }}>
                        {wrongNow.length > 0 && (
                          <button onClick={() => startReview(wrongNow.map(qid), `${selectedGroup.title} 오답`, 'dashboard')}
                            style={{ padding: '12px 20px', borderRadius: '10px', border: 'none', background: '#ef4444', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>
                            틀린 {wrongNow.length}개만 다시
                          </button>
                        )}
                        <button onClick={() => {
                            clearMany(ordered.map(qid));   // 이 개념 진행 초기화 → 재측정
                            setStudyIdx(0);
                            setStudyNonce(n => n + 1);     // 카드 강제 리마운트(이전 응답 표시 제거)
                            window.scrollTo(0, 0);
                          }}
                          style={{ padding: '12px 20px', borderRadius: '10px', border: '1px solid #bfdbfe', background: '#fff', color: '#1d4ed8', fontWeight: 700, cursor: 'pointer' }}>
                          처음부터 다시
                        </button>
                      </div>
                    );
                  })()}
                </div>
              )}
            </>
          ) : (
            <div className="empty-state"><span className="emoji">📭</span><div className="title">문제가 없습니다</div></div>
          )}
        </main>
        {overlays}
      </div>
    );
  }

  if (currentView === 'question_list' && selectedGroup) {
    // 필터링된 문제를 연도 내림차순, 문제 번호 오름차순으로 정렬
    const filteredQuestions = processedData
      .filter(selectedGroup.filterFn)
      .sort((a, b) => {
        const yearA = parseInt(a.year, 10);
        const yearB = parseInt(b.year, 10);
        if (yearA !== yearB) return yearB - yearA; // 연도 내림차순
        return parseInt(a.number, 10) - parseInt(b.number, 10); // 번호 오름차순
      });
    
    return (
      <div className="app-container">
        {drillHeader(
          <button className="drill-action" onClick={() => { scrollMem.qlist = window.scrollY; setStudyIdx(0); setCurrentView('study'); window.scrollTo(0, 0); }}>
            📚 학습
          </button>
        )}

        <div className="drill-head">
          <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '4px' }}>{selectedGroup.subtitle}</div>
          <h1 className="screen-title">{selectedGroup.title} ({filteredQuestions.length}문제)</h1>
          {(() => {
            const s = progressStats(filteredQuestions, progress);
            const pct = s.total ? Math.round((s.answered / s.total) * 100) : 0;
            return (
              <div style={{ marginTop: '12px' }}>
                <div style={{ height: '8px', background: '#e5e7eb', borderRadius: '999px', overflow: 'hidden' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: 'var(--primary)', transition: 'width .3s' }} />
                </div>
                <div style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: '6px' }}>
                  푼 문제 <b>{s.answered}/{s.total}</b> · 정답 <b style={{ color: '#16a34a' }}>{s.correct}</b>
                </div>
              </div>
            );
          })()}
        </div>

        <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
          {filteredQuestions.map((q) => (
            <QuestionItem
              key={qid(q)}
              q={q}
              prior={progress[qid(q)]}
              onAnswer={recordAnswer}
              bmReason={bmReasonOf(bm[qid(q)])}
              onToggleBookmark={cycleBookmark}
            />
          ))}
        </main>
      </div>
    );
  }


  // Drill-down 위치 표시 — 마지막은 굵게(현재), 나머지는 탭하면 그 단계로 복귀
  const renderBreadcrumb = () => {
    const crumbs = [];
    if (taxScope) {
      crumbs.push({ label: taxScope.label, onClick: () => {
        setTaxSubject(null); setTaxSubSubject(null); setTaxChapter(null); setTaxSection(null);
        setCurrentView('tax_subjects');
      }});
    } else if (browseExam) {
      crumbs.push({ label: browseExam, onClick: () => {
        setTaxSubject(null); setTaxSubSubject(null); setTaxChapter(null); setTaxSection(null);
        setCurrentView('dashboard');
      }});
    }
    if (taxSubject) {
      crumbs.push({ label: taxSubject, onClick: () => {
        setTaxSubSubject(null); setTaxChapter(null); setTaxSection(null);
        setCurrentView('tax_sub_subjects');
      }});
    }
    if (taxSubSubject) {
      crumbs.push({ label: taxSubSubject, onClick: () => {
        setTaxChapter(null); setTaxSection(null);
        setCurrentView('tax_chapters');
      }});
    }
    if (taxChapter) {
      crumbs.push({ label: taxChapter, onClick: () => {
        setTaxSection(null); setCurrentView('tax_sections');
      }});
    }
    if (taxSection) {
      crumbs.push({ label: taxSection, onClick: () => setCurrentView('tax_items') });
    }
    if (crumbs.length <= 1) return null;  // 1단계뿐이면 안 보임
    return (
      <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center',
        padding: '12px 20px 4px', fontSize: '0.78rem', color: '#6b7280' }}>
        {crumbs.map((c, i) => (
          <span key={i} style={{ display: 'inline-flex', alignItems: 'center' }}>
            {i > 0 && <span style={{ margin: '0 6px', color: '#d1d5db' }}>›</span>}
            {i === crumbs.length - 1 ? (
              <span style={{ color: '#111827', fontWeight: 700 }}>{c.label}</span>
            ) : (
              <button onClick={c.onClick} style={{
                border: 'none', background: 'none', padding: 0, cursor: 'pointer',
                color: '#1d4ed8', fontSize: 'inherit', fontWeight: 600
              }}>{c.label}</button>
            )}
          </span>
        ))}
      </div>
    );
  };

  const renderStudyGrid = (title, subtitle, groups) => {
    // 현재 tax 드릴 위치가 AI 학습 leaf로 매핑되면 점프 버튼 노출
    const tax = { subject: taxSubject, sub_subject: taxSubSubject, chapter: taxChapter, section: taxSection };
    const aiLeaf = (taxChapter || taxSection) ? findAiLeafForTax(tax) : null;
    // 카드별 AI 진척 — group.title을 절 또는 관으로 해서 leaf 찾기
    const aiMastery = getAiMastery();
    const groupAiLeaf = (group) => {
      if (!group || !group.title) return null;
      const isItemGrid = currentView === 'tax_items';
      return findAiLeafForTax({
        subject: taxSubject,
        sub_subject: taxSubSubject,
        chapter: taxChapter,
        section: isItemGrid ? taxSection : group.title,
        item: isItemGrid ? group.title : null,
      });
    };
    return (
    <div className="app-container">
      {drillHeader()}
      {renderBreadcrumb()}

      <div className="drill-head">
        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '4px' }}>{subtitle}</div>
        <h1 className="screen-title">{title}</h1>
      </div>
      {aiLeaf && (
        <div style={{ padding: '8px 20px 0' }}>
          <button
            onClick={() => jumpToAILearn(aiLeaf)}
            style={{
              width: '100%', padding: '10px 14px',
              background: 'linear-gradient(90deg, #eef2ff 0%, #fce7f3 100%)',
              border: '1px solid #c7d2fe', borderRadius: 10, color: '#4338ca',
              fontSize: '0.88rem', fontWeight: 700, cursor: 'pointer',
              display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            }}
          >
            <span>🎓 AI 튜터로 이 단원 배우기</span>
            <span style={{ fontSize: '0.75rem', color: '#6366f1', fontWeight: 600 }}>
              {aiLeaf.path.slice(-1)[0]} ›
            </span>
          </button>
        </div>
      )}
      
      <main className="main-content" style={{ marginTop: '20px' }}>
        <div className="study-grid">
          {groups.map((group, idx) => {
            const isAll = group.type && group.type.startsWith('play_all');
            const s = progressStats(cardQuestions(group), progress);
            const pct = s.total ? Math.round((s.answered / s.total) * 100) : 0;
            const dm = s.level ? (DIFFICULTY_META[s.level] || null) : null;
            return (
              <div key={idx} className="study-card" onClick={() => handleGroupClick(group)} style={isAll ? { background: '#eff6ff', borderColor: '#bfdbfe' } : {}}>
                <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                  <div className="card-badge" style={isAll ? { background: 'var(--primary)', color: '#fff', border: 'none' } : {}}>{group.tag}</div>
                  {dm && (
                    <span style={{ fontSize: '0.72rem', fontWeight: 700, padding: '2px 8px', borderRadius: '999px', background: dm.bg, color: dm.fg }}>
                      난이도 {s.avgDiff.toFixed(1)}
                    </span>
                  )}
                </div>
                <div className="card-subtitle">{group.subtitle}</div>
                <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{group.title}</h3>
                <div className="card-total">총 {group.total} 문제 {s.answered > 0 && <span style={{ color: 'var(--primary)', fontWeight: 700 }}>· {pct}%</span>}</div>
                <div className="card-progress-container">
                  <div className="card-progress-fill" style={{ width: `${pct}%` }}></div>
                </div>
                {(() => {
                  const gLeaf = groupAiLeaf(group);
                  const gm = gLeaf ? aiMastery[gLeaf.id] : null;
                  if (!gm || !gm.coverage) return null;
                  const aiPct = Math.round(gm.coverage * 100);
                  return (
                    <div style={{ marginTop: 4, fontSize: '0.72rem', color: '#4338ca', display: 'flex', alignItems: 'center', gap: 4 }}>
                      <span>🎓 AI {aiPct}%</span>
                      <div style={{ flex: 1, height: 3, background: '#e5e7eb', borderRadius: 2, overflow: 'hidden' }}>
                        <div style={{ width: `${aiPct}%`, height: '100%', background: '#4f46e5' }} />
                      </div>
                      {gm.status === 'mastered' && <span style={{ color: '#047857' }}>✓</span>}
                    </div>
                  );
                })()}
                <div className="play-btn" style={isAll ? { background: 'var(--primary)', color: '#fff' } : {}}>선택</div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
    );
  };

  // ===== 단일 v4 분류축 뷰 (시험별/과목별/단원별/연도별 공용) =====
  const scopePrefix = taxScope ? `${taxScope.label} · ` : '';
  if (currentView === 'tax_subjects') return renderStudyGrid(taxScope ? taxScope.label : '과목 선택', taxScope ? `${taxScope.label} 과목별` : '단원별 학습', taxSubjectGroups);
  if (currentView === 'tax_sub_subjects' && taxSubject) return renderStudyGrid(`${scopePrefix}${taxSubject}`, '세부과목 / 장 선택', taxSubSubjectGroups);
  if (currentView === 'tax_chapters' && taxSubSubject) return renderStudyGrid(`${scopePrefix}${taxSubSubject}`, '장(Chapter) 선택', taxChapterGroups);
  if (currentView === 'tax_sections' && taxChapter) return renderStudyGrid(`${scopePrefix}${taxChapter}`, '절(Section) 선택', taxSectionGroups);
  if (currentView === 'tax_items' && taxSection) return renderStudyGrid(`${scopePrefix}${taxSection}`, '관(Item) 선택', taxItemGroups);

  // Dashboard View

  if (loading) {
    const stage = loadPct < 5 ? '시험 목록 확인 중'
      : loadPct < 100 ? `기출문제 ${loadPct}% 받는 중 (13시험 동시 다운로드)`
      : '정리하는 중…';
    return (
      <div className="boot">
        <div className="boot-mark">감정평가사 기출</div>
        <div className="boot-title">1차 기출 12,000+ 문제</div>
        <div className="boot-bar"><div className="boot-fill" style={{ width: `${Math.max(4, loadPct)}%` }} /></div>
        <div className="boot-pct" style={{ fontSize: '0.85rem' }}>{stage}</div>
        <div className="boot-note">최초 1회만 받으면 다음부터 오프라인에서도 바로 열려요</div>
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="boot">
        <div className="boot-mark">감정평가사 기출</div>
        <div className="boot-title" style={{ marginBottom: 8 }}>잠깐 연결이 끊겼어요</div>
        <div className="boot-note" style={{ marginBottom: 22 }}>
          네트워크를 확인하고 다시 시도해 주세요. 데이터는 안전합니다.
        </div>
        <button onClick={() => window.location.reload()} className="boot-retry">
          다시 시도
        </button>
      </div>
    );
  }

  if (totalQuestions === 0) {
    return (
      <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#f8fafc', color: '#6b7280', padding: '24px', textAlign: 'center' }}>
        <div style={{ fontWeight: 700, fontSize: '1.2rem', color: '#374151', marginBottom: '8px' }}>표시할 분류된 문제가 없습니다</div>
        <div>데이터가 비어 있거나 분류가 아직 반영되지 않았습니다.</div>
      </div>
    );
  }

  if (currentView === 'search') {
    const activeCount = filters.exams.length + filters.subjects.length + filters.years.length + filters.diffs.length + (filters.kw.trim() ? 1 : 0) + (filters.cleanOnly ? 1 : 0);
    const shown = filteredResults.slice(0, 200);
    const chip = (on) => ({
      padding: '6px 12px', borderRadius: '999px', fontSize: '0.85rem', cursor: 'pointer',
      border: on ? '1px solid var(--primary)' : '1px solid #d1d5db',
      background: on ? 'var(--primary)' : '#fff', color: on ? '#fff' : '#374151',
    });
    const groupChips = (label, items, sel, k, fmt) => (
      <div style={{ marginBottom: '14px' }}>
        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#6b7280', marginBottom: '6px' }}>{label}</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          {items.map(it => (
            <span key={String(it)} style={chip(sel.includes(it))} onClick={() => toggleFilter(k, it)}>
              {fmt ? fmt(it) : it}
            </span>
          ))}
        </div>
      </div>
    );
    return shell(
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => setCurrentView('dashboard')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>문제풀이</span>
          </button>
        </header>
        <div className="screen-head">
          <h1 className="screen-title">
            🔍 검색
            {browseExam && (
              <span style={{ marginLeft: 8, fontSize: '0.78rem', color: '#1d4ed8',
                fontWeight: 700, padding: '3px 9px', background: '#eff6ff',
                borderRadius: 999, verticalAlign: 'middle' }}>
                {browseExam} 모드
              </span>
            )}
          </h1>
        </div>
        <div style={{ padding: '20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <input
            value={filters.kw}
            onChange={(e) => setFilters(f => ({ ...f, kw: e.target.value }))}
            placeholder="문제·보기·해설 키워드 검색"
            style={{ width: '100%', padding: '12px 14px', fontSize: '1rem', border: '1px solid #d1d5db', borderRadius: '10px', marginBottom: '16px', boxSizing: 'border-box' }}
          />
          {groupChips('시험', filterOptions.exams, filters.exams, 'exams')}
          {groupChips('과목', filterOptions.subjects, filters.subjects, 'subjects')}
          {groupChips('연도', filterOptions.years, filters.years, 'years', (y) => `${y}년`)}
          {groupChips('난이도', filterOptions.diffs, filters.diffs, 'diffs', (d) => `난이도 ${d}`)}
          <div style={{ marginBottom: '10px' }}>
            <span
              style={chip(filters.cleanOnly)}
              onClick={() => setFilters(f => ({ ...f, cleanOnly: !f.cleanOnly }))}
            >
              ✓ 정답·보기 있는 문항만
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '6px' }}>
            <span style={{ fontWeight: 700 }}>{activeCount ? `${filteredResults.length}문제` : '필터를 선택하세요'}</span>
            {activeCount > 0 && (
              <button onClick={clearFilters} style={{ border: 'none', background: '#f3f4f6', padding: '6px 12px', borderRadius: '8px', cursor: 'pointer', fontSize: '0.85rem' }}>필터 초기화</button>
            )}
          </div>
          {filteredResults.length > 0 && (
            <button
              onClick={() => startReview(filteredResults.map(qid), `검색 결과 학습 (${filteredResults.length})`, 'search')}
              style={{ width: '100%', marginTop: '14px', padding: '14px', border: 'none', borderRadius: '12px',
                background: 'var(--primary)', color: '#fff', fontWeight: 800, fontSize: '0.95rem', cursor: 'pointer' }}
            >
              ▶ 이 결과로 가이드 학습 시작 ({filteredResults.length}문제)
            </button>
          )}
        </div>
        <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
          {shown.map(q => (
            <QuestionItem key={qid(q)} q={q} prior={progress[qid(q)]} onAnswer={recordAnswer} bmReason={bmReasonOf(bm[qid(q)])} onToggleBookmark={cycleBookmark} />
          ))}
          {filteredResults.length > shown.length && (
            <div style={{ textAlign: 'center', color: '#6b7280', padding: '16px' }}>
              상위 {shown.length}개만 표시 중 (총 {filteredResults.length}개) — 필터를 좁혀주세요
            </div>
          )}
        </main>
      </div>
    );
  }

  if (currentView === 'profile') {
    const prof = loadProfile();
    let firstTs = null;
    for (const k in progress) { const t = progress[k] && progress[k].ts; if (t && (firstTs == null || t < firstTs)) firstTs = t; }
    const fmt = (iso) => { const d = new Date(iso); return `${d.getFullYear()}.${d.getMonth() + 1}.${d.getDate()}`; };
    const daysAgo = prof.lastBackup ? Math.floor((nowTs - new Date(prof.lastBackup).getTime()) / 86400000) : null;
    const stale = overall.answered > 0 && (daysAgo == null || daysAgo >= 7);
    return shell(
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => setCurrentView('home')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>홈</span>
          </button>
        </header>
        <div className="screen-head"><h1 className="screen-title">👤 내 프로필</h1></div>
        <main className="main-content" style={{ marginTop: '16px' }}>
          <section style={{ background: '#fff', borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
            <label style={{ fontSize: '0.8rem', fontWeight: 700, color: '#6b7280' }}>닉네임</label>
            <input
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              placeholder="학습자 이름"
              style={{ width: '100%', padding: '11px 14px', marginTop: '6px', fontSize: '1rem',
                border: '1px solid #d1d5db', borderRadius: '10px', boxSizing: 'border-box' }}
            />
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginTop: '16px' }}>
              {[
                ['학습 시작', firstTs ? fmt(firstTs) : '–'],
                ['총 학습', `${overall.answered}문제`],
                ['정답률', overall.accuracy == null ? '–' : `${overall.accuracy}%`],
                ['연속 학습', `${analytics.streak}일`],
              ].map(([k, v]) => (
                <div key={k} style={{ background: '#f8fafc', borderRadius: '10px', padding: '12px', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.05rem', fontWeight: 800 }}>{v}</div>
                  <div style={{ fontSize: '0.72rem', color: '#6b7280', marginTop: '2px' }}>{k}</div>
                </div>
              ))}
            </div>
          </section>

          <section style={{ background: stale ? '#fffbeb' : '#fff', border: `1px solid ${stale ? '#fde68a' : '#e5e7eb'}`,
            borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
            <div style={{ fontWeight: 800, marginBottom: '4px' }}>데이터 백업</div>
            <div style={{ fontSize: '0.82rem', color: '#6b7280', marginBottom: '12px' }}>
              학습 기록은 이 기기에만 저장돼요. 백업 파일을 보관하면 기기를 바꿔도 그대로 복원할 수 있어요.
              {prof.lastBackup
                ? <> 마지막 백업: <b>{daysAgo === 0 ? '오늘' : `${daysAgo}일 전`}</b>.</>
                : <> <b>아직 백업한 적 없어요.</b></>}
              {stale && <span style={{ color: '#b45309' }}> 백업을 권장합니다.</span>}
            </div>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              <button onClick={exportUserData}
                style={{ flex: 1, minWidth: 110, padding: '12px', borderRadius: '10px', border: 'none',
                  background: 'var(--primary)', color: '#fff', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                ⬇ 백업 내보내기
              </button>
              <button onClick={() => fileRef.current && fileRef.current.click()}
                style={{ flex: 1, minWidth: 110, padding: '12px', borderRadius: '10px', border: '1px solid #d1d5db',
                  background: '#fff', color: '#374151', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                ⬆ 백업 가져오기
              </button>
            </div>
            <button onClick={() => { if (window.confirm('모든 학습 기록을 삭제할까요? 되돌릴 수 없습니다.')) { resetUserData(); window.location.reload(); } }}
              style={{ width: '100%', marginTop: '8px', padding: '11px', borderRadius: '10px', border: '1px solid #fecaca',
                background: '#fef2f2', color: '#b91c1c', fontWeight: 700, fontSize: '0.85rem', cursor: 'pointer' }}>
              전체 초기화
            </button>
            <input ref={fileRef} type="file" accept="application/json,.json" onChange={onImportFile} style={{ display: 'none' }} />
          </section>

          <section style={{ background: '#fff', borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '12px' }}>
            <div style={{ fontWeight: 800, marginBottom: '4px' }}>☁ 클라우드 동기화</div>
            {!cloudEnabled ? (
              <div style={{ fontSize: '0.82rem', color: '#9ca3af' }}>설정되지 않음 (파일 백업만 사용)</div>
            ) : authUser ? (
              <>
                <div style={{ fontSize: '0.82rem', color: '#6b7280', marginBottom: '12px' }}>
                  로그인: <b>{authUser.email}</b>
                  {loadProfile().lastCloud && <> · 마지막 동기화 {new Date(loadProfile().lastCloud).toLocaleString('ko-KR')}</>}
                  <br />다른 기기에서도 같은 계정으로 로그인하면 이어집니다. (앱을 닫을 때 자동 백업)
                </div>
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  <button onClick={() => cloudPush(false)}
                    style={{ flex: 1, minWidth: 120, padding: '12px', borderRadius: '10px', border: 'none', background: 'var(--primary)', color: '#fff', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                    ☁⬆ 클라우드에 백업
                  </button>
                  <button onClick={cloudPull}
                    style={{ flex: 1, minWidth: 120, padding: '12px', borderRadius: '10px', border: '1px solid #d1d5db', background: '#fff', color: '#374151', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                    ☁⬇ 클라우드에서 복원
                  </button>
                </div>
                <button onClick={async () => { await supabase.auth.signOut(); setCloudMsg('로그아웃되었어요.'); }}
                  style={{ width: '100%', marginTop: '8px', padding: '10px', borderRadius: '10px', border: '1px solid #d1d5db', background: '#fff', color: '#6b7280', fontWeight: 700, fontSize: '0.82rem', cursor: 'pointer' }}>
                  로그아웃
                </button>
              </>
            ) : (
              <>
                <div style={{ fontSize: '0.82rem', color: '#6b7280', marginBottom: '12px' }}>
                  이메일로 로그인하면 여러 기기에서 학습 기록이 자동으로 이어져요.
                </div>
                <input value={cloudEmail} onChange={(e) => setCloudEmail(e.target.value)} placeholder="이메일" type="email"
                  style={{ width: '100%', padding: '11px 14px', marginBottom: '8px', border: '1px solid #d1d5db', borderRadius: '10px', boxSizing: 'border-box' }} />
                <input value={cloudPw} onChange={(e) => setCloudPw(e.target.value)} placeholder="비밀번호(6자 이상)" type="password"
                  style={{ width: '100%', padding: '11px 14px', marginBottom: '10px', border: '1px solid #d1d5db', borderRadius: '10px', boxSizing: 'border-box' }} />
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button onClick={() => cloudAuth('signin')}
                    style={{ flex: 1, padding: '12px', borderRadius: '10px', border: 'none', background: 'var(--primary)', color: '#fff', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                    로그인
                  </button>
                  <button onClick={() => cloudAuth('signup')}
                    style={{ flex: 1, padding: '12px', borderRadius: '10px', border: '1px solid #d1d5db', background: '#fff', color: '#374151', fontWeight: 700, fontSize: '0.88rem', cursor: 'pointer' }}>
                    회원가입
                  </button>
                </div>
              </>
            )}
            {cloudMsg && <div style={{ fontSize: '0.8rem', color: '#1d4ed8', marginTop: '10px' }}>{cloudMsg}</div>}
          </section>

          <div style={{ fontSize: '0.75rem', color: '#9ca3af', textAlign: 'center', padding: '0 8px' }}>
            파일 백업도 함께 쓰면 가장 안전해요.
          </div>
        </main>
      </div>
    );
  }

  if (currentView === 'status') {
    // ─── 데이터 통합 ────────────────────────────────────────
    const cv = modeCoverage || coverage;
    const coachUsed = modeCoach || coach;
    const analyticsUsed = modeAnalytics || analytics;
    const aiMastery = getAiMastery();
    const aiDueArr = getAiDue();
    const allLeavesFlat = Object.values(leavesBySubject).flat();
    const flatLeafById = new Map(allLeavesFlat.map((l) => [l.id, l]));

    // 종합 학습률 = quiz coverage 50% + AI coverage 평균 50%
    const quizLearnedPct = cv.total ? ((cv.learned + cv.mastered + cv.review) / cv.total) : 0;
    const aiCovAvg = (() => {
      if (allLeavesFlat.length === 0) return 0;
      const sum = allLeavesFlat.reduce((a, l) => a + (aiMastery[l.id]?.coverage || 0), 0);
      return sum / allLeavesFlat.length;
    })();
    const overallPct = Math.round((quizLearnedPct * 0.5 + aiCovAvg * 0.5) * 100);
    const todoCount = srs.due.length + aiDueArr.length;

    // 5과목 매트릭스 (quiz + AI 통합) — 통합 점수 낮은 순 정렬
    const subjectMatrix = AI_SUBJECTS.map((s) => {
      const aiKs = Object.keys(aiMastery).filter((k) => k.startsWith(s.id + '__') || k.startsWith(s.id + '_'));
      const aiCov = aiKs.length ? aiKs.reduce((a, k) => a + (aiMastery[k]?.coverage || 0), 0) / aiKs.length : 0;
      const aiMaster = aiKs.filter((k) => aiMastery[k]?.status === 'mastered').length;
      const aiTotal = (leavesBySubject[s.id] || []).length;

      // 2차는 답안 평균 점수 활용
      const isStage2 = s.stage === 2;
      const avgScorePct = isStage2 && aiKs.length
        ? aiKs.reduce((a, k) => a + (aiMastery[k]?.avg_score_pct || 0), 0) / aiKs.length / 100
        : 0;
      const answerCountSum = isStage2 ? aiKs.reduce((a, k) => a + (aiMastery[k]?.answer_count || 0), 0) : 0;

      const quizSubj = analyticsUsed.subjects.find((x) => x.name === s.title);
      const quizAcc = quizSubj && quizSubj.scored >= 5 ? quizSubj.correct / quizSubj.scored : null;
      const quizCov = quizSubj && quizSubj.total ? quizSubj.scored / quizSubj.total : 0;
      const quizTotal = quizSubj?.total || 0;
      const quizScored = quizSubj?.scored || 0;

      // 통합 점수 — stage별 다른 산식
      let score;
      if (isStage2) {
        score = aiCov * 0.5 + avgScorePct * 0.5;  // 1차 기출 없음 가정
      } else {
        score = aiCov * 0.4 + quizCov * 0.3 + (quizAcc || 0) * 0.3;
      }
      const weakAiCount = ((aiWeakPathsBySubject || {})[s.id] || []).length;
      return {
        s, aiCov, aiMaster, aiTotal, quizAcc, quizCov, quizTotal, quizScored, score, weakAiCount,
        isStage2, avgScorePct, answerCountSum,
      };
    }).sort((a, b) => a.score - b.score);
    const matrixStage1 = subjectMatrix.filter((x) => !x.isStage2);
    const matrixStage2 = subjectMatrix.filter((x) => x.isStage2);

    // leaf 통합 score — quiz + AI
    const leafUnified = allLeavesFlat
      .map((l) => {
        const m = aiMastery[l.id] || {};
        const qs = quizStatsByLeaf[l.id];
        const aiCov = m.coverage || 0;
        const quizAcc = qs && qs.answered > 0 ? qs.accuracy : 0;
        const quizCov = qs && qs.total > 0 ? qs.coverage : 0;
        const score = aiCov * 0.5 + quizAcc * 0.3 + quizCov * 0.2;
        const subjId = (l.id || '').split('__')[0];
        const sMeta = AI_SUBJECTS.find((x) => x.id === subjId);
        return { leaf: l, sMeta, aiCov, quizAcc, quizCov, qs, m, score };
      })
      .filter((x) => x.aiCov > 0 || (x.qs && x.qs.answered > 0));
    const topLeaves = [...leafUnified].sort((a, b) => b.score - a.score).slice(0, 5);
    const bottomLeaves = [...leafUnified].filter((x) => x.score < 0.5).sort((a, b) => a.score - b.score).slice(0, 5);

    const kpi = (v, sub, color, bg) => (
      <div style={{ flex: 1, background: bg || '#fff', borderRadius: '12px', padding: '14px 10px', textAlign: 'center', boxShadow: 'var(--shadow-sm)' }}>
        <div style={{ fontSize: '1.25rem', fontWeight: 800, color: color || '#111827' }}>{v}</div>
        <div style={{ fontSize: '0.72rem', color: '#6b7280', marginTop: '2px' }}>{sub}</div>
      </div>
    );

    // ─── 시각화 헬퍼 ────────────────────────────────────────
    // SVG 도넛 게이지 (value 0~1)
    const Donut = ({ size = 70, value, color, stroke = 8, centerText, centerSub }) => {
      const r = 50 - stroke / 2;
      const C = 2 * Math.PI * r;
      const v = Math.max(0, Math.min(1, value || 0));
      return (
        <svg viewBox="0 0 100 100" width={size} height={size} style={{ display: 'block' }}>
          <circle cx="50" cy="50" r={r} fill="none" stroke="#f3f4f6" strokeWidth={stroke} />
          <circle cx="50" cy="50" r={r} fill="none" stroke={color} strokeWidth={stroke}
            strokeDasharray={`${(C * v).toFixed(2)} ${C.toFixed(2)}`}
            strokeLinecap="round"
            transform="rotate(-90 50 50)" />
          {centerText != null && (
            <text x="50" y={centerSub ? 47 : 55} textAnchor="middle" fontSize="22" fontWeight="800" fill={color}>
              {centerText}
            </text>
          )}
          {centerSub && (
            <text x="50" y="65" textAnchor="middle" fontSize="11" fill="#9ca3af">{centerSub}</text>
          )}
        </svg>
      );
    };

    // 최근 56일 활동 잔디 (GitHub 스타일)
    const last56Days = (() => {
      const arr = [];
      const today = new Date(); today.setHours(0, 0, 0, 0);
      const counts = {};
      Object.values(progress || {}).forEach((p) => {
        if (!p?.ts) return;
        const d = new Date(p.ts); d.setHours(0, 0, 0, 0);
        const k = d.toDateString();
        counts[k] = (counts[k] || 0) + 1;
      });
      // AI 학습 메시지 횟수도 가산 (ailearn-usage)
      try {
        const usage = JSON.parse(localStorage.getItem('ailearn-usage') || '{}');
        Object.entries(usage).forEach(([yyyymmdd, u]) => {
          const [y, m, d] = yyyymmdd.split('-').map(Number);
          if (!y || !m || !d) return;
          const dt = new Date(y, m - 1, d);
          const k = dt.toDateString();
          counts[k] = (counts[k] || 0) + (u.messages || 0);
        });
      } catch { /* noop */ }
      for (let i = 55; i >= 0; i--) {
        const d = new Date(today); d.setDate(today.getDate() - i);
        arr.push({ date: d, count: counts[d.toDateString()] || 0, isToday: i === 0 });
      }
      return arr;
    })();
    const heatMax = Math.max(1, ...last56Days.map((x) => x.count));

    // 5과목 레이더 차트 — subjectMatrix를 고정 순서로 다시 정렬
    const radarStats = AI_SUBJECTS.map((s) => {
      const found = subjectMatrix.find((x) => x.s.id === s.id);
      return found || { s, score: 0, aiCov: 0, quizCov: 0, quizAcc: 0 };
    });
    return shell(
      <div className="app-container">
        <div className="screen-head">
          <h1 className="screen-title">
            📊 학습 현황
            {browseExam && (
              <span style={{ marginLeft: 8, fontSize: '0.78rem', color: '#1d4ed8',
                fontWeight: 700, padding: '3px 9px', background: '#eff6ff',
                borderRadius: 999, verticalAlign: 'middle' }}>
                {browseExam} 모드
              </span>
            )}
          </h1>
        </div>
        <main className="main-content" style={{ marginTop: '16px' }}>
          {/* 모드 pill — status 통계의 범위를 시험별로 전환 */}
          <div style={{ marginBottom: 14 }}>{renderModePicker()}</div>

          {/* ① D-DAY 미니 카드 (1차/2차) */}
          {(() => {
            const d1 = daysUntil(examDates[`${PRIMARY_EXAM}_1차`] || examDates[PRIMARY_EXAM]);
            const d2 = daysUntil(examDates[`${PRIMARY_EXAM}_2차`]);
            if (d1 == null && d2 == null) return null;
            const dColor = (d) => d == null ? '#9ca3af'
              : d < 0 ? '#9ca3af' : d <= 30 ? '#dc2626' : d <= 90 ? '#ea580c' : '#1d4ed8';
            const dPill = (label, d) => d == null ? null : (
              <div style={{ flex: 1, background: '#fff', borderRadius: 12, padding: '10px 12px',
                display: 'flex', alignItems: 'center', gap: 8, boxShadow: 'var(--shadow-sm)' }}>
                <span style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700 }}>{label}</span>
                <span style={{ marginLeft: 'auto', fontSize: '1.05rem', fontWeight: 800, color: dColor(d) }}>
                  D{d > 0 ? '-' : '+'}{Math.abs(d)}
                </span>
              </div>
            );
            return (
              <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
                {dPill('1차', d1)}
                {dPill('2차', d2)}
              </div>
            );
          })()}

          {/* ② 종합 KPI — quiz + AI 통합 */}
          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
            {kpi(`${overallPct}%`, '종합 학습률', '#4f46e5', '#eef2ff')}
            {kpi(coachUsed.skillAcc == null ? '–' : `${coachUsed.skillAcc}%`, '기출 정답률', '#16a34a')}
            {kpi(`${analytics.streak}일`, '연속 학습', '#ea580c')}
            {kpi(todoCount, '오늘 할 일', todoCount > 0 ? '#dc2626' : '#9ca3af')}
          </div>

          {/* ②.5 합격 코치 + 5과목 레이더 — 종합 시각화 */}
          {coachUsed.readiness != null && (
            <section style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: '16px',
              padding: '16px', marginBottom: '16px', boxShadow: 'var(--shadow-md)' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, alignItems: 'center' }}>
                {/* 좌: 합격 코치 도넛 */}
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '0.78rem', fontWeight: 700, color: '#374151', marginBottom: 6 }}>🎯 합격 준비도</div>
                  <div style={{ display: 'flex', justifyContent: 'center' }}>
                    <Donut
                      size={140}
                      value={Math.min(1, coachUsed.readiness / COACH_TARGET)}
                      color={coachUsed.readiness >= COACH_TARGET ? '#16a34a' : '#4f46e5'}
                      stroke={10}
                      centerText={`${coachUsed.readiness}%`}
                      centerSub={`목표 ${COACH_TARGET}%`}
                    />
                  </div>
                  <div style={{ fontSize: '0.78rem', color: '#374151', fontWeight: 600, marginTop: 8 }}>{coachUsed.verdict}</div>
                </div>
                {/* 우: 5과목 레이더 */}
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '0.78rem', fontWeight: 700, color: '#374151', marginBottom: 6 }}>📊 5과목 균형</div>
                  {(() => {
                    const cx = 80, cy = 80, R = 60;
                    const N = radarStats.length;
                    const ang = (i) => (Math.PI * 2 * i) / N - Math.PI / 2;
                    const pt = (i, v) => ({
                      x: cx + R * v * Math.cos(ang(i)),
                      y: cy + R * v * Math.sin(ang(i)),
                    });
                    const polyPts = radarStats.map((st, i) => pt(i, st.score)).map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
                    return (
                      <svg viewBox="0 0 160 160" style={{ width: '100%', maxWidth: 180 }}>
                        {[0.25, 0.5, 0.75, 1].map((r) => (
                          <polygon key={r}
                            points={radarStats.map((_, i) => {
                              const p = pt(i, r);
                              return `${p.x.toFixed(1)},${p.y.toFixed(1)}`;
                            }).join(' ')}
                            fill="none" stroke="#f3f4f6" strokeWidth="1" />
                        ))}
                        {radarStats.map((_, i) => {
                          const p = pt(i, 1);
                          return <line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="#e5e7eb" strokeWidth="1" />;
                        })}
                        <polygon points={polyPts} fill="#4f46e5" fillOpacity="0.22" stroke="#4f46e5" strokeWidth="2" />
                        {radarStats.map((st, i) => {
                          const p = pt(i, st.score);
                          return <circle key={i} cx={p.x} cy={p.y} r="3.5" fill="#4f46e5" />;
                        })}
                        {radarStats.map((st, i) => {
                          const p = pt(i, 1.18);
                          return (
                            <text key={i} x={p.x} y={p.y + 4}
                              fontSize="10" fontWeight="700"
                              fill="#4338ca"
                              textAnchor={p.x > cx + 5 ? 'start' : p.x < cx - 5 ? 'end' : 'middle'}>
                              {st.s.short}
                            </text>
                          );
                        })}
                      </svg>
                    );
                  })()}
                </div>
              </div>
              {coachUsed.topFix && (
                <button onClick={() => startConcept(coachUsed.topFix.name,
                  `${browseExam ? browseExam + ' · ' : ''}${coachUsed.topFix.name} 보강`, browseExam || null)}
                  style={{ width: '100%', marginTop: 14, padding: '11px 14px',
                    background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 10, fontWeight: 800, cursor: 'pointer' }}>
                  🔥 약점 보강 · {coachUsed.topFix.name} → 시작
                </button>
              )}
            </section>
          )}

          {/* ②.7 학습 캘린더 — 56일 일별 학습량 (셀 1개 = 하루) */}
          {(() => {
            const activeDays = last56Days.filter((x) => x.count > 0).length;
            const totalCount = last56Days.reduce((a, x) => a + x.count, 0);
            const avg = activeDays > 0 ? Math.round(totalCount / activeDays) : 0;
            const maxCell = last56Days.reduce((a, x) => x.count > a.count ? x : a, { count: 0 });
            // 셀이 비어있을 때는 의미가 떨어지므로 데이터가 거의 없으면 안내만 표시
            if (totalCount === 0) return (
              <section style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: '16px',
                padding: '16px', marginBottom: '16px', boxShadow: 'var(--shadow-md)', textAlign: 'center' }}>
                <div style={{ fontWeight: 800, fontSize: '0.95rem', marginBottom: 8 }}>📅 학습 캘린더</div>
                <div style={{ fontSize: '0.82rem', color: '#9ca3af' }}>
                  학습을 시작하면 매일 활동량이 칸으로 쌓입니다
                </div>
              </section>
            );
            const weekLabels = ['7주전', '6주전', '5주전', '4주전', '3주전', '2주전', '지난주', '이번주'];
            const dayNames = ['일', '월', '화', '수', '목', '금', '토'];
            return (
              <section style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: '16px',
                padding: '16px', marginBottom: '16px', boxShadow: 'var(--shadow-md)' }}>
                <div style={{ marginBottom: 4 }}>
                  <div style={{ fontWeight: 800, fontSize: '0.95rem' }}>📅 학습 캘린더 — 최근 56일</div>
                  <div style={{ fontSize: '0.72rem', color: '#6b7280', marginTop: 2 }}>
                    칸 하나가 하루. 색이 진할수록 그날 많이 학습 (기출 풀이 + AI 메시지)
                  </div>
                </div>
                {/* 통계 */}
                <div style={{ display: 'flex', gap: 12, marginTop: 10, marginBottom: 10, fontSize: '0.78rem', color: '#374151', flexWrap: 'wrap' }}>
                  <span>🔥 <b style={{ color: '#ea580c' }}>{analytics.streak}일</b> 연속</span>
                  <span>📌 학습일 <b style={{ color: '#4338ca' }}>{activeDays}/56</b></span>
                  <span>📊 활동일 평균 <b>{avg}</b>회</span>
                  {maxCell.count > 0 && (
                    <span>⭐ 최고 <b>{maxCell.count}</b>회 ({maxCell.date.getMonth() + 1}/{maxCell.date.getDate()})</span>
                  )}
                </div>
                {/* 본체: 좌측 요일 라벨 + 8주 격자 */}
                <div style={{ display: 'flex', gap: 4 }}>
                  {/* 요일 라벨 */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 4, paddingTop: 18 }}>
                    {dayNames.map((d, i) => (
                      <div key={i} style={{
                        height: 16, fontSize: '0.62rem', color: '#9ca3af',
                        display: 'flex', alignItems: 'center', justifyContent: 'flex-end', minWidth: 16,
                      }}>
                        {i % 2 === 0 ? d : ''}
                      </div>
                    ))}
                  </div>
                  {/* 격자 */}
                  <div style={{ flex: 1 }}>
                    {/* 주 라벨 */}
                    <div style={{ display: 'flex', gap: 4, marginBottom: 4 }}>
                      {weekLabels.map((w, i) => (
                        <div key={i} style={{
                          flex: 1, fontSize: '0.6rem', textAlign: 'center',
                          color: i === 7 ? '#ea580c' : '#9ca3af',
                          fontWeight: i === 7 ? 700 : 500,
                        }}>
                          {i % 2 === 0 || i === 7 ? w : ''}
                        </div>
                      ))}
                    </div>
                    <div style={{ display: 'flex', gap: 4 }}>
                      {Array.from({ length: 8 }).map((_, wi) => (
                        <div key={wi} style={{ display: 'flex', flexDirection: 'column', gap: 4, flex: 1 }}>
                          {Array.from({ length: 7 }).map((_, di) => {
                            const idx = wi * 7 + di;
                            const cell = last56Days[idx];
                            if (!cell) return <div key={di} style={{ height: 16 }} />;
                            const intensity = cell.count > 0 ? Math.min(1, 0.2 + (cell.count / heatMax) * 0.8) : 0;
                            const bg = intensity === 0 ? '#f3f4f6'
                              : intensity < 0.4 ? '#c7d2fe'
                              : intensity < 0.7 ? '#818cf8'
                              : '#4f46e5';
                            const day = (cell.date.getMonth() + 1) + '월 ' + cell.date.getDate() + '일';
                            return (
                              <div key={di}
                                title={`${day} (${dayNames[cell.date.getDay()]}) · ${cell.count}회 학습`}
                                style={{
                                  height: 16, borderRadius: 3, background: bg,
                                  border: cell.isToday ? '1.5px solid #ea580c' : '1px solid transparent',
                                }} />
                            );
                          })}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                {/* 범례 */}
                <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 4, marginTop: 10, fontSize: '0.68rem', color: '#9ca3af' }}>
                  <span>적음</span>
                  {['#f3f4f6', '#c7d2fe', '#818cf8', '#4f46e5'].map((c) => (
                    <span key={c} style={{ width: 12, height: 12, borderRadius: 3, background: c, display: 'inline-block' }} />
                  ))}
                  <span>많음</span>
                </div>
              </section>
            );
          })()}


          {/* ④ 8과목 도넛 카드 그리드 — 1차 / 2차 섹션 분리 */}
          {[
            { label: '📖 1차 시험 (5과목)', matrix: matrixStage1 },
            { label: '✍️ 2차 시험 (3과목)', matrix: matrixStage2 },
          ].map(({ label, matrix }) => matrix.length === 0 ? null : (
            <section key={label} style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: '16px',
              padding: '16px', marginBottom: '16px', boxShadow: 'var(--shadow-md)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                <div style={{ fontWeight: 800, fontSize: '1rem' }}>📊 {label}</div>
                <div style={{ fontSize: '0.7rem', color: '#9ca3af' }}>약점 우선</div>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: 10 }}>
                {matrix.map(({ s, aiCov, aiMaster, aiTotal, quizAcc, quizCov, quizScored, quizTotal, score, isStage2, avgScorePct, answerCountSum }) => {
                  const scorePct = Math.round(score * 100);
                  const blueShade = scorePct >= 70 ? '#1d4ed8' : scorePct >= 40 ? '#4f46e5' : '#818cf8';
                  const tierLabel = scorePct >= 70 ? '안정' : scorePct >= 40 ? '진행' : '시작';
                  return (
                    <div key={s.id} style={{
                      background: 'linear-gradient(160deg, #f5f8ff 0%, #ffffff 100%)',
                      border: '1px solid #dbeafe', borderRadius: 12, padding: 12,
                      display: 'flex', flexDirection: 'column', gap: 6,
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <span style={{ fontSize: '1.1rem' }}>{s.icon}</span>
                        <span style={{ fontWeight: 800, color: '#1e3a8a', fontSize: '0.9rem' }}>{s.short}</span>
                        <span style={{ marginLeft: 'auto', fontSize: '0.62rem', fontWeight: 700, color: '#4338ca',
                          background: '#eef2ff', padding: '2px 6px', borderRadius: 999, border: '1px solid #c7d2fe' }}>
                          {tierLabel}
                        </span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'center', margin: '4px 0' }}>
                        <Donut size={86} value={score} color={blueShade} stroke={8}
                          centerText={`${scorePct}`} centerSub="통합" />
                      </div>
                      {/* 듀얼 미니 막대 — stage 2는 답안 평균 표시 */}
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                          <span style={{ fontSize: '0.65rem', color: '#6b7280', width: 14 }}>🎓</span>
                          <div style={{ flex: 1, height: 4, background: '#fff', borderRadius: 2, overflow: 'hidden', border: '1px solid #e0e7ff' }}>
                            <div style={{ width: `${Math.round(aiCov * 100)}%`, height: '100%', background: '#4f46e5' }} />
                          </div>
                          <span style={{ fontSize: '0.62rem', color: '#374151', minWidth: 32, textAlign: 'right' }}>
                            {Math.round(aiCov * 100)}%
                          </span>
                        </div>
                        {isStage2 ? (
                          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                            <span style={{ fontSize: '0.65rem', color: '#6b7280', width: 14 }}>📝</span>
                            <div style={{ flex: 1, height: 4, background: '#fff', borderRadius: 2, overflow: 'hidden', border: '1px solid #e0e7ff' }}>
                              <div style={{ width: `${Math.round(avgScorePct * 100)}%`, height: '100%', background: '#7c3aed' }} />
                            </div>
                            <span style={{ fontSize: '0.62rem', color: '#374151', minWidth: 32, textAlign: 'right' }}>
                              {Math.round(avgScorePct * 100)}%
                            </span>
                          </div>
                        ) : (
                          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                            <span style={{ fontSize: '0.65rem', color: '#6b7280', width: 14 }}>📚</span>
                            <div style={{ flex: 1, height: 4, background: '#fff', borderRadius: 2, overflow: 'hidden', border: '1px solid #e0e7ff' }}>
                              <div style={{ width: `${Math.round(quizCov * 100)}%`, height: '100%', background: '#60a5fa' }} />
                            </div>
                            <span style={{ fontSize: '0.62rem', color: '#374151', minWidth: 32, textAlign: 'right' }}>
                              {quizAcc != null ? `${Math.round(quizAcc * 100)}%` : '–'}
                            </span>
                          </div>
                        )}
                      </div>
                      <div style={{ fontSize: '0.62rem', color: '#6b7280', display: 'flex', justifyContent: 'space-between' }}>
                        <span>마스터 {aiMaster}/{aiTotal}</span>
                        <span>{isStage2 ? `답안 ${answerCountSum}` : `${quizScored}/${quizTotal}`}</span>
                      </div>
                      <div style={{ display: 'flex', gap: 4, marginTop: 2 }}>
                        <button
                          onClick={() => {
                            const sl = (leavesBySubject[s.id] || [])[0];
                            if (sl) jumpToAILearn(sl); else jumpToAILearn(null);
                          }}
                          style={{ flex: 1, padding: '5px', fontSize: '0.7rem', fontWeight: 700,
                            background: '#4f46e5', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
                          🎓
                        </button>
                        {!isStage2 && (
                          <button
                            onClick={() => {
                              setTaxScope({ key: PRIMARY_EXAM, label: PRIMARY_EXAM });
                              setTaxSubject(s.title);
                              setTaxSubSubject(null); setTaxChapter(null); setTaxSection(null);
                              setCurrentView('tax_sub_subjects');
                              window.scrollTo(0, 0);
                            }}
                            style={{ flex: 1, padding: '5px', fontSize: '0.7rem', fontWeight: 700,
                              background: '#fff', color: '#4338ca', border: '1px solid #c7d2fe', borderRadius: 6, cursor: 'pointer' }}>
                            📚
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>
          ))}



          {/* 오늘 학습 목표 */}
          {(() => {
            const done = analytics.todayCount;
            const pct = Math.min(100, Math.round((done / dailyGoal) * 100));
            const met = done >= dailyGoal;
            return (
              <section style={{ background: met ? '#ecfdf5' : '#fff', border: `1px solid ${met ? '#a7f3d0' : '#e5e7eb'}`,
                borderRadius: '16px', padding: '18px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <span style={{ fontWeight: 800 }}>🎯 오늘 목표 {met && <span style={{ color: '#16a34a' }}>달성!</span>}</span>
                  <span style={{ fontSize: '0.9rem', color: '#374151' }}><b>{done}</b> / {dailyGoal}문제</span>
                </div>
                <div style={{ height: '10px', background: '#f1f5f9', borderRadius: '999px', overflow: 'hidden', marginBottom: '12px' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: met ? '#16a34a' : 'var(--primary)', transition: 'width .3s' }} />
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <span style={{ fontSize: '0.85rem', color: '#374151' }}>
                    🔥 목표 연속 <b style={{ color: '#ea580c' }}>{analytics.goalStreak}일</b>
                  </span>
                  <span style={{ display: 'flex', gap: '5px' }}>
                    {analytics.weekMet.map((w, i) => (
                      <span key={i} title={w.label} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2px' }}>
                        <span style={{ width: 14, height: 14, borderRadius: '50%',
                          background: w.met ? '#16a34a' : '#e5e7eb',
                          outline: w.isToday ? '2px solid var(--primary)' : 'none', outlineOffset: '1px' }} />
                        <span style={{ fontSize: '0.55rem', color: '#9ca3af' }}>{w.label}</span>
                      </span>
                    ))}
                  </span>
                </div>
                <div style={{ display: 'flex', gap: '6px' }}>
                  {[10, 20, 30, 50].map(g => (
                    <button key={g} onClick={() => setDailyGoal(g)}
                      style={{ flex: 1, padding: '7px', borderRadius: '8px', fontSize: '0.78rem', fontWeight: 700, cursor: 'pointer',
                        border: dailyGoal === g ? '1px solid var(--primary)' : '1px solid #d1d5db',
                        background: dailyGoal === g ? 'var(--primary)' : '#fff', color: dailyGoal === g ? '#fff' : '#6b7280' }}>
                      {g}문제
                    </button>
                  ))}
                </div>
              </section>
            );
          })()}

          {/* 추세 — 일별 학습량 라인 + 누적 정답률 */}
          <section style={{ background: '#fff', borderRadius: '16px', padding: '16px', boxShadow: 'var(--shadow-md)', marginBottom: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <span style={{ fontWeight: 800, fontSize: '0.95rem' }}>📈 최근 {trendDays}일 · {analytics.trendSum}문제</span>
              <span style={{ display: 'flex', gap: '4px' }}>
                {[7, 30].map(d => (
                  <button key={d} onClick={() => setTrendDays(d)}
                    style={{ border: 'none', borderRadius: '6px', padding: '4px 10px', fontSize: '0.72rem', fontWeight: 700, cursor: 'pointer',
                      background: trendDays === d ? 'var(--primary)' : '#f1f5f9', color: trendDays === d ? '#fff' : '#6b7280' }}>{d}일</button>
                ))}
              </span>
            </div>
            {(() => {
              const W = 320, H = 80, PAD = 6;
              const data = analytics.trend;
              const n = data.length;
              const maxV = analytics.trendMax || 1;
              const xAt = (i) => PAD + (n > 1 ? (i * (W - 2 * PAD)) / (n - 1) : (W / 2));
              const yAt = (v) => H - PAD - ((H - 2 * PAD) * v) / maxV;
              const linePts = data.map((t, i) => `${xAt(i).toFixed(1)},${yAt(t.count).toFixed(1)}`).join(' ');
              const areaPts = `${PAD},${H - PAD} ${linePts} ${(W - PAD)},${H - PAD}`;
              return (
                <svg viewBox={`0 0 ${W} ${H + 16}`} style={{ width: '100%', height: 'auto', display: 'block' }}>
                  {/* y axis grid */}
                  {[0.25, 0.5, 0.75, 1].map((g) => (
                    <line key={g} x1={PAD} x2={W - PAD}
                      y1={H - PAD - (H - 2 * PAD) * g}
                      y2={H - PAD - (H - 2 * PAD) * g}
                      stroke="#f3f4f6" strokeWidth="1" strokeDasharray="2,3" />
                  ))}
                  <polygon points={areaPts} fill="#4f46e5" fillOpacity="0.12" />
                  <polyline points={linePts} fill="none" stroke="#4f46e5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  {data.map((t, i) => (
                    <circle key={i} cx={xAt(i)} cy={yAt(t.count)} r={t.isToday ? 3.5 : 1.8}
                      fill={t.isToday ? '#ea580c' : '#4f46e5'}
                      stroke={t.isToday ? '#fff' : 'none'} strokeWidth={t.isToday ? 1.5 : 0}>
                      <title>{t.label} · {t.count}문제{t.acc != null ? ` · ${t.acc}%` : ''}</title>
                    </circle>
                  ))}
                  {/* x labels — 7일이면 모두, 30일이면 5등분 */}
                  {data.map((t, i) => {
                    if (trendDays > 7 && i % Math.ceil(n / 6) !== 0 && !t.isToday) return null;
                    return (
                      <text key={i} x={xAt(i)} y={H + 12} fontSize="9"
                        textAnchor="middle"
                        fill={t.isToday ? '#ea580c' : '#9ca3af'}
                        fontWeight={t.isToday ? 700 : 500}>
                        {t.label || `${t.date ? '' : i + 1}`}
                      </text>
                    );
                  })}
                </svg>
              );
            })()}
          </section>

          {/* ⑦ 난이도별 정답률 — 미니 차트 */}
          <section style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: '16px',
            padding: '16px', marginBottom: '16px', boxShadow: 'var(--shadow-md)' }}>
            <div style={{ fontWeight: 800, fontSize: '0.95rem', marginBottom: 10 }}>📈 난이도별 정답률</div>
            <div style={{ display: 'flex', gap: '6px' }}>
              {analyticsUsed.diffAcc.map(({ d, acc }) => {
                const m = DIFFICULTY_META[d] || {};
                return (
                  <div key={d} style={{ flex: 1, textAlign: 'center' }}>
                    <div style={{ height: '40px', display: 'flex', alignItems: 'flex-end', justifyContent: 'center' }}>
                      <div style={{ width: '64%', borderRadius: '3px 3px 0 0', height: `${acc == null ? 3 : Math.max(4, acc * 0.38)}px`, background: acc == null ? '#e5e7eb' : (m.fg || 'var(--primary)') }} />
                    </div>
                    <div style={{ fontSize: '0.62rem', color: '#9ca3af', marginTop: '3px' }}>난{d}</div>
                    <div style={{ fontSize: '0.68rem', fontWeight: 700, color: acc == null ? '#9ca3af' : '#374151' }}>{acc == null ? '–' : `${acc}%`}</div>
                  </div>
                );
              })}
            </div>
          </section>

          {/* 북마크 요약 */}
          {bookmarkedList.length > 0 && (
            <section style={{ background: '#fffbeb', border: '1px solid #fde68a', borderRadius: '16px', padding: '18px', marginBottom: '8px' }}>
              <div style={{ fontWeight: 800, marginBottom: '10px', color: '#b45309' }}>★ 북마크 {bookmarkedList.length}</div>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {BM_REASONS.map(r => {
                  const ids = bookmarkedList.filter(q => bmReasonOf(bm[qid(q)]) === r).map(qid);
                  if (!ids.length) return null;
                  const m = BM_META[r];
                  return (
                    <button key={r} onClick={() => startReview(ids, `북마크 · ${m.label}`, 'status')}
                      style={{ border: `1px solid ${m.color}`, background: '#fff', color: m.color, borderRadius: '999px',
                        padding: '7px 13px', fontSize: '0.82rem', fontWeight: 700, cursor: 'pointer' }}>
                      {m.icon} {m.label} {ids.length}
                    </button>
                  );
                })}
              </div>
            </section>
          )}

          <button onClick={() => setCurrentView('profile')}
            style={{ width: '100%', textAlign: 'left', padding: '14px 16px', borderRadius: '12px', marginBottom: '8px',
              border: '1px solid #d1d5db', background: '#fff', color: '#374151', cursor: 'pointer',
              display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: 700 }}>👤 프로필 · 데이터 백업</span>
            <span style={{ fontSize: '0.8rem', color: '#9ca3af' }}>관리 →</span>
          </button>
        </main>
      </div>
    );
  }

  if (currentView === 'today') {
    const fmtDate = (ms) => {
      const d = new Date(ms), t = new Date(); t.setHours(0, 0, 0, 0);
      const diff = Math.round((new Date(ms).setHours(0, 0, 0, 0) - t.getTime()) / DAY);
      const label = diff <= 0 ? '오늘' : diff === 1 ? '내일' : `${diff}일 후`;
      return `${d.getMonth() + 1}/${d.getDate()} (${label})`;
    };
    return shell(
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => setCurrentView('reviewHome')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>복습 홈</span>
          </button>
        </header>
        <div style={{ padding: '24px 20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700 }}>📅 오늘 복습</h1>
          <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>
            오늘 복습 {srs.due.length}문제
            {srs.capped && <> · 전체 {srs.dueTotal}개 중 (나머지는 다음에)</>}
            · 맞히면 간격이 늘어 더 나중에 나와요
          </div>
          <div style={{ display: 'flex', gap: '6px', marginTop: '12px' }}>
            {Object.entries(SRS_MODES).map(([m, cfg]) => (
              <button key={m} onClick={() => setSrsMode(m)}
                style={{ flex: 1, padding: '8px', borderRadius: '8px', cursor: 'pointer', fontSize: '0.82rem', fontWeight: 700,
                  border: srsMode === m ? '1px solid var(--primary)' : '1px solid #d1d5db',
                  background: srsMode === m ? 'var(--primary)' : '#fff',
                  color: srsMode === m ? '#fff' : '#374151' }}>
                {cfg.label}
                <span style={{ display: 'block', fontWeight: 500, fontSize: '0.68rem', opacity: 0.8 }}>
                  하루 {cfg.cap === Infinity ? '무제한' : `${cfg.cap}개`}
                </span>
              </button>
            ))}
          </div>
        </div>
        <main className="main-content" style={{ marginTop: '20px' }}>
          {srs.due.length === 0 ? (
            <div className="empty-state">
              <span className="emoji">🎉</span>
              <div className="title">오늘 복습할 문제가 없어요</div>
              <div className="sub">
                {srs.nextDue != null
                  ? <>다음 복습 예정: <b>{fmtDate(srs.nextDue)}</b></>
                  : '문제를 풀다 틀리면 복습 일정이 생겨요'}
              </div>
            </div>
          ) : (
            <div className="study-grid">
              <div className="study-card"
                onClick={() => startReview(srs.due.map(qid), '오늘 복습 전체', 'today')}
                style={{ background: '#eff6ff', borderColor: '#bfdbfe', cursor: 'pointer' }}>
                <div className="card-badge" style={{ background: 'var(--primary)', color: '#fff', border: 'none' }}>전체</div>
                <h3 className="card-title" style={{ fontSize: '1.1rem' }}>오늘 복습 전체</h3>
                <div className="card-total">총 {srs.due.length} 문제</div>
                <div className="play-btn" style={{ background: 'var(--primary)', color: '#fff' }}>시작</div>
              </div>
              {srs.groups.map((g) => (
                <div key={g.subj} className="study-card"
                  onClick={() => startReview(g.ids, `${g.subj} 오늘 복습`, 'today')}
                  style={{ cursor: 'pointer' }}>
                  <div className="card-badge">과목</div>
                  <div className="card-subtitle">오늘 복습</div>
                  <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{g.subj}</h3>
                  <div className="card-total">{g.count} 문제</div>
                  <div className="play-btn">시작</div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    );
  }

  if (currentView === 'review') {
    // 현재 스코프(전체 또는 선택 과목)의 오답 집합
    const scopeWrong = reviewSubject
      ? wrongList.filter(q => (q.taxSubjectName || '기타') === reviewSubject)
      : wrongList;
    // 난이도 오답 분포 (1~5)
    const dist = [1, 2, 3, 4, 5].map(d => scopeWrong.filter(q => q.difficulty === d).length);
    const distMax = Math.max(1, ...dist);
    // 과목 선택 시 절(section) 단위 그룹
    const sectionGroups = (() => {
      if (!reviewSubject) return [];
      const by = {};
      for (const q of scopeWrong) {
        const k = q.taxSectionName || q.taxChapterName || q.taxSubSubjectName || '기타';
        (by[k] || (by[k] = [])).push(q);
      }
      return Object.entries(by).map(([sec, qs]) => ({ sec, ids: qs.map(qid), count: qs.length }))
        .sort((a, b) => b.count - a.count);
    })();
    return shell(
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => reviewSubject ? setReviewSubject(null) : setCurrentView('reviewHome')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>{reviewSubject ? '뒤로가기' : '복습 홈'}</span>
          </button>
        </header>
        <div style={{ padding: '24px 20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700 }}>
            {reviewSubject ? `${reviewSubject} 오답` : '오답 복습'}
          </h1>
          <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>
            {reviewSubject ? '절 단위로 약점을 좁혀 복습하세요' : '여러 번 틀린·어려운 문제부터 우선 출제됩니다'}
          </div>
          {scopeWrong.length > 0 && (
            <div style={{ display: 'flex', gap: '6px', alignItems: 'flex-end', marginTop: '14px', height: '44px' }}>
              {dist.map((c, i) => (
                <div key={i} style={{ flex: 1, textAlign: 'center' }}>
                  <div style={{ height: `${Math.round((c / distMax) * 32)}px`, background: (DIFFICULTY_META[i + 1] || {}).fg || '#9ca3af', borderRadius: '3px 3px 0 0', minHeight: c ? '3px' : '0' }} />
                  <div style={{ fontSize: '0.65rem', color: '#9ca3af', marginTop: '3px' }}>난{i + 1}·{c}</div>
                </div>
              ))}
            </div>
          )}
        </div>
        <main className="main-content" style={{ marginTop: '20px' }}>
          {scopeWrong.length === 0 ? (
            <div className="empty-state">
              <span className="emoji">🎉</span>
              <div className="title">{reviewSubject ? '이 과목 오답을 모두 해결했어요' : '복습할 오답이 없어요'}</div>
              <div className="sub">{reviewSubject ? '다른 과목도 확인해 보세요' : '잘하고 있어요! 계속 풀어볼까요?'}</div>
            </div>
          ) : (
            <div className="study-grid">
              <div className="study-card"
                onClick={() => startReview(scopeWrong.map(qid), reviewSubject ? `${reviewSubject} 오답` : '전체 오답 복습')}
                style={{ background: '#fef2f2', borderColor: '#fecaca', cursor: 'pointer' }}>
                <div className="card-badge" style={{ background: '#ef4444', color: '#fff', border: 'none' }}>{reviewSubject ? '과목 전체' : '전체'}</div>
                <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{reviewSubject ? `${reviewSubject} 전체 오답` : '전체 오답 복습'}</h3>
                <div className="card-total">총 {scopeWrong.length} 문제</div>
                <div className="play-btn" style={{ background: '#ef4444', color: '#fff' }}>복습</div>
              </div>
              {!reviewSubject && reviewGroups.map((g) => (
                <div key={g.subj} className="study-card" onClick={() => setReviewSubject(g.subj)} style={{ cursor: 'pointer' }}>
                  <div className="card-badge">과목</div>
                  <div className="card-subtitle">절 단위로 좁히기 →</div>
                  <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{g.subj}</h3>
                  <div className="card-total">오답 {g.count} 문제</div>
                  <div className="play-btn">선택</div>
                </div>
              ))}
              {reviewSubject && sectionGroups.map((g) => (
                <div key={g.sec} className="study-card" onClick={() => startReview(g.ids, `${g.sec} 오답`)} style={{ cursor: 'pointer' }}>
                  <div className="card-badge">절</div>
                  <div className="card-subtitle">{reviewSubject}</div>
                  <h3 className="card-title" style={{ fontSize: '1.05rem' }}>{g.sec}</h3>
                  <div className="card-total">오답 {g.count} 문제</div>
                  <div className="play-btn">복습</div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    );
  }

  // ===== 홈 탭 =====
  if (currentView === 'home') {
    return shell(
    <div className="app-container">
      <div className="banner">
        <div style={{ position: 'absolute', right: '16px',
          top: 'calc(env(safe-area-inset-top, 0px) + 14px)', zIndex: 10,
          display: 'flex', gap: '8px' }}>
          <button aria-label="검색" onClick={() => setShowCmdK(true)} title="검색 (⌘K)"
            style={{ width: 44, height: 44, borderRadius: '50%', border: '1px solid rgba(255,255,255,0.3)', cursor: 'pointer',
              background: 'rgba(255,255,255,0.28)', color: '#fff', fontSize: '1.2rem',
              display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            🔍
          </button>
          <button aria-label="프로필" onClick={() => setCurrentView('profile')}
            style={{ width: 44, height: 44, borderRadius: '50%', border: '1px solid rgba(255,255,255,0.3)', cursor: 'pointer',
              background: 'rgba(255,255,255,0.28)', color: '#fff', fontSize: '1.2rem',
              display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            👤
          </button>
          <button aria-label="설정" onClick={() => openSettings('home')}
            style={{ width: 44, height: 44, borderRadius: '50%', border: '1px solid rgba(255,255,255,0.3)', cursor: 'pointer',
              background: 'rgba(255,255,255,0.28)', color: '#fff', fontSize: '1.2rem',
              display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            ⚙️
          </button>
        </div>
        <div className="banner-content">
          <div className="banner-title">{PRIMARY_EXAM} 합격 트랙</div>
          <p style={{ marginTop: '6px', opacity: 0.85, fontSize: '0.9rem', fontWeight: 500 }}>
            {nickname ? `${nickname}님, 오늘도 한 걸음 더` : '오늘도 한 걸음 더'}
          </p>
        </div>
      </div>

      <main className="main-content">
        {/* 감정평가사 D-DAY 카드 — 1차/2차 두 단계 + 일일 권장량 자동 계산 */}
        {(() => {
          const d1 = daysUntil(examDates[`${PRIMARY_EXAM}_1차`] || examDates[PRIMARY_EXAM]);
          const d2 = daysUntil(examDates[`${PRIMARY_EXAM}_2차`]);
          const hasAny = d1 != null || d2 != null;
          const dColor = (d) => d == null ? '#9ca3af'
            : d < 0 ? '#9ca3af'
            : d <= 30 ? '#dc2626'
            : d <= 90 ? '#ea580c'
            : '#1d4ed8';
          // 가장 임박한 미래 시험을 기준으로 일일 권장량 계산
          // 미응답 ÷ 남은일 (최소 5, 최대 100문제/일)
          const focusD = [d1, d2].filter(x => x != null && x > 0).sort((a, b) => a - b)[0];
          const remain1stQs = classifiedList.filter(q =>
            q.exam === PRIMARY_EXAM && !progress[qid(q)]).length;
          const rec = focusD ? Math.max(5, Math.min(100, Math.ceil(remain1stQs / focusD))) : null;
          return (
            <section style={{ background: '#fff', borderRadius: 16,
              padding: '14px 16px', boxShadow: 'var(--shadow-md)', marginBottom: 14 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between',
                alignItems: 'center', marginBottom: hasAny ? 10 : 0 }}>
                <span style={{ fontWeight: 800, fontSize: '0.95rem', color: '#111827' }}>
                  📅 {PRIMARY_EXAM} 시험일
                </span>
                <button onClick={() => openSettings('home')}
                  style={{ fontSize: '0.72rem', color: '#6b7280',
                    background: 'none', border: 'none', cursor: 'pointer' }}>
                  {hasAny ? '수정 →' : '입력하기 →'}
                </button>
              </div>
              {hasAny ? (
                <>
                  <div style={{ display: 'flex', gap: 10 }}>
                    {[
                      { label: '1차', d: d1, date: examDates[`${PRIMARY_EXAM}_1차`] || examDates[PRIMARY_EXAM] },
                      { label: '2차', d: d2, date: examDates[`${PRIMARY_EXAM}_2차`] },
                    ].map(({ label, d, date }) => (
                      <div key={label} style={{ flex: 1, padding: '10px 12px',
                        borderRadius: 10, border: '1px solid #e5e7eb',
                        background: d != null && d <= 30 ? '#fef2f2' : '#f9fafb' }}>
                        <div style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 600 }}>
                          {label}
                        </div>
                        <div style={{ fontSize: '1.1rem', fontWeight: 800,
                          color: dColor(d), marginTop: 2 }}>
                          {d != null ? fmtDday(d) : '—'}
                        </div>
                        <div style={{ fontSize: '0.68rem', color: '#9ca3af', marginTop: 2 }}>
                          {date || '미입력'}
                        </div>
                      </div>
                    ))}
                  </div>
                  {rec != null && remain1stQs > 0 && (
                    <div style={{ marginTop: 10, padding: '8px 12px',
                      background: '#eff6ff', borderRadius: 8,
                      fontSize: '0.78rem', color: '#1e40af', textAlign: 'center' }}>
                      💡 합격까지 미학습 {remain1stQs}문제 · 하루 <b>{rec}문제</b> 추천
                      {dailyGoal !== rec && (
                        <button onClick={() => {
                          const nearest = [10, 20, 30, 50].reduce((p, c) =>
                            Math.abs(c - rec) < Math.abs(p - rec) ? c : p, 20);
                          setDailyGoal(nearest);
                        }}
                          style={{ marginLeft: 6, fontSize: '0.72rem', color: '#1d4ed8',
                            fontWeight: 800, background: 'none', border: 'none', cursor: 'pointer' }}>
                          목표로 설정
                        </button>
                      )}
                    </div>
                  )}
                </>
              ) : (
                <div style={{ fontSize: '0.78rem', color: '#9ca3af', textAlign: 'center',
                  padding: '8px 0' }}>
                  시험일을 등록하면 D-DAY와 일일 권장 학습량을 추천해드려요
                </div>
              )}
            </section>
          );
        })()}
        {/* 오늘 할 일 — 4탭 통합 액션 (우선순위: SRS 기출 → AI 복습 → 약점 → 추천) */}
        {(() => {
          const aiDueLocal = getAiDue();
          const modeWeak = modeAnalytics ? modeAnalytics.weak[0] : null;
          const w0 = modeWeak || analytics.weak[0];
          let act;
          if (srs.due.length > 0) {
            act = { tag: '🔁 기출 복습', title: `오늘 복습 ${srs.due.length}문제`,
              desc: '기억 곡선이 도래했어요 · 지금이 가장 잘 외워질 때',
              go: () => setCurrentView('today') };
          } else if (aiDueLocal.length > 0) {
            const firstLeaf = Object.values(leavesBySubject).flat().find((l) => l.id === aiDueLocal[0].code);
            const leafName = firstLeaf ? firstLeaf.path.slice(-1)[0] : '단원';
            act = { tag: '🎓 AI 복습', title: `AI 학습 복습 ${aiDueLocal.length}단원`,
              desc: `${leafName} 등 마스터 단원 SRS 도래`,
              go: () => firstLeaf ? jumpToAILearn(firstLeaf) : jumpToAILearn(null) };
          } else if (w0) {
            const prefix = browseExam ? `${browseExam} · ` : '';
            act = { tag: '🔥 약점 보강', title: `${prefix}${w0.name} 집중`,
              desc: `현재 정답률 ${w0.acc}% — 약한 곳부터 끌어올려요`,
              go: () => startConcept(w0.name, `${prefix}${w0.name} 집중 학습`, browseExam || null) };
          } else {
            const prefix = browseExam ? `${browseExam} ` : '오늘의 ';
            act = { tag: '✨ 추천', title: `${prefix}추천 ${dailyGoal}문제`,
              desc: '미학습 위주로 골라 담았어요 · 한 번에 시작',
              go: () => startRecommended(browseExam || null) };
          }
          return (
            <button onClick={act.go} className="todo-hero">
              <span className="todo-tag">{act.tag}</span>
              <span className="todo-title">{act.title}</span>
              <span className="todo-desc">{act.desc}</span>
              <span className="todo-cta">바로 시작하기 →</span>
            </button>
          );
        })()}

        {/* ⚡ 4탭 빠른 진입 — AI학습·문제풀이·복습·현황 통합 허브 */}
        {(() => {
          const aiMastery = getAiMastery();
          const aiDueArr = getAiDue();
          const aiCur = (() => {
            try { return JSON.parse(localStorage.getItem('ailearn-current') || 'null'); } catch { return null; }
          })();
          const allLeavesFlat = Object.values(leavesBySubject).flat();
          const aiCurLeaf = aiCur ? allLeavesFlat.find((l) => l.id === aiCur.leaf_id) : null;
          const aiMastered = Object.values(aiMastery).filter((m) => m?.status === 'mastered').length;
          const overallPct = (() => {
            const total = allLeavesFlat.length || 1;
            const cov = allLeavesFlat.reduce((a, l) => a + (aiMastery[l.id]?.coverage || 0), 0) / total;
            const quizPct = overall.total ? (overall.answered / overall.total) : 0;
            return Math.round((cov * 0.5 + quizPct * 0.5) * 100);
          })();
          return (
            <section style={{ marginBottom: 14 }}>
              <div style={{ fontSize: '0.9rem', fontWeight: 800, color: '#111827', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                ⚡ 빠른 진입
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                {/* 🤖 AI 학습 */}
                <button
                  onClick={() => setCurrentView('civil')}
                  style={{
                    padding: 14, textAlign: 'left', cursor: 'pointer',
                    background: 'linear-gradient(160deg, #eef2ff 0%, #ffffff 100%)',
                    border: '1px solid #c7d2fe', borderRadius: 12,
                    display: 'flex', flexDirection: 'column', gap: 4,
                  }}>
                  <div style={{ fontSize: '1.3rem' }}>🤖</div>
                  <div style={{ fontWeight: 800, color: '#1e3a8a', fontSize: '1rem' }}>AI 학습</div>
                  <div style={{ fontSize: '0.78rem', color: '#1f2937', fontWeight: 600 }}>
                    {aiCurLeaf ? `이어서: ${aiCurLeaf.path.slice(-1)[0]}` : '단원 선택 후 대화 시작'}
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#475569', marginTop: 2 }}>
                    마스터 {aiMastered}{aiDueArr.length > 0 ? ` · 🔁 ${aiDueArr.length}` : ''}
                  </div>
                </button>
                {/* 📚 문제풀이 */}
                <button
                  onClick={() => setCurrentView('dashboard')}
                  style={{
                    padding: 14, textAlign: 'left', cursor: 'pointer',
                    background: 'linear-gradient(160deg, #ecfdf5 0%, #ffffff 100%)',
                    border: '1px solid #a7f3d0', borderRadius: 12,
                    display: 'flex', flexDirection: 'column', gap: 4,
                  }}>
                  <div style={{ fontSize: '1.3rem' }}>📚</div>
                  <div style={{ fontWeight: 800, color: '#065f46', fontSize: '1rem' }}>문제풀이</div>
                  <div style={{ fontSize: '0.78rem', color: '#1f2937', fontWeight: 600 }}>
                    {overall.answered > 0 ? `${overall.answered}/${overall.total} 풀이` : '8과목 기출 풀이'}
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#475569', marginTop: 2 }}>
                    {coach?.skillAcc != null ? `정답률 ${coach.skillAcc}%` : '학습 시작'}
                  </div>
                </button>
                {/* 🔁 복습 */}
                <button
                  onClick={() => { setReviewSubject(null); setCurrentView('reviewHome'); }}
                  style={{
                    padding: 14, textAlign: 'left', cursor: 'pointer',
                    background: srs.due.length > 0 || aiDueArr.length > 0
                      ? 'linear-gradient(160deg, #fef3c7 0%, #ffffff 100%)'
                      : 'linear-gradient(160deg, #f9fafb 0%, #ffffff 100%)',
                    border: srs.due.length > 0 || aiDueArr.length > 0 ? '1px solid #fcd34d' : '1px solid #e5e7eb',
                    borderRadius: 12,
                    display: 'flex', flexDirection: 'column', gap: 4,
                  }}>
                  <div style={{ fontSize: '1.3rem' }}>🔁</div>
                  <div style={{ fontWeight: 800, color: srs.due.length > 0 || aiDueArr.length > 0 ? '#92400e' : '#374151', fontSize: '1rem' }}>
                    복습
                  </div>
                  <div style={{ fontSize: '0.78rem', color: '#1f2937', fontWeight: 600 }}>
                    {srs.due.length > 0 || aiDueArr.length > 0
                      ? `기출 ${srs.due.length} · AI ${aiDueArr.length}단원`
                      : '복습 만기 없음'}
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#475569', marginTop: 2 }}>
                    🔥 {analytics.streak}일 연속
                  </div>
                </button>
                {/* 📊 현황 */}
                <button
                  onClick={() => setCurrentView('status')}
                  style={{
                    padding: 14, textAlign: 'left', cursor: 'pointer',
                    background: 'linear-gradient(160deg, #fce7f3 0%, #ffffff 100%)',
                    border: '1px solid #fbcfe8', borderRadius: 12,
                    display: 'flex', flexDirection: 'column', gap: 4,
                  }}>
                  <div style={{ fontSize: '1.3rem' }}>📊</div>
                  <div style={{ fontWeight: 800, color: '#9d174d', fontSize: '1rem' }}>현황</div>
                  <div style={{ fontSize: '0.78rem', color: '#1f2937', fontWeight: 600 }}>
                    종합 학습률 {overallPct}%
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#475569', marginTop: 2 }}>
                    {coach?.readiness != null ? `합격 준비도 ${coach.readiness}%` : '레이더·잔디·통계'}
                  </div>
                </button>
              </div>
            </section>
          );
        })()}

        {/* 감정평가사 1차 5과목 합격 준비도 — 단일 시험 multi-subject gauge */}
        {(() => {
          // 감정평가사 시험만 필터해서 과목별 readiness 계산
          const subjStats = {};
          for (const q of classifiedList) {
            if (q.exam !== PRIMARY_EXAM) continue;
            const sName = q.taxSubjectName || '기타';
            const s = subjStats[sName] || (subjStats[sName] = { total: 0, scored: 0, correct: 0 });
            s.total++;
            const p = progress[qid(q)];
            if (!p) continue;
            if (p.correct === true || p.correct === false) {
              s.scored++; if (p.correct === true) s.correct++;
            }
          }
          // 1차 표준 5과목 + 데이터에 실제로 있는 과목만 표시
          const subjects = APPRAISER_1ST_SUBJECTS.filter(name => (subjStats[name]?.total || 0) > 0);
          if (subjects.length === 0) return null;
          return (
            <section style={{ background: '#fff', borderRadius: 16, padding: 16,
              boxShadow: 'var(--shadow-md)', marginBottom: 14 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between',
                alignItems: 'baseline', marginBottom: 12 }}>
                <span style={{ fontWeight: 800, fontSize: '0.95rem', color: '#111827' }}>
                  🎯 1차 5과목 진척 <b style={{ color: 'var(--primary)', fontSize: '0.78rem' }}>합격선 {COACH_TARGET}%</b>
                </span>
                <button onClick={() => setCurrentView('status')}
                  style={{ fontSize: '0.72rem', color: '#1d4ed8',
                    background: 'none', border: 'none', cursor: 'pointer', fontWeight: 700 }}>
                  현황 상세 →
                </button>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
                {subjects.map(name => {
                  const v = subjStats[name];
                  const has = v && v.scored >= 5;
                  const acc = has ? Math.round((v.correct / v.scored) * 100) : null;
                  const cov = v.total ? Math.round((v.scored / v.total) * 100) : 0;
                  const pct = has ? Math.min(100, Math.round((acc / COACH_TARGET) * 100)) : 0;
                  const color = !has ? '#d1d5db'
                    : acc >= COACH_TARGET ? '#16a34a'
                    : acc >= 55 ? '#2563eb'
                    : acc >= 40 ? '#ea580c'
                    : '#dc2626';
                  const verdict = !has ? `학습 ${cov}% · 시작 →`
                    : acc >= COACH_TARGET ? '안정권'
                    : acc >= 55 ? '근접'
                    : acc >= 40 ? '보강 필요'
                    : '집중 학습';
                  return (
                    <button key={name}
                      onClick={() => startConcept(name, `${name} 집중`, PRIMARY_EXAM)}
                      style={{ display: 'flex', alignItems: 'center', gap: 10,
                        padding: '8px 10px', borderRadius: 10,
                        border: '1px solid transparent', background: 'transparent',
                        cursor: 'pointer', textAlign: 'left' }}>
                      <div style={{ minWidth: 110 }}>
                        <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#374151' }}>
                          {name}
                        </div>
                        <div style={{ fontSize: '0.68rem', color: '#9ca3af', marginTop: 1 }}>
                          {v.scored}/{v.total}문제
                        </div>
                      </div>
                      <div style={{ flex: 1, position: 'relative' }}>
                        <div style={{ height: 8, background: '#f3f4f6',
                          borderRadius: 4, overflow: 'hidden' }}>
                          <div style={{ width: `${pct}%`, height: '100%',
                            background: color, transition: 'width 0.3s' }} />
                        </div>
                        <div style={{ fontSize: '0.7rem', color: '#9ca3af', marginTop: 3 }}>
                          {verdict}
                        </div>
                      </div>
                      <div style={{ minWidth: 44, textAlign: 'right' }}>
                        <div style={{ fontWeight: 800, fontSize: '1.05rem', color }}>
                          {has ? `${acc}` : '—'}
                          {has && <span style={{ fontSize: '0.7rem', fontWeight: 600 }}>%</span>}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </section>
          );
        })()}

        {/* 다음 목표(마일스톤) — 단일 진행 지표 */}
        {(() => {
          const ms = [50, 100, 300, 500, 1000, 2000, 3000, 5000];
          const next = ms.find(m => overall.answered < m);
          if (!next) return null;
          const prev = ms[ms.indexOf(next) - 1] || 0;
          const p = Math.round(((overall.answered - prev) / (next - prev)) * 100);
          return (
            <div className="milestone">
              <div className="milestone-row">
                <span>🏁 다음 목표 <b>{next}문제</b></span>
                <span style={{ color: 'var(--text-sub)' }}>{next - overall.answered}문제 남음</span>
              </div>
              <div className="progress-bar-container" style={{ marginTop: 8, height: 6 }}>
                <div className="progress-bar-fill" style={{ width: `${p}%` }} />
              </div>
            </div>
          );
        })()}

        {/* 오늘의 목표 */}
        {(() => {
          const goal = dailyGoal;
          const done = analytics.todayCount;
          const gpct = Math.min(100, Math.round((done / (goal || 1)) * 100));
          const reached = done >= goal;
          return (
            <section style={{ background: '#fff', borderRadius: '16px', padding: '18px',
              boxShadow: 'var(--shadow-md)', marginBottom: '14px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                <div style={{ fontWeight: 800, fontSize: '1.05rem', color: '#111827' }}>
                  {reached ? '🎉 오늘 목표 달성!' : '🎯 오늘의 목표'}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#6b7280', fontWeight: 600 }}>
                  <span style={{ color: reached ? '#16a34a' : '#1d4ed8', fontWeight: 800 }}>{done}</span> / {goal}문제
                </div>
              </div>
              <div className="progress-bar-container" style={{ marginTop: '12px' }}>
                <div className="progress-bar-fill" style={{ width: `${gpct}%`,
                  background: reached ? '#16a34a' : undefined }}></div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '14px' }}>
                <div style={{ display: 'flex', gap: '6px' }}>
                  {analytics.weekMet.map((w, i) => (
                    <div key={i} title={w.label} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                      <div style={{ width: 22, height: 22, borderRadius: '50%',
                        background: w.met ? '#16a34a' : '#e5e7eb',
                        color: w.met ? '#fff' : '#9ca3af', fontSize: '0.7rem',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        outline: w.isToday ? '2px solid #1d4ed8' : 'none', outlineOffset: '1px' }}>
                        {w.met ? '✓' : ''}
                      </div>
                      <span style={{ fontSize: '0.68rem', color: '#9ca3af' }}>{w.label}</span>
                    </div>
                  ))}
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#ea580c' }}>
                    🔥 {analytics.streak}일
                  </div>
                  <div style={{ fontSize: '0.7rem', color: '#9ca3af' }}>연속 학습</div>
                </div>
              </div>
            </section>
          );
        })()}

        {/* 모의고사 + 2차 논술 진입 — 감정평가사 1차/2차 시험 트랙 */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
          <button onClick={() => setCurrentView('mock')}
            style={{ flex: 1, display: 'flex', flexDirection: 'column',
              padding: '14px', borderRadius: 12,
              border: '1px solid #fde68a', background: '#fffbeb',
              color: '#92400e', cursor: 'pointer', textAlign: 'left' }}>
            <span style={{ fontWeight: 800, fontSize: '0.9rem' }}>🎯 1차 모의고사</span>
            <span style={{ fontSize: '0.74rem', color: '#a16207', marginTop: 2,
              lineHeight: 1.4 }}>
              5과목 · 시간제한 · 자동채점
            </span>
          </button>
          <button onClick={() => setCurrentView('essay_subjects')}
            style={{ flex: 1, display: 'flex', flexDirection: 'column',
              padding: '14px', borderRadius: 12,
              border: '1px solid #c4b5fd', background: '#f5f3ff',
              color: '#5b21b6', cursor: 'pointer', textAlign: 'left' }}>
            <span style={{ fontWeight: 800, fontSize: '0.9rem' }}>📝 2차 논술</span>
            <span style={{ fontSize: '0.74rem', color: '#6d28d9', marginTop: 2,
              lineHeight: 1.4 }}>
              실무·이론·법규 · 모범답안
            </span>
          </button>
        </div>

        {/* 약점 집중 — 모드 적용. 보강 권유는 주황 톤(긴급 X)으로 — 빨강은 D-30 등 진짜 임박용 */}
        {(modeAnalytics ? modeAnalytics.weak : analytics.weak).length > 0 && (
          <section style={{ marginBottom: '14px' }}>
            <div style={{ fontWeight: 800, fontSize: '0.95rem', color: '#374151', margin: '0 2px 10px' }}>
              📉 약점 집중{browseExam && ` · ${browseExam}`}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {(modeAnalytics ? modeAnalytics.weak : analytics.weak).map((w) => {
                const critical = w.acc < 50;   // 50% 미만만 빨강(진짜 위험), 그 외 주황
                const fg = critical ? '#dc2626' : '#c2410c';
                const bg = critical ? '#fef2f2' : '#fff7ed';
                const bd = critical ? '#fecaca' : '#fed7aa';
                return (
                  <button key={w.name} onClick={() => startConcept(w.name,
                    `${browseExam ? browseExam + ' · ' : ''}${w.name} 집중 학습`, browseExam || null)}
                    style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '10px',
                      padding: '13px 15px', borderRadius: '12px', cursor: 'pointer',
                      border: `1px solid ${bd}`, background: bg, textAlign: 'left' }}>
                    <span style={{ fontWeight: 700, fontSize: '0.9rem', color: '#374151' }}>{w.name}</span>
                    <span style={{ fontSize: '0.82rem', color: fg, fontWeight: 700, flexShrink: 0 }}>
                      정답률 {w.acc}% · 보강 →
                    </span>
                  </button>
                );
              })}
            </div>
          </section>
        )}

        {/* 학습 진행 요약 */}
        <section className="overview-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <h2 className="overview-title">나의 학습 진행</h2>
              <p className="overview-subtitle">전체 {totalQuestions}개 문항 중 현재 진행 현황</p>
            </div>
            {overall.answered > 0 && (
              <button
                onClick={() => { if (window.confirm('학습 진행률을 모두 초기화할까요?')) resetProgress(); }}
                style={{ background: 'var(--primary-light)', padding: '8px 16px', borderRadius: '12px', color: 'var(--primary)', fontWeight: '700', fontSize: '0.9rem', border: 'none', cursor: 'pointer' }}
              >
                초기화
              </button>
            )}
          </div>

          {(() => {
            const pct = totalQuestions ? Math.round((overall.answered / totalQuestions) * 100) : 0;
            const acc = overall.accuracy;
            return (
              <>
                <div className="progress-bar-container">
                  <div className="progress-bar-fill" style={{ width: `${pct}%` }}></div>
                </div>
                <div className="progress-stats">
                  <div>
                    <span className="stat-dot"></span>
                    학습한 문제 <span className="stat-bold">{overall.answered}/{totalQuestions}</span>
                    {acc !== null && <> · 정답률 <span className="stat-bold" style={{ color: '#16a34a' }}>{acc}%</span></>}
                  </div>
                  <div>{pct}%</div>
                </div>
              </>
            );
          })()}

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '8px', marginTop: '16px' }}>
            {[
              ['미응답', coverage.unseen, '#6b7280', '#f3f4f6'],
              ['학습', coverage.learned, '#1d4ed8', '#eff6ff'],
              // 복습필요는 통계라 차분한 주황 (위험 X)
              ['복습필요', coverage.review, '#c2410c', '#fff7ed'],
              ['마스터', coverage.mastered, '#16a34a', '#f0fdf4'],
            ].map(([lbl, n, c, bg]) => (
              <div key={lbl} style={{ background: bg, borderRadius: '10px', padding: '10px 6px', textAlign: 'center' }}>
                <div style={{ fontSize: '1.05rem', fontWeight: 800, color: c }}>{n}</div>
                <div style={{ fontSize: '0.7rem', color: '#6b7280', marginTop: '2px' }}>{lbl}</div>
              </div>
            ))}
          </div>

          {overall.answered > 0 && (
            <button
              onClick={() => setCurrentView('status')}
              style={{ width: '100%', textAlign: 'center', padding: '12px', marginTop: '14px', borderRadius: '12px',
                border: '1px solid #bfdbfe', background: '#eff6ff', color: '#1d4ed8', cursor: 'pointer',
                fontWeight: 700, fontSize: '0.9rem' }}
            >
              📊 학습 현황 자세히 보기 →
            </button>
          )}
        </section>

        {/* 시험별 진척 / 복습 알림 카드는 status 탭·Settings로 이관 — 홈 간소화 */}

      </main>
    </div>
    );
  }

  // ===== 복습 탭: 오늘 복습 / 오답 복습 진입 =====
  if (currentView === 'reviewHome') {
    return shell(
    <div className="app-container">
      <div className="screen-head">
        <h1 className="screen-title">🔁 복습</h1>
        <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>기억 곡선 복습과 누적 오답을 한곳에서</p>
      </div>
      <main className="main-content" style={{ marginTop: '16px' }}>
        <div
          onClick={() => srs.due.length && setCurrentView('today')}
          style={{ padding: '18px', marginBottom: '12px', borderRadius: '12px',
            border: `1px solid ${srs.due.length ? '#bfdbfe' : '#e5e7eb'}`,
            background: srs.due.length ? '#eff6ff' : '#fff',
            cursor: srs.due.length ? 'pointer' : 'default' }}
        >
          <div style={{ fontWeight: 700, fontSize: '1.05rem', color: srs.due.length ? '#1d4ed8' : '#6b7280' }}>
            📅 오늘 복습 {srs.due.length > 0 ? `${srs.due.length}문제` : '없음'}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: '4px' }}>
            {srs.due.length > 0
              ? '기억 곡선에 따라 오늘 풀 차례예요 →'
              : (srs.nextDue != null
                  ? `다음 복습 예정: ${new Date(srs.nextDue).getMonth() + 1}/${new Date(srs.nextDue).getDate()}`
                  : '틀린 문제가 쌓이면 복습 일정이 생겨요')}
          </div>
        </div>
        {/* AI 학습 SRS due 단원 */}
        {(() => {
          const aiDueArr = getAiDue();
          const aiMastery = getAiMastery();
          if (aiDueArr.length === 0) return null;
          // leaf id → leaf 찾기 (leavesBySubject 캐시)
          const flat = Object.values(leavesBySubject).flat();
          const dueLeaves = aiDueArr.map((d) => ({
            leaf: flat.find((l) => l.id === d.code),
            days_overdue: d.days_overdue,
            m: aiMastery[d.code],
          })).filter((x) => x.leaf);
          return (
            <div style={{ padding: '14px', marginBottom: '12px', borderRadius: '12px',
              border: '1px solid #c7d2fe', background: '#eef2ff' }}>
              <div style={{ fontWeight: 700, fontSize: '1.05rem', color: '#4338ca', marginBottom: 4 }}>
                🎓 AI 학습 복습 만기 {dueLeaves.length}단원
              </div>
              <div style={{ fontSize: '0.78rem', color: '#6b7280', marginBottom: 8 }}>
                SRS 간격에 따라 마스터한 단원을 다시 보세요
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                {dueLeaves.slice(0, 5).map((x) => (
                  <button
                    key={x.leaf.id}
                    onClick={() => jumpToAILearn(x.leaf)}
                    style={{
                      textAlign: 'left', padding: '8px 10px', background: '#fff',
                      border: '1px solid #ddd6fe', borderRadius: 8, cursor: 'pointer',
                      fontSize: '0.82rem',
                    }}
                  >
                    <div style={{ fontWeight: 700, color: '#1e1b4b' }}>{x.leaf.path.slice(-1)[0]}</div>
                    <div style={{ fontSize: '0.72rem', color: '#6b7280' }}>
                      {x.leaf.path.slice(0, -1).join(' › ')}
                      {x.days_overdue > 0 && <span style={{ color: '#9a3412', marginLeft: 6 }}>· {x.days_overdue}일 경과</span>}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          );
        })()}
        <div
          onClick={() => wrongList.length && (setReviewSubject(null), setCurrentView('review'))}
          style={{ padding: '18px', borderRadius: '12px',
            border: `1px solid ${wrongList.length ? '#fecaca' : '#e5e7eb'}`,
            background: wrongList.length ? '#fef2f2' : '#fff',
            cursor: wrongList.length ? 'pointer' : 'default' }}
        >
          <div style={{ fontWeight: 700, fontSize: '1.05rem', color: wrongList.length ? '#b91c1c' : '#9ca3af' }}>
            🔁 오답 복습 {wrongList.length > 0 ? `${wrongList.length}문제` : '없음'}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: '4px' }}>
            {wrongList.length > 0 ? '틀린 문제를 과목·절별로 다시 풀기 →' : '아직 틀린 문제가 없어요'}
          </div>
        </div>
        <div style={{ padding: '18px', marginTop: '12px', borderRadius: '12px',
          border: `1px solid ${bookmarkedList.length ? '#fde68a' : '#e5e7eb'}`,
          background: bookmarkedList.length ? '#fffbeb' : '#fff' }}>
          <div
            onClick={() => bookmarkedList.length && startReview(bookmarkedList.map(qid), '북마크 전체', 'reviewHome')}
            style={{ cursor: bookmarkedList.length ? 'pointer' : 'default' }}
          >
            <div style={{ fontWeight: 700, fontSize: '1.05rem', color: bookmarkedList.length ? '#b45309' : '#9ca3af' }}>
              ★ 북마크 {bookmarkedList.length > 0 ? `${bookmarkedList.length}문제` : '없음'}
            </div>
            <div style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: '4px' }}>
              {bookmarkedList.length > 0 ? '전체 모아 학습 →' : '문제 풀 때 ☆를 눌러 북마크(중요·헷갈림·실수)'}
            </div>
          </div>
          {bookmarkedList.length > 0 && (
            <div style={{ display: 'flex', gap: '8px', marginTop: '12px', flexWrap: 'wrap' }}>
              {BM_REASONS.map(r => {
                const ids = bookmarkedList.filter(q => bmReasonOf(bm[qid(q)]) === r).map(qid);
                if (ids.length === 0) return null;
                const m = BM_META[r];
                return (
                  <button key={r} onClick={() => startReview(ids, `북마크 · ${m.label}`, 'reviewHome')}
                    style={{ border: `1px solid ${m.color}`, background: '#fff', color: m.color,
                      borderRadius: '999px', padding: '7px 13px', fontSize: '0.82rem', fontWeight: 700, cursor: 'pointer' }}>
                    {m.icon} {m.label} {ids.length}
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </main>
    </div>
    );
  }

  // ===== 둘러보기 탭: 시험/과목/단원/연도 =====
  // browseExam이 set이면 시험별 viewMode는 1개 시험뿐이라 무의미 → 숨김
  const viewModeTabs = browseExam
    ? [['subject','과목별'],['chapter','단원별'],['year','연도별']]
    : [['exam','시험별'],['subject','과목별'],['chapter','단원별'],['year','연도별']];
  return shell(
    <div className="app-container">
      <div className="screen-head">
        <h1 className="screen-title">📚 문제풀이</h1>
      </div>
      <main className="main-content" style={{ marginTop: '16px' }}>
        {/* 시험 모드 (감정평가사 ↔ 전체 DB 토글) */}
        <div style={{ marginBottom: '16px' }}>{renderModePicker()}</div>

        {/* 통합 검색 */}
        <button
          onClick={() => setCurrentView('search')}
          style={{ width: '100%', textAlign: 'left', padding: '14px 16px', marginBottom: '20px',
            border: '1px solid #c7d2fe', borderRadius: '12px',
            background: 'linear-gradient(160deg, #eff6ff 0%, #ffffff 100%)',
            color: '#1f2937', fontSize: '0.95rem', cursor: 'pointer', fontWeight: 600 }}
        >
          🔍 통합 검색·필터 (시험·과목·연도·난이도·키워드)
        </button>

        {/* 1차/2차 과목 카드 그리드 — AI 학습 홈과 통일된 디자인 */}
        {[
          { stage: 1, label: '1차 시험 — 객관식 5지선다', subjects: AI_SUBJECTS.filter((s) => s.stage === 1) },
          { stage: 2, label: '2차 시험 — 서술형·답안 작성', subjects: AI_SUBJECTS.filter((s) => s.stage === 2) },
        ].map(({ stage, label, subjects }) => (
          <div key={stage} style={{ marginBottom: 18 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
              <div style={{ fontSize: '1rem', color: '#111827', fontWeight: 800 }}>
                {stage === 1 ? '📖' : '✍️'} {label}
              </div>
              <span style={{ fontSize: '0.82rem', color: '#1f2937', fontWeight: 600 }}>{subjects.length}과목</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: 10 }}>
              {subjects.map((s) => {
                const subjStat = analytics.subjects.find((x) => x.name === s.title);
                const totalN = subjStat?.total || 0;
                const answeredN = subjStat?.scored || 0;
                const correctN = subjStat?.correct || 0;
                const pct = totalN > 0 ? Math.round((answeredN / totalN) * 100) : 0;
                const acc = answeredN > 0 ? Math.round((correctN / answeredN) * 100) : 0;
                const isStage2 = s.stage === 2;
                const hasQuiz = totalN > 0;
                return (
                  <button
                    key={s.id}
                    onClick={() => {
                      if (!hasQuiz) return;
                      setTaxScope({ key: PRIMARY_EXAM, label: PRIMARY_EXAM });
                      setTaxSubject(s.title);
                      setTaxSubSubject(null);
                      setTaxChapter(null);
                      setTaxSection(null);
                      const tax = taxonomyData?.[s.title];
                      if (tax?.has_subjects) setCurrentView('tax_sub_subjects');
                      else setCurrentView('tax_chapters');
                      window.scrollTo(0, 0);
                    }}
                    disabled={!hasQuiz}
                    style={{
                      padding: 16, textAlign: 'left',
                      background: hasQuiz
                        ? 'linear-gradient(160deg, #eff6ff 0%, #ffffff 100%)'
                        : 'linear-gradient(160deg, #f9fafb 0%, #ffffff 100%)',
                      border: hasQuiz ? '1px solid #c7d2fe' : '1px solid #e5e7eb',
                      borderRadius: 12, cursor: hasQuiz ? 'pointer' : 'not-allowed',
                      display: 'flex', flexDirection: 'column', gap: 6, position: 'relative',
                      opacity: hasQuiz ? 1 : 0.6,
                    }}
                  >
                    {isStage2 && (
                      <span style={{ position: 'absolute', top: 10, right: 10, fontSize: '0.7rem', fontWeight: 800,
                        background: '#4f46e5', color: '#fff', padding: '3px 8px', borderRadius: 999 }}>2차</span>
                    )}
                    <div style={{ fontSize: '1.8rem', lineHeight: 1 }}>{s.icon}</div>
                    <div style={{ fontWeight: 800, color: '#1e3a8a', fontSize: '1.1rem' }}>{s.short}</div>
                    <div style={{ fontSize: '0.82rem', color: '#1f2937', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {s.title}
                    </div>
                    <div style={{ marginTop: 8, height: 5, background: '#dbeafe', borderRadius: 3, overflow: 'hidden' }}>
                      <div style={{ width: `${Math.max(2, pct)}%`, height: '100%', background: '#4f46e5' }} />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.88rem', color: '#111827', marginTop: 4 }}>
                      <span style={{ fontWeight: 800 }}>{pct}%</span>
                      <span style={{ color: '#1f2937', fontWeight: 600 }}>
                        {hasQuiz ? `${answeredN}/${totalN}` : '기출 없음'}
                      </span>
                    </div>
                    {hasQuiz && acc > 0 && (
                      <div style={{ fontSize: '0.76rem', color: '#374151', marginTop: -2 }}>
                        정답률 {acc}%
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}

        {/* 🗂️ 다른 방식으로 둘러보기 — 본 UI 통합 */}
        <div style={{ marginTop: 4 }}>
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            marginBottom: 10, gap: 8, flexWrap: 'wrap',
          }}>
            <div style={{ fontSize: '1rem', color: '#111827', fontWeight: 800, display: 'flex', alignItems: 'center', gap: 6 }}>
              🗂️ 다른 방식으로 둘러보기
            </div>
            <div style={{ display: 'flex', gap: 4, background: '#eef2ff', padding: 3, borderRadius: 10, border: '1px solid #c7d2fe' }}>
              {viewModeTabs.map(([mode, label]) => (
                <button
                  key={mode}
                  onClick={() => switchTab(mode)}
                  style={{
                    padding: '6px 12px', borderRadius: 7, border: 'none',
                    background: viewMode === mode ? '#4f46e5' : 'transparent',
                    color: viewMode === mode ? '#fff' : '#4338ca',
                    fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer',
                    transition: 'all 0.15s',
                  }}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: 10 }}>
            {activeGroups.map((group, idx) => {
              const s = progressStats(cardQuestions(group), progress);
              const pct = s.total ? Math.round((s.answered / s.total) * 100) : 0;
              const dm = s.level ? (DIFFICULTY_META[s.level] || null) : null;
              const modeIcon = viewMode === 'exam' ? '🎓'
                : viewMode === 'subject' ? '📚'
                : viewMode === 'chapter' ? '📖'
                : viewMode === 'year' ? '📅' : '📂';
              const hasQuiz = group.total > 0;
              return (
                <button
                  key={idx}
                  onClick={() => handleGroupClick(group)}
                  disabled={!hasQuiz}
                  style={{
                    padding: 16, textAlign: 'left',
                    background: hasQuiz
                      ? 'linear-gradient(160deg, #eff6ff 0%, #ffffff 100%)'
                      : 'linear-gradient(160deg, #f9fafb 0%, #ffffff 100%)',
                    border: hasQuiz ? '1px solid #c7d2fe' : '1px solid #e5e7eb',
                    borderRadius: 12, cursor: hasQuiz ? 'pointer' : 'not-allowed',
                    display: 'flex', flexDirection: 'column', gap: 6, position: 'relative',
                    opacity: hasQuiz ? 1 : 0.6,
                  }}
                >
                  {dm && (
                    <span style={{ position: 'absolute', top: 10, right: 10, fontSize: '0.7rem', fontWeight: 800,
                      background: dm.fg, color: '#fff', padding: '3px 8px', borderRadius: 999 }}>
                      난이도 {s.avgDiff.toFixed(1)}
                    </span>
                  )}
                  <div style={{ fontSize: '1.8rem', lineHeight: 1 }}>{modeIcon}</div>
                  <div style={{ fontWeight: 800, color: '#1e3a8a', fontSize: '1.05rem',
                    overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {group.title}
                  </div>
                  {group.subtitle && (
                    <div style={{ fontSize: '0.78rem', color: '#1f2937', fontWeight: 500,
                      overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {group.subtitle}
                    </div>
                  )}
                  <div style={{ marginTop: 8, height: 5, background: '#dbeafe', borderRadius: 3, overflow: 'hidden' }}>
                    <div style={{ width: `${Math.max(2, pct)}%`, height: '100%', background: '#4f46e5' }} />
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.88rem', color: '#111827', marginTop: 4 }}>
                    <span style={{ fontWeight: 800 }}>{pct}%</span>
                    <span style={{ color: '#1f2937', fontWeight: 600 }}>
                      {s.answered}/{group.total}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
