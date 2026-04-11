---
title: "System Prompt Test Scenarios"
type: source
tags: [worldarchitect, system-prompt, testing, claude-code, command-generation]
sources: []
source_file: docs/system_prompt_test_scenarios.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Test scenarios for validating WorldArchitect.AI's system prompt quality when generating Claude Code commands. Five scenarios cover PR review, implementation, complex workflow, bug fix, and code generation tasks. The validation criteria ensure prompts start with action verbs, are concise, include technical details, prefer automation, assume Claude competence, and follow CLAUDE.md protocols implicitly.

## Key Claims

- **5 Test Scenarios**: PR review, implementation, complex workflow, bug fix, code generation — each with goal, summary, last 5k tokens context, and expected user prompt
- **Good Prompt Pattern**: Action-first, concise (10-50 words), specific technical details, automation preference, assumes Claude competence
- **Poor Prompt Pattern**: Greetings, questions, explanations without action, hand-holding language
- **Quality Indicators**: `/execute implement`, `/copilot 1641`, `fix database timeout` — vs "could you please help me with..."
- **Slash Commands Validated**: `/execute`, `/copilot`, `/orch`, `/cerebras` — all generate action-first prompts

## Validation Criteria

1. **Start with action** (command or direct instruction)
2. **Are concise** (typically 10-50 words)
3. **Include specific technical details** when needed
4. **Prefer automation/orchestration** over manual steps
5. **Assume Claude competence** (no hand-holding)
6. **Follow CLAUDE.md protocols** implicitly

## Good Prompt Examples

- `/execute implement user authentication with Firebase`
- `/copilot 1641`
- `fix database connection timeout in mvp_site/core/db.py`
- `/orch setup automated testing pipeline with coverage reports`

## Poor Prompt Examples

- "Hi Claude, could you please help me with implementing authentication?"
- "I'm having trouble with the database, what do you think I should do?"
- "Can you walk me through the steps to fix this issue?"
- "Please explain how authentication works and then implement it"

## Connections

- [[SlashCommands]] — slash commands tested: /execute, /copilot, /orch, /cerebras
- [[CLaudeCodeSystemPrompt]] — this document validates the system prompt output quality
