// D-day 시험 플래너 — Phase β.
// 시험일 입력 → D-day 카운트, 일별 권장 학습량(미숙 단원 수 / 남은 일수)
// + 약점 단원 우선 배치.

import { useState, useMemo } from 'react';
import { getExamPlan, setExamPlan, daysUntilExam, getMastery } from './aiLearningStore';

function countNotStarted(masteryDict, leaves) {
  return (leaves || []).filter((l) => {
    const m = masteryDict[l.id];
    return !m || m.status === 'not_started';
  }).length;
}

function countInProgress(masteryDict, leaves) {
  return (leaves || []).filter((l) => {
    const m = masteryDict[l.id];
    return m && m.status === 'in_progress';
  }).length;
}

export default function DDayPlanner({ leavesBySubject }) {
  const [plan, setPlanState] = useState(() => getExamPlan());
  const dDay = daysUntilExam();

  const summary = useMemo(() => {
    const mastery = getMastery();
    const all = Object.values(leavesBySubject || {}).flat();
    const total = all.length;
    const notStarted = countNotStarted(mastery, all);
    const inProgress = countInProgress(mastery, all);
    const mastered = all.length - notStarted - inProgress;
    return { total, notStarted, inProgress, mastered };
  }, [leavesBySubject]);

  const handleDateChange = (e) => {
    const next = { ...plan, exam_date: e.target.value };
    setPlanState(next);
    setExamPlan(next);
  };

  const recommendedPerDay = useMemo(() => {
    if (!dDay || dDay <= 0) return 0;
    // 미숙 + 미진행 분량을 남은 일수로 분배
    const todo = summary.notStarted + summary.inProgress * 0.5;
    return Math.ceil(todo / dDay);
  }, [dDay, summary]);

  const progressPct = summary.total > 0 ? Math.round((summary.mastered / summary.total) * 100) : 0;

  return (
    <div style={{ padding: 14, background: '#fff', borderRadius: 10, border: '1px solid #e5e7eb' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 10 }}>
        <h3 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 800, color: '#111827' }}>
          📅 D-day 학습 플래너
        </h3>
        {dDay != null && (
          <span style={{
            padding: '3px 12px', borderRadius: 999,
            background: dDay < 30 ? '#fee2e2' : dDay < 90 ? '#fef3c7' : '#dbeafe',
            color: dDay < 30 ? '#991b1b' : dDay < 90 ? '#92400e' : '#1e40af',
            fontSize: '0.85rem', fontWeight: 800,
          }}>
            D{dDay >= 0 ? '-' : '+'}{Math.abs(dDay)}
          </span>
        )}
      </div>
      <label style={{ display: 'block', fontSize: '0.78rem', color: '#6b7280', marginBottom: 4 }}>
        시험 예정일
      </label>
      <input
        type="date"
        value={plan.exam_date || ''}
        onChange={handleDateChange}
        style={{
          width: '100%', padding: '8px 12px',
          border: '1px solid #d1d5db', borderRadius: 8,
          fontSize: '0.92rem', marginBottom: 12,
        }}
      />
      {plan.exam_date && dDay != null && (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8, marginBottom: 10 }}>
            <div style={{ padding: 8, background: '#f0fdf4', borderRadius: 6, textAlign: 'center' }}>
              <div style={{ fontSize: '0.72rem', color: '#15803d', fontWeight: 700 }}>마스터</div>
              <div style={{ fontSize: '1.05rem', fontWeight: 800, color: '#047857' }}>{summary.mastered}</div>
            </div>
            <div style={{ padding: 8, background: '#fef3c7', borderRadius: 6, textAlign: 'center' }}>
              <div style={{ fontSize: '0.72rem', color: '#92400e', fontWeight: 700 }}>진행 중</div>
              <div style={{ fontSize: '1.05rem', fontWeight: 800, color: '#b45309' }}>{summary.inProgress}</div>
            </div>
            <div style={{ padding: 8, background: '#fee2e2', borderRadius: 6, textAlign: 'center' }}>
              <div style={{ fontSize: '0.72rem', color: '#991b1b', fontWeight: 700 }}>미시작</div>
              <div style={{ fontSize: '1.05rem', fontWeight: 800, color: '#b91c1c' }}>{summary.notStarted}</div>
            </div>
          </div>
          <div style={{ marginBottom: 10 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', color: '#374151', marginBottom: 4 }}>
              <span>전체 진척률</span>
              <span style={{ fontWeight: 800 }}>{progressPct}%</span>
            </div>
            <div style={{ height: 8, background: '#e5e7eb', borderRadius: 4, overflow: 'hidden' }}>
              <div style={{
                width: `${progressPct}%`, height: '100%',
                background: 'linear-gradient(90deg, #4f46e5, #06b6d4)',
              }} />
            </div>
          </div>
          {dDay > 0 && (
            <div style={{
              padding: 10, background: '#eef2ff',
              borderRadius: 8, fontSize: '0.85rem', color: '#3730a3',
              lineHeight: 1.55,
            }}>
              💡 시험까지 <strong>{dDay}일</strong> 남음. 미숙 단원 {summary.notStarted + summary.inProgress}개를 끝내려면
              하루에 <strong style={{ color: '#1e40af', fontSize: '1.05em' }}>{recommendedPerDay}개</strong> 권장.
            </div>
          )}
          {dDay <= 0 && (
            <div style={{
              padding: 10, background: '#fff7ed',
              borderRadius: 8, fontSize: '0.85rem', color: '#9a3412',
            }}>
              📌 시험일이 지났거나 오늘입니다. 새 시험일을 입력하세요.
            </div>
          )}
        </>
      )}
    </div>
  );
}
