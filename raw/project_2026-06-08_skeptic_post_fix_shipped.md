---
name: skeptic post fix shipped 2026-06-08
description: PR #654 skeptic post bug (cross-user 403) fixed by subagent a6194e0e16bd939e0 — commit fca0cc322; bd-2hmj closed
metadata:
  type: project
---

Subagent `a6194e0e16bd939e0` completed the skeptic post fix on 2026-06-08. The bug: `packages/cli/src/commands/skeptic/posting.ts:56-70` rethrew 403 errors from cross-user comment PATCH, causing the verdict to silently disappear while the CLI reported "Done!".

**Fix shipped (commit fca0cc322):**
- Added `isGhForbiddenError()` alongside `isGhNotFoundError()`
- 403 now falls back to `createComment` (alongside the existing 404 fallback)
- Other errors (422 oversized body, 500, network) still rethrow

**TDD:** Red (1 failing test for 403 fallback) → Green (5/5 posting.test.ts tests pass) → 696/696 full suite (no regressions)

**E2E verified on PR #654:**
- Comment #4644588084: idempotent PATCH on existing comment matching SHA 97b51e6ff
- Comment #4644642181: fresh CREATE for new SHA fca0cc322
- Both have all required markers (`<!-- skeptic-agent-verdict -->`, `<!-- skeptic-head-sha-{sha} -->`, 8 gate markers + 8c/8d, `<!-- skeptic-gate-trigger-{sha} -->`, `<!-- skeptic-cron-trigger-{sha} -->`, `VERDICT: FAIL`)

**PR #654 status:** Skeptic Gate is correctly FAIL because PR has real blockers (`reviewDecision=CHANGES_REQUESTED`, 2 unresolved CR threads, ZFC violation in `skeptic-cron-local.ts:103`, stale evidence at old head 53342b7837). Skeptic is doing its job — author needs to address these in subsequent work.

**Bead:** bd-2hmj closed
**PR:** https://github.com/jleechanorg/agent-orchestrator/pull/654
**Pushed commit:** https://github.com/jleechanorg/agent-orchestrator/commit/fca0cc322a971721493f9af58a41d63edfa07d02
**Documentation:** /tmp/skeptic-post-fix.md

**Related:** [[feedback_2026-06-08_skeptic_post_403_fallback]], [[project_2026-06-07_worldai_skeptic_conflation]], [[project_2026-06-07_tilde_systemic]]
