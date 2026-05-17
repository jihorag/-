"""viewer/public/images 의 PNG를 WebP로 변환해 배포 용량을 줄인다.

- 참조 무결성: 파일명은 그대로 (foo.png -> foo.webp). questions_db 의
  [IMAGE:foo.png] 태그는 손대지 않고, 앱(ParsedText)이 .png→.webp 로
  해석하므로 데이터 변경 0.
- 멱등: 대상 .webp 가 이미 있고 원본보다 최신이면 건너뜀.
- 원본 PNG 는 저장소 루트 images/ 에 그대로 보존(되돌림 가능).

사용:
  python3 5_vision/png_to_webp.py           # 변환만
  python3 5_vision/png_to_webp.py --prune-unused   # 미참조 파일 먼저 제거
  python3 5_vision/png_to_webp.py --drop-png       # 변환 후 public 의 .png 제거

품질: cwebp -q 82 -m 6 (스캔 문서/텍스트 기준 가독성·용량 균형)
"""
import json, os, re, subprocess, sys, concurrent.futures

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(BASE, "viewer", "public", "images")
DB = os.path.join(BASE, "questions_db.json")
Q, M = "82", "6"


def referenced_names():
    db = json.load(open(DB))
    pat = re.compile(r"\[IMAGE:\s*([^\]]+)\]")
    names = set()
    for q in db:
        blob = " ".join([
            q.get("question") or "",
            " ".join(q.get("options") or q.get("choices") or []),
            q.get("explanation") or "",
        ])
        for m in pat.findall(blob):
            names.add(m.strip().split("/")[-1])
    return names


def convert_one(name):
    src = os.path.join(IMG, name)
    dst = src.rsplit(".", 1)[0] + ".webp"
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return ("skip", name)
    if name.lower().endswith(".gif"):
        cmd = ["gif2webp", "-quiet", "-q", Q, src, "-o", dst]
    else:
        cmd = ["cwebp", "-quiet", "-q", Q, "-m", M, src, "-o", dst]
    r = subprocess.run(cmd, capture_output=True)
    return ("ok" if r.returncode == 0 else "fail", name)


def main():
    args = set(sys.argv[1:])
    SRC_EXT = (".png", ".gif")
    pngs = sorted(f for f in os.listdir(IMG) if f.lower().endswith(SRC_EXT))

    if "--prune-unused" in args:
        ref = referenced_names()
        removed = 0
        for f in list(os.listdir(IMG)):
            if f not in ref and f.lower().endswith(SRC_EXT):
                os.remove(os.path.join(IMG, f)); removed += 1
        print(f"pruned unused: {removed}")
        pngs = sorted(f for f in os.listdir(IMG) if f.lower().endswith(SRC_EXT))

    stats = {"ok": 0, "skip": 0, "fail": 0}
    fails = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        for status, png in ex.map(convert_one, pngs):
            stats[status] += 1
            if status == "fail":
                fails.append(png)
    print(f"convert: ok={stats['ok']} skip={stats['skip']} fail={stats['fail']} (total {len(pngs)})")
    if fails:
        print("FAILED:", fails[:10])

    if "--drop-png" in args and not fails:
        dropped = 0
        for png in pngs:
            wp = os.path.join(IMG, png.rsplit(".", 1)[0] + ".webp")
            if os.path.exists(wp):
                os.remove(os.path.join(IMG, png)); dropped += 1
        print(f"dropped source images from public: {dropped} (originals kept in repo-root images/)")


if __name__ == "__main__":
    main()
