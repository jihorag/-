// 답안 히스토리 위젯 — 2차 답안 작성 모드에서 같은 leaf 의 시간순 답안 표시.
// 핵심 기능: 점수 추이 미니 차트, 자동 인사이트(개선·여전한 약점), 옛 답안 펼치기.

import { useState, useMemo } from 'react';
import { getAnswerHistory } from './aiLearningStore';

const CHART_W = 240, CHART_H = 60, PADL = 18, PADB = 14, PADT = 8, PADR = 8;

function ScoreTrend({ history, max = 30 }) {
  if (!history.length) return null;
  const pts = history.map((h, i) => {
    const x = PADL + (i / Math.max(1, history.length - 1)) * (CHART_W - PADL - PADR);
    const y = PADT + (1 - (h.score / max)) * (CHART_H - PADT - PADB);
    return [x, y, h.score];
  });
  const pathD = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');
  const lastScore = pts[pts.length - 1][2];
  const firstScore = pts[0][2];
  const delta = lastScore - firstScore;
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
      <svg viewBox={`0 0 ${CHART_W} ${CHART_H}`} style={{ width: CHART_W, height: CHART_H }}>
        <line x1={PADL} y1={CHART_H - PADB} x2={CHART_W - PADR} y2={CHART_H - PADB} stroke="#e5e7eb" strokeWidth={1} />
        <text x={PADL - 4} y={PADT + 4} fontSize={8} fill="#9ca3af" textAnchor="end">{max}</text>
        <text x={PADL - 4} y={CHART_H - PADB + 2} fontSize={8} fill="#9ca3af" textAnchor="end">0</text>
        <path d={pathD} fill="none" stroke="#4f46e5" strokeWidth={2} />
        {pts.map((p, i) => (
          <circle key={i} cx={p[0]} cy={p[1]} r={3} fill={i === pts.length - 1 ? '#1d4ed8' : '#a5b4fc'} />
        ))}
      </svg>
      <div style={{ fontSize: '0.78rem', lineHeight: 1.4 }}>
        <div style={{ fontWeight: 800, color: '#111827' }}>{lastScore}/{max}점</div>
        <div style={{ color: delta > 0 ? '#15803d' : delta < 0 ? '#b91c1c' : '#6b7280', fontWeight: 600 }}>
          {delta > 0 ? '▲' : delta < 0 ? '▼' : '–'} {Math.abs(delta)}점 {history.length > 1 ? '(첫 답안 대비)' : ''}
        </div>
        <div style={{ color: '#6b7280', fontSize: '0.72rem' }}>{history.length}회 작성</div>
      </div>
    </div>
  );
}

function extractInsight(history) {
  if (history.length < 2) return null;
  const last = history[history.length - 1];
  const prev = history[history.length - 2];
  if (!last || !prev) return null;
  const improvements = [];
  const persistent = [];
  // strengths 비교 — 새로 추가된 강점
  const lastS = new Set(last.strengths || []);
  const prevS = new Set(prev.strengths || []);
  lastS.forEach((s) => { if (!prevS.has(s)) improvements.push(s); });
  // missed 비교 — 여전히 지적된 약점
  const lastM = new Set(last.missed || []);
  const prevM = new Set(prev.missed || []);
  lastM.forEach((m) => { if (prevM.has(m)) persistent.push(m); });
  return { improvements, persistent, scoreDelta: last.score - prev.score };
}

export default function AnswerHistoryWidget({ leafId, onLoadAnswer }) {
  const [expanded, setExpanded] = useState(null);
  const history = useMemo(() => getAnswerHistory(leafId), [leafId]);
  const insight = useMemo(() => extractInsight(history), [history]);

  if (!leafId || !history.length) return null;

  const maxScore = history[0]?.max || 30;

  return (
    <div style={{
      margin: '8px 0', padding: 10,
      background: '#f9fafb', border: '1px solid #e5e7eb', borderRadius: 8,
    }}>
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
        marginBottom: 8,
      }}>
        <div style={{ fontWeight: 800, color: '#111827', fontSize: '0.88rem' }}>
          📈 답안 추이 · {history.length}회
        </div>
        <button
          onClick={() => setExpanded(expanded === 'all' ? null : 'all')}
          style={{
            background: 'none', border: 'none', cursor: 'pointer',
            color: '#4f46e5', fontSize: '0.78rem', fontWeight: 700,
          }}
        >
          {expanded === 'all' ? '접기 ▴' : '전체 보기 ▾'}
        </button>
      </div>
      <ScoreTrend history={history} max={maxScore} />
      {insight && (insight.improvements.length > 0 || insight.persistent.length > 0) && (
        <div style={{ marginTop: 10, padding: '8px 10px', background: '#fff', borderRadius: 6, border: '1px solid #e5e7eb' }}>
          {insight.improvements.length > 0 && (
            <div style={{ fontSize: '0.78rem', color: '#15803d', marginBottom: 4 }}>
              ✓ <strong>이번 보완</strong>: {insight.improvements.join(', ')}
            </div>
          )}
          {insight.persistent.length > 0 && (
            <div style={{ fontSize: '0.78rem', color: '#b91c1c' }}>
              ⚠️ <strong>여전한 약점</strong>: {insight.persistent.join(', ')}
            </div>
          )}
        </div>
      )}
      {expanded === 'all' && (
        <div style={{ marginTop: 10, maxHeight: 320, overflowY: 'auto' }}>
          {history.slice().reverse().map((h, idx) => {
            const real = history.length - idx;
            return (
              <details key={h.ts} style={{ marginBottom: 6, padding: '6px 10px', background: '#fff', borderRadius: 6, border: '1px solid #e5e7eb' }}>
                <summary style={{ cursor: 'pointer', fontSize: '0.82rem', fontWeight: 700 }}>
                  #{real} · {h.score}/{h.max}점 · {h.ts?.slice(0, 16).replace('T', ' ')} · {h.time_used_min ? `${h.time_used_min}분` : ''}
                </summary>
                <div style={{ marginTop: 6, fontSize: '0.78rem', color: '#374151', lineHeight: 1.55 }}>
                  {h.strengths?.length > 0 && (
                    <div>✓ <strong>강점</strong>: {h.strengths.join(', ')}</div>
                  )}
                  {h.missed?.length > 0 && (
                    <div>⚠ <strong>보강</strong>: {h.missed.join(', ')}</div>
                  )}
                  {h.rewrite_hint && (
                    <div style={{ marginTop: 4, padding: '4px 8px', background: '#fef3c7', borderRadius: 4, color: '#854d0e' }}>
                      💡 {h.rewrite_hint}
                    </div>
                  )}
                  {h.answer_text && onLoadAnswer && (
                    <button
                      onClick={() => onLoadAnswer(h.answer_text)}
                      style={{
                        marginTop: 6, padding: '4px 10px',
                        background: '#eef2ff', color: '#4338ca',
                        border: '1px solid #c7d2fe', borderRadius: 6,
                        fontSize: '0.74rem', fontWeight: 700, cursor: 'pointer',
                      }}
                    >
                      📋 이 답안 불러오기 (재작성)
                    </button>
                  )}
                </div>
              </details>
            );
          })}
        </div>
      )}
    </div>
  );
}
