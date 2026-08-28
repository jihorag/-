#!/usr/bin/env python3
"""관(leaf) 하나의 압축 재료를 한 덩어리로 모은다 — ⑦ 필기 압축의 입력.

모으는 것:
  1) 필기노트 쪽 텍스트   — 강사가 화면에 띄운 문서 원본 (골격)
  2) 강의 구간 전사       — 그 쪽을 설명하며 실제로 한 말
  3) 판서 키프레임 목록   — 그 구간에 손으로 더한 것 (⑤ 판독 대상)

관 하나가 여러 강의에 흩어져 있을 수 있으므로 강의·시각 순으로 정렬해 붙인다.

사용:
  python3 scripts/lectures/build_note_bundle.py economics --top 5      # 큰 관 5개 미리보기
  python3 scripts/lectures/build_note_bundle.py economics --leaf <id> --out bundle.json
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from map_notes_to_leaves import extract_note_pages  # noqa: E402

from _paths import STUDY, WORK

DEFAULT_PDF = ('/Volumes/WD_Black/인터넷강의/감정평가사 인터넷강의/1차_경제학/손병익/'
               '[2026_기본이론] 경제학원론 (25년 7-8월:손병익)/강의자료/'
               '경제학+필기+노트/경제학 필기 노트_10판.pdf')


def merge_spans(spans, gap=180):
    """같은 강의 안에서 이어지는 구간을 합친다(사이가 gap초 이내면 한 덩어리)."""
    out = []
    for s in sorted(spans, key=lambda x: (x['lecture_id'], x['start'])):
        if out and out[-1]['lecture_id'] == s['lecture_id'] and s['start'] - out[-1]['end'] <= gap:
            out[-1]['end'] = max(out[-1]['end'], s['end'])
            out[-1]['pages'] = sorted(set(out[-1]['pages'] + [s['page']]))
        else:
            out.append({'lecture_id': s['lecture_id'], 'no': s['no'],
                        'start': s['start'], 'end': s['end'], 'pages': [s['page']]})
    return out


def build(subject, leaf_id, pages_text, note_map, align, transcripts_dir, keyframes_dir):
    leaf_pages = note_map['by_leaf'].get(leaf_id, {}).get('pages', [])
    spans = merge_spans(align['by_leaf'].get(leaf_id, []))

    # 이 관을 다루는 leaf 정보
    info = next((p['dp'] for p in note_map['pages'] if p['dp']['leaf_id'] == leaf_id), None)

    lecture_blocks = []
    for sp in spans:
        tf = transcripts_dir / f"{sp['lecture_id']}.json"
        if not tf.exists():
            continue
        tr = json.loads(tf.read_text(encoding='utf-8'))
        text = ' '.join(s['text'] for s in tr['segments']
                        if sp['start'] <= s['start'] < sp['end'])
        # 이 구간에 걸친 판서 키프레임
        kf_idx = keyframes_dir / sp['lecture_id'] / 'index.json'
        frames = []
        if kf_idx.exists():
            ki = json.loads(kf_idx.read_text(encoding='utf-8'))
            frames = [{'ts': f['ts'], 'file': str(keyframes_dir / sp['lecture_id'] / f['file'])}
                      for f in ki['frames'] if sp['start'] <= f['t'] < sp['end']]
        lecture_blocks.append({
            'lecture_id': sp['lecture_id'], 'no': sp['no'],
            'ts': f"{int(sp['start']) // 60}:{int(sp['start']) % 60:02d}"
                  f"~{int(sp['end']) // 60}:{int(sp['end']) % 60:02d}",
            'minutes': round((sp['end'] - sp['start']) / 60, 1),
            'note_pages': sp['pages'],
            'transcript': text,
            'frames': frames,
        })

    return {
        'leaf_id': leaf_id,
        'unit_code': info['unit_code'] if info else None,
        'path': info['path'] if info else [],
        'note_pages': leaf_pages,
        'note_text': '\n\n'.join(f"[필기노트 {p}쪽]\n{pages_text.get(p, '')}" for p in leaf_pages),
        'lectures': lecture_blocks,
        'total_minutes': round(sum(b['minutes'] for b in lecture_blocks), 1),
        'total_chars': sum(len(b['transcript']) for b in lecture_blocks),
        'total_frames': sum(len(b['frames']) for b in lecture_blocks),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--pdf', default=DEFAULT_PDF)
    ap.add_argument('--leaf')
    ap.add_argument('--top', type=int, help='분량 큰 관 N개 요약 출력')
    ap.add_argument('--out')
    args = ap.parse_args()

    base = STUDY / args.subject / 'lectures'
    note_map = json.loads((base / 'note_map.json').read_text(encoding='utf-8'))
    align = json.loads((base / 'align.json').read_text(encoding='utf-8'))
    pages = extract_note_pages(args.pdf)
    pages_text = {p['page']: p['text'] for p in pages}

    tdir = WORK / 'transcripts' / args.subject
    kdir = WORK / 'keyframes' / args.subject

    if args.top:
        rows = []
        for lid in align['by_leaf']:
            b = build(args.subject, lid, pages_text, note_map, align, tdir, kdir)
            rows.append(b)
        rows.sort(key=lambda x: -x['total_chars'])
        print(f"{'관':<46}{'강의':>5}{'분':>6}{'전사자':>8}{'판서':>6}{'필기쪽':>7}")
        for b in rows[:args.top]:
            name = (b['path'][-1] if b['path'] else b['leaf_id'])[:44]
            print(f"{name:<46}{len(b['lectures']):>5}{b['total_minutes']:>6.0f}"
                  f"{b['total_chars']:>8,}{b['total_frames']:>6}{len(b['note_pages']):>7}")
        chars = [b['total_chars'] for b in rows]
        chars.sort()
        print(f"\n관 {len(rows)}개 · 전사 중앙값 {chars[len(chars) // 2]:,}자 · "
              f"평균 {sum(chars) // len(chars):,}자 · 최대 {chars[-1]:,}자")
        return

    if not args.leaf:
        sys.exit('--leaf 또는 --top 중 하나가 필요합니다.')
    b = build(args.subject, args.leaf, pages_text, note_map, align, tdir, kdir)
    if args.out:
        Path(args.out).write_text(json.dumps(b, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f"저장: {args.out}")
    print(f"{' / '.join(b['path'])}")
    print(f"필기 {len(b['note_pages'])}쪽 · 강의 {len(b['lectures'])}개 구간 · "
          f"{b['total_minutes']}분 · 전사 {b['total_chars']:,}자 · 판서 {b['total_frames']}장")


if __name__ == '__main__':
    main()
