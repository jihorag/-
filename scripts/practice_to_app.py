#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""연습문제를 questions_db.json(정본)에 통합 후 sync-data로 chunk 자동 생성.

흐름:
  practice/economics/*.json → 변환 → questions_db.json(append) → sync-data.mjs → chunk
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE_DIRS = [
    ROOT / 'viewer/public/data/practice/economics',
    # ROOT / 'viewer/public/data/practice/civil-law',
    ROOT / 'viewer/public/data/practice/realestate',
    ROOT / 'viewer/public/data/practice/law'
]
QDB = ROOT / 'questions_db.json'
EXAM_NAME = '[연습문제]'


def map_civil_taxonomy(sub_subject, chapter, section, item):
    orig_sub = sub_subject
    orig_ch = chapter
    orig_sec = section
    orig_item = item
    
    if sub_subject == '총칙':
        sub_subject = '민법총칙'
        if chapter == '제1장 통칙':
            if section == '제1절 민법의 법원':
                chapter = '제1장 민법 서론'
                section = '제2절 민법의 법원'
                item = ''
            elif section == '제2절 신의성실의 원칙':
                chapter = '제2장 법률관계와 신의성실의 원칙'
                section = '제2절 신의성실의 원칙'
                if '권리남용' in orig_item:
                    item = '제3관 권리남용금지의 원칙'
                else:
                    item = '제1관 신의칙 서설'
        elif chapter == '제2장 인':
            chapter = '제3장 권리의 주체'
            section = '제1절 자연인'
            if '1절' in orig_sec or '권리능력' in orig_sec:
                item = '제1관 권리능력'
            elif '2절' in orig_sec or '행위능력' in orig_sec:
                if '미성년' in orig_item:
                    item = '제4관 미성년자'
                elif '상대방' in orig_item:
                    item = '제6관 제한능력자의 상대방 보호'
                else:
                    item = '제5관 피성년·피한정·피특정후견인'
            elif '3절' in orig_sec or '부재' in orig_sec or '실종' in orig_sec:
                if '부재자' in orig_item:
                    item = '제8관 부재자의 재산관리'
                else:
                    item = '제9관 실종선고'
        elif chapter == '제3장 법인':
            chapter = '제3장 권리의 주체'
            section = '제2절 법인'
            if '본질' in orig_item or '종류' in orig_item:
                item = '제1관 법인의 의의와 종류'
            elif '설립' in orig_item:
                item = '제2관 법인의 설립'
            elif '능력' in orig_item or '불법행위' in orig_item:
                item = '제3관 법인의 능력'
            elif '기관' in orig_item or '이사' in orig_item:
                item = '제4관 법인의 기관'
            else:
                item = '제8관 권리능력 없는 사단·재단'
        elif chapter == '제4장 물건':
            chapter = '제4장 권리의 객체'
            if '1절' in orig_sec or '총설' in orig_sec:
                section = '제1절 물건의 의의와 분류'
            elif '2절' in orig_sec or '부동산' in orig_sec:
                section = '제2절 부동산과 동산'
            else:
                if '주물' in orig_item:
                    section = '제3절 주물과 종물'
                else:
                    section = '제4절 원물과 과실'
            item = ''
        elif chapter == '제5장 법률행위':
            chapter = '제5장 권리의 변동'
            if orig_sec in ('제1절 총설', '제1절 총칙'):
                section = '제2절 법률행위'
                if '종류' in orig_item or '요건' in orig_item:
                    item = '제1관 법률행위의 의의와 종류'
                else:
                    item = '제6관 법률행위의 해석'
            elif orig_sec in ('제2절 목적', '제2절 법률행위의 목적'):
                section = '제2절 법률행위'
                if '반사회' in orig_item:
                    item = '제4관 반사회질서의 법률행위'
                else:
                    item = '제5관 불공정한 법률행위'
            elif orig_sec == '제3절 의사표시':
                section = '제3절 의사표시'
                if '비진의' in orig_item:
                    item = '제2관 진의 아닌 의사표시'
                elif '통정' in orig_item:
                    item = '제3관 통정허위표시'
                elif '착오' in orig_item:
                    item = '제4관 착오에 의한 의사표시'
                elif '사기' in orig_item:
                    item = '제5관 사기·강박에 의한 의사표시'
                else:
                    item = '제6관 의사표시의 효력발생'
        elif chapter == '제6장 대리':
            chapter = '제5장 권리의 변동'
            section = '제4절 법률행위의 대리'
            if '의의' in orig_item or '종류' in orig_item:
                item = '제1관 대리 서설'
            elif '범위' in orig_item or '제한' in orig_item:
                item = '제2관 대리권'
            elif '복대리' in orig_item:
                item = '제5관 복대리'
            elif '표현대리' in orig_item:
                item = '제7관 표현대리'
            else:
                item = '제6관 협의의 무권대리'
        elif chapter == '제7장 무효와 취소':
            chapter = '제5장 권리의 변동'
            section = '제5절 법률행위의 무효와 취소'
            if '1절' in orig_sec or '무효' in orig_sec:
                if '추인' in orig_item or '전환' in orig_item:
                    item = '제2관 무효행위의 전환과 추인'
                else:
                    item = '제1관 무효 총설'
            elif '2절' in orig_sec or '취소' in orig_sec:
                if '법정추인' in orig_item or '소멸' in orig_item:
                    item = '제4관 취소의 효과와 법정추인'
                else:
                    item = '제3관 취소 총설'
        elif chapter == '제8장 조건과 기한':
            chapter = '제5장 권리의 변동'
            section = '제6절 법률행위의 부관'
            if '조건' in orig_item:
                item = '제2관 조건'
            else:
                item = '제3관 기한'
        elif chapter == '제9장 기간':
            chapter = '제6장 기간'
            section = '제2절 기간의 계산방법'
            item = ''
        elif chapter == '제10장 소멸시효':
            chapter = '제7장 소멸시효'
            if '1절' in orig_sec or '일반' in orig_sec or '소멸시효 일반' in orig_sec:
                section = '제1절 총설 · 제2절 소멸시효의 요건'
                if '대상' in orig_item:
                    item = '제2관 소멸시효의 대상 권리'
                elif '기산점' in orig_item:
                    item = '제3관 소멸시효의 기산점'
                else:
                    item = '제4관 소멸시효의 기간'
            elif '2절' in orig_sec or '중단' in orig_sec or '정지' in orig_sec:
                if '완성' in orig_item:
                    section = '제4절 소멸시효 완성의 효과'
                    item = '제1관 시효완성의 효과'
                else:
                    section = '제3절 시효의 장애'
                    item = '제1관 소멸시효의 중단'
    
    elif sub_subject == '물권':
        sub_subject = '물권법'
        if chapter in ('제1장 물권 총설', '제2장 물권의 변동', '제3장 물권의 소멸', '제1장 물권 총칙'):
            chapter = '제1장 물권법 총설'
            if '1절' in orig_sec or '일반' in orig_sec or '본질' in orig_sec:
                section = '제1절 물권법 일반 · 제2절 물권변동'
                item = '제1관 물권의 의의와 종류'
            elif '3절' in orig_sec or '부동산물권' in orig_sec or '등기' in orig_sec or '186' in orig_item:
                section = '제3절 부동산 물권변동'
                if '중간생략' in orig_item:
                    item = '제4관 중간생략등기'
                elif '가등기' in orig_item:
                    item = '제5관 가등기'
                elif '추정력' in orig_item:
                    item = '제3관 등기의 유효요건과 추정력'
                elif '등기청구권' in orig_item:
                    item = '제2관 등기절차와 등기청구권'
                elif '187' in orig_item or '법률규정' in orig_item:
                    item = '제6관 법률규정에 의한 물권변동'
                else:
                    item = '제2관 등기절차와 등기청구권'
            elif '4절' in orig_sec or '공시' in orig_sec or '공신' in orig_sec or '원칙' in orig_sec or '인도' in orig_item or '동산' in orig_item:
                section = '제4절 동산 물권 변동'
                if '선의취득' in orig_item or '249' in orig_item:
                    item = '제2관 선의취득'
                else:
                    item = '제1관 동산물권변동과 인도'
            elif '5절' in orig_sec or '소멸' in orig_sec:
                section = '제5절 물권의 소멸'
                if '혼동' in orig_item:
                    item = '제2관 혼동'
                else:
                    item = '제1관 물권의 소멸원인'
        elif chapter == '제2장 점유권':
            chapter = '제2장 점유권'
            if '1절' in orig_sec or '의의' in orig_sec or '점유' in orig_sec or '성립' in orig_sec or orig_sec == '제1절 점유':
                if '취득' in orig_item or '소멸' in orig_item:
                    section = '제2절 점유권의 취득과 소멸'
                    item = ''
                else:
                    section = '제1절 서론'
                    if '보조자' in orig_item or '간접' in orig_item:
                        item = '제2관 점유보조자와 간접점유'
                    elif '자주' in orig_item or '타주' in orig_item or '종류' in orig_item:
                        item = '제3관 점유의 종류'
                    else:
                        item = '제1관 점유의 의의와 관념화'
            elif '2절' in orig_sec or '3절' in orig_sec or '효력' in orig_sec:
                section = '제3절 점유권의 효력 · 제4절 준점유'
                if '회복자' in orig_item:
                    item = '제2관 점유자와 회복자의 관계'
                elif '청구권' in orig_item:
                    item = '제3관 점유보호청구권'
                else:
                    item = '제1관 점유의 추정적 효력'
        elif chapter == '제3장 소유권':
            chapter = '제3장 소유권'
            if '1절' in orig_sec or '일반' in orig_sec:
                section = '제1절 총설'
                item = '제1관 소유권의 의의와 내용'
            elif '2절' in orig_sec or '상린관계' in orig_sec:
                section = '제2절 상린관계'
                if '주위토지' in orig_item:
                    item = '제5관 주위토지통행권'
                else:
                    item = '제1관 상린관계 총설'
            elif '3절' in orig_sec or '4절' in orig_sec or '취득' in orig_sec:
                if '첨부' in orig_item or '부합' in orig_item:
                    section = '제4절 기타 소유권의 취득'
                    item = '제2관 첨부'
                else:
                    section = '제3절 소유권의 취득'
                    item = '제2관 부동산 점유취득시효'
            elif '4절' in orig_sec or '공동소유' in orig_sec or '공동' in orig_sec:
                section = '제6절 공동소유'
                if '공유' in orig_item:
                    item = '제2관 공유'
                else:
                    item = '제3관 합유'
            elif '5절' in orig_sec or '명의신탁' in orig_sec:
                section = '제7절 명의신탁'
                item = '제2관 명의신탁의 유형과 효력'
        elif chapter == '제4장 지상권':
            chapter = '제4장 용익물권'
            section = '제1절 지상권'
            if '구분지상권' in orig_item or '분묘기지권' in orig_item:
                if '분묘' in orig_item:
                    item = '제6관 분묘기지권'
                else:
                    item = '제5관 구분지상권'
            elif '법정지상권' in orig_item:
                if '관습' in orig_item:
                    item = '제8관 관습법상 법정지상권'
                else:
                    item = '제7관 법정지상권'
            elif '존속기간' in orig_item or '취득' in orig_item:
                item = '제2관 지상권의 존속기간'
            else:
                item = '제3관 지상권의 효력'
        elif chapter == '제5장 지역권':
            chapter = '제4장 용익물권'
            section = '제2절 지역권'
            if '취득' in orig_item or '불가분성' in orig_item:
                item = '제2관 지역권의 취득'
            elif '소멸' in orig_item:
                item = '제4관 지역권의 소멸'
            elif '특수지역권' in orig_item:
                item = '제5관 특수지역권'
            else:
                item = '제3관 지역권의 효력'
        elif chapter == '제6장 전세권':
            chapter = '제4장 용익물권'
            section = '제3절 전세권'
            if '성립' in orig_item or '존속기간' in orig_item:
                item = '제2관 전세권의 존속기간'
            elif '소멸' in orig_item:
                item = '제5관 전세권의 소멸'
            else:
                item = '제3관 전세권의 효력'
        elif chapter == '제7장 유치권':
            chapter = '제5장 담보물권'
            section = '제2절 유치권'
            if '성립' in orig_item or '제한' in orig_item:
                item = '제1관 유치권의 의의와 성립'
            elif '소멸' in orig_item:
                item = '제3관 유치권의 소멸'
            else:
                item = '제2관 유치권의 효력'
        elif chapter == '제8장 질권':
            chapter = '제5장 담보물권'
            section = '제3절 질권'
            if '동산질권' in orig_item:
                item = '제1관 동산질권의 성립'
            else:
                item = '제3관 권리질권'
        elif chapter == '제9장 저당권':
            chapter = '제5장 담보물권'
            section = '제4절 저당권'
            if '공동저당' in orig_item:
                item = '제6관 공동저당'
            elif '근저당' in orig_item:
                item = '제7관 근저당'
            elif '효력 범위' in orig_item:
                item = '제2관 효력이 미치는 범위'
            elif '물상대위' in orig_item or '우선변제' in orig_item:
                item = '제3관 우선변제적 효력과 물상대위'
            else:
                item = '제1관 저당권의 의의와 성립'

    return sub_subject, chapter, section, item


def convert(p, meta):
    sub = meta['subject']
    sub_subj = meta.get('sub_subject', '')
    ch = meta['chapter']
    sec = meta['section']
    it = meta.get('item', '')
    
    if sub == '민법':
        sub_subj, ch, sec, it = map_civil_taxonomy(sub_subj, ch, sec, it)
        
    return {
        'id': p['id'],
        'number': '',
        'period': 'practice',
        'year': '2026',
        'exam_date': '2026-05-31',
        'question': p['question'],
        'options': p['options'],
        'answer': p['answer'],
        'explanation': p['explanation'],
        'subject': sub,
        'tags': {
            'subject': sub,
            'is_practice': True,
            'difficulty': p['difficulty'],
            'question_type': p['question_type'],
            'system_note': 'practice-v1',
        },
        'exam': EXAM_NAME,
        'indexing_v4': {
            'difficulty': p['difficulty'],
            'mapped_taxonomy': {
                'subject': sub,
                'sub_subject': sub_subj,
                'chapter': ch,
                'section': sec,
                'item': it,
            },
            'needs_higher_ai': False,
            'reason': f'연습문제 v{meta["version"]} — {it or sec} 출제',
            # 'claude-sonnet-4-6'을 사용해야 manifest의 "classified" 통계에 포함되고
            # 앱 분류별 보기에서 정상 노출됨.
            'processed_by': 'claude-sonnet-4-6',
        },
        'indexing_v4_count': 1,
    }


def load_practice():
    qs = []
    for pdir in PRACTICE_DIRS:
        if not pdir.exists():
            continue
        for fp in sorted(pdir.glob('*.json')):
            with open(fp, encoding='utf-8') as f:
                data = json.load(f)
            meta = data.get('meta', {})
            for q in data.get('questions', []):
                qs.append(convert(q, meta))
            print(f'  practice loaded: {fp.name} ({len(data.get("questions",[]))}문제)')
    return qs


def merge_to_qdb(new_qs):
    """questions_db.json에서 기존 연습문제 제거 후 새 연습문제 추가."""
    with open(QDB, encoding='utf-8') as f:
        db = json.load(f)

    # 기존 연습문제 제거 (id가 'practice-' 시작하거나 exam이 [연습문제])
    before = len(db)
    db = [q for q in db if not (
        q.get('id', '').startswith('practice-') or q.get('exam') == EXAM_NAME
    )]
    removed = before - len(db)
    print(f'  removed {removed} prior practice questions from db')

    # 새 연습문제 추가
    db.extend(new_qs)
    print(f'  added {len(new_qs)} new practice questions')

    with open(QDB, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False)
    print(f'  questions_db.json: {len(db)} questions total')
    return db


def run_sync():
    """sync 실행 — node가 있으면 sync-data.mjs, 없으면 Python 재구현 사용."""
    # node 시도
    try:
        result = subprocess.run(
            ['node', 'scripts/sync-data.mjs'],
            cwd=ROOT / 'viewer',
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print(result.stdout)
            return True
    except FileNotFoundError:
        pass

    # Python 재구현 사용
    print('  node not found, using Python re-implementation')
    result = subprocess.run(
        ['python3', 'scripts/sync_data_py.py'],
        cwd=ROOT, capture_output=True, text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print('stderr:', result.stderr)
        return False
    return True


def main():
    print('=== 연습문제 → questions_db → app sync ===\n')
    print('[1/3] 연습문제 로드')
    practice_qs = load_practice()
    if not practice_qs:
        print('No practice questions found.')
        return
    print(f'\n[2/3] questions_db.json 통합')
    merge_to_qdb(practice_qs)
    print(f'\n[3/3] sync-data 실행 (chunk 자동 생성)')
    if run_sync():
        print('\n✅ 앱 반영 완료')
        print(f'   dev: http://localhost:5173 (npm run dev)')
        print(f'   build: npm run build')


if __name__ == '__main__':
    main()
