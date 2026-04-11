---
title: "PR #149: [agento] fix: use PATCH for settings update test (worldai_claw-tes1)"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-149.md
sources: []
last_updated: 2026-03-30
---

## Summary
- Add `_patch_json` helper to `testing_mcp/test_worldai_claw_api.py` (same pattern as `_post_json` but uses `method='PATCH'`)
- Change `test_settings_update` to call `_patch_json` instead of `_post_json` for the `/settings` endpoint

## Metadata
- **PR**: #149
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +8/-2 in 1 files
- **Labels**: none

## Connections
