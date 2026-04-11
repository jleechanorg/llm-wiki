---
title: "Test Constants Module Values and Structure"
type: source
tags: [python, testing, unit-tests, constants]
source_file: "raw/test_constants.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating the mvp_site constants module. Tests verify actor constants, interaction mode constants, dictionary key constants, export format constants with MIME types, prompt filename constants, prompt type constants, and prompt path constants. Ensures all constants are properly defined strings.

## Key Claims
- **Actor Constants**: ACTOR_USER and ACTOR_GEMINI properly defined
- **Interaction Modes**: MODE_CHARACTER and MODE_GOD correctly configured
- **Dictionary Keys**: KEY_ACTOR, KEY_MODE, KEY_TEXT, KEY_TITLE, KEY_FORMAT, KEY_USER_INPUT, KEY_SELECTED_PROMPTS, KEY_MBTI all defined
- **Export Formats**: FORMAT_PDF, FORMAT_DOCX, FORMAT_TXT with correct MIME types
- **Prompt Files**: FILENAME_NARRATIVE, FILENAME_MECHANICS, FILENAME_GAME_STATE, FILENAME_CHARACTER_TEMPLATE, FILENAME_MASTER_DIRECTIVE, FILENAME_DND_SRD properly set
- **Prompt Paths**: PROMPTS_DIR and all path constants constructed with os.path.join

## Key Test Cases
- test_actor_constants — validates ACTOR_USER == "user", ACTOR_GEMINI == "gemini"
- test_interaction_mode_constants — validates MODE_CHARACTER == "character", MODE_GOD == "god"
- test_dictionary_key_constants — validates all KEY_* constants
- test_export_format_constants — validates FORMAT_* constants and MIME types
- test_prompt_filename_constants — validates FILENAME_* constants
- test_prompt_type_constants — validates PROMPT_TYPE_* constants
- test_prompt_path_constants — validates PROMPTS_DIR and path construction
- test_constants_are_strings — ensures no accidental None values

## Connections
- [[mvp_site]] — module containing the constants under test
- [[Python Testing]] — testing framework used (unittest)
- [[Constants Module]] — design pattern for centralized configuration
