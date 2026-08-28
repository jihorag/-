#!/usr/bin/env python3
"""LLM이 임의로 적었거나 오수집된 '비정상 정답'을 정답 없음으로 되돌린다.

판정: answer 가 단일 1~5 / 단일 ①~⑤ / (콤마·공백 구분) 전부 1~5 또는 ①~⑤(복수·전항정답)
      → 정상(보존). 그 외 전부 INVALID(예: 0,6~9, 'null','N/A','정답','해당 없음',
      '…추론할 수 없습니다' 같은 LLM 거절/필러 문구) → answer='' 로 비움.
정상 1~5 단일값은 절대 건드리지 않는다(출처 마커가 없어 LLM/원본 구분 불가하므로 안전 우선).
원값은 data_quality.answer_removed 에 보존(되돌리기 가능).

사용:
  python3 pipeline/6_db_utils/blank_invalid_answers.py --dry-run
  python3 pipeline/6_db_utils/blank_invalid_answers.py --sync
"""
import json
import re
import sys
import shutil
import collections
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "questions_db.json"
BACKUP_DIR = ROOT / "pipeline/6_db_utils" / "backup"
CIRC = "①②③④⑤"


def is_valid(a):
    s = str(a).strip()
    if s == "" or s.lower() in ("none", "null"):
        return None  # 이미 정답 없음(처리 대상 아님)
    if len(s) == 1 and (s in "12345" or s in CIRC):
        return True
    toks = [t.strip() for t in re.split(r"[,\s]+", s) if t.strip()]
    if toks and (all(t in "12345" for t in toks) or all(t in CIRC for t in toks)):
        return True  # 복수정답/전항정답
    return False


def main():
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    dry = "--dry-run" in flags

    qs = json.loads(DB.read_text(encoding="utf-8"))
    targets = [q for q in qs if is_valid(q.get("answer")) is False]
    dist = collections.Counter(str(q.get("answer")).strip() for q in targets)
    print(f"INVALID(비정상 정답 → 정답 없음) 대상: {len(targets)}건")
    for v, n in dist.most_common(30):
        print(f"  {n:>3}  {v[:70]!r}")

    if dry:
        print("--dry-run: 파일 미수정")
        return
    if not targets:
        print("대상 없음 — 변경 없음")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = BACKUP_DIR / f"questions_db.pre_blankinvalid_{ts}.json"
    shutil.copy2(DB, bak)

    now = datetime.now().astimezone().isoformat()
    for q in targets:
        orig = q.get("answer")
        q["answer"] = ""
        dq = q.setdefault("data_quality", {})
        dq["no_answer"] = True
        dq["answer_removed"] = {
            "orig": orig,
            "reason": "llm_or_miscollected_invalid",
            "at": now,
        }
        # 잘못 채워졌던 출처 태그가 있으면 제거
        for k in ("answer_source", "answer_filled_at", "answer_key_file"):
            dq.pop(k, None)

    DB.write_text(json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"백업: {bak.relative_to(ROOT)}")
    print(f"저장: questions_db.json ({len(targets)}건 정답 없음 처리)")

    if "--sync" in flags:
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scratch" / "sync_db.py")], check=True)
        print("앱 DB 동기화 완료")
    else:
        print("앱 반영하려면: python3 scratch/sync_db.py")


if __name__ == "__main__":
    main()
