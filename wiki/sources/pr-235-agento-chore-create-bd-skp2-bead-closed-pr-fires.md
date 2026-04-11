---
title: "PR #235: [agento] chore: create bd-skp2 bead — closed PR fires changes-requested reaction"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-235.md
sources: []
last_updated: 2026-03-27
---

## Summary
PR #223 was CLOSED, but the lifecycle-manager's `changes-requested` reaction kept firing because `determineStatus` checks `reviewDecision === "changes_requested"` without first verifying the PR is OPEN. GitHub does not clear `reviewDecision` when a PR is closed, and the batch path's `batch.state` can be falsy/undefined, bypassing the closed guard.

## Metadata
- **PR**: #235
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +2/-2 in 1 files
- **Labels**: none

## Connections
