---
title: "Story Truncation"
type: concept
tags: [narrative, context, optimization]
sources: ["context-budget-design-document"]
last_updated: 2026-04-08
---

## Description
Mechanism for fitting story context within token limits by selectively preserving portions of conversation history. Uses percentage-based allocation rather than fixed truncation.

## Approach
- **Start turns**: 25% of story budget — context setup
- **Middle summary**: 10% — compacted key events from dropped turns
- **End turns**: 60% — recent action turns
- **Truncation marker**: 5% — safety margin

## Difference from Legacy
- Legacy: Fixed 20+20 turn truncation
- New: Percentage-based handles variable turn lengths

## Related Pages
- [[Context Budget]] — system containing truncation
- [[Token Management]] — related concept
