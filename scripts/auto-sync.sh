#!/bin/bash
# auto-sync.sh — repo의 모든 변경을 매분 commit + push
#
# 동작:
#   1) 작업 트리에 변경 있으면 `auto-sync: YYYY-MM-DD HH:MM:SS` 메시지로 commit
#   2) origin/main 으로 push 시도 (네트워크/인증 실패는 silent — 다음 분에 재시도)
#
# 호출:
#   - LaunchAgent (~/Library/LaunchAgents/com.jiho.gampyeong-autosync.plist) 가 60초마다 실행
#   - 또는 수동: `bash scripts/auto-sync.sh`
#
# 로그: ~/Library/Logs/gampyeong-autosync.log (LaunchAgent 가 stdout/stderr 리다이렉트)

set -u

REPO="${REPO_PATH:-/Users/hanjiho/Documents/감정평가사 기출문제}"
cd "$REPO" || { echo "[$(date '+%F %T')] repo not found: $REPO"; exit 0; }

# 대화형 prompt 절대 띄우지 않기 (백그라운드에서 무한 대기 방지)
export GIT_TERMINAL_PROMPT=0
export LANG="${LANG:-ko_KR.UTF-8}"
export LC_ALL="${LC_ALL:-ko_KR.UTF-8}"

# rebase/merge/cherry-pick 중이면 건드리지 않는다
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] \
   || [ -f .git/MERGE_HEAD ] || [ -f .git/CHERRY_PICK_HEAD ]; then
  echo "[$(date '+%F %T')] skip — repo in mid-operation"
  exit 0
fi

# 변경 스테이징 (삭제·신규·수정 모두). .gitignore 는 그대로 존중됨.
git add -A

# 스테이지에 변경 없으면 푸시만 시도 (이전에 commit만 되고 push 못 한 분량 있을 수 있음)
if git diff --cached --quiet; then
  if git rev-list --count @{u}..HEAD >/dev/null 2>&1; then
    AHEAD=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo 0)
    if [ "$AHEAD" -gt 0 ]; then
      git push origin main >/dev/null 2>&1 \
        && echo "[$(date '+%F %T')] pushed $AHEAD pending commit(s)" \
        || echo "[$(date '+%F %T')] push pending failed (auth/network?)"
    fi
  fi
  exit 0
fi

# 새 commit
TS=$(date '+%Y-%m-%d %H:%M:%S')
git -c commit.gpgsign=false commit -m "auto-sync: $TS" >/dev/null 2>&1 \
  || { echo "[$(date '+%F %T')] commit failed"; exit 0; }
echo "[$(date '+%F %T')] committed: auto-sync: $TS"

# push (실패는 silent — 다음 분에 다시 시도. 누적되어도 안전)
git push origin main >/dev/null 2>&1 \
  && echo "[$(date '+%F %T')] pushed" \
  || echo "[$(date '+%F %T')] push failed (auth/network?) — will retry next minute"
