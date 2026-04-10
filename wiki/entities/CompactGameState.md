---
title: "CompactGameState"
type: entity
tags: [function, context-compaction]
sources: [json-truncation-handling-tests]
last_updated: 2026-04-08
---

Function in `mvp_site.context_compaction` that compacts game_state JSON to fit within budget constraints.

## Purpose
Reduces JSON payload size when context window limits are approached.

## Current Bug
Lines 579-581 truncate JSON string with `compacted_json[:max_chars]`, producing invalid JSON when truncation cuts mid-object.

## Expected Behavior
When compaction would exceed budget, return original game_state instead of truncated invalid JSON.


## Related
- [[JSONTruncation]] — the bug pattern
- [[ContextCompaction]] — parent module
