// T-account 분개표 — 차변·대변 양쪽 정렬.
// HTML/CSS 기반 (SVG 불필요). 금액·합계 자동 정렬.

function fmt(n) {
  if (typeof n !== 'number') return n;
  return n.toLocaleString('ko-KR');
}

function TAccountChart({ params }) {
  const debits = params.debits || [];
  const credits = params.credits || [];
  const debitSum = debits.reduce((a, b) => a + (Number(b.amount) || 0), 0);
  const creditSum = credits.reduce((a, b) => a + (Number(b.amount) || 0), 0);
  const balanced = Math.abs(debitSum - creditSum) < 0.01;

  const cellStyle = (side) => ({
    padding: '6px 10px', fontSize: '0.82rem', color: '#111827',
    borderRight: side === 'debit' ? '2px solid #111827' : 'none',
  });

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12, maxWidth: 560 }}>
      {params.account_name && (
        <figcaption style={{ textAlign: 'center', fontSize: '0.95rem', fontWeight: 800, color: '#111827', marginBottom: 8 }}>
          {params.account_name}
        </figcaption>
      )}
      <table style={{ width: '100%', borderCollapse: 'collapse', tableLayout: 'fixed' }}>
        <thead>
          <tr>
            <th style={{ width: '50%', padding: '6px 10px', borderBottom: '2px solid #111827', borderRight: '2px solid #111827', fontSize: '0.82rem', color: '#374151', textAlign: 'left' }}>
              차변 (Debit) <span style={{ color: '#9ca3af', fontWeight: 400 }}>—  자산↑ 부채↓ 자본↓ 비용↑</span>
            </th>
            <th style={{ width: '50%', padding: '6px 10px', borderBottom: '2px solid #111827', fontSize: '0.82rem', color: '#374151', textAlign: 'left' }}>
              대변 (Credit) <span style={{ color: '#9ca3af', fontWeight: 400 }}>—  자산↓ 부채↑ 자본↑ 수익↑</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: Math.max(debits.length, credits.length) }).map((_, i) => {
            const d = debits[i];
            const c = credits[i];
            return (
              <tr key={i}>
                <td style={cellStyle('debit')}>
                  {d ? (
                    <span style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span>{d.label}</span>
                      <span style={{ fontFamily: 'ui-monospace, monospace', fontWeight: 600 }}>{fmt(d.amount)}</span>
                    </span>
                  ) : <span>&nbsp;</span>}
                </td>
                <td style={cellStyle('credit')}>
                  {c ? (
                    <span style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span>{c.label}</span>
                      <span style={{ fontFamily: 'ui-monospace, monospace', fontWeight: 600 }}>{fmt(c.amount)}</span>
                    </span>
                  ) : <span>&nbsp;</span>}
                </td>
              </tr>
            );
          })}
          <tr style={{ background: '#f9fafb' }}>
            <td style={{ ...cellStyle('debit'), borderTop: '1px solid #d1d5db', fontWeight: 700 }}>
              <span style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>합계</span>
                <span style={{ fontFamily: 'ui-monospace, monospace' }}>{fmt(debitSum)}</span>
              </span>
            </td>
            <td style={{ ...cellStyle('credit'), borderTop: '1px solid #d1d5db', fontWeight: 700 }}>
              <span style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>합계</span>
                <span style={{ fontFamily: 'ui-monospace, monospace' }}>{fmt(creditSum)}</span>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
      <div style={{ marginTop: 6, fontSize: '0.74rem', color: balanced ? '#047857' : '#b91c1c', textAlign: 'right', fontWeight: 700 }}>
        {balanced ? '✓ 대차 일치' : `⚠️ 차변·대변 불일치 (차 ${fmt(debitSum)} vs 대 ${fmt(creditSum)})`}
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const tAccountTemplate = {
  name: 't-account',
  version: 1,
  subjects: ['accounting'],
  helpText: 'T-계정 분개표 (차변·대변·합계 자동 정렬)',
  Component: TAccountChart,
  schema: {
    type: 'object',
    properties: {
      account_name: { type: 'string' },
      debits: {
        type: 'array',
        items: {
          type: 'object',
          required: ['label', 'amount'],
          properties: {
            label: { type: 'string' },
            amount: { type: 'number' },
          },
        },
      },
      credits: {
        type: 'array',
        items: {
          type: 'object',
          required: ['label', 'amount'],
          properties: {
            label: { type: 'string' },
            amount: { type: 'number' },
          },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    account_name: '현금 매입 거래 분개',
    debits: [{ label: '상품(자산)', amount: 100000 }],
    credits: [{ label: '현금(자산)', amount: 100000 }],
    narration: '상품 10만원 현금 매입 → 자산 내 교환.',
  },
};
