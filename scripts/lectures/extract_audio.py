#!/usr/bin/env python3
"""강의 mp4 → 16kHz 모노 FLAC 추출 (Whisper 입력 규격).

작업 산출물은 전부 외장에 둔다. 저장소에는 압축된 필기 md만 커밋한다(.git이 이미 2.3GB).
중단 후 다시 돌려도 이미 만든 건 건너뛴다.

사용:
  python3 scripts/lectures/extract_audio.py economics --phase basic
  python3 scripts/lectures/extract_audio.py economics            # 과목 전체
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import require_drive, STUDY, WORK


def catalog_path(subject):
    return STUDY / subject / 'lectures/catalog.json'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--phase', help='basic/deep/prac/mock/final/intro/found 중 하나. 생략 시 전체')
    ap.add_argument('--limit', type=int, help='앞에서 N개만 (시험용)')
    args = ap.parse_args()

    require_drive()

    cp = catalog_path(args.subject)
    if not cp.exists():
        sys.exit(f'카탈로그가 없습니다: {cp}\n먼저 build_catalog.py 를 실행하세요.')
    cat = json.loads(cp.read_text(encoding='utf-8'))

    items = cat['lectures']
    if args.phase:
        items = [x for x in items if x['phase'] == args.phase]
    if args.limit:
        items = items[:args.limit]
    if not items:
        sys.exit('대상 강의가 없습니다.')

    out_dir = WORK / 'audio' / args.subject
    out_dir.mkdir(parents=True, exist_ok=True)

    total_min = sum(x['minutes'] or 0 for x in items)
    print(f"{cat['subject_ko']} · {len(items)}강 · {total_min}분 ({total_min / 60:.1f}h)")
    print(f'출력: {out_dir}\n')

    done = skipped = failed = silent = 0
    t_start = time.time()
    for i, it in enumerate(items, 1):
        dst = out_dir / f"{it['id']}.flac"
        if dst.exists() and dst.stat().st_size > 0:
            skipped += 1
            continue
        src = it['path']
        if not Path(src).exists():
            print(f"  [{i}/{len(items)}] ❌ 원본 없음: {it['id']}")
            failed += 1
            continue

        t0 = time.time()
        r = subprocess.run(
            ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src,
             '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'flac',
             '-compression_level', '8', str(dst)],
            capture_output=True, text=True)
        if r.returncode != 0:
            # 민법 '밑줄영상'처럼 **오디오 트랙이 아예 없는** 영상이 섞여 있다.
            # 교재 어디에 밑줄을 그으라고 화면으로만 보여주는 2~4분짜리라 말소리가 없다.
            # 이건 고장이 아니라 원래 그런 것이므로 실패로 세지 않는다 —
            # 실패 건수에 섞이면 진짜 문제가 묻힌다.
            dst.unlink(missing_ok=True)
            if 'does not contain any stream' in r.stderr or 'Output file #0 does not' in r.stderr:
                print(f"  [{i}/{len(items)}] ⏭  음성 없는 영상(밑줄영상 등): {it['id']}")
                silent += 1
            else:
                print(f"  [{i}/{len(items)}] ❌ 실패: {it['id']}\n     {r.stderr.strip()[:200]}")
                failed += 1
            continue

        el = time.time() - t0
        mb = dst.stat().st_size / 1e6
        done += 1
        print(f"  [{i}/{len(items)}] {it['id']} {it['minutes']}분 → {mb:.0f}MB ({el:.0f}초)")

    el = time.time() - t_start
    print(f'\n완료 {done} · 건너뜀 {skipped} · 음성없음 {silent} · 실패 {failed} · 소요 {el / 60:.1f}분')
    if done:
        size = sum(f.stat().st_size for f in out_dir.glob('*.flac')) / 1e9
        print(f'오디오 총 {size:.1f}GB')


if __name__ == '__main__':
    main()
