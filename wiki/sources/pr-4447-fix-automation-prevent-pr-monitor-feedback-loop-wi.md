---
title: "PR #4447: fix(automation): Prevent PR monitor feedback loop with sub-PR filtering"
type: source
tags: []
date: 2026-02-01
source_file: raw/prs-worldarchitect-ai/pr-4447.md
sources: []
last_updated: 2026-02-01
---

## Summary
- Fix missing `COMMENT_VALIDATION_MARKER_PREFIX` causing repeated bot comment reprocessing
- Draft PRs (including `copilot/sub-pr-*` branches) already filtered by existing `isDraft` check

## Metadata
- **PR**: #4447
- **Merged**: 2026-02-01
- **Author**: jleechan2015
- **Stats**: +165/-0 in 2 files
- **Labels**: none

## Connections
