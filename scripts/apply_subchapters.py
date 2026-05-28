#!/usr/bin/env python3
"""각 문제에 subchapter 필드 자동 매핑 — topic 키워드 기반."""
import json
from pathlib import Path

DATA_DIR = Path('viewer/public/data/essay/practice')

# 단원별 subchapter 분류 (키워드 매칭)
TAXONOMY = {
    '2a': {
        'subchapters': [
            {'id': '2a-1', 'title': '공시지가기준법',
             'keywords': ['공시지가', '비교표준지', '시점수정', '지역요인', '개별요인', '그밖의요인',
                          '6대 조건', '6대 요인', '표준지']},
            {'id': '2a-2', 'title': '거래사례비교법',
             'keywords': ['거래사례', '사정보정', '비준가액', '사례 선정', '사례 적격', '비교법']},
            {'id': '2a-3', 'title': '원가법 (토지·건물)',
             'keywords': ['원가법', '재조달원가', '적산가액', '정액법', '정률법', '감가수정', '잔가율',
                          '내용연수', '관찰감가', '주체·부대', '경제적 감가', '기능적 감가', '물리적 감가',
                          '복합 감가', '복합부동산', '토지잔여법', '건물잔여법']},
            {'id': '2a-4', 'title': '수익환원법 (기초)',
             'keywords': ['수익환원', '환원이율', 'NOI', 'DCF', '직접환원', '시장추출', '요소구성',
                          '투자결합', '부채감당', '할인율', '매각가치', '매각환원']},
            {'id': '2a-5', 'title': '시산조정·일반론',
             'keywords': ['시산조정', '시산가액', '3방식', '평가절차', '평가방식', '평가 절차', '평가 방식',
                          '가격형성', '기준시점', '시장가치', '공정가치', '가치 개념', '평가 윤리',
                          '평가보고서', '소송감정', '담보평가', '매매계약 검증', '평가 효력']},
            {'id': '2a-6', 'title': '보상평가 (토지·잔여지)',
             'keywords': ['보상', '편입', '잔여지', '잔여 토지', '구분지상권', '입체이용', '공공용지',
                          '사실상 도로', '도시계획도로', '미지급용지', '도로 확장']},
            {'id': '2a-7', 'title': '보상평가 (영업·영농·동산)',
             'keywords': ['영업손실', '휴업', '폐업', '영농손실', '실제소득', '통계소득',
                          '분묘', '이장', '농작물', '과수', '입목', '시장가 역산', '가식',
                          '영업장', '영업', '영농']},
            {'id': '2a-8', 'title': '도시정비',
             'keywords': ['정비사업', '도시정비', '비례율', '권리가액', '분담금', '청산금', '청산',
                          '종전자산', '종후자산', '재개발', '재건축']},
            {'id': '2a-9', 'title': '특수 평가',
             'keywords': ['맹지', '노선가', '표준지 평가', '특수토지', '골프장', '호텔', '아파트',
                          '구분소유', '대지권', '층 효용비', '집합건물', '준공·산업단지']},
        ],
        'default': '2a-5',  # 일반론·이론
    },
    '3': {
        'subchapters': [
            {'id': '3-1', 'title': '건물 원가법',
             'keywords': ['건물 원가법', '재조달원가', '적산가액', '정액법', '정률법', '관찰감가',
                          '주체·부대', '주체 부대', '잔가율', '내용연수', '만년감가', '기능적 감가',
                          '경제적 감가', '리모델링', '원가법']},
            {'id': '3-2', 'title': '복합부동산 평가',
             'keywords': ['복합부동산', '일체 평가', '일체효용', '토지잔여법', '건물잔여법',
                          '잔여법', '일체 vs 별도', '일체가격 배분', '3방식', '시산조정',
                          '토지·건물 일체']},
            {'id': '3-3', 'title': '구분소유·집합건물',
             'keywords': ['구분소유', '집합건물', '대지권', '층 효용비', '평형 효용비', '아파트',
                          '전유면적', '공급면적', '공용부분', '오피스텔', '구분상가']},
            {'id': '3-4', 'title': '임대료 평가',
             'keywords': ['임대료', '임대사례', '적산법', '수익분석법', '기대이율', '필요제경비',
                          '보증금', '월세', '전세', '전월세 전환율', '임차권', '임대권',
                          '임대 사례', '갱신', '시장임대료', '계약임대료']},
            {'id': '3-5', 'title': '건물 비교·수익',
             'keywords': ['건물 거래사례', '건물 비교법', 'DCF', '수익환원', '직접환원',
                          'NOI', '환원이율', '할인율', '매각가치', '호텔', '쇼핑센터',
                          '임대 매장', '임대 오피스', '임대 상가']},
        ],
        'default': '3-5',
    },
    '6a': {
        'subchapters': [
            {'id': '6a-1', 'title': '토지보상 기본·원칙',
             'keywords': ['보상 원칙', '토지보상법', '시행규칙', '사업인정', '협의', '재결']},
            {'id': '6a-2', 'title': '토지 평가 (보상)',
             'keywords': ['보상 토지', '공시지가', '그밖의요인', '비교표준지']},
        ],
        'default': '6a-1',
    },
    '6b': {
        'subchapters': [
            {'id': '6b-1', 'title': '공법상 제한',
             'keywords': ['공법상 제한', '도시계획', '용도지역', '제한']},
            {'id': '6b-2', 'title': '특수 보상 (잔여지·미지급)',
             'keywords': ['잔여지', '미지급', '구분지상권', '입체이용']},
        ],
        'default': '6b-1',
    },
    '7': {
        'subchapters': [
            {'id': '7-1', 'title': '건축물 보상',
             'keywords': ['건축물', '건물 보상', '잔존', '이전비']},
            {'id': '7-2', 'title': '영업·영농 보상',
             'keywords': ['영업', '영농', '휴업', '폐업', '농작물', '과수', '입목', '분묘']},
            {'id': '7-3', 'title': '이전·이주 보상',
             'keywords': ['이주', '이전', '주거이전']},
        ],
        'default': '7-2',
    },
    '8a': {
        'subchapters': [
            {'id': '8a-1', 'title': '담보평가',
             'keywords': ['담보', 'LTV', '저당', '경매']},
            {'id': '8a-2', 'title': '경매·소송 평가',
             'keywords': ['경매', '소송', '법원', '감정인']},
            {'id': '8a-3', 'title': '국공유재산·기타',
             'keywords': ['국공유', '국유', '공유', '매각']},
        ],
        'default': '8a-3',
    },
    '8b': {
        'subchapters': [
            {'id': '8b-1', 'title': '표준지 공시지가',
             'keywords': ['표준지', '공시지가', '평가절차']},
            {'id': '8b-2', 'title': '정비사업 (종전·종후·분담)',
             'keywords': ['정비', '재개발', '재건축', '종전', '종후', '비례율', '분담금']},
            {'id': '8b-3', 'title': '불의타·기타',
             'keywords': ['불의타', '기타']},
        ],
        'default': '8b-3',
    },
    '4': {
        'subchapters': [
            {'id': '4-1', 'title': '유형별 평가', 'keywords': []},
        ],
        'default': '4-1',
    },
    '5': {
        'subchapters': [
            {'id': '5-1', 'title': '비가치추계 (시산조정·검증)',
             'keywords': ['비가치', '검증', '시산']},
            {'id': '5-2', 'title': '기업가치',
             'keywords': ['기업', '주식', '비상장', '기업가치']},
            {'id': '5-3', 'title': '무형자산',
             'keywords': ['무형', '영업권', '특허', '브랜드', '상표', '저작권']},
        ],
        'default': '5-1',
    },
}


def classify(q, chapter):
    """문제의 topic·body 텍스트에서 키워드 매칭하여 subchapter 결정."""
    tax = TAXONOMY.get(chapter)
    if not tax:
        return None
    text = (q.get('topic', '') + ' ' + q.get('body', '')[:500] + ' ' + ' '.join(q.get('keyPoints', []))).lower()
    # 각 subchapter의 키워드 점수 계산
    best = None
    best_score = 0
    for sc in tax['subchapters']:
        score = sum(1 for kw in sc['keywords'] if kw.lower() in text)
        if score > best_score:
            best_score = score
            best = sc['id']
    return best if best else tax['default']


def main():
    summary = {}
    for chapter in TAXONOMY:
        path = DATA_DIR / f'{chapter}.json'
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding='utf-8'))
        counts = {}
        for q in data['questions']:
            sc = classify(q, chapter)
            q['subchapter'] = sc
            counts[sc] = counts.get(sc, 0) + 1
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        summary[chapter] = counts
        print(f"\n=== 단원 {chapter} ===")
        for sc_id, cnt in sorted(counts.items()):
            title = next((s['title'] for s in TAXONOMY[chapter]['subchapters'] if s['id'] == sc_id), '?')
            print(f"  {sc_id} {title:30s} : {cnt}개")

    # manifest에 subchapter 목록 추가
    manifest_path = DATA_DIR / 'manifest.json'
    m = json.loads(manifest_path.read_text(encoding='utf-8'))
    for c in m['chapters']:
        cid = c['id']
        if cid in TAXONOMY:
            c['subchapters'] = TAXONOMY[cid]['subchapters']
    manifest_path.write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')
    print('\nmanifest.json subchapter 목록 추가 완료')


if __name__ == '__main__':
    main()
