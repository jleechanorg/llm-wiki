---
title: "Server-Owned Administrative Flags"
type: concept
tags: [rewards, server-correction, architecture]
sources: []
last_updated: 2026-01-22
---

## Definition

The Server-Owned Administrative Flags pattern is an architectural principle where the server takes responsibility for setting and maintaining administrative state (like `rewards_processed=true`) rather than relying on the LLM to set these flags reliably. This separates content generation responsibility (LLM's job) from state maintenance (server's job).

## Problem

LLMs consistently fail to set administrative flags like `rewards_processed=true` despite explicit instructions repeated 4+ times in the prompt. Prose instructions get buried in 16KB prompts, and the LLM prioritizes narrative generation.

## The Infinite Loop Problem

Without server-side enforcement, the current flow creates an infinite loop:
1. Turn N: LLM omits flag, server detects discrepancy, adds to `system_corrections`
2. Turn N+1: LLM ignores `system_corrections` (prose instructions buried)
3. Cycle repeats indefinitely

## Solution: Option D

When `_detect_rewards_discrepancy()` detects a missing flag, the server immediately sets it in `state_dict` in place — no retry, no system_corrections injection, no next-turn dependency.

```python
# In _detect_rewards_discrepancy(), when discrepancy detected:
state_dict["rewards_processed"] = True  # Server auto-sets
state_dict["rewards_box"] = original_state_dict["rewards_box"]  # Restore
```

## Architectural Principle

| Field Type | Owner | Example | Server Sets When |
|---|---|---|---|
| Administrative | Server | `rewards_processed` | Always |
| LLM Content | LLM | `dice_rolls`, `narrative` | Never (prompt enrichment only) |
| Mixed | Both | `rewards_box` | On discrepancy detection |

## Sources

- server-owned-rewards-flag.md (Option D approved/implemented)
- rewards-state-error-autocorrection.md (related)
