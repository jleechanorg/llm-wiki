---
title: "PR #257: [agento] feat: add verify6Green() pre-merge gate in lifecycle-manager"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-257.md
sources: []
last_updated: 2026-03-28
---

## Summary
A 24-hour audit found 8/12 merged PRs were NOT 6-green: 4 had CR CHANGES_REQUESTED, 2 had NO CR review, 3 had no skeptic verdict. The lifecycle-manager was calling `checkMergeGate()` but there was no named, explicit entry point that made the gate contract clear and testable. CLAUDE.md instructions are insufficient — agents bypass them.

## Metadata
- **PR**: #257
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +329/-15 in 2 files
- **Labels**: none

## Connections
