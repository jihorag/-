#!/usr/bin/env python3
"""
단원 2a 실문제 (official) 본문/답안 교정 — LLM 직접 검토 결과 반영

검증 결과 (7개 답안 매칭 문제 중):
- r18-q1: 잘못 매칭 (답안 가격시점 2007.08.26 ≠ 본문 2010.08.26) → modelAnswer null
- r18-q2: 잘못 매칭 (답안은 담보평가, 2007.8.25 기준) → null
- r18-q3: 잘못 매칭 (답안은 보상평가, 2007.1.20 기준) → null
- r18-q4: 정확 매칭 (비상장주식 2009.12.31) → 답안 줄바꿈/형식 정리
- r25-q4: 잘못 매칭 (답안은 토지건물 시장가치, 본문은 수익률·임대권) → null
- r31-q2: 잘못 매칭 (답안은 할인율·재매도환원율, 본문은 임대료 평가) → null
- r31-q4: 잘못 매칭 (답안은 휴업보상, 본문은 공익사업 협의평가) → null

본문 cleanup: 시험지 헤더("STUDY FIGHTER 감정평가실무 N회", "1교시 100분", "공통유의사항") 제거
"""
import re
import json
from pathlib import Path

DATA_PATH = Path('viewer/public/data/essay/practice/2a.json')

# ─────────── 본문 cleanup 패턴 (모든 문제에 적용) ───────────
CLEAN_PATTERNS = [
    # 시험지 헤더
    re.compile(r'STUDY\s*FIGHTER\s*감정평가실무\s*\d+회\s*기출문제\s*', re.I),
    re.compile(r'^\s*\d+\s*$', re.M),  # 페이지 번호 단독 라인
    re.compile(r'1교시\s*감정평가실무\s*100분\s*', re.I),
    re.compile(r'※\s*공통유의사항\s*'),
    re.compile(r'1\.\s*각\s*문제는\s*해답\s*산정시\s*산식과\s*도출과정을\s*반드시\s*기재할\s*것\.\s*'),
    re.compile(r'2\.\s*단가는\s*관련\s*규정에서\s*정하고\s*있는\s*사항을\s*제외하고\s*천원미만은\s*절사,?\s*기타요인\s*보정치는\s*'),
    re.compile(r'\s*소수점\s*셋째자리까지\s*사정함\.\s*', re.I),
    re.compile(r'<!--p\.\d+-->', re.I),  # 페이지 마커
]

# ─────────── 답안 매칭 신뢰성 결정 (LLM 검토 결과) ───────────
# True = 답안 매칭 정확 / False = 잘못 매칭 → null 처리
ANSWER_MATCHED = {
    'v3-2a-r18-q1': False,   # 답안 시점 2007.08.26 ≠ 본문 2010.08.26
    'v3-2a-r18-q2': False,   # 답안은 담보평가 (시점 2007.8.25)
    'v3-2a-r18-q3': False,   # 답안은 보상평가 (시점 2007.1.20)
    'v3-2a-r18-q4': True,    # 비상장주식 매칭 정확 ✓
    'v3-2a-r25-q4': False,   # 답안은 토지건물 시장가치 (본문은 수익률 통계)
    'v3-2a-r31-q2': False,   # 답안은 할인율 (본문은 임대료)
    'v3-2a-r31-q4': False,   # 답안은 휴업보상 (본문은 공익사업 협의)
}


def clean_body(text):
    """본문에서 시험지 헤더·페이지 번호 제거 + 빈줄 정리."""
    cleaned = text
    for pat in CLEAN_PATTERNS:
        cleaned = pat.sub('', cleaned)
    # 끝 부분에 자주 남는 잔여물 추가 제거
    cleaned = re.sub(r'\s*1\s*교시\s*감정평가실무\s*\d*\s*분\s*$', '', cleaned, flags=re.M)
    # 연속 빈줄 1개로
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
    # 각 라인 끝 공백 제거
    lines = [l.rstrip() for l in cleaned.split('\n')]
    return '\n'.join(lines).strip()


def enhance_answer(text):
    """답안 줄바꿈 보강 (Ⅰ./Ⅱ./Ⅲ. 앞, 1./2. 앞, ①/② 앞에 줄바꿈)."""
    if not text:
        return text
    # 기존 줄바꿈 정리
    out = text.strip()
    # Roman 숫자 절 앞 줄바꿈
    out = re.sub(r'(?<![\n])(?=[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]\.)', '\n', out)
    # 본격 항목 (1. 2. 3. 가. 나.)
    out = re.sub(r'(?<=[^\n])(?=\d+\.\s)', '\n', out)
    out = re.sub(r'(?<=[^\n])(?=[가-하]\.\s)', '\n', out)
    # ① ② ③
    out = re.sub(r'(?<=[^\n])(?=[①②③④⑤⑥⑦⑧⑨⑩])', '\n', out)
    # (1) (2)
    out = re.sub(r'(?<=[^\n])(?=\(\d+\)\s)', '\n', out)
    # 연속 줄바꿈 정리
    out = re.sub(r'\n{3,}', '\n\n', out)
    return out.strip()


def main():
    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    body_cleaned = 0
    answer_nulled = 0
    answer_enhanced = 0

    for q in data['questions']:
        # 1) 본문 cleanup (모든 문제)
        old_body = q.get('body', '')
        new_body = clean_body(old_body)
        if new_body != old_body:
            q['body'] = new_body
            body_cleaned += 1

        # 2) 답안 매칭 검증 (답안 있는 문제만)
        qid = q.get('id')
        if q.get('modelAnswer'):
            if qid in ANSWER_MATCHED:
                if not ANSWER_MATCHED[qid]:
                    # 잘못 매칭 → null + 메타 표시
                    q['modelAnswer'] = None
                    q['modelAnswerSource'] = None
                    q['answerMatchingWarning'] = 'parser가 다른 회차의 답안을 잘못 매칭함. 수동 채점만 가능.'
                    answer_nulled += 1
                else:
                    # 정확 매칭 → 답안 정리
                    q['modelAnswer'] = enhance_answer(q['modelAnswer'])
                    answer_enhanced += 1

    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    print(f'═══ 단원 2a 교정 완료 ═══')
    print(f'본문 cleanup: {body_cleaned}/{len(data["questions"])} 문제')
    print(f'답안 null 처리 (잘못 매칭): {answer_nulled} 문제')
    print(f'답안 정리 (정확 매칭): {answer_enhanced} 문제')

    # 최종 답안 매칭 통계
    matched = sum(1 for q in data['questions']
                  if q.get('modelAnswer') and q.get('modelAnswerSource') in ('matched', 'ai-generated'))
    print(f'\n최종 답안 매칭: {matched}/{len(data["questions"])}')


if __name__ == '__main__':
    main()
