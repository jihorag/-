// 🤖 학습 계획 — '순차 완성' 방식.
// 학생은 한 과목을 끝까지(최소 N회독) 완성한 뒤 다음 과목으로 넘어간다(과목을 섞지 않음).
// AI는 '과목 순서 + 과목별 일수'라는 작은 JSON만 생성(→ 빠름). 나머지 날짜별 계획은
// expandDay()가 즉시 결정론적으로 펼친다. 오늘의 계획·달력이 같은 스케줄을 읽어 정확히 호응.

import { getPrefs } from './aiLearningStore';
import { resolveCall } from './modelRegistry';
import { sendMessagesUnified } from './aiProviders';
import { UNIT_POOLS, S1_SHORT, S2_SHORT } from './curriculumPlan';
import { subjectChapterPool } from './unitTree';
import { loadPassInsights, planStrategyText } from './passInsights';

// 계획 단원 풀 — 스케줄에 저장된 장(章) 풀(강의노트 기반)을 우선, 없으면 기본 8단원 풀로 폴백.
// 항목은 { name, hier } 객체 또는 (레거시) 문자열.
function poolArr(pools, sid) { const p = pools && pools[sid]; if (p && p.length) return p; return UNIT_POOLS[sid] || []; }
const entryName = (e) => (typeof e === 'string' ? e : (e && e.name) || '');
const entryHier = (e) => (typeof e === 'string' ? null : (e && e.hier) || null);
const entryMeta = (e) => (typeof e === 'string' ? {} : (e || {}));

const AIPLAN_KEY = 'curriculum-aiplan-v1';
const DAY = 86400000;
const ALL_SHORT = { ...S1_SHORT, ...S2_SHORT };
const S1_IDS = ['civil', 'economics', 'accounting', 'realestate', 'law'];

// 과목별 색 — 달력·오늘의 계획에서 과목 구분용(과목명 색상 표기).
export const SUBJECT_COLORS = {
  civil: '#2563eb', economics: '#16a34a', accounting: '#dc2626',
  realestate: '#d97706', law: '#7c3aed',
  appraisal_practice: '#0891b2', appraisal_theory: '#9333ea', appraisal_law: '#db2777',
};
const dkey = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const midnight = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());

export function getAiPlan() {
  try {
    const p = JSON.parse(localStorage.getItem(AIPLAN_KEY) || 'null');
    return (p && p.v === 4 && Array.isArray(p.blocks) && p.blocks.length) ? p : null;
  } catch { return null; }
}
export function saveSchedule(s) { try { localStorage.setItem(AIPLAN_KEY, JSON.stringify(s)); } catch { /* quota */ } }
export function clearAiPlan() { try { localStorage.removeItem(AIPLAN_KEY); } catch { /* noop */ } }

const amtFor = (kind, round) => (kind === '학습' ? '개념 학습 + 기출 풀이' : `${round}회독 · 기출 인출`);

// 기본 과목 순서 — 진도 있는 과목 먼저(이어서 완성, 거의 끝난 것부터 마무리), 미착수는 기본 순서.
function defaultOrder(ss) {
  const base = ['economics', 'civil', 'accounting', 'realestate', 'law'];
  if (!ss) return base;
  const started = base.filter((s) => ss[s] && (ss[s].coveredPct || 0) > 0)
    .sort((a, b) => (ss[b].coveredPct || 0) - (ss[a].coveredPct || 0));
  const rest = base.filter((s) => !started.includes(s));
  return [...started, ...rest];
}

// 2차(논술) 과목 순서 — 이론(체계)→실무(답안훈련)→법규(조문·판례). 동차 병행 트랙.
const S2_ORDER = ['appraisal_theory', 'appraisal_practice', 'appraisal_law'];

// 한 트랙(과목 순서)을 기간(totalDays)에 맞춰 집중창 blocks + 꼬리복습 trailing 으로 만든다.
function buildTrack(ord, focus, review, totalDays, daysMap, pools) {
  const nUnits = (sid) => poolArr(pools, sid).length || 8;
  const fW = (sid) => (daysMap && daysMap[sid]) || (nUnits(sid) * focus);
  const lastSid = ord[ord.length - 1];
  const trailW = review > 0 ? nUnits(lastSid) * review : 0;
  const totalW = ord.reduce((s, sid) => s + fW(sid), 0) + trailW || 1;
  const scale = totalDays ? totalDays / totalW : null;
  const span = (w, min) => (scale ? Math.max(min, Math.round(w * scale)) : Math.max(min, Math.round(w)));
  const blocks = []; let off = 0;
  ord.forEach((sid) => { const days = span(fW(sid), 3); blocks.push({ sid, fromOff: off, toOff: off + days }); off += days; });
  let trailing = null;
  if (review > 0) { const days = span(trailW, 3); trailing = { sid: lastSid, fromOff: off, toOff: off + days }; off += days; }
  if (totalDays) { const tail = trailing || blocks[blocks.length - 1]; if (tail) tail.toOff = Math.max(tail.fromOff + 3, totalDays); }
  return { blocks, trailing };
}

/**
 * 동차 스케줄 — 1차 트랙(순차+겹침) + 2차 트랙(항상 병행).
 * 1차는 today→exam1, 2차는 today→exam2 창에 각각 순차 배치.
 * 1차 시험 전: 매일 [1차 집중(+병행복습)] + [2차 1과목 병행]. 1차 시험 후: 2차 총력(집중+병행).
 */
export function buildSchedule({ exam1, exam2, rounds = 3, focusRounds = 2, opts = {}, order = null, daysMap = null, base = null, aiRefined = false, note = '', subjectState = null, leavesBySubject = null } = {}) {
  const now = new Date();
  const b0 = base ? new Date(base + 'T00:00:00') : midnight(now);
  const ord = (order && order.length ? order : defaultOrder(subjectState)).filter((s) => S1_IDS.includes(s));
  S1_IDS.forEach((s) => { if (!ord.includes(s)) ord.push(s); });

  const focus = Math.max(1, Math.min(focusRounds, rounds));
  const review = Math.max(0, rounds - focus);

  // 계획 단원 풀 — 강의노트 장(章) 구조에서 만든다(서수 구체화). 없으면 기본 8단원 풀로 폴백.
  const pools = {};
  if (leavesBySubject) {
    [...S1_IDS, ...S2_ORDER].forEach((sid) => { const p = subjectChapterPool(leavesBySubject[sid] || []); if (p.length) pools[sid] = p; });
  }

  const e1 = exam1 ? new Date(exam1 + 'T00:00:00') : null;
  const e2 = exam2 ? new Date(exam2 + 'T00:00:00') : null;
  const D1 = (e1 && !isNaN(e1.getTime()) && e1 > b0) ? Math.max(ord.length * 3, Math.round((e1 - b0) / DAY)) : null;
  const D2 = (e2 && !isNaN(e2.getTime()) && e2 > b0) ? Math.max(S2_ORDER.length * 3, Math.round((e2 - b0) / DAY)) : (D1 ? D1 + 120 : null);

  const t1 = buildTrack(ord, focus, review, D1, daysMap, pools);
  const t2 = buildTrack(S2_ORDER, focus, review, D2, null, pools);

  return {
    v: 4, base: dkey(b0), exam1: exam1 || '', exam2: exam2 || '',
    exam1Off: D1, exam2Off: D2, rounds, focusRounds: focus,
    opts: { hoursWeekday: opts.hoursWeekday || 3, hoursWeekend: opts.hoursWeekend || 8, working: !!opts.working },
    order: ord, blocks: t1.blocks, trailing: t1.trailing,
    order2: S2_ORDER, blocks2: t2.blocks, trailing2: t2.trailing,
    pools, poolsBuilt: leavesBySubject ? 2 : 0, note, aiRefined, generatedAt: now.toISOString(),
  };
}

export function defaultSchedule(p = {}) {
  return buildSchedule({ ...p, order: null, aiRefined: false, note: p.note || '과목별 순차 완성(기본 순서) — 🤖 버튼으로 내 진도 맞춤 최적화' });
}

// 한 과목의 진행분수(prog)에서 (단원idx, 회독) 계산. roundBase = 이 단계 시작 회독.
function pick(sid, prog, roundBase, roundCount, arr) {
  arr = arr || UNIT_POOLS[sid] || [];
  const passes = Math.max(1, arr.length * Math.max(1, roundCount));
  const pos = Math.min(passes - 1, Math.floor(Math.min(0.999, Math.max(0, prog)) * passes));
  const idx = arr.length ? pos % arr.length : 0;
  const round = roundBase + Math.floor(pos / (arr.length || 1));
  return unitAtIdx(sid, idx, round, arr);
}
// 특정 단원 idx로 태스크 구성(누적 파이프라인의 어제·그제 단원 지정용).
function unitAtIdx(sid, idx, round, arr) {
  arr = arr || UNIT_POOLS[sid] || [];
  const e = arr[idx];
  const m = entryMeta(e);
  const kind = round === 1 ? '학습' : '복습';
  return { sid, unit: entryName(e), hier: entryHier(e), level: m.level || null, sub: m.sub || null, div: m.div || '', chap: m.chap || '', idx, total: arr.length || 8, round, kind, amount: amtFor(kind, round) };
}

// 한 블록에서 off일의 학습 단원(범위 밖이면 null).
function pickAt(block, off, roundBase, roundCount, arr) {
  if (!block || off < block.fromOff || off >= block.toOff) return null;
  const prog = (off - block.fromOff) / Math.max(1, block.toOff - block.fromOff);
  return pick(block.sid, prog, roundBase, roundCount, arr);
}

// 🔁 누적 파이프라인 — 한 단원을 하루에 몰아치지 않고 여러 날에 나눠 누적 복습한다.
//   오늘 배우는 단원은 '학습'(개념), 직전 단원은 '문제풀이'(기출), 그 전 단원은 '드릴'(인출).
//   단원 인덱스 기준이라 진도 속도와 무관하게 항상 누적 3단계가 유지된다.
function pipeline(block, off, roundBase, roundCount, arr) {
  const p0 = pickAt(block, off, roundBase, roundCount, arr);
  if (!p0) return [];
  const out = [{ ...p0, activity: '학습' }];
  if (p0.idx - 1 >= 0) out.push({ ...unitAtIdx(block.sid, p0.idx - 1, p0.round, arr), activity: '문제풀이' });
  if (p0.idx - 2 >= 0) out.push({ ...unitAtIdx(block.sid, p0.idx - 2, p0.round, arr), activity: '드릴' });
  return out;
}

// 한 트랙에서 off일의 (집중 파이프라인 + 앞 과목 병행복습) 계산.
function trackDay(off, blocks, trailing, focus, review, pools) {
  if (trailing && off >= trailing.fromOff && off < trailing.toOff) {
    return pipeline(trailing, off, focus + 1, review || 1, poolArr(pools, trailing.sid)).map((t) => ({ ...t, tail: true }));
  }
  const bi = blocks.findIndex((bl) => off >= bl.fromOff && off < bl.toOff);
  if (bi < 0) return [];
  const block = blocks[bi];
  const out = pipeline(block, off, 1, focus, poolArr(pools, block.sid));
  if (bi > 0 && review > 0) {
    const prog = (off - block.fromOff) / Math.max(1, block.toOff - block.fromOff);
    const pv = pick(blocks[bi - 1].sid, prog, focus + 1, review, poolArr(pools, blocks[bi - 1].sid));
    if (pv && pv.unit) out.push({ ...pv, activity: '문제풀이', parallel: true });
  }
  return out;
}

/**
 * 특정 날짜의 계획을 펼친다 — 1차 트랙(집중+병행) + 2차 트랙(항상 병행/총력).
 */
export function expandDay(dateObj, schedule, hoursOverride) {
  if (!schedule || !Array.isArray(schedule.blocks)) return null;
  const b = new Date(schedule.base + 'T00:00:00');
  const off = Math.round((midnight(dateObj) - b) / DAY);
  if (off < 0) return null;
  const rounds = schedule.rounds || 3;
  const focus = Math.max(1, Math.min(schedule.focusRounds || 2, rounds));
  const review = Math.max(0, rounds - focus);
  const before1 = schedule.exam1Off == null || off < schedule.exam1Off;
  const pools = schedule.pools || {};

  const subs = [];
  // ① 1차 트랙 — 1차 시험 전까지
  if (before1 && schedule.blocks.length) {
    trackDay(off, schedule.blocks, schedule.trailing, focus, review, pools).forEach((s) => subs.push({ ...s, stage: 1 }));
  }
  // ② 2차 트랙 — 항상 병행(1차 전엔 집중 1과목만, 1차 후엔 총력)
  if (Array.isArray(schedule.blocks2) && schedule.blocks2.length && (schedule.exam2Off == null || off < schedule.exam2Off)) {
    const two = trackDay(off, schedule.blocks2, schedule.trailing2, focus, review, pools);
    if (before1) {
      if (two[0]) subs.push({ ...two[0], stage: 2, companion: true });
    } else {
      two.forEach((s) => subs.push({ ...s, stage: 2 }));
    }
  }
  if (!subs.length) return null;

  const dow = dateObj.getDay();
  const h = hoursOverride || ((dow === 0 || dow === 6) ? (schedule.opts?.hoursWeekend || 8) : (schedule.opts?.hoursWeekday || 3));
  // 회독이 올라갈수록 하루 학습량↑ (1회독=기준, 2회독=+35%, 3회독=+70% …)
  const roundOfDay = subs.reduce((m, s) => Math.max(m, s.round || 1), 1);
  const vol = Math.max(10, Math.round(h * 12 * (1 + 0.35 * (roundOfDay - 1))));
  return { subs, vol, round: roundOfDay, ai: !!schedule.aiRefined, phase: subs[0] && subs[0].kind };
}

function progressLines(ss) {
  if (!ss) return '(아직 학습 기록 없음 — 처음부터 순차 시작)';
  const lines = [];
  S1_IDS.forEach((sid) => {
    const s = ss[sid];
    if (!s || !s.total) return;
    lines.push(`- ${ALL_SHORT[sid]}: 진도 ${Math.round(s.coveredPct || 0)}% · 평균정답률 ${Math.round(s.avgAccuracy || 0)}% · 복습도래 ${(s.due || []).length}개`);
  });
  return lines.length ? lines.join('\n') : '(아직 학습 기록 없음 — 처음부터 순차 시작)';
}

function parseJson(text) {
  if (!text) return null;
  const t = text.replace(/```json/gi, '').replace(/```/g, '').trim();
  const s = t.indexOf('{'); const e = t.lastIndexOf('}');
  if (s < 0 || e < 0 || e <= s) return null;
  try { return JSON.parse(t.slice(s, e + 1)); } catch { return null; }
}

/**
 * AI로 '과목 순서 + 과목별 일수'만 받아(작고 빠름) 순차 스케줄을 만든다.
 * 파싱 실패 시 기본 순서로 폴백(에러 없이 항상 계획이 나온다).
 */
export async function generateAiPlan({ exam1, exam2, rounds = 3, opts = {}, subjectState = null, leavesBySubject = null, signal } = {}) {
  const model = (getPrefs() && getPrefs().model) || 'claude-sonnet-4-6';
  const { apiKey, baseUrl, needsKey } = resolveCall(model);
  if (needsKey && !apiKey) throw new Error('AI 모델의 API 키가 필요해요 — 홈 설정 🔑에서 키를 등록하세요.');

  const now = new Date();
  const t0 = midnight(now);
  const e1 = exam1 ? new Date(exam1 + 'T00:00:00') : null;
  const D = e1 && !isNaN(e1.getTime()) ? Math.max(1, Math.round((e1 - t0) / DAY)) : null;

  const strat = planStrategyText(await loadPassInsights()); // 합격수기 78건 기반 전략

  const system = `너는 감정평가사 1차 수험 플래너다. 학생은 '한 과목을 집중 완성(1~2회독)한 뒤 다음 과목으로 넘어가되, 앞 과목의 남은 복습 회독은 다음 과목 학습과 겹쳐서(병행) 굴리는' 파이프라인 순차 방식으로 공부한다.
5개 과목의 학습 순서(order)와 각 과목의 '집중 학습 기간(days)'을 정하라.
- id: 민법=civil, 경제=economics, 회계=accounting, 부동산=realestate, 관계법규=law
- 진도가 이미 있는 과목을 먼저(이어서 완성). 회계·경제처럼 휘발성 큰 과목을 맨 뒤로 미루지 말 것.
- days = 그 과목을 집중해서 처음 배우는(1~2회독) 기간. 남은 복습은 다음 과목과 겹치니 포함하지 말 것.
${strat ? '\n' + strat + '\n' : ''}[출력 — 오직 JSON 하나. 설명문 금지]
{"order":["economics","civil","accounting","realestate","law"],"days":{"economics":24,"civil":30,"accounting":26,"realestate":18,"law":18},"note":"한 줄 이유"}`;

  const user = `오늘: ${dkey(t0)}
1차 시험: ${D != null ? `D-${D}` : '미등록'}
하루 공부시간: 평일 ${opts.hoursWeekday || 3}시간 / 주말 ${opts.hoursWeekend || 8}시간${opts.working ? ' · 직장 병행' : ''}
목표 최소 회독: ${rounds}회
[과목별 현재 진도]
${progressLines(subjectState)}`;

  let parsed = null;
  try {
    const { text } = await sendMessagesUnified({
      apiKey, model, system,
      messages: [{ role: 'user', content: user }],
      maxTokens: 700, baseUrl, signal,
    });
    parsed = parseJson(text);
  } catch (e) {
    if (signal && signal.aborted) throw e;
    parsed = null; // 실패해도 기본 순서로 폴백
  }

  const order = (parsed && Array.isArray(parsed.order)) ? parsed.order.filter((s) => S1_IDS.includes(s)) : null;
  const daysMap = (parsed && parsed.days && typeof parsed.days === 'object') ? parsed.days : null;
  const sched = buildSchedule({
    exam1, exam2, rounds, opts, order, daysMap, subjectState, leavesBySubject,
    aiRefined: !!(order && order.length), note: (parsed && parsed.note) || '',
  });
  saveSchedule(sched);
  return sched;
}
