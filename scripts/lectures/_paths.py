"""강의 파이프라인의 경로 한 곳.

**산출물은 웹앱(viewer)으로 간다.** 기준 앱이 웹앱으로 바뀌었다(2026-08-17).
PC앱 소스·데이터는 웹앱으로 옮겨 두 앱의 기능이 같아진 상태다.

경로가 바뀌면 여기만 고친다.
"""
from pathlib import Path

# 이 저장소(데이터·파이프라인)
REPO = Path(__file__).resolve().parents[2]

# 원본 강의가 있는 외장 + 중간 산출물(오디오·전사·키프레임) 작업 루트.
# 드라이브 이름을 박아 두면 외장을 바꿀 때마다 파이프라인이 통째로 멈춘다
# (WD_Black → T7 Shield 로 옮기면서 실제로 겪었다). 마운트된 볼륨에서 찾는다.
def _find_drive():
    for vol in sorted(Path('/Volumes').iterdir()) if Path('/Volumes').exists() else []:
        if (vol / '인터넷강의/감정평가사 인터넷강의').exists():
            return vol / '인터넷강의'
    return Path('/Volumes/T7 Shield/인터넷강의')   # 못 찾으면 마지막으로 쓰던 곳(오류 메시지용)


_DRIVE = _find_drive()
SRC_ROOT = _DRIVE / '감정평가사 인터넷강의'
WORK = _DRIVE / '_ai_pipeline'

# 앱 데이터 — **웹앱(viewer)이 기준** (2026-08-17 변경)
# 이전에는 PC앱(gampyeong-desktop)이 기준이었으나 개발을 접었다.
# 산출 경로가 여기 한 곳뿐이어야 파이프라인이 두 갈래로 갈라지지 않는다.
APP = REPO / 'viewer'
STUDY = APP / 'public/data/study'


def require_drive():
    """외장이 마운트돼 있는지 확인하고, 아니면 즉시 멈춘다.

    마운트가 풀린 상태로 스크립트를 돌리면 `/Volumes/…` 가 그냥 빈 폴더로 보여서
    거기에 출력 디렉터리를 만들려다 알아보기 힘든 오류를 낸다(실제로 두 번 겪었다).
    더 나쁘게는 내장 디스크에 대용량 산출물을 쓰기 시작할 수도 있다.
    그래서 원본 경로가 실제로 보이는지로 판정한다.
    """
    import sys
    if not SRC_ROOT.exists():
        sys.exit('❌ 강의 원본이 있는 외장이 연결돼 있지 않습니다.\n'
                 f'   확인 경로: {SRC_ROOT}\n'
                 '   드라이브를 연결한 뒤 다시 실행하세요.')


def study_dir(subject):
    return STUDY / subject


def lectures_dir(subject):
    return STUDY / subject / 'lectures'
