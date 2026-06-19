---
title: "integrate.sh hard-stop on uncommitted state — decision matrix + never --force"
type: source
tags: [integrate, git, branch, worktree-isolation, verification, protocol]
date: 2026-06-19
source_file: feedback_2026-06-19_integrate_hard_stop_uncommitted_state.md
---

## Summary
`/integrate` correctly hard-stopped on `fix/mcp-daemon-keepalive` with 11 uncommitted `M` files. The hard-stop is a feature, not a bug — it prevents silent data loss when checking out a new branch from origin/main. The response is NOT to add `--force`; it's to work a 4-option decision matrix (split into scoped PRs / commit as-is / stash / discard). Mandatory sub-rule: never `./integrate.sh --force` without explicit in-thread human approval (analog to push-safety rule). Special warning: `workspace/SOUL.md` is a live symlink, so discarding its `M` silently reverts live policy.

## Key Claims
- integrate.sh has 4 hard-stops: uncommitted changes, local-only commits, unmerged integration PRs, `git checkout main` failure in worktree.
- The correct response to a hard-stop is to work the decision matrix, NOT to add `--force`.
- 4-option decision matrix: (A) split into scoped PRs for scope creep, (B) commit as-is for coherent single concern, (C) stash for WIP, (D) discard for wrong/obsolete changes.
- `workspace/SOUL.md` modifications are live-policy changes via symlink; discard silently reverts runtime policy.
- Minor gap: integrate.sh reports only `M` files, not `??` (untracked) — untracked files pass the hard-stop check and get silently lost on checkout. Fix candidate: use `git status --porcelain` (one-line change).

## Key Quotes
> "HARD STOP: You have uncommitted changes on 'fix/mcp-daemon-keepalive'. Please commit or stash your changes before integrating." — integrate.sh output 2026-06-19 03:40Z

> "No `git push --force` / `--force-with-lease` without explicit in-thread human approval naming target branch." — CLAUDE.md push-safety rule (analog applies to `--force` in integrate.sh)

## Connections
- [[IntegrateHardStopPattern]] — the hard-stop is a feature, not a bug
- [[UncommittedStateDecisionMatrix]] — the 4-option matrix (A/B/C/D)
- [[HermesLivenessProtocol]] + [[MergeReadinessGate]] — companion protocols in the same session
- [[WorktreeIsolation]] — context: `workspace/SOUL.md` symlink warning
- [[fix-mcp-daemon-keepalive]] — the branch that triggered the hard-stop
- [[PhantomRevert]] — adjacent risk: branches whose own diff looks clean but revert main work