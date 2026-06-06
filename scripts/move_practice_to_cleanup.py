#!/usr/bin/env python3
"""실무 연습문제(practice-set) 전부를 단원에서 분리 → 정리(triage).
 · 각 단원 JSON은 official(기출)만 남김. (내가 출제한 2a-generated.json은 불변)
 · 연습문제 triage:
     - 정크2(템플릿 '[논점] #N의 의의와 적용…') 신호 2+  → 폐기(_discarded 백업)
     - 그 외(진짜 약술)                                  → 'cleanup.json'(🧹 정리중)에 적재(보강 대기)
 · manifest 갱신: 각 단원 count=기출(+generated), '정리중' 단원 추가, total 재합산.
이후 정리중 단원의 문항을 하나씩 보강/바꿈/복귀시키는 작업을 이어간다.
"""
import json, glob, re, datetime
from pathlib import Path

DATA = Path('viewer/public/data/essay/practice')
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()


def level_from_points(p):
    p = p or 0
    if p >= 40: return 5
    if p >= 25: return 4
    if p >= 15: return 3
    if p >= 8:  return 2
    return 1


def junk2_score(q):
    """대량 템플릿('[논점] #N…/감정평가의 핵심 요소/깨진 조사/고정날짜') 신호 개수."""
    t = (q.get('body', '') or '') + ' ' + (q.get('modelAnswer', '') or '')
    s = 0
    if re.search(r'#\s?\d', t): s += 1
    if re.search(r'[가-힣]\((는|은|를|을|가|이)\)', t): s += 1
    if '2026.5.29' in t or '2026. 5. 29' in t: s += 1
    if '감정평가의 핵심 요소' in t or '감정평가의 핵심이다' in t or '정의·적용 원칙·산정' in t: s += 1
    if 'K씨는' in (q.get('body', '') or '') and '검토한다' in (q.get('body', '') or ''): s += 1
    return s


def main():
    keepers, discarded = [], []
    chapter_official = {}  # {id: official_count}

    for f in sorted(DATA.glob('*.json')):
        if f.name == 'manifest.json' or 'generated' in f.name or f.name in ('cleanup.json', '_discarded_practice.json'):
            continue
        d = json.loads(f.read_text(encoding='utf-8'))
        chid = d.get('chapter') or f.stem
        official, ps = [], []
        for q in d.get('questions', []):
            (official if q.get('source') == 'official' else ps).append(q)
        # 단원에는 기출만 남김
        d['questions'] = official
        d['count'] = len(official)
        d['withAnswer'] = sum(1 for q in official if q.get('modelAnswer'))
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
        chapter_official[chid] = len(official)
        # 연습문제 triage
        for q in ps:
            if junk2_score(q) >= 2:
                discarded.append({'id': q.get('id'), 'origChapter': chid, 'reason': 'template_junk2',
                                  'body': q.get('body', '')[:80]})
            else:
                q2 = dict(q)
                q2['origChapter'] = chid
                q2['level'] = level_from_points(q.get('points'))
                q2['reviewStatus'] = '검토중'
                keepers.append(q2)

    # 정리중 단원 파일
    (DATA / 'cleanup.json').write_text(json.dumps({
        'built_at': NOW, 'chapter': 'cleanup', 'chapterTitle': '🧹 정리중 (보강 대기)',
        'count': len(keepers), 'withAnswer': sum(1 for q in keepers if q.get('modelAnswer')),
        'rounds': [], 'questions': keepers,
    }, ensure_ascii=False, indent=1), encoding='utf-8')

    # 폐기 백업(append)
    df = DATA / '_discarded_practice.json'
    prev = json.loads(df.read_text(encoding='utf-8')) if df.exists() else {'count': 0, 'items': []}
    prev_items = prev.get('items', [])
    df.write_text(json.dumps({
        'count': len(prev_items) + len(discarded),
        'note': '메타-fluff(이전) + 템플릿 정크2(이번)',
        'items': prev_items + discarded,
    }, ensure_ascii=False, indent=1), encoding='utf-8')

    # manifest 갱신
    mf = DATA / 'manifest.json'
    m = json.loads(mf.read_text(encoding='utf-8'))
    for ch in m.get('chapters', []):
        cid = ch.get('id')
        if cid in chapter_official:
            ch['count'] = chapter_official[cid] + ch.get('generatedCount', 0)
    # 정리중 단원 추가(중복 방지)
    if not any(ch.get('id') == 'cleanup' for ch in m.get('chapters', [])):
        m.setdefault('chapters', []).append({
            'id': 'cleanup', 'title': '🧹 정리중 (보강 대기)', 'file': 'cleanup.json',
            'count': len(keepers), 'withAnswer': 0, 'matchedAnswer': 0, 'rounds': [],
            'generatedCount': 0, 'subchapters': []})
    else:
        for ch in m['chapters']:
            if ch.get('id') == 'cleanup':
                ch['count'] = len(keepers)
    m['total'] = sum(ch.get('count', 0) for ch in m.get('chapters', []))
    m['cleanup_moved_at'] = NOW
    mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

    print(f"연습문제 정리: 폐기(템플릿 정크) {len(discarded)} / 정리중 적재 {len(keepers)}")
    print(f"각 단원은 기출만 남음. manifest total={m['total']}")


if __name__ == '__main__':
    main()
