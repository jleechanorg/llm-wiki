---
title: "PR #5131: Fix integrate force-mode checkout blockers"
type: source
tags: []
date: 2026-02-09
source_file: raw/prs-worldarchitect-ai/pr-5131.md
sources: []
last_updated: 2026-02-09
---

## Summary
- make `integrate.sh --force` resilient when branch checkout is blocked by transient untracked `.beads` runtime files
- include untracked files in force-mode auto-stash so checkout can proceed cleanly
- add checkout recovery path in force mode with clearer error output if retry still fails
- include current `.beads/issues.jsonl` state update on this branch

## Metadata
- **PR**: #5131
- **Merged**: 2026-02-09
- **Author**: jleechan2015
- **Stats**: +289/-4 in 2 files
- **Labels**: none

## Connections
