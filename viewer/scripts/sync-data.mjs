// 빌드/개발 시작 전 정본 데이터를 앱(public/data)으로 동기화한다.
//
// 새 포맷 (E2 chunk loading):
//   public/data/manifest.json         — 메타(시험명, 카운트, 분류 수, 파일명)
//   public/data/exams/<NN>.json       — 시험별 questions 배열
//   public/data/taxonomy.json         — 분류 트리(기존 그대로)
//
// 정본: 저장소 루트의 questions_db.json / taxonomy_v4.json
// 정본이 없으면(얕은 체크아웃 등) 기존 public/data 유지하고 경고만.
//
// 거대한 24MB 단일 파일을 시험별 ~30KB~7MB chunk로 분할:
//   - HTTP/2 병렬 fetch로 첫 로드 빠름
//   - 캐시 granularity ↑ (한 시험 갱신해도 다른 시험 캐시 안 깨짐)
//   - SW 데이터 캐시는 vite.config.js의 maxEntries=40 으로 수용

import { readFileSync, writeFileSync, mkdirSync, existsSync, statSync, readdirSync, unlinkSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(here, '..', '..');
const destDir = join(here, '..', 'public', 'data');
const examsDir = join(destDir, 'exams');

mkdirSync(destDir, { recursive: true });
mkdirSync(examsDir, { recursive: true });

// ─── taxonomy ────────────────────────────────────────────
const taxSrc = join(repoRoot, 'taxonomy_v4.json');
const taxDest = join(destDir, 'taxonomy.json');
if (existsSync(taxSrc)) {
  writeFileSync(taxDest, readFileSync(taxSrc));
  const kb = (statSync(taxDest).size / 1024).toFixed(1);
  console.log(`[sync-data] taxonomy_v4.json -> public/data/taxonomy.json (${kb} KB)`);
} else {
  console.warn(`[sync-data] source missing, keeping existing: taxonomy_v4.json`);
}

// ─── questions: 시험별 chunk ──────────────────────────────
// questions_db*.json 파일을 모두 읽어 합친다 (과목별 병렬 작업 충돌 방지)
const qSrc = join(repoRoot, 'questions_db.json');
if (!existsSync(qSrc)) {
  console.warn(`[sync-data] source missing, keeping existing: questions_db.json (chunks unchanged)`);
} else {
  const dbFiles = readdirSync(repoRoot)
    .filter(f => /^questions_db.*\.json$/.test(f))
    .sort();
  const arr = [];
  for (const f of dbFiles) {
    const parsed = JSON.parse(readFileSync(join(repoRoot, f), 'utf8'));
    arr.push(...parsed);
    console.log(`[sync-data] loaded ${f} (${parsed.length}문)`);
  }
  const groups = new Map();
  for (const q of arr) {
    const ex = q.exam || '기타';
    if (!groups.has(ex)) groups.set(ex, []);
    groups.get(ex).push(q);
  }
  // 결정론적 슬롯: 시험명 사전순(파일명도 안정)
  const exams = [...groups.keys()].sort();

  // 분류 통계 (앱이 manifest만 보고 picker UI 그릴 수 있도록)
  const isClassified = (q) => {
    const iv = q.indexing_v4;
    if (!iv) return false;
    if (iv.in_scope === false) return false;
    const mt = iv.mapped_taxonomy;
    return !!(mt && mt.subject &&
      (iv.processed_by === 'gemini-2.5-flash' || iv.processed_by === 'claude-sonnet-4-6'));
  };

  // 기존 chunk 정리(이번 빌드에 없는 시험은 삭제)
  const wantFiles = new Set();
  exams.forEach((_, i) => wantFiles.add(String(i).padStart(2, '0') + '.json'));
  for (const f of readdirSync(examsDir)) {
    if (f.endsWith('.json') && !wantFiles.has(f)) {
      try { unlinkSync(join(examsDir, f)); } catch { /* noop */ }
    }
  }

  const manifestExams = [];
  exams.forEach((name, i) => {
    const list = groups.get(name);
    const file = String(i).padStart(2, '0') + '.json';
    const path = join(examsDir, file);
    writeFileSync(path, JSON.stringify(list));
    const classifiedCount = list.filter(isClassified).length;
    const years = [...new Set(list.map(q => String(q.year || '미상')))].sort();
    const size = statSync(path).size;
    manifestExams.push({
      name, file, count: list.length, classified: classifiedCount,
      years, sizeBytes: size,
    });
    console.log(`[sync-data] chunk ${file} = ${name} · ${list.length}문 (${(size/1024).toFixed(0)} KB)`);
  });

  // questions_db.json 단일 파일은 더 이상 작성하지 않음(과거 캐시는 SW가 정리).
  // 단, 기존 파일이 남아 있으면 삭제해 dist 크기 절감.
  const legacy = join(destDir, 'questions_db.json');
  if (existsSync(legacy)) {
    try { unlinkSync(legacy); console.log(`[sync-data] removed legacy public/data/questions_db.json`); }
    catch { /* noop */ }
  }

  const manifest = {
    built_at: new Date().toISOString(),
    total: arr.length,
    classified: manifestExams.reduce((s, e) => s + e.classified, 0),
    exams: manifestExams,
  };
  writeFileSync(join(destDir, 'manifest.json'), JSON.stringify(manifest));
  console.log(`[sync-data] manifest.json -> ${exams.length} exams, ${arr.length} questions, ${manifest.classified} classified`);
}

console.log(`[sync-data] done`);
