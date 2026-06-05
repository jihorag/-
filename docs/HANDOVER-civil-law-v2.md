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

**END OF HANDOVER**

> 이 문서만 있으면 어디서든 작업 재개 가능. 빠진 내용 있으면 `docs/civil-law-question-generation-status.md` 의 §1~§9 참고.
