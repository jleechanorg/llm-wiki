---
title: "PR #5705: Integrate script: recover forced checkout on main in --force mode"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldarchitect-ai/pr-5705.md
sources: []
last_updated: 2026-02-22
---

## Summary
- Fixes integrate.sh forced-mode branch switch failure when tracked runtime/config files (notably `.beads/issues.jsonl`) still block checkout.
- In `FORCE_MODE` checkout recovery, adds fallback to `git checkout -f main` if normal `git checkout main` retry still fails.
- Preserves non-force behavior.

## Metadata
- **PR**: #5705
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +8/-4 in 1 files
- **Labels**: none

## Connections
