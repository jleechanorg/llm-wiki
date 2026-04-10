---
title: "Division by Zero"
type: concept
tags: [python, error-handling, testing]
sources: []
last_updated: 2026-04-08
---

## Description
Software bug that occurs when dividing by zero. In the context of GameState.validate_checkpoint_consistency, this could occur when computing HP percentages if hp_max=0. The fix adds guard conditions to check for zero hp_max before performing division operations.

## Related Concepts
- [[Checkpoint Validation]] — validates save state consistency
- [[HP Validation]] — validates HP values (hp_current, hp_max)

## Example
```python
# Before fix (could raise ZeroDivisionError):
percentage = (hp_current / hp_max) * 100

# After fix (safe):
if hp_max > 0:
    percentage = (hp_current / hp_max) * 100
```
