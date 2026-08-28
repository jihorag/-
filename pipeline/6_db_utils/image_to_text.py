#!/usr/bin/env python3
"""이미지로 박제된 '텍스트 전용' 문항 본문을 추출 텍스트로 치환.

표·그래프·도형·필수수식 그림은 대상 아님(호출자가 TEXT_ONLY로 판정한 것만 입력).
안전 규율(정답 보정과 동일):
- 대상 필드(question)가 '이미지뿐'일 때만 치환(--force로 완화). 일반 텍스트 섞인 건 건드리지 않음.
- 원본 이미지 파일명을 data_quality.orig_image 에 보존(롤백·폴백 가능).
- data_quality.image_extracted = source 라벨, image_extracted_at = ts.
- 루트 questions_db.json 백업 후 수정. --sync 시 scratch/sync_db.py 실행. --dry-run 지원.

입력 TSV(탭): qid <TAB> text         (qid = questions_db 의 id)
  · text 안의 줄바꿈은 리터럴 '\\n' 으로. 빈 text 행은 무시.

사용:
  python3 pipeline/6_db_utils/image_to_text.py keys.tsv --source=pilot_vision [--dry-run] [--sync] [--force]
"""
import json
import re
import sys
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "questions_db.json"
BACKUP_DIR = ROOT / "pipeline/6_db_utils" / "backup"
IMG_RE = re.compile(r"\[IMAGE:\s*([^\]]+)\]")


def parse_keys(path):
    rows = []
    for ln, line in enumerate(Path(path).read_text(encoding="utf-8").split("\n"), 1):
        if not line.strip():
            continue
        if "\t" not in line:
            print(f"  [무시] {ln}행 탭 없음")
            continue
        parts = line.split("\t")
        qid = parts[0].strip()
        text = parts[1].replace("\\n", "\n").strip() if len(parts) > 1 else ""
        # 3번째 필드(선택): 보기. ' ||| ' 로 구분
        opts = None
        if len(parts) > 2 and parts[2].strip():
            opts = [o.strip() for o in parts[2].split(" ||| ") if o.strip()]
        if not qid or not text:
            print(f"  [무시] {ln}행 qid/text 비어있음")
            continue
        rows.append((qid, text, opts))
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        print(__doc__)
        sys.exit(1)
    force = "--force" in flags
    dry = "--dry-run" in flags
    source = "image_extracted"
    for a in sys.argv[1:]:
        if a.startswith("--source="):
            source = a.split("=", 1)[1]

    keys = parse_keys(args[0])
    print(f"입력 {len(keys)}건")
    qs = json.loads(DB.read_text(encoding="utf-8"))
    by_id = {str(q.get("id")): q for q in qs}

    done = skip_notimg = skip_noid = conflict = kept = 0
    now = datetime.now().astimezone().isoformat()
    for qid, text, opts in keys:
        q = by_id.get(qid)
        if q is None:
            skip_noid += 1
            print(f"  [미매칭] id={qid}")
            continue
        body = str(q.get("question") or "")
        imgs = IMG_RE.findall(body)
        body_wo = IMG_RE.sub("", body).strip()
        is_img_only = bool(imgs) and len(body_wo) <= 3
        if not is_img_only and not force:
            skip_notimg += 1
            print(f"  [건너뜀-이미지전용아님] id={qid} body={body[:40]!r}")
            continue
        dq = q.setdefault("data_quality", {})
        if (dq.get("image_extracted") or dq.get("image_kept")) and not force:
            conflict += 1
            continue
        # 표/그래프/도형 — 텍스트화 불가, 이미지 유지로 표시(재집계 제외)
        if text == "__FIGURE__":
            if not dry:
                dq["image_kept"] = source
                dq["image_kept_at"] = now
            kept += 1
            continue
        if not dry:
            dq["orig_image"] = imgs[0] if imgs else None
            dq["orig_question"] = body
            dq["image_extracted"] = source
            dq["image_extracted_at"] = now
            q["question"] = text
            # 보기가 비어 있고(또는 --force) opts 주어지면 options 복원
            if opts and (not q.get("options") or force):
                dq["orig_options"] = q.get("options")
                q["options"] = opts
        done += 1

    print(f"\n치환 {done} · 도형유지 {kept} · 이미지전용아님 {skip_notimg} · 미매칭 {skip_noid} · 이미처리 {conflict}")
    if dry:
        print("--dry-run: 파일 미수정")
        return
    if done == 0 and kept == 0:
        print("변경 없음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = BACKUP_DIR / f"questions_db.pre_img2txt_{ts}.json"
    shutil.copy2(DB, bak)
    DB.write_text(json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"백업: {bak.relative_to(ROOT)}\n저장: questions_db.json ({done}건)")
    if "--sync" in flags:
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scratch" / "sync_db.py")], check=True)
        print("앱 DB 동기화 완료")
    else:
        print("앱 반영: python3 scratch/sync_db.py")


if __name__ == "__main__":
    main()
