#!/usr/bin/env python3
"""관(leaf)별 강의 필기 생성 — 전사본 + 필기노트 + 판서 키프레임 → 교재에 녹아드는 보충 본문.

핵심은 **교재를 반복하지 않는 것**이다. 교재에 이미 있는 정의·수식을 다시 쓰면 화면에서
같은 말을 두 번 읽게 된다. 강의에만 있는 것(설명 순서, 비유, 무엇을 외우고 무엇을 넘길지,
판서로만 남은 수식)을 골라 교재 소제목 사이에 끼워 넣는다.

출력 형식은 `notes/{unit_code}.{phase}.md` — 한 유닛의 여러 관이 `<!-- leaf: … -->` 앵커로
이어지고, 각 관 안에서는 `<!-- after: 교재소제목 -->` 로 삽입 위치를 지정한다.

사용:
  python3 scripts/lectures/generate_notes.py economics --phase basic --limit 2
  python3 scripts/lectures/generate_notes.py economics --phase basic          # 전체
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import REPO, STUDY, WORK  # noqa: E402
from build_note_bundle import build, DEFAULT_PDF  # noqa: E402
from map_notes_to_leaves import extract_note_pages  # noqa: E402

MODEL = 'gemini-3-flash-preview'
API = 'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}'
MAX_FRAMES = 8          # 관당 판서 이미지 수 상한 — 비용과 판독 이득의 절충
MAX_TRANSCRIPT = 60000  # 아주 긴 관은 앞뒤를 살려 자른다

STYLE = """당신은 감정평가사 1차 수험 교재를 쓰는 사람입니다.
강의(음성 전사 + 강사 필기노트 + 판서 사진)에서 **교재에 없는 것만** 뽑아
교재 사이사이에 끼워 넣을 보충 본문을 씁니다.

[가장 중요 — 교재를 반복하지 말 것]
- 아래 [교재 본문]에 이미 있는 정의·수식·표는 다시 쓰지 마세요. 독자는 바로 위에서 그걸 읽었습니다.
- 강의에만 있는 것을 쓰세요: 설명의 순서와 이유, 비유·예시, 무엇을 외우고 무엇은 넘기라는 지침,
  판서에만 있는 수식·도식, 학파 간 대립 구도, 다음 단원과의 연결.

[문체 — 교재와 구분이 안 되게]
- **"강사", "강의", "선생님" 이라는 단어를 아예 쓰지 마세요.** "강사가 제시한", "강의에서 강조한"
  같은 표현도 금지입니다. 출처를 밝히지 말고 그냥 교재처럼 단정적으로 서술하세요.
- 큰따옴표로 강사 말을 옮기지 마세요. 내용만 일반 서술로 바꾸세요.
- 전사 오류·음성 인식 같은 제작 뒷얘기는 절대 쓰지 마세요.
- 문장은 '~이다/~한다' 체. 수험서 톤으로 담백하게.

[표기]
- 수식은 KaTeX 인라인 `$...$`, 독립 수식은 `$$...$$`.
- 강조는 `**굵게**`.
- **둘 이상을 나란히 놓고 견주는 대목은 반드시 마크다운 표로 쓰세요.**
  학파 대립(케인즈 vs 고전·통화주의), A안 vs B안, 단기 vs 장기, 장점 vs 단점,
  유형 분류(3가지 이상) 같은 것은 산문으로 늘어놓지 말고 표로 정리합니다.
  예)
  | | 케인즈학파 | 통화주의 |
  |---|---|---|
  | 화폐수요의 이자율탄력성 | 크다 | 작다 |
  | 통화정책 효과 | 작다 | 크다 |
- 표는 비교축(행)을 3개 이상 잡아 실제로 대조가 드러나게 하세요.
- 근거가 된 강의 시각은 문장 끝에 `[43강 39:45]` 형태로 답니다(화면에는 안 보이지만 되짚기용).

[복습 메이트]
- 학습 조언(무엇을 외우고 무엇은 넘길지, 어떤 문제로 나오는지)은 아래 형식으로 분리하세요.
  > 🐶 **복습 메이트** — 조언 내용
- 내용 설명은 넣지 마세요. 조언만. 관당 0~2개면 충분합니다.

[이 관의 범위를 지킬 것]
- 지금 쓰는 것은 **이 관 하나**의 보충입니다. 다른 관 제목에 해당하는 내용은 쓰지 마세요.
  (예: '3면 등가의 원칙'이 별도 관이면 여기서 그 내용을 설명하지 않습니다.)
- 전사에 다른 관·다른 장의 이야기가 섞여 있어도 걸러내세요. 강의 도입부의 과목 전체 안내처럼
  이 관과 무관한 대목도 버립니다.

[삽입 위치]
- 각 덩어리 앞에 `<!-- after: 교재소제목 -->` 을 붙여 어느 소제목 뒤에 들어갈지 지정합니다.
- 소제목은 아래 [교재 소제목 목록]에 있는 문자열을 **그대로** 쓰세요.
- 관 도입부(교재 맨 앞)에 넣을 것은 `<!-- after: _top -->`.

출력은 마크다운 본문만. 설명·인사말·코드펜스 없이 바로 시작하세요."""

# 과목별로 **지어내면 치명적인 것**이 다르다. 음성 전사는 숫자에 특히 약해서
# ("제99조"가 "제98조"로 들린다) 확인되지 않은 번호를 그럴듯하게 채워 넣기 쉽다.
# 틀린 조문 번호·판례 번호는 수험생이 그대로 외우므로 없느니만 못하다.
SUBJECT_RULES = {
    'law': """
[법규 — 번호를 지어내지 말 것]
- **조문 번호(제○조·제○항·제○호)와 기간·금액·면적 수치는 [교재 본문]에 있는 것만 쓰세요.**
  전사에서 들린 번호는 음성 인식 오류일 수 있으니 교재로 확인되지 않으면 번호 없이
  "관계 법령에서 정한다" 식으로 쓰거나 아예 언급하지 마세요.
- 법률 이름은 줄이지 말고 정식 명칭을 쓰세요(예: '국토계획법' → '국토의 계획 및 이용에 관한 법률').
- 절차·권한은 **누가(주체) / 무엇을(대상) / 며칠 안에(기한)** 를 표로 정리하면 좋습니다.
""",
    'civil': """
[민법 — 번호를 지어내지 말 것]
- **조문 번호와 판례 사건번호는 [교재 본문]에 있는 것만 쓰세요.** 전사에서 들린 번호는
  음성 인식 오류일 수 있습니다. 확인되지 않으면 "판례는 …라고 본다" 처럼 번호 없이 쓰세요.
- 요건·효과는 나눠서 쓰세요. 특히 **요건은 빠짐없이** 적어야 사례형에서 쓸 수 있습니다.
- 학설 대립은 표로(견해 / 논거 / 결론), 판례 입장은 어느 견해에 서 있는지 분명히 적으세요.
""",
    'accounting': """
[회계 — 숫자와 분개]
- 분개는 차변/대변을 표로 쓰세요.
  | 차변 | 금액 | 대변 | 금액 |
  |---|---:|---|---:|
- **금액은 판서·전사에서 확인된 것만** 쓰고, 계산 과정을 한 줄로 같이 보이세요
  (예: $감가상각비 = (취득원가 - 잔존가치) \\times \\frac{1}{내용연수}$).
- 계산 순서가 있는 논점은 번호를 매긴 단계로 쓰세요. 결과만 적으면 시험에서 못 씁니다.
""",
}


def load_leaf_sections(subject):
    """관 → (unit_code, 교재 본문, 소제목 목록)"""
    base = STUDY / subject
    idx = json.loads((base / 'ai_taxonomy_index.json').read_text(encoding='utf-8'))
    leaves = idx['leaves'] if isinstance(idx, dict) else idx
    cache = {}
    out = {}
    for lf in leaves:
        uf = lf.get('unit_file')
        if not uf:
            continue
        if uf not in cache:
            p = base / uf
            cache[uf] = p.read_text(encoding='utf-8').split('\n') if p.exists() else []
        lines = cache[uf]
        sl = lf.get('section_lines')
        body = '\n'.join(lines[max(0, sl[0] - 1):min(len(lines), sl[1])]) if sl else ''
        heads = [re.sub(r'^#+\s*', '', l).strip() for l in body.split('\n') if re.match(r'^#{2,6}\s', l)]
        out[lf['id']] = {'unit_code': lf.get('unit_code'), 'body': body, 'heads': heads,
                         'path': lf.get('path', [])}
    return out


def call_gemini(key, prompt, images):
    parts = [{'text': prompt}]
    for img in images:
        parts.append({'inline_data': {'mime_type': 'image/jpeg',
                                      'data': base64.b64encode(Path(img).read_bytes()).decode()}})
    payload = {'contents': [{'parts': parts}],
               'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 8000}}
    req = urllib.request.Request(
        API.format(m=MODEL, k=key),
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            cand = (d.get('candidates') or [{}])[0]
            txt = ''.join(p.get('text', '') for p in cand.get('content', {}).get('parts', []))
            usage = d.get('usageMetadata', {})
            return txt.strip(), usage
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:200]
            if e.code in (429, 500, 503) and attempt < 3:
                time.sleep(8 * (attempt + 1))
                continue
            raise RuntimeError(f'HTTP {e.code}: {body}')
        except Exception:
            if attempt < 3:
                time.sleep(5)
                continue
            raise
    return '', {}


def normalize_mate(md):
    """복습 메이트 줄을 인용문(>)으로 맞춘다.

    렌더러는 `> 🐶 …` 형태여야 말풍선 박스로 그린다. 모델이 `>` 를 자주 빠뜨리는데,
    그러면 본문에 섞여 조언인지 설명인지 구분이 사라진다.
    """
    # 모델이 종종 흘리는 출처 표현을 걷어낸다. 문장이 깨지지 않는 형태로만 치환한다.
    for a, b in [('강사가 제시한 ', ''), ('강사가 강조한 ', ''), ('강사가 짚은 ', ''),
                 ('강사의 ', ''), ('강사는 ', ''), ('강의에서 강조한 ', ''),
                 ('강의에서는 ', ''), ('강의에서 ', '')]:
        md = md.replace(a, b)
    out = []
    for ln in md.split('\n'):
        if re.match(r'^\s*🐶', ln):
            out.append('> ' + ln.strip())
        else:
            out.append(ln)
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--phase', default='basic')
    ap.add_argument('--pdf', default=None,
                    help='강사 필기노트 PDF. 없는 과목은 생략(전사+판서만 사용)')
    ap.add_argument('--limit', type=int)
    ap.add_argument('--only', help='특정 leaf_id 하나만')
    ap.add_argument('--leaves-file', help='재생성할 leaf_id 목록 JSON')
    ap.add_argument('--model', default=MODEL)
    args = ap.parse_args()

    globals()['MODEL'] = args.model

    env = {}
    for line in (REPO / '.env').read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    key = env.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    if not key:
        sys.exit('GEMINI_API_KEY 없음')

    base = STUDY / args.subject / 'lectures'
    align = json.loads((base / 'align.json').read_text(encoding='utf-8'))
    # 필기노트가 있는 과목(경제학)만 쪽 매핑을 쓴다. 없으면 빈 껍데기로 두고 전사·판서만 쓴다.
    nm_path = base / 'note_map.json'
    note_map = (json.loads(nm_path.read_text(encoding='utf-8'))
                if nm_path.exists() else {'pages': [], 'by_leaf': {}})
    pdf = args.pdf or (DEFAULT_PDF if args.subject == 'economics' else None)
    pages_text = {p['page']: p['text'] for p in extract_note_pages(pdf)} if pdf else {}
    sections = load_leaf_sections(args.subject)
    tdir, kdir = WORK / 'transcripts' / args.subject, WORK / 'keyframes' / args.subject

    targets = [lid for lid in align['by_leaf'] if lid in sections]
    if args.only:
        targets = [t for t in targets if t == args.only]
    if args.leaves_file:
        want = set(json.loads(Path(args.leaves_file).read_text(encoding='utf-8')))
        targets = [t for t in targets if t in want]
    if args.limit:
        targets = targets[:args.limit]
    print(f'대상 관 {len(targets)}개 · 모델 {MODEL}\n')

    by_unit = {}
    tot_in = tot_out = 0
    t0 = time.time()
    for n, lid in enumerate(targets, 1):
        sec = sections[lid]
        b = build(args.subject, lid, pages_text, note_map, align, tdir, kdir)
        if not b['lectures']:
            print(f'  [{n}/{len(targets)}] 건너뜀(강의 구간 없음) {sec["path"][-1] if sec["path"] else lid}')
            continue

        transcript = '\n\n'.join(f"[{l['no']}강 {l['ts']}]\n{l['transcript']}" for l in b['lectures'])
        if len(transcript) > MAX_TRANSCRIPT:
            half = MAX_TRANSCRIPT // 2
            transcript = transcript[:half] + '\n\n…(중략)…\n\n' + transcript[-half:]
        frames = [f['file'] for l in b['lectures'] for f in l['frames']][:MAX_FRAMES]

        prompt = (
            f"{STYLE}\n{SUBJECT_RULES.get(args.subject, '')}\n\n"
            f"[관] {' / '.join(sec['path'])}\n\n"
            f"[교재 소제목 목록 — 앵커에 그대로 쓸 것]\n"
            + '\n'.join(f'- {h}' for h in sec['heads']) + "\n\n"
            f"[교재 본문 — 절대 반복하지 말 것]\n{sec['body'][:14000]}\n\n"
            + (f"[강사 필기노트 — 화면에 띄운 문서]\n{b['note_text'][:8000]}\n\n"
               if b['note_text'].strip() else "")
            +
            f"[강의 전사]\n{transcript}\n\n"
            f"첨부한 이미지는 그 구간의 판서 화면입니다. 수식·도식이 텍스트에 없으면 여기서 읽어 반영하세요."
        )

        try:
            md, usage = call_gemini(key, prompt, frames)
        except Exception as e:
            print(f'  [{n}/{len(targets)}] ❌ 실패 {e}')
            continue
        md = re.sub(r'^```(?:markdown)?\s*|\s*```$', '', md.strip())
        md = normalize_mate(md)
        if not md:
            print(f'  [{n}/{len(targets)}] ❌ 빈 응답')
            continue

        by_unit.setdefault(sec['unit_code'], []).append((lid, sec['path'], md))
        tot_in += usage.get('promptTokenCount', 0)
        tot_out += usage.get('candidatesTokenCount', 0)
        title = sec['path'][-1] if sec['path'] else lid
        print(f"  [{n}/{len(targets)}] {title[:34]:<34} {len(md):>5}자 · 판서 {len(frames)}장 · "
              f"in {usage.get('promptTokenCount', 0):,}")

    out_dir = base / 'notes'
    out_dir.mkdir(parents=True, exist_ok=True)
    header = ("<!-- 강의에서 뽑아 교재 문체로 다듬은 보충 본문.\n"
              "     화면에서는 교재와 한 흐름으로 합쳐지므로 \"강사는/강의에서는\" 같은 말은 쓰지 않는다.\n"
              "     [43강 39:45] 는 되짚기용 표시일 뿐 화면에는 나오지 않는다.\n"
              "     > 🐶 = 복습 메이트의 학습 조언. 내용 설명이 아니라 \"어떻게 공부할지\"만 담는다.\n"
              "     <!-- after: … --> 는 교재 어느 소제목 뒤에 들어갈지를 가리키는 앵커다. -->\n")
    for unit, items in by_unit.items():
        dst = out_dir / f'{unit}.{args.phase}.md'
        new = {lid: (path, md) for lid, path, md in items}
        blocks = []          # (leaf_id, 본문블록)
        if dst.exists():
            # 기존 파일의 관 순서를 지키고, 재생성한 관만 갈아끼운다.
            # 통째로 다시 쓰면 이번에 안 돌린 관이 사라진다.
            old = dst.read_text(encoding='utf-8')
            for chunk in re.split(r'(?=<!-- leaf: )', old):
                m = re.match(r'<!-- leaf: (\S+?) -->', chunk)
                if m:
                    blocks.append((m.group(1), chunk))
        seen = {lid for lid, _ in blocks}
        for lid, (path, md) in new.items():
            block = f"<!-- leaf: {lid} -->\n## {path[-1] if path else lid}\n\n{md}\n\n"
            if lid in seen:
                blocks = [(l, block if l == lid else c) for l, c in blocks]
            else:
                blocks.append((lid, block))
        dst.write_text(header + '\n' + '\n'.join(c for _, c in blocks), encoding='utf-8')

    el = time.time() - t0
    print(f'\n유닛 {len(by_unit)}개 파일 저장 · {el / 60:.1f}분')
    print(f'토큰 in {tot_in:,} / out {tot_out:,}')


if __name__ == '__main__':
    main()
