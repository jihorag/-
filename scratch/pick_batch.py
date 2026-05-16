"""Resumable batch picker for Claude-driven image classification.
Usage: python3 scratch/pick_batch.py <EXAM> <N>
Writes scratch/batch_current.json with the next N unclassified image-questions
for <EXAM>, resolving each [IMAGE:] tag to an actual file under images/.
"""
import json, os, re, sys, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE, "questions_db.json")
IMG_DIR = os.path.join(BASE, "images")


def safe_load(path, tries=20):
    for _ in range(tries):
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            time.sleep(0.5)
    sys.exit("could not read " + path)


def is_done(q):
    iv = q.get("indexing_v4")
    return isinstance(iv, dict) and q.get("indexing_v4_count", 0) >= 1 and (
        iv.get("in_scope") is not None or iv.get("mapped_taxonomy")
    )


def resolve_image(tag):
    name = tag.strip().replace("./", "")
    if name.startswith("images/"):
        name = name[len("images/"):]
    p = os.path.join(IMG_DIR, name)
    return p if os.path.exists(p) else None


def main():
    exam, n = sys.argv[1], int(sys.argv[2])
    db = safe_load(DB)
    todo = [q for q in db if q.get("exam") == exam and not is_done(q)]
    batch = todo[:n]
    out = []
    for q in batch:
        tags = re.findall(r"\[IMAGE:\s*(.*?)\]", (q.get("question", "") or "") + (q.get("explanation", "") or ""))
        imgs = [resolve_image(t) for t in tags]
        out.append({
            "id": q["id"],
            "subject": q.get("subject"),
            "year": q.get("year"),
            "image_paths": [i for i in imgs if i],
            "missing_images": [t for t, i in zip(tags, imgs) if not i],
            "options": q.get("options"),
        })
    json.dump(out, open(os.path.join(BASE, "scratch/batch_current.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"exam={exam} remaining_todo={len(todo)} picked={len(out)}")
    miss = sum(1 for o in out if o["missing_images"])
    print(f"questions with unresolved image: {miss}")
    print("first ids:", [o["id"] for o in out[:5]])


if __name__ == "__main__":
    main()
