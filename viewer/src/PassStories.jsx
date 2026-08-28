// 🏆 합격수기 열람 탭 — 정독·구조화한 감정평가사 합격수기 카드.
// 데이터: public/data/pass-stories/pass_stories.json (박문각 게시판 + 랜드잇 + eduspa/법률저널 등 78건).
// AI 학습·드릴·계획에 이미 '방법론'으로 녹여 쓰지만, 원본 수기 자체도 사람이 직접 열람할 수 있게 한다.
import { useState, useEffect, useMemo } from 'react';
import { ArrowLeft, X, Search, ExternalLink } from 'lucide-react';

const TRACK_META = {
  '동차': { c: '#0e7490', bg: '#ecfeff', label: '동차' },
  '유예': { c: '#b45309', bg: '#fffbeb', label: '유예' },
  '장수': { c: '#7c3aed', bg: '#f5f3ff', label: '장수' },
};
const trackMeta = (t) => TRACK_META[t] || { c: '#64748b', bg: '#f1f5f9', label: t || '미상' };

function round2Avg(scores) {
  const r2 = scores?.round2;
  if (!r2) return null;
  // 여러 해차 응시가 있으면 합격한(가장 최근) 해의 평균을 우선
  const years = Object.keys(r2).filter((k) => /^\d{4}$/.test(k)).sort();
  const last = years.length ? r2[years[years.length - 1]] : r2;
  const avg = last?.avg ?? r2.avg;
  return typeof avg === 'number' ? avg : null;
}

function Field({ label, children }) {
  if (children == null || children === '' || (Array.isArray(children) && !children.length)) return null;
  return (
    <div style={{ marginBottom: 14 }}>
      <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#94a3b8', marginBottom: 5, letterSpacing: '0.02em' }}>{label}</div>
      <div style={{ fontSize: '0.86rem', color: '#1e293b', lineHeight: 1.65 }}>{children}</div>
    </div>
  );
}

function Detail({ rec, onClose }) {
  const tm = trackMeta(rec.track);
  const m = rec.methods || {};
  const s = rec.source || {};
  const sh = rec.study_hours || {};
  return (
    <div onClick={onClose}
      style={{ position: 'fixed', inset: 0, zIndex: 3000, background: 'rgba(15,23,42,0.55)', display: 'flex', justifyContent: 'center', alignItems: 'flex-start', overflowY: 'auto', padding: '24px 12px' }}>
      <div onClick={(e) => e.stopPropagation()}
        style={{ background: '#fff', borderRadius: 16, maxWidth: 620, width: '100%', padding: '22px 22px 30px', boxShadow: '0 20px 60px rgba(0,0,0,0.3)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, marginBottom: 14 }}>
          <div style={{ minWidth: 0 }}>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', alignItems: 'center', marginBottom: 6 }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 800, color: tm.c, background: tm.bg, padding: '3px 9px', borderRadius: 999 }}>{tm.label}</span>
              {rec.working && <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#0f766e', background: '#f0fdfa', padding: '3px 9px', borderRadius: 999 }}>직장병행</span>}
              {rec.year && <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#64748b' }}>{rec.year}{rec.cohort ? ` · ${rec.cohort}` : ''}</span>}
            </div>
            <div style={{ fontSize: '1.02rem', fontWeight: 800, color: '#0f172a', lineHeight: 1.35 }}>{s.title || '합격수기'}</div>
            {s.author && <div style={{ fontSize: '0.78rem', color: '#94a3b8', marginTop: 3 }}>{s.author}</div>}
          </div>
          <button onClick={onClose} style={{ border: 'none', background: '#f1f5f9', borderRadius: 9, cursor: 'pointer', padding: 7, flexShrink: 0 }}><X size={18} color="#64748b" /></button>
        </div>

        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 16 }}>
          {rec.total_period_months && <Stat label="총 수험" value={`${rec.total_period_months}개월`} />}
          {round2Avg(rec.scores) != null && <Stat label="2차 평균" value={`${round2Avg(rec.scores)}점`} />}
          {rec.scores?.round1 && <Stat label="1차" value={typeof rec.scores.round1 === 'number' ? `${rec.scores.round1}` : '합격'} />}
        </div>

        <Field label="공부 시간">{[sh.weekday && `평일 ${sh.weekday}`, sh.weekend && `주말 ${sh.weekend}`].filter(Boolean).join(' · ')}</Field>
        <Field label="핵심 교훈">
          <ul style={{ margin: 0, paddingLeft: 18 }}>{(rec.key_takeaways || []).map((k, i) => <li key={i} style={{ marginBottom: 4 }}>{k}</li>)}</ul>
        </Field>
        {(m.round2_common || m.round1) && <Field label="공부법 — 총론">{m.round2_common || m.round1}</Field>}
        {(m.실무 || m.이론 || m.법규) && (
          <Field label="2차 과목별 공부법">
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {m.실무 && <div><b style={{ color: '#7c3aed' }}>실무</b> {m.실무}</div>}
              {m.이론 && <div><b style={{ color: '#0d9488' }}>이론</b> {m.이론}</div>}
              {m.법규 && <div><b style={{ color: '#be123c' }}>법규</b> {m.법규}</div>}
            </div>
          </Field>
        )}
        <Field label="실패 요인 / 시행착오">
          {(rec.failure_factors || []).length ? <ul style={{ margin: 0, paddingLeft: 18 }}>{rec.failure_factors.map((k, i) => <li key={i} style={{ marginBottom: 4 }}>{k}</li>)}</ul> : null}
        </Field>
        <Field label="사용 교재·단권화">{rec.materials}</Field>
        <Field label="메모">{rec.notes}</Field>

        {s.url && (
          <a href={s.url} target="_blank" rel="noreferrer"
            style={{ display: 'inline-flex', alignItems: 'center', gap: 5, marginTop: 8, fontSize: '0.8rem', color: '#2563eb', textDecoration: 'none', fontWeight: 700 }}>
            <ExternalLink size={14} /> 원문 보기 · {s.name || '출처'}
          </a>
        )}
        {!s.url && s.name && <div style={{ marginTop: 8, fontSize: '0.76rem', color: '#94a3b8' }}>출처: {s.name}</div>}
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div style={{ background: '#f8fafc', border: '1px solid #eef2f6', borderRadius: 10, padding: '8px 12px', textAlign: 'center', minWidth: 74 }}>
      <div style={{ fontSize: '0.66rem', color: '#94a3b8', fontWeight: 700 }}>{label}</div>
      <div style={{ fontSize: '0.92rem', color: '#0f172a', fontWeight: 800, marginTop: 2 }}>{value}</div>
    </div>
  );
}

export default function PassStories({ onBack }) {
  const [all, setAll] = useState(null);
  const [track, setTrack] = useState('전체');
  const [workingOnly, setWorkingOnly] = useState(false);
  const [q, setQ] = useState('');
  const [sel, setSel] = useState(null);

  useEffect(() => {
    let dead = false;
    fetch('/data/pass-stories/pass_stories.json')
      .then((r) => r.json())
      .then((d) => { if (!dead) setAll(Array.isArray(d) ? d : (d.stories || [])); })
      .catch(() => { if (!dead) setAll([]); });
    return () => { dead = true; };
  }, []);

  const filtered = useMemo(() => {
    if (!all) return [];
    const needle = q.trim();
    return all.filter((r) => {
      if (track !== '전체' && r.track !== track) return false;
      if (workingOnly && !r.working) return false;
      if (needle) {
        const hay = JSON.stringify(r);
        if (!hay.includes(needle)) return false;
      }
      return true;
    });
  }, [all, track, workingOnly, q]);

  const counts = useMemo(() => {
    const c = { 전체: all?.length || 0, 동차: 0, 유예: 0, 장수: 0 };
    (all || []).forEach((r) => { if (c[r.track] != null) c[r.track] += 1; });
    return c;
  }, [all]);

  return (
    <div className="app-container" style={{ background: '#f8fafc', minHeight: '100dvh', paddingBottom: 30 }}>
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
        {onBack && (
          <button className="back-btn" onClick={onBack}>
            <ArrowLeft size={24} style={{ marginRight: 8 }} /><span style={{ fontSize: '0.95rem', fontWeight: 600 }}>홈</span>
          </button>
        )}
      </header>
      <div className="screen-head">
        <h1 className="screen-title">🏆 합격수기</h1>
        <p style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: 4 }}>
          실제 합격자 {all?.length ?? '…'}명의 수기를 정독·구조화 — 이 앱의 AI 학습·드릴·계획도 이 패턴을 반영합니다.
        </p>
      </div>

      <main className="main-content" style={{ marginTop: 8 }}>
        {/* 필터 */}
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 10, alignItems: 'center' }}>
          {['전체', '동차', '유예', '장수'].map((t) => {
            const on = track === t;
            const tm = t === '전체' ? { c: '#334155' } : trackMeta(t);
            return (
              <button key={t} onClick={() => setTrack(t)}
                style={{ padding: '6px 12px', borderRadius: 999, cursor: 'pointer', fontWeight: 800, fontSize: '0.78rem',
                  border: on ? `1.5px solid ${tm.c}` : '1px solid #e5e7eb', background: on ? '#fff' : '#fff', color: on ? tm.c : '#94a3b8' }}>
                {t} <span style={{ fontWeight: 600, opacity: 0.7 }}>{counts[t] ?? 0}</span>
              </button>
            );
          })}
          <button onClick={() => setWorkingOnly((v) => !v)}
            style={{ padding: '6px 12px', borderRadius: 999, cursor: 'pointer', fontWeight: 800, fontSize: '0.78rem',
              border: workingOnly ? '1.5px solid #0f766e' : '1px solid #e5e7eb', background: '#fff', color: workingOnly ? '#0f766e' : '#94a3b8' }}>
            직장병행
          </button>
        </div>
        <div style={{ position: 'relative', marginBottom: 14 }}>
          <Search size={16} color="#94a3b8" style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)' }} />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="키워드 검색 (예: 완주, 단권화, 회독, 슬럼프)"
            style={{ width: '100%', padding: '10px 12px 10px 36px', border: '1px solid #e5e7eb', borderRadius: 10, fontSize: '15px', boxSizing: 'border-box', background: '#fff' }} />
        </div>

        {all == null && <div style={{ padding: 30, textAlign: 'center', color: '#9ca3af', fontSize: '0.85rem' }}>불러오는 중…</div>}
        {all && filtered.length === 0 && <div style={{ padding: 30, textAlign: 'center', color: '#9ca3af', fontSize: '0.85rem' }}>조건에 맞는 수기가 없어요</div>}

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 10 }}>
          {filtered.map((r) => {
            const tm = trackMeta(r.track);
            const avg = round2Avg(r.scores);
            const take = (r.key_takeaways || [])[0];
            return (
              <button key={r.id} onClick={() => setSel(r)}
                style={{ textAlign: 'left', background: '#fff', border: '1px solid #eef0f2', borderRadius: 14, padding: '13px 14px', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: 7 }}>
                <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.68rem', fontWeight: 800, color: tm.c, background: tm.bg, padding: '2px 8px', borderRadius: 999 }}>{tm.label}</span>
                  {r.working && <span style={{ fontSize: '0.66rem', fontWeight: 700, color: '#0f766e', background: '#f0fdfa', padding: '2px 7px', borderRadius: 999 }}>직장</span>}
                  <span style={{ fontSize: '0.68rem', color: '#94a3b8', fontWeight: 700, marginLeft: 'auto' }}>
                    {r.year || ''}{avg != null ? ` · 2차 ${avg}` : ''}
                  </span>
                </div>
                <div style={{ fontSize: '0.86rem', fontWeight: 800, color: '#1e293b', lineHeight: 1.35, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                  {r.source?.title || '합격수기'}
                </div>
                {take && (
                  <div style={{ fontSize: '0.76rem', color: '#64748b', lineHeight: 1.5, display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    💡 {take}
                  </div>
                )}
                {r.total_period_months && <div style={{ fontSize: '0.7rem', color: '#94a3b8', fontWeight: 600, marginTop: 'auto' }}>총 {r.total_period_months}개월</div>}
              </button>
            );
          })}
        </div>
      </main>

      {sel && <Detail rec={sel} onClose={() => setSel(null)} />}
    </div>
  );
}
