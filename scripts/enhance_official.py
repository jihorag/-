#!/usr/bin/env python3
"""
실문제(기출) 전체에 keyPoints + difficulty 메타 자동 부착.

추출 로직:
1) 법조문 reference: 본문·답안에서 정규표현식 매칭 (감칙, 토지보상법, 시행규칙 등)
2) 핵심 개념 keyword: 단원별 사전 정의 keyword 중 본문/답안에 등장하는 것
3) 평가방식: 공시지가기준법·거래사례비교법·원가법·수익환원법 등
4) difficulty: 배점 기반 추정 (10-15점=2, 16-25점=3, 26-35점=4, 36+점=5)

출력: viewer/public/data/essay/practice/<chapter>.json 직접 수정
manifest는 별도 갱신 안 함 (count는 같음)
"""
import re
import json
from pathlib import Path
from collections import Counter

DATA_DIR = Path('viewer/public/data/essay/practice')

# ─────────── 법조문 정규표현식 ───────────
LEGAL_PATTERNS = [
    (re.compile(r'감칙\s*제\s*(\d+)\s*조(?:\s*제\s*(\d+)\s*항)?'),
     lambda m: f'감칙 제{m.group(1)}조' + (f' 제{m.group(2)}항' if m.group(2) else '')),
    (re.compile(r'감정평가에\s*관한\s*규칙\s*제\s*(\d+)\s*조'),
     lambda m: f'감칙 제{m.group(1)}조'),
    (re.compile(r'토지보상법\s*제\s*(\d+)\s*조(?:\s*제\s*(\d+)\s*항)?'),
     lambda m: f'토지보상법 제{m.group(1)}조' + (f' 제{m.group(2)}항' if m.group(2) else '')),
    (re.compile(r'공익사업을\s*위한\s*토지\s*등의\s*취득\s*및\s*보상에\s*관한\s*법률\s*제\s*(\d+)\s*조'),
     lambda m: f'토지보상법 제{m.group(1)}조'),
    (re.compile(r'(?:토지보상법\s*)?시행규칙\s*제\s*(\d+)\s*조(?:의(\d+))?'),
     lambda m: f'시행규칙 제{m.group(1)}조' + (f'의{m.group(2)}' if m.group(2) else '')),
    (re.compile(r'(?:토지보상법\s*)?시행령\s*제\s*(\d+)\s*조'),
     lambda m: f'시행령 제{m.group(1)}조'),
    (re.compile(r'국토(?:의\s*계획\s*및\s*이용에\s*관한\s*법률|계획법)\s*제\s*(\d+)\s*조'),
     lambda m: f'국토계획법 제{m.group(1)}조'),
    (re.compile(r'택지개발(?:촉진)?법\s*제\s*(\d+)\s*조'),
     lambda m: f'택지개발촉진법 제{m.group(1)}조'),
    (re.compile(r'도시(?:\s*및\s*주거환경)?정비법\s*제\s*(\d+)\s*조'),
     lambda m: f'도시정비법 제{m.group(1)}조'),
    (re.compile(r'산업(?:입지\s*및\s*개발에\s*관한\s*법률|입지법)\s*제\s*(\d+)\s*조'),
     lambda m: f'산업입지법 제{m.group(1)}조'),
    (re.compile(r'부동산\s*가격공시(?:에\s*관한\s*법률|법)\s*제\s*(\d+)\s*조'),
     lambda m: f'부동산가격공시법 제{m.group(1)}조'),
    (re.compile(r'헌법\s*제\s*(\d+)\s*조(?:\s*제\s*(\d+)\s*항)?'),
     lambda m: f'헌법 제{m.group(1)}조' + (f' 제{m.group(2)}항' if m.group(2) else '')),
]

# ─────────── 단원별 핵심 개념 keyword ───────────
# 본문·답안에 등장하면 keyPoint로 추가
CHAPTER_KEYWORDS = {
    '2a': [
        # 평가방식
        '공시지가기준법', '거래사례비교법', '원가법',
        # 핵심 절차
        '비교표준지', '시점수정', '지가변동률', '생산자물가지수',
        '지역요인', '개별요인', '그 밖의 요인', '사정보정',
        '재조달원가', '정액법', '정률법', '잔존가율',
        # 공법상 제한
        '도시계획시설', '저촉', '공법상 제한',
        # 기타
        '인근지역', '유사지역', '정상가격', '시산가액',
        '배분법', '금융조건 보정', '현금등가액',
    ],
    '2b': [
        '수익환원법', '직접환원법', 'DCF', 'NOI',
        '순수익', '순영업소득', '환원이율', '할인율',
        '임대료', '임료', '시장임대료', '계약임대료',
        '공실률', '임대보증금', '운영경비',
    ],
    '3': [
        '건물 평가', '복합부동산', '구분소유',
        '재조달원가', '감가수정', '정액법', '정률법',
        '경과연수', '잔존내용연수', '잔존가율',
        '주체부분', '부대부분',
        '임대료', '계약임대료', '시장임대료',
        '구분소유권', '대지권', '집합건물',
    ],
    '4': [
        '유형별 평가', '기계기구', '광업권',
        '농지', '임야', '잡종지',
        '특수토지', '비특수 부동산',
        '구분지상권', '지상권',
    ],
    '5': [
        '비가치추계', '기업가치', '비상장주식',
        '무형자산', '영업권', '특허권', '실용신안권',
        '저작권', '상표권', '저당가치',
        '담보가치', '경매', '소송감정',
        '수정재무상태표', 'EVA', '자기자본가치',
    ],
    '6a': [
        # 보상 기본
        '적용공시지가', '사업인정의제일', '개발이익 배제',
        '정상가격', '완전보상', '시가주의', '적정가격',
        # 절차
        '협의 보상', '재결', '이의재결', '잔여지',
        '비교표준지', '시점수정', '지가변동률',
        '그 밖의 요인', '보상선례', '평가사례',
        # 사업 유형
        '실시계획 인가', '지구지정', '추가편입', '세목고시일',
        '도시계획시설', '택지개발', '도시정비', '산업단지',
    ],
    '6b': [
        '공법상 제한', '도시계획시설', '저촉',
        '미지급용지', '편입 당시', '이용상황', '용도지역',
        '사실상의 사도', '예정된 사도', '도로법 도로',
        '잔여지', '잔여지 매수청구', '잔여건축물',
        '환매', '환매권',
    ],
    '7': [
        '건축물 보상', '이전비', '물건의 가격',
        '영업보상', '휴업보상', '폐업보상', '경영손실',
        '농업보상', '축산보상', '농업소득',
        '이주대책', '주거이전비', '이사비', '이주정착금',
        '재편입 가산금', '실농 보상', '실어 보상',
    ],
    '8a': [
        '담보평가', '대출 가능금액', '담보가치',
        '경매평가', '국공유재산', '처분',
        '소송감정', '법원 평가', '부당이득',
        '권리내역', '근저당권', '소유권', '임차권',
    ],
    '8b': [
        '표준지 공시지가', '표준지 선정',
        '정비사업', '재개발', '재건축', '리모델링',
        '관리처분계획', '종전자산', '종후자산',
        '불의의 타격', '예측 불가능', '불의타',
    ],
}

# ─────────── 평가방식·일반 키워드 (모든 단원 공통) ───────────
COMMON_KEYWORDS = [
    '감정평가', '시장가치', '기준시점',
    '평가목적', '평가방식',
]


def extract_keypoints(body, answer, chapter_id, max_count=10):
    """본문·답안에서 keyPoints 자동 추출."""
    text = (body or '') + '\n' + (answer or '')

    found = []
    seen = set()

    def add(kp):
        norm = kp.strip()
        if norm and norm not in seen:
            found.append(norm)
            seen.add(norm)

    # 1. 법조문 reference
    for pattern, formatter in LEGAL_PATTERNS:
        for m in pattern.finditer(text):
            add(formatter(m))

    # 2. 단원별 핵심 개념
    keywords = CHAPTER_KEYWORDS.get(chapter_id, []) + COMMON_KEYWORDS
    counts = Counter()
    for kw in keywords:
        if kw in text:
            counts[kw] = text.count(kw)

    # 빈도 높은 순으로 정렬해서 추가
    for kw, _ in counts.most_common():
        add(kw)

    # max_count로 제한
    return found[:max_count]


def estimate_difficulty(points):
    """배점 기반 난이도 추정."""
    if not points:
        return 3
    if points <= 15:
        return 2
    if points <= 25:
        return 3
    if points <= 35:
        return 4
    return 5


def process_chapter(chapter_id, dry_run=False):
    """단원의 official .json 파일 처리 (-generated.json은 건드리지 않음)."""
    path = DATA_DIR / f'{chapter_id}.json'
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding='utf-8'))
    enhanced = 0
    diff_added = 0
    for q in data['questions']:
        # 기존 keyPoints가 없으면 추가
        if not q.get('keyPoints'):
            kp = extract_keypoints(q.get('body', ''), q.get('modelAnswer', ''), chapter_id)
            if kp:
                q['keyPoints'] = kp
                enhanced += 1
        # 기존 difficulty가 없으면 추가
        if 'difficulty' not in q or q['difficulty'] is None:
            q['difficulty'] = estimate_difficulty(q.get('points'))
            diff_added += 1

    if not dry_run:
        path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    return {
        'chapter': chapter_id,
        'total': len(data['questions']),
        'keypoints_added': enhanced,
        'difficulty_added': diff_added,
    }


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    manifest_path = DATA_DIR / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

    total_enhanced = 0
    total_diff = 0
    total_questions = 0
    print(f'═══ 실문제 메타 강화 (dry-run: {args.dry_run}) ═══\n')
    for c in manifest['chapters']:
        result = process_chapter(c['id'], dry_run=args.dry_run)
        if result:
            print(f'  [{c["id"]}] {c["title"][:35]:<37} '
                  f'keyPoints {result["keypoints_added"]:>3}/{result["total"]:<3} '
                  f'· difficulty {result["difficulty_added"]:>3}/{result["total"]}')
            total_enhanced += result['keypoints_added']
            total_diff += result['difficulty_added']
            total_questions += result['total']
    print(f'\n전체 {total_questions}문항 중 keyPoints 추가 {total_enhanced}, difficulty 추가 {total_diff}')

    # 샘플 출력
    sample_path = DATA_DIR / '2a.json'
    if sample_path.exists():
        sample = json.loads(sample_path.read_text(encoding='utf-8'))
        q = sample['questions'][0] if sample['questions'] else None
        if q:
            print(f'\n[샘플 — 2a 첫 문항]')
            print(f'  id: {q["id"]}')
            print(f'  difficulty: {q.get("difficulty")}')
            print(f'  keyPoints ({len(q.get("keyPoints", []))}개): {q.get("keyPoints")}')


if __name__ == '__main__':
    main()
