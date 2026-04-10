---
title: "JSON Artifact Detection"
type: concept
tags: [json, detection, parsing]
sources: [safer-json-cleanup-tests]
last_updated: 2026-04-08
---

## Summary
Detection logic distinguishing actual JSON responses from plain text containing incidental JSON-like characters.

## Detection Criteria
- Starts with `{` and ends with `}`: likely JSON
- Contains escaped quotes `\"`: likely JSON
- Has quoted field names: likely JSON
- Plain text with `{word}` or `[word]`: not JSON

## Related Functions
- [[contains_json_artifacts]] — detection predicate
- [[clean_json_artifacts]] — cleanup/ normalization (not used in current implementation)
