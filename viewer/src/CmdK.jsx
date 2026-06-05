// 글로벌 Cmd+K 검색 모달
// 검색 항목: 탭·과목·단원(leaf)·채팅방·설정
//
// props:
//   open: boolean
//   onClose: () => void
//   onNavigate: (action) => void   — action: { type, ...payload }
//   subjects: [{id, title, short, icon, color, stage}]
//   leaves: [{id, path, ...}]      (모든 과목 leaves 평탄)
//   rooms: [{leafId, msg_count, last_ts}]
//   leafById: Map<id, leaf>
//
// action 타입:
//   { type: 'tab', view }                — 탭/뷰 전환
//   { type: 'subject', id }              — 과목 진입
//   { type: 'leaf', leaf }               — 단원 진입
//   { type: 'settings', ctx }            — 설정 드로어 열기

import { useEffect, useMemo, useRef, useState } from 'react';
import { useScrollLock } from './uiHooks';

const TABS = [
  { id: 'home', label: '홈', icon: '🏠', sub: '대시보드', view: 'home' },
  { id: 'ai',   label: 'AI 학습', icon: '🤖', sub: '대화형 학습', view: 'civil' },
  { id: 'browse', label: '문제풀이', icon: '📚', sub: '기출 풀이', view: 'dashboard' },
  { id: 'review', label: '복습', icon: '🔁', sub: 'SRS 복습', view: 'reviewHome' },
  { id: 'status', label: '현황', icon: '📊', sub: '시각화', view: 'status' },
];

const SETTINGS_OPTIONS = [
  { ctx: 'home',     label: '홈 설정', sub: '시험일·일일 목표' },
  { ctx: 'ai',       label: 'AI 학습 설정', sub: '모델·스트리밍·API 키' },
  { ctx: 'practice', label: '문제풀이 설정', sub: '학습 순서·자동 다음·글자 크기' },
  { ctx: 'review',   label: '복습 설정', sub: 'SRS 강도·알림' },
  { ctx: 'status',   label: '현황 설정', sub: '추세 기간' },
];

function normalize(s) {
  return (s || '').toLowerCase().replace(/\s+/g, '');
}

export default function CmdK({ open, onClose, onNavigate, subjects = [], leaves = [], rooms = [], leafById }) {
  useScrollLock(open);
  const [q, setQ] = useState('');
  const [activeIdx, setActiveIdx] = useState(0);
  const inputRef = useRef(null);

  // 모달 오픈 시 input focus + 초기화
  useEffect(() => {
    if (open) {
      setQ('');
      setActiveIdx(0);
      setTimeout(() => inputRef.current?.focus(), 30);
    }
  }, [open]);

  // 항목 빌드 (검색어 적용)
  const items = useMemo(() => {
    const nq = normalize(q);
    const out = [];

    const matches = (s) => !nq || normalize(s).includes(nq);

    // 탭
    TABS.forEach((t) => {
      if (matches(t.label) || matches(t.sub)) {
        out.push({ section: '탭', kind: 'tab', label: t.label, sub: t.sub, icon: t.icon, action: { type: 'tab', view: t.view } });
      }
    });

    // 과목
    subjects.forEach((s) => {
      if (matches(s.title) || matches(s.short)) {
        out.push({
          section: '과목', kind: 'subject',
          label: s.short, sub: `${s.title}${s.stage === 2 ? ' · 2차' : ''}`,
          icon: s.icon, action: { type: 'subject', id: s.id },
        });
      }
    });

    // 단원 (leaves)
    if (nq.length >= 1) {
      const matched = leaves.filter((l) => {
        const path = (l.path || []).join(' / ');
        return matches(path) || matches(l.title || '');
      }).slice(0, 12);
      matched.forEach((l) => {
        out.push({
          section: '단원', kind: 'leaf',
          label: l.path?.slice(-1)[0] || l.title || l.id,
          sub: (l.path || []).slice(0, -1).join(' › '),
          icon: '📂', action: { type: 'leaf', leaf: l },
        });
      });
    }

    // 채팅방
    rooms.slice(0, 8).forEach((r) => {
      const leaf = leafById?.get?.(r.leafId);
      const name = leaf ? (leaf.path?.slice(-1)[0] || leaf.title) : r.leafId;
      if (matches(name) || (leaf && matches((leaf.path || []).join(' / ')))) {
        out.push({
          section: '채팅방', kind: 'room',
          label: name, sub: `${r.msg_count}건 · ${(r.last_ts || '').slice(0, 10)}`,
          icon: '💬', action: { type: 'leaf', leaf },
        });
      }
    });

    // 설정
    SETTINGS_OPTIONS.forEach((s) => {
      if (matches(s.label) || matches(s.sub) || matches('설정') || matches('settings')) {
        out.push({
          section: '설정', kind: 'settings',
          label: s.label, sub: s.sub,
          icon: '⚙️', action: { type: 'settings', ctx: s.ctx },
        });
      }
    });

    return out;
  }, [q, subjects, leaves, rooms, leafById]);

  // 활성 인덱스 보정
  useEffect(() => {
    if (activeIdx >= items.length) setActiveIdx(Math.max(0, items.length - 1));
  }, [items.length, activeIdx]);

  // 키 이벤트
  useEffect(() => {
    if (!open) return;
    const onKey = (e) => {
      if (e.key === 'Escape') { e.preventDefault(); onClose(); return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); setActiveIdx((i) => Math.min(items.length - 1, i + 1)); return; }
      if (e.key === 'ArrowUp') { e.preventDefault(); setActiveIdx((i) => Math.max(0, i - 1)); return; }
      if (e.key === 'Enter') {
        e.preventDefault();
        const it = items[activeIdx];
        if (it) { onNavigate(it.action); onClose(); }
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, items, activeIdx, onClose, onNavigate]);

  if (!open) return null;

  // 섹션별 그룹화
  let lastSection = null;

  return (
    <div className="cmdk-overlay" onClick={onClose}>
      <div className="cmdk-modal" onClick={(e) => e.stopPropagation()}>
        <input
          ref={inputRef}
          className="cmdk-input"
          placeholder="🔍 탭·과목·단원·채팅방·설정 검색..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <div className="cmdk-list">
          {items.length === 0 && (
            <div style={{ padding: 24, textAlign: 'center', color: '#9ca3af', fontSize: '0.88rem' }}>
              일치하는 항목이 없습니다
            </div>
          )}
          {items.map((it, i) => {
            const showSection = it.section !== lastSection;
            lastSection = it.section;
            return (
              <div key={`${it.kind}-${i}`}>
                {showSection && <div className="cmdk-section">{it.section}</div>}
                <div
                  className={`cmdk-item ${i === activeIdx ? 'active' : ''}`}
                  onMouseEnter={() => setActiveIdx(i)}
                  onClick={() => { onNavigate(it.action); onClose(); }}
                >
                  <span className="ic">{it.icon}</span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontWeight: 700, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {it.label}
                    </div>
                    {it.sub && (
                      <div className="sub" style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {it.sub}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        <div className="cmdk-footer">
          <span><kbd className="cmdk-kbd">↑↓</kbd> 이동</span>
          <span><kbd className="cmdk-kbd">⏎</kbd> 선택</span>
          <span><kbd className="cmdk-kbd">Esc</kbd> 닫기</span>
        </div>
      </div>
    </div>
  );
}
