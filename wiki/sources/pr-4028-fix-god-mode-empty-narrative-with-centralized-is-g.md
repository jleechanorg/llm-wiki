---
title: "PR #4028: fix: God mode empty narrative with centralized is_god_mode() detection"
type: source
tags: []
date: 2026-01-28
source_file: raw/prs-worldarchitect-ai/pr-4028.md
sources: []
last_updated: 2026-01-28
---

## Summary
God mode responses now keep `narrative` empty and the frontend reads `god_mode_response` directly. Empty-narrative handling in `world_logic.py` uses centralized god mode detection so case-insensitive modes and the `GOD MODE:` prefix are handled consistently.

### Key Changes

1. `mvp_site/narrative_response_schema.py`: `_combine_god_mode_and_narrative()` no longer copies `god_mode_response` into `narrative`.
2. `mvp_site/world_logic.py`: `_resolve_empty_narrative()` uses `constants.is_god_mode(u

## Metadata
- **PR**: #4028
- **Merged**: 2026-01-28
- **Author**: jleechan2015
- **Stats**: +1149/-975 in 12 files
- **Labels**: none

## Connections
