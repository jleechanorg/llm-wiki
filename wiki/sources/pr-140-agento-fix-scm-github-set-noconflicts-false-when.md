---
title: "PR #140: [agento] fix(scm-github): set noConflicts=false when mergeable=UNKNOWN (bd-ara.2)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-140.md
sources: []
last_updated: 2026-03-24
---

## Summary
13/19 open PRs were stuck at `mergeable=UNKNOWN`. Workers went idle because the `merge-conflicts` reaction only fired when GitHub explicitly reported `CONFLICTING` — not when it reported `UNKNOWN` (merge status still being computed). The existing `merge-conflicts` reaction (which sends a rebase message to the worker) was never triggered.

## Metadata
- **PR**: #140
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +83/-15 in 3 files
- **Labels**: none

## Connections
