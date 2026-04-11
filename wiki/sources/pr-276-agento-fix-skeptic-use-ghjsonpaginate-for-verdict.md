---
title: "PR #276: [agento] fix(skeptic): use ghJsonPaginate for verdict comments + flat() fix"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-276.md
sources: []
last_updated: 2026-03-29
---

## Summary
Fixes two bugs in `fetchMergeGateState` skeptic verdict parsing:

1. **Wrong API call**: The verdict section called `ghJson` (single-page) instead of `ghJsonPaginate` (paginated). For PRs with many comments, only the first 100 were searched.
2. **Missing `.flat()`**: `ghJsonPaginate` uses `--paginate --slurp`, returning `Array<Array<...>>` (pages). The code cast to `Array<...>` and iterated — but since `Array<Array<...>>` is iterable, the loop ran over page-arrays not comment objects. Added `.fl

## Metadata
- **PR**: #276
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +427/-259 in 4 files
- **Labels**: none

## Connections
