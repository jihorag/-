// 과목별 학습 진단 — 사용자가 푼 기출을 '유형·과목특성·단원·난이도·개념'별로 버킷해
// 어디가 약한지 드러낸다. 데이터: q.tags.question_type(유형), q.taxChapterName(단원),
// q.difficulty(난이도), q.tags.concept(개념). 경제 그래프만 텍스트 휴리스틱(플래그 없음).
// 정오: progress[qid] = { correct:true|false|null }. 1차 5과목만(기출 태깅 기준).

import { SUBJECTS } from './aiLearningStore';
import { wilsonLower } from './proficiencyEngine';
import { getMistakeSummary } from './studyMeta';

const S1 = SUBJECTS.filter((s) => s.stage === 1);
const CALC = '계산문제';

// 과목 특성 차원(그래프/계산/판례/조문/개념) — 과목마다 다르게.
function dimensionOf(sid, q) {
  const type = q.tags?.question_type || '';
  const txt = `${q.question || ''} ${q.explanation || ''}`;
  const isCalc = type === CALC;
  if (sid === 'economics') {
    if (isCalc) return '계산';
    if (/곡선|그래프|그림|도표|좌표|이동시|우측 이동|좌측 이동/.test(txt)) return '그래프·도해';
    return '개념·이론';
  }
  if (sid === 'accounting') return isCalc ? '계산·분개' : '개념·이론';
  if (sid === 'civil') return type === '판례해석' ? '판례' : '조문·개념';
  if (sid === 'law') {
    if (type === '조문암기') return '조문암기';
    if (type === '판례해석') return '판례';
    if (isCalc) return '계산';
    return '개념';
  }
  if (sid === 'realestate') return isCalc ? '계산' : '개념·이론';
  return isCalc ? '계산' : '개념';
}

const typeLabel = (t) => (!t ? '기타' : t.replace(' 고르기', '').replace('옳지 않은 것', '옳지않은것'));

const newBucket = (key) => ({ key, total: 0, answered: 0, correct: 0, wrongIds: [], ids: [] });
function tally(map, key, answered, correct, id) {
  let b = map.get(key); if (!b) { b = newBucket(key); map.set(key, b); }
  b.total++; b.ids.push(id);
  if (answered) { b.answered++; if (correct) b.correct++; else b.wrongIds.push(id); }
}
function finalize(map, { includeUntouched = false, minAnswered = 1 } = {}) {
  return [...map.values()]
    .filter((b) => (includeUntouched ? b.total > 0 : b.answered >= minAnswered))
    .map((b) => ({ ...b, untouched: b.answered === 0, acc: b.answered ? b.correct / b.answered : null, wilson: b.answered ? wilsonLower(b.correct, b.answered) : 1 }));
}
// 약한 순 — 푼 것(정답률 하한 낮은 순) 먼저, 미학습(가장 낮은 상태)은 큰 묶음부터 뒤에.
const byWeak = (a, b) => {
  const au = a.answered === 0, bu = b.answered === 0;
  if (au !== bu) return au ? 1 : -1;
  if (au) return b.total - a.total;
  return a.wilson - b.wilson;
};

/**
 * @param {{classifiedList:array, progress:object, qidFn:function}} ctx
 * @returns {{ [sid]: subjectDiag }}
 */
export function buildSubjectDiag(ctx) {
  const { classifiedList = [], progress = {}, qidFn = (q) => q.id } = ctx || {};
  const taxToId = {}; S1.forEach((s) => { taxToId[s.tax_key] = s.id; });

  const acc = {};
  S1.forEach((s) => { acc[s.id] = {
    total: 0, answered: 0, correct: 0,
    byType: new Map(), byDim: new Map(), byArea: new Map(), byDiff: new Map(), byConcept: new Map(), byDiv: new Map(),
  }; });

  for (const q of classifiedList) {
    if (q.exam !== '감정평가사') continue; // 감정평가사 기출만 (타 시험 문항 제외)
    const sid = taxToId[q.taxSubjectName];
    if (!sid) continue;
    const S = acc[sid];
    const id = qidFn(q);
    const p = progress[id];
    const answered = !!p && p.correct != null;
    const correct = answered && p.correct === true;
    S.total++;
    if (answered) { S.answered++; if (correct) S.correct++; }
    tally(S.byType, typeLabel(q.tags?.question_type), answered, correct, id);
    tally(S.byDim, dimensionOf(sid, q), answered, correct, id);
    if (q.taxChapterName) tally(S.byArea, q.taxChapterName, answered, correct, id);
    const div = q.taxSubSubjectName || q.indexing_v4?.mapped_taxonomy?.sub_subject;
    if (div) tally(S.byDiv, div, answered, correct, id);
    if (q.difficulty) tally(S.byDiff, String(q.difficulty), answered, correct, id);
    const concept = q.tags?.concept; if (concept) tally(S.byConcept, concept, answered, correct, id);
  }

  const res = {};
  S1.forEach((s) => {
    const S = acc[s.id];
    let mistakes = {}; try { mistakes = getMistakeSummary(s.title) || {}; } catch { mistakes = {}; }
    res[s.id] = {
      id: s.id, short: s.short, title: s.title, color: s.color, icon: s.icon,
      total: S.total, answered: S.answered, correct: S.correct,
      acc: S.answered ? S.correct / S.answered : null,
      byType: finalize(S.byType, { includeUntouched: true }).sort(byWeak),
      byDim: finalize(S.byDim, { includeUntouched: true }).sort(byWeak),
      byArea: finalize(S.byArea, { includeUntouched: true }).sort(byWeak),
      byDiv: finalize(S.byDiv, { includeUntouched: true }).sort(byWeak),
      byDiff: finalize(S.byDiff, { includeUntouched: true }).sort((a, b) => Number(a.key) - Number(b.key)),
      byConcept: finalize(S.byConcept, { minAnswered: 3 }).sort(byWeak).slice(0, 8),
      mistakes,
    };
  });
  return res;
}

// 오답 원인 코드 → 라벨(진단 리포트 표시용)
export const MISTAKE_LABEL = {
  concept: '개념 부족', misread: '문제 오독', forgot: '암기 인출 실패',
  formula: '공식 혼동', sign: '부호·방향 실수', calc: '계산 실수',
};
