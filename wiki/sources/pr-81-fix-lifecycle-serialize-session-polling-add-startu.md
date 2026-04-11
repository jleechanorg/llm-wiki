---
title: "PR #81: fix(lifecycle): serialize session polling + add startup jitter (bd-wse)"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-81.md
sources: []
last_updated: 2026-03-21
---

## Summary
Diagnosed via /auton (bead bd-wse): 15 concurrent sessions caused GitHub API rate limit exhaustion, blocking all PR progress. Root cause in lifecycle-manager.ts and lifecycle-worker.ts.

## Metadata
- **PR**: #81
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +85/-2 in 3 files
- **Labels**: none

## Connections
