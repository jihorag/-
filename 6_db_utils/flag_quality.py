"""4단계: 복구 불가 결함을 questions_db.json 에 명시 플래그.

3단계(LLM 재도출)는 4개 모델 측정 결과 최고 gpt-4o 54%@high 로
학습 DB 주입 부적합 판정 → 미적용. 대신 결함을 q.data_quality 에 기록해
감사·필터·앱 노출 옵션의 근거로 삼는다. (앱은 런타임에서 이미 우아하게
degrade: 무효정답=채점제외, 보기없음=안내. 본 플래그는 데이터측 표식.)

플래그:
  no_options      : 보기 없음
  no_answer       : 정답 무효/빈/센티넬 (정규화 후에도 1..보기수 숫자 아님)
  no_explanation  : 해설 없음 (학습 보조 약함; 노출은 유지)

사용: python3 6_db_utils/flag_quality.py [--apply]
"""
import json, os, sys, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE, "questions_db.json")


def answer_valid(q):
    a = str(q.get("answer") or "").strip()
    o = q.get("options") or q.get("choices") or []
    return a.isdigit() and 1 <= int(a) <= len(o)


def main():
    apply = "--apply" in sys.argv
    db = json.load(open(DB))
    cnt = collections.Counter()
    for q in db:
        o = q.get("options") or q.get("choices") or []
        flags = []
        if not o:
            flags.append("no_options")
        if not answer_valid(q):
            flags.append("no_answer")
        if not (q.get("explanation") or "").strip():
            flags.append("no_explanation")
        for f in flags:
            cnt[f] += 1
        if apply:
            dq = q.get("data_quality") or {}
            # 1단계 표식(answer_normalized)은 보존
            for key in ("no_options", "no_answer", "no_explanation"):
                if key in flags:
                    dq[key] = True
                elif key in dq:
                    del dq[key]            # 보정/복구되면 해제
            if dq:
                q["data_quality"] = dq
            elif "data_quality" in q:
                del q["data_quality"]

    print("플래그 집계(전체 DB):", dict(cnt))
    if apply:
        tmp = DB + ".tmp"
        json.dump(db, open(tmp, "w"), ensure_ascii=False, indent=2)
        os.replace(tmp, DB)
        print("적용 완료 → questions_db.json")
    else:
        print("(dry-run) 적용하려면 --apply")


if __name__ == "__main__":
    main()
