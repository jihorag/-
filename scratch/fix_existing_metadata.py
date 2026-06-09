import json
import os
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
PRACTICE_DIR = ROOT / "viewer/public/data/practice/civil-law"

def fix_metadata():
    # 1. Ch 4 files
    for idx, name in enumerate(["물건의 의의와 분류", "부동산과 동산", "주물과 종물", "원물과 과실"], 1):
        fp = PRACTICE_DIR / f"civil-gen-ch04-sec{idx:02d}-item01.json"
        if fp.exists():
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["meta"]["chapter"] = "제4장 권리의 객체"
            data["meta"]["item"] = ""
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Fixed {fp.name}")

    # 2. Ch 6 files
    for idx, name in enumerate(["의의", "계산방법"], 1):
        fp = PRACTICE_DIR / f"civil-gen-ch06-sec{idx:02d}-item01.json"
        if fp.exists():
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["meta"]["chapter"] = "제6장 기간"
            data["meta"]["item"] = ""
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Fixed {fp.name}")

    # 3. Ch 9 Sec 2 files (점유권의 취득과 소멸)
    items = ["제1관 점유권의 취득", "제2관 점유의 승계", "제3관 점유권의 소멸"]
    for idx, it in enumerate(items, 1):
        fp = PRACTICE_DIR / f"civil-gen-ch09-sec02-item{idx:02d}.json"
        if fp.exists():
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["meta"]["chapter"] = "제2장 점유권"
            data["meta"]["section"] = "제2절 점유권의 취득과 소멸"
            data["meta"]["item"] = it
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Fixed {fp.name}")

if __name__ == "__main__":
    fix_metadata()
