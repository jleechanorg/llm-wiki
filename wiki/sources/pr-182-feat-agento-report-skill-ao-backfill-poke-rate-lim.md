---
title: "PR #182: feat: agento-report skill + ao-backfill poke rate-limiting + SOUL policy updates"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-182.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Add `/agento_report` skill and `agento-report.sh` script for PR status dashboards
- Extend `ao-backfill.sh` with Pass 3: poke idle sessions that have open PR comments (with 60-min rate-limit guard)
- Add `workspace/SOUL.md` agent policy rules: CR false-positive evaluation, pre-exit merge checklist, poll-loop rule
- Move Slack channel IDs to env vars; clean up docs/launchd/config

## Metadata
- **PR**: #182
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +464/-32 in 8 files
- **Labels**: none

## Connections
