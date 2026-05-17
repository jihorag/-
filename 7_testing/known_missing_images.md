# 소실 이미지 추적 (데이터 갭)

questions_db.json 의 `[IMAGE:]` 태그가 가리키지만 **원본을 복구할 수 없는** 이미지.
앱(`viewer` ParsedText)은 누락 이미지를 `[이미지 없음]` 으로 우아하게 대체하므로
화면은 깨지지 않는다. 아래는 콘텐츠가 실제로 비어 보이는 문항 기록.

| 이미지 | 문항 id | 시험 | 연도 | 번호 | 상태 |
|---|---|---|---|---|---|
| cek20220402m99.gif | cek20220402-99 | 감정평가사 | 2022 | 99 | **복구 불가** — 소스(cbtbank.kr)도 0바이트 응답 |

## 경위
- 2026-05-17 PNG/GIF→WebP 최적화 중 발견(0바이트 파일).
- 1_scraping 패턴(`https://cbtbank.kr/images/{ec}/{ec}{date}/{file}`)으로 재시도 →
  HTTP 200 이나 본문 0바이트. 소스에 원본이 없음.
- 같은 작업에서 다른 깨진 10건(cgx/we)은 동일 경로로 **복구 성공**.

## 재점검 방법
```
python3 - <<'PY'
import json,re,os
db=json.load(open('questions_db.json'))
pat=re.compile(r'\[IMAGE:\s*([^\]]+)\]'); have=set(os.listdir('viewer/public/images'))
res=lambda n:(n[:-4]+'.webp') if n.lower().endswith(('.png','.gif')) else n
miss={}
for q in db:
    b=(q.get('question')or'')+' '+' '.join(q.get('options')or q.get('choices')or[])+' '+(q.get('explanation')or'')
    for m in pat.findall(b):
        nm=m.strip().split('/')[-1]
        if res(nm) not in have: miss.setdefault(nm,[]).append(q.get('id'))
print(miss)
PY
```

## 후속(미결정)
해당 문항의 `[IMAGE:]` 태그 제거 또는 대체 캡션 삽입은 데이터 보정 작업으로 보류.
