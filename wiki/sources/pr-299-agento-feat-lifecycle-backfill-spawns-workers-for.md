---
title: "PR #299: [agento] feat(lifecycle): backfill spawns workers for dead-agent CHANGES_REQUESTED PRs"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-299.md
sources: []
last_updated: 2026-03-30
---

## Summary
The lifecycle backfill loop (`backfillUncoveredPRs`) currently only spawns workers for PRs with no session coverage. When a live agent session dies with an unresolved CHANGES_REQUESTED review from CodeRabbit, the PR becomes orphaned — no worker will pick it up until a human notices.

## Metadata
- **PR**: #299
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +1352/-273 in 13 files
- **Labels**: none

## Connections
