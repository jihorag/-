// 관 안의 상단 3탭 — 시안 316:3 의 tabs.
// 탭 전환은 관을 벗어나지 않는다. 같은 관의 다른 트랙으로 갈아 끼울 뿐이다.
export const TABS = [
  { key: 'concept', label: '개념 완성' },
  { key: 'exam', label: '기출 분석' },
  { key: 'deep', label: '심화' },
];

export default function ConceptTabs({ tab, onPick, right, hide = [] }) {
  const shown = TABS.filter((t) => !hide.includes(t.key));
  return (
    <div className="ctabs" role="tablist" aria-label="학습 방식">
      {shown.map((t) => (
        <button type="button" key={t.key} role="tab"
          aria-selected={tab === t.key}
          className={`ctab${tab === t.key ? ' is-on' : ''}`}
          onClick={() => onPick(t.key)}>
          {t.label}
        </button>
      ))}
      {right && <span className="ctabs-right">{right}</span>}
    </div>
  );
}
