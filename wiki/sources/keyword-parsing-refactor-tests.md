---
title: "Keyword Parsing Refactor Tests"
type: source
tags: [python, testing, prompt-engineering, tdd, refactor]
source_file: "raw/test_keyword_parsing_refactor.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test suite verifying the removal of hacky keyword-based prompt switching in get_current_turn_prompt(). Tests confirm that "think" and "plan" keywords in user input no longer trigger different prompt templates, eliminating false positives like "I plan to attack" incorrectly triggering think mode.

## Key Claims
- **No keyword detection in get_current_turn_prompt()**: Function uses consistent prompt template for all character mode inputs
- **False positives eliminated**: Phrases like "I plan to attack" no longer trigger think mode
- **LLM handles intent interpretation**: System instructions tell the LLM how to handle think/plan commands
- **Consistent prompt template**: All character mode inputs generate "Continue the story" prompts
- **God mode unchanged**: God mode prompts remain separate and functional

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| test_action_with_plan_word_not_treated_as_think_command | "I plan to attack the goblin" | Standard story continuation, not think mode |
| test_action_describing_existing_plan_not_think_command | "The merchant explains the plan" | Standard story continuation |
| test_sentence_with_think_word_not_think_command | "I think the guard is lying" | Observation, not deliberation request |
| test_character_mode_consistent_prompt_template | Various inputs | All use "Continue the story" template |
| test_god_mode_unchanged | God mode input | GOD MODE: prompt preserved |

## Connections
- [[IntentClassifier]] — semantic routing that replaces keyword detection
- [[PromptTemplate]] — consistent template pattern for character mode
- [[GodMode]] — separate prompt mode unaffected by this refactor

## Contradictions
- None identified — this refactor aligns with the JSON mode preference tests that also remove legacy parsing
