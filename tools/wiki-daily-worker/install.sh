#!/bin/bash
# Install wiki daily worker under ~/Library/Application Support/llm-wiki/
# and register a user LaunchAgent (no OpenClaw, no dependency on repo path).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SOURCE_SCRIPT="$REPO_ROOT/tools/wiki-daily-worker/wiki-daily-worker.sh"
SUPPORT_DIR="$HOME/Library/Application Support/llm-wiki"
TARGET_SCRIPT="$SUPPORT_DIR/daily-worker.sh"
PLIST_LABEL="com.jleechan.wiki-daily-worker"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_LABEL}.plist"
LOG_OUT="$HOME/Library/Logs/wiki-daily-worker.log"
LOG_ERR="$HOME/Library/Logs/wiki-daily-worker.error.log"

if [[ ! -f "$SOURCE_SCRIPT" ]]; then echo "error: missing $SOURCE_SCRIPT" >&2
    exit 1
fi

mkdir -p "$SUPPORT_DIR"
cp "$SOURCE_SCRIPT" "$TARGET_SCRIPT"
chmod +x "$TARGET_SCRIPT"

# Write LaunchAgent plist (absolute paths only)
cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${TARGET_SCRIPT}</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>8</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>
    <key>StandardOutPath</key>
    <string>${LOG_OUT}</string>
    <key>StandardErrorPath</key>
    <string>${LOG_ERR}</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

chmod 644 "$PLIST_PATH"

UID_NUM="$(id -u)"
# Reload job if already registered
if launchctl print "gui/${UID_NUM}/${PLIST_LABEL}" &>/dev/null; then
    launchctl bootout "gui/${UID_NUM}" "$PLIST_PATH" 2>/dev/null || true
fi
launchctl bootstrap "gui/${UID_NUM}" "$PLIST_PATH"

echo "Installed:"
echo "  Script:  $TARGET_SCRIPT"
echo "  Plist:   $PLIST_PATH"
echo "  Logs:    $LOG_OUT"
echo ""
echo "Optional env (edit script or wrap): LLM_WIKI_DIR, MEMORY_WIKI_DIR"
echo "Default wiki path: \$HOME/llm_wiki"
echo ""
echo "Run once: $TARGET_SCRIPT"
echo "Unload:    launchctl bootout gui/${UID_NUM} $PLIST_PATH"
