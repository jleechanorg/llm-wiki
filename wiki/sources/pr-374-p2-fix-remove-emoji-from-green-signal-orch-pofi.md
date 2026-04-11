---
title: "PR #374: [P2] fix: remove emoji from green signal (orch-pofi)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-374.md
sources: []
last_updated: 2026-03-23
---

## Summary
PR #358 (merged 2026-03-21) explicitly canonicalized the green signal to remove the ✅ emoji for orchestrator pattern-matching consistency. The canonical form is:

```
PR is green (6/6 criteria met — awaiting auto-merge)
```

PR #351 (merged 2026-03-22, ~8h later) re-added the ✅ emoji everywhere, undoing #358.

This regresses the green signal pattern that the orchestrator's merge-gate and lifecycle-worker rely on for reliable detection.

## Metadata
- **PR**: #374
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +12/-12 in 2 files
- **Labels**: none

## Connections
