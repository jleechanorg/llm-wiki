---
title: "PR #2425: fix(auth): default clock skew to 600s for local development"
type: source
tags: []
date: 2025-12-13
source_file: raw/prs-worldarchitect-ai/pr-2425.md
sources: []
last_updated: 2025-12-13
---

## Summary
- Fixed clock skew detection to work with `TESTING=true` (was returning 0 instead of 600)
- Added `_is_local_development()` helper that detects local dev by:
  - `WORLDAI_DEV_MODE=true`
  - `TESTING=true`
  - `~/serviceAccountKey.json` exists

## Metadata
- **PR**: #2425
- **Merged**: 2025-12-13
- **Author**: jleechan2015
- **Stats**: +50/-57 in 2 files
- **Labels**: none

## Connections
