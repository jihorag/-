// 4단째 교재 패널 — 시안 334:229.
//
// 대화가 근거를 못 대면 확인할 데가 있어야 한다. 대화 열이 560 에서 약 470 으로
// 좁아지는 것을 감수하는 대신 교재와 대화를 나란히 본다.
//
// 교재 본문에도 대화와 **같은 형광펜 규칙**을 적용한다 — 노랑=공식, 보라=뒤집힘.
// 같은 색이 같은 뜻이어야 한다.
import { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import ParsedText from './ParsedText';
import { markEmphasis } from './emphasis';

export default function TextbookPanel({ chunks, focusId, onClose, onAskAbout }) {
  const ref = useRef(null);
  useEffect(() => {
    if (focusId) ref.current?.querySelector(`[data-chunk="${focusId}"]`)?.scrollIntoView({ block: 'center' });
  }, [focusId]);

  return (
    <aside className="tbook" aria-label="교재">
      <div className="tbook-head">
        <span className="tbook-label">교재</span>
        <button type="button" className="cs-tool" onClick={onClose} aria-label="닫기">
          <X size={15} strokeWidth={1.75} />
        </button>
      </div>
      <div className="tbook-body" ref={ref}>
        {chunks.length === 0 && <p className="tbook-empty">이 단원의 교재가 아직 없습니다.</p>}
        {chunks.map((c) => (
          <section key={c.id} data-chunk={c.id} className="tbook-chunk">
            <h4 className="tbook-h">{(c.path || []).join(' › ')}</h4>
            <ParsedText text={markEmphasis(c.text)} />
            {onAskAbout && (
              <button type="button" className="tbook-ask"
                onClick={() => onAskAbout(c)}>이 부분 물어보기</button>
            )}
          </section>
        ))}
      </div>
    </aside>
  );
}
