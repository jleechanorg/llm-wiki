---
title: "Month Name Normalization"
type: concept
tags: [normalization, temporal, strings]
sources: []
last_updated: 2026-04-08
---

## Definition
Process of cleaning month names from LLM responses before parsing, specifically removing trailing punctuation that would cause incorrect month parsing.

## Key Aspects
- Some LLM responses include month names with trailing punctuation (e.g., "Kythorn.", "Mirtul.")
- Without normalization, "Kythorn." is parsed as month 0, which is less than valid months (1-12)
- This causes false temporal violation flags for future times with punctuated months
- Normalization strips punctuation before month name lookup

## Related Tests
- [[Temporal Violation Edge Cases — Punctuated Month Names and Equal Timestamps]]
