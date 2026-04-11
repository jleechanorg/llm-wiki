---
title: "DialogAgent prompt loading verification test"
type: source
tags: [python, testing, dialog-agent, prompt-engineering, integration]
source_file: "raw/test_dialog_agent_prompt_loading.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit test that verifies DialogAgent correctly loads its prompt files during initialization. The test mocks the `read_file_cached` function and validates that building prompts for DialogAgent includes content from `dialog_system_instruction.md`.

## Key Claims
- **Prompt Loading**: DialogAgent's PromptBuilder includes content from `dialog_system_instruction.md`
- **File Path Resolution**: The prompt loading uses `read_file_cached` with appropriate file paths
- **Content Verification**: Test verifies specific content from dialog instruction file is present in final prompt

## Test Logic
The test uses MagicMock to create a mock GameState and patches `read_file_cached` to return specific content for each expected file:
- `dialog_system_instruction.md` → "CONTENT_FROM_DIALOG_INSTRUCTION"
- `master_directive.md` → "CONTENT_FROM_MASTER_DIRECTIVE"
- `game_state_instruction.md` → "CONTENT_FROM_GAME_STATE"
- `planning_protocol.md` → "CONTENT_FROM_PLANNING"
- `character_template.md` → "CONTENT_FROM_CHARACTER_TEMPLATE"
- `relationship_instruction.md` → "CONTENT_FROM_RELATIONSHIP"

The test then builds prompts using `PromptBuilder.build_for_agent(self.agent)` and verifies `CONTENT_FROM_DIALOG_INSTRUCTION` is present in the combined prompt output.

## Connections
- [[DialogAgent]] — the agent being tested
- [[PromptBuilder]] — the component responsible for loading and assembling prompts
