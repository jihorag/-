# 경제학 문제 생성 작업 상태 (감정평가사 경제학)

> **재개 명령 예시**: "경제학 문제 생성 이어가", "다음 관 작업해", "경제학 5관 더 만들어"
> 사용자가 위와 같이 지시하면 이 파일을 먼저 읽고 압축 모드로 즉시 작업 재개.
> **명시 지시 없이는 자율 진행하지 않음.**

## 1. 진척률

- **누적 v2 완료**: **68관** (약 29%)
- **미완료 (v1 자동생성)**: 167관
- **그래프 SVG 라이브러리**: 53종 (`viewer/public/data/practice/economics/graphs/`)
- **전체 목표**: 235관 (미시 60관 + 거시 66관 + 국제 16관 + 재정 61관 = 203관 + α)

## 2. 작업 모드 (압축 모드)

### 2.1 문제 구성

- **25문제/관** (이전 30문제에서 축소)
- 비율: **계산 12 + 그래프 5 + 이론 8**
- 5-difficulty 분포 유지 (1×5, 2×7, 3×10, 4×5, 5×3 ... 조정 가능)
- 각 문제 5지선다, 정답은 1번에 우선 배치(가능한 경우)

### 2.2 JSON 스키마

```json
{
  "meta": {
    "subject": "경제학원론",
    "sub_subject": "미시경제학",  // 또는 거시·국제·재정
    "chapter": "제X장 ...",
    "section": "제Y절 ...",
    "item": "제Z관 ...",
    "source": "practice-set",
    "version": "v2-handcrafted",
    "created": "2026-06-01",
    "count": 25,
    "mix_profile": "calc12-graph5-theory8"
  },
  "questions": [
    {
      "id": "practice-econ-{sub_slug}-ch{NN}-sec{NN}-item{NN}-{NNN}",
      "difficulty": 1,
      "question_type": "이론형",  // 또는 계산형·그래프형·옳은 것 고르기·보기 결합형
      "question": "...",
      "options": ["...", "...", "...", "...", "..."],
      "answer": "1",  // 1~5 문자열
      "explanation": "..."
    }
  ]
}
```

### 2.3 그래프 인라인 참조

```
[IMAGE: data/practice/economics/graphs/{name}.svg]
```

문제 본문에 위 토큰 삽입. ParsedText.jsx가 `<img>` 로 렌더링.

### 2.4 KaTeX 수식

- 인라인: `$Q_d = 100 - 2P$`
- 분수: `$\dfrac{a + c}{b + d}$`
- 시그마: `$\Sigma p_i \cdot x_i$`
- 절댓값: `$|\varepsilon_d|$`

### 2.5 turn당 4관 처리

- 한 묶음 4관 작성 → `python3 scripts/practice_to_app.py` 한 번에 sync
- 매 관마다 sync 안 함

### 2.6 작업 패턴

- 답·계산 검증 후 작성
- 한국어 조사 규칙 (은/는, 이/가, 을/를) 준수
- 도메인 지식 포함: 학자 이름·연도·노벨상·핵심 저서
- 한국 정책 사례 (공정위, 한전, 카카오·네이버 등)

## 3. v2 완료 관 목록 (68관)

### 미시경제학 (54관)

| 관 | 내용 |
|---|---|
| ch01-sec01-item01~04 | 경제학 정의/체제/기회비용/PPC |
| ch01-sec02-item01~02 | 실증·규범 / 이론·모형·가정 |
| ch02-sec01-item01~04 | 수요·공급·시장균형·균형이동 |
| ch02-sec02-item01~04 | 가격탄력성·소득교차탄력성·공급탄력성·탄력성과총수입 |
| ch02-sec03-item01~03 | 가격통제·조세귀착·보조금 |
| ch03-sec01-item01~03 | 효용·한계효용균등·수요곡선도출 |
| ch03-sec02-item01~04 | 무차별곡선·예산선·가격소득효과·슬러츠키 |
| ch03-sec03-item01~02 | 현시선호·수요곡선도출(현시선호) |
| ch03-sec04-item01~03 | 노동공급·시점간소비·소비자잉여 |
| ch03-sec05-item01~03 | 기대효용·위험태도·위험프리미엄과보험 |
| ch04-sec01-item01~04 | 생산함수·단기·장기·규모수익 |
| ch04-sec02-item01~03 | 회계경제비용·단기비용·장기비용규모경제 |
| ch05-sec01-item01~03 | 완전경쟁시장특징·단기이윤극대·장기균형 |
| ch05-sec02-item01~04 | 독점발생원인·이윤극대·가격차별·폐해규제 |
| ch05-sec03-item01~02 | 독점적경쟁특징·단기장기균형 |
| ch05-sec04-item01~02 | 과점특징모형·쿠르노베르트랑슈타켈베르크 |
| ch05-sec16-item03·04 | 굴절수요·카르텔담합 (이전 파일명 sec16) |
| ch05-sec05-item01·03 | 전략형게임내쉬·순차반복 |
| ch05-sec17-item02 | 죄수의딜레마 (이전 파일명 sec17) |
| ch06-sec01-item01 | 요소수요 (한계생산물가치) |
| ch07-sec22-item01 | 후생경제학 제1·2정리 |
| ch08-sec23-item01 | 시장실패의 원인 |

### 거시경제학 (7관)

| 관 | 내용 |
|---|---|
| ch01-sec04-item01 | 유효수요의 원리 |
| ch02-sec06-item02·04 | 한계효율·토빈 q이론 |
| ch03-sec07-item01 | 화폐의 기능과 통화지표 |
| ch06-sec15-item02 | 통화주의 |
| ch06-sec16-item02 | 새케인즈학파 |
| ch07-sec19-item01 | 해로드-도마 모형 |

### 재정학 (3관)

| 관 | 내용 |
|---|---|
| ch02-sec04-item04 | 클럽재 |
| ch02-sec05-item02 | 애로우 불가능성정리 |
| ch02-sec05-item04 | 지대추구행위 |

### 국제경제학 (0관)

## 4. 다음 우선순위 (미완료 167관)

### 4.1 미시 6장 (요소시장) — 진행 중, 8관 남음

| 관 | 내용 |
|---|---|
| ~~ch06-sec01-item01~~ | ~~요소수요 (완료)~~ |
| ch06-sec01-item02 | 요소공급 |
| ch06-sec01-item03 | 요소시장 균형 |
| ch06-sec02-item01~02 | 불완전경쟁 요소시장 (단조) |
| ch06-sec03-item01~02 | 임금·이자·지대 |
| ch06-sec04-item01~02 | 소득분배 (로렌츠·지니) |

### 4.2 미시 7장 (일반균형·후생) — 5관 남음

- ch07-sec20·21·22 (일반균형·에지워스·후생경제학 추가관)

### 4.3 미시 8장 (시장실패·정보) — 6관 남음

- ch08-sec23·24·25 (외부효과·공공재·정보경제학)

### 4.4 거시 1~7장 — 65관 남음 (큰 분량)

| 장 | 미완료 |
|---|---|
| 1장 국민소득결정 | 11관 |
| 2장 소비·투자함수 | 6관 |
| 3장 화폐금융론 | 6관 |
| 4장 총수요·총공급 | 12관 |
| 5장 인플레이션·실업 | 11관 |
| 6장 거시학파·안정화 | 6관 |
| 7장 경기변동·성장 | 7관 |

### 4.5 국제 1~2장 — 16관 남음

- 1장 무역론 (비교우위·HOS·관세) 8관
- 2장 금융론 (환율·국제수지) 8관

### 4.6 재정 1~7장 — 58관 남음 (큰 분량)

| 장 | 미완료 |
|---|---|
| 1장 재정학 개요 | 6관 |
| 2장 외부성·공공재 | 9관 |
| 3장 공공지출 | 8관 |
| 4장 조세 기초·전가 | 8관 |
| 5장 초과부담·최적과세 | 6관 |
| 6장 조세 경제효과 | 7관 |
| 7장 기타 | 14관 |

## 5. 그래프 라이브러리 53종

`viewer/public/data/practice/economics/graphs/` 의 SVG 파일들:

### 기본 시장
- demand-supply-equilibrium.svg
- tax-incidence.svg
- subsidy.svg
- price-ceiling.svg
- price-floor.svg
- elasticity-comparison.svg
- trade-gains.svg

### 소비자
- indifference-budget.svg
- ic-perfect-substitutes.svg
- ic-perfect-complements.svg
- giffen-good.svg
- engel-curve.svg
- income-consumption-curve.svg
- price-consumption-curve.svg
- substitution-income-effect.svg
- intertemporal-choice.svg
- utility-concave.svg

### 생산자·비용
- mp-ap.svg
- isoquant-isocost.svg
- cost-curves.svg
- lrac-envelope.svg
- ppc.svg

### 시장구조
- perfect-competition-long-run.svg
- monopoly.svg
- natural-monopoly.svg
- monopolistic-competition.svg
- kinked-demand.svg
- cournot-equilibrium.svg
- price-discrimination.svg

### 요소시장
- factor-market.svg
- labor-market.svg
- labor-backward-bending.svg
- monopsony.svg
- rent-economic.svg

### 게임이론
- game-payoff-prisoner.svg

### 거시
- as-ad.svg
- is-lm.svg
- keynes-cross.svg
- money-market.svg
- liquidity-trap.svg
- solow-growth.svg
- phillips-curve.svg
- marginal-efficiency.svg
- tobin-q.svg

### 국제
- comparative-advantage.svg
- exchange-rate.svg

### 후생·재정·외부효과
- externality-negative.svg
- externality-positive.svg
- public-good.svg
- coase-theorem.svg
- pigou-tax.svg
- lorenz-gini.svg
- edgeworth-box.svg

## 6. 파일 경로·동기화

- 작업 디렉토리: `/Users/hanjiho/Documents/감정평가사 기출문제`
- 문제 JSON: `viewer/public/data/practice/economics/{sub_slug}-ch{NN}-sec{NN}-item{NN}.json`
  - sub_slug: micro / macro / intl / fiscal
- SVG: `viewer/public/data/practice/economics/graphs/`
- 동기화: `python3 scripts/practice_to_app.py`
- 앱 viewer 렌더링: `viewer/src/ParsedText.jsx` ([IMAGE: ...] + KaTeX 처리)

## 7. 재개 절차 (요약)

사용자가 "경제학 문제 생성 이어가"라고 지시하면:

1. 이 파일 Read
2. 다음 우선순위에서 4관 골라 작성 (압축 모드)
3. 각 관 25문제, 계산 12 + 그래프 5 + 이론 8
4. 그래프는 53종 SVG에서 적합한 것 선택
5. KaTeX 수식 활용, 답 검증, 한국 사례 포함
6. 4관 묶음 작성 후 sync
7. 진척 보고 후 다음 명령 대기 (자율 진행 안 함)
