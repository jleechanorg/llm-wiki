---
title: "PR #5832: fix: raise RuntimeError when rmtree silently fails in _fresh_clone"
type: source
tags: []
date: 2026-03-03
source_file: raw/prs-worldarchitect-ai/pr-5832.md
sources: []
last_updated: 2026-03-03
---

## Summary
- `shutil.rmtree(ignore_errors=True)` in `_fresh_clone` can silently no-op on macOS (locked files, permission issues), leaving the stale clone directory in place
- The subsequent `git clone` into the non-empty dir exits 128 with an opaque error, causing `fix-comment` to fail with no actionable message
- Audit showed **56 PR dispatch failures** in 24h, all from this root cause

## Metadata
- **PR**: #5832
- **Merged**: 2026-03-03
- **Author**: jleechan2015
- **Stats**: +27/-0 in 2 files
- **Labels**: none

## Connections
