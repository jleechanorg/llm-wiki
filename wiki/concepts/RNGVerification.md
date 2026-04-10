---
title: "RNG Verification"
type: concept
tags: [random-number-generation, dice, verification, code-execution]
sources: ["code-execution-evidence-extraction-rng-verification-tests"]
last_updated: 2026-04-08
---

## Definition

Process of verifying that dice roll results were generated using genuine random number generation (RNG) rather than being fabricated or hardcoded by the LLM.

## Implementation

The `extract_code_execution_evidence()` function in `gemini_provider` inspects executed code to determine:

1. **code_contains_rng**: Does the code include `random.randint()`, `random.choice()`, or other RNG functions?
2. **rng_verified**: Boolean flag indicating whether genuine RNG was used

## Verification Criteria

- Code must contain actual random number generation (e.g., `random.randint(1, 20)`)
- Output must match what the code would produce
- Both code and result must be present in the response

## Why It Matters

Without RNG verification, LLMs could fabricate dice roll results that look legitimate but weren't actually computed. The verification ensures provably fair gameplay by confirming that dice rolls are genuinely random.

## Related Concepts

- [[Code Execution Fabrication Detection]] — flags rolls that lack RNG verification
- [[Provably Fair]] — broader concept of verifiable game integrity
- [[Code Execution Evidence Extraction]] — the mechanism that collects RNG verification data
