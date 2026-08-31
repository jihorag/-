// 유효 무게 = 다섯 계수의 곱. 전부 순수 함수다 — 저장소를 만지지 않는다.
// 스펙 §4-2.
//
//   w_eff = weights[f][g] × guess(nopt) × source[src] × repeat(rep, Δt_prev) × decay(Δt_now)
//
// 두 개의 Δt 를 혼동하지 않는다:
//   Δt_prev = ts − prevTs   직전 응답과 이번 응답 사이. 짧으면 문항을 외운 것이다.
//   Δt_now  = now − ts      이번 응답 이후 지금까지. 오래됐으면 지금은 모를 수 있다.
import { baseWeight, SOURCE, HALFLIFE, RHO } from './tables.js';

const DAY = 86400000;

/** §4-4 찍기 하한 보정. 5지선다를 1.0 으로 정규화한다. recog 에만 적용. */
export function guessAdj(f, nopt) {
  if (f !== 'recog') return 1;
  if (!nopt || nopt < 2) return 1;          // 모르면 깎지 않는다(로그는 record.js 가 남긴다)
  return (1 - 1 / nopt) / 0.8;
}

/** §4-5 출처 신뢰도. 모르는 출처는 자체제작만큼 보수적으로 본다. */
export function sourceAdj(src) {
  const v = SOURCE[src];
  return v == null ? SOURCE.practice : v;
}

/**
 * §4-6 반복 감쇠. 같은 문항을 또 맞히는 것은 문항을 외운 것일 수 있다.
 * 다만 간격이 길면 문항 기억이 아니라 진짜 인출이므로 회복시킨다.
 */
export function repeatFactor(rep, dtPrevDays, f) {
  const n = Math.max(1, rep || 1);
  if (n === 1) return 1;
  const S = HALFLIFE[f] || HALFLIFE.recog;
  const dt = Math.max(0, dtPrevDays || 0);
  return 1 - (1 - Math.pow(RHO, n - 1)) * Math.exp(-dt / S);
}

/** §4-7 시간 감쇠. 점수가 아니라 무게에 건다 — 오래된 것은 낮은 게 아니라 모르는 것이다. */
export function decayFactor(dtNowDays, f, g) {
  const S = (HALFLIFE[f] || HALFLIFE.recog) * (g === 'self' ? 0.5 : 1);
  return Math.exp(-Math.max(0, dtNowDays || 0) / S);
}

/** 계약 레코드 하나의 유효 무게. */
export function effectiveWeight(rec, nowMs) {
  if (!rec) return 0;
  const base = baseWeight(rec.f, rec.g, rec.strict);
  if (!base) return 0;                       // null(불가능 조합) · 0(무채점) 둘 다 여기서 걸린다
  const dtPrev = rec.prevTs ? (rec.ts - rec.prevTs) / DAY : Infinity;
  const dtNow = (nowMs - rec.ts) / DAY;
  return base
    * guessAdj(rec.f, rec.nopt)
    * sourceAdj(rec.src)
    * repeatFactor(rec.rep, dtPrev, rec.f)
    * decayFactor(dtNow, rec.f, rec.g);
}
