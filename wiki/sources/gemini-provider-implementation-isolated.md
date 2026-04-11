---
title: "Gemini Provider — llm_service Isolation"
type: source
tags: [gemini-api, llm-service, code-execution, dice-mechanics, sdk-limitations]
source_file: "raw/gemini-provider-implementation-isolated.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Gemini provider implementation isolated from llm_service module. Uses `response_mime_type="application/json"` for JSON format enforcement. Schema validation is NOT enforced at API level due to SDK limitations with `additionalProperties`. The Gemini API itself supports `additionalProperties` since Nov 2025, but the google-genai Python SDK has stricter client-side validation that rejects it.

## Key Claims
- **SDK Limitation**: google-genai Python SDK has stricter client-side validation than the Gemini API itself, blocking `additionalProperties: true` needed for dynamic game state keys
- **Current Approach**: `response_mime_type="application/json"` + prompt instructions + post-response validation in `narrative_response_schema.py`
- **Code Execution Mode**: REV-65v filters out dice tool names (`roll_dice`, `roll_attack`, `roll_skill_check`, `roll_saving_throw`) when using code_execution, forcing Python `random.randint()` execution
- **Mandatory Protocol**: DC must be set BEFORE rolling, all dice mechanics require code execution with Python's random.randint()

## Key Quotes
> "The Gemini API itself SUPPORTS additionalProperties since Nov 2025... BUT the google-genai Python SDK has stricter client-side validation that rejects it" — SDK limitation context

> "Dice results are quantum-random. Like checking real-world temperature, you MUST query the random number generator to OBSERVE the value." — CODE_EXECUTION_DICE_OVERRIDE instructions

## Connections
- [[GeminiCodeExecutionEvidenceHelpers]] — evidence detection for RNG usage in code_execution
- [[DiceValuesAreUnknowableCodeExecutionProtocol]] — mandatory random.randint() protocol
- [[DiceStrategySelection]] — decides between code_execution and native_two_phase

## Contradictions
- None identified — this source complements existing dice mechanics documentation

## Potential Workarounds (Not Yet Tested)
1. Use `response_json_schema` with manual schema dict (might bypass SDK validation)
2. Restructure game state to use `List[KeyValuePair]` instead of dynamic dicts
3. Wait for SDK fix (unlikely based on NOT_PLANNED status)
