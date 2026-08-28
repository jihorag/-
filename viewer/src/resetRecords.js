// 🗑 학습 기록 초기화.
// 진도·정답률·커버리지·SRS·모의·복습·마일스톤·AI 채팅 기록·오늘/월간 AI계획을 한 번에 비운다.
// 보존: API 키·모델·프록시, 시험일, 과목 목표점수·전략·회독목표·플래너, 사용자 작성 노트, 커스텀 드릴 주제.

const REMOVE_EXACT = [
  // 기출·문제풀이 진행/통계
  'quiz-progress-v1', 'quiz-essay-progress', 'quiz-essay-cards-srs-v1', 'quiz-mem-v1',
  'quiz-mock-history', 'quiz-sessions-v1', 'quiz-studytime-v1', 'quiz-journey-v3',
  'quiz-chatcards-v1', 'wrong-rounds-v1',
  // AI 학습 숙련도·SRS·사용량·현재상태·확인대기
  'ailearn-mastery', 'ailearn-items-v1', 'ailearn-usage', 'ailearn-current',
  'ailearn-msg-ratings', 'ailearn-pending-check',
  // 드릴 진행
  'drill-progress-v1',
  // 커리큘럼 진행/실측/회독카운터/오늘·월간 계획
  'curriculum-progress-v1', 'curriculum-auto-v1', 'curriculum-rounds-v1',
  'curriculum-today-v1', 'curriculum-summary-v1', 'curriculum-aiplan-v1',
];
// 프리픽스로 지우는 것: AI 학습 단원별 채팅방(ailearn-room:{leafId})
const REMOVE_PREFIX = ['ailearn-room:'];

export function clearStudyRecords() {
  try {
    REMOVE_EXACT.forEach((k) => localStorage.removeItem(k));
    Object.keys(localStorage).forEach((k) => {
      if (REMOVE_PREFIX.some((p) => k.startsWith(p))) localStorage.removeItem(k);
    });
  } catch { /* noop */ }
}

// 사용자가 명시적으로 요청한 1회 초기화 — 센티넬로 딱 한 번만 실행(이후 리로드엔 skip).
const ONESHOT = 'records-reset-oneshot-20260731';
try {
  if (typeof localStorage !== 'undefined' && !localStorage.getItem(ONESHOT)) {
    clearStudyRecords();
    localStorage.setItem(ONESHOT, String(Date.now()));
  }
} catch { /* noop */ }
