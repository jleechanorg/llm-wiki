---
title: "Cron"
type: concept
tags: [automation, scheduling, unix]
sources: []
last_updated: 2026-04-07
---

Cron is a time-based job scheduler in Unix-like systems. The backup script runs automatically every 4 hours via a cron job.

## Cron Schedule
```cron
0 */4 * * * "$HOME/.local/bin/claude_backup_cron.sh" "$HOME/Library/CloudStorage/Dropbox" 2>&1
```

This runs at minute 0 of every 4th hour (midnight, 4am, 8am, noon, 4pm, 8pm).

## Related Sources
- [[Backup Script Enhancement: Added Codex Conversations Support]] — Runs via cron every 4 hours
