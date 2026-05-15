import json

raw = """
제1편 민법총칙
제1장 민법 서론 _2
제2장 법률관계와 신의성실의 원칙 _6
제1절 법률관계와 권리·의무 6
제2절 신의성실의 원칙 8
제1관 서설 8
제2관 신의칙의 파생원칙 10
제3장 권리의 주체 _15
제1절 자연인 15
제1관 권리능력 15
제2관 의사능력 17
제3관 행위능력 19
제4관 자연인의 주소 · 제5관 부재와 실종 32
제2절 법인 42
제4장 권리의 객체 _66
제5장 권리의 변동 _73
제1절 총설 73
제2절 법률행위 74
제1관 총설 · 제2관 법률행위의 목적 74
제3절 의사표시 90
제1관 흠 있는 의사표시 90
제2관 의사표시의 효력발생 110
제4절 법률행위의 대리 114
제1관 서설 114
제2관 대리권 115
제3관 대리행위 119
제4관 복대리 122
제5관 무권대리 126
제5절 법률행위의 무효와 취소 141
제1관 무효 141
제2관 취소 148
제6절 법률행위의 부관 155
제1관 서설 · 제2관 조건 155
제3관 기한 161
제6장 기간 _165
제7장 소멸시효 _168
제1절 총설 · 제2절 소멸시효의 요건 168
제1관 소멸시효의 대상이 되는 권리 168
제2관 소멸시효의 기산점 171
제3관 소멸시효의 기간 175
제3절 시효의 장애 179
제1관 소멸시효의 중단 179
제2관 소멸시효의 정지 186
제4절 소멸시효 완성의 효과 187
제5절 제척기간 192

제2편 물권법
제1장 물권법 총설 _198
제1절 물권법 일반 · 제2절 물권변동 198
제3절 부동산 물권변동 204
제1관 법률행위에 의한 부동산 물권의 변동 204
제2관 법률행위에 의하지 않는 부동산물권의 변동 213
제3관 부동산 216
제4관 입목등기 및 명인방법 225
제4절 동산 물권 변동 228
제5절 물권의 소멸 235
제2장 점유권 _238
제1절 서론 238
제2절 점유권의 취득과 소멸 246
제3절 점유권의 효력 · 제4절 준점유 248
제3장 소유권 _257
제1절 총설 257
제2절 상린관계 257
제3절 소유권의 취득 267
제1관 총설 267
제2관 부동산 점유취득시효 267
제3관 부동산 등기부 취득시효 276
제4관 취득시효의 중단과 정지 등 278
제4절 기타 소유권의 취득 281
제5절 소유권에 기한 물권적 청구권 287
제6절 공동소유 292
제1관 총설 292
제2관 공유 292
제3관 합유 304
제4관 총유 305
제7절 명의신탁 308
제1관 총설 · 제2관 부동산 실권리자 명의 등기에 관한 법률 308
제3관 유효한 명의신탁에 관한 판례의 이론 319
제4장 용익물권 _322
제1절 지상권 322
제2절 지역권 337
제3절 전세권 342
제5장 담보물권 _354
제1절 총설 354
제2절 유치권 356
제3절 질권 367
제1관 동산질권 367
제2관 권리질권 371
제4절 저당권 375
제1관 총설 · 제2관 저당권의 성립 375
제3관 저당권의 효력 376
제4관 저당권의 처분 및 소멸 385
제5관 특수저당권 388
제5절 비전형담보 396
제1관 총설 · 제2관 가등기담보 396
제3관 양도담보 399
제4관 소유권유보부 매매 404
"""

import re
lines = raw.strip().split('\n')
taxonomy = {"민법": []}
cur_part = None
cur_chapter = None
cur_section = None
cur_sub = None

for l in lines:
    l = l.strip()
    if not l: continue
    # remove page numbers at the end (e.g. " _2", " 6")
    l = re.sub(r'(_\d+|\s+\d+)$', '', l).strip()
    
    if l.startswith("제") and "편" in l.split(" ")[0]:
        cur_part = {"name": l, "children": []}
        taxonomy["민법"].append(cur_part)
        cur_chapter = None
        cur_section = None
        cur_sub = None
    elif l.startswith("제") and "장" in l.split(" ")[0]:
        cur_chapter = {"name": l, "children": []}
        if cur_part is None:
            cur_part = {"name": "기본편", "children": []}
            taxonomy["민법"].append(cur_part)
        cur_part["children"].append(cur_chapter)
        cur_section = None
        cur_sub = None
    elif l.startswith("제") and "절" in l.split(" ")[0]:
        cur_section = {"name": l, "children": []}
        if cur_chapter is None: continue
        cur_chapter["children"].append(cur_section)
        cur_sub = None
    elif l.startswith("제") and "관" in l.split(" ")[0]:
        cur_sub = {"name": l}
        if cur_section is None: continue
        cur_section["children"].append(cur_sub)

with open("taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(taxonomy, f, ensure_ascii=False, indent=2)
print("Saved taxonomy.json")
