---
title: "PR #97: [agento] feat: add PR worker coverage harness with validation script (bd-7ay)"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-97.md
sources: []
last_updated: 2026-03-21
---

## Summary
Adds a deterministic, fail-closed harness for PR worker coverage reconciliation:

- **`CLAUDE.md`**: Documents the mandatory recovery command (`ao spawn --claim-pr <PR>`), PR coverage reconciliation procedure, validation script usage, and EPIPE handling patterns.
- **`scripts/check-pr-worker-coverage.sh`**: Reports PR→session mapping, exits 0 when all open PRs have active sessions, exits non-zero with uncovered PRs listed.

## Metadata
- **PR**: #97
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +130/-1 in 2 files
- **Labels**: none

## Connections
