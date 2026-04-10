---
title: "DC Ordering Enforcement"
type: concept
tags: [dice, verification, fairness]
sources: ["dice-values-unknowable-code-execution-protocol"]
last_updated: 2026-04-08
---

DC ordering enforcement prevents "just in time" DC manipulation by requiring difficulty class assignment BEFORE random number generation.


## Rule
DC value and reasoning MUST appear in code BEFORE any `random.randint()` call.

## Why It Matters
- Prevents adjusting DC to fit narrative after seeing roll
- Proves fairness through code inspection
- Enables player verification

## Correct vs Wrong
**Correct:**
```python
dc = 15
dc_reasoning = "medium difficulty terrain"  
roll = random.randint(1, 20)
```

**Wrong:**
```python
roll = random.randint(1, 20)  # Violation
dc = 15                   # Set after roll
```

## Related Concepts
- [[DiceRollingProtocol]] — enforced by dice protocol
- [[CodeExecutionMode]] — inspection happens in this mode
