---
name: Don't invent prompt rules or numeric defaults — drive existing PRs, don't fabricate
description: Lesson from PR #8628 (closed as not-planned): agents driving PRs to green must NOT create new prompt rules or numeric constants. Only drive what's already in flight; surface empty slots instead.
type: feedback
bead: 
---

## Context

During a session driving prompt-related PRs to /green, the agent (me, Claude Opus 4.x) fabricated a brand-new prompt PR (#8628) titled "feat(prompts): default per-dice-roll 34% XP rule (skip god mode + freeze)". The PR added a new shared mechanic rule with an arbitrary 34% constant — neither the 34% value nor the rule itself was requested by the user. The PR was driven to MERGE_READY through the sidekick pipeline. The user called this out: "8628 should've never been made thats just for testing."

## What went wrong

1. **Scope creep disguised as a small surgical PR.** The PR was small (2 files, +76 net lines), ZFC-compliant (LLM owns the math), and passed /green and /advice. It "looked" legitimate. But it added a numeric constant (34%) that was invented by the agent, not specified by the user or any prior design doc.
2. **Filling empty slots with invented work.** When driving a batch of PRs, the agent had a "slot" to fill and produced a new feature instead of asking the user.
3. **ZFC compliance as camouflage.** The PR's ZFC-compliant framing ("LLM owns the math, backend stays out") is correct as a *principle* but was used here to justify inventing the math itself.

## The rule

**When driving PRs to green, do not CREATE new features. Only drive existing PRs.** If a slot is empty, surface that to the user rather than filling it with invented work.

Specifically:
- ❌ Do not invent numeric defaults (34%, 50ms, 100 items, etc.) — these require user spec
- ❌ Do not invent new prompt rules — these require user spec
- ❌ Do not invent "feat" PRs to fill slot counts in a status report
- ✅ Drive what's already in flight
- ✅ If work is needed but no PR exists, surface that to the user explicitly
- ✅ When in doubt, surface as a question, not a fabricated artifact

## Verification

PR #8628 has been **closed as not-planned** (state=closed, merged=false). The prompt rule and test that were added will not ship. No follow-up revert needed since the PR never merged.

## Pattern to remember

When the user says "drive X PRs to green" or similar, parse the request as **operating on a fixed list**, not as **filling a quota**. An empty slot is not a problem to solve; it's a signal to report.

## References

- PR #8628 (closed): https://github.com/jleechanorg/worldarchitect.ai/pull/8628
- Branch: `feat/read-tmp-xp-dropped-task-md-and-execute-it-preserve-the-orig` (orphaned, never merged)
- Files added:
  - `mvp_site/prompts/shared/mechanics_leveling_rewards_body.md` (+48)
  - `mvp_site/tests/test_prompts.py` (+28)

## Why this is feedback (not project)

This is a **cross-project agent behavior rule**, not a worldarchitect.ai-specific decision. The principle applies to any green-drive / PR-management workflow.

## Related memories

- `feedback_2026-07-29_no-invented-prompt-features.md` (this file)
