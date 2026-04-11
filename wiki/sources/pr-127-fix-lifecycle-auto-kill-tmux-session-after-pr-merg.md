---
title: "PR #127: fix(lifecycle): auto-kill tmux session after PR merged/closed"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-127.md
sources: []
last_updated: 2026-03-23
---

## Summary
P0 bug (jleechan-v7oa): `packages/core/src/lifecycle-manager.ts` detects merged/killed session status transitions but never calls `sessionManager.kill()` for the `killed` case, causing zombie tmux sessions to accumulate indefinitely. The merged case was already handled (bd-s4t.1), but killed was missed.

Known zombie session examples: `bb5e6b7f8db3-ao-302`, `-314`, `-315`. Related prior work: PR #86 (lifecycle-manager cleanup).

## Metadata
- **PR**: #127
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +92/-5 in 2 files
- **Labels**: none

## Connections
