---
title: "Adaptive Context Truncation"
type: concept
tags: [context-management, token-optimization, model-limits]
sources: [adaptive-context-truncation-tests]
last_updated: 2026-04-08
---

## Description
An algorithm that iteratively reduces the number of conversation turns when content exceeds the model's context budget. Unlike fixed truncation (e.g., always keeping 40 turns), adaptive truncation dynamically adjusts turn count based on actual content size to prevent ContextTooLargeError.

## Key Mechanics
- **Initial Calculation**: Attempts 20 user + 20 system turns (40 total)
- **Iterative Reduction**: If exceeding budget, removes middle turns progressively
- **Minimum Threshold**: Preserves at least 3 start turns + 5 end turns
- **Marker Insertion**: Adds truncation marker to indicate omitted content

## Connections
- [[Token Estimation]] — calculates content size to determine truncation needs
- [[Cerebras]] — target use case: models with smaller context windows
- [[Context Budget]] — the maximum token allowance for model input
- [[MetaHarness]] — contrast: Meta-Harness optimizes WHAT context to present, while truncation only makes existing context fit
