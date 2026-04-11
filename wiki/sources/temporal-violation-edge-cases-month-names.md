---
title: "Temporal Violation Edge Cases — Punctuated Month Names and Equal Timestamps"
type: source
tags: [testing, python, temporal, game-state, edge-cases]
source_file: "raw/temporal-violation-edge-cases-month-names.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for temporal violation detection edge cases: trailing punctuation on month names (e.g., "Kythorn.") should not cause false backward time flags, and equal timestamps should not trigger temporal anomaly warnings.

## Key Claims
- **Punctuated Month Names**: Month names with trailing punctuation (e.g., "Kythorn.") must be normalized before comparison to avoid treating the month as zero
- **Equal Timestamps**: Identical timestamps should not surface a temporal anomaly warning — no time has passed
- **Bug Root Cause**: Previously, "Kythorn." was compared as-is, causing the month to be parsed as 0, which is less than any valid month (1-12), triggering a false backward violation

## Key Quotes
> "Some LLM responses include month names with trailing punctuation (e.g., 'Kythorn.'), which previously caused the temporal comparison to treat the month as zero" — explains the bug that motivated these tests

## Connections
- [[Temporal Correction Loop Tests]] — related temporal handling tests
- [[Temporal Correction Misleading Success Message Bug]] — related temporal correction logic

## Contradictions
- None identified
