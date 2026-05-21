---
name: lite-green-merge-bypass
description: Docs-only PRs qualify for lite-green (3 gates); Green Gate times out polling Skeptic VERDICT — merge directly when 3 gates pass
type: feedback
bead: none
---

## Context

The `Green Gate` CI workflow runs the full 7-green check including polling for a Skeptic Gate VERDICT comment. On docs-only PRs the Skeptic Gate may not post a VERDICT quickly (or at all), causing the Green Gate to time out after ~10–15 min.

## Rule

For **docs-only PRs** (no `mvp_site/**` or production code changes):

1. Classify as **lite-green** — only 3 gates required.
2. Verify manually:
   - `gh api repos/jleechanorg/worldarchitect.ai/commits/<SHA>/status --jq '.state'` = `success`
   - `gh pr view <N> --json mergeable --jq '.mergeable'` = `MERGEABLE`
   - `gh pr view <N> --json reviews --jq '[.reviews[] | select(.author.login == "coderabbitai")] | sort_by(.submittedAt) | reverse | .[0].state'` = `APPROVED`
3. Merge directly — do NOT wait for Green Gate to complete or Skeptic VERDICT.

## Why

Green Gate always polls for Skeptic VERDICT regardless of PR type. For docs PRs, this is unnecessary overhead. The 3 lite-green gates (CI, mergeable, CR APPROVED) are sufficient per `~/.claude/skills/pr-green-definition.md`.

## Observed in

PR #6942 (`chore/trim-claude-md`), 2026-05-16. Green Gate ran for 15+ min polling for Skeptic VERDICT that never came. Merged after confirming 3 lite-green gates passed.

**How to apply:** When Green Gate is stuck in "Poll for VERDICT", check PR files — if all docs/skills, do lite-green check and merge.
