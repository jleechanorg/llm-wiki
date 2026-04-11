---
title: "TDD Tests for Character/NPC Extraction Regex Bug"
type: source
tags: [python, testing, tdd, regex, character-extraction, npc]
source_file: "raw/test_character_extraction_regex_bug.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Red-Green test suite validating that the `re` module is properly imported in `llm_service.py` and that NPC pattern extraction works correctly. Tests verify `re.findall` for extracting character names from prompts and `re.search` for detecting character creation blocks.

## Key Claims
- **re Module Import**: The `re` module must be properly imported in llm_service.py scope for NPC extraction to work
- **NPC Pattern Extraction**: Uses `re.findall` with two patterns to extract character names from prompts containing "NPCs including" and "advisor/companion named" formats
- **Character Creation Detection**: Uses `re.search` with `re.IGNORECASE` flag to detect "[CHARACTER CREATION]" blocks
- **Pattern Coverage**: Handles both comma-separated NPC lists (Elena, Marcus) and single NPCs (advisor named Gandalf)

## Key Quotes
> "NPCs?\s+(?:including|such as)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)*)" — pattern for extracting NPCs from prompt

## Connections
- [[llm_service]] — module being tested for regex functionality
- [[CharacterCreationAgent]] — uses character creation detection via re.search
- [[Regex]] — underlying pattern matching technology
- [[NPC]] — Non-Player Character extraction from LLM prompts

## Contradictions
- None identified — this test validates existing functionality
