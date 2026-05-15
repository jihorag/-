import os
import json
import shutil
from pathlib import Path
import re

text_data = """
1번
① 소비
② 저축
③ 국내총생산
④ 외환보유고
⑤ 감가상각

2번
① 100
② 175
③ 200
④ 325
⑤ 375

3번
① 가
② 나
③ 다
④ 가, 나
⑤ 나, 다

4번
① 이 소비자에게 X재는 비재화이다.
② y값이 같다면 한계대체율은 x값에 관계없이 일정하다.
③ X재 수요곡선에 수평인 부분이 존재한다.
④ X재 수요곡선은 45°선을 기준으로 대칭이다.
⑤ X재에 대한 지출이 극대화되는 가격이 여러 개 존재한다.

5번
① 20
② 30
③ 40
④ 60
⑤ 80

6번
① (x,y)=(2,5)를 선택하면 약공리가 위배된다.
② (x,y)=(6,3)을 선택하면 약공리가 위배된다.
③ (x,y)=(8,2)를 선택하면 약공리가 위배된다.
④ (x,y)=(10,1)을 선택하면 약공리가 위배된다.
⑤ 예산선상의 어느 점을 선택하더라도 약공리가 위배되지 않는다.

7번
① 1/7
② 1/3
③ 2/3
④ 3/4
⑤ 4/5

8번
① 가, 나
② 가, 다
③ 나, 다
④ 나, 라
⑤ 다, 라

9번
① 0
② 1,000
③ 1,250
④ 1,875
⑤ 3,125

10번
① 건강 상태가 좋은 가입자의 의료보험료를 할인해준다.
② 화재가 발생한 경우 피해액의 일정 비율만을 보험금으로 지급한다.
③ 실손의료보험 가입자의 병원 이용 시 일정액을 본인이 부담하게 한다.
④ 실업보험 급여를 받기 위한 요건으로 구직 활동과 실업 기간에 대한 규정을 둔다.
⑤ 보험 가입 이후 가입기간 동안 산정한 안전운전 점수가 높은 가입자에게는 보험료 일부를 환급해준다.

11번
① u(x,y)=x
② u(x,y)=x+y
③ u(x,y)=y
④ u(x,y)=xy
⑤ u(x,y)=min{x,y}

12번
① 가, 나
② 가, 다
③ 나, 다
④ 나, 라
⑤ 다, 라

13번
① w>r이면 공정1만 사용된다.
② w<r이면 공정2만 사용된다.
③ w=r이면 공정2와 공정3이 동시에 사용될 수 있다.
④ 규모수익이 증가한다.
⑤ 이 기업의 비용함수는 선형이다.

14번
① 2y
② $\\sqrt{2}y$
③ $\\sqrt{2}$
④ $\\frac{1}{\\sqrt{2}}$
⑤ 2

15번
① 4.5
② 9
③ 12
④ 18
⑤ 36

16번
① 4
② 5
③ 6
④ 7
⑤ 8

17번
① 3
② 4
③ 5
④ 6
⑤ 7

18번
① 2/3
② 1
③ 3/2
④ $\\sqrt{\\frac{2}{3}}$
⑤ $\\sqrt{\\frac{3}{2}}$

19번
① 가
② 나
③ 다
④ 가, 나
⑤ 나, 다

20번
① A국은 모든 재화에 대해 절대우위를 갖는다.
② 교역 이전에 A국은 Y재를 100단위 생산한다.
③ 교역이 이루어지면 A국의 X재 생산량은 교역 이전의 두 배가 된다.
④ 교역이 이루어지면 A국과 B국의 X재 생산량 합계는 교역 이전에 비해 100단위 늘어난다.
⑤ 교역 전후 B국의 X재 소비량이 동일하다면 교역 이후 B국의 Y재 소비량은 125단위이다.

21번
① 가
② 나
③ 다
④ 가, 다
⑤ 나, 다

22번
① 가, 나
② 나, 다
③ 다, 라
④ 가, 나, 다
⑤ 가, 다, 라

23번
① 가파른, 가파른, 가파른
② 완만한, 가파른, 가파른
③ 가파른, 완만한, 가파른
④ 완만한, 완만한, 가파른
⑤ 완만한, 가파른, 완만한

24번
① 가, 나
② 가, 다
③ 나, 다
④ 나, 라
⑤ 다, 라

25번
① 새고전학파, 통화주의학파, 케인즈학파
② 새고전학파, 케인즈학파, 통화주의학파
③ 케인즈학파, 새고전학파, 통화주의학파
④ 케인즈학파, 통화주의학파, 새고전학파
⑤ 통화주의학파, 새고전학파, 케인즈학파

26번
① $\\frac{e+b}{n+b}$
② $\\frac{n+e}{n+b}$
③ $\\frac{n+e}{n+e+b}$
④ $\\frac{b}{n+e+b}$
⑤ $\\frac{e}{n+e+b}$

28번
① 가
② 나
③ 가, 나
④ 나, 다
⑤ 가, 다

29번
① $\\frac{1}{1+r}$
② $\\frac{1}{2+r}$
③ $\\frac{1}{3+r}$
④ $\\frac{r}{1+r}$
⑤ $\\frac{r}{2+r}$

30번
① 자본의 이동은 BP1인 경우보다 BP2인 경우에 더 자유롭다.
② 확장적 재정정책이 시행되면 BP1인 경우와 BP2인 경우 모두 이자율이 상승한다.
③ 확장적 재정정책에 따른 소득 증가효과는 BP1인 경우보다 BP2인 경우에 더 크다.
④ 확장적 재정정책에 따른 구축효과는 BP1인 경우보다 BP2인 경우에 더 크다.
⑤ 확장적 통화정책이 소득에 미치는 효과는 BP1인 경우와 BP2인 경우에 동일하다.

31번
① 상승, 상승 / 불변, 불변
② 하락, 상승 / 불변, 증가
③ 하락, 하락 / 불변, 증가
④ 불변, 하락 / 감소, 증가
⑤ 불변, 불변 / 감소, 증가

32번
① 한국은행이 IMF로부터 10억 달러를 차입했다.
② 외국 투자자들이 국내 증권시장에서 1억 달러어치의 국내 기업 주식을 매입했다.
③ 국내 기업 A가 특허권을 외국에 매각하고 20만 달러를 벌었다.
④ 외국에서 1년 미만 단기로 일하는 우리나라 근로자가 근로소득으로 받은 10만 달러를 국내로 송금했다.
⑤ 우리나라 정부가 개발도상국에 2천만 달러의 무상원조를 제공했다.

33번
① (가)-(나)-(다)
② (가)-(다)-(나)
③ (나)-(가)-(다)
④ (나)-(다)-(가)
⑤ (다)-(가)-(나)

34번
① A-B-C
② A-C-B
③ B-C-A
④ C-A-B
⑤ C-B-A

35번
① 1인당 자본이 감소한다.
② 1인당 생산이 감소한다.
③ 1인당 소비가 감소한다.
④ 1인당 생산 대비 1인당 소비 비율은 변하지 않는다.
⑤ 1인당 생산 대비 1인당 자본 비율은 변하지 않는다.

36번
① 명목환율이 하락한다.
② 명목이자율이 하락한다.
③ 소득이 감소한다.
④ 투자가 증가한다.
⑤ 소비가 감소한다.

37번
① 국공채 매입, 재정지출 확대
② 국공채 매입, 재정지출 축소
③ 국공채 매각, 재정지출 불변
④ 국공채 매각, 세금 인하
⑤ 국공채 매각, 세금 인상

38번
① 대부자금시장에서 저축곡선이 좌측 이동한다.
② IS-LM에서 IS곡선이 상향 이동한다.
③ AS-AD에서 AS곡선이 좌측 이동한다.
④ 화폐시장에서 실질화폐잔고 공급곡선이 좌측 이동한다.
⑤ 화폐시장에서 실질화폐잔고 수요곡선이 좌측 이동한다.

39번
① 변화 없음, 2% 포인트 증가
② 변화 없음, 2% 포인트 감소
③ 2% 포인트 증가, 2% 포인트 증가
④ 2% 포인트 감소, 2% 포인트 감소
⑤ 2% 포인트 증가, 변화 없음

40번
① F → I → J
② I → H → F
③ I → J → L
④ I → K → L
⑤ L → M → L
"""

q27_options = [
    "① $\\frac{M_1^x+M_1^y}{P_0^x\\frac{M_1^x}{P_1^x}+P_0^y\\frac{M_1^y}{P_1^y}}$",
    "② $\\frac{M_1^x+M_1^y}{P_1^x\\frac{M_1^x}{P_0^x}+P_1^y\\frac{M_1^y}{P_0^y}}$",
    "③ $\\frac{P_0^x\\frac{M_1^x}{P_1^x}+P_0^y\\frac{M_1^y}{P_1^y}}{M_0^x+M_0^y}$",
    "④ $\\frac{P_1^x\\frac{M_1^x}{P_0^x}+P_1^y\\frac{M_1^y}{P_0^y}}{M_0^x+M_0^y}$",
    "⑤ $\\frac{P_1^x\\frac{M_1^x}{P_0^x}+P_1^y\\frac{M_1^y}{P_0^y}}{P_0^x\\frac{M_1^x}{P_1^x}+P_0^y\\frac{M_1^y}{P_1^y}}$"
]

def parse_options(text):
    options_map = {}
    current_q = None
    
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        m = re.match(r'^(\d+)번', line)
        if m:
            current_q = int(m.group(1))
            options_map[current_q] = []
        elif line.startswith('①') or line.startswith('②') or line.startswith('③') or line.startswith('④') or line.startswith('⑤'):
            if current_q is not None:
                options_map[current_q].append(line)
                
    options_map[27] = q27_options
    return options_map

def main():
    options_map = parse_options(text_data)
    
    src_dir = Path("기출문제/회계사/2021/경제학")
    images = list(src_dir.glob("*.png"))
    # Sort images by filename to preserve chronological order of screenshots
    images.sort()
    
    if len(images) != 40:
        print(f"Warning: Expected 40 images, found {len(images)}.")
        
    db_path = "questions_db.json"
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    # Remove existing CPA 2021 경제학
    db = [q for q in db if not (q.get("exam") == "회계사" and q.get("year") == "2021" and q.get("subject") == "경제학")]
    
    os.makedirs("images", exist_ok=True)
    
    for i, img_path in enumerate(images):
        q_num = i + 1
        new_filename = f"cpa_2021_econ_{q_num}.png"
        new_path = os.path.join("images", new_filename)
        shutil.copy(img_path, new_path)
        
        opts = options_map.get(q_num, ["①", "②", "③", "④", "⑤"])
        
        q_data = {
            "id": f"cpa_2021_econ_{q_num}",
            "exam": "회계사",
            "year": "2021",
            "subject": "경제학",
            "number": str(q_num),
            "question": f"[IMAGE: {new_filename}]",
            "options": opts,
            "answer": "",
            "explanation": "",
            "tags": {}
        }
        db.append(q_data)
        
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        
    shutil.copy(db_path, "viewer/src/data/questions_db.json")
    print(f"✅ 2021년 회계사 경제학 {len(images)}문항 DB 등록 완료!")

if __name__ == "__main__":
    main()
