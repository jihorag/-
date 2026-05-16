import React, { useState, useMemo, useEffect } from 'react';
import { ChevronLeft, ArrowLeft, Loader2 } from 'lucide-react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

// Helper to deduce subject from question number
const getSubject = (numStr, period, exam) => {
  const num = parseInt(numStr, 10);
  if (exam === '공인중개사') {
    if (period === 'g1') {
      if (num <= 40) return '부동산학개론';
      return '민법 및 민사특별법';
    } else if (period === 'g2') {
      if (num <= 40) return '중개사법';
      if (num <= 80) return '부동산공법';
      return '공시세법';
    }
  }

  if (exam === '주택관리사' || period === 'cc') {
    if (num <= 40) return '민법(주택)';
    return '회계원리(주택)';
  }

  if (exam === '변리사' || period === 'hk') {
    return '민법(변리사)';
  }

  if (exam === '가맹거래사' || period === 'rp') {
    return '민법(가맹)';
  }

  if (exam === '공인노무사') {
    if (period === 'cgg' || period === 'cfp') return '민법(노무사)';
    if (period === 'cgi' || period === 'cfr') return '경제학(노무사)';
  }

  if (exam === '행정사') {
    return '민법(행정)';
  }
  
  if (exam === '관세사') {
    return '회계학(관세사)';
  }

  if (exam === '9급 국가직 공무원') {
    return '경제학원론(공무원)';
  }

  if (exam === '세무사') {
    return '재정학';
  }
  
  if (period === '1') {
    if (num <= 40) return '민법';
    if (num <= 80) return '경제학원론';
    return '부동산학원론';
  } else if (period === '1_old') {
    if (num <= 40) return '민법';
    return '경제학원론';
  } else {
    // period === '2'
    if (num <= 40) return '감정평가관계법규';
    return '회계학';
  }
};

// Mocking unit for demonstration until LLM tags are added
const getMockUnit = (numStr) => {
  const num = parseInt(numStr, 10);
  const ch = Math.ceil((num % 40 || 40) / 10); // 10 questions per chapter
  return `제${ch}장`;
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
            } catch (e) {
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
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
        <span style={{ fontWeight: '700', fontSize: '1.125rem', color: '#2563eb' }}>Q. {q.number}</span>
        <span style={{ fontSize: '0.875rem', color: '#9ca3af' }}>
          ({q.year}) {q.exam} {q.year}년 {q.number}번
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
          let textColor = '#4b5563';
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
  const [selectedExam, setSelectedExam] = useState(null);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedUnit, setSelectedUnit] = useState(null);
  const [selectedYear, setSelectedYear] = useState(null);
  const [selectedYearSubject, setSelectedYearSubject] = useState(null);
  
  // taxonomy states
  const [taxSubject, setTaxSubject] = useState(null);
  const [taxSubSubject, setTaxSubSubject] = useState(null);
  const [taxChapter, setTaxChapter] = useState(null);

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
      let displaySubject = q.subject || q.tags?.subject || getSubject(q.number, q.period || '2', q.exam);
      
      // 세무사 시험 과목명 정규화
      if (q.exam === '세무사') {
        if (displaySubject === '회계학' || displaySubject === '회계학개론') displaySubject = '회계학개론';
        if (displaySubject === '민법' || displaySubject === '민법총칙') displaySubject = '민법';
      }
      
      let unifiedSubject = displaySubject;
      if (displaySubject.includes('민법')) unifiedSubject = '민법';
      else if (displaySubject.includes('경제학') || displaySubject === '재정학') unifiedSubject = '경제학';
      else if (displaySubject.includes('부동산학')) unifiedSubject = '부동산학개론';
      else if (displaySubject.includes('회계학') || displaySubject.includes('회계원리')) unifiedSubject = '회계학';
      else if (displaySubject.includes('관계법규') || displaySubject.includes('공법') || displaySubject.includes('중개사법') || displaySubject.includes('공시세법')) unifiedSubject = '감정평가관계법규';

      const unit = q.tags?.sub_unit || getMockUnit(q.number);
      const category = q.tags?.unit || unifiedSubject;

      // V4 분류 정보: Gemini(gemini-2.5-flash) 또는 Claude(claude-sonnet-4-6)로
      // 분류되어 mapped_taxonomy가 있는 문제만 단원별 탭에 노출한다.
      // (Gemini는 in_scope 필드가 없어 null → 통과, Claude는 in_scope===false면 제외)
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
        options: q.options || q.choices, // Unify options and choices
        subject: displaySubject,
        unifiedSubject: unifiedSubject,
        category: category,
        unit: unit,
        concept: (q.tags?.concept && q.tags?.concept.trim() !== '') ? q.tags.concept :
                 ((q.tags?.sub_sub_unit && q.tags?.sub_sub_unit.trim() !== '') ? q.tags.sub_sub_unit : '기본 개념'),
        isWeak: q.tags?.difficulty === 3 || q.tags?.difficulty === 4 || q.tags?.difficulty === 5 || parseInt(q.number, 10) % 5 === 0,
        // 단원별 탭 전용 분류 필드 (mapped_taxonomy 기반)
        isClassified,
        taxSubjectName: isClassified ? mt.subject : null,
        taxSubSubjectName: isClassified ? (mt.sub_subject || null) : null,
        taxChapterName: isClassified ? (mt.chapter || null) : null,
        taxSectionName: isClassified ? (mt.section || null) : null,
      };
    });
  }, [loading, questionsData]);

  // View: 과목별 (5과목 등) - 새롭게 정밀 분류된 문제만 필터링
  const subjectGroups = useMemo(() => {
    const groups = {};
    processedData.forEach(q => {
      // V4 파이프라인으로 1회 이상 재분류된 문제만 통과
      if (!q.indexing_v4_count || q.indexing_v4_count < 1) return;

      const key = q.unifiedSubject;
      if (!groups[key]) {
        groups[key] = {
          type: 'unified_subject',
          title: q.unifiedSubject,
          subtitle: '과목',
          total: 0,
          weak: false,
          tag: '정밀분류 완료',
          filterFn: (item) => item.unifiedSubject === q.unifiedSubject && item.indexing_v4_count >= 1
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    return Object.values(groups).sort((a, b) => b.total - a.total);
  }, [processedData]);

  // Level 1: Categories (PART)
  const subjectCategoryGroups = useMemo(() => {
    if (!selectedSubject) return [];
    const groups = {};
    const filtered = processedData.filter(q => q.unifiedSubject === selectedSubject);
    
    groups['ALL'] = {
      type: 'play_all_subject',
      title: `${selectedSubject} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: false,
      tag: '전체',
      filterFn: (item) => item.unifiedSubject === selectedSubject
    };

    filtered.forEach(q => {
      const key = q.category;
      if (!groups[key]) {
        groups[key] = {
          type: 'subject_category',
          title: q.category,
          subtitle: selectedSubject,
          total: 0,
          weak: false,
          tag: '파트',
          filterFn: (item) => item.unifiedSubject === selectedSubject && item.category === q.category
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    
    const allGroup = groups['ALL'];
    delete groups['ALL'];
    return [allGroup, ...Object.values(groups).sort((a, b) => a.title.localeCompare(b.title))];
  }, [processedData, selectedSubject]);

  // Level 2: Units (Chapter)
  const subjectUnitGroups = useMemo(() => {
    if (!selectedCategory) return [];
    const groups = {};
    const filtered = processedData.filter(q => q.unifiedSubject === selectedSubject && q.category === selectedCategory);
    
    groups['ALL'] = {
      type: 'play_all_category',
      title: `${selectedCategory} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: false,
      tag: '전체',
      filterFn: (item) => item.unifiedSubject === selectedSubject && item.category === selectedCategory
    };

    filtered.forEach(q => {
      const key = q.unit;
      if (!groups[key]) {
        groups[key] = {
          type: 'subject_unit',
          title: q.unit,
          subtitle: selectedCategory,
          total: 0,
          weak: false,
          tag: '챕터',
          filterFn: (item) => item.unifiedSubject === selectedSubject && item.category === selectedCategory && item.unit === q.unit
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    
    const allGroup = groups['ALL'];
    delete groups['ALL'];
    return [allGroup, ...Object.values(groups).sort((a, b) => a.title.localeCompare(b.title))];
  }, [processedData, selectedSubject, selectedCategory]);

  // Level 3: Concepts (절)
  const subjectConceptGroups = useMemo(() => {
    if (!selectedUnit) return [];
    const groups = {};
    const filtered = processedData.filter(q => q.unifiedSubject === selectedSubject && q.category === selectedCategory && q.unit === selectedUnit);
    
    groups['ALL'] = {
      type: 'play_all_unit',
      title: `${selectedUnit} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: false,
      tag: '전체',
      filterFn: (item) => item.unifiedSubject === selectedSubject && item.category === selectedCategory && item.unit === selectedUnit
    };

    filtered.forEach(q => {
      const key = q.concept;
      if (!groups[key]) {
        groups[key] = {
          type: 'subject_concept',
          title: q.concept,
          subtitle: selectedUnit,
          total: 0,
          weak: false,
          tag: '절',
          filterFn: (item) => item.unifiedSubject === selectedSubject && item.category === selectedCategory && item.unit === selectedUnit && item.concept === q.concept
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    
    const allGroup = groups['ALL'];
    delete groups['ALL'];
    return [allGroup, ...Object.values(groups).sort((a, b) => a.title.localeCompare(b.title))];
  }, [processedData, selectedSubject, selectedCategory, selectedUnit]);

  // View: 연도별 (Level 1: Years)
  const yearGroups = useMemo(() => {
    const groups = {};
    processedData.forEach(q => {
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
    
    // Sort descending by year
    return Object.values(groups).sort((a, b) => parseInt(b.rawValue) - parseInt(a.rawValue));
  }, [processedData]);

  // View: 특정 연도 내 과목별 (Level 2: Subjects within a Year)
  const yearSubjectGroups = useMemo(() => {
    if (!selectedYear) return [];
    const groups = {};
    const filtered = processedData.filter(q => q.year === selectedYear);
    
    groups['ALL'] = {
      type: 'play_all_year',
      title: `${selectedYear}년 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: false,
      tag: '전체',
      filterFn: (item) => item.year === selectedYear
    };

    filtered.forEach(q => {
      // 감정평가사 5과목 기준으로 분류하기 위해 unifiedSubject 사용
      const key = q.unifiedSubject;
      if (!groups[key]) {
        groups[key] = {
          type: 'year_subject',
          title: q.unifiedSubject,
          subtitle: `${selectedYear}년`,
          total: 0,
          weak: false,
          tag: '과목',
          filterFn: (item) => item.year === selectedYear && item.unifiedSubject === q.unifiedSubject
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    
    const allGroup = groups['ALL'];
    delete groups['ALL'];
    return [allGroup, ...Object.values(groups).sort((a, b) => a.title.localeCompare(b.title))];
  }, [processedData, selectedYear]);

  // View: 특정 연도 및 과목 내 시험별 (Level 3: Exams within Year and Subject)
  const yearSubjectExamGroups = useMemo(() => {
    if (!selectedYear || !selectedYearSubject) return [];
    const groups = {};
    const filtered = processedData.filter(q => q.year === selectedYear && q.unifiedSubject === selectedYearSubject);
    
    groups['ALL'] = {
      type: 'play_all_year_subject',
      title: `${selectedYearSubject} 전체 풀기`,
      subtitle: `${selectedYear}년`,
      total: filtered.length,
      weak: false,
      tag: '전체',
      filterFn: (item) => item.year === selectedYear && item.unifiedSubject === selectedYearSubject
    };

    filtered.forEach(q => {
      const key = q.exam;
      if (!groups[key]) {
        groups[key] = {
          type: 'year_subject_exam',
          title: q.exam,
          subtitle: selectedYearSubject,
          total: 0,
          weak: false,
          tag: '시험',
          filterFn: (item) => item.year === selectedYear && item.unifiedSubject === selectedYearSubject && item.exam === q.exam
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    
    const allGroup = groups['ALL'];
    delete groups['ALL'];
    return [allGroup, ...Object.values(groups).sort((a, b) => a.title.localeCompare(b.title))];
  }, [processedData, selectedYear, selectedYearSubject]);

  // View: 시험별 (Exams)
  const examGroups = useMemo(() => {
    const groups = {};
    processedData.forEach(q => {
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

  // View: 특정 시험 내 과목별 (Subjects within an Exam)
  const examSubjectGroups = useMemo(() => {
    if (!selectedExam) return [];
    const groups = {};
    processedData.filter(q => q.exam === selectedExam).forEach(q => {
      const key = q.subject;
      if (!groups[key]) {
        groups[key] = {
          type: 'subject',
          title: q.subject,
          subtitle: selectedExam,
          total: 0,
          weak: false,
          tag: '과목',
          filterFn: (item) => item.exam === selectedExam && item.subject === q.subject
        };
      }
      groups[key].total += 1;
      if (q.isWeak) groups[key].weak = true;
    });
    return Object.values(groups).sort((a, b) => a.title.localeCompare(b.title));
  }, [processedData, selectedExam]);

  // View: 단원별 - 과목 목록 (Gemini/Claude로 분류된 문제만)
  const taxSubjectGroups = useMemo(() => {
    if (!taxonomyData) return [];
    return Object.keys(taxonomyData).map(subj => {
      const filtered = processedData.filter(q => q.isClassified && q.taxSubjectName === subj);
      return {
        type: 'tax_subject',
        title: subj,
        subtitle: '단원별 학습',
        total: filtered.length,
        weak: false,
        tag: '과목'
      };
    }).filter(g => g.total > 0);
  }, [taxonomyData, processedData]);

  // View: 단원별 - 세부 과목 또는 장(Chapter) 목록 (분류 문제만)
  const taxSubSubjectGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject) return [];
    const subjData = taxonomyData[taxSubject];
    const filtered = processedData.filter(q => q.isClassified && q.taxSubjectName === taxSubject);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSubject} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: false,
      tag: '전체',
      filterFn: (item) => item.isClassified && item.taxSubjectName === taxSubject
    });

    if (subjData.has_subjects) {
      Object.keys(subjData.subjects).forEach(subSubj => {
        const ssCount = filtered.filter(q => q.taxSubSubjectName === subSubj).length;
        if (ssCount === 0) return;
        groups.push({
          type: 'tax_sub_subject',
          title: subSubj,
          subtitle: taxSubject,
          total: ssCount,
          weak: false,
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
          weak: false,
          tag: 'PART/장',
          filterFn: (item) => item.isClassified && item.taxSubjectName === taxSubject && item.taxChapterName === ch.name
        });
      });
    }
    return groups;
  }, [taxonomyData, taxSubject, processedData]);

  // View: 단원별 - 장(Chapter) 목록 (세부 과목이 있는 경우, 분류 문제만)
  const taxChapterGroups = useMemo(() => {
    if (!taxonomyData || !taxSubject || !taxSubSubject) return [];
    const subjData = taxonomyData[taxSubject];
    const chapters = subjData.subjects[taxSubSubject] || [];
    const filtered = processedData.filter(q =>
      q.isClassified && q.taxSubjectName === taxSubject && q.taxSubSubjectName === taxSubSubject);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxSubSubject} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: false,
      tag: '전체',
      filterFn: (item) => item.isClassified && item.taxSubjectName === taxSubject && item.taxSubSubjectName === taxSubSubject
    });
    chapters.forEach(ch => {
      const chFiltered = filtered.filter(q => q.taxChapterName === ch.name);
      if (chFiltered.length === 0) return;
      groups.push({
        type: 'tax_chapter',
        title: ch.name,
        subtitle: taxSubSubject,
        total: chFiltered.length,
        weak: false,
        tag: 'PART/장',
        filterFn: (item) => item.isClassified && item.taxSubjectName === taxSubject && item.taxChapterName === ch.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, processedData]);

  // View: 단원별 - 절(Section) 목록
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
    
    const filtered = processedData.filter(q =>
      q.isClassified && q.taxSubjectName === taxSubject && q.taxChapterName === taxChapter);

    const groups = [];
    groups.push({
      type: 'play_all_tax',
      title: `${taxChapter} 전체 풀기`,
      subtitle: '전체',
      total: filtered.length,
      weak: false,
      tag: '전체',
      filterFn: (item) => item.isClassified && item.taxSubjectName === taxSubject && item.taxChapterName === taxChapter
    });

    chapterData.sections.forEach(sec => {
      const secCount = filtered.filter(q => q.taxSectionName === sec.name).length;
      if (secCount === 0) return;
      groups.push({
        type: 'play_all_tax',
        title: sec.name,
        subtitle: taxChapter,
        total: secCount,
        weak: false,
        tag: '절',
        filterFn: (item) => item.isClassified && item.taxSubjectName === taxSubject && item.taxSectionName === sec.name
      });
    });
    return groups;
  }, [taxonomyData, taxSubject, taxSubSubject, taxChapter, processedData]);

  let activeGroups = [];
  if (viewMode === 'subject') activeGroups = subjectGroups;
  else if (viewMode === 'year') activeGroups = yearGroups;
  else if (viewMode === 'exam') activeGroups = examGroups;
  else if (viewMode === 'chapter') activeGroups = taxSubjectGroups;

  const totalQuestions = processedData.length;

  const handleGroupClick = (group) => {
    if (group.type === 'exam') {
      setSelectedExam(group.title);
      setCurrentView('exam_subjects');
      window.scrollTo(0, 0);
    } else if (group.type === 'unified_subject') {
      setSelectedSubject(group.title);
      setCurrentView('subject_categories');
      window.scrollTo(0, 0);
    } else if (group.type === 'year_group') {
      setSelectedYear(group.rawValue);
      setCurrentView('year_subjects');
      window.scrollTo(0, 0);
    } else if (group.type === 'year_subject') {
      setSelectedYearSubject(group.title);
      setCurrentView('year_subject_exams');
      window.scrollTo(0, 0);
    } else if (group.type === 'subject_category') {
      setSelectedCategory(group.title);
      setCurrentView('subject_units');
      window.scrollTo(0, 0);
    } else if (group.type === 'subject_unit') {
      setSelectedUnit(group.title);
      setCurrentView('subject_concepts');
      window.scrollTo(0, 0);
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
    } else {
      setSelectedGroup(group);
      setCurrentView('question_list');
      window.scrollTo(0, 0);
    }
  };

  const handleBack = () => {
    if (currentView === 'question_list') {
      if (selectedGroup?.type === 'subject') {
        setCurrentView('exam_subjects');
      } else if (selectedGroup?.type === 'year_subject_exam') {
        setCurrentView('year_subject_exams');
      } else if (selectedGroup?.type?.startsWith('play_all_')) {
        let taxReturnView = 'dashboard';
        if (taxChapter) taxReturnView = 'tax_sections';
        else if (taxSubSubject) taxReturnView = 'tax_chapters';
        else if (taxSubject) taxReturnView = 'tax_sub_subjects';
        
        const typeMap = { 
          'play_all_subject': 'subject_categories', 
          'play_all_category': 'subject_units', 
          'play_all_unit': 'subject_concepts', 
          'play_all_year': 'year_subjects', 
          'play_all_year_subject': 'year_subject_exams',
          'play_all_tax': taxReturnView
        };
        setCurrentView(typeMap[selectedGroup.type] || 'dashboard');
      } else if (selectedGroup?.type === 'subject_concept') {
        setCurrentView('subject_concepts');
      } else {
        setCurrentView('dashboard');
      }
      setSelectedGroup(null);
    } else if (currentView === 'exam_subjects') {
      setCurrentView('dashboard');
      setSelectedExam(null);
    } else if (currentView === 'year_subjects') {
      setCurrentView('dashboard');
      setSelectedYear(null);
    } else if (currentView === 'year_subject_exams') {
      setCurrentView('year_subjects');
      setSelectedYearSubject(null);
    } else if (currentView === 'subject_categories') {
      setCurrentView('dashboard');
      setSelectedSubject(null);
    } else if (currentView === 'subject_units') {
      setCurrentView('subject_categories');
      setSelectedCategory(null);
    } else if (currentView === 'subject_concepts') {
      setCurrentView('subject_units');
      setSelectedUnit(null);
    } else if (currentView === 'tax_sub_subjects') {
      setCurrentView('dashboard');
      setTaxSubject(null);
    } else if (currentView === 'tax_chapters') {
      setCurrentView('tax_sub_subjects');
      setTaxSubSubject(null);
    } else if (currentView === 'tax_sections') {
      setCurrentView('tax_chapters');
      setTaxChapter(null);
    }
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

  if (currentView === 'exam_subjects' && selectedExam) {
    return (
      <div className="app-container">
        <header className="top-nav" style={{ borderBottom: '1px solid #e5e7eb' }}>
          <button className="back-btn" onClick={handleBack}>
            <ArrowLeft size={24} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '1rem', fontWeight: '600' }}>뒤로가기</span>
          </button>
        </header>
        
        <div style={{ padding: '24px 20px', background: '#fff', borderBottom: '1px solid #e5e7eb' }}>
          <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '4px' }}>자격시험</div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: '700' }}>{selectedExam} 과목 목록</h1>
        </div>
        
        <main className="main-content" style={{ marginTop: '20px' }}>
          <div className="study-grid">
            {examSubjectGroups.map((group, idx) => (
              <div key={idx} className="study-card" onClick={() => handleGroupClick(group)}>
                <div className="card-badge">과목</div>
                <div className="card-subtitle">{group.subtitle}</div>
                <h3 className="card-title">{group.title}</h3>
                <div className="card-total">총 {group.total} 문제</div>
                <div className="play-btn">선택</div>
              </div>
            ))}
          </div>
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

  if (currentView === 'subject_categories' && selectedSubject) return renderStudyGrid(selectedSubject, '과목별 파트 목록', subjectCategoryGroups);
  if (currentView === 'subject_units' && selectedCategory) return renderStudyGrid(selectedCategory, '단원(Chapter) 목록', subjectUnitGroups);
  if (currentView === 'subject_concepts' && selectedUnit) return renderStudyGrid(selectedUnit, '개념(절) 목록', subjectConceptGroups);
  if (currentView === 'year_subjects' && selectedYear) return renderStudyGrid(`${selectedYear}년 기출`, '연도별 과목 목록', yearSubjectGroups);
  if (currentView === 'year_subject_exams' && selectedYearSubject) return renderStudyGrid(selectedYearSubject, `${selectedYear}년 자격시험 목록`, yearSubjectExamGroups);

  // Taxonomy Views
  if (currentView === 'tax_sub_subjects' && taxSubject) return renderStudyGrid(taxSubject, '목차 학습', taxSubSubjectGroups);
  if (currentView === 'tax_chapters' && taxSubSubject) return renderStudyGrid(taxSubSubject, '장(Chapter) 선택', taxChapterGroups);
  if (currentView === 'tax_sections' && taxChapter) return renderStudyGrid(taxChapter, '절(Section) 선택', taxSectionGroups);

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
            <button 
              className={viewMode === 'exam' ? 'active' : ''} 
              onClick={() => { setViewMode('exam'); setSelectedExam(null); setSelectedSubject(null); setSelectedYear(null); setSelectedYearSubject(null); setSelectedCategory(null); setSelectedUnit(null); setTaxSubject(null); setTaxSubSubject(null); setTaxChapter(null); }}
            >
              시험별
            </button>
            <button 
              className={viewMode === 'subject' ? 'active' : ''} 
              onClick={() => { setViewMode('subject'); setSelectedSubject(null); setSelectedCategory(null); setSelectedUnit(null); setSelectedExam(null); setSelectedYear(null); setSelectedYearSubject(null); setTaxSubject(null); setTaxSubSubject(null); setTaxChapter(null); }}
            >
              과목별
            </button>
            <button 
              className={viewMode === 'chapter' ? 'active' : ''} 
              onClick={() => { setViewMode('chapter'); setCurrentView('dashboard'); setSelectedSubject(null); setSelectedCategory(null); setSelectedUnit(null); setSelectedExam(null); setSelectedYear(null); setSelectedYearSubject(null); setTaxSubject(null); setTaxSubSubject(null); setTaxChapter(null); }}
            >
              단원별
            </button>
            <button 
              className={viewMode === 'year' ? 'active' : ''} 
              onClick={() => { setViewMode('year'); setSelectedSubject(null); setSelectedCategory(null); setSelectedUnit(null); setSelectedExam(null); setSelectedYear(null); setSelectedYearSubject(null); setTaxSubject(null); setTaxSubSubject(null); setTaxChapter(null); }}
            >
              연도별
            </button>
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
