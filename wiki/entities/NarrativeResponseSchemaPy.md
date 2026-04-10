---
title: "NarrativeResponseSchema.py"
type: entity
tags: [python, file, parsing, llm]
sources: ["fallback-behavior-review-mvp-site"]
last_updated: 2026-04-08
---

Narrative response parsing module with multi-layer fallback:
- Extracts known fields from malformed JSON
- Regex-parses narrative text
- Cleans JSON-like strings

## Rationale
Upstream LLM responses are nondeterministic; user-facing flows need readable output rather than crashes. Does not hide configuration errors.
