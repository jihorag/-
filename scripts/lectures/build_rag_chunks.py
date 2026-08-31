# 교재 md → 검색용 청크. 심화 탭의 RAG 가 이걸 읽는다.
#
# 왜 필요한가: 지금 심화 튜터는 단원 md 를 통째로 프롬프트에 넣는다(평균 10만 자).
# 질문이 무엇이든 같은 덩어리가 가고, 관련 없는 부분까지 매번 들어간다.
# 소제목 단위로 쪼개 두면 질문에 관련된 것만 골라 넣을 수 있다.
#
# 임베딩을 쓰지 않는다 — 제공자마다 달라서 제공자를 바꾸면 인덱스를 다시 만들어야
# 한다. 어절과 2-gram 만으로도 시험 용어(「한계대체율」·「구축효과」)는 그대로 잡힌다.
import json
import os
import re
import sys

# 이보다 짧은 토막은 검색에 쓸 수 없다. 제목만 있고 본문이 없는 자리다.
MIN_CHARS = 10
HEAD = re.compile(r'^(#{3,4})\s+(.+?)\s*$', re.M)


def split_chunks(md):
    """소제목(### / ####) 단위로 쪼갠다. 제목 경로를 보존한다."""
    heads = list(HEAD.finditer(md))
    out = []
    for i, m in enumerate(heads):
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(md)
        body = md[start:end].strip()
        if len(body) < MIN_CHARS:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        # 제목 경로 — 이 청크 위쪽에서 더 얕은 제목을 거슬러 올라간다.
        path = [title]
        lv = level
        for prev in reversed(heads[:i]):
            plv = len(prev.group(1))
            if plv < lv:
                path.insert(0, prev.group(2).strip())
                lv = plv
        out.append({'path': path, 'text': body})
    return out


def terms_of(text):
    """어절 + 2-gram. 형태소 분석기 없이 한국어 용어를 잡는 최소 장치."""
    words = [w for w in re.split(r'[^0-9A-Za-z가-힣]+', text) if len(w) >= 2]
    grams = set(words)
    for w in words:
        for k in range(len(w) - 1):
            grams.add(w[k:k + 2])
    return sorted(grams)


def build(unit_path, out_path):
    md = open(unit_path, encoding='utf-8').read()
    unit = os.path.splitext(os.path.basename(unit_path))[0]
    chunks = []
    for n, c in enumerate(split_chunks(md)):
        chunks.append({
            'id': '%s#%d' % (unit, n),
            'path': c['path'],
            'text': c['text'],
            'terms': terms_of(c['path'][-1] + ' ' + c['text']),
        })
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump({'unit': unit, 'chunks': chunks},
              open(out_path, 'w', encoding='utf-8'), ensure_ascii=False)
    return len(chunks)


def main(subject):
    src_dir = 'viewer/public/data/study/%s/units' % subject
    out_dir = 'viewer/public/data/study/%s/rag' % subject
    total = 0
    for name in sorted(os.listdir(src_dir)):
        if not name.endswith('.md') or name.endswith('.orig'):
            continue
        n = build(os.path.join(src_dir, name),
                  os.path.join(out_dir, name[:-3] + '.chunks.json'))
        print('%s → %d청크' % (name, n))
        total += n
    print('합계 %d청크' % total)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'economics')
