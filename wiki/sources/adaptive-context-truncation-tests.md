---
title: "Adaptive Context Truncation Tests"
type: source
tags: [python, testing, unittest, context-truncation, cerebras, token-estimation]
source_file: "raw/adaptive-context-truncation-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest file testing adaptive context truncation for smaller context window models like Cerebras 131K. Validates iterative reduction of turns when content exceeds model budget, preventing ContextTooLargeError.

## Key Claims
- **Adaptive Reduction**: Truncation iteratively reduces turns until content fits within context budget
- **Minimum Preservation**: Keeps at least 3 start + 5 end turns even under extreme budget pressure
- **No Change When Under Budget**: Returns original content unchanged when within budget
- **Recent Context Priority**: Preserves recent (end) context over older content

## Key Quotes
> "Previously, truncation kept a fixed 40 turns regardless of whether that fit, causing context overflow for long narrative entries."

## Connections
- [[Cerebras]] — target model with smaller 131K context window
- [[Token Estimation]] — mechanism for calculating context size
- [[Context Truncation]] — core concept being tested

## Contradictions
- None identified
