---
title: "Dormant Duplication Guard"
type: concept
tags: [guardrails, timeline, testing, bug-prevention]
sources: [timeline-log-budget-end2end-tests]
last_updated: 2026-04-08
---

A guardrail that prevents duplicated entries in timeline_log when story_context grows large. Activates when context reaches approximately 80+ turns to prevent false duplication from stale or dormant entries.

## Purpose
- Prevents timeline_log from accumulating duplicate entries
- Handles edge case where old story_context entries might be re-added
- Ensures timeline accuracy for long-running campaigns

## Testing
Validated via [[Timeline Log Budget End-to-End Tests]] which creates 80-turn story context to trigger the guard

## Connections
- [[Timeline Log]] — the data structure being guarded
- [[Story Context]] — the input that triggers guard activation
- [[Sequence ID Budget Enforcement]] — related budget mechanism
