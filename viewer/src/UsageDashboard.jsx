// 관측 데이터 대시보드 — Phase δ.
// viz 사용 통계 + AI 응답 평가 분포 + API 비용 추적.

import { useMemo } from 'react';
import { getVizUsage, getMsgRatings, getUsage, todayKey } from './aiLearningStore';
import { listTemplates } from './viz/vizRegistry';

const MODEL_RATE = {
  // USD per 1M tokens (입력/출력)
  'claude-sonnet-4-6': { input: 3, output: 15 },
  'gpt-5.4':           { input: 2.5, output: 15 },
  'gemini-3.5-flash':  { input: 1.5, output: 9 },
  'gemini-3.1-pro-preview': { input: 2, output: 12 },
};
const FX_KRW = 1340;

function summarizeVizUsage() {
  const usage = getVizUsage();
  const templates = listTemplates();
  const rows = templates.map((t) => {
    const u = usage[t.name] || { ok: 0, err: 0, last_ts: null };
    const total = (u.ok || 0) + (u.err || 0);
    const errRate = total > 0 ? (u.err || 0) / total : 0;
    return { name: t.name, helpText: t.helpText, ok: u.ok || 0, err: u.err || 0, total, errRate, last: u.last_ts };
  });
  rows.sort((a, b) => b.total - a.total);
  return rows;
}

function summarizeRatings() {
  const r = getMsgRatings();
  let up = 0, down = 0;
  Object.values(r).forEach((entry) => {
    if (entry?.rating === 1) up++;
    else if (entry?.rating === -1) down++;
  });
  return { up, down, total: up + down };
}

function summarizeCost7Days() {
  const usage = getUsage();
  const out = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(); d.setDate(d.getDate() - i);
    const pad = (n) => String(n).padStart(2, '0');
    const key = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
    const u = usage[key] || {};
    // 단순 추정 — Sonnet 4.6 단가 기준
    const cacheReadCost = (u.cache_read || 0) * 0.30 / 1e6;
    const cacheWriteCost = (u.cache_write || 0) * 6 / 1e6;
    const inputCost = (u.input_tokens || 0) * 3 / 1e6;
    const outputCost = (u.output_tokens || 0) * 15 / 1e6;
    const usd = cacheReadCost + cacheWriteCost + inputCost + outputCost;
    out.push({ date: key.slice(5), usd, krw: usd * FX_KRW, msgs: u.messages || 0 });
  }
  return out;
}

function MiniBar({ value, max, color, height = 24 }) {
  const pct = max > 0 ? Math.min(100, (value / max) * 100) : 0;
  return (
    <div style={{ flex: 1, position: 'relative', height, background: '#f3f4f6', borderRadius: 3 }}>
      <div style={{
        position: 'absolute', left: 0, bottom: 0,
        width: '100%', height: `${pct}%`,
        background: color, borderRadius: 3,
      }} />
    </div>
  );
}

export default function UsageDashboard() {
  const vizRows = useMemo(() => summarizeVizUsage(), []);
  const ratings = useMemo(() => summarizeRatings(), []);
  const cost7 = useMemo(() => summarizeCost7Days(), []);

  const usedCount = vizRows.filter((r) => r.total > 0).length;
  const totalTemplates = vizRows.length;
  const maxCost = Math.max(...cost7.map((c) => c.usd), 0.01);
  const totalCostKRW = cost7.reduce((a, b) => a + b.krw, 0);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {/* viz 사용 통계 */}
      <div style={{ padding: 14, background: '#fff', borderRadius: 10, border: '1px solid #e5e7eb' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 8 }}>
          <h3 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 800, color: '#111827' }}>
            📊 시각자료 사용 통계
          </h3>
          <span style={{ fontSize: '0.74rem', color: '#6b7280' }}>
            {usedCount}/{totalTemplates}개 호출됨
          </span>
        </div>
        {vizRows.filter((r) => r.total > 0).length === 0 ? (
          <div style={{ padding: 20, textAlign: 'center', fontSize: '0.85rem', color: '#9ca3af' }}>
            아직 시각자료가 호출되지 않았습니다.<br />
            AI에게 그래프·도식을 요청해보세요.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {vizRows.filter((r) => r.total > 0).map((r) => (
              <div key={r.name} style={{
                display: 'flex', alignItems: 'center', gap: 8,
                padding: '4px 8px', background: '#f9fafb', borderRadius: 6,
              }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#111827' }}>{r.name}</div>
                  <div style={{ fontSize: '0.7rem', color: '#6b7280', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {r.helpText}
                  </div>
                </div>
                <div style={{ textAlign: 'right', minWidth: 90 }}>
                  <div style={{ fontSize: '0.82rem', fontWeight: 800, color: r.errRate > 0.2 ? '#b91c1c' : '#047857' }}>
                    {r.ok}회
                  </div>
                  {r.err > 0 && (
                    <div style={{ fontSize: '0.7rem', color: '#b91c1c' }}>오류 {r.err}회</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* AI 응답 평가 */}
      <div style={{ padding: 14, background: '#fff', borderRadius: 10, border: '1px solid #e5e7eb' }}>
        <h3 style={{ margin: '0 0 10px', fontSize: '0.95rem', fontWeight: 800, color: '#111827' }}>
          💬 AI 응답 평가
        </h3>
        {ratings.total === 0 ? (
          <div style={{ padding: 12, textAlign: 'center', fontSize: '0.85rem', color: '#9ca3af' }}>
            AI 메시지 옆 👍 / 🤔 로 평가하면 통계가 누적됩니다.
          </div>
        ) : (
          <div style={{ display: 'flex', gap: 8 }}>
            <div style={{ flex: 1, padding: 12, background: '#f0fdf4', borderRadius: 8, textAlign: 'center' }}>
              <div style={{ fontSize: '0.72rem', color: '#15803d', fontWeight: 700 }}>👍 이해됨</div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#047857' }}>{ratings.up}</div>
              <div style={{ fontSize: '0.72rem', color: '#15803d' }}>
                {Math.round((ratings.up / ratings.total) * 100)}%
              </div>
            </div>
            <div style={{ flex: 1, padding: 12, background: '#fef2f2', borderRadius: 8, textAlign: 'center' }}>
              <div style={{ fontSize: '0.72rem', color: '#991b1b', fontWeight: 700 }}>🤔 더 자세히</div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#b91c1c' }}>{ratings.down}</div>
              <div style={{ fontSize: '0.72rem', color: '#991b1b' }}>
                {Math.round((ratings.down / ratings.total) * 100)}%
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 비용 7일 추이 */}
      <div style={{ padding: 14, background: '#fff', borderRadius: 10, border: '1px solid #e5e7eb' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 8 }}>
          <h3 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 800, color: '#111827' }}>
            💰 7일 비용 추이 (Sonnet 4.6 기준)
          </h3>
          <span style={{ fontSize: '0.82rem', color: '#1e40af', fontWeight: 800 }}>
            ~{Math.round(totalCostKRW).toLocaleString()}원
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: 6, height: 80, marginBottom: 6 }}>
          {cost7.map((c, i) => (
            <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
              <MiniBar value={c.usd} max={maxCost} color={c.usd > 0 ? '#4f46e5' : '#e5e7eb'} height={80} />
            </div>
          ))}
        </div>
        <div style={{ display: 'flex', gap: 6, fontSize: '0.7rem', color: '#9ca3af' }}>
          {cost7.map((c, i) => (
            <div key={i} style={{ flex: 1, textAlign: 'center' }}>{c.date}</div>
          ))}
        </div>
        <div style={{ marginTop: 6, fontSize: '0.74rem', color: '#6b7280', textAlign: 'right' }}>
          오늘: <span style={{ fontWeight: 700 }}>{Math.round(cost7[cost7.length - 1].krw).toLocaleString()}원</span> · {cost7[cost7.length - 1].msgs}건
        </div>
      </div>
    </div>
  );
}
