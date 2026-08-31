// 심화 탭의 약점 카드 — 「이 관에서 두 번 이상 틀린 곳입니다」.
//
// 자유 대화는 「무엇을 물어야 할지 모르겠다」에서 막힌다. 약점 카드가 첫 발을
// 대신 뗀다. 화면과 프롬프트가 **같은 것**을 보게 하려고 여기 한 곳에서만 뽑는다.
//
// 부제(why)가 근거다 — 「기출 3문제 중 3개 오답」처럼 왜 약점으로 뽑혔는지 숫자로
// 말한다. 근거 없이 「약점」이라고만 하면 믿을 이유가 없다.

/** 이만큼 틀려야 약점이다. 한 번 틀린 것은 실수일 수 있다. */
export const WEAK_MIN_MISS = 2;

const MAX = 5;
const KIND_LABEL = { exam: '기출', ox: '확인 문제', recall: '서술 인출', quiz: '확인 문제' };
const KIND_UNIT = { exam: '문제', ox: '회', recall: '회', quiz: '회' };

export function weakSpots({ leafId, track, items }) {
  const points = track?.points || [];
  if (!leafId || !points.length || !Array.isArray(items)) return [];
  const byId = new Map(points.map((p) => [p.id, p]));

  const rows = [];
  for (const it of items) {
    if (it?.leafId !== leafId) continue;             // 다른 관의 기록을 섞지 않는다
    const p = byId.get(it.pointId);
    if (!p) continue;
    const miss = (it.attempted || 0) - (it.correct || 0);
    if (miss < WEAK_MIN_MISS) continue;
    const label = KIND_LABEL[it.kind] || '확인 문제';
    const unit = KIND_UNIT[it.kind] || '회';
    rows.push({
      pointId: p.id,
      seq: p.seq,
      title: p.title,
      miss,
      why: `${label} ${it.attempted}${unit} 중 ${miss}개 오답 · 논점 ${p.seq}`,
    });
  }
  return rows.sort((a, b) => b.miss - a.miss).slice(0, MAX);
}
