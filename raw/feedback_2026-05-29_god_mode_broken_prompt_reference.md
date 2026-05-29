---
name: god-mode-broken-prompt-reference
description: god_mode_instruction.md referenced living_world_instruction.md which is not in god mode's REQUIRED_PROMPT_ORDER — the model never sees it during god mode turns
type: feedback
bead: rev-r3x1g
---

## Learning: Never Reference a Prompt File That Isn't in the Agent's Prompt Order

**Classification**: Mandatory

**Rule**: Before writing "apply `<file>.md` rules verbatim" inside any system instruction, verify that `<file>` appears in the same agent's `REQUIRED_PROMPT_ORDER` or `OPTIONAL_PROMPTS`. If it doesn't, the model has no access to that file and the reference is a broken pointer.

**Why**: god_mode_instruction.md (PR [#7110](https://github.com/jleechanorg/worldarchitect.ai/pull/7110)) included the line:

> "Apply `living_world_instruction.md` lifecycle rules verbatim before generating anything."

But `GodModeAgent.REQUIRED_PROMPT_ORDER` in `mvp_site/agents.py` is:

```
master → god_mode → game_state → planning_protocol → dnd_srd → mechanics
```

`living_world_instruction.md` is absent. The model receives god_mode_instruction.md but not living_world_instruction.md, so the cross-reference was unresolvable.

**How to apply**:
- Before writing any cross-file reference in a system instruction (e.g., "see X.md" or "apply X.md rules"), grep for the referenced filename in the agent class's `REQUIRED_PROMPT_ORDER` and `OPTIONAL_PROMPTS`.
- If the file is absent, inline the rules directly instead of cross-referencing.
- The fix: replaced the broken pointer with self-contained cascade rules in god_mode_instruction.md (commit `30da85811` on PR [#7110](https://github.com/jleechanorg/worldarchitect.ai/pull/7110)).

**Verification**:
- `grep -n "REQUIRED_PROMPT_ORDER" mvp_site/agents.py` reveals each agent's full prompt order.
- `mvp_site/agent_prompts.py:build_god_mode_instructions()` confirms god mode loads: master, god_mode, game_state, planning_protocol, dnd_srd, mechanics.

**References**:
- PR [#7110](https://github.com/jleechanorg/worldarchitect.ai/pull/7110)
- Fix commit: `30da85811`
- File fixed: `mvp_site/prompts/god_mode_instruction.md`
- Agent class: `mvp_site/agents.py` `GodModeAgent`
- Bead: rev-r3x1g (closed)
