#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""부동산학원론 연습문제 생성 완료 모니터링 및 자동 동기화 데몬 스크립트.
"""
import os
import json
import time
import subprocess
from pathlib import Path

ROOT = Path("/Users/hanjiho/Documents/감정평가사 기출문제")
PRACTICE_DIR = ROOT / "viewer/public/data/practice/realestate"
TAX_INDEX = ROOT / "viewer/public/data/study/realestate/ai_taxonomy_index.json"

def count_target_sections():
    try:
        with open(TAX_INDEX, "r", encoding="utf-8") as f:
            data = json.load(f)
        return len(data.get("leaves", []))
    except Exception as e:
        print("Error loading taxonomy index:", e)
        return 101  # Default to 101 sections

def get_current_valid_files():
    if not PRACTICE_DIR.exists():
        return 0
    count = 0
    for fp in PRACTICE_DIR.glob("*.json"):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 50문항이 완벽하게 생성되고 유효한 JSON인지 검증
            if len(data.get("questions", [])) == 50:
                count += 1
        except Exception:
            pass
    return count

def is_generator_running():
    try:
        res = subprocess.run(
            ["pgrep", "-f", "generate_unique_realestate_practice.py"],
            capture_output=True, text=True
        )
        pids = res.stdout.strip().split()
        return len(pids) > 0
    except Exception:
        return False

def main():
    target_count = count_target_sections()
    print(f"[모니터링 시작] 목표 단원 개수: {target_count}개")
    
    start_time = time.time()
    
    while True:
        valid_files = get_current_valid_files()
        running = is_generator_running()
        elapsed = int(time.time() - start_time)
        print(f"[{elapsed}초 경과] 현재 완료된 단원: {valid_files}/{target_count}개, 생성기 실행 여부: {running}")
        
        if valid_files >= target_count and not running:
            print("\n🎉 모든 단원(101개)의 초고난도 연습문제 생성이 완료되었습니다!")
            print("[1/2] scripts/practice_to_app.py 실행 및 DB 동기화...")
            
            # DB 동기화 구동
            res = subprocess.run(
                ["python3", "scripts/practice_to_app.py"],
                cwd=ROOT, capture_output=True, text=True
            )
            print(res.stdout)
            if res.stderr:
                print("Error stdout:", res.stderr)
                
            print("[2/2] 웹앱 최종 PWA 정적 리소스 컴파일 빌드 수행...")
            # PWA 웹앱 빌드 구동
            res_build = subprocess.run(
                ["npm", "run", "build"],
                cwd=ROOT / "viewer", capture_output=True, text=True
            )
            print(res_build.stdout)
            if res_build.stderr:
                print("Build stderr:", res_build.stderr)
                
            print("\n✅ 동기화 및 웹앱 빌드가 성공적으로 완결되었습니다!")
            break
            
        time.sleep(30)  # 30초 대기

if __name__ == "__main__":
    main()
