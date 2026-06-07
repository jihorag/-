import json
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
QDB = ROOT / "questions_db.json"
TAX_INDEX = ROOT / "viewer" / "public" / "data" / "study" / "law" / "ai_taxonomy_index.json"

with open(TAX_INDEX, "r", encoding="utf-8") as f:
    tax_data = json.load(f)

leaves = tax_data.get("leaves", [])
leaf_ids = [leaf["id"] for leaf in leaves]

with open(QDB, "r", encoding="utf-8") as f:
    db = json.load(f)

leaf_counts = Counter()
for q in db:
    if "indexing_v4" in q and q["indexing_v4"] and "mapped_taxonomy" in q["indexing_v4"] and q["indexing_v4"]["mapped_taxonomy"]:
        tax = q["indexing_v4"]["mapped_taxonomy"]
        if tax.get("subject") == "감정평가관계법규":
            # Reconstruction leaf id
            chapter = tax.get("chapter", "")
            section = tax.get("section", "")
            item = tax.get("item", "")
            
            # Find matching leaf in our taxonomy
            matched_leaf = None
            for leaf in leaves:
                path = leaf["path"]
                l_chap = path[0]
                l_sec = path[1]
                l_item = path[2] if len(path) > 2 else ""
                
                # Check match
                if l_chap == chapter and l_sec == section:
                    if not l_item or l_item == item:
                        matched_leaf = leaf["id"]
                        break
            if matched_leaf:
                leaf_counts[matched_leaf] += 1
            else:
                # Fallback matching
                for leaf in leaves:
                    if leaf["id"].endswith(section.replace(" ", "_").replace("·", "_").replace(",", "_")):
                        matched_leaf = leaf["id"]
                        break
                if matched_leaf:
                    leaf_counts[matched_leaf] += 1

print("Leaf count distribution:")
for leaf in leaves:
    print(f"  {leaf['id'][:60]}: {leaf_counts[leaf['id']]} questions")
