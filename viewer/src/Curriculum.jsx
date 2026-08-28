// 🎓 합격 커리큘럼 — '인강 커리큘럼'처럼, 합격까지의 전체 로드맵을 단계별로 제시한다.
//
// 근거: 이 앱을 위해 수집·검증한 감정평가사 합격수기(landit·DCInside·고시위크·land-it·Threads).
//   · 1차 3개월 골격: 1개월 기본강의 → 2개월째 문제풀이 → 마지막 1개월 기출·모의고사
//   · 과목별 목표점수 + 과감한 '버리기'(경제 현시선호·솔로우 / 회계 법인세·주당이익·리스)
//   · 회계는 휘발성 1위 → 매일 인출, 최소 3회독(권장 5), 회계원리→중급→고급(제외)
//   · 불합격 1위 원인 = 완전이해 집착·문제풀이 부족("강사 이해 ≠ 내 이해")
//   · 2차: 채점평을 답안지로 옮겨 득점/감점 암기(실무 31→61점) / 목차 키워드 압축 인출(7~8회독)
//   · 2차 균형: 실무 우선 포기 → 3과목 균형(실무 50→30% · 이론 20→35% · 법규 35~40%)
//
// 적용 기능:
//   ① 1차/2차 전환 + 2차 로드맵   ② 실측 자동 체크(정답률·커버리지·모의·복습)   ③ 목표점수·버리기 개인화
// 각 마일스톤은 앱 기능으로 딥링크(onOpenTask)되고, 단계 전체를 플래너에 자동 배치할 수 있다.
// 저장: 'curriculum-progress-v1'(체크) · 'curriculum-auto-v1'(실측반영) · 'curriculum-strat-v1'(개인 목표/버리기)

import { useEffect, useMemo, useState } from 'react';
import { SUBJECTS } from './aiLearningStore';
import { generatePlan, getPlanOpts, setPlanOpts } from './curriculumPlan';
import { generateAiPlan, getAiPlan, defaultSchedule, buildSchedule, saveSchedule, expandDay, SUBJECT_COLORS } from './curriculumAi';
import { loadPassInsights, subjectTip } from './passInsights';
import { buildSubjectState, leafLabel } from './learnState';
import { TASK_TYPES } from './StudyPlanner';
import CurriculumCalendar from './CurriculumCalendar';

const PROG_KEY = 'curriculum-progress-v1';
const AUTO_KEY = 'curriculum-auto-v1';
const STRAT_KEY = 'curriculum-strat-v1';
const DATES_KEY = 'curriculum-dates-v1'; // { phaseId: 'YYYY-MM-DD' } 단계별 목표 일자
const ROUNDS_KEY = 'curriculum-rounds-v1'; // { itemId: 회독수 } 회독 카운터
const PKEY = 'quiz-planner-v1';
const pad = (n) => String(n).padStart(2, '0');
const SMAP = Object.fromEntries(SUBJECTS.map((s) => [s.id, s]));

// ── 1차 단계 ─────────────────────────────────────────────
const PHASES_1 = [
  {
    id: 'p0', w: 0, title: '시작 세팅', icon: '🎯', color: '#334155',
    goal: '방향부터 잡는다 — 목표점수·버릴 단원·시험일',
    note: '합격생 공통 교훈: "전체를 다 이해할 필요 없다. 강사 이해 ≠ 내 이해." 시작부터 목표점수와 버릴 단원을 정한다.',
    items: [
      { id: 'p0-1', type: 'custom', label: '시험일(1차) 등록 — 홈/프로필 D-day', tip: '남은 날짜에 맞춰 아래 단계가 자동 배치됩니다.' },
      { id: 'p0-2', type: 'custom', label: '과목별 목표점수 확정', tip: '민법 60 · 경제 50 · 회계 50 · 부동산 70+ · 관계법규 70+ (평균 60 / 과락 40 방어)' },
      { id: 'p0-3', type: 'custom', label: '버릴 단원 정하기', tip: '경제=현시선호·솔로우모형 / 회계=법인세·주당이익·리스(원가회계는 유지). 선택과 집중.' },
    ],
  },
  {
    id: 'p1', w: 0.30, title: '기본 이론 (개념 1회독)', icon: '📖', color: '#475569',
    goal: '전 과목 개념을 한 번 훑어 뼈대를 세운다',
    note: '완벽 이해에 매달리지 말 것 — 막히면 표시만 하고 넘어가 문제풀이 단계에서 채운다. 회계는 이 단계부터 매일 조금씩(휘발성 1위).',
    items: [
      { id: 'p1-civil', subject: 'civil', type: 'study', label: '민법 전 범위 개념 1회독 (총칙→물권→채권)', tip: '판례는 도식으로 시각화해 반복. 어려운 용어는 노트 툴팁 활용.', auto: { kind: 'aiCov', subject: 'civil', need: 0.6 } },
      { id: 'p1-econ', subject: 'economics', type: 'study', label: '경제 핵심 개념 1회독 (미시·거시 그래프 위주)', tip: '완벽 이해 포기 — 문제 푸는 데 필요한 부분만.', auto: { kind: 'aiCov', subject: 'economics', need: 0.6 } },
      { id: 'p1-acc', subject: 'accounting', type: 'study', label: '회계 회계원리→중급회계 개념 (분개로 이해)', tip: '고급회계는 제외. 매일 분개 조금씩.', auto: { kind: 'aiCov', subject: 'accounting', need: 0.6 } },
      { id: 'p1-re', subject: 'realestate', type: 'study', label: '부동산학 전 범위 개념 1회독', tip: '효자 과목 — 70+ 목표로 개념 탄탄히.', auto: { kind: 'aiCov', subject: 'realestate', need: 0.6 } },
      { id: 'p1-law', subject: 'law', type: 'study', label: '관계법규 A·B급 조문·체계 1회독', tip: '두문자로 뼈대 암기 시작.', auto: { kind: 'aiCov', subject: 'law', need: 0.6 } },
    ],
  },
  {
    id: 'p2', w: 0.45, title: '기출·문제풀이 반복 (최소 5회독)', icon: '✍️', color: '#475569',
    goal: '불합격 1위 원인이 "문제풀이 부족" — 기출은 돌릴수록 유리, 최소 5회독을 목표로',
    note: '합격수기 기준 회계는 "최소 3·권장 5회독 이상", 기출은 많이 돌릴수록 유리하다. 풀 문제 수를 먼저 정하고 → 기본서 확인 → 풀기 → 오답 체크. 틀린 건 오답노트. 계산은 "다른 방식"으로 검산. 회계는 휘발성 1위라 매일 인출 + 5회독.',
    items: [
      { id: 'p2-civil', subject: 'civil', type: 'solve', round: 5, label: '민법 기출 5회독 + 오답노트', tip: '판례 적용 실수 유형을 태그해 모은다.', auto: { kind: 'answered', subject: 'civil', need: 0.5 } },
      { id: 'p2-civil-d', subject: 'civil', type: 'drill', label: '민법 취약 관(章) 드릴 인출' },
      { id: 'p2-econ', subject: 'economics', type: 'solve', round: 5, label: '경제 기출·문제집 5회독 (하루 20~30문제)', tip: '복잡한 사칙연산은 즉시 계산기. 계산 와꾸로 유형 고정.', auto: { kind: 'answered', subject: 'economics', need: 0.5 } },
      { id: 'p2-acc', subject: 'accounting', type: 'solve', round: 5, label: '회계 기출 5회독 (원가회계 꼭 챙기기)', tip: '버린 파트는 스킵. 공학용 계산기 괄호로 한 번에 검산.', auto: { kind: 'answered', subject: 'accounting', need: 0.5 } },
      { id: 'p2-acc-d', subject: 'accounting', type: 'drill', label: '회계 매일 인출 드릴 (휘발 방지)' },
      { id: 'p2-re', subject: 'realestate', type: 'solve', round: 5, label: '부동산학 기출 5회독 + 계산 와꾸(입지·금융)', auto: { kind: 'answered', subject: 'realestate', need: 0.5 } },
      { id: 'p2-law', subject: 'law', type: 'solve', round: 5, label: '관계법규 기출 5회독 + 두문자 암기덱', tip: 'A·B급 먼저 완성, 조문 인출.', auto: { kind: 'answered', subject: 'law', need: 0.5 } },
    ],
  },
  {
    id: 'p3', w: 0.25, title: '실전 마무리 (모의 + 약점 압축)', icon: '🏁', color: '#334155',
    goal: '시간 안에 푸는 훈련 + 과락 방어 + 마지막 암기',
    note: '모의고사로 시간 배분·컨디션 점검. 오답은 소진될 때까지 반복. 관계법규 C·D급과 두문자는 이 시기에 최종 암기(이동·식사시간 틈틈이).',
    items: [
      { id: 'p3-mock', type: 'mock', label: '실전 모의고사 (전 과목 시간 배분 훈련)', tip: '다른 방식 검산 습관 유지.', auto: { kind: 'mock', need: 1 } },
      { id: 'p3-review', type: 'review', label: '오답 소진 복습 (틀린 것만 반복)', auto: { kind: 'reviewClear' } },
      { id: 'p3-law', subject: 'law', type: 'drill', label: '관계법규 C·D급 + 두문자 최종 인출' },
      { id: 'p3-acc', subject: 'accounting', type: 'drill', label: '회계 매일 인출 유지 (마지막까지)' },
      { id: 'p3-weak', type: 'review', label: '과락 위험 단원 집중 점검', tip: '40점 미만 과목이 없도록 최저 과목부터.' },
    ],
  },
];

// ── 2차 단계 ─────────────────────────────────────────────
const PHASES_2 = [
  {
    id: 's2-p0', w: 0, title: '시작 세팅', icon: '🎯', color: '#334155',
    goal: '3과목 균형과 답안 소스부터',
    note: '슬럼프 탈출의 핵심은 "실무를 먼저 잡아야 한다는 조급함 버리기". 처음부터 3과목을 균형 있게(실무 30% · 이론 35% · 법규 35%) 굴린다.',
    items: [
      { id: 's2-p0-1', type: 'custom', label: '시험일(2차) 등록 — 홈/프로필 D-day', tip: '남은 날짜에 맞춰 단계가 자동 배치됩니다.' },
      { id: 's2-p0-2', type: 'custom', label: '3과목 균형 배분 정하기 (실무30·이론35·법규35)', tip: '실무 편중은 정체의 원인 — 균형이 합격 전략.' },
      { id: 's2-p0-3', type: 'custom', label: 'GS/모의답안·채점평 소스 확보', tip: '채점평을 받아 두는 것이 이후 단계의 핵심 재료.' },
    ],
  },
  {
    id: 's2-p1', w: 0.30, title: '기본 이론 · 목차 체계', icon: '📖', color: '#475569',
    goal: '3과목의 목차 뼈대를 세우고 논점을 구조화한다',
    note: '목차마다 중요 키워드 2~3개를 정해 둔다. 이 키워드가 뒤 단계의 압축 인출 씨앗이 된다.',
    items: [
      { id: 's2-p1-prac', subject: 'appraisal_practice', type: 'essay', label: '실무 물건별 평가방법·계산 유형 이해' },
      { id: 's2-p1-theo', subject: 'appraisal_theory', type: 'essay', label: '이론 목차 체계 잡기 (논점 지도)' },
      { id: 's2-p1-law', subject: 'appraisal_law', type: 'essay', label: '보상법규 조문·판례 체계' },
    ],
  },
  {
    id: 's2-p2', w: 0.45, title: '답안 작성 + 채점평 내재화', icon: '✍️', color: '#475569',
    goal: '2차 점수 급상승의 핵심 — 채점평을 내 답안에 흡수한다',
    note: '채점평을 답안지로 옮겨 "어디서 득점/감점했는지" 정리·이해·암기하고 주 2~3회 반복. 이 방법으로 실무가 31점→61점으로 계단식 상승한 사례.',
    items: [
      { id: 's2-p2-prac', subject: 'appraisal_practice', type: 'essay', label: '실무 계산+약술 답안 작성 훈련' },
      { id: 's2-p2-theo', subject: 'appraisal_theory', type: 'essay', label: '이론 논점별 답안 목차 작성' },
      { id: 's2-p2-law', subject: 'appraisal_law', type: 'essay', label: '보상법규 사례형 답안 작성' },
      { id: 's2-p2-fb', type: 'custom', label: '★ 채점평 내재화 — 득점/감점 지점 카드화·주 2~3회 반복', tip: '2차 공부에서 제일 중요했다고 꼽힌 방법. 채점평을 그대로 답안에 옮겨 외운다.' },
    ],
  },
  {
    id: 's2-p3', w: 0.25, title: '목차 키워드 압축 인출', icon: '🏁', color: '#334155',
    goal: '키워드 하나로 전체 목차를 쏟아내는 속도를 만든다',
    note: '키워드 1개(예: 최유효이용)로 하위 목차·키워드 전체를 연상. "A상황 = A멘트"가 기계적으로 떠오르게. 7~8회독이면 1시간에 400~500점 분량을 검토.',
    items: [
      { id: 's2-p3-kw', type: 'custom', label: '키워드 → 목차 역인출 (키워드 1개로 하위 전체 연상)', tip: '백지에 키워드만 보고 하위 목차·키워드를 쏟아낸다.' },
      { id: 's2-p3-match', type: 'custom', label: '상황 = 멘트 매칭 암기', tip: '문제 상황을 보면 답안 멘트가 자동으로 떠오르도록.' },
      { id: 's2-p3-rep', type: 'custom', label: '3순환 7~8회독 반복 (인출 속도 ↑)', tip: '갈수록 회독이 빨라진다 — 시간 단축이 곧 숙달.' },
      { id: 's2-p3-mock', subject: 'appraisal_practice', type: 'essay', label: '실전 모의답안 시간 배분 훈련' },
    ],
  },
];

// 1차 과목별 전략 — 목표점수 / 유지 / 버리기 / 무기 (합격수기 수치 기반, goal·drop은 편집 가능)
const STRAT_DEF = [
  { id: 'civil', goal: '60', keep: '판례·조문 정확히', drop: '지엽 특별법', weapon: '판례 도식화 시각 암기' },
  { id: 'economics', goal: '50', keep: '문제풀이에 필요한 개념·계산', drop: '현시선호이론 · 솔로우모형', weapon: '복잡 계산 즉시 계산기 + 다른 방식 검산' },
  { id: 'accounting', goal: '50', keep: '회계원리·중급·원가회계(매일)', drop: '고급회계 · 법인세 · 주당이익 · 리스', weapon: '분개로 이해 + 5회독 이상(휘발성 1위)' },
  { id: 'realestate', goal: '70+', keep: '전 범위 + 계산(투자·금융·입지)', drop: '거의 없음 (효자 과목)', weapon: '고득점으로 평균 방어' },
  { id: 'law', goal: '70+', keep: 'A·B급 먼저 → C·D급 마지막', drop: '없음 (등급별 우선순위)', weapon: '두문자 · 단권화 · 틈새 청각 암기' },
];

// 2차 전략 참고(고정)
const STRAT_2 = [
  { id: 'appraisal_practice', goal: '균형 30%', keep: '물건별 평가·계산 정확도', drop: '실무 편중(우선 포기)', weapon: '채점평 내재화로 감점 지점 제거' },
  { id: 'appraisal_theory', goal: '균형 35%', keep: '논점 목차·키워드 2~3개', drop: '지엽 학설 나열', weapon: '키워드→목차 압축 인출' },
  { id: 'appraisal_law', goal: '균형 35%', keep: '조문·판례 정확 인용', drop: '불확실한 사견', weapon: '사례=쟁점 매칭 암기' },
];

const PHASE_SHORT = { p1: '기초·2차 병행', p2: '1차 스퍼트', p3: '2차 총력' }; // 월별 단계 약칭
// 단색 팔레트 — 인디고 1색 + 뉴트럴로 통일(장식용 다색 제거). 위험/성공만 시맨틱 색 유지.
const ACCENT = '#4361ee';   // 앱 기본 컬러(파란색)
const ACCENT_BG = '#eef1fe';
const ACCENT_BR = '#c6cefb';
const INK = '#2b3aa8';       // 진한 파랑(다크 헤더용)

const PRINCIPLES = [
  { icon: '🧠', title: '메타인지로 공부하라', body: '스톱워치로 회독·암기 시간을 재고, "안다/모른다"를 냉정히 진단해 모르는 것만 반복한다. 시간이 줄어드는 게 곧 숙달.' },
  { icon: '🔁', title: '이해 착시를 깨라', body: '강사 말이 이해된다 ≠ 내가 안다. 불합격 1위 원인이 "완전이해 집착 + 문제풀이 부족". 반드시 스스로 문제로 확인한다.' },
  { icon: '🧮', title: '검산은 다른 방식으로', body: '같은 방식으로 다시 풀면 뇌가 이미 정답으로 인식해 실수를 못 잡는다. 역연산·괄호계산 등 다른 경로로 검산한다.' },
];

// ── 과목별 인강식 월별 커리큘럼(간트) ──────────────────────────────
// 표준 수험 사이클(6월~다음해 3월, 1차 4월경) 기준. 카테고리 4행 × 월 10열.
// from/to = 월 인덱스(0=6월 … 9=3월, 포함). 과목별 단계 구성은 합격수기 기반으로 차등.
const GANTT_MONTHS = ['6월', '7월', '8월', '9월', '10월', '11월', '12월', '1월', '2월', '3월'];
// 행 = 이 앱의 학습 기능. 각 블록은 그 달에 어떤 앱 기능으로 공부할지를 나타내고, 누르면 해당 학습으로 이동한다.
const GANTT_ROWS = ['🎓 AI 개념학습', '📚 기출 문제풀이', '🔁 드릴·복습', '📝 모의고사', '🔄 회독 사이클'];
const GANTT_MODE = { study: 'AI 학습', solve: '문제풀이', drill: '드릴', review: '복습', mock: '모의고사' }; // block.type → 배지 라벨
const GANTT_ORDER = ['civil', 'economics', 'accounting', 'realestate', 'law'];
// 누적 파이프라인의 각 태스크는 '활동'이 하나로 정해져 있다(오늘 학습 / 어제 것 문제풀이 / 그제 것 드릴).
// 활동 → 앱 내 그 기능 한 곳으로 이동(onOpenTask). 2차는 문제풀이 대신 2차 논술.
const ACTIVITY_META = {
  '학습': { icon: '📘', label: '학습' },
  '문제풀이': { icon: '✏️', label: '문제풀이' },
  '드릴': { icon: '⚡', label: '드릴' },
};
// 직접 추가 계획의 활동 → 눌렀을 때 이동할 앱 기능
const MANUAL_TYPE = { '학습': 'study', '문제풀이': 'solve', '드릴': 'drill', '복습': 'review' };
// 회독별 점증 스텝 — AI 학습 실기능(모드·docTab·노트)을 그대로 반영.
// 회독이 오를수록 스텝 수·깊이가 늘어 하루 학습량이 순차적으로 증가한다.
// step: { type(이동 기능), tab, mode(AI 모드), docTab, do(설명) }
function planSteps(activity, round, stage, subjectId) {
  const r = Math.min(3, Math.max(1, round || 1));
  if (stage === 2) {
    if (activity === '학습') {
      const s = [{ type: 'study', tab: 'AI 학습', mode: 'concept_s2', do: '개념 모드로 논점 도입' }];
      if (r >= 2) s.push({ type: 'study', tab: 'AI 학습', mode: 'template', do: '양식 모드로 답안 골격 암기' });
      if (r >= 3) s.push({ type: 'study', tab: 'AI 학습', mode: 'topic_extract', do: '논점 모드로 사례 분석' });
      return s;
    }
    if (activity === '문제풀이') {
      const s = [{ type: 'essay', tab: '2차 논술', mode: 'answer_write', do: '답안 모드로 직접 작성·채점' }];
      if (r >= 2) s.push({ type: 'study', tab: 'AI 학습', mode: 'answer_write', do: '모범답안과 비교·보완' });
      if (r >= 3) s.push({ type: 'study', tab: 'AI 학습', mode: 'mock_full', do: '실전 모드 4문제 타이머' });
      return s;
    }
    const s = [{ type: 'drill', tab: '드릴', do: '목차·판례 인출' }];
    if (r >= 2) s.push({ type: 'study', tab: 'AI 학습', mode: 'template', do: '답안 골격 백지 인출' });
    return s;
  }
  const isAcc = subjectId === 'accounting';
  const isCalc = subjectId === 'accounting' || subjectId === 'economics';
  if (activity === '학습') {
    const s = [{ type: 'study', tab: 'AI 학습', mode: 'study', do: '이론 모드로 개념 잡기' }];
    if (r >= 2) {
      s.push({ type: 'study', tab: 'AI 학습', mode: 'deep', do: '심화 모드로 판례·함정 파기' });
      s.push({ type: 'study', tab: 'AI 학습', mode: 'summary', do: '복습 모드 핵심 압축 → 답변 💾 단권화' });
      if (isCalc) s.push({ type: 'study', tab: 'AI 학습', mode: isAcc ? 'journal' : 'calc', do: isAcc ? '분개 채점 연습' : '계산 한 단계씩' });
    }
    if (r >= 3) {
      s.push({ type: 'study', tab: 'AI 학습', mode: 'diagnose', docTab: 'ox', do: '진단 OX 5문제 셀프체크' });
      s.push({ type: 'study', tab: 'AI 학습', docTab: 'mem', do: '암기시트(형광펜 가리기) 인출' });
    }
    return s;
  }
  if (activity === '문제풀이') {
    const s = [
      { type: 'solve', tab: '문제풀이', do: '이 단원 기출 풀기' },
      { type: 'study', tab: 'AI 학습', mode: 'practice', do: '틀린 문제 문제풀이 모드로 해설' },
    ];
    if (r >= 2) s.push({ type: 'solve', tab: '문제풀이', do: '기출 반복 — 틀린 것 재도전' });
    if (r >= 3) s.push({ type: 'study', tab: 'AI 학습', mode: 'deep', do: '오답 함정 심화 정리' });
    return s;
  }
  const s = [{ type: 'drill', tab: '드릴', do: '핵심 인출' }];
  if (r >= 2) s.push({ type: 'drill', tab: '드릴', do: '두문자·암기카드 반복' });
  if (r >= 3) s.push({ type: 'drill', tab: '드릴', do: '백지 인출 + 판례·조문' });
  return s;
}
// row: 0=AI개념 1=기출풀이 2=드릴·복습 3=모의고사 / type: 눌렀을 때 이동할 앱 기능
const TRACKS = {
  civil: {
    subtitle: '판례 시각암기 + 기출 5회독',
    cycle: { from: 4, to: 8, rounds: 5 },
    blocks: [
      { row: 0, type: 'study', name: 'AI로 총칙→물권→채권 개념', from: 0, to: 2 },
      { row: 0, type: 'study', name: '판례 도식·용어 정리', from: 3, to: 4 },
      { row: 1, type: 'solve', name: '기출 5회독 + 오답노트', from: 4, to: 6 },
      { row: 2, type: 'drill', name: '취약 관·판례 인출 드릴', from: 5, to: 7 },
      { row: 3, type: 'mock', name: '실전 모의고사', from: 8, to: 9 },
    ],
    tips: ['AI 학습으로 총칙→물권→채권을 잡고, 판례는 도식·용어 툴팁으로 반복', '기출 5회독 + 오답노트 (문제풀이 부족이 불합격 1위)', '드릴로 취약 관·판례를 인출 훈련'],
  },
  economics: {
    subtitle: '계산 중심 · 완벽이해보다 문제풀이',
    cycle: { from: 4, to: 8, rounds: 5 },
    blocks: [
      { row: 0, type: 'study', name: 'AI 개념 (미시·거시) + 계산 와꾸', from: 0, to: 2 },
      { row: 0, type: 'study', name: '핵심 요약', from: 3, to: 4 },
      { row: 1, type: 'solve', name: '기출 문제풀이 (하루 20~30)', from: 4, to: 6 },
      { row: 2, type: 'drill', name: '계산 유형 인출 드릴', from: 5, to: 7 },
      { row: 3, type: 'mock', name: '실전 모의고사', from: 8, to: 9 },
    ],
    tips: ['현시선호이론·솔로우모형은 과감히 버림 (목표 50점)', '계산 와꾸로 유형 고정 · 복잡한 계산은 즉시 계산기', '검산은 반드시 다른 방식으로'],
  },
  accounting: {
    subtitle: '휘발성 1위 · 전 기간 매일 인출',
    cycle: { from: 4, to: 8, rounds: 5 },
    blocks: [
      { row: 0, type: 'study', name: 'AI로 회계원리→중급 (분개로)', from: 0, to: 2 },
      { row: 0, type: 'study', name: '이론 요약', from: 3, to: 4 },
      { row: 1, type: 'solve', name: '기출 5회독 (원가회계 필수)', from: 5, to: 6 },
      { row: 2, type: 'drill', name: '매일 인출 드릴 (휘발 방지)', from: 0, to: 8 },
      { row: 3, type: 'mock', name: '실전 모의고사', from: 8, to: 9 },
    ],
    tips: ['회계원리→중급 순, 고급회계·법인세·주당이익·리스는 버림 (원가회계는 필수)', '휘발성 1위 — 6월부터 시험까지 매일 인출 드릴을 끊지 않는다', '기출 최소 3회독(권장 5회독), 괄호로 한 번에 검산'],
  },
  realestate: {
    subtitle: '효자 과목 · 70+ 목표',
    cycle: { from: 4, to: 8, rounds: 5 },
    blocks: [
      { row: 0, type: 'study', name: 'AI로 전 범위 개념', from: 0, to: 2 },
      { row: 0, type: 'study', name: '요약 정리', from: 3, to: 4 },
      { row: 1, type: 'solve', name: '기출 + 계산 와꾸(입지·금융)', from: 4, to: 6 },
      { row: 2, type: 'drill', name: '취약 단원 인출 드릴', from: 5, to: 7 },
      { row: 3, type: 'mock', name: '실전 모의고사', from: 8, to: 9 },
    ],
    tips: ['효자 과목 — 고득점으로 평균 방어 (70+ 목표)', '투자·금융·입지 계산은 와꾸로 유형 고정', '개념 범위가 넓어 이론을 일찍 탄탄히'],
  },
  law: {
    subtitle: '순수 암기 · 후반 집중',
    cycle: { from: 6, to: 9, rounds: 6 },
    blocks: [
      { row: 0, type: 'study', name: 'AI로 조문·체계 (A·B급)', from: 1, to: 4 },
      { row: 1, type: 'solve', name: '기출·조문 문제풀이', from: 5, to: 6 },
      { row: 2, type: 'drill', name: '두문자 암기덱 + C·D급', from: 6, to: 8 },
      { row: 3, type: 'mock', name: '실전 모의고사', from: 8, to: 9 },
    ],
    tips: ['암기 과목 — 이론은 7월부터 시작해도 늦지 않음', 'A·B급 먼저 완성 → C·D급은 막판 암기', '두문자 암기덱으로 이동·식사시간 틈틈이 인출'],
  },
};

// 과목별 월별 학습 로드맵 카드(간트) — 각 칸은 "그 달에 이 앱에서 할 학습". 누르면 해당 기능으로 이동.
// 오늘(진입 시점)부터 1차 시험일(목표)까지로 월 축을 동적 생성하고, 표준 10개월 계획을 그 기간에 맞춰 압축/확장한다.
const GANTT_CANON = 10; // 표준 계획의 기준 개월 수(6월~3월)
function GanttCard({ subjectId, onOpenTask, exam1, onAskAI }) {
  const sm = SMAP[subjectId];
  const track = TRACKS[subjectId];
  if (!track) return null;
  const color = ACCENT; // 단색

  // ── 동적 월 축: 오늘 → 1차 시험월 ──
  const now = new Date();
  const startM0 = now.getMonth(); // 0-based
  const ed = exam1 ? new Date(exam1 + 'T00:00:00') : null;
  const dynamic = ed && !isNaN(ed.getTime()) && ed > now;
  let months, N, curCol, examLabel, examIsLast = false;
  if (dynamic) {
    const diff = (ed.getFullYear() * 12 + ed.getMonth()) - (now.getFullYear() * 12 + startM0) + 1; // 시험월 포함
    N = Math.max(2, Math.min(15, diff));
    examIsLast = N === diff; // 마지막 칸이 실제 시험월과 일치할 때만 '시험' 표기
    months = Array.from({ length: N }, (_, i) => `${((startM0 + i) % 12) + 1}월`);
    curCol = 0; // 오늘이 첫 칸
    examLabel = `${ed.getFullYear()}년 ${ed.getMonth() + 1}월`;
  } else {
    months = GANTT_MONTHS; N = GANTT_MONTHS.length;
    const cm = now.getMonth() + 1; curCol = cm >= 6 ? cm - 6 : cm <= 3 ? cm + 6 : -1;
    examLabel = '';
  }
  // 표준(0~9) → 실제 N개월로 리스케일. 같은 행에서는 앞 블록 끝을 넘겨 겹침 방지.
  const rowEnd = {};
  const scaleCol = (v) => Math.round((v / GANTT_CANON) * N);
  const pos = track.blocks.map((b) => {
    let c0 = scaleCol(b.from);
    let c1 = scaleCol(b.to + 1);
    c0 = Math.max(c0, rowEnd[b.row] || 0);
    if (c0 > N - 1) c0 = N - 1;
    c1 = Math.min(Math.max(c0 + 1, c1), N);
    rowEnd[b.row] = c1;
    return { ...b, c0, c1 };
  });
  let cyc = null;
  if (track.cycle) {
    const c0 = Math.min(scaleCol(track.cycle.from), N - 1);
    const c1 = Math.min(Math.max(c0 + 1, scaleCol(track.cycle.to + 1)), N);
    cyc = { c0, c1, rounds: track.cycle.rounds };
  }
  const minW = Math.max(560, 70 + N * 54);

  const askAI = () => {
    if (!onAskAI) return;
    const plan = track.blocks.map((b) => `${GANTT_MODE[b.type]}(${b.name})`).join(', ');
    const span = dynamic ? `오늘부터 1차 시험(${examLabel})까지 약 ${N - 1}~${N}개월` : '기간 미정(시험일 미등록)';
    const q = `나는 감정평가사 1차를 준비 중이야. ${span} 남았어.\n`
      + `${sm.short} 과목의 표준 커리큘럼은 [${plan}] 이고, 회독은 기출 ${track.cycle?.rounds || 5}회독을 목표로 해.\n`
      + `내 남은 기간에 맞춰 월별로 어떻게 조정하면 좋을지 — 무엇을 압축/생략하고 무엇에 집중할지 — 이 앱 기능(AI 개념학습·기출 문제풀이·드릴·모의고사·회독 사이클)을 활용하는 방식으로 구체적으로 코칭해줘. 특히 기간이 촉박하면 버릴 것을 분명히 정해줘.`;
    onAskAI(q);
  };

  return (
    <section style={{ border: '1px solid #e5e7eb', borderRadius: 16, overflow: 'hidden', boxShadow: 'var(--shadow-md)', marginBottom: 14, background: '#fff' }}>
      {/* 네이비 헤더 */}
      <div style={{ background: INK, color: '#fff', padding: '13px 15px' }}>
        <div style={{ fontSize: '0.64rem', opacity: 0.72, fontWeight: 700, letterSpacing: '0.03em' }}>이 앱으로 합격하는 월별 학습 플랜</div>
        <div style={{ fontWeight: 800, fontSize: '1rem', marginTop: 3 }}>{sm.icon} {sm.short} <span style={{ opacity: 0.85, fontWeight: 700, fontSize: '0.78rem' }}>· {track.subtitle}</span></div>
        <div style={{ fontSize: '0.64rem', opacity: 0.8, marginTop: 5, fontWeight: 600 }}>
          {dynamic ? `📆 오늘부터 1차(${examLabel})까지 ${N}개월 — 남은 기간에 맞춰 자동 배치` : '📆 표준 6월~3월 · 설정에서 시험일을 등록하면 내 기간에 맞춰 자동 조정'}
        </div>
      </div>
      {/* 간트 그리드 */}
      <div style={{ overflowX: 'auto', padding: 12 }}>
        <div style={{ display: 'grid', gridTemplateColumns: `70px repeat(${N}, minmax(46px,1fr))`, gridAutoRows: 'minmax(48px, auto)', minWidth: minW }}>
          {/* 좌상단 코너 */}
          <div style={{ gridColumn: 1, gridRow: 1, background: '#eef1f7', borderTopLeftRadius: 7 }} />
          {/* 월 헤더 */}
          {months.map((mm, i) => {
            const isExam = examIsLast && i === N - 1;
            return (
              <div key={i} style={{ gridColumn: i + 2, gridRow: 1, textAlign: 'center', fontSize: '0.72rem', fontWeight: 700,
                color: isExam ? '#334155' : i === curCol ? '#334155' : '#94a3b8', background: isExam ? '#fee2e2' : i === curCol ? '#dfe3fd' : '#eef1f7',
                padding: '6px 0', borderLeft: '1px solid #fff', lineHeight: 1.1 }}>
                {mm}{isExam && <div style={{ fontSize: '0.58rem', fontWeight: 800 }}>🎯시험</div>}{!isExam && i === curCol && <div style={{ fontSize: '0.58rem', fontWeight: 800 }}>오늘</div>}
              </div>
            );
          })}
          {/* 카테고리(앱 기능) 라벨 */}
          {GANTT_ROWS.map((rl, r) => (
            <div key={'lbl' + r} style={{ gridColumn: 1, gridRow: r + 2, display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontWeight: 800, fontSize: '0.64rem', color: '#475569', background: '#f8fafc', borderTop: '1px solid #eef0f2', textAlign: 'center', padding: '0 3px', lineHeight: 1.25 }}>{rl}</div>
          ))}
          {/* 배경 셀(격자) */}
          {GANTT_ROWS.flatMap((rl, r) => months.map((_, i) => (
            <div key={`bg${r}-${i}`} style={{ gridColumn: i + 2, gridRow: r + 2, borderTop: '1px solid #f1f5f9', borderLeft: '1px solid #f1f5f9',
              background: i === curCol ? 'rgba(224,231,255,0.4)' : 'transparent' }} />
          )))}
          {/* 학습 블록 — 누르면 그 앱 기능으로 이동 */}
          {pos.map((b, bi) => (
            <button key={bi} onClick={() => onOpenTask && onOpenTask({ type: b.type, subjectId })}
              style={{ gridColumn: `${b.c0 + 2} / ${b.c1 + 2}`, gridRow: b.row + 2, margin: 3, textAlign: 'left', cursor: onOpenTask ? 'pointer' : 'default',
                background: color + '14', border: `1px solid ${color}44`, borderLeft: `3px solid ${color}`, borderRadius: 8,
                padding: '5px 8px', display: 'flex', flexDirection: 'column', justifyContent: 'center', minWidth: 0 }}>
              <span style={{ fontSize: '0.58rem', fontWeight: 800, color }}>{GANTT_MODE[b.type] || ''}{onOpenTask ? ' ›' : ''}</span>
              <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#1e293b', lineHeight: 1.22, overflow: 'hidden', textOverflow: 'ellipsis' }}>{b.name}</span>
            </button>
          ))}
          {/* 🔄 회독 사이클 — 구간을 rounds개 세그먼트로 분할(뒤로 갈수록 진해짐 = 회독 누적) */}
          {cyc && (() => {
            const { c0, c1, rounds } = cyc;
            const alphaHex = (i) => (Math.round(26 + (i / Math.max(1, rounds - 1)) * 90)).toString(16).padStart(2, '0');
            return (
              <button onClick={() => onOpenTask && onOpenTask({ type: 'solve', subjectId })} title={`기출·요약 ${rounds}회독 반복 (뒤로 갈수록 빨라짐)`}
                style={{ gridColumn: `${c0 + 2} / ${c1 + 2}`, gridRow: 6, margin: 3, padding: 0, borderRadius: 8, overflow: 'hidden',
                  border: `1px solid ${color}55`, display: 'flex', cursor: onOpenTask ? 'pointer' : 'default', background: '#fff' }}>
                {Array.from({ length: rounds }).map((_, i) => (
                  <span key={i} style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '0.58rem', fontWeight: 800, color: '#1e293b',
                    background: color + alphaHex(i), borderRight: i < rounds - 1 ? '1px solid #fff' : 'none' }}>{i + 1}회</span>
                ))}
              </button>
            );
          })()}
        </div>
      </div>
      {/* AI 조정 버튼만 (구체 설명·팁 제거) */}
      {onAskAI && (
        <div style={{ padding: '0 15px 13px', display: 'flex' }}>
          <button onClick={askAI} style={{ marginLeft: 'auto', fontSize: '0.72rem', fontWeight: 800, color: '#fff', cursor: 'pointer',
            background: ACCENT, border: 'none', borderRadius: 999, padding: '6px 12px' }}>
            🤖 AI로 내 일정 맞춤 조정
          </button>
        </div>
      )}
    </section>
  );
}

const loadJSON = (k, def) => { try { return JSON.parse(localStorage.getItem(k) || 'null') ?? def; } catch { return def; } };
const saveJSON = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* SSR */ } };

const daysUntil = (yyyymmdd) => {
  if (!yyyymmdd) return null;
  const d = new Date(yyyymmdd + 'T00:00:00');
  if (isNaN(d.getTime())) return null;
  const t = new Date(); t.setHours(0, 0, 0, 0);
  return Math.ceil((d - t) / 86400000);
};
const fmtMD = (offset) => { const d = new Date(); d.setDate(d.getDate() + offset); return `${d.getMonth() + 1}/${d.getDate()}`; };
const dateKeyAt = (offset) => { const d = new Date(); d.setDate(d.getDate() + offset); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; };

const OPENABLE = new Set(['study', 'solve', 'drill', 'mock', 'review', 'essay']);
const TYPE_BADGE = {
  study: { t: 'AI 학습', c: '#334155', b: '#eef1fe' },
  solve: { t: '문제풀이', c: '#4361ee', b: '#eef1fe' },
  drill: { t: '드릴', c: '#4361ee', b: '#eef1fe' },
  mock: { t: '모의고사', c: '#334155', b: '#fef2f2' },
  review: { t: '복습·오답', c: '#ea580c', b: '#fff7ed' },
  essay: { t: '2차 논술', c: '#059669', b: '#ecfdf5' },
  custom: { t: '준비', c: '#475569', b: '#f3f4f6' },
};

// 실측 지표 → 마일스톤 자동 달성 판정 + 라이브 라벨
function evalAuto(item, metrics) {
  const a = item.auto;
  if (!a || !metrics) return null;
  const b = a.subject ? metrics.bySubject?.[a.subject] : null;
  if (a.kind === 'aiCov') { const v = b?.aiCov || 0; return { done: v >= a.need, label: `AI 커버리지 ${Math.round(v * 100)}%` }; }
  if (a.kind === 'answered') {
    const ans = b?.answered || 0, tot = b?.total || 0;
    const acc = ans ? Math.round((b.correct / ans) * 100) : 0;
    const ratio = tot ? ans / tot : 0;
    return { done: ratio >= a.need && ans >= 20, label: `기출 ${ans}/${tot} · 정답률 ${acc}%` };
  }
  if (a.kind === 'mock') { const n = metrics.mockCount || 0; return { done: n >= a.need, label: `모의 ${n}회 응시` }; }
  if (a.kind === 'reviewClear') { const d = metrics.reviewDue || 0; return { done: d === 0, label: d ? `복습 대기 ${d}` : '복습 대기 없음' }; }
  return null;
}

// 마일스톤 달성 판정(순수 함수) — 수동(prog) 우선 → 회독 목표 → 실측 자동
function computeDone(item, { prog, rounds, useAuto, metrics }) {
  const ov = prog[item.id];
  if (ov !== undefined) return ov;
  if (item.round) return (rounds[item.id] || 0) >= item.round;
  if (useAuto) { const au = evalAuto(item, metrics); if (au) return au.done; }
  return false;
}

// 동차 정밀 코칭용 프롬프트(선택적 AI 상세 조언)
function buildDongchaPrompt(plan, opts) {
  const work = opts.working ? `직장 병행(평일 ${opts.hoursWeekday}h·주말 ${opts.hoursWeekend}h)` : `전업(평일 ${opts.hoursWeekday}h·주말 ${opts.hoursWeekend}h)`;
  const ph = plan.phases.map((p) => `${p.title}(${p.label})`).join(' → ');
  return `나는 감정평가사 '동차'(같은 해 1·2차 동시 합격)를 목표로 해. 오늘 기준 1차 D-${plan.d1}, 2차 D-${plan.d2}, ${work}.\n`
    + `현재 자동 계획은 [${ph}] 단계로, 2차를 미리 벌어두고 1차 직전 8주 스퍼트 → 1차 후 2차 총력 구조야.\n`
    + `이 구조가 내 남은 기간과 상황에 현실적인지 점검하고, 무엇을 더 압축/생략하고 어디에 집중할지, 2차를 언제부터 얼마나 해야 동차가 가능한지 이 앱 기능(AI학습·기출·드릴·2차논술·모의)을 활용하는 방식으로 구체적으로 코칭해줘.`;
}

export default function Curriculum({ examDates = {}, primaryExam = '감정평가사', onOpenTask, onAskAI, onDiagnostic, metrics = null, learnCtx = null }) {
  const exam1 = examDates[`${primaryExam}_1차`] || examDates[primaryExam] || ''; // 간트 동적 축 기준(1차 시험일)
  const exam2 = examDates[`${primaryExam}_2차`] || ''; // 2차 시험일(동차 계획 기준)
  const WD = ['일', '월', '화', '수', '목', '금', '토'];
  const [stage, setStage] = useState(1);
  const [prog, setProg] = useState(() => loadJSON(PROG_KEY, {}));
  const [autoOn, setAutoOn] = useState(() => loadJSON(AUTO_KEY, true));
  const [pdates, setPdates] = useState(() => loadJSON(DATES_KEY, {})); // 단계별 목표 일자
  const [rounds, setRounds] = useState(() => loadJSON(ROUNDS_KEY, {})); // 회독 카운터
  const [placed, setPlaced] = useState({});
  const [gsubj, setGsubj] = useState('civil'); // 인강식 월별 커리큘럼 과목 선택
  const [planOpts, setPlanOptsState] = useState(getPlanOpts); // 동차 계획 옵션(하루 공부시간·직장병행)
  const [showPlanOpts, setShowPlanOpts] = useState(false);
  const [expSubj, setExpSubj] = useState(null); // 실력 현황에서 펼친 과목(진단 리포트)
  const [snSubj, setSnSubj] = useState('civil'); // 단권화 노트 과목
  const [snOpen, setSnOpen] = useState(false);
  const [snText, setSnText] = useState('');
  const [targets, setTargets] = useState(() => loadJSON('curriculum-targets-v1', { civil: 60, economics: 50, accounting: 50, realestate: 70, law: 70 }));
  const updateTarget = (sid, v) => { const next = { ...targets, [sid]: v }; setTargets(next); saveJSON('curriculum-targets-v1', next); };
  const [showTargets, setShowTargets] = useState(false); // 목표점수 설정 — 평소엔 숨김
  const [planVariant, setPlanVariant] = useState(0); // '다시 짜기' 변주
  const TODAY_KEY = 'curriculum-today-v1';
  const _now = new Date();
  const todayStr = `${_now.getFullYear()}-${String(_now.getMonth() + 1).padStart(2, '0')}-${String(_now.getDate()).padStart(2, '0')}`;
  const [todayState, setTodayState] = useState(() => {
    const s = loadJSON(TODAY_KEY, null);
    return s && s.date === todayStr ? s : { date: '', done: {} };
  });
  const [editStrat, setEditStrat] = useState(false);
  const [strat, setStrat] = useState(() => {
    const ov = loadJSON(STRAT_KEY, {});
    return STRAT_DEF.map((s) => ({ ...s, ...(ov[s.id] || {}) }));
  });

  // 내 학습상태 집계(단원별 기출·AI·SRS) — 탭 진입 시 1회, leavesBySubject 준비되면 계산
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const subjectState = useMemo(() => (learnCtx && learnCtx.leavesBySubject ? buildSubjectState(learnCtx) : null), [learnCtx && learnCtx.leavesBySubject]);
  // 동차 자동 계획 — planOpts 선언 이후에 계산(TDZ 방지)
  const plan = useMemo(() => generatePlan({ exam1, exam2, opts: planOpts, variant: planVariant, subjectState, targets }), [exam1, exam2, planOpts, planVariant, subjectState, targets]);
  const updatePlanOpts = (patch) => { const next = { ...planOpts, ...patch }; setPlanOptsState(next); setPlanOpts(next); };
  // 🤖 학습 계획(순차 완성 스케줄) — AI는 '과목 순서+일수'만 빠르게 정하고, expandDay가 매일 펼친다.
  //   오늘의 계획 + 달력이 '같은 스케줄'을 expandDay로 읽어 정확히 호응한다.
  const [aiPlan, setAiPlan] = useState(() => getAiPlan());
  const [aiBusy, setAiBusy] = useState(false);
  const [aiErr, setAiErr] = useState('');
  // 🎓 합격수기 기반 과목별 팁 — 오늘의 계획·달력에 표기
  const [passInsights, setPassInsights] = useState(null);
  useEffect(() => { loadPassInsights().then((d) => { if (d) setPassInsights(d); }); }, []);
  const [roundsTarget, setRoundsTargetState] = useState(() => { try { return Number(localStorage.getItem('curriculum-rounds-target-v1')) || 3; } catch { return 3; } });
  // 오늘 공부 가능 시간 — 미리 고를 수 있음. null이면 요일별 기본값 자동 사용.
  const defTodayHours = (_now.getDay() === 0 || _now.getDay() === 6) ? (planOpts.hoursWeekend || 8) : (planOpts.hoursWeekday || 3);
  const [todayHours, setTodayHours] = useState(null);
  // ✏️ 직접 추가한 계획 — 구조화(과목·활동·시간)·미완료 이월·인라인 편집·정렬
  const MANUAL_KEY = 'curriculum-manual-v2';
  const loadManual = () => {
    const norm = (it, d) => ({ subjectId: '', activity: '', mins: 0, date: d || todayStr, doneDate: it.done ? (d || todayStr) : null, ...it });
    const s = loadJSON(MANUAL_KEY, null);
    if (s && Array.isArray(s.items)) return s.items.map((it) => norm(it, it.date));
    const old = loadJSON('curriculum-today-manual-v1', null); // v1 마이그레이션(오늘치만)
    if (old && Array.isArray(old.items)) return old.items.map((it) => norm(it, old.date));
    return [];
  };
  const [manualTasks, setManualTasks] = useState(loadManual);
  const [manualInput, setManualInput] = useState('');
  const [manualSubj, setManualSubj] = useState('');
  const [manualAct, setManualAct] = useState('');
  const [manualMins, setManualMins] = useState(0);
  const [manualEdit, setManualEdit] = useState(null); // { id, text }
  const saveManual = (items) => { setManualTasks(items); saveJSON(MANUAL_KEY, { items }); };
  const addManual = () => {
    const t = manualInput.trim(); if (!t) return;
    saveManual([...manualTasks, { id: `m-${Date.now()}`, text: t.slice(0, 200), done: false, doneDate: null, subjectId: manualSubj, activity: manualAct, mins: manualMins, date: todayStr }]);
    setManualInput(''); setManualMins(0); // 과목·활동은 연속 추가 편의로 유지
  };
  const toggleManual = (id) => saveManual(manualTasks.map((m) => (m.id === id ? { ...m, done: !m.done, doneDate: !m.done ? todayStr : null } : m)));
  const removeManual = (id) => saveManual(manualTasks.filter((m) => m.id !== id));
  const editManual = (id, text) => saveManual(manualTasks.map((m) => (m.id === id ? { ...m, text: (text || '').slice(0, 200) } : m)));
  const moveManual = (id, dir) => { const i = manualTasks.findIndex((m) => m.id === id); const j = i + dir; if (i < 0 || j < 0 || j >= manualTasks.length) return; const arr = manualTasks.slice(); [arr[i], arr[j]] = [arr[j], arr[i]]; saveManual(arr); };
  // 표시: 미완료(과거 포함=이월) + 오늘 완료분. 과거 완료분은 보관(숨김).
  const visManual = manualTasks.filter((m) => !m.done || m.doneDate === todayStr);
  // 스케줄이 없으면(초기) 기본 순차 스케줄을 즉시 만들어 저장 — 대기 없이 계획이 바로 보인다.
  // 시험일·목표회독이 바뀌면(AI 미최적화 상태) 기본 스케줄을 재구성.
  const lbs = learnCtx && learnCtx.leavesBySubject;
  const lbsKey = lbs ? Object.keys(lbs).length : 0;
  useEffect(() => {
    if (!aiPlan) {
      const d = defaultSchedule({ exam1, exam2, rounds: roundsTarget, opts: planOpts, subjectState, leavesBySubject: lbs });
      saveSchedule(d); setAiPlan(d);
    } else if (!aiPlan.aiRefined && (aiPlan.exam1 !== exam1 || aiPlan.exam2 !== exam2 || aiPlan.rounds !== roundsTarget)) {
      const d = defaultSchedule({ exam1, exam2, rounds: roundsTarget, opts: planOpts, subjectState, base: aiPlan.base, leavesBySubject: lbs });
      saveSchedule(d); setAiPlan(d);
    } else if (lbsKey > 0 && aiPlan.poolsBuilt !== 2) {
      // 강의노트 목차가 도착하면 계획 단원을 장(章) 서수·분량으로 재구성(기존 설정 유지).
      const d = buildSchedule({ exam1, exam2, rounds: aiPlan.rounds || roundsTarget, opts: planOpts, subjectState, order: aiPlan.order, aiRefined: aiPlan.aiRefined, note: aiPlan.note, base: aiPlan.base, leavesBySubject: lbs });
      saveSchedule(d); setAiPlan(d);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [aiPlan, exam1, exam2, roundsTarget, lbsKey]);
  const runAiPlan = async () => {
    if (aiBusy) return;
    setAiBusy(true); setAiErr('');
    try {
      const p = await generateAiPlan({ exam1, exam2, rounds: roundsTarget, opts: planOpts, subjectState, leavesBySubject: lbs });
      setAiPlan(p);
      const s = { date: todayStr, done: {} }; setTodayState(s); saveJSON(TODAY_KEY, s);
    } catch (e) { setAiErr((e && e.message) || 'AI 계획 생성 실패'); }
    finally { setAiBusy(false); }
  };
  // 목표 회독 변경 → 순서 유지한 채 스케줄 재구성(계획이 회독수에 따라 바뀜)
  const setRoundsTarget = (v) => {
    setRoundsTargetState(v);
    try { localStorage.setItem('curriculum-rounds-target-v1', String(v)); } catch { /* */ }
    const d = buildSchedule({ exam1, exam2, rounds: v, opts: planOpts, subjectState, order: aiPlan && aiPlan.order, aiRefined: aiPlan && aiPlan.aiRefined, note: aiPlan && aiPlan.note, base: aiPlan && aiPlan.base, leavesBySubject: lbs });
    saveSchedule(d); setAiPlan(d);
  };
  // 오늘의 계획 = 스케줄에서 오늘 날짜를 펼침. 완료 토글은 인덱스 기반.
  const aiToday = expandDay(_now, aiPlan, todayHours || defTodayHours);
  const todayGenerated = !!aiToday;
  const toggleTaskDone = (i) => { const done = { ...todayState.done, [i]: !todayState.done[i] }; const s = { date: todayStr, done }; setTodayState(s); saveJSON(TODAY_KEY, s); };
  const todayDoneN = Object.values(todayState.done).filter(Boolean).length;
  // 오늘 배정 태스크(범위=좌 오늘의 계획, 루틴=우측 스텝 공용)
  const todayTasks = (aiToday && aiToday.subs ? aiToday.subs : []).map((s, i) => ({ i, subjectId: s.sid, unit: s.unit, kind: s.kind, activity: s.activity || s.kind, idx: s.idx, total: s.total, hier: s.hier, level: s.level, sub: s.sub, div: s.div, chap: s.chap, round: s.round, parallel: s.parallel, stage: s.stage }));
  // ⏱ 오늘 공부 가능 시간 칩 — AI로 짜기 전에 미리 선택(무채색)
  const hoursSelector = (
    <div style={{ marginBottom: 12 }}>
      <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#475569', marginBottom: 7 }}>⏱ 오늘 공부 가능 시간</div>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
        {[2, 3, 4, 5, 6, 8, 10].map((h) => {
          const on = (todayHours || defTodayHours) === h;
          return (
            <button key={h} onClick={() => setTodayHours(h)} style={{
              fontSize: '0.72rem', fontWeight: 800, borderRadius: 8, padding: '6px 12px', cursor: 'pointer',
              border: on ? '1.5px solid #334155' : '1px solid #e5e7eb', background: on ? '#f1f5f9' : '#fff', color: on ? '#1e293b' : '#94a3b8',
            }}>{h}시간</button>
          );
        })}
      </div>
    </div>
  );

  const PHASES = stage === 1 ? PHASES_1 : PHASES_2;
  const examKey = stage === 1
    ? (examDates[`${primaryExam}_1차`] || examDates[primaryExam])
    : examDates[`${primaryExam}_2차`];
  const T = daysUntil(examKey);
  const useAuto = autoOn && stage === 1 && metrics;

  // 마일스톤 달성 여부 — 수동(prog) 우선 → 회독 목표 도달 → 실측 자동
  const isDone = (item) => computeDone(item, { prog, rounds, useAuto, metrics });

  // 홈 카드용 1차 완료율 요약 발행 (회독·실측까지 반영)
  useEffect(() => {
    const items = PHASES_1.flatMap((p) => p.items);
    const opts = { prog, rounds, useAuto: !!(autoOn && metrics), metrics };
    const done = items.filter((it) => computeDone(it, opts)).length;
    saveJSON('curriculum-summary-v1', { p1Done: done, p1Total: items.length });
  }, [prog, rounds, autoOn, metrics]);

  // 단권화 노트 — 과목 바뀌면 그 과목 노트 로드
  useEffect(() => { try { setSnText(localStorage.getItem('subnote-v1-' + snSubj) || ''); } catch { setSnText(''); } }, [snSubj]);
  // 회독 카운터 증감(0 ~ 목표)
  const bumpRound = (item, delta) => {
    const cur = rounds[item.id] || 0;
    const next = Math.max(0, Math.min(item.round, cur + delta));
    const nr = { ...rounds, [item.id]: next };
    setRounds(nr); saveJSON(ROUNDS_KEY, nr);
    if (prog[item.id] !== undefined) { const np = { ...prog }; delete np[item.id]; setProg(np); saveJSON(PROG_KEY, np); } // 회독으로 조작 시 수동 override 해제
  };

  // 단계 창(window): 사용자가 넣은 목표 일자를 우선 사용하고, 없으면 시험일(D-day) 비중으로 자동 계산.
  // 각 단계의 시작 = 직전 단계의 끝(없으면 오늘). 목표 일자만 넣어도 시험일 없이 동작한다.
  const windows = useMemo(() => {
    const timed = PHASES.filter((p) => p.w > 0);
    const map = {};
    let prevEnd = 0; // 오늘 기준 offset(일)
    let cum = 0;
    for (const p of timed) {
      cum += p.w;
      const autoEnd = (T != null && T > 0) ? Math.round(T * cum) : null;
      const dstr = pdates[p.id];
      let endOff = dstr ? daysUntil(dstr) : null;
      if (endOff == null) endOff = autoEnd;
      if (endOff == null) { map[p.id] = null; continue; } // 일정 없음
      const startOff = prevEnd;
      map[p.id] = {
        startOff, endOff, dateStr: dstr || dateKeyAt(endOff), explicit: !!dstr,
        label: `${fmtMD(startOff)} ~ ${fmtMD(endOff)}`, days: Math.max(1, endOff - startOff),
      };
      prevEnd = endOff;
    }
    return map;
  }, [T, PHASES, pdates]);

  const toggle = (item) => {
    const cur = isDone(item);
    const next = { ...prog, [item.id]: !cur };
    setProg(next); saveJSON(PROG_KEY, next);
  };
  const flipAuto = () => { const v = !autoOn; setAutoOn(v); saveJSON(AUTO_KEY, v); };

  // 단계별 목표 일자 편집
  const setDate = (pid, v) => {
    const next = { ...pdates }; if (v) next[pid] = v; else delete next[pid];
    setPdates(next); saveJSON(DATES_KEY, next);
  };
  // 시험일(D-day) 비중으로 목표 일자 일괄 채우기
  const autofillDates = () => {
    if (T == null || T <= 0) return;
    const next = { ...pdates }; let cum = 0;
    for (const p of PHASES.filter((x) => x.w > 0)) { cum += p.w; next[p.id] = dateKeyAt(Math.round(T * cum)); }
    setPdates(next); saveJSON(DATES_KEY, next);
  };
  const clearDates = () => {
    const next = { ...pdates }; PHASES.forEach((p) => { delete next[p.id]; });
    setPdates(next); saveJSON(DATES_KEY, next);
  };
  const hasDates = PHASES.some((p) => pdates[p.id]);

  const phaseStat = (p) => {
    const done = p.items.filter(isDone).length;
    return { done, total: p.items.length, pct: p.items.length ? Math.round((done / p.items.length) * 100) : 0 };
  };
  const currentPhaseId = useMemo(() => {
    for (const p of PHASES) { if (p.items.some((it) => !isDone(it))) return p.id; }
    return PHASES[PHASES.length - 1].id;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [prog, autoOn, metrics, PHASES, rounds]);

  const [open, setOpen] = useState({});
  const isOpen = (id) => (id in open ? open[id] : id === currentPhaseId);
  const toggleOpen = (id) => setOpen((o) => ({ ...o, [id]: !isOpen(id) }));

  const allItems = PHASES.flatMap((p) => p.items);
  const overallDone = allItems.filter(isDone).length;
  const overallPct = Math.round((overallDone / allItems.length) * 100);

  const updateStrat = (id, patch) => {
    setStrat((prev) => prev.map((s) => (s.id === id ? { ...s, ...patch } : s)));
    const ov = loadJSON(STRAT_KEY, {}); ov[id] = { ...(ov[id] || {}), ...patch }; saveJSON(STRAT_KEY, ov);
  };
  const resetStrat = () => { saveJSON(STRAT_KEY, {}); setStrat(STRAT_DEF.map((s) => ({ ...s }))); };

  const placeInPlanner = (p) => {
    const w = windows[p.id]; if (!w) return;
    const plans = loadJSON(PKEY, {}) || {};
    const base = Math.max(0, w.startOff);              // 과거 날짜에는 배치하지 않음
    const end = Math.max(base, w.endOff);
    const span = Math.max(1, end - base);
    p.items.forEach((it, i) => {
      const off = base + Math.round(span * (i / Math.max(1, p.items.length)));
      const dk = dateKeyAt(off);
      const sm = it.subject ? SMAP[it.subject] : null;
      const text = (sm ? `${sm.short} · ` : '') + it.label + (it.round ? ` · ${it.round}회독` : '');
      const task = { id: `${dk}_${Date.now()}_${i}`, type: it.type, ...(it.subject ? { subjectId: it.subject } : {}), ...(it.round ? { round: it.round } : {}), text, done: false, fromCurriculum: true };
      plans[dk] = [...(plans[dk] || []), task];
    });
    saveJSON(PKEY, plans);
    setPlaced((m) => ({ ...m, [p.id]: true }));
  };

  const ringColor = overallPct >= 80 ? '#16a34a' : overallPct >= 40 ? '#f59e0b' : '#334155';
  const curTitle = PHASES.find((p) => p.id === currentPhaseId)?.title;
  const stratView = stage === 1 ? strat : STRAT_2;
  // 히어로 D-day: 시험일이 있으면 그걸, 없으면 마지막 단계의 목표 일자를 기준으로
  const lastTimed = PHASES.filter((p) => p.w > 0).slice(-1)[0];
  const planEndOff = lastTimed ? windows[lastTimed.id]?.endOff : null;
  const heroFromExam = T != null && T > 0;
  const heroD = heroFromExam ? T : (planEndOff != null && planEndOff > 0 ? planEndOff : null);

  const swBtn = (n, label) => (
    <button onClick={() => { setStage(n); setOpen({}); setEditStrat(false); }} style={{
      flex: 1, padding: '9px', borderRadius: 9, cursor: 'pointer', fontSize: '0.78rem', fontWeight: 800,
      border: 'none', background: stage === n ? '#fff' : 'transparent',
      color: stage === n ? '#334155' : 'rgba(255,255,255,0.85)',
      boxShadow: stage === n ? '0 1px 4px rgba(0,0,0,0.12)' : 'none',
    }}>{label}</button>
  );

  return (
    <div className="app-container">
      <div className="screen-head" style={{ padding: '0 4px' }}>
        <h1 className="screen-title">🎓 합격 커리큘럼</h1>
      </div>
      <main className="main-content" style={{ marginTop: 16 }}>

        {/* 📅 이 앱으로 합격하는 월별 학습 플랜(간트) — 최상단, 전폭 */}
        <div style={{ display: 'flex', alignItems: 'center', margin: '0 4px 8px', flexWrap: 'wrap', gap: 8 }}>
          <span style={{ fontSize: '0.86rem', fontWeight: 800, color: '#1e293b' }}>📅 월별 학습 플랜</span>
          <span style={{ fontSize: '0.64rem', color: '#94a3b8' }}>이 앱으로 합격하는</span>
          <button onClick={() => setShowTargets((v) => !v)} style={{ marginLeft: 'auto', fontSize: '0.64rem', fontWeight: 800, cursor: 'pointer', borderRadius: 999, padding: '4px 10px', border: showTargets ? `1px solid ${ACCENT}` : '1px solid #e5e7eb', background: showTargets ? ACCENT_BG : '#fff', color: showTargets ? ACCENT : '#94a3b8' }}>
            🎯 목표점수 {showTargets ? '▲' : '▾'}
          </button>
        </div>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 10 }}>
          {GANTT_ORDER.map((id) => {
            const s = SMAP[id]; const on = gsubj === id;
            return (
              <button key={id} onClick={() => setGsubj(id)} style={{
                fontSize: '0.72rem', fontWeight: 800, borderRadius: 999, padding: '6px 12px', cursor: 'pointer',
                border: on ? `1.5px solid ${ACCENT}` : '1px solid #e5e7eb',
                background: on ? ACCENT_BG : '#fff', color: on ? ACCENT : '#94a3b8',
              }}>{s.icon} {s.short}</button>
            );
          })}
        </div>
        {/* 🎯 선택 과목 목표점수 — 평소엔 숨김, 토글로 설정. 여기서 바꾸면 오늘 계획 우선순위가 바뀜 */}
        {showTargets && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap', marginBottom: 10, padding: '9px 12px', background: ACCENT_BG, border: `1px solid ${ACCENT_BR}`, borderRadius: 12 }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#475569' }}>🎯 {SMAP[gsubj] ? SMAP[gsubj].short : ''} 목표점수</span>
          <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            {[40, 50, 60, 70, 80, 90].map((v) => {
              const on = (targets[gsubj] ?? 60) === v;
              return (
                <button key={v} onClick={() => updateTarget(gsubj, v)} style={{ fontSize: '0.72rem', fontWeight: 800, borderRadius: 7, padding: '4px 9px', cursor: 'pointer', border: on ? `1.5px solid ${ACCENT}` : '1px solid #d6dae1', background: '#fff', color: on ? ACCENT : '#94a3b8' }}>{v}</button>
              );
            })}
          </div>
          {subjectState && subjectState[gsubj] && subjectState[gsubj].avgAccuracy != null && (
            <span style={{ marginLeft: 'auto', fontSize: '0.64rem', color: '#94a3b8' }}>현재 {subjectState[gsubj].avgAccuracy}%</span>
          )}
          <span style={{ fontSize: '0.64rem', color: '#94a3b8', flexBasis: '100%' }}>목표와 격차가 큰 과목을 오늘 계획이 먼저 잡아요</span>
        </div>
        )}
        <GanttCard subjectId={gsubj} onOpenTask={onOpenTask} exam1={exam1} onAskAI={onAskAI} />

        {/* 히어로 */}
        <section style={{ borderRadius: 18, padding: '18px', marginBottom: 14, color: '#fff', background: INK, boxShadow: 'var(--shadow-md)' }}>
          {/* 1차/2차 전환 */}
          <div style={{ display: 'flex', gap: 4, background: 'rgba(255,255,255,0.15)', borderRadius: 11, padding: 4, marginBottom: 16 }}>
            {swBtn(1, '1차 (객관식)')}
            {swBtn(2, '2차 (논술)')}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <div style={{ position: 'relative', width: 74, height: 74, flexShrink: 0 }}>
              <div style={{ width: '100%', height: '100%', borderRadius: '50%', background: `conic-gradient(${ringColor} ${overallPct * 3.6}deg, rgba(255,255,255,0.22) 0deg)`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ width: 56, height: 56, borderRadius: '50%', background: '#3b1f7a', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                  <span style={{ fontSize: '1.12rem', fontWeight: 900, lineHeight: 1 }}>{overallPct}%</span>
                  <span style={{ fontSize: '0.58rem', opacity: 0.85, marginTop: 1 }}>{overallDone}/{allItems.length}</span>
                </div>
              </div>
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: '0.72rem', opacity: 0.9, fontWeight: 600 }}>{stage === 1 ? '1차 합격 로드맵' : '2차 합격 로드맵'}</div>
              <div style={{ fontSize: '1rem', fontWeight: 800, margin: '2px 0 6px' }}>지금은 <span style={{ color: '#ffffff' }}>{curTitle}</span> 단계</div>
              {heroD != null ? (
                <div style={{ fontSize: '0.78rem', fontWeight: 700 }}>
                  {stage === 1 ? '1차' : '2차'}{heroFromExam ? '까지' : ' 목표 완료까지'} <b style={{ color: '#ffffff', fontSize: '0.86rem' }}>D-{heroD}</b>
                  <span style={{ opacity: 0.75, fontWeight: 600 }}> · {heroFromExam ? '단계별 일정 자동 배치됨' : '단계별 목표 일자 기준'}</span>
                </div>
              ) : (
                <div style={{ fontSize: '0.72rem', opacity: 0.9, fontWeight: 600 }}>{stage === 1 ? '1차' : '2차'} 시험일을 등록하거나, 아래에서 단계별 목표 일자를 넣어보세요</div>
              )}
            </div>
          </div>
          <div style={{ marginTop: 12, fontSize: '0.72rem', opacity: 0.85, lineHeight: 1.6, borderTop: '1px solid rgba(255,255,255,0.18)', paddingTop: 10 }}>
            📚 실제 감정평가사 합격수기를 바탕으로 구성했습니다.
          </div>
        </section>

        {/* ── PC 2단: 좌(오늘의 계획) · 우(나머지) ── */}
        <div className="curr-2col">
        <div className="curr-left">
        {/* ⭐ 오늘의 계획 — 플래너 스타일, AI 버튼으로 생성(1차/2차 무관, 항상 표시) */}
        <section style={{ background: '#fff', borderRadius: 16, boxShadow: 'var(--shadow-md)', padding: 16, marginBottom: 14 }}>
          {/* 플래너식 그라디언트 히어로 */}
          <div style={{ borderRadius: 14, padding: '16px', background: ACCENT, color: '#fff', marginBottom: todayGenerated ? 14 : 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
              <span style={{ fontWeight: 800, fontSize: '1rem' }}>⭐ 오늘의 계획</span>
              <span style={{ fontSize: '0.64rem', background: 'rgba(255,255,255,0.18)', borderRadius: 999, padding: '2px 9px', fontWeight: 700 }}>{plan.today.phaseTitle}</span>
              <span style={{ marginLeft: 'auto', fontSize: '0.72rem', fontWeight: 700 }}>{WD[plan.today.dow]}요일 · {plan.today.hours}시간</span>
            </div>
            <div style={{ fontSize: '0.64rem', opacity: 0.92, marginTop: 7, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              <span style={{ background: 'rgba(255,255,255,0.16)', borderRadius: 999, padding: '2px 8px', fontWeight: 700 }}>
                {plan.today.dataDriven ? '📊 내 학습기록 반영' : '📊 기록 쌓이면 개인화'}
              </span>
              {metrics && metrics.reviewDue > 0 && (
                <span style={{ background: 'rgba(253,230,138,0.28)', borderRadius: 999, padding: '2px 8px', fontWeight: 800, color: '#ffffff' }}>🔔 복습 {metrics.reviewDue}개 도래</span>
              )}
            </div>
            {(todayGenerated || visManual.length > 0) && (() => {
              const md = visManual.filter((m) => m.done).length;
              const n = (aiToday && aiToday.subs ? aiToday.subs.length : 0) + visManual.length;
              const dn = todayDoneN + md;
              return (
                <div style={{ marginTop: 12 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', fontWeight: 700, marginBottom: 5, opacity: 0.95 }}>
                    <span>완료 {dn} / {n}</span>
                    <span>{n ? Math.round((dn / n) * 100) : 0}%</span>
                  </div>
                  <div style={{ height: 6, borderRadius: 3, background: 'rgba(255,255,255,0.25)', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: `${n ? (dn / n) * 100 : 0}%`, background: '#fde68a', transition: 'width .2s' }} />
                  </div>
                </div>
              );
            })()}
          </div>

          {!todayGenerated ? (
            <div style={{ padding: '14px 4px 4px' }}>
              {hoursSelector}
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '0.78rem', color: '#94a3b8', margin: '4px 0 14px', lineHeight: 1.7 }}>
                  내 진도·시험일·목표 회독에 맞춰<br />AI가 오늘 할 일을 <b>단원·분량까지</b> 짜드려요
                </div>
                <button onClick={runAiPlan} disabled={aiBusy} style={{
                  width: '100%', padding: '13px', borderRadius: 12, border: 'none', cursor: aiBusy ? 'default' : 'pointer',
                  background: aiBusy ? '#c6cefb' : ACCENT, color: '#fff', fontWeight: 800, fontSize: '0.86rem',
                  boxShadow: '0 10px 24px -12px rgba(79,70,229,0.6)',
                }}>{aiBusy ? '✨ AI가 계획 짜는 중…' : '🤖 오늘 계획 AI로 짜기'}</button>
                {aiErr && <div style={{ marginTop: 10, fontSize: '0.72rem', color: '#334155', background: '#f1f5f9', borderRadius: 9, padding: '8px 10px', lineHeight: 1.5 }}>{aiErr}</div>}
              </div>
            </div>
          ) : (() => {
            // 순차 완성 — 오늘 배정된 과목(주 과목 + 완성과목 유지복습)만 표시
            const tasks = (aiToday.subs || []).map((s, i) => ({ i, subjectId: s.sid, unit: s.unit, amount: s.amount, kind: s.kind, activity: s.activity || s.kind, idx: s.idx, total: s.total, hier: s.hier, level: s.level, sub: s.sub, div: s.div, chap: s.chap, round: s.round, parallel: s.parallel, stage: s.stage }));
            // 태스크 1건 — 단원 + 앱 내 구체 학습 경로(클릭하면 그 기능으로 이동). 과목 헤더는 바깥에서 렌더.
            // 좌측 오늘의 계획 — 간단한 학습 범위(단원)만. 구체 경로는 우측 '오늘의 학습 루틴'.
            const taskRow = (t) => {
              const done = !!todayState.done[t.i];
              return (
                <div key={t.i} style={{ display: 'flex', alignItems: 'center', gap: 9, marginBottom: 6,
                  background: done ? '#f0fdf4' : '#fafafa', border: `1px solid ${done ? '#bbf7d0' : '#eef0f2'}`, borderRadius: 9, padding: '9px 11px' }}>
                  <button onClick={() => toggleTaskDone(t.i)} aria-label="완료 토글" style={{ width: 22, height: 22, borderRadius: '50%', flexShrink: 0, cursor: 'pointer',
                    border: `2px solid ${done ? '#16a34a' : '#cbd5e1'}`, background: done ? '#16a34a' : '#fff', color: '#fff', fontSize: '0.64rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{done ? '✓' : ''}</button>
                  {(t.hier || t.total != null) ? <span title={`이 과목 ${t.total}단원 중 ${t.idx + 1}번째`} style={{ flexShrink: 0, fontSize: '0.58rem', fontWeight: 800, color: '#fff', background: '#4361ee', borderRadius: 5, padding: '2px 6px', whiteSpace: 'nowrap' }}>{t.hier || `${t.idx + 1}단원`}</span> : null}
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 3, fontSize: '0.58rem', fontWeight: 800, flexShrink: 0, color: '#475569', background: '#f1f5f9', borderRadius: 5, padding: '2px 7px' }}>{(ACTIVITY_META[t.activity] || {}).icon || ''} {(ACTIVITY_META[t.activity] || {}).label || t.activity}{t.parallel ? ' · 병행' : ''}</span>
                  <span style={{ flex: 1, minWidth: 0, fontSize: '0.78rem', fontWeight: 700, color: done ? '#94a3b8' : '#1e293b', textDecoration: done ? 'line-through' : 'none', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{t.unit}{t.round > 1 ? <span style={{ marginLeft: 5, fontSize: '0.58rem', fontWeight: 700, color: '#94a3b8' }}>{t.round}회독</span> : null}</span>
                </div>
              );
            };
            return (
            <>
              {/* 8과목 보드 — 오늘 배정이 없어도 과목명은 항상, 각 구역은 카드+여백으로 구분 */}
              {[1, 2].map((stg) => {
                const subs = SUBJECTS.filter((s) => s.stage === stg);
                const stgHas = subs.some((sub) => tasks.some((t) => t.subjectId === sub.id));
                return (
                  <div key={stg}>
                    {/* 1차/2차 소제목 */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, margin: stg === 1 ? '0 2px 8px' : '13px 2px 8px' }}>
                      <span style={{ fontSize: '0.78rem', fontWeight: 800, color: stg === 2 ? '#7c3aed' : '#4361ee' }}>{stg === 1 ? '1차' : '2차'}</span>
                      <span style={{ fontSize: '0.64rem', color: '#94a3b8', fontWeight: 700 }}>{stg === 1 ? '객관식 5과목' : '논술 3과목'}</span>
                      <div style={{ flex: 1, height: 1, background: '#eef0f3' }} />
                      {!stgHas && <span style={{ fontSize: '0.64rem', color: '#cbd5e1', fontWeight: 700 }}>오늘 배정 없음</span>}
                    </div>
                    {subs.map((sub) => {
                      const col = SUBJECT_COLORS[sub.id] || '#94a3b8';
                      const subTasks = tasks.filter((t) => t.subjectId === sub.id);
                      const has = subTasks.length > 0;
                      return (
                        <div key={sub.id} style={{ marginBottom: 9, padding: has ? '11px 12px 11px 13px' : '8px 12px 8px 13px', borderRadius: 11,
                          background: has ? '#fff' : '#fafbfc', border: `1px solid ${has ? '#e6e9ef' : '#edeff3'}`,
                          borderLeft: `4px solid ${has ? col : '#dfe3ea'}`, boxShadow: has ? '0 1px 4px rgba(15,23,42,0.04)' : 'none' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: has ? 8 : 0, paddingBottom: has ? 7 : 0, borderBottom: has ? '1px solid #f4f5f7' : 'none' }}>
                            <span style={{ width: 10, height: 10, borderRadius: '50%', background: has ? col : '#e2e8f0', flexShrink: 0 }} />
                            <span style={{ fontSize: '0.78rem', fontWeight: 800, color: has ? '#1e293b' : '#9aa4b2' }}>{sub.short}</span>
                            {!has && <span style={{ marginLeft: 'auto', fontSize: '0.64rem', color: '#cbd5e1', fontWeight: 700 }}>오늘 배정 없음</span>}
                          </div>
                          {has && subTasks.map(taskRow)}
                        </div>
                      );
                    })}
                  </div>
                );
              })}
              {aiErr && <div style={{ marginTop: 10, fontSize: '0.72rem', color: '#334155', background: '#f1f5f9', borderRadius: 9, padding: '8px 10px' }}>{aiErr}</div>}
              <div style={{ marginTop: 14 }}>{hoursSelector}</div>
              <button onClick={runAiPlan} disabled={aiBusy} style={{
                width: '100%', padding: '10px', borderRadius: 10, cursor: aiBusy ? 'default' : 'pointer',
                border: 'none', background: aiBusy ? '#c6cefb' : ACCENT, color: '#fff', fontWeight: 800, fontSize: '0.78rem',
              }}>{aiBusy ? '✨ 최적화 중…' : '🤖 AI로 내 진도 맞춤 최적화'}</button>
            </>
            );
          })()}

          {/* ✏️ 직접 추가한 계획 — 과목·활동·시간 구조화 · 미완료 이월 · 편집/정렬 · 딥링크 */}
          <div style={{ marginTop: 20, paddingTop: 16, borderTop: '1px solid #f1f5f9' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 11 }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#94a3b8' }}>✏️ 직접 추가한 계획</span>
              {visManual.length > 0 && (() => { const mins = visManual.reduce((s, m) => s + (m.mins || 0), 0); return (
                <span style={{ marginLeft: 'auto', fontSize: '0.64rem', fontWeight: 700, color: '#94a3b8' }}>{visManual.filter((m) => m.done).length}/{visManual.length} 완료{mins ? ` · ${mins}분` : ''}</span>
              ); })()}
            </div>
            {visManual.map((m, mi) => {
              const msub = SUBJECTS.find((x) => x.id === m.subjectId);
              const mcol = msub ? (SUBJECT_COLORS[m.subjectId] || '#94a3b8') : '#94a3b8';
              const carried = m.date && m.date < todayStr && !m.done;
              const actionable = m.subjectId && m.activity && MANUAL_TYPE[m.activity];
              const editing = manualEdit && manualEdit.id === m.id;
              return (
                <div key={m.id} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8,
                  background: m.done ? '#f0fdf4' : '#fafafa', border: `1px solid ${m.done ? '#bbf7d0' : '#eef0f2'}`, borderRadius: 10, padding: '10px 11px' }}>
                  <button onClick={() => toggleManual(m.id)} aria-label="완료 토글" style={{ width: 21, height: 21, borderRadius: '50%', flexShrink: 0, cursor: 'pointer',
                    border: `2px solid ${m.done ? '#16a34a' : '#cbd5e1'}`, background: m.done ? '#16a34a' : '#fff', color: '#fff', fontSize: '0.62rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{m.done ? '✓' : ''}</button>
                  {msub && <span style={{ flexShrink: 0, fontSize: '0.58rem', fontWeight: 800, color: '#fff', background: mcol, borderRadius: 5, padding: '2px 6px', whiteSpace: 'nowrap' }}>{msub.short}{m.activity ? ` · ${m.activity}` : ''}</span>}
                  {carried && <span title="지난 날 못 끝낸 계획이 넘어왔어요" style={{ flexShrink: 0, fontSize: '0.56rem', fontWeight: 800, color: '#b45309', background: '#fef3c7', borderRadius: 5, padding: '2px 5px' }}>이월</span>}
                  {editing ? (
                    <input autoFocus value={manualEdit.text} onChange={(e) => setManualEdit({ id: m.id, text: e.target.value })}
                      onKeyDown={(e) => { if (e.key === 'Enter') { editManual(m.id, manualEdit.text); setManualEdit(null); } if (e.key === 'Escape') setManualEdit(null); }}
                      onBlur={() => { editManual(m.id, manualEdit.text); setManualEdit(null); }}
                      style={{ flex: 1, minWidth: 0, fontSize: '15px', padding: '4px 7px', border: `1px solid ${ACCENT}`, borderRadius: 7, boxSizing: 'border-box' }} />
                  ) : (
                    <span onDoubleClick={() => setManualEdit({ id: m.id, text: m.text })} title="더블클릭하면 수정" style={{ flex: 1, minWidth: 0, fontSize: '0.78rem', fontWeight: 600, lineHeight: 1.5, wordBreak: 'break-word', cursor: 'text',
                      color: m.done ? '#94a3b8' : '#1e293b', textDecoration: m.done ? 'line-through' : 'none' }}>{m.text}{m.mins ? <span style={{ marginLeft: 6, fontSize: '0.62rem', fontWeight: 700, color: '#94a3b8' }}>{m.mins}분</span> : null}</span>
                  )}
                  {actionable && !editing && <button onClick={() => onOpenTask && onOpenTask({ type: MANUAL_TYPE[m.activity], subjectId: m.subjectId })} title="이 기능 열기" style={{ flexShrink: 0, fontSize: '0.6rem', fontWeight: 800, color: ACCENT, background: '#eef1fe', border: 'none', borderRadius: 6, padding: '3px 7px', cursor: 'pointer' }}>▶ 열기</button>}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 1, flexShrink: 0 }}>
                    <button onClick={() => moveManual(m.id, -1)} disabled={mi === 0} aria-label="위로" style={{ background: 'none', border: 'none', color: mi === 0 ? '#e2e8f0' : '#94a3b8', cursor: mi === 0 ? 'default' : 'pointer', fontSize: '0.6rem', lineHeight: 1, padding: 0 }}>▲</button>
                    <button onClick={() => moveManual(m.id, 1)} disabled={mi === visManual.length - 1} aria-label="아래로" style={{ background: 'none', border: 'none', color: mi === visManual.length - 1 ? '#e2e8f0' : '#94a3b8', cursor: mi === visManual.length - 1 ? 'default' : 'pointer', fontSize: '0.6rem', lineHeight: 1, padding: 0 }}>▼</button>
                  </div>
                  <button onClick={() => removeManual(m.id)} aria-label="삭제" style={{ flexShrink: 0, background: 'none', border: 'none', color: '#c1c7cf', cursor: 'pointer', fontSize: '0.86rem', padding: '0 2px' }}>✕</button>
                </div>
              );
            })}
            {/* 입력 + 옵션(과목·활동·시간) */}
            <div style={{ marginTop: visManual.length ? 6 : 0, background: '#fff', border: '1px solid #eef0f2', borderRadius: 10, padding: 9 }}>
              <div style={{ display: 'flex', gap: 8 }}>
                <input value={manualInput} onChange={(e) => setManualInput(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') addManual(); }}
                  placeholder="예: 탄력성 기출 20문제 / 판례 정리"
                  style={{ flex: 1, minWidth: 0, fontSize: '15px', padding: '10px', border: '1px solid #e5e7eb', borderRadius: 9, background: '#fff', color: '#1e293b', boxSizing: 'border-box' }} />
                <button onClick={addManual} disabled={!manualInput.trim()} style={{ flexShrink: 0, padding: '0 16px', borderRadius: 9, border: 'none', cursor: manualInput.trim() ? 'pointer' : 'default',
                  background: manualInput.trim() ? ACCENT : '#c6cefb', color: '#fff', fontWeight: 800, fontSize: '0.78rem' }}>추가</button>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 8, flexWrap: 'wrap' }}>
                <select value={manualSubj} onChange={(e) => { setManualSubj(e.target.value); if (!e.target.value) setManualAct(''); }}
                  style={{ fontSize: '0.7rem', fontWeight: 700, color: manualSubj ? '#334155' : '#94a3b8', border: '1px solid #e5e7eb', borderRadius: 7, padding: '5px 8px', background: '#fff', cursor: 'pointer' }}>
                  <option value="">＋ 과목 연결(선택)</option>
                  {SUBJECTS.map((s) => <option key={s.id} value={s.id}>{s.short}</option>)}
                </select>
                {manualSubj && ['학습', '문제풀이', '드릴', '복습'].map((a) => (
                  <button key={a} onClick={() => setManualAct(manualAct === a ? '' : a)} style={{ fontSize: '0.66rem', fontWeight: 800, borderRadius: 7, padding: '5px 9px', cursor: 'pointer',
                    border: manualAct === a ? `1.5px solid ${ACCENT}` : '1px solid #e5e7eb', background: manualAct === a ? '#eef1fe' : '#fff', color: manualAct === a ? '#334155' : '#94a3b8' }}>{a}</button>
                ))}
                <span style={{ marginLeft: 'auto', display: 'inline-flex', gap: 4, alignItems: 'center' }}>
                  <span style={{ fontSize: '0.7rem', color: '#cbd5e1' }}>⏱</span>
                  {[20, 40, 60, 90].map((mm) => (
                    <button key={mm} onClick={() => setManualMins(manualMins === mm ? 0 : mm)} style={{ fontSize: '0.64rem', fontWeight: 800, borderRadius: 6, padding: '4px 7px', cursor: 'pointer',
                      border: manualMins === mm ? `1.5px solid ${ACCENT}` : '1px solid #e5e7eb', background: manualMins === mm ? '#eef1fe' : '#fff', color: manualMins === mm ? '#334155' : '#94a3b8' }}>{mm}</button>
                  ))}
                </span>
              </div>
            </div>
          </div>
        </section>
        </div>{/* /curr-left */}
        <div className="curr-right">

        {/* 📅 월별·일별 학습 달력 — 우측 최상단 */}
        <CurriculumCalendar exam1={exam1} exam2={exam2} onOpenTask={onOpenTask} schedule={aiPlan} rounds={roundsTarget} onRoundsChange={setRoundsTarget} insights={passInsights} />

        {/* 🔀 오늘의 학습 루틴 — 오늘 배정 과목을 앱 어디서 어떻게 학습할지(구체 경로) */}
        <section style={{ background: '#fff', border: '1px solid #eceff3', borderRadius: 16, boxShadow: 'var(--shadow-md)', marginBottom: 14, padding: 15 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ fontSize: '0.86rem', fontWeight: 800, color: '#1e293b' }}>🔀 오늘의 학습 루틴</span>
            <span style={{ fontSize: '0.64rem', color: '#94a3b8', fontWeight: 700 }}>앱에서 순서대로</span>
          </div>
          <div style={{ fontSize: '0.72rem', color: '#94a3b8', margin: '4px 0 12px', lineHeight: 1.5 }}>AI 학습의 실제 기능(이론·심화·진단·암기시트 등)으로 단계를 안내합니다 · <b style={{ color: '#475569' }}>회독이 오를수록 스텝·학습량이 늘어납니다</b></div>
          {todayTasks.length === 0 ? (
            <div style={{ fontSize: '0.72rem', color: '#94a3b8', textAlign: 'center', padding: '18px 8px', lineHeight: 1.6 }}>오늘 배정된 학습이 없어요<br />왼쪽 오늘의 계획에서 🤖 로 생성하세요</div>
          ) : todayTasks.map((t) => {
            const sub = SUBJECTS.find((x) => x.id === t.subjectId);
            const col = SUBJECT_COLORS[t.subjectId] || '#94a3b8';
            const _leaves = (learnCtx && learnCtx.leavesBySubject && learnCtx.leavesBySubject[t.subjectId]) || [];
            // 클릭 시 그 장의 '첫 단원'으로 이동(어느 부분인지 바로 찾기). 없으면 이름 매칭 폴백.
            const leaf = _leaves.find((l) => l && l.path && (!t.div || l.path[0] === t.div) && l.path[1] && t.chap && l.path[1].includes(t.chap))
              || _leaves.find((l) => l && (l.title === t.unit || (l.path && l.path[l.path.length - 1] === t.unit)));
            const steps = planSteps(t.activity, t.round, t.stage, t.subjectId);
            const am = ACTIVITY_META[t.activity] || { icon: '', label: t.activity };
            const go = (st) => onOpenTask && onOpenTask({ type: st.type, subjectId: t.subjectId, leafId: leaf ? leaf.id : undefined, mode: st.mode, docTab: st.docTab });
            return (
              <div key={t.i} style={{ marginBottom: 11, padding: '11px 12px 11px 13px', borderRadius: 11, background: '#fff',
                border: '1px solid #e6e9ef', borderLeft: `4px solid ${col}`, boxShadow: '0 1px 4px rgba(15,23,42,0.04)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginBottom: 8, flexWrap: 'wrap' }}>
                  <span style={{ width: 9, height: 9, borderRadius: '50%', background: col, flexShrink: 0 }} />
                  <span style={{ fontSize: '0.78rem', fontWeight: 800, color: '#1e293b' }}>{sub ? sub.short : t.subjectId}</span>
                  {(t.hier || t.total != null) ? <span title={`이 과목 ${t.total}단원 중 ${t.idx + 1}번째`} style={{ fontSize: '0.58rem', fontWeight: 800, color: '#fff', background: '#4361ee', borderRadius: 5, padding: '2px 6px', whiteSpace: 'nowrap' }}>{t.hier || `${t.idx + 1}단원`}<span style={{ opacity: 0.7 }}> · {t.idx + 1}/{t.total}</span></span> : null}
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 3, fontSize: '0.58rem', fontWeight: 800, color: '#475569', background: '#f1f5f9', borderRadius: 5, padding: '2px 7px' }}>{am.icon} {am.label}{t.parallel ? ' · 병행' : ''}</span>
                  <span style={{ marginLeft: 'auto', fontSize: '0.58rem', fontWeight: 800, color: '#475569', background: '#f1f5f9', borderRadius: 5, padding: '2px 7px', whiteSpace: 'nowrap' }}>{t.stage === 2 ? '2차' : '1차'} · {t.round || 1}회독 · {steps.length}스텝</span>
                </div>
                {/* 오늘 배울 범위 — 계층 경로 + 레벨 + 분량 */}
                <div style={{ marginBottom: 9, padding: '9px 10px', borderRadius: 8, background: col + '12', border: `1px solid ${col}2e` }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 5 }}>
                    <span style={{ fontSize: '0.58rem', fontWeight: 800, color: col, background: '#fff', borderRadius: 5, padding: '2px 6px', whiteSpace: 'nowrap' }}>📖 오늘 범위</span>
                    {t.level ? <span title="이 단원의 계층 레벨" style={{ fontSize: '0.58rem', fontWeight: 800, color: '#fff', background: col, borderRadius: 5, padding: '2px 6px' }}>{t.level} 단위</span> : null}
                    {t.sub ? <span style={{ marginLeft: 'auto', fontSize: '0.58rem', fontWeight: 700, color: '#64748b', whiteSpace: 'nowrap' }}>분량 {t.sub}</span> : null}
                  </div>
                  <div style={{ fontSize: '0.78rem', fontWeight: 800, color: '#1e293b', lineHeight: 1.4 }}>
                    {t.div ? <span style={{ color: '#94a3b8', fontWeight: 700 }}>{t.div} › </span> : null}
                    {t.hier ? <span style={{ color: col }}>{t.hier} </span> : null}
                    {t.chap || t.unit}
                  </div>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
                  {steps.map((st, si) => (
                    <button key={si} onClick={() => go(st)} style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 8, textAlign: 'left', background: '#fafbfc', border: '1px solid #eef0f2', borderRadius: 8, padding: '8px 10px', cursor: 'pointer' }}>
                      <span style={{ width: 18, height: 18, flexShrink: 0, borderRadius: '50%', background: '#eef1fe', color: '#4361ee', fontSize: '0.6rem', fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{si + 1}</span>
                      <span style={{ flex: 1, minWidth: 0, fontSize: '0.72rem', color: '#334155', lineHeight: 1.4 }}><b style={{ color: '#1e293b' }}>{st.tab}</b>{' '}{st.do}</span>
                      <span style={{ color: '#cbd5e1', fontSize: '0.86rem', flexShrink: 0 }}>›</span>
                    </button>
                  ))}
                </div>
              </div>
            );
          })}
        </section>

        {/* 🩺 내 실력 현황 — 홈 탭으로 이동(사용자 요청). 아래 인라인본은 숨김 */}
        {false && subjectState && (
          <section style={{ background: '#fff', border: '1px solid #eceff3', borderRadius: 16, boxShadow: 'var(--shadow-md)', marginBottom: 14, padding: 15 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.86rem', fontWeight: 800, color: '#1e293b' }}>🩺 내 실력 현황</span>
              {(() => {
                const s1 = SUBJECTS.filter((s) => s.stage === 1).map((s) => subjectState[s.id]).filter(Boolean);
                if (!s1.length) return null;
                const avg = Math.round(s1.reduce((a, x) => a + x.coveredPct, 0) / s1.length);
                const accs = s1.map((x) => x.avgAccuracy).filter((x) => x != null);
                const avgAcc = accs.length ? Math.round(accs.reduce((a, b) => a + b, 0) / accs.length) : null;
                const aC = avgAcc == null ? '#94a3b8' : avgAcc < 40 ? '#ef4444' : avgAcc < 60 ? '#f59e0b' : avgAcc < 80 ? '#4361ee' : '#16a34a';
                return (
                  <span style={{ marginLeft: 'auto', display: 'inline-flex', gap: 5 }}>
                    <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#334155', background: '#eef1fe', borderRadius: 999, padding: '2px 10px' }}>진도 {avg}%</span>
                    {avgAcc != null && <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#fff', background: aC, borderRadius: 999, padding: '2px 10px' }}>정답률 {avgAcc}%</span>}
                  </span>
                );
              })()}
            </div>
            <div style={{ fontSize: '0.72rem', color: '#94a3b8', margin: '3px 0 11px' }}>문제를 풀면 자동 측정됩니다 · 진단으로 여러 단원을 빠르게 파악하세요</div>
            {(() => {
              const risk = SUBJECTS.filter((s) => s.stage === 1).filter((s) => { const st = subjectState[s.id]; return st && st.avgAccuracy != null && st.avgAccuracy < 40; });
              if (!risk.length) return null;
              return (
                <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 9, padding: '8px 11px', marginBottom: 11, fontSize: '0.72rem', color: '#334155', fontWeight: 700, lineHeight: 1.5 }}>
                  ⚠️ 과락 위험(정답률 40% 미만): {risk.map((s) => s.short).join(' · ')} — 동차는 한 과목만 과락해도 끝. 이 과목부터 끌어올리세요
                </div>
              );
            })()}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {SUBJECTS.map((s) => {
                const st = subjectState[s.id];
                const covered = st ? st.coveredPct : 0;
                const acc = st ? st.avgAccuracy : null;
                const accColor = acc == null ? '#cbd5e1' : acc < 40 ? '#ef4444' : acc < 60 ? '#f59e0b' : acc < 80 ? '#4361ee' : '#16a34a';
                const open = expSubj === s.id;
                const remaining = st ? st.total - st.mastered : 0;
                const perDay = st && plan.d1 > 0 ? remaining / plan.d1 : null;
                const pace = perDay == null ? null : perDay <= 0.4 ? { t: '여유', c: '#94a3b8' } : perDay <= 0.9 ? { t: '빠듯', c: '#94a3b8' } : { t: '촉박', c: '#334155' };
                const grp = (label, arr, type, color, showAcc) => (arr && arr.length ? (
                  <div style={{ marginTop: 7 }}>
                    <div style={{ fontSize: '0.64rem', fontWeight: 800, color, marginBottom: 4 }}>{label} {arr.length}</div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
                      {arr.slice(0, 6).map((x, i) => (
                        <button key={i} onClick={() => onOpenTask && onOpenTask({ type, subjectId: s.id, leafId: x.leaf.id })}
                          style={{ fontSize: '0.64rem', fontWeight: 600, color: '#475569', background: '#f8fafc', border: '1px solid #eef0f2', borderRadius: 7, padding: '4px 8px', cursor: 'pointer' }}>
                          {leafLabel(x.leaf)}{showAcc && x.quiz && x.quiz.answered ? ` ${Math.round((x.quiz.accuracy || 0) * 100)}%` : ''} ›
                        </button>
                      ))}
                    </div>
                  </div>
                ) : null);
                return (
                  <div key={s.id} style={{ border: open ? '1px solid #eef0f2' : '1px solid transparent', borderRadius: 10, padding: open ? '8px 10px' : 0, background: open ? '#fcfcfd' : 'transparent' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                      <button onClick={() => setExpSubj(open ? null : s.id)} style={{ flex: 1, minWidth: 0, display: 'flex', alignItems: 'center', gap: 10, background: 'none', border: 'none', cursor: 'pointer', padding: 0, textAlign: 'left' }}>
                        <span style={{ fontSize: '0.86rem', flexShrink: 0 }}>{s.icon}</span>
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
                            <span style={{ fontSize: '0.86rem', fontWeight: 800, color: '#1e293b' }}>{s.short}</span>
                            <span style={{ fontSize: '0.58rem', fontWeight: 800, color: s.stage === 2 ? '#7c3aed' : '#4361ee', background: s.stage === 2 ? '#f0ebff' : '#eef1fe', borderRadius: 5, padding: '1px 5px' }}>{s.stage === 2 ? '2차' : '1차'}</span>
                            <span style={{ marginLeft: 'auto', fontSize: '0.64rem', fontWeight: 800, color: '#fff', background: accColor, borderRadius: 999, padding: '2px 9px', minWidth: 42, textAlign: 'center' }}>
                              {acc == null ? '미측정' : `${acc}%`}
                            </span>
                            <span style={{ fontSize: '0.64rem', color: '#cbd5e1' }}>{open ? '▲' : '▼'}</span>
                          </div>
                          {/* 진도 바 */}
                          <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
                            <span style={{ width: 28, flexShrink: 0, fontSize: '0.58rem', fontWeight: 800, color: '#94a3b8' }}>진도</span>
                            <div style={{ flex: 1, height: 8, borderRadius: 4, background: '#f1f5f9', overflow: 'hidden' }}>
                              <div style={{ height: '100%', width: `${covered}%`, background: ACCENT, transition: 'width .3s' }} />
                            </div>
                            <span style={{ width: 66, flexShrink: 0, textAlign: 'right', fontSize: '0.58rem', fontWeight: 700, color: '#64748b' }}>{covered}%{st ? ` ${st.mastered}/${st.total}` : ''}</span>
                          </div>
                          {/* 정답률 바 (위험도 색) */}
                          <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginTop: 4 }}>
                            <span style={{ width: 28, flexShrink: 0, fontSize: '0.58rem', fontWeight: 800, color: '#94a3b8' }}>정답</span>
                            <div style={{ flex: 1, height: 8, borderRadius: 4, background: '#f1f5f9', overflow: 'hidden' }}>
                              <div style={{ height: '100%', width: `${acc == null ? 0 : acc}%`, background: accColor, transition: 'width .3s' }} />
                            </div>
                            <span style={{ width: 66, flexShrink: 0, textAlign: 'right', fontSize: '0.58rem', fontWeight: 800, color: accColor }}>{acc == null ? '—' : `${acc}%`}</span>
                          </div>
                        </div>
                      </button>
                      {s.stage === 1 && onDiagnostic && (
                        <button onClick={() => onDiagnostic(s.id)} style={{ flexShrink: 0, fontSize: '0.72rem', fontWeight: 800, color: '#334155', background: '#eef1fe', border: '1px solid #c6cefb', borderRadius: 8, padding: '5px 10px', cursor: 'pointer' }}>
                          진단
                        </button>
                      )}
                    </div>
                    {open && st && (
                      <div style={{ marginLeft: 26, marginTop: 6 }}>
                        {plan.d1 > 0 && s.stage === 1 && (
                          <div style={{ fontSize: '0.72rem', color: '#475569' }}>
                            🏁 완주까지 <b>{remaining}단원</b> · 1차 D-{plan.d1} → 하루 <b>{perDay != null ? perDay.toFixed(2) : '–'}단원</b> 필요
                            {pace && <span style={{ marginLeft: 6, fontWeight: 800, color: pace.c }}>{pace.t}</span>}
                          </div>
                        )}
                        {grp('🔁 복습 도래', st.due, 'drill', '#94a3b8')}
                        {grp('📉 약점 단원', st.weak, 'solve', '#334155', true)}
                        {grp('📖 다음 볼 단원', st.next, 'study', '#4361ee')}
                        {!st.due.length && !st.weak.length && !st.next.length && (
                          <div style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: 6 }}>아직 데이터가 적어요 · 위 진단으로 측정해보세요</div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
            {/* ✍️ 2차 답안 연습 현황 — quiz-essay-progress(자기채점) 연결 */}
            {(() => {
              let ep = {}; try { ep = JSON.parse(localStorage.getItem('quiz-essay-progress') || '{}') || {}; } catch { /* */ }
              const entries = Object.values(ep).filter((e) => e && e.attempts && e.attempts.length);
              const scores = entries.map((e) => e.attempts[e.attempts.length - 1].selfScore).filter((x) => typeof x === 'number');
              const avg = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null;
              return (
                <div style={{ marginTop: 11, paddingTop: 11, borderTop: '1px solid #f1f5f9', display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontSize: '0.86rem' }}>✍️</span>
                  <span style={{ fontWeight: 800, fontSize: '0.78rem', color: entries.length ? '#475569' : '#cbd5e1' }}>2차 답안 연습</span>
                  <span style={{ fontSize: '0.64rem', color: '#94a3b8' }}>{entries.length ? `${entries.length}개 작성` : '2차 논술에서 답안 쓰면 집계'}</span>
                  {entries.length > 0 && (
                    <span style={{ marginLeft: 'auto', fontSize: '0.72rem', fontWeight: 800, color: avg == null ? '#cbd5e1' : avg < 40 ? '#334155' : '#475569' }}>
                      자기채점 {avg == null ? '—' : `${avg}점`}
                    </span>
                  )}
                </div>
              );
            })()}
          </section>
        )}

        {/* 🎯 동차 합격 플랜 — 위 월별 간트 + 달력과 중복이라 숨김(사용자 요청). 공부시간·직장병행 설정(planOpts)은 값이 localStorage에 남아 달력 계획에 계속 반영됨 */}
        {false && (
        <section style={{ background: '#fff', border: '1px solid #eceff3', borderRadius: 16, boxShadow: 'var(--shadow-md)', marginBottom: 14, padding: 15 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap', marginBottom: 4 }}>
            <span style={{ fontSize: '0.86rem', fontWeight: 800, color: '#1e293b' }}>🎯 동차 합격 플랜</span>
            <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#334155', background: '#eef1fe', borderRadius: 999, padding: '2px 9px' }}>
              1차 D-{plan.d1 >= 0 ? plan.d1 : '–'} · 2차 D-{plan.d2 >= 0 ? plan.d2 : '–'}
            </span>
            <button onClick={() => setShowPlanOpts((v) => !v)} style={{ marginLeft: 'auto', fontSize: '0.72rem', fontWeight: 800, color: '#fff', cursor: 'pointer', background: ACCENT, border: 'none', borderRadius: 999, padding: '6px 12px' }}>
              🤖 내 상황 맞춤 {showPlanOpts ? '▲' : '▼'}
            </button>
          </div>
          <div style={{ fontSize: '0.72rem', color: '#94a3b8', marginBottom: 10 }}>
            동차(1·2차 같은 해 동시 합격) 목표 · 2차를 미리 벌어두는 전략
            {(plan.approx1 || plan.approx2) && <span style={{ color: '#475569' }}> · 시험일을 등록하면 정확해집니다</span>}
          </div>

          {/* 내 상황 맞춤 옵션 — 바꾸면 즉시 재생성 */}
          {showPlanOpts && (
            <div style={{ background: '#f8fafc', border: '1px solid #eef0f2', borderRadius: 12, padding: 12, marginBottom: 12 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10, flexWrap: 'wrap' }}>
                <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#475569' }}>직장 병행</span>
                <div style={{ display: 'flex', gap: 6 }}>
                  {[['전업 수험', false], ['직장 병행', true]].map(([lbl, val]) => (
                    <button key={lbl} onClick={() => updatePlanOpts({ working: val })} style={{
                      fontSize: '0.72rem', fontWeight: 700, borderRadius: 999, padding: '5px 11px', cursor: 'pointer',
                      border: planOpts.working === val ? '1.5px solid #4361ee' : '1px solid #e5e7eb',
                      background: planOpts.working === val ? '#eef1fe' : '#fff', color: planOpts.working === val ? '#334155' : '#94a3b8',
                    }}>{lbl}</button>
                  ))}
                </div>
              </div>
              {[['평일 하루', 'hoursWeekday', [1, 2, 3, 4, 5, 6, 8, 10]], ['주말 하루', 'hoursWeekend', [2, 4, 6, 8, 10, 12]]].map(([lbl, key, opts]) => (
                <div key={key} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                  <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#475569', width: 60 }}>{lbl}</span>
                  <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap' }}>
                    {opts.map((h) => (
                      <button key={h} onClick={() => updatePlanOpts({ [key]: h })} style={{
                        fontSize: '0.72rem', fontWeight: 700, borderRadius: 8, padding: '4px 9px', cursor: 'pointer',
                        border: planOpts[key] === h ? '1.5px solid #4361ee' : '1px solid #e5e7eb',
                        background: planOpts[key] === h ? '#eef1fe' : '#fff', color: planOpts[key] === h ? '#334155' : '#94a3b8',
                      }}>{h}h</button>
                    ))}
                  </div>
                </div>
              ))}
              {onAskAI && (
                <button onClick={() => onAskAI(buildDongchaPrompt(plan, planOpts))} style={{
                  marginTop: 4, width: '100%', fontSize: '0.72rem', fontWeight: 800, color: '#334155', cursor: 'pointer',
                  background: '#eef1fe', border: '1px solid #c6cefb', borderRadius: 9, padding: '8px',
                }}>🤖 AI에게 정밀 코칭 받기 (선택)</button>
              )}
            </div>
          )}

          {/* 전체 계획(단계) */}
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#94a3b8', margin: '2px 0 7px' }}>전체 계획</div>
          {plan.phases.map((p) => (
            <div key={p.key} style={{ borderLeft: `3px solid ${ACCENT}`, background: p.active ? ACCENT + '0e' : '#fafafa', borderRadius: '0 10px 10px 0', padding: '9px 11px', marginBottom: 6 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
                <span style={{ fontWeight: 800, fontSize: '0.78rem', color: '#1e293b' }}>{p.title}</span>
                {p.active && <span style={{ fontSize: '0.58rem', fontWeight: 800, color: '#fff', background: ACCENT, borderRadius: 999, padding: '1px 7px' }}>지금</span>}
                <span style={{ marginLeft: 'auto', fontSize: '0.64rem', color: '#94a3b8' }}>{p.label} · {p.days}일</span>
              </div>
              <div style={{ fontSize: '0.72rem', color: '#475569', marginTop: 3, lineHeight: 1.5 }}>{p.goal}</div>
              <div style={{ display: 'flex', gap: 5, marginTop: 6, flexWrap: 'wrap' }}>
                {p.mix.map((mx, j) => <span key={j} style={{ fontSize: '0.64rem', color: '#475569', background: '#f1f5f9', borderRadius: 6, padding: '2px 7px' }}>{mx.k} {mx.pct}%</span>)}
              </div>
            </div>
          ))}

          {/* 월별 계획 */}
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#94a3b8', margin: '11px 0 6px' }}>월별 계획</div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {plan.months.map((m) => (
              <div key={m.ym} style={{ display: 'flex', gap: 9, alignItems: 'center', padding: '6px 2px', borderTop: '1px solid #f4f4f5' }}>
                <span style={{ width: 46, flexShrink: 0, fontWeight: 800, fontSize: '0.72rem', color: m.isCurrent ? '#334155' : '#475569' }}>{m.label}{m.isExam1 ? ' 🎯' : ''}{m.isExam2 ? ' 🏁' : ''}</span>
                <span style={{ width: 8, height: 8, borderRadius: '50%', background: m.color, flexShrink: 0 }} />
                <span style={{ flex: 1, fontSize: '0.72rem', color: '#475569', fontWeight: m.isCurrent ? 700 : 500, lineHeight: 1.4 }}>{m.focus}</span>
              </div>
            ))}
          </div>
        </section>
        )}

        {false && (<>
        {/* 📒 단권화 노트(서브)·단계별 로드맵 — 사용자 요청으로 숨김 */}
        <section style={{ background: '#fff', border: '1px solid #eceff3', borderRadius: 16, boxShadow: 'var(--shadow-md)', marginBottom: 14, padding: 15 }}>
          <button onClick={() => setSnOpen((v) => !v)} style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 8, background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}>
            <span style={{ fontSize: '0.86rem', fontWeight: 800, color: '#1e293b' }}>📒 단권화 노트</span>
            <span style={{ fontSize: '0.64rem', color: '#94a3b8' }}>과목별 단일 정리 — 합격수기 1위 도구</span>
            <span style={{ marginLeft: 'auto', color: '#cbd5e1' }}>{snOpen ? '▲' : '▼'}</span>
          </button>
          {snOpen && (
            <div style={{ marginTop: 11 }}>
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 9 }}>
                {SUBJECTS.map((s) => {
                  const on = snSubj === s.id;
                  return (
                    <button key={s.id} onClick={() => setSnSubj(s.id)} style={{ fontSize: '0.72rem', fontWeight: 800, borderRadius: 999, padding: '5px 9px', cursor: 'pointer', border: on ? `1.5px solid ${ACCENT}` : '1px solid #e5e7eb', background: on ? ACCENT + '12' : '#fff', color: on ? ACCENT : '#94a3b8' }}>{s.icon} {s.short}</button>
                  );
                })}
              </div>
              <textarea value={snText}
                onChange={(e) => { const v = e.target.value; setSnText(v); try { localStorage.setItem('subnote-v1-' + snSubj, v); } catch { /* */ } }}
                placeholder={`${SMAP[snSubj] ? SMAP[snSubj].short : ''} 핵심을 한 곳에 — 조문·판례·산식·자주 틀리는 포인트를 계속 덧붙이세요`}
                style={{ width: '100%', minHeight: 220, boxSizing: 'border-box', border: '1px solid #e5e7eb', borderRadius: 10, padding: '11px 12px', fontSize: '0.78rem', lineHeight: 1.6, color: '#1e293b', resize: 'vertical', fontFamily: 'inherit' }} />
              <div style={{ fontSize: '0.64rem', color: '#94a3b8', marginTop: 6 }}>자동 저장됨 · {snText.length}자 · 시험 직전 이 노트만 회독</div>
            </div>
          )}
        </section>

        {/* ── 아래는 과목별 상세(1차/2차 전환) ── */}

        {/* 로드맵 헤더 + 실측 자동반영 토글 */}
        <div style={{ display: 'flex', alignItems: 'center', margin: '4px 4px 8px' }}>
          <span style={{ fontSize: '0.78rem', fontWeight: 800, color: '#475569' }}>🗺 단계별 로드맵</span>
          {stage === 1 && metrics && (
            <button onClick={flipAuto} title="정답률·커버리지·모의·복습 실측으로 자동 체크" style={{
              marginLeft: 'auto', display: 'inline-flex', alignItems: 'center', gap: 6, cursor: 'pointer',
              border: `1px solid ${autoOn ? '#aab6f7' : '#e5e7eb'}`, background: autoOn ? '#eef1fe' : '#fff',
              borderRadius: 999, padding: '4px 10px', fontSize: '0.72rem', fontWeight: 800, color: autoOn ? '#334155' : '#94a3b8',
            }}>
              <span style={{ width: 26, height: 15, borderRadius: 999, background: autoOn ? '#334155' : '#cbd5e1', position: 'relative', transition: 'background .15s' }}>
                <span style={{ position: 'absolute', top: 2, left: autoOn ? 13 : 2, width: 11, height: 11, borderRadius: '50%', background: '#fff', transition: 'left .15s' }} />
              </span>
              실측 자동반영
            </button>
          )}
        </div>

        {/* 목표 일자 안내 + 일괄 채우기 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, margin: '0 4px 10px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.72rem', color: '#94a3b8', fontWeight: 700 }}>🎯 각 단계에 목표 일자를 넣으면 일정·플래너 배치가 그 날짜로 작동해요</span>
          {T != null && T > 0 && (
            <button onClick={autofillDates} style={{ fontSize: '0.64rem', fontWeight: 800, color: '#334155', background: '#eef1fe', border: '1px solid #c6cefb', borderRadius: 999, padding: '4px 10px', cursor: 'pointer' }}>
              시험일 기준 자동 채우기
            </button>
          )}
          {hasDates && (
            <button onClick={clearDates} style={{ fontSize: '0.64rem', fontWeight: 700, color: '#94a3b8', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 999, padding: '4px 10px', cursor: 'pointer' }}>
              일정 초기화
            </button>
          )}
        </div>

        {/* 단계 카드 */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 18 }}>
          {PHASES.map((p, pi) => {
            const st = phaseStat(p); const w = windows[p.id]; const isCur = p.id === currentPhaseId; const opened = isOpen(p.id);
            const pace = w && st.pct < 100 ? (w.endOff < 0 ? 'late' : w.startOff > 0 ? 'future' : 'now') : null;
            const paceMeta = { late: { t: '지연', c: '#334155', b: '#fef2f2' }, now: { t: '진행 중', c: '#ea580c', b: '#fff7ed' }, future: { t: '예정', c: '#94a3b8', b: '#f1f5f9' } }[pace];
            return (
              <section key={p.id} style={{ background: '#fff', borderRadius: 14, overflow: 'hidden', border: isCur ? `2px solid ${ACCENT}` : '1px solid #eef0f2', boxShadow: 'var(--shadow-md)' }}>
                <button onClick={() => toggleOpen(p.id)} style={{ width: '100%', textAlign: 'left', cursor: 'pointer', border: 'none', background: 'none', padding: '13px 14px', display: 'flex', alignItems: 'center', gap: 11 }}>
                  <span style={{ flexShrink: 0, width: 34, height: 34, borderRadius: 9, background: ACCENT + '18', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.1rem' }}>{p.icon}</span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
                      <span style={{ fontWeight: 800, fontSize: '0.86rem', color: '#1e293b' }}>{pi === 0 ? '' : `${pi}단계 · `}{p.title}</span>
                      {isCur && <span style={{ fontSize: '0.64rem', fontWeight: 800, color: '#fff', background: ACCENT, borderRadius: 999, padding: '2px 8px' }}>지금 여기</span>}
                    </div>
                    <div style={{ fontSize: '0.72rem', color: '#475569', marginTop: 2 }}>{p.goal}</div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 6 }}>
                      {w ? (
                        <span style={{ fontSize: '0.64rem', fontWeight: 700, color: ACCENT, background: ACCENT + '12', borderRadius: 6, padding: '2px 7px' }}>📅 {w.label} · 약 {w.days}일</span>
                      ) : p.w > 0 ? (
                        <span style={{ fontSize: '0.64rem', color: '#94a3b8' }}>권장 비중 {Math.round(p.w * 100)}%</span>
                      ) : (
                        <span style={{ fontSize: '0.64rem', color: '#94a3b8' }}>지금 바로</span>
                      )}
                      {paceMeta && <span style={{ fontSize: '0.64rem', fontWeight: 800, color: paceMeta.c, background: paceMeta.b, borderRadius: 5, padding: '2px 6px' }}>{paceMeta.t}</span>}
                      <span style={{ fontSize: '0.64rem', fontWeight: 800, color: st.pct === 100 ? '#16a34a' : '#94a3b8', marginLeft: 'auto' }}>{st.done}/{st.total}</span>
                      <span style={{ fontSize: '0.86rem', color: '#cbd5e1' }}>{opened ? '▲' : '▼'}</span>
                    </div>
                    <div style={{ height: 4, borderRadius: 3, background: '#f1f5f9', marginTop: 6, overflow: 'hidden' }}>
                      <div style={{ height: '100%', width: `${st.pct}%`, background: st.pct === 100 ? '#16a34a' : ACCENT, transition: 'width .2s' }} />
                    </div>
                  </div>
                </button>

                {opened && (
                  <div style={{ padding: '0 14px 14px' }}>
                    <div style={{ fontSize: '0.72rem', color: '#475569', background: '#faf9f7', border: '1px solid #f0eeeb', borderRadius: 9, padding: '9px 11px', marginBottom: 10, lineHeight: 1.6 }}>💡 {p.note}</div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                      {p.items.map((it) => {
                        const sm = it.subject ? SMAP[it.subject] : null;
                        const bd = TYPE_BADGE[it.type] || TYPE_BADGE.custom;
                        const done = isDone(it);
                        const au = stage === 1 && metrics ? evalAuto(it, metrics) : null;
                        const autoHit = useAuto && au && au.done && prog[it.id] === undefined; // 실측으로 자동 체크된 항목
                        const openable = OPENABLE.has(it.type) && onOpenTask;
                        return (
                          <div key={it.id} style={{ display: 'flex', alignItems: 'flex-start', gap: 9, background: done ? '#f0fdf4' : '#fff', border: `1px solid ${done ? '#bbf7d0' : '#eef0f2'}`, borderRadius: 10, padding: '9px 11px' }}>
                            <button onClick={() => toggle(it)} aria-label="완료 토글" style={{ width: 21, height: 21, borderRadius: '50%', flexShrink: 0, cursor: 'pointer', marginTop: 1, border: `2px solid ${done ? '#16a34a' : '#cbd5e1'}`, background: done ? '#16a34a' : '#fff', color: '#fff', fontSize: '0.64rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{done ? '✓' : ''}</button>
                            <div style={{ flex: 1, minWidth: 0 }}>
                              <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
                                <span style={{ fontSize: '0.58rem', fontWeight: 800, color: bd.c, background: bd.b, borderRadius: 6, padding: '2px 6px' }}>{bd.t}</span>
                                {sm && <span style={{ fontSize: '0.64rem', fontWeight: 800, color: ACCENT }}>{sm.icon} {sm.short}</span>}
                                {autoHit && <span style={{ fontSize: '0.58rem', fontWeight: 800, color: '#475569', background: '#dcfce7', borderRadius: 5, padding: '1px 5px' }}>실측 달성</span>}
                              </div>
                              <button onClick={() => openable && onOpenTask(it)} disabled={!openable} style={{ display: 'block', textAlign: 'left', background: 'none', border: 'none', padding: '3px 0 0', width: '100%', cursor: openable ? 'pointer' : 'default', fontSize: '0.78rem', fontWeight: 600, color: done ? '#94a3b8' : '#1f2937', textDecoration: done ? 'line-through' : 'none' }}>
                                {it.label}{openable && <span style={{ color: bd.c, fontWeight: 800 }}> ›</span>}
                              </button>
                              {it.round && (() => {
                                const cnt = rounds[it.id] || 0;
                                const stepBtn = { width: 22, height: 22, borderRadius: 6, border: '1px solid #e5e7eb', background: '#fff', color: '#475569', fontSize: '0.86rem', fontWeight: 800, cursor: 'pointer', lineHeight: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 };
                                return (
                                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 7, flexWrap: 'wrap' }}>
                                    <span style={{ fontSize: '0.64rem', fontWeight: 800, color: '#475569' }}>회독</span>
                                    <button onClick={() => bumpRound(it, -1)} disabled={cnt <= 0} style={{ ...stepBtn, opacity: cnt <= 0 ? 0.4 : 1 }}>−</button>
                                    <span style={{ display: 'flex', gap: 3 }}>
                                      {Array.from({ length: it.round }).map((_, k) => (
                                        <span key={k} style={{ width: 9, height: 9, borderRadius: '50%', background: k < cnt ? '#16a34a' : '#e5e7eb' }} />
                                      ))}
                                    </span>
                                    <button onClick={() => bumpRound(it, 1)} disabled={cnt >= it.round} style={{ ...stepBtn, opacity: cnt >= it.round ? 0.4 : 1 }}>＋</button>
                                    <span style={{ fontSize: '0.72rem', fontWeight: 800, color: cnt >= it.round ? '#16a34a' : '#a16207' }}>{cnt}/{it.round}회독{cnt >= it.round ? ' ✓' : ''}</span>
                                  </div>
                                );
                              })()}
                              {it.tip && <div style={{ fontSize: '0.72rem', color: '#475569', marginTop: 3, lineHeight: 1.5 }}>↳ {it.tip}</div>}
                              {au && <div style={{ fontSize: '0.64rem', color: au.done ? '#16a34a' : '#94a3b8', marginTop: 3, fontWeight: 700 }}>📊 {au.label}</div>}
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    {p.w > 0 && (
                      <div style={{ marginTop: 10 }}>
                        {/* 🎯 이 단계 목표 일자 */}
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap', background: '#f8fafc', border: '1px solid #eef0f2', borderRadius: 9, padding: '8px 10px', marginBottom: 8 }}>
                          <span style={{ fontSize: '0.72rem', fontWeight: 800, color: '#475569' }}>🎯 목표 일자</span>
                          <input type="date" value={pdates[p.id] || ''} onChange={(e) => setDate(p.id, e.target.value)}
                            style={{ fontSize: '0.72rem', padding: '5px 8px', border: '1px solid #e5e7eb', borderRadius: 8, color: '#475569', background: '#fff' }} />
                          {w ? (
                            <span style={{ fontSize: '0.64rem', fontWeight: 800, color: w.endOff < 0 ? '#334155' : '#16a34a' }}>
                              {w.endOff < 0 ? `${-w.endOff}일 지남` : `D-${w.endOff}`} · 약 {w.days}일
                            </span>
                          ) : (
                            <span style={{ fontSize: '0.64rem', color: '#94a3b8' }}>날짜 미설정</span>
                          )}
                          {pdates[p.id] && <button onClick={() => setDate(p.id, '')} style={{ marginLeft: 'auto', fontSize: '0.64rem', color: '#94a3b8', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 700 }}>지우기</button>}
                        </div>
                        {/* 📅 플래너 배치 */}
                        {w ? (
                          <button onClick={() => placeInPlanner(p)} disabled={placed[p.id]} style={{ width: '100%', padding: '9px', borderRadius: 9, cursor: placed[p.id] ? 'default' : 'pointer', border: `1px solid ${placed[p.id] ? '#bbf7d0' : ACCENT + '55'}`, background: placed[p.id] ? '#f0fdf4' : ACCENT + '10', color: placed[p.id] ? '#16a34a' : ACCENT, fontWeight: 800, fontSize: '0.78rem' }}>
                            {placed[p.id] ? '✓ 플래너에 배치됨' : '📅 이 단계를 플래너에 배치'}
                          </button>
                        ) : (
                          <div style={{ fontSize: '0.72rem', color: '#94a3b8', textAlign: 'center' }}>목표 일자를 넣거나 시험일을 등록하면 플래너에 자동 배치할 수 있어요</div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </section>
            );
          })}
        </div>
        </>)}

        </div>{/* /curr-right */}
        </div>{/* /curr-2col */}
      </main>
    </div>
  );
}
