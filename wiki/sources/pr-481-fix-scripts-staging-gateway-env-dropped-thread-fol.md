---
title: "PR #481: fix(scripts): staging gateway env + dropped-thread follow-up detection"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-481.md
sources: []
last_updated: 2026-04-03
---

## Summary
- **staging-gateway.sh**: Start staging gateway with `OPENCLAW_CONFIG_PATH` and `OPENCLAW_STATE_DIR` (matches gateway plist / doctor expectations; replaces `OPENCLAW_CONFIG_DIR`-only usage).
- **dropped-thread-followup.sh**: Compute last user vs last agent message times; flag `followup-pending` when the user posted after the agent with an actionable-looking message and has waited ≥5 minutes; avoid treating “recent agent result” as done when the user followed up afterward.
- **workspace/SOUL.md**

## Metadata
- **PR**: #481
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +46/-2 in 5 files
- **Labels**: none

## Connections
