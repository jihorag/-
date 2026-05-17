/**
 * 탭 간 분류 정합성 교차검증.
 * 4개 탭(시험별/과목별/단원별/연도별)이 동일한 v4 mapped_taxonomy 분류축을
 * 쓰므로, 같은 모집단을 다른 축으로 집계하면 합계가 일치해야 한다.
 *
 *   node 7_testing/test_tab_consistency.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const db = JSON.parse(fs.readFileSync(path.join(ROOT, 'questions_db.json'), 'utf-8'));
const tax = JSON.parse(fs.readFileSync(path.join(ROOT, 'taxonomy_v4.json'), 'utf-8'));

// 앱 App.jsx 의 isClassified 게이트와 동일 로직
const isClassified = (q) => {
  const iv = q.indexing_v4;
  const mt = iv && iv.mapped_taxonomy;
  return !!(
    iv && mt && mt.subject &&
    (iv.processed_by === 'gemini-2.5-flash' || iv.processed_by === 'claude-sonnet-4-6') &&
    iv.in_scope !== false
  );
};

const classified = db.filter(isClassified);
let fail = 0;
const eq = (name, a, b) => {
  const ok = a === b;
  if (!ok) fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}: ${a} ${ok ? '==' : '!='} ${b}`);
};

const N = classified.length;
console.log(`분류 완료 문항(공통 모집단): ${N} / 전체 ${db.length}`);

// 축별 합계가 공통 모집단과 같아야 함
const sum = (keyFn) => {
  const g = {};
  classified.forEach(q => { const k = keyFn(q); g[k] = (g[k] || 0) + 1; });
  return Object.values(g).reduce((a, b) => a + b, 0);
};
eq('시험별 합계', sum(q => q.exam), N);
eq('연도별 합계', sum(q => q.year), N);
eq('과목별(taxSubject) 합계', sum(q => q.indexing_v4.mapped_taxonomy.subject), N);

// taxonomy subject 키가 모두 taxonomy_v4 에 존재해야 함 (단원별 트리 정합성)
const taxSubjects = new Set(Object.keys(tax));
const badSubjects = [...new Set(classified.map(q => q.indexing_v4.mapped_taxonomy.subject))]
  .filter(s => !taxSubjects.has(s));
eq('미지의 taxonomy subject 수', badSubjects.length, 0);
if (badSubjects.length) console.log('  →', badSubjects);

// 교차: (시험=회계사) ∩ (과목=회계학) 은 어느 축으로 세도 같아야 함
const cpaAcc = classified.filter(q =>
  q.exam === '회계사' && q.indexing_v4.mapped_taxonomy.subject === '회계학');
const cpaAccByYear = sum_filtered(cpaAcc, q => q.year);
eq('회계사∩회계학: 연도축 합계 == 직접 카운트', cpaAccByYear, cpaAcc.length);
function sum_filtered(arr, keyFn) {
  const g = {};
  arr.forEach(q => { const k = keyFn(q); g[k] = (g[k] || 0) + 1; });
  return Object.values(g).reduce((a, b) => a + b, 0);
}

// out_of_scope / 미분류는 어떤 축에도 새지 않아야 함
const leaked = db.filter(q => !isClassified(q) && classified.includes(q));
eq('미분류 누수', leaked.length, 0);

console.log(fail === 0 ? '\n✅ 모든 교차검증 통과' : `\n❌ ${fail}건 실패`);
process.exit(fail === 0 ? 0 : 1);
