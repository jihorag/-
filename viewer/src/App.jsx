import { useState, useMemo, useEffect, useCallback } from 'react';
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

// Component to parse and render text with inline images and math
const ParsedText = ({ text }) => {
  if (!text) return null;
  const parts = text.split(/(\[IMAGE:\s*.*?\])/g);
  return (
    <>
      {parts.map((part, i) => {
        const imgMatch = part.match(/\[IMAGE:\s*(.*?)\]/);
        if (imgMatch) {
          const imageName = imgMatch[1].split('/').pop();
          return (
            <img 
              key={i} 
              src={`/images/${imageName}`}
              alt="content" 
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
const QuestionItem = ({ q }) => {
  const [selectedOpt, setSelectedOpt] = useState(null);
  const isRevealed = selectedOpt !== null;

  const handleOptionClick = (optIdx) => {
    if (isRevealed) return; // Prevent changing answer after revealed
    setSelectedOpt(String(optIdx + 1));
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
  const [viewMode, setViewMode] = useState('exam'); // 'exam' | 'subject' | 'year' | 'chapter'
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedGroup, setSelectedGroup] = useState(null);

  // taxonomy states
  const [taxSubject, setTaxSubject] = useState(null);
  const [taxSubSubject, setTaxSubSubject] = useState(null);
  const [taxChapter, setTaxChapter] = useState(null);
  const [taxSection, setTaxSection] = useState(null);
  // 시험별/연도별 진입 시 적용되는 분류 스코프: null | {kind:'exam'|'year', value, label}
  const [taxScope, setTaxScope] = useState(null);

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
        setLoading(false);
      });
  }, []);

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

  const totalQuestions = useMemo(
    () => processedData.filter(q => q.isClassified).length,
    [processedData]
  );

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
      setCurrentView('question_list');
      window.scrollTo(0, 0);
    }
  };

  const handleBack = () => {
    if (currentView === 'question_list') {
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
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={handleBack}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>뒤로가기</span>
          </button>
        </header>
        
        <div style={{ padding: '24px 20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '4px' }}>{selectedGroup.subtitle}</div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: '700' }}>{selectedGroup.title} ({filteredQuestions.length}문제)</h1>
        </div>
        
        <main style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
          {filteredQuestions.map((q, idx) => (
            <QuestionItem key={idx} q={q} />
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
            return (
              <div key={idx} className="study-card" onClick={() => handleGroupClick(group)} style={isAll ? { background: '#eff6ff', borderColor: '#bfdbfe' } : {}}>
                <div className="card-badge" style={isAll ? { background: '#3b82f6', color: '#fff', border: 'none' } : {}}>{group.tag}</div>
                <div className="card-subtitle">{group.subtitle}</div>
                <h3 className="card-title" style={{ fontSize: '1.1rem' }}>{group.title}</h3>
                <div className="card-total">총 {group.total} 문제</div>
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
            <div style={{ background: 'var(--primary-light)', padding: '8px 16px', borderRadius: '12px', color: 'var(--primary)', fontWeight: '700', fontSize: '0.9rem' }}>
              D-DAY 준비 중
            </div>
          </div>
          
          <div className="progress-bar-container">
            <div className="progress-bar-fill" style={{ width: '0%' }}></div>
          </div>
          
          <div className="progress-stats">
            <div>
              <span className="stat-dot"></span>
              학습한 콘텐츠 <span className="stat-bold">0/{totalQuestions}</span>
            </div>
            <div>0%</div>
          </div>
          
          <button className="btn-primary">모든 문제 풀기</button>
        </section>

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
          {activeGroups.map((group, idx) => (
            <div key={idx} className="study-card" onClick={() => handleGroupClick(group)}>
              {group.weak ? (
                <div className="card-badge weak">취약</div>
              ) : (
                <div className="card-badge">기본</div>
              )}
              
              <div className="card-subtitle">{group.subtitle}</div>
              <h3 className="card-title">{group.title}</h3>
              <div className="card-total">총 {group.total} 문제</div>
              
              <div className="card-tag">{group.tag}</div>
              
              <div className="card-progress-container">
                <div className="card-progress-fill" style={{ width: '0%' }}></div>
              </div>
              
              <div className="progress-stats" style={{ marginBottom: '0' }}>
                <span>학습한 문제 <span className="stat-bold">0/{group.total}</span></span>
                <span style={{ color: 'var(--primary)', fontWeight: '700' }}>0%</span>
              </div>
              
              <div className="play-btn">Q</div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default App;
