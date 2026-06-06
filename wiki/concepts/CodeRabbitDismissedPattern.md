---
title: "CodeRabbitDismissedPattern"
type: concept
tags: []
sources: []
last_updated: 2026-06-06
---

## Summary
CR DISMISSED means CodeRabbit ran but found nothing to comment on, so it auto-dismisses its review. An empty commit does NOT re-trigger CR re-review. A **substantive code change** is required to get CR to post a new review.

A related failure mode is the **stall** — CR never cleanly reaches `APPROVED` even when the PR is genuinely ready. Two observed flavors (see "Stall variants" below). Resolution for both: once every *actionable* item is fixed+verified, CI is green, and the local suite is green, **stop chasing APPROVED** and admin squash-merge per explicit operator authorization.

## Pattern
- **CHANGES_REQUESTED**: CR found issues → push fixes → CR re-reviews → may move to COMMENTED or APPROVED
- **DISMISSED**: CR ran but found nothing → auto-dismissed → push of any kind does NOT trigger re-review
- **Workaround for DISMISSED**: Push a **substantive code change** (not empty commit). CR re-triggers on actual diff changes.

## Examples
- PR #6287: CR posted 5 DISMISSED reviews. Pushed empty commit `008c674289` to trigger re-review — CR did NOT re-review. Then pushed substantive fix `5c1875808d` (using `rewards_box` param in `_infer_level_up_target_from_xp`) — CR re-triggered.

## How to Apply
When CR shows DISMISSED on a PR that needs APPROVED (7-green requirement):
1. Do NOT push empty commit to "trigger CI/CR" — it won't work
2. Instead, make a substantive code fix and push that
3. If no real code change is possible, close the PR and re-create with a different approach

## Stall variants (CR never reaches APPROVED)
Two distinct stalls seen on the `jleechanorg/dark-factory` repo (no branch protection):

- **COMMENTED-stall (PR #10, 2026-05-31):** CR will not re-review already-reviewed commits and won't auto-approve unless `request_changes_workflow: true` was configured BEFORE its first review. It stays in COMMENTED indefinitely. Mitigation: add a root `.coderabbit.yaml` with `request_changes_workflow: true` *before the first PR push*.
- **Perpetual-nitpick treadmill (PR #16, 2026-06-06):** CR DOES re-review each new head (415c77f, dcd5810) — so "won't re-review" is not universal — but on **every** pass files a fresh `CHANGES_REQUESTED` carrying **new** low-severity nitpicks (unused loop var, `_git` fail-fast on non-zero rc, a RESULTS.md typo, then 9 more + re-raised "Duplicate"s). It never auto-dismisses its own change request and never flips `reviewDecision` to APPROVED, even with CI green and local suite 226 passed. Chasing APPROVED is a treadmill — CR generates nitpicks faster than it clears them.

### Resolution (both stalls)
Once (a) every *actionable/substantive* CR item is fixed and individually verified, (b) CI is green, and (c) the local test suite is green → **stop chasing APPROVED** → admin squash-merge per explicit operator authorization:
```
gh pr merge <N> --admin --squash --delete-branch
```
**Mandatory pre-merge re-check even when overriding:** `gh pr view <N> --json headRefOid,mergeable,reviewDecision`; confirm `mergeable=MERGEABLE` and local HEAD == remote branch HEAD before merging. Verify each CR "fix" with a local suite run *before* pushing. No branch protection on dark-factory (re-confirmed 2026-06-06), so `--admin` works. PR #16 merged 2026-06-06 → squash commit `d010cf6` on main (`4b8b921 → d010cf6`). Bead `jleechan-xpv`.
