// 개념 완성의 등장인물 넷 — 선으로만 그린다.
//
// 이모지를 쓰지 않는 이유는 취향이 아니라 일관성이다. 이 앱의 아이콘은 전부
// 1.75 굵기의 선화(lucide)라 이모지 하나가 끼면 그것만 다른 세계에서 온 것처럼
// 보인다. 그래서 같은 선 굵기·같은 원형 틀로 직접 그렸다.
//
// 얼굴은 currentColor 로만 그린다 — 캐릭터마다 색을 달리하면 형광펜 네 색과
// 부딪힌다. 사람은 무채색, 강조는 형광펜. 색이 뜻을 갖는 자리는 한 곳뿐이다.
//
// mood 는 셋뿐이다: 기본 · 맞음 · 틀림. 표정을 늘리면 데이터가 그것을 지정해야
// 하는데 논점 878개에 표정 정보가 없다. 지금 아는 사실로만 표정을 바꾼다.

const R = 1.6;   // 선 굵기 — lucide 1.75 와 같은 계열
const V = 44;    // viewBox 한 변

/** 눈 한 쌍. shape 로 눈매를 바꾼다. */
function Eyes({ shape }) {
  if (shape === 'closed') {
    return (
      <>
        <path d="M14 20 q2.4 2 4.8 0" />
        <path d="M25.2 20 q2.4 2 4.8 0" />
      </>
    );
  }
  if (shape === 'narrow') {
    return (
      <>
        <path d="M13.6 20.4 h5.2" />
        <path d="M25.2 20.4 h5.2" />
      </>
    );
  }
  if (shape === 'wide') {
    return (
      <>
        <circle cx="16.2" cy="20" r="2.4" />
        <circle cx="27.8" cy="20" r="2.4" />
      </>
    );
  }
  return (
    <>
      <circle cx="16.2" cy="20" r="1.5" />
      <circle cx="27.8" cy="20" r="1.5" />
    </>
  );
}

/** 입. mood 가 표정을 정한다. */
function Mouth({ mood }) {
  if (mood === 'right') return <path d="M17.5 26.6 q4.5 4 9 0" />;
  if (mood === 'wrong') return <path d="M17.5 28 q4.5 -3.4 9 0" />;
  return <path d="M18.6 27.2 h6.8" />;
}

const FACE = { fill: 'none', stroke: 'currentColor', strokeWidth: R, strokeLinecap: 'round', strokeLinejoin: 'round' };

/** 묻는 이 — 머리 위에 물음표. 눈이 크고 둥글다. */
function AskFace({ mood }) {
  return (
    <g {...FACE}>
      <circle cx="22" cy="23" r="12.4" />
      <Eyes shape={mood === 'wrong' ? 'wide' : 'round'} />
      <Mouth mood={mood} />
      <path d="M18.8 7.6 q0 -3.4 3.2 -3.4 q3.2 0 3.2 2.8 q0 2.2 -3.2 3.2" />
      <path d="M22 12.2 v.2" />
    </g>
  );
}

/** 선생 — 각진 안경. 차분한 눈매. */
function TeachFace({ mood }) {
  return (
    <g {...FACE}>
      <circle cx="22" cy="23" r="12.4" />
      <rect x="12.2" y="17.2" width="8" height="5.6" rx="1.2" />
      <rect x="23.8" y="17.2" width="8" height="5.6" rx="1.2" />
      <path d="M20.2 20 h3.6" />
      <path d="M9.4 19.4 l2.8 -.9" />
      <path d="M34.6 19.4 l-2.8 -.9" />
      <Mouth mood={mood} />
    </g>
  );
}

/** 깐깐이 — 눈을 가늘게 뜨고 눈썹을 세운다. */
function GotchaFace({ mood }) {
  return (
    <g {...FACE}>
      <circle cx="22" cy="23" r="12.4" />
      <path d="M12.8 16.4 l5.6 1.8" />
      <path d="M31.2 16.4 l-5.6 1.8" />
      <Eyes shape="narrow" />
      {mood === 'wrong'
        ? <path d="M17.5 28.4 q4.5 -3.6 9 0" />
        : <path d="M17.8 27 q4.2 1.8 8.4 -.6" />}
    </g>
  );
}

/** 복습 메이트 — 강아지. 늘어진 귀. */
function MateFace({ mood }) {
  return (
    <g {...FACE}>
      <circle cx="22" cy="23.4" r="11.6" />
      <path d="M11.6 15.4 q-4.4 1.6 -3.4 7.4 q.8 4.2 4.6 4" />
      <path d="M32.4 15.4 q4.4 1.6 3.4 7.4 q-.8 4.2 -4.6 4" />
      <Eyes shape={mood === 'right' ? 'closed' : 'round'} />
      <path d="M22 25.4 q-1.4 0 -1.4 -1.2 q0 -1.2 1.4 -1.2 q1.4 0 1.4 1.2 q0 1.2 -1.4 1.2" />
      <path d="M22 25.4 v1.8" />
      {mood === 'wrong'
        ? <path d="M18.6 30 q3.4 -2.6 6.8 0" />
        : <path d="M18.6 27.4 q3.4 3 6.8 0" />}
    </g>
  );
}

const FACES = { ask: AskFace, teach: TeachFace, gotcha: GotchaFace, mate: MateFace };

/**
 * 화자 아바타.
 * @param {'ask'|'teach'|'gotcha'|'mate'} who
 * @param {'idle'|'right'|'wrong'} mood
 * @param {number} size  픽셀
 */
export default function Avatar({ who, mood = 'idle', size = 44 }) {
  const Face = FACES[who] || FACES.teach;
  return (
    <span className={`cast-avatar cast-avatar--${who}`} aria-hidden="true">
      <svg width={size} height={size} viewBox={`0 0 ${V} ${V}`} role="presentation">
        <Face mood={mood} />
      </svg>
    </span>
  );
}
