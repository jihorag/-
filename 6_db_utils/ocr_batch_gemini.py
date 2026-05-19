#!/usr/bin/env python3
"""본문-이미지-전용 문항을 Gemini 비전으로 전량 텍스트화(무인 배치).

규율은 image_to_text.py와 동일:
- question 이 '이미지뿐'인 문항만 대상. 이미 image_extracted 면 건너뜀(재개 가능·멱등).
- 모델이 도형/표/그래프로 판정(__FIGURE__)하면 이미지 유지 + data_quality.image_kept 태깅(다시 안 물음).
- 텍스트로 판정되면 충실 전사: 수식 $...$, 줄바꿈 보존. question 치환 +
  data_quality.orig_image/orig_question 보존(롤백) + image_extracted='gemini:<model>'.
- N건마다 체크포인트 저장(중단/쿼터 안전). 시작 시 1회 백업. --sync 시 sync_db.

환경: GEMINI_API_KEY 필요.
사용:
  python3 6_db_utils/ocr_batch_gemini.py [--limit 200] [--dry-run] [--sync] [--model gemini-2.0-flash]
"""
import json
import os
import re
import sys
import time
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "questions_db.json"
IMG_DIRS = [ROOT / "images", ROOT / "viewer" / "public" / "images"]
BACKUP_DIR = ROOT / "6_db_utils" / "backup"
IMG_RE = re.compile(r"\[IMAGE:\s*([^\]]+)\]")
CKPT_EVERY = 25

PROMPT = (
    "다음은 한국 전문자격 시험(회계사·세무사·감정평가사·보험계리사) 문제의 '문제 본문' 이미지다.\n"
    "규칙:\n"
    "1) 표·그래프·도표·그림·도형 등 텍스트로 옮길 수 없는 시각요소가 본질이면, 다른 말 없이 정확히 __FIGURE__ 만 출력.\n"
    "2) 순수 텍스트(지문·ㄱ/ㄴ/ㄷ 항목·수식 포함)면 보이는 그대로 충실히 전사. "
    "수식/기호는 LaTeX로 $...$ 안에. 줄바꿈은 실제 줄바꿈으로. "
    "머리말·해설·추가설명 금지, 이미지에 없는 내용 추가 금지, 보기(①②③④⑤)는 본문에 있을 때만 포함.\n"
    "출력은 전사 텍스트(또는 __FIGURE__) 그 자체만."
)


def find_image(name):
    base = name.split("/")[-1].strip()
    cands = [base]
    if base.lower().endswith((".png", ".gif")):
        cands.append(re.sub(r"\.(png|gif)$", ".webp", base, flags=re.I))
    for d in IMG_DIRS:
        for c in cands:
            p = d / c
            if p.exists():
                return p
    return None


def main():
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    dry = "--dry-run" in flags
    limit = None
    model_name = "gemini-2.0-flash"
    for a in sys.argv[1:]:
        if a.startswith("--limit"):
            limit = int(a.split("=")[1]) if "=" in a else int(sys.argv[sys.argv.index(a) + 1])
        if a.startswith("--model="):
            model_name = a.split("=", 1)[1]

    qs = json.loads(DB.read_text(encoding="utf-8"))
    targets = []
    for q in qs:
        body = str(q.get("question") or "")
        imgs = IMG_RE.findall(body)
        if not imgs:
            continue
        if len(IMG_RE.sub("", body).strip()) > 3:
            continue
        dq = q.get("data_quality") or {}
        if dq.get("image_extracted") or dq.get("image_kept"):
            continue
        targets.append((q, imgs[0]))
    if limit:
        targets = targets[:limit]
    print(f"대상 {len(targets)}건 (model={model_name}, dry={dry})")
    if dry or not targets:
        for q, im in targets[:20]:
            print(f"  {q.get('id')}  <- {im}  ({'있음' if find_image(im) else '이미지없음'})")
        return

    import google.generativeai as genai
    key = os.environ.get("GEMINI_API_KEY")
    if not key or key == "여기에_API_키를_입력하세요":
        print("환경변수 GEMINI_API_KEY 미설정. export GEMINI_API_KEY=... 후 재실행.")
        sys.exit(1)
    genai.configure(api_key=key)
    model = genai.GenerativeModel(model_name)
    import PIL.Image

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = BACKUP_DIR / f"questions_db.pre_ocrbatch_{ts}.json"
    shutil.copy2(DB, bak)
    print(f"백업: {bak.relative_to(ROOT)}")

    now = datetime.now().astimezone().isoformat()
    conv = fig = miss = err = 0
    for i, (q, im) in enumerate(targets, 1):
        p = find_image(im)
        if not p:
            miss += 1
            continue
        try:
            img = PIL.Image.open(p)
            r = model.generate_content(
                [PROMPT, img],
                generation_config={"temperature": 0},
                request_options={"timeout": 60},
            )
            out = (r.text or "").strip()
        except Exception as e:
            err += 1
            print(f"  [오류] {q.get('id')}: {str(e)[:80]}")
            time.sleep(2)
            continue
        dq = q.setdefault("data_quality", {})
        if out == "__FIGURE__" or not out:
            dq["image_kept"] = "gemini:" + model_name
            dq["image_kept_at"] = now
            fig += 1
        else:
            dq["orig_image"] = im
            dq["orig_question"] = str(q.get("question"))
            dq["image_extracted"] = "gemini:" + model_name
            dq["image_extracted_at"] = now
            q["question"] = out
            conv += 1
        if i % CKPT_EVERY == 0:
            DB.write_text(json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  …{i}/{len(targets)} (변환 {conv} · 도형유지 {fig} · 누락 {miss} · 오류 {err})")
        time.sleep(0.5)

    DB.write_text(json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n완료: 변환 {conv} · 도형유지 {fig} · 이미지누락 {miss} · 오류 {err}")
    print(f"저장: questions_db.json (백업 {bak.name})")
    if "--sync" in flags:
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scratch" / "sync_db.py")], check=True)
        print("앱 DB 동기화 완료")
    else:
        print("앱 반영: python3 scratch/sync_db.py")


if __name__ == "__main__":
    main()
