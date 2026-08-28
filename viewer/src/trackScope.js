// 개념 완성의 목차 범위. 강의가 없는 세부과목을 이 화면에서만 뺀다.
//
// taxonomy 자체는 건드리지 않는다 — AI 학습·드릴·문제풀이는 교재 기반이라
// 강의가 없어도 성립한다. 제외는 개념 완성 화면에서만 이뤄진다.
// 과목명을 코드에 박지 않으려고 규칙을 scope.json 으로 뺐다.

export function applyScope(leaves = [], scope) {
  const ex = scope?.exclude_divisions;
  if (!Array.isArray(ex) || ex.length === 0) return leaves.slice();
  const drop = new Set(ex);
  // path 가 없는 leaf 는 판단할 수 없으므로 남긴다. 조용히 사라지는 쪽이 더 나쁘다.
  return leaves.filter((l) => !(Array.isArray(l?.path) && drop.has(l.path[0])));
}
