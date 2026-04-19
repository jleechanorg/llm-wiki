---
title: "Scope Drift"
type: concept
tags: []
date: 2026-04-19
---

## Definition

A PR or change introduces behavioral modifications that go beyond its stated goals, without those modifications being explicitly disclosed or justified in the PR body.

## Key Characteristics

- **Unstated behavior changes**: The diff contains changes that affect user-visible behavior (UI, API contracts, game mechanics) that are not mentioned in the PR goals or summary
- **Silent scope expansion**: A PR claiming to fix "X" also modifies "Y" and "Z" without separate PRs or explicit acknowledgment
- **Evidence mismatch**: The PR body claims "no UI changes" while the diff contains UI-visible changes

## Examples from WorldArchitect.AI

- PR #6370: Claimed to fix stale level-up flags, but also changed ASI choices from multiclass-only to all-classes, and changed `xp_gained` display from computed overflow to `rewards_pending.xp_gained`

## Detection

1. Diff review for behavior-affecting changes beyond stated scope
2. Check PR body claims (e.g., "UI evidence is N/A") against actual diff for UI-visible changes
3. Cross-reference with existing concept pages for known behavior contracts

## Prevention

- Require PR bodies to explicitly list all behavior changes, not just the primary fix
- Split PRs when multiple behaviors are being changed
- Use the [[SevenGreenQueue]] discipline: explicit scope statement required before merge
