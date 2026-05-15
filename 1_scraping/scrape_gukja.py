import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time
import shutil

categories = [
    ('142161', '2025'),
    ('124643', '2024'),
    ('98287', '2023'),
    ('78442', '2022'),
    ('92833', '2021'),
    ('99215', '2020'),
    ('101376', '2019'),
    ('102080', '2018'),
    ('124360', '2017')
]

db_path = "questions_db.json"
images_dir = "images"
viewer_public_images = "viewer/public/images"

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

def download_image(img_url):
    try:
        if img_url.startswith("//"): img_url = "https:" + img_url
        elif img_url.startswith("/"): img_url = "https://gukja.net" + img_url
        
        filename = os.path.basename(img_url).split('?')[0]
        filepath = os.path.join(images_dir, filename)
        if not os.path.exists(filepath):
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(img_url, headers=headers)
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

def get_answer(exam_srl):
    url = f"https://gukja.net/nexam14?exam_srl={exam_srl}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        ans_el = soup.find(class_='correct_answer')
        if ans_el:
            text = ans_el.get_text(strip=True)
            match = re.search(r'\d+', text)
            if match:
                return match.group(0)
    return None

def scrape_category(cat_srl, year):
    url = f"https://gukja.net/nexam14?category_srl={cat_srl}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200: return []
    
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all(class_='exam_item')
    parsed = []
    seen_q = set()
    
    for item in items:
        exam_srl = item.get('exam_srl')
        q_el = item.find(class_='exam_question')
        if not q_el: continue
            
        full_q_text = extract_text(q_el)
        match = re.match(r'^(\d+)[\.\s]+(.*)', full_q_text)
        if match:
            q_num = match.group(1)
            q_body = match.group(2).strip()
        else:
            q_num = str(len(parsed) + 1)
            q_body = full_q_text.strip()
            
        if q_num in seen_q: continue
        seen_q.add(q_num)
            
        options = []
        opt_els = item.find_all(class_='exam_answer')
        for opt_el in opt_els:
            # exclude correct_answer if present
            if 'correct_answer' in opt_el.get('class', []): continue
            
            a_tag = opt_el.find('a', class_='answer_select')
            if a_tag:
                # remove the number prefix inside span.select_num
                num_span = a_tag.find(class_='select_num')
                if num_span:
                    num_span.extract()
                options.append(extract_text(a_tag))
                
        answer = get_answer(exam_srl)
        time.sleep(0.5)
        
        parsed.append({
            "exam": "행정사",
            "period": "nexam14",
            "exam_date": f"{year}-01-01",
            "year": year,
            "number": q_num,
            "question": q_body,
            "options": options,
            "answer": answer,
            "explanation": ""
        })
    return parsed

def main():
    db = json.load(open(db_path, "r", encoding="utf-8")) if os.path.exists(db_path) else []
    
    new_added = 0
    for cat_srl, year in categories:
        if any(q.get('exam') == '행정사' and q.get('year') == year for q in db):
            print(f"Skipping 행정사 {year} (exists)")
            continue
            
        print(f"Scraping 행정사 {year} (cat: {cat_srl})...")
        qs = scrape_category(cat_srl, year)
        print(f" -> Found {len(qs)} questions")
        db.extend(qs)
        new_added += len(qs)
        json.dump(db, open(db_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        
    if new_added > 0:
        shutil.copy(db_path, 'viewer/src/data/questions_db.json')
        print(f"Done! Added {new_added} questions.")
    else:
        print("No new questions.")

if __name__ == "__main__":
    main()
