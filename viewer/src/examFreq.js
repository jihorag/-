// 기출 출제량 기반 '중요도 A~D급' — public/data/study/{subject}/exam_freq.json 을 읽는다.
// 이 파일은 기출(questions_db.json)에서 교재 leaf별 출제량을 계산해 만든 것(scratch/gen_exam_freq.py).
// tier 는 '과목 내 상대 백분위'(A 상위15% · B 25% · C 30% · D 30%). 신호 없는 leaf는 tier 없음.
const cache = {};

export async function loadExamFreq(subjectId) {
  if (!subjectId) return {};
  if (cache[subjectId] !== undefined) return cache[subjectId];
  try {
    const r = await fetch(`/data/study/${subjectId}/exam_freq.json`);
    if (!r.ok) throw new Error('no file');
    const d = await r.json();
    cache[subjectId] = d.byLeaf || {};
  } catch { cache[subjectId] = {}; }
  return cache[subjectId];
}

// 배지 색: A(빈출)만 강조색, 나머지는 차분하게 — 화면이 배지로 시끄럽지 않게.
export const TIER_META = {
  A: { label: '빈출 A', color: '#b91c1c', bg: '#fef2f2', bd: '#fecaca', rank: 4 },
  B: { label: 'B', color: '#c2410c', bg: '#fff7ed', bd: '#fed7aa', rank: 3 },
  C: { label: 'C', color: '#475569', bg: '#f1f5f9', bd: '#e2e8f0', rank: 2 },
  D: { label: 'D', color: '#94a3b8', bg: '#f8fafc', bd: '#eef2f6', rank: 1 },
};

export function tierOf(freqMap, leafId) { return freqMap?.[leafId]?.tier || null; }
export function tierRank(t) { return TIER_META[t]?.rank || 0; }
