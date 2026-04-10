---
title: "NPC Pattern Matching"
type: concept
tags: [llm, extraction, character-detection]
sources: [test-character-extraction-regex-bug]
last_updated: 2026-04-08
---

Technique for extracting Non-Player Character (NPC) names from LLM prompt outputs using regular expressions.

## Patterns
1. **NPCs including**: `r"NPCs?\s+(?:including|such as)\s+([A-Z][a-z]+...)"` — handles comma-separated lists
2. **Advisor/Companion named**: `r"(?:advisor|companion|member)s?\s+(?:named?|called?)\s+([A-Z][a-z]+...)"` — handles single NPC references

## Implementation in llm_service.py
- Uses `re.findall()` to extract all matching NPC names
- Splits comma-separated matches into individual names
- Filters out common words (and, or, the, a, an)

## Connections
- [[Regex]] — underlying pattern technology
- [[CharacterCreationAgent]] — consumes NPC extraction for character setup
- [[Elena]], [[Marcus]], [[Gandalf]] — example extracted NPCs
