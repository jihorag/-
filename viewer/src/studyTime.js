// 자동 공부시간 기록 (열품타 스타일) — AI 학습/문제풀이 화면에 머문 시간을 일자별로 누적.
// localStorage 'quiz-studytime-v1': { 'YYYY-MM-DD': { ai: seconds, quiz: seconds } }

const KEY = 'quiz-studytime-v1';

const pad = (n) => String(n).padStart(2, '0');
export const dayKey = (d = new Date()) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

export const loadStudyTime = () => {
  try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; }
  catch { return {}; }
};
const save = (obj) => {
  try { localStorage.setItem(KEY, JSON.stringify(obj)); } catch { /* SSR */ }
};

// category: 'ai' | 'quiz'. secs는 누적 초(소수 허용 — 저장 시 반올림).
// subjectId: 과목 id(있으면 과목별 누적), unit: 단원/세션 라벨(과목 아래 중첩).
export const addStudySeconds = (category, secs, subjectId, unit) => {
  if (!category || !(secs > 0)) return;
  const all = loadStudyTime();
  const k = dayKey();
  const day = all[k] || { ai: 0, quiz: 0 };
  day[category] = Math.round((day[category] || 0) + secs);
  // 과목별(+단원) 누적
  if (subjectId) {
    day.subjects = day.subjects || {};
    const sj = day.subjects[subjectId] || { secs: 0, units: {} };
    sj.secs = Math.round(sj.secs + secs);
    if (unit) sj.units[unit] = Math.round((sj.units[unit] || 0) + secs);
    day.subjects[subjectId] = sj;
  }
  // 10분 슬롯(0~143)별 기록 — 시간대 그리드용
  const d = new Date();
  const slot = Math.floor((d.getHours() * 60 + d.getMinutes()) / 10); // 0..143
  day.slots = day.slots || {};
  const sl = day.slots[slot] || { ai: 0, quiz: 0 };
  sl[category] = Math.min(600, Math.round((sl[category] || 0) + secs)); // 한 슬롯 최대 600초
  day.slots[slot] = sl;
  all[k] = day;
  save(all);
};

// 해당 날짜의 10분 슬롯 기록 { slotIndex: { ai, quiz } }
export const getDaySlots = (key) => loadStudyTime()[key]?.slots || {};

// 해당 날짜의 과목별 기록 { subjectId: { secs, units: { label: secs } } }
export const getDaySubjects = (key) => loadStudyTime()[key]?.subjects || {};

export const getDayStudyTime = (key) => {
  const d = loadStudyTime()[key];
  return { ai: d?.ai || 0, quiz: d?.quiz || 0 };
};
export const getDayTotal = (key) => {
  const { ai, quiz } = getDayStudyTime(key);
  return ai + quiz;
};

// 초 → "1시간 23분" / "45분" / "30초"
export const fmtDuration = (secs) => {
  const s = Math.round(secs || 0);
  if (s < 60) return `${s}초`;
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (h > 0) return m > 0 ? `${h}시간 ${m}분` : `${h}시간`;
  return `${m}분`;
};
// 초 → "1:23:45" / "45:30" (타이머 표기)
export const fmtClock = (secs) => {
  const s = Math.round(secs || 0);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  return h > 0 ? `${h}:${pad(m)}:${pad(sec)}` : `${m}:${pad(sec)}`;
};
// 초 → "04:00:10" (항상 HH:MM:SS) — 과목별 시간 표기
export const fmtHMS = (secs) => {
  const s = Math.round(secs || 0);
  return `${pad(Math.floor(s / 3600))}:${pad(Math.floor((s % 3600) / 60))}:${pad(s % 60)}`;
};
