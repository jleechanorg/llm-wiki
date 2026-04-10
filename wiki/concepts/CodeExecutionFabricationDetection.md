---
title: "Code Execution Fabrication Detection"
type: concept
tags: [dice-integrity, code-execution, testing, fraud-detection]
sources: ["code-execution-evidence-extraction-rng-verification-tests"]
last_updated: 2026-04-08
---

## Definition

Mechanism to detect when code execution results are fabricated rather than genuinely computed. In the context of LLM-based dice rolling, fabrication detection ensures that dice rolls reported by the LLM were actually computed using real random number generation rather than invented results.

## How It Works

The `_is_code_execution_fabrication()` function in `mvp_site.dice_integrity` evaluates whether evidence suggests fabricated dice rolls:

1. **Presence of Dice**: Checks if the structured response contains mechanics.rolls or mechanics.audit_events
2. **Evidence Analysis**: Evaluates the evidence dict for code_execution_used, rng_verified, and code_contains_rng flags
3. **Edge Cases**: Handles empty evidence dicts (still flags fabrication when dice present) and legacy string audit_events

## Key Rules

- Empty evidence dict with dice present → FABRICATION (still flagged)
- Legacy string audit_events with no rolls → counts as dice evidence
- Code without random.randint() → FABRICATION even if output looks valid
- RNG-verified evidence → clears fabrication flag

## Related Concepts

- [[RNG Verification]] — the complementary process of confirming genuine random number generation
- [[Code Execution Evidence Extraction]] — gathering evidence from LLM code execution responses
- [[Gemini Provider]] — the provider module that performs code execution and evidence extraction
