#!/usr/bin/env python3
"""강의 필기 md → 노트 탭이 읽을 색인.

노트 탭(NotesPanel)은 지금까지 localStorage의 사용자 노트만 다뤘다. 강의 필기를 거기에
집어넣으면 500개 한도와 용량 제한을 갉아먹고 사용자가 쓴 메모와 섞여 지워질 수 있다.
그래서 강의 필기는 **파일로 두고 읽기 전용으로 합쳐** 보여준다. 이 색인이 그 목록이다.

본문 전체는 넣지 않는다(97개 관이면 수백 KB). 펼칠 때 md를 직접 가져가게 하고,
여기에는 미리보기만 담는다.

출력: viewer/public/data/study/lecture_notes_index.json

사용:
  python3 scripts/lectures/build_notes_index.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import STUDY

PHASE_LABEL = {
    'basic': '1회독 기본', 'deep': '2회독 심화', 'prac': '3회독 문풀',
    'mock': '4회독 모의', 'final': '마무리 특강',
}


def split_sections(md):
    """<!-- leaf: ... --> 앵커 기준으로 관별 구간을 자른다."""
    parts = []
    for m in re.finditer(r'<!--\s*leaf:\s*(\S+?)\s*-->', md):
        parts.append((m.group(1), m.start()))
    out = []
    for i, (leaf_id, pos) in enumerate(parts):
        end = parts[i + 1][1] if i + 1 < len(parts) else len(md)
        body = md[pos:end]
        title = ''
        tm = re.search(r'^##\s+(.+)$', body, flags=re.M)
        if tm:
            title = tm.group(1).strip()
        # 미리보기 — 앵커·주석·인용부호를 걷어낸 첫 본문
        clean = re.sub(r'<!--.*?-->', '', body, flags=re.S)
        clean = re.sub(r'^#{1,6}\s+.*$', '', clean, flags=re.M)
        clean = re.sub(r'^>.*$', '', clean, flags=re.M)
        clean = re.sub(r'^\s*-{3,}\s*$', '', clean, flags=re.M)   # 구분선
        clean = re.sub(r'[|`*_$]', '', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        out.append({
            'leaf_id': leaf_id,
            'title': title,
            'chars': len(body),
            'preview': clean[:220],
        })
    return out


def load_leaf_paths(subject):
    """leaf_id → 사람이 읽는 경로. leaf_id를 쪼개 쓰면 밑줄이 그대로 보이므로 원본 경로를 쓴다."""
    nm = STUDY / subject / 'lectures/note_map.json'
    if not nm.exists():
        return {}
    d = json.loads(nm.read_text(encoding='utf-8'))
    out = {}
    for p in d.get('pages', []):
        dp = p.get('dp') or {}
        if dp.get('leaf_id'):
            out[dp['leaf_id']] = dp.get('path', [])
    return out


def main():
    entries = []
    for notes_dir in sorted(STUDY.glob('*/lectures/notes')):
        subject = notes_dir.parents[1].name
        leaf_paths = load_leaf_paths(subject)
        for f in sorted(notes_dir.glob('*.md')):
            m = re.match(r'(.+?)\.(\w+)\.md$', f.name)
            if not m:
                continue
            unit_code, phase = m.group(1), m.group(2)
            md = f.read_text(encoding='utf-8')
            for sec in split_sections(md):
                # 출처 줄에서 강의 번호를 뽑아 태그로 쓴다
                lec = re.findall(r'(\d+강)', md[:600])
                entries.append({
                    **sec,
                    'path': leaf_paths.get(sec['leaf_id'], []),
                    'subject': subject,
                    'unit_code': unit_code,
                    'phase': phase,
                    'phase_label': PHASE_LABEL.get(phase, phase),
                    'file': f'/data/study/{subject}/lectures/notes/{f.name}',
                    'lectures': sorted(set(lec))[:4],
                })

    dst = STUDY / 'lecture_notes_index.json'
    dst.write_text(json.dumps({
        'count': len(entries),
        'notes': entries,
    }, ensure_ascii=False, indent=1), encoding='utf-8')

    by_subj = {}
    for e in entries:
        by_subj.setdefault(e['subject'], 0)
        by_subj[e['subject']] += 1
    print(f'강의 필기 {len(entries)}개 색인')
    for k, v in sorted(by_subj.items()):
        print(f'  {k}: {v}개')
    print(f'저장: {dst}')


if __name__ == '__main__':
    main()
