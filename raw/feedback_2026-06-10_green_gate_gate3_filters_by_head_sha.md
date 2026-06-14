---
name: green-gate-gate3-filters-by-head-sha
description: "Green Gate's Gate 3 (CodeRabbit APPROVED) filters by head SHA so stale CHANGES_REQUESTED on old SHAs are NOT blockers for the Green Gate; but GitHub's mergeStateStatus=BLOCKED on the PR still blocks actual merge"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 11b18814-6b01-49a8-a167-12c66b99835e
---

# Green Gate Gate 3 filters by head SHA — but PR-level mergeStateStatus is what blocks human merge

The `.github/workflows/green-gate.yml` Gate 3 (CodeRabbit APPROVED) query:
```bash
gh api .../pulls/${PR_NUM}/reviews | jq -rs --arg head "$HEAD_SHA" 'add | [.[] | select((.user.login == "coderabbitai[bot]" or .user.login == "coderabbitai") and .state != "COMMENTED" and .commit_id == $head)] | sort_by(.submitted_at) | if length > 0 then (last | .state // "none") else "none" end'
```

The `.commit_id == $head` filter excludes reviews on **older** SHAs. So a CHANGES_REQUESTED review on `4ed5063a` does NOT block Green Gate's "CodeRabbit APPROVED" check on a new head `32e3e5c`.

The fallback path is also lenient: if no formal review exists on the head SHA, the gate looks at:
- `CR_STATUS` (commit status check)
- `CR_APPROVE_COMMENT` (PR comment matching `[approve]` regex)

If both are `none` or `success`, the gate reports `APPROVED(status-only)` or `APPROVED(status+comment)`.

**BUT** GitHub's PR-level `mergeStateStatus` does NOT apply this filter. It uses the worst state across all reviews:
- `reviewDecision: CHANGES_REQUESTED` (stale on old SHA) → `mergeStateStatus: BLOCKED`
- The PR cannot be merged via the GitHub UI even though the Green Gate workflow says it's green.

So the workflow is internally consistent (Green Gate gates 1-8 can all be green), but the human's merge attempt via the GitHub UI is blocked by GitHub's own check.

**Resolution paths:**
1. **Push a new commit** to the PR branch → triggers `ping-coderabbit` workflow → CodeRabbit reviews the new SHA → posts APPROVED/CHANGES_REQUESTED on new SHA → `reviewDecision` updates → `mergeStateStatus` clears to `CLEAN` or `UNSTABLE`.
2. **Manually dismiss the stale review** in the GitHub UI (human action, not agent).
3. **Wait for CodeRabbit to re-review on its own** (push-triggered, but only on push events — not on @-mention PR comments).

**Why**: Dice-audit PR #7353 had `reviewDecision: CHANGES_REQUESTED` from an old CodeRabbit review on `4ed5063a8267` (06-08), but the head was `32e3e5c6dc` (06-10). Green Gate passed (gates 1-8), but `mergeStateStatus: BLOCKED` until a fresh review on the new SHA landed. Push of a doc-only commit `530f364ee1` triggered the new CR review.

**How to apply:**
- When a PR is "all gates green" per the Green Gate workflow but `mergeStateStatus` is `BLOCKED` or `UNSTABLE`, check `reviewDecision`:
  - If `CHANGES_REQUESTED` from CodeRabbit: check the `commit_id` of that review. If it's on an old SHA, push a new commit (or a no-op) to trigger a fresh CR review.
  - If `CHANGES_REQUESTED` from a human: human must dismiss.
  - If `REVIEW_REQUIRED` (no CR review yet): push a commit to trigger ping-coderabbit.
- The CodeRabbit PR comment `@coderabbitai review` does NOT trigger a workflow — the only push-based trigger is `coderabbit-ping-on-push.yml` on `push` events.
- The 8-gate Green Gate verdict ≠ GitHub UI mergeability. Always check both.
