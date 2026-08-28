// 📊 실력 리포트 — 계산 엔진(순수 로직)
// AI 학습(이해)·드릴(인출)·문제풀이(적용) 3개 모드의 신호를 모아
// "지금 이 순간 시험장에서 낼 수 있는 실력"을 단원→과목→종합 점수로 환산한다.
//
// 학습과학 근거(각 요소에 주석):
//  P1 테스팅 효과(Roediger 2006)  — 인출·적용을 노출보다 무겁게 가중
//  P2 망각곡선(Ebbinghaus/Cepeda)  — 오래된 학습은 현재 인출가능성으로 할인
//  P3 기억 안정성(간격효과)         — 회독(box)이 높을수록 감쇠가 느림
//  P4 메타인지 보정(Bjork)          — 자신감('know')과 실제 정답률의 괴리 = 과신
//  P5 시험 타당도                   — 기출 빈도(tier)로 가중해 '빈출 실력'을 반영
//  P6 숙달학습 임계(Bloom)          — 단원을 숙달/학습중/취약/미착수로 분류
//  P7 측정의 정직성                 — 표본 적으면 Wilson 하한 + 신뢰도 표기
import { SUBJECTS, getMastery, SRS_LADDER } from './aiLearningStore';
import { getConfidenceMap } from './studyMeta';
import { loadExamFreq } from './examFreq';

const DAY = 86400000;
const norm = (s) => (s || '').replace(/\s+/g, '');
const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));

// P7 — Wilson 95% 하한. 표본이 적으면 정답률을 보수적으로 낮춘다(5문제 100% ≠ 실력 100).
export function wilsonLower(correct, n) {
  if (!n) return 0;
  const z = 1.96, p = correct / n;
  const denom = 1 + (z * z) / n;
  const centre = p + (z * z) / (2 * n);
  const margin = z * Math.sqrt((p * (1 - p) + (z * z) / (4 * n)) / n);
  return clamp((centre - margin) / denom, 0, 1);
}

// P2/P3 — 현재 인출가능성 R = exp(-Δt / S). S(안정성)는 회독 box에서 유도. 날짜 모르면 할인 안 함.
export function retrievability(box, ageDays) {
  if (ageDays == null) return 1;
  const S = SRS_LADDER[clamp(box || 0, 0, SRS_LADDER.length - 1)]; // [1,3,7,16,35,70]일
  return Math.exp(-Math.max(0, ageDays) / Math.max(1, S));
}

// P5 — 기출 빈도 tier → 가중치. 무등급은 낮게(정보 없음을 과대평가하지 않음).
const TIER_W = { A: 4, B: 3, C: 2, D: 1 };
const tierW = (t) => TIER_W[t] || 0.8;

// 드릴 기록(drill-progress-v1)을 leaf 단위로 집계
function drillByLeaf() {
  let prog = {};
  try { prog = JSON.parse(localStorage.getItem('drill-progress-v1') || '{}') || {}; } catch { /* */ }
  const byLeaf = {};
  for (const p of Object.values(prog)) {
    if (!p || !p.leafId) continue;
    const b = byLeaf[p.leafId] || (byLeaf[p.leafId] = { doneBoxes: [], doing: 0, lastTs: 0 });
    if (p.status === 'done') b.doneBoxes.push(p.box || 1);
    else if (p.status === 'doing') b.doing += 1;
    b.lastTs = Math.max(b.lastTs, p.ts || 0);
  }
  return byLeaf;
}

// score(0~100) → 예상 원점수 밴드(추정, 넓게). 합격선 60·과락 40 기준의 보수적 선형 보간.
function expectedBand(score) {
  const mid = 38 + score * 0.46; // 0→38, 100→84
  return { lo: Math.round(clamp(mid - 7, 0, 100)), mid: Math.round(mid), hi: Math.round(clamp(mid + 5, 0, 100)) };
}

/**
 * 전 과목 실력 리포트 계산.
 * @param leavesBySubject { subjectId: [leaf...] }
 * @param classifiedList  기출 문항(taxSubjectName/taxItemName/taxSectionName/taxChapterName 포함)
 * @param progress        { qid: { correct } }
 * @param qidFn           문항→id
 */
export async function computeProficiency({ leavesBySubject = {}, classifiedList = [], progress = {}, qidFn } = {}) {
  const qid = qidFn || ((q) => q.id);
  const now = Date.now();
  const mastery = getMastery();       // { leafId: { coverage, accuracy, srs_box, last_studied } }
  const confMap = getConfidenceMap(); // { qid: 'know'|'fuzzy'|'unknown' }
  const drill = drillByLeaf();

  const freqBySubj = {};
  await Promise.all(SUBJECTS.map(async (s) => { freqBySubj[s.id] = await loadExamFreq(s.id); }));

  // ── 문제풀이 집계: 과목·leaf별 정오 + 자신감 교차(P4) ──
  const stage1 = SUBJECTS.filter((s) => s.stage === 1);
  const titleMap = {};     // subjId → Map(normTitle → leafId)
  const quizAgg = {};      // subjId → { leaves:{leafId:{c,n}}, subj:{c,n}, calib:{...} }
  const korToId = {};
  for (const s of stage1) {
    const m = new Map();
    for (const l of (leavesBySubject[s.id] || [])) m.set(norm(l.title || (l.path || []).slice(-1)[0]), l.id);
    titleMap[s.id] = m;
    quizAgg[s.id] = { leaves: {}, subj: { c: 0, n: 0 }, calib: { knowN: 0, knowWrong: 0, lowN: 0, lowCorrect: 0 } };
    korToId[s.tax_key] = s.id; korToId[s.title] = s.id;
  }
  for (const q of classifiedList) {
    const sid = korToId[q.taxSubjectName];
    if (!sid) continue;
    const p = progress[qid(q)];
    if (!p || (p.correct !== true && p.correct !== false)) continue;
    const agg = quizAgg[sid];
    agg.subj.n += 1; if (p.correct) agg.subj.c += 1;
    const conf = confMap[qid(q)];
    if (conf === 'know') { agg.calib.knowN += 1; if (!p.correct) agg.calib.knowWrong += 1; }
    else if (conf === 'fuzzy' || conf === 'unknown') { agg.calib.lowN += 1; if (p.correct) agg.calib.lowCorrect += 1; }
    const tm = titleMap[sid];
    const leafId = tm.get(norm(q.taxItemName)) || tm.get(norm(q.taxSectionName)) || tm.get(norm(q.taxChapterName));
    if (leafId) { const lf = agg.leaves[leafId] || (agg.leaves[leafId] = { c: 0, n: 0 }); lf.n += 1; if (p.correct) lf.c += 1; }
  }

  // ── 과목별 leaf 점수 산출 ──
  const subjects = {};
  for (const s of SUBJECTS) {
    const leaves = leavesBySubject[s.id] || [];
    if (!leaves.length) { subjects[s.id] = null; continue; }
    const freq = freqBySubj[s.id] || {};
    const quiz = quizAgg[s.id];
    let wSum = 0, mSum = 0, breadthNum = 0, breadthDen = 0;
    let mastered = 0, learning = 0, weak = 0, untouched = 0;
    const axisU = [], axisR = [], axisA = [];
    let decayRiskW = 0, decaySafeW = 0;
    const rows = [];

    for (const l of leaves) {
      const w = tierW(freq[l.id]?.tier);
      // U 이해 — AI 학습 coverage
      const mm = mastery[l.id];
      const U = mm && mm.coverage != null ? clamp(mm.coverage, 0, 1) * 100 : null;
      // R 인출 — 드릴 회독
      const d = drill[l.id];
      let R = null, box = 0, drillTs = 0;
      if (d && d.doneBoxes.length) {
        box = Math.max(...d.doneBoxes);
        R = clamp((d.doneBoxes.reduce((a, b) => a + b, 0) / d.doneBoxes.length) / 4, 0, 1) * 100;
        drillTs = d.lastTs;
      } else if (d && d.doing) { R = 18; drillTs = d.lastTs; }
      // A 적용 — 기출 정답률(Wilson 하한)
      let A = null, qn = 0;
      if (quiz && quiz.leaves[l.id]) { const { c, n } = quiz.leaves[l.id]; A = wilsonLower(c, n) * 100; qn = n; }

      const msTs = mm && mm.last_studied ? Date.parse(mm.last_studied) : 0;
      const touch = Math.max(drillTs || 0, msTs || 0);
      const ageDays = touch ? (now - touch) / DAY : null;

      // P1 — 인출·적용 지배 가중. 측정된 축만 사용해 정규화.
      const axes = [];
      if (U != null) axes.push([0.20, U]);
      if (R != null) axes.push([0.35, R]);
      if (A != null) axes.push([0.45, A]);
      let M = null, Mraw = null;
      if (axes.length) {
        const ws = axes.reduce((a, [wt]) => a + wt, 0);
        Mraw = axes.reduce((a, [wt, v]) => a + wt * v, 0) / ws;
        const coverPenalty = 0.7 + 0.1 * axes.length;      // 1축0.8·2축0.9·3축1.0 (안 해본 축=모름)
        const Rnow = retrievability(box, ageDays);          // P2/P3
        M = Mraw * coverPenalty * (0.4 + 0.6 * Rnow);        // 최근일수록 만점 근접
        const rnowFlag = Rnow;
        if (Mraw * coverPenalty >= 55) { if (rnowFlag < 0.6) decayRiskW += w; else decaySafeW += w; }
      }
      const Rnow = retrievability(box, ageDays);

      let status;
      if (M == null) { status = 'untouched'; untouched += 1; }
      else if (M >= 75 && (A == null || A >= 55)) { status = 'mastered'; mastered += 1; }
      else if (M >= 45) { status = 'learning'; learning += 1; }
      else { status = 'weak'; weak += 1; }

      if (M != null) {
        wSum += w; mSum += w * M; breadthNum += w;
        if (U != null) axisU.push(U);
        if (R != null) axisR.push(R);
        if (A != null) axisA.push(A);
      }
      breadthDen += w;
      rows.push({ id: l.id, title: l.title || (l.path || []).slice(-1)[0], tier: freq[l.id]?.tier || null, w, U, R, A, M, status, Rnow, qn, ageDays });
    }

    const score = wSum ? mSum / wSum : 0;
    const breadth = breadthDen ? (breadthNum / breadthDen) * 100 : 0;
    const completion = leaves.length ? (mastered / leaves.length) * 100 : 0;
    const measured = rows.filter((r) => r.M != null).length;
    const confidence = clamp(measured / Math.max(8, leaves.length * 0.5), 0, 1); // 측정 단원이 많을수록 신뢰↑
    const avg = (a) => (a.length ? a.reduce((x, y) => x + y, 0) / a.length : null);

    let calibration = null;
    if (quiz && quiz.calib.knowN >= 3) {
      calibration = {
        overconfidence: quiz.calib.knowWrong / quiz.calib.knowN,
        knowN: quiz.calib.knowN, knowWrong: quiz.calib.knowWrong,
        underN: quiz.calib.lowN, underCorrect: quiz.calib.lowCorrect,
      };
    }
    // P5 — 빈출×약점 레버리지 = 가중치 × 부족분. 미착수는 M=28로 취급(빈출이면 우선순위 위로).
    const weakTop = rows
      .map((r) => ({ ...r, leverage: r.w * (100 - (r.M == null ? 28 : r.M)) }))
      .sort((a, b) => b.leverage - a.leverage)
      .filter((r) => r.status !== 'mastered')
      .slice(0, 10);

    subjects[s.id] = {
      id: s.id, title: s.title, short: s.short, icon: s.icon, color: s.color, stage: s.stage,
      score, breadth, completion, confidence,
      axes: { U: avg(axisU), R: avg(axisR), A: avg(axisA) },
      buckets: { mastered, learning, weak, untouched, total: leaves.length },
      calibration, decayRisk: decayRiskW, decaySafe: decaySafeW,
      quizN: quiz ? quiz.subj.n : 0,
      quizAcc: quiz && quiz.subj.n ? quiz.subj.c / quiz.subj.n : null,
      weakTop,
    };
  }

  const pick = (stage) => SUBJECTS.filter((s) => s.stage === stage).map((s) => subjects[s.id]).filter(Boolean);
  const s1 = pick(1), s2 = pick(2);
  const idxOf = (arr) => (arr.length ? arr.reduce((a, x) => a + x.score, 0) / arr.length : 0);
  const stage1Index = idxOf(s1), stage2Index = idxOf(s2);
  const overallConf = s1.length ? s1.reduce((a, x) => a + x.confidence, 0) / s1.length : 0;

  return {
    generatedAt: now,
    overall: {
      stage1Index, stage2Index, index: stage1Index,
      expected: expectedBand(stage1Index),
      confidence: overallConf,
      passLine: 60, floor: 40,
    },
    subjects,
  };
}

// 주간 추이 스냅샷 저장/조회 (P: 성장 추세)
const HIST_KEY = 'proficiency-history-v1';
export function snapshotProficiency(report) {
  try {
    const arr = JSON.parse(localStorage.getItem(HIST_KEY) || '[]') || [];
    const today = new Date(report.generatedAt); today.setHours(0, 0, 0, 0);
    const ymd = today.toISOString().slice(0, 10);
    const entry = {
      d: ymd, ts: report.generatedAt,
      i1: Math.round(report.overall.stage1Index), i2: Math.round(report.overall.stage2Index),
      subj: Object.fromEntries(Object.entries(report.subjects).filter(([, v]) => v).map(([k, v]) => [k, Math.round(v.score)])),
    };
    const rest = arr.filter((e) => e.d !== ymd);
    rest.push(entry);
    localStorage.setItem(HIST_KEY, JSON.stringify(rest.slice(-60)));
  } catch { /* quota */ }
}
export function getProficiencyHistory() {
  try { return JSON.parse(localStorage.getItem(HIST_KEY) || '[]') || []; } catch { return []; }
}
