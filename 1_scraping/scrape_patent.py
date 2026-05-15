import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time
import shutil

dates = [
    "20250215", "20240224", "20230218", "20220219", "20210227",
    "20200530", "20190216", "20180317", "20170225", "20160227",
    "20150214", "20140222", "20130223", "20120226", "20110227",
    "20080309"
]

db_path = "questions_db.json"
images_dir = "images"
viewer_public_images = "viewer/public/images"
base_url = "https://cbtbank.kr"

if not os.path.exists(images_dir):
    os.makedirs(images_dir)
if not os.path.exists(viewer_public_images):
    os.makedirs(viewer_public_images)

def download_image(img_url):
    try:
        full_url = base_url + img_url if img_url.startswith("/") else img_url
        if full_url.startswith("//"): full_url = "https:" + full_url
        filename = os.path.basename(img_url).split('?')[0]
        filepath = os.path.join(images_dir, filename)
        if not os.path.exists(filepath):
            headers = {"User-Agent": "Mozilla/5.0", "Referer": base_url}
            res = requests.get(full_url, headers=headers)
            res.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(res.content)
            shutil.copy(filepath, os.path.join(viewer_public_images, filename))
        return f"./images/{filename}"
    except:
        return img_url

def extract_text(element):
    if not element: return ""
    text_parts = []
    for child in element.descendants:
        if isinstance(child, str):
            text_parts.append(child.strip())
        elif child.name == 'img':
            img_src = child.get('src')
            if img_src:
                local_path = download_image(img_src)
                text_parts.append(f"[IMAGE: {local_path}]")
    return " ".join([p for p in text_parts if p]).strip()

def scrape_exam(date):
    url = f"{base_url}/exam/hk{date}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200: return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    boxes = soup.find_all(class_='exam-box')
    parsed = []
    
    for i, box in enumerate(boxes):
        q_num = i + 1
        q_title_el = box.find(class_='exam-title') or box.find(class_='question-title') or box.find(class_=re.compile(r'text-lg.*'))
        if not q_title_el: continue
            
        full_text = extract_text(q_title_el)
        q_body = re.sub(rf'^{q_num}[\.\s]*', '', full_text).strip()
            
        options = []
        answer = None
        ol = box.find('ol', class_='circlednumbers')
        if ol:
            answer = ol.get('correct')
            for li in ol.find_all('li'):
                options.append(extract_text(li))
        
        reply_comment = box.find(class_='reply-comment')
        explanation = extract_text(reply_comment) if reply_comment else ""
        
        parsed.append({
            "exam": "변리사",
            "period": "hk",
            "exam_date": f"{date[:4]}-{date[4:6]}-{date[6:]}",
            "year": date[:4],
            "number": str(q_num),
            "question": q_body,
            "options": options,
            "answer": answer,
            "explanation": explanation
        })
    return parsed

def main():
    db = json.load(open(db_path, "r", encoding="utf-8")) if os.path.exists(db_path) else []
    print(f"Loaded {len(db)} existing questions.")
    
    new_added = 0
    for date in dates:
        date_str = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        if any(q.get('period') == 'hk' and q.get('exam_date') == date_str for q in db):
            print(f"Skipping {date_str} (exists)")
            continue
            
        print(f"Scraping {date_str}...")
        qs = scrape_exam(date)
        print(f" -> Found {len(qs)} questions")
        db.extend(qs)
        new_added += len(qs)
        json.dump(db, open(db_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        time.sleep(1)
        
    if new_added > 0:
        shutil.copy(db_path, 'viewer/src/data/questions_db.json')
        print(f"Done! Added {new_added} questions.")
    else:
        print("No new questions.")

if __name__ == "__main__":
    main()
