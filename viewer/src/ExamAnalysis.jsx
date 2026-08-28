// 📊 기출 분석 — 감정평가사 기출(exam_analysis.json)을 과목별로 분석해 보여준다.
// 빈출 단원 랭킹 · 분야 비중 · 유형/난이도 분포 · 연도별 추이 · 빈출 개념. (문제풀이 탭)
import { useEffect, useMemo, useState } from 'react';
import { SUBJECTS } from './aiLearningStore';

const S1 = SUBJECTS.filter((s) => s.stage === 1);
const ACCENT = '#4361ee';
const card = { background: '#fff', border: '1px solid #eef0f3', borderRadius: 14, boxShadow: '0 1px 6px rgba(15,23,42,0.05)', padding: 14, marginBottom: 12 };
const stripPre = (s) => (s || '').replace(/^(?:제?\s*\d+\s*(?:장|절|관|편)|PART\s*0*\d+|Chapter\s*0*\d+)\s*/i, '').trim() || s;

function Bars({ items, max, unit = '', color = ACCENT, onClick, subLabel }) {
  const mx = max || Math.max(1, ...items.map((x) => x.n));
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
      {items.map((it, i) => {
        const pct = Math.round((it.n / mx) * 100);
        return (
          <button key={i} onClick={onClick ? () => onClick(it) : undefined}
            style={{ display: 'flex', alignItems: 'center', gap: 9, textAlign: 'left', background: 'none', border: 'none', padding: 0, cursor: onClick ? 'pointer' : 'default' }}>
            <span style={{ width: 150, flexShrink: 0, fontSize: '0.76rem', color: '#334155', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={it.name}>{it.name}</span>
            <span style={{ flex: 1, minWidth: 0, height: 12, background: '#f1f5f9', borderRadius: 6, overflow: 'hidden' }}>
              <span style={{ display: 'block', height: '100%', width: `${Math.max(4, pct)}%`, background: color, borderRadius: 6 }} />
            </span>
            <span style={{ width: 62, flexShrink: 0, textAlign: 'right', fontSize: '0.72rem', fontWeight: 800, color: '#475569', fontVariantNumeric: 'tabular-nums' }}>{it.n}{unit}{subLabel ? <span style={{ color: '#94a3b8', fontWeight: 600 }}> {subLabel(it)}</span> : null}</span>
          </button>
        );
      })}
    </div>
  );
}

function YearTrend({ data }) {
  const max = Math.max(1, ...data.map((d) => d.n));
  return (
    <div style={{ display: 'flex', alignItems: 'flex-end', gap: 3, height: 64 }}>
      {data.map((d) => (
        <div key={d.year} title={`${d.year}: ${d.n}문항`} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3 }}>
          <div style={{ width: '100%', height: `${Math.round((d.n / max) * 46)}px`, background: ACCENT, borderRadius: '3px 3px 0 0', minHeight: 2 }} />
          <span style={{ fontSize: '0.5rem', color: '#94a3b8', transform: 'rotate(-60deg)', transformOrigin: 'center', whiteSpace: 'nowrap' }}>{String(d.year).slice(2)}</span>
        </div>
      ))}
    </div>
  );
}

function SectionTitle({ children, hint }) {
  return <div style={{ display: 'flex', alignItems: 'baseline', gap: 7, marginBottom: 9 }}>
    <span style={{ fontSize: '0.82rem', fontWeight: 800, color: '#1e293b' }}>{children}</span>
    {hint && <span style={{ fontSize: '0.66rem', color: '#94a3b8' }}>{hint}</span>}
  </div>;
}

export default function ExamAnalysis({ onBack, onGoChapter }) {
  const [db, setDb] = useState(null);
  const [err, setErr] = useState('');
  const [sel, setSel] = useState('all');

  useEffect(() => {
    fetch('/data/exam_analysis.json').then((r) => r.ok ? r.json() : Promise.reject(new Error(String(r.status))))
      .then(setDb).catch((e) => setErr(e.message || '분석 데이터를 불러오지 못했습니다'));
  }, []);

  const subjectsOrdered = useMemo(() => (db ? S1.map((s) => db.subjects[s.id]).filter(Boolean) : []), [db]);

  const wrap = (children) => (
    <div style={{ minHeight: '100dvh', background: '#f8fafc' }}>
      <header style={{ position: 'sticky', top: 0, zIndex: 5, background: '#fff', borderBottom: '1px solid #eceff3', display: 'flex', alignItems: 'center', gap: 8, padding: '10px 14px' }}>
        {onBack && <button onClick={onBack} style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.3rem', color: '#475569', lineHeight: 1 }}>‹</button>}
        <span style={{ fontSize: '1rem', fontWeight: 800, color: '#1e293b' }}>📊 기출 분석</span>
        {db && <span style={{ marginLeft: 'auto', fontSize: '0.68rem', color: '#94a3b8', fontWeight: 700 }}>감정평가사 {db.years?.[0]}~{db.years?.[db.years.length - 1]} · {db.grandTotal}문항</span>}
      </header>
      <div style={{ padding: 14, maxWidth: 760, margin: '0 auto' }}>{children}</div>
    </div>
  );

  if (err) return wrap(<div style={{ ...card, color: '#64748b', textAlign: 'center' }}>{err}</div>);
  if (!db) return wrap(<div style={{ ...card, color: '#94a3b8', textAlign: 'center' }}>기출 분석을 불러오는 중…</div>);

  return wrap(
    <>
      {/* 과목 선택 */}
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 12 }}>
        {[{ id: 'all', short: '전과목' }, ...subjectsOrdered].map((s) => {
          const on = sel === s.id;
          return <button key={s.id} onClick={() => setSel(s.id)} style={{ fontSize: '0.76rem', fontWeight: 800, borderRadius: 8, padding: '7px 12px', cursor: 'pointer',
            border: on ? `1.5px solid ${ACCENT}` : '1px solid #e5e7eb', background: on ? '#eef1fe' : '#fff', color: on ? '#1e293b' : '#94a3b8' }}>{s.short}</button>;
        })}
      </div>

      {sel === 'all' ? (
        <div style={card}>
          <SectionTitle hint="클릭하면 과목별 상세">과목별 출제 개요</SectionTitle>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {subjectsOrdered.map((s) => {
              const topCh = s.byChapter[0];
              const topType = s.byType[0];
              return (
                <button key={s.id} onClick={() => setSel(s.id)} style={{ display: 'flex', alignItems: 'center', gap: 10, textAlign: 'left', background: '#fcfcfd', border: '1px solid #eef0f2', borderRadius: 10, padding: '11px 12px', cursor: 'pointer' }}>
                  <span style={{ fontSize: '0.86rem', fontWeight: 800, color: '#1e293b', width: 66, flexShrink: 0 }}>{s.short}</span>
                  <span style={{ fontSize: '0.72rem', fontWeight: 800, color: ACCENT, background: '#eef1fe', borderRadius: 999, padding: '2px 9px', flexShrink: 0 }}>{s.total}문항</span>
                  <span style={{ flex: 1, minWidth: 0, fontSize: '0.72rem', color: '#475569', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    빈출 <b style={{ color: '#334155' }}>{stripPre(topCh?.name)}</b> {topCh?.n} · {topType?.name} {Math.round((topType?.n / s.total) * 100)}%
                  </span>
                  <span style={{ color: '#cbd5e1' }}>›</span>
                </button>
              );
            })}
          </div>
        </div>
      ) : (() => {
        const s = db.subjects[sel]; if (!s) return null;
        const typeMax = Math.max(1, ...s.byType.map((x) => x.n));
        const diffMax = Math.max(1, ...s.byDifficulty.map((x) => x.n));
        return (
          <>
            <div style={{ ...card, display: 'flex', alignItems: 'center', gap: 14 }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 900, color: ACCENT, lineHeight: 1 }}>{s.total}</div>
                <div style={{ fontSize: '0.6rem', color: '#94a3b8', marginTop: 3 }}>총 기출</div>
              </div>
              <div style={{ width: 1, height: 30, background: '#eef0f2' }} />
              <div style={{ fontSize: '0.74rem', color: '#475569', lineHeight: 1.6 }}>
                가장 많이 나온 단원 <b>{stripPre(s.byChapter[0]?.name)}</b>({s.byChapter[0]?.n}문항)<br />
                주 유형 <b>{s.byType[0]?.name}</b> · 평균 난이도 {(() => { const t = s.byDifficulty.reduce((a, d) => a + Number(d.level) * d.n, 0), n = s.byDifficulty.reduce((a, d) => a + d.n, 0); return n ? (t / n).toFixed(1) : '–'; })()}
              </div>
            </div>

            <div style={card}>
              <SectionTitle hint={`${db.years?.[0]}~${db.years?.[db.years.length - 1]}`}>연도별 출제 수</SectionTitle>
              <YearTrend data={s.byYear} />
            </div>

            {s.byDivision.length > 1 && (
              <div style={card}>
                <SectionTitle hint="세부과목 비중">분야별 출제</SectionTitle>
                <Bars items={s.byDivision} unit="" subLabel={(it) => `${Math.round((it.n / s.total) * 100)}%`} />
              </div>
            )}

            <div style={card}>
              <SectionTitle hint="빈출순 · 클릭하면 그 단원 풀기">빈출 단원 Top 12</SectionTitle>
              <Bars items={s.byChapter.slice(0, 12).map((c) => ({ ...c, name: stripPre(c.name) }))}
                onClick={onGoChapter ? (it) => onGoChapter(sel, s.byChapter.find((c) => stripPre(c.name) === it.name)?.name || it.name) : undefined}
                subLabel={(it) => `${Math.round((it.n / s.total) * 100)}%`} />
            </div>

            <div style={card}>
              <SectionTitle hint="세부 절 빈출">빈출 절 Top 15</SectionTitle>
              <Bars items={s.bySection.slice(0, 15).map((c) => ({ ...c, name: c.name.split(' › ').map(stripPre).join(' › ') }))} />
            </div>

            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
              <div style={{ ...card, flex: '1 1 280px', marginBottom: 12 }}>
                <SectionTitle>문제 유형 분포</SectionTitle>
                <Bars items={s.byType} max={typeMax} subLabel={(it) => `${Math.round((it.n / s.total) * 100)}%`} />
              </div>
              <div style={{ ...card, flex: '1 1 220px', marginBottom: 12 }}>
                <SectionTitle hint="1 쉬움 ~ 5 어려움">난이도 분포</SectionTitle>
                <Bars items={s.byDifficulty.map((d) => ({ name: `난이도 ${d.level}`, n: d.n }))} max={diffMax} subLabel={(it) => `${Math.round((it.n / s.total) * 100)}%`} />
              </div>
            </div>

            <div style={card}>
              <SectionTitle hint="자주 출제된 세부 논점">빈출 개념 Top 20</SectionTitle>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {s.topConcepts.slice(0, 20).map((c) => (
                  <span key={c.name} style={{ fontSize: '0.72rem', fontWeight: 700, color: '#334155', background: '#f1f5f9', borderRadius: 999, padding: '4px 10px' }}>{c.name} <b style={{ color: ACCENT }}>{c.n}</b></span>
                ))}
              </div>
            </div>
          </>
        );
      })()}
    </>
  );
}
