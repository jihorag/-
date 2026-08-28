import json
import os
import re
import glob
import shutil

def process_cpa_2023_econ():
    # 1. Parse choices text
    raw_text = r"""
1번: ① 균형 가격/거래량 ② 가격상한제와 암시장 ③ 수요의 가격탄력성 ④ 소비자잉여 ⑤ 왈라스 안정성
2번: ① 가, 나 ② 가, 라 ③ 다, 라 ④ 가, 나, 다 ⑤ 나, 다, 라
3번: ① 1/16 ② 1/4 ③ 1/2 ④ 4 ⑤ 16
4번: ① 가~나~다 ② 가>나>다 ③ 가~나>다 ④ 다~나>가 ⑤ 다>나>가
5번: ① 12 ② 24 ③ 36 ④ 48 ⑤ 512
6번: ① Y재 지출액 증가 ② 대체효과 부재 ③ Y재 소득탄력성 ④ 소득 증가 시 X재 지출액 ⑤ Y재 가격 하락 시 소비량
7번: ① 노동수요곡선 존재 여부 ② 한계요소비용곡선 기울기 ③ 임금과 한계생산물가치 ④ 후생손실 크기 ⑤ 최저임금제 고용 효과
8번: ① 가, 나 ② 나, 라 ③ 다, 라 ④ 가, 나, 다 ⑤ 가, 나, 라
9번: ① 23 ② 35 ③ 40 ④ 48 ⑤ 54
10번: ① 가 ② 나 ③ 다 ④ 가, 나 ⑤ 가, 다
11번: ① 0.5 ② 1 ③ 1.5 ④ 2 ⑤ 4
12번: ① 20 ② 24 ③ 35 ④ 40 ⑤ 42
13번: ① 0 ② 1 ③ 2 ④ 3 ⑤ 4
14번: ① 노동 한계생산 체감 ② 자본 한계생산 체증 ③ 등량곡선 볼록성 ④ 생산량 2배 시 투입조합 거리 ⑤ 규모에 대한 수익
15번: ① 가 ② 나 ③ 다 ④ 나, 다 ⑤ 가, 나, 다
16번: ① 예산집합 크기 비교 ② 소득-소비 일치 시 변화 ③ 1기 차입 시 효과 방향 ④ 1기 저축 시 효과 방향 ⑤ 저축 시 차입 선택 가능성
17번: ① 750 ② 900 ③ 1,200 ④ 1,350 ⑤ 1,420
18번: ① 가 ② 나 ③ 다 ④ 가, 다 ⑤ 나, 다
19번: ① 가, 나 ② 다, 라 ③ 가, 나, 다 ④ 가, 나, 라 ⑤ 나, 다, 라
20번: ① 가 ② 나 ③ 다 ④ 가, 나 ⑤ 나, 다
21번: ① 가 ② 나 ③ 다 ④ 가, 나 ⑤ 나, 다
22번: (A, B 순) ① 1, 4 ② 2, 6 ③ 2, 8 ④ 4, 5 ⑤ 6, 5
23번: ① 가 ② 나 ③ 다 ④ 가, 나 ⑤ 나, 다
24번: ① 가 ② 나 ③ 가, 다 ④ 나, 다 ⑤ 가, 나, 다
25번: ① IS 가팔라짐, 총수요 완만 ② IS 완만, 총수요 가팔라짐 ③ 모두 완만 ④ 모두 가팔라짐 ⑤ 모두 좌측 이동
26번: ① 매각, 공급 증가, 수익률 상승 ② 매각, 공급 증가, 수익률 하락 ③ 매입, 수요 감소, 수익률 하락 ④ 매입, 공급 증가, 수익률 상승 ⑤ 매입, 수요 증가, 수익률 하락
27번: ① 2022년 국민소득 증가액 ② 2022년 소비 증가액 ③ 2022년 투자 증가액 ④ 2022년 정부지출 증가액 ⑤ 2022년 순수출 변화
28번: (민간저축, 정부저축 순) ① 200, -20 ② 220, -20 ③ 200, 20 ④ 220, 20 ⑤ 180, 0
29번: ① 가, 나 ② 가, 다 ③ 나, 다 ④ 다, 라 ⑤ 가, 나, 다
30번: ① A의 2012년 환산 연봉 ② B의 2012년 환산 연봉 ③ A의 2023년 환산 연봉 ④ B의 2003년 환산 연봉 ⑤ 2015년 가치 비교
31번: ① 가, 나 ② 가, 라 ③ 다, 라 ④ 가, 나, 다 ⑤ 나, 다, 라
32번: ① 500억원 ② 300억원 ③ 200억원 ④ 100억원 ⑤ 20억원
33번: ① 가 ② 나 ③ 가, 다 ④ 나, 라 ⑤ 가, 다, 라
34번: (총생산, 물가상승률, 명목이자율 순) ① 100, 3%, 7% ② 100, 5%, 4% ③ 100, 5%, 7% ④ 105, 5%, 4% ⑤ 105, 7%, 3%
35번: ① 1,185.77원 ② 1,196.00원 ③ 1,207.50원 ④ 1,219.11원 ⑤ 1,318.59원
36번: (균형이자율, 대차관계 순) ① 50%, A→B 100단위 대여 ② 50%, A→B 120단위 대여 ③ 25%, A→B 100단위 대여 ④ 25%, A→B 120단위 대여 ⑤ 0%, 대차관계 없음
37번: ① 2%p 하락 ② 1%p 하락 ③ 변화 없음 ④ 1%p 상승 ⑤ 2%p 상승
38번: ① 4단위 증가 ② 2단위 증가 ③ 변화 없음 ④ 2단위 감소 ⑤ 4단위 감소
39번: ① 소비세율 인상 ② 통화량 감소 ③ 수입규제 완화 ④ 정부 재정지출 감소 ⑤ 새로운 정책 불요
40번: ① 다음 기 1인당 자본 ② 황금률 도달 저축률 전략 ③ 황금률 도달 시 1인당 소비 ④ 균제상태 여부 ⑤ 동태적 효율성
    """
    
    # Parse choices
    choices_map = {}
    pattern = r"(\d+)번:\s*(.*?)(?=\d+번:|$)"
    matches = re.findall(pattern, raw_text, re.DOTALL)
    for num_str, content in matches:
        num = int(num_str)
        opts = re.split(r"[①②③④⑤]", content)
        opts = [o.strip() for o in opts if o.strip()]
        choices_map[num] = opts

    # 2. Answers for Econ (Page 2 of PDF)
    answers = [
        5, 4, 1, 1, 3, 2, 5, 5, 4, 5,
        4, 1, 3, 3, 5, 4, 4, 4, 4, 1,
        2, 2, 2, 5, 5, 1, 3, 2, 4, 5,
        4, 1, 3, 3, 2, 3, 1, 3, 2, 5
    ]

    # 3. Match images
    img_dir = "sources/기출문제/회계사/2023"
    files = glob.glob(os.path.join(img_dir, "스크린샷*.png"))
    files.sort(key=os.path.getmtime)
    
    print(f"Found {len(files)} screenshots for 2023 Econ.")
    
    target_img_dir = "images"
    new_questions = []
    
    for i, src in enumerate(files):
        q_num = i + 1
        img_name = f"cpa_2023_econ_{q_num}.png"
        dst = os.path.join(target_img_dir, img_name)
        shutil.copy2(src, dst)
        
        # Sync to viewer
        viewer_img_path = os.path.join("viewer/public/images", img_name)
        if os.path.exists("viewer/public/images"):
            shutil.copy2(src, viewer_img_path)
        
        new_questions.append({
            "id": f"cpa_2023_econ_{q_num}",
            "year": "2023",
            "exam": "회계사",
            "subject": "경제학원론",
            "number": str(q_num),
            "question": f"[IMAGE: ./images/{img_name}]",
            "options": choices_map.get(q_num, []),
            "answer": str(answers[i]),
            "explanation": "",
            "tags": {
                "subject": "경제학원론",
                "difficulty": 3
            }
        })

    # 4. Update DB
    db_path = "questions_db.json"
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            db = json.load(f)
    else:
        db = []
        
    db = [q for q in db if not q.get('id', '').startswith('cpa_2023_econ_')]
    db.extend(new_questions)
    
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        
    shutil.copy(db_path, "viewer/src/data/questions_db.json")
    print(f"Successfully added {len(new_questions)} CPA 2023 Economics questions.")

    # 5. Cleanup
    for f in files:
        os.remove(f)
    print("Source screenshots deleted.")

if __name__ == "__main__":
    process_cpa_2023_econ()
