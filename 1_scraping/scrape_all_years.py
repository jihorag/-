import requests
from bs4 import BeautifulSoup
import json
import re
import os
from urllib.parse import urljoin
import time
import shutil

base_url = 'https://cbtbank.kr'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

dates = [
    "2025-04-05", "2024-04-06", "2023-04-08", "2022-04-02",
    "2021-04-24", "2020-06-13", "2019-03-02", "2018-03-03",
    "2017-03-04", "2016-03-12", "2015-06-27", "2014-07-05",
    "2013-06-29", "2012-07-01", "2011-07-03", "2010-07-04",
    "2009-07-05"
]

def download_image(img_url, save_dir, referer):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    img_name = img_url.split('/')[-1]
    save_path = os.path.join(save_dir, img_name)
    
    if not os.path.exists(save_path):
        try:
            req_headers = headers.copy()
            req_headers['Referer'] = referer
            response = requests.get(img_url, headers=req_headers, stream=True)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Downloaded: {img_name}")
            else:
                print(f"Failed to download {img_url} (Status: {response.status_code})")
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")
            
    return f"./images/{img_name}"

def extract_text(element, page_url):
    if not element:
        return ""
    text = ""
    for child in element.contents:
        if isinstance(child, str):
            text += child.strip() + " "
        elif child.name == 'img':
            src = child.get('src')
            if src:
                img_url = urljoin(page_url, src)
                local_path = download_image(img_url, './images', page_url)
                text += f"[IMAGE: {local_path}] "
        elif child.name == 'span' and 'exam-number' in child.get('class', []):
            continue 
        else:
            text += extract_text(child, page_url) + " "
    return re.sub(r'\s+', ' ', text).strip()

def scrape_exam(date_str):
    date_code = date_str.replace("-", "")
    url = f"https://cbtbank.kr/exam/cem{date_code}"
    
    req_headers = headers.copy()
    response = requests.get(url, headers=req_headers)
    if response.status_code != 200:
        print(f"Failed to load {url}")
        return []
        
    soup = BeautifulSoup(response.text, 'html.parser')
    exam_boxes = soup.find_all(class_='exam-box')
    questions = []
    
    for box in exam_boxes:
        q_id = box.get('question-id')
        q_num = box.get('question-num')
        
        title_el = box.find(class_='exam-title')
        q_text = extract_text(title_el, url)
        if q_text.startswith('. '):
            q_text = q_text[2:]
        
        ol = box.find('ol', class_='circlednumbers')
        correct_answer = ol.get('correct') if ol else None
        
        options = []
        if ol:
            for li in ol.find_all('li', recursive=False):
                options.append(extract_text(li, url))
                
        reply_comment = box.find(class_='reply-comment')
        explanation = extract_text(reply_comment, url) if reply_comment else ""
        
        questions.append({
            'id': q_id,
            'number': q_num,
            'year': date_str.split("-")[0],
            'exam_date': date_str,
            'question': q_text,
            'options': options,
            'answer': correct_answer,
            'explanation': explanation
        })
        
    return questions

if __name__ == '__main__':
    all_questions = []
    for d in dates:
        print(f"Scraping exam for {d}...")
        q_list = scrape_exam(d)
        print(f" -> Found {len(q_list)} questions")
        all_questions.extend(q_list)
        time.sleep(1) # Be polite
        
    with open('questions_db.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    print(f"Successfully extracted total {len(all_questions)} questions.")

    # Also copy to viewer directory
    shutil.copy('questions_db.json', 'viewer/src/data/questions_db.json')
    if os.path.exists('./images'):
        if not os.path.exists('viewer/public/images'):
            os.makedirs('viewer/public/images')
        for item in os.listdir('./images'):
            s = os.path.join('./images', item)
            d = os.path.join('viewer/public/images', item)
            shutil.copy2(s, d)
    print("Copied db and images to viewer directory.")
