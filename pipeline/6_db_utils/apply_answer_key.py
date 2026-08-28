#!/usr/bin/env python3
"""공식 정답표 → questions_db.json 정밀 주입.

검증된 '공식' 답안만 채운다. LLM 추정/제3자 미검증 값은 넣지 않는다(오답 주입 방지).
- 입력: TSV(탭 구분). 컬럼: exam, year, number, answer [, subject]
  · 헤더 줄 있어도 됨(첫 줄에 'exam'/'number' 포함 시 무시)
  · subject 컬럼은 선택(있으면 부분일치까지 매칭 보조에만 사용, 매칭 키 아님)
  · answer 는 1~5 정수(원문자 ①~⑤ / "정답 3" 형태도 허용 → 숫자만 추출)
- 매칭 키: (exam, year, number)  ← 공식표가 이 단위로 발표되므로 본문 안 읽어도 정확
- 기본은 '정답 비어있는 문항'만 채움. 이미 답 있는 건 건드리지 않음(--force 로 덮어쓰기 허용)
- 루트 questions_db.json 백업 후 수정. 끝에 --sync 주면 scratch/sync_db.py 실행.

사용:
  python3 pipeline/6_db_utils/apply_answer_key.py pipeline/6_db_utils/answer_keys/감정평가사_2026.tsv [--sync] [--force] [--dry-run]
"""
import json
import re
import sys
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "questions_db.json"
BACKUP_DIR = ROOT / "pipeline/6_db_utils" / "backup"


def norm_answer(raw):
    """'③', '정답: 3', ' 3 ' → '3'. 1~5 아니면 None."""
    if raw is None:
        return None
    s = str(raw).strip()
    circ = "①②③④⑤⑥⑦⑧⑨"
    for i, c in enumerate(circ, 1):
        if c in s:
            return str(i) if 1 <= i <= 5 else None
    m = re.search(r"[1-5]", s)
    return m.group(0) if m else None


def parse_key(path):
    rows = []
    for ln, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split("\t")]
        low = [p.lower() for p in parts]
        if ln == 1 and ("exam" in low or "number" in low):
            continue  # 헤더
        if len(parts) < 4:
            print(f"  [무시] {ln}행 컬럼 부족: {line!r}")
            continue
        exam, year, number, answer = parts[0], parts[1], parts[2], parts[3]
        subject = parts[4] if len(parts) >= 5 else None
        a = norm_answer(answer)
        if a is None:
            print(f"  [무시] {ln}행 답 비유효(1~5 아님): {line!r}")
            continue
        rows.append({"exam": exam, "year": str(year), "number": str(number),
                     "answer": a, "subject": subject})
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        print(__doc__)
        sys.exit(1)
    key_path = args[0]
    force = "--force" in flags
    dry = "--dry-run" in flags
    source = "official"
    for a in sys.argv[1:]:
        if a.startswith("--source="):
            source = a.split("=", 1)[1]

    keyrows = parse_key(key_path)
    print(f"정답표 유효 행: {len(keyrows)}")
    if not keyrows:
        sys.exit(1)

    qs = json.loads(DB.read_text(encoding="utf-8"))
    index = {}
    for q in qs:
        index.setdefault((str(q.get("exam")), str(q.get("year")), str(q.get("number"))), []).append(q)

    filled = skipped_has = unmatched = ambiguous = conflict = 0
    now = datetime.now(timezone.utc).isoformat()
    for r in keyrows:
        cand = index.get((r["exam"], r["year"], r["number"]), [])
        if not cand:
            unmatched += 1
            print(f"  [미매칭] {r['exam']} {r['year']} {r['number']}번")
            continue
        if r["subject"]:
            narrowed = [q for q in cand if r["subject"] in str(q.get("subject", ""))]
            if narrowed:
                cand = narrowed
        if len(cand) > 1:
            ambiguous += 1
            print(f"  [모호-건너뜀] {r['exam']} {r['year']} {r['number']}번 → {len(cand)}건(과목 미지정?)")
            continue
        q = cand[0]
        cur = str(q.get("answer") or "").strip()
        if cur and not force:
            if norm_answer(cur) != r["answer"]:
                conflict += 1
                print(f"  [충돌-보존] {r['exam']} {r['year']} {r['number']}번 기존={cur} 표={r['answer']} (--force 시 덮어씀)")
            else:
                skipped_has += 1
            continue
        if not dry:
            q["answer"] = r["answer"]
            dq = q.setdefault("data_quality", {})
            dq["answer_source"] = source
            dq["answer_filled_at"] = now
            dq["answer_key_file"] = Path(key_path).name
        filled += 1

    print(f"\n채움 {filled} · 이미있어건너뜀 {skipped_has} · 충돌보존 {conflict} "
          f"· 모호건너뜀 {ambiguous} · 미매칭 {unmatched}")

    if dry:
        print("--dry-run: 파일 미수정")
        return
    if filled == 0:
        print("변경 없음 — 백업/저장 생략")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = BACKUP_DIR / f"questions_db.pre_answerkey_{ts}.json"
    shutil.copy2(DB, bak)
    DB.write_text(json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"백업: {bak.relative_to(ROOT)}\n저장: questions_db.json")

    if "--sync" in flags:
        print("sync_db 실행…")
        subprocess.run([sys.executable, str(ROOT / "scratch" / "sync_db.py")], check=True)
        print("앱 DB 동기화 완료")
    else:
        print("앱 반영하려면: python3 scratch/sync_db.py")


if __name__ == "__main__":
    main()
