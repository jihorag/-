#!/usr/bin/env python3
"""실무(essay/practice) 자체제작 문제 품질 폐기.
기준 미달 정크(고신뢰)만 폐기, official 기출은 보존. 폐기분은 _discarded_practice.json 백업.
정크 신호:
 1) 깨진 모범답안 — 원문자 마커가 문장 조각마다 촘촘(중앙값 간격<9)
 2) 메타-fluff 본문 — '본 사안은…/다중 평가 방식의 종합/평가법인은 다양한 자료…' 류
 3) 대량복제 템플릿 — 본문 앞 60자가 3회+ 반복되며 '본'으로 시작(메타 양산물)
사용: python3 scripts/discard_lowquality_practice.py [--apply]
"""
import json, glob, re, sys, statistics as st, datetime
from collections import Counter
from pathlib import Path

DATA = Path('viewer/public/data/essay/practice')
APPLY = '--apply' in sys.argv

CIRC = re.compile(r'[①②③④⑤⑥⑦⑧⑨⑩]')
META = re.compile(r'본\s*사안은|본\s*고난도|본\s*응용|본\s*평가는|다중 평가 방식의 종합|'
                  r'평가법인은 다양한 자료|평가법인은 시점·지역·개별|4대\s*요인을?\s*종합|'
                  r'복잡 시나리오|다층 분쟁|고난도 (종합 )?평가 사안')


def garbled(ma):
    ma = ma or ''
    pos = [m.start() for m in CIRC.finditer(ma)]
    if len(pos) < 5:
        return False
    gaps = [pos[i + 1] - pos[i] for i in range(len(pos) - 1)]
    return st.median(gaps) < 9


def collect_dupkeys():
    pref = Counter()
    for f in DATA.glob('*.json'):
        if f.name == 'manifest.json' or 'generated' in f.name:
            continue
        for q in json.loads(f.read_text(encoding='utf-8')).get('questions', []):
            if q.get('source') != 'official':
                pref[re.sub(r'\s+', '', q.get('body', ''))[:60]] += 1
    return {k for k, c in pref.items() if c >= 3}


def is_junk(q, dupkeys):
    if q.get('source') == 'official':
        return None
    if garbled(q.get('modelAnswer')):
        return 'garbled'
    if META.search(q.get('body', '') or ''):
        return 'meta_fluff'
    bs = re.sub(r'\s+', '', q.get('body', ''))
    if bs[:60] in dupkeys and bs.startswith('본'):
        return 'dup_template'
    return None


def main():
    dupkeys = collect_dupkeys()
    discarded, reason_cnt = [], Counter()
    kept_total = 0
    chapter_updates = {}  # fname -> (kept_questions)

    for f in sorted(DATA.glob('*.json')):
        if f.name == 'manifest.json' or 'generated' in f.name:
            continue
        d = json.loads(f.read_text(encoding='utf-8'))
        kept = []
        for q in d.get('questions', []):
            r = is_junk(q, dupkeys)
            if r:
                reason_cnt[r] += 1
                discarded.append({'file': f.name, 'reason': r, 'id': q.get('id'),
                                  'difficulty': q.get('difficulty'), 'body': q.get('body', '')[:80]})
            else:
                kept.append(q)
        chapter_updates[f.name] = (d, kept)
        kept_total += len(kept)

    print(f"폐기 {len(discarded)}문 (사유: {dict(reason_cnt)})")
    print(f"보존 {kept_total}문")
    if not APPLY:
        print("\n(드라이런) 적용하려면 --apply")
        return

    # 적용: 챕터 JSON 갱신
    for fname, (d, kept) in chapter_updates.items():
        d['questions'] = kept
        d['count'] = len(kept)
        d['withAnswer'] = sum(1 for q in kept if q.get('modelAnswer'))
        (DATA / fname).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')

    # manifest 갱신 (per-chapter count/withAnswer + total)
    mf = DATA / 'manifest.json'
    m = json.loads(mf.read_text(encoding='utf-8'))
    by_file = {fn: kept for fn, (_, kept) in chapter_updates.items()}
    total = 0
    for ch in m.get('chapters', []):
        kept = by_file.get(ch.get('file'), None)
        if kept is not None:
            ch['count'] = len(kept)
            ch['withAnswer'] = sum(1 for q in kept if q.get('modelAnswer'))
            total += len(kept)
    m['total'] = total
    m['classified'] = total
    m['quality_pruned_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')

    # 백업
    (DATA / '_discarded_practice.json').write_text(
        json.dumps({'count': len(discarded), 'reasons': dict(reason_cnt), 'items': discarded},
                   ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"\n적용 완료. manifest total={total}. 백업: _discarded_practice.json")


if __name__ == '__main__':
    main()
