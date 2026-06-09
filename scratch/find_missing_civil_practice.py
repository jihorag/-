# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
TAXONOMY_PATH = ROOT / "taxonomy_v4.json"
PRACTICE_DIR = ROOT / "viewer/public/data/practice/civil-law"

sys.path.insert(0, str(ROOT))
from scripts.practice_to_app import map_civil_taxonomy

with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
    tax = json.load(f)

taxonomy_nodes = []
for subject_name in ["민법총칙", "물권법"]:
    chapters = tax["민법"]["subjects"][subject_name]
    for ch in chapters:
        ch_name = ch["name"]
        for sec in ch["sections"]:
            sec_name = sec["name"]
            items = sec.get("items", [])
            if not items:
                taxonomy_nodes.append((subject_name, ch_name, sec_name, ""))
            else:
                for it in items:
                    taxonomy_nodes.append((subject_name, ch_name, sec_name, it["name"]))

mapped_practice = set()
for fp in PRACTICE_DIR.glob("*.json"):
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    meta = data.get("meta", {})
    if not meta:
        continue
    sub = meta.get("subject", "민법")
    sub_subj = meta.get("sub_subject", "")
    ch = meta.get("chapter", "")
    sec = meta.get("section", "")
    it = meta.get("item", "")
    
    mapped_subj, mapped_ch, mapped_sec, mapped_it = map_civil_taxonomy(sub_subj, ch, sec, it)
    mapped_practice.add((mapped_subj, mapped_ch, mapped_sec, mapped_it))

print(f"Total taxonomy nodes in civil: {len(taxonomy_nodes)}")
print(f"Total unique mapped practice nodes: {len(mapped_practice)}")

missing_nodes = []
for node in taxonomy_nodes:
    if node not in mapped_practice:
        missing_nodes.append(node)

print(f"\nMissing practice nodes (count={len(missing_nodes)}):")
for node in missing_nodes:
    print(f"  {node[0]} > {node[1]} > {node[2]} > {node[3]}")
