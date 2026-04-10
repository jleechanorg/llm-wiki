---
title: "Regex"
type: concept
tags: [python, pattern-matching, text-processing]
sources: [test-character-extraction-regex-bug]
last_updated: 2026-04-08
---

Regular expressions (regex) in Python using the `re` module for pattern matching and text extraction.

## Details
- **Module**: `re` — Python's built-in regular expression module
- **Functions Used**: `re.findall()`, `re.search()`
- **Flags**: `re.IGNORECASE` for case-insensitive matching

## Patterns in llm_service
1. NPC extraction: `r"NPCs?\s+(?:including|such as)\s+([A-Z][a-z]+...)"`
2. Advisor extraction: `r"(?:advisor|companion|member)s?\s+(?:named?|called?)\s+([A-Z][a-z]+...)"`
3. Character creation detection: `r"\[CHARACTER CREATION"`

## Connections
- [[NPCPatternMatching]] — application of regex for NPC extraction
- [[llm_service]] — uses regex for character detection
