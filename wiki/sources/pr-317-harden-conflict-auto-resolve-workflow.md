---
title: "PR #317: Harden conflict auto-resolve workflow"
type: source
tags: [codex]
date: 2025-10-13
source_file: raw/prs-/pr-317.md
sources: []
last_updated: 2025-10-13
---

## Summary
- ensure the conflict resolution scripts operate from the repo root, guard against dirty trees, and work in CI contexts
- make the auto-resolver fail fast for forked PRs and restore the previous branch when run locally
- document how to trigger and replicate the auto resolve workflow inside `.github/workflows/README.md`

## Metadata
- **PR**: #317
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +277/-14 in 6 files
- **Labels**: codex

## Connections
