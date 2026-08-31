# 교재의 「🧠 암기법」을 관 마지막 복습 메이트 대사로 옮긴다.
#
# 지금은 우측 교재 패널의 별도 탭에 있어서, 논점을 다 익힌 사람이 그 탭을 따로
# 눌러야 본다. 대화 끝에 두면 익힌 직후에 만난다.
#
# 재실행 안전 — 같은 문장이 이미 있으면 건너뛴다.
import json
import os
import re
import sys

MEM_HEAD = re.compile(r'^#{4}\s*🧠\s*암기법\s*$', re.M)
ANY_HEAD = re.compile(r'^(#{1,4})\s+(.+?)\s*$', re.M)


def extract_mnemonics(md):
    """(관 제목, 암기법 한 덩이) 목록. 암기법은 그것이 속한 `### 관` 에 붙는다.

    관마다 암기법이 따로 있으므로 단원 전체에 하나를 돌려쓰면 안 된다 —
    엉뚱한 관에 남의 암기법이 붙는다.
    """
    heads = list(ANY_HEAD.finditer(md))
    out = []
    for i, h in enumerate(heads):
        if not MEM_HEAD.match(h.group(0)):
            continue
        # 이 암기법이 속한 상위 `###` 를 거슬러 찾는다.
        owner = None
        for prev in reversed(heads[:i]):
            if len(prev.group(1)) == 3:
                owner = prev.group(2).strip()
                break
        if not owner:
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(md)
        body = md[h.end():end]
        tip = first_block(body)
        if tip:
            out.append((owner, tip))
    return out


def first_block(body):
    """`> 🔑` 블록 하나를 평문으로. 인용 기호를 떼고 최대 두 줄만 쓴다 —
    세 줄을 넘기면 마지막 말풍선이 벽이 된다."""
    lines = []
    started = False
    for raw in body.split('\n'):
        line = raw.strip()
        if line.startswith('>'):
            started = True
            lines.append(line.lstrip('>').strip())
        elif started:
            break
    lines = [x for x in lines if x]
    return '\n'.join(lines[:2]) if lines else ''


def already_has(point, text):
    for t in point.get('turns', []):
        if t.get('who') == 'mate' and t.get('text', '').strip() == text.strip():
            return True
    return False


def merge(track_path, unit_md_path):
    md = open(unit_md_path, encoding='utf-8').read()
    tips = dict(extract_mnemonics(md))       # 관 제목 → 암기법
    if not tips:
        return 0
    d = json.load(open(track_path, encoding='utf-8'))
    added = 0
    for leaf in d.get('leaves', []):
        pts = leaf.get('points') or []
        if not pts:
            continue
        title = (leaf.get('title') or '').strip()
        tip = tips.get(title)
        if not tip:
            continue                          # 짝이 없으면 넣지 않는다
        last = pts[-1]
        text = '외우는 법 — ' + tip
        if already_has(last, text):
            continue
        last.setdefault('turns', []).append({'who': 'mate', 'text': text})
        added += 1
    if added:
        json.dump(d, open(track_path, 'w', encoding='utf-8'), ensure_ascii=False)
    return added


def main(subject):
    base = 'viewer/public/data/study/%s' % subject
    tdir = os.path.join(base, 'lectures', 'track')
    total = 0
    for name in sorted(os.listdir(tdir)):
        if not name.endswith('.basic.json'):
            continue
        unit = name[:-len('.basic.json')]
        md = os.path.join(base, 'units', unit + '.md')
        if not os.path.exists(md):
            print('건너뜀(교재 없음): %s' % unit)
            continue
        n = merge(os.path.join(tdir, name), md)
        print('%s → %d관에 추가' % (unit, n))
        total += n
    print('합계 %d관' % total)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'economics')
