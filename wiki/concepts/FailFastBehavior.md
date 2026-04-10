---
title: "Fail-Fast Behavior"
type: concept
tags: [error-handling, design-pattern]
sources: ["fallback-behavior-review-mvp-site"]
last_updated: 2026-04-08
---

Design principle where errors are surfaced immediately rather than masked with fallback values. The mvp_site fallback review identified this as the preferred approach for configuration/setup errors.

## Examples in mvp_site
- MCP functions — raise `MCPMemoryError` if handlers missing
- Firestore writes — raise `FirestoreWriteError` if document ID missing
- Game state reconstruction — return HTTP 500 instead of silent empty state
- Mock wrappers — use direct imports that fail on missing dependencies

## Contrast with Justified Fallbacks
Fail-fast is NOT appropriate for:
- Untrusted external input (LLM output parsing)
- User-facing UX errors (frontend error messages)
- Standard SPA routing patterns

## When to Apply
- Configuration errors that should be fixed, not worked around
- Missing dependencies that indicate setup problems
- Data corruption that could silently propagate
