const fs = require('fs');
const questionsData = JSON.parse(fs.readFileSync('viewer/src/data/questions_db.json', 'utf-8'));

const getSubject = (numStr, period, exam) => {
  const num = parseInt(numStr, 10);
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

const processedData = questionsData.map(q => {
  const subject = q.subject || q.tags?.subject || getSubject(q.number, q.period || '2', q.exam);
  let unifiedSubject = subject;
  if (subject.includes('민법')) unifiedSubject = '민법';
  else if (subject.includes('경제학') || subject === '재정학') unifiedSubject = '경제학';
  else if (subject.includes('부동산학')) unifiedSubject = '부동산학개론';
  else if (subject.includes('회계학')) unifiedSubject = '회계학';
  else if (subject.includes('관계법규') || subject.includes('공법') || subject.includes('중개사법') || subject.includes('공시세법')) unifiedSubject = '감정평가관계법규';

  return {
    exam: q.exam || '감정평가사',
    subject: subject,
    unifiedSubject: unifiedSubject
  };
});

const groups = {};
processedData.filter(q => q.exam === '세무사').forEach(q => {
  const key = q.subject;
  if (!groups[key]) groups[key] = 0;
  groups[key]++;
});

console.log('세무사 subjects:', groups);
