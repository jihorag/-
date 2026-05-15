import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time

dates = [
    "20241026", "20231028", "20221029", "20211030", "20201031",
    "20191026", "20181027", "20171028", "20161029", "20151024",
    "20141026", "20131027", "20121028", "20111123", "20101024",
    "20081026", "20071028", "20061029", "20051030", "20050522"
]

db_path = "questions_db.json"
images_dir = "images"
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

def download_image(img_url, filename):
    try:
        if img_url.startswith("//"):
            img_url = "https:" + img_url
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://cbtbank.kr/"
        }
        res = requests.get(img_url, headers=headers)
        res.raise_for_status()
        filepath = os.path.join(images_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(res.content)
        return f"./images/{filename}"
    except:
        return img_url

def extract_text(element):
    if not element:
        return ""
    text_parts = []
    for child in element.descendants:
        if isinstance(child, str):
            text_parts.append(child.strip())
        elif child.name == 'img':
            img_src = child.get('src')
            if img_src:
                filename = os.path.basename(img_src).split('?')[0]
                local_path = download_image(img_src, filename)
                text_parts.append(f"[IMAGE: {local_path}]")
    
    return " ".join([p for p in text_parts if p]).strip()

def scrape_exam(date):
    url = f"https://cbtbank.kr/exam/g1{date}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    boxes = soup.find_all(class_='exam-box')
    parsed_questions = []
    
    for box in boxes:
        # Try different question title selectors
        q_title_el = box.find(class_='exam-title') or box.find(class_='question-title') or box.find(class_=re.compile(r'text-lg.*'))
        if not q_title_el:
            continue
            
        full_text = extract_text(q_title_el)
        # Try to find number in exam-number span first
        num_span = q_title_el.find(class_='exam-number')
        if num_span:
            q_num = num_span.get_text().strip()
            # Remove number from full_text if it's there
            q_body = re.sub(rf'^{q_num}[\.\s]*', '', full_text).strip()
        else:
            match = re.match(r'^(\d+)[\.\s]+(.*)', full_text)
            if match:
                q_num = match.group(1)
                q_body = match.group(2).strip()
            else:
                continue
                
        options = []
        answer = None
        ol = box.find('ol', class_='circlednumbers')
        if ol:
            answer = ol.get('correct')
            for li in ol.find_all('li'):
                options.append(extract_text(li))
        
        reply_comment = box.find(class_='reply-comment')
        explanation = extract_text(reply_comment) if reply_comment else ""
        
        parsed_questions.append({
            "exam": "공인중개사",
            "period": "g1",
            "exam_date": f"{date[:4]}-{date[4:6]}-{date[6:]}",
            "year": date[:4],
            "number": q_num,
            "question": q_body,
            "options": options,
            "answer": answer,
            "explanation": explanation
        })
        
    return parsed_questions

def main():
    db = json.load(open(db_path, "r", encoding="utf-8")) if os.path.exists(db_path) else []
    print(f"Loaded {len(db)} existing questions.")
    
    new_added = 0
    for date in dates:
        date_str = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        if any(q.get('period') == 'g1' and q.get('exam_date') == date_str for q in db):
            print(f"Skipping {date_str} (already exists)")
            continue
            
        print(f"Scraping {date_str}...")
        qs = scrape_exam(date)
        print(f" -> Found {len(qs)} questions")
        db.extend(qs)
        new_added += len(qs)
        json.dump(db, open(db_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        time.sleep(1)
        
    if new_added > 0:
        import shutil
        shutil.copy(db_path, 'viewer/src/data/questions_db.json')
        print(f"Done! Added {new_added} questions.")
    else:
        print("No new questions.")

if __name__ == "__main__":
    main()
