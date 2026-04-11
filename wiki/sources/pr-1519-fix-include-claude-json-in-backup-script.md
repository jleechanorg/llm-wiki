---
title: "PR #1519: fix: Include .claude.json in backup script"
type: source
tags: []
date: 2025-09-01
source_file: raw/prs-worldarchitect-ai/pr-1519.md
sources: []
last_updated: 2025-09-01
---

## Summary
- Add .claude.json and .claude.json.backup* to rsync include patterns in claude_backup.sh
- Prevents loss of historical usage data during file corruption events
- Ensures ccusage can access complete token usage history

## Metadata
- **PR**: #1519
- **Merged**: 2025-09-01
- **Author**: jleechan2015
- **Stats**: +95/-93 in 2 files
- **Labels**: none

## Connections
