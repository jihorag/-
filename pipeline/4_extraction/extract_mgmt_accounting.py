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

urls = [
    "https://cbtbank.kr/exam/cfm20250412",
    "https://cbtbank.kr/exam/cfm20240420",
    "https://cbtbank.kr/exam/cfm20230422",
    "https://cbtbank.kr/exam/cda20220423",
    "https://cbtbank.kr/exam/cda20210403",
    "https://cbtbank.kr/exam/rt20200829",
    "https://cbtbank.kr/exam/rt20190406",
    "https://cbtbank.kr/exam/rt20180407",
    "https://cbtbank.kr/exam/rt20170408",
    "https://cbtbank.kr/exam/rt20160507",
    "https://cbtbank.kr/exam/rt20150516",
    "https://cbtbank.kr/exam/rt20140517",
    "https://cbtbank.kr/exam/rt20130518"
]

def download_image(img_url, save_dir, referer):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    img_name = img_url.split('/')[-1]
    # Strip query params if any
    img_name = img_name.split('?')[0]
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
            else:
                print(f"Failed to download {img_url}")
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")
    return f"./images/{img_name}"

def extract_text(element, page_url):
    if not element: return ""
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
        elif child.name == 'br':
            text += "\n"
        else:
            text += extract_text(child, page_url) + " "
    return re.sub(r' +', ' ', text).strip()

def scrape_mgmt_accounting(url):
    print(f"Processing {url}...")
    year_match = re.search(r'(\d{4})', url)
    year = year_match.group(1) if year_match else "Unknown"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to load {url}")
        return []
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all subject headers with 'exam-class-title' class
    headers_tags = soup.find_all(lambda t: t.name in ['div', 'p', 'h3', 'h4'] and 'exam-class-title' in t.get('class', []) and '회계학개론' in t.get_text())
    
    target_questions = []
    
    if not headers_tags:
        # Fallback for older versions if 'exam-class-title' is not used
        headers_tags = soup.find_all(lambda t: t.name in ['div', 'p', 'h3', 'h4'] and '회계학개론' in t.get_text() and len(t.get_text().strip()) < 30)
        if not headers_tags:
            print(f"No '회계학개론' header found for {year}")
            return []
    
    # Use the first one found
    header = headers_tags[0]
    seen_ids = set()
    
    # Get all exam-boxes following this header
    for el in header.find_all_next():
        # Check if we hit the next subject header
        if el.name in ['div', 'p', 'h3', 'h4'] and '과목' in el.get_text() and '회계학' not in el.get_text():
            txt = el.get_text().strip()
            if len(txt) < 30 and (txt.startswith('1') or txt.startswith('2') or txt.startswith('3') or txt.startswith('4') or txt.startswith('5')):
                break
        
        if el.get('class') and 'exam-box' in el.get('class'):
            q_id = el.get('question-id')
            if q_id in seen_ids: continue
            seen_ids.add(q_id)
            
            q_num = el.get('question-num')
            if not q_num: continue # Skip if no number
            
            title_el = el.find(class_='exam-title')
            q_text = extract_text(title_el, url)
            if not q_text: continue # Skip if no question text
            
            # Clean up number from text
            q_text = re.sub(fr"^{q_num}\s*\.\s*", "", q_text)
            
            ol = el.find('ol', class_='circlednumbers')
            correct_answer = ol.get('correct') if ol else "1"
            
            options = []
            if ol:
                for li in ol.find_all('li', recursive=False):
                    options.append(extract_text(li, url))
            
            reply_comment = el.find(class_='reply-comment')
            explanation = extract_text(reply_comment, url) if reply_comment else ""
            
            target_questions.append({
                'id': f"mgmt_acc_{year}_{q_num}",
                'number': q_num,
                'year': year,
                'exam': '경영지도사',
                'subject': '회계학',
                'question': q_text,
                'options': options,
                'answer': correct_answer,
                'explanation': explanation,
                'tags': {
                    'subject': '회계학',
                    'difficulty': 3
                }
            })
    
    print(f" -> Found {len(target_questions)} questions for {year}")
    return target_questions

if __name__ == '__main__':
    all_mgmt_questions = []
    for u in urls:
        questions = scrape_mgmt_accounting(u)
        all_mgmt_questions.extend(questions)
        time.sleep(0.5)
        
    # Merge into existing db
    db_path = 'questions_db.json'
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            db = json.load(f)
    else:
        db = []
    
    # Remove old mgmt_acc questions to avoid duplicates
    db = [q for q in db if not q.get('id', '').startswith('mgmt_acc_')]
    db.extend(all_mgmt_questions)
    
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"Total {len(all_mgmt_questions)} Management Consultant Accounting questions added.")
    
    # Sync images to viewer
    if not os.path.exists('viewer/public/images'):
        os.makedirs('viewer/public/images')
    if os.path.exists('./images'):
        for item in os.listdir('./images'):
            src = os.path.join('./images', item)
            dst = os.path.join('viewer/public/images', item)
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
    
    # Sync db to viewer
    shutil.copy(db_path, 'viewer/src/data/questions_db.json')
    print("Database and images synced to viewer.")
