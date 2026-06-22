#!/usr/bin/env bash
# Install wiki-aggregator as a uv tool + register a daily scheduled job.
# macOS → launchd LaunchAgent; Linux → systemd user timer.
# Subcommands: install (default) | uninstall
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TOOL_DIR="$REPO_ROOT/tools/wiki-aggregator"
LABEL="com.jleechan.wiki-aggregator"

action="${1:-install}"

if [[ "$(id -u)" -eq 0 ]]; then
  echo "error: do not run install.sh as root (user-level agents only)" >&2
  exit 1
fi

install_python_tool() {
  if ! command -v uv >/dev/null 2>&1; then
    echo "error: 'uv' not found. Install via: curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    exit 1
  fi
  echo "Installing wiki-aggregator via uv tool..."
  (cd "$TOOL_DIR" && uv tool install --force .)
  command -v wiki-aggregator >/dev/null || {
    echo "error: wiki-aggregator not found on PATH after uv install" >&2
    exit 1
  }
}

uninstall_python_tool() {
  uv tool uninstall wiki-aggregator 2>/dev/null || true
}

install_schedule() {
  case "$(uname -s)" in
    Darwin)
      PLIST_TEMPLATE="$TOOL_DIR/launchd/${LABEL}.plist.template"
      PLIST_DST="$HOME/Library/LaunchAgents/${LABEL}.plist"
      [[ -f "$PLIST_TEMPLATE" ]] || { echo "missing $PLIST_TEMPLATE" >&2; exit 1; }
      sed "s|@HOME@|${HOME}|g" "$PLIST_TEMPLATE" > "$PLIST_DST"
      chmod 644 "$PLIST_DST"
      UID_NUM="$(id -u)"
      if launchctl print "gui/${UID_NUM}/${LABEL}" &>/dev/null; then
        launchctl bootout "gui/${UID_NUM}" "$PLIST_DST" 2>/dev/null || true
      fi
      launchctl bootstrap "gui/${UID_NUM}" "$PLIST_DST"
      echo "Installed (launchd):"
      echo "  Binary: $(command -v wiki-aggregator)"
      echo "  Plist:  $PLIST_DST"
      echo "  Logs:   ~/Library/Logs/wiki-aggregator.log"
      ;;
    Linux)
      SYSTEMD_DIR="$HOME/.config/systemd/user"
      mkdir -p "$SYSTEMD_DIR"
      cp "$TOOL_DIR/systemd/wiki-aggregator.service" "$SYSTEMD_DIR/"
      cp "$TOOL_DIR/systemd/wiki-aggregator.timer"   "$SYSTEMD_DIR/"
      systemctl --user daemon-reload
      systemctl --user enable --now wiki-aggregator.timer
      echo "Installed (systemd):"
      echo "  Binary: $(command -v wiki-aggregator)"
      echo "  Unit:   $SYSTEMD_DIR/wiki-aggregator.{service,timer}"
      echo "  Logs:   journalctl --user -u wiki-aggregator.service"
      ;;
    *)
      echo "warning: unsupported OS $(uname -s); only the uv tool was installed." >&2
      ;;
  esac
}

uninstall_schedule() {
  case "$(uname -s)" in
    Darwin)
      PLIST_DST="$HOME/Library/LaunchAgents/${LABEL}.plist"
      UID_NUM="$(id -u)"
      if [[ -f "$PLIST_DST" ]]; then
        launchctl bootout "gui/${UID_NUM}" "$PLIST_DST" 2>/dev/null || true
        rm -f "$PLIST_DST"
      fi
      ;;
    Linux)
      systemctl --user disable --now wiki-aggregator.timer 2>/dev/null || true
      rm -f "$HOME/.config/systemd/user/wiki-aggregator."{service,timer}
      systemctl --user daemon-reload
      ;;
  esac
}

case "$action" in
  install)    install_python_tool; install_schedule ;;
  uninstall)  uninstall_schedule;  uninstall_python_tool ;;
  *) echo "usage: $0 [install|uninstall]" >&2; exit 1 ;;
esac