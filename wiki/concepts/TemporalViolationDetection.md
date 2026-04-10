---
title: "Temporal Violation Detection"
type: concept
tags: [temporal, game-state, validation]
sources: []
last_updated: 2026-04-08
---

## Definition
System for detecting when AI responses create time paradoxes by providing timestamps that go backward in game time.

## Key Aspects
- Compares new timestamp against previous world_time to detect backward jumps
- Must handle malformed data gracefully (e.g., incomplete time fields)
- Must normalize month names with trailing punctuation before comparison
- Equal timestamps should not trigger warnings (no time has passed)

## Related Tests
- [[Temporal Correction Loop Tests]]
- [[Temporal Violation Edge Cases — Punctuated Month Names and Equal Timestamps]]
- [[Temporal Correction Misleading Success Message Bug]]
