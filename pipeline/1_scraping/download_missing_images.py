import os
import re
import requests
import time

missing_list_path = "missing_images_list.txt"
images_dir = "images"
os.makedirs(images_dir, exist_ok=True)

try:
    with open(missing_list_path, "r", encoding="utf-8") as f:
        missing_images = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"File not found: {missing_list_path}")
    exit()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://cbtbank.kr/"
}

# 정규식: (영문숫자 조합 접두사) + (8자리 숫자 날짜) + (나머지 파일명)
pattern = re.compile(r'^([a-zA-Z0-9]+?)(\d{8})(.*)\.(gif|png|jpg|jpeg)$', re.IGNORECASE)

success_count = 0
fail_count = 0

print(f"총 {len(missing_images)}개의 누락된 이미지 다운로드를 시작합니다...")

for filename in missing_images:
    match = pattern.match(filename)
    if not match:
        print(f"파일명 형식 오류, 건너뜀: {filename}")
        fail_count += 1
        continue
        
    exam_code = match.group(1)
    date_str = match.group(2)
    exam_dir = f"{exam_code}{date_str}"
    
    # URL 구성 (예: https://cbtbank.kr/images/cgx/cgx20150411/cgx20150411m39.gif)
    url = f"https://cbtbank.kr/images/{exam_code}/{exam_dir}/{filename}"
    save_path = os.path.join(images_dir, filename)
    
    # 이미 다운로드 되어있으면 건너뜀
    if os.path.exists(save_path):
        success_count += 1
        continue
        
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"다운로드 성공: {filename}")
            success_count += 1
        else:
            print(f"다운로드 실패 ({response.status_code}): {url}")
            fail_count += 1
    except Exception as e:
        print(f"오류 발생 ({filename}): {e}")
        fail_count += 1
        
    # 서버 부하 방지를 위해 약간 대기
    time.sleep(0.2)

print("\n다운로드 완료!")
print(f"성공: {success_count}개, 실패: {fail_count}개")
