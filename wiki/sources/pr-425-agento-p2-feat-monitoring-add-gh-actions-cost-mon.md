---
title: "PR #425: [agento] [P2] feat(monitoring): add GH Actions cost monitor"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-425.md
sources: []
last_updated: 2026-03-28
---

## Summary
- Adds `scripts/gh-actions-cost-monitor.sh` — queries today's workflow runs across three private repos, sums duration in minutes, and estimates daily cost at $0.002/min (Linux self-hosted runner rate). Fires Slack alert + GitHub issue when daily total exceeds $5.
- Adds `launchd/com.jleechanorg.gh-actions-cost-monitor.plist` — runs the script daily at 9pm.

## Metadata
- **PR**: #425
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +309/-0 in 2 files
- **Labels**: none

## Connections
