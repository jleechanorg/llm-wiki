---
name: Post-merge branch commits are silently lost on integrate
description: integrate.sh auto-deletes branches with merged PRs; commits made after the PR merges are NOT on main and get dropped
type: feedback
bead: none
originSessionId: 90406e34-3014-4f52-90ff-74da8a1daf37
---
## Rule

Once a PR is merged, **do not commit to its source branch** expecting those changes to reach main. `integrate.sh` detects branches with merged PRs and auto-deletes them. Any commits pushed to that branch after the merge are orphaned.

**Why:** `integrate.sh` checks if the local branch has a merged PR — if yes, it considers the branch "safe to delete" and removes it. The script only checks PR merge status, not whether there are commits ahead of main.

**How to apply:**
- After a PR merges, immediately open a new branch for any follow-up work
- Do NOT add improvements to the merged PR's source branch (e.g., `feat/babysit-skill`) and expect them to land on main
- If you need to land a post-merge improvement, create a new PR from a fresh branch

## Incident

2026-05-10: After PR #6850 (babysit skill) merged, I committed an improvement to Gate 5 (dynamic owner/repo detection in SKILL.md) to `feat/babysit-skill`. `integrate.sh` detected PR #6850 was merged, deleted the branch, and the Gate 5 improvement was lost.

## Reusable Pattern

```bash
# Before committing to a branch, check if its PR is already merged:
gh pr list --head $(git branch --show-current) --state merged --json number --jq '.[].number'
# If output is non-empty → create a NEW branch instead of committing here
```
