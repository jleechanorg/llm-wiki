---
title: "PR #6030: [agento] fix: trim large traceability state keys (rev-l6c)"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6030.md
sources: []
last_updated: 2026-04-04
---

## Summary
- add _LARGE_STATE_KEYS in structured_fields_utils to remove item_registry, npc_data, and entity_tracking from full_state_updates
- keep existing custom campaign trim (story_history) and preserve core_memories_snapshot
- add regression test covering large top-level key trimming in _build_traceability_fields

## Metadata
- **PR**: #6030
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +200/-56 in 4 files
- **Labels**: none

## Connections
