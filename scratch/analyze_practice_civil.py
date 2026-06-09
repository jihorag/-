# -*- coding: utf-8 -*-
import json
from pathlib import Path

# Load taxonomy
tax_file = Path('taxonomy_v4.json')
with open(tax_file, 'r', encoding='utf-8') as f:
    tax_data = json.load(f)

# Load civil law questions
db_file = Path('questions_db_civil.json')
with open(db_file, 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Filter practice questions
practice_qs = [q for q in questions if q.get('period') == 'practice']

# Build a lookup for practice question counts
counts = {}
for q in practice_qs:
    idx = q.get('indexing_v4', {})
    mt = idx.get('mapped_taxonomy', {})
    if mt.get('subject') == '민법':
        sub_subject = mt.get('sub_subject', '')
        chapter = mt.get('chapter', '')
        section = mt.get('section', '')
        item = mt.get('item', '')
        if not item:
            item = ''
        key = (sub_subject, chapter, section, item)
        counts[key] = counts.get(key, 0) + 1

# Analyze taxonomy and generate Markdown content
civil_tax = tax_data['민법']['subjects']

md_lines = []
md_lines.append("# 민법 연습문제 출제 현황 보고서\n")
md_lines.append("연습문제 전용 데이터베이스인 `questions_db_civil.json`을 분석하여 민법총칙 및 물권법의 각 관(절)별 연습문제 출제 현황을 총정리한 보고서입니다.\n")

total_nodes = 0
completed_nodes = 0
incomplete_nodes = 0

for sub_subject in ['민법총칙', '물권법']:
    md_lines.append(f"## {sub_subject}\n")
    chapters = civil_tax[sub_subject]
    for ch in chapters:
        ch_name = ch['name']
        md_lines.append(f"### {ch_name}\n")
        for sec in ch['sections']:
            sec_name = sec['name']
            items = sec.get('items', [])
            if not items:
                key = (sub_subject, ch_name, sec_name, '')
                cnt = counts.get(key, 0)
                total_nodes += 1
                if cnt > 0:
                    completed_nodes += 1
                    status = f"✅ 완료 ({cnt}문제)"
                else:
                    incomplete_nodes += 1
                    status = "❌ 미출제"
                md_lines.append(f"- **{sec_name}**: {status}\n")
            else:
                md_lines.append(f"- **{sec_name}**\n")
                for it in items:
                    it_name = it['name']
                    key = (sub_subject, ch_name, sec_name, it_name)
                    cnt = counts.get(key, 0)
                    total_nodes += 1
                    if cnt > 0:
                        completed_nodes += 1
                        status = f"✅ 완료 ({cnt}문제)"
                    else:
                        incomplete_nodes += 1
                        status = "❌ 미출제"
                    md_lines.append(f"    - {it_name}: {status}\n")
        md_lines.append("\n")

summary_lines = []
summary_lines.append("## 출제 현황 요약\n")
summary_lines.append("| 항목 | 수치 | 비율 |")
summary_lines.append("| :--- | :--- | :--- |")
summary_lines.append(f"| **전체 taxonomy 노드 수** | {total_nodes}개 | 100% |")
summary_lines.append(f"| **출제 완료 노드 수** | {completed_nodes}개 | {completed_nodes/total_nodes*100:.1f}% |")
summary_lines.append(f"| **미출제 노드 수** | {incomplete_nodes}개 | {incomplete_nodes/total_nodes*100:.1f}% |")
summary_lines.append("\n")

md_content = "\n".join(md_lines) + "\n" + "\n".join(summary_lines)

# Write to artifact directory
artifact_dir = Path('/Users/hanjiho/.gemini/antigravity/brain/7f9a4a74-e580-40fc-87f2-ab77ac0b683b')
out_file = artifact_dir / 'civil_practice_status.md'

with open(out_file, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"Report written to {out_file}")
