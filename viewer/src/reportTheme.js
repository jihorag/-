// 학습 진단 리포트 공용 디자인 토큰 — A4 미색 종이 + 명조 활자 + 먹색(INK) 계조.
// Proficiency.jsx(종합 리포트)와 SubjectDiagnostic.jsx(과목별 진단)가 같은 양식을 공유한다.
import { createElement } from 'react';

export const SERIF = "'AppleMyungjo','Nanum Myeongjo','Batang','Times New Roman',serif";
export const INK = { 900: '#17150f', 800: '#26231b', 700: '#3a362c', 600: '#57513f', 500: '#726b57', 400: '#9a927d', 300: '#c9c2ad', 200: '#e2dccb', 100: '#efe9da', 50: '#f7f2e6' };
export const PAPER = '#fbf8f0';
export const DESK = '#ffffff';
export const NUM = { fontVariantNumeric: 'tabular-nums' };
export const ROMAN = ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ'];

// 로마숫자(또는 무번호) 표제 섹션 — 명조 제목 + 먹색 밑줄.
export function DocSection({ no, title, hint, dense, children }) {
  return createElement('section', { style: { marginTop: dense ? 16 : 26 } },
    createElement('h2', { style: { fontFamily: SERIF, fontSize: dense ? '0.94rem' : '1.05rem', fontWeight: 800, color: INK[900], margin: '0 0 3px', letterSpacing: '-0.01em' } },
      no != null ? createElement('span', { style: { color: INK[400], marginRight: 9 } }, no) : null,
      title,
      hint ? createElement('span', { style: { fontSize: '0.64rem', fontWeight: 600, color: INK[400], marginLeft: 8 } }, hint) : null,
    ),
    createElement('div', { style: { borderBottom: `1px solid ${INK[300]}`, marginBottom: dense ? 10 : 13 } }),
    children,
  );
}
