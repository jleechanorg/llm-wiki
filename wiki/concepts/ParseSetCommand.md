---
title: "ParseSetCommand"
type: concept
tags: [parsing, command-processing, error-handling]
sources: ["parse-set-command-error-handling-tests"]
last_updated: 2026-04-08
---

A function in `main.py` that parses set command strings into dictionaries. Takes a multi-line string with `key=value` pairs and returns a dict of parsed values.

## Error Handling Behavior
- Skips lines without `=` sign
- Silently skips invalid JSON values while logging warnings
- Handles empty keys/values gracefully
- Supports all JSON value types: strings, numbers, booleans, null, arrays, objects
- Handles escaped characters and unicode

## Related
- [[JSON Parsing]]
- [[Command Line Parsing]]
