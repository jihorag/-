// Phillips 곡선 — 단기 우하향 + 장기 수직 + 기대 인플레이션 조정.
// 의미 파라미터: 단·장기 곡선 표시, 기대 shift (자연실업률 전후).

const W = 480, H = 360, PADL = 56, PADB = 50, PADT = 24, PADR = 30;
const PW = W - PADL - PADR;
const PH = H - PADT - PADB;

function nx(u) { return PADL + u * PW; }
function ny(p) { return PADT + (1 - p) * PH; }

function PhillipsCurveChart({ params }) {
  const naturalU = typeof params.natural_unemployment === 'number' ? params.natural_unemployment : 0.5;
  const expectedPi = typeof params.expected_inflation === 'number' ? params.expected_inflation : 0.0;
  const shortRunVisible = params.short_run_visible !== false;
  const longRunVisible = params.long_run_visible !== false;
  const shiftScenario = params.shift;  // {direction: 'up'|'down', magnitude: 'small|moderate|large', reason}

  const MAG = { small: 0.10, moderate: 0.18, large: 0.28 };
  const shiftAmt = shiftScenario ? (MAG[shiftScenario.magnitude] || MAG.moderate) * (shiftScenario.direction === 'up' ? 1 : -1) : 0;
  const newExpectedPi = expectedPi + shiftAmt;

  // 단기 Phillips: π = πᵉ + slope*(u_n - u)  (slope > 0 → 우하향)
  const slope = -1.4;
  const initialPhillips = (u) => expectedPi + slope * (u - naturalU);
  const shiftedPhillips = (u) => newExpectedPi + slope * (u - naturalU);

  const buildLine = (fn) => {
    const pts = [];
    for (let i = 0; i <= 40; i++) {
      const u = i / 40;
      const p = fn(u) + 0.5;  // 정규화 (π 축 중앙 = 0)
      pts.push([nx(u), ny(p)]);
    }
    return pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');
  };

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12 }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 6 }}>
          📊 {params.scenario}
        </figcaption>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', maxWidth: 520, display: 'block' }}>
        {/* 축 */}
        <line x1={nx(0)} y1={ny(0)} x2={nx(1)} y2={ny(0)} stroke="#9ca3af" strokeWidth={1.5} />
        <line x1={nx(0)} y1={ny(0)} x2={nx(0)} y2={ny(1)} stroke="#9ca3af" strokeWidth={1.5} />
        <text x={nx(1) + 2} y={ny(0) + 4} fontSize={12} fill="#374151">u (실업률)</text>
        <text x={nx(0) - 6} y={ny(1) - 6} fontSize={12} fill="#374151" textAnchor="end">π (인플레이션)</text>

        {/* π = 0 기준선 */}
        <line x1={nx(0)} y1={ny(0.5)} x2={nx(1)} y2={ny(0.5)} stroke="#d1d5db" strokeWidth={0.8} strokeDasharray="2 3" />

        {/* 장기 (자연실업률 수직선) */}
        {longRunVisible && (
          <g>
            <line x1={nx(naturalU)} y1={ny(0)} x2={nx(naturalU)} y2={ny(1)} stroke="#7c3aed" strokeWidth={2} />
            <text x={nx(naturalU) + 4} y={ny(0.92)} fontSize={11} fontWeight={700} fill="#7c3aed">LRPC</text>
            <text x={nx(naturalU)} y={ny(0) + 14} fontSize={11} fill="#374151" textAnchor="middle">u_n</text>
          </g>
        )}

        {/* 단기 곡선 — 이전 (shift 있을 때 점선) */}
        {shortRunVisible && shiftScenario && (
          <g>
            <path d={buildLine(initialPhillips)} fill="none" stroke="#fca5a5" strokeWidth={1.5} strokeDasharray="4 4" />
            <text x={nx(0.85)} y={ny(initialPhillips(0.85) + 0.5) + 14} fontSize={10} fill="#fca5a5">SRPC₀</text>
          </g>
        )}
        {/* 단기 곡선 — 현재 */}
        {shortRunVisible && (
          <g>
            <path d={buildLine(shiftedPhillips)} fill="none" stroke="#dc2626" strokeWidth={2.2} />
            <text x={nx(0.85)} y={ny(shiftedPhillips(0.85) + 0.5) + 14} fontSize={11} fontWeight={700} fill="#dc2626">{shiftScenario ? 'SRPC₁' : 'SRPC'}</text>
          </g>
        )}

        {/* 자연실업률·기대인플레이션 교점 마커 */}
        {longRunVisible && shortRunVisible && (
          <circle cx={nx(naturalU)} cy={ny(newExpectedPi + 0.5)} r={5} fill="#111827" />
        )}
      </svg>
      {/* 자동 자막 */}
      <div style={{ marginTop: 6, fontSize: '0.78rem', color: '#374151', lineHeight: 1.55 }}>
        <div>• 자연실업률 u_n = <strong>{(naturalU * 100).toFixed(0)}%</strong></div>
        <div>• 기대 인플레이션 πᵉ = <strong>{(newExpectedPi * 100).toFixed(1)}%</strong></div>
        {shiftScenario && (
          <div style={{ color: shiftScenario.direction === 'up' ? '#b91c1c' : '#15803d', fontWeight: 700 }}>
            ⇒ SRPC {shiftScenario.direction === 'up' ? '상방' : '하방'} 이동 {shiftScenario.reason && `— ${shiftScenario.reason}`}
          </div>
        )}
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const phillipsCurveTemplate = {
  name: 'phillips-curve',
  version: 1,
  subjects: ['economics'],
  helpText: 'Phillips 곡선 (단기 우하향·장기 수직·기대 조정 shift)',
  Component: PhillipsCurveChart,
  schema: {
    type: 'object',
    properties: {
      scenario: { type: 'string' },
      natural_unemployment: { type: 'number' },
      expected_inflation: { type: 'number' },
      short_run_visible: { type: 'boolean' },
      long_run_visible: { type: 'boolean' },
      shift: {
        type: 'object',
        properties: {
          direction: { enum: ['up', 'down'] },
          magnitude: { enum: ['small', 'moderate', 'large'], default: 'moderate' },
          reason: { type: 'string' },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '기대 인플레이션 상승 → SRPC 상방 이동',
    natural_unemployment: 0.5,
    expected_inflation: 0.0,
    short_run_visible: true,
    long_run_visible: true,
    shift: { direction: 'up', magnitude: 'moderate', reason: '국제유가 충격 → 기대 πᵉ ↑' },
    narration: 'SRPC가 위로 평행이동, LRPC(자연실업률 수직선)는 불변. 장기적으로 자연실업률 점으로 회귀.',
  },
};
