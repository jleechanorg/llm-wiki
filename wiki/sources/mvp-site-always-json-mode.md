---
title: "test_always_json_mode.py"
type: source
tags: [testing, json-mode, llm, structured-response]
date: 2026-04-14
source_file: raw/mvp_site_all/test_always_json_mode.py
---

## Summary
Tests that JSON mode is always used for all LLM calls. Verifies JSON-first responses with separate planning_block field containing thinking, context, and choices. Tests entity tracking requirements in structured prompt injection.

## Key Claims
- JSON mode is always enabled internally (no use_json_mode parameter needed)
- Response narrative is clean text without planning block JSON embedded
- Structured response contains planning_block as dictionary with choices
- create_generic_json_instruction returns empty string when always-JSON mode is enabled
- create_structured_prompt_injection includes entity tracking requirements when entities present

## Key Quotes
> "JSON mode is now always enabled internally, no need to check for use_json_mode parameter"

## Connections
- [[mvp-site-llm-service]] — LLM service with always-JSON mode
- [[mvp-site-narrative-response-schema]] — Structured response schemas

## Contradictions
- None identified in test file