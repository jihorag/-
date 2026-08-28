#!/usr/bin/env python3
"""전사본을 필기노트 쪽 단위로 정렬한다 → 관(leaf)별 강의 구간이 확정된다.

왜 필요한가:
  · note_map.json 은 "필기노트 쪽 → 관" 을 안다.
  · catalog.json 은 "강의 → 필기노트 쪽 범위" 를 안다(예: 2강 = 필기 3~7쪽).
  · 하지만 **강의 안에서 언제 어느 쪽을 다뤘는지**는 아무도 모른다.
    그걸 모르면 관마다 강사 설명을 잘라 올 수 없다.

방법: 전사본을 시간 창으로 자르고, 각 창을 그 강의가 다루는 필기노트 쪽들과만 비교한다
      (후보가 5쪽 내외로 좁아 정확도가 높다). 시간이 흐르면 쪽 번호도 커져야 하므로
      map_notes_to_leaves 와 같은 단조 정렬 DP를 쓴다.

산출: lectures/align.json
  · by_lecture : 강의별 [시간구간 → 쪽 → 관]
  · by_leaf    : 관별 [강의 + 시간구간] — ⑦ 필기 압축이 이걸 먹는다

사용:
  python3 scripts/lectures/align_transcript_to_notes.py economics \\
      --pdf "…/경제학 필기 노트_10판.pdf" --phase basic
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from map_notes_to_leaves import (  # noqa: E402
    extract_note_pages, candidates_for, tfidf_vectors, cosine, monotonic_assign)

from _paths import STUDY, WORK  # 산출은 PC앱으로

WINDOW_SEC = 120       # 전사본을 자를 시간 창. 필기노트 한 쪽을 설명하는 시간과 비슷한 규모.


def chunk_transcript(segments, window=WINDOW_SEC):
    """전사 구간들을 시간 창 단위로 묶는다."""
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--phase', default='basic')
    args = ap.parse_args()

    base = STUDY / args.subject
    note_map = json.loads((base / 'lectures/note_map.json').read_text(encoding='utf-8'))
    catalog = json.loads((base / 'lectures/catalog.json').read_text(encoding='utf-8'))
    page_leaf = {p['page']: p['dp'] for p in note_map['pages']}

    pages = extract_note_pages(args.pdf)
    page_text = {p['page']: p['text'] for p in pages}

    tdir = WORK / 'transcripts' / args.subject
    lectures = [x for x in catalog['lectures']
                if x['phase'] == args.phase and x.get('note_pages')]

    by_lecture, by_leaf = {}, defaultdict(list)
    done = skipped = 0

    for lec in lectures:
        tf = tdir / f"{lec['id']}.json"
        if not tf.exists():
            skipped += 1
            continue
        tr = json.loads(tf.read_text(encoding='utf-8'))
        chunks = chunk_transcript(tr.get('segments', []))
        if not chunks:
            skipped += 1
            continue

        lo, hi = min(lec['note_pages']), max(lec['note_pages'])
        # 꼬리말 번호로 후보를 찾는다(구역 무관). 파일명 면수 표기가 딱 맞지 않는 경우가 있어
        # 앞뒤로 한 쪽씩 넓힌다. 미시·거시 같은 번호가 둘 다 후보로 들어가지만
        # 내용이 전혀 달라 유사도가 알아서 가른다.
        cands = [p for p in candidates_for(pages, lo, hi, pad=1) if p in page_text]
        if not cands:
            skipped += 1
            continue

        vecs = tfidf_vectors([c['text'] for c in chunks] + [page_text[p] for p in cands])
        cv, pvv = vecs[:len(chunks)], vecs[len(chunks):]
        rows = [[cosine(cv[i], pvv[j]) for j in range(len(cands))] for i in range(len(chunks))]
        path = monotonic_assign(rows, len(cands))

        spans = []
        for i, c in enumerate(chunks):
            pg = cands[path[i]]
            leaf = page_leaf.get(pg)
            spans.append({
                'start': c['start'], 'end': c['end'],
                'ts': f"{int(c['start']) // 60}:{int(c['start']) % 60:02d}",
                'page': pg,
                'leaf_id': leaf['leaf_id'] if leaf else None,
                'score': round(rows[i][path[i]], 4),
            })
            if leaf:
                by_leaf[leaf['leaf_id']].append({
                    'lecture_id': lec['id'], 'no': lec['no'],
                    'start': c['start'], 'end': c['end'], 'ts': spans[-1]['ts'],
                    'page': pg,
                })

        by_lecture[lec['id']] = {
            'no': lec['no'], 'title': lec['title'], 'phase': lec['phase'],
            'note_pages': [lo, hi], 'window_sec': WINDOW_SEC, 'spans': spans,
        }
        done += 1

    dst = base / 'lectures/align.json'
    dst.write_text(json.dumps({
        'subject': args.subject, 'phase': args.phase,
        'window_sec': WINDOW_SEC,
        'lectures_aligned': done, 'lectures_skipped': skipped,
        'by_lecture': by_lecture,
        'by_leaf': {k: v for k, v in sorted(by_leaf.items())},
    }, ensure_ascii=False, indent=1), encoding='utf-8')

    tot_span = sum(len(v['spans']) for v in by_lecture.values())
    print(f'정렬 {done}강 · 건너뜀 {skipped}강 · 구간 {tot_span}개')
    print(f'관 {len(by_leaf)}개에 강의 구간이 붙음')
    if by_leaf:
        avg = sum(len(v) for v in by_leaf.values()) / len(by_leaf)
        mins = sum(sum(s['end'] - s['start'] for s in v) for v in by_leaf.values()) / 60
        print(f'관당 평균 {avg:.1f}구간 · 총 {mins:.0f}분 분량')
    print(f'저장: {dst}')


if __name__ == '__main__':
    main()
