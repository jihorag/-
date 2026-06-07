#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026년 감정평가사 기출문제 누락 해설 생성 및 반영 스크립트.
멀티모달 이미지 지원 및 15 RPM 무료 API 제한 준수.
"""
import os
import re
import json
import time
import base64
import urllib.request
import urllib.error
import threading
import unicodedata

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
DB_PATH = os.path.join(ROOT, "questions_db.json")
IMAGES_DIR = os.path.join(ROOT, "viewer/public/images")

# API 속도 제어
api_lock = threading.Lock()
last_request_time = 0.0

def load_gemini_key():
    try:
        with open(os.path.join(ROOT, ".env"), "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except Exception as e:
        print("Error loading API key:", e)
    return None

GEMINI_API_KEY = load_gemini_key()

def get_normalized_image_path(img_name):
    # DB에 저장된 이미지 파일 이름(예: appraisal_2026_회계학_41_body.png)을 실제 webp 파일 경로로 매핑
    base_name = os.path.splitext(img_name)[0]
    target_f = base_name + ".webp"
    
    # OS 파일 시스템의 NFC/NFD 매칭을 위해 파일 목록 스캔
    target_norm = unicodedata.normalize('NFC', target_f)
    
    if not os.path.exists(IMAGES_DIR):
        return None
        
    for fname in os.listdir(IMAGES_DIR):
        fname_norm = unicodedata.normalize('NFC', fname)
        if fname_norm == target_norm:
            return os.path.join(IMAGES_DIR, fname)
            
    # 대소문자나 미세한 차이를 대비한 유연한 매칭
    target_clean = re.sub(r'[^a-zA-Z0-9가-힣]', '', target_norm)
    for fname in os.listdir(IMAGES_DIR):
        fname_norm = unicodedata.normalize('NFC', fname)
        fname_clean = re.sub(r'[^a-zA-Z0-9가-힣]', '', fname_norm)
        if fname_clean == target_clean:
            return os.path.join(IMAGES_DIR, fname)
            
    return None

def query_gemini_with_image(prompt, image_path, filename_log):
    global last_request_time
    
    # 15 RPM 한도 준수를 위한 4.5초 간격 확보
    with api_lock:
        now = time.time()
        elapsed = now - last_request_time
        if elapsed < 4.5:
            time.sleep(4.5 - elapsed)
        last_request_time = time.time()
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    # 이미지 파일 읽기 및 base64 인코딩
    try:
        with open(image_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        print(f"  [{filename_log}] Failed to read image {image_path}: {e}")
        return None
        
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inlineData": {
                        "mimeType": "image/webp",
                        "data": img_data
                    }
                }
            ]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)
    
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                return res_json["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            print(f"  [{filename_log} - Attempt {attempt+1}] HTTP Error {e.code}: {err_msg}")
            if e.code == 429:
                print(f"  [{filename_log}] Rate limit hit. Sleeping 30s...")
                time.sleep(30.0)
            else:
                time.sleep(2 ** (attempt + 1))
        except Exception as e:
            print(f"  [{filename_log} - Attempt {attempt+1}] Error: {e}")
            time.sleep(2 ** (attempt + 1))
            
    return None

def query_gemini_text(prompt, filename_log):
    global last_request_time
    
    with api_lock:
        now = time.time()
        elapsed = now - last_request_time
        if elapsed < 4.5:
            time.sleep(4.5 - elapsed)
        last_request_time = time.time()
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)
    
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                return res_json["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            print(f"  [{filename_log} - Attempt {attempt+1}] HTTP Error {e.code}: {err_msg}")
            if e.code == 429:
                print(f"  [{filename_log}] Rate limit hit. Sleeping 30s...")
                time.sleep(30.0)
            else:
                time.sleep(2 ** (attempt + 1))
        except Exception as e:
            print(f"  [{filename_log} - Attempt {attempt+1}] Error: {e}")
            time.sleep(2 ** (attempt + 1))
            
    return None

def generate_explanation_for_question(q):
    subject = q.get("subject", "")
    q_num = q.get("number", "")
    correct_ans = q.get("answer", "")
    question_text = q.get("question", "")
    options = q.get("options", [])
    
    # 과목별 시스템 가이드라인 설정
    guide = ""
    if subject == "민법":
        guide = (
            "당신은 대한민국 민법 판례 및 이론 전문가입니다.\n"
            "이 문제는 감정평가사 1차 시험 민법 기출문제입니다.\n"
            "정답 선지가 왜 옳은지/틀린지 대법원 판례(예: 대판 2018.X.X, 2018다XXXX) 또는 민법 조문을 정확히 인용하여 해설을 작성하십시오.\n"
            "오답 선지들 또한 어떤 부분이 어떻게 잘못되었는지 조문과 판례에 근거해 상세히 논박하십시오.\n"
        )
    elif subject == "감정평가관계법규":
        guide = (
            "당신은 감정평가관계법규(국토계획법, 감정평가법, 부동산공시법, 국유재산법, 건축법 등) 전문가입니다.\n"
            "이 문제는 감정평가사 1차 시험 관계법규 기출문제입니다.\n"
            "관련 법률 조항(예: 국토의 계획 및 이용에 관한 법률 제O조 제O항)을 구체적이고 정확하게 명시하여 해설을 구성하십시오.\n"
            "오답 선지들도 법조문에 근거하여 틀린 부분을 꼼꼼하게 짚어주십시오.\n"
        )
    elif subject == "경제학원론":
        guide = (
            "당신은 거시/미시 경제학 교수이자 출제위원입니다.\n"
            "이 문제는 감정평가사 1차 시험 경제학원론 기출문제입니다.\n"
            "문제 해결에 필요한 경제학 모형, 정리, 수식 계산 과정을 상세하고 명확하게 작성하십시오.\n"
            "필요한 경우 LaTeX 수식 기호(예: $Y = C + I + G$)를 적절히 활용하여 계산의 전개 과정을 친절히 보여주십시오.\n"
        )
    elif subject == "회계학":
        guide = (
            "당신은 공인회계사(CPA)이자 대학 회계학 교수입니다.\n"
            "이 문제는 감정평가사 1차 시험 회계학 기출문제입니다.\n"
            "문제 이미지 또는 텍스트의 정보를 기반으로 분개(Journal entry), T-계정 흐름, 공식 대입 등 상세 계산 과정을 단계별로 서술하십시오.\n"
            "왜 특정 번호가 정답이며 나머지 선지들은 계산상 또는 이론상 왜 틀렸는지를 명확히 분별하여 적어주십시오.\n"
        )
    else:
        guide = (
            "당신은 감정평가사 1차 시험 부동산학원론 전문가입니다.\n"
            "정답의 정확한 법적/이론적 배경과 오답 선지들의 오류 원인을 꼼꼼히 밝혀 해설을 작성하십시오.\n"
        )

    prompt = (
        f"{guide}\n"
        f"--- 문제 정보 ---\n"
        f"- 과목: {subject}\n"
        f"- 문제 번호: {q_num}번\n"
        f"- 발표된 공식 정답: {correct_ans}번\n"
        f"- 문제 본문:\n{question_text}\n"
        f"- 선지 목록:\n" + "\n".join(options) + "\n\n"
        f"--- 작성 규칙 ---\n"
        f"1. 어투: 신뢰감을 주는 존댓말 또는 단정적인 문체(예: '~이다', '~한다')를 일관되게 사용하십시오. 존댓말과 단정적인 문체를 섞지 마십시오.\n"
        f"2. 반환 형식: 마크다운 문법을 사용하여 오직 해설 텍스트만 출력하십시오. 추가적인 머리말이나 인사말은 포함하지 마십시오.\n"
        f"3. ⚠️ 핵심 요구사항: 오답 선지(①~⑤ 중 정답이 아닌 선지 4개)도 각각에 대해 왜 틀렸는지 반드시 상세히 서술하십시오.\n"
    )

    # 이미지 분석 필요 여부 판별
    img_match = re.search(r'\[IMAGE:\s*(.*?)\]', question_text)
    if img_match:
        raw_img_name = img_match.group(1)
        img_path = get_normalized_image_path(raw_img_name)
        if img_path and os.path.exists(img_path):
            print(f"  -> Q{q_num}에 대한 이미지 파일 로드 성공: {img_path}")
            return query_gemini_with_image(prompt, img_path, f"{subject}_{q_num}")
        else:
            print(f"  -> [오류] Q{q_num}의 이미지 파일 매핑 실패: {raw_img_name}")
            # 이미지가 매핑되지 않은 경우, 텍스트 프롬프트로 대체 (선지만 보고 가능한 범위 시도)
            return query_gemini_text(prompt, f"{subject}_{q_num}_fallback")
    else:
        return query_gemini_text(prompt, f"{subject}_{q_num}")

def main():
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY가 없습니다. .env 파일을 확인해 주십시오.")
        return
        
    print("Questions DB 읽는 중...")
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    appraisal_2026 = [q for q in db if q.get('exam') == '감정평가사' and q.get('year') == '2026']
    
    # 해설이 비어있거나 누락된 문제 필터링
    to_generate = []
    for q in appraisal_2026:
        exp = q.get('explanation', '').strip()
        if not exp or exp == "해설이 없습니다." or "준비중" in exp:
            to_generate.append(q)
            
    print(f"2026년 감정평가사 기출문제 총 {len(appraisal_2026)}개 중 해설 누락 문항: {len(to_generate)}개")
    
    if not to_generate:
        print("모든 2026년도 기출문제에 해설이 이미 존재합니다.")
        return

    # 테스트 모드 여부
    test_mode = False
    
    if test_mode:
        print("--- 테스트 모드: 텍스트 1문제, 이미지(회계학) 1문제 해설 생성 시도 ---")
        text_q = None
        img_q = None
        for q in to_generate:
            if "[IMAGE:" in q.get("question", ""):
                if img_q is None: img_q = q
            else:
                if text_q is None: text_q = q
                
        targets = [t for t in [text_q, img_q] if t is not None]
        for q in targets:
            print(f"\n[테스트 출제] {q['subject']} Q{q['number']}")
            exp = generate_explanation_for_question(q)
            if exp:
                print("--- 생성된 해설 ---")
                print(exp[:500] + "...")
                print("-------------------")
            else:
                print("해설 생성 실패!")
    else:
        print("--- 전체 누락 해설 생성 시작 ---")
        success_count = 0
        
        for idx, q in enumerate(to_generate, 1):
            print(f"[{idx}/{len(to_generate)}] {q['subject']} Q{q['number']} 해설 생성 중...")
            exp = generate_explanation_for_question(q)
            
            if exp:
                q["explanation"] = exp.strip()
                # 임시 마크다운에 저장된 data_quality 플래그 갱신
                if "data_quality" in q:
                    q["data_quality"]["no_explanation"] = False
                
                success_count += 1
                print(f"  -> 완료! (성공 {success_count}/{idx})")
                
                # 매 성공시마다 즉시 DB 파일에 백업 저장하여 데이터 보존
                with open(DB_PATH, "w", encoding="utf-8") as f:
                    json.dump(db, f, ensure_ascii=False, indent=2)
            else:
                print(f"  -> [실패] {q['subject']} Q{q['number']} 해설을 생성하지 못했습니다.")
                
        print(f"\n🎉 작업 종료! 성공적으로 {success_count}개 문항의 해설을 보강했습니다.")

if __name__ == "__main__":
    main()
