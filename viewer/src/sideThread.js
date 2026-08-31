// 샛길 — 학습 중 끼어들어 물은 대화. 논점 하나에 하나씩 붙는다.
//
// 심화 탭의 관 단위 대화(`ailearn-room:{leafId}`)와 **다른 키를 쓴다**.
// 논점에 붙은 즉문즉답과 관 전체를 놓고 하는 대화는 다시 열었을 때 보여야 할 것이
// 다르다. 같은 키에 담으면 논점 A 에서 물은 것이 논점 B 에도 뜬다.
//
// 트랙 상태(conceptTurns 의 cursor)는 여기서 건드리지 않는다 — 그래야 돌아갈 자리가
// 정확하다. 이 파일은 대화만 들고 있다.

/** 한 논점에 남길 최대 메시지 수. 넘으면 오래된 것부터 버린다. */
export const SIDE_MAX = 40;

export const sideKey = (leafId, pointId) => `ailearn-side:${leafId}:${pointId}`;

export function loadSide(leafId, pointId) {
  try {
    const raw = localStorage.getItem(sideKey(leafId, pointId));
    const arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch {
    // 저장소가 깨졌다고 학습을 멈플 이유는 없다.
    return [];
  }
}

export function appendSide(leafId, pointId, msg) {
  const next = loadSide(leafId, pointId).concat(msg).slice(-SIDE_MAX);
  try {
    localStorage.setItem(sideKey(leafId, pointId), JSON.stringify(next));
  } catch { /* 용량 초과 — 화면의 대화는 그대로 두고 저장만 포기한다 */ }
  return next;
}

export function clearSide(leafId, pointId) {
  try { localStorage.removeItem(sideKey(leafId, pointId)); } catch { /* noop */ }
}

export const sideCount = (leafId, pointId) => loadSide(leafId, pointId).length;
