---
title: "Gemini Code Execution"
type: concept
tags: [gemini, code-execution, llm-capabilities]
sources: []
last_updated: 2026-04-08
---

## Definition
Gemini's code execution capability allows the model to generate and execute code snippets, returning structured evidence about the execution. Part types include `executable_code` (code to run) and `code_execution_result` (output from execution).

## Usage in WorldAI
The `mvp_site.llm_providers.gemini_code_execution` module provides utilities:
- `extract_code_execution_evidence()` — detects if code execution was used and counts parts
- `extract_code_execution_parts_summary()` — summarizes parts with truncation for large content

## Key Patterns
- Evidence extraction returns structured dict with boolean `code_execution_used` flag
- Truncation adds "...(truncated)" suffix when content exceeds `max_chars`
- Supports multiple candidates and parts per response

## Streaming Instruction/Tool Parity

2026-06-06 WorldArchitect RCA: do not send code-execution instructions on a
Gemini request path unless the request also attaches the actual
`code_execution` tool. A streaming turn for campaign `8J0RzsHVHH1GLg6E6BLM`
returned a JSON list of inert `tool=code_execution` objects with `args.code`
but no normal `text` and no observed `code_execution_result.output`. Text-only
extraction then dropped the answer and parser fail-open persisted
`The story continues...`.

Operational rule: on placeholder/fail-open incidents, inspect raw response part
types (`text`, `executable_code`, `code_execution_result`, tool/function parts)
and compare streaming vs non-streaming tool config before blaming model
narrative quality or frontend truncation.
