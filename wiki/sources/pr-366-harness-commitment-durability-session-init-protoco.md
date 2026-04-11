---
title: "PR #366: harness: commitment durability — session-init protocol + COMMIT: format"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-366.md
sources: []
last_updated: 2026-03-23
---

## Summary
OpenClaw repeatedly made commitments ("I'll always do X going forward") that were forgotten next session. Root cause: there was a write-path for commitments (Promise Gate) but no read-path — nothing forced the agent to reload commitments at session start. Tracked in orch-7df.

## Metadata
- **PR**: #366
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +65/-19 in 4 files
- **Labels**: none

## Connections
