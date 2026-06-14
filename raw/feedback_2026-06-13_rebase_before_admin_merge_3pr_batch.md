---
name: rebase-before-admin-merge-batch-of-3
description: "When substantive 7-green is met (CR APPROVED, no CI failures) but PRs are BEHIND main, rebase onto origin/main then admin-merge — works for a batch of 3 PRs even when 2 of them touch the same module (skeptic) and the base PR #683 is also a skeptic change."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8e1493a5-115a-4b66-9790-42973f21fc27
---

**Why:** 2026-06-13 batch — PRs #683 (skeptic 3-layer cooldown, base), #681 (watchdog alert routing), #679 (skeptic CR review filter). All three merged in 8 minutes. #681 rebase: 8/8 clean. #679 rebase: 20/20 clean — no conflicts with #683's skeptic code changes despite #679 also touching `packages/core/src/skeptic-cron-local.ts` and `packages/core/src/mergeGate.ts`. Order on main: #683 (99232739a) → #681 (d8940175b) → #679 (afa4ecb18).

**How to apply:**
1. For each PR, `git worktree add` at the PR's head SHA (detached HEAD is fine — `--force-with-lease origin HEAD:<branch>` will recreate the branch ref)
2. `git rebase origin/main` — if it succeeds without conflicts, push with `--force-with-lease` and admin-merge
3. Admin-merge is non-interactive when the PR is MERGEABLE + CR APPROVED; `gh pr merge` returns empty stdout but `state` flips to MERGED on next view
4. Verify with `git fetch origin main && git log --oneline -3 origin/main` — not the local index, which can be stale
5. Re-verify with `gh pr view N --json state,closed,mergedAt,mergeCommit` using **mergedAt** (not `merged` — field doesn't exist)

**Verify field name gotcha**: `gh pr view --json` supports `closed`, `mergedAt`, `mergeCommit.oid` — does NOT support `merged` (boolean) directly. Use `state == "MERGED"` instead.

**Why this is faster than /claw or /f for BEHIND-but-green PRs**: AO workers die in SCM death-spiral at high failure counts (PR-683-batch saw 73 and 204). Direct rebase + admin-merge is ~5 min per PR, no LLM calls, and the substantive 7-green is already met (CR + evidence + tests).

**Adjacent learning**: When 2 PRs touch the same module as the just-merged base, rebase is still expected to be clean if the PRs are non-overlapping at the hunk level. Run the rebase; don't pre-emptively merge the base first. `git rebase` reports each commit as it applies, so "Rebasing (1/8) ... (8/8)" output confirms zero conflicts.
