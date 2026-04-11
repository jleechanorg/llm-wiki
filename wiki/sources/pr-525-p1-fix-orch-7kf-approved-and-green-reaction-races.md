---
title: "PR #525: [P1] fix(orch-7kf): approved-and-green reaction races CI checks"
type: source
tags: []
date: 2026-04-06
source_file: raw/prs-worldai_claw/pr-525.md
sources: []
last_updated: 2026-04-06
---

## Summary
PR #383 in `agent-orchestrator` experienced a race condition where the `approved-and-green` reaction fired before all CI checks had completed. This was caused by loose verification logic that only looked for the absence of `FAILURE` conclusions, missing `IN_PROGRESS` or `PENDING` states.

## Metadata
- **PR**: #525
- **Merged**: 2026-04-06
- **Author**: jleechan2015
- **Stats**: +51/-11 in 5 files
- **Labels**: none

## Connections
