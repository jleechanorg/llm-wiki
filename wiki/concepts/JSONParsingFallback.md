---
title: "JSON Parsing Fallback"
type: concept
tags: ["json", "parsing", "error-handling"]
sources: ["json-display-bugs-analysis-report-2026-04-07"]
last_updated: 2026-04-07
---

## Description
A robust parsing strategy that handles malformed JSON by attempting multiple extraction methods in sequence.

## Pattern
When primary JSON parsing fails, fallback strategies are applied:
1. Try standard JSON parsing
2. Try regex extraction of narrative field
3. Attempt partial JSON recovery
4. Return graceful error with minimal data

## Related Concepts
- [[Structured Response]] - The JSON format being parsed
- [[Robust JSON Parser]] - The component implementing fallback handling
