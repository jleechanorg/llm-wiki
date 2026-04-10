---
title: "God Mode Placeholder Validation"
type: concept
tags: [god-mode, validation, testing, placeholder-detection]
sources: []
last_updated: 2026-04-08
---

## Summary
Validation logic that distinguishes between placeholder content (which should be ignored) and actual narrative prose (which triggers `GOD_MODE_VIOLATION` warnings) in god mode responses.

## Validation Rules

### Pass (No Warning)
- Empty strings ("")
- Whitespace-only content
- `[SESSION_HEADER]` markers
- `[Mode: GOD MODE]` markers
- Timestamp metadata ("Timestamp: 209 AC, Month 5 Day 1")
- Short non-prose (<50 chars, no periods)
- Combined placeholder patterns

### Fail (Warning Triggered)
- Actual narrative prose (sentences with periods)
- Long content without metadata markers (>50 chars)
- Prose containing placeholder substrings
- Prose ending with placeholder text

## Implementation
Uses `startswith()` check to detect embedded placeholders within prose text, ensuring content like "Status: You fight the dragon" triggers warning.

## Related
- [[NarrativeResponseSchema]] — response schema
- [[GODMode]] — god mode functionality
