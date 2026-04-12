---
title: "DiceProviderFallback"
type: concept
tags: [dice, model, flash-lite, code-execution, worldarchitect]
sources: [rev-xxsx]
last_updated: 2026-04-12
---

## Summary

`DiceProviderFallback` is the pattern where the dice rolling system falls back to a non-code-execution path when the flash-lite model (which is excluded from `MODELS_WITH_CODE_EXECUTION`) is in use.

## The Mechanism

The `MODELS_WITH_CODE_EXECUTION` constant lists which models are allowed to execute generated dice-rolling code. When a model is NOT in this list (e.g., flash-lite variants), the dice system silently falls back to a deterministic roll path without explicit notification.

## Code Pattern

```python
# MODELS_WITH_CODE_EXECUTION excludes flash-lite
if model_name not in MODELS_WITH_CODE_EXECUTION:
    # Use non-code-execution fallback for dice rolls
    return deterministic_roll(dice_spec)
```

## Implication

Games running on flash-lite model tiers get deterministic dice rolls (same input → same output) rather than true random rolls with code execution. This is by design but can surprise players expecting genuine randomness.

## Related

- [[DiceSystemRequirement]] — Dice system requirements
- [[Harness5LayerModel]] — Model tier considerations
