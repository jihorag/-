"""Sync the canonical root data into the viewer app so the deployed UI sees
the latest classifications.

Copies (atomically):
  questions_db.json   -> viewer/public/data/questions_db.json
  taxonomy_v4.json    -> viewer/public/data/taxonomy.json

Prints an indexed-count diff so a stale viewer copy is obvious.
Called automatically at the end of scratch/apply_batch.py; also runnable
standalone:  python3 scratch/sync_db.py
"""
import json, os, sys, tempfile, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAIRS = [
    ("questions_db.json", "viewer/public/data/questions_db.json"),
    ("taxonomy_v4.json", "viewer/public/data/taxonomy.json"),
]


def indexed_count(path):
    try:
        db = json.load(open(path))
    except (OSError, ValueError):
        return None
    if not isinstance(db, list):
        return None
    return sum(1 for q in db if q.get("indexing_v4_count", 0) >= 1), len(db)


def atomic_copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(dst), suffix=".tmp")
    os.close(fd)
    shutil.copyfile(src, tmp)
    os.replace(tmp, dst)


def main():
    changed = False
    for rel_src, rel_dst in PAIRS:
        src, dst = os.path.join(BASE, rel_src), os.path.join(BASE, rel_dst)
        if not os.path.exists(src):
            sys.exit(f"missing source: {src}")
        before = indexed_count(dst) if os.path.exists(dst) else None
        atomic_copy(src, dst)
        after = indexed_count(dst)
        if rel_src.endswith("questions_db.json"):
            b = f"{before[0]}/{before[1]}" if before else "—"
            a = f"{after[0]}/{after[1]}" if after else "—"
            print(f"synced {rel_dst}: indexed {b} -> {a}")
            if before and before != after:
                changed = True
        else:
            print(f"synced {rel_dst}")
    if changed:
        print("NOTE: viewer data updated. Rebuild/redeploy to refresh dist/.")


if __name__ == "__main__":
    main()
