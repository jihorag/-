// 손익계산서 — stepdown 형태.
// 매출 → 매출원가 → 매출총이익 → 판관비 → 영업이익 → 영업외 → 법인세 → 당기순이익.
// 각 step은 type(revenue|cost|expense|tax|subtotal|net)에 따라 색 자동.

function fmt(n) {
  if (typeof n !== 'number') return n || '';
  return n.toLocaleString('ko-KR');
}

const TYPE_STYLE = {
  revenue:  { color: '#047857', sign: '+', bold: false, bg: '#fff' },
  cost:     { color: '#b91c1c', sign: '−', bold: false, bg: '#fff' },
  expense:  { color: '#b91c1c', sign: '−', bold: false, bg: '#fff' },
  tax:      { color: '#b91c1c', sign: '−', bold: false, bg: '#fff' },
  income:   { color: '#047857', sign: '+', bold: false, bg: '#fff' },
  subtotal: { color: '#1e40af', sign: '=', bold: true,  bg: '#eff6ff' },
  net:      { color: '#111827', sign: '=', bold: true,  bg: '#f3f4f6' },
};

function IncomeStatementChart({ params }) {
  const items = params.items || [];

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12, maxWidth: 640 }}>
      <figcaption style={{ textAlign: 'center', fontSize: '0.95rem', fontWeight: 800, color: '#111827', marginBottom: 6 }}>
        손익계산서
        {params.entity && <span style={{ fontWeight: 400, color: '#6b7280', marginLeft: 6 }}>· {params.entity}</span>}
        {params.period && <span style={{ fontWeight: 400, color: '#6b7280', marginLeft: 6 }}>· {params.period}</span>}
      </figcaption>
      <div>
        {items.map((it, i) => {
          const t = TYPE_STYLE[it.type] || TYPE_STYLE.expense;
          const indent = Math.min(it.indent || 0, 3) * 16;
          return (
            <div key={i} style={{
              padding: t.bold ? '6px 10px' : '4px 10px',
              paddingLeft: 10 + indent,
              background: t.bg,
              borderTop: t.bold ? `1px solid ${t.color}` : 'none',
              borderBottom: t.bold ? `1px solid ${t.color}` : '1px dashed #f3f4f6',
              display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              fontSize: t.bold ? '0.88rem' : '0.82rem',
              fontWeight: t.bold ? 800 : 500,
              color: t.color,
            }}>
              <span>
                <span style={{ display: 'inline-block', width: 14, color: t.color, fontWeight: 700 }}>{t.sign}</span>
                {it.label}
              </span>
              <span style={{ fontFamily: 'ui-monospace, monospace', fontWeight: t.bold ? 800 : 600 }}>
                {fmt(it.amount)}
              </span>
            </div>
          );
        })}
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const incomeStatementTemplate = {
  name: 'income-statement',
  version: 1,
  subjects: ['accounting'],
  helpText: '손익계산서 (stepdown — 매출→당기순이익)',
  Component: IncomeStatementChart,
  schema: {
    type: 'object',
    properties: {
      entity: { type: 'string' },
      period: { type: 'string' },
      items: {
        type: 'array',
        minItems: 1,
        items: {
          type: 'object',
          required: ['label', 'amount', 'type'],
          properties: {
            label: { type: 'string' },
            amount: { type: 'number' },
            type: { enum: ['revenue', 'cost', 'expense', 'tax', 'income', 'subtotal', 'net'] },
            indent: { type: 'number' },
          },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    entity: '예시회사',
    period: '2025년',
    items: [
      { label: '매출액',        amount: 1000000, type: 'revenue' },
      { label: '매출원가',      amount: 600000,  type: 'cost' },
      { label: '매출총이익',    amount: 400000,  type: 'subtotal' },
      { label: '판매비와관리비', amount: 200000, type: 'expense' },
      { label: '영업이익',      amount: 200000,  type: 'subtotal' },
      { label: '영업외수익',    amount: 30000,   type: 'income' },
      { label: '영업외비용',    amount: 20000,   type: 'expense' },
      { label: '법인세비용차감전순이익', amount: 210000, type: 'subtotal' },
      { label: '법인세비용',    amount: 50000,   type: 'tax' },
      { label: '당기순이익',    amount: 160000,  type: 'net' },
    ],
    narration: '영업이익률 20%, 순이익률 16% — 영업외 손익 거의 균형.',
  },
};
