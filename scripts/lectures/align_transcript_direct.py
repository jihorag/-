#!/usr/bin/env python3
"""필기노트가 없는 과목용 — 전사본을 관(leaf)에 **직접** 정렬한다.

경제학은 강사 필기노트 PDF(229쪽, 텍스트 레이어 있음)가 있어서
"필기 쪽 → 관" 을 먼저 풀고 거기에 전사를 얹었다. 다른 과목은 그 사다리가 없다.
  · 부동산학원론: 빵구노트 43쪽·수업자료 1~2쪽뿐, 본교재(이종호 400쪽)는 스캔본이라 텍스트 없음
  · 감정평가관계법규: 강의자료 자체가 없음

대신 부동산은 **파일명에 편·장이 그대로 적혀 있다**(`제1편 제3장 03. 공동주택과 단독주택`).
taxonomy 의 `PART 01 / Chapter 03` 과 번호가 그대로 대응하므로, 이걸로 후보 관을
한 챕터로 좁힌 뒤 전사 내용으로 관을 고른다. 후보가 3개 내외로 줄어 정확도가 크게 오른다.

장 표기가 없는 강의는 직전 강의가 있던 챕터부터 뒤쪽 전체를 후보로 둔다(강의는 교재 순서대로 간다).

산출: lectures/align.json — 경제학과 같은 형식(by_lecture / by_leaf)

사용:
  python3 scripts/lectures/align_transcript_direct.py realestate --phase basic
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import STUDY, WORK  # noqa: E402
from map_notes_to_leaves import tfidf_vectors, cosine, monotonic_assign  # noqa: E402

WINDOW_SEC = 120
TITLE_TOPK = 8       # 제목 유사도 상위 몇 개를 후보에 넣을지
WINDOW_LEAVES = 12   # 직전 강의 위치부터 앞으로 몇 관까지를 후보로 볼지
PAGE_BAND_RATIO = 0.12  # 면수로 짚은 위치 앞뒤로 전체 관의 몇 %를 후보로 둘지
MIN_BAND_CAND = 4       # 밴드 안 후보가 이보다 적으면 밴드 전체를 후보로 쓴다

# 면수 밴드를 **쓸 과목**. 재보고 정했다.
#   civil·law·accounting  편→PART 신호가 없거나 맞지 않는다. 대신 파일명 면수가 강사
#                         본교재의 전 범위를 덮는다(민법 2~408, 법규 10~441, 회계 1~587).
#                         민법에서 10면짜리 강의가 저당권에, 85면짜리가 취득시효에 붙던 것이 고쳐졌다.
#   realestate·economics  편↔PART 가 정확해 후보가 이미 3개 안팎이다. 게다가 이쪽 '면수'는
#                         본교재가 아니라 빵구노트(43쪽)·수업자료 쪽수라 위치를 잘못 짚는다.
#                         실제로 밴드를 켜니 제목 일치가 73%→63% 로 떨어져 끄기로 했다.
USE_PAGE_BAND = {'civil', 'law', 'accounting'}


def chunk_transcript(segments, window=WINDOW_SEC):
    if not segments:
        return []
    out, cur, start = [], [], segments[0]['start']
    for s in segments:
        if s['start'] - start >= window and cur:
            out.append({'start': round(start, 1), 'end': round(cur[-1]['end'], 1),
                        'text': ' '.join(x['text'] for x in cur)})
            cur, start = [], s['start']
        cur.append(s)
    if cur:
        out.append({'start': round(start, 1), 'end': round(cur[-1]['end'], 1),
                    'text': ' '.join(x['text'] for x in cur)})
    return out


def load_leaves(subject):
    """관 목록 + 각 관의 교재 본문(내용 매칭용) + PART/Chapter 번호."""
    base = STUDY / subject
    idx = json.loads((base / 'ai_taxonomy_index.json').read_text(encoding='utf-8'))
    leaves = idx['leaves'] if isinstance(idx, dict) else idx
    cache = {}
    out = []
    for lf in leaves:
        body = ''
        uf, sl = lf.get('unit_file'), lf.get('section_lines')
        if uf:
            if uf not in cache:
                p = base / uf
                cache[uf] = p.read_text(encoding='utf-8').split('\n') if p.exists() else []
            lines = cache[uf]
            body = '\n'.join(lines[max(0, sl[0] - 1):min(len(lines), sl[1])]) if sl else '\n'.join(lines)
        path = lf.get('path', [])
        joined = ' '.join(path)
        part = re.search(r'PART\s*(\d+)', joined)
        chap = re.search(r'Chapter\s*(\d+)', joined)
        out.append({
            'leaf': lf,
            'root': path[0] if path else '',
            'part': int(part.group(1)) if part else None,
            'chapter': int(chap.group(1)) if chap else None,
            'chapter_key': (int(part.group(1)) if part else 0,
                            int(chap.group(1)) if chap else 0),
            # 제목은 짧아도 판별력이 크므로 반복해 가중
            'doc': (joined + ' ') * 3 + body[:6000],
        })

    # taxonomy 의 Chapter 번호는 **PART 마다 01 로 리셋**된다(01-01 … 09-06, 총 40개).
    # 그런데 강의 파일명은 「제55장」처럼 **전 과목 연속 번호**를 쓴다(2~57).
    # 그래서 (PART, Chapter) 조합에 등장 순서대로 연속 번호를 매겨 파일명 번호와 맞춘다.
    order, seq = {}, 0
    for l in out:
        k = l['chapter_key']
        if k not in order:
            seq += 1
            order[k] = seq
        l['chapter_seq'] = order[k]
    return out


# 과목별로 **어떤 신호가 실제로 맞는지** 다르다. 안 맞는 신호를 쓰면 조용히 어긋난다.
#
#   realestate  파일명의 편 ↔ taxonomy PART 가 정확히 대응 (검증됨, 33%→80%)
#   economics   〃
#   law         편 번호가 **맞지 않는다**. 강사마다 교재가 달라 도승하 제1편=공간정보(PART 04),
#               김희상 제4편=국토계획(PART 01) 식이다. 대신 파일명에 법률 이름이 들어 있으므로
#               법률명 → PART 로 좁힌다.
#   civil       편 표기가 아예 없다(0/66강). 제목 유사도 + 단조 창에 맡긴다.
#   accounting  편 표기는 있으나 taxonomy 대분류와 번호가 대응하지 않는다. 위와 같다.
PYEON_IS_PART = {'realestate', 'economics'}

# 법규 — 파일명의 법률 이름으로 PART 를 특정한다.
LAW_PART_HINTS = {
    1: r'국토|광역도시|도시.?군\s*(기본|관리)|용도지역|지구단위|개발행위|기반시설|도시계획시설',
    2: r'건축',
    3: r'정비사업|재개발|재건축|주거환경|도시.?및.?주거',
    4: r'공간정보|지적|측량|토지의?\s*표시|지적공부|등록사항',
    5: r'등기',
    6: r'국유재산|행정재산|일반재산',
    7: r'공시지가|가격공시|주택가격|표준지|개별공시',
    8: r'감정평가|평가사|징계|과징금|권리와\s*의무|자격',
    9: r'동산|채권.?담보',
}


# 한 과목 안에서 **강좌마다 다루는 교재 대분류가 갈리는** 경우.
#
# 회계는 재무회계 강좌(63강)와 원가회계 강좌(21강)가 서로 다른 책을 나간다. 그런데 교재의
# 관 이름은 겹친다(재고자산·원가배부 등). 단조 DP 는 한 번 앞으로 간 뒤 되돌아오지 못하므로,
# 원가 강의가 재무회계 관에 한 번 붙으면 그 뒤가 통째로 밀린다.
# 그래서 강좌가 다룰 대분류를 못박아 후보에서 아예 뺀다.
COURSE_ROOTS = {
    'accounting': [
        ('원가회계', {'원가관리회계'}),
        ('재무회계', {'재무회계', '회계원리', '고급회계'}),
    ],
}


def allowed_indices(subject, course, leaves):
    """이 강좌가 건드려도 되는 관 번호. 제한이 없으면 None."""
    for key, roots in COURSE_ROOTS.get(subject, []):
        if key in (course or ''):
            idxs = [i for i, l in enumerate(leaves) if l['root'] in roots]
            return set(idxs) if idxs else None
    return None


def part_from_title(subject, title):
    """파일명에서 taxonomy PART 번호를 뽑는다. 못 뽑으면 None."""
    t = title or ''
    if subject in PYEON_IS_PART:
        m = re.search(r'제\s*(\d+)\s*편', t)
        return int(m.group(1)) if m else None
    if subject == 'law':
        hits = [p for p, rx in LAW_PART_HINTS.items() if re.search(rx, t)]
        # 두 법률이 함께 걸리면 어느 쪽인지 단정할 수 없다 — 좁히지 않는다.
        return hits[0] if len(hits) == 1 else None
    return None


def page_band(page, page_lo, page_hi, order):
    """강의 파일명의 **교재 면수**로 후보 구간을 짚는다.

    파일명에는 그날 나간 교재 쪽이 거의 다 적혀 있다(민법 63/66, 법규 74/75, 회계 84/84).
    교재를 앞에서 뒤로 순서대로 나가므로, 면수는 곧 **교재 안에서의 위치**다.
    쪽 수 자체를 관에 대응시킬 수는 없지만(강사 교재와 앱 교재가 다른 책이다),
    "교재의 몇 %쯤" 이라는 비율은 그대로 쓸 수 있다.

    이게 없으면 제목이 모호한 강의(「노트 7번」, 「Ⅴ. 원물과 과실」)에서 유사도가
    엉뚱하게 멀리 있는 관을 집어온다 — 실제로 10면짜리 강의가 저당권에,
    85면짜리가 취득시효에 붙었다. 둘 다 교재 훨씬 뒤쪽이다.
    """
    if page is None or page_hi <= page_lo or not order:
        return None
    rel = (page - page_lo) / (page_hi - page_lo)
    center = round(rel * (len(order) - 1))
    w = max(10, round(len(order) * PAGE_BAND_RATIO))
    return {order[i] for i in range(max(0, center - w), min(len(order), center + w + 1))}


def candidates_for(subject, title, leaves, last_idx, title_rank=None, allow=None, band=None):
    """후보 관을 좁힌다. 여러 신호를 **합집합**으로 쓴다.

    ① 면수 밴드 — 교재 안 위치. 신뢰도가 가장 높아 다른 신호를 이 안으로 가둔다.
    ② PART 신호 — `part_from_title` (과목에 따라 편 번호 또는 법률명)
    ③ 제목 유사도 — 파일명에 관 이름이 그대로 있는 경우가 많다
       (「제4관 저당권의 처분 및 소멸」처럼 taxonomy 관 제목과 사실상 같다).
    ④ 단조 창 — 강의는 교재 순서를 따라가므로 직전 위치 뒤쪽

    좁히기는 어디까지나 **후보 축소**다. 최종 선택은 전사 내용 유사도 + 단조 DP 가 한다.
    그래서 하나가 빗나가도 나머지가 받쳐 준다 — 교집합으로 쓰면 하나만 틀려도 무너진다.
    다만 면수 밴드만은 예외로 **가두는** 역할을 한다. 위치는 제목보다 훨씬 잘 맞기 때문이다.
    """
    picks = set()

    pt = part_from_title(subject, title)
    if pt is not None:
        idxs = [i for i, l in enumerate(leaves) if l['part'] == pt]
        if idxs:
            # PART 경계에 걸친 강의를 위해 앞뒤로 한 관씩 여유
            picks.update(range(max(0, min(idxs) - 1), min(len(leaves) - 1, max(idxs) + 1) + 1))

    if title_rank:
        picks.update(title_rank[:TITLE_TOPK])

    start = max(0, last_idx)
    picks.update(range(start, min(len(leaves), start + WINDOW_LEAVES)))

    if band:
        # 면수 밴드는 **좁히는** 데 쓴다. 무조건 통째로 더하면 후보만 불어나 정밀도가 떨어진다.
        # (실제로 부동산은 편→PART 가 정확해 후보가 3개인데 밴드 25개를 더했더니
        #  제목 일치가 73%→61% 로 떨어졌다.)
        # 다른 신호가 밴드 안에서 충분히 후보를 냈으면 그것만 쓰고,
        # 신호가 약할 때만 밴드가 후보를 댄다 — 민법처럼 편 표기가 없는 과목이 그렇다.
        narrowed = picks & band
        picks = narrowed if len(narrowed) >= MIN_BAND_CAND else (narrowed | band)

    if allow is not None:
        picks &= allow
        if not picks:           # 좁히다 비면 허용 범위 전체로 되돌린다(빈 후보는 정렬 자체가 불가)
            picks = set(allow)
    # 단조 DP 는 후보가 관 순서대로 늘어서 있다고 전제한다.
    return sorted(picks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    # 부동산은 기초이론(선행)+기본이론이 함께 1회독이다. 쉼표로 여러 단계를 한 번에 처리한다.
    # 단계마다 따로 돌리면 align.json 을 덮어써서 앞 단계 결과가 사라진다.
    ap.add_argument('--phase', default='basic', help='쉼표로 여러 개 가능 (예: found,basic)')
    ap.add_argument('--course', help='강좌 이름 일부로 거르기 (예: 도승하) — 주강사만 쓰고 싶을 때')
    args = ap.parse_args()

    base = STUDY / args.subject / 'lectures'
    catalog = json.loads((base / 'catalog.json').read_text(encoding='utf-8'))
    leaves = load_leaves(args.subject)
    tdir = WORK / 'transcripts' / args.subject

    phases = [p.strip() for p in args.phase.split(',') if p.strip()]
    lectures = [x for x in catalog['lectures'] if x['phase'] in phases]
    if args.course:
        lectures = [x for x in lectures if args.course in (x.get('course') or '')]
        if not lectures:
            sys.exit(f'--course {args.course!r} 에 해당하는 강의가 없습니다.')

    # ⚠️ 한 과목에 **강좌가 여럿** 섞여 있다. 각 강좌는 1강부터 다시 시작한다.
    #   · 회계  재무회계 63강 + 원가회계 21강  (둘 다 1강부터)
    #   · 법규  도승하 36강 + 김희상 39강      (같은 과목을 각자 처음부터)
    # 강번호만으로 정렬하면 두 강좌가 지그재그로 섞여 "교재를 순서대로 나간다"는 전제가 깨지고,
    # 단조 DP 가 뒤로 못 돌아가는 성질 때문에 뒤쪽 강좌가 통째로 잘못된 관에 붙는다.
    # 그래서 강좌를 묶어 정렬하고, 강좌가 바뀌면 진행 위치(last_idx)를 0으로 되돌린다.
    tracks = []
    for x in lectures:
        t = x.get('course') or ''
        if t not in tracks:
            tracks.append(t)
    lectures.sort(key=lambda x: (tracks.index(x.get('course') or ''),
                                 phases.index(x['phase']), x['no'] or 0))
    if len(tracks) > 1:
        print(f'강좌 {len(tracks)}개를 각각 독립 정렬합니다:')
        for t in tracks:
            print(f"   · {t or '(이름없음)'} — {sum(1 for x in lectures if (x.get('course') or '') == t)}강")

    # 제목 ↔ 관 유사도를 **한 번에** 계산한다.
    # 강의마다 따로 돌리면 IDF(문서빈도)가 매번 달라져 순위가 들쭉날쭉해진다.
    titles = [lec.get('topic_hint') or lec['title'] or '' for lec in lectures]
    tvecs = tfidf_vectors([l['doc'] for l in leaves] + titles)
    lvecs, tvecs = tvecs[:len(leaves)], tvecs[len(leaves):]
    title_ranks = []
    for tv in tvecs:
        title_ranks.append(sorted(range(len(leaves)),
                                  key=lambda i: -cosine(tv, lvecs[i])))

    by_lecture, by_leaf = {}, defaultdict(list)
    done = skipped = 0
    last_idx = 0
    cur_track = None

    for li_lec, lec in enumerate(lectures):
        track = lec.get('course') or ''
        if track != cur_track:
            cur_track, last_idx = track, 0   # 새 강좌는 교재 처음부터 다시 나간다
            allow = allowed_indices(args.subject, track, leaves)
            if allow is not None:
                last_idx = min(allow)
                print(f'   ↳ 「{track[-14:]}」 은 관 {len(allow)}개로 제한')
            # 면수 비율은 **강좌 안에서만** 뜻이 있다. 강사·교재가 다르면 쪽 번호도 다르다.
            order = sorted(allow) if allow is not None else list(range(len(leaves)))
            pgs = [x['book_pages'][0] for x in lectures
                   if (x.get('course') or '') == track and x.get('book_pages')]
            page_lo, page_hi = (min(pgs), max(pgs)) if pgs else (None, None)
        tf = tdir / f"{lec['id']}.json"
        if not tf.exists():
            skipped += 1
            continue
        chunks = chunk_transcript(json.loads(tf.read_text(encoding='utf-8')).get('segments', []))
        if not chunks:
            skipped += 1
            continue

        pg = lec['book_pages'][0] if lec.get('book_pages') else None
        band = (page_band(pg, page_lo, page_hi, order)
                if args.subject in USE_PAGE_BAND else None)
        cand = candidates_for(args.subject, lec.get('topic_hint') or lec['title'],
                              leaves, last_idx, title_ranks[li_lec], allow, band)
        vecs = tfidf_vectors([c['text'] for c in chunks] + [leaves[i]['doc'] for i in cand])
        cv, lv = vecs[:len(chunks)], vecs[len(chunks):]
        rows = [[cosine(cv[i], lv[j]) for j in range(len(cand))] for i in range(len(chunks))]
        path = monotonic_assign(rows, len(cand))

        spans = []
        for i, c in enumerate(chunks):
            li = cand[path[i]]
            lf = leaves[li]['leaf']
            spans.append({'start': c['start'], 'end': c['end'],
                          'ts': f"{int(c['start'])//60}:{int(c['start'])%60:02d}",
                          'leaf_id': lf['id'], 'score': round(rows[i][path[i]], 4)})
            by_leaf[lf['id']].append({'lecture_id': lec['id'], 'no': lec['no'],
                                      'start': c['start'], 'end': c['end'],
                                      'ts': spans[-1]['ts'], 'page': None})
        last_idx = cand[path[-1]]
        by_lecture[lec['id']] = {'no': lec['no'], 'title': lec['title'], 'phase': lec['phase'],
                                 'candidates': len(cand), 'window_sec': WINDOW_SEC, 'spans': spans}
        done += 1

    dst = base / 'align.json'
    dst.write_text(json.dumps({
        'subject': args.subject, 'phase': phases, 'window_sec': WINDOW_SEC,
        'method': '파일명 편·장으로 후보 축소 + 한글 2-gram TF-IDF + 단조 DP',
        'lectures_aligned': done, 'lectures_skipped': skipped,
        'by_lecture': by_lecture, 'by_leaf': {k: v for k, v in sorted(by_leaf.items())},
    }, ensure_ascii=False, indent=1), encoding='utf-8')

    print(f'정렬 {done}강 · 건너뜀 {skipped}강')
    print(f'관 {len(by_leaf)}개 / 전체 {len(leaves)}개에 강의 구간이 붙음')
    if by_lecture:
        avg = sum(v['candidates'] for v in by_lecture.values()) / len(by_lecture)
        print(f'강의당 평균 후보 관 {avg:.1f}개')
    print(f'저장: {dst}')


if __name__ == '__main__':
    main()
