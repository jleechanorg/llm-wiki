---
title: "PR #5695: fix(orchestration): add CLAUDECODE to minimax env_unset (prevent nested-session preflight failure)"
type: source
tags: []
date: 2026-02-21
source_file: raw/prs-worldarchitect-ai/pr-5695.md
sources: []
last_updated: 2026-02-21
---

## Summary
- Restores CLAUDECODE to minimax env_unset, dropped by PR #5654 auth hardening
- Prevents claude child process from hitting nested-session guard during preflight
- Adds TestMinimaxCliEnvironment (5 tests) to lock in correct behavior

## Metadata
- **PR**: #5695
- **Merged**: 2026-02-21
- **Author**: jleechan2015
- **Stats**: +165/-17 in 9 files
- **Labels**: none

## Connections
