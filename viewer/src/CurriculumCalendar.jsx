// 월별·일별 학습 달력 — '순차 완성' 스케줄(schedule)을 expandDay로 날짜별로 펼쳐 보여준다.
// 오늘의 계획과 같은 스케줄을 읽으므로 날짜별 계획이 정확히 호응한다.
// 날짜 칸에는 아이콘이 아니라 '과목 이름을 색깔로 한 줄씩' 쌓아 그날 할 공부를 적는다.

import { useMemo, useState } from 'react';
import { SUBJECTS } from './aiLearningStore';
import { UNIT_POOLS } from './curriculumPlan';
import { expandDay, SUBJECT_COLORS } from './curriculumAi';

const POOL = (sid) => UNIT_POOLS[sid] || [];

const S1 = ['civil', 'economics', 'accounting', 'realestate', 'law'];
const S2 = ['appraisal_theory', 'appraisal_practice', 'appraisal_law'];
const ALLSUBJ = [...S1, ...S2];
const SMAP = Object.fromEntries(SUBJECTS.map((s) => [s.id, s]));
const CAL_SHORT = {
  civil: '민법', economics: '경제', accounting: '회계', realestate: '부동산', law: '법규',
  appraisal_theory: '이론', appraisal_practice: '실무', appraisal_law: '2차법규',
};
const WD = ['일', '월', '화', '수', '목', '금', '토'];
const DAY = 86400000;
const ACCENT = '#4361ee';
const midnight = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
const card = { background: '#fff', border: '1px solid #eceff3', borderRadius: 16, boxShadow: 'var(--shadow-md)', marginBottom: 14, padding: 15 };
const navBtn = { width: 30, height: 30, borderRadius: 8, border: '1px solid #e5e7eb', background: '#fff', cursor: 'pointer', fontSize: '1rem', color: '#475569' };
const scol = (sid) => SUBJECT_COLORS[sid] || '#475569';
const sname = (sid) => CAL_SHORT[sid] || SMAP[sid]?.short || sid;
// 누적 파이프라인 활동 → 아이콘 + 이동할 앱 기능
const ACT_ICON = { '학습': '📘', '문제풀이': '✏️', '드릴': '⚡' };
const ACT_TYPE = { '학습': 'study', '문제풀이': 'solve', '드릴': 'drill' };

export default function CurriculumCalendar({ exam1 = '', exam2 = '', onOpenTask, schedule = null, rounds = 3, onRoundsChange, insights = null }) {
  const now = new Date();
  const today0 = midnight(now);
  const ed = exam1 ? new Date(exam1 + 'T00:00:00') : null;
  const hasExam = ed && !isNaN(ed.getTime());
  const ed2 = exam2 ? new Date(exam2 + 'T00:00:00') : null;
  const hasExam2 = ed2 && !isNaN(ed2.getTime());

  const [view, setView] = useState({ y: now.getFullYear(), m: now.getMonth() });
  const [sel, setSel] = useState(today0);

  const dayPlan = (dateObj) => expandDay(dateObj, schedule);
  // 계획 단원 풀 — 스케줄에 저장된 장(章) 풀(항목 { name, hier }) 우선, 없으면 기본 8단원 풀.
  const poolOf = (sid) => (schedule && schedule.pools && schedule.pools[sid]) || POOL(sid);
  const eName = (e) => (typeof e === 'string' ? e : (e && e.name) || '');
  const eHier = (e) => (typeof e === 'string' ? null : (e && e.hier) || null);

  const cells = useMemo(() => {
    const first = new Date(view.y, view.m, 1).getDay();
    const total = new Date(view.y, view.m + 1, 0).getDate();
    const arr = [];
    for (let i = 0; i < first; i++) arr.push(null);
    for (let d = 1; d <= total; d++) arr.push(d);
    while (arr.length % 7) arr.push(null);
    return arr;
  }, [view]);

  // 이 달 과목별 단원 범위 + 볼륨 (스케줄을 날마다 펼쳐 집계)
  const monthTargets = useMemo(() => {
    const res = {};
    ALLSUBJ.forEach((sid) => { res[sid] = { min: Infinity, max: -1, minR: Infinity, maxR: -1, vol: 0 }; });
    const totalDays = new Date(view.y, view.m + 1, 0).getDate();
    for (let d = 1; d <= totalDays; d++) {
      const dp = expandDay(new Date(view.y, view.m, d), schedule);
      if (!dp) continue;
      dp.subs.forEach((s) => {
        const r = res[s.sid]; if (!r) return;
        r.min = Math.min(r.min, s.idx); r.max = Math.max(r.max, s.idx);
        r.minR = Math.min(r.minR, s.round); r.maxR = Math.max(r.maxR, s.round);
        r.vol += Math.round(dp.vol / dp.subs.length);
      });
    }
    return res;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [view, schedule]);

  const moveMonth = (delta) => { const dt = new Date(view.y, view.m + delta, 1); setView({ y: dt.getFullYear(), m: dt.getMonth() }); };
  const goToday = () => { setView({ y: now.getFullYear(), m: now.getMonth() }); setSel(today0); };

  if (!schedule) {
    return <section style={card}><div style={{ fontSize: '0.78rem', color: '#94a3b8', textAlign: 'center', padding: 12, lineHeight: 1.6 }}>📅 오늘의 계획에서 🤖 버튼으로<br />학습 계획을 생성하면 달력이 채워집니다</div></section>;
  }

  const selPlan = dayPlan(sel);

  return (
    <section style={card}>
      {/* 월 네비 */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
        <button onClick={() => moveMonth(-1)} style={navBtn} aria-label="이전 달">‹</button>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
          <span style={{ fontWeight: 800, fontSize: '1rem', color: '#1e293b' }}>{view.y}년 {view.m + 1}월</span>
          <button onClick={goToday} style={{ fontSize: '0.64rem', color: '#334155', fontWeight: 800, background: '#eef1fe', border: 'none', borderRadius: 999, padding: '2px 8px', cursor: 'pointer' }}>오늘</button>
        </div>
        <button onClick={() => moveMonth(1)} style={navBtn} aria-label="다음 달">›</button>
      </div>

      {/* 🔄 최소 목표 회독 — 계획이 이 값에 따라 바뀜(한 과목당 회독수) */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#475569' }}>🔄 과목당 목표 회독</span>
        <div style={{ display: 'flex', gap: 4 }}>
          {[2, 3, 4, 5, 6, 7].map((v) => {
            const on = rounds === v;
            return (
              <button key={v} onClick={() => onRoundsChange && onRoundsChange(v)} style={{ fontSize: '0.72rem', fontWeight: 800, borderRadius: 7, padding: '4px 9px', cursor: 'pointer', border: on ? `1.5px solid ${ACCENT}` : '1px solid #e5e7eb', background: on ? '#eef1fe' : '#fff', color: on ? '#334155' : '#94a3b8' }}>{v}</button>
            );
          })}
        </div>
        <span style={{ fontSize: '0.64rem', color: '#94a3b8', flexBasis: '100%' }}>한 과목을 이 회독수만큼 끝낸 뒤 다음 과목으로 넘어가도록 일정이 배분됩니다</span>
      </div>

      {/* 이 달 목표 — 과목별 단원 범위(과목명 색깔) */}
      <div style={{ background: '#f8fafc', border: '1px solid #eef0f2', borderRadius: 10, padding: '9px 11px', marginBottom: 12, display: 'flex', flexDirection: 'column', gap: 5 }}>
        <div style={{ fontSize: '0.64rem', fontWeight: 800, color: '#94a3b8', marginBottom: 1 }}>이 달의 목표</div>
        {ALLSUBJ.map((sid) => {
          const t = monthTargets[sid];
          if (!t || t.max < 0) return null;
          const pool = poolOf(sid);
          const from = eName(pool[t.min]), to = eName(pool[t.max]);
          const fromH = eHier(pool[t.min]), toH = eHier(pool[t.max]);
          const rangeH = fromH ? (toH && toH !== fromH ? `${fromH}~${toH}` : fromH) : null;
          const phase = t.maxR === 1 ? '학습' : t.minR >= 2 ? '복습' : '학습·복습';
          const rNum = t.minR === t.maxR ? `${t.minR}` : `${t.minR}~${t.maxR}`;
          return (
            <div key={sid} style={{ display: 'flex', alignItems: 'center', gap: 7, fontSize: '0.72rem' }}>
              <span style={{ fontSize: '0.58rem', fontWeight: 800, flexShrink: 0, color: '#94a3b8' }}>{S2.includes(sid) ? '2차' : '1차'}</span>
              <span style={{ fontWeight: 800, fontSize: '0.72rem', color: scol(sid), background: scol(sid) + '1f', borderRadius: 6, padding: '2px 8px', flexShrink: 0 }}>{sname(sid)}</span>
              {rangeH ? <span style={{ fontWeight: 800, fontSize: '0.58rem', color: '#fff', background: '#4361ee', borderRadius: 5, padding: '2px 6px', flexShrink: 0, whiteSpace: 'nowrap' }}>{rangeH}</span> : null}
              <span style={{ color: '#475569', flex: 1, minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{from === to ? from : `${from} ~ ${to}`}</span>
              <span style={{ fontWeight: 800, flexShrink: 0, color: '#334155' }}>{phase} {rNum}회</span>
              <span style={{ color: '#94a3b8', flexShrink: 0, fontVariantNumeric: 'tabular-nums' }}>~{t.vol}문항</span>
            </div>
          );
        })}
        {ALLSUBJ.every((sid) => !monthTargets[sid] || monthTargets[sid].max < 0) && <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>이 달은 학습 기간이 아니에요</div>}
      </div>

      {/* 요일 헤더 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7,1fr)', marginBottom: 4 }}>
        {WD.map((w) => <div key={w} style={{ textAlign: 'center', fontSize: '0.64rem', fontWeight: 700, color: '#94a3b8' }}>{w}</div>)}
      </div>
      {/* 달력 그리드 — 칸마다 과목명을 색깔로 한 줄씩 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7,1fr)', gap: 3 }}>
        {cells.map((d, i) => {
          if (d == null) return <div key={'e' + i} />;
          const dt = new Date(view.y, view.m, d);
          const dp = dayPlan(dt);
          const isToday = dt.getTime() === today0.getTime();
          const isSel = dt.getTime() === sel.getTime();
          const isExam = hasExam && ed.getFullYear() === dt.getFullYear() && ed.getMonth() === dt.getMonth() && ed.getDate() === dt.getDate();
          const isExam2 = hasExam2 && ed2.getFullYear() === dt.getFullYear() && ed2.getMonth() === dt.getMonth() && ed2.getDate() === dt.getDate();
          const past = dt < today0;
          return (
            <button key={d} onClick={() => setSel(dt)} style={{
              minHeight: 58, borderRadius: 8, cursor: 'pointer', overflow: 'hidden',
              border: isSel ? `2px solid ${ACCENT}` : '1px solid #f1f5f9',
              background: (isExam || isExam2) ? '#fef2f2' : isToday ? '#eef1fe' : '#fff',
              opacity: past ? 0.5 : 1, padding: '3px 2px',
              display: 'flex', flexDirection: 'column', alignItems: 'stretch', justifyContent: 'flex-start', gap: 1,
            }}>
              <span style={{ fontSize: '0.58rem', fontWeight: isToday ? 800 : 600, color: (isExam || isExam2) ? '#334155' : '#475569', lineHeight: 1.1, textAlign: 'center' }}>{d}{isExam ? '🎯' : ''}{isExam2 ? '🏁' : ''}</span>
              {dp && !past && [...new Set(dp.subs.map((s) => s.sid))].map((sid) => (
                <span key={sid} style={{ fontSize: '0.5rem', fontWeight: 800, lineHeight: 1.25, color: scol(sid), background: scol(sid) + '1f', borderRadius: 5, padding: '1px 3px', textAlign: 'center', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{sname(sid)}</span>
              ))}
            </button>
          );
        })}
      </div>

      {/* 선택 날짜 상세 — 과목명 색깔 + 오늘 범위(단원, 강조) + 학습/복습 */}
      {selPlan ? (
        <div style={{ marginTop: 12, borderTop: '1px solid #f1f5f9', paddingTop: 11 }}>
          <div style={{ fontWeight: 800, fontSize: '0.78rem', color: '#1e293b', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
            <span>{sel.getMonth() + 1}월 {sel.getDate()}일 계획</span>
            <span style={{ marginLeft: 'auto', color: '#94a3b8', fontWeight: 700, fontSize: '0.72rem' }}>약 {selPlan.vol}문항</span>
          </div>
          {selPlan.subs.map((s, i) => {
            const activity = s.activity || s.kind || (s.round === 1 ? '학습' : '복습');
            const goType = ACT_TYPE[activity] || (s.round === 1 ? 'study' : 'review');
            return (
              <button key={i} onClick={() => onOpenTask && onOpenTask({ type: goType, subjectId: s.sid })}
                style={{ display: 'flex', alignItems: 'center', gap: 7, width: '100%', textAlign: 'left', background: '#fff', border: '1px solid #eef0f2', borderRadius: 9, padding: '8px 10px', marginBottom: 5, cursor: 'pointer' }}>
                <span style={{ fontSize: '0.58rem', fontWeight: 800, flexShrink: 0, color: '#94a3b8' }}>{s.stage === 2 ? '2차' : '1차'}</span>
                {(s.hier || s.total != null) ? <span title={`이 과목 ${s.total}단원 중 ${s.idx + 1}번째`} style={{ fontSize: '0.58rem', fontWeight: 800, color: '#fff', background: '#4361ee', borderRadius: 5, padding: '2px 5px', flexShrink: 0, whiteSpace: 'nowrap' }}>{s.hier || `${s.idx + 1}단원`}</span> : null}
                <span style={{ fontWeight: 800, fontSize: '0.72rem', color: scol(s.sid), background: scol(s.sid) + '1f', borderRadius: 6, padding: '3px 8px', flexShrink: 0 }}>{sname(s.sid)}</span>
                <span style={{ flex: 1, minWidth: 0, fontSize: '0.78rem', fontWeight: 700, color: '#1e293b', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{s.unit}{s.parallel ? ' · 병행' : ''}</span>
                <span style={{ fontSize: '0.58rem', fontWeight: 800, flexShrink: 0, borderRadius: 6, padding: '2px 6px', background: '#f1f5f9', color: '#475569', whiteSpace: 'nowrap' }}>{ACT_ICON[activity] || ''} {activity}</span>
              </button>
            );
          })}
        </div>
      ) : (
        <div style={{ marginTop: 12, borderTop: '1px solid #f1f5f9', paddingTop: 11, fontSize: '0.72rem', color: '#94a3b8', textAlign: 'center' }}>
          {hasExam2 && sel > ed2 ? '2차 시험 이후예요' : '학습 계획 기간이 아니에요'}
        </div>
      )}
    </section>
  );
}
