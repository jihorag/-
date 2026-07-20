// 스터디 플래너 — 월간 캘린더 + '학습 태스크' 플랜.
// 계획 항목을 자유 텍스트가 아니라 앱 기능(드릴·AI학습·문제풀이·모의고사·2차논술·복습)에
// 연결된 구조화 태스크로 만든다. 탭하면 그 학습으로 바로 이동(딥링크), 회독 회차 지정 가능.
// localStorage 'quiz-planner-v1' = { 'YYYY-MM-DD': [item] }.
//   item: { id, type, subjectId?, leafId?, round?, scope?, text, done, doneAt? }
//   (레거시 { id, text, done } 은 type='custom' 으로 취급)

import { useMemo, useState } from 'react';
import { loadStudyTime, getDayStudyTime, getDaySubjects, getDaySlots, fmtDuration, fmtClock, fmtHMS } from './studyTime';
import { SUBJECTS } from './aiLearningStore';

const PLANNER_KEY = 'quiz-planner-v1';
const WD = ['일', '월', '화', '수', '목', '금', '토'];

// 학습 태스크 타입 — 앱의 각 기능에 대응
export const TASK_TYPES = {
  drill:  { icon: '⚡', label: '드릴',      color: '#7c3aed', bg: '#f5f3ff', needsSubject: true,  needsLeaf: true,  round: true },
  study:  { icon: '🎓', label: 'AI 학습',   color: '#4338ca', bg: '#eef2ff', needsSubject: true,  needsLeaf: true,  round: false },
  solve:  { icon: '📚', label: '문제풀이',   color: '#2563eb', bg: '#eff6ff', needsSubject: true,  needsLeaf: false, round: true },
  mock:   { icon: '📝', label: '모의고사',   color: '#dc2626', bg: '#fef2f2', needsSubject: false, needsLeaf: false, round: false },
  essay:  { icon: '✍️', label: '2차 논술',  color: '#059669', bg: '#ecfdf5', needsSubject: false, needsLeaf: false, round: true },
  review: { icon: '🔁', label: '복습·오답',  color: '#ea580c', bg: '#fff7ed', needsSubject: false, needsLeaf: false, round: true },
  custom: { icon: '✏️', label: '직접 입력',  color: '#6b7280', bg: '#f9fafb', needsSubject: false, needsLeaf: false, round: false },
};
const typeMeta = (t) => TASK_TYPES[t] || TASK_TYPES.custom;
// 레거시/신규 통일
const norm = (it) => (it.type ? it : { ...it, type: 'custom' });

const loadPlans = () => {
  try { return JSON.parse(localStorage.getItem(PLANNER_KEY) || '{}') || {}; }
  catch { return {}; }
};
const savePlans = (p) => {
  try { localStorage.setItem(PLANNER_KEY, JSON.stringify(p)); } catch { /* SSR */ }
};

const pad = (n) => String(n).padStart(2, '0');
const keyOf = (y, m, d) => `${y}-${pad(m + 1)}-${pad(d)}`; // m: 0-based
const dateFromKey = (k) => { const [y, m, d] = k.split('-').map(Number); return new Date(y, m - 1, d); };
const addDaysKey = (k, n) => { const d = dateFromKey(k); d.setDate(d.getDate() + n); return keyOf(d.getFullYear(), d.getMonth(), d.getDate()); };
const daysUntil = (yyyymmdd) => {
  if (!yyyymmdd) return null;
  const d = new Date(yyyymmdd + 'T00:00:00');
  if (isNaN(d.getTime())) return null;
  const t = new Date(); t.setHours(0, 0, 0, 0);
  return Math.ceil((d - t) / 86400000);
};

// 태스크 표시 라벨 자동 생성
const leafShort = (leaf) => leaf ? (leaf.path ? leaf.path[leaf.path.length - 1] : (leaf.title || '')) : '';
function buildLabel({ type, subjMeta, leaf, round, scope }) {
  const parts = [];
  if (subjMeta) parts.push(subjMeta.short);
  if (leaf) parts.push(leafShort(leaf));
  let base = parts.join(' · ') || typeMeta(type).label;
  const extras = [];
  if (scope) extras.push(scope);
  if (round) extras.push(`${round}회독`);
  return base + (extras.length ? ` · ${extras.join(' · ')}` : '');
}

export default function StudyPlanner({ examDates = {}, primaryExam = '감정평가사', leavesBySubject = {}, onOpenTask }) {
  const [plans, setPlans] = useState(loadPlans);
  const [study] = useState(loadStudyTime); // 자동 기록된 일자별 공부시간(읽기 전용)
  const now = new Date();
  const [view, setView] = useState({ y: now.getFullYear(), m: now.getMonth() }); // m: 0-based
  const todayKey = keyOf(now.getFullYear(), now.getMonth(), now.getDate());
  const [selected, setSelected] = useState(todayKey);

  // 태스크 빌더 상태
  const [bType, setBType] = useState('drill');
  const [bSubject, setBSubject] = useState('');
  const [bLeaf, setBLeaf] = useState('');
  const [bLeafQuery, setBLeafQuery] = useState(''); // 단원 검색어(수백 개 네이티브 드롭다운 대체)
  const [bRound, setBRound] = useState('');
  const [bScope, setBScope] = useState('');
  const [showCycle, setShowCycle] = useState(false);
  const [showBuilder, setShowBuilder] = useState(false); // 태스크 추가 폼 기본 접힘
  const [showRecord, setShowRecord] = useState(false);   // 자동 공부기록 기본 접힘

  const update = (next) => { setPlans(next); savePlans(next); };

  const addItemToDate = (dateKey, item) => {
    const list = plans[dateKey] || [];
    return { ...plans, [dateKey]: [...list, item] };
  };

  const addTask = () => {
    const tm = typeMeta(bType);
    if (!selected) return;
    if (tm.needsSubject && !bSubject) return;
    const subjMeta = bSubject ? SUBJECTS.find((s) => s.id === bSubject) : null;
    const leaf = bLeaf ? (leavesBySubject[bSubject] || []).find((l) => l.id === bLeaf) : null;
    if (bType === 'custom' && !bScope.trim()) return; // 직접입력은 내용 필수
    const round = tm.round && bRound ? Number(bRound) : undefined;
    const text = bType === 'custom'
      ? bScope.trim()
      : buildLabel({ type: bType, subjMeta, leaf, round, scope: bScope.trim() });
    const item = {
      id: `${selected}_${Date.now()}`,
      type: bType,
      ...(bSubject ? { subjectId: bSubject } : {}),
      ...(leaf ? { leafId: leaf.id } : {}),
      ...(round ? { round } : {}),
      ...(bScope.trim() && bType !== 'custom' ? { scope: bScope.trim() } : {}),
      text, done: false,
    };
    update(addItemToDate(selected, item));
    setBScope(''); setBLeaf(''); setBLeafQuery(''); setBRound('');
  };

  const toggleItem = (id) =>
    update({
      ...plans,
      [selected]: (plans[selected] || []).map((it) =>
        it.id === id ? { ...it, done: !it.done, doneAt: !it.done ? Date.now() : undefined } : it),
    });
  const removeItem = (id) => {
    const next = { ...plans, [selected]: (plans[selected] || []).filter((it) => it.id !== id) };
    if (next[selected].length === 0) delete next[selected];
    update(next);
  };
  const openItem = (it) => {
    const t = norm(it);
    if (t.type === 'custom') return;
    onOpenTask && onOpenTask(t);
  };

  // 🔁 회독 플랜 자동 배치 — 과목 N회독을 기간에 걸쳐 마일스톤 태스크로 펼침
  const genCycle = ({ subjectId, type, rounds, startKey, endKey, scope }) => {
    const subjMeta = SUBJECTS.find((s) => s.id === subjectId);
    if (!subjMeta || rounds < 1) return;
    const span = Math.max(1, (dateFromKey(endKey) - dateFromKey(startKey)) / 86400000);
    let next = { ...plans };
    for (let i = 1; i <= rounds; i++) {
      const offset = Math.round((span / rounds) * (i - 1));
      const dk = addDaysKey(startKey, offset);
      const text = buildLabel({ type, subjMeta, leaf: null, round: i, scope: scope || (type === 'solve' ? '기출' : '') });
      const item = { id: `${dk}_${Date.now()}_${i}`, type, subjectId, round: i, ...(scope ? { scope } : {}), text, done: false, cycle: true };
      next = { ...next, [dk]: [...(next[dk] || []), item] };
    }
    update(next);
  };

  const moveMonth = (delta) => {
    const d = new Date(view.y, view.m + delta, 1);
    setView({ y: d.getFullYear(), m: d.getMonth() });
  };
  const goToday = () => { setView({ y: now.getFullYear(), m: now.getMonth() }); setSelected(todayKey); };

  // 달력 셀(앞쪽 빈칸 포함)
  const cells = useMemo(() => {
    const first = new Date(view.y, view.m, 1).getDay();
    const total = new Date(view.y, view.m + 1, 0).getDate();
    const arr = [];
    for (let i = 0; i < first; i++) arr.push(null);
    for (let d = 1; d <= total; d++) arr.push(d);
    while (arr.length % 7 !== 0) arr.push(null);
    return arr;
  }, [view]);

  // 가장 임박한 미래 시험까지 D-day
  const dday = useMemo(() => {
    const cands = [
      { label: '1차', d: daysUntil(examDates[`${primaryExam}_1차`] || examDates[primaryExam]) },
      { label: '2차', d: daysUntil(examDates[`${primaryExam}_2차`]) },
    ].filter((x) => x.d != null && x.d >= 0).sort((a, b) => a.d - b.d)[0];
    return cands || null;
  }, [examDates, primaryExam]);

  const selList = ((selected && plans[selected]) || []).map(norm);
  const selLabel = selected ? (() => {
    const [y, m, d] = selected.split('-').map(Number);
    return `${y}년 ${m}월 ${d}일 (${WD[new Date(y, m - 1, d).getDay()]})`;
  })() : '';
  const doneCount = selList.filter((it) => it.done).length;

  const curSubjMeta = bSubject ? SUBJECTS.find((s) => s.id === bSubject) : null;
  const bTypeMeta = typeMeta(bType);
  const subjLeaves = (bSubject && leavesBySubject[bSubject]) || [];
  const selectedLeafObj = bLeaf ? subjLeaves.find((l) => l.id === bLeaf) : null;
  const leafMatches = (() => {
    const q = bLeafQuery.trim().toLowerCase();
    if (!q) return [];
    return subjLeaves.filter((l) => ((l.path ? l.path.join(' ') : '') + ' ' + (l.title || '')).toLowerCase().includes(q)).slice(0, 30);
  })();

  const inputStyle = { fontSize: '0.82rem', padding: '8px 10px', border: '1px solid #e5e7eb', borderRadius: 9, background: '#fff', color: '#374151' };

  return (
    <div className="app-container">
      <div className="screen-head" style={{ padding: '0 4px' }}>
        <h1 className="screen-title">📅 스터디 플래너</h1>
      </div>
      <main className="main-content" style={{ marginTop: '16px' }}>
        {/* 🕒 오늘 공부 시간 */}
        {(() => {
          const t = getDayStudyTime(todayKey);
          const total = t.ai + t.quiz;
          return (
            <section style={{ borderRadius: 16, padding: '18px 16px', marginBottom: 14,
              background: 'linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%)', color: '#fff',
              boxShadow: 'var(--shadow-md)' }}>
              <div style={{ fontSize: '0.8rem', opacity: 0.9, fontWeight: 600 }}>🕒 오늘 공부 시간</div>
              <div style={{ fontSize: '2.1rem', fontWeight: 800, fontVariantNumeric: 'tabular-nums', margin: '2px 0 10px' }}>
                {total > 0 ? fmtClock(total) : '0:00'}
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <div style={{ flex: 1, background: 'rgba(255,255,255,0.16)', borderRadius: 10, padding: '8px 10px' }}>
                  <div style={{ fontSize: '0.72rem', opacity: 0.9 }}>🤖 AI 학습</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 800, marginTop: 1 }}>{fmtDuration(t.ai)}</div>
                </div>
                <div style={{ flex: 1, background: 'rgba(255,255,255,0.16)', borderRadius: 10, padding: '8px 10px' }}>
                  <div style={{ fontSize: '0.72rem', opacity: 0.9 }}>📚 문제풀이</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 800, marginTop: 1 }}>{fmtDuration(t.quiz)}</div>
                </div>
              </div>
              <div style={{ fontSize: '0.66rem', opacity: 0.75, marginTop: 8, textAlign: 'center' }}>
                AI 학습·문제풀이 화면에 머무는 시간이 자동 기록돼요
              </div>
            </section>
          );
        })()}

        {/* 캘린더 */}
        <section style={{ background: '#fff', borderRadius: 16, padding: 16, boxShadow: 'var(--shadow-md)', marginBottom: 14 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
            <button onClick={() => moveMonth(-1)} aria-label="이전 달"
              style={{ width: 34, height: 34, borderRadius: 8, border: '1px solid #e5e7eb', background: '#fff', cursor: 'pointer', fontSize: '1rem', color: '#374151' }}>‹</button>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
              <span style={{ fontWeight: 800, fontSize: '1.05rem', color: '#111827' }}>{view.y}년 {view.m + 1}월</span>
              <button onClick={goToday}
                style={{ fontSize: '0.72rem', color: '#4f46e5', fontWeight: 700, background: '#eef2ff', border: 'none', borderRadius: 999, padding: '3px 9px', cursor: 'pointer' }}>오늘</button>
            </div>
            <button onClick={() => moveMonth(1)} aria-label="다음 달"
              style={{ width: 34, height: 34, borderRadius: 8, border: '1px solid #e5e7eb', background: '#fff', cursor: 'pointer', fontSize: '1rem', color: '#374151' }}>›</button>
          </div>
          {dday && (
            <div style={{ textAlign: 'center', fontSize: '0.76rem', color: '#6b7280', marginBottom: 12 }}>
              {primaryExam} {dday.label}까지 <b style={{ color: dday.d <= 30 ? '#dc2626' : dday.d <= 90 ? '#ea580c' : '#1d4ed8' }}>D-{dday.d}</b>
            </div>
          )}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7,1fr)', marginBottom: 4 }}>
            {WD.map((w, i) => (
              <div key={w} style={{ textAlign: 'center', fontSize: '0.7rem', fontWeight: 700, color: i === 0 ? '#dc2626' : i === 6 ? '#2563eb' : '#9ca3af' }}>{w}</div>
            ))}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7,1fr)', gap: 4 }}>
            {cells.map((d, i) => {
              if (d == null) return <div key={`e${i}`} />;
              const k = keyOf(view.y, view.m, d);
              const isToday = k === todayKey;
              const isSel = k === selected;
              const list = (plans[k] || []).map(norm);
              const dow = i % 7;
              const st = study[k];
              const sMin = st ? Math.round(((st.ai || 0) + (st.quiz || 0)) / 60) : 0;
              return (
                <button key={k} onClick={() => setSelected(k)}
                  style={{ aspectRatio: '1 / 1', borderRadius: 10, cursor: 'pointer', position: 'relative',
                    border: isSel ? '2px solid #4f46e5' : '1px solid #f1f5f9',
                    background: isToday ? '#eef2ff' : '#fff', padding: 2,
                    display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start' }}>
                  {list.length > 0 && (
                    <span style={{ position: 'absolute', top: 4, right: 4, width: 5, height: 5, borderRadius: '50%',
                      background: list.every((it) => it.done) ? '#16a34a' : '#f59e0b' }} />
                  )}
                  <span style={{ fontSize: '0.8rem', fontWeight: isToday ? 800 : 600, marginTop: 2,
                    color: isToday ? '#4f46e5' : dow === 0 ? '#dc2626' : dow === 6 ? '#2563eb' : '#374151' }}>{d}</span>
                  {sMin > 0 && (
                    <span style={{ marginTop: 'auto', marginBottom: 3, fontSize: '0.54rem', fontWeight: 800, color: '#4f46e5' }}>
                      {sMin >= 60 ? `${(sMin / 60).toFixed(1)}h` : `${sMin}분`}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </section>

        {/* 선택 날짜 */}
        <section style={{ background: '#fff', borderRadius: 16, padding: 16, boxShadow: 'var(--shadow-md)' }}>
          <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 12 }}>
            <div style={{ fontWeight: 800, fontSize: '0.92rem', color: '#111827' }}>🗓 {selLabel || '날짜를 선택하세요'}</div>
            {selList.length > 0 && (
              <span style={{ fontSize: '0.74rem', color: doneCount === selList.length ? '#16a34a' : '#6b7280', fontWeight: 700 }}>
                {doneCount}/{selList.length} 완료
              </span>
            )}
          </div>

          {/* 자동 기록 — 과목별 시간 + 시간대 그리드 */}
          {selected && (() => {
            const t = getDayStudyTime(selected);
            const total = t.ai + t.quiz;
            const subs = getDaySubjects(selected);
            const slots = getDaySlots(selected);
            const cellBg = (idx) => {
              const sl = slots[idx];
              const ai = sl?.ai || 0, quiz = sl?.quiz || 0;
              const secs = ai + quiz;
              if (secs === 0) return '#f1f5f9';
              const op = 0.3 + 0.7 * Math.min(1, secs / 600);
              return ai >= quiz ? `rgba(79,70,229,${op})` : `rgba(22,163,74,${op})`;
            };
            const renderSubject = (s) => {
              const d = subs[s.id];
              const secs = d?.secs || 0;
              const units = d?.units ? Object.entries(d.units).sort((a, b) => b[1] - a[1]) : [];
              return (
                <div key={s.id} style={{ marginBottom: 12 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
                    <span style={{ fontSize: '0.78rem', flexShrink: 0 }}>{s.icon}</span>
                    <span style={{ flex: 1, fontSize: '0.8rem', fontWeight: 700, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', color: secs > 0 ? '#111827' : '#9ca3af' }}>{s.short}</span>
                    <span style={{ fontSize: '0.74rem', fontWeight: 800, fontVariantNumeric: 'tabular-nums', flexShrink: 0, color: secs > 0 ? '#4f46e5' : '#cbd5e1' }}>{fmtHMS(secs)}</span>
                  </div>
                  {units.map(([label, sec], i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 5, paddingLeft: 21, marginTop: 5 }}>
                      <span style={{ flex: 1, fontSize: '0.7rem', color: '#6b7280', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>· {label}</span>
                      <span style={{ fontSize: '0.66rem', color: '#9ca3af', fontVariantNumeric: 'tabular-nums', flexShrink: 0 }}>{fmtDuration(sec)}</span>
                    </div>
                  ))}
                </div>
              );
            };
            const stage1 = SUBJECTS.filter((s) => s.stage === 1);
            const stage2 = SUBJECTS.filter((s) => s.stage === 2);
            if (total === 0) return null;
            return (
              <div style={{ marginBottom: 12 }}>
                <button onClick={() => setShowRecord((v) => !v)}
                  style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    background: '#f8fafc', border: '1px solid #eef0f2', borderRadius: 10, padding: '8px 12px',
                    cursor: 'pointer', fontSize: '0.76rem', fontWeight: 700, color: '#475569' }}>
                  <span>⏱ 이 날 공부 기록 · {fmtClock(total)} <span style={{ color: '#9ca3af', fontWeight: 600 }}>(🤖 {fmtDuration(t.ai)} · 📚 {fmtDuration(t.quiz)})</span></span>
                  <span style={{ color: '#9ca3af' }}>{showRecord ? '▲' : '▼'}</span>
                </button>
                {showRecord && (
                <div style={{ marginTop: 10 }}>
                <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                  <div style={{ flex: '1 1 0', minWidth: 0 }}>
                    <div style={{ fontSize: '0.66rem', color: '#9ca3af', fontWeight: 800, marginBottom: 5 }}>1차</div>
                    {stage1.map(renderSubject)}
                    <div style={{ fontSize: '0.66rem', color: '#9ca3af', fontWeight: 800, margin: '9px 0 5px' }}>2차</div>
                    {stage2.map(renderSubject)}
                  </div>
                  <div style={{ flex: '0 0 128px' }}>
                    <div style={{ fontSize: '0.66rem', color: '#9ca3af', fontWeight: 800, marginBottom: 5 }}>시간대</div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                      {Array.from({ length: 24 }, (_, h) => (
                        <div key={h} style={{ display: 'flex', alignItems: 'center', gap: 3 }}>
                          <span style={{ width: 13, fontSize: '0.5rem', color: '#cbd5e1', textAlign: 'right', flexShrink: 0, fontVariantNumeric: 'tabular-nums' }}>{h}</span>
                          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6,1fr)', gap: 1, flex: 1 }}>
                            {Array.from({ length: 6 }, (_, sg) => {
                              const idx = h * 6 + sg;
                              return <div key={sg} title={`${h}:${String(sg * 10).padStart(2, '0')}`} style={{ height: 7, borderRadius: 1, background: cellBg(idx) }} />;
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                    <div style={{ display: 'flex', gap: 8, marginTop: 7, fontSize: '0.58rem', color: '#9ca3af', flexWrap: 'wrap' }}>
                      <span><span style={{ color: '#4f46e5', fontWeight: 800 }}>■</span> AI</span>
                      <span><span style={{ color: '#16a34a', fontWeight: 800 }}>■</span> 문제풀이</span>
                    </div>
                  </div>
                </div>
                </div>
                )}
              </div>
            );
          })()}

          {/* 학습 태스크 목록 */}
          {selList.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 14 }}>
              {selList.map((it) => {
                const tm = typeMeta(it.type);
                const openable = it.type !== 'custom' && onOpenTask;
                return (
                  <div key={it.id} style={{ display: 'flex', alignItems: 'center', gap: 8,
                    background: it.done ? '#f0fdf4' : '#fff', border: `1px solid ${it.done ? '#bbf7d0' : '#eef0f2'}`,
                    borderRadius: 10, padding: '8px 10px' }}>
                    <button onClick={() => toggleItem(it.id)} aria-label="완료 토글"
                      style={{ width: 22, height: 22, borderRadius: '50%', flexShrink: 0, cursor: 'pointer',
                        border: `2px solid ${it.done ? '#16a34a' : '#cbd5e1'}`, background: it.done ? '#16a34a' : '#fff',
                        color: '#fff', fontSize: '0.7rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      {it.done ? '✓' : ''}
                    </button>
                    {/* 타입 배지 */}
                    <span style={{ flexShrink: 0, fontSize: '0.66rem', fontWeight: 800, color: tm.color, background: tm.bg,
                      borderRadius: 7, padding: '3px 7px', display: 'inline-flex', alignItems: 'center', gap: 3 }}>
                      {tm.icon}{tm.label}
                    </span>
                    {/* 본문 — 열 수 있으면 클릭 시 이동 */}
                    <button onClick={() => openable && openItem(it)} disabled={!openable}
                      style={{ flex: 1, minWidth: 0, textAlign: 'left', background: 'none', border: 'none',
                        cursor: openable ? 'pointer' : 'default', padding: 0,
                        fontSize: '0.85rem', color: it.done ? '#9ca3af' : '#374151',
                        textDecoration: it.done ? 'line-through' : 'none',
                        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {it.text}{openable && <span style={{ color: tm.color, fontWeight: 700 }}> ›</span>}
                    </button>
                    <button onClick={() => removeItem(it.id)}
                      style={{ flexShrink: 0, fontSize: '0.72rem', color: '#c1c7cf', background: 'none', border: 'none', cursor: 'pointer' }}>✕</button>
                  </div>
                );
              })}
            </div>
          ) : null}

          {/* 태스크 빌더 — 기본 접힘: '+ 오늘 학습 추가'로 열기 */}
          {!showBuilder ? (
            <button onClick={() => setShowBuilder(true)}
              style={{ width: '100%', padding: '12px', borderRadius: 12, border: '1px dashed #c7d2fe',
                background: '#f5f6ff', color: '#4f46e5', fontWeight: 800, fontSize: '0.88rem', cursor: 'pointer' }}>
              + 오늘 학습 추가
            </button>
          ) : (
          <div style={{ background: '#f8fafc', borderRadius: 12, padding: 12, border: '1px solid #eef0f2' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8 }}>
              <div style={{ fontSize: '0.74rem', fontWeight: 800, color: '#475569' }}>학습 태스크 추가</div>
              <button onClick={() => setShowBuilder(false)}
                style={{ fontSize: '0.72rem', color: '#9ca3af', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 700 }}>닫기 ✕</button>
            </div>
            {/* 타입 칩 */}
            <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap', marginBottom: 9 }}>
              {Object.entries(TASK_TYPES).map(([k, tm]) => {
                const on = bType === k;
                return (
                  <button key={k} onClick={() => { setBType(k); setBLeaf(''); setBLeafQuery(''); if (!TASK_TYPES[k].needsSubject) { setBSubject(''); } }}
                    style={{ fontSize: '0.74rem', fontWeight: 700, borderRadius: 999, padding: '5px 10px', cursor: 'pointer',
                      border: on ? `1.5px solid ${tm.color}` : '1px solid #e5e7eb',
                      background: on ? tm.bg : '#fff', color: on ? tm.color : '#6b7280' }}>
                    {tm.icon} {tm.label}
                  </button>
                );
              })}
            </div>
            {/* 과목 / 단원 / 회독 / 범위 */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 8 }}>
              {bTypeMeta.needsSubject && (
                <select value={bSubject} onChange={(e) => { setBSubject(e.target.value); setBLeaf(''); setBLeafQuery(''); }} style={{ ...inputStyle, flex: '1 1 120px' }}>
                  <option value="">과목 선택…</option>
                  <optgroup label="1차">
                    {SUBJECTS.filter((s) => s.stage === 1).map((s) => <option key={s.id} value={s.id}>{s.icon} {s.short}</option>)}
                  </optgroup>
                  <optgroup label="2차">
                    {SUBJECTS.filter((s) => s.stage === 2).map((s) => <option key={s.id} value={s.id}>{s.icon} {s.short}</option>)}
                  </optgroup>
                </select>
              )}
              {/* 단원: 검색형(수백 개라 네이티브 드롭다운은 스크롤이 끝없이 길어짐) */}
              {bTypeMeta.needsLeaf && bSubject && subjLeaves.length > 0 && (
                <div style={{ flex: '1 1 100%' }}>
                  {selectedLeafObj ? (
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, background: '#eef2ff', border: '1px solid #c7d2fe', borderRadius: 9, padding: '7px 10px' }}>
                      <span style={{ flex: 1, minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontSize: '0.82rem', color: '#4338ca', fontWeight: 700 }}>📍 {leafShort(selectedLeafObj)}</span>
                      <button onClick={() => { setBLeaf(''); setBLeafQuery(''); }} style={{ flexShrink: 0, background: 'none', border: 'none', color: '#6366f1', cursor: 'pointer', fontSize: '0.74rem', fontWeight: 700 }}>✕ 전체</button>
                    </div>
                  ) : (
                    <>
                      <input type="text" value={bLeafQuery} onChange={(e) => setBLeafQuery(e.target.value)}
                        placeholder="단원 검색 (미선택 시 전체)" style={{ ...inputStyle, width: '100%', boxSizing: 'border-box' }} />
                      {bLeafQuery.trim() && (
                        <div style={{ marginTop: 4, maxHeight: 168, overflowY: 'auto', border: '1px solid #e5e7eb', borderRadius: 9, background: '#fff' }}>
                          {leafMatches.length ? leafMatches.map((l) => (
                            <button key={l.id} onClick={() => { setBLeaf(l.id); setBLeafQuery(''); }}
                              style={{ display: 'flex', alignItems: 'baseline', gap: 6, width: '100%', textAlign: 'left', padding: '7px 10px',
                                background: 'none', border: 'none', borderBottom: '1px solid #f1f5f9', cursor: 'pointer' }}>
                              <span style={{ fontSize: '0.8rem', color: '#374151', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{leafShort(l)}</span>
                              {l.path && l.path.length > 1 && <span style={{ flexShrink: 0, marginLeft: 'auto', fontSize: '0.68rem', color: '#9ca3af' }}>{l.path[l.path.length - 2]}</span>}
                            </button>
                          )) : <div style={{ padding: '8px 10px', fontSize: '0.78rem', color: '#9ca3af' }}>일치하는 단원 없음</div>}
                        </div>
                      )}
                    </>
                  )}
                </div>
              )}
              {bTypeMeta.round && (
                <select value={bRound} onChange={(e) => setBRound(e.target.value)} style={{ ...inputStyle, flex: '0 0 92px' }}>
                  <option value="">회독 없음</option>
                  {[1, 2, 3, 4, 5, 6, 7].map((n) => <option key={n} value={n}>{n}회독</option>)}
                </select>
              )}
            </div>
            <div style={{ display: 'flex', gap: 6 }}>
              <input type="text" value={bScope}
                placeholder={bType === 'custom' ? '할 일 입력' : '범위·메모(선택) 예: 기출 40문제'}
                onChange={(e) => setBScope(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') addTask(); }}
                style={{ ...inputStyle, flex: 1 }} />
              <button onClick={addTask}
                disabled={!selected || (bTypeMeta.needsSubject && !bSubject) || (bType === 'custom' && !bScope.trim())}
                style={{ fontSize: '0.82rem', fontWeight: 800, color: '#fff', borderRadius: 9, padding: '8px 16px', border: 'none',
                  cursor: 'pointer', background: (bTypeMeta.needsSubject && !bSubject) || (bType === 'custom' && !bScope.trim()) ? '#c7d2fe' : '#4f46e5' }}>
                추가
              </button>
            </div>

            {/* 🔁 회독 플랜 자동 배치 */}
            <button onClick={() => setShowCycle((v) => !v)}
              style={{ marginTop: 10, fontSize: '0.76rem', fontWeight: 700, color: '#ea580c', background: '#fff7ed',
                border: '1px solid #fed7aa', borderRadius: 9, padding: '7px 12px', cursor: 'pointer', width: '100%' }}>
              🔁 회독 플랜 자동 배치 {showCycle ? '▲' : '▼'}
            </button>
            {showCycle && <CyclePlanner subjects={SUBJECTS} startKey={selected} examDates={examDates} primaryExam={primaryExam} onGenerate={genCycle} />}
          </div>
          )}
        </section>
      </main>
    </div>
  );
}

// 회독 플랜 자동 배치 폼
function CyclePlanner({ subjects, startKey, examDates, primaryExam, onGenerate }) {
  const [subjectId, setSubjectId] = useState('');
  const [type, setType] = useState('solve');
  const [rounds, setRounds] = useState(3);
  const [scope, setScope] = useState('기출');
  const examKey = examDates[`${primaryExam}_1차`] || examDates[primaryExam] || '';
  const defaultEnd = examKey || (() => { const d = new Date(startKey + 'T00:00:00'); d.setDate(d.getDate() + rounds * 14); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; })();
  const [endKey, setEndKey] = useState(defaultEnd);
  const inputStyle = { fontSize: '0.82rem', padding: '8px 10px', border: '1px solid #e5e7eb', borderRadius: 9, background: '#fff', color: '#374151' };
  return (
    <div style={{ marginTop: 8, padding: 10, background: '#fff', border: '1px solid #fed7aa', borderRadius: 10 }}>
      <div style={{ fontSize: '0.72rem', color: '#9a3412', marginBottom: 8, lineHeight: 1.5 }}>
        한 과목을 <b>N회독</b>으로 나눠, 시작일부터 종료일(기본 시험일)까지 캘린더에 회독 마일스톤을 자동 배치합니다.
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 8 }}>
        <select value={subjectId} onChange={(e) => setSubjectId(e.target.value)} style={{ ...inputStyle, flex: '1 1 120px' }}>
          <option value="">과목 선택…</option>
          {subjects.map((s) => <option key={s.id} value={s.id}>{s.icon} {s.short}</option>)}
        </select>
        <select value={type} onChange={(e) => setType(e.target.value)} style={{ ...inputStyle, flex: '0 0 108px' }}>
          <option value="solve">📚 문제풀이</option>
          <option value="drill">⚡ 드릴</option>
        </select>
        <select value={rounds} onChange={(e) => setRounds(Number(e.target.value))} style={{ ...inputStyle, flex: '0 0 92px' }}>
          {[2, 3, 4, 5, 6].map((n) => <option key={n} value={n}>{n}회독</option>)}
        </select>
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 8, alignItems: 'center' }}>
        <span style={{ fontSize: '0.72rem', color: '#6b7280' }}>{startKey} →</span>
        <input type="date" value={endKey} onChange={(e) => setEndKey(e.target.value)} style={{ ...inputStyle, flex: '0 0 auto' }} />
        <input type="text" value={scope} placeholder="범위(예: 기출)" onChange={(e) => setScope(e.target.value)} style={{ ...inputStyle, flex: '1 1 80px' }} />
      </div>
      <button onClick={() => { if (subjectId && endKey) { onGenerate({ subjectId, type, rounds, startKey, endKey, scope }); setSubjectId(''); } }}
        disabled={!subjectId || !endKey}
        style={{ fontSize: '0.8rem', fontWeight: 800, color: '#fff', borderRadius: 9, padding: '8px 0', border: 'none', width: '100%',
          cursor: subjectId && endKey ? 'pointer' : 'default', background: subjectId && endKey ? '#ea580c' : '#fdba74' }}>
        회독 플랜 배치
      </button>
    </div>
  );
}
