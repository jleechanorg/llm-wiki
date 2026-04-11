---
title: "Regression Test: _maybe_get_gemini_code_execution_evidence Context Parameter"
type: source
tags: [python, testing, regression, gemini, typeerror]
source_file: "raw/test_gemini_code_execution_evidence_context.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Regression test ensuring `_maybe_get_gemini_code_execution_evidence` is called with the required `context` keyword argument. The test uses AST parsing to verify the function call includes the context parameter, making it robust to code formatting changes.

## Key Claims
- **continue_story() calls _maybe_get_gemini_code_execution_evidence with context**: The function must pass `context='continue_story'` to prevent TypeError
- **TypeError prevention**: Missing context parameter causes "TypeError: missing 1 required keyword-only argument: 'context'"
- **AST-based verification**: Uses Python AST parsing instead of string matching for robust test against formatting changes

## Key Test Cases
- `test_continue_story_calls_maybe_get_gemini_code_execution_evidence_with_context`: Verifies the function call includes context keyword
- `test_maybe_get_gemini_code_execution_evidence_requires_context_parameter`: Verifies TypeError is raised when context is missing

## Connections
- [[LLMService]] — module containing continue_story()
- [[GeminiAPI]] — provider being tested
- [[ASTParsing]] — technique used for verification

## Contradictions
- None
