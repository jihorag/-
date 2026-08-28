// 과목 아이콘 — 컬러 이모지 대신 단색(모노크롬) lucide 아이콘.
// 색은 호출부에서 지정(기본 중성 회색). 앱 전반의 무채색 톤과 일치.
import { TrendingUp, Calculator, Scale, Building2, ScrollText, Ruler, BookOpen, Gavel, BookMarked } from 'lucide-react';

const MAP = {
  economics: TrendingUp,      // 경제학
  accounting: Calculator,     // 회계학
  civil: Scale,               // 민법
  realestate: Building2,      // 부동산학
  law: ScrollText,            // 관계법규
  appraisal_practice: Ruler,  // 감정평가실무
  appraisal_theory: BookOpen, // 감정평가이론
  appraisal_law: Gavel,       // 보상법규
};

export default function SubjectIcon({ id, size = 24, color = '#6b7280', strokeWidth = 2, style }) {
  const Ic = MAP[id] || BookMarked;
  return <Ic size={size} color={color} strokeWidth={strokeWidth} style={style} />;
}
