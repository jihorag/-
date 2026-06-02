// 무차별곡선 + 예산선 + 최적 소비점.
// Cobb-Douglas: U = X^a * Y^(1-a) → MRS = a/(1-a) * Y/X
// 예산: PxX + PyY = M → Y = M/Py - (Px/Py)X

const W = 480, H = 360, PADL = 50, PADB = 50, PADT = 24, PADR = 30;
const PW = W - PADL - PADR;
const PH = H - PADT - PADB;

function nx(x) { return PADL + x * PW; }
function ny(y) { return PADT + (1 - y) * PH; }

function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

function IndifferenceBudgetChart({ params }) {
  // 정규화 가정 — 0~1
  const alpha = clamp(params.preference_alpha ?? 0.5, 0.1, 0.9);  // X 선호 비중
  const pxOverPy = clamp(params.price_ratio ?? 1, 0.2, 5);         // Px/Py
  const incomeOverPy = clamp(params.income_over_py ?? 1.0, 0.3, 2); // M/Py

  // 예산선: Y = M/Py - (Px/Py)*X
  const yIntercept = incomeOverPy;
  const xIntercept = incomeOverPy / pxOverPy;

  // 최적: 한계대체율 MRS = Px/Py
  // Cobb-Douglas → X* = αM/Px, Y* = (1-α)M/Py
  const xStar = alpha * incomeOverPy / pxOverPy;
  const yStar = (1 - alpha) * incomeOverPy;
  const uStar = Math.pow(xStar, alpha) * Math.pow(yStar, 1 - alpha);

  // 무차별곡선 (U = const): Y = (U / X^α)^(1/(1-α))
  const indifferenceY = (x, U) => Math.pow(U / Math.pow(x, alpha), 1 / (1 - alpha));

  // 곡선 path 빌더 (지정한 U 값에 대해)
  const buildIC = (U) => {
    const pts = [];
    for (let i = 1; i <= 80; i++) {
      const x = 0.02 + (1.4 - 0.02) * (i / 80);
      const y = indifferenceY(x, U);
      if (y > 1.5 || isNaN(y)) continue;
      pts.push([nx(clamp(x, 0, 1)), ny(clamp(y, 0, 1))]);
    }
    return pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');
  };

  // 보조 IC: 낮은 U, 높은 U
  const uLow = uStar * 0.7;
  const uHigh = uStar * 1.3;

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
        <text x={nx(1) + 2} y={ny(0) + 4} fontSize={12} fill="#374151">{params.x_label || 'X'}</text>
        <text x={nx(0) - 6} y={ny(1) - 6} fontSize={12} fill="#374151" textAnchor="end">{params.y_label || 'Y'}</text>

        {/* 보조 IC */}
        <path d={buildIC(uLow)} fill="none" stroke="#fed7aa" strokeWidth={1.5} strokeDasharray="3 3" />
        <path d={buildIC(uHigh)} fill="none" stroke="#fdba74" strokeWidth={1.5} strokeDasharray="3 3" />

        {/* 최적 IC (U*) */}
        <path d={buildIC(uStar)} fill="none" stroke="#f97316" strokeWidth={2.2} />
        <text x={nx(clamp(xStar + 0.18, 0, 0.95))} y={ny(clamp(indifferenceY(xStar + 0.18, uStar), 0, 1)) - 4} fontSize={11} fontWeight={700} fill="#f97316">U*</text>

        {/* 예산선 */}
        {xIntercept <= 1 && yIntercept <= 1 && (
          <line x1={nx(0)} y1={ny(clamp(yIntercept, 0, 1))} x2={nx(clamp(xIntercept, 0, 1))} y2={ny(0)}
            stroke="#1d4ed8" strokeWidth={2.2} />
        )}
        <text x={nx(clamp(xIntercept * 0.55, 0.05, 0.9))} y={ny(clamp(yIntercept * 0.55, 0.05, 0.95)) - 6} fontSize={11} fontWeight={700} fill="#1d4ed8">예산선</text>

        {/* 최적점 가이드선 */}
        <line x1={nx(xStar)} y1={ny(0)} x2={nx(xStar)} y2={ny(yStar)} stroke="#6b7280" strokeWidth={1} strokeDasharray="2 3" />
        <line x1={nx(0)} y1={ny(yStar)} x2={nx(xStar)} y2={ny(yStar)} stroke="#6b7280" strokeWidth={1} strokeDasharray="2 3" />

        {/* 최적점 */}
        <circle cx={nx(xStar)} cy={ny(yStar)} r={5} fill="#111827" />
        <text x={nx(xStar) + 8} y={ny(yStar) - 6} fontSize={12} fontWeight={800} fill="#111827">E*</text>
        <text x={nx(xStar)} y={ny(0) + 14} fontSize={11} fill="#374151" textAnchor="middle">X*</text>
        <text x={nx(0) - 6} y={ny(yStar) + 4} fontSize={11} fill="#374151" textAnchor="end">Y*</text>
      </svg>
      <div style={{ marginTop: 6, fontSize: '0.78rem', color: '#374151', lineHeight: 1.55 }}>
        <div>• 선호 가중치 α = <strong>{alpha.toFixed(2)}</strong> (X 비중)</div>
        <div>• 상대가격 Px/Py = <strong>{pxOverPy.toFixed(2)}</strong></div>
        <div>• 최적점: MRS = Px/Py 조건에서 효용 극대화 (X* = αM/Px, Y* = (1−α)M/Py)</div>
      </div>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const indifferenceBudgetTemplate = {
  name: 'indifference-budget',
  version: 1,
  subjects: ['economics'],
  helpText: '무차별곡선 + 예산선 + 최적 소비점 (Cobb-Douglas)',
  Component: IndifferenceBudgetChart,
  schema: {
    type: 'object',
    properties: {
      scenario: { type: 'string' },
      preference_alpha: { type: 'number' },   // 0.1~0.9, X 선호 비중
      price_ratio: { type: 'number' },        // Px/Py
      income_over_py: { type: 'number' },     // M/Py
      x_label: { type: 'string' },
      y_label: { type: 'string' },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '효용극대화 — 균형 소비조합',
    preference_alpha: 0.5,
    price_ratio: 1.0,
    income_over_py: 1.0,
    narration: 'MRS = Px/Py 조건에서 E* 결정. α = 0.5 → X·Y 대칭 소비.',
  },
};
