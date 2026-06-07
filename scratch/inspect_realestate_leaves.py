import json
import os

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
TAX_INDEX = os.path.join(ROOT, "viewer/public/data/study/realestate/ai_taxonomy_index.json")

with open(TAX_INDEX, "r", encoding="utf-8") as f:
    data = json.load(f)

leaves = data.get("leaves", [])
print(f"Total leaves: {len(leaves)}")

# Group by unit_code
by_unit = {}
for leaf in leaves:
    uc = leaf.get("unit_code")
    by_unit.setdefault(uc, []).append(leaf)

for uc, items in sorted(by_unit.items()):
    print(f"Unit: {uc} has {len(items)} leaves")
    for item in items[:3]:
        print(f"  - {' / '.join(item['path'])}")
    if len(items) > 3:
        print(f"  - ... ({len(items) - 3} more)")
