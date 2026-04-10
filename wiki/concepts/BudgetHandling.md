---
title: "Budget Handling"
type: concept
tags: [context-management, safety]
sources: [json-truncation-handling-tests]
last_updated: 2026-04-08
---

Pattern where operations respect size constraints by falling back to safe defaults instead of producing invalid output.

## Safe Fallback Pattern
When an operation would exceed budget, return the original state rather than produce corrupted output.

## Example
_compact_game_state should return original game_state when compacted JSON exceeds max_chars, not truncate and produce invalid JSON.

## Related
- [[CompactGameState]] — applies this pattern
- [[JSONTruncation]] — anti-pattern to avoid
