#!/usr/bin/env python3
"""
ai_taxonomy_index.json / ai_index.json 의 section_lines 를 더 좁은 윈도우로 narrow.

목적: leaf 한 개당 평균 17K 토큰 → 3K 토큰 수준으로 축소 (API 비용 ~50% 추가 절감).

전략:
1. 현재 section_lines 범위 내에서 leaf path 마지막 토큰 키워드 검색
2. 첫 등장 위치 기준 ±N 라인 윈도우 (앞 20, 뒤 230 = 약 250라인 ≈ 7.5KB ≈ 3K 토큰)
3. 같은 키워드가 절·관 marker 옆에 있는 라인을 우선 선택 (실제 헤딩일 확률 높음)
4. 키워드 못 찾으면 현재 범위 첫 250라인으로 fallback
5. 이미 250라인 미만이면 그대로 보존
"""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDY = os.path.join(ROOT, 'viewer/public/data/study')

# 슬라이스 윈도우 — 키워드 기준 앞/뒤 라인 수
# handover.md 가 매 요청에 cached 로 제공되어 일반 교습법·과목 맥락은 그쪽이 담당.
# section 은 leaf-specific 디테일만 좁게 — 평균 1.5K 토큰 ≒ 130라인.
WIN_BEFORE = 10
WIN_AFTER  = 120
MAX_WIN    = 140   # 절대 상한 (handover 활용으로 더 좁게 가능)
MIN_KEEP   = 40    # 이미 이보다 짧으면 보존

# 정규화: 제N장/절/관/편/Chapter/PART 등 접두 제거
_PREFIX = re.compile(r'^(제\d+(장|절|관|편)|Chapter\s*\d+|PART\s*\d+|\([0-9]+\))\s+')
_BRACKETS = re.compile(r'[\[\]\(\)\{\}「」『』""""]')

def normalize(s: str) -> str:
    if not s: return ''
    s = re.sub(r'<a\s+name="[^"]+"\s*>\s*</a>', '', s)
    s = _PREFIX.sub('', s).strip()
    s = _BRACKETS.sub('', s)
    s = re.sub(r'\s+', '', s)
    return s

# 절·관·항 marker 패턴 — 본문에서 헤딩성 라인 식별
_HEADING_HINT = re.compile(r'(제\s*\d+\s*(절|관|항|장)|^\s*\d+\.\s|^\s*##+\s|⑴|⑵|⑶|⑷|⑸|⑹|⑺|⑻|⑼|⑽)')

_UNIT_CACHE = {}
def load_unit(path):
    if path in _UNIT_CACHE: return _UNIT_CACHE[path]
    if not os.path.exists(path):
        _UNIT_CACHE[path] = None
        return None
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    _UNIT_CACHE[path] = lines
    return lines


def find_keyword_window(lines, range_start, range_end, keyword):
    """범위 내에서 keyword 가 등장하는 best line 찾기.
    헤딩성 라인(절/관/숫자.) 부근의 등장을 우선."""
    if not keyword or len(keyword) < 2: return None
    rs = max(1, range_start)
    re_ = min(len(lines), range_end)
    norm_kw = normalize(keyword)
    if not norm_kw: return None
    # 1차: 정확히 keyword 가 헤딩성 라인 부근 (±2)에 있는 첫 위치
    best = None
    for i in range(rs - 1, re_):
        line = lines[i]
        if normalize(line).find(norm_kw) >= 0:
            # heading hint 가 ±2 라인 내에 있는가?
            window = ''.join(lines[max(0, i-1):i+2])
            is_heading_area = bool(_HEADING_HINT.search(window))
            if is_heading_area and best is None:
                best = i + 1
                break
            if best is None:
                best = i + 1
    return best


def narrow_section(leaf_or_topic, unit_lines):
    """단일 leaf/topic 의 section_lines 를 좁힘. 원본 변경하지 않고 새 [s, e] 반환."""
    cur_lines = leaf_or_topic.get('section_lines')
    if not cur_lines or not unit_lines:
        return cur_lines
    cur_s, cur_e = cur_lines
    cur_e = min(cur_e, len(unit_lines))
    cur_s = max(1, cur_s)
    cur_span = cur_e - cur_s + 1
    # 이미 충분히 좁으면 그대로
    if cur_span <= MIN_KEEP:
        return cur_lines
    # leaf path 의 후미 토큰부터 시도
    path = leaf_or_topic.get('path') or []
    title = leaf_or_topic.get('title') or ''
    candidates = []
    for p in reversed(path):
        candidates.append(p)
    if title: candidates.append(title)
    # 정규식·괄호·접두 제거 + 핵심 명사 추출 (마지막 토큰의 마지막 단어)
    extra = []
    for c in list(candidates):
        c_norm = _PREFIX.sub('', c).strip()
        # 공백으로 split 한 뒤 마지막 의미 단어 (2자 이상)
        toks = re.split(r'[\s·,/\-—]+', c_norm)
        for t in toks:
            t = _BRACKETS.sub('', t).strip()
            if len(t) >= 2 and t not in extra:
                extra.append(t)
    candidates = extra + candidates
    found = None
    matched_kw = None
    for kw in candidates:
        pos = find_keyword_window(unit_lines, cur_s, cur_e, kw)
        if pos:
            found = pos
            matched_kw = kw
            break
    if found:
        new_s = max(cur_s, found - WIN_BEFORE)
        new_e = min(cur_e, found + WIN_AFTER)
        # 상한 캡
        if new_e - new_s + 1 > MAX_WIN:
            new_e = new_s + MAX_WIN - 1
        return [new_s, new_e]
    # 키워드 못 찾음 — 현재 범위 시작 ~ 최대 280라인
    return [cur_s, min(cur_e, cur_s + MAX_WIN - 1)]


def narrow_subject(subject_id, index_path):
    if not os.path.exists(index_path):
        print(f'  ✗ index 없음: {index_path}')
        return
    with open(index_path, encoding='utf-8') as f:
        idx = json.load(f)
    base = os.path.join(STUDY, subject_id)
    # 1차/2차 구조 분기
    stage = 1
    leaves = idx.get('leaves')
    if not leaves and 'units' in idx:
        stage = 2

    changed = 0
    total = 0
    before_sum = 0
    after_sum = 0

    def process(leaf_or_topic):
        nonlocal changed, total, before_sum, after_sum
        uf = leaf_or_topic.get('unit_file')
        if not uf:
            return
        unit_path = os.path.join(base, uf)
        unit_lines = load_unit(unit_path)
        if not unit_lines:
            return
        old = leaf_or_topic.get('section_lines')
        new = narrow_section(leaf_or_topic, unit_lines)
        if not new:
            return
        total += 1
        if old:
            old_s, old_e = old
            old_e = min(old_e, len(unit_lines))
            old_byte = sum(len(unit_lines[i].encode()) for i in range(max(0, old_s-1), min(len(unit_lines), old_e)))
            before_sum += old_byte
        new_byte = sum(len(unit_lines[i].encode()) for i in range(max(0, new[0]-1), min(len(unit_lines), new[1])))
        after_sum += new_byte
        if new != old:
            leaf_or_topic['section_lines'] = new
            leaf_or_topic['section_key'] = (leaf_or_topic.get('section_key') or 'auto') + '_narrow'
            changed += 1

    if stage == 1:
        for l in leaves:
            process(l)
    else:
        for u in idx['units']:
            for t in (u.get('topics') or []):
                # topic 에 unit_file 가 없으니 unit 의 unit_file 주입
                t.setdefault('unit_file', u.get('unit_file'))
                process(t)
            # 단원 자체 leaf (topics 없을 때 unit 자체) — title 만 있으므로 path 추정
            if not u.get('topics'):
                process({**u, 'path': [u.get('title','')]})

    avg_before = before_sum / max(1, total)
    avg_after = after_sum / max(1, total)
    drop = 100 * (1 - avg_after / max(1, avg_before)) if avg_before else 0
    print(f'  [{subject_id}] {changed}/{total} narrowed | avg {int(avg_before):,}B → {int(avg_after):,}B ({drop:.1f}% drop) | ~{int(avg_after/3):,} tok')

    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else [
        ('civil',              'ai_taxonomy_index.json'),
        ('economics',          'ai_taxonomy_index.json'),
        ('law',                'ai_taxonomy_index.json'),
        ('realestate',         'ai_taxonomy_index.json'),
        ('accounting',         'ai_taxonomy_index.json'),
        ('appraisal_practice', 'ai_index.json'),
        ('appraisal_theory',   'ai_index.json'),
        ('appraisal_law',      'ai_index.json'),
    ]
    print('narrowing section_lines...')
    for sid, fname in targets:
        narrow_subject(sid, os.path.join(STUDY, sid, fname))
    print('done.')


if __name__ == '__main__':
    main()
