---
title: "PR #88: feat(scripts): add ao-doctor-monitor — extended health monitor (bd-92j)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-88.md
sources: []
last_updated: 2026-03-23
---

## Summary
The namespace mismatch bug (bd-e4t) revealed that lifecycle-workers can silently operate in the wrong data namespace, making them blind to sessions. The existing `ao doctor` only checks install/env basics — it doesn't catch runtime issues like namespace mismatches, session sprawl, zombie sessions, or CR coverage gaps.

## Metadata
- **PR**: #88
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +697/-1 in 2 files
- **Labels**: none

## Connections
