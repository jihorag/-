// 공용 UI 훅 — 모달/오버레이 공통 동작 일원화
import { useEffect } from 'react';

// 오버레이가 열려 있는 동안 배경(body) 스크롤 잠금.
// 모바일에서 모달 위 스와이프가 뒤 콘텐츠로 새는 문제 방지.
//
// ⚠️ 참조 카운트 방식 — 같은 모달을 두 곳에서 잠그거나(예: App이 showCmdK,
// CmdK 컴포넌트가 open) 모달이 중첩될 때, 각 인스턴스가 직전 overflow 값을
// 캡처·복원하면 'hidden'을 서로 물려받아 마지막 해제 시 잠금이 영구히 남는다
// (CmdK 한 번 열었다 닫으면 전체 상하 스크롤 멈춤). 카운트 0일 때만 해제.
let _scrollLockCount = 0;
export function useScrollLock(active) {
  useEffect(() => {
    if (!active) return undefined;
    _scrollLockCount += 1;
    document.body.style.overflow = 'hidden';
    return () => {
      _scrollLockCount = Math.max(0, _scrollLockCount - 1);
      if (_scrollLockCount === 0) document.body.style.overflow = '';
    };
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
