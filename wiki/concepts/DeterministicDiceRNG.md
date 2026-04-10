---
title: "Deterministic Dice RNG"
type: concept
tags: [dice, testing, rng, deterministic, reproducibility]
sources: []
last_updated: 2026-04-08
---

## Definition
Testing mechanism that enables reproducible dice rolls by seeding the random number generator via DICE_SEED environment variable. Used for generating consistent test evidence.

## Implementation
```python
_DICE_SEED = os.getenv("DICE_SEED")
if _DICE_SEED:
    _DICE_RNG = random.Random(int(_DICE_SEED))
else:
    _DICE_RNG = random  # Use system RNG
```

## Use Cases
- Creating reproducible test scenarios
- Generating consistent evidence for test captures
- Debugging dice-related issues with known roll sequences

## Related Concepts
- [[DiceRollResult]] — the data structure for roll results
- [[Data Capture Framework]] — test evidence capture system
- [[Real-Mode Testing]] — testing with real service interactions
