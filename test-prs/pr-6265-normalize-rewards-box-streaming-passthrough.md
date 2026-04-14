---
title: "PR #6265: [antig] [Fix] Normalize rewards box in streaming passthrough"
type: test-pr
date: 2026-04-14
pr_number: 6265
files_changed: [streaming_orchestrator.py, world_logic.py, test_streaming_passthrough_normalization.py]
---

## Summary
Fixes a P0 bug where raw, un-normalized rewards box data from the LLM was getting merged into Firestore because the fallback passthrough path skipped normalization. Now all streaming payloads pass through `_resolve_canonical_level_up_ui_pair` unconditionally, and the passthrough branch explicitly calls `normalize_rewards_box_for_ui`.

## Key Changes
- **streaming_orchestrator.py**: Removed `_has_level_up_ui_signal` conditional - now calls `_resolve_canonical_level_up_ui_pair` unconditionally for all payloads
- **world_logic.py**: Added normalization call in the passthrough fallback codepath at line 1717
- **test_streaming_passthrough_normalization.py**: Added integration test that asserts normalization works even with chaotic LLM keys

## Diff Snippets
```python
# streaming_orchestrator.py - unconditional normalization
-                canonical_stream_rewards_box = raw_structured_rewards_box
-                if world_logic._has_level_up_ui_signal(
+                (
+                    resolved_rb,
+                    resolved_pb,
+                ) = world_logic._resolve_canonical_level_up_ui_pair(
                     updated_state_dict,
-                    raw_structured_rewards_box,
-                    raw_structured_planning_block,
+                    rewards_box=raw_structured_rewards_box,
+                    planning_block=raw_structured_planning_block,
+                    allow_injection=True,
                 )
```

## Motivation
A P0 bug was identified where raw LLM payloads were bypassing normalization in the streaming fallback path, causing un-normalized rewards box data to persist to Firestore.