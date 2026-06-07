#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""부동산학원론 연습문제 일괄 고품질 생성 및 DB 통합 스크립트 (Gemini 무료 API 병렬 스로틀링 버전).
교재 마크다운 파일을 파싱해 각 단원에 맞는 실제 감정평가사 1차 부동산학원론 시험 수준의 고품질 5지선다 문항을 출제합니다.
"""
import os
import re
import json
import time
import urllib.request
import urllib.error
import threading
from concurrent.futures import ThreadPoolExecutor

ROOT = "/Users/hanjiho/Documents/감정평가사 기출문제"
PRACTICE_DIR = os.path.join(ROOT, "viewer/public/data/practice/realestate")
TAX_INDEX = os.path.join(ROOT, "viewer/public/data/study/realestate/ai_taxonomy_index.json")

# 병렬 요청 속도 조절용 락 및 전역 타이머 (무료 API 15 RPM 한도 준수)
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

def slugify(s):
    s = re.sub(r'[^\w가-힣]', '_', s)
    return re.sub(r'_+', '_', s).strip('_')

def get_textbook_context(leaf):
    try:
        unit_file = leaf["unit_file"]
        lines_range = leaf["section_lines"]
        unit_path = os.path.join(ROOT, "viewer/public/data/study/realestate", unit_file)
        
        if not os.path.exists(unit_path):
            return "No textbook context file found."
            
        with open(unit_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        start = max(0, lines_range[0] - 1)
        end = min(len(lines), lines_range[1])
        return "".join(lines[start:end])
    except Exception as e:
        return f"Error reading textbook context: {e}"

def query_gemini(prompt, system_prompt, filename_log):
    global last_request_time
    
    # 락을 획득하여 요청 간 간격을 최소 4.5초 확보 (최대 13.3 RPM)
    with api_lock:
        now = time.time()
        elapsed = now - last_request_time
        if elapsed < 4.5:
            time.sleep(4.5 - elapsed)
        last_request_time = time.time()
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }],
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.4
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
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
            
    raise Exception(f"API query failed for {filename_log} after multiple retries.")

def clean_and_validate_questions(questions, count):
    if not isinstance(questions, list) or len(questions) != count:
        return None
    
    validated = []
    for q in questions:
        if not isinstance(q, dict):
            return None
        
        opts = q.get("options")
        q_text = q.get("question", "")
        
        if not opts or not isinstance(opts, list) or len(opts) != 5:
            # Try to extract options from question body using regex
            pattern = r'(①.*?)\n?(②.*?)\n?(③.*?)\n?(④.*?)\n?(⑤.*)'
            match = re.search(pattern, q_text, re.DOTALL)
            if match:
                opts = [m.strip() for m in match.groups()]
                q_text = q_text[:match.start()].strip()
                q["question"] = q_text
                q["options"] = opts
            else:
                return None
                
        if not isinstance(opts, list) or len(opts) != 5:
            return None
            
        ans = q.get("answer")
        if not ans or str(ans) not in ["1", "2", "3", "4", "5"]:
            return None
            
        validated.append(q)
        
    return validated

def generate_batch(leaf, start_num, count, id_prefix, context):
    system_prompt = (
        "당신은 대한민국 감정평가사 1차 시험 부동산학원론 출제위원입니다. "
        "제공된 교재 텍스트를 바탕으로, 실제 매우 어렵게 출제되었던 2026년도 감정평가사 1차 시험 수준의 초고난도 부동산학원론 연습문제를 출제하십시오. "
        "단순한 용어 정의나 단편적 암기식 문항은 철저히 배제하고, 복잡한 법조문 해석, 2~3단계의 복합 계산, 판례 대립, 그리고 다중 선지 분석이 필요한 고난도 문항을 구성해 주십시오. "
        "선지(options)는 반드시 ①, ②, ③, ④, ⑤ 기호로 시작해야 합니다."
    )
    
    prompt = (
        f"단원 정보:\n"
        f"- 대단원: {leaf['path'][0]}\n"
        f"- 중단원: {leaf['path'][1]}\n"
        f"- 소단원: {leaf['path'][2] if len(leaf['path']) > 2 else ''}\n\n"
        f"--- 교재 내용 --\n"
        f"{context}\n\n"
        f"--- 출제 요건 ---\n"
        f"1. 생성할 문항 수: {count}개 (ID 번호는 {id_prefix}-{start_num:03d} 부터 {id_prefix}-{start_num+count-1:03d} 까지 순차 부여)\n"
        f"2. 난이도 분포: **난이도 3(어려움)부터 5(매우 어려움)까지로만 구성**하며, 평균 난이도를 4.0 이상으로 타겟팅하십시오. (난이도 1~2의 단순한 기본 문항 출제 절대 금지)\n"
        f"3. 문제 유형 가이드라인:\n"
        f"   - **이론형**: 법률 조항(건축법상 대지산정, 국토계획법상 용도지역 건폐율/용적률 예외 규정, 공인중개사법/부동산등기법 판례, 감정평가 및 감정평가사에 관한 법률, 감칙 등)의 구체적인 세부 예외 규정이나 까다로운 문맥 해석을 요구하는 문제.\n"
        f"   - **계산형**: 경제론(수요·공급 탄력성 및 지점 탄력성), 투자론(LTV/DTI/DSR 한도 계산, 순현재가치(NPV), 내부수익률(IRR), 포트폴리오 가중평균수익률 및 분산), 입지론(입지계수(LQ), 허프의 상업유인력), 감정평가론(원가법의 정액법 감가 수정, 수익환원법의 부채감당법 및 환원율 계산) 등 반드시 실제 수치 대입 및 2~3단계 복합 연산이 필요한 문제 출제 및 수식 상세 기술.\n"
        f"   - **결합형/개수형**: 다수의 보기(ㄱ, ㄴ, ㄷ, ㄹ, ㅁ)를 제시하고 '옳은 것을 모두 고른 것은?' 또는 '틀린 것의 개수는 몇 개인가?' 와 같은 최고난도 유형 적극 출제.\n"
        f"4. 5지선다 객관식 형식이며, answer 필드는 \"1\"~\"5\" 중 하나여야 합니다.\n"
        f"5. explanation(해설)에는 정답이 도출되는 명확한 근거(법조문 인용 또는 수식 풀이 과정)뿐만 아니라, 오답 선지 4개가 각각 이론/법리/계산상 왜 틀렸는지를 아주 상세하게 파헤쳐 서술하십시오.\n"
        f"6. 반환 형식: 반드시 다음 JSON 규격만을 출력하십시오.\n"
        f"{{\n"
        f"  \"questions\": [\n"
        f"    {{\n"
        f"      \"id\": \"{id_prefix}-{start_num:03d}\",\n"
        f"      \"difficulty\": 4,\n"
        f"      \"question_type\": \"계산형\",\n"
        f"      \"question\": \"...\",\n"
        f"      \"options\": [\"① ...\", \"② ...\", \"③ ...\", \"④ ...\", \"⑤ ...\"],\n"
        f"      \"answer\": \"3\",\n"
        f"      \"explanation\": \"...\"\n"
        f"    }},\n"
        f"    ...\n"
        f"  ]\n"
        f"}}\n"
    )
    
    for attempt in range(3):
        try:
            res_raw = query_gemini(prompt, system_prompt, f"{leaf['id']}_{start_num}")
            data = json.loads(res_raw)
            qs = data.get("questions", [])
            validated = clean_and_validate_questions(qs, count)
            if validated is not None:
                return validated
            print(f"  [{leaf['id']}_{start_num}] 검증 실패. 배치 재지정 요청 중... (시도 {attempt+1}/3)")
            time.sleep(2)
        except Exception as e:
            print(f"  [{leaf['id']}_{start_num}] 에러/검증 실패: {e}. 재시도 중...")
            time.sleep(2)
            
    # 최종 시도
    res_raw = query_gemini(prompt, system_prompt, f"{leaf['id']}_{start_num}_final")
    data = json.loads(res_raw)
    qs = data.get("questions", [])
    validated = clean_and_validate_questions(qs, count)
    if validated is not None:
        return validated
    return qs

def is_existing_file_valid(out_path):
    if not os.path.exists(out_path):
        return False
    # Only skip if the file was modified within the last hour (belonging to the current run)
    mtime = os.path.getmtime(out_path)
    if time.time() - mtime > 3600:
        return False
    try:
        with open(out_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        questions = data.get("questions", [])
        if len(questions) != 50:
            return False
        for q in questions:
            if "options" not in q or not isinstance(q["options"], list) or len(q["options"]) != 5 or "answer" not in q:
                return False
        return True
    except Exception:
        return False

def generate_for_leaf(leaf):
    leaf_id = leaf["id"]
    slug = slugify(leaf_id.replace("realestate__", ""))
    out_path = os.path.join(PRACTICE_DIR, f"{leaf_id}.json")
    
    if is_existing_file_valid(out_path):
        print(f"  [스킵] {leaf_id} (이미 유효한 50문항이 존재함)")
        return True
        
    # 50문항 ID prefix
    id_prefix = f"practice-realestate-{slug}"
    
    print(f"  [시작] {leaf_id} 문항 생성 중...")
    
    context = get_textbook_context(leaf)
    
    all_questions = []
    batch_size = 10
    for b in range(5):
        start_num = b * batch_size + 1
        print(f"  [진행] {leaf_id} Batch {b+1}/5 (Q{start_num}~Q{start_num+batch_size-1}) 생성 중...")
        questions_part = generate_batch(leaf, start_num, batch_size, id_prefix, context)
        if len(questions_part) != batch_size:
            print(f"  [경고] {leaf_id} Batch {b+1}에서 {batch_size}개 대신 {len(questions_part)}개 생성됨. 재시도.")
            questions_part = generate_batch(leaf, start_num, batch_size, id_prefix, context)
        all_questions.extend(questions_part)
        
    # ID 번호 정렬 및 보정
    for idx, q in enumerate(all_questions, 1):
        q["id"] = f"{id_prefix}-{idx:03d}"
        
    out_data = {
        "meta": {
            "subject": "부동산학원론",
            "chapter": leaf["path"][0],
            "section": leaf["path"][1],
            "item": leaf["path"][2] if len(leaf["path"]) > 2 else leaf["path"][1],
            "source": "practice-set",
            "version": "v1",
            "created": "2026-06-07",
            "count": len(all_questions)
        },
        "questions": all_questions
    }
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
        
    print(f"  [성공] {leaf_id} 생성 완료! (총 {len(all_questions)}문항 저장)")
    return True

def main():
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY가 존재하지 않습니다. .env를 확인하십시오.")
        return
        
    with open(TAX_INDEX, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    leaves = data.get("leaves", [])
    print(f"총 {len(leaves)}개 단원 발견.")
    
    # 테스트 모드 여부
    test_mode = False
    
    if test_mode:
        print("--- 테스트 모드 가동: 1개 단원만 생성해 품질 검증 ---")
        # 부동산학의 의미 단원 선택
        target_leaf = leaves[0]
        generate_for_leaf(target_leaf)
        print("테스트 파일 생성 성공. viewer/public/data/practice/realestate/ 내 첫 번째 파일을 검증해 보세요.")
    else:
        # 전체 단원 병렬 생성 (전역 락을 통해 13.3 RPM 속도 제한 준수하며 다중 워커 작동)
        print("--- 전체 101개 단원 병렬 생성 시작 ---")
        max_workers = 3
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(generate_for_leaf, leaves)
        print("모든 단원 문항 생성 완료!")

if __name__ == "__main__":
    main()
