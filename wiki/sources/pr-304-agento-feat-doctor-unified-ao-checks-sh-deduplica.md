---
title: "PR #304: [agento] feat(doctor): unified ao-checks.sh — deduplicate setup/doctor + operational health checks"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-304.md
sources: []
last_updated: 2026-03-30
---

## Summary
Self-healing infrastructure is fragmented across `setup.sh`, `ao-doctor.sh`, `start-all.sh`, and `health-check.sh` with overlapping check logic. When components fail (launchd deregisters, main repo drifts to feature branch, ghost worktrees accumulate), doctor doesn't detect or fix them. PR #294 added runner checks but didn't address the structural duplication.

## Metadata
- **PR**: #304
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +700/-856 in 6 files
- **Labels**: none

## Connections
