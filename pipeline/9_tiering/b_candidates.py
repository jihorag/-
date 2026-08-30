#!/usr/bin/env python3
"""B 후보 추출 — 규칙으로 좁히고, 판정은 사람(에이전트)이 한다.

기판정 A 549 / B 133 에서 뽑은 판별 신호로 점수를 매긴다.
가중치는 A 대비 B 에서의 출현비(판별력)에 맞췄다.

  숫자 3개 이상  B 38% / A  5%  → 7.6배 → 3점
  단서(단,)      B 14% / A  6%  → 2.3배 → 1점
  연산자 포함    B 28% / A 13%  → 2.2배 → 1점
  본문 100자+    B 47% / A 29%  → 1.6배 → 1점
  박스형 ㄱㄴㄷ  B 23% / A 16%  → 1.4배 → 1점

점수는 B 가능성의 순위일 뿐 등급이 아니다. 등급은 사람이 읽고 정한다.

사용:
  python3 pipeline/9_tiering/b_candidates.py --min-score 5 [--out FILE]
  python3 pipeline/9_tiering/b_candidates.py --self-test
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
OUT = Path(__file__).resolve().parent / "b_candidates.json"

NUM = re.compile(r"\d")
OPS = re.compile(r"[=+\-*/^×÷]|\\frac")
BOX = re.compile(r"ㄱ[.,、]|ㄴ[.,、]|ㄷ[.,、]")
COND = re.compile(r"단,|가정하|라고 하자|주어졌")
# 연도는 계산이 아니다. 학설사 연표(1879·1920·1927…)가 숫자로 세어져
# 점수를 부풀리는 것을 막는다.
YEAR = re.compile(r"\(?\b(1[89]\d\d|20[0-4]\d)\b년?\)?")
HISTORY = re.compile(r"발전사|학설사|의 역사")


def score(q):
    t = q.get("question") or ""
    if HISTORY.search(t):        # 학설사 나열형은 계산문제가 아니다
        return 0
    t_nonyear = YEAR.sub(" ", t)
    s = 0
    if len(NUM.findall(t_nonyear)) >= 3:
        s += 3
    if OPS.search(t):
        s += 1
    if len(t) >= 100:
        s += 1
    if COND.search(t):
        s += 1
    if BOX.search(t):
        s += 1
    return s


def _self_test():
    assert score({"question": "가" * 50}) == 0
    # 숫자 3개
    assert score({"question": "Q=1, P=2, T=3 이다"}) >= 3
    # 본문 100자 + 단서
    long_cond = {"question": "가" * 100 + " 단, 조건이 있다"}
    assert score(long_cond) == 2
    # 박스형
    assert score({"question": "ㄱ. 하나 ㄴ. 둘 ㄷ. 셋"}) == 1
    # 모두 겹치면 최대 7
    full = {"question": "Q=1 P=2 T=3 " + "가" * 100 + " 단, ㄱ. 하나 ㄴ. 둘"}
    assert score(full) == 7

    # 연도는 숫자로 세지 않는다 — 학설사 연표가 계산문제로 오인되던 결함
    years = {"question": "마샬(1890), 피구(1920), 램지(1927)의 기여를 고르면?"}
    assert score(years) == 0
    # 연도와 실제 수치가 섞이면 수치만 센다
    mixed = {"question": "케인즈(1936) 모형에서 C=100, I=50, G=30 일 때 Y는?"}
    assert mixed and score(mixed) >= 3
    # 발전사 문항은 점수를 주지 않는다
    assert score({"question": "다음은 효용 이론의 발전사이다. Q=1 P=2 T=3"}) == 0
    print("b_candidates self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return
    mn = 5
    if "--min-score" in sys.argv:
        mn = int(sys.argv[sys.argv.index("--min-score") + 1])

    db = json.loads(DB.read_text(encoding="utf-8"))
    un = [q for q in db if not q.get("tier")]
    scored = [(score(q), q) for q in un]
    print(f"미판정 {len(un)}건 점수 분포:", dict(sorted(Counter(s for s, _ in scored).items(), reverse=True)))

    picked = [q for s, q in scored if s >= mn]
    picked.sort(key=lambda q: -score(q))
    slim = [{"id": q["id"], "score": score(q), "src": "hq" if "-hq-" in q["id"] else "v1",
             "question": q.get("question"), "options": q.get("options"),
             "answer": q.get("answer"), "explanation": q.get("explanation"),
             "item": ((q.get("indexing_v4") or {}).get("mapped_taxonomy") or {}).get("item"),
             "section": ((q.get("indexing_v4") or {}).get("mapped_taxonomy") or {}).get("section")}
            for q in picked]
    OUT.write_text(json.dumps(slim, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"점수 {mn} 이상 {len(slim)}건 → {OUT.name}")
    print("  출처:", Counter(x["src"] for x in slim).most_common())


if __name__ == "__main__":
    main()
