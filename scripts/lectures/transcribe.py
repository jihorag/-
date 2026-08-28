#!/usr/bin/env python3
"""FLAC → 타임스탬프 전사 JSON (로컬 mlx-whisper, Apple Silicon).

타임스탬프를 반드시 남긴다. 나중에 "이 개념은 12강 23:10" 처럼 강의 구간을 되짚어야 하고,
전사본을 관(leaf)에 매핑할 때도 구간 단위로 잘라야 하기 때문이다.

중단 후 다시 돌려도 이미 끝낸 건 건너뛴다. 처리 속도(실시간 대비 배수)를 매 건 기록해
전체 소요를 추정할 수 있게 한다.

사용:
  python3 scripts/lectures/transcribe.py economics --phase basic --limit 1
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _paths import require_drive, STUDY, WORK

# 한국어 강의 기준 기본값. 정확도가 부족하면 --model mlx-community/whisper-large-v3-mlx 로 올린다.
DEFAULT_MODEL = 'mlx-community/whisper-large-v3-turbo'

# 강사가 반복하는 도메인 용어를 미리 흘려주면 오인식이 줄어든다.
PROMPT = {
    'economics': '감정평가사 1차 경제학원론 강의. 수요곡선, 공급곡선, 탄력성, 한계효용, '
                 '무차별곡선, 예산제약, 생산가능곡선, 기회비용, 소비자잉여, 조세부담의 귀착.',
    'civil': '감정평가사 1차 민법 강의. 법률행위, 의사표시, 대리, 무효와 취소, 조건과 기한, '
             '소멸시효, 물권변동, 등기, 점유권, 소유권, 저당권, 유치권.',
    'realestate': '감정평가사 1차 부동산학원론 강의. 부동산의 개념, 토지의 분류, 자연적 특성, '
                  '수요와 공급, 탄력성, 시장실패, 지대이론, 입지이론, 감정평가 3방식.',
    # 법규는 9개 법률을 두루 다룬다. 앞의 몇 개만 흘려주면 뒤쪽 법률(지적·등기·국유재산 등)의
    # 고유 용어가 통째로 오인식된다 — 교재 9개 PART 를 모두 덮도록 적는다.
    'law': '감정평가사 1차 감정평가관계법규 강의. 국토의 계획 및 이용에 관한 법률, 용도지역, '
           '지구단위계획, 개발행위허가, 건축법, 도시 및 주거환경정비법, 정비사업, '
           '공간정보의 구축 및 관리 등에 관한 법률, 지적공부, 지적소관청, 토지의 표시, 측량, '
           '부동산등기법, 국유재산법, 행정재산, 부동산 가격공시에 관한 법률, 표준지공시지가, '
           '개별공시지가, 감정평가 및 감정평가사에 관한 법률, 동산·채권 등의 담보에 관한 법률.',
    # 회계는 재무회계와 원가회계가 별도 강좌로 나뉘어 있다. 양쪽 용어를 함께 넣는다.
    'accounting': '감정평가사 1차 회계학 강의. 재무상태표, 포괄손익계산서, 수익인식, 금융자산, '
                  '재고자산, 유형자산, 감가상각, 손상차손, 무형자산, 충당부채, 사채, 자본, '
                  '리스, 법인세회계, 현금흐름표, 원가계산, 제조간접원가, 배부율, '
                  '개별원가계산, 종합원가계산, 표준원가, 변동원가계산, 활동기준원가계산.',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('--phase')
    ap.add_argument('--limit', type=int)
    ap.add_argument('--model', default=DEFAULT_MODEL)
    args = ap.parse_args()

    require_drive()

    try:
        import mlx_whisper
    except ImportError:
        sys.exit('mlx_whisper 가 없습니다. ~/.venvs/lecture-whisper/bin/python 으로 실행하세요.')

    cp = STUDY / args.subject / 'lectures/catalog.json'
    cat = json.loads(cp.read_text(encoding='utf-8'))
    items = cat['lectures']
    if args.phase:
        items = [x for x in items if x['phase'] == args.phase]
    if args.limit:
        items = items[:args.limit]

    audio_dir = WORK / 'audio' / args.subject
    out_dir = WORK / 'transcripts' / args.subject
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"{cat['subject_ko']} · 대상 {len(items)}강 · 모델 {args.model}\n")

    speeds = []
    for i, it in enumerate(items, 1):
        src = audio_dir / f"{it['id']}.flac"
        dst = out_dir / f"{it['id']}.json"
        if dst.exists():
            print(f"  [{i}/{len(items)}] 건너뜀 {it['id']}")
            continue
        if not src.exists():
            print(f"  [{i}/{len(items)}] ❌ 오디오 없음 {it['id']} — extract_audio.py 먼저")
            continue

        t0 = time.time()
        res = mlx_whisper.transcribe(
            str(src),
            path_or_hf_repo=args.model,
            language='ko',
            initial_prompt=PROMPT.get(args.subject),
            word_timestamps=False,
            condition_on_previous_text=False,  # 긴 강의에서 환각 연쇄를 끊는다
        )
        el = time.time() - t0

        segs = [{'start': round(s['start'], 2), 'end': round(s['end'], 2),
                 'text': s['text'].strip()} for s in res.get('segments', [])]
        dur = segs[-1]['end'] if segs else 0
        speed = dur / el if el else 0
        speeds.append(speed)

        dst.write_text(json.dumps({
            'lecture_id': it['id'],
            'no': it['no'],
            'phase': it['phase'],
            'title': it['title'],
            'book_pages': it['book_pages'],
            'model': args.model,
            'duration_sec': round(dur),
            'elapsed_sec': round(el),
            'speed_x': round(speed, 1),
            'char_count': sum(len(s['text']) for s in segs),
            'segments': segs,
        }, ensure_ascii=False, indent=1), encoding='utf-8')

        chars = sum(len(s['text']) for s in segs)
        print(f"  [{i}/{len(items)}] {it['id']} · {dur / 60:.0f}분 → {el / 60:.1f}분 소요 "
              f"(실시간 {speed:.1f}배) · {chars:,}자 · {len(segs)}구간")

    if speeds:
        avg = sum(speeds) / len(speeds)
        total_h = cat['total_minutes'] / 60
        print(f'\n평균 {avg:.1f}배속 → 과목 전체 {total_h:.0f}h 처리에 약 {total_h / avg:.1f}시간')


if __name__ == '__main__':
    main()
