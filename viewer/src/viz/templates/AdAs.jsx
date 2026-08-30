// AD-AS 모형 — 총수요·총단기공급·장기공급 평면.
//
// 가로축은 실질 GDP(Y), 세로축은 물가(P). AD 는 우하향, SAS 는 우상향,
// LAS 는 완전고용 산출에서 수직이다. 학파 차이(고전학파 = LAS 만, 케인즈 =
// 수평 구간)를 `as_shape` 로 고른다.
//
// 의미 파라미터만 받는다: 어떤 곡선이 어느 쪽으로 얼마나 왜 움직였는가.
// 좌표는 여기서 계산한다.

const W = 480, H = 360, PADL = 52, PADB = 50, PADT = 24, PADR = 30;
const PW = W - PADL - PADR;
const PH = H - PADT - PADB;

const MAG = { small: 0.10, moderate: 0.18, large: 0.30 };

const nx = (y) => PADL + y * PW;
const ny = (p) => PADT + (1 - p) * PH;
const clamp01 = (v) => Math.max(0, Math.min(1, v));

// AD: P = adIntercept - 0.7Y   SAS: P = sasIntercept + slope·Y   LAS: Y = lasY
function compute(shifts, shape, adSteep) {
  let ad = 0.88;
  let sas = 0.12;
  let las = 0.58;
  for (const s of shifts || []) {
    const m = MAG[s.magnitude] || MAG.moderate;
    const sign = s.direction === 'right' ? 1 : -1;
    if (s.curve === 'AD') ad += sign * m;
    else if (s.curve === 'SAS') sas -= sign * m;
    else if (s.curve === 'LAS') las += sign * m;
  }
  // 케인즈 극단은 수평(기울기 0에 가깝게), 고전학파는 수직에 가깝게 세운다.
  const slope = shape === 'keynes' ? 0.08 : shape === 'classic' ? 2.4 : 0.72;
  // AD 기울기는 IS·LM 의 모양에서 따라온다(IS 와 비례, LM 과 반비례).
  // 그 비교를 눈으로 보이려면 기울기 자체가 파라미터여야 한다.
  const adSlope = adSteep === 'steep' ? -1.5 : adSteep === 'flat' ? -0.32 : -0.7;
  const yStar = (ad - sas) / (slope - adSlope);
  const pStar = ad + adSlope * yStar;
  return { ad, sas, las, slope, adSlope, yStar, pStar };
}

const AD_C = '#2563eb', SAS_C = '#dc2626', LAS_C = '#111827';
const AD_C0 = '#93c5fd', SAS_C0 = '#fca5a5';

function line(intercept, slope) {
  return { x1: 0, y1: intercept, x2: 1, y2: intercept + slope };
}

function AdAsChart({ params }) {
  const shape = params.as_shape || 'normal';
  const shifts = params.shifts || [];
  const hasShift = shifts.length > 0;
  const showLas = params.show_las !== false;

  const before = compute([], shape, params.ad_slope);
  const after = compute(shifts, shape, params.ad_slope);

  const adB = line(before.ad, before.adSlope);
  const adA = line(after.ad, after.adSlope);
  const sasB = line(before.sas, before.slope);
  const sasA = line(after.sas, after.slope);

  const seg = (l, color, dash, wdt) => (
    <line x1={nx(clamp01(l.x1))} y1={ny(clamp01(l.y1))}
      x2={nx(clamp01(l.x2))} y2={ny(clamp01(l.y2))}
      stroke={color} strokeWidth={wdt} strokeDasharray={dash} />
  );

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
        <text x={nx(1)} y={ny(0) + 17} fontSize={12} fill="#374151" textAnchor="end">Y (실질 GDP)</text>
        <text x={nx(0) + 4} y={ny(1) - 6} fontSize={12} fill="#374151">P (물가)</text>

        {/* 장기총공급 — 완전고용 산출에서 수직 */}
        {showLas && (
          <>
            <line x1={nx(after.las)} y1={ny(0)} x2={nx(after.las)} y2={ny(1)}
              stroke={LAS_C} strokeWidth={2} strokeDasharray="6 4" />
            <text x={nx(after.las) + 5} y={ny(1) + 12} fontSize={12} fontWeight={700} fill={LAS_C}>LAS</text>
            <text x={nx(after.las)} y={ny(0) + 17} fontSize={10} fill="#6b7280" textAnchor="middle">Yf</text>
          </>
        )}

        {hasShift && (
          <>
            {seg(adB, AD_C0, '4 4', 1.5)}
            {seg(sasB, SAS_C0, '4 4', 1.5)}
          </>
        )}
        {seg(adA, AD_C, undefined, 2.2)}
        {seg(sasA, SAS_C, undefined, 2.2)}

        <text x={nx(clamp01(adA.x2)) - 4} y={ny(clamp01(adA.y2)) + 14} fontSize={12} fontWeight={700}
          fill={AD_C} textAnchor="end">{hasShift ? 'AD₁' : 'AD'}</text>
        <text x={nx(clamp01(sasA.x2)) - 4} y={ny(clamp01(sasA.y2)) - 6} fontSize={12} fontWeight={700}
          fill={SAS_C} textAnchor="end">{hasShift ? 'SAS₁' : 'SAS'}</text>

        <line x1={nx(after.yStar)} y1={ny(0)} x2={nx(after.yStar)} y2={ny(after.pStar)}
          stroke="#6b7280" strokeWidth={1} strokeDasharray="2 3" />
        <line x1={nx(0)} y1={ny(after.pStar)} x2={nx(after.yStar)} y2={ny(after.pStar)}
          stroke="#6b7280" strokeWidth={1} strokeDasharray="2 3" />

        {hasShift && (
          <>
            <circle cx={nx(before.yStar)} cy={ny(before.pStar)} r={4} fill="#fff" stroke="#9ca3af" strokeWidth={2} />
            <text x={nx(before.yStar) + 6} y={ny(before.pStar) - 6} fontSize={11} fill="#6b7280">E₀</text>
          </>
        )}
        <circle cx={nx(after.yStar)} cy={ny(after.pStar)} r={5} fill="#111827" />
        <text x={nx(after.yStar) + 8} y={ny(after.pStar) - 6} fontSize={12} fontWeight={700} fill="#111827">
          {hasShift ? 'E₁' : 'E*'}
        </text>
      </svg>

      {hasShift && (
        <ul style={{ margin: '6px 0 0', padding: '0 0 0 18px', fontSize: '0.78rem', color: '#374151', lineHeight: 1.5 }}>
          {shifts.map((s, i) => (
            <li key={i}>
              <strong>{s.curve}</strong> {s.direction === 'right' ? '우측' : '좌측'} 이동
              {s.magnitude && s.magnitude !== 'moderate' && ` (${s.magnitude === 'small' ? '소폭' : '대폭'})`}
              {s.reason && ` — ${s.reason}`}
            </li>
          ))}
          <li style={{ color: after.yStar > before.yStar ? '#15803d' : '#b91c1c', fontWeight: 700 }}>
            ⇒ Y {after.yStar > before.yStar ? '↑' : after.yStar < before.yStar ? '↓' : '—'},
            P {after.pStar > before.pStar ? '↑' : after.pStar < before.pStar ? '↓' : '—'}
          </li>
        </ul>
      )}
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const adAsTemplate = {
  name: 'ad-as',
  version: 1,
  subjects: ['economics'],
  helpText: 'AD-AS 모형 (총수요·단기총공급·장기총공급)',
  Component: AdAsChart,
  schema: {
    type: 'object',
    properties: {
      scenario: { type: 'string' },
      // normal = 우상향 SAS, keynes = 수평에 가까움, classic = 수직에 가까움
      as_shape: { enum: ['normal', 'keynes', 'classic'], default: 'normal' },
      show_las: { type: 'boolean', default: true },
      // AD 의 가파름. IS 와 비례·LM 과 반비례라는 규칙을 눈으로 보일 때 쓴다.
      ad_slope: { enum: ['steep', 'normal', 'flat'], default: 'normal' },
      shifts: {
        type: 'array',
        items: {
          type: 'object',
          required: ['curve', 'direction'],
          properties: {
            curve: { enum: ['AD', 'SAS', 'LAS'] },
            direction: { enum: ['left', 'right'] },
            magnitude: { enum: ['small', 'moderate', 'large'], default: 'moderate' },
            reason: { type: 'string' },
          },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '부정적 공급충격 (유가 급등)',
    as_shape: 'normal',
    shifts: [{ curve: 'SAS', direction: 'left', magnitude: 'moderate', reason: '생산비 상승' }],
    narration: 'SAS 좌측 이동 → 물가는 오르고 산출은 줄어드는 스태그플레이션.',
  },
};
