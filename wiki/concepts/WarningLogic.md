---
title: "Warning Logic"
type: concept
tags: [logging, debugging, conditional-logging, python]
sources: [story-context-tests-consolidated]
last_updated: 2026-04-08
---

## Definition
Conditional logging pattern where warning messages are only emitted when there is actual problem state to report, avoiding noisy or spam-like logging output.

## Key Principle
Only emit warnings when the condition being warned about is actually true. A warning about "no reduction" when there was no reduction is itself a false positive.

## Example
```python
# Before (always warns):
if story_tokens > 0:
    logger.warning("Story context present")

# After (only warns on actual issue):
reduction = original_tokens - reduced_tokens
if reduction > 0:
    logger.warning(f"Reduced story context by {reduction} tokens")
```

## Related Concepts
- [[TypeSafetyGuards]] — defensive checks before logging
- [[ContextCompaction]] — uses warning logic for token budget reporting
- [[LoggingBestPractices]] — structured logging patterns
