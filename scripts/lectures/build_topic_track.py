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
from build_note_bundle import merge_spans  # noqa: E402
from map_notes_to_leaves import extract_note_pages  # noqa: E402
from generate_notes import (SUBJECT_RULES, call_gemini, load_leaf_sections,  # noqa: E402
                            MODEL, MAX_FRAMES)
from track_core import (make_point_id, order_spans, chunk_lectures,  # noqa: E402
                        parse_points, parse_meta, parses_as_json, check_track, diff_ids)

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
- 지금 쓰는 것은 **이 관 하나**입니다. 전사에는 같은 절에 속한 다른 관 이야기도
  섞여 있습니다 — [교재 본문] 슬라이스가 **이 관의 범위**입니다. 그 범위에
  해당하는 이야기만 골라 논점으로 쓰고, 나머지는 걸러내세요.
- **자체 점검 — 출력하기 전에 반드시 거치세요.** [교재 본문]은 `####` 로 시작하는
  소제목들로 나뉘어 있습니다. 지금 쓰려는 논점이 그 소제목 중 **어느 것**에
  해당하는지 하나씩 짚어 보세요. 대응하는 소제목이 없다면, 그건 이 관 얘기가
  아니라 배경 설명(희소성·경제주체 목적 같은 총론)이거나 형제 관 얘기입니다 —
  **이미 다른 논점(또는 형제 관)이 다룬 배경 설명을 재탕하는 것은 이 관의
  논점이 아닙니다.**
- 이 소제목들 중 **전사에서 실제로 다뤄진 것이 하나도 없다면**, 배경 설명만으로
  분량을 채우지 말고 `"covered": false` 로 판정하세요. 강의가 다루지 않은
  것을 다룬 것처럼 만드는 것은, 아무것도 만들지 않는 것보다 나쁩니다.
- **[관] 이름에 "A와 B"·"A·B" 처럼 핵심어가 여럿 나열돼 있으면, 그 핵심어 각각이
  전사에서 실제로 설명됐는지 따로 확인하세요.** 예를 들어 관 이름이
  "경제문제와 경제체제"인데 전사가 "경제문제"만 다루고 "경제체제"(자본주의·
  계획경제·가격기구 등)는 전혀 언급하지 않는다면, "경제문제" 쪽 배경 설명
  몇 개로 분량을 채우지 말고 **관 전체를 `"covered": false` 로 판정**하세요.
  핵심어 하나를 통째로 빼먹은 채 나머지 핵심어의 배경 설명만으로 대신 채우는
  것은 허용되지 않습니다.

[문체]
- **"강사", "강의", "선생님" 이라는 단어를 아예 쓰지 마세요.** "강사가 제시한",
  "강의에서 강조한" 같은 표현도 금지입니다. 캐릭터 「선생」이 설명하는 것이지
  누군가를 인용하는 게 아닙니다.
- 전사 오류·음성 인식 같은 제작 뒷얘기는 절대 쓰지 마세요.

[없는 결론을 채우지 말 것 — 가장 중요한 규칙]
- 전사가 어떤 결론(숫자·등식·"~이다")에 **도달하기 전에 끊기면, 그 직전까지만
  논점으로 만들고 결론을 임의로 채우지 마세요.**
- 교과서적으로 맞는 값이라도, 전사가 말하지 않았으면 쓰지 않습니다. 대화를 읽는
  사람은 그것을 강의 내용으로 오인하고 그대로 외웁니다. 틀린 채움보다 없는 편이 낫습니다.
- 결론이 없으면 그 사실을 대사로 적으세요 — 예: "여기까지는 도출 과정이고,
  최종 값은 뒤에서 정리돼요."
- **turns 안 모든 수치·예시는 전사 원문에 실제로 나온 것만** 씁니다. 설명을
  매끄럽게 하려고 새 예시 숫자를 지어내지 마세요.
- 대칭 구조(정책 A vs 정책 B, 학파 X vs 학파 Y, 단기 vs 장기처럼 전사가 둘 이상을
  나란히 놓고 견주는 대목)는 **축마다 최소 하나씩 독립 논점을 배정**하세요. 한쪽만
  논점으로 세우고 다른 쪽을 다른 논점 안에 묻으면, 그 축을 묻는 문제 앞에서
  목록이 빈 것처럼 보입니다.
- 교재 본문은 이 관의 범위를 알기 위한 기준입니다. 교재에 있고 전사에 없는
  내용을 논점으로 세우지 마세요. 이 목록은 "이 강의가 다룬 것"의 목록이지
  "이 관에서 알아야 할 것"의 목록이 아닙니다.

[각 논점에 담을 것]
- title: 논점 이름. 명사구가 아니라 **무엇을 알게 되는지**가 드러나게. 25자 이내.
- gist: 한 줄 요약. 목록에서 이것만 보고도 무슨 얘긴지 알게. 60자 이내.
- turns: 아래 [출력 — 각 논점은 대화다] 를 따르세요.
- example: 계산·판단이 있는 논점에만. 없으면 생략하세요.
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

[출력 — 각 논점은 대화다]
논점 하나를 캐릭터 넷이 주고받는 대화(turns)로 씁니다. turns 는 6~12개.

캐릭터:
- "ask"    묻는 이 — 학습자 대신 묻는다. 짧고 솔직하게. "이거 왜 배워요?" "아까 그거랑 뭐가 달라요?"
- "teach"  선생 — 설명한다. **일상 언어로 먼저 풀고, 비유를 든 다음, 그제서야 교재 표현**을 말한다.
- "gotcha" 깐깐이 — 찌른다. 반례·경계조건·시험 함정. "그럼 이 경우엔요?"
- "mate"   복습 메이트 — 무엇을 외우고 무엇은 넘길지. **내용 설명은 하지 않는다. 학습 조언만.**

[반드시 지킬 것]
- **turns 에 "quiz" 턴이 최소 하나 있어야 합니다.** 없으면 학습자가 그냥 넘겨 버립니다.
- quiz 는 정답 1개, 오답 2~3개입니다.
- **오답은 그럴듯해야 합니다.** 실제로 헷갈리는 것 — 반대 개념(수요 vs 공급), 조건 하나만
  바꾼 것, 방향만 뒤집은 것. 전사에서 함정이라고 경고한 대목이 있으면 그걸 오답으로 쓰세요.
- **오답마다 그 오답 전용 reply 를 씁니다.** "틀렸습니다" 로 시작하지 마세요.
  왜 그렇게 생각했는지 짚고 바로잡으세요. 예: "그건 사는 쪽 얘기예요. 파는 사람
  입장에서 생각해봐요 — 값이 비싸지면 더 팔고 싶겠죠?"
- 정답 choice 에도 reply 를 씁니다(짧게 확인해 주는 말).
- "강사", "강의", "선생님" 이라는 **단어**는 여전히 쓰지 마세요. 캐릭터 「선생」이 말하는
  것이지 누군가를 인용하는 게 아닙니다.
- 과장된 감탄사나 이모티콘을 남발하지 마세요. 친근하되 유치하지 않게.

[출력 형식 — JSON 객체 하나만]
설명·인사말·코드펜스 없이 아래 형태의 JSON 객체 하나만 출력하세요.
**"자체 점검"에서 이 관 고유 소제목이 전사에 하나도 없다고 판단되면 covered
를 false 로, points 를 빈 배열로 두세요.** reason 에는 그렇게 판단한 근거를
한 줄로 적으세요(예: "전사에 경제체제·자본주의·계획경제 언급 없음").
{
 "covered": true,
 "reason": "이 관의 소제목 중 몇 개가 전사에서 실제로 다뤄졌는지 한 줄로",
 "points": [
  {"title":"…","gist":"…",
   "turns":[
     {"who":"ask","text":"…"},
     {"who":"teach","text":"…","viz":{"template":"supply-demand","params":{},"steps":[]}},
     {"who":"quiz","prompt":"…","choices":[
        {"text":"…","ok":true,"reply":"…"},
        {"text":"…","ok":false,"who":"gotcha","reply":"…"}
     ]},
     {"who":"gotcha","text":"…"},
     {"who":"mate","text":"…"}
   ],
   "example":{"q":"…","solution":"…"},
   "check":{"q":"…","a":"…"},
   "src":[{"lec":12,"t":1390}]}
 ]
}
example 은 계산·판단이 있는 논점에만 넣고, 없으면 생략하세요."""


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


def section_key(sec):
    """관을 절 단위로 묶는 키. path 의 앞 3개(과목/장/절)가 같으면 같은 절이다."""
    return tuple((sec.get('path') or [])[:3])


def _leaf_lecture_blocks(leaf_id, align, transcripts_dir, keyframes_dir):
    """이 leaf_id 하나의 강의 구간 블록. build_note_bundle.build 의 조립 로직과
    같지만, 그 함수는 leaf 하나만 받게 돼 있어(수정 금지 파일) 절 단위로 여러
    leaf 를 합치려면 이 조립부만 별도로 둬야 한다."""
    blocks = []
    for sp in merge_spans(align['by_leaf'].get(leaf_id, [])):
        tf = transcripts_dir / ('%s.json' % sp['lecture_id'])
        if not tf.exists():
            continue
        tr = json.loads(tf.read_text(encoding='utf-8'))
        text = ' '.join(s['text'] for s in tr['segments'] if sp['start'] <= s['start'] < sp['end'])
        kf_idx = keyframes_dir / sp['lecture_id'] / 'index.json'
        frames = []
        if kf_idx.exists():
            ki = json.loads(kf_idx.read_text(encoding='utf-8'))
            frames = [{'ts': f['ts'], 'file': str(keyframes_dir / sp['lecture_id'] / f['file'])}
                      for f in ki['frames'] if sp['start'] <= f['t'] < sp['end']]
        blocks.append({
            'lecture_id': sp['lecture_id'], 'no': sp['no'], 'start': sp['start'],
            'ts': '%d:%02d~%d:%02d' % (int(sp['start']) // 60, int(sp['start']) % 60,
                                       int(sp['end']) // 60, int(sp['end']) % 60),
            'minutes': round((sp['end'] - sp['start']) / 60, 1),
            'note_pages': sp['pages'],
            'transcript': text,
            'frames': frames,
        })
    return blocks


def build_section_bundle(leaf_ids, pages_text, note_map, align, meta, transcripts_dir, keyframes_dir):
    """절 하나에 속한 모든 관의 강의 구간을 모아 시각순으로 정렬한다.

    관 경계로 구간을 재배정하는 시도가 세 번(TF-IDF 두 번, LLM 한 번) 다
    실패해(표본으로 본 절은 고쳐지고 안 본 절은 틀림), 판단 시점을 절 단위
    재료 + 프롬프트의 관 범위 지정으로 옮겼다. 이 함수가 그 재료 조립부다.
    """
    blocks = []
    for lid in leaf_ids:
        blocks.extend(_leaf_lecture_blocks(lid, align, transcripts_dir, keyframes_dir))
    blocks = order_spans(blocks, meta)
    leaf_pages = sorted({p for lid in leaf_ids
                         for p in note_map['by_leaf'].get(lid, {}).get('pages', [])})
    note_text = '\n\n'.join('[필기노트 %s쪽]\n%s' % (p, pages_text.get(p, '')) for p in leaf_pages)
    return {'lectures': blocks, 'note_text': note_text,
            'total_minutes': round(sum(b['minutes'] for b in blocks), 1)}


def prev_bodies_for(base, unit, phase, lid, cache):
    """이 관의 옛 트랙에서 body 텍스트를 모은다. 재생성 시 재료로 재사용한다.

    cache 는 leaf_already_built 와 같은 형태({unit: track_dict|None}) 를 공유한다
    — 유닛 파일 하나를 두 번 읽지 않는다.
    """
    if unit not in cache:
        p = track_path(base, unit, phase)
        cache[unit] = json.loads(p.read_text(encoding='utf-8')) if p.exists() else None
    track = cache[unit]
    for lf in (track or {}).get('leaves') or []:
        if lf.get('leaf_id') != lid:
            continue
        return '\n\n'.join(pt.get('body') for pt in lf.get('points') or [] if pt.get('body'))
    return ''


def gen_leaf(key, sec, bundle, catalog, subject, siblings=None, prev_bodies=''):
    """관 하나의 논점 목록을 만든다. 긴 관은 나눠 호출해 이어 붙인다.

    bundle 은 이 관 하나가 아니라 **이 관이 속한 절 전체**의 강의 구간이다 —
    절 안에서 관별로 구간을 다시 나누는 시도(TF-IDF 두 번, LLM 한 번)가 세 번 다
    실패해(안 본 절에서 오배정), 판단 시점을 "구간을 관에 배정"에서 "절 재료를
    주고 그 관 범위만 쓰게 한다"로 옮겼다. sec['body']가 그 범위 기준이고,
    siblings 는 같은 절의 다른 관 제목 목록 — 프롬프트가 그 내용을 걸러내라고
    지시하는 데 쓴다. prev_bodies 는 이 관의 옛 트랙에서 모은 body 텍스트로,
    재생성 시 검증된 내용을 재료로 재사용한다(처음부터 다시 읽는 것보다 싸다).

    청크 성공/전체는 chunk_holder(전역, usage_holder 와 같은 패턴)에 남긴다 — 이
    함수의 공개 시그니처(반환값 points 리스트)는 바꾸지 않는다. save_leaf 가
    chunk_holder 를 읽어 트랙에 chunks_ok/chunks_total 을 적으면, 청크 일부가
    빈 배열로 실패해도 "성공"으로 저장되던 문제를 --check 가 잡을 수 있다.
    """
    chunk_holder['ok'] = 0
    chunk_holder['total'] = 0
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
        sib_block = ''
        if siblings:
            sib_block = (
                '[같은 절의 다른 관 — 이 내용은 쓰지 마세요]\n'
                '아래는 이 관과 같은 절에 속한 다른 관들입니다. 전사에 이 관들 얘기가\n'
                '섞여 있어도 걸러내세요 — 그 관에서 따로 다룹니다.\n'
                + '\n'.join('- ' + s for s in siblings) + '\n\n'
            )
        prev_block = (('[이 관의 이전 정리 — 내용 근거로만 쓰고 문장을 그대로 옮기지 마세요]\n%s\n\n'
                       % prev_bodies[:6000]) if prev_bodies else '')
        prompt = (
            '%s\n%s\n\n%s\n\n'
            '[관] %s\n\n'
            '[교재 본문 — **이 관의 범위 기준**. 전사에는 절 전체 내용이 섞여 있으니,\n'
            ' 이 슬라이스에 해당하는 이야기만 이 관의 논점으로 쓰세요. 그대로 옮기지\n'
            ' 말고, 강의가 실제로 다룬 것만 쓰세요.]\n%s\n\n'
            '%s%s%s%s'
            '[강의 전사 — 이 관이 속한 절 전체 구간 (%d/%d)]\n%s%s\n\n'
            '첨부한 이미지는 그 구간의 판서 화면입니다. 수식·도식이 텍스트에 없으면 여기서 읽어 반영하세요.'
            % (STYLE, SUBJECT_RULES.get(subject, ''), catalog,
               ' / '.join(sec['path']), sec['body'][:12000],
               sib_block, prev_block, note_block, density_note,
               i, len(chunks), transcript, cont)
        )
        raw, usage = call_gemini(key_holder['key'], prompt, frames)
        got = parse_points(raw)
        covered, reason = parse_meta(raw)
        if covered is False:
            print('  ⚠ %s: 강의에 없다고 판정 (%d/%d) — %s' % (key, i, len(chunks), reason))
        chunk_holder['total'] += 1
        # got 이 비어도 raw 가 문법적으로 유효한 JSON(빈 배열 포함)이면 실패가
        # 아니다 — 이 관의 주제가 그 구간에 없다는 정당한 판정일 수 있다.
        if not got and raw and not parses_as_json(raw):
            print('  ⚠ %s: 논점 파싱 실패 (%d/%d) — 응답 끝 100자: %r'
                  % (key, i, len(chunks), raw[-100:]))
        else:
            chunk_holder['ok'] += 1
        points.extend(got)
        usage_holder['in'] += usage.get('promptTokenCount', 0)
        usage_holder['out'] += usage.get('candidatesTokenCount', 0)
    for p in points:
        p['source'] = 'lecture'
    return points


TEXTBOOK_ONLY_NOTE = """
[중요 — 이 관은 강의 전사에 주제가 없다고 판정됐습니다]
이 관은 강의가 다루지 않아 교재만으로 논점을 만듭니다.
- **강의에서 나온 것처럼 쓰지 마세요.** "전사에서", "이 강의는" 같은 표현을 쓰지
  마세요. turns 의 teach 대사도 교재 설명이지 강의를 옮긴 게 아닙니다.
- src 는 빈 배열 `[]` 로 두세요. 근거로 삼을 강의 시각이 없습니다.
- 그래도 turns·quiz·오답별 전용 반박은 똑같이 요구됩니다.
- **STYLE 의 "자체 점검"·covered 판정은 이 호출에는 해당 없습니다** — 여기엔
  [강의 전사] 자체가 없으니 "전사에 없다"는 이유로 다시 covered:false 를 내면
  안 됩니다. covered 는 true 로 두고, 교재에 있는 내용으로 points 를 채우세요."""


def gen_leaf_textbook(key, sec, catalog, subject, siblings=None):
    """강의 전사에 주제가 없는 관을 위한 2차 호출. 전사를 아예 넣지 않는다 —
    넣으면 gen_leaf 처럼 형제 관 내용을 다시 끌어온다. 반환하는 논점마다
    source='textbook' 을 붙인다(앱은 이 값으로 「교재 기반」 배지를 보여준다,
    viewer/src/ConceptScene.jsx, 수정 금지 파일 — 여기선 값만 채워 넘긴다).
    """
    sib_block = ''
    if siblings:
        sib_block = (
            '[같은 절의 다른 관 — 이 내용은 쓰지 마세요]\n'
            '아래는 이 관과 같은 절에 속한 다른 관들입니다.\n'
            + '\n'.join('- ' + s for s in siblings) + '\n\n'
        )
    prompt = (
        '%s\n%s\n\n%s\n\n'
        '[관] %s\n\n'
        '[교재 본문 — 이 관의 유일한 재료입니다]\n%s\n\n'
        '%s%s'
        % (STYLE, SUBJECT_RULES.get(subject, ''), catalog, ' / '.join(sec['path']),
           sec['body'][:12000], sib_block, TEXTBOOK_ONLY_NOTE)
    )
    raw, usage = call_gemini(key_holder['key'], prompt, [])
    got = parse_points(raw)
    chunk_holder['total'] += 1
    if got or parses_as_json(raw):
        chunk_holder['ok'] += 1
    usage_holder['in'] += usage.get('promptTokenCount', 0)
    usage_holder['out'] += usage.get('candidatesTokenCount', 0)
    for p in got:
        p['source'] = 'textbook'
        p.setdefault('src', [])
    return got


key_holder = {'key': None}
usage_holder = {'in': 0, 'out': 0}
chunk_holder = {'ok': 0, 'total': 0}


def track_path(base, unit, phase):
    return base / 'track' / ('%s.%s.json' % (unit, phase))


def leaf_already_built(base, unit, phase, lid, cache):
    """이 관의 논점이 트랙 파일에 이미 있는지. 파일 하나를 유닛당 한 번만 읽는다.

    청크 중 일부가 실패한 채 저장된 관(chunks_ok < chunks_total)은 "이미 만들어짐"
    으로 치지 않는다 — 그렇지 않으면 강의 3분의 1이 사라진 관이 영구히 다시
    만들어지지 않는다. chunks_ok/chunks_total 이 없는 관(이 필드 이전에 저장된
    기존 관)은 완전한 것으로 간주해 불필요한 재생성을 강제하지 않는다.
    """
    if unit not in cache:
        p = track_path(base, unit, phase)
        cache[unit] = json.loads(p.read_text(encoding='utf-8')) if p.exists() else None
    track = cache[unit]
    for lf in (track or {}).get('leaves') or []:
        if lf.get('leaf_id') != lid or not lf.get('points'):
            continue
        c_ok, c_total = lf.get('chunks_ok'), lf.get('chunks_total')
        if c_ok is not None and c_total is not None and c_ok < c_total:
            return False
        return True
    return False


def save_leaf(base, subject, phase, unit, lid, title, pts, chunks_ok=None, chunks_total=None):
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
    # 같은 자리(id)의 옛 논점에 body 가 있고 새 논점엔 없으면 옮겨 담는다 —
    # turns 프롬프트는 더 이상 body 를 요구하지 않지만, 화면 폴백과 다음
    # 재생성의 재료(prev_bodies_for)로 계속 쓰인다.
    old_body_by_id = {}
    if lid in index:
        old_body_by_id = {op.get('id'): op.get('body')
                          for op in leaves[index[lid]].get('points') or [] if op.get('body')}
    for seq, p in enumerate(pts, 1):
        p['seq'] = seq
        p['id'] = make_point_id(unit, li, seq)
        if not p.get('body') and old_body_by_id.get(p['id']):
            p['body'] = old_body_by_id[p['id']]
        p.setdefault('viz', None)
        p.setdefault('check', None)
        p.setdefault('src', [])
    entry = {'leaf_id': lid, 'title': title, 'points': pts,
             'chunks_ok': chunks_ok, 'chunks_total': chunks_total}
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


ORPHAN_MIN_GAP_SEC = 2.0   # 라운딩 오차(관측상 <2초)를 구멍으로 오인하지 않는 하한


def _orphan_gist(transcripts_dir, lecture_id, t0, t1):
    """구멍 구간과 겹치는 첫 전사 문장을 잘라 온다. API 를 새로 쓰지 않는다.

    전사 파일이 없으면(외장 드라이브 미마운트 등) 빈 문자열 — 조용히 생략한다.
    """
    f = transcripts_dir / ('%s.json' % lecture_id)
    if not f.exists():
        return ''
    try:
        tr = json.loads(f.read_text(encoding='utf-8'))
    except (ValueError, OSError):
        return ''
    for s in tr.get('segments') or []:
        if s.get('start', 0) < t1 and s.get('end', 0) > t0:
            return (s.get('text') or '')[:80]
    return ''


def compute_orphans(subject, align, sections, transcripts_dir):
    """정렬(align)이 강의 시간 중 어느 관에도 못 붙인 구간을 모은다 (스펙 §5-3).

    두 갈래를 합친다:
      1. by_lecture 의 span 사이·앞·뒤에 남는 시간 간극 — 정렬 알고리즘이 그
         구간을 아예 창(window)으로 만들지 못했거나 건너뛴 경우.
      2. 이 과목 taxonomy 전체(sections)에는 있지만 align['by_leaf']에 스팬이
         하나도 없는 관 — 정렬이 그 관의 실제 시간을 통째로 다른 관에 잘못
         붙였을 때 이 형태로 드러난다. lec/sec 정보가 없으므로 0으로 둔다.
    """
    orphans = []
    for lid, meta in (align.get('by_lecture') or {}).items():
        spans = meta.get('spans') or []
        no = meta.get('no')
        if not spans:
            continue
        gaps = []
        if spans[0].get('start', 0) > ORPHAN_MIN_GAP_SEC:
            gaps.append((0.0, spans[0]['start']))
        for i in range(len(spans) - 1):
            g0, g1 = spans[i].get('end', 0), spans[i + 1].get('start', 0)
            if g1 - g0 > ORPHAN_MIN_GAP_SEC:
                gaps.append((g0, g1))
        m = re.search(r'\((\d+)\s*분\)', meta.get('title') or '')
        if m:
            total_sec = int(m.group(1)) * 60
            last_end = spans[-1].get('end', 0)
            if total_sec - last_end > ORPHAN_MIN_GAP_SEC:
                gaps.append((last_end, total_sec))
        for g0, g1 in gaps:
            orphans.append({'lec': no, 'sec': round(g1 - g0, 1),
                            'gist': _orphan_gist(transcripts_dir, lid, g0, g1)})

    hollow = sorted(set(sections.keys()) - set((align.get('by_leaf') or {}).keys()))
    for lid in hollow:
        title = sections[lid]['path'][-1] if sections[lid].get('path') else lid
        orphans.append({'lec': None, 'sec': 0, 'leaf_id': lid,
                        'gist': '이 관에 정렬(align)로 붙은 전사 구간이 하나도 없음: %s' % title})
    return orphans


def target_leaves(sections, align):
    """생성 대상 관 목록 + 절별 관 묶음.

    관 경계가 아니라 절 단위로 판단을 옮겼으므로(build_section_bundle 참고),
    그 절에 구간이 하나라도 있으면 그 절의 모든 관이 대상이다 — 구간이 몰린
    관만 대상이 되고 나머지 관은 통째로 빈 채 넘어가던 문제(옛 97/160관)를
    없앤다.
    """
    section_of = {}
    for lid, sec in sections.items():
        section_of.setdefault(section_key(sec), []).append(lid)
    with_spans = {k for k, lids in section_of.items() if any(align['by_leaf'].get(l) for l in lids)}
    targets = [lid for lid in sections if section_key(sections[lid]) in with_spans]
    return targets, section_of


def apply_scope(targets, sections, base):
    """강의가 없는 세부과목은 생성 대상에서 뺀다. 화면(개념 완성)의 제외 규칙과
    같은 파일을 쓴다."""
    scope_f = base / 'scope.json'
    if not scope_f.exists():
        return targets
    ex = set(json.loads(scope_f.read_text(encoding='utf-8')).get('exclude_divisions') or [])
    if not ex:
        return targets
    before = len(targets)
    targets = [t for t in targets if not ((sections[t].get('path') or [''])[0] in ex)]
    print('  범위 제외(%s): %d → %d관' % (', '.join(sorted(ex)), before, len(targets)))
    return targets


def write_index(base, phase):
    """목차 화면이 읽을 색인. 트랙 파일 여러 개를 전부 받지 않게 하려는 것이다."""
    out = {}
    for f in sorted((base / 'track').glob('*.%s.json' % phase)):
        d = json.loads(f.read_text(encoding='utf-8'))
        for lf in d.get('leaves') or []:
            if not lf.get('leaf_id'):
                continue
            pts = lf.get('points') or []
            src = (pts[0].get('source') if pts else None) or 'lecture'
            out[lf['leaf_id']] = {'points': len(pts), 'source': src}
    (base / 'track' / '_index.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print('색인 %d관 저장' % len(out))


def save_orphans(base, subject, phase, orphans):
    """orphans 는 과목 전체 기준이라 유닛 파일마다 중복 적지 않고 _subject 트랙
    파일 하나에만 적는다(과목 레벨 트랙과 이미 같은 파일을 공유한다).
    """
    dst = track_path(base, '_subject', phase)
    old = json.loads(dst.read_text(encoding='utf-8')) if dst.exists() else None
    track = {'subject': subject, 'phase': phase, 'unit_code': '_subject',
             'leaves': (old or {}).get('leaves') or [], 'orphans': orphans}
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(track, ensure_ascii=False, indent=1), encoding='utf-8')


def anchors_by_section(sections, align):
    """앵커 검사용으로 절 안의 모든 leaf 구간을 합친 align_by_leaf.

    build_section_bundle 이 절 전체 구간을 재료로 주므로, 같은 절 형제 leaf 의
    강의를 앵커로 삼는 것은 정당하다 — check_track 자체는 건드리지 않고, 여기서
    "이 leaf 의 정당한 구간" 정의만 절 단위로 넓힌다. 절 밖 강의를 가리키는
    앵커(진짜 오분류)는 여전히 고심각도로 잡힌다.
    """
    _, section_of = target_leaves(sections, align)
    expanded = dict(align['by_leaf'])
    for lids in section_of.values():
        combined = [s for l in lids for s in align['by_leaf'].get(l, [])]
        for l in lids:
            expanded[l] = combined
    return expanded


def do_check(subject, phase):
    base = STUDY / subject / 'lectures'
    align = json.loads((base / 'align.json').read_text(encoding='utf-8'))
    names = template_names()
    tdir = base / 'track'
    if not tdir.exists():
        sys.exit('트랙이 아직 없습니다: %s' % tdir)
    write_index(base, phase)

    # F-3 후보 계산과 앵커 확장 둘 다 sections 가 필요하니 먼저 로드한다.
    try:
        sections = load_leaf_sections(subject)
    except Exception as e:
        sections = None
        print('  ⚠ taxonomy 로드 실패로 F-3(관 누락)·절 단위 앵커 확장을 건너뜀: %s' % e)
    anchors = anchors_by_section(sections, align) if sections is not None else align['by_leaf']

    total_issues, total_points, total_leaves = 0, 0, 0
    generated_leaf_ids = set()
    for f in sorted(tdir.glob('*.%s.json' % phase)):
        track = json.loads(f.read_text(encoding='utf-8'))
        issues = check_track(track, anchors, names)
        total_issues += len(issues)
        for lf in track.get('leaves', []):
            total_leaves += 1
            total_points += len(lf.get('points') or [])
            if lf.get('leaf_id'):
                generated_leaf_ids.add(lf['leaf_id'])
        for i in issues:
            print('  ⚠ %s' % i)
    print('\n관 %d개 · 논점 %d개 · 문제 %d건' % (total_leaves, total_points, total_issues))

    # F-3: align 에 있는데(=생성 대상이 될 수 있었는데) 트랙에 아예 없는 관.
    # 존재하는 트랙 파일만 순회하는 위 루프는 이걸 절대 못 잡는다 — 관 하나가
    # 통째로 건너뛰어져도 조용하다.
    if sections is not None:
        cand_list, _ = target_leaves(sections, align)
        cand_list = apply_scope(cand_list, sections, base)
        candidates = set(cand_list)
        missing = sorted(candidates - generated_leaf_ids)
        if missing:
            print('\n트랙이 아예 생성되지 않은 관 %d개:' % len(missing))
            for lid in missing:
                title = sections[lid]['path'][-1] if sections[lid].get('path') else lid
                print('  ⚠ 생성 안 됨: %s (%s)' % (title, lid))

    # F-1: orphans — 정렬이 어느 관에도 못 붙인 구간.
    orphan_secs, orphan_top = 0, []
    for f in sorted(tdir.glob('*.%s.json' % phase)):
        track = json.loads(f.read_text(encoding='utf-8'))
        for o in track.get('orphans') or []:
            orphan_secs += o.get('sec', 0)
            orphan_top.append(o)
    if orphan_secs or orphan_top:
        print('\n관에 안 붙은 구간 합계 %.1f분 (%d건)' % (orphan_secs / 60, len(orphan_top)))
        for o in sorted(orphan_top, key=lambda x: -(x.get('sec') or 0))[:10]:
            if o.get('lec') is None:
                print('  ⚠ %s' % o.get('gist', ''))
            else:
                print('  ⚠ %s강 %.1f초 미매핑 — %s' % (o.get('lec'), o.get('sec', 0), o.get('gist', '')))


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

    # orphans(F-1)는 과목 전체 기준이라 --limit/--only/--extra 와 무관하게, 이
    # 실행에서 생성 대상 관을 정하기 전에 align 전체를 훑어 한 번만 갱신한다.
    orphans = compute_orphans(args.subject, align, sections, tdir)
    save_orphans(base, args.subject, args.phase, orphans)
    orphan_sec = sum(o.get('sec', 0) for o in orphans)
    print('orphans 갱신: %d건 · %.1f분' % (len(orphans), orphan_sec / 60))

    if args.extra:
        build_extra(args, base, tdir, catalog)
        return

    targets, section_of = target_leaves(sections, align)
    targets = apply_scope(targets, sections, base)
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
    section_bundle_cache = {}
    t0 = time.time()
    for n, lid in enumerate(targets, 1):
        sec = sections[lid]
        title = sec['path'][-1] if sec['path'] else lid
        skey = section_key(sec)
        if skey not in section_bundle_cache:
            section_bundle_cache[skey] = build_section_bundle(
                section_of[skey], pages_text, note_map, align, meta, tdir, kdir)
        bundle = section_bundle_cache[skey]
        if not bundle['lectures']:
            print('  [%d/%d] 건너뜀(강의 구간 없음) %s' % (n, len(targets), title))
            continue
        siblings = [sections[s]['path'][-1] for s in section_of[skey]
                   if s != lid and sections[s].get('path')]
        prev_bodies = prev_bodies_for(base, sec['unit_code'], args.phase, lid, track_cache)
        try:
            pts = gen_leaf(lid, sec, bundle, catalog, args.subject,
                          siblings=siblings, prev_bodies=prev_bodies)
        except Exception as e:
            print('  [%d/%d] ❌ 실패 %s' % (n, len(targets), e))
            continue
        # 강의 전사가 이 관의 주제를 다루지 않는다고 판정되면(빈 배열) 형제 관
        # 내용을 끌어오는 대신, 전사 없이 교재 슬라이스만으로 다시 시도한다.
        if not pts and sec.get('body', '').strip():
            print('  [%d/%d] 강의에 없음 — 교재 기반으로 재시도 %s' % (n, len(targets), title))
            try:
                pts = gen_leaf_textbook(lid, sec, catalog, args.subject, siblings=siblings)
            except Exception as e:
                print('  [%d/%d] ❌ 교재 기반 생성도 실패 %s' % (n, len(targets), e))
        if not pts:
            print('  [%d/%d] ❌ 논점 0개 %s' % (n, len(targets), title))
            continue
        c_ok, c_total = chunk_holder['ok'], chunk_holder['total']
        save_leaf(base, args.subject, args.phase, sec['unit_code'], lid, title, pts,
                 chunks_ok=c_ok, chunks_total=c_total)
        units_touched.add(sec['unit_code'])
        chunk_note = ' (청크 %d/%d 실패 있음)' % (c_ok, c_total) if c_ok < c_total else ''
        print('  [%d/%d] %-34s 논점 %d개 · %d분%s' % (n, len(targets), title[:34],
                                                  len(pts), bundle['total_minutes'], chunk_note))

    print('\n유닛 %d개 저장 · 건너뜀 %d개 · %.1f분' % (len(units_touched), skipped,
                                              (time.time() - t0) / 60))
    print('토큰 in %s / out %s' % ('{:,}'.format(usage_holder['in']),
                                  '{:,}'.format(usage_holder['out'])))
    write_index(base, args.phase)


if __name__ == '__main__':
    main()
