---
name: orphan-branch-vs-open-pr-detection
description: "When an OPEN PR (often from claude/sonnet) exists on a feature branch with the same name as a local branch, the local branch is likely orphaned — detect before merging to avoid duplicate or divergent work landing on main"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f5ab2b78-cc07-4082-92a7-dccbfe631787
---

## Rule

When scanning local branches for work to merge, **always cross-reference with `gh pr list --state all --json headRefName`** before deciding what to merge. If a local branch and an open PR share a feature name (e.g. `feat/skills-usage-tracking` vs `feat/skills-usage-flag`):

1. The two implementations are likely **divergent** — same goal, different approach
2. The PR (typically from claude/sonnet) is usually the **canonical** one to merge
3. The local branch is **orphaned** and should be flagged for deletion after the PR merges

**Why:** Merging the local branch first causes:
- Merge conflict churn (different file structure, different tests)
- Duplicate features on main (both implementations land)
- Review fatigue (the canonical PR gets superseded silently)

Verified 2026-07-23: local `feat/skills-usage-tracking` (commit 0520f3c by jleechan2015, analyzer-based, +491 LOC) vs PR #15 `feat/skills-usage-flag` (commit 2db62f6 by claude/sonnet, session-log scanner, +507 LOC across 4 files). Trees diverge by 8,000+ lines despite both being "skills-usage". PR #15 was the live branch; local one was orphaned.

**How to apply:**

Pre-merge orphan-detection protocol:
```bash
# 1. Find local branches with commits ahead of origin/main
for branch in $(git branch | tr -d ' *' | grep -v 'main'); do
  count=$(git rev-list --count origin/main..$branch 2>/dev/null)
  [ "$count" -gt 0 ] && echo "$branch: $count ahead"
done

# 2. List all open + closed PRs by head ref
gh pr list --state all --json number,title,headRefName,state

# 3. Cross-reference: for each local branch ahead of main, search PR list
#    by fuzzy name match (e.g. "skills-usage" → PR #15 feat/skills-usage-flag)

# 4. If match found: compare file lists via `git diff <local-sha> <pr-sha> --stat`
#    - If <100 lines diff and same files: local is stale duplicate → drop
#    - If divergent >1000 lines: local is orphan → flag for user, merge PR only
```

**Merge-only-the-PR pattern**: when local is orphan, do NOT push it, do NOT create a competing PR. Squash-merge the live PR with `--delete-branch`. Mention the orphan in the final report so the user can `git branch -D` it explicitly (destructive action stays user-gated).

**Related:**
- `feedback_2026-05-14_llm-inspector-integrate-no-script.md` — manual /integrate sequence
- `project_2026-07-12_codex-e2e-support.md` — same session, different branch with no PR yet (push + create PR pattern instead)

**Reusable pattern for any repo:**

| Local branch state | Open PR state | Action |
|---|---|---|
| Local is fast-forward of merged PR | Either | `git branch -D local` (no-op since same commits) |
| Local diverges from open PR | PR MERGEABLE | Merge PR, flag local as orphan for deletion |
| Local diverges from open PR | PR closed/not-mergeable | Push local as new PR, close stale PR |
| Local only (no PR) | None | Push branch + `gh pr create` |