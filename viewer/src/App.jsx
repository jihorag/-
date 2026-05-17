import { useState, useMemo, useEffect, useCallback, useRef } from 'react';
import { ChevronLeft, ArrowLeft, Loader2 } from 'lucide-react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

// v4 난이도(1~5) 배지 메타: 색/라벨
const DIFFICULTY_META = {
  1: { label: '난이도 1 · 매우쉬움', bg: '#ecfdf5', fg: '#047857' },
  2: { label: '난이도 2 · 쉬움', bg: '#f0fdf4', fg: '#15803d' },
  3: { label: '난이도 3 · 보통', bg: '#fefce8', fg: '#a16207' },
  4: { label: '난이도 4 · 어려움', bg: '#fff7ed', fg: '#c2410c' },
  5: { label: '난이도 5 · 매우어려움', bg: '#fef2f2', fg: '#b91c1c' },
};

// ===== 학습 진행률 (localStorage) =====
const PROGRESS_KEY = 'quiz-progress-v1';
const qid = (q) => q.id || `${q.exam}_${q.year}_${q.number}`;

const loadProgress = () => {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}') || {};
  } catch {
    return {};
  }
};

// 검색·필터 영속화 (새로고침/딥링크 시 유지)
const FILTERS_KEY = 'quiz-filters-v1';
const EMPTY_FILTERS = { exams: [], subjects: [], years: [], diffs: [], kw: '' };
const loadFilters = () => {
  try {
    const f = JSON.parse(localStorage.getItem(FILTERS_KEY) || 'null');
    return f && typeof f === 'object' ? { ...EMPTY_FILTERS, ...f } : { ...EMPTY_FILTERS };
  } catch {
    return { ...EMPTY_FILTERS };
  }
};

// 진행률 상태 + 영속화 훅. record(q, sel) 로 기록, reset() 으로 초기화.
const useProgress = () => {
  const [progress, setProgress] = useState(loadProgress);
  const persist = (next) => {
    setProgress(next);
    try { localStorage.setItem(PROGRESS_KEY, JSON.stringify(next)); } catch { /* quota/SSR */ }
  };
  const record = (q, sel) => {
    const id = qid(q);
    if (progress[id]) return; // 최초 응답만 진행률에 반영
    persist({ ...progress, [id]: { sel, correct: sel === q.answer, ts: Date.now() } });
  };
  const reset = () => persist({});
  const clearMany = (ids) => {
    const set = new Set(ids);
    const next = {};
    for (const k in progress) if (!set.has(k)) next[k] = progress[k];
    persist(next);
  };
  return { progress, record, reset, clearMany };
};

// 문항 배열에 대한 진행 통계
const progressStats = (questions, progress) => {
  let answered = 0, correct = 0, dSum = 0, dCnt = 0;
  for (const q of questions) {
    if (typeof q.difficulty === 'number') { dSum += q.difficulty; dCnt++; }
    const p = progress[qid(q)];
    if (p) { answered++; if (p.correct) correct++; }
  }
  // avgDiff: 그룹의 평균 난이도(1~5), level: 색/라벨용 반올림값
  const avgDiff = dCnt ? dSum / dCnt : null;
  return {
    answered, correct, total: questions.length,
    avgDiff, level: avgDiff ? Math.round(avgDiff) : null,
  };
};

// ===== URL 라우팅 (해시 동기화) =====
// 네비게이션 계층을 #/seg/seg.. 로 직렬화. 빈 값은 '-'.
const NAV_KEYS = ['viewMode', 'currentView', 'scope', 'taxSubject', 'taxSubSubject', 'taxChapter', 'taxSection'];
const enc = (v) => (v == null || v === '' ? '-' : encodeURIComponent(v));
const dec = (v) => (v == null || v === '-' ? null : decodeURIComponent(v));

const serializeNav = (s) => {
  const scope = s.taxScope ? `${s.taxScope.kind}~${s.taxScope.value}` : null;
  const parts = [s.viewMode, s.currentView, scope, s.taxSubject, s.taxSubSubject, s.taxChapter, s.taxSection];
  return '#/' + parts.map(enc).join('/');
};

const parseNav = (hash) => {
  if (!hash || !hash.startsWith('#/')) return null;
  const segs = hash.slice(2).split('/');
  if (segs.length < 2) return null;
  const obj = {};
  NAV_KEYS.forEach((k, i) => { obj[k] = dec(segs[i]); });
  let taxScope = null;
  if (obj.scope) {
    const [kind, ...rest] = obj.scope.split('~');
    const value = rest.join('~');
    if (kind === 'exam' || kind === 'year') {
      taxScope = { kind, value, label: kind === 'year' ? `${value}년` : value };
    }
  }
  return {
    viewMode: obj.viewMode || 'exam',
    currentView: obj.currentView || 'dashboard',
    taxScope,
    taxSubject: obj.taxSubject,
    taxSubSubject: obj.taxSubSubject,
    taxChapter: obj.taxChapter,
    taxSection: obj.taxSection,
  };
};

// Component to parse and render text with inline images and math
const ParsedText = ({ text }) => {
  if (!text) return null;
  const parts = text.split(/(\[IMAGE:\s*.*?\])/g);
  return (
    <>
      {parts.map((part, i) => {
        const imgMatch = part.match(/\[IMAGE:\s*(.*?)\]/);
        if (imgMatch) {
          const rawName = imgMatch[1].split('/').pop();
          // PNG/GIF는 빌드 시 동일 파일명의 WebP로 변환됨(확장자만 교체).
          const imageName = rawName.replace(/\.(png|gif)$/i, '.webp');
          return (
            <img
              key={i}
              src={`/images/${imageName}`}
              alt="content"
              loading="lazy"
              decoding="async"
              onError={(e) => {
                // 원본 소실 이미지: 깨진 아이콘 대신 안내로 대체
                const ph = document.createElement('span');
                ph.textContent = '[이미지 없음]';
                ph.style.cssText = 'display:inline-block;color:#9ca3af;font-size:0.85rem;padding:8px 0';
                e.currentTarget.replaceWith(ph);
              }}
              style={{ maxWidth: '100%', display: 'block', margin: '12px auto', borderRadius: '4px' }}
            />
          );
        }
        
        // Render math in the text part
        const mathParts = part.split(/(\$[\s\S]*?\$)/g);
        return mathParts.map((mathPart, j) => {
          if (mathPart.startsWith('$') && mathPart.endsWith('$')) {
            const math = mathPart.slice(1, -1);
            try {
              const html = katex.renderToString(math, { 
                throwOnError: false,
                output: 'html' // Only output HTML to prevent duplicate text when copy-pasting
              });
              return <span key={`${i}-${j}`} dangerouslySetInnerHTML={{ __html: html }} />;
            } catch {
              return <span key={`${i}-${j}`}>{mathPart}</span>;
            }
          }
          return <span key={`${i}-${j}`}>{mathPart}</span>;
        });
      })}
    </>
  );
};

// Interactive Question Component
const QuestionItem = ({ q, prior, onAnswer }) => {
  const [selectedOpt, setSelectedOpt] = useState(prior ? prior.sel : null);
  const isRevealed = selectedOpt !== null;

  const handleOptionClick = (optIdx) => {
    if (isRevealed) return; // Prevent changing answer after revealed
    const sel = String(optIdx + 1);
    setSelectedOpt(sel);
    if (onAnswer) onAnswer(q, sel);
  };

  return (
    <div style={{ background: '#fff', borderRadius: '12px', padding: '24px', marginBottom: '24px', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', gap: '8px' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontWeight: '700', fontSize: '1.125rem', color: '#2563eb' }}>Q. {q.number}</span>
          {typeof q.difficulty === 'number' && (() => {
            const m = DIFFICULTY_META[q.difficulty] || DIFFICULTY_META[3];
            return (
              <span style={{
                fontSize: '0.75rem', fontWeight: 700, padding: '2px 8px', borderRadius: '999px',
                background: m.bg, color: m.fg
              }}>
                {m.label}
              </span>
            );
          })()}
        </span>
        <span style={{ fontSize: '0.875rem', color: '#9ca3af' }}>
          {q.exam} {q.year}년 {q.number}번
        </span>
      </div>
      
      <h3 style={{ fontSize: '1.125rem', lineHeight: '1.6', marginBottom: '20px', fontWeight: '600' }}>
        <ParsedText text={q.question} />
      </h3>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
        {q.options && q.options.map((opt, optIdx) => {
          const optNumber = String(optIdx + 1);
          const isCorrectAnswer = q.answer === optNumber;
          const isSelected = selectedOpt === optNumber;
          
          let bgColor = '#f9fafb';
          let borderColor = '#e5e7eb';
          let badgeBg = '#fff';
          let badgeColor = '#4b5563';
          let badgeBorder = '1px solid #d1d5db';

          if (isRevealed) {
            if (isCorrectAnswer) {
              bgColor = '#eff6ff';
              borderColor = '#bfdbfe';
              badgeBg = '#3b82f6';
              badgeColor = '#fff';
              badgeBorder = 'none';
            } else if (isSelected && !isCorrectAnswer) {
              bgColor = '#fef2f2';
              borderColor = '#fecaca';
              badgeBg = '#ef4444';
              badgeColor = '#fff';
              badgeBorder = 'none';
            }
          } else {
            if (isSelected) {
              // Hover or active state could be added here if we wanted
            }
          }

          return (
            <div 
              key={optIdx} 
              onClick={() => handleOptionClick(optIdx)}
              style={{ 
                padding: '12px 16px', 
                borderRadius: '8px', 
                background: bgColor,
                border: borderColor,
                display: 'flex',
                alignItems: 'flex-start',
                cursor: isRevealed ? 'default' : 'pointer',
                transition: 'all 0.2s'
              }}
            >
              <span style={{ 
                display: 'inline-flex', 
                alignItems: 'center', 
                justifyContent: 'center', 
                width: '24px', 
                height: '24px', 
                borderRadius: '50%', 
                background: badgeBg,
                color: badgeColor,
                border: badgeBorder,
                marginRight: '12px',
                fontSize: '0.875rem',
                fontWeight: '600',
                flexShrink: 0
              }}>
                {optIdx + 1}
              </span>
              <div style={{ fontSize: '0.95rem', lineHeight: '1.5', color: '#1f2937' }}>
                <ParsedText text={opt} />
              </div>
            </div>
          );
        })}
      </div>
      
      {isRevealed && q.explanation && (
        <div style={{ padding: '16px', background: '#f3f4f6', borderRadius: '8px', borderLeft: '4px solid #3b82f6', animation: 'fadeIn 0.3s ease-in-out' }}>
          <div style={{ fontWeight: '700', marginBottom: '8px', fontSize: '0.95rem', display: 'flex', justifyContent: 'space-between' }}>
            <span>해설</span>
            <span style={{ color: selectedOpt === q.answer ? '#16a34a' : '#ef4444' }}>
              {selectedOpt === q.answer ? '정답입니다!' : '오답입니다.'}
            </span>
          </div>
          <div style={{ fontSize: '0.95rem', lineHeight: '1.6', color: '#4b5563' }}>
            <ParsedText text={q.explanation} />
          </div>
        </div>
      )}
    </div>
  );
};

const App = () => {
  const [questionsData, setQuestionsData] = useState([]);
  const [taxonomyData, setTaxonomyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  // 새로고침/딥링크 복원: 최초 렌더에서 URL 해시를 1회 파싱해 초기 상태로 사용
  const [bootNav] = useState(() => parseNav(typeof window !== 'undefined' ? window.location.hash : ''));
  const bootView = (() => {
    if (!bootNav) return 'dashboard';
    let cv = bootNav.currentView;
    if (cv === 'question_list' || cv === 'study') {
      if (bootNav.taxSection) cv = 'tax_items';
      else if (bootNav.taxChapter) cv = 'tax_sections';
      else if (bootNav.taxSubSubject) cv = 'tax_chapters';
      else if (bootNav.taxSubject) cv = 'tax_sub_subjects';
      else if (bootNav.taxScope) cv = 'tax_subjects';
      else cv = 'dashboard';
    }
    return cv;
  })();

  const [viewMode, setViewMode] = useState(bootNav?.viewMode || 'exam'); // 'exam' | 'subject' | 'year' | 'chapter'
  const [currentView, setCurrentView] = useState(bootView);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [studyIdx, setStudyIdx] = useState(0); // 가이드 학습 모드 현재 문항 인덱스
  const [studyNonce, setStudyNonce] = useState(0); // 재학습 시 문항 카드 강제 리마운트
  const { progress, record: recordAnswer, reset: resetProgress, clearMany } = useProgress();
  // 복합 검색·필터 상태
  const [filters, setFilters] = useState(loadFilters);

  // taxonomy states
  const [taxSubject, setTaxSubject] = useState(bootNav?.taxSubject || null);
  const [taxSubSubject, setTaxSubSubject] = useState(bootNav?.taxSubSubject || null);
  const [taxChapter, setTaxChapter] = useState(bootNav?.taxChapter || null);
  const [taxSection, setTaxSection] = useState(bootNav?.taxSection || null);
  // 시험별/연도별 진입 시 적용되는 분류 스코프: null | {kind:'exam'|'year', value, label}
  const [taxScope, setTaxScope] = useState(bootNav?.taxScope || null);

  // 데이터 불러오기
  useEffect(() => {
    Promise.all([
      fetch('/data/questions_db.json').then(res => res.json()),
      fetch('/data/taxonomy.json').then(res => res.json())
    ])
      .then(([qData, tData]) => {
        setQuestionsData(qData);
        setTaxonomyData(tData);
        setLoading(false);
      })
      .catch(err => {
        console.error("데이터 로딩 실패:", err);
        setLoadError(true);
        setLoading(false);
      });
  }, []);

  // 가이드 학습: 키보드 ← 이전 / → · Enter 다음
  useEffect(() => {
    if (currentView !== 'study' || !selectedGroup) return;
    const onKey = (e) => {
      const tag = e.target && e.target.tagName;
      if (tag && /^(INPUT|TEXTAREA|SELECT)$/.test(tag)) return;
      if (e.key === 'ArrowLeft') {
        setStudyIdx(i => Math.max(0, i - 1)); window.scrollTo(0, 0);
      } else if (e.key === 'ArrowRight' || e.key === 'Enter') {
        const n = processedData.filter(selectedGroup.filterFn).length;
        setStudyIdx(i => Math.min(Math.max(0, n - 1), i + 1)); window.scrollTo(0, 0);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [currentView, selectedGroup, processedData]);

  // ----- URL 라우팅: 해시 ↔ 네비게이션 상태 동기 -----
  const hydratedRef = useRef(false);

  const applyNav = useCallback((n) => {
    if (!n) return;
    setViewMode(n.viewMode);
    setTaxScope(n.taxScope);
    setTaxSubject(n.taxSubject);
    setTaxSubSubject(n.taxSubSubject);
    setTaxChapter(n.taxChapter);
    setTaxSection(n.taxSection);
    setSelectedGroup(null);
    // 문제목록은 filterFn 직렬화가 불가 → 가장 가까운 상위 목록으로 복원
    let cv = n.currentView;
    if (cv === 'question_list' || cv === 'study') {
      if (n.taxSection) cv = 'tax_items';
      else if (n.taxChapter) cv = 'tax_sections';
      else if (n.taxSubSubject) cv = 'tax_chapters';
      else if (n.taxSubject) cv = 'tax_sub_subjects';
      else if (n.taxScope) cv = 'tax_subjects';
      else cv = 'dashboard';
    }
    setCurrentView(cv);
  }, []);

  // popstate(브라우저 뒤로/앞으로) 구독. 초기 상태는 이미 해시에서 복원됨.
  useEffect(() => {
    hydratedRef.current = true;
    const onPop = () => applyNav(parseNav(window.location.hash));
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, [applyNav]);

  // 네비게이션 상태 변경 → 해시 push (딥링크/뒤로가기 지원)
  useEffect(() => {
    if (!hydratedRef.current) return;
    const hash = serializeNav({ viewMode, currentView, taxScope, taxSubject, taxSubSubject, taxChapter, taxSection });
    if (hash !== window.location.hash) {
      window.history.pushState(null, '', hash);
    }
  }, [viewMode, currentView, taxScope, taxSubject, taxSubSubject, taxChapter, taxSection]);

  // 검색·필터 영속화: 변경 시 localStorage 저장 (새로고침 후 복원)
  useEffect(() => {
    try { localStorage.setItem(FILTERS_KEY, JSON.stringify(filters)); } catch { /* quota/SSR */ }
  }, [filters]);

  // Process data
  const processedData = useMemo(() => {
    if (loading || !questionsData) return [];
    return questionsData.map(q => {
      // V4 분류 정보: Gemini 또는 Claude로 분류되어 mapped_taxonomy가 있고
      // in_scope!==false 인 문제만 전 탭(시험/과목/단원/연도)에 노출.
      const iv = q.indexing_v4;
      const mt = iv && iv.mapped_taxonomy;
      const isClassified = !!(
        iv && mt && mt.subject &&
        (iv.processed_by === 'gemini-2.5-flash' || iv.processed_by === 'claude-sonnet-4-6') &&
        iv.in_scope !== false
      );

      return {
        ...q,
        year: q.year || '2025',
        exam: q.exam || '감정평가사',
        options: q.options || q.choices, // options / choices 통일
        // 실제 v4 난이도(1~5). 분류 전이면 null. 4 이상을 '취약'으로 간주.
        difficulty: (iv && typeof iv.difficulty === 'number') ? iv.difficulty : null,
        isWeak: !!(iv && typeof iv.difficulty === 'number' && iv.difficulty >= 4),
        // v4 mapped_taxonomy 기반 분류 필드 (모든 탭이 공유하는 단일 분류축)
        isClassified,
        taxSubjectName: isClassified ? mt.subject : null,
        taxSubSubjectName: isClassified ? (mt.sub_subject || null) : null,
        taxChapterName: isClassified ? (mt.chapter || null) : null,
        taxSectionName: isClassified ? (mt.section || null) : null,
        taxItemName: isClassified ? (mt.item || null) : null,
      };
    });
  }, [loading, questionsData]);

  // ===== 단일 v4 분류축 엔진 =====
  // 모든 탭(시험별/과목별/단원별/연도별)이 동일한 mapped_taxonomy 분류축을 공유한다.
  // taxScope: null(과목별/단원별) | {kind:'exam'|'year', value, label} (시험별/연도별 진입 시)
  const baseFilter = useCallback((item) => {
    if (!item.isClassified) return false;
    if (!taxScope) return true;
    if (taxScope.kind === 'exam') return item.exam === taxScope.value;
    if (taxScope.kind === 'year') return String(item.year) === String(taxScope.value);
    return true;
  }, [taxScope]);

  const scopedClassified = useMemo(
    () => processedData.filter(baseFilter),
    [processedData, baseFilter]
  );

  // Level 0: 연도 목록 (연도별 탭) — 분류 완료 문항만 집계
  const yearGroups = useMemo(() => {
    const groups = {};
    processedData.forEach(q => {
      if (!q.isClassified) return;
      const key = q.year;
      if (!groups[key]) {
        groups[key] = {
          type: 'year_group',
          title: `${q.year}년`,
          subtitle: '기출연도',
          total: 0,
          weak: false,
          tag: '기출',
          rawValue: q.year
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    return Object.values(groups).sort((a, b) => parseInt(b.rawValue) - parseInt(a.rawValue));
  }, [processedData]);

  // Level 0: 시험 목록 (시험별 탭) — 분류 완료 문항만 집계
  const examGroups = useMemo(() => {
    const groups = {};
    processedData.forEach(q => {
      if (!q.isClassified) return;
      const key = q.exam;
      if (!groups[key]) {
        groups[key] = {
          type: 'exam',
          title: q.exam,
          subtitle: '자격시험',
          total: 0,
          weak: false,
          tag: '기출문제'
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    return Object.values(groups).sort((a, b) => b.total - a.total);
  }, [processedData]);

  // 과목(taxonomy subject) 목록 — 시험별/과목별/단원별/연도별 공용 (scope 반영)
  const taxSubjectGroups = useMemo(() => {
    if (!taxonomyData) return [];
    return Object.keys(taxonomyData).map(subj => {
      const filtered = scopedClassified.filter(q => q.taxSubjectName === subj);
      return {
        type: 'tax_subject',
        title: subj,
        subtitle: taxScope ? taxScope.label : '단원별 학습',
        total: filtered.length,
        weak: filtered.some(q => q.isWeak),
        tag: '과목'
      };
    }).filter(g => g.total > 0);
  }, [taxonomyData, scopedClassified, taxScope]);

  // 세부과목 또는 장(Chapter) 목록 (scope 반영)
  const taxSubSubjectGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject) return [];
    const subjData = taxonomyData[taxSubject];
    const filtered = scopedClassified.filter(q => q.taxSubjectName === taxSubject);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSubject} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject
    });

    if (subjData.has_subjects) {
      Object.keys(subjData.subjects).forEach(subSubj => {
        const sub = filtered.filter(q => q.taxSubSubjectName === subSubj);
        if (sub.length === 0) return;
        groups.push({
          type: 'tax_sub_subject',
          title: subSubj,
          subtitle: taxSubject,
          total: sub.length,
          weak: sub.some(q => q.isWeak),
          tag: '세부과목'
        });
      });
    } else {
      subjData.chapters.forEach(ch => {
        const chFiltered = filtered.filter(q => q.taxChapterName === ch.name);
        if (chFiltered.length === 0) return;
        groups.push({
          type: 'tax_chapter',
          title: ch.name,
          subtitle: taxSubject,
          total: chFiltered.length,
          weak: chFiltered.some(q => q.isWeak),
          tag: 'PART/장',
          filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxChapterName === ch.name
        });
      });
    }
    return groups;
  }, [taxonomyData, taxSubject, scopedClassified, baseFilter]);

  // 장(Chapter) 목록 (세부과목이 있는 경우, scope 반영)
  const taxChapterGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxSubSubject) return [];
    const subjData = taxonomyData[taxSubject];
    const chapters = subjData.subjects[taxSubSubject] || [];
    const filtered = scopedClassified.filter(q =>
      q.taxSubjectName === taxSubject && q.taxSubSubjectName === taxSubSubject);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSubSubject} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSubSubjectName === taxSubSubject
    });
    chapters.forEach(ch => {
      const chFiltered = filtered.filter(q => q.taxChapterName === ch.name);
      if (chFiltered.length === 0) return;
      groups.push({
        type: 'tax_chapter',
        title: ch.name,
        subtitle: taxSubSubject,
        total: chFiltered.length,
        weak: chFiltered.some(q => q.isWeak),
        tag: 'PART/장',
        filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxChapterName === ch.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, scopedClassified, baseFilter]);

  // 절(Section) 목록 — 절은 클릭 시 관(item) 목록으로 진입 (scope 반영)
  const taxSectionGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxChapter) return [];
    const subjData = taxonomyData[taxSubject];
    let chapters = [];
    if (subjData.has_subjects && taxSubSubject) {
      chapters = subjData.subjects[taxSubSubject];
    } else if (!subjData.has_subjects) {
      chapters = subjData.chapters;
    }
    const chapterData = chapters.find(c => c.name === taxChapter);
    if (!chapterData || !chapterData.sections) return [];

    const filtered = scopedClassified.filter(q =>
      q.taxSubjectName === taxSubject && q.taxChapterName === taxChapter);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxChapter} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxChapterName === taxChapter
    });

    chapterData.sections.forEach(sec => {
      const secQs = filtered.filter(q => q.taxSectionName === sec.name);
      if (secQs.length === 0) return;
      const hasItems = (sec.items || []).some(it =>
        secQs.some(q => q.taxItemName === it.name));
      groups.push({
        // 관(item) 단위 분류가 있으면 진입형(tax_section), 없으면 바로 풀기(play_all_tax)
        type: hasItems ? 'tax_section' : 'play_all_tax',
        title: sec.name,
        subtitle: taxChapter,
        total: secQs.length,
        weak: secQs.some(q => q.isWeak),
        tag: '절',
        filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSectionName === sec.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, taxChapter, scopedClassified, baseFilter]);

  // 관(item) 목록 — 최저 분류 단위 (scope 반영)
  const taxItemGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxChapter || !taxSection) return [];
    const subjData = taxonomyData[taxSubject];
    let chapters = [];
    if (subjData.has_subjects && taxSubSubject) {
      chapters = subjData.subjects[taxSubSubject];
    } else if (!subjData.has_subjects) {
      chapters = subjData.chapters;
    }
    const chapterData = chapters.find(c => c.name === taxChapter);
    const sectionData = chapterData && (chapterData.sections || []).find(s => s.name === taxSection);
    if (!sectionData) return [];

    const filtered = scopedClassified.filter(q =>
      q.taxSubjectName === taxSubject && q.taxSectionName === taxSection);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSection} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: filtered.some(q => q.isWeak),
      tag: '전체',
      filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSectionName === taxSection
    });

    (sectionData.items || []).forEach(it => {
      const itQs = filtered.filter(q => q.taxItemName === it.name);
      if (itQs.length === 0) return;
      groups.push({
        type: 'play_all_tax',
        title: it.name,
        subtitle: taxSection,
        total: itQs.length,
        weak: itQs.some(q => q.isWeak),
        tag: '관',
        filterFn: (item) => baseFilter(item) && item.taxSubjectName === taxSubject && item.taxSectionName === taxSection && item.taxItemName === it.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, taxChapter, taxSection, scopedClassified, baseFilter]);

  // 4개 탭 모두 동일 v4 분류축 사용. 시험별/연도별은 picker → 스코프 설정 후 동일 엔진.
  let activeGroups = [];
  if (viewMode === 'subject' || viewMode === 'chapter') activeGroups = taxSubjectGroups;
  else if (viewMode === 'year') activeGroups = yearGroups;
  else if (viewMode === 'exam') activeGroups = examGroups;

  const classifiedList = useMemo(
    () => processedData.filter(q => q.isClassified),
    [processedData]
  );

  // 복합 필터 선택지
  const filterOptions = useMemo(() => {
    const exams = new Set(), subjects = new Set(), years = new Set();
    for (const q of classifiedList) {
      exams.add(q.exam);
      if (q.taxSubjectName) subjects.add(q.taxSubjectName);
      years.add(String(q.year));
    }
    return {
      exams: [...exams].sort(),
      subjects: [...subjects].sort(),
      years: [...years].sort((a, b) => Number(b) - Number(a)),
      diffs: [1, 2, 3, 4, 5],
    };
  }, [classifiedList]);

  // 복합 필터 결과 (AND 결합, 키워드는 문제/보기/해설 OR 매칭)
  const filteredResults = useMemo(() => {
    const { exams, subjects, years, diffs, kw } = filters;
    const active = exams.length || subjects.length || years.length || diffs.length || kw.trim();
    if (!active) return [];
    const k = kw.trim().toLowerCase();
    return classifiedList.filter(q => {
      if (exams.length && !exams.includes(q.exam)) return false;
      if (subjects.length && !subjects.includes(q.taxSubjectName)) return false;
      if (years.length && !years.includes(String(q.year))) return false;
      if (diffs.length && !diffs.includes(q.difficulty)) return false;
      if (k) {
        const hay = `${q.question || ''} ${(q.options || []).join(' ')} ${q.explanation || ''}`.toLowerCase();
        if (!hay.includes(k)) return false;
      }
      return true;
    });
  }, [classifiedList, filters]);

  const toggleFilter = (key, val) => setFilters(f => {
    const arr = f[key];
    return { ...f, [key]: arr.includes(val) ? arr.filter(x => x !== val) : [...arr, val] };
  });
  const clearFilters = () => setFilters({ ...EMPTY_FILTERS });
  const totalQuestions = classifiedList.length;
  const overall = useMemo(
    () => progressStats(classifiedList, progress),
    [classifiedList, progress]
  );

  // 카드 한 장이 대표하는 문항 집합 (filterFn 없으면 타입별 추론)
  const cardQuestions = (group) => {
    if (group.filterFn) return processedData.filter(group.filterFn);
    if (group.type === 'exam') return classifiedList.filter(q => q.exam === group.title);
    if (group.type === 'year_group') return classifiedList.filter(q => String(q.year) === String(group.rawValue));
    if (group.type === 'tax_subject') return scopedClassified.filter(q => q.taxSubjectName === group.title);
    if (group.type === 'tax_sub_subject') return scopedClassified.filter(q => q.taxSubjectName === taxSubject && q.taxSubSubjectName === group.title);
    return [];
  };

  const enterTaxScope = (scope) => {
    setTaxScope(scope);
    setTaxSubject(null);
    setTaxSubSubject(null);
    setTaxChapter(null);
    setTaxSection(null);
    setCurrentView('tax_subjects');
    window.scrollTo(0, 0);
  };

  const handleGroupClick = (group) => {
    if (group.type === 'exam') {
      enterTaxScope({ kind: 'exam', value: group.title, label: group.title });
    } else if (group.type === 'year_group') {
      enterTaxScope({ kind: 'year', value: group.rawValue, label: `${group.rawValue}년` });
    } else if (group.type === 'tax_subject') {
      setTaxSubject(group.title);
      setCurrentView('tax_sub_subjects');
      window.scrollTo(0, 0);
    } else if (group.type === 'tax_sub_subject') {
      setTaxSubSubject(group.title);
      setCurrentView('tax_chapters');
      window.scrollTo(0, 0);
    } else if (group.type === 'tax_chapter') {
      setTaxChapter(group.title);
      setCurrentView('tax_sections');
      window.scrollTo(0, 0);
    } else if (group.type === 'tax_section') {
      setTaxSection(group.title);
      setCurrentView('tax_items');
      window.scrollTo(0, 0);
    } else {
      setSelectedGroup(group);
      setStudyIdx(0);
      setCurrentView('study');
      window.scrollTo(0, 0);
    }
  };

  const handleBack = () => {
    if (currentView === 'question_list' || currentView === 'study') {
      // play_all_tax: 진입했던 가장 깊은 tax 레벨로 복귀
      if (taxSection) setCurrentView('tax_items');
      else if (taxChapter) setCurrentView('tax_sections');
      else if (taxSubSubject) setCurrentView('tax_chapters');
      else if (taxSubject) setCurrentView('tax_sub_subjects');
      else if (taxScope) setCurrentView('tax_subjects');
      else setCurrentView('dashboard');
      setSelectedGroup(null);
    } else if (currentView === 'tax_items') {
      setCurrentView('tax_sections');
      setTaxSection(null);
    } else if (currentView === 'tax_sections') {
      setCurrentView('tax_chapters');
      setTaxChapter(null);
    } else if (currentView === 'tax_chapters') {
      setCurrentView('tax_sub_subjects');
      setTaxSubSubject(null);
    } else if (currentView === 'tax_sub_subjects') {
      setCurrentView(taxScope ? 'tax_subjects' : 'dashboard');
      setTaxSubject(null);
    } else if (currentView === 'tax_subjects') {
      setCurrentView('dashboard');
      setTaxScope(null);
    } else {
      setCurrentView('dashboard');
    }
  };

  // 탭 전환: 모든 드릴다운 상태를 초기화하고 대시보드로
  const switchTab = (mode) => {
    setViewMode(mode);
    setCurrentView('dashboard');
    setTaxScope(null);
    setTaxSubject(null);
    setTaxSubSubject(null);
    setTaxChapter(null);
    setTaxSection(null);
    setSelectedGroup(null);
    window.scrollTo(0, 0);
  };

  // 가이드 학습 모드: 한 개념의 문제를 난이도↑ 순으로 한 문제씩, 해설로 누적 학습
  if (currentView === 'study' && selectedGroup) {
    const ordered = processedData
      .filter(selectedGroup.filterFn)
      .sort((a, b) => {
        const da = a.difficulty ?? 99, db = b.difficulty ?? 99;
        if (da !== db) return da - db;                 // 쉬운 문제부터
        const ya = parseInt(a.year, 10), yb = parseInt(b.year, 10);
        if (ya !== yb) return yb - ya;                  // 같은 난이도면 최신 연도
        return parseInt(a.number, 10) - parseInt(b.number, 10);
      });
    const total = ordered.length;
    const idx = Math.min(studyIdx, Math.max(0, total - 1));
    const q = ordered[idx];
    const s = progressStats(ordered, progress);
    const pathParts = q ? [q.taxSubjectName, q.taxSubSubjectName, q.taxChapterName, q.taxSectionName, q.taxItemName].filter(Boolean) : [];
    const done = total > 0 && s.answered >= total;
    return (
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', display: 'flex', justifyContent: 'space-between' }}>
          <button className="back-btn" onClick={handleBack}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>뒤로가기</span>
          </button>
          <button onClick={() => setCurrentView('question_list')}
            style={{ border: 'none', background: 'transparent', color: '#3b82f6', fontWeight: 600, cursor: 'pointer', padding: '0 16px' }}>
            전체 목록 ▦
          </button>
        </header>

        <div style={{ padding: '20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <div style={{ fontSize: '0.8rem', color: '#6b7280' }}>{selectedGroup.title}</div>
          {pathParts.length > 0 && (
            <div style={{ fontSize: '0.85rem', color: '#374151', margin: '6px 0', fontWeight: 600 }}>
              {pathParts.join(' ▸ ')}
            </div>
          )}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '8px' }}>
            <div style={{ flex: 1, height: '8px', background: '#e5e7eb', borderRadius: '999px', overflow: 'hidden' }}>
              <div style={{ width: `${total ? Math.round((s.answered / total) * 100) : 0}%`, height: '100%', background: '#3b82f6', transition: 'width .3s' }} />
            </div>
            <span style={{ fontSize: '0.8rem', color: '#6b7280', whiteSpace: 'nowrap' }}>
              {idx + 1} / {total} · 정답 <b style={{ color: '#16a34a' }}>{s.correct}</b>
            </span>
          </div>
        </div>

        <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
          {q ? (
            <>
              <QuestionItem key={`${qid(q)}-${studyNonce}`} q={q} prior={progress[qid(q)]} onAnswer={recordAnswer} />
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', marginTop: '8px' }}>
                <button
                  onClick={() => { setStudyIdx(Math.max(0, idx - 1)); window.scrollTo(0, 0); }}
                  disabled={idx === 0}
                  style={{ flex: 1, padding: '14px', minHeight: '48px', borderRadius: '10px', border: '1px solid #d1d5db', background: '#fff', cursor: idx === 0 ? 'default' : 'pointer', color: idx === 0 ? '#d1d5db' : '#374151', fontWeight: 600 }}
                >← 이전</button>
                <button
                  onClick={() => { setStudyIdx(Math.min(total - 1, idx + 1)); window.scrollTo(0, 0); }}
                  disabled={idx >= total - 1}
                  style={{ flex: 2, padding: '14px', minHeight: '48px', borderRadius: '10px', border: 'none', background: idx >= total - 1 ? '#e5e7eb' : '#3b82f6', color: idx >= total - 1 ? '#9ca3af' : '#fff', cursor: idx >= total - 1 ? 'default' : 'pointer', fontWeight: 700 }}
                >다음 문제 →</button>
              </div>
              <div style={{ textAlign: 'center', fontSize: '0.75rem', color: '#9ca3af', marginTop: '8px' }}>
                키보드 <b>←</b> 이전 · <b>→</b> 또는 <b>Enter</b> 다음
              </div>
              {done && (
                <div style={{ marginTop: '20px', padding: '20px', background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '12px', textAlign: 'center' }}>
                  <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: '6px' }}>이 개념 학습 완료 🎉</div>
                  <div style={{ color: '#374151', marginBottom: '14px' }}>
                    {total}문제 중 정답 <b style={{ color: '#16a34a' }}>{s.correct}</b> · 오답 <b style={{ color: '#dc2626' }}>{s.answered - s.correct}</b>
                  </div>
                  <button onClick={() => {
                      clearMany(ordered.map(qid));   // 이 개념 진행 초기화 → 재측정
                      setStudyIdx(0);
                      setStudyNonce(n => n + 1);      // 카드 강제 리마운트(이전 응답 표시 제거)
                      window.scrollTo(0, 0);
                    }}
                    style={{ padding: '12px 20px', borderRadius: '10px', border: 'none', background: '#3b82f6', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>
                    처음부터 다시 풀기
                  </button>
                </div>
              )}
            </>
          ) : (
            <div style={{ textAlign: 'center', color: '#6b7280', padding: '40px' }}>문제가 없습니다.</div>
          )}
        </main>
      </div>
    );
  }

  if (currentView === 'question_list' && selectedGroup) {
    // 필터링된 문제를 연도 내림차순, 문제 번호 오름차순으로 정렬
    const filteredQuestions = processedData
      .filter(selectedGroup.filterFn)
      .sort((a, b) => {
        const yearA = parseInt(a.year, 10);
        const yearB = parseInt(b.year, 10);
        if (yearA !== yearB) return yearB - yearA; // 연도 내림차순
        return parseInt(a.number, 10) - parseInt(b.number, 10); // 번호 오름차순
      });
    
    return (
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb', display: 'flex', justifyContent: 'space-between' }}>
          <button className="back-btn" onClick={handleBack}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>뒤로가기</span>
          </button>
          <button onClick={() => { setStudyIdx(0); setCurrentView('study'); window.scrollTo(0, 0); }}
            style={{ border: 'none', background: 'transparent', color: '#3b82f6', fontWeight: 600, cursor: 'pointer', padding: '0 16px' }}>
            📚 가이드 학습
          </button>
        </header>

        <div style={{ padding: '24px 20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '4px' }}>{selectedGroup.subtitle}</div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: '700' }}>{selectedGroup.title} ({filteredQuestions.length}문제)</h1>
          {(() => {
            const s = progressStats(filteredQuestions, progress);
            const pct = s.total ? Math.round((s.answered / s.total) * 100) : 0;
            return (
              <div style={{ marginTop: '12px' }}>
                <div style={{ height: '8px', background: '#e5e7eb', borderRadius: '999px', overflow: 'hidden' }}>
                  <div style={{ width: `${pct}%`, height: '100%', background: '#3b82f6', transition: 'width .3s' }} />
                </div>
                <div style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: '6px' }}>
                  푼 문제 <b>{s.answered}/{s.total}</b> · 정답 <b style={{ color: '#16a34a' }}>{s.correct}</b>
                </div>
              </div>
            );
          })()}
        </div>

        <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
          {filteredQuestions.map((q) => (
            <QuestionItem
              key={qid(q)}
              q={q}
              prior={progress[qid(q)]}
              onAnswer={recordAnswer}
            />
          ))}
        </main>
      </div>
    );
  }


  const renderStudyGrid = (title, subtitle, groups) => (
    <div className="app-container">
      <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
        <button className="back-btn" onClick={handleBack}>
          <ArrowLeft size={24} style={{ marginRight: '8px' }} />
          <span style={{ fontSize: '1rem', fontWeight: '600' }}>뒤로가기</span>
        </button>
      </header>
      
      <div style={{ padding: '24px 20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '4px' }}>{subtitle}</div>
        <h1 style={{ fontSize: '1.5rem', fontWeight: '700' }}>{title}</h1>
      </div>
      
      <main className="main-content" style={{ marginTop: '20px' }}>
        <div className="study-grid">
          {groups.map((group, idx) => {
            const isAll = group.type && group.type.startsWith('play_all');
            const s = progressStats(cardQuestions(group), progress);
            const pct = s.total ? Math.round((s.answered / s.total) * 100) : 0;
            const dm = s.level ? (DIFFICULTY_META[s.level] || null) : null;
            return (
              <div key={idx} className="study-card" onClick={() => handleGroupClick(group)} style={isAll ? { background: '#eff6ff', borderColor: '#bfdbfe' } : {}}>
                <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                  <div className="card-badge" style={isAll ? { background: '#3b82f6', color: '#fff', border: 'none' } : {}}>{group.tag}</div>
                  {dm && (
                    <span style={{ fontSize: '0.72rem', fontWeight: 700, padding: '2px 8px', borderRadius: '999px', background: dm.bg, color: dm.fg }}>
                      난이도 {s.avgDiff.toFixed(1)}
                    </span>
                  )}
                </div>
                <div className="card-subtitle">{group.subtitle}</div>
                <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{group.title}</h3>
                <div className="card-total">총 {group.total} 문제 {s.answered > 0 && <span style={{ color: 'var(--primary)', fontWeight: 700 }}>· {pct}%</span>}</div>
                <div className="card-progress-container">
                  <div className="card-progress-fill" style={{ width: `${pct}%` }}></div>
                </div>
                <div className="play-btn" style={isAll ? { background: '#3b82f6', color: '#fff' } : {}}>선택</div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );

  // ===== 단일 v4 분류축 뷰 (시험별/과목별/단원별/연도별 공용) =====
  const scopePrefix = taxScope ? `${taxScope.label} · ` : '';
  if (currentView === 'tax_subjects') return renderStudyGrid(taxScope ? taxScope.label : '과목 선택', taxScope ? `${taxScope.label} 과목별` : '단원별 학습', taxSubjectGroups);
  if (currentView === 'tax_sub_subjects' && taxSubject) return renderStudyGrid(`${scopePrefix}${taxSubject}`, '세부과목 / 장 선택', taxSubSubjectGroups);
  if (currentView === 'tax_chapters' && taxSubSubject) return renderStudyGrid(`${scopePrefix}${taxSubSubject}`, '장(Chapter) 선택', taxChapterGroups);
  if (currentView === 'tax_sections' && taxChapter) return renderStudyGrid(`${scopePrefix}${taxChapter}`, '절(Section) 선택', taxSectionGroups);
  if (currentView === 'tax_items' && taxSection) return renderStudyGrid(`${scopePrefix}${taxSection}`, '관(Item) 선택', taxItemGroups);

  // Dashboard View

  if (loading) {
    return (
      <div style={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#f8fafc',
        color: '#3b82f6'
      }}>
        <Loader2 size={48} className="animate-spin" style={{ marginBottom: '16px' }} />
        <div style={{ fontWeight: '700', fontSize: '1.25rem' }}>데이터를 불러오는 중입니다...</div>
      </div>
    );
  }

  if (loadError) {
    return (
      <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#f8fafc', color: '#374151', padding: '24px', textAlign: 'center' }}>
        <div style={{ fontWeight: 700, fontSize: '1.2rem', marginBottom: '8px' }}>데이터를 불러오지 못했습니다</div>
        <div style={{ color: '#6b7280', marginBottom: '20px' }}>네트워크 상태를 확인한 뒤 다시 시도해 주세요.</div>
        <button onClick={() => window.location.reload()}
          style={{ padding: '12px 22px', borderRadius: '10px', border: 'none', background: '#3b82f6', color: '#fff', fontWeight: 700, cursor: 'pointer' }}>
          다시 시도
        </button>
      </div>
    );
  }

  if (totalQuestions === 0) {
    return (
      <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#f8fafc', color: '#6b7280', padding: '24px', textAlign: 'center' }}>
        <div style={{ fontWeight: 700, fontSize: '1.2rem', color: '#374151', marginBottom: '8px' }}>표시할 분류된 문제가 없습니다</div>
        <div>데이터가 비어 있거나 분류가 아직 반영되지 않았습니다.</div>
      </div>
    );
  }

  if (currentView === 'search') {
    const activeCount = filters.exams.length + filters.subjects.length + filters.years.length + filters.diffs.length + (filters.kw.trim() ? 1 : 0);
    const shown = filteredResults.slice(0, 200);
    const chip = (on) => ({
      padding: '6px 12px', borderRadius: '999px', fontSize: '0.85rem', cursor: 'pointer',
      border: on ? '1px solid #3b82f6' : '1px solid #d1d5db',
      background: on ? '#3b82f6' : '#fff', color: on ? '#fff' : '#374151',
    });
    const groupChips = (label, items, sel, k, fmt) => (
      <div style={{ marginBottom: '14px' }}>
        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#6b7280', marginBottom: '6px' }}>{label}</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          {items.map(it => (
            <span key={String(it)} style={chip(sel.includes(it))} onClick={() => toggleFilter(k, it)}>
              {fmt ? fmt(it) : it}
            </span>
          ))}
        </div>
      </div>
    );
    return (
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={() => setCurrentView('dashboard')}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>뒤로가기</span>
          </button>
        </header>
        <div style={{ padding: '20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <input
            value={filters.kw}
            onChange={(e) => setFilters(f => ({ ...f, kw: e.target.value }))}
            placeholder="문제·보기·해설 키워드 검색"
            style={{ width: '100%', padding: '12px 14px', fontSize: '1rem', border: '1px solid #d1d5db', borderRadius: '10px', marginBottom: '16px', boxSizing: 'border-box' }}
          />
          {groupChips('시험', filterOptions.exams, filters.exams, 'exams')}
          {groupChips('과목', filterOptions.subjects, filters.subjects, 'subjects')}
          {groupChips('연도', filterOptions.years, filters.years, 'years', (y) => `${y}년`)}
          {groupChips('난이도', filterOptions.diffs, filters.diffs, 'diffs', (d) => `난이도 ${d}`)}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '6px' }}>
            <span style={{ fontWeight: 700 }}>{activeCount ? `${filteredResults.length}문제` : '필터를 선택하세요'}</span>
            {activeCount > 0 && (
              <button onClick={clearFilters} style={{ border: 'none', background: '#f3f4f6', padding: '6px 12px', borderRadius: '8px', cursor: 'pointer', fontSize: '0.85rem' }}>필터 초기화</button>
            )}
          </div>
        </div>
        <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
          {shown.map(q => (
            <QuestionItem key={qid(q)} q={q} prior={progress[qid(q)]} onAnswer={recordAnswer} />
          ))}
          {filteredResults.length > shown.length && (
            <div style={{ textAlign: 'center', color: '#6b7280', padding: '16px' }}>
              상위 {shown.length}개만 표시 중 (총 {filteredResults.length}개) — 필터를 좁혀주세요
            </div>
          )}
        </main>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="top-nav">
        <button className="back-btn">
          <ChevronLeft size={24} />
        </button>
      </header>

      <div className="banner">
        <div className="banner-content">
          <div className="banner-subtitle">PROFESSIONAL APPRAISER EXAM</div>
          <div className="banner-title">감정평가사 1차 기출 완전정복</div>
          <p style={{ marginTop: '12px', opacity: 0.8, fontSize: '1rem', fontWeight: '500' }}>
            합격을 위한 최단기 기출 반복 학습 솔루션
          </p>
        </div>
      </div>

      <main className="main-content">
        <section className="overview-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <h2 className="overview-title">나의 학습 통계</h2>
              <p className="overview-subtitle">전체 {totalQuestions}개 문항 중 현재 학습 진행 현황</p>
            </div>
            {overall.answered > 0 && (
              <button
                onClick={() => { if (window.confirm('학습 진행률을 모두 초기화할까요?')) resetProgress(); }}
                style={{ background: 'var(--primary-light)', padding: '8px 16px', borderRadius: '12px', color: 'var(--primary)', fontWeight: '700', fontSize: '0.9rem', border: 'none', cursor: 'pointer' }}
              >
                진행률 초기화
              </button>
            )}
          </div>

          {(() => {
            const pct = totalQuestions ? Math.round((overall.answered / totalQuestions) * 100) : 0;
            const acc = overall.answered ? Math.round((overall.correct / overall.answered) * 100) : 0;
            return (
              <>
                <div className="progress-bar-container">
                  <div className="progress-bar-fill" style={{ width: `${pct}%` }}></div>
                </div>
                <div className="progress-stats">
                  <div>
                    <span className="stat-dot"></span>
                    학습한 문제 <span className="stat-bold">{overall.answered}/{totalQuestions}</span>
                    {overall.answered > 0 && <> · 정답률 <span className="stat-bold" style={{ color: '#16a34a' }}>{acc}%</span></>}
                  </div>
                  <div>{pct}%</div>
                </div>
              </>
            );
          })()}
        </section>

        <button
          onClick={() => setCurrentView('search')}
          style={{ width: '100%', textAlign: 'left', padding: '14px 16px', margin: '4px 0 20px', border: '1px solid #d1d5db', borderRadius: '12px', background: '#fff', color: '#6b7280', fontSize: '0.95rem', cursor: 'pointer' }}
        >
          🔍 통합 검색·필터 (시험·과목·연도·난이도·키워드)
        </button>

        <div className="section-header">
          <h3 className="section-title">학습 목록</h3>
          <div className="view-toggle">
            {[['exam','시험별'],['subject','과목별'],['chapter','단원별'],['year','연도별']].map(([mode,label]) => (
              <button
                key={mode}
                className={viewMode === mode ? 'active' : ''}
                onClick={() => switchTab(mode)}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <div className="study-grid">
          {activeGroups.map((group, idx) => {
            const s = progressStats(cardQuestions(group), progress);
            const pct = s.total ? Math.round((s.answered / s.total) * 100) : 0;
            const dm = s.level ? (DIFFICULTY_META[s.level] || null) : null;
            return (
            <div key={idx} className="study-card" onClick={() => handleGroupClick(group)}>
              {dm ? (
                <div className="card-badge" style={{ background: dm.bg, color: dm.fg, border: 'none' }}>
                  난이도 {s.avgDiff.toFixed(1)}
                </div>
              ) : (
                <div className="card-badge">기본</div>
              )}

              <div className="card-subtitle">{group.subtitle}</div>
              <h3 className="card-title">{group.title}</h3>
              <div className="card-total">총 {group.total} 문제 · 평균 {s.avgDiff ? s.avgDiff.toFixed(1) : '-'}</div>

              <div className="card-tag">{group.tag}</div>

              <div className="card-progress-container">
                <div className="card-progress-fill" style={{ width: `${pct}%` }}></div>
              </div>

              <div className="progress-stats" style={{ marginBottom: '0' }}>
                <span>학습한 문제 <span className="stat-bold">{s.answered}/{s.total}</span></span>
                <span style={{ color: 'var(--primary)', fontWeight: '700' }}>{pct}%</span>
              </div>

              <div className="play-btn">Q</div>
            </div>
            );
          })}
        </div>
      </main>
    </div>
  );
};

export default App;
