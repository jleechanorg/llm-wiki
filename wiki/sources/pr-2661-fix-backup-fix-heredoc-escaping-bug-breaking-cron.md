---
title: "PR #2661: fix(backup): Fix heredoc escaping bug breaking cron backups"
type: source
tags: []
date: 2025-12-27
source_file: raw/prs-worldarchitect-ai/pr-2661.md
sources: []
last_updated: 2025-12-27
---

## Summary
- Fix heredoc escaping bug in `install_backup_system.sh` that caused cron backups to fail since Nov 22
- Update `claude_backup.sh` to include Codex conversation backups (in addition to Claude)
- Sync `claude_backup_cron.sh` with the working fixed version

## Metadata
- **PR**: #2661
- **Merged**: 2025-12-27
- **Author**: jleechan2015
- **Stats**: +190/-160 in 3 files
- **Labels**: none

## Connections
