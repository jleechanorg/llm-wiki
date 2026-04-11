---
title: "PR #4226: Fix dice display issue with version-based cache busting"
type: source
tags: []
date: 2026-01-31
source_file: raw/prs-worldarchitect-ai/pr-4226.md
sources: []
last_updated: 2026-01-31
---

## Summary
- Implements automatic cache invalidation using git commit hash as version identifier
- Fixes dice rolls not displaying after PR #4111 merge due to cached old frontend code
- Adds backfill logic for legacy outcome_resolution → action_resolution migration
- Includes regression tests for dice strategy backfill behavior

## Metadata
- **PR**: #4226
- **Merged**: 2026-01-31
- **Author**: jleechan2015
- **Stats**: +2092/-124 in 28 files
- **Labels**: none

## Connections
