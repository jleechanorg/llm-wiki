---
title: "JSON Truncation"
type: concept
tags: [json, bugs, context-management]
sources: [json-truncation-handling-tests]
last_updated: 2026-04-08
---

Bug pattern where JSON strings are truncated at arbitrary character boundaries, producing invalid JSON structures.

## Problem
Truncating JSON mid-object breaks parseability:
```json
{"location":"village","time":"morn  // Invalid - truncated
```

## Solution
When budget exceeded, return original JSON instead of producing invalid output.

## Related
- [[CompactGameState]] — function with this bug
- [[BudgetHandling]] — correct pattern
