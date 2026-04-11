---
title: "PR #5852: feat(backup): add OpenClaw conversations to Dropbox backup"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldarchitect-ai/pr-5852.md
sources: []
last_updated: 2026-03-04
---

## Summary
- Extends `scripts/claude_backup.sh` to back up `~/.openclaw/agents` (all agent session JSONL files) alongside Claude and Codex in the same parallel rsync job
- Removes the separate openclaw-specific Dropbox cron entry (`10 */4 * * *`) — consolidated into the existing `0 */4 * * * claude_backup_cron.sh` job

## Metadata
- **PR**: #5852
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +34/-13 in 1 files
- **Labels**: none

## Connections
