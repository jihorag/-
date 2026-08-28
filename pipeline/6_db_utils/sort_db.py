import json

with open('questions_db.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

def sort_key(q):
    # Sort primarily by Year, then Exam, then Period, then Subject, then Number
    year = q.get('year', '0')
    exam = q.get('exam') or '감정평가사'
    
    subject = q.get('subject') or q.get('tags', {}).get('subject') or ''
    # Specific ordering for Tax: 재정학 (1교시), 세법학개론 (1교시), 회계학개론 (2교시), 민법 (2교시)
    subj_order = 99
    if exam == '세무사':
        if '재정학' in subject: subj_order = 1
        elif '회계학' in subject: subj_order = 2
        elif '민법' in subject: subj_order = 3
        
    num = int(q.get('number', 999))
    return (year, exam, subj_order, subject, num)

d.sort(key=sort_key)

with open('questions_db.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

import os
os.system('cp questions_db.json viewer/src/data/questions_db.json')
print("Sorted DB!")
