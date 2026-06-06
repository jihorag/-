#!/usr/bin/env python3
"""기출 도면/그림을 'A4 전체 가로폭 + 위아래만 정밀 크롭'으로 추출 → webp.
도면 y범위는 임베드 이미지 bbox 또는 벡터 도형 bbox로 자동 검출(추측 X).
ParsedText 규약(평탄 webp, basename .png→.webp)에 맞춰 public/images/<name>.webp 저장.

사용:
  python3 scripts/crop_figure.py <pdf> <page0base> <out_name> [y0 y1]
  - y0,y1 생략 시 자동 검출(이미지/도형 bbox)
예:
  python3 scripts/crop_figure.py "...기출문제지...pdf" 9 kichul-r1q4-fig
"""
import sys, fitz
from pathlib import Path
from PIL import Image
import io

OUT_DIR = Path('viewer/public/images')


def figure_yrange(page):
    """페이지에서 도면 y범위 자동 검출 — 임베드 이미지 우선, 없으면 벡터 도형."""
    r = page.rect
    ys = []
    for im in page.get_images(full=True):
        for bb in page.get_image_rects(im[0]):
            if bb.height < r.height * 0.95:  # 페이지 전체 배경 제외
                ys += [bb.y0, bb.y1]
    if not ys:
        for d in page.get_drawings():
            b = d['rect']
            if 0 < b.height < r.height * 0.95 and 0 < b.width < r.width * 0.99:
                ys += [b.y0, b.y1]
    if not ys:
        return None
    return min(ys), max(ys)


def crop(pdf, page0, name, y0=None, y1=None, pad=8, dpi=150):
    doc = fitz.open(pdf)
    pg = doc[page0]
    r = pg.rect
    if y0 is None or y1 is None:
        yr = figure_yrange(pg)
        if not yr:
            print('!! 도면 y범위 검출 실패 — y0 y1 수동 지정 필요'); return
        y0, y1 = yr
    clip = fitz.Rect(r.x0, max(r.y0, y0 - pad), r.x1, min(r.y1, y1 + pad))  # 가로 전체, 위아래만
    pix = pg.get_pixmap(dpi=dpi, clip=clip)
    img = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f'{name}.webp'
    img.save(out, 'WEBP', quality=88)
    print(f'크롭 → {out}  ({img.width}x{img.height})  y[{y0:.0f}~{y1:.0f}] 가로전체')


if __name__ == '__main__':
    a = sys.argv[1:]
    pdf, page0, name = a[0], int(a[1]), a[2]
    y0 = float(a[3]) if len(a) > 3 else None
    y1 = float(a[4]) if len(a) > 4 else None
    crop(pdf, page0, name, y0, y1)
