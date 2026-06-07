import json
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
TAX_INDEX = ROOT / "viewer" / "public" / "data" / "study" / "law" / "ai_taxonomy_index.json"

with open(TAX_INDEX, "r", encoding="utf-8") as f:
    data = json.load(f)

leaves = data.get("leaves", [])
print(f"Total leaves: {len(leaves)}")
for i, leaf in enumerate(leaves):
    print(f"{i+1}: {leaf['id']}")
