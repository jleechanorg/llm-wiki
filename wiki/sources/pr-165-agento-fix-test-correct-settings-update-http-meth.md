---
title: "PR #165: [agento] fix(test): correct settings update HTTP method -- POST vs PATCH (wc-st4)"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-165.md
sources: []
last_updated: 2026-03-31
---

## Summary
Commit 6d8e5a1 (worldai_claw-tes1) switched test_settings_update in testing_mcp/test_worldai_claw_api.py from _post_json (POST) to _patch_json (PATCH) to match the backend's PATCH /settings route. However, the evidence descriptor in generate_integration_evidence.py was not updated, leaving a stale POST /settings reference.

## Metadata
- **PR**: #165
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: none

## Connections
