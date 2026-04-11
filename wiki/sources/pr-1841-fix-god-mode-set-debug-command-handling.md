---
title: "PR #1841: Fix GOD_MODE_SET debug command handling"
type: source
tags: [codex]
date: 2025-10-07
source_file: raw/prs-worldarchitect-ai/pr-1841.md
sources: []
last_updated: 2025-10-07
---

## Summary
- route GOD_MODE_SET debug commands through the existing set/update helpers so multi-line payloads with nested paths are applied
- share the debug-mode-disabled response and reuse the ASK_STATE/UPDATE_STATE helpers to keep other debug flows intact
- add a regression test that exercises GOD_MODE_SET multi-line payloads through the debug command handler
- restore GOD_ASK_STATE responses to include the structured `game_state` payload and cover the contract with a unit test
- switch the game state u

## Metadata
- **PR**: #1841
- **Merged**: 2025-10-07
- **Author**: jleechan2015
- **Stats**: +100/-56 in 2 files
- **Labels**: codex

## Connections
