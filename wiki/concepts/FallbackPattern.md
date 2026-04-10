---
title: "Fallback Pattern"
type: concept
tags: [error-handling, resilience, defaults]
sources: []
last_updated: 2026-04-08
---

Software design pattern where a secondary value is used when the primary value is unavailable, invalid, or errors out. The centralized model selection uses this pattern extensively.

## Examples in Model Selection
- No user → default model
- Invalid preference → default model
- Database error → default model

## Related
- [[Centralized Model Selection]] — uses this pattern
- [[DEFAULT_MODEL]] — fallback value
