---
title: "PR #297: [agento] fix: remove hardcoded test command and fix green criteria count (bd-ppm)"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-297.md
sources: []
last_updated: 2026-03-29
---

## Summary
Fixes two issues in the AO task dispatch template:

1. **Hardcoded test command removed** (packages/cli/templates/rules/base.md): Replaced 'Always run tests before pushing.' with 'Run tests as specified in this project'''s CLAUDE.md.' — agents now follow project-specific test instructions instead of a hardcoded override.

2. **Green criteria count corrected** (backfill-extensions.ts, lifecycle-manager.ts): Changed '6-green' to '7-green' in the backfill spawn prompt and verify6Green JSDoc comment

## Metadata
- **PR**: #297
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +10/-9 in 3 files
- **Labels**: none

## Connections
