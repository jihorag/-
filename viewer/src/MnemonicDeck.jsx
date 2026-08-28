// 🔑 두문자 암기덱 — 과목·단원에 흩어진 `#### 🧠 암기법` 975개를 한 곳에 모아
// '가리고 재현'하는 카드덱. 합격수기: "감관법 두문자 = 평균 올려주는 효자과목".
// 저술이 아니라 이미 있는 교재의 암기법 레이어를 수집·인출 훈련으로 바꾸는 배선 기능.
import { useState, useEffect, useMemo, useRef } from 'react';
import { ArrowLeft, Sparkles } from 'lucide-react';
import { SUBJECTS } from './aiLearningStore';
import { ParsedText } from './ParsedText';
import { useScrollLock } from './uiHooks';

const DECK_KEY = 'mnemonic-deck-v1'; // { [cardId]: { s:'learned'|'again', ts } }
const loadDeck = () => { try { return JSON.parse(localStorage.getItem(DECK_KEY) || '{}') || {}; } catch { return {}; } };
const saveDeck = (v) => { try { localStorage.setItem(DECK_KEY, JSON.stringify(v)); } catch { /* full */ } };

const indexUrl = (s) => s.stage === 2
  ? `/data/study/${s.id}/ai_index.json`
  : `/data/study/${s.id}/ai_taxonomy_index.json`;
const studyBase = (s) => `/data/study/${s.id}/`;

// 인덱스에서 유니크 단원 파일 목록을 뽑는다 (1차 taxonomy leaves / 2차 units 모두 대응).
function unitFilesFrom(raw) {
  const out = []; const seen = new Set();
  const push = (file, title) => { if (file && !seen.has(file)) { seen.add(file); out.push({ file, title: title || '' }); } };
  if (raw?.stage === 2 && Array.isArray(raw.units)) {
    raw.units.forEach((u) => push(u.unit_file, u.title));
  } else {
    const leaves = raw?.leaves || (Array.isArray(raw) ? raw : []);
    leaves.forEach((l) => push(l.unit_file, (l.path && l.path[0]) || l.title));
  }
  return out;
}

// 한 단원 MD에서 `#### 🧠 암기법` 섹션들을 뽑아 카드로. topic = 직전 ### 제목.
function extractMnemonics(md, unitLabel) {
  const lines = md.split('\n');
  const cards = [];
  let topic = unitLabel;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    const h2 = l.match(/^##\s+(.+)$/);       // 레이어 헤딩 → topic 초기화
    if (h2) { topic = unitLabel; continue; }
    const h3 = l.match(/^###\s+(.+)$/);
    if (h3) { topic = h3[1].replace(/<a\s+name=.*?<\/a>/gi, '').replace(/^\[|\]$/g, '').trim(); continue; }
    if (/^####\s*🧠\s*암기법/.test(l)) {
      const buf = []; let j = i + 1;
      for (; j < lines.length; j++) { if (/^#{1,4}\s/.test(lines[j])) break; buf.push(lines[j]); }
      const body = buf.join('\n').trim();
      if (body) cards.push({ topic, body });
      i = j - 1;
    }
  }
  return cards;
}

const normKey = (s) => (s || '').replace(/\s+/g, '').slice(0, 44);

export default function MnemonicDeck({ onClose, initialSubjectId }) {
  useScrollLock(true);
  const [subjectId, setSubjectId] = useState(initialSubjectId || null);
  const [loading, setLoading] = useState(false);
  const [cards, setCards] = useState([]);
  const [idx, setIdx] = useState(0);
  const [reveal, setReveal] = useState(false);
  const [onlyAgain, setOnlyAgain] = useState(false);
  const [deck, setDeck] = useState(loadDeck);
  const subj = SUBJECTS.find((s) => s.id === subjectId);

  // 과목 선택 시 그 과목의 모든 단원에서 암기법 수집 (레이어 중복은 본문으로 dedup)
  useEffect(() => {
    if (!subj) { setCards([]); return; }
    let dead = false;
    setLoading(true); setCards([]); setIdx(0); setReveal(false);
    fetch(indexUrl(subj)).then((r) => r.json()).then(async (raw) => {
      const files = unitFilesFrom(raw);
      const all = []; const seen = new Set();
      await Promise.all(files.map(({ file, title }) =>
        fetch(studyBase(subj) + file).then((r) => (r.ok ? r.text() : '')).then((md) => {
          if (!md) return;
          for (const c of extractMnemonics(md, title)) {
            const k = normKey(c.body);
            if (seen.has(k)) continue; seen.add(k);
            all.push({ id: `${subj.id}::${file}::${all.length}`, ...c });
          }
        }).catch(() => {})
      ));
      if (!dead) { setCards(all); setLoading(false); }
    }).catch(() => { if (!dead) { setCards([]); setLoading(false); } });
    return () => { dead = true; };
  }, [subjectId]);

  const view = useMemo(() => onlyAgain ? cards.filter((c) => deck[c.id]?.s === 'again') : cards, [cards, onlyAgain, deck]);
  const card = view[idx] || null;
  const mark = (s) => {
    if (!card) return;
    setDeck((prev) => { const n = { ...prev, [card.id]: { s, ts: Date.now() } }; saveDeck(n); return n; });
    next();
  };
  const next = () => { setReveal(false); setIdx((i) => Math.min(view.length - 1, i + 1)); };
  const prev = () => { setReveal(false); setIdx((i) => Math.max(0, i - 1)); };
  useEffect(() => { if (idx > view.length - 1) setIdx(Math.max(0, view.length - 1)); }, [view.length]);

  const learnedCount = useMemo(() => cards.filter((c) => deck[c.id]?.s === 'learned').length, [cards, deck]);
  const againCount = useMemo(() => cards.filter((c) => deck[c.id]?.s === 'again').length, [cards, deck]);

  const wrap = (children) => (
    <div style={{ position: 'fixed', inset: 0, zIndex: 3000, background: '#f4f2ec', display: 'flex', flexDirection: 'column' }}>
      {children}
    </div>
  );

  // ── 과목 선택 ──
  if (!subj) {
    return wrap(
      <>
        <Head onBack={onClose} title="🔑 두문자 암기덱" sub="과목을 골라 암기법을 한 장씩 인출하세요" />
        <div style={{ flex: 1, overflowY: 'auto', padding: 16 }}>
          {[1, 2].map((stage) => (
            <div key={stage} style={{ marginBottom: 18 }}>
              <div style={{ fontSize: '0.82rem', fontWeight: 800, color: '#6b7280', marginBottom: 10 }}>{stage === 1 ? '📖 1차' : '✍️ 2차'}</div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(150px,1fr))', gap: 12 }}>
                {SUBJECTS.filter((s) => s.stage === stage).map((s) => (
                  <button key={s.id} onClick={() => { setSubjectId(s.id); setOnlyAgain(false); }}
                    style={{ background: '#fff', border: '1px solid #eae6dc', borderRadius: 16, padding: '18px 16px', textAlign: 'left', cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,23,51,0.05)' }}>
                    <div style={{ fontSize: '1.8rem' }}>{s.icon}</div>
                    <div style={{ fontWeight: 800, color: '#191F28', marginTop: 8 }}>{s.short}</div>
                    <div style={{ fontSize: '0.76rem', color: '#8B95A1', marginTop: 2 }}>{s.title}</div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </>
    );
  }

  // ── 덱 ──
  return wrap(
    <>
      <Head onBack={() => setSubjectId(null)} title={`🔑 ${subj.short} 암기덱`}
        sub={loading ? '암기법을 모으는 중…' : `${cards.length}장 · ✅외움 ${learnedCount} · 🔁다시 ${againCount}`} />
      {!loading && cards.length > 0 && (
        <div style={{ display: 'flex', gap: 8, padding: '0 16px 8px', alignItems: 'center' }}>
          <button onClick={() => { setOnlyAgain((v) => !v); setIdx(0); setReveal(false); }}
            style={{ fontSize: '0.74rem', fontWeight: 700, padding: '5px 12px', borderRadius: 999, cursor: 'pointer',
              border: `1px solid ${onlyAgain ? '#c2410c' : '#e5e7eb'}`, background: onlyAgain ? '#ffedd5' : '#fff', color: onlyAgain ? '#c2410c' : '#6b7280' }}>
            🔁 다시 볼 것만 {onlyAgain ? 'ON' : ''}
          </button>
          <span style={{ fontSize: '0.74rem', color: '#9ca3af', marginLeft: 'auto' }}>{view.length ? idx + 1 : 0} / {view.length}</span>
        </div>
      )}
      <div style={{ flex: 1, minHeight: 0, overflowY: 'auto', padding: '4px 16px 16px', display: 'flex', flexDirection: 'column' }}>
        {loading && <Center>📚 {subj.short} 전 단원에서 암기법을 모으는 중…</Center>}
        {!loading && cards.length === 0 && <Center>이 과목엔 아직 정리된 암기법이 없어요.</Center>}
        {!loading && cards.length > 0 && view.length === 0 && <Center>🎉 '다시 볼 것'이 없어요! 필터를 꺼보세요.</Center>}
        {!loading && card && (
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <div style={{ background: '#fff', border: '1px solid #eae6dc', borderRadius: 16, padding: '18px 18px 20px', flex: 1, overflowY: 'auto', boxShadow: '0 4px 16px rgba(0,23,51,0.06)' }}>
              <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#7c3aed', letterSpacing: '0.02em' }}>🔑 암기법</div>
              <div style={{ fontSize: '1.02rem', fontWeight: 800, color: '#191F28', marginTop: 6, lineHeight: 1.4 }}>{card.topic}</div>
              <div style={{ borderTop: '1px dashed #e5e7eb', margin: '14px 0' }} />
              {reveal ? (
                <div className="parsed-body" style={{ fontSize: '0.94rem', lineHeight: 1.7, color: '#1f2937' }}>
                  <ParsedText text={card.body} />
                </div>
              ) : (
                <button onClick={() => setReveal(true)}
                  style={{ width: '100%', minHeight: 120, border: '2px dashed #ddd6fe', borderRadius: 12, background: '#faf5ff', color: '#7c3aed', fontWeight: 800, fontSize: '0.92rem', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 6 }}>
                  <Sparkles size={22} />
                  <span>머릿속으로 먼저 떠올린 뒤 — 탭하여 확인</span>
                </button>
              )}
            </div>
            {/* 하단 조작 */}
            <div style={{ display: 'flex', gap: 8, marginTop: 12, flexShrink: 0 }}>
              <button onClick={prev} disabled={idx === 0}
                style={{ flex: '0 0 auto', padding: '12px 16px', borderRadius: 12, border: '1px solid #e5e7eb', background: '#fff', color: idx === 0 ? '#d1d5db' : '#6b7280', fontWeight: 700, cursor: idx === 0 ? 'default' : 'pointer' }}>← 이전</button>
              {reveal ? (
                <>
                  <button onClick={() => mark('again')}
                    style={{ flex: 1, padding: '12px', borderRadius: 12, border: '1px solid #fdba74', background: '#fff7ed', color: '#c2410c', fontWeight: 800, cursor: 'pointer', minHeight: 48 }}>🔁 다시</button>
                  <button onClick={() => mark('learned')}
                    style={{ flex: 1, padding: '12px', borderRadius: 12, border: 'none', background: '#7c3aed', color: '#fff', fontWeight: 800, cursor: 'pointer', minHeight: 48 }}>✅ 외웠음</button>
                </>
              ) : (
                <button onClick={next} disabled={idx >= view.length - 1}
                  style={{ flex: 1, padding: '12px', borderRadius: 12, border: '1px solid #e5e7eb', background: '#fff', color: '#6b7280', fontWeight: 700, cursor: 'pointer', minHeight: 48 }}>건너뛰기 →</button>
              )}
            </div>
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
      <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#191F28' }}>{title}</div>
      <div style={{ fontSize: '0.8rem', color: '#8B95A1', marginTop: 3 }}>{sub}</div>
    </div>
  );
}
function Center({ children }) {
  return <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', color: '#9ca3af', fontSize: '0.9rem', padding: 30 }}>{children}</div>;
}
