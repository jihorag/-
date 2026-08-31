// 학습 측정 계약 — 단일 진입점.
// 앱의 모든 학습 활동은 이 함수 하나를 거쳐 기록된다. 스펙 §4-1·§4-9.
//
// 기존 저장소(quiz-progress-v1 · ailearn-items-v1 · ailearn-track-progress ·
// quiz-essay-progress)는 그대로 둔다. 여기는 병행 기록이다 — 기존 화면의
// 동작을 바꾸지 않으므로 되돌리기 쉽다.
export const RECORD_KEY = 'measure-records-v1';

/**
 * 채점 단위마다 최신 몇 개를 남길지.
 * 5인 이유: 반복 감쇠(§4-6)가 즉시 재응답 5회차에서 이미 0.13 이라
 * 그 뒤 기록은 무게가 거의 0이다. 무한히 쌓아 localStorage 를 채울 이유가 없다.
 * ponytail: localStorage 용량이 문제되면 IndexedDB 로 옮긴다. 지금은 필요 없다.
 */
export const MAX_PER_UNIT = 5;

const F_VALUES = new Set(['recog', 'recall', 'produce', 'write']);
const G_VALUES = new Set(['machine', 'ai', 'human', 'self', 'none']);
const AXIS_VALUES = new Set(['knowledge', 'performance']);

/** 계약 위반 사유를 모아 돌려준다. 비어 있으면 통과. */
export function validate(entry) {
  const bad = [];
  if (!entry || typeof entry !== 'object') return ['레코드가 객체가 아니다'];
  if (!entry.id) bad.push('id 가 없다');
  if (!entry.leaf) bad.push('leaf 가 없다 — 어디의 실력인지 알 수 없다');
  if (!AXIS_VALUES.has(entry.axis)) bad.push(`axis 가 잘못됐다: ${entry.axis}`);
  if (!F_VALUES.has(entry.f)) bad.push(`f 가 잘못됐다: ${entry.f}`);
  if (!G_VALUES.has(entry.g)) bad.push(`g 가 잘못됐다: ${entry.g}`);
  if (typeof entry.ts !== 'number') bad.push('ts 가 없다');

  const hasCorrect = entry.correct === true || entry.correct === false;
  const hasScore = typeof entry.score === 'number';
  if (entry.g !== 'none' && !hasCorrect && !hasScore) {
    bad.push('correct 도 score 도 없다 — 채점 결과가 없다');
  }
  if (hasScore && (entry.score < 0 || entry.score > 1)) {
    bad.push(`score 는 0~1 이다: ${entry.score}`);
  }
  return bad;
}

/** rep · prevTs · score · v · parent 를 채운 완성 레코드를 만든다. */
export function normalize(entry, prevList) {
  const same = (prevList || []).filter((r) => r.id === entry.id);
  const last = same.length ? same[same.length - 1] : null;
  const score = typeof entry.score === 'number'
    ? entry.score
    : (entry.correct === true ? 1 : entry.correct === false ? 0 : null);

  const out = {
    v: 1,
    ...entry,
    parent: entry.parent || entry.id,
    score,
    rep: same.length + 1,
  };
  if (entry.rev === undefined && contentRev) out.rev = contentRev;
  if (last) out.prevTs = last.ts;
  // 값이 없는 필드는 저장하지 않는다 — localStorage 를 아낀다.
  for (const k of Object.keys(out)) if (out[k] === undefined) delete out[k];
  return out;
}

/** 채점 단위마다 최신 maxPerUnit 개만 남기고, 전체를 시간 순으로 돌려준다. */
export function prune(records, maxPerUnit = MAX_PER_UNIT) {
  const byUnit = new Map();
  for (const r of records) {
    const list = byUnit.get(r.id) || [];
    list.push(r);
    byUnit.set(r.id, list);
  }
  const kept = [];
  for (const list of byUnit.values()) {
    list.sort((a, b) => a.ts - b.ts);
    kept.push(...list.slice(-maxPerUnit));
  }
  kept.sort((a, b) => a.ts - b.ts);
  return kept;
}

/**
 * leaf id 를 계층 경로로 쪼갠다. 1차는 5단, 2차는 3단이지만 같은 함수를 쓴다 —
 * 계층 축소(스펙 §8-C)가 깊이에 무관해야 두 구조가 같은 코드를 탄다.
 */
export function pathFromLeafId(leafId) {
  if (!leafId) return [];
  return String(leafId).split('__').filter(Boolean);
}

/**
 * 콘텐츠 판. 이 앱에는 판 번호 체계가 없고, 데이터 빌드 시각(manifest.built_at)이
 * 유일한 표식이다. 콘텐츠를 다시 구우면 값이 바뀌므로 "이 기록이 어느 콘텐츠에
 * 대한 것인지"를 나중에 가릴 수 있다. App 이 manifest 를 읽은 뒤 한 번 세팅한다.
 */
let contentRev = null;
export function setContentRev(v) { contentRev = v || null; }
export function getContentRev() { return contentRev; }

export function loadRecords() {
  try { return JSON.parse(localStorage.getItem(RECORD_KEY) || '[]') || []; }
  catch { return []; }
}

function save(list) {
  try { localStorage.setItem(RECORD_KEY, JSON.stringify(list)); }
  catch { /* 용량 초과 — 다음 가지치기에서 줄어든다 */ }
}

export function recordsForLeaf(leaf) {
  return loadRecords().filter((r) => r.leaf === leaf);
}

/**
 * 계약 레코드 하나를 남긴다.
 * 계약 위반은 개발 빌드에서 throw 한다 — 새 기능이 f·g·axis 를 빠뜨리는 것을
 * 배포 뒤에 발견하면 그 기간의 기록은 복구할 수 없다.
 */
export function record(entry) {
  const bad = validate(entry);
  if (bad.length) {
    const msg = `[measure] 계약 위반: ${bad.join(' · ')}`;
    if (import.meta.env && import.meta.env.DEV) throw new Error(msg);
    console.warn(msg, entry);
    return null;
  }
  if (entry.f === 'recog' && !entry.nopt) {
    console.warn('[measure] recog 인데 nopt 가 없다 — 찍기 하한을 모른다', entry.id);
  }
  const prev = loadRecords();
  const full = normalize(entry, prev);
  save(prune([...prev, full]));
  return full;
}
