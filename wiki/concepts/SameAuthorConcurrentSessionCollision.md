---
title: "Same-Author Concurrent-Session Collision"
type: concept
tags: [pr-workflow, merge-conflicts, agent-orchestration, tooling-gaps]
date: 2026-07-10
---

# Same-Author Concurrent-Session Collision

Two PRs from the **same GitHub account** (e.g. concurrent Claude Code / AO worker sessions
operating as one identity) independently edit the same file region to fix the same underlying
pain point, then collide when the first merges to main — flipping the second from CLEAN to
CONFLICTING with zero action on its own branch.

## Why standard tooling cannot see it
- **CODEOWNERS review gates**: evaluate each PR in isolation; cannot surface that a sibling open PR already edited the same lines.
- **Conflict-detector bots** (e.g. github-community-projects/pr-conflict-detector): hard-coded same-author exclusions — built for multi-contributor conflicts, structurally silent here.
- **GitHub merge queues**: only re-validate at merge-attempt time, and only gate on required status checks (which may be empty); an approved-but-unmerged PR sitting idle is never re-validated.
- **Write-time conflict predictors** (merge_train): fire when the local session writes a file, not when a sibling PR merges to main later.

## Durable mitigation (behavioral, not tooling)
1. Treat every mergeability claim as an expiring snapshot: re-fetch `mergeable`/`mergeStateStatus` before every claim, repeat, or merge action; report with SHA + UTC timestamp.
2. Resolve resulting conflicts autonomously — mechanical same-fix collisions take the already-merged side and reapply own changes.
3. Before starting CI-infra work, check for sibling open PRs touching the same paths from the same account; treat a hit as a coordination event (single-writer rule), not two independent fixes.

## Variant: merge-out-from-under-you (not just conflict)

2026-09-06: while one session was still driving PR #9743 through `/ready` (gates in
progress, no `gh pr merge` call made), a *different* concurrent session on the same
account (git-attributed "Claude Fable 5.1") independently squash-merged that exact
PR. Detected only because `gh pr view --json state,mergedAt` was re-checked and
suddenly returned `MERGED`; `git merge-base --is-ancestor <own pushed commit>
origin/main` then correctly returned false for a commit pushed *after* the merge
point, since the branch had already been squashed and closed. **Mitigation**: any
commit pushed after such a race needs a fresh cherry-pick PR onto current
`origin/main` — the original PR is closed and cannot receive further review; do not
try to reopen or force-push to it.

## Provenance
2026-07-10 incident: PR #8268 vs PR #8310 (jleechanorg/worldarchitect.ai, `.github/workflows/test.yml` checkout fetch-depth block). A 9-agent swarm adversarially refuted all 5 tooling-based fixes with live repo evidence (172 open same-file PR pairs = alert noise; zero required status checks = nothing for a merge queue to gate on).

2026-09-06 incident: PR #9743 merged mid-`/ready` by a sibling session; follow-up commit landed as a fresh cherry-pick PR #9768. See [[AdviceRunner]].

## Variant: shared-worktree filesystem collision (not just PR/merge)

2026-09-07: the same underlying hazard shows up one layer down, at the working-directory
level. `/integrate` in `worktree_beads_fix_again` hard-stopped on uncommitted changes
that belonged to a *different, live* concurrent session sharing that exact worktree
path — not a merge race, a filesystem race. `git status` cannot distinguish "my own
drift" from "another session's live edits"; `lsof +D <worktree-path>` (live process
holders) plus a repeated `git diff` a few seconds apart (changing output = active
editing) is the detection technique. See [[IntegrateHardStopPattern]].

## Connections
- [[7-Green-Proof-Artifact]]
- [[swarm-orchestration-pattern]]
- [[IntegrateHardStopPattern]] — filesystem-level variant of this collision class
- Source: [[feedback-2026-07-10-mergeability-drift-and-coderabbit-ratelimit]]
- Source: [[feedback-2026-09-06-advice-runner-lfs-smudge-and-concurrent-merge-race]]
- Source: [feedback-2026-09-07-integrate-shared-worktree-concurrent-session-collision](../sources/feedback-2026-09-07-integrate-shared-worktree-concurrent-session-collision.md)
