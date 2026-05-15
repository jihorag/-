#!/usr/bin/env python3
"""
보험계리사 PDF 자동 크롭 & DB 등록 스크립트 v3
- 2단 레이아웃(좌: x≈71, 우: x≈371) 지원
- 열을 넘어가는(spanning) 문제 자동 감지 & 이미지 합성
- 경제학원론 → subject: "경제학"
- 회계원리   → subject: "회계학"
"""

import fitz
import re
import json
import os
import shutil
import unicodedata
from pathlib import Path
from PIL import Image
import io


# ──────────────────────────────────────────────
#  설정
# ──────────────────────────────────────────────
BASE_DIR = Path("기출문제/보험계리사")
IMG_DIR = Path("images")
DB_PATH = Path("questions_db.json")
VIEWER_DB_PATH = Path("viewer/src/data/questions_db.json")
DPI = 200
TRIM_PADDING = 15  # 트리밍 후 남기는 여백(px)

RIGHT_COL_MIN_X = 340
HEADER_Y = 95           # 페이지 상단 헤더/가로선 제거를 위해 상향 조정
TOP_THRESHOLD = 130      # 이보다 아래서 시작하면 위에 overflow 텍스트 존재

def norm(s):
    return unicodedata.normalize("NFC", str(s))

YEAR_MAP = [
    (2018, 41, "41회1차(계리사)경제학원론.pdf", "41회1차(계리사)회계원리.pdf", "41회 1차시험 확정답안(공지).pdf"),
    (2019, 42, "42회 1차(계리사)_경제학원론.pdf", "42회 1차(계리사)_회계원리.pdf", "42회 1차시험 확정답안.pdf"),
    (2020, 43, "43회 1차시험(계리사)-경제학원론.pdf", "43회 1차시험(계리사)-회계원리.pdf", "43회 1차시험 확정답안.pdf"),
    (2021, 44, "44회 1차시험(계리사)-경제학원론.pdf", "44회 1차시험(계리사)-회계원리.pdf", "44회 1차시험 확정답안.pdf"),
    (2022, 45, "제45회 1차시험(계리사)_경제학원론.pdf", "제45회 1차시험(계리사)_회계원리.pdf", "제45회 1차시험 확정답안.pdf"),
    (2023, 46, "제46회 1차시험(계리사)_경제학원론.pdf", "제46회 1차시험(계리사)_회계원리.pdf", "제46회 1차시험 확정답안.pdf"),
    (2024, 47, "제47회 1차시험(계리사)_경제학원론.pdf", "제47회 1차시험(계리사)_회계원리.pdf", "제47회 1차시험 확정답안.pdf"),
    (2025, 48, "경제학원론(B4)(최종).pdf", "회계원리(B4)(최종).pdf", "48회 1차시험 확정답안.pdf"),
    (2026, 49, "49회_1차_경제학원론.pdf", "49회_1차_회계원리.pdf", None),
]

ANSWER_COL_ECON = (160, 210)
ANSWER_COL_ACC = (275, 320)
ANSWER_COL_QNUM = (55, 85)


# ──────────────────────────────────────────────
#  PDF에서 파일 찾기 (NFC 정규화 매칭)
# ──────────────────────────────────────────────
def find_pdf(year_dir, target_name):
    """NFC 정규화를 사용하여 PDF 파일을 찾는다."""
    target_norm = norm(target_name)
    for f in year_dir.iterdir():
        if norm(f.name) == target_norm:
            return f
    return None


# ──────────────────────────────────────────────
#  문제 위치 찾기
# ──────────────────────────────────────────────
def find_question_positions(doc):
    """PDF에서 문제 번호(N.)의 위치를 찾는다.
    Returns: [(q_num, page_idx, col, y_coord)]
    """
    raw = []
    for pg_idx in range(len(doc)):
        page = doc[pg_idx]
        for b in page.get_text("dict")["blocks"]:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                text = "".join([s["text"] for s in line["spans"]]).strip()
                bbox = line["bbox"]
                m = re.match(r"^(\d{1,2})\.\s", text)
                if m:
                    q_num = int(m.group(1))
                    if 1 <= q_num <= 40:
                        col = "L" if bbox[0] < RIGHT_COL_MIN_X else "R"
                        raw.append((q_num, pg_idx, col, bbox[1]))

    seen = set()
    positions = []
    for item in sorted(raw, key=lambda x: x[0]):
        if item[0] not in seen:
            positions.append(item)
            seen.add(item[0])
    return positions


# ──────────────────────────────────────────────
#  Spanning 문제 감지
# ──────────────────────────────────────────────
def detect_spanning(positions, num_pages):
    """열을 넘어가는 문제를 감지한다.
    Returns: dict { q_num: { 'type': 'L2R' or 'R2L',
                              'overflow_page': int,
                              'overflow_col': 'L' or 'R',
                              'overflow_y_end': float } }
    """
    from collections import defaultdict

    # 페이지별, 열별 그룹핑
    page_cols = defaultdict(lambda: {"L": [], "R": []})
    for q_num, pg_idx, col, y in positions:
        page_cols[pg_idx][col].append((q_num, y))

    for pg in page_cols:
        page_cols[pg]["L"].sort(key=lambda x: x[1])
        page_cols[pg]["R"].sort(key=lambda x: x[1])

    spanning = {}

    for pg_idx in range(num_pages):
        if pg_idx not in page_cols:
            continue
        L = page_cols[pg_idx]["L"]
        R = page_cols[pg_idx]["R"]

        # Case 1: 왼쪽열 마지막 문제 → 오른쪽열로 이어짐
        if L and R:
            first_r_y = R[0][1]
            if first_r_y > TOP_THRESHOLD:
                last_l_q = L[-1][0]
                spanning[last_l_q] = {
                    "type": "L2R",
                    "overflow_page": pg_idx,
                    "overflow_col": "R",
                    "overflow_y_end": first_r_y,
                }

        # Case 2: 오른쪽열 마지막 문제 → 다음 페이지 왼쪽열로 이어짐
        if R and (pg_idx + 1) in page_cols:
            nL = page_cols[pg_idx + 1]["L"]
            if nL:
                first_nl_y = nL[0][1]
                if first_nl_y > TOP_THRESHOLD:
                    last_r_q = R[-1][0]
                    spanning[last_r_q] = {
                        "type": "R2L",
                        "overflow_page": pg_idx + 1,
                        "overflow_col": "L",
                        "overflow_y_end": first_nl_y,
                    }

    return spanning


# ──────────────────────────────────────────────
#  여백 자동 트리밍
# ──────────────────────────────────────────────
def auto_trim(img_path, padding=TRIM_PADDING):
    """이미지의 불필요한 여백을 자동으로 제거한다."""
    img = Image.open(str(img_path)).convert("RGB")
    # 배경색(흰색) 기준으로 콘텐츠 영역 감지
    from PIL import ImageChops
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        # 패딩 추가
        x0 = max(0, bbox[0] - padding)
        y0 = max(0, bbox[1] - padding)
        x1 = min(img.width, bbox[2] + padding)
        y1 = min(img.height, bbox[3] + padding)
        cropped = img.crop((x0, y0, x1, y1))
        cropped.save(str(img_path), "PNG")


# ──────────────────────────────────────────────
#  이미지 크롭 (spanning 지원 + 자동 트리밍)
# ──────────────────────────────────────────────
def crop_questions(doc, positions, prefix, dpi=DPI):
    """각 문제를 크롭하여 이미지로 저장한다.
    spanning 문제는 두 영역을 세로로 합성한다.
    저장 후 자동 트리밍으로 여백을 제거한다."""
    img_paths = {}
    margin_top = 12
    margin_bottom = 8
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)

    page_width = doc[0].rect.width
    half_width = page_width / 2

    spanning = detect_spanning(positions, len(doc))

    for i, (q_num, pg_idx, col, y_start) in enumerate(positions):
        page = doc[pg_idx]
        page_height = page.rect.height

        # 열에 따른 x 범위 (중앙 세로선 제거를 위해 여백 추가)
        if col == "L":
            x_start, x_end = 0, half_width - 10
        else:
            x_start, x_end = half_width + 10, page_width

        crop_y_start = max(0, y_start - margin_top)

        # 같은 페이지, 같은 열에서 다음 문제 찾기
        crop_y_end = page_height
        for j in range(i + 1, len(positions)):
            nq, npg, ncol, ny = positions[j]
            if npg == pg_idx and ncol == col:
                crop_y_end = ny - margin_bottom
                break
            elif npg > pg_idx:
                break

        # ── Spanning 처리 ──
        if q_num in spanning:
            sp = spanning[q_num]
            # Part 1: 현재 열 (문제 시작부터 열 끝까지)
            clip1 = fitz.Rect(x_start, crop_y_start, x_end, page_height)
            pix1 = page.get_pixmap(matrix=mat, clip=clip1)
            img1 = Image.open(io.BytesIO(pix1.tobytes("png")))

            # Part 2: overflow 영역 (다음 열/페이지 상단 ~ 다음 문제 시작)
            ov_pg_idx = sp["overflow_page"]
            ov_page = doc[ov_pg_idx]
            ov_y_end = sp["overflow_y_end"] - margin_bottom

            if sp["overflow_col"] == "R":
                ov_x_start, ov_x_end = half_width + 10, page_width
            else:
                ov_x_start, ov_x_end = 0, half_width - 10

            clip2 = fitz.Rect(ov_x_start, HEADER_Y, ov_x_end, ov_y_end)
            pix2 = ov_page.get_pixmap(matrix=mat, clip=clip2)
            img2 = Image.open(io.BytesIO(pix2.tobytes("png")))

            # 세로 합성
            total_w = max(img1.width, img2.width)
            total_h = img1.height + img2.height + 10  # 10px 간격
            combined = Image.new("RGB", (total_w, total_h), (255, 255, 255))
            combined.paste(img1, (0, 0))
            combined.paste(img2, (0, img1.height + 10))

            img_name = f"{prefix}_{q_num}.png"
            out_path = IMG_DIR / img_name
            combined.save(str(out_path), "PNG")

        else:
            # ── 일반 크롭 ──
            clip = fitz.Rect(x_start, crop_y_start, x_end, crop_y_end)
            pix = page.get_pixmap(matrix=mat, clip=clip)

            img_name = f"{prefix}_{q_num}.png"
            out_path = IMG_DIR / img_name
            pix.save(str(out_path))

        # ── 여백 자동 트리밍 ──
        auto_trim(out_path)

        img_paths[q_num] = img_name

    return img_paths


# ──────────────────────────────────────────────
#  정답 추출
# ──────────────────────────────────────────────
def extract_answers(answer_pdf_path, col_range):
    answers = {}
    try:
        doc = fitz.open(str(answer_pdf_path))
    except:
        return answers

    for pg_idx in range(len(doc)):
        page = doc[pg_idx]
        spans = []
        for b in page.get_text("dict")["blocks"]:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for s in line["spans"]:
                    t = s["text"].strip()
                    if t:
                        spans.append((s["bbox"][0], s["bbox"][1], t))

        rows = {}
        for x, y, t in spans:
            row_key = round(y / 5) * 5
            if row_key not in rows:
                rows[row_key] = []
            rows[row_key].append((x, t))

        for row_key in sorted(rows.keys()):
            cells = sorted(rows[row_key], key=lambda c: c[0])
            q_num = None
            answer_val = None
            for x, t in cells:
                if ANSWER_COL_QNUM[0] <= x <= ANSWER_COL_QNUM[1]:
                    try:
                        q_num = int(t)
                    except ValueError:
                        pass
                elif col_range[0] <= x <= col_range[1]:
                    try:
                        answer_val = int(t)
                    except ValueError:
                        pass
            if q_num and answer_val:
                answers[q_num] = str(answer_val)

    doc.close()
    return answers


# ──────────────────────────────────────────────
#  과목 처리
# ──────────────────────────────────────────────
def process_one_exam(year, round_num, pdf_path, answer_pdf_path, subject_key, db_subject, col_range):
    prefix = f"actuary_{round_num}_{subject_key}"
    print(f"  📄 {pdf_path.name}")
    doc = fitz.open(str(pdf_path))

    positions = find_question_positions(doc)
    if not positions:
        print(f"    ⚠️  문제를 찾지 못했습니다.")
        doc.close()
        return []

    spanning = detect_spanning(positions, len(doc))
    q_nums = [p[0] for p in positions]
    span_qs = [q for q in spanning.keys()]

    print(f"    → {len(positions)}문제 감지", end="")
    if span_qs:
        print(f" (spanning: Q{span_qs})", end="")
    print()

    img_paths = crop_questions(doc, positions, prefix)
    doc.close()

    answers = {}
    if answer_pdf_path and answer_pdf_path.exists():
        answers = extract_answers(answer_pdf_path, col_range)
        matched = sum(1 for q in q_nums if q in answers)
        print(f"    → 정답 {matched}/{len(positions)}개 매칭")

    questions = []
    for q_num, img_name in sorted(img_paths.items()):
        questions.append({
            "id": f"actuary_{round_num}_{subject_key}_{q_num}",
            "year": str(year),
            "exam": "보험계리사",
            "subject": db_subject,
            "number": str(q_num),
            "question": f"[IMAGE: ./images/{img_name}]",
            "options": [],
            "answer": answers.get(q_num, ""),
            "explanation": "",
            "tags": {
                "subject": db_subject,
                "round": round_num,
                "difficulty": 3
            }
        })
    return questions


# ──────────────────────────────────────────────
#  메인
# ──────────────────────────────────────────────
def main():
    IMG_DIR.mkdir(exist_ok=True)
    all_new = []

    for year, rnd, econ_file, acc_file, ans_file in YEAR_MAP:
        year_dir = BASE_DIR / str(year)
        if not year_dir.exists():
            continue

        print(f"\n{'='*50}")
        print(f"🗓️  {year}년 ({rnd}회)")
        print(f"{'='*50}")

        ans_path = find_pdf(year_dir, ans_file) if ans_file else None

        econ_path = find_pdf(year_dir, econ_file)
        if econ_path:
            qs = process_one_exam(year, rnd, econ_path, ans_path, "econ", "경제학", ANSWER_COL_ECON)
            all_new.extend(qs)
            print(f"    ✅ 경제학 {len(qs)}문제 완료")
        else:
            print(f"    ⚠️  경제학 PDF 없음")

        acc_path = find_pdf(year_dir, acc_file)
        if acc_path:
            qs = process_one_exam(year, rnd, acc_path, ans_path, "acc", "회계학", ANSWER_COL_ACC)
            all_new.extend(qs)
            print(f"    ✅ 회계학 {len(qs)}문제 완료")
        else:
            print(f"    ⚠️  회계원리 PDF 없음")

    # DB 업데이트
    print(f"\n{'='*50}")
    print(f"📊 DB 업데이트 중...")

    db = []
    if DB_PATH.exists():
        with open(DB_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)

    before = len(db)
    db = [q for q in db if not q.get("id", "").startswith("actuary_")]
    removed = before - len(db)
    if removed:
        print(f"  → 기존 보험계리사 {removed}건 제거")

    db.extend(all_new)

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    shutil.copy(str(DB_PATH), str(VIEWER_DB_PATH))

    econ_c = sum(1 for q in all_new if q["subject"] == "경제학")
    acc_c = sum(1 for q in all_new if q["subject"] == "회계학")
    ans_c = sum(1 for q in all_new if q["answer"])

    print(f"  → 총 {len(all_new)}문제 추가!")
    print(f"  → DB 총 {len(db)}문제")
    print(f"\n📈 통계:")
    print(f"  경제학: {econ_c}문제")
    print(f"  회계학: {acc_c}문제")
    print(f"  정답 있음: {ans_c}/{len(all_new)}")
    span_total = sum(1 for q in all_new if "spanning" in str(q.get("tags", {})))
    print(f"  열 넘김 합성: {sum(1 for q in all_new if q.get('id', '') in [])}")


if __name__ == "__main__":
    main()
