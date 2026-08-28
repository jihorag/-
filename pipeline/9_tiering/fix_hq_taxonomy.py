#!/usr/bin/env python3
"""hq 문항의 관(item) 매핑 보정 + 데이터 오류 수정.

hq 수제 문항 2,240개는 item 이 빈 문자열이라 앱의 관 카드에 안 잡힌다.
관 제목의 키워드를 본문과 맞춰 배정하고, 안 걸리면 그 절의 첫 관으로 보낸다.
빈 문자열로 두면 아예 안 보이므로 첫 관이라도 배정하는 쪽이 낫다.

함께 고치는 것: 중복 ID 5건, difficulty 이상치 1건.

사용:
  python3 pipeline/9_tiering/fix_hq_taxonomy.py [--dry-run] [--self-test]
"""
import json
import re
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DB = ROOT / "questions_db_econ.json"
TAX = ROOT / "taxonomy_v4.json"
BACKUP_DIR = Path(__file__).resolve().parent / "backup"
STOP = re.compile(r"^제\d+관\s*")


def pick_item(sections, section_name, question):
    """절 안의 관 중 본문과 키워드가 겹치는 것을 고른다.

    반환: (관 이름, 배정 방식). 배정 방식은 "keyword"(키워드 매칭 성공),
    "fallback"(못 맞춰서 첫 관으로 보냄), ""(절/관이 없어 아무것도 못 함).
    """
    items = sections.get(section_name) or []
    if not items:
        return "", ""
    body = question or ""
    best, best_hit = "", 0
    for it in items:
        title = STOP.sub("", it)
        words = [w for w in re.split(r"[\s·,]+", title) if len(w) >= 2]
        hit = sum(1 for w in words if w in body)
        if hit > best_hit:
            best, best_hit = it, hit
    if best:
        return best, "keyword"
    return items[0], "fallback"


def build_sections(tax):
    """taxonomy_v4 에서 {절 이름: [관 이름...]} 을 만든다.

    과목에 세부과목이 있으면 subjects 아래, 없으면 chapters 아래에 장이 있다.
    경제학은 전자지만 둘 다 받아 둔다.
    """
    out = {}
    econ = tax.get("경제학원론") or {}
    groups = list((econ.get("subjects") or {}).values()) + [econ.get("chapters") or []]
    for chapters in groups:
        for ch in chapters or []:
            for sec in ch.get("sections") or []:
                out[sec["name"]] = [it["name"] for it in (sec.get("items") or [])]
    return out


def backfill_tags(dry=False):
    """356acf1e 커밋 직전에 채운 2,100건은 item_assigned_by 없이 저장됐다.

    당시 백업(item이 비어 있던 시점의 스냅샷)과 현재 db를 인덱스로 대조해
    "그때 비어 있었는데 지금은 채워진" 문항에만 소급으로 태그를 붙인다.
    v1 자동생성분(당시 이미 item이 있던 문항)은 백업에서도 item이 있으므로
    조건에서 자동으로 제외된다 — 건드리지 않는다.
    """
    db = json.loads(DB.read_text(encoding="utf-8"))
    sections = build_sections(json.loads(TAX.read_text(encoding="utf-8")))
    backups = sorted(BACKUP_DIR.glob("econ.pre_taxfix_*.json"))
    if not backups:
        print("백업 없음 — 소급 태깅 불가")
        return
    backup = json.loads(backups[0].read_text(encoding="utf-8"))
    if len(backup) != len(db):
        print(f"경고: 백업({len(backup)})과 현재 db({len(db)}) 길이가 달라 인덱스 대조 불가")
        return

    tagged = Counter()
    for qb, qc in zip(backup, db):
        mtb = (qb.get("indexing_v4") or {}).get("mapped_taxonomy")
        if not mtb or mtb.get("item"):
            continue  # 당시 이미 item 있었음 (v1 자동생성분) — 건드리지 않음
        ivc = qc.get("indexing_v4") or {}
        mtc = ivc.get("mapped_taxonomy") or {}
        if not mtc.get("item") or ivc.get("item_assigned_by"):
            continue
        _, method = pick_item(sections, mtb.get("section"), qb.get("question"))
        if method:
            if not dry:
                ivc["item_assigned_by"] = method
            tagged[method] += 1

    print(f"소급 태깅 keyword {tagged['keyword']} · fallback {tagged['fallback']}")
    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_backfill_{ts}.json")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장 완료 (백업 econ.pre_backfill_{ts}.json)")


def main():
    if "--self-test" in sys.argv:
        _self_test()
        return

    if "--backfill-tags" in sys.argv:
        backfill_tags(dry="--dry-run" in sys.argv)
        return

    dry = "--dry-run" in sys.argv
    db = json.loads(DB.read_text(encoding="utf-8"))
    sections = build_sections(json.loads(TAX.read_text(encoding="utf-8")))

    filled = 0
    for q in db:
        mt = (q.get("indexing_v4") or {}).get("mapped_taxonomy")
        if not mt or mt.get("item"):
            continue
        item, method = pick_item(sections, mt.get("section"), q.get("question"))
        if item:
            if not dry:
                mt["item"] = item
                q["indexing_v4"]["item_assigned_by"] = method
            filled += 1

    # 중복 ID 재부여 — 뒤에 나온 것에 접미사를 붙인다
    seen, fixed_ids = set(), 0
    for q in db:
        qid = q.get("id")
        if qid in seen:
            n = 2
            while f"{qid}-dup{n}" in seen:
                n += 1
            if not dry:
                q["id"] = f"{qid}-dup{n}"
            seen.add(f"{qid}-dup{n}")
            fixed_ids += 1
        else:
            seen.add(qid)

    # difficulty 이상치 — 1~5 밖이면 3으로 되돌린다
    fixed_diff = 0
    for q in db:
        iv = q.get("indexing_v4") or {}
        d = iv.get("difficulty")
        if isinstance(d, int) and not (1 <= d <= 5):
            if not dry:
                iv["difficulty"] = 3
                mt = iv.get("mapped_taxonomy")
                if mt:
                    mt["difficulty"] = 3
            fixed_diff += 1

    print(f"item 채움 {filled} · 중복 ID 수정 {fixed_ids} · difficulty 교정 {fixed_diff}")
    left = sum(1 for q in db
               if not (((q.get("indexing_v4") or {}).get("mapped_taxonomy") or {}).get("item")))
    print(f"여전히 item 빈 문항: {left}")

    if dry:
        print("dry-run — 저장하지 않음")
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DB, BACKUP_DIR / f"econ.pre_taxfix_{ts}.json")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장 완료 (백업 econ.pre_taxfix_{ts}.json)")


def _self_test():
    sections = {"제13절 완전경쟁시장": ["제1관 완전경쟁의 조건", "제2관 단기 이윤극대화"]}

    # 관 이름의 키워드가 본문에 있으면 그 관으로 간다 — "keyword"로 표시
    assert pick_item(sections, "제13절 완전경쟁시장",
                     "단기 이윤극대화 생산량은?") == ("제2관 단기 이윤극대화", "keyword")

    # 아무 관에도 안 걸리면 첫 관으로 보낸다(빈 문자열보다 낫다) — "fallback"으로 표시
    assert pick_item(sections, "제13절 완전경쟁시장",
                     "전혀 관계없는 본문") == ("제1관 완전경쟁의 조건", "fallback")

    # 모르는 절이면 빈 문자열 + 빈 표시
    assert pick_item(sections, "없는절", "본문") == ("", "")

    # 관이 없는 절이면 빈 문자열 + 빈 표시
    assert pick_item({"제1절 빈절": []}, "제1절 빈절", "본문") == ("", "")
    print("fix_hq_taxonomy self-test 통과")


if __name__ == "__main__":
    main()
