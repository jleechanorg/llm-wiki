---
title: "Temporal Violation"
type: concept
tags: [temporal, validation, game-state]
sources: []
last_updated: 2026-04-08
---

## Definition
A flag indicating the LLM generated a backward time jump in the game world. Occurs when new_time < old_time in complete temporal data.

## Detection Rules
- **Complete backward time**: Flagged as violation (year/month/day all present and new < old)
- **Incomplete time**: NOT flagged (missing fields = malformed data, not backward travel)
- **Year 0**: NOT flagged (invalid year treated as malformed)
- **None values**: NOT flagged (graceful handling of missing data)

## Related
- [[TemporalCorrection]] — handles violation response
- [[WorldTime]] — time tracking module
