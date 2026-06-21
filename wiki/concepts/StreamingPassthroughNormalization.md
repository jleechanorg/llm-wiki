---
title: "Streaming Passthrough Normalization"
type: concept
tags: [streaming, normalization, rewards, worldai]
last_updated: 2026-04-14
---

## Summary

Streaming Passthrough Normalization ensures that rewards boxes flowing through the streaming LLM path are normalized before being persisted to Firestore, even when no UI signal is detected.

## The Problem

The streaming path (LLM → llm_parser → rewards_engine → Firestore) had a "passthrough" branch where `_has_level_up_ui_signal == False`. In this branch, the raw LLM rewards_box was returned without normalization:

```python
# BEFORE (buggy)
if _has_level_up_ui_signal:
    normalized = normalize_rewards_box_for_ui(raw_rewards_box)
    return normalized
else:
    return raw_rewards_box  # ❌ NOT NORMALIZED
```

## The Fix

```python
# AFTER (fixed)
if _has_level_up_ui_signal:
    normalized = normalize_rewards_box_for_ui(raw_rewards_box)
    return normalized
else:
    normalized = normalize_rewards_box_for_ui(raw_rewards_box)
    return normalized  # ✅ Always normalize
```

## Why Both Branches Normalize

1. **Schema compliance** — All Firestore writes must pass schema validation
2. **Numeric bounds** — Raw LLM output could exceed MAX_REWARDS
3. **Consistency** — Both paths produce identical output shape

## PR #6565 Update (2026-04-23) — backfilled 2026-06-21

PR #6565 ensures all code paths (streaming, polling, passthrough) call `normalize_rewards_box_for_ui()` before Firestore persistence. The MCP test harness proves atomicity at the JSON-RPC layer. However, the streaming path (`/interaction/stream`) was NOT exercised in the evidence bundle (0 streaming scenarios in `streaming_evidence.json`; `collection_log.txt` missing from artifacts), leaving a gap in the streaming normalization proof. This backfill captures the design intent; production streaming evidence is still pending.

Source: [PR #6565 — ZFC M0 Stabilization Bridge — 2026-04-23](../sources/2026-04-23-pr6565-zfc-m0-stabilization-bridge.md).

## Connections
- [RewardsBoxSchema](RewardsBoxSchema.md) — Schema definition
- [CentralizedNumericExtraction](CentralizedNumericExtraction.md) — Numeric extraction
- [RewardsBoxObservability](RewardsBoxObservability.md) — Observability for normalized data
- [StreamingResponseParsing](StreamingResponseParsing.md) — Streaming response parsing
