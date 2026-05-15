import json
import re

raw = """
PART. 01 미시경제학
1장 경제학의 기초 9
2장 수요－공급 10
3장 탄력성 13
4장 수요－공급이론의 응용 18
5장 무차별곡선이론 22
6장 현시선호이론 32
7장 소비자이론의 응용 34
8장 불확실성하의 선택이론 35
9장 생산함수 37
10장 비용함수 42
11장 완전경쟁시장 47
12장 독점시장 51
13장 독점적 경쟁시장 61
14장 과점시장 62
15장 게임이론 65
16장 요소시장 70
17장 일반균형이론 76
18장 후생경제학 79
19장 시장 실패 80
20장 정보경제학 86

PART. 02 거시경제학
1장 국민소득의 측정과 경제구조 91
2장 고전학파의 국민소득결정이론 98
3장 케인즈의 국민소득결정이론 100
4장 소비함수론 103
5장 투자함수론 105
6장 금융제도와 화폐공급 107
7장 화폐수요와 금융정책 110
8장 IS－LM과 정책효과 112
9장 총수요－총공급 122
10장 물가와 인플레이션 128
11장 노동시장과 실업 132
12장 필립스곡선과 스태그플레이션 135
13장 각 학파 모형의 주요 내용 139
14장 안정화정책과 관련된 논쟁 141
15장 경제변동론 144
16장 경제성장론 145
17장 국제무역이론 153
18장 무역정책론 154
19장 환율 155
20장 국제수지론 158
"""

lines = raw.strip().split('\n')
eco_taxonomy = []
cur_part = None

for l in lines:
    l = l.strip()
    if not l: continue
    
    # Remove page numbers at the end
    l = re.sub(r'\s+\d+$', '', l).strip()
    
    if l.startswith("PART"):
        cur_part = {"name": l.replace("PART. ", "PART 0").replace("PART.", "PART 0"), "children": []}
        eco_taxonomy.append(cur_part)
    elif "장 " in l:
        if cur_part:
            cur_part["children"].append({"name": l})

with open("taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy = json.load(f)

taxonomy["경제학원론"] = eco_taxonomy

with open("taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(taxonomy, f, ensure_ascii=False, indent=2)

print("Updated 경제학원론 in taxonomy.json")
