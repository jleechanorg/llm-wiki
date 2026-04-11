---
title: "Banned Names Visibility Behavior Tests"
type: source
tags: [python, testing, unittest, world-loader, banned-names, visibility]
source_file: "raw/banned-names-visibility-behavior-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite verifying that banned naming restrictions are properly identifiable in world content. Tests check for structure markers, source identification, and enforcement directives without relying on exact content strings.

## Key Claims
- **Naming Restrictions Section**: World content must have clearly marked section with naming restrictions (section markers + naming keywords + restriction keywords)
- **Source Identification**: Content must identify where naming restrictions come from (specific file/source reference)
- **Enforcement Directive**: Banned names content must include enforcement instructions (must/never + directive language)
- **Content Structure**: Combined world content should be substantial (>1000 chars) with proper section organization

## Key Test Methods
- `_has_naming_restrictions_section()`: Checks for section markers, naming keywords, and restriction keywords
- `_has_source_identification()`: Verifies content identifies the source file (.md reference)
- `_has_enforcement_directive()`: Validates presence of enforcement language

## Test Cases
1. `test_world_content_includes_naming_restrictions`: Validates naming restrictions section exists in world content
2. `test_banned_names_loader_returns_content`: Validates loader returns substantial content with enforcement directive
3. `test_world_content_structure_includes_all_sections`: Validates proper structure with world content header and section dividers

## Connections
- [[banned-names-loading-unit-tests]] — Tests file loading vs visibility behavior
- [[ai-character-banned-name-prevention-tests]] — Tests AI pre-generation name checking
- [[world-loader]] — Module being tested

## Contradictions
- None identified
