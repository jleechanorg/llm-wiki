---
title: "Code Execution Artifact JSON Parsing Tests"
type: source
tags: [python, testing, json-parsing, code-execution, gemini, structured-response]
source_file: "raw/test_code_execution_artifact_json_parsing.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating Gemini code execution artifact handling in JSON parsing. Tests verify that parse_structured_response() correctly handles responses when code execution mode is used, which can include whitespace or code output before the actual JSON response.

## Key Claims
- **Whitespace Prefix**: Leading whitespace and newlines before JSON are stripped correctly
- **Array Before Object**: When code execution outputs array (dice rolls) followed by JSON object, parsing prefers { over [ to find the main response
- **Mixed Output**: Realistic code execution scenarios with stdout prefix followed by JSON are handled
- **Tab/CR Handling**: Tab characters and carriage return prefixes are processed correctly

## Key Test Cases
1. `test_code_execution_whitespace_prefix` — validates whitespace removal
2. `test_code_execution_stdout_prefix` — validates array+object scenario
3. `test_code_execution_mixed_output` — validates production-like patterns
4. `test_code_execution_tab_prefix` — validates tab handling
5. `test_code_execution_carriage_return_prefix` — validates CR handling
6. `test_code_execution_with_array_first` — validates object preference over array

## Connections
- [[parse_structured_response]] — function being tested in narrative_response_schema
- [[CodeExecutionMode]] — Gemini mode that produces artifacts before JSON

## Contradictions
- None identified
