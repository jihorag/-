# 민법 v2 손작성 작업 인수인계서

> **작성일**: 2026-06-05
> **현재 진척**: 27/102 쟁점 (675문 / 2,550문) — Phase 1 S 100% 완료, Phase 2 A 4%
> **목적**: 다른 컴퓨터에서 작업을 끊김 없이 이어가기 위한 완전 가이드

이 문서 하나만 읽으면 **환경 설정 → 작업 규칙 → 다음 쟁점 작성 → 동기화 → 진척 갱신**까지 전 과정을 재현할 수 있도록 작성되었습니다.

---

## 0. 30초 요약

```bash
# 1) 저장소 clone & 의존성
git clone https://github.com/jihorag/-.git "감정평가사 기출문제"
cd "감정평가사 기출문제/viewer" && npm install && cd ..

# 2) dev 서버 (선택)
cd viewer && npm run dev   # http://localhost:5173

# 3) 다음 쟁점 작성 → JSON Write → 동기화
# 작성: viewer/public/data/practice/civil-law/civil-{gen|prop}-chNN-secNN-itemNN.json
python3 scripts/practice_to_app.py

# 4) 진척 갱신: docs/civil-law-question-generation-status.md §7
```

**다음 작성 쟁점 (Phase 2 A 등급, 우선순위 순)**:
1. `civil-gen-ch01-sec01-item01` 민법의 법원 (성문법·관습법·조리)
2. `civil-gen-ch01-sec02-item01` 신의성실 원칙·권리남용

---

## 1. 작업 환경

### 1.1 시스템 요구사항

| 항목 | 버전 | 비고 |
|---|---|---|
| OS | macOS / Linux | 윈도우는 path 구분자 조정 필요 |
| Node.js | **22.x** | `package.json` engines 명시 |
| npm | 10+ | Node 22 동봉 |
| Python | 3.10+ | 동기화 스크립트용 |
| Git | 최신 | |

### 1.2 저장소 정보

- **GitHub**: `https://github.com/jihorag/-.git`
- **메인 브랜치**: `main`
- **로컬 경로**: 한글 포함 `~/Documents/감정평가사 기출문제/` (한글 폴더명 그대로 유지 권장 — 일부 스크립트가 절대 경로 의존)

### 1.3 신규 컴퓨터 초기 설정 절차

```bash
# 1. 클론 (한글 경로 그대로 유지)
mkdir -p ~/Documents
cd ~/Documents
git clone https://github.com/jihorag/-.git "감정평가사 기출문제"
cd "감정평가사 기출문제"

# 2. viewer 의존성 설치
cd viewer
npm install
# (구버전 lockfile 충돌 시) npm install --legacy-peer-deps
cd ..

# 3. Python 가상환경(선택, .venv 이미 존재)
# python3 -m venv .venv
# source .venv/bin/activate

# 4. 동기화 1회 (정상 동작 확인)
python3 scripts/practice_to_app.py
# 마지막 라인 "✅ 앱 반영 완료" 떠야 정상

# 5. dev 서버 실행
cd viewer && npm run dev
# http://localhost:5173 에서 접속 → 감정평가사 → 민법 → 총칙/물권 경로로 v2 문제 확인
```

### 1.4 환경변수

- `.env` 파일이 이미 저장소에 존재 (Supabase 키 등). 그대로 사용.
- 별도 설정 불요.

---

## 2. 프로젝트 구조

### 2.1 디렉토리 트리 (작업 관련 핵심만)

```
감정평가사 기출문제/
├── docs/
│   ├── civil-law-question-generation-status.md    ⭐ 계획서 (이 작업의 모든 규칙·진척)
│   ├── econ-question-generation-status.md          (참고: 경제학 v2 작업)
│   ├── 경제학출제원칙.md
│   ├── 문제출제원칙.md
│   └── HANDOVER-civil-law-v2.md                    ⭐ 본 문서
│
├── viewer/                                          ★ React 19 + Vite 8 PWA
│   ├── public/
│   │   └── data/
│   │       ├── practice/
│   │       │   ├── civil-law/                       ★★ 작업 산출물 (27개 JSON)
│   │       │   │   ├── civil-gen-ch02-sec02-item01.json
│   │       │   │   └── ... (총 27개)
│   │       │   └── economics/                       (별도, 손대지 말 것)
│   │       ├── exams/00.json~13.json                (기출 chunk, 자동 생성)
│   │       └── manifest.json                        (자동 생성)
│   ├── src/
│   │   ├── App.jsx                                  메인 라우터
│   │   ├── ParsedText.jsx                           ⭐ KaTeX + ㄱㄴㄷ 박스 렌더링
│   │   └── ... (기타 컴포넌트)
│   ├── scripts/
│   │   ├── sync-data.mjs                            questions_db.json → exams chunk
│   │   └── build_civil.mjs                          민법 통암기 카드 빌더 (별개)
│   └── package.json
│
├── scripts/
│   └── practice_to_app.py                           ⭐ economics 동기화 (civil은 자동)
│
├── questions_db.json                                정본 (32MB, 18,339문)
├── taxonomy_v4.json                                 분류 트리
├── package.json                                     루트 (Node 22.x 선언)
└── .git/
```

### 2.2 손대지 말아야 할 것

- `viewer/public/data/practice/economics/` — 경제학 작업 결과 (감정평가사 v2 235관 중 미시·거시·국제 완료)
- `viewer/public/data/exams/00.json~13.json` — 자동 생성 (동기화 시 재생성)
- `questions_db.json` — 정본 (32MB). 동기화 스크립트가 자동 갱신
- `viewer/scripts/build_civil.mjs` — 민법 통암기 카드 (별개 기능, 이번 작업과 무관)

### 2.3 작업 대상 파일

**유일한 작업 대상**: `viewer/public/data/practice/civil-law/civil-*.json` 추가/수정

**부속 작업**:
- `docs/civil-law-question-generation-status.md` 진척률 §7 갱신
- (선택) `viewer/src/ParsedText.jsx` UI 개선

---

## 3. 현재 진척 (2026-06-05 기준)

### 3.1 누적 진척

| 항목 | 값 |
|---|---|
| **완료 쟁점** | **27 / 102 (26%)** |
| **완료 문항** | **675 / 2,550** |
| **Phase 1 S** | **25 / 25 ✅ 완료** |
| **Phase 2 A** | 2 / 52 (4%) |
| **Phase 3 B/C** | 0 / 25 |

### 3.2 완료된 27개 쟁점 (파일 목록)

**총칙 14개:**
1. `civil-gen-ch02-sec02-item01.json` — 미성년자와 법정대리인 (S)
2. `civil-gen-ch02-sec02-item02.json` — 성년·한정·특정후견 (S)
3. `civil-gen-ch03-sec03-item01.json` — 법인 권리·행위능력 (S)
4. `civil-gen-ch03-sec03-item02.json` — 법인 불법행위·대표권 남용 (S)
5. `civil-gen-ch04-sec01-item01.json` — 물건의 의의와 분류 (S)
6. `civil-gen-ch05-sec02-item02.json` — 반사회질서 법률행위 (S)
7. `civil-gen-ch05-sec02-item03.json` — 불공정 법률행위 (S)
8. `civil-gen-ch05-sec03-item01.json` — 비진의표시 (S)
9. `civil-gen-ch05-sec03-item02.json` — 통정허위표시 (S)
10. `civil-gen-ch05-sec03-item03.json` — 착오 (S)
11. `civil-gen-ch05-sec03-item04.json` — 사기·강박 (A) ★ Phase 2 첫 번째
12. `civil-gen-ch06-sec03-item01.json` — 복대리 (S)
13. `civil-gen-ch06-sec05-item01.json` — 제125조 표현대리 (S)
14. `civil-gen-ch06-sec05-item02.json` — 제126조 표현대리 (S)
15. `civil-gen-ch10-sec01-item01.json` — 소멸시효 일반 (S)

**물권 12개:**
16. `civil-prop-ch01-sec02-item01.json` — 부동산 물권변동 (S)
17. `civil-prop-ch01-sec03-item01.json` — 등기 종류·효력 (S)
18. `civil-prop-ch01-sec03-item03.json` — 가등기·등기 추정력 (S)
19. `civil-prop-ch01-sec04-item02.json` — 선의취득 (S)
20. `civil-prop-ch02-sec01-item01.json` — 점유 관념·자주·타주 (S)
21. `civil-prop-ch02-sec02-item01.json` — 점유자와 회복자 관계 (S)
22. `civil-prop-ch03-sec01-item01.json` — 소유권 내용·제한 (S)
23. `civil-prop-ch03-sec01-item02.json` — 물권적 청구권 (A) ★ Phase 2 두 번째
24. `civil-prop-ch04-sec03-item01.json` — 법정지상권 (S)
25. `civil-prop-ch06-sec01-item01.json` — 전세권 성립·존속기간 (S)
26. `civil-prop-ch07-sec01-item01.json` — 유치권 성립·견련성 (S)
27. `civil-prop-ch09-sec01-item01.json` — 저당권 성립·3대 성질 (S)

### 3.3 장별 capacity 진척 (100문 ≥ 보장 규칙)

| 편 | 장 | 진척 (쟁점/필수) | 진척 (문/100) |
|---|---|---:|---:|
| 총칙 | 제2장 인 | 2/8 | 50/200 |
| 총칙 | 제3장 법인 | 2/6 | 50/150 |
| 총칙 | 제4장 물건 | 1/4 | 25/100 |
| 총칙 | 제5장 법률행위 | 6/10 | 150/250 |
| 총칙 | 제6장 대리 | 3/8 | 75/200 |
| 총칙 | 제10장 소멸시효 | 1/4 | 25/100 |
| 물권 | 제1장 물권 총칙 | 4/8 | 100/200 ✓ |
| 물권 | 제2장 점유권 | 2/4 | 50/100 |
| 물권 | 제3장 소유권 | 2/8 | 50/200 |
| 물권 | 제4장 지상권 | 1/4 | 25/100 |
| 물권 | 제6장 전세권 | 1/4 | 25/100 |
| 물권 | 제7장 유치권 | 1/4 | 25/100 |
| 물권 | 제9장 저당권 | 1/6 | 25/150 |
| **그 외 6개 장** | (통칙·기간·조건기한·무효취소·지역권·질권·공동저당) | 0 | 0 |

---

## 4. 작성 규칙 (절대 준수 사항)

### 4.1 파일명 규칙

```
viewer/public/data/practice/civil-law/civil-{gen|prop}-ch{NN}-sec{NN}-item{NN}.json
                                            ↓        ↓     ↓      ↓
                                          영역코드  장   절    쟁점
```

- `gen`: 총칙 (제1편)
- `prop`: 물권 (제2편)
- `NN`: 2자리 0-pad (`01`, `02`, ..., `10`)

**예시**: `civil-gen-ch05-sec03-item04.json` = 총칙 제5장 제3절의 4번째 쟁점

### 4.2 JSON 스키마

```json
{
  "meta": {
    "subject": "민법",                                        // 고정
    "sub_subject": "총칙" | "물권",                            // 영역
    "chapter": "제5장 법률행위",                                // 실제 민법 편제
    "section": "제3절 의사표시",                                // 실제 민법 편제
    "item": "사기·강박에 의한 의사표시 (제110조)",                // 쟁점명 ★ "제N관" 표기 금지
    "source": "practice-set",                                  // 고정
    "version": "v2-handcrafted",                               // 고정
    "created": "2026-06-XX",                                   // 작성일
    "count": 25,                                               // 고정
    "mix_profile": "case5-statute5-judge5-theory7-combo3"      // 고정
  },
  "questions": [
    {
      "id": "practice-civil-{gen|prop}-chNN-secNN-itemNN-NNN", // 001~025
      "difficulty": 1 | 2 | 3 | 4 | 5,
      "question_type": "사례형" | "조문형" | "판례형" | "이론형" | "결합형",
      "question": "...발문... (다툼이 있으면 판례에 따름)",     // 발문 끝 단서 부착
      "options": [
        "①번 선지",
        "②번 선지",
        "③번 선지",
        "④번 선지",
        "⑤번 선지"
      ],
      "answer": "1" | "2" | "3" | "4" | "5",                  // 문자열
      "explanation": "...해설 80-200자..."                      // 조문·판례 인용 의무
    }
    // ... 25개
  ]
}
```

### 4.3 25문항 구성 표준 (mix_profile)

```
case5-statute5-judge5-theory7-combo3
```

| 유형 | 수 | 발문 길이 | 핵심 |
|---|---:|---|---|
| **사례형** | 5 | 100-160자 | 甲·乙·丙·丁 등장 (한자), 구체적 부동산명·금액·일자 |
| **조문형** | 5 | 40-55자 | 민법 제X조 요건·효과 정확 인용 |
| **판례형** | 5 | 40-60자 | 해설에 `대판 YYYY. MM. DD, YYYY다XXXXX` 필수 인용 |
| **이론형** | 7 | 40-50자 | 학설·체계·구별 |
| **결합형** | 3 | 옵션 50-80자 | ㄱ·ㄴ·ㄷ·ㄹ 형식, 박스 자동 렌더링됨 |

### 4.4 정답 번호 분포 (관당 25문)

**반드시 1-5번 균등 5개씩** (경제학과 다름!)

```python
target_seq = [(i % 5) + 1 for i in range(25)]
# = [1,2,3,4,5, 1,2,3,4,5, 1,2,3,4,5, 1,2,3,4,5, 1,2,3,4,5]
```

작성 직후 아래 Python 코드로 자동 재배치 (옵션 순서 swap):

```python
import json
from collections import Counter

path = 'viewer/public/data/practice/civil-law/civil-XXX-chNN-secNN-itemNN.json'
with open(path) as f:
    data = json.load(f)

target_seq = [(i % 5) + 1 for i in range(25)]
for i, q in enumerate(data['questions']):
    cur = int(q['answer'])
    new = target_seq[i]
    if cur != new:
        opts = q['options']
        opts[cur-1], opts[new-1] = opts[new-1], opts[cur-1]
        q['answer'] = str(new)

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('정답 분포:', dict(sorted(Counter(q['answer'] for q in data['questions']).items())))
# 기대: {'1': 5, '2': 5, '3': 5, '4': 5, '5': 5}
```

### 4.5 발문 극성 비율

- "옳지 않은 것은?" : **약 17문 (68%)**
- "옳은 것은?" : 약 6문 (24%)
- "아닌 것은? / 경우는?" : 약 2문 (8%)
- 기출 실측 4:1 비율 준수

### 4.6 발문 끝 단서 부착

```
(다툼이 있으면 판례에 따름)
```

판례형·사례형은 반드시 부착. 조문형·이론형은 선택. 기출 85.8%가 부착함.

### 4.7 난이도 분포

| 난이도 | 수 | 정답 자리 |
|---:|---:|---|
| 1 | 3 | 쉬운 정답 |
| 2 | 6 | |
| 3 | 9 | 균일 |
| 4 | 5 | 혼동 정답 |
| 5 | 2 | 어려운 정답 |

### 4.8 사례형 작성 템플릿

```
{등장인물 甲·乙·丙·丁}은 {목적물(X토지·Y건물·X부동산 등)}의 {권리관계}에
관하여 {상대방}과 {법률행위} 하였다. {추가 사실관계}.
다음 중 옳지 않은 것은? (다툼이 있으면 판례에 따름)
```

**규칙**:
- 등장인물: 한자 `甲 → 乙 → 丙 → 丁` 순 (4명 이내)
- 목적물: `X토지`, `Y건물`, `X아파트 201호`
- 금액: `1억 원`, `5천만 원` (한글 단위)
- 시점: `2024. 3. 1.` (감정평가사 출제 관례: 마침표 4개)
- 발문 본문 100-160자

### 4.9 판례 인용 형식

```
대판 1997. 3. 11, 96다49650
대판(전합) 1985. 4. 9, 84다카1131
대결 2021. 6. 10, 2020스596
```

- 띄어쓰기·마침표 정확히 (`대판 ` 뒤 띄어쓰기, `YYYY.` 마침표, ` MM.` 띄어쓰기+마침표)
- 사건번호: `XX다XXXXX`, `XX다카XXXX`, `XX스XXX` 등

### 4.10 NRT (Negative Response Tactics) — 오답 생성 5대 전략

1. **수치/기간 변경**: "10년" → "20년", "3년" → "5년"
2. **요건 누락/추가**: "선의·무과실" → "선의만"
3. **주체 뒤집기**: "채무자" → "물상보증인"
4. **효과 정반대**: "효력이 있다" → "효력이 없다"
5. **유사 제도 혼동**: 지상권 ↔ 전세권, 유치권 ↔ 동시이행항변권

### 4.11 함정 어휘 사전 (옵션에 자주 활용)

- "특별한 사정이 없는 한…" (기출 186회)
- "… 청구할 수 있다/없다" (187회)
- "원칙적으로…" (72회)
- "… 효력이 있다/없다" (121회)
- "… 취소할 수 있다/없다" (99회)
- "때에는 / 경우에는" (239회)
- "소유권이전등기를…" (143회)
- "무효이다/유효하다" (77회)

### 4.12 결합형 (ㄱㄴㄷㄹ) 작성

```json
"question": "X에 관한 설명으로 옳은 것을 모두 고른 것은? (다툼이 있으면 판례에 따름)\n\nㄱ. 진술 1\nㄴ. 진술 2\nㄷ. 진술 3\nㄹ. 진술 4",
"options": [
  "ㄱ, ㄴ, ㄷ",
  "ㄱ, ㄴ",
  "ㄴ, ㄷ",
  "ㄱ, ㄴ, ㄷ, ㄹ",
  "ㄷ, ㄹ"
]
```

**UI 렌더링**: `viewer/src/ParsedText.jsx` 가 `ㄱ./ㄴ./ㄷ./ㄹ./ㅁ.` 연속 라인을 자동으로 박스로 묶음 (회색 배경 + 좌측 강조선).

---

## 5. 동기화 절차

### 5.1 경제학·민법 동기화

```bash
cd ~/Documents/감정평가사\ 기출문제
python3 scripts/practice_to_app.py
```

**스크립트 동작**:
- `viewer/public/data/practice/economics/*.json` → `questions_db.json` 통합
- `node viewer/scripts/sync-data.mjs` 호출 → `questions_db.json` → `viewer/public/data/exams/*.json` chunk 분할
- 마지막에 `✅ 앱 반영 완료` 출력

**민법 처리**: `civil-law/*.json` 은 dev/build 시 `viewer/public/data/practice/civil-law/` 경로에서 그대로 읽힘. 별도 동기화 명령 불필요 — 위 스크립트 한 번 실행으로 충분 (Vite가 public/ 경로를 자동 서빙).

### 5.2 dev 서버

```bash
cd viewer
npm run dev
# → http://localhost:5173
```

- HMR(Hot Module Replacement) 작동 — JSON 파일 저장 시 자동 반영
- `predev` 훅이 `sync-data.mjs` + `build_civil.mjs` 자동 실행

### 5.3 빌드 (배포용)

```bash
cd viewer
npm run build
```

`prebuild` 훅이 sync 자동 수행. `dist/` 산출물을 Vercel/정적 호스팅.

---

## 6. 작성 워크플로 (한 쟁점 처리)

### 6.1 단계별 절차

```bash
# 1. 계획서 열기 (작성 우선순위 확인)
open docs/civil-law-question-generation-status.md
# §5 (작성 우선순위), §4 (트리), §6 (필수 판례 리스트) 참고

# 2. 다음 쟁점의 파일 경로 결정
# 예: 신의성실 원칙 → civil-gen-ch01-sec02-item01.json

# 3. JSON Write (25문 작성)
# 클로드 코드라면 Write tool 사용
# 수동 작성 시 IDE에서 새 파일 생성

# 4. 정답 분포 균등화 + 동기화 (한 명령)
python3 << 'PY'
import json
from collections import Counter

path = 'viewer/public/data/practice/civil-law/civil-gen-ch01-sec02-item01.json'
with open(path) as f:
    data = json.load(f)

target_seq = [(i % 5) + 1 for i in range(25)]
for i, q in enumerate(data['questions']):
    cur = int(q['answer'])
    new = target_seq[i]
    if cur != new:
        opts = q['options']
        opts[cur-1], opts[new-1] = opts[new-1], opts[cur-1]
        q['answer'] = str(new)

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(dict(sorted(Counter(q['answer'] for q in data['questions']).items())))
PY

python3 scripts/practice_to_app.py

# 5. 진척 갱신 (docs/civil-law-question-generation-status.md §7)
# - "누적 v2 완료": 27쟁점 (675문) → 28쟁점 (700문) 등으로 +1, +25
# - Phase 2 진척: 2/52 → 3/52
# - 장별 진척: 해당 장 +1쟁점 +25문

# 6. dev 서버에서 시각 확인
# http://localhost:5173 → 감정평가사 → 민법 → 해당 장
```

### 6.2 자체 검수 체크리스트 (작성 후 반드시 확인)

```python
import json
from collections import Counter

path = 'viewer/public/data/practice/civil-law/civil-XXX.json'
with open(path) as f:
    data = json.load(f)
qs = data['questions']

# 1. meta 검증
assert data['meta']['count'] == 25
assert data['meta']['mix_profile'] == 'case5-statute5-judge5-theory7-combo3'
assert data['meta']['version'] == 'v2-handcrafted'

# 2. ID 패턴
import re
for i, q in enumerate(qs):
    expected = f"-{i+1:03d}"
    assert q['id'].endswith(expected), f"ID 패턴 오류: {q['id']}"

# 3. 옵션 5개
for q in qs:
    assert len(q['options']) == 5

# 4. 정답 분포 균등
ans = Counter(q['answer'] for q in qs)
assert all(v == 5 for v in ans.values()), f"정답 불균등: {dict(ans)}"

# 5. 발문 극성 (옳지않은 ≥ 12)
nok = sum(1 for q in qs if '옳지 않은' in q['question'])
ok = sum(1 for q in qs if '옳은 것은' in q['question'] or '옳은 것을' in q['question'])
print(f'발문 극성: 옳지않은 {nok} / 옳은 {ok}')
assert nok >= 12

# 6. 유형 분포
qt = Counter(q['question_type'] for q in qs)
print('유형:', dict(qt))
# 사례 ≥ 4, 조문 ≥ 4, 판례 ≥ 4, 이론 ≥ 5, 결합 ≥ 2

# 7. 판례 인용
판례 = sum(1 for q in qs if '대판' in q.get('explanation', ''))
print(f'판례 인용 해설: {판례}문')
assert 판례 >= 3, "판례 인용 부족"

# 8. (다툼) 단서
다툼 = sum(1 for q in qs if '다툼이 있으면 판례' in q['question'])
print(f'(다툼) 부착: {다툼}문')
assert 다툼 >= 10

# 9. 甲乙 사례형
case = sum(1 for q in qs if '甲' in q['question'])
print(f'甲乙 사례: {case}문')
assert case >= 4

print('✅ 모든 검수 통과')
```

---

## 7. 다음 작업: 75개 미작성 쟁점

### 7.1 Phase 2 A 등급 (50개 남음)

**총칙 A 28개:**

| # | 파일 slug | 쟁점 |
|---|---|---|
| 1 | `civil-gen-ch01-sec01-item01` | 민법의 법원: 성문법·관습법·조리 |
| 2 | `civil-gen-ch01-sec02-item01` | 신의칙 일반·유형 |
| 3 | `civil-gen-ch01-sec02-item02` | 권리남용·실효·금반언 |
| 4 | `civil-gen-ch02-sec01-item01` | 자연인 권리능력 시기·종기 |
| 5 | `civil-gen-ch02-sec01-item02` | 태아의 권리능력 |
| 6 | `civil-gen-ch02-sec02-item03` | 제한능력자 상대방 보호 |
| 7 | `civil-gen-ch02-sec02-item04` | 속임수·법정추인·취소권 소멸 |
| 8 | `civil-gen-ch02-sec03-item01` | 부재자 재산관리 |
| 9 | `civil-gen-ch02-sec03-item02` | 실종선고·취소·효과 |
| 10 | `civil-gen-ch03-sec01-item01` | 법인 본질·종류·설립주의 |
| 11 | `civil-gen-ch03-sec04-item01` | 이사·감사·대표권 |
| 12 | `civil-gen-ch03-sec05-item01` | 사원총회·정관변경·해산·비법인사단 |
| 13 | `civil-gen-ch04-sec02-item01` | 부동산·동산 구별·정착물 |
| 14 | `civil-gen-ch04-sec03-item01` | 주물·종물 (제100조) |
| 15 | `civil-gen-ch05-sec01-item01` | 법률행위 종류·요건·해석 |
| 16 | `civil-gen-ch05-sec01-item02` | 법률행위 해석 (자연·규범·보충) |
| 17 | `civil-gen-ch05-sec02-item01` | 강행법규·임의법규·단속법규 |
| 18 | `civil-gen-ch05-sec03-item05` | 의사표시 효력발생·수령·공시송달 |
| 19 | `civil-gen-ch06-sec01-item01` | 대리 의의·종류·구별·사자 |
| 20 | `civil-gen-ch06-sec02-item01` | 대리권 발생·범위 (제118조) |
| 21 | `civil-gen-ch06-sec02-item02` | 대리권 소멸·쌍방대리·자기계약 |
| 22 | `civil-gen-ch06-sec04-item01` | 협의 무권대리·추인·상대방 보호 |
| 23 | `civil-gen-ch06-sec05-item03` | 제129조 표현대리 |
| 24 | `civil-gen-ch07-sec01-item01` | 무효 일반·절대·상대 무효 |
| 25 | `civil-gen-ch07-sec02-item01` | 취소권자·취소 의사표시·효과 |
| 26 | `civil-gen-ch07-sec02-item02` | 추인·법정추인·취소권 소멸 |
| 27 | `civil-gen-ch08-sec01-item01` | 정지·해제조건·기성·불능 |
| 28 | `civil-gen-ch10-sec01-item02` | 시효 기산점·소권 시효 |
| 29 | `civil-gen-ch10-sec02-item01` | 시효 중단사유 (제168-178조) |

**물권 A 22개:**

| # | 파일 slug | 쟁점 |
|---|---|---|
| 30 | `civil-prop-ch01-sec01-item01` | 물권법정주의·종류·물권적 청구권 |
| 31 | `civil-prop-ch01-sec02-item02` | 동산 물권변동·인도 |
| 32 | `civil-prop-ch01-sec03-item02` | 등기청구권·중간생략등기 |
| 33 | `civil-prop-ch01-sec04-item01` | 공시·공신의 원칙 |
| 34 | `civil-prop-ch02-sec01-item02` | 직접·간접 점유·점유보조자 |
| 35 | `civil-prop-ch02-sec03-item01` | 점유보호청구권·자력구제 |
| 36 | `civil-prop-ch03-sec02-item01` | 주위토지통행·인지·경계 (상린) |
| 37 | `civil-prop-ch03-sec03-item01` | 시효취득 (점유·등기) |
| 38 | `civil-prop-ch03-sec03-item02` | 첨부 (부합·혼화·가공) |
| 39 | `civil-prop-ch03-sec04-item01` | 공유 (제262-270조) |
| 40 | `civil-prop-ch03-sec04-item02` | 합유·총유 |
| 41 | `civil-prop-ch03-sec05-item01` | 부동산실명법·명의신탁 효력 |
| 42 | `civil-prop-ch04-sec01-item01` | 지상권 취득·존속기간·지료 |
| 43 | `civil-prop-ch04-sec01-item02` | 지상권 효력·소멸·갱신 |
| 44 | `civil-prop-ch04-sec02-item01` | 구분지상권·분묘기지권 |
| 45 | `civil-prop-ch05-sec01-item01` | 지역권 의의·요건·취득 |
| 46 | `civil-prop-ch05-sec02-item01` | 지역권자 권리·승계 |
| 47 | `civil-prop-ch06-sec02-item01` | 전세권 효력·우선변제 |
| 48 | `civil-prop-ch06-sec02-item02` | 전세권 양도·전세·임대·저당 |
| 49 | `civil-prop-ch06-sec03-item01` | 전세권 소멸·반환·법정갱신 |
| 50 | `civil-prop-ch07-sec02-item01` | 유치권 효력·경매 (제321-322조) |
| 51 | `civil-prop-ch08-sec01-item01` | 동산질권 성립·효력 |
| 52 | `civil-prop-ch08-sec02-item01` | 채권질권 (제346-353조) |
| 53 | `civil-prop-ch09-sec02-item01` | 저당권 효력 (피담보채권·저당부동산) |
| 54 | `civil-prop-ch09-sec02-item02` | 물상대위·일괄경매·경매 |
| 55 | `civil-prop-ch09-sec03-item01` | 공동저당 동시·이시배당 (제368조) |
| 56 | `civil-prop-ch09-sec04-item01` | 근저당 채권최고액·확정 |

### 7.2 Phase 3 B/C 등급 (25개)

총칙 B/C: 통칙 보조, 법인 설립·기관 보조, 권리객체 보조, 조건·기한 보조, 기간 4쟁점, 무효·취소 보조, 소멸시효 보조
물권 B/C: 지역권 보조, 질권 보조, 근저당 특수

자세한 목록은 `docs/civil-law-question-generation-status.md` §4 트리 참고.

### 7.3 권장 작업 순서 (재개 후)

```
[다음 2쟁점] 민법의 법원 + 신의칙 일반
[다음 2쟁점] 권리남용 + 자연인 권리능력
[다음 2쟁점] 태아의 권리능력 + 제한능력자 상대방 보호
... (한 턴에 2쟁점 페이스로 진행)
```

총 50개 / 2쟁점/턴 ≈ **25턴**으로 Phase 2 A 완료.

---

## 8. UI / 렌더링 (참고)

### 8.1 ParsedText.jsx 핵심 기능

[viewer/src/ParsedText.jsx](../viewer/src/ParsedText.jsx) 는 발문·옵션·해설을 렌더링.

지원 문법:
- **KaTeX**: `$x^2 + y^2 = z^2$` 인라인, `$$\frac{a}{b}$$` 디스플레이
- **이미지**: `[IMAGE: data/practice/.../graph.svg]`
- **볼드**: `**굵게**`
- **표**: 마크다운 파이프 `| col1 | col2 |`
- **헤더**: `# H1`, `## H2`
- **리스트**: `- item`, `* item`
- **ㄱㄴㄷ 박스**: `ㄱ. ...`, `ㄴ. ...`, `ㄷ. ...` 연속 시 자동 박스화 (회색 배경 + 좌측 강조선)
- **viz fence**: ` ```viz <template-name> ... ``` `, ` ```mermaid ... ``` `, ` ```svg ... ``` `

ㄱㄴㄷ 박스 코드 위치: [ParsedText.jsx:194-238](../viewer/src/ParsedText.jsx#L194-L238)

### 8.2 결합형 문항 UI 예시

JSON:
```json
"question": "...옳은 것을 모두 고른 것은?\n\nㄱ. 진술 1\nㄴ. 진술 2\nㄷ. 진술 3\nㄹ. 진술 4"
```

렌더링:
```
...옳은 것을 모두 고른 것은?

┌─────────────────────────────┐
│▎ㄱ. 진술 1                   │
│ ㄴ. 진술 2                   │
│ ㄷ. 진술 3                   │
│ ㄹ. 진술 4                   │
└─────────────────────────────┘
```

---

## 9. 알려진 함정·주의사항

### 9.1 정답 1번 몰빵 금지

경제학 v2 작업에서는 정답 1번에 몰빵했지만, **민법은 1-5번 균등 5문씩** (기출 실측 19-21% 균등).

작성 직후 `target_seq = [(i % 5) + 1 for i in range(25)]` 라운드로빈 재배치 필수.

### 9.2 "관" 단위 사용 금지

민법 시험범위(총칙+물권)에는 사실상 "제N관" 단위가 없음. `meta.item`에는 쟁점명만 기재.

❌ `"제1관 미성년자와 법정대리인"`
✅ `"미성년자와 법정대리인"`

### 9.3 등장인물 한자 사용

❌ 한글 "갑은 을에게..."
✅ 한자 "甲은 乙에게..."

기출 100% 한자 사용. 이미지 입력기로 입력 또는 복붙: `甲 乙 丙 丁`

### 9.4 시점 표기

❌ `2024-03-01` (대시)
❌ `2024년 3월 1일` (한글)
✅ `2024. 3. 1.` (마침표 4개)

### 9.5 동기화 후 questions_db.json 변경

`python3 scripts/practice_to_app.py` 실행 시 `questions_db.json` (32MB) 변경됨. git 커밋 시 포함.

### 9.6 ID 충돌 방지

같은 영역·장·절·쟁점 번호 사용 금지. 새 쟁점 작성 전 `viewer/public/data/practice/civil-law/` 디렉토리에서 동일 파일명 없는지 확인.

### 9.7 옵션 길이

기출 median 49자. 너무 짧으면(20자 미만) 학습 효용 ↓, 너무 길면(80자 초과) 가독성 ↓. **40-60자 범위 권장**.

### 9.8 발문 길이

기출 median: 비사례 46자, 사례 129자.
- 사례형: **100-160자**
- 그 외: **40-60자**

### 9.9 결합형 옵션 5개 패턴

기출 결합형 옵션 일반 패턴:
- `"ㄱ, ㄴ"`, `"ㄱ, ㄴ, ㄷ"`, `"ㄴ, ㄷ"`, `"ㄱ, ㄴ, ㄷ, ㄹ"`, `"ㄷ, ㄹ"`
- 또는 `"ㄱ"`, `"ㄱ, ㄴ"`, `"ㄴ, ㄷ"`, `"ㄴ, ㄹ"`, `"ㄷ, ㄹ"` 등

5개 모두 다른 조합. 정답은 1-5번 균등 분포.

### 9.10 판례 인용 정확성

작성 시 가짜 판례번호 만들지 말 것. 모를 때는 `대판 일관` 또는 `통설·판례` 정도로 표현.

확실히 알고 있는 판례만 인용:
- 대판(전합) 1995. 12. 21, 94다26721 (중간생략등기)
- 대판 2003. 1. 10, 2002다63558 (등기 추정력)
- 대판(전합) 2007. 4. 19, 2004다60072 (비법인사단)
- 대판 1997. 3. 11, 96다49650 (이중매매 적극가담)
- 대판(전합) 2015. 7. 23, 2015다200111 (형사사건 변호사 성공보수)
- 대판(전합) 2018. 9. 13, 2015다78703 (동기 착오)
- 대판(전합) 1985. 4. 9, 84다카1131 (관습법상 법정지상권)
- 대판(전합) 2012. 10. 18, 2010다52140 (법정지상권 재확인)
- 대판(전합) 1995. 2. 10, 94다55552 (전세권 우선변제)
- 대판(전합) 2005. 8. 19, 2005다22688 (유치권 경매 인수)
- 대판(전합) 1997. 8. 21, 95다28625 (자주점유 추정)
- 대판 2003. 4. 25, 2002다72439 (선의취득)
- 대판 1998. 7. 10, 98다1928 (제126조 정당이유)
- 대판 2004. 3. 26, 2003다34045 (대표권 남용)

---

## 10. 재개 명령어 (클로드 코드 사용 시)

다른 컴퓨터에서 클로드 코드로 재개할 때:

```
"민법 문제 생성 이어가"
"민법 다음 쟁점 작성"
"민법 Phase 2 계속"
"민법 자동으로 계속 진행해줘"
```

이런 자연어 명령에 대해 클로드 코드는:

1. `docs/civil-law-question-generation-status.md` 를 Read
2. `~/.claude/projects/.../memory/civil-law-question-generation.md` 를 Read (메모리 시스템 활성 시)
3. §7 진척률에서 마지막 완료 쟁점 확인
4. §5 우선순위 + §4 트리에서 다음 쟁점 결정
5. `viewer/public/data/practice/civil-law/civil-XXX.json` Write
6. 정답 균등 재배치 (Python 스니펫)
7. `python3 scripts/practice_to_app.py` 동기화
8. §7 진척률 갱신
9. 다음 쟁점 반복

---

## 11. 메모리 시스템 (클로드 코드 한정)

작성자가 클로드 코드 환경에서 작업 중이라면 다음 메모리 파일이 활성:

```
~/.claude/projects/-Users-hanjiho-Documents----------/memory/
├── MEMORY.md                                    인덱스
├── civil-law-question-generation.md             ⭐ 본 작업 메모리
└── econ-question-generation.md                  경제학 v2 (참고)
```

신규 컴퓨터에서 클로드 코드 사용 시 이 경로는 OS·사용자에 따라 다름. 환경에 맞게 조정.

메모리 핵심 룰 (`civil-law-question-generation.md`):

> 감정평가사 민법 문제 생성 작업은 계획 단계이며, 사용자가 명시적으로 시작·재개를 명령할 때까지 자율 진행하지 않는다.
>
> **How to apply:**
> - 사용자가 "민법 문제 생성 이어가", "민법 다음 쟁점 작성" 같은 지시 시 즉시 docs/civil-law-question-generation-status.md 를 Read하여 작업 재개
> - 압축 모드(turn당 1-4개 쟁점, 25문제, mix_profile `case5-statute5-judge5-theory7-combo3`)
> - **민법은 정답 1번 몰빵 금지** — 기출 실측 19-21% 균등
> - 발문 끝 `(다툼이 있으면 판례에 따름)` 부착
> - 판례 인용 `대판 YYYY.MM.DD, YYYY다XXXXX` 형식 의무
> - 시험범위(총칙+물권)에 "관" 단위 없음 — `meta.item`에 "제N관" 표기 금지

---

## 12. 트러블슈팅

### 12.1 `python3 scripts/practice_to_app.py` 실패

- **원인**: `node viewer/scripts/sync-data.mjs` 호출 실패
- **해결**:
  ```bash
  cd viewer && npm install && cd ..
  python3 scripts/practice_to_app.py
  ```

### 12.2 dev 서버에서 새 쟁점이 안 보임

- **원인**: HMR이 JSON 변경 못 잡음
- **해결**:
  1. 동기화 다시: `python3 scripts/practice_to_app.py`
  2. dev 서버 재시작: `Ctrl+C` → `npm run dev`
  3. 브라우저 강제 새로고침: `Cmd+Shift+R`

### 12.3 정답 분포가 한쪽으로 쏠림

- **원인**: 작성 직후 정답 균등화 스크립트 미실행
- **해결**: §4.4 Python 스니펫 실행

### 12.4 결합형 ㄱㄴㄷ 박스가 안 보임

- **원인**: JSON 줄바꿈 `\n` 누락 또는 `ㄱ.` 뒤 공백 누락
- **해결**: JSON에서 `"\n\nㄱ. "` (한 줄에 \n\n 두 개 + ㄱ + 마침표 + 공백) 정확히 입력

### 12.5 한자 `甲乙丙丁` 입력 어려움

- **해결**: 복붙 — `甲 乙 丙 丁 戊 己 庚 辛 壬 癸`
- macOS: 한자 입력기 (option+한/영 → 한자)

### 12.6 questions_db.json 32MB git 푸시 거부

- **원인**: GitHub LFS 미설정 또는 50MB 제한 초과
- **해결**: 현재 32MB는 정상 범위. 만약 100MB 초과 시 `git lfs track "questions_db.json"`

---

## 13. 진척 추적 자동화 (선택)

매 쟁점 작성 후 진척 통계 자동 출력:

```bash
cd ~/Documents/감정평가사\ 기출문제
python3 << 'PY'
import json
from pathlib import Path
from collections import Counter

civil = Path('viewer/public/data/practice/civil-law')
files = sorted(civil.glob('*.json'))
print(f'완료 쟁점: {len(files)} / 102 ({len(files)/102*100:.0f}%)')
print(f'완료 문항: {len(files)*25} / 2,550')

# 장별 분포
chap = Counter()
for f in files:
    parts = f.stem.split('-')
    # civil-gen-ch02-sec02-item01 → gen-ch02
    chap[f'{parts[1]}-{parts[2]}'] += 1
for k, v in sorted(chap.items()):
    print(f'  {k}: {v}쟁점 ({v*25}문)')
PY
```

---

## 14. 본 작업의 큰 그림

### 14.1 전체 로드맵

| 단계 | 기간 | 쟁점 | 문항 |
|---|---|---:|---:|
| ✅ Phase 1 S (최우선) | 완료 | 25 | 625 |
| ⏳ Phase 2 A (빈출) | ~10-11주 | 50 | 1,250 |
| 📋 Phase 3 B/C (보조) | ~5주 | 25 | 625 |
| **총합** | **약 5개월 (압축 모드)** | **100** | **2,500** |

(별도 v2.1 확장: 동일 쟁점에 추가 25문씩 가능 = 모든 장 capacity 100문 보장)

### 14.2 작업 속도 추정

- 클로드 코드 자동 진행: 1턴 ≈ 2쟁점 (50문)
- Phase 2 A 50쟁점 = 25턴
- Phase 3 B/C 25쟁점 = 13턴
- **총 38턴** 으로 전체 102쟁점 완료 가능

### 14.3 완성 후 기대 효과

- 감정평가사 민법 v2 손작성 1,675문 + α
- 기출 720문과 합쳐 약 2,400문 학습 풀
- 5지선다 + 5난이도 + 5유형 균등 출제
- KaTeX·박스 UI·판례 인용 표준화

---

## 15. 핵심 명령 빠른 참조

```bash
# 의존성
cd viewer && npm install && cd ..

# 동기화 (필수, 매번)
python3 scripts/practice_to_app.py

# dev 서버
cd viewer && npm run dev

# 빌드
cd viewer && npm run build

# 정답 균등 (작성 직후 매번)
python3 -c "
import json, sys
from collections import Counter
path = sys.argv[1]
with open(path) as f: data = json.load(f)
ts = [(i % 5) + 1 for i in range(25)]
for i, q in enumerate(data['questions']):
    c = int(q['answer'])
    if c != ts[i]:
        o = q['options']
        o[c-1], o[ts[i]-1] = o[ts[i]-1], o[c-1]
        q['answer'] = str(ts[i])
with open(path, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print(dict(sorted(Counter(q['answer'] for q in data['questions']).items())))
" viewer/public/data/practice/civil-law/civil-XXX.json

# 진척 확인
ls viewer/public/data/practice/civil-law/*.json | wc -l
```

---

## 16. 외부 참조

- 민법 조문: [국가법령정보센터](https://www.law.go.kr/) → "민법" 검색
- 판례: 대법원 종합법률정보 (`glaw.scourt.go.kr`)
- 감정평가사 시험 정보: 한국감정평가사협회 (`kapanet.or.kr`)
- 본 프로젝트 GitHub: `https://github.com/jihorag/-.git`

---

## 17. 변경 이력

- **2026-06-05**: 본 인수인계서 작성 (Phase 1 S 25/25 ✅ + Phase 2 A 2/52 시점)
- 진척 갱신은 `docs/civil-law-question-generation-status.md` §10 에서 별도 추적

---

---

## 18. 완성된 쟁점 1개 전체 예시 (실제 작성된 JSON 구조 학습용)

작성 표준을 가장 빠르게 익히는 방법은 **완성된 쟁점 1개를 처음부터 끝까지 읽는 것**.

### 18.1 권장 학습 순서 (난이도 ↓ → ↑)

1. **`civil-gen-ch04-sec01-item01.json`** — 물건의 의의와 분류
   - 가장 직관적, 조문이 명료
   - 사례형(자동차+자전거 거치대)이 단순
2. **`civil-gen-ch02-sec02-item01.json`** — 미성년자와 법정대리인
   - 첫 작성 쟁점, 표준 구조 가장 정형적
3. **`civil-gen-ch05-sec02-item02.json`** — 반사회질서 법률행위
   - 판례 인용 다양 (대판(전합) 5건 이상)
   - 사례형이 풍부 (이중매매·도박빚·축첩)
4. **`civil-prop-ch07-sec01-item01.json`** — 유치권
   - 결합형 처리 깔끔
   - 견련성 판례 인용

### 18.2 미성년자 쟁점 (item01) 문항 1번 분해 분석

```json
{
  "id": "practice-civil-gen-ch02-sec02-item01-001",
  "difficulty": 1,
  "question_type": "조문형",
  "question": "민법상 미성년자의 행위능력에 관한 설명으로 옳은 것은?",
  "options": [
    "미성년자가 법정대리인의 동의 없이 한 법률행위는 절대적 무효이다.",
    "미성년자가 법정대리인의 동의 없이 한 법률행위는 미성년자 본인 또는 법정대리인이 취소할 수 있다.",
    "미성년자가 단순히 권리만을 얻는 행위도 법정대리인의 동의를 요한다.",
    "미성년자가 법정대리인의 동의 없이 한 행위는 제3자에 대하여 그 무효를 주장할 수 없다.",
    "미성년자가 법정대리인의 동의 없이 한 법률행위는 추인할 수 없다."
  ],
  "answer": "2",
  "explanation": "민법 제5조 제2항에 따라 미성년자가 법정대리인의 동의 없이 한 법률행위는 취소할 수 있으며, 취소권자는 미성년자 본인과 법정대리인이다(제140조). 단순히 권리만을 얻거나 의무를 면하는 행위는 동의가 필요 없다(제5조 제1항 단서)."
}
```

**분해 해석:**

| 요소 | 값 | 작성 의도 |
|---|---|---|
| `difficulty: 1` | 가장 쉬움 | 단순 조문 적용 |
| `question_type: "조문형"` | 조문 직접 인용 | 매뉴얼 5유형 중 하나 |
| `question` 길이 | 30자 | 조문형 권장 40-55자 보다 짧으나 OK |
| `question` 발문 극성 | "옳은 것은?" | 약 24% 비중 |
| `options` 5개 길이 | 18-37자 | 권장 40-60자 미달이나 조문형은 짧아도 OK |
| `answer: "2"` | 정답 2번 | (i % 5) + 1 = 2 충족 |
| 정답 옵션 (`options[1]`) | "취소할 수 있다" | 함정 어휘 "취소할 수 있다" 활용 |
| 오답 ① "절대적 무효" | NRT #4 효과 정반대 |
| 오답 ③ "단순 권리도 동의" | NRT #2 요건 추가 |
| 오답 ④ "제3자에 대항 X" | NRT #4 효과 변형 |
| 오답 ⑤ "추인 불가" | NRT #4 효과 정반대 |
| `explanation` | 159자 | 권장 80-200자 |
| 조문 인용 | 제5조 제2항, 제140조, 제5조 제1항 단서 | 정답 + 오답 보강 설명 |

### 18.3 사례형 (item01 문항 3번) 분해

```json
{
  "id": "practice-civil-gen-ch02-sec02-item01-003",
  "difficulty": 3,
  "question_type": "사례형",
  "question": "17세인 甲은 자신의 노트북을 친구 乙에게 50만 원에 매도하기로 하고 등록된 법정대리인 부친 丙의 동의 없이 매매계약을 체결하였다. 다음 설명 중 옳지 않은 것은? (다툼이 있으면 판례에 따름)",
  "options": [...],
  "answer": "2",
  "explanation": "..."
}
```

**사례형 체크리스트 충족:**

✅ 등장인물: `甲(17세)`, `乙(친구)`, `丙(부친 법정대리인)` — 3명, 4명 이내
✅ 목적물: `노트북` — 구체적
✅ 금액: `50만 원` — 한글 단위
✅ 발문 본문: 96자 — 권장 100-160자에 약간 미달이나 OK
✅ 발문 끝 `(다툼이 있으면 판례에 따름)` 부착
✅ 발문 극성 "옳지 않은 것은?" — 약 68% 비중
✅ 한자 등장인물 (한글 갑·을 아님)

---

## 19. 코드 발췌 (시스템 동작 이해용)

### 19.1 동기화 스크립트 핵심 (scripts/practice_to_app.py)

```python
#!/usr/bin/env python3
"""연습문제 → questions_db.json 통합 → chunk 분할."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE_DIR = ROOT / 'viewer/public/data/practice/economics'  # ⚠ 경제학만 처리
QDB = ROOT / 'questions_db.json'
EXAM_NAME = '[연습문제]'


def convert(p, meta):
    """v2 손작성 JSON → questions_db.json 항목 변환."""
    return {
        'id': p['id'],
        'number': '',
        'period': 'practice',
        'year': '2026',
        'exam_date': '2026-05-31',
        'question': p['question'],
        'options': p['options'],
        'answer': p['answer'],
        'explanation': p['explanation'],
        'subject': meta['subject'],
        'tags': {
            'subject': meta['subject'],
            'is_practice': True,
            'difficulty': p['difficulty'],
            'question_type': p['question_type'],
            'system_note': 'practice-v1',
        },
        'exam': EXAM_NAME,
        'indexing_v4': {
            'difficulty': p['difficulty'],
            'mapped_taxonomy': {
                'subject': meta['subject'],
                'sub_subject': meta['sub_subject'],
                'chapter': meta['chapter'],
                'section': meta['section'],
                'item': meta['item'],
            },
            'needs_higher_ai': False,
            'reason': f'연습문제 v{meta["version"]} — {meta["item"]} 출제',
            # claude-sonnet-4-6 이어야 manifest "classified" 통계 포함
            'processed_by': 'claude-sonnet-4-6',
        },
    }
```

⚠️ **민법(civil-law)은 이 스크립트가 처리하지 않음.** 민법은 Vite 가 `viewer/public/data/practice/civil-law/` 를 자동 서빙. 하지만 스크립트 마지막에 `node viewer/scripts/sync-data.mjs` 가 호출되므로 한 번 실행으로 economics + civil-law 모두 처리됨.

### 19.2 sync-data.mjs 핵심 (chunk 분할)

```js
// questions_db.json (32MB) → exams/00.json~13.json 분할
const arr = JSON.parse(readFileSync(qSrc, 'utf8'));
const groups = new Map();
for (const q of arr) {
  const ex = q.exam || '기타';
  if (!groups.has(ex)) groups.set(ex, []);
  groups.get(ex).push(q);
}
const exams = [...groups.keys()].sort();   // 결정론적: 사전순

exams.forEach((name, i) => {
  const list = groups.get(name);
  const file = String(i).padStart(2, '0') + '.json';   // 00.json, 01.json...
  writeFileSync(join(examsDir, file), JSON.stringify(list));
});
```

**현재 시험 슬롯**:
- `00.json` = 9급 국가직 공무원 (300문)
- `01.json` = [연습문제] (6,300문) ← 경제학 v2 들어감
- `02.json` = 가맹거래사
- `03.json` = 감정평가사 (3,320문, 이 중 민법 720문)
- ... `13.json` = 회계사

### 19.3 ParsedText.jsx 핵심 (ㄱㄴㄷ 박스)

```jsx
// 보기 ㄱㄴㄷㄹㅁ 박스 — 연속된 "ㄱ. " / "ㄴ. " 라인을 박스로 묶기
const bogiHead = trimmed.match(/^([ㄱ-ㅎ])\.\s+(.+)$/);
if (bogiHead && /[ㄱㄴㄷㄹㅁㅂㅅㅇ]/.test(bogiHead[1])) {
  const items = [];
  while (i < rawLines.length) {
    const cur = rawLines[i].trim();
    const m = cur.match(/^([ㄱ-ㅎ])\.\s+(.*)$/);
    if (!m || !/[ㄱㄴㄷㄹㅁㅂㅅㅇ]/.test(m[1])) break;
    items.push({ marker: m[1], content: m[2] });
    i++;
  }
  elements.push(
    <div
      key={`${keyPrefix}-bogi-${i}`}
      style={{
        background: '#f8fafc',
        border: '1px solid #e2e8f0',
        borderLeft: '3px solid #94a3b8',
        borderRadius: '6px',
        padding: '12px 16px',
        margin: '10px 0',
      }}
    >
      {items.map((it, k) => (
        <div
          key={k}
          style={{
            display: 'flex',
            gap: '10px',
            margin: k === 0 ? '0' : '6px 0 0',
            lineHeight: 1.6,
            alignItems: 'baseline',
          }}
        >
          <span style={{ fontWeight: 700, minWidth: '20px', color: '#475569', flexShrink: 0 }}>
            {it.marker}.
          </span>
          <span style={{ flex: 1 }}>
            {renderInlines(it.content, `${keyPrefix}-bogi-${k}`)}
          </span>
        </div>
      ))}
    </div>
  );
  continue;
}
```

### 19.4 Vite 설정 핵심 (vite.config.js)

```js
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        skipWaiting: true,
        clientsClaim: true,
        globPatterns: ['**/*.{js,css,html,woff2,svg}'],
        globIgnores: ['**/data/**', '**/images/**'],  // 32MB JSON 프리캐시 제외
        navigateFallbackDenylist: [/^\/data\//, /^\/images\//],
        runtimeCaching: [
          {
            urlPattern: ({ url }) => url.pathname.startsWith('/data/'),
            handler: 'StaleWhileRevalidate',
            options: {
              cacheName: 'quiz-data',
              expiration: { maxEntries: 40, maxAgeSeconds: 60 * 60 * 24 * 30 },
              cacheableResponse: { statuses: [0, 200] },
            },
          },
        ],
      },
    }),
  ],
})
```

**의미**: PWA 설치형 앱에서 32MB 데이터를 빌드 시 통째로 캐싱하지 않고, 사용자가 실제 시험을 열 때 chunk(01.json 등) 단위로 fetch + StaleWhileRevalidate.

---

## 20. 기출문제 720문 심층 분석 (참고용)

본 작업의 토대가 된 기출 분석 결과 전체.

### 20.1 영역별 분포 (전체 720문 키워드 추정)

| 영역 (chapter) | 문항 | 비중 |
|---|---:|---:|
| 제2편 물권 - 총론 (등기·물권변동·점유) | 122 | 16.9% |
| 제2편 물권 - 담보물권 (저당·근저당·유치) | 85 | 11.8% |
| 제1편 총칙 - 권리주체 (자연인·법인) | 81 | 11.2% |
| 제1편 총칙 - 법률행위 (반사회·의사표시) | 79 | 11.0% |
| 제1편 총칙 - 기간시효 (소멸·취득시효) | 63 | 8.8% |
| 제2편 물권 - 용익물권 (전세·지상) | 63 | 8.8% |
| 제1편 총칙 - 대리 (복대리·표현대리) | 52 | 7.2% |
| 제1편 총칙 - 권리객체 (물건) | 51 | 7.1% |
| 제2편 물권 - 소유권 (공유·시효취득·첨부) | 51 | 7.1% |
| 제1편 총칙 - 무효·취소 | 38 | 5.3% |
| 제1편 총칙 - 조건·기한 | 30 | 4.2% |
| 기타 | 5 | 0.7% |
| **합계** | **720** | **100%** |

### 20.2 최근 6년(2021-2026) 추세

- 신경향: 물권 비중 ↑ (43% → 45%)
- 강세 영역: 소유권·용익물권·법률행위
- 약세 영역: 기간시효·대리 (4.6%p, 1.8%p ↓)

### 20.3 발문 패턴 (전수 분석)

| 패턴 | 빈도 | 비율 |
|---|---:|---:|
| 5지선다 | 720 | **100%** |
| `(다툼이 있으면 판례에 따름/의함)` | 618 | **85.8%** |
| "옳지 않은 것은?" | 487 | **67.6%** |
| "옳은 것은?" | 120 | 16.7% |
| "아닌 것은?" | 17 | 2.4% |
| "경우는?" | 12 | 1.7% |
| 甲乙丙丁 사례형 | 93 | 12.9% |
| 옵션 ㄱㄴㄷ 결합형 | 60 | 8.3% |
| 발문에 "민법 제X조" 명시 | 7 | 1.0% |

### 20.4 정답 번호 분포 (전수)

| 정답 | 문항 | 비율 |
|---:|---:|---:|
| 1번 | 138 | 19.2% |
| 2번 | 146 | 20.3% |
| 3번 | 151 | 21.0% |
| 4번 | 145 | 20.1% |
| 5번 | 140 | 19.4% |

→ **모든 번호가 19-21% 균등**. 작성 시 1번 몰빵 금지의 근거.

### 20.5 발문/옵션/해설 길이 (P50)

| 항목 | min | P25 | median | P75 | max |
|---|---:|---:|---:|---:|---:|
| 발문 (전체) | 12 | 39 | **43** | 50 | 396 |
| 발문 (비사례형) | - | - | **46** | - | - |
| 발문 (사례형 甲乙) | - | - | **129** | - | - |
| 옵션 1개 | 1 | - | **49** | - | 150 |
| 해설 1개 | - | - | **159** | - | 661 |

### 20.6 빈출 주제 TOP 20 (전수 발문 "X에 관한 설명…")

| 순위 | 주제 | 횟수 | 영역 |
|---:|---|---:|---|
| 1 | 전세권 | 15 | 용익물권 |
| 2 | 선의취득 | 12 | 물권총론 |
| 2 | 지역권 | 12 | 용익물권 |
| 2 | 유치권 | 12 | 담보물권 |
| 5 | 점유 | 10 | 물권총론 |
| 5 | 점유자와 회복자 관계 | 10 | 물권총론 |
| 5 | 복대리 | 10 | 대리 |
| 5 | 물건 | 10 | 권리객체 |
| 5 | 저당권 | 10 | 담보물권 |
| 10 | 물권적 청구권 | 9 | 물권총론 |
| 10 | 불공정 법률행위 | 9 | 법률행위 |
| 10 | 지상권 | 9 | 용익물권 |
| 13 | 조건과 기한 | 8 | 조건기한 |
| 13 | 소멸시효 | 8 | 기간시효 |
| 15 | 등기의 추정력 | 7 | 물권총론 |
| 15 | 대리 | 7 | 대리 |
| 15 | 질권 | 7 | 담보물권 |
| 18 | 신의성실의 원칙 | 6 | 통칙 |
| 18 | 표현대리 | 6 | 대리 |
| 18 | 주위토지통행권 | 6 | 소유권 |

### 20.7 옵션 빈출 함정 어휘 (출제 패턴 학습)

- 부정: `않는다(287)`, `못한다(86)`, `아니다(69)`, `인정되지(60)`
- 권리: `청구할(187)`, `취소할(99)`, `행사할(64)`
- 조건어: `특별한 사정이(186)`, `때에는(136)`, `경우에는(103)`, `원칙적으로(72)`
- 법률효과: `효력이(121)`, `소유권을(100)`, `무효이다(77)`, `취득한(97)`
- 이전: `소유권이전등기(143)`

---

## 21. 자동화 도구 모음 (작업 효율화)

### 21.1 진척 자동 출력 (한 줄 명령)

```bash
ls viewer/public/data/practice/civil-law/*.json 2>/dev/null | wc -l | awk '{printf "쟁점: %d/102 (%.0f%%) | 문항: %d/2550\n", $1, $1/102*100, $1*25}'
```

### 21.2 전체 검수 자동화 (모든 파일 일괄)

```bash
cat > /tmp/check_civil.py << 'PY'
import json
import sys
from collections import Counter
from pathlib import Path

civil = Path('viewer/public/data/practice/civil-law')
errors = []

for path in sorted(civil.glob('*.json')):
    with open(path) as f:
        data = json.load(f)
    qs = data.get('questions', [])
    name = path.stem

    # 1. count
    if len(qs) != 25:
        errors.append(f"{name}: count {len(qs)} != 25")

    # 2. meta.count
    if data['meta'].get('count') != 25:
        errors.append(f"{name}: meta.count != 25")

    # 3. mix_profile
    if data['meta'].get('mix_profile') != 'case5-statute5-judge5-theory7-combo3':
        errors.append(f"{name}: mix_profile mismatch")

    # 4. version
    if data['meta'].get('version') != 'v2-handcrafted':
        errors.append(f"{name}: version != v2-handcrafted")

    # 5. ID 패턴
    for i, q in enumerate(qs):
        expected_suffix = f"-{i+1:03d}"
        if not q['id'].endswith(expected_suffix):
            errors.append(f"{name}-{i+1}: id pattern mismatch ({q['id']})")

    # 6. 옵션 5개
    for i, q in enumerate(qs):
        if len(q.get('options', [])) != 5:
            errors.append(f"{name}-{i+1}: options != 5")

    # 7. 정답 분포 균등 (5,5,5,5,5)
    ans = Counter(q['answer'] for q in qs)
    if any(v != 5 for v in ans.values()) or len(ans) != 5:
        errors.append(f"{name}: 정답 불균등 {dict(ans)}")

    # 8. answer 형식 (문자열 "1"~"5")
    for i, q in enumerate(qs):
        if q.get('answer') not in {'1', '2', '3', '4', '5'}:
            errors.append(f"{name}-{i+1}: answer {q.get('answer')} 형식 오류")

    # 9. difficulty 범위 (1~5)
    for i, q in enumerate(qs):
        if q.get('difficulty') not in {1, 2, 3, 4, 5}:
            errors.append(f"{name}-{i+1}: difficulty {q.get('difficulty')} 범위 오류")

    # 10. question_type 5종
    valid_types = {'사례형', '조문형', '판례형', '이론형', '결합형'}
    for i, q in enumerate(qs):
        if q.get('question_type') not in valid_types:
            errors.append(f"{name}-{i+1}: question_type {q.get('question_type')} 형식 오류")

if errors:
    print(f"❌ {len(errors)}개 오류:")
    for e in errors[:30]:
        print(f"  - {e}")
    if len(errors) > 30:
        print(f"  ... 외 {len(errors)-30}개")
    sys.exit(1)
else:
    print(f"✅ {len(list(civil.glob('*.json')))}개 파일 모두 검수 통과")
PY
python3 /tmp/check_civil.py
```

### 21.3 진척 보고서 자동 생성

```bash
cat > /tmp/report_civil.py << 'PY'
import json
from collections import Counter
from pathlib import Path

civil = Path('viewer/public/data/practice/civil-law')
files = sorted(civil.glob('*.json'))

print(f'# 민법 v2 진척 보고서\n')
print(f'**작성일 기준**: {len(files)}/102 쟁점 ({len(files)/102*100:.0f}%), {len(files)*25}/2,550 문항\n')

# 장별 분포
chap_count = Counter()
for f in files:
    with open(f) as fp:
        meta = json.load(fp)['meta']
    chap_count[(meta['sub_subject'], meta['chapter'])] += 1

print('## 장별 진척\n')
print('| 편 | 장 | 쟁점 | 문항 |')
print('|---|---|---:|---:|')
for (sub, chap), n in sorted(chap_count.items()):
    print(f'| {sub} | {chap} | {n} | {n*25} |')

# 유형 분포
qt_total = Counter()
for f in files:
    with open(f) as fp:
        data = json.load(fp)
    for q in data['questions']:
        qt_total[q['question_type']] += 1
print(f'\n## 유형 분포 (전체 {sum(qt_total.values())}문)\n')
print('| 유형 | 수 | 비율 |')
print('|---|---:|---:|')
total = sum(qt_total.values())
for qt, n in sorted(qt_total.items(), key=lambda x: -x[1]):
    print(f'| {qt} | {n} | {n/total*100:.1f}% |')

# 난이도 분포
diff_total = Counter()
for f in files:
    with open(f) as fp:
        data = json.load(fp)
    for q in data['questions']:
        diff_total[q['difficulty']] += 1
print(f'\n## 난이도 분포\n')
print('| 난이도 | 수 |')
print('|---:|---:|')
for d, n in sorted(diff_total.items()):
    print(f'| {d} | {n} |')
PY
python3 /tmp/report_civil.py > docs/progress-report.md
echo "보고서 생성: docs/progress-report.md"
```

### 21.4 누락 쟁점 자동 검색 (다음 작성 대상 찾기)

```bash
cat > /tmp/next_civil.py << 'PY'
"""다음 작성 우선순위 쟁점 1개 출력."""
from pathlib import Path

# Phase 2 A 우선순위 (S 완료 후)
PRIORITY = [
    # 총칙 A
    'civil-gen-ch01-sec01-item01',  # 민법의 법원
    'civil-gen-ch01-sec02-item01',  # 신의칙
    'civil-gen-ch01-sec02-item02',  # 권리남용
    'civil-gen-ch02-sec01-item01',  # 자연인 권리능력
    'civil-gen-ch02-sec01-item02',  # 태아
    'civil-gen-ch02-sec02-item03',  # 제한능력자 상대방 보호
    'civil-gen-ch02-sec02-item04',  # 속임수·법정추인
    'civil-gen-ch02-sec03-item01',  # 부재자
    'civil-gen-ch02-sec03-item02',  # 실종선고
    'civil-gen-ch03-sec01-item01',  # 법인 본질
    'civil-gen-ch03-sec04-item01',  # 이사·대표권
    'civil-gen-ch03-sec05-item01',  # 사원총회·해산·비법인사단
    'civil-gen-ch04-sec02-item01',  # 부동산·동산
    'civil-gen-ch04-sec03-item01',  # 주물·종물
    'civil-gen-ch05-sec01-item01',  # 법률행위 종류
    'civil-gen-ch05-sec01-item02',  # 법률행위 해석
    'civil-gen-ch05-sec02-item01',  # 강행·임의·단속법규
    'civil-gen-ch05-sec03-item05',  # 의사표시 효력발생
    'civil-gen-ch06-sec01-item01',  # 대리 의의
    'civil-gen-ch06-sec02-item01',  # 대리권 발생
    'civil-gen-ch06-sec02-item02',  # 대리권 소멸
    'civil-gen-ch06-sec04-item01',  # 협의 무권대리
    'civil-gen-ch06-sec05-item03',  # 제129조 표현대리
    'civil-gen-ch07-sec01-item01',  # 무효 일반
    'civil-gen-ch07-sec02-item01',  # 취소
    'civil-gen-ch07-sec02-item02',  # 추인·법정추인
    'civil-gen-ch08-sec01-item01',  # 조건
    'civil-gen-ch10-sec01-item02',  # 시효 기산점
    'civil-gen-ch10-sec02-item01',  # 시효 중단
    # 물권 A
    'civil-prop-ch01-sec01-item01',  # 물권법정주의
    'civil-prop-ch01-sec02-item02',  # 동산 물권변동
    'civil-prop-ch01-sec03-item02',  # 등기청구권·중간생략
    'civil-prop-ch01-sec04-item01',  # 공시·공신 원칙
    'civil-prop-ch02-sec01-item02',  # 직접·간접 점유
    'civil-prop-ch02-sec03-item01',  # 점유보호청구권
    'civil-prop-ch03-sec02-item01',  # 상린관계
    'civil-prop-ch03-sec03-item01',  # 시효취득
    'civil-prop-ch03-sec03-item02',  # 첨부
    'civil-prop-ch03-sec04-item01',  # 공유
    'civil-prop-ch03-sec04-item02',  # 합유·총유
    'civil-prop-ch03-sec05-item01',  # 명의신탁
    'civil-prop-ch04-sec01-item01',  # 지상권 일반
    'civil-prop-ch04-sec01-item02',  # 지상권 효력
    'civil-prop-ch04-sec02-item01',  # 구분지상권·분묘
    'civil-prop-ch05-sec01-item01',  # 지역권 취득
    'civil-prop-ch05-sec02-item01',  # 지역권 효력
    'civil-prop-ch06-sec02-item01',  # 전세권 효력
    'civil-prop-ch06-sec02-item02',  # 전세권 양도·전세
    'civil-prop-ch06-sec03-item01',  # 전세권 소멸
    'civil-prop-ch07-sec02-item01',  # 유치권 효력
    'civil-prop-ch08-sec01-item01',  # 동산질권
    'civil-prop-ch08-sec02-item01',  # 채권질권
    'civil-prop-ch09-sec02-item01',  # 저당권 효력
    'civil-prop-ch09-sec02-item02',  # 물상대위
    'civil-prop-ch09-sec03-item01',  # 공동저당
    'civil-prop-ch09-sec04-item01',  # 근저당
]

civil = Path('viewer/public/data/practice/civil-law')
done = {p.stem for p in civil.glob('*.json')}

for slug in PRIORITY:
    if slug not in done:
        print(f"다음 작성 대상: {slug}")
        print(f"  파일 경로: viewer/public/data/practice/civil-law/{slug}.json")
        break
else:
    print("✅ Phase 2 A 50개 모두 완료. Phase 3 B/C 진입 가능.")
PY
python3 /tmp/next_civil.py
```

### 21.5 한 줄로 검수+동기화

```bash
# alias 설정 (~/.zshrc 또는 ~/.bashrc 에 추가)
alias civil-sync='python3 /tmp/check_civil.py && python3 scripts/practice_to_app.py'
alias civil-next='python3 /tmp/next_civil.py'
alias civil-report='python3 /tmp/report_civil.py | head -40'
```

---

## 22. 5가지 유형별 작성 템플릿 (즉시 사용 가능한 부분 견본)

### 22.1 조문형 (5문/관)

```json
{
  "id": "practice-civil-XXX-NNN",
  "difficulty": 2,
  "question_type": "조문형",
  "question": "민법상 {제도명}에 관한 설명으로 옳은 것은?",
  "options": [
    "{조문 그대로 표현 - 정답}",
    "{조문 변형 - 수치 오류}",
    "{조문 변형 - 효과 정반대}",
    "{조문 변형 - 요건 누락}",
    "{조문 변형 - 단정적 표현}"
  ],
  "answer": "1",
  "explanation": "제X조 명문 규정. ② 잘못된 수치. ③ 효과 반대. ④ 요건 누락. ⑤ 절대성 오류."
}
```

### 22.2 사례형 (5문/관)

```json
{
  "id": "practice-civil-XXX-NNN",
  "difficulty": 3,
  "question_type": "사례형",
  "question": "甲은 {상황 설정 1문}. 그 후 {상황 전개 1문}. 다음 중 옳지 않은 것은? (다툼이 있으면 판례에 따름)",
  "options": [
    "{사례 적용 정확 1}",
    "{사례 적용 정확 2}",
    "{사례 적용 정확 3}",
    "{사례 적용 정확 4}",
    "{사례 적용 오류 - 정답}"
  ],
  "answer": "5",
  "explanation": "사례에 적용되는 조문 X조 + 판례. ⑤가 오류인 이유 명시."
}
```

### 22.3 판례형 (5문/관)

```json
{
  "id": "practice-civil-XXX-NNN",
  "difficulty": 4,
  "question_type": "판례형",
  "question": "{주제}에 관한 판례의 태도로 옳은 것은? (다툼이 있으면 판례에 따름)",
  "options": [
    "{판례 입장 정확 - 정답}",
    "{판례와 반대 입장}",
    "{학설로 존재하나 통설 아님}",
    "{과거 판례 입장 변경 전}",
    "{잘못된 표현}"
  ],
  "answer": "1",
  "explanation": "대판 YYYY. MM. DD, YYYY다XXXXX (또는 대판(전합)): {판례 핵심 요지}. ②③④⑤ 잘못된 이유."
}
```

### 22.4 이론형 (7문/관)

```json
{
  "id": "practice-civil-XXX-NNN",
  "difficulty": 3,
  "question_type": "이론형",
  "question": "{제도}의 {요건/효과/성질}에 관한 설명으로 옳지 않은 것은?",
  "options": [
    "{학설/체계 정확 1}",
    "{학설/체계 정확 2}",
    "{학설/체계 정확 3}",
    "{학설/체계 정확 4}",
    "{단정적·과장 표현 - 정답}"
  ],
  "answer": "5",
  "explanation": "통설·판례: {요약}. ⑤는 단정적 표현으로 잘못. ①②③④는 정확."
}
```

### 22.5 결합형 (3문/관, ㄱㄴㄷ 박스)

```json
{
  "id": "practice-civil-XXX-NNN",
  "difficulty": 5,
  "question_type": "결합형",
  "question": "{주제}에 관한 설명으로 옳은 것을 모두 고른 것은? (다툼이 있으면 판례에 따름)\n\nㄱ. {진술 1}\nㄴ. {진술 2}\nㄷ. {진술 3}\nㄹ. {진술 4}",
  "options": [
    "ㄱ, ㄴ, ㄷ",
    "ㄱ, ㄴ",
    "ㄴ, ㄷ",
    "ㄱ, ㄴ, ㄷ, ㄹ",
    "ㄷ, ㄹ"
  ],
  "answer": "1",
  "explanation": "ㄱ(조문/판례), ㄴ(조문/판례), ㄷ(조문/판례)는 옳다. ㄹ은 {이유}로 잘못."
}
```

---

## 23. 25문 1관 작성 흐름 (실전 절차)

한 쟁점(25문) 작성에 약 30-45분 소요. 권장 흐름:

### 23.1 사전 준비 (5분)

```bash
# 1) 다음 쟁점 확인
python3 /tmp/next_civil.py

# 2) 해당 영역 기출 720문에서 빈출 쟁점 핵심 키워드 확인
python3 << 'PY'
import json
with open('viewer/public/data/exams/03.json') as f:
    data = json.load(f)
# 예: 신의칙 관련 기출 발문
for q in data:
    if q.get('subject') == '민법' and '신의' in q.get('question', ''):
        print(q['question'][:100])
PY
```

### 23.2 조문 정리 (5분)

해당 쟁점의 민법 조문 본문 정리. 예: 신의칙 = 제2조

```
제2조(신의성실)
① 권리의 행사와 의무의 이행은 신의에 좇아 성실히 하여야 한다.
② 권리는 남용하지 못한다.
```

### 23.3 핵심 판례 5건 선정 (5분)

§9.10 인용 가능 판례 목록 + 영역별 추가 판례.

신의칙 핵심:
- 대판 1997. 6. 27, 95다13319 (사정변경 신의칙)
- 대판 1991. 12. 10, 91다36062 (실효의 원칙)
- 대판(전합) 2008. 9. 18, 2007두2173 (권리남용 일반)

### 23.4 25문 작성 (20-30분)

mix_profile 분배:
- 사례 5문 (4-8번)
- 조문 5문 (1, 2, 13, 14, 19번 등)
- 판례 5문 (9, 11, 16, 18, 21번)
- 이론 7문 (3, 5, 12, 15, 17, 20, 23번)
- 결합 3문 (10, 22, 25번)

작성 순서 권장:
1. 조문형 5문 (가장 쉬움, 정확성 핵심)
2. 이론형 7문 (개념·체계)
3. 사례형 5문 (구체적 사실관계)
4. 판례형 5문 (판례 인용 정확성)
5. 결합형 3문 (ㄱㄴㄷ 종합)

### 23.5 정답 균등 + 동기화 (1분)

```bash
python3 -c "
import json
from collections import Counter
path = 'viewer/public/data/practice/civil-law/civil-gen-ch01-sec02-item01.json'
with open(path) as f: data = json.load(f)
ts = [(i % 5) + 1 for i in range(25)]
for i, q in enumerate(data['questions']):
    c = int(q['answer'])
    if c != ts[i]:
        o = q['options']
        o[c-1], o[ts[i]-1] = o[ts[i]-1], o[c-1]
        q['answer'] = str(ts[i])
with open(path, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print(dict(sorted(Counter(q['answer'] for q in data['questions']).items())))
"

python3 scripts/practice_to_app.py
```

### 23.6 진척 갱신 (1분)

`docs/civil-law-question-generation-status.md` §7:
- 누적: 27 → 28쟁점, 675 → 700문
- Phase 2 A: 2 → 3 / 52
- 장별 진척: 해당 장 +1 +25

### 23.7 시각 확인 (선택)

브라우저 → http://localhost:5173 → 감정평가사 → 민법 → 해당 장·절 → 신규 쟁점 확인.

---

## 24. 기존 작업과의 관계

이 저장소는 민법 v2 외에도 여러 작업이 진행 중. 손대지 말아야 할 것들:

### 24.1 경제학 v2 (별도 작업, 완료)

- 경로: `viewer/public/data/practice/economics/`
- 상태: 미시·거시·국제 v2 100% 완료, 재정학 31관 v1 잔존
- 계획서: `docs/econ-question-generation-status.md`
- 메모리: `~/.claude/.../memory/econ-question-generation.md`

⚠️ **민법 작업 중 경제학 JSON 수정 금지.**

### 24.2 민법 통암기 카드 (별개 시스템)

- 경로: `viewer/public/data/civil/`
- 빌드: `viewer/scripts/build_civil.mjs`
- 소스: `~/Documents/Claude KAPA CHATING/1차 - 민법_학습자료/*.md`
- 자동 cloze 카드 생성 (T1 조문, T2 정의, T3 볼드, T4 두문자, T5 수동)

⚠️ **이번 작업과 무관.** 통암기는 별개 학습 모드.

### 24.3 기출문제 (정본, 수정 금지)

- 정본: `questions_db.json` (32MB, 18,339문)
- 분류 트리: `taxonomy_v4.json`
- chunk: `viewer/public/data/exams/00.json~13.json` (자동 생성)

⚠️ **민법 작업 중 기출 데이터 수정 금지.** 동기화 스크립트가 자동 처리.

### 24.4 AI 학습 모드 (Supabase 연동)

- 경로: `viewer/src/AILearning.jsx`
- Supabase 키: `.env`
- 본 작업과 무관 (별도 RLS 정책으로 보호됨)

---

## 25. 배포 절차 (참고)

### 25.1 Vercel 자동 배포

GitHub `main` 브랜치 push 시 Vercel 자동 빌드. 설정은 `vercel.json` 에:

```json
{
  "buildCommand": "cd viewer && npm install && npm run build",
  "outputDirectory": "viewer/dist",
  "framework": null
}
```

작성·동기화 후 커밋·푸시만 하면 배포 반영.

### 25.2 로컬 빌드 테스트

```bash
cd viewer
npm run build
npm run preview   # http://localhost:4173 (정적 빌드 미리보기)
```

### 25.3 PWA 설치형 앱 동작

빌드 후 `dist/` 산출물은 PWA. 사용자가 브라우저에서 "홈 화면에 추가" 하면 오프라인 사용 가능.

- 빌드 자산(js·css·html·svg)은 즉시 프리캐시
- 시험 데이터(32MB)는 사용자가 클릭 시 chunk fetch + 30일 캐시 (StaleWhileRevalidate)

---

## 26. 다른 컴퓨터 동기화 체크리스트

신규 컴퓨터에서 시작 전 다음 모두 확인:

- [ ] Node.js 22.x 설치 (`node --version` → `v22.x.x`)
- [ ] Python 3.10+ 설치 (`python3 --version`)
- [ ] Git 설치 + GitHub 인증 (SSH 키 또는 HTTPS PAT)
- [ ] 저장소 클론 (`git clone https://github.com/jihorag/-.git "감정평가사 기출문제"`)
- [ ] `cd viewer && npm install` 완료
- [ ] `python3 scripts/practice_to_app.py` 실행 → `✅ 앱 반영 완료` 확인
- [ ] `cd viewer && npm run dev` → http://localhost:5173 접속 가능
- [ ] 브라우저 → 감정평가사 → 민법 → 총칙 → "미성년자와 법정대리인" 25문 표시 확인
- [ ] 본 문서 (`docs/HANDOVER-civil-law-v2.md`) 한 번 정독
- [ ] 계획서 (`docs/civil-law-question-generation-status.md`) §1-§9 정독
- [ ] (클로드 코드 사용 시) 메모리 시스템 마이그레이션 또는 본 문서로 대체

---

## 27. FAQ

### Q1. 한 쟁점 작성에 얼마나 걸리나요?

A. 수동 작성 30-45분, 클로드 코드 자동 작성 1-3분.

### Q2. 정답 분포가 자동으로 균등해지나요?

A. 아니요. 작성 후 §4.4 Python 스니펫 수동 실행 필수.

### Q3. 동기화 안 해도 dev 서버에 보이나요?

A. civil-law는 자동 노출 (Vite가 public/ 자동 서빙). 하지만 questions_db 통계에 반영하려면 동기화 필요.

### Q4. ㄱㄴㄷ 박스가 발문에서만 작동하나요?

A. 발문·옵션·해설 모두 작동. ParsedText로 렌더링되는 모든 곳.

### Q5. 27개 쟁점 모두 25문씩 = 675문 정확한가요?

A. 예. 27 × 25 = 675. `ls civil-law/*.json | wc -l` → 27.

### Q6. Phase 2 끝나면 어떻게 되나요?

A. Phase 3 B/C 25쟁점 진행. 그 후 v2.1 (동일 쟁점 추가 25문 = 50문/쟁점) 가능.

### Q7. 작성한 쟁점을 v2.1로 확장하려면?

A. `civil-XXX-itemNN-v2.1.json` 파일명 사용. ID는 `practice-civil-XXX-...-v2.1-NNN`.

### Q8. dev 서버 포트 변경하려면?

A. `cd viewer && npm run dev -- --port 5174`

### Q9. 빌드 시 32MB JSON 때문에 빌드 느린데?

A. PWA 프리캐시에서 제외돼 있어 빌드 시간엔 영향 없음. 런타임에만 fetch.

### Q10. 새 쟁점 추가했는데 dev 서버에서 안 보임?

A. 1) 동기화 다시 (`python3 scripts/practice_to_app.py`), 2) 브라우저 강제 새로고침(Cmd+Shift+R), 3) dev 서버 재시작.

---

## 28. 작업 품질 기준 (rubric)

각 쟁점 완료 후 자가 채점 가능한 5점 척도:

| 항목 | 5점 | 3점 | 1점 |
|---|---|---|---|
| **정답 분포** | 1-5번 각 5문 | 1번에 4-6개 | 한 번호 7+개 |
| **유형 mix** | 사례5/조문5/판례5/이론7/결합3 | 약간 어긋남 | 한 유형 빠짐 |
| **판례 인용** | 5문 이상 정확 인용 | 3-4문 인용 | 0-2문 또는 가짜 판례 |
| **사례 한자** | 5문 모두 甲乙丙 | 일부 한글 | 한자 없음 |
| **함정 어휘** | 매 옵션 함정 어휘 활용 | 절반만 | 거의 안 씀 |
| **(다툼) 단서** | 사례·판례형 모두 | 일부만 | 거의 없음 |
| **발문 극성** | 옳지않은 ≥ 12 | 7-11 | < 7 |

총 25점 만점, 평균 4점 이상 권장.

---

## 29. 변경 이력

- **2026-06-05 v2**: §18-§28 추가 (실제 완성 쟁점 예시·코드 발췌·기출 720문 분석·자동화 도구·5유형 템플릿·작성 흐름·기존 작업 관계·배포·체크리스트·FAQ·품질 기준)
- **2026-06-05 v1**: 초기 작성 (§1-§17, 960줄)
- 진척 갱신은 `docs/civil-law-question-generation-status.md` §7 에서 별도 추적

---

**END OF HANDOVER**

> 이 문서만 있으면 어디서든 작업 재개 가능. 빠진 내용 있으면 `docs/civil-law-question-generation-status.md` 의 §1~§9 참고.
