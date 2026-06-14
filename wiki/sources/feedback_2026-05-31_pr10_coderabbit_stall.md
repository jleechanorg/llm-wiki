---
title: "PR #10 CodeRabbit Stall — dark-factory (2026-05-31)"
type: source
tags: [dark-factory, coderabbit, admin-merge, pr-workflow]
date: 2026-05-31
source_file: raw/feedback_2026-05-31_pr10_coderabbit_stall.md
bead: jleechan-xpv
---

## Summary
CodeRabbit stalls on dark-factory PRs in two flavors: (1) COMMENTED-stall — won't re-review already-reviewed commits, and (2) perpetual-nitpick treadmill — re-reviews but files new low-severity items on every pass without ever auto-dismissing its own change request. Once actionable CR items are fixed + CI green + local suite green, admin squash-merge is the correct fallback. No branch protection on dark-factory.

## Key Claims
- CodeRabbit's `request_changes_workflow: true` config must be set BEFORE its first review; otherwise the CHANGES_REQUESTED → APPROVED cycle never initiates and CR stays COMMENTED.
- Bugbot auto-re-evaluates on new pushes (NEUTRAL → SUCCESS) once flagged issues are fixed; CodeRabbit does NOT have this property in the same way.
- Per-PR resolution: (a) `.coderabbit.yaml` with `request_changes_workflow: true` at repo root (Write tool blocks this — use `cat > file << 'EOF'` via Bash), (b) admin merge via `gh pr merge N --squash --admin` if all other gates pass.
- Gate 6 (Evidence): N/A for dark-factory — no evidence-review-bot or evidence-gate CI workflow exists.
- PR #16 addendum: even when CR re-reviews, it generates new nitpicks faster than it clears old ones — chasing APPROVED is a treadmill.
- Pre-merge re-check (mandatory): `gh pr view <N> --json headRefOid,mergeable,reviewDecision` — confirm `mergeable=MERGEABLE` and local HEAD == remote branch HEAD.

## Key Quotes
> "Once (a) every *actionable/substantive* CR item is fixed and individually verified, (b) CI is green, and (c) the local test suite is green, **stop chasing APPROVED** — admin squash-merge per explicit operator authorization"

> "Chasing CodeRabbit to a clean `APPROVED` on this repo is a treadmill. It generates new nitpicks faster than it clears old ones."

## Connections
- [[CodeRabbitDismissedPattern]] — CR never auto-dismisses its own change request
- [[CodeRabbitStaleLineRefs]] — CR line refs don't update after function renames
- [[SkepticGateCodeRabbit]] — Skeptic Gate vs CodeRabbit conflict
- [[AdminOverrideContract]] — admin-merge protocol
- [[TerminalAdministrator]] — operator's explicit "merge it" gate
- [[ServerOwnedAdministrativeFlags]] — admin flag management
- [[AdministrativeStatePoisoning]] — what's poisoned when admin state diverges
