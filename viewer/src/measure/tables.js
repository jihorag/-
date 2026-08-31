// 학습 측정 계약 — 튜닝 가능한 값은 전부 이 파일에만 산다.
// 스펙: docs/superpowers/specs/2026-08-30-학습측정계약-design.md §4-3~§4-8
//
// 값을 바꾸면 TABLES_VERSION 을 올린다. 과거 기록은 자기가 기록될 때의
// 버전으로 계산해야 하기 때문이다 — 표를 고쳤다고 작년 점수가 흔들리면 안 된다.

export const TABLES_VERSION = 1;

/** §4-3 형식(f) × 채점 주체(g). null = 존재할 수 없는 조합. */
const WEIGHTS = {
  produce: { machine: 3.0, ai: 2.5, human: 3.0, self: 0.5, none: 0 },
  write:   { machine: null, ai: 2.5, human: 3.0, self: 0.6, none: 0 },
  recall:  { machine: 2.2, ai: 2.0, human: 2.4, self: 0.4, none: 0 },
  recog:   { machine: 1.0, ai: 0.9, human: 1.0, self: 0.3, none: 0 },
};

// 유일한 예외. AI 논점 quiz 는 선택지형이지만 2회 오답 시 통과를 박탈하므로
// 찍기 내성이 실질적으로 높다. 예외를 늘리지 않는다 — 늘리면 표가 아니라 코드가 된다.
const STRICT_RECOG_MACHINE = 2.0;

export const SOURCE = {
  official: 1.0,   // 기출
  gs: 0.8,         // 스터디
  practice: 0.5,   // 자체제작 — 재제작 후 상향
  ai: 0.3,
  internal: 0.9,   // 드릴·논점 quiz 등 강의·교재 기반
};

/** §4-7 시간 감쇠 반감기(일). 형식으로만 키를 잡는다. */
export const HALFLIFE = { produce: 120, write: 90, recall: 60, recog: 45 };

/** §4-6 반복 감쇠 계수. */
export const RHO = 0.6;

/** §4-8 상한. 내림차순으로 두고 처음 만족하는 것을 쓴다. */
const CAPS = [
  [3.0, 100],
  [2.5, 85],
  [2.0, 73],
  [1.0, 65],
  [0.4, 50],
];

export function baseWeight(f, g, strict = false) {
  const row = WEIGHTS[f];
  if (!row) return null;
  const w = row[g];
  if (w == null) return null;
  if (strict && f === 'recog' && g === 'machine') return STRICT_RECOG_MACHINE;
  return w;
}

export function capFor(wMax) {
  if (!wMax || wMax <= 0) return null;      // 미측정
  for (const [threshold, cap] of CAPS) {
    if (wMax >= threshold) return cap;
  }
  return CAPS[CAPS.length - 1][1];
}
