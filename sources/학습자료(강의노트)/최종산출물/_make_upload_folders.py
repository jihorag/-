#!/usr/bin/env python3
"""각 과목별로 _업로드용_단원별/ 하위에 단원 폴더를 만들고
   해당 단원 학습 시 한 번에 업로드할 파일들을 모음.
   각 폴더는 클로드 10파일 제한 이내."""
import shutil, re
from pathlib import Path

ROOT = Path('/Users/hanjiho/Documents/Claude KAPA CHATING/최종산출물')

# 과목별 설정: (폴더명, 동행파일 리스트, 단원파일 패턴, 문제파일 패턴)
SUBJECTS = [
    {
        'folder': '1과목_1차_경제학',
        'companions': ['인수인계_경제학_v2.md', '_단원별_자료량.md'],
        'unit_prefix': '단원_',
        'problem_prefix': '문제_',
    },
    {
        'folder': '2과목_2차_감정평가실무',
        'companions': ['인수인계_v3.md', '_공식모음.md', '_법령모음.md'],
        'unit_prefix': '단원_',
        'problem_prefix': '문제_',
    },
    {
        'folder': '3과목_2차_감정평가이론',
        'companions': ['인수인계_이론_v2.md', '_논점별_출제빈도.md', '_필기노트_핵심포인트.md', '_법령모음.md'],
        'unit_prefix': '단원_',
        'problem_prefix': '문제_',
    },
    {
        'folder': '4과목_2차_감정평가법규',
        'companions': ['인수인계_법규_v1.md', '_단원별_출제빈도.md', '_기출연도별_논점정리.md'],
        'unit_prefix': '단원_',
        'problem_prefix': '문제_',
    },
    {
        'folder': '5과목_1차_부동산학원론',
        'companions': ['인수인계_부동산학원론_v1.md', '_출제빈도_분석.md'],
        'unit_prefix': '단원_',
        'problem_prefix': '문제_',
    },
    {
        'folder': '6과목_1차_민법',
        'companions': ['인수인계_민법_v1.md', '_출제빈도_분석.md'],
        'unit_prefix': '단원_',
        'problem_prefix': '문제_',
    },
    {
        'folder': '7과목_1차_감정평가관계법규',
        'companions': ['인수인계_관계법규_v1.md', '_출제빈도_분석.md'],
        'unit_prefix': '단원_',
        'problem_prefix': '문제_',
    },
    {
        'folder': '8과목_1차_회계학',
        'companions': ['인수인계_회계학_v1.md', '_출제빈도_분석.md'],
        'unit_prefix': '단원_',
        'problem_prefix': '문제_',
    },
]


def get_unit_id(filename, prefix):
    """단원_M01_수학적_기초.md → 'M01' (또는 PART01, 2a 등)"""
    name = filename.replace(prefix, '', 1).replace('.md', '')
    # 첫 토큰까지가 단원 ID
    m = re.match(r'([A-Za-z0-9]+[a-z]?)', name)
    if m:
        return m.group(1)
    # 한자가 직접 시작하면 (예: 단원_M01_..., 단원_PART01_...)
    return name.split('_')[0]


def process_subject(cfg):
    src_dir = ROOT / cfg['folder']
    if not src_dir.exists():
        print(f'  ⚠️  {cfg["folder"]} 없음 — 건너뜀')
        return
    upload_root = src_dir / '_업로드용_단원별'
    if upload_root.exists():
        shutil.rmtree(upload_root)
    upload_root.mkdir()

    # 동행 파일 존재 확인
    companion_paths = []
    for c in cfg['companions']:
        p = src_dir / c
        if p.exists():
            companion_paths.append(p)
        else:
            print(f'    ⚠️  동행 파일 없음: {c}')

    # 단원 파일 찾기
    unit_files = sorted([p for p in src_dir.glob(f'{cfg["unit_prefix"]}*.md')
                         if not p.name.startswith('_')])
    problem_files = {get_unit_id(p.name, cfg['problem_prefix']): p
                     for p in src_dir.glob(f'{cfg["problem_prefix"]}*.md')}

    count = 0
    for unit_file in unit_files:
        unit_id = get_unit_id(unit_file.name, cfg['unit_prefix'])
        # 단원 폴더명: 단원_M01_수학적_기초·경제학_기초/
        folder_name = unit_file.name.replace('.md', '')
        unit_folder = upload_root / folder_name
        unit_folder.mkdir(exist_ok=True)

        # 동행 파일 복사
        for cp in companion_paths:
            shutil.copy(cp, unit_folder / cp.name)
        # 단원 파일 복사
        shutil.copy(unit_file, unit_folder / unit_file.name)
        # 문제 파일 복사
        if unit_id in problem_files:
            shutil.copy(problem_files[unit_id], unit_folder / problem_files[unit_id].name)

        file_count = len(list(unit_folder.iterdir()))
        count += 1

    print(f'  ✅ {cfg["folder"]}: {count}개 단원 폴더 생성 (각 폴더 {len(companion_paths)+2}개 파일)')


print('=== 단원별 업로드 폴더 생성 시작 ===\n')
for cfg in SUBJECTS:
    process_subject(cfg)

print('\n=== 완료 ===')
