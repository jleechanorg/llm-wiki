# god_mode prompt cross-references absent file (2026-05-29)

**Source**: `~/.claude/projects/-Users-jleechan-projects-worktree-skillsz/memory/feedback_2026-05-29_god_mode_broken_prompt_reference.md`
**Type**: feedback / Mandatory
**Bead**: rev-r3x1g (closed)

## Summary

`god_mode_instruction.md` contained "Apply `living_world_instruction.md` lifecycle rules verbatim" but `living_world_instruction.md` is absent from `GodModeAgent.REQUIRED_PROMPT_ORDER`. The model never receives that file during god mode turns, making the cross-reference a broken pointer.

## Agent Prompt Order (GodModeAgent)

```
master → god_mode → game_state → planning_protocol → dnd_srd → mechanics
```

`living_world_instruction.md` is only included for regular narrative turns (via `build_living_world_instruction()`), not god mode.

## Rule

Before writing any cross-file reference ("apply X.md verbatim", "see X.md") inside a system instruction, verify `X` appears in the agent's `REQUIRED_PROMPT_ORDER` or `OPTIONAL_PROMPTS`. If absent, inline the rules directly.

## Fix

Commit `30da85811` on PR [#7110](https://github.com/jleechanorg/worldarchitect.ai/pull/7110) replaced the broken reference with self-contained cascade rules in `god_mode_instruction.md`.

## Concepts

- [[prompt-file-cross-reference]]
- [[agent-prompt-order]]
