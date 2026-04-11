---
title: "PR #5112: Perf: gate heavy state dump logs behind DEBUG"
type: source
tags: []
date: 2026-02-09
source_file: raw/prs-worldarchitect-ai/pr-5112.md
sources: []
last_updated: 2026-02-09
---

## Summary
Follow-up to #5110 to address reviewer feedback about INFO-level guards still evaluating expensive payload formatting under default logging.

### Changes
- `mvp_site/world_logic.py`
  - In `_handle_set_command`, moved heavy payload/state dump logs from INFO to DEBUG.
  - Cached `debug_enabled` once and reused it for all expensive log guards.
  - Kept lightweight INFO markers (`received`, `raw payload`, `complete`) intact.
- `mvp_site/firestore_service.py`
  - In `update_campaign_game_state`, mov

## Metadata
- **PR**: #5112
- **Merged**: 2026-02-09
- **Author**: jleechan2015
- **Stats**: +18/-14 in 2 files
- **Labels**: none

## Connections
