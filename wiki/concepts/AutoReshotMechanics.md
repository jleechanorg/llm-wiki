---
title: "Auto-Reshot Mechanics"
type: concept
tags: [auto-reshot, resubmit, validation, retry, structured-response]
sources: ["preventing-scene-backtracking-god-mode-corrections"]
last_updated: 2026-04-07
---

## Description
Automatic retry mechanism for LLM responses that fail validation or omit required fields. Instead of surfacing errors to users, the system transparently resubmits the same prompt until valid response received.

## Key Patterns
- **God-mode acknowledgement**: Resubmit until acknowledgement field appears
- **Critical deltas**: If model omits critical state deltas twice, perform guided reshot with expanded prompt
- **Silent operation**: No user-visible failures; all retries happen transparently

## References
- [[StructuredFieldsUtils]] — validates and triggers auto-reshots
- [[WorldLogic]] — process_action_unified handles retry logic
