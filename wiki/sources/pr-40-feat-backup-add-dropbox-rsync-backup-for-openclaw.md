---
title: "PR #40: feat(backup): add Dropbox rsync backup for ~/.openclaw (ORCH-59b)"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldai_claw/pr-40.md
sources: []
last_updated: 2026-03-04
---

## Summary
- New `scripts/dropbox-openclaw-backup.sh`: rsync `~/.openclaw` to `~/Library/CloudStorage/Dropbox/openclaw_backup/latest/` as a local redundancy alongside the existing GitHub backup
- Updated `scripts/install-openclaw-backup-jobs.sh`: adds Dropbox cron section at `10 */4 * * *` (staggered :10 after launchd :00, complements openclaw-cron :20 and system cron :40)

## Metadata
- **PR**: #40
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +46/-0 in 4 files
- **Labels**: none

## Connections
