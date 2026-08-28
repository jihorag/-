// 동차(같은 해 1·2차 동시 합격) 목표 자동 학습 계획 생성기.
//
// 합격수기 공통 통찰(1차 대비): 2차가 진짜 관문(과락·논술) → 동차생은 2차를 일찍·비중 있게 깔고,
// 1차는 시험 직전 6~8주 '스퍼트'로 압축한다. 1차 직후에는 2차에 총력.
// 직장병행: 평일은 압축(출퇴근·점심·새벽), 주말에 몰아친다.
//
// 이 엔진은 오늘(진입 시점)·1차·2차 시험일·하루 공부시간·직장병행 여부로부터
//   ① 전체 계획(단계)  ② 월별 계획  ③ 오늘의 계획(구체 태스크)
// 을 결정론적으로 생성한다. AI 조정 버튼이 이 함수를 다시 돌려 즉시 반영한다.

import { leafLabel } from './learnState';

const OPTS_KEY = 'curriculum-plan-opts-v1';
const DAY = 86400000;
const S1_IDS = ['civil', 'economics', 'accounting', 'realestate', 'law'];

export const DEFAULT_OPTS = { hoursWeekday: 3, hoursWeekend: 8, working: false, target: 'dongcha' };
export function getPlanOpts() {
  try { return { ...DEFAULT_OPTS, ...(JSON.parse(localStorage.getItem(OPTS_KEY) || '{}') || {}) }; }
  catch { return { ...DEFAULT_OPTS }; }
}
export function setPlanOpts(o) { try { localStorage.setItem(OPTS_KEY, JSON.stringify(o)); } catch { /* SSR */ } }

const S1 = ['civil', 'economics', 'accounting', 'realestate', 'law'];       // 1차 5과목
const S1_SHORT = { civil: '민법', economics: '경제', accounting: '회계', realestate: '부동산', law: '관계법규' };
const S2_SHORT = { appraisal_practice: '실무', appraisal_theory: '이론', appraisal_law: '법규' };

const toDate = (s) => { if (!s) return null; const d = new Date(s + 'T00:00:00'); return isNaN(d.getTime()) ? null : d; };
const addDays = (d, n) => new Date(d.getTime() + n * DAY);
const daysBetween = (a, b) => Math.round((b - a) / DAY);
const monthKey = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
const fmtMD = (d) => `${d.getMonth() + 1}/${d.getDate()}`;
// from 이후 처음 오는 (month, day). month: 0-based
const nextOccur = (from, month, day) => {
  let d = new Date(from.getFullYear(), month, day);
  if (d <= from) d = new Date(from.getFullYear() + 1, month, day);
  return d;
};

/**
 * @param {{today?:Date, exam1?:string, exam2?:string, opts?:object}} p
 */
export function generatePlan({ today = new Date(), exam1, exam2, opts, variant = 0, subjectState = null, targets = null } = {}) {
  const O = { ...DEFAULT_OPTS, ...(opts || {}) };
  const t0 = new Date(today.getFullYear(), today.getMonth(), today.getDate()); // 자정 기준

  // 시험일 — 미등록 시 예상값(감정평가사 통상: 1차 4월 초, 2차 8월 초)
  let e1 = toDate(exam1); const approx1 = !e1;
  if (!e1) e1 = nextOccur(t0, 3, 5);           // 다음 4월 5일경
  let e2 = toDate(exam2); const approx2 = !e2;
  if (!e2) e2 = new Date(e1.getFullYear(), 7, 3); // 같은 해 8월 초
  if (e2 <= e1) e2 = new Date(e1.getFullYear(), 7, 3);

  const d1 = daysBetween(t0, e1);
  const d2 = daysBetween(t0, e2);

  // 단계 경계: 1차 8주 전부터 1차 스퍼트, 1차 다음날부터 2차 총력
  const spurtStart = addDays(e1, -56);
  const p3Start = addDays(e1, 1);

  const rawPhases = [
    {
      key: 'p1', title: '기초 다지기 · 2차 이론 병행', color: '#0ea5e9', from: t0, to: spurtStart,
      goal: '2차 이론(실무·이론·법규)을 일찍 깔면서 1차 개념·기출을 병행 — 동차의 핵심은 2차를 미리 벌어두는 것',
      mix: [{ k: '2차 이론', pct: 45 }, { k: '1차 개념·기출', pct: 45 }, { k: '회계 매일인출', pct: 10 }],
    },
    {
      key: 'p2', title: '1차 집중 스퍼트 (직전 8주)', color: '#f59e0b', from: spurtStart, to: e1,
      goal: '1차 기출 회독으로 몰아친다. 2차는 감만 유지(최소). 모의고사로 시간 배분 훈련',
      mix: [{ k: '1차 기출·회독', pct: 80 }, { k: '2차 유지', pct: 10 }, { k: '모의·오답', pct: 10 }],
    },
    {
      key: 'p3', title: '2차 총력 (1차 직후 → 2차)', color: '#dc2626', from: p3Start, to: e2,
      goal: '진짜 승부처. 실무·이론·법규 답안 작성 + 채점평 내재화 + 목차 키워드 인출 회독',
      mix: [{ k: '2차 답안·실무', pct: 55 }, { k: '2차 이론·법규', pct: 30 }, { k: '채점평·회독', pct: 15 }],
    },
  ];
  // 오늘 이후 구간만, 시작을 오늘로 클램프
  const phases = rawPhases
    .filter((p) => p.to > t0)
    .map((p) => ({ ...p, from: p.from < t0 ? t0 : p.from }));
  phases.forEach((p) => { p.active = t0 >= p.from && t0 < p.to; p.days = Math.max(0, daysBetween(p.from, p.to)); p.label = `${fmtMD(p.from)} ~ ${fmtMD(p.to)}`; });
  const curPhase = phases.find((p) => p.active) || phases[0] || rawPhases[2];

  // ── 월별 계획 ──
  const months = [];
  let cur = new Date(t0.getFullYear(), t0.getMonth(), 1);
  const lastM = new Date(e2.getFullYear(), e2.getMonth(), 1);
  while (cur <= lastM) {
    const mid = new Date(cur.getFullYear(), cur.getMonth(), 15);
    const ph = rawPhases.find((p) => mid >= p.from && mid < p.to)
      || (mid < rawPhases[0].to ? rawPhases[0] : rawPhases[2]);
    const isExam1 = cur.getFullYear() === e1.getFullYear() && cur.getMonth() === e1.getMonth();
    const isExam2 = cur.getFullYear() === e2.getFullYear() && cur.getMonth() === e2.getMonth();
    months.push({
      ym: monthKey(cur),
      label: `${cur.getMonth() + 1}월`,
      year: cur.getFullYear(),
      phaseKey: ph.key, phaseTitle: ph.title, color: ph.color,
      focus: monthFocus(ph.key, isExam1, isExam2),
      isExam1, isExam2,
      isCurrent: cur.getFullYear() === t0.getFullYear() && cur.getMonth() === t0.getMonth(),
    });
    cur = new Date(cur.getFullYear(), cur.getMonth() + 1, 1);
  }

  // ── 오늘의 계획 ──
  const dow = t0.getDay(); // 0=일
  const isWeekend = dow === 0 || dow === 6;
  const hours = isWeekend ? O.hoursWeekend : O.hoursWeekday;
  const dayIdx = Math.floor(t0.getTime() / DAY);
  const todayPlan = {
    phaseKey: curPhase.key, phaseTitle: curPhase.title, color: curPhase.color,
    dow, isWeekend, hours,
    tasks: dailyTasks(curPhase.key, dayIdx + (variant || 0), hours, O, isWeekend, subjectState, targets),
    dataDriven: !!(subjectState && S1_IDS.some((s) => subjectState[s] && subjectState[s].total > 0)),
  };

  return { t0, e1, e2, d1, d2, approx1, approx2, phases, curPhase, months, today: todayPlan, opts: O };
}

function monthFocus(key, isExam1, isExam2) {
  if (isExam1) return '🎯 1차 시험 — 마지막 총정리·컨디션';
  if (isExam2) return '🎯 2차 시험 — 답안 마무리';
  if (key === 'p1') return '2차 이론 정착 + 1차 개념·기출 병행 (2차를 미리 벌어둔다)';
  if (key === 'p2') return '1차 기출 회독 총력 + 모의고사 (2차는 감만 유지)';
  return '2차 답안 작성 + 채점평 내재화 + 목차 키워드 인출 회독';
}

// 과목별 대표 단원 풀(대략적 학습 순서) — 오늘 어느 단원을 볼지 구체 지정용. 요일마다 로테이션.
const UNIT_POOLS = {
  civil: ['총칙 · 법률행위/의사표시', '총칙 · 대리/무효·취소', '물권 · 물권변동/점유', '물권 · 소유권/용익물권', '물권 · 담보물권', '채권총론 · 채무불이행', '채권각론 · 계약/매매', '채권각론 · 부당이득/불법행위'],
  economics: ['미시 · 수요·공급/탄력성', '미시 · 소비자이론(효용)', '미시 · 생산·비용', '미시 · 시장구조(독점·과점)', '미시 · 후생·외부효과', '거시 · 국민소득/IS-LM', '거시 · 화폐·인플레이션', '거시 · 국제·경제성장'],
  accounting: ['회계원리 · 분개/재무제표', '자산 · 재고자산', '자산 · 유형·무형자산', '금융자산·부채(사채)', '자본 · 자본거래/이익잉여금', '수익인식·현금흐름표', '원가 · 원가흐름/배부', '관리 · CVP/표준원가'],
  realestate: ['총론 · 부동산 특성', '경제론 · 수요·공급', '시장·정책론', '투자론 · 수익·위험', '금융론 · LTV/MBS', '개발·관리·마케팅', '지대·입지이론', '감정평가론 기초'],
  law: ['국토계획법 · 용도지역·지구', '도시개발/정비사업법', '감정평가법 · 감정평가규칙', '부동산공시법 · 공시지가', '부동산공시법 · 등기·지적', '토지보상법 · 손실보상', '국유재산·거래신고법', '개별법 총정리'],
  appraisal_practice: ['3방식 · 원가법', '3방식 · 거래사례비교법', '3방식 · 수익환원법', '토지·건물 평가', '임대료·권리금', '보상 · 토지보상', '보상 · 영업/지장물', '물건별 종합문제'],
  appraisal_theory: ['감정평가 기초이론', '지역·개별분석', '가격제원칙', '3방식 이론근거', '시산가액 조정', '최유효이용 분석', '부동산가격·시장', '특수·목적별 평가'],
  appraisal_law: ['토지보상법 · 사업인정/수용', '토지보상법 · 보상기준', '부동산공시법 논점', '감정평가법 논점', '행정법 · 처분/쟁송', '행정법 · 재결/행정소송', '헌법 · 재산권', '최신 판례 정리'],
};

// 여러 과목의 같은 종류(kind) 후보를 교대로 뽑는다(인터리빙 — 연구: 섞어서 학습하면 파지·변별 ↑).
// subs: 우선순위 정렬된 과목 목록(목표점수와의 격차 큰 과목이 앞).
function interleave(ss, kind, perSub, subs) {
  const field = kind === 'review' ? 'due' : kind === 'weak' ? 'weak' : 'next';
  const lists = subs.filter((s) => ss[s]).map((s) => (ss[s][field] || []).slice(0, perSub).map((st) => ({ sid: s, st, kind })));
  const res = []; let i = 0, any = true;
  while (any) {
    any = false;
    for (let k = 0; k < lists.length; k++) { if (lists[k][i]) { res.push(lists[k][i]); any = true; } }
    i++;
  }
  return res;
}
function candToTask(c) {
  const leaf = c.st.leaf; const unit = leafLabel(leaf);
  if (c.kind === 'review') return { type: 'drill', subjectId: c.sid, leafId: leaf.id, unit, amount: '복습 인출 · 기억곡선 도래', mins: 20 };
  if (c.kind === 'weak') { const acc = Math.round((c.st.quiz.accuracy || 0) * 100); return { type: 'solve', subjectId: c.sid, leafId: leaf.id, unit, amount: `기출 재도전 · 정답률 ${acc}%`, mins: 45 }; }
  return { type: 'study', subjectId: c.sid, leafId: leaf.id, unit, amount: '개념 학습 · 미학습', mins: 40 };
}
// 데이터 기반 1차 태스크 — 복습(기억곡선) → 약점 → 진도(미학습), 예산(분) 안에서 채움.
// 과목 순서는 '목표점수 - 현재 정답률' 격차가 큰 과목 우선(내가 세팅한 목표가 계획을 바꾼다).
const DEF_TARGET = { civil: 60, economics: 50, accounting: 50, realestate: 70, law: 70 };
function build1(ss, budgetMin, dayIdx, targets) {
  const gap = (sid) => ((targets && targets[sid]) || DEF_TARGET[sid] || 60) - (ss[sid]?.avgAccuracy ?? 0);
  const subs = S1_IDS.filter((s) => ss[s]).sort((a, b) => gap(b) - gap(a));
  const queue = [
    ...interleave(ss, 'review', 2, subs),
    ...interleave(ss, 'weak', 2, subs),
    ...interleave(ss, 'new', 1, subs),
  ];
  const T = []; let used = 0;
  for (const c of queue) {
    const task = candToTask(c);
    if (used + task.mins > budgetMin && T.length > 0) break;
    T.push(task); used += task.mins;
    if (used >= budgetMin) break;
  }
  return T;
}
// 데이터 없을 때(초기) 폴백 — 아직 기록이 없으니 '처음부터'. 과목은 요일마다 바꾸되
// 단원은 커리큘럼 순서의 앞(회계원리·총칙 등 index 0~)부터. (뒤 단원 원가/관리가 먼저 나오지 않게)
function fallback1(key, dayIdx, hours) {
  const rot = (n) => S1_IDS[(dayIdx + n) % S1_IDS.length];
  const unitAt = (sid, idx = 0) => { const p = UNIT_POOLS[sid] || []; return p.length ? p[Math.min(idx, p.length - 1)] : ''; };
  const q = Math.max(15, Math.round(hours * 12));
  const mk = (type, sid, amount, mins, idx = 0) => ({ type, subjectId: sid, unit: unitAt(sid, idx), amount, mins });
  if (key === 'p1') return [mk('study', rot(0), '개념 1단원 정독', 50, 0), mk('solve', rot(1), `기출 ${q}문항`, 50, 0), mk('drill', 'accounting', '취약 20지문 인출', 20, 0)];
  if (key === 'p2') return [mk('solve', rot(0), `기출 회독 ${q}문항`, 70, 0), mk('solve', rot(2), '기출 회독', 60, 1), mk('drill', 'accounting', '취약 20지문 인출', 20, 0)];
  return [{ type: 'review', subjectId: null, unit: '누적 오답', amount: '오답 소진', mins: 30 }];
}
// 2차 태스크(essay 풀) — 2차는 leaf 기반 데이터가 얇아 대표 논점 로테이션.
function build2(key, dayIdx, budgetMin, isWeekend) {
  const unitOf = (sid, off = 0) => { const p = UNIT_POOLS[sid] || []; return p.length ? p[(((dayIdx + off) % p.length) + p.length) % p.length] : ''; };
  const raw = [];
  const push = (type, sid, amount, mins, off = 0) => raw.push({ type, subjectId: sid, unit: unitOf(sid, off), amount, mins });
  if (key === 'p3') {
    push('essay', 'appraisal_practice', '답안 1문제 · 시간 재고 실전', 80);
    const alt = ['appraisal_theory', 'appraisal_law'][dayIdx % 2]; push('essay', alt, '목차 1논점 작성', 60);
    raw.push({ type: 'review', subjectId: null, unit: '채점평 카드', amount: '득점/감점 지점 인출', mins: 40 });
    push('essay', 'appraisal_theory', '키워드→하위목차 백지인출', 30, 4);
  } else if (key === 'p1') {
    push('essay', 'appraisal_theory', '기본이론 1논점 정리(2차 미리)', 60);
  } else if (!isWeekend) {
    push('essay', 'appraisal_practice', '감 유지 1문제(가볍게)', 20);
  }
  const out = []; let used = 0;
  for (const t of raw) { if (used + t.mins > budgetMin && out.length > 0) break; out.push(t); used += t.mins; }
  return out;
}

// 하루 태스크 — 내 학습상태(subjectState) 기반으로 1차를 짜고, 동차 단계 비중으로 2차를 얹는다.
function dailyTasks(key, dayIdx, hours, O, isWeekend, ss, targets) {
  const totalMin = hours * 60;
  const w1 = key === 'p1' ? 0.55 : key === 'p2' ? 0.9 : 0.15; // 1차 시간 비중(동차 전략)
  const min1 = Math.round(totalMin * w1);
  const min2 = totalMin - min1;
  const has1 = ss && S1_IDS.some((s) => ss[s] && ss[s].total > 0);
  const T = [];
  T.push(...(has1 ? build1(ss, min1, dayIdx, targets) : fallback1(key, dayIdx, hours)));
  if (key === 'p2' && isWeekend) T.push({ type: 'mock', subjectId: null, unit: '전 과목', amount: '실전 1회 · 시간 배분', mins: 120 });
  T.push(...build2(key, dayIdx, min2, isWeekend));
  return T;
}

export { S1_SHORT, S2_SHORT, UNIT_POOLS };
