// 🩺 내 실력 현황 — 과목별 진도(AI 커버리지)·정답률(위험도 색)·진단. (홈 탭에서 사용)
// subjectState: buildSubjectState(learnCtx) 결과 · d1: 1차 D-day(일) · onOpenTask/onDiagnostic 콜백.
import { useState } from 'react';
import { SUBJECTS } from './aiLearningStore';
import { leafLabel } from './learnState';

const ACCENT = '#4361ee';

export default function SubjectHealth({ subjectState, d1 = 0, onOpenTask, onDiagnostic }) {
  const [expSubj, setExpSubj] = useState(null);
  if (!subjectState) return null;
  return (
    <section style={{ background: '#fff', border: '1px solid #eceff3', borderRadius: 16, boxShadow: 'var(--shadow-md)', marginBottom: 14, padding: 15 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.92rem', fontWeight: 800, color: '#1e293b' }}>🩺 내 실력 현황</span>
        {(() => {
          const s1 = SUBJECTS.filter((s) => s.stage === 1).map((s) => subjectState[s.id]).filter(Boolean);
          if (!s1.length) return null;
          const avg = Math.round(s1.reduce((a, x) => a + x.coveredPct, 0) / s1.length);
          const accs = s1.map((x) => x.avgAccuracy).filter((x) => x != null);
          const avgAcc = accs.length ? Math.round(accs.reduce((a, b) => a + b, 0) / accs.length) : null;
          const aC = avgAcc == null ? '#94a3b8' : avgAcc < 40 ? '#ef4444' : avgAcc < 60 ? '#f59e0b' : avgAcc < 80 ? '#4361ee' : '#16a34a';
          return (
            <span style={{ marginLeft: 'auto', display: 'inline-flex', gap: 5 }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#334155', background: '#eef1fe', borderRadius: 999, padding: '2px 10px' }}>진도 {avg}%</span>
              {avgAcc != null && <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#fff', background: aC, borderRadius: 999, padding: '2px 10px' }}>정답률 {avgAcc}%</span>}
            </span>
          );
        })()}
      </div>
      <div style={{ fontSize: '0.72rem', color: '#94a3b8', margin: '3px 0 11px' }}>문제를 풀면 자동 측정됩니다 · 진단으로 여러 단원을 빠르게 파악하세요</div>
      {(() => {
        const risk = SUBJECTS.filter((s) => s.stage === 1).filter((s) => { const st = subjectState[s.id]; return st && st.avgAccuracy != null && st.avgAccuracy < 40; });
        if (!risk.length) return null;
        return (
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 9, padding: '8px 11px', marginBottom: 11, fontSize: '0.74rem', color: '#334155', fontWeight: 700, lineHeight: 1.5 }}>
            ⚠️ 과락 위험(정답률 40% 미만): {risk.map((s) => s.short).join(' · ')} — 동차는 한 과목만 과락해도 끝. 이 과목부터 끌어올리세요
          </div>
        );
      })()}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {SUBJECTS.map((s) => {
          const st = subjectState[s.id];
          const covered = st ? st.coveredPct : 0;
          const acc = st ? st.avgAccuracy : null;
          const accColor = acc == null ? '#cbd5e1' : acc < 40 ? '#ef4444' : acc < 60 ? '#f59e0b' : acc < 80 ? '#4361ee' : '#16a34a';
          const open = expSubj === s.id;
          const remaining = st ? st.total - st.mastered : 0;
          const perDay = st && d1 > 0 ? remaining / d1 : null;
          const pace = perDay == null ? null : perDay <= 0.4 ? { t: '여유', c: '#94a3b8' } : perDay <= 0.9 ? { t: '빠듯', c: '#94a3b8' } : { t: '촉박', c: '#334155' };
          const grp = (label, arr, type, color, showAcc) => (arr && arr.length ? (
            <div style={{ marginTop: 7 }}>
              <div style={{ fontSize: '0.64rem', fontWeight: 800, color, marginBottom: 4 }}>{label} {arr.length}</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
                {arr.slice(0, 6).map((x, i) => (
                  <button key={i} onClick={() => onOpenTask && onOpenTask({ type, subjectId: s.id, leafId: x.leaf.id })}
                    style={{ fontSize: '0.7rem', fontWeight: 600, color: '#475569', background: '#f8fafc', border: '1px solid #eef0f2', borderRadius: 7, padding: '4px 8px', cursor: 'pointer' }}>
                    {leafLabel(x.leaf)}{showAcc && x.quiz && x.quiz.answered ? ` ${Math.round((x.quiz.accuracy || 0) * 100)}%` : ''} ›
                  </button>
                ))}
              </div>
            </div>
          ) : null);
          return (
            <div key={s.id} style={{ border: open ? '1px solid #eef0f2' : '1px solid transparent', borderRadius: 10, padding: open ? '8px 10px' : 0, background: open ? '#fcfcfd' : 'transparent' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <button onClick={() => setExpSubj(open ? null : s.id)} style={{ flex: 1, minWidth: 0, display: 'flex', alignItems: 'center', gap: 10, background: 'none', border: 'none', cursor: 'pointer', padding: 0, textAlign: 'left' }}>
                  <span style={{ fontSize: '0.95rem', flexShrink: 0 }}>{s.icon}</span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
                      <span style={{ fontSize: '0.88rem', fontWeight: 800, color: '#1e293b' }}>{s.short}</span>
                      <span style={{ fontSize: '0.56rem', fontWeight: 800, color: s.stage === 2 ? '#7c3aed' : '#4361ee', background: s.stage === 2 ? '#f0ebff' : '#eef1fe', borderRadius: 5, padding: '1px 5px' }}>{s.stage === 2 ? '2차' : '1차'}</span>
                      <span style={{ marginLeft: 'auto', fontSize: '0.7rem', fontWeight: 800, color: '#fff', background: accColor, borderRadius: 999, padding: '2px 9px', minWidth: 42, textAlign: 'center' }}>
                        {acc == null ? '미측정' : `${acc}%`}
                      </span>
                      <span style={{ fontSize: '0.7rem', color: '#cbd5e1' }}>{open ? '▲' : '▼'}</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
                      <span style={{ width: 28, flexShrink: 0, fontSize: '0.58rem', fontWeight: 800, color: '#94a3b8' }}>진도</span>
                      <div style={{ flex: 1, height: 8, borderRadius: 4, background: '#f1f5f9', overflow: 'hidden' }}>
                        <div style={{ height: '100%', width: `${covered}%`, background: ACCENT, transition: 'width .3s' }} />
                      </div>
                      <span style={{ width: 66, flexShrink: 0, textAlign: 'right', fontSize: '0.62rem', fontWeight: 700, color: '#64748b' }}>{covered}%{st ? ` ${st.mastered}/${st.total}` : ''}</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginTop: 4 }}>
                      <span style={{ width: 28, flexShrink: 0, fontSize: '0.58rem', fontWeight: 800, color: '#94a3b8' }}>정답</span>
                      <div style={{ flex: 1, height: 8, borderRadius: 4, background: '#f1f5f9', overflow: 'hidden' }}>
                        <div style={{ height: '100%', width: `${acc == null ? 0 : acc}%`, background: accColor, transition: 'width .3s' }} />
                      </div>
                      <span style={{ width: 66, flexShrink: 0, textAlign: 'right', fontSize: '0.62rem', fontWeight: 800, color: accColor }}>{acc == null ? '—' : `${acc}%`}</span>
                    </div>
                  </div>
                </button>
                {s.stage === 1 && onDiagnostic && (
                  <button onClick={() => onDiagnostic(s.id)} style={{ flexShrink: 0, fontSize: '0.72rem', fontWeight: 800, color: '#334155', background: '#eef1fe', border: '1px solid #c6cefb', borderRadius: 8, padding: '5px 10px', cursor: 'pointer' }}>
                    진단
                  </button>
                )}
              </div>
              {open && st && (
                <div style={{ marginLeft: 26, marginTop: 6 }}>
                  {d1 > 0 && s.stage === 1 && (
                    <div style={{ fontSize: '0.72rem', color: '#475569' }}>
                      🏁 완주까지 <b>{remaining}단원</b> · 1차 D-{d1} → 하루 <b>{perDay != null ? perDay.toFixed(2) : '–'}단원</b> 필요
                      {pace && <span style={{ marginLeft: 6, fontWeight: 800, color: pace.c }}>{pace.t}</span>}
                    </div>
                  )}
                  {grp('🔁 복습 도래', st.due, 'drill', '#94a3b8')}
                  {grp('📉 약점 단원', st.weak, 'solve', '#334155', true)}
                  {grp('📖 다음 볼 단원', st.next, 'study', '#4361ee')}
                  {!st.due.length && !st.weak.length && !st.next.length && (
                    <div style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: 6 }}>아직 데이터가 적어요 · 위 진단으로 측정해보세요</div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
      {(() => {
        let ep = {}; try { ep = JSON.parse(localStorage.getItem('quiz-essay-progress') || '{}') || {}; } catch { /* */ }
        const entries = Object.values(ep).filter((e) => e && e.attempts && e.attempts.length);
        const scores = entries.map((e) => e.attempts[e.attempts.length - 1].selfScore).filter((x) => typeof x === 'number');
        const avg = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null;
        return (
          <div style={{ marginTop: 11, paddingTop: 11, borderTop: '1px solid #f1f5f9', display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ fontSize: '0.9rem' }}>✍️</span>
            <span style={{ fontWeight: 800, fontSize: '0.82rem', color: entries.length ? '#475569' : '#cbd5e1' }}>2차 답안 연습</span>
            <span style={{ fontSize: '0.66rem', color: '#94a3b8' }}>{entries.length ? `${entries.length}개 작성` : '2차 논술에서 답안 쓰면 집계'}</span>
            {entries.length > 0 && (
              <span style={{ marginLeft: 'auto', fontSize: '0.72rem', fontWeight: 800, color: avg == null ? '#cbd5e1' : avg < 40 ? '#334155' : '#475569' }}>
                자기채점 {avg == null ? '—' : `${avg}점`}
              </span>
            )}
          </div>
        );
      })()}
    </section>
  );
}
