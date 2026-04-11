---
title: "Gemini Code Execution Evidence Extraction Tests"
type: source
tags: [python, testing, gemini, code-execution, evidence-extraction]
source_file: "raw/test_gemini_code_execution_evidence.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating the `extract_code_execution_evidence` and `extract_code_execution_parts_summary` functions in `mvp_site.llm_providers.gemini_code_execution` module. Tests verify detection of executable code and code execution result parts, as well as truncation logic for large outputs.

## Key Claims
- **Code execution detection**: `extract_code_execution_evidence` correctly identifies when code execution is used by checking for `executable_code` and `code_execution_result` parts in Gemini responses
- **Evidence structure**: Returns dict with `code_execution_used`, `executable_code_parts`, and `code_execution_result_parts` counts
- **Truncation logic**: `extract_code_execution_parts_summary` truncates both code and output to `max_chars` (default 50) and adds "...(truncated)" suffix when content exceeds limits
- **Part counting**: Tracks candidate count, total parts, and samples of executable code and execution results

## Key Quotes
> "x=" + ("1" * 2000) — example of large code that gets truncated
> "...(truncated)" — suffix appended to truncated content

## Connections
- [[Gemini Code Execution]] — the module being tested
- [[Evidence Extraction]] — pattern of extracting structured data from LLM responses

## Contradictions
- None
