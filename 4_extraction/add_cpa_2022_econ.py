import json
import os
import re
import shutil
import fitz

DB_PATH = "questions_db.json"
IMG_SRC_DIR = "/Users/jiho/감정평가사 기출문제/기출문제/회계사/2022/경제학"
IMG_DEST_DIR = "images"
ANS_PDF = "/Users/jiho/감정평가사 기출문제/기출문제/회계사/2022/_정답_2022.pdf"

choices_raw = """
## 1번 문항
* ① 가, 나
* ② 가, 다
* ③ 가, 라
* ④ 나, 다
* ⑤ 나, 라

## 2번 문항
* ① 생산자잉여 250, 자중손실 750
* ② 생산자잉여 750, 자중손실 750
* ③ 생산자잉여 750, 자중손실 1,500
* ④ 생산자잉여 1,750, 자중손실 750
* ⑤ 생산자잉여 2,750, 자중손실 1,500

## 3번 문항
* ① 가
* ② 나
* ③ 가, 나
* ④ 가, 다
* ⑤ 나, 다

## 4번 문항
* ① 가, 나
* ② 가, 라
* ③ 나, 다
* ④ 나, 라
* ⑤ 다, 라

## 5번 문항
* ① 생산함수는 규모에 대한 수익체감을 나타낸다.
* ② 생산요소간 대체탄력성이 1이다.
* ③ 한계기술대체율은 일정하다.
* ④ $w=1, r=3$인 경우, 총비용함수는 $TC(Q)=Q^{2}$ 이다.
* ⑤ $w=2, r=1$인 경우, 총비용함수는 $TC(Q)=\frac{1}{2}Q^{2}$이다.

## 6번 문항
* ① 80개, 10
* ② 80개, 20
* ③ 60개, 20
* ④ 40개, 15
* ⑤ 40개, 10

## 7번 문항
* ① 가, 나
* ② 나, 라
* ③ 다, 라
* ④ 가, 나, 다
* ⑤ 가, 다, 라

## 8번 문항
* ① $A>B>C$
* ② $A>C>B$
* ③ $B>A>C$
* ④ $B>C>A$
* ⑤ $C>B>A$

## 9번 문항
* ① 가
* ② 나
* ③ 다
* ④ 가, 나
* ⑤ 나, 다

## 10번 문항
* ① 2
* ② 3
* ③ 5
* ④ 7
* ⑤ 10

## 11번 문항
* ① 1
* ② 2
* ③ 3
* ④ 4
* ⑤ 5

## 12번 문항
* ① 소비자 1
* ② 소비자 2
* ③ 소비자 3
* ④ 소비자 1, 소비자 2
* ⑤ 소비자 2, 소비자 3

## 13번 문항
* ① 생산보조금 지급으로 균형가격은 단위당 10만큼 하락한다.
* ② 생산보조금 지급으로 거래량은 10단위 증가한다.
* ③ 정부의 보조금 지급으로 사회후생은 증가한다.
* ④ 정부의 총보조금 지급액은 250이다.
* ⑤ 생산자잉여는 정부의 총보조금 지급액만큼 증가한다.

## 14번 문항
* ① 부존효과(endowment effect)
* ② 심적회계방식(mental accounting)
* ③ 확실성효과(certainty effect)
* ④ 쌍곡선형 할인(hyperbolic discounting)
* ⑤ 닻내림효과(anchoring effect)

## 15번 문항
* ① 가, 나
* ② 가, 다
* ③ 나, 다
* ④ 나, 라
* ⑤ 다, 라

## 16번 문항
* ① $x_{1}=15, y_{1}=40$
* ② $x_{1}=20, y_{1}=40$
* ③ $x_{1}=30, y_{1}=50$
* ④ $x_{1}=50, y_{1}=40$
* ⑤ $x_{1}=60, y_{1}=30$

## 17번 문항
* ① 가
* ② 가, 다
* ③ 나, 라
* ④ 나, 다, 라
* ⑤ 가, 나, 다, 라

## 18번 문항
* ① 10.0%
* ② 12.5%
* ③ 20.0%
* ④ 50.0%
* ⑤ 52.5%

## 19번 문항
* ① 소비자잉여의 감소는 a+b+c+d이다.
* ② 대국의 사회적 후생 증가 조건은 c>b+c 이다.
* ③ c는 국내 소비자에게 전가되는 관세 부담이다.
* ④ e는 관세의 교역조건 효과이다.
* ⑤ 생산자잉여의 증가는 a이다.

## 20번 문항
* ① 무역 이전, $\frac{X\text{재의 가격}}{Y\text{재의 가격}}$은 A국이 B국보다 낮다.
* ② 무역 이전, $\frac{\text{단위당 노동사용보수}}{\text{단위당 자본사용보수}}$는 B국이 A국보다 낮다.
* ③ A국은 X재를, B국은 Y재를 각각 불완전특화 생산하여 수출한다.
* ④ 무역의 결과, 양국 간 단위당 노동사용보수의 격차는 감소하지만 단위당 자본사용보수의 격차는 증가한다.
* ⑤ 무역의 결과, A국의 자본 소유자의 실질소득은 감소한다.

## 21번 문항
* ① 1,150원/달러
* ② 1,100원/달러
* ③ 1,050원/달러
* ④ 1,000원/달러
* ⑤ 950원/달러

## 22번 문항
* ① 가
* ② 나
* ③ 가, 다
* ④ 나, 다
* ⑤ 가, 나, 다

## 23번 문항
* ① A: 4, B: 6, C: 102
* ② A: 5, B: 5, C: 102
* ③ A: 5, B: 6, C: 103
* ④ A: 5, B: 6, C: 102
* ⑤ A: 4, B: 5, C: 103

## 24번 문항
* ① 투자 100, 공공저축 80
* ② 투자 150, 공공저축 90
* ③ 투자 200, 공공저축 100
* ④ 투자 250, 공공저축 110
* ⑤ 투자 300, 공공저축 120

## 25번 문항
* ① 균형이자율 0.5, A의 1기 소비 1/2
* ② 균형이자율 0.5, A의 1기 소비 3/4
* ③ 균형이자율 0.2, A의 1기 소비 1/4
* ④ 균형이자율 0.2, A의 1기 소비 1/2
* ⑤ 균형이자율 0.0, A의 1기 소비 3/4

## 26번 문항
* ① 2.0%
* ② 3.5%
* ③ 5.0%
* ④ 7.0%
* ⑤ 9.0%

## 27번 문항
* ① 저축곡선은 양(+)의 기울기를 갖는다.
* ② 투자곡선은 수직이다.
* ③ 정부지출이 증가하면 실질이자율은 상승한다.
* ④ 소비가 외생적으로 증가해도 소득은 불변이다.
* ⑤ 노동 공급이 감소하면 실질이자율은 상승한다.

## 28번 문항
* ① 250만 명, 16.67%
* ② 250만 명, 17.84%
* ③ 250만 명, 18.32%
* ④ 300만 명, 16.67%
* ⑤ 300만 명, 17.84%

## 29번 문항
* ① 50
* ② 60
* ③ 70
* ④ 80
* ⑤ 90

## 30번 문항
* ① 황금률 균제상태에 부합하는 저축률은 0.5이다.
* ② 황금률 균제상태에서 1인당 생산은 2.5이다.
* ③ 황금률 균제상태에서 1인당 소비는 현재의 균제상태에서 보다 크다.
* ④ 황금률 균제상태에 도달하기 전까지 1인당 자본의 증가율은 0보다 작다.
* ⑤ 황금률 균제상태에 도달하기 전까지 1인당 자본과 1인당 생산의 증가율은 같다.

## 31번 문항
* ① 2.0
* ② 2.5
* ③ 3.0
* ④ 3.5
* ⑤ 4.0

## 32번 문항
* ① 2.5
* ② 3.0
* ③ 3.5
* ④ 4.0
* ⑤ 4.5

## 33번 문항
* ① 1.4%
* ② 2.4%
* ③ 3.4%
* ④ 4.4%
* ⑤ 5.4%

## 34번 문항
* ① 89만 명
* ② 99만 명
* ③ 109만 명
* ④ 119만 명
* ⑤ 129만 명

## 35번 문항
* ① 갑국의 2010년 GDP디플레이터는 50이다.
* ② 갑국의 2010년과 2015년 사이의 실질GDP 성장률은 2015년과 2020년 사이의 실질GDP 성장률에 비해 100%포인트 높다.
* ③ 을국은 2010년에 비해 2015년에 물가수준이 상승하였다.
* ④ 을국의 2015년 물가수준은 기준년도 물가수준보다 낮다.
* ⑤ 2015년 대비 2020년 물가상승률은 갑국이 을국보다 높다.

## 36번 문항
* ① 0%
* ② 1%
* ③ 2%
* ④ 3%
* ⑤ 4%

## 37번 문항
* ① 소득 불변, 소득 증가
* ② 소득 감소, 소득 불변
* ③ 소득 감소, 소득 증가
* ④ 소득 감소, 소득 감소
* ⑤ 소득 증가, 소득 감소

## 38번 문항
* ① (가)의 경우 실질화폐잔고 수요의 이자율탄력성이 0보다 크다.
* ② (나)의 경우 실질화폐잔고 수요의 소득탄력성이 0보다 크다.
* ③ (가)의 경우 LM곡선은 수평선의 형태를 갖는다.
* ④ (나)의 경우 통화량을 늘리더라도 총수요가 증가하지 않는다.
* ⑤ (가)의 경우 재정지출을 늘리더라도 총수요가 증가하지 않는다.

## 39번 문항
* ① 갑국에서 통화량이 증가하였다.
* ② 갑국에서 IS곡선이 좌측 이동하였다.
* ③ 갑국에서 물가가 하락하였다.
* ④ 갑국 정부의 재정적자가 감소하였다.
* ⑤ 갑국에서 AS곡선이 우측 이동하였다.

## 40번 문항
* ① 가
* ② 나
* ③ 가, 나
* ④ 나, 다
* ⑤ 가, 나, 다
"""

def extract_answers_cpa_econ(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    
    ans_map = {}
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    found_econ = False
    for i, line in enumerate(lines):
        if "경제원론" in line and "1교시" in line:
            found_econ = True
            j = i + 1
            while j < len(lines):
                parts = lines[j].split()
                for k in range(0, len(parts)-1, 2):
                    try:
                        num = int(parts[k])
                        ans = parts[k+1]
                        if 1 <= num <= 40:
                            ans_map[num] = ans
                    except: pass
                if j > i + 20: break
                j += 1
            break
    return ans_map

def main():
    # 1. Parse choices
    choices = {}
    pattern = r"## (\d+)번 문항\n(.*?)(?=\n##|$)"
    matches = re.findall(pattern, choices_raw, re.DOTALL)
    for num_str, content in matches:
        num = int(num_str)
        opts = [o.strip() for o in re.split(r"[①②③④⑤]", content) if o.strip()]
        choices[num] = opts

    # 2. Extract answers
    answers = extract_answers_cpa_econ(ANS_PDF)
    print(f"Extracted {len(answers)} answers from PDF.")

    # 3. Sort image files by creation time
    img_files = [f for f in os.listdir(IMG_SRC_DIR) if f.endswith(".png") and "스크린샷" in f]
    img_files.sort(key=lambda x: os.path.getctime(os.path.join(IMG_SRC_DIR, x)))

    # 4. Prepare DB items
    new_items = []
    for i in range(1, 41):
        q_id = f"cpa_2022_econ_{i}"
        if i <= len(img_files):
            img_src = os.path.join(IMG_SRC_DIR, img_files[i-1])
            img_dest = os.path.join(IMG_DEST_DIR, f"{q_id}.png")
            shutil.copy(img_src, img_dest)
        
        item = {
            "id": q_id,
            "year": "2022",
            "exam": "회계사",
            "subject": "경제학",
            "number": str(i),
            "question": f"[IMAGE: ./images/{q_id}.png]",
            "options": choices.get(i, []),
            "answer": answers.get(i, "")
        }
        new_items.append(item)

    # 5. Update DB
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    db = [q for q in db if not q.get("id", "").startswith("cpa_2022_econ_")]
    db.extend(new_items)
    
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    shutil.copy(DB_PATH, "viewer/src/data/questions_db.json")
    print(f"Successfully added {len(new_items)} questions to DB.")

if __name__ == "__main__":
    main()
