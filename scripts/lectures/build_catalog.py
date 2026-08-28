#!/usr/bin/env python3
"""인터넷강의 파일명 → 강의 카탈로그 JSON.

원본은 외장(/Volumes/WD_Black)에 두고, 메타데이터만 뽑아 앱 데이터로 만든다.
파일명이 유일한 메타 소스이므로 여기서 최대한 긁어낸다:
  "12강 - 25:07:10 노트 7번, 감평민법 10면 중단 (60분).mp4"
   └강번호   └녹화일        └주제              └교재면 └재생시간

출력: (PC앱) public/data/study/{subject}/lectures/catalog.json

주의 — 파일명이 macOS NFD로 저장돼 있어 NFC 정규화 없이는 한글 정규식이 전부 빗나간다.
      AppleDouble(._*) 2,482개가 섞여 있어 제외하지 않으면 강의 수가 정확히 2배가 된다.
"""
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import SRC_ROOT as SRC  # 경로는 _paths.py 한 곳에서만 정한다
from _paths import require_drive, STUDY as OUT_ROOT  # 산출은 PC앱으로

# 1차만 대상 (2차는 보류)
SUBJECTS = {
    '1차_경제학': ('economics', '경제학원론'),
    '1차_민법': ('civil', '민법'),
    '1차_부동산학원론': ('realestate', '부동산학원론'),
    '1차_감관법': ('law', '감정평가관계법규'),
    '1차_회계학': ('accounting', '회계학'),
}

# 커리큘럼 단계 = 회독 축. 긴 것부터 매칭해야 '기본이론'이 '기초이론'을 삼키지 않는다.
PHASES = [
    ('입문', 'intro', '입문'),
    ('기초이론', 'found', '기초이론'),
    ('기본이론', 'basic', '기본이론'),
    ('심화이론', 'deep', '심화이론'),
    ('문제풀이', 'prac', '문제풀이'),
    ('모의', 'mock', '모의+핵심'),
    ('특강', 'final', '특강'),
]


def nfc(s):
    return unicodedata.normalize('NFC', s)


def probe_minutes(path):
    """파일명에 재생시간이 없을 때만 ffprobe로 실측(초 → 분)."""
    import subprocess
    try:
        out = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'csv=p=0', path],
            capture_output=True, text=True, timeout=60)
        return round(float(out.stdout.strip()) / 60)
    except Exception:
        return None


def detect_phase(course_name):
    for ko, code, label in PHASES:
        if ko in course_name:
            return code, label
    return 'etc', '기타'


def parse_lecture(rel_parts, abs_path):
    """rel_parts = [과목, 강사, 과정, ..., 파일명] — 과정 폴더 없이 파일이 바로 놓인 경우도 있다."""
    fname = rel_parts[-1]
    stem = re.sub(r'\.(mp4|mov)$', '', fname, flags=re.I)

    # 과정명: 강사 아래 폴더. 없으면(파일이 강사 폴더 직속) 파일명 자체를 과정 취급.
    course = rel_parts[2] if len(rel_parts) >= 4 else stem
    phase, phase_ko = detect_phase(course)

    m = re.match(r'\s*(\d+)\s*강', stem)
    no = int(m.group(1)) if m else None

    m = re.search(r'\((\d+)\s*분\)', stem)
    minutes = int(m.group(1)) if m else None

    # 면수 힌트. 손병익 기본이론은 "(p.170~188 : 필기노트 p.24~27)" 처럼
    # 교재 면수와 필기노트 면수를 콜론으로 나란히 적는다 → 첫 구간이 교재, 둘째가 필기노트.
    # 민법·이론은 "10면", "(p78~86)" 처럼 교재 면수만 적는다.
    ranges = []
    for mm in re.finditer(r'p[.,]?\s*(\d+)\s*(?:[~\-–]\s*(\d+))?', stem, flags=re.I):
        a, b = mm.groups()
        ranges.append([int(a), int(b) if b else int(a)])
    for mm in re.finditer(r'(\d+)\s*면', stem):
        ranges.append([int(mm.group(1)), int(mm.group(1))])

    book_pages = ranges[0] if ranges else None
    # 두 구간이 나오면 뒤쪽은 필기노트 면수다("p.86~90:p.12~16"처럼 단어가 생략되기도 한다).
    note_pages = ranges[1] if len(ranges) > 1 else None
    pages = sorted({n for r in ranges for n in r}) or None

    # 주제 힌트 — 강번호·날짜·재생시간을 걷어낸 나머지
    topic = stem
    topic = re.sub(r'^\s*\d+\s*강\s*[-–]?\s*', '', topic)
    topic = re.sub(r'\d{2}:\d{2}:\d{2}_?', '', topic)
    topic = re.sub(r'\(\d+\s*분\)', '', topic)
    topic = re.sub(r'\[\d+주차\]', '', topic)
    topic = re.sub(r'\s{2,}', ' ', topic).strip(' -–_,')

    try:
        size = os.path.getsize(abs_path)
    except OSError:
        size = None

    return {
        'no': no,
        'title': stem,
        'course': course,
        'phase': phase,
        'phase_ko': phase_ko,
        'minutes': minutes,
        'pages': pages,
        'book_pages': book_pages,
        'note_pages': note_pages,
        'topic_hint': topic or None,
        'size_bytes': size,
        'path': str(abs_path),
    }


def main():

    require_drive()
    if not SRC.exists():
        sys.exit(f'외장 드라이브를 찾을 수 없습니다: {SRC}\n외장이 마운트됐는지 확인하세요.')

    per_subject = {}
    for subj_dir, (sid, ko) in SUBJECTS.items():
        base = SRC / subj_dir
        if not base.exists():
            print(f'  건너뜀(없음): {subj_dir}')
            continue

        items = []
        for p in base.rglob('*'):
            if not p.is_file():
                continue
            name = nfc(p.name)
            if name.startswith('._') or not re.search(r'\.(mp4|mov)$', name, flags=re.I):
                continue
            rel = [nfc(x) for x in p.relative_to(SRC).parts]
            entry = parse_lecture(rel, p)
            entry['instructor'] = rel[1] if len(rel) >= 3 else None
            entry['subject'] = sid
            items.append(entry)

        # 같은 과정·같은 강 번호가 둘 이상일 때만 실제 재생시간을 재서 중복 여부를 가른다.
        # 파일명이 같아도 내용이 다른 경우가 있다(민법 '7강 …밑줄영상' 4분짜리와 56분짜리).
        # 재생시간이 15% 이내로 붙어야 같은 녹화본으로 보고 용량 큰 쪽(고화질)만 남긴다.
        seen_no = {}
        for it in items:
            if it['no'] is not None:
                seen_no.setdefault((it['course'], it['no']), []).append(it)
        for group in seen_no.values():
            if len(group) > 1:
                for it in group:
                    if it['minutes'] is None:
                        it['minutes'] = probe_minutes(it['path'])

        dup_excluded = []
        keep = []
        for (course, no), group in seen_no.items():
            if len(group) == 1:
                continue
            group.sort(key=lambda x: -(x['size_bytes'] or 0))
            best = group[0]
            for other in group[1:]:
                a, b = best['minutes'] or 0, other['minutes'] or 0
                if a and b and abs(a - b) / max(a, b) <= 0.15:
                    dup_excluded.append(other)
        dup_paths = {d['path'] for d in dup_excluded}
        items = [it for it in items if it['path'] not in dup_paths]
        del keep

        # 단계 → 강 번호 순. 번호 없는 건 뒤로.
        phase_order = {code: i for i, (_, code, _) in enumerate(PHASES)}
        items.sort(key=lambda x: (phase_order.get(x['phase'], 99), x['no'] if x['no'] else 9999))
        for i, it in enumerate(items):
            it['id'] = f"{sid}-{it['phase']}-{i + 1:03d}"

        if dup_excluded:
            print(f'    ↳ 중복본 {len(dup_excluded)}개 제외: '
                  + ', '.join(sorted({os.path.basename(os.path.dirname(d['path'])) for d in dup_excluded})))
        per_subject[sid] = {'ko': ko, 'items': items, 'dup': dup_excluded}

    total_n = total_min = 0
    for sid, data in per_subject.items():
        items = data['items']
        out_dir = OUT_ROOT / sid / 'lectures'
        out_dir.mkdir(parents=True, exist_ok=True)

        # 단계별 요약 — 회독 배지 UI가 바로 쓸 수 있는 형태
        phases = {}
        for it in items:
            ph = phases.setdefault(it['phase'], {
                'phase': it['phase'], 'label': it['phase_ko'],
                'count': 0, 'minutes': 0, 'instructors': set(), 'courses': set(),
            })
            ph['count'] += 1
            ph['minutes'] += it['minutes'] or 0
            if it['instructor']:
                ph['instructors'].add(it['instructor'])
            ph['courses'].add(it['course'])
        ordered = []
        for _, code, _ in PHASES:
            if code in phases:
                ph = phases[code]
                ph['instructors'] = sorted(ph['instructors'])
                ph['courses'] = sorted(ph['courses'])
                ordered.append(ph)

        mins = sum(it['minutes'] or 0 for it in items)
        catalog = {
            'subject': sid,
            'subject_ko': data['ko'],
            'source_root': str(SRC / [k for k, v in SUBJECTS.items() if v[0] == sid][0]),
            'total_lectures': len(items),
            'total_minutes': mins,
            'duplicates_excluded': [
                {'path': d['path'], 'course': d['course'], 'no': d['no']} for d in data['dup']
            ],
            'phases': ordered,
            'lectures': items,
        }
        (out_dir / 'catalog.json').write_text(
            json.dumps(catalog, ensure_ascii=False, indent=1), encoding='utf-8')

        total_n += len(items)
        total_min += mins
        breakdown = ', '.join('{} {}'.format(p['label'], p['count']) for p in ordered)
        print('  {:<12} {:>4}강 {:>6.0f}h  ({})'.format(data['ko'], len(items), mins / 60, breakdown))

    print(f"\n합계 {total_n}강 · {total_min / 60:.0f}시간")


if __name__ == '__main__':
    main()
