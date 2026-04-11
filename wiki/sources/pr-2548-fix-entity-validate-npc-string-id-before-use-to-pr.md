---
title: "PR #2548: fix(entity): validate NPC string_id before use to prevent invalid prefix errors"
type: source
tags: []
date: 2025-12-22
source_file: raw/prs-worldarchitect-ai/pr-2548.md
sources: []
last_updated: 2025-12-22
---

## Summary
- Fixed Pydantic ValidationError when NPC has invalid `string_id` prefix (e.g., `faction_` instead of `npc_`)
- Invalid `string_id` values are now regenerated with proper `npc_` prefix instead of crashing
- Added regression test `test_invalid_string_ids_regenerated`

## Metadata
- **PR**: #2548
- **Merged**: 2025-12-22
- **Author**: jleechan2015
- **Stats**: +34/-3 in 2 files
- **Labels**: none

## Connections
