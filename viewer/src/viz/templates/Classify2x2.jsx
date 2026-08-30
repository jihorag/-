// 2×2 분류표 — 두 축(각 low/high)으로 나뉘는 4분면 분류.
// 경합성×배제성(재화 분류), 거래전후×정보우위(비대칭정보) 등 순수 텍스트 분류에 사용.
// 좌표 계산 없음 — CSS grid 로 4칸만 고정 배치.

function Classify2x2Chart({ params }) {
  const xAxis = params.x_axis || {};
  const yAxis = params.y_axis || {};
  const cells = params.cells || [];
  const find = (x, y) => cells.find((c) => c.x === x && c.y === y);

  // 화면상 위→아래는 high→low (2사분면 관습과 동일)
  const grid = [
    [find('low', 'high'), find('high', 'high')],
    [find('low', 'low'), find('high', 'low')],
  ];

  const cellBox = (c) => (
    <div style={{
      border: '1px solid #e5e7eb', borderRadius: 8, padding: '10px 12px',
      minHeight: 64, background: '#f9fafb',
    }}>
      {c ? (
        <>
          <div style={{ fontSize: '0.86rem', fontWeight: 800, color: '#111827' }}>{c.title}</div>
          {c.note && <div style={{ fontSize: '0.76rem', color: '#6b7280', marginTop: 4 }}>{c.note}</div>}
        </>
      ) : <span style={{ color: '#d1d5db', fontSize: '0.78rem' }}>—</span>}
    </div>
  );

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12, maxWidth: 480 }}>
      {params.caption && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 8 }}>
          {params.caption}
        </figcaption>
      )}
      <div style={{ display: 'grid', gridTemplateColumns: '64px 1fr 1fr', gridTemplateRows: '20px 1fr 1fr', gap: 6 }}>
        <div />
        <div style={{ textAlign: 'center', fontSize: '0.74rem', color: '#9ca3af' }}>{xAxis.low}</div>
        <div style={{ textAlign: 'center', fontSize: '0.74rem', color: '#9ca3af' }}>{xAxis.high}</div>

        <div style={{ writingMode: 'vertical-rl', textAlign: 'center', fontSize: '0.74rem', color: '#9ca3af', gridRow: '2 / 4' }}>
          {yAxis.label}
        </div>
        {cellBox(grid[0][0])}
        {cellBox(grid[0][1])}
        {cellBox(grid[1][0])}
        {cellBox(grid[1][1])}
      </div>
      <div style={{ marginTop: 6, fontSize: '0.72rem', color: '#9ca3af', textAlign: 'center' }}>
        ↓ {yAxis.label} · → {xAxis.label}
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const classify2x2Template = {
  name: 'classify-2x2',
  version: 1,
  subjects: ['economics', 'accounting', 'civil', 'law', 'appraisal_law'],
  helpText: '두 기준으로 4분면 분류 (배제성×경합성, 거래 전/후×정보우위 등) — 그래프 아닌 분류 개념용, 반드시 2×2(4칸)만',
  Component: Classify2x2Chart,
  schema: {
    type: 'object',
    required: ['x_axis', 'y_axis', 'cells'],
    properties: {
      x_axis: {
        type: 'object', required: ['label', 'low', 'high'],
        properties: { label: { type: 'string' }, low: { type: 'string' }, high: { type: 'string' } },
      },
      y_axis: {
        type: 'object', required: ['label', 'low', 'high'],
        properties: { label: { type: 'string' }, low: { type: 'string' }, high: { type: 'string' } },
      },
      cells: {
        type: 'array', minItems: 4,
        items: {
          type: 'object', required: ['x', 'y', 'title'],
          properties: {
            x: { enum: ['low', 'high'] },
            y: { enum: ['low', 'high'] },
            title: { type: 'string' },
            note: { type: 'string' },
          },
        },
      },
      caption: { type: 'string' },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    caption: '재화의 분류 — 경합성 × 배제성',
    x_axis: { label: '경합성', low: '비경합', high: '경합' },
    y_axis: { label: '배제성', low: '비배제', high: '배제' },
    cells: [
      { x: 'low', y: 'low', title: '공공재', note: '국방·등대' },
      { x: 'high', y: 'low', title: '공유자원', note: '공유지의 비극' },
      { x: 'low', y: 'high', title: '클럽재', note: '케이블TV' },
      { x: 'high', y: 'high', title: '사적재', note: '일반 상품' },
    ],
    narration: '배제성·경합성 조합에 따라 재화가 4가지로 분류됨.',
  },
};
