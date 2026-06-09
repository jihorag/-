from pathlib import Path

file_path = Path("/Users/hanjiho/Documents/감정평가사 기출문제/scratch/generate_relations_questions.py")
content = file_path.read_text(encoding="utf-8")

# Replace JSON-style boolean/null with Python equivalents
content = content.replace('"correct": false', '"correct": False')
content = content.replace('"correct": true', '"correct": True')
content = content.replace('"correct": False', '"correct": False')
content = content.replace('"correct": True', '"correct": True')
content = content.replace('"no": null', '"no": None')
content = content.replace('"no": None', '"no": None')
content = content.replace('"in_scope": true', '"in_scope": True')
content = content.replace('"in_scope": false', '"in_scope": False')
content = content.replace('"in_scope": True', '"in_scope": True')
content = content.replace('"in_scope": False', '"in_scope": False')

file_path.write_text(content, encoding="utf-8")
print("Successfully replaced all JSON literals with Python literals in generate_relations_questions.py.")
