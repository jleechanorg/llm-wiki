---
title: "Integrate Hard-Stop Pattern (feature, not bug)"
type: concept
tags: [integrate, git, branch, safety, pattern]
last_updated: 2026-06-19
---

# Integrate Hard-Stop Pattern

`integrate.sh` is a shell script that creates a fresh `dev{timestamp}` branch from `origin/main` to start clean. It has 4 hard-stops that prevent silent data loss:

1. **Uncommitted changes** (`M` or `??` in `git status`)
2. **Local-only commits** (commits not pushed to origin)
3. **Unmerged integration PRs** (a previous `/integrate` PR still open)
4. **`git checkout main` failure** (when main lives in another worktree)

The script supports `--force` to override ALL hard stops, and `--new-branch` to skip deletion.

## The hard-stop is a feature

When integrate.sh hard-stops, the correct response is NOT to add `--force`. The hard-stop is a guardrail preventing silent data loss:

- Uncommitted changes get silently dropped when the script checks out a new branch from origin/main
- Local-only commits get stranded on the old branch when the script deletes it (without `--new-branch`)
- Unmerged integration PRs get duplicated work if you integrate again before the previous PR merges

## Mandatory sub-rule: never `--force` without explicit human approval

`./integrate.sh --force` overrides all hard-stops. CLAUDE.md push-safety rule applies by analog:

> "No `git push --force` / `--force-with-lease` without explicit in-thread human approval naming target branch."

If a user types `/integrate --force`, stop and ask for explicit confirmation:

> "I need to run `./integrate.sh --force` on `fix/mcp-daemon-keepalive` because [reason]. This will discard/strand: [list]. Approve --force?"

## Hard-stop as a state-quality signal

A hard-stop is essentially a free lint check. Use it to:

1. Diagnose why the state is bad (run the 5-gate merge-readiness check)
2. Decide which option in the decision matrix applies
3. Execute the chosen path
4. Re-run integrate.sh without `--force`

This converts a "blocked" outcome into a diagnostic workflow. The integrate.sh hard-stop catches the same anti-patterns as the merge-readiness protocol.

## Global-script fallback (no local integrate.sh)

When a repo has no repository-local `./integrate.sh` (e.g. dark-factory,
2026-08-28), `/integrate` treats the maintained global script under
`~/.claude/plugins/marketplaces/claude-commands-marketplace/scripts/integrate.sh`
as the fallback implementation rather than a terminal failure — verified by
content/hash against the top-level marketplace copy, since the two files can
share an identical filesystem mtime. The same hard-stop discipline applies:
run without `--force` first, and if a backup branch hard-stops on local
commits, use `--new-branch` to preserve it and branch fresh from
`origin/main` instead of forcing past the guard. See
[feedback-2026-08-28-integrate-global-script-fallback](../sources/feedback-2026-08-28-integrate-global-script-fallback.md).

## Known gap (fix candidate)

integrate.sh reports only `M` (modified tracked) files, not `??` (untracked) files. Untracked files pass the hard-stop and get silently lost on checkout.

**Fix**: change `git status` to `git status --porcelain` in the hard-stop check (one-line change in integrate.sh).

## Sources

- [feedback-2026-06-19-integrate-hard-stop-uncommitted-state](../sources/feedback-2026-06-19-integrate-hard-stop-uncommitted-state.md) — primary source
- [[feedback-2026-06-12-integrate-sh-worktree-main-elsewhere]] — prior integrate.sh hard-stop case (different trigger)
- CLAUDE.md "Worktree Isolation — Edit Your Copy, Not ~/.hermes/ Directly"

## Connections

- [UncommittedStateDecisionMatrix](UncommittedStateDecisionMatrix.md) — the 4-option matrix to apply after a hard-stop
- [MergeReadinessGate](MergeReadinessGate.md) — sibling protocol that catches the same state pollution pre-merge
- [HermesLivenessProtocol](HermesLivenessProtocol.md) — companion protocol
- [[WorktreeIsolation]] — context: the `~/.hermes/` editing rule this pattern enforces
- [fix-mcp-daemon-keepalive](../entities/fix-mcp-daemon-keepalive.md) — branch that triggered the 2026-06-19 verification