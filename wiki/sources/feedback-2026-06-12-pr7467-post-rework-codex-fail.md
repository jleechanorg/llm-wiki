---
title: "PR #7467 post-rework: real-LLM PASS but Codex FAIL (auto-selection gap + spell-count clamp)"
type: source
tags: [pr-7467, level-up, codex-verdict, v6-prompt, auto-selection-gap, spell-clamp, bead]
date: 2026-06-12
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-12_pr7467_post_rework_codex_fail.md
---

## Summary
PR #7467 (`fix/level-up-modal-turn-revert`) achieved RUNTIME PASS on the multi-organic L1→L2→L3→L4 progression at head `d1873d2dc7` (post V6 prompt rework), but the Codex leveling review FAILed on 2 pre-existing backend blockers that the prior over-fit V6 prompt was masking: an auto-selection gap in `agents.py`/`rewards_engine.py` (no `pending_level_up_selections` pre-population on modal entry) and a spell-count clamp that drops 2 of 6 Paladin prepared spells. Both blockers are independent of the V6 prompt rework and would FAIL at the prior head `212b0133` too. Option A (ship prompt + file follow-up beads) is the recommended tradeoff against the /goal constraint.

## Key Claims
- The V6 prompt rework at `7610402` correctly expresses the generic subclass-granted always-prepared/known rule, replacing Paladin enumeration. The 2 codex blockers are NOT caused by the rework — the prior over-fit prompt's narrower scope may have coincidentally matched the backend's clamp, masking the bug.
- Blocker 1: `story[51]` exposes `finish_level_up_return_to_game` but does not persist `pending_level_up_selections`; only sets `level_up_in_progress=true` and `level_up_pending=true`. Backend in `agents.py` or `rewards_engine.py` does not pre-populate `pending_level_up_selections` from the LLM's `state_updates.rewards_box.level_up.*` recommended package. This is a UI affordance gap.
- Blocker 2: Level 4 first modal recommends 6 prepared paladin spells (Cure Wounds, Divine Favor, Shield of Faith, Bless, Heroism, Wrathful Smite) but the final committed level 4 state keeps only 4 (Cure Wounds, Divine Favor, Shield of Faith, Bless). Backend in `rewards_engine.canonicalize_rewards()` or `agents.py` post-process drops 2 of 6. This is a persistence/clamp bug.
- The user said: "lets not thin anything that actually fixes an obvious bug from testing_mcp/core level up organic for now and do it alter" — but the rework exposed two new obvious bugs, requiring a decision between options A (ship + beads), B (revert), or C (fix in this PR).
- Option A is the recommended path under the /goal constraint: accept prompt rework as net win, file 2 backend blockers as follow-up beads, pivot PR description to be honest about residual blockers.

## Key Quotes
> "The V6 prompt rework is **correct in itself** (it now expresses the generic subclass-granted always-prepared/known rule, not Paladin enumeration). The two blockers are **pre-existing backend bugs** that the prior over-fit V6 prompt at 7610402 was masking."

> "The minimum-before-merge contract (live head, CI green, threads resolved, CR APPROVED, real-LLM PASS, Skeptic PASS) requires real-LLM PASS, which requires the codex verdict to flip. The codex verdict cannot flip without addressing both blockers."

## Connections
- [[PR7467]] — the parent PR whose codex review FAILed
- [[LevelUpModalRouting]] — the modal auto-selection gap is in the modal-entry handler
- [[CanonicalizeRewards]] — the spell-clamp bug is suspected to live in `rewards_engine.canonicalize_rewards()`
- [[GenericPromptFixes]] — related V6 generalization feedback
- [[PRReadinessMinimumGates]] — the 6-gate minimum contract that option A challenges
