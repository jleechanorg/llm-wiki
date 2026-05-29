---
name: pr-body-mechanism-not-constant
description: PR body should describe runtime mechanism (field checks, routing) not internal constant removal — CR P2 violation on PR #7142
type: feedback
bead: none
---

## Rule

**PR body must describe the observable runtime mechanism, not the implementation artifact removed.**

When a constant is deleted to implement a behavior change, the PR body summary should lead with what the system *does* differently at runtime — not "removed `_PREPARED_CASTER_CLASSES`".

## Why

CR flagged PR #7142 as a P2 because the original PR body opened with:
> "The `_PREPARED_CASTER_CLASSES` backend constant was removed entirely."

That tells a reader nothing about the actual behavior. The real mechanism was:
1. **3-field OR spell detection**: `spells_known[] OR spells[] OR spells_prepared[]` — cantrips-only no longer satisfies spell presence
2. **LLM-driven field selection**: which fields the LLM populates is governed by prompts, not a backend class list

## How to Apply

When writing a PR body for any refactor/deletion:
- Lead with the **runtime invariant** that now holds (e.g. "spell presence requires at least one of spells_known / spells / spells_prepared to be non-empty")
- Follow with the **mechanism** (e.g. "3-field OR check")
- Then explain the **ownership model** (e.g. "field selection is LLM-owned, governed by prompts in level_up_instruction.md")
- Only mention removed constants/code as implementation detail in a later section

## Example (PR #7142)

Bad: "Removed `_PREPARED_CASTER_CLASSES` backend constant; class-specific routing now handled by `_SPELLCASTING_CLASSES` + `_match_spellcasting_class`"

Good: "Spell presence detection now uses a ruleset-agnostic 3-field OR check: `spells_known[] is empty AND spells[] is empty AND spells_prepared[] is empty`; cantrips-only no longer satisfies the check. Field selection is LLM-owned via prompts."

## References

- PR [#7142](https://github.com/jleechanorg/worldarchitect.ai/pull/7142)
- CR comment: https://github.com/jleechanorg/worldarchitect.ai/pull/7142#issuecomment-4571810409
- PR body updated 2026-05-29
