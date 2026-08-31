#!/usr/bin/env python3
"""관(leaf)별 논점 트랙 생성 — 전사 + 교재 + 판서 → 강의 진행 순서의 논점 목록.

`generate_notes.py` 가 "교재에 없는 것만" 뽑는 보충이라면, 이쪽은 **강의가 실제로
다룬 것을 빠짐없이** 순서대로 세운다. 개념 완성 화면이 이 목록을 하나씩 소진하고,
다 비우면 그 관의 강의를 끝까지 들은 것과 같다.

**외부 API 호출은 없다.** 논점 생성은 Claude 에이전트가 파일을 읽고 써서 한다.
  --dump   : 관 하나를 만드는 데 필요한 재료(전사·교재·규칙)를 마크다운 파일로 낸다.
  --ingest : 에이전트가 채운 결과 JSON 을 검증한 뒤 트랙 파일에 병합한다.

출력: viewer/public/data/study/{과목}/lectures/track/{unit}.{phase}.json
중간 산출물(dump/ingest 왕복 파일): scripts/lectures/_work/{과목}/{phase}/

사용:
  python3 scripts/lectures/build_topic_track.py economics --phase basic --dump --limit 3
  # ... _work/economics/basic/{leaf_id}.md 를 읽고 {leaf_id}.json 을 채운다 ...
  python3 scripts/lectures/build_topic_track.py economics --phase basic --ingest
  python3 scripts/lectures/build_topic_track.py economics --phase basic --check
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import REPO, STUDY, WORK, SRC_ROOT  # noqa: E402
from build_note_bundle import merge_spans  # noqa: E402
from map_notes_to_leaves import extract_note_pages  # noqa: E402
from generate_notes import SUBJECT_RULES, load_leaf_sections  # noqa: E402
from track_core import (make_point_id, order_spans, check_track, diff_ids,  # noqa: E402
                        parse_viz_schema)

# dump/ingest 왕복 파일 루트. _paths.WORK(외장 드라이브의 _ai_pipeline)와는 다르다 —
# 이건 저장소 로컬(커밋 제외, .gitignore)이고 전사/키프레임 원본이 아니라 에이전트가
# 주고받는 중간 파일이다.
DUMP_ROOT = Path(__file__).resolve().parent / '_work'

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
- "gotcha" 깐깐이 — **묻기만 하지 말고 짚어 준다.** 반례·경계조건·시험 함정을 스스로 제시하고,
  왜 그 경계가 시험에 나오는지까지 말한다. "그럼 이 경우엔요?" 로 끝내는 질문형은 turns 전체에서
  절반 이하로 — 나머지는 "여기서 자주 틀리는 게 …" 처럼 짚어 주는 서술형으로 쓴다.
- "mate"   복습 메이트 — 무엇을 외우고 무엇은 넘길지. **개념·수치·이론 내용은 한 글자도 설명하지
  않는다.** ("콥더글러스는 ~이다", "1급 가격차별은 ~이다" 같은 설명 문장 금지.) 순수 학습 조언만
  — "이건 외워라", "이건 시험에 잘 안 나오니 넘겨도 된다", "앞 논점이랑 헷갈리지 않게 정리해라".

[반드시 지킬 것]
- **turns 에 "quiz" 턴이 최소 하나 있어야 합니다.** 없으면 학습자가 그냥 넘겨 버립니다.
- **캐릭터 넷(ask/teach/gotcha/mate)이 논점마다 최소 한 번씩은 등장해야 합니다.** 다만 억지로
  분량을 채우려고 내용 없는 대사를 넣지는 마세요 — 자연스럽게 넣을 자리가 정말 없으면 생략해도
  됩니다.
- **quiz 의 질문(prompt)은 긍정형으로만 쓰세요.** "틀린 것은?", "옳지 않은 것은?", "아닌 것은?"
  같은 부정형은 절대 쓰지 마세요. choices 의 `ok: true` 는 언제나 **맞는 선택지**를 뜻하는데,
  부정형 질문에서는 이 약속이 뒤집혀 채점이 반대로 됩니다.
- **quiz 의 choices 는 정답 1개 + 오답 2~3개, 총 3~4개입니다. 2개(정답1·오답1)는 절대
  만들지 마세요** — 찍어서 절반을 맞히는 문제가 됩니다.
- **오답은 그럴듯해야 합니다.** 실제로 헷갈리는 것 — 반대 개념(수요 vs 공급), 조건 하나만
  바꾼 것, 방향만 뒤집은 것. 전사에서 함정이라고 경고한 대목이 있으면 그걸 오답으로 쓰세요.
- **오답마다 그 오답 전용 reply 를 씁니다.** "틀렸습니다" 로 시작하지 마세요.
  왜 그렇게 생각했는지 짚고 바로잡으세요. 예: "그건 사는 쪽 얘기예요. 파는 사람
  입장에서 생각해봐요 — 값이 비싸지면 더 팔고 싶겠죠?"
- **quiz 는 바로 앞 대사에 답이 그대로 적혀 있으면 안 됩니다.** 방금 말한 문장을 그대로
  되묻는 것은 기억력 테스트일 뿐입니다. 앞에서 배운 것을 **적용**하거나 **구별**하게 하세요.
- 정답 choice 에도 reply 를 씁니다(짧게 확인해 주는 말).
- "강사", "강의", "선생님" 이라는 **단어**는 여전히 쓰지 마세요. 캐릭터 「선생」이 말하는
  것이지 누군가를 인용하는 게 아닙니다.
- 과장된 감탄사나 이모티콘을 남발하지 마세요. 친근하되 유치하지 않게.

[viz — 놓치지 말 것]
곡선의 이동, 균형의 변화, 면적(잉여·후생손실), 수식의 구조를 **말로** 설명하고 있다면
그림을 붙이세요. "왼쪽으로 이동한다"는 문장으로 끝내지 말고 [viz.steps — 상태가 변하는
논점이면 반드시 쓸 것]을 따라 실제 이동을 보이는 편이 훨씬 낫습니다. 이 대화 형식으로
바뀌었다고 viz 지시가 약해지는 것이 아닙니다 — 그림이 맞는 논점에 viz 를 빠뜨리는 것은
이전과 똑같이 잘못입니다.

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


def template_viz_schemas():
    """{템플릿 이름: parse_viz_schema() 결과} — --check 가 viz.params 를 검증하는 데 쓴다.

    template_names() 와 같은 방식으로 vizRegistry.js 를 긁어 템플릿 파일을 찾는다.
    스키마 파싱에 실패한 템플릿(부분집합 파서의 한계)은 그냥 빠진다 — check_track
    이 스키마가 없는 템플릿은 검증을 건너뛰므로 조용한 후퇴이지 오검출이 아니다.
    """
    src = (REPO / 'viewer/src/viz/vizRegistry.js').read_text(encoding='utf-8')
    out = {}
    for n in re.findall(r"from './templates/(\w+)'", src):
        f = REPO / 'viewer/src/viz/templates' / (n + '.jsx')
        if not f.exists():
            continue
        text = f.read_text(encoding='utf-8')
        m = re.search(r"name:\s*'([^']+)'", text)
        if not m:
            continue
        schema = parse_viz_schema(text)
        if schema is not None:
            out[m.group(1)] = schema
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


def gen_leaf_prompt(key, sec, bundle, catalog, subject, siblings=None, prev_bodies=''):
    """관 하나의 논점 생성 프롬프트를 조립한다.

    예전에는 이 함수(gen_leaf)가 전사를 청크로 나눠(chunk_lectures) 청크마다
    Gemini 를 호출했다 — 그 상한(MAX_CHUNK_CHARS)은 API 컨텍스트 한계 때문이었다.
    이제 API 를 부르지 않으므로 그 제약이 없다: 절 전체 전사를 통째로 한 프롬프트에
    담는다. 반환값은 (prompt, frames) — frames 는 참고용 판서 이미지 경로 목록이다
    (예전엔 call_gemini 에 이미지로 직접 넘겼다; 이제 dump 파일에 경로만 적어 두면
    필요할 때 Read 로 열어볼 수 있다).
    """
    blocks = bundle['lectures']
    transcript = '\n\n'.join('[%s강 %s]\n%s' % (b['no'], b['ts'], b['transcript'])
                             for b in blocks)
    frames = [f['file'] for b in blocks for f in b['frames']]
    note_block = ('[강사 필기노트 — 강의 중 화면에 띄운 문서]\n%s\n\n' % bundle['note_text'][:8000]
                  if bundle.get('note_text', '').strip() else '')
    # 밀도 지시 — 이 관 전체 분량에서 나와야 할 논점 개수를 프롬프트에 직접 숫자로 박는다.
    # 목표: 강의 3~4분당 논점 1개. (예전엔 청크당 상한 15개를 뒀다 — call_gemini 의
    # maxOutputTokens 를 안 넘기려는 안전판이었다. API 를 안 부르므로 그 상한은 더
    # 이상 의미가 없어 없앴다.)
    total_minutes = round(sum(b.get('minutes', 0) for b in blocks), 1)
    density_lo = max(3, int(total_minutes // 4))
    density_hi = max(density_lo, -(-int(total_minutes) // 3))  # ceil(minutes/3)
    density_note = (
        '\n[분량과 논점 개수]\n'
        '이 관의 강의 구간은 총 %s분입니다. 논점 하나가 강의 3~4분치를 덮는 밀도를\n'
        '목표로 하면 논점 %d~%d개가 나와야 합니다.\n'
        '이 목록만 읽고 강의를 대체할 사람이 있으므로, 한 논점이 강의 10분치를\n'
        '뭉뚱그리면 그 사람은 그 10분의 내용을 모릅니다.\n'
        '다만 이 개수는 목표이지 할당량이 아닙니다 — 강의가 실제로 짧게 다룬 내용을\n'
        '억지로 쪼개거나 없는 내용을 지어내 채우지 마세요. 강의가 정말 그만큼 다뤘을 때만\n'
        '그만큼 쓰세요.\n' % (total_minutes, density_lo, density_hi)
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
        '[강의 전사 — 이 관이 속한 절 전체 구간, %d분 · %d개 강의 구간 전체]\n%s\n\n'
        '판서 이미지가 있으면 이 파일 아래 "판서 이미지" 절에 경로가 있습니다. 수식·도식이\n'
        '텍스트에 없으면 열어서 반영하세요.'
        % (STYLE, SUBJECT_RULES.get(subject, ''), catalog,
           ' / '.join(sec['path']), sec['body'][:12000],
           sib_block, prev_block, note_block, density_note,
           total_minutes, len(blocks), transcript)
    )
    return prompt, frames


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


def gen_leaf_textbook_prompt(key, sec, catalog, subject, siblings=None):
    """강의 전사에 주제가 없는 관을 위한 프롬프트 조립. 전사를 아예 넣지 않는다 —
    넣으면 gen_leaf_prompt 처럼 형제 관 내용을 다시 끌어온다. 결과 points 마다
    source='textbook' 을 붙이는 것은 병합 단계(ingest)의 몫이다(앱은 이 값으로
    「교재 기반」 배지를 보여준다, viewer/src/ConceptScene.jsx, 수정 금지 파일).
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
    return prompt


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
# 자연히 여러 개다. 과목 레벨 트랙은 span 이 없어 강의 전체가 블록 하나가 되기 쉬워,
# 시간 창으로 나눠 두면 파일 안에서도 훑어보기 쉽다(글자수 상한과는 무관 — 자르는
# 것이 아니라 구획만 나누는 것이다. 전체 내용은 그대로 다 들어간다).
EXTRA_WINDOW_SEC = 600     # 블록 하나당 시간 창(10분)


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


def load_align(base, phase):
    """회독에 맞는 정렬 파일을 읽는다.

    1회독(basic)은 align.json, 그 밖의 회독은 align.<phase>.json 을 쓴다.
    회독별 파일이 없으면 align.json 으로 물러선다 — 예전 산출물 호환.
    """
    p = base / ('align.json' if phase == 'basic' else 'align.%s.json' % phase)
    if not p.exists():
        p = base / 'align.json'
    return json.loads(p.read_text(encoding='utf-8'))


def do_check(subject, phase):
    base = STUDY / subject / 'lectures'
    align = load_align(base, phase)
    names = template_names()
    schemas = template_viz_schemas()
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
        issues = check_track(track, anchors, names, schemas)
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


# ---------------------------------------------------------------------------
# --dump / --ingest — 재료 내보내기·결과 병합. API 호출은 하지 않는다.
# ---------------------------------------------------------------------------

def dump_dir(subject, phase):
    d = DUMP_ROOT / subject / phase
    d.mkdir(parents=True, exist_ok=True)
    return d


def manifest_path(subject, phase):
    return dump_dir(subject, phase) / '_manifest.json'


def load_manifest(subject, phase):
    p = manifest_path(subject, phase)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def save_manifest(subject, phase, manifest):
    manifest_path(subject, phase).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8')


# 결과 JSON 배열 원소 하나의 스키마 — 관 단위(output_instructions)·절 단위
# (output_instructions_section) dump 가 공유한다.
SCHEMA_BLOCK = (
    '배열 원소 하나의 스키마:\n'
    '```json\n'
    '{"title": "…", "gist": "…",\n'
    ' "turns": [\n'
    '   {"who": "ask", "text": "…"},\n'
    '   {"who": "teach", "text": "…", "viz": {"template": "…", "params": {}, "steps": []}},\n'
    '   {"who": "quiz", "prompt": "…", "choices": [\n'
    '      {"text": "…", "ok": true, "reply": "…"},\n'
    '      {"text": "…", "ok": false, "who": "gotcha", "reply": "…"}\n'
    '   ]},\n'
    '   {"who": "gotcha", "text": "…"},\n'
    '   {"who": "mate", "text": "…"}\n'
    ' ],\n'
    ' "example": {"q": "…", "solution": "…"},\n'
    ' "check": {"q": "…", "a": "…"},\n'
    ' "src": [{"lec": 12, "t": 1390}]}\n'
    '```\n'
    '`example` 은 계산·판단이 있는 논점에만 넣고, 없으면 생략하세요. 전사가 없는\n'
    '(교재 전용) 관이면 `src` 는 빈 배열로 두세요.\n'
)


def output_instructions(leaf_id, has_lecture=True):
    empty_note = (
        '이 관의 소제목이 전사에서 하나도 다뤄지지 않았다고 판단되면(=STYLE 의 covered\n'
        ':false 판정에 해당하면) 빈 배열 `[]` 을 저장하세요.\n\n'
        if has_lecture else
        '이 관은 강의 전사가 없어 교재만으로 씁니다 — [중요] 절이 설명하듯 covered:false\n'
        '판정은 여기 해당하지 않습니다. 교재에 있는 내용으로 points 를 채우세요.\n\n'
    )
    return (
        '\n\n---\n\n'
        '## 무엇을 어디에 쓸지\n\n'
        '위 내용을 바탕으로 이 관의 논점을 작성하세요. **STYLE 의 "[출력 형식]" 절이\n'
        '설명하는 covered/reason 래퍼는 이 파일에는 쓰지 않습니다** — 결과는 points\n'
        '만 담은 **JSON 배열**입니다. 다음 경로에 저장하세요 (이 .md 파일과 같은 폴더):\n\n'
        '    %s.json\n\n'
        '%s'
        + SCHEMA_BLOCK
    ) % (leaf_id, empty_note)


def build_md(lid, sec, prompt_text, frames, has_lecture=True):
    header = ('# 관: %s\n\nleaf_id: `%s`\nunit_code: `%s`\n\n---\n\n'
             % (' / '.join(sec.get('path') or [lid]), lid, sec.get('unit_code') or ''))
    frame_block = ''
    if frames:
        frame_block = ('\n\n---\n\n## 판서 이미지 (참고용 — 필요하면 Read 로 열어보세요)\n'
                       + '\n'.join('- %s' % f for f in frames))
    return header + prompt_text + frame_block + output_instructions(lid, has_lecture=has_lecture)


def dump_leaf(subject, phase, lid, sec, bundle, catalog, siblings, prev_bodies, manifest):
    has_lecture = bool(bundle and bundle.get('lectures'))
    if has_lecture:
        prompt, frames = gen_leaf_prompt(lid, sec, bundle, catalog, subject,
                                         siblings=siblings, prev_bodies=prev_bodies)
    else:
        prompt, frames = gen_leaf_textbook_prompt(lid, sec, catalog, subject, siblings=siblings), []
    md = build_md(lid, sec, prompt, frames, has_lecture=has_lecture)
    (dump_dir(subject, phase) / ('%s.md' % lid)).write_text(md, encoding='utf-8')
    manifest[lid] = {
        'unit_code': sec.get('unit_code'),
        'title': sec['path'][-1] if sec.get('path') else lid,
        'path': sec.get('path') or [],
        'has_lecture': has_lecture,
        'transcript_chars': sum(len(b['transcript']) for b in bundle['lectures']) if bundle else 0,
    }


def do_dump(args):
    base = STUDY / args.subject / 'lectures'
    align = load_align(base, args.phase)
    nm_path = base / 'note_map.json'
    note_map = (json.loads(nm_path.read_text(encoding='utf-8'))
                if nm_path.exists() else {'pages': [], 'by_leaf': {}})
    rel = NOTE_PDF.get(args.subject)
    pdf = str(SRC_ROOT / rel) if rel else None
    pages_text = ({p['page']: p['text'] for p in extract_note_pages(pdf)}
                  if pdf and Path(pdf).exists() else {})
    sections = load_leaf_sections(args.subject)
    tdir, kdir = WORK / 'transcripts' / args.subject, WORK / 'keyframes' / args.subject
    catalog = load_viz_catalog(args.subject)
    meta = lecture_meta(align)

    orphans = compute_orphans(args.subject, align, sections, tdir)
    save_orphans(base, args.subject, args.phase, orphans)
    orphan_sec = sum(o.get('sec', 0) for o in orphans)
    print('orphans 갱신: %d건 · %.1f분' % (len(orphans), orphan_sec / 60))

    targets, section_of = target_leaves(sections, align)
    targets = apply_scope(targets, sections, base)
    if args.only:
        targets = [t for t in targets if t == args.only]

    out_dir = dump_dir(args.subject, args.phase)
    manifest = load_manifest(args.subject, args.phase)
    track_cache = {}
    skipped = 0
    if not args.force:
        kept = []
        for lid in targets:
            unit = sections[lid]['unit_code']
            title = sections[lid]['path'][-1] if sections[lid]['path'] else lid
            if leaf_already_built(base, unit, args.phase, lid, track_cache):
                print('  건너뜀(트랙에 이미 있음) %s' % title)
                skipped += 1
            elif (out_dir / ('%s.json' % lid)).exists():
                print('  건너뜀(응답 대기중 — ingest 하세요) %s' % title)
                skipped += 1
            else:
                kept.append(lid)
        targets = kept

    if args.limit:
        targets = targets[:args.limit]
    print('대상 관 %d개(건너뜀 %d개)\n' % (len(targets), skipped))

    section_bundle_cache = {}
    dumped = 0
    for n, lid in enumerate(targets, 1):
        sec = sections[lid]
        title = sec['path'][-1] if sec['path'] else lid
        skey = section_key(sec)
        if skey not in section_bundle_cache:
            section_bundle_cache[skey] = build_section_bundle(
                section_of[skey], pages_text, note_map, align, meta, tdir, kdir)
        bundle = section_bundle_cache[skey]
        siblings = [sections[s]['path'][-1] for s in section_of[skey]
                   if s != lid and sections[s].get('path')]
        prev_bodies = prev_bodies_for(base, sec['unit_code'], args.phase, lid, track_cache)
        dump_leaf(args.subject, args.phase, lid, sec, bundle, catalog, siblings, prev_bodies, manifest)
        dumped += 1
        kind = 'lecture' if bundle['lectures'] else 'textbook'
        print('  [%d/%d] dump %-34s (%s)' % (n, len(targets), title[:34], kind))

    save_manifest(args.subject, args.phase, manifest)
    print('\ndump %d개 · 건너뜀 %d개 → %s' % (dumped, skipped, out_dir))


def dump_extra(args):
    groups = EXTRA_GROUPS.get(args.subject)
    if not groups:
        sys.exit('%s 는 과목 레벨 트랙 정의가 없습니다.' % args.subject)
    base = STUDY / args.subject / 'lectures'
    tdir = WORK / 'transcripts' / args.subject
    catalog = load_viz_catalog(args.subject)
    out_dir = dump_dir(args.subject, args.phase)
    manifest = load_manifest(args.subject, args.phase)
    dumped = skipped = 0
    for gi, g in enumerate(groups):
        lid = '_subject-%02d' % gi
        if not args.force:
            if extra_group_built(base, args.phase, g['title']):
                print('  건너뜀(트랙에 이미 있음) %s' % g['title'])
                skipped += 1
                continue
            if (out_dir / ('%s.json' % lid)).exists():
                print('  건너뜀(응답 대기중 — ingest 하세요) %s' % g['title'])
                skipped += 1
                continue
        blocks = []
        for lecid in g['lectures']:
            f = tdir / ('%s.json' % lecid)
            if not f.exists():
                print('  ⚠ 전사 없음: %s' % lecid)
                continue
            tr = json.loads(f.read_text(encoding='utf-8'))
            no = tr.get('no')
            if no is None:
                no = int(re.search(r'(\d+)$', lecid).group(1))
            blocks.extend(windowed_blocks(tr, no))
        if not blocks:
            print('  ⚠ %s: 전사가 하나도 없어 건너뜀' % g['title'])
            continue
        sec = {'path': [g['title']], 'body': '', 'heads': [], 'unit_code': '_subject'}
        prompt, frames = gen_leaf_prompt(g['title'], sec, {'lectures': blocks, 'note_text': ''},
                                         catalog, args.subject)
        md = build_md(lid, sec, prompt, frames)
        (out_dir / ('%s.md' % lid)).write_text(md, encoding='utf-8')
        manifest[lid] = {'unit_code': '_subject', 'title': g['title'], 'path': [g['title']],
                         'has_lecture': True, 'kind': g['kind'], 'gi': gi,
                         'transcript_chars': sum(len(b['transcript']) for b in blocks)}
        dumped += 1
        print('  [%d/%d] dump %s' % (gi + 1, len(groups), g['title']))
    save_manifest(args.subject, args.phase, manifest)
    print('\ndump %d개 · 건너뜀 %d개 → %s' % (dumped, skipped, out_dir))


# ---------------------------------------------------------------------------
# --dump-section — 관 단위 dump 는 같은 절의 형제 관마다 절 전사가 통째로
# 중복된다(관 5개짜리 절이면 전사가 5번). 그러면 파일이 커질 뿐 아니라, 형제
# 관을 각각 따로 채우는 에이전트가 서로 뭘 썼는지 몰라 관문이 지적한 형제
# 중복(같은 관 안·관 사이)이 재발한다. 절 하나를 파일 하나로 묶어 한 번에
# 나눠 쓰게 하면 전사 중복도, 형제 중복도 함께 없어진다.
#
# 결과 JSON({leaf_id}.json)은 관 단위 dump 와 **같은 자리**
# (dump_dir(subject, phase), sections/ 하위가 아니다)에 쓰라고 안내한다 —
# do_ingest 를 전혀 건드리지 않고 그대로 재사용하기 위해서다. 대신 이 leaf_id
# 들을 평평한 매니페스트(_manifest.json)에도 같이 등록해, --dump-section 으로만
# 낸 관도 --ingest 가 찾을 수 있게 한다.
# ---------------------------------------------------------------------------

def section_slug(path):
    """절 경로(대분류/장/절)를 파일명으로 쓸 수 있는 식별자로 만든다."""
    return '__'.join(re.sub(r'[\s·]+', '_', p) for p in path)


def gen_section_prompt(path, lids, sections, bundle, catalog, subject, base, phase, track_cache):
    """절 하나의 논점 생성 프롬프트를 조립한다 — 전사는 절 전체에서 딱 한 번만
    등장하고, 그 절에 속한 모든 관의 교재 본문을 나란히 늘어놓아 전사를 관별로
    나눠 쓰게 한다. gen_leaf_prompt 와 달리 관 하나가 아니라 절 전체가 대상이라
    '형제 관 배제' 대신 '형제 관과 나눠 쓰기' 프레이밍을 쓴다.
    """
    has_lecture = bool(bundle['lectures'])
    frames = [f['file'] for b in bundle['lectures'] for f in b['frames']]
    if has_lecture:
        transcript_header = ('[강의 전사 — 이 절 전체, %d분 · %d개 강의 구간 전체]'
                             % (bundle['total_minutes'], len(bundle['lectures'])))
        transcript_block = '\n\n'.join('[%s강 %s]\n%s' % (b['no'], b['ts'], b['transcript'])
                                       for b in bundle['lectures'])
    else:
        transcript_header = '[강의 전사]'
        transcript_block = '이 절은 강의가 다루지 않습니다 — 교재만으로 쓰세요.'
    note_block = ('[강사 필기노트 — 강의 중 화면에 띄운 문서]\n%s\n\n' % bundle['note_text'][:8000]
                  if bundle.get('note_text', '').strip() else '')

    leaves_parts = []
    for lid in lids:
        sec = sections[lid]
        title = sec['path'][-1] if sec.get('path') else lid
        heads = sec.get('heads') or []
        body = sec.get('body') or ''
        prev_bodies = prev_bodies_for(base, sec['unit_code'], phase, lid, track_cache)
        part = '### 관: %s\n\nleaf_id: `%s`\n\n' % (title, lid)
        if heads:
            part += '교재 소제목: ' + ' / '.join(heads) + '\n\n'
        part += '[교재 본문 — 이 관의 범위 기준]\n%s\n\n' % body
        if prev_bodies:
            part += '[이 관의 이전 정리 — 재료로만 사용, 문장을 그대로 옮기지 마세요]\n%s\n\n' % prev_bodies[:6000]
        leaves_parts.append(part)

    prompt = (
        '%s\n%s\n\n%s\n\n'
        '## 이 절에 속한 관 목록 (%d개) — 전사를 이 관들로 나눠 쓰세요\n\n%s'
        '%s\n%s\n%s\n\n'
        '판서 이미지가 있으면 이 파일 아래 "판서 이미지" 절에 경로가 있습니다. 수식·도식이\n'
        '텍스트에 없으면 열어서 반영하세요.'
        % (STYLE, SUBJECT_RULES.get(subject, ''), catalog,
           len(lids), '\n'.join(leaves_parts),
           note_block, transcript_header, transcript_block)
    )
    return prompt, frames, has_lecture


SECTION_SPLIT_PARAGRAPH = (
    '이 절의 관들을 **한 번에 나눠 쓰는 것**이 이 파일의 목적입니다. 전사를 읽고 각 내용이\n'
    '어느 관에 속하는지 판단한 뒤, 그 관의 JSON 에만 쓰세요. **같은 내용을 두 관에 쓰지\n'
    '마세요.** 어느 관에도 명확히 속하지 않는 내용은 버리세요.\n'
    '강의가 어떤 관의 주제를 실제로 다루지 않았다면, 그 관의 JSON 은 **빈 배열 `[]`** 로\n'
    '두세요. 형제 관 내용으로 채우지 마세요 — 강의가 다루지 않은 것을 다룬 것처럼 만드는\n'
    '것은 아무것도 만들지 않는 것보다 나쁩니다. 그런 관은 나중에 교재만으로 따로 만듭니다.\n'
)


def output_instructions_section(leaf_titles, out_dir_abs, has_lecture):
    """leaf_titles: [(leaf_id, title), ...]. 결과 JSON은 관 단위 dump 와 같은
    자리(out_dir_abs, dump_dir(subject, phase))에 쓰라고 안내한다 — ingest 는
    거기만 본다."""
    paths = '\n'.join('    %s → %s/%s.json' % (title, out_dir_abs, lid)
                      for lid, title in leaf_titles)
    textbook_note = (
        '\n이 절은 강의가 없어 교재만으로 씁니다 — 각 관의 논점마다 `"source": "textbook"`\n'
        '을 넣고, `src` 는 빈 배열로 두세요. covered:false 판정은 여기 해당하지 않습니다.\n'
        if not has_lecture else ''
    )
    return (
        '\n\n---\n\n'
        '## 무엇을 어디에 쓸지\n\n'
        + SECTION_SPLIT_PARAGRAPH +
        '\n각 관마다 covered/reason 래퍼 없이 points 만 담은 JSON 배열을 다음 경로에\n'
        '저장하세요 (관마다 파일 하나, 이 절 안에서 관 이름이 아니라 leaf_id 로 구분):\n\n'
        + paths + '\n\n' + textbook_note + '\n'
        + SCHEMA_BLOCK
    )


def build_section_md(sid, path, lids, sections, bundle, catalog, subject, base, phase,
                     track_cache, out_dir_abs):
    prompt, frames, has_lecture = gen_section_prompt(
        path, lids, sections, bundle, catalog, subject, base, phase, track_cache)
    leaf_titles = [(lid, sections[lid]['path'][-1] if sections[lid].get('path') else lid)
                  for lid in lids]
    header = ('# 절: %s\n\n절 식별자: `%s`\n관 %d개: %s\n\n---\n\n'
             % (' / '.join(path), sid, len(lids), ', '.join(t for _, t in leaf_titles)))
    frame_block = ''
    if frames:
        frame_block = ('\n\n---\n\n## 판서 이미지 (참고용 — 필요하면 Read 로 열어보세요)\n'
                       + '\n'.join('- %s' % f for f in frames))
    footer = output_instructions_section(leaf_titles, out_dir_abs, has_lecture)
    return header + prompt + frame_block + footer, has_lecture, leaf_titles


def do_dump_section(args):
    base = STUDY / args.subject / 'lectures'
    align = load_align(base, args.phase)
    nm_path = base / 'note_map.json'
    note_map = (json.loads(nm_path.read_text(encoding='utf-8'))
                if nm_path.exists() else {'pages': [], 'by_leaf': {}})
    rel = NOTE_PDF.get(args.subject)
    pdf = str(SRC_ROOT / rel) if rel else None
    pages_text = ({p['page']: p['text'] for p in extract_note_pages(pdf)}
                  if pdf and Path(pdf).exists() else {})
    sections = load_leaf_sections(args.subject)
    tdir, kdir = WORK / 'transcripts' / args.subject, WORK / 'keyframes' / args.subject
    catalog = load_viz_catalog(args.subject)
    meta = lecture_meta(align)

    orphans = compute_orphans(args.subject, align, sections, tdir)
    save_orphans(base, args.subject, args.phase, orphans)
    orphan_sec = sum(o.get('sec', 0) for o in orphans)
    print('orphans 갱신: %d건 · %.1f분' % (len(orphans), orphan_sec / 60))

    targets, section_of = target_leaves(sections, align)
    targets = apply_scope(targets, sections, base)
    # 절은 with_spans 판정에서 이미 전부-혹은-전무로 걸러졌으므로(target_leaves),
    # apply_scope 뒤 남은 leaf 들의 section_key 를 모으면 그 절의 leaf 전체가
    # section_of[skey] 에 그대로 남아 있다 — 부분적으로 잘린 절은 없다.
    skeys = list(dict.fromkeys(section_key(sections[lid]) for lid in targets))

    out_dir = dump_dir(args.subject, args.phase)      # 결과 JSON·평평한 매니페스트 자리
    sections_dir = out_dir / 'sections'
    sections_dir.mkdir(parents=True, exist_ok=True)
    section_manifest_path = sections_dir / '_manifest.json'
    section_manifest = (json.loads(section_manifest_path.read_text(encoding='utf-8'))
                        if section_manifest_path.exists() else {})
    flat_manifest = load_manifest(args.subject, args.phase)

    track_cache = {}

    def section_done(lids):
        return all(
            leaf_already_built(base, sections[lid]['unit_code'], args.phase, lid, track_cache)
            or (out_dir / ('%s.json' % lid)).exists()
            for lid in lids
        )

    kept = []
    skipped = 0
    for skey in skeys:
        lids = section_of[skey]
        sid = section_slug(list(skey))
        if args.only and args.only != sid and args.only not in lids:
            continue
        if not args.force and section_done(lids):
            print('  건너뜀(모든 관 완료/응답대기) %s' % sid)
            skipped += 1
            continue
        kept.append((skey, sid, lids))

    if args.limit:
        kept = kept[:args.limit]
    print('대상 절 %d개(건너뜀 %d개)\n' % (len(kept), skipped))

    dumped = 0
    for n, (skey, sid, lids) in enumerate(kept, 1):
        bundle = build_section_bundle(lids, pages_text, note_map, align, meta, tdir, kdir)
        md, has_lecture, leaf_titles = build_section_md(
            sid, list(skey), lids, sections, bundle, catalog, args.subject,
            base, args.phase, track_cache, str(out_dir))
        (sections_dir / ('%s.md' % sid)).write_text(md, encoding='utf-8')
        chars = sum(len(b['transcript']) for b in bundle['lectures'])
        section_manifest[sid] = {
            'path': list(skey),
            'leaves': [{'leaf_id': lid, 'title': t} for lid, t in leaf_titles],
            'has_lecture': has_lecture, 'transcript_chars': chars,
            'file': 'sections/%s.md' % sid,
        }
        # 관 단위 --dump 와 같은 평평한 매니페스트에도 등록한다 — do_ingest 는
        # 이 매니페스트만 읽으므로, 여기 등록하지 않으면 --dump-section 으로만
        # 낸 관을 ingest 가 "매니페스트에 없음"으로 건너뛴다.
        for lid, title in leaf_titles:
            flat_manifest[lid] = {
                'unit_code': sections[lid].get('unit_code'), 'title': title,
                'path': sections[lid].get('path') or [],
                'has_lecture': has_lecture, 'transcript_chars': chars,
            }
        dumped += 1
        kind = 'lecture' if has_lecture else 'textbook'
        print('  [%d/%d] dump-section %-30s 관 %d개 (%s)'
             % (n, len(kept), sid[:30], len(lids), kind))

    section_manifest_path.write_text(
        json.dumps(section_manifest, ensure_ascii=False, indent=1), encoding='utf-8')
    save_manifest(args.subject, args.phase, flat_manifest)
    print('\ndump-section %d개 · 건너뜀 %d개 → %s' % (dumped, skipped, sections_dir))


# 이 표현 중 하나라도 issue 문자열에 들어있으면 병합을 거부한다(과제 명세 §2 그대로).
# 나머지 check_track 의 issue(논점 수 상식 범위, 미등록 viz 템플릿 등)는 경고만
# 찍고 병합은 진행한다.
BLOCKING_MARKERS = ('turns 없음', 'quiz 턴 없음', '정답 선택지가', '오답 선택지가', '전용 반박이 없다')


def validate_result(points_raw, lid, title, unit, names):
    """dump 결과 JSON 을 병합 전에 검사한다. (issues, blocking) 을 돌려준다.

    track_core.check_track 을 재사용한다 — 병합 전이라 트랙 형태가 아니므로
    leaf 하나짜리 가짜 트랙으로 감싸는 어댑터만 둔다. align_by_leaf 를 빈 dict 로
    주면 앵커(src) 검사는 자연히 건너뛴다(그 leaf 의 정당한 구간을 모르니 판정할
    수 없다) — ingest 가 align.json/외장 드라이브 없이도 동작하게 하려는 의도다.
    """
    if not isinstance(points_raw, list):
        return (['결과가 JSON 배열이 아닙니다'], True)
    if not points_raw:
        return (['논점이 0개입니다'], True)
    if not all(isinstance(p, dict) for p in points_raw):
        return (['배열 원소 중 논점 객체가 아닌 항목이 있습니다'], True)
    fake_track = {'unit_code': unit, 'leaves': [{'leaf_id': lid, 'title': title, 'points': points_raw}]}
    issues = check_track(fake_track, {}, names)
    blocking = any(any(m in i for m in BLOCKING_MARKERS) for i in issues)
    return (issues, blocking)


def do_ingest(args):
    base = STUDY / args.subject / 'lectures'
    sections = load_leaf_sections(args.subject)
    manifest = load_manifest(args.subject, args.phase)
    out_dir = dump_dir(args.subject, args.phase)
    names = template_names()

    ids = [args.only] if args.only else sorted(manifest.keys())
    if args.extra and not args.only:
        ids = [i for i in ids if i.startswith('_subject-')]

    merged, rejected, waiting = 0, 0, 0
    for lid in ids:
        info = manifest.get(lid)
        if info is None:
            print('  ⚠ %s: 매니페스트에 없음 — 먼저 --dump 를 실행하세요' % lid)
            continue
        rf = out_dir / ('%s.json' % lid)
        if not rf.exists():
            waiting += 1
            continue
        try:
            raw = json.loads(rf.read_text(encoding='utf-8'))
        except (ValueError, OSError) as e:
            print('  ❌ %s: JSON 파싱 실패 — %s' % (lid, e))
            rejected += 1
            continue

        title = info.get('title', lid)
        unit = info.get('unit_code') or '?'
        issues, blocking = validate_result(raw, lid, title, unit, names)
        if blocking:
            print('  ❌ %s: 병합 거부' % title)
            for i in issues:
                print('     - %s' % i)
            rejected += 1
            continue
        for i in issues:
            print('  ⚠ %s: %s' % (title, i))

        has_lecture = info.get('has_lecture')
        for p in raw:
            if not p.get('source'):
                p['source'] = 'lecture' if has_lecture else 'textbook'
            if not has_lecture:
                p.setdefault('src', [])

        if unit == '_subject':
            gi = info.get('gi')
            if gi is None:
                print('  ⚠ %s: _subject 그룹인데 매니페스트에 gi 없음 — 건너뜀' % lid)
                rejected += 1
                continue
            save_extra_group(base, args.subject, args.phase, gi, info.get('kind', 'extra'), title, raw)
        else:
            if lid not in sections:
                print('  ⚠ %s: taxonomy 에 없는 leaf_id — 건너뜀' % lid)
                rejected += 1
                continue
            save_leaf(base, args.subject, args.phase, sections[lid]['unit_code'], lid, title, raw)
        merged += 1
        print('  [%d] 병합 %s — 논점 %d개' % (merged, title, len(raw)))

    print('\n병합 %d개 · 거부 %d개 · 응답 대기 %d개' % (merged, rejected, waiting))
    if merged:
        write_index(base, args.phase)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--phase', default='basic')
    ap.add_argument('--limit', type=int)
    ap.add_argument('--only', help='특정 leaf_id 하나만 (또는 _subject-NN)')
    ap.add_argument('--check', action='store_true', help='생성하지 않고 검증만')
    ap.add_argument('--force', action='store_true',
                    help='이미 트랙에 있거나 이미 응답이 와 있는 관도 다시 처리')
    ap.add_argument('--extra', action='store_true',
                    help='관에 안 붙은 강의를 과목 레벨 트랙(_subject)으로 처리')
    ap.add_argument('--dump', action='store_true',
                    help='재료를 관 단위로 scripts/lectures/_work/ 에 마크다운으로 내보낸다(API 호출 없음)')
    ap.add_argument('--dump-section', action='store_true',
                    help='재료를 절 단위로 _work/.../sections/ 에 내보낸다 — 전사 중복·형제 관 '
                         '중복을 피하려면 이쪽을 쓰세요(API 호출 없음)')
    ap.add_argument('--ingest', action='store_true',
                    help='_work/ 의 결과 JSON 을 검증한 뒤 트랙에 병합한다(API 호출 없음)')
    args = ap.parse_args()

    if args.check:
        do_check(args.subject, args.phase)
        return

    if args.dump_section:
        if args.dump or args.ingest:
            sys.exit('--dump-section 은 --dump/--ingest 와 함께 쓸 수 없습니다.')
        do_dump_section(args)
        return

    if args.dump and args.ingest:
        sys.exit('--dump 와 --ingest 는 동시에 쓸 수 없습니다.')
    if not args.dump and not args.ingest:
        ap.print_help()
        sys.exit('\n외부 API 호출은 제거됐습니다(더 이상 이 스크립트가 직접 모델을 부르지\n'
                 '않습니다). --dump (관 단위) 또는 --dump-section (절 단위, 권장) 로 재료를\n'
                 '내보내거나, --ingest 로 결과를 병합하세요. 검증만 하려면 --check.')

    if args.dump:
        if args.extra:
            dump_extra(args)
        else:
            do_dump(args)
    else:
        do_ingest(args)


if __name__ == '__main__':
    main()
