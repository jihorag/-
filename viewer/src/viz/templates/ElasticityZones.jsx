// 수요곡선 상 탄력성 구간 시각화.
// 선형 D 곡선: 상단=탄력적 / 중간점=단위탄력 / 하단=비탄력.
// |E|=1 점에 마커 + 영역 색칠.

const W = 480, H = 360, PADL = 50, PADB = 50, PADT = 24, PADR = 30;
const PW = W - PADL - PADR;
const PH = H - PADT - PADB;

function nx(q) { return PADL + q * PW; }
function ny(p) { return PADT + (1 - p) * PH; }

// D: P = a - b*Q. 단위탄력 점 = (a/2b, a/2)
const a = 0.9, b = 0.85;
const dP = (q) => a - b * q;

function ElasticityZonesChart({ params }) {
  const xUnitElastic = a / (2 * b);  // 중간점
  const yUnitElastic = a / 2;
  const showZones = params.show_zones !== false;
  const showLabels = params.show_labels !== false;
  const markerQ = typeof params.point_q === 'number' ? params.point_q : null;
  const markerP = markerQ !== null ? dP(markerQ) : null;
  const markerE = markerQ !== null ? (b * markerQ) / Math.max(0.001, (a - b * markerQ)) * -1 : null;
  // E = -(dQ/dP) * (P/Q). For P = a-bQ → dQ/dP = -1/b. So |E| = (1/b)*(P/Q) = (a-bQ)/(bQ)

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12 }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 6 }}>
          📊 {params.scenario}
        </figcaption>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', maxWidth: 520, display: 'block' }}>
        <line x1={nx(0)} y1={ny(0)} x2={nx(1)} y2={ny(0)} stroke="#9ca3af" strokeWidth={1.5} />
        <line x1={nx(0)} y1={ny(0)} x2={nx(0)} y2={ny(1)} stroke="#9ca3af" strokeWidth={1.5} />
        <text x={nx(1) + 2} y={ny(0) + 4} fontSize={12} fill="#374151">Q</text>
        <text x={nx(0) - 6} y={ny(1) - 6} fontSize={12} fill="#374151" textAnchor="end">P</text>

        {/* 영역 색칠 — 상단(탄력) / 하단(비탄력) */}
        {showZones && (
          <>
            <polygon points={`${nx(0)},${ny(a)} ${nx(xUnitElastic)},${ny(yUnitElastic)} ${nx(0)},${ny(yUnitElastic)}`}
              fill="#bbf7d0" fillOpacity={0.4} />
            <polygon points={`${nx(0)},${ny(yUnitElastic)} ${nx(xUnitElastic)},${ny(yUnitElastic)} ${nx(xUnitElastic)},${ny(0)} ${nx(0)},${ny(0)}`}
              fill="#fee2e2" fillOpacity={0.4} />
            <polygon points={`${nx(xUnitElastic)},${ny(yUnitElastic)} ${nx(a/b)},${ny(0)} ${nx(xUnitElastic)},${ny(0)}`}
              fill="#fecaca" fillOpacity={0.5} />
          </>
        )}

        {/* D 곡선 */}
        <line x1={nx(0)} y1={ny(a)} x2={nx(a/b)} y2={ny(0)} stroke="#dc2626" strokeWidth={2.4} />
        <text x={nx(a/b) - 4} y={ny(0) - 8} fontSize={12} fontWeight={700} fill="#dc2626" textAnchor="end">D</text>

        {/* 중간점 (E=1) */}
        <circle cx={nx(xUnitElastic)} cy={ny(yUnitElastic)} r={5} fill="#fbbf24" stroke="#92400e" strokeWidth={2} />
        <text x={nx(xUnitElastic) + 8} y={ny(yUnitElastic) - 6} fontSize={11} fontWeight={700} fill="#92400e">|E|=1</text>
        <line x1={nx(0)} y1={ny(yUnitElastic)} x2={nx(xUnitElastic)} y2={ny(yUnitElastic)} stroke="#fbbf24" strokeWidth={0.8} strokeDasharray="2 3" />
        <line x1={nx(xUnitElastic)} y1={ny(0)} x2={nx(xUnitElastic)} y2={ny(yUnitElastic)} stroke="#fbbf24" strokeWidth={0.8} strokeDasharray="2 3" />

        {/* 라벨 — 상단/하단 구간 */}
        {showLabels && (
          <>
            <text x={nx(xUnitElastic * 0.35)} y={ny((yUnitElastic + a) / 2)} fontSize={11} fontWeight={700} fill="#15803d" textAnchor="middle">
              탄력적 |E|&gt;1
            </text>
            <text x={nx(xUnitElastic * 0.45 + 0.18)} y={ny(yUnitElastic * 0.45)} fontSize={11} fontWeight={700} fill="#b91c1c" textAnchor="middle">
              비탄력 |E|&lt;1
            </text>
          </>
        )}

        {/* 임의 점 마커 (optional) */}
        {markerQ !== null && markerP !== null && (
          <g>
            <circle cx={nx(markerQ)} cy={ny(markerP)} r={5} fill="#1f2937" />
            <text x={nx(markerQ) + 8} y={ny(markerP) - 6} fontSize={11} fontWeight={800} fill="#111827">
              |E|≈{Math.abs(markerE).toFixed(2)}
            </text>
          </g>
        )}
      </svg>
      <div style={{ marginTop: 6, fontSize: '0.78rem', color: '#374151', lineHeight: 1.55 }}>
        <div>• 선형 D 곡선에서 <strong>중간점 = 단위탄력</strong> (|E|=1)</div>
        <div>• 상단 (높은 가격) → <strong style={{ color: '#15803d' }}>탄력적</strong> (가격 변화에 수요 민감)</div>
        <div>• 하단 (낮은 가격) → <strong style={{ color: '#b91c1c' }}>비탄력</strong> (수요 둔감)</div>
        <div>• 같은 곡선이라도 가격대에 따라 탄력성이 달라짐</div>
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const elasticityZonesTemplate = {
  name: 'elasticity-zones',
  version: 1,
  subjects: ['economics'],
  helpText: '수요곡선 위 탄력성 구간 (탄력/단위탄력/비탄력)',
  Component: ElasticityZonesChart,
  schema: {
    type: 'object',
    properties: {
      scenario: { type: 'string' },
      show_zones: { type: 'boolean' },
      show_labels: { type: 'boolean' },
      point_q: { type: 'number' },  // 임의 점 Q (탄력성 계산)
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '선형 수요곡선 — 가격대별 탄력성',
    show_zones: true,
    show_labels: true,
    point_q: 0.3,
    narration: '중간점 기준 위쪽은 탄력적, 아래쪽은 비탄력. 같은 D 곡선이라도 가격에 따라 탄력성이 다름.',
  },
};
