---
title: "PR #155: feat(notify): parallel Slack+email escalation alerts + webhook daemon in install script"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldai_claw/pr-155.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Escalation alerts now fire Slack DM **and** email simultaneously via `ThreadPoolExecutor`; succeeds if either channel works
- `ai.openclaw.webhook` daemon added to `install-launchagents.sh` (macOS launchctl + Linux systemd)

## Metadata
- **PR**: #155
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +269/-101 in 7 files
- **Labels**: none

## Connections
