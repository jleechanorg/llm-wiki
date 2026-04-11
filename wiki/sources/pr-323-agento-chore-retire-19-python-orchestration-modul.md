---
title: "PR #323: [agento] chore: retire 19 Python orchestration modules duplicated by AO"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-323.md
sources: []
last_updated: 2026-03-21
---

## Summary
jleechanclaw should be config + skills + launchd only. The Python orchestration layer in src/orchestration/ grew as a parallel reimplementation of what agent-orchestrator (AO) TypeScript now handles natively. PR309 started retiring 12 modules — this PR retires the remaining 19.

## Metadata
- **PR**: #323
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +331/-14755 in 42 files
- **Labels**: none

## Connections
