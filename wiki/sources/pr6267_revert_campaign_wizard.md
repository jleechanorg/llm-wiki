---
title: "PR #6267 — Revert 'feat: re-enable LLM-driven Custom Campaign Wizard with bug fixes'"
type: source
tags: [revert, campaign-wizard, repo-integrity, CI]
date: 2026-04-14
source_file: wiki/sources/pr6267_revert_campaign_wizard.md
---

## Summary
Reverts PR #6034 which accidentally acted as a destructive revert — deleting docs, tests, and repo-level hooks including `.claude/hooks/block-merge.sh`. Restores repository integrity by re-adding the block-merge hook and fixing CI scope. Medium risk: changes repo-level automation and CI behavior but does not alter production runtime code paths.

## Key Claims
- PR #6034 was an accidental destructive revert that deleted docs, tests, and Claude hooks
- Reverted to restore: `.claude/hooks/block-merge.sh` PreToolUse hook
- `.claude/settings.json` wires block-merge hook to deny `gh pr merge` attempts unless human-approved
- `coverage.yml` scoped to `main` pushes only (avoids duplicate PR runs)
- New `wiki-html.yml` workflow auto-regenerates and commits `docs/wiki/**/*.html` from `wiki/**`
- Also restores 4 documentation/getting-started guides and D&D 5e mechanics references

## Key Quotes
> "Reverts PR 6034. PR 6034 accidentally acted as a massive destructive revert branch that deleted docs, tests, and repo-level hooks (.claude/hooks/block-merge.sh). Reverting to restore repository integrity." — PR description

## Connections
- [[Campaign Wizard]] — feature was reverted
- [[repo-integrity]] — block-merge.sh hook prevents unintended agent merges
- [[CI Automation]] — coverage.yml scoped to main, wiki-html.yml added
