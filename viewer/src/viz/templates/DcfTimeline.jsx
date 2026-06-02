// DCF 타임라인 — 연차별 현금흐름 + 할인계수 + PV.
// 운영기간 NOI + 종기가치(reversion) → 각 연차 PV → 합계 = V.

function fmt(n) {
  if (typeof n !== 'number') return n || '—';
  return Math.round(n).toLocaleString('ko-KR');
}

function DcfTimelineChart({ params }) {
  const r = params.discount_rate || 0.08;
  const cashflows = params.cashflows || [];
  // 각 연차 PV 자동 계산
  const rows = cashflows.map((cf, i) => {
    const t = cf.year != null ? cf.year : i + 1;
    const df = Math.pow(1 + r, -t);
    const pv = (Number(cf.amount) || 0) * df;
    return { t, amount: Number(cf.amount) || 0, df, pv, note: cf.note, type: cf.type || 'noi' };
  });
  const totalPV = rows.reduce((a, b) => a + b.pv, 0);

  const TYPE_COLOR = {
    noi: { bg: '#dbeafe', text: '#1e40af', label: 'NOI' },
    reversion: { bg: '#fef3c7', text: '#92400e', label: '복귀가치' },
    capex: { bg: '#fee2e2', text: '#991b1b', label: '자본지출' },
    other: { bg: '#f3f4f6', text: '#374151', label: '기타' },
  };

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 14, overflowX: 'auto' }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 6 }}>
          📅 {params.scenario}
        </figcaption>
      )}
      <div style={{ fontSize: '0.78rem', color: '#6b7280', marginBottom: 8 }}>
        할인율 r = <strong style={{ color: '#111827' }}>{(r * 100).toFixed(2)}%</strong>
        {params.method && <span> · {params.method}</span>}
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', minWidth: 480 }}>
        <thead>
          <tr style={{ background: '#f9fafb' }}>
            <th style={{ padding: '6px 8px', textAlign: 'right', borderBottom: '2px solid #111827', color: '#374151' }}>t</th>
            <th style={{ padding: '6px 8px', textAlign: 'left', borderBottom: '2px solid #111827', color: '#374151' }}>유형</th>
            <th style={{ padding: '6px 8px', textAlign: 'right', borderBottom: '2px solid #111827', color: '#374151' }}>현금흐름 CF<sub>t</sub></th>
            <th style={{ padding: '6px 8px', textAlign: 'right', borderBottom: '2px solid #111827', color: '#374151' }}>할인계수 (1+r)⁻ᵗ</th>
            <th style={{ padding: '6px 8px', textAlign: 'right', borderBottom: '2px solid #111827', color: '#374151' }}>현재가치 PV</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => {
            const tc = TYPE_COLOR[row.type] || TYPE_COLOR.other;
            return (
              <tr key={i} style={{ borderBottom: '1px solid #f3f4f6' }}>
                <td style={{ padding: '5px 8px', textAlign: 'right', fontFamily: 'ui-monospace, monospace', fontWeight: 700 }}>{row.t}</td>
                <td style={{ padding: '5px 8px' }}>
                  <span style={{
                    display: 'inline-block', padding: '1px 6px', borderRadius: 4,
                    background: tc.bg, color: tc.text, fontSize: '0.72rem', fontWeight: 700,
                  }}>{tc.label}</span>
                  {row.note && <span style={{ marginLeft: 6, fontSize: '0.74rem', color: '#6b7280' }}>{row.note}</span>}
                </td>
                <td style={{ padding: '5px 8px', textAlign: 'right', fontFamily: 'ui-monospace, monospace' }}>{fmt(row.amount)}</td>
                <td style={{ padding: '5px 8px', textAlign: 'right', fontFamily: 'ui-monospace, monospace', color: '#6b7280' }}>{row.df.toFixed(4)}</td>
                <td style={{ padding: '5px 8px', textAlign: 'right', fontFamily: 'ui-monospace, monospace', fontWeight: 700 }}>{fmt(row.pv)}</td>
              </tr>
            );
          })}
        </tbody>
        <tfoot>
          <tr>
            <td colSpan={4} style={{ padding: '8px 8px', textAlign: 'right', borderTop: '2px solid #111827', fontWeight: 800, fontSize: '0.88rem', color: '#1e40af' }}>
              ΣPV (총 현재가치)
            </td>
            <td style={{ padding: '8px 8px', textAlign: 'right', borderTop: '2px solid #111827', fontFamily: 'ui-monospace, monospace', fontWeight: 800, fontSize: '0.95rem', color: '#1e40af' }}>
              {fmt(totalPV)}
            </td>
          </tr>
        </tfoot>
      </table>
      {params.narration && (
        <p style={{ margin: '10px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const dcfTimelineTemplate = {
  name: 'dcf-timeline',
  version: 1,
  subjects: ['appraisal_practice', 'realestate'],
  helpText: 'DCF 타임라인 (연차별 CF · 할인계수 · PV 합산)',
  Component: DcfTimelineChart,
  schema: {
    type: 'object',
    required: ['cashflows'],
    properties: {
      scenario: { type: 'string' },
      method: { type: 'string' },
      discount_rate: { type: 'number' },
      cashflows: {
        type: 'array',
        minItems: 1,
        items: {
          type: 'object',
          required: ['amount'],
          properties: {
            year: { type: 'number' },
            amount: { type: 'number' },
            type: { enum: ['noi', 'reversion', 'capex', 'other'] },
            note: { type: 'string' },
          },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '5년 보유 후 매각 시나리오',
    method: 'DCF 5년 + 종기 복귀가치',
    discount_rate: 0.08,
    cashflows: [
      { year: 1, amount: 80000000, type: 'noi' },
      { year: 2, amount: 82400000, type: 'noi', note: '+3%' },
      { year: 3, amount: 84872000, type: 'noi', note: '+3%' },
      { year: 4, amount: 87418160, type: 'noi', note: '+3%' },
      { year: 5, amount: 90040705, type: 'noi', note: '+3%' },
      { year: 5, amount: 1287724357, type: 'reversion', note: '5년차 NOI × (1+r) / R, R=0.07' },
    ],
    narration: '운영기간 NOI + 5년차 말 매각 복귀가치를 모두 현재가치로 환원. 총 PV가 부동산 가치.',
  },
};
