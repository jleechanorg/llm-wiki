---
title: "Centralized Numeric Extraction"
type: concept
tags: [numeric-extraction, llm, parsing, canonical, worldai]
last_updated: 2026-04-14
---

## Summary

Numeric extraction in LLM responses should be centralized in a single module rather than scattered across parsers. This ensures consistent handling of decimal separators, units, and ambiguous number formats (e.g., "2.5M" vs "2500000").

## Canonical Pattern

**Single extraction function**:
```python
def extract_number(text: str) -> float | None:
    """Canonical number extraction from LLM text output."""
    patterns = [
        r"(\d+(?:\.\d+)?)\s*(?:million|billion|m|b)?",
        r"\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)",
        r"(-?\d+(?:\.\d+)?)",
    ]
    for pattern in patterns:
        if match := re.search(pattern, text, re.IGNORECASE):
            return parse_number_string(match.group(1))
    return None
```

## Why Centralize

1. **Consistency** — All numeric outputs from LLMs use the same parsing rules
2. **Testability** — Single test suite covers all extraction
3. **Debugging** — One place to add logging/tracing
4. **Schema drift prevention** — If the LLM changes output format, one place to update

## Validation Layer

Always validate extracted numbers against expected ranges:
```python
def validate_rewards_box(numeric_value: float, context: dict) -> bool:
    if not 0 <= numeric_value <= MAX_REWARDS:
        return False
    return True
```

## Connections
- [[CanonicalCodePatterns]] — Parent canonical pattern
- [[RewardsBoxSchema]] — Rewards-specific schema
- [[StreamingPassthroughNormalization]] — Normalization in streaming path
