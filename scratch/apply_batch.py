"""Merge Claude classifications into questions_db.json (atomic, validated, resumable).
Reads scratch/batch_results.json: list of
  {id, in_scope(bool), difficulty(int 1-5), mapped_taxonomy(obj|null), reason(str), flags(list?)}
Writes indexing_v4 onto matching questions and appends to the progress log.
Usage: python3 scratch/apply_batch.py
"""
import json, os, sys, time, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE, "questions_db.json")
RESULTS = os.path.join(BASE, "scratch/batch_results.json")
PROGRESS = os.path.join(BASE, "scratch/claude_index_progress.json")
PROC_BY = "claude-sonnet-4-6"
TAX_KEYS = {"subject", "sub_subject", "chapter", "section", "item"}


def safe_load(path, tries=20):
    for _ in range(tries):
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            time.sleep(0.5)
    sys.exit("could not read " + path)


def validate(r):
    assert isinstance(r.get("id"), str), "missing id"
    assert isinstance(r.get("in_scope"), bool), f"{r['id']}: in_scope must be bool"
    assert r.get("difficulty") in (1, 2, 3, 4, 5), f"{r['id']}: difficulty 1-5"
    assert isinstance(r.get("reason"), str) and r["reason"].strip(), f"{r['id']}: reason required"
    mt = r.get("mapped_taxonomy")
    if r["in_scope"]:
        assert isinstance(mt, dict) and TAX_KEYS.issubset(mt), f"{r['id']}: in_scope needs full mapped_taxonomy"
    else:
        assert mt in (None, {}), f"{r['id']}: out-of-scope must have mapped_taxonomy null"


def main():
    results = json.load(open(RESULTS))
    for r in results:
        validate(r)
    db = safe_load(DB)
    by_id = {q["id"]: q for q in db}
    applied = []
    for r in results:
        q = by_id.get(r["id"])
        if q is None:
            print("WARN id not found:", r["id"]); continue
        q["indexing_v4"] = {
            "difficulty": r["difficulty"],
            "in_scope": r["in_scope"],
            "mapped_taxonomy": r["mapped_taxonomy"] if r["in_scope"] else None,
            "needs_higher_ai": False,
            "reason": r["reason"],
            "flags": r.get("flags", []),
            "processed_by": PROC_BY,
        }
        q["indexing_v4_count"] = q.get("indexing_v4_count", 0) + 1
        applied.append({"id": r["id"], "in_scope": r["in_scope"],
                         "exam": q.get("exam"), "ts": time.strftime("%Y-%m-%dT%H:%M:%S")})

    fd, tmp = tempfile.mkstemp(dir=BASE, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DB)

    log = json.load(open(PROGRESS)) if os.path.exists(PROGRESS) else []
    log.extend(applied)
    json.dump(log, open(PROGRESS, "w"), ensure_ascii=False, indent=2)

    ins = sum(1 for a in applied if a["in_scope"])
    print(f"applied={len(applied)} in_scope={ins} out={len(applied)-ins} | progress_total={len(log)}")


if __name__ == "__main__":
    main()
