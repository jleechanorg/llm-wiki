---
title: "2026-06-13 Rebase Before Admin Merge 3Pr Batch"
type: source
tags: ["feedback", "agent-orchestrator", "pr-683"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_rebase_before_admin_merge_3pr_batch.md
---

## Summary
When substantive 7-green is met (CR APPROVED, no CI failures) but PRs are BEHIND main, rebase onto origin/main then admin-merge — works for a batch of 3 PRs even when 2 of them touch the same module (skeptic) and the base PR #683 is also a skeptic change.

## Key Claims
- 1. For each PR, `git worktree add` at the PR's head SHA (detached HEAD is fine — `--force-with-lease origin HEAD:<branch>` will recreate the branch ref)
- 2. `git rebase origin/main` — if it succeeds without conflicts, push with `--force-with-lease` and admin-merge
- 3. Admin-merge is non-interactive when the PR is MERGEABLE + CR APPROVED; `gh pr merge` returns empty stdout but `state` flips to MERGED on next view
- 4. Verify with `git fetch origin main && git log --oneline -3 origin/main` — not the local index, which can be stale
- 5. Re-verify with `gh pr view N --json state,closed,mergedAt,mergeCommit` using **mergedAt** (not `merged` — field doesn't exist)

## Connections
- [[AgentOrchestrator]] — AO worker dispatch memory
- [[KarpathyWikiPattern]] — wiki-ingest protocol
- Source: `raw/feedback_2026-06-13_rebase_before_admin_merge_3pr_batch.md`
