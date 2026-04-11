---
title: "PR #6121: fix(streaming): persist server system_warnings to Firestore (BD-724 parity)"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldarchitect-ai/pr-6121.md
sources: []
last_updated: 2026-04-07
---

## Summary
- **Problem:** Non-streaming `process_action_unified` already writes combined server warnings to `structured_fields["system_warnings"]` before Firestore persist (BD-724). The **streaming** path (`stream_story_with_game_state` → `_enrich_streaming_structured_fields` → `add_story_entry`) did not, so `debug_info._server_system_warnings` (dice integrity, validation) never reached the persisted story entry’s top-level `system_warnings` — warnings could disappear on reload when using SSE streaming.
-

## Metadata
- **PR**: #6121
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +102/-20 in 3 files
- **Labels**: none

## Connections
