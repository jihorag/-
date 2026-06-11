#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""품질 감사 결과 적용 — drop 판정 문항을 DB에서 분리.

안전장치:
  - 기본은 dry-run (무엇이 빠지는지 출력만). 실제 적용은 --apply 명시.
  - 적용 시: DB 백업(.bak-날짜) + 제거 문항은 scratch/quality_audit/removed_{db}.json 에 보존
  - 이후 cd viewer && npm run sync-data 재실행 필요 (안내 출력)

사용:
  python3 scratch/quality_apply_local.py questions_db_re.json                 # 미리보기
  python3 scratch/quality_apply_local.py questions_db_re.json --apply         # drop 제거
  python3 scratch/quality_apply_local.py questions_db_re.json --also-review --apply  # review까지 제거
"""
import argparse
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = ROOT / 'scratch' / 'quality_audit'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('db')
    ap.add_argument('--apply', action='store_true', help='실제로 DB에서 제거 (기본은 미리보기)')
    ap.add_argument('--also-review', action='store_true', help='review 판정도 함께 제거')
    args = ap.parse_args()

    db_path = ROOT / args.db
    if db_path.name == 'questions_db.json':
        raise SystemExit('🚫 기출(questions_db.json)은 원본 보존 — 삭제 적용 불가. '
                         '정답 불일치는 감사 리포트(answer_mismatch)를 보고 수동 교정하세요.')
    audit_path = AUDIT_DIR / (db_path.stem + '.jsonl')
    if not audit_path.exists():
        raise SystemExit(f'감사 파일 없음: {audit_path} — quality_audit_local.py 먼저 실행')

    target_verdicts = {'drop'} | ({'review'} if args.also_review else set())
    audits = {}
    for line in audit_path.read_text(encoding='utf-8').splitlines():
        try:
            r = json.loads(line)
            audits[r['id']] = r
        except (json.JSONDecodeError, KeyError):
            pass

    db = json.load(open(db_path, encoding='utf-8'))
    removed, kept = [], []
    for q in db:
        a = audits.get(q.get('id'))
        if a and a.get('verdict') in target_verdicts:
            removed.append({**q, '_audit': {k: a.get(k) for k in ('score', 'issues', 'reason', 'verdict')}})
        else:
            kept.append(q)

    print(f'{db_path.name}: 전체 {len(db)} → 유지 {len(kept)} / 제거 대상 {len(removed)}'
          f' (감사 완료 {len(audits)}건, 대상 판정 {sorted(target_verdicts)})')
    # 제거 대상 절별 분포
    by_sec = {}
    for q in removed:
        sec = ((q.get('indexing_v4') or {}).get('mapped_taxonomy') or {}).get('item') or '?'
        by_sec[sec] = by_sec.get(sec, 0) + 1
    for sec, n in sorted(by_sec.items(), key=lambda x: -x[1])[:10]:
        print(f'   {n:4d}  {sec}')

    if not args.apply:
        print('\n(미리보기 — 실제 적용은 --apply)')
        return

    stamp = time.strftime('%Y%m%d-%H%M')
    bak = db_path.with_suffix(f'.json.bak-{stamp}')
    bak.write_bytes(db_path.read_bytes())
    (AUDIT_DIR / f'removed_{db_path.stem}.json').write_text(
        json.dumps(removed, ensure_ascii=False, indent=1), encoding='utf-8')
    db_path.write_text(json.dumps(kept, ensure_ascii=False), encoding='utf-8')
    print(f'\n✅ 적용 완료. 백업: {bak.name}')
    print(f'   제거 문항 보존: scratch/quality_audit/removed_{db_path.stem}.json')
    print('   다음 단계: cd viewer && npm run sync-data')


if __name__ == '__main__':
    main()
