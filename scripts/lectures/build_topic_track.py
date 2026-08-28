#!/usr/bin/env python3
"""관(leaf)별 논점 트랙 생성 — 전사 + 교재 + 판서 → 강의 진행 순서의 논점 목록.

`generate_notes.py` 가 "교재에 없는 것만" 뽑는 보충이라면, 이쪽은 **강의가 실제로
다룬 것을 빠짐없이** 순서대로 세운다. 개념 완성 화면이 이 목록을 하나씩 소진하고,
다 비우면 그 관의 강의를 끝까지 들은 것과 같다.

출력: viewer/public/data/study/{과목}/lectures/track/{unit}.{phase}.json

사용:
  python3 scripts/lectures/build_topic_track.py economics --phase basic --limit 2
  python3 scripts/lectures/build_topic_track.py economics --phase basic
  python3 scripts/lectures/build_topic_track.py economics --phase basic --check
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import REPO, STUDY, WORK, SRC_ROOT  # noqa: E402
from build_note_bundle import build  # noqa: E402
from map_notes_to_leaves import extract_note_pages  # noqa: E402
from generate_notes import (SUBJECT_RULES, call_gemini, load_leaf_sections,  # noqa: E402
                            MODEL, MAX_FRAMES)
from track_core import (make_point_id, order_spans, chunk_lectures,  # noqa: E402
                        parse_points, check_track, diff_ids)

MAX_CHUNK_CHARS = 45000   # 한 번의 호출에 넣을 전사 글자수 상한

# 강사 필기노트 PDF — 드라이브 이름을 박지 않는다. _paths.SRC_ROOT 가 마운트된 볼륨을 찾아 준다.
# (build_note_bundle.DEFAULT_PDF 에는 옛 드라이브 이름(WD_Black)이 박혀 있어 쓰지 않는다.)
NOTE_PDF = {
    'economics': ('1차_경제학/손병익/[2026_기본이론] 경제학원론 (25년 7-8월:손병익)/'
                  '강의자료/경제학+필기+노트/경제학 필기 노트_10판.pdf'),
}

STYLE = """당신은 감정평가사 1차 수험 교재를 쓰는 사람입니다.
강의(음성 전사 + 판서 사진)를 읽고, 그 강의가 **실제로 다룬 논점**을
**강의가 진행된 순서 그대로** 나열합니다.

[가장 중요 — 빠뜨리지 말 것]
- 이 목록을 다 읽은 사람은 강의를 듣지 않아도 됩니다. 강의에서 다룬 내용이
  목록에 없으면 그 사람은 그걸 영영 모릅니다.
- 반대로 강의에 없던 내용을 지어내 채우지 마세요. 교재에서 끌어와 부풀리는 것도 금지입니다.
- 잡담·다음 강의 예고·수강 안내·시스템 공지는 논점이 아닙니다. 버리세요.
- 지금 쓰는 것은 **이 관 하나**입니다. 전사에 다른 관 이야기가 섞여 있어도 걸러내세요.

[문체 — 교재와 구분이 안 되게]
- **"강사", "강의", "선생님" 이라는 단어를 아예 쓰지 마세요.** "강사가 제시한",
  "강의에서 강조한" 같은 표현도 금지입니다. 출처를 밝히지 말고 교재처럼 단정 서술하세요.
- 큰따옴표로 말을 옮기지 마세요. 내용만 일반 서술로 바꾸세요.
- 전사 오류·음성 인식 같은 제작 뒷얘기는 절대 쓰지 마세요.
- 문장은 '~이다/~한다' 체.

[없는 결론을 채우지 말 것 — 가장 중요한 규칙]
- 전사가 어떤 결론(숫자·등식·"~이다")에 **도달하기 전에 끊기면, 그 직전까지만
  논점으로 만들고 결론을 임의로 채우지 마세요.**
- 교과서적으로 맞는 값이라도, 전사가 말하지 않았으면 쓰지 않습니다. 이 목록을 읽는
  사람은 그것을 강의 내용으로 오인하고 그대로 외웁니다. 틀린 채움보다 없는 편이 낫습니다.
- 결론이 없으면 body에 그 사실을 적으세요 — 예: "이 관에서는 도출 과정까지 다루고,
  최종 값은 이어지는 구간에서 정리된다."
- **body에 쓰는 모든 수치·예시는 전사 원문에 실제로 나온 것만** 씁니다. 설명을
  매끄럽게 하려고 새 예시 숫자를 지어내지 마세요.
- 대칭 구조(정책 A vs 정책 B, 학파 X vs 학파 Y, 단기 vs 장기처럼 전사가 둘 이상을
  나란히 놓고 견주는 대목)는 **축마다 최소 하나씩 독립 논점을 배정**하세요. 한쪽만
  논점으로 세우고 다른 쪽을 다른 논점 본문에 묻으면, 그 축을 묻는 문제 앞에서
  목록이 빈 것처럼 보입니다.
- 교재 본문은 이 관의 범위를 알기 위한 참고일 뿐입니다. 교재에 있고 전사에 없는
  내용을 논점으로 세우지 마세요. 이 목록은 "이 강의가 다룬 것"의 목록이지
  "이 관에서 알아야 할 것"의 목록이 아닙니다.

[각 논점에 담을 것]
- title: 논점 이름. 명사구가 아니라 **무엇을 알게 되는지**가 드러나게. 25자 이내.
- gist: 한 줄 요약. 목록에서 이것만 보고도 무슨 얘긴지 알게. 60자 이내.
- body: 본문 400~800자. 설명의 순서와 이유, 비유·예시, 무엇을 외우고 무엇은 넘길지,
  판서에만 있는 수식·도식까지. 수식은 KaTeX 인라인 `$...$`.
  둘 이상을 견주는 대목은 마크다운 표로 쓰세요(비교축 3개 이상).
- check: 이 논점을 이해했는지 확인하는 질문 하나와, 정답 + 왜 그런지.
- viz: 그림이 이해를 돕는 논점에만. 아래 [VIZ_CATALOG] 의 템플릿 중에서 고르세요.
  카탈로그에 없으면 viz 를 null 로 두세요. 억지로 붙이지 마세요.
- src: 이 논점의 근거가 된 대목. [12강 23:10] 표기에서 읽어 {"lec":12,"t":1390} 형태로.
  t 는 초 단위 정수입니다.

[viz.steps — 상태가 변하는 논점이면 반드시 쓸 것]
그 논점이 **변화 과정**을 설명한다면 (곡선이 이동해 균형이 옮겨가는 과정, 단기→장기
조정, 정책 시행 전/직후/최종 효과, 그래프 위에 순차로 더해지는 요소 등) viz.steps 를
채우세요. 이런 논점에 steps 없이 그림 한 장만 주는 것은 **잘못**입니다 — 경제학에서
이건 예외가 아니라 대부분입니다.
- steps 는 2~4단계.
- 각 step 은 {"label": "...", ...그 단계에서 달라지는 파라미터만} — 전체 params 를
  다시 쓰지 않습니다. 앱이 이전 단계 params 위에 얹어 적용합니다.
- 정적인 그림 하나로 충분한 논점(분류표, 관계도 등 변화가 없는 것)에는 steps 를
  쓰지 마세요.

supply-demand 예시 — "소득 증가로 수요가 늘어 균형이 이동하는 과정":
{"template":"supply-demand",
 "params":{"scenario":"소득 증가 → 수요 우측 이동", "shifts":[],
           "narration":"최초 균형에서 시작한다."},
 "steps":[
   {"label":"최초 균형", "shifts":[]},
   {"label":"수요 우측 이동", "shifts":[{"curve":"D","direction":"right","magnitude":"moderate","reason":"소득 증가"}]},
   {"label":"새 균형 형성", "shifts":[{"curve":"D","direction":"right","magnitude":"moderate","reason":"소득 증가"}],
    "annotations":{"price_change":{"show_arrow":true},"quantity_change":{"show_arrow":true}}}
 ]}

[출력 형식 — JSON 배열만]
설명·인사말·코드펜스 없이 JSON 배열 하나만 출력하세요.
[
  {"title":"…","gist":"…","body":"…",
   "viz":{"template":"supply-demand","params":{…},"steps":[{"label":"…", …}]},
   "check":{"q":"…","a":"…"},
   "src":[{"lec":12,"t":1390}]}
]"""


def load_viz_catalog(subject):
    """vizRegistry 가 앱에 주입하는 카탈로그와 같은 내용을 파이썬에서 읽는다.

    레지스트리는 JS 라 여기서 실행할 수 없다. exampleParams 를 그대로 뽑아 쓰는 대신,
    템플릿 이름과 helpText 만 정규식으로 긁어 온다. 파라미터 정확도는 --check 와
    앱의 VizRouter 검증이 잡는다.

    subjects 필드로 이 과목에 쓰는 템플릿만 남긴다(vizRegistry.buildCatalog 와 동일한
    필터). subjects 를 못 읽은 템플릿은 걸러내지 않고 포함한다 — 조용한 유실 방지.
    """
    src = (REPO / 'viewer/src/viz/vizRegistry.js').read_text(encoding='utf-8')
    names = re.findall(r"from './templates/(\w+)'", src)
    lines = []
    for n in names:
        f = REPO / 'viewer/src/viz/templates' / (n + '.jsx')
        if not f.exists():
            continue
        t = f.read_text(encoding='utf-8')
        nm = re.search(r"name:\s*'([^']+)'", t)
        ht = re.search(r"helpText:\s*'([^']*)'", t)
        ex = re.search(r'exampleParams:\s*(\{.*?\n  \},)', t, flags=re.S)
        subj = re.search(r"subjects:\s*\[([^\]]*)\]", t)
        if not nm:
            continue
        if subj:
            subj_list = [s.strip().strip("'\"") for s in subj.group(1).split(',') if s.strip()]
            if subject not in subj_list:
                continue
        lines.append('### %s — %s\n```json\n%s\n```'
                     % (nm.group(1), ht.group(1) if ht else '',
                        (ex.group(1).rstrip(',') if ex else '{}')))
    print('  viz 카탈로그: %s 과목 템플릿 %d개' % (subject, len(lines)))
    return ('## [VIZ_CATALOG] 쓸 수 있는 시각자료 템플릿\n\n'
            '아래에 없는 도식은 만들지 말고 viz 를 null 로 두세요.\n\n'
            + '\n\n'.join(lines))


def template_names():
    src = (REPO / 'viewer/src/viz/vizRegistry.js').read_text(encoding='utf-8')
    out = set()
    for n in re.findall(r"from './templates/(\w+)'", src):
        f = REPO / 'viewer/src/viz/templates' / (n + '.jsx')
        if f.exists():
            m = re.search(r"name:\s*'([^']+)'", f.read_text(encoding='utf-8'))
            if m:
                out.add(m.group(1))
    return out


def lecture_meta(align):
    return {lid: {'no': v.get('no'), 'course': v.get('course') or v.get('phase') or ''}
            for lid, v in align.get('by_lecture', {}).items()}


def gen_leaf(key, sec, bundle, catalog, subject):
    """관 하나의 논점 목록을 만든다. 긴 관은 나눠 호출해 이어 붙인다."""
    points = []
    chunks = chunk_lectures(bundle['lectures'], MAX_CHUNK_CHARS)
    for i, blocks in enumerate(chunks, 1):
        transcript = '\n\n'.join('[%s강 %s]\n%s' % (b['no'], b['ts'], b['transcript'])
                                 for b in blocks)
        frames = [f['file'] for b in blocks for f in b['frames']][:MAX_FRAMES]
        cont = ('\n\n[이어서]\n앞 구간에서 이미 세운 논점입니다. 겹치지 말고 이어서 쓰세요.\n'
                + '\n'.join('- ' + p['title'] for p in points)) if points else ''
        note_block = ('[강사 필기노트 — 강의 중 화면에 띄운 문서]\n%s\n\n' % bundle['note_text'][:8000]
                      if bundle.get('note_text', '').strip() else '')
        # 밀도 지시 — 이 구간 분량에서 나와야 할 논점 개수를 프롬프트에 직접 숫자로 박는다.
        # 목표: 강의 3~4분당 논점 1개. 상한 15개는 call_gemini 의 maxOutputTokens(8000,
        # 수정 금지 파일)를 응답이 넘지 않게 하려는 안전판이지 할당량이 아니다.
        chunk_minutes = round(sum(b.get('minutes', 0) for b in blocks), 1)
        density_lo = min(15, max(3, int(chunk_minutes // 4)))
        density_hi = min(15, max(density_lo, int(-(-chunk_minutes // 3))))  # ceil(minutes/3)
        density_note = (
            '\n[분량과 논점 개수]\n'
            '이 구간은 %s분입니다. 논점 하나가 강의 3~4분치를 덮는 밀도를 목표로 하면\n'
            '이 구간에서는 논점 %d~%d개가 나와야 합니다(상한 15개).\n'
            '이 목록만 읽고 강의를 대체할 사람이 있으므로, 한 논점이 강의 10분치를\n'
            '뭉뚱그리면 그 사람은 그 10분의 내용을 모릅니다.\n'
            '다만 이 개수는 목표이지 할당량이 아닙니다 — 강의가 실제로 짧게 다룬 내용을\n'
            '억지로 쪼개거나 없는 내용을 지어내 채우지 마세요. 강의가 정말 그만큼 다뤘을 때만\n'
            '그만큼 쓰세요.\n' % (chunk_minutes, density_lo, density_hi)
        )
        prompt = (
            '%s\n%s\n\n%s\n\n'
            '[관] %s\n\n'
            '[교재 본문 — 이 관의 범위를 알기 위한 참고. 여기 있는 내용을 그대로 옮기지 말고,\n'
            ' 강의가 실제로 다룬 것만 쓰세요.]\n%s\n\n'
            '%s%s'
            '[강의 전사 (%d/%d)]\n%s%s\n\n'
            '첨부한 이미지는 그 구간의 판서 화면입니다. 수식·도식이 텍스트에 없으면 여기서 읽어 반영하세요.'
            % (STYLE, SUBJECT_RULES.get(subject, ''), catalog,
               ' / '.join(sec['path']), sec['body'][:12000], note_block, density_note,
               i, len(chunks), transcript, cont)
        )
        raw, usage = call_gemini(key_holder['key'], prompt, frames)
        got = parse_points(raw)
        if not got and raw:
            print('  ⚠ %s: 논점 파싱 실패 (%d/%d) — 응답 끝 100자: %r'
                  % (key, i, len(chunks), raw[-100:]))
        points.extend(got)
        usage_holder['in'] += usage.get('promptTokenCount', 0)
        usage_holder['out'] += usage.get('candidatesTokenCount', 0)
    return points


key_holder = {'key': None}
usage_holder = {'in': 0, 'out': 0}


def track_path(base, unit, phase):
    return base / 'track' / ('%s.%s.json' % (unit, phase))


def leaf_already_built(base, unit, phase, lid, cache):
    """이 관의 논점이 트랙 파일에 이미 있는지. 파일 하나를 유닛당 한 번만 읽는다."""
    if unit not in cache:
        p = track_path(base, unit, phase)
        cache[unit] = json.loads(p.read_text(encoding='utf-8')) if p.exists() else None
    track = cache[unit]
    return any(lf.get('leaf_id') == lid and lf.get('points')
               for lf in (track or {}).get('leaves') or [])


def save_leaf(base, subject, phase, unit, lid, title, pts):
    """관 하나의 논점을 트랙 파일에 즉시 병합해 저장한다.

    루프가 도중에 죽어도 이미 만든 관은 남는다. 기존 관 순서를 지키고 이번에
    만든 관만 갈아끼운다 — 통째로 다시 쓰면 이번에 안 돌린 관이 사라진다
    (generate_notes 와 같은 규칙).
    """
    out_dir = base / 'track'
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = track_path(base, unit, phase)
    old = json.loads(dst.read_text(encoding='utf-8')) if dst.exists() else None
    leaves = list((old or {}).get('leaves') or [])
    index = {lf.get('leaf_id'): i for i, lf in enumerate(leaves)}
    li = index.get(lid, len(leaves))
    for seq, p in enumerate(pts, 1):
        p['seq'] = seq
        p['id'] = make_point_id(unit, li, seq)
        p.setdefault('viz', None)
        p.setdefault('check', None)
        p.setdefault('src', [])
    entry = {'leaf_id': lid, 'title': title, 'points': pts}
    if lid in index:
        leaves[index[lid]] = entry
    else:
        leaves.append(entry)
        index[lid] = len(leaves) - 1
    track = {'subject': subject, 'phase': phase, 'unit_code': unit,
             'leaves': leaves, 'orphans': (old or {}).get('orphans') or []}
    if old:
        d = diff_ids(old, track)
        if d['removed']:
            print('  ⚠ %s: 사라진 논점 id %d개 — 진도 확인 필요' % (unit, len(d['removed'])))
    dst.write_text(json.dumps(track, ensure_ascii=False, indent=1), encoding='utf-8')


# 관 축에 안 맞는 강의 — 제목에 면수가 없어 붙을 관이 없는 것들.
# 버리면 "전부 파악"이 아니게 되므로 과목 레벨 트랙(_subject)으로 담는다.
EXTRA_GROUPS = {
    'economics': [
        {'kind': 'prereq', 'title': '경제 기초수학',
         'lectures': ['economics-basic-004', 'economics-basic-005']},
        {'kind': 'review', 'title': '미시경제학 총정리',
         'lectures': ['economics-basic-035']},
        {'kind': 'review', 'title': '거시경제학 총정리',
         'lectures': ['economics-basic-051']},
    ],
}


def extra_group_built(base, phase, title):
    """이 그룹이 _subject 트랙 파일에 이미 논점과 함께 들어있는지. title 로 식별한다
    (leaf_id 가 전부 None 이라 leaf_id 로는 그룹을 구분할 수 없다)."""
    p = track_path(base, '_subject', phase)
    if not p.exists():
        return False
    track = json.loads(p.read_text(encoding='utf-8'))
    return any(lf.get('title') == title and lf.get('points') for lf in track.get('leaves') or [])


def save_extra_group(base, subject, phase, gi, kind, title, pts):
    """그룹 하나의 논점을 _subject 트랙 파일에 즉시 병합해 저장한다.

    save_leaf 와 같은 이유로 즉시 저장한다 — 도중에 죽어도 이미 만든 그룹은 남는다.
    leaf_id 가 전부 None 이라 save_leaf 의 leaf_id 색인을 그대로 못 쓰므로 title 로 색인한다.
    """
    dst = track_path(base, '_subject', phase)
    old = json.loads(dst.read_text(encoding='utf-8')) if dst.exists() else None
    leaves = list((old or {}).get('leaves') or [])
    index = {lf.get('title'): i for i, lf in enumerate(leaves)}
    for seq, p in enumerate(pts, 1):
        p['seq'] = seq
        p['id'] = make_point_id('_subject', gi, seq)
        p.setdefault('viz', None)
        p.setdefault('check', None)
        p.setdefault('src', [])
    entry = {'leaf_id': None, 'kind': kind, 'title': title, 'points': pts}
    if title in index:
        leaves[index[title]] = entry
    else:
        leaves.append(entry)
    track = {'subject': subject, 'phase': phase, 'unit_code': '_subject',
             'leaves': leaves, 'orphans': (old or {}).get('orphans') or []}
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(track, ensure_ascii=False, indent=1), encoding='utf-8')


# 관 빌드의 정상 경로는 align.json 의 span 이 강의를 몇 분 단위로 잘라 주므로 블록이
# 자연히 여러 개다. 과목 레벨 트랙은 span 이 없어 강의 전체가 블록 하나가 되기 쉽고,
# 긴 강의(50분 이상) 하나를 통째로 넣으면 밀도 지시(분당 논점 목표)가 커져 Gemini
# 응답이 maxOutputTokens 를 넘어 파싱이 깨진다 — 미시경제학 총정리(58분)에서 실측.
# 시간 창으로 블록을 잘게 쪼개고, 이 호출에서만 청크 글자수 상한도 낮춰
# 자연히 여러 번 나눠 부르게 한다.
EXTRA_WINDOW_SEC = 600     # 블록 하나당 시간 창(10분)
EXTRA_MAX_CHUNK_CHARS = 12000


def windowed_blocks(tr, no, window_sec=EXTRA_WINDOW_SEC):
    segs = tr.get('segments') or []
    blocks, i = [], 0
    while i < len(segs):
        t0 = segs[i]['start']
        cur, j = [], i
        while j < len(segs) and segs[j]['start'] < t0 + window_sec:
            cur.append(segs[j])
            j += 1
        t1 = cur[-1]['end'] if cur else t0
        blocks.append({
            'no': no,
            'ts': '%d:%02d~%d:%02d' % (int(t0) // 60, int(t0) % 60, int(t1) // 60, int(t1) % 60),
            'minutes': round((t1 - t0) / 60, 1),
            'transcript': ' '.join(s['text'] for s in cur),
            'frames': [],
        })
        i = j
    return blocks


def build_extra(args, base, tdir, catalog):
    groups = EXTRA_GROUPS.get(args.subject)
    if not groups:
        sys.exit('%s 는 과목 레벨 트랙 정의가 없습니다.' % args.subject)
    global MAX_CHUNK_CHARS
    for gi, g in enumerate(groups):
        if not args.force and extra_group_built(base, args.phase, g['title']):
            print('  건너뜀(이미 생성됨) %s' % g['title'])
            continue
        blocks = []
        for lid in g['lectures']:
            f = tdir / ('%s.json' % lid)
            if not f.exists():
                print('  ⚠ 전사 없음: %s' % lid)
                continue
            tr = json.loads(f.read_text(encoding='utf-8'))
            no = tr.get('no')
            if no is None:
                no = int(re.search(r'(\d+)$', lid).group(1))
            blocks.extend(windowed_blocks(tr, no))
        if not blocks:
            print('  ⚠ %s: 전사가 하나도 없어 건너뜀' % g['title'])
            continue
        sec = {'path': [g['title']], 'body': '', 'heads': [], 'unit_code': '_subject'}
        orig_max = MAX_CHUNK_CHARS
        MAX_CHUNK_CHARS = EXTRA_MAX_CHUNK_CHARS
        try:
            pts = gen_leaf(g['title'], sec, {'lectures': blocks}, catalog, args.subject)
        finally:
            MAX_CHUNK_CHARS = orig_max
        if not pts:
            print('  ❌ 논점 0개 %s' % g['title'])
            continue
        save_extra_group(base, args.subject, args.phase, gi, g['kind'], g['title'], pts)
        print('  %-20s 논점 %d개' % (g['title'], len(pts)))
    print('저장: %s' % track_path(base, '_subject', args.phase))


def do_check(subject, phase):
    base = STUDY / subject / 'lectures'
    align = json.loads((base / 'align.json').read_text(encoding='utf-8'))
    names = template_names()
    tdir = base / 'track'
    if not tdir.exists():
        sys.exit('트랙이 아직 없습니다: %s' % tdir)
    total_issues, total_points, total_leaves = 0, 0, 0
    for f in sorted(tdir.glob('*.%s.json' % phase)):
        track = json.loads(f.read_text(encoding='utf-8'))
        issues = check_track(track, align['by_leaf'], names)
        total_issues += len(issues)
        for lf in track.get('leaves', []):
            total_leaves += 1
            total_points += len(lf.get('points') or [])
        for i in issues:
            print('  ⚠ %s' % i)
    print('\n관 %d개 · 논점 %d개 · 문제 %d건' % (total_leaves, total_points, total_issues))
    orphan_secs = 0
    for f in sorted(tdir.glob('*.%s.json' % phase)):
        track = json.loads(f.read_text(encoding='utf-8'))
        orphan_secs += sum(o.get('sec', 0) for o in track.get('orphans') or [])
    if orphan_secs:
        print('관에 안 붙은 구간 합계 %.1f분' % (orphan_secs / 60))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--phase', default='basic')
    ap.add_argument('--limit', type=int)
    ap.add_argument('--only', help='특정 leaf_id 하나만')
    ap.add_argument('--check', action='store_true', help='생성하지 않고 검증만')
    ap.add_argument('--force', action='store_true', help='이미 만든 관도 다시 생성')
    ap.add_argument('--extra', action='store_true',
                    help='관에 안 붙은 강의를 과목 레벨 트랙(_subject)으로 생성')
    ap.add_argument('--model', default=MODEL)
    args = ap.parse_args()

    if args.check:
        do_check(args.subject, args.phase)
        return

    import generate_notes
    generate_notes.MODEL = args.model

    env = {}
    for line in (REPO / '.env').read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    key_holder['key'] = env.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    if not key_holder['key']:
        sys.exit('GEMINI_API_KEY 없음')

    base = STUDY / args.subject / 'lectures'
    align = json.loads((base / 'align.json').read_text(encoding='utf-8'))
    nm_path = base / 'note_map.json'
    note_map = (json.loads(nm_path.read_text(encoding='utf-8'))
                if nm_path.exists() else {'pages': [], 'by_leaf': {}})
    rel = NOTE_PDF.get(args.subject)
    pdf = str(SRC_ROOT / rel) if rel else None
    # 상대경로를 SRC_ROOT(마운트된 볼륨)에서 조립한다. 과목에 항목이 없거나 파일이
    # 실제로 없으면 pages_text 를 빈 dict 로 둔 채 넘어간다(전사·판서만으로 진행).
    pages_text = ({p['page']: p['text'] for p in extract_note_pages(pdf)}
                  if pdf and Path(pdf).exists() else {})
    sections = load_leaf_sections(args.subject)
    tdir, kdir = WORK / 'transcripts' / args.subject, WORK / 'keyframes' / args.subject
    catalog = load_viz_catalog(args.subject)
    meta = lecture_meta(align)

    if args.extra:
        build_extra(args, base, tdir, catalog)
        return

    targets = [lid for lid in align['by_leaf'] if lid in sections]
    if args.only:
        targets = [t for t in targets if t == args.only]

    track_cache = {}
    skipped = 0
    if not args.force:
        kept = []
        for lid in targets:
            unit = sections[lid]['unit_code']
            if leaf_already_built(base, unit, args.phase, lid, track_cache):
                title = sections[lid]['path'][-1] if sections[lid]['path'] else lid
                print('  건너뜀(이미 생성됨) %s' % title)
                skipped += 1
            else:
                kept.append(lid)
        targets = kept

    if args.limit:
        targets = targets[:args.limit]
    print('대상 관 %d개(건너뜀 %d개) · 모델 %s\n' % (len(targets), skipped, args.model))

    units_touched = set()
    t0 = time.time()
    for n, lid in enumerate(targets, 1):
        sec = sections[lid]
        title = sec['path'][-1] if sec['path'] else lid
        bundle = build(args.subject, lid, pages_text, note_map, align, tdir, kdir)
        # build() 가 내부에서 merge_spans() 로 (lecture_id, start) 재정렬을 해서
        # 강좌별 순서가 무너진다. 여기서 bundle['lectures'] 를 다시 강좌 기준으로
        # 정렬한다 — order_spans 는 'lecture_id'/'start' 키만 읽으므로 그대로 쓸 수 있다.
        # sorted 는 안정 정렬이라 같은 강좌 안의 원래(시간) 순서는 유지된다.
        bundle['lectures'] = order_spans(bundle['lectures'], meta)
        if not bundle['lectures']:
            print('  [%d/%d] 건너뜀(강의 구간 없음) %s' % (n, len(targets), title))
            continue
        try:
            pts = gen_leaf(lid, sec, bundle, catalog, args.subject)
        except Exception as e:
            print('  [%d/%d] ❌ 실패 %s' % (n, len(targets), e))
            continue
        if not pts:
            print('  [%d/%d] ❌ 논점 0개 %s' % (n, len(targets), title))
            continue
        save_leaf(base, args.subject, args.phase, sec['unit_code'], lid, title, pts)
        units_touched.add(sec['unit_code'])
        print('  [%d/%d] %-34s 논점 %d개 · %d분' % (n, len(targets), title[:34],
                                                  len(pts), bundle['total_minutes']))

    print('\n유닛 %d개 저장 · 건너뜀 %d개 · %.1f분' % (len(units_touched), skipped,
                                              (time.time() - t0) / 60))
    print('토큰 in %s / out %s' % ('{:,}'.format(usage_holder['in']),
                                  '{:,}'.format(usage_holder['out'])))


if __name__ == '__main__':
    main()
