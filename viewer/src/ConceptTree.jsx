// 학습 중에도 옆에 남아 있는 단원 트리 — 시안 250:380.
//
// 관에 들어가면 목차가 통째로 사라져서 지금 어디를 하고 있는지, 다음이 무엇인지
// 알려면 「단원 목록」으로 한 번 나갔다 와야 했다. 이 트리는 그 왕복을 없앤다.
//
// 목차 모델은 만들지 않는다 — buildUnitTree 는 AI 학습·드릴·문제풀이·개념 완성이
// 함께 쓰는 단일 목차다(unitTree.js). 여기서 따로 만들면 네 탭의 목차가 갈라진다.
// ConceptOutline 이 같은 모델로 전면 목차를 그리고, 이 파일은 좁은 폭용이다.
import { useMemo, useState, useRef, useEffect } from 'react';
import { Search } from 'lucide-react';
import { buildUnitTree, stripUnitPrefix } from './unitTree';
import { applyScope } from './trackScope';
import { STATE } from './trackProgress';

/** 장·절 자체가 학습 단위인 leaf 까지 관 항목과 같은 모양으로 편다. */
function flatten(ch) {
  const out = [];
  if (ch.leaf) out.push({ leaf: ch.leaf, name: ch.name, sec: null });
  ch.sections.forEach((sec) => {
    if (sec.leaf) out.push({ leaf: sec.leaf, name: sec.name, sec: null });
    sec.items.forEach((it) => out.push({ leaf: it.leaf, name: it.name, sec: sec.name }));
  });
  return out;
}

export default function ConceptTree({
  leaves, scope, index, progress, leafId, onPick, quizStatsByLeaf, subjectName, subjectNote,
}) {
  const [q, setQ] = useState('');
  const scoped = useMemo(() => applyScope(leaves || [], scope), [leaves, scope]);
  const { divisions } = useMemo(() => buildUnitTree(scoped), [scoped]);

  const needle = q.trim();
  const hit = (name) => !needle || stripUnitPrefix(name).includes(needle);

  const counts = (id) => {
    const total = index?.[id]?.points || 0;
    const rec = (progress || {})[id] || {};
    const passed = Object.values(rec).filter((s) => s >= STATE.PASSED).length;
    return { total, passed };
  };

  // 160행짜리 목록이라 고른 관이 화면 밖에 있을 때가 대부분이다. 관이 바뀌면
  // 그 줄을 가운데로 끌어온다 — 이걸 안 하면 트리를 둔 이유(지금 어디인가)가 없다.
  const onRef = useRef(null);
  useEffect(() => {
    onRef.current?.scrollIntoView({ block: 'center' });
  }, [leafId]);

  return (
    <nav className="ctree" aria-label="단원 트리">
      {subjectName && (
        <div className="ctree-subject">
          <p className="ctree-subject-name">{subjectName}</p>
          {subjectNote && <p className="ctree-subject-note">{subjectNote}</p>}
        </div>
      )}
      <div className="ctree-search">
        <Search size={16} strokeWidth={1.75} aria-hidden />
        <input value={q} onChange={(e) => setQ(e.target.value)}
          placeholder="단원·관 검색" aria-label="단원·관 검색" />
      </div>

      <div className="ctree-list">
        {divisions.map((div) => {
          const chapters = div.chapters
            .map((ch) => ({ ch, rows: flatten(ch).filter((r) => hit(r.name) || hit(ch.name)) }))
            .filter((x) => x.rows.length);
          if (!chapters.length) return null;
          return (
            <div key={div.name}>
              <p className="ctree-div">{div.name}</p>
              {chapters.map(({ ch, rows }) => (
                <div key={ch.name}>
                  <p className="ctree-ch">{ch.hier} {stripUnitPrefix(ch.name)}</p>
                  {rows.map((r) => {
                    const c = counts(r.leaf.id);
                    const stat = quizStatsByLeaf?.[r.leaf.id];
                    const pct = stat && stat.answered > 0 ? Math.round(stat.accuracy * 100) : null;
                    return (
                      <button type="button" key={r.leaf.id}
                        ref={r.leaf.id === leafId ? onRef : null}
                        className={`ctree-row${r.leaf.id === leafId ? ' is-on' : ''}`}
                        disabled={c.total === 0}
                        aria-current={r.leaf.id === leafId ? 'true' : undefined}
                        onClick={() => c.total > 0 && onPick(r.leaf.id)}>
                        <span className="ctree-row-t">
                          <span className="ctree-name">{stripUnitPrefix(r.name)}</span>
                          <span className="ctree-sub">
                            {c.total > 0 ? `논점 ${c.passed} / ${c.total}` : '준비 중'}
                            {stat?.total ? ` · 기출 ${stat.total}` : ''}
                          </span>
                        </span>
                        {/* 아직 안 푼 절은 이 칸을 그냥 비운다. 「—」로 채우면
                            스무 줄이 넘어갈 때 대시가 세로줄을 이뤄 먼저 눈에 들어온다.
                            낮은 정답률만 붉게 세운다 — 다시 볼 곳이 보여야 한다. */}
                        <span className={`ctree-pct${pct !== null && pct < 60 ? ' is-low' : ''}`}>
                          {pct !== null ? `${pct}%` : ''}
                        </span>
                      </button>
                    );
                  })}
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </nav>
  );
}
