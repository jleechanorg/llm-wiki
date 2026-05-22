# Inline prompt drift in `mvp_site/agents.py` — edit `prompts/*_instruction.md` instead

- **Date:** 2026-05-22
- **Type:** feedback / anti-pattern
- **Origin:** review of PR [#6968](https://github.com/jleechanorg/worldarchitect.ai/pull/6968) — eliminate extra continue-story step after level-up finish
- **Raw source:** [[raw/feedback_2026-05-22_inline_prompt_drift_agents_py]]
- **Memory file:** `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-05-22_inline_prompt_drift_agents_py.md`
- **Beads:** [rev-ivchh](https://github.com/jleechanorg/worldarchitect.ai/issues/6979) (move clause), [rev-7v63f](https://github.com/jleechanorg/worldarchitect.ai/issues/6980) (broader audit)

## Rule

When you need to add or modify prompt content for an agent that already has a markdown instruction file under `mvp_site/prompts/` (loaded via `_load_instruction_file()` / `PromptBuilder`), edit the markdown file. **Do not** append a new string literal inside `build_system_instructions()` in `mvp_site/agents.py`.

## Evidence

PR #6968 added a 9-line **FINISH INTENT RECOGNITION** clause inline in `LevelUpAgent.build_system_instructions()` (`mvp_site/agents.py:1402-1410`) when `mvp_site/prompts/level_up_instruction.md` is already loaded for that same agent through the existing prompt-loader pipeline.

State of `mvp_site/agents.py` at merge time:

- 3,853 lines
- 10 `build_system_instructions` methods
- ~157 long string literals (>60 chars), much of it prompt content

## Why this matters

- Splits the prompt surface across two files: markdown + Python
- Forces prompt iteration through Python edits instead of plain markdown
- Bypasses the loader / `PromptBuilder` pipeline already established for other agents
- Increases agents.py line count, which is the same anti-pattern that put `world_logic.py` against the 10,000-line budget ([rev-gan4o](https://github.com/jleechanorg/worldarchitect.ai/issues/6982))

## Applies to

Related concepts: [[ZeroFrameworkCognition]] (model-owned contracts), [[AgentArchitecture]].

## How to apply

Before adding any string literal longer than ~60 characters inside an agent's `build_system_instructions()`, check whether `mvp_site/prompts/<agent>_instruction.md` already exists.

- If yes → add the new clause as a clearly-titled section in the markdown.
- If no → prefer creating the markdown file and wiring the loader over inlining.
