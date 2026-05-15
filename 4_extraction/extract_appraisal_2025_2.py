import json
import os
from bs4 import BeautifulSoup

def extract_appraisal_2025_2():
    html_path = 'exam_raw.html'
    db_path = 'questions_db.json'
    
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found.")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    questions = []
    exam_boxes = soup.find_all('div', class_='exam-box')
    
    print(f"Found {len(exam_boxes)} exam boxes in HTML.")

    for box in exam_boxes:
        q_num_raw = int(box.get('question-num', 0))
        if q_num_raw == 0: continue
        
        # Mapping to global 2025 Appraisal sequence (121-200)
        global_num = q_num_raw + 120
        q_id = f"cek20250405-{global_num}"
        
        # Subject mapping
        if 1 <= q_num_raw <= 40:
            subject = "감정평가관계법규"
        else:
            subject = "회계학"
            
        # Extract title/body
        title_div = box.find('p', class_='exam-title')
        if not title_div: continue
        
        # Handle images in title
        body_parts = []
        for content in title_div.contents:
            if content.name == 'span' and 'exam-number' in content.get('class', []):
                continue
            if content.name == 'img':
                img_name = content['src'].split('/')[-1]
                body_parts.append(f" [IMAGE: ./images/{img_name}]")
            elif isinstance(content, str):
                body_parts.append(content.strip())
            else:
                body_parts.append(content.get_text().strip())
        
        question_text = "".join(body_parts).strip()
        if question_text.startswith('.'):
            question_text = question_text[1:].strip()
            
        # Extract choices
        choices = []
        ol = box.find('ol', class_='circlednumbers')
        if ol:
            lis = ol.find_all('li')
            for li in lis:
                choices.append(li.get_text().strip())
        
        # Extract answer
        answer = ol.get('correct', '1') if ol else '1'
        
        # Extract explanation
        explanation = ""
        reply_div = box.find('div', class_='reply-comment')
        if reply_div:
            # Handle images in explanation too
            exp_parts = []
            for content in reply_div.contents:
                if content.name == 'img':
                    img_name = content['src'].split('/')[-1]
                    exp_parts.append(f" [IMAGE: ./images/{img_name}]")
                elif content.name == 'br':
                    exp_parts.append("\n")
                elif isinstance(content, str):
                    exp_parts.append(content.strip())
                else:
                    exp_parts.append(content.get_text().strip())
            explanation = "".join(exp_parts).strip()

        questions.append({
            "id": q_id,
            "year": "2025",
            "exam": "감정평가사",
            "subject": subject,
            "number": str(global_num),
            "question": question_text,
            "options": choices,
            "answer": answer,
            "explanation": explanation,
            "tags": {
                "subject": subject,
                "difficulty": 3
            }
        })

    # Merge into DB
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            db = json.load(f)
    else:
        db = []

    # Remove existing 121-200 if any (clean start)
    db = [q for q in db if not (q.get('exam') == '감정평가사' and q.get('year') == '2025' and 121 <= int(q.get('number', 0)) <= 200)]
    
    db.extend(questions)
    
    # Sort DB for sanity
    # db.sort(key=lambda x: (x.get('year', '0'), x.get('exam', ''), int(x.get('number', 0))))

    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"Successfully added {len(questions)} questions (121-200) to {db_path}")

if __name__ == "__main__":
    extract_appraisal_2025_2()
