import os
import re

missing_list_path = "missing_images_list.txt"
images_dir = "images"

try:
    with open(missing_list_path, "r", encoding="utf-8") as f:
        missing_images = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("missing_images_list.txt not found.")
    exit()

failed_images = [img for img in missing_images if not os.path.exists(os.path.join(images_dir, img))]

prefix_pattern = re.compile(r'^([a-zA-Z0-9]+?)\d{8}')
prefix_counts = {}

for img in failed_images:
    match = prefix_pattern.match(img)
    if match:
        prefix = match.group(1)
        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1

print(f"다운로드 실패한 총 이미지 수: {len(failed_images)}")
print("실패한 이미지들의 접두사(시험코드) 통계:")
for prefix, count in sorted(prefix_counts.items(), key=lambda item: item[1], reverse=True):
    print(f"- {prefix}: {count}개")
