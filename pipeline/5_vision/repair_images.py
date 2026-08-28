import json
import requests
import os
import re

db_path = "questions_db.json"
images_dir = "images"
base_url = "https://cbtbank.kr"

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

def download_image(img_url):
    full_url = base_url + img_url if img_url.startswith("/") else img_url
    filename = os.path.basename(img_url).split('?')[0]
    filepath = os.path.join(images_dir, filename)
    
    try:
        res = requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(res.content)
        print(f"Repaired: {filename}")
        return f"./images/{filename}"
    except Exception as e:
        print(f"Failed to repair {full_url}: {e}")
        return img_url

def repair_text(text):
    if not text: return text
    matches = re.findall(r'\[IMAGE: (/images/.*?)\]', text)
    for img_path in matches:
        local_path = download_image(img_path)
        text = text.replace(f"[IMAGE: {img_path}]", f"[IMAGE: {local_path}]")
    return text

count = 0
for q in db:
    q['question'] = repair_text(q.get('question', ''))
    if q.get('options'):
        q['options'] = [repair_text(opt) for opt in q['options']]
    q['explanation'] = repair_text(q.get('explanation', ''))

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

# Sync to viewer
import shutil
shutil.copy(db_path, 'viewer/src/data/questions_db.json')
# Also copy new images
for filename in os.listdir(images_dir):
    src = os.path.join(images_dir, filename)
    dst = os.path.join('viewer/public/images', filename)
    if not os.path.exists(dst):
        shutil.copy(src, dst)

print("Repair complete!")
