# 소실 이미지 추적 (데이터 갭)

questions_db.json 의 `[IMAGE:]` 태그가 가리키지만 **원본을 복구할 수 없는** 이미지.
앱(`viewer` ParsedText)은 누락 이미지를 `[이미지 없음]` 으로 우아하게 대체하므로
화면은 깨지지 않는다. 아래는 콘텐츠가 실제로 비어 보이는 문항 기록.

| 이미지 | 문항 id | 시험 | 연도 | 번호 | 상태 |
|---|---|---|---|---|---|
| cek20220402m99.gif | cek20220402-99 | 감정평가사 | 2022 | 99 | **복구 불가** — 소스(cbtbank.kr)도 0바이트 응답 |

## 경위
- 2026-05-17 PNG/GIF→WebP 최적화 중 발견(0바이트 파일).
- pipeline/1_scraping 패턴(`https://cbtbank.kr/images/{ec}/{ec}{date}/{file}`)으로 재시도 →
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

---

# 데이터 품질 보정 결과 (2026-05-17)

`questions_db.json` `data_quality` 필드로 플래그됨. 앱은 런타임에서 우아하게 degrade
(무효정답=채점제외, 보기없음=안내, 해설없음=판정만). 백업: `pipeline/6_db_utils/backup/questions_db.*pre_quality.json`.

분류 노출 10,360문항 기준:
- **정상 채점 가능 9,657**
- `answer_normalized` 40 — 원문자 정답 ①②③ → 숫자 (1단계, 영구 보정 완료)
- `no_answer` 703 — 정답 무효/빈/센티넬 (채점 제외)
- `no_options` 298 — 보기 없음
- `no_explanation` 1,399 — 해설 없음 (노출은 유지, 판정만 표시)

**왜 자동 복구 안 했나**: 2단계(재수집) — 결손 문항은 cbtbank 소스코드/`source_url`
없고 PDF 추출 출처라 회수 0. 3단계(LLM 재도출) — gpt-4o-mini/gpt-4o/gpt-5-mini/o4-mini
4개 측정, 최고 gpt-4o **54%@high** (랜덤 20% 대비 무의미 수준, 그림·계산 의존 문항이
다수). 학습 DB에 50%대 정답 주입은 플래그보다 해로워 **3단계 비채택**.

재집계: `python3 pipeline/6_db_utils/flag_quality.py` / 원문자 정규화: `normalize_answers.py`.
개별 문항을 사람이 풀어 정답을 채우는 수작업 보정만 추가로 가능(고비용·범위 외).
