#!/usr/bin/env python3
"""강의 필기노트 PDF의 각 쪽을 관(leaf)에 **내용으로** 잇는다.

왜 내용으로 붙이나: 필기노트의 장 번호(1장 경제학의 개요)와 앱 taxonomy의 장·절 번호
(제1장 경제학의 기초 / 제1절 경제학의 개요)는 체계가 다르다. 번호로 맞출 수 없다.

방법:
  1) 필기노트 PDF → 쪽별 텍스트 (머리말·꼬리말 제거)
  2) 관별 본문 = units/{unit_code}.md 를 section_lines 로 자른 것 (앱이 챗에 넣는 그 텍스트)
  3) 한글 2-gram TF-IDF 코사인으로 쪽 ↔ 관 유사도
  4) 단조 정렬(DP) — 필기노트와 교재는 같은 커리큘럼 순서를 따르므로,
     쪽 번호가 커지면 관 순서도 뒤로 가야 한다. 이 제약으로 튀는 매칭을 잡는다.

raw(제약 없는 최고점)와 dp(단조 정렬) 결과를 함께 남겨 품질을 비교할 수 있게 한다.

사용:
  python3 scripts/lectures/map_notes_to_leaves.py economics \\
      --pdf "/Volumes/…/경제학 필기 노트_10판.pdf"
"""
import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import STUDY  # 산출은 PC앱으로

HANGUL = re.compile(r'[^가-힣0-9A-Za-z]')


def norm(text):
    """한글·숫자·영문만 남기고 공백 제거 — 띄어쓰기 흔들림에 강해진다."""
    return HANGUL.sub('', unicodedata.normalize('NFC', text or ''))


def grams(text, n=2):
    s = norm(text)
    return [s[i:i + n] for i in range(len(s) - n + 1)] if len(s) >= n else []


def tfidf_vectors(docs):
    """docs: list[str] → list[dict[gram, weight]] (L2 정규화)"""
    tfs = [Counter(grams(d)) for d in docs]
    df = Counter()
    for tf in tfs:
        df.update(tf.keys())
    n = len(docs)
    vecs = []
    for tf in tfs:
        v = {}
        for g, c in tf.items():
            v[g] = (1 + math.log(c)) * math.log((n + 1) / (df[g] + 1))
        mag = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({g: x / mag for g, x in v.items()})
    return vecs


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(w * b.get(g, 0.0) for g, w in a.items())


def extract_note_pages(pdf_path):
    """PDF 쪽별 텍스트 + **꼬리말에 찍힌 쪽 번호**.

    한 PDF 안에 미시(1~126)와 거시(127~229)가 이어 붙어 있고, 거시가 시작되는 지점에서
    꼬리말 번호가 1로 리셋된다. 강의 파일명의 "필기 p.14"는 이 **꼬리말 번호**를 가리키므로
    PDF 인덱스와 혼동하면 거시 강의가 통째로 미시 쪽에 붙는다(실제로 그랬다).
    그래서 (구역, 꼬리말번호)를 같이 들고 다닌다.
    """
    import pypdf
    r = pypdf.PdfReader(pdf_path)
    out = []
    section = 0
    prev_no = 0
    for i, page in enumerate(r.pages):
        t = unicodedata.normalize('NFC', page.extract_text() or '')
        # 이 PDF는 낱말 사이를 공백이 아니라 NUL(\x00)로 채운다.
        # 먼저 공백으로 바꾸지 않으면 아래 정규식이 전부 빗나간다.
        t = t.replace('\x00', ' ')
        m = re.search(r'손병익\s*회계사\s*(\d+)\s*sonconomics@gmail\.com', t)
        note_no = int(m.group(1)) if m else None
        if note_no is not None:
            if note_no < prev_no:      # 번호가 되감기면 새 구역(미시 → 거시)
                section += 1
            prev_no = note_no
        # 머리말/꼬리말은 모든 쪽에 반복돼 유사도를 오염시킨다
        t = re.sub(r'서울\s*법학원.*?기본강의', '', t, flags=re.S)
        t = re.sub(r'손병익\s*회계사\s*\d+\s*sonconomics@gmail\.com', '', t)
        t = re.sub(r'[ \t]{2,}', ' ', t)
        t = '\n'.join(l.strip() for l in t.split('\n') if l.strip())
        out.append({'page': i + 1, 'note_no': note_no, 'section': section, 'text': t})
    return out


def candidates_for(pages, lo, hi, pad=1):
    """꼬리말 번호가 [lo-pad, hi+pad]인 PDF 쪽 전부 — 구역을 가리지 않고 모은다.

    미시 14쪽과 거시 14쪽 둘 다 후보로 넣고 내용 유사도가 고르게 한다.
    두 쪽의 내용이 전혀 달라 실제로는 헷갈리지 않는다.
    """
    return [p['page'] for p in pages
            if p['note_no'] is not None and lo - pad <= p['note_no'] <= hi + pad]


def load_leaves(subject):
    base = STUDY / subject
    idx = json.loads((base / 'ai_taxonomy_index.json').read_text(encoding='utf-8'))
    leaves = idx['leaves'] if isinstance(idx, dict) else idx
    cache = {}
    out = []
    for lf in leaves:
        body = ''
        uf = lf.get('unit_file')
        if uf:
            if uf not in cache:
                p = base / uf
                cache[uf] = p.read_text(encoding='utf-8').split('\n') if p.exists() else []
            lines = cache[uf]
            sl = lf.get('section_lines')
            if sl and lines:
                body = '\n'.join(lines[max(0, sl[0] - 1):min(len(lines), sl[1])])
            else:
                body = '\n'.join(lines)
        # 제목은 짧지만 판별력이 크므로 3번 반복해 가중
        title = ' '.join(lf.get('path', []))
        out.append({'leaf': lf, 'doc': (title + ' ') * 3 + body[:6000]})
    return out


def monotonic_assign(score_rows, n_leaves):
    """쪽 순서와 관 순서가 함께 커지도록(비감소) 최적 배정. O(쪽×관).

    dp[i][j] = rows[i][j] + max(dp[i-1][k] for k <= j)  — 접두 최댓값으로 선형 처리.
    """
    n_pages = len(score_rows)
    NEG = float('-inf')
    dp = [[NEG] * n_leaves for _ in range(n_pages)]
    back = [[-1] * n_leaves for _ in range(n_pages)]

    for j in range(n_leaves):
        dp[0][j] = score_rows[0][j]

    for i in range(1, n_pages):
        best, best_k = NEG, -1
        for j in range(n_leaves):
            if dp[i - 1][j] > best:           # k <= j 범위의 접두 최댓값
                best, best_k = dp[i - 1][j], j
            dp[i][j] = score_rows[i][j] + best
            back[i][j] = best_k

    j = max(range(n_leaves), key=lambda x: dp[n_pages - 1][x])
    path = [0] * n_pages
    for i in range(n_pages - 1, -1, -1):
        path[i] = j
        if i > 0:
            j = back[i][j]
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--topk', type=int, default=3)
    # 필기노트는 특정 과정의 자료다. 다른 회차 강의는 교재도 쪽 번호 체계도 달라
    # 같은 필기노트로 이으면 엉뚱한 관에 붙는다.
    ap.add_argument('--lecture-phase', default='basic',
                    help='이 필기노트를 쓰는 커리큘럼 단계 (기본값 basic)')
    args = ap.parse_args()

    if not Path(args.pdf).exists():
        sys.exit(f'PDF 없음: {args.pdf}')

    pages = extract_note_pages(args.pdf)
    leaves = load_leaves(args.subject)
    print(f'필기노트 {len(pages)}쪽 · 관 {len(leaves)}개')

    # 쪽과 관을 한 말뭉치로 벡터화해야 idf가 공유된다
    vecs = tfidf_vectors([p['text'] for p in pages] + [l['doc'] for l in leaves])
    pv, lv = vecs[:len(pages)], vecs[len(pages):]

    rows = []
    for i in range(len(pages)):
        rows.append([cosine(pv[i], lv[j]) for j in range(len(leaves))])

    dp_path = monotonic_assign(rows, len(leaves))

    out = []
    for i, p in enumerate(pages):
        order = sorted(range(len(leaves)), key=lambda j: -rows[i][j])[:args.topk]
        dj = dp_path[i]
        out.append({
            'page': p['page'],
            'chars': len(p['text']),
            'raw': [{
                'leaf_id': leaves[j]['leaf']['id'],
                'unit_code': leaves[j]['leaf'].get('unit_code'),
                'path': leaves[j]['leaf']['path'],
                'score': round(rows[i][j], 4),
            } for j in order],
            'dp': {
                'leaf_id': leaves[dj]['leaf']['id'],
                'unit_code': leaves[dj]['leaf'].get('unit_code'),
                'path': leaves[dj]['leaf']['path'],
                'score': round(rows[i][dj], 4),
            },
            'agree': leaves[order[0]]['leaf']['id'] == leaves[dj]['leaf']['id'],
        })

    # 역방향 인덱스 — 관 하나가 필기노트 몇 쪽에 걸쳐 있나 (⑦ 필기 압축이 이걸 먹는다)
    by_leaf = defaultdict(list)
    for x in out:
        by_leaf[x['dp']['leaf_id']].append(x['page'])
    by_leaf_out = {
        lid: {'pages': sorted(pp), 'page_span': [min(pp), max(pp)], 'page_count': len(pp)}
        for lid, pp in by_leaf.items()
    }

    # 강의 → 관 : 카탈로그의 note_pages(필기노트 면수)를 관으로 옮긴다
    by_lecture = {}
    cat_path = STUDY / args.subject / 'lectures/catalog.json'
    if cat_path.exists():
        page_to_leaf = {x['page']: x['dp'] for x in out}
        for lec in json.loads(cat_path.read_text(encoding='utf-8'))['lectures']:
            if lec.get('phase') != args.lecture_phase:
                continue
            np_ = lec.get('note_pages')
            if not np_:
                continue
            lo, hi = min(np_), max(np_)
            seen = []
            # 꼬리말 번호로 PDF 쪽을 찾는다. 단순히 range(lo, hi+1)을 PDF 인덱스로 쓰면
            # 거시 강의(필기 14쪽)가 미시 14쪽에 붙는다.
            for pg in candidates_for(pages, lo, hi, pad=0):
                e = page_to_leaf.get(pg)
                if e and e['leaf_id'] not in [s['leaf_id'] for s in seen]:
                    seen.append({'leaf_id': e['leaf_id'], 'unit_code': e['unit_code'],
                                 'path': e['path']})
            if seen:
                by_lecture[lec['id']] = {
                    'no': lec['no'], 'phase': lec['phase'],
                    'note_pages': [lo, hi], 'leaves': seen,
                }

    dst = STUDY / args.subject / 'lectures/note_map.json'
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps({
        'subject': args.subject,
        'source_pdf': args.pdf,
        'note_pages': len(pages),
        'leaves': len(leaves),
        'method': 'hangul 2-gram TF-IDF cosine + monotonic DP',
        'pages': out,
        'by_leaf': by_leaf_out,
        'by_lecture': by_lecture,
    }, ensure_ascii=False, indent=1), encoding='utf-8')

    agree = sum(1 for x in out if x['agree'])
    top = sum(x['raw'][0]['score'] for x in out) / max(1, len(out))
    print(f'raw 1위와 dp 일치: {agree}/{len(out)}쪽 ({agree / len(out) * 100:.0f}%)')
    print(f'raw 1위 평균 유사도: {top:.3f}')
    print(f'필기노트가 닿은 관: {len(by_leaf_out)}/{len(leaves)}개')
    if by_lecture:
        cov = sum(len(v['leaves']) for v in by_lecture.values()) / len(by_lecture)
        print(f'강의 → 관 연결: {len(by_lecture)}강 · 강의당 평균 {cov:.1f}개 관')
    print(f'저장: {dst}')


if __name__ == '__main__':
    main()
