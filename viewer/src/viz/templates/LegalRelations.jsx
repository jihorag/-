// 법률관계 그래프 — 당사자(노드) + 권리·의무·관계(엣지) 시각화.
// react-flow 없이 자체 레이아웃: 노드 개수에 따라 원형(circular) 또는 수평(horizontal) 자동.

const W = 600, H = 360;
const NODE_R = 38;  // 노드 반지름 (원형 디자인)

// 노드 위치 자동 배치
function layoutNodes(nodes) {
  const n = nodes.length;
  if (n === 0) return [];
  if (n === 1) return [{ ...nodes[0], x: W / 2, y: H / 2 }];
  if (n === 2) {
    return [
      { ...nodes[0], x: W * 0.25, y: H / 2 },
      { ...nodes[1], x: W * 0.75, y: H / 2 },
    ];
  }
  if (n === 3) {
    // 삼각형
    return [
      { ...nodes[0], x: W / 2, y: H * 0.25 },
      { ...nodes[1], x: W * 0.25, y: H * 0.75 },
      { ...nodes[2], x: W * 0.75, y: H * 0.75 },
    ];
  }
  // 4+ : 원형 배치
  const cx = W / 2, cy = H / 2;
  const r = Math.min(W, H) * 0.32;
  return nodes.map((node, i) => {
    const angle = -Math.PI / 2 + (2 * Math.PI * i) / n;
    return { ...node, x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) };
  });
}

// 두 점 사이 곡선 (양방향 엣지 분리 위해 약간 offset)
function edgePath(p1, p2, offset = 0) {
  const dx = p2.x - p1.x, dy = p2.y - p1.y;
  const len = Math.hypot(dx, dy);
  if (len < 1) return { d: '', mid: { x: p1.x, y: p1.y }, end: p2 };
  // 노드 가장자리에서 시작·종료
  const ux = dx / len, uy = dy / len;
  const sx = p1.x + ux * NODE_R;
  const sy = p1.y + uy * NODE_R;
  const ex = p2.x - ux * NODE_R;
  const ey = p2.y - uy * NODE_R;
  // 수직 normal로 곡률 적용
  const nx = -uy, ny = ux;
  const cx = (sx + ex) / 2 + nx * offset;
  const cy = (sy + ey) / 2 + ny * offset;
  return {
    d: `M ${sx} ${sy} Q ${cx} ${cy} ${ex} ${ey}`,
    mid: { x: cx, y: cy },
    end: { x: ex, y: ey },
    start: { x: sx, y: sy },
  };
}

const RELATION_COLORS = {
  '권리': '#2563eb',
  '의무': '#dc2626',
  '청구': '#7c3aed',
  '반환': '#0891b2',
  '효력': '#059669',
  default: '#6b7280',
};

function colorFor(rel) {
  if (!rel) return RELATION_COLORS.default;
  for (const [k, v] of Object.entries(RELATION_COLORS)) {
    if (rel.includes(k)) return v;
  }
  return RELATION_COLORS.default;
}

function LegalRelationsChart({ params }) {
  const nodes = layoutNodes(params.nodes || []);
  const nodeById = new Map(nodes.map((n) => [n.id, n]));
  const edges = params.edges || [];

  // 같은 (from, to) 쌍 다중 엣지 → offset 분리
  const pairCount = new Map();
  edges.forEach((e) => {
    const k = `${e.from}->${e.to}`;
    pairCount.set(k, (pairCount.get(k) || 0) + 1);
  });
  const pairSeen = new Map();

  return (
    <figure style={{ margin: '12px 0', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: 12, maxWidth: 640 }}>
      {params.scenario && (
        <figcaption style={{ fontSize: '0.88rem', fontWeight: 700, color: '#111827', marginBottom: 6 }}>
          ⚖️ {params.scenario}
        </figcaption>
      )}
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', maxWidth: 640, display: 'block' }}>
        <defs>
          {Object.entries(RELATION_COLORS).filter(([k]) => k !== 'default').concat([['default', RELATION_COLORS.default]]).map(([k, color]) => (
            <marker key={k} id={`arrow-${k}`} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill={color} />
            </marker>
          ))}
        </defs>

        {/* 엣지 */}
        {edges.map((e, i) => {
          const from = nodeById.get(e.from);
          const to = nodeById.get(e.to);
          if (!from || !to) return null;
          const k = `${e.from}->${e.to}`;
          const total = pairCount.get(k);
          const idx = (pairSeen.get(k) || 0);
          pairSeen.set(k, idx + 1);
          const offset = total > 1 ? (idx - (total - 1) / 2) * 22 : 0;
          const path = edgePath(from, to, offset);
          const color = colorFor(e.relation);
          const markerKey = (RELATION_COLORS[e.relation && Object.keys(RELATION_COLORS).find((k) => e.relation.includes(k))]) ? Object.keys(RELATION_COLORS).find((k) => e.relation.includes(k)) : 'default';
          return (
            <g key={i}>
              <path d={path.d} stroke={color} strokeWidth={1.8} fill="none" markerEnd={`url(#arrow-${markerKey})`} />
              {(e.relation || e.article) && (
                <g>
                  <rect
                    x={path.mid.x - 28} y={path.mid.y - 10}
                    width={56} height={20} rx={10}
                    fill="#fff" stroke={color} strokeWidth={1}
                  />
                  <text x={path.mid.x} y={path.mid.y + 4} fontSize={11} fontWeight={700} fill={color} textAnchor="middle">
                    {e.relation || e.article}
                  </text>
                </g>
              )}
              {e.article && e.relation && (
                <text x={path.mid.x} y={path.mid.y + 24} fontSize={10} fill="#6b7280" textAnchor="middle">
                  {e.article}
                </text>
              )}
            </g>
          );
        })}

        {/* 노드 */}
        {nodes.map((n) => (
          <g key={n.id}>
            <circle cx={n.x} cy={n.y} r={NODE_R}
              fill={n.role === 'plaintiff' ? '#dbeafe' : n.role === 'defendant' ? '#fee2e2' : n.role === 'court' ? '#fef3c7' : '#f3f4f6'}
              stroke={n.role === 'plaintiff' ? '#2563eb' : n.role === 'defendant' ? '#dc2626' : n.role === 'court' ? '#d97706' : '#9ca3af'}
              strokeWidth={2}
            />
            <text x={n.x} y={n.y - 4} fontSize={12} fontWeight={800} fill="#111827" textAnchor="middle">{n.party || n.id}</text>
            {n.role && (
              <text x={n.x} y={n.y + 12} fontSize={10} fill="#6b7280" textAnchor="middle">{n.role}</text>
            )}
          </g>
        ))}
      </svg>
      {params.narration && (
        <p style={{ margin: '8px 0 0', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
          {params.narration}
        </p>
      )}
    </figure>
  );
}

export const legalRelationsTemplate = {
  name: 'legal-relations',
  version: 1,
  subjects: ['civil', 'law', 'appraisal_law'],
  helpText: '법률관계 노드/엣지 그래프 (당사자, 권리·의무, 조문)',
  Component: LegalRelationsChart,
  schema: {
    type: 'object',
    required: ['nodes'],
    properties: {
      scenario: { type: 'string' },
      nodes: {
        type: 'array',
        minItems: 2,
        items: {
          type: 'object',
          required: ['id', 'party'],
          properties: {
            id: { type: 'string' },
            party: { type: 'string' },
            role: { type: 'string' },  // plaintiff | defendant | court | thirdparty 자유 텍스트
          },
        },
      },
      edges: {
        type: 'array',
        items: {
          type: 'object',
          required: ['from', 'to'],
          properties: {
            from: { type: 'string' },
            to: { type: 'string' },
            relation: { type: 'string' },
            article: { type: 'string' },
          },
        },
      },
      narration: { type: 'string' },
    },
  },
  exampleParams: {
    scenario: '매매계약의 기본 법률관계',
    nodes: [
      { id: 'A', party: '매도인', role: 'plaintiff' },
      { id: 'B', party: '매수인', role: 'defendant' },
    ],
    edges: [
      { from: 'A', to: 'B', relation: '소유권 이전 의무', article: '민법 제568조' },
      { from: 'B', to: 'A', relation: '대금 지급 의무', article: '민법 제568조' },
    ],
    narration: '쌍방의 동시이행 관계 (제536조).',
  },
};
