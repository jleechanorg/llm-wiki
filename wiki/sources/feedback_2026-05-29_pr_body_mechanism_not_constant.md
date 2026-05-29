# PR Body: Describe Runtime Mechanism Not Constant Removal

**Date**: 2026-05-29
**Type**: feedback
**Source**: `~/.claude/projects/-Users-jleechan-projects-worktree-autolvl-coder/memory/feedback_2026-05-29_pr_body_mechanism_not_constant.md`

## Rule

PR body must lead with the observable runtime mechanism, not the implementation artifact removed.

When a constant is deleted to implement a behavior change, describe what the system *does* at runtime:
- **3-field OR spell detection**: `spells_known[] OR spells[] OR spells_prepared[]`
- **LLM-owned field selection**: governed by prompts, not backend class list

## Context

CodeRabbit flagged PR [#7142](https://github.com/jleechanorg/worldarchitect.ai/pull/7142) as P2 because the original PR body opened with "The `_PREPARED_CASTER_CLASSES` backend constant was removed entirely" — an implementation detail, not the mechanism.

The real mechanism: 3-field OR spell presence check + LLM-driven field selection via prompts.

## Pattern

**Bad**: "Removed `_PREPARED_CASTER_CLASSES`; class routing now handled by X"
**Good**: "Spell presence detection uses a 3-field OR check: spells_known[] / spells[] / spells_prepared[]; field selection is LLM-owned via prompts"

## References

- PR [#7142](https://github.com/jleechanorg/worldarchitect.ai/pull/7142)
- CR comment: https://github.com/jleechanorg/worldarchitect.ai/pull/7142#issuecomment-4571810409
