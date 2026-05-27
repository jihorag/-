// 모의고사 — 시험·연도 단위 시간제한 풀이 + 자동 채점 + 합격 추정
// localStorage:
//   quiz-mock-current  : 진행 중 세션(1개) — { exam, year, qids, startedAt, limitMs, answers }
//   quiz-mock-history  : 완료 세션 누적 배열
import { useState, useEffect, useMemo, useCallback } from 'react';
import { ArrowLeft } from 'lucide-react';
import { ParsedText } from './ParsedText';

const CUR_KEY = 'quiz-mock-current';
const HIST_KEY = 'quiz-mock-history';
const LIMIT_KEY = 'quiz-mock-limit';
const SHUFFLE_KEY = 'quiz-mock-shuffle';

// 기본 합격선(감정평가사 1차 규정). 다른 자격증도 비슷한 매과 40 / 평균 60 룰을 적용.
const PASS_SUBJ = 40;
const PASS_AVG = 60;
const LIMITS = [
  { ms: 60 * 60 * 1000, label: '60분' },
  { ms: 90 * 60 * 1000, label: '90분' },
  { ms: 100 * 60 * 1000, label: '100분' },
  { ms: 120 * 60 * 1000, label: '120분' },
  { ms: 240 * 60 * 1000, label: '240분' },
  { ms: 0, label: '무제한' },
];
const DEFAULT_LIMIT_MS = 120 * 60 * 1000;
// 시험별 1차 표준 시간(ms) — picker에 "권장" 힌트
const EXAM_STD_TIME = {
  '감정평가사': 120 * 60 * 1000,
  '세무사': 240 * 60 * 1000,
  '공인중개사': 100 * 60 * 1000,
};

const loadCurrent = () => {
  try { return JSON.parse(localStorage.getItem(CUR_KEY) || 'null'); }
  catch { return null; }
};
const saveCurrent = (s) => {
  try {
    if (s) localStorage.setItem(CUR_KEY, JSON.stringify(s));
    else localStorage.removeItem(CUR_KEY);
  } catch { /* SSR */ }
};
const loadHistory = () => {
  try { return JSON.parse(localStorage.getItem(HIST_KEY) || '[]') || []; }
  catch { return []; }
};
const saveHistory = (arr) => {
  try { localStorage.setItem(HIST_KEY, JSON.stringify(arr.slice(-50))); } catch { /* SSR */ }
};

const fmtClock = (ms) => {
  if (ms < 0) ms = 0;
  const s = Math.floor(ms / 1000);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const ss = s % 60;
  const pad = (n) => String(n).padStart(2, '0');
  return h > 0 ? `${pad(h)}:${pad(m)}:${pad(ss)}` : `${pad(m)}:${pad(ss)}`;
};
const fmtDate = (ts) => {
  const d = new Date(ts);
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
};

// 결정론적 셔플(시드 기반) — 같은 시험·연도·시작시각이면 같은 순서 → 새로고침 안정
const shuffleSeeded = (arr, seed) => {
  let s = seed >>> 0;
  const out = arr.slice();
  for (let i = out.length - 1; i > 0; i--) {
    s = (s * 1664525 + 1013904223) >>> 0;
    const j = s % (i + 1);
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
};
const hashStr = (str) => {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < str.length; i++) {
    h = (h ^ str.charCodeAt(i)) >>> 0;
    h = (h * 16777619) >>> 0;
  }
  return h;
};

// 시험·연도 후보 도출: 분류된 문제만 집계, 과목별 분포까지
function buildPicker(classifiedList) {
  const map = new Map();
  for (const q of classifiedList) {
    const ex = q.exam || '기타';
    const yr = String(q.year || '미상');
    const key = `${ex}__${yr}`;
    if (!map.has(key)) map.set(key, { exam: ex, year: yr, total: 0, subjects: {} });
    const e = map.get(key);
    e.total++;
    const subj = q.taxSubjectName || '기타';
    e.subjects[subj] = (e.subjects[subj] || 0) + 1;
  }
  // 과목 ≥ 3개, 문항 ≥ 100개인 시험만 모의고사 후보로 노출 (1과목 한정은 의미 약함)
  return [...map.values()]
    .filter(e => Object.keys(e.subjects).length >= 3 && e.total >= 100)
    .sort((a, b) => {
      if (b.year !== a.year) return b.year.localeCompare(a.year);
      return a.exam.localeCompare(b.exam);
    });
}

// 사용자 정답률(과목별) — Monte Carlo 추정에 사용
function subjectAccuracyMap(classifiedList, progress, qidFn) {
  const m = {};
  let totalCorrect = 0, totalScored = 0;
  for (const q of classifiedList) {
    const p = progress[qidFn(q)];
    if (!p || (p.correct !== true && p.correct !== false)) continue;
    const subj = q.taxSubjectName || '기타';
    const a = m[subj] || (m[subj] = { c: 0, n: 0 });
    a.n++; totalScored++;
    if (p.correct) { a.c++; totalCorrect++; }
  }
  const overall = totalScored ? totalCorrect / totalScored : 0.5;
  return { perSubj: m, overall, scoredTotal: totalScored };
}

// 합격 확률 추정 — Monte Carlo (1000회): 매과 ≥ PASS_SUBJ, 평균 ≥ PASS_AVG
function passProb(subjectCounts, accMap) {
  const trials = 1000;
  const subjs = Object.entries(subjectCounts); // [[name, count]]
  if (!subjs.length) return null;
  const totalQ = subjs.reduce((s, [, n]) => s + n, 0);
  const ps = subjs.map(([name, count]) => {
    const a = accMap.perSubj[name];
    const p = a && a.n >= 3 ? a.c / a.n : accMap.overall;
    return { name, count, p: Math.max(0.05, Math.min(0.95, p)) };
  });
  let pass = 0;
  for (let t = 0; t < trials; t++) {
    let totalCorrect = 0;
    let perOk = true;
    for (const { count, p } of ps) {
      let c = 0;
      for (let i = 0; i < count; i++) if (Math.random() < p) c++;
      totalCorrect += c;
      if ((c / count) * 100 < PASS_SUBJ) perOk = false;
    }
    if (!perOk) continue;
    if ((totalCorrect / totalQ) * 100 >= PASS_AVG) pass++;
  }
  return pass / trials;
}

// ─────────────────────────────────────────────────────────────────────
const MockExam = ({ mode, classifiedList, progress, recordAnswer, qidFn,
                    onNavigate, onStartReview, fontScale,
                    browseExam, examDates }) => {
  // mode: 'mock' | 'mockSession' | 'mockResult'
  const [current, setCurrent] = useState(() => loadCurrent());
  const [history, setHistory] = useState(() => loadHistory());
  const [now, setNow] = useState(() => Date.now());
  const [limitChoice, setLimitChoice] = useState(() => {
    try { const v = parseInt(localStorage.getItem(LIMIT_KEY), 10);
      return LIMITS.some(l => l.ms === v) ? v : DEFAULT_LIMIT_MS; }
    catch { return DEFAULT_LIMIT_MS; }
  });
  const [shuffleOn, setShuffleOn] = useState(() => {
    try { return localStorage.getItem(SHUFFLE_KEY) !== '0'; } catch { return true; }
  });
  // 세션 화면: 문항 인덱스, 팔레트 모달
  const [idx, setIdx] = useState(0);
  const [palette, setPalette] = useState(false);
  const [confirmSubmit, setConfirmSubmit] = useState(false);
  // 결과 화면: 무엇을 표시할지 (마지막 완료 항목 or 선택)
  const [resultId, setResultId] = useState(null);
  // history 필터: '' = 전체, 'mode' = 현재 모드 시험만
  const [historyFilter, setHistoryFilter] = useState('mode');

  // 1초 틱(세션 모드일 때만 활성)
  useEffect(() => {
    if (mode !== 'mockSession') return;
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, [mode]);

  useEffect(() => { try { localStorage.setItem(LIMIT_KEY, String(limitChoice)); } catch { /* SSR */ } }, [limitChoice]);
  useEffect(() => { try { localStorage.setItem(SHUFFLE_KEY, shuffleOn ? '1' : '0'); } catch { /* SSR */ } }, [shuffleOn]);

  // 진입 시 새 세션 없으면 picker로 부드럽게 강등
  useEffect(() => {
    if (mode === 'mockSession' && !current) onNavigate('mock');
    if (mode === 'mockResult' && !resultId && history.length) setResultId(history[history.length - 1].id);
    if (mode === 'mockResult' && !history.length) onNavigate('mock');
  }, [mode, current, history, resultId, onNavigate]);

  const pickerRaw = useMemo(() => buildPicker(classifiedList), [classifiedList]);
  // browseExam이 set이면 그 시험을 picker 최상단으로
  const picker = useMemo(() => {
    if (!browseExam) return pickerRaw;
    return [...pickerRaw].sort((a, b) => {
      const aMatch = a.exam === browseExam ? 0 : 1;
      const bMatch = b.exam === browseExam ? 0 : 1;
      if (aMatch !== bMatch) return aMatch - bMatch;
      return b.year.localeCompare(a.year);
    });
  }, [pickerRaw, browseExam]);
  // history filter — 모드 필터링 + 모드 미설정 시 자동 전체
  const filteredHistory = useMemo(() => {
    if (!browseExam || historyFilter !== 'mode') return history;
    return history.filter(r => r.exam === browseExam);
  }, [history, browseExam, historyFilter]);
  // 문항 id → 객체 맵 — 12k 엔트리를 1초 틱마다 재구축하지 않도록 캐시
  const qById = useMemo(() => {
    const m = new Map();
    for (const q of classifiedList) m.set(qidFn(q), q);
    return m;
  }, [classifiedList, qidFn]);

  // ───────── 세션 시작/종료 ─────────
  const startMock = useCallback((exam, year) => {
    const all = classifiedList.filter(q => (q.exam || '기타') === exam && String(q.year || '') === String(year));
    if (!all.length) return;
    // 과목별 묶음 → 시험지 순서: 과목 묶음(과목 내 정렬)
    const bySubj = {};
    for (const q of all) {
      const s = q.taxSubjectName || '기타';
      (bySubj[s] || (bySubj[s] = [])).push(q);
    }
    const subjectsSorted = Object.keys(bySubj).sort();
    const startedAt = Date.now();
    const seed = hashStr(`${exam}|${year}|${startedAt}`);
    const ordered = [];
    for (const s of subjectsSorted) {
      const list = bySubj[s].slice().sort((a, b) => (a.number || 0) - (b.number || 0));
      ordered.push(...(shuffleOn ? shuffleSeeded(list, seed ^ hashStr(s)) : list));
    }
    const session = {
      exam, year,
      qids: ordered.map(qidFn),
      startedAt,
      limitMs: limitChoice,
      answers: {},
      submitted: false,
    };
    saveCurrent(session);
    setCurrent(session);
    setIdx(0);
    setPalette(false);
    setConfirmSubmit(false);
    onNavigate('mockSession');
  }, [classifiedList, qidFn, limitChoice, shuffleOn, onNavigate]);

  const updateAnswer = useCallback((qId, sel) => {
    setCurrent(prev => {
      if (!prev || prev.submitted) return prev;
      const next = { ...prev, answers: { ...prev.answers, [qId]: sel } };
      saveCurrent(next);
      return next;
    });
  }, []);

  const submitMock = useCallback((auto = false) => {
    const s = current;
    if (!s || s.submitted) return;
    const endedAt = Date.now();
    const elapsedMs = endedAt - s.startedAt;
    // 채점
    const subjectCounts = {};
    const subjectScore = {};
    const wrongIds = [];
    for (const id of s.qids) {
      const q = qById.get(id);
      if (!q) continue;
      const subj = q.taxSubjectName || '기타';
      subjectCounts[subj] = (subjectCounts[subj] || 0) + 1;
      const sel = s.answers[id];
      const hasAnswer = !!q.answerNorm;
      const correct = hasAnswer && sel === q.answerNorm;
      if (!subjectScore[subj]) subjectScore[subj] = { correct: 0, total: 0, gradable: 0 };
      subjectScore[subj].total++;
      if (hasAnswer) {
        subjectScore[subj].gradable++;
        if (correct) subjectScore[subj].correct++;
        else if (sel != null) wrongIds.push(id);
        // 기존 풀이 진척에도 반영 (정답 정보 있는 경우만)
        if (sel != null && recordAnswer) recordAnswer(q, sel, correct);
      }
    }
    let totalCorrect = 0, totalGradable = 0;
    let passSubj = true;
    const subjects = Object.entries(subjectScore).map(([name, v]) => {
      const pct = v.gradable ? Math.round((v.correct / v.gradable) * 100) : null;
      totalCorrect += v.correct;
      totalGradable += v.gradable;
      if (pct != null && pct < PASS_SUBJ) passSubj = false;
      return { name, ...v, pct };
    }).sort((a, b) => a.name.localeCompare(b.name));
    const avgPct = totalGradable ? Math.round((totalCorrect / totalGradable) * 100) : null;
    const passAvg = avgPct != null && avgPct >= PASS_AVG;
    const passed = passSubj && passAvg;
    // 합격 추정(과거 정답률 기반)
    const accMap = subjectAccuracyMap(classifiedList, progress, qidFn);
    const estProb = passProb(subjectCounts, accMap);

    const record = {
      id: `${s.exam}-${s.year}-${s.startedAt}`,
      exam: s.exam, year: s.year,
      startedAt: s.startedAt, endedAt, elapsedMs, limitMs: s.limitMs,
      qids: s.qids, answers: s.answers, wrongIds,
      subjects, totalCorrect, totalGradable,
      avgPct, passSubj, passAvg, passed,
      estProb, auto,
    };
    const nextHist = [...history, record];
    setHistory(nextHist);
    saveHistory(nextHist);
    saveCurrent(null);
    setCurrent(null);
    setResultId(record.id);
    onNavigate('mockResult');
  }, [current, classifiedList, qById, qidFn, recordAnswer, progress, history, onNavigate]);

  const abandonMock = useCallback(() => {
    saveCurrent(null);
    setCurrent(null);
    onNavigate('mock');
  }, [onNavigate]);

  // 시간 초과 자동 제출
  useEffect(() => {
    if (mode !== 'mockSession' || !current || current.submitted || !current.limitMs) return;
    const remaining = current.startedAt + current.limitMs - now;
    if (remaining <= 0) submitMock(true);
  }, [mode, current, now, submitMock]);

  // ═══════════════════ 화면별 렌더 ═══════════════════
  const wrap = (children) => (
    <div className="app-container" style={{ '--q-fs': fontScale }}>{children}</div>
  );

  // ───── PICKER ─────
  if (mode === 'mock') {
    return wrap(<>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
        <button className="back-btn" onClick={() => onNavigate('home')}>
          <ArrowLeft size={24} style={{ marginRight: 8 }} />
          <span style={{ fontSize: '1rem', fontWeight: 600 }}>홈</span>
        </button>
      </header>
      <div className="screen-head"><h1 className="screen-title">🎯 모의고사</h1>
        <p style={{ fontSize: '0.85rem', color: '#6b7280', marginTop: 4 }}>
          실제 시험처럼 한 회차를 시간 제한으로 풀고 채점·합격 추정까지
        </p>
      </div>
      <main className="main-content" style={{ marginTop: 16 }}>

        {current && !current.submitted && (() => {
          const remaining = current.limitMs ? Math.max(0, current.startedAt + current.limitMs - now) : null;
          const answered = Object.keys(current.answers).length;
          return (
            <button onClick={() => onNavigate('mockSession')} style={{
              width: '100%', textAlign: 'left', padding: '16px',
              borderRadius: 14, border: '1px solid #93c5fd', background: '#eff6ff',
              cursor: 'pointer', marginBottom: 16 }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#1d4ed8' }}>이어서 풀기</div>
              <div style={{ fontSize: '1.05rem', fontWeight: 800, color: '#111827', marginTop: 4 }}>
                {current.exam} · {current.year}년
              </div>
              <div style={{ fontSize: '0.85rem', color: '#374151', marginTop: 6 }}>
                {answered} / {current.qids.length} 풀이
                {remaining != null && <> · 남은 시간 <b>{fmtClock(remaining)}</b></>}
              </div>
            </button>
          );
        })()}

        <section style={{ background: '#fff', borderRadius: 14, padding: 16,
          boxShadow: 'var(--shadow-sm)', marginBottom: 12 }}>
          <div style={{ fontWeight: 700, fontSize: '0.92rem', color: '#374151' }}>제한 시간</div>
          <div style={{ display: 'flex', gap: 8, marginTop: 10, flexWrap: 'wrap' }}>
            {LIMITS.map(l => {
              const on = limitChoice === l.ms;
              return (
                <button key={l.label} onClick={() => setLimitChoice(l.ms)}
                  style={{ flex: '1 1 auto', minWidth: 64, padding: '9px 10px',
                    borderRadius: 9, cursor: 'pointer', fontSize: '0.85rem', fontWeight: 600,
                    border: on ? '1px solid #2563eb' : '1px solid #d1d5db',
                    background: on ? '#eff6ff' : '#fff', color: on ? '#1d4ed8' : '#6b7280' }}>
                  {l.label}
                </button>
              );
            })}
          </div>
          <div style={{ marginTop: 14, display: 'flex', justifyContent: 'space-between',
            alignItems: 'center', gap: 12 }}>
            <div>
              <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#374151' }}>문항 셔플</div>
              <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: 2 }}>
                과목 내 순서를 섞어요. 실제 시험과 더 비슷한 긴장감
              </div>
            </div>
            <button onClick={() => setShuffleOn(s => !s)}
              style={{ border: shuffleOn ? '1px solid #2563eb' : '1px solid #d1d5db',
                background: shuffleOn ? '#eff6ff' : '#fff', color: shuffleOn ? '#1d4ed8' : '#6b7280',
                borderRadius: 9, padding: '8px 14px', fontSize: '0.85rem',
                fontWeight: 600, cursor: 'pointer' }}>
              {shuffleOn ? '켜짐' : '꺼짐'}
            </button>
          </div>
        </section>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
          margin: '18px 2px 10px' }}>
          <div style={{ fontWeight: 700, fontSize: '0.95rem', color: '#374151' }}>
            이용 가능한 회차
            {browseExam && (
              <span style={{ marginLeft: 6, fontSize: '0.78rem', color: '#1d4ed8', fontWeight: 700 }}>
                · {browseExam} 우선
              </span>
            )}
          </div>
          {browseExam && EXAM_STD_TIME[browseExam] && EXAM_STD_TIME[browseExam] !== limitChoice && (
            <button onClick={() => setLimitChoice(EXAM_STD_TIME[browseExam])}
              style={{ fontSize: '0.72rem', color: '#1d4ed8', background: '#eff6ff',
                border: '1px solid #93c5fd', borderRadius: 8, padding: '4px 8px',
                fontWeight: 700, cursor: 'pointer' }}>
              {browseExam} 표준 {Math.round(EXAM_STD_TIME[browseExam] / 60000)}분으로 →
            </button>
          )}
        </div>
        {picker.length === 0 && (
          <div style={{ background: '#fff', borderRadius: 12, padding: 18,
            color: '#9ca3af', fontSize: '0.9rem', textAlign: 'center' }}>
            분류된 문제가 충분한 시험 회차가 없어요.
          </div>
        )}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {picker.map(p => {
            const subjs = Object.entries(p.subjects).sort((a, b) => b[1] - a[1]);
            const isCurMode = browseExam && p.exam === browseExam;
            return (
              <button key={`${p.exam}-${p.year}`} onClick={() => startMock(p.exam, p.year)}
                style={{ background: '#fff', borderRadius: 12, padding: 16,
                  border: isCurMode ? '2px solid #2563eb' : '1px solid #e5e7eb',
                  textAlign: 'left', cursor: 'pointer',
                  boxShadow: 'var(--shadow-sm)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                  <div style={{ fontWeight: 800, fontSize: '1rem', color: '#111827' }}>
                    {p.exam} · {p.year}년
                    {isCurMode && (
                      <span style={{ marginLeft: 6, fontSize: '0.7rem', fontWeight: 700,
                        background: '#dbeafe', color: '#1e40af', padding: '2px 7px',
                        borderRadius: 999 }}>
                        현재 모드
                      </span>
                    )}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#2563eb', fontWeight: 700 }}>시작 →</div>
                </div>
                <div style={{ fontSize: '0.82rem', color: '#6b7280', marginTop: 6 }}>
                  {p.total}문제 · {subjs.length}과목
                </div>
                <div style={{ display: 'flex', gap: 6, marginTop: 8, flexWrap: 'wrap' }}>
                  {subjs.slice(0, 6).map(([name, n]) => (
                    <span key={name} style={{ fontSize: '0.72rem', padding: '3px 9px',
                      borderRadius: 999, background: '#f3f4f6', color: '#4b5563', fontWeight: 600 }}>
                      {name} {n}
                    </span>
                  ))}
                </div>
              </button>
            );
          })}
        </div>

        {history.length > 0 && (
          <>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
              margin: '24px 2px 10px' }}>
              <div style={{ fontWeight: 700, fontSize: '0.95rem', color: '#374151' }}>
                이전 기록 {browseExam && historyFilter === 'mode'
                  ? `(${browseExam} ${filteredHistory.length}건)`
                  : `(전체 ${history.length}건)`}
              </div>
              {browseExam && (
                <button onClick={() => setHistoryFilter(historyFilter === 'mode' ? '' : 'mode')}
                  style={{ fontSize: '0.72rem', color: '#6b7280', background: 'none',
                    border: '1px solid #d1d5db', borderRadius: 8, padding: '4px 10px',
                    fontWeight: 600, cursor: 'pointer' }}>
                  {historyFilter === 'mode' ? '전체 보기' : `${browseExam}만`}
                </button>
              )}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {[...filteredHistory].reverse().slice(0, 10).map(r => (
                <button key={r.id} onClick={() => { setResultId(r.id); onNavigate('mockResult'); }}
                  style={{ background: '#fff', borderRadius: 10, padding: '12px 14px',
                    border: '1px solid #e5e7eb', textAlign: 'left', cursor: 'pointer',
                    display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#111827' }}>
                      {r.exam} {r.year}년
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: 2 }}>
                      {fmtDate(r.startedAt)} · {fmtClock(r.elapsedMs)}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '1rem', fontWeight: 800,
                      color: r.passed ? '#16a34a' : '#dc2626' }}>
                      {r.avgPct ?? '—'}점 · {r.passed ? '합격' : '불합격'}
                    </div>
                    <div style={{ fontSize: '0.72rem', color: '#9ca3af' }}>자세히 →</div>
                  </div>
                </button>
              ))}
              {filteredHistory.length === 0 && (
                <div style={{ fontSize: '0.82rem', color: '#9ca3af', padding: '12px 0' }}>
                  이 모드에서 푼 회차가 없어요.
                </div>
              )}
            </div>
          </>
        )}

        <div style={{ marginTop: 20, padding: 12, borderRadius: 10,
          background: '#fafafa', border: '1px solid #e5e7eb', fontSize: '0.78rem', color: '#6b7280' }}>
          합격 기준: 매 과목 {PASS_SUBJ}점 이상 + 평균 {PASS_AVG}점 이상.
          {browseExam && examDate && (() => {
            const d = (() => {
              const dt = new Date(examDate + 'T00:00:00');
              if (isNaN(dt)) return null;
              const t = new Date(); t.setHours(0,0,0,0);
              return Math.ceil((dt - t) / 86400000);
            })();
            if (d == null) return null;
            return (
              <div style={{ marginTop: 4, color: d <= 30 ? '#dc2626' : '#1d4ed8', fontWeight: 700 }}>
                📅 {browseExam} D-{d}일 남음 — 시험 시뮬레이션 추천
              </div>
            );
          })()}
        </div>
      </main>
    </>);
  }

  // ───── SESSION ─────
  if (mode === 'mockSession') {
    if (!current) return wrap(<div style={{ padding: 24 }}>세션을 불러오는 중…</div>);
    const total = current.qids.length;
    const safeIdx = Math.min(Math.max(0, idx), total - 1);
    const curId = current.qids[safeIdx];
    const q = qById.get(curId);
    const answered = Object.keys(current.answers).length;
    const remaining = current.limitMs ? Math.max(0, current.startedAt + current.limitMs - now) : null;
    const timeWarn = remaining != null && remaining < 5 * 60 * 1000;
    const sel = current.answers[curId] || null;
    const opts = (q && q.options) || [];

    const goto = (i) => { setIdx(Math.min(Math.max(0, i), total - 1)); window.scrollTo(0, 0); };
    const onPick = (n) => updateAnswer(curId, String(n));
    const onClearPick = () => {
      setCurrent(prev => {
        if (!prev) return prev;
        const ans = { ...prev.answers };
        delete ans[curId];
        const next = { ...prev, answers: ans };
        saveCurrent(next);
        return next;
      });
    };

    return wrap(<>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb',
        display: 'flex', justifyContent: 'space-between' }}>
        <button className="back-btn" onClick={() => onNavigate('mock')}>
          <ArrowLeft size={24} style={{ marginRight: 8 }} />
          <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>저장하고 종료</span>
        </button>
        {remaining != null && (
          <div style={{ display: 'flex', alignItems: 'center', padding: '6px 12px',
            borderRadius: 8, fontWeight: 800, fontSize: '0.95rem',
            background: timeWarn ? '#fef2f2' : '#f3f4f6',
            color: timeWarn ? '#dc2626' : '#374151' }}>
            ⏱ {fmtClock(remaining)}
          </div>
        )}
      </header>

      <div style={{ padding: '12px 16px 0' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
          fontSize: '0.85rem', color: '#6b7280', marginBottom: 6 }}>
          <span>{current.exam} {current.year}년 · {q && q.taxSubjectName}</span>
          <span>{safeIdx + 1} / {total} · 응답 {answered}</span>
        </div>
        <div style={{ height: 6, background: '#e5e7eb', borderRadius: 3, overflow: 'hidden' }}>
          <div style={{ width: `${((safeIdx + 1) / total) * 100}%`, height: '100%',
            background: '#2563eb', transition: 'width 0.2s' }} />
        </div>
      </div>

      <main className="main-content" style={{ marginTop: 12 }}>
        {q ? (
          <div style={{ background: '#fff', borderRadius: 12, padding: 20,
            boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
            <div style={{ fontWeight: 700, fontSize: '1.05rem', color: '#2563eb', marginBottom: 12 }}>
              Q. {q.number}
            </div>
            <div className="q-text" style={{ lineHeight: 1.6, fontWeight: 600 }}>
              <ParsedText text={q.question} />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 18 }}>
              {(opts.length ? opts : ['', '', '', '']).map((o, i) => {
                const n = i + 1;
                const on = sel === String(n);
                return (
                  <button key={i} onClick={() => onPick(n)}
                    className="opt-btn"
                    style={{ background: on ? '#eff6ff' : '#f9fafb',
                      borderColor: on ? '#93c5fd' : '#e5e7eb' }}>
                    <span style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                      width: 26, height: 26, borderRadius: '50%',
                      background: on ? '#2563eb' : '#fff', color: on ? '#fff' : '#4b5563',
                      border: on ? 'none' : '1.5px solid #d1d5db',
                      fontSize: '0.875rem', fontWeight: 700, flexShrink: 0 }}>
                      {n}
                    </span>
                    <span className="q-opt" style={{ lineHeight: 1.5, color: '#1f2937' }}>
                      {o ? <ParsedText text={o} /> : `${n}번`}
                    </span>
                  </button>
                );
              })}
            </div>
            {sel && (
              <button onClick={onClearPick}
                style={{ marginTop: 12, padding: '7px 12px', fontSize: '0.8rem',
                  border: '1px solid #e5e7eb', background: '#fff', color: '#6b7280',
                  borderRadius: 8, cursor: 'pointer' }}>
                선택 해제
              </button>
            )}
          </div>
        ) : (
          <div style={{ padding: 20, color: '#9ca3af' }}>문항을 찾을 수 없어요.</div>
        )}
      </main>

      <div style={{ position: 'sticky', bottom: 0, background: '#fff',
        borderTop: '1px solid #e5e7eb', padding: '10px 12px',
        display: 'flex', gap: 8, alignItems: 'center' }}>
        <button onClick={() => goto(safeIdx - 1)} disabled={safeIdx === 0}
          style={{ flex: 1, padding: '10px', borderRadius: 8, fontWeight: 700,
            border: '1px solid #d1d5db', background: '#fff', color: '#374151',
            cursor: safeIdx === 0 ? 'default' : 'pointer', opacity: safeIdx === 0 ? 0.4 : 1 }}>
          ← 이전
        </button>
        <button onClick={() => setPalette(true)}
          style={{ padding: '10px 14px', borderRadius: 8, fontWeight: 700,
            border: '1px solid #d1d5db', background: '#fff', color: '#374151',
            cursor: 'pointer' }}>
          ▦
        </button>
        <button onClick={() => goto(safeIdx + 1)} disabled={safeIdx >= total - 1}
          style={{ flex: 1, padding: '10px', borderRadius: 8, fontWeight: 700,
            border: '1px solid #d1d5db', background: '#fff', color: '#374151',
            cursor: safeIdx >= total - 1 ? 'default' : 'pointer',
            opacity: safeIdx >= total - 1 ? 0.4 : 1 }}>
          다음 →
        </button>
        <button onClick={() => setConfirmSubmit(true)}
          style={{ padding: '10px 14px', borderRadius: 8, fontWeight: 700,
            border: 'none', background: '#2563eb', color: '#fff', cursor: 'pointer' }}>
          제출
        </button>
      </div>

      {palette && (
        <div onClick={() => setPalette(false)} style={{ position: 'fixed', inset: 0,
          background: 'rgba(0,0,0,0.5)', zIndex: 100, display: 'flex', alignItems: 'flex-end' }}>
          <div onClick={(e) => e.stopPropagation()}
            style={{ background: '#fff', width: '100%', maxHeight: '70vh', overflow: 'auto',
              borderRadius: '16px 16px 0 0', padding: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between',
              alignItems: 'center', marginBottom: 14 }}>
              <div style={{ fontWeight: 800, fontSize: '1rem' }}>문항 팔레트</div>
              <button onClick={() => setPalette(false)} style={{ border: 'none',
                background: 'none', fontSize: '1.3rem', cursor: 'pointer' }}>✕</button>
            </div>
            <div style={{ fontSize: '0.78rem', color: '#6b7280', marginBottom: 10 }}>
              <span style={{ display: 'inline-block', width: 10, height: 10, background: '#2563eb',
                borderRadius: 3, marginRight: 4 }}></span> 응답
              <span style={{ marginLeft: 10, display: 'inline-block', width: 10, height: 10,
                background: '#fff', border: '1.5px solid #d1d5db', borderRadius: 3,
                marginRight: 4 }}></span> 미응답
              <span style={{ marginLeft: 10, display: 'inline-block', width: 10, height: 10,
                background: '#fbbf24', borderRadius: 3, marginRight: 4 }}></span> 현재
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(8, 1fr)', gap: 6 }}>
              {current.qids.map((id, i) => {
                const ans = !!current.answers[id];
                const isCur = i === safeIdx;
                return (
                  <button key={id} onClick={() => { goto(i); setPalette(false); }}
                    style={{ aspectRatio: '1', padding: 0, borderRadius: 6,
                      border: isCur ? '2px solid #fbbf24'
                        : ans ? 'none' : '1.5px solid #d1d5db',
                      background: ans && !isCur ? '#2563eb' : '#fff',
                      color: ans && !isCur ? '#fff' : '#374151',
                      fontWeight: 700, fontSize: '0.78rem', cursor: 'pointer' }}>
                    {i + 1}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {confirmSubmit && (
        <div onClick={() => setConfirmSubmit(false)} style={{ position: 'fixed', inset: 0,
          background: 'rgba(0,0,0,0.5)', zIndex: 110, display: 'flex',
          alignItems: 'center', justifyContent: 'center', padding: 24 }}>
          <div onClick={(e) => e.stopPropagation()}
            style={{ background: '#fff', borderRadius: 14, padding: 22, maxWidth: 360, width: '100%' }}>
            <div style={{ fontWeight: 800, fontSize: '1.05rem', color: '#111827' }}>제출할까요?</div>
            <div style={{ fontSize: '0.88rem', color: '#6b7280', marginTop: 8 }}>
              {total - answered > 0
                ? `미응답 ${total - answered}문제가 남아 있어요. 제출 후엔 수정할 수 없어요.`
                : '모든 문항에 응답했어요. 채점을 시작합니다.'}
            </div>
            <div style={{ display: 'flex', gap: 8, marginTop: 18 }}>
              <button onClick={() => setConfirmSubmit(false)}
                style={{ flex: 1, padding: '10px', borderRadius: 8, fontWeight: 700,
                  border: '1px solid #d1d5db', background: '#fff', color: '#374151',
                  cursor: 'pointer' }}>취소</button>
              <button onClick={() => { setConfirmSubmit(false); submitMock(false); }}
                style={{ flex: 1, padding: '10px', borderRadius: 8, fontWeight: 700,
                  border: 'none', background: '#2563eb', color: '#fff',
                  cursor: 'pointer' }}>제출하기</button>
            </div>
            {!current.submitted && (
              <button onClick={() => { setConfirmSubmit(false); if (window.confirm('진행 중 세션을 버릴까요? 응답은 사라져요.')) abandonMock(); }}
                style={{ marginTop: 10, width: '100%', padding: '8px', fontSize: '0.82rem',
                  background: 'none', border: 'none', color: '#dc2626',
                  cursor: 'pointer' }}>세션 버리기</button>
            )}
          </div>
        </div>
      )}
    </>);
  }

  // ───── RESULT ─────
  if (mode === 'mockResult') {
    const r = history.find(x => x.id === resultId) || history[history.length - 1];
    if (!r) return wrap(<div style={{ padding: 24 }}>결과가 없어요.</div>);
    const accent = r.passed ? '#16a34a' : '#dc2626';
    const bg = r.passed ? '#f0fdf4' : '#fef2f2';
    return wrap(<>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
        <button className="back-btn" onClick={() => onNavigate('mock')}>
          <ArrowLeft size={24} style={{ marginRight: 8 }} />
          <span style={{ fontSize: '1rem', fontWeight: 600 }}>모의고사 목록</span>
        </button>
      </header>
      <main className="main-content" style={{ marginTop: 16 }}>
        <section style={{ background: bg, borderRadius: 14, padding: 20,
          border: `1px solid ${r.passed ? '#bbf7d0' : '#fecaca'}`, marginBottom: 16 }}>
          <div style={{ fontSize: '0.78rem', fontWeight: 700, color: accent }}>
            {r.exam} · {r.year}년 모의고사
          </div>
          <div style={{ fontSize: '1.65rem', fontWeight: 800, color: accent, marginTop: 8 }}>
            {r.passed ? '✓ 합격선 통과' : '✕ 합격선 미달'}
          </div>
          <div style={{ fontSize: '0.95rem', color: '#374151', marginTop: 8 }}>
            평균 <b style={{ color: accent, fontSize: '1.1rem' }}>{r.avgPct ?? '—'}점</b>
            {r.totalGradable > 0 && <> · 총 {r.totalGradable}문 채점 중 {r.totalCorrect}개 정답</>}
            <br />소요 {fmtClock(r.elapsedMs)}{r.auto && ' (시간 초과 자동 제출)'}
          </div>
          <div style={{ marginTop: 10, fontSize: '0.8rem', color: '#6b7280' }}>
            합격 기준: 매과목 {PASS_SUBJ}점 + 평균 {PASS_AVG}점
            <span style={{ marginLeft: 8, color: r.passSubj ? '#16a34a' : '#dc2626', fontWeight: 700 }}>
              과목 {r.passSubj ? '✓' : '✕'}
            </span>
            <span style={{ marginLeft: 6, color: r.passAvg ? '#16a34a' : '#dc2626', fontWeight: 700 }}>
              평균 {r.passAvg ? '✓' : '✕'}
            </span>
          </div>
        </section>

        <div style={{ fontWeight: 800, fontSize: '0.95rem', color: '#374151', margin: '0 2px 10px' }}>
          과목별 점수
        </div>
        <div style={{ background: '#fff', borderRadius: 12, padding: 14,
          boxShadow: 'var(--shadow-sm)', marginBottom: 14 }}>
          {r.subjects.map(s => {
            const ok = s.pct == null || s.pct >= PASS_SUBJ;
            return (
              <div key={s.name} style={{ display: 'flex', alignItems: 'center', gap: 10,
                padding: '8px 0', borderBottom: '1px solid #f3f4f6' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#374151' }}>{s.name}</div>
                  <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: 2 }}>
                    {s.gradable ? `${s.correct}/${s.gradable}` : `${s.total}문 (채점 불가)`}
                  </div>
                </div>
                <div style={{ width: 90, height: 6, background: '#e5e7eb',
                  borderRadius: 3, overflow: 'hidden' }}>
                  {s.pct != null && (
                    <div style={{ width: `${s.pct}%`, height: '100%',
                      background: ok ? '#2563eb' : '#dc2626' }} />
                  )}
                </div>
                <div style={{ width: 56, textAlign: 'right',
                  fontWeight: 800, fontSize: '0.95rem', color: ok ? '#1d4ed8' : '#dc2626' }}>
                  {s.pct != null ? `${s.pct}점` : '—'}
                </div>
              </div>
            );
          })}
        </div>

        {r.estProb != null && (
          <div style={{ background: '#fffbeb', border: '1px solid #fde68a',
            borderRadius: 12, padding: 16, marginBottom: 14 }}>
            <div style={{ fontWeight: 800, fontSize: '0.92rem', color: '#92400e' }}>
              🎲 합격 추정 (지금 정답률로 1000회 시뮬레이션)
            </div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#92400e', marginTop: 6 }}>
              {Math.round(r.estProb * 100)}%
            </div>
            <div style={{ fontSize: '0.75rem', color: '#9a6914', marginTop: 4 }}>
              과목별 누적 정답률 기반. 표본 5문 미만 과목은 전체 평균으로 대체.
            </div>
          </div>
        )}

        {r.wrongIds && r.wrongIds.length > 0 && (
          <button onClick={() => onStartReview(r.wrongIds, `모의고사 오답 (${r.exam} ${r.year})`, 'mockResult')}
            style={{ width: '100%', padding: '14px', borderRadius: 12,
              background: '#dc2626', color: '#fff', border: 'none',
              fontWeight: 800, fontSize: '0.95rem', cursor: 'pointer', marginBottom: 10 }}>
            🔁 오답 {r.wrongIds.length}문제만 복습하기
          </button>
        )}
        <button onClick={() => onNavigate('mock')}
          style={{ width: '100%', padding: '12px', borderRadius: 12,
            background: '#fff', color: '#374151', border: '1px solid #d1d5db',
            fontWeight: 700, fontSize: '0.9rem', cursor: 'pointer', marginBottom: 24 }}>
          모의고사 목록으로
        </button>

        {history.length > 1 && (
          <>
            <div style={{ fontWeight: 800, fontSize: '0.92rem', color: '#374151', margin: '4px 2px 10px' }}>
              이전 회차
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {[...history].reverse().filter(x => x.id !== r.id).slice(0, 5).map(h => (
                <button key={h.id} onClick={() => setResultId(h.id)}
                  style={{ background: '#fff', borderRadius: 8, padding: '10px 12px',
                    border: '1px solid #e5e7eb', textAlign: 'left', cursor: 'pointer',
                    display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.85rem', color: '#374151' }}>
                    {h.exam} {h.year}년 · {fmtDate(h.startedAt)}
                  </span>
                  <span style={{ fontWeight: 700, fontSize: '0.85rem',
                    color: h.passed ? '#16a34a' : '#dc2626' }}>
                    {h.avgPct ?? '—'}점
                  </span>
                </button>
              ))}
            </div>
          </>
        )}
      </main>
    </>);
  }

  return null;
};

export default MockExam;
