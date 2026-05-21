# ZFC Violation Spiral — Misdiagnosis Pattern (PR #6908)

**Source**: Claude memory — `feedback_2026-05-14_zfc_violation_spiral_misdiagnosis.md`
**Date**: 2026-05-14
**Project**: worldarchitect.ai
**PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/6908

## Summary

PR #6908 accumulated 61 commits because server-side choice injection (`_inject_modal_finish_choice_if_needed`) was added to patch symptoms instead of fixing the upstream LevelUpAgent prompt. The root-cause fix was 5 lines. A 3-question ZFC pre-flight at commit 1 would have caught this.

## The Spiral Pattern

1. Symptom: fallback choices appear after level-up finish
2. Fix: add server-side injection `_inject_modal_finish_choice_if_needed`
3. New symptom: injection fires in wrong cases
4. Fix: add more conditions to injection
5. New symptom: conditional injection misses edge cases
6. ... (repeat 50+ times)

## Root Cause

The LevelUpAgent prompt had no post-finish JSON example. The model had no explicit instruction to return story choices on the finish turn — so it guessed and sometimes returned nothing, which triggered the fallback.

## The Fix

- Remove all 4 `_inject_modal_finish_choice_if_needed` calls
- Remove `_ensure_custom_action_planning_block` from canonical stream path
- Remove `pop("planning_block")` that deleted valid Gemini choices
- Add LevelUpAgent post-finish prompt example
- Keep `_ensure_custom_action_planning_block` only as true last-resort

**Test result**: GREEN — LLM returned `strike_with_smite`, `defensive_parry`, `cast_bless`, `intimidating_challenge`

## The 3-Question ZFC Pre-flight

Before adding any `_inject_*`/`_ensure_*`/`_fallback_*` on model output:
1. Does the model have explicit instruction for this output? (Check agent prompt)
2. Can a prompt fix this?
3. If yes → fix prompt first.

## Related Concepts

- [[ZeroCognitionFramework]]
- [[RootCauseFirst]]
- [[ServerGeneratedPlanningBlock]]
- [[SymptomPatchingAntiPattern]]
