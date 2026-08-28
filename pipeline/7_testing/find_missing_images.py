import json
import re
import os

db_path = "questions_db.json"
images_dir = "images"

# 1. DB에서 모든 이미지 파일명 추출
with open(db_path, "r", encoding="utf-8") as f:
    db_data = json.load(f)

required_images = set()
image_pattern = re.compile(r'\[IMAGE:\s*(.*?)\]')

for q in db_data:
    question_text = q.get("question", "")
    choices = q.get("choices", [])
    explanation = q.get("explanation", "")
    
    # 문제, 선지, 해설에서 모두 검색
    texts_to_search = [question_text, explanation] + choices
    
    for text in texts_to_search:
        if not isinstance(text, str):
            continue
        matches = image_pattern.findall(text)
        for match in matches:
            filename = match.split("/")[-1] # 파일명만 추출
            required_images.add(filename)

# 2. 실제 폴더에 있는 이미지 파일명 목록
if os.path.exists(images_dir):
    existing_images = set(os.listdir(images_dir))
else:
    existing_images = set()

# 3. 누락된 이미지 찾기
missing_images = required_images - existing_images

print(f"DB에서 요구하는 총 이미지 수: {len(required_images)}개")
print(f"실제 폴더에 있는 이미지 수: {len(existing_images)}개")
print(f"누락된 이미지 수: {len(missing_images)}개")

# 누락된 이미지 목록을 파일로 저장
with open("missing_images_list.txt", "w", encoding="utf-8") as f:
    for img in sorted(missing_images):
        f.write(f"{img}\n")

print("\n누락된 이미지 목록이 'missing_images_list.txt' 파일로 저장되었습니다.")
