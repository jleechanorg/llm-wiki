---
title: "backup-home.sh"
type: entity
tags: [script, backup, dropbox, user_scope]
---

## What it is
`scripts/backup-home.sh` in the `user_scope` repo — rsyncs machine config (`~/.claude/`, `~/.codex/`, conversation history) into `backup/<hostname>/` in git and to Dropbox, on a launchd schedule (`org.jleechan.user-scope-backup.plist`, `StartInterval=7200` = every 2 hours).

## Known issue (2026-08-31, open)
Runs two Dropbox upload legs from the same `BACKUP_ITEMS` array:
- rsync/FileProvider leg: `DROPBOX_TARGET` (line 49) = `${DROPBOX_BASE_DIR}/${DROPBOX_BACKUP_SUBDIR:-conversation-backups}` — correctly prefixed.
- rclone leg (`run_dropbox_rclone_target_job`, ~line 1220): `dst_remote="dropbox:${rel_norm%/}"` — **missing** the `conversation-backups/` prefix, writing to Dropbox root instead.

Effect: same conversation-history data lands in two places on Dropbox every 2h — root-level `codex_conversations/`/`claude_conversations/` (~55GB apparent, ~118,570 files) and `conversation-backups/codex_conversations/`/`claude_conversations/` (~94GB apparent, >450,000 files). This is Dropbox cloud-quota duplication, not local disk — the root copies are Smart Sync dataless placeholders (see [[disk-audit-apparent-vs-actual-size]]).

**Fix (identified, not applied):** `dst_remote="dropbox:${DROPBOX_BACKUP_SUBDIR:-conversation-backups}/${rel_norm%/}"`. Pending explicit user approval — changes a live scheduled automation's write destination. Tracked as bead `rev-3rsl5`.

## Connections
- [[disk-audit-apparent-vs-actual-size]]
