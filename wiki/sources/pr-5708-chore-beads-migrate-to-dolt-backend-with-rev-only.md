---
title: "PR #5708: chore(beads): migrate to Dolt backend with REV-only canonical JSONL"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldarchitect-ai/pr-5708.md
sources: []
last_updated: 2026-02-22
---

## Summary
- Switches beads backend from legacy SQLite (`beads.db`) to Dolt
- Canonicalizes `issues.jsonl` to REV-prefix-only format (268 issues, was 596 mixed-prefix)
- Enables `no-daemon` mode to prevent worktree branch commit conflicts

## Metadata
- **PR**: #5708
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +647/-622 in 5 files
- **Labels**: none

## Connections
