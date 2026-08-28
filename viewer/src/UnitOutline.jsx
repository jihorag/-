// 공유 목차(단원 개요) — AI학습·드릴·문제풀이가 동일하게 쓰는 단일 렌더러.
// buildUnitTree로 세부과목›장›절›관 트리를 만들고, 각 단원에 서수 배지(#통합순번 + 계층 "1장·2절")를 붙인다.
// onPick(leaf): 탭별 동작(학습 열기 / 드릴 시작 / 기출 풀기). renderMeta(leaf): 우측 보조정보(진도·기출수 등).
import { useMemo, useState } from 'react';
import { buildUnitTree, stripUnitPrefix } from './unitTree';
import { leafLabel } from './learnState';

const ACCENT = '#4361ee';

function SeqBadge({ ord, accent }) {
  if (!ord) return null;
  return (
    <span title={`${ord.seq}번째 단원 · 과목 총 ${ord.total}단원`}
      style={{ fontSize: '0.6rem', fontWeight: 800, color: '#fff', background: accent, borderRadius: 5, padding: '2px 6px', flexShrink: 0, fontVariantNumeric: 'tabular-nums', lineHeight: 1.3 }}>
      #{ord.seq}
    </span>
  );
}
function HierBadge({ hier }) {
  if (!hier) return null;
  return (
    <span style={{ fontSize: '0.6rem', fontWeight: 800, color: '#475569', background: '#eef0f3', borderRadius: 5, padding: '2px 6px', flexShrink: 0, whiteSpace: 'nowrap', lineHeight: 1.3 }}>
      {hier}
    </span>
  );
}

function LeafRow({ leaf, ord, depth, active, accent, onPick, renderMeta, tierBadge }) {
  return (
    <button onClick={() => onPick && onPick(leaf)}
      style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 7, textAlign: 'left', cursor: 'pointer',
        padding: `8px 10px 8px ${10 + depth * 14}px`, background: active ? '#eef1fe' : 'transparent',
        border: 'none', borderLeft: active ? `3px solid ${accent}` : '3px solid transparent' }}>
      <SeqBadge ord={ord} accent={accent} />
      <HierBadge hier={ord?.hier} />
      <span style={{ flex: 1, minWidth: 0, fontSize: '0.82rem', fontWeight: active ? 800 : 600, color: '#1e293b', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
        {stripUnitPrefix(leafLabel(leaf))}
        {tierBadge && tierBadge(leaf)}
      </span>
      {renderMeta && <span style={{ flexShrink: 0, display: 'inline-flex', alignItems: 'center', gap: 6 }}>{renderMeta(leaf)}</span>}
      <span style={{ color: '#cbd5e1', fontSize: '0.85rem', flexShrink: 0 }}>›</span>
    </button>
  );
}

export default function UnitOutline({
  leaves = [], onPick, currentLeafId, renderMeta, tierBadge,
  search = true, accent = ACCENT, emptyHint = '단원이 없습니다',
}) {
  const { divisions, ordinalById, multiDiv } = useMemo(() => buildUnitTree(leaves), [leaves]);
  const [q, setQ] = useState('');
  const [collapsed, setCollapsed] = useState({}); // chKey → true(접힘)
  const query = q.trim().toLowerCase();
  const searching = query.length > 0;
  const match = (leaf) => !searching || (leaf?.path || []).join(' ').toLowerCase().includes(query) || (leaf?.title || '').toLowerCase().includes(query);
  const ordOf = (leaf) => ordinalById.get(leaf?.id);

  const chapterLeaves = (ch) => {
    const out = [];
    if (ch.leaf) out.push(ch.leaf);
    ch.sections.forEach((sec) => { if (sec.leaf) out.push(sec.leaf); sec.items.forEach((it) => out.push(it.leaf)); });
    return out;
  };

  if (!leaves.length) return <div style={{ padding: 24, textAlign: 'center', color: '#94a3b8', fontSize: '0.82rem' }}>{emptyHint}</div>;

  return (
    <div>
      {search && (
        <div style={{ position: 'sticky', top: 0, background: '#fff', zIndex: 2, padding: '2px 2px 8px' }}>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="단원 검색 (예: 행위능력, 재무제표)"
            style={{ width: '100%', boxSizing: 'border-box', border: '1px solid #e5e7eb', background: '#f8fafc', borderRadius: 9, padding: '8px 11px', fontSize: '0.82rem', outline: 'none' }} />
        </div>
      )}
      {divisions.map((div, di) => (
        <div key={div.name || di} style={{ marginBottom: 4 }}>
          {multiDiv && (
            <div style={{ padding: '9px 10px 5px', fontSize: '0.72rem', fontWeight: 800, color: accent }}>{div.name}</div>
          )}
          {div.chapters.map((ch) => {
            const cLeaves = chapterLeaves(ch);
            if (searching && !cLeaves.some(match)) return null;
            const key = `${di}:${ch.name}`;
            const isCol = !searching && !!collapsed[key];
            const shownCount = cLeaves.filter(match).length;
            return (
              <div key={ch.name} style={{ borderTop: '1px solid #f1f5f9' }}>
                <button onClick={() => setCollapsed((c) => ({ ...c, [key]: !isCol }))}
                  style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 7, textAlign: 'left', cursor: 'pointer', background: 'transparent', border: 'none', padding: '9px 10px' }}>
                  <span style={{ color: '#94a3b8', fontSize: '0.7rem', flexShrink: 0, width: 10, transition: 'transform .15s', transform: isCol ? 'rotate(-90deg)' : 'none' }}>▾</span>
                  <HierBadge hier={ch.hier} />
                  <span style={{ flex: 1, minWidth: 0, fontSize: '0.85rem', fontWeight: 800, color: '#111827', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{stripUnitPrefix(ch.name)}</span>
                  <span style={{ fontSize: '0.66rem', color: '#94a3b8', flexShrink: 0 }}>{shownCount}</span>
                </button>
                {!isCol && (
                  <div>
                    {ch.leaf && match(ch.leaf) && (
                      <LeafRow leaf={ch.leaf} ord={ordOf(ch.leaf)} depth={1} active={ch.leaf.id === currentLeafId} accent={accent} onPick={onPick} renderMeta={renderMeta} tierBadge={tierBadge} />
                    )}
                    {ch.sections.map((sec) => {
                      const sLeaves = sec.leaf ? [sec.leaf, ...sec.items.map((it) => it.leaf)] : sec.items.map((it) => it.leaf);
                      if (searching && !sLeaves.some(match)) return null;
                      return (
                        <div key={sec.name}>
                          {sec.leaf && match(sec.leaf) && (
                            <LeafRow leaf={sec.leaf} ord={ordOf(sec.leaf)} depth={1} active={sec.leaf.id === currentLeafId} accent={accent} onPick={onPick} renderMeta={renderMeta} tierBadge={tierBadge} />
                          )}
                          {!sec.leaf && sec.items.length > 0 && (
                            <div style={{ padding: '5px 10px 3px 24px', fontSize: '0.72rem', fontWeight: 700, color: '#94a3b8' }}>{sec.hier} · {stripUnitPrefix(sec.name)}</div>
                          )}
                          {sec.items.filter((it) => match(it.leaf)).map((it) => (
                            <LeafRow key={it.leaf.id} leaf={it.leaf} ord={ordOf(it.leaf)} depth={2} active={it.leaf.id === currentLeafId} accent={accent} onPick={onPick} renderMeta={renderMeta} tierBadge={tierBadge} />
                          ))}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
