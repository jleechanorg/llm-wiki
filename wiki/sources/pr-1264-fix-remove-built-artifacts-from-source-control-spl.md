---
title: "PR #1264: fix: Remove built artifacts from source control (Split from #1221)"
type: source
tags: []
date: 2025-08-11
source_file: raw/prs-worldarchitect-ai/pr-1264.md
sources: []
last_updated: 2025-08-11
---

## Summary
This PR removes built artifacts from source control as part of the infrastructure cleanup effort.

### Changes Made
- ✅ **Removed built artifacts**: Deleted entire `mvp_site/static/v2/assets/` directory containing compiled JS/CSS bundles
- ✅ **Updated .gitignore**: Added additional patterns to prevent future built artifact commits:
  - `*.js.map` (source maps)
  - `*.gz` (gzip compressed files)
  - `*.br` (brotli compressed files)

### Files Removed
- `mvp_site/static/v2/assets/index-*.css.{br,g

## Metadata
- **PR**: #1264
- **Merged**: 2025-08-11
- **Author**: jleechan2015
- **Stats**: +3/-0 in 11 files
- **Labels**: none

## Connections
