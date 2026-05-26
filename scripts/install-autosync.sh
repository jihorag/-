#!/bin/bash
# install-autosync.sh — macOS LaunchAgent로 매분 auto-sync 설치
#
# 사용:  bash scripts/install-autosync.sh
# 제거:  bash scripts/install-autosync.sh --uninstall
#
# 추가로 필요한 사용자 조치 (이 스크립트가 자동화 못 함):
#   1) Full Disk Access — System Settings → Privacy & Security → Full Disk Access
#      → "+" 클릭 → Cmd+Shift+G → "/bin/bash" 입력 → "/bin/bash" 추가
#      (또는 처음 실행 시 macOS가 띄우는 "bash가 ~/Documents 접근하려 합니다" 팝업에서 허용)
#      이거 없으면 LaunchAgent가 "Operation not permitted"로 실패함
#
#   2) GitHub push 인증 (둘 중 하나)
#      HTTPS+토큰: 한 번 수동 push (`git push origin main`) → 사용자명/PAT 입력 →
#                  osxkeychain 에 저장됨 → 이후 LaunchAgent 푸시도 통과
#      SSH:        `ssh-keygen -t ed25519 -C "..."` → `~/.ssh/id_ed25519.pub`을 GitHub에 등록 →
#                  `git remote set-url origin git@github.com:jihorag/-.git`

set -eu

LABEL="com.jiho.gampyeong-autosync"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$REPO/scripts/$LABEL.plist.template"
LOG="$HOME/Library/Logs/gampyeong-autosync.log"

uninstall() {
  if [ -f "$PLIST" ]; then
    launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"
    echo "✓ removed $PLIST"
  else
    echo "(nothing to remove)"
  fi
}

if [ "${1:-}" = "--uninstall" ] || [ "${1:-}" = "-u" ]; then
  uninstall
  exit 0
fi

if [ ! -f "$TEMPLATE" ]; then
  echo "✗ template missing: $TEMPLATE"; exit 1
fi

# 기존 등록 해제 (재실행 안전)
launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true

# 템플릿 치환 → 사용자 LaunchAgents 디렉토리에 작성
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"
sed -e "s|__REPO__|$REPO|g" -e "s|__HOME__|$HOME|g" "$TEMPLATE" > "$PLIST"
echo "✓ wrote $PLIST"
echo "  → repo: $REPO"

# 검증
if ! plutil -lint "$PLIST" >/dev/null; then
  echo "✗ plist invalid"; exit 1
fi

# git identity 없으면 안내
if ! git -C "$REPO" config user.name >/dev/null 2>&1; then
  echo ""
  echo "⚠  git user.name 미설정. 권장:"
  echo "    git -C \"$REPO\" config user.name \"$(whoami)\""
  echo "    git -C \"$REPO\" config user.email \"you@example.com\""
fi

# 등록
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "✓ launchctl bootstrap OK"

echo ""
echo "다음 60초 안에 첫 사이클이 돕니다. 로그 모니터:"
echo "  tail -f \"$LOG\""
echo ""
echo "❗ 첫 실행에서 '/bin/bash: Operation not permitted' 가 보이면:"
echo "  System Settings → Privacy & Security → Full Disk Access"
echo "  → '+' → Cmd+Shift+G → /bin/bash 추가 (체크박스 켜기)"
echo "  설정 후 launchctl kickstart gui/$(id -u)/$LABEL 으로 즉시 재실행"
echo ""
echo "제거: bash scripts/install-autosync.sh --uninstall"
