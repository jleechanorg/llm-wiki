---
name: cr-evaluates-old-commit-not-head
description: CodeRabbit may evaluate a stale commit, not current HEAD — verify which SHA CR reviewed
type: feedback
bead: rev-3jjro
---

CR bots can evaluate an older commit when multiple commits land close together.
In PR #6913, the fix was in commit `5d3c8c412` but CR evaluated `c5f9a7c6` (older)
and posted CHANGES_REQUESTED based on code that had already been fixed.

**Why it matters:** Seeing CR CHANGES_REQUESTED after applying a fix does NOT mean
the fix is missing. Always verify which SHA CR actually evaluated before debugging
"why isn't CR happy".

**How to apply:**
1. Check CR review body for the SHA it mentions (often in "Verified at commit X").
2. Compare to `gh pr view <N> --json headRefOid`.
3. If CR evaluated old SHA, trigger re-review: `@coderabbitai review` or `@coderabbitai all good?`.

**Green Gate behavior:** Gate-3 logs `CR=APPROVED(status-only)` even when formal
`reviewDecision=CHANGES_REQUESTED` — it reads the ping-coderabbit CI check, not the
review state. So Green Gate CI can PASS while CR review state shows CHANGES_REQUESTED.

**References:**
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6913
- Old SHA CR evaluated: `c5f9a7c6`
- Actual HEAD with fix: `01f46c6b`
