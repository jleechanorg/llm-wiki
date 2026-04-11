---
title: "PR #70: [agento] feat: add launchd keepalive wrapper for start-all.sh (bd-la7)"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-70.md
sources: []
last_updated: 2026-03-21
---

## Summary
`start-all.sh` starts all AO lifecycle-workers but is a one-shot script — if a worker crashes, launchd has no keepalive to restart it. The per-project plist in jleechanclaw uses `KeepAlive: true` with `ao lifecycle-worker` directly, but this isn't portable or multi-project.

Refs: bd-la7

## Metadata
- **PR**: #70
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +214/-11 in 5 files
- **Labels**: none

## Connections
