#!/usr/bin/env python3
"""강의 영상 → 판서 완성 시점의 키프레임.

화면 구조(경제학 기본이론 기준 실측):
  · 왼쪽 약 75% = 교재 PDF 스크롤 + 색깔 손글씨 판서, 오른쪽 약 25% = 강사
  · 교재 페이지 번호가 화면에 그대로 찍힌다 → 강의 시각 ↔ 교재 면 매핑에 쓸 수 있다
  · 판서는 누적되므로 "페이지가 넘어가기 직전" 프레임이 완성본이다

그래서 장면 전환을 찾은 뒤 그 **직전** 프레임을 뜬다. 전환 순간을 뜨면 이미 지워진 뒤라
빈 페이지가 찍힌다.

강사 영역은 잘라낸다 — VLM 입력 토큰을 줄이고 판독 정확도를 높인다.

사용:
  python3 scripts/lectures/extract_keyframes.py economics --phase basic --limit 3
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import require_drive, STUDY, WORK

# 크롭은 과목별로만 건다. 레이아웃이 강사마다 완전히 다르기 때문이다(실측):
#   경제학  판서 왼쪽 전체·강사 오른쪽 옆   → 왼쪽 75% 크롭 안전
#   법규    슬라이드 왼쪽 80%·강사 오른쪽   → 왼쪽 82% 크롭 안전
#   부동산  슬라이드+판서가 화면 전체, 강사가 화면 안 → 크롭 금지
#   민법    초록 칠판, 강사가 판서 영역 안에 서 있음  → 크롭 금지
#   회계    문제는 왼쪽·판서는 **오른쪽 45%**        → 크롭하면 판서가 통째로 사라짐
# 기본값은 크롭 없음(안전). 해상도도 1920x810/820/1080으로 제각각이라 고정 픽셀값은 못 쓴다.
SUBJECT_CROP = {
    'economics': 'iw*0.75:ih:0:0',
    'law': 'iw*0.82:ih:0:0',
}
# 장면 전환 임계값도 과목마다 다르다(실측). 슬라이드를 넘기는 강의는 전환이 뚜렷하지만,
# 칠판에 손으로 쌓아가는 강의(민법)는 변화가 완만해 같은 임계값이면 프레임이 거의 안 잡힌다.
SUBJECT_SCENE_TH = {
    'economics': 0.06,
}
SCENE_TH = 0.02         # 기본값 — 전환은 보조 신호라 낮게 두고 폭넓게 받는다
CLUSTER_SEC = 3.0       # 전환 1회가 연속 프레임 여러 개로 잡히므로 묶는다
BACKOFF_SEC = 1.2       # 전환 직전 = 판서 완성 시점
# 시간 격자 간격. 프레임 수 = 강의길이 / STEP_SEC 로 정확히 정해진다.
# 120초 → 60분 강의당 30장. 경제학 실측(27장/60분)과 같은 수준.
STEP_SEC = 120
# 크롭을 안 하면 같은 출력 폭에서 글자가 작아진다. 판독 정확도를 지키려고 폭을 키운다.
OUT_WIDTH = 1600


def scene_times(src, crop):
    """장면 전환 시각(초) 목록. 크롭·축소해서 빠르게 훑는다."""
    vf = (f'crop={crop},' if crop else '') + \
         f"scale=480:-1,select='gt(scene,{SCENE_TH})',metadata=print:file=-"
    r = subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-i', src, '-vf', vf, '-an', '-f', 'null', '-'],
        capture_output=True, text=True)
    times = []
    for line in r.stdout.splitlines():
        if 'pts_time:' in line:
            try:
                times.append(float(line.split('pts_time:')[1].split()[0]))
            except (ValueError, IndexError):
                pass
    times.sort()
    clustered = []
    for t in times:
        if not clustered or t - clustered[-1] > CLUSTER_SEC:
            clustered.append(t)
    return clustered


def frame_times(src, crop, duration_sec):
    """뽑을 시각 목록.

    장면 전환만으로는 과목을 가로질러 쓸 수 없다(실측):
      경제학 60분 74건 · 민법 51분 0건 · 회계 63분 0건.
    초록 칠판에 흰 분필이거나 슬라이드가 거의 안 바뀌면 픽셀 변화가 작아 전환이 안 잡힌다.

    그래서 **시간 격자를 기준**으로 잡고, 그 창 안에 전환이 있으면 전환 직전으로 당긴다
    (판서 완성 시점). 전환이 없으면 격자 시각을 그대로 쓴다.
    → 어떤 화면 형태에서도 강의당 프레임 수가 예측 가능하고 커버리지가 고르다.
    """
    cuts = scene_times(src, crop)
    out = []
    t = STEP_SEC
    while t < duration_sec - 3:
        window = [c for c in cuts if t - STEP_SEC < c <= t]
        out.append(max(window) - BACKOFF_SEC if window else float(t))
        t += STEP_SEC
    if duration_sec > 10:
        out.append(duration_sec - 5)     # 마지막 화면
    return sorted({round(x, 2) for x in out if x > 0})


def probe_duration(src):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', src], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def grab(src, t, dst, crop):
    vf = (f'crop={crop},' if crop else '') + f'scale={OUT_WIDTH}:-1'
    r = subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-ss', f'{t:.2f}', '-i', src,
         '-frames:v', '1', '-vf', vf, '-q:v', '4', '-y', str(dst)],
        capture_output=True, text=True)
    return r.returncode == 0 and dst.exists()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--phase')
    ap.add_argument('--limit', type=int)
    ap.add_argument('--scene-th', type=float, default=None, help='장면 전환 임계값')
    ap.add_argument('--crop', default=None,
                    help="ffmpeg crop 식. 생략하면 과목 기본값, '' 이면 크롭 안 함")
    args = ap.parse_args()

    require_drive()

    cp = STUDY / args.subject / 'lectures/catalog.json'
    if not cp.exists():
        sys.exit(f'카탈로그 없음: {cp}')
    cat = json.loads(cp.read_text(encoding='utf-8'))
    items = cat['lectures']
    if args.phase:
        items = [x for x in items if x['phase'] == args.phase]
    if args.limit:
        items = items[:args.limit]

    crop = args.crop if args.crop is not None else SUBJECT_CROP.get(args.subject, '')
    global SCENE_TH
    SCENE_TH = args.scene_th if args.scene_th is not None else \
        SUBJECT_SCENE_TH.get(args.subject, SCENE_TH)
    root = WORK / 'keyframes' / args.subject
    root.mkdir(parents=True, exist_ok=True)
    print(f"{cat['subject_ko']} · 대상 {len(items)}강 · 크롭 {crop or '없음'} · 임계 {SCENE_TH}\n")

    total_frames = 0
    t_all = time.time()
    for i, it in enumerate(items, 1):
        out_dir = root / it['id']
        idx_path = out_dir / 'index.json'
        if idx_path.exists():
            print(f"  [{i}/{len(items)}] 건너뜀 {it['id']}")
            continue
        src = it['path']
        if not Path(src).exists():
            print(f"  [{i}/{len(items)}] ❌ 원본 없음 {it['id']}")
            continue
        out_dir.mkdir(parents=True, exist_ok=True)

        t0 = time.time()
        dur = (it['minutes'] or 0) * 60 or probe_duration(src)
        frames = []
        for at in frame_times(src, crop, dur):   # backoff는 frame_times가 이미 반영
            mm, ss = divmod(int(at), 60)
            dst = out_dir / f'{mm:03d}m{ss:02d}s.jpg'
            if grab(src, at, dst, crop):
                frames.append({'t': round(at, 2), 'file': dst.name,
                               'ts': f'{mm}:{ss:02d}'})
        idx_path.write_text(json.dumps({
            'lecture_id': it['id'], 'no': it['no'], 'title': it['title'],
            'phase': it['phase'], 'book_pages': it['book_pages'],
            'scene_threshold': SCENE_TH, 'crop': crop or None,
            'out_width': OUT_WIDTH, 'step_sec': STEP_SEC,
            'duration_sec': round(dur),
            'frame_count': len(frames), 'frames': frames,
        }, ensure_ascii=False, indent=1), encoding='utf-8')

        total_frames += len(frames)
        mb = sum(f.stat().st_size for f in out_dir.glob('*.jpg')) / 1e6
        print(f"  [{i}/{len(items)}] {it['id']} {it['minutes']}분 → "
              f"{len(frames)}장 {mb:.0f}MB ({time.time() - t0:.0f}초)")

    el = time.time() - t_all
    print(f'\n총 {total_frames}장 · {el / 60:.1f}분 소요')
    if items:
        print(f'강의당 평균 {total_frames / max(1, len(items)):.0f}장')


if __name__ == '__main__':
    main()
