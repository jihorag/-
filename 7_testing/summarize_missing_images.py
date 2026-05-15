import json

db_path = "questions_db.json"
missing_list_path = "missing_images_list.txt"

# 누락된 이미지 목록 로드
try:
    with open(missing_list_path, "r", encoding="utf-8") as f:
        missing_images = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    print("missing_images_list.txt 파일을 찾을 수 없습니다.")
    exit()

# DB 로드
with open(db_path, "r", encoding="utf-8") as f:
    db_data = json.load(f)

# 과목별 누락 통계용 딕셔너리
missing_stats = {}

import re
image_pattern = re.compile(r'\[IMAGE:\s*(.*?)\]')

# DB를 순회하며 누락된 이미지가 어떤 과목에 속해 있는지 카운트
for q in db_data:
    subject = q.get("subject", "알 수 없음")
    
    question_text = q.get("question", "")
    choices = q.get("choices", [])
    explanation = q.get("explanation", "")
    
    texts_to_search = [question_text, explanation] + [c for c in choices if isinstance(c, str)]
    
    for text in texts_to_search:
        if not isinstance(text, str):
            continue
        matches = image_pattern.findall(text)
        for match in matches:
            filename = match.split("/")[-1]
            if filename in missing_images:
                missing_stats[subject] = missing_stats.get(subject, 0) + 1

# 결과 출력
print("과목별 누락된 이미지 개수:")
print("-" * 30)
# 값(누락 개수)을 기준으로 내림차순 정렬
sorted_stats = sorted(missing_stats.items(), key=lambda item: item[1], reverse=True)
for subject, count in sorted_stats:
    print(f"{subject}: {count}개")
print("-" * 30)
total_occurrences = sum(missing_stats.values())
print(f"총 누락된 이미지 참조 횟수: {total_occurrences}회")
