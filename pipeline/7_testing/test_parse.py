import requests
from bs4 import BeautifulSoup
import json
import re
import os
from urllib.parse import urljoin

base_url = 'https://cbtbank.kr'

# Define headers to bypass 403 Forbidden
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'https://cbtbank.kr/exam/cem20250405'
}

def download_image(img_url, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    img_name = img_url.split('/')[-1]
    save_path = os.path.join(save_dir, img_name)
    
    if not os.path.exists(save_path):
        try:
            response = requests.get(img_url, headers=headers, stream=True)
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
            img_url = urljoin(page_url, src)
            local_path = download_image(img_url, './images')
            text += f"[IMAGE: {local_path}] "
            
        elif child.name == 'span' and 'exam-number' in child.get('class', []):
            continue # Skip question number
        else:
            text += extract_text(child, page_url) + " "
    return re.sub(r'\s+', ' ', text).strip()

def scrape_exam(url):
    response = requests.get(url, headers=headers)
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
            for idx, li in enumerate(ol.find_all('li', recursive=False)):
                options.append(extract_text(li, url))
                
        # Explanation
        reply_comment = box.find(class_='reply-comment')
        explanation = extract_text(reply_comment, url) if reply_comment else ""
        
        questions.append({
            'id': q_id,
            'number': q_num,
            'question': q_text,
            'options': options,
            'answer': correct_answer,
            'explanation': explanation
        })
        
    return questions

if __name__ == '__main__':
    url = 'https://cbtbank.kr/exam/cem20250405'
    data = scrape_exam(url)
    with open('questions_db.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully extracted {len(data)} questions and downloaded images.")
