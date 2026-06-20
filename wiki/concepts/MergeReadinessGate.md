---
title: "Merge Readiness Gate (5-gate checklist)"
type: concept
tags: [merge, pr, verification, protocol, gates]
last_updated: 2026-06-19
---

# Merge Readiness Gate

A 5-gate checklist to evaluate BEFORE answering any user question of the form "do we need to merge `<branch>` to origin/main?" or "drive this PR to merge." Every gate must pass; any fail → answer is NO with the specific blocker cited.

## The 5 gates

| # | Check | Pass signal |
|---|---|---|
| 1 | `git status --short` | EMPTY (no uncommitted M/?? files) |
| 2 | `git log --oneline origin/main..HEAD` | commits exist with focused scope matching branch name |
| 3 | `gh pr list --head <branch> --state all` | exactly ONE PR open (or already merged) |
| 4 | `gh pr view <N> --json reviewDecision,mergeable` | `reviewDecision=APPROVED` AND `mergeable=true` AND Skeptic PASS for head SHA |
| 5 | Conversation grep for literal `MERGE APPROVED` | present in current thread |

**Also required**: `scripts/staging-canary.sh` must have passed — per CLAUDE.md "Worktree Isolation", direct merges bypass the staging canary gate. Without canary pass, merge is unsafe even if all 5 gates above pass.

## Why each gate matters

- **Gate 1 (clean tree)**: Uncommitted M/?? files get silently dropped on merge → silent data loss. The 2026-06-19 session caught `fix/mcp-daemon-keepalive` with 11 M (including live `workspace/SOUL.md`) + 7 ?? untracked files.
- **Gate 2 (focused scope)**: Scope creep between branch name and commits makes review harder and revert risk higher. `fix/mcp-daemon-keepalive` had commits touching 5e detector docs + untracked files including launchd-drift-audit + skills/worldarchitect + browserclaw spec — should split into 3-4 PRs.
- **Gate 3 (PR exists)**: Merging a branch via `git push origin main` directly bypasses 7-green, CodeRabbit, Skeptic, and reviewer accountability. Forbidden by CLAUDE.md "Merge safety" rule.
- **Gate 4 (7-green + Skeptic)**: All 4 PR green criteria from CLAUDE.md 7-green table must hold (CI green, no conflicts, CR APPROVED, Bugbot clean, comments resolved, evidence pass, Skeptic PASS).
- **Gate 5 (MERGE APPROVED)**: Per CLAUDE.md merge-safety: literal phrase "MERGE APPROVED" is the ONLY valid trigger. "drive to 7-green", "go ahead", "ship it", "looks good" are NOT merge authorization on their own.

## Anti-patterns (caught in 2026-06-19 session)

- Uncommitted changes silently dropped on merge
- Scope creep — branch name doesn't match commits
- Merging without a PR (`git push origin main`)
- Untracked `??` + deleted `D` files easy to miss if you only look at `M`
- Working in `~/.hermes/` directly bypasses the staging canary gate

## Sources

- [feedback-2026-06-19-hermes-liveness-and-merge-readiness](../sources/feedback-2026-06-19-hermes-liveness-and-merge-readiness.md) — primary source, verification on `fix/mcp-daemon-keepalive`
- CLAUDE.md "Worktree Isolation — Edit Your Copy, Not ~/.hermes/ Directly" + "Merge safety — explicit MERGE APPROVED required"
- [MergeConflictResolution](MergeConflictResolution.md) — adjacent concept (how to handle merge conflicts that arise after gates 1-4 pass)
- [MergeReadiness](MergeReadiness.md) — existing related concept
- [MergeReadinessContract](MergeReadinessContract.md) — existing related concept (admin override path)

## Connections

- [HermesLivenessProtocol](HermesLivenessProtocol.md) — companion protocol; "is Hermes working" is the precondition for "can we merge"
- [[WorktreeIsolation]] — staging canary gate rule
- [[MergeApprovedPattern]] — the literal phrase requirement (gate 5)
- [PhantomRevert](PhantomRevert.md) — adjacent risk class caught by `git diff origin/main..HEAD` (gate 2)
- [fix-mcp-daemon-keepalive](../entities/fix-mcp-daemon-keepalive.md) — branch that triggered the 2026-06-19 verification (5/5 gates failed)