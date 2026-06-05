// 전역 토스트 알림 시스템
// 사용: window.showToast('메시지', 'success'|'error'|'info'|'warn')
//      또는 import { toast } from './Toast'; toast.success('...')

import { useEffect, useState } from 'react';

let pushFn = null;

export const toast = {
  show: (msg, type = 'info', duration = 3000) => {
    if (pushFn) pushFn({ msg, type, duration });
    else if (typeof window !== 'undefined') window.alert(msg);
  },
  success: (msg, d) => toast.show(msg, 'success', d),
  error: (msg, d) => toast.show(msg, 'error', d ?? 4500),
  warn: (msg, d) => toast.show(msg, 'warn', d),
  info: (msg, d) => toast.show(msg, 'info', d),
};

const COLORS = {
  success: { bg: '#dcfce7', border: '#86efac', text: '#15803d', icon: '✅' },
  error:   { bg: '#fef2f2', border: '#fecaca', text: '#991b1b', icon: '⚠️' },
  warn:    { bg: '#fef3c7', border: '#fcd34d', text: '#92400e', icon: '⚠️' },
  info:    { bg: '#eff6ff', border: '#bfdbfe', text: '#1d4ed8', icon: 'ℹ️' },
};

export default function ToastContainer() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    pushFn = (item) => {
      const id = Math.random().toString(36).slice(2) + Date.now();
      // 동시 표시 최대 3개 — 초과 시 가장 오래된 것부터 밀어냄 (화면 상단 점유 방지)
      setItems((arr) => [...arr, { id, ...item }].slice(-3));
      setTimeout(() => {
        setItems((arr) => arr.filter((x) => x.id !== id));
      }, item.duration || 3000);
    };
    // window 전역 핸들 (기존 alert 대체용)
    if (typeof window !== 'undefined') {
      window.showToast = (msg, type, duration) => toast.show(msg, type, duration);
    }
    return () => { pushFn = null; };
  }, []);

  if (items.length === 0) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 'calc(env(safe-area-inset-top, 0px) + 14px)',
      left: '50%', transform: 'translateX(-50%)',
      zIndex: 'var(--z-toast)', display: 'flex', flexDirection: 'column', gap: 8,
      pointerEvents: 'none',
      width: 'min(420px, 92vw)',
    }}>
      {items.map((t) => {
        const c = COLORS[t.type] || COLORS.info;
        return (
          <div key={t.id}
            style={{
              background: c.bg, border: `1px solid ${c.border}`,
              color: c.text, borderRadius: 10, padding: '11px 14px',
              boxShadow: '0 6px 18px rgba(15,23,42,0.12)',
              display: 'flex', alignItems: 'center', gap: 8,
              fontSize: '0.9rem', fontWeight: 700,
              pointerEvents: 'auto',
              animation: 'toastIn 0.22s cubic-bezier(0.22, 0.61, 0.36, 1)',
            }}
            onClick={() => setItems((arr) => arr.filter((x) => x.id !== t.id))}
          >
            <span style={{ fontSize: '1.05rem' }}>{c.icon}</span>
            <span style={{ flex: 1, whiteSpace: 'pre-wrap' }}>{t.msg}</span>
          </div>
        );
      })}
    </div>
  );
}
