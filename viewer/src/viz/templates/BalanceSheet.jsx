// 재무상태표 — 좌(자산) / 우(부채+자본) 격자 시각화.
// K-IFRS 형식. 유동/비유동 자동 그룹핑.

function fmt(n) {
  if (typeof n !== 'number') return n || '';
  return n.toLocaleString('ko-KR');
}

function totalOf(items) {
  return (items || []).reduce((a, b) => a + (Number(b.amount) || 0), 0);
}

function renderGroup(title, items, color) {
  const sum = totalOf(items);
  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{
        padding: '4px 8px', background: color.bg, color: color.fg,
        fontSize: '0.78rem', fontWeight: 700, display: 'flex', justifyContent: 'space-between',
        borderRadius: 4,
      }}>
        <span>{title}</span>
        <span style={{ fontFamily: 'ui-monospace, monospace' }}>{fmt(sum)}</span>
      </div>
      {(items || []).map((it, i) => (
        <div key={i} style={{
          padding: '3px 16px', display: 'flex', justifyContent: 'space-between',
          fontSize: '0.78rem', color: '#374151',
        }}>
          <span>{it.label}</span>
          <span style={{ fontFamily: 'ui-monospace, monospace' }}>{fmt(it.amount)}</span>
        </div>
      ))}
    </div>
  );
}

function BalanceSheetChart({ params }) {
  const assets = params.assets || {};
  const liab = params.liabilities || {};
  const equity = params.equity || {};

  const currAssets = totalOf(assets.current);
  const nonCurrAssets = totalOf(assets.non_current);
  const totalAssets = currAssets + nonCurrAssets;

  const currLiab = totalOf(liab.current);
  const nonCurrLiab = totalOf(liab.non_current);
  const totalLiab = currLiab + nonCurrLiab;

  const totalEquity = totalOf(equity.items);
  const totalLiabEquity = totalLiab + totalEquity;

  const balanced = Math.abs(totalAssets - totalLiabEquity) < 0.01;

  const assetColor = { bg: '#dbeafe', fg: '#1e40af' };
  const liabColor = { bg: '#fee2e2', fg: '#991b1b' };
  const equityColor = { bg: '#d1fae5', fg: '#047857' };

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12, maxWidth: 720 }}>
      <figcaption style={{ textAlign: 'center', fontSize: '0.95rem', fontWeight: 800, color: '#111827', marginBottom: 4 }}>
        재무상태표
        {params.entity && <span style={{ fontWeight: 400, color: '#6b7280', marginLeft: 6 }}>· {params.entity}</span>}
        {params.as_of && <span style={{ fontWeight: 400, color: '#6b7280', marginLeft: 6 }}>· {params.as_of}</span>}
      </figcaption>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
        {/* 좌측: 자산 */}
        <div style={{ borderRight: '2px solid #d1d5db', paddingRight: 12 }}>
          <div style={{ fontSize: '0.85rem', fontWeight: 800, color: '#1e40af', marginBottom: 6 }}>
            자산 (Assets)
          </div>
          {(assets.current || []).length > 0 && renderGroup('유동자산', assets.current, assetColor)}
          {(assets.non_current || []).length > 0 && renderGroup('비유동자산', assets.non_current, assetColor)}
          <div style={{
            marginTop: 6, padding: '6px 8px', borderTop: '2px solid #1e40af',
            display: 'flex', justifyContent: 'space-between', fontWeight: 800,
            fontSize: '0.88rem', color: '#1e40af',
          }}>
            <span>자산 총계</span>
            <span style={{ fontFamily: 'ui-monospace, monospace' }}>{fmt(totalAssets)}</span>
          </div>
        </div>
        {/* 우측: 부채 + 자본 */}
        <div style={{ paddingLeft: 0 }}>
          <div style={{ fontSize: '0.85rem', fontWeight: 800, color: '#991b1b', marginBottom: 6 }}>
            부채 (Liabilities)
          </div>
          {(liab.current || []).length > 0 && renderGroup('유동부채', liab.current, liabColor)}
          {(liab.non_current || []).length > 0 && renderGroup('비유동부채', liab.non_current, liabColor)}
          <div style={{
            marginTop: 4, padding: '6px 8px', borderTop: '1px dashed #991b1b',
            display: 'flex', justifyContent: 'space-between', fontWeight: 700,
            fontSize: '0.82rem', color: '#991b1b',
          }}>
            <span>부채 총계</span>
            <span style={{ fontFamily: 'ui-monospace, monospace' }}>{fmt(totalLiab)}</span>
          </div>
          <div style={{ fontSize: '0.85rem', fontWeight: 800, color: '#047857', marginTop: 12, marginBottom: 6 }}>
            자본 (Equity)
          </div>
          {(equity.items || []).length > 0 && renderGroup('자본 항목', equity.items, equityColor)}
          <div style={{
            marginTop: 4, padding: '6px 8px', borderTop: '1px dashed #047857',
            display: 'flex', justifyContent: 'space-between', fontWeight: 700,
            fontSize: '0.82rem', color: '#047857',
          }}>
            <span>자본 총계</span>
            <span style={{ fontFamily: 'ui-monospace, monospace' }}>{fmt(totalEquity)}</span>
          </div>
          <div style={{
            marginTop: 8, padding: '6px 8px', borderTop: '2px solid #6b7280',
            display: 'flex', justifyContent: 'space-between', fontWeight: 800,
            fontSize: '0.88rem', color: '#111827',
          }}>
            <span>부채 + 자본 총계</span>
            <span style={{ fontFamily: 'ui-monospace, monospace' }}>{fmt(totalLiabEquity)}</span>
          </div>
        </div>
      </div>
      <div style={{ marginTop: 8, fontSize: '0.74rem', color: balanced ? '#047857' : '#b91c1c', textAlign: 'right', fontWeight: 700 }}>
        {balanced ? '✓ 자산 = 부채 + 자본' : `⚠️ 불일치 (자산 ${fmt(totalAssets)} ≠ 부채+자본 ${fmt(totalLiabEquity)})`}
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const balanceSheetTemplate = {
  name: 'balance-sheet',
  version: 1,
  subjects: ['accounting'],
  helpText: '재무상태표 (자산/부채/자본 격자, 회계등식 검증)',
  Component: BalanceSheetChart,
  schema: {
    type: 'object',
    properties: {
      entity: { type: 'string' },
      as_of: { type: 'string' },
      assets: {
        type: 'object',
        properties: {
          current: { type: 'array', items: { type: 'object', required: ['label', 'amount'], properties: { label: { type: 'string' }, amount: { type: 'number' } } } },
          non_current: { type: 'array', items: { type: 'object', required: ['label', 'amount'], properties: { label: { type: 'string' }, amount: { type: 'number' } } } },
        },
      },
      liabilities: {
        type: 'object',
        properties: {
          current: { type: 'array', items: { type: 'object', required: ['label', 'amount'], properties: { label: { type: 'string' }, amount: { type: 'number' } } } },
          non_current: { type: 'array', items: { type: 'object', required: ['label', 'amount'], properties: { label: { type: 'string' }, amount: { type: 'number' } } } },
        },
      },
      equity: {
        type: 'object',
        properties: {
          items: { type: 'array', items: { type: 'object', required: ['label', 'amount'], properties: { label: { type: 'string' }, amount: { type: 'number' } } } },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    entity: '예시회사',
    as_of: '2025-12-31',
    assets: {
      current: [{ label: '현금및현금성자산', amount: 50000 }, { label: '매출채권', amount: 30000 }],
      non_current: [{ label: '유형자산', amount: 120000 }],
    },
    liabilities: {
      current: [{ label: '매입채무', amount: 25000 }],
      non_current: [{ label: '장기차입금', amount: 75000 }],
    },
    equity: {
      items: [{ label: '자본금', amount: 50000 }, { label: '이익잉여금', amount: 50000 }],
    },
    narration: '자산 200,000 = 부채 100,000 + 자본 100,000 — 회계등식 성립.',
  },
};
