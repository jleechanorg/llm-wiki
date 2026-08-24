---
title: "Gemini 3 ThinkingConfig Low Level and Code Execution Mutual Exclusion"
type: source
tags: [gemini-3, thinking-config, code-execution, agy-provider, llm-forensics]
date: 2026-08-23
source_file: raw/feedback_2026-08-23_gemini_3_thinking_low_and_code_execution_exclusion.md
last_updated: 2026-08-23
---

## Summary
Documents the wire configuration and runtime constraints for Gemini 3.6/3.7 Flash thinking levels across direct Gemini API SDK and Google Antigravity (AGY) CLI provider pathways. Establishes the mandatory mutual exclusion invariant where `ThinkingConfig` must be omitted when `code_execution` is enabled to avoid `400 FAILED_PRECONDITION`.

## Key Claims
- Direct Gemini SDK configures `types.ThinkingConfig(thinking_level="low")` for `gemini-3.6-flash` and `gemini-3.7-flash`.
- Gemini API endpoint strictly forbids combining `ThinkingConfig` with `code_execution` (returns `FAILED_PRECONDITION`).
- `mvp_site/llm_providers/gemini_provider.py` attaches `thinking_config` only when `allow_code_execution=False`.
- AGY CLI provider routes thinking levels via explicit model label aliases (`Gemini 3.5 Flash (Low)`, `Gemini 3.6 Flash (Low)`, `Gemini 3.7 Flash (Low)`) selected via `AGY_LOW_THINKING_OPT_IN=1`.
- Both pathways record serialized configuration and model labels in BigQuery `worldarchitecture-ai.llm_forensics.llm_payloads`.

## Connections
- [[GeminiProvider]] — Direct SDK provider handling `ThinkingConfig` and BQ serialization
- [[AgyProvider]] — CLI provider executing headless `agy` with model aliases
- [[BigQueryForensics]] — Telemetry sink verifying request/response payloads
