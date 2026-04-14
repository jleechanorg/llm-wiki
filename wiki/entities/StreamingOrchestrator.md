---
title: "StreamingOrchestrator"
type: entity
tags: [project, worldarchitect, streaming]
sources: [stream-event-type]
last_updated: 2026-04-14
---

Part of the `mvp_site` project. Defines streaming flows and uses the `StreamEvent` type for Server-Sent Events. Must import from a separate module to avoid circular dependencies with [[LlmService]].

**Related:**
- [[StreamEventType]] — the shared type it imports
- [[LlmService]] — shares StreamEvent dependency

## Streaming Passthrough Normalization Bug (jleechan-ajww)

**Bug (FIXED):** `streaming_orchestrator.py:709` assigned `canonical_stream_rewards_box = raw_structured_rewards_box` **unconditionally** before the `_has_level_up_ui_signal` check. When that check returned `False` (no active level-up signal), raw un-normalized LLM `rewards_box` flowed to Firestore without calling `normalize_rewards_box_for_ui`.

**Fix (PR #6265):** Streaming orchestrator now uses `_resolve_canonical_level_up_ui_pair` unconditionally, which calls `normalize_rewards_box_for_ui` in its passthrough branch.

**Key file:** `mvp_site/streaming_orchestrator.py` — `stream_story_with_game_state` function, done-event persistence block
