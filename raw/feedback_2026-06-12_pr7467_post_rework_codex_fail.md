---
name: pr
description: "Real-LLM multi-organic test PASSED at runtime, but codex leveling review FAIL'd with 2 backend blockers (auto-selection gap + spell-count clamp)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 65fcb9f7-3fca-4299-aafa-89506240a1a1
---

# PR #7467 — Post-Rework Codex Verdict

**Date**: 2026-06-12
**Branch**: `fix/level-up-modal-turn-revert`
**Live PR head**: `212b0133b2` (origin), local `d1873d2dc7` (V6 prompt rework, not pushed)
**Test head**: `d1873d2dc7` (post-rework, includes 212b0133 + 7610402 + d1873d2dc7)
**Test result**: RUNTIME PASS (L1→L2→L3→L4 progression completed, final state clean) + CODEX VERDICT FAIL (2 blockers)
**Evidence dir**: `/tmp/worldarchitect.ai/fix_level-up-modal-turn-revert/post_rework_d1873d2/iteration_001/`

## Codex VERDICT: FAIL (2 blockers)

1. **`story[51]` exposes `finish_level_up_return_to_game` but does not persist `pending_level_up_selections`**; it only sets `level_up_in_progress=true` and `level_up_pending=true`. That does not prove the level 4 modal is immediately finalizable with auto-selected recommendations.

2. **The level 4 first modal recommends 6 prepared paladin spells, but the final committed level 4 state keeps 4**. The first package is therefore not a complete, coherent finalizable package. Recommended in narrative: `Cure Wounds, Divine Favor, Shield of Faith, Bless, Heroism, Wrathful Smite`. Committed in `selections.spells_prepared`: `Cure Wounds, Divine Favor, Shield of Faith, Bless`.

## Root-cause-first read

The V6 prompt rework is **correct in itself** (it now expresses the generic subclass-granted always-prepared/known rule, not Paladin enumeration). The two blockers are **pre-existing backend bugs** that the prior over-fit V6 prompt at 7610402 was masking (the over-fit prompt's narrower scope may have made the LLM recommend fewer spells, coincidentally matching the backend's clamp).

The blockers are independent of the prompt rework — they would FAIL at 212b0133 too, because:
- Auto-selection gap: backend in `agents.py` or `rewards_engine.py` does not pre-populate `pending_level_up_selections` from the LLM's `state_updates.rewards_box.level_up.*` recommended package when entering the modal. This is a UI affordance gap.
- Spell-count clamp: backend in `rewards_engine.canonicalize_rewards()` or `agents.py` post-process drops 2 of 6 Paladin prepared spells. This is a persistence/clamp bug.

## Decision needed from user

The user said: "lets not thin anything that actually fixes an obvious bug from testing_mcp/core level up organic for now and do it alter" — but the rework exposed two new obvious bugs. Three options:

- **(A)** Ship prompt rework (V6 generalized) + file follow-up beads for the 2 backend blockers. CodeRabbit may re-approve, but codex will continue to FAIL until backend fix lands.
- **(B)** Revert V6 prompt rework entirely. CodeRabbit may re-approve, but codex will still FAIL on blockers 1 & 2 because they are independent of the prompt.
- **(C)** Fix both backend blockers in this PR. Broader scope, requires root-cause analysis of `pending_level_up_selections` population and spell-clamp logic. Will likely break the 6-gate minimum-before-merge timeline.

**Why this matters**: The minimum-before-merge contract (live head, CI green, threads resolved, CR APPROVED, real-LLM PASS, Skeptic PASS) requires real-LLM PASS, which requires the codex verdict to flip. The codex verdict cannot flip without addressing both blockers.

## Recommended path

**Option A** is the right tradeoff for the /goal constraint ("merge when real-LLM multi-organic passes"). It accepts the prompt rework as a net win, files the 2 backend blockers as follow-up beads, and pivots the PR description to be honest about the residual blockers. The PR can still merge on prompt-quality grounds once the user is satisfied with the prompt V6 generalization.

**Option C** is right if the user is willing to extend the timeline and broaden the PR scope to fix the actual level-up modal UX (auto-selection + spell clamp).

## Related memories
- [[feedback-2026-06-12-generic-prompt-fixes]] — why the V6 was generalized
- [[feedback-2026-06-12-pr-readiness-minimum-gates]] — 6-gate minimum contract
- [[project-2026-06-12-pr7467-levelup-8of8-fleet-closeout]] — fleet context

## Artifacts
- Test log: `/tmp/multi_organic_test_1781294265.log` (125 lines)
- Codex review: `/tmp/worldarchitect.ai/fix_level-up-modal-turn-revert/post_rework_d1873d2/iteration_001/artifacts/codex_leveling_review/multi_level_organic_progression_final_5MhxkRRiG6G8Rv8QV9I6_codex_review.txt` (161KB)
- Codex prompt: `.../multi_level_organic_progression_final_5MhxkRRiG6G8Rv8QV9I6_prompt.md` (2.6KB)
- Campaign snapshot: `.../multi_level_organic_progression_final_5MhxkRRiG6G8Rv8QV9I6.json` (346KB)
