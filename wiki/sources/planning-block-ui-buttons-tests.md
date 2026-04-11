---
title: "Test Script for Planning Block UI Buttons Functionality"
type: source
tags: [python, testing, planning-block, ui, buttons, parsing]
source_file: "raw/test_planning_block_ui_buttons.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest script validating the parsing and rendering of planning blocks as clickable buttons in the game UI. Tests cover standard planning block format with multiple choices, deep think block format with pros and cons, choice text extraction, and special character preservation without HTML escaping.

## Key Claims
- **Standard planning block format**: Validates three-choice format with id/description structure (e.g., "Action_1", "Continue_1", "Explore_2")
- **Deep think block format**: Validates option-based format with pros and cons structure (e.g., "Option_1", "Option_2", "Option_3")
- **Choice text extraction**: Validates that button data attributes contain full choice text in format "id: description"
- **Special character preservation**: Normal quotes are preserved without HTML escaping (e.g., `"Hello"` stays as `"`, not `&quot;`)

## Key Connections
- [[parsePlanningBlocks]] — JavaScript function that parses planning block JSON for button rendering
- [[PlanningBlock]] — data structure with id/description fields used in choices

## Test Cases
1. `test_standard_planning_block_format` — validates three-choice format with id/description
2. `test_deep_think_block_format` — validates deep think option format
3. `test_choice_text_extraction` — validates "id: description" extraction
4. `test_special_characters_preserved` — validates quote preservation without HTML escaping
