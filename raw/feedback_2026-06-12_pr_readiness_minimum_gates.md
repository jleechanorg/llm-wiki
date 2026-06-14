---
name: pr-readiness-minimum-gates-before-merge
description: "Before claiming a PR is merge-ready, ALL of: live head SHA matches PR body evidence, CI is green at current head, all review threads resolved, CodeRabbit enabled with reviewDecision APPROVED, real-LLM test re-run at live head and passes. Missing any of these is a known blocker, not a soft concern."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 65fcb9f7-3fca-4299-aafa-89506240a1a1
---

The user's "Minimum before merge" list (PR #7467 review feedback, 2026-06-12) is the canonical PR-readiness gate for this repo. Do not claim a PR is merge-ready until every item is verified.

**Required gates:**
1. **Live head SHA matches PR body evidence.** `git fetch origin && git rev-parse origin/<branch>` must equal the SHA cited in the PR description's "Testing" / "Evidence" / "head" section.
2. **CI is green at current head.** All current-head checks complete and passing, not "still running" or "queued." `gh pr checks <N>` or `gh pr view <N> --json statusCheckRollup` must show all green, with no stale pre-rebase runs lingering.
3. **All review threads resolved.** `gh pr view <N> --json comments` shows every thread has a resolution: "✅ Addressed" or explicit maintainer dismissal with reason. Stale "X open comments" summaries from CodeRabbit are unreliable — check each thread body, not the count.
4. **CodeRabbit enabled with reviewDecision APPROVED.** Not skipped, not paused, not empty. `reviewDecision` in the PR JSON is one of `{"", "APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"}`; only `APPROVED` is mergeable. Skipped/paused = not mergeable.
5. **Real-LLM test re-run at live head passes.** If the test was run at an older local head, re-run at the live head. A passing result on an older SHA is not proof for the current PR.
6. **Skeptic verdict matches live head.** Skeptic gate's "VERDICT: PASS" must be for the live head SHA, not an earlier SHA. A stale PASS for an older head is not a current approval.

**Anti-pattern (PR #7467, 2026-06-12):**
- I described the PR's "test verdict" as the relevant evidence while the PR body still cited a SHA from before several commits had landed.
- I focused on backend code quality (thinning, refactor) before establishing the test passes at the live head.
- I implicitly treated "the Codex blocker is a content issue, not a backend issue" as a soft signal rather than a hard blocker for "organic fully passes."

**Reusable pattern:**
- **Pre-merge checklist (run all 6 before any "ready" claim):**
  ```bash
  git fetch origin
  echo "Live head: $(git rev-parse origin/<branch>)"
  echo "PR body head: $(gh pr view <N> --json body --jq '.body' | rg -o '[0-9a-f]{40}' | head -1)"
  gh pr checks <N> --json name,conclusion --jq '.[] | select(.conclusion != "SUCCESS" and .conclusion != "NEUTRAL" and .conclusion != "SKIPPED")'
  gh pr view <N> --json reviewDecision,comments
  ```
- **If any gate fails**: the PR is not ready. Report the failing gate(s), do not invent compensating evidence.
- **If local and origin diverge**: rebase local onto origin and re-run the test before claiming ready.

**Related:**
- `feedback_2026-06-12_live_pr_head_staleness.md` (the underlying local-vs-origin tracking lesson)
- `feedback_2026-06-12_generic_prompt_fixes.md` (the prompt rework needed for the test)
- `~/.claude/CLAUDE.md` global rules: "NEVER merge without explicit human MERGE APPROVED", "MANDATORY: ALL CI tests must pass before merge"
- `~/.claude/skills/pr-green-definition.md` (7-green verification — never trust `gh pr checks`)
