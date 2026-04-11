---
title: "JSON Parsing Changes - PR #3458"
type: source
tags: [worldarchitect-ai, pr-3458, json-parsing, migration, breaking-changes]
sources: []
last_updated: 2026-04-07
---

## Summary

PR #3458 removed regex-based JSON parsing and recovery functionality, standardizing on `json.loads()` only. This is a breaking change that shifts from graceful degradation to fail-fast behavior — LLM providers must now return complete, valid JSON.

## Key Claims

- **Regex fallback removed** — 729 lines deleted from `json_utils.py`, 135+ lines removed from `narrative_response_schema.py`
- **Fail-fast behavior** — Invalid, truncated, or text-wrapped JSON now fails completely instead of being recovered
- **Markdown code block extraction still works** — JSON inside ``` code blocks is still extracted automatically
- **Provider requirements increased** — LLM providers must now return complete JSON with no extra text

## Key Quotes

> "Invalid JSON response received. Please try again." — New error message when JSON parsing fails

## Connections

- Related to [[Iteration 007 Final Campaign Analysis]] — iteration testing may be affected by stricter JSON parsing
- Related to [[Security Fixes for PR #1294 Follow-up]] — both involve security/robustness improvements

## Contradictions

- None identified — this is a new source not contradicting existing content