---
title: "PR #437: [agento] orch-jq2: dropped-thread-followup launchd + Slack MCP nudge system"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-437.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Adds `dropped-thread-followup.sh` (launchd every 4h): scans monitored Slack channels for cold threads where user asked agent to do work but no action was taken, nudges via Slack API with idempotency guard
- Adds launchd plist `ai.openclaw.schedule.dropped-thread-followup` (4h interval)
- Updates `HEARTBEAT.md`: adds 30-min periodic task section for dropped thread check cadence
- Updates `TOOLS.md`: adds Slack MCP reminder to prevent future "forgot Slack MCP" incidents
- Fixes `SOUL.md` §5 memo

## Metadata
- **PR**: #437
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +412/-3 in 5 files
- **Labels**: none

## Connections
