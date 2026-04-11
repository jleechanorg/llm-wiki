---
title: "PR #349: [agento] fix: zombie sessions detected via session.status not pr.state (bd-ara.2)"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-349.md
sources: []
last_updated: 2026-04-03
---

## Summary
Sessions ao-2303, ao-2312, and ao-2322 were stuck with `status=merged` in the AO session DB but their tmux processes were still alive and consuming session slots. Sessions ao-1957, ao-1966, ao-2092, ao-2223 were stuck with no active work and high `scmFailureCount` values (900-1500).

## Metadata
- **PR**: #349
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +235/-30 in 6 files
- **Labels**: none

## Connections
