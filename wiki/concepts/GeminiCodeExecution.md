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
