---
title: "PR #490: [agento] fix(harness): detect stale session locks that cause silent message loss"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-490.md
sources: []
last_updated: 2026-04-04
---

## Summary
2026-04-04: OpenClaw stopped responding to Slack DMs for ~6 hours. Gateway reported HTTP 200 and all 6 canary checks passed. Root cause: pid=59865 (a dead agent subprocess) held stale `.lock` files in `agents/main/sessions/`, causing every inbound message to hit `"session file locked (timeout 10000ms)"` and be silently dropped.

## Metadata
- **PR**: #490
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +64/-9 in 3 files
- **Labels**: none

## Connections
