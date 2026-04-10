---
title: "Repo Identity Check"
type: concept
tags: [validation, github, repository, identity]
sources: [smartclaw-routing-delegation-failures-postmortem.md]
last_updated: 2026-04-07
---

## Description
A mandatory validation step performed before creating PRs to verify the correct repository context. Implemented after the March 2026 delegation routing failure.

## Validation Steps
1. `git remote -v` — verify git remote configuration
2. `gh repo view --json nameWithOwner` — confirm GitHub repo identity
3. Explicit `gh pr create --repo <target-repo> ...` — force correct repo in command

## Why It Matters
Prevents work from being committed to wrong repository due to stale session context or ambiguous dispatch prompts.
