import json
import re

raw = """
PART 01 국토의 계획 및 이용에 관한 법률
Chapter 01 총칙
Chapter 02 광역도시계획
Chapter 03 도시·군기본계획
Chapter 04 도시·군관리계획
제1절 도시·군관리계획
제2절 용도지역·용도지구·용도구역
제3절 기반시설과 도시·군계획시설 등
제4절 지구단위계획구역과 지구단위계획
Chapter 05 개발행위의 허가 등
Chapter 06 보칙 및 벌칙

PART 02 건축법
Chapter 01 총칙
Chapter 02 건축물의 건축 등
Chapter 03 건축물의 대지와 도로
Chapter 04 건축물의 구조 및 재료
Chapter 05 지역 및 지구 안의 건축물
Chapter 06 특별건축구역, 건축협정, 결합건축, 벌칙

PART 03 도시 및 주거환경정비법
Chapter 01 총칙
Chapter 02 기본계획의 수립 및 정비구역의 지정
Chapter 03 정비사업의 시행
제1절 시행자 및 사업시행계획
제2절 관리처분계획 및 소유권이전

PART 04 공간정보의 구축 및 관리 등에 관한 법률
Chapter 01 총칙
Chapter 02 측량
Chapter 03 지적(地籍)
제1절 토지의 조사 및 등록
제2절 지번
제3절 지목
제4절 경계
제5절 면적
Chapter 04 지적공부
Chapter 05 토지의 이동 등
제1절 토지의 이동
제2절 등록사항의 정정 등

PART 05 부동산등기법
Chapter 01 총칙
Chapter 02 등기부 등
Chapter 03 등기절차
Chapter 04 표시에 관한 등기
Chapter 05 권리에 관한 등기
Chapter 06 이의신청

PART 06 국유재산법
Chapter 01 총칙
Chapter 02 총괄청
Chapter 03 행정재산
Chapter 04 일반재산
Chapter 05 지식재산 관리·처분의 특례
Chapter 06 대장과 보고 및 보칙

PART 07 부동산 가격공시에 관한 법률
Chapter 01 용어의 정의
Chapter 02 표준지공시지가
Chapter 03 개별공시지가
Chapter 04 주택가격의 공시
Chapter 05 비주거용 부동산가격의 공시
Chapter 06 부동산가격공시위원회

PART 08 감정평가 및 감정평가사에 관한 법률
Chapter 01 총칙
Chapter 02 감정평가사
Chapter 03 감정평가법인
Chapter 04 징계
Chapter 05 과징금
Chapter 06 보칙 및 벌칙

PART 09 동산.채권 등의 담보에 관한 법률
Chapter 01 동산담보권
Chapter 02 채권담보권
Chapter 03 담보등기
"""

lines = raw.strip().split('\n')
law_taxonomy = []
cur_part = None
cur_chapter = None

for l in lines:
    l = l.strip()
    if not l: continue
        
    if l.startswith("PART"):
        cur_part = {"name": l, "children": []}
        law_taxonomy.append(cur_part)
        cur_chapter = None
    elif l.startswith("Chapter"):
        cur_chapter = {"name": l, "children": []}
        if cur_part:
            cur_part["children"].append(cur_chapter)
    elif l.startswith("제") and "절" in l.split(" ")[0]:
        if cur_chapter:
            cur_chapter["children"].append({"name": l})

with open("taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy = json.load(f)

taxonomy["감정평가관계법규"] = law_taxonomy

with open("taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(taxonomy, f, ensure_ascii=False, indent=2)

print("Updated 감정평가관계법규 in taxonomy.json")
