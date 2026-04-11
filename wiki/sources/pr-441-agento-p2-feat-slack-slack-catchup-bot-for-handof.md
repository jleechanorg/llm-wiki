---
title: "PR #441: [agento] [P2] feat(slack): Slack catchup bot for handoff digests"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-441.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Adds `src/orchestration/slack_catchup.py` — an on-demand Slack bot that synthesizes recent Slack activity into a structured handoff digest
- Triggered by: `python scripts/slack_catchup.py --post-to <channel> --thread-ts <ts>` (wired to OpenClaw gateway DM handler)
- Reads allowed channels from `openclaw.json`; fetches last 48h of messages per channel
- Classifies messages into: threads, questions requiring response, announcements, noise
- Expands thread roots and renders a per-channel digest
-

## Metadata
- **PR**: #441
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +841/-0 in 2 files
- **Labels**: none

## Connections
