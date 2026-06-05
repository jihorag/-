// 공용 UI 훅 — 모달/오버레이 공통 동작 일원화
import { useEffect } from 'react';

// 오버레이가 열려 있는 동안 배경(body) 스크롤 잠금.
// 모바일에서 모달 위 스와이프가 뒤 콘텐츠로 새는 문제 방지.
export function useScrollLock(active) {
  useEffect(() => {
    if (!active) return undefined;
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, [active]);
}

// 오버레이가 열려 있는 동안 ESC 키로 닫기.
export function useEscClose(active, onClose) {
  useEffect(() => {
    if (!active) return undefined;
    const onKey = (e) => { if (e.key === 'Escape') { e.stopPropagation(); onClose(); } };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [active, onClose]);
}
