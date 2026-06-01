// leaf 단위 통합 진척 모델 — 둘러보기·AI학습·현황·복습 4탭 공통 데이터.
//
// leaf 정의: ai_taxonomy_index.json 의 leaves[i] (taxonomy 경로)
// 두 진척 소스를 하나의 단위로 묶는다:
//   quiz : quiz-progress-v1 (문제 id 기반) — 둘러보기·복습 입력
//   ai   : ailearn-mastery   (leaf id 기반) — AI 학습 입력
//
// 4탭이 모두 같은 leaf id로 묶이므로 한 사용자 활동이 모든 탭에 반영된다.

// taxonomy mapped path (sub_subject, chapter, section, item) → leaf path 배열
// "민법" 과목은 sub_subject 포함, 부동산·관계법규는 chapter부터 시작.
export function quizQuestionToLeafPath(q) {
  if (!q || !q.taxSubjectName) return null;
  return [q.taxSubSubjectName, q.taxChapterName, q.taxSectionName, q.taxItemName].filter(Boolean);
}

// quiz subject name → AI subject id
export const QUIZ_SUBJECT_TO_AI = {
  '민법': 'civil',
  '경제학원론': 'economics',
  '부동산학원론': 'realestate',
  '감정평가관계법규': 'law',
  '회계학': 'accounting',
};
export const AI_SUBJECT_TO_QUIZ = Object.fromEntries(
  Object.entries(QUIZ_SUBJECT_TO_AI).map(([k, v]) => [v, k])
);

// leaf path → leaves에서 매칭되는 leaf 찾기 (정확 일치 → 후미부터 짧게)
export function findLeafByPath(leaves, path) {
  if (!Array.isArray(leaves) || !leaves.length || !Array.isArray(path) || !path.length) return null;
  const key = path.join('|');
  // 정확 일치
  for (const l of leaves) {
    if ((l.path || []).join('|') === key) return l;
  }
  // path 길이 줄여가며
  for (let n = path.length - 1; n >= 1; n--) {
    const k = path.slice(0, n).join('|');
    for (const l of leaves) {
      if ((l.path || []).join('|') === k) return l;
    }
  }
  return null;
}

// quiz 문제 list에서 특정 leaf에 속하는 문제만 필터.
// q.taxSubSubjectName/chapter/section/item을 leaf.path와 prefix 매칭.
export function questionsInLeaf(classifiedList, leaf) {
  if (!classifiedList || !leaf) return [];
  const subjName = AI_SUBJECT_TO_QUIZ[(leaf.id || '').split('__')[0]];
  if (!subjName) return [];
  const leafPath = leaf.path || [];
  return classifiedList.filter((q) => {
    if (q.taxSubjectName !== subjName) return false;
    const qPath = quizQuestionToLeafPath(q);
    // leaf가 더 짧으면 prefix matching, 길거나 같으면 정확/유사 일치
    if (qPath.length < leafPath.length) return false;
    for (let i = 0; i < leafPath.length; i++) {
      if (qPath[i] !== leafPath[i]) return false;
    }
    return true;
  });
}

// leaf의 quiz 통계 (정답률·answered·due·mastered)
export function leafQuizStats(leaf, classifiedList, progress, qidFn) {
  const qs = questionsInLeaf(classifiedList, leaf);
  let answered = 0, correct = 0, wrong = 0, due = 0, mastered = 0;
  const total = qs.length;
  const now = Date.now();
  for (const q of qs) {
    const p = progress[qidFn(q)];
    if (!p) continue;
    answered += 1;
    if (p.correct === true) correct += 1;
    if (p.correct === false) wrong += 1;
    if (p.srs?.due && p.srs.due <= now) due += 1;
    if (p.srs?.graduated) mastered += 1;
  }
  return {
    total,
    answered,
    correct,
    wrong,
    due,
    mastered,
    accuracy: answered > 0 ? correct / answered : 0,
    coverage: total > 0 ? answered / total : 0,
  };
}

// leaf의 AI 학습 진척 (ailearn-mastery에서 추출)
export function leafAiStats(leaf, masteryMap) {
  const m = masteryMap[leaf?.id] || {};
  return {
    coverage: m.coverage || 0,
    accuracy: m.accuracy || 0,
    attempted: m.attempted || 0,
    correct: m.correct || 0,
    status: m.status || 'not_started',
    last_studied: m.last_studied || null,
    next_review: m.next_review || null,
    srs_box: m.srs_box || 0,
    is_due: m.next_review ? new Date(m.next_review).getTime() <= Date.now() : false,
  };
}

// 통합 score: quiz accuracy 50% + ai coverage 50% (가중치는 추후 조정 가능)
export function leafCompositeScore(quizStats, aiStats) {
  const q = quizStats.coverage > 0 ? quizStats.accuracy : 0;
  const a = aiStats.coverage || 0;
  return Math.max(0, Math.min(1, q * 0.5 + a * 0.5));
}

// leaf 통합 상태
export function getLeafState(leaf, ctx) {
  if (!leaf) return null;
  const quiz = leafQuizStats(leaf, ctx.classifiedList || [], ctx.progress || {}, ctx.qidFn);
  const ai = leafAiStats(leaf, ctx.mastery || {});
  return {
    leaf,
    quiz,
    ai,
    score: leafCompositeScore(quiz, ai),
    is_active: quiz.answered > 0 || ai.coverage > 0,
    is_mastered: (quiz.coverage >= 0.9 && quiz.accuracy >= 0.8) || ai.status === 'mastered',
    needs_review: quiz.due > 0 || ai.is_due,
  };
}
