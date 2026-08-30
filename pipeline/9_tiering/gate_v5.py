#!/usr/bin/env python3
"""게이트 v5 — 주제어만 갈아 끼운 메타 진술 껍데기를 걸러낸다.

v1 생성기는 절마다 같은 문항 틀을 찍어내며 주제어만 바꿨다. 그 결과
"부분균형 분석", "하버거 모형", "초과부담" 어느 것을 넣어도 성립하는
문항이 대량으로 남았다. 정답은 "…분석 방법·가정·정책 함의에 차이가
있을 수 있다" 같은 일반론이고 오답은 "마르크스 경제학은 시장 분석을
완전히 거부한다" 같은 고정 문구다. 주제를 몰라도 소거로 풀린다.

gate_v4 가 접두사 반복을 봤다면 여기서는 오답에 반복되는 상투 문구
자체를 본다. 선지 중 둘 이상이 목록에 걸리면 껍데기로 본다. 하나만
걸리는 경우는 정상 문항의 오답이 우연히 닮았을 수 있어 남긴다.

목록은 repair 집합에서 8회 이상 반복된 선지 골격을 추출해 만들었고,
도메인 주장(예: "변동성을 무한대로 증폭시킨다")은 정상 오답일 수
있으므로 제외하고 분석·학파·개념에 관한 메타 진술만 담았다.

사용:
  python3 pipeline/9_tiering/gate_v5.py [--dry-run] [--self-test]
"""
import json
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tier_judge import _atomic_write_json          # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"
MACHINE = {"tier_gate", "gate_v2", "gate_v3", "gate_v4", "gate_v5"}
MIN_HITS = 2

BOILERPLATE = (
    "정치적 견해 채택", "정치적 신념으로만 결정", "학문적 발전을 저해",
    "단기·장기 구분은 모든 학파에서 동일", "단기와 장기 구분 없이 동일한 결과",
    "단기 분석만 가능하며 장기는 의미가 없", "항상 장기 분석만 가능",
    "단기에는 가격 경직성, 장기에는 가격 신축성을 일반적으로 가정",
    "관련 개념의 차이는 임의로 결정", "관련 개념과 완전히 동일하며 구분이 불가능",
    "항상 관련 개념보다 우월한 분석력", "비교가 학문적으로 금기시",
    "시장 분석을 완전히 거부", "합리적 선택 가정만 사용",
    "단기 가격 경직성 가정은 모든 학파에서 거부",
    "다른 경제 변수와 무관하게 발생", "정부 정책에만 영향을 미치고 시장에는 영향이 없",
    "항상 동일한 크기로 모든 변수에 동일 영향", "측정 불가능하여 분석의 의미가 없",
    "특정 학파의 전유물이며 다른 학파는 다룰 수 없",
    "경제학의 모든 분야를 포괄하는 단일 통합 이론",
    "모형을 무시하고 직관에만 의존", "가정의 검토 없이 시행", "정량적 추정이 불가능",
    "자료의 의미와 무관하게 임의로 결정",
    "측정 자체가 불가능하여 학문적 분석 대상이 아니",
    "시대에 따라 그 의미가 완전히 달라져 일관된 정의가 불가능",
    "경제학과 무관한 분야의 개념", "항상 정부의 직접적 개입으로만 분석",
    "학파별로", "분석 방법·가정·정책 함의에 차이",
)


def boilerplate_hits(q):
    joined = " | ".join(str(o) for o in (q.get("options") or []))
    return sum(1 for phrase in BOILERPLATE if phrase in joined)


def is_shell(q):
    return boilerplate_hits(q) >= MIN_HITS


def _self_test():
    shell = {"options": ["마르크스 경제학은 시장 분석을 완전히 거부한다",
                         "행동경제학은 합리적 선택 가정만 사용한다",
                         "신고전학파의 한계분석은 X 분석에도 적용된다",
                         "정상 선지", "정상 선지2"]}
    assert boilerplate_hits(shell) == 2 and is_shell(shell)

    # 하나만 걸리면 정상 문항의 오답일 수 있으므로 남긴다
    one = {"options": ["마르크스 경제학은 시장 분석을 완전히 거부한다",
                       "수요곡선은 우하향한다", "공급곡선은 우상향한다",
                       "탄력성은 1이다", "균형은 교점이다"]}
    assert boilerplate_hits(one) == 1 and not is_shell(one)

    normal = {"options": ["균형가격 30, 균형거래량 60", "균형가격 26, 균형거래량 68",
                          "균형가격 20, 균형거래량 80", "균형가격 25, 균형거래량 45",
                          "균형가격 30, 균형거래량 30"]}
    assert boilerplate_hits(normal) == 0 and not is_shell(normal)

    assert not is_shell({"options": []})
    print("gate_v5 self-test 통과")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return
    dry = "--dry-run" in sys.argv

    db = json.loads(DB.read_text(encoding="utf-8"))
    now = datetime.now().strftime("%Y-%m-%d")
    hit, from_tier = 0, Counter()
    for q in db:
        tm = q.get("tier_meta") or {}
        if tm.get("decided_by") in MACHINE:
            continue
        if not is_shell(q):
            continue
        hit += 1
        from_tier[q.get("tier") or "미판정"] += 1
        if dry:
            continue
        tm = q.get("tier_meta") or {}
        tm.update({"prev_tier": q.get("tier"), "prev_decided_by": tm.get("decided_by"),
                   "prev_reason": tm.get("reason"), "decided_by": "gate_v5",
                   "decided_at": now, "reason": "메타진술 껍데기(상투 오답 2개 이상)"})
        q["tier_meta"] = tm
        q["tier"] = "discard"

    print(f"  껍데기 검출: {hit}")
    print("  등급별 출처:", dict(from_tier))
    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_gate_v5_{ts}.json")
    _atomic_write_json(DB, db)
    print(f"저장 완료 (백업 econ.pre_gate_v5_{ts}.json)")


if __name__ == "__main__":
    main()
