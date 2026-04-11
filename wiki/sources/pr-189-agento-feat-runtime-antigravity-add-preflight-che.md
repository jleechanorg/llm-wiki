---
title: "PR #189: [agento] feat(runtime-antigravity): add preflight checks before Peekaboo session creation"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-189.md
sources: []
last_updated: 2026-03-25
---

## Summary
runtime-antigravity create() dives straight into Peekaboo window ops without validating the environment. When Antigravity is not running or the Manager window is missing, opaque errors surface deep in the call stack.

## Metadata
- **PR**: #189
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +294/-0 in 5 files
- **Labels**: none

## Connections
