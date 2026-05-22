---
name: inline-prompt-drift-agents-py
description: "When adding prompt content for an existing agent, edit prompts/*_instruction.md — do not inline new strings into mvp_site/agents.py"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b31c9b56-8b29-494f-8d28-98ce99d0a17e
---

When you need to add or modify prompt content for an agent that already has a markdown instruction file under `mvp_site/prompts/` (loaded via `_load_instruction_file()` / `PromptBuilder`), edit the markdown file — do **not** append a new string literal inside `build_system_instructions()` in `mvp_site/agents.py`.

**Why:** `mvp_site/agents.py` is at 3,853 lines with 10 `build_system_instructions` methods and ~157 long string literals — much of it prompt content that should live in `prompts/*.md`. PR [#6968](https://github.com/jleechanorg/worldarchitect.ai/pull/6968) added a 9-line FINISH INTENT RECOGNITION clause inline in `LevelUpAgent.build_system_instructions()` when `mvp_site/prompts/level_up_instruction.md` is already loaded for that same agent. Inline strings split the prompt surface, make iteration require Python edits, and bypass the existing loader pipeline. Tracked: [rev-ivchh](https://github.com/jleechanorg/worldarchitect.ai/issues/6979) and broader audit [rev-7v63f](https://github.com/jleechanorg/worldarchitect.ai/issues/6980).

**How to apply:** Before adding any string literal longer than ~60 characters inside an agent's `build_system_instructions()`, check whether `mvp_site/prompts/<agent>_instruction.md` already exists. If yes, add the new clause as a clearly-titled section in the markdown. If no, prefer creating the markdown file and wiring the loader over inlining. Related: [[pr6968-merged-followups]].
