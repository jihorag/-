// 「개념 완성」 — 관의 논점 트랙을 하나씩 소진한다.
//
// 인강을 보지 않고도 강의 내용을 전부 익히는 것이 목적이다. 그래서 자유 대화가
// 아니라 **선형 트랙**이다. 남은 논점이 몇 개인지 보이는 것이 이 화면의 핵심이고,
// 그 숫자가 곧 mastery coverage 가 된다.
//
// body·viz·check 는 사전 생성분을 그대로 읽는다 — API 키 없이도, 오프라인에서도
// 여기까지는 동작한다. "더 묻기" 를 눌렀을 때만 대화 엔진이 붙는다.
import { useState, useEffect, useMemo, useCallback } from 'react';
import { ChevronRight, CheckCircle2, HelpCircle, MessageCircle } from 'lucide-react';
import ParsedText from './ParsedText';
import {
  STATE, getTrackProgress, setPointState, leafCounts, nextPoint, leafCoverage,
} from './trackProgress';
import { getChapterMastery, updateChapterMastery, markActiveToday } from './aiLearningStore';

const studyBase = (subjectId) => `/data/study/${subjectId}/`;

export default function ConceptTrack({ subjectId, leaves, onOpenDeep }) {
  const [leafId, setLeafId] = useState(null);
  const [track, setTrack] = useState(null);      // 이 관의 { leaf_id, title, points }
  const [progress, setProgress] = useState(() => getTrackProgress());
  const [idx, setIdx] = useState(0);
  const [revealed, setRevealed] = useState(false);   // check 정답 공개
  const [loading, setLoading] = useState(false);

  const leaf = useMemo(() => leaves.find((l) => l.id === leafId) || null, [leaves, leafId]);

  // 트랙 로드 — 아직 만들어지지 않은 관·회독이 대부분이므로 404 는 조용히 빈 값.
  useEffect(() => {
    if (!leaf?.unit_code) { setTrack(null); return undefined; }
    let dead = false;
    setLoading(true);
    fetch(`${studyBase(subjectId)}lectures/track/${leaf.unit_code}.basic.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        if (dead) return;
        const found = d?.leaves?.find((x) => x.leaf_id === leafId) || null;
        setTrack(found);
        setIdx(0);
        setRevealed(false);
      })
      .catch(() => { if (!dead) setTrack(null); })
      .finally(() => { if (!dead) setLoading(false); });
    return () => { dead = true; };
  }, [subjectId, leaf?.unit_code, leafId]);

  // 트랙을 열면 이어서 볼 논점으로 이동
  useEffect(() => {
    if (!track) return;
    const np = nextPoint(track, progress);
    if (np) {
      const i = track.points.findIndex((p) => p.id === np.id);
      if (i >= 0) setIdx(i);
    }
    // 진도 위치만 맞춘다. progress 를 의존성에 넣으면 답할 때마다 튄다.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [track]);

  const counts = track ? leafCounts(track, progress) : { total: 0, seen: 0, passed: 0 };
  const point = track?.points?.[idx] || null;

  // coverage 를 실측값으로 기록. 통과 논점 ÷ 전체.
  const syncCoverage = useCallback((next) => {
    // 과목 레벨 트랙(선행·총정리)은 taxonomy 의 관이 아니다. mastery 에 쓰면 존재하지 않는
    // 단원 코드로 기록이 생기고 실력 리포트 평균에 섞인다.
    if (!track || !leafId || leafId.startsWith('_extra:')) return;
    const cov = leafCoverage(track, next);
    const prev = getChapterMastery(leafId, 'basic');
    if (Math.abs((prev.coverage || 0) - cov) < 0.001) return;
    updateChapterMastery(leafId, { coverage: cov }, 'basic');
  }, [track, leafId]);

  const mark = (state) => {
    if (!point) return;
    const next = setPointState(leafId, point.id, state);
    setProgress({ ...next });
    syncCoverage(next);
    markActiveToday();
  };

  // 논점을 열면 '설명 봄'
  useEffect(() => {
    if (point) mark(STATE.SEEN);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [point?.id]);

  const goNext = () => {
    setRevealed(false);
    setIdx((i) => Math.min((track?.points?.length || 1) - 1, i + 1));
  };

  if (!leafId) {
    return (
      <div style={{ padding: 16 }}>
        <h2 style={{ fontSize: '1.05rem', margin: '0 0 4px' }}>개념 완성</h2>
        <p style={{ color: '#6b7280', fontSize: '0.84rem', margin: '0 0 14px' }}>
          강의가 다룬 논점을 순서대로 하나씩 익힙니다. 다 비우면 그 관을 마친 것입니다.
        </p>
        <LeafList leaves={leaves} onPick={setLeafId} />
      </div>
    );
  }

  if (loading) return <div style={{ padding: 24, color: '#6b7280' }}>불러오는 중…</div>;

  if (!track) {
    return (
      <div style={{ padding: 16 }}>
        <button onClick={() => setLeafId(null)} style={linkBtn()}>← 단원 목록</button>
        <p style={{ color: '#6b7280', fontSize: '0.86rem', marginTop: 14 }}>
          이 단원은 아직 논점 트랙이 없습니다. 강의가 다루지 않은 범위이거나 아직 생성 전입니다.
        </p>
        {onOpenDeep && (
          <button onClick={() => onOpenDeep(leafId)} style={linkBtn()}>
            AI 학습에서 대화로 배우기 →
          </button>
        )}
      </div>
    );
  }

  const done = counts.passed >= counts.total && counts.total > 0;

  return (
    <div style={{ padding: 16, maxWidth: 760, margin: '0 auto' }}>
      <button onClick={() => setLeafId(null)} style={linkBtn()}>← 단원 목록</button>

      <div style={{ margin: '10px 0 4px', display: 'flex', alignItems: 'center', gap: 8 }}>
        <div style={{ flex: 1, height: 6, background: '#e5e7eb', borderRadius: 3, overflow: 'hidden' }}>
          <div style={{
            width: `${counts.total ? (counts.passed / counts.total) * 100 : 0}%`,
            height: '100%', background: '#374151', transition: 'width 0.3s ease-out',
          }} />
        </div>
        <span style={{ fontSize: '0.76rem', color: '#6b7280', fontWeight: 700, whiteSpace: 'nowrap' }}>
          {counts.passed} / {counts.total}
        </span>
      </div>
      <div style={{ fontSize: '0.78rem', color: '#9ca3af', marginBottom: 14 }}>{track.title}</div>

      {done && (
        <div style={{
          padding: '10px 12px', marginBottom: 14, borderRadius: 8,
          background: '#f3f4f6', fontSize: '0.84rem', color: '#374151', fontWeight: 700,
        }}>
          <CheckCircle2 size={15} style={{ verticalAlign: -2, marginRight: 6 }} />
          이 관의 강의 논점을 모두 마쳤습니다.
        </div>
      )}

      {point && (
        <article>
          <h3 style={{ fontSize: '1.02rem', margin: '0 0 2px' }}>
            {point.seq}. {point.title}
          </h3>
          <p style={{ color: '#6b7280', fontSize: '0.83rem', margin: '0 0 12px' }}>{point.gist}</p>

          {point.viz && (
            <ParsedText text={'```viz ' + point.viz.template + '\n'
              + JSON.stringify({ ...point.viz.params, steps: point.viz.steps }, null, 1)
              + '\n```'} />
          )}

          <ParsedText text={point.body} />

          {point.check && (
            <section style={{
              marginTop: 16, padding: '12px 14px',
              border: '1px solid #e5e7eb', borderRadius: 8, background: '#fafafa',
            }}>
              <div style={{ fontSize: '0.76rem', color: '#6b7280', fontWeight: 700, marginBottom: 6 }}>
                <HelpCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />확인
              </div>
              <ParsedText text={point.check.q} />
              {revealed
                ? (
                  <>
                    <div style={{ marginTop: 10, paddingTop: 10, borderTop: '1px dashed #d1d5db' }}>
                      <ParsedText text={point.check.a} />
                    </div>
                    <div style={{ display: 'flex', gap: 6, marginTop: 12 }}>
                      <button onClick={() => { mark(STATE.PASSED); goNext(); }} style={primaryBtn()}>
                        이해했어요 · 다음 <ChevronRight size={14} style={{ verticalAlign: -2 }} />
                      </button>
                      <button onClick={goNext} style={ghostBtn()}>넘어가기</button>
                    </div>
                  </>
                )
                : (
                  <button onClick={() => setRevealed(true)} style={{ ...ghostBtn(), marginTop: 10 }}>
                    답 확인
                  </button>
                )}
            </section>
          )}

          {onOpenDeep && (
            <button onClick={() => onOpenDeep(leafId)} style={{ ...linkBtn(), marginTop: 16 }}>
              <MessageCircle size={13} style={{ verticalAlign: -2, marginRight: 4 }} />
              이 논점에 대해 더 묻기
            </button>
          )}
        </article>
      )}

      <nav style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 22 }}>
        {track.points.map((p, i) => {
          const s = (progress[leafId] || {})[p.id] || 0;
          return (
            <button key={p.id} onClick={() => { setIdx(i); setRevealed(false); }}
              title={p.title}
              style={{
                width: 26, height: 26, borderRadius: 6, cursor: 'pointer',
                border: i === idx ? '1.5px solid #374151' : '1px solid #e5e7eb',
                background: s >= STATE.PASSED ? '#374151' : s >= STATE.SEEN ? '#d1d5db' : '#fff',
                color: s >= STATE.PASSED ? '#fff' : '#6b7280',
                fontSize: '0.7rem', fontWeight: 700,
              }}>{p.seq}</button>
          );
        })}
      </nav>
    </div>
  );
}

function LeafList({ leaves, onPick }) {
  const progress = getTrackProgress();
  return (
    <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
      {leaves.map((l) => {
        const rec = progress[l.id] || {};
        const passed = Object.values(rec).filter((s) => s >= STATE.PASSED).length;
        return (
          <li key={l.id}>
            <button onClick={() => onPick(l.id)} style={{
              width: '100%', textAlign: 'left', padding: '10px 12px',
              border: '1px solid #e5e7eb', borderRadius: 8, background: '#fff',
              cursor: 'pointer', marginBottom: 6,
              display: 'flex', alignItems: 'center', gap: 8,
            }}>
              <span style={{ flex: 1, fontSize: '0.87rem', color: '#111827' }}>
                {l.path?.slice(-1)[0] || l.title}
              </span>
              {passed > 0 && (
                <span style={{ fontSize: '0.72rem', color: '#6b7280', fontWeight: 700 }}>
                  {passed}개 완료
                </span>
              )}
              <ChevronRight size={14} color="#9ca3af" />
            </button>
          </li>
        );
      })}
    </ul>
  );
}

const linkBtn = () => ({
  background: 'none', border: 'none', padding: 0, cursor: 'pointer',
  color: '#4b5563', fontSize: '0.8rem', fontWeight: 700,
});
const primaryBtn = () => ({
  padding: '7px 12px', borderRadius: 7, border: 'none', cursor: 'pointer',
  background: '#374151', color: '#fff', fontSize: '0.82rem', fontWeight: 700,
});
const ghostBtn = () => ({
  padding: '7px 12px', borderRadius: 7, border: '1px solid #d1d5db', cursor: 'pointer',
  background: '#fff', color: '#374151', fontSize: '0.82rem', fontWeight: 700,
});
