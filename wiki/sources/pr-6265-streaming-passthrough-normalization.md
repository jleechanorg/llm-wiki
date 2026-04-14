---
title: "PR #6265: Streaming Passthrough Normalization"
type: source
tags: [worldarchitect, level-up, rewards-box, streaming, bug-fix]
date: 2026-04-14
source_file: raw/pr-6265-streaming-passthrough-normalization.md
---

## Summary
PR #6265 fixes the streaming passthrough normalization bug (jleechan-ajww P0). When `_has_level_up_ui_signal` returned False (no active level-up signal), the streaming orchestrator's done handler bypassed `_resolve_canonical_level_up_ui_pair` and passed raw un-normalized LLM rewards_box directly to Firestore, causing players to see missing/stale rewards_box after reload.

## Key Claims
- **Root cause**: `streaming_orchestrator.py:709` unconditionally assigned `canonical_stream_rewards_box = raw_structured_rewards_box` before the `_has_level_up_ui_signal` check
- **Fix location 1**: `world_logic.py:1741-1744` — passthrough branch now calls `normalize_rewards_box_for_ui(rewards_box)`
- **Fix location 2**: `streaming_orchestrator.py:707-730` — uses `_resolve_canonical_level_up_ui_pair` unconditionally instead of conditional
- **Bead**: jleechan-ajww (P0) — CLOSED

## Key Changes
1. `_resolve_canonical_level_up_ui_pair` passthrough branch calls `normalize_rewards_box_for_ui`
2. Streaming done handler restructured to call `_resolve_canonical_level_up_ui_pair` for all payloads (not just level-up cases)
3. Tests: `TestPassthroughNormalization` class in `test_level_up_stale_flags.py`

## Connections
- [[LevelUpBug]] — bug chain includes PR #6265
- [[StreamingOrchestrator]] — streaming done handler fix
- [[RewardsBox]] — rewards_box normalization requirement
- [[StreamingVsNonStreaming]] — architectural pattern
