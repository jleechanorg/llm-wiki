---
title: "Character Counting"
type: concept
tags: [strings, metrics, logging]
sources: [token-counting-utilities]
last_updated: 2026-04-08
---

## Definition
Character counting is the fundamental operation of measuring the length of a string by counting individual characters. In WorldAI's token utilities, this serves as the base measurement for token estimation.

## Implementation Details
- Handles both single strings and lists of strings via isinstance() checks
- Filters out non-string items in lists to prevent errors
- Returns 0 for empty/None input to avoid errors

## Related Concepts
- [[TokenEstimation]] — uses character count as input
- [[TokenCountingUtilities]] — contains the character counting logic
- [[LoggingWithMetadata]] — logging that includes character/token counts
