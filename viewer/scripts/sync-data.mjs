// 빌드/개발 시작 전 정본 데이터를 앱(public/data)으로 복사한다.
// Vercel 빌드(npm run build)와 로컬 dev 모두에서 항상 최신 분류가 반영되도록 보장.
// 정본: 저장소 루트의 questions_db.json / taxonomy_v4.json
import { copyFileSync, mkdirSync, existsSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(here, '..', '..');
const destDir = join(here, '..', 'public', 'data');

const pairs = [
  ['questions_db.json', 'questions_db.json'],
  ['taxonomy_v4.json', 'taxonomy.json'],
];

mkdirSync(destDir, { recursive: true });

let synced = 0;
for (const [srcName, destName] of pairs) {
  const src = join(repoRoot, srcName);
  const dest = join(destDir, destName);
  if (!existsSync(src)) {
    // 정본이 없으면(예: 얕은 체크아웃) 기존 public/data 유지하고 경고만.
    console.warn(`[sync-data] source missing, keeping existing: ${srcName}`);
    continue;
  }
  copyFileSync(src, dest);
  const mb = (statSync(dest).size / 1048576).toFixed(1);
  console.log(`[sync-data] ${srcName} -> public/data/${destName} (${mb} MB)`);
  synced++;
}
console.log(`[sync-data] done (${synced}/${pairs.length})`);
