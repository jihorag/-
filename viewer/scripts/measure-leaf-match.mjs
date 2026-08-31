// 기출 문항이 taxonomy leaf 에 실제로 몇 % 붙는지 잰다. 읽기 전용.
//
// proficiencyEngine 은 제목 문자열로 leaf 를 찾는다:
//   titleMap.get(norm(q.taxItemName)) || norm(q.taxSectionName) || norm(q.taxChapterName)
// 여기서 실패하면 그 관의 증거가 통째로 사라진다. P1 엔진 작업 전에 상한을 알아야 한다.
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(here, '..', '..');
const studyDir = join(here, '..', 'public', 'data', 'study');

const norm = (s) => (s || '').replace(/\s+/g, '');

const db = JSON.parse(readFileSync(join(repoRoot, 'questions_db.json'), 'utf8'));

// 과목별 leaf 제목 집합
const titleSets = {};
for (const sid of readdirSync(studyDir)) {
  const p = join(studyDir, sid, 'ai_taxonomy_index.json');
  if (!existsSync(p)) continue;
  const idx = JSON.parse(readFileSync(p, 'utf8'));
  const leaves = idx.leaves || [];
  const set = new Set();
  for (const l of leaves) {
    const t = l.title || (l.path || []).slice(-1)[0];
    if (t) set.add(norm(t));
  }
  titleSets[sid] = { set, count: leaves.length };
}

const SUBJ = {
  '경제학원론': 'economics', '회계학': 'accounting', '민법': 'civil',
  '부동산학원론': 'realestate', '감정평가관계법규': 'law',
};

const stat = {};
let noTax = 0, noSubject = 0, notClassified = 0;
for (const q of db) {
  // V4 분류 조건 확인 (App.jsx processedData와 동일)
  const iv = q.indexing_v4;
  const mt = iv && iv.mapped_taxonomy;
  const isClassified = !!(
    iv && mt && mt.subject &&
    (iv.processed_by === 'gemini-2.5-flash' || iv.processed_by === 'claude-sonnet-4-6' || iv.processed_by === 'aigen') &&
    iv.in_scope !== false
  );

  if (!isClassified) { notClassified += 1; continue; }

  const kor = mt.subject;
  if (!kor) { noTax += 1; continue; }
  const sid = SUBJ[kor];
  if (!sid || !titleSets[sid]) { noSubject += 1; continue; }
  const s = stat[sid] || (stat[sid] = { total: 0, item: 0, section: 0, chapter: 0, miss: 0 });
  s.total += 1;
  const ts = titleSets[sid].set;
  if (ts.has(norm(mt.item))) s.item += 1;
  else if (ts.has(norm(mt.section))) s.section += 1;
  else if (ts.has(norm(mt.chapter))) s.chapter += 1;
  else s.miss += 1;
}

const pct = (a, b) => (b ? ((a / b) * 100).toFixed(1) : '0.0');

console.log(`기출 총 ${db.length}문항`);
console.log(`  V4 분류 미완료           ${notClassified}`);
console.log(`  taxonomy 미매핑          ${noTax}`);
console.log(`  과목 index 없음          ${noSubject}`);
console.log('');
console.log('과목        문항수   관일치   절대체   장대체   실패    붙는비율');
let T = 0, M = 0;
for (const [sid, s] of Object.entries(stat)) {
  const hit = s.item + s.section + s.chapter;
  T += s.total; M += hit;
  console.log(
    `${sid.padEnd(12)}${String(s.total).padStart(6)}` +
    `${String(s.item).padStart(9)}${String(s.section).padStart(9)}` +
    `${String(s.chapter).padStart(9)}${String(s.miss).padStart(7)}` +
    `${pct(hit, s.total).padStart(10)}%   (leaf ${titleSets[sid].count}개)`
  );
}
console.log('');
console.log(`전체 붙는 비율 ${pct(M, T)}%  —  P1 엔진이 기출에서 얻을 수 있는 증거의 상한이다.`);
