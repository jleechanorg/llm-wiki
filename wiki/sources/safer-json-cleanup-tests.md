---
title: "Safer JSON Cleanup Tests"
type: source
tags: [python, testing, json, narrative, parsing]
source_file: "raw/test_json_cleanup_safety.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite verifying that narrative text containing JSON-like patterns is preserved during parsing. Tests validate that JSON syntax within story text (brackets, quotes, braces) isn't corrupted by aggressive cleanup, while truly malformed JSON still triggers appropriate error handling.

## Key Claims
- **Narrative preservation**: Valid JSON responses preserve all JSON-like characters in narrative text ({, }, [, ], quotes)
- **Malformed JSON handling**: Clearly broken JSON (missing quotes, unclosed braces) triggers error message instead of aggressive cleanup
- **Context-aware detection**: JSON artifact detection distinguishes actual JSON from text with incidental JSON-like characters
- **Recovery disabled**: Recovery mechanism is disabled - invalid JSON returns error narrative rather than attempting repair

## Key Quotes
> "The wizard says: 'Cast {spell} with [\"power\": 10]!' He winks." — nested braces and quotes in narrative preserved

> "The party enters the {treasure room} and finds [gold coins]." — plain text with JSON-like chars handled as text

## Connections
- [[parse_structured_response]] — main function under test; extracts narrative from JSON or returns error
- [[clean_json_artifacts]] — cleanup function that would corrupt narrative if aggressive
- [[contains_json_artifacts]] — detection function for JSON vs narrative text

## Contradictions
- None identified — tests confirm current behavior is safe
