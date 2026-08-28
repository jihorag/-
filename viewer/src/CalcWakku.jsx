// 🧮 경제 계산 와꾸 — 경제학 단원 워크북의 표채우기 계산 연습을 모아 푸는 surface.
// 경제 단원의 계산 와꾸는 파일 끝 '✏️ 워크북' 레이어에 있어 taxonomy leaf 슬라이스로는
// 닿지 않는다. 이 화면은 단원 파일을 직접 읽어 그 구간만 잘라 PracticeCard로 렌더한다.
import { useState, useEffect } from 'react';
import { ArrowLeft, Calculator } from 'lucide-react';
import { ParsedText } from './ParsedText';
import { useScrollLock } from './uiHooks';

const IDX = '/data/study/economics/ai_taxonomy_index.json';
const base = '/data/study/economics/';
const WB_RE = /^##\s*(?:<a\s+name="워크북"[^>]*>\s*<\/a>\s*)?✏️\s*워크북/m;
const WAKKU_RE = /^###\s*\[계산\s*와꾸\]/m;

// 워크북(계산 와꾸) 구간만 잘라낸다. 계산 와꾸 소제목이 있으면 그 앞부터, 없으면 워크북 헤딩부터 EOF.
function sliceWakku(md) {
  const lines = md.split('\n');
  let start = -1;
  for (let i = 0; i < lines.length; i++) { if (/^###\s*\[계산\s*와꾸\]/.test(lines[i])) { start = i; break; } }
  if (start < 0) return '';
  return lines.slice(start).join('\n');
}
const countWakku = (md) => (md.match(/```연습/g) || []).length;

export default function CalcWakku({ onClose }) {
  useScrollLock(true);
  const [units, setUnits] = useState(null); // [{file, code, chapter, root, n}]
  const [sel, setSel] = useState(null);     // {file, chapter, code}
  const [md, setMd] = useState('');
  const [loading, setLoading] = useState(false);

  // 단원 목록 + 각 단원의 계산 와꾸 연습 수 스캔
  useEffect(() => {
    let dead = false;
    fetch(IDX).then((r) => r.json()).then(async (raw) => {
      const leaves = raw.leaves || [];
      const byFile = new Map();
      for (const l of leaves) {
        const f = l.unit_file; if (!f || byFile.has(f)) continue;
        byFile.set(f, { file: f, code: l.unit_code || '', chapter: (l.path && l.path[1]) || l.title || f, root: (l.path && l.path[0]) || '' });
      }
      const arr = [...byFile.values()];
      await Promise.all(arr.map((u) => fetch(base + u.file).then((r) => (r.ok ? r.text() : '')).then((t) => {
        u.n = t && WAKKU_RE.test(t) ? countWakku(sliceWakku(t)) : 0;
      }).catch(() => { u.n = 0; })));
      if (!dead) setUnits(arr.filter((u) => u.n > 0));
    }).catch(() => { if (!dead) setUnits([]); });
    return () => { dead = true; };
  }, []);

  useEffect(() => {
    if (!sel) { setMd(''); return; }
    let dead = false; setLoading(true); setMd('');
    fetch(base + sel.file).then((r) => r.text()).then((t) => { if (!dead) { setMd(sliceWakku(t)); setLoading(false); } })
      .catch(() => { if (!dead) { setMd(''); setLoading(false); } });
    return () => { dead = true; };
  }, [sel]);

  const wrap = (children) => (
    <div style={{ position: 'fixed', inset: 0, zIndex: 3000, background: '#f4f2ec', display: 'flex', flexDirection: 'column' }}>{children}</div>
  );

  // ── 단원 선택 ──
  if (!sel) {
    const total = units ? units.reduce((s, u) => s + u.n, 0) : 0;
    // root(미시/거시/국제/재정)별 묶기
    const groups = {};
    (units || []).forEach((u) => { (groups[u.root] = groups[u.root] || []).push(u); });
    return wrap(
      <>
        <Head onBack={onClose} title="경제 계산 와꾸"
          sub={units == null ? '계산 연습을 모으는 중…' : `${total}개 표채우기 — 단원을 골라 표를 채워보세요`} />
        <div style={{ flex: 1, overflowY: 'auto', padding: 16 }}>
          {units == null && <Center>📚 경제 전 단원에서 계산 와꾸를 스캔하는 중…</Center>}
          {units && units.length === 0 && <Center>계산 와꾸가 아직 없어요.</Center>}
          {Object.entries(groups).map(([root, us]) => (
            <div key={root} style={{ marginBottom: 18 }}>
              <div style={{ fontSize: '0.82rem', fontWeight: 800, color: '#6b7280', marginBottom: 10 }}>{root}</div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(160px,1fr))', gap: 12 }}>
                {us.map((u) => (
                  <button key={u.file} onClick={() => setSel(u)}
                    style={{ background: '#fff', border: '1px solid #eae6dc', borderRadius: 16, padding: '16px 14px', textAlign: 'left', cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,23,51,0.05)' }}>
                    <div style={{ fontSize: '0.68rem', fontWeight: 800, color: '#0891b2' }}>{u.code}</div>
                    <div style={{ fontWeight: 800, color: '#191F28', marginTop: 4, fontSize: '0.92rem', lineHeight: 1.35 }}>{u.chapter}</div>
                    <div style={{ fontSize: '0.74rem', color: '#0891b2', marginTop: 8, fontWeight: 700 }}>🧮 표채우기 {u.n}개</div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </>
    );
  }

  // ── 단원 계산 와꾸 ──
  return wrap(
    <>
      <Head onBack={() => setSel(null)} title={sel.chapter} sub={`${sel.code} · 표를 채우고 「채점」으로 확인하세요`} />
      <div style={{ flex: 1, minHeight: 0, overflowY: 'auto', padding: '10px 16px 24px' }}>
        {loading && <Center>불러오는 중…</Center>}
        {!loading && !md && <Center>이 단원엔 계산 와꾸가 없어요.</Center>}
        {!loading && md && (
          <div className="parsed-body" style={{ maxWidth: 720, margin: '0 auto' }}>
            <ParsedText text={md} />
          </div>
        )}
      </div>
    </>
  );
}

function Head({ onBack, title, sub }) {
  return (
    <div style={{ padding: 'calc(12px + env(safe-area-inset-top,0px)) 16px 10px', background: '#fff', borderBottom: '1px solid #eae6dc', flexShrink: 0 }}>
      <button onClick={onBack} style={{ display: 'flex', alignItems: 'center', gap: 6, border: 'none', background: 'none', cursor: 'pointer', color: '#6b7280', fontWeight: 600, padding: 0, marginBottom: 8 }}>
        <ArrowLeft size={22} /> 뒤로
      </button>
      <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#191F28', display: 'flex', alignItems: 'center', gap: 6 }}>
        <Calculator size={20} color="#0891b2" /> {title}
      </div>
      <div style={{ fontSize: '0.8rem', color: '#8B95A1', marginTop: 3 }}>{sub}</div>
    </div>
  );
}
function Center({ children }) {
  return <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', color: '#9ca3af', fontSize: '0.9rem', padding: 40, minHeight: 160 }}>{children}</div>;
}
