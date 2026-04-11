---
title: "PR #10: backup: daily 9am email report for GitHub + Dropbox backup runs"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-/pr-10.md
sources: []
last_updated: 2026-03-14
---

## Summary
- add backup run report capture to scripts/backup-home.sh so each run writes a latest report with file-level rsync itemized lines and final git/dropbox status
- add scripts/send_backup_report_email.sh to email the latest backup report (or missing-report/failure state)
- extend scripts/install_conversation_backup_launchd.sh to also install a second LaunchAgent that sends the backup report email daily at 9:00 AM local time
- update README with new daily-email behavior and script

## Metadata
- **PR**: #10
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +283/-33 in 82 files
- **Labels**: none

## Connections
