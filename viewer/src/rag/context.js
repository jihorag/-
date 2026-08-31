// 심화 튜터에게 줄 자료를 조립한다 — 블록마다 상한을 못 박는다.
//
// 지금은 단원 md 를 통째로 넣는다(평균 10만 자). 관련 없는 부분까지 매번 들어가고
// 캐시 자리를 잡아먹는다. 여기서는 블록마다 글자 수를 자른다.
//
// 상한은 스펙 §6-4 의 값이다. 튜닝하려면 스펙을 먼저 고친다.

export const BUDGET = { chunks: 3000, points: 600, record: 800, lecture: 800 };

const clip = (s, n) => (s && s.length > n ? s.slice(0, n) : (s || ''));

/**
 * @returns {{ text: string, cited: Array<{id:string, path:string[]}> }}
 *   text  — 시스템 블록에 얹을 자료
 *   cited — 넣은 청크. 답변의 출처 칩을 만들 때 화면이 쓴다.
 */
export function buildContext({ question, chunks, points, record, lecture }) {
  const parts = [];
  const cited = [];

  const hits = Array.isArray(chunks) ? chunks : [];
  if (hits.length) {
    let used = 0;
    const lines = [];
    for (const c of hits) {
      const body = clip(c.text, BUDGET.chunks - used);
      if (!body) break;
      lines.push(`— ${(c.path || []).join(' › ')}\n${body}`);
      cited.push({ id: c.id, path: c.path || [] });
      used += body.length;
      if (used >= BUDGET.chunks) break;
    }
    parts.push(`[교재]\n${lines.join('\n\n')}`);
  } else {
    // 빈손일 때 그렇다고 적는 것이 중요하다. 안 적으면 모델이 기억으로 지어낸다.
    parts.push(`[교재]\n이 질문에 걸리는 대목을 교재에서 찾지 못했다. 교재를 인용하지 말고, 모르면 모른다고 답하라.`);
  }

  if (points) parts.push(`[이 관의 논점]\n${clip(points, BUDGET.points)}`);
  if (record) parts.push(`[학습 기록]\n${clip(record, BUDGET.record)}`);
  if (lecture) parts.push(`[강의 필기]\n${clip(lecture, BUDGET.lecture)}`);

  return { text: parts.join('\n\n'), cited };
}
