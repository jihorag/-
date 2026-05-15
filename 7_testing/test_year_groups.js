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
  return {
    year: q.year || '2025',
    subject: subject,
  };
});

const groups2026 = new Set();
processedData.filter(q => q.year === '2026').forEach(q => groups2026.add(q.subject));

console.log('2026 subjects:', Array.from(groups2026));
