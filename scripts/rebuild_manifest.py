#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""essay/practice manifest의 카운트 필드를 chapter JSON에서 전부 재계산하는 단일 소스.
여러 스크립트가 부분 갱신하며 생긴 stale 값(count·withAnswer·matchedAnswer·rounds) 정합 복구.
sync-data 이후 또는 데이터 스크립트 실행 후 항상 이것만 돌리면 됨.

- count        = chapter json 문항 수 (generated 별도 파일은 generatedCount 유지)
- withAnswer   = modelAnswer 비어있지 않은 문항 수
- matchedAnswer= withAnswer 와 동일 의미로 통일(과거 매처 잔재 제거)
- rounds       = GS 단원(gs*)은 제외(내부 세션 인코딩이라 UI 노출 무의미), 그 외 실제 회차만
- total        = cleanup 제외 합(학습 가능 문항 기준)
"""
import json
from pathlib import Path

DATA = Path('viewer/public/data/essay/practice')

mf = DATA / 'manifest.json'
m = json.loads(mf.read_text(encoding='utf-8'))

for ch in m['chapters']:
    cid = ch['id']
    f = DATA / f'{cid}.json'
    if not f.exists():
        ch['count'] = 0
        ch['withAnswer'] = ch['matchedAnswer'] = 0
        ch['rounds'] = []
        continue
    qs = json.loads(f.read_text(encoding='utf-8')).get('questions', [])
    ch['count'] = len(qs) + ch.get('generatedCount', 0)
    wa = sum(1 for q in qs if q.get('modelAnswer'))
    ch['withAnswer'] = wa
    ch['matchedAnswer'] = wa
    if cid.startswith('gs'):
        ch['rounds'] = []  # 세션 인코딩(101=1주차-1) — UI 노출 안 함
        ch['sessionCount'] = len({q.get('session') for q in qs if q.get('session')})
    else:
        ch['rounds'] = sorted({q.get('round') for q in qs
                               if isinstance(q.get('round'), int) and q.get('source') == 'official'})

m['total'] = sum(ch.get('count', 0) for ch in m['chapters'] if ch['id'] != 'cleanup')

mf.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf-8')
print('manifest 재계산 완료:')
for ch in m['chapters']:
    if ch.get('count'):
        extra = f" 세션{ch['sessionCount']}" if ch.get('sessionCount') else ''
        print(f"  {ch['id']:8s} count={ch['count']:4d} 답안={ch['withAnswer']:3d}{extra}")
print(f"  total(학습가능)={m['total']}")
