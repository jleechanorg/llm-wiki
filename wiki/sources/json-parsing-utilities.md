---
title: "JSON Parsing Utilities for Robust Extraction"
type: source
tags: [json, parsing, extraction, utilities, llm-responses, text-processing]
source_file: "raw/json-parsing-utilities.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Module providing tools for extracting valid JSON from text that may contain artifacts like code execution output, logs, or markdown formatting. Includes brace matching and intelligent JSON candidate selection.

## Key Claims
- **Brace Matching**: `find_matching_brace()` finds closing brace/bracket matching an opening one, respecting string boundaries and escape sequences
- **Best JSON Extraction**: `extract_best_json()` scans text for all valid JSON objects/arrays and returns the best candidate using a scoring function
- **Default Scoring**: Prioritizes objects with "narrative" key (+500 points) or "god_mode_response" key (+500 points), then by size
- **Custom Scoring**: Users can provide custom scoring functions to prioritize specific JSON structures
- **LLM Response Handling**: Designed for parsing LLM responses containing code artifacts, markdown, and logging output

## Connections
- [[mvp_site]] — project where this utility is used
- [[LoggingUtil]] — logging module imported from mvp_site
