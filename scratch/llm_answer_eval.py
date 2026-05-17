"""3단계 사전 검증: LLM 정답 재도출 신뢰도 측정.
정답이 이미 있는 문항(정답+보기 정상)을 결손-결손 분포와 비슷한 시험/과목에서
표본 추출 → 정답 가린 채 LLM에 풀게 함 → 실제 정답과 비교.
전체 정확도 + confidence=high 한정 정확도로 3단계 진행 여부/임계값 판단.

python3 scratch/llm_answer_eval.py [N]
"""
import json, os, re, sys, random, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for line in open(os.path.join(BASE, ".env")):
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.strip().split("=", 1); os.environ.setdefault(k, v)

import google.generativeai as genai
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
MODEL = genai.GenerativeModel("gemini-2.5-flash")

N = int(sys.argv[1]) if len(sys.argv) > 1 else 30
db = json.load(open(os.path.join(BASE, "questions_db.json")))


def cls(q):
    iv = q.get("indexing_v4"); mt = iv and iv.get("mapped_taxonomy")
    return bool(iv and mt and mt.get("subject") and iv.get("processed_by") in
                ("gemini-2.5-flash", "claude-sonnet-4-6") and iv.get("in_scope") is not False)


# 결손이 많은 시험(보험계리사/회계사/세무사/감정평가사) 중 정답 정상 문항을 표본으로
pool = []
for q in db:
    if not cls(q):
        continue
    a = str(q.get("answer") or "").strip()
    o = q.get("options") or q.get("choices") or []
    if a.isdigit() and 1 <= int(a) <= len(o) and (q.get("question") or "").strip() and len(o) >= 4:
        if q.get("exam") in ("보험계리사", "회계사", "세무사", "감정평가사"):
            pool.append(q)
random.seed(42)
sample = random.sample(pool, min(N, len(pool)))

PROMPT = """다음은 객관식 기출문제입니다. 보기 중 정답 하나만 고르세요.
계산이 필요하면 풀이 후 판단하세요. 추측이 불가하면 confidence를 low로 하세요.
반드시 JSON만 출력: {{"answer": <보기번호 정수>, "confidence": "high|medium|low"}}

[문제] {q}

[보기]
{opts}"""

ok = okhi = hi = n = 0
by_exam = {}
for q in sample:
    o = q.get("options") or q.get("choices") or []
    opts = "\n".join(f"{i+1}. {re.sub(r'\\[IMAGE:[^\\]]+\\]', '(그림)', str(x))}" for i, x in enumerate(o))
    qt = re.sub(r"\[IMAGE:[^\]]+\]", "(그림)", str(q.get("question") or ""))
    try:
        r = MODEL.generate_content(PROMPT.format(q=qt[:4000], opts=opts[:4000]))
        m = re.search(r'\{.*\}', r.text, re.S)
        d = json.loads(m.group(0))
        pred, conf = str(d.get("answer")), d.get("confidence")
    except Exception as e:
        pred, conf = "?", "err"
    truth = str(q.get("answer")).strip()
    good = pred == truth
    n += 1; ok += good
    e = q.get("exam"); by_exam.setdefault(e, [0, 0]); by_exam[e][1] += 1; by_exam[e][0] += good
    if conf == "high":
        hi += 1; okhi += good
    print(f"{q.get('id'):28s} pred={pred} truth={truth} conf={conf} {'O' if good else 'X'}")
    time.sleep(0.4)

print(f"\n표본 {n} | 전체 정확도 {ok}/{n} = {ok/n:.0%}")
if hi:
    print(f"confidence=high {okhi}/{hi} = {okhi/hi:.0%}")
for e, (c, t) in by_exam.items():
    print(f"  {e}: {c}/{t}")
