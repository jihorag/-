// 합격까지의 여정 타임라인 — 콤팩트형.
// 왼쪽: 연도 + (학년·나이) / 오른쪽: 12개월 가로 타임라인(수직선 그리드 + 마커).
// 마커는 자유 목록 — 감정평가사 1차(4월)·2차(7월), 임용 1차(11월)·2차(1월) 등.

import { useMemo, useState } from 'react';

const JOURNEY_KEY = 'quiz-journey-v3';

const mk = (id, label, month, type, status = 'pending') => ({ id, label, month, type, status });

// 사용자 예시 기본값 — 2028년 감정평가사 1차 합격 / 2029년 2차 합격,
// 2027.11 임용 1차 · 2028.01 임용 2차 추가
const DEFAULT_ROWS = [
  { id: 'y2026', year: 2026, grade: '3학년', age: 24,
    markers: [mk('gp1', '1차', 4, 'gp'), mk('gp2', '2차', 7, 'gp')] },
  { id: 'y2027', year: 2027, grade: '4학년', age: 25,
    markers: [mk('gp1', '1차', 4, 'gp'), mk('gp2', '2차', 7, 'gp'), mk('im1', '임용1', 11, 'im')] },
  { id: 'y2028', year: 2028, grade: '1년차', age: 26,
    markers: [mk('im2', '임용2', 1, 'im'), mk('gp1', '1차', 4, 'gp', 'passed'), mk('gp2', '2차', 7, 'gp')] },
  { id: 'y2029', year: 2029, grade: '2년차', age: 27,
    markers: [mk('gp1', '1차', 4, 'gp'), mk('gp2', '2차', 7, 'gp', 'passed')] },
];

// 홈 화면도 같은 데이터를 읽는다 — 저장 형식이 갈리지 않게 여기 하나만 쓴다.
export const loadJourneyRows = () => {
  try {
    const v = JSON.parse(localStorage.getItem(JOURNEY_KEY) || 'null');
    if (Array.isArray(v) && v.length) return v;
  } catch { /* noop */ }
  return DEFAULT_ROWS;
};
const loadRows = loadJourneyRows;
const saveRows = (rows) => {
  try { localStorage.setItem(JOURNEY_KEY, JSON.stringify(rows)); } catch { /* SSR */ }
};

// 상태 3종 — 예정 → 합격 → 재도전 순환
const STATUS = {
  pending: { word: '', mark: '' },
  passed: { word: '합격', mark: '✓' },
  failed: { word: '재도전', mark: '↻' },
};
const STATUS_ORDER = ['pending', 'passed', 'failed'];
const colorOf = (m) => m.type === 'im' ? '#0d9488' : m.label.startsWith('1') ? '#2563eb' : '#7c3aed';

const LEFT_W = 70;
const monthDate = (y, m) => new Date(y, m - 1, 15);
const fmtDday = (n) => n === 0 ? 'D-DAY' : n > 0 ? `D-${n}` : `D+${-n}`;
const posOf = (month) => ((month - 0.5) / 12) * 100;

export default function JourneyTimeline() {
  const [rows, setRows] = useState(loadRows);
  const [editing, setEditing] = useState(false);

  const update = (next) => { setRows(next); saveRows(next); };
  const setField = (id, field, value) =>
    update(rows.map((r) => (r.id === id ? { ...r, [field]: value } : r)));
  const cycleMarker = (rowId, markerId) =>
    update(rows.map((r) => r.id !== rowId ? r : {
      ...r,
      markers: r.markers.map((m) => m.id !== markerId ? m
        : { ...m, status: STATUS_ORDER[(STATUS_ORDER.indexOf(m.status) + 1) % STATUS_ORDER.length] }),
    }));
  const removeYear = (id) => update(rows.filter((r) => r.id !== id));
  const addYear = () => {
    const sorted = [...rows].sort((a, b) => a.year - b.year);
    const last = sorted[sorted.length - 1];
    const year = (last ? last.year : 2026) + 1;
    update([...rows, { id: `y${year}_${rows.length}`, year, grade: '', age: (last?.age || 24) + 1,
      markers: [mk('gp1', '1차', 4, 'gp'), mk('gp2', '2차', 7, 'gp')] }]);
  };

  const sortedRows = useMemo(() => [...rows].sort((a, b) => a.year - b.year), [rows]);
  const now = new Date();
  const curYear = now.getFullYear();
  const curMonth = now.getMonth() + 1;
  const today = useMemo(() => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; }, []);

  // 헤드라인 — 가장 임박한 미래의 미합격 마커까지 D-day
  const headline = useMemo(() => {
    let best = null;
    for (const r of sortedRows) {
      for (const m of r.markers) {
        if (m.status === 'passed') continue;
        const d = Math.round((monthDate(r.year, m.month) - today) / 86400000);
        if (d >= 0 && (!best || d < best.d)) best = { label: m.label, year: r.year, d, color: colorOf(m) };
      }
    }
    return best;
  }, [sortedRows, today]);

  return (
    <section style={{ background: '#fff', borderRadius: 16, padding: '16px 16px 18px',
      boxShadow: 'var(--shadow-md)', marginBottom: 14 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 4 }}>
        <span style={{ fontWeight: 800, fontSize: '0.95rem', color: '#111827' }}>🗺️ 합격까지의 여정</span>
        <button onClick={() => setEditing((v) => !v)}
          style={{ fontSize: '0.74rem', color: editing ? '#1d4ed8' : '#6b7280', fontWeight: 700,
            background: 'none', border: 'none', cursor: 'pointer' }}>
          {editing ? '완료' : '✏️ 편집'}
        </button>
      </div>
      <div style={{ fontSize: '0.82rem', color: '#374151', marginBottom: 12 }}>
        {headline ? (
          <>다음 <b style={{ color: headline.color }}>{headline.year} {headline.label}</b>까지{' '}
            <b style={{ color: headline.d <= 30 ? '#dc2626' : headline.d <= 90 ? '#ea580c' : '#1d4ed8' }}>
              {fmtDday(headline.d)}</b></>
        ) : (
          <span style={{ color: '#16a34a', fontWeight: 600 }}>🎉 합격을 향한 여정을 완주했어요</span>
        )}
      </div>

      {/* 월 눈금 헤더 (그리드 위에 한 번만) */}
      <div style={{ display: 'flex', marginBottom: 5 }}>
        <div style={{ width: LEFT_W, flexShrink: 0 }} />
        <div style={{ flex: 1, display: 'flex' }}>
          {Array.from({ length: 12 }, (_, i) => (
            <div key={i} style={{ flex: 1, textAlign: 'center', fontSize: '0.56rem',
              color: '#cbd5e1', fontWeight: 600 }}>{i + 1}</div>
          ))}
        </div>
      </div>

      {/* 연도별 행 */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {sortedRows.map((r) => {
          const isCur = r.year === curYear;
          return (
            <div key={r.id} style={{ display: 'flex', alignItems: 'center' }}>
              {/* 왼쪽: 연도 + 학년·나이 */}
              <div style={{ width: LEFT_W, flexShrink: 0, lineHeight: 1.15 }}>
                <div style={{ fontWeight: 800, fontSize: '0.92rem',
                  color: isCur ? '#4f46e5' : '#111827' }}>
                  {r.year}{isCur && <span style={{ fontSize: '0.56rem', color: '#4f46e5', marginLeft: 3 }}>●</span>}
                </div>
                <div style={{ fontSize: '0.62rem', color: '#9ca3af', fontWeight: 600 }}>
                  {[r.grade, r.age != null && r.age !== '' ? `${r.age}살` : null].filter(Boolean).join('·')}
                </div>
              </div>

              {/* 오른쪽: 12칸 그리드 + 마커 */}
              <div style={{ flex: 1, position: 'relative', height: 42,
                border: '1px solid #e5e7eb', borderRadius: 8, overflow: 'hidden', background: '#fcfcfd' }}>
                {/* 12칸 수직선 */}
                {Array.from({ length: 12 }, (_, i) => (
                  <div key={i} style={{ position: 'absolute', top: 0, bottom: 0,
                    left: `${(i / 12) * 100}%`, width: `${100 / 12}%`,
                    borderRight: i < 11 ? '1px solid #eef2f7' : 'none',
                    background: isCur && i + 1 === curMonth ? '#eef2ff' : 'transparent' }} />
                ))}
                {/* 오늘 라인 */}
                {isCur && (
                  <div style={{ position: 'absolute', top: 0, bottom: 0, left: `${posOf(curMonth)}%`,
                    width: 2, marginLeft: -1, background: '#a5b4fc' }} />
                )}
                {/* 마커 */}
                {r.markers.map((m) => {
                  const base = colorOf(m);
                  const dotBg = m.status === 'passed' ? '#16a34a' : m.status === 'failed' ? '#ea580c' : '#fff';
                  const dotBd = m.status === 'passed' ? '#16a34a' : m.status === 'failed' ? '#ea580c' : base;
                  const dotFg = m.status === 'pending' ? base : '#fff';
                  return (
                    <button key={m.id} onClick={() => editing && cycleMarker(r.id, m.id)}
                      title={editing ? '탭하여 상태 변경' : `${r.year} ${m.label}`}
                      style={{ position: 'absolute', left: `${posOf(m.month)}%`, top: '50%',
                        transform: 'translate(-50%,-50%)', display: 'flex', flexDirection: 'column',
                        alignItems: 'center', background: 'none', border: 'none', padding: 0,
                        cursor: editing ? 'pointer' : 'default', zIndex: 2 }}>
                      <span style={{ fontSize: '0.5rem', fontWeight: 800, color: dotBd, whiteSpace: 'nowrap',
                        lineHeight: 1, marginBottom: 1 }}>
                        {m.label}{m.status !== 'pending' ? ` ${STATUS[m.status].word}` : ''}
                      </span>
                      <span style={{ width: 15, height: 15, borderRadius: '50%', background: dotBg,
                        border: `2px solid ${dotBd}`, color: dotFg, fontSize: '0.55rem', fontWeight: 800,
                        display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        {STATUS[m.status].mark}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* 범례 */}
      <div style={{ display: 'flex', gap: 12, marginTop: 10, fontSize: '0.62rem', color: '#9ca3af' }}>
        <span><span style={{ color: '#2563eb', fontWeight: 800 }}>●</span> 감정평가사 1차</span>
        <span><span style={{ color: '#7c3aed', fontWeight: 800 }}>●</span> 2차</span>
        <span><span style={{ color: '#0d9488', fontWeight: 800 }}>●</span> 임용</span>
      </div>

      {/* 편집 패널 */}
      {editing && (
        <div style={{ marginTop: 14, paddingTop: 14, borderTop: '1px solid #f1f5f9' }}>
          <div style={{ fontSize: '0.72rem', color: '#6b7280', marginBottom: 10 }}>
            💡 그리드의 마커를 탭하면 <b>예정 → 합격 → 재도전</b>으로 바뀌어요.
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {sortedRows.map((r) => (
              <div key={r.id} style={{ display: 'flex', alignItems: 'center', gap: 6,
                background: '#f9fafb', border: '1px solid #e5e7eb', borderRadius: 8, padding: '7px 10px' }}>
                <span style={{ fontWeight: 800, fontSize: '0.82rem', color: '#374151', minWidth: 38 }}>{r.year}</span>
                <input type="text" value={r.grade} placeholder="학년/연차"
                  onChange={(e) => setField(r.id, 'grade', e.target.value)}
                  style={{ width: 70, fontSize: '0.74rem', padding: '4px 6px', border: '1px solid #e5e7eb', borderRadius: 6 }} />
                <input type="number" value={r.age} placeholder="나이"
                  onChange={(e) => setField(r.id, 'age', e.target.value === '' ? '' : Number(e.target.value))}
                  style={{ width: 52, fontSize: '0.74rem', padding: '4px 6px', border: '1px solid #e5e7eb', borderRadius: 6 }} />
                <span style={{ fontSize: '0.66rem', color: '#9ca3af' }}>살</span>
                <button onClick={() => removeYear(r.id)}
                  style={{ marginLeft: 'auto', fontSize: '0.7rem', color: '#dc2626',
                    background: 'none', border: 'none', cursor: 'pointer' }}>삭제</button>
              </div>
            ))}
          </div>
          <button onClick={addYear}
            style={{ marginTop: 10, width: '100%', fontSize: '0.78rem', fontWeight: 700, color: '#1d4ed8',
              background: '#eff6ff', border: '1px dashed #bfdbfe', borderRadius: 8, padding: '8px', cursor: 'pointer' }}>
            + 연도 추가
          </button>
        </div>
      )}
    </section>
  );
}
