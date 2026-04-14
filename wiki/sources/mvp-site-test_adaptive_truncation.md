---
title: "test_adaptive_truncation.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Test suite for adaptive context truncation functionality in the LLM service. Tests cover iterative turn reduction when context exceeds model limits, percentage-based allocation (25% start, 60% end), middle turn compaction with keyword extraction, improved sentence splitting, and pattern-based importance detection.

## Key Claims
- Adaptive truncation iteratively reduces turns until content fits, preventing ContextTooLargeError for smaller context models like Cerebras 131K
- Middle compaction extracts key events (dice rolls, damage, dialogue) instead of dropping content
- Sentence splitting handles abbreviations (Dr., Mr.) and decimals (3.14) without false splits
- Importance detection is language-agnostic, relying on pattern matching rather than semantic analysis

## Connections
- [[mvp-site-llm_service]] — implements the truncation logic tested here
- [[mvp-site-constants]] — provider constants define supported LLM backends