// 거래사례 보정 단계표 — 감정평가실무 비교방식.
// 기준 거래단가 → 사정보정·시점수정·지역요인·개별요인 보정 → 비준가액.
// 각 단계 % 와 누적 결과 자동 표시.

function fmt(n) {
  if (typeof n !== 'number') return n || '—';
  return Math.round(n).toLocaleString('ko-KR');
}

function pct(n) {
  if (typeof n !== 'number') return n || '—';
  return (n > 0 ? '+' : '') + (n * 100).toFixed(2) + '%';
}

function SalesAdjustmentChart({ params }) {
  const basePrice = Number(params.base_price) || 0;
  const adjustments = params.adjustments || [];

  // 누적 계산
  const rows = [];
  let cur = basePrice;
  rows.push({
    label: params.base_label || '기준 거래단가',
    factor: '—',
    rate: '—',
    result: cur,
    reason: params.base_note || '',
  });
  for (const adj of adjustments) {
    const rate = Number(adj.rate) || 0;
    cur = cur * (1 + rate);
    rows.push({
      label: adj.factor,
      factor: adj.factor,
      rate: rate,
      result: cur,
      reason: adj.reason || '',
    });
  }

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12, overflowX: 'auto' }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 6 }}>
          🏠 {params.scenario}
        </figcaption>
      )}
      {params.method && (
        <div style={{ fontSize: '0.78rem', color: '#6b7280', marginBottom: 8 }}>
          {params.method}{params.case_ref ? ` · ${params.case_ref}` : ''}
        </div>
      )}
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', minWidth: 520 }}>
        <thead>
          <tr style={{ background: '#f9fafb' }}>
            <th style={{ padding: '6px 10px', textAlign: 'left', borderBottom: '2px solid #111827', color: '#374151' }}>단계</th>
            <th style={{ padding: '6px 10px', textAlign: 'right', borderBottom: '2px solid #111827', color: '#374151' }}>보정률</th>
            <th style={{ padding: '6px 10px', textAlign: 'right', borderBottom: '2px solid #111827', color: '#374151' }}>누적 단가 (원/㎡)</th>
            <th style={{ padding: '6px 10px', textAlign: 'left', borderBottom: '2px solid #111827', color: '#374151' }}>적용 사유</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} style={{ borderBottom: '1px solid #f3f4f6' }}>
              <td style={{
                padding: '6px 10px',
                fontWeight: 700,
                color: i === 0 ? '#1e40af' : '#374151',
              }}>
                {i === 0 ? '🔹 ' : '↓ '}{row.label}
              </td>
              <td style={{
                padding: '6px 10px', textAlign: 'right', fontFamily: 'ui-monospace, monospace',
                fontWeight: 700,
                color: typeof row.rate === 'number' ? (row.rate > 0 ? '#15803d' : row.rate < 0 ? '#b91c1c' : '#6b7280') : '#6b7280',
              }}>
                {pct(row.rate)}
              </td>
              <td style={{
                padding: '6px 10px', textAlign: 'right', fontFamily: 'ui-monospace, monospace',
                fontWeight: i === 0 ? 600 : 700,
              }}>
                {fmt(row.result)}
              </td>
              <td style={{ padding: '6px 10px', color: '#475569', fontSize: '0.78rem' }}>
                {row.reason || <span style={{ color: '#d1d5db' }}>—</span>}
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <td colSpan={2} style={{
              padding: '10px 10px', textAlign: 'right',
              borderTop: '2px solid #111827', fontWeight: 800, fontSize: '0.92rem', color: '#1e40af',
            }}>
              ➡ 비준가액 (원/㎡)
            </td>
            <td style={{
              padding: '10px 10px', textAlign: 'right',
              borderTop: '2px solid #111827', fontFamily: 'ui-monospace, monospace',
              fontWeight: 800, fontSize: '1.0rem', color: '#7c2d12', background: '#fef3c7',
            }}>
              {fmt(cur)}
            </td>
            <td style={{ borderTop: '2px solid #111827' }}></td>
          </tr>
        </tfoot>
      </table>
      {/* 총 보정률 자동 자막 */}
      {basePrice > 0 && (
        <div style={{ marginTop: 6, fontSize: '0.78rem', color: '#374151' }}>
          • 총 보정률: <strong>{pct((cur - basePrice) / basePrice)}</strong>
          {' '}({adjustments.length}단계 누적)
        </div>
      )}
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const salesAdjustmentTemplate = {
  name: 'sales-adjustment',
  version: 1,
  subjects: ['appraisal_practice', 'realestate'],
  helpText: '거래사례 보정 단계표 (사정·시점·지역·개별 누적)',
  Component: SalesAdjustmentChart,
  schema: {
    type: 'object',
    required: ['base_price', 'adjustments'],
    properties: {
      scenario: { type: 'string' },
      method: { type: 'string' },
      case_ref: { type: 'string' },
      base_price: { type: 'number' },
      base_label: { type: 'string' },
      base_note: { type: 'string' },
      adjustments: {
        type: 'array',
        items: {
          type: 'object',
          required: ['factor', 'rate'],
          properties: {
            factor: { type: 'string' },     // '사정보정', '시점수정', '지역요인', '개별요인'
            rate: { type: 'number' },       // 0.05 = +5%
            reason: { type: 'string' },
          },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '인근 거래사례를 기준으로 대상 토지 비준가액 산정',
    method: '비교방식 — 거래사례비교법',
    case_ref: '사례 #3 (2024-08)',
    base_price: 2500000,
    base_label: '거래단가 (원/㎡)',
    base_note: '시장 정상거래',
    adjustments: [
      { factor: '사정보정', rate: 0,     reason: '정상거래로 보정 불필요' },
      { factor: '시점수정', rate: 0.03,  reason: '8개월 경과, 지가지수 +3%' },
      { factor: '지역요인', rate: -0.05, reason: '대상지가 사례지보다 상권 미약 (-5%)' },
      { factor: '개별요인', rate: 0.08,  reason: '도로조건·획지조건 우세 (+8%)' },
    ],
    narration: '총 보정률 +5.9% — 비준가액 약 2,648,000 원/㎡. 적용 우선순위 (사정→시점→지역→개별) 준수.',
  },
};
