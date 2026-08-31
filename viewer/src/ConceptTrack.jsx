// 「개념 완성」 — 관의 논점 트랙을 하나씩 소진한다.
//
// 인강을 보지 않고도 강의 내용을 전부 익히는 것이 목적이다. 그래서 자유 대화가
// 아니라 **선형 트랙**이다. 남은 논점이 몇 개인지 보이는 것이 이 화면의 핵심이고,
// 그 숫자가 곧 mastery coverage 가 된다.
//
// body·viz·check 는 사전 생성분을 그대로 읽는다 — API 키 없이도, 오프라인에서도
// 여기까지는 동작한다. "더 묻기" 를 눌렀을 때만 대화 엔진이 붙는다.
//
// 목차·장면 렌더는 이 파일이 들지 않는다 — ConceptOutline(단일 목차 모델)과
// ConceptScene(턴 진행)에 넘긴다. 이 파일은 트랙 fetch·진도 저장만 하는 셸이다.
import { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { ChevronRight, ChevronLeft, CheckCircle2, X } from 'lucide-react';
import ConceptOutline from './ConceptOutline';
import ConceptTree from './ConceptTree';
import ConceptTabs from './ConceptTabs';
import ConceptScene, { ConceptRecap, ConceptDone } from './ConceptScene';
import TextbookPanel from './TextbookPanel';
import { stripUnitPrefix } from './unitTree';
import {
  STATE, getTrackProgress, setPointState, leafCounts, nextPoint, leafCoverage,
} from './trackProgress';
import { getChapterMastery, updateChapterMastery, markActiveToday, getApiKey, getPrefs } from './aiLearningStore';
import { record, pathFromLeafId } from './measure/record.js';
import DeepChat from './DeepChat';
import { getAllItems, buildLearnerStatus, recordItem } from './studyDrill';
import { searchChunks, withTerms } from './rag/search';
import { buildContext } from './rag/context';
import { sendMessagesUnified, getProviderForModel } from './aiProviders';

const studyBase = (subjectId) => `/data/study/${subjectId}/`;

export default function ConceptTrack({
  subjectId, leaves, onOpenDeep, onSolve, getQuizCountForLeaf, quizStatsByLeaf, subjectName,
  onOpenSettings,
}) {
  const [leafId, setLeafId] = useState(null);
  const [track, setTrack] = useState(null);      // 이 관의 { leaf_id, title, points }
  const [progress, setProgress] = useState(() => getTrackProgress());
  const [idx, setIdx] = useState(0);
  const [loading, setLoading] = useState(false);
  const [recap, setRecap] = useState(false);   // 관을 마친 뒤의 되짚기 한 판
  const [summary, setSummary] = useState(false);  // 「/정리」 — 이 관의 논점 요약
  // 'concept' 개념 완성 · 'exam' 기출 분석 · 'deep' 심화.
  // 관을 옮겨도 탭은 유지한다 — 기출을 보던 사람은 다음 관에서도 기출부터 본다.
  const [tab, setTab] = useState('concept');
  const [finished, setFinished] = useState(null); // 관을 다 익힌 뒤의 마무리 화면 { right, total }
  const [book, setBook] = useState(false); // 「/교재」 — 4단째 교재 패널

  // 교재의 「이 부분 물어보기」와 슬래시 명령이 ConceptScene 안의 샛길을 부른다.
  const sceneRef = useRef(null);
  const askSideFromTrack = (q) => sceneRef.current?.askSide?.(q);

  // 스트림은 스크롤 박스라 거터가 내용 폭을 줄이는데 도크는 아니다. 순수 CSS 로는
  // 그 폭을 알 수 없어(scrollbar-gutter 는 스크롤 박스에만 걸린다) 런타임에 재어
  // 도크 안쪽 여백으로 되돌린다. 안 맞추면 교재 패널이 열렸을 때 말풍선과 입력줄이
  // 서로 다른 세로선에 선다.
  useEffect(() => {
    const sync = () => {
      const el = document.querySelector('.cs-stream');
      if (!el) return;
      const half = Math.max(0, (el.offsetWidth - el.clientWidth) / 2);
      document.documentElement.style.setProperty('--cs-gutter', `${half}px`);
    };
    sync();
    window.addEventListener('resize', sync);
    return () => window.removeEventListener('resize', sync);
  });

  const leaf = useMemo(() => leaves.find((l) => l.id === leafId) || null, [leaves, leafId]);

  // 관에 들어온 시각. 완료 화면이 「N분」을 보여 준다.
  const enteredAt = useRef(0);
  useEffect(() => { enteredAt.current = Date.now(); setFinished(null); }, [leafId]);

  // 감춘 탭이 선택돼 있으면 개념으로 되돌린다.
  // _extra: 리프를 exam 탭 상태에서 열면 아무 탭도 선택 안 된 화면이 된다.
  useEffect(() => {
    if (leafId?.startsWith('_extra:') && tab === 'exam') setTab('concept');
  }, [leafId, tab]);

  // 과목 레벨 트랙 — 관 축에 안 붙는 선행·총정리 강의 묶음.
  const [extra, setExtra] = useState([]);
  useEffect(() => {
    let dead = false;
    fetch(`${studyBase(subjectId)}lectures/track/_subject.basic.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => { if (!dead) setExtra(d?.leaves || []); })
      .catch(() => { if (!dead) setExtra([]); });
    return () => { dead = true; };
  }, [subjectId]);

  // 목차가 읽을 색인과 범위 규칙. 트랙 파일 전부를 받지 않고 이 둘만 받는다.
  const [index, setIndex] = useState(null);

  // 교재 청크 — 심화·샛길의 검색 재료. 관이 아니라 단원 단위 파일이다.
  const [chunks, setChunks] = useState([]);
  useEffect(() => {
    if (!leaf?.unit_code) { setChunks([]); return undefined; }
    let dead = false;
    fetch(`${studyBase(subjectId)}rag/${leaf.unit_code}.chunks.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => { if (!dead) setChunks(withTerms(d?.chunks || [])); })
      .catch(() => { if (!dead) setChunks([]); });
    return () => { dead = true; };
  }, [subjectId, leaf?.unit_code]);

  // 「/교재」는 근거를 확인하러 여는 것이다. 단원 맨 앞에 떨어뜨리면 확인이 안 된다.
  // 관 제목과 겹치는 첫 청크로 보낸다. 못 찾으면 맨 앞(null).
  const bookFocusId = useMemo(() => {
    const name = stripUnitPrefix(leaf?.title || track?.title || '');
    if (!name || !chunks.length) return null;
    const hit = chunks.find((c) => (c.path || []).some((p) => p.includes(name) || name.includes(p)));
    return hit?.id || null;
  }, [chunks, leaf?.title, track?.title]);

  const [scope, setScope] = useState(null);
  useEffect(() => {
    let dead = false;
    Promise.all([
      fetch(`${studyBase(subjectId)}lectures/track/_index.json`).then((r) => (r.ok ? r.json() : null)).catch(() => null),
      fetch(`${studyBase(subjectId)}lectures/scope.json`).then((r) => (r.ok ? r.json() : null)).catch(() => null),
    ]).then(([i, s]) => { if (!dead) { setIndex(i); setScope(s); } });
    return () => { dead = true; };
  }, [subjectId]);

  // 트랙 로드 — 아직 만들어지지 않은 관·회독이 대부분이므로 404 는 조용히 빈 값.
  useEffect(() => {
    // 이어보기 위치를 track 과 같은 커밋에서 확정한다. setIdx(0) 으로 먼저 그렸다가
    // 별도 effect 에서 되돌리면, 그 중간 렌더의 논점 1번이 SEEN 으로 찍혀버린다
    // (아래 [point?.id] effect 가 idx=0 렌더에도 반응하기 때문). track·idx 를 함께
    // 세팅해 첫 렌더부터 이어보기 위치가 맞도록 한다.
    const resumeIdx = (t) => {
      if (!t?.points?.length) return 0;
      const np = nextPoint(t, getTrackProgress());
      const i = np ? t.points.findIndex((p) => p.id === np.id) : -1;
      return i >= 0 ? i : 0;
    };
    setRecap(false);
    if (leafId?.startsWith('_extra:')) {
      const title = leafId.slice('_extra:'.length);
      const found = extra.find((e) => e.title === title) || null;
      const withId = found ? { ...found, leaf_id: leafId } : null;
      // progressKey 로 leaf_id 를 덮어씀
      if (withId) withId.leaf_id = progressKey;
      setTrack(withId);
      setIdx(resumeIdx(withId));
      setLoading(false);
      return undefined;
    }
    if (!leaf?.unit_code) { setTrack(null); return undefined; }
    let dead = false;
    setLoading(true);
    // 개념은 basic, 기출은 exam. 심화는 트랙이 없다(DeepChat 이 맡는다).
    const suffix = tab === 'exam' ? 'exam' : 'basic';
    fetch(`${studyBase(subjectId)}lectures/track/${leaf.unit_code}.${suffix}.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        if (dead) return;
        const found = d?.leaves?.find((x) => x.leaf_id === leafId) || null;
        // progressKey 로 leaf_id 를 덮어씀
        if (found) found.leaf_id = progressKey;
        setTrack(found);
        setIdx(resumeIdx(found));
      })
      .catch(() => { if (!dead) setTrack(null); })
      .finally(() => { if (!dead) setLoading(false); });
    return () => { dead = true; };
  }, [subjectId, leaf?.unit_code, leafId, extra, tab]);

  // 진도 버킷을 트랙별로 가른다. basic 은 기존 키를 그대로 써서 이미 쌓인 진도를
  // 잃지 않고, exam 만 따로 담는다. 안 가르면 기출 학습이 개념 완성 진도로 섞인다.
  // 선행·총정리는 과목 레벨 트랙이라 기출이 대응하지 않는다. 탭을 감추지만,
  // 어떤 경로로든 exam 상태로 들어와도 진도 키는 튀지 않게 막아 둔다.
  const isExtra = !!leafId?.startsWith('_extra:');
  const progressKey = (tab === 'exam' && !isExtra) ? `${leafId}#exam` : leafId;

  const counts = track ? leafCounts(track, progress) : { total: 0, seen: 0, passed: 0 };
  const point = track?.points?.[idx] || null;

  // coverage 를 실측값으로 기록. 통과 논점 ÷ 전체.
  const syncCoverage = useCallback((next) => {
    // 과목 레벨 트랙(선행·총정리)은 taxonomy 의 관이 아니다. mastery 에 쓰면 존재하지 않는
    // 단원 코드로 기록이 생기고 실력 리포트 평균에 섞인다.
    if (!track || !leafId || leafId.startsWith('_extra:')) return;
    // 기출 학습을 개념 완성 이해도로 기록하지 않는다 — 다른 종류의 실력이다.
    if (tab !== 'concept') return;
    const cov = leafCoverage(track, next);
    const prev = getChapterMastery(leafId, 'basic');
    if (Math.abs((prev.coverage || 0) - cov) < 0.001) return;
    updateChapterMastery(leafId, { coverage: cov }, 'basic');
  }, [track, leafId, tab]);

  // 이미 그 이상으로 기록돼 있으면 아무것도 하지 않는다. 이 가드가 없으면
  // setProgress 가 매번 새 객체를 만들고 → ConceptTrack 이 다시 렌더되고 →
  // onPassed 콜백의 identity 가 바뀌어 ConceptScene 의 effect 가 또 불린다.
  // 실제로 "Maximum update depth exceeded" 가 콘솔을 채우고 있었다.
  const mark = useCallback((state) => {
    if (!point) return;
    if (((progress[progressKey] || {})[point.id] || 0) >= state) return;
    const next = setPointState(progressKey, point.id, state);
    setProgress({ ...next });
    syncCoverage(next);
    markActiveToday();
  }, [progressKey, point, progress, syncCoverage]);

  // 논점을 열면 '설명 봄'
  useEffect(() => {
    if (point) mark(STATE.SEEN);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [point?.id]);

  // 마지막 논점에서 「다음」을 누르면 곧장 되짚기로 넘어간다. 관의 끝이
  // 아무 마무리 없이 멈추면 마지막 문제가 곁다리처럼 느껴진다.
  // 되짚기는 이 관의 quiz 턴을 다시 푸는 판이다. quiz 가 하나도 없는 관
  // (문서형만 있는 관)에서는 판 자체가 성립하지 않으니 들르지 않는다.
  const hasRecap = (track?.points || []).some(
    (p) => (p.turns || []).some((t) => t.who === 'quiz'),
  );

  const goNext = () => {
    const last = (track?.points?.length || 1) - 1;
    if (idx >= last) { if (hasRecap) setRecap(true); else setFinished({ right: 0, total: 0 }); return; }
    setIdx(idx + 1);
  };

  // 심화·샛길이 함께 쓰는 튜터 호출. 키가 없으면 null 을 넘겨 화면이 안내를 띄우게 한다.
  // 키가 있는지는 **실제로 호출할 제공자** 기준으로 본다. getPrefs().provider 는
  // 존재하지 않는 필드라 늘 anthropic 만 봤다(DEFAULT_PREFS 참조).
  // getApiKey('local') 이 더미 키를 돌려주므로 로컬 모델은 자동으로 통과한다.
  const hasKey = !!getApiKey(getProviderForModel(getPrefs().model));
  const askTutor = useCallback(async (question) => {
    const hits = searchChunks(chunks, question);
    const ctx = buildContext({
      question,
      chunks: hits,
      points: (track?.points || []).map((p) => `- ${p.title}: ${p.gist || ''}`).join('\n'),
      record: buildLearnerStatus(leafId, leaf?.title || ''),
    });
    const prefs = getPrefs();
    const res = await sendMessagesUnified({
      model: prefs.model,
      apiKey: getApiKey(getProviderForModel(prefs.model)),
      maxTokens: prefs.max_tokens || 1200,
      system: [
        { type: 'text', text: '당신은 감정평가사 1차 시험 과외 선생님입니다. 학생이 지금 보고 있는 관에 대해 답합니다.' },
        { type: 'text', text: '답한 내용이 어느 대목에서 온 것인지 밝히고, 준 자료에 없는 내용은 「교재에 없습니다」라고 말하고 지어내지 마라.' },
        { type: 'text', text: ctx.text },
      ],
      messages: [{ role: 'user', content: question }],
    });
    return { answer: res?.text || '', cited: ctx.cited };
  }, [chunks, track, leafId, leaf?.title]);

  // ── 슬래시 명령 ────────────────────────────────────────────────────────
  // 여섯 중 다섯은 이미 가진 데이터로 처리한다 — API 키 없이, 오프라인에서 동작한다.
  // 생성이 필요한 것은 「/쉽게」 하나뿐이고, 그것만 대화 엔진으로 넘긴다.
  const runCommand = useCallback((cmd) => {
    switch (cmd) {
      case '/시작':
        setRecap(false);
        setIdx(0);
        break;
      case '/이어서': {
        // 아직 통과하지 못한 첫 논점. 다 끝냈으면 마지막에 머문다.
        const np = track ? nextPoint(track, getTrackProgress()) : null;
        const i = np ? track.points.findIndex((x) => x.id === np.id) : -1;
        setRecap(false);
        setIdx(i >= 0 ? i : Math.max(0, (track?.points?.length || 1) - 1));
        break;
      }
      case '/진단':
        if (hasRecap) setRecap(true);
        break;
      case '/정리':
        setSummary(true);
        break;
      case '/교재':
        setBook((v) => !v);
        break;
      case '/쉽게':
        // 유일하게 생성이 필요한 명령. 사용자가 키를 넣어 둔 경우에만 실제로 답이 온다.
        onOpenDeep?.(leafId, point, '방금 설명을 더 쉬운 말로 다시 해 주세요.');
        break;
      default:
        break;
    }
  }, [track, hasRecap, leafId, point, onOpenDeep]);

  if (!leafId) {
    return (
      <div className="concept-index">
        <h2 className="concept-index-title">개념 완성</h2>
        <p className="concept-index-lede">
          강의가 다룬 논점을 순서대로 하나씩 익힙니다. 다 비우면 그 관을 마친 것입니다.
        </p>
        {extra.filter((e) => e.kind === 'prereq').map((e) => (
          <ExtraCard key={e.title} entry={e} onPick={() => setLeafId(`_extra:${e.title}`)} />
        ))}
        <ConceptOutline leaves={leaves} scope={scope} index={index}
          progress={progress} onPick={setLeafId}
          quizStatsByLeaf={quizStatsByLeaf} subjectName={subjectName} />
        {extra.filter((e) => e.kind === 'review').map((e) => (
          <ExtraCard key={e.title} entry={e} onPick={() => setLeafId(`_extra:${e.title}`)} />
        ))}
      </div>
    );
  }

  // 관을 연 뒤의 모든 화면은 이 셸을 쓴다. 한 갈래라도 빠뜨리면 그 상태에서만
  // 트리가 사라져 본문이 옆으로 튄다.
  const workspace = (inner) => (
    <div className="concept-workspace">
      <ConceptTree
        leaves={leaves} scope={scope} index={index} progress={progress}
        leafId={leafId} quizStatsByLeaf={quizStatsByLeaf}
        subjectName={subjectName} subjectNote={scope?.label || ''}
        onPick={(id) => { setFinished(null); setRecap(false); setLeafId(id); }} />
      {inner}
      {book && (
        <TextbookPanel chunks={chunks} focusId={bookFocusId}
          onClose={() => setBook(false)}
          onAskAbout={hasKey ? (c) => {
            // 교재를 읽다 막히면 그 문단을 물고 대화로 돌아간다 — 샛길의 또 다른 입구다.
            setBook(false);
            askSideFromTrack(`교재의 「${(c.path || []).slice(-1)[0]}」 부분을 쉽게 풀어 설명해 주세요.`);
          } : null} />
      )}
    </div>
  );

  // 심화는 트랙이 없다. 로딩·트랙 없음 분기보다 먼저 가로챈다.
  if (leafId && tab === 'deep') {
    return workspace(
      <div className="concept-runner">
        <ConceptTabs tab={tab} onPick={setTab} />
        <DeepChat
          leafTitle={leaf?.title || ''}
          track={track ? { ...track, leaf_id: leafId } : null}
          items={getAllItems()}
          onAsk={hasKey ? async (q) => askTutor(q) : null}
          onOpenSettings={onOpenSettings}
          onGoPoint={null}
        />
      </div>,
    );
  }

  if (loading) return workspace(<div className="concept-loading">불러오는 중…</div>);

  if (!track) {
    return workspace(
      <div className="concept-index">
        <button type="button" className="concept-back" onClick={() => setLeafId(null)}>
          <ChevronLeft size={14} strokeWidth={1.75} />단원 목록
        </button>
        <p className="concept-index-lede" style={{ marginTop: 14 }}>
          {tab === 'exam'
            ? '이 관의 기출 분석은 아직 준비되지 않았습니다. 개념 완성부터 익혀 두세요.'
            : '이 단원은 아직 논점 트랙이 없습니다. 강의가 다루지 않은 범위이거나 아직 생성 전입니다.'}
        </p>
        {tab === 'exam' && (
          <button type="button" className="concept-op" onClick={() => setTab('concept')}>
            개념 완성으로 →
          </button>
        )}
        {onOpenDeep && (
          <button type="button" className="concept-op" onClick={() => onOpenDeep(leafId)}>
            AI 학습에서 대화로 배우기 →
          </button>
        )}
      </div>,
    );
  }

  const done = counts.passed >= counts.total && counts.total > 0;
  const rec = progress[progressKey] || {};

  if (!track.points?.length) {
    return workspace(
      <div className="concept-runner">
        <header className="concept-head">
          <button type="button" className="concept-back" onClick={() => setLeafId(null)}>
            <ChevronLeft size={14} strokeWidth={1.75} />단원 목록
          </button>
          <h2 className="concept-head-title">{track.title}</h2>
        </header>
        <div className="concept-stage">
          <div className="concept-gist">아직 논점이 없습니다.</div>
        </div>
        <div className="concept-say" />
        <div className="cs-dock">
          <button type="button" className="cs-primary" onClick={() => setLeafId(null)}>목록으로</button>
        </div>
      </div>,
    );
  }

  const pct = counts.total ? Math.round((counts.passed / counts.total) * 100) : 0;
  // 「다음 관으로」 — 과목 레벨 트랙(_extra:)에는 다음이 없다.
  const nextLeafId = (() => {
    if (!leafId || leafId.startsWith('_extra:')) return null;
    const i = leaves.findIndex((l) => l.id === leafId);
    return i >= 0 && i + 1 < leaves.length ? leaves[i + 1].id : null;
  })();

  return workspace(
    <div className="concept-runner">
      <ConceptTabs tab={tab} onPick={setTab}
        right={tab === 'exam' && counts.total ? `기출 ${counts.passed} / ${counts.total}` : null}
        hide={leafId?.startsWith('_extra:') ? ['exam'] : []} />
      <header className="concept-head">
        <button type="button" className="concept-back" onClick={() => setLeafId(null)}>
          <ChevronLeft size={14} strokeWidth={1.75} />단원 목록
        </button>
        <h2 className="concept-head-title">{track.title}</h2>
        <span className="concept-head-count">
          {recap ? '되짚기' : `논점 ${Math.min(idx + 1, counts.total)} / ${counts.total}`}
          <span className="concept-head-passed">· {pct}%</span>
          {/* 완료 안내를 조작 줄 아래 배너로 두면 그 배너가 생기는 순간 조작 줄이
              위로 밀린다 — 이 화면이 지키려는 단 하나가 그거라 머리로 올렸다. */}
          {!recap && !finished && done && hasRecap && (
            <button type="button" className="concept-op" onClick={() => setRecap(true)}>
              <CheckCircle2 size={14} strokeWidth={1.75} />되짚기 한 판
            </button>
          )}
        </span>
        {leaf?.path?.length > 0 && (
          <p className="concept-crumb">{leaf.path.slice(1).join(' › ')}</p>
        )}
        {/* 트랙 하나에 채움 하나. 논점마다 칸을 나누면 경계선이 보여서 진행률이
            여러 개인 것처럼 읽힌다. 논점으로 건너뛰는 일은 「/정리」 시트가 맡는다. */}
        <div className="concept-track" role="progressbar"
          aria-valuenow={counts.passed} aria-valuemin={0} aria-valuemax={counts.total}
          aria-label={`논점 진행 ${counts.passed} / ${counts.total}`}>
          <div className="concept-track-fill"
            style={{ width: counts.total ? `${(counts.passed / counts.total) * 100}%` : 0 }} />
        </div>
      </header>

      {finished
        ? (
          <ConceptDone
            track={track}
            score={finished}
            elapsedMs={enteredAt.current ? Date.now() - enteredAt.current : 0}
            quizCount={getQuizCountForLeaf && leaf ? getQuizCountForLeaf(leaf) : 0}
            onSolve={onSolve && leaf ? () => onSolve(leaf) : null}
            onNextLeaf={nextLeafId ? () => { setFinished(null); setLeafId(nextLeafId); } : null}
            onExit={() => { setFinished(null); setLeafId(null); }}
          />
        )
        : recap
        ? (
          <ConceptRecap track={track}
            onFinish={(sc) => { setRecap(false); setFinished(sc); }}
            onExit={() => { setRecap(false); setLeafId(null); }} />
        )
        : point && (
          <ConceptScene
            ref={sceneRef}
            point={point}
            leafId={leafId}
            seq={idx + 1}
            total={counts.total}
            onCommand={runCommand}
            onPassed={() => mark(STATE.PASSED)}
            onDone={(d) => record({
              id: `concept:${leafId}:${point.id}`,
              leaf: leafId,
              path: pathFromLeafId(leafId),
              subject: pathFromLeafId(leafId)[0] || '',
              stage: 1,
              axis: 'knowledge',
              // 선택지형이지만 2회 오답 시 통과를 박탈하므로 찍기 내성이 높다(§4-3 예외).
              f: 'recog', g: 'machine', strict: true,
              nopt: (point.turns || []).find((t) => t.who === 'quiz')?.choices?.length,
              src: 'internal',
              score: d.score,
              assisted: d.assistedCount > 0,
              tries: d.tries,
              ms: d.ms,
              ts: Date.now(),
            })}
            onNext={goNext}
            onAsk={onOpenDeep ? (text) => onOpenDeep(leafId, point, text) : null}
            onAskSide={hasKey ? async (q) => (await askTutor(q)).answer : null}
            onQueueItem={(it) => {
              recordItem({
                kind: it.kind, idx: it.idx, q: it.q, isCorrect: it.isCorrect,
                leaf: { leafId, subject: subjectId, leafTitle: track?.title || '' },
                gradedBy: it.kind === 'recall' ? 'self' : 'machine',
                f: it.kind === 'recall' ? 'recall' : it.kind === 'ox' ? 'recall' : 'recog',
                nopt: it.kind === 'ox' ? 2 : undefined,
              });
            }}
          />
        )}

      {summary && (
        <div className="cs-panel" role="dialog" aria-label="이 관에서 배운 것">
          <div className="cs-panel-head">
            <span className="cs-panel-label">이 관에서 배운 것</span>
            <button type="button" className="cs-tool" onClick={() => setSummary(false)} aria-label="닫기">
              <X size={15} strokeWidth={1.75} />
            </button>
          </div>
          <div className="cs-panel-body">
            <ol className="cs-summary">
              {(track.points || []).map((p, i) => {
                const st = rec[p.id] || 0;
                return (
                  <li key={p.id} className={st >= STATE.PASSED ? 'is-passed' : st >= STATE.SEEN ? 'is-seen' : ''}>
                    <button type="button" className="cs-summary-row"
                      onClick={() => { setSummary(false); setRecap(false); setIdx(i); }}>
                      <span className="cs-summary-title">{p.title}</span>
                      {p.gist && <span className="cs-summary-gist">{p.gist}</span>}
                    </button>
                  </li>
                );
              })}
            </ol>
          </div>
        </div>
      )}
    </div>,
  );
}

function ExtraCard({ entry, onPick }) {
  const progress = getTrackProgress();
  const rec = progress[`_extra:${entry.title}`] || {};
  const passed = Object.values(rec).filter((s) => s >= STATE.PASSED).length;
  return (
    <button type="button" onClick={onPick} className="concept-extra">
      <span className="concept-extra-kind">{entry.kind === 'prereq' ? '선행' : '총정리'}</span>
      <span className="concept-extra-title">{entry.title}</span>
      {passed > 0 && <span className="concept-extra-count">{passed}개 완료</span>}
      <ChevronRight size={14} strokeWidth={1.75} />
    </button>
  );
}
