---
title: "PR #120: fix(lifecycle): auto-merge pipeline — 3 bugs blocking autonomous merge (bd-ara)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-120.md
sources: []
last_updated: 2026-03-23
---

## Summary
PR #115 proved AO workers can independently drive a PR to 6-green, but the lifecycle-worker failed to auto-merge it. Three interacting bugs in the lifecycle polling loop prevented the approved-and-green reaction from firing and succeeding.

## Metadata
- **PR**: #120
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +55/-11 in 2 files
- **Labels**: none

## Connections
