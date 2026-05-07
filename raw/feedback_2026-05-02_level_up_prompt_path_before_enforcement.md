---
name: Level-up prompt path before enforcement
description: For PR 6748 level-up work, verify selected agent/prompt path and use model target/current transition before any backend enforcement.
type: feedback
bead: rev-sd96f
---

# Level-up prompt path before enforcement

## Context

PR 6748 organic level-up testing showed an escape attempt during level-up was routed to `RewardsAgent`, not `LevelUpAgent`. The failing LLM request did not include `level_up_instruction.md`, so the model never saw the modal no-XP/no-story/explicit-finish contract.

## Rule

Before adding backend protection for level-up bugs, inspect the raw LLM request/response and selected agent. Fix the prompt/schema/routing path first. For PR 6748 specifically, backend enforcement is forbidden unless the human explicitly says `ENFORCEMENT APPROVED`.

## Level-up signal contract

Prefer explicit model fields over loose booleans. `target_level > current_level` is an actionable model-owned level-up signal. Backend may interpret that explicit transition for routing/formatting, but must not compute primary availability from XP thresholds.

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6748
- Bead: rev-sd96f
- Evidence source: `/tmp/worldarchitect.ai/pr-6748/test_level_up_organic/iteration_005/llm_request_responses_1777706772359.jsonl`
