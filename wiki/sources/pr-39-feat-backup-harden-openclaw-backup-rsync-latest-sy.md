---
title: "PR #39: feat(backup): harden openclaw backup — rsync, latest/ symlink, triple-scheduler stagger, watchdog"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldai_claw/pr-39.md
sources: []
last_updated: 2026-03-04
---

## Summary
- Replace shutil with rsync + post-redaction for faster incremental backups with `--delete` cleanup
- Add `latest/` symlink after each successful commit (consumers no longer scan timestamps)
- Fix all three scheduler timing conflicts (all fired at `:00`) — now staggered :00/:20/:40
- Fix wrong target repo in openclaw-cron job and sync script
- Add hourly `backup-watchdog.sh` that alerts via Slack + email if newest backup is >6h old
- Add one-time `consolidate-workspace-snapshots.sh` to rsync ~29

## Metadata
- **PR**: #39
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +0/-0 in 0 files
- **Labels**: none

## Connections
