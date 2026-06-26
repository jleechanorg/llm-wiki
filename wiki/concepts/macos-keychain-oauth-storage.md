---
title: "macOS Keychain OAuth Storage"
type: concept
tags: [claude-code, oauth, macos, keychain, credential-storage, false-positive]
date: 2026-06-26
---

# macOS Keychain OAuth Storage

**Definition**: Claude Code 2.x writes OAuth tokens to macOS **Keychain** under service names like `Claude Code-credentials-<uuid>`, NOT to `~/.claude/.credentials.json`. The JSON file is the OLD Claude Code 1.x storage format and only contains dated backups (`.bak` files). Code that reads `~/.claude/.credentials.json` will silently miss the live credentials.

## Why it matters

Any local helper that depends on Claude Code OAuth (e.g. `ccproxy-api`'s `oauth_claude` plugin) will block during startup if the JSON file is missing — even when valid tokens exist in Keychain. Symptom: ccproxy logs `server_starting` but `lsof -ti:8000 -sTCP:LISTEN` returns nothing; `launchctl print` shows `state=running, pid=N` but the process has no TCP sockets.

## How to recover

```bash
# 1. List Claude Code keychain entries
security dump-keychain 2>/dev/null | grep -B1 -A3 "Claude Code" | grep -E "(svce|cdat)"

# 2. Pick the freshest by cdat field (the .cdat shows the creation timestamp)
#    Typical entries: Claude Code-credentials-a5083ba3 (older),
#                     Claude Code-credentials-8aadb663 (newer)

# 3. Read the freshest into the JSON file ccproxy-api expects
security find-generic-password -s "Claude Code-credentials-8aadb663" \
  -a "jleechan" -w > ~/.claude/.credentials.json
chmod 600 ~/.claude/.credentials.json

# 4. Restart the consumer so it re-reads the file
launchctl kickstart -k "gui/$(id -u)/com.jleechan.ccproxy-api"
```

## When to use the workaround

- Live service (ccproxy-api, oauth-claude plugin, etc.) is logging `server_starting` but not binding its port
- `lsof -ti:PORT -sTCP:LISTEN` returns nothing
- `~/.claude/.credentials.json` doesn't exist or is older than the freshest Keychain entry

## Backup file format

`~/.claude/.credentials.json.YYYYMMDD-HHMMSS.bak` files exist in the filesystem. They are CC's old auto-backup mechanism (rotated on each successful auth). The accessToken in these backups expires after ~1 hour; the refreshToken may work for longer. Always prefer restoring from Keychain over a stale backup.

## Related concepts

- [[ServiceDiscrimination]] — same class of false-positive (assuming location is canonical when storage migrated)
- [[ClaudeCode]] — the upstream tool that uses this storage
- [[ccproxy_api]] — the consumer that depends on the JSON file location