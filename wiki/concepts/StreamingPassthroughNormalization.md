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

## Connections
- [[RewardsBoxSchema]] — Schema definition
- [[CentralizedNumericExtraction]] — Numeric extraction
- [[RewardsBoxObservability]] — Observability for normalized data
- [[StreamingResponseParsing]] — Streaming response parsing
