// 심화 탭 — 약점에서 출발하는 자유 대화.
//
// 빈손으로 시작하지 않는다(시안 316:506). 탭을 열면 「이 관에서 두 번 이상 틀린
// 곳입니다」와 약점 카드가 먼저 뜬다. 자유 대화는 「무엇을 물어야 할지 모르겠다」에서
// 막히기 때문이다.
//
// 말풍선은 개념 완성과 같은 렌더러(ConceptScene 의 Bubble)를 쓰지 않고 여기서 다시
// 그린다 — Bubble 은 ConceptScene 안의 지역 컴포넌트라 지금 내보내지 않는다.
// 클래스 이름은 같은 것을 쓰므로 생김새는 같다.
import { useMemo, useState } from 'react';
import ParsedText from './ParsedText';
import Avatar from './ConceptCast';
import { markEmphasis } from './emphasis';
import { weakSpots } from './weakSpots';
import { WHO } from './conceptTurns';

export default function DeepChat({
  leafTitle, track, items, onAsk, onGoPoint, onOpenSettings,
}) {
  const [msgs, setMsgs] = useState([]);
  const [draft, setDraft] = useState('');
  const [busy, setBusy] = useState(false);
  const weak = useMemo(
    () => weakSpots({ leafId: track?.leaf_id, track, items }),
    [track, items],
  );

  if (!onAsk) {
    return (
      <div className="cs-room">
        <div className="cs-stream">
          <div className="byok">
            <h2>AI 튜터와 단원별 1:1 학습</h2>
            <ul>
              <li>교재 전 단원을 대화하며 개념 학습 → 이해 확인 퀴즈</li>
              <li>문제풀이 중 막히면 「AI 튜터로 이 단원 배우기」로 바로 연결</li>
              <li>학습 기록 기반 약점 분석·복습 추천</li>
            </ul>
            <div className="byok-box">
              <h3>API 키 입력</h3>
              <p>
                본 앱은 사용자의 API 키로 직접 요청합니다. 키는 이 기기에만 저장되고
                서버로 전송되지 않습니다. 키 없이도 개념 완성과 기출 분석은 끝까지 진행됩니다.
              </p>
              <button type="button" className="cs-primary" onClick={onOpenSettings}>
                설정에서 키 넣기
              </button>
              <p className="byok-hint">Claude · OpenAI · Gemini 를 모두 지원합니다.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const send = async (text) => {
    if (!text.trim() || busy) return;
    setDraft('');
    setMsgs((m) => m.concat({ who: 'me', text }));
    setBusy(true);
    try {
      const { answer, cited } = await onAsk(text);
      setMsgs((m) => m.concat({ who: 'ai', text: answer, cited }));
    } catch (e) {
      setMsgs((m) => m.concat({ who: 'ai', text: `답을 가져오지 못했습니다. ${e?.message || ''}`.trim() }));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="cs-room">
      <div className="cs-stream">
        {msgs.length === 0 && (
          <>
            <Line who={WHO.teach} text={weak.length
              ? '이 관에서 두 번 이상 틀린 곳입니다.\n눌러서 바로 이야기해요.'
              : `${leafTitle || '이 관'}에 대해 무엇이든 물어보세요.`} />
            {weak.length > 0 && (
              <div className="deep-cards">
                {weak.map((w) => (
                  <button type="button" key={w.pointId} className="deep-card"
                    onClick={() => send(`${w.title}에 대해 다시 설명해 주세요. 제가 자꾸 틀립니다.`)}>
                    <span className="deep-card-title">{w.title}</span>
                    <span className="deep-card-why">{w.why}</span>
                  </button>
                ))}
              </div>
            )}
            <p className="deep-note">목록에 없는 것도 아래에 바로 물어보세요.</p>
          </>
        )}
        {msgs.map((m, i) => (
          <Line key={i} who={m.who === 'me' ? WHO.ask : WHO.teach} text={m.text}
            cited={m.cited} onGoPoint={onGoPoint} />
        ))}
        {busy && <p className="deep-note">답을 가져오는 중…</p>}
      </div>
      <div className="cs-dock">
        <div className="cs-inputwrap">
          <div className="cs-input">
            <input value={draft} onChange={(e) => setDraft(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); send(draft); } }}
              placeholder="무엇이든 물어보세요" aria-label="질문" />
            <button type="button" className="cs-send" onClick={() => send(draft)}
              disabled={!draft.trim() || busy} aria-label="보내기">→</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function Line({ who, text, cited, onGoPoint }) {
  const right = who === WHO.ask;
  return (
    <div className={`cs-line${right ? ' is-right' : ''}`}>
      {!right && <div className="cs-avatar"><Avatar who={who} size={28} /></div>}
      <div className="cs-linebody">
        <span className="cs-who">{right ? '나' : '선생'}</span>
        <div className={`cs-bubble cs-bubble--${who}`}>
          <ParsedText text={markEmphasis(text)} />
          {/* 출처는 교재 문단 번호가 아니라 논점이다 — 학습자가 아는 단위가 그것이다. */}
          {(cited || []).slice(0, 2).map((c) => (
            <button type="button" key={c.id} className="deep-cite"
              onClick={() => onGoPoint?.(c)}>
              {(c.path || []).slice(-1)[0] || '교재'}
            </button>
          ))}
        </div>
      </div>
      {right && <div className="cs-avatar"><Avatar who={who} size={28} /></div>}
    </div>
  );
}
